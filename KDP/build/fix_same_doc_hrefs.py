"""Fix same-document hrefs in source HTML so KFX converter can resolve them.

Why: KFX (Kindle Format X) converter doesn't resolve href="#foo"
(fragment-only) references. It needs href="filename.html#foo" with an
explicit file part. EPUBCheck accepts both per EPUB 3 spec, but KFX
silently emits W10001 "Hyperlink could not be resolved" warnings on
same-document fragment-only refs.

This script:
  1. Walks all source HTML files in the project root (excludes
     KDP/output/, KDP/build/source_fix_backups/, node_modules/, pagefind/).
  2. For each <a href="#anchor">...</a> in a file, checks if id="anchor"
     exists in the SAME file.
  3. If yes -> rewrites to <a href="<basename>.html#anchor">...</a>.
     html2epub will map basename.html to its flat chapter filename when
     building the EPUB, producing href="ch_NNNN_*.xhtml#anchor" which KFX
     handles correctly.
  4. Skips fragment-only refs whose targets DON'T exist in this file
     (those are already broken in EPUB too and require a different fix).
  5. Writes a per-file backup under KDP/build/source_fix_backups/.

Usage:
  python KDP/build/fix_same_doc_hrefs.py                  # dry-run, show plan
  python KDP/build/fix_same_doc_hrefs.py --apply          # actually edit files
  python KDP/build/fix_same_doc_hrefs.py --only path.html # restrict to one file
"""
from __future__ import annotations
import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXCLUDE_PATTERNS = [
    "KDP/output", "KDP/build/source_fix_backups", "node_modules",
    "pagefind/", "KDP/html2epub", "KDP/validation/_raw",
    "agents/book-skills/templates",  # the {{TEMPLATE}} files; not real content
    "appendices/_archive", ".git/",
]

# Match <a ... href="#anchor" ...>
HREF_FRAGMENT = re.compile(
    r'(<a\b[^>]*?\bhref=")(#[^"#]+)("[^>]*>)',
    flags=re.IGNORECASE | re.DOTALL,
)
# Match id="anchor" on any element
ID_ATTR = re.compile(r'\bid="([^"]+)"')


def should_skip(p: Path) -> bool:
    sp = str(p).replace("\\", "/")
    return any(ex in sp for ex in EXCLUDE_PATTERNS)


def fix_file(html_path: Path, apply: bool) -> dict:
    """Inspect one HTML file; return stats."""
    try:
        text = html_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return {"file": str(html_path), "skipped": True, "reason": "read-error"}

    ids = set(ID_ATTR.findall(text))
    fixable: list[str] = []   # anchors we'll fix
    orphan: list[str] = []    # anchors with no matching id in same file
    self_name = html_path.name  # e.g. "section-19.4.html"

    def replace(m: re.Match) -> str:
        anchor = m.group(2)              # "#anchor"
        target_id = anchor[1:]
        if target_id in ids:
            fixable.append(anchor)
            return f'{m.group(1)}{self_name}{anchor}{m.group(3)}'
        else:
            orphan.append(anchor)
            return m.group(0)            # leave broken anchors alone (different problem)

    new_text = HREF_FRAGMENT.sub(replace, text)
    changed = new_text != text

    if apply and changed:
        bak_dir = ROOT / "KDP" / "build" / "source_fix_backups" / "same_doc_hrefs"
        bak_dir.mkdir(parents=True, exist_ok=True)
        # Mirror the source path under backup dir, with timestamp
        rel = html_path.relative_to(ROOT)
        bak_path = bak_dir / f"{rel.as_posix().replace('/', '_')}.bak"
        bak_path.write_text(text, encoding="utf-8")
        html_path.write_text(new_text, encoding="utf-8")

    return {
        "file": str(html_path.relative_to(ROOT)),
        "fixed": len(fixable), "fixable_anchors": fixable,
        "orphan": len(orphan), "orphan_anchors": orphan,
        "changed": changed,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Actually edit files (default: dry-run)")
    ap.add_argument("--only", type=Path, default=None,
                    help="Restrict to single file (path relative to ROOT)")
    args = ap.parse_args()

    if args.only:
        files = [args.only.resolve()]
    else:
        files = sorted(ROOT.rglob("*.html"))

    files = [f for f in files if not should_skip(f)]
    print(f"{'DRY-RUN' if not args.apply else 'APPLYING'} same-doc href fix")
    print(f"  Scanning {len(files)} HTML files")
    print()

    results: list[dict] = []
    total_fixed = 0
    total_orphan = 0
    files_changed = 0
    for f in files:
        r = fix_file(f, args.apply)
        results.append(r)
        total_fixed += r.get("fixed", 0)
        total_orphan += r.get("orphan", 0)
        if r.get("changed"): files_changed += 1
        if r.get("fixed") or r.get("orphan"):
            mark = "*" if r.get("changed") else " "
            print(f"  {mark} {r['file']}")
            for a in (r.get("fixable_anchors") or [])[:8]:
                print(f"      fix:    {a}  -> {f.name}{a}")
            for a in (r.get("orphan_anchors") or [])[:8]:
                print(f"      orphan: {a}   (no matching id; not changed)")

    print()
    print("=" * 60)
    print(f"Files scanned:       {len(files)}")
    print(f"Files changed:       {files_changed}")
    print(f"Hrefs fixed:         {total_fixed}")
    print(f"Orphan hrefs (skipped, need different fix): {total_orphan}")
    if not args.apply:
        print()
        print("DRY-RUN. Re-run with --apply to actually edit files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
