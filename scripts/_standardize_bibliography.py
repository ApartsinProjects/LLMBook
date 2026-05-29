#!/usr/bin/env python3
"""Standardize bibliography callouts across the book.

Idempotent: re-running is a no-op.

Operations:
  1. Label canonicalization:
       <details class="bibliography-collapsible">
         <summary><strong>X</strong></summary>
     where X in {Bibliography, Core References, References, ...} ->
       <summary><strong>Further Reading</strong></summary>
     Exception: "Bibliography: the durable venues" (section-65.5) is a unique
     structural label tied to the H2 heading; left alone.

  2. Card-format conversion: inside the bibliography <section>, plain
     <ul><li>...</li></ul> lists are converted to a series of
     <div class="bib-entry-card"><div class="bib-ref">...</div></div> blocks.
     Paragraph pairs of (<p class="bib-ref">...) (<p class="bib-annotation">...)
     are also wrapped into bib-entry-card blocks.

  3. Old <ul class="bibliography"> outside any <details> wrapper: removed when
     it duplicates a sibling <details class="bibliography-collapsible">; otherwise
     wrapped into the collapsible details format.

  4. Position-to-last: the bibliography <details> block must be the LAST
     content block before <nav class="chapter-nav">. If anything (whats-next,
     fun-note, self-check, exercise, etc.) follows the bibliography, the
     bibliography block is moved to right before <nav class="chapter-nav">.
     Skip files where the bibliography is structurally part of section
     content (section-65.5 unique label; section-24.5 with merged-section
     divider after bib).

The script prints per-category counts and the final delta.
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude",
    ".book-update", ".html2epub_cache", "_archive", "scripts", "agents",
    "styles", "images", "__pycache__", "vendor", "_concept-figs",
    "tmp_whats_next", "downloads",
}

CANONICAL_LABEL = "Further Reading"

# Files where the bibliography is structurally embedded in section content
# and must NOT be moved to the end of the page.
NO_MOVE_FILES = {
    Path("part-12-frontiers/module-65-tools-of-the-trade/section-65.5.html"),
    Path("part-5-retrieval-conversation/module-24-conversational-ai/section-24.5.html"),
}

# Labels that should NOT be renamed to "Further Reading" (preserve structural labels).
PRESERVE_LABELS = {
    "Bibliography: the durable venues",
}


# ── File collection ────────────────────────────────────────────────────────

def collect_files() -> list[Path]:
    results = []
    for dirpath, dirnames, filenames in os.walk(BOOK_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".html"):
                results.append(Path(dirpath) / f)
    return sorted(results)


def relative(path: Path) -> Path:
    try:
        return path.relative_to(BOOK_ROOT)
    except ValueError:
        return path


# ── Regex patterns ─────────────────────────────────────────────────────────

DETAILS_BIB_OPEN = re.compile(r'<details\s+class="bibliography-collapsible"[^>]*>', re.IGNORECASE)
DETAILS_BIB_BLOCK = re.compile(
    r'<details\s+class="bibliography-collapsible"[^>]*>.*?</details>',
    re.DOTALL | re.IGNORECASE,
)
SUMMARY_PAT = re.compile(r'(<summary[^>]*>\s*<strong>)(.*?)(</strong>\s*</summary>)',
                         re.DOTALL | re.IGNORECASE)
SECTION_BIB_PAT = re.compile(r'<section\s+class="bibliography"[^>]*>(.*?)</section>',
                             re.DOTALL | re.IGNORECASE)
NAV_CHAPTER_PAT = re.compile(r'<nav\s+class="chapter-nav"', re.IGNORECASE)
UL_BIB_PAT = re.compile(r'<ul\s+class="bibliography"[^>]*>.*?</ul>',
                        re.DOTALL | re.IGNORECASE)
BIB_ENTRY_CARD_PAT = re.compile(r'<div\s+class="bib-entry-card"', re.IGNORECASE)
UL_OPEN_PAT = re.compile(r'<ul[^>]*>', re.IGNORECASE)
LI_PAT = re.compile(r'<li[^>]*>(.*?)</li>', re.DOTALL | re.IGNORECASE)
P_BIBREF_PAT = re.compile(r'<p\s+class="bib-ref"[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)
P_BIBANN_PAT = re.compile(r'<p\s+class="bib-annotation"[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)

# Block that constitutes a "callout" placed after bibliography (would trigger move).
# Includes:
#   - <div class="callout ...">
#   - <div class="whats-next">
#   - bare <h2>What Comes Next</h2> / <h2>What's Next</h2> (used in part-11 instead
#     of a whats-next div)
POST_BIB_BLOCK = re.compile(
    r'<div\s+class="(?:callout\s+[^"]+|whats-next)"'
    r'|<h2[^>]*>\s*(?:What(?:\s+Comes|&#39;s|’s)?\s+Next|What\'s\s+Next)\s*</h2>',
    re.IGNORECASE,
)

# Legacy <div class="bibliography"> (NOT class="callout bibliography") — old
# format that pre-dates the current convention. Reported as anomaly but not
# modified, because in observed cases the content differs from the sibling
# <details class="bibliography-collapsible"> and merging risks content loss.
LEGACY_DIV_BIB_PAT = re.compile(r'<div\s+class="bibliography"(?!\w)', re.IGNORECASE)


# ── Transformations ────────────────────────────────────────────────────────

def normalize_summary_label(text: str) -> tuple[str, int]:
    """Rewrite <summary><strong>X</strong></summary> to canonical label.

    Returns (new_text, n_renamed).
    """
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        prefix, label, suffix = m.group(1), m.group(2), m.group(3)
        plain = re.sub(r"<[^>]+>", "", label).strip()
        if plain in PRESERVE_LABELS:
            return m.group(0)
        if plain == CANONICAL_LABEL:
            return m.group(0)
        n += 1
        return f"{prefix}{CANONICAL_LABEL}{suffix}"

    # Only operate on summaries inside <details class="bibliography-collapsible">.
    def block_repl(bm: re.Match) -> str:
        return SUMMARY_PAT.sub(repl, bm.group(0))

    new_text = DETAILS_BIB_BLOCK.sub(block_repl, text)
    return new_text, n


def _convert_li_to_cards(ul_html: str) -> str:
    """Convert a single <ul>...</ul> string into a sequence of bib-entry-card divs."""
    parts = []
    for m in LI_PAT.finditer(ul_html):
        inner = m.group(1).strip()
        # Wrap the entire li content as bib-ref
        parts.append(
            f'<div class="bib-entry-card">\n'
            f'<div class="bib-ref">{inner}</div>\n'
            f'</div>'
        )
    return "\n".join(parts)


def _convert_p_pairs_to_cards(section_inner: str) -> tuple[str, int]:
    """Convert <p class="bib-ref">...</p>[<p class="bib-annotation">...</p>] pairs
    into bib-entry-card blocks. Returns (new_inner, n_converted)."""
    # Tokenize: walk paragraphs in order and pair bib-ref with optional next
    # bib-annotation. Anything else passes through unchanged.
    # We do this with a single regex over the section_inner string, in order.
    pattern = re.compile(
        r'<p\s+class="bib-ref"[^>]*>(?P<ref>.*?)</p>'
        r'(?:\s*<p\s+class="bib-annotation"[^>]*>(?P<ann>.*?)</p>)?',
        re.DOTALL | re.IGNORECASE,
    )
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        ref = m.group("ref").strip()
        ann = (m.group("ann") or "").strip()
        out = f'<div class="bib-entry-card">\n<div class="bib-ref">{ref}</div>'
        if ann:
            out += f'\n<div class="bib-annotation">{ann}</div>'
        out += "\n</div>"
        return out

    new_inner = pattern.sub(repl, section_inner)
    return new_inner, n


def convert_section_to_cards(text: str) -> tuple[str, int]:
    """Inside each <section class="bibliography">...</section> within a
    bibliography-collapsible block, convert any plain <ul><li>...</li></ul>
    or <p class="bib-ref"> pairs into bib-entry-card divs.

    Returns (new_text, n_files_with_conversions) — actually counts the total
    number of conversions per call, not per file.
    """
    n_ul_converted = 0
    n_p_converted = 0

    def section_repl(secm: re.Match) -> str:
        nonlocal n_ul_converted, n_p_converted
        full = secm.group(0)
        inner = secm.group(1)

        # First convert <p class="bib-ref"> pairs
        new_inner, np = _convert_p_pairs_to_cards(inner)
        n_p_converted += np

        # Then handle <ul>...</ul> blocks. Use a stateful regex:
        # match outermost <ul>...</ul>; convert if it doesn't already contain bib-entry-card.
        def ul_repl(um: re.Match) -> str:
            nonlocal n_ul_converted
            ul_html = um.group(0)
            if "bib-entry-card" in ul_html:
                return ul_html
            # Replace this <ul>...</ul> with the cards
            cards = _convert_li_to_cards(ul_html)
            if not cards:
                return ul_html
            n_ul_converted += 1
            return cards

        # Find <ul>...</ul> blocks at the top level of this section. Use non-greedy.
        ul_block_pat = re.compile(r'<ul\b[^>]*>.*?</ul>', re.DOTALL | re.IGNORECASE)
        new_inner = ul_block_pat.sub(ul_repl, new_inner)

        # Reconstruct the section
        # secm.group(0) starts with <section ...> and ends with </section>
        opener_match = re.match(r'(<section\s+class="bibliography"[^>]*>)', full, re.IGNORECASE)
        opener = opener_match.group(1) if opener_match else '<section class="bibliography">'
        return f"{opener}{new_inner}</section>"

    # Only operate within a <details class="bibliography-collapsible"> block.
    def block_repl(bm: re.Match) -> str:
        return SECTION_BIB_PAT.sub(section_repl, bm.group(0))

    new_text = DETAILS_BIB_BLOCK.sub(block_repl, text)
    return new_text, n_ul_converted + n_p_converted


def remove_orphan_ul_bibliography(text: str) -> tuple[str, int]:
    """Remove <ul class="bibliography">...</ul> blocks that sit OUTSIDE any
    <details class="bibliography-collapsible"> wrapper, provided the file
    already contains a <details class="bibliography-collapsible"> sibling
    bibliography. (Duplicate cleanup.)

    Returns (new_text, n_removed).
    """
    n = 0
    if not DETAILS_BIB_OPEN.search(text):
        return text, 0

    # Find all UL bibliography matches and remove those not inside a details bib.
    # Build a list of details-block spans.
    details_spans = [(m.start(), m.end()) for m in DETAILS_BIB_BLOCK.finditer(text)]

    def is_inside_details(pos: int) -> bool:
        return any(s <= pos < e for s, e in details_spans)

    # Iterate (highest-position first to keep offsets stable on removal)
    matches = list(UL_BIB_PAT.finditer(text))
    if not matches:
        return text, 0

    new_text = text
    for m in reversed(matches):
        if is_inside_details(m.start()):
            continue
        # Remove the ul block (and a single trailing newline if present)
        start, end = m.start(), m.end()
        # consume one trailing newline
        if end < len(new_text) and new_text[end] == "\n":
            end += 1
        new_text = new_text[:start] + new_text[end:]
        n += 1
    return new_text, n


def move_bibliography_to_last(text: str, file_rel: Path) -> tuple[str, int]:
    """Move the <details class="bibliography-collapsible"> block to right
    before <nav class="chapter-nav"> if anything follows it.

    Returns (new_text, 0 or 1).
    """
    if file_rel in NO_MOVE_FILES:
        return text, 0

    bib_match = DETAILS_BIB_BLOCK.search(text)
    if not bib_match:
        return text, 0
    # If multiple, pick the LAST one (rare; warn in caller)
    all_bibs = list(DETAILS_BIB_BLOCK.finditer(text))
    if len(all_bibs) > 1:
        bib_match = all_bibs[-1]

    nav_match = NAV_CHAPTER_PAT.search(text, pos=bib_match.end())
    if not nav_match:
        # No chapter-nav after this bib; cannot move; leave alone.
        return text, 0

    # Check if any "callout" or "whats-next" sits between bib_end and nav_start.
    between = text[bib_match.end():nav_match.start()]
    if not POST_BIB_BLOCK.search(between):
        # Already last.
        return text, 0

    # Extract the bibliography block.
    bib_html = bib_match.group(0)
    # Remove from current position.
    before = text[:bib_match.start()]
    after = text[bib_match.end():]
    # Strip a trailing newline that may have followed bib in original.
    if after.startswith("\n"):
        after = after[1:]

    # Find the nav-chapter location in the new (joined) text.
    new_text_pre = before + after
    nav_re = re.compile(r'<nav\s+class="chapter-nav"', re.IGNORECASE)
    new_nav = nav_re.search(new_text_pre)
    if not new_nav:
        # Defensive: revert.
        return text, 0

    # Insert bib_html immediately before the nav line.
    # Strip any whitespace before the nav so we control spacing.
    insert_at = new_nav.start()
    # Trim any trailing whitespace before insert point (preserve one newline)
    head = new_text_pre[:insert_at]
    tail = new_text_pre[insert_at:]
    # Ensure exactly one newline between bib and nav
    head_stripped = head.rstrip(" \t\r\n")
    new_text_final = head_stripped + "\n" + bib_html + "\n" + tail
    return new_text_final, 1


# ── Per-file pipeline ──────────────────────────────────────────────────────

def process_file(path: Path) -> dict:
    rel = relative(path)
    original = path.read_text(encoding="utf-8", errors="replace")

    # Skip files with no bibliography indicator at all.
    has_bib = bool(DETAILS_BIB_OPEN.search(original) or UL_BIB_PAT.search(original))
    if not has_bib:
        return {"file": rel, "skipped": "no_bibliography"}

    text = original

    text, n_label = normalize_summary_label(text)
    text, n_cards = convert_section_to_cards(text)
    text, n_ulrm = remove_orphan_ul_bibliography(text)
    text, n_moved = move_bibliography_to_last(text, rel)

    has_legacy_div = bool(LEGACY_DIV_BIB_PAT.search(text))

    if text != original:
        path.write_text(text, encoding="utf-8")
        changed = True
    else:
        changed = False

    return {
        "file": rel,
        "changed": changed,
        "label_renames": n_label,
        "card_conversions": n_cards,
        "ul_orphan_removed": n_ulrm,
        "moved_to_last": n_moved,
        "has_legacy_div_bib": has_legacy_div,
    }


# ── Main ───────────────────────────────────────────────────────────────────

def main() -> int:
    files = collect_files()
    print(f"Scanning {len(files)} HTML files...")

    totals = {
        "files_with_bib": 0,
        "files_changed": 0,
        "label_renames": 0,
        "card_conversions": 0,
        "ul_orphan_removed": 0,
        "moved_to_last": 0,
    }
    changed_files: list[Path] = []
    legacy_div_files: list[Path] = []

    for f in files:
        result = process_file(f)
        if "skipped" in result:
            continue
        totals["files_with_bib"] += 1
        if result["changed"]:
            totals["files_changed"] += 1
            changed_files.append(result["file"])
        if result.get("has_legacy_div_bib"):
            legacy_div_files.append(result["file"])
        for k in ("label_renames", "card_conversions", "ul_orphan_removed", "moved_to_last"):
            totals[k] += result[k]

    print()
    print("=" * 72)
    print("  Bibliography standardization summary")
    print("=" * 72)
    print(f"  Files scanned:              {len(files)}")
    print(f"  Files with bibliography:    {totals['files_with_bib']}")
    print(f"  Files changed (this run):   {totals['files_changed']}")
    print(f"  Label renames:              {totals['label_renames']}")
    print(f"  Card conversions:           {totals['card_conversions']}")
    print(f"  Orphan <ul> bibs removed:   {totals['ul_orphan_removed']}")
    print(f"  Moved to last:              {totals['moved_to_last']}")
    print()
    print(f"  Canonical label: \"{CANONICAL_LABEL}\"")
    print(f"  Files skipped from move:    {len(NO_MOVE_FILES)}")
    for p in sorted(NO_MOVE_FILES):
        print(f"    - {p}")
    print(f"  Labels preserved (not renamed):")
    for lab in sorted(PRESERVE_LABELS):
        print(f"    - {lab!r}")
    if legacy_div_files:
        print(f"  Legacy <div class=\"bibliography\"> blocks (NOT modified, content-loss risk):")
        for p in sorted(legacy_div_files):
            print(f"    - {p}")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
