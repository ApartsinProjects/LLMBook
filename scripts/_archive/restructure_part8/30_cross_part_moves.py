"""Phase 3: execute cross-part section moves from migration-map.json.

Cross-part moves (action contains 'cross-part') relocate a section between
Part 8 and Part 10 (or back). For each move:
  1. git mv source -> destination.
  2. Rewrite the file's chapter/section number references (h1, h2, breadcrumb,
     pagefind-meta, title, page-current, cross-folder hrefs).
  3. Rewrite the breadcrumb part name (Part VIII -> Part X) if the move is
     cross-part.

For merge moves (action contains 'merge'), the destination already exists
from a prior cross-part move; merge body content + dedup callouts. After
the merge, the legacy module module-49-post-launch-monitoring should be
empty and can be removed.

DRY-RUN by default.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP = HERE / "migration-map.json"

# Hard-coded part metadata for breadcrumb rewriting
PART_META = {
    "part-8-evaluation-production": ("VIII", "Evaluation of LLM-Based Systems"),
    "part-10-idea-to-product": ("X", "Building LLM and Agent Products"),
}


def parse_section_num(filename: str) -> tuple[int, int] | None:
    m = re.match(r"section-(\d+)\.(\d+)\.html", filename)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def rewrite_file_metadata(text: str, old_path: str, new_path: str,
                          old_sec: tuple[int, int], new_sec: tuple[int, int],
                          new_chapter_title: str | None = None) -> str:
    """Rewrite the section file's metadata for a cross-part move."""
    old_ch, old_secn = old_sec
    new_ch, new_secn = new_sec

    # Determine the destination part metadata
    dst_part = None
    for part_slug, (roman, title) in PART_META.items():
        if part_slug in new_path:
            dst_part = (roman, title)
            break

    # Rewrite "Section old.X" -> "Section new.Y"
    text = re.sub(
        rf"\bSection {old_ch}\.{old_secn}\b",
        f"Section {new_ch}.{new_secn}",
        text,
    )
    # In the title tag specifically
    text = re.sub(
        rf"<title>Section {old_ch}\.{old_secn}",
        f"<title>Section {new_ch}.{new_secn}",
        text,
    )
    # page-current
    text = re.sub(
        rf'<div class="page-current">Section {old_ch}\.{old_secn}</div>',
        f'<div class="page-current">Section {new_ch}.{new_secn}</div>',
        text,
    )
    # Chapter ref in breadcrumb / pagefind-meta — rewrite Chapter old_ch -> Chapter new_ch
    text = re.sub(rf"\bChapter {old_ch}\b", f"Chapter {new_ch}", text)

    # Anchor IDs (h2/h3): old_ch-old_secn-... -> new_ch-new_secn-...
    text = re.sub(
        rf'\bid="{old_ch}-{old_secn}-',
        f'id="{new_ch}-{new_secn}-',
        text,
    )
    text = re.sub(
        rf'#{old_ch}-{old_secn}-',
        f'#{new_ch}-{new_secn}-',
        text,
    )

    # h2 / h3 raw text prefixes: ">old.X.Y Title</h2>" -> new.Y.Z
    # Use \g<1> to disambiguate from "\151.4." which re parses as backref 151.
    text = re.sub(
        rf"(<h[234][^>]*>){old_ch}\.{old_secn}\.",
        rf"\g<1>{new_ch}.{new_secn}.",
        text,
    )

    # Caption labels: Code Fragment / Figure / Table / Listing
    for label in ["Code Fragment", "Figure", "Table", "Listing"]:
        text = re.sub(
            rf"\b{label} {old_ch}\.{old_secn}\.",
            f"{label} {new_ch}.{new_secn}.",
            text,
        )

    # Breadcrumb part link rewrite (cross-part move)
    if dst_part:
        dst_roman, dst_title = dst_part
        # Rewrite the breadcrumb part-link text
        text = re.sub(
            r'<a href="\.\./index\.html">Part [VIX]+: [^<]+</a>',
            f'<a href="../index.html">Part {dst_roman}: {dst_title}</a>',
            text,
        )
        # Rewrite the pagefind-meta part: tag
        text = re.sub(
            r'data-pagefind-meta="part:Part [VIX]+: [^"]+"',
            f'data-pagefind-meta="part:Part {dst_roman}: {dst_title}"',
            text,
        )

    # Chapter title in breadcrumb / pagefind-meta if new_chapter_title given
    if new_chapter_title:
        text = re.sub(
            r'<a href="index\.html">Chapter \d+: [^<]+</a>',
            f'<a href="index.html">Chapter {new_ch}: {new_chapter_title}</a>',
            text,
        )
        text = re.sub(
            r'data-pagefind-meta="chapter:Chapter \d+: [^"]+"',
            f'data-pagefind-meta="chapter:Chapter {new_ch}: {new_chapter_title}"',
            text,
        )

    # Self-folder hrefs need rewriting too (section-old.X.html -> section-new.Y.html
    # for *this* file's siblings). But the new siblings have new numbers — we'd need
    # the FULL map of moved sections to handle this. For now, simple rewrite:
    # any href to section-old_ch.something.html in this file points at a stale path.
    # Phase 5 handles this comprehensively. Just rewrite our own section number here.

    return text


def resolve_current_src(from_path: str, module_renames: dict) -> str:
    """If from_path's parent module was renamed by phase 2, return the new path."""
    parts = from_path.split("/")
    # match against module_renames keys
    for old_mod, new_mod in module_renames.items():
        if from_path.startswith(old_mod + "/"):
            rest = from_path[len(old_mod) + 1:]
            return new_mod + "/" + rest
    return from_path


def cross_part_move(entry: dict, module_renames: dict, chapter_titles: dict, dry_run: bool) -> bool:
    # Resolve src to its CURRENT path after phase 2 module renames
    src_path = resolve_current_src(entry["from"], module_renames)
    src = ROOT / src_path
    dst = ROOT / entry["to"]
    if not src.exists():
        print(f"  SKIP (no src): {src_path} (orig {entry['from']})")
        return False
    if dst.exists():
        # Could be a merge case
        if "merge" in entry.get("action", ""):
            print(f"  MERGE (dst exists): {entry['from']} + {entry['to']}")
            # For now, log and skip; do the merge manually
            return False
        print(f"  SKIP (dst exists): {entry['to']}")
        return False

    src_sec = parse_section_num(src.name)
    dst_sec = parse_section_num(dst.name)
    if not src_sec or not dst_sec:
        print(f"  SKIP (can't parse section nums): {src_path} -> {entry['to']}")
        return False

    # Determine destination chapter title from the entry's destination module
    dst_mod = dst.parent.name
    new_chapter_title = chapter_titles.get(dst_mod)

    print(f"  git mv {src_path} -> {entry['to']}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        # First git mv
        result = subprocess.run(
            ["git", "mv", str(src), str(dst)],
            cwd=ROOT, capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"  ERROR git mv: {result.stderr}")
            return False
        # Then rewrite content
        text = dst.read_text(encoding="utf-8")
        text = rewrite_file_metadata(text, src_path, entry["to"],
                                       src_sec, dst_sec, new_chapter_title)
        dst.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    # Build destination-module to chapter-title map for new chapter title injection
    chapter_titles = {}
    for entry in data["modules_to_create"]:
        mod = Path(entry["path"]).name
        chapter_titles[mod] = entry["title"]
    # Also include renamed existing modules (their chapter titles come from index.html)
    for src, dst in data["module_renames"].items():
        dst_mod = Path(dst).name
        if dst_mod in chapter_titles:
            continue
        # Read the renamed module's index.html for its title
        idx = ROOT / dst / "index.html"
        if idx.exists():
            t = idx.read_text(encoding="utf-8")
            m = re.search(r"<h1>([^<]+)</h1>", t)
            if m:
                chapter_titles[dst_mod] = m.group(1)

    print(f"=== Phase 3: cross-part section moves ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)")
    print()
    n_moved = 0
    n_merge = 0
    module_renames = data["module_renames"]
    for entry in data["section_moves"]:
        action = entry.get("action", "")
        if "cross-part" not in action:
            continue
        if cross_part_move(entry, module_renames, chapter_titles, dry_run):
            n_moved += 1
        elif "merge" in action:
            n_merge += 1
    print()
    print(f"=== Summary ===")
    print(f"Cross-part moves applied: {n_moved}")
    print(f"Merges flagged: {n_merge} (manual editorial pass)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
