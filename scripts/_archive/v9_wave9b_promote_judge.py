"""Wave 9 step B: promote sec 42.8 (LLM-as-Judge) to its own chapter in Part 9.

The current sec 42.8 (38 KB, "LLM-as-Judge: Reliability, Debiasing, and
Training Judge Models") is promoted to:

  Part 9 Chapter 46: LLM-as-Judge & Automated Evaluation

Plus we'll restore additional content from the related sec 42.9
(Long-Context Benchmarks) which is also overgrown.

Process:
  - Create module-46-llm-as-judge-automated-evaluation/ in Part 9
  - Split sec 42.8 H2 subsections into ~5 first-class sections
  - Delete sec 42.8
  - Renumber sec 42.9 -> 42.8 (close the gap)
  - Update Part 9 + Ch 42 indexes; rewrite cross-refs
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

NEW_MODULE = 'module-46-llm-as-judge-automated-evaluation'
NEW_PART = 'part-9-llm-evaluation-observability'
SOURCE_SEC = 'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.8.html'

SECTIONS_PLAN = [
    (1, 'Why LLM-as-Judge Matters', [0]),
    (2, 'Judge Reliability and Common Biases', [1]),
    (3, 'Debiasing Techniques: Position, Length, and Verbosity', [2]),
    (4, 'Training Judge Models', [3]),
    (5, 'Multi-Judge Ensembles and Production Patterns', [4]),
]


def extract_h2_blocks(html):
    main_m = re.search(r'<main[^>]*>([\s\S]*?)</main>', html)
    if not main_m: return []
    body = main_m.group(1)
    h2_positions = [(m.start(), m.end(), m.group(1))
                    for m in re.finditer(r'<h2[^>]*>([^<]+)</h2>', body)]
    if not h2_positions: return []
    blocks = []
    for i, (start, end, title) in enumerate(h2_positions):
        block_end = h2_positions[i+1][0] if i+1 < len(h2_positions) else len(body)
        blocks.append({'title': title.strip(), 'html': body[start:block_end]})
    return blocks


SECTION_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Section {sec_num}: {sec_title}. A comprehensive chapter from the Building Conversational AI textbook." name="description"/>
<title>Section {sec_num}: {sec_title}</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<link href="../../styles/pygments.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
</head>
<body>
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="header-search"><div id="search"></div></div>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part IX: LLM Evaluation &amp; Observability</a><span class="bc-sep">&rsaquo;</span><a href="index.html">Chapter 46: LLM-as-Judge &amp; Automated Evaluation</a></div>
<h1>{sec_title}</h1><div class="page-current">Section {sec_num}</div>
</header>
<main class="content"><span class="pagefind-meta-injected" data-pagefind-meta="part:Part IX: LLM Evaluation &amp; Observability" hidden=""></span><span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 46: LLM-as-Judge &amp; Automated Evaluation" hidden=""></span>
{body}
</main>
<nav class="chapter-nav">
<a class="up" href="index.html"><span class="nav-label">In Chapter</span><span class="nav-num">Chapter 46</span><span class="nav-title">LLM-as-Judge &amp; Automated Evaluation</span></a>
</nav>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
'''

CHAPTER_INDEX = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter 46: LLM-as-Judge and Automated Evaluation. Judge reliability, debiasing techniques, training judge models, multi-judge ensembles, production patterns." name="description"/>
<title>Chapter 46: LLM-as-Judge &amp; Automated Evaluation | Building Conversational AI with LLMs and Agents</title>
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
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part IX: LLM Evaluation &amp; Observability</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Chapter 46</span></div>
<h1>LLM-as-Judge &amp; Automated Evaluation</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 46: LLM-as-Judge &amp; Automated Evaluation" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>LLM-as-Judge is the dominant automated-evaluation pattern in 2025-2026: a powerful LLM scores outputs from other LLMs against a rubric. It works because grading is often easier than generating, but it brings its own bias profile (position, length, verbosity, self-preference). This chapter covers when to use it, how to debias it, how to train custom judges, and the multi-judge ensemble patterns that make it production-grade.</p>
</div>
<h2>Sections in This Chapter</h2>
<ul class="sections-list">
{section_cards}
</ul>
<nav class="chapter-nav">
<a class="up" href="../index.html"><span class="nav-label">In Part</span><span class="nav-num">Part IX</span><span class="nav-title">LLM Evaluation &amp; Observability</span></a>
</nav>
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
'''


def main():
    src = ROOT / SOURCE_SEC
    if not src.exists():
        print(f'ERR: source not found')
        return

    html = src.read_text(encoding='utf-8')
    blocks = extract_h2_blocks(html)
    print(f'Found {len(blocks)} H2 blocks in sec 42.8')

    new_dir = ROOT / NEW_PART / NEW_MODULE
    new_dir.mkdir(parents=True, exist_ok=True)
    (new_dir / 'images').mkdir(exist_ok=True)

    section_cards = []
    for new_y, title, h2_indices in SECTIONS_PLAN:
        combined = ''
        for idx in h2_indices:
            if idx < len(blocks):
                bh = blocks[idx]['html']
                bh = re.sub(r'\bid="42-8-(\d+)-', f'id="46-{new_y}-\\1-', bh)
                bh = re.sub(r'\bhref="#42-8-(\d+)-', f'href="#46-{new_y}-\\1-', bh)
                combined += bh + '\n'
        # If no content (overflow indices), provide a stub
        if not combined.strip():
            combined = f'<p>This section covers {title.lower()}. Content forthcoming.</p>'

        page = SECTION_TEMPLATE.format(sec_num=f'46.{new_y}', sec_title=title, body=combined)
        (new_dir / f'section-46.{new_y}.html').write_text(page, encoding='utf-8')
        section_cards.append(
            f'<li><a class="section-card" href="section-46.{new_y}.html">\n'
            f'<span class="section-num">46.{new_y}</span>\n'
            f'<span class="section-title">{title}</span>\n'
            f'<span class="section-desc">Promoted and expanded from old section 42.8.</span>\n'
            f'</a></li>'
        )

    (new_dir / 'index.html').write_text(
        CHAPTER_INDEX.format(section_cards='\n'.join(section_cards)),
        encoding='utf-8'
    )
    print(f'Created Ch 46 with {len(SECTIONS_PLAN)} sections')

    # Delete source
    subprocess.run(['git', 'rm', '-f', str(src)], cwd=ROOT, capture_output=True)
    print(f'Deleted source')

    # Update Ch 42 index — drop the 42.8 entry, renumber 42.9 -> 42.8
    ch42_dir = ROOT / 'part-9-llm-evaluation-observability/module-42-evaluation-foundations'
    sec_429 = ch42_dir / 'section-42.9.html'
    sec_428 = ch42_dir / 'section-42.8.html'
    if sec_429.exists() and not sec_428.exists():
        subprocess.run(['git', 'mv', str(sec_429), str(sec_428)], cwd=ROOT, capture_output=True)
        t = sec_428.read_text(encoding='utf-8')
        t = re.sub(r'<title>Section 42\.9:', '<title>Section 42.8:', t)
        t = re.sub(r'(<meta content=")Section 42\.9:', r'\1Section 42.8:', t)
        t = re.sub(r'<div class="page-current">Section 42\.9</div>',
                   '<div class="page-current">Section 42.8</div>', t)
        t = re.sub(r'\bSection 42\.9\b', 'Section 42.8', t)
        t = re.sub(r'\b42\.9\.(\d+)\b', r'42.8.\1', t)
        t = re.sub(r'\bid="42-9-', 'id="42-8-', t)
        t = re.sub(r'\bhref="#42-9-', 'href="#42-8-', t)
        sec_428.write_text(t, encoding='utf-8')

    # Update Ch 10/42 index (drop 42.8 entry that pointed to LLM-as-Judge, since now that lives in Ch 46)
    # Also: the 42.9 -> 42.8 rename means we need to update the ch 42 index entry
    ch42_idx = ch42_dir / 'index.html'
    if ch42_idx.exists():
        text = ch42_idx.read_text(encoding='utf-8')
        # Remove the OLD 42.8 (LLM-as-Judge) entry
        text = re.sub(
            r'<li><a class="section-card" href="section-42\.8\.html">[\s\S]*?LLM-as-Judge[\s\S]*?</a></li>\s*',
            '', text
        )
        # The new 42.8 is what was 42.9 (Long-Context Benchmarks) — rewrite ref
        text = text.replace('section-42.9.html', 'section-42.8.html').replace('>42.9<', '>42.8<')
        ch42_idx.write_text(text, encoding='utf-8')
        print('Updated Ch 42 index')

    # Update Part 9 index with Ch 46 card
    part9_idx = ROOT / NEW_PART / 'index.html'
    text = part9_idx.read_text(encoding='utf-8')
    if 'module-46-llm-as-judge' not in text:
        new_card = f'''<div class="chapter-card">
<div class="chapter-card-header"><span class="mod-num">Chapter 46</span> LLM-as-Judge &amp; Automated Evaluation</div>
<div class="chapter-card-body">
<ul class="section-list">
'''
        for new_y, title, _ in SECTIONS_PLAN:
            new_card += f'<li><a href="{NEW_MODULE}/section-46.{new_y}.html"><span class="sec-num">46.{new_y}</span> {title}</a></li>\n'
        new_card += '</ul>\n</div>\n</div>\n'
        text = text.replace('</main>', new_card + '</main>', 1)
        part9_idx.write_text(text, encoding='utf-8')
        print('Added Ch 46 card to Part 9 index')

    # Rewrite refs to old sec 42.8 -> Ch 46 index
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text = re.sub(
            r'(href="[^"]*?)module-42-evaluation-foundations/section-42\.8\.html(#[^"]*)?"',
            rf'\1{NEW_MODULE}/index.html"',
            text
        )
        # Also need to fix internal Ch 42 refs that pointed at 42.9 -> 42.8
        text = re.sub(r'\bsection-42\.9\.html\b', 'section-42.8.html', text)
        text = re.sub(r'\bSection 42\.9\b', 'Section 42.8', text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    print(f'Cross-refs updated in {n} files')


if __name__ == '__main__':
    main()
