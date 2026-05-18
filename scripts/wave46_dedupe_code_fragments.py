"""Wave 46: Renumber duplicate Code Fragment captions.

Pattern: within a single file, multiple <div class="code-caption"> divs use
the same "Code Fragment X.Y.Z" number. Keep the first occurrence as-is; for
each subsequent duplicate, increment to the next unused number within that
file's X.Y prefix.

Example: if file has Code Fragment 42.9.6 at line 460 and again at line 592,
and the file's existing fragments are 42.9.1-42.9.6, then the line-592 caption
becomes Code Fragment 42.9.7.

Only operates on CAPTION instances (inside <div class="code-caption"><strong>...).
Prose references (e.g. "as shown in Code Fragment 42.9.6") are left untouched
since they may refer to either occurrence (re-checking those is a separate
authoring task).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match: <div class="code-caption"><strong>Code Fragment X.Y.Z[:]</strong>
CAPTION_RE = re.compile(
    r'(<div\s+class="code-caption">\s*<strong>\s*Code Fragment\s+)(\d+\.\d+\.\d+)(\s*:?)(\s*</strong>)',
    re.IGNORECASE,
)


def dedupe_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    # First pass: collect all caption fragment numbers in order
    matches = list(CAPTION_RE.finditer(text))
    if len(matches) < 2:
        return 0

    # Group by chapter.section prefix
    seen_per_prefix: dict[str, set[int]] = {}
    rewrites: list[tuple[int, int, str]] = []  # (start, end, new_text)
    n_dedupe = 0

    for m in matches:
        full_num = m.group(2)  # e.g. "42.9.6"
        parts = full_num.split('.')
        prefix = '.'.join(parts[:-1])  # "42.9"
        idx = int(parts[-1])  # 6

        seen = seen_per_prefix.setdefault(prefix, set())
        if idx not in seen:
            seen.add(idx)
            continue

        # Duplicate — find next unused index
        next_idx = idx + 1
        while next_idx in seen:
            next_idx += 1
        seen.add(next_idx)

        new_num = f'{prefix}.{next_idx}'
        new_caption = m.group(1) + new_num + m.group(3) + m.group(4)
        rewrites.append((m.start(), m.end(), new_caption))
        n_dedupe += 1

    if not rewrites:
        return 0

    # Apply rewrites right-to-left
    rewrites.sort(reverse=True)
    new_text = text
    for start, end, replacement in rewrites:
        new_text = new_text[:start] + replacement + new_text[end:]

    p.write_text(new_text, encoding='utf-8')
    return n_dedupe


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = dedupe_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
            print(f'  {p.relative_to(ROOT)}: {n} renumbered')
    print(f'\nTotal Code Fragment captions renumbered: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
