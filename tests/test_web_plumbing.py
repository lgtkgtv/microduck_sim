"""
test_web_plumbing.py - Pytest wrapper for static web plumbing and broken link auditor.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)

import verify_web_plumbing

def test_static_web_plumbing():
    result = verify_web_plumbing.main()
    assert result == 0, "Web plumbing verification detected broken links!"
