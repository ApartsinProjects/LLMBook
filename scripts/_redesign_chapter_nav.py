"""Rebuild every <nav class="chapter-nav"> in the book with a richer,
standardized structure:

    <nav class="chapter-nav">
      <a class="prev" href="...">
        <span class="nav-label">Previous</span>
        <span class="nav-num">Section 31.0</span>
        <span class="nav-title">Page title</span>
      </a>
      <a class="up" href="...">
        <span class="nav-label">In Chapter</span>
        <span class="nav-num">Chapter 31</span>
        <span class="nav-title">LLM Strategy ...</span>
      </a>
      <a class="next" href="...">
        <span class="nav-label">Next</span>
        <span class="nav-num">Section 31.2</span>
        <span class="nav-title">LLM Product Management</span>
      </a>
    </nav>

This script:
1. Derives the destination's "number" (Section X.Y / Chapter N / Part X /
   Appendix X / Appendix X.Y / Book Index / Front Matter etc.) from the HREF.
2. Reads the destination's <h1> for the title.
3. Strips inline arrow glyphs from existing anchor text.
4. Picks an appropriate "label" per anchor class:
     prev  -> "Previous"
     up    -> "In Chapter" (section), "In Part" (chapter), "Book" (part),
              "In Appendix" (appendix section)
     next  -> "Next"
5. Replaces the anchor inner HTML with the three spans.

Idempotent: if anchor already has the new structure, leave alone.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
         8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}

_h1_cache: dict[Path, str] = {}


def get_h1(p: Path) -> str:
    if p in _h1_cache:
        return _h1_cache[p]
    if not p.exists():
        _h1_cache[p] = ""
        return ""
    text = p.read_text(encoding="utf-8")
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", text)
    title = m.group(1).strip() if m else ""
    # Decode HTML entities
    import html as html_mod
    title = html_mod.unescape(title)
    # Strip any leading "Chapter X:", "Part X:", "Section X.Y:", "Appendix X:"
    title = re.sub(r"^(Chapter|Part|Section|Appendix)\s+\S+\s*:?\s*", "", title)
    _h1_cache[p] = title
    return title


def derive_destination(href: str, src_dir: Path) -> tuple[str, str, str]:
    """Given an href + the directory of the source page, return
    (kind, number_label, title). 'kind' is one of:
        section, chapter, part, appendix_section, appendix_landing,
        front_matter, book_index, unknown."""
    if not href:
        return "unknown", "", ""

    # Strip fragment + query
    href_clean = href.split("#")[0].split("?")[0]
    target = (src_dir / href_clean).resolve()

    # Top of book
    if target.name == "toc.html":
        return "book_index", "Book Index", get_h1(target) or "Table of Contents"
    if target.name == "index.html" and target.parent == ROOT:
        return "book_index", "Book", get_h1(target) or "Cover"

    parts = target.relative_to(ROOT).parts if target.is_relative_to(ROOT) else target.parts

    # Section in main book: part-N/module-MM/section-X.Y.html
    if (len(parts) == 3 and parts[0].startswith("part-")
            and parts[1].startswith("module-") and re.match(r"section-[\d.]+\.html", parts[2])):
        m = re.match(r"section-([\d.]+)\.html", parts[2])
        if m:
            return "section", f"Section {m.group(1)}", get_h1(target)

    # Chapter landing: part-N/module-MM/index.html
    if (len(parts) == 3 and parts[0].startswith("part-")
            and parts[1].startswith("module-") and parts[2] == "index.html"):
        m = re.match(r"module-(\d+)-", parts[1])
        if m:
            return "chapter", f"Chapter {int(m.group(1))}", get_h1(target)

    # Part landing: part-N/index.html
    if (len(parts) == 2 and parts[0].startswith("part-") and parts[1] == "index.html"):
        m = re.match(r"part-(\d+)-", parts[0])
        if m:
            roman = ROMAN.get(int(m.group(1)), m.group(1))
            return "part", f"Part {roman}", get_h1(target)

    # Appendix section: appendices/appendix-X-slug/section-X.N.html
    if (len(parts) == 3 and parts[0] == "appendices"
            and parts[1].startswith("appendix-")
            and re.match(r"section-[a-z]?[\d.]+\.html", parts[2])):
        m = re.match(r"section-([a-z]?[\d.]+)\.html", parts[2])
        if m:
            num = m.group(1).upper()
            return "appendix_section", f"Section {num}", get_h1(target)

    # Appendix landing: appendices/appendix-X-slug/index.html
    if (len(parts) == 3 and parts[0] == "appendices"
            and parts[1].startswith("appendix-") and parts[2] == "index.html"):
        m = re.match(r"appendix-([a-z])-", parts[1])
        if m:
            return "appendix_landing", f"Appendix {m.group(1).upper()}", get_h1(target)

    # Appendices index
    if (len(parts) == 2 and parts[0] == "appendices" and parts[1] == "index.html"):
        return "appendix_landing", "Appendices", "Appendices"

    # Glossary
    if "glossary" in parts:
        return "appendix_landing", "Glossary", "Glossary"

    # Front matter
    if parts[0] == "front-matter":
        return "front_matter", "Front Matter", get_h1(target)

    return "unknown", "", ""


def label_for(anchor_class: str, src_kind: str, dest_kind: str) -> str:
    """Pick the label text for this anchor."""
    if "prev" in anchor_class:
        return "Previous"
    if "next" in anchor_class:
        return "Next"
    if "up" in anchor_class:
        # The 'up' label depends on where we ARE, not where we're going.
        if src_kind == "section":
            return "In Chapter"
        if src_kind == "appendix_section":
            return "In Appendix"
        if src_kind == "chapter":
            return "In Part"
        if src_kind == "appendix_landing":
            return "Appendices"
        if src_kind == "part":
            return "Up"
        return "Up"
    return ""


def classify_source(p: Path) -> str:
    """Return the same kind taxonomy for the source page."""
    parts = p.relative_to(ROOT).parts
    name = p.name
    if parts[0].startswith("part-") and len(parts) == 2 and name == "index.html":
        return "part"
    if (len(parts) == 3 and parts[0].startswith("part-")
            and parts[1].startswith("module-") and name == "index.html"):
        return "chapter"
    if (len(parts) == 3 and parts[0].startswith("part-")
            and parts[1].startswith("module-") and re.match(r"section-[\d.]+\.html", name)):
        return "section"
    if (len(parts) == 3 and parts[0] == "appendices"
            and parts[1].startswith("appendix-") and name == "index.html"):
        return "appendix_landing"
    if (len(parts) == 3 and parts[0] == "appendices"
            and parts[1].startswith("appendix-")
            and re.match(r"section-[a-z]?[\d.]+\.html", name)):
        return "appendix_section"
    if parts[0] == "front-matter":
        return "front_matter"
    return "unknown"


def rebuild_nav(p: Path, dry_run: bool) -> int:
    text = p.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    nav = soup.find("nav", class_="chapter-nav")
    if nav is None:
        return 0

    src_kind = classify_source(p)
    src_dir = p.parent

    anchors = nav.find_all("a")
    if not anchors:
        return 0

    changed = 0
    for a in anchors:
        # Already converted? skip (has nav-num span)
        if a.find("span", class_="nav-num") is not None:
            continue
        href = a.get("href", "")
        anchor_classes = a.get("class") or []
        # Determine class for label decision: explicit prev/up/next or positional
        anchor_class = " ".join(anchor_classes)
        if not any(c in anchor_class for c in ("prev", "up", "next")):
            # Use positional fallback
            idx = list(nav.find_all("a")).index(a)
            if idx == 0:
                anchor_class = "prev"
            elif idx == len(anchors) - 1:
                anchor_class = "next"
            else:
                anchor_class = "up"

        dest_kind, num, title = derive_destination(href, src_dir)
        label = label_for(anchor_class, src_kind, dest_kind)

        # Existing text fallback (strip arrows + leading whitespace)
        existing_text = a.get_text(" ", strip=True)
        existing_text = re.sub(r"^[←→↑↓]+\s*", "", existing_text)
        existing_text = re.sub(r"\s*[←→↑↓]+$", "", existing_text)
        # Strip "(Chapter N: )" or "(Section N.M: )" prefix if duplicated by derived num
        if num and existing_text.lower().startswith(num.lower()):
            existing_text = existing_text[len(num):].lstrip(": ").strip()

        # If we couldn't derive a title, use existing_text
        if not title:
            title = existing_text
        # If number not derivable, the existing text might already have it
        if not num and existing_text:
            m = re.match(r"^(Section\s+[\d.]+|Chapter\s+\d+|Part\s+[IVXLCDM]+|Appendix\s+[A-Z]+(?:\.[\d.]+)?)\s*:?\s*(.*)$", existing_text)
            if m:
                num = m.group(1)
                title = m.group(2) if m.group(2) else title

        # Clear existing children and add new spans
        a.clear()
        if label:
            sp_label = soup.new_tag("span")
            sp_label["class"] = ["nav-label"]
            sp_label.append(NavigableString(label))
            a.append(sp_label)
        if num:
            sp_num = soup.new_tag("span")
            sp_num["class"] = ["nav-num"]
            sp_num.append(NavigableString(num))
            a.append(sp_num)
        if title and title.lower() != num.lower():
            sp_title = soup.new_tag("span")
            sp_title["class"] = ["nav-title"]
            sp_title.append(NavigableString(title))
            a.append(sp_title)

        changed += 1

    if not changed:
        return 0
    new = str(soup)
    if not dry_run:
        p.write_text(new, encoding="utf-8")
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    files = 0
    anchors = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n = rebuild_nav(p, args.dry_run)
        if n:
            files += 1
            anchors += n
    print(f"TOTAL: {anchors} chapter-nav anchors restructured across {files} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
