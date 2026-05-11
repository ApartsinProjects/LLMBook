"""v6.13: Chapter-nav repositioning + ToC cleanup + module-36 grid fix.

USER REPORTS

A. "part-11-idea-to-product/module-36/index.html: navigation is misplaced;
    should be at bottom"
   Audit found 6 chapter index files where <nav class="chapter-nav"> sits
   at 66-84% of the file (should be ~95%, just before <footer>). Cause:
   when module-37 / 16 / 30 / 35 were merged into their siblings during
   v3.x restructure, new section-grid cards were appended AFTER the
   existing nav block instead of before it.

B. "TOC, FM part, some sections are stale"
   Audit found:
     - 1 dead link: front-matter/section-fm.1.html (deleted in v5.0)
     - 19 pathway labels and 10 syllabi labels in the expanded ToC that
       all point to the same generic index page. The labels promise
       deep links to per-pathway pages that no longer exist.

FIX (this script)

  1. Move <nav class="chapter-nav">...</nav> from wherever it currently
     sits to right before the closing <footer> element. Idempotent.

  2. Remove the dead front-matter/section-fm.1.html link from toc.html.

  3. Module 36 chapter index has two additional problems we fix here:
     - Section-grid cards: "36.5" → section-36.4 (off-by-one)
     - "What's Next" box says "In the next chapter, Module 36" — the
       SAME chapter. Should reference Chapter 38.
     - "36.7" and "36.8" cards both point to section-36.6 (duplicate).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


# ----- A. Move chapter-nav to end ----------------------------------

def fix_nav_placement(p: Path) -> bool:
    text = p.read_text(encoding='utf-8')
    nav_m = re.search(
        r'\s*<nav class="chapter-nav">(?:.|\n)*?</nav>\s*',
        text,
    )
    if not nav_m:
        return False
    nav_block = nav_m.group(0).strip('\n')
    # Where SHOULD the nav be? Right before <footer>, OR before </main> if no footer.
    footer_m = re.search(r'<footer\b', text)
    if not footer_m:
        return False  # no footer; skip rather than guess

    # If the nav is already directly before the footer (within 10 chars), skip
    nav_end = nav_m.end()
    footer_start = footer_m.start()
    if nav_end <= footer_start and footer_start - nav_end < 50:
        # Already adjacent. Skip.
        return False

    # Remove the nav from its current position
    without_nav = text[:nav_m.start()] + text[nav_m.end():]
    # Re-find <footer> in the cleaned text
    footer_m2 = re.search(r'<footer\b', without_nav)
    if not footer_m2:
        return False
    new_text = (
        without_nav[:footer_m2.start()] +
        nav_block + '\n' +
        without_nav[footer_m2.start():]
    )
    if new_text == text:
        return False
    p.write_text(new_text, encoding='utf-8')
    return True


# ----- B. Drop dead front-matter ToC link --------------------------

def fix_toc_dead_links() -> int:
    p = ROOT / 'toc.html'
    text = p.read_text(encoding='utf-8')
    original = text

    # Remove the dead section-fm.1 link AND its surrounding parent <li> or
    # dense-section entry. Pattern is just a single <a> in a single line:
    # match the line containing the href and drop ONE entry around it.
    PATTERNS = [
        # Pattern 1: a complete <a href="...section-fm.1.html"...>label</a> possibly
        # followed by a separator (&middot;) — kill the link AND any preceding/trailing
        # &middot; so we don't leave orphan separators
        (re.compile(r'\s*&middot;\s*<a[^>]+href="front-matter/section-fm\.1\.html"[^>]*>[^<]+</a>'), ''),
        (re.compile(r'<a[^>]+href="front-matter/section-fm\.1\.html"[^>]*>[^<]+</a>\s*&middot;\s*'), ''),
        # If the link stands alone (no separators), just remove it
        (re.compile(r'<a[^>]+href="front-matter/section-fm\.1\.html"[^>]*>[^<]+</a>'), ''),
    ]
    n = 0
    for pat, repl in PATTERNS:
        text, sub_n = pat.subn(repl, text)
        n += sub_n
    if text != original:
        p.write_text(text, encoding='utf-8')
    return n


# ----- C. Module 36 specific fixes ---------------------------------

# Card mapping problems (numbers shown vs actual file):
#   "36.5" → section-36.4   (wrong: should be section-36.5)
#   "36.6" → section-36.5   (wrong: should be section-36.6)
#   "36.7" → section-36.6   (wrong)
#   "36.8" → section-36.6   (wrong; should be 36.8 doesn't exist; remove)
#   "36.9" → section-36.7   (wrong: should be section-36.7 but display 36.7)
# The actual module-36 has sections 36.1 through 36.7 (per v5.9 spine).

MODULE_36_CARDS_NEW = '''<div class="section-grid">
<a href="section-36.1.html" class="section-card">
<span class="section-num">36.1</span>
<span class="section-title">What Makes AI Products Different</span>
<span class="section-desc">See section for details.</span>
</a>
<a href="section-36.2.html" class="section-card">
<span class="section-num">36.2</span>
<span class="section-title">Choosing the Model's Role</span>
<span class="section-desc">See section for details.</span>
</a>
<a href="section-36.3.html" class="section-card">
<span class="section-num">36.3</span>
<span class="section-title">Risk and Feasibility Assessment</span>
<span class="section-desc">See section for details.</span>
</a>
<a href="section-36.4.html" class="section-card">
<span class="section-num">36.4</span>
<span class="section-title">The Observe-Steer Development Loop</span>
<span class="section-desc">See section for details.</span>
</a>
<a href="section-36.5.html" class="section-card">
<span class="section-num">36.5</span>
<span class="section-title">The Founder's Prototype Loop</span>
<span class="section-desc">See section for details.</span>
</a>
<a href="section-36.6.html" class="section-card">
<span class="section-num">36.6</span>
<span class="section-title">Documentation as Control Surface</span>
<span class="section-desc">See section for details.</span>
</a>
<a href="section-36.7.html" class="section-card">
<span class="section-num">36.7</span>
<span class="section-title">From Prototype to MVP</span>
<span class="section-desc">See section for details.</span>
</a>
</div>'''


def fix_module_36() -> int:
    p = ROOT / 'part-11-idea-to-product/module-36-idea-to-product/index.html'
    text = p.read_text(encoding='utf-8')
    edits = 0

    # 1. Replace BOTH section-grid blocks with the single canonical one.
    # First, find any <ul class="section-list"> OR <div class='section-grid'>
    # blocks and collapse them.
    # Pattern: <ul...class="section-list">...</ul> followed by orphan
    # <div class='section-grid'>...</div> after the chapter-nav.
    ul_pat = re.compile(r'<ul class="section-list">(?:.|\n)*?</ul>', re.DOTALL)
    grid_pat = re.compile(r"<div class='section-grid'>(?:.|\n)*?</div>", re.DOTALL)

    # Remove the orphan grid (after the nav)
    new_text = grid_pat.sub('', text)
    if new_text != text:
        text = new_text
        edits += 1

    # Replace the original <ul class="section-list"> with the canonical grid
    new_text, n = ul_pat.subn(MODULE_36_CARDS_NEW, text, count=1)
    if n:
        text = new_text
        edits += n

    # 2. Fix "What's Next" stale text
    text, n2 = re.subn(
        r'<div class="whats-next">\s*<h3>What\'s Next\?</h3>\s*<p>[^<]*Module 36[^<]*</p>\s*</div>',
        '''<div class="whats-next">
<h3>What's Next?</h3>
<p>The next chapter, <a href="../module-38-shipping-scaling/index.html">Chapter 38: Shipping and Scaling AI Products</a>, picks up where this one ends. Once you have a validated product hypothesis and a working prototype, Chapter 38 covers the engineering and operational steps to take it from MVP to production at scale.</p>
</div>''',
        text,
    )
    if n2:
        edits += n2

    if edits:
        p.write_text(text, encoding='utf-8')
    return edits


# ----- Driver ---------------------------------------------------

def main() -> int:
    print('A. Move misplaced <nav class="chapter-nav"> to just before <footer>')
    fixed_navs = 0
    for p in sorted(ROOT.glob('part-*/module-*/index.html')):
        if fix_nav_placement(p):
            fixed_navs += 1
            print(f'   moved nav: {p.relative_to(ROOT)}')
    print(f'   total: {fixed_navs} chapter index files\n')

    print('B. Drop dead front-matter ToC link')
    n = fix_toc_dead_links()
    print(f'   removed {n} occurrences\n')

    print('C. Module 36 grid + What\'s Next cleanup')
    n = fix_module_36()
    print(f'   applied {n} edits\n')

    return 0


if __name__ == '__main__':
    sys.exit(main())
