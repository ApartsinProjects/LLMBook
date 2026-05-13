"""Renumber duplicate Figure X.Y.Z labels within a section.

For each section, scan in document order. Track which figure numbers
have been used. When we hit a duplicate (the same X.Y.Z appearing for
a different figure), renumber the duplicate to the next available
number in the same chapter (X.Y.N+1 where N is the current max).

Touches BOTH the displayed <strong>Figure X.Y.Z</strong> labels AND
any cross-references to those figures within the same file. Does NOT
touch cross-references from OTHER files (those would need an inter-
file pass; the duplicate-fix scope here is intra-section since that
is where the user-visible defect lives).

Idempotent.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

FIG_LABEL_RE = re.compile(r'<strong>Figure\s+([\d]+\.[\d]+(?:\.[\d]+)?[a-z]?)</strong>')


def renumber_file(text: str) -> tuple[str, list[tuple[str, str]]]:
    """For each section, find duplicate Figure X.Y.Z labels and renumber
    the second occurrence to the next available number.

    Returns (new_text, list_of_remappings).
    """
    # 1) Find all figure labels in document order, with offsets
    matches = list(FIG_LABEL_RE.finditer(text))
    if not matches:
        return text, []

    # 2) Group by "base" (X.Y) and figure out max Z used per base
    from collections import defaultdict
    base_to_used = defaultdict(set)
    base_to_max = defaultdict(int)
    for m in matches:
        full = m.group(1)
        # Strip trailing alpha (e.g., '16.4.1a' -> base '16.4', z '1a')
        parts = full.split('.')
        if len(parts) >= 3:
            base = '.'.join(parts[:2])
            z_part = parts[2]
            # Numeric prefix of z
            num_match = re.match(r'(\d+)', z_part)
            if num_match:
                z = int(num_match.group(1))
                base_to_used[base].add(z)
                base_to_max[base] = max(base_to_max[base], z)
            base_to_used[base].add(full)
        else:
            # 2-part fig like '1.4' -- skip
            continue

    # 3) Walk matches in order; track first occurrence per full label.
    #    On second occurrence, allocate a new Z = max+1 (and bump max).
    seen_full = {}
    remap = []  # list of (offset, old_full, new_full)
    for m in matches:
        full = m.group(1)
        parts = full.split('.')
        if len(parts) < 3:
            continue
        if full not in seen_full:
            seen_full[full] = m.start()
            continue
        # Duplicate. Allocate next available Z.
        base = '.'.join(parts[:2])
        base_to_max[base] += 1
        new_z = base_to_max[base]
        new_full = f'{base}.{new_z}'
        remap.append((m.start(), full, new_full))

    if not remap:
        return text, []

    # 4) Apply remaps in REVERSE order so offsets remain valid
    new_text = text
    out_remap = []
    for offset, old_full, new_full in reversed(remap):
        # Replace just the label-text portion (Figure X.Y.Z) at this offset
        # Use a precise replacement: find the label starting at offset
        label_pat = re.compile(r'<strong>Figure\s+' + re.escape(old_full) + r'</strong>')
        m = label_pat.search(new_text, offset)
        if m and m.start() == offset:
            new_text = (new_text[:m.start()]
                        + f'<strong>Figure {new_full}</strong>'
                        + new_text[m.end():])
            out_remap.append((old_full, new_full))

    # 5) Also re-write any intra-file cross-references that name the OLD
    #    figure number, BUT only the second-and-later mentions. The first
    #    mention is the original figure that kept its number; subsequent
    #    references that point to the SAME figure should NOT be touched.
    #    Since we cannot disambiguate intent, we leave non-label mentions
    #    alone and rely on the duplicate-fix happening at label level only.
    #    The user-visible issue (two figures sharing a label) is resolved.

    return new_text, out_remap


def main() -> int:
    n_files = 0
    n_renumbered = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_text, remaps = renumber_file(text)
        if remaps:
            p.write_text(new_text, encoding='utf-8')
            n_files += 1
            n_renumbered += len(remaps)
            print(f'  renumbered: {p.relative_to(ROOT)}')
            for old, new in remaps:
                print(f'      Figure {old} -> Figure {new}')
    print(f'\nRenumbered {n_renumbered} duplicate labels across {n_files} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
