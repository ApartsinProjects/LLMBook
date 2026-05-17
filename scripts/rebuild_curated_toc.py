"""Rebuild the curated toc.html structure from disk reality.

Preserves:
  - front-matter section (curated; lists front-matter pages)
  - appendices section (curated; lists current appendices A/B/O/P/Q/R/S/T)

Regenerates from disk:
  - Parts I-XIII with their chapter lists
  - Each chapter's number, title, and subtitle
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOC = ROOT / 'toc.html'

PARTS_META = [
    ('I',    'Foundations',                                'part-1-foundations',                       'Math, ML, PyTorch, NLP basics, transformers, decoding, and the everyday tooling.'),
    ('II',   'Understanding LLMs',                          'part-2-understanding-llms',                'Pre-training, scaling laws, evaluation, alignment, frontier models, and reasoning models.'),
    ('III',  'Working with LLMs',                           'part-3-working-with-llms',                 'Prompts, structured output, tool use, and reasoning models for application builders.'),
    ('IV',   'LLM Training and Adaptation',                 'part-4-training-adapting',                 'Supervised fine-tuning, PEFT, RLHF / DPO / GRPO, post-training, and the training stack.'),
    ('V',    'Retrieval and Conversation with LLMs and Agents', 'part-5-retrieval-conversation',         'Embeddings, vector search, RAG, conversation design, memory, and the retrieval stack.'),
    ('VI',   'Agentic AI',                                  'part-6-agentic-ai',                        'Agent architectures, tool use, multi-agent systems, and the agent-framework stack.'),
    ('VII',  'Multimodal Generation',                       'part-7-multimodal-generation',             'Vision, audio, video, 3D, document understanding, robotics, and unified multimodal models.'),
    ('VIII', 'Evaluation of LLM-Based Systems',             'part-8-evaluation-production',             'Rigorous evaluation, observability, and the eval / monitoring stack.'),
    ('IX',   'LLM Safety, Security, and Ethics',            'part-9-safety-security-ethics',            'Threats, defenses, regulation, ethics, and the safety / guardrails stack.'),
    ('X',    'LLM Operations and Production Infrastructure', 'part-10-llmops',                          'Compute planning, serving, gateways, durable execution, reliability, and K8s-native operations.'),
    ('XI',   'Designing LLM-Based Products',                'part-11-designing-llm-products',           'Ideation, product management, MVPs, prototype-to-production, economics, and shipping.'),
    ('XII',  'Applications Across Industries',              'part-12-applications-across-industries',   'Legal, finance, healthcare, education, cybersecurity, government, manufacturing, creative, recommendation.'),
    ('XIII', 'Frontiers',                                   'part-13-frontiers',                        'Frontier architectures, theory, hardware, AGI trajectories, and the cutting-edge tooling.'),
]


def get_h1(p):
    if not p.exists(): return None
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    return m.group(1).strip() if m else None


def get_chapter_subtitle(idx_path):
    """Pull a short subtitle from the chapter index's big-picture callout or part-overview."""
    if not idx_path.exists(): return ''
    text = idx_path.read_text(encoding='utf-8')
    # Look at meta description for a one-sentence summary
    m = re.search(r'<meta content="(?:Chapter|Module) \d+:?[^.]+\.\s+([^"]+)"\s+name="description"', text)
    if m:
        s = m.group(1).strip()
        # First sentence only
        s = re.split(r'(?<=[.!?])\s+', s)[0]
        if len(s) > 200: s = s[:197] + '...'
        return s
    # Fall back to chapter-subtitle <p>
    m = re.search(r'<p class="chapter-subtitle">([^<]+)</p>', text)
    if m: return m.group(1).strip()
    return ''


def chapter_count_section_count(part_slug):
    """Return (chapter_count, section_count) for a part."""
    part_dir = ROOT / part_slug
    mods = list(part_dir.glob('module-*/'))
    secs = sum(1 for m in mods for _ in m.glob('section-*.html'))
    return (len(mods), secs)


def build_part_section(roman, title, part_slug, subtitle):
    """Build a <section class="toc-part"> block for one part."""
    part_dir = ROOT / part_slug
    if not part_dir.exists(): return ''
    # Collect chapters in order
    modules = sorted(part_dir.glob('module-*/'),
                    key=lambda d: int(re.match(r'module-(\d+)-', d.name).group(1)))
    ch_count, sec_count = chapter_count_section_count(part_slug)

    items = []
    for mod in modules:
        m = re.match(r'module-(\d+)-', mod.name)
        if not m: continue
        ch_num = int(m.group(1))
        ch_title = get_h1(mod / 'index.html') or '?'
        # strip "Chapter N: " prefix if present
        ch_title = re.sub(r'^Chapter\s+\d+:?\s*', '', ch_title)
        ch_subtitle = get_chapter_subtitle(mod / 'index.html')

        sub_html = f'<span class="toc-chapter-subtitle">{ch_subtitle}</span>\n' if ch_subtitle else ''
        items.append(
            f'<li class="toc-chapter">\n'
            f'<a href="{part_slug}/{mod.name}/index.html">\n'
            f'<span class="toc-chapter-num" aria-label="Chapter {ch_num}">{ch_num}</span>\n'
            f'<span class="toc-chapter-title">{ch_title}</span>\n'
            f'{sub_html}'
            f'</a>\n'
            f'</li>'
        )

    items_html = '\n'.join(items)
    part_num = int(re.match(r'part-(\d+)-', part_slug).group(1))
    return (
        f'<section class="toc-part" id="part-{part_num}" data-part-num="{part_num}">\n'
        f'<header class="toc-part-header">\n'
        f'<h2 class="toc-part-title"><span class="toc-part-prefix">Part {roman}</span> '
        f'<span class="toc-part-sep">·</span> <a href="{part_slug}/index.html">{title}</a></h2>'
        f'<span class="toc-part-count">{ch_count} chapters · {sec_count} sections</span>\n'
        f'<p class="toc-part-subtitle">{subtitle}</p>\n'
        f'</header>\n'
        f'<ol class="toc-chapter-list">\n'
        f'{items_html}\n'
        f'</ol>\n'
        f'</section>'
    )


def main():
    text = TOC.read_text(encoding='utf-8')

    # Find the section block for each part (id="part-N")
    new_text = text
    for roman, title, part_slug, subtitle in PARTS_META:
        part_num = int(re.match(r'part-(\d+)-', part_slug).group(1))
        new_block = build_part_section(roman, title, part_slug, subtitle)
        if not new_block: continue

        # Try to replace existing section with id="part-N"
        pat = re.compile(rf'<section class="toc-part"[^>]*id="part-{part_num}"[^>]*>[\s\S]*?</section>')
        if pat.search(new_text):
            new_text = pat.sub(new_block, new_text, count=1)
            print(f'  Replaced Part {roman} (part-{part_num})')
        else:
            # Insert before appendices section
            app_pat = re.compile(r'<section class="toc-part toc-appendices"|<section class="toc-part"[^>]*id="appendices"')
            m = app_pat.search(new_text)
            if m:
                new_text = new_text[:m.start()] + new_block + '\n\n' + new_text[m.start():]
                print(f'  Inserted Part {roman} (part-{part_num}) before appendices')
            else:
                print(f'  WARN: could not insert Part {roman} (part-{part_num})')

    TOC.write_text(new_text, encoding='utf-8')


if __name__ == '__main__':
    main()
