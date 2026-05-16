"""Phase 2: rename module directories using `git mv` to preserve history.

Reads migration-map.json's `module_renames` and `modules_to_delete` and
`modules_to_create`. Executes git mv for renames. Creates skeleton
index.html files for new modules. Renames section-*.html files inside
renamed modules ONLY when their slug encodes the old chapter number
(e.g., section-40.1.html in module-40 -> module-42 becomes section-42.1.html).

Cross-part section moves (those in `section_moves` with action containing
"cross-part") are handled in a LATER phase, not here.

Idempotent: if a destination already exists (already-renamed), skip.

DRY-RUN by default. Pass --apply to execute.
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


def git_mv(src: Path, dst: Path, dry_run: bool) -> bool:
    """Return True on success."""
    if not src.exists():
        print(f"  SKIP (no source): {src.relative_to(ROOT)}")
        return False
    if dst.exists():
        print(f"  SKIP (already exists): {dst.relative_to(ROOT)}")
        return False
    print(f"  git mv {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    if dry_run:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "mv", str(src), str(dst)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        return False
    return True


def rename_section_files_in_module(mod_dir: Path, old_chapter: int, new_chapter: int, dry_run: bool) -> int:
    """Rename section-{old_chapter}.N.html -> section-{new_chapter}.N.html inside mod_dir."""
    if old_chapter == new_chapter:
        return 0
    count = 0
    pattern = re.compile(rf"^section-{old_chapter}\.(\d+)\.html$")
    for sec in list(mod_dir.glob("section-*.html")):
        m = pattern.match(sec.name)
        if not m:
            continue
        n = m.group(1)
        new_name = f"section-{new_chapter}.{n}.html"
        new_path = sec.parent / new_name
        if new_path.exists():
            print(f"  SKIP rename (target exists): {new_path.relative_to(ROOT)}")
            continue
        print(f"  git mv {sec.relative_to(ROOT)} -> {new_path.name}")
        if not dry_run:
            result = subprocess.run(
                ["git", "mv", str(sec), str(new_path)],
                cwd=ROOT, capture_output=True, text=True,
            )
            if result.returncode != 0:
                print(f"  ERROR: {result.stderr}")
                continue
        count += 1
    return count


def extract_chapter_num_from_slug(slug: str) -> int | None:
    """Extract chapter num from a module slug like 'module-40-ideation'."""
    m = re.match(r"module-(\d+)-", Path(slug).name)
    if m:
        return int(m.group(1))
    return None


def create_skeleton_module(entry: dict, dry_run: bool) -> bool:
    """Create a new module directory with a stub index.html."""
    dst = ROOT / entry["path"]
    if dst.exists():
        print(f"  SKIP (exists): {dst.relative_to(ROOT)}")
        return False
    print(f"  CREATE module: {dst.relative_to(ROOT)}")
    if dry_run:
        return True
    dst.mkdir(parents=True, exist_ok=True)
    # Create a placeholder index.html with the canonical template
    title = entry["title"]
    chapter_num = entry["chapter_num"]
    subtitle = entry["subtitle"]
    part_slug = dst.parent.name  # e.g., 'part-8-evaluation-production'
    part_num_m = re.match(r"part-(\d+)-", part_slug)
    part_num = part_num_m.group(1) if part_num_m else "?"
    roman = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V", "6": "VI",
             "7": "VII", "8": "VIII", "9": "IX", "10": "X", "11": "XI", "12": "XII"}.get(part_num, part_num)
    skeleton = f"""<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter {chapter_num}: {title}. {subtitle}" name="description"/>
<title>Chapter {chapter_num}: {title} | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
</head>
<body class="index-page chapter-index">
<header class="chapter-header">
<nav class="header-nav">
        <a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
        <a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">☰</span> Contents</a>
</nav>
<div class="header-search">
<div id="search"></div>
</div>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part {roman}</a><span class="bc-sep">›</span><span class="bc-current">Chapter {chapter_num}</span></div>
<h1>{title}</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {chapter_num}: {title}" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>{subtitle}</p>
</div>
<h2>Sections</h2>
<ul class="sections-list">
<!-- Section cards added by phase 60 -->
</ul>
</main>
<nav class="chapter-nav">
<!-- prev/next added by phase 60 -->
</nav>
<footer><p>Fifteenth Edition, 2026 · <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
"""
    dst_index = dst / "index.html"
    dst_index.write_text(skeleton, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    # Sort module renames so that destinations descending (avoid clobbering
    # a not-yet-renamed source that's also a destination).
    renames = list(data["module_renames"].items())
    # Two-pass: src -> __tmp_src, then __tmp_src -> dst, OR sort by destination chapter num descending.
    # Simpler: sort by dest chapter num descending so we rename module-50 before module-48.
    def sort_key(item):
        src, dst = item
        dn = extract_chapter_num_from_slug(dst)
        return -(dn or 0)
    renames.sort(key=sort_key)

    print("=== Phase 2: Module renames + skeleton creation ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)")
    print()
    print("--- Module renames ---")
    n_rename = 0
    n_section_rename = 0
    for src, dst in renames:
        src_p = ROOT / src
        dst_p = ROOT / dst
        if git_mv(src_p, dst_p, dry_run):
            n_rename += 1
            # If the slug chapter number changed, rename sections inside
            old_ch = extract_chapter_num_from_slug(src)
            new_ch = extract_chapter_num_from_slug(dst)
            if old_ch and new_ch and old_ch != new_ch:
                # In dry-run mode, the dst dir doesn't exist; use src for the section file listing
                target_dir = dst_p if (dst_p.exists() and not dry_run) else src_p
                n_section_rename += rename_section_files_in_module(target_dir, old_ch, new_ch, dry_run)

    print()
    print("--- Module deletions ---")
    n_delete = 0
    for mod in data["modules_to_delete"]:
        p = ROOT / mod
        if not p.exists():
            print(f"  SKIP (not on disk): {mod}")
            continue
        # Sections that were in this module should be moved by phase 30 first;
        # so by this point, the module dir should be empty (or contain only index.html).
        # For safety, this phase only deletes empty modules. Real deletion in phase 30.
        contents = list(p.glob("*"))
        if len(contents) <= 1:  # only index.html or empty
            print(f"  RM (empty): {mod}")
            if not dry_run:
                subprocess.run(["git", "rm", "-rf", str(p)], cwd=ROOT)
            n_delete += 1
        else:
            print(f"  DEFER (non-empty; will be cleaned in phase 30): {mod}  ({len(contents)} files)")

    print()
    print("--- New module skeletons ---")
    n_create = 0
    for entry in data["modules_to_create"]:
        if create_skeleton_module(entry, dry_run):
            n_create += 1

    print()
    print(f"=== Summary ===")
    print(f"Module renames:     {n_rename}")
    print(f"Section renames:    {n_section_rename}")
    print(f"Module deletions:   {n_delete}")
    print(f"New module skel:    {n_create}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
