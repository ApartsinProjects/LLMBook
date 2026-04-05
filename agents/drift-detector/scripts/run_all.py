#!/usr/bin/env python3
"""Run all drift detection checks and print a consolidated report."""

import sys
import os
import time
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    print("=" * 60)
    print("  DRIFT DETECTION: Full Audit")
    print("=" * 60)
    start = time.time()

    checks = [
        ("detect_toc_drift", "TOC vs Files"),
        ("detect_index_drift", "Index Pages vs Sections"),
        ("detect_nav_drift", "Navigation Links"),
        ("detect_xref_drift", "Cross-References"),
        ("detect_caption_drift", "Caption Numbering"),
        ("detect_section_drift", "Section Numbering"),
    ]

    total_errors = 0
    total_warns = 0
    total_infos = 0

    for module_name, label in checks:
        print(f"\n  Running: {label}...")
        try:
            mod = __import__(module_name)
            mod.main()
        except Exception as e:
            print(f"  [FATAL] {label} failed: {e}")
            import traceback
            traceback.print_exc()

    elapsed = time.time() - start
    print(f"\n{'=' * 60}")
    print(f"  Completed in {elapsed:.1f}s")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
