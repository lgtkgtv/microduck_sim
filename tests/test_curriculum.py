"""
test_curriculum.py - Pytest wrapper for 6-phase curriculum verification.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)

import verify_curriculum

def test_phase1():
    verify_curriculum.test_phase1_anatomy()

def test_phase2():
    verify_curriculum.test_phase2_matrix()

def test_phase3():
    verify_curriculum.test_phase3_dogtrainer()

def test_phase4():
    verify_curriculum.test_phase4_brainsurgery()

def test_phase5():
    verify_curriculum.test_phase5_nervoussystem()

def test_phase6():
    verify_curriculum.test_phase6_securingswarm()
