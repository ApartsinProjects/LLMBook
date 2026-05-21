"""Two bulk auto-fixes:

1. CODE_OUTPUT_OUTSIDE_WRAPPER:
   Move <div class="code-output"> inside the preceding code-block-wrapper.
   Canonical order: <pre><code></code></pre> <div code-output> <div code-caption> </div code-block-wrapper>

2. ALGORITHM_NO_NUMBERING:
   For each <div class="callout algorithm"> with title lacking
   "Algorithm X.Y.Z:" prefix, prepend it. Derive X.Y from the section
   file name; pick Z as next available integer for that section.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ===== Fix 1: code-output inside wrapper =====

def fix_code_output_position(text: str) -> tuple[str, int]:
    """Move <div class="code-output">...</div> that appears immediately
    after a code-block-wrapper closing </div> INSIDE the wrapper,
    placed BEFORE the closing </div> and BEFORE the code-caption."""
    fixed = 0
    # Pattern: <div class="code-block-wrapper">...</div>\s*<div class="code-output">...</div>
    # Capture wrapper contents and the orphan output.
    # Use greedy-balanced-ish matching: assume wrapper ends at the first
    # </div> that returns depth to 0.
    # Iterative depth-counted approach:
    i = 0
    out_parts = []
    while True:
        wrap_start = text.find('<div class="code-block-wrapper">', i)
        if wrap_start == -1:
            out_parts.append(text[i:])
            break
        # Find matching close
        depth = 1
        j = wrap_start + len('<div class="code-block-wrapper">')
        while j < len(text) and depth > 0:
            o = text.find('<div', j)
            c = text.find('</div>', j)
            if c == -1:
                break
            if o != -1 and o < c:
                depth += 1
                j = o + 4
            else:
                depth -= 1
                j = c + 6
        if depth != 0:
            # malformed; bail
            out_parts.append(text[i:])
            break
        wrap_end = j  # past closing </div>
        # Check if a <div class="code-output"> follows
        after_ws = re.match(r'\s*', text[wrap_end:])
        gap_end = wrap_end + after_ws.end()
        out_token = text[gap_end:gap_end + 50]
        m = re.match(r'<div\s+class="code-output[\s"]', out_token)
        if not m:
            # No orphan output; keep as is
            out_parts.append(text[i:wrap_end])
            i = wrap_end
            continue
        # Find end of the output div
        op_depth = 1
        k = gap_end + len('<div class="code-output">')
        # Adjust for class string variants
        k = text.find('>', gap_end) + 1
        while k < len(text) and op_depth > 0:
            o = text.find('<div', k)
            c = text.find('</div>', k)
            if c == -1:
                break
            if o != -1 and o < c:
                op_depth += 1
                k = o + 4
            else:
                op_depth -= 1
                k = c + 6
        if op_depth != 0:
            out_parts.append(text[i:wrap_end])
            i = wrap_end
            continue
        output_end = k
        # Extract the wrapper body and the output
        wrapper_body = text[wrap_start:wrap_end - len('</div>')]
        output_block = text[gap_end:output_end].rstrip() + '\n'
        # Within wrapper_body, find the position to insert the output:
        # AFTER </pre>, BEFORE any <div class="code-caption">
        body_inner = wrapper_body[len('<div class="code-block-wrapper">'):]
        pre_close = body_inner.find('</pre>')
        if pre_close == -1:
            out_parts.append(text[i:wrap_end])
            i = wrap_end
            continue
        pre_close += len('</pre>')
        # Insert output after </pre>
        new_inner = body_inner[:pre_close] + '\n' + output_block + body_inner[pre_close:].lstrip()
        new_wrapper = '<div class="code-block-wrapper">' + new_inner + '</div>'
        out_parts.append(text[i:wrap_start])
        out_parts.append(new_wrapper)
        # Skip past the orphan output (already merged in)
        i = output_end
        fixed += 1
    return ''.join(out_parts), fixed


# ===== Fix 2: algorithm numbering =====

ALG_RE = re.compile(
    r'<div\s+class="callout\s+algorithm"[^>]*>\s*<div\s+class="callout-title"[^>]*>([^<]+)</div>',
    re.IGNORECASE | re.DOTALL,
)
NUMBERED_RE = re.compile(r'^Algorithm\s+\d+\.\d+(?:\.\d+)?[a-z]?:\s+\S', re.IGNORECASE)


def section_number_from_path(filepath: Path) -> str | None:
    m = re.search(r'section-(\d+\.\d+[a-z]?)\.html$', filepath.name)
    if m:
        # Strip letter suffix for the algo number scope (a/b paired sections
        # share algorithm numbering)
        return re.sub(r'[a-z]$', '', m.group(1))
    return None


def fix_algorithm_numbering(text: str, filepath: Path) -> tuple[str, int]:
    sec = section_number_from_path(filepath)
    if not sec:
        return text, 0
    # Find existing "Algorithm X.Y.Z" numbers already in this file
    existing = set()
    for m in re.finditer(r'Algorithm\s+(\d+\.\d+\.\d+)', text):
        existing.add(m.group(1))
    # next available counter for this section
    next_n = 1
    while f'{sec}.{next_n}' in existing:
        next_n += 1

    fixed = 0
    parts = []
    last = 0
    for m in ALG_RE.finditer(text):
        title = m.group(1).strip()
        if NUMBERED_RE.match(title):
            continue
        # Build the new title with Algorithm X.Y.Z: prefix
        new_label = f'{sec}.{next_n}'
        existing.add(new_label)
        next_n += 1
        new_title = f'Algorithm {new_label}: {title}'
        # Splice
        # Find exact title text range to replace within the original match
        title_start = m.start(1)
        title_end = m.end(1)
        parts.append(text[last:title_start])
        parts.append(new_title)
        last = title_end
        fixed += 1
    parts.append(text[last:])
    return ''.join(parts), fixed


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY' if apply else 'DRY-RUN'}")
    co_total = 0
    al_total = 0
    co_files = 0
    al_files = 0
    for f in ROOT.rglob('*.html'):
        if any(s in f.parts for s in ('_archive', 'node_modules', '.git',
                                       'pagefind', 'KDP', 'build', 'vendor',
                                       '.claude', '__pycache__', 'templates')):
            continue
        text = f.read_text(encoding='utf-8')
        orig = text
        text, co = fix_code_output_position(text)
        text, al = fix_algorithm_numbering(text, f)
        if text != orig:
            if co:
                co_total += co
                co_files += 1
                print(f'  CO {f.relative_to(ROOT)}: {co}')
            if al:
                al_total += al
                al_files += 1
                print(f'  AL {f.relative_to(ROOT)}: {al}')
            if apply:
                f.write_text(text, encoding='utf-8')

    print(f'\nCode-output position fixes: {co_total} ({co_files} files)')
    print(f'Algorithm numbering fixes: {al_total} ({al_files} files)')


if __name__ == '__main__':
    main()
