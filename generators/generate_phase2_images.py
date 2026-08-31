#!/usr/bin/env python3
"""
generate_phase2_images.py
Generates 4 clean, professional, tech-themed PNG diagrams (size 400x300)
for Phase 2 (The Invisible Matrix: MuJoCo Physics & MJCF Architecture):
  1. kinematic_tree.png - Hierarchical kinematic tree & joint parent-child relationships
  2. mujoco_geom.png - Collision geometries, mass distribution, contact surfaces & friction cones
  3. forward_dynamics.png - Forward dynamics pipeline: mj_step(), forces, accelerations & integrator
  4. mjcf_xml.png - MJCF Wrapper architecture & dynamic URDF compilation
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IMG_DIR = os.path.join(PROJECT_ROOT, "images")
os.makedirs(IMG_DIR, exist_ok=True)

SCALE = 2
TARGET_W, TARGET_H = 400, 300
W, H = TARGET_W * SCALE, TARGET_H * SCALE

def get_font(size, bold=False, mono=False):
    scaled_size = int(size * SCALE)
    font_paths = []
    if mono:
        font_paths = [
            "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ]
    else:
        font_paths = [
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, scaled_size)
            except Exception:
                pass
    return ImageFont.load_default()

# Theme Colors
BG_COLOR = (15, 23, 42)          # Slate 900
PANEL_BG = (30, 41, 59)          # Slate 800
CYAN_ACCENT = (14, 165, 233)     # Sky 500
CYAN_GLOW = (56, 189, 248)       # Sky 400
EMERALD = (16, 185, 129)         # Emerald 500
EMERALD_GLOW = (52, 211, 153)    # Emerald 400
AMBER = (245, 158, 11)           # Amber 500
AMBER_GLOW = (251, 191, 36)      # Amber 400
ROSE = (244, 63, 94)             # Rose 500
PURPLE = (168, 85, 247)          # Purple 500
TEXT_LIGHT = (248, 250, 252)     # Slate 50
TEXT_MUTED = (148, 163, 184)     # Slate 400
BORDER_COLOR = (51, 65, 85)      # Slate 700

def draw_grid(draw):
    step = 40 * SCALE
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=(24, 34, 53), width=1 * SCALE)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=(24, 34, 53), width=1 * SCALE)
    
    acc_len = 15 * SCALE
    for (cx, cy) in [(10, 10), (TARGET_W - 10, 10), (10, TARGET_H - 10), (TARGET_W - 10, TARGET_H - 10)]:
        sx, sy = cx * SCALE, cy * SCALE
        dx = 1 if cx < TARGET_W // 2 else -1
        dy = 1 if cy < TARGET_H // 2 else -1
        draw.line([(sx, sy), (sx + dx * acc_len, sy)], fill=CYAN_ACCENT, width=2 * SCALE)
        draw.line([(sx, sy), (sx, sy + dy * acc_len)], fill=CYAN_ACCENT, width=2 * SCALE)

def draw_header_badge(draw, text, subtitle, icon_color=CYAN_ACCENT):
    f_title = get_font(12, bold=True)
    f_sub = get_font(9, mono=True)
    pill_x, pill_y = 20 * SCALE, 14 * SCALE
    draw.ellipse([pill_x, pill_y + 3 * SCALE, pill_x + 8 * SCALE, pill_y + 11 * SCALE], fill=icon_color)
    draw.text((pill_x + 14 * SCALE, pill_y), text, fill=TEXT_LIGHT, font=f_title)
    
    bbox = draw.textbbox((0, 0), subtitle, font=f_sub)
    draw.text((W - (bbox[2] - bbox[0]) - 20 * SCALE, pill_y + 2 * SCALE), subtitle, fill=TEXT_MUTED, font=f_sub)
    draw.line([(20 * SCALE, 34 * SCALE), (W - 20 * SCALE, 34 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)

def save_image(img, filename):
    resized = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    out_path = os.path.join(IMG_DIR, filename)
    resized.save(out_path, "PNG", optimize=True)
    print(f"✅ Saved: {out_path} ({TARGET_W}x{TARGET_H})")


# ============================================================================
# DIAGRAM 1: Kinematic Tree (URDF/MJCF Parent-Child Hierarchy)
# ============================================================================
def generate_kinematic_tree():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "1. KINEMATIC TREE & HIERARCHY", "URDF/MJCF PARENT-CHILD JOINT TOPOLOGY", CYAN_ACCENT)
    
    # Root Node: Base / Torso
    root_x, root_y = W // 2, 60 * SCALE
    node_w, node_h = 100 * SCALE, 26 * SCALE
    
    # Draw Root (Torso)
    draw.rounded_rectangle([root_x - node_w // 2, root_y, root_x + node_w // 2, root_y + node_h],
                           radius=5 * SCALE, fill=(30, 58, 95), outline=CYAN_GLOW, width=2 * SCALE)
    draw.text((root_x, root_y + node_h // 2), "base_link (Torso)", fill=TEXT_LIGHT, font=get_font(8, bold=True, mono=True), anchor="mm")

    # Level 1: Left Hip & Right Hip
    l_hip_x, l_hip_y = root_x - 110 * SCALE, root_y + 60 * SCALE
    r_hip_x, r_hip_y = root_x + 110 * SCALE, root_y + 60 * SCALE
    
    # Tree connecting branches
    draw.line([(root_x, root_y + node_h), (root_x, root_y + node_h + 15 * SCALE)], fill=CYAN_ACCENT, width=2 * SCALE)
    draw.line([(l_hip_x, root_y + node_h + 15 * SCALE), (r_hip_x, root_y + node_h + 15 * SCALE)], fill=CYAN_ACCENT, width=2 * SCALE)
    draw.line([(l_hip_x, root_y + node_h + 15 * SCALE), (l_hip_x, l_hip_y)], fill=CYAN_ACCENT, width=2 * SCALE)
    draw.line([(r_hip_x, root_y + node_h + 15 * SCALE), (r_hip_x, r_hip_y)], fill=CYAN_ACCENT, width=2 * SCALE)

    # Hip Nodes
    for hx, hy, lbl in [(l_hip_x, l_hip_y, "l_hip_yaw (Joint 0)"), (r_hip_x, r_hip_y, "r_hip_yaw (Joint 7)")]:
        draw.rounded_rectangle([hx - 70 * SCALE, hy, hx + 70 * SCALE, hy + node_h],
                               radius=5 * SCALE, fill=(24, 45, 75), outline=EMERALD_GLOW, width=2 * SCALE)
        draw.text((hx, hy + node_h // 2), lbl, fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Level 2: Left Knee & Right Knee
    l_knee_x, l_knee_y = l_hip_x, l_hip_y + 55 * SCALE
    r_knee_x, r_knee_y = r_hip_x, r_hip_y + 55 * SCALE
    
    draw.line([(l_hip_x, l_hip_y + node_h), (l_knee_x, l_knee_y)], fill=EMERALD, width=2 * SCALE)
    draw.line([(r_hip_x, r_hip_y + node_h), (r_knee_x, r_knee_y)], fill=EMERALD, width=2 * SCALE)

    for kx, ky, lbl in [(l_knee_x, l_knee_y, "l_knee (Joint 3)"), (r_knee_x, r_knee_y, "r_knee (Joint 10)")]:
        draw.rounded_rectangle([kx - 65 * SCALE, ky, kx + 65 * SCALE, ky + node_h],
                               radius=5 * SCALE, fill=(35, 35, 60), outline=AMBER_GLOW, width=2 * SCALE)
        draw.text((kx, ky + node_h // 2), lbl, fill=AMBER_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Level 3: Left Foot & Right Foot (End Effectors)
    l_foot_x, l_foot_y = l_knee_x, l_knee_y + 50 * SCALE
    r_foot_x, r_foot_y = r_knee_x, r_knee_y + 50 * SCALE
    
    draw.line([(l_knee_x, l_knee_y + node_h), (l_foot_x, l_foot_y)], fill=AMBER, width=2 * SCALE)
    draw.line([(r_knee_x, r_knee_y + node_h), (r_foot_x, r_foot_y)], fill=AMBER, width=2 * SCALE)

    for fx, fy, lbl in [(l_foot_x, l_foot_y, "l_foot (Geom Contact)"), (r_foot_x, r_foot_y, "r_foot (Geom Contact)")]:
        draw.rounded_rectangle([fx - 65 * SCALE, fy, fx + 65 * SCALE, fy + node_h],
                               radius=5 * SCALE, fill=(45, 25, 40), outline=ROSE, width=2 * SCALE)
        draw.text((fx, fy + node_h // 2), lbl, fill=ROSE, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Callout badge in middle: Forward Kinematics Matrix
    mid_x0, mid_y0 = root_x - 38 * SCALE, root_y + 115 * SCALE
    mid_x1, mid_y1 = root_x + 38 * SCALE, root_y + 195 * SCALE
    draw.rounded_rectangle([mid_x0, mid_y0, mid_x1, mid_y1], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((root_x, mid_y0 + 12 * SCALE), "TRANSFORMS", fill=CYAN_GLOW, font=get_font(6, bold=True, mono=True), anchor="mm")
    draw.text((root_x, mid_y0 + 26 * SCALE), "T_world → torso", fill=TEXT_MUTED, font=get_font(6, mono=True), anchor="mm")
    draw.text((root_x, mid_y0 + 40 * SCALE), "T_torso → hip", fill=TEXT_MUTED, font=get_font(6, mono=True), anchor="mm")
    draw.text((root_x, mid_y0 + 54 * SCALE), "T_hip → knee", fill=TEXT_MUTED, font=get_font(6, mono=True), anchor="mm")
    draw.text((root_x, mid_y0 + 68 * SCALE), "T_knee → foot", fill=TEXT_LIGHT, font=get_font(6, bold=True, mono=True), anchor="mm")

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "FORWARD KINEMATICS: 15 DOFs PROPAGATE WORLD POSITIONS & MOMENTUM", fill=EMERALD_GLOW, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "kinematic_tree.png")


# ============================================================================
# DIAGRAM 2: MuJoCo Geom (Collision, Mass, Friction Cones & Soft Contacts)
# ============================================================================
def generate_mujoco_geom():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "2. COLLISION & MASS (GEOMS)", "PRIMITIVE VOLUMES, INERTIA & FRICTION CONES", EMERALD)
    
    # Ground Plane
    g_y = H - 55 * SCALE
    draw.line([(30 * SCALE, g_y), (W - 30 * SCALE, g_y)], fill=(70, 85, 105), width=3 * SCALE)
    # Ground hatch marks
    for hx in range(40 * SCALE, W - 40 * SCALE, 20 * SCALE):
        draw.line([(hx, g_y), (hx - 12 * SCALE, g_y + 12 * SCALE)], fill=(40, 55, 75), width=1 * SCALE)
    draw.text((45 * SCALE, g_y + 16 * SCALE), "GROUND PLANE (geom type='plane')", fill=TEXT_MUTED, font=get_font(7, mono=True))

    # Left: Capsule Collision Geom (Robot Thigh/Shin)
    cx, cy = 110 * SCALE, 140 * SCALE
    cap_w, cap_h = 32 * SCALE, 90 * SCALE
    
    # Capsule Outline
    draw.rounded_rectangle([cx - cap_w // 2, cy - cap_h // 2, cx + cap_w // 2, cy + cap_h // 2],
                           radius=16 * SCALE, fill=(25, 45, 70), outline=CYAN_GLOW, width=2 * SCALE)
    # Center of Mass (CoM) Target Marker
    draw.circle((cx, cy), 8 * SCALE, outline=AMBER_GLOW, width=2 * SCALE)
    draw.line([(cx - 12 * SCALE, cy), (cx + 12 * SCALE, cy)], fill=AMBER_GLOW, width=1 * SCALE)
    draw.line([(cx, cy - 12 * SCALE), (cx, cy + 12 * SCALE)], fill=AMBER_GLOW, width=1 * SCALE)
    draw.circle((cx, cy), 3 * SCALE, fill=AMBER)
    
    draw.text((cx, cy - cap_h // 2 - 14 * SCALE), "geom type='capsule'", fill=CYAN_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.text((cx + 22 * SCALE, cy), "CoM (m=0.35kg)", fill=AMBER_GLOW, font=get_font(6.5, bold=True, mono=True))

    # Right: Foot Box Geom in Contact with Ground
    fx, fy = W // 2 + 50 * SCALE, g_y - 25 * SCALE
    fw, fh = 80 * SCALE, 25 * SCALE
    draw.rounded_rectangle([fx - fw // 2, fy - fh // 2, fx + fw // 2, fy + fh // 2],
                           radius=4 * SCALE, fill=(35, 55, 40), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((fx, fy), "l_foot (box)", fill=TEXT_LIGHT, font=get_font(7, bold=True, mono=True), anchor="mm")
    
    # Contact Points & Normal Force Vectors
    cp1 = (fx - 28 * SCALE, g_y)
    cp2 = (fx + 28 * SCALE, g_y)
    for px, py in [cp1, cp2]:
        # Contact point glow
        draw.circle((px, py), 4 * SCALE, fill=ROSE)
        # Normal Force vector (Upward arrow)
        draw.line([(px, py), (px, py - 35 * SCALE)], fill=EMERALD_GLOW, width=2 * SCALE)
        draw.polygon([(px, py - 40 * SCALE), (px - 4 * SCALE, py - 32 * SCALE), (px + 4 * SCALE, py - 32 * SCALE)], fill=EMERALD_GLOW)
        # Friction Cone (Dashed triangle)
        draw.line([(px, py), (px - 16 * SCALE, py - 30 * SCALE)], fill=(150, 80, 120), width=1 * SCALE)
        draw.line([(px, py), (px + 16 * SCALE, py - 30 * SCALE)], fill=(150, 80, 120), width=1 * SCALE)
        draw.line([(px - 16 * SCALE, py - 30 * SCALE), (px + 16 * SCALE, py - 30 * SCALE)], fill=(150, 80, 120), width=1 * SCALE)

    draw.text((fx, g_y - 48 * SCALE), "Normal Force Fn", fill=EMERALD_GLOW, font=get_font(6.5, bold=True, mono=True), anchor="mm")
    draw.text((fx + 35 * SCALE, g_y - 28 * SCALE), "Friction Cone (μ=0.8)", fill=ROSE, font=get_font(6, mono=True))

    # Right Information Panel
    px0, py0 = W - 120 * SCALE, 45 * SCALE
    px1, py1 = W - 15 * SCALE, 140 * SCALE
    draw.rounded_rectangle([px0, py0, px1, py1], radius=6 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((px0 + 8 * SCALE, py0 + 8 * SCALE), "PHYSICS PROPERTIES", fill=AMBER_GLOW, font=get_font(7, bold=True, mono=True))
    draw.text((px0 + 8 * SCALE, py0 + 22 * SCALE), "• Shape: Box/Capsule", fill=TEXT_LIGHT, font=get_font(6.5, mono=True))
    draw.text((px0 + 8 * SCALE, py0 + 35 * SCALE), "• Mass: Volume × Density", fill=TEXT_LIGHT, font=get_font(6.5, mono=True))
    draw.text((px0 + 8 * SCALE, py0 + 48 * SCALE), "• Inertia: 3x3 Tensor", fill=CYAN_GLOW, font=get_font(6.5, mono=True))
    draw.text((px0 + 8 * SCALE, py0 + 61 * SCALE), "• Solref: Soft Contact", fill=EMERALD_GLOW, font=get_font(6.5, mono=True))
    draw.text((px0 + 8 * SCALE, py0 + 74 * SCALE), "• Friction: Tangential", fill=ROSE, font=get_font(6.5, mono=True))

    save_image(img, "mujoco_geom.png")


# ============================================================================
# DIAGRAM 3: Forward Dynamics (mj_step pipeline)
# ============================================================================
def generate_forward_dynamics():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "3. FORWARD DYNAMICS (mj_step)", "MOMENTUM, CONSTRAINTS & 50Hz NUMERICAL INTEGRATION", AMBER)
    
    # 4 Pipeline Stages (Horizontal Flow)
    stages = [
        ("1. STATE q, v", "Current joint positions & velocities", CYAN_ACCENT, (20, 45, 75)),
        ("2. FORCES & TORQUE", "Motors (u), Gravity (g), Contacts", AMBER, (55, 45, 20)),
        ("3. ACCELERATION q̈", "M(q)q̈ + c(q,v) = τ + J^T f", EMERALD, (20, 50, 35)),
        ("4. INTEGRATE Δt", "Euler / RK4 Integration (20ms step)", PURPLE, (45, 25, 60)),
    ]
    
    box_w = 78 * SCALE
    box_h = 95 * SCALE
    start_x = 24 * SCALE
    gap = 18 * SCALE
    cy = 135 * SCALE
    
    for idx, (title, desc, col_accent, col_bg) in enumerate(stages):
        bx = start_x + idx * (box_w + gap)
        by = cy - box_h // 2
        # Card Box
        draw.rounded_rectangle([bx, by, bx + box_w, by + box_h], radius=6 * SCALE, fill=col_bg, outline=col_accent, width=2 * SCALE)
        # Stage Header
        draw.text((bx + box_w // 2, by + 16 * SCALE), title, fill=col_accent, font=get_font(7, bold=True, mono=True), anchor="mm")
        draw.line([(bx + 8 * SCALE, by + 28 * SCALE), (bx + box_w - 8 * SCALE, by + 28 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
        # Stage Details
        # Wrap description text
        words = desc.split()
        l1 = " ".join(words[:len(words)//2])
        l2 = " ".join(words[len(words)//2:])
        draw.text((bx + box_w // 2, by + 45 * SCALE), l1, fill=TEXT_LIGHT, font=get_font(6.5, mono=True), anchor="mm")
        draw.text((bx + box_w // 2, by + 60 * SCALE), l2, fill=TEXT_MUTED, font=get_font(6.5, mono=True), anchor="mm")
        
        # Draw Arrow to next stage
        if idx < 3:
            ax = bx + box_w + 3 * SCALE
            ay = cy
            draw.line([(ax, ay), (ax + 10 * SCALE, ay)], fill=TEXT_LIGHT, width=2 * SCALE)
            draw.polygon([(ax + 12 * SCALE, ay), (ax + 6 * SCALE, ay - 4 * SCALE), (ax + 6 * SCALE, ay + 4 * SCALE)], fill=TEXT_LIGHT)

    # Feedback Loop arrow from stage 4 back to stage 1
    f_y = cy + box_h // 2 + 25 * SCALE
    s1_x = start_x + box_w // 2
    s4_x = start_x + 3 * (box_w + gap) + box_w // 2
    draw.line([(s4_x, cy + box_h // 2), (s4_x, f_y)], fill=EMERALD_GLOW, width=2 * SCALE)
    draw.line([(s4_x, f_y), (s1_x, f_y)], fill=EMERALD_GLOW, width=2 * SCALE)
    draw.line([(s1_x, f_y), (s1_x, cy + box_h // 2)], fill=EMERALD_GLOW, width=2 * SCALE)
    draw.polygon([(s1_x, cy + box_h // 2), (s1_x - 4 * SCALE, cy + box_h // 2 + 8 * SCALE), (s1_x + 4 * SCALE, cy + box_h // 2 + 8 * SCALE)], fill=EMERALD_GLOW)
    draw.text((W // 2, f_y - 8 * SCALE), "NEXT TIME STEP q(t+Δt), v(t+Δt) @ 50Hz (20ms CYCLE)", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Bottom Info
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "mujoco.mj_step(model, data): COMPUTATIONAL GRAPH RESOLVED IN <0.4ms", fill=CYAN_GLOW, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "forward_dynamics.png")


# ============================================================================
# DIAGRAM 4: MJCF XML (Wrapper Architecture & Compilation)
# ============================================================================
def generate_mjcf_xml():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "4. MJCF WRAPPER & COMPILER", "DYNAMIC URDF IMPORT, AUTOLIMITS & MOTOR INJECTION", PURPLE)
    
    # Left Box: Raw Vendor URDF (Bones Only)
    u_x, u_y = 70 * SCALE, 130 * SCALE
    u_w, u_h = 100 * SCALE, 120 * SCALE
    draw.rounded_rectangle([u_x - u_w // 2, u_y - u_h // 2, u_x + u_w // 2, u_y + u_h // 2],
                           radius=6 * SCALE, fill=(35, 30, 45), outline=ROSE, width=2 * SCALE)
    draw.text((u_x, u_y - u_h // 2 + 14 * SCALE), "VENDOR URDF", fill=ROSE, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(u_x - u_w // 2 + 6 * SCALE, u_y - u_h // 2 + 25 * SCALE), (u_x + u_w // 2 - 6 * SCALE, u_y - u_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    urdf_lines = ["• <robot>", "• <link> (Meshes)", "• <joint> (Pivots)", "[-] NO MOTORS", "[-] ZERO INERTIA"]
    for l_idx, l_txt in enumerate(urdf_lines):
        c = ROSE if "[-]" in l_txt else TEXT_MUTED
        draw.text((u_x - u_w // 2 + 10 * SCALE, u_y - u_h // 2 + 38 * SCALE + l_idx * 16 * SCALE), l_txt, fill=c, font=get_font(6.5, mono=True))

    # Center: MJCF Wrapper Injection Engine
    w_x, w_y = W // 2, 130 * SCALE
    w_w, w_h = 110 * SCALE, 135 * SCALE
    draw.rounded_rectangle([w_x - w_w // 2, w_y - w_h // 2, w_x + w_w // 2, w_y + w_h // 2],
                           radius=6 * SCALE, fill=(25, 45, 65), outline=CYAN_GLOW, width=2 * SCALE)
    draw.text((w_x, w_y - w_h // 2 + 14 * SCALE), "MJCF WRAPPER", fill=CYAN_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(w_x - w_w // 2 + 6 * SCALE, w_y - w_h // 2 + 25 * SCALE), (w_x + w_w // 2 - 6 * SCALE, w_y - w_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    mjcf_lines = [
        "1. <include URDF>",
        "2. autolimits='true'",
        "3. <actuator> (15 Motors)",
        "4. <default> Limits",
        "5. Friction & Solref"
    ]
    for l_idx, l_txt in enumerate(mjcf_lines):
        draw.text((w_x - w_w // 2 + 10 * SCALE, w_y - w_h // 2 + 38 * SCALE + l_idx * 18 * SCALE), l_txt, fill=TEXT_LIGHT, font=get_font(6.5, bold=True, mono=True))

    # Right Box: Compiled Physics Model (MjModel)
    m_x, m_y = W - 70 * SCALE, 130 * SCALE
    m_w, m_h = 100 * SCALE, 120 * SCALE
    draw.rounded_rectangle([m_x - m_w // 2, m_y - m_h // 2, m_x + m_w // 2, m_y + m_h // 2],
                           radius=6 * SCALE, fill=(20, 50, 35), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((m_x, m_y - m_h // 2 + 14 * SCALE), "FINAL MjModel", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(m_x - m_w // 2 + 6 * SCALE, m_y - m_h // 2 + 25 * SCALE), (m_x + m_w // 2 - 6 * SCALE, m_y - m_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    model_lines = ["• model.njnt = 15", "• model.nu = 15", "• Valid Inertias", "• Clamped Limits", "[+] RL READY!"]
    for l_idx, l_txt in enumerate(model_lines):
        c = EMERALD_GLOW if "[+]" in l_txt else TEXT_LIGHT
        draw.text((m_x - m_w // 2 + 10 * SCALE, m_y - m_h // 2 + 38 * SCALE + l_idx * 16 * SCALE), l_txt, fill=c, font=get_font(6.5, mono=True))

    # Connecting Arrows
    draw.line([(u_x + u_w // 2, u_y), (w_x - w_w // 2, w_y)], fill=AMBER_GLOW, width=2 * SCALE)
    draw.polygon([(w_x - w_w // 2, w_y), (w_x - w_w // 2 - 6 * SCALE, w_y - 4 * SCALE), (w_x - w_w // 2 - 6 * SCALE, w_y + 4 * SCALE)], fill=AMBER_GLOW)
    
    draw.line([(w_x + w_w // 2, w_y), (m_x - m_w // 2, m_y)], fill=EMERALD_GLOW, width=2 * SCALE)
    draw.polygon([(m_x - m_w // 2, m_y), (m_x - m_w // 2 - 6 * SCALE, m_y - 4 * SCALE), (m_x - m_w // 2 - 6 * SCALE, m_y + 4 * SCALE)], fill=EMERALD_GLOW)

    # Bottom Bar
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "XML COMPILER MERGES URDF HIERARCHY WITH MJCF ACTUATOR DYNAMICS", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "mjcf_xml.png")


def main():
    print("=" * 60)
    print("🎨 Generating 4 Phase 2 Diagrams with Pillow (400x300)...")
    print("=" * 60)
    generate_kinematic_tree()
    generate_mujoco_geom()
    generate_forward_dynamics()
    generate_mjcf_xml()
    print("=" * 60)
    print("✅ All Phase 2 diagrams successfully created in:", IMG_DIR)
    print("=" * 60)

if __name__ == "__main__":
    main()
