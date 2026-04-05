"""Audit structural/formatting issues in Part 9 section files."""
import re
import os
import json
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")
PART9 = ROOT / "part-9-safety-strategy"

results = {}

for html_file in sorted(PART9.rglob("section-*.html")):
    rel = str(html_file.relative_to(ROOT))
    content = html_file.read_text(encoding="utf-8")
    issues = []

    # 1. Check for inline style= on class-based elements
    for elem_class in ["whats-next", "epigraph", "prerequisites", "callout", "bibliography", "code-caption", "lab", "diagram-container"]:
        pattern = rf'class="[^"]*{elem_class}[^"]*"[^>]*style='
        matches = re.findall(pattern, content)
        if matches:
            issues.append(f"INLINE_STYLE: {len(matches)} inline style(s) on .{elem_class} elements")

    # 2. Check for em dashes
    em_dash_count = content.count("\u2014")
    double_dash_matches = re.findall(r'(?<!-)--(?!-)', content)
    if em_dash_count:
        issues.append(f"EM_DASH: {em_dash_count} em dashes found")
    if double_dash_matches:
        issues.append(f"DOUBLE_DASH: {len(double_dash_matches)} double dashes found")

    # 3. Check for epigraph presence
    has_epigraph = "class=\"epigraph\"" in content
    epigraph_count = content.count("class=\"epigraph\"")
    if not has_epigraph:
        issues.append("MISSING_EPIGRAPH: No epigraph found")
    elif epigraph_count > 1:
        issues.append(f"DUPLICATE_EPIGRAPH: {epigraph_count} epigraphs found")

    # 4. Check epigraph is blockquote (not div)
    div_epigraph = re.findall(r'<div[^>]*class="epigraph"', content)
    if div_epigraph:
        issues.append("EPIGRAPH_DIV: Epigraph uses <div> instead of <blockquote>")

    # 5. Check epigraph attribution format
    cite_matches = re.findall(r'<cite>(.*?)</cite>', content)
    for cite in cite_matches:
        cite_text = re.sub(r'<[^>]+>', '', cite).strip()
        if not re.search(r'A\s+[A-Z]', cite_text):
            issues.append(f"EPIGRAPH_ATTRIBUTION: '{cite_text}' doesn't follow 'A [Adjective] AI ...' pattern")

    # 6. Check for bibliography
    has_bib = "class=\"bibliography\"" in content
    if not has_bib:
        issues.append("MISSING_BIBLIOGRAPHY: No bibliography section found")

    # 7. Check bib-ref uses <p> not <div>
    div_bib_ref = re.findall(r'<div class="bib-ref"', content)
    if div_bib_ref:
        issues.append(f"BIB_REF_DIV: {len(div_bib_ref)} bib-ref entries use <div> instead of <p>")

    # 8. Check for prerequisites
    has_prereq = "class=\"prerequisites\"" in content
    if not has_prereq:
        issues.append("MISSING_PREREQUISITES: No prerequisites box found")

    # 9. Check for research-frontier callout
    has_rf = "research-frontier" in content
    if not has_rf:
        issues.append("MISSING_RESEARCH_FRONTIER: No research-frontier callout found")

    # 10. Check for whats-next
    has_wn = "whats-next" in content
    if not has_wn:
        issues.append("MISSING_WHATS_NEXT: No what's-next section found")

    # 11. Check link to book.css
    has_bookcss = "book.css" in content
    if not has_bookcss:
        issues.append("MISSING_BOOK_CSS: No link to book.css found")

    # 12. Check for non-canonical callout classes
    callout_classes = re.findall(r'class="callout\s+([^"]+)"', content)
    canonical = {"big-picture", "key-insight", "note", "warning", "practical-example",
                 "fun-note", "research-frontier", "algorithm", "tip", "exercise",
                 "key-takeaway", "library-shortcut", "pathway", "self-check", "lab"}
    for cc in callout_classes:
        for cls in cc.split():
            if cls not in canonical and cls != "callout":
                issues.append(f"NON_CANONICAL_CALLOUT: '{cls}' is not a canonical callout type")

    # 13. Check figures have figcaption
    figures = re.findall(r'<figure[^>]*>(.*?)</figure>', content, re.DOTALL)
    for i, fig in enumerate(figures):
        if '<figcaption' not in fig:
            issues.append(f"MISSING_FIGCAPTION: Figure {i+1} has no <figcaption>")

    # 14. Check images have alt text
    imgs = re.findall(r'<img\s[^>]*>', content)
    for img in imgs:
        if 'alt=""' in img or 'alt' not in img:
            issues.append(f"MISSING_ALT: Image without alt text")

    # 15. Check for <style> blocks with potential overrides
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    has_style = len(style_blocks) > 0

    # 16. Check element ordering (epigraph before prereqs before content before RF before WN before bib)
    positions = {}
    for tag, pat in [
        ("epigraph", r'class="epigraph"'),
        ("prerequisites", r'class="prerequisites"'),
        ("research-frontier", r'class="callout research-frontier"'),
        ("whats-next", r'class="whats-next"'),
        ("bibliography", r'class="bibliography"'),
    ]:
        m = re.search(pat, content)
        if m:
            positions[tag] = m.start()

    order_keys = ["epigraph", "prerequisites", "research-frontier", "whats-next", "bibliography"]
    present = [(k, positions[k]) for k in order_keys if k in positions]
    for i in range(len(present) - 1):
        if present[i][1] > present[i+1][1]:
            issues.append(f"ELEMENT_ORDER: {present[i][0]} appears after {present[i+1][0]}")

    # 17. Check for code captions above code blocks (should be below)
    # Look for .code-caption immediately before <pre>
    caption_before_code = re.findall(r'class="code-caption"[^>]*>.*?</\w+>\s*<pre', content, re.DOTALL)
    if caption_before_code:
        issues.append(f"CODE_CAPTION_ABOVE: {len(caption_before_code)} code caption(s) appear above code blocks")

    results[rel] = issues

# Print summary
for f, issues in sorted(results.items()):
    if issues:
        print(f"\n=== {f} ===")
        for issue in issues:
            print(f"  - {issue}")

# Print count summary
total = sum(len(v) for v in results.values())
files_with_issues = sum(1 for v in results.values() if v)
print(f"\n\nSUMMARY: {total} issues across {files_with_issues}/{len(results)} files")
