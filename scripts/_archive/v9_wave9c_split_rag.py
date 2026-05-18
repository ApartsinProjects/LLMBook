"""Wave 9 step C: split RAG monster (Ch 32, 9 sections) into Ch 32 Fundamentals + Ch 35 Advanced.

Split per v9 plan:
  Ch 32 RAG Fundamentals (4 sections):
    32.1  RAG Architecture & Fundamentals          (was 32.1, kept)
    32.2  Deep Research & Agentic RAG               (was 32.4 -> renumber)
    32.3  Structured Data & Text-to-SQL             (was 32.5 -> renumber)
    32.4  Source Attribution and Citation in RAG    (was 32.9 -> renumber)

  Ch 35 Advanced RAG (5 sections):
    35.1  Advanced RAG Techniques                   (was 32.2 -> move)
    35.2  RAG with Knowledge Graphs                 (was 32.3 -> move)
    35.3  GraphRAG: Knowledge Graph Augmented       (was 32.7 -> move)
    35.4  RAG Ingestion Pipelines and Connectors    (was 32.8 -> move)
    35.5  RAG Frameworks & Orchestration            (was 32.6 -> move)

Total: 9 sections preserved (no content loss per consolidation rule).
"""
from pathlib import Path
import re
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

PART = 'part-7-retrieval-information-extraction-with-llms'
CH32_DIR = ROOT / PART / 'module-32-rag'
CH35_DIR = ROOT / PART / 'module-35-advanced-rag'

# Moves: (source_section_in_old_ch32, target_ch, target_new_y, title)
# These get moved to new Ch 35
TO_CH35 = [
    (2, 35, 1, 'Advanced RAG Techniques'),
    (3, 35, 2, 'RAG with Knowledge Graphs'),
    (7, 35, 3, 'GraphRAG: Knowledge Graph-Augmented Retrieval'),
    (8, 35, 4, 'RAG Ingestion Pipelines and Connectors'),
    (6, 35, 5, 'RAG Frameworks & Orchestration'),
]

# These stay in Ch 32 but get renumbered
RENUMBER_IN_CH32 = [
    (1, 1, 'RAG Architecture & Fundamentals'),   # stays at 1
    (4, 2, 'Deep Research & Agentic RAG'),
    (5, 3, 'Structured Data & Text-to-SQL'),
    (9, 4, 'Source Attribution and Citation in RAG'),
]


CH35_INDEX = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter 35: Advanced RAG. Knowledge graphs, GraphRAG, ingestion pipelines, frameworks and orchestration." name="description"/>
<title>Chapter 35: Advanced RAG | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
</head>
<body class="index-page chapter-index">
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part VII: Retrieval &amp; Information Extraction with LLMs</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Chapter 35</span></div>
<h1>Advanced RAG: Knowledge Graphs, Ingestion &amp; Frameworks</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 35: Advanced RAG" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>Beyond RAG fundamentals, production retrieval systems integrate with knowledge graphs (both for storage and for query reasoning), use orchestration frameworks like LangChain and LlamaIndex, and depend on robust ingestion pipelines that handle the messy real world of PDFs, scraped sites, and database connectors. This chapter covers the advanced techniques.</p>
</div>
<h2>Sections in This Chapter</h2>
<ul class="sections-list">
{section_cards}
</ul>
<nav class="chapter-nav">
<a class="up" href="../index.html"><span class="nav-label">In Part</span><span class="nav-num">Part VII</span><span class="nav-title">Retrieval &amp; Information Extraction with LLMs</span></a>
</nav>
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
'''


def rewrite_section_metadata(file_path, old_ch, old_y, new_ch, new_y, new_title=None):
    text = file_path.read_text(encoding='utf-8')
    new_label = f'{new_ch}.{new_y}'
    text = re.sub(rf'<title>Section {old_ch}\.{old_y}:', f'<title>Section {new_label}:', text)
    text = re.sub(rf'(<meta content=")Section {old_ch}\.{old_y}:', rf'\1Section {new_label}:', text)
    text = re.sub(r'<div class="page-current">Section [^<]+</div>',
                  f'<div class="page-current">Section {new_label}</div>', text)
    text = re.sub(r'<span class="bc-current">Section [^<]+</span>',
                  f'<span class="bc-current">Section {new_label}</span>', text)
    # Update breadcrumb chapter reference if moving to different ch
    if old_ch != new_ch:
        # Update breadcrumb
        text = re.sub(
            r'<a href="index\.html">Chapter \d+: [^<]+</a>',
            f'<a href="index.html">Chapter {new_ch}</a>',
            text
        )
        # Update pagefind chapter meta
        text = re.sub(
            r'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:[^"]+"',
            f'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {new_ch}"',
            text
        )
        # Update chapter-nav up link
        text = re.sub(
            r'<span class="nav-num">Chapter \d+</span><span class="nav-title">[^<]+</span>',
            f'<span class="nav-num">Chapter {new_ch}</span><span class="nav-title">Advanced RAG</span>',
            text
        )
    # Anchor IDs and body refs
    text = re.sub(rf'\bid="{old_ch}-{old_y}-', f'id="{new_ch}-{new_y}-', text)
    text = re.sub(rf'\bhref="#{old_ch}-{old_y}-', f'href="#{new_ch}-{new_y}-', text)
    text = re.sub(rf'\bSection {old_ch}\.{old_y}\b', f'Section {new_label}', text)
    text = re.sub(rf'\b{old_ch}\.{old_y}\.(\d+)\b', rf'{new_ch}.{new_y}.\1', text)
    file_path.write_text(text, encoding='utf-8')


def main():
    CH35_DIR.mkdir(parents=True, exist_ok=True)
    (CH35_DIR / 'images').mkdir(exist_ok=True)
    print(f'Created {CH35_DIR.relative_to(ROOT)}')

    # Step 1: move TO_CH35 sections to .__tmp__ first to avoid collisions
    for old_y, new_ch, new_y, _title in TO_CH35:
        src = CH32_DIR / f'section-32.{old_y}.html'
        tmp = CH35_DIR / f'section-35.{new_y}.html.__tmp__'
        if src.exists() and not tmp.exists():
            subprocess.run(['git', 'mv', str(src), str(tmp)], cwd=ROOT, capture_output=True)

    # Step 2: rename .__tmp__ to final + rewrite metadata
    for old_y, new_ch, new_y, _title in TO_CH35:
        tmp = CH35_DIR / f'section-35.{new_y}.html.__tmp__'
        dst = CH35_DIR / f'section-35.{new_y}.html'
        if tmp.exists() and not dst.exists():
            subprocess.run(['git', 'mv', str(tmp), str(dst)], cwd=ROOT, capture_output=True)
            rewrite_section_metadata(dst, 32, old_y, 35, new_y)
            print(f'  Moved 32.{old_y} -> 35.{new_y}')

    # Step 3: renumber remaining Ch 32 sections
    # Use .__tmp__ pattern
    for old_y, new_y, _title in RENUMBER_IN_CH32:
        if old_y == new_y: continue
        src = CH32_DIR / f'section-32.{old_y}.html'
        tmp = CH32_DIR / f'section-32.{new_y}.html.__tmp__'
        if src.exists() and not tmp.exists():
            subprocess.run(['git', 'mv', str(src), str(tmp)], cwd=ROOT, capture_output=True)

    for old_y, new_y, _title in RENUMBER_IN_CH32:
        if old_y == new_y: continue
        tmp = CH32_DIR / f'section-32.{new_y}.html.__tmp__'
        dst = CH32_DIR / f'section-32.{new_y}.html'
        if tmp.exists() and not dst.exists():
            subprocess.run(['git', 'mv', str(tmp), str(dst)], cwd=ROOT, capture_output=True)
            rewrite_section_metadata(dst, 32, old_y, 32, new_y)
            print(f'  Renumbered 32.{old_y} -> 32.{new_y} in Ch 32')

    # Step 4: write Ch 35 index
    section_cards = []
    for _, _, new_y, title in TO_CH35:
        section_cards.append(
            f'<li><a class="section-card" href="section-35.{new_y}.html">\n'
            f'<span class="section-num">35.{new_y}</span>\n'
            f'<span class="section-title">{title}</span>\n'
            f'<span class="section-desc">Split from old Ch 32 RAG monster.</span>\n'
            f'</a></li>'
        )
    (CH35_DIR / 'index.html').write_text(
        CH35_INDEX.format(section_cards='\n'.join(section_cards)),
        encoding='utf-8'
    )
    print(f'Created Ch 35 index with {len(TO_CH35)} sections')

    # Step 5: update Ch 32 index (now has 4 sections, renumbered)
    ch32_idx = CH32_DIR / 'index.html'
    if ch32_idx.exists():
        text = ch32_idx.read_text(encoding='utf-8')
        new_cards = []
        for old_y, new_y, title in RENUMBER_IN_CH32:
            new_cards.append(
                f'<li><a class="section-card" href="section-32.{new_y}.html">\n'
                f'<span class="section-num">32.{new_y}</span>\n'
                f'<span class="section-title">{title}</span>\n'
                f'<span class="section-desc">RAG fundamentals.</span>\n'
                f'</a></li>'
            )
        text = re.sub(
            r'<ul class="sections-list">[\s\S]*?</ul>',
            f'<ul class="sections-list">\n' + '\n'.join(new_cards) + '\n</ul>',
            text,
            count=1
        )
        # Also update h1 to "RAG Fundamentals"
        text = re.sub(r'<h1>[^<]+</h1>', '<h1>RAG Fundamentals</h1>', text, count=1)
        ch32_idx.write_text(text, encoding='utf-8')
        print('Updated Ch 32 index')

    # Step 6: update Part 7 index with Ch 35 card
    part7_idx = ROOT / PART / 'index.html'
    text = part7_idx.read_text(encoding='utf-8')
    if 'module-35-advanced-rag' not in text:
        new_card = f'''<div class="chapter-card">
<div class="chapter-card-header"><span class="mod-num">Chapter 35</span> Advanced RAG: Knowledge Graphs, Ingestion &amp; Frameworks</div>
<div class="chapter-card-body">
<ul class="section-list">
'''
        for _, _, new_y, title in TO_CH35:
            new_card += f'<li><a href="module-35-advanced-rag/section-35.{new_y}.html"><span class="sec-num">35.{new_y}</span> {title}</a></li>\n'
        new_card += '</ul>\n</div>\n</div>\n'
        text = text.replace('</main>', new_card + '</main>', 1)
        part7_idx.write_text(text, encoding='utf-8')
        print('Added Ch 35 card to Part 7 index')

    # Step 7: cross-ref rewrite (32.X moved to 35.Y, or 32.X renumbered to 32.Y)
    # Build mapping
    moves = []  # (old_ch, old_y, new_ch, new_y)
    for old_y, new_ch, new_y, _ in TO_CH35:
        moves.append((32, old_y, 35, new_y))
    for old_y, new_y, _ in RENUMBER_IN_CH32:
        if old_y != new_y:
            moves.append((32, old_y, 32, new_y))

    # Use sentinel-based rewriting to avoid double-application
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Replace with sentinel markers first
        for old_ch, old_y, new_ch, new_y in moves:
            # In Ch 32 file: href="section-X.Y.html"
            # In other files: href="module-32-rag/section-X.Y.html"
            text = re.sub(
                rf'(href="[^"]*?)module-32-rag/section-32\.{old_y}\.html',
                rf'\1__MOVE_{old_ch}_{old_y}__',
                text
            )
        for old_ch, old_y, new_ch, new_y in moves:
            mod_name = 'module-35-advanced-rag' if new_ch == 35 else 'module-32-rag'
            text = text.replace(
                f'__MOVE_{old_ch}_{old_y}__',
                f'{mod_name}/section-{new_ch}.{new_y}.html'
            )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'Cross-refs updated in {n_files} files')


if __name__ == '__main__':
    main()
