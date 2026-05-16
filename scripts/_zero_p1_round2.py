"""Second-round P1 zero-out sweep. Targets per-file depth + slug issues
that survived the first pass.

1. appendix-p-course-syllabi/index.html, appendix-q-reading-pathways/index.html:
   wrong-depth refs (../ -> ../../) for toc, front-matter; sister-appendix
   refs use ../appendix-X-... not ../appendices/appendix-X-...; one
   double-typo path 'appendices/appendices/'; strip dead section-33.7 ref.

2. front-matter/*.html: href="index.html" -> href="../index.html"
   (the deleted FM index used to be the target; book root is one level up).

3. Slug renames:
   module-24-context-management -> module-24-conversational-ai
   module-24-vector-databases   -> module-22-embeddings-vector-db
   module-07-pretraining        -> module-07-pretraining-scaling-laws

4. Strip dead section refs (sections don't exist):
   section-33.4 through section-33.11 in module-61 (only 1-4 exist)
   section-42.5 in module-42 (only 1-4 exist)
   section-62.5, .6, .7 in module-62 (only 1-4 exist)

Idempotent.
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


def fix_appendix_pq_indexes(dry_run: bool) -> int:
    """Two files only: appendix-p-course-syllabi/index.html, appendix-q-
    reading-pathways/index.html."""
    files = [
        ROOT / "appendices" / "appendix-p-course-syllabi" / "index.html",
        ROOT / "appendices" / "appendix-q-reading-pathways" / "index.html",
    ]
    n = 0
    for p in files:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        # ../toc.html (broken from /appendices/appendix-X/) -> ../../toc.html
        text = text.replace('href="../toc.html"', 'href="../../toc.html"')
        # ../front-matter/ -> ../../front-matter/
        text = text.replace('href="../front-matter/', 'href="../../front-matter/')
        # ../appendices/appendix-X-X- -> ../appendix-X- (sister appendix from within appendices/)
        text = re.sub(r'href="\.\./appendices/(appendix-[a-z]-)',
                       r'href="../\1', text)
        # appendices/appendices/ typo
        text = text.replace("appendices/appendices/", "")
        # Strip dead module-61 section-33.7+ refs
        text = re.sub(
            r'<a[^>]*href="[^"]*module-61-frontier-architectures/section-33\.(4|5|6|7|8|9|10|11)\.html[^"]*"[^>]*>'
            r'([^<]*)</a>',
            r'\2', text,
        )
        if text != orig:
            n += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    return n


def fix_front_matter_index_refs(dry_run: bool) -> int:
    """In front-matter/*.html, href="index.html" pointed at the deleted
    FM index. Should be ../index.html (book root cover)."""
    fm_dir = ROOT / "front-matter"
    if not fm_dir.exists():
        return 0
    n = 0
    for p in fm_dir.glob("*.html"):
        text = p.read_text(encoding="utf-8")
        orig = text
        # Match href="index.html" but NOT href="../index.html" or others
        text = re.sub(r'href="index\.html"', 'href="../index.html"', text)
        if text != orig:
            n += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    return n


def fix_slug_renames(dry_run: bool) -> int:
    """Book-wide slug renames for old module names."""
    renames = [
        ("module-24-context-management", "module-24-conversational-ai"),
        ("module-24-vector-databases", "module-22-embeddings-vector-db"),
        ("module-07-pretraining/", "module-07-pretraining-scaling-laws/"),
    ]
    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        for old, new in renames:
            text = text.replace(old, new)
        if text != orig:
            n_files += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    return n_files


def strip_dead_section_refs(dry_run: bool) -> int:
    """Strip <a> wrappers pointing at section files that don't exist."""
    dead_refs = [
        r"module-61-frontier-architectures/section-33\.(4|5|6|7|8|9|10|11)\.html",
        r"module-42-strategy-prioritization/section-42\.5\.html",
        r"module-62-frontier-theory/section-62\.(5|6|7|8|9)\.html",
    ]
    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        for pat in dead_refs:
            text = re.sub(
                rf'<a[^>]*href="[^"]*{pat}[^"]*"[^>]*>([^<]*)</a>',
                r"\1", text,
            )
        if text != orig:
            n_files += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    return n_files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    n_pq = fix_appendix_pq_indexes(dry_run)
    n_fm = fix_front_matter_index_refs(dry_run)
    n_slug = fix_slug_renames(dry_run)
    n_strip = strip_dead_section_refs(dry_run)
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"P/Q index fixes:           {n_pq}")
    print(f"Front-matter index.html:   {n_fm}")
    print(f"Slug rename files:         {n_slug}")
    print(f"Dead-section strips:       {n_strip}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
