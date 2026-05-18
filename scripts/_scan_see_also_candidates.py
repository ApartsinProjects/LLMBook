"""Find sections with 3+ prose cross-reference patterns that aren't yet in a See Also callout."""
import re
from pathlib import Path
from collections import defaultdict

root = Path(r'E:/Projects/BookBlogsHome/LLMBook')

PATTERNS = [
    # "see Section 4.5" / "see Chapter 3"
    re.compile(r'(?:^|[^>])see\s+(?:Section|Sections|Chapter|Chapters|Module|Modules|Part|Parts)\s+\d', re.I),
    # "(see Section 4.5)" parenthetical
    re.compile(r'\(see\s+(?:Section|Chapter|Module|Part)\s+\d', re.I),
    # "discussed in Section 4.5"
    re.compile(r'(?:discussed|covered|described|introduced|explored|examined|treated|presented|detailed)\s+in\s+(?:Section|Chapter|Module|Part)\s+\d', re.I),
    # "For more on X, see Section Y"
    re.compile(r'[Ff]or\s+(?:more|details|deeper|further|additional)\s+(?:on|about|coverage)?[^.]{0,40}(?:see|refer\s+to)\s+(?:Section|Chapter|Module|Part)\s+\d', re.I),
    # "refer to Section X.Y"
    re.compile(r'[Rr]efer(?:s)?\s+to\s+(?:Section|Chapter|Module|Part)\s+\d', re.I),
    # Anchor link with "see" preceding: see <a href="...">Section X.Y</a>
    re.compile(r'see\s+<a\s+href="[^"]+"[^>]*>(?:Section|Chapter|Module|Part)\s+\d', re.I),
    # (see <a>Section X</a>)
    re.compile(r'\(see\s+<a\s+href="[^"]+"[^>]*>(?:Section|Chapter|Module|Part)\s+\d', re.I),
]

def is_skip(path: Path) -> bool:
    sep = chr(92)
    s = str(path).lower().replace(sep, '/')
    if '.book-update' in s:
        return True
    if 'tools-of-the-trade' in s:
        return True
    if '/appendices/' in s:
        return True
    if '/front-matter/' in s:
        return True
    if path.name == 'index.html':
        return True
    if '/kdp/' in s:
        return True
    if '/scripts/' in s:
        return True
    if '/node_modules/' in s:
        return True
    if '/_concept-figs/' in s:
        return True
    if '/templates/' in s:
        return True
    if '/temp_epub/' in s:
        return True
    if '/docs/' in s:
        return True
    if '/agents/' in s:
        return True
    return False

opens_cross_ref_re = re.compile(r'<div class="callout cross-ref">')


def strip_cross_refs(html):
    out = []
    i = 0
    div_open = re.compile(r'<div\b', re.I)
    div_close = re.compile(r'</div>', re.I)
    while i < len(html):
        m = opens_cross_ref_re.search(html, i)
        if not m:
            out.append(html[i:])
            break
        out.append(html[i:m.start()])
        depth = 1
        j = m.end()
        while depth > 0 and j < len(html):
            no = div_open.search(html, j)
            nc = div_close.search(html, j)
            if not nc:
                break
            if no and no.start() < nc.start():
                depth += 1
                j = no.end()
            else:
                depth -= 1
                j = nc.end()
        i = j
    return ''.join(out)


def main():
    candidates = {}
    for p in root.rglob('*.html'):
        if is_skip(p):
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        stripped = strip_cross_refs(text)
        count = 0
        for pat in PATTERNS:
            count += len(pat.findall(stripped))
        if count >= 2:
            candidates[p] = count

    items = sorted(candidates.items(), key=lambda kv: -kv[1])
    for p, c in items[:120]:
        print(c, str(p).replace(str(root) + chr(92), ''))
    print('Total candidate files:', len(items))


if __name__ == '__main__':
    main()
