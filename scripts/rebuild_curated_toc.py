"""Rebuild the curated toc.html structure from disk reality.

Preserves:
  - front-matter section (curated; lists front-matter pages)
  - appendices section (curated; lists current appendices A/B/C/D/E/F/G after renumbering)

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
    ('I',    'LLM Building Blocks',                           'part-1-llm-building-blocks',                            'Math, ML/PyTorch prerequisites, NLP and text representation, tokenization, attention, transformers, decoding.'),
    ('II',   'Understanding LLMs',                            'part-2-understanding-llms',                              'Pre-training, scaling laws, modern landscape, reasoning, inference optimization, interpretability.'),
    ('III',  'Working with LLMs',                             'part-3-working-with-llms',                               'LLM APIs, prompt engineering, hybrid ML+LLM application patterns.'),
    ('IV',   'LLM Training and Adaptation',                   'part-4-training-adaptation',                             'Synthetic data, supervised fine-tuning, PEFT, RLHF / DPO / preference tuning, training tools.'),
    ('V',    'Multimodal LLMs',                               'part-5-multimodal-llms',                                 'Vision-language & Omni models, image/video/audio generation, document understanding, 3D, embodied AI / VLA / robotics.'),
    ('VI',   'Agentic AI',                                    'part-6-agentic-ai',                                      'Agent foundations, tool use (MCP / A2A), multi-agent systems, specialized agents.'),
    ('VII',  'Retrieval & Information Extraction with LLMs',  'part-7-retrieval-information-extraction-with-llms',      'Embeddings, structured information extraction & NER, RAG, knowledge graphs, cross-modal retrieval.'),
    ('VIII', 'Conversational AI with LLMs',                   'part-8-conversational-ai-with-llms',                     'Dialogue architecture, memory and context management, multi-turn flows, voice and realtime multimodal assistants.'),
    ('IX',   'LLM Evaluation & Observability',                'part-9-llm-evaluation-observability',                    'Quality metrics, LLM-as-judge, specialized evaluation, online monitoring, eval tools.'),
    ('X',    'LLM Security & Runtime Safety',                 'part-10-llm-security-runtime-safety',                    'Adversarial threats, guardrails, agent safety, privacy, security tooling.'),
    ('XI',   'LLM Ethics, Trust & Governance',                'part-11-llm-ethics-trust-governance',                    'Bias and hallucination, provenance and transparency, regulation and compliance, frontier safety.'),
    ('XII',  'LLM Systems at Scale',                          'part-12-llm-systems-at-scale',                           'Compute planning, distributed training systems, hardware and chip diversity, edge and on-device LLMs.'),
    ('XIII', 'LLMOps & Lifecycle Management',                 'part-13-llmops-lifecycle',                               'AI gateways and routing, workflow orchestration, containers, reliability and SLOs, model registry and lifecycle.'),
    ('XIV',  'Designing LLM & Agent-based Products',          'part-14-designing-llm-agent-products',                   'Ideation, product management, prototyping, MVP, economics, shipping, product tools.'),
    ('XV',   'Applications of LLMs Across Industries',        'part-15-applications-of-llms-across-industries',         'LLM use across legal, finance, healthcare, education, cybersecurity, government, and other domains.'),
    ('XVI',  'LLM & Agentic AI Research Frontiers',           'part-16-llm-agentic-ai-research-frontiers',              'Frontier architectures, theory and cognition, AGI trajectories, frontier research tooling.'),
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
