"""Audit Part XII (LLM Applications Across Industries) for content richness.

Walks every index.html under part-12-llm-applications-across-industries/ and
scores each chapter on the dimensions the author cares about for a rich,
book-quality application chapter:

  - External hyperlinks (off-book URLs, real products/companies)
  - Callout boxes by type (big-picture, warning, tip, key-insight,
    practical-example, production-pattern, postmortem, etc.)
  - Tables (architecture, comparison, pricing, etc.)
  - Figures (img / figure elements with alt text)
  - Bibliography / "Where to Read More" entries
  - Presence of a "Use Cases That Actually Work" or similar section
  - Word count (rough proxy for depth)

The audit is READ-ONLY. Findings are printed to stdout.

Run from project root:
    /c/Python314/python scripts/_audit_part12_richness.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
PART_DIR = ROOT / "part-12-llm-applications-across-industries"


def classify_link(href: str) -> str:
    """Return 'external', 'internal', or 'anchor' for an href."""
    if not href:
        return "anchor"
    href = href.strip()
    if href.startswith("#"):
        return "anchor"
    parsed = urlparse(href)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return "external"
    return "internal"


def callout_type(div) -> str:
    """Extract the callout subtype from a div.callout's class list."""
    classes = [c for c in div.get("class", []) if c != "callout"]
    return classes[0] if classes else "unspecified"


def has_use_case_section(soup: BeautifulSoup) -> bool:
    text = soup.get_text(" ", strip=True).lower()
    keys = [
        "use cases that actually work",
        "use cases that actually ship",
        "production examples",
        "what works",
        "use cases",
    ]
    return any(k in text for k in keys)


def has_bibliography(soup: BeautifulSoup) -> tuple[bool, int]:
    """Look for a 'Where to Read More' / 'Further Reading' / 'References' section
    and count the <li>/<a> entries under it.
    """
    text = soup.get_text("\n", strip=False).lower()
    headers = ["where to read more", "further reading", "references",
               "bibliography", "sources"]
    for h in headers:
        if h in text:
            # Heuristic: count anchors inside the last <ul> after that header.
            for ul in soup.find_all("ul"):
                preceding = ul.find_previous(string=re.compile(h, re.I))
                if preceding is not None:
                    entries = len(ul.find_all("li"))
                    return True, entries
    return False, 0


def audit_chapter(path: Path) -> dict:
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup

    # Links
    anchors = main.find_all("a", href=True)
    link_kinds = Counter(classify_link(a["href"]) for a in anchors)
    external_anchors = [a for a in anchors if classify_link(a["href"]) == "external"]

    # Callouts
    callouts = main.find_all("div", class_="callout")
    callout_counter = Counter(callout_type(c) for c in callouts)

    # Tables
    tables = main.find_all("table")

    # Figures (img or figure)
    figures = main.find_all(["figure", "img"])
    figures_with_alt = [
        f for f in figures
        if (f.name == "img" and f.get("alt"))
        or (f.name == "figure" and f.find("img") and f.find("img").get("alt"))
    ]

    # Bibliography
    has_bib, bib_entries = has_bibliography(soup)

    # Use Cases section presence
    has_uc = has_use_case_section(soup)

    # Word count (rough)
    text = main.get_text(" ", strip=True)
    words = len(re.findall(r"\b\w+\b", text))

    return {
        "path": path,
        "external_links": link_kinds.get("external", 0),
        "internal_links": link_kinds.get("internal", 0),
        "external_anchor_texts": [a.get_text(" ", strip=True)[:60]
                                   for a in external_anchors][:8],
        "callouts_total": len(callouts),
        "callouts_by_type": dict(callout_counter),
        "tables": len(tables),
        "figures": len(figures),
        "figures_with_alt": len(figures_with_alt),
        "has_bibliography": has_bib,
        "bibliography_entries": bib_entries,
        "has_use_case_section": has_uc,
        "word_count": words,
    }


def overall_rating(c: dict) -> str:
    score = 0
    if c["external_links"] >= 6:
        score += 2
    elif c["external_links"] >= 2:
        score += 1
    if c["callouts_total"] >= 6:
        score += 2
    elif c["callouts_total"] >= 4:
        score += 1
    if len(c["callouts_by_type"]) >= 3:
        score += 1
    if c["tables"] >= 1:
        score += 1
    if c["figures"] >= 1:
        score += 1
    if c["bibliography_entries"] >= 5:
        score += 1
    if c["word_count"] >= 2500:
        score += 1
    if score >= 6:
        return "rich"
    if score >= 3:
        return "medium"
    return "sparse"


def main() -> None:
    chapter_paths = sorted(PART_DIR.glob("module-*/index.html"))
    part_index = PART_DIR / "index.html"

    print(f"Auditing Part XII at {PART_DIR}")
    print(f"Found {len(chapter_paths)} chapter(s) plus part index")
    print()

    # Header
    header = (
        "| Chapter | ext links | callouts (by type) | tables | figures "
        "| bib entries | words | rating |"
    )
    sep = "|" + "|".join("---" for _ in range(8)) + "|"
    print(header)
    print(sep)

    rows = []
    for p in [part_index] + chapter_paths:
        c = audit_chapter(p)
        rating = overall_rating(c)
        rows.append((p, c, rating))
        name = p.parent.name if p.name == "index.html" and p.parent != PART_DIR \
            else "(part index)"
        callout_summary = ", ".join(f"{k}:{v}" for k, v in
                                    sorted(c["callouts_by_type"].items())) or "-"
        print(f"| {name} | {c['external_links']} | {callout_summary} "
              f"| {c['tables']} | {c['figures']} "
              f"| {c['bibliography_entries']} | {c['word_count']} | {rating} |")

    print()
    print("== External link details ==")
    for p, c, _ in rows:
        if c["external_links"]:
            print(f"  {p.parent.name}: {c['external_anchor_texts']}")
        else:
            print(f"  {p.parent.name}: NONE")

    print()
    print("== Use-case section presence ==")
    for p, c, _ in rows:
        print(f"  {p.parent.name}: {'yes' if c['has_use_case_section'] else 'NO'}")


if __name__ == "__main__":
    main()
