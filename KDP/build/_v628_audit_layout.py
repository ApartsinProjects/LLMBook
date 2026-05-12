"""v6.28: Audit page layout consistency book-wide.

Checks every section/index page for these problems:
  A) chapter-nav has plain-text middle/next slot (no <a> anchor)
  B) chapter-nav appears AFTER <footer>
  C) Stray content (e.g. <div class='section-grid'>) appears AFTER <footer>
     or after </main>
  D) Page is missing chapter-nav entirely
  E) Page is missing <footer> entirely
"""
from __future__ import annotations
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent

ALL = sorted({
    *ROOT.glob('part-*/module-*/section-*.html'),
    *ROOT.glob('part-*/module-*/index.html'),
    *ROOT.glob('appendices/appendix-*/section-*.html'),
    *ROOT.glob('appendices/appendix-*/index.html'),
    *ROOT.glob('part-*/index.html'),
    *ROOT.glob('appendices/index.html'),
    *ROOT.glob('front-matter/*.html'),
    *ROOT.glob('front-matter/**/index.html'),
})

issues = defaultdict(list)
for p in ALL:
    text = p.read_text(encoding='utf-8', errors='replace')
    rel = str(p.relative_to(ROOT)).replace('\\', '/')

    nav_m = re.search(r'<nav class="chapter-nav">(.*?)</nav>', text, re.DOTALL)
    footer_m = re.search(r'<footer\b', text)

    if not nav_m:
        issues['E_no_nav'].append(rel)
        continue

    if not footer_m:
        issues['F_no_footer'].append(rel)

    # A) nav has all three slots as <a> ?
    nav = nav_m.group(1)
    a_count = len(re.findall(r'<a\s', nav))
    # Strip <a>...</a> blocks; if any text outside whitespace remains, that's plain-text bug
    after_strip = re.sub(r'<a\b[^>]*>.*?</a>', '', nav, flags=re.DOTALL).strip()
    if after_strip:
        # remove tag-only fragments
        after_strip2 = re.sub(r'<[^>]+>', '', after_strip).strip()
        if after_strip2:
            issues['A_plaintext_in_nav'].append(f'{rel}  text={after_strip2[:60]!r}')

    # B) nav AFTER footer?
    if footer_m and nav_m.start() > footer_m.start():
        issues['B_nav_after_footer'].append(rel)

    # C) stray <div class='section-grid'> after footer?
    if footer_m:
        after_footer = text[footer_m.start():]
        if re.search(r"<div class=['\"]section-grid['\"]>", after_footer):
            issues['C_grid_after_footer'].append(rel)
        # also any <main> closing within after_footer is fine; check for orphan content
        # between </footer> and </main> that's not whitespace
        m_close = re.search(r'</footer>(.*?)</main>', after_footer, re.DOTALL)
        if m_close:
            stuff = m_close.group(1).strip()
            if stuff:
                # Strip pure whitespace / comments
                meaningful = re.sub(r'<!--.*?-->', '', stuff, flags=re.DOTALL).strip()
                if meaningful and 'C_grid_after_footer' not in str(issues['C_grid_after_footer'])[-100:]:
                    issues['C2_other_after_footer'].append(f'{rel}  has={meaningful[:50]!r}')

print(f'Audited {len(ALL)} pages.\n')
for code, items in issues.items():
    print(f'== {code}: {len(items)} ==')
    for x in items[:8]:
        print(f'   {x}')
    if len(items) > 8:
        print(f'   ... +{len(items) - 8} more')
    print()
