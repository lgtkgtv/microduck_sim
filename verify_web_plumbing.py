#!/usr/bin/env python3
"""
verify_web_plumbing.py
Automated static website plumbing and broken link checker for GitHub Pages.
Scans index.html and all curriculum/*.html files to ensure:
  • 100% of internal HTML href links resolve to existing files
  • 100% of img src tags resolve to existing image assets
  • 100% of JavaScript dynamic page routes (e.g. slidePages, location.href) resolve to real files
  • 0 broken links or 404 errors
"""

import os
import re
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def check_file_plumbing(html_path):
    print(f"\n🔍 Scanning: {os.path.relpath(html_path, SCRIPT_DIR)}")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    base_dir = os.path.dirname(html_path)

    # 1. Regex patterns for HTML attributes
    hrefs = re.findall(r'href=["\'](.*?)["\']', content)
    srcs = re.findall(r'src=["\'](.*?)["\']', content)

    # 2. Regex for JavaScript strings referencing .html or .pdf or images
    js_strings = re.findall(r'["\']([^"\']+\.(?:html|pdf|png|zip))["\']', content)

    all_links = list(set(hrefs + srcs + js_strings))
    broken = []
    verified = 0

    for link in all_links:
        # Ignore external URLs, anchor fragments, and javascript:
        if link.startswith(("http://", "https://", "#", "javascript:", "mailto:")):
            continue

        clean_link = link.split("?")[0].split("#")[0]
        if not clean_link or clean_link.startswith("$"):
            continue

        target_path = os.path.normpath(os.path.join(base_dir, clean_link))
        if os.path.exists(target_path):
            verified += 1
        else:
            broken.append((link, target_path))

    print(f"  • Verified internal links, assets & JS routes: {verified}")
    if broken:
        print(f"  ❌ Broken Links Found ({len(broken)}):")
        for orig, target in broken:
            print(f"    - Link '{orig}' -> Target '{os.path.relpath(target, SCRIPT_DIR)}' (MISSING)")
        return False
    else:
        print(f"  ✅ Plumbing check passed: 0 broken links!")
        return True

def main():
    print("=" * 65)
    print("🌐 GitHub Pages Static Web Plumbing & Link Integrity Checker")
    print("=" * 65)

    html_files = [os.path.join(SCRIPT_DIR, "index.html")] + glob.glob(os.path.join(SCRIPT_DIR, "curriculum", "*.html"))
    
    all_passed = True
    for html_file in html_files:
        if not check_file_plumbing(html_file):
            all_passed = False

    print("\n" + "=" * 65)
    if all_passed:
        print("🎉 ALL STATIC WEB PLUMBING VERIFIED: 100% HEALTHY (0 BROKEN LINKS)")
    else:
        print("❌ WEB PLUMBING FAILED: Some links could not be resolved.")
    print("=" * 65 + "\n")

    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
