"""Audit pedagogical scaffolding across every chapter landing page.

Reads main-chapter `index.html` files (part-N-*/module-NN-*/index.html) and
checks the seven canonical scaffolding blocks:

  1. callout looking-back
  2. overview (with h2 'Chapter Overview')
  3. callout big-picture
  4. objectives (or alternate: learning-objectives)
  5. prereqs (or alternate: prerequisites)
  6. h2 'Sections' with ul.sections-list
  7. whats-next (with h3 "What's Next?")

Also gives lighter audit for front-matter and appendices pages.

Writes findings to scaffolding-audit.md at repo root.

READ-ONLY: never modifies HTML. Save script to scripts/_audit_scaffolding.py
for re-runs.
"""

from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, Tag

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
REPORT_PATH = ROOT / "scaffolding-audit.md"

# ----------------------------------------------------------------------
# Block specs
# ----------------------------------------------------------------------

BLOCKS = [
    "looking_back",
    "overview",
    "big_picture",
    "objectives",
    "prereqs",
    "sections",
    "whats_next",
]

BLOCK_LABEL = {
    "looking_back": "Looking Back",
    "overview": "Overview",
    "big_picture": "Big Picture",
    "objectives": "Objectives",
    "prereqs": "Prereqs",
    "sections": "Sections",
    "whats_next": "What's Next?",
}

# Canonical class names (alternates listed second / third)
CANONICAL_CLASS = {
    "objectives": "objectives",
    "prereqs": "prereqs",
}
ALTERNATE_CLASSES = {
    "objectives": ["learning-objectives"],
    "prereqs": ["prerequisites"],
}

MIN_MEANINGFUL_CHARS = 30  # below this -> "empty / near-empty"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def has_class(el: Tag, name: str) -> bool:
    classes = el.get("class") or []
    return name in classes


def find_block_div(
    soup: BeautifulSoup, classes: list[str]
) -> Optional[tuple[Tag, str]]:
    """Find a <div> whose class list contains any of the given names.

    Returns (element, matched_class_name) or None.
    """
    for cls in classes:
        el = soup.find("div", class_=cls)
        if el:
            return el, cls
    return None


def block_text_length(el: Tag) -> int:
    """Count visible characters in the block, excluding the callout-title."""
    # Clone-like: build text from non-title children
    text_parts = []
    for child in el.descendants:
        if isinstance(child, Tag):
            # Skip the callout-title div
            if has_class(child, "callout-title"):
                continue
            # Skip headings that are essentially boilerplate
            if child.name in ("h2", "h3") and child.get_text(strip=True) in {
                "Chapter Overview",
                "Learning Objectives",
                "Prerequisites",
                "What's Next?",
                "What's Next",
                "Sections",
            }:
                continue
    # Simpler: just strip the title text and any matched headings
    raw = el.get_text(" ", strip=True)
    for boiler in [
        "Looking Back",
        "Big Picture",
        "Chapter Overview",
        "Learning Objectives",
        "Prerequisites",
        "What's Next?",
        "What's Next",
        "Sections",
    ]:
        # Remove first occurrence as a leading label
        if raw.startswith(boiler):
            raw = raw[len(boiler) :].strip()
            break
    return len(raw)


def heading_text(el: Tag) -> str:
    h = el.find(["h2", "h3", "h4"])
    return h.get_text(strip=True) if h else ""


def find_sections_block(
    soup: BeautifulSoup,
) -> Optional[tuple[Tag, Tag]]:
    """Find the <h2>Sections</h2> followed by ul.sections-list.

    Returns (h2_tag, ul_tag) or None. We accept ANY <h2> with text 'Sections'
    OR any <ul class="sections-list">.
    """
    h2 = None
    for cand in soup.find_all("h2"):
        if cand.get_text(strip=True).lower() == "sections":
            h2 = cand
            break
    ul = soup.find("ul", class_="sections-list")
    if h2 is None and ul is None:
        return None
    # We accept the block if either is present, but return both (may be None)
    return (h2, ul)


# ----------------------------------------------------------------------
# Per-file analysis
# ----------------------------------------------------------------------


class ChapterReport:
    def __init__(self, path: Path, part_num: int, chap_num: int):
        self.path = path
        self.part_num = part_num
        self.chap_num = chap_num
        self.title = ""
        self.h1 = ""
        # block_status: maps block_name -> 'present' | 'missing' | 'empty' | 'alternate'
        self.block_status: OrderedDict[str, str] = OrderedDict(
            (b, "missing") for b in BLOCKS
        )
        # block_line: line number where block starts (0 if missing)
        self.block_line: dict[str, int] = {b: 0 for b in BLOCKS}
        # alternates used: block -> alt class name
        self.alternates: dict[str, str] = {}
        # empty/near-empty
        self.empty_blocks: list[tuple[str, int]] = []  # (block, length)
        # order issue: list of strings describing
        self.order_issues: list[str] = []

    @property
    def rel_path(self) -> str:
        return str(self.path.relative_to(ROOT)).replace("\\", "/")


def get_line_number(html: str, snippet: str) -> int:
    """Find the 1-based line number of snippet in html.

    Strategy: shorten the snippet to just the opening tag (up to and including
    the first '>') so we are robust to BS4 serialization differences.
    """
    # Try full snippet first
    idx = html.find(snippet)
    if idx < 0:
        # Fall back: just the opening tag
        end_of_tag = snippet.find(">") + 1
        if end_of_tag > 0:
            tag_only = snippet[:end_of_tag]
            idx = html.find(tag_only)
    if idx < 0:
        return 0
    return html.count("\n", 0, idx) + 1


def analyze_main_chapter(path: Path) -> ChapterReport:
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Extract part and chapter numbers
    m_part = re.search(r"part-(\d+)-", str(path))
    m_chap = re.search(r"module-(\d+)-", str(path))
    part_num = int(m_part.group(1)) if m_part else 0
    chap_num = int(m_chap.group(1)) if m_chap else 0

    rep = ChapterReport(path, part_num, chap_num)
    title_tag = soup.find("title")
    rep.title = title_tag.get_text(strip=True) if title_tag else ""
    h1 = soup.find("h1")
    rep.h1 = h1.get_text(strip=True) if h1 else ""

    # Track block locations to detect order issues
    block_positions: dict[str, int] = {}

    # --- 1) Looking Back (callout looking-back) ---
    el = soup.find("div", class_="looking-back")
    if el:
        status = (
            "empty" if block_text_length(el) < MIN_MEANINGFUL_CHARS else "present"
        )
        rep.block_status["looking_back"] = status
        snippet = str(el)[:80]
        line = get_line_number(html, snippet)
        rep.block_line["looking_back"] = line
        block_positions["looking_back"] = line
        if status == "empty":
            rep.empty_blocks.append(("looking_back", block_text_length(el)))

    # --- 2) Overview ---
    el = soup.find("div", class_="overview")
    if el:
        # We expect h2 'Chapter Overview' (but accept any heading)
        status = (
            "empty" if block_text_length(el) < MIN_MEANINGFUL_CHARS else "present"
        )
        rep.block_status["overview"] = status
        snippet = str(el)[:80]
        line = get_line_number(html, snippet)
        rep.block_line["overview"] = line
        block_positions["overview"] = line
        if status == "empty":
            rep.empty_blocks.append(("overview", block_text_length(el)))

    # --- 3) Big Picture (callout big-picture) ---
    el = soup.find("div", class_="big-picture")
    if el:
        status = (
            "empty" if block_text_length(el) < MIN_MEANINGFUL_CHARS else "present"
        )
        rep.block_status["big_picture"] = status
        snippet = str(el)[:80]
        line = get_line_number(html, snippet)
        rep.block_line["big_picture"] = line
        block_positions["big_picture"] = line
        if status == "empty":
            rep.empty_blocks.append(("big_picture", block_text_length(el)))

    # --- 4) Objectives (canonical: "objectives", alt: "learning-objectives") ---
    el_pair = find_block_div(soup, ["objectives", "learning-objectives"])
    if el_pair:
        el, matched_cls = el_pair
        is_alt = matched_cls != CANONICAL_CLASS["objectives"]
        status = (
            "empty" if block_text_length(el) < MIN_MEANINGFUL_CHARS else "present"
        )
        if is_alt and status == "present":
            status = "alternate"
            rep.alternates["objectives"] = matched_cls
        rep.block_status["objectives"] = status
        snippet = str(el)[:80]
        line = get_line_number(html, snippet)
        rep.block_line["objectives"] = line
        block_positions["objectives"] = line
        if status == "empty":
            rep.empty_blocks.append(("objectives", block_text_length(el)))

    # --- 5) Prereqs (canonical: "prereqs", alt: "prerequisites") ---
    el_pair = find_block_div(soup, ["prereqs", "prerequisites"])
    if el_pair:
        el, matched_cls = el_pair
        is_alt = matched_cls != CANONICAL_CLASS["prereqs"]
        status = (
            "empty" if block_text_length(el) < MIN_MEANINGFUL_CHARS else "present"
        )
        if is_alt and status == "present":
            status = "alternate"
            rep.alternates["prereqs"] = matched_cls
        rep.block_status["prereqs"] = status
        snippet = str(el)[:80]
        line = get_line_number(html, snippet)
        rep.block_line["prereqs"] = line
        block_positions["prereqs"] = line
        if status == "empty":
            rep.empty_blocks.append(("prereqs", block_text_length(el)))

    # --- 6) Sections h2 + sections-list ul ---
    sec_pair = find_sections_block(soup)
    if sec_pair:
        h2_tag, ul_tag = sec_pair
        if ul_tag is not None:
            # Count li children
            lis = ul_tag.find_all("li", recursive=False)
            status = "present" if lis else "empty"
            snippet_src = ul_tag
        elif h2_tag is not None:
            status = "empty"
            snippet_src = h2_tag
        else:
            status = "missing"
            snippet_src = None
        rep.block_status["sections"] = status
        if snippet_src is not None:
            snippet = str(snippet_src)[:80]
            line = get_line_number(html, snippet)
            rep.block_line["sections"] = line
            block_positions["sections"] = line
        if status == "empty":
            length = len(ul_tag.get_text(strip=True)) if ul_tag is not None else 0
            rep.empty_blocks.append(("sections", length))

    # --- 7) What's Next ---
    el = soup.find("div", class_="whats-next")
    if el:
        status = (
            "empty" if block_text_length(el) < MIN_MEANINGFUL_CHARS else "present"
        )
        rep.block_status["whats_next"] = status
        snippet = str(el)[:80]
        line = get_line_number(html, snippet)
        rep.block_line["whats_next"] = line
        block_positions["whats_next"] = line
        if status == "empty":
            rep.empty_blocks.append(("whats_next", block_text_length(el)))

    # --- Order check ---
    # Expected order:
    expected_order = [
        "looking_back",
        "overview",
        "big_picture",
        "objectives",
        "prereqs",
        "sections",
        "whats_next",
    ]
    # Project to present blocks only
    present_seq = [
        (block_positions[b], b) for b in expected_order if b in block_positions
    ]
    actual_seq = sorted(present_seq)
    expected_seq = [(0, b) for b in expected_order if b in block_positions]
    # Compare block order
    if [a[1] for a in actual_seq] != [
        b for b in expected_order if b in block_positions
    ]:
        actual_order = [a[1] for a in actual_seq]
        expected_blocks_present = [b for b in expected_order if b in block_positions]
        rep.order_issues.append(
            f"Actual order: {' -> '.join(actual_order)}; "
            f"expected: {' -> '.join(expected_blocks_present)}"
        )

    return rep


# ----------------------------------------------------------------------
# Front-matter and appendix audits
# ----------------------------------------------------------------------


class LightReport:
    def __init__(self, path: Path, kind: str):
        self.path = path
        self.kind = kind  # 'front-matter' | 'appendix' | 'glossary'
        self.has_h1 = False
        self.h1_text = ""
        self.has_intro = False
        self.intro_chars = 0
        self.has_chapter_nav = False
        self.has_sections_list = False
        # Bare = no intro AND no sections list AND no scaffolding
        self.is_bare = False
        self.notes: list[str] = []

    @property
    def rel_path(self) -> str:
        return str(self.path.relative_to(ROOT)).replace("\\", "/")


def analyze_light(path: Path, kind: str) -> LightReport:
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    rep = LightReport(path, kind)
    h1 = soup.find("h1")
    if h1:
        rep.has_h1 = True
        rep.h1_text = h1.get_text(strip=True)
    # Find the main element
    main = soup.find("main") or soup
    # Intro = the FIRST <p> inside <main> (after possible <figure>/<header>) with > 50 chars
    intro_chars = 0
    for p in main.find_all("p", recursive=True)[:5]:
        # Skip if inside chapter-nav or footer
        if p.find_parent(["nav", "footer"]):
            continue
        txt = p.get_text(strip=True)
        if len(txt) > intro_chars:
            intro_chars = len(txt)
    rep.intro_chars = intro_chars
    rep.has_intro = intro_chars >= MIN_MEANINGFUL_CHARS
    # chapter-nav
    rep.has_chapter_nav = bool(soup.find("nav", class_="chapter-nav"))
    # sections list
    rep.has_sections_list = bool(soup.find("ul", class_="sections-list"))
    # Bare = h1 only with no intro
    if rep.has_h1 and not rep.has_intro and not rep.has_sections_list:
        rep.is_bare = True
    return rep


# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------


def status_glyph(s: str) -> str:
    return {
        "present": "OK",
        "missing": "MISS",
        "empty": "EMPTY",
        "alternate": "ALT",
    }[s]


def main() -> None:
    main_chapters: list[ChapterReport] = []
    for path in sorted(
        ROOT.glob("part-*/module-*/index.html"),
        key=lambda p: (
            int(re.search(r"part-(\d+)", str(p)).group(1)),
            int(re.search(r"module-(\d+)", str(p)).group(1)),
        ),
    ):
        rep = analyze_main_chapter(path)
        main_chapters.append(rep)

    front_matter_pages: list[LightReport] = []
    for path in sorted((ROOT / "front-matter").glob("*.html")):
        front_matter_pages.append(analyze_light(path, "front-matter"))

    appendix_pages: list[LightReport] = []
    for path in sorted((ROOT / "appendices").glob("appendix-*/index.html")):
        appendix_pages.append(analyze_light(path, "appendix"))
    glossary_path = ROOT / "appendices" / "glossary" / "index.html"
    if glossary_path.exists():
        appendix_pages.append(analyze_light(glossary_path, "glossary"))

    # ---- Aggregate stats ----
    n_total = len(main_chapters)
    block_stats: dict[str, dict[str, int]] = {
        b: {"present": 0, "missing": 0, "empty": 0, "alternate": 0} for b in BLOCKS
    }
    for ch in main_chapters:
        for b in BLOCKS:
            block_stats[b][ch.block_status[b]] += 1

    # ---- Build report ----
    lines: list[str] = []
    lines.append("# Pedagogical Scaffolding Audit")
    lines.append("")
    lines.append(
        "Audit of the seven canonical scaffolding blocks on every chapter landing page "
        "(`part-N-*/module-NN-*/index.html`), plus a lighter audit of front-matter and "
        "appendix pages."
    )
    lines.append("")
    lines.append(f"- Main chapters audited: **{n_total}**")
    lines.append(f"- Front-matter pages audited: **{len(front_matter_pages)}**")
    lines.append(f"- Appendix pages audited: **{len(appendix_pages)}**")
    lines.append("")
    lines.append("Legend (per-chapter table): `OK` = present, `MISS` = missing, "
                 "`EMPTY` = present but <30 chars meaningful content, `ALT` = uses "
                 "alternate class name (flagged for normalization).")
    lines.append("")

    # ---- (1) Summary table ----
    lines.append("## 1. Summary: Block Coverage Across Main Chapters")
    lines.append("")
    lines.append(
        "| Block | Total | Present | Missing | Empty | Alt-class |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|")
    for b in BLOCKS:
        s = block_stats[b]
        lines.append(
            f"| {BLOCK_LABEL[b]} | {n_total} | {s['present']} | {s['missing']} | "
            f"{s['empty']} | {s['alternate']} |"
        )
    lines.append("")

    # Headline missing-block counts for quick scan
    lines.append("**Headline missing-block counts (across all main chapters):**")
    lines.append("")
    for b in BLOCKS:
        s = block_stats[b]
        missing_or_empty = s["missing"] + s["empty"]
        lines.append(
            f"- {BLOCK_LABEL[b]}: **{s['missing']} missing**, {s['empty']} empty, "
            f"{s['alternate']} using alternate class"
        )
    lines.append("")

    # ---- (2) Per-chapter checklist ----
    lines.append("## 2. Per-Chapter Checklist")
    lines.append("")
    lines.append(
        "| Part | Ch | Title | Looking Back | Overview | Big Picture | "
        "Objectives | Prereqs | Sections | What's Next? |"
    )
    lines.append("|---:|---:|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|")
    for ch in main_chapters:
        row_cells = [status_glyph(ch.block_status[b]) for b in BLOCKS]
        # Shorten title
        short_title = ch.h1[:60]
        lines.append(
            f"| {ch.part_num} | {ch.chap_num} | {short_title} | "
            + " | ".join(row_cells)
            + " |"
        )
    lines.append("")

    # ---- (3) Empty / near-empty blocks ----
    lines.append("## 3. Empty / Near-Empty Blocks")
    lines.append("")
    empty_rows = [ch for ch in main_chapters if ch.empty_blocks]
    if not empty_rows:
        lines.append("_No empty blocks detected._")
    else:
        lines.append("Blocks with less than 30 chars of meaningful content "
                     "(excluding the block heading/title).")
        lines.append("")
        for ch in empty_rows:
            lines.append(f"- **Ch {ch.chap_num}** ({ch.rel_path}):")
            for b, length in ch.empty_blocks:
                lines.append(f"    - {BLOCK_LABEL[b]} (~{length} chars)")
    lines.append("")

    # ---- (4) Out-of-order chapters ----
    lines.append("## 4. Out-of-Order Chapters")
    lines.append("")
    out_of_order = [ch for ch in main_chapters if ch.order_issues]
    if not out_of_order:
        lines.append("_No order issues detected — every chapter that has multiple "
                     "scaffolding blocks has them in conventional order._")
    else:
        lines.append(
            "Expected order: Looking Back -> Overview -> Big Picture -> "
            "Objectives -> Prereqs -> Sections -> What's Next?"
        )
        lines.append("")
        for ch in out_of_order:
            # First block of file (lowest line number)
            first_block_line = min(
                (ln for ln in ch.block_line.values() if ln > 0), default=0
            )
            lines.append(
                f"- **Ch {ch.chap_num}** ({ch.rel_path}:{first_block_line})"
            )
            for issue in ch.order_issues:
                lines.append(f"    - {issue}")
            # Show each block's line number
            line_strs = [
                f"{BLOCK_LABEL[b]} L{ch.block_line[b]}"
                for b in BLOCKS
                if ch.block_line[b] > 0
            ]
            lines.append(f"    - Line locations: {'; '.join(line_strs)}")
    lines.append("")

    # ---- (5) Alternate-class-name chapters ----
    lines.append("## 5. Alternate Class Names (Flagged for Normalization)")
    lines.append("")
    alt_chapters = [ch for ch in main_chapters if ch.alternates]
    if not alt_chapters:
        lines.append("_No chapters using alternate class names._")
    else:
        canonical_map = {
            "objectives": "`objectives`",
            "prereqs": "`prereqs`",
        }
        lines.append("Canonical class names per block:")
        for b, c in canonical_map.items():
            alts = ", ".join(f"`{x}`" for x in ALTERNATE_CLASSES[b])
            lines.append(f"- {BLOCK_LABEL[b]}: canonical {c}, alternates: {alts}")
        lines.append("")
        lines.append("Chapters using alternate class names:")
        lines.append("")
        for ch in alt_chapters:
            alt_strs = ", ".join(
                f"{BLOCK_LABEL[b]} uses `{cls}`" for b, cls in ch.alternates.items()
            )
            lines.append(f"- **Ch {ch.chap_num}** ({ch.rel_path}): {alt_strs}")
    lines.append("")

    # ---- (6) Front Matter + Appendices ----
    lines.append("## 6. Front Matter + Appendices (Lighter Criteria)")
    lines.append("")
    lines.append(
        "Lighter criteria: each page should have an `<h1>` plus an intro paragraph "
        "(>= 30 chars). Bare pages (h1 with no intro and no sections list) are flagged."
    )
    lines.append("")
    lines.append("### Front Matter")
    lines.append("")
    lines.append(
        "| File | H1 | Intro (chars) | Sections list | Chapter-nav | Bare? |"
    )
    lines.append("|---|:-:|---:|:-:|:-:|:-:|")
    for r in front_matter_pages:
        lines.append(
            f"| {r.rel_path} | {'OK' if r.has_h1 else 'MISS'} | {r.intro_chars} | "
            f"{'OK' if r.has_sections_list else '-'} | "
            f"{'OK' if r.has_chapter_nav else 'MISS'} | "
            f"{'YES' if r.is_bare else '-'} |"
        )
    lines.append("")
    bare_fm = [r for r in front_matter_pages if r.is_bare]
    if bare_fm:
        lines.append("**Bare front-matter pages (no intro + no sections list):**")
        lines.append("")
        for r in bare_fm:
            lines.append(f"- {r.rel_path}")
        lines.append("")

    lines.append("### Appendices + Glossary")
    lines.append("")
    lines.append(
        "| File | H1 | Intro (chars) | Sections list | Chapter-nav | Bare? |"
    )
    lines.append("|---|:-:|---:|:-:|:-:|:-:|")
    for r in appendix_pages:
        lines.append(
            f"| {r.rel_path} | {'OK' if r.has_h1 else 'MISS'} | {r.intro_chars} | "
            f"{'OK' if r.has_sections_list else '-'} | "
            f"{'OK' if r.has_chapter_nav else 'MISS'} | "
            f"{'YES' if r.is_bare else '-'} |"
        )
    lines.append("")
    bare_apx = [r for r in appendix_pages if r.is_bare]
    if bare_apx:
        lines.append("**Bare appendix pages (no intro + no sections list):**")
        lines.append("")
        for r in bare_apx:
            lines.append(f"- {r.rel_path}")
        lines.append("")

    # ---- (7) Recommended fix priority ----
    lines.append("## 7. Recommended Fix Priority")
    lines.append("")

    # Compute totals for prioritisation
    most_missing = sorted(
        BLOCKS, key=lambda b: block_stats[b]["missing"], reverse=True
    )
    top_missing = [
        f"{BLOCK_LABEL[b]} ({block_stats[b]['missing']} chapters)"
        for b in most_missing
        if block_stats[b]["missing"] > 0
    ][:3]
    alt_count = sum(1 for ch in main_chapters if ch.alternates)
    empty_count = len([ch for ch in main_chapters if ch.empty_blocks])
    order_count = len(out_of_order)

    bullets: list[str] = []
    if top_missing:
        bullets.append(
            f"**Add the most commonly missing block first:** "
            f"top three deficits are {'; '.join(top_missing)}. Adding Big Picture "
            f"(missing on Part 1 chapters 0 to 5 plus Chapter 6) and re-adding the "
            f"five missing blocks on Part 12 industry chapters delivers the largest "
            f"per-chapter improvement."
        )
    if alt_count > 0:
        bullets.append(
            f"**Normalize alternate class names** in {alt_count} chapter(s) so the "
            f"CSS, navigation, and exporters can rely on a single canonical class "
            f"(`objectives`, `prereqs`). Mechanical find-replace; no content changes."
        )
    if empty_count > 0:
        bullets.append(
            f"**Fill empty / near-empty blocks** in {empty_count} chapter(s). These "
            f"usually only need a 1-2 sentence recap or bridge, but reads as "
            f"broken markup on the rendered page."
        )
    if order_count > 0:
        bullets.append(
            f"**Re-order misordered scaffolding** in {order_count} chapter(s). "
            f"Convention: Looking Back -> Overview -> Big Picture -> Objectives -> "
            f"Prereqs -> Sections -> What's Next?"
        )
    bullets.append(
        "**Treat Part 12 (industry chapters) as a distinct template.** Chapters 36-42 "
        "follow a Big Picture + use-cases + failure-modes pattern that intentionally "
        "skips Looking Back, Overview, Objectives, Prereqs, and What's Next. Decide "
        "explicitly whether this is the documented convention or a drift to be "
        "harmonised with the rest of the book."
    )
    bullets.append(
        "**Reconcile the chapter template with current convention.** "
        "`templates/chapter-index.html` already exists, but it does NOT include "
        "the `callout looking-back` block and orders objectives BEFORE prereqs. "
        "The 11 out-of-order chapters (all in Parts 1 and 2) match a slightly "
        "older convention with prereqs BEFORE objectives. Decide which order is "
        "canonical, then update the template AND the drifted chapters to match."
    )
    bullets.append(
        "**Run this audit as part of CI** (`scripts/_audit_scaffolding.py`). The "
        "summary table at the top of the report is the regression check; fail the "
        "build when any block's missing count increases."
    )
    bullets.append(
        "**Add the missing Big Picture callout to the seven Part 1 / 2 chapters** "
        "first. These are core foundational chapters whose pedagogical value "
        "benefits most from a single-paragraph why-this-matters block; the rest "
        "of the convention is already in place."
    )
    bullets.append(
        "**Decide whether the missing Learning Objectives in chapters 34 and 35 "
        "(Part 11) are intentional.** Both chapters jump directly from the "
        "Big Picture callout to Prerequisites, skipping Learning Objectives. "
        "These two chapters are short enough that adding 3-4 bullet objectives "
        "would noticeably improve scannability."
    )

    for b in bullets[:7]:
        lines.append(f"- {b}")
    lines.append("")

    # ---- Footer ----
    lines.append("---")
    lines.append("")
    lines.append(
        f"_Generated by `scripts/_audit_scaffolding.py`. Re-run with "
        f"`/c/Python314/python scripts/_audit_scaffolding.py`._"
    )
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")
    print(f"Lines: {len(lines)}")
    print("Headline missing counts:")
    for b in BLOCKS:
        s = block_stats[b]
        print(
            f"  {BLOCK_LABEL[b]:14}  missing={s['missing']:2d}  "
            f"empty={s['empty']:2d}  alt={s['alternate']:2d}"
        )


if __name__ == "__main__":
    main()
