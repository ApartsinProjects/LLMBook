"""For each candidate section file, print the cross-reference patterns and bibliography placement."""
import re
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r'(?:^|[^>])(see\s+(?:Section|Sections|Chapter|Chapters|Module|Modules|Part|Parts)\s+\d[\d.]*[^.,()]{0,60})', re.I), "see-prose"),
    (re.compile(r'(\(see\s+(?:Section|Chapter|Module|Part)\s+\d[\d.]*[^).]{0,80}\))', re.I), "paren-see"),
    (re.compile(r'((?:discussed|covered|described|introduced|explored|examined|treated|presented|detailed)\s+in\s+(?:Section|Chapter|Module|Part)\s+\d[\d.]*[^.,]{0,60})', re.I), "discussed-in"),
    (re.compile(r'([Ff]or\s+(?:more|details|deeper|further|additional)\s+(?:on|about|coverage)?[^.]{0,40}(?:see|refer\s+to)\s+(?:Section|Chapter|Module|Part)\s+\d[\d.]*[^.,]{0,60})', re.I), "for-more"),
    (re.compile(r'([Rr]efer(?:s)?\s+to\s+(?:Section|Chapter|Module|Part)\s+\d[\d.]*[^.,]{0,60})', re.I), "refer-to"),
    (re.compile(r'(see\s+<a\s+href="[^"]+"[^>]*>(?:Section|Chapter|Module|Part)\s+\d[\d.]*[^<]{0,60}</a>[^.,]{0,40})', re.I), "see-link"),
    (re.compile(r'(\(see\s+<a\s+href="[^"]+"[^>]*>(?:Section|Chapter|Module|Part)\s+\d[\d.]*[^<]{0,60}</a>[^).]{0,40}\))', re.I), "paren-see-link"),
]

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


def main(target):
    p = Path(target)
    text = p.read_text(encoding='utf-8')
    stripped = strip_cross_refs(text)
    print(f"=== {p} ===")
    for pat, label in PATTERNS:
        for m in pat.finditer(stripped):
            snippet = m.group(1)
            # context
            idx = m.start()
            ctx = stripped[max(0, idx - 60):min(len(stripped), idx + 200)]
            print(f"  [{label}] {snippet.strip()[:150]!r}")
    # Check if has bibliography section
    has_bib = bool(re.search(r'<h[23][^>]*>(?:Bibliography|References)', text, re.I))
    print(f"  has-bibliography: {has_bib}")
    # Check if has any existing See Also callout
    has_see_also = bool(re.search(r'<div class="callout cross-ref">', text))
    print(f"  has-existing-see-also: {has_see_also}")


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        main(arg)
