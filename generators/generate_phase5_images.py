#!/usr/bin/env python3
"""
generate_phase5_images.py
Generates 4 clean, professional, tech-themed PNG diagrams (size 400x300)
for Phase 5 (The Nervous System: Rust on Rockchip RK3566):
  1. rust_memory.png - Rust ownership model, borrow checker & zero-cost abstractions
  2. robotd_daemon.png - robotd 50Hz spinal cord daemon & sensor-actuator bus loop
  3. robotctl_cli.png - robotctl CLI interface & Unix domain socket architecture
  4. config_daemon.png - configd daemon, joint zero calibration & PID tuning
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
# DIAGRAM 1: Rust Memory Safety (Ownership & Zero Data Races)
# ============================================================================
def generate_rust_memory():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "1. RUST MEMORY & THREAD SAFETY", "OWNERSHIP, BORROW CHECKER & ZERO-COST REAL-TIME KERNEL", AMBER)
    
    # Left: Traditional C/C++ Embedded Pitfalls (Red Card)
    c_x, c_y = 100 * SCALE, 135 * SCALE
    c_w, c_h = 140 * SCALE, 135 * SCALE
    draw.rounded_rectangle([c_x - c_w // 2, c_y - c_h // 2, c_x + c_w // 2, c_y + c_h // 2],
                           radius=6 * SCALE, fill=(35, 25, 35), outline=ROSE, width=2 * SCALE)
    draw.text((c_x, c_y - c_h // 2 + 14 * SCALE), "C / C++ PITFALLS", fill=ROSE, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(c_x - c_w // 2 + 6 * SCALE, c_y - c_h // 2 + 25 * SCALE), (c_x + c_w // 2 - 6 * SCALE, c_y - c_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    c_lines = [
        "[-] Dangling Pointers (Segfault)",
        "[-] Data Races on /dev/imu",
        "[-] Memory Leaks Crash Daemon",
        "[-] Unbounded Garbage Collector",
        "[-] Robot Collapses Randomly"
    ]
    for idx, l in enumerate(c_lines):
        draw.text((c_x - c_w // 2 + 8 * SCALE, c_y - 18 * SCALE + idx * 15 * SCALE), l, fill=ROSE if "[-]" in l else TEXT_MUTED, font=get_font(6, mono=True))

    # Right: Rust Embedded Guarantees (Green Card)
    r_x, r_y = W - 100 * SCALE, 135 * SCALE
    r_w, r_h = 140 * SCALE, 135 * SCALE
    draw.rounded_rectangle([r_x - r_w // 2, r_y - r_h // 2, r_x + r_w // 2, r_y + r_h // 2],
                           radius=6 * SCALE, fill=(20, 45, 35), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((r_x, r_y - r_h // 2 + 14 * SCALE), "RUST EMBEDDED GUARANTEES", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(r_x - r_w // 2 + 6 * SCALE, r_y - r_h // 2 + 25 * SCALE), (r_x + r_w // 2 - 6 * SCALE, r_y - r_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    r_lines = [
        "[+] Compile-Time Ownership",
        "[+] Send + Sync (Race Free)",
        "[+] Zero-Cost Abstractions",
        "[+] Deterministic 0ms GC Pause",
        "[+] 99.999% Daemon Uptime"
    ]
    for idx, l in enumerate(r_lines):
        draw.text((r_x - r_w // 2 + 8 * SCALE, r_y - 18 * SCALE + idx * 15 * SCALE), l, fill=EMERALD_GLOW if "[+]" in l else TEXT_LIGHT, font=get_font(6, mono=True))

    # Center: Ferriss Shield / Lock Icon
    draw.circle((W // 2, c_y), 18 * SCALE, fill=(45, 35, 20), outline=AMBER_GLOW, width=2 * SCALE)
    draw.text((W // 2, c_y), "🔒", fill=AMBER_GLOW, font=get_font(10, bold=True), anchor="mm")

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "RUST GUARANTEES 100% MEMORY SAFETY WITHOUT RUNTIME GARBAGE COLLECTION PAUSES", fill=AMBER_GLOW, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "rust_memory.png")


# ============================================================================
# DIAGRAM 2: robotd Daemon (50Hz Spinal Cord Architecture)
# ============================================================================
def generate_robotd_daemon():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "2. THE robotd SPINAL CORD DAEMON", "REAL-TIME 50Hz (20ms) SENSOR-ACTUATOR CONTROL LOOP", CYAN_ACCENT)
    
    # 4 Cyclic Loop Nodes
    cy = 135 * SCALE
    cx = W // 2
    r_loop = 65 * SCALE
    
    # Circular Background Track
    draw.ellipse([cx - r_loop, cy - r_loop, cx + r_loop, cy + r_loop], outline=BORDER_COLOR, width=2 * SCALE)
    
    nodes_info = [
        ("1. READ IMU", cx, cy - r_loop, CYAN_ACCENT, "/dev/i2c-1 (200Hz)"),
        ("2. POLL ENCODERS", cx + r_loop, cy, AMBER, "15 Motor Angles"),
        ("3. ONNX INFER", cx, cy + r_loop, EMERALD, "< 2.5ms Execution"),
        ("4. WRITE PWM", cx - r_loop, cy, PURPLE, "CAN / Serial Bus"),
    ]
    
    for title, nx, ny, col, sub in nodes_info:
        draw.rounded_rectangle([nx - 45 * SCALE, ny - 16 * SCALE, nx + 45 * SCALE, ny + 16 * SCALE],
                               radius=5 * SCALE, fill=PANEL_BG, outline=col, width=2 * SCALE)
        draw.text((nx, ny - 4 * SCALE), title, fill=col, font=get_font(6.5, bold=True, mono=True), anchor="mm")
        draw.text((nx, ny + 7 * SCALE), sub, fill=TEXT_MUTED, font=get_font(5.5, mono=True), anchor="mm")

    # Center 50Hz Heartbeat Indicator
    draw.circle((cx, cy), 22 * SCALE, fill=(20, 45, 65), outline=CYAN_GLOW, width=2 * SCALE)
    draw.text((cx, cy - 4 * SCALE), "50 Hz", fill=CYAN_GLOW, font=get_font(8, bold=True, mono=True), anchor="mm")
    draw.text((cx, cy + 7 * SCALE), "20ms loop", fill=TEXT_LIGHT, font=get_font(5.5, mono=True), anchor="mm")

    # Left & Right Callout Badges
    draw.text((25 * SCALE, cy), "KERNEL\nTIMER\n±0.1ms", fill=CYAN_GLOW, font=get_font(6.5, bold=True, mono=True), anchor="mm")
    draw.text((W - 25 * SCALE, cy), "WATCHDOG\nSAFETY\nACTIVE", fill=EMERALD_GLOW, font=get_font(6.5, bold=True, mono=True), anchor="mm")

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "robotd EXECUTES IN BACKGROUND AS A HIGH-PRIORITY REAL-TIME SYSTEMD SERVICE", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "robotd_daemon.png")


# ============================================================================
# DIAGRAM 3: robotctl CLI (Unix Socket Architecture)
# ============================================================================
def generate_robotctl_cli():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "3. THE robotctl CLI INTERFACE", "UNIX DOMAIN SOCKET IPC & SYSTEM OBSERVABILITY", PURPLE)
    
    # Left: User Terminal / robotctl CLI
    t_x, t_y = 90 * SCALE, 135 * SCALE
    t_w, t_h = 130 * SCALE, 135 * SCALE
    draw.rounded_rectangle([t_x - t_w // 2, t_y - t_h // 2, t_x + t_w // 2, t_y + t_h // 2],
                           radius=6 * SCALE, fill=(18, 24, 38), outline=CYAN_GLOW, width=2 * SCALE)
    draw.text((t_x, t_y - t_h // 2 + 14 * SCALE), "robotctl CLI (User)", fill=CYAN_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(t_x - t_w // 2 + 6 * SCALE, t_y - t_h // 2 + 25 * SCALE), (t_x + t_w // 2 - 6 * SCALE, t_y - t_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    cli_cmds = [
        "$ robotctl status",
        "$ robotctl monitor",
        "$ robotctl update model",
        "$ robotctl stop --estop",
        "$ robotctl logs"
    ]
    for idx, c in enumerate(cli_cmds):
        draw.text((t_x - t_w // 2 + 8 * SCALE, t_y - 18 * SCALE + idx * 15 * SCALE), c, fill=TEXT_LIGHT if idx < 3 else (ROSE if "estop" in c else TEXT_MUTED), font=get_font(6, mono=True))

    # Center: Unix Domain Socket Bridge
    s_x = W // 2
    draw.rounded_rectangle([s_x - 30 * SCALE, t_y - 20 * SCALE, s_x + 30 * SCALE, t_y + 20 * SCALE],
                           radius=4 * SCALE, fill=PANEL_BG, outline=AMBER_GLOW, width=int(1.5 * SCALE))
    draw.text((s_x, t_y - 6 * SCALE), "UNIX SOCKET", fill=AMBER_GLOW, font=get_font(6, bold=True, mono=True), anchor="mm")
    draw.text((s_x, t_y + 8 * SCALE), "/run/robotd.sock", fill=TEXT_MUTED, font=get_font(5, mono=True), anchor="mm")

    # Arrows between CLI and Socket, Socket and Daemon
    draw.line([(t_x + t_w // 2, t_y - 5 * SCALE), (s_x - 30 * SCALE, t_y - 5 * SCALE)], fill=CYAN_GLOW, width=2 * SCALE)
    draw.line([(s_x - 30 * SCALE, t_y + 5 * SCALE), (t_x + t_w // 2, t_y + 5 * SCALE)], fill=EMERALD_GLOW, width=2 * SCALE)

    # Right: robotd Daemon (Target)
    d_x, d_y = W - 90 * SCALE, 135 * SCALE
    d_w, d_h = 130 * SCALE, 135 * SCALE
    draw.rounded_rectangle([d_x - d_w // 2, d_y - d_h // 2, d_x + d_w // 2, d_y + d_h // 2],
                           radius=6 * SCALE, fill=(20, 45, 35), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((d_x, d_y - d_h // 2 + 14 * SCALE), "robotd (Spinal Cord)", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(d_x - d_w // 2 + 6 * SCALE, d_y - d_h // 2 + 25 * SCALE), (d_x + d_w // 2 - 6 * SCALE, d_y - d_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    daemon_lines = [
        "• Real-Time Control Loop",
        "• IPC JSON Dispatcher",
        "• Model Hot-Reloading",
        "• Telemetry Streamer",
        "• Hardware Failsafe"
    ]
    for idx, dl in enumerate(daemon_lines):
        draw.text((d_x - d_w // 2 + 8 * SCALE, d_y - 18 * SCALE + idx * 15 * SCALE), dl, fill=TEXT_LIGHT, font=get_font(6, mono=True))

    draw.line([(s_x + 30 * SCALE, t_y - 5 * SCALE), (d_x - d_w // 2, t_y - 5 * SCALE)], fill=CYAN_GLOW, width=2 * SCALE)
    draw.line([(d_x - d_w // 2, t_y + 5 * SCALE), (s_x + 30 * SCALE, t_y + 5 * SCALE)], fill=EMERALD_GLOW, width=2 * SCALE)

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "NON-BLOCKING IPC: CLI QUERIES TELEMETRY WITHOUT DELAYING THE 50Hz BALANCE HEARTBEAT", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "robotctl_cli.png")


# ============================================================================
# DIAGRAM 4: Config Daemon (Joint Offsets & Calibration)
# ============================================================================
def generate_config_daemon():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "4. CONFIGURATION & CALIBRATION (configd)", "JOINT ZERO OFFSETS, PID GAINS & HARDWARE LIMITS", EMERALD)
    
    # Left: Calibration JSON Configuration
    j_x, j_y = 100 * SCALE, 135 * SCALE
    j_w, j_h = 145 * SCALE, 135 * SCALE
    draw.rounded_rectangle([j_x - j_w // 2, j_y - j_h // 2, j_x + j_w // 2, j_y + j_h // 2],
                           radius=6 * SCALE, fill=(18, 24, 38), outline=AMBER_GLOW, width=2 * SCALE)
    draw.text((j_x, j_y - j_h // 2 + 14 * SCALE), "config.json (Offsets)", fill=AMBER_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(j_x - j_w // 2 + 6 * SCALE, j_y - j_h // 2 + 25 * SCALE), (j_x + j_w // 2 - 6 * SCALE, j_y - j_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    json_lines = [
        '{\n  "joint_offsets": [',
        '    "l_hip_yaw": -0.042,',
        '    "r_hip_yaw": +0.038,',
        '    "l_knee":    +0.015',
        '  ],\n  "pid_kp": 24.5\n}'
    ]
    for idx, jl in enumerate(json_lines):
        draw.text((j_x - j_w // 2 + 8 * SCALE, j_y - 20 * SCALE + idx * 14 * SCALE), jl, fill=TEXT_LIGHT, font=get_font(6, mono=True))

    # Center: Mathematical Compensation Operator
    draw.circle((W // 2, j_y), 16 * SCALE, fill=(25, 45, 65), outline=CYAN_GLOW, width=2 * SCALE)
    draw.text((W // 2, j_y), "q + δ", fill=CYAN_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Right: True Physical Motor Calibration
    p_x, p_y = W - 100 * SCALE, 135 * SCALE
    p_w, p_h = 145 * SCALE, 135 * SCALE
    draw.rounded_rectangle([p_x - p_w // 2, p_y - p_h // 2, p_x + p_w // 2, p_y + p_h // 2],
                           radius=6 * SCALE, fill=(20, 45, 35), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((p_x, p_y - p_h // 2 + 14 * SCALE), "CALIBRATED SILICON", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(p_x - p_w // 2 + 6 * SCALE, p_y - p_h // 2 + 25 * SCALE), (p_x + p_w // 2 - 6 * SCALE, p_y - p_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    cal_lines = [
        "• Compensates 3D Print Slop",
        "• True Zero Neutral Position",
        "• Persistent EEPROM Sync",
        "• Thermal Limit Watchdog",
        "• Failsafe Auto-Shutdown"
    ]
    for idx, cl in enumerate(cal_lines):
        draw.text((p_x - p_w // 2 + 8 * SCALE, p_y - 18 * SCALE + idx * 15 * SCALE), cl, fill=TEXT_LIGHT, font=get_font(6, mono=True))

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "configd ELIMINATES MECHANICAL TOLERANCE DRIFT FOR SEAMLESS FLEET DEPLOYMENT", fill=EMERALD_GLOW, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "config_daemon.png")


def main():
    print("=" * 60)
    print("🎨 Generating 4 Phase 5 Diagrams with Pillow (400x300)...")
    print("=" * 60)
    generate_rust_memory()
    generate_robotd_daemon()
    generate_robotctl_cli()
    generate_config_daemon()
    print("=" * 60)
    print("✅ All Phase 5 diagrams successfully created in:", IMG_DIR)
    print("=" * 60)

if __name__ == "__main__":
    main()
