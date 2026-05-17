"""Wave 12: rebuild each part's index.html chapter-card-list from filesystem reality.

Issues addressed:
  - Part 5 index has no chapter cards (placeholder comment only)
  - Part 7 index missing Ch 31/32/33 cards
  - Part 8 index missing Ch 37 card
  - Parts 10/11/12/13 index pages have empty placeholders
  - Part 14 has 9 cards for 5 modules (duplicates Ch 68, 69, 70, 71)
  - Part 15 has phantom Ch 79/80 cards pointing to module-78 sections
  - Part 16 triple-numbering conflict
  - Plus rebuild appendices/index.html

Strategy: walk each part dir, list module-NN-slug dirs in numerical order, read
each module's index.html for h1 + section cards, generate one chapter-card per
module. Replace the chapter-card-list block in the part's index.html.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

# Parts that need rebuild (all of them — the safest)
PARTS = [
    'part-1-llm-building-blocks',
    'part-2-understanding-llms',
    'part-3-working-with-llms',
    'part-4-training-adaptation',
    'part-5-multimodal-llms',
    'part-6-agentic-ai',
    'part-7-retrieval-information-extraction-with-llms',
    'part-8-conversational-ai-with-llms',
    'part-9-llm-evaluation-observability',
    'part-10-llm-security-runtime-safety',
    'part-11-llm-ethics-trust-governance',
    'part-12-llm-systems-at-scale',
    'part-13-llmops-lifecycle',
    'part-14-designing-llm-agent-products',
    'part-15-applications-of-llms-across-industries',
    'part-16-llm-agentic-ai-research-frontiers',
]


def extract_module_info(module_dir):
    """Extract chapter number, title, and section list from a module dir."""
    idx = module_dir / 'index.html'
    info = {
        'module_name': module_dir.name,
        'ch_num': None,
        'ch_title': None,
        'sections': [],  # list of (section_num, section_title, file_basename)
    }

    # Parse module number from dir name: module-NN-slug
    m = re.match(r'module-(\d+)-', module_dir.name)
    if m:
        info['ch_num'] = int(m.group(1))

    if not idx.exists():
        return info

    text = idx.read_text(encoding='utf-8')

    # Find h1 — prefer the one inside <header>/<main>
    h1_match = re.search(r'<h1>([^<]+)</h1>', text)
    if h1_match:
        info['ch_title'] = h1_match.group(1).strip()

    # Try to find chapter title from <title> tag if h1 was generic
    if not info['ch_title']:
        t_match = re.search(r'<title>(?:Chapter \d+:\s*)?([^<|]+)', text)
        if t_match:
            info['ch_title'] = t_match.group(1).strip()

    # Get section cards from sections-list
    # Pattern: <a class="section-card" href="section-X.Y.html">...<span class="section-num">X.Y</span>
    #          <span class="section-title">TITLE</span>...
    for m in re.finditer(
        r'<a class="section-card" href="(section-[\d.]+\.html)"[^>]*>\s*'
        r'<span class="section-num">([^<]+)</span>\s*'
        r'<span class="section-title">([^<]+)</span>',
        text
    ):
        info['sections'].append((m.group(2), m.group(3), m.group(1)))

    # Also try the regular sections-list format
    if not info['sections']:
        for m in re.finditer(
            r'<a href="(section-[\d.]+\.html)"[^>]*>\s*'
            r'<span class="sec-num">([^<]+)</span>\s*([^<]+)<',
            text
        ):
            info['sections'].append((m.group(2), m.group(3).strip(), m.group(1)))

    # If we still don't have sections, list them from disk
    if not info['sections']:
        for section_file in sorted(module_dir.glob('section-*.html'),
                                    key=lambda p: [int(x) for x in re.findall(r'\d+', p.name)]):
            # Extract section number from filename: section-X.Y.html
            sm = re.match(r'section-(\d+)\.(\d+)\.html', section_file.name)
            if not sm:
                continue
            sec_num = f'{sm.group(1)}.{sm.group(2)}'
            # Extract title from the section file's h1
            stext = section_file.read_text(encoding='utf-8')
            sh1 = re.search(r'<h1>([^<]+)</h1>', stext)
            sec_title = sh1.group(1).strip() if sh1 else f'Section {sec_num}'
            info['sections'].append((sec_num, sec_title, section_file.name))

    return info


def build_chapter_card(module_dir_name, ch_num, ch_title, sections):
    """Build a single chapter-card HTML block."""
    lines = [
        '<div class="chapter-card">',
        f'<div class="chapter-card-header"><span class="mod-num">Chapter {ch_num}</span> {ch_title}</div>',
        '<div class="chapter-card-body">',
        '<ul class="section-list">',
    ]
    for sec_num, sec_title, sec_file in sections:
        lines.append(
            f'<li><a href="{module_dir_name}/{sec_file}">'
            f'<span class="sec-num">{sec_num}</span> {sec_title}</a></li>'
        )
    lines.extend(['</ul>', '</div>', '</div>'])
    return '\n'.join(lines)


def rebuild_part_index(part_slug):
    part_dir = ROOT / part_slug
    idx = part_dir / 'index.html'
    if not idx.exists():
        print(f'  {part_slug}: no index.html, skip')
        return

    # Find all module dirs sorted by number
    modules = sorted(
        [d for d in part_dir.iterdir() if d.is_dir() and re.match(r'module-(\d+)-', d.name)],
        key=lambda d: int(re.match(r'module-(\d+)-', d.name).group(1))
    )

    cards = []
    for m in modules:
        info = extract_module_info(m)
        if info['ch_num'] is None or info['ch_title'] is None:
            print(f'  WARN: {m.name} missing ch_num or ch_title; skipping')
            continue
        # Take a Reasonable upper bound of sections (the real ones)
        cards.append(build_chapter_card(
            m.name, info['ch_num'], info['ch_title'], info['sections']
        ))

    if not cards:
        print(f'  {part_slug}: no modules found')
        return

    new_cards = '\n'.join(cards)
    text = idx.read_text(encoding='utf-8')

    # Look for existing chapter-card-list block, or insert after <h2>Chapters</h2>
    # Patterns to consider:
    #   <div class="chapter-card-list">...</div>
    #   <h2>Chapters</h2>... [maybe direct chapter-card divs]

    if '<div class="chapter-card-list">' in text:
        # Replace entire block
        text = re.sub(
            r'<div class="chapter-card-list">[\s\S]*?</div>\s*(?=</main>|<h2|<footer)',
            f'<div class="chapter-card-list">\n{new_cards}\n</div>\n',
            text
        )
    elif '<div class="chapter-card">' in text:
        # Existing cards — replace from first chapter-card to last (consecutive)
        # Find first and last
        first = text.find('<div class="chapter-card">')
        # Find last </div></div> that ends a chapter-card pattern
        # Easier: collect ALL chapter-card blocks and replace the range
        # We assume they're all consecutive (typical pattern)
        # Use a non-greedy strip from first chapter-card to before </main>
        text_before = text[:first]
        text_after = text[first:]
        # Strip everything from first chapter-card up to </main>
        after_match = re.search(r'(</main>|<footer)', text_after)
        if after_match:
            text = text_before + f'<div class="chapter-card-list">\n{new_cards}\n</div>\n' + text_after[after_match.start():]
    else:
        # No existing structure; insert before </main>
        text = text.replace(
            '</main>',
            f'<h2>Chapters</h2>\n<div class="chapter-card-list">\n{new_cards}\n</div>\n</main>',
            1
        )

    idx.write_text(text, encoding='utf-8')
    print(f'  {part_slug}: rebuilt with {len(cards)} chapter cards')


def rebuild_appendices_index():
    """Rebuild appendices/index.html with the 3-appendix layout (A/B/C)."""
    p = ROOT / 'appendices' / 'index.html'
    text = p.read_text(encoding='utf-8')

    # Build chapter-card-list for the 3 appendices
    cards = '''<div class="chapter-card">
<div class="chapter-card-header"><span class="mod-num">Appendix A</span> Mathematical Foundations</div>
<div class="chapter-card-body">
<p>The essential linear algebra, probability, calculus, and information theory that power every transformer. Six sections covering vectors and matrices, probability distributions, derivatives and gradient descent, entropy and KL divergence, and information theory for language models.</p>
<a href="appendix-a-mathematical-foundations/index.html" class="card-cta">Open Appendix A &rarr;</a>
</div>
</div>
<div class="chapter-card">
<div class="chapter-card-header"><span class="mod-num">Appendix B</span> Course Syllabi</div>
<div class="chapter-card-body">
<p>Five tested course tracks (undergraduate engineering, undergraduate research, graduate engineering, graduate research, professional bootcamp) with week-by-week schedules, prerequisites, and assessment rubrics for instructors building courses on this book.</p>
<a href="appendix-b-course-syllabi/index.html" class="card-cta">Open Appendix B &rarr;</a>
</div>
</div>
<div class="chapter-card">
<div class="chapter-card-header"><span class="mod-num">Appendix C</span> Reading Pathways</div>
<div class="chapter-card-body">
<p>Per-audience reading guides for engineers, researchers, founders/PMs, and self-study learners. Each pathway tells you what to read in what order, roughly how long it takes, and what you can do after.</p>
<a href="appendix-c-reading-pathways/index.html" class="card-cta">Open Appendix C &rarr;</a>
</div>
</div>'''

    # The existing structure has two empty H2 headers; replace them with a single H2 + the cards
    # Find <h2 id="group-foundations">Foundations</h2>...<h2 id="group-for-instructors">For Instructors</h2>
    # and replace with sectioned cards.
    new_section = f'''<h2 id="group-foundations">Foundations</h2>
<div class="chapter-card-list">
{cards.split('</div>\n<div class="chapter-card">\n<div class="chapter-card-header"><span class="mod-num">Appendix B</span>')[0]}</div>
</div>
<h2 id="group-for-instructors">For Instructors</h2>
<div class="chapter-card-list">
<div class="chapter-card">
<div class="chapter-card-header"><span class="mod-num">Appendix B</span> Course Syllabi</div>
<div class="chapter-card-body">
<p>Five tested course tracks (undergraduate engineering, undergraduate research, graduate engineering, graduate research, professional bootcamp) with week-by-week schedules, prerequisites, and assessment rubrics for instructors building courses on this book.</p>
<a href="appendix-b-course-syllabi/index.html" class="card-cta">Open Appendix B &rarr;</a>
</div>
</div>
<div class="chapter-card">
<div class="chapter-card-header"><span class="mod-num">Appendix C</span> Reading Pathways</div>
<div class="chapter-card-body">
<p>Per-audience reading guides for engineers, researchers, founders/PMs, and self-study learners. Each pathway tells you what to read in what order, roughly how long it takes, and what you can do after.</p>
<a href="appendix-c-reading-pathways/index.html" class="card-cta">Open Appendix C &rarr;</a>
</div>
</div>
</div>'''

    text = re.sub(
        r'<h2 id="group-foundations">Foundations</h2>\s*<h2 id="group-for-instructors">For Instructors</h2>',
        new_section,
        text
    )
    p.write_text(text, encoding='utf-8')
    print('  Rebuilt appendices/index.html')


def main():
    for part_slug in PARTS:
        rebuild_part_index(part_slug)
    rebuild_appendices_index()


if __name__ == '__main__':
    main()
