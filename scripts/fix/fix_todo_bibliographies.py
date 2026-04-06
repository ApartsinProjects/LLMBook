#!/usr/bin/env python3
"""
fix_todo_bibliographies.py
==========================
Audit (and eventually fix) bibliography sections that contain TODO placeholders.

Phase 1 (DRY RUN): Scan all .html files under part-*/ and appendices/,
find <section class="bibliography"> blocks containing "TODO", extract
section topic info from headings/content, and report findings.

Usage:
    python fix_todo_bibliographies.py              # dry-run audit
    python fix_todo_bibliographies.py --fix        # apply fixes (Phase 2)
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
SKIP_DIRS = {"_archive", "_lab_fragments", "node_modules", ".git", "__pycache__"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def gather_html_files():
    """Collect all section .html files under part-*/ and appendices/."""
    files = []
    for pattern in ["part-*/**/section-*.html", "appendices/**/section-*.html"]:
        for p in BOOK_ROOT.glob(pattern):
            # Skip any path component in SKIP_DIRS
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            files.append(p)
    files.sort()
    return files


def extract_todo_bibliographies(filepath):
    """Return True if the file has a bibliography section with TODO text."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    # Find bibliography sections
    bib_match = re.search(
        r'<section\s+class="bibliography">(.*?)</section>',
        text, re.DOTALL
    )
    if not bib_match:
        return False, None
    bib_content = bib_match.group(1)
    if "TODO" in bib_content:
        return True, bib_content
    return False, None


def extract_section_topic(filepath):
    """Extract topic info from the section: h1/h2 headings, key terms."""
    text = filepath.read_text(encoding="utf-8", errors="replace")

    info = {}

    # Get the chapter/section from the file path
    parts = filepath.relative_to(BOOK_ROOT).parts
    info["path"] = str(filepath.relative_to(BOOK_ROOT))
    info["parent_dir"] = parts[-2] if len(parts) >= 2 else ""

    # Extract chapter name from parent directory
    parent = filepath.parent.name
    # e.g. "module-22-ai-agents" or "appendix-k-huggingface-ecosystem"
    info["chapter_slug"] = parent

    # Extract h1
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
    if h1:
        info["h1"] = re.sub(r"<[^>]+>", "", h1.group(1)).strip()

    # Extract all h2 headings (topic indicators)
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", text, re.DOTALL)
    info["h2s"] = [re.sub(r"<[^>]+>", "", h).strip() for h in h2s]
    # Filter out generic headings
    info["h2s"] = [
        h for h in info["h2s"]
        if h not in ("References and Further Reading", "What Comes Next",
                     "Prerequisites", "Learning Objectives",
                     "Key Takeaways", "Knowledge Check")
    ]

    # Extract key terms from <strong> or <dfn> tags (first 20)
    strongs = re.findall(r"<(?:strong|dfn)[^>]*>(.*?)</(?:strong|dfn)>", text)
    terms = list(dict.fromkeys(
        re.sub(r"<[^>]+>", "", s).strip() for s in strongs[:30]
    ))
    info["key_terms"] = terms[:15]

    return info


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------

def audit():
    """Run the dry-run audit and print findings."""
    files = gather_html_files()
    print(f"Scanning {len(files)} HTML files...\n")

    todo_files = []
    has_bib_no_todo = 0
    no_bib = 0

    for f in files:
        has_todo, bib_content = extract_todo_bibliographies(f)
        if has_todo:
            topic = extract_section_topic(f)
            todo_files.append((f, topic))
        elif bib_content is not None:
            has_bib_no_todo += 1
        else:
            no_bib += 1

    # Group by chapter
    by_chapter = defaultdict(list)
    for f, topic in todo_files:
        by_chapter[topic["chapter_slug"]].append((f, topic))

    print("=" * 78)
    print(f"TODO BIBLIOGRAPHY AUDIT REPORT")
    print("=" * 78)
    print(f"Total files scanned:           {len(files)}")
    print(f"Files with TODO bibliographies: {len(todo_files)}")
    print(f"Files with complete biblios:    {has_bib_no_todo}")
    print(f"Files with no bibliography:     {no_bib}")
    print(f"Chapters affected:              {len(by_chapter)}")
    print("=" * 78)

    for chapter_slug in sorted(by_chapter.keys()):
        entries = by_chapter[chapter_slug]
        print(f"\n--- {chapter_slug} ({len(entries)} sections) ---")
        for f, topic in entries:
            section_name = f.stem  # e.g. section-22.4
            h1 = topic.get("h1", "(no h1)")
            h2_list = topic.get("h2s", [])
            terms = topic.get("key_terms", [])

            print(f"\n  {section_name}: {h1}")
            if h2_list:
                print(f"    Subtopics: {', '.join(h2_list[:5])}")
            if terms:
                print(f"    Key terms: {', '.join(terms[:8])}")

    print("\n" + "=" * 78)
    print("END OF AUDIT")
    print("=" * 78)

    return todo_files


if __name__ == "__main__":
    if "--fix" in sys.argv:
        print("FIX mode not yet implemented. Run without --fix for audit.")
        sys.exit(1)
    audit()
