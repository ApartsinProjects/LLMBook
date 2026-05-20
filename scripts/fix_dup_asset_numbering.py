"""Renumber duplicate Code Fragment / Figure / Algorithm / Table labels.

When a file has duplicate asset numbers (e.g., Code Fragment 47.2.1 appearing
twice), this script renumbers them sequentially in document order. Targets ONLY
files that the audit flags as having duplicates.

For each asset type (Code Fragment, Figure, Algorithm, Table, Exercise),
scans the file in document order and assigns 1, 2, 3, ... within the same
chapter.section prefix. Updates the caption strong tag AND any in-prose
references to the same label in the same file.

This is a "best effort" deduplication. It does not touch cross-file
references (which would be hard to disambiguate without context).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent


ASSETS = {
    'Code Fragment': r'<div class="code-caption"[^>]*><strong>Code Fragment\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</strong>)',
    'Figure': r'<div class="(?:diagram-caption|figure-caption)"[^>]*><strong>Figure\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</strong>)',
    'Algorithm': r'<div class="callout-title">Algorithm\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</div>)',
    'Table': r'<div class="(?:comparison-)?table(?:-caption|-title)"[^>]*><strong>Table\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</strong>)',
}


def get_section_prefix(filepath: Path):
    """Derive 'C.S' from filename 'section-C.S.html'."""
    m = re.match(r'^section-(\d+)\.(\d+)\.html$', filepath.name)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def fix_file_assets(path: Path, apply: bool):
    text = path.read_text(encoding='utf-8')
    sec_info = get_section_prefix(path)
    if sec_info is None:
        return 0
    chap, sec = sec_info
    fixes = 0

    for kind, pat_str in ASSETS.items():
        pat = re.compile(pat_str)
        captions = []  # list of (start, end, k_old, m.group(2))
        for m in pat.finditer(text):
            c, s, k_str = int(m.group(1)), int(m.group(2)), m.group(3)
            if c != chap or s != sec:
                continue
            captions.append((m.start(), m.end(), k_str, m))
        if not captions:
            continue
        # Check for duplicates in this kind
        k_counts = {}
        for _, _, k_str, _ in captions:
            k_counts[k_str] = k_counts.get(k_str, 0) + 1
        if all(c == 1 for c in k_counts.values()):
            continue  # No duplicates, skip this asset type
        # Renumber sequentially in document order
        # Build old_K_with_position -> new_K
        # Strategy: for the i-th caption, new_K = i+1
        replacement_pairs = []  # (old_label, new_label, span)
        for i, (st, en, k_str, m) in enumerate(captions, start=1):
            new_k = str(i)
            old_label = f'{kind} {chap}.{sec}.{k_str}'
            new_label = f'{kind} {chap}.{sec}.{new_k}'
            replacement_pairs.append((old_label, new_label, st))
        # Apply caption-tag replacements first, in reverse position order
        # to preserve offsets.
        new_text = text
        for st, en, k_str, m in reversed(captions):
            i_pos = next(i for i, (s, e, k, _) in enumerate(captions) if s == st)
            new_k = str(i_pos + 1)
            old_chunk = m.group(0)
            new_chunk = old_chunk.replace(f'{chap}.{sec}.{k_str}', f'{chap}.{sec}.{new_k}', 1)
            if old_chunk == new_chunk:
                continue
            new_text = new_text[:st] + new_chunk + new_text[en:]
            if old_chunk != new_chunk:
                fixes += 1
        text = new_text

        # Now also update in-prose references to the same old K values, but
        # be careful: an old K like '5' might map to multiple new K values
        # (if there were duplicates of '5'). We can only safely rewrite if
        # the old K was UNIQUE. Skip ambiguous ones.
        # Build old_K -> new_K map (only for unique old K)
        unique_remap = {}
        new_caps = list(pat.finditer(text))
        # Iterate again over the original captions to build mapping
        for i, (_, _, k_str_old, _) in enumerate(captions, start=1):
            # New K is i (positional)
            new_k = str(i)
            if k_str_old in unique_remap:
                # Conflict: same old K mapped to multiple new K
                unique_remap[k_str_old] = None
            else:
                unique_remap[k_str_old] = new_k
        for k_str_old, new_k in unique_remap.items():
            if new_k is None:
                continue
            if k_str_old == new_k:
                continue
            # Rewrite prose refs like "<strong>Code Fragment C.S.K_OLD</strong>"
            prose_pat = re.compile(
                rf'(<strong>{kind}\s+){chap}\.{sec}\.{re.escape(k_str_old)}(</strong>)'
            )
            text, n = prose_pat.subn(rf'\g<1>{chap}.{sec}.{new_k}\g<2>', text)
            fixes += n

    if fixes and apply:
        path.write_text(text, encoding='utf-8')
    return fixes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--files', nargs='+', help='specific section files to fix')
    args = ap.parse_args()

    if args.files:
        paths = [Path(f) for f in args.files]
    else:
        paths = list(ROOT.rglob('section-*.html'))
        paths = [p for p in paths if '_archive' not in p.parts]

    total = 0
    for p in paths:
        n = fix_file_assets(p, args.apply)
        if n:
            print(f"  {p.relative_to(ROOT)}: {n} fix(es)")
            total += n
    print(f"\nTotal: {total} fixes {'applied' if args.apply else 'would apply (dry run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == '__main__':
    main()
