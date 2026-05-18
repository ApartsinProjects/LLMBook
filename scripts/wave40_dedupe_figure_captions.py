"""Wave 40: DUP_FIGURE_NUM heuristic deduplication.

Per user approval: carte blanche to remove duplicate Figure/Table/Code-Fragment
captions by keeping the FIRST occurrence in each file.

Patterns affected (per DUP_FIGURE_NUM plugin):
  - `<figcaption><strong>Figure X.Y.Z</strong>:...` appearing on multiple lines
  - `<div class="diagram-caption"><strong>Figure X.Y.Z</strong>:...` appearing twice
  - `<div class="code-caption"><strong>Code Fragment X.Y.Z</strong>:...` twice
  - `<div class="comparison-table-title"><strong>Table X.Y.Z</strong>:...` twice

Strategy: for each file, scan captions in document order. If a caption's
LABEL ("Figure 3.1.1", "Code Fragment 5.2.1", etc.) has already appeared in
this file, REMOVE the entire caption element (the line containing it).

This is the safer approach: keeping the first occurrence preserves the
correct figure-caption pairing in most cases (where the dup is a leftover
artifact of a forced merge or copy-paste).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match a caption block (one line typically):
#   <figcaption><strong>Figure X.Y.Z</strong>:...</figcaption>
#   <div class="diagram-caption"><strong>Figure X.Y.Z</strong>:...</div>
#   <div class="code-caption"><strong>Code Fragment X.Y.Z</strong>:...</div>
#   <div class="comparison-table-title"><strong>Table X.Y.Z</strong>:...</div>
CAPTION_PATTERNS = [
    re.compile(r'<figcaption>\s*<strong>(Figure\s+\d+(?:\.\d+){1,2})[a-z]?</strong>[\s\S]*?</figcaption>\s*\n?', re.IGNORECASE),
    re.compile(r'<div\s+class="diagram-caption">\s*<strong>(Figure\s+\d+(?:\.\d+){1,2})[a-z]?</strong>[\s\S]*?</div>\s*\n?', re.IGNORECASE),
    re.compile(r'<div\s+class="code-caption">\s*<strong>(Code\s+Fragment\s+\d+(?:\.\d+){1,2})[a-z]?</strong>[\s\S]*?</div>\s*\n?', re.IGNORECASE),
    re.compile(r'<div\s+class="comparison-table-title">\s*<strong>(Table\s+\d+(?:\.\d+){1,2})[a-z]?</strong>[\s\S]*?</div>\s*\n?', re.IGNORECASE),
]


def dedupe_in_file(text: str) -> tuple[str, int]:
    """Find all caption blocks; if a label appears multiple times, remove all but first."""
    # First pass: find all caption blocks with their labels
    occurrences = []  # list of (label, match_start, match_end, full_match)
    for pat in CAPTION_PATTERNS:
        for m in pat.finditer(text):
            label = m.group(1).strip()
            # Normalize: collapse multiple spaces
            label = re.sub(r'\s+', ' ', label)
            occurrences.append((label, m.start(), m.end(), m.group(0)))

    # Sort by start position
    occurrences.sort(key=lambda x: x[1])

    # Group by label
    label_first_pos = {}
    to_remove_ranges = []  # (start, end) spans to delete
    for label, start, end, full in occurrences:
        if label in label_first_pos:
            # Duplicate; remove this occurrence
            to_remove_ranges.append((start, end))
        else:
            label_first_pos[label] = start

    if not to_remove_ranges:
        return text, 0

    # Remove ranges in reverse order to preserve offsets
    new_text = text
    for start, end in reversed(to_remove_ranges):
        new_text = new_text[:start] + new_text[end:]

    return new_text, len(to_remove_ranges)


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = dedupe_in_file(text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
            if n > 1 or n_files <= 20:
                print(f'  {p.relative_to(ROOT)}: removed {n} duplicate caption(s)')
    print(f'\nRemoved {n_total} duplicate captions across {n_files} files')


if __name__ == '__main__':
    main()
