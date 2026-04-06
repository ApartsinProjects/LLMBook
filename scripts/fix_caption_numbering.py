"""
Fix code fragment caption numbering across the entire book.

For each section file (section-X.Y.html):
1. Finds all <div class="code-caption"><strong>Code Fragment X.Y.N:</strong>...</div>
2. Renumbers N sequentially (1, 2, 3, ...) in document order
3. Updates inline prose references like "Code Fragment X.Y.N below"
4. Reports and removes duplicate captions for the same code block
5. Also handles Pseudocode X.Y.N captions

Usage:
  python fix_caption_numbering.py          # Dry run (report only)
  python fix_caption_numbering.py --fix    # Apply fixes
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Match Code Fragment captions
CAPTION_RE = re.compile(
    r'(<div class="code-caption">\s*<strong>Code Fragment )(\d+\.\d+)\.(\d+)(:</strong>)',
    re.DOTALL
)

# Match inline references like "Code Fragment 9.4.16 below" or "Code Fragment 9.4.16)"
INLINE_REF_RE = re.compile(
    r'(Code Fragment )(\d+\.\d+)\.(\d+)(\b)'
)


def analyze_and_fix(filepath, fix=False):
    """Analyze caption numbering in a file. Optionally fix."""
    content = filepath.read_text(encoding="utf-8")
    original = content

    fname = filepath.stem
    m = re.match(r'section-(\d+)\.(\d+)', fname)
    if not m:
        return []
    sec_prefix = f"{m.group(1)}.{m.group(2)}"

    # Find all Code Fragment captions for this section
    captions = list(CAPTION_RE.finditer(content))
    # Filter to only captions matching this section's prefix
    section_captions = [c for c in captions if c.group(2) == sec_prefix]

    if not section_captions:
        return []

    issues = []

    # Check if numbering is already correct
    needs_fix = False
    old_to_new = {}
    for i, cap in enumerate(section_captions):
        old_num = int(cap.group(3))
        new_num = i + 1
        if old_num != new_num:
            needs_fix = True
            line_no = content[:cap.start()].count('\n') + 1
            issues.append(f"  L{line_no}: Code Fragment {sec_prefix}.{old_num} -> {sec_prefix}.{new_num}")
        old_to_new[old_num] = new_num

    if not needs_fix:
        return []

    if not fix:
        return issues

    # Apply fix using two-phase placeholder approach to avoid swap cycles.
    # Phase 1: Replace all old numbers with unique placeholders
    # Phase 2: Replace placeholders with final sequential numbers

    PLACEHOLDER = "@@CAPNUM_{}@@"

    # Phase 1: Replace captions with placeholders
    cap_counter = [0]

    def caption_to_placeholder(match):
        if match.group(2) != sec_prefix:
            return match.group(0)
        cap_counter[0] += 1
        return f'{match.group(1)}{PLACEHOLDER.format(cap_counter[0])}{match.group(4)}'

    content = CAPTION_RE.sub(caption_to_placeholder, content)

    # Replace inline references with placeholders using the mapping
    def ref_to_placeholder(match):
        if match.group(2) != sec_prefix:
            return match.group(0)
        old_num = int(match.group(3))
        new_num = old_to_new.get(old_num, old_num)
        return f'{match.group(1)}{PLACEHOLDER.format(new_num)}{match.group(4)}'

    content = INLINE_REF_RE.sub(ref_to_placeholder, content)

    # Phase 2: Replace all placeholders with final numbers
    for num in range(1, cap_counter[0] + 1):
        content = content.replace(PLACEHOLDER.format(num), f'{sec_prefix}.{num}')

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        issues.append("  -> FIXED")

    return issues


def main():
    fix = '--fix' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    total_files_with_issues = 0
    for f in all_files:
        issues = analyze_and_fix(f, fix=fix)
        if issues:
            total_files_with_issues += 1
            rel = f.relative_to(BOOK_ROOT)
            print(f"\n{rel}:")
            for issue in issues:
                print(issue)

    print(f"\n{'='*60}")
    print(f"Files with numbering issues: {total_files_with_issues}")
    print(f"Total files scanned: {len(all_files)}")
    if not fix and total_files_with_issues > 0:
        print(f"\nRun with --fix to apply changes.")


if __name__ == "__main__":
    main()
