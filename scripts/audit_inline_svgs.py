"""Audit all inline SVG diagrams in HTML section files."""

import glob
import os
import re
import sys
from collections import Counter, defaultdict
from html import unescape


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATTERNS = [
    os.path.join(ROOT, "part-*", "module-*", "section-*.html"),
    os.path.join(ROOT, "appendices", "appendix-*", "section-*.html"),
]


def find_html_files():
    files = []
    for pat in PATTERNS:
        files.extend(sorted(glob.glob(pat)))
    return files


def extract_inline_svgs(html):
    """Return list of (start_index, svg_string) for inline <svg elements."""
    results = []
    # Find all <svg occurrences not preceded by <img (i.e. truly inline)
    for m in re.finditer(r"<svg[\s>]", html, re.IGNORECASE):
        start = m.start()
        # Check this is not inside an <img tag src attribute
        preceding = html[max(0, start - 200):start]
        if re.search(r'<img[^>]*$', preceding, re.IGNORECASE):
            continue
        # Find the matching </svg>
        depth = 0
        i = start
        while i < len(html):
            open_m = re.search(r"<svg[\s>]", html[i:], re.IGNORECASE)
            close_m = re.search(r"</svg>", html[i:], re.IGNORECASE)
            if close_m is None:
                break
            if open_m and open_m.start() < close_m.start():
                depth += 1
                i += open_m.start() + 4
            else:
                if depth <= 1:
                    end = i + close_m.end()
                    results.append((start, html[start:end]))
                    break
                else:
                    depth -= 1
                    i += close_m.end()
        else:
            # Fallback: grab up to first </svg>
            close_m = re.search(r"</svg>", html[start:], re.IGNORECASE)
            if close_m:
                results.append((start, html[start:start + close_m.end()]))
    return results


def get_surrounding_figure(html, svg_start):
    """Look for enclosing <figure> and extract id, caption."""
    # Search backwards for <figure
    search_back = html[max(0, svg_start - 2000):svg_start]
    fig_m = list(re.finditer(r"<figure[^>]*>", search_back, re.IGNORECASE))
    figure_id = ""
    caption = ""
    if fig_m:
        fig_tag = fig_m[-1].group(0)
        id_m = re.search(r'id=["\']([^"\']+)["\']', fig_tag)
        if id_m:
            figure_id = id_m.group(1)
    # Search forward for <figcaption
    search_fwd = html[svg_start:svg_start + 5000]
    cap_m = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", search_fwd, re.IGNORECASE | re.DOTALL)
    if cap_m:
        caption = re.sub(r"<[^>]+>", "", cap_m.group(1)).strip()
        caption = unescape(caption)
        caption = re.sub(r"\s+", " ", caption)
    # Also check backwards for figcaption (caption above SVG)
    if not caption:
        cap_m = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", search_back, re.IGNORECASE | re.DOTALL)
        if cap_m:
            caption = re.sub(r"<[^>]+>", "", cap_m.group(1)).strip()
            caption = unescape(caption)
            caption = re.sub(r"\s+", " ", caption)
    return figure_id, caption


def analyze_svg(svg_str):
    """Classify SVG content and extract key info."""
    # Dimensions
    width = ""
    height = ""
    viewbox = ""
    w_m = re.search(r'\bwidth=["\']([^"\']+)["\']', svg_str[:500])
    h_m = re.search(r'\bheight=["\']([^"\']+)["\']', svg_str[:500])
    vb_m = re.search(r'viewBox=["\']([^"\']+)["\']', svg_str[:500], re.IGNORECASE)
    if w_m:
        width = w_m.group(1)
    if h_m:
        height = h_m.group(1)
    if vb_m:
        viewbox = vb_m.group(1)

    dims = ""
    if width and height:
        dims = f"{width} x {height}"
    if viewbox:
        dims = (dims + ", " if dims else "") + f"viewBox={viewbox}"
    if not dims:
        dims = "(no dimensions)"

    # Element counts
    elements = {}
    for tag in ["text", "rect", "circle", "ellipse", "path", "line", "polygon", "polyline", "g", "use"]:
        count = len(re.findall(rf"<{tag}[\s>/]", svg_str, re.IGNORECASE))
        if count > 0:
            elements[tag] = count

    # Extract text contents (first 5)
    text_contents = []
    for tm in re.finditer(r"<text[^>]*>(.*?)</text>", svg_str, re.IGNORECASE | re.DOTALL):
        txt = re.sub(r"<[^>]+>", "", tm.group(1)).strip()
        txt = unescape(txt)
        txt = re.sub(r"\s+", " ", txt)
        if txt and len(txt) < 200:
            text_contents.append(txt)
        if len(text_contents) >= 5:
            break

    # Also grab tspan text if no text found
    if not text_contents:
        for tm in re.finditer(r"<tspan[^>]*>(.*?)</tspan>", svg_str, re.IGNORECASE | re.DOTALL):
            txt = re.sub(r"<[^>]+>", "", tm.group(1)).strip()
            txt = unescape(txt)
            txt = re.sub(r"\s+", " ", txt)
            if txt and len(txt) < 200:
                text_contents.append(txt)
            if len(text_contents) >= 5:
                break

    return dims, elements, text_contents


def chapter_key(filepath):
    """Extract chapter/appendix identifier from path."""
    rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
    # e.g. part-1-foundations/module-04-transformer-architecture/section-4.1.html
    parts = rel.split("/")
    if "appendices" in rel:
        # appendices/appendix-l-langchain/section-l.1.html
        if len(parts) >= 2:
            return parts[1]  # appendix-l-langchain
        return parts[0]
    else:
        if len(parts) >= 2:
            return parts[1]  # module-04-transformer-architecture
        return parts[0]


def main():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    output_lines = []

    def emit(line=""):
        output_lines.append(line)
        print(line)

    html_files = find_html_files()
    emit(f"Scanning {len(html_files)} HTML files for inline SVGs...")
    emit("=" * 80)

    # Collect all SVG records grouped by chapter
    by_chapter = defaultdict(list)
    total_svgs = 0

    for fpath in html_files:
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()

        svgs = extract_inline_svgs(html)
        if not svgs:
            continue

        rel_path = os.path.relpath(fpath, ROOT).replace("\\", "/")
        chap = chapter_key(fpath)

        for svg_start, svg_str in svgs:
            total_svgs += 1
            fig_id, caption = get_surrounding_figure(html, svg_start)
            dims, elements, text_contents = analyze_svg(svg_str)

            record = {
                "file": rel_path,
                "figure_id": fig_id,
                "caption": caption,
                "dims": dims,
                "elements": elements,
                "texts": text_contents,
                "svg_len": len(svg_str),
            }
            by_chapter[chap].append(record)

    # Output grouped by chapter
    emit("")
    emit("INLINE SVG INVENTORY BY CHAPTER")
    emit("=" * 80)

    caption_words = Counter()

    for chap in sorted(by_chapter.keys()):
        records = by_chapter[chap]
        emit("")
        emit(f"  {chap} ({len(records)} SVG(s))")
        emit(f"  {'-' * 70}")

        for rec in records:
            emit(f"    File: {rec['file']}")
            if rec["figure_id"]:
                emit(f"    Figure ID: {rec['figure_id']}")
            if rec["caption"]:
                emit(f"    Caption: {rec['caption'][:120]}")
                # Collect caption words for themes
                words = re.findall(r"[a-zA-Z]{3,}", rec["caption"].lower())
                caption_words.update(words)
            emit(f"    Dimensions: {rec['dims']}")
            emit(f"    SVG size: {rec['svg_len']:,} chars")

            # Element summary
            if rec["elements"]:
                parts = [f"{tag}:{cnt}" for tag, cnt in sorted(rec["elements"].items(), key=lambda x: -x[1])]
                emit(f"    Elements: {', '.join(parts)}")

            # Text labels
            if rec["texts"]:
                labels = rec["texts"][:5]
                emit(f"    Text labels: {labels}")

            emit("")

    # Stats
    emit("=" * 80)
    emit("SUMMARY STATISTICS")
    emit("=" * 80)
    emit(f"Total inline SVGs found: {total_svgs}")
    emit(f"Chapters/appendices with SVGs: {len(by_chapter)}")
    emit("")

    emit("SVGs per chapter:")
    for chap in sorted(by_chapter.keys()):
        emit(f"  {chap}: {len(by_chapter[chap])}")

    emit("")
    emit("Top 30 caption keywords (concept themes):")
    # Filter out common stop words
    stop = {
        "the", "and", "for", "with", "from", "that", "this", "are", "was",
        "how", "its", "can", "each", "into", "has", "between", "over",
        "figure", "fig", "diagram", "shows", "show", "illustrates",
        "through", "across", "where", "while", "using", "used", "which",
        "during", "after", "before", "about", "than", "more", "most",
        "all", "both", "their", "they", "not", "but", "when", "then",
        "also", "will", "been", "have", "does", "being", "other",
    }
    top_words = [(w, c) for w, c in caption_words.most_common(80) if w not in stop][:30]
    for word, count in top_words:
        emit(f"  {word}: {count}")

    # Save report
    report_path = os.path.join(ROOT, "scripts", "audit_inline_svgs_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
