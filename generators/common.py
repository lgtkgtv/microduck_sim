"""
common.py - Shared styling, color constants, and two-pass canvas for ReportLab & Pillow generators.
"""

import os
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from PIL import ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IMG_DIR = os.path.join(PROJECT_ROOT, "images")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

# Brand Color Palette
PRIMARY_COLOR = colors.HexColor("#0f172a")     # Dark Slate
SECONDARY_COLOR = colors.HexColor("#0284c7")   # Electric Blue
ACCENT_COLOR = colors.HexColor("#10b981")      # Emerald Green
WARN_COLOR = colors.HexColor("#f59e0b")        # Amber
DANGER_COLOR = colors.HexColor("#ef4444")      # Rose Red
BG_LIGHT = colors.HexColor("#f8fafc")          # Off-White
TEXT_DARK = colors.HexColor("#1e293b")         # Charcoal

class MasterclassCanvas(canvas.Canvas):
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

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 756, "Microduck Physical AI Masterclass • Companion Guide")
            self.drawRightString(576, 756, "Pollen Robotics Architecture")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)

        # Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 45, 576, 45)
        self.drawString(36, 32, "Confidential & Educational • MIT License")
        self.drawRightString(576, 32, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()
