"""Phase 1: Part 10 split + Parts 11/12 cascade.

Steps (in order):
  1. git mv part-12-frontiers -> part-13-frontiers
  2. git mv part-11-applications-across-industries -> part-12-applications-across-industries
  3. Create part-10-llmops/ + part-11-designing-llm-products/ as new top-level dirs
     with index.html scaffolding.
  4. Move existing module-67 + module-70 from part-10-idea-to-product to part-10-llmops
     (renumbered to 50 and 53)
  5. Move existing modules 61-66, 68-69 from part-10-idea-to-product to part-11-designing
     (renumbered to 58-65)
  6. Move module-71 to part-11-designing/module-66
  7. Delete old part-10-idea-to-product/

After this script: in-file rewrites + cross-link rewrite in phases 20/30.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP = HERE / "migration-map.json"


def git_mv(src, dst, dry_run):
    if not src.exists():
        return False
    if dst.exists():
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
        if not m: continue
        new_path = sec.parent / f"section-{new_ch}.{m.group(1)}.html"
        if new_path.exists(): continue
        if not dry_run:
            subprocess.run(["git", "mv", str(sec), str(new_path)],
                          cwd=ROOT, capture_output=True, text=True)
        count += 1
    return count


def create_part_dir(part_info, dry_run):
    dst = ROOT / part_info["slug"]
    if dst.exists():
        return False
    if not dry_run:
        dst.mkdir(parents=True, exist_ok=True)
        (dst / "images").mkdir(exist_ok=True)
        roman = part_info["roman"]
        title = part_info["title"]
        sub = part_info["subtitle"]
        skel = f"""<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Part {roman}: {title}. {sub}" name="description"/>
<title>Part {roman}: {title} | Building Conversational AI with LLMs and Agents</title>
<link href="../styles/book.css" rel="stylesheet"/>
<script defer="" src="../scripts/book.js"></script>
<link href="../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../pagefind/pagefind-ui.js"></script>
</head>
<body class="index-page part-index">
<header class="chapter-header">
<nav class="header-nav">
        <a class="book-title-link" href="../index.html">Building Conversational AI with LLMs and Agents</a>
        <a class="toc-link" href="../toc.html" title="Table of Contents"><span class="toc-icon">☰</span> Contents</a>
</nav>
<div class="page-breadcrumb" data-pagefind-meta="part"><a href="../index.html">Building Conversational AI</a><span class="bc-sep">›</span><span class="bc-current">Part {roman}</span></div>
<h1>Part {roman}: {title}</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="part:Part {roman}: {title}" hidden=""></span>
<h2>Part Overview</h2>
<p>{sub}</p>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>{sub}</p>
</div>
<h2>Chapters</h2>
<div class="chapter-card-list">
<!-- Chapter cards added by rebuild script -->
</div>
</main>
<footer><p>Fifteenth Edition, 2026 · <a href="../toc.html">Contents</a></p></footer>
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

    print("=== Part 10 split phase 1 ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)\n")

    # Step 1: rename existing top-level parts (descending order)
    print("--- Cascade part renames ---")
    for src, dst in sorted(data["top_level_part_renames"].items(),
                           key=lambda x: -int(re.search(r'part-(\d+)-', x[1]).group(1))):
        src_p = ROOT / src
        dst_p = ROOT / dst
        if git_mv(src_p, dst_p, dry_run):
            print(f"  git mv {src} -> {dst}")

    # Step 2: create new top-level parts
    print("\n--- Create new top-level part dirs ---")
    for info in data["new_top_level_parts"]:
        if create_part_dir(info, dry_run):
            print(f"  CREATE: {info['slug']}")

    # Step 3: move modules to new Part 10 LLMOps
    print("\n--- Move ops modules to part-10-llmops ---")
    n_ops = 0
    for entry in data["module_moves_to_new_part_10_llmops"]:
        src = ROOT / entry["from"]
        dst = ROOT / entry["to"]
        if git_mv(src, dst, dry_run):
            print(f"  {entry['from']} -> {entry['to']}")
            n_ops += 1
            # rename section files inside if chapter num changed
            old_ch = entry["chapter_num_old"]
            new_ch = entry["chapter_num_new"]
            if old_ch != new_ch:
                target = dst if (dst.exists() and not dry_run) else src
                rename_section_files(target, old_ch, new_ch, dry_run)

    # Step 4: move modules to new Part 11 Designing
    print("\n--- Move product modules to part-11-designing-llm-products ---")
    n_prod = 0
    for entry in data["module_moves_to_new_part_11_designing"]:
        src = ROOT / entry["from"]
        dst = ROOT / entry["to"]
        if git_mv(src, dst, dry_run):
            print(f"  {entry['from']} -> {entry['to']}")
            n_prod += 1
            old_ch = entry["chapter_num_old"]
            new_ch = entry["chapter_num_new"]
            if old_ch != new_ch:
                target = dst if (dst.exists() and not dry_run) else src
                rename_section_files(target, old_ch, new_ch, dry_run)

    # Step 5: move tools module
    print("\n--- Move tools module ---")
    tools = data["tools_module_disposition"]
    src = ROOT / tools["from"]
    dst = ROOT / tools["to"]
    if git_mv(src, dst, dry_run):
        print(f"  {tools['from']} -> {tools['to']}")
        old_ch = tools["chapter_num_old"]
        new_ch = tools["chapter_num_new"]
        target = dst if (dst.exists() and not dry_run) else src
        rename_section_files(target, old_ch, new_ch, dry_run)

    # Step 6: delete old part-10-idea-to-product (only if empty after moves)
    print("\n--- Delete old part-10-idea-to-product ---")
    old_p10 = ROOT / "part-10-idea-to-product"
    if old_p10.exists():
        # Check if only index.html + images remain (no module dirs)
        leftover = [x for x in old_p10.iterdir() if x.name.startswith("module-")]
        if not leftover:
            print(f"  rm -rf {old_p10.name} (no modules left)")
            if not dry_run:
                subprocess.run(["git", "rm", "-rf", str(old_p10)],
                              cwd=ROOT, capture_output=True, text=True)
        else:
            print(f"  SKIP: {len(leftover)} modules still in old part-10-idea-to-product")

    print(f"\n=== Summary ===")
    print(f"Ops modules moved:     {n_ops}")
    print(f"Product modules moved: {n_prod}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
