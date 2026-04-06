"""
Add captions to code-block-wrappers that are missing them.

Works with the new structure:
  <div class="code-block-wrapper">
    <pre><code>...</code></pre>
    <div class="code-output">...</div>     <!-- optional -->
    <div class="code-caption">...</div>    <!-- MUST exist -->
  </div>

Generates caption from the code's first comment line, function/class names,
or import statements.

Usage:
  python fix_missing_captions_v2.py          # Dry run
  python fix_missing_captions_v2.py --fix    # Apply
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

TAG_RE = re.compile(r'<[^>]+>')

CODE_RE = re.compile(r'<pre[^>]*>(?:<code[^>]*>)?(.*?)(?:</code>)?</pre>', re.DOTALL)

WRAPPER_OPEN = '<div class="code-block-wrapper">'


def strip_html(text):
    return TAG_RE.sub('', text).strip()


def find_wrapper_spans(content):
    """Find all code-block-wrapper spans using proper div depth counting."""
    spans = []
    search_start = 0
    while True:
        idx = content.find(WRAPPER_OPEN, search_start)
        if idx == -1:
            break
        # Count div depth to find matching </div>
        depth = 0
        pos = idx
        end = -1
        while pos < len(content):
            if content[pos:pos+4] == '<div':
                depth += 1
            elif content[pos:pos+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end = pos + 6
                    break
            pos += 1
        if end != -1:
            spans.append((idx, end))
        search_start = end if end != -1 else idx + 1
    return spans


def extract_description(code_text):
    """Extract a meaningful description from code content."""
    clean = strip_html(code_text)
    lines = clean.split('\n')

    # Try first comment line
    for line in lines[:5]:
        line = line.strip()
        if line.startswith('#') and len(line) > 10:
            desc = line.lstrip('#').strip()
            if desc.lower() not in ('example', 'code', 'test', 'setup', '!pip install', '---'):
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
        libs = list(dict.fromkeys([i.split('.')[0] for i in imports[:4]]))
        return f"Working with {', '.join(libs)}"

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

    # Count existing captions to know the next number
    existing_captions = re.findall(
        r'Code Fragment ' + re.escape(sec_prefix) + r'\.(\d+)',
        content
    )
    next_num = max([int(n) for n in existing_captions], default=0) + 1

    missing = 0

    # Find all wrapper spans using proper depth counting
    spans = find_wrapper_spans(content)

    # Process in reverse order to preserve positions when inserting
    for start, end in reversed(spans):
        block = content[start:end]

        # Skip if already has caption
        if 'code-caption' in block:
            continue

        # Must have a <pre>
        code_match = CODE_RE.search(block)
        if not code_match:
            continue

        code_text = code_match.group(1)

        # Skip very short code
        if len(strip_html(code_text).strip()) < 20:
            continue

        missing += 1
        desc = extract_description(code_text)

        if not fix:
            line = content[:start].count('\n') + 1
            print(f"  L{line}: [MISSING] {desc[:80]}")
            continue

        caption_num = next_num
        next_num += 1
        caption_html = f'<div class="code-caption"><strong>Code Fragment {sec_prefix}.{caption_num}:</strong> {desc}</div>'

        # Insert caption BEFORE the wrapper's closing </div>
        # The closing </div> is at end-6 to end
        insert_pos = end - 6
        content = content[:insert_pos] + caption_html + '\n' + content[insert_pos:]

    if fix and content != original:
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
        print(f"\nRun with --fix to add captions.")


if __name__ == "__main__":
    main()
