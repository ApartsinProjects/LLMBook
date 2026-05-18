"""Wave 9 step A: promote sec 13.5 (Structured Information Extraction & NER) to its own chapter.

The current sec 13.5 is a 79 KB monster with 12 H2 sub-sections. Per the v9 plan
this becomes Part 7 Ch 34 (Structured Information Extraction & NER), with the
12 H2 sub-sections split into ~5 first-class sections.

Process:
  1. Read the current sec 13.5 content
  2. Identify H2 split points
  3. Create new module-34-structured-info-extraction-ner/ in Part 7
  4. Create section files for each split (section-34.1.html ... section-34.5.html)
  5. Create chapter index.html
  6. Delete the original sec 13.5
  7. Update part-3 chapter-13 index (drop the 13.5 entry)
  8. Update part-7 part-index (add chapter card for ch 34)
  9. Rewrite cross-refs across the book
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

NEW_MODULE_NAME = 'module-34-structured-information-extraction-ner'
NEW_PART = 'part-7-retrieval-information-extraction-with-llms'
SOURCE_SEC = 'part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html'

# Group the 12 H2 sub-sections of sec 13.5 into 5 new chapters
# Source H2s observed:
#   13.5.1 The Information Extraction Landscape
#   13.5.2 Classical IE with spaCy
#   13.5.3 Open Information Extraction
#   13.5.4 Hybrid IE Architectures
#   13.5.5 Production Deployment Patterns
#   13.5.6 End-to-End Example: Financial Event Extraction
#   13.5.7 Coreference Resolution
#   13.5.8 Integrated Document Understanding Pipeline
#   ... (12 total — script will partition by index)

# Partition strategy: group H2s into 5 sections
SECTIONS_PLAN = [
    # (new_section_num, title, h2_indices, anchor_id_prefix)
    (1, 'The Information Extraction Landscape', [0], '34-1'),
    (2, 'Classical and Open Information Extraction', [1, 2], '34-2'),
    (3, 'Hybrid IE Architectures with LLMs', [3], '34-3'),
    (4, 'Production IE Deployment Patterns', [4, 5], '34-4'),
    (5, 'Coreference Resolution and Document Pipelines', [6, 7], '34-5'),
]


def extract_h2_blocks(html):
    """Extract H2 sections from the main content area."""
    main_m = re.search(r'<main[^>]*>([\s\S]*?)</main>', html)
    if not main_m: return []
    body = main_m.group(1)

    # Find all <h2 ...>...</h2> positions
    h2_positions = []
    for m in re.finditer(r'<h2[^>]*>([^<]+)</h2>', body):
        h2_positions.append((m.start(), m.end(), m.group(1)))

    if not h2_positions: return []

    # Each H2 block is from its start to the start of the next H2 (or end of body)
    blocks = []
    for i, (start, end, title) in enumerate(h2_positions):
        block_end = h2_positions[i+1][0] if i+1 < len(h2_positions) else len(body)
        block_html = body[start:block_end]
        blocks.append({'title': title.strip(), 'html': block_html})
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
<link href="../../vendor/prism/prism-theme.css" rel="stylesheet"/>
<script defer="" src="../../vendor/prism/prism-bundle.min.js"></script>
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
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part VII: Retrieval &amp; Information Extraction with LLMs</a><span class="bc-sep">&rsaquo;</span><a href="index.html">Chapter 34: Structured Information Extraction &amp; NER</a></div>
<h1>{sec_title}</h1><div class="page-current">Section {sec_num}</div>
</header>
<main class="content"><span class="pagefind-meta-injected" data-pagefind-meta="part:Part VII: Retrieval &amp; Information Extraction with LLMs" hidden=""></span><span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 34: Structured Information Extraction &amp; NER" hidden=""></span>
{body}
</main>
<nav class="chapter-nav">
<a class="up" href="index.html"><span class="nav-label">In Chapter</span><span class="nav-num">Chapter 34</span><span class="nav-title">Structured Information Extraction &amp; NER</span></a>
</nav>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
'''

CHAPTER_INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter 34: Structured Information Extraction &amp; NER. Information extraction landscape, classical and open IE, hybrid LLM architectures, production deployment, coreference resolution and document pipelines." name="description"/>
<title>Chapter 34: Structured Information Extraction &amp; NER | Building Conversational AI with LLMs and Agents</title>
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
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part VII: Retrieval &amp; Information Extraction with LLMs</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Chapter 34</span></div>
<h1>Structured Information Extraction &amp; NER</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 34: Structured Information Extraction &amp; NER" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>Information extraction is how unstructured text becomes structured data: named entities, relations, events, and the typed records that downstream pipelines need. This chapter covers the spectrum from classical NER and OpenIE through hybrid LLM architectures to production deployment patterns, with coreference resolution and document-level pipelines as the integrating capstone.</p>
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


def main():
    src = ROOT / SOURCE_SEC
    if not src.exists():
        print(f'ERR: source {SOURCE_SEC} not found')
        return

    # Read and parse
    html = src.read_text(encoding='utf-8')
    blocks = extract_h2_blocks(html)
    print(f'Found {len(blocks)} H2 blocks in sec 13.5')

    # Create the new module dir
    new_dir = ROOT / NEW_PART / NEW_MODULE_NAME
    new_dir.mkdir(parents=True, exist_ok=True)
    (new_dir / 'images').mkdir(exist_ok=True)
    print(f'Created: {new_dir.relative_to(ROOT)}')

    # Build each new section file
    section_cards = []
    for new_y, title, h2_indices, anchor_prefix in SECTIONS_PLAN:
        # Combine the chosen H2 blocks
        combined_html = ''
        for idx in h2_indices:
            if idx < len(blocks):
                # Rewrite anchor IDs from 13-5-X-Y to 34-Y-Z
                block_html = blocks[idx]['html']
                # Update h2 to new numbering
                block_html = re.sub(
                    r'<h2[^>]*>([^<]+)</h2>',
                    lambda m: m.group(0),  # leave original H2 text for now
                    block_html
                )
                combined_html += block_html + '\n'

        # Rewrite anchor IDs from 13-5- to 34-{new_y}-
        combined_html = re.sub(r'\bid="13-5-(\d+)-', f'id="34-{new_y}-\\1-', combined_html)
        combined_html = re.sub(r'\bhref="#13-5-(\d+)-', f'href="#34-{new_y}-\\1-', combined_html)

        # Rewrite "13.5.X.Y" to "34.{new_y}.Y" in body text
        combined_html = re.sub(r'\b13\.5\.(\d+)\.(\d+)\b', rf'34.{new_y}.\1.\2', combined_html)
        combined_html = re.sub(r'\b13\.5\.(\d+)\b', rf'34.{new_y}.\1', combined_html)
        # Rewrite "Section 13.5" -> chapter 34 reference (rare in sub-section, but be safe)
        combined_html = re.sub(r'\bSection 13\.5\b', 'Chapter 34', combined_html)

        section_html = SECTION_TEMPLATE.format(
            sec_num=f'34.{new_y}',
            sec_title=title,
            body=combined_html,
        )
        section_path = new_dir / f'section-34.{new_y}.html'
        section_path.write_text(section_html, encoding='utf-8')

        section_cards.append(
            f'<li><a class="section-card" href="section-34.{new_y}.html">\n'
            f'<span class="section-num">34.{new_y}</span>\n'
            f'<span class="section-title">{title}</span>\n'
            f'<span class="section-desc">Promoted from old section 15.5.</span>\n'
            f'</a></li>'
        )

    # Write chapter index
    index_html = CHAPTER_INDEX_TEMPLATE.format(section_cards='\n'.join(section_cards))
    (new_dir / 'index.html').write_text(index_html, encoding='utf-8')
    print(f'Created chapter index with {len(SECTIONS_PLAN)} sections')

    # Delete the original sec 13.5
    r = subprocess.run(['git', 'rm', '-f', str(src)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode == 0:
        print(f'Deleted source: {SOURCE_SEC}')

    # Update part-3 chapter-13 index to drop the 13.5 entry
    ch13_idx = ROOT / 'part-3-working-with-llms/module-13-hybrid-ml-llm/index.html'
    if ch13_idx.exists():
        text = ch13_idx.read_text(encoding='utf-8')
        # Remove the section-card for 13.5
        text = re.sub(
            r'<li><a class="section-card" href="section-13\.5\.html">[\s\S]*?</a></li>\s*',
            '', text
        )
        ch13_idx.write_text(text, encoding='utf-8')
        print('Updated Ch 13 index (dropped 13.5 entry)')

    # Update part-7 index to add chapter card for Ch 34
    part7_idx = ROOT / NEW_PART / 'index.html'
    text = part7_idx.read_text(encoding='utf-8')
    if 'module-34-structured-information-extraction-ner' not in text:
        new_card = f'''<div class="chapter-card">
<div class="chapter-card-header"><span class="mod-num">Chapter 34</span> Structured Information Extraction &amp; NER</div>
<div class="chapter-card-body">
<ul class="section-list">
'''
        for new_y, title, _, _ in SECTIONS_PLAN:
            new_card += f'<li><a href="{NEW_MODULE_NAME}/section-34.{new_y}.html"><span class="sec-num">34.{new_y}</span> {title}</a></li>\n'
        new_card += '''</ul>
</div>
</div>
'''
        # Insert before </main>
        text = text.replace('</main>', new_card + '</main>', 1)
        part7_idx.write_text(text, encoding='utf-8')
        print('Added Ch 34 card to Part 7 index')

    # Rewrite refs across the book: old sec 13.5 -> Ch 34 index
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Replace refs to old section-13.5.html
        text = re.sub(
            r'(href="[^"]*?)module-13-hybrid-ml-llm/section-13\.5\.html(#[^"]*)?"',
            rf'\1{NEW_PART}/{NEW_MODULE_NAME}/index.html"',
            text
        )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'Updated cross-refs in {n_files} files')


if __name__ == '__main__':
    main()
