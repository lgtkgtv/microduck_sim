#!/usr/bin/env python3
"""
generate_images.py
Generates 6 clean, professional, tech-themed PNG diagrams (size 400x300)
for the Microduck Physical AI Masterclass handout:
  1. rockchip_rk3566.png - Microchip diagram with pins & bus labels
  2. imu_sensor.png - 3D axis diagram showing Pitch, Roll, Yaw
  3. dof_motors.png - Robotic joint with rotational arrows & limits
  4. lidar_radar.png - Laser sweeping radar schematic with obstacles
  5. rgb_camera.png - Camera lens with ray tracing and pixel grid
  6. battery_drain.png - Lithium-ion battery with discharge power curves
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# Ensure images directory exists in project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IMG_DIR = os.path.join(PROJECT_ROOT, "images")
os.makedirs(IMG_DIR, exist_ok=True)

# Supersampling factor for crisp anti-aliasing
SCALE = 2
TARGET_W, TARGET_H = 400, 300
W, H = TARGET_W * SCALE, TARGET_H * SCALE

# Load fonts with fallbacks
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

# Color Palette (Dark High-Tech Theme)
BG_COLOR = (15, 23, 42)          # Slate 900
PANEL_BG = (30, 41, 59)          # Slate 800
CYAN_ACCENT = (14, 165, 233)     # Sky 500 / Cyan
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
    """Draw subtle background tech grid"""
    step = 40 * SCALE
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=(24, 34, 53), width=1 * SCALE)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=(24, 34, 53), width=1 * SCALE)
    
    # Corner tech accents
    acc_len = 15 * SCALE
    draw.line([(10 * SCALE, 10 * SCALE), (10 * SCALE + acc_len, 10 * SCALE)], fill=CYAN_ACCENT, width=2 * SCALE)
    draw.line([(10 * SCALE, 10 * SCALE), (10 * SCALE, 10 * SCALE + acc_len)], fill=CYAN_ACCENT, width=2 * SCALE)
    
    draw.line([(W - 10 * SCALE, 10 * SCALE), (W - 10 * SCALE - acc_len, 10 * SCALE)], fill=CYAN_ACCENT, width=2 * SCALE)
    draw.line([(W - 10 * SCALE, 10 * SCALE), (W - 10 * SCALE, 10 * SCALE + acc_len)], fill=CYAN_ACCENT, width=2 * SCALE)
    
    draw.line([(10 * SCALE, H - 10 * SCALE), (10 * SCALE + acc_len, H - 10 * SCALE)], fill=CYAN_ACCENT, width=2 * SCALE)
    draw.line([(10 * SCALE, H - 10 * SCALE), (10 * SCALE, H - 10 * SCALE - acc_len)], fill=CYAN_ACCENT, width=2 * SCALE)
    
    draw.line([(W - 10 * SCALE, H - 10 * SCALE), (W - 10 * SCALE - acc_len, H - 10 * SCALE)], fill=CYAN_ACCENT, width=2 * SCALE)
    draw.line([(W - 10 * SCALE, H - 10 * SCALE), (W - 10 * SCALE, H - 10 * SCALE - acc_len)], fill=CYAN_ACCENT, width=2 * SCALE)

def draw_header_badge(draw, text, subtitle, icon_color=CYAN_ACCENT):
    f_title = get_font(12, bold=True)
    f_sub = get_font(9, mono=True)
    
    # Top badge pill
    pill_x, pill_y = 20 * SCALE, 14 * SCALE
    draw.ellipse([pill_x, pill_y + 3 * SCALE, pill_x + 8 * SCALE, pill_y + 11 * SCALE], fill=icon_color)
    draw.text((pill_x + 14 * SCALE, pill_y), text, fill=TEXT_LIGHT, font=f_title)
    
    # Subtitle / category on right
    bbox = draw.textbbox((0, 0), subtitle, font=f_sub)
    draw.text((W - (bbox[2] - bbox[0]) - 20 * SCALE, pill_y + 2 * SCALE), subtitle, fill=TEXT_MUTED, font=f_sub)
    
    # Header divider
    draw.line([(20 * SCALE, 34 * SCALE), (W - 20 * SCALE, 34 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)

def save_image(img, filename):
    resized = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    out_path = os.path.join(IMG_DIR, filename)
    resized.save(out_path, "PNG", optimize=True)
    print(f" Saved: {out_path} ({TARGET_W}x{TARGET_H})")


# ============================================================================
# DIAGRAM 1: Rockchip RK3566 (Microchip diagram with pins)
# ============================================================================
def generate_rockchip_diagram():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "1. ROCKCHIP RK3566", "MAIN COMPUTE & REAL-TIME CONTROLLER", CYAN_ACCENT)
    
    cx, cy = W // 2, (H // 2) + 10 * SCALE
    chip_w, chip_h = 160 * SCALE, 140 * SCALE
    x0, y0 = cx - chip_w // 2, cy - chip_h // 2
    x1, y1 = cx + chip_w // 2, cy + chip_h // 2
    
    trace_color = (30, 60, 95)
    active_trace_color = (0, 180, 216)
    
    num_pins_lr = 6
    num_pins_tb = 7
    pin_len = 22 * SCALE
    pad_w = 4 * SCALE
    
    # Left & Right Pins
    for i in range(num_pins_lr):
        py = y0 + int((i + 1) * chip_h / (num_pins_lr + 1))
        # Left pin
        draw.rectangle([x0 - pin_len, py - pad_w // 2, x0, py + pad_w // 2], fill=AMBER)
        draw.line([(x0 - pin_len, py), (x0 - pin_len - 35 * SCALE, py)], fill=active_trace_color if i in (1, 3, 4) else trace_color, width=2 * SCALE)
        draw.circle((x0 - pin_len - 35 * SCALE, py), 3 * SCALE, fill=CYAN_GLOW if i in (1, 3, 4) else BORDER_COLOR)
        
        # Right pin
        draw.rectangle([x1, py - pad_w // 2, x1 + pin_len, py + pad_w // 2], fill=AMBER)
        draw.line([(x1 + pin_len, py), (x1 + pin_len + 35 * SCALE, py)], fill=active_trace_color if i in (0, 2, 5) else trace_color, width=2 * SCALE)
        draw.circle((x1 + pin_len + 35 * SCALE, py), 3 * SCALE, fill=EMERALD_GLOW if i in (0, 2, 5) else BORDER_COLOR)
        
    # Top & Bottom Pins
    for i in range(num_pins_tb):
        px = x0 + int((i + 1) * chip_w / (num_pins_tb + 1))
        # Top pin
        draw.rectangle([px - pad_w // 2, y0 - pin_len, px + pad_w // 2, y0], fill=AMBER)
        draw.line([(px, y0 - pin_len), (px, y0 - pin_len - 18 * SCALE)], fill=active_trace_color if i in (1, 3, 5) else trace_color, width=2 * SCALE)
        draw.circle((px, y0 - pin_len - 18 * SCALE), 3 * SCALE, fill=AMBER_GLOW if i in (1, 3, 5) else BORDER_COLOR)
        
        # Bottom pin
        draw.rectangle([px - pad_w // 2, y1, px + pad_w // 2, y1 + pin_len], fill=AMBER)
        draw.line([(px, y1 + pin_len), (px, y1 + pin_len + 18 * SCALE)], fill=active_trace_color if i in (2, 4) else trace_color, width=2 * SCALE)
        draw.circle((px, y1 + pin_len + 18 * SCALE), 3 * SCALE, fill=PURPLE if i in (2, 4) else BORDER_COLOR)

    # Chip Body (Silicon & Heatspreader)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8 * SCALE, fill=(24, 32, 47), outline=CYAN_ACCENT, width=3 * SCALE)
    # Inner die boundary
    draw.rounded_rectangle([x0 + 8 * SCALE, y0 + 8 * SCALE, x1 - 8 * SCALE, y1 - 8 * SCALE], radius=4 * SCALE, fill=(18, 24, 38), outline=BORDER_COLOR, width=1 * SCALE)
    
    # Pin 1 indicator dot
    draw.circle((x0 + 16 * SCALE, y0 + 16 * SCALE), 4 * SCALE, fill=CYAN_GLOW)
    
    # Chip markings text
    f_chip_brand = get_font(11, bold=True)
    f_chip_model = get_font(16, bold=True)
    f_chip_sub = get_font(8, mono=True)
    
    draw.text((cx, cy - 35 * SCALE), "ROCKCHIP", fill=TEXT_MUTED, font=f_chip_brand, anchor="mm")
    draw.text((cx, cy - 12 * SCALE), "RK3566", fill=CYAN_GLOW, font=f_chip_model, anchor="mm")
    draw.text((cx, cy + 12 * SCALE), "QUAD-CORE A55 @ 1.8GHz", fill=TEXT_LIGHT, font=f_chip_sub, anchor="mm")
    draw.text((cx, cy + 28 * SCALE), "0.8 TOPS NPU • 50Hz LOOP", fill=EMERALD_GLOW, font=f_chip_sub, anchor="mm")
    
    # Outer Peripheral Labels
    f_lbl = get_font(8, bold=True, mono=True)
    draw.text((25 * SCALE, cy - 35 * SCALE), "MIPI CSI-2", fill=CYAN_GLOW, font=f_lbl)
    draw.text((25 * SCALE, cy), "I2C / IMU", fill=TEXT_LIGHT, font=f_lbl)
    draw.text((25 * SCALE, cy + 35 * SCALE), "UART / TELEM", fill=AMBER_GLOW, font=f_lbl)
    
    draw.text((W - 25 * SCALE, cy - 35 * SCALE), "PWM 15-DOF", fill=EMERALD_GLOW, font=f_lbl, anchor="ra")
    draw.text((W - 25 * SCALE, cy), "USB 3.0 OTG", fill=TEXT_LIGHT, font=f_lbl, anchor="ra")
    draw.text((W - 25 * SCALE, cy + 35 * SCALE), "SPI / FLASH", fill=PURPLE, font=f_lbl, anchor="ra")
    
    f_stat = get_font(8, mono=True)
    draw.rounded_rectangle([60 * SCALE, H - 24 * SCALE, W - 60 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "STATUS: 50Hz REAL-TIME CONTROL CADENCE (20ms CYCLE)", fill=EMERALD_GLOW, font=f_stat, anchor="mm")
    
    save_image(img, "rockchip_rk3566.png")


# ============================================================================
# DIAGRAM 2: IMU Sensor (3D axis diagram showing Pitch, Roll, Yaw)
# ============================================================================
def generate_imu_diagram():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "2. INERTIAL MEASUREMENT UNIT (IMU)", "6-DOF ORIENTATION & GRAVITY VECTOR", EMERALD)
    
    ox, oy = W // 2 - 30 * SCALE, (H // 2) + 25 * SCALE
    
    # Ground shadow plane
    ground_color = (25, 38, 58)
    draw.polygon([
        (ox, oy),
        (ox + 130 * SCALE, oy - 45 * SCALE),
        (ox + 60 * SCALE, oy + 45 * SCALE),
        (ox - 70 * SCALE, oy + 90 * SCALE)
    ], fill=ground_color, outline=BORDER_COLOR)
    
    # IMU chip at origin
    chip_w, chip_h = 45 * SCALE, 25 * SCALE
    draw.rectangle([ox - chip_w // 2, oy - chip_h // 2 - 5 * SCALE, ox + chip_w // 2, oy + chip_h // 2 - 5 * SCALE],
                   fill=(30, 45, 68), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((ox, oy - 5 * SCALE), "6-DOF IMU", fill=TEXT_LIGHT, font=get_font(7, bold=True, mono=True), anchor="mm")
    
    # 3 Axes
    # +Z Axis (Yaw)
    z_len = 120 * SCALE
    zx, zy = ox, oy - z_len
    draw.line([(ox, oy), (zx, zy)], fill=CYAN_GLOW, width=4 * SCALE)
    draw.polygon([(zx, zy - 8 * SCALE), (zx - 6 * SCALE, zy + 4 * SCALE), (zx + 6 * SCALE, zy + 4 * SCALE)], fill=CYAN_GLOW)
    
    # +X Axis (Roll)
    x_len_x, x_len_y = 120 * SCALE, 50 * SCALE
    xx, xy = ox + x_len_x, oy + x_len_y
    draw.line([(ox, oy), (xx, xy)], fill=ROSE, width=4 * SCALE)
    draw.polygon([(xx + 6 * SCALE, xy + 3 * SCALE), (xx - 4 * SCALE, xy - 6 * SCALE), (xx - 6 * SCALE, xy + 5 * SCALE)], fill=ROSE)
    
    # +Y Axis (Pitch)
    y_len_x, y_len_y = -110 * SCALE, 35 * SCALE
    yx, yy = ox + y_len_x, oy + y_len_y
    draw.line([(ox, oy), (yx, yy)], fill=EMERALD_GLOW, width=4 * SCALE)
    draw.polygon([(yx - 6 * SCALE, yy + 2 * SCALE), (yx + 6 * SCALE, yy + 4 * SCALE), (yx + 4 * SCALE, yy - 6 * SCALE)], fill=EMERALD_GLOW)
    
    # Curved rotation arrows
    # Yaw Arc
    draw.arc([ox - 35 * SCALE, oy - 75 * SCALE, ox + 35 * SCALE, oy - 45 * SCALE], start=30, end=240, fill=CYAN_ACCENT, width=3 * SCALE)
    draw.polygon([(ox + 32 * SCALE, oy - 60 * SCALE), (ox + 22 * SCALE, oy - 68 * SCALE), (ox + 24 * SCALE, oy - 52 * SCALE)], fill=CYAN_ACCENT)
    
    # Roll Arc
    draw.arc([ox + 50 * SCALE, oy + 5 * SCALE, ox + 95 * SCALE, oy + 45 * SCALE], start=100, end=330, fill=ROSE, width=3 * SCALE)
    draw.polygon([(ox + 94 * SCALE, oy + 25 * SCALE), (ox + 84 * SCALE, oy + 18 * SCALE), (ox + 88 * SCALE, oy + 32 * SCALE)], fill=ROSE)
    
    # Pitch Arc
    draw.arc([ox - 85 * SCALE, oy + 0 * SCALE, ox - 40 * SCALE, oy + 38 * SCALE], start=200, end=40, fill=EMERALD, width=3 * SCALE)
    draw.polygon([(ox - 42 * SCALE, oy + 20 * SCALE), (ox - 48 * SCALE, oy + 32 * SCALE), (ox - 36 * SCALE, oy + 30 * SCALE)], fill=EMERALD)

    # Gravity Vector
    draw.line([(ox, oy), (ox, oy + 65 * SCALE)], fill=PURPLE, width=3 * SCALE)
    draw.polygon([(ox, oy + 72 * SCALE), (ox - 5 * SCALE, oy + 60 * SCALE), (ox + 5 * SCALE, oy + 60 * SCALE)], fill=PURPLE)
    
    f_axis = get_font(10, bold=True)
    f_sub = get_font(8, mono=True)
    
    draw.text((zx + 10 * SCALE, zy), "+Z : YAW (ψ)", fill=CYAN_GLOW, font=f_axis)
    draw.text((zx + 10 * SCALE, zy + 12 * SCALE), "Heading Rotation", fill=TEXT_MUTED, font=f_sub)
    
    draw.text((xx + 10 * SCALE, xy - 10 * SCALE), "+X : ROLL (φ)", fill=ROSE, font=f_axis)
    draw.text((xx + 10 * SCALE, xy + 2 * SCALE), "Lateral Tilt", fill=TEXT_MUTED, font=f_sub)
    
    draw.text((yx - 10 * SCALE, yy - 18 * SCALE), "+Y : PITCH (θ)", fill=EMERALD_GLOW, font=f_axis, anchor="ra")
    draw.text((yx - 10 * SCALE, yy - 6 * SCALE), "Forward / Back Lean", fill=TEXT_MUTED, font=f_sub, anchor="ra")
    
    draw.text((ox + 8 * SCALE, oy + 65 * SCALE), "ḡ Gravity Vector", fill=PURPLE, font=f_sub)
    
    # Telemetry specs card
    card_x0, card_y0 = W - 140 * SCALE, 45 * SCALE
    card_x1, card_y1 = W - 15 * SCALE, 140 * SCALE
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=6 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    
    draw.text((card_x0 + 10 * SCALE, card_y0 + 8 * SCALE), "TELEMETRY SPECS", fill=AMBER_GLOW, font=get_font(8, bold=True, mono=True))
    draw.text((card_x0 + 10 * SCALE, card_y0 + 24 * SCALE), "• Accel: ±4g (ax, ay, az)", fill=TEXT_LIGHT, font=get_font(7, mono=True))
    draw.text((card_x0 + 10 * SCALE, card_y0 + 38 * SCALE), "• Gyro: ±1000°/s (ωx, ωy, ωz)", fill=TEXT_LIGHT, font=get_font(7, mono=True))
    draw.text((card_x0 + 10 * SCALE, card_y0 + 52 * SCALE), "• Obs Buffer: 4 Frames (60 floats)", fill=CYAN_GLOW, font=get_font(7, mono=True))
    draw.text((card_x0 + 10 * SCALE, card_y0 + 66 * SCALE), "• Filter: Madgwick / EKF Fusion", fill=EMERALD_GLOW, font=get_font(7, mono=True))
    draw.text((card_x0 + 10 * SCALE, card_y0 + 80 * SCALE), "• Rate: 50Hz Real-Time", fill=TEXT_MUTED, font=get_font(7, mono=True))

    save_image(img, "imu_sensor.png")


# ============================================================================
# DIAGRAM 3: DOF Motors (Robotic joint with rotational arrows)
# ============================================================================
def generate_motors_diagram():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "3. 15-DOF ACTUATORS & JOINTS", "SERVO MOTOR CONTROL & CLAMPED ACTION SPACE", AMBER)
    
    jx, jy = W // 2 - 50 * SCALE, H // 2 + 10 * SCALE
    
    # Upper Robotic Link
    draw.rounded_rectangle([jx - 18 * SCALE, jy - 100 * SCALE, jx + 18 * SCALE, jy - 30 * SCALE], radius=6 * SCALE,
                           fill=(45, 55, 72), outline=(100, 116, 139), width=2 * SCALE)
    draw.text((jx, jy - 65 * SCALE), "UPPER LINK", fill=TEXT_MUTED, font=get_font(7, bold=True, mono=True), anchor="mm")
    
    # Lower Robotic Link (Angled at 28 degrees)
    ang = math.radians(28)
    link_len = 85 * SCALE
    lx_end = jx + int(math.sin(ang) * link_len)
    ly_end = jy + int(math.cos(ang) * link_len)
    
    hw = 16 * SCALE
    cos_a, sin_a = math.cos(ang), math.sin(ang)
    p1 = (jx - hw * cos_a, jy + hw * sin_a)
    p2 = (jx + hw * cos_a, jy - hw * sin_a)
    p3 = (lx_end + hw * cos_a, ly_end - hw * sin_a)
    p4 = (lx_end - hw * cos_a, ly_end + hw * sin_a)
    draw.polygon([p1, p2, p3, p4], fill=(30, 64, 90), outline=CYAN_ACCENT)
    draw.text((jx + int(math.sin(ang) * 50 * SCALE), jy + int(math.cos(ang) * 50 * SCALE)), "LOWER LINK", fill=TEXT_LIGHT, font=get_font(7, bold=True, mono=True), anchor="mm")
    
    # Central Actuator Housing
    r_stator = 36 * SCALE
    draw.ellipse([jx - r_stator, jy - r_stator, jx + r_stator, jy + r_stator], fill=(20, 30, 45), outline=AMBER_GLOW, width=3 * SCALE)
    r_rotor = 20 * SCALE
    draw.ellipse([jx - r_rotor, jy - r_rotor, jx + r_rotor, jy + r_rotor], fill=(35, 45, 65), outline=BORDER_COLOR, width=2 * SCALE)
    draw.circle((jx, jy), 6 * SCALE, fill=CYAN_GLOW)
    
    # Rotational Torque Motion Arrows
    r_arc = 55 * SCALE
    draw.arc([jx - r_arc, jy - r_arc, jx + r_arc, jy + r_arc], start=-60, end=60, fill=AMBER, width=4 * SCALE)
    draw.polygon([(jx + 32 * SCALE, jy - 50 * SCALE), (jx + 46 * SCALE, jy - 35 * SCALE), (jx + 24 * SCALE, jy - 38 * SCALE)], fill=AMBER)
    draw.polygon([(jx + 32 * SCALE, jy + 50 * SCALE), (jx + 46 * SCALE, jy + 35 * SCALE), (jx + 24 * SCALE, jy + 38 * SCALE)], fill=AMBER)
    
    # Angle Range Indicator
    draw.arc([jx - 40 * SCALE, jy - 40 * SCALE, jx + 40 * SCALE, jy + 40 * SCALE], start=0, end=28, fill=EMERALD_GLOW, width=2 * SCALE)
    draw.text((jx + 52 * SCALE, jy + 5 * SCALE), "θ: +28°", fill=EMERALD_GLOW, font=get_font(8, bold=True, mono=True))
    
    # Right Side Specs Card
    cx0, cy0 = W - 145 * SCALE, 45 * SCALE
    cx1, cy1 = W - 15 * SCALE, H - 25 * SCALE
    draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=6 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    
    draw.text((cx0 + 10 * SCALE, cy0 + 10 * SCALE), "ACTUATION SPECS", fill=AMBER_GLOW, font=get_font(8, bold=True, mono=True))
    
    specs = [
        ("Motors:", "15 Coreless Servos"),
        ("Control Range:", "[-1.0, +1.0] Normalized"),
        ("Safety:", "torch.clamp() hard limit"),
        ("Torque Limit:", "2.5 N·m Continuous"),
        ("Feedback:", "Position + Velocity (50Hz)"),
        ("Bus Protocol:", "High-Speed Serial / CAN"),
        ("Control Mode:", "PD Position Tracking"),
        ("Latency:", "< 3.2ms End-to-End"),
    ]
    
    f_spec_lbl = get_font(7, bold=True, mono=True)
    f_spec_val = get_font(7, mono=True)
    
    y_off = cy0 + 28 * SCALE
    for lbl, val in specs:
        draw.text((cx0 + 10 * SCALE, y_off), lbl, fill=TEXT_MUTED, font=f_spec_lbl)
        draw.text((cx0 + 10 * SCALE, y_off + 10 * SCALE), val, fill=CYAN_GLOW if "[-1.0" in val or "clamp" in val else TEXT_LIGHT, font=f_spec_val)
        y_off += 24 * SCALE
        
    save_image(img, "dof_motors.png")


# ============================================================================
# DIAGRAM 4: LiDAR Radar (Laser sweeping radar schematic)
# ============================================================================
def generate_lidar_diagram():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "4. 2D LIDAR SENSING", "360° LASER TIME-OF-FLIGHT RADAR SCHEMATIC", EMERALD)
    
    rx, ry = W // 2 - 40 * SCALE, H // 2 + 10 * SCALE
    r_max = 95 * SCALE
    
    # Radar Outer Bezel & Scope Circle
    draw.ellipse([rx - r_max - 5 * SCALE, ry - r_max - 5 * SCALE, rx + r_max + 5 * SCALE, ry + r_max + 5 * SCALE],
                 fill=(10, 25, 20), outline=(20, 70, 50), width=3 * SCALE)
    
    # Concentric Range Rings
    f_range = get_font(6, mono=True)
    for dist, ratio in [(0.5, 0.25), (1.0, 0.50), (1.5, 0.75), (2.0, 1.0)]:
        rad = int(r_max * ratio)
        draw.ellipse([rx - rad, ry - rad, rx + rad, ry + rad], outline=(20, 80, 55), width=1 * SCALE)
        draw.text((rx + 3 * SCALE, ry - rad - 2 * SCALE), f"{dist}m", fill=EMERALD_GLOW, font=f_range)
        
    # Crosshairs
    draw.line([(rx - r_max, ry), (rx + r_max, ry)], fill=(20, 80, 55), width=1 * SCALE)
    draw.line([(rx, ry - r_max), (rx, ry + r_max)], fill=(20, 80, 55), width=1 * SCALE)
    
    diag_len = int(r_max * 0.707)
    draw.line([(rx - diag_len, ry - diag_len), (rx + diag_len, ry + diag_len)], fill=(15, 60, 40), width=1 * SCALE)
    draw.line([(rx - diag_len, ry + diag_len), (rx + diag_len, ry - diag_len)], fill=(15, 60, 40), width=1 * SCALE)
    
    # Sweeping Beam Sector
    sweep_angle = 55
    sector_w = 40
    for a in range(sweep_angle - sector_w, sweep_angle):
        alpha_val = int(255 * (a - (sweep_angle - sector_w)) / sector_w)
        c_beam = (int(16 + alpha_val * 0.2), int(185 * alpha_val / 255), int(129 * alpha_val / 255))
        rad_a = math.radians(a)
        bx = rx + int(math.cos(rad_a) * r_max)
        by = ry - int(math.sin(rad_a) * r_max)
        draw.line([(rx, ry), (bx, by)], fill=c_beam, width=2 * SCALE)
        
    lead_rad = math.radians(sweep_angle)
    lx = rx + int(math.cos(lead_rad) * r_max)
    ly = ry - int(math.sin(lead_rad) * r_max)
    draw.line([(rx, ry), (lx, ly)], fill=(150, 255, 180), width=2 * SCALE)
    
    # Obstacle Blips
    obstacles = [
        (42, 0.62, "OBS-1: 1.24m"),
        (135, 0.45, "OBS-2: 0.90m"),
        (220, 0.85, "WALL: 1.70m"),
    ]
    f_obs = get_font(7, bold=True, mono=True)
    for ang_deg, dist_r, tag in obstacles:
        rad_o = math.radians(ang_deg)
        ox = rx + int(math.cos(rad_o) * r_max * dist_r)
        oy = ry - int(math.sin(rad_o) * r_max * dist_r)
        draw.circle((ox, oy), 6 * SCALE, fill=(244, 63, 94), outline=ROSE, width=2 * SCALE)
        draw.circle((ox, oy), 2 * SCALE, fill=TEXT_LIGHT)
        draw.line([(ox, oy), (ox + 15 * SCALE, oy - 12 * SCALE)], fill=ROSE, width=1 * SCALE)
        draw.text((ox + 18 * SCALE, oy - 16 * SCALE), tag, fill=ROSE, font=f_obs)

    draw.circle((rx, ry), 8 * SCALE, fill=(30, 45, 65), outline=CYAN_GLOW, width=2 * SCALE)
    draw.circle((rx, ry), 3 * SCALE, fill=CYAN_ACCENT)
    
    # Right Information Panel
    px0, py0 = W - 145 * SCALE, 45 * SCALE
    px1, py1 = W - 15 * SCALE, H - 25 * SCALE
    draw.rounded_rectangle([px0, py0, px1, py1], radius=6 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    
    draw.text((px0 + 10 * SCALE, py0 + 10 * SCALE), "LIDAR PARAMETERS", fill=EMERALD_GLOW, font=get_font(8, bold=True, mono=True))
    
    lidar_info = [
        ("Type:", "2D Time-of-Flight (ToF)"),
        ("Scan Rate:", "10 Hz (3600 pts/sec)"),
        ("Range:", "0.12m – 8.0m"),
        ("Accuracy:", "±15mm @ 2.0m"),
        ("Beam:", "905nm Class 1 Eye-Safe"),
        ("Usage:", "Obstacle Avoidance & SLAM"),
        ("FOV:", "360° Planar Scan"),
        ("Interface:", "UART 230400 bps"),
    ]
    f_l_lbl = get_font(7, bold=True, mono=True)
    f_l_val = get_font(7, mono=True)
    y_off = py0 + 28 * SCALE
    for k, v in lidar_info:
        draw.text((px0 + 10 * SCALE, y_off), k, fill=TEXT_MUTED, font=f_l_lbl)
        draw.text((px0 + 10 * SCALE, y_off + 10 * SCALE), v, fill=TEXT_LIGHT, font=f_l_val)
        y_off += 24 * SCALE
        
    save_image(img, "lidar_radar.png")


# ============================================================================
# DIAGRAM 5: RGB Camera (Camera lens with a pixel grid)
# ============================================================================
def generate_camera_diagram():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "5. RGB VISION SENSOR", "OPTICAL LENS & PIXEL MATRIX TENSOR", CYAN_ACCENT)
    
    cam_x = 75 * SCALE
    cam_y = H // 2 + 10 * SCALE
    
    # Camera Barrel
    draw.rectangle([cam_x - 45 * SCALE, cam_y - 55 * SCALE, cam_x + 10 * SCALE, cam_y + 55 * SCALE],
                   fill=(30, 41, 59), outline=BORDER_COLOR, width=2 * SCALE)
    # Lens elements
    draw.arc([cam_x - 30 * SCALE, cam_y - 65 * SCALE, cam_x + 40 * SCALE, cam_y + 65 * SCALE],
             start=270, end=90, fill=CYAN_GLOW, width=4 * SCALE)
    draw.ellipse([cam_x + 10 * SCALE, cam_y - 45 * SCALE, cam_x + 35 * SCALE, cam_y + 45 * SCALE],
                 fill=(20, 60, 95), outline=CYAN_ACCENT, width=2 * SCALE)
    # Reflection flare
    draw.arc([cam_x + 14 * SCALE, cam_y - 30 * SCALE, cam_x + 28 * SCALE, cam_y + 10 * SCALE],
             start=200, end=290, fill=(200, 240, 255), width=3 * SCALE)
    
    draw.text((cam_x - 18 * SCALE, cam_y + 70 * SCALE), "OPTICAL LENS", fill=TEXT_MUTED, font=get_font(7, bold=True, mono=True), anchor="mm")
    
    # Focal point / sensor rays
    focal_x = cam_x + 95 * SCALE
    focal_y = cam_y
    
    sensor_x = W // 2 + 10 * SCALE
    draw.line([(cam_x + 30 * SCALE, cam_y - 40 * SCALE), (focal_x, focal_y)], fill=CYAN_ACCENT, width=1 * SCALE)
    draw.line([(cam_x + 30 * SCALE, cam_y + 40 * SCALE), (focal_x, focal_y)], fill=CYAN_ACCENT, width=1 * SCALE)
    draw.line([(focal_x, focal_y), (sensor_x, cam_y - 55 * SCALE)], fill=CYAN_ACCENT, width=1 * SCALE)
    draw.line([(focal_x, focal_y), (sensor_x, cam_y + 55 * SCALE)], fill=CYAN_ACCENT, width=1 * SCALE)
    draw.circle((focal_x, focal_y), 4 * SCALE, fill=AMBER_GLOW)
    draw.text((focal_x, focal_y + 12 * SCALE), "Focal Point", fill=AMBER_GLOW, font=get_font(6, mono=True), anchor="mm")
    
    # Pixel Grid Tensor
    grid_sz = 5
    cell_w = 20 * SCALE
    gx0 = sensor_x
    gy0 = cam_y - (grid_sz * cell_w) // 2
    
    colors = [
        [(239, 68, 68), (245, 158, 11), (16, 185, 129), (59, 130, 246), (168, 85, 247)],
        [(245, 158, 11), (239, 68, 68), (14, 165, 233), (16, 185, 129), (236, 72, 153)],
        [(16, 185, 129), (59, 130, 246), (255, 255, 255), (245, 158, 11), (14, 165, 233)],
        [(59, 130, 246), (168, 85, 247), (239, 68, 68), (16, 185, 129), (59, 130, 246)],
        [(168, 85, 247), (236, 72, 153), (245, 158, 11), (59, 130, 246), (16, 185, 129)],
    ]
    
    for r in range(grid_sz):
        for c in range(grid_sz):
            px = gx0 + c * cell_w
            py = gy0 + r * cell_w
            cell_col = colors[r][c]
            draw.rectangle([px, py, px + cell_w - 2 * SCALE, py + cell_w - 2 * SCALE],
                           fill=cell_col, outline=BORDER_COLOR, width=1 * SCALE)
            
    hl_r, hl_c = 2, 2
    hl_px = gx0 + hl_c * cell_w
    hl_py = gy0 + hl_r * cell_w
    draw.rectangle([hl_px - 2 * SCALE, hl_py - 2 * SCALE, hl_px + cell_w, hl_py + cell_w],
                   outline=CYAN_GLOW, width=3 * SCALE)
    
    call_x = W - 120 * SCALE
    call_y = cam_y - 20 * SCALE
    draw.line([(hl_px + cell_w, hl_py + cell_w // 2), (call_x - 10 * SCALE, call_y + 20 * SCALE)], fill=CYAN_GLOW, width=2 * SCALE)
    
    draw.rounded_rectangle([call_x - 10 * SCALE, call_y, W - 15 * SCALE, call_y + 65 * SCALE],
                           radius=4 * SCALE, fill=PANEL_BG, outline=CYAN_ACCENT)
    draw.text((call_x, call_y + 8 * SCALE), "PIXEL TENSOR", fill=CYAN_GLOW, font=get_font(7, bold=True, mono=True))
    draw.text((call_x, call_y + 22 * SCALE), "R: 255 (1.00)", fill=ROSE, font=get_font(7, mono=True))
    draw.text((call_x, call_y + 34 * SCALE), "G: 255 (1.00)", fill=EMERALD_GLOW, font=get_font(7, mono=True))
    draw.text((call_x, call_y + 46 * SCALE), "B: 255 (1.00)", fill=CYAN_GLOW, font=get_font(7, mono=True))
    
    draw.rounded_rectangle([30 * SCALE, H - 28 * SCALE, W - 30 * SCALE, H - 8 * SCALE],
                           radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 18 * SCALE), "TENSOR SHAPE: [Batch, 3, 224, 224] • NORMALIZED FLOAT [0.0, 1.0]", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")
    
    save_image(img, "rgb_camera.png")


# ============================================================================
# DIAGRAM 6: Battery Drain (Lithium-ion battery with a power curve)
# ============================================================================
def generate_battery_diagram():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "6. POWER & THERMAL DYNAMICS", "3S LI-ION DISCHARGE & MOTOR LOAD DRAIN CURVES", ROSE)
    
    bx0, by0 = 40 * SCALE, 45 * SCALE
    bw, bh = 110 * SCALE, 40 * SCALE
    bx1, by1 = bx0 + bw, by0 + bh
    
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=6 * SCALE, fill=(30, 41, 59), outline=TEXT_LIGHT, width=2 * SCALE)
    draw.rounded_rectangle([bx1, by0 + 10 * SCALE, bx1 + 6 * SCALE, by1 - 10 * SCALE], radius=2 * SCALE, fill=TEXT_LIGHT)
    
    seg_w = 20 * SCALE
    seg_gap = 4 * SCALE
    for idx in range(4):
        sx = bx0 + 6 * SCALE + idx * (seg_w + seg_gap)
        col = EMERALD_GLOW if idx < 3 else AMBER_GLOW
        draw.rounded_rectangle([sx, by0 + 6 * SCALE, sx + seg_w, by1 - 6 * SCALE], radius=3 * SCALE, fill=col)
        
    draw.text((bx0 + bw // 2, by0 + bh // 2), "3S 2200mAh 11.1V", fill=BG_COLOR, font=get_font(7, bold=True, mono=True), anchor="mm")
    
    draw.text((bx1 + 18 * SCALE, by0 + 5 * SCALE), "Nominal: 11.1V | Max: 12.6V", fill=TEXT_LIGHT, font=get_font(7, mono=True))
    draw.text((bx1 + 18 * SCALE, by0 + 20 * SCALE), "Cutoff: 9.9V (3.3V / Cell)", fill=ROSE, font=get_font(7, mono=True))
    
    chart_x0 = 45 * SCALE
    chart_y0 = 105 * SCALE
    chart_w = W - 70 * SCALE
    chart_h = 150 * SCALE
    chart_x1 = chart_x0 + chart_w
    chart_y1 = chart_y0 + chart_h
    
    draw.rounded_rectangle([chart_x0, chart_y0, chart_x1, chart_y1], radius=4 * SCALE, fill=(20, 28, 42), outline=BORDER_COLOR)
    
    f_chart = get_font(7, mono=True)
    draw.text((chart_x0 + 10 * SCALE, chart_y0 + 6 * SCALE), "DISCHARGE CURVES: VOLTAGE (V) vs TIME (MIN)", fill=TEXT_MUTED, font=get_font(7, bold=True, mono=True))
    
    v_levels = [
        (12.6, "12.6V (100%)", (40, 55, 75)),
        (11.1, "11.1V (Nominal)", (40, 55, 75)),
        (9.9, "9.9V (CUTOFF)", (180, 40, 60)),
    ]
    for v_val, v_lbl, v_col in v_levels:
        norm_y = (v_val - 9.0) / 4.0
        y_pos = int(chart_y1 - norm_y * (chart_h - 30 * SCALE))
        draw.line([(chart_x0, y_pos), (chart_x1, y_pos)], fill=v_col, width=1 * SCALE)
        draw.text((chart_x0 + 6 * SCALE, y_pos - 10 * SCALE), v_lbl, fill=ROSE if "CUTOFF" in v_lbl else TEXT_MUTED, font=f_chart)
        
    # Curve 1: Nominal
    points_nominal = []
    for t_min in range(0, 46):
        v = 12.6 - 0.5 * (t_min / 45.0) - 1.2 * math.pow(t_min / 45.0, 2) - 1.0 * math.pow(t_min / 45.0, 6)
        norm_x = t_min / 60.0
        norm_y = (v - 9.0) / 4.0
        px = chart_x0 + 70 * SCALE + int(norm_x * (chart_w - 80 * SCALE))
        py = int(chart_y1 - norm_y * (chart_h - 30 * SCALE))
        points_nominal.append((px, py))
    draw.line(points_nominal, fill=CYAN_GLOW, width=3 * SCALE)
    
    # Curve 2: High torque
    points_high_load = []
    for t_min in range(0, 20):
        v = 12.6 - 1.0 * (t_min / 18.0) - 1.5 * math.pow(t_min / 18.0, 2) - 1.2 * math.pow(t_min / 18.0, 5)
        norm_x = t_min / 60.0
        norm_y = (v - 9.0) / 4.0
        px = chart_x0 + 70 * SCALE + int(norm_x * (chart_w - 80 * SCALE))
        py = int(chart_y1 - norm_y * (chart_h - 30 * SCALE))
        points_high_load.append((px, py))
    draw.line(points_high_load, fill=ROSE, width=3 * SCALE)
    
    # Legend
    leg_x = chart_x1 - 140 * SCALE
    leg_y = chart_y0 + 20 * SCALE
    draw.line([(leg_x, leg_y + 6 * SCALE), (leg_x + 18 * SCALE, leg_y + 6 * SCALE)], fill=CYAN_GLOW, width=3 * SCALE)
    draw.text((leg_x + 24 * SCALE, leg_y), "Nominal Gait (45 min)", fill=TEXT_LIGHT, font=f_chart)
    
    draw.line([(leg_x, leg_y + 20 * SCALE), (leg_x + 18 * SCALE, leg_y + 20 * SCALE)], fill=ROSE, width=3 * SCALE)
    draw.text((leg_x + 24 * SCALE, leg_y + 14 * SCALE), "Max Torque Sprint (18 min)", fill=TEXT_LIGHT, font=f_chart)
    
    save_image(img, "battery_drain.png")


def main():
    print("=" * 60)
    print("🎨 Generating 6 Technical Diagrams with Pillow (400x300)...")
    print("=" * 60)
    generate_rockchip_diagram()
    generate_imu_diagram()
    generate_motors_diagram()
    generate_lidar_diagram()
    generate_camera_diagram()
    generate_battery_diagram()
    print("=" * 60)
    print(" All 6 diagrams successfully created in:", IMG_DIR)
    print("=" * 60)

if __name__ == "__main__":
    main()
