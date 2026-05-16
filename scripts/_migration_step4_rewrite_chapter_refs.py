"""Migration step 4: book-wide rewrite of chapter / section / caption refs
per the target yaml chapter renumbering.

Two-pass with temp tokens to avoid cascading collisions:

Pass 1: Rewrite every old chapter number reference to a temp token
        "Chapter 21" -> "Chapter §21§" (and similar for sections, captions, hrefs)
Pass 2: Rewrite temp tokens to final values
        "Chapter §21§" -> "Chapter 26"

Token used: § (section sign) surrounding the number, then the literal old
number. Easy to distinguish from real chapter numbers and easy to swap out.

Rewrite targets:
- "Chapter N" body text
- "Section X.Y" body text
- "Code Fragment X.Y.Z" / "Figure X.Y.Z" / "Table X.Y.Z" / "Pseudocode X.Y.Z" captions
- href paths: module-NN-slug -> module-MM-slug
- href paths to specific section files: section-X.Y.html (where X = old chap num)

Idempotent.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

TOKEN = "§"


def build_chap_map(target: dict) -> dict[int, int]:
    """Return {old_num: new_num} for every chapter whose number changed."""
    out: dict[int, int] = {}
    for p in target["parts"]:
        for c in p.get("chapters", []):
            if c.get("_new"):
                continue
            old = c.get("old_num")
            new = c.get("num")
            if old is None or new is None:
                continue
            if isinstance(old, int) and isinstance(new, int) and old != new:
                out[old] = new
    return out


def rewrite_file(p: Path, chap_map: dict[int, int], dry_run: bool) -> int:
    """Return number of edits applied to this file."""
    text = p.read_text(encoding="utf-8")
    orig = text

    # Pass 1: encode old chapter refs as tokens
    for old, new in chap_map.items():
        # "Chapter N" (word boundary)
        text = re.sub(rf"\bChapter\s+{old}\b",
                       f"Chapter {TOKEN}{old}{TOKEN}", text)
        # "Section N.Y" (word boundary on N; preserve .Y)
        text = re.sub(rf"\bSection\s+{old}\.(\d+(?:\.\d+)?)\b",
                       rf"Section {TOKEN}{old}{TOKEN}.\1", text)
        # Captions: Code Fragment N.Y.Z, Figure, Table, Pseudocode
        for kind in ("Code Fragment", "Figure", "Table", "Pseudocode"):
            text = re.sub(rf"\b{kind}\s+{old}\.(\d+(?:\.\d+)?)\b",
                           rf"{kind} {TOKEN}{old}{TOKEN}.\1", text)
        # href to module-NN-slug
        text = re.sub(rf"module-{old:02d}-",
                       f"module-{TOKEN}{old}{TOKEN}-", text)
        # href to section-N.Y.html where N is old chap num
        text = re.sub(rf"section-{old}\.(\d+(?:\.\d+)?)\.html",
                       rf"section-{TOKEN}{old}{TOKEN}.\1.html", text)

    # Pass 2: replace tokens with new values
    for old, new in chap_map.items():
        text = text.replace(f"{TOKEN}{old}{TOKEN}", str(new))
        # module-NN- format needs zero-padding
        text = text.replace(f"module-{new}-", f"module-{new:02d}-")

    if text == orig:
        return 0
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path,
                    default=ROOT / "book_structure.target.yaml")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    target = yaml.safe_load(args.target.read_text(encoding="utf-8"))
    chap_map = build_chap_map(target)
    print(f"Chapter renumber map: {len(chap_map)} entries")
    for old, new in sorted(chap_map.items()):
        print(f"  {old} -> {new}")

    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        if rewrite_file(p, chap_map, dry_run):
            n_files += 1
    # Also rewrite toc.html
    for special in ("toc.html",):
        sp = ROOT / special
        if sp.exists():
            if rewrite_file(sp, chap_map, dry_run):
                n_files += 1

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n{mode}: rewrote chapter/section refs in {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
