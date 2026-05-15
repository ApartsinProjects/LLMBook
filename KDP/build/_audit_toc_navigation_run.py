"""Book-wide audit of navigation and Table of Contents links.

Outputs a markdown report covering:
  - Per-page chapter-nav (prev/up/next) presence and target validity
  - Header-nav (book-title + ToC link) presence and target validity
  - ToC entries vs actual section files (both short and detailed views)
  - Title mismatches between ToC entry text and the linked page <title>/<h1>
"""
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import html as htmllib

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
TOC_PATH = ROOT / 'toc.html'
OUT_PATH = ROOT / 'KDP' / 'build' / 'AUDIT_toc_navigation.md'

SKIP_DIRS = {
    'node_modules', '.git', 'pagefind', 'temp_epub', 'backup',
    'source_fix_backups',
}
SKIP_PATH_PREFIXES = [
    'KDP/output', 'KDP/build', 'KDP/html2pub',
    'scripts/_exercise_payloads',
    # The following are not "published" pages but contain template/marketing
    # HTML with placeholders or alternate layouts; excluding to keep the audit
    # focused on the book itself.
    'agents/',
    'templates/',
    'KDP/metadata/',
]


def is_skipped(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    for part in p.parts:
        if part in SKIP_DIRS:
            return True
    for pref in SKIP_PATH_PREFIXES:
        if rel.startswith(pref):
            return True
    return False


def collect_html_pages():
    pages = []
    for p in ROOT.rglob('*.html'):
        if is_skipped(p):
            continue
        pages.append(p)
    return sorted(pages)


def read_soup(p: Path):
    try:
        text = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        text = p.read_text(encoding='utf-8', errors='replace')
    return BeautifulSoup(text, 'html.parser')


def is_section_page(p: Path) -> bool:
    """Section files: section-X.Y.html in module/appendix directories."""
    name = p.name.lower()
    return name.startswith('section-') and name.endswith('.html')


def is_index_or_module(p: Path) -> bool:
    return p.name.lower() == 'index.html'


def resolve_href(page: Path, href: str) -> Path | None:
    if not href:
        return None
    href = href.strip()
    if href.startswith(('http://', 'https://', 'mailto:', 'javascript:')):
        return None
    href_no_frag = href.split('#', 1)[0]
    if not href_no_frag:
        # Pure anchor; treat as same-page link (valid)
        return page
    try:
        target = (page.parent / href_no_frag).resolve()
        return target
    except Exception:
        return None


def get_h1_or_title(soup) -> str:
    h1 = soup.find('h1')
    if h1:
        return h1.get_text(' ', strip=True)
    t = soup.find('title')
    if t:
        return t.get_text(' ', strip=True)
    return ''


def normalize_for_compare(s: str) -> str:
    s = htmllib.unescape(s or '')
    s = re.sub(r'\s+', ' ', s).strip().lower()
    # Strip common decorations
    s = re.sub(r'^(chapter|module|appendix|app|section|ch|fm)\.?\s*[\w.]+[:.\s-]*', '', s)
    s = re.sub(r'^[\d.a-z]+[:.\s-]+', '', s, count=1)
    return s


print('Scanning HTML pages...')
pages = collect_html_pages()
print(f'  found {len(pages)} pages')

# --------------------------------------------------------------------------
# 1. Per-page navigation audits
# --------------------------------------------------------------------------
header_nav_missing = []
header_nav_broken = []  # (page, kind, href, target)
chapter_nav_missing = []
chapter_nav_partial = []  # missing prev/up/next anchors specifically
chapter_nav_broken = []  # (page, kind, href, target)

# Map page -> {prev_resolved, up_resolved, next_resolved}
nav_state = {}
title_index = {}  # resolved path -> h1/title text

# Pre-build title index for every page
for p in pages:
    try:
        soup = read_soup(p)
    except Exception:
        continue
    title_index[p.resolve()] = get_h1_or_title(soup)

for p in pages:
    try:
        soup = read_soup(p)
    except Exception:
        continue
    # Header nav
    hn = soup.find('nav', class_='header-nav')
    if hn is None:
        header_nav_missing.append(p)
    else:
        for a in hn.find_all('a'):
            href = a.get('href', '').strip()
            if not href:
                continue
            tgt = resolve_href(p, href)
            if tgt is not None and not tgt.exists():
                header_nav_broken.append((p, a.get_text(strip=True), href, tgt))
    # Chapter nav: required only on section pages and on module/appendix indexes
    if is_section_page(p) or is_index_or_module(p):
        cn = soup.find('nav', class_='chapter-nav')
        if cn is None:
            # Index pages at the project root or part level may not have one;
            # only flag section pages and module/appendix indexes.
            rel = p.relative_to(ROOT).as_posix()
            is_module_or_appendix_idx = (
                is_index_or_module(p) and (
                    rel.startswith('part-') and '/module-' in rel
                    or rel.startswith('appendices/appendix-')
                    or rel.startswith('capstone/')
                )
            )
            if is_section_page(p) or is_module_or_appendix_idx:
                chapter_nav_missing.append(p)
        else:
            prev_a = cn.find('a', class_='prev')
            up_a = cn.find('a', class_='up')
            next_a = cn.find('a', class_='next')
            missing_anchors = []
            if not prev_a:
                missing_anchors.append('prev')
            if not up_a:
                missing_anchors.append('up')
            if not next_a:
                missing_anchors.append('next')
            if missing_anchors:
                chapter_nav_partial.append((p, missing_anchors))
            for kind, a in (('prev', prev_a), ('up', up_a), ('next', next_a)):
                if not a:
                    continue
                href = a.get('href', '').strip()
                if not href:
                    continue
                tgt = resolve_href(p, href)
                if tgt is None:
                    continue
                if not tgt.exists():
                    chapter_nav_broken.append((p, kind, href, tgt))
            nav_state[p.resolve()] = {
                'prev': resolve_href(p, prev_a['href']) if prev_a and prev_a.get('href') else None,
                'up':   resolve_href(p, up_a['href'])   if up_a   and up_a.get('href')   else None,
                'next': resolve_href(p, next_a['href']) if next_a and next_a.get('href') else None,
            }

# Reciprocity check (warn-level)
asymmetric = []
for src, refs in nav_state.items():
    nxt = refs['next']
    if nxt and nxt in nav_state:
        back = nav_state[nxt]['prev']
        if back and back.resolve() != src.resolve():
            asymmetric.append(('next/prev', src, nxt, back))
    prv = refs['prev']
    if prv and prv in nav_state:
        fwd = nav_state[prv]['next']
        if fwd and fwd.resolve() != src.resolve():
            asymmetric.append(('prev/next', src, prv, fwd))

# --------------------------------------------------------------------------
# 2. ToC audit
# --------------------------------------------------------------------------
toc_soup = read_soup(TOC_PATH)
toc_entries = []  # (view, href_resolved, anchor_text, label)

for view_id, view in (('short', toc_soup.find(id='toc-short')),
                      ('detailed', toc_soup.find(id='toc-detailed'))):
    if view is None:
        continue
    for a in view.find_all('a'):
        href = a.get('href', '').strip()
        if not href or href.startswith(('http://', 'https://')):
            continue
        target = resolve_href(TOC_PATH, href)
        text = a.get_text(' ', strip=True)
        # Find optional chip badge (dense-ch-num) preceding this anchor in
        # the same dense-chapter div
        parent = a.find_parent('div', class_='dense-chapter')
        chip = ''
        if parent:
            chip_span = parent.find('span', class_='dense-ch-num')
            if chip_span:
                chip = chip_span.get_text(strip=True)
        toc_entries.append((view_id, href, target, text, chip))

# Broken ToC links
toc_broken = [(v, h, tgt, txt, chip) for (v, h, tgt, txt, chip) in toc_entries
              if tgt is not None and not tgt.exists()]

# Index ToC targets by resolved path for cross-checking
toc_targets = {e[2].resolve() for e in toc_entries
               if e[2] is not None and e[2].exists()}

# Find section files not referenced anywhere in the ToC
unreferenced_sections = []
for p in pages:
    if not is_section_page(p):
        continue
    if p.resolve() not in toc_targets:
        unreferenced_sections.append(p)

# Find module/appendix indexes not in ToC
unreferenced_indexes = []
for p in pages:
    rel = p.relative_to(ROOT).as_posix()
    if not is_index_or_module(p):
        continue
    is_module_idx = '/module-' in rel and rel.endswith('/index.html')
    is_appendix_idx = rel.startswith('appendices/appendix-') and rel.endswith('/index.html')
    if not (is_module_idx or is_appendix_idx):
        continue
    if p.resolve() not in toc_targets:
        unreferenced_indexes.append(p)

# Title mismatches: compare the ToC anchor text against the linked page's h1
# Allow a generous match (substring after normalization).
title_mismatches = []
for view_id, href, target, txt, chip in toc_entries:
    if target is None or not target.exists():
        continue
    page_title = title_index.get(target.resolve(), '')
    if not page_title:
        continue
    norm_toc = normalize_for_compare(txt)
    norm_page = normalize_for_compare(page_title)
    if not norm_toc or not norm_page:
        continue
    # Accept if either contains the other (handles "X.Y Foo" vs "Foo")
    if norm_toc in norm_page or norm_page in norm_toc:
        continue
    # Lightweight token overlap fallback (avoid noise from tiny differences)
    set_toc = set(re.findall(r'\w{3,}', norm_toc))
    set_page = set(re.findall(r'\w{3,}', norm_page))
    if set_toc and set_page and len(set_toc & set_page) / max(1, len(set_toc)) >= 0.6:
        continue
    title_mismatches.append((view_id, href, txt, page_title, chip))

# --------------------------------------------------------------------------
# 3. Header nav target audit specifics: ToC + book-title-link targets exist
# --------------------------------------------------------------------------
# (Already done via header_nav_broken collection above; surface a tally.)

# --------------------------------------------------------------------------
# Build report
# --------------------------------------------------------------------------
lines = []
A = lines.append

A('# ToC and Navigation Audit\n')
A(f'_Generated: 2026-05-15_\n')
A(f'_Repository: `E:/Projects/BookBlogsHome/LLMBook`_\n')
A('## Scope\n')
A(f'- Total HTML pages scanned: **{len(pages)}**')
A(f'- Section pages (section-*.html): {sum(1 for p in pages if is_section_page(p))}')
A(f'- Index pages (index.html): {sum(1 for p in pages if is_index_or_module(p))}')
A(f'- ToC source: `toc.html` ({len(toc_entries)} link entries indexed)\n')

A('## Header Navigation Issues\n')
A(f'- Pages missing `<nav class="header-nav">`: **{len(header_nav_missing)}**')
if header_nav_missing:
    A('\nFirst missing:')
    for p in header_nav_missing[:20]:
        A(f'  - `{p.relative_to(ROOT).as_posix()}`')
A(f'\n- Broken header-nav anchor targets: **{len(header_nav_broken)}**')
if header_nav_broken:
    for (src, txt, href, tgt) in header_nav_broken[:25]:
        A(f'  - `{src.relative_to(ROOT).as_posix()}` -> `{href}` (text: "{txt}") MISSING')

A('\n## Chapter Navigation Issues\n')
A(f'- Section/module-index pages missing `<nav class="chapter-nav">`: **{len(chapter_nav_missing)}**')
if chapter_nav_missing:
    for p in chapter_nav_missing[:25]:
        A(f'  - `{p.relative_to(ROOT).as_posix()}`')
    if len(chapter_nav_missing) > 25:
        A(f'  - ... +{len(chapter_nav_missing) - 25} more')

A(f'\n- Pages with partial chapter-nav (missing prev/up/next anchor): **{len(chapter_nav_partial)}**')
if chapter_nav_partial:
    for (p, miss) in chapter_nav_partial[:25]:
        A(f'  - `{p.relative_to(ROOT).as_posix()}` -> missing: {", ".join(miss)}')
    if len(chapter_nav_partial) > 25:
        A(f'  - ... +{len(chapter_nav_partial) - 25} more')

A(f'\n- Broken chapter-nav targets (prev/up/next -> 404): **{len(chapter_nav_broken)}**')
if chapter_nav_broken:
    for (src, kind, href, tgt) in chapter_nav_broken[:40]:
        A(f'  - `{src.relative_to(ROOT).as_posix()}` ({kind}) -> `{href}` MISSING')
    if len(chapter_nav_broken) > 40:
        A(f'  - ... +{len(chapter_nav_broken) - 40} more')

A(f'\n- Asymmetric prev/next chains (A.next != B and B.prev != A): **{len(asymmetric)}**')
if asymmetric:
    for (kind, src, tgt, back) in asymmetric[:20]:
        try:
            back_rel = back.relative_to(ROOT).as_posix() if back else 'NONE'
        except Exception:
            back_rel = str(back)
        A(f'  - {kind}: `{src.relative_to(ROOT).as_posix()}` -> `{tgt.relative_to(ROOT).as_posix()}` (back: `{back_rel}`)')
    if len(asymmetric) > 20:
        A(f'  - ... +{len(asymmetric) - 20} more')

A('\n## Table of Contents Issues\n')
A(f'- Broken ToC links (point to non-existent files): **{len(toc_broken)}**')
if toc_broken:
    for (v, h, tgt, txt, chip) in toc_broken[:40]:
        A(f'  - [{v}] `{h}` (chip="{chip}", text="{txt}") MISSING')
    if len(toc_broken) > 40:
        A(f'  - ... +{len(toc_broken) - 40} more')

A(f'\n- Section files NOT referenced in ToC (orphaned sections): **{len(unreferenced_sections)}**')
if unreferenced_sections:
    for p in unreferenced_sections[:40]:
        A(f'  - `{p.relative_to(ROOT).as_posix()}`')
    if len(unreferenced_sections) > 40:
        A(f'  - ... +{len(unreferenced_sections) - 40} more')

A(f'\n- Module/Appendix index files NOT referenced in ToC: **{len(unreferenced_indexes)}**')
if unreferenced_indexes:
    for p in unreferenced_indexes[:40]:
        A(f'  - `{p.relative_to(ROOT).as_posix()}`')

A(f'\n- Probable ToC title vs page-title mismatches: **{len(title_mismatches)}**')
if title_mismatches:
    A('\n_(Heuristic: text shown in ToC does not overlap with the page h1/title.)_')
    for (v, h, txt, page_title, chip) in title_mismatches[:30]:
        A(f'  - [{v}] `{h}` chip="{chip}"')
        A(f'    - ToC anchor : "{txt}"')
        A(f'    - Page title : "{page_title}"')
    if len(title_mismatches) > 30:
        A(f'  - ... +{len(title_mismatches) - 30} more')

A('\n## Recommendation Priority\n')

total_issues = (
    len(header_nav_missing) + len(header_nav_broken) +
    len(chapter_nav_missing) + len(chapter_nav_partial) + len(chapter_nav_broken) +
    len(asymmetric) + len(toc_broken) + len(unreferenced_sections) +
    len(unreferenced_indexes) + len(title_mismatches)
)
A(f'- Total issues detected: **{total_issues}**\n')

prio = []
if toc_broken:
    prio.append(f'**P0** Fix {len(toc_broken)} broken ToC link(s) (lead to 404).')
if chapter_nav_broken:
    prio.append(f'**P0** Fix {len(chapter_nav_broken)} broken prev/up/next target(s).')
if header_nav_broken:
    prio.append(f'**P0** Fix {len(header_nav_broken)} broken header-nav anchor target(s).')
if chapter_nav_missing:
    prio.append(f'**P1** Add missing chapter-nav block to {len(chapter_nav_missing)} section/module-index page(s).')
if chapter_nav_partial:
    prio.append(f'**P1** Fill in {len(chapter_nav_partial)} chapter-nav block(s) missing prev/up/next anchors.')
if header_nav_missing:
    prio.append(f'**P1** Add missing `<nav class="header-nav">` to {len(header_nav_missing)} page(s).')
if unreferenced_sections:
    prio.append(f'**P2** Decide whether to add {len(unreferenced_sections)} unreferenced section file(s) to the ToC, or delete them.')
if unreferenced_indexes:
    prio.append(f'**P2** Reference {len(unreferenced_indexes)} module/appendix index file(s) in the ToC.')
if asymmetric:
    prio.append(f'**P2** Reconcile {len(asymmetric)} asymmetric prev/next chain(s).')
if title_mismatches:
    prio.append(f'**P3** Review {len(title_mismatches)} probable ToC title vs page-title mismatch(es).')

if not prio:
    A('No issues detected. Navigation and ToC are healthy.')
else:
    for line in prio:
        A(f'- {line}')

A('')

OUT_PATH.write_text('\n'.join(lines), encoding='utf-8')
print(f'\nReport written to: {OUT_PATH}')
print()
print(f'Issues summary:')
print(f'  Header nav missing : {len(header_nav_missing)}')
print(f'  Header nav broken  : {len(header_nav_broken)}')
print(f'  Chap nav missing   : {len(chapter_nav_missing)}')
print(f'  Chap nav partial   : {len(chapter_nav_partial)}')
print(f'  Chap nav broken    : {len(chapter_nav_broken)}')
print(f'  Asymmetric nav     : {len(asymmetric)}')
print(f'  ToC broken         : {len(toc_broken)}')
print(f'  Orphan sections    : {len(unreferenced_sections)}')
print(f'  Orphan idx pages   : {len(unreferenced_indexes)}')
print(f'  Title mismatches   : {len(title_mismatches)}')
print(f'  TOTAL              : {total_issues}')
