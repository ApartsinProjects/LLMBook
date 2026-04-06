"""
Fix caption/output ordering: move code-caption to AFTER code-output.

The correct structure is:
    </pre>
    <div class="code-output">...</div>   (optional)
    <div class="code-caption">...</div>

But many files have the caption BETWEEN the code and its output:
    </pre>
    <div class="code-caption">...</div>   <-- WRONG position
    <div class="code-output">...</div>

This script swaps them to the correct order.

Usage:
  python fix_caption_output_order.py          # Dry run
  python fix_caption_output_order.py --fix    # Apply fixes
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Match: </pre> whitespace caption whitespace output
# Capture the caption and output separately so we can swap them
WRONG_ORDER_RE = re.compile(
    r'(</pre>)'                                          # group 1: closing pre
    r'(\s*\n?\s*)'                                       # group 2: whitespace
    r'(<div class="code-caption">.*?</div>)'             # group 3: caption
    r'(\s*\n?\s*)'                                       # group 4: whitespace
    r'(<div class="code-output">.*?</div>)',             # group 5: output
    re.DOTALL
)


def process_file(filepath, fix=False):
    content = filepath.read_text(encoding="utf-8")
    original = content

    matches = list(WRONG_ORDER_RE.finditer(content))
    count = len(matches)

    if not fix:
        for m in matches:
            line = content[:m.start()].count('\n') + 1
            cap_text = m.group(3)[:80]
            print(f"    L{line}: {cap_text}")
        return count

    # Fix: swap caption and output
    content = WRONG_ORDER_RE.sub(
        r'\1\2\5\4\3',  # pre, ws, OUTPUT, ws, CAPTION
        content
    )

    if content != original:
        filepath.write_text(content, encoding="utf-8")

    return count


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
            action = "FIXED" if fix else "found"
            print(f"  {action}: {rel} ({count} swaps)")

    print(f"\n{'='*60}")
    print(f"Caption/output order issues: {total} across {files_affected} files")
    print(f"Scanned: {len(all_files)} files")
    if not fix and total > 0:
        print(f"\nRun with --fix to swap caption/output to correct order.")


if __name__ == "__main__":
    main()
