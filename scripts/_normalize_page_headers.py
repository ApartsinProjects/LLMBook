"""Normalize page headers across the book so every page shows a clear
breadcrumb of (Part > Chapter > Section) plus a numbered h1.

Target structure per page type:

PART LANDING (e.g. part-1-foundations/index.html)
    <header class="chapter-header">
      <nav class="header-nav">...</nav>
      <div class="header-search">...</div>
      <div class="part-label">Part I</div>
      <h1 class="part-title">Part I: Foundations</h1>
      <p class="chapter-subtitle">...</p>
    </header>

CHAPTER LANDING (e.g. module-00-..../index.html)
    <header class="chapter-header">
      <nav>...</nav>
      <div class="header-search">...</div>
      <div class="part-label"><a href="../index.html">Part I: Foundations</a></div>
      <div class="chapter-label">Chapter 0</div>
      <h1>Chapter 0: ML and PyTorch Foundations</h1>
    </header>

SECTION (e.g. section-0.1.html)
    <header class="chapter-header">
      <nav>...</nav>
      <div class="header-search">...</div>
      <div class="part-label"><a href="../../part-X/index.html">Part I: Foundations</a></div>
      <div class="chapter-label"><a href="index.html">Chapter 0: ML and PyTorch Foundations</a></div>
      <div class="section-label">Section 0.1</div>
      <h1>Section 0.1: What Every LLM Engineer Needs From Classical ML</h1>
    </header>

APPENDIX LANDING / SECTION: same shape but uses "Appendices" and "Appendix A" etc.

Conservative apply: only modifies what's clearly wrong. Preserves existing
section subtitles and any extra rows the page already has.

Idempotent.
"""
from __future__ import annotations
import argparse
import html
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}


def should_skip(p: Path) -> bool:
    return bool(set(p.parts) & SKIP_PARTS)


# ----------------------------------------------------------------------
# Classify each page by path
# ----------------------------------------------------------------------

def classify(p: Path) -> dict | None:
    """Return descriptor: {kind, part_num, part_title, chapter_num, chapter_title, section_num, section_title}."""
    parts = p.relative_to(ROOT).parts
    name = p.name
    # Part landing: parts[0] == part-N-NAME, name == index.html, no module
    if (parts[0].startswith("part-") and len(parts) == 2 and name == "index.html"):
        m = re.match(r"part-(\d+)-(.+)", parts[0])
        if m:
            return {"kind": "part_landing", "part_num": int(m.group(1)),
                    "part_slug": m.group(2)}
    # Chapter landing: part-N/module-MM-NAME/index.html
    if (len(parts) == 3 and parts[0].startswith("part-")
            and parts[1].startswith("module-") and name == "index.html"):
        m1 = re.match(r"part-(\d+)-(.+)", parts[0])
        m2 = re.match(r"module-(\d+)-(.+)", parts[1])
        if m1 and m2:
            return {"kind": "chapter_landing",
                    "part_num": int(m1.group(1)), "part_slug": m1.group(2),
                    "chapter_num": int(m2.group(1)), "chapter_slug": m2.group(2)}
    # Section: part-N/module-MM-NAME/section-X.Y.html
    if (len(parts) == 3 and parts[0].startswith("part-")
            and parts[1].startswith("module-") and re.match(r"section-[\d.]+\.html", name)):
        m1 = re.match(r"part-(\d+)-(.+)", parts[0])
        m2 = re.match(r"module-(\d+)-(.+)", parts[1])
        m3 = re.match(r"section-([\d.]+)\.html", name)
        if m1 and m2 and m3:
            return {"kind": "section",
                    "part_num": int(m1.group(1)), "part_slug": m1.group(2),
                    "chapter_num": int(m2.group(1)), "chapter_slug": m2.group(2),
                    "section_num": m3.group(1)}
    # Appendix landing: appendices/appendix-X-NAME/index.html
    if (len(parts) == 3 and parts[0] == "appendices"
            and parts[1].startswith("appendix-") and name == "index.html"):
        m = re.match(r"appendix-([a-z])-(.+)", parts[1])
        if m:
            return {"kind": "appendix_landing",
                    "appendix_letter": m.group(1).upper(),
                    "appendix_slug": m.group(2)}
    # Appendix section: appendices/appendix-X-NAME/section-X.Y.html
    if (len(parts) == 3 and parts[0] == "appendices"
            and parts[1].startswith("appendix-") and re.match(r"section-[a-z\d.]+\.html", name)):
        m1 = re.match(r"appendix-([a-z])-(.+)", parts[1])
        m2 = re.match(r"section-([a-z]?[\d.]+)\.html", name)
        if m1 and m2:
            return {"kind": "appendix_section",
                    "appendix_letter": m1.group(1).upper(),
                    "appendix_slug": m1.group(2),
                    "section_num": m2.group(1).upper()}
    return None


ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
         8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}


# Cache: part_num -> Part title (read from toc.html or the part landing once)
_part_title_cache: dict[int, str] = {}
_chapter_title_cache: dict[tuple[int, int], str] = {}
_appendix_title_cache: dict[str, str] = {}


def part_title(part_num: int) -> str:
    if part_num in _part_title_cache:
        return _part_title_cache[part_num]
    # Read the part landing
    for d in ROOT.glob(f"part-{part_num}-*"):
        idx = d / "index.html"
        if idx.exists():
            t = idx.read_text(encoding="utf-8")
            m = re.search(r'<h1[^>]*class="part-title"[^>]*>([^<]+)</h1>', t)
            if m:
                title = html.unescape(m.group(1).strip())
                # Strip "Part X: " prefix if present
                title = re.sub(r"^Part [IVXLCDM]+:\s*", "", title)
                _part_title_cache[part_num] = title
                return title
    return ""


def chapter_title(part_num: int, chapter_num: int) -> str:
    key = (part_num, chapter_num)
    if key in _chapter_title_cache:
        return _chapter_title_cache[key]
    chap_dirs = list(ROOT.glob(f"part-{part_num}-*/module-{chapter_num:02d}-*"))
    if not chap_dirs:
        return ""
    idx = chap_dirs[0] / "index.html"
    if not idx.exists():
        return ""
    t = idx.read_text(encoding="utf-8")
    # The chapter landing h1 is the chapter title; strip "Chapter N: " if there
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', t)
    if m:
        title = html.unescape(m.group(1).strip())
        title = re.sub(r"^Chapter \d+:\s*", "", title)
        _chapter_title_cache[key] = title
        return title
    return ""


def appendix_title(letter: str) -> str:
    if letter in _appendix_title_cache:
        return _appendix_title_cache[letter]
    # Use letter -> slug-prefix mapping by scanning appendices/
    for d in (ROOT / "appendices").glob(f"appendix-{letter.lower()}-*"):
        idx = d / "index.html"
        if idx.exists():
            t = idx.read_text(encoding="utf-8")
            m = re.search(r'<h1[^>]*>([^<]+)</h1>', t)
            if m:
                title = html.unescape(m.group(1).strip())
                title = re.sub(r"^Appendix [A-Z]+:\s*", "", title)
                _appendix_title_cache[letter] = title
                return title
    return ""


# ----------------------------------------------------------------------
# Header normalization
# ----------------------------------------------------------------------

def _make_breadcrumb(soup, *items) -> "BeautifulSoup":
    """Build <div class="page-breadcrumb">[a > a > a]</div>.
    Each item is (text, href) where href=None means plain text (current page)."""
    bc = soup.new_tag("div")
    bc["class"] = ["page-breadcrumb"]
    for i, (text, href) in enumerate(items):
        if i > 0:
            sep = soup.new_tag("span")
            sep["class"] = ["bc-sep"]
            sep.append(NavigableString("›"))  # single right-pointing angle quote ›
            bc.append(sep)
        if href:
            a = soup.new_tag("a", href=href)
            a.append(NavigableString(text))
            bc.append(a)
        else:
            sp = soup.new_tag("span")
            sp["class"] = ["bc-current"]
            sp.append(NavigableString(text))
            bc.append(sp)
    return bc


def _make_below_label(soup, text: str) -> "BeautifulSoup":
    """Build <div class="page-current">…</div> — current-location caption that
    sits below the h1 (e.g. "Section 31.1" or "Chapter 31")."""
    d = soup.new_tag("div")
    d["class"] = ["page-current"]
    d.append(NavigableString(text))
    return d


def normalize_header(p: Path, desc: dict, dry_run: bool) -> bool:
    """Rebuild breadcrumb above h1 + current-location caption below h1.
    Layout per kind:

      part_landing:      [Part X]              (just .part-label above h1)
      chapter_landing:   [Part X] > Chapter Y  → h1 → Chapter Y caption below
      section:           [Part X] > [Chapter Y] → h1 → Section X.Y caption below
      appendix_landing:  [Appendices] > Appendix A → h1 → Appendix A caption below
      appendix_section:  [Appendices] > [Appendix A] → h1 → Section A.N caption below
    """
    text = p.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    header = soup.find("header")
    if header is None:
        return False

    kind = desc["kind"]
    above: list = []  # rows above h1 (in order)
    below: list = []  # rows below h1

    if kind == "part_landing":
        roman = ROMAN.get(desc["part_num"], str(desc["part_num"]))
        d = soup.new_tag("div")
        d["class"] = ["part-label"]
        d["data-pagefind-meta"] = "part"
        d.append(NavigableString(f"Part {roman}"))
        above.append(d)
    elif kind == "chapter_landing":
        roman = ROMAN.get(desc["part_num"], str(desc["part_num"]))
        ptitle = part_title(desc["part_num"])
        # Chapter landing: breadcrumb shows current location, no below-caption
        # needed (h1 already names the chapter).
        bc = _make_breadcrumb(
            soup,
            (f"Part {roman}: {ptitle}", "../index.html"),
            (f"Chapter {desc['chapter_num']}", None),
        )
        bc["data-pagefind-meta"] = "chapter"
        above.append(bc)
    elif kind == "section":
        roman = ROMAN.get(desc["part_num"], str(desc["part_num"]))
        ptitle = part_title(desc["part_num"])
        ctitle = chapter_title(desc["part_num"], desc["chapter_num"])
        bc = _make_breadcrumb(
            soup,
            (f"Part {roman}: {ptitle}", "../index.html"),
            (f"Chapter {desc['chapter_num']}: {ctitle}", "index.html"),
        )
        bc["data-pagefind-meta"] = "chapter"
        above.append(bc)
        below.append(_make_below_label(soup, f"Section {desc['section_num']}"))
    elif kind == "appendix_landing":
        # Appendix landing: breadcrumb shows current location, no below-caption
        # (the h1 already names the appendix).
        bc = _make_breadcrumb(
            soup,
            ("Appendices", "../index.html"),
            (f"Appendix {desc['appendix_letter']}", None),
        )
        bc["data-pagefind-meta"] = "chapter"
        above.append(bc)
    elif kind == "appendix_section":
        atitle = appendix_title(desc["appendix_letter"].lower())
        bc = _make_breadcrumb(
            soup,
            ("Appendices", "../index.html"),
            (f"Appendix {desc['appendix_letter']}: {atitle}", "index.html"),
        )
        bc["data-pagefind-meta"] = "chapter"
        above.append(bc)
        below.append(_make_below_label(soup, f"Section {desc['section_num']}"))

    # Remove old-style breadcrumb rows + any prior page-breadcrumb / page-current
    for cls in ("part-label", "chapter-label", "section-label",
                "page-breadcrumb", "page-current"):
        for el in header.find_all("div", class_=cls):
            el.decompose()

    h1 = header.find("h1")
    if h1 is None:
        for r in above + below:
            header.append(r)
            header.append(NavigableString("\n"))
    else:
        for r in above:
            h1.insert_before(r)
            h1.insert_before(NavigableString("\n"))
        # below rows: insert AFTER any chapter-subtitle <p> that follows h1,
        # so the visual order is h1 → subtitle → page-current.
        anchor = h1
        # Walk past any chapter-subtitle paragraph immediately after h1
        nxt = h1.find_next_sibling()
        while nxt is not None and getattr(nxt, "name", None) == "p" and \
              "chapter-subtitle" in (nxt.get("class") or []):
            anchor = nxt
            nxt = nxt.find_next_sibling()
        for r in below:
            anchor.insert_after(r)
            anchor = r  # chain so subsequent rows append in order
            r.insert_after(NavigableString("\n"))

    new_text = str(soup)
    if new_text == text:
        return False
    if not dry_run:
        p.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    by_kind: dict[str, int] = {}
    files_changed = 0
    for p in ROOT.rglob("*.html"):
        if should_skip(p):
            continue
        desc = classify(p)
        if not desc:
            continue
        try:
            changed = normalize_header(p, desc, args.dry_run)
        except Exception as e:
            print(f"  ERR {p.relative_to(ROOT)}: {e}")
            continue
        if changed:
            files_changed += 1
            by_kind[desc["kind"]] = by_kind.get(desc["kind"], 0) + 1
    print()
    print(f"TOTAL: {files_changed} files normalized")
    for k, n in sorted(by_kind.items()):
        print(f"  {k}: {n}")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
