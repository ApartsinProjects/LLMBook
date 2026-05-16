"""Normalize chapter-end callout layout book-wide.

Three issues this script fixes (all stemming from the same root cause:
ad-hoc trailing-block layout when authoring agents appended blocks
without enforcing canonical order):

1. **Bibliography misplaced**: <div class="callout bibliography"> sometimes
   appears AFTER <div class="whats-next">. Bibliography is reference
   material that belongs BEFORE the forward-thread block.

2. **Learning Objectives in all caps**: <div class="objectives"><h3>...</h3>
   has CSS text-transform:uppercase. Standardize to canonical
   <div class="callout pathway"><div class="callout-title">Learning
   Objectives</div> form (which renders Title Case via .callout-title).
   Same for <div class="prereqs"> -> <div class="callout note"> titled
   "Prerequisites".

3. **Lab / Bibliography / section-grid after What's Next**: any HTML
   block sitting between </div> (closing whats-next) and <nav class=
   "chapter-nav"> (the bottom-nav) is in the wrong place. Reorder so
   whats-next is the LAST block before chapter-nav. Everything else
   moves to BEFORE whats-next.

Canonical chapter-end order:
   [sections list / chapter content]
   [section-grid for lab section card, if any]
   [callout bibliography]
   [other callouts like exercise / self-check]
   <div class="whats-next">...</div>
   <nav class="chapter-nav">...</nav>
   <footer>...</footer>

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}


# Phase A: <div class="objectives"> -> <div class="callout pathway">
# Phase B: <div class="prereqs">    -> <div class="callout note">
def phase_ab_legacy_to_callouts(text: str) -> tuple[str, int]:
    n = 0

    # objectives -> pathway (Learning Objectives)
    def conv_obj(m: re.Match) -> str:
        nonlocal n
        inner = m.group(1)
        # Strip inner <h3>...</h3> heading (it duplicates the callout title)
        inner = re.sub(r"\s*<h3>[^<]*</h3>\s*", "\n", inner, count=1)
        n += 1
        return ('<div class="callout pathway">\n'
                '<div class="callout-title">Learning Objectives</div>'
                + inner + '</div>')
    text = re.sub(
        r'<div class="objectives">([\s\S]*?)</div>',
        conv_obj, text,
    )

    # prereqs -> note (Prerequisites)
    def conv_pre(m: re.Match) -> str:
        nonlocal n
        inner = m.group(1)
        inner = re.sub(r"\s*<h3>[^<]*</h3>\s*", "\n", inner, count=1)
        n += 1
        return ('<div class="callout note">\n'
                '<div class="callout-title">Prerequisites</div>'
                + inner + '</div>')
    text = re.sub(
        r'<div class="prereqs">([\s\S]*?)</div>',
        conv_pre, text,
    )

    return text, n


# Phase C: Move any non-whitespace block sitting between </div> (closing
# whats-next) and <nav class="chapter-nav"> to BEFORE the <div class=
# "whats-next">.
WHATS_NEXT_RE = re.compile(
    r'(<div class="whats-next">[\s\S]*?</div>)',
)
NAV_RE = re.compile(r'<nav class="chapter-nav"')


def phase_c_reorder_whats_next(text: str) -> tuple[str, int]:
    """If there's content between the whats-next block and the
    chapter-nav, move it before whats-next."""
    n = 0
    while True:
        m = WHATS_NEXT_RE.search(text)
        if not m:
            break
        wn_start, wn_end = m.start(), m.end()
        nav_match = NAV_RE.search(text, wn_end)
        if not nav_match:
            break
        nav_start = nav_match.start()
        between = text[wn_end:nav_start]
        # Trim leading/trailing whitespace; check if there's any
        # non-comment, non-whitespace content
        stripped = re.sub(r"<!--[\s\S]*?-->", "", between).strip()
        if not stripped:
            # Nothing to move; remove the comment-only / whitespace-only
            # leftover to avoid re-detecting
            if between != "\n":
                text = text[:wn_end] + "\n" + text[nav_start:]
            break
        # Move 'between' (with its comments preserved) to BEFORE the
        # whats-next block
        wn_block = text[wn_start:wn_end]
        new_text = (
            text[:wn_start]
            + between.strip()
            + "\n"
            + wn_block
            + "\n"
            + text[nav_start:]
        )
        if new_text == text:
            break
        text = new_text
        n += 1
        # One iteration moves all between content in one shot; break
        break
    return text, n


# Phase D: Convert <h3>Title</h3> inside `<div class="callout XXX">` blocks
# to canonical `<div class="callout-title">Title</div>`. Avoid touching
# blocks that already have a callout-title div.
CALLOUT_OPEN_RE = re.compile(
    r'(<div class="callout [a-z-]+">\s*)<h3>([^<]+)</h3>'
)


def phase_d_normalize_callout_titles(text: str) -> tuple[str, int]:
    n = 0
    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        title = m.group(2).strip()
        # Title-case if all-caps; otherwise leave the author's choice
        if title.isupper() and len(title) > 3:
            title = title.title()
        return f'{m.group(1)}<div class="callout-title">{title}</div>'
    text = CALLOUT_OPEN_RE.sub(repl, text)

    # Also normalize callout-title contents that are ALL-CAPS
    def norm_title(m: re.Match) -> str:
        nonlocal n
        body = m.group(1)
        if body.isupper() and len(body) > 3:
            n += 1
            return f'<div class="callout-title">{body.title()}</div>'
        return m.group(0)
    text = re.sub(
        r'<div class="callout-title">([^<]+)</div>',
        norm_title, text,
    )
    return text, n


# Phase E: Strip empty bibliography placeholder comments.
def phase_e_strip_empty_bib_comments(text: str) -> tuple[str, int]:
    new_text, n = re.subn(
        r"\s*<!--\s*bibliography skipped:[^>]*-->\s*",
        "\n",
        text,
    )
    return new_text, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    totals = {"phase_ab": 0, "phase_c": 0, "phase_d": 0, "phase_e": 0}
    files_edited = 0

    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        text, n_ab = phase_ab_legacy_to_callouts(text)
        text, n_c = phase_c_reorder_whats_next(text)
        text, n_d = phase_d_normalize_callout_titles(text)
        text, n_e = phase_e_strip_empty_bib_comments(text)

        totals["phase_ab"] += n_ab
        totals["phase_c"] += n_c
        totals["phase_d"] += n_d
        totals["phase_e"] += n_e

        if text != orig:
            files_edited += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Phase A/B (legacy -> callout):     {totals['phase_ab']}")
    print(f"Phase C (reorder whats-next):      {totals['phase_c']}")
    print(f"Phase D (normalize titles):        {totals['phase_d']}")
    print(f"Phase E (strip empty bib stubs):   {totals['phase_e']}")
    print(f"Files edited:                      {files_edited}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
