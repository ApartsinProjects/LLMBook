"""Fix orphan same-doc hrefs: href="#foo" where #foo doesn't exist in THIS file.

If the target id exists in some OTHER source HTML file, rewrite the href to
point to that file. If the id doesn't exist anywhere, leave the href alone
(report for manual review — likely a deleted/renamed reference).

This complements fix_same_doc_hrefs.py:
  - fix_same_doc_hrefs.py: handles WORKING same-doc refs by adding filename prefix.
  - fix_orphan_anchors.py:  handles BROKEN same-doc refs by finding the right target file.

Usage:
  python KDP/build/fix_orphan_anchors.py            # dry-run, propose fixes
  python KDP/build/fix_orphan_anchors.py --apply    # write changes + backups
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict


ROOT = Path(__file__).resolve().parents[2]
EXCLUDE = ("kpv-direct", "source_fix_backups", "node_modules", "pagefind",
           ".git", "KDP/output", "KDP/build/tools", "agents/book-skills/templates")


def excluded(p: Path) -> bool:
    s = str(p).replace("\\", "/")
    return any(x in s for x in EXCLUDE)


HREF_FRAGMENT = re.compile(
    r'(<a\b[^>]*?\bhref=")(#[^"#]+)("[^>]*>)',
    flags=re.IGNORECASE | re.DOTALL,
)
ID_ATTR = re.compile(r'\bid="([^"]+)"')


def build_id_index(files: list[Path]) -> dict[str, list[Path]]:
    """For every id="..." in every source HTML file, record which files contain it."""
    index: dict[str, list[Path]] = defaultdict(list)
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in ID_ATTR.finditer(text):
            index[m.group(1)].append(f)
    return index


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    files = [f for f in ROOT.rglob("*.html") if not excluded(f)]
    print(f"Scanning {len(files)} source HTML files...")
    id_index = build_id_index(files)
    print(f"Indexed {len(id_index)} unique ids across all files.")
    print()

    total_fixed = 0
    total_orphan_still = 0
    total_ambiguous = 0
    files_changed = 0
    backup_root = ROOT / "KDP" / "build" / "source_fix_backups" / "orphan_anchors"

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        ids_in_this = set(ID_ATTR.findall(text))

        fixes: list[tuple[str, str]] = []  # (anchor, target_filename)
        report: list[str] = []

        def replace(m: re.Match) -> str:
            anchor = m.group(2)               # "#foo"
            target = anchor[1:]
            if target in ids_in_this:
                return m.group(0)  # working same-doc; handled by other script
            owners = id_index.get(target, [])
            owners = [o for o in owners if o != f]  # exclude self
            if not owners:
                # SMART FALLBACK: same-file STALE-PREFIX heuristic.
                # Section-number renumberings leave broken hrefs like
                # `#9-5-2-unstructured-pruning` whose tail (`unstructured-pruning`)
                # still matches an id `#9-7-2-unstructured-pruning` in the same
                # file. Auto-find by matching trailing slug parts.
                target_parts = target.split("-")
                if len(target_parts) >= 3:
                    tail_slug = "-".join(target_parts[2:])  # skip first 2 numeric parts
                    candidates = [i for i in ids_in_this
                                  if i.endswith("-" + tail_slug) or i == tail_slug]
                    if len(candidates) == 1:
                        fixes.append((anchor, f"(stale-prefix: ->#{candidates[0]})"))
                        return f'{m.group(1)}#{candidates[0]}{m.group(3)}'
                    elif len(candidates) > 1:
                        report.append(f"AMBIGUOUS  {anchor}  (stale-prefix; {len(candidates)} matches "
                                      f"by tail-slug: {candidates[:3]}...; needs manual review)")
                        return m.group(0)
                report.append(f"ORPHAN     {anchor}  (no source HTML file defines id={target!r})")
                return m.group(0)
            if len(owners) > 1:
                # Pick the one in the closest dir (heuristic)
                owner = min(owners, key=lambda o: len(str(o.relative_to(ROOT)).split("/")))
                report.append(f"AMBIGUOUS  {anchor}  (in {len(owners)} files; using {owner.name})")
            else:
                owner = owners[0]
            new_href = f"{owner.name}{anchor}"
            fixes.append((anchor, owner.name))
            return f'{m.group(1)}{new_href}{m.group(3)}'

        new_text = HREF_FRAGMENT.sub(replace, text)
        if fixes or report:
            print(f"  {f.relative_to(ROOT)}")
            for a, fn in fixes:
                print(f"    fix:       {a}  ->  {fn}{a}")
            for r in report:
                print(f"    {r}")
            total_fixed += len(fixes)
            total_orphan_still += sum(1 for r in report if r.startswith("ORPHAN"))
            total_ambiguous += sum(1 for r in report if r.startswith("AMBIGUOUS"))

        if args.apply and new_text != text:
            files_changed += 1
            backup_root.mkdir(parents=True, exist_ok=True)
            bak_name = str(f.relative_to(ROOT)).replace("/", "_").replace("\\", "_") + ".bak"
            (backup_root / bak_name).write_text(text, encoding="utf-8")
            f.write_text(new_text, encoding="utf-8")

    print()
    print("=" * 60)
    print(f"Hrefs rewritten:                  {total_fixed}")
    print(f"Orphans still unresolvable:       {total_orphan_still}")
    print(f"Ambiguous (multi-file targets):   {total_ambiguous}")
    print(f"Files changed:                    {files_changed}")
    if not args.apply:
        print("\nDRY-RUN. Re-run with --apply to write changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
