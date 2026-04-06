"""
Audit: Find real-world scenario callouts with partial narrative markers.

Scans all .html files under part-*/ and appendices/ for
<div class="callout practical-example"> blocks, checks which narrative
markers are present, and reports any that have some but not all required
markers.

Required markers (minimum): Who, Problem, Result, Lesson
Full set: Who, Situation, Problem, Decision/Dilemma, Result, Lesson
Optional: How, Approach, Scenario
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

REQUIRED_MARKERS = {"Who", "Problem", "Result", "Lesson"}
FULL_MARKERS = {"Who", "Situation", "Problem", "Decision", "Dilemma", "Result", "Lesson"}
OPTIONAL_MARKERS = {"How", "Approach", "Scenario"}
ALL_KNOWN = FULL_MARKERS | OPTIONAL_MARKERS

# Pattern to match marker labels in <strong>Label:</strong> form
MARKER_PATTERN = re.compile(r"<strong>\s*(Who|Situation|Problem|Decision|Dilemma|Result|Lesson|How|Approach|Scenario)\s*(?:/\s*\w+)?\s*:?\s*</strong>", re.IGNORECASE)

# Pattern to find callout practical-example blocks
CALLOUT_PATTERN = re.compile(
    r'<div\s+class="callout\s+practical-example"[^>]*>(.*?)</div>\s*(?:</div>|\Z)',
    re.DOTALL
)

# More robust: find the opening tag and then grab content until the matching close
def find_practical_examples(html_text):
    """Yield (start_pos, block_text) for each practical-example callout."""
    tag = '<div class="callout practical-example">'
    start = 0
    while True:
        idx = html_text.find(tag, start)
        if idx == -1:
            break
        # Find the matching closing div by counting nesting
        depth = 0
        i = idx
        block_start = idx
        while i < len(html_text):
            if html_text[i:i+4] == '<div':
                depth += 1
                i += 4
            elif html_text[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    yield (block_start, html_text[block_start:i+6])
                    start = i + 6
                    break
                i += 6
            else:
                i += 1
        else:
            # Reached end without closing
            yield (block_start, html_text[block_start:])
            break


def get_title(block_text):
    """Extract the title from <h4> or <h3> inside the block."""
    m = re.search(r'<h[34][^>]*>(.*?)</h[34]>', block_text, re.DOTALL)
    if m:
        # Strip HTML tags from title
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        return title
    return "(no title)"


def get_line_number(html_text, pos):
    """Return 1-based line number for character position."""
    return html_text[:pos].count('\n') + 1


def scan_file(filepath):
    """Scan a single HTML file for partial scenario callouts."""
    html_text = filepath.read_text(encoding="utf-8", errors="replace")
    results = []

    for (pos, block) in find_practical_examples(html_text):
        # Find all markers present
        found = set()
        for m in MARKER_PATTERN.finditer(block):
            label = m.group(1).strip().title()
            found.add(label)

        # Normalize: treat Decision and Dilemma as interchangeable for "Decision/Dilemma"
        has_decision_or_dilemma = "Decision" in found or "Dilemma" in found

        # Count how many known markers are present
        if len(found) < 2:
            continue  # Not a partial scenario, either 0-1 markers

        # Check which required markers are missing
        missing_required = set()
        for req in REQUIRED_MARKERS:
            if req not in found:
                missing_required.add(req)

        if not missing_required:
            continue  # All required markers present, nothing to fix

        title = get_title(block)
        line = get_line_number(html_text, pos)
        rel_path = filepath.relative_to(BOOK_ROOT)

        results.append({
            "file": str(rel_path),
            "line": line,
            "title": title,
            "present": sorted(found),
            "missing_required": sorted(missing_required),
        })

    return results


def main():
    # Collect HTML files
    html_files = []
    for pattern in ["part-*/**/*.html", "appendices/**/*.html"]:
        for f in BOOK_ROOT.glob(pattern):
            if "_archive" in str(f):
                continue
            if f.is_file():
                html_files.append(f)

    html_files.sort()
    print(f"Scanning {len(html_files)} HTML files...\n")

    all_results = []
    for f in html_files:
        results = scan_file(f)
        all_results.extend(results)

    if not all_results:
        print("No partial scenarios found.")
        return

    print(f"Found {len(all_results)} partial scenario(s):\n")
    print("=" * 100)

    for i, r in enumerate(all_results, 1):
        print(f"\n[{i}] {r['file']}  (line {r['line']})")
        print(f"    Title:            {r['title']}")
        print(f"    Present markers:  {', '.join(r['present'])}")
        print(f"    Missing required: {', '.join(r['missing_required'])}")

    print("\n" + "=" * 100)
    print(f"\nTotal partial scenarios: {len(all_results)}")

    # Summary by missing marker
    from collections import Counter
    missing_counts = Counter()
    for r in all_results:
        for m in r["missing_required"]:
            missing_counts[m] += 1

    print("\nMissing marker frequency:")
    for marker, count in missing_counts.most_common():
        print(f"  {marker}: {count}")


if __name__ == "__main__":
    main()
