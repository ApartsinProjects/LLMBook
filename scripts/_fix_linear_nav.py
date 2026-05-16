"""Enforce a single linear reading order for bottom-nav prev/next.

Replaces the prior 'sibling-only' nav convention (chapter index next =
next chapter index, which skips the chapter's own sections) with a
linear thread that walks every page in reading order. Clicking 'next'
from any page should take the reader to the next page in book order.

Order (built from book_structure.yaml + filesystem):
  index.html (cover)
  toc.html
  front-matter/foreword.html
  front-matter/look-inside-preview.html
  front-matter/fm-what-this-book-covers.html
  front-matter/fm-who-should-read.html
  front-matter/fm-how-to-use.html
  front-matter/about-authors.html
  front-matter/copyright.html
  part-1-foundations/index.html
    part-1-foundations/module-00-.../index.html
      part-1-foundations/module-00-.../section-0.1.html
      part-1-foundations/module-00-.../section-0.2.html
      ...
    part-1-foundations/module-01-.../index.html
      ...
  part-2-.../index.html
    ...
  ...
  part-12-.../module-65-.../section-65.5.html  (LAST chapter content)
  appendices/index.html
  appendices/appendix-a-.../index.html
    appendices/appendix-a-.../section-a.1.html
    ...
  appendices/appendix-u-.../section-u.last.html
  (loop back to toc.html)

'up' semantics unchanged:
  section page -> chapter index
  chapter index -> part index
  part index -> toc.html
  appendix section -> appendix index
  appendix index -> appendices/index.html
  appendices/index.html -> toc.html
  front-matter page -> toc.html
  toc.html -> index.html (cover)

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}

PART_ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
              7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}


def _resolve(p: Path) -> str:
    """Path relative to ROOT, forward slashes."""
    return str(p.relative_to(ROOT)).replace("\\", "/")


def build_reading_order() -> list[dict]:
    """Return a list of page dicts in linear reading order.

    Each dict has: path (Path), label_num (str for nav-num),
    label_title (str for nav-title), parent_path (Path or None for up).
    """
    yaml_path = ROOT / "book_structure.yaml"
    struct = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    order: list[dict] = []

    # 1. Cover
    cover = ROOT / "index.html"
    if cover.exists():
        order.append({"path": cover, "label_num": "Book",
                      "label_title": "Cover", "parent": None})

    # 2. TOC
    toc = ROOT / "toc.html"
    if toc.exists():
        order.append({"path": toc, "label_num": "Book Index",
                      "label_title": "Table of Contents", "parent": cover})

    # 3. Front matter (in yaml-declared order)
    for fm in struct.get("front_matter", []):
        slug = fm["slug"]
        p = ROOT / "front-matter" / f"{slug}.html"
        if p.exists():
            order.append({
                "path": p,
                "label_num": "Front Matter",
                "label_title": fm.get("title", slug),
                "parent": toc,
            })

    # 4. Parts -> chapters -> sections
    for part in struct.get("parts", []):
        pnum = part["num"]
        pslug = part["slug"]
        roman = PART_ROMAN.get(pnum, str(pnum))
        part_idx = ROOT / f"part-{pnum}-{pslug}" / "index.html"
        if part_idx.exists():
            order.append({
                "path": part_idx,
                "label_num": f"Part {roman}",
                "label_title": part.get("title", f"Part {roman}"),
                "parent": toc,
            })
        for chap in part.get("chapters", []):
            cnum = chap["num"]
            cslug = chap["slug"]
            chap_idx = (ROOT / f"part-{pnum}-{pslug}"
                         / f"module-{cnum:02d}-{cslug}" / "index.html")
            if chap_idx.exists():
                order.append({
                    "path": chap_idx,
                    "label_num": f"Chapter {cnum}",
                    "label_title": chap.get("title", f"Chapter {cnum}"),
                    "parent": part_idx,
                })
            # Sections (use filesystem order, since some chapters have
            # sections outside the yaml manifest)
            chap_dir = chap_idx.parent
            if chap_dir.exists():
                # Match section-N.M.html where N is chapter number
                sec_files = sorted(
                    chap_dir.glob(f"section-{cnum}.*.html"),
                    key=lambda p: (
                        [int(x) for x in re.findall(r"\d+", p.stem)]
                    ),
                )
                # Read each file's h1 for nav-title
                for sf in sec_files:
                    m = re.search(r"section-(\d+)\.(\d+)\.html$", sf.name)
                    if not m:
                        continue
                    snum = f"{m.group(1)}.{m.group(2)}"
                    h1 = _read_h1(sf) or f"Section {snum}"
                    order.append({
                        "path": sf,
                        "label_num": f"Section {snum}",
                        "label_title": h1,
                        "parent": chap_idx,
                    })

    # 5. Appendices index
    appx_idx = ROOT / "appendices" / "index.html"
    if appx_idx.exists():
        order.append({
            "path": appx_idx,
            "label_num": "Appendices",
            "label_title": "Reference, Frameworks, Infrastructure & Pedagogy",
            "parent": toc,
        })

    # 6. Each appendix index + sections
    for app in struct.get("appendices", []):
        letter = app["letter"]
        slug = app["slug"]
        app_idx = (ROOT / "appendices"
                    / f"appendix-{letter.lower()}-{slug}" / "index.html")
        if app_idx.exists():
            order.append({
                "path": app_idx,
                "label_num": f"Appendix {letter}",
                "label_title": app.get("title", f"Appendix {letter}"),
                "parent": appx_idx,
            })
        app_dir = app_idx.parent
        if app_dir.exists():
            sec_files = sorted(
                app_dir.glob(f"section-{letter.lower()}.*.html"),
                key=lambda p: (
                    [int(x) for x in re.findall(r"\d+", p.stem)]
                ),
            )
            for sf in sec_files:
                m = re.search(r"section-([a-z])\.(\d+)\.html$", sf.name)
                if not m:
                    continue
                snum = f"{letter}.{m.group(2)}"
                h1 = _read_h1(sf) or f"Section {snum}"
                order.append({
                    "path": sf,
                    "label_num": f"Section {snum}",
                    "label_title": h1,
                    "parent": app_idx,
                })

    return order


def _read_h1(p: Path) -> str | None:
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", text)
    return m.group(1).strip() if m else None


def _href_from(src: Path, dst: Path) -> str:
    """Compute the relative href from src page to dst page."""
    try:
        return str(dst.relative_to(src.parent)).replace("\\", "/")
    except ValueError:
        # Walk up
        src_parts = src.parent.parts
        dst_parts = dst.parts
        # Find common prefix
        i = 0
        while (i < len(src_parts) and i < len(dst_parts)
                and src_parts[i] == dst_parts[i]):
            i += 1
        ups = len(src_parts) - i
        rel = ("../" * ups) + "/".join(dst_parts[i:])
        return rel


def build_nav_block(prev_page: dict | None, parent_page: dict | None,
                      next_page: dict | None, self_path: Path) -> str:
    """Build the chapter-nav HTML block with correct hrefs + labels."""
    parts = []
    parts.append('<nav class="chapter-nav">')
    if prev_page:
        href = _href_from(self_path, prev_page["path"])
        parts.append(
            f'<a class="prev" href="{href}">'
            f'<span class="nav-label">Previous</span>'
            f'<span class="nav-num">{_esc(prev_page["label_num"])}</span>'
            f'<span class="nav-title">{_esc(prev_page["label_title"])}</span></a>'
        )
    if parent_page:
        href = _href_from(self_path, parent_page["path"])
        up_label = _up_label_for(parent_page)
        parts.append(
            f'<a class="up" href="{href}">'
            f'<span class="nav-label">{up_label}</span>'
            f'<span class="nav-num">{_esc(parent_page["label_num"])}</span>'
            f'<span class="nav-title">{_esc(parent_page["label_title"])}</span></a>'
        )
    if next_page:
        href = _href_from(self_path, next_page["path"])
        parts.append(
            f'<a class="next" href="{href}">'
            f'<span class="nav-label">Next</span>'
            f'<span class="nav-num">{_esc(next_page["label_num"])}</span>'
            f'<span class="nav-title">{_esc(next_page["label_title"])}</span></a>'
        )
    parts.append('</nav>')
    return "\n".join(parts)


def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _up_label_for(parent: dict) -> str:
    n = parent["label_num"]
    if n.startswith("Chapter"):
        return "In Chapter"
    if n.startswith("Part"):
        return "In Part"
    if n.startswith("Appendix"):
        return "In Appendix"
    if n == "Appendices":
        return "Appendices"
    if n == "Book Index":
        return "Up"
    return "Up"


def fix_nav_in_file(p: Path, prev_page, parent_page, next_page,
                     dry_run: bool) -> bool:
    text = p.read_text(encoding="utf-8")
    # Find existing chapter-nav block; replace with the new one
    new_nav = build_nav_block(prev_page, parent_page, next_page, p)
    new_text, n = re.subn(
        r'<nav class="chapter-nav">[\s\S]*?</nav>',
        new_nav.replace("\\", "\\\\"),  # safe regex backslash escape
        text,
        count=1,
    )
    if n == 0:
        # No existing nav block; insert before <footer> if any, else before </main>
        if "<footer" in text:
            new_text = re.sub(
                r'(<footer)',
                new_nav + "\n\\1",
                text,
                count=1,
            )
        elif "</main>" in text:
            new_text = text.replace("</main>", new_nav + "\n</main>", 1)
        else:
            return False
    if new_text == text:
        return False
    if not dry_run:
        p.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    order = build_reading_order()
    print(f"Reading order: {len(order)} pages")

    # For loop-back: last appendix section -> toc.html
    toc = ROOT / "toc.html"

    n_edited = 0
    for i, page in enumerate(order):
        # Cover and TOC do not need a chapter-nav block; skip them.
        # (They typically don't have one anyway.)
        rel = _resolve(page["path"])
        if rel in {"index.html", "toc.html"}:
            continue
        prev_page = order[i - 1] if i > 0 else None
        next_page = order[i + 1] if i + 1 < len(order) else {
            "path": toc,
            "label_num": "Book Index",
            "label_title": "Table of Contents",
        }
        parent_page = None
        if page.get("parent"):
            for q in order:
                if q["path"] == page["parent"]:
                    parent_page = q
                    break
        changed = fix_nav_in_file(page["path"], prev_page, parent_page,
                                    next_page, dry_run)
        if changed:
            n_edited += 1

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Pages in order: {len(order)}")
    print(f"Files edited:   {n_edited}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
