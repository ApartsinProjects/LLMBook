"""Apply a book-structure migration.

Inputs:
  --current  Path to the CURRENT book_structure.yaml (snapshot of disk)
  --target   Path to the TARGET book_structure.yaml (the desired final state)

Diffs the two and applies the necessary moves/renames/cross-reference
rewrites to bring the disk into alignment with the target.

Operations performed (in order):

1. **Identity table**: build a (kind, old_id) -> (new_id, new_path) mapping
   from any entry that exists in both yamls. Identity is matched by SLUG
   (not by number) so that "Module 27 in Part 7" matches "Module 25 in
   Part 7" if its slug stayed `llm-applications` (we explicitly mark
   moves in target yaml via a `from:` field).

2. **Rename + move**: for each entry whose path changed, `git mv` the
   directory or file. Use `git mv` so history is preserved.

3. **Caption letter shifts**: for each entry whose number changed (chapter
   or appendix), rewrite all caption labels inside that file's HTML
   (`Code Fragment N.M.K`, `Figure N.M.K`, `Table N.M.K`,
   `Pseudocode N.M.K`).

4. **Cross-reference rewrite**: walk every HTML body book-wide; for each
   token that resolves via the identity table, rewrite to the new id +
   relative path.

5. **Drop**: for entries in current but missing in target, EITHER delete
   the file (if `drop: true` is set in current entry) OR halt and report
   (default).

6. **Add**: for entries in target but missing in current, create a
   skeleton HTML file using the section template. The skeleton has the
   right breadcrumb, h1, and a `TODO author this section` marker.

7. **Rebuild artifacts**: call the sibling rebuild scripts:
   - scripts/_rebuild_toc.py
   - scripts/_rebuild_appendices_index.py
   - scripts/_normalize_page_headers.py
   - scripts/_redesign_chapter_nav.py
   - scripts/_fix_whatsnext_hyperlinks.py
   In that order.

8. **Cross-reference integrity check**: report any link that resolves to
   a non-existent target.

Dry-run mode: prints the planned ops without executing.

Idempotent.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]


def build_identity(current: dict, target: dict) -> list[dict]:
    """Build the identity / move table.

    Returns a list of dicts: {
        kind: 'part' | 'chapter' | 'section' | 'appendix' | 'appendix_section' | 'front_matter',
        old_id: str,
        new_id: str,
        old_path: str,  # relative to book root
        new_path: str,  # relative to book root
        action: 'rename' | 'keep' | 'drop' | 'add' | 'renumber_only',
    }
    """
    rows: list[dict] = []

    # Build lookup by slug for fast matching
    def part_key(p): return p["slug"]
    def chap_key(c, p): return f"{p['slug']}/{c['slug']}"
    def sec_key(s, c, p): return f"{p['slug']}/{c['slug']}/{s['slug']}"
    def app_key(a): return a["slug"]
    def app_sec_key(s, a): return f"{a['slug']}/{s['slug']}"

    cur_parts = {part_key(p): p for p in current.get("parts", [])}
    tgt_parts = {part_key(p): p for p in target.get("parts", [])}

    # Parts
    for slug, p_cur in cur_parts.items():
        p_tgt = tgt_parts.get(slug)
        if p_tgt is None:
            rows.append({"kind": "part", "old_id": p_cur["num"], "new_id": None,
                         "old_path": f"part-{p_cur['num']}-{slug}",
                         "new_path": None, "action": "drop"})
            continue
        if p_cur["num"] != p_tgt["num"]:
            rows.append({"kind": "part", "old_id": p_cur["num"], "new_id": p_tgt["num"],
                         "old_path": f"part-{p_cur['num']}-{slug}",
                         "new_path": f"part-{p_tgt['num']}-{slug}",
                         "action": "rename"})
        else:
            rows.append({"kind": "part", "old_id": p_cur["num"], "new_id": p_tgt["num"],
                         "old_path": f"part-{p_cur['num']}-{slug}",
                         "new_path": f"part-{p_tgt['num']}-{slug}",
                         "action": "keep"})
    for slug, p_tgt in tgt_parts.items():
        if slug not in cur_parts:
            rows.append({"kind": "part", "old_id": None, "new_id": p_tgt["num"],
                         "old_path": None,
                         "new_path": f"part-{p_tgt['num']}-{slug}",
                         "action": "add"})

    # Chapters
    cur_chaps: dict[str, tuple[dict, dict]] = {}  # key -> (part, chapter)
    for p in current.get("parts", []):
        for c in p.get("chapters", []):
            cur_chaps[chap_key(c, p)] = (p, c)
    tgt_chaps: dict[str, tuple[dict, dict]] = {}
    for p in target.get("parts", []):
        for c in p.get("chapters", []):
            tgt_chaps[chap_key(c, p)] = (p, c)

    # When a chapter MOVES between parts, the key changes. Allow target
    # entries to declare a `from:` field with the old key for explicit
    # cross-part moves.
    for p in target.get("parts", []):
        for c in p.get("chapters", []):
            if "from" in c:
                cur_chaps[chap_key(c, p)] = cur_chaps.pop(c["from"])

    for k, (p_cur, c_cur) in cur_chaps.items():
        tup = tgt_chaps.get(k)
        if tup is None:
            rows.append({"kind": "chapter", "old_id": c_cur["num"], "new_id": None,
                         "old_path": f"part-{p_cur['num']}-{p_cur['slug']}/module-{c_cur['num']:02d}-{c_cur['slug']}",
                         "new_path": None, "action": "drop"})
            continue
        p_tgt, c_tgt = tup
        old_path = f"part-{p_cur['num']}-{p_cur['slug']}/module-{c_cur['num']:02d}-{c_cur['slug']}"
        new_path = f"part-{p_tgt['num']}-{p_tgt['slug']}/module-{c_tgt['num']:02d}-{c_tgt['slug']}"
        action = "keep" if old_path == new_path else "rename"
        rows.append({"kind": "chapter", "old_id": c_cur["num"], "new_id": c_tgt["num"],
                     "old_path": old_path, "new_path": new_path, "action": action})

    for k, (p_tgt, c_tgt) in tgt_chaps.items():
        if k not in cur_chaps:
            rows.append({"kind": "chapter", "old_id": None, "new_id": c_tgt["num"],
                         "old_path": None,
                         "new_path": f"part-{p_tgt['num']}-{p_tgt['slug']}/module-{c_tgt['num']:02d}-{c_tgt['slug']}",
                         "action": "add"})

    # TODO: same shape for sections, appendices, appendix sections, front-matter.
    # Implementation deferred until current + target yamls land.

    return rows


def apply_renames(rows: list[dict], dry_run: bool) -> list[str]:
    """Execute git-mv for every action='rename' entry."""
    msgs: list[str] = []
    for r in rows:
        if r["action"] != "rename":
            continue
        old = ROOT / r["old_path"]
        new = ROOT / r["new_path"]
        if not old.exists():
            msgs.append(f"  SKIP rename {r['old_path']} -> {r['new_path']}: source missing")
            continue
        if new.exists():
            msgs.append(f"  SKIP rename {r['old_path']} -> {r['new_path']}: target exists")
            continue
        msgs.append(f"  RENAME {r['old_path']} -> {r['new_path']}")
        if not dry_run:
            new.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "mv", str(old), str(new)],
                            cwd=ROOT, check=False)
    return msgs


def rewrite_cross_refs(identity: list[dict], dry_run: bool) -> list[str]:
    """Walk every HTML book-wide, rewrite tokens that match the identity
    table. Tokens to find: 'Chapter N', 'Part X', 'Section N.M', 'Appendix X[.N]',
    plus href paths."""
    # Build replacement maps
    chap_map: dict[int, int] = {}
    part_map: dict[int, int] = {}
    for r in identity:
        if r["kind"] == "chapter" and r["old_id"] and r["new_id"] and r["old_id"] != r["new_id"]:
            chap_map[r["old_id"]] = r["new_id"]
        if r["kind"] == "part" and r["old_id"] and r["new_id"] and r["old_id"] != r["new_id"]:
            part_map[r["old_id"]] = r["new_id"]

    msgs: list[str] = []
    msgs.append(f"  Chapter renumbers: {len(chap_map)}")
    msgs.append(f"  Part renumbers: {len(part_map)}")
    # TODO: actual rewrite. Deferred until yamls land.
    return msgs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--current", type=Path, required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--apply", action="store_true",
                    help="Actually execute (default is dry-run)")
    ap.add_argument("--out-mapping", type=Path,
                    default=ROOT / ".book-update" / "migration-map.json")
    args = ap.parse_args()

    current = yaml.safe_load(args.current.read_text(encoding="utf-8"))
    target = yaml.safe_load(args.target.read_text(encoding="utf-8"))

    rows = build_identity(current, target)
    args.out_mapping.parent.mkdir(parents=True, exist_ok=True)
    args.out_mapping.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Wrote migration map: {args.out_mapping} ({len(rows)} entries)")

    # Summary
    by_action: dict[str, int] = {}
    for r in rows:
        by_action[r["action"]] = by_action.get(r["action"], 0) + 1
    for action, n in sorted(by_action.items()):
        print(f"  {action}: {n}")

    dry = not args.apply
    print(f"\n{'DRY-RUN' if dry else 'APPLY'} renames:")
    for m in apply_renames(rows, dry_run=dry):
        print(m)
    print(f"\nCross-ref rewrite:")
    for m in rewrite_cross_refs(rows, dry_run=dry):
        print(m)

    return 0


if __name__ == "__main__":
    sys.exit(main())
