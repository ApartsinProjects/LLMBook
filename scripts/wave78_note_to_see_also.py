"""Wave 78: Convert note callouts that ARE See Also content into cross-ref
callouts.

Pattern: <div class="callout note"> whose body contains:
  - Phrase "covered in detail", "covered in depth", "treated more thoroughly",
    "see Section X.Y", "see Chapter N", "see Module N", "for the deep dive"
  - AND at least one <a href> link

User example (42.12): title "Note: Covered in Detail" + body "For a
comprehensive discussion ... see Module 4". This IS a See Also; should be
class="callout cross-ref" with title "See Also".
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Trigger phrases that indicate a See Also intent
TRIGGER_RE = re.compile(
    r'\b(?:covered\s+in\s+detail|covered\s+in\s+depth|treated\s+more\s+thoroughly|'
    r'discussed\s+at\s+length|for\s+the\s+deep\s+dive|for\s+the\s+full\s+treatment|'
    r'see\s+(?:Section|Chapter|Module|Appendix|Part)\s+[\dA-Z])',
    re.IGNORECASE,
)
NOTE_OPEN_RE = re.compile(r'<div\s+class="callout note"([^>]*)>', re.IGNORECASE)


def _find_balanced_div_close(text: str, open_end: int) -> int:
    """Given pos right after `<div ...>` opener, return pos just past matching </div>."""
    depth = 1
    pos = open_end
    while pos < len(text) and depth > 0:
        o = text.find('<div', pos)
        c = text.find('</div>', pos)
        if c == -1:
            return -1
        if o != -1 and o < c:
            depth += 1
            pos = o + 4
        else:
            depth -= 1
            pos = c + 6
            if depth == 0:
                return pos
    return -1


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    orig = text
    n = 0
    # Iterate openings; for each, check body for trigger phrase + <a href>
    out = []
    pos = 0
    for m in NOTE_OPEN_RE.finditer(text):
        end = _find_balanced_div_close(text, m.end())
        if end == -1:
            continue
        body = text[m.end():end - len('</div>')]
        # Trigger? must have trigger phrase AND at least one <a href>
        if TRIGGER_RE.search(body) and '<a href=' in body.lower():
            # Convert class to cross-ref AND rewrite title to "See Also"
            new_block = (
                '<div class="callout cross-ref"' + m.group(1) + '>'
                + re.sub(
                    r'<div\s+class="callout-title"[^>]*>[^<]+</div>',
                    '<div class="callout-title">See Also</div>',
                    body,
                    count=1,
                )
                + '</div>'
            )
            out.append(text[pos:m.start()])
            out.append(new_block)
            pos = end
            n += 1
    out.append(text[pos:])
    new = ''.join(out)
    if new != orig:
        p.write_text(new, encoding='utf-8')
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
    print(f'note callouts converted to cross-ref (See Also): {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
