"""Hero/opener image audit for landing pages (READ-ONLY).

Scans every landing page in the LLMBook for the presence (or absence) of a
prominent "opener" image, defined as a <figure> or top-level <img> appearing
BEFORE the first <h2> heading inside the <main> content region.

Landing pages audited:
  * Part landings:        part-N/index.html
  * Chapter landings:     part-N/module-MM/index.html
  * Appendix landings:    appendices/appendix-X/index.html
  * Front-matter pages:   front-matter/*.html  (including index.html)

For each landing page we record:
  * has_opener            (figure/img before first h2)
  * opener_src            (relative path of the image)
  * opener_size_bytes     (file size on disk)
  * opener_dimensions     (width x height in pixels, via PIL)
  * opener_alt            (alt text or "<missing>")
  * other_figure_count    (other <figure>/<img> count anywhere in <main>)

Categorization:
  * HAS opener image
  * NO opener image  (subdivided into "barren" pages with zero other figures)

The script is READ-ONLY: no files are written or modified.

Excluded directories: KDP/, .claude/, node_modules/, build/, temp_*, pagefind/,
templates/, scripts/, vendor/, __pycache__/, source_fix_backups/.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup, Tag

try:
    from PIL import Image
except ImportError:
    Image = None

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIR_NAMES = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    "build", ".git", "source_fix_backups", "__pycache__", "vendor",
    "_concept-figs", "images", "downloads", "agents",
}
SKIP_PREFIXES = ("temp_",)


def is_skipped(path: Path) -> bool:
    """True if any path component is in the skip list."""
    for part in path.parts:
        if part in SKIP_DIR_NAMES:
            return True
        for prefix in SKIP_PREFIXES:
            if part.startswith(prefix):
                return True
    return False


def find_landing_pages() -> dict[str, list[Path]]:
    """Return landing pages grouped by category."""
    landings: dict[str, list[Path]] = {
        "part": [],
        "chapter": [],
        "appendix": [],
        "front-matter": [],
    }

    # Part landings: part-N-*/index.html
    for p in sorted(ROOT.glob("part-*/index.html")):
        if is_skipped(p):
            continue
        landings["part"].append(p)

    # Chapter landings: part-N-*/module-MM-*/index.html
    for p in sorted(ROOT.glob("part-*/module-*/index.html")):
        if is_skipped(p):
            continue
        landings["chapter"].append(p)

    # Appendix landings: appendices/appendix-X-*/index.html and appendices/index.html
    for p in sorted(ROOT.glob("appendices/appendix-*/index.html")):
        if is_skipped(p):
            continue
        landings["appendix"].append(p)
    app_index = ROOT / "appendices" / "index.html"
    if app_index.exists():
        landings["appendix"].insert(0, app_index)

    # Front-matter: front-matter/*.html
    fm_dir = ROOT / "front-matter"
    if fm_dir.exists():
        for p in sorted(fm_dir.glob("*.html")):
            if is_skipped(p):
                continue
            landings["front-matter"].append(p)

    return landings


def analyze_landing(path: Path) -> dict:
    """Return analysis dict for a single landing page."""
    html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    # The "content" region is everything in <main>, falling back to <body>.
    main = soup.find("main") or soup.find("body")
    if main is None:
        return {
            "path": path,
            "has_opener": False,
            "reason": "no <main> or <body>",
            "other_figure_count": 0,
            "first_h2_found": False,
        }

    # Find first h2 (it marks the end of "above the fold" content).
    first_h2 = main.find("h2")

    # Look for first figure/img that appears BEFORE the first h2.
    opener: Tag | None = None
    opener_kind: str | None = None
    for elem in main.descendants:
        if not isinstance(elem, Tag):
            continue
        if first_h2 is not None and elem is first_h2:
            break
        if elem.name == "figure":
            opener = elem
            opener_kind = "figure"
            break
        if elem.name == "img":
            # Skip tiny inline agent avatars used in epigraphs.
            parent_classes: set[str] = set()
            for p in elem.parents:
                if isinstance(p, Tag):
                    parent_classes.update(p.get("class", []) or [])
            if "agent-avatar-inline" in parent_classes:
                continue
            # Skip nav/header icons.
            if "header" in parent_classes or "nav" in parent_classes:
                continue
            opener = elem
            opener_kind = "img"
            break

    # Count other figures/imgs in main (excluding the opener and tiny avatars).
    all_figs = main.find_all("figure")
    all_imgs = [
        i for i in main.find_all("img")
        if not any(
            "agent-avatar-inline" in (p.get("class", []) or [])
            for p in i.parents if isinstance(p, Tag)
        )
    ]
    other_figure_count = max(0, len(all_figs) + max(0, len(all_imgs) - len(all_figs)) - (1 if opener else 0))
    # Simpler: count figures + standalone imgs minus opener if opener is fig/img.
    other_figs = len(all_figs) - (1 if opener_kind == "figure" else 0)
    # Standalone <img> not inside any <figure>.
    standalone_imgs = [
        i for i in all_imgs
        if not any(isinstance(p, Tag) and p.name == "figure" for p in i.parents)
    ]
    other_standalone = len(standalone_imgs) - (1 if opener_kind == "img" else 0)
    other_figure_count = max(0, other_figs) + max(0, other_standalone)

    result: dict = {
        "path": path,
        "has_opener": opener is not None,
        "opener_kind": opener_kind,
        "other_figure_count": other_figure_count,
        "first_h2_found": first_h2 is not None,
    }

    if opener is not None:
        img_tag = opener.find("img") if opener_kind == "figure" else opener
        if img_tag is not None and isinstance(img_tag, Tag):
            src = img_tag.get("src", "")
            alt = img_tag.get("alt", None)
            result["opener_src"] = src
            result["opener_alt"] = alt if alt is not None else "<missing>"
            result["opener_alt_present"] = alt is not None and len(alt.strip()) > 0

            # Resolve the image path relative to the HTML file.
            if src and not src.startswith(("http://", "https://", "data:")):
                img_path = (path.parent / src).resolve()
                result["opener_resolved_path"] = img_path
                if img_path.exists():
                    try:
                        result["opener_size_bytes"] = img_path.stat().st_size
                    except OSError:
                        result["opener_size_bytes"] = None
                    if Image is not None:
                        try:
                            with Image.open(img_path) as im:
                                result["opener_dimensions"] = im.size
                        except Exception:
                            result["opener_dimensions"] = None
                    else:
                        result["opener_dimensions"] = None
                else:
                    result["opener_size_bytes"] = None
                    result["opener_dimensions"] = None
                    result["opener_missing_file"] = True
        else:
            result["opener_src"] = "<inline svg or other>"
            result["opener_alt"] = "<n/a>"

    return result


def fmt_bytes(n: int | None) -> str:
    if n is None:
        return "?"
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f}KB"
    return f"{n / (1024 * 1024):.2f}MB"


def fmt_dims(d) -> str:
    if not d:
        return "?"
    return f"{d[0]}x{d[1]}"


def relpath(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def print_section(title: str, rows: list[dict]) -> None:
    print(f"\n=== {title} ({len(rows)} pages) ===")
    for r in rows:
        rp = relpath(r["path"])
        if r["has_opener"]:
            size = fmt_bytes(r.get("opener_size_bytes"))
            dims = fmt_dims(r.get("opener_dimensions"))
            alt = r.get("opener_alt", "<missing>") or "<empty>"
            alt_status = "OK" if r.get("opener_alt_present") else "MISSING/EMPTY"
            src = r.get("opener_src", "?")
            print(f"  [HAS]   {rp}")
            print(f"          src={src} ({dims}, {size}, alt={alt_status})")
        else:
            barren = " [BARREN: no other figs]" if r["other_figure_count"] == 0 else f" (has {r['other_figure_count']} other figs)"
            print(f"  [NO]    {rp}{barren}")


def main() -> int:
    landings = find_landing_pages()

    all_results: dict[str, list[dict]] = {}
    for category, pages in landings.items():
        results = [analyze_landing(p) for p in pages]
        all_results[category] = results

    # Print per-category sections.
    label = {
        "part": "PART LANDINGS",
        "chapter": "CHAPTER LANDINGS",
        "appendix": "APPENDIX LANDINGS",
        "front-matter": "FRONT-MATTER PAGES",
    }
    for cat in ("part", "chapter", "appendix", "front-matter"):
        print_section(label[cat], all_results.get(cat, []))

    # Summary stats.
    print("\n\n========== SUMMARY ==========")
    total = 0
    with_opener = 0
    barren = 0
    for cat, rows in all_results.items():
        cat_total = len(rows)
        cat_with = sum(1 for r in rows if r["has_opener"])
        cat_barren = sum(1 for r in rows if not r["has_opener"] and r["other_figure_count"] == 0)
        total += cat_total
        with_opener += cat_with
        barren += cat_barren
        print(f"  {cat:15s}  {cat_with:3d}/{cat_total:3d} have opener  ({cat_barren} barren no-opener)")
    print(f"  {'TOTAL':15s}  {with_opener:3d}/{total:3d} have opener  ({barren} barren no-opener)")

    # Priority list: pages without opener, sorted: barren first, then by part order.
    print("\n\n========== PRIORITY: pages most needing a hero image ==========")
    priority: list[tuple[int, dict, str]] = []
    for cat in ("part", "chapter", "appendix", "front-matter"):
        for r in all_results.get(cat, []):
            if r["has_opener"]:
                continue
            # Lower score = higher priority.
            # Barren (0 other figs) gets +0; some figs gets +10.
            # Part landings get -5 boost (they introduce a Part).
            # Chapter landings get -3 boost.
            score = r["other_figure_count"] * 5
            if cat == "part":
                score -= 5
            elif cat == "chapter":
                score -= 3
            priority.append((score, r, cat))
    priority.sort(key=lambda t: (t[0], relpath(t[1]["path"])))

    for i, (score, r, cat) in enumerate(priority[:10], 1):
        rp = relpath(r["path"])
        flag = "BARREN" if r["other_figure_count"] == 0 else f"{r['other_figure_count']} other figs"
        print(f"  {i:2d}. [{cat:5s}] {rp}  ({flag})")

    print(f"\n(Total no-opener pages: {len(priority)})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
