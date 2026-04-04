#!/usr/bin/env python3
"""Fix caption numbering across all section-*.html files.

Changes bare sequential numbers like 'Code Fragment 1:' to section-aligned
numbers like 'Code Fragment 4.2.1:'. Also adds Figure numbering to
unnumbered <figcaption> elements, respecting existing numbered figures.
"""

import re
import os
import glob

ROOT = r"E:\Projects\LLMCourse"


def extract_section_id(filepath):
    """Extract section identifier from filename like section-4.2.html -> '4.2'."""
    basename = os.path.basename(filepath)
    m = re.match(r"section-([a-zA-Z]?\d*\.?\d+)\.html", basename)
    if not m:
        return None
    sec = m.group(1)
    # Uppercase letter prefixes for appendices: a.1 -> A.1
    if sec[0].isalpha():
        sec = sec[0].upper() + sec[1:]
    return sec


def process_file(filepath):
    """Process a single file. Returns (changed, stats_dict)."""
    sec_id = extract_section_id(filepath)
    if sec_id is None:
        return False, {}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    stats = {"code_fragments_renumbered": 0, "figures_added": 0, "refs_updated": 0}

    # --- Phase 1: Collect all captions in document order to build numbering ---
    # We need to do a single pass to:
    # 1. Renumber bare Code Fragments
    # 2. Count existing figures and add numbers to unnumbered figcaptions

    # --- Code Fragments ---
    # Pattern for bare numbered code fragments: Code Fragment N:
    # But NOT already section-aligned like Code Fragment 4.2.1:
    # We match "Code Fragment" followed by a bare integer (no dots)
    code_frag_counter = 0

    def renumber_code_fragment(m):
        nonlocal code_frag_counter
        code_frag_counter += 1
        old_num = m.group(1)
        new_label = f"Code Fragment {sec_id}.{code_frag_counter}:"
        stats["code_fragments_renumbered"] += 1
        return f"{m.group(0)[:m.start(1)-m.start()]}{new_label}"

    # Replace bare Code Fragment N: in code-caption divs
    # Match: <strong>Code Fragment N:</strong> where N is a bare integer
    bare_code_pattern = re.compile(
        r'(<div class="code-caption"><strong>)Code Fragment (\d+):(</strong>)'
    )

    # Also handle Code Fragment N: that might already be section-aligned
    # We only want to replace bare integers (no dots)
    code_frag_counter = 0

    def replace_code_caption(m):
        nonlocal code_frag_counter
        code_frag_counter += 1
        prefix = m.group(1)
        suffix = m.group(3)
        stats["code_fragments_renumbered"] += 1
        return f"{prefix}Code Fragment {sec_id}.{code_frag_counter}:{suffix}"

    content = bare_code_pattern.sub(replace_code_caption, content)

    # --- Build in-text reference mapping ---
    # We know how many code fragments were renumbered, build old->new map
    ref_map = {}
    for i in range(1, code_frag_counter + 1):
        ref_map[str(i)] = f"{sec_id}.{i}"

    # Update in-text references like "Code Fragment 2 below" or "Code Fragment 2,"
    # But NOT inside <strong> tags (already handled above)
    # Match "Code Fragment N" where N is bare integer, not followed by a dot+digit
    if ref_map:
        def replace_ref(m):
            old_num = m.group(1)
            if old_num in ref_map:
                stats["refs_updated"] += 1
                return f"Code Fragment {ref_map[old_num]}"
            return m.group(0)

        # Only replace references that are NOT inside <strong> tags
        # and where N is a bare integer not already section-aligned
        ref_pattern = re.compile(r'(?<!<strong>)Code Fragment (\d+)(?!\.\d)(?!:</)')
        content = ref_pattern.sub(replace_ref, content)

    # --- Figures ---
    # Count existing numbered figures (in diagram-caption and figcaption)
    # and add numbers to unnumbered figcaptions
    # We need to process in document order

    # Find all figure-related elements in order
    fig_counter = 0

    # Pattern for already-numbered figures in diagram-caption
    diagram_fig_pattern = re.compile(
        rf'<div class="diagram-caption">Figure {re.escape(sec_id)}\.(\d+):'
    )
    # Pattern for already-numbered figures in figcaption
    figcaption_numbered_pattern = re.compile(
        rf'<figcaption>Figure {re.escape(sec_id)}\.(\d+):'
    )
    # Pattern for already-numbered figures in figcaption with <strong>
    figcaption_strong_numbered_pattern = re.compile(
        rf'<figcaption><strong>Figure {re.escape(sec_id)}\.(\d+)</strong>'
    )

    # Pattern for unnumbered figcaptions (no "Figure X.Y.N:" prefix)
    # Must not start with "Figure"
    figcaption_unnumbered_pattern = re.compile(
        r'<figcaption>(?!Figure \S+[\.:])(?!<strong>Figure )(.+?)</figcaption>',
        re.DOTALL
    )

    # We need to process all these in document order
    # Build a list of (position, type, match) tuples
    events = []

    for m in diagram_fig_pattern.finditer(content):
        events.append((m.start(), "numbered", m))

    for m in figcaption_numbered_pattern.finditer(content):
        events.append((m.start(), "numbered", m))

    for m in figcaption_strong_numbered_pattern.finditer(content):
        events.append((m.start(), "numbered_strong", m))

    for m in figcaption_unnumbered_pattern.finditer(content):
        events.append((m.start(), "unnumbered", m))

    events.sort(key=lambda x: x[0])

    # Deduplicate overlapping positions (same match counted twice)
    seen_positions = set()
    deduped_events = []
    for pos, typ, m in events:
        if pos not in seen_positions:
            seen_positions.add(pos)
            deduped_events.append((pos, typ, m))
    events = deduped_events

    # Now process: count numbered ones, assign numbers to unnumbered ones
    fig_counter = 0
    replacements = []  # (start, end, new_text)

    for pos, typ, m in events:
        if typ in ("numbered", "numbered_strong"):
            fig_num = int(m.group(1))
            fig_counter = max(fig_counter, fig_num)
        elif typ == "unnumbered":
            fig_counter += 1
            old_text = m.group(0)
            caption_text = m.group(1)
            new_text = f"<figcaption>Figure {sec_id}.{fig_counter}: {caption_text}</figcaption>"
            replacements.append((m.start(), m.end(), new_text))
            stats["figures_added"] += 1

    # Apply replacements in reverse order to preserve positions
    for start, end, new_text in reversed(replacements):
        content = content[:start] + new_text + content[end:]

    changed = content != original
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return changed, stats


def main():
    # Find all section-*.html files
    patterns = [
        os.path.join(ROOT, "**", "section-*.html"),
    ]

    all_files = set()
    for pattern in patterns:
        all_files.update(glob.glob(pattern, recursive=True))

    all_files = sorted(all_files)
    print(f"Found {len(all_files)} section files to process")

    total_changed = 0
    total_code = 0
    total_figs = 0
    total_refs = 0

    for filepath in all_files:
        changed, stats = process_file(filepath)
        if changed:
            total_changed += 1
            cf = stats.get("code_fragments_renumbered", 0)
            fa = stats.get("figures_added", 0)
            ru = stats.get("refs_updated", 0)
            total_code += cf
            total_figs += fa
            total_refs += ru
            rel = os.path.relpath(filepath, ROOT)
            parts = []
            if cf:
                parts.append(f"{cf} code fragments")
            if fa:
                parts.append(f"{fa} figures numbered")
            if ru:
                parts.append(f"{ru} refs updated")
            print(f"  {rel}: {', '.join(parts)}")

    print(f"\nSummary:")
    print(f"  Files changed: {total_changed}")
    print(f"  Code fragments renumbered: {total_code}")
    print(f"  Figures numbered: {total_figs}")
    print(f"  In-text references updated: {total_refs}")


if __name__ == "__main__":
    main()
