#!/usr/bin/env python3
"""
generate_phase3_handout.py
Generates the official "Microduck Physical AI Masterclass - Phase 3: The Dog Trainer"
handout using the 'Diagram Method', embedding 4 technical Pillow diagrams next to
their descriptive engineering and pedagogical text, plus a 5-question Knowledge Check.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas

# Ensure paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
IMG_DIR = os.path.join(PROJECT_ROOT, "images")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)
PDF_OUTPUT = os.path.join(DOCS_DIR, "Phase3_DogTrainer_Handout.pdf")

REQUIRED_IMAGES = [
    "rl_gym.png",
    "reward_function.png",
    "ppo_actor_critic.png",
    "curriculum_learning.png"
]

def ensure_images():
    missing = [img for img in REQUIRED_IMAGES if not os.path.exists(os.path.join(IMG_DIR, img))]
    if missing:
        print(f"⚠️ Missing Phase 3 images: {missing}. Generating them now...")
        import generate_phase3_images
        generate_phase3_images.main()


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        page_w, page_h = letter
        margin = 36

        # Running Header (Pages 2+)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(margin, page_h - 26, "🦆 MICRODUCK PHYSICAL AI MASTERCLASS")
            self.setFont("Helvetica", 8)
            self.drawRightString(page_w - margin, page_h - 26, "Phase 3: The Dog Trainer — Reinforcement Learning & PPO")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.75)
            self.line(margin, page_h - 30, page_w - margin, page_h - 30)

        # Running Footer (All Pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(margin, 38, page_w - margin, 38)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(margin, 26, "Confidential & Proprietary • Physical AI Robotics Stack")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(page_w - margin, 26, page_str)
        self.restoreState()


def create_handout(output_path=PDF_OUTPUT):
    ensure_images()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor("#ffffff"),
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#94a3b8"),
        alignment=0
    )

    spec_bar_style = ParagraphStyle(
        'SpecBar',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#f59e0b")
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor("#0f172a")
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#d97706")
    )

    body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor("#334155")
    )

    bullet_style = ParagraphStyle(
        'CardBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # =========================================================================
    # HEADER BANNER (Page 1 Top)
    # =========================================================================
    banner_content = [
        [
            Paragraph("🦆 MICRODUCK PHYSICAL AI MASTERCLASS", title_style),
            Paragraph("<b>PHASE 3 HANDOUT</b>", ParagraphStyle('Tag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#f59e0b"), alignment=2))
        ],
        [
            Paragraph("<b>Module 3: The Dog Trainer:</b> Gym Environments, Reward Engineering, PPO & Curriculum Learning", subtitle_style),
            Paragraph("RL & PPO", ParagraphStyle('Tag2', parent=badge_style, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"), alignment=2))
        ]
    ]
    banner_table = Table(banner_content, colWidths=[420, 110])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('PADDING', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 0),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 6))

    # Quick Metadata Strip
    meta_data = [
        [
            Paragraph("<b>ALGORITHM:</b> PPO (Clipped)", spec_bar_style),
            Paragraph("<b>OBSERVATION:</b> 60 Floats (4 Frames)", spec_bar_style),
            Paragraph("<b>ACTION:</b> 15 Clamped [-1, 1]", spec_bar_style),
            Paragraph("<b>FREQUENCY:</b> 50 Hz Control Loop", spec_bar_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[130, 150, 130, 120])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    def build_diagram_card(img_filename, title, subtitle_category, accent_color_hex, desc_paragraphs, bullet_items):
        img_path = os.path.join(IMG_DIR, img_filename)
        img_flowable = Image(img_path, width=195, height=146.25)

        text_elements = []
        header_table = Table([
            [
                Paragraph(f"<font color='{accent_color_hex}'><b>■</b></font> <b>{title}</b>", section_header_style),
                Paragraph(f"<b>{subtitle_category.upper()}</b>", ParagraphStyle('Cat', parent=badge_style, textColor=colors.HexColor(accent_color_hex), alignment=2))
            ]
        ], colWidths=[205, 115])
        header_table.setStyle(TableStyle([
            ('PADDING', (0, 0), (-1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        text_elements.append(header_table)
        text_elements.append(Spacer(1, 3))
        text_elements.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#e2e8f0"), spaceAfter=4, spaceBefore=0))

        for p in desc_paragraphs:
            text_elements.append(Paragraph(p, body_style))
            text_elements.append(Spacer(1, 2.5))

        if bullet_items:
            for b_lbl, b_val in bullet_items:
                bullet_text = f"• <b>{b_lbl}</b>: {b_val}"
                text_elements.append(Paragraph(bullet_text, bullet_style))
                text_elements.append(Spacer(1, 1.2))

        card_table = Table(
            [[img_flowable, text_elements]],
            colWidths=[200, 330]
        )
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ('LINELEFT', (0, 0), (0, -1), 3.5, colors.HexColor(accent_color_hex)),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ]))
        return card_table

    # =========================================================================
    # MODULE 1: RL GYM INTERFACE
    # =========================================================================
    card1 = build_diagram_card(
        img_filename="rl_gym.png",
        title="1. Gymnasium Environment & State Loop",
        subtitle_category="Observation & Action Cadence",
        accent_color_hex="#0284c7",
        desc_paragraphs=[
            "<b>The RL Paradigm:</b> The policy observes a sliding history tensor $s_t \\in \\mathbb{R}^{60}$, infers 15 normalized motor velocity actions $a_t \\in [-1.0, 1.0]$, and receives a scalar reward.",
            "<b>The 12-Year-Old Analogy:</b> When you train a puppy to fetch, you don't pick up its paws. You show it the ball, watch what it does, and toss a biscuit when it brings it back."
        ],
        bullet_items=[
            ("Observation Space", "Box(-inf, inf, shape=(60,), float32) representing 4 frames × 15 sensors."),
            ("Action Space", "Box(-1.0, 1.0, shape=(15,), float32) target joint velocities."),
            ("50Hz Execution", "Strict 20ms step cadence ensuring zero sim-to-real timing discrepancy.")
        ]
    )
    story.append(card1)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 2: REWARD FUNCTION MATHEMATICS
    # =========================================================================
    card2 = build_diagram_card(
        img_filename="reward_function.png",
        title="2. Reward Engineering & Penalties",
        subtitle_category="Balancing Progress vs Energy Burn",
        accent_color_hex="#059669",
        desc_paragraphs=[
            "<b>Mathematical Incentive Design:</b> $R_t = w_{up} r_{up} + w_{fwd} r_{fwd} - w_\\tau ||\\tau||^2 - w_j ||\\Delta a||^2$. The agent is penalized for high torque and action jerk.",
            "<b>The 12-Year-Old Analogy:</b> If you only reward speed, the duck will throw itself down the stairs to cross the line. You must penalize falling and shaking."
        ],
        bullet_items=[
            ("Upright Bonus", "$r_{up} = +1.0$ if torso $z > 0.22\\text{m}$ (immediate termination if $z < 0.14\\text{m}$)."),
            ("Velocity Tracking", "$r_{fwd} = \\exp(-2.0 \\cdot (v_x - v_{target})^2)$ matching target forward pace."),
            ("Torque Regularizer", "$-0.005 \\cdot ||\\tau||^2$ prevents motor overheating and gear wear.")
        ]
    )
    story.append(card2)
    story.append(PageBreak())

    # =========================================================================
    # MODULE 3: PPO ACTOR-CRITIC
    # =========================================================================
    card3 = build_diagram_card(
        img_filename="ppo_actor_critic.png",
        title="3. PPO: Actor-Critic Architecture",
        subtitle_category="Coach vs Athlete & Clipped Objective",
        accent_color_hex="#d97706",
        desc_paragraphs=[
            "<b>Proximal Policy Optimization:</b> The Actor network $\\pi_\\theta(a|s)$ drives the joints, while the Critic network $V_\\phi(s)$ evaluates performance. The clipped surrogate objective prevents destructive weight updates.",
            "<b>The 12-Year-Old Analogy:</b> The Gymnast (Actor) performs a trick; the Coach (Critic) scores it. PPO stops the Gymnast from making crazy changes that erase past lessons."
        ],
        bullet_items=[
            ("Clipped Envelope", "$L^{CLIP}(\\theta) = \\hat{\\mathbb{E}}_t [\\min(r_t(\\theta)\\hat{A}_t, \\text{clip}(r_t(\\theta), 1-\\epsilon, 1+\\epsilon)\\hat{A}_t)]$, with $\\epsilon=0.2$."),
            ("Advantage Estimation", "GAE $(\\lambda=0.95)$ computes temporal difference score $\\hat{A}_t$ to guide policy gradient."),
            ("Pruned Edge Export", "Critic is discarded post-training; only lightweight Actor is exported to ONNX.")
        ]
    )
    story.append(card3)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 4: CURRICULUM LEARNING
    # =========================================================================
    card4 = build_diagram_card(
        img_filename="curriculum_learning.png",
        title="4. Curriculum & Sim-to-Real Transfer",
        subtitle_category="4-Stage Ladder & Domain Randomization",
        accent_color_hex="#7c3aed",
        desc_paragraphs=[
            "<b>Progressive Training:</b> Locomotion is unlocked across 4 stages (Stand $\\to$ Push Recovery $\\to$ Gait $\\to$ Domain Randomization) to avoid catastrophic policy collapse.",
            "<b>The 12-Year-Old Analogy:</b> First teach a child to stand on two feet. Then teach balance against gentle shoves. Then take a step. Then run on wet grass."
        ],
        bullet_items=[
            ("Stage Progression", "Stage 1 (200k steps) $\\to$ Stage 2 (500k steps) $\\to$ Stage 3 (1.2M steps) $\\to$ Stage 4 (2.5M steps)."),
            ("Domain Randomization", "Perturbs link mass $(\\pm 15\\%)$, ground friction $(\\pm 20\\%)$, and latency $(1\\dots 5\\text{ms})$."),
            ("Hardware Safety Clamp", "<code>torch.clamp(a, -1.0, 1.0)</code> baked in silicon guarantees 0% gear stripping.")
        ]
    )
    story.append(card4)
    story.append(Spacer(1, 8))

    # Summary card at bottom of Page 2
    summary_content = [
        [
            Paragraph("<b>⚡ PHYSICAL AI COMPLETE MASTERCLASS CERTIFICATION</b>", ParagraphStyle('SumH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#0f172a"))),
        ],
        [
            Paragraph(
                "• <b>Hardware (Phase 1):</b> RK3566 onboard compute, 6-DOF IMU, 15 actuators, and battery constraints.<br/>"
                "• <b>Simulation (Phase 2):</b> MuJoCo kinematic trees, collision geoms, autolimits, and 50Hz integration.<br/>"
                "• <b>Control (Phase 3):</b> PPO reinforcement learning, clamped action graphs, and sim-to-real transfer.",
                ParagraphStyle('SumB', parent=styles['Normal'], fontName='Helvetica', fontSize=7.2, leading=9.5, textColor=colors.HexColor("#334155"))
            )
        ]
    ]
    summary_table = Table(summary_content, colWidths=[530])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(summary_table)

    # =========================================================================
    # PAGE 3: KNOWLEDGE CHECK (5 QUESTIONS)
    # =========================================================================
    story.append(PageBreak())

    kc_banner_content = [
        [
            Paragraph("🧠 PHASE 3 KNOWLEDGE CHECK", title_style),
            Paragraph("<b>ASSESSMENT</b>", ParagraphStyle('KcTag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#f59e0b"), alignment=2))
        ],
        [
            Paragraph("Test your understanding of Reinforcement Learning, PPO, and Sim-to-Real transfer.", subtitle_style),
            Paragraph("5 Questions", ParagraphStyle('KcTag2', parent=badge_style, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"), alignment=2))
        ]
    ]
    kc_banner_table = Table(kc_banner_content, colWidths=[420, 110])
    kc_banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('PADDING', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 0),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(kc_banner_table)
    story.append(Spacer(1, 10))

    q_title_style = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#0f172a")
    )
    q_text_style = ParagraphStyle(
        'QText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e293b")
    )
    q_opt_style = ParagraphStyle(
        'QOption',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155")
    )

    def build_question_card(q_num_label, q_topic, q_text, options_data, accent_hex):
        items = []
        for opt_letter, opt_text in options_data:
            item_para = Paragraph(f"<b>{opt_letter}.</b> {opt_text}", q_opt_style)
            items.append(ListItem(item_para, bulletColor=colors.HexColor(accent_hex), leftIndent=12, bulletOffsetY=1))

        list_flowable = ListFlowable(
            items,
            bulletType='bullet',
            start='circle',
            leftIndent=8,
            bulletFontName='Helvetica',
            bulletFontSize=6,
            spaceAfter=0
        )

        card_elements = [
            Table([
                [
                    Paragraph(f"<font color='{accent_hex}'><b>■</b></font> <b>{q_num_label}:</b> {q_topic}", q_title_style),
                    Paragraph(f"<b>MULTIPLE CHOICE</b>", ParagraphStyle('QType', parent=badge_style, fontSize=7, textColor=colors.HexColor(accent_hex), alignment=2))
                ]
            ], colWidths=[390, 120]),
            Spacer(1, 2),
            HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=4, spaceBefore=0),
            Paragraph(q_text, q_text_style),
            Spacer(1, 4),
            list_flowable
        ]

        card_table = Table([[card_elements]], colWidths=[530])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
            ('LINELEFT', (0, 0), (0, -1), 3, colors.HexColor(accent_hex)),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        return card_table

    questions = [
        ("Q1", "Temporal Observation Dimensions", "<b>How many float values make up the Microduck's 4-frame observation tensor?</b>", [
            ("A", "15 floats"),
            ("B", "60 floats (4 historical frames × 15 sensors)"),
            ("C", "1,000 floats")
        ], "#0284c7"),
        ("Q2", "Torque Penalty in Reward Design", "<b>Why must reward functions include a negative torque penalty term (-||τ||²)?</b>", [
            ("A", "To eliminate high-frequency motor shaking and conserve battery energy."),
            ("B", "Because torque does not exist in real robotics."),
            ("C", "To force the robot to walk backwards.")
        ], "#059669"),
        ("Q3", "Actor-Critic Roles", "<b>In Actor-Critic architectures like PPO, what is the specific role of the Critic?</b>", [
            ("A", "It directly sends PWM electrical commands to the motors."),
            ("B", "It acts as the Coach, predicting expected future discounted returns V(s)."),
            ("C", "It regulates the cooling fans on the Rockchip CPU.")
        ], "#d97706"),
        ("Q4", "Silicon Safety Clamping", "<b>Why is torch.clamp(a, -1.0, 1.0) baked directly into the ONNX graph?</b>", [
            ("A", "To mathematically guarantee motor targets never exceed physical limits, preventing gear stripping."),
            ("B", "To reduce the file size of the neural network."),
            ("C", "To activate the RGB camera lens.")
        ], "#7c3aed"),
        ("Q5", "Sim-to-Real Transfer", "<b>What is Domain Randomization during curriculum training?</b>", [
            ("A", "Playing random background music during training."),
            ("B", "Randomly perturbing mass, friction, and latency in simulation so the policy transfers robustly to reality."),
            ("C", "Randomly shutting off power to the computer.")
        ], "#ef4444")
    ]

    for q_lbl, q_top, q_txt, q_opts, q_col in questions:
        story.append(build_question_card(q_lbl, q_top, q_txt, q_opts, q_col))
        story.append(Spacer(1, 6))

    ans_key_style = ParagraphStyle(
        'AnswerKey',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#64748b"),
        alignment=1
    )
    ans_key_content = [
        [
            Paragraph("<b>Answer Key:</b> 1-B, 2-A, 3-B, 4-A, 5-B (1-B: 60 floats; 2-A: Energy/jerk suppression; 3-B: Value Coach; 4-A: Hardware protection; 5-B: Robust physics randomization)", ans_key_style)
        ]
    ]
    ans_key_table = Table(ans_key_content, colWidths=[530])
    ans_key_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(ans_key_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Phase 3 Handout PDF successfully created: {output_path}")

def main():
    print("=" * 60)
    print("📄 Building Phase 3 Handout: The Dog Trainer...")
    print("=" * 60)
    create_handout()
    print("=" * 60)
    print("🎉 Phase 3 Handout complete. PDF ready for viewing.")
    print("=" * 60)


if __name__ == "__main__":
    main()
