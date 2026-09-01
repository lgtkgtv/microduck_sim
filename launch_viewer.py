#!/usr/bin/env python3
"""
launch_viewer.py
Comprehensive Interactive MuJoCo Simulation Viewer for the Pollen Robotics Microduck.

Architecture:
- ViewerConfig: Configuration parameters, physical limits, and nominal poses.
- ActionLogger: Colorized, structured console logging of user intents and system responses.
- SimulationState: Thread-safe state container for driving commands, heading, and physics clocks.
- PolicyController: 61-D observation assembly, 50Hz inference decimation, and closed-loop heading stabilization.
- TerminalInputListener: Background daemon thread for seamless non-blocking terminal input.
- MuJoCoViewer: GLFW rendering loop, orbit/pan/zoom camera, spring perturbations, visual toggles, and HUD overlay.
"""

import os
import sys
import time
import math
import argparse
import threading
import select
from dataclasses import dataclass
import glfw
import mujoco
import numpy as np
import OpenGL.GL as gl

# Optional ONNX Runtime for policy playback
try:
    import onnxruntime as ort
    HAS_ONNX = True
except ImportError:
    HAS_ONNX = False


# ==============================================================================
# 1. Configuration & Constants
# ==============================================================================
@dataclass
class ViewerConfig:
    """Simulation and locomotion parameters."""
    # 14-actuator nominal standing pose (left leg, neck/head, right leg)
    DEFAULT_POSITION_14 = np.array([
        0.0, -0.0873, -0.4579, -0.0049, 0.4530,  # Left Leg: hip_yaw, hip_roll, hip_pitch, knee, ankle
        0.3491, 0.3491, 0.0, 0.0,               # Neck/Head: neck_pitch, head_pitch, head_yaw, head_roll
        0.0, 0.0873, 0.4579, 0.0049, -0.4530    # Right Leg: hip_yaw, hip_roll, hip_pitch, knee, ankle
    ], dtype=np.float32)

    # Locomotion velocities
    FORWARD_VX: float = 0.22        # m/s forward walking
    BACKWARD_VX: float = -0.24      # m/s reverse walking
    TURN_VX: float = 0.20           # m/s forward speed while turning
    HEADING_STEP_DEG: float = 35.0  # degrees heading change per A/D press
    HEADING_KP: float = 1.5         # Course correction gain
    MAX_YAW_RATE: float = 0.65      # Max yaw command magnitude (rad/s)
    ACTION_SCALE: float = 0.40      # Policy action scaling factor
    
    # Timing
    PHYSICS_TIMESTEP: float = 0.002 # 500 Hz physics
    POLICY_DECIMATION: int = 10     # 50 Hz policy (500 / 10)


# ==============================================================================
# 2. Action & Telemetry Logger
# ==============================================================================
class ActionLogger:
    """Formatted, structured console logger for user actions and system states."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @classmethod
    def log_action(cls, key_name: str, action_desc: str, details: str = ""):
        """Logs an explicit user action and the engine's response."""
        timestamp = time.strftime("%H:%M:%S")
        prefix = f"{cls.CYAN}[{timestamp}]{cls.RESET} {cls.BOLD}[USER INPUT: {key_name}]{cls.RESET}"
        msg = f"{cls.GREEN}➔ {action_desc}{cls.RESET}"
        if details:
            msg += f" {cls.YELLOW}({details}){cls.RESET}"
        print(f"\r{prefix} {msg}")

    @classmethod
    def log_status(cls, status_msg: str):
        """Prints a general status message."""
        print(f"\r{cls.BLUE}ℹ️  {status_msg}{cls.RESET}")

    @classmethod
    def log_error(cls, error_msg: str):
        """Prints an error message."""
        print(f"\r{cls.RED}❌ ERROR: {error_msg}{cls.RESET}")


# ==============================================================================
# 3. Simulation State Container
# ==============================================================================
class SimulationState:
    """Encapsulates the dynamic state of the simulation and user controls."""
    def __init__(self, config: ViewerConfig):
        self.config = config
        self.cmd_vx: float = 0.0
        self.cmd_vy: float = 0.0
        self.cmd_vtheta: float = 0.0
        self.target_heading: float = 0.0  # Radians in world frame
        self.paused: bool = False
        self.step_count: int = 0
        self.sim_time_accumulator: float = 0.0
        self.last_action = np.zeros(14, dtype=np.float32)
        self.last_infer_time_ms: float = 0.0

    @property
    def is_driving(self) -> bool:
        """Returns True if user has commanded active movement."""
        return abs(self.cmd_vx) > 0.02 or abs(self.cmd_vtheta) > 0.02

    def reset_controls(self):
        """Resets velocity commands and target heading to zero."""
        self.cmd_vx = 0.0
        self.cmd_vy = 0.0
        self.cmd_vtheta = 0.0
        self.target_heading = 0.0
        self.last_action.fill(0.0)


# ==============================================================================
# 4. Policy Controller & Kinematics Math
# ==============================================================================
def quat_rotate_inverse(q: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Rotates a vector v from world frame into body frame using quaternion q."""
    qc = np.array([q[0], -q[1], -q[2], -q[3]], dtype=np.float64)
    res = np.zeros(3, dtype=np.float64)
    mujoco.mju_rotVecQuat(res, v.astype(np.float64), qc)
    return res

def quat_to_yaw(q: np.ndarray) -> float:
    """Extracts yaw angle (radians) from quaternion [w, x, y, z]."""
    return math.atan2(2.0 * (q[0]*q[3] + q[1]*q[2]), 1.0 - 2.0 * (q[2]**2 + q[3]**2))

def wrap_to_pi(angle: float) -> float:
    """Wraps an angle to [-pi, +pi]."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


class PolicyController:
    """Manages ONNX policy execution, 61-D observation assembly, and closed-loop heading lock."""
    def __init__(self, policy_path: str, config: ViewerConfig):
        self.config = config
        self.policy_path = policy_path
        self.session = None
        self.input_name = "obs"

        if policy_path and HAS_ONNX and os.path.exists(policy_path):
            try:
                self.session = ort.InferenceSession(policy_path)
                inputs = self.session.get_inputs()
                self.input_name = inputs[0].name if inputs else "obs"
                ActionLogger.log_status(f"Loaded ONNX Locomotion Policy: {os.path.basename(policy_path)} (Input: '{self.input_name}')")
            except Exception as e:
                ActionLogger.log_error(f"Failed to load ONNX policy: {e}")
                self.session = None

    def step(self, model: mujoco.MjModel, data: mujoco.MjData, state: SimulationState):
        """Executes a single 50Hz control step or holds nominal standing posture."""
        if self.session and state.is_driving:
            if state.step_count % self.config.POLICY_DECIMATION == 0:
                t0 = time.time()
                obs = np.zeros((1, 61), dtype=np.float32)

                # 1. Base gyro in trunk frame (freejoint qvel[3:6] is in body frame)
                trunk_quat = data.qpos[3:7] if len(data.qpos) >= 7 else np.array([1.0, 0.0, 0.0, 0.0])
                trunk_gyro = data.qvel[3:6] if len(data.qvel) >= 6 else np.zeros(3)
                obs[0, 0:3] = trunk_gyro

                # 2. Projected gravity vector in trunk frame
                obs[0, 3:6] = quat_rotate_inverse(trunk_quat, np.array([0.0, 0.0, -1.0]))

                # 3. Joint angles relative to nominal home pose
                if len(data.qpos) >= 21:
                    obs[0, 6:20] = (data.qpos[7:21] - self.config.DEFAULT_POSITION_14).astype(np.float32)
                if len(data.qvel) >= 20:
                    obs[0, 20:34] = data.qvel[6:20].astype(np.float32)

                # 4. Previous action feedback
                obs[0, 34:48] = state.last_action

                # 5. Closed-Loop Heading Stabilization
                current_yaw = quat_to_yaw(trunk_quat)
                yaw_err = wrap_to_pi(current_yaw - state.target_heading)
                effective_vtheta = float(np.clip(-self.config.HEADING_KP * yaw_err, -self.config.MAX_YAW_RATE, self.config.MAX_YAW_RATE))

                # 6. Command twist vector [vx, vy, vtheta]
                obs[0, 48] = state.cmd_vx
                obs[0, 49] = state.cmd_vy
                obs[0, 50] = effective_vtheta

                try:
                    raw_action = self.session.run(None, {self.input_name: obs})[0].flatten()
                    state.last_action = raw_action.copy()
                    target_pos = self.config.DEFAULT_POSITION_14 + self.config.ACTION_SCALE * raw_action
                    data.ctrl[:model.nu] = target_pos[:model.nu]
                except Exception as e:
                    ActionLogger.log_error(f"Inference error: {e}")

                state.last_infer_time_ms = (time.time() - t0) * 1000.0
        else:
            # Nominal Passive / Active Standing Stance Hold
            if model.nu >= 14:
                data.ctrl[:14] = self.config.DEFAULT_POSITION_14
            state.last_action.fill(0.0)


# ==============================================================================
# 5. Non-Blocking Terminal Input Listener
# ==============================================================================
class TerminalInputListener(threading.Thread):
    """Listens for single keypresses on terminal stdin without requiring Enter."""
    def __init__(self, callback):
        super().__init__(daemon=True)
        self.callback = callback
        self.running = True

    def run(self):
        try:
            import termios
            import tty
            if not sys.stdin.isatty():
                return
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                while self.running:
                    rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
                    if rlist:
                        ch = sys.stdin.read(1)
                        if ch:
                            self.callback(ch)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            pass


# ==============================================================================
# 6. MuJoCo Interactive Viewer & OpenGL Renderer
# ==============================================================================
class MuJoCoViewer:
    """Manages GLFW window, camera, user inputs, perturbation, and simulation loop."""
    def __init__(self, model_path: str, policy_path: str, speed_multiplier: float = 1.0):
        self.config = ViewerConfig()
        self.model_path = model_path
        self.speed_multiplier = speed_multiplier
        self.state = SimulationState(self.config)
        self.policy = PolicyController(policy_path, self.config)

        # Build full MuJoCo scene XML with ground plane
        scene_xml = f"""
        <mujoco>
            <option gravity="0 0 -9.81" timestep="{self.config.PHYSICS_TIMESTEP}" iterations="50" solver="Newton" cone="elliptic"/>
            <asset>
                <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="512"/>
                <texture name="texplane" type="2d" builtin="checker" rgb1=".25 .3 .35" rgb2=".15 0.18 0.22" width="512" height="512" mark="cross" markrgb=".8 .8 .8"/>
                <material name="matplane" reflectance="0.2" texture="texplane" texrepeat="2 2" texuniform="true"/>
            </asset>
            <worldbody>
                <light directional="true" diffuse=".9 .9 .9" specular=".3 .3 .3" pos="0 0 4" dir="0 0 -1"/>
                <geom name="floor" type="plane" pos="0 0 0" size="10 10 0.1" material="matplane" contype="1" conaffinity="1" friction="2.0 0.01 0.001" solref="0.004 1" solimp="0.95 0.99 0.001 0.5 2"/>
            </worldbody>
            <include file="{self.model_path}"/>
        </mujoco>
        """

        self.model = mujoco.MjModel.from_xml_string(scene_xml)
        self.data = mujoco.MjData(self.model)

        # Viewer structures
        self.camera = mujoco.MjvCamera()
        self.option = mujoco.MjvOption()
        self.scene = mujoco.MjvScene(self.model, maxgeom=10000)
        self.context = None
        self.perturb = mujoco.MjvPerturb()
        self.window = None

        # Interaction mouse states
        self.button_left = False
        self.button_middle = False
        self.button_right = False
        self.last_x = 0.0
        self.last_y = 0.0

        # Initialize posture
        self.reset_to_standing()

        # Terminal input thread
        self.term_listener = TerminalInputListener(self.process_command_char)
        self.term_listener.start()

    def reset_to_standing(self):
        """Resets the robot to an upright standing posture resting stably on the floor."""
        mujoco.mj_resetData(self.model, self.data)
        if self.model.nq >= 21:
            self.data.qpos[0:3] = [0.0, 0.0, 0.125]
            self.data.qpos[3:7] = [1.0, 0.0, 0.0, 0.0]
            self.data.qpos[7:21] = self.config.DEFAULT_POSITION_14
        if self.model.nu >= 14:
            self.data.ctrl[:14] = self.config.DEFAULT_POSITION_14
        self.data.qvel[:] = 0.0
        mujoco.mj_forward(self.model, self.data)
        self.state.reset_controls()

    def get_current_yaw(self) -> float:
        """Returns the current yaw of trunk_base in radians."""
        trunk_quat = self.data.qpos[3:7] if len(self.data.qpos) >= 7 else np.array([1.0, 0.0, 0.0, 0.0])
        return quat_to_yaw(trunk_quat)

    def process_command_char(self, key_char: str):
        """Processes high-level user command characters from terminal or GLFW."""
        k = key_char.lower()
        if k in ('w', 'up'):
            self.state.cmd_vx = self.config.FORWARD_VX
            self.state.target_heading = self.get_current_yaw()
            ActionLogger.log_action("W / UP", "Forward Walking", f"vx={self.state.cmd_vx:+.2f} m/s, Heading Latch={math.degrees(self.state.target_heading):+.0f}°")
        elif k in ('s', 'down'):
            self.state.cmd_vx = self.config.BACKWARD_VX
            self.state.target_heading = self.get_current_yaw()
            ActionLogger.log_action("S / DOWN", "Backward Walking", f"vx={self.state.cmd_vx:+.2f} m/s, Heading Latch={math.degrees(self.state.target_heading):+.0f}°")
        elif k in ('a', 'left'):
            self.state.cmd_vx = self.config.TURN_VX
            self.state.target_heading = wrap_to_pi(self.state.target_heading + math.radians(self.config.HEADING_STEP_DEG))
            ActionLogger.log_action("A / LEFT", "Steer Left", f"+{self.config.HEADING_STEP_DEG:.0f}° ➔ New Target Heading={math.degrees(self.state.target_heading):+.0f}°")
        elif k in ('d', 'right'):
            self.state.cmd_vx = self.config.TURN_VX
            self.state.target_heading = wrap_to_pi(self.state.target_heading - math.radians(self.config.HEADING_STEP_DEG))
            ActionLogger.log_action("D / RIGHT", "Steer Right", f"-{self.config.HEADING_STEP_DEG:.0f}° ➔ New Target Heading={math.degrees(self.state.target_heading):+.0f}°")
        elif k == 'x':
            self.state.reset_controls()
            ActionLogger.log_action("X", "Emergency Stop", "Motors locked in stable standing stance")
        elif k == 'r':
            self.reset_to_standing()
            ActionLogger.log_action("R", "Reset Robot", "Respawned upright at origin")
        elif k == ' ':
            self.state.paused = not self.state.paused
            ActionLogger.log_action("SPACE", "Pause Toggle", "PAUSED" if self.state.paused else "RESUMED")

    def print_diagnostics(self):
        """Prints startup model diagnostics and kinematics table."""
        print("=" * 65)
        print("🦆 Microduck Physical AI Simulation & Masterclass Viewer")
        print("=" * 65)
        print(f"Loading MJCF model from: {self.model_path}")
        print("✅ Model and Scene loaded successfully!")
        print(f"  • Generalized coordinates (nq) : {self.model.nq}")
        print(f"  • Degrees of freedom (nv)      : {self.model.nv}")
        print(f"  • Number of joints (njnt)      : {self.model.njnt}")
        print(f"  • Number of bodies (nbody)     : {self.model.nbody}")
        print(f"  • Number of geoms (ngeom)      : {self.model.ngeom}")
        print(f"  • Number of actuators (nu)     : {self.model.nu}")
        print(f"  • Timestep                     : {self.model.opt.timestep:.4f} s ({1.0/self.model.opt.timestep:.0f} Hz)")
        print("-" * 65)
        print("🎮 Controls Guide (Works in Terminal OR 3D Window):")
        print("  • 'W' / Up Arrow        : 🚶 Walk Straight Ahead (Heading Locked)")
        print("  • 'S' / Down Arrow      : 🔙 Walk Backward (vx = -0.24 m/s)")
        print("  • 'A' / 'D' (Left/Right): 🔄 Steer Left / Right (±35° course step)")
        print("  • 'X'                   : 🛑 Stop & Hold Standing Balance")
        print("  • 'R'                   : 🔄 Reset Position to Standing")
        print("  • Spacebar              : ⏸️ Pause / Resume Physics")
        print("  • Left Click + Drag     : Orbit Camera around Duck")
        print("  • Right Click + Drag    : Pan Camera")
        print("  • Scroll Wheel          : Zoom In / Out")
        print("  • Ctrl + Left Drag      : 🪢 Grab & Pull Body (Spring Perturbation)")
        print("  • [J]oints | [G] Sites | [C]ontacts | [I]nertia | [T]ransparent : Visual Toggles")
        print("  • ESC                   : Quit Viewer")
        print("=" * 65)

    def run_headless(self, steps: int = 500):
        """Runs the simulation headlessly for automated verification."""
        ActionLogger.log_status(f"Headless mode detected. Stepping physics {steps} times...")
        for _ in range(steps):
            self.policy.step(self.model, self.data, self.state)
            mujoco.mj_step(self.model, self.data)
            self.state.step_count += 1
        pos = self.data.qpos[:3]
        ActionLogger.log_status(f"Headless simulation completed: Trunk pos = [{pos[0]:+.4f}, {pos[1]:+.4f}, {pos[2]:.4f}]m")

    def run(self):
        """Main GLFW graphical viewer loop."""
        display = os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
        if not display:
            self.run_headless()
            return

        if not glfw.init():
            ActionLogger.log_error("Failed to initialize GLFW. Falling back to headless.")
            self.run_headless()
            return

        self.window = glfw.create_window(1280, 720, "Microduck Physical AI Interactive Simulation", None, None)
        if not self.window:
            glfw.terminate()
            self.run_headless()
            return

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        # Setup MuJoCo rendering context
        self.context = mujoco.MjrContext(self.model, mujoco.mjtFontScale.mjFONTSCALE_150)
        mujoco.mjv_defaultCamera(self.camera)
        mujoco.mjv_defaultOption(self.option)
        mujoco.mjv_defaultPerturb(self.perturb)

        # Set default camera orbit
        self.camera.azimuth = 135.0
        self.camera.elevation = -20.0
        self.camera.distance = 0.85
        self.camera.lookat = np.array([0.0, 0.0, 0.12])

        # Register GLFW callbacks
        glfw.set_mouse_button_callback(self.window, self._mouse_button_callback)
        glfw.set_cursor_pos_callback(self.window, self._cursor_pos_callback)
        glfw.set_scroll_callback(self.window, self._scroll_callback)
        glfw.set_key_callback(self.window, self._key_callback)

        self.print_diagnostics()

        sim_dt = self.model.opt.timestep
        last_wall_time = time.time()

        while not glfw.window_should_close(self.window):
            current_wall_time = time.time()
            elapsed_wall = current_wall_time - last_wall_time
            last_wall_time = current_wall_time

            if not self.state.paused:
                self.state.sim_time_accumulator += min(elapsed_wall * max(self.speed_multiplier, 0.1), 0.1)

                while self.state.sim_time_accumulator >= sim_dt:
                    # 1. Policy step / course-correction
                    self.policy.step(self.model, self.data, self.state)

                    # 2. Apply interactive perturbations
                    if self.perturb.active != 0:
                        mujoco.mjv_applyPerturbPose(self.model, self.data, self.perturb, 0)
                        mujoco.mjv_applyPerturbForce(self.model, self.data, self.perturb)

                    # 3. Advance physics
                    mujoco.mj_step(self.model, self.data)
                    self.state.step_count += 1
                    self.state.sim_time_accumulator -= sim_dt

            # Camera tracks robot root
            if self.model.nq >= 3:
                self.camera.lookat[0] = self.data.qpos[0]
                self.camera.lookat[1] = self.data.qpos[1]
                self.camera.lookat[2] = self.data.qpos[2]

            # Render scene
            width, height = glfw.get_framebuffer_size(self.window)
            viewport = mujoco.MjrRect(0, 0, width, height)
            mujoco.mjv_updateScene(self.model, self.data, self.option, self.perturb, self.camera, mujoco.mjtCatBit.mjCAT_ALL, self.scene)
            mujoco.mjr_render(viewport, self.scene, self.context)

            # Live HUD Overlay
            self._render_hud(viewport)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()
        ActionLogger.log_status("Viewer closed cleanly.")

    def _render_hud(self, viewport):
        """Renders live on-screen telemetry overlay."""
        q = self.data.qpos[3:7] if len(self.data.qpos) >= 7 else np.array([1.0, 0.0, 0.0, 0.0])
        roll = np.degrees(np.arctan2(2.0*(q[0]*q[1] + q[2]*q[3]), 1.0 - 2.0*(q[1]**2 + q[2]**2)))
        pitch = np.degrees(np.arcsin(2.0*(q[0]*q[2] - q[3]*q[1])))
        yaw = np.degrees(quat_to_yaw(q))
        z_height = self.data.qpos[2] if len(self.data.qpos) >= 3 else 0.0

        state_str = "PAUSED" if self.state.paused else ("WALKING" if self.state.is_driving else "STANDING")
        hud_left = (
            f"State: {state_str} | vx: {self.state.cmd_vx:+.2f} m/s | Target Heading: {math.degrees(self.state.target_heading):+.0f}°\n"
            f"Trunk z: {z_height:.3f}m | Roll: {roll:+.1f}° | Pitch: {pitch:+.1f}° | Yaw: {yaw:+.1f}°\n"
            f"Contacts: {self.data.ncon:2d} | Infer: {self.state.last_infer_time_ms:.1f}ms (50Hz)"
        )
        mujoco.mjr_overlay(
            mujoco.mjtFontScale.mjFONTSCALE_150,
            mujoco.mjtGridPos.mjGRID_TOPLEFT,
            viewport,
            hud_left,
            "",
            self.context
        )

    # GLFW Event Callbacks
    def _mouse_button_callback(self, win, button, act, mods):
        self.button_left = (glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
        self.button_middle = (glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
        self.button_right = (glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)
        self.last_x, self.last_y = glfw.get_cursor_pos(win)

        ctrl_pressed = (glfw.get_key(win, glfw.KEY_LEFT_CONTROL) == glfw.PRESS or glfw.get_key(win, glfw.KEY_RIGHT_CONTROL) == glfw.PRESS)

        if act == glfw.PRESS and ctrl_pressed:
            width, height = glfw.get_framebuffer_size(win)
            selpnt = np.zeros(3, dtype=np.float64)
            selgeom = np.zeros(1, dtype=np.int32)
            selskin = np.zeros(1, dtype=np.int32)
            selbody = mujoco.mjv_select(
                self.model, self.data, self.option, width / height,
                self.last_x / width, (height - self.last_y) / height,
                self.scene, selpnt, selgeom, selskin
            )
            if selbody >= 0:
                if self.button_left:
                    self.perturb.active = int(mujoco.mjtPertBit.mjPERT_TRANSLATE)
                elif self.button_right:
                    self.perturb.active = int(mujoco.mjtPertBit.mjPERT_ROTATE)
                mujoco.mjv_initPerturb(self.model, self.data, self.scene, self.perturb)
                body_name = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_BODY, selbody) or f"body_{selbody}"
                ActionLogger.log_action("CTRL+CLICK", "Spring Perturbation", f"Grabbed {body_name}")
        elif act == glfw.RELEASE:
            self.perturb.active = 0

    def _cursor_pos_callback(self, win, xpos, ypos):
        dx = xpos - self.last_x
        dy = ypos - self.last_y
        self.last_x = xpos
        self.last_y = ypos

        if not (self.button_left or self.button_right or self.button_middle):
            return

        width, height = glfw.get_framebuffer_size(win)
        ctrl_pressed = (glfw.get_key(win, glfw.KEY_LEFT_CONTROL) == glfw.PRESS or glfw.get_key(win, glfw.KEY_RIGHT_CONTROL) == glfw.PRESS)

        if ctrl_pressed and self.perturb.active != 0:
            action = int(mujoco.mjtMouse.mjMOUSE_MOVE_V) if self.button_right else int(mujoco.mjtMouse.mjMOUSE_MOVE_H)
            mujoco.mjv_movePerturb(self.model, self.data, action, dx / width, dy / height, self.scene, self.perturb)
            return

        if self.button_left:
            action = int(mujoco.mjtMouse.mjMOUSE_ROTATE_H) if abs(dx) > abs(dy) else int(mujoco.mjtMouse.mjMOUSE_ROTATE_V)
        elif self.button_right:
            action = int(mujoco.mjtMouse.mjMOUSE_MOVE_H) if abs(dx) > abs(dy) else int(mujoco.mjtMouse.mjMOUSE_MOVE_V)
        elif self.button_middle:
            action = int(mujoco.mjtMouse.mjMOUSE_ZOOM)
        else:
            action = int(mujoco.mjtMouse.mjMOUSE_NONE)

        mujoco.mjv_moveCamera(self.model, action, dx / width, dy / height, self.camera)

    def _scroll_callback(self, win, xoffset, yoffset):
        action = int(mujoco.mjtMouse.mjMOUSE_ZOOM)
        mujoco.mjv_moveCamera(self.model, action, 0.0, -0.05 * yoffset, self.camera)

    def _key_callback(self, win, key, scancode, act, mods):
        if act in (glfw.PRESS, glfw.REPEAT):
            # Motion controls
            if key in (glfw.KEY_W, glfw.KEY_UP):
                self.process_command_char('w')
            elif key in (glfw.KEY_S, glfw.KEY_DOWN):
                self.process_command_char('s')
            elif key in (glfw.KEY_A, glfw.KEY_LEFT):
                self.process_command_char('a')
            elif key in (glfw.KEY_D, glfw.KEY_RIGHT):
                self.process_command_char('d')
            elif key == glfw.KEY_X:
                self.process_command_char('x')

        if act == glfw.PRESS:
            if key == glfw.KEY_SPACE:
                self.process_command_char(' ')
            elif key in (glfw.KEY_R, glfw.KEY_BACKSPACE):
                self.process_command_char('r')
            elif key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(win, True)
                ActionLogger.log_action("ESC", "Quit Viewer", "Closing window")
            # Visual flag toggles
            elif key == glfw.KEY_J:
                self.option.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = not self.option.flags[mujoco.mjtVisFlag.mjVIS_JOINT]
                ActionLogger.log_action("J", "Toggle Joint Axes", f"Active={bool(self.option.flags[mujoco.mjtVisFlag.mjVIS_JOINT])}")
            elif key == glfw.KEY_G:
                self.option.sitegroup[3] = 0 if self.option.sitegroup[3] == 1 else 1
                ActionLogger.log_action("G", "Toggle Sensor Sites", f"SiteGroup3={self.option.sitegroup[3]}")
            elif key == glfw.KEY_C:
                curr = self.option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT]
                self.option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = not curr
                self.option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = not curr
                ActionLogger.log_action("C", "Toggle Contacts & Forces", f"Active={not curr}")
            elif key == glfw.KEY_I:
                self.option.flags[mujoco.mjtVisFlag.mjVIS_INERTIA] = not self.option.flags[mujoco.mjtVisFlag.mjVIS_INERTIA]
                ActionLogger.log_action("I", "Toggle Inertia Ellipsoids", f"Active={bool(self.option.flags[mujoco.mjtVisFlag.mjVIS_INERTIA])}")
            elif key == glfw.KEY_T:
                self.option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = not self.option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT]
                ActionLogger.log_action("T", "Toggle Transparency", f"Active={bool(self.option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT])}")
            elif key == glfw.KEY_F:
                self.option.flags[mujoco.mjtVisFlag.mjVIS_TEXTURE] = not self.option.flags[mujoco.mjtVisFlag.mjVIS_TEXTURE]
                ActionLogger.log_action("F", "Toggle Floor Texture", f"Active={bool(self.option.flags[mujoco.mjtVisFlag.mjVIS_TEXTURE])}")


# ==============================================================================
# 7. Main Entry Point
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Microduck Physical AI Interactive Simulation Viewer")
    parser.add_argument("--model", type=str, default=os.path.join(os.path.dirname(__file__), "kinematics", "assets", "alpha", "robot_walk.xml"), help="Path to robot XML")
    parser.add_argument("--policy", type=str, default=os.path.join(os.path.dirname(__file__), "policies", "alpha_walking.onnx"), help="Path to ONNX policy")
    parser.add_argument("--speed", type=float, default=1.0, help="Simulation playback speed multiplier")
    args = parser.parse_args()

    model_path = os.path.abspath(args.model)
    if not os.path.exists(model_path):
        ActionLogger.log_error(f"Model file not found: {model_path}")
        sys.exit(1)

    viewer = MuJoCoViewer(model_path=model_path, policy_path=args.policy, speed_multiplier=args.speed)
    viewer.run()


if __name__ == "__main__":
    main()
