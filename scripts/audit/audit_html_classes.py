#!/usr/bin/env python3
"""
audit_html_classes.py - Comprehensive HTML class audit for the LLM Course textbook.

Scans all section-*.html and index.html files, extracts CSS classes from key elements,
cross-references with book.css, and reports issues including typos, orphaned classes,
dead CSS, and rare/non-standard patterns.
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from difflib import get_close_matches

# ── Configuration ──────────────────────────────────────────────────────────
ROOT = Path(r"E:/Projects/LLMCourse")
CSS_FILE = ROOT / "styles" / "book.css"
REPORT_FILE = ROOT / "scripts" / "audit" / "html_class_audit_report.txt"

# Elements to scan for class attributes
TARGET_ELEMENTS = {
    "div", "section", "nav", "header", "main", "footer",
    "details", "summary", "figure", "blockquote", "aside", "article",
}

# Threshold for "standard" vs "rare"
STANDARD_THRESHOLD = 10  # used in 10+ files
RARE_MAX = 3             # used in 1-3 files


# ── Step 1: Find all HTML files ───────────────────────────────────────────
def find_html_files(root: Path) -> list[Path]:
    """Find all section-*.html and index.html, excluding _archive dirs."""
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip _archive directories
        dirnames[:] = [d for d in dirnames if d != "_archive" and not d.startswith(".")]
        dp = Path(dirpath)
        for fn in filenames:
            if fn.startswith("section-") and fn.endswith(".html"):
                results.append(dp / fn)
            elif fn == "index.html":
                results.append(dp / fn)
    return sorted(results)


# ── Step 2: Extract classes from HTML ─────────────────────────────────────
# Regex: match opening tags for target elements and capture class attribute
TAG_RE = re.compile(
    r'<(' + '|'.join(TARGET_ELEMENTS) + r')\b([^>]*?)(/?)>',
    re.IGNORECASE | re.DOTALL
)
CLASS_ATTR_RE = re.compile(r'''class\s*=\s*["']([^"']*)["']''', re.IGNORECASE)
BAD_CLASS_RE = re.compile(r'[^a-zA-Z0-9_ \-]')  # unexpected chars in class value


def extract_classes_from_file(filepath: Path):
    """
    Returns:
      - class_entries: list of (line_num, tag, class_list_str, classes_set)
      - classless_entries: list of (line_num, tag) for elements with no class
      - bad_class_entries: list of (line_num, tag, class_str, bad_chars)
    """
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    class_entries = []
    classless_entries = []
    bad_class_entries = []

    # Build a char-offset-to-line-number map
    line_starts = []
    offset = 0
    for line in lines:
        line_starts.append(offset)
        offset += len(line) + 1  # +1 for newline

    def offset_to_line(pos):
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1  # 1-indexed

    for m in TAG_RE.finditer(text):
        tag = m.group(1).lower()
        attrs = m.group(2)
        line_num = offset_to_line(m.start())

        cm = CLASS_ATTR_RE.search(attrs)
        if cm:
            class_str = cm.group(1).strip()
            if class_str:
                classes = set(class_str.split())
                class_entries.append((line_num, tag, class_str, classes))

                # Check for unexpected characters
                bad = BAD_CLASS_RE.findall(class_str)
                if bad:
                    bad_class_entries.append((line_num, tag, class_str, bad))
            else:
                # Empty class attribute
                classless_entries.append((line_num, tag))
        else:
            classless_entries.append((line_num, tag))

    return class_entries, classless_entries, bad_class_entries


# ── Step 3: Extract CSS class selectors from book.css ─────────────────────
CSS_CLASS_RE = re.compile(r'\.([a-zA-Z_-][a-zA-Z0-9_-]*)')

def extract_css_classes(css_path: Path) -> set[str]:
    """Extract all class names referenced in CSS selectors."""
    text = css_path.read_text(encoding="utf-8", errors="replace")
    # Remove comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    classes = set()
    for m in CSS_CLASS_RE.finditer(text):
        classes.add(m.group(1))
    return classes


# ── Step 4: Known typo patterns ──────────────────────────────────────────
KNOWN_STANDARD_CLASSES = [
    "callout", "big-picture", "analogy", "warning", "tip", "fun-note",
    "diagram", "illustration", "self-check", "chapter-header", "content",
    "chapter-nav", "epigraph", "bibliography", "code-block", "exercise",
    "key-concept", "technical-note", "real-world", "historical-note",
    "definition", "example", "deep-dive", "research-frontier",
    "nav-prev", "nav-next", "nav-up", "section-card", "toc-link",
]


def find_typo_suspects(all_classes: set[str], standard_classes: set[str]) -> list[tuple[str, str]]:
    """Find classes that look like typos of standard ones."""
    suspects = []
    for cls in all_classes:
        if cls in standard_classes:
            continue
        # Check against known standard patterns
        matches = get_close_matches(cls, KNOWN_STANDARD_CLASSES, n=1, cutoff=0.75)
        if matches and matches[0] != cls:
            suspects.append((cls, matches[0]))
        # Also check against actual standard classes
        matches2 = get_close_matches(cls, standard_classes, n=1, cutoff=0.8)
        if matches2 and matches2[0] != cls and (cls, matches2[0]) not in suspects:
            suspects.append((cls, matches2[0]))
    return suspects


# ── Step 5: Main audit ───────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("HTML CLASS AUDIT - LLM Course Textbook")
    print("=" * 70)
    print()

    # Find files
    html_files = find_html_files(ROOT)
    print(f"Found {len(html_files)} HTML files to scan.")

    # Extract CSS classes
    css_classes = extract_css_classes(CSS_FILE)
    print(f"Found {len(css_classes)} CSS class selectors in book.css.")
    print()

    # Scan all HTML files
    # class_name -> { "count": int, "files": set, "locations": [(file, line)] }
    class_data = defaultdict(lambda: {"count": 0, "files": set(), "locations": []})
    all_classless = []       # (file, line, tag)
    all_bad_classes = []     # (file, line, tag, class_str, bad_chars)
    file_count = 0

    for fp in html_files:
        file_count += 1
        rel = fp.relative_to(ROOT)
        class_entries, classless, bad_classes = extract_classes_from_file(fp)

        for line_num, tag, class_str, classes in class_entries:
            for cls in classes:
                class_data[cls]["count"] += 1
                class_data[cls]["files"].add(str(rel))
                # Keep at most 5 locations per class for the report
                if len(class_data[cls]["locations"]) < 5:
                    class_data[cls]["locations"].append((str(rel), line_num))

        for line_num, tag in classless:
            all_classless.append((str(rel), line_num, tag))

        for line_num, tag, class_str, bad in bad_classes:
            all_bad_classes.append((str(rel), line_num, tag, class_str, bad))

    # Build sets
    html_classes = set(class_data.keys())
    standard_classes = {c for c, d in class_data.items() if len(d["files"]) >= STANDARD_THRESHOLD}
    rare_classes = {c for c, d in class_data.items() if 1 <= len(d["files"]) <= RARE_MAX}

    # Find typos
    typo_suspects = find_typo_suspects(html_classes, standard_classes)

    # Cross-reference
    orphaned_html = html_classes - css_classes   # in HTML but not in CSS
    dead_css = css_classes - html_classes          # in CSS but not in HTML

    # ── Build report ──────────────────────────────────────────────────────
    lines = []
    lines.append("=" * 80)
    lines.append("HTML CLASS AUDIT REPORT")
    lines.append(f"Scanned: {file_count} HTML files")
    lines.append(f"Unique classes in HTML: {len(html_classes)}")
    lines.append(f"CSS class selectors in book.css: {len(css_classes)}")
    lines.append("=" * 80)

    # ── Section 1: Frequency table ────────────────────────────────────────
    lines.append("")
    lines.append("-" * 80)
    lines.append("1. COMPLETE FREQUENCY TABLE (sorted by occurrence count)")
    lines.append("-" * 80)
    lines.append(f"{'Class Name':<45} {'Count':>6}  {'Files':>5}  In CSS?")
    lines.append("-" * 80)

    sorted_classes = sorted(class_data.items(), key=lambda x: -x[1]["count"])
    for cls, data in sorted_classes:
        in_css = "YES" if cls in css_classes else "NO"
        lines.append(f"{cls:<45} {data['count']:>6}  {len(data['files']):>5}  {in_css}")

    # ── Section 2: Standard classes ───────────────────────────────────────
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"2. STANDARD CLASSES (used in {STANDARD_THRESHOLD}+ files): {len(standard_classes)}")
    lines.append("-" * 80)
    for cls in sorted(standard_classes):
        d = class_data[cls]
        lines.append(f"  {cls:<40} ({d['count']} uses, {len(d['files'])} files)")

    # ── Section 3: Rare classes ───────────────────────────────────────────
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"3. RARE CLASSES (used in 1-{RARE_MAX} files): {len(rare_classes)}")
    lines.append("   These may be typos, one-off experiments, or non-standard patterns.")
    lines.append("-" * 80)
    for cls in sorted(rare_classes):
        d = class_data[cls]
        locs = "; ".join(f"{f}:{ln}" for f, ln in d["locations"][:3])
        lines.append(f"  {cls:<40} ({d['count']} uses, {len(d['files'])} files)")
        lines.append(f"    Locations: {locs}")

    # ── Section 4: Suspected typos ────────────────────────────────────────
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"4. SUSPECTED TYPOS / NEAR-MATCHES: {len(typo_suspects)}")
    lines.append("-" * 80)
    if typo_suspects:
        for suspect, likely in typo_suspects:
            d = class_data[suspect]
            locs = "; ".join(f"{f}:{ln}" for f, ln in d["locations"][:5])
            lines.append(f"  '{suspect}' -> probably meant '{likely}'")
            lines.append(f"    {d['count']} uses in {len(d['files'])} files: {locs}")
    else:
        lines.append("  (none found)")

    # ── Section 5: Orphaned HTML classes (not in CSS) ─────────────────────
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"5. ORPHANED HTML CLASSES (in HTML but NOT defined in CSS): {len(orphaned_html)}")
    lines.append("-" * 80)
    for cls in sorted(orphaned_html):
        d = class_data[cls]
        locs = "; ".join(f"{f}:{ln}" for f, ln in d["locations"][:3])
        lines.append(f"  {cls:<40} ({d['count']} uses, {len(d['files'])} files)")
        lines.append(f"    Locations: {locs}")

    # ── Section 6: Dead CSS (in CSS but not used in HTML) ─────────────────
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"6. DEAD CSS CLASSES (in book.css but never used in scanned HTML): {len(dead_css)}")
    lines.append("   Note: Some may be used in JS, non-scanned HTML, or pseudo-selectors.")
    lines.append("-" * 80)
    for cls in sorted(dead_css):
        lines.append(f"  .{cls}")

    # ── Section 7: Broken class attributes (unexpected characters) ────────
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"7. BROKEN CLASS ATTRIBUTES (unexpected characters): {len(all_bad_classes)}")
    lines.append("-" * 80)
    if all_bad_classes:
        for filepath, line_num, tag, class_str, bad in all_bad_classes:
            lines.append(f"  {filepath}:{line_num}  <{tag} class=\"{class_str}\">  bad chars: {bad}")
    else:
        lines.append("  (none found)")

    # ── Section 8: Classless elements (sample) ────────────────────────────
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"8. ELEMENTS WITHOUT CLASS ATTRIBUTE: {len(all_classless)} total")
    lines.append("   (Showing first 50; many are expected, e.g. <div> wrappers)")
    lines.append("-" * 80)
    # Group by tag
    classless_by_tag = defaultdict(int)
    for _, _, tag in all_classless:
        classless_by_tag[tag] += 1
    lines.append("  Summary by tag:")
    for tag, cnt in sorted(classless_by_tag.items(), key=lambda x: -x[1]):
        lines.append(f"    <{tag}>: {cnt}")
    lines.append("")
    lines.append("  First 50 instances:")
    for filepath, line_num, tag in all_classless[:50]:
        lines.append(f"    {filepath}:{line_num}  <{tag}>")

    # ── Section 9: Quick pattern checks ───────────────────────────────────
    lines.append("")
    lines.append("-" * 80)
    lines.append("9. PATTERN CHECKS")
    lines.append("-" * 80)

    # Check for 'answer' class not inside <details>
    answer_issues = []
    for fp in html_files:
        text = fp.read_text(encoding="utf-8", errors="replace")
        rel = str(fp.relative_to(ROOT))
        # Find <div class="answer"> not preceded by <details> within ~200 chars
        for m in re.finditer(r'<div\s+class="answer"', text):
            # Check if inside <details>
            before = text[max(0, m.start()-300):m.start()]
            if '<details' not in before or '</details>' in before:
                line_starts_local = []
                offset = 0
                for line in text.split("\n"):
                    line_starts_local.append(offset)
                    offset += len(line) + 1
                lo, hi = 0, len(line_starts_local) - 1
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    if line_starts_local[mid] <= m.start():
                        lo = mid
                    else:
                        hi = mid - 1
                answer_issues.append((rel, lo + 1))

    if answer_issues:
        lines.append(f"  'answer' divs possibly NOT inside <details>: {len(answer_issues)}")
        for fp, ln in answer_issues[:20]:
            lines.append(f"    {fp}:{ln}")
    else:
        lines.append("  'answer' divs: all appear properly wrapped in <details> (or none found)")

    # Check for non-standard quiz/self-check patterns
    quiz_variants = [c for c in html_classes if "quiz" in c.lower() or "self-check" in c.lower() or "selfcheck" in c.lower()]
    if quiz_variants:
        lines.append(f"  Quiz/self-check class variants found: {quiz_variants}")
    else:
        lines.append("  No quiz/self-check class variants found.")

    # ── Summary ───────────────────────────────────────────────────────────
    lines.append("")
    lines.append("=" * 80)
    lines.append("SUMMARY")
    lines.append("=" * 80)
    lines.append(f"  Total HTML files scanned:         {file_count}")
    lines.append(f"  Unique HTML classes found:         {len(html_classes)}")
    lines.append(f"  Standard classes (10+ files):      {len(standard_classes)}")
    lines.append(f"  Rare classes (1-3 files):          {len(rare_classes)}")
    lines.append(f"  Suspected typos:                   {len(typo_suspects)}")
    lines.append(f"  Orphaned HTML (not in CSS):        {len(orphaned_html)}")
    lines.append(f"  Dead CSS (not in HTML):            {len(dead_css)}")
    lines.append(f"  Broken class attributes:           {len(all_bad_classes)}")
    lines.append(f"  Classless elements:                {len(all_classless)}")

    # Write report
    report_text = "\n".join(lines)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report_text, encoding="utf-8")
    print(f"Full report saved to: {REPORT_FILE}")
    print()

    # Print summary to console
    # Print sections 2-7 summary and full section 4 (typos)
    print("-" * 70)
    print("CONSOLE SUMMARY")
    print("-" * 70)
    print(f"  Total files scanned:    {file_count}")
    print(f"  Unique HTML classes:    {len(html_classes)}")
    print(f"  Standard (10+ files):   {len(standard_classes)}")
    print(f"  Rare (1-3 files):       {len(rare_classes)}")
    print(f"  Suspected typos:        {len(typo_suspects)}")
    print(f"  Orphaned (no CSS):      {len(orphaned_html)}")
    print(f"  Dead CSS (no HTML):     {len(dead_css)}")
    print(f"  Broken attributes:      {len(all_bad_classes)}")
    print()

    if typo_suspects:
        print("SUSPECTED TYPOS:")
        for suspect, likely in typo_suspects:
            d = class_data[suspect]
            print(f"  '{suspect}' -> '{likely}'  ({d['count']} uses, {len(d['files'])} files)")
        print()

    if rare_classes:
        print(f"RARE CLASSES ({len(rare_classes)}):")
        for cls in sorted(rare_classes):
            d = class_data[cls]
            locs = "; ".join(f"{f}:{ln}" for f, ln in d["locations"][:2])
            print(f"  {cls:<35} ({d['count']}x, {len(d['files'])}f) {locs}")
        print()

    if orphaned_html:
        print(f"ORPHANED HTML CLASSES ({len(orphaned_html)}):")
        for cls in sorted(orphaned_html):
            d = class_data[cls]
            print(f"  {cls:<35} ({d['count']}x, {len(d['files'])}f)")
        print()

    if dead_css:
        print(f"DEAD CSS CLASSES ({len(dead_css)}):")
        for cls in sorted(dead_css):
            print(f"  .{cls}")
        print()

    print(f"Full report: {REPORT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
