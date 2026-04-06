#!/usr/bin/env python3
"""Audit <strong> tag usage inside callout divs across the LLM Course textbook.

Flags:
  - Callouts with 3+ <strong> tags ("heavy bold")
  - Paragraph-level bold: <strong> spans > 50 chars
  - Sentence-level bold: <strong> spans > 80 chars
  - Structural-word bold: common label phrases that could use <em> or nothing
"""

import re
from collections import Counter, defaultdict
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

SCAN_DIRS = [
    BOOK_ROOT / "part-1-foundations",
    BOOK_ROOT / "part-2-understanding-llms",
    BOOK_ROOT / "part-3-working-with-llms",
    BOOK_ROOT / "part-4-training-adapting",
    BOOK_ROOT / "part-5-retrieval-conversation",
    BOOK_ROOT / "part-6-agentic-ai",
    BOOK_ROOT / "part-7-multimodal-applications",
    BOOK_ROOT / "part-8-evaluation-production",
    BOOK_ROOT / "part-9-safety-strategy",
    BOOK_ROOT / "part-10-frontiers",
    BOOK_ROOT / "part-11-idea-to-product",
    BOOK_ROOT / "appendices",
]

CALLOUT_TYPES = [
    "key-insight", "warning", "tip", "note", "practical-example",
    "library-shortcut", "research-frontier", "big-picture", "fun-note",
]

# Structural label phrases that probably don't need bold
STRUCTURAL_LABELS = re.compile(
    r"^(Key (advantage|limitation|insight|difference|takeaway|point|concept|idea|benefit|challenge|question)|"
    r"Why\??|How\??|What\??|When\??|Result:?|Note:?|Example:?|Important:?|"
    r"Tip:?|Warning:?|Caution:?|Summary:?|Bottom line:?|In practice:?|"
    r"Trade-?off:?|Recall:?|Definition:?|Rule of thumb:?):?\s*$",
    re.IGNORECASE,
)

# Regex to find callout divs (greedy but bounded by next closing </div> at same nesting)
# We use a simpler approach: find callout start, then collect until we hit a line that is
# just </div> at the right nesting level.
CALLOUT_START = re.compile(
    r'<div\s+class="callout\s+(' + "|".join(CALLOUT_TYPES) + r')"'
)
STRONG_TAG = re.compile(r"<strong>(.*?)</strong>", re.DOTALL)


def extract_callouts(html: str) -> list[tuple[str, str]]:
    """Return list of (callout_type, callout_html) from an HTML string."""
    results = []
    lines = html.split("\n")
    i = 0
    while i < len(lines):
        m = CALLOUT_START.search(lines[i])
        if m:
            callout_type = m.group(1)
            depth = 0
            callout_lines = []
            for j in range(i, len(lines)):
                line = lines[j]
                # Count div opens and closes
                depth += len(re.findall(r"<div[\s>]", line))
                depth -= len(re.findall(r"</div>", line))
                callout_lines.append(line)
                if depth <= 0:
                    break
            results.append((callout_type, "\n".join(callout_lines)))
            i = j + 1 if depth <= 0 else i + 1
        else:
            i += 1
    return results


def analyze_callout(callout_html: str) -> dict:
    """Analyze a single callout for bold usage issues."""
    strongs = STRONG_TAG.findall(callout_html)
    issues = []

    for content in strongs:
        clean = re.sub(r"<[^>]+>", "", content).strip()
        length = len(clean)

        if length > 80:
            issues.append(("sentence_bold", clean[:100]))
        elif length > 50:
            issues.append(("paragraph_bold", clean[:100]))

        if STRUCTURAL_LABELS.match(clean):
            issues.append(("structural_label", clean))

    return {
        "strong_count": len(strongs),
        "issues": issues,
    }


def collect_html_files() -> list[Path]:
    files = []
    for d in SCAN_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.rglob("*.html")):
            if "_archive" in str(f):
                continue
            files.append(f)
    return files


def main():
    files = collect_html_files()
    print(f"Scanning {len(files)} HTML files...\n")

    # Aggregates
    strong_per_type: Counter = Counter()
    callout_count_per_type: Counter = Counter()
    heavy_bold_files: list[tuple[str, str, int, list]] = []  # (file, type, count, issues)
    paragraph_bold_total = 0
    sentence_bold_total = 0
    structural_label_total = 0
    all_structural_labels: list[tuple[str, str]] = []  # (file, label)
    file_bold_totals: Counter = Counter()  # file -> total strong tags in callouts

    for fpath in files:
        html = fpath.read_text(encoding="utf-8", errors="replace")
        callouts = extract_callouts(html)
        rel = fpath.relative_to(BOOK_ROOT)

        for ctype, chtml in callouts:
            callout_count_per_type[ctype] += 1
            analysis = analyze_callout(chtml)
            strong_per_type[ctype] += analysis["strong_count"]
            file_bold_totals[str(rel)] += analysis["strong_count"]

            for issue_type, text in analysis["issues"]:
                if issue_type == "paragraph_bold":
                    paragraph_bold_total += 1
                elif issue_type == "sentence_bold":
                    sentence_bold_total += 1
                elif issue_type == "structural_label":
                    structural_label_total += 1
                    all_structural_labels.append((str(rel), text))

            if analysis["strong_count"] >= 3:
                heavy_bold_files.append((
                    str(rel), ctype, analysis["strong_count"], analysis["issues"]
                ))

    # === REPORT ===
    print("=" * 75)
    print("BOLD USAGE IN CALLOUTS: SUMMARY")
    print("=" * 75)

    print(f"\n{'Callout Type':<22} {'Callouts':>9} {'<strong> tags':>13} {'Avg/callout':>12}")
    print("-" * 60)
    for ctype in CALLOUT_TYPES:
        count = callout_count_per_type[ctype]
        strongs = strong_per_type[ctype]
        avg = f"{strongs / count:.1f}" if count else "n/a"
        print(f"  {ctype:<20} {count:>9} {strongs:>13} {avg:>12}")
    total_callouts = sum(callout_count_per_type.values())
    total_strongs = sum(strong_per_type.values())
    avg_total = f"{total_strongs / total_callouts:.1f}" if total_callouts else "n/a"
    print("-" * 60)
    print(f"  {'TOTAL':<20} {total_callouts:>9} {total_strongs:>13} {avg_total:>12}")

    print(f"\n{'=' * 75}")
    print("ISSUE COUNTS")
    print("=" * 75)
    print(f"  Heavy-bold callouts (3+ <strong>):  {len(heavy_bold_files)}")
    print(f"  Paragraph-level bold (>50 chars):   {paragraph_bold_total}")
    print(f"  Sentence-level bold (>80 chars):    {sentence_bold_total}")
    print(f"  Structural-label bold:              {structural_label_total}")

    print(f"\n{'=' * 75}")
    print("TOP 20 FILES BY TOTAL <strong> TAGS IN CALLOUTS")
    print("=" * 75)
    for path, count in file_bold_totals.most_common(20):
        print(f"  {count:>4}  {path}")

    print(f"\n{'=' * 75}")
    print(f"HEAVY-BOLD CALLOUTS (3+ <strong>): {len(heavy_bold_files)} total")
    print("=" * 75)
    # Sort by strong count descending
    heavy_bold_files.sort(key=lambda x: -x[2])
    for filepath, ctype, count, issues in heavy_bold_files[:40]:
        print(f"\n  [{count} strongs] {filepath}  ({ctype})")
        for itype, text in issues:
            tag = {"paragraph_bold": "PARA-BOLD", "sentence_bold": "SENT-BOLD",
                   "structural_label": "STRUCT-LBL"}.get(itype, itype)
            print(f"    {tag}: {text[:90]}")

    if all_structural_labels:
        print(f"\n{'=' * 75}")
        print(f"STRUCTURAL LABELS WRAPPED IN <strong>: {structural_label_total} total")
        print("=" * 75)
        for filepath, label in all_structural_labels[:50]:
            print(f"  {filepath}: \"{label}\"")

    print(f"\n{'=' * 75}")
    print("PARAGRAPH-LEVEL BOLD (>50 chars): samples")
    print("=" * 75)
    # Re-scan for samples
    sample_count = 0
    for fpath in files:
        if sample_count >= 30:
            break
        html = fpath.read_text(encoding="utf-8", errors="replace")
        callouts = extract_callouts(html)
        rel = fpath.relative_to(BOOK_ROOT)
        for ctype, chtml in callouts:
            strongs = STRONG_TAG.findall(chtml)
            for content in strongs:
                clean = re.sub(r"<[^>]+>", "", content).strip()
                if len(clean) > 50 and sample_count < 30:
                    print(f"  {str(rel)}")
                    print(f"    [{len(clean)} chars] \"{clean[:120]}...\"" if len(clean) > 120 else f"    [{len(clean)} chars] \"{clean}\"")
                    sample_count += 1


if __name__ == "__main__":
    main()
