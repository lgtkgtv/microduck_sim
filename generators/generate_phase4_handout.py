#!/usr/bin/env python3
"""
generate_phase4_handout.py
Generates the official "Microduck Physical AI Masterclass - Phase 4: Brain Surgery & Edge Inference"
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
PDF_OUTPUT = os.path.join(DOCS_DIR, "Phase4_BrainSurgery_Handout.pdf")

REQUIRED_IMAGES = [
    "actor_extraction.png",
    "hardware_clamp.png",
    "onnx_graph.png",
    "temporal_memory.png"
]

def ensure_images():
    missing = [img for img in REQUIRED_IMAGES if not os.path.exists(os.path.join(IMG_DIR, img))]
    if missing:
        print(f"⚠️ Missing Phase 4 images: {missing}. Generating them now...")
        import generate_phase4_images
        generate_phase4_images.main()


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
            self.drawRightString(page_w - margin, page_h - 26, "Phase 4: Brain Surgery & Edge Inference")
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
        textColor=colors.HexColor("#c084fc")
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
        textColor=colors.HexColor("#7c3aed")
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
            Paragraph("<b>PHASE 4 HANDOUT</b>", ParagraphStyle('Tag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#c084fc"), alignment=2))
        ],
        [
            Paragraph("<b>Module 4: Brain Surgery:</b> Actor Isolation, Hardware Clamps, ONNX Export & Temporal Memory", subtitle_style),
            Paragraph("Edge Inference", ParagraphStyle('Tag2', parent=badge_style, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"), alignment=2))
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
            Paragraph("<b>PRUNED SIZE:</b> 35 KB (99.8% Drop)", spec_bar_style),
            Paragraph("<b>INFERENCE:</b> 2.5ms on RK3566", spec_bar_style),
            Paragraph("<b>SAFETY:</b> torch.clamp()", spec_bar_style),
            Paragraph("<b>BUFFER:</b> deque(maxlen=4)", spec_bar_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[140, 130, 130, 130])
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
    # MODULE 1: ACTOR EXTRACTION
    # =========================================================================
    card1 = build_diagram_card(
        img_filename="actor_extraction.png",
        title="1. Surgical Actor Extraction",
        subtitle_category="Reflex Isolation & 99.8% Pruning",
        accent_color_hex="#0284c7",
        desc_paragraphs=[
            "<b>Pruning Training Overhead:</b> The 24MB PyTorch checkpoint contains the Critic value network $V_\\phi(s)$, Adam optimizer state, and backward autograd graphs. We extract only the 35KB forward Actor $\\pi_\\theta(a|s)$.",
            "<b>The 12-Year-Old Analogy:</b> When you take a piano exam, your teacher doesn't sit on your lap. You leave the teacher at home and only bring your muscle memory."
        ],
        bullet_items=[
            ("Actor Model", "Extracts deterministic mean $\\mu(s)$ policy graph for direct joint actuation."),
            ("Weight Freezing", "Discards gradient tracking (`requires_grad=False`), eliminating dynamic memory allocations."),
            ("Silicon Size", "Reduces model footprint from 24,000 KB down to a lightweight 35 KB binary.")
        ]
    )
    story.append(card1)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 2: HARDWARE SAFETY CLAMPING
    # =========================================================================
    card2 = build_diagram_card(
        img_filename="hardware_clamp.png",
        title="2. Hardware Safety Clamping in Silicon",
        subtitle_category="torch.clamp() Bounds & Gear Protection",
        accent_color_hex="#059669",
        desc_paragraphs=[
            "<b>Mathematical Inviolability:</b> Unbounded neural outputs ($>1.0$) can strip physical nylon servo gears. By baking `torch.clamp(a, -1.0, 1.0)` into the computational graph, motor safety is guaranteed in silicon.",
            "<b>The 12-Year-Old Analogy:</b> Bumper rails on a bowling lane that physically prevent the ball from bouncing into the next lane, no matter how hard you throw it."
        ],
        bullet_items=[
            ("Silicon Clamping", "Compiled as a native ONNX `Clip` operator executed directly on the NPU."),
            ("Range Guarantee", "Outputs are mathematically bounded to $[-1.0, 1.0]$ before reaching the PWM bus."),
            ("Failsafe Redundancy", "Prevents runaway policy gradients from destroying $399 physical hardware.")
        ]
    )
    story.append(card2)
    story.append(PageBreak())

    # =========================================================================
    # MODULE 3: ONNX COMPUTATIONAL GRAPH
    # =========================================================================
    card3 = build_diagram_card(
        img_filename="onnx_graph.png",
        title="3. ONNX Computational Graph",
        subtitle_category="Cross-Platform IR & 2.5ms Execution",
        accent_color_hex="#d97706",
        desc_paragraphs=[
            "<b>Standardized Tensor Graph:</b> Compiles PyTorch weights into an ONNX Opset 17 computational DAG (Gemm $\\to$ ReLU $\\to$ Clip), executable via `onnxruntime` across any CPU/NPU hardware without Python.",
            "<b>The 12-Year-Old Analogy:</b> Translating an English recipe into universal cooking symbols that any chef in any country can read and execute instantly."
        ],
        bullet_items=[
            ("Execution Speed", "Runs full 60-float inference in &lt;2.5ms on Rockchip RK3566 quad-core ARM."),
            ("Deterministic Pipeline", "Eliminates Python Global Interpreter Lock (GIL) and runtime garbage collection."),
            ("Opset 17 Standard", "Portable representation deployable across C++, Rust, or embedded Linux kernels.")
        ]
    )
    story.append(card3)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 4: TEMPORAL MEMORY
    # =========================================================================
    card4 = build_diagram_card(
        img_filename="temporal_memory.png",
        title="4. Temporal Memory & Sliding Buffer",
        subtitle_category="Fixed deque(maxlen=4) vs Token Explosion",
        accent_color_hex="#7c3aed",
        desc_paragraphs=[
            "<b>Fixed Memory Horizon:</b> Balancing requires velocity and acceleration awareness. A fixed sliding window `deque(maxlen=4)` buffers 4 frames $\\times$ 15 sensors = 60 floats with constant $O(1)$ memory.",
            "<b>The 12-Year-Old Analogy:</b> Unlike ChatGPT which grows huge and slower the more you talk, the duck's memory is a 4-frame conveyor belt where old frames quietly drop off."
        ],
        bullet_items=[
            ("Constant O(1) Memory", "Prevents LLM-style $O(N^2)$ quadratic token memory growth and latency spikes."),
            ("State Dimensions", "Produces flat $[1, 60]$ input tensor capturing instantaneous joint momentum."),
            ("Strict 50Hz Budget", "2.5ms inference + 17.5ms cadence sleep = perfectly steady 20.0ms heartbeat.")
        ]
    )
    story.append(card4)
    story.append(Spacer(1, 8))

    # Summary card at bottom of Page 2
    summary_content = [
        [
            Paragraph("<b>⚡ PHASE 4 SILICON DEPLOYMENT SUMMARY & RUST DAEMON HANDOFF</b>", ParagraphStyle('SumH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#0f172a"))),
        ],
        [
            Paragraph(
                "• <b>Reflex Model:</b> Extracted 35KB ONNX policy containing pure clamped walking muscle memory.<br/>"
                "• <b>Real-Time Cadence:</b> Predictable 2.5ms inference guarantees zero timing jitter on edge hardware.<br/>"
                "• <b>Next Module:</b> Deploy the ONNX binary into Phase 5: The Rust Nervous System (`robotd` & `robotctl`).",
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
            Paragraph("🧠 PHASE 4 KNOWLEDGE CHECK", title_style),
            Paragraph("<b>ASSESSMENT</b>", ParagraphStyle('KcTag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#c084fc"), alignment=2))
        ],
        [
            Paragraph("Test your understanding of Model Extraction, Clamping, ONNX Compilation, and Temporal Memory.", subtitle_style),
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
        ("Q1", "Actor Policy Extraction", "<b>Why do we extract only the Actor network and discard the Critic?</b>", [
            ("A", "Because the Critic is written in a different programming language."),
            ("B", "The Critic is only needed to score actions during training; the Actor contains all walking reflexes."),
            ("C", "The Critic network causes the robot to walk backwards.")
        ], "#0284c7"),
        ("Q2", "Silicon Clamping Protection", "<b>What is the primary danger of deploying an ONNX policy without torch.clamp()?</b>", [
            ("A", "Runaway neural outputs (>1.0) can command excessive speed, stripping physical gears."),
            ("B", "The robot's battery will charge too quickly."),
            ("C", "The WiFi antenna will disconnect.")
        ], "#059669"),
        ("Q3", "ONNX Edge Execution", "<b>What is the advantage of compiling PyTorch models to ONNX for edge robotics?</b>", [
            ("A", "ONNX allows the robot to fly."),
            ("B", "ONNX represents pure math graphs, executing in <2.5ms without heavy Python overhead."),
            ("C", "ONNX turns the camera into an IMU.")
        ], "#d97706"),
        ("Q4", "50Hz Timing Discipline", "<b>Why does our 50Hz control loop explicitly sleep for 17.5ms after a 2.5ms inference?</b>", [
            ("A", "To maintain a perfectly steady 20ms heartbeat and prevent motor timing jitter."),
            ("B", "To allow the CPU to cool down to 0 degrees."),
            ("C", "Because Linux cannot run for more than 3ms.")
        ], "#7c3aed"),
        ("Q5", "Sliding Temporal Memory", "<b>Why does deque(maxlen=4) avoid the 'token explosion' problem of LLMs?</b>", [
            ("A", "It deletes the robot's brain every second."),
            ("B", "It holds a fixed 60-float buffer, ensuring constant O(1) memory and predictable 2.5ms latency."),
            ("C", "It compresses video into text files.")
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
            Paragraph("<b>Answer Key:</b> 1-B, 2-A, 3-B, 4-A, 5-B (1-B: Actor reflexes; 2-A: Gear strip prevention; 3-B: Fast math graph; 4-A: Precise 20ms cadence; 5-B: Constant O(1) buffer)", ans_key_style)
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
    print(f"✅ Phase 4 Handout PDF successfully created: {output_path}")

    if output_path != PDF_ALIAS:
        import shutil
        shutil.copyfile(output_path, PDF_ALIAS)
        print(f"✅ Created alias copy: {PDF_ALIAS}")


def main():
    print("=" * 60)
    print("📄 Building Phase 4 Handout: Brain Surgery & Edge Inference...")
    print("=" * 60)
    create_handout()
    print("=" * 60)
    print("🎉 Phase 4 Handout complete. PDF ready for viewing.")
    print("=" * 60)


if __name__ == "__main__":
    main()
