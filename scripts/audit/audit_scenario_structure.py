#!/usr/bin/env python3
"""Audit practical-example callouts for required narrative structure.

Scans all section HTML files under part-*/ and appendices-*/ for
<div class="callout practical-example"> blocks and checks whether each
one contains the required bold-prefix fields for a real-world scenario.

Required fields (all must be present):
    Who, Situation, Problem, Decision or Dilemma (at least one), Result, Lesson

Optional fields (allowed but not required):
    How, Scenario, Approach

Classification:
    CONFORMING    : all required fields present
    PARTIAL       : some required fields present, some missing
    NON_NARRATIVE : zero required fields (likely a code demo needing reclassification)

Usage:
    python audit_scenario_structure.py          # report only
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOOK_ROOT = Path("E:/Projects/LLMCourse")

# Patterns for locating section HTML files
SECTION_GLOBS = [
    "part-*/module-*/section-*.html",
    "appendices/*/section-*.html",
]

# Required bold prefixes. "Decision" and "Dilemma" count as one slot
# (at least one of the two must appear).
REQUIRED_SINGLES = ["Who", "Situation", "Problem", "Result", "Lesson"]
DECISION_GROUP = ["Decision", "Dilemma"]

# Optional (never flagged as missing)
OPTIONAL_FIELDS = ["How", "Scenario", "Approach"]

# All recognized fields (for detection)
ALL_FIELDS = REQUIRED_SINGLES + DECISION_GROUP + OPTIONAL_FIELDS

# Regex to find a practical-example callout opening tag
RE_CALLOUT_OPEN = re.compile(
    r'<div\s+class="callout\s+practical-example">', re.IGNORECASE
)

# Regex to extract the callout-title text
RE_CALLOUT_TITLE = re.compile(
    r'<div\s+class="callout-title">\s*(.*?)\s*</div>', re.IGNORECASE | re.DOTALL
)

# Regex to find bold prefixes like <strong>Who:</strong>
RE_BOLD_PREFIX = re.compile(r"<strong>(\w[\w\s]*):\s*</strong>", re.IGNORECASE)


def find_section_files() -> list[Path]:
    """Return sorted list of section HTML files, excluding _archive/."""
    files: list[Path] = []
    for pattern in SECTION_GLOBS:
        for p in BOOK_ROOT.glob(pattern):
            if "_archive" in p.parts:
                continue
            files.append(p)
    files.sort()
    return files


def extract_callout_blocks(html: str) -> list[tuple[int, str]]:
    """Return list of (line_number, block_html) for each practical-example callout.

    We track nesting depth of <div> tags to capture the complete block.
    """
    results: list[tuple[int, str]] = []
    lines = html.split("\n")
    i = 0
    while i < len(lines):
        match = RE_CALLOUT_OPEN.search(lines[i])
        if match:
            start_line = i + 1  # 1-based
            depth = 0
            block_lines: list[str] = []
            j = i
            # Walk forward, tracking div depth
            while j < len(lines):
                line = lines[j]
                # Count opening divs (excluding self-closing)
                depth += len(re.findall(r"<div[\s>]", line, re.IGNORECASE))
                depth -= len(re.findall(r"</div>", line, re.IGNORECASE))
                block_lines.append(line)
                if depth <= 0:
                    break
                j += 1
            results.append((start_line, "\n".join(block_lines)))
            i = j + 1
        else:
            i += 1
    return results


def extract_title(block_html: str) -> str:
    """Extract the callout-title text from a block."""
    m = RE_CALLOUT_TITLE.search(block_html)
    if m:
        # Strip HTML tags from the title
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return title
    return "(no title)"


def extract_found_fields(block_html: str) -> set[str]:
    """Return the set of bold-prefix field names found in the block."""
    found: set[str] = set()
    for m in RE_BOLD_PREFIX.finditer(block_html):
        field = m.group(1).strip()
        # Normalize to title case for matching
        for known in ALL_FIELDS:
            if field.lower() == known.lower():
                found.add(known)
                break
    return found


def classify_callout(
    found_fields: set[str],
) -> tuple[str, list[str]]:
    """Classify a callout and return (status, list_of_missing_fields).

    Returns one of: CONFORMING, PARTIAL, NON_NARRATIVE
    """
    missing: list[str] = []

    # Check each required single field
    for field in REQUIRED_SINGLES:
        if field not in found_fields:
            missing.append(field)

    # Check Decision/Dilemma group
    has_decision_or_dilemma = bool(found_fields & set(DECISION_GROUP))
    if not has_decision_or_dilemma:
        missing.append("Decision/Dilemma")

    if not missing:
        return "CONFORMING", []

    # Count how many required slots are present
    total_required = len(REQUIRED_SINGLES) + 1  # +1 for the Decision/Dilemma group
    present = total_required - len(missing)
    if present == 0:
        return "NON_NARRATIVE", missing

    return "PARTIAL", missing


def main() -> None:
    files = find_section_files()
    if not files:
        print("ERROR: No section files found. Check BOOK_ROOT path.")
        sys.exit(1)

    total_callouts = 0
    conforming: list[tuple[str, int, str]] = []
    partial: list[tuple[str, int, str, list[str], set[str]]] = []
    non_narrative: list[tuple[str, int, str, set[str]]] = []

    for filepath in files:
        html = filepath.read_text(encoding="utf-8", errors="replace")
        blocks = extract_callout_blocks(html)

        rel_path = filepath.relative_to(BOOK_ROOT).as_posix()

        for line_num, block_html in blocks:
            total_callouts += 1
            title = extract_title(block_html)
            found = extract_found_fields(block_html)
            status, missing = classify_callout(found)

            if status == "CONFORMING":
                conforming.append((rel_path, line_num, title))
            elif status == "PARTIAL":
                partial.append((rel_path, line_num, title, missing, found))
            else:
                non_narrative.append((rel_path, line_num, title, found))

    # Print report
    print("=" * 78)
    print("PRACTICAL-EXAMPLE SCENARIO STRUCTURE AUDIT")
    print("=" * 78)
    print()
    print(f"Files scanned:    {len(files)}")
    print(f"Callouts found:   {total_callouts}")
    print()
    print(f"  CONFORMING:     {len(conforming)}")
    print(f"  PARTIAL:        {len(partial)}")
    print(f"  NON_NARRATIVE:  {len(non_narrative)}")
    print()

    if partial:
        print("-" * 78)
        print("PARTIAL (has some required fields, missing others)")
        print("-" * 78)
        for rel_path, line_num, title, missing, found in partial:
            print(f"\n  File:    {rel_path}")
            print(f"  Line:    {line_num}")
            print(f"  Title:   {title}")
            print(f"  Found:   {', '.join(sorted(found)) if found else '(none)'}")
            print(f"  Missing: {', '.join(missing)}")

    if non_narrative:
        print()
        print("-" * 78)
        print("NON_NARRATIVE (no required fields; likely needs reclassification)")
        print("-" * 78)
        for rel_path, line_num, title, found in non_narrative:
            print(f"\n  File:    {rel_path}")
            print(f"  Line:    {line_num}")
            print(f"  Title:   {title}")
            if found:
                print(f"  Fields:  {', '.join(sorted(found))} (optional only)")

    if not partial and not non_narrative:
        print("All practical-example callouts conform to the required structure.")

    print()
    print("=" * 78)
    print("AUDIT COMPLETE")
    print("=" * 78)


if __name__ == "__main__":
    main()
