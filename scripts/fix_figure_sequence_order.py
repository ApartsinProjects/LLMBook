"""Renumber Code Fragment / Figure / Algorithm / Table labels in document order.

The FIGURE_SEQUENCE audit complains when assets appear out of order in a
file (e.g., "Code Fragment 9.2.6 at line 301 appears after Code Fragment
9.2.8a at line 241"). This script reads each section file, walks through
the asset captions in document order, and renumbers them 1, 2, 3, ... so
the labels match position.

Also updates in-file prose references in `<strong>Code Fragment X.Y.K</strong>`
form (or similar) to use the new K.

Note: out-of-file references in other sections are NOT updated. Asset labels
are usually local; if you find references like "see Code Fragment 9.2.7 in
Section 9.2", those would need a separate sweep.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    '_archive', 'node_modules', '.git', 'pagefind', 'KDP',
    'build', 'vendor', '.claude', '__pycache__', '.book-update',
}

# Asset caption patterns; capture (full match, chap, sec, K_old)
ASSET_PATTERNS = {
    'Code Fragment': r'<strong>Code Fragment\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</strong>)',
    'Figure': r'<strong>Figure\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</strong>|\b)',
    'Algorithm': r'<div class="callout-title">Algorithm\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</div>)',
    'Table': r'<strong>Table\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</strong>|\b)',
    'Exercise': r'<div class="callout-title">Exercise\s+(\d+)\.(\d+)\.(\d+(?:[a-z])?)(:|</div>|<)',
}


def get_section_prefix(path: Path):
    m = re.match(r'^section-(\d+)\.(\d+)\.html$', path.name)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def fix_file(path: Path, apply: bool) -> int:
    sec_info = get_section_prefix(path)
    if sec_info is None:
        return 0
    chap, sec = sec_info
    text = path.read_text(encoding='utf-8')
    total_fixes = 0

    for kind, pat_str in ASSET_PATTERNS.items():
        # Find all matches in document order
        pat = re.compile(pat_str)
        matches = []
        for m in pat.finditer(text):
            c, s, k = int(m.group(1)), int(m.group(2)), m.group(3)
            if c == chap and s == sec:
                matches.append((m.start(), m.end(), k, m))
        if not matches:
            continue
        # Only renumber if K values are OUT OF ORDER (not just gappy).
        # Parse K as int (stripping any trailing letter).
        def k_to_int(k):
            m_k = re.match(r'^(\d+)', k)
            return int(m_k.group(1)) if m_k else 0
        current_ks = [m[2] for m in matches]
        current_ks_int = [k_to_int(k) for k in current_ks]
        if current_ks_int == sorted(current_ks_int):
            continue  # Already in order (gaps are OK)
        # Build remap: original_K_at_position_i -> (i + 1)
        # We rewrite captions in REVERSE position order to preserve offsets.
        new_text = text
        # Track unique K -> new K (for prose updates).
        # If the same K appeared at two positions, we can only safely remap
        # the captions; prose remap is ambiguous.
        k_to_new = {}
        for new_idx, (st, en, k_old, m_obj) in enumerate(matches):
            new_k = str(new_idx + 1)
            if k_old in k_to_new and k_to_new[k_old] != new_k:
                k_to_new[k_old] = None  # ambiguous
            elif k_old not in k_to_new:
                k_to_new[k_old] = new_k
        # Rewrite captions in reverse order
        for st, en, k_old, m_obj in reversed(matches):
            new_idx = matches.index((st, en, k_old, m_obj))
            new_k = str(new_idx + 1)
            if k_old == new_k:
                continue
            old_chunk = m_obj.group(0)
            # Replace only the K portion: chap.sec.k_old -> chap.sec.new_k
            new_chunk = old_chunk.replace(f'{chap}.{sec}.{k_old}',
                                           f'{chap}.{sec}.{new_k}', 1)
            new_text = new_text[:st] + new_chunk + new_text[en:]
            total_fixes += 1
        text = new_text
        # Now update prose refs (only unambiguous remaps)
        for k_old, new_k in k_to_new.items():
            if new_k is None or k_old == new_k:
                continue
            # Patterns like <strong>Code Fragment X.Y.K</strong>
            prose_pat = re.compile(
                rf'(<strong>{kind}\s+){chap}\.{sec}\.{re.escape(k_old)}(</strong>)'
            )
            text, n = prose_pat.subn(rf'\g<1>{chap}.{sec}.{new_k}\g<2>', text)
            total_fixes += n

    if total_fixes and apply:
        path.write_text(text, encoding='utf-8')
    return total_fixes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--files', nargs='+', help='specific files to fix')
    args = ap.parse_args()

    if args.files:
        paths = [Path(f) for f in args.files]
    else:
        paths = list(ROOT.rglob('section-*.html'))
        paths = [p for p in paths
                 if not any(s in p.parts for s in SKIP_DIRS)]

    total = 0
    for p in paths:
        n = fix_file(p, args.apply)
        if n:
            try:
                rel = p.relative_to(ROOT)
            except ValueError:
                rel = p
            print(f"  {rel}: {n} fix(es)")
            total += n
    print(f"\nTotal: {total} fixes {'applied' if args.apply else 'would apply (dry run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == '__main__':
    main()
