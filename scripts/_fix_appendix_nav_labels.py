"""Fix the appendix-letter labels in appendices/index.html and toc.html so
they match the on-disk directory letter (which is authoritative).

In appendices/index.html each chapter-card looks like:

    <div class="chapter-card-header">
      <span class="mod-num">Appendix X</span> Title text
    </div>
    <div class="chapter-card-body">
      <p>...</p>
      <p><a href="appendix-y-slug/index.html">Read Appendix X →</a></p>
    </div>

When X != y (case-insensitive), this script changes both X labels to match y.

For toc.html, the `#toc-detailed` block contains lines like:

    <a href="appendices/appendix-y-slug/section-y.N.html">X.N Title</a>

where the X prefix in the link text drifts from y. Replace prefix X with y.

Idempotent. Skip the Glossary (no appendix letter).
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fix_appendices_index(dry_run: bool) -> tuple[int, list[str]]:
    p = ROOT / "appendices" / "index.html"
    text = p.read_text(encoding="utf-8")
    orig = text
    messages: list[str] = []

    # Walk every chapter-card block and rewrite labels if mismatched.
    # Use regex over a coarse window: from `<div class="chapter-card">` to its
    # matching `</div></div></div>` (the standard 3-closing pattern in the
    # existing file). Simpler approach: find all (mod_num_letter, dir_letter)
    # pairs by anchoring on `<span class="mod-num">Appendix X</span>` and the
    # closest following `appendix-y-` href.
    card_pat = re.compile(
        r'(<span class="mod-num">Appendix\s+([A-Z]+)</span>[\s\S]*?'
        r'href="(appendix-([a-z])-[^"/]+/[^"]+)")',
        re.M,
    )

    def fix_card(m: re.Match) -> str:
        whole, mod_letter, href, dir_letter = m.group(1), m.group(2), m.group(3), m.group(4).upper()
        if mod_letter == dir_letter:
            return whole
        # Replace the first Appendix <X> in the captured group
        new = whole.replace(
            f"Appendix {mod_letter}</span>",
            f"Appendix {dir_letter}</span>",
            1,
        )
        messages.append(f"  card '{mod_letter}' -> '{dir_letter}' (href {href[:50]}...)")
        return new

    text = card_pat.sub(fix_card, text)

    # Also fix the "Read Appendix X" link text inside each card body. Walk each
    # card href and rewrite the surrounding "Read Appendix X →" text.
    read_pat = re.compile(
        r'<a href="(appendix-([a-z])-[^"/]+/[^"]+)">Read Appendix\s+([A-Z]+)\s*&rarr;\s*</a>',
        re.I,
    )

    def fix_read_link(m: re.Match) -> str:
        href, dir_letter, label_letter = m.group(1), m.group(2).upper(), m.group(3)
        if label_letter == dir_letter:
            return m.group(0)
        messages.append(f"  'Read Appendix {label_letter}' -> 'Read Appendix {dir_letter}'")
        return f'<a href="{href}">Read Appendix {dir_letter} &rarr;</a>'

    text = read_pat.sub(fix_read_link, text)

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return (1 if text != orig else 0), messages


def fix_toc_detailed(dry_run: bool) -> tuple[int, list[str]]:
    """Fix toc.html `#toc-detailed` link labels whose prefix letter drifted
    from the on-disk file's letter."""
    p = ROOT / "toc.html"
    text = p.read_text(encoding="utf-8")
    orig = text
    messages: list[str] = []

    # Match: <a href="appendices/appendix-y-slug/section-y.N.html">X.M Title</a>
    # where X may have drifted from Y. Replace prefix X with Y (uppercased).
    pat = re.compile(
        r'<a href="(appendices/appendix-([a-z])-[^"/]+/section-[a-z](\.\d+)?\.html)">\s*([A-Z]+)(\.\d+(?:\.\d+)*)\s+([^<]+?)</a>'
    )

    def fix(m: re.Match) -> str:
        href, dir_letter, _, label_letter, rest_num, title = (
            m.group(1), m.group(2).upper(), m.group(3), m.group(4), m.group(5), m.group(6)
        )
        if label_letter == dir_letter:
            return m.group(0)
        messages.append(f"  TOC '{label_letter}{rest_num}' -> '{dir_letter}{rest_num}'")
        return f'<a href="{href}">{dir_letter}{rest_num} {title}</a>'

    text = pat.sub(fix, text)

    # Also catch appendix-landing links: <a href="appendices/appendix-y-slug/index.html">Appendix X: Title</a>
    pat2 = re.compile(
        r'<a href="(appendices/appendix-([a-z])-[^"/]+/index\.html)">\s*Appendix\s+([A-Z]+)\s*:\s*([^<]+?)</a>'
    )

    def fix2(m: re.Match) -> str:
        href, dir_letter, label_letter, title = (
            m.group(1), m.group(2).upper(), m.group(3), m.group(4)
        )
        if label_letter == dir_letter:
            return m.group(0)
        messages.append(f"  TOC landing 'Appendix {label_letter}' -> 'Appendix {dir_letter}'")
        return f'<a href="{href}">Appendix {dir_letter}: {title}</a>'

    text = pat2.sub(fix2, text)

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return (1 if text != orig else 0), messages


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n1, msgs1 = fix_appendices_index(args.dry_run)
    if msgs1:
        print("appendices/index.html:")
        for m in msgs1:
            print(m)
    n2, msgs2 = fix_toc_detailed(args.dry_run)
    if msgs2:
        print("toc.html:")
        for m in msgs2:
            print(m)
    total = len(msgs1) + len(msgs2)
    print(f"\nTOTAL: {total} nav label fixes across {n1 + n2} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
