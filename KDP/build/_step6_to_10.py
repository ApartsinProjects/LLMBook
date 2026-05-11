"""Steps 6-10: continue book restructure (deferred follow-ups).

Step 6: Move Module 35 (AI & Society leftovers) into Module 32 (Safety/Ethics)
        as 32.14-32.18. Delete Module 35 directory.
Step 7: Move Module 18 (Interpretability) directory from Part 2 -> Part 10.
Step 8: Merge Module 16 (Distillation & Merging) into Module 15 (PEFT)
        as 15.5-15.7. Delete Module 16 directory.
Step 9: Merge Module 30 (Observability) into Module 29 (Evaluation),
        filling previously-deleted gap numbers (29.5, 29.7, 29.8, 29.12).
Step 10: Slim each module-index page to a brief abstract + section list.

Run from project root:
    /c/Python314/python KDP/build/_step6_to_10.py
"""
from __future__ import annotations
import re
import sys
import shutil
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE_DIRS = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


# ---------------------------------------------------------------------------
# Move / rename helpers
# ---------------------------------------------------------------------------
def fix_relative_paths(text: str, src_path: Path, dst_path: Path) -> str:
    """Re-root href/src relative URLs from src_path to dst_path."""
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
    """Update section-number labels inside a moved file's body."""
    # H1 leading number "X.Y "
    text = re.sub(rf'>{re.escape(old_num)}(\s+|&nbsp;)', f'>{new_num}\\1', text)
    text = re.sub(rf'\bSection {re.escape(old_num)}\b', f'Section {new_num}', text)
    text = re.sub(rf'(?<![\d.]){re.escape(old_num)}(?![\d.])', new_num, text)
    return text


def perform_moves(moves: list[tuple[str, str, str | None, str | None]]) -> int:
    """Apply moves AND inbound-link rewrites.

    Each move = (src_rel, dst_rel, old_num, new_num)
    If old_num/new_num are None, no body renumbering is done.
    """
    n_moved = 0
    for src_rel, dst_rel, old_num, new_num in moves:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            print(f"  [skip] missing: {src_rel}")
            continue
        if dst.exists():
            print(f"  [skip] dest exists: {dst_rel}")
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        text = fix_relative_paths(text, src, dst)
        if old_num and new_num:
            text = renumber_inside(text, old_num, new_num)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        src.unlink()
        n_moved += 1
        print(f"  mv  {src_rel}\n   -> {dst_rel}")

    # Inbound-link rewrites
    print("\n  Rewriting inbound cross-references...")
    n_files = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for src_rel, dst_rel, _, _ in moves:
            old_base = Path(src_rel).stem  # section-35.1
            new_base = Path(dst_rel).stem  # section-32.14
            old_dir = Path(src_rel).parent.name
            new_dir = Path(dst_rel).parent.name
            old_part = Path(src_rel).parts[0]
            new_part = Path(dst_rel).parts[0]
            text = text.replace(f"{old_part}/{old_dir}/{old_base}.html",
                                f"{new_part}/{new_dir}/{new_base}.html")
            text = text.replace(f"{old_dir}/{old_base}.html",
                                f"{new_dir}/{new_base}.html")
            text = re.sub(rf'\b{re.escape(old_base)}\.html', f'{new_base}.html', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  Updated {n_files} inbound files")
    return n_moved


def move_directory(src_rel: str, dst_rel: str) -> int:
    """Move an entire directory + fix internal/external references.
    Used for whole-module moves where every file moves with no renumbering.
    """
    src = ROOT / src_rel
    dst = ROOT / dst_rel
    if not src.exists():
        print(f"  [skip] missing: {src_rel}")
        return 0
    if dst.exists():
        print(f"  [skip] dest exists: {dst_rel}")
        return 0

    # 1. Re-root internal hrefs in every file in the moved dir
    moved_files = list(src.rglob("*.html"))
    for f in moved_files:
        rel_within = f.relative_to(src)
        new_path = dst / rel_within
        text = f.read_text(encoding="utf-8", errors="replace")
        text = fix_relative_paths(text, f, new_path)
        f.write_text(text, encoding="utf-8")

    # 2. Move the directory
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    print(f"  mv  {src_rel} -> {dst_rel}")

    # 3. Rewrite inbound paths
    src_parts = Path(src_rel).parts
    dst_parts = Path(dst_rel).parts
    old_path = "/".join(src_parts)
    new_path = "/".join(dst_parts)
    n_files = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if old_path in text:
            text = text.replace(old_path, new_path)
            p.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  Updated {n_files} inbound files")
    return 1


def delete_directory(rel: str) -> None:
    d = ROOT / rel
    if d.exists():
        shutil.rmtree(d)
        print(f"  rm -r {rel}")
    else:
        print(f"  (gone) {rel}")


# ---------------------------------------------------------------------------
# Index page slim
# ---------------------------------------------------------------------------
def slim_module_index(p: Path) -> int:
    """Strip a module-index page to: title H1, first paragraph, and the
    first <ul>/<ol> (the section list). Drop everything else.

    Returns words removed (0 if no change).
    """
    text = p.read_text(encoding="utf-8", errors="replace")
    body_match = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL)
    if not body_match:
        return 0
    body = body_match.group(1)
    # Find article or container
    art = re.search(r'<article[^>]*>(.*?)</article>', body, re.DOTALL)
    block = art.group(1) if art else body

    h1 = re.search(r'<h1[^>]*>.*?</h1>', block, re.DOTALL)
    if not h1:
        return 0

    # Take everything up to the first <h2> after H1
    after_h1 = block[h1.end():]
    h2_split = re.search(r'<h2[^>]*>', after_h1)
    intro = after_h1[:h2_split.start()] if h2_split else after_h1

    # Limit intro to first paragraph
    p_match = re.search(r'<p[^>]*>.*?</p>', intro, re.DOTALL)
    intro_p = p_match.group(0) if p_match else ""

    # Find first <ul>/<ol> in entire block (TOC)
    list_match = re.search(r'<(ul|ol)[^>]*>.*?</\1>', block, re.DOTALL)
    toc_html = list_match.group(0) if list_match else ""

    new_block = h1.group(0) + "\n" + intro_p + "\n" + toc_html
    new_words = len(re.sub(r'<[^>]+>', ' ', new_block).split())
    old_words = len(re.sub(r'<[^>]+>', ' ', block).split())
    if new_words >= old_words * 0.6:
        return 0  # not enough savings; skip
    if not toc_html:
        return 0  # no TOC; don't strip

    new_text = text[:body_match.start(1)] + (
        "\n" + (f'<article>\n{new_block}\n</article>' if art else new_block) + "\n"
    ) + text[body_match.end(1):]
    p.write_text(new_text, encoding="utf-8")
    return old_words - new_words


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def step6() -> None:
    print("\n=== Step 6: Module 35 -> Module 32 ===")
    moves = [
        ("part-10-frontiers/module-35-ai-society/section-35.1.html",
         "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.14.html",
         "35.1", "32.14"),
        ("part-10-frontiers/module-35-ai-society/section-35.2.html",
         "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.15.html",
         "35.2", "32.15"),
        ("part-10-frontiers/module-35-ai-society/section-35.3.html",
         "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.16.html",
         "35.3", "32.16"),
        ("part-10-frontiers/module-35-ai-society/section-35.4.html",
         "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.17.html",
         "35.4", "32.17"),
        ("part-10-frontiers/module-35-ai-society/section-35.9.html",
         "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.18.html",
         "35.9", "32.18"),
    ]
    perform_moves(moves)
    print("  Deleting Module 35 directory:")
    delete_directory("part-10-frontiers/module-35-ai-society")


def step7() -> None:
    print("\n=== Step 7: Move Module 18 (Interpretability) Part 2 -> Part 10 ===")
    move_directory("part-2-understanding-llms/module-18-interpretability",
                   "part-10-frontiers/module-18-interpretability")


def step8() -> None:
    print("\n=== Step 8: Module 16 (Distillation) -> Module 15 (PEFT) ===")
    moves = [
        ("part-4-training-adapting/module-16-distillation-merging/section-16.1.html",
         "part-4-training-adapting/module-15-peft/section-15.5.html",
         "16.1", "15.5"),
        ("part-4-training-adapting/module-16-distillation-merging/section-16.2.html",
         "part-4-training-adapting/module-15-peft/section-15.6.html",
         "16.2", "15.6"),
        ("part-4-training-adapting/module-16-distillation-merging/section-16.3.html",
         "part-4-training-adapting/module-15-peft/section-15.7.html",
         "16.3", "15.7"),
    ]
    perform_moves(moves)
    print("  Deleting Module 16 directory:")
    delete_directory("part-4-training-adapting/module-16-distillation-merging")


def step9() -> None:
    print("\n=== Step 9: Module 30 (Observability) -> Module 29 (Evaluation) ===")
    # Fill the previously-deleted 29.x gaps
    moves = [
        ("part-8-evaluation-production/module-30-observability-monitoring/section-30.1.html",
         "part-8-evaluation-production/module-29-evaluation-observability/section-29.7.html",
         "30.1", "29.7"),
        ("part-8-evaluation-production/module-30-observability-monitoring/section-30.2.html",
         "part-8-evaluation-production/module-29-evaluation-observability/section-29.5.html",
         "30.2", "29.5"),
        ("part-8-evaluation-production/module-30-observability-monitoring/section-30.3.html",
         "part-8-evaluation-production/module-29-evaluation-observability/section-29.8.html",
         "30.3", "29.8"),
        ("part-8-evaluation-production/module-30-observability-monitoring/section-30.5.html",
         "part-8-evaluation-production/module-29-evaluation-observability/section-29.12.html",
         "30.5", "29.12"),
    ]
    perform_moves(moves)
    print("  Deleting Module 30 directory:")
    delete_directory("part-8-evaluation-production/module-30-observability-monitoring")


def step10() -> None:
    print("\n=== Step 10: Slim module-index pages ===")
    total_saved = 0
    n_slimmed = 0
    for p in ROOT.glob("part-*/module-*/index.html"):
        saved = slim_module_index(p)
        if saved > 0:
            total_saved += saved
            n_slimmed += 1
            print(f"  {saved:>5}w saved  {p.relative_to(ROOT).as_posix()}")
    for p in ROOT.glob("appendices/*/index.html"):
        saved = slim_module_index(p)
        if saved > 0:
            total_saved += saved
            n_slimmed += 1
            print(f"  {saved:>5}w saved  {p.relative_to(ROOT).as_posix()}")
    print(f"\n  Slimmed {n_slimmed} index pages, {total_saved:,} words removed")


def main() -> int:
    step6()
    step7()
    step8()
    step9()
    step10()
    return 0


if __name__ == "__main__":
    sys.exit(main())
