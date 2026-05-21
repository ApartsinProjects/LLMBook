"""Renumber asset captions in document order (CAPTIONS ONLY, NO PROSE).

This is a safe re-numbering script that ONLY touches lines matching the
caption-wrapper pattern (e.g., `<div class="code-caption"><strong>Code
Fragment X.Y.K`). It does NOT modify prose `<strong>Code Fragment X.Y.K</strong>`
references in body text, so it avoids the cascade bug where prose
substitution chained through multiple K remappings.

The trade-off: prose refs may become stale (e.g., body text says "see Code
Fragment 24.1.3" but caption is now numbered 1). Authors should review prose
refs separately, but at minimum captions will be unique and in document order.

Usage:
  py -3 scripts/fix_caption_order_only.py --files <paths> --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

CAPTION_PATTERNS = [
    # Code Fragment caption inside code-caption div
    (
        'Code Fragment',
        re.compile(
            r'(<div class="code-caption"[^>]*><strong>Code Fragment\s+)(\d+)\.(\d+)\.(\d+(?:[a-z])?)(</strong>|:</strong>|\b)',
        ),
    ),
    # Figure caption inside diagram-caption or figcaption
    (
        'Figure',
        re.compile(
            r'(<(?:div class="(?:diagram|figure)-caption"[^>]*|figcaption[^>]*)>(?:[^<]*<strong>)?Figure\s+)(\d+)\.(\d+)\.(\d+(?:[a-z])?)',
        ),
    ),
    # Table caption
    (
        'Table',
        re.compile(
            r'(<div class="(?:comparison-)?table-(?:title|caption)"[^>]*><strong>Table\s+)(\d+)\.(\d+)\.(\d+(?:[a-z])?)',
        ),
    ),
]


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
    total = 0

    # Use placeholder-based single-pass substitution
    placeholders = {}
    pfx = '\x00CAP\x01'
    sfx = '\x02'
    counter = [0]

    def stash(repl: str) -> str:
        idx = counter[0]
        counter[0] += 1
        ph = f'{pfx}{idx}{sfx}'
        placeholders[ph] = repl
        return ph

    for kind, pat in CAPTION_PATTERNS:
        # Collect matches in document order
        matches = []
        for m in pat.finditer(text):
            c, s, k = int(m.group(2)), int(m.group(3)), m.group(4)
            if c == chap and s == sec:
                matches.append((m, k))
        if not matches:
            continue
        # Check if already in order (numeric K)
        def k_int(k):
            mk = re.match(r'^(\d+)', k)
            return int(mk.group(1)) if mk else 0
        current = [k_int(k) for _, k in matches]
        if current == sorted(current) and len(set(current)) == len(current):
            continue  # Already in order and unique
        # Build target list: 1, 2, 3, ...
        # Process matches in document order to build new K mapping
        target_ks = [str(i + 1) for i in range(len(matches))]
        # Apply in REVERSE order via placeholder
        new_text = text
        for (m_obj, k_old), new_k in zip(reversed(matches), reversed(target_ks)):
            if k_old == new_k:
                continue
            st, en = m_obj.start(), m_obj.end()
            # Rebuild the matched chunk with new K
            old_match = m_obj.group(0)
            # Replace the K portion only
            new_chunk = old_match.replace(
                f'{chap}.{sec}.{k_old}', f'{chap}.{sec}.{new_k}', 1)
            placeholder = stash(new_chunk)
            new_text = new_text[:st] + placeholder + new_text[en:]
            total += 1
        text = new_text

    # Resolve placeholders
    for ph, repl in placeholders.items():
        text = text.replace(ph, repl)

    if total and apply:
        path.write_text(text, encoding='utf-8')
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--files', nargs='+', required=True)
    args = ap.parse_args()
    total = 0
    for f in args.files:
        p = Path(f)
        n = fix_file(p, args.apply)
        if n:
            try:
                rel = p.relative_to(ROOT)
            except ValueError:
                rel = p
            print(f"  {rel}: {n} fix(es)")
            total += n
    print(f"\nTotal: {total} fixes {'applied' if args.apply else 'would apply (dry run)'}")


if __name__ == '__main__':
    main()
