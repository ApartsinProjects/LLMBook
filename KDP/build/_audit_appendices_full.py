"""Audit: comprehensive appendix inventory and redundancy analysis.

For each appendix in `appendices/`, this script counts:
  - number of section files (index + section-*.html)
  - total HTML byte size and approximate word count
  - outbound references (links to other appendices, parts, capstone)
  - inbound references (how often the appendix is referenced elsewhere)
  - glossary-link count, concept-link count, table count, callout count
  - presence of images directory

It also tabulates the appendix numbering gap (after L jumps to R, after V
jumps to AD, after AG jumps to AI, after AK is end). And it reports the
top overlap candidates between appendices by shared topic keywords.

The output is a single Markdown report plus structured JSON for downstream
tools. This script is read-only.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
APPENDICES_DIR = ROOT / 'appendices'
BUILD_DIR = ROOT / 'KDP' / 'build'

# Letters in the canonical appendix scheme that the project has ever used.
EXPECTED_LETTERS = [
    'A', 'B', 'C', 'D', 'E',
    'F', 'G', 'H', 'I', 'J',
    'K', 'L',
    'M', 'N', 'O', 'P', 'Q',  # historically merged into L
    'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z',  # moved to Part XII
    'AA', 'AB', 'AC',  # moved to Part XII
    'AD', 'AE', 'AF', 'AG',
    'AH',  # dropped in v14.5
    'AI', 'AJ', 'AK',
]


def appendix_letter(dirname: str) -> str:
    """appendix-ad-master-reference-tables -> 'AD'."""
    parts = dirname.split('-')
    return parts[1].upper()


def html_word_count(soup: BeautifulSoup) -> int:
    """Approximate word count from prose nodes only."""
    text = soup.get_text(separator=' ')
    # Strip code blocks, but soup.get_text already pulls those in; this is
    # an approximation. Words are whitespace-delimited tokens.
    words = re.findall(r"\S+", text)
    return len(words)


def parse_appendix(app_dir: Path) -> dict:
    """Collect stats for one appendix directory."""
    letter = appendix_letter(app_dir.name)
    section_files = sorted(
        [p for p in app_dir.glob('*.html') if p.name != 'index.html']
    )
    all_files = sorted(app_dir.glob('*.html'))
    has_images = (app_dir / 'images').is_dir()

    total_bytes = sum(p.stat().st_size for p in all_files)
    total_words = 0
    glossary_link_count = 0
    concept_link_count = 0
    table_count = 0
    callout_count = 0
    outbound = Counter()
    h1_text = ''
    title_text = ''

    for f in all_files:
        try:
            html = f.read_text(encoding='utf-8')
        except Exception:
            continue
        soup = BeautifulSoup(html, 'html.parser')
        total_words += html_word_count(soup)
        glossary_link_count += len(soup.find_all('a', class_='glossary-link'))
        concept_link_count += len(soup.find_all('a', class_='concept-link'))
        table_count += len(soup.find_all('table'))
        callout_count += len(soup.find_all('div', class_='callout'))

        if f.name == 'index.html':
            t = soup.find('title')
            if t:
                title_text = t.get_text(strip=True)
            h1 = soup.find('h1')
            if h1:
                h1_text = h1.get_text(strip=True)

        for a in soup.find_all('a', href=True):
            href = a['href']
            # Outbound: any depth ../ chain followed by part-*, appendices/appendix-*, capstone
            m_part = re.search(r'(?:\.\./)+(part-[^/]+)', href)
            m_app = re.search(r'(?:\.\./)+appendices/(appendix-[^/]+)', href)
            m_cap = re.search(r'(?:\.\./)+(capstone)', href)
            if m_part:
                outbound[m_part.group(1)] += 1
            elif m_app:
                if m_app.group(1) != app_dir.name:
                    outbound[m_app.group(1)] += 1
            elif m_cap:
                outbound['capstone'] += 1
            elif href.startswith('appendix-'):
                # within-appendices peer xref (rare, but capture it)
                m = re.match(r'(appendix-[^/]+)', href)
                if m and m.group(1) != app_dir.name:
                    outbound[m.group(1)] += 1
            elif href.startswith('../appendix-'):
                # sibling-style appendix link (../appendix-X/...)
                m = re.match(r'\.\./(appendix-[^/]+)', href)
                if m and m.group(1) != app_dir.name:
                    outbound[m.group(1)] += 1

    return {
        'letter': letter,
        'dirname': app_dir.name,
        'title': title_text,
        'h1': h1_text,
        'section_count': len(section_files),
        'total_files': len(all_files),
        'is_single_page': len(section_files) == 0,
        'total_bytes': total_bytes,
        'approx_words': total_words,
        'has_images': has_images,
        'glossary_links_in': glossary_link_count,
        'concept_links_in': concept_link_count,
        'tables': table_count,
        'callouts': callout_count,
        'outbound_refs': dict(outbound),
        'outbound_total': sum(outbound.values()),
    }


def inbound_counts(stats: dict[str, dict]) -> Counter:
    """For each appendix-X dir, count how many times it appears as the
    target of a link from ANY HTML file in the repo (not just appendices)."""
    by_dirname = Counter()
    search_globs = [
        ROOT.glob('part-*/module-*/*.html'),
        ROOT.glob('part-*/module-*/section-*.html'),
        ROOT.glob('appendices/appendix-*/*.html'),
        ROOT.glob('front-matter/*.html'),
        ROOT.glob('capstone/*.html'),
        [ROOT / 'toc.html'],
        [ROOT / 'index.html'],
    ]
    appendix_dirs = {s['dirname'] for s in stats.values()}
    for glob_iter in search_globs:
        for f in glob_iter:
            if not f.exists():
                continue
            try:
                html = f.read_text(encoding='utf-8')
            except Exception:
                continue
            for ad in appendix_dirs:
                # Count any href that contains the appendix dirname
                # (one count per file mention, but multiplicty per href).
                c = len(re.findall(r'(?<![A-Za-z0-9_-])' + re.escape(ad), html))
                if c:
                    by_dirname[ad] += c
    return by_dirname


# Topic keywords used to score appendix overlap pairs.
TOPIC_KEYWORDS = {
    'huggingface': ['huggingface', 'hf transformers', 'datasets library', 'hf hub', 'hf trainer'],
    'langchain': ['langchain', 'lcel', 'runnable', 'chain composition'],
    'tracking': ['wandb', 'weights & biases', 'mlflow', 'experiment tracking', 'run logging'],
    'serving': ['vllm', 'tgi', 'sglang', 'continuous batching', 'pagedattention'],
    'distributed': ['pyspark', 'databricks', 'ray ', 'horovod', 'deepspeed', 'fsdp'],
    'docker': ['dockerfile', 'docker compose', 'container', 'oci image'],
    'evaluation': ['benchmark', 'leaderboard', 'mmlu', 'gsm8k', 'humaneval'],
    'model_cards': ['gpt-4', 'claude', 'llama', 'gemini', 'qwen', 'mistral', 'context window'],
    'production': ['observability', 'guardrail', 'rate limit', 'circuit breaker', 'kill switch'],
    'math': ['linear algebra', 'probability', 'gradient', 'information theory'],
    'reading_paths': ['reading path', 'syllabus', 'curriculum', 'goal-based'],
    'glossary': ['definition', 'glossary'],
    'prompt_templates': ['prompt template', 'few-shot', 'system prompt'],
    'tooling_survey': ['tooling landscape', 'ecosystem survey', 'tool selection'],
    'reference_tables': ['comparison table', 'master reference', 'scannable table'],
}


def topic_signal(stats: dict[str, dict]) -> dict[str, dict[str, int]]:
    """For each appendix, count keyword occurrences per topic."""
    out = {}
    for dirname, s in stats.items():
        topic_hits = {}
        # Read all html files for this appendix and count keywords
        app_dir = APPENDICES_DIR / dirname
        full_text = ''
        for f in app_dir.glob('*.html'):
            try:
                full_text += f.read_text(encoding='utf-8').lower() + '\n'
            except Exception:
                continue
        for topic, kws in TOPIC_KEYWORDS.items():
            hits = sum(full_text.count(k) for k in kws)
            if hits:
                topic_hits[topic] = hits
        out[dirname] = topic_hits
    return out


def gap_analysis(stats: dict[str, dict]) -> dict:
    """Produce a gap table."""
    present = {s['letter']: s['dirname'] for s in stats.values()}
    rows = []
    for L in EXPECTED_LETTERS:
        rows.append({
            'letter': L,
            'present': L in present,
            'dirname': present.get(L, ''),
        })
    return {'rows': rows, 'present_letters': sorted(present.keys())}


def render_markdown(
    stats: dict[str, dict],
    inbound: Counter,
    topics: dict[str, dict[str, int]],
    gap: dict,
) -> str:
    """Render the audit-only portion (Phase 1) of the report. The redesign
    plan (Phases 2-4) is appended by a separate Python literal so this
    function stays a pure data renderer."""
    lines = []
    lines.append('# Appendix Audit (Phase 1: data only)')
    lines.append('')
    lines.append(f'Generated by `_audit_appendices_full.py` on the current snapshot.')
    lines.append('')

    lines.append('## A. Inventory')
    lines.append('')
    lines.append('| Letter | Dir | Sections | Files | Bytes | Words | Tables | Callouts | Glossary-links | Concept-links | Images | Inbound refs | Outbound refs |')
    lines.append('| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :-: | ---: | ---: |')
    for letter in sorted(stats, key=lambda d: (len(stats[d]['letter']), stats[d]['letter'])):
        s = stats[letter]
        lines.append(
            f"| {s['letter']} | `{s['dirname']}` | {s['section_count']} | "
            f"{s['total_files']} | {s['total_bytes']:,} | "
            f"{s['approx_words']:,} | {s['tables']} | {s['callouts']} | "
            f"{s['glossary_links_in']} | {s['concept_links_in']} | "
            f"{'Y' if s['has_images'] else '-'} | "
            f"{inbound.get(s['dirname'], 0)} | "
            f"{s['outbound_total']} |"
        )
    lines.append('')

    lines.append('## B. Gap analysis')
    lines.append('')
    lines.append(f"Present letters: `{', '.join(gap['present_letters'])}`")
    lines.append('')
    lines.append('| Expected letter | Present? | Dir |')
    lines.append('| :-: | :-: | --- |')
    for row in gap['rows']:
        mark = 'YES' if row['present'] else 'gap'
        dirname = f"`{row['dirname']}`" if row['dirname'] else '—'
        lines.append(f"| {row['letter']} | {mark} | {dirname} |")
    lines.append('')

    lines.append('## C. Outbound link targets per appendix')
    lines.append('')
    for letter in sorted(stats, key=lambda d: (len(stats[d]['letter']), stats[d]['letter'])):
        s = stats[letter]
        if not s['outbound_refs']:
            continue
        top5 = sorted(s['outbound_refs'].items(), key=lambda kv: -kv[1])[:5]
        lines.append(f"- **{s['letter']}** ({s['dirname']}): " + ', '.join(
            f"{k} x{v}" for k, v in top5
        ))
    lines.append('')

    lines.append('## D. Topic-keyword signal (raw hit counts)')
    lines.append('')
    topic_list = sorted({t for hits in topics.values() for t in hits})
    header = '| Appendix | ' + ' | '.join(topic_list) + ' |'
    sep = '| --- | ' + ' | '.join(['---:'] * len(topic_list)) + ' |'
    lines.append(header)
    lines.append(sep)
    for letter in sorted(stats, key=lambda d: (len(stats[d]['letter']), stats[d]['letter'])):
        s = stats[letter]
        hits = topics.get(s['dirname'], {})
        row = [f"**{s['letter']}**"] + [str(hits.get(t, 0)) for t in topic_list]
        lines.append('| ' + ' | '.join(row) + ' |')
    lines.append('')

    lines.append('## E. Overlap candidates (top topic-pair scores)')
    lines.append('')
    # For each topic, find appendices with non-trivial coverage.
    overlap_pairs = []
    for topic in topic_list:
        carriers = sorted(
            ((d, h.get(topic, 0)) for d, h in topics.items()),
            key=lambda kv: -kv[1],
        )
        carriers = [c for c in carriers if c[1] > 0]
        if len(carriers) < 2:
            continue
        primary = carriers[0]
        for other in carriers[1:]:
            score = min(primary[1], other[1])
            if score >= 3:
                overlap_pairs.append((topic, primary[0], primary[1], other[0], other[1], score))
    overlap_pairs.sort(key=lambda r: -r[5])
    lines.append('| Topic | Primary appendix | hits | Secondary appendix | hits | min |')
    lines.append('| --- | --- | ---: | --- | ---: | ---: |')
    for row in overlap_pairs[:30]:
        lines.append(
            f"| {row[0]} | `{row[1]}` | {row[2]} | `{row[3]}` | {row[4]} | {row[5]} |"
        )
    lines.append('')

    return '\n'.join(lines)


def main():
    stats = {}
    for app_dir in sorted(APPENDICES_DIR.iterdir()):
        if not app_dir.is_dir() or not app_dir.name.startswith('appendix-'):
            continue
        s = parse_appendix(app_dir)
        stats[app_dir.name] = s

    inbound = inbound_counts(stats)
    topics = topic_signal(stats)
    gap = gap_analysis(stats)

    md = render_markdown(stats, inbound, topics, gap)
    json_data = {
        'stats': stats,
        'inbound': dict(inbound),
        'topics': topics,
        'gap': gap,
    }

    (BUILD_DIR / 'AUDIT_appendices_full.md').write_text(md, encoding='utf-8')
    (BUILD_DIR / 'AUDIT_appendices_full.json').write_text(
        json.dumps(json_data, indent=2), encoding='utf-8'
    )

    # Console summary
    total = len(stats)
    sectioned = sum(1 for s in stats.values() if not s['is_single_page'])
    single = total - sectioned
    print(f'Audited {total} appendices: {sectioned} sectioned, {single} single-page.')
    print(f'Present letters: {gap["present_letters"]}')
    expected_set = set(EXPECTED_LETTERS)
    present_set = set(gap['present_letters'])
    # Distinguish "true gaps" from "deliberately removed"
    print(f'Truly missing in current scheme: '
          f'{sorted(expected_set - present_set)}')


if __name__ == '__main__':
    main()
