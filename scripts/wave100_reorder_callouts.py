"""Wave 100: Reorder out-of-order singleton callouts to canonical positions.

The CALLOUT_ORDER audit flags singletons that appear out of canonical
order (e.g. key-takeaway after self-check, lab after key-takeaway).
The fix is a mechanical block swap: extract the misplaced block,
re-insert it before the block that should come after it.

Canonical order:
  big-picture -> prerequisites -> lab -> key-takeaway -> self-check ->
  exercises -> whats-next -> bibliography

Approach: for each file, find every singleton block with its start
and end byte offsets. If two blocks are out of order, swap them.
Repeat until stable. Single block per category; if there are
duplicates we skip the file (the consolidator wave handles those).

A "block" is the div opening tag through the matching closing </div>,
or for exercises/bibliography their wrapping section/details element.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

# Ordered list. Tuple: (name, opening pattern, kind)
# kind = "div"     -> match opening <div> and find matching </div>
#      = "section" -> match opening <section> and find matching </section>
#      = "details" -> match opening <details> and find matching </details>
SINGLETONS = [
    ("big-picture",   r'<div\s+class="callout big-picture"', "div"),
    ("prerequisites", r'<div\s+class="prerequisites"',       "div"),
    ("lab",           r'<div\s+class="callout lab"',         "div"),
    ("key-takeaway",  r'<div\s+class="callout key-takeaway"', "div"),
    ("self-check",    r'<div\s+class="callout self-check"',  "div"),
    ("exercises",     r'<section\s+class="exercises"',       "section"),
    ("whats-next",    r'<div\s+class="(?:callout\s+)?whats-next"', "div"),
    ("bibliography",  r'<details\s+class="bibliography-collapsible', "details"),
]

ORDER_INDEX = {name: i for i, (name, _, _) in enumerate(SINGLETONS)}


def find_matching_close(text: str, start: int, tag: str) -> int:
    """Given an opening tag at position start, find matching close.
    Returns the position AFTER the closing tag, or -1."""
    open_re = re.compile(rf'<{tag}\b', re.IGNORECASE)
    close_re = re.compile(rf'</{tag}>', re.IGNORECASE)
    depth = 1
    pos = start
    # Skip the opening tag's '>' first
    gt = text.find('>', start)
    if gt < 0:
        return -1
    pos = gt + 1
    while depth > 0 and pos < len(text):
        next_open = open_re.search(text, pos)
        next_close = close_re.search(text, pos)
        if not next_close:
            return -1
        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            pos = next_close.end()
    return pos if depth == 0 else -1


def find_blocks(text: str) -> list[dict]:
    """For each singleton in canonical order, locate its first occurrence
    in `text` and return [{name, start, end, idx}] sorted by start."""
    blocks: list[dict] = []
    for name, pat, kind in SINGLETONS:
        regex = re.compile(pat, re.IGNORECASE)
        # First occurrence only (singletons)
        matches = list(regex.finditer(text))
        if len(matches) != 1:
            # If 0, the section just doesn't have this callout. Skip.
            # If >1, duplicates exist — bail; we don't want to touch.
            if len(matches) > 1:
                return []  # signal "skip this file"
            continue
        m = matches[0]
        end = find_matching_close(text, m.start(), kind)
        if end < 0:
            return []
        # Include trailing newline if present
        if end < len(text) and text[end] == "\n":
            end += 1
        blocks.append({
            "name": name,
            "start": m.start(),
            "end": end,
            "idx": ORDER_INDEX[name],
        })
    blocks.sort(key=lambda b: b["start"])
    return blocks


def reorder_once(text: str) -> tuple[str, bool]:
    """Find first out-of-order singleton pair and swap. Return new text
    and True if a swap was made."""
    blocks = find_blocks(text)
    if not blocks:
        return text, False
    # Find first pair where current block has a higher idx than its successor
    for i in range(len(blocks) - 1):
        a = blocks[i]
        b = blocks[i + 1]
        if a["idx"] > b["idx"]:
            # Swap a and b: extract a's content and b's content, reinsert
            # in reversed order at a's original start position. Anything
            # between them (other prose / headings) MUST be preserved
            # between the two.
            content_a = text[a["start"]:a["end"]]
            content_b = text[b["start"]:b["end"]]
            between = text[a["end"]:b["start"]]
            new_text = (
                text[:a["start"]]
                + content_b
                + between
                + content_a
                + text[b["end"]:]
            )
            return new_text, True
    return text, False


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    n = 0
    max_iter = 20
    for _ in range(max_iter):
        new_text, swapped = reorder_once(text)
        if not swapped:
            break
        text = new_text
        n += 1
    if n == 0:
        return 0
    p.write_text(text, encoding="utf-8")
    return n


def main():
    n_files = n_total = 0
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_total += n
            print(f"  + {p.relative_to(ROOT)}: {n} swap(s)")
    print(f"\nFiles touched: {n_files}, swaps: {n_total}")


if __name__ == "__main__":
    main()
