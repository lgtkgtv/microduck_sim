#!/usr/bin/env python3
"""
generate_phase6_handout.py
Generates the official "Microduck Physical AI Masterclass - Phase 6: Securing the Swarm"
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
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(PROJECT_ROOT, "images")
PDF_OUTPUT = os.path.join(PROJECT_ROOT, "Phase6_SecuringSwarm_Handout.pdf")
PDF_ALIAS = os.path.join(PROJECT_ROOT, "microduck_phase6_handout.pdf")

REQUIRED_IMAGES = [
    "ota_updates.png",
    "devsecops_pipeline.png",
    "edge_security.png",
    "telemetry_auth.png"
]

def ensure_images():
    missing = [img for img in REQUIRED_IMAGES if not os.path.exists(os.path.join(IMG_DIR, img))]
    if missing:
        print(f"⚠️ Missing Phase 6 images: {missing}. Generating them now...")
        import generate_phase6_images
        generate_phase6_images.main()


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
            self.drawRightString(page_w - margin, page_h - 26, "Phase 6: Securing the Swarm (DevSecOps for Physical AI)")
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
        textColor=colors.HexColor("#10b981")
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
        textColor=colors.HexColor("#059669")
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
            Paragraph("<b>PHASE 6 HANDOUT</b>", ParagraphStyle('Tag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#10b981"), alignment=2))
        ],
        [
            Paragraph("<b>Module 6: Securing the Swarm:</b> OTA Updates (updaterd), MuJoCo CI Gates, Cryptography & Fleet Observability", subtitle_style),
            Paragraph("DevSecOps", ParagraphStyle('Tag2', parent=badge_style, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"), alignment=2))
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
            Paragraph("<b>UPDATES:</b> A/B Atomic (updaterd)", spec_bar_style),
            Paragraph("<b>CI GATE:</b> 1,000 MuJoCo Sims", spec_bar_style),
            Paragraph("<b>CRYPTO:</b> ED25519 + SHA-256", spec_bar_style),
            Paragraph("<b>FLEET:</b> Swarm Observability", spec_bar_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[150, 130, 130, 130])
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
    # MODULE 1: OTA UPDATES
    # =========================================================================
    card1 = build_diagram_card(
        img_filename="ota_updates.png",
        title="1. Atomic OTA Updates & Rollback",
        subtitle_category="A/B Partitioning & Zero-Brick Failsafe",
        accent_color_hex="#0284c7",
        desc_paragraphs=[
            "<b>Over-The-Air Brain Swaps:</b> `updaterd` downloads candidate policies to Slot B while Slot A runs. A 10-second post-update health watchdog automatically rolls back to Slot A if the robot trips.",
            "<b>The 12-Year-Old Analogy:</b> Neo plugging in a Kung Fu data cartridge in The Matrix. If the move has a glitch, the duck immediately snaps back to its safe old reflexes."
        ],
        bullet_items=[
            ("A/B Partitioning", "Guarantees atomic, seamless hot-reloading without interrupting ongoing operations."),
            ("10s Health Watchdog", "Monitors IMU angular acceleration; trips trigger instantaneous fallback to golden slot."),
            ("Zero-Brick Guarantee", "Hardware never gets stuck with a corrupted or non-functional policy file.")
        ]
    )
    story.append(card1)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 2: DEVSECOPS CI/CD PIPELINE
    # =========================================================================
    card2 = build_diagram_card(
        img_filename="devsecops_pipeline.png",
        title="2. Physical AI CI/CD Testing Gates",
        subtitle_category="1,000 Headless MuJoCo Simulation Runs",
        accent_color_hex="#d97706",
        desc_paragraphs=[
            "<b>Automated Physics Gating:</b> On every git commit, GitHub Actions executes 1,000 parallel headless MuJoCo drop tests across friction, mass, and slope variances to verify 100% stability before deployment.",
            "<b>The 12-Year-Old Analogy:</b> A digital gymnastics tryout. The new brain must balance through 1,000 simulated obstacle courses without falling once before touching real motors."
        ],
        bullet_items=[
            ("Physics Test Gate", "Runs 1,000 headless physics seeds on GPU cluster in &lt;15 seconds."),
            ("Torque Spike Audit", "Asserts that peak motor commands never exceed normalized $[-1.0, 1.0]$ bounds."),
            ("Automated Rejection", "Any simulated fall immediately blocks model signing and halts the release pipeline.")
        ]
    )
    story.append(card2)
    story.append(PageBreak())

    # =========================================================================
    # MODULE 3: EDGE SECURITY & CRYPTOGRAPHY
    # =========================================================================
    card3 = build_diagram_card(
        img_filename="edge_security.png",
        title="3. Edge Security & Anti-Tamper",
        subtitle_category="ED25519 Signatures & Root of Trust",
        accent_color_hex="#e11d48",
        desc_paragraphs=[
            "<b>Cryptographic Policy Integrity:</b> Edge robots verify SHA-256 checksums and ED25519 asymmetric signatures. Unsigned or modified ONNX binaries are rejected at the hardware root of trust.",
            "<b>The 12-Year-Old Analogy:</b> A royal wax seal on an official letter. If a sneaky attacker changes even a single number in the brain, the seal breaks and the robot blocks it."
        ],
        bullet_items=[
            ("Asymmetric ED25519", "Public key on Rockchip RK3566 validates private signature generated during CI build."),
            ("Anti-Tamper Lock", "Protects physical robots from rogue WiFi man-in-the-middle model injections."),
            ("Immutable Root", "Read-only boot partitions prevent malware persistence across robot reboots.")
        ]
    )
    story.append(card3)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 4: FLEET OBSERVABILITY & TELEMETRY
    # =========================================================================
    card4 = build_diagram_card(
        img_filename="telemetry_auth.png",
        title="4. Fleet Observability & Diagnostics",
        subtitle_category="Fall-Rates, Latency Jitter & Thermals",
        accent_color_hex="#7c3aed",
        desc_paragraphs=[
            "<b>Real-Time Swarm Health:</b> Operating a fleet of 100+ robots requires streaming latency metrics, IMU tilt distributions, motor temperatures, and fall-rate anomalies to a cloud dashboard.",
            "<b>The 12-Year-Old Analogy:</b> A fitness tracker smartwatch for your robot. If motor #4 gets too warm, the dashboard alerts the technician before the plastic melts."
        ],
        bullet_items=[
            ("Predictive Diagnostics", "Detects mechanical gear friction and battery degradation weeks before failure."),
            ("Swarm Fleet Sync", "Simultaneously updates entire fleets with synchronized policy rollout waves."),
            ("Zero-Trust Mesh", "mTLS encrypted MQTT/gRPC telemetry ensures fleet communication cannot be snooped.")
        ]
    )
    story.append(card4)
    story.append(Spacer(1, 8))

    # Summary card at bottom of Page 2 (MASTERCLASS GRADUATION)
    summary_content = [
        [
            Paragraph("<b>🎓 CONGRATULATIONS! COMPLETE PHYSICAL AI MASTERCLASS GRADUATION</b>", ParagraphStyle('SumH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#0f172a"))),
        ],
        [
            Paragraph(
                "• <b>Full Stack Mastery:</b> Hardware (P1) $\\to$ MuJoCo (P2) $\\to$ PPO RL (P3) $\\to$ ONNX Clamping (P4) $\\to$ Rust Daemons (P5) $\\to$ DevSecOps (P6).<br/>"
                "• <b>Production Ready:</b> You have architected an enterprise-grade, secure, 50Hz real-time robotics deployment pipeline.<br/>"
                "• <b>Next Step:</b> Connect to physical hardware via <code>robotctl</code> and watch the Microduck walk!",
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
            Paragraph("🧠 PHASE 6 KNOWLEDGE CHECK", title_style),
            Paragraph("<b>ASSESSMENT</b>", ParagraphStyle('KcTag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#10b981"), alignment=2))
        ],
        [
            Paragraph("Test your understanding of DevSecOps, OTA Updates, Cryptography, and Fleet Observability.", subtitle_style),
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
        ("Q1", "Atomic A/B Partition Updates", "<b>What is the purpose of an A/B atomic partition update in updaterd?</b>", [
            ("A", "To double the robot's walking speed."),
            ("B", "To safely test a new policy in Slot B with instant auto-rollback to Slot A if the robot trips."),
            ("C", "To install video games on the Rockchip CPU.")
        ], "#0284c7"),
        ("Q2", "Automated Physics CI Gates", "<b>Why must new neural policies pass 1,000 headless MuJoCo simulations in CI?</b>", [
            ("A", "To mathematically guarantee the model does not trip or spike motor torques before touching real hardware."),
            ("B", "Because physical robots do not have batteries."),
            ("C", "To make the simulation render faster in 3D.")
        ], "#d97706"),
        ("Q3", "Cryptographic Model Signatures", "<b>How does cryptographic ED25519 signing protect an edge robot?</b>", [
            ("A", "It prevents the robot from getting wet in the rain."),
            ("B", "It ensures the robot only executes verified neural weights signed by authorized DevOps engineers, blocking rogue models."),
            ("C", "It encrypts the camera lens.")
        ], "#e11d48"),
        ("Q4", "Fleet Observability & Metrics", "<b>Why is real-time telemetry observability critical for a fleet of robots?</b>", [
            ("A", "It tracks motor temperatures, latency jitter, and fall rates to detect mechanical wear before catastrophic failure."),
            ("B", "To broadcast the robot's location to social media."),
            ("C", "It reduces the physical weight of the robot.")
        ], "#7c3aed"),
        ("Q5", "DevSecOps Release Pipeline", "<b>In the 5-stage DevSecOps lifecycle, what happens after automated CI testing passes?</b>", [
            ("A", "The model is immediately deleted."),
            ("B", "The model is cryptographically signed and packaged for secure OTA deployment."),
            ("C", "The robot shuts down permanently.")
        ], "#10b981")
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
            Paragraph("<b>Answer Key:</b> 1-B, 2-A, 3-B, 4-A, 5-B (1-B: Safe A/B rollback; 2-A: Automated physics safety; 3-B: Cryptographic trust; 4-A: Predictive diagnostics; 5-B: Secure OTA release)", ans_key_style)
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
    print(f"✅ Phase 6 Handout PDF successfully created: {output_path}")

    if output_path != PDF_ALIAS:
        import shutil
        shutil.copyfile(output_path, PDF_ALIAS)
        print(f"✅ Created alias copy: {PDF_ALIAS}")


def main():
    print("=" * 60)
    print("📄 Building Phase 6 Handout: Securing the Swarm...")
    print("=" * 60)
    create_handout()
    print("=" * 60)
    print("🎉 Phase 6 Handout complete. PDF ready for viewing.")
    print("=" * 60)


if __name__ == "__main__":
    main()
