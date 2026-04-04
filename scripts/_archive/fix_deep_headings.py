"""
Convert h4/h5/h6 headings outside callout blocks to h3 (or h2 if they appear to be section-level).

Standard: only h1 (in header), h2 (main sections), h3 (subsections) in content.
h4/h5/h6 should not appear outside callouts.

Strategy:
- h4 -> h3 (most common case: subsection headings)
- h5 -> h3
- h6 -> h3
- Preserve all attributes and content
"""

import re
from pathlib import Path
from collections import defaultdict

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates", "styles"}

def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)

def fix_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    orig = text
    fixes = 0

    # We need to avoid converting h4/h5/h6 inside callout blocks
    # Strategy: track callout nesting depth
    lines = text.split("\n")
    new_lines = []
    in_callout = 0  # nesting depth

    for line in lines:
        # Track callout entry/exit
        # Count callout opens
        callout_opens = len(re.findall(r'<div\s+class="callout\b', line))
        in_callout += callout_opens

        # Only fix if not inside a callout
        if in_callout == 0:
            # Replace h4/h5/h6 opening and closing tags
            new_line = line
            for n in ["4", "5", "6"]:
                if f"<h{n}" in new_line or f"</h{n}>" in new_line:
                    new_line = re.sub(f"<h{n}(\\b)", "<h3\\1", new_line)
                    new_line = re.sub(f"</h{n}>", "</h3>", new_line)
                    if new_line != line:
                        fixes += 1
            line = new_line

        # Count div closes (approximate callout exits)
        if in_callout > 0:
            div_closes = line.count("</div>")
            in_callout = max(0, in_callout - div_closes)
            # Re-add callout opens that were on the same line
            # (already counted above)

        new_lines.append(line)

    if fixes:
        filepath.write_text("\n".join(new_lines), encoding="utf-8")
    return fixes

def main():
    files = find_html_files()
    print(f"Scanning {len(files)} HTML files for deep headings (h4/h5/h6) outside callouts...\n")

    total = 0
    files_fixed = 0

    for f in files:
        n = fix_file(f)
        if n:
            files_fixed += 1
            total += n
            print(f"  {f.relative_to(BASE)}: {n} headings converted to h3")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {total} deep headings converted in {files_fixed} files")

if __name__ == "__main__":
    main()
