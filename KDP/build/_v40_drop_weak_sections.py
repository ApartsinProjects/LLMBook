"""v4.0: Drop 3 weak sections from Modules 36 + 38 (audit-supported).

  36.4 'Case Studies: Role Assignment in Practice' (4220w) - case studies date fast
  36.8 'AI Coding Assistants: Trust but Verify' (4320w) - overlaps Module 25
  38.5 'Capstone Lab and Assessment'         (1715w) - overlaps Module 31 labs

After deletes:
  Module 36: 9 -> 7 sections (renumber 36.5-9 to fill gaps)
  Module 38: 5 -> 4 sections (no renumber needed; .5 is at end)

Inbound xrefs redirected to nearest survivor.
"""
from __future__ import annotations
import re
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def update_inbound(redirects: list[tuple[str, str]]) -> int:
    n = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        try:
            if p.stat().st_size > 5_000_000: continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        original = text
        for old, new in redirects:
            text = re.sub(rf'\b{re.escape(old)}\.html', f'{new}.html', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n += 1
    return n


def delete_with_redirect(rel: str, target_basename: str) -> None:
    p = ROOT / rel
    if not p.exists():
        print(f"  [skip] {rel} missing")
        return
    old_base = p.stem
    n = update_inbound([(old_base, target_basename)])
    p.unlink()
    print(f"  rm {rel} -> redirected {n} files to {target_basename}")


def renumber_section(src_rel: str, new_num: str) -> None:
    src = ROOT / src_rel
    dst = src.parent / f"section-{new_num}.html"
    if not src.exists() or dst.exists(): return
    text = src.read_text(encoding="utf-8", errors="replace")
    old_num = src.stem.split("-")[1]
    text = re.sub(rf'>{re.escape(old_num)}(\s+|&nbsp;)', rf'>{new_num}\1', text)
    text = re.sub(rf'\bSection {re.escape(old_num)}\b', f'Section {new_num}', text)
    dst.write_text(text, encoding="utf-8")
    src.unlink()
    n = update_inbound([(src.stem, dst.stem)])
    print(f"  mv {src.name} -> {dst.name} ({n} cross-refs updated)")


def main() -> int:
    print("=== Drop weak sections ===")
    delete_with_redirect("part-11-idea-to-product/module-36-idea-to-product/section-36.4.html", "section-36.3")
    delete_with_redirect("part-11-idea-to-product/module-36-idea-to-product/section-36.8.html", "section-36.7")
    delete_with_redirect("part-11-idea-to-product/module-38-shipping-scaling/section-38.5.html", "section-38.4")

    print("\n=== Renumber Module 36 to close gaps (36.5..9 -> 36.4..7) ===")
    # After deleting 36.4 and 36.8: existing files are 36.1, 36.2, 36.3, 36.5, 36.6, 36.7, 36.9
    # Renumber 36.5->36.4, 36.6->36.5, 36.7->36.6, 36.9->36.7
    for old, new in [(5, 4), (6, 5), (7, 6), (9, 7)]:
        renumber_section(f"part-11-idea-to-product/module-36-idea-to-product/section-36.{old}.html",
                         f"36.{new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
