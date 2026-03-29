"""
Add missing title="" attribute to callout divs that lack one.

Standard: <div class="callout TYPE" title="TYPE: Short description">
The title attribute provides a hover tooltip matching the callout type.
"""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates", "styles"}

# Standard tooltip text per callout type
TITLE_MAP = {
    "big-picture": "Big Picture: Core concept overview",
    "key-insight": "Key Insight: Important takeaway",
    "note": "Note: Additional context",
    "warning": "Warning: Common pitfall",
    "practical-example": "Practical Example: Hands-on demonstration",
    "fun-note": "Fun Fact: Interesting trivia",
    "research-frontier": "Research Frontier: Cutting-edge development",
    "algorithm": "Algorithm: Step-by-step procedure",
    "tip": "Tip: Helpful suggestion",
    "exercise": "Exercise: Practice problem",
}

def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)

def fix_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    fixes = 0

    def add_title(match):
        nonlocal fixes
        prefix = match.group(1)
        classes = match.group(2)
        rest = match.group(3)

        # Extract callout type from classes
        callout_type = None
        for cls in classes.split():
            if cls in TITLE_MAP:
                callout_type = cls
                break

        if callout_type and 'title="' not in rest:
            fixes += 1
            tooltip = TITLE_MAP[callout_type]
            return f'{prefix}"{classes}" title="{tooltip}"{rest}'
        return match.group(0)

    new_text = re.sub(
        r'(<div\s+class="callout\s+)([^"]+)"(\s*>)',
        add_title,
        text
    )

    if fixes:
        filepath.write_text(new_text, encoding="utf-8")
    return fixes

def main():
    files = find_html_files()
    print(f"Scanning {len(files)} HTML files for callouts missing title attribute...\n")

    total = 0
    files_fixed = 0

    for f in files:
        n = fix_file(f)
        if n:
            files_fixed += 1
            total += n
            print(f"  {f.relative_to(BASE)}: {n} callouts fixed")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {total} title attributes added across {files_fixed} files")

if __name__ == "__main__":
    main()
