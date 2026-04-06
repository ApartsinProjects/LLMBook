"""Comprehensive section numbering consistency check for LLM textbook."""

import os
import re
import glob
from collections import defaultdict
from html.parser import HTMLParser

BASE = r"E:\Projects\LLMCourse"

# ── Collect all section files ──────────────────────────────────────────────
section_files = sorted(glob.glob(os.path.join(BASE, "part-*", "module-*", "section-*.html")))

print(f"Found {len(section_files)} section files.\n")

# ── Helper: extract module number from directory name ──────────────────────
def module_num_from_dir(dirpath):
    m = re.search(r'module-(\d+)', dirpath)
    return int(m.group(1)) if m else None

# ── Helper: expected section number from filename ─────────────────────────
def section_from_filename(filepath):
    m = re.search(r'section-(\d+\.\d+)\.html$', filepath)
    return m.group(1) if m else None

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 1: Filename vs content mismatch
# ═══════════════════════════════════════════════════════════════════════════
print("=" * 80)
print("CHECK 1: Filename vs Content Mismatch")
print("=" * 80)

issues_1 = []

for fpath in section_files:
    expected_sec = section_from_filename(fpath)
    if not expected_sec:
        issues_1.append(f"  Cannot parse section number from filename: {fpath}")
        continue

    expected_major = int(expected_sec.split(".")[0])
    dir_module = module_num_from_dir(os.path.dirname(fpath))

    # Check directory match
    if dir_module is not None and dir_module != expected_major:
        issues_1.append(
            f"  FILE IN WRONG DIRECTORY: {os.path.relpath(fpath, BASE)}\n"
            f"    Section {expected_sec} is in module-{dir_module:02d} directory"
        )

    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Check <title>
    title_match = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    if title_match:
        title_text = title_match.group(1)
        # Title should contain the section number like "Section 4.1:" or "4.1"
        if expected_sec not in title_text:
            issues_1.append(
                f"  TITLE MISMATCH: {os.path.relpath(fpath, BASE)}\n"
                f"    Expected '{expected_sec}' in title, got: {title_text.strip()[:80]}"
            )
    else:
        issues_1.append(f"  NO TITLE: {os.path.relpath(fpath, BASE)}")

    # Check <h1> or <span class="section-number">
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
    span_match = re.search(r'<span\s+class="section-number">(.*?)</span>', content, re.DOTALL)

    # The h1 may or may not contain the number. Check both h1 and span.
    has_number_in_h1 = False
    if h1_match:
        h1_text = re.sub(r"<[^>]+>", "", h1_match.group(1))
        if expected_sec in h1_text:
            has_number_in_h1 = True
    has_number_in_span = False
    if span_match:
        span_text = span_match.group(1).strip()
        if expected_sec in span_text:
            has_number_in_span = True

    # Note: many files use the title pattern "Section X.Y: Title" but h1 may just be the title
    # This is informational, not necessarily an error

if issues_1:
    for i in issues_1:
        print(i)
else:
    print("  No issues found.")

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 2: Cross-reference correctness
# ═══════════════════════════════════════════════════════════════════════════
print()
print("=" * 80)
print("CHECK 2: Cross-reference Link Verification")
print("=" * 80)

issues_2 = []

# Also check index.html files in modules
all_html = section_files + sorted(glob.glob(os.path.join(BASE, "part-*", "module-*", "index.html")))

for fpath in all_html:
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    fdir = os.path.dirname(fpath)
    relpath = os.path.relpath(fpath, BASE)

    # Find all cross-ref links
    for m in re.finditer(r'<a\s+class="cross-ref"\s+href="([^"]+)"[^>]*>(.*?)</a>', content, re.DOTALL):
        href = m.group(1)
        link_text = re.sub(r"<[^>]+>", "", m.group(2)).strip()

        # Resolve href relative to file directory
        if href.startswith("http"):
            continue
        # Strip anchor
        href_path = href.split("#")[0]
        if not href_path:
            continue

        target = os.path.normpath(os.path.join(fdir, href_path))
        if not os.path.exists(target):
            issues_2.append(
                f"  BROKEN CROSS-REF: {relpath}\n"
                f"    href=\"{href}\" -> file not found: {os.path.relpath(target, BASE)}\n"
                f"    Link text: {link_text[:80]}"
            )
        else:
            # Check if link text mentions the correct section number for the target
            target_sec = section_from_filename(target)
            if target_sec and target_sec not in link_text:
                # Sometimes link text says "Chapter X" for module index, that's ok
                target_major = target_sec.split(".")[0]
                if f"Chapter {target_major}" not in link_text and f"Section {target_sec}" not in link_text and target_sec not in link_text:
                    issues_2.append(
                        f"  CROSS-REF TEXT MISMATCH: {relpath}\n"
                        f"    Links to {os.path.relpath(target, BASE)} (section {target_sec})\n"
                        f"    But link text is: {link_text[:80]}"
                    )

if issues_2:
    for i in issues_2:
        print(i)
else:
    print("  No issues found.")

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 3: Chapter-nav consistency
# ═══════════════════════════════════════════════════════════════════════════
print()
print("=" * 80)
print("CHECK 3: Chapter-nav Consistency")
print("=" * 80)

issues_3 = []

# Build ordered list of sections per module
module_sections = defaultdict(list)
for fpath in section_files:
    sec = section_from_filename(fpath)
    if sec:
        major = int(sec.split(".")[0])
        minor = int(sec.split(".")[1])
        module_sections[major].append((minor, sec, fpath))

for major in sorted(module_sections):
    sections = sorted(module_sections[major], key=lambda x: x[0])
    minors = [s[0] for s in sections]

    # Check for gaps
    if minors:
        expected_minors = list(range(minors[0], minors[-1] + 1))
        missing = set(expected_minors) - set(minors)
        if missing:
            issues_3.append(
                f"  SECTION GAP in Chapter {major}: "
                f"has {[f'{major}.{m}' for m in minors]}, "
                f"missing {[f'{major}.{m}' for m in sorted(missing)]}"
            )

    # Check duplicates
    if len(minors) != len(set(minors)):
        issues_3.append(f"  DUPLICATE SECTIONS in Chapter {major}: {minors}")

# Now check prev/next links
for fpath in section_files:
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    relpath = os.path.relpath(fpath, BASE)
    fdir = os.path.dirname(fpath)
    sec = section_from_filename(fpath)
    if not sec:
        continue
    major = int(sec.split(".")[0])
    minor = int(sec.split(".")[1])

    # Find the chapter-nav block
    nav_match = re.search(r'<nav\s+class="chapter-nav">(.*?)</nav>', content, re.DOTALL)
    if not nav_match:
        issues_3.append(f"  NO CHAPTER-NAV: {relpath}")
        continue

    nav_html = nav_match.group(1)

    # Extract prev and next links
    prev_link = re.search(r'<a\s+href="([^"]+)"\s+class="prev"[^>]*>(.*?)</a>', nav_html, re.DOTALL)
    next_link = re.search(r'<a\s+href="([^"]+)"\s+class="next"[^>]*>(.*?)</a>', nav_html, re.DOTALL)

    # Determine expected prev/next within the module
    sections_in_module = sorted(module_sections[major], key=lambda x: x[0])
    idx = None
    for i, (m, s, p) in enumerate(sections_in_module):
        if m == minor:
            idx = i
            break

    if idx is not None:
        # Check prev link
        if idx == 0:
            # First section: prev should be index.html or previous chapter's last section
            if prev_link:
                prev_href = prev_link.group(1).split("#")[0]
                prev_text = re.sub(r"<[^>]+>", "", prev_link.group(2)).strip()
                # It's OK to point to index.html
                # But check it exists
                prev_target = os.path.normpath(os.path.join(fdir, prev_href))
                if not os.path.exists(prev_target):
                    issues_3.append(
                        f"  BROKEN PREV LINK: {relpath}\n"
                        f"    href=\"{prev_href}\" -> file not found"
                    )
        else:
            expected_prev_minor = sections_in_module[idx - 1][0]
            expected_prev_sec = f"{major}.{expected_prev_minor}"
            if prev_link:
                prev_href = prev_link.group(1).split("#")[0]
                prev_text = re.sub(r"<[^>]+>", "", prev_link.group(2)).strip()
                # Check the href points to the right section
                prev_sec_from_href = section_from_filename(prev_href)
                if prev_sec_from_href and prev_sec_from_href != expected_prev_sec:
                    issues_3.append(
                        f"  PREV LINK WRONG TARGET: {relpath}\n"
                        f"    Expected prev to be section {expected_prev_sec}, "
                        f"but href points to section {prev_sec_from_href}"
                    )
                # Check existence
                prev_target = os.path.normpath(os.path.join(fdir, prev_href))
                if not os.path.exists(prev_target):
                    issues_3.append(
                        f"  BROKEN PREV LINK: {relpath}\n"
                        f"    href=\"{prev_href}\" -> file not found"
                    )
            else:
                issues_3.append(
                    f"  MISSING PREV LINK: {relpath}\n"
                    f"    Section {sec} should have prev link to {expected_prev_sec}"
                )

        # Check next link
        if idx == len(sections_in_module) - 1:
            # Last section: next should be next chapter or nothing
            if next_link:
                next_href = next_link.group(1).split("#")[0]
                next_target = os.path.normpath(os.path.join(fdir, next_href))
                if not os.path.exists(next_target):
                    issues_3.append(
                        f"  BROKEN NEXT LINK: {relpath}\n"
                        f"    href=\"{next_href}\" -> file not found"
                    )
        else:
            expected_next_minor = sections_in_module[idx + 1][0]
            expected_next_sec = f"{major}.{expected_next_minor}"
            if next_link:
                next_href = next_link.group(1).split("#")[0]
                next_text = re.sub(r"<[^>]+>", "", next_link.group(2)).strip()
                next_sec_from_href = section_from_filename(next_href)
                if next_sec_from_href and next_sec_from_href != expected_next_sec:
                    issues_3.append(
                        f"  NEXT LINK WRONG TARGET: {relpath}\n"
                        f"    Expected next to be section {expected_next_sec}, "
                        f"but href points to section {next_sec_from_href}"
                    )
                next_target = os.path.normpath(os.path.join(fdir, next_href))
                if not os.path.exists(next_target):
                    issues_3.append(
                        f"  BROKEN NEXT LINK: {relpath}\n"
                        f"    href=\"{next_href}\" -> file not found"
                    )
            else:
                issues_3.append(
                    f"  MISSING NEXT LINK: {relpath}\n"
                    f"    Section {sec} should have next link to {expected_next_sec}"
                )

if issues_3:
    for i in issues_3:
        print(i)
else:
    print("  No issues found.")

# ═══════════════════════════════════════════════════════════════════════════
# CHECK 4: Duplicate callout-title divs
# ═══════════════════════════════════════════════════════════════════════════
print()
print("=" * 80)
print("CHECK 4: Duplicate Consecutive callout-title Divs")
print("=" * 80)

issues_4 = []

all_content_files = section_files + sorted(glob.glob(os.path.join(BASE, "part-*", "module-*", "index.html")))

for fpath in all_content_files:
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    relpath = os.path.relpath(fpath, BASE)

    # Pattern: two callout-title divs in a row (with optional whitespace between)
    pattern = r'(<div\s+class="callout-title"[^>]*>.*?</div>\s*<div\s+class="callout-title"[^>]*>)'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if matches:
        for m in matches:
            # Find line number
            line_num = content[:m.start()].count('\n') + 1
            snippet = m.group(1)[:120].replace('\n', ' ')
            issues_4.append(
                f"  DUPLICATE CALLOUT-TITLE: {relpath} (line ~{line_num})\n"
                f"    Snippet: {snippet}..."
            )

if issues_4:
    for i in issues_4:
        print(i)
else:
    print("  No issues found.")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
total = len(issues_1) + len(issues_2) + len(issues_3) + len(issues_4)
print(f"  Check 1 (Filename vs Content):     {len(issues_1)} issues")
print(f"  Check 2 (Cross-references):        {len(issues_2)} issues")
print(f"  Check 3 (Chapter-nav):             {len(issues_3)} issues")
print(f"  Check 4 (Duplicate callout-title): {len(issues_4)} issues")
print(f"  TOTAL:                             {total} issues")
