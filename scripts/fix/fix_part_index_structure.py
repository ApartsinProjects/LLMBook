#!/usr/bin/env python3
"""Fix part index.html files to match the standard structure:

    Epigraph > Part Image Opener > Part Overview > Big Picture > Chapters > What's Next

Two fixes applied:
1. Swap Big Picture and Part Overview if Big Picture comes first (wrong order).
2. Add a placeholder epigraph after </header> if none exists.

Usage:
    python fix_part_index_structure.py          # dry run (report only)
    python fix_part_index_structure.py --fix     # apply changes
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(r"E:/Projects/LLMCourse")

PART_DIRS = [
    "part-1-foundations",
    "part-2-understanding-llms",
    "part-3-working-with-llms",
    "part-4-training-adapting",
    "part-5-retrieval-conversation",
    "part-6-agentic-ai",
    "part-7-multimodal-applications",
    "part-8-evaluation-production",
    "part-9-safety-strategy",
    "part-10-frontiers",
    "part-11-idea-to-product",
]

EPIGRAPH_PLACEHOLDER = """\
<blockquote class="epigraph">
    <p>TODO: Add part epigraph</p>
    <cite>A Thoughtful AI Agent</cite>
</blockquote>"""

# Regex patterns (DOTALL so . matches newlines)
RE_BIG_PICTURE = re.compile(
    r'(<div\s+class="callout\s+big-picture">.*?</div>)\s*',
    re.DOTALL,
)
RE_PART_OVERVIEW = re.compile(
    r'(<div\s+class="part-overview">.*?</div>)\s*',
    re.DOTALL,
)
RE_EPIGRAPH = re.compile(r'<blockquote\s+class="epigraph">')


def fix_file(path: Path, apply: bool) -> list[str]:
    """Return list of actions taken (or that would be taken)."""
    html = path.read_text(encoding="utf-8")
    original = html
    actions: list[str] = []

    # --- 1. Ensure Part Overview comes BEFORE Big Picture ---
    m_bp = RE_BIG_PICTURE.search(html)
    m_ov = RE_PART_OVERVIEW.search(html)

    if m_bp and m_ov:
        if m_bp.start() < m_ov.start():
            # Big Picture appears before Overview: swap them
            bp_block = m_bp.group(0)
            ov_block = m_ov.group(0)

            # Strategy: remove both blocks, then insert overview then big-picture
            # at the position of whichever came first.
            insert_pos = m_bp.start()

            # Remove the later block first (so positions stay valid)
            html = html[: m_ov.start()] + html[m_ov.end() :]
            # Now remove the earlier block (big-picture)
            html = html[: m_bp.start()] + html[m_bp.end() :]

            # Compute proper indentation from context
            replacement = ov_block.rstrip() + "\n\n" + bp_block.rstrip() + "\n\n"
            html = html[:insert_pos] + replacement + html[insert_pos:]

            actions.append("Swapped: moved Part Overview before Big Picture")
        else:
            actions.append("Order OK: Part Overview already before Big Picture")
    elif m_bp and not m_ov:
        actions.append("WARNING: Big Picture found but no Part Overview block")
    elif m_ov and not m_bp:
        actions.append("WARNING: Part Overview found but no Big Picture block")
    else:
        actions.append("WARNING: Neither Part Overview nor Big Picture found")

    # --- 2. Add placeholder epigraph after </header> if missing ---
    if RE_EPIGRAPH.search(html):
        actions.append("Epigraph already present")
    else:
        # Insert after closing </header> tag
        header_end = html.find("</header>")
        if header_end != -1:
            insert_at = header_end + len("</header>")
            # Preserve the newline(s) after </header>, then inject epigraph
            html = (
                html[:insert_at]
                + "\n\n"
                + EPIGRAPH_PLACEHOLDER
                + "\n"
                + html[insert_at:]
            )
            actions.append("Added placeholder epigraph after </header>")
        else:
            actions.append("WARNING: No </header> tag found, cannot add epigraph")

    # --- Write if changed ---
    if apply and html != original:
        path.write_text(html, encoding="utf-8")
        actions.append("FILE WRITTEN")

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix part index.html structure")
    parser.add_argument(
        "--fix", action="store_true", help="Apply changes (default is dry run)"
    )
    args = parser.parse_args()

    mode = "FIX" if args.fix else "DRY RUN"
    print(f"=== Part Index Structure Fixer ({mode}) ===\n")

    total_swaps = 0
    total_epigraphs = 0

    for dirname in PART_DIRS:
        path = ROOT / dirname / "index.html"
        if not path.exists():
            print(f"  MISSING: {path}")
            continue

        actions = fix_file(path, apply=args.fix)
        print(f"  {dirname}/index.html")
        for a in actions:
            print(f"    - {a}")
            if "Swapped" in a:
                total_swaps += 1
            if "Added placeholder epigraph" in a:
                total_epigraphs += 1
        print()

    print(f"Summary: {total_swaps} order swaps, {total_epigraphs} epigraphs added")
    if not args.fix and (total_swaps > 0 or total_epigraphs > 0):
        print("Re-run with --fix to apply changes.")


if __name__ == "__main__":
    main()
