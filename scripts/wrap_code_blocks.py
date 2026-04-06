"""
Wrap code blocks (pre + optional code-output + code-caption) in a unified
<div class="code-block-wrapper"> container.

This ensures code, output, and caption are always grouped as a single
structural unit, preventing ordering bugs and orphaned elements.

The structure after wrapping:
  <div class="code-block-wrapper">
    <pre><code>...</code></pre>
    <div class="code-output">...</div>     <!-- optional -->
    <div class="code-caption">...</div>    <!-- optional -->
  </div>

Usage:
  python wrap_code_blocks.py          # Dry run
  python wrap_code_blocks.py --fix    # Apply
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Match a code block followed by optional output and optional caption.
# The regex captures the full group that should be wrapped.
CODE_GROUP_RE = re.compile(
    r'(?P<pre><pre[^>]*>(?:<code[^>]*>)?.*?(?:</code>)?</pre>)'  # the <pre> block
    r'(?P<after_pre>\s*)'                                          # whitespace
    r'(?:'                                                         # optional output
        r'(?P<output><div class="code-output">.*?</div>)'
        r'(?P<after_output>\s*)'
    r')?'
    r'(?:'                                                         # optional caption
        r'(?P<caption><div class="code-caption">.*?</div>)'
    r')?',
    re.DOTALL
)

WRAPPER_OPEN = '<div class="code-block-wrapper">'
WRAPPER_CLOSE = '</div>'


def process_file(filepath, fix=False):
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Skip if already wrapped (check for any existing wrapper)
    if 'code-block-wrapper' in content:
        # Count how many pre blocks are already wrapped vs not
        pass

    # Find all code groups
    matches = list(CODE_GROUP_RE.finditer(content))

    wraps_needed = 0
    insertions = []  # (start, end, replacement)

    for m in matches:
        pre = m.group('pre')
        if not pre:
            continue

        # Skip very short code (inline snippets)
        clean = re.sub(r'<[^>]+>', '', pre).strip()
        if len(clean) < 20:
            continue

        full_match = m.group(0)
        start = m.start()
        end = m.end()

        # Check if already inside a code-block-wrapper
        preceding = content[max(0, start - 100):start]
        if 'code-block-wrapper' in preceding:
            # More precise check: find last opening tag
            open_pos = preceding.rfind('code-block-wrapper')
            # Check we haven't closed it yet
            between_snippet = preceding[open_pos:]
            if between_snippet.count('</div>') < 1:
                continue  # Already wrapped

        # Check if inside a callout (keep code inside callouts as-is)
        # Actually, we SHOULD wrap these too for consistency
        # But skip if inside details.code-collapse (already processed by book.js)

        output = m.group('output') or ''
        caption = m.group('caption') or ''

        # Build the wrapped version
        parts = [pre]
        if output:
            parts.append(output)
        if caption:
            parts.append(caption)

        wrapped = WRAPPER_OPEN + '\n' + '\n'.join(parts) + '\n' + WRAPPER_CLOSE

        insertions.append((start, end, wrapped))
        wraps_needed += 1

    if not fix:
        if wraps_needed > 0:
            for start, end, _ in insertions[:5]:
                line = content[:start].count('\n') + 1
                print(f"    L{line}: needs wrapping")
            if wraps_needed > 5:
                print(f"    ... and {wraps_needed - 5} more")
        return wraps_needed

    # Apply in reverse order
    for start, end, replacement in sorted(insertions, key=lambda x: x[0], reverse=True):
        content = content[:start] + replacement + content[end:]

    if content != original:
        filepath.write_text(content, encoding="utf-8")

    return wraps_needed


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
            action = "WRAPPED" if fix else "needs wrapping"
            print(f"  {action}: {rel} ({count} code blocks)")

    print(f"\n{'='*60}")
    print(f"Code blocks to wrap: {total} across {files_affected} files")
    print(f"Scanned: {len(all_files)} files")
    if not fix and total > 0:
        print(f"\nRun with --fix to wrap code blocks.")


if __name__ == "__main__":
    main()
