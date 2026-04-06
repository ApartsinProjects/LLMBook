"""Scan all HTML files and identify SVGs that are charts/graphs (with axes and curves)."""
import re, json, os
from pathlib import Path

ROOT = Path(r"E:/Projects/LLMCourse")
results = []

for html_path in sorted(ROOT.rglob("*.html")):
    rel = html_path.relative_to(ROOT)
    # Skip non-content dirs
    if any(p in str(rel) for p in ['_archive', 'vendor', 'node_modules', '.git']):
        continue

    text = html_path.read_text(encoding='utf-8', errors='ignore')

    # Find all SVG blocks
    svg_pattern = re.compile(r'<svg\b[^>]*>(.*?)</svg>', re.DOTALL)
    for i, m in enumerate(svg_pattern.finditer(text)):
        svg_content = m.group(0)
        svg_inner = m.group(1)
        start_line = text[:m.start()].count('\n') + 1

        # Heuristics for chart detection:
        has_axes = bool(re.search(r'(x-axis|y-axis|axis|Error|Loss|Accuracy|Score)', svg_inner, re.I))

        # Check for axis labels (text with arrows or axis keywords)
        axis_labels = re.findall(r'<text[^>]*>([^<]*)</text>', svg_inner)
        axis_label_text = ' '.join(axis_labels).lower()

        chart_keywords = ['error', 'loss', 'accuracy', 'score', 'epoch', 'step',
                         'rate', 'complexity', 'parameter', 'size', 'performance',
                         'probability', 'frequency', 'count', 'time', 'iteration',
                         'training', 'validation', 'test', 'layer', 'dimension',
                         'perplexity', 'gradient', 'weight', 'tokens', 'flops',
                         'compute', 'data size', 'scale', 'temperature', 'top-',
                         'threshold', 'precision', 'recall', 'f1', 'bleu',
                         'rouge', 'latency', 'throughput', 'batch', 'learning rate',
                         'model complexity', 'noise floor', 'bias', 'variance',
                         'attention', 'softmax', 'cosine', 'similarity',
                         'reward', 'return', 'kl divergence', 'entropy']

        has_chart_labels = any(kw in axis_label_text for kw in chart_keywords)

        # Check for curve paths (smooth lines, not boxes)
        paths = re.findall(r'<path\s+d="([^"]*)"', svg_inner)
        has_curves = False
        for p in paths:
            # Curves typically use Q, C, S (quadratic/cubic bezier) or many L segments
            if re.search(r'[QCS]', p) and len(p) > 50:
                has_curves = True
                break
            # Many L segments = polyline chart
            if p.count('L') > 5:
                has_curves = True
                break

        # Check for axis lines (two perpendicular lines)
        lines = re.findall(r'<line\s+[^>]*>', svg_inner)

        # Check for polylines (common in charts)
        has_polyline = '<polyline' in svg_inner

        # Check for grid lines
        has_grid = bool(re.search(r'stroke-dasharray.*stroke-dasharray', svg_inner, re.DOTALL))

        # Get viewBox dimensions
        vb_match = re.search(r'viewBox="([^"]*)"', svg_content)
        viewBox = vb_match.group(1) if vb_match else ""

        # Get nearby caption
        after_svg = text[m.end():m.end()+500]
        caption_match = re.search(r'<(?:div class="diagram-caption"|figcaption)>(?:<strong>)?(Figure [^<]+)(?:</strong>)?[:\s]*([^<]*)', after_svg)
        caption = caption_match.group(0) if caption_match else ""

        # EXCLUDE: flowcharts (lots of rects, few curves)
        rect_count = svg_inner.count('<rect')
        circle_count = svg_inner.count('<circle')
        path_count = len(paths)
        marker_count = svg_inner.count('<marker')

        # Charts: have curves + chart labels, ratio of paths to rects higher
        is_chart = False

        if has_curves and has_chart_labels:
            is_chart = True
        elif has_polyline and has_chart_labels:
            is_chart = True
        elif has_curves and len(lines) >= 2 and (rect_count <= 3):
            # Axes (2 lines) + curves + few rects = likely chart
            is_chart = True

        # Exclude very small SVGs (icons)
        char_count = len(svg_content)
        if char_count < 500:
            is_chart = False

        # Exclude if too many rects relative to paths (likely flowchart)
        if rect_count > 8 and path_count <= 2:
            is_chart = False

        if is_chart:
            results.append({
                'file': str(rel).replace('\\', '/'),
                'svg_index': i + 1,
                'start_line': start_line,
                'caption': caption[:200],
                'viewBox': viewBox,
                'char_count': char_count,
                'labels': axis_labels[:15],
                'rect_count': rect_count,
                'path_count': path_count,
                'has_polyline': has_polyline,
            })

print(f"Found {len(results)} chart-like SVGs")
for r in results:
    print(f"\n  {r['file']} (SVG #{r['svg_index']}, line {r['start_line']})")
    print(f"    Caption: {r['caption'][:120]}")
    print(f"    Labels: {r['labels'][:8]}")
    print(f"    Stats: {r['char_count']} chars, {r['rect_count']} rects, {r['path_count']} paths, polyline={r['has_polyline']}")

with open(ROOT / 'scripts/svg_to_matplotlib/chart_svgs.json', 'w') as f:
    json.dump(results, f, indent=2)
