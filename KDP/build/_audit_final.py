"""Final pre-ship audit. Read-only. Collects evidence for the audit report."""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parent.parent.parent
SECTION_RE = re.compile(r'section-(\d+)\.(\d+)(?:\.(\d+))?\.html$')
SECTION_ALPHA_RE = re.compile(r'section-([a-z]+)\.(\d+)(?:\.(\d+))?\.html$')
SPAN_NUM_RE = re.compile(r'<span class="section-num">([0-9]+(?:\.[0-9]+)+)</span>')
TITLE_RE = re.compile(r'<title>([^<]+)</title>', re.IGNORECASE)
H1_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.IGNORECASE | re.DOTALL)
H2_RE = re.compile(r'<h2[^>]*>(.*?)</h2>', re.IGNORECASE | re.DOTALL)
A_HREF_RE = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
IMG_SRC_RE = re.compile(r'<img\s+[^>]*src="([^"]+)"', re.IGNORECASE)
FIG_INSIDE_HEADER = re.compile(r'<header[^>]*>[\s\S]*?<figure[^>]*>[\s\S]*?</figure>[\s\S]*?</header>', re.IGNORECASE)
ASIDE_IN_HEADER = re.compile(r'<header[^>]*>[\s\S]*?<aside[^>]*class="callout[^"]*"[\s\S]*?</aside>[\s\S]*?</header>', re.IGNORECASE)


def iter_reader_html_files():
    skip_dirs = {'KDP', 'node_modules', 'pagefind', 'agents', 'scripts', '.git', 'images', 'downloads'}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith('_') and not d.startswith('.')]
        for fn in filenames:
            if fn.endswith('.html'):
                yield Path(dirpath) / fn


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace('\\', '/')
    except ValueError:
        return str(p)


def main():
    results = defaultdict(list)
    title_to_files = defaultdict(list)
    all_files = []
    section_files = []

    # Collect text once per file
    file_text = {}
    for p in iter_reader_html_files():
        all_files.append(p)
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            results['read_errors'].append(f'{rel(p)}: {e}')
            continue
        file_text[p] = text
        if SECTION_RE.search(p.name):
            section_files.append(p)

    # ---- 1. Numbering drift: section-num span vs URL ----
    for p in section_files:
        m_url = SECTION_RE.search(p.name)
        url_ch, url_sub = int(m_url.group(1)), int(m_url.group(2))
        url_sub3 = int(m_url.group(3)) if m_url.group(3) else None
        text = file_text[p]
        spans = SPAN_NUM_RE.findall(text)
        # First span is the page's own number; check it
        if spans:
            disp = spans[0]
            parts = disp.split('.')
            if len(parts) >= 2:
                try:
                    d_ch, d_sub = int(parts[0]), int(parts[1])
                    d_sub3 = int(parts[2]) if len(parts) >= 3 else None
                    if (d_ch, d_sub, d_sub3) != (url_ch, url_sub, url_sub3):
                        results['drift_span_vs_url'].append(f'{rel(p)}: span={disp} url={url_ch}.{url_sub}{"." + str(url_sub3) if url_sub3 else ""}')
                except ValueError:
                    pass

    # ---- 1b. ToC and chapter-index display mismatches ----
    toc_index_files = [p for p in all_files if p.name == 'index.html']
    a_disp_vs_url_mismatches = []
    a_section_re = re.compile(r'section-(\d+)\.(\d+)(?:\.(\d+))?\.html')
    for p in toc_index_files:
        text = file_text.get(p, '')
        for m in A_HREF_RE.finditer(text):
            href, inner = m.group(1), m.group(2)
            am = a_section_re.search(href)
            if not am:
                continue
            url_num = f'{int(am.group(1))}.{int(am.group(2))}'
            if am.group(3):
                url_num += f'.{int(am.group(3))}'
            # find any visible section-num span inside
            sm = SPAN_NUM_RE.search(inner)
            if sm:
                disp = sm.group(1)
                if disp != url_num:
                    a_disp_vs_url_mismatches.append(f'{rel(p)}: url={url_num} disp={disp}')
    results['drift_toc_disp'] = a_disp_vs_url_mismatches

    # ---- 1c. Prose 'see Section X.Y' references ----
    see_section_re = re.compile(r'\b[Ss]ee\s+Section\s+(\d+)\.(\d+)(?:\.(\d+))?\b')
    see_chapter_re = re.compile(r'\b[Ss]ee\s+Chapter\s+(\d+)\b')
    section_exists = set()
    for p in section_files:
        m = SECTION_RE.search(p.name)
        key = f'{int(m.group(1))}.{int(m.group(2))}'
        if m.group(3):
            key += f'.{int(m.group(3))}'
        section_exists.add(key)
    # also accept sections at .0 level (chapters)
    chapter_max = max([int(SECTION_RE.search(p.name).group(1)) for p in section_files], default=38)
    bad_see_refs = []
    for p in all_files:
        text = file_text.get(p, '')
        for m in see_section_re.finditer(text):
            ref = f'{int(m.group(1))}.{int(m.group(2))}'
            if m.group(3):
                ref += f'.{int(m.group(3))}'
            if ref not in section_exists:
                bad_see_refs.append(f'{rel(p)}: see Section {ref}')
        for m in see_chapter_re.finditer(text):
            ch = int(m.group(1))
            if ch > chapter_max or ch < 0:
                bad_see_refs.append(f'{rel(p)}: see Chapter {ch} (max={chapter_max})')
    results['bad_see_refs'] = bad_see_refs

    # ---- 3. Editing-history pollution ----
    pollution_patterns = [
        (r'\b(?:8th|9th|10th|11th|12th|eighth|ninth|tenth|eleventh|twelfth)\s+edition', 'edition reference'),
        (r'\bsince the previous edition\b', 'previous edition'),
        (r'\bnext edition\b', 'next edition'),
        (r'\bfuture edition\b', 'future edition'),
        (r'\bprevious edition\b', 'previous edition'),
        (r'\bin this edition\b', 'in this edition'),
        (r'\bgoing into 202[6-9]\b', 'going into 202X'),
        (r'\bspine_manifest\b', 'spine_manifest leak'),
        (r'\b_v\d{2,4}_', 'script reference leak'),
        (r'\bagent_reports\b', 'agent_reports leak'),
        (r'\bEPUBCheck\b', 'EPUBCheck leak'),
        (r'\bbuild pipeline\b', 'build pipeline leak'),
        (r'\bproduction pipeline\b', 'production pipeline leak'),
        (r'\bedition archive\b', 'edition archive leak'),
    ]
    # Pollution: only scan reader-facing pages. Already filtered.
    # Exclude footer text "Eleventh Edition, 2026" -- that's allowed.
    footer_ok_re = re.compile(r'Eleventh Edition,\s*2026')
    for p in all_files:
        text = file_text.get(p, '')
        for pat, label in pollution_patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                # If it's inside the footer "Eleventh Edition, 2026", skip
                start = m.start()
                ctx = text[max(0, start-40):start+80]
                if footer_ok_re.search(ctx) and 'Eleventh Edition' in m.group(0).title():
                    continue
                results['pollution'].append(f'{rel(p)}: [{label}] ...{text[max(0,start-30):start+60]}...')
                break  # one match per pattern per file is enough

    # ---- 3b. TODO / review / reviewer in <p> prose ----
    p_block_re = re.compile(r'<p[^>]*>(.*?)</p>', re.IGNORECASE | re.DOTALL)
    for p in all_files:
        text = file_text.get(p, '')
        for m in p_block_re.finditer(text):
            block = m.group(1)
            for term in ['TODO', 'FIXME', 'XXX:', 'reviewer', 'editorial note']:
                if term in block:
                    snippet = block[:160].replace('\n', ' ')
                    results['todo_in_prose'].append(f'{rel(p)}: [{term}] {snippet}')
                    break

    # ---- 4. Structural consistency ----
    for p in section_files:
        text = file_text[p]
        if 'class="chapter-header"' not in text:
            results['missing_chapter_header'].append(rel(p))
        if 'class="chapter-nav"' not in text:
            results['missing_chapter_nav'].append(rel(p))
        if '<footer' not in text:
            results['missing_footer'].append(rel(p))
        if '<div class="container">' in text and '<main class="content">' not in text:
            results['div_container_no_main'].append(rel(p))
        if ASIDE_IN_HEADER.search(text):
            results['aside_in_header'].append(rel(p))
        # figure in header: allowed if it's a chapter-opener illustration
        # Heuristic: if <figure> precedes </header> and the figure does NOT have class containing 'chapter-opener' or 'illustration', flag
        for m in re.finditer(r'<header[^>]*>([\s\S]*?)</header>', text, re.IGNORECASE):
            inner = m.group(1)
            for fm in re.finditer(r'<figure[^>]*class="([^"]*)"', inner):
                cls = fm.group(1)
                if 'chapter-opener' not in cls and 'illustration' not in cls and 'hero' not in cls:
                    results['fig_in_header_nonchapter'].append(f'{rel(p)}: class="{cls}"')

    # ---- 5. Duplications ----
    title_counter = defaultdict(list)
    for p in all_files:
        text = file_text.get(p, '')
        tm = TITLE_RE.search(text)
        if tm:
            title_counter[tm.group(1).strip()].append(rel(p))
    for title, paths in title_counter.items():
        if len(paths) > 1:
            results['dup_titles'].append(f'"{title}": {len(paths)} files: {paths[:3]}')

    # H1 duplication on same page
    for p in all_files:
        text = file_text.get(p, '')
        h1s = H1_RE.findall(text)
        if len(h1s) > 1:
            results['multi_h1'].append(f'{rel(p)}: {len(h1s)} <h1> tags')

    # ---- 6. Missing assets ----
    def resolve(base: Path, href: str) -> Path | None:
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:', 'data:')):
            return None
        # strip fragment and query
        href = href.split('#', 1)[0].split('?', 1)[0]
        if not href:
            return None
        target = (base.parent / href).resolve()
        return target

    for p in all_files:
        text = file_text.get(p, '')
        for m in IMG_SRC_RE.finditer(text):
            src = m.group(1)
            tgt = resolve(p, src)
            if tgt and not tgt.exists():
                results['missing_img'].append(f'{rel(p)}: src="{src}"')
        # Sample a-href for html files - too many, so only do those ending .html
        for m in A_HREF_RE.finditer(text):
            href = m.group(1)
            if '.html' in href and not href.startswith(('http', 'mailto', '#')):
                tgt = resolve(p, href)
                if tgt and not tgt.exists():
                    results['missing_html_href'].append(f'{rel(p)} -> {href}')

    # ---- 7. Standardization: footer text and title format ----
    # Accept: "Eleventh Edition, 2026 · Contents" or "Eleventh Edition, 2026 · <a ...>Contents</a>"
    expected_footer = re.compile(r'Eleventh Edition,\s*2026\s*(?:&middot;|[\xb7·•\-])\s*(?:<a[^>]*>)?Contents', re.IGNORECASE)
    expected_book_title = 'Building Conversational AI with LLMs and Agents'
    for p in all_files:
        text = file_text.get(p, '')
        # Footer check
        fm = re.search(r'<footer[^>]*>([\s\S]*?)</footer>', text, re.IGNORECASE)
        if fm:
            fblock = fm.group(1)
            if not expected_footer.search(fblock):
                # capture small snippet
                snip = re.sub(r'\s+', ' ', fblock).strip()[:120]
                results['nonstandard_footer'].append(f'{rel(p)}: {snip}')
        # Title check
        tm = TITLE_RE.search(text)
        if tm:
            t = tm.group(1).strip()
            if expected_book_title not in t:
                results['nonstandard_title'].append(f'{rel(p)}: <title>{t}</title>')

    # ---- 8. Capstone completeness ----
    cap_index = ROOT / 'capstone' / 'index.html'
    cap_req = ROOT / 'capstone' / 'requirements.html'
    results['capstone_status'].append(f'capstone/index.html exists: {cap_index.exists()}')
    results['capstone_status'].append(f'capstone/requirements.html exists: {cap_req.exists()}')

    # Capstone linking
    appendix_index = ROOT / 'appendices' / 'index.html'
    toc_pages = [ROOT / 'index.html']
    for path in [appendix_index] + toc_pages:
        if path.exists():
            t = path.read_text(encoding='utf-8', errors='replace')
            has_capstone = 'capstone' in t.lower()
            results['capstone_status'].append(f'{rel(path)} mentions capstone: {has_capstone}')

    # ---- Output summary ----
    out = []
    out.append('=== AUDIT RAW DATA ===\n')
    for k, v in results.items():
        out.append(f'\n## {k}: count={len(v)}')
        for line in v[:25]:
            out.append(f'  {line}')
    out.append(f'\n\nTotal HTML files scanned: {len(all_files)}')
    out.append(f'Section files: {len(section_files)}')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
