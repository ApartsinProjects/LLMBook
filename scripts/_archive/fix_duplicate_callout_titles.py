"""
Detect and fix duplicate <div class="callout-title"> elements within a single callout div.

Pattern: A callout div contains two consecutive callout-title divs, e.g.:
  <div class="callout practical-example" title="...">
    <div class="callout-title">Practical Example</div>
    <div class="callout-title">Using a Reasoning Model to Automate Tax Regulation Analysis</div>

Fix: Keep the more specific title (longer one, or the one that isn't just the callout type name).
"""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates", "styles"}

# Generic callout type names that should be removed if a more specific title exists
GENERIC_TITLES = {
    "big picture", "big-picture", "the big picture",
    "key insight", "key-insight",
    "note",
    "warning",
    "practical example", "practical-example",
    "fun fact", "fun note", "fun-note",
    "research frontier", "research-frontier",
    "algorithm",
    "tip",
    "exercise",
}

def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)

def detect_and_fix(filepath, dry_run=False):
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    issues = []
    fixed_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue

        # Check if this line and next line are both callout-title divs
        if i + 1 < len(lines):
            match1 = re.match(r'^(\s*)<div class="callout-title">(.*?)</div>\s*$', line)
            match2 = re.match(r'^(\s*)<div class="callout-title">(.*?)</div>\s*$', lines[i + 1])

            if match1 and match2:
                title1 = match1.group(2).strip()
                title2 = match2.group(2).strip()
                indent = match1.group(1)

                # Determine which to keep
                t1_lower = title1.lower().strip()
                t2_lower = title2.lower().strip()

                t1_is_generic = t1_lower in GENERIC_TITLES
                t2_is_generic = t2_lower in GENERIC_TITLES

                if t1_is_generic and not t2_is_generic:
                    # Keep title2 (more specific)
                    keep = title2
                    remove = title1
                elif t2_is_generic and not t1_is_generic:
                    # Keep title1 (more specific)
                    keep = title1
                    remove = title2
                elif t1_is_generic and t2_is_generic:
                    # Both generic, keep first
                    keep = title1
                    remove = title2
                else:
                    # Neither generic, keep the longer one
                    if len(title2) >= len(title1):
                        keep = title2
                        remove = title1
                    else:
                        keep = title1
                        remove = title2

                issues.append({
                    "line": i + 1,
                    "title1": title1,
                    "title2": title2,
                    "kept": keep,
                    "removed": remove,
                })

                fixed_lines.append(f'{indent}<div class="callout-title">{keep}</div>')
                skip_next = True
                continue

        fixed_lines.append(line)

    if issues and not dry_run:
        filepath.write_text("\n".join(fixed_lines), encoding="utf-8")

    return issues

def main():
    files = find_html_files()
    print(f"Scanning {len(files)} HTML files for duplicate callout-title divs...\n")

    total_issues = 0
    files_with_issues = 0

    for f in files:
        issues = detect_and_fix(f, dry_run=False)
        if issues:
            files_with_issues += 1
            rel = f.relative_to(BASE)
            print(f"  {rel}")
            for issue in issues:
                print(f"    Line {issue['line']}: DUPLICATE")
                print(f"      Title 1: \"{issue['title1']}\"")
                print(f"      Title 2: \"{issue['title2']}\"")
                print(f"      Kept:    \"{issue['kept']}\"")
                print(f"      Removed: \"{issue['removed']}\"")
            total_issues += len(issues)

    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_issues} duplicate callout-title pairs in {files_with_issues} files")
    print(f"All duplicates have been merged (kept the more specific title).")

if __name__ == "__main__":
    main()
