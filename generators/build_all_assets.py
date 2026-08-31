#!/usr/bin/env python3
"""
build_all_assets.py
Unified single-command build pipeline for all curriculum assets:
  1. Renders all 26 Pillow technical diagrams (400x300 PNGs) into images/
  2. Compiles all 6 ReportLab module handouts into docs/
  3. Merges handouts into the Complete Masterclass Book in docs/
  4. Packages everything into docs/microduck_all_handouts.zip
"""

import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import generate_images
import generate_phase2_images
import generate_phase3_images
import generate_phase4_images
import generate_phase5_images
import generate_phase6_images

import generate_handout
import generate_phase2_handout
import generate_phase3_handout
import generate_phase4_handout
import generate_phase5_handout
import generate_phase6_handout

import bundle_handouts

def main():
    start_time = time.time()
    print("=" * 70)
    print("🚀 MICRODUCK PHYSICAL AI: UNIFIED ASSET COMPILATION PIPELINE")
    print("=" * 70)

    # 1. Generate all Pillow Diagrams
    print("\n🎨 [1/3] Rendering 26 Technical Engineering Diagrams into images/...")
    generate_images.main()
    generate_phase2_images.main()
    generate_phase3_images.main()
    generate_phase4_images.main()
    generate_phase5_images.main()
    generate_phase6_images.main()
    print("   ✔ All 26 diagrams generated.")

    # 2. Compile all 6 ReportLab Handouts
    print("\n📄 [2/3] Compiling 6 ReportLab Module Handouts into docs/...")
    generate_handout.main()
    generate_phase2_handout.main()
    generate_phase3_handout.main()
    generate_phase4_handout.main()
    generate_phase5_handout.main()
    generate_phase6_handout.main()
    print("   ✔ All 6 handouts compiled.")

    # 3. Bundle Master Manual & Zip Archive
    print("\n📦 [3/3] Merging Masterclass Book & Packaging Zip Archive into docs/...")
    bundle_handouts.main()
    print("   ✔ Master book and zip archive compiled.")

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"🎉 PIPELINE COMPLETE in {elapsed:.2f}s: All assets up to date in images/ and docs/!")
    print("=" * 70)

if __name__ == "__main__":
    main()
