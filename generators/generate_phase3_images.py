#!/usr/bin/env python3
"""
generate_phase3_images.py
Generates 4 clean, professional, tech-themed PNG diagrams (size 400x300)
for Phase 3 (The Dog Trainer: Reinforcement Learning & PPO Architecture):
  1. rl_gym.png - RL Environment-Agent Step Loop & Telemetry Flow
  2. reward_function.png - Reward function mathematics & penalty budgeting
  3. ppo_actor_critic.png - Actor-Critic architecture with PPO clipping envelope
  4. curriculum_learning.png - Staged progressive learning & domain randomization ladder
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
# DIAGRAM 1: RL Gym Loop (State, Action, Reward, Observation Buffer)
# ============================================================================
def generate_rl_gym():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "1. RL GYMNASIUM INTERFACE", "STATE-ACTION-REWARD REAL-TIME CONTROL CADENCE", CYAN_ACCENT)
    
    # Left Box: Agent (PPO Neural Policy)
    ag_x, ag_y = 80 * SCALE, 140 * SCALE
    ag_w, ag_h = 105 * SCALE, 110 * SCALE
    draw.rounded_rectangle([ag_x - ag_w // 2, ag_y - ag_h // 2, ag_x + ag_w // 2, ag_y + ag_h // 2],
                           radius=6 * SCALE, fill=(25, 45, 75), outline=CYAN_GLOW, width=2 * SCALE)
    draw.text((ag_x, ag_y - ag_h // 2 + 14 * SCALE), "AGENT (POLICY)", fill=CYAN_GLOW, font=get_font(7.5, bold=True, mono=True), anchor="mm")
    draw.line([(ag_x - ag_w // 2 + 6 * SCALE, ag_y - ag_h // 2 + 25 * SCALE), (ag_x + ag_w // 2 - 6 * SCALE, ag_y - ag_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    draw.text((ag_x, ag_y - 6 * SCALE), "Actor-Critic", fill=TEXT_LIGHT, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.text((ag_x, ag_y + 10 * SCALE), "MLP [256, 256]", fill=TEXT_MUTED, font=get_font(6.5, mono=True), anchor="mm")
    draw.text((ag_x, ag_y + 26 * SCALE), "torch.clamp()", fill=EMERALD_GLOW, font=get_font(6.5, mono=True), anchor="mm")

    # Right Box: Environment (MuJoCo Physics Simulation)
    env_x, env_y = W - 80 * SCALE, 140 * SCALE
    env_w, env_h = 105 * SCALE, 110 * SCALE
    draw.rounded_rectangle([env_x - env_w // 2, env_y - env_h // 2, env_x + env_w // 2, env_y + env_h // 2],
                           radius=6 * SCALE, fill=(30, 50, 40), outline=EMERALD_GLOW, width=2 * SCALE)
    draw.text((env_x, env_y - env_h // 2 + 14 * SCALE), "ENVIRONMENT", fill=EMERALD_GLOW, font=get_font(7.5, bold=True, mono=True), anchor="mm")
    draw.line([(env_x - env_w // 2 + 6 * SCALE, env_y - env_h // 2 + 25 * SCALE), (env_x + env_w // 2 - 6 * SCALE, env_y - env_h // 2 + 25 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
    
    draw.text((env_x, env_y - 6 * SCALE), "MuJoCo Sandbox", fill=TEXT_LIGHT, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.text((env_x, env_y + 10 * SCALE), "mj_step(m, d)", fill=TEXT_MUTED, font=get_font(6.5, mono=True), anchor="mm")
    draw.text((env_x, env_y + 26 * SCALE), "15 Motors (50Hz)", fill=AMBER_GLOW, font=get_font(6.5, mono=True), anchor="mm")

    # Top Arrow: Action a_t (Agent -> Env)
    top_y = 100 * SCALE
    draw.line([(ag_x + ag_w // 2, top_y), (env_x - env_w // 2, top_y)], fill=AMBER_GLOW, width=3 * SCALE)
    draw.polygon([(env_x - env_w // 2, top_y), (env_x - env_w // 2 - 8 * SCALE, top_y - 4 * SCALE), (env_x - env_w // 2 - 8 * SCALE, top_y + 4 * SCALE)], fill=AMBER_GLOW)
    draw.text((W // 2, top_y - 12 * SCALE), "ACTION: a_t ∈ [-1.0, 1.0]^15", fill=AMBER_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Bottom Arrow 1: Observation o_{t+1} (Env -> Agent)
    bot_y1 = 165 * SCALE
    draw.line([(env_x - env_w // 2, bot_y1), (ag_x + ag_w // 2, bot_y1)], fill=CYAN_GLOW, width=3 * SCALE)
    draw.polygon([(ag_x + ag_w // 2, bot_y1), (ag_x + ag_w // 2 + 8 * SCALE, bot_y1 - 4 * SCALE), (ag_x + ag_w // 2 + 8 * SCALE, bot_y1 + 4 * SCALE)], fill=CYAN_GLOW)
    draw.text((W // 2, bot_y1 - 10 * SCALE), "OBSERVATION: s_t (60 Floats / 4 Frames)", fill=CYAN_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")

    # Bottom Arrow 2: Reward r_t (Env -> Agent)
    bot_y2 = 195 * SCALE
    draw.line([(env_x - env_w // 2, bot_y2), (ag_x + ag_w // 2, bot_y2)], fill=EMERALD_GLOW, width=2 * SCALE)
    draw.polygon([(ag_x + ag_w // 2, bot_y2), (ag_x + ag_w // 2 + 8 * SCALE, bot_y2 - 4 * SCALE), (ag_x + ag_w // 2 + 8 * SCALE, bot_y2 + 4 * SCALE)], fill=EMERALD_GLOW)
    draw.text((W // 2, bot_y2 + 10 * SCALE), "REWARD: r_t = r_alive + r_fwd - r_energy", fill=EMERALD_GLOW, font=get_font(6.5, bold=True, mono=True), anchor="mm")

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "STEP CADENCE: 50 ACTIONS / SECOND (20ms) SYNCHRONIZED WITH ONNX EDGE", fill=TEXT_LIGHT, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "rl_gym.png")


# ============================================================================
# DIAGRAM 2: Reward Function (Math Composition & Penalty Budgeting)
# ============================================================================
def generate_reward_function():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "2. REWARD FUNCTION ARCHITECTURE", "BALANCING POSITIVE INCENTIVES & REGULARIZATION PENALTIES", EMERALD)
    
    # 4 Reward Component Bars (Stacked horizontal breakdown)
    components = [
        ("r_upright (+1.0)", "Posture Bonus (Keep Torso Z > 0.22m)", EMERALD_GLOW, 0.35),
        ("r_forward (+2.0 * vx)", "Locomotion Incentive (Match Target Speed)", CYAN_GLOW, 0.40),
        ("r_torque (-0.005 * ||τ||²)", "Energy Regularizer (Prevent Motor Burnout)", AMBER_GLOW, 0.15),
        ("r_jerk (-0.01 * ||Δa||²)", "Smoothness Penalty (Eliminate High-Freq Shake)", ROSE, 0.10),
    ]
    
    start_y = 52 * SCALE
    bar_h = 42 * SCALE
    gap = 8 * SCALE
    
    for idx, (title, desc, col, weight) in enumerate(components):
        by = start_y + idx * (bar_h + gap)
        # Card Container
        draw.rounded_rectangle([30 * SCALE, by, W - 30 * SCALE, by + bar_h], radius=5 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
        # Left color bar
        draw.rounded_rectangle([30 * SCALE, by, 36 * SCALE, by + bar_h], radius=2 * SCALE, fill=col)
        
        # Component Title & Value
        draw.text((45 * SCALE, by + 8 * SCALE), title, fill=col, font=get_font(8, bold=True, mono=True))
        draw.text((45 * SCALE, by + 23 * SCALE), desc, fill=TEXT_LIGHT, font=get_font(6.5, mono=True))
        
        # Mini Visual Gauge Bar on Right
        gw = 90 * SCALE
        gx = W - 130 * SCALE
        gy = by + 14 * SCALE
        draw.rounded_rectangle([gx, gy, gx + gw, gy + 14 * SCALE], radius=3 * SCALE, fill=(15, 23, 42), outline=BORDER_COLOR)
        draw.rounded_rectangle([gx + 2 * SCALE, gy + 2 * SCALE, gx + 2 * SCALE + int((gw - 4 * SCALE) * weight), gy + 12 * SCALE],
                               radius=2 * SCALE, fill=col)
        draw.text((gx + gw + 10 * SCALE, gy + 7 * SCALE), f"{int(weight * 100)}%", fill=TEXT_MUTED, font=get_font(6, mono=True), anchor="lm")

    # Bottom Formula Card
    draw.rounded_rectangle([30 * SCALE, H - 32 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=(20, 45, 35), outline=EMERALD_GLOW)
    draw.text((W // 2, H - 20 * SCALE), "TOTAL REWARD: R_t = w_1·r_alive + w_2·r_fwd - w_3·||τ||² - w_4·||Δa||²", fill=TEXT_LIGHT, font=get_font(7, bold=True, mono=True), anchor="mm")

    save_image(img, "reward_function.png")


# ============================================================================
# DIAGRAM 3: PPO Actor-Critic (Neural Architecture & Clipped Objective)
# ============================================================================
def generate_ppo_actor_critic():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "3. PPO ACTOR-CRITIC ARCHITECTURE", "COACH (VALUE ESTIMATE) & ATHLETE (MOTOR ACTION GRAPH)", AMBER)
    
    # Left: Dual Neural Networks
    net_x = 100 * SCALE
    
    # Input Observation Layer
    in_y = 75 * SCALE
    draw.rounded_rectangle([net_x - 70 * SCALE, in_y - 12 * SCALE, net_x + 70 * SCALE, in_y + 12 * SCALE],
                           radius=4 * SCALE, fill=PANEL_BG, outline=CYAN_GLOW)
    draw.text((net_x, in_y), "Observation Tensor [60 Floats]", fill=CYAN_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    
    # Actor Network Branch (Top Right)
    act_y = 135 * SCALE
    draw.rounded_rectangle([net_x - 75 * SCALE, act_y - 18 * SCALE, net_x + 75 * SCALE, act_y + 18 * SCALE],
                           radius=5 * SCALE, fill=(25, 45, 75), outline=AMBER_GLOW, width=2 * SCALE)
    draw.text((net_x, act_y - 6 * SCALE), "ACTOR NETWORK π_θ(a|s)", fill=AMBER_GLOW, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.text((net_x, act_y + 8 * SCALE), "Outputs 15 Motor Targets [-1, 1]", fill=TEXT_LIGHT, font=get_font(6.5, mono=True), anchor="mm")

    # Critic Network Branch (Bottom Right)
    crit_y = 195 * SCALE
    draw.rounded_rectangle([net_x - 75 * SCALE, crit_y - 18 * SCALE, net_x + 75 * SCALE, crit_y + 18 * SCALE],
                           radius=5 * SCALE, fill=(35, 25, 55), outline=PURPLE, width=2 * SCALE)
    draw.text((net_x, crit_y - 6 * SCALE), "CRITIC NETWORK V_φ(s)", fill=PURPLE, font=get_font(7, bold=True, mono=True), anchor="mm")
    draw.text((net_x, crit_y + 8 * SCALE), "Estimates State Value Score V(s)", fill=TEXT_LIGHT, font=get_font(6.5, mono=True), anchor="mm")

    # Connecting branch lines
    draw.line([(net_x, in_y + 12 * SCALE), (net_x, act_y - 18 * SCALE)], fill=CYAN_ACCENT, width=2 * SCALE)
    draw.line([(net_x - 50 * SCALE, in_y + 12 * SCALE), (net_x - 50 * SCALE, crit_y - 18 * SCALE)], fill=CYAN_ACCENT, width=1 * SCALE)

    # Right: PPO Clipping Envelope Curve
    ch_x0, ch_y0 = W - 170 * SCALE, 65 * SCALE
    ch_w, ch_h = 150 * SCALE, 150 * SCALE
    ch_x1, ch_y1 = ch_x0 + ch_w, ch_y0 + ch_h
    
    draw.rounded_rectangle([ch_x0, ch_y0, ch_x1, ch_y1], radius=6 * SCALE, fill=(20, 28, 45), outline=BORDER_COLOR)
    draw.text((ch_x0 + ch_w // 2, ch_y0 + 12 * SCALE), "PPO CLIPPED OBJECTIVE L_CLIP", fill=TEXT_LIGHT, font=get_font(6.5, bold=True, mono=True), anchor="mm")
    
    # Axes
    ax_ox = ch_x0 + 20 * SCALE
    ax_oy = ch_y1 - 25 * SCALE
    draw.line([(ax_ox, ch_y0 + 25 * SCALE), (ax_ox, ax_oy)], fill=BORDER_COLOR, width=1 * SCALE)
    draw.line([(ax_ox, ax_oy), (ch_x1 - 10 * SCALE, ax_oy)], fill=BORDER_COLOR, width=1 * SCALE)
    
    # Clipping bounds (1 - eps, 1 + eps)
    draw.line([(ax_ox + 40 * SCALE, ch_y0 + 25 * SCALE), (ax_ox + 40 * SCALE, ax_oy)], fill=(70, 50, 60), width=1 * SCALE)
    draw.line([(ax_ox + 90 * SCALE, ch_y0 + 25 * SCALE), (ax_ox + 90 * SCALE, ax_oy)], fill=(70, 50, 60), width=1 * SCALE)
    draw.text((ax_ox + 40 * SCALE, ax_oy + 8 * SCALE), "1-ε", fill=ROSE, font=get_font(6, mono=True), anchor="mm")
    draw.text((ax_ox + 90 * SCALE, ax_oy + 8 * SCALE), "1+ε", fill=EMERALD_GLOW, font=get_font(6, mono=True), anchor="mm")

    # Clipped policy curve
    pts = [
        (ax_ox + 5 * SCALE, ax_oy - 10 * SCALE),
        (ax_ox + 40 * SCALE, ax_oy - 40 * SCALE),
        (ax_ox + 90 * SCALE, ax_oy - 75 * SCALE),
        (ch_x1 - 15 * SCALE, ax_oy - 75 * SCALE)
    ]
    draw.line(pts, fill=EMERALD_GLOW, width=3 * SCALE)
    draw.text((ch_x1 - 25 * SCALE, ax_oy - 85 * SCALE), "Clipped", fill=EMERALD_GLOW, font=get_font(6, mono=True), anchor="mm")

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "PPO ENSURES SAFE GRADIENT STEPS: PREVENTS DESTRUCTIVE WEIGHT EXPLOSIONS", fill=AMBER_GLOW, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "ppo_actor_critic.png")


# ============================================================================
# DIAGRAM 4: Curriculum Learning (Progression Ladder & Domain Randomization)
# ============================================================================
def generate_curriculum_learning():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_grid(draw)
    draw_header_badge(draw, "4. CURRICULUM & DOMAIN RANDOMIZATION", "PROGRESSIVE 4-STAGE TRAINING LADDER & SIM-TO-REAL ROBUSTNESS", PURPLE)
    
    # 4 Progressive Steps (Ascending Staircase / Ladder)
    stages = [
        ("STAGE 1: STAND STILL", "Keep Torso Z > 0.22m\nZero joint jerk\n200k steps", CYAN_ACCENT, (25, 45, 75)),
        ("STAGE 2: PUSH RECOVERY", "Lateral impulse forces\nIMU pitch/roll balance\n500k steps", EMERALD, (20, 50, 35)),
        ("STAGE 3: FORWARD GAIT", "Target speed v=0.4m/s\nAlternating leg cycle\n1.2M steps", AMBER, (55, 45, 20)),
        ("STAGE 4: SIM-TO-REAL", "Domain Randomization\nMass ±15%, Friction ±20%\n2.5M steps", PURPLE, (45, 25, 60)),
    ]
    
    step_w = 78 * SCALE
    step_h = 32 * SCALE
    base_x = 26 * SCALE
    base_y = H - 55 * SCALE
    
    for idx, (title, desc, col_accent, col_bg) in enumerate(stages):
        sx = base_x + idx * (step_w + 14 * SCALE)
        sy = base_y - (idx + 1) * 36 * SCALE
        
        # Step Box
        draw.rounded_rectangle([sx, sy, sx + step_w, sy + 60 * SCALE + idx * 36 * SCALE],
                               radius=5 * SCALE, fill=col_bg, outline=col_accent, width=2 * SCALE)
        # Stage Badge
        draw.text((sx + step_w // 2, sy + 14 * SCALE), title, fill=col_accent, font=get_font(6.5, bold=True, mono=True), anchor="mm")
        draw.line([(sx + 6 * SCALE, sy + 24 * SCALE), (sx + step_w - 6 * SCALE, sy + 24 * SCALE)], fill=BORDER_COLOR, width=1 * SCALE)
        
        # Description lines
        for d_idx, d_line in enumerate(desc.split("\n")):
            draw.text((sx + step_w // 2, sy + 36 * SCALE + d_idx * 13 * SCALE), d_line, fill=TEXT_LIGHT if d_idx == 0 else TEXT_MUTED,
                      font=get_font(6, mono=True), anchor="mm")

        # Ascending arrow indicator
        if idx < 3:
            draw.line([(sx + step_w + 2 * SCALE, sy + 10 * SCALE), (sx + step_w + 12 * SCALE, sy - 15 * SCALE)], fill=TEXT_LIGHT, width=2 * SCALE)
            draw.polygon([(sx + step_w + 12 * SCALE, sy - 15 * SCALE), (sx + step_w + 5 * SCALE, sy - 12 * SCALE), (sx + step_w + 10 * SCALE, sy - 5 * SCALE)], fill=TEXT_LIGHT)

    # Bottom Banner
    draw.rounded_rectangle([30 * SCALE, H - 24 * SCALE, W - 30 * SCALE, H - 8 * SCALE], radius=4 * SCALE, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((W // 2, H - 16 * SCALE), "GRADUAL COMPLEXITY PREVENTS POLICY COLLAPSE AND ENSURES HARDWARE TRANSFER", fill=EMERALD_GLOW, font=get_font(7, mono=True), anchor="mm")

    save_image(img, "curriculum_learning.png")


def main():
    print("=" * 60)
    print("🎨 Generating 4 Phase 3 Diagrams with Pillow (400x300)...")
    print("=" * 60)
    generate_rl_gym()
    generate_reward_function()
    generate_ppo_actor_critic()
    generate_curriculum_learning()
    print("=" * 60)
    print("✅ All Phase 3 diagrams successfully created in:", IMG_DIR)
    print("=" * 60)

if __name__ == "__main__":
    main()
