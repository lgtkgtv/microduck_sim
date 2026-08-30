#!/usr/bin/env python3
"""
launch_viewer.py
Comprehensive Interactive MuJoCo Simulation Viewer for the Pollen Robotics Microduck.
Features:
- Complete Model Diagnostics & Kinematics Banner (nq, nv, njnt, nbody, dt, Hz)
- Full 3D Camera Controls (Orbit, Pan, Zoom) with Dynamic Root Tracking
- Interactive Physics Perturbation (Ctrl + Click & Drag to grab and pull bodies)
- Visual Flags Toggles ([J]oints, [S]ites, [C]ontacts, [I]nertia, [T]ransparent, [F]loor)
- Live Kinematics Telemetry HUD (Trunk z-height, IMU Roll/Pitch/Yaw, Toggle Status)
- Guaranteed In-Frame OpenGL Rendered Cursor (WSLg & Linux compatible)
"""

import os
import sys
import time
import math
import glfw
import mujoco
import numpy as np
import OpenGL.GL as gl

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, "kinematics", "assets", "alpha", "robot_walk.xml")

def quat_to_euler_deg(q):
    """Converts a quaternion [w, x, y, z] to Euler angles in degrees (roll, pitch, yaw)."""
    w, x, y, z = q
    # Roll (x-axis rotation)
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # Pitch (y-axis rotation)
    sinp = 2.0 * (w * y - z * x)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    # Yaw (z-axis rotation)
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return (math.degrees(roll), math.degrees(pitch), math.degrees(yaw))

def render_gl_cursor(x, y, win_w, win_h, fb_w, fb_h, is_dragging, is_perturbing):
    """
    Renders an in-frame, high-visibility 2D cursor directly onto the framebuffer.
    Resets MuJoCo's GLSL shader program and VAOs so fixed-function 2D rendering works.
    """
    # 1. Reset Modern OpenGL shader state
    gl.glUseProgram(0)
    gl.glBindVertexArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    # 2. Viewport and Projection
    gl.glViewport(0, 0, fb_w, fb_h)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPushMatrix()
    gl.glLoadIdentity()
    gl.glOrtho(0, win_w, win_h, 0, -1, 1)

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPushMatrix()
    gl.glLoadIdentity()

    # 3. Blending and 2D state
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_CULL_FACE)
    gl.glDisable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    # Pick cursor color theme
    if is_perturbing:
        main_color = (1.0, 0.2, 0.2, 1.0)  # Red for force perturbation
    elif is_dragging:
        main_color = (1.0, 0.85, 0.0, 1.0)  # Gold for camera orbit/pan
    else:
        main_color = (0.1, 0.95, 1.0, 1.0)  # Electric Cyan for hover

    # A. Circular Targeting Ring
    gl.glColor4f(0.0, 0.0, 0.0, 0.8)
    gl.glLineWidth(3.5)
    gl.glBegin(gl.GL_LINE_LOOP)
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        gl.glVertex2f(x + math.cos(rad) * 10, y + math.sin(rad) * 10)
    gl.glEnd()

    gl.glColor4f(*main_color)
    gl.glLineWidth(1.8)
    gl.glBegin(gl.GL_LINE_LOOP)
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        gl.glVertex2f(x + math.cos(rad) * 9, y + math.sin(rad) * 9)
    gl.glEnd()

    # B. Arrow Outline (Black)
    gl.glColor4f(0.0, 0.0, 0.0, 1.0)
    gl.glLineWidth(4.0)
    gl.glBegin(gl.GL_LINE_LOOP)
    gl.glVertex2f(x, y)
    gl.glVertex2f(x + 18, y + 13)
    gl.glVertex2f(x + 10, y + 13)
    gl.glVertex2f(x + 15, y + 23)
    gl.glVertex2f(x + 11, y + 25)
    gl.glVertex2f(x + 6, y + 15)
    gl.glVertex2f(x, y + 19)
    gl.glEnd()

    # C. Arrow Interior
    gl.glColor4f(*main_color)
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex2f(x, y)
    gl.glVertex2f(x + 17, y + 13)
    gl.glVertex2f(x + 6, y + 15)

    gl.glVertex2f(x + 10, y + 13)
    gl.glVertex2f(x + 14, y + 23)
    gl.glVertex2f(x + 7, y + 15)
    gl.glEnd()

    # D. Center Precision Dot
    gl.glColor4f(1.0, 1.0, 1.0, 1.0)
    gl.glPointSize(4.0)
    gl.glBegin(gl.GL_POINTS)
    gl.glVertex2f(x, y)
    gl.glEnd()

    # 4. Restore OpenGL State
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glPopMatrix()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glPopMatrix()

def main():
    print("=" * 65)
    print("🦆 Microduck Physical AI Native Simulation Viewer")
    print("=" * 65)
    print(f"Loading MJCF model from: {MODEL_PATH}")

    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model file not found at {MODEL_PATH}")
        sys.exit(1)

    scene_xml = f"""
    <mujoco>
        <option gravity="0 0 -9.81" timestep="0.002"/>
        <asset>
            <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="512"/>
            <texture name="texplane" type="2d" builtin="checker" rgb1=".25 .3 .35" rgb2=".15 0.18 0.22" width="512" height="512" mark="cross" markrgb=".8 .8 .8"/>
            <material name="matplane" reflectance="0.2" texture="texplane" texrepeat="2 2" texuniform="true"/>
        </asset>
        <worldbody>
            <light directional="true" diffuse=".9 .9 .9" specular=".3 .3 .3" pos="0 0 4" dir="0 0 -1"/>
            <geom name="floor" type="plane" pos="0 0 -0.25" size="3 3 0.1" material="matplane"/>
        </worldbody>
        <include file="{MODEL_PATH}"/>
    </mujoco>
    """

    model = mujoco.MjModel.from_xml_string(scene_xml)
    data = mujoco.MjData(model)

    # 1. Print Comprehensive Model Diagnostics & Kinematics Banner
    print("✅ Model and Scene loaded successfully!")
    print(f"  • Generalized coordinates (nq) : {model.nq}")
    print(f"  • Degrees of freedom (nv)      : {model.nv}")
    print(f"  • Number of joints (njnt)      : {model.njnt}")
    print(f"  • Number of bodies (nbody)     : {model.nbody}")
    print(f"  • Number of geoms (ngeom)      : {model.ngeom}")
    print(f"  • Number of actuators (nu)     : {model.nu}")
    print(f"  • Timestep                     : {model.opt.timestep:.4f} s ({1.0/model.opt.timestep:.0f} Hz)")
    print("-" * 65)

    display = os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    if not display:
        print("ℹ️ Headless mode detected (no DISPLAY/WAYLAND_DISPLAY).")
        print("Stepping simulation 500 times in headless mode...")
        for _ in range(500):
            mujoco.mj_step(model, data)
        print(f"✅ Headless physics simulation completed: Trunk pos = {data.qpos[:3]}")
        return

    if not glfw.init():
        print("❌ Failed to initialize GLFW.")
        sys.exit(1)

    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.VISIBLE, glfw.TRUE)
    window = glfw.create_window(1280, 720, "🦆 Microduck Physical AI Simulation (WSLg Full Interactive)", None, None)
    if not window:
        glfw.terminate()
        print("❌ Failed to create GLFW window.")
        sys.exit(1)

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    # MuJoCo visualization & perturbation context
    camera = mujoco.MjvCamera()
    option = mujoco.MjvOption()
    scene = mujoco.MjvScene(model, maxgeom=2000)
    context = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150)
    perturb = mujoco.MjvPerturb()

    # Default visualization options: Enable Sensor Sites (group 3 has camera, ToF, IMU, feet)
    option.sitegroup[3] = 1
    option.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = False        # Joint axes
    option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = False # Contact points
    option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = False # Force vectors
    option.flags[mujoco.mjtVisFlag.mjVIS_INERTIA] = False      # Inertial ellipsoids
    option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = False  # Transparent mode
    option.flags[mujoco.mjtVisFlag.mjVIS_PERTFORCE] = True     # Render perturbation force spring

    # Camera presets (Tracking trunk_base)
    trunk_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "trunk_base")
    camera.distance = 1.3
    camera.elevation = -18.0
    camera.azimuth = 100.0
    if trunk_id >= 0:
        camera.lookat[:] = data.xpos[trunk_id]

    # Pre-render initial scene to populate camera matrices for perturbation
    mujoco.mjv_updateScene(model, data, option, perturb, camera, mujoco.mjtCatBit.mjCAT_ALL, scene)
    if trunk_id >= 0:
        perturb.select = trunk_id
        mujoco.mjv_initPerturb(model, data, scene, perturb)

    # Mouse & Keyboard interaction state
    button_left = False
    button_middle = False
    button_right = False
    mouse_x = 640.0
    mouse_y = 360.0
    last_x = 640.0
    last_y = 360.0
    paused = False

    def mouse_button_callback(win, button, action, mods):
        nonlocal button_left, button_middle, button_right, last_x, last_y
        mod_ctrl = (glfw.get_key(win, glfw.KEY_LEFT_CONTROL) == glfw.PRESS or 
                    glfw.get_key(win, glfw.KEY_RIGHT_CONTROL) == glfw.PRESS)

        if button == glfw.MOUSE_BUTTON_LEFT:
            button_left = (action == glfw.PRESS)
            if action == glfw.PRESS and mod_ctrl:
                perturb.active = int(mujoco.mjtPerturb.mjPERT_TRANSLATE)
                mujoco.mjv_initPerturb(model, data, scene, perturb)
            elif action == glfw.RELEASE:
                perturb.active = 0
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            button_right = (action == glfw.PRESS)
            if action == glfw.PRESS and mod_ctrl:
                perturb.active = int(mujoco.mjtPerturb.mjPERT_ROTATE)
                mujoco.mjv_initPerturb(model, data, scene, perturb)
            elif action == glfw.RELEASE:
                perturb.active = 0
        elif button == glfw.MOUSE_BUTTON_MIDDLE:
            button_middle = (action == glfw.PRESS)

        last_x, last_y = glfw.get_cursor_pos(win)

    def cursor_pos_callback(win, xpos, ypos):
        nonlocal last_x, last_y, mouse_x, mouse_y
        mouse_x = xpos
        mouse_y = ypos
        dx = xpos - last_x
        dy = ypos - last_y
        last_x = xpos
        last_y = ypos

        if not (button_left or button_middle or button_right):
            return

        width, height = glfw.get_window_size(win)
        mod_ctrl = (glfw.get_key(win, glfw.KEY_LEFT_CONTROL) == glfw.PRESS or 
                    glfw.get_key(win, glfw.KEY_RIGHT_CONTROL) == glfw.PRESS)
        mod_shift = (glfw.get_key(win, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or 
                     glfw.get_key(win, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS)

        # Force Perturbation (Ctrl + Drag)
        if mod_ctrl and perturb.active != 0:
            action = int(mujoco.mjtMouse.mjMOUSE_MOVE_V) if button_left else int(mujoco.mjtMouse.mjMOUSE_ROTATE_V)
            mujoco.mjv_movePerturb(model, data, action, dx / width, dy / height, scene, perturb)
            return

        # Standard Camera Navigation
        if button_left and not mod_shift:
            action = int(mujoco.mjtMouse.mjMOUSE_ROTATE_V)
        elif button_right or (button_left and mod_shift):
            action = int(mujoco.mjtMouse.mjMOUSE_MOVE_V)
        elif button_middle:
            action = int(mujoco.mjtMouse.mjMOUSE_ZOOM)
        else:
            action = int(mujoco.mjtMouse.mjMOUSE_NONE)

        mujoco.mjv_moveCamera(model, action, dx / width, dy / height, camera)

    def scroll_callback(win, xoffset, yoffset):
        action = int(mujoco.mjtMouse.mjMOUSE_ZOOM)
        mujoco.mjv_moveCamera(model, action, 0.0, -0.05 * yoffset, camera)

    def key_callback(win, key, scancode, action, mods):
        nonlocal paused
        if action == glfw.PRESS:
            # Space -> Pause / Resume
            if key == glfw.KEY_SPACE:
                paused = not paused
            # R or Backspace -> Reset simulation
            elif key in (glfw.KEY_R, glfw.KEY_BACKSPACE):
                mujoco.mj_resetData(model, data)
                mujoco.mj_forward(model, data)
            # ESC -> Quit
            elif key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(win, True)
            # J -> Toggle Joint axes
            elif key == glfw.KEY_J:
                option.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = not option.flags[mujoco.mjtVisFlag.mjVIS_JOINT]
            # S -> Toggle Sensor sites
            elif key == glfw.KEY_S:
                option.sitegroup[3] = 0 if option.sitegroup[3] == 1 else 1
            # C -> Toggle Contact points and forces
            elif key == glfw.KEY_C:
                curr = option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT]
                option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = not curr
                option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = not curr
            # I -> Toggle Inertial ellipsoids
            elif key == glfw.KEY_I:
                option.flags[mujoco.mjtVisFlag.mjVIS_INERTIA] = not option.flags[mujoco.mjtVisFlag.mjVIS_INERTIA]
            # T -> Toggle Transparent mode
            elif key == glfw.KEY_T:
                option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = not option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT]
            # F -> Toggle Floor textures
            elif key == glfw.KEY_F:
                option.flags[mujoco.mjtVisFlag.mjVIS_TEXTURE] = not option.flags[mujoco.mjtVisFlag.mjVIS_TEXTURE]

    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window, key_callback)

    print("🎮 Interactive Controls Guide:")
    print("  • Left Click + Drag     : Orbit Camera around Duck")
    print("  • Right Click + Drag    : Pan Camera (Up / Down / Left / Right)")
    print("  • Scroll Wheel          : Zoom In / Out")
    print("  • Ctrl + Left Drag      : 🪢 Grab & Pull Robot (Spring Perturbation)")
    print("  • Ctrl + Right Drag     : 🔄 Apply Rotational Torque")
    print("  • Spacebar              : Pause / Resume Physics")
    print("  • 'R' / Backspace       : Reset Robot Position")
    print("  • [J]oint | [S]ite | [C]ontact | [I]nertia | [T]ransparent : Toggle Visual Layers")
    print("  • ESC                   : Quit Viewer")
    print("=" * 65)

    # Main Rendering & Physics Loop
    while not glfw.window_should_close(window):
        step_start = time.time()

        if not paused:
            # Apply interactive perturbation forces
            if perturb.active != 0:
                mujoco.mjv_applyPerturbPose(model, data, perturb, 0)
                mujoco.mjv_applyPerturbForce(model, data, perturb)

            mujoco.mj_step(model, data)
        else:
            if perturb.active != 0:
                mujoco.mjv_applyPerturbPose(model, data, perturb, 1)

        # Smooth dynamic camera tracking when not orbiting manually
        if trunk_id >= 0 and not (button_left or button_right or button_middle):
            camera.lookat[0] = data.xpos[trunk_id][0]
            camera.lookat[1] = data.xpos[trunk_id][1]
            camera.lookat[2] = data.xpos[trunk_id][2] + 0.05

        # Render 3D MuJoCo Scene
        win_w, win_h = glfw.get_window_size(window)
        fb_w, fb_h = glfw.get_framebuffer_size(window)
        viewport = mujoco.MjrRect(0, 0, fb_w, fb_h)

        mujoco.mjv_updateScene(model, data, option, perturb, camera, mujoco.mjtCatBit.mjCAT_ALL, scene)
        mujoco.mjr_render(viewport, scene, context)

        # 1. Top-Left HUD (Title, Status, Sim Time)
        status_text = f"PAUSED ({data.time:.2f}s)" if paused else f"RUNNING ({data.time:.2f}s)"
        mujoco.mjr_overlay(
            mujoco.mjtFontScale.mjFONTSCALE_150,
            mujoco.mjtGridPos.mjGRID_TOPLEFT,
            viewport,
            "🦆 Microduck Simulation",
            status_text,
            context
        )

        # 2. Top-Right HUD (Live Telemetry & Visual Flags)
        if trunk_id >= 0:
            trunk_x, trunk_y, trunk_z = data.xpos[trunk_id]
            q = data.xquat[trunk_id]
            r, p, y = quat_to_euler_deg(q)
            flags_str = (
                f"Trunk Pos: [{trunk_x:+.2f}, {trunk_y:+.2f}, {trunk_z:+.2f}]m\n"
                f"IMU Euler: R:{r:+.1f}° P:{p:+.1f}° Y:{y:+.1f}°\n"
                f"Flags: [J]oints:{'ON' if option.flags[mujoco.mjtVisFlag.mjVIS_JOINT] else 'OFF'} | "
                f"[S]ites:{'ON' if option.sitegroup[3] == 1 else 'OFF'} | "
                f"[C]ontacts:{'ON' if option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] else 'OFF'} | "
                f"[I]nertia:{'ON' if option.flags[mujoco.mjtVisFlag.mjVIS_INERTIA] else 'OFF'}"
            )
            mujoco.mjr_overlay(
                mujoco.mjtFontScale.mjFONTSCALE_150,
                mujoco.mjtGridPos.mjGRID_TOPRIGHT,
                viewport,
                "📊 Live Telemetry",
                flags_str,
                context
            )

        # 3. Bottom-Left HUD (Controls Cheatsheet)
        ctrl_help = "Space: Pause | R: Reset | Ctrl+Drag: Perturb | J,S,C,I,T: Toggles"
        mujoco.mjr_overlay(
            mujoco.mjtFontScale.mjFONTSCALE_100,
            mujoco.mjtGridPos.mjGRID_BOTTOMLEFT,
            viewport,
            ctrl_help,
            "",
            context
        )

        # 4. Render Guaranteed In-Frame Cursor
        is_perturbing = (perturb.active != 0)
        is_dragging = (button_left or button_right or button_middle)
        render_gl_cursor(mouse_x, mouse_y, win_w, win_h, fb_w, fb_h, is_dragging, is_perturbing)

        glfw.swap_buffers(window)
        glfw.poll_events()

        time_until_next = model.opt.timestep - (time.time() - step_start)
        if time_until_next > 0:
            time.sleep(time_until_next)

    glfw.terminate()

if __name__ == "__main__":
    main()
