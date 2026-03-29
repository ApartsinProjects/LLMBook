"""
Fix duplicate code-caption divs that appear after code-output blocks.

Pattern to detect and fix:
  <div class="code-caption">...</div>   (first caption, keep)
  <div class="code-output">...</div>    (output block, keep)
  <div class="code-caption">...</div>   (duplicate caption, REMOVE)

The second caption is redundant. This script removes it.
Does NOT renumber captions (handled separately).
"""

import re
import glob
import os

# Match a code-caption div followed (with whitespace only) by a code-output div,
# followed (with whitespace only) by another code-caption div.
#
# Key: use [^<]* inside divs to prevent matching across HTML tags, which avoids
# the backtracking issue where .*? could span entire sections.
# For code-caption content we allow nested tags like <strong> and <code>,
# so we use a pattern that matches content without nested </div>.
#
# Groups:
#   1) The first code-caption + code-output block (to keep)
#   2) The duplicate code-caption (to remove)

def _no_nested_div(tag_class):
    """Build a pattern for a div with given class that does not contain nested divs."""
    # Match <div class="X"> then any content that does not include </div>, then </div>
    return rf'<div class="{tag_class}">(?:(?!</div>).)*?</div>'

CAPTION_PAT = _no_nested_div("code-caption")
OUTPUT_PAT = _no_nested_div("code-output")

PATTERN = re.compile(
    rf'({CAPTION_PAT}'     # group 1 start: first caption
    rf'\s*'
    rf'{OUTPUT_PAT})'      # group 1 end: code-output
    rf'(\s*'
    rf'{CAPTION_PAT})',    # group 2: duplicate caption to remove
    re.DOTALL
)


def scan_and_fix(file_path, dry_run=False):
    """Scan a file for the pattern. Returns list of matches found."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Collect all findings by iterating until no more matches (handles chains)
    findings = []
    temp = content
    while True:
        matches = list(PATTERN.finditer(temp))
        if not matches:
            break
        for m in matches:
            duplicate_caption = m.group(2).strip()
            label_match = re.search(r'<strong>(.*?)</strong>', duplicate_caption)
            label = label_match.group(1) if label_match else '(unknown)'
            findings.append(label)
        temp = PATTERN.sub(r'\1', temp)

    if not findings:
        return []

    if not dry_run:
        new_content = content
        # Loop until stable (handles chained caption-output-caption sequences)
        while PATTERN.search(new_content):
            new_content = PATTERN.sub(r'\1', new_content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return findings


def main():
    base = os.path.dirname(os.path.abspath(__file__))

    globs = [
        os.path.join(base, 'part-*', 'module-*', '**', '*.html'),
        os.path.join(base, 'appendices', '**', '*.html'),
    ]

    all_files = []
    for g in globs:
        all_files.extend(glob.glob(g, recursive=True))

    all_files = sorted(set(all_files))

    print(f"Scanning {len(all_files)} HTML files...\n")

    total_fixes = 0
    files_fixed = 0

    for fp in all_files:
        rel = os.path.relpath(fp, base)
        # First pass: report (dry run)
        findings = scan_and_fix(fp, dry_run=True)
        if findings:
            print(f"  {rel}")
            for label in findings:
                print(f"    - removing duplicate: {label}")
            # Second pass: actually fix
            scan_and_fix(fp, dry_run=False)
            total_fixes += len(findings)
            files_fixed += 1

    print(f"\nDone. Removed {total_fixes} duplicate caption(s) across {files_fixed} file(s).")


if __name__ == '__main__':
    main()
