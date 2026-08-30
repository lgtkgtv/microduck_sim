#!/usr/bin/env python3
"""
generate_phase6_images.py
Generates 4 clean, professional, tech-themed PNG diagrams (size 400x300)
for Phase 6 (Securing the Swarm: DevSecOps, OTA & Fleet Security):
  1. ota_updates.png - A/B atomic updates & automatic rollback with updaterd
  2. devsecops_pipeline.png - Continuous Integration & automated MuJoCo test gate
  3. edge_security.png - Cryptographic SHA-256 signatures & model tamper rejection
  4. telemetry_auth.png - Encrypted fleet telemetry & real-time health dashboard
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# Path setup
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
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
# DIAGRAM 1: OTA Updates (Atomic A/B Partition & Rollback)
# ============================================================================
def generate_ota_updates():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "1. ATOMIC OTA UPDATES (updaterd)", "A/B PARTITIONS, INSTANT HOT-SWAP & AUTO-ROLLBACK", CYAN_ACCENT)
    
    # Left: Slot A (Active Running Policy)
    a_x, a_y = 100 * SCALE, 135 * SCALE
    a_w, a_h = 140 * SCALE, 135 * SCALE
    draw.rounded_rectangle([a_x - a_w // 2, a_y - a_h // 2, a_x + a_w // 2, a_y + a_h // 2],
                           radius=6 * SCALE, fill=(20, 45, 35), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((a_x, a_y - a_h // 2 + 14 * SCALE), "SLOT A (CURRENT POLICY)", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(a_x - a_w // 2 + 6 * SCALE, a_y - a_h // 2 + 25 * SCALE), (a_x + a_w // 2 - 6 * SCALE, a_y - a_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    a_lines = [
        "• State: ACTIVE (Live)",
        "• Model: walk_v2.onnx",
        "• Checksum: a9f81c... (OK)",
        "• Failsafe Golden Image",
        "• Safe Fallback Target"
    ]
    for idx, l in enumerate(a_lines):
        draw.text((a_x - a_w // 2 + 8 * SCALE, a_y - 18 * SCALE + idx * 15 * SCALE), l, fill=TEXT_LIGHT, font=get_font(6, mono=True))

    # Center: updaterd Daemon Switcher
    s_x = W // 2
    draw.circle((s_x, a_y), 20 * SCALE, fill=(25, 45, 65), outline=CYAN_GLOW, width=2 * SCALE)
    draw.text((s_x, a_y - 5 * SCALE), "updaterd", fill=CYAN_GLOW, font=get_font(6.5, bold=True, mono=True), anchor="mm")
    draw.text((s_x, a_y + 7 * SCALE), "Atomic A/B", fill=TEXT_MUTED, font=get_font(5, mono=True), anchor="mm")

    # Right: Slot B (New Downloaded Policy)
    b_x, b_y = W - 100 * SCALE, 135 * SCALE
    b_w, b_h = 140 * SCALE, 135 * SCALE
    draw.rounded_rectangle([b_x - b_w // 2, b_y - b_h // 2, b_x + b_w // 2, b_y + b_h // 2],
                           radius=6 * SCALE, fill=(35, 30, 20), outline=AMBER_GLOW, width=2 * SCALE)
    draw.text((b_x, b_y - b_h // 2 + 14 * SCALE), "SLOT B (STAGING INCOMING)", fill=AMBER_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(b_x - b_w // 2 + 6 * SCALE, b_y - b_h // 2 + 25 * SCALE), (b_x + b_w // 2 - 6 * SCALE, b_y - b_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    b_lines = [
        "• State: VERIFYING (OTA)",
        "• Model: sprint_v3.onnx",
        "• Signature: ED25519 Valid",
        "• 10s Health Probe Watchdog",
        "• Auto-Rollback on Fall"
    ]
    for idx, bl in enumerate(b_lines):
        draw.text((b_x - b_w // 2 + 8 * SCALE, b_y - 18 * SCALE + idx * 15 * SCALE), bl, fill=TEXT_LIGHT, font=get_font(6, mono=True))

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "ZERO BRICK GUARANTEE: IF NEW BRAIN TRIPS WITHIN 10s, ROBOT INSTANTLY REVERTS TO SLOT A", fill=EMERALD_GLOW, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "ota_updates.png")


# ============================================================================
# DIAGRAM 2: DevSecOps Pipeline (Continuous Integration for Physics)
# ============================================================================
def generate_devsecops_pipeline():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "2. PHYSICAL AI CI/CD PIPELINE", "AUTOMATED MUJOCO HEADLESS SIMULATION GATES BEFORE DEPLOY", AMBER)
    
    # 4 Pipeline Stages
    stages = [
        ("1. Git Commit", "Push PyTorch\nWeights (.pt)", CYAN_ACCENT, (20, 35, 55)),
        ("2. MuJoCo CI", "1,000 Headless\nDrop Tests", AMBER, (45, 35, 15)),
        ("3. Model Audit", "Verify Clamp\n& Checksum", PURPLE, (35, 20, 45)),
        ("4. Fleet Deploy", "Encrypted OTA\nBroadcast", EMERALD, (15, 45, 30)),
    ]
    
    start_x = 22 * SCALE
    node_w = 80 * SCALE
    node_h = 85 * SCALE
    gap = 18 * SCALE
    cy = 135 * SCALE
    
    for idx, (title, desc, col_acc, col_bg) in enumerate(stages):
        nx = start_x + idx * (node_w + gap)
        ny = cy - node_h // 2
        
        draw.rounded_rectangle([nx, ny, nx + node_w, ny + node_h], radius=6 * SCALE, fill=col_bg, outline=col_acc, width=2 * SCALE)
        draw.text((nx + node_w // 2, ny + 16 * SCALE), title, fill=col_acc, font=get_font(7, bold=True, mono=True), anchor="mm")
        draw.line([(nx + 6 * SCALE, ny + 26 * SCALE), (nx + node_w - 6 * SCALE, ny + 26 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
        
        # Multiline description
        lines = desc.split("\n")
        draw.text((nx + node_w // 2, ny + 45 * SCALE), lines[0], fill=TEXT_LIGHT, font=get_font(6, mono=True), anchor="mm")
        draw.text((nx + node_w // 2, ny + 58 * SCALE), lines[1], fill=TEXT_MUTED, font=get_font(5.5, mono=True), anchor="mm")
        
        # Arrow
        if idx < 3:
            ax = nx + node_w + 2 * SCALE
            draw.line([(ax, cy), (ax + 12 * SCALE, cy)], fill=TEXT_LIGHT, width=2 * SCALE)
            draw.polygon([(ax + 14 * SCALE, cy), (ax + 8 * SCALE, cy - 4 * SCALE), (ax + 8 * SCALE, cy + 4 * SCALE)], fill=TEXT_LIGHT)

    # Center CI Pass Gate Banner
    rx0, ry0 = 50 * SCALE, cy + node_h // 2 + 18 * SCALE
    rx1, ry1 = W - 50 * SCALE, cy + node_h // 2 + 48 * SCALE
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=4 * SCALE, fill=PANEL_BG, outline=EMERALD_GLOW)
    draw.text((W // 2, (ry0 + ry1) // 2), "CI CRITERIA: 0% FALLS ACROSS 1,000 SEEDED RUNS + TORQUE PEAKS < 1.0", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "NO MODEL EVER TOUCHES REAL MOTORS UNTIL IT PASSES HEADLESS PHYSICS GATES", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "devsecops_pipeline.png")


# ============================================================================
# DIAGRAM 3: Edge Security (Cryptographic Signatures & Anti-Tamper)
# ============================================================================
def generate_edge_security():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "3. EDGE SECURITY & ANTI-TAMPER", "ED25519 CRYPTOGRAPHIC SIGNATURES & MODEL INTEGRITY", ROSE)
    
    # Left: Signed Official Policy (Green)
    v_x, v_y = 100 * SCALE, 135 * SCALE
    v_w, v_h = 140 * SCALE, 135 * SCALE
    draw.rounded_rectangle([v_x - v_w // 2, v_y - v_h // 2, v_x + v_w // 2, v_y + v_h // 2],
                           radius=6 * SCALE, fill=(20, 45, 35), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((v_x, v_y - v_h // 2 + 14 * SCALE), "OFFICIAL SIGNED MODEL", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(v_x - v_w // 2 + 6 * SCALE, v_y - v_h // 2 + 25 * SCALE), (v_x + v_w // 2 - 6 * SCALE, v_y - v_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    v_lines = [
        "• File: policy.onnx",
        "• SHA-256: 7d4a90...",
        "• ED25519: VALID",
        "• Signed by Core DevOps",
        "• STATUS: FLASHED ✅"
    ]
    for idx, vl in enumerate(v_lines):
        draw.text((v_x - v_w // 2 + 8 * SCALE, v_y - 18 * SCALE + idx * 15 * SCALE), vl, fill=EMERALD_GLOW if "✅" in vl else TEXT_LIGHT, font=get_font(6, mono=True))

    # Center: Hardware Secure Element / Lock
    draw.circle((W // 2, v_y), 18 * SCALE, fill=(45, 25, 35), outline=ROSE, width=2 * SCALE)
    draw.text((W // 2, v_y), "🛡️", fill=ROSE, font=get_font(10, bold=True), anchor="mm")

    # Right: Tampered / Malicious Policy (Red - Rejected)
    m_x, m_y = W - 100 * SCALE, 135 * SCALE
    m_w, m_h = 140 * SCALE, 135 * SCALE
    draw.rounded_rectangle([m_x - m_w // 2, m_y - m_h // 2, m_x + m_w // 2, m_y + m_h // 2],
                           radius=6 * SCALE, fill=(45, 20, 30), outline=ROSE, width=2 * SCALE)
    draw.text((m_x, m_y - m_h // 2 + 14 * SCALE), "TAMPERED / UNVERIFIED", fill=ROSE, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(m_x - m_w // 2 + 6 * SCALE, m_y - m_h // 2 + 25 * SCALE), (m_x + m_w // 2 - 6 * SCALE, m_y - m_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    m_lines = [
        "• File: hacked_brain.onnx",
        "• SHA-256: e3b0c4... (MISMATCH)",
        "• ED25519: UNTRUSTED",
        "• Rogue WiFi Inject",
        "• STATUS: BLOCKED 🛑"
    ]
    for idx, ml in enumerate(m_lines):
        draw.text((m_x - m_w // 2 + 8 * SCALE, m_y - 18 * SCALE + idx * 15 * SCALE), ml, fill=ROSE if "🛑" in ml else TEXT_LIGHT, font=get_font(6, mono=True))

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "ROOT OF TRUST: HARDWARE REFUSES TO EXECUTE ANY UNVERIFIED NEURAL WEIGHTS", fill=ROSE, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "edge_security.png")


# ============================================================================
# DIAGRAM 4: Telemetry Observability (Fleet Health & Fall Rate Metrics)
# ============================================================================
def generate_telemetry_auth():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "4. FLEET OBSERVABILITY & TELEMETRY", "REAL-TIME IMU DRIFT, FALL-RATES & THERMAL MONITORING", PURPLE)
    
    # 3 Metric Gauges / Panels
    panels = [
        ("Fleet Fall Rate", "0.02 Falls / Hr", "99.8% Stability Score", EMERALD_GLOW, (20, 45, 35)),
        ("Latency Jitter", "± 0.08 ms", "50.0 Hz Real-Time Loop", CYAN_GLOW, (20, 35, 55)),
        ("Motor Thermals", "44.2 °C (Nominal)", "Max Limit: 75.0 °C", AMBER_GLOW, (45, 35, 15)),
    ]
    
    p_w = 110 * SCALE
    p_h = 120 * SCALE
    p_gap = 14 * SCALE
    p_start_x = 22 * SCALE
    p_y = 135 * SCALE - p_h // 2
    
    for idx, (title, val, sub, col_acc, col_bg) in enumerate(panels):
        px = p_start_x + idx * (p_w + p_gap)
        draw.rounded_rectangle([px, p_y, px + p_w, p_y + p_h], radius=6 * SCALE, fill=col_bg, outline=col_acc, width=2 * SCALE)
        draw.text((px + p_w // 2, p_y + 16 * SCALE), title, fill=col_acc, font=get_font(7, bold=True, mono=True), anchor="mm")
        draw.line([(px + 6 * SCALE, p_y + 26 * SCALE), (px + p_w - 6 * SCALE, p_y + 26 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
        
        draw.text((px + p_w // 2, p_y + 55 * SCALE), val, fill=TEXT_LIGHT, font=get_font(8.5, bold=True, mono=True), anchor="mm")
        draw.text((px + p_w // 2, p_y + 85 * SCALE), sub, fill=TEXT_MUTED, font=get_font(5.5, mono=True), anchor="mm")

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "OBSERVABILITY PIPELINE STREAMS DIAGNOSTICS TO DETECT WEAR BEFORE MOTORS FAIL", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "telemetry_auth.png")


def main():
    print("=" * 60)
    print("🎨 Generating 4 Phase 6 Diagrams with Pillow (400x300)...")
    print("=" * 60)
    generate_ota_updates()
    generate_devsecops_pipeline()
    generate_edge_security()
    generate_telemetry_auth()
    print("=" * 60)
    print("✅ All Phase 6 diagrams successfully created in:", IMG_DIR)
    print("=" * 60)

if __name__ == "__main__":
    main()
