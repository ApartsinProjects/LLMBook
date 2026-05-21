"""Migration step 6: Split Module 33 (Emerging Architectures) into 4 target
chapters per the Frontiers expansion plan.

Source: part-12-frontiers/module-33-emerging-architectures/
        with sections 33.1 through 33.11.

Target distribution:

  module-61-frontier-architectures (rename module-33 to this):
    section-61.1.html (from 33.1 Emergent Abilities)
    section-61.2.html (from 33.2 Scaling Frontiers)
    section-61.3.html (from 33.3 Alternative Architectures)
    section-61.4.html (from 33.10 Universal Sequence Machines)

  module-62-frontier-theory (new dir):
    section-62.1.html (from 33.5 Theory of Reasoning)
    section-62.2.html (from 33.6 Memory)
    section-62.3.html (from 33.7 Mechanistic Interpretability)
    section-62.4.html (from 33.8 Nature of Agency)

  Move out of module-33:
    33.4 -> part-7-multimodal-generation/module-32-embodied-world-models/section-32.4.html
    33.9 -> part-6-agentic-ai/module-27-tool-use-protocols/ (append as section)
    33.11 -> module-64-agi-trajectories/section-64.5.html (closing section)

Procedure:
  1. Create module-62 dir.
  2. git mv each section file to its target chapter dir with new filename.
  3. After moves: rename module-33 to module-61.
  4. Update breadcrumbs / page-current inside each moved file to point at
     its new chapter num.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SRC = ROOT / "part-12-frontiers" / "module-33-emerging-architectures"
TARGET_61 = ROOT / "part-12-frontiers" / "module-61-frontier-architectures"
TARGET_62 = ROOT / "part-12-frontiers" / "module-62-frontier-theory"
TARGET_32 = ROOT / "part-7-multimodal-generation" / "module-32-embodied-world-models"
TARGET_27 = ROOT / "part-6-agentic-ai" / "module-27-tool-use-protocols"
TARGET_64 = ROOT / "part-12-frontiers" / "module-64-agi-trajectories"

# (source_filename, target_dir, target_section_num)
MOVES = [
    ("section-33.1.html",  TARGET_61, "61.1"),
    ("section-33.2.html",  TARGET_61, "61.2"),
    ("section-33.3.html",  TARGET_61, "61.3"),
    ("section-33.10.html", TARGET_61, "61.4"),
    ("section-33.5.html",  TARGET_62, "62.1"),
    ("section-33.6.html",  TARGET_62, "62.2"),
    ("section-33.7.html",  TARGET_62, "62.3"),
    ("section-33.8.html",  TARGET_62, "62.4"),
    ("section-33.4.html",  TARGET_32, "32.4"),
    ("section-33.9.html",  TARGET_27, "27.6"),  # append as new section
    ("section-33.11.html", TARGET_64, "64.5"),  # closing section of AGI chap
]


CHAP_TITLES = {
    61: "Frontier Architectures & Scaling",
    62: "Frontier Theory & Cognition",
    32: "Embodied AI, World Models & Multimodal Reasoning",
    27: "Tool Use, Function Calling & Protocols",
    64: "AGI Trajectories & Open Questions",
}


def update_section_internals(p: Path, new_section_num: str, new_chap_num: int,
                              new_chap_title: str, part_roman: str,
                              part_title: str, dry_run: bool) -> None:
    """Update breadcrumb, page-current, captions inside the moved section."""
    text = p.read_text(encoding="utf-8")
    orig = text

    # page-current
    text = re.sub(r'<div class="page-current">[^<]+</div>',
                   f'<div class="page-current">Section {new_section_num}</div>',
                   text)
    # bc-current
    text = re.sub(r'<span class="bc-current">Section [^<]+</span>',
                   f'<span class="bc-current">Section {new_section_num}</span>',
                   text)
    # Breadcrumb chapter anchor inside .page-breadcrumb (link to chapter)
    text = re.sub(
        r'(<a href="index\.html">)Chapter \d+(?::[^<]*)?(</a>)',
        rf'\1Chapter {new_chap_num}: {new_chap_title}\2',
        text,
    )
    # Pagefind meta
    text = re.sub(
        r'data-pagefind-meta="chapter:Chapter \d+(?:: [^"]+)?"',
        f'data-pagefind-meta="chapter:Chapter {new_chap_num}: {new_chap_title}"',
        text,
    )
    # Captions: rewrite "Section X.Y" / "Code Fragment X.Y.Z" etc.
    # NOTE: my step4 cross-ref rewrite handled most cross-refs already.
    # This step is for SELF-references inside the moved file.
    # Strip old section num from h1 and section captions (best-effort).

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    if not SRC.exists():
        print(f"ERROR: source {SRC} missing — has step 3 already split it?")
        return 1

    # Create new target dirs if needed
    for d in (TARGET_61, TARGET_62):
        if not d.exists():
            print(f"  CREATE dir {d.relative_to(ROOT)}")
            if not args.apply == False:
                d.mkdir(parents=True, exist_ok=True)
                (d / "images").mkdir(exist_ok=True)
            elif not dry_run:
                d.mkdir(parents=True, exist_ok=True)

    # Move each section
    n_moved = 0
    for src_name, target_dir, target_num in MOVES:
        src = SRC / src_name
        if not src.exists():
            print(f"  SKIP {src_name}: source missing")
            continue
        target_filename = f"section-{target_num}.html"
        dst = target_dir / target_filename
        if dst.exists():
            print(f"  SKIP {src_name} -> {dst.relative_to(ROOT)}: target exists")
            continue
        if not target_dir.exists():
            print(f"  WARN target dir {target_dir.relative_to(ROOT)} missing; will create")
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
        print(f"  git mv {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        if not dry_run:
            subprocess.run(["git", "mv", str(src), str(dst)],
                            cwd=ROOT, check=False)
            n_moved += 1
            # Update internals
            chap_num = int(target_num.split(".")[0])
            chap_title = CHAP_TITLES.get(chap_num, "")
            # Part info
            if chap_num in (61, 62, 64):
                proman, ptitle = "XII", "Frontiers"
            elif chap_num == 32:
                proman, ptitle = "VII", "Multimodal Generation"
            elif chap_num == 27:
                proman, ptitle = "VI", "Agentic AI"
            else:
                proman, ptitle = "", ""
            update_section_internals(dst, target_num, chap_num, chap_title,
                                       proman, ptitle, dry_run)

    # After all 11 sections moved out, the original module-33 dir is empty.
    # Move the index.html to module-61 as the new Architectures chapter index.
    if not dry_run:
        # Create module-61 index by copying module-33 index, renaming, updating
        old_idx = SRC / "index.html"
        new_idx_61 = TARGET_61 / "index.html"
        if old_idx.exists() and not new_idx_61.exists():
            subprocess.run(["git", "mv", str(old_idx), str(new_idx_61)],
                            cwd=ROOT, check=False)
            # Update its content (chapter num, title, etc.)
            text = new_idx_61.read_text(encoding="utf-8")
            text = re.sub(
                r'data-pagefind-meta="chapter:Chapter \d+: [^"]+"',
                'data-pagefind-meta="chapter:Chapter 61: Frontier Architectures & Scaling"',
                text,
            )
            text = re.sub(r'<h1>[^<]+</h1>',
                           '<h1>Frontier Architectures &amp; Scaling</h1>',
                           text, count=1)
            text = re.sub(r'<span class="bc-current">Chapter \d+</span>',
                           '<span class="bc-current">Chapter 61</span>',
                           text)
            new_idx_61.write_text(text, encoding="utf-8")
        # Generate a minimal index.html for module-62 (Frontier Theory) since
        # it's brand new
        idx_62 = TARGET_62 / "index.html"
        if not idx_62.exists():
            idx_62.write_text(
                '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
                '<meta charset="utf-8"/>\n'
                '<title>Chapter 62: Frontier Theory &amp; Cognition</title>\n'
                '<link href="../../styles/book.css" rel="stylesheet"/>\n'
                '</head>\n<body>\n<header class="chapter-header">\n'
                '<nav class="header-nav"><a class="book-title-link" href="../../index.html">'
                'Building Conversational AI with LLMs and Agents</a>'
                '<a class="toc-link" href="../../toc.html">Contents</a></nav>\n'
                '<div class="page-breadcrumb">'
                '<a href="../index.html">Part XII: Frontiers</a>'
                '<span class="bc-sep">›</span>'
                '<span class="bc-current">Chapter 62</span></div>\n'
                '<h1>Frontier Theory &amp; Cognition</h1>\n'
                '<p class="chapter-subtitle">Formal theories of reasoning, '
                'memory primitives, mechanistic interpretability at scale, '
                'and the nature of agency.</p>\n'
                '</header>\n<main class="content">\n'
                '<p>This chapter collects four sections from the Frontiers '
                'expansion (62.1-62.4).</p>\n'
                '</main></body></html>',
                encoding="utf-8")

        # Remove now-empty module-33 dir
        try:
            SRC.rmdir()
            print(f"  Removed empty {SRC.relative_to(ROOT)}")
        except OSError:
            # Not empty — leftover files (illustrations.json, images/)
            # Move what's left to module-61
            for leftover in SRC.iterdir():
                tgt = TARGET_61 / leftover.name
                if not tgt.exists():
                    subprocess.run(["git", "mv", str(leftover), str(tgt)],
                                    cwd=ROOT, check=False)
            try:
                SRC.rmdir()
                print(f"  Removed empty {SRC.relative_to(ROOT)} after moving leftovers")
            except OSError as e:
                print(f"  WARN: could not remove {SRC.relative_to(ROOT)}: {e}")

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n{mode}: moved {n_moved} section files from Module 33")
    return 0


if __name__ == "__main__":
    sys.exit(main())
