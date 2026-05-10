"""
Walk the LLMBook source directory and produce the EPUB spine manifest.

Order:
  1. Front matter (in TOC order)
  2. For each part:
       part-N/index.html
       For each module in part:
         module/index.html
         module/section-*.html (in order)
  3. Capstone
  4. Appendices

Output:
  KDP/build/spine_manifest.json
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "spine_manifest.json"


def section_sort_key(p: Path) -> tuple:
    """
    Sort section-N.M.html and section-N.Ma.html and section-fm.1a.html naturally.

    Examples:
      section-0.1.html       -> (0, 1, '')
      section-fm.1.html      -> (-1, 1, '')        (front-matter sentinel)
      section-fm.1a.html     -> (-1, 1, 'a')
      section-12.10.html     -> (12, 10, '')
      section-7.3b.html      -> (7, 3, 'b')
    """
    name = p.stem  # 'section-12.10' or 'section-fm.1a'
    m = re.match(r"section-(?:fm\.)?(\d+)\.(\d+)([a-z]?)$", name)
    if not m:
        return (999, 999, name)
    if "fm" in name:
        major = -1
    else:
        major = int(m.group(1))
    minor = int(m.group(2))
    suffix = m.group(3)
    return (major, minor, suffix)


def list_sections(module_dir: Path) -> list[Path]:
    sections = sorted(module_dir.glob("section-*.html"), key=section_sort_key)
    return sections


def front_matter_order() -> list[str]:
    """Return the TOC order of front-matter pages.

    Order optimized for Amazon "Look Inside" preview (~10% of book, so the
    first ~5 pages matter most). Strategy:
      1. index           - intro page (always first)
      2. foreword        - "why this book exists"
      3. look-inside-preview - rich content excerpt (callout + code + insight)
      4. about-book      - structure + contents
      5. about-authors   - credentials (after the reader is hooked, not before)
      6. ... rest of front-matter

    Note: section-fm.1.html is excluded (website redirect stub).
    """
    fm = ROOT / "front-matter"
    candidates = [
        "index.html",
        "copyright.html",               # Legal: copyright + disclaimer + trademark + AI disclosure
        "foreword.html",                # Author foreword
        "look-inside-preview.html",     # Rich content excerpt for Look Inside
        "about-book.html",
        "about-authors.html",
        # section-fm.1.html intentionally omitted (redirect stub, no EPUB value)
        "section-fm.1a.html",
        "section-fm.1b.html",
        "section-fm.4.html",
        "section-fm.8.html",
        "pathways/index.html",
        "syllabi/index.html",
        "section-fm.5.html",
        "wisdom-council.html",
        "section-fm.7.html",
    ]
    return [f"front-matter/{name}" for name in candidates if (fm / name).exists()]


def part_order() -> list[Path]:
    parts = sorted(ROOT.glob("part-*"), key=lambda p: int(re.match(r"part-(\d+)", p.name).group(1)))
    return parts


def module_order(part_dir: Path) -> list[Path]:
    modules = sorted(
        [p for p in part_dir.iterdir() if p.is_dir() and p.name.startswith("module-")],
        key=lambda p: int(re.match(r"module-(\d+)", p.name).group(1)),
    )
    return modules


def appendix_order() -> list[Path]:
    app_root = ROOT / "appendices"
    apps = sorted(
        [p for p in app_root.iterdir() if p.is_dir() and p.name.startswith("appendix-")],
        key=lambda p: re.match(r"appendix-([a-z])", p.name).group(1),
    )
    return apps


def build_spine() -> list[dict]:
    spine: list[dict] = []

    def add(rel_path: str, kind: str, title_hint: str | None = None) -> None:
        full = ROOT / rel_path
        if not full.exists():
            print(f"  [skip] missing: {rel_path}")
            return
        spine.append({
            "path": rel_path.replace("\\", "/"),
            "kind": kind,
            "title_hint": title_hint or "",
        })

    print("Front matter:")
    for path in front_matter_order():
        add(path, "front-matter")

    print("Parts and modules:")
    for part_dir in part_order():
        part_rel = f"{part_dir.name}/index.html"
        add(part_rel, "part-index", part_dir.name)
        for module_dir in module_order(part_dir):
            mod_rel = f"{part_dir.name}/{module_dir.name}/index.html"
            add(mod_rel, "module-index", module_dir.name)
            for sec in list_sections(module_dir):
                add(f"{part_dir.name}/{module_dir.name}/{sec.name}", "section", sec.stem)

    print("Capstone:")
    cap = ROOT / "capstone"
    if (cap / "index.html").exists():
        add("capstone/index.html", "capstone-index", "capstone")
    if (cap / "requirements.html").exists():
        add("capstone/requirements.html", "capstone", "capstone-requirements")

    print("Appendices:")
    if (ROOT / "appendices" / "index.html").exists():
        add("appendices/index.html", "appendix-index", "appendices")
    for app_dir in appendix_order():
        # Each appendix folder might have an index.html and section pages
        if (app_dir / "index.html").exists():
            add(f"appendices/{app_dir.name}/index.html", "appendix", app_dir.name)
        for sec in sorted(app_dir.glob("section-*.html"), key=section_sort_key):
            add(f"appendices/{app_dir.name}/{sec.name}", "appendix-section", sec.stem)

    return spine


def main() -> int:
    spine = build_spine()
    OUT.write_text(json.dumps(spine, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT.relative_to(ROOT)} with {len(spine)} entries")

    counts: dict[str, int] = {}
    for s in spine:
        counts[s["kind"]] = counts.get(s["kind"], 0) + 1
    print("\nBreakdown by kind:")
    for k, v in sorted(counts.items()):
        print(f"  {k:20s} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
