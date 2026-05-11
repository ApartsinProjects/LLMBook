"""v6.15: Strip decorative pathway/syllabi labels from toc.html.

USER REPORT
"pathway/syllabi decorative ToC labels (19 + 10) all point to a generic page, strip"

ROOT CAUSE
The expanded ToC has `<div class="dense-sections">` blocks under FM.5 (Pathways)
and FM.6 (Syllabi) that list 20 / 9 individual labels respectively — but every
single anchor in those blocks points to the SAME generic landing page
(`front-matter/pathways/index.html` or `front-matter/syllabi/index.html`).

The labels promise per-pathway / per-syllabus deep links that don't exist.
Result: misleading ToC. Click "Build AI Products" or "Grad Engineering" and
you land on the same generic page as "Reading Pathways".

FIX
Detect any `<div class="dense-sections">` whose anchors ALL point to one of
the two generic pages, and remove that entire div. Keep the top-level
"Reading Pathways" / "Course Syllabi" links in the FM.5 / FM.6 chapter rows.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TOC = ROOT / 'toc.html'

GENERIC_TARGETS = {
    'front-matter/pathways/index.html',
    'front-matter/syllabi/index.html',
}


def is_all_generic(div_html: str) -> tuple[bool, str | None]:
    """Return (True, target) if every <a> in div_html points to one generic target."""
    anchors = re.findall(r'<a[^>]+href="([^"]+)"', div_html)
    if not anchors:
        return False, None
    # Strip any in-page fragment
    hrefs = {a.split('#', 1)[0] for a in anchors}
    if len(hrefs) == 1 and next(iter(hrefs)) in GENERIC_TARGETS:
        return True, next(iter(hrefs))
    return False, None


def main() -> int:
    text = TOC.read_text(encoding='utf-8')
    original = text

    # Find each <div class="dense-sections">...</div> block
    pat = re.compile(r'<div class="dense-sections">(.*?)</div>', re.DOTALL)
    removed = {'pathways': 0, 'syllabi': 0}
    label_count = 0

    def repl(m: re.Match) -> str:
        nonlocal label_count
        body = m.group(1)
        ok, target = is_all_generic(body)
        if not ok:
            return m.group(0)
        # Count labels we're removing
        n = len(re.findall(r'<a[^>]+>', body))
        label_count += n
        key = 'pathways' if 'pathways' in target else 'syllabi'
        removed[key] += 1
        return ''  # strip the whole div

    text = pat.sub(repl, text)

    # Collapse any trailing whitespace artifacts (consecutive blank lines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    if text == original:
        print('No changes (already clean).')
        return 0

    TOC.write_text(text, encoding='utf-8')
    print(f'Stripped dense-sections blocks: '
          f'{removed["pathways"]} pathway-block(s), '
          f'{removed["syllabi"]} syllabi-block(s)')
    print(f'Total decorative labels removed: {label_count}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
