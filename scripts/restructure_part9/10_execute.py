"""Phase 1: execute Part 9 restructure.

Strategy:
  1. Cascade rename module-40 -> module-41, module-41 -> module-50 (Part 9)
     plus part-10 modules 42-52 -> 51-61 (+9 each).
  2. Create 9 new module skeletons (40, 42-49).
  3. Wholesale move 10 sections to new homes (no splits this phase).
  4. Rename old module-39 -> module-39-adversarial-security-red-team
     (which retains 39.1 and 39.8).
  5. Update section file metadata (title/breadcrumb/page-current).
  6. DEFER content splits (39.1/39.2/39.3 etc.) and net-new authoring.

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


def git_mv(src, dst, dry_run):
    if not src.exists():
        return False
    if dst.exists():
        return False
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(["git", "mv", str(src), str(dst)],
                                 cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr}")
            return False
    return True


def rename_section_files_in_module(mod_dir, old_ch, new_ch, dry_run):
    if old_ch == new_ch:
        return 0
    count = 0
    pattern = re.compile(rf"^section-{old_ch}\.(\d+)\.html$")
    for sec in list(mod_dir.glob("section-*.html")):
        m = pattern.match(sec.name)
        if not m:
            continue
        new_name = f"section-{new_ch}.{m.group(1)}.html"
        new_path = sec.parent / new_name
        if new_path.exists():
            continue
        if not dry_run:
            subprocess.run(["git", "mv", str(sec), str(new_path)],
                          cwd=ROOT, capture_output=True, text=True)
        count += 1
    return count


def create_skeleton(entry, dry_run):
    dst = ROOT / entry["path"]
    if dst.exists():
        return False
    if not dry_run:
        dst.mkdir(parents=True, exist_ok=True)
        title = entry["title"]
        ch = entry["chapter_num"]
        sub = entry["subtitle"]
        part_slug = dst.parent.name
        part_num_m = re.match(r"part-(\d+)-", part_slug)
        part_num = part_num_m.group(1) if part_num_m else "?"
        roman = {"9": "IX"}.get(part_num, part_num)
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
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part {roman}: LLM Safety, Security, and Ethics</a><span class="bc-sep">›</span><span class="bc-current">Chapter {ch}</span></div>
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
<!-- Section cards added by phase 60 once content lands -->
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


def rewrite_section_metadata(text, old_path, new_path, title_new, new_chapter_title, new_chapter_num):
    """Rewrite section metadata for cross-module move within Part 9."""
    new_name = new_path.split("/")[-1]
    src_name = old_path.split("/")[-1]
    src_m = re.match(r"section-(\d+)\.(\d+)\.html", src_name)
    dst_m = re.match(r"section-(\d+)\.(\d+)\.html", new_name)
    if not (src_m and dst_m):
        return text
    src_ch, src_n = int(src_m.group(1)), int(src_m.group(2))
    dst_ch, dst_n = int(dst_m.group(1)), int(dst_m.group(2))

    text = re.sub(rf'<title>Section {src_ch}\.{src_n}:?[^<]*</title>',
                   f'<title>Section {dst_ch}.{dst_n}: {title_new}</title>', text, count=1)
    text = re.sub(r'<h1>[^<]+</h1>', f'<h1>{title_new}</h1>', text, count=1)
    text = re.sub(rf'<div class="page-current">Section {src_ch}\.{src_n}</div>',
                   f'<div class="page-current">Section {dst_ch}.{dst_n}</div>', text)
    text = re.sub(rf'\b(?:Chapter|chapter) {src_ch}\b', f'Chapter {dst_ch}', text)
    text = re.sub(rf'\bSection {src_ch}\.{src_n}\b',
                   f'Section {dst_ch}.{dst_n}', text)
    # Chapter title in breadcrumb
    text = re.sub(r'<a href="index\.html">Chapter \d+:[^<]+</a>',
                   f'<a href="index.html">Chapter {dst_ch}: {new_chapter_title}</a>', text)
    text = re.sub(r'data-pagefind-meta="chapter:Chapter \d+:[^"]+"',
                   f'data-pagefind-meta="chapter:Chapter {dst_ch}: {new_chapter_title}"', text)
    # Anchor IDs
    text = re.sub(rf'\bid="{src_ch}-{src_n}-', f'id="{dst_ch}-{dst_n}-', text)
    text = re.sub(rf'#{src_ch}-{src_n}-', f'#{dst_ch}-{dst_n}-', text)
    # H2/h3 prefixes
    for tag in ('h2', 'h3', 'h4'):
        text = re.sub(rf'(<{tag}[^>]*>){src_ch}\.{src_n}\.',
                      rf'\g<1>{dst_ch}.{dst_n}.', text)
    # Caption labels
    for label in ['Code Fragment', 'Figure', 'Table', 'Listing']:
        text = re.sub(rf'\b{label} {src_ch}\.{src_n}\.',
                       f'{label} {dst_ch}.{dst_n}.', text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    print("=== Part 9 Restructure: Phase 1 ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)\n")

    # Step 1: cascade module renames (descending chapter num)
    print("--- Cascade module renames ---")
    renames = list(data["module_renames"].items())
    def sort_key(item):
        _, dst = item
        m = re.search(r"module-(\d+)-", dst)
        return -(int(m.group(1)) if m else 0)
    renames.sort(key=sort_key)
    n_rename = 0
    n_sec_rename = 0
    for src, dst in renames:
        src_p = ROOT / src
        dst_p = ROOT / dst
        old_m = re.search(r"module-(\d+)-", src)
        new_m = re.search(r"module-(\d+)-", dst)
        if not (old_m and new_m): continue
        old_ch = int(old_m.group(1))
        new_ch = int(new_m.group(1))
        if git_mv(src_p, dst_p, dry_run):
            print(f"  git mv {src} -> {dst}")
            n_rename += 1
            if old_ch != new_ch and not dry_run:
                target_dir = dst_p if dst_p.exists() else src_p
                n_sec_rename += rename_section_files_in_module(target_dir, old_ch, new_ch, dry_run)
            elif old_ch != new_ch and dry_run:
                # Estimate
                if src_p.exists():
                    n_sec_rename += rename_section_files_in_module(src_p, old_ch, new_ch, True)

    # Step 2: create new modules
    print("\n--- New module skeletons ---")
    n_create = 0
    for entry in data["modules_to_create"]:
        if create_skeleton(entry, dry_run):
            print(f"  CREATE: {entry['path']}")
            n_create += 1

    # Step 3: wholesale section moves
    print("\n--- Wholesale section moves ---")
    new_chapter_titles = {e["path"].split("/")[-1]: e["title"]
                          for e in data["modules_to_create"]}
    n_moved = 0
    for entry in data["wholesale_section_moves"]:
        src = ROOT / entry["from"]
        dst = ROOT / entry["to"]
        if not src.exists():
            print(f"  SKIP (no src): {entry['from']}")
            continue
        if dst.exists():
            print(f"  SKIP (dst exists): {entry['to']}")
            continue
        print(f"  git mv {entry['from']} -> {entry['to']}")
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(["git", "mv", str(src), str(dst)],
                              cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"  ERROR: {r.stderr}")
                continue
            dst_mod = entry["to"].split("/")[-2]
            new_chapter_title = new_chapter_titles.get(dst_mod, "?")
            new_chapter_num_m = re.search(r"module-(\d+)-", dst_mod)
            new_chapter_num = int(new_chapter_num_m.group(1)) if new_chapter_num_m else 0
            text = dst.read_text(encoding="utf-8")
            text = rewrite_section_metadata(
                text, entry["from"], entry["to"],
                entry["title_new"], new_chapter_title, new_chapter_num,
            )
            dst.write_text(text, encoding="utf-8")
        n_moved += 1

    # Step 4: rename old module-39 to adversarial-security-red-team
    print("\n--- Rename module-39 to adversarial-security-red-team ---")
    src39 = ROOT / "part-9-safety-security-ethics/module-39-safety-ethics-regulation"
    dst39 = ROOT / "part-9-safety-security-ethics/module-39-adversarial-security-red-team"
    if src39.exists() and not dst39.exists():
        print(f"  git mv module-39-safety-ethics-regulation -> module-39-adversarial-security-red-team")
        if not dry_run:
            subprocess.run(["git", "mv", str(src39), str(dst39)],
                          cwd=ROOT, capture_output=True, text=True)
            # Update index.html title
            idx = dst39 / "index.html"
            if idx.exists():
                t = idx.read_text(encoding="utf-8")
                t = re.sub(r'<h1>[^<]+</h1>',
                          '<h1>Adversarial Security and Red Teaming</h1>',
                          t, count=1)
                idx.write_text(t, encoding="utf-8")

    print(f"\n=== Summary ===")
    print(f"Module renames:     {n_rename}")
    print(f"Section renames:    {n_sec_rename}")
    print(f"New module skel:    {n_create}")
    print(f"Sections moved:     {n_moved}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
