"""Phase 4: rewrite chapter/section numbers INSIDE renamed section files.

After phase 2 renamed module dirs and section file slugs, every file's
internal content still references the OLD chapter number in:
  - <title>Section X.Y: Title</title>
  - <meta description "Section X.Y: ...">
  - <h1>...</h1> (h1 itself usually has the title, not number — fine)
  - <div class="page-current">Section X.Y</div>
  - <div class="page-breadcrumb">... Chapter X: Title ... </div>
  - <span data-pagefind-meta="chapter:Chapter X: Title">
  - <span data-pagefind-meta="part:Part roman: Title">
  - <h2 id="X-Y-Z-...">X.Y.Z Subsection Title</h2>
  - <h3 id="X-Y-Z-A-...">X.Y.Z.A Sub-subsection Title</h3>
  - same-folder hrefs like href="section-X.Y.html" (these go to the new
    slug, so they need rewrite)
  - chapter-nav prev/next links inside the file
  - Code/Table/Figure caption labels like "Code Fragment X.Y.Z"

Reads the migration map, iterates over each renamed module, computes
the (old_ch, new_ch) for that module, applies a two-pass rename:
  Pass 1: Replace 'X.' with '__TMP_X__.' for every old chapter number
          where X is BOTH a source AND somebody else's target.
  Pass 2: Replace placeholders with their targets.

Idempotent: a file already containing new chapter numbers will be
unchanged.

DRY-RUN by default; --apply to execute.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP = HERE / "migration-map.json"


def build_chapter_renumber_map(data: dict) -> dict[int, int]:
    """Build dict: old_chapter_num -> new_chapter_num for all renamed modules.

    Only includes modules whose CHAPTER NUM changed (e.g., 40 -> 42).
    Same-number renames (module-X-old-slug -> module-X-new-slug) excluded.
    """
    out: dict[int, int] = {}
    for src, dst in data["module_renames"].items():
        old_m = re.match(r".*/module-(\d+)-", src)
        new_m = re.match(r".*/module-(\d+)-", dst)
        if not (old_m and new_m):
            continue
        old_n = int(old_m.group(1))
        new_n = int(new_m.group(1))
        if old_n != new_n:
            out[old_n] = new_n
    return out


def rewrite_file(path: Path, old_ch: int, new_ch: int, full_renumber: dict[int, int], dry_run: bool) -> int:
    """Rewrite numeric prefixes inside `path` from old_ch to new_ch.

    Returns count of replacements. The two-pass placeholder pattern handles
    chains like 40->42 AND 42->44 by tagging all old-keys with placeholders
    in pass 1, then mapping placeholders to new values in pass 2.

    `full_renumber` is the dict mapping old_chapter -> new_chapter for ALL
    renamed modules (needed for chain-safe rewrite).
    """
    text = path.read_text(encoding="utf-8")
    orig = text

    # === Pass 1: turn every old chapter number reference into a placeholder ===
    # Patterns to catch (chapter num appears as X. or X-):
    #
    # Section X.Y: ... ; Chapter X: ... ; X.Y.Z ; section-X.Y.html ; section-X-Y-Z (id) ;
    # "Chapter X" alone (in prose / nav) ; pagefind-meta chapter:Chapter X: ...
    #
    # For two-pass safety: turn each old chapter number into "__CHN__" first,
    # then map all "__CHN__" tokens to their new values.

    pairs_to_apply = sorted(full_renumber.items(), key=lambda x: -x[0])  # process larger numbers first

    # Pass 1: source -> placeholder
    # Match the chapter number when:
    #   - "Chapter X" (word boundary on both sides)
    #   - "Section X.Y" (where the X is followed by a dot + digit)
    #   - "section-X.Y.html"
    #   - "section-X-Y-..." (id form)
    #   - "X.Y.Z" caption prefix (CodeFragment / Figure / Table / Listing)
    #   - "module-XX-" in href

    # Build a SINGLE regex that finds chapter-number anchors safely.
    # We don't want to touch random "40" in prose; only when it's a chapter ref.

    # The patterns where chapter num is meaningful:
    # 1. "Chapter N" (with capital C, word-boundary N)
    # 2. "Section N." (specifically Section, capital S, before dot+digit)
    # 3. "section-N." (in slug)
    # 4. "section-N-" (in id slug)
    # 5. ">N.M<" (raw heading text like h2>40.1)
    # 6. "Code Fragment N.M.K:"
    # 7. "Figure N.M.K"
    # 8. "Table N.M.K"
    # 9. "Listing N.M.K"
    # 10. "module-NN-" in href
    # 11. data-pagefind-meta="chapter:Chapter N: Title"

    for old_n in [old for old, _ in pairs_to_apply]:
        placeholder = f"__CH_{old_n}__"
        # Use raw text replace where unambiguous; regex where context-sensitive.
        # Apply only within this file if it's part of a module that's part of the renumber
        # (caller has already filtered to per-file).
        patterns = [
            (rf"\bChapter {old_n}\b", placeholder),
            (rf"\bSection {old_n}\.", f"__S_{old_n}_DOT__"),
            (rf"\bsection-{old_n}\.", f"__SF_{old_n}_DOT__"),
            (rf"\bsection-{old_n}-", f"__SF_{old_n}_DASH__"),
            (rf"\bmodule-{old_n}-", f"__M_{old_n}_DASH__"),
            (rf"\bCode Fragment {old_n}\.", f"__CF_{old_n}_DOT__"),
            (rf"\bFigure {old_n}\.", f"__FIG_{old_n}_DOT__"),
            (rf"\bTable {old_n}\.", f"__TBL_{old_n}_DOT__"),
            (rf"\bListing {old_n}\.", f"__LST_{old_n}_DOT__"),
            # Inside h2/h3 raw "<h2>40.1 Title</h2>" form (any heading)
            (rf"(<h[234][^>]*>){old_n}\.", rf"\1__H_{old_n}_DOT__"),
            (rf"(<h[234][^>]*>){old_n}\s", rf"\1__H_{old_n}_SPACE__"),
        ]
        for pat, repl in patterns:
            text = re.sub(pat, repl, text)

    # Pass 2: placeholder -> new
    for old_n, new_n in pairs_to_apply:
        text = text.replace(f"__CH_{old_n}__", f"Chapter {new_n}")
        text = text.replace(f"__S_{old_n}_DOT__", f"Section {new_n}.")
        text = text.replace(f"__SF_{old_n}_DOT__", f"section-{new_n}.")
        text = text.replace(f"__SF_{old_n}_DASH__", f"section-{new_n}-")
        text = text.replace(f"__M_{old_n}_DASH__", f"module-{new_n}-")
        text = text.replace(f"__CF_{old_n}_DOT__", f"Code Fragment {new_n}.")
        text = text.replace(f"__FIG_{old_n}_DOT__", f"Figure {new_n}.")
        text = text.replace(f"__TBL_{old_n}_DOT__", f"Table {new_n}.")
        text = text.replace(f"__LST_{old_n}_DOT__", f"Listing {new_n}.")
        text = text.replace(f"__H_{old_n}_DOT__", f"{new_n}.")
        text = text.replace(f"__H_{old_n}_SPACE__", f"{new_n} ")

    if text != orig:
        if not dry_run:
            path.write_text(text, encoding="utf-8")
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    renumber = build_chapter_renumber_map(data)
    print(f"=== Phase 4: rewrite in-file chapter/section numbers ===")
    print(f"Chapter number renumbering map:")
    for k, v in sorted(renumber.items()):
        print(f"  {k:>3} -> {v:>3}")
    print()

    # Walk every renamed module's contents (and the modules themselves
    # since they were already renamed by phase 2). For each file in a
    # renamed module, run rewrite using the SINGLE pair for that module.
    # But also: the file may reference OTHER renumbered chapters in
    # cross-refs. So we need to apply ALL pairs to every file.
    SKIP = {"node_modules", ".git", "KDP", "build", "temp_ebook",
            "temp_epub", "source_fix_backups", "pagefind", "templates",
            ".claude", ".book-update", "vendor", "docs"}

    edited = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        # Only consider files in renumbered modules to limit scope at this
        # phase. (Phase 5 will do the book-wide cross-link rewrite.)
        rel = p.relative_to(ROOT).as_posix()
        # The renamed modules are the destinations in data["module_renames"]
        in_renamed = any(rel.startswith(dst + "/") for dst in data["module_renames"].values())
        if not in_renamed:
            continue
        # Determine the file's CURRENT chapter number from its directory slug
        m = re.search(r"module-(\d+)-", rel)
        if not m:
            continue
        cur_ch = int(m.group(1))
        # The file's CONTENT may still have OLD chapter num. Find the
        # corresponding old_ch for this destination.
        # Build inverse map: new_ch -> old_ch.
        inv = {v: k for k, v in renumber.items()}
        old_ch = inv.get(cur_ch)
        if old_ch is None:
            # Module name unchanged (e.g., module-34 retitled but kept number),
            # or destination not in renumber set. Skip in-place rewrite.
            continue
        # Run rewrite (using FULL renumber map so cross-references also rewrite)
        n = rewrite_file(p, old_ch, cur_ch, renumber, dry_run)
        if n:
            edited += 1

    print(f"=== Summary ===")
    print(f"Files edited: {edited}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
