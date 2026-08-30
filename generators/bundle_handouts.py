#!/usr/bin/env python3
"""
bundle_handouts.py
Merges all 6 phase handouts into a single Masterclass PDF Manual
and packages them into a convenient zip file for students.
"""

import os
import zipfile
from pypdf import PdfWriter

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

HANDOUT_FILES = [
    ("Phase 1: Anatomy of a Robot", os.path.join(PROJECT_ROOT, "Phase1_Anatomy_Handout.pdf")),
    ("Phase 2: The Invisible Matrix", os.path.join(PROJECT_ROOT, "Phase2_Matrix_Handout.pdf")),
    ("Phase 3: The Dog Trainer", os.path.join(PROJECT_ROOT, "Phase3_DogTrainer_Handout.pdf")),
    ("Phase 4: Brain Surgery & Edge Inference", os.path.join(PROJECT_ROOT, "Phase4_BrainSurgery_Handout.pdf")),
    ("Phase 5: The Nervous System", os.path.join(PROJECT_ROOT, "Phase5_NervousSystem_Handout.pdf")),
    ("Phase 6: Securing the Swarm", os.path.join(PROJECT_ROOT, "Phase6_SecuringSwarm_Handout.pdf")),
]

MASTER_PDF = os.path.join(PROJECT_ROOT, "Microduck_Physical_AI_Masterclass_Complete_Book.pdf")
ZIP_BUNDLE = os.path.join(PROJECT_ROOT, "microduck_all_handouts.zip")

def main():
    print("=" * 60)
    print("📦 Bundling all 6 Phase Handouts...")
    print("=" * 60)
    
    # 1. Merge into Complete Master PDF
    writer = PdfWriter()
    for title, pdf_path in HANDOUT_FILES:
        if os.path.exists(pdf_path):
            print(f"  + Merging {title} ({os.path.basename(pdf_path)})...")
            writer.append(pdf_path)
        else:
            print(f"  ⚠️ Missing: {pdf_path}")
            
    with open(MASTER_PDF, "wb") as f_out:
        writer.write(f_out)
    writer.close()
    print(f"✅ Generated Complete Master Book: {MASTER_PDF} ({os.path.getsize(MASTER_PDF)} bytes)")
    
    # 2. Package into Zip Archive
    with zipfile.ZipFile(ZIP_BUNDLE, "w", zipfile.ZIP_DEFLATED) as zf:
        for title, pdf_path in HANDOUT_FILES:
            if os.path.exists(pdf_path):
                zf.write(pdf_path, arcname=os.path.basename(pdf_path))
        zf.write(MASTER_PDF, arcname=os.path.basename(MASTER_PDF))
        
    print(f"✅ Generated Zip Archive: {ZIP_BUNDLE} ({os.path.getsize(ZIP_BUNDLE)} bytes)")
    print("=" * 60)

if __name__ == "__main__":
    main()
