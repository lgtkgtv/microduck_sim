#!/usr/bin/env python3
"""
generate_handout.py
Generates the official "Microduck Physical AI Masterclass - Phase 1: Hardware Anatomy"
handout using the 'Diagram Method', embedding 6 technical Pillow diagrams next to
their descriptive engineering and pedagogical text.
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
PDF_OUTPUT = os.path.join(DOCS_DIR, "Phase1_Anatomy_Handout.pdf")

REQUIRED_IMAGES = [
    "rockchip_rk3566.png",
    "imu_sensor.png",
    "dof_motors.png",
    "lidar_radar.png",
    "rgb_camera.png",
    "battery_drain.png"
]

def ensure_images():
    missing = [img for img in REQUIRED_IMAGES if not os.path.exists(os.path.join(IMG_DIR, img))]
    if missing:
        print(f"⚠️ Missing images detected: {missing}. Generating them now...")
        import generate_images
        generate_images.main()



class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page numbers ('Page X of Y')
    along with running header and footer banners.
    """
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
        margin = 36  # 0.5 inch

        # Running Header (Pages 2+)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(margin, page_h - 26, "🦆 MICRODUCK PHYSICAL AI MASTERCLASS")
            self.setFont("Helvetica", 8)
            self.drawRightString(page_w - margin, page_h - 26, "Phase 1: Hardware Architecture & Control Handout")
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

    # Custom styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#ffffff"),
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#94a3b8"),
        alignment=0
    )

    spec_bar_style = ParagraphStyle(
        'SpecBar',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#38bdf8")
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0f172a")
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0284c7")
    )

    body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )

    bullet_style = ParagraphStyle(
        'CardBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )

    code_style = ParagraphStyle(
        'CardCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0369a1")
    )

    story = []

    # =========================================================================
    # HEADER BANNER (Page 1 Top)
    # =========================================================================
    banner_content = [
        [
            Paragraph("🦆 MICRODUCK PHYSICAL AI MASTERCLASS", title_style),
            Paragraph("<b>PHASE 1 HANDOUT</b>", ParagraphStyle('Tag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#f59e0b"), alignment=2))
        ],
        [
            Paragraph("<b>Module 1 Hardware Architecture:</b> Sensor-Actuator Stack, 50Hz Real-Time Loop, & Silicon Constraints", subtitle_style),
            Paragraph("MuJoCo + ONNX", ParagraphStyle('Tag2', parent=badge_style, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"), alignment=2))
        ]
    ]
    banner_table = Table(banner_content, colWidths=[420, 110])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('PADDING', (0, 0), (-1, -1), 10),
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
            Paragraph("<b>COMPUTE:</b> Rockchip RK3566", spec_bar_style),
            Paragraph("<b>CADENCE:</b> 50 Hz (20ms / step)", spec_bar_style),
            Paragraph("<b>DEGREES OF FREEDOM:</b> 15 Actuators", spec_bar_style),
            Paragraph("<b>AI STACK:</b> PyTorch PPO → ONNX", spec_bar_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[132, 132, 138, 128])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # HELPER: BUILD DIAGRAM METHOD CARD
    # =========================================================================
    def build_diagram_card(img_filename, title, subtitle_category, accent_color_hex, desc_paragraphs, bullet_items):
        img_path = os.path.join(IMG_DIR, img_filename)
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Missing diagram image: {img_path}")

        # Image flowable: width=200pt, height=150pt (exact 4:3 aspect ratio)
        img_flowable = Image(img_path, width=195, height=146.25)

        # Right-side text flowable list
        text_elements = []
        
        # Header + Badge
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
        text_elements.append(Spacer(1, 4))
        text_elements.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#e2e8f0"), spaceAfter=5, spaceBefore=0))

        # Descriptive Paragraphs
        for p in desc_paragraphs:
            text_elements.append(Paragraph(p, body_style))
            text_elements.append(Spacer(1, 3))

        # Bullet Specifications
        if bullet_items:
            for b_lbl, b_val in bullet_items:
                bullet_text = f"• <b>{b_lbl}</b>: {b_val}"
                text_elements.append(Paragraph(bullet_text, bullet_style))
                text_elements.append(Spacer(1, 1.5))

        # Wrap in a 2-Column Table Card
        card_table = Table(
            [[img_flowable, text_elements]],
            colWidths=[200, 330]
        )
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ('LINELEFT', (0, 0), (0, -1), 3.5, colors.HexColor(accent_color_hex)),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ]))
        return card_table

    # =========================================================================
    # MODULE 1: ROCKCHIP RK3566
    # =========================================================================
    card1 = build_diagram_card(
        img_filename="rockchip_rk3566.png",
        title="1. The Brain: Rockchip RK3566",
        subtitle_category="Onboard Compute & Real-Time Kernel",
        accent_color_hex="#0284c7",
        desc_paragraphs=[
            "<b>The Core Engine:</b> A quad-core ARM Cortex-A55 @ 1.8GHz with an integrated 0.8 TOPS NPU running an optimized Linux OS. It serves as the physical robot's central nervous system.",
            "<b>The 12-Year-Old Analogy:</b> Like an orchestra conductor who doesn't play the instruments but cues 15 musicians exactly 50 times every single second."
        ],
        bullet_items=[
            ("50Hz Control Cadence", "Strict 20ms execution loop managed by real-time daemon (<code>robotd</code>)."),
            ("Interface Peripherals", "MIPI-CSI2 camera, high-speed UART IMU, CAN/PWM motor buses."),
            ("Edge Inference", "Executes pruned ONNX Actor graph with &lt;2.8ms latency per step.")
        ]
    )
    story.append(card1)
    story.append(Spacer(1, 10))

    # =========================================================================
    # MODULE 2: IMU SENSOR
    # =========================================================================
    card2 = build_diagram_card(
        img_filename="imu_sensor.png",
        title="2. The Inner Ear: 6-DOF IMU Sensor",
        subtitle_category="Inertial Navigation & Gravity Vector",
        accent_color_hex="#059669",
        desc_paragraphs=[
            "<b>The Vestibular Sense:</b> Combines a 3-axis accelerometer and 3-axis gyroscope to track Pitch (θ), Roll (φ), and Yaw (ψ) along with dynamic gravity vectors.",
            "<b>The 12-Year-Old Analogy:</b> Close your eyes and stand on one leg. Your inner ear tells you instantly if you are tilting before your eyes even notice."
        ],
        bullet_items=[
            ("Observation Window", "Fixed sliding buffer of 4 frames × 15 sensors = 60 float telemetry tensor."),
            ("Sensor Fusion", "Real-time Madgwick / Extended Kalman Filter running at 200Hz internal rate."),
            ("RL Input", "Normalizes angular velocity [ωx, ωy, ωz] and projected gravity vector [gx, gy, gz].")
        ]
    )
    story.append(card2)
    story.append(PageBreak())

    # =========================================================================
    # MODULE 3: 15-DOF ACTUATORS
    # =========================================================================
    card3 = build_diagram_card(
        img_filename="dof_motors.png",
        title="3. The Muscles: 15-DOF Actuators",
        subtitle_category="Robotic Joints & Action Clamping",
        accent_color_hex="#d97706",
        desc_paragraphs=[
            "<b>High-Torque Articulation:</b> 15 coreless servo motors drive hips, knees, and ankles. The neural network outputs normalized action targets.",
            "<b>The 12-Year-Old Analogy:</b> Muscles have bone stops so your knee can't bend backwards. We clamp the AI math in silicon so it never breaks a joint."
        ],
        bullet_items=[
            ("Action Space", "Strictly bounded <code>a ∈ [-1.0, 1.0]</code> via <code>torch.clamp()</code> in ONNX graph."),
            ("Control Protocol", "High-speed serial bus delivering target velocity and PD torque gains."),
            ("Joint Limits", "Enforced in both URDF/MJCF definitions and firmware safety watchdogs.")
        ]
    )
    story.append(card3)
    story.append(Spacer(1, 10))

    # =========================================================================
    # MODULE 4: 2D LIDAR RADAR
    # =========================================================================
    card4 = build_diagram_card(
        img_filename="lidar_radar.png",
        title="4. The Bat Sonar: 2D LiDAR Scanner",
        subtitle_category="Planar Rangefinding & Spatial SLAM",
        accent_color_hex="#10b981",
        desc_paragraphs=[
            "<b>Time-of-Flight Ranging:</b> Emits 905nm pulsed laser rays at 10Hz, capturing 360° point clouds for real-time obstacle avoidance and hallway navigation.",
            "<b>The 12-Year-Old Analogy:</b> Exactly like a bat navigating a pitch-black cave using ultrasonic clicks, but using light beams that bounce off walls at the speed of light."
        ],
        bullet_items=[
            ("Effective Range", "0.12m to 8.0m with ±15mm distance precision at walking height."),
            ("Spatial Perception", "Generates polar obstacle distance map to modulate locomotion goals."),
            ("Sensor Interface", "Direct DMA UART link feeding 3600 spatial measurement points per second.")
        ]
    )
    story.append(card4)
    story.append(PageBreak())

    # =========================================================================
    # MODULE 5: RGB CAMERA
    # =========================================================================
    card5 = build_diagram_card(
        img_filename="rgb_camera.png",
        title="5. The Visual Cortex: RGB Camera",
        subtitle_category="Optical Sensor & Tensor Processing",
        accent_color_hex="#6366f1",
        desc_paragraphs=[
            "<b>Embodied Vision:</b> Captures raw optical photons through an ultra-wide lens and translates them into an RGB pixel matrix tensor for neural feature extraction.",
            "<b>The 12-Year-Old Analogy:</b> A computer doesn't see a picture; it sees a giant grid of Red, Green, and Blue numbers between 0 and 255."
        ],
        bullet_items=[
            ("Tensor Pipeline", "Preprocessed into <code>[Batch, 3, 224, 224]</code> float tensors normalized to [0.0, 1.0]."),
            ("Hardware Acceleration", "Direct hardware ISP color conversion passing directly into RK3566 NPU."),
            ("Semantic Guidance", "Supplements high-frequency blind proprioception with terrain recognition.")
        ]
    )
    story.append(card5)
    story.append(Spacer(1, 10))

    # =========================================================================
    # MODULE 6: BATTERY CONSTRAINTS
    # =========================================================================
    card6 = build_diagram_card(
        img_filename="battery_drain.png",
        title="6. The Gas Tank: Power & Thermal Dynamics",
        subtitle_category="3S Li-Ion Discharge & Load Budgeting",
        accent_color_hex="#e11d48",
        desc_paragraphs=[
            "<b>Energy Limitations:</b> A 3S 11.1V 2200mAh Lithium-Ion battery powers all 15 actuators. Motor current draw directly determines operating duration.",
            "<b>The 12-Year-Old Analogy:</b> If you sprint as fast as you can, you will collapse in 1 minute. If you jog steadily, you can run for an hour. The AI must budget energy."
        ],
        bullet_items=[
            ("Voltage Thresholds", "12.6V Full Charge → 11.1V Nominal → 9.9V Emergency Low-Voltage Cutoff."),
            ("Gait Efficiency", "Smooth 50Hz policies consume ~3.2A (45 min runtime) vs 15A during erratic thrashing."),
            ("Reward Regularization", "RL training introduces energy penalty term: <code>reward_energy = -c * ||torque||²</code>.")
        ]
    )
    story.append(card6)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SUMMARY FOOTNOTE / NEXT STEPS CARD
    # =========================================================================
    summary_content = [
        [
            Paragraph("<b>⚡ PHYSICAL AI PHASE 1 ARCHITECTURE SUMMARY & NEXT STEPS</b>", ParagraphStyle('SumH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#0f172a"))),
        ],
        [
            Paragraph(
                "• <b>MuJoCo Simulation:</b> Train policy in headless virtual sandbox where falling costs $0.<br/>"
                "• <b>Hardware Clamping:</b> Bake <code>torch.clamp()</code> directly into ONNX graph before exporting to edge.<br/>"
                "• <b>Phase 2 Transition:</b> Proceed to Module 2 Reinforcement Learning with PPO and Gym environments.",
                ParagraphStyle('SumB', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=colors.HexColor("#334155"))
            )
        ]
    ]
    summary_table = Table(summary_content, colWidths=[530])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(summary_table)

    # =========================================================================
    # PAGE 4: KNOWLEDGE CHECK
    # =========================================================================
    story.append(PageBreak())

    # Knowledge Check Header Banner
    kc_banner_content = [
        [
            Paragraph("🧠 KNOWLEDGE CHECK", title_style),
            Paragraph("<b>ASSESSMENT</b>", ParagraphStyle('KcTag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#f59e0b"), alignment=2))
        ],
        [
            Paragraph("Test your understanding of the Microduck hardware before moving to the software layer.", subtitle_style),
            Paragraph("Phase 1 Review", ParagraphStyle('KcTag2', parent=badge_style, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"), alignment=2))
        ]
    ]
    kc_banner_table = Table(kc_banner_content, colWidths=[420, 110])
    kc_banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 0),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(kc_banner_table)
    story.append(Spacer(1, 14))

    # Styles for Questions & Options
    q_title_style = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0f172a")
    )

    q_text_style = ParagraphStyle(
        'QText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    q_opt_style = ParagraphStyle(
        'QOption',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155")
    )

    def build_question_card(q_num_label, q_topic, q_text, options_data, accent_hex):
        items = []
        for opt_letter, opt_text in options_data:
            item_para = Paragraph(f"<b>{opt_letter}.</b> {opt_text}", q_opt_style)
            items.append(ListItem(item_para, bulletColor=colors.HexColor(accent_hex), leftIndent=15, bulletOffsetY=1))

        list_flowable = ListFlowable(
            items,
            bulletType='bullet',
            start='circle',
            leftIndent=10,
            bulletFontName='Helvetica',
            bulletFontSize=7,
            spaceAfter=0
        )

        card_elements = [
            Table([
                [
                    Paragraph(f"<font color='{accent_hex}'><b>■</b></font> <b>{q_num_label}:</b> {q_topic}", q_title_style),
                    Paragraph(f"<b>MULTIPLE CHOICE</b>", ParagraphStyle('QType', parent=badge_style, fontSize=7.5, textColor=colors.HexColor(accent_hex), alignment=2))
                ]
            ], colWidths=[380, 130]),
            Spacer(1, 3),
            HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=6, spaceBefore=0),
            Paragraph(q_text, q_text_style),
            Spacer(1, 6),
            list_flowable
        ]

        card_table = Table([[card_elements]], colWidths=[530])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ('LINELEFT', (0, 0), (0, -1), 3.5, colors.HexColor(accent_hex)),
            ('PADDING', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        return card_table

    # Question 1
    q1_card = build_question_card(
        q_num_label="Q1",
        q_topic="Control Frequency & Cadence",
        q_text="<b>Why does the Rockchip brain need to send motor commands 50 times a second?</b>",
        options_data=[
            ("A", "To keep the battery charged"),
            ("B", "To constantly catch its balance so the duck doesn't fall"),
            ("C", "Because Linux only runs at 50Hz")
        ],
        accent_hex="#0284c7"
    )
    story.append(q1_card)
    story.append(Spacer(1, 12))

    # Question 2
    q2_card = build_question_card(
        q_num_label="Q2",
        q_topic="Actuator Clamping & Protection",
        q_text="<b>What happens if the AI sends a motor command of 2.5 (past the 1.0 limit)?</b>",
        options_data=[
            ("A", "The robot walks faster"),
            ("B", "The IMU takes over"),
            ("C", "The physical motor breaks")
        ],
        accent_hex="#d97706"
    )
    story.append(q2_card)
    story.append(Spacer(1, 12))

    # Question 3
    q3_card = build_question_card(
        q_num_label="Q3",
        q_topic="Sensory Perception in Darkness",
        q_text="<b>If the duck is in a completely dark room, how does it see a wall?</b>",
        options_data=[
            ("A", "RGB Camera night vision"),
            ("B", "LiDAR shoots invisible lasers"),
            ("C", "The inner ear feels it")
        ],
        accent_hex="#10b981"
    )
    story.append(q3_card)
    story.append(Spacer(1, 20))

    # Answer Key at the very bottom
    ans_key_style = ParagraphStyle(
        'AnswerKey',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748b"),
        alignment=1
    )
    ans_key_content = [
        [
            Paragraph("<b>Answer Key:</b> 1-B, 2-C, 3-B", ans_key_style)
        ]
    ]
    ans_key_table = Table(ans_key_content, colWidths=[530])
    ans_key_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(ans_key_table)

    # Build the document with two-pass canvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Handout PDF successfully created: {output_path}")

def main():
    print("=" * 60)
    print("📄 Building Microduck Physical AI Handout (Diagram Method)...")
    print("=" * 60)
    create_handout()
    print("=" * 60)
    print("🎉 All tasks complete. PDF is ready for viewing.")
    print("=" * 60)


if __name__ == "__main__":
    main()
