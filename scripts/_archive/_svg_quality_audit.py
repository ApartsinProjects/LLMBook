"""
SVG Quality Audit Script
Scans all section-*.html files for inline SVG diagrams and scores their visual quality.
"""

import os
import re
import glob

BASE_DIR = r"E:\Projects\LLMCourse"

def find_section_files():
    """Find all section-*.html files recursively."""
    results = []
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.startswith("section-") and f.endswith(".html"):
                results.append(os.path.join(root, f))
    results.sort()
    return results

def extract_svgs(html_content):
    """Extract all <svg>...</svg> blocks from HTML content."""
    # Use non-greedy matching, handling nested tags via finding matching close
    svgs = []
    start = 0
    while True:
        idx = html_content.find("<svg", start)
        if idx == -1:
            break
        # Find the matching </svg>
        depth = 0
        pos = idx
        while pos < len(html_content):
            open_match = html_content.find("<svg", pos + 1)
            close_match = html_content.find("</svg>", pos + 1)
            if close_match == -1:
                break
            if open_match != -1 and open_match < close_match:
                depth += 1
                pos = open_match
            else:
                if depth == 0:
                    end = close_match + len("</svg>")
                    svgs.append(html_content[idx:end])
                    start = end
                    break
                else:
                    depth -= 1
                    pos = close_match
        else:
            break
        if close_match == -1:
            break
    return svgs

def get_figure_context(html_content, svg_text):
    """Try to find the figure caption/number near an SVG."""
    idx = html_content.find(svg_text[:80])
    if idx == -1:
        return "Unknown"

    # Look for <figcaption> after the SVG
    region_after = html_content[idx:idx + len(svg_text) + 500]
    cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", region_after, re.DOTALL)
    if cap:
        caption_text = re.sub(r"<[^>]+>", "", cap.group(1)).strip()
        return caption_text[:100]

    # Look for <figure> wrapping with caption before
    region_before = html_content[max(0, idx - 500):idx]
    cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", region_before, re.DOTALL)
    if cap:
        caption_text = re.sub(r"<[^>]+>", "", cap.group(1)).strip()
        return caption_text[:100]

    # Look for a heading before
    h_match = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", region_before, re.DOTALL)
    if h_match:
        heading = re.sub(r"<[^>]+>", "", h_match[-1]).strip()
        return f"(near: {heading[:80]})"

    return "No caption found"

def analyze_svg(svg_text):
    """Analyze an SVG block and return quality metrics and issues."""
    issues = []
    score = 0

    # 1. Check for <defs> with gradients
    has_defs = bool(re.search(r"<defs", svg_text, re.IGNORECASE))
    has_linear_gradient = bool(re.search(r"<linearGradient", svg_text, re.IGNORECASE))
    has_radial_gradient = bool(re.search(r"<radialGradient", svg_text, re.IGNORECASE))
    has_any_gradient = has_linear_gradient or has_radial_gradient

    if has_any_gradient:
        score += 2
    else:
        issues.append("No gradients (flat fills only)")

    # 2. Check for filter elements (shadows, blur, etc.)
    has_filter = bool(re.search(r"<filter", svg_text, re.IGNORECASE))
    if has_filter:
        score += 1
    else:
        issues.append("No filters/shadows")

    # 3. Check minimum font-size
    font_sizes = re.findall(r'font-size[=:]\s*["\']?(\d+(?:\.\d+)?)', svg_text)
    font_sizes_num = [float(f) for f in font_sizes] if font_sizes else []
    min_font = min(font_sizes_num) if font_sizes_num else None

    if min_font is not None and min_font < 10:
        issues.append(f"Tiny text: font-size={min_font}")
    elif min_font is not None and min_font >= 10:
        score += 1
    elif min_font is None:
        # No text in SVG, not necessarily bad
        score += 1

    # 4. Check viewBox dimensions
    vb_match = re.search(r'viewBox\s*=\s*["\']([^"\']+)["\']', svg_text)
    vb_width, vb_height = None, None
    if vb_match:
        parts = vb_match.group(1).split()
        if len(parts) == 4:
            try:
                vb_width = float(parts[2])
                vb_height = float(parts[3])
            except ValueError:
                pass

    if vb_width is not None and vb_height is not None:
        if vb_width < 400 or vb_height < 150:
            issues.append(f"Small viewBox: {vb_width}x{vb_height}")
        else:
            score += 1
    else:
        # No viewBox at all
        issues.append("No viewBox attribute found")

    # 5. Check for black strokes
    has_black_stroke = bool(re.search(r'stroke\s*[=:]\s*["\']?\s*#000(?:000)?(?:["\'\s;])', svg_text, re.IGNORECASE))
    has_black_word = bool(re.search(r'stroke\s*[=:]\s*["\']?\s*black(?:["\'\s;])', svg_text, re.IGNORECASE))

    if has_black_stroke or has_black_word:
        issues.append("Black borders (stroke=#000 or black)")
    else:
        score += 1

    # 6. Bonus: check for rounded corners (rx attribute), opacity usage
    has_rounded = bool(re.search(r'\brx\s*=', svg_text))
    if has_rounded:
        score += 1

    viewbox_str = f"{vb_width}x{vb_height}" if vb_width else "N/A"

    return {
        "score": score,
        "issues": issues,
        "viewbox": viewbox_str,
        "has_gradients": has_any_gradient,
        "has_filters": has_filter,
        "min_font_size": min_font,
        "has_black_strokes": has_black_stroke or has_black_word,
    }

def main():
    section_files = find_section_files()
    print(f"Found {len(section_files)} section HTML files\n")

    all_results = []

    for filepath in section_files:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        svgs = extract_svgs(content)
        if not svgs:
            continue

        rel_path = os.path.relpath(filepath, BASE_DIR)

        for i, svg in enumerate(svgs):
            analysis = analyze_svg(svg)
            caption = get_figure_context(content, svg)

            all_results.append({
                "file": rel_path,
                "svg_index": i + 1,
                "svg_count": len(svgs),
                "caption": caption,
                "analysis": analysis,
                "svg_length": len(svg),
            })

    # Sort by score ascending (worst first)
    all_results.sort(key=lambda x: (x["analysis"]["score"], x["file"], x["svg_index"]))

    # Print report
    print("=" * 120)
    print("SVG QUALITY AUDIT REPORT")
    print("=" * 120)

    # Summary counts
    needs_rebuild = sum(1 for r in all_results if r["analysis"]["score"] <= 2)
    needs_polish = sum(1 for r in all_results if 3 <= r["analysis"]["score"] <= 4)
    acceptable = sum(1 for r in all_results if r["analysis"]["score"] >= 5)

    print(f"\nTotal SVGs found: {len(all_results)}")
    print(f"  Needs rebuild (score 0-2): {needs_rebuild}")
    print(f"  Needs polish  (score 3-4): {needs_polish}")
    print(f"  Acceptable    (score 5+):  {acceptable}")
    print()

    # Category headers
    categories = [
        (0, 2, "NEEDS REBUILD"),
        (3, 4, "NEEDS POLISH"),
        (5, 99, "ACCEPTABLE"),
    ]

    for lo, hi, label in categories:
        subset = [r for r in all_results if lo <= r["analysis"]["score"] <= hi]
        if not subset:
            continue

        print(f"\n{'=' * 120}")
        print(f"  {label} (score {lo}-{hi}): {len(subset)} SVGs")
        print(f"{'=' * 120}")

        for r in subset:
            a = r["analysis"]
            print(f"\n  File:     {r['file']}  (SVG #{r['svg_index']} of {r['svg_count']})")
            print(f"  Caption:  {r['caption']}")
            print(f"  Score:    {a['score']}/7  |  viewBox: {a['viewbox']}  |  SVG size: {r['svg_length']} chars")
            print(f"  Issues:   {'; '.join(a['issues']) if a['issues'] else 'None'}")

    # Also output a compact CSV-style summary for easy processing
    print(f"\n\n{'=' * 120}")
    print("COMPACT SUMMARY (sorted worst first)")
    print(f"{'=' * 120}")
    print(f"{'Score':<6} {'ViewBox':<16} {'File':<75} {'Issues'}")
    print("-" * 120)
    for r in all_results:
        a = r["analysis"]
        fname = f"{r['file']} #{r['svg_index']}"
        issues_str = "; ".join(a["issues"]) if a["issues"] else "OK"
        print(f"{a['score']:<6} {a['viewbox']:<16} {fname:<75} {issues_str}")

if __name__ == "__main__":
    main()
