"""Repair internal links whose #fragment id is stale after the renumber.

After the a/b renumber + restructure, many cross-links still point at old heading
ids like #12-2-huggingface-transformers-deep-dive while the target heading is now
#10-7-huggingface-transformers-deep-dive. The DESCRIPTIVE tail of the id is stable;
only the leading number prefix changed. So for each broken fragment we strip the
numeric prefix and look in the target file for the heading whose tail matches, then
rewrite the fragment to the current id.

Only rewrites when there is exactly ONE unambiguous tail match in the target file.
Unresolved ones are reported (manual follow-up).

Run:  py -3 scripts/fix_broken_fragments.py            # dry-run
      py -3 scripts/fix_broken_fragments.py --apply
"""
from __future__ import annotations
import argparse, os, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SKIP = {"_archive", "node_modules", ".git", "pagefind", "KDP", "build", "vendor",
        ".claude", "__pycache__", ".book-update", ".tools", "temp_epub"}
ID_RE = re.compile(r'\sid="([^"]+)"')
HREF_RE = re.compile(r'href="([^"#]+\.html)#([^"]+)"')
NUMPREFIX = re.compile(r'^\d+(?:-\d+)*-(?=[A-Za-z])')


def strip_num(frag: str) -> str:
    return NUMPREFIX.sub("", frag)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--drop-unresolved", action="store_true",
                    help="for fragments with no tail match, drop the #fragment so "
                         "the link still resolves to the (correct) target file")
    args = ap.parse_args()

    files = [p for p in ROOT.rglob("*.html") if not any(s in p.parts for s in SKIP)]
    ids: dict[Path, set] = {}
    tails: dict[Path, dict] = {}
    text_cache: dict[Path, str] = {}
    for p in files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        text_cache[p] = t
        idset = set(ID_RE.findall(t))
        ids[p] = idset
        d: dict[str, list] = {}
        for i in idset:
            d.setdefault(strip_num(i), []).append(i)
        tails[p] = d

    # global index: descriptive tail -> set of (file, id) book-wide, for content
    # that MOVED to a different file during the restructure.
    global_tails: dict[str, set] = {}
    for p in files:
        for i in ids[p]:
            global_tails.setdefault(strip_num(i), set()).add((p, i))

    fixed = unresolved = brokenfile = retargeted = dropped = 0
    unresolved_list = []
    changed_files = 0
    for p in files:
        t = text_cache[p]
        new = t
        nfix = 0
        for m in HREF_RE.finditer(t):
            tgt_rel, frag = m.group(1), m.group(2)
            tgt = Path(os.path.normpath(p.parent / tgt_rel))
            if tgt not in ids:
                brokenfile += 1
                continue
            if frag in ids[tgt]:
                continue
            cand = tails[tgt].get(strip_num(frag))
            if cand and len(set(cand)) == 1:
                old = f'href="{tgt_rel}#{frag}"'
                newh = f'href="{tgt_rel}#{cand[0]}"'
                if old in new:
                    new = new.replace(old, newh)
                    nfix += 1
                    fixed += 1
            else:
                # content may have moved to another file: search book-wide for
                # the descriptive tail and re-target the full href if unambiguous.
                g = global_tails.get(strip_num(frag), set())
                uniq = {(f, i) for (f, i) in g}
                if len(uniq) == 1:
                    tf, tid = next(iter(uniq))
                    rel = os.path.relpath(tf, p.parent).replace("\\", "/")
                    old = f'href="{tgt_rel}#{frag}"'
                    newh = f'href="{rel}#{tid}"'
                    if old in new:
                        new = new.replace(old, newh)
                        nfix += 1
                        retargeted += 1
                        continue
                if args.drop_unresolved:
                    old = f'href="{tgt_rel}#{frag}"'
                    newh = f'href="{tgt_rel}"'
                    if old in new:
                        new = new.replace(old, newh)
                        nfix += 1
                        dropped += 1
                        continue
                unresolved += 1
                unresolved_list.append((str(p.relative_to(ROOT)), frag,
                                        str(tgt.relative_to(ROOT)) if tgt.exists() else tgt_rel))
        if nfix and new != t:
            changed_files += 1
            if args.apply:
                p.write_text(new, encoding="utf-8")

    print(f"fragments fixed in-place: {fixed}  re-targeted (moved files): {retargeted}  "
          f"dropped: {dropped}  (in {changed_files} files) "
          f"{'[APPLIED]' if args.apply else '(dry-run)'}")
    print(f"unresolved fragments: {unresolved}")
    print(f"links to missing files: {brokenfile}")
    if unresolved_list:
        print("\n-- unresolved (target lacks a matching tail) --")
        seen = set()
        for src, frag, tgt in unresolved_list:
            key = (frag, tgt)
            if key in seen:
                continue
            seen.add(key)
            print(f"  {frag}  -> {tgt}")
    if not args.apply:
        print("\n(pass --apply to write)")


if __name__ == "__main__":
    main()
