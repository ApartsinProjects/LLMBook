"""v6.29: Normalize page layout book-wide.

Apply the canonical layout from PAGE_LAYOUT_STANDARD.md:
  - For each page, ensure: <nav class="chapter-nav"> appears INSIDE <main>
    immediately before <footer>; nothing comes after <footer> except </main>.
  - For appendix index pages, fix plain-text "Appendices" -> proper anchor link
    to appendices/index.html.

Specific fixes:

  Fix B (nav after footer): move <nav class="chapter-nav"> to immediately
    before <footer>. (13 files affected per audit.)

  Fix C (section-grid after footer): move <div class="section-grid"> to
    immediately before <nav class="chapter-nav"> inside <main>. (5 files.)

  Fix A-appendix (appendix index nav has plain-text "Appendices"): wrap in
    <a href="../index.html">Appendices</a>. (~25 files.)

  Fix C2 (other content after footer): move it before nav. (~12 files.)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

ALL_PAGES = sorted({
    *ROOT.glob('part-*/module-*/section-*.html'),
    *ROOT.glob('part-*/module-*/index.html'),
    *ROOT.glob('appendices/appendix-*/section-*.html'),
    *ROOT.glob('appendices/appendix-*/index.html'),
    *ROOT.glob('part-*/index.html'),
    *ROOT.glob('appendices/index.html'),
})


def fix_nav_after_footer(text: str) -> tuple[str, bool]:
    """Fix B: move chapter-nav to immediately before footer."""
    nav_m = re.search(r'\s*<nav class="chapter-nav">.*?</nav>\s*', text, re.DOTALL)
    footer_m = re.search(r'<footer\b', text)
    if not nav_m or not footer_m:
        return text, False
    if nav_m.end() <= footer_m.start():
        return text, False  # already in order
    # Cut nav out, paste before footer
    nav_block = nav_m.group(0).strip('\n')
    without = text[:nav_m.start()] + text[nav_m.end():]
    fm2 = re.search(r'<footer\b', without)
    if not fm2:
        return text, False
    new_text = without[:fm2.start()] + nav_block + '\n' + without[fm2.start():]
    return new_text, True


def fix_orphan_section_grid(text: str) -> tuple[str, bool]:
    """Fix C: move <div class='section-grid'> from after footer to before nav."""
    footer_m = re.search(r'<footer\b', text)
    if not footer_m:
        return text, False
    after = text[footer_m.start():]
    grid_m = re.search(r"\s*<div class=['\"]section-grid['\"]>.*?</div>\s*",
                       after, re.DOTALL)
    if not grid_m:
        return text, False
    grid_block = grid_m.group(0).strip('\n')
    abs_start = footer_m.start() + grid_m.start()
    abs_end = footer_m.start() + grid_m.end()
    without = text[:abs_start] + text[abs_end:]
    # Now place grid before chapter-nav (or before footer if no nav)
    nav_m = re.search(r'<nav class="chapter-nav">', without)
    if nav_m:
        anchor = nav_m.start()
    else:
        fm2 = re.search(r'<footer\b', without)
        if not fm2:
            return text, False
        anchor = fm2.start()
    new_text = without[:anchor] + grid_block + '\n' + without[anchor:]
    return new_text, True


def fix_appendix_plaintext_nav(text: str, p: Path) -> tuple[str, bool]:
    """Fix A-appendix: wrap plain-text 'Appendices' in nav with proper link."""
    rel = str(p).replace('\\', '/')
    if 'appendices/appendix-' not in rel:
        return text, False
    if p.name != 'index.html':
        return text, False
    # Look for nav block
    nav_m = re.search(r'(<nav class="chapter-nav">.*?</nav>)', text, re.DOTALL)
    if not nav_m:
        return text, False
    nav = nav_m.group(1)
    # Find plain-text "Appendices" sandwiched between </a> and <a or </nav>
    # Pattern: </a>\nAppendices\n<a or </a>\nAppendices\n</nav>
    new_nav = re.sub(
        r'(</a>\s*)Appendices(\s*<a)',
        r'\1<a class="up" href="../index.html">Appendices</a>\2',
        nav,
    )
    new_nav = re.sub(
        r'(</a>\s*)Appendices(\s*</nav>)',
        r'\1<a class="up" href="../index.html">Appendices</a>\2',
        new_nav,
    )
    if new_nav == nav:
        return text, False
    return text.replace(nav, new_nav, 1), True


def fix_part_landing_plaintext_nav(text: str, p: Path) -> tuple[str, bool]:
    """Fix A: part landing pages have plain-text nav like:
       <nav class="chapter-nav">
           &larr; Part I: Foundations
           Book Index
           Part III: Working with LLMs &rarr;
       </nav>
    Convert to proper 3-anchor form. Path semantics:
       prev: previous part landing (or front-matter for part 1)
       up:   ../toc.html (Book Index)
       next: next part landing (or appendices for last part)
    """
    rel = str(p).replace('\\', '/')
    # Only part landing pages and appendices/index
    is_part = re.match(r'(?:.*/)?part-\d+-[^/]+/index\.html$', rel)
    is_appendix_root = rel.endswith('/appendices/index.html') or rel.endswith('appendices/index.html')
    is_appendix_idx = '/appendices/appendix-' in rel and p.name == 'index.html'
    is_fm_root = rel.endswith('/front-matter/index.html') or rel.endswith('front-matter/index.html')
    if not (is_part or is_appendix_root or is_fm_root or is_appendix_idx):
        return text, False
    nav_m = re.search(r'<nav class="chapter-nav">(.*?)</nav>', text, re.DOTALL)
    if not nav_m:
        return text, False
    inner = nav_m.group(1)
    # Already has 3 anchors with no plaintext? then OK
    # Strip <a> blocks; if anything left after that is meaningful text (not arrows), it's broken
    stripped = re.sub(r'<a\b[^>]*>.*?</a>', '', inner, flags=re.DOTALL)
    stripped = re.sub(r'&larr;|&rarr;|<[^>]+>', '', stripped).strip()
    if not stripped:
        return text, False
    # Parse the existing labels — split by lines, look for arrow markers
    lines = [l.strip() for l in inner.split('\n') if l.strip()]
    prev_label = up_label = next_label = ''
    for line in lines:
        clean = re.sub(r'<[^>]+>', '', line).strip()
        clean = re.sub(r'&larr;\s*', '', clean)
        clean = re.sub(r'\s*&rarr;', '', clean)
        clean = clean.strip()
        if line.startswith('&larr;') or '&larr;' in line:
            prev_label = clean
        elif '&rarr;' in line:
            next_label = clean
        else:
            up_label = clean
    if not up_label:
        return text, False
    # Decide hrefs based on page type
    if is_part:
        m = re.search(r'part-(\d+)-', rel)
        n = int(m.group(1)) if m else 0
        prev_href = '../toc.html' if n <= 1 else _part_landing_href(n - 1)
        if not prev_label:
            prev_label = 'Front Matter' if n <= 1 else _part_label(n - 1)
        up_href = '../toc.html'
        if n >= 11:
            next_href = '../appendices/index.html'
            if not next_label:
                next_label = 'Appendices'
        else:
            next_href = _part_landing_href(n + 1)
            if not next_label:
                next_label = _part_label(n + 1)
    elif is_appendix_root:
        prev_href = '../part-11-idea-to-product/index.html'
        up_href = '../toc.html'
        next_href = 'appendix-a-mathematical-foundations/index.html'
        if not prev_label: prev_label = 'Part XI: From Idea to AI Product'
        if not next_label: next_label = 'Appendix A: Mathematical Foundations'
    elif is_fm_root:
        prev_href = '../toc.html'
        up_href = '../toc.html'
        next_href = '../part-1-foundations/index.html'
        if not prev_label: prev_label = 'Book Index'
        if not next_label: next_label = 'Part I: Foundations'
    elif is_appendix_idx:
        # appendix-r etc. with multiline nav — leave for now, complex
        return text, False
    else:
        return text, False
    new_nav = (
        '<nav class="chapter-nav">\n'
        f'<a class="prev" href="{prev_href}">{prev_label}</a>\n'
        f'<a class="up" href="{up_href}">{up_label or "Book Index"}</a>\n'
        f'<a class="next" href="{next_href}">{next_label}</a>\n'
        '</nav>'
    )
    new_text = text.replace(nav_m.group(0), new_nav, 1)
    return new_text, new_text != text


def _part_landing_href(n):
    parts = {
        1: '../part-1-foundations/index.html',
        2: '../part-2-understanding-llms/index.html',
        3: '../part-3-working-with-llms/index.html',
        4: '../part-4-training-adapting/index.html',
        5: '../part-5-retrieval-conversation/index.html',
        6: '../part-6-agentic-ai/index.html',
        7: '../part-7-multimodal-applications/index.html',
        8: '../part-8-evaluation-production/index.html',
        9: '../part-9-safety-strategy/index.html',
        10: '../part-10-frontiers/index.html',
        11: '../part-11-idea-to-product/index.html',
    }
    return parts.get(n, '../toc.html')


def _part_label(n):
    labels = {
        1: 'Part I: Foundations',
        2: 'Part II: Understanding LLMs',
        3: 'Part III: Working with LLMs',
        4: 'Part IV: Training and Adapting',
        5: 'Part V: Retrieval and Conversation',
        6: 'Part VI: Agentic AI',
        7: 'Part VII: AI Applications',
        8: 'Part VIII: Evaluation and Production',
        9: 'Part IX: Safety and Strategy',
        10: 'Part X: Frontiers',
        11: 'Part XI: From Idea to AI Product',
    }
    return labels.get(n, 'Book')


def fix_section_plaintext_next(text: str, p: Path) -> tuple[str, bool]:
    """Fix A for section pages: chapter-nav has plain-text 'next' slot
    (no <a> anchor). Build a proper <a class="next"> link by sniffing the
    actual next section in the same module."""
    rel = str(p).replace('/', '/').replace('\\', '/')
    sec_m = re.match(r'.*/section-(\d+)\.(\d+)(?:\.\d+)?\.html$', rel)
    if not sec_m:
        return text, False
    chap = int(sec_m.group(1))
    sec = int(sec_m.group(2))
    nav_m = re.search(r'(<nav class="chapter-nav">)(.*?)(</nav>)', text, re.DOTALL)
    if not nav_m:
        return text, False
    inner = nav_m.group(2)
    # Verify there's plain text remaining after stripping anchors
    stripped = re.sub(r'<a\b[^>]*>.*?</a>', '', inner, flags=re.DOTALL)
    stripped = re.sub(r'<[^>]+>', '', stripped).strip()
    if not stripped:
        return text, False
    # Try to find the next section file
    next_rel = f'section-{chap}.{sec + 1}.html'
    next_path = p.parent / next_rel
    if not next_path.exists():
        return text, False
    # Get its title
    next_title = stripped  # default to the plaintext we found
    try:
        nt = next_path.read_text(encoding='utf-8')
        m = re.search(r'<h1[^>]*>(.+?)</h1>', nt, re.DOTALL)
        if m:
            next_title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    except Exception:
        pass
    # Build new inner: keep existing <a> blocks; replace plaintext with <a class="next">
    # Find all <a> blocks; the plaintext is whatever's after the last </a>
    parts = re.split(r'(<a\b[^>]*>.*?</a>)', inner, flags=re.DOTALL)
    new_parts = []
    plaintext_replaced = False
    for piece in parts:
        if piece.startswith('<a'):
            new_parts.append(piece)
        else:
            # this is interstitial: whitespace + maybe plain text
            cleaned = re.sub(r'<[^>]+>', '', piece).strip()
            if cleaned and not plaintext_replaced:
                anchor = f'<a class="next" href="{next_rel}">{next_title}</a>'
                new_parts.append('\n' + anchor + '\n')
                plaintext_replaced = True
            else:
                new_parts.append(piece)
    if not plaintext_replaced:
        return text, False
    new_inner = ''.join(new_parts)
    new_nav = nav_m.group(1) + new_inner + nav_m.group(3)
    return text.replace(nav_m.group(0), new_nav, 1), True


def fix_stray_after_footer(text: str) -> tuple[str, bool]:
    """Fix C2: orphan </div> or other content between </footer> and </main>.
    Specifically: remove stray </div> right after </footer>."""
    # Common pattern: </footer>\n</div></main>  -- the </div> is stray
    new_text, n = re.subn(r'(</footer>)\s*</div>(\s*</main>)', r'\1\2', text)
    return new_text, n > 0


def main() -> int:
    fix_b = fix_c = fix_a_app = fix_part = fix_stray = fix_sec_next = 0
    for p in ALL_PAGES:
        text = p.read_text(encoding='utf-8')
        original = text
        text, b = fix_nav_after_footer(text)
        if b:
            fix_b += 1
        text, c = fix_orphan_section_grid(text)
        if c:
            fix_c += 1
        text, ax = fix_appendix_plaintext_nav(text, p)
        if ax:
            fix_a_app += 1
        text, pa = fix_part_landing_plaintext_nav(text, p)
        if pa:
            fix_part += 1
        text, sn = fix_section_plaintext_next(text, p)
        if sn:
            fix_sec_next += 1
        text, st = fix_stray_after_footer(text)
        if st:
            fix_stray += 1
        if text != original:
            p.write_text(text, encoding='utf-8')

    print(f'Fix B (nav moved before footer):         {fix_b} files')
    print(f'Fix C (section-grid moved before nav):   {fix_c} files')
    print(f'Fix A (appendix nav wrap "Appendices"):  {fix_a_app} files')
    print(f'Fix part-landing plaintext nav:          {fix_part} files')
    print(f'Fix section plaintext "next" slot:       {fix_sec_next} files')
    print(f'Fix stray </div> after footer:           {fix_stray} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
