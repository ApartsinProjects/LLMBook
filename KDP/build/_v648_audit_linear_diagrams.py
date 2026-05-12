"""v6.48: Audit Mermaid diagrams that are just 'linear sequences of steps'.

These tend to have low pedagogical value: they take prose like
'Step 1: do X. Step 2: do Y. Step 3: do Z.' and just draw it as
boxes with arrows. The reader gains nothing the prose didn't already say.

Detection criteria (any one is a flag):
  - The .mmd is a flowchart TB or LR
  - 80%+ of edges are A --> B (linear, not branching)
  - Less than 1 subgraph (no grouping/structure)
  - No diamond decision nodes
  - Mostly text-only nodes (no icons, no styling)
  - Node count between 3 and 12 (sweet spot for "linear step list")

Output: KDP/validation/linear_diagram_audit.csv with candidates ranked by
how-linear-they-are. Manual review then decides DROP vs CONVERT.
"""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'KDP' / 'validation' / 'linear_diagram_audit.csv'


def analyze_mmd(p: Path) -> dict:
    text = p.read_text(encoding='utf-8', errors='replace')
    # Parse direction
    direction_m = re.search(r'^\s*flowchart\s+(\w+)', text, re.MULTILINE)
    direction = direction_m.group(1) if direction_m else ''

    # Count edges: A --> B  or  A --- B  or  A -.-> B
    edges = re.findall(r'(\w+)\s*-+\.?-+>\s*(\w+)', text)
    edge_count = len(edges)

    # Count nodes (unique identifiers in edges + standalone declarations)
    nodes = set()
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)
    # Also count node-style lines: NodeId[Label] or NodeId(Label)
    for m in re.finditer(r'^\s*(\w+)\s*[\[\(\{]', text, re.MULTILINE):
        nodes.add(m.group(1))
    node_count = len(nodes)

    # Branching factor: how many nodes have multiple outgoing edges?
    out_counts = {}
    for a, b in edges:
        out_counts[a] = out_counts.get(a, 0) + 1
    branching = sum(1 for v in out_counts.values() if v >= 2)

    # Subgraphs (grouping)
    subgraph_count = len(re.findall(r'^\s*subgraph\s+', text, re.MULTILINE))

    # Decision diamonds (diamond shape: {Label})
    diamond_count = len(re.findall(r'\{[^}]+\}', text))

    # Styling: classDef or class XX yyy or style XX fill
    has_styling = bool(re.search(r'classDef|^\s*style\s+', text, re.MULTILINE))

    # Linearity score: high if most edges are sequential
    linearity = (edge_count - branching) / max(1, edge_count)

    return {
        'direction': direction,
        'edge_count': edge_count,
        'node_count': node_count,
        'branching_nodes': branching,
        'subgraph_count': subgraph_count,
        'diamond_count': diamond_count,
        'has_styling': has_styling,
        'linearity_score': round(linearity, 2),
    }


def is_linear_step_diagram(stats: dict) -> bool:
    return (
        3 <= stats['node_count'] <= 14
        and stats['subgraph_count'] == 0
        and stats['diamond_count'] == 0
        and stats['linearity_score'] >= 0.8
        and stats['edge_count'] >= 3
    )


def find_figure_caption(mmd_path: Path) -> str:
    """Find the figcaption in the corresponding HTML page."""
    img_name = mmd_path.with_suffix('.png').name
    parent = mmd_path.parent.parent  # module dir
    for html_path in parent.glob('*.html'):
        try:
            text = html_path.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if img_name in text:
            # Find caption right after the img
            m = re.search(
                rf'<img[^>]*src="[^"]*{re.escape(img_name)}"[^>]*/?>(.{{0,800}}?)<(?:/figure|/div)',
                text, re.DOTALL,
            )
            if m:
                cap_m = re.search(r'<(?:figcaption|div class="diagram-caption")[^>]*>(.+?)</(?:figcaption|div)>',
                                  m.group(1), re.DOTALL)
                if cap_m:
                    return re.sub(r'<[^>]+>', '', cap_m.group(1)).strip()[:200]
    return ''


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    candidates = []
    for mmd in sorted(ROOT.rglob('part-*/module-*/images/*.mmd')):
        stats = analyze_mmd(mmd)
        if is_linear_step_diagram(stats):
            cap = find_figure_caption(mmd)
            candidates.append({
                'mmd': str(mmd.relative_to(ROOT)).replace('\\', '/'),
                'caption': cap,
                **stats,
            })

    candidates.sort(key=lambda x: (-x['linearity_score'], x['node_count']))

    with OUT.open('w', encoding='utf-8', newline='') as f:
        if candidates:
            w = csv.DictWriter(f, fieldnames=list(candidates[0].keys()))
            w.writeheader()
            w.writerows(candidates)

    print(f'Total Mermaid diagrams scanned: '
          f'{len(list(ROOT.rglob("part-*/module-*/images/*.mmd")))}')
    print(f'Linear-step-list candidates:    {len(candidates)}')
    print(f'\nTop 20 candidates (most-linear first):')
    for c in candidates[:20]:
        print(f'  {c["mmd"]}')
        print(f'    nodes={c["node_count"]} edges={c["edge_count"]} '
              f'linearity={c["linearity_score"]} branching={c["branching_nodes"]}')
        if c['caption']:
            print(f'    caption: {c["caption"][:100]}')
    print(f'\nReport: {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
