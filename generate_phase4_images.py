#!/usr/bin/env python3
"""
generate_phase4_images.py
Generates 4 clean, professional, tech-themed PNG diagrams (size 400x300)
for Phase 4 (Brain Surgery & Edge Inference: Model Extraction & Clamping):
  1. actor_extraction.png - Isolating Actor network and discarding Critic/Optimizer
  2. hardware_clamp.png - Mathematical torch.clamp() safety envelope in silicon
  3. onnx_graph.png - Computational graph export (PyTorch -> ONNX Graph -> ONNX Runtime)
  4. temporal_memory.png - Fixed sliding buffer (deque maxlen=4) vs token explosion
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
# DIAGRAM 1: Actor Extraction (Isolating the Reflexes)
# ============================================================================
def generate_actor_extraction():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "1. SURGICAL ACTOR EXTRACTION", "ISOLATING REFLEXES & DISCARDING TRAINING OVERHEAD", CYAN_ACCENT)
    
    # Left: Heavy PyTorch Training Graph
    box1_x, box1_y = 90 * SCALE, 135 * SCALE
    box1_w, box1_h = 130 * SCALE, 145 * SCALE
    draw.rounded_rectangle([box1_x - box1_w // 2, box1_y - box1_h // 2, box1_x + box1_w // 2, box1_y + box1_h // 2],
                           radius=6 * SCALE, fill=(30, 41, 59), outline=ROSE, width=2 * SCALE)
    draw.text((box1_x, box1_y - box1_h // 2 + 14 * SCALE), "PYTORCH PPO GRAPH (24MB)", fill=ROSE, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(box1_x - box1_w // 2 + 6 * SCALE, box1_y - box1_h // 2 + 25 * SCALE), (box1_x + box1_w // 2 - 6 * SCALE, box1_y - box1_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    # Components inside PyTorch box
    # Actor (Keep)
    draw.rounded_rectangle([box1_x - box1_w // 2 + 8 * SCALE, box1_y - 38 * SCALE, box1_x + box1_w // 2 - 8 * SCALE, box1_y - 2 * SCALE],
                           radius=4 * SCALE, fill=(20, 50, 40), outline=EMERALD_GLOW, width=int(1.5 * SCALE))
    draw.text((box1_x, box1_y - 20 * SCALE), "✓ Actor Policy (π_θ)", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    
    # Critic (Discard)
    draw.rounded_rectangle([box1_x - box1_w // 2 + 8 * SCALE, box1_y + 4 * SCALE, box1_x + box1_w // 2 - 8 * SCALE, box1_y + 30 * SCALE],
                           radius=4 * SCALE, fill=(45, 25, 35), outline=(180, 60, 80), width=1 * SCALE)
    draw.text((box1_x, box1_y + 17 * SCALE), "✗ Critic Value Head (V_φ)", fill=ROSE, font=get_font(6.5, mono=True), anchor="mm")

    # Optimizer (Discard)
    draw.rounded_rectangle([box1_x - box1_w // 2 + 8 * SCALE, box1_y + 36 * SCALE, box1_x + box1_w // 2 - 8 * SCALE, box1_y + 62 * SCALE],
                           radius=4 * SCALE, fill=(45, 25, 35), outline=(180, 60, 80), width=1 * SCALE)
    draw.text((box1_x, box1_y + 49 * SCALE), "✗ Adam State & Autograd", fill=ROSE, font=get_font(6.5, mono=True), anchor="mm")

    # Center: Extraction Scalpel / Arrow
    arrow_y = 135 * SCALE
    draw.line([(box1_x + box1_w // 2 + 8 * SCALE, arrow_y), (W // 2 + 15 * SCALE, arrow_y)], fill=AMBER_GLOW, width=3 * SCALE)
    draw.polygon([(W // 2 + 18 * SCALE, arrow_y), (W // 2 + 10 * SCALE, arrow_y - 5 * SCALE), (W // 2 + 10 * SCALE, arrow_y + 5 * SCALE)], fill=AMBER_GLOW)
    draw.text((W // 2 - 10 * SCALE, arrow_y - 12 * SCALE), "SURGICAL STRIP", fill=AMBER_GLOW, font=get_font(6.5, bold=True, mono=True), anchor="mm")

    # Right: Pure Pruned Reflex Policy
    box2_x, box2_y = W - 85 * SCALE, 135 * SCALE
    box2_w, box2_h = 120 * SCALE, 145 * SCALE
    draw.rounded_rectangle([box2_x - box2_w // 2, box2_y - box2_h // 2, box2_x + box2_w // 2, box2_y + box2_h // 2],
                           radius=6 * SCALE, fill=(20, 45, 35), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((box2_x, box2_y - box2_h // 2 + 14 * SCALE), "PRUNED ACTOR (35KB)", fill=EMERALD_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.line([(box2_x - box2_w // 2 + 6 * SCALE, box2_y - box2_h // 2 + 25 * SCALE), (box2_x + box2_w // 2 - 6 * SCALE, box2_y - box2_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)

    lines = [
        "• Pure Inference Graph",
        "• Deterministic Mean μ(s)",
        "• Zero Autograd Overhead",
        "• Clamped [-1.0, 1.0]",
        "• Latency: < 2.5ms"
    ]
    for idx, l in enumerate(lines):
        draw.text((box2_x - box2_w // 2 + 10 * SCALE, box2_y - 20 * SCALE + idx * 16 * SCALE), l, fill=TEXT_LIGHT, font=get_font(6.5, mono=True))

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "99.8% SIZE REDUCTION: EXTRACTS PURE REFLEXES FOR LOW-POWER SILICON", fill=EMERALD_GLOW, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "actor_extraction.png")


# ============================================================================
# DIAGRAM 2: Hardware Clamp (Silicon Safety Limits)
# ============================================================================
def generate_hardware_clamp():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "2. HARDWARE SAFETY CLAMPING", "torch.clamp() BAKED MATHEMATICAL SILICON SAFETY", EMERALD)
    
    # Main Coordinate Graph of Clamping
    cx, cy = W // 2 - 25 * SCALE, 140 * SCALE
    gw, gh = 180 * SCALE, 120 * SCALE
    gx0, gy0 = cx - gw // 2, cy - gh // 2
    gx1, gy1 = cx + gw // 2, cy + gh // 2
    
    draw.rounded_rectangle([gx0, gy0, gx1, gy1], radius=6 * SCALE, fill=(20, 28, 45), outline=BORDER_COLOR)
    
    # Axes (Center origin)
    draw.line([(gx0 + 15 * SCALE, cy), (gx1 - 15 * SCALE, cy)], fill=BORDER_COLOR, width=1 * SCALE)
    draw.line([(cx, gy0 + 10 * SCALE), (cx, gy1 - 10 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    draw.text((gx1 - 10 * SCALE, cy + 4 * SCALE), "x", fill=TEXT_MUTED, font=get_font(7, mono=True))
    draw.text((cx + 5 * SCALE, gy0 + 12 * SCALE), "y", fill=TEXT_MUTED, font=get_font(7, mono=True))
    
    # Clamp Limits (+1.0 and -1.0 horizontal lines)
    y_p1 = cy - 35 * SCALE
    y_m1 = cy + 35 * SCALE
    x_p1 = cx + 35 * SCALE
    x_m1 = cx - 35 * SCALE
    
    draw.line([(gx0 + 10 * SCALE, y_p1), (gx1 - 10 * SCALE, y_p1)], fill=(40, 70, 60), width=1 * SCALE)
    draw.line([(gx0 + 10 * SCALE, y_m1), (gx1 - 10 * SCALE, y_m1)], fill=(40, 70, 60), width=1 * SCALE)
    draw.text((gx0 + 14 * SCALE, y_p1 - 8 * SCALE), "+1.0 Limit (Max Motor CCW)", fill=EMERALD_GLOW, font=get_font(6, mono=True))
    draw.text((gx0 + 14 * SCALE, y_m1 + 8 * SCALE), "-1.0 Limit (Max Motor CW)", fill=ROSE, font=get_font(6, mono=True))
    
    # Clamped Function Line: y = clamp(x, -1, 1)
    pts_clamped = [
        (gx0 + 20 * SCALE, y_m1),
        (x_m1, y_m1),
        (x_p1, y_p1),
        (gx1 - 20 * SCALE, y_p1)
    ]
    draw.line(pts_clamped, fill=CYAN_GLOW, width=3 * SCALE)
    
    # Unclamped Dangerous Danger Zone (Dashed Red Lines extending out)
    draw.line([(x_p1, y_p1), (gx1 - 20 * SCALE, gy0 + 10 * SCALE)], fill=ROSE, width=2 * SCALE)
    draw.line([(x_m1, y_m1), (gx0 + 20 * SCALE, gy1 - 10 * SCALE)], fill=ROSE, width=2 * SCALE)
    draw.text((gx1 - 25 * SCALE, gy0 + 16 * SCALE), "Stripped Gears!", fill=ROSE, font=get_font(6, bold=True, mono=True), anchor="ra")

    # Right Card: Hardware Guarantee
    card_x0, card_y0 = W - 110 * SCALE, 50 * SCALE
    card_x1, card_y1 = W - 15 * SCALE, 160 * SCALE
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=5 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((card_x0 + 8 * SCALE, card_y0 + 8 * SCALE), "SAFETY GUARANTEE", fill=AMBER_GLOW, font=get_font(7, bold=True, mono=True))
    draw.text((card_x0 + 8 * SCALE, card_y0 + 22 * SCALE), "• Bounded in Silicon", fill=TEXT_LIGHT, font=get_font(6, mono=True))
    draw.text((card_x0 + 8 * SCALE, card_y0 + 35 * SCALE), "• 0% Software Gear Strip", fill=EMERALD_GLOW, font=get_font(6, mono=True))
    draw.text((card_x0 + 8 * SCALE, card_y0 + 48 * SCALE), "• ONNX Clip Operator", fill=CYAN_GLOW, font=get_font(6, mono=True))
    draw.text((card_x0 + 8 * SCALE, card_y0 + 61 * SCALE), "• Failsafe Firmware", fill=TEXT_MUTED, font=get_font(6, mono=True))

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "torch.clamp(a, -1.0, 1.0): ABSOLUTE SILICON PROTECTION AGAINST RUNAWAY GRADIENTS", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "hardware_clamp.png")


# ============================================================================
# DIAGRAM 3: ONNX Computational Graph
# ============================================================================
def generate_onnx_graph():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "3. ONNX COMPUTATIONAL GRAPH", "CROSS-PLATFORM INTERMEDIATE REPRESENTATION & RUNTIME", AMBER)
    
    # 4 Nodes in vertical/horizontal computation flow
    nodes = [
        ("Input Tensor", "[1, 60] Floats", CYAN_ACCENT, (25, 45, 75)),
        ("Gemm + ReLU", "Weights [60, 256]", AMBER, (55, 45, 20)),
        ("Gemm + ReLU", "Weights [256, 15]", PURPLE, (45, 25, 60)),
        ("Clip [-1, 1]", "15 Motor Targets", EMERALD, (20, 50, 35)),
    ]
    
    start_x = 25 * SCALE
    node_w = 78 * SCALE
    node_h = 85 * SCALE
    gap = 18 * SCALE
    cy = 135 * SCALE
    
    for idx, (title, desc, col_acc, col_bg) in enumerate(nodes):
        nx = start_x + idx * (node_w + gap)
        ny = cy - node_h // 2
        
        draw.rounded_rectangle([nx, ny, nx + node_w, ny + node_h], radius=6 * SCALE, fill=col_bg, outline=col_acc, width=2 * SCALE)
        draw.text((nx + node_w // 2, ny + 16 * SCALE), title, fill=col_acc, font=get_font(7, bold=True, mono=True), anchor="mm")
        draw.line([(nx + 6 * SCALE, ny + 26 * SCALE), (nx + node_w - 6 * SCALE, ny + 26 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
        
        draw.text((nx + node_w // 2, ny + 45 * SCALE), desc, fill=TEXT_LIGHT, font=get_font(6.5, mono=True), anchor="mm")
        
        # Arrow
        if idx < 3:
            ax = nx + node_w + 2 * SCALE
            draw.line([(ax, cy), (ax + 12 * SCALE, cy)], fill=TEXT_LIGHT, width=2 * SCALE)
            draw.polygon([(ax + 14 * SCALE, cy), (ax + 8 * SCALE, cy - 4 * SCALE), (ax + 8 * SCALE, cy + 4 * SCALE)], fill=TEXT_LIGHT)

    # Edge Runtime Box at Bottom Center
    rx0, ry0 = 50 * SCALE, cy + node_h // 2 + 18 * SCALE
    rx1, ry1 = W - 50 * SCALE, cy + node_h // 2 + 48 * SCALE
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=4 * SCALE, fill=PANEL_BG, outline=CYAN_GLOW)
    draw.text((W // 2, (ry0 + ry1) // 2), "EXECUTED VIA onnxruntime ON ROCKCHIP RK3566 NPU / CPU IN < 2.5ms", fill=CYAN_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "OPSET 17: PURE MATHEMATICAL TENSOR GRAPH INDEPENDENT OF PYTHON RUNTIMES", fill=TEXT_MUTED, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "onnx_graph.png")


# ============================================================================
# DIAGRAM 4: Temporal Memory (Sliding Buffer vs Token Explosion)
# ============================================================================
def generate_temporal_memory():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "4. TEMPORAL MEMORY BUFFER", "FIXED DEQUE(MAXLEN=4) VS EXPONENTIAL TOKEN EXPLOSION", PURPLE)
    
    # Left: Sliding Window Buffer (Physical AI Method)
    lx, ly = W // 4 + 10 * SCALE, 135 * SCALE
    lw, lh = 160 * SCALE, 130 * SCALE
    draw.rounded_rectangle([lx - lw // 2, ly - lh // 2, lx + lw // 2, ly + lh // 2], radius=6 * SCALE,
                           fill=(25, 45, 65), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((lx, ly - lh // 2 + 14 * SCALE), "SLIDING WINDOW (deque maxlen=4)", fill=EMERALD_GLOW, font=get_font(6.5, bold=True, mono=True), anchor="mm")
    draw.line([(lx - lw // 2 + 6 * SCALE, ly - lh // 2 + 24 * SCALE), (lx + lw // 2 - 6 * SCALE, ly - lh // 2 + 24 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)

    # 4 Frames in Queue
    f_w = 32 * SCALE
    f_h = 36 * SCALE
    f_gap = 4 * SCALE
    f_start_x = lx - lw // 2 + 12 * SCALE
    f_y = ly - 8 * SCALE
    
    for i, lbl in enumerate(["t-3", "t-2", "t-1", "t (New)"]):
        fx = f_start_x + i * (f_w + f_gap)
        c_fill = (20, 50, 40) if i == 3 else (20, 30, 45)
        c_out = EMERALD_GLOW if i == 3 else CYAN_GLOW
        draw.rounded_rectangle([fx, f_y, fx + f_w, f_y + f_h], radius=3 * SCALE, fill=c_fill, outline=c_out, width=int(1.5 * SCALE))
        draw.text((fx + f_w // 2, f_y + 12 * SCALE), lbl, fill=TEXT_LIGHT, font=get_font(6, bold=True, mono=True), anchor="mm")
        draw.text((fx + f_w // 2, f_y + 24 * SCALE), "15 floats", fill=TEXT_MUTED, font=get_font(5.5, mono=True), anchor="mm")

    draw.text((lx, ly + 40 * SCALE), "Total Tensor: [1, 60] Floats", fill=CYAN_GLOW, font=get_font(6.5, bold=True, mono=True), anchor="mm")
    draw.text((lx, ly + 52 * SCALE), "Latency: 2.5ms (Constant O(1))", fill=EMERALD_GLOW, font=get_font(6.5, mono=True), anchor="mm")

    # Right: LLM Context Window (Token Explosion - Bad for 50Hz)
    rx, ry = 3 * W // 4 - 10 * SCALE, 135 * SCALE
    rw, rh = 160 * SCALE, 130 * SCALE
    draw.rounded_rectangle([rx - rw // 2, ry - rh // 2, rx + rw // 2, ry + rh // 2], radius=6 * SCALE,
                           fill=(35, 25, 40), outline=ROSE, width=2 * SCALE)
    draw.text((rx, ry - rh // 2 + 14 * SCALE), "UNBOUNDED CONTEXT (LLM / RNN)", fill=ROSE, font=get_font(6.5, bold=True, mono=True), anchor="mm")
    draw.line([(rx - rw // 2 + 6 * SCALE, ry - rh // 2 + 24 * SCALE), (rx + rw // 2 - 6 * SCALE, ry - rh // 2 + 24 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)

    llm_lines = [
        "[-] O(N²) Quadratic Memory",
        "[-] Latency Explosion (>500ms)",
        "[-] Misses 20ms Control Deadline",
        "[-] Robot Falls Over Instantly",
        "[-] Unfit for Physical Reflexes"
    ]
    for idx, l in enumerate(llm_lines):
        draw.text((rx - rw // 2 + 10 * SCALE, ry - 14 * SCALE + idx * 14 * SCALE), l, fill=ROSE if "[-]" in l else TEXT_MUTED, font=get_font(6, mono=True))

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "FIXED TEMPORAL HORIZON PROVIDES VELOCITY & ACCELERATION AWARENESS WITH ZERO LATENCY", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "temporal_memory.png")


def main():
    print("=" * 60)
    print("🎨 Generating 4 Phase 4 Diagrams with Pillow (400x300)...")
    print("=" * 60)
    generate_actor_extraction()
    generate_hardware_clamp()
    generate_onnx_graph()
    generate_temporal_memory()
    print("=" * 60)
    print("✅ All Phase 4 diagrams successfully created in:", IMG_DIR)
    print("=" * 60)

if __name__ == "__main__":
    main()
