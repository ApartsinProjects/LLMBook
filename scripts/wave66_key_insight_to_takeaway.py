"""Wave 66: When a <div class="callout key-insight"> contains a <ul> or <ol>,
reclassify it as <div class="callout key-takeaway">. The new
KEY_INSIGHT_VS_TAKEAWAY audit (added by the image-reuse + visual identity
agent) flags 50 such callouts: key-insight is for a single inline aha
observation; key-takeaway is for bulleted summary boxes.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match a callout key-insight block and check if its body contains <ul> or <ol>
# Need to balance the divs to find the full block.
OPEN_RE = re.compile(r'<div\s+class="callout key-insight"([^>]*)>', re.IGNORECASE)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    orig = text
    n = 0

    # Iterate over openings; for each, find the matching </div> and check inner content
    # We do this with a list of replacements to apply right-to-left.
    replacements: list[tuple[int, int, str]] = []  # (start, end, new_text)

    for m in OPEN_RE.finditer(text):
        # Find balanced </div> close
        pos = m.end()
        depth = 1
        max_chars = 8000
        while pos < len(text) and depth > 0 and pos - m.end() < max_chars:
            next_open = text.find('<div', pos)
            next_close = text.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                pos = next_close + 6
                if depth == 0:
                    break
        if depth != 0:
            continue
        block = text[m.end():pos - len('</div>')]
        # Check if body contains <ul> or <ol> as a child element
        if re.search(r'<(?:ul|ol)\b', block, re.IGNORECASE):
            # Rewrite the OPENING tag's class
            new_open = '<div class="callout key-takeaway"' + m.group(1) + '>'
            replacements.append((m.start(), m.end(), new_open))

    # Apply right-to-left
    if not replacements:
        return 0
    replacements.sort(reverse=True)
    for s, e, repl in replacements:
        text = text[:s] + repl + text[e:]
        n += 1

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
    print(f'key-insight → key-takeaway (contains list): {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
