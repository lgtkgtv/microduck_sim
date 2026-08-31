#!/usr/bin/env python3
"""
generate_phase5_handout.py
Generates the official "Microduck Physical AI Masterclass - Phase 5: The Nervous System"
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
PDF_OUTPUT = os.path.join(DOCS_DIR, "Phase5_NervousSystem_Handout.pdf")

REQUIRED_IMAGES = [
    "rust_memory.png",
    "robotd_daemon.png",
    "robotctl_cli.png",
    "config_daemon.png"
]

def ensure_images():
    missing = [img for img in REQUIRED_IMAGES if not os.path.exists(os.path.join(IMG_DIR, img))]
    if missing:
        print(f"⚠️ Missing Phase 5 images: {missing}. Generating them now...")
        import generate_phase5_images
        generate_phase5_images.main()


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
            self.drawRightString(page_w - margin, page_h - 26, "Phase 5: The Nervous System (Rust on RK3566)")
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
            Paragraph("<b>PHASE 5 HANDOUT</b>", ParagraphStyle('Tag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#f59e0b"), alignment=2))
        ],
        [
            Paragraph("<b>Module 5: The Nervous System:</b> Rust Daemons (robotd), IPC Sockets (robotctl) & Calibration (configd)", subtitle_style),
            Paragraph("Embedded Rust", ParagraphStyle('Tag2', parent=badge_style, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"), alignment=2))
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
            Paragraph("<b>LANGUAGE:</b> Rust 2021 Edition", spec_bar_style),
            Paragraph("<b>DAEMON:</b> robotd @ 50Hz", spec_bar_style),
            Paragraph("<b>IPC:</b> Unix Domain Sockets", spec_bar_style),
            Paragraph("<b>HARDWARE:</b> Rockchip RK3566", spec_bar_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[140, 130, 140, 120])
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
    # MODULE 1: RUST MEMORY SAFETY
    # =========================================================================
    card1 = build_diagram_card(
        img_filename="rust_memory.png",
        title="1. Rust Memory Safety on Silicon",
        subtitle_category="Compile-Time Guarantees & 0ms GC",
        accent_color_hex="#d97706",
        desc_paragraphs=[
            "<b>Eliminating Segfaults:</b> Embedded micro-controllers cannot tolerate Garbage Collection (GC) pauses or data races on `/dev/imu`. Rust enforces strict ownership and borrow checking at compile time.",
            "<b>The 12-Year-Old Analogy:</b> In a library, only one student can check out a book at a time. The borrow checker ensures two motors never fight over the same wire."
        ],
        bullet_items=[
            ("Zero Runtime GC", "Deterministic microsecond execution without unpredictable garbage collector latency."),
            ("Data-Race Free", "Compile-time `Send` and `Sync` traits prevent concurrent memory corruption."),
            ("Memory Footprint", "Compiled standalone binary consumes &lt;8MB RAM on the Rockchip RK3566.")
        ]
    )
    story.append(card1)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 2: ROBOTD DAEMON
    # =========================================================================
    card2 = build_diagram_card(
        img_filename="robotd_daemon.png",
        title="2. The robotd Spinal Cord Daemon",
        subtitle_category="50Hz Real-Time Sensor-Actuator Loop",
        accent_color_hex="#0284c7",
        desc_paragraphs=[
            "<b>The Real-Time Engine:</b> Running under Linux `SCHED_FIFO` real-time scheduling priority, `robotd` polls the IMU at 200Hz, executes ONNX inference, and commands 15 PWM motors every 20ms.",
            "<b>The 12-Year-Old Analogy:</b> When the doctor taps your knee, your spinal cord kicks your leg before your brain even notices. `robotd` handles these lightning-fast reflexes."
        ],
        bullet_items=[
            ("Strict 20ms Loop", "Kernel timer precision within ±0.08ms jitter, preventing motor torque stutter."),
            ("Bus Interfaces", "High-speed UART/I2C communication polling 15 joint encoders concurrently."),
            ("Hardware Watchdog", "Auto-failsafe system powers down motor PWM lines if telemetry times out.")
        ]
    )
    story.append(card2)
    story.append(PageBreak())

    # =========================================================================
    # MODULE 3: ROBOTCTL CLI
    # =========================================================================
    card3 = build_diagram_card(
        img_filename="robotctl_cli.png",
        title="3. The robotctl CLI & Unix Sockets",
        subtitle_category="Non-Blocking Local IPC Sockets",
        accent_color_hex="#7c3aed",
        desc_paragraphs=[
            "<b>Zero-Disruption Observability:</b> Developers monitor telemetry, hot-swap walking policies, and trigger emergency stops via `robotctl` over a Unix domain socket (`/var/run/robotd.sock`).",
            "<b>The 12-Year-Old Analogy:</b> Slipping a written note under a classroom door without making the teacher pause the lecture."
        ],
        bullet_items=[
            ("Zero-Copy IPC", "Non-blocking Unix sockets query live joint states in &lt;0.1ms without stalling 50Hz loop."),
            ("Policy Hot-Reload", "Commands `robotctl update <model.onnx>` seamlessly replace policy weights in RAM."),
            ("Emergency E-Stop", "`robotctl stop --estop` immediately zeroes torque across all 15 actuators.")
        ]
    )
    story.append(card3)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 4: CONFIG DAEMON
    # =========================================================================
    card4 = build_diagram_card(
        img_filename="config_daemon.png",
        title="4. Configuration & Calibration (configd)",
        subtitle_category="Joint Zero Offsets & Hardware Tuning",
        accent_color_hex="#059669",
        desc_paragraphs=[
            "<b>Compensating 3D-Print Slop:</b> Physical tolerances cause slight joint misalignments. `configd` loads joint offsets $\\delta$ from `/etc/microduck/calibration.json` to achieve true neutral zero.",
            "<b>The 12-Year-Old Analogy:</b> If your new bicycle handlebars are slightly crooked from the factory, you adjust the screw so it drives perfectly straight."
        ],
        bullet_items=[
            ("Offset Calibration", "Applies $q_{calibrated} = q_{raw} + \\delta$ before passing sensor telemetry to ONNX."),
            ("Persistent EEPROM", "Stores zero-positions, PID velocity gains, and temperature thresholds permanently."),
            ("Fleet Uniformity", "Ensures a single ONNX walking policy transfers identically across 100 robots.")
        ]
    )
    story.append(card4)
    story.append(Spacer(1, 8))

    # Summary card at bottom of Page 2
    summary_content = [
        [
            Paragraph("<b>⚡ PHASE 5 EMBEDDED SYSTEM SUMMARY & FLEET DEPLOYMENT</b>", ParagraphStyle('SumH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#0f172a"))),
        ],
        [
            Paragraph(
                "• <b>Rust Daemons:</b> `robotd` and `configd` guarantee crash-proof, real-time 50Hz execution.<br/>"
                "• <b>Hardware Control:</b> `robotctl` empowers seamless live monitoring and emergency failsafes.<br/>"
                "• <b>Curriculum Final Phase:</b> Proceed to Phase 6: Securing the Swarm (OTA Updates & DevSecOps).",
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
            Paragraph("🧠 PHASE 5 KNOWLEDGE CHECK", title_style),
            Paragraph("<b>ASSESSMENT</b>", ParagraphStyle('KcTag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#f59e0b"), alignment=2))
        ],
        [
            Paragraph("Test your understanding of Rust Memory Safety, robotd, robotctl, and configd calibration.", subtitle_style),
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
        ("Q1", "Rust Memory Guarantees", "<b>Why is Rust's zero-cost ownership model essential for the 50Hz control loop?</b>", [
            ("A", "Rust makes the battery output infinite electricity."),
            ("B", "It prevents data races and memory leaks at compile-time with zero Garbage Collection pauses."),
            ("C", "Rust only compiles on quantum computers.")
        ], "#0284c7"),
        ("Q2", "robotd Daemon Function", "<b>What is the primary operational role of the robotd daemon?</b>", [
            ("A", "It serves as the 50Hz spinal cord, polling IMU/encoders, running ONNX inference, and firing motors."),
            ("B", "It renders video game graphics for the user."),
            ("C", "It streams music to the robot's speakers.")
        ], "#059669"),
        ("Q3", "Unix Domain Socket IPC", "<b>Why does robotctl interact with robotd via a Unix domain socket (/var/run/robotd.sock)?</b>", [
            ("A", "Because internet cables are forbidden in robotics."),
            ("B", "It enables non-blocking local communication without stalling the real-time balance loop."),
            ("C", "To increase CPU temperature.")
        ], "#d97706"),
        ("Q4", "configd Hardware Calibration", "<b>What problem does configd solve on physical 3D-printed robots?</b>", [
            ("A", "It applies joint zero-offsets to calibrate mechanical manufacturing imperfections."),
            ("B", "It changes the color of the robot's plastic parts."),
            ("C", "It deletes the ONNX model when the robot trips.")
        ], "#7c3aed"),
        ("Q5", "Emergency Stop Command", "<b>What CLI command immediately cuts power to all 15 motors in an emergency?</b>", [
            ("A", "robotctl sleep"),
            ("B", "robotctl stop --estop (or robotctl estop)"),
            ("C", "robotctl reboot")
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
            Paragraph("<b>Answer Key:</b> 1-B, 2-A, 3-B, 4-A, 5-B (1-B: Zero GC pauses; 2-A: 50Hz spinal loop; 3-B: Non-blocking IPC; 4-A: Joint offset calibration; 5-B: Immediate E-Stop)", ans_key_style)
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
    print(f"✅ Phase 5 Handout PDF successfully created: {output_path}")

def main():
    print("=" * 60)
    print("📄 Building Phase 5 Handout: The Nervous System...")
    print("=" * 60)
    create_handout()
    print("=" * 60)
    print("🎉 Phase 5 Handout complete. PDF ready for viewing.")
    print("=" * 60)


if __name__ == "__main__":
    main()
