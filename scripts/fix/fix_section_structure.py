#!/usr/bin/env python3
"""
Fix mandatory section structure: add missing elements and reorder existing ones.

Beginning (in order after <main class="content">):
  1. Epigraph:      <blockquote class="epigraph">
  2. Big Picture:   <div class="callout big-picture">
  3. Prerequisites: <div class="prerequisites">

End (in order before <nav class="chapter-nav">):
  1. Key Takeaways: <div class="callout key-insight"> (last one before nav)
  2. What's Next:   <div class="whats-next">
  3. Bibliography:  <section class="bibliography">

Skips redirect pages (meta http-equiv="refresh").

Usage:
  python fix_section_structure.py              # Dry run
  python fix_section_structure.py --fix        # Apply all
  python fix_section_structure.py --fix --main # Main chapters only
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Detection patterns
EPIGRAPH_RE = re.compile(r'<blockquote\s+class="epigraph"')
BIG_PICTURE_RE = re.compile(r'<div\s+class="callout\s+big-picture">')
PREREQUISITES_RE = re.compile(r'<div\s+class="prerequisites">')
KEY_INSIGHT_RE = re.compile(r'<div\s+class="callout\s+key-insight">')
WHATS_NEXT_RE = re.compile(r'<div\s+class="whats-next">')
BIBLIOGRAPHY_RE = re.compile(r'<section\s+class="bibliography">')
CHAPTER_NAV_RE = re.compile(r'<nav\s+class="chapter-nav">')
MAIN_CONTENT_RE = re.compile(r'<main\s+class="content">')

# Placeholders
EPIGRAPH_PH = '''<blockquote class="epigraph">
    <p>TODO: Add section epigraph</p>
    <cite>A Thoughtful AI Agent</cite>
</blockquote>'''

BIG_PICTURE_PH = '''<div class="callout big-picture">
    <div class="callout-title">Big Picture</div>
    <p>TODO: Add big picture context for this section.</p>
</div>'''

PREREQUISITES_PH = '''<div class="prerequisites">
    <h3>Prerequisites</h3>
    <p>TODO: Add prerequisites for this section.</p>
</div>'''

KEY_INSIGHT_PH = '''<div class="callout key-insight">
    <div class="callout-title">Key Takeaways</div>
    <ul>
        <li>TODO: Add key takeaways for this section.</li>
    </ul>
</div>'''

WHATS_NEXT_PH = '''<div class="whats-next">
    <h2>What Comes Next</h2>
    <p>TODO: Add what comes next.</p>
</div>'''

BIBLIOGRAPHY_PH = '''<section class="bibliography">
<div class="bibliography-title">
    <h2>References and Further Reading</h2>
</div>
<p>TODO: Add bibliography entries.</p>
</section>'''


def find_block_end(content, start):
    """Find end of a block starting at `start` using depth counting."""
    if content[start:start+12] == '<blockquote ':
        open_tag, close_tag = '<blockquote', '</blockquote>'
    elif content[start:start+8] == '<section':
        open_tag, close_tag = '<section', '</section>'
    else:
        open_tag, close_tag = '<div', '</div>'

    depth = 0
    pos = start
    while pos < len(content):
        if content[pos:pos+len(open_tag)] == open_tag and (
            pos + len(open_tag) >= len(content) or content[pos+len(open_tag)] in ' >\n\r\t'
        ):
            depth += 1
        elif content[pos:pos+len(close_tag)] == close_tag:
            depth -= 1
            if depth == 0:
                return pos + len(close_tag)
        pos += 1
    return -1


def extract_block_text(content, match):
    """Extract full block text from a regex match, including trailing whitespace."""
    start = match.start()
    end = find_block_end(content, start)
    if end == -1:
        return None, -1, -1
    # Include trailing newlines but stop before consuming the next element
    while end < len(content) and content[end] in '\n\r \t':
        end += 1
    # Safety: back off if we consumed the '<' of the next element
    if end < len(content) and content[end] == '<':
        # Back off to just after the last newline
        while end > 0 and content[end - 1] in ' \t':
            end -= 1
    return content[start:end], start, end


def process_file(filepath, fix=False):
    content = filepath.read_text(encoding="utf-8")
    original = content

    if 'http-equiv="refresh"' in content:
        return 0

    changes = 0
    issues = []

    main_match = MAIN_CONTENT_RE.search(content)
    if not main_match:
        return 0
    main_end = main_match.end()

    nav_match = CHAPTER_NAV_RE.search(content)
    if not nav_match:
        return 0
    nav_pos = nav_match.start()

    # ============================================================
    # BEGINNING: Reorder epigraph, big_picture, prerequisites
    # ============================================================

    ep_m = EPIGRAPH_RE.search(content, main_end, nav_pos)
    bp_m = BIG_PICTURE_RE.search(content, main_end, nav_pos)
    pr_m = PREREQUISITES_RE.search(content, main_end, nav_pos)

    # Collect existing beginning blocks with positions
    begin_blocks = {}  # name -> (text, start, end)
    for name, match, regex in [('epigraph', ep_m, EPIGRAPH_RE),
                                ('big_picture', bp_m, BIG_PICTURE_RE),
                                ('prerequisites', pr_m, PREREQUISITES_RE)]:
        if match:
            text, start, end = extract_block_text(content, match)
            if text:
                begin_blocks[name] = (text, start, end)

    # Check if reorder needed
    if len(begin_blocks) >= 2:
        order = ['epigraph', 'big_picture', 'prerequisites']
        existing = [(name, begin_blocks[name][1]) for name in order if name in begin_blocks]
        actual_positions = [pos for _, pos in existing]
        if actual_positions != sorted(actual_positions):
            # Need to reorder: extract all blocks, remove them, reinsert in order
            changes += 1
            issues.append(f"[REORDER] Beginning: {[n for n,_ in existing]}")

            if fix:
                # Sort blocks by position (highest first for removal)
                blocks_to_remove = sorted(begin_blocks.values(), key=lambda x: x[1], reverse=True)
                for text, start, end in blocks_to_remove:
                    # Also remove leading whitespace
                    ws_start = start
                    while ws_start > 0 and content[ws_start-1] in ' \t':
                        ws_start -= 1
                    if ws_start > 0 and content[ws_start-1] == '\n':
                        ws_start -= 1
                    content = content[:ws_start] + content[end:]

                # Find insertion point (after <main class="content"> + whitespace)
                main_match2 = MAIN_CONTENT_RE.search(content)
                insert_pos = main_match2.end()
                while insert_pos < len(content) and content[insert_pos] in '\n\r\t ':
                    insert_pos += 1

                # Build ordered insertion
                ordered_text = ''
                for name in order:
                    if name in begin_blocks:
                        block_text = begin_blocks[name][0].strip()
                        ordered_text += '\n' + block_text + '\n\n'

                content = content[:insert_pos] + ordered_text + content[insert_pos:]

    # ============================================================
    # BEGINNING: Add missing elements
    # ============================================================

    # Re-find positions after possible reorder
    main_match2 = MAIN_CONTENT_RE.search(content)
    main_end2 = main_match2.end() if main_match2 else main_end

    ep_exists = bool(EPIGRAPH_RE.search(content, main_end2))
    bp_exists = bool(BIG_PICTURE_RE.search(content, main_end2))
    pr_exists = bool(PREREQUISITES_RE.search(content, main_end2))

    missing_begin = []
    if not ep_exists:
        missing_begin.append(('epigraph', EPIGRAPH_PH))
        changes += 1
        issues.append("[MISSING] Epigraph")
    if not bp_exists:
        missing_begin.append(('big_picture', BIG_PICTURE_PH))
        changes += 1
        issues.append("[MISSING] Big Picture")
    if not pr_exists:
        missing_begin.append(('prerequisites', PREREQUISITES_PH))
        changes += 1
        issues.append("[MISSING] Prerequisites")

    if missing_begin and fix:
        insert_pos = main_end2
        while insert_pos < len(content) and content[insert_pos] in '\n\r\t ':
            insert_pos += 1

        # Find where to insert each missing element based on order
        # We need to insert after existing elements that come before in order
        ep_m2 = EPIGRAPH_RE.search(content, main_end2)
        bp_m2 = BIG_PICTURE_RE.search(content, main_end2)
        pr_m2 = PREREQUISITES_RE.search(content, main_end2)

        for name, placeholder in missing_begin:
            # Find correct insertion position
            if name == 'epigraph':
                # Insert at beginning
                pos = insert_pos
            elif name == 'big_picture':
                # Insert after epigraph if it exists
                if ep_m2 or EPIGRAPH_RE.search(content, main_end2):
                    m = EPIGRAPH_RE.search(content, main_end2)
                    _, _, end = extract_block_text(content, m)
                    pos = end
                else:
                    pos = insert_pos
            elif name == 'prerequisites':
                # Insert after big_picture or epigraph
                m = BIG_PICTURE_RE.search(content, main_end2)
                if m:
                    _, _, end = extract_block_text(content, m)
                    pos = end
                else:
                    m = EPIGRAPH_RE.search(content, main_end2)
                    if m:
                        _, _, end = extract_block_text(content, m)
                        pos = end
                    else:
                        pos = insert_pos

            content = content[:pos] + '\n' + placeholder + '\n\n' + content[pos:]

    # ============================================================
    # END: Add missing elements before <nav class="chapter-nav">
    # ============================================================

    nav_match3 = CHAPTER_NAV_RE.search(content)
    if not nav_match3:
        if fix and content != original:
            filepath.write_text(content, encoding="utf-8")
        return changes

    nav_pos3 = nav_match3.start()

    ki_exists = bool(KEY_INSIGHT_RE.search(content))
    wn_exists = bool(WHATS_NEXT_RE.search(content))
    bib_exists = bool(BIBLIOGRAPHY_RE.search(content))

    missing_end = []
    if not ki_exists:
        missing_end.append(('key_insight', KEY_INSIGHT_PH))
        changes += 1
        issues.append("[MISSING] Key Takeaways")
    if not wn_exists:
        missing_end.append(('whats_next', WHATS_NEXT_PH))
        changes += 1
        issues.append("[MISSING] What's Next")
    if not bib_exists:
        missing_end.append(('bibliography', BIBLIOGRAPHY_PH))
        changes += 1
        issues.append("[MISSING] Bibliography")

    if missing_end and fix:
        # Re-find nav position
        nav_match4 = CHAPTER_NAV_RE.search(content)
        nav_pos4 = nav_match4.start()

        # Insert in order: key_insight, whats_next, bibliography (before nav)
        # But respect existing elements: insert each missing one in its correct slot
        insert_text = '\n'
        for name, placeholder in missing_end:
            insert_text += placeholder + '\n\n'

        content = content[:nav_pos4] + insert_text + content[nav_pos4:]

    # ============================================================
    # END: Check order of existing end elements
    # ============================================================

    nav_match5 = CHAPTER_NAV_RE.search(content)
    if nav_match5:
        nav_p5 = nav_match5.start()
        # Find last key-insight before nav (the one serving as "key takeaways")
        ki_matches = list(KEY_INSIGHT_RE.finditer(content))
        ki_last = None
        for m in reversed(ki_matches):
            # Check it's a "takeaway" type (near end of file, before nav)
            if m.start() > nav_p5 * 0.5:  # in the latter half of the file
                ki_last = m
                break

        wn_m = WHATS_NEXT_RE.search(content)
        bib_m = BIBLIOGRAPHY_RE.search(content)

        end_elements = []
        if ki_last: end_elements.append(('key_insight', ki_last.start()))
        if wn_m: end_elements.append(('whats_next', wn_m.start()))
        if bib_m: end_elements.append(('bibliography', bib_m.start()))

        if len(end_elements) >= 2:
            expected = ['key_insight', 'whats_next', 'bibliography']
            actual = [n for n, _ in sorted(end_elements, key=lambda x: x[1])]
            expected_f = [e for e in expected if e in actual]
            if actual != expected_f:
                changes += 1
                issues.append(f"[REORDER] End: {actual} should be {expected_f}")

    if fix and content != original:
        filepath.write_text(content, encoding="utf-8")

    return changes, issues


def main():
    fix = '--fix' in sys.argv
    main_only = '--main' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    if not main_only:
        all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    total_changes = 0
    files_changed = 0

    for f in all_files:
        if '_archive' in str(f):
            continue
        result = process_file(f, fix=fix)
        if isinstance(result, tuple):
            ch, issues = result
        else:
            ch, issues = result, []
        if ch > 0:
            files_changed += 1
            total_changes += ch
            rel = f.relative_to(BOOK_ROOT)
            if fix:
                print(f"  FIXED: {rel} ({ch} changes)")
            else:
                for issue in issues:
                    print(f"    {issue}")
                print(f"  {rel}: {ch} issues")

    print(f"\n{'=' * 60}")
    print(f"Total changes: {total_changes}")
    print(f"Files affected: {files_changed}")
    if not fix and total_changes > 0:
        print(f"\nRun with --fix to apply changes.")
        print(f"Run with --fix --main to fix only main chapters.")


if __name__ == "__main__":
    main()
