#!/usr/bin/env python3
"""
Batch convert ALL remaining inline SVGs to Mermaid PNGs.
Reads SVG text content and captions, generates Mermaid diagrams, renders, and replaces.

Usage:
    C:/Python314/python scripts/mermaid/batch_convert_svgs.py
"""

import os
import re
import subprocess
import sys
import json
import html as html_module
from pathlib import Path
from typing import Optional, List, Dict
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "mermaid-config.json"
ARCHIVE_DIR = BASE_DIR / "_archive" / "replaced-svgs"

# Color palettes for diagram nodes
COLORS = {
    'blue':   {'fill': '#e3f2fd', 'stroke': '#1565c0'},
    'green':  {'fill': '#e8f5e9', 'stroke': '#2e7d32'},
    'purple': {'fill': '#f3e5f5', 'stroke': '#6a1b9a'},
    'orange': {'fill': '#fff3e0', 'stroke': '#e65100'},
    'red':    {'fill': '#fce4ec', 'stroke': '#c62828'},
    'teal':   {'fill': '#e0f2f1', 'stroke': '#00695c'},
    'amber':  {'fill': '#fff8e1', 'stroke': '#ff8f00'},
    'gray':   {'fill': '#f5f5f5', 'stroke': '#616161'},
}

COLOR_CYCLE = list(COLORS.keys())

def style_node(node_id: str, color_key: str) -> str:
    c = COLORS.get(color_key, COLORS['blue'])
    return f"    style {node_id} fill:{c['fill']},stroke:{c['stroke']},stroke-width:2px"


def render_mermaid(mmd_content: str, output_path: Path, width: int = 1200) -> Optional[Path]:
    """Write .mmd content to file and render to PNG via mmdc."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    mmd_path = output_path.with_suffix(".mmd")
    mmd_path.write_text(mmd_content, encoding="utf-8")

    cmd = [
        "mmdc", "-i", str(mmd_path), "-o", str(output_path),
        "-c", str(CONFIG_PATH), "-w", str(width),
        "-s", "3", "--backgroundColor", "white",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"  ERROR rendering {output_path.name}: {result.stderr[:200]}")
        return None
    return output_path


def extract_text_elements(svg_content: str) -> List[Dict]:
    """Extract individual text elements with position and formatting info."""
    elements = []
    for m in re.finditer(r'<text([^>]*)>(.*?)</text>', svg_content, re.DOTALL):
        attrs_str = m.group(1)
        text_content = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        text_content = html_module.unescape(text_content)
        if not text_content or len(text_content) < 2:
            continue

        # Parse attributes
        x = float(re.search(r'x="([^"]+)"', attrs_str).group(1)) if re.search(r'x="([^"]+)"', attrs_str) else 0
        y = float(re.search(r'y="([^"]+)"', attrs_str).group(1)) if re.search(r'y="([^"]+)"', attrs_str) else 0
        is_bold = 'font-weight' in attrs_str and ('700' in attrs_str or '600' in attrs_str or 'bold' in attrs_str)
        font_size = float(re.search(r'font-size="(\d+)"', attrs_str).group(1)) if re.search(r'font-size="(\d+)"', attrs_str) else 12

        elements.append({
            'text': text_content,
            'x': x, 'y': y,
            'bold': is_bold,
            'size': font_size,
        })
    return elements


def group_text_elements(elements: List[Dict], y_threshold: float = 25) -> List[Dict]:
    """Group text elements by spatial proximity into logical nodes."""
    if not elements:
        return []

    # Sort by y, then x
    elements.sort(key=lambda e: (e['y'], e['x']))

    groups = []
    current_group = [elements[0]]

    for elem in elements[1:]:
        last = current_group[-1]
        # Same spatial group if y-distance is small and x is similar
        if abs(elem['y'] - last['y']) < y_threshold and abs(elem['x'] - last['x']) < 200:
            current_group.append(elem)
        else:
            groups.append(current_group)
            current_group = [elem]
    groups.append(current_group)

    # Convert groups to labeled nodes
    nodes = []
    for group in groups:
        # Find the "title" (bold or largest text)
        bold_items = [e for e in group if e['bold'] or e['size'] > 12]
        detail_items = [e for e in group if not e['bold'] and e['size'] <= 12]

        title = ' '.join(e['text'] for e in bold_items) if bold_items else group[0]['text']
        detail = ' '.join(e['text'] for e in detail_items[:3])  # Max 3 detail lines

        # Clean up
        title = title.strip()[:80]
        detail = detail.strip()[:100]

        if title:
            nodes.append({
                'title': title,
                'detail': detail,
                'x': group[0]['x'],
                'y': group[0]['y'],
            })

    return nodes


def extract_svg_info(html_path: Path) -> List[Dict]:
    """Extract all SVGs from an HTML file with their captions and text content."""
    content = html_path.read_text(encoding="utf-8")
    svgs = list(re.finditer(r'<svg[^>]*>.*?</svg>', content, re.DOTALL))
    results = []
    for i, m in enumerate(svgs):
        after = content[m.end():m.end()+500]
        cap_m = re.search(r'<div class="diagram-caption"[^>]*>(.*?)</div>', after, re.DOTALL)
        caption = re.sub(r'<[^>]+>', '', cap_m.group(1)).strip() if cap_m else ''

        # Extract structured text elements from SVG
        text_elements = extract_text_elements(m.group())
        grouped_nodes = group_text_elements(text_elements)

        # Also get flat text for pattern detection
        svg_text = ' '.join(e['text'] for e in text_elements)

        # Get surrounding heading for context
        before = content[max(0, m.start()-2000):m.start()]
        heading_m = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', before, re.DOTALL)
        heading = re.sub(r'<[^>]+>', '', heading_m[-1]).strip() if heading_m else ''

        results.append({
            'index': i,
            'start': m.start(),
            'end': m.end(),
            'svg': m.group(),
            'caption': caption,
            'svg_text': svg_text[:500],
            'text_elements': text_elements,
            'grouped_nodes': grouped_nodes,
            'heading': heading,
        })
    return results


def slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')[:60]
    return text


def parse_svg_concepts(svg_text: str, caption: str) -> Dict:
    """Parse the SVG text content to extract key concepts, nodes, and relationships."""
    # Combine caption and svg text for analysis
    combined = f"{caption} {svg_text}"

    # Look for arrow-like flow patterns
    has_flow = any(x in combined for x in ['->', '→', 'pipeline', 'flow', 'chain', 'process', 'stage', 'step', 'phase'])
    has_comparison = any(x in combined for x in ['vs.', 'vs ', 'versus', 'compared', 'comparison', 'left', 'right', 'approach'])
    has_hierarchy = any(x in combined for x in ['layer', 'level', 'tier', 'stack', 'hierarchy', 'nested'])
    has_cycle = any(x in combined for x in ['loop', 'cycle', 'repeat', 'feedback', 'iterative'])
    has_decision = any(x in combined for x in ['decision', 'choose', 'if ', 'yes', 'no', 'does ', 'is '])
    has_grid = any(x in combined for x in ['matrix', 'grid', 'table', 'accuracy', '%'])
    has_chart = any(x in combined for x in ['axis', 'scale', 'log scale', 'performance'])

    return {
        'has_flow': has_flow,
        'has_comparison': has_comparison,
        'has_hierarchy': has_hierarchy,
        'has_cycle': has_cycle,
        'has_decision': has_decision,
        'has_grid': has_grid,
        'has_chart': has_chart,
    }


def generate_mermaid_from_svg(svg_info: Dict, file_stem: str) -> str:
    """Generate a Mermaid diagram definition based on SVG content analysis."""
    caption = svg_info['caption']
    svg_text = svg_info['svg_text']
    grouped_nodes = svg_info.get('grouped_nodes', [])
    concepts = parse_svg_concepts(svg_text, caption)

    # Use grouped nodes from spatial analysis if available
    if grouped_nodes and len(grouped_nodes) >= 2:
        return generate_from_grouped_nodes(grouped_nodes, caption, concepts)

    # Fallback: try text splitting
    text_parts = [t.strip() for t in re.split(r'\s{2,}', svg_text) if t.strip() and len(t.strip()) > 1]

    if concepts['has_decision']:
        return generate_decision_diagram(svg_text, caption, text_parts)
    elif concepts['has_comparison']:
        return generate_comparison_diagram(svg_text, caption, text_parts)
    elif concepts['has_cycle']:
        return generate_cycle_diagram(svg_text, caption, text_parts)
    elif concepts['has_hierarchy']:
        return generate_hierarchy_diagram(svg_text, caption, text_parts)
    elif concepts['has_flow']:
        return generate_flow_diagram(svg_text, caption, text_parts)
    else:
        # Final fallback: use caption as a multi-node diagram
        return generate_from_caption(caption)


def generate_from_grouped_nodes(grouped_nodes: List[Dict], caption: str, concepts: Dict) -> str:
    """Generate Mermaid from spatially-grouped SVG text nodes."""
    # Deduplicate and filter meaningful nodes
    seen = set()
    nodes = []
    for n in grouped_nodes:
        title = n['title'].strip()
        if not title or len(title) < 2:
            continue
        key = title.lower()[:40]
        if key in seen:
            continue
        seen.add(key)
        nodes.append(n)

    if len(nodes) < 2:
        return generate_from_caption(caption)

    # Limit to max 12 nodes for readability
    nodes = nodes[:12]

    # Determine layout based on x/y distribution
    x_range = max(n['x'] for n in nodes) - min(n['x'] for n in nodes)
    y_range = max(n['y'] for n in nodes) - min(n['y'] for n in nodes)
    horizontal = x_range > y_range * 1.5

    # Check if nodes form clear groups (similar x values = columns)
    if concepts.get('has_comparison') or concepts.get('has_hierarchy'):
        direction = "TB"
    elif horizontal:
        direction = "LR"
    else:
        direction = "TB"

    lines = [f"flowchart {direction}"]
    node_ids = []

    for i, n in enumerate(nodes):
        nid = f"N{i}"
        node_ids.append(nid)
        title = sanitize_label(n['title'])
        detail = sanitize_label(n['detail']) if n.get('detail') else ''
        if detail and detail != title:
            lines.append(f'    {nid}["<b>{title}</b><br/><i>{detail}</i>"]')
        else:
            lines.append(f'    {nid}["{title}"]')

    # Connect nodes based on layout
    if concepts.get('has_cycle'):
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")
        if len(node_ids) > 2:
            lines.append(f"    {node_ids[-1]} -.->|repeat| {node_ids[0]}")
    elif concepts.get('has_comparison'):
        # Side by side, no arrows
        pass
    elif concepts.get('has_decision'):
        if len(node_ids) >= 3:
            lines.append(f'    {node_ids[0]} -->|"Yes"| {node_ids[1]}')
            lines.append(f'    {node_ids[0]} -->|"No"| {node_ids[2]}')
            for i in range(3, len(node_ids)):
                lines.append(f"    {node_ids[(i-1)//2]} --> {node_ids[i]}")
        else:
            for i in range(len(node_ids) - 1):
                lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")
    else:
        # Default: sequential flow
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")

    # Style nodes
    for i, nid in enumerate(node_ids):
        color = COLOR_CYCLE[i % len(COLOR_CYCLE)]
        lines.append(style_node(nid, color))

    return "\n".join(lines)


def generate_from_caption(caption: str) -> str:
    """Generate a Mermaid diagram from just the caption, splitting into key phrases."""
    if not caption:
        return 'flowchart LR\n    A["Diagram"]\n    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px'

    # Try to extract key concepts from caption
    # Remove figure number
    clean = re.sub(r'^Figure \d+\.\d+\.\d+:?\s*', '', caption)

    # Split on common delimiters
    parts = re.split(r'[;.]', clean)
    parts = [p.strip() for p in parts if p.strip() and len(p.strip()) > 5]

    if len(parts) < 2:
        # Try splitting on commas
        parts = re.split(r',\s+', clean)
        parts = [p.strip() for p in parts if p.strip() and len(p.strip()) > 5]

    if len(parts) < 2:
        # Use the whole caption as a single node with a note
        return f"""flowchart TB
    MAIN["{sanitize_label(clean[:80])}"]
    style MAIN fill:#e3f2fd,stroke:#1565c0,stroke-width:2px"""

    # Create nodes from parts (max 6)
    parts = parts[:6]
    lines = ["flowchart TB"]
    node_ids = []
    for i, p in enumerate(parts):
        nid = f"P{i}"
        node_ids.append(nid)
        lines.append(f'    {nid}["{sanitize_label(p[:80])}"]')

    for i in range(len(node_ids) - 1):
        lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")

    for i, nid in enumerate(node_ids):
        color = COLOR_CYCLE[i % len(COLOR_CYCLE)]
        lines.append(style_node(nid, color))

    return "\n".join(lines)


def sanitize_label(text: str) -> str:
    """Clean text for use in Mermaid labels."""
    text = text.replace('"', "'")
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 80:
        text = text[:77] + "..."
    return text


def extract_key_concepts(text_parts: List[str], max_nodes: int = 8) -> List[Dict]:
    """Extract key concepts from text parts to create diagram nodes."""
    concepts = []
    seen = set()
    for part in text_parts:
        part = part.strip()
        if len(part) < 3 or len(part) > 150:
            continue
        # Skip pure numbers, arrows, symbols
        if re.match(r'^[\d\s\.\,\-\+\=\>\<\&\;]+$', part):
            continue
        # Use as a concept if not too similar to existing
        key = part.lower()[:30]
        if key not in seen:
            seen.add(key)
            concepts.append({'label': sanitize_label(part), 'raw': part})
            if len(concepts) >= max_nodes:
                break
    return concepts


def generate_flow_diagram(svg_text: str, caption: str, text_parts: List[str]) -> str:
    """Generate a flowchart LR diagram."""
    concepts = extract_key_concepts(text_parts, max_nodes=8)
    if len(concepts) < 2:
        # Fallback: just use caption
        return f"""flowchart LR
    A["<b>{sanitize_label(caption[:80])}</b>"]
    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px"""

    lines = ["flowchart LR"]
    node_ids = []
    for i, c in enumerate(concepts):
        nid = f"N{i}"
        node_ids.append(nid)
        lines.append(f'    {nid}["{c["label"]}"]')

    # Connect sequentially
    for i in range(len(node_ids) - 1):
        lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")

    # Add styles
    for i, nid in enumerate(node_ids):
        color = COLOR_CYCLE[i % len(COLOR_CYCLE)]
        lines.append(style_node(nid, color))

    return "\n".join(lines)


def generate_comparison_diagram(svg_text: str, caption: str, text_parts: List[str]) -> str:
    """Generate a comparison (side-by-side subgraph) diagram."""
    concepts = extract_key_concepts(text_parts, max_nodes=10)

    # Try to split concepts into two groups
    mid = len(concepts) // 2
    if mid < 1:
        return generate_flow_diagram(svg_text, caption, text_parts)

    group_a = concepts[:mid]
    group_b = concepts[mid:]

    lines = ["flowchart TB"]
    lines.append(f'    subgraph A["{group_a[0]["label"]}"]')
    lines.append("        direction TB")
    for i, c in enumerate(group_a[1:]):
        lines.append(f'        A{i}["{c["label"]}"]')
    lines.append("    end")

    lines.append(f'    subgraph B["{group_b[0]["label"]}"]')
    lines.append("        direction TB")
    for i, c in enumerate(group_b[1:]):
        lines.append(f'        B{i}["{c["label"]}"]')
    lines.append("    end")

    lines.append("    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px")
    lines.append("    style B fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px")

    return "\n".join(lines)


def generate_hierarchy_diagram(svg_text: str, caption: str, text_parts: List[str]) -> str:
    """Generate a hierarchy/stack diagram."""
    concepts = extract_key_concepts(text_parts, max_nodes=8)
    if len(concepts) < 2:
        return generate_flow_diagram(svg_text, caption, text_parts)

    lines = ["flowchart TB"]
    node_ids = []
    for i, c in enumerate(concepts):
        nid = f"L{i}"
        node_ids.append(nid)
        lines.append(f'    {nid}["{c["label"]}"]')

    for i in range(len(node_ids) - 1):
        lines.append(f"    {node_ids[i]} --- {node_ids[i+1]}")

    for i, nid in enumerate(node_ids):
        color = COLOR_CYCLE[i % len(COLOR_CYCLE)]
        lines.append(style_node(nid, color))

    return "\n".join(lines)


def generate_cycle_diagram(svg_text: str, caption: str, text_parts: List[str]) -> str:
    """Generate a cycle/loop diagram."""
    concepts = extract_key_concepts(text_parts, max_nodes=6)
    if len(concepts) < 2:
        return generate_flow_diagram(svg_text, caption, text_parts)

    lines = ["flowchart LR"]
    node_ids = []
    for i, c in enumerate(concepts):
        nid = f"C{i}"
        node_ids.append(nid)
        lines.append(f'    {nid}["{c["label"]}"]')

    for i in range(len(node_ids) - 1):
        lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")

    # Close the loop
    if len(node_ids) > 2:
        lines.append(f"    {node_ids[-1]} -.->|repeat| {node_ids[0]}")

    for i, nid in enumerate(node_ids):
        color = COLOR_CYCLE[i % len(COLOR_CYCLE)]
        lines.append(style_node(nid, color))

    return "\n".join(lines)


def generate_decision_diagram(svg_text: str, caption: str, text_parts: List[str]) -> str:
    """Generate a decision tree diagram."""
    concepts = extract_key_concepts(text_parts, max_nodes=8)
    if len(concepts) < 2:
        return generate_flow_diagram(svg_text, caption, text_parts)

    lines = ["flowchart TD"]
    node_ids = []
    for i, c in enumerate(concepts):
        nid = f"D{i}"
        node_ids.append(nid)
        if i == 0:
            lines.append(f'    {nid}{{{{"<b>{c["label"]}</b>"}}}}')
        else:
            lines.append(f'    {nid}["{c["label"]}"]')

    # Create a tree-like structure
    if len(node_ids) >= 3:
        lines.append(f'    {node_ids[0]} -->|"Yes"| {node_ids[1]}')
        lines.append(f'    {node_ids[0]} -->|"No"| {node_ids[2]}')
        for i in range(3, len(node_ids)):
            parent = node_ids[i // 2]
            lines.append(f"    {parent} --> {node_ids[i]}")
    else:
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")

    for i, nid in enumerate(node_ids):
        color = COLOR_CYCLE[i % len(COLOR_CYCLE)]
        lines.append(style_node(nid, color))

    return "\n".join(lines)


def generate_chart_placeholder(svg_text: str, caption: str, text_parts: List[str]) -> str:
    """Generate a placeholder for chart-type diagrams."""
    # For charts with axes, create a simple representation
    concepts = extract_key_concepts(text_parts, max_nodes=6)
    return generate_flow_diagram(svg_text, caption, text_parts)


# ============================================================================
# MANUALLY CURATED DIAGRAMS (for complex/important diagrams)
# ============================================================================

CURATED_DIAGRAMS = {}

def load_curated():
    """Load manually curated Mermaid definitions for important diagrams."""
    global CURATED_DIAGRAMS

    # key = "filepath|svg_index"

    # --- Appendices (existing from generate_mermaid_diagrams.py) ---
    CURATED_DIAGRAMS["appendices/appendix-l-langchain/section-l.1.html|0"] = """flowchart LR
    A["<b>PromptTemplate</b><br/><i>fills variables</i>"]
    B["<b>ChatModel</b><br/><i>generates response</i>"]
    C["<b>OutputParser</b><br/><i>extracts content</i>"]
    D["<b>Result</b><br/><i>clean string</i>"]
    A -->|"pipe"| B -->|"pipe"| C -->|"pipe"| D
    style A fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style B fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style C fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style D fill:#e3f2fd,stroke:#1565c0,stroke-width:2px"""

    CURATED_DIAGRAMS["appendices/appendix-l-langchain/section-l.2.html|0"] = """flowchart LR
    UI["<b>User Input</b>"]
    RWM["<b>RunnableWith<br/>MessageHistory</b>"]
    HS["<b>History Store</b><br/><i>get_session_history</i>"]
    CH["<b>LCEL Chain</b>"]
    RS["<b>Response</b>"]
    UI --> RWM
    HS -.->|"load history"| RWM
    RWM --> CH --> RS
    CH -.->|"save exchange"| HS
    style UI fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style RWM fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style HS fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style CH fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style RS fill:#e3f2fd,stroke:#1565c0,stroke-width:2px"""

    CURATED_DIAGRAMS["appendices/appendix-l-langchain/section-l.3.html|0"] = """flowchart LR
    DOC["<b>Document Text</b>"]
    C1["<b>Chunk 1</b>"]
    C2["<b>Chunk 2</b>"]
    C3["<b>Chunk 3</b>"]
    C4["<b>Chunk 4</b>"]
    DOC --> C1
    DOC --> C2
    DOC --> C3
    DOC --> C4
    C1 ---|"overlap"| C2
    C2 ---|"overlap"| C3
    C3 ---|"overlap"| C4
    style DOC fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style C1 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style C2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style C3 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style C4 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["appendices/appendix-l-langchain/section-l.5.html|0"] = """flowchart LR
    UI["<b>User Input</b>"]
    LLM["<b>LLM</b><br/><i>decides action</i>"]
    TOOL["<b>Tool</b><br/><i>execute</i>"]
    FA["<b>Final Answer</b>"]
    UI --> LLM
    LLM -->|"tool call"| TOOL
    TOOL -.->|"observation"| LLM
    LLM -->|"done"| FA
    style UI fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style LLM fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style TOOL fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style FA fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    CURATED_DIAGRAMS["appendices/appendix-o-llamaindex/section-o.1.html|0"] = """flowchart LR
    DS["<b>Data Sources</b><br/><i>files, APIs, DBs</i>"]
    CN["<b>Connectors</b><br/><i>Readers / Loaders</i>"]
    DC["<b>Documents</b><br/><i>+ Transformations</i>"]
    TN["<b>TextNodes</b><br/><i>in an Index</i>"]
    DS --> CN --> DC --> TN
    style DS fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style CN fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style DC fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style TN fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    CURATED_DIAGRAMS["appendices/appendix-o-llamaindex/section-o.2.html|0"] = """flowchart TB
    subgraph VS["VectorStoreIndex"]
        V1["Embedding similarity"]
        V2["Top-k retrieval"]
    end
    subgraph SI["SummaryIndex"]
        S1["Sequential scan"]
        S2["All nodes visited"]
    end
    subgraph TI["TreeIndex"]
        T1["Hierarchical summaries"]
        T2["Top-down traversal"]
    end
    subgraph KI["KeywordTableIndex"]
        K1["Keyword extraction"]
        K2["Exact term match"]
    end
    style VS fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style SI fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style TI fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style KI fill:#fff3e0,stroke:#e65100,stroke-width:2px"""

    # --- Section 0.1: Gradient descent and bias-variance ---
    CURATED_DIAGRAMS["part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html|0"] = """flowchart LR
    START["<b>Start</b><br/><i>high loss</i>"]
    STEP1["Step 1<br/><i>follow gradient</i>"]
    STEP2["Step 2"]
    LOCAL["<b>Local Min</b>"]
    GLOBAL["<b>Global Min</b><br/><i>target</i>"]
    NOTE["Step size = learning rate x gradient<br/>Too big: overshoot<br/>Too small: slow"]
    START --> STEP1 --> STEP2 --> LOCAL
    STEP2 -.->|"escape"| GLOBAL
    START --> NOTE
    style START fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style LOCAL fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style GLOBAL fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style NOTE fill:#f5f5f5,stroke:#616161,stroke-width:1px"""

    CURATED_DIAGRAMS["part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html|1"] = """flowchart LR
    subgraph TRADEOFF["Bias-Variance Tradeoff"]
        direction TB
        UND["<b>Underfitting</b><br/>High bias"]
        OPT["<b>Optimal</b><br/>Min total error"]
        OVR["<b>Overfitting</b><br/>High variance"]
    end
    UND -->|"increase complexity"| OPT -->|"increase complexity"| OVR
    style UND fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style OPT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style OVR fill:#fce4ec,stroke:#c62828,stroke-width:2px"""

    # --- Section 0.4: RLHF mapping ---
    CURATED_DIAGRAMS["part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html|0"] = """flowchart LR
    PROMPT["<b>User Prompt</b><br/><i>Initial State</i>"]
    LLM["<b>LLM (Policy)</b><br/><i>Generates tokens</i>"]
    RESP["<b>Complete Response</b><br/><i>Sequence of actions</i>"]
    RM["<b>Reward Model</b><br/><i>Scores response</i>"]
    PPO["<b>PPO Optimizer</b><br/><i>Clipped policy update</i>"]
    PROMPT --> LLM --> RESP --> RM -->|"reward signal"| PPO -.->|"update policy"| LLM
    style PROMPT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style LLM fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style RESP fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style RM fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style PPO fill:#fce4ec,stroke:#c62828,stroke-width:2px"""

    # --- Section 3.1: LSTM cell ---
    CURATED_DIAGRAMS["part-1-foundations/module-03-sequence-models-attention/section-3.1.html|0"] = """flowchart LR
    subgraph LSTM["LSTM Cell"]
        direction TB
        FG["<b>Forget Gate</b><br/><i>sigma: what to erase</i>"]
        IG["<b>Input Gate</b><br/><i>sigma: what to write</i>"]
        CAND["<b>Candidate</b><br/><i>tanh: new info</i>"]
        OG["<b>Output Gate</b><br/><i>sigma: what to output</i>"]
        CS["<b>Cell State</b><br/><i>memory highway</i>"]
    end
    CT["c(t-1)"] --> FG
    FG -->|"erase"| CS
    IG --> CS
    CAND --> CS
    CS -->|"filtered by"| OG
    OG --> HT["h(t)"]
    NOTE["Cell state acts as memory highway<br/>with only additive interactions<br/>solving the vanishing gradient"]
    LSTM --> NOTE
    style FG fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style IG fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style CAND fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style OG fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style CS fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    # Section 6.3: emergent abilities + MoE
    CURATED_DIAGRAMS["part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html|0"] = """flowchart LR
    subgraph EM["Exact Match (looks emergent)"]
        direction TB
        E1["Small model: 0%"]
        E2["Medium model: 0%"]
        E3["Large model: 95%!"]
    end
    subgraph LL["Log-Likelihood (smooth)"]
        direction TB
        L1["Small model: low"]
        L2["Medium model: medium"]
        L3["Large model: high"]
    end
    NOTE["Same capability appears emergent<br/>or smooth depending on metric"]
    EM --> NOTE
    LL --> NOTE
    style EM fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style LL fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style NOTE fill:#f5f5f5,stroke:#616161,stroke-width:1px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html|1"] = """flowchart TB
    TOKEN["<b>Token hidden state x</b>"]
    ROUTER["<b>Router</b><br/><i>gating network</i>"]
    subgraph EXPERTS["6 Experts (top-2 active)"]
        direction LR
        E1["<b>Expert 1</b><br/>w=0.62 ✓"]
        E2["<b>Expert 2</b><br/>w=0.38 ✓"]
        E3["Expert 3<br/>skipped"]
        E4["Expert 4<br/>skipped"]
    end
    SUM["<b>Weighted Sum</b><br/>0.62*E1 + 0.38*E2"]
    TOKEN --> ROUTER --> EXPERTS
    E1 --> SUM
    E2 --> SUM
    style TOKEN fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style ROUTER fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style E1 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style E2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style E3 fill:#f5f5f5,stroke:#616161,stroke-width:1px
    style E4 fill:#f5f5f5,stroke:#616161,stroke-width:1px
    style SUM fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    # Section 6.5: grokking
    CURATED_DIAGRAMS["part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html|0"] = """flowchart LR
    subgraph GROK["Grokking"]
        direction LR
        MEM["<b>Memorized</b><br/>Train: 100%<br/>Val: low"]
        PLAT["<b>Long Plateau</b><br/>Train: 100%<br/>Val: still low"]
        GEN["<b>Generalized!</b><br/>Train: 100%<br/>Val: 100%"]
    end
    MEM -->|"many more steps"| PLAT -->|"sudden jump"| GEN
    style MEM fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style PLAT fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style GEN fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    # Section 6.8: production training arch
    CURATED_DIAGRAMS["part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html|0"] = """flowchart TB
    subgraph DP["Data Pipeline"]
        DP1["Object Storage"] --> DP2["Mosaic Streaming"] --> DP3["Data Mixing"]
    end
    subgraph TF["Training Framework"]
        TF1["Megatron-Core"] --> TF2["TP + PP + DP + CP"] --> TF3["FlashAttention + FP8"]
    end
    subgraph FT["Fault Tolerance"]
        FT1["TorchElastic"] --> FT2["Health Monitor"] --> FT3["Auto-Recovery"]
    end
    subgraph CK["Checkpointing"]
        CK1["PyTorch DCP"] --> CK2["Async Staging"] --> CK3["Reshardable"]
    end
    DP --> TF --> FT --> CK
    style DP fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style TF fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style FT fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style CK fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    # Section 7.1: reasoning token flow + multimodal
    CURATED_DIAGRAMS["part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html|0"] = """flowchart LR
    P["<b>Prompt</b><br/><i>user input</i>"]
    TH["<b>Thinking Tokens</b><br/><i>5,000+ internal</i>"]
    AN["<b>Answer Tokens</b><br/><i>visible to user</i>"]
    API["<b>API Response</b>"]
    VIS["Hidden: o-series (billed)<br/>Visible: DeepSeek R1"]
    P --> TH --> AN --> API
    TH -.-> VIS
    style P fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style TH fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style AN fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style API fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html|1"] = """flowchart LR
    subgraph BOLT["Bolt-On Multimodal"]
        direction TB
        VE["Vision Encoder (ViT)"]
        LA["Linear Adapter"]
        LLM1["LLM Backbone"]
        VE --> LA --> LLM1
    end
    subgraph NATIVE["Native Multimodal"]
        direction TB
        IMG["Image patches"]
        TXT["Text tokens"]
        LLM2["Unified model<br/>interleaved tokens"]
        IMG --> LLM2
        TXT --> LLM2
    end
    style BOLT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style NATIVE fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    # Section 7.3: ORM vs PRM + MCTS
    CURATED_DIAGRAMS["part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html|0"] = """flowchart TB
    subgraph ORM["Outcome Reward Model"]
        direction TB
        O1["Step 1 ✓"] --> O2["Step 2 ✓"] --> O3["Step 3 ✗"]
        O4["Final: Wrong ✗<br/>Score: 0.0 (no step signal)"]
    end
    subgraph PRM["Process Reward Model"]
        direction TB
        P1["Step 1 ✓ (0.95)"] --> P2["Step 2 ✓ (0.88)"] --> P3["Step 3 ✗ (0.12)"]
        P4["Error caught at Step 3!<br/>Can backtrack here"]
    end
    O3 --> O4
    P3 --> P4
    style ORM fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style PRM fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html|1"] = """flowchart TB
    PROB["<b>Problem</b>"]
    S1A["Step 1a<br/>12/15"]
    S1B["Step 1b<br/>5/10"]
    S1C["Step 1c<br/>1/8"]
    S2A["Step 2a<br/>8/9"]
    ANS["<b>Answer ✓</b>"]
    PROB --> S1A --> S2A --> ANS
    PROB --> S1B
    PROB --> S1C
    NOTE["MCTS: Select, Expand,<br/>Simulate, Backpropagate"]
    PROB --> NOTE
    style S1A fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style S1B fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style S1C fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style ANS fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    # Section 7.4: multilingual
    CURATED_DIAGRAMS["part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html|0"] = """flowchart TB
    subgraph INPUT["Input Layer"]
        EN["English: The cat sleeps"]
        FR["French: Le chat dort"]
        JA["Japanese"]
        AR["Arabic"]
    end
    SHARED["<b>Shared Representation Space</b><br/><i>Knowledge transfers across languages</i>"]
    INPUT --> SHARED
    style INPUT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style SHARED fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html|1"] = """flowchart LR
    subgraph HIGH["High-resource"]
        EN["EN 88%"]
        DE["DE 85%"]
        ZH["ZH 84%"]
    end
    subgraph MED["Medium-resource"]
        AR["AR 70%"]
        HI["HI 65%"]
        SW["SW 60%"]
    end
    subgraph LOW["Low-resource"]
        YO["YO 43%"]
        QU["QU 34%"]
    end
    NOTE["Low-resource languages trail<br/>English by 40+ points"]
    LOW --> NOTE
    style HIGH fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style MED fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style LOW fill:#fce4ec,stroke:#c62828,stroke-width:2px"""

    # Section 8.x: Reasoning
    CURATED_DIAGRAMS["part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html|0"] = """flowchart LR
    subgraph STRATEGIES["Scaling Strategies"]
        TRAIN["<b>Train-time</b><br/>bigger model, single pass"]
        TEST["<b>Test-time</b><br/>same model, more thinking"]
        BOTH["<b>Combined</b><br/>larger model + thinking"]
    end
    NOTE["On hard reasoning tasks,<br/>test-time scaling achieves<br/>higher accuracy per FLOP"]
    STRATEGIES --> NOTE
    style TRAIN fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style TEST fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style BOTH fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html|1"] = """flowchart TB
    subgraph ARCH["Four Reasoning Architectures"]
        direction TB
        COT["<b>1. Extended CoT</b><br/>Visible reasoning trace<br/>No arch change"]
        HIDDEN["<b>2. Hidden Thinking</b><br/>Internal tokens (o-series)<br/>Billed but not shown"]
        VERIFY["<b>3. Verifier-Guided</b><br/>ORM/PRM scoring<br/>Best-of-N selection"]
        SEARCH["<b>4. Tree Search</b><br/>MCTS over reasoning<br/>Branch and backtrack"]
    end
    style COT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style HIDDEN fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style VERIFY fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style SEARCH fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html|0"] = """flowchart TB
    subgraph OAI["OpenAI o-Series"]
        O1["Hidden Chain-of-Thought"]
        O2["reasoning_summary (optional)"]
        O3["reasoning_effort: low/med/high"]
    end
    subgraph DS["DeepSeek R1 / QwQ"]
        D1["Visible Chain-of-Thought"]
        D2["Full reasoning in output"]
    end
    subgraph GEM["Gemini 2.5"]
        G1["Thinking tokens exposed"]
        G2["Via thinking_budget param"]
    end
    style OAI fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style DS fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style GEM fill:#fff3e0,stroke:#e65100,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.4.html|0"] = """flowchart TD
    Q1{"Does the task require<br/>multi-step logic?"}
    NO1["Use standard model<br/>Retrieval, summarization, chat"]
    Q2{"Is the answer<br/>verifiable?"}
    Q3{"Is latency<br/>acceptable?"}
    MAYBE["Consider reasoning model<br/>May help, test empirically"]
    YES3["Use reasoning model"]
    NO3["Use standard model<br/>+ better prompting"]
    Q1 -->|"No"| NO1
    Q1 -->|"Yes"| Q2
    Q2 -->|"No"| MAYBE
    Q2 -->|"Yes"| Q3
    Q3 -->|"Yes"| YES3
    Q3 -->|"No"| NO3
    style Q1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Q2 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Q3 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style YES3 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style NO1 fill:#f5f5f5,stroke:#616161,stroke-width:1px
    style NO3 fill:#f5f5f5,stroke:#616161,stroke-width:1px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html|0"] = """flowchart LR
    subgraph EASY["Easy Tasks"]
        E1["Bigger model optimal"]
        E2["70B, 1 sample"]
    end
    subgraph HARD["Hard Tasks"]
        H1["Test-time scaling optimal"]
        H2["7B, 64 samples + PRM"]
    end
    NOTE["Compute-optimal frontier:<br/>allocate budget based on<br/>task difficulty"]
    EASY --> NOTE
    HARD --> NOTE
    style EASY fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style HARD fill:#fce4ec,stroke:#c62828,stroke-width:2px"""

    # Section 9.x: Inference optimization
    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.1.html|0"] = """flowchart TB
    subgraph QUANT["Quantization Granularity"]
        direction TB
        PT["<b>Per-Tensor</b><br/>1 scale for entire matrix"]
        PC["<b>Per-Channel</b><br/>1 scale per row"]
        PG["<b>Per-Group (g=128)</b><br/>1 scale + 1 zero per 128 values<br/><i>Best accuracy for 4-bit</i>"]
    end
    PT --- PC --- PG
    style PT fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style PC fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style PG fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.1.html|1"] = """flowchart LR
    subgraph GPTQ["GPTQ"]
        direction TB
        G1["Column-by-column"]
        G2["Uses Hessian H = X^TX"]
        G3["Needs 128 calibration samples"]
        G4["Best perplexity at 4-bit"]
    end
    subgraph AWQ["AWQ"]
        direction TB
        A1["Channel-wise scaling"]
        A2["Protects salient channels"]
        A3["Fast, no retraining"]
        A4["Best speed/quality tradeoff"]
    end
    style GPTQ fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style AWQ fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.2.html|0"] = """flowchart LR
    subgraph LOGICAL["Logical View"]
        direction TB
        SA["Seq A (45 tokens): blk0, blk1, blk2"]
        SB["Seq B (28 tokens): blk0, blk1"]
        SC["Seq C (shared prefix): shared!, own"]
    end
    BT["Block Table"]
    subgraph PHYS["Physical GPU Memory"]
        direction LR
        P0["P0"] --- P1["P1"] --- P2["P2"] --- P3["P3"] --- P4["P4"]
    end
    LOGICAL --> BT --> PHYS
    NOTE["Non-contiguous blocks<br/>eliminate fragmentation"]
    PHYS --> NOTE
    style LOGICAL fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style PHYS fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.2.html|1"] = """flowchart LR
    subgraph MHA["MHA (Multi-Head)"]
        direction TB
        M1["32 Q heads"]
        M2["32 K heads, 32 V heads"]
        M3["KV Cache: 32 x d_head/layer"]
    end
    subgraph MQA["MQA (Multi-Query)"]
        direction TB
        Q1["32 Q heads"]
        Q2["1 shared K, 1 shared V"]
        Q3["KV Cache: 1 x d_head/layer"]
    end
    subgraph GQA["GQA (Grouped-Query)"]
        direction TB
        G1["32 Q heads"]
        G2["8 K groups, 8 V groups"]
        G3["KV Cache: 8 x d_head/layer"]
    end
    style MHA fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style MQA fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style GQA fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.2.html|2"] = """flowchart TB
    ROOT["<b>Root (empty)</b>"]
    SYS["<b>System Prompt KV</b><br/>(2,000 tokens)<br/><i>SHARED across all requests</i>"]
    UA["User A tokens"]
    UB["User B tokens"]
    UC["User C tokens"]
    ROOT --> SYS
    SYS --> UA
    SYS --> UB
    SYS --> UC
    style ROOT fill:#f5f5f5,stroke:#616161,stroke-width:1px
    style SYS fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style UA fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style UB fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style UC fill:#e3f2fd,stroke:#1565c0,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.2.html|3"] = """flowchart LR
    subgraph STATIC["Static Batching"]
        direction TB
        ST1["A B C D"]
        ST2["idle (wasted) while short<br/>sequences wait for long ones"]
    end
    subgraph CONT["Continuous Batching"]
        direction TB
        CT1["A B C D"]
        CT2["Completed slots immediately<br/>filled by new requests E, F, G"]
    end
    style STATIC fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style CONT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.3.html|0"] = """flowchart LR
    DRAFT["<b>Step 1: Draft</b><br/>(fast model)<br/>sat, on, the, mat"]
    VERIFY["<b>Step 2: Verify</b><br/>(target model, 1 pass)<br/>sat ✓, on ✓, the ✓, mat ✗"]
    RESAMPLE["<b>Step 3: Resample</b><br/>from target at rejected pos"]
    DRAFT --> VERIFY --> RESAMPLE -.->|"repeat"| DRAFT
    style DRAFT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style VERIFY fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style RESAMPLE fill:#fff3e0,stroke:#e65100,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.3.html|1"] = """flowchart TB
    CTX["<b>Context: the</b>"]
    subgraph TREE["Tree-Structured Verification"]
        A["a"] --- B["his"]
        C["cat"] --- D["dog"]
        E["small"] --- F["old"]
        G["sat"]
    end
    BEST["Best path: the -> cat -> sat<br/>(3 tokens in 1 forward pass)"]
    CTX --> TREE --> BEST
    style CTX fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style BEST fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.4.html|0"] = """flowchart TB
    HTTP["<b>HTTP Clients</b><br/>OpenAI-compatible API"]
    API["<b>API Server</b><br/>FastAPI/gRPC, streaming"]
    SCHED["<b>Request Scheduler</b><br/>continuous batching, priority"]
    KV["<b>KV Cache Manager</b><br/>PagedAttention"]
    EXEC["<b>Model Executor</b><br/>tensor parallel, pipeline"]
    GPU["<b>GPU Hardware</b>"]
    HTTP --> API --> SCHED --> KV --> EXEC --> GPU
    style HTTP fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style API fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style SCHED fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style KV fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style EXEC fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style GPU fill:#fce4ec,stroke:#c62828,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.4.html|1"] = """flowchart LR
    PF["<b>Prefill</b><br/><i>TTFT</i>"]
    DEC["<b>Decode</b><br/><i>N tokens x TPOT each</i>"]
    E2E["<b>End-to-End Latency</b><br/>= TTFT + (N x TPOT)"]
    PF --> DEC --> E2E
    style PF fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style DEC fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style E2E fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-09-inference-optimization/section-9.5.html|0"] = """flowchart LR
    DENSE["<b>Dense weights</b><br/>0.3 0.0 0.7 0.0<br/>0.0 0.5 0.0 0.9"]
    PRUNE["<b>2:4 Prune</b><br/>Keep 2 of every 4"]
    COMP["<b>Compressed</b><br/>Values: 0.3 0.7 0.5 0.9<br/>+ 2-bit index metadata"]
    NOTE["Memory: 50% of original<br/>Throughput: ~2x on Tensor Cores"]
    DENSE --> PRUNE --> COMP --> NOTE
    style DENSE fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style PRUNE fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style COMP fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    # Section 18.x: Interpretability
    CURATED_DIAGRAMS["part-2-understanding-llms/module-18-interpretability/section-18.1.html|0"] = """flowchart TB
    subgraph HEADS["Attention Head Types"]
        direction LR
        PREV["<b>Previous Token</b><br/>attends to t-1"]
        IND["<b>Induction Head</b><br/>copies previous pattern"]
        POS["<b>Positional Head</b><br/>attends to BOS/first"]
        SEM["<b>Semantic Head</b><br/>attends to related tokens"]
    end
    style PREV fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style IND fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style POS fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style SEM fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-18-interpretability/section-18.1.html|1"] = """flowchart LR
    L0["<b>Layer 0</b><br/>Top: 'the' (noisy)"]
    L4["<b>Layer 4</b><br/>Top: 'France' (weak)"]
    L8["<b>Layer 8</b><br/>Top: 'Paris' (strong)"]
    L11["<b>Layer 11</b><br/>Top: 'Paris' (final)"]
    INPUT["The Eiffel Tower is in ___"]
    UE["<b>Unembedding W_U</b>"]
    INPUT --> UE
    L0 --> L4 --> L8 --> L11
    style L0 fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style L4 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style L8 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style L11 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-18-interpretability/section-18.2.html|0"] = """flowchart LR
    EMB["<b>Embed</b>"]
    A0["Attn 0.0"]
    A1["Attn 0.1"]
    M0["MLP 0"]
    A2["Attn 1.0"]
    M1["MLP 1"]
    OUT["<b>Output</b>"]
    EMB -->|"+ write"| A0 -->|"+ write"| A1 -->|"+ write"| M0 -->|"+ write"| A2 -->|"+ write"| M1 --> OUT
    NOTE["Each component reads from and writes<br/>to the shared residual stream"]
    M1 --> NOTE
    style EMB fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style OUT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-18-interpretability/section-18.2.html|1"] = """flowchart LR
    subgraph CLEAN["No Superposition"]
        direction TB
        C1["1 feature = 1 neuron"]
        C2["cat, dog, blue"]
        C3["Clean, interpretable"]
        C4["But limited: 3 neurons, 3 features"]
    end
    subgraph SUP["Superposition"]
        direction TB
        S1["Many features share neurons"]
        S2["cat+legal, dog+blue"]
        S3["5+ features in 3 neurons"]
        S4["Higher capacity, harder to interpret"]
    end
    style CLEAN fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style SUP fill:#fff3e0,stroke:#e65100,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-18-interpretability/section-18.3.html|0"] = """flowchart TB
    subgraph EXTRACT["Control Vector Extraction"]
        direction TB
        E1["Run model on contrastive prompts"]
        E2["Extract direction in activation space"]
    end
    subgraph STEER["Steered Generation"]
        direction LR
        H["h = transformer_layer(x)"]
        CV["+ a * control_vector"]
        HP["h' = steered hidden state"]
        H --> CV --> HP
    end
    EXTRACT --> STEER
    style EXTRACT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style STEER fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-18-interpretability/section-18.3.html|1"] = """flowchart LR
    BUG["<b>Bug Report</b><br/>Model hallucinates X"]
    ATTR["<b>Attribution</b><br/>Which tokens caused it?<br/><i>IG, SHAP, attention</i>"]
    LOC["<b>Localize</b><br/>Which layers/heads?<br/><i>Activation patching</i>"]
    FIX["<b>Fix</b><br/>Edit, steer, or retrain<br/><i>ROME, RepE, fine-tune</i>"]
    BUG --> ATTR --> LOC --> FIX
    style BUG fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style ATTR fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style LOC fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style FIX fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-18-interpretability/section-18.4.html|0"] = """flowchart LR
    subgraph RAW["Raw Attention"]
        direction TB
        R1["'it' attends to 'cat' (0.7)"]
        R2["Only one layer visible"]
        R3["Misses indirect flow"]
    end
    subgraph ROLL["Attention Rollout"]
        direction TB
        A1["'it' traces to 'cat' (0.45)"]
        A2["'sat' (0.25), 'The' (0.15)"]
        A3["Accounts for all layers"]
    end
    style RAW fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style ROLL fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    CURATED_DIAGRAMS["part-2-understanding-llms/module-18-interpretability/section-18.4.html|1"] = """flowchart TB
    subgraph METHODS["Explanation Methods"]
        direction LR
        RA["Raw Attn<br/><i>low cost, low faith</i>"]
        RO["Rollout<br/><i>low cost</i>"]
        GA["Grad x Attn"]
        IG["IG"]
        LRP["LRP"]
        SHAP["Perturb/SHAP<br/><i>high cost, high faith</i>"]
    end
    RA --> RO --> GA --> IG --> LRP --> SHAP
    style RA fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style SHAP fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px"""

    # Rest will be auto-generated

load_curated()


def process_all_files():
    """Process all HTML files with remaining SVGs."""
    # Find all files still containing SVGs
    import subprocess
    result = subprocess.run(
        ['grep', '-rl', '<svg', '--include=section-*.html', '--include=index.html'],
        capture_output=True, text=True, cwd=str(BASE_DIR)
    )
    files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    files = [f for f in files if '_archive/' not in f and 'front-matter/pathways' not in f]
    files.sort()

    total_svgs = 0
    total_replaced = 0
    errors = []

    for filepath in files:
        html_path = BASE_DIR / filepath
        svgs = extract_svg_info(html_path)
        if not svgs:
            continue

        total_svgs += len(svgs)
        print(f"\n{'='*60}")
        print(f"Processing {filepath} ({len(svgs)} SVGs)")

        # Prepare replacements
        replacements = []
        for svg in svgs:
            key = f"{filepath}|{svg['index']}"

            # Determine image filename
            fig_match = re.search(r'Figure (\d+\.\d+\.\d+)', svg['caption'])
            if fig_match:
                fig_num = fig_match.group(1)
                slug = slugify(svg['caption'][svg['caption'].find(':')+1:].strip()[:60] if ':' in svg['caption'] else svg['caption'][:60])
                img_name = f"fig-{fig_num}-{slug}.png"
            else:
                section = html_path.stem  # e.g., section-0.1
                img_name = f"{section}-svg{svg['index']+1}.png"

            img_src = f"images/{img_name}"
            img_path = html_path.parent / "images" / img_name

            # Check if already converted
            if img_path.exists():
                print(f"  SVG#{svg['index']}: Already converted ({img_name}), skipping render")
                # Still need to replace if SVG still in HTML
                alt = sanitize_label(svg['caption'][:120]) if svg['caption'] else 'Diagram'
                replacements.append({
                    'svg_index': svg['index'],
                    'img_src': img_src,
                    'alt': alt,
                    'rendered': True,
                })
                continue

            # Get Mermaid content
            if key in CURATED_DIAGRAMS:
                mmd = CURATED_DIAGRAMS[key]
                print(f"  SVG#{svg['index']}: Using curated diagram")
            else:
                mmd = generate_mermaid_from_svg(svg, html_path.stem)
                print(f"  SVG#{svg['index']}: Auto-generated diagram")

            # Render
            rendered = render_mermaid(mmd, img_path, width=1100)
            alt = sanitize_label(svg['caption'][:120]) if svg['caption'] else 'Diagram'
            replacements.append({
                'svg_index': svg['index'],
                'img_src': img_src,
                'alt': alt,
                'rendered': rendered is not None,
            })

        # Replace SVGs in reverse order
        content = html_path.read_text(encoding='utf-8')
        svgs_in_html = list(re.finditer(r'<svg[^>]*>.*?</svg>', content, re.DOTALL))

        # Sort replacements by svg_index descending
        replacements.sort(key=lambda x: x['svg_index'], reverse=True)

        for rep in replacements:
            if not rep['rendered']:
                errors.append(f"Render failed: {filepath} SVG#{rep['svg_index']}")
                continue
            idx = rep['svg_index']
            if idx >= len(svgs_in_html):
                errors.append(f"SVG index {idx} out of range: {filepath}")
                continue

            svg_match = svgs_in_html[idx]

            # Archive
            archive_name = f"{html_path.stem}-svg{idx+1}.html"
            archive_path = ARCHIVE_DIR / archive_name
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            if not archive_path.exists():
                archive_path.write_text(svg_match.group()[:50000], encoding="utf-8")

            # Replace
            img_tag = f'<img src="{rep["img_src"]}" alt="{rep["alt"]}" loading="lazy" style="max-width: 100%;">'
            content = content[:svg_match.start()] + img_tag + content[svg_match.end():]
            total_replaced += 1
            print(f"  Replaced SVG#{idx} with {rep['img_src']}")

        html_path.write_text(content, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"Total SVGs found: {total_svgs}")
    print(f"Total replaced: {total_replaced}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")


if __name__ == "__main__":
    process_all_files()
