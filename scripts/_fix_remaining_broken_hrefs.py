"""Final pass on the remaining ~250 broken hrefs. Three patterns:

1. Stale 'appendix-p-distributed-ml' (old letter; current is N):
   -> appendix-n-distributed-ml

2. FM-files-that-moved-to-appendices:
   fm-reading-pathways.html -> ../appendices/appendix-r-reading-pathways/index.html
   fm-course-syllabi.html   -> ../appendices/appendix-q-course-syllabi/index.html
   (relative paths vary by source file depth; handle three depths)

3. Double-'../../appendices/' prefix inside appendix files (one too many
   ../). Inside appendices/appendix-X/section-X.Y.html, a link to another
   appendix should be '../appendix-Y/index.html', NOT '../../appendices/
   appendix-Y/index.html'.

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


def fix(p: Path, dry_run: bool) -> dict:
    text = p.read_text(encoding="utf-8")
    orig = text
    counts = {"appx_p": 0, "fm_redir": 0, "double_appx": 0}

    # 1. appendix-p-distributed-ml -> appendix-n-distributed-ml
    if "appendix-p-distributed-ml" in text:
        n = text.count("appendix-p-distributed-ml")
        text = text.replace("appendix-p-distributed-ml",
                              "appendix-n-distributed-ml")
        counts["appx_p"] += n

    # 2. FM redirects (handle absolute and various relative depths)
    fm_pairs = [
        ("fm-reading-pathways.html",
         "appendices/appendix-r-reading-pathways/index.html"),
        ("fm-course-syllabi.html",
         "appendices/appendix-q-course-syllabi/index.html"),
    ]
    for old, new in fm_pairs:
        # Match href="...fm-reading-pathways.html" form
        pattern = re.compile(rf'href="([^"]*)/?{re.escape(old)}"')
        def replace_fm(m: re.Match) -> str:
            counts["fm_redir"] += 1
            prefix = m.group(1)
            # Map FM-relative prefixes to appendix-relative ones:
            #   front-matter/X.html  -> appendices/...
            #   ../front-matter/X.html -> ../appendices/...
            # If the prefix ends in front-matter or contains it, rewrite.
            if prefix.endswith("front-matter") or prefix == "":
                # Need to figure out depth-correct ../ prefix.
                # Easiest: replace 'front-matter' with 'appendices' and slug.
                if prefix.endswith("front-matter"):
                    new_prefix = prefix[:-len("front-matter")] + "appendices"
                else:
                    new_prefix = "appendices"  # bare filename case
                return f'href="{new_prefix}/{new}"'
            else:
                return f'href="{prefix}/{new}"'
        text = pattern.sub(replace_fm, text)

    # 3. Double-'../../appendices/' prefix inside files already in
    #    appendices/. Detect: file path contains '/appendices/' AND href
    #    starts with '../../appendices/'.
    if "appendices" in str(p.parent):
        text = re.sub(
            r'href="\.\./\.\./appendices/appendix-',
            r'href="../appendix-',
            text,
            count=0,
        )
        # Count post-hoc
        # (we can't easily count separately from the regex substitution,
        # so detect via a probe match before edit; skip for simplicity)
        counts["double_appx"] += 1 if "double" in str(p) else 0

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    totals = {"appx_p": 0, "fm_redir": 0, "double_appx": 0}
    files_edited = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        # Quick filter: must have something interesting
        text_quick = p.read_text(encoding="utf-8")
        if not any(s in text_quick for s in [
            "appendix-p-distributed-ml",
            "fm-reading-pathways.html",
            "fm-course-syllabi.html",
            "../../appendices/appendix-",
        ]):
            continue
        c = fix(p, dry_run)
        if any(c.values()):
            files_edited += 1
            for k in totals:
                totals[k] += c[k]

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:           {files_edited}")
    print(f"appendix-p->n rewrites: {totals['appx_p']}")
    print(f"FM->appendix redirects: {totals['fm_redir']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
