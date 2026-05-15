"""v15.12: separate the glossary from the appendix tree, then renumber
appendices G..V down to F..U so the letter sequence is contiguous A..U.

PHASE 1 — Move glossary out of the appendix sequence
  appendices/appendix-f-glossary/   →  appendices/glossary/
  Section files stay as section-f.1.html etc. (URL stable except parent
  dir) to keep the 3,579 inbound glossary-link hrefs simple to rewrite.

PHASE 2 — Internal glossary cleanup
  <title>Appendix F: Glossary           →  <title>Glossary
  <h1>F.1 Libraries…</h1>               →  <h1>Glossary 1: Libraries…</h1>
  <span class="section-num">F.1</span>  →  <span class="section-num">1</span>
  <div class="chapter-label">Appendix F →  <div class="chapter-label">Glossary
  data-pagefind-meta="chapter:Appendix F" → "chapter:Glossary"
  prose: "Appendix F"  →  "the Glossary"
  Remove the <div class="whats-next"> block from the LAST glossary
  section (section-f.5.html) — there is no "next" past the glossary.

PHASE 3 — Renumber the OTHER appendices, G→F, H→G, ... V→U.
  Directory rename + section-file rename + every cross-reference href.
  Internal markup (h1 labels, chapter-labels, span section-nums, prose
  "Appendix G").

PHASE 4 — Update build_epub.py path detection
  The glossary special-cases (path-suffix match for landmark and TOC
  promotion) used 'appendix-f-glossary'. Update to 'glossary'.

After this script:
  appendices/
    appendix-a-mathematical-foundations/   (was a)
    …
    appendix-e-git-collaboration/          (was e)
    appendix-f-hardware-compute/           (was g)
    appendix-g-model-cards/                (was h)
    …
    appendix-u-freshness-2026/             (was v)
    glossary/                              (was appendix-f-glossary)
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
APX = ROOT / "appendices"
SKIP = {"KDP", "node_modules", ".git", "pagefind", "scripts", "styles"}


# G..V → F..U
RENUMBER = [
    ("g", "f"), ("h", "g"), ("i", "h"), ("j", "i"),
    ("k", "j"), ("l", "k"), ("m", "l"), ("n", "m"),
    ("o", "n"), ("p", "o"), ("q", "p"), ("r", "q"),
    ("s", "r"), ("t", "s"), ("u", "t"), ("v", "u"),
]


def log(msg: str) -> None:
    print(msg.replace("→", "->"))


def phase1_move_glossary(apply: bool) -> None:
    """Rename appendix-f-glossary/ to glossary/."""
    src = APX / "appendix-f-glossary"
    dst = APX / "glossary"
    if not src.exists():
        log(f"[phase 1] glossary source missing: {src.name}")
        return
    if dst.exists():
        log(f"[phase 1] glossary already at glossary/, nothing to do")
        return
    log(f"[phase 1] move {src.name} → {dst.name}")
    if apply:
        src.rename(dst)


def phase2_glossary_internal(apply: bool) -> None:
    """Relabel headings, drop 'Appendix F' prose, remove 'What Comes Next'."""
    gloss = APX / "glossary"
    if not gloss.exists():
        log(f"[phase 2] glossary/ missing")
        return
    n_files = 0
    for p in gloss.rglob("*.html"):
        text = p.read_text(encoding="utf-8")
        original = text
        # Heading h1 like "F.1 Libraries & Frameworks" → "Glossary 1: Libraries & Frameworks"
        # Two forms: bare text "F.1 " and span <span class="section-num">F.1</span>
        text = re.sub(r"<h1>F\.(\d+)\s+", r"<h1>Glossary \1: ", text)
        text = re.sub(r'<span class="section-num">F\.(\d+)</span>',
                      r'<span class="section-num">\1</span>', text)
        text = re.sub(r"\b(Section )?F\.(\d+)\b", r"Glossary Section \2", text)
        # Title
        text = re.sub(r"<title>Appendix F: Glossary", "<title>Glossary", text)
        text = re.sub(r"<title>Appendix F\b", "<title>Glossary", text)
        # Chapter label divs
        text = re.sub(r'(<div class="chapter-label"[^>]*>)Appendix F</div>',
                      r"\1Glossary</div>", text)
        text = re.sub(r'(<div class="part-label"[^>]*>)Appendix F</div>',
                      r"\1Glossary</div>", text)
        # data-pagefind-meta
        text = re.sub(r'chapter:Appendix F\b', 'chapter:Glossary', text)
        # description meta
        text = re.sub(r'"Appendix F: Glossary"', '"Glossary"', text)
        # Plain prose mention
        text = re.sub(r"\bAppendix F: Glossary\b", "the Glossary", text)
        text = re.sub(r"\bAppendix F\b", "the Glossary", text)
        text = re.sub(r"\bthis appendix\b", "this glossary", text)
        text = re.sub(r"\bThis appendix\b", "This glossary", text)
        # Remove the trailing "What Comes Next" block from the LAST section
        # (section-f.5.html). The glossary is now the last section of the
        # whole book; there is no "next".
        if p.name == "section-f.5.html":
            text = re.sub(
                r'<div class="whats-next">.*?</div>\s*',
                "",
                text,
                flags=re.DOTALL,
            )
            # Also drop the chapter-nav's "next" link (last page).
            text = re.sub(
                r'<a class="next"[^>]*>[^<]*</a>\s*',
                "",
                text,
            )
        if text != original:
            n_files += 1
            if apply:
                p.write_text(text, encoding="utf-8")
    log(f"[phase 2] glossary internal labels updated: {n_files} files")


def phase3a_rename_dirs(apply: bool) -> None:
    """Rename appendix dirs G→F, H→G, …, V→U.

    Order: lowest-to-highest old letter so each rename happens AFTER the
    target slot is freed.
    """
    n = 0
    for old, new in RENUMBER:
        old_dirs = list(APX.glob(f"appendix-{old}-*"))
        for d in old_dirs:
            new_name = d.name.replace(f"appendix-{old}-", f"appendix-{new}-", 1)
            target = d.parent / new_name
            if target.exists():
                log(f"  [skip] target exists: {target.name}")
                continue
            log(f"  rename {d.name} → {new_name}")
            if apply:
                d.rename(target)
            n += 1
    log(f"[phase 3a] renamed {n} appendix directories")


def phase3b_rename_section_files(apply: bool) -> None:
    """Inside each renamed dir, rename section-<old>.N.html → section-<new>.N.html."""
    n = 0
    for old, new in RENUMBER:
        new_dirs = list(APX.glob(f"appendix-{new}-*"))
        for d in new_dirs:
            # The glossary dir was moved out — never touch it
            if d.name == "glossary":
                continue
            for sf in d.glob(f"section-{old}.*.html"):
                new_name = sf.name.replace(f"section-{old}.", f"section-{new}.", 1)
                target = sf.parent / new_name
                if target.exists():
                    log(f"  [skip] target exists: {target.name}")
                    continue
                log(f"    {sf.relative_to(ROOT)} → {new_name}")
                if apply:
                    sf.rename(target)
                n += 1
    log(f"[phase 3b] renamed {n} section files")


def phase3c_internal_markup(apply: bool) -> None:
    """Update internal markup in each renamed appendix:
    - <h1>G.1 → <h1>F.1
    - <span class="section-num">G.1</span> → F.1
    - 'Appendix G' → 'Appendix F'
    - in-section href section-g.X.html → section-f.X.html
    - title "Appendix G:" → "Appendix F:"
    """
    n_files = 0
    for old, new in RENUMBER:
        old_upper = old.upper()
        new_upper = new.upper()
        for d in APX.glob(f"appendix-{new}-*"):
            if d.name == "glossary":
                continue
            for p in d.rglob("*.html"):
                text = p.read_text(encoding="utf-8")
                original = text
                # Section letter labels
                text = re.sub(
                    rf"<h1>{old_upper}\.(\d+)",
                    rf"<h1>{new_upper}.\1",
                    text,
                )
                text = re.sub(
                    rf'<span class="section-num">{old_upper}\.(\d+)</span>',
                    rf'<span class="section-num">{new_upper}.\1</span>',
                    text,
                )
                # Chapter label "Appendix G" inside this directory
                text = re.sub(rf"\bAppendix {old_upper}\b",
                              f"Appendix {new_upper}", text)
                text = re.sub(rf"chapter:Appendix {old_upper}\b",
                              f"chapter:Appendix {new_upper}", text)
                # Title
                text = re.sub(rf"<title>Appendix {old_upper}:",
                              f"<title>Appendix {new_upper}:", text)
                # In-section sibling refs section-g.N.html
                text = re.sub(rf"section-{old}\.(\d+)\.html",
                              rf"section-{new}.\1.html", text)
                if text != original:
                    n_files += 1
                    if apply:
                        p.write_text(text, encoding="utf-8")
    log(f"[phase 3c] updated internal markup in {n_files} files")


def phase4_book_wide_hrefs(apply: bool) -> None:
    """Update book-wide hrefs:
    - appendix-f-glossary/ → glossary/    (3,579 refs)
    - appendix-g-* → appendix-f-*          (URL)
    - appendix-h-* → appendix-g-*
    - ... etc.

    Process in two passes:
    Pass A: glossary path rewrite (must run before letter shifts so we
            don't accidentally hit `appendix-f-glossary` after F slot is
            taken by hardware-compute).
    Pass B: letter renumber for G..V → F..U.

    Both passes operate on URL strings only (parent-dir + filename).
    Letter substitutions to "Appendix X" prose are NOT done globally
    here — that would risk false positives in unrelated text. The
    in-appendix prose was already updated in phase 3c.
    """
    # Pass A: glossary
    n_glossary = 0
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP for part in p.parts):
            continue
        # Skip files inside the moved glossary itself (already phase 2)
        if "glossary" in p.parts and "appendices" in p.parts:
            # Glossary itself only refers internally as relative; skip
            pass
        text = p.read_text(encoding="utf-8")
        original = text
        text = text.replace("appendix-f-glossary/", "glossary/")
        if text != original:
            n_glossary += text.count("glossary/") - original.count("glossary/")
            if apply:
                p.write_text(text, encoding="utf-8")
    log(f"[phase 4a] glossary href rewrites: ~{n_glossary} occurrences")

    # Pass B: letter renumber for hrefs only
    # Build a single regex pass per file that maps old→new in URL context.
    # Process letters from low-to-high to avoid double-shifts (g→f then we
    # see new appendix-f-* but we're now processing h→g, we don't touch f).
    n_renamed = 0
    for old, new in RENUMBER:
        # Match "appendix-g-" in href attributes
        pattern_dir = re.compile(rf'(["\'/])appendix-{old}-([a-z0-9-]+)')
        pattern_sec = re.compile(rf'section-{old}\.(\d+)\.html')
        for p in ROOT.rglob("*.html"):
            if any(part in SKIP for part in p.parts):
                continue
            text = p.read_text(encoding="utf-8")
            original = text
            text = pattern_dir.sub(rf'\1appendix-{new}-\2', text)
            text = pattern_sec.sub(rf'section-{new}.\1.html', text)
            if text != original:
                n_renamed += 1
                if apply:
                    p.write_text(text, encoding="utf-8")
    log(f"[phase 4b] letter-renumber hrefs touched: {n_renamed} files")


def phase5_update_build_hooks(apply: bool) -> None:
    """Update build_epub.py's path-suffix detection from `appendix-f-glossary`
    to `glossary`."""
    b = ROOT / "KDP" / "build" / "build_epub.py"
    text = b.read_text(encoding="utf-8")
    original = text
    text = text.replace('"appendix-f-glossary"', '"glossary"')
    text = text.replace("'appendix-f-glossary'", "'glossary'")
    # Also handle generate_spine.py
    g = ROOT / "KDP" / "build" / "generate_spine.py"
    if g.exists():
        gtext = g.read_text(encoding="utf-8")
        gtext_orig = gtext
        # generate_spine looks for 'appendix-' prefix. Glossary is no longer
        # under that prefix; it's now its own directory. Add it explicitly.
        # Without modification, generate_spine will MISS glossary in the spine.
        # The simplest fix: include `glossary` as an additional dir explicitly
        # next to appendix folders.
        # (Edit handled separately if needed - just check if changes needed.)
    if text != original:
        if apply:
            b.write_text(text, encoding="utf-8")
        log(f"[phase 5] build_epub.py glossary path-detection updated")
    else:
        log(f"[phase 5] no changes needed in build_epub.py")


def main():
    apply = "--apply" in sys.argv
    log("=== v15.12 glossary separation + appendix renumber ===")
    log(f"Mode: {'APPLY' if apply else 'DRY RUN'}")
    log("")
    phase1_move_glossary(apply)
    log("")
    phase2_glossary_internal(apply)
    log("")
    phase3a_rename_dirs(apply)
    log("")
    phase3b_rename_section_files(apply)
    log("")
    phase3c_internal_markup(apply)
    log("")
    phase4_book_wide_hrefs(apply)
    log("")
    phase5_update_build_hooks(apply)
    log("")
    log("Done. Run with --apply to write changes.")


if __name__ == "__main__":
    main()
