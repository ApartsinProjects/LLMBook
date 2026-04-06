"""
Detect and remove orphan code captions (captions not preceded by a code block).

An orphan caption is a <div class="code-caption"> that appears without a
preceding </pre> or <div class="code-output"> within a reasonable distance.

Also detects and removes consecutive duplicate captions (two captions for
the same code block where one is auto-generated and one is manual).

Usage:
  python fix_orphan_captions.py          # Dry run
  python fix_orphan_captions.py --fix    # Apply fixes
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

CAPTION_FULL_RE = re.compile(
    r'\n?<div class="code-caption">.*?</div>\s*',
    re.DOTALL
)


def process_file(filepath, fix=False):
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Find all elements in order: </pre>, code-output, code-caption
    elements = []

    for m in re.finditer(r'</pre>', content):
        elements.append(('pre_close', m.start(), m.end()))

    for m in re.finditer(r'<div class="code-output">.*?</div>', content, re.DOTALL):
        elements.append(('output', m.start(), m.end()))

    for m in re.finditer(r'<div class="code-caption">.*?</div>', content, re.DOTALL):
        elements.append(('caption', m.start(), m.end(), m.group(0)))

    elements.sort(key=lambda e: e[1])

    # Walk through and identify orphan captions
    orphans = []
    last_code_end = -1

    for el in elements:
        if el[0] == 'pre_close':
            last_code_end = el[2]
        elif el[0] == 'output':
            # Output extends the "code block zone"
            if last_code_end > 0 and el[1] - last_code_end < 200:
                last_code_end = el[2]
        elif el[0] == 'caption':
            cap_start = el[1]
            # Check if there's a code block or output within 200 chars before this caption
            between = content[max(0, cap_start - 200):cap_start] if last_code_end < 0 else content[last_code_end:cap_start]

            # If there's no </pre> or code-output close before this caption
            # (or if the distance is too large), it's orphan
            if last_code_end < 0 or (cap_start - last_code_end > 300):
                orphans.append(el)
            else:
                # This caption consumed the last code block
                last_code_end = -1

    # Also detect consecutive captions (two captions with no code between them)
    prev_caption = None
    for el in elements:
        if el[0] == 'caption':
            if prev_caption is not None:
                # Two consecutive captions; the second is likely a duplicate
                # Keep the one with the longer/better description
                prev_text = prev_caption[3] if len(prev_caption) > 3 else ""
                curr_text = el[3] if len(el) > 3 else ""
                if len(curr_text) > len(prev_text):
                    # Remove the first (shorter) one
                    if prev_caption not in orphans:
                        orphans.append(prev_caption)
                else:
                    # Remove the second (shorter) one
                    if el not in orphans:
                        orphans.append(el)
            prev_caption = el
        elif el[0] in ('pre_close', 'output'):
            prev_caption = None

    issues = len(orphans)

    if not fix:
        for el in orphans:
            cap_text = el[3][:80] if len(el) > 3 else "?"
            line = content[:el[1]].count('\n') + 1
            print(f"    L{line}: {cap_text}")
    else:
        # Remove orphans in reverse order
        for el in sorted(orphans, key=lambda e: e[1], reverse=True):
            # Remove the caption and surrounding whitespace
            start = el[1]
            end = el[2]
            # Extend to eat preceding newline
            while start > 0 and content[start - 1] in '\n\r':
                start -= 1
            content = content[:start] + content[end:]

        if content != original:
            filepath.write_text(content, encoding="utf-8")

    return issues


def main():
    fix = '--fix' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    total = 0
    files_affected = 0

    for f in all_files:
        count = process_file(f, fix=fix)
        if count > 0:
            files_affected += 1
            total += count
            rel = f.relative_to(BOOK_ROOT)
            action = "CLEANED" if fix else "found"
            print(f"  {action}: {rel} ({count} orphan captions)")

    print(f"\n{'='*60}")
    print(f"Orphan captions: {total} across {files_affected} files")
    print(f"Scanned: {len(all_files)} files")
    if not fix and total > 0:
        print(f"\nRun with --fix to remove orphan captions.")


if __name__ == "__main__":
    main()
