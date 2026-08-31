#!/usr/bin/env python3
"""
generate_phase2_handout.py
Generates the official "Microduck Physical AI Masterclass - Phase 2: The Invisible Matrix"
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
PDF_OUTPUT = os.path.join(DOCS_DIR, "Phase2_Matrix_Handout.pdf")

REQUIRED_IMAGES = [
    "kinematic_tree.png",
    "mujoco_geom.png",
    "forward_dynamics.png",
    "mjcf_xml.png"
]

def ensure_images():
    missing = [img for img in REQUIRED_IMAGES if not os.path.exists(os.path.join(IMG_DIR, img))]
    if missing:
        print(f"⚠️ Missing Phase 2 images: {missing}. Generating them now...")
        import generate_phase2_images
        generate_phase2_images.main()


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
            self.drawRightString(page_w - margin, page_h - 26, "Phase 2: The Invisible Matrix — MuJoCo & MJCF")
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
        textColor=colors.HexColor("#00f0ff")
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
        textColor=colors.HexColor("#0284c7")
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
            Paragraph("<b>PHASE 2 HANDOUT</b>", ParagraphStyle('Tag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#00f0ff"), alignment=2))
        ],
        [
            Paragraph("<b>Module 2: The Invisible Matrix:</b> Kinematic Trees, Collision Geoms, Forward Dynamics & MJCF", subtitle_style),
            Paragraph("MuJoCo Physics", ParagraphStyle('Tag2', parent=badge_style, fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"), alignment=2))
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
            Paragraph("<b>ENGINE:</b> MuJoCo 3.x", spec_bar_style),
            Paragraph("<b>INTEGRATOR:</b> mj_step() @ 50Hz", spec_bar_style),
            Paragraph("<b>TREE:</b> 15 Joints DAG", spec_bar_style),
            Paragraph("<b>COMPILER:</b> autolimits='true'", spec_bar_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[130, 140, 130, 130])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Helper function for 2-column cards
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
    # MODULE 1: KINEMATIC TREES
    # =========================================================================
    card1 = build_diagram_card(
        img_filename="kinematic_tree.png",
        title="1. Kinematic Trees & DAG Topology",
        subtitle_category="Parent-Child Coordinate Frames",
        accent_color_hex="#0284c7",
        desc_paragraphs=[
            "<b>Hierarchical Transforms:</b> Robot bodies are structured as Directed Acyclic Graphs (DAGs). Rotations at parent joints (hip) automatically propagate through child links (knee, foot).",
            "<b>The 12-Year-Old Analogy:</b> When you swing your shoulder, your elbow and hand move along automatically because they are attached children in the tree."
        ],
        bullet_items=[
            ("Base Link Origin", "Root floating base (<code>base_link</code>) has 6 unactuated DOFs (position + quaternion)."),
            ("Joint Articulations", "15 1-DOF revolute joints defined in radians relative to parent link frames."),
            ("End Effectors", "Feet contact positions computed via recursive forward kinematics chain.")
        ]
    )
    story.append(card1)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 2: COLLISION & GEOMS
    # =========================================================================
    card2 = build_diagram_card(
        img_filename="mujoco_geom.png",
        title="2. Collision & Mass (Geoms)",
        subtitle_category="Bounding Volumes & Contact Solvers",
        accent_color_hex="#059669",
        desc_paragraphs=[
            "<b>Fast Collision Primitives:</b> Physics engines do not collide 50k-triangle visual meshes. Instead, Geoms encapsulate bodies in convex primitives (capsules, boxes, spheres).",
            "<b>The 12-Year-Old Analogy:</b> Instead of calculating every feather on a duck, the computer wraps the foot in a smooth rubber box that bounces cleanly off the floor."
        ],
        bullet_items=[
            ("Contact Dynamics", "Soft constraint solver (<code>solref</code>) avoids numerical stiffness spikes on foot strike."),
            ("Friction Cones", "Tangential friction $\\mu=0.8$ prevents foot slippage during dynamic walking push-off."),
            ("Inertia Tensors", "3×3 rotational inertia matrices derived from primitive bounding volumes.")
        ]
    )
    story.append(card2)
    story.append(PageBreak())

    # =========================================================================
    # MODULE 3: FORWARD DYNAMICS
    # =========================================================================
    card3 = build_diagram_card(
        img_filename="forward_dynamics.png",
        title="3. Forward Dynamics: mj_step()",
        subtitle_category="Equations of Motion & 50Hz Loop",
        accent_color_hex="#d97706",
        desc_paragraphs=[
            "<b>Equations of Motion:</b> Resolves $M(q)\\ddot{q} + c(q,v) = \\tau + J^T f$ to calculate joint accelerations $\\ddot{q}$ from motor torques, gravity, and ground reaction forces.",
            "<b>The 12-Year-Old Analogy:</b> A math engine solving 50 physics puzzles a second to calculate where momentum throws the duck after each step."
        ],
        bullet_items=[
            ("50Hz Heartbeat", "Executes with fixed $\\Delta t = 0.020\\text{s}$ cadence matching real robotd kernel."),
            ("State Evolution", "Integrates accelerations to update joint velocities $v(t+\\Delta t)$ and positions $q(t+\\Delta t)$."),
            ("Computational Efficiency", "MuJoCo executes full 15-DOF dynamics in &lt;0.35ms per step.")
        ]
    )
    story.append(card3)
    story.append(Spacer(1, 8))

    # =========================================================================
    # MODULE 4: MJCF XML WRAPPER
    # =========================================================================
    card4 = build_diagram_card(
        img_filename="mjcf_xml.png",
        title="4. MJCF Wrapper Architecture",
        subtitle_category="Dynamic URDF Import & Motor Injection",
        accent_color_hex="#7c3aed",
        desc_paragraphs=[
            "<b>The Wrapper Pattern:</b> Vendor URDFs lack motor definitions and physics tuning. The MJCF Wrapper dynamically imports the URDF and injects 15 actuators and safety bounds.",
            "<b>The 12-Year-Old Analogy:</b> Downloading a toy car 3D model and dropping a real electric motor and battery inside its chassis."
        ],
        bullet_items=[
            ("autolimits='true'", "Infers missing link inertias from mesh volumes, preventing zero-mass divide-by-zero crashes."),
            ("Actuator Injection", "Adds 15 <code>&lt;motor&gt;</code> tags bounded with <code>ctrlrange='-1.0 1.0'</code>."),
            ("Unified Compilation", "<code>mujoco.mj_saveLastXML()</code> dumps merged, fully optimized model to disk.")
        ]
    )
    story.append(card4)
    story.append(Spacer(1, 8))

    # Summary card at bottom of Page 2
    summary_content = [
        [
            Paragraph("<b>⚡ PHASE 2 PHYSICS SUMMARY & REINFORCEMENT LEARNING HANDOFF</b>", ParagraphStyle('SumH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#0f172a"))),
        ],
        [
            Paragraph(
                "• <b>MjModel vs MjData:</b> Static blueprint defines constraints; live state tracks positions and momentum.<br/>"
                "• <b>Hardware Safety:</b> Geoms and solref parameters ensure accurate ground contacts without simulation exploding.<br/>"
                "• <b>Ready for Training:</b> With the virtual duck compiled, proceed to Phase 3: The Dog Trainer (PPO).",
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
            Paragraph("🧠 PHASE 2 KNOWLEDGE CHECK", title_style),
            Paragraph("<b>ASSESSMENT</b>", ParagraphStyle('KcTag', parent=badge_style, fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#00f0ff"), alignment=2))
        ],
        [
            Paragraph("Test your understanding of the MuJoCo physics matrix before training reinforcement learning policies.", subtitle_style),
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
        ("Q1", "Physics Blueprint vs Live State", "<b>What is the key operational difference between MjModel and MjData?</b>", [
            ("A", "MjModel changes dynamically while MjData is frozen."),
            ("B", "MjModel is the static physics blueprint; MjData holds the live state (qpos, qvel)."),
            ("C", "MjData only stores camera images.")
        ], "#0284c7"),
        ("Q2", "Collision Geometry Efficiency", "<b>Why do physics engines use Geoms (capsules/boxes) instead of high-poly 3D meshes for contacts?</b>", [
            ("A", "Bounding shapes make contact and friction math over 100x faster."),
            ("B", "Meshes cannot have color in MuJoCo."),
            ("C", "Geoms prevent gravity from affecting the robot.")
        ], "#059669"),
        ("Q3", "Forward Dynamics Step", "<b>What occurs when calling mujoco.mj_step(model, data)?</b>", [
            ("A", "It reboots the Linux operating system."),
            ("B", "It calculates forces, accelerations, and integrates time forward by one Δt step."),
            ("C", "It automatically converts Python code to C++.")
        ], "#d97706"),
        ("Q4", "The Wrapper Pattern", "<b>Why do we use an MJCF Wrapper instead of directly editing the vendor URDF?</b>", [
            ("A", "It injects 15 motors and physics rules without modifying the vendor's source file."),
            ("B", "URDF files cannot be read by Python."),
            ("C", "It reduces the robot's physical weight by 50%.")
        ], "#7c3aed"),
        ("Q5", "Autolimits & Mass Singularities", "<b>What happens if autolimits='true' is omitted when a vendor link has mass=0.0?</b>", [
            ("A", "The robot moves normally."),
            ("B", "Division by zero occurs and the simulation explodes with NaN velocity."),
            ("C", "The battery recharges instantly.")
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
            Paragraph("<b>Answer Key:</b> 1-B, 2-A, 3-B, 4-A, 5-B (1-B: Blueprint vs State; 2-A: Contact speed; 3-B: Force integration; 4-A: Motor injection; 5-B: Zero-mass NaN crash)", ans_key_style)
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
    print(f"✅ Phase 2 Handout PDF successfully created: {output_path}")

def main():
    print("=" * 60)
    print("📄 Building Phase 2 Handout: The Invisible Matrix...")
    print("=" * 60)
    create_handout()
    print("=" * 60)
    print("🎉 Phase 2 Handout complete. PDF ready for viewing.")
    print("=" * 60)


if __name__ == "__main__":
    main()
