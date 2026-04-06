"""Audit all appendix HTML files for structural/formatting issues."""
import os
import re
import json
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse\appendices")

issues = {}

def check_file(fpath):
    rel = str(fpath.relative_to(BASE.parent))
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    file_issues = []

    # 1. Check for book.css link
    # Appendix files should link to ../../styles/book.css
    if 'styles/book.css' not in content:
        file_issues.append("MISSING_BOOK_CSS: No link to styles/book.css")

    # 2. Check for <style> blocks (inline CSS)
    style_blocks = re.findall(r'<style[^>]*>.*?</style>', content, re.DOTALL)
    if style_blocks:
        file_issues.append(f"HAS_STYLE_BLOCK: {len(style_blocks)} inline <style> block(s)")

    # 3. Check for em dashes
    em_dash_count = content.count('\u2014')  # —
    if em_dash_count:
        # Find line numbers
        lines_with_em = []
        for i, line in enumerate(content.split('\n'), 1):
            if '\u2014' in line:
                lines_with_em.append(i)
        file_issues.append(f"EM_DASH: {em_dash_count} em dash(es) on lines {lines_with_em[:10]}")

    # 4. Check for double dashes (--) in prose, not in HTML comments or code
    # Simple heuristic: find -- outside of <pre>, <!-- -->, and attributes
    dd_matches = []
    in_pre = False
    for i, line in enumerate(content.split('\n'), 1):
        stripped = line.strip()
        if '<pre' in stripped.lower():
            in_pre = True
        if '</pre>' in stripped.lower():
            in_pre = False
            continue
        if in_pre:
            continue
        if '<!--' in stripped:
            continue
        # Check for -- that's not in an HTML comment or code
        if '--' in stripped and '<!--' not in stripped and '-->' not in stripped:
            # Skip if it's in an attribute or tag
            # Simple: check if -- is in visible text
            text_only = re.sub(r'<[^>]+>', '', stripped)
            if '--' in text_only:
                dd_matches.append(i)
    if dd_matches:
        file_issues.append(f"DOUBLE_DASH: Lines with '--' in prose: {dd_matches[:10]}")

    # 5. Check inline style= on structural elements
    inline_style_pattern = re.findall(r'class="[^"]*(?:callout|whats-next|bibliography|code-caption|epigraph|prerequisites|lab|diagram-container)[^"]*"[^>]*style=', content)
    inline_style_pattern2 = re.findall(r'style="[^"]*"[^>]*class="[^"]*(?:callout|whats-next|bibliography|code-caption|epigraph|prerequisites|lab|diagram-container)', content)
    total_inline = len(inline_style_pattern) + len(inline_style_pattern2)
    if total_inline:
        file_issues.append(f"INLINE_STYLE: {total_inline} structural element(s) with inline style=")

    # 6. Check code captions above code blocks
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'code-caption' in line:
            # Check next 5 lines for <pre
            for j in range(i+1, min(i+6, len(lines))):
                if '<pre' in lines[j]:
                    file_issues.append(f"CAPTION_ABOVE_CODE: code-caption on line {i+1} appears BEFORE <pre on line {j+1}")
                    break

    # 7. Check for <p class="code-caption"> (should be <div>)
    p_captions = re.findall(r'<p\s+class="code-caption"', content)
    if p_captions:
        file_issues.append(f"P_CODE_CAPTION: {len(p_captions)} code-caption(s) using <p> instead of <div>")

    # 8. Check for <div class="bib-ref"> (should be <p>)
    div_bib_ref = re.findall(r'<div\s+class="bib-ref"', content)
    if div_bib_ref:
        file_issues.append(f"DIV_BIB_REF: {len(div_bib_ref)} bib-ref(s) using <div> instead of <p>")

    # 9. Check for non-canonical callout classes
    callout_classes = re.findall(r'class="callout\s+([^"]+)"', content)
    canonical = {'big-picture', 'key-insight', 'note', 'warning', 'practical-example',
                 'fun-note', 'research-frontier', 'algorithm', 'tip', 'exercise',
                 'key-takeaway', 'library-shortcut', 'pathway', 'self-check', 'lab'}
    for cls in callout_classes:
        if cls.strip() not in canonical:
            file_issues.append(f"NON_CANONICAL_CALLOUT: '{cls}'")

    # 10. Check figures for alt text and captions
    img_tags = re.findall(r'<img\s[^>]*>', content)
    for img in img_tags:
        if 'alt=' not in img or 'alt=""' in img:
            file_issues.append(f"IMG_NO_ALT: {img[:80]}...")

    if file_issues:
        issues[rel] = file_issues

# Collect all files
all_files = []
for appendix_dir in sorted(BASE.iterdir()):
    if not appendix_dir.is_dir():
        continue
    idx = appendix_dir / "index.html"
    if idx.exists():
        all_files.append(idx)
    for sf in sorted(appendix_dir.glob("section-*.html")):
        all_files.append(sf)

print(f"Scanning {len(all_files)} files...")

for f in all_files:
    check_file(f)

# Print summary
print(f"\n{'='*60}")
print(f"FILES WITH ISSUES: {len(issues)} / {len(all_files)}")
print(f"{'='*60}\n")

# Count by issue type
type_counts = {}
for fpath, file_issues in sorted(issues.items()):
    for issue in file_issues:
        itype = issue.split(':')[0]
        type_counts[itype] = type_counts.get(itype, 0) + 1

print("ISSUE TYPE SUMMARY:")
for itype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {itype}: {count} files")

print(f"\n{'='*60}")
print("DETAILS BY FILE:")
print(f"{'='*60}\n")

for fpath, file_issues in sorted(issues.items()):
    print(f"\n{fpath}:")
    for issue in file_issues:
        print(f"  - {issue}")

# Save to JSON for programmatic use
with open(BASE.parent / "scripts" / "detect" / "appendix_audit_results.json", "w") as f:
    json.dump(issues, f, indent=2)
