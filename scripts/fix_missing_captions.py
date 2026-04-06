"""
Add captions to code blocks that are missing them.

For each <pre><code> block without a following <div class="code-caption">,
generates a caption from the code's first comment line or function/class names,
and inserts it after the code block (and after code-output if present).

Usage:
  python fix_missing_captions.py          # Dry run
  python fix_missing_captions.py --fix    # Apply
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Match code blocks
CODE_BLOCK_RE = re.compile(
    r'(<pre[^>]*>(?:<code[^>]*>)?)(.*?)(?:</code>)?</pre>',
    re.DOTALL
)
CAPTION_RE = re.compile(r'<div class="code-caption">')
OUTPUT_RE = re.compile(r'<div class="code-output">.*?</div>', re.DOTALL)

TAG_RE = re.compile(r'<[^>]+>')


def strip_html(text):
    return TAG_RE.sub('', text).strip()


def extract_description(code_text):
    """Extract a meaningful description from code content."""
    clean = strip_html(code_text)
    lines = clean.split('\n')

    # Try first comment line
    for line in lines[:5]:
        line = line.strip()
        if line.startswith('#') and len(line) > 10:
            desc = line.lstrip('#').strip()
            # Skip generic comments
            if desc.lower() not in ('example', 'code', 'test', 'setup'):
                return desc[:120]

    # Try function/class names
    funcs = re.findall(r'def\s+(\w+)', clean)
    classes = re.findall(r'class\s+(\w+)', clean)

    if classes:
        return f"Defining {', '.join(classes[:3])}"
    if funcs:
        return f"Implementation of {', '.join(funcs[:3])}"

    # Try imports for context
    imports = re.findall(r'(?:from|import)\s+([\w.]+)', clean)
    if imports:
        libs = [i.split('.')[0] for i in imports[:3]]
        return f"Working with {', '.join(set(libs))}"

    return "Code example"


def process_file(filepath, fix=False):
    content = filepath.read_text(encoding="utf-8")
    original = content

    fname = filepath.stem
    m = re.match(r'section-(\d+)\.(\d+)', fname)
    if not m:
        m = re.match(r'section-([a-z])\.(\d+)', fname)
    if not m:
        return 0

    sec_prefix = f"{m.group(1)}.{m.group(2)}"

    # Find all code blocks and their positions
    blocks = list(CODE_BLOCK_RE.finditer(content))
    if not blocks:
        return 0

    # Count existing captions to know the next number
    existing_captions = re.findall(
        r'Code Fragment ' + re.escape(sec_prefix) + r'\.(\d+)',
        content
    )
    next_num = max([int(n) for n in existing_captions], default=0) + 1

    missing = 0
    insertions = []  # (position, caption_html)

    for block in blocks:
        block_end = block.end()
        code_text = block.group(2)

        # Skip very short code
        if len(strip_html(code_text).strip()) < 20:
            continue

        # Skip if inside a callout (algorithm boxes have their own captions)
        preceding = content[max(0, block.start() - 300):block.start()]
        if 'callout algorithm' in preceding:
            # Check if the algorithm div hasn't been closed yet
            after_callout = preceding.split('callout algorithm')[-1]
            if after_callout.count('</div>') < 2:
                continue

        # Look ahead for code-output then code-caption
        after = content[block_end:block_end + 500]

        # Skip past code-output if present
        insert_pos = block_end
        output_match = OUTPUT_RE.match(after)
        if output_match:
            insert_pos = block_end + output_match.end()
            after = content[insert_pos:insert_pos + 200]

        # Check if a caption follows
        after_stripped = after.lstrip()
        if after_stripped.startswith('<div class="code-caption">'):
            continue  # Already has caption

        # Missing caption!
        missing += 1
        desc = extract_description(code_text)
        caption_num = next_num
        next_num += 1

        caption_html = f'\n<div class="code-caption"><strong>Code Fragment {sec_prefix}.{caption_num}:</strong> {desc}</div>'

        if not fix:
            line = content[:block.start()].count('\n') + 1
            rel = filepath.relative_to(BOOK_ROOT)
            print(f"  L{line}: [MISSING] {desc[:80]}")
        else:
            insertions.append((insert_pos, caption_html))

    if fix and insertions:
        # Apply insertions in reverse order to preserve positions
        for pos, html in sorted(insertions, reverse=True):
            content = content[:pos] + html + content[pos:]

        if content != original:
            filepath.write_text(content, encoding="utf-8")

    return missing


def main():
    fix = '--fix' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    total_missing = 0
    files_with_missing = 0

    for f in all_files:
        missing = process_file(f, fix=fix)
        if missing > 0:
            files_with_missing += 1
            total_missing += missing
            rel = f.relative_to(BOOK_ROOT)
            if not fix:
                print(f"  ({missing} missing in {rel})")
            else:
                print(f"  FIXED: {rel} ({missing} captions added)")

    print(f"\n{'='*60}")
    print(f"Total missing captions: {total_missing}")
    print(f"Files affected: {files_with_missing}")
    print(f"Total files scanned: {len(all_files)}")
    if not fix and total_missing > 0:
        print(f"\nRun with --fix to add placeholder captions.")


if __name__ == "__main__":
    main()
