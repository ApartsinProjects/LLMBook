"""Phase 1: Part 7 restructure mechanical execution.

Strategy:
  1. Cascade rename Part 8-10 modules +10 (Part 8 ch 34->44, Part 9 ch 39->49, Part 10 ch 51->61).
  2. Rename module-32-embodied-world-models -> module-41-world-models-simulation.
  3. Rename module-33-tools -> module-43-tools.
  4. Create 10 new module skeletons (32, 33, 34, 35, 36, 37, 38, 39, 40, 42).
  5. Skip module-31 rename for now (would need 31.x section renumber + content split).

Content splits DEFERRED.
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


def git_mv(src, dst, dry_run):
    if not src.exists() or dst.exists():
        return False
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ERR: {r.stderr}")
            return False
    return True


def rename_section_files(mod_dir, old_ch, new_ch, dry_run):
    if old_ch == new_ch:
        return 0
    count = 0
    pat = re.compile(rf"^section-{old_ch}\.(\d+)\.html$")
    for sec in list(mod_dir.glob("section-*.html")):
        m = pat.match(sec.name)
        if not m:
            continue
        new_path = sec.parent / f"section-{new_ch}.{m.group(1)}.html"
        if new_path.exists():
            continue
        if not dry_run:
            subprocess.run(["git", "mv", str(sec), str(new_path)],
                          cwd=ROOT, capture_output=True, text=True)
        count += 1
    return count


def create_skeleton(entry, part_roman, part_title, dry_run):
    dst = ROOT / entry["path"]
    if dst.exists():
        return False
    if not dry_run:
        dst.mkdir(parents=True, exist_ok=True)
        title = entry["title"]
        ch = entry["chapter_num"]
        sub = entry["subtitle"]
        skel = f"""<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter {ch}: {title}. {sub}" name="description"/>
<title>Chapter {ch}: {title} | Building Conversational AI with LLMs and Agents</title>
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
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part {part_roman}: {part_title}</a><span class="bc-sep">›</span><span class="bc-current">Chapter {ch}</span></div>
<h1>{title}</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {ch}: {title}" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>{sub}</p>
</div>
<h2>Sections</h2>
<ul class="sections-list">
<!-- Sections to be added when content lands -->
</ul>
</main>
<nav class="chapter-nav">
</nav>
<footer><p>Fifteenth Edition, 2026 · <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
"""
        (dst / "index.html").write_text(skel, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    print(f"=== Part 7 Restructure Phase 1 ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)\n")

    # Cascade module renames descending
    renames = list(data["module_renames"].items())
    renames.sort(key=lambda x: -(int(re.search(r"module-(\d+)-", x[1]).group(1))))
    n_ren = 0
    n_sec_ren = 0
    for src, dst in renames:
        src_p = ROOT / src
        dst_p = ROOT / dst
        old_m = re.search(r"module-(\d+)-", src)
        new_m = re.search(r"module-(\d+)-", dst)
        if not (old_m and new_m): continue
        old_ch = int(old_m.group(1))
        new_ch = int(new_m.group(1))
        if git_mv(src_p, dst_p, dry_run):
            n_ren += 1
            target = dst_p if (dst_p.exists() and not dry_run) else src_p
            n_sec_ren += rename_section_files(target, old_ch, new_ch, dry_run)

    # New module skeletons
    for entry in data["modules_to_create"]:
        if create_skeleton(entry, "VII", "Multimodal Generation", dry_run):
            print(f"  CREATE: {entry['path']}")

    print(f"\n=== Summary ===")
    print(f"Module renames:     {n_ren}")
    print(f"Section renames:    {n_sec_ren}")
    print(f"Module skeletons:   {len(data['modules_to_create'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
