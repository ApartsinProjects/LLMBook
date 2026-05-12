"""v6.50: Audit every Mermaid diagram on the 3 axes — TEXT-ONLY analysis.

Reads each .mmd source (cheap, no image load). For each:
  A. Didactic value: structural complexity (node count, edges, subgraphs,
     decision diamonds, named-entity density)
  B. Type fit: 'is Mermaid the right tool?' (CORRECT vs WRONG-should-be-X)
  C. Publishing quality: text-length-overflow risk, edge-bundle complexity

Output: KDP/validation/mermaid_diagram_audit.csv with per-diagram scoring.
"""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'KDP' / 'validation' / 'mermaid_diagram_audit.csv'

# Known framework / model / library names (signals Mermaid is right tool)
NAMED_ENTITIES = {
    'GPT', 'Claude', 'Gemini', 'Llama', 'Mistral', 'BERT', 'T5',
    'PyTorch', 'TensorFlow', 'HuggingFace', 'LangChain', 'LlamaIndex',
    'OpenAI', 'Anthropic', 'Google', 'NVIDIA',
    'vLLM', 'TGI', 'Triton', 'TensorRT', 'DeepSpeed', 'Megatron',
    'Pinecone', 'Weaviate', 'Qdrant', 'ChromaDB', 'pgvector', 'Milvus',
    'MLflow', 'Wandb', 'Comet',
    'FastAPI', 'Flask', 'Pydantic',
    'MCP', 'A2A', 'RAG', 'LoRA', 'QLoRA', 'RLHF', 'DPO', 'PPO', 'GRPO',
    'FlashAttention', 'KV', 'MinHash', 'HNSW', 'IVF', 'PQ',
    'OpenTelemetry', 'Langfuse', 'Helicone',
    'CUDA', 'GPU', 'CPU', 'TPU', 'NVMe',
    'BPE', 'WordPiece', 'SentencePiece',
}

# Words that suggest quantitative content (axis B: should be matplotlib)
QUANT_WORDS = {
    'tokens/s', 'tokens/sec', 'ms', 'GB', 'MB', 'TB', '%', 'FLOPs', 'FLOP',
    'latency', 'throughput', 'cost', 'price', 'tokens', 'ratio',
}

# Words that suggest metaphor/intuition (axis B: should be Gemini)
METAPHOR_WORDS = {
    'imagine', 'like a', 'analogy', 'metaphor', 'think of', 'kitchen',
    'restaurant', 'orchestra', 'musician', 'recipe', 'navigator',
}


def parse_mmd(text: str) -> dict:
    direction = re.search(r'^\s*flowchart\s+(\w+)', text, re.MULTILINE)
    direction = direction.group(1) if direction else 'TB'

    # Edges (linear arrow patterns)
    edges = re.findall(r'(\w+)\s*-+\.?-+>\s*(\w+)', text)
    edge_count = len(edges)

    # Nodes — unique IDs in edges + standalone declarations
    nodes = set()
    for a, b in edges:
        nodes.add(a); nodes.add(b)
    for m in re.finditer(r'^\s*(\w+)\s*[\[\(\{]', text, re.MULTILINE):
        nodes.add(m.group(1))
    node_count = len(nodes)

    # Out-degrees -> branching
    out = {}
    for a, b in edges:
        out[a] = out.get(a, 0) + 1
    branching = sum(1 for v in out.values() if v >= 2)
    max_outdeg = max(out.values()) if out else 0

    subgraphs = len(re.findall(r'^\s*subgraph\b', text, re.MULTILINE))
    diamonds = len(re.findall(r'\{[^}]+\}', text))
    rounded = len(re.findall(r'\([^)]+\)', text))
    classDefs = len(re.findall(r'^\s*classDef\s', text, re.MULTILINE))

    # Extract node labels (text between brackets/parens/braces)
    labels = []
    for m in re.finditer(r'[\[\(\{]"?([^"\]\)\}]{2,})"?[\]\)\}]', text):
        labels.append(m.group(1).strip())

    # Stats on labels
    total_label_chars = sum(len(L) for L in labels)
    long_labels = sum(1 for L in labels if len(L) > 50)
    named_entity_hits = 0
    quant_hits = 0
    metaphor_hits = 0
    label_text = ' '.join(labels)
    for ne in NAMED_ENTITIES:
        if re.search(rf'\b{re.escape(ne)}\b', label_text):
            named_entity_hits += 1
    for qw in QUANT_WORDS:
        if qw in label_text:
            quant_hits += 1
    for mw in METAPHOR_WORDS:
        if mw in label_text.lower():
            metaphor_hits += 1

    return {
        'direction': direction,
        'node_count': node_count,
        'edge_count': edge_count,
        'branching_nodes': branching,
        'max_outdegree': max_outdeg,
        'subgraphs': subgraphs,
        'diamonds': diamonds,
        'has_classDef': classDefs > 0,
        'label_chars_total': total_label_chars,
        'long_label_count': long_labels,
        'named_entity_hits': named_entity_hits,
        'quant_hits': quant_hits,
        'metaphor_hits': metaphor_hits,
    }


def score_axes(stats: dict) -> dict:
    """Apply the 3-axis rubric using the parsed stats."""

    # === Axis A: Didactic Value ===
    if stats['node_count'] < 3:
        a = 'LOW'
        a_reason = 'Trivial: < 3 nodes, nothing to map'
    elif (stats['node_count'] >= 5 and stats['branching_nodes'] >= 1 and
          stats['subgraphs'] >= 1):
        a = 'HIGH'
        a_reason = 'Structured: branching + grouping + multiple nodes'
    elif stats['named_entity_hits'] >= 3:
        a = 'HIGH'
        a_reason = (f'Names {stats["named_entity_hits"]} specific tools/models — '
                    'useful reference')
    elif (stats['node_count'] <= 8 and stats['branching_nodes'] == 0 and
          stats['subgraphs'] == 0 and stats['named_entity_hits'] == 0 and
          stats['quant_hits'] == 0):
        a = 'LOW'
        a_reason = ('Linear step-list with no named tools / no quantities — '
                    'prose redundancy')
    else:
        a = 'MEDIUM'
        a_reason = 'Adds structure but no exceptional teaching value'

    # === Axis B: Type Fit ===
    if stats['quant_hits'] >= 3 and stats['named_entity_hits'] < 2:
        b = 'WRONG-should-be-matplotlib'
        b_reason = (f'{stats["quant_hits"]} quantitative tokens (tokens/s, GB, %, '
                    'etc.) — better as matplotlib chart')
    elif stats['metaphor_hits'] >= 1:
        b = 'WRONG-should-be-Gemini'
        b_reason = 'Contains metaphor/analogy words — better as Gemini illustration'
    elif (stats['named_entity_hits'] >= 2 or stats['subgraphs'] >= 1 or
          stats['branching_nodes'] >= 1 or stats['diamonds'] >= 1):
        b = 'CORRECT'
        b_reason = 'Architecture / pipeline / decision content — Mermaid fits'
    elif stats['node_count'] <= 8 and stats['edge_count'] <= 8:
        b = 'CORRECT'
        b_reason = 'Small structural diagram — Mermaid is appropriate'
    else:
        b = 'CORRECT'
        b_reason = 'Default — structural diagram'

    # === Axis C: Publishing Quality ===
    quality_defects = []
    if stats['long_label_count'] >= 2:
        quality_defects.append(
            f'{stats["long_label_count"]} labels > 50 chars (likely wrap or clip)')
    if stats['node_count'] >= 18:
        quality_defects.append(
            f'{stats["node_count"]} nodes — likely cramped at print size')
    if stats['max_outdegree'] >= 5:
        quality_defects.append(
            f'one node has out-degree {stats["max_outdegree"]} — edge bundle')
    if stats['label_chars_total'] >= 800 and stats['node_count'] <= 10:
        quality_defects.append(
            f'{stats["label_chars_total"]} chars across only '
            f'{stats["node_count"]} nodes — node walls of text')

    if quality_defects:
        c = 'DEFECT'
        c_reason = '; '.join(quality_defects)
    else:
        c = 'OK'
        c_reason = 'Within typical dimensions; no obvious quality flags'

    # Recommended action
    if a == 'LOW':
        action = 'DROP'
    elif b.startswith('WRONG'):
        action = f'REWORK-AS-{"matplotlib" if "matplotlib" in b else "Gemini"}'
    elif c == 'DEFECT':
        action = 'FIX'
    else:
        action = 'KEEP'

    return {
        'A_value': a, 'A_reasoning': a_reason,
        'B_fit': b, 'B_reasoning': b_reason,
        'C_quality': c, 'C_reasoning': c_reason,
        'recommended_action': action,
    }


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for mmd in sorted(ROOT.glob('part-*/module-*/images/*.mmd')):
        try:
            text = mmd.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        stats = parse_mmd(text)
        scored = score_axes(stats)
        rows.append({
            'mmd': str(mmd.relative_to(ROOT)).replace('\\', '/'),
            **stats,
            **scored,
        })

    with OUT.open('w', encoding='utf-8', newline='') as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    print(f'Audited {len(rows)} Mermaid diagrams')
    # Summary
    from collections import Counter
    actions = Counter(r['recommended_action'] for r in rows)
    print('\nRecommended actions:')
    for a, n in actions.most_common():
        print(f'  {a}: {n}')
    a_dist = Counter(r['A_value'] for r in rows)
    print('\nDidactic-value distribution:')
    for a, n in a_dist.most_common():
        print(f'  {a}: {n}')
    b_dist = Counter(r['B_fit'] for r in rows)
    print('\nType-fit distribution:')
    for b, n in b_dist.most_common():
        print(f'  {b}: {n}')
    c_dist = Counter(r['C_quality'] for r in rows)
    print('\nQuality distribution:')
    for c, n in c_dist.most_common():
        print(f'  {c}: {n}')
    print(f'\nReport: {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
