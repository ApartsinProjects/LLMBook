"""v3.4 #3: Merge Module 37 (Building & Steering AI Products) into
Module 36 (Idea-to-Product) as sections 36.5 .. 36.9.

Module 36 currently has 4 sections; absorbs 5 sections from 37:
  37.1 Observe-Steer Development Loop      -> 36.5
  37.2 The Founder's Prototype Loop        -> 36.6
  37.3 Documentation as Control Surface    -> 36.7
  37.4 AI Coding Assistants                -> 36.8
  37.5 From Prototype to MVP               -> 36.9

Module 37 directory deleted. Module 38 stays as 38 (Shipping & Scaling
is a distinct phase from Build).

After this, Module 36 becomes "From Prototype to Production" with 9
sections covering the full product-build journey.
"""
from __future__ import annotations
import re
import sys
import shutil
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

MOVES = [
    ("part-11-idea-to-product/module-37-building-steering/section-37.1.html",
     "part-11-idea-to-product/module-36-idea-to-product/section-36.5.html",
     "37.1", "36.5"),
    ("part-11-idea-to-product/module-37-building-steering/section-37.2.html",
     "part-11-idea-to-product/module-36-idea-to-product/section-36.6.html",
     "37.2", "36.6"),
    ("part-11-idea-to-product/module-37-building-steering/section-37.3.html",
     "part-11-idea-to-product/module-36-idea-to-product/section-36.7.html",
     "37.3", "36.7"),
    ("part-11-idea-to-product/module-37-building-steering/section-37.4.html",
     "part-11-idea-to-product/module-36-idea-to-product/section-36.8.html",
     "37.4", "36.8"),
    ("part-11-idea-to-product/module-37-building-steering/section-37.5.html",
     "part-11-idea-to-product/module-36-idea-to-product/section-36.9.html",
     "37.5", "36.9"),
]


def fix_relative_paths(text: str, src_path: Path, dst_path: Path) -> str:
    src_parent = src_path.parent
    dst_parent = dst_path.parent

    def _rewrite(match: re.Match) -> str:
        attr = match.group(1)
        url = match.group(2)
        if url.startswith(("http://", "https://", "mailto:", "javascript:", "#", "data:")):
            return match.group(0)
        try:
            anchor = ""
            if "#" in url:
                url_clean, anchor = url.split("#", 1)
                anchor = "#" + anchor
            else:
                url_clean = url
            if not url_clean:
                return match.group(0)
            target = (src_parent / url_clean).resolve()
            new_rel = os.path.relpath(str(target), str(dst_parent.resolve())).replace("\\", "/")
            return f'{attr}="{new_rel}{anchor}"'
        except Exception:
            return match.group(0)

    return re.sub(r'(href|src)="([^"]+)"', _rewrite, text)


def renumber_inside(text: str, old_num: str, new_num: str) -> str:
    text = re.sub(rf'>{re.escape(old_num)}(\s+|&nbsp;)', f'>{new_num}\\1', text)
    text = re.sub(rf'\bSection {re.escape(old_num)}\b', f'Section {new_num}', text)
    text = re.sub(rf'(?<![\d.]){re.escape(old_num)}(?![\d.])', new_num, text)
    return text


def main() -> int:
    moved = 0
    for src_rel, dst_rel, old, new in MOVES:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists() or dst.exists():
            print(f"  [skip] {src_rel} -> {dst_rel}")
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        text = fix_relative_paths(text, src, dst)
        text = renumber_inside(text, old, new)
        dst.write_text(text, encoding="utf-8")
        src.unlink()
        moved += 1
        print(f"  mv  {src_rel} -> {dst_rel}")

    # Inbound rewrites
    n_files = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for src_rel, dst_rel, old, new in MOVES:
            old_base = Path(src_rel).stem
            new_base = Path(dst_rel).stem
            old_dir = Path(src_rel).parent.name
            new_dir = Path(dst_rel).parent.name
            text = text.replace(f"{old_dir}/{old_base}.html", f"{new_dir}/{new_base}.html")
            text = re.sub(rf'\b{re.escape(old_base)}\.html', f'{new_base}.html', text)
            text = re.sub(rf'\bSection {re.escape(old)}\b', f'Section {new}', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  Updated {n_files} inbound files")

    # Delete module 37 directory
    mod37 = ROOT / "part-11-idea-to-product/module-37-building-steering"
    if mod37.exists():
        shutil.rmtree(mod37)
        print(f"  rm -r {mod37.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
