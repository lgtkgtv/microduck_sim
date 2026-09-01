"""
tests/test_viewer_comprehensive.py
Comprehensive End-to-End Automated Verification Test Suite for the Microduck Simulation Viewer.
"""

import os
import sys
import math
import numpy as np
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from launch_viewer import (
    ViewerConfig,
    SimulationState,
    PolicyController,
    ActionLogger,
    MuJoCoViewer,
    quat_to_yaw,
    wrap_to_pi,
)
import mujoco


@pytest.fixture
def viewer_instance():
    """Fixture providing an initialized MuJoCoViewer instance."""
    model_path = os.path.join(PROJECT_ROOT, "kinematics", "assets", "alpha", "robot_walk.xml")
    policy_path = os.path.join(PROJECT_ROOT, "policies", "alpha_walking.onnx")
    return MuJoCoViewer(model_path=model_path, policy_path=policy_path)


def test_standing_stability(viewer_instance):
    """Verifies that the robot holds its standing posture stably for 5 seconds."""
    v = viewer_instance
    v.reset_to_standing()

    for _ in range(2500):
        v.policy.step(v.model, v.data, v.state)
        mujoco.mj_step(v.model, v.data)
        v.state.step_count += 1

    x, y, z = v.data.qpos[0:3]
    trunk_quat = v.data.qpos[3:7]
    roll = math.degrees(math.atan2(2.0*(trunk_quat[0]*trunk_quat[1] + trunk_quat[2]*trunk_quat[3]), 1.0 - 2.0*(trunk_quat[1]**2 + trunk_quat[2]**2)))
    pitch = math.degrees(math.asin(2.0*(trunk_quat[0]*trunk_quat[2] - trunk_quat[3]*trunk_quat[1])))

    assert z > 0.120, f"Robot fell down: z={z:.3f}m"
    assert abs(roll) < 5.0, f"Excessive roll tilt: {roll:.1f} deg"
    assert abs(pitch) < 5.0, f"Excessive pitch tilt: {pitch:.1f} deg"
    assert abs(x) < 0.05, f"Robot drifted in stance: x={x:+.3f}m"


def test_forward_locomotion_w_key(viewer_instance):
    """Verifies that pressing 'W' executes forward locomotion with positive displacement."""
    v = viewer_instance
    v.reset_to_standing()
    v.process_command_char('w')

    assert v.state.cmd_vx == v.config.FORWARD_VX
    assert v.state.is_driving

    for _ in range(2500):
        v.policy.step(v.model, v.data, v.state)
        mujoco.mj_step(v.model, v.data)
        v.state.step_count += 1

    x, y, z = v.data.qpos[0:3]
    assert x > 0.10, f"Insufficient forward traversal: x={x:+.3f}m"
    assert z > 0.11, f"Robot fell during walking: z={z:.3f}m"


def test_backward_locomotion_s_key(viewer_instance):
    """Verifies that pressing 'S' executes reverse locomotion with negative displacement."""
    v = viewer_instance
    v.reset_to_standing()
    v.process_command_char('s')

    assert v.state.cmd_vx == v.config.BACKWARD_VX
    assert v.state.is_driving

    for _ in range(2500):
        v.policy.step(v.model, v.data, v.state)
        mujoco.mj_step(v.model, v.data)
        v.state.step_count += 1

    x, y, z = v.data.qpos[0:3]
    assert x < -0.05, f"Insufficient backward traversal: x={x:+.3f}m"
    assert z > 0.11, f"Robot fell during reverse walking: z={z:.3f}m"


def test_steer_left_a_key(viewer_instance):
    """Verifies that pressing 'A' changes target heading and turns left."""
    v = viewer_instance
    v.reset_to_standing()
    v.process_command_char('a')

    assert math.isclose(v.state.target_heading, math.radians(v.config.HEADING_STEP_DEG), abs_tol=1e-3)

    for _ in range(2000):
        v.policy.step(v.model, v.data, v.state)
        mujoco.mj_step(v.model, v.data)
        v.state.step_count += 1

    yaw_deg = math.degrees(v.get_current_yaw())
    assert yaw_deg > 15.0, f"Robot did not turn left: yaw={yaw_deg:+.1f} deg"


def test_steer_right_d_key(viewer_instance):
    """Verifies that pressing 'D' changes target heading and turns right."""
    v = viewer_instance
    v.reset_to_standing()
    v.process_command_char('d')

    assert math.isclose(v.state.target_heading, math.radians(-v.config.HEADING_STEP_DEG), abs_tol=1e-3)

    for _ in range(2000):
        v.policy.step(v.model, v.data, v.state)
        mujoco.mj_step(v.model, v.data)
        v.state.step_count += 1

    yaw_deg = math.degrees(v.get_current_yaw())
    assert yaw_deg < -15.0, f"Robot did not turn right: yaw={yaw_deg:+.1f} deg"


def test_stop_x_key(viewer_instance):
    """Verifies that pressing 'X' halts driving commands and recovers standing balance."""
    v = viewer_instance
    v.reset_to_standing()
    v.process_command_char('w')

    for _ in range(1000):
        v.policy.step(v.model, v.data, v.state)
        mujoco.mj_step(v.model, v.data)
        v.state.step_count += 1

    v.process_command_char('x')
    assert not v.state.is_driving

    for _ in range(1000):
        v.policy.step(v.model, v.data, v.state)
        mujoco.mj_step(v.model, v.data)
        v.state.step_count += 1

    z = v.data.qpos[2]
    assert z > 0.12, f"Robot failed to hold balance after stop: z={z:.3f}m"


def test_reset_r_key(viewer_instance):
    """Verifies that pressing 'R' resets all state, positions, and controls to origin."""
    v = viewer_instance
    v.process_command_char('w')
    for _ in range(500):
        v.policy.step(v.model, v.data, v.state)
        mujoco.mj_step(v.model, v.data)

    v.process_command_char('r')

    assert v.data.qpos[0] == 0.0
    assert v.data.qpos[1] == 0.0
    assert math.isclose(v.data.qpos[2], 0.125, abs_tol=1e-3)
    assert not v.state.is_driving


def test_action_logger_and_state():
    """Verifies ActionLogger methods and SimulationState properties execute without error."""
    ActionLogger.log_action("TEST_KEY", "Test Action", "Test Details")
    ActionLogger.log_status("Test Status")
    ActionLogger.log_error("Test Error (Expected in test)")

    cfg = ViewerConfig()
    st = SimulationState(cfg)
    assert not st.is_driving
    st.cmd_vx = 0.20
    assert st.is_driving
    st.reset_controls()
    assert not st.is_driving
