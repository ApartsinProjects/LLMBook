"""
Detect and fix non-standard illustration/figure captions.

Standard format (no inline styles):
  <figure class="illustration">
      <img src="..." alt="..." loading="lazy">
      <figcaption>Caption text.</figcaption>
  </figure>

Issues to detect:
1. figcaption with inline style attributes
2. img with inline style attributes inside figures
3. figure without class="illustration"
4. figure with inline style attributes
5. Images wrapped in non-standard containers
"""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates", "styles"}

def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)

def detect_issues(filepath):
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    issues = []

    for i, line in enumerate(lines, 1):
        # figcaption with inline style
        if re.search(r'<figcaption\s+style=', line):
            issues.append((i, "FIGCAPTION_INLINE_STYLE", line.strip()))

        # figure with inline style
        if re.search(r'<figure\s[^>]*style=', line):
            issues.append((i, "FIGURE_INLINE_STYLE", line.strip()))

        # img inside figure with inline style
        if re.search(r'<img\s[^>]*style=', line):
            # Check if inside a figure context (rough heuristic: within 3 lines of <figure)
            context = "\n".join(lines[max(0, i-4):i])
            if "<figure" in context or "illustration" in context:
                issues.append((i, "IMG_INLINE_STYLE_IN_FIGURE", line.strip()))

        # figure without class="illustration"
        m = re.search(r'<figure(?:\s|>)', line)
        if m and 'class="illustration"' not in line and '<figure>' in line:
            issues.append((i, "FIGURE_NO_CLASS", line.strip()))

    return issues

def fix_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    original = text

    # Fix figcaption with inline styles - remove style attribute
    text = re.sub(
        r'<figcaption\s+style="[^"]*"[^>]*>',
        '<figcaption>',
        text
    )

    # Fix figure with inline styles - keep class but remove style
    text = re.sub(
        r'(<figure\s+class="illustration")\s+style="[^"]*"',
        r'\1',
        text
    )

    # Fix bare <figure> without class
    text = re.sub(
        r'<figure>',
        '<figure class="illustration">',
        text
    )

    # Fix img inline styles inside figures
    # Remove style attribute from img tags that have it
    # More targeted: only within figure.illustration context
    # We'll do a multi-line approach
    def fix_img_in_figure(match):
        block = match.group(0)
        # Remove style from img tags within this figure block
        block = re.sub(
            r'(<img\s[^>]*?)style="[^"]*"\s*',
            r'\1',
            block
        )
        # Clean up double spaces
        block = re.sub(r'  +', ' ', block)
        return block

    text = re.sub(
        r'<figure class="illustration">.*?</figure>',
        fix_img_in_figure,
        text,
        flags=re.DOTALL
    )

    # Add loading="lazy" to img in figures if missing
    def add_lazy(match):
        block = match.group(0)
        if 'loading=' not in block:
            block = re.sub(r'(<img\s)', r'\1loading="lazy" ', block)
        return block

    text = re.sub(
        r'<figure class="illustration">.*?</figure>',
        add_lazy,
        text,
        flags=re.DOTALL
    )

    changed = text != original
    if changed:
        filepath.write_text(text, encoding="utf-8")
    return changed

def main():
    files = find_html_files()
    print(f"Scanning {len(files)} HTML files for non-standard illustration captions...\n")

    total_issues = 0
    files_with_issues = 0
    issues_by_type = {}

    # Phase 1: Detect
    all_issues = {}
    for f in files:
        issues = detect_issues(f)
        if issues:
            all_issues[f] = issues
            files_with_issues += 1
            total_issues += len(issues)
            for _, itype, _ in issues:
                issues_by_type[itype] = issues_by_type.get(itype, 0) + 1

    # Print detection results
    for f, issues in sorted(all_issues.items()):
        rel = f.relative_to(BASE)
        print(f"  {rel}")
        for line_num, itype, snippet in issues:
            print(f"    Line {line_num}: {itype}")
            print(f"      {snippet[:120]}")

    print(f"\n{'='*60}")
    print(f"DETECTION: {total_issues} issues in {files_with_issues} files")
    for itype, count in sorted(issues_by_type.items()):
        print(f"  {itype}: {count}")

    # Phase 2: Fix all files with figures/figcaptions
    print(f"\nApplying fixes...")
    fixed_count = 0
    for f in files:
        if fix_file(f):
            fixed_count += 1

    print(f"Fixed {fixed_count} files.")

    # Phase 3: Re-detect
    print(f"\nRe-scanning after fixes...")
    remaining = 0
    for f in files:
        issues = detect_issues(f)
        if issues:
            remaining += len(issues)
            rel = f.relative_to(BASE)
            for line_num, itype, snippet in issues:
                print(f"  REMAINING: {rel} Line {line_num}: {itype}")

    print(f"\nRemaining issues: {remaining}")

if __name__ == "__main__":
    main()
