"""Wave 101: Move misplaced singleton callouts to canonical positions
when the exercises anchor is an <h2 id="exercises"> (not a <section
class="exercises"> wrapper).

Wave 100 only knows about <section class="exercises">. The audit also
accepts <h2 id="exercises"> as the exercises anchor; many sections use
this h2-only form. For those sections, Wave 100 cannot fix the
ordering: it would swap the misplaced singleton with the h2 line and
leave the exercise content stranded.

Strategy here is different from Wave 100. Instead of swapping two
singletons, we MOVE each misplaced singleton block to just before the
exercises_h2 anchor (preserving the exercise content as a contiguous
trailing region). Order:
  big-picture -> prerequisites -> lab -> key-takeaway -> self-check ->
  exercises -> whats-next -> bibliography

For each file:
1. Find the exercises anchor (exercises_h2 or exercises_section).
2. For each pre-exercises singleton (lab, key-takeaway, self-check)
   that currently appears AFTER the exercises anchor, extract its
   block and re-insert it just before the anchor.
3. Within the relocated pre-exercises group, ensure their pairwise
   order is canonical (lab < key-takeaway < self-check) — this part
   is handled by a final pass of Wave 100's logic on the result.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

# Patterns mirroring the audit's check definitions.
SINGLE_PATTERNS = {
    "big-picture":      (r'<div\s+class="callout big-picture"',         "div"),
    "prerequisites":    (r'<div\s+class="prerequisites"',                "div"),
    "lab":              (r'<div\s+class="callout lab"',                  "div"),
    "key-takeaway":     (r'<div\s+class="callout key-takeaway"',         "div"),
    "self-check":       (r'<div\s+class="callout self-check"',           "div"),
    "exercises_section":(r'<section\s+class="exercises"',                "section"),
    "exercises_h2":     (r'<h2\s+id="exercises"',                        "h2"),
    "whats-next":       (r'<div\s+class="(?:callout\s+)?whats-next"',    "div"),
    "bibliography":     (r'<details\s+class="bibliography-collapsible',  "details"),
}

# Canonical positional index; both exercises forms map to idx 5.
ORDER_IDX = {
    "big-picture": 0,
    "prerequisites": 1,
    "lab": 2,
    "key-takeaway": 3,
    "self-check": 4,
    "exercises_section": 5,
    "exercises_h2": 5,
    "whats-next": 6,
    "bibliography": 7,
}

PRE_EXERCISES = ("lab", "key-takeaway", "self-check")


def find_matching_close(text: str, start: int, tag: str) -> int:
    """Return position AFTER the matching closing tag, or -1.

    For self-closing-style anchors (h2), return position after </h2>;
    h2 has no nesting in practice."""
    open_re = re.compile(rf'<{tag}\b', re.IGNORECASE)
    close_re = re.compile(rf'</{tag}>', re.IGNORECASE)
    depth = 1
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


def first_match(text: str, name: str):
    """Return (start, end) of first occurrence of singleton `name`, or None.

    Returns None if zero matches OR more than one match (duplicates).
    The caller decides what to do with duplicates separately."""
    pat, tag = SINGLE_PATTERNS[name]
    matches = list(re.finditer(pat, text, re.IGNORECASE))
    if len(matches) != 1:
        return None
    m = matches[0]
    end = find_matching_close(text, m.start(), tag)
    if end < 0:
        return None
    if end < len(text) and text[end] == "\n":
        end += 1
    return (m.start(), end)


def relocate_block(text: str, src_range, target_pos):
    """Cut text[src_range[0]:src_range[1]] and paste it at target_pos.

    target_pos must be OUTSIDE src_range (typically before src_range[0])
    in the ORIGINAL coordinate system. Returns new text and the new
    position of the relocated block's start.
    """
    s, e = src_range
    assert target_pos <= s or target_pos >= e, "overlapping move"
    if target_pos <= s:
        # paste then remove the original
        new_text = (
            text[:target_pos]
            + text[s:e]
            + text[target_pos:s]
            + text[e:]
        )
        return new_text, target_pos
    else:  # target_pos >= e
        new_text = (
            text[:s]
            + text[e:target_pos]
            + text[s:e]
            + text[target_pos:]
        )
        return new_text, target_pos - (e - s)


def fix_exercises_h2_misorder(text: str):
    """If the exercises anchor is an h2 and any of lab/key-takeaway/
    self-check appears AFTER it, move those blocks to just BEFORE the
    h2. Returns (new_text, list_of_actions)."""
    actions = []
    # First, locate the exercises anchor (prefer section over h2; h2 if no section).
    sec = first_match(text, "exercises_section")
    h2 = first_match(text, "exercises_h2")
    if sec:
        anchor_start, anchor_end = sec
        anchor_kind = "exercises_section"
    elif h2:
        anchor_start, anchor_end = h2
        anchor_kind = "exercises_h2"
    else:
        return text, actions  # no exercises -> nothing to do

    # For each pre-exercises singleton, check if it appears AFTER the anchor.
    # We iterate by name, since pairwise misorder is reported one block at a time.
    # Repeat until stable.
    for _ in range(10):
        # re-locate the anchor (may have shifted after a relocation)
        sec = first_match(text, "exercises_section")
        h2 = first_match(text, "exercises_h2")
        if sec:
            anchor_start, anchor_end = sec
        elif h2:
            anchor_start, anchor_end = h2
        else:
            break

        moved_any = False
        for name in PRE_EXERCISES:
            blk = first_match(text, name)
            if blk is None:
                continue
            s, e = blk
            if s > anchor_start:
                # Move this block to just before anchor_start.
                # Make sure we don't slice mid-line; anchor_start is the
                # opening "<" of the anchor tag. We paste right at
                # anchor_start so the new block ends with newline before <.
                text, new_pos = relocate_block(text, (s, e), anchor_start)
                actions.append(f"move {name} (offset {s} -> {new_pos}) before "
                               f"{anchor_kind} anchor")
                moved_any = True
                # restart from updated text/anchor
                break
        if not moved_any:
            break
    return text, actions


def reorder_within_pre_exercises(text: str):
    """After relocation, ensure that lab < key-takeaway < self-check
    among the singletons that exist. We swap pairs (idx-bigger before
    idx-smaller) like Wave 100 does."""
    actions = []
    target_order = ["big-picture", "prerequisites", "lab", "key-takeaway", "self-check"]
    for _ in range(15):
        positions = []
        for name in target_order:
            blk = first_match(text, name)
            if blk:
                positions.append((name, blk))
        positions.sort(key=lambda x: x[1][0])
        # Find any pair where actual order differs from target_order index
        actual_indices = [target_order.index(name) for name, _ in positions]
        swap_i = None
        for i in range(len(actual_indices) - 1):
            if actual_indices[i] > actual_indices[i + 1]:
                swap_i = i
                break
        if swap_i is None:
            break
        a_name, (a_s, a_e) = positions[swap_i]
        b_name, (b_s, b_e) = positions[swap_i + 1]
        # swap: like Wave 100
        content_a = text[a_s:a_e]
        content_b = text[b_s:b_e]
        between = text[a_e:b_s]
        text = text[:a_s] + content_b + between + content_a + text[b_e:]
        actions.append(f"swap {a_name} <-> {b_name}")
    return text, actions


def fix_file(p: Path):
    text = p.read_text(encoding="utf-8")
    orig = text
    all_actions = []

    text, actions = fix_exercises_h2_misorder(text)
    all_actions.extend(actions)

    text, actions = reorder_within_pre_exercises(text)
    all_actions.extend(actions)

    if text != orig:
        p.write_text(text, encoding="utf-8")
        return all_actions
    return []


def main():
    files = [
        # files with no duplicate singletons; just need exercises_h2 reorder
        "part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html",
        "part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html",
        "part-14-designing-llm-agent-products/module-70-shipping-products/section-70.3.html",
        "part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.4.html",
        "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html",
        "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html",
        "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html",
        "part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html",
        "part-6-agentic-ai/module-26-ai-agents/section-26.4.html",
        "part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.1.html",
        "part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.2.html",
    ]
    total = 0
    n_files = 0
    for f in files:
        p = ROOT / f
        actions = fix_file(p)
        if actions:
            n_files += 1
            total += len(actions)
            print(f"+ {f}")
            for a in actions:
                print(f"    {a}")
        else:
            print(f"- {f}: no change")
    print(f"\nFiles touched: {n_files}, total actions: {total}")


if __name__ == "__main__":
    main()
