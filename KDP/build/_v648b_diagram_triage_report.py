"""v6.48b: Triage report — for each linear-step diagram, show the .mmd
content + figcaption + surrounding prose, and apply heuristic recommendation:

  DROP:    pure step-list, no synthesizing insight; prose says the same thing
  KEEP:    linear but informative (named tools/components, real architecture)
  CONVERT: has potential but needs richer visualization

Heuristics:
  - DROP if .mmd has only generic step-words (Input, Process, Output, Step 1...)
  - KEEP if .mmd has named specific tools/products/algorithms
  - CONVERT if .mmd has quantitative or structural info worth illustrating
"""
from __future__ import annotations
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
IN_CSV = ROOT / 'KDP' / 'validation' / 'linear_diagram_audit.csv'
OUT_CSV = ROOT / 'KDP' / 'validation' / 'linear_diagram_triage.csv'
OUT_MD = ROOT / 'KDP' / 'validation' / 'linear_diagram_triage.md'

GENERIC_STEP_WORDS = {
    'input', 'output', 'process', 'step', 'start', 'end', 'next',
    'before', 'after', 'apply', 'use', 'see',
}


def extract_node_labels(mmd_text: str) -> list[str]:
    """Pull human-readable labels from Mermaid node definitions."""
    labels = []
    # Patterns: NodeId[Label], NodeId(Label), NodeId{Label}, NodeId("Label")
    for m in re.finditer(r'\w+\s*[\[\(\{]"?([^"\]\)\}]+)"?[\]\)\}]', mmd_text):
        labels.append(m.group(1).strip())
    return labels


def has_specific_names(labels: list[str]) -> bool:
    """Detect named tools/algorithms/products in node labels."""
    text = ' '.join(labels).lower()
    indicators = [
        'gpt', 'bert', 't5', 'claude', 'gemini', 'llama', 'mistral',
        'huggingface', 'pytorch', 'tensorflow', 'pinecone', 'qdrant',
        'langchain', 'llamaindex', 'mcp', 'openai', 'anthropic',
        'rlhf', 'dpo', 'lora', 'qlora', 'flash attention',
        'minhash', 'kv cache', 'vllm', 'opentelemetry',
    ]
    return any(name in text for name in indicators)


def has_quantitative(labels: list[str]) -> bool:
    """Detect numeric content (sizes, counts, percentages)."""
    text = ' '.join(labels)
    return bool(re.search(r'\b\d+[KMBkmb]\b|\b\d+%|\b\d+x\b', text)) or \
           bool(re.search(r'\b\d{2,}\b.*\b\d{2,}\b', text))


def classify(mmd_path: Path, caption: str) -> tuple[str, str]:
    mmd_text = mmd_path.read_text(encoding='utf-8', errors='replace')
    labels = extract_node_labels(mmd_text)

    # Generic-step-list test: most labels are generic short phrases
    generic_count = sum(
        1 for lab in labels
        if all(w.lower() in GENERIC_STEP_WORDS
               or len(w) < 4 for w in lab.split()[:3])
    )
    is_generic_majority = labels and generic_count / len(labels) > 0.5

    specific = has_specific_names(labels)
    quantitative = has_quantitative(labels)

    if is_generic_majority and not specific and not quantitative:
        return 'DROP', 'Generic step-words only; prose covers same content'
    if specific:
        return 'KEEP', 'Names specific tools/algorithms — useful reference'
    if quantitative:
        return 'CONVERT', 'Has numeric content — better as quantitative infographic'
    return 'REVIEW', 'Linear but no clear signal — manual inspection'


def main() -> int:
    with IN_CSV.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    triaged = []
    counts = {'DROP': 0, 'KEEP': 0, 'CONVERT': 0, 'REVIEW': 0}
    for r in rows:
        mmd = ROOT / r['mmd']
        if not mmd.exists():
            continue
        action, reason = classify(mmd, r.get('caption', ''))
        counts[action] = counts.get(action, 0) + 1
        triaged.append({
            'mmd': r['mmd'],
            'action': action,
            'reason': reason,
            'caption': r.get('caption', '')[:200],
            'nodes': r['node_count'],
            'edges': r['edge_count'],
        })

    # Sort by action group
    order = {'DROP': 0, 'CONVERT': 1, 'REVIEW': 2, 'KEEP': 3}
    triaged.sort(key=lambda x: (order.get(x['action'], 4), x['mmd']))

    with OUT_CSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(triaged[0].keys()) if triaged
                           else ['mmd', 'action', 'reason', 'caption', 'nodes', 'edges'])
        w.writeheader()
        w.writerows(triaged)

    # Also write a markdown summary
    with OUT_MD.open('w', encoding='utf-8') as f:
        f.write('# Linear-Diagram Triage Report\n\n')
        f.write(f'Total scanned: {len(rows)}\n\n')
        for action in ('DROP', 'CONVERT', 'REVIEW', 'KEEP'):
            n = counts.get(action, 0)
            f.write(f'## {action} ({n})\n\n')
            for t in triaged:
                if t['action'] != action:
                    continue
                f.write(f'### `{t["mmd"]}`\n')
                f.write(f'- **Reason**: {t["reason"]}\n')
                if t['caption']:
                    f.write(f'- **Caption**: {t["caption"][:160]}\n')
                f.write(f'- nodes={t["nodes"]}, edges={t["edges"]}\n\n')

    print(f'Triage summary:')
    for action, n in counts.items():
        print(f'  {action}: {n}')
    print(f'\nCSV: {OUT_CSV}\nMarkdown: {OUT_MD}')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
