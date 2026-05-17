"""Build a content-index summary for every HTML page in the book.

Output: book_content_index.jsonl — one JSON record per page, easy to grep,
load into Python, or feed to an analysis agent.

Per-page record:
{
  "schema": 1,
  "path": "part-9-.../section-42.1.html",
  "page_type": "section" | "chapter-index" | "part-index" | "fm" | "appendix-section" | "appendix-index" | "toc" | "cover" | "other",
  "part_slug": "part-9-llm-evaluation-observability",
  "part_roman": "IX",
  "chapter_num": 42,
  "section_num": "42.1",
  "title": "LLM Evaluation Fundamentals",
  "first_para": "...",
  "big_picture": "...",
  "epigraph": {"quote": "...", "cite": "..."},
  "headings": [{"level": 2, "number": "42.1.1", "text": "..."}],
  "callouts": [{"type": "key-insight", "title": "Key Insight", "first": "..."}],
  "links": [{"href": "...", "text": "...", "is_external": false}],
  "images": ["images/foo.png"],
  "code_blocks": {"python": 3, "bash": 1, "text": 2},
  "tables": 2,
  "figures": 5,
  "word_count": 4200,
  "has_bibliography": true,
  "has_chapter_nav": true,
  "has_section_nav": true,
  "byte_size": 78912
}

Usage:
  python scripts/build_content_index.py [--single PATH]
    Build full index, or update one file if --single given.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from collections import Counter
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / 'book_content_index.jsonl'

SKIP_DIRS = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
             'source_fix_backups', 'pagefind', 'templates', '.claude',
             '.book-update', 'vendor', 'agents'}

PART_NAMES = {
    'part-1-llm-building-blocks': ('I', 'LLM Building Blocks'),
    'part-2-understanding-llms': ('II', 'Understanding LLMs'),
    'part-3-working-with-llms': ('III', 'Working with LLMs'),
    'part-4-training-adaptation': ('IV', 'LLM Training and Adaptation'),
    'part-5-multimodal-llms': ('V', 'Multimodal LLMs'),
    'part-6-agentic-ai': ('VI', 'Agentic AI'),
    'part-7-retrieval-information-extraction-with-llms': ('VII', 'Retrieval & Information Extraction with LLMs'),
    'part-8-conversational-ai-with-llms': ('VIII', 'Conversational AI with LLMs'),
    'part-9-llm-evaluation-observability': ('IX', 'LLM Evaluation & Observability'),
    'part-10-llm-security-runtime-safety': ('X', 'LLM Security & Runtime Safety'),
    'part-11-llm-ethics-trust-governance': ('XI', 'LLM Ethics, Trust & Governance'),
    'part-12-llm-systems-at-scale': ('XII', 'LLM Systems at Scale'),
    'part-13-llmops-lifecycle': ('XIII', 'LLMOps Lifecycle'),
    'part-14-designing-llm-agent-products': ('XIV', 'Designing LLM/Agent Products'),
    'part-15-applications-of-llms-across-industries': ('XV', 'Applications of LLMs Across Industries'),
    'part-16-llm-agentic-ai-research-frontiers': ('XVI', 'LLM & Agentic AI Research Frontiers'),
}


def strip_html(s: str) -> str:
    """Remove HTML tags, decode common entities, collapse whitespace."""
    s = re.sub(r'<[^>]+>', '', s)
    s = (s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
         .replace('&quot;', '"').replace('&#39;', "'").replace('&rsquo;', "'")
         .replace('&lsquo;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"')
         .replace('&hellip;', '...').replace('&nbsp;', ' '))
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def truncate(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    return s[:n - 1].rsplit(' ', 1)[0] + '…'


def page_type(path: Path) -> str:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    name = path.name

    if name == 'index.html' and len(parts) == 1:
        return 'cover'
    if name == 'toc.html':
        return 'toc'
    if parts[0] == 'front-matter':
        return 'fm'
    if parts[0] == 'appendices':
        if name == 'index.html' and len(parts) == 2:
            return 'appendix-overview'
        if name == 'index.html':
            return 'appendix-index'
        if name.startswith('section-'):
            return 'appendix-section'
        return 'other'
    if parts[0].startswith('part-'):
        if name == 'index.html' and len(parts) == 2:
            return 'part-index'
        if name == 'index.html':
            return 'chapter-index'
        if name.startswith('section-'):
            return 'section'
        return 'other'
    if parts[0] == 'capstone':
        return 'capstone'
    return 'other'


def extract_part_chapter_section(path: Path) -> tuple[Optional[str], Optional[str], Optional[int], Optional[str]]:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    part_slug = parts[0] if parts and parts[0] in PART_NAMES else None
    part_roman = PART_NAMES[part_slug][0] if part_slug else None

    ch_num = None
    sec_num = None

    if len(parts) >= 2:
        m = re.match(r'module-(\d+)-', parts[1])
        if m:
            ch_num = int(m.group(1))

    m = re.match(r'section-(\d+)\.(\d+)\.html', path.name)
    if m:
        sec_num = f'{m.group(1)}.{m.group(2)}'

    # Appendix sections
    m = re.match(r'section-([a-z])\.(\d+)\.html', path.name)
    if m:
        sec_num = f'{m.group(1).upper()}.{m.group(2)}'

    return part_slug, part_roman, ch_num, sec_num


def extract_title(text: str) -> str:
    m = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', text)
    if m:
        return strip_html(m.group(1))
    m = re.search(r'<title>([^<]+)</title>', text)
    if m:
        return strip_html(m.group(1)).split('|')[0].strip()
    return ''


def extract_first_para(text: str) -> str:
    # First <p> inside <main>
    main_m = re.search(r'<main[^>]*>([\s\S]*?)</main>', text)
    body = main_m.group(1) if main_m else text
    # Skip <p> inside the big-picture callout to avoid duplicating
    # Strip out callouts first
    body_no_callouts = re.sub(
        r'<div class="callout[^"]*">[\s\S]*?</div>\s*</div>?',
        '',
        body
    )
    # Strip out figure / blockquote
    body_no_callouts = re.sub(r'<figure[^>]*>[\s\S]*?</figure>', '', body_no_callouts)
    body_no_callouts = re.sub(r'<blockquote[^>]*>[\s\S]*?</blockquote>', '', body_no_callouts)
    m = re.search(r'<p>([\s\S]*?)</p>', body_no_callouts)
    if m:
        return truncate(strip_html(m.group(1)), 400)
    return ''


def extract_big_picture(text: str) -> str:
    m = re.search(
        r'<div class="callout big-picture">\s*<div class="callout-title">[^<]*</div>\s*<p>([\s\S]*?)</p>',
        text
    )
    if m:
        return truncate(strip_html(m.group(1)), 600)
    return ''


def extract_epigraph(text: str) -> Optional[dict]:
    m = re.search(
        r'<blockquote class="epigraph">\s*<p>([\s\S]*?)</p>([\s\S]*?)</blockquote>',
        text
    )
    if not m:
        return None
    quote = truncate(strip_html(m.group(1)), 300)
    cite_m = re.search(r'<cite>([\s\S]*?)</cite>', m.group(2))
    cite = strip_html(cite_m.group(1)) if cite_m else ''
    return {'quote': quote, 'cite': cite}


def extract_headings(text: str) -> list[dict]:
    """Extract h2/h3/h4 headings with their visible numbering and text."""
    main_m = re.search(r'<main[^>]*>([\s\S]*?)</main>', text)
    body = main_m.group(1) if main_m else text
    out = []
    for m in re.finditer(r'<(h[234])[^>]*id="([^"]*)"[^>]*>([^<]*)</\1>', body):
        level = int(m.group(1)[1])
        h_id = m.group(2)
        full = m.group(3).strip()
        # Number prefix (e.g. "42.1.1 Foo" → number "42.1.1", text "Foo")
        num_m = re.match(r'^((?:\d+|[A-Z])(?:\.\d+)*\.?)\s+(.+)$', full)
        if num_m:
            number = num_m.group(1).rstrip('.')
            label = num_m.group(2)
        else:
            number = ''
            label = full
        out.append({
            'level': level,
            'number': number,
            'text': label,
            'id': h_id,
        })
    # H2/H3 without explicit id
    for m in re.finditer(r'<(h[234])[^>]*>([^<]*)</\1>', body):
        if 'id=' in m.group(0):
            continue  # already captured
        level = int(m.group(1)[1])
        full = m.group(2).strip()
        num_m = re.match(r'^((?:\d+|[A-Z])(?:\.\d+)*\.?)\s+(.+)$', full)
        if num_m:
            number = num_m.group(1).rstrip('.')
            label = num_m.group(2)
        else:
            number = ''
            label = full
        out.append({'level': level, 'number': number, 'text': label, 'id': ''})
    return out


def extract_callouts(text: str) -> list[dict]:
    """Extract callout blocks: type, title, first sentence of body."""
    out = []
    for m in re.finditer(
        r'<div class="callout ([a-z-]+)">\s*<div class="callout-title">([\s\S]*?)</div>\s*([\s\S]*?)</div>\s*(?=<div class="callout|<h\d|<p>|<ul|<ol|<pre|<figure|<table|<nav|<section|<details|<footer|</main|$)',
        text
    ):
        ctype = m.group(1).strip()
        title = strip_html(m.group(2)).strip()
        body = m.group(3)
        # First <p> inside the callout body
        p_m = re.search(r'<p>([\s\S]*?)</p>', body)
        if p_m:
            first = truncate(strip_html(p_m.group(1)), 200)
        else:
            first = truncate(strip_html(body), 200)
        out.append({'type': ctype, 'title': title, 'first': first})
    return out


def extract_links(text: str) -> list[dict]:
    out = []
    for m in re.finditer(r'<a\s[^>]*?href="([^"]+)"[^>]*>([\s\S]*?)</a>', text):
        href = m.group(1)
        link_text = truncate(strip_html(m.group(2)), 80)
        is_external = href.startswith('http://') or href.startswith('https://')
        out.append({
            'href': href,
            'text': link_text,
            'external': is_external,
        })
    return out


def extract_images(text: str) -> list[str]:
    out = []
    for m in re.finditer(r'<img\s[^>]*?src="([^"]+)"', text):
        out.append(m.group(1))
    return out


def extract_code_blocks(text: str) -> dict:
    counts = Counter()
    # <pre><code class="pygments-highlighted lang-X">
    for m in re.finditer(r'<pre[^>]*><code class="[^"]*lang-([a-z]+)', text):
        counts[m.group(1)] += 1
    return dict(counts)


def count_pattern(text: str, pat: str) -> int:
    return len(re.findall(pat, text))


def word_count(text: str) -> int:
    main_m = re.search(r'<main[^>]*>([\s\S]*?)</main>', text)
    body = main_m.group(1) if main_m else text
    plain = strip_html(body)
    return len(plain.split())


def build_record(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    part_slug, part_roman, ch_num, sec_num = extract_part_chapter_section(path)
    rec = {
        'schema': 1,
        'path': str(path.relative_to(ROOT)).replace('\\', '/'),
        'page_type': page_type(path),
        'part_slug': part_slug,
        'part_roman': part_roman,
        'chapter_num': ch_num,
        'section_num': sec_num,
        'title': extract_title(text),
        'first_para': extract_first_para(text),
        'big_picture': extract_big_picture(text),
        'epigraph': extract_epigraph(text),
        'headings': extract_headings(text),
        'callouts': extract_callouts(text),
        'links': extract_links(text),
        'images': extract_images(text),
        'code_blocks': extract_code_blocks(text),
        'tables': count_pattern(text, r'<table[\s>]'),
        'figures': count_pattern(text, r'<figure[\s>]'),
        'word_count': word_count(text),
        'has_bibliography': 'class="bibliography"' in text or '<section class="bibliography"' in text,
        'has_chapter_nav': '<nav class="chapter-nav"' in text,
        'has_section_nav': '<nav class="section-nav"' in text,
        'byte_size': len(text.encode('utf-8')),
    }
    return rec


def iter_pages():
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP_DIRS:
            continue
        yield p


def build_full_index():
    records = []
    n = 0
    for p in iter_pages():
        try:
            rec = build_record(p)
            records.append(rec)
            n += 1
        except Exception as e:
            print(f'  ERROR on {p}: {e}', file=sys.stderr)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'Indexed {n} HTML files → {INDEX_PATH.relative_to(ROOT)}')
    return records


def update_single(rel_path: str):
    target = ROOT / rel_path
    if not target.exists():
        print(f'ERROR: {target} does not exist')
        return
    rec = build_record(target)
    # Read existing index, replace the matching record, write back
    existing = []
    if INDEX_PATH.exists():
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                r = json.loads(line)
                if r.get('path') != rec['path']:
                    existing.append(r)
    existing.append(rec)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        for r in existing:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'Updated {rec["path"]}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--single', help='Rebuild index for one HTML path (relative to repo root)')
    args = ap.parse_args()
    if args.single:
        update_single(args.single)
    else:
        build_full_index()


if __name__ == '__main__':
    main()
