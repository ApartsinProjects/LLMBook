#!/usr/bin/env python3
"""Audit section HTML files for structural consistency (beginning and end elements).

Standard beginning (in order):
  1. Epigraph:      <blockquote class="epigraph">
  2. Big Picture:   <div class="callout big-picture">
  3. Prerequisites: <div class="prerequisites">

Mandatory end elements (before </main>):
  1. Key Takeaways: <div class="callout key-insight"> with title containing
                    "Key Takeaway" or "Key Insight"  (MANDATORY)
  2. What's Next:   <div class="whats-next">           (MANDATORY)
  3. Bibliography:  <section class="bibliography">      (MANDATORY)

Optional end elements (checked but not flagged as errors):
  - Real-World Scenario: <div class="callout practical-example">
  - Research Frontier:   <div class="callout research-frontier">
  - Self-Check:          <div class="callout self-check">
  - Exercises:           <div class="callout exercise">
  - Lab:                 <div class="lab"> or <h3 class="lab-title">

Usage:
    /c/Python314/python scripts/audit/audit_section_structure.py
"""

from pathlib import Path
import re
import sys


BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Glob patterns for section files
SECTION_GLOBS = [
    "part-*/module-*/section-*.html",
    "appendices/*/section-*.html",
]

# Exclude archive folders
EXCLUDE_PATTERNS = ["_archive"]


def find_section_files() -> list[Path]:
    files = []
    for pattern in SECTION_GLOBS:
        for f in sorted(BOOK_ROOT.glob(pattern)):
            if any(ex in str(f) for ex in EXCLUDE_PATTERNS):
                continue
            files.append(f)
    return files


def check_file(filepath: Path) -> dict:
    """Check a single section file and return findings."""
    text = filepath.read_text(encoding="utf-8", errors="replace")

    # Compute relative path for display
    rel = filepath.relative_to(BOOK_ROOT)

    result = {
        "file": str(rel),
        # Beginning elements
        "has_epigraph": bool(re.search(r'<blockquote\s+class="epigraph"', text)),
        "has_big_picture": bool(re.search(r'class="callout\s+big-picture"', text)),
        "has_prerequisites": bool(re.search(r'class="prerequisites"', text)),
        # Mandatory end elements
        "has_key_insight": bool(re.search(r'class="callout\s+key-insight"', text)),
        "has_whats_next": bool(re.search(r'class="whats-next"', text)),
        "has_bibliography": bool(re.search(r'<section\s+class="bibliography"', text)),
        # Optional end elements (informational)
        "has_practical_example": bool(re.search(r'class="callout\s+practical-example"', text)),
        "has_research_frontier": bool(re.search(r'class="callout\s+research-frontier"', text)),
        "has_self_check": bool(re.search(r'class="callout\s+self-check"', text)),
        "has_exercise": bool(re.search(r'class="callout\s+exercise"', text)),
        "has_lab": bool(
            re.search(r'class="lab"', text)
            or re.search(r'class="lab-title"', text)
        ),
    }
    return result


def main():
    files = find_section_files()
    if not files:
        print("ERROR: No section files found. Check BOOK_ROOT path.")
        sys.exit(1)

    results = [check_file(f) for f in files]
    total = len(results)

    # --- Mandatory element labels ---
    mandatory_beginning = [
        ("has_epigraph", "Epigraph"),
        ("has_big_picture", "Big Picture"),
        ("has_prerequisites", "Prerequisites"),
    ]
    mandatory_end = [
        ("has_key_insight", "Key Takeaways / Key Insight"),
        ("has_whats_next", "What's Next"),
        ("has_bibliography", "Bibliography"),
    ]
    optional_end = [
        ("has_practical_example", "Real-World Scenario"),
        ("has_research_frontier", "Research Frontier"),
        ("has_self_check", "Self-Check"),
        ("has_exercise", "Exercises"),
        ("has_lab", "Lab"),
    ]

    # --- Collect missing lists ---
    missing_map: dict[str, list[str]] = {}
    for key, _ in mandatory_beginning + mandatory_end + optional_end:
        missing_map[key] = [r["file"] for r in results if not r[key]]

    # === SUMMARY TABLE ===
    print("=" * 78)
    print(f"  SECTION STRUCTURE AUDIT   ({total} files scanned)")
    print("=" * 78)

    print("\n  BEGINNING ELEMENTS (all mandatory)")
    print("  " + "-" * 55)
    print(f"  {'Element':<35} {'Present':>8} {'Missing':>8}")
    print("  " + "-" * 55)
    for key, label in mandatory_beginning:
        missing = len(missing_map[key])
        present = total - missing
        flag = " ***" if missing > 0 else ""
        print(f"  {label:<35} {present:>8} {missing:>8}{flag}")

    print("\n  END ELEMENTS (mandatory)")
    print("  " + "-" * 55)
    print(f"  {'Element':<35} {'Present':>8} {'Missing':>8}")
    print("  " + "-" * 55)
    for key, label in mandatory_end:
        missing = len(missing_map[key])
        present = total - missing
        flag = " ***" if missing > 0 else ""
        print(f"  {label:<35} {present:>8} {missing:>8}{flag}")

    print("\n  END ELEMENTS (optional, informational)")
    print("  " + "-" * 55)
    print(f"  {'Element':<35} {'Present':>8} {'Missing':>8}")
    print("  " + "-" * 55)
    for key, label in optional_end:
        missing = len(missing_map[key])
        present = total - missing
        print(f"  {label:<35} {present:>8} {missing:>8}")

    # === DETAILED MISSING FILES ===
    print("\n" + "=" * 78)
    print("  DETAILED: FILES MISSING MANDATORY ELEMENTS")
    print("=" * 78)

    any_missing = False
    for key, label in mandatory_beginning + mandatory_end:
        if missing_map[key]:
            any_missing = True
            print(f"\n  Missing: {label} ({len(missing_map[key])} files)")
            print("  " + "-" * 55)
            for f in missing_map[key]:
                print(f"    {f}")

    if not any_missing:
        print("\n  All files have all mandatory elements. No issues found.")

    print()


if __name__ == "__main__":
    main()
