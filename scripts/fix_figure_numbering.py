#!/usr/bin/env python
"""Fix duplicate and out-of-sequence Figure/Code Fragment numbering in section files.

Strategy (per file):
1. Parse all caption-bearing elements (figcaption, code-caption, diagram-caption)
   in document order, capturing (kind, base_number, letter_suffix, line).
2. Determine the section's canonical prefix from the filename
   (e.g., section-9.2.html -> 9.2).
3. Group entries into "rename groups" that share a single new base number.
   A run of consecutive (per kind) lettered captions with the same old base
   forms one group; every other caption is its own group.
4. Walk groups in document order and assign monotonically-increasing
   sequence numbers per kind, starting at 1.  Each group's letters survive.
5. Re-emit the file in a single positional pass:
     - Caption occurrences get the new label assigned to that group.
     - Prose / img-alt occurrences use a global rename map; ambiguous
       old labels (same key in 2+ groups) are left untouched and reported.

Run:  python scripts/fix_figure_numbering.py [--dry-run] [files...]
If no files are given, processes every section-*.html under the book root.
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Caption marker keywords used to identify caption-bearing lines.
CAPTION_MARKERS = ("figcaption", "code-caption", "diagram-caption")

# Matches a complete caption block: figcaption, code-caption div, diagram-caption div,
# or <caption>.  We use this to extract the full caption substring so we can
# pick the FIRST "<strong>Figure X.Y.Z" inside it as the caption's own label.
CAPTION_BLOCK_RE = re.compile(
    r'<figcaption\b[^>]*>(.*?)</figcaption>'
    r'|<div\s+class="code-caption"[^>]*>(.*?)</div>'
    r'|<div\s+class="diagram-caption"[^>]*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)

# Matches "<strong>(Figure|Code Fragment) X.Y.Z[letter]" inside a caption.
# We accept both "<strong>X:</strong>" and "<strong>X</strong>:" forms.
CAP_NUM_RE = re.compile(
    r'<strong>\s*(?P<kind>Figure|Code Fragment)\s+'
    r'(?P<base>\d+\.\d+\.\d+)'
    r'(?P<letter>[a-z])?'
    r'\s*[:<]'
)

# Generic match for any "Figure X.Y.Z" / "Code Fragment X.Y.Z" reference
# anywhere in the file.  Used to rewrite prose cross-references and
# img-alt labels.
GENERIC_REF_RE = re.compile(
    r'\b(?P<kind>Figure|Code Fragment)\s+'
    r'(?P<base>\d+\.\d+\.\d+)'
    r'(?P<letter>[a-z])?\b'
)


def section_prefix_from_path(p: Path) -> str | None:
    """Derive the canonical section prefix from a section-X.Y.html filename.

    Note: section-X.Yb.html ("split section continuation" files) are skipped
    because their captions logically belong to the parent section-X.Y.html
    numbering space; we can't safely renumber them in isolation.
    """
    m = re.match(r'section-(\d+\.\d+)\.html$', p.name)
    return m.group(1) if m else None


def line_starts(text: str):
    """Return a sorted list of character offsets at which each line starts."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def line_of(starts, pos):
    """Binary-search the line number (1-based) for a character position."""
    lo, hi = 0, len(starts)
    while lo < hi:
        mid = (lo + hi) // 2
        if starts[mid] <= pos:
            lo = mid + 1
        else:
            hi = mid
    return lo  # 1-based


def collect_caption_anchors(text: str, line_starts_arr):
    """For every caption block (figcaption, code-caption, diagram-caption),
    extract the FIRST "<strong>(Figure|Code Fragment) X.Y.Z[letter]" inside
    the block.  That match represents the caption's own label.  Cross-refs
    to OTHER fragments that appear inside the caption text (after the first
    label) are NOT anchors -- they're prose, just like cross-refs outside
    the caption.

    Yields (match_pos, match_end, kind, base, letter, line_no) tuples in
    document order.
    """
    out = []
    for block_m in CAPTION_BLOCK_RE.finditer(text):
        # Find the FIRST <strong>(Figure|Code Fragment) X.Y.Z[letter] inside
        # the matched caption block.  The block starts at block_m.start();
        # the inner caption text starts at the first non-None group end.
        block_start = block_m.start()
        block_end = block_m.end()
        inner_match = CAP_NUM_RE.search(text, block_start, block_end)
        if inner_match is None:
            continue
        ln = line_of(line_starts_arr, inner_match.start())
        out.append((inner_match.start(), inner_match.end(),
                    inner_match.group("kind"), inner_match.group("base"),
                    inner_match.group("letter") or "", ln))
    out.sort()
    return out


def renumber_file(path: Path, dry_run: bool = False, verbose: bool = False):
    text = path.read_text(encoding="utf-8")
    section_prefix = section_prefix_from_path(path)
    if section_prefix is None:
        return False, {"skipped": "non-section-file"}

    starts = line_starts(text)
    anchors = collect_caption_anchors(text, starts)
    if not anchors:
        return False, {"skipped": "no-captions"}

    # Build per-kind document-order lists.
    by_kind = defaultdict(list)  # kind -> list of anchor indices
    for idx, a in enumerate(anchors):
        by_kind[a[2]].append(idx)

    # Group lettered consecutive runs.
    # anchor_to_group: idx -> group_id
    anchor_to_group = {}
    groups = []  # list of dict(kind, members=[anchor_idx], first_pos)
    for kind, idx_list in by_kind.items():
        idx_list.sort(key=lambda i: anchors[i][0])
        current_id = None
        for i in idx_list:
            pos, end, k, base, letter, ln = anchors[i]
            if (current_id is not None
                    and groups[current_id]["kind"] == kind
                    and anchors[groups[current_id]["members"][-1]][3] == base
                    and letter
                    and anchors[groups[current_id]["members"][-1]][4]):
                # extend
                groups[current_id]["members"].append(i)
            else:
                current_id = len(groups)
                groups.append({"kind": kind, "members": [i], "first_pos": pos})
            anchor_to_group[i] = current_id

    # Assign sequence numbers per kind in document order of first_pos.
    groups_in_doc_order = sorted(range(len(groups)),
                                 key=lambda g: groups[g]["first_pos"])
    new_seq_by_kind = defaultdict(int)
    group_new_base = {}  # group_id -> new_base
    for gid in groups_in_doc_order:
        g = groups[gid]
        new_seq_by_kind[g["kind"]] += 1
        group_new_base[gid] = f'{section_prefix}.{new_seq_by_kind[g["kind"]]}'

    # Compute the rename map for prose / img-alt: (kind, old_label) -> new_label.
    # If the same (kind, old_label) maps to multiple new_labels (because the
    # same old caption number appears in 2+ groups), mark as ambiguous.
    rename_map = {}
    # Base-only map: (kind, old_base) -> new_base.  Lets us rename "sibling"
    # letter-suffixed prose refs (e.g. "Figure 20.1.1b" when only the "a"
    # variant has an actual caption) so the prose still belongs to the same
    # series.  Same ambiguity rule applies.
    base_rename_map = {}
    ambiguous = set()
    base_ambiguous = set()
    for gid, g in enumerate(groups):
        for i in g["members"]:
            _, _, kind, base, letter, _ = anchors[i]
            old_label = base + letter
            new_label = group_new_base[gid] + letter
            key = (kind, old_label)
            if key in rename_map and rename_map[key] != new_label:
                ambiguous.add(key)
            else:
                rename_map[key] = new_label
            bkey = (kind, base)
            new_base = group_new_base[gid]
            if bkey in base_rename_map and base_rename_map[bkey] != new_base:
                base_ambiguous.add(bkey)
            else:
                base_rename_map[bkey] = new_base

    # Build per-anchor new labels.
    anchor_new_label = {}
    for gid, g in enumerate(groups):
        for i in g["members"]:
            _, _, kind, base, letter, _ = anchors[i]
            anchor_new_label[i] = group_new_base[gid] + letter

    # Pass 1: emit text with all GENERIC_REF_RE matches.
    # For each generic match, decide:
    #   - If it overlaps a known caption anchor, use that anchor's new label.
    #   - Else (prose/alt), look up rename_map; if ambiguous, leave unchanged.
    # Build an index from generic match position -> anchor index (if caption).
    # We use the fact that CAP_NUM_RE is a STRICTER prefix of GENERIC_REF_RE.
    # An anchor's match position equals the position of the "Figure" or
    # "Code Fragment" word inside the <strong>...</strong>.  The generic
    # regex finds the same word.  We map by (start_kind, start_byte_of_kind_word).
    # Compute that mapping using anchors.
    # Find for each anchor, the position of the kind word.  The CAP_NUM_RE
    # match starts at "<strong>"; the actual kind word starts at the first
    # alpha after "<strong>".  We just re-scan each anchor's slice.
    anchor_kind_word_pos = {}
    for i, (pos, end, kind, base, letter, ln) in enumerate(anchors):
        # Inside text[pos:end], find the position of the kind word.
        slice_text = text[pos:end]
        wm = re.search(r'(Figure|Code Fragment)', slice_text)
        if wm:
            anchor_kind_word_pos[i] = pos + wm.start()

    pos_to_anchor = {v: k for k, v in anchor_kind_word_pos.items()}

    skipped_ambiguous = defaultdict(int)
    n_caption_subs = 0
    n_prose_subs = 0
    n_unchanged = 0

    def replace(m):
        nonlocal n_caption_subs, n_prose_subs, n_unchanged
        kind = m.group("kind")
        base = m.group("base")
        letter = m.group("letter") or ""
        old_label = base + letter
        key = (kind, old_label)
        anchor_idx = pos_to_anchor.get(m.start())
        if anchor_idx is not None:
            new_label = anchor_new_label[anchor_idx]
            if new_label != old_label:
                n_caption_subs += 1
            else:
                n_unchanged += 1
            return f"{kind} {new_label}"
        # Prose / img-alt path.
        if key in ambiguous:
            skipped_ambiguous[key] += 1
            n_unchanged += 1
            return m.group(0)
        if key in rename_map:
            new_label = rename_map[key]
            if new_label != old_label:
                n_prose_subs += 1
            else:
                n_unchanged += 1
            return f"{kind} {new_label}"
        # Fallback: if the base has a known rename (from a sibling letter
        # variant), apply the base rename and keep the letter.  This catches
        # orphan prose refs like "Figure 20.1.1b" when only "20.1.1a" exists
        # as a caption.
        if letter:
            bkey = (kind, base)
            if bkey not in base_ambiguous and bkey in base_rename_map:
                new_base = base_rename_map[bkey]
                if new_base != base:
                    n_prose_subs += 1
                    return f"{kind} {new_base}{letter}"
        n_unchanged += 1
        return m.group(0)

    new_text = GENERIC_REF_RE.sub(replace, text)

    any_change = (n_caption_subs + n_prose_subs) > 0

    stats = {
        "anchors": len(anchors),
        "groups": len(groups),
        "caption_subs": n_caption_subs,
        "prose_subs": n_prose_subs,
        "ambiguous": dict(skipped_ambiguous),
    }

    if verbose:
        for gid, g in enumerate(groups):
            for i in g["members"]:
                _, _, kind, base, letter, ln = anchors[i]
                old = base + letter
                new = group_new_base[gid] + letter
                if old != new:
                    print(f"  L{ln}  {kind} {old} -> {kind} {new}")
        if skipped_ambiguous:
            for key, cnt in skipped_ambiguous.items():
                print(f"  AMBIGUOUS (skipped {cnt} prose ref(s)): {key[0]} {key[1]}")

    if not dry_run and any_change:
        path.write_text(new_text, encoding="utf-8")

    return any_change, stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("paths", nargs="*",
                        help="Section files (default: all section-*.html)")
    args = parser.parse_args()

    if args.paths:
        files = [Path(p).resolve() for p in args.paths]
    else:
        files = sorted(ROOT.rglob("section-*.html"))
        skip = ("node_modules", "_archive", "vendor", "temp_epub",
                "_concept-figs", "_html2epub_cache", "downloads", "pagefind",
                "KDP")  # KDP/build/source_fix_backups holds historical snapshots
        files = [f for f in files if not any(s in f.parts for s in skip)]

    total_files = 0
    changed_files = 0
    total_caption = 0
    total_prose = 0
    total_ambig = 0
    for f in files:
        changed, stats = renumber_file(f, dry_run=args.dry_run, verbose=args.verbose)
        total_files += 1
        if changed:
            changed_files += 1
            total_caption += stats.get("caption_subs", 0)
            total_prose += stats.get("prose_subs", 0)
            total_ambig += sum(stats.get("ambiguous", {}).values())
            rel = f.relative_to(ROOT) if str(ROOT) in str(f) else f
            print(f"{rel}: caption={stats.get('caption_subs', 0)} "
                  f"prose={stats.get('prose_subs', 0)} "
                  f"ambig-skip={sum(stats.get('ambiguous', {}).values())} "
                  f"groups={stats.get('groups', 0)}")

    print()
    print(f"Files scanned: {total_files}")
    print(f"Files changed: {changed_files}")
    print(f"Caption renumbers: {total_caption}")
    print(f"Prose ref renumbers: {total_prose}")
    print(f"Ambiguous prose refs (left untouched): {total_ambig}")


if __name__ == "__main__":
    main()
