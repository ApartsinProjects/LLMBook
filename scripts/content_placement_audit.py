#!/usr/bin/env python3
"""Content-placement audit: verify each section's main topic lives in the correct (chapter, part) home.

Read-only scan. Produces docs/content-audit/CONTENT_PLACEMENT_AUDIT.md.
"""

import os
import re
import json
import html
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
OUT = ROOT / "docs" / "content-audit" / "CONTENT_PLACEMENT_AUDIT.md"

# Map of part -> tools-of-the-trade module number (these are NOT main chapters)
TOOLS_MODULES = {5, 14, 19, 25, 30, 36, 41, 45, 51, 56, 61, 71, 79, 83}

# Map module-number -> (part, chapter-title)
MODULE_OWNERS = {}

# Map module-number -> "scope sentence" from chapter index
MODULE_SCOPE = {}

# Map module-number -> module directory path
MODULE_DIR = {}

# Map module-number -> list of section card descriptions
MODULE_SECTION_CARDS = defaultdict(list)


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def parse_module_index(path: Path):
    """Extract chapter overview + section card descriptions."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None, []

    # Get module number from path
    m = re.search(r"module-(\d+[a-z]?)-", str(path))
    if not m:
        return None, []
    mod_num = m.group(1)

    # Find chapter title from <h1>
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
    h1 = strip_tags(h1_m.group(1)) if h1_m else ""

    # Find overview text - usually first long <p> or in a card section
    # Look for "Chapter Overview" or first overview-class block
    overview = ""
    over_m = re.search(r"<div[^>]*class=\"overview[^\"]*\"[^>]*>(.*?)</div>", text, re.DOTALL)
    if over_m:
        overview = strip_tags(over_m.group(1))[:400]

    if not overview:
        # Look for first chapter-subtitle / .chapter-subtitle / first <p> after h1
        sub_m = re.search(r'<p[^>]*class="chapter-subtitle"[^>]*>(.*?)</p>', text, re.DOTALL)
        if sub_m:
            overview = strip_tags(sub_m.group(1))[:400]

    # Find section card titles/desc
    cards = []
    # Section cards: <li class="section-card"> or h3 inside section list
    for card_m in re.finditer(r'<li[^>]*class="[^"]*(?:section|sect|chapter)-card[^"]*"[^>]*>(.*?)</li>', text, re.DOTALL):
        card_text = strip_tags(card_m.group(1))[:300]
        cards.append(card_text)

    # Alternative: section cards via <a class="section-card">
    if not cards:
        for card_m in re.finditer(r'<a[^>]*class="[^"]*(?:section|sect)-card[^"]*"[^>]*>(.*?)</a>', text, re.DOTALL):
            card_text = strip_tags(card_m.group(1))[:300]
            cards.append(card_text)

    return overview, cards


def parse_section(path: Path):
    """Extract h1, h2 keywords, and dominant callout types from a section file."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    # Get section number
    section_m = re.search(r"section-(\d+(?:\.\d+)+)([a-z]?)\.html", path.name)
    if not section_m:
        return None
    section_num = section_m.group(1) + (section_m.group(2) or "")

    # Module number from path
    mod_m = re.search(r"module-(\d+[a-z]?)-", str(path))
    if not mod_m:
        return None
    mod_num = mod_m.group(1)

    # Find h1 - main section title
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
    h1 = strip_tags(h1_m.group(1)) if h1_m else ""

    # Find chapter-subtitle/section-subtitle
    sub_m = re.search(r'<p[^>]*class="(?:chapter|section)-subtitle"[^>]*>(.*?)</p>', text, re.DOTALL)
    subtitle = strip_tags(sub_m.group(1)) if sub_m else ""

    # Find all h2 headings (skip boilerplate)
    h2_list = []
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", text, re.DOTALL):
        ht = strip_tags(m.group(1))
        if ht and ht.lower() not in ("bibliography", "what's next", "what next", "key takeaways", "summary", "exercises", "lab"):
            h2_list.append(ht)

    # Find all h3 headings
    h3_list = []
    for m in re.finditer(r"<h3[^>]*>(.*?)</h3>", text, re.DOTALL):
        ht = strip_tags(m.group(1))
        if ht:
            h3_list.append(ht)

    # Find callout types
    callouts = []
    for m in re.finditer(r'<div[^>]*class="callout (\S+?)(?:\s|")', text):
        callouts.append(m.group(1))
    callout_counts = Counter(callouts)

    # Find significant prose first 800 chars (after h1 / subtitle, before first callout)
    body_text = strip_tags(text)
    # Limit body length
    body_short = body_text[:1500]

    # Try to extract introductory prose - first <p> after h1
    intro_p = ""
    intro_m = re.search(r"<h1[^>]*>.*?</h1>(.*?)(?:<h2|<div\s+class=\"callout)", text, re.DOTALL)
    if intro_m:
        intro_p = strip_tags(intro_m.group(1))[:600]

    return {
        "section_num": section_num,
        "module_num": mod_num,
        "path": str(path).replace("\\", "/"),
        "h1": h1,
        "subtitle": subtitle,
        "h2_list": h2_list[:8],
        "h3_list": h3_list[:12],
        "callouts": dict(callout_counts),
        "intro": intro_p,
    }


def main():
    # 1) Parse module index pages
    for idx in sorted(ROOT.glob("part-*/module-*/index.html")):
        m = re.search(r"module-(\d+[a-z]?)-", str(idx))
        if not m:
            continue
        mod_num = m.group(1)
        MODULE_DIR[mod_num] = idx.parent

        # Determine part number from path
        part_m = re.search(r"part-(\d+)-", str(idx))
        part_num = part_m.group(1) if part_m else "?"

        # Get part folder name for title context
        part_dir = idx.parent.parent.name

        overview, cards = parse_module_index(idx)
        MODULE_OWNERS[mod_num] = (part_num, part_dir)
        MODULE_SCOPE[mod_num] = overview or ""
        MODULE_SECTION_CARDS[mod_num] = cards

    # 2) Parse all sections in main parts
    sections = []
    for sec in sorted(ROOT.glob("part-*/module-*/section-*.html")):
        # Skip KDP/backup paths
        if "KDP" in str(sec) or "backup" in str(sec):
            continue
        s = parse_section(sec)
        if s:
            sections.append(s)

    # Save for downstream analysis
    out_json = ROOT / "docs" / "content-audit" / "_placement_inventory.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "modules": {
                k: {
                    "part": MODULE_OWNERS.get(k, ("?", "?"))[0],
                    "part_dir": MODULE_OWNERS.get(k, ("?", "?"))[1],
                    "scope": MODULE_SCOPE.get(k, ""),
                    "is_tools": (int(k) if k.isdigit() else -1) in TOOLS_MODULES,
                    "cards": MODULE_SECTION_CARDS.get(k, []),
                } for k in MODULE_OWNERS
            },
            "sections": sections,
        }, f, indent=2)

    print(f"Parsed {len(MODULE_OWNERS)} modules, {len(sections)} sections")
    print(f"Saved inventory to {out_json}")

    # 3) Identify misplacement signals
    return sections


if __name__ == "__main__":
    main()
