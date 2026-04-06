"""Fix bibliography structure issues across book HTML files.

Issues addressed:
  1. <div class="bibliography"> should be <section class="bibliography">
     (with matching closing tag).
  2. Orphaned <div class="bibliography-title"> that sits outside any
     bibliography container should be moved inside the next bibliography
     section (or removed if there is no corresponding section).

Usage:
    python scripts/fix/fix_bibliography_structure.py          # dry-run
    python scripts/fix/fix_bibliography_structure.py --fix     # apply changes
"""

import argparse
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
SKIP_DIRS = {"_archive", "node_modules", ".git"}

# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def find_section_files() -> list[Path]:
    """Return all section-*.html files under part-* and appendices/*, skipping
    _archive and similar directories."""
    patterns = [
        "part-*/module-*/section-*.html",
        "appendices/*/section-*.html",
    ]
    files: list[Path] = []
    for pat in patterns:
        for p in BOOK_ROOT.glob(pat):
            # Skip if any ancestor directory is in SKIP_DIRS
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            files.append(p)
    return sorted(files)


# ---------------------------------------------------------------------------
# Fix 1: <div class="bibliography"> -> <section class="bibliography">
# ---------------------------------------------------------------------------

RE_BIB_DIV_OPEN = re.compile(
    r'<div(\s+class="bibliography"(?:\s+id="[^"]*")?)>'
    r'|<div(\s+id="[^"]*"\s+class="bibliography")>'
)

def fix_div_to_section(text: str) -> tuple[str, int]:
    """Replace <div class="bibliography"> with <section class="bibliography">
    and fix the matching closing </div> to </section>.

    Returns (new_text, count_of_replacements).
    """
    count = 0
    result_lines = text.split("\n")

    # We need to find each opening <div class="bibliography"...> and its
    # matching </div>, then convert both.
    # Strategy: work on the full text, find opening tags, track nesting to
    # find the matching close, then replace from the end to preserve offsets.

    # Collect positions of opening tags
    opens = []
    for m in RE_BIB_DIV_OPEN.finditer(text):
        attr = m.group(1) or m.group(2)
        opens.append((m.start(), m.end(), attr))

    if not opens:
        return text, 0

    # Process from last to first so earlier offsets stay valid
    for start, end, attr in reversed(opens):
        # Find matching </div>
        depth = 1
        pos = end
        while depth > 0 and pos < len(text):
            next_open = text.find("<div", pos)
            next_close = text.find("</div>", pos)
            if next_close == -1:
                break  # malformed HTML, give up
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                if depth == 0:
                    # Replace closing tag
                    text = text[:next_close] + "</section>" + text[next_close + 6:]
                else:
                    pos = next_close + 6

        # Replace opening tag
        text = text[:start] + f"<section{attr}>" + text[end:]
        count += 1

    return text, count


# ---------------------------------------------------------------------------
# Fix 2: Orphaned bibliography-title divs
# ---------------------------------------------------------------------------

RE_ORPHAN_TITLE = re.compile(
    r'^(\s*)<div class="bibliography-title">(.*?)</div>\s*$',
    re.MULTILINE,
)

def fix_orphaned_titles(text: str) -> tuple[str, int]:
    """Find <div class="bibliography-title"> lines that are NOT inside a
    <section class="bibliography"> or <div class="bibliography"> and either:
      - move them into the next bibliography section, or
      - remove them if no bibliography section follows.

    Returns (new_text, count_of_fixes).
    """
    count = 0
    lines = text.split("\n")
    removals = []  # line indices to remove

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not re.match(r'<div class="bibliography-title">', stripped):
            continue

        # Check whether this line is inside a bibliography container.
        # Look backwards for the nearest opening bibliography tag that has
        # not been closed yet.
        inside = False
        depth = 0
        for j in range(i - 1, -1, -1):
            prev = lines[j].strip()
            if "</section>" in prev or (re.search(r'</div>', prev) and "bibliography" not in prev):
                # This could close a container above, but we only care about
                # bibliography containers.
                pass
            if '<section class="bibliography"' in prev or '<div class="bibliography"' in prev:
                inside = True
                break
            # If we hit another section or major structural element, stop
            if re.match(r'<(section|article|main|body|html)\b', prev):
                break

        if inside:
            continue  # title is properly inside its container, skip

        # This is an orphaned bibliography-title. Remove it.
        removals.append(i)
        count += 1

    if not removals:
        return text, 0

    new_lines = [line for idx, line in enumerate(lines) if idx not in removals]
    return "\n".join(new_lines), count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_file(path: Path, fix: bool) -> dict:
    """Process one file. Returns a dict of issue counts."""
    text = path.read_text(encoding="utf-8")
    original = text
    issues = {"div_to_section": 0, "orphaned_title": 0}

    text, n = fix_div_to_section(text)
    issues["div_to_section"] = n

    text, n = fix_orphaned_titles(text)
    issues["orphaned_title"] = n

    if text != original:
        if fix:
            path.write_text(text, encoding="utf-8")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Fix bibliography structure issues")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (default is dry-run)")
    args = parser.parse_args()

    files = find_section_files()
    print(f"Scanning {len(files)} section files...\n")

    totals = {"div_to_section": 0, "orphaned_title": 0}
    affected_files = []

    for path in files:
        issues = process_file(path, fix=args.fix)
        if any(v > 0 for v in issues.values()):
            rel = path.relative_to(BOOK_ROOT)
            affected_files.append((rel, issues))
            for k, v in issues.items():
                totals[k] += v

    # Report
    mode = "FIXED" if args.fix else "DRY-RUN (use --fix to apply)"
    print(f"Mode: {mode}\n")

    if not affected_files:
        print("No issues found.")
        return

    print("Issue 1: <div class='bibliography'> -> <section class='bibliography'>")
    div_files = [(f, i) for f, i in affected_files if i["div_to_section"] > 0]
    if div_files:
        for rel, issues in div_files:
            print(f"  {rel}  ({issues['div_to_section']})")
    else:
        print("  (none)")

    print(f"\nIssue 2: Orphaned bibliography-title divs")
    orphan_files = [(f, i) for f, i in affected_files if i["orphaned_title"] > 0]
    if orphan_files:
        for rel, issues in orphan_files:
            print(f"  {rel}  ({issues['orphaned_title']})")
    else:
        print("  (none)")

    print(f"\nTotals:")
    print(f"  div -> section conversions: {totals['div_to_section']}")
    print(f"  orphaned titles removed:    {totals['orphaned_title']}")
    print(f"  files affected:             {len(affected_files)}")


if __name__ == "__main__":
    main()
