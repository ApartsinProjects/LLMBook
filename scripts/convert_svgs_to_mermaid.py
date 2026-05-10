#!/usr/bin/env python3
"""
Convert inline SVGs in HTML files to Mermaid diagrams rendered as PNG.

Reads the audit report to find files with inline SVGs, then for each SVG:
1. Extracts text labels, shape counts, and structural info from the SVG
2. Extracts surrounding prose context (h2 heading, caption, paragraphs)
3. Analyzes the SVG structure to determine the best Mermaid diagram type
4. Generates a .mmd Mermaid source file with proper styling
5. Renders it to PNG via mmdc
6. Replaces the inline SVG in the HTML with an <img> tag

Usage:
    python convert_svgs_to_mermaid.py [--limit N] [--dry-run] [--start-at N]
"""

import re
import os
import sys
import io
import json
import subprocess
import argparse
import html as html_mod
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(r"E:/Projects/LLMCourse")
AUDIT_REPORT = PROJECT_ROOT / "scripts" / "audit_inline_svgs_report.txt"
MERMAID_CONFIG = PROJECT_ROOT / "scripts" / "mermaid" / "mermaid-config.json"
MMDC_CMD = "npx mmdc"

# Book color palette for Mermaid styling
COLORS = {
    "blue_bg": "#e8f4fd",
    "blue_border": "#3498db",
    "green_bg": "#e8f5e9",
    "green_border": "#27ae60",
    "purple_bg": "#f0e6ff",
    "purple_border": "#8e44ad",
    "orange_bg": "#fef9e7",
    "orange_border": "#f39c12",
    "red_bg": "#fdedec",
    "red_border": "#e74c3c",
    "dark_bg": "#2c3e50",
    "dark_text": "#1a1a2e",
    "gray_bg": "#f8f9fa",
    "gray_border": "#6c757d",
}

# Style classes for Mermaid nodes
STYLE_DEFS = """
    classDef blue fill:#e8f4fd,stroke:#3498db,stroke-width:2px,color:#1a1a2e
    classDef green fill:#e8f5e9,stroke:#27ae60,stroke-width:2px,color:#1a1a2e
    classDef purple fill:#f0e6ff,stroke:#8e44ad,stroke-width:2px,color:#1a1a2e
    classDef orange fill:#fef9e7,stroke:#f39c12,stroke-width:2px,color:#1a1a2e
    classDef red fill:#fdedec,stroke:#e74c3c,stroke-width:2px,color:#1a1a2e
    classDef dark fill:#2c3e50,stroke:#1a1a2e,stroke-width:2px,color:#ecf0f1
    classDef gray fill:#f8f9fa,stroke:#6c757d,stroke-width:2px,color:#1a1a2e
    classDef emphasis fill:#2c3e50,stroke:#1a1a2e,stroke-width:2px,color:#ecf0f1
"""


# ============================================================
# Data Structures
# ============================================================

@dataclass
class SVGInfo:
    """Information extracted from a single inline SVG and its context."""
    file_path: str            # Relative path from project root
    svg_index: int            # Which SVG in the file (0-based)
    svg_text: str             # The full <svg>...</svg> markup
    text_labels: list         # All <text> content from SVG
    rect_count: int = 0
    circle_count: int = 0
    line_count: int = 0
    path_count: int = 0
    polygon_count: int = 0
    ellipse_count: int = 0
    caption: str = ""         # figcaption or diagram-caption text
    figure_id: str = ""       # e.g. "Figure 11.1.2"
    heading: str = ""         # The <h2> this SVG appears under
    context_before: str = ""  # 1-2 paragraphs before the SVG
    context_after: str = ""   # 1 paragraph after the SVG
    diagram_type: str = ""    # flowchart, hierarchy, comparison, cycle, etc.
    mmd_path: str = ""        # Output .mmd path
    png_path: str = ""        # Output .png path


# ============================================================
# Parsing
# ============================================================

def parse_audit_report(report_path: Path) -> list[dict]:
    """Parse the audit report to get a list of (file, svg_info) entries."""
    entries = []
    current_file = None
    current_entry = {}

    with open(report_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()

            # Match file lines
            m = re.match(r"\s+File:\s+(.+)", line)
            if m:
                if current_entry and current_file:
                    entries.append(current_entry.copy())
                current_file = m.group(1).strip()
                current_entry = {"file": current_file}
                continue

            # Match caption
            m = re.match(r"\s+Caption:\s+(.+)", line)
            if m:
                current_entry["caption"] = m.group(1).strip()
                continue

            # Match elements
            m = re.match(r"\s+Elements:\s+(.+)", line)
            if m:
                current_entry["elements"] = m.group(1).strip()
                continue

            # Match text labels
            m = re.match(r"\s+Text labels:\s+(.+)", line)
            if m:
                try:
                    labels_str = m.group(1).strip()
                    current_entry["text_labels"] = eval(labels_str)
                except Exception:
                    current_entry["text_labels"] = []
                continue

            # Match SVG size
            m = re.match(r"\s+SVG size:\s+(.+)", line)
            if m:
                current_entry["svg_size"] = m.group(1).strip()
                continue

        # Don't forget the last entry
        if current_entry and current_file:
            entries.append(current_entry)

    return entries


def extract_svgs_from_html(html_path: Path) -> list[dict]:
    """Extract all inline SVGs from an HTML file with their context."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    svgs = []

    # Find all <svg ...>...</svg> blocks (non-greedy, but SVGs can nest via <use>, so be careful)
    # Use a regex that handles the nesting by finding the outermost svg tags
    svg_pattern = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL)
    matches = list(svg_pattern.finditer(content))

    for i, match in enumerate(matches):
        svg_text = match.group(0)
        start_pos = match.start()
        end_pos = match.end()

        # Extract text labels from SVG
        text_labels = re.findall(r"<text[^>]*>(.*?)</text>", svg_text, re.DOTALL)
        # Clean up labels: strip tags, decode entities
        clean_labels = []
        for label in text_labels:
            label = re.sub(r"<[^>]+>", "", label)
            label = html_mod.unescape(label).strip()
            if label and label not in ["", " "]:
                clean_labels.append(label)

        # Count shapes
        rect_count = len(re.findall(r"<rect\b", svg_text))
        circle_count = len(re.findall(r"<circle\b", svg_text))
        line_count = len(re.findall(r"<line\b", svg_text))
        path_count = len(re.findall(r"<path\b", svg_text))
        polygon_count = len(re.findall(r"<polygon\b", svg_text))
        ellipse_count = len(re.findall(r"<ellipse\b", svg_text))

        # Get caption (look for diagram-caption div or figcaption after the SVG)
        caption = ""
        figure_id = ""
        after_svg = content[end_pos:end_pos + 500]
        cap_m = re.search(
            r'<div\s+class="diagram-caption">(.*?)</div>',
            after_svg, re.DOTALL
        )
        if not cap_m:
            cap_m = re.search(r"<figcaption>(.*?)</figcaption>", after_svg, re.DOTALL)
        if cap_m:
            caption = re.sub(r"<[^>]+>", "", cap_m.group(1)).strip()
            fig_m = re.match(r"(Figure\s+[\d.]+)", caption)
            if fig_m:
                figure_id = fig_m.group(1)

        # Get the h2 heading this SVG appears under
        heading = ""
        before_svg = content[:start_pos]
        h2_matches = re.findall(r"<h2[^>]*>(.*?)</h2>", before_svg, re.DOTALL)
        if h2_matches:
            heading = re.sub(r"<[^>]+>", "", h2_matches[-1]).strip()

        # Get 1-2 paragraphs of context before the SVG
        context_before = ""
        # Find the parent div.diagram-container
        container_start = content.rfind('<div class="diagram-container">', 0, start_pos)
        if container_start == -1:
            container_start = start_pos
        before_text = content[max(0, container_start - 2000):container_start]
        paras = re.findall(r"<p>(.*?)</p>", before_text, re.DOTALL)
        if paras:
            # Take last 2 paragraphs
            context_paras = paras[-2:] if len(paras) >= 2 else paras
            context_before = " ".join(
                re.sub(r"<[^>]+>", "", p).strip() for p in context_paras
            )

        # Get 1 paragraph after the diagram container
        context_after = ""
        container_end_search = content[end_pos:end_pos + 1000]
        container_end_m = re.search(r"</div>\s*</div>", container_end_search)
        if container_end_m:
            after_container = container_end_search[container_end_m.end():]
        else:
            after_container = container_end_search[200:]
        after_p = re.search(r"<p>(.*?)</p>", after_container, re.DOTALL)
        if after_p:
            context_after = re.sub(r"<[^>]+>", "", after_p.group(1)).strip()

        # Find the full extent of the diagram-container div wrapping this SVG
        # This is the text we will replace in the HTML
        container_re = re.compile(
            r'(<div\s+class="diagram-container">\s*)'
            + re.escape(svg_text)
            + r'(.*?</div>\s*</div>)',
            re.DOTALL
        )
        full_match = container_re.search(content)
        if full_match:
            full_container = full_match.group(0)
        else:
            full_container = svg_text

        svgs.append({
            "index": i,
            "svg_text": svg_text,
            "full_container": full_container,
            "text_labels": clean_labels,
            "rect_count": rect_count,
            "circle_count": circle_count,
            "line_count": line_count,
            "path_count": path_count,
            "polygon_count": polygon_count,
            "ellipse_count": ellipse_count,
            "caption": caption,
            "figure_id": figure_id,
            "heading": heading,
            "context_before": context_before,
            "context_after": context_after,
        })

    return svgs


# ============================================================
# Diagram Type Detection
# ============================================================

def detect_diagram_type(svg_info: dict) -> str:
    """Analyze SVG structure to determine the best Mermaid diagram type."""
    labels = svg_info["text_labels"]
    labels_lower = " ".join(labels).lower()
    rects = svg_info["rect_count"]
    circles = svg_info["circle_count"]
    lines = svg_info["line_count"]
    paths = svg_info["path_count"]
    polygons = svg_info["polygon_count"]
    caption = svg_info.get("caption", "").lower()
    heading = svg_info.get("heading", "").lower()

    # Check for cycle/loop patterns
    cycle_words = ["cycle", "loop", "iterate", "repeat", "circular", "feedback"]
    if any(w in labels_lower for w in cycle_words) or any(w in caption for w in cycle_words):
        return "cycle"

    # Check for decision tree / flowchart with yes/no
    if any(l.lower() in ("yes", "no", "y", "n") for l in labels):
        return "decision_tree"

    # Check for numbered steps / pipeline / sequence
    step_pattern = re.compile(r"^(step\s*\d|stage\s*\d|\d+[.:)]|\d+\.\s)", re.IGNORECASE)
    step_labels = [l for l in labels if step_pattern.match(l)]
    if len(step_labels) >= 2:
        return "pipeline"

    # Check for comparison (two or more parallel groups)
    vs_words = ["vs", "versus", "compared", "comparison"]
    if any(w in labels_lower for w in vs_words):
        return "comparison"

    # Check for hierarchy / layers
    layer_words = ["layer", "level", "tier"]
    if any(w in labels_lower for w in layer_words):
        return "hierarchy"

    # Check for spectrum / scale
    spectrum_words = ["spectrum", "scale", "range", "axis", "continuum"]
    if any(w in labels_lower for w in spectrum_words) or any(w in caption for w in spectrum_words):
        return "spectrum"

    # Arrow patterns (lines + polygons) suggest flowcharts
    arrow_count = lines + polygons + paths
    if arrow_count >= 4 and rects >= 3:
        return "flowchart"

    # Many circles suggest a network/graph
    if circles >= 4:
        return "graph"

    # Many rects in a grid pattern suggest comparison table
    if rects >= 8 and lines < 3:
        return "comparison"

    # Default: if there are connections, it is a flowchart; otherwise a hierarchy
    if arrow_count >= 2:
        return "flowchart"

    return "hierarchy"


# ============================================================
# Mermaid Generation
# ============================================================

def sanitize_label(text: str, for_diamond: bool = False) -> str:
    """Make a label safe for Mermaid HTML labels."""
    # Remove problematic characters
    text = text.replace('"', "'")
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    # Remove arrow characters that could confuse Mermaid
    text = text.replace("→", "to")
    text = text.replace("←", "from")
    text = text.replace("↓", "")
    text = text.replace("↑", "")
    text = text.replace("▼", "")
    text = text.replace("▲", "")
    # For diamond nodes, parentheses, brackets, and special chars cause parse errors
    if for_diamond:
        text = text.replace("(", "")
        text = text.replace(")", "")
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("+", " plus ")
        text = text.replace("#", "num")
    return text.strip()


def make_node_id(index: int) -> str:
    """Generate a clean node ID."""
    return f"N{index}"


def group_labels_into_nodes(labels: list[str]) -> list[dict]:
    """
    Group consecutive labels into logical nodes.

    The SVG typically has pairs/triples: a title label followed by description labels.
    We detect this by looking at label patterns:
    - Short bold-looking labels (title) followed by longer descriptive labels
    - Numbered items (1., 2., etc.)
    - Connector labels (arrows, "to", etc.) are skipped
    """
    nodes = []
    skip_labels = {"", " ", "→", "←", "↓", "↑", "▼", "▲", "|"}
    i = 0
    while i < len(labels):
        label = labels[i].strip()
        if label in skip_labels:
            i += 1
            continue

        node = {"title": label, "description": ""}

        # Check if next labels are descriptions (longer text, not a new node title)
        descs = []
        j = i + 1
        while j < len(labels) and j <= i + 3:
            next_label = labels[j].strip()
            if next_label in skip_labels:
                j += 1
                continue
            # Heuristic: if next label is short and looks like a title, stop
            # Description labels tend to be longer or contain specific patterns
            is_likely_desc = (
                len(next_label) > len(label) * 0.5
                and not re.match(r"^(Level|Step|Stage|Phase|Gate|Layer)\s*\d", next_label, re.IGNORECASE)
                and not re.match(r"^\d+[.:)]", next_label)
                and not re.match(r"^[A-Z][a-z]+\s*$", next_label)
                and len(next_label) < 80
            )
            if is_likely_desc and len(descs) < 2:
                descs.append(next_label)
                j += 1
            else:
                break

        if descs:
            node["description"] = ", ".join(descs)
            i = j
        else:
            i += 1

        nodes.append(node)

    return nodes


def assign_colors(nodes: list[dict], diagram_type: str) -> list[str]:
    """Assign color classes to nodes based on position and diagram type."""
    color_cycle = ["blue", "green", "purple", "orange", "red", "gray"]
    n = len(nodes)

    if diagram_type in ("pipeline", "flowchart", "cycle"):
        # Cycle through colors sequentially
        return [color_cycle[i % len(color_cycle)] for i in range(n)]
    elif diagram_type == "decision_tree":
        # Root gets dark, branches get alternating colors
        colors = ["dark"]
        for i in range(1, n):
            colors.append(color_cycle[(i - 1) % len(color_cycle)])
        return colors
    elif diagram_type == "comparison":
        # Alternate between two color groups
        return ["blue" if i % 2 == 0 else "green" for i in range(n)]
    elif diagram_type == "hierarchy":
        # Top-down gradient
        return [color_cycle[min(i, len(color_cycle) - 1)] for i in range(n)]
    else:
        return [color_cycle[i % len(color_cycle)] for i in range(n)]


def generate_mermaid(svg_info: dict) -> str:
    """Generate a Mermaid diagram source from SVG analysis."""
    labels = svg_info["text_labels"]
    diagram_type = svg_info.get("diagram_type", "flowchart")
    caption = svg_info.get("caption", "")
    heading = svg_info.get("heading", "")

    # Group labels into logical nodes
    nodes = group_labels_into_nodes(labels)

    if not nodes:
        return ""

    colors = assign_colors(nodes, diagram_type)

    # Build Mermaid source
    lines = []

    if diagram_type == "decision_tree":
        lines.append("flowchart TB")
        lines.append("")
        # Build a tree structure based on Yes/No labels
        node_ids = []
        for i, node in enumerate(nodes):
            nid = make_node_id(i)
            is_decision = "?" in node["title"] or "?" in node.get("description", "")
            title = sanitize_label(node["title"], for_diamond=is_decision)
            desc = sanitize_label(node["description"], for_diamond=is_decision)
            if is_decision:
                # Decision node (diamond)
                content = title
                if desc:
                    content += f"<br/><i>{desc}</i>"
                lines.append(f'    {nid}{{{{{content}}}}}')
            else:
                content = f"<b>{title}</b>"
                if desc:
                    content += f"<br/><i>{desc}</i>"
                lines.append(f'    {nid}["{content}"]')
            node_ids.append(nid)

        # Connect nodes: try to detect yes/no branching
        for i, node in enumerate(nodes):
            title_lower = node["title"].lower()
            if title_lower in ("yes", "no") and i > 0:
                # Connect the previous decision to this outcome
                # Find the nearest decision node before this
                for k in range(i - 1, -1, -1):
                    if "?" in nodes[k]["title"] or "?" in nodes[k].get("description", ""):
                        edge_label = node["title"]
                        lines.append(f"    {node_ids[k]} -->|{edge_label}| {node_ids[i]}")
                        break
            elif i > 0 and nodes[i - 1]["title"].lower() not in ("yes", "no"):
                # Default sequential connection
                lines.append(f"    {node_ids[i-1]} --> {node_ids[i]}")

    elif diagram_type == "pipeline":
        lines.append("flowchart LR")
        lines.append("")
        node_ids = []
        for i, node in enumerate(nodes):
            nid = make_node_id(i)
            title = sanitize_label(node["title"])
            desc = sanitize_label(node["description"])
            content = f"<b>{title}</b>"
            if desc:
                content += f"<br/><i>{desc}</i>"
            lines.append(f'    {nid}["{content}"]')
            node_ids.append(nid)

        # Sequential connections
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")

    elif diagram_type == "cycle":
        lines.append("flowchart LR")
        lines.append("")
        node_ids = []
        for i, node in enumerate(nodes):
            nid = make_node_id(i)
            title = sanitize_label(node["title"])
            desc = sanitize_label(node["description"])
            content = f"<b>{title}</b>"
            if desc:
                content += f"<br/><i>{desc}</i>"
            lines.append(f'    {nid}["{content}"]')
            node_ids.append(nid)

        # Sequential + loop back
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")
        if len(node_ids) >= 3:
            lines.append(f"    {node_ids[-1]} -.-> {node_ids[0]}")

    elif diagram_type == "comparison":
        lines.append("flowchart TB")
        lines.append("")
        # Try to split nodes into two groups for side-by-side comparison
        mid = len(nodes) // 2
        if mid == 0:
            mid = 1
        group_a = nodes[:mid]
        group_b = nodes[mid:]

        lines.append('    subgraph left [" "]')
        left_ids = []
        for i, node in enumerate(group_a):
            nid = f"L{i}"
            title = sanitize_label(node["title"])
            desc = sanitize_label(node["description"])
            content = f"<b>{title}</b>"
            if desc:
                content += f"<br/><i>{desc}</i>"
            lines.append(f'        {nid}["{content}"]')
            left_ids.append(nid)
        lines.append("    end")

        lines.append('    subgraph right [" "]')
        right_ids = []
        for i, node in enumerate(group_b):
            nid = f"R{i}"
            title = sanitize_label(node["title"])
            desc = sanitize_label(node["description"])
            content = f"<b>{title}</b>"
            if desc:
                content += f"<br/><i>{desc}</i>"
            lines.append(f'        {nid}["{content}"]')
            right_ids.append(nid)
        lines.append("    end")

        # Connect within groups
        for ids in [left_ids, right_ids]:
            for i in range(len(ids) - 1):
                lines.append(f"    {ids[i]} --> {ids[i+1]}")

    elif diagram_type == "hierarchy":
        lines.append("flowchart TB")
        lines.append("")
        node_ids = []
        for i, node in enumerate(nodes):
            nid = make_node_id(i)
            title = sanitize_label(node["title"])
            desc = sanitize_label(node["description"])
            content = f"<b>{title}</b>"
            if desc:
                content += f"<br/><i>{desc}</i>"
            lines.append(f'    {nid}["{content}"]')
            node_ids.append(nid)

        # Connect top-down
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")

    elif diagram_type == "spectrum":
        lines.append("flowchart LR")
        lines.append("")
        node_ids = []
        for i, node in enumerate(nodes):
            nid = make_node_id(i)
            title = sanitize_label(node["title"])
            desc = sanitize_label(node["description"])
            content = f"<b>{title}</b>"
            if desc:
                content += f"<br/><i>{desc}</i>"
            lines.append(f'    {nid}["{content}"]')
            node_ids.append(nid)

        # Connect left-to-right with dotted lines for spectrum
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} -.- {node_ids[i+1]}")

    elif diagram_type == "graph":
        lines.append("flowchart TB")
        lines.append("")
        node_ids = []
        for i, node in enumerate(nodes):
            nid = make_node_id(i)
            title = sanitize_label(node["title"])
            desc = sanitize_label(node["description"])
            content = f"<b>{title}</b>"
            if desc:
                content += f"<br/><i>{desc}</i>"
            # Use circles for graph nodes
            lines.append(f'    {nid}(("{content}"))')
            node_ids.append(nid)

        # Connect in a reasonable pattern for graphs
        if len(node_ids) >= 2:
            # Connect first node to several others as a hub
            for i in range(1, min(len(node_ids), 5)):
                lines.append(f"    {node_ids[0]} --- {node_ids[i]}")
            # Connect remaining nodes
            for i in range(2, len(node_ids)):
                if i + 1 < len(node_ids):
                    lines.append(f"    {node_ids[i]} --- {node_ids[i+1]}")

    else:
        # Default: flowchart TB
        lines.append("flowchart TB")
        lines.append("")
        node_ids = []
        for i, node in enumerate(nodes):
            nid = make_node_id(i)
            title = sanitize_label(node["title"])
            desc = sanitize_label(node["description"])
            content = f"<b>{title}</b>"
            if desc:
                content += f"<br/><i>{desc}</i>"
            lines.append(f'    {nid}["{content}"]')
            node_ids.append(nid)
        for i in range(len(node_ids) - 1):
            lines.append(f"    {node_ids[i]} --> {node_ids[i+1]}")

    # Add style classes
    lines.append("")
    lines.append(STYLE_DEFS.rstrip())
    lines.append("")

    # Apply colors to nodes
    all_node_ids = re.findall(r"^\s+(N\d+|L\d+|R\d+)\b", "\n".join(lines), re.MULTILINE)
    # Deduplicate while preserving order
    seen = set()
    unique_ids = []
    for nid in all_node_ids:
        if nid not in seen:
            seen.add(nid)
            unique_ids.append(nid)

    for i, nid in enumerate(unique_ids):
        color = colors[i % len(colors)] if i < len(colors) else colors[i % len(colors)]
        lines.append(f"    class {nid} {color}")

    return "\n".join(lines)


# ============================================================
# Rendering and Replacement
# ============================================================

def generate_output_filename(file_path: str, svg_index: int, figure_id: str) -> str:
    """Generate a meaningful filename for the output .mmd and .png."""
    # Extract section number from filename
    basename = Path(file_path).stem  # e.g., "section-10.3"
    if figure_id:
        # Use figure ID: "figure-10.3.2" -> "section-10.3-fig2"
        fig_num = figure_id.replace("Figure ", "").replace(" ", "")
        return f"{basename}-svg{svg_index + 1}"
    return f"{basename}-svg{svg_index + 1}"


def render_mermaid(mmd_path: Path, png_path: Path) -> bool:
    """Render a .mmd file to PNG using mmdc."""
    cmd = (
        f'npx mmdc -i "{mmd_path}" -o "{png_path}" '
        f'-c "{MERMAID_CONFIG}" '
        f'-w 1200 -s 3 --backgroundColor white'
    )
    print(f"  Rendering: {cmd}")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=60,
            cwd=str(PROJECT_ROOT)
        )
        if result.returncode != 0:
            print(f"  ERROR: mmdc failed: {result.stderr[:500]}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print("  ERROR: mmdc timed out")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def replace_svg_in_html(html_path: Path, svg_text: str, png_rel_path: str,
                        caption: str, figure_id: str) -> bool:
    """Replace an inline SVG in the HTML with an <img> tag in a diagram-container."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the SVG in its container
    # The SVG might be wrapped in <div class="diagram-container">
    # We need to find the full container and replace it

    # Build the replacement HTML
    alt_text = caption if caption else "Diagram"
    # Truncate alt text if too long
    if len(alt_text) > 200:
        alt_text = alt_text[:200] + "..."

    png_filename = Path(png_rel_path).name
    img_tag = f'<img src="images/{png_filename}" alt="{sanitize_label(alt_text)}" loading="lazy">'

    # Build replacement: keep caption if it exists
    caption_html = ""
    if caption:
        if figure_id:
            caption_html = f'\n <div class="diagram-caption"><strong>{figure_id}</strong>: {caption[len(figure_id)+2:].strip()}</div>'
        else:
            caption_html = f'\n <div class="diagram-caption">{caption}</div>'

    replacement = f'<div class="diagram-container">\n {img_tag}{caption_html}\n </div>'

    # Try to find and replace the container with the SVG
    # Strategy: find the SVG text, then expand to its container div
    svg_pos = content.find(svg_text)
    if svg_pos == -1:
        # SVG not found (maybe already replaced?)
        print(f"  WARNING: SVG not found in {html_path}")
        return False

    # Find the start of the diagram-container div
    search_back = content[max(0, svg_pos - 200):svg_pos]
    container_marker = '<div class="diagram-container">'
    container_offset = search_back.rfind(container_marker)

    if container_offset != -1:
        container_start = max(0, svg_pos - 200) + container_offset
    else:
        container_start = svg_pos

    # Find the end of the container (after caption div and closing div)
    after_svg = content[svg_pos + len(svg_text):]

    # Look for the caption and closing </div> tags
    # Pattern: optional whitespace, optional caption div, optional whitespace, </div>
    end_pattern = re.compile(
        r'(\s*<div\s+class="diagram-caption">.*?</div>)?\s*</div>',
        re.DOTALL
    )
    end_match = end_pattern.match(after_svg)

    if end_match and container_offset != -1:
        container_end = svg_pos + len(svg_text) + end_match.end()
        old_text = content[container_start:container_end]
    else:
        # Fallback: just replace the SVG tag itself
        old_text = svg_text
        replacement = img_tag

    # Debug: verify old_text is actually in content
    if old_text not in content:
        print(f"  DEBUG: old_text ({len(old_text)} chars) not found in content ({len(content)} chars)")
        print(f"  DEBUG: old_text starts with: {repr(old_text[:80])}")
        # Fallback: just replace the SVG tag directly
        if svg_text in content:
            print(f"  DEBUG: Falling back to direct SVG replacement")
            new_content = content.replace(svg_text, img_tag, 1)
        else:
            print(f"  WARNING: SVG text also not found, cannot replace")
            return False
    else:
        new_content = content.replace(old_text, replacement, 1)

    if new_content == content:
        print(f"  WARNING: No replacement made in {html_path}")
        return False

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


# ============================================================
# Main Processing
# ============================================================

def process_svg(html_path: Path, svg_info: dict, svg_index: int,
                dry_run: bool = False) -> bool:
    """Process a single SVG: analyze, generate Mermaid, render, replace."""
    file_rel = str(html_path.relative_to(PROJECT_ROOT))
    images_dir = html_path.parent / "images"

    # Detect diagram type
    diagram_type = detect_diagram_type(svg_info)
    svg_info["diagram_type"] = diagram_type

    # Generate output filenames
    base_name = generate_output_filename(file_rel, svg_index, svg_info.get("figure_id", ""))
    mmd_path = images_dir / f"{base_name}.mmd"
    png_path = images_dir / f"{base_name}.png"

    print(f"\n{'='*70}")
    print(f"Processing: {file_rel}, SVG #{svg_index + 1}")
    print(f"  Caption: {svg_info.get('caption', '(none)')[:80]}")
    print(f"  Heading: {svg_info.get('heading', '(none)')[:80]}")
    print(f"  Diagram type: {diagram_type}")
    print(f"  Labels ({len(svg_info['text_labels'])}): {svg_info['text_labels'][:8]}")
    print(f"  Shapes: rect={svg_info['rect_count']}, line={svg_info['line_count']}, "
          f"circle={svg_info['circle_count']}, path={svg_info['path_count']}")

    # Generate Mermaid source
    mermaid_src = generate_mermaid(svg_info)

    if not mermaid_src:
        print("  SKIP: No Mermaid content generated")
        return False

    print(f"  Output: {mmd_path}")
    print(f"\n--- Mermaid Source ---")
    print(mermaid_src)
    print(f"--- End Mermaid ---\n")

    if dry_run:
        print("  DRY RUN: skipping file writes and rendering")
        return True

    # Ensure images directory exists
    images_dir.mkdir(parents=True, exist_ok=True)

    # Write .mmd file
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mermaid_src)
    print(f"  Wrote: {mmd_path}")

    # Render to PNG
    success = render_mermaid(mmd_path, png_path)
    if not success:
        print(f"  FAILED to render: {mmd_path}")
        return False
    print(f"  Rendered: {png_path}")

    # Replace SVG in HTML
    success = replace_svg_in_html(
        html_path,
        svg_info["svg_text"],
        str(png_path.relative_to(html_path.parent)),
        svg_info.get("caption", ""),
        svg_info.get("figure_id", ""),
    )
    if success:
        print(f"  Replaced SVG in HTML")
    else:
        print(f"  WARNING: Could not replace SVG in HTML")

    return success


def build_replacement_html(png_filename: str, caption: str, figure_id: str) -> str:
    """Build the replacement HTML for a converted SVG."""
    alt_text = caption if caption else "Diagram"
    if len(alt_text) > 200:
        alt_text = alt_text[:200] + "..."

    # Always use forward slashes for HTML paths (not Windows backslashes)
    png_filename = png_filename.replace("\\", "/")
    img_tag = f'<img src="images/{png_filename}" alt="{sanitize_label(alt_text)}" loading="lazy">'

    caption_html = ""
    if caption:
        if figure_id:
            caption_html = f'\n <div class="diagram-caption"><strong>{figure_id}</strong>: {caption[len(figure_id)+2:].strip()}</div>'
        else:
            caption_html = f'\n <div class="diagram-caption">{caption}</div>'

    return f'<div class="diagram-container">\n {img_tag}{caption_html}\n </div>'


def find_container_extent(content: str, svg_text: str) -> tuple:
    """Find the full diagram-container extent around an SVG.
    Returns (start, end) positions in content, or None if not found."""
    svg_pos = content.find(svg_text)
    if svg_pos == -1:
        return None

    end_pos = svg_pos + len(svg_text)

    # Find the start of the diagram-container div
    search_back = content[max(0, svg_pos - 300):svg_pos]
    container_marker = '<div class="diagram-container">'
    container_offset = search_back.rfind(container_marker)

    if container_offset != -1:
        container_start = max(0, svg_pos - 300) + container_offset
    else:
        # No container found; just replace the SVG itself
        return (svg_pos, end_pos)

    # Find the end of the container (after caption div and closing div)
    after_svg = content[end_pos:]
    end_pattern = re.compile(
        r'(\s*<div\s+class="diagram-caption">.*?</div>)?\s*</div>',
        re.DOTALL
    )
    end_match = end_pattern.match(after_svg)

    if end_match:
        container_end = end_pos + end_match.end()
    else:
        container_end = end_pos

    return (container_start, container_end)


def main():
    parser = argparse.ArgumentParser(description="Convert inline SVGs to Mermaid diagrams")
    parser.add_argument("--limit", type=int, default=10,
                        help="Maximum number of SVGs to process (default: 10)")
    parser.add_argument("--start-at", type=int, default=0,
                        help="Skip this many SVGs before starting (default: 0)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate Mermaid source but do not render or modify HTML")
    parser.add_argument("--file", type=str, default=None,
                        help="Only process SVGs in this specific file (relative path)")
    args = parser.parse_args()

    print(f"SVG to Mermaid Converter")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Limit: {args.limit}, Start at: {args.start_at}, Dry run: {args.dry_run}")
    print()

    # Parse audit report to get the file list
    audit_entries = parse_audit_report(AUDIT_REPORT)
    print(f"Found {len(audit_entries)} SVG entries in audit report")

    # Get unique files from audit report
    unique_files = []
    seen_files = set()
    for entry in audit_entries:
        f = entry["file"]
        if f not in seen_files:
            seen_files.add(f)
            unique_files.append(f)

    print(f"Unique files with SVGs: {len(unique_files)}")

    # Process SVGs
    processed = 0
    skipped = 0
    succeeded = 0
    failed = 0
    global_svg_index = 0

    for rel_path in unique_files:
        if args.file and args.file not in rel_path:
            continue

        html_path = PROJECT_ROOT / rel_path
        if not html_path.exists():
            print(f"WARNING: File not found: {html_path}")
            continue

        # Extract SVGs from the actual HTML file
        svgs = extract_svgs_from_html(html_path)
        if not svgs:
            continue

        # Read the full file content once
        with open(html_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        file_modified = False
        images_dir = html_path.parent / "images"

        for svg_info in svgs:
            if global_svg_index < args.start_at:
                global_svg_index += 1
                skipped += 1
                continue

            if processed >= args.limit:
                break

            file_rel = str(html_path.relative_to(PROJECT_ROOT))
            svg_index = svg_info["index"]

            # Detect diagram type
            diagram_type = detect_diagram_type(svg_info)
            svg_info["diagram_type"] = diagram_type

            # Generate output filenames
            base_name = generate_output_filename(file_rel, svg_index, svg_info.get("figure_id", ""))
            mmd_path = images_dir / f"{base_name}.mmd"
            png_path = images_dir / f"{base_name}.png"

            print(f"\n{'='*70}")
            print(f"Processing: {file_rel}, SVG #{svg_index + 1}")
            print(f"  Caption: {svg_info.get('caption', '(none)')[:80]}")
            print(f"  Heading: {svg_info.get('heading', '(none)')[:80]}")
            print(f"  Diagram type: {diagram_type}")
            print(f"  Labels ({len(svg_info['text_labels'])}): {svg_info['text_labels'][:8]}")
            print(f"  Shapes: rect={svg_info['rect_count']}, line={svg_info['line_count']}, "
                  f"circle={svg_info['circle_count']}, path={svg_info['path_count']}")

            # Generate Mermaid source
            mermaid_src = generate_mermaid(svg_info)

            if not mermaid_src:
                print("  SKIP: No Mermaid content generated")
                failed += 1
                processed += 1
                global_svg_index += 1
                continue

            print(f"  Output: {mmd_path}")
            print(f"\n--- Mermaid Source ---")
            print(mermaid_src)
            print(f"--- End Mermaid ---\n")

            if args.dry_run:
                print("  DRY RUN: skipping file writes and rendering")
                succeeded += 1
                processed += 1
                global_svg_index += 1
                continue

            # Ensure images directory exists
            images_dir.mkdir(parents=True, exist_ok=True)

            # Write .mmd file
            with open(mmd_path, "w", encoding="utf-8") as f:
                f.write(mermaid_src)
            print(f"  Wrote: {mmd_path}")

            # Render to PNG
            render_ok = render_mermaid(mmd_path, png_path)
            if not render_ok:
                print(f"  FAILED to render: {mmd_path}")
                failed += 1
                processed += 1
                global_svg_index += 1
                continue
            print(f"  Rendered: {png_path}")

            # Replace SVG in the in-memory content
            svg_text = svg_info["svg_text"]
            extent = find_container_extent(file_content, svg_text)
            if extent is None:
                print(f"  WARNING: SVG not found in content, cannot replace")
                failed += 1
            else:
                start, end = extent
                png_filename = png_path.name
                replacement = build_replacement_html(
                    png_filename,
                    svg_info.get("caption", ""),
                    svg_info.get("figure_id", ""),
                )
                file_content = file_content[:start] + replacement + file_content[end:]
                file_modified = True
                print(f"  Replaced SVG in content (pos {start}:{end})")
                succeeded += 1

            processed += 1
            global_svg_index += 1

        # Write modified content back to file (once per file)
        if file_modified and not args.dry_run:
            svg_count_before = file_content.count("<svg")
            print(f"\n  Writing HTML: {html_path}")
            print(f"  Content length: {len(file_content)}, remaining SVGs: {svg_count_before}")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            # Verify write
            with open(html_path, "r", encoding="utf-8") as f:
                verify = f.read()
            verify_svgs = verify.count("<svg")
            verify_imgs = verify.count("-svg")
            print(f"  Verification: SVGs={verify_svgs}, img refs={verify_imgs}, length={len(verify)}")
            if verify != file_content:
                print(f"  ERROR: Written content does not match! Lengths: {len(file_content)} vs {len(verify)}")

        if processed >= args.limit:
            break

    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Processed: {processed}")
    print(f"Succeeded: {succeeded}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Remaining: {len(audit_entries) - global_svg_index}")


if __name__ == "__main__":
    main()
