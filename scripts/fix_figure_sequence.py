"""Fix figure and code fragment sequence numbering across the book.

For each HTML file, renumber Figure X.Y.Z and Code Fragment X.Y.Z
captions and references so they appear in sequential order (1, 2, 3, ...)
matching their document order.

Skips _archive/ and agents/ directories.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

BOOK_ROOT = Path(r"E:\Projects\LLMCourse")
SKIP_DIRS = {"vendor", "node_modules", ".git", "deprecated", "__pycache__", "_archive", "agents"}

# Matches captions like <strong>Figure 0.1.3</strong> or <strong>Code Fragment 9.1.2:</strong>
CAPTION_RE = re.compile(
    r"(<strong>\s*(?:Figure|Code Fragment)\s+)(\d+\.\d+)\.(\d+)(\s*[:</strong>])",
    re.IGNORECASE,
)

# Matches any mention of Figure X.Y.Z or Code Fragment X.Y.Z in text
REF_RE = re.compile(
    r"((?:Figure|Code Fragment)\s+)(\d+\.\d+)\.(\d+)",
    re.IGNORECASE,
)


def find_html_files():
    for f in BOOK_ROOT.rglob("*.html"):
        if any(s in f.parts for s in SKIP_DIRS):
            continue
        yield f


def get_caption_order(html):
    """Extract caption entries in document order, grouped by (kind, prefix).

    Returns: dict of (kind_lower, prefix) -> [(seq_int, line_idx, kind_original)]
    """
    groups = defaultdict(list)
    lines = html.split("\n")
    for i, line in enumerate(lines):
        for m in CAPTION_RE.finditer(line):
            full_prefix_text = m.group(1)  # e.g. "<strong>Figure " or "<strong>Code Fragment "
            kind = "figure" if "figure" in full_prefix_text.lower() else "code fragment"
            prefix = m.group(2)  # e.g. "0.1"
            seq = int(m.group(3))  # e.g. 3
            groups[(kind, prefix)].append((seq, i))
    return groups


def build_remap(groups):
    """Build old->new mapping for each (kind, prefix) group.

    Returns: dict of (kind_lower, prefix) -> {old_seq: new_seq}
    Only includes groups that need changes.
    """
    remaps = {}
    for key, entries in groups.items():
        # entries are already in document order (by line index)
        # Assign new sequential numbers 1, 2, 3, ...
        mapping = {}
        for new_seq, (old_seq, _line_idx) in enumerate(entries, 1):
            if old_seq != new_seq:
                mapping[old_seq] = new_seq
        if mapping:
            # But we also need to note identity mappings for conflict resolution
            full_mapping = {}
            for new_seq, (old_seq, _) in enumerate(entries, 1):
                full_mapping[old_seq] = new_seq
            remaps[key] = full_mapping
    return remaps


def apply_remap(html, remaps):
    """Apply renumbering to all figure/code fragment references in the HTML.

    Uses a two-pass approach: first replace with temp placeholders, then
    replace placeholders with final numbers (to avoid chain replacements).
    """
    if not remaps:
        return html

    # Build a lookup: (kind_lower, prefix, old_seq_str) -> new_seq_str
    lookup = {}
    for (kind, prefix), mapping in remaps.items():
        for old_seq, new_seq in mapping.items():
            lookup[(kind, prefix, str(old_seq))] = str(new_seq)

    # Pass 1: Replace old numbers with unique placeholders
    placeholder_map = {}
    counter = [0]

    def make_placeholder(kind, prefix, new_seq_str):
        counter[0] += 1
        ph = f"__FIGFIX_{counter[0]}__"
        placeholder_map[ph] = new_seq_str
        return ph

    def replacer(m):
        full_text = m.group(0)
        prefix_text = m.group(1)  # "Figure " or "Code Fragment "
        prefix = m.group(2)       # "0.1"
        seq_str = m.group(3)      # "3"

        kind = "figure" if "figure" in prefix_text.lower() else "code fragment"
        key = (kind, prefix, seq_str)
        if key in lookup:
            ph = make_placeholder(kind, prefix, lookup[key])
            return f"{prefix_text}{prefix}.{ph}"
        return full_text

    result = REF_RE.sub(replacer, html)

    # Pass 2: Replace placeholders with final numbers
    for ph, new_seq in placeholder_map.items():
        result = result.replace(ph, new_seq)

    return result


def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    files_changed = 0
    total_remaps = 0

    for filepath in sorted(find_html_files()):
        try:
            html = filepath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"WARNING: Cannot read {filepath}: {e}", file=sys.stderr)
            continue

        groups = get_caption_order(html)
        remaps = build_remap(groups)

        if not remaps:
            continue

        rel = filepath.relative_to(BOOK_ROOT)
        num_changes = sum(
            sum(1 for old, new in mapping.items() if old != new)
            for mapping in remaps.values()
        )
        total_remaps += num_changes

        if verbose or dry_run:
            print(f"\n{rel}:")
            for (kind, prefix), mapping in sorted(remaps.items()):
                changes = [(old, new) for old, new in sorted(mapping.items()) if old != new]
                if changes:
                    for old, new in changes:
                        kname = kind.title()
                        print(f"  {kname} {prefix}.{old} -> {kname} {prefix}.{new}")

        if not dry_run:
            new_html = apply_remap(html, remaps)
            if new_html != html:
                filepath.write_text(new_html, encoding="utf-8")
                files_changed += 1
                if not verbose:
                    print(f"  Fixed {rel} ({num_changes} renumberings)")

    action = "Would fix" if dry_run else "Fixed"
    print(f"\n{action} {total_remaps} numbering issues across {files_changed if not dry_run else 'N/A'} files.")


if __name__ == "__main__":
    main()
