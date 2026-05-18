"""Add level badges to section cards in module index.html files.

For each module:
- Reads its index.html
- Finds <a class="section-card" ...> entries inside the sections-list
- Inserts a <span class="level-badge LEVEL" title="..."> before closing </a>
- Heuristic: section 1 = basic (entry); middle sections = intermediate;
  final/lab/advanced/research-flavored sections = advanced.
"""
import re
import sys
from pathlib import Path

ROOT = Path(r'E:/Projects/BookBlogsHome/LLMBook')

TARGETS = [
    'part-1-llm-building-blocks/module-00-ml-pytorch-foundations',
    'part-1-llm-building-blocks/module-01-foundations-nlp-text-representation',
    'part-1-llm-building-blocks/module-02-sequence-models-attention',
    'part-1-llm-building-blocks/module-03-transformer-architecture',
    'part-1-llm-building-blocks/module-04-decoding-text-generation',
    'part-2-understanding-llms/module-06-pretraining-scaling-laws',
    'part-2-understanding-llms/module-07-modern-llm-landscape',
    'part-2-understanding-llms/module-08-reasoning-test-time-compute',
    'part-2-understanding-llms/module-09-inference-optimization',
    'part-2-understanding-llms/module-10-interpretability',
    'part-3-working-with-llms/module-11-llm-apis',
    'part-3-working-with-llms/module-12-prompt-engineering',
    'part-3-working-with-llms/module-13-hybrid-ml-llm',
    'part-4-training-adaptation/module-15-synthetic-data',
    'part-4-training-adaptation/module-16-fine-tuning-fundamentals',
    'part-4-training-adaptation/module-17-peft',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo',
    'part-5-multimodal-llms/module-20-audio-music-generation',
    'part-5-multimodal-llms/module-21-document-understanding-ocr',
    'part-5-multimodal-llms/module-22-vision-language-models',
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes',
    'part-5-multimodal-llms/module-24-vla-models',
    'part-6-agentic-ai/module-26-ai-agents',
    'part-6-agentic-ai/module-27-tool-use-protocols',
    'part-6-agentic-ai/module-28-multi-agent-systems',
    'part-6-agentic-ai/module-29-specialized-agents',
    'part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db',
    'part-7-retrieval-information-extraction-with-llms/module-32-rag',
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag',
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner',
    'part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag',
    'part-8-conversational-ai-with-llms/module-37-conversational-ai',
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations',
    'part-9-llm-evaluation-observability/module-43-specialized-evaluation',
    'part-9-llm-evaluation-observability/module-44-online-eval-observability',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation',
]


def assign_level(idx, total, title_text):
    """Pick basic/intermediate/advanced based on section position and keywords."""
    t = title_text.lower()
    # Strong advanced cues
    advanced_kw = ['lab:', 'advanced', 'research', 'frontier', 'scaling',
                   'distributed', 'production', 'optimization', 'optimization',
                   'efficient', 'large-scale', 'parallelism', 'theory',
                   'in-context learning theory', 'mechanistic', 'sparse',
                   'mixture-of-experts', 'speculative', 'paged', 'quantization',
                   'red team', 'adversarial', 'edge', 'on-device', 'flash',
                   'continuous batching', 'pruning', 'distillation']
    # Entry-level cues
    entry_kw = ['introduction', 'overview', 'foundations', 'basics',
                'getting started', 'why', 'what is', 'fundamentals',
                'primer', 'landscape', 'big picture']
    if any(kw in t for kw in advanced_kw):
        return ('advanced', 'Advanced')
    if any(kw in t for kw in entry_kw):
        return ('basic', 'Entry')
    # Position-based fallback
    if total <= 3:
        # Few sections: 1st entry, last advanced, middle intermediate
        if idx == 0:
            return ('basic', 'Entry')
        if idx == total - 1:
            return ('advanced', 'Advanced')
        return ('intermediate', 'Intermediate')
    # Many sections: first 1-2 entry, last 1-2 advanced, rest intermediate
    if idx == 0:
        return ('basic', 'Entry')
    if idx == 1 and total >= 6:
        return ('basic', 'Entry')
    if idx >= total - 2:
        return ('advanced', 'Advanced')
    return ('intermediate', 'Intermediate')


# Pattern matches each <a class="section-card" ...>...</a> block
CARD_RE = re.compile(
    r'(<a class="section-card"[^>]*>)(.*?)(</a>)',
    re.DOTALL,
)
TITLE_RE = re.compile(r'<span class="section-title">(.*?)</span>', re.DOTALL)


def process_index(idx_path: Path) -> tuple[int, list[str]]:
    """Returns (num_badges_inserted, level_summary)."""
    text = idx_path.read_text(encoding='utf-8')
    if 'class="level-badge' in text:
        return (0, ['already has badges'])

    cards = list(CARD_RE.finditer(text))
    if not cards:
        return (0, ['no section-card matches'])

    total = len(cards)
    new_text = text
    inserted = 0
    summary = []
    # Process in reverse so offsets stay valid
    for i, m in enumerate(cards):
        pass  # we'll do forward with replace

    # Build replacement map: card_index -> (open, inner, close, new_block)
    # We must replace each in order; since CARD_RE may match identical strings,
    # build the new HTML by walking matches sequentially.
    parts = []
    last_end = 0
    for i, m in enumerate(cards):
        parts.append(text[last_end:m.start()])
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        title_m = TITLE_RE.search(inner)
        title_text = title_m.group(1) if title_m else ''
        # strip simple HTML tags from title for keyword analysis
        plain_title = re.sub(r'<[^>]+>', '', title_text)
        level_class, level_label = assign_level(i, total, plain_title)
        badge = (
            f'<span class="level-badge {level_class}" '
            f'title="{level_label}">{level_label}</span>'
        )
        # Insert badge before closing </a>, preserve trailing whitespace
        new_inner = inner.rstrip()
        trailing_ws = inner[len(new_inner):]
        new_block = f'{open_tag}{new_inner}\n{badge}{trailing_ws}{close_tag}'
        parts.append(new_block)
        last_end = m.end()
        inserted += 1
        summary.append(f's{i+1}={level_class}')
    parts.append(text[last_end:])
    new_text = ''.join(parts)

    idx_path.write_text(new_text, encoding='utf-8')
    return (inserted, summary)


def main():
    overall = []
    for tgt in TARGETS:
        idx = ROOT / tgt / 'index.html'
        if not idx.exists():
            print(f'MISSING: {tgt}')
            continue
        n, summary = process_index(idx)
        print(f'{tgt}: +{n} badges  {summary}')
        overall.append((tgt, n))
    print(f'\nTotal modules touched: {sum(1 for _, n in overall if n > 0)}')
    print(f'Total badges inserted: {sum(n for _, n in overall)}')


if __name__ == '__main__':
    main()
