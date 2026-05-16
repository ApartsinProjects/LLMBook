"""Audit Overview-section presence on every part / chapter / appendix landing page.

READ-ONLY. Walks the LLMBook tree, identifies all landing `index.html` files
under part-*, part-N-*/module-NN-*/, and appendices/appendix-*/, and verifies
each one has overview-like introductory content.

Criteria (any one is sufficient):
  1. A heading (h1..h6) whose text contains "Overview" (case-insensitive)
  2. A heading "What This Part Covers" / "What You'll Learn"
  3. A `.callout` whose title is "Big Picture", "Looking Back", or "Looking Ahead"
  4. A `.chapter-intro`, `.part-intro`, `.part-overview`, or `.overview` div
  5. The first meaningful paragraph in <main> being long-ish introductory prose
     (>= 150 chars) and not just a section list or breadcrumb.

For pages with overview content, we measure its character length. Anything
< 150 chars after stripping nav/header/breadcrumb is flagged as "weak".

Template-breakage flags on landing pages:
  - Missing <h1> in header
  - More than one <h1>
  - Empty header element
  - h1 text that is a bare number, "TBD", "TODO", or placeholder pattern.

Skips: KDP/, .claude/, node_modules/, build/, temp_*, vendor/, pagefind/.

Usage:
    /c/Python314/python E:/Projects/BookBlogsHome/LLMBook/scripts/_audit_overview_presence.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    sys.stderr.write("BeautifulSoup4 is required. pip install beautifulsoup4\n")
    sys.exit(1)


ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

SKIP_DIRS = {"KDP", ".claude", "node_modules", "build", "vendor", "pagefind",
             "__pycache__", "images", "downloads"}

OVERVIEW_HEADING_PATTERNS = [
    re.compile(r"\boverview\b", re.IGNORECASE),
    re.compile(r"\bwhat\s+this\s+(part|chapter|appendix)\s+covers\b", re.IGNORECASE),
    re.compile(r"\bwhat\s+you[’']?ll\s+learn\b", re.IGNORECASE),
    re.compile(r"\bin\s+this\s+(part|chapter|appendix)\b", re.IGNORECASE),
]

CALLOUT_OVERVIEW_TITLES = {"big picture", "looking back", "looking ahead"}

INTRO_DIV_CLASSES = {"chapter-intro", "part-intro", "part-overview",
                     "overview", "chapter-overview", "appendix-overview"}

PLACEHOLDER_H1_PATTERNS = [
    re.compile(r"^\s*\d+\s*$"),
    re.compile(r"^\s*(TBD|TODO|FIXME|PLACEHOLDER|TITLE)\s*$", re.IGNORECASE),
    re.compile(r"^\s*(chapter|part|appendix)\s*\d*\s*$", re.IGNORECASE),
    re.compile(r"^\s*$"),
]

MIN_OVERVIEW_CHARS = 150


def is_skipped(p: Path) -> bool:
    parts = set(p.parts)
    for s in SKIP_DIRS:
        if s in parts:
            return True
    for part in p.parts:
        if part.startswith("temp_"):
            return True
    return False


def find_landing_pages():
    """Return list of (kind, label, path) for every landing index.html.

    kind in {"part", "chapter", "appendix", "appendix-root", "glossary"}.
    """
    pages = []

    # Part-level landings: part-N-*/index.html (only direct children of ROOT)
    for part_dir in sorted(ROOT.glob("part-*-*")):
        if not part_dir.is_dir() or is_skipped(part_dir):
            continue
        idx = part_dir / "index.html"
        if idx.exists():
            pages.append(("part", part_dir.name, idx))
        # Chapter landings inside the part
        for mod_dir in sorted(part_dir.glob("module-*")):
            if not mod_dir.is_dir() or is_skipped(mod_dir):
                continue
            midx = mod_dir / "index.html"
            if midx.exists():
                pages.append(("chapter", f"{part_dir.name}/{mod_dir.name}", midx))

    # Appendix landings
    app_root = ROOT / "appendices"
    if app_root.exists():
        # Appendix root index
        root_idx = app_root / "index.html"
        if root_idx.exists():
            pages.append(("appendix-root", "appendices", root_idx))
        for app_dir in sorted(app_root.glob("appendix-*")):
            if not app_dir.is_dir() or is_skipped(app_dir):
                continue
            aidx = app_dir / "index.html"
            if aidx.exists():
                pages.append(("appendix", f"appendices/{app_dir.name}", aidx))
        # Glossary
        gloss = app_root / "glossary"
        if gloss.exists():
            gidx = gloss / "index.html"
            if gidx.exists():
                pages.append(("appendix", "appendices/glossary", gidx))

    return pages


def parse(path: Path) -> Optional[BeautifulSoup]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [err] {path}: {e}", file=sys.stderr)
        return None
    return BeautifulSoup(text, "html.parser")


def text_of(tag: Optional[Tag]) -> str:
    if tag is None:
        return ""
    return tag.get_text(" ", strip=True)


def heading_is_overview(text: str) -> bool:
    if not text:
        return False
    for pat in OVERVIEW_HEADING_PATTERNS:
        if pat.search(text):
            return True
    return False


def find_overview(soup: BeautifulSoup) -> tuple[str, str, int]:
    """Return (source, snippet, char_count) of any overview-like content found.

    source in {"heading", "callout", "div", "first-para", "none"}.
    """
    main = soup.find("main") or soup.body
    if main is None:
        return ("none", "", 0)

    # 1. Heading match
    for h in main.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        txt = text_of(h)
        if heading_is_overview(txt):
            # Collect the prose that follows the heading (until next heading)
            prose_parts = []
            for sib in h.find_all_next():
                if sib.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                    break
                if sib.name == "p":
                    prose_parts.append(text_of(sib))
                if sum(len(x) for x in prose_parts) > 1500:
                    break
            prose = " ".join(prose_parts).strip()
            return ("heading", f"[h:{txt}] {prose[:200]}", len(prose))

    # 2. Intro div
    for klass in INTRO_DIV_CLASSES:
        d = main.find(class_=lambda c: c and klass in (c if isinstance(c, list) else c.split()))
        if d is not None:
            prose = text_of(d)
            # strip leading "Overview" / "Chapter Overview" from prose
            cleaned = re.sub(r"^(part|chapter|appendix)?\s*overview\s*", "",
                             prose, flags=re.IGNORECASE).strip()
            return ("div", f"[div.{klass}] {cleaned[:200]}", len(cleaned))

    # 3. Callout
    callouts = main.find_all(class_="callout")
    for c in callouts:
        title_el = c.find(class_="callout-title")
        title = text_of(title_el).lower()
        if title in CALLOUT_OVERVIEW_TITLES:
            body = ""
            for p in c.find_all("p"):
                body += text_of(p) + " "
            body = body.strip()
            return ("callout", f"[callout:{title}] {body[:200]}", len(body))

    # 4. First long paragraph in main
    for p in main.find_all("p"):
        # Skip paragraphs nested in figcaption / blockquote
        if p.find_parent(["figcaption", "blockquote", "header", "nav"]):
            continue
        # Skip subtitle
        if p.has_attr("class") and "chapter-subtitle" in p.get("class", []):
            continue
        txt = text_of(p)
        if len(txt) >= MIN_OVERVIEW_CHARS:
            return ("first-para", f"[p] {txt[:200]}", len(txt))
        elif len(txt) > 0:
            # Record short prose too in case nothing better is found
            return ("first-para-short", f"[p] {txt[:200]}", len(txt))

    return ("none", "", 0)


def check_template(soup: BeautifulSoup) -> list[str]:
    issues = []
    header = soup.find("header")
    if header is None:
        # The page may use <main> as header; fall back to first h1 in body
        h1s = soup.find_all("h1")
    else:
        # Empty header check
        if not header.get_text(strip=True):
            issues.append("empty <header>")
        h1s = soup.find_all("h1")

    if len(h1s) == 0:
        issues.append("no <h1> on page")
    elif len(h1s) > 1:
        issues.append(f"multiple <h1> ({len(h1s)})")

    if h1s:
        h1_text = text_of(h1s[0])
        for pat in PLACEHOLDER_H1_PATTERNS:
            if pat.match(h1_text):
                issues.append(f"placeholder h1: '{h1_text}'")
                break

    return issues


def main():
    pages = find_landing_pages()
    print(f"Found {len(pages)} landing pages to audit.\n")

    missing = []          # no overview at all
    weak = []             # overview but <150 chars
    unclear = []          # only first-para-short kind / ambiguous
    template_issues = []  # template breakage entries
    good = []             # passed cleanly

    by_part = defaultdict(list)  # part_label -> list of issue dicts

    for kind, label, path in pages:
        soup = parse(path)
        if soup is None:
            continue

        rel = path.relative_to(ROOT).as_posix()

        # Template
        tmpl = check_template(soup)
        if tmpl:
            template_issues.append((kind, label, rel, tmpl))

        # Overview
        source, snippet, n = find_overview(soup)

        # Determine bucket
        part_key = None
        if kind == "part":
            part_key = label
        elif kind == "chapter":
            part_key = label.split("/", 1)[0]
        elif kind in ("appendix", "appendix-root"):
            part_key = "appendices"

        entry = {
            "kind": kind, "label": label, "rel": rel,
            "source": source, "chars": n, "snippet": snippet,
            "template": tmpl,
        }

        if source == "none":
            missing.append(entry)
            by_part[part_key].append(("MISSING", entry))
        elif source == "first-para-short":
            unclear.append(entry)
            by_part[part_key].append(("UNCLEAR", entry))
        elif n < MIN_OVERVIEW_CHARS:
            weak.append(entry)
            by_part[part_key].append(("WEAK", entry))
        else:
            good.append(entry)

        if tmpl:
            by_part[part_key].append(("TEMPLATE", entry))

    # ---- Print report ----
    def head(t): print(f"\n{'=' * 72}\n{t}\n{'=' * 72}")

    head("LLMBook Overview-Presence Audit")
    print(f"Total landing pages: {len(pages)}")
    print(f"  PASS: {len(good)}")
    print(f"  WEAK (<{MIN_OVERVIEW_CHARS} chars): {len(weak)}")
    print(f"  UNCLEAR (only short intro para): {len(unclear)}")
    print(f"  MISSING overview entirely:        {len(missing)}")
    print(f"  Template breakage entries:        {len(template_issues)}")

    head("Missing Overview (no overview-like content)")
    if not missing:
        print("(none)")
    for e in missing:
        print(f"  - {e['rel']}  [{e['kind']}]")

    head("Weak Overview (<150 chars)")
    if not weak:
        print("(none)")
    for e in weak:
        print(f"  - {e['rel']}  [{e['source']}] {e['chars']} chars")
        print(f"      {e['snippet']}")

    head("Unclear / Misplaced Overview")
    if not unclear:
        print("(none)")
    for e in unclear:
        print(f"  - {e['rel']}  [{e['source']}] {e['chars']} chars")
        print(f"      {e['snippet']}")

    head("Template Breakage")
    if not template_issues:
        print("(none)")
    for kind, label, rel, issues in template_issues:
        print(f"  - {rel}  [{kind}]")
        for i in issues:
            print(f"      * {i}")

    head("By Part / Grouping")
    for k in sorted(by_part.keys()):
        ents = by_part[k]
        if not ents:
            continue
        print(f"\n## {k}  ({len(ents)} issue(s))")
        for tag, e in ents:
            print(f"  [{tag}] {e['rel']} -- src={e['source']}, n={e['chars']}")
            if e['template']:
                for ti in e['template']:
                    print(f"     template: {ti}")

    head("PASS Detail (source distribution & char counts)")
    src_counts = defaultdict(int)
    for e in good:
        src_counts[e["source"]] += 1
    for k, v in sorted(src_counts.items()):
        print(f"  {k}: {v}")
    print("\nShortest 10 PASS pages (char-count of overview):")
    for e in sorted(good, key=lambda x: x["chars"])[:10]:
        print(f"  {e['chars']:5d}  [{e['source']:>10s}]  {e['rel']}")
    print("\nAll PASS pages with source=first-para (long intro paragraph):")
    for e in good:
        if e["source"] == "first-para":
            print(f"  {e['chars']:5d}  {e['rel']}")
            print(f"        {e['snippet'][:160]}")

    print(f"\nDone. {len(pages)} pages scanned; "
          f"{len(missing) + len(weak) + len(unclear)} pages need attention.")


if __name__ == "__main__":
    main()
