"""
Sweep: Standardize content order on chapter index pages.

Canonical order for chapter index pages (part-*/module-*/index.html):
  1. header (header-nav, part-label, h1)
  2. epigraph
  3. illustration
  4. overview
  5. prereqs  <-- MOVED UP from bottom
  6. objectives
  7. fun-note (optional, max 1 before sections)
  8. h2 "Sections" + sections-list
  9. fun-note (optional, max 1 after sections)
  10. bibliography
  11. whats-next
  12. chapter-nav
  13. footer

This script specifically moves <div class="prereqs"> from its current position
(typically after sections-list) to right before <div class="objectives">.
"""

import re
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")

def find_chapter_indices():
    """Find all chapter index.html files (inside module-* dirs)."""
    files = []
    for f in ROOT.rglob("index.html"):
        if "module-" in str(f.parent.name) and "agents" not in str(f):
            files.append(f)
    return sorted(files)

def extract_block(html, start_pattern, end_patterns):
    """Extract a block from HTML between start pattern and one of end patterns."""
    start_match = re.search(start_pattern, html)
    if not start_match:
        return None, None, None

    start_pos = start_match.start()
    # Find the end of this block
    remaining = html[start_match.end():]

    # For div blocks, count nesting
    if '<div' in start_match.group():
        depth = 1
        i = 0
        while i < len(remaining) and depth > 0:
            if remaining[i:i+4] == '<div':
                depth += 1
            elif remaining[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end_pos = start_match.end() + i + 6
                    # Include trailing whitespace/newlines
                    while end_pos < len(html) and html[end_pos] in '\n\r ':
                        end_pos += 1
                    return start_pos, end_pos, html[start_pos:end_pos]
            i += 1

    return None, None, None

def process_file(filepath):
    """Move prereqs block to before objectives block."""
    html = filepath.read_text(encoding="utf-8")
    original = html

    # Check if both prereqs and objectives exist
    prereqs_match = re.search(r'<div\s+class="prereqs">', html)
    objectives_match = re.search(r'<div\s+class="objectives">', html)

    if not prereqs_match or not objectives_match:
        return False, "missing prereqs or objectives"

    # Check if prereqs is already before objectives
    if prereqs_match.start() < objectives_match.start():
        return False, "already in order"

    # Extract the prereqs block
    prereqs_start, prereqs_end, prereqs_block = extract_block(
        html, r'<div\s+class="prereqs">', [])

    if not prereqs_block:
        return False, "could not extract prereqs block"

    # Remove prereqs from its current position
    html = html[:prereqs_start] + html[prereqs_end:]

    # Find objectives position again (it may have shifted)
    objectives_match2 = re.search(r'<div\s+class="objectives">', html)
    if not objectives_match2:
        return False, "lost objectives after removal"

    # Insert prereqs right before objectives
    insert_pos = objectives_match2.start()
    # Add proper spacing
    prereqs_insert = prereqs_block.rstrip() + "\n\n    "
    html = html[:insert_pos] + prereqs_insert + html[insert_pos:]

    if html != original:
        filepath.write_text(html, encoding="utf-8")
        return True, "moved prereqs before objectives"
    return False, "no change"

def main():
    files = find_chapter_indices()
    print(f"Found {len(files)} chapter index files\n")

    moved = 0
    already_ok = 0
    missing = 0
    errors = 0

    for f in files:
        try:
            changed, reason = process_file(f)
            rel = f.relative_to(ROOT)
            if changed:
                moved += 1
                print(f"  MOVED: {rel} ({reason})")
            elif "already" in reason:
                already_ok += 1
            elif "missing" in reason:
                missing += 1
                print(f"  SKIP:  {rel} ({reason})")
            else:
                print(f"  SKIP:  {rel} ({reason})")
        except Exception as e:
            errors += 1
            print(f"  ERROR: {f.relative_to(ROOT)}: {e}")

    print(f"\n=== Summary ===")
    print(f"Total chapter indices: {len(files)}")
    print(f"Prereqs moved: {moved}")
    print(f"Already in order: {already_ok}")
    print(f"Missing prereqs/objectives: {missing}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    main()
