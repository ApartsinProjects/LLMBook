"""Comprehensive consistency audit for LLMBook v14.6.

Audits link integrity, ToC coherence, orphans, stale references, and nav
chain integrity AFTER the v14.5 restructuring:
  - Industries moved appendix-{w..ac} -> part-12 module-36..42
  - Conceptual Map appendix-ah dropped
  - Appendix numbering alignment
  - Bibliography header consolidation
  - 940 hyperlink injections (.glossary-link / .concept-link)
  - v14.4 nav boundary fixes (7 specific corrections)

Writes report to:  KDP/build/AUDIT_consistency_v14_6.md
"""
from __future__ import annotations
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
OUT  = ROOT / 'KDP' / 'build' / 'AUDIT_consistency_v14_6.md'
TOC  = ROOT / 'toc.html'

# Skip patterns: never scan/touch these
SKIP_DIRS = {'node_modules', '.git', 'pagefind', 'temp_epub',
             'source_fix_backups', 'backup'}
SKIP_REL  = ('KDP/output', 'KDP/build', 'KDP/html2pub',
             'scripts/_exercise_payloads',
             'agents/', 'templates/', 'KDP/metadata/')


def is_skip(p: Path) -> bool:
    parts = p.parts
    if any(d in SKIP_DIRS for d in parts):
        return True
    rel = p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else str(p)
    return any(rel.startswith(s) for s in SKIP_REL)


def read_html(p: Path) -> str | None:
    try:
        return p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            return None
    except Exception:
        return None


# --------------------------------------------------------------------------
# 1. Catalog every HTML page in scope
# --------------------------------------------------------------------------
print('Cataloging HTML pages...')
pages: list[Path] = []
for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    pages.append(p)
pages.sort()
print(f'  {len(pages)} HTML pages in scope')

page_set = {p.resolve() for p in pages}

# --------------------------------------------------------------------------
# 2. Per-page link extraction
# --------------------------------------------------------------------------
print('Parsing links...')

# Per-page state
nav_state = {}      # path -> {'prev', 'up', 'next', 'prev_text', 'next_text'}
all_internal_links = defaultdict(set)  # target_path -> {source_paths}
links_by_file = defaultdict(list)  # source_path -> [(href, target_path, line_no, kind, class)]

# Bibliography-section links (separate audit)
bib_links = []      # (source_path, href, target_resolved, ok)

# Glossary/concept hyperlinks (new in v14.5)
hyperlink_targets = []  # (source_path, klass, href, target_resolved, ok)

# Self-link list
self_links = []     # (source, kind, href)

# Page title for ToC comparison
title_index = {}

# Track parse errors
unparseable = []


def get_h1_or_title(soup) -> str:
    h1 = soup.find('h1')
    if h1:
        return h1.get_text(' ', strip=True)
    t = soup.find('title')
    if t:
        return t.get_text(' ', strip=True)
    return ''


def resolve_href(page: Path, href: str) -> tuple[Path | None, str]:
    """Return (resolved_path_no_anchor, anchor_or_empty)."""
    if not href:
        return None, ''
    href = href.strip()
    if href.startswith(('http://', 'https://', 'mailto:', 'javascript:',
                        'data:', 'tel:')):
        return None, ''
    if '#' in href:
        path_part, anchor = href.split('#', 1)
    else:
        path_part, anchor = href, ''
    if not path_part:
        # Pure anchor: same page
        return page.resolve(), anchor
    try:
        return (page.parent / path_part).resolve(), anchor
    except Exception:
        return None, anchor


for p in pages:
    txt = read_html(p)
    if txt is None:
        unparseable.append(p)
        continue
    try:
        soup = BeautifulSoup(txt, 'html.parser')
    except Exception:
        unparseable.append(p)
        continue

    title_index[p.resolve()] = get_h1_or_title(soup)

    # chapter-nav
    cn = soup.find('nav', class_='chapter-nav')
    if cn:
        prev_a = cn.find('a', class_='prev')
        up_a = cn.find('a', class_='up')
        next_a = cn.find('a', class_='next')

        def rsv(a):
            if not a or not a.get('href'):
                return None, ''
            return resolve_href(p, a['href'])

        prev_r, _ = rsv(prev_a)
        up_r, _ = rsv(up_a)
        next_r, _ = rsv(next_a)

        nav_state[p.resolve()] = {
            'prev': prev_r,
            'up': up_r,
            'next': next_r,
            'prev_text': prev_a.get_text(strip=True) if prev_a else None,
            'next_text': next_a.get_text(strip=True) if next_a else None,
            'has_prev_anchor': prev_a is not None,
            'has_up_anchor': up_a is not None,
            'has_next_anchor': next_a is not None,
        }

    # All <a href> for broken-link audit, with line numbers
    # Use regex over raw text for line numbers; combine with BeautifulSoup
    # to know inside-bibliography classification.
    in_bib_ranges = []
    for sec in soup.find_all(['section', 'div', 'aside'],
                              class_=lambda c: bool(c) and 'bibliography' in c):
        # We don't know exact line ranges from bs4; cheap proxy: presence test.
        in_bib_ranges.append(sec)

    # Build a mapping char_index -> in_bibliography? by reserialising regions
    # Quick approach: extract all <a> via bs4, check their ancestor.
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if not href:
            continue
        if href.startswith(('http://', 'https://', 'mailto:', 'javascript:',
                            'data:', 'tel:')):
            # External - track only for bibliography validity check
            klass = ' '.join(a.get('class') or [])
            in_bib = bool(a.find_parent(class_=lambda c: bool(c) and 'bibliography' in c))
            if in_bib:
                bib_links.append({
                    'source': p,
                    'href': href,
                    'external': True,
                    'ok': True,  # external URLs assumed OK (no network check)
                })
            continue

        target, anchor = resolve_href(p, href)
        klass = ' '.join(a.get('class') or [])
        line_no = None  # we'll skip for speed

        # Track internal link
        if target is not None:
            ok = target.exists()
            if ok:
                all_internal_links[target].add(p.resolve())

            in_bib = bool(a.find_parent(class_=lambda c: bool(c) and 'bibliography' in c))
            if in_bib:
                bib_links.append({
                    'source': p,
                    'href': href,
                    'target': target,
                    'anchor': anchor,
                    'external': False,
                    'ok': ok,
                })

            if 'glossary-link' in klass or 'concept-link' in klass:
                hyperlink_targets.append({
                    'source': p,
                    'klass': 'glossary-link' if 'glossary-link' in klass else 'concept-link',
                    'href': href,
                    'target': target,
                    'anchor': anchor,
                    'ok': ok,
                })

            # Self-link detection
            if target.resolve() == p.resolve() and ('next' in klass.split()
                                                    or 'prev' in klass.split()):
                self_links.append((p, klass, href))

            links_by_file[p].append({
                'href': href,
                'target': target,
                'anchor': anchor,
                'klass': klass,
                'ok': ok,
            })

print(f'  parsed {len(pages) - len(unparseable)} pages successfully')
if unparseable:
    print(f'  WARNING: {len(unparseable)} unparseable pages')

# --------------------------------------------------------------------------
# 3. Broken-link aggregation
# --------------------------------------------------------------------------
broken_links = []  # (source, href, target_resolved)
for src, entries in links_by_file.items():
    for e in entries:
        if not e['ok'] and e['target'] is not None:
            broken_links.append((src, e['href'], e['target'], e['klass']))

print(f'\nBroken internal links: {len(broken_links)}')

# --------------------------------------------------------------------------
# 4. Anchor validity (for href#anchor, does the anchor exist in target?)
# --------------------------------------------------------------------------
# Build id index per page
id_index = {}
for p in pages:
    if p in unparseable:
        continue
    txt = read_html(p)
    if txt is None:
        continue
    ids = set(re.findall(r'\bid="([^"]+)"', txt))
    id_index[p.resolve()] = ids

broken_anchors = []
for src, entries in links_by_file.items():
    for e in entries:
        if not e['ok'] or not e['anchor']:
            continue
        tgt = e['target']
        if tgt is None:
            continue
        tgt_ids = id_index.get(tgt, None)
        if tgt_ids is None:
            continue  # Couldn't index, skip
        if e['anchor'] not in tgt_ids:
            broken_anchors.append((src, e['href'], tgt, e['anchor']))

print(f'Broken anchors:        {len(broken_anchors)}')

# --------------------------------------------------------------------------
# 5. Orphan files: HTML in source tree not referenced anywhere
# --------------------------------------------------------------------------
# Build referenced-by-anything set, including ToC and index pages
referenced = set(all_internal_links.keys())

# Files explicitly safe (always reachable): index.html at root, toc.html
ALWAYS_REACHABLE_RELS = {'index.html', 'toc.html'}

orphans = []
for p in pages:
    resolved = p.resolve()
    rel = p.relative_to(ROOT).as_posix()
    if rel in ALWAYS_REACHABLE_RELS:
        continue
    if resolved in referenced:
        continue
    # Skip part/appendix top-level index.html if part is in TOC?
    # We'll be strict: report and let reviewer triage.
    orphans.append(p)

print(f'Orphan files:          {len(orphans)}')

# --------------------------------------------------------------------------
# 6. ToC audit
# --------------------------------------------------------------------------
print('\nAuditing toc.html...')
toc_html = read_html(TOC)
toc_entries = []  # (view, href, target_resolved, text, chip)
toc_broken = []   # (view, href, text, chip)
toc_targets = set()

if toc_html:
    toc_soup = BeautifulSoup(toc_html, 'html.parser')
    for view_id_name, view in (('short', toc_soup.find(id='toc-short')),
                                ('detailed', toc_soup.find(id='toc-detailed'))):
        if view is None:
            continue
        for a in view.find_all('a'):
            href = a.get('href', '').strip()
            if not href or href.startswith(('http://', 'https://')):
                continue
            target, _ = resolve_href(TOC, href)
            text = a.get_text(' ', strip=True)
            chip = ''
            parent = a.find_parent('div', class_='dense-chapter')
            if parent:
                chip_span = parent.find('span', class_='dense-ch-num')
                if chip_span:
                    chip = chip_span.get_text(strip=True)
            entry = (view_id_name, href, target, text, chip)
            toc_entries.append(entry)
            if target is None or not target.exists():
                toc_broken.append(entry)
            elif target is not None and target.exists():
                toc_targets.add(target)

print(f'  toc entries: {len(toc_entries)}')
print(f'  toc broken links: {len(toc_broken)}')

# Orphan TOC entries are already in toc_broken.
# Inversely: section/index files not referenced in TOC.
def is_section_page(p: Path) -> bool:
    return p.name.lower().startswith('section-') and p.name.endswith('.html')


def is_module_or_appendix_index(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    if not p.name == 'index.html':
        return False
    return ('/module-' in rel) or rel.startswith('appendices/appendix-')


unreferenced_sections = []
unreferenced_indexes = []
for p in pages:
    rl = p.resolve()
    if is_section_page(p) and rl not in toc_targets:
        unreferenced_sections.append(p)
    elif is_module_or_appendix_index(p) and rl not in toc_targets:
        unreferenced_indexes.append(p)

print(f'  sections not in ToC: {len(unreferenced_sections)}')
print(f'  module/appendix indexes not in ToC: {len(unreferenced_indexes)}')

# --------------------------------------------------------------------------
# 7. Nav chain integrity: reciprocity and edge cases
# --------------------------------------------------------------------------
print('\nAuditing navigation chain...')
asymmetric = []
broken_nav_targets = []
for src, refs in nav_state.items():
    for kind in ('prev', 'up', 'next'):
        tgt = refs[kind]
        if tgt and not tgt.exists():
            broken_nav_targets.append((src, kind, tgt))

    # Reciprocity
    nxt = refs['next']
    if nxt and nxt.exists() and nxt in nav_state:
        back = nav_state[nxt]['prev']
        if back and back.resolve() != src.resolve():
            asymmetric.append(('next/prev', src, nxt, back))
        elif not back:
            asymmetric.append(('next/prev', src, nxt, None))
    prv = refs['prev']
    if prv and prv.exists() and prv in nav_state:
        fwd = nav_state[prv]['next']
        if fwd and fwd.resolve() != src.resolve():
            asymmetric.append(('prev/next', src, prv, fwd))
        elif not fwd:
            asymmetric.append(('prev/next', src, prv, None))

print(f'  asymmetric nav: {len(asymmetric)}')
print(f'  broken nav targets: {len(broken_nav_targets)}')
print(f'  self-links (next/prev pointing at self): {len(self_links)}')

# --------------------------------------------------------------------------
# 8. Stale appendix/section references in prose
# --------------------------------------------------------------------------
print('\nScanning prose for stale references...')

# Build catalog of valid section / appendix refs
section_catalog = set()      # 'AB.6', '27.3', etc.
appendix_letters = set()     # 'A', 'B', ..., 'F', 'AD', 'AE', 'AF', 'AI', 'AJ', 'AK'
chapter_numbers = set()      # '0', '1', ..., '42'

for p in pages:
    rel = p.relative_to(ROOT).as_posix()
    name = p.name.lower()
    m = re.match(r'section-([a-z]+)\.(\d+)\.html', name)
    if m:
        section_catalog.add(f'{m.group(1).upper()}.{m.group(2)}')
        appendix_letters.add(m.group(1).upper())
        continue
    m = re.match(r'section-(\d+)\.(\d+)\.html', name)
    if m:
        section_catalog.add(f'{m.group(1)}.{m.group(2)}')
        chapter_numbers.add(m.group(1))
        continue
    # Module/appendix indexes register the chapter num / appendix letter
    if name == 'index.html':
        am = re.search(r'appendices/appendix-([a-z]+)-', rel)
        if am:
            appendix_letters.add(am.group(1).upper())
        mm = re.search(r'/module-(\d+)-', rel)
        if mm:
            chapter_numbers.add(str(int(mm.group(1))))

# Dropped/missing appendix letters: W, X, Y, Z, AA, AB, AC, AH should not appear
DROPPED_APPENDICES = {'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AH'}

ref_pattern = re.compile(
    r'\b(?:Appendix|Section|Chapter)\s+([A-Z]{1,3}(?:\.\d+)?|\d{1,2}(?:\.\d+)?)\b',
)

stale_refs = []        # (source, full_match, ref_token, ctx)
dropped_appendix_refs = []  # (source, mention)
ah_refs = []           # specifically appendix-AH mentions

for p in pages:
    txt = read_html(p)
    if txt is None:
        continue
    try:
        s = BeautifulSoup(txt, 'html.parser')
    except Exception:
        continue
    # Take prose text only (skip code/pre)
    for tag in s.find_all(['pre', 'code', 'script', 'style']):
        tag.decompose()
    text = s.get_text(' ', strip=True)

    for m in ref_pattern.finditer(text):
        token = m.group(1).upper()
        full = m.group(0)
        # Check if the ref is to a section
        if '.' in token:
            if token not in section_catalog:
                # Skip false positives: numbers like "5.0", "0.5", versions
                ctx = text[max(0, m.start() - 40):m.end() + 40]
                if any(w in ctx.lower() for w in
                        ['figure', 'fig.', 'eq.', 'equation', 'algorithm',
                         'table ', 'tab.']):
                    continue
                # Skip references to chapters with sections (e.g., "27.3" is
                # in section_catalog since file still exists)
                stale_refs.append({
                    'source': p,
                    'full': full,
                    'ref': token,
                    'ctx': ctx.strip()[:120],
                })
        else:
            # Plain "Appendix W" / "Chapter 42"
            if full.lower().startswith('appendix'):
                if token in DROPPED_APPENDICES:
                    ctx = text[max(0, m.start() - 60):m.end() + 60]
                    if token == 'AH':
                        ah_refs.append({'source': p, 'full': full, 'ctx': ctx.strip()[:140]})
                    else:
                        dropped_appendix_refs.append({
                            'source': p, 'full': full, 'token': token,
                            'ctx': ctx.strip()[:140],
                        })

print(f'  stale section refs: {len(stale_refs)}')
print(f'  refs to dropped appendix letters: {len(dropped_appendix_refs)}')
print(f'  refs to appendix AH (dropped):    {len(ah_refs)}')

# --------------------------------------------------------------------------
# 9. Part XII reachability check (special)
# --------------------------------------------------------------------------
print('\nChecking Part XII reachability...')
part12_modules = sorted(
    (ROOT / 'part-12-llm-applications-across-industries').glob('module-*/index.html')
)
part12_reach = {}
for m in part12_modules:
    rl = m.resolve()
    inbound = all_internal_links.get(rl, set())
    in_toc = rl in toc_targets
    part12_reach[m] = {
        'inbound_count': len(inbound),
        'in_toc': in_toc,
    }
    print(f'  {m.relative_to(ROOT).as_posix()}: inbound={len(inbound)}, in_toc={in_toc}')

# Part XII prev/next chain coherence
part12_chain_issues = []
expected_chain = [m.resolve() for m in part12_modules]
for i, mod in enumerate(part12_modules):
    rl = mod.resolve()
    refs = nav_state.get(rl, {})
    expected_prev = expected_chain[i - 1] if i > 0 else None
    expected_next = expected_chain[i + 1] if i < len(expected_chain) - 1 else None
    if expected_prev is not None and refs.get('prev') and refs['prev'].resolve() != expected_prev:
        part12_chain_issues.append((mod, 'prev', refs['prev'], expected_prev))
    if expected_next is not None and refs.get('next') and refs['next'].resolve() != expected_next:
        part12_chain_issues.append((mod, 'next', refs['next'], expected_next))

print(f'  Part XII chain issues: {len(part12_chain_issues)}')

# --------------------------------------------------------------------------
# 10. Path-depth sanity: relative paths with wrong number of ".."
# --------------------------------------------------------------------------
# This is implicitly covered by broken-link audit (wrong depth -> 404).
# We additionally flag "../../" prefixes in single-level files.
suspicious_paths = []
for src, entries in links_by_file.items():
    rel_depth = len(src.relative_to(ROOT).parts) - 1  # depth in tree
    for e in entries:
        if e['target'] is None:
            continue
        href = e['href']
        if href.startswith('http'):
            continue
        # Count '../' prefix
        ups = 0
        rest = href
        while rest.startswith('../'):
            ups += 1
            rest = rest[3:]
        # If ups exceeds the page's depth-from-root by more than 1, suspicious
        if ups > rel_depth:
            suspicious_paths.append((src, href, e['target'], e['ok']))

print(f'  suspicious-depth paths: {len(suspicious_paths)}')

# --------------------------------------------------------------------------
# 11. Bibliography link summary
# --------------------------------------------------------------------------
bib_broken = [b for b in bib_links if not b.get('external') and not b['ok']]
print(f'\nBibliography internal links: {sum(1 for b in bib_links if not b.get("external"))}')
print(f'Bibliography external links: {sum(1 for b in bib_links if b.get("external"))}')
print(f'Bibliography broken internal: {len(bib_broken)}')

# --------------------------------------------------------------------------
# 12. Glossary / concept link summary
# --------------------------------------------------------------------------
bad_hyperlinks = [h for h in hyperlink_targets if not h['ok']]
bad_hyperlink_anchors = []
for h in hyperlink_targets:
    if not h['ok'] or not h['anchor']:
        continue
    tgt_ids = id_index.get(h['target'])
    if tgt_ids is not None and h['anchor'] not in tgt_ids:
        bad_hyperlink_anchors.append(h)

print(f'\n.glossary-link / .concept-link total: {len(hyperlink_targets)}')
print(f'  with broken file target:   {len(bad_hyperlinks)}')
print(f'  with broken anchor:        {len(bad_hyperlink_anchors)}')

# --------------------------------------------------------------------------
# 13. Self-links (any href to self, broader than just next/prev)
# --------------------------------------------------------------------------
all_self_links = []
for src, entries in links_by_file.items():
    src_r = src.resolve()
    for e in entries:
        if e['target'] is None:
            continue
        if e['target'].resolve() == src_r:
            # Anchor-only is OK (jump within page); flag href-without-anchor
            if not e['anchor']:
                all_self_links.append((src, e['href'], e['klass']))

print(f'Self-links (whole-page): {len(all_self_links)}')

# --------------------------------------------------------------------------
# Build markdown report
# --------------------------------------------------------------------------
lines = []
A = lines.append

A('# v14.6 Consistency Audit')
A('')
A('_Generated 2026-05-15 after v14.5 restructuring (industries -> Part XII, '
  'appendix AH dropped, appendix numbering aligned, bibliography headers '
  'consolidated, 940 hyperlinks added, v14.4 nav boundary fixes)._')
A('')
A(f'_Repository: `{ROOT.as_posix()}`_')
A('')
A('## Scope')
A('')
A(f'- HTML pages scanned: **{len(pages)}**')
A(f'- Pages with chapter-nav: **{len(nav_state)}**')
A(f'- Pages indexed for IDs:  **{len(id_index)}**')
A(f'- ToC entries indexed:    **{len(toc_entries)}**')
A(f'- Unparseable pages:      **{len(unparseable)}**')
A('')

# Findings summary table
A('## Findings Summary')
A('')
A('| Category | Count |')
A('|---|---|')
A(f'| Broken internal links | **{len(broken_links)}** |')
A(f'| Broken anchor fragments | **{len(broken_anchors)}** |')
A(f'| Orphan HTML files (no inbound link) | **{len(orphans)}** |')
A(f'| ToC links broken | **{len(toc_broken)}** |')
A(f'| Section files not in ToC | **{len(unreferenced_sections)}** |')
A(f'| Module/appendix indexes not in ToC | **{len(unreferenced_indexes)}** |')
A(f'| Asymmetric prev/next chains | **{len(asymmetric)}** |')
A(f'| Broken prev/up/next targets | **{len(broken_nav_targets)}** |')
A(f'| Self-links (next/prev to same page) | **{len(self_links)}** |')
A(f'| All self-links (any kind) | **{len(all_self_links)}** |')
A(f'| Stale section references in prose | **{len(stale_refs)}** |')
A(f'| Refs to dropped appendix letters (W/X/Y/Z/AA/AB/AC) | **{len(dropped_appendix_refs)}** |')
A(f'| Refs to dropped Appendix AH | **{len(ah_refs)}** |')
A(f'| Suspicious-depth `../` paths | **{len(suspicious_paths)}** |')
A(f'| Bibliography broken internal links | **{len(bib_broken)}** |')
A(f'| Glossary/concept hyperlinks (total) | **{len(hyperlink_targets)}** |')
A(f'| Glossary/concept broken file targets | **{len(bad_hyperlinks)}** |')
A(f'| Glossary/concept broken anchors | **{len(bad_hyperlink_anchors)}** |')
A(f'| Part XII chain issues | **{len(part12_chain_issues)}** |')
A('')

# Part XII special check
A('## Part XII Restructuring Status')
A('')
A('| Module | Inbound Refs | In ToC |')
A('|---|---|---|')
for m, info in part12_reach.items():
    rel = m.relative_to(ROOT).as_posix()
    A(f'| `{rel}` | {info["inbound_count"]} | {"YES" if info["in_toc"] else "**NO**"} |')

p12_not_in_toc = [m for m, info in part12_reach.items() if not info['in_toc']]
if p12_not_in_toc:
    A('')
    A(f'> **CRITICAL: {len(p12_not_in_toc)} of 7 Part XII modules are missing '
      f'from the Table of Contents.**')
A('')

if part12_chain_issues:
    A('### Part XII prev/next chain issues')
    A('')
    for mod, kind, actual, expected in part12_chain_issues:
        rel = mod.relative_to(ROOT).as_posix()
        act = actual.relative_to(ROOT).as_posix() if actual else 'NONE'
        exp = expected.relative_to(ROOT).as_posix() if expected else 'NONE'
        A(f'- `{rel}` {kind}: -> `{act}` (expected `{exp}`)')
    A('')

# AH status
A('## Dropped Appendix AH (Conceptual Map)')
A('')
A(f'- Source-tree presence of `appendices/appendix-ah-*/`: '
  f'**{"PRESENT" if (ROOT / "appendices").glob("appendix-ah-*") and any((ROOT / "appendices").glob("appendix-ah-*")) else "GONE (correct)"}**')
A(f'- Prose references to "Appendix AH": **{len(ah_refs)}**')
if ah_refs:
    A('')
    for r in ah_refs[:15]:
        rel = r['source'].relative_to(ROOT).as_posix()
        A(f'  - `{rel}`: "{r["full"]}" ctx: ...{r["ctx"]}...')
    if len(ah_refs) > 15:
        A(f'  - ...and {len(ah_refs) - 15} more')
A('')

# Dropped appendix letters
A('## References to Moved/Dropped Appendix Letters (W, X, Y, Z, AA, AB, AC)')
A('')
A(f'- Total mentions: **{len(dropped_appendix_refs)}**')
if dropped_appendix_refs:
    by_letter = Counter(r['token'] for r in dropped_appendix_refs)
    A('')
    A('| Letter | Count |')
    A('|---|---|')
    for letter, n in by_letter.most_common():
        A(f'| {letter} | {n} |')
    A('')
    A('### Sample contexts')
    for r in dropped_appendix_refs[:20]:
        rel = r['source'].relative_to(ROOT).as_posix()
        A(f'- `{rel}`: "{r["full"]}" ctx: ...{r["ctx"]}...')
    if len(dropped_appendix_refs) > 20:
        A(f'- ...and {len(dropped_appendix_refs) - 20} more')
A('')

# Broken links - top
A('## Broken Internal Links (first 40)')
A('')
if not broken_links:
    A('_None. All internal hrefs resolve._')
else:
    for src, href, target, klass in broken_links[:40]:
        rel = src.relative_to(ROOT).as_posix()
        A(f'- `{rel}` -> `{href}` (class="{klass}")')
    if len(broken_links) > 40:
        A(f'\n_...and {len(broken_links) - 40} more._')
A('')

# Broken anchors
A('## Broken Anchor Fragments (first 30)')
A('')
if not broken_anchors:
    A('_None._')
else:
    for src, href, target, anchor in broken_anchors[:30]:
        rel = src.relative_to(ROOT).as_posix()
        A(f'- `{rel}` -> `{href}` (#{anchor} not in target)')
    if len(broken_anchors) > 30:
        A(f'\n_...and {len(broken_anchors) - 30} more._')
A('')

# Orphans
A('## Orphan HTML Files (no inbound links)')
A('')
if not orphans:
    A('_None._')
else:
    for p in orphans[:40]:
        rel = p.relative_to(ROOT).as_posix()
        A(f'- `{rel}`')
    if len(orphans) > 40:
        A(f'\n_...and {len(orphans) - 40} more._')
A('')

# ToC broken
A('## ToC Broken Links')
A('')
if not toc_broken:
    A('_None._')
else:
    for v, h, _, txt, chip in toc_broken[:30]:
        A(f'- [{v}] `{h}` (chip="{chip}", text="{txt}")')
    if len(toc_broken) > 30:
        A(f'\n_...and {len(toc_broken) - 30} more._')
A('')

# Section / index orphans relative to ToC
A('## Section Files Not in ToC')
A('')
if not unreferenced_sections:
    A('_All section files are referenced in the ToC._')
else:
    for p in unreferenced_sections[:40]:
        rel = p.relative_to(ROOT).as_posix()
        A(f'- `{rel}`')
    if len(unreferenced_sections) > 40:
        A(f'\n_...and {len(unreferenced_sections) - 40} more._')
A('')

A('## Module/Appendix Indexes Not in ToC')
A('')
if not unreferenced_indexes:
    A('_All module/appendix indexes are in the ToC._')
else:
    for p in unreferenced_indexes:
        rel = p.relative_to(ROOT).as_posix()
        A(f'- `{rel}`')
A('')

# Nav chain
A('## Asymmetric prev/next Chains')
A('')
if not asymmetric:
    A('_All prev/next pairs are reciprocal._')
else:
    for kind, src, tgt, back in asymmetric[:30]:
        rel = src.relative_to(ROOT).as_posix()
        tgt_rel = tgt.relative_to(ROOT).as_posix()
        back_rel = back.relative_to(ROOT).as_posix() if back else 'NONE'
        A(f'- {kind}: `{rel}` -> `{tgt_rel}` (back-link: `{back_rel}`)')
    if len(asymmetric) > 30:
        A(f'\n_...and {len(asymmetric) - 30} more._')
A('')

# Broken nav targets
A('## Broken prev/up/next Targets')
A('')
if not broken_nav_targets:
    A('_None._')
else:
    for src, kind, tgt in broken_nav_targets[:30]:
        rel = src.relative_to(ROOT).as_posix()
        try:
            tgt_rel = tgt.relative_to(ROOT).as_posix()
        except Exception:
            tgt_rel = str(tgt)
        A(f'- `{rel}` ({kind}) -> `{tgt_rel}` MISSING')
    if len(broken_nav_targets) > 30:
        A(f'\n_...and {len(broken_nav_targets) - 30} more._')
A('')

# Self-links
A('## Self-Links (page hyperlinking to itself)')
A('')
if not all_self_links:
    A('_None._')
else:
    for src, href, klass in all_self_links[:20]:
        rel = src.relative_to(ROOT).as_posix()
        A(f'- `{rel}` -> `{href}` (class="{klass}")')
    if len(all_self_links) > 20:
        A(f'\n_...and {len(all_self_links) - 20} more._')
A('')

# Stale section refs
A('## Stale Section References (prose)')
A('')
A(f'_Mentions of `Section X.Y` or `Appendix X.Y` where the referenced section file does not exist._')
A('')
if stale_refs:
    by_ref = Counter(r['ref'] for r in stale_refs)
    A('### Top stale ref tokens')
    A('')
    A('| Ref | Mentions |')
    A('|---|---|')
    for ref, n in by_ref.most_common(15):
        A(f'| {ref} | {n} |')
    A('')
    A('### Sample mentions')
    for r in stale_refs[:25]:
        rel = r['source'].relative_to(ROOT).as_posix()
        A(f'- `{rel}`: "{r["full"]}" ctx: ...{r["ctx"]}...')
    if len(stale_refs) > 25:
        A(f'\n_...and {len(stale_refs) - 25} more._')
else:
    A('_None._')
A('')

# Suspicious paths
A('## Suspicious-Depth `../` Paths')
A('')
if not suspicious_paths:
    A('_None._')
else:
    for src, href, tgt, ok in suspicious_paths[:25]:
        rel = src.relative_to(ROOT).as_posix()
        flag = '' if ok else ' BROKEN'
        A(f'- `{rel}` -> `{href}`{flag}')
    if len(suspicious_paths) > 25:
        A(f'\n_...and {len(suspicious_paths) - 25} more._')
A('')

# Glossary/concept hyperlinks
A('## Glossary / Concept Hyperlinks (v14.5 additions)')
A('')
A(f'- Total `.glossary-link` and `.concept-link` anchors: **{len(hyperlink_targets)}**')
A(f'- With broken file target: **{len(bad_hyperlinks)}**')
A(f'- With broken anchor: **{len(bad_hyperlink_anchors)}**')
A('')
if bad_hyperlinks:
    A('### Broken-target hyperlinks (first 20)')
    A('')
    for h in bad_hyperlinks[:20]:
        rel = h['source'].relative_to(ROOT).as_posix()
        A(f'- `{rel}` -> `{h["href"]}` (class={h["klass"]})')
    if len(bad_hyperlinks) > 20:
        A(f'\n_...and {len(bad_hyperlinks) - 20} more._')
    A('')
if bad_hyperlink_anchors:
    A('### Hyperlinks pointing at non-existent anchors (first 20)')
    A('')
    for h in bad_hyperlink_anchors[:20]:
        rel = h['source'].relative_to(ROOT).as_posix()
        A(f'- `{rel}` -> `{h["href"]}` (#{h["anchor"]} not in target)')
    if len(bad_hyperlink_anchors) > 20:
        A(f'\n_...and {len(bad_hyperlink_anchors) - 20} more._')
    A('')

# Bibliography
A('## Bibliography Link Status')
A('')
A(f'- Internal bibliography links: **{sum(1 for b in bib_links if not b.get("external"))}**')
A(f'- External (URL) bibliography links: **{sum(1 for b in bib_links if b.get("external"))}**')
A(f'- Broken internal bibliography links: **{len(bib_broken)}**')
if bib_broken:
    A('')
    A('### Sample broken bibliography links')
    for b in bib_broken[:20]:
        rel = b['source'].relative_to(ROOT).as_posix()
        A(f'- `{rel}` -> `{b["href"]}`')
A('')

# Recommendations
A('## Recommended v14.7 Patch Priority')
A('')
prio = []
if p12_not_in_toc:
    prio.append(('P0', f'Add Part XII (7 modules) to `toc.html` (both short and detailed views). '
                       f'Currently {len(p12_not_in_toc)}/7 modules invisible in nav.'))
# Stale module-27 entries should be removed if file is gone, or replaced
if any('module-27-llm-applications' in (e[1] or '') for e in toc_broken):
    prio.append(('P0', 'Remove stale `module-27-llm-applications` entries from `toc.html` '
                       '(industries content was moved to Part XII).'))
if toc_broken:
    prio.append(('P0', f'Fix {len(toc_broken)} broken ToC link(s) (lead to 404).'))
if broken_links:
    prio.append(('P0', f'Fix {len(broken_links)} broken internal link(s).'))
if broken_nav_targets:
    prio.append(('P0', f'Fix {len(broken_nav_targets)} broken prev/up/next target(s).'))
if ah_refs:
    prio.append(('P1', f'Remove or redirect {len(ah_refs)} prose reference(s) to dropped Appendix AH.'))
if dropped_appendix_refs:
    prio.append(('P1', f'Remap {len(dropped_appendix_refs)} prose reference(s) to moved '
                       f'appendix letters (W/X/Y/Z/AA/AB/AC -> Part XII modules).'))
if asymmetric:
    prio.append(('P1', f'Reconcile {len(asymmetric)} asymmetric prev/next chain(s).'))
if all_self_links:
    prio.append(('P1', f'Repair {len(all_self_links)} self-link(s) (page hyperlinks to itself).'))
if broken_anchors:
    prio.append(('P2', f'Fix {len(broken_anchors)} `#anchor` fragment(s) that don\'t resolve.'))
if bad_hyperlinks or bad_hyperlink_anchors:
    prio.append(('P2', f'Repair {len(bad_hyperlinks)} broken-target + {len(bad_hyperlink_anchors)} '
                       f'broken-anchor `.glossary-link`/`.concept-link` instance(s).'))
if unreferenced_sections:
    prio.append(('P2', f'Decide whether to add {len(unreferenced_sections)} unreferenced section(s) '
                       f'to ToC or delete them.'))
if orphans:
    prio.append(('P2', f'Triage {len(orphans)} orphan HTML file(s) (no inbound links).'))
if stale_refs:
    prio.append(('P3', f'Review {len(stale_refs)} stale `Section X.Y` mention(s) in prose.'))
if bib_broken:
    prio.append(('P3', f'Fix {len(bib_broken)} broken internal bibliography link(s).'))

if not prio:
    A('No issues detected. Nav, ToC, and link integrity are healthy.')
else:
    for level, text in sorted(prio, key=lambda x: x[0]):
        A(f'- **{level}** {text}')

A('')
A('---')
A('')
A('_End of report._')

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'\nReport written to: {OUT}')
print(f'\nTotal issues across all categories: '
      f'{len(broken_links) + len(broken_anchors) + len(orphans) + len(toc_broken) + len(unreferenced_sections) + len(unreferenced_indexes) + len(asymmetric) + len(broken_nav_targets) + len(all_self_links) + len(stale_refs) + len(dropped_appendix_refs) + len(ah_refs) + len(bad_hyperlinks) + len(bad_hyperlink_anchors) + len(part12_chain_issues) + len(bib_broken)}')
