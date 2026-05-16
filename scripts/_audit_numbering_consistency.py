"""Audit numbering consistency across the LLM Book.

This is a READ-ONLY audit that walks every content HTML page, builds a book-wide
inventory of section files, figure captions, code-fragment captions, chapter dirs,
part dirs, and appendix dirs, and then checks every prose reference inside body
content (excluding nav/header/footer chrome) against that inventory.

Categories of problems:
  - phantom        : prose cites a number that does not exist anywhere
  - drift          : prose cites X.Y but only X.(Y-1) or X.(Y+1) exists
  - letter-mismatch: prose says "Appendix AD" but target page renders as "Appendix Q"
  - cross-ref-broken: <a href> anchor text says one number but resolves elsewhere
  - duplicate      : same caption label appears on multiple pages
  - gap            : a chapter has captions 1, 2, 4 but not 3

Output: numbering-audit.md at the project root.

Usage: python scripts/_audit_numbering_consistency.py
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIR_PARTS = {
    "KDP",
    ".claude",
    "scripts",
    "node_modules",
    "pagefind",
    "templates",
    "vendor",
    "agents",
    "__pycache__",
}


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    for ex in EXCLUDE_DIR_PARTS:
        if ex in parts:
            return True
    name = path.name.lower()
    if name.startswith("temp_") or "backups" in name or name.endswith(".bak.html"):
        return True
    # Skip files in any directory that matches temp_* or *backups*
    for p in path.parts:
        pl = p.lower()
        if pl.startswith("temp_") or "backups" in pl:
            return True
    return False


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*.html"):
        if is_excluded(p.relative_to(ROOT)):
            continue
        files.append(p)
    return sorted(files)


# ---------------------------------------------------------------------------
# Inventory construction
# ---------------------------------------------------------------------------

# Map of "X.Y" or "X.Y.Z" -> list[Path] of section files
SECTION_FILES: dict[str, list[Path]] = defaultdict(list)
# Map of chapter number (int) -> list[Path] of module index.html files
CHAPTER_DIRS: dict[int, list[Path]] = defaultdict(list)
# Map of part roman numeral -> Path
PART_DIRS: dict[str, Path] = {}
PART_NUM_TO_ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
    6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
    11: "XI", 12: "XII",
}
ROMAN_TO_PART_NUM = {v: k for k, v in PART_NUM_TO_ROMAN.items()}

# Appendix display letters seen in the appendix index, mapped to the actual
# directory letter that hosts that appendix.
# e.g. "G" -> "f" because Appendix G lives in appendix-f-hardware-compute/
APPENDIX_DISPLAY_TO_DIR: dict[str, str] = {}
APPENDIX_DIR_TO_DISPLAY: dict[str, str] = {}

# label "X.Y.Z" -> list[(file_path, line_no, full_caption_text)]
FIGURE_CAPTIONS: dict[str, list[tuple[Path, int, str]]] = defaultdict(list)
CODE_CAPTIONS: dict[str, list[tuple[Path, int, str]]] = defaultdict(list)


def parse_filename_section_label(filename: str) -> str | None:
    """section-12.3.html -> "12.3". section-f.2.html -> None (glossary)."""
    m = re.match(r"section-(\d+(?:\.\d+)*)\.html$", filename)
    return m.group(1) if m else None


def build_directory_inventory() -> None:
    # Section files
    for path in ROOT.rglob("section-*.html"):
        rel = path.relative_to(ROOT)
        if is_excluded(rel):
            continue
        label = parse_filename_section_label(path.name)
        if not label:
            continue
        SECTION_FILES[label].append(path)

    # Module / chapter directories
    for path in ROOT.glob("part-*/module-*/index.html"):
        rel = path.relative_to(ROOT)
        if is_excluded(rel):
            continue
        m = re.match(r"module-(\d+)", path.parent.name)
        if m:
            CHAPTER_DIRS[int(m.group(1))].append(path)

    # Part directories
    for path in ROOT.glob("part-*/index.html"):
        rel = path.relative_to(ROOT)
        if is_excluded(rel):
            continue
        m = re.match(r"part-(\d+)", path.parent.name)
        if m:
            num = int(m.group(1))
            roman = PART_NUM_TO_ROMAN.get(num)
            if roman:
                PART_DIRS[roman] = path


def build_appendix_letter_map() -> None:
    """Parse appendices/index.html cards to build display<->directory map."""
    idx = ROOT / "appendices" / "index.html"
    if not idx.exists():
        return
    soup = BeautifulSoup(idx.read_text(encoding="utf-8", errors="replace"), "html.parser")
    for card in soup.select("div.chapter-card"):
        header = card.select_one("div.chapter-card-header span.mod-num")
        if not header:
            continue
        header_text = header.get_text(strip=True)
        m = re.match(r"Appendix\s+([A-Z][A-Z]?)$", header_text)
        if not m:
            continue
        display_letter = m.group(1)
        # Find the right "Read Appendix X →" link, not glossary-link sublinks
        link = None
        for a in card.select("div.chapter-card-body a"):
            if "Read" in a.get_text():
                link = a
                break
        if link is None:
            continue
        href = link.get("href", "")
        # appendix-x-foo/index.html or glossary/index.html
        dm = re.match(r"appendix-([a-z])-", href)
        if dm:
            dir_letter = dm.group(1).upper()
        elif href.startswith("glossary/"):
            dir_letter = "GLOSSARY"
        else:
            dir_letter = "?"
        APPENDIX_DISPLAY_TO_DIR[display_letter] = dir_letter
        APPENDIX_DIR_TO_DISPLAY[dir_letter] = display_letter


CAPTION_FIGURE_RE = re.compile(
    r"^\s*figure\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE
)
CAPTION_CODE_RE = re.compile(
    r"^\s*code\s+fragment\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE
)


def build_caption_inventory() -> None:
    for path in iter_html_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        soup = BeautifulSoup(text, "html.parser")
        # Figures: <figcaption>, <div class="diagram-caption">, and table <caption>
        candidates = (
            soup.find_all(["figcaption", "caption"])
            + soup.find_all("div", class_=["diagram-caption"])
        )
        for el in candidates:
            t = el.get_text(" ", strip=True)
            m = CAPTION_FIGURE_RE.match(t)
            if m:
                label = m.group(1)
                FIGURE_CAPTIONS[label].append((path, 0, t[:200]))
        # Code captions
        for el in soup.find_all("div", class_=["code-caption"]):
            t = el.get_text(" ", strip=True)
            m = CAPTION_CODE_RE.match(t)
            if m:
                label = m.group(1)
                CODE_CAPTIONS[label].append((path, 0, t[:200]))


# ---------------------------------------------------------------------------
# Reference scanning inside body prose
# ---------------------------------------------------------------------------

# Reference patterns. We compile a single combined regex for speed.
# Group 1 names which category the match belongs to.
REF_PATTERNS = [
    # Capture potentially alphanumeric suffix components (e.g. 17.1.1a) so we
    # match the full label, not just its numeric prefix.
    ("section", re.compile(
        r"\bSection\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
        re.IGNORECASE,
    )),
    ("figure", re.compile(
        r"\bFigure\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
        re.IGNORECASE,
    )),
    ("code_fragment", re.compile(
        r"\bCode\s+Fragment\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
        re.IGNORECASE,
    )),
    ("chapter", re.compile(r"\bChapter\s+(\d{1,2})\b", re.IGNORECASE)),
    # Roman I-XII, no empty match. We list every valid roman explicitly to
    # avoid the V?I{0,3} bug which accepts an empty string.
    ("part", re.compile(
        r"\bPart\s+(XII|XI|IX|VIII|VII|VI|IV|III|II|I|X|V)\b"
    )),
    ("appendix", re.compile(r"\bAppendix\s+([A-Z][A-Z]?)\b")),
]

# Tags that contain navigation chrome we should ignore.
CHROME_SELECTORS = [
    "nav.chapter-nav",
    "nav.header-nav",
    "footer",
    "header",  # chapter header includes label "Chapter X" badges
    "div.chapter-card",  # part overview cards
    "aside.references",  # bibliography lists
    "div.further-reading",
    "div.bibliography",
    # Code blocks: refs in comments inside fenced code are not prose claims.
    "pre",
    "code",
    # KaTeX-rendered math and SVG diagrams may contain decimal numbers that
    # look like section/figure IDs but are math content.
    "span.katex",
    "svg",
    # Figure captions are inventory, not citation prose.
    "figcaption",
    "div.diagram-caption",
    "div.code-caption",
    # Per-section ToC asides ("What's in this section: 30.1.1 ... 30.1.2 ...")
    # are inventory, not citation.
    "aside.section-internal-toc",
    # Header navigation chip ("Section 12.3") inside chapter labels
    "div.chapter-label",
    "div.part-label",
]


def strip_chrome(soup: BeautifulSoup) -> Tag:
    """Return <main> (or body) with chrome removed."""
    main = soup.find("main") or soup.body or soup
    if main is None:
        return soup
    # Make a working copy by re-parsing
    main_copy = BeautifulSoup(str(main), "html.parser")
    for sel in CHROME_SELECTORS:
        for el in main_copy.select(sel):
            el.decompose()
    return main_copy


def gather_text_with_lines(html_text: str) -> list[tuple[int, str]]:
    """Approximate per-line text from body content (chrome removed).

    Strategy: re-parse the trimmed body to get its serialized HTML, then walk
    the *original* file looking for the same text positions to get line numbers.
    For our purposes "good enough" line attribution is fine — we record the
    line number of the first occurrence of the matched phrase in the source.
    """
    soup = BeautifulSoup(html_text, "html.parser")
    body = strip_chrome(soup)
    # Get plain-text-with-tags removed for matching
    text_chunks: list[tuple[int, str]] = []
    # We want line numbers, so iterate the original source line-by-line and
    # mark lines that fall inside the trimmed body.
    # Easier: get the set of decoded plain text from body, then linearly scan
    # the original file for each match phrase to recover line numbers.
    plain = body.get_text(" ", strip=False)
    text_chunks.append((1, plain))
    return text_chunks


def find_line_for_phrase(html_text: str, phrase: str, used: set[int]) -> int:
    """Return the line number of the first occurrence of phrase in html_text
    that has not yet been used (for de-duplication when the same phrase
    appears multiple times on different lines). If no fresh occurrence is
    available, return the first occurrence's line anyway (better than 0).
    """
    start = 0
    first_line = 0
    while True:
        idx = html_text.find(phrase, start)
        if idx < 0:
            return first_line  # no more occurrences; return what we have
        line = html_text.count("\n", 0, idx) + 1
        if first_line == 0:
            first_line = line
        if line not in used:
            used.add(line)
            return line
        start = idx + 1


# ---------------------------------------------------------------------------
# Reference categorisation and resolution
# ---------------------------------------------------------------------------

def section_exists(label: str) -> bool:
    """Return True if a section file (or its parent subsection page) exists.

    A reference to "Section 4.2.1" is satisfied if section-4.2.1.html exists,
    OR if section-4.2.html exists AND contains a subsection 4.2.1 (verified by
    anchor id or by an <h2>/<h3>/<h4> whose text starts with the label).
    """
    if label in SECTION_FILES and len(SECTION_FILES[label]) > 0:
        return True
    # Try the parent: drop the last component
    parts = label.split(".")
    if len(parts) >= 3:
        parent = ".".join(parts[:-1])
        if parent in SECTION_FILES and len(SECTION_FILES[parent]) > 0:
            anchor = "-".join(parts)
            heading_re = re.compile(
                r"<h[2-4][^>]*>\s*<[^>]+>\s*"
                + re.escape(label) + r"\b|<h[2-4][^>]*>\s*"
                + re.escape(label) + r"\b",
                re.IGNORECASE,
            )
            anchor_re = re.compile(
                r'id="' + re.escape(anchor) + r'(?:-[^"]*)?"', re.IGNORECASE
            )
            for p in SECTION_FILES[parent]:
                try:
                    txt = p.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if anchor_re.search(txt) or heading_re.search(txt):
                    return True
    return False


def chapter_exists(num: int) -> bool:
    return num in CHAPTER_DIRS and len(CHAPTER_DIRS[num]) > 0


def part_exists(roman: str) -> bool:
    return roman in PART_DIRS


def appendix_display_exists(letter: str) -> bool:
    return letter in APPENDIX_DISPLAY_TO_DIR


def closest_section_candidates(label: str) -> list[str]:
    """Return existing section labels that share the same prefix or differ by
    one in the last component. e.g. for "12.3.4" we look for "12.3.3" and
    "12.3.5", plus any "12.3.*" siblings.
    """
    parts = label.split(".")
    if not parts:
        return []
    last = parts[-1]
    head = ".".join(parts[:-1])
    candidates: list[str] = []
    try:
        n = int(last)
        for delta in (-1, 1, -2, 2):
            sib = f"{head}.{n + delta}" if head else f"{n + delta}"
            if sib in SECTION_FILES:
                candidates.append(sib)
    except ValueError:
        pass
    # Also list any existing siblings
    siblings = [k for k in SECTION_FILES if k.startswith(head + ".")]
    for s in sorted(siblings):
        if s not in candidates and s != label:
            candidates.append(s)
    return candidates[:5]


def closest_caption_candidates(
    label: str, inventory: dict[str, list]
) -> list[str]:
    parts = label.split(".")
    if not parts:
        return []
    last = parts[-1]
    head = ".".join(parts[:-1])
    candidates: list[str] = []
    try:
        n = int(last)
        for delta in (-1, 1, -2, 2):
            sib = f"{head}.{n + delta}"
            if sib in inventory:
                candidates.append(sib)
    except ValueError:
        pass
    siblings = sorted(k for k in inventory if k.startswith(head + ".") and k != label)
    for s in siblings:
        if s not in candidates:
            candidates.append(s)
    return candidates[:5]


# ---------------------------------------------------------------------------
# Cross-reference href check
# ---------------------------------------------------------------------------

XREF_SECTION_RE = re.compile(r"\bSection\s+(\d+(?:\.\d+)+)\b", re.IGNORECASE)


def check_xref_hrefs(path: Path) -> list[dict]:
    """For every <a href>...Section X.Y...</a> in the body, verify the href
    resolves to section-X.Y.html (or contains the right anchor)."""
    try:
        html_text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    soup = BeautifulSoup(html_text, "html.parser")
    body = strip_chrome(soup)
    problems: list[dict] = []
    for a in body.find_all("a", href=True):
        anchor_text = a.get_text(" ", strip=True)
        m = XREF_SECTION_RE.search(anchor_text)
        if not m:
            continue
        prose_label = m.group(1)
        href = a["href"]
        # Strip query/fragment
        href_path = href.split("#", 1)[0].split("?", 1)[0]
        if not href_path:
            continue
        fn = os.path.basename(href_path)
        href_m = re.match(r"section-(\d+(?:\.\d+)+)\.html$", fn)
        if not href_m:
            continue  # not pointing to a section file
        href_label = href_m.group(1)
        # Tolerate hierarchical relationships: prose "Section 12.3" → href
        # section-12.3.1.html (child) or section-12.html (ancestor) are both
        # legitimate. Only flag if neither label is a prefix of the other.
        if href_label == prose_label:
            continue
        if href_label.startswith(prose_label + "."):
            continue
        if prose_label.startswith(href_label + "."):
            continue
        problems.append({
            "file": path,
            "prose_label": prose_label,
            "href": href,
            "href_label": href_label,
            "anchor_text": anchor_text[:120],
        })
    return problems


# ---------------------------------------------------------------------------
# Appendix letter check (visit target page, see how it renders)
# ---------------------------------------------------------------------------

# label "AD" -> what its destination index.html actually renders as (read once)
APPENDIX_TARGET_RENDER_CACHE: dict[str, str] = {}


def appendix_target_renders_as(display_letter: str) -> str | None:
    """Visit the target index.html for an appendix display letter, return the
    'Appendix X' string that the page's h1 actually shows (or None if not
    found). Cached.
    """
    if display_letter in APPENDIX_TARGET_RENDER_CACHE:
        return APPENDIX_TARGET_RENDER_CACHE[display_letter]
    dir_letter = APPENDIX_DISPLAY_TO_DIR.get(display_letter)
    if not dir_letter:
        APPENDIX_TARGET_RENDER_CACHE[display_letter] = ""
        return ""
    if dir_letter == "GLOSSARY":
        candidate = ROOT / "appendices" / "glossary" / "index.html"
    else:
        # Find the directory: appendix-<dir_letter.lower()>-*
        d = None
        for cand in (ROOT / "appendices").glob(
            f"appendix-{dir_letter.lower()}-*"
        ):
            if cand.is_dir():
                d = cand
                break
        candidate = d / "index.html" if d else None
    if candidate is None or not candidate.exists():
        APPENDIX_TARGET_RENDER_CACHE[display_letter] = ""
        return ""
    try:
        soup = BeautifulSoup(candidate.read_text(encoding="utf-8", errors="replace"), "html.parser")
    except OSError:
        APPENDIX_TARGET_RENDER_CACHE[display_letter] = ""
        return ""
    # Look for the rendered title — h1 or breadcrumb / chapter-label
    for h1 in soup.find_all(["h1"]):
        t = h1.get_text(" ", strip=True)
        m = re.search(r"\bAppendix\s+([A-Z][A-Z]?)\b", t)
        if m:
            APPENDIX_TARGET_RENDER_CACHE[display_letter] = m.group(1)
            return m.group(1)
    # Fallback: <title> tag
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    m = re.search(r"\bAppendix\s+([A-Z][A-Z]?)\b", title)
    if m:
        APPENDIX_TARGET_RENDER_CACHE[display_letter] = m.group(1)
        return m.group(1)
    APPENDIX_TARGET_RENDER_CACHE[display_letter] = ""
    return ""


# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------


def scan_file(path: Path) -> dict:
    try:
        html_text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {"errors": []}
    soup = BeautifulSoup(html_text, "html.parser")
    body = strip_chrome(soup)
    prose = body.get_text(" ", strip=False)

    issues: list[dict] = []
    used_lines: dict[str, set[int]] = defaultdict(set)

    # Section refs
    for m in REF_PATTERNS[0][1].finditer(prose):
        label = m.group(1)
        if section_exists(label):
            continue
        # Search for the phrase in source for line attribution
        phrase = m.group(0)
        line = find_line_for_phrase(html_text, phrase, used_lines[phrase])
        issues.append({
            "category": "phantom" if not closest_section_candidates(label) else "drift",
            "kind": "section",
            "label": label,
            "phrase": phrase,
            "line": line,
            "candidates": closest_section_candidates(label),
        })

    # Figure refs
    for m in REF_PATTERNS[1][1].finditer(prose):
        label = m.group(1)
        if label in FIGURE_CAPTIONS:
            continue
        phrase = m.group(0)
        line = find_line_for_phrase(html_text, phrase, used_lines[phrase])
        cands = closest_caption_candidates(label, FIGURE_CAPTIONS)
        issues.append({
            "category": "drift" if cands else "phantom",
            "kind": "figure",
            "label": label,
            "phrase": phrase,
            "line": line,
            "candidates": cands,
        })

    # Code fragment refs
    for m in REF_PATTERNS[2][1].finditer(prose):
        label = m.group(1)
        if label in CODE_CAPTIONS:
            continue
        phrase = m.group(0)
        line = find_line_for_phrase(html_text, phrase, used_lines[phrase])
        cands = closest_caption_candidates(label, CODE_CAPTIONS)
        issues.append({
            "category": "drift" if cands else "phantom",
            "kind": "code_fragment",
            "label": label,
            "phrase": phrase,
            "line": line,
            "candidates": cands,
        })

    # Chapter refs
    for m in REF_PATTERNS[3][1].finditer(prose):
        try:
            num = int(m.group(1))
        except ValueError:
            continue
        # We treat chapters 0-42 as the valid range; outside that, ignore (likely a
        # numeric token in a list, not a real reference).
        if num < 0 or num > 42:
            continue
        if chapter_exists(num):
            continue
        phrase = m.group(0)
        line = find_line_for_phrase(html_text, phrase, used_lines[phrase])
        # Suggest nearest chapter
        cands: list[str] = []
        for delta in (-1, 1, -2, 2):
            if chapter_exists(num + delta):
                cands.append(f"Chapter {num + delta}")
        issues.append({
            "category": "drift" if cands else "phantom",
            "kind": "chapter",
            "label": str(num),
            "phrase": phrase,
            "line": line,
            "candidates": cands,
        })

    # Part refs
    for m in REF_PATTERNS[4][1].finditer(prose):
        roman = m.group(1)
        if part_exists(roman):
            continue
        phrase = m.group(0)
        line = find_line_for_phrase(html_text, phrase, used_lines[phrase])
        issues.append({
            "category": "phantom",
            "kind": "part",
            "label": roman,
            "phrase": phrase,
            "line": line,
            "candidates": [],
        })

    # Appendix refs
    for m in REF_PATTERNS[5][1].finditer(prose):
        letter = m.group(1)
        phrase = m.group(0)
        line = find_line_for_phrase(html_text, phrase, used_lines[phrase])
        if not appendix_display_exists(letter):
            issues.append({
                "category": "phantom",
                "kind": "appendix",
                "label": letter,
                "phrase": phrase,
                "line": line,
                "candidates": [],
            })
            continue
        # If exists, also check whether the target page renders as the same letter
        # (i.e. detect letter drift between prose and target h1).
        target = appendix_target_renders_as(letter)
        if target and target != letter:
            issues.append({
                "category": "letter-mismatch",
                "kind": "appendix",
                "label": letter,
                "phrase": phrase,
                "line": line,
                "candidates": [f"target renders as Appendix {target}"],
            })

    # Cross-reference href problems (only Section X.Y for now)
    xref = check_xref_hrefs(path)
    for x in xref:
        # Determine source line for the href
        sub = f'href="{x["href"]}"'
        line = find_line_for_phrase(html_text, sub, set()) or 0
        issues.append({
            "category": "cross-ref-broken",
            "kind": "section_href",
            "label": x["prose_label"],
            "phrase": f'<a href="{x["href"]}">…{x["anchor_text"]}…</a>',
            "line": line,
            "candidates": [f"href resolves to section-{x['href_label']}.html"],
        })

    return {"issues": issues}


# ---------------------------------------------------------------------------
# Duplicate / gap detection
# ---------------------------------------------------------------------------


def find_duplicates(inv: dict[str, list]) -> list[tuple[str, list[Path]]]:
    dupes = []
    for label, occs in inv.items():
        # Multiple distinct files bearing the same label = duplicate
        files = list({o[0] for o in occs})
        if len(files) > 1:
            dupes.append((label, sorted(files)))
    return sorted(dupes, key=lambda x: x[0])


def find_gaps(inv: dict[str, list]) -> list[tuple[str, list[int]]]:
    """Group labels by chapter.section prefix, then look for missing integers
    in the suffix sequence.

    Only consider 3-component labels (chapter.section.idx). Entries with
    suffixes like '30.5.L1' or '30.8.1a' use non-integer last components and
    are skipped — they don't participate in sequence counting.
    """
    by_prefix: dict[str, set[int]] = defaultdict(set)
    for label in inv.keys():
        parts = label.split(".")
        if len(parts) != 3:
            continue
        prefix = ".".join(parts[:-1])
        try:
            n = int(parts[-1])
        except ValueError:
            continue
        by_prefix[prefix].add(n)
    gaps: list[tuple[str, list[int]]] = []
    for prefix, nums in by_prefix.items():
        if not nums:
            continue
        lo = min(nums)
        hi = max(nums)
        # Only flag if there's a real range
        if hi - lo < 2:
            continue
        missing = sorted(set(range(lo, hi + 1)) - nums)
        if missing:
            gaps.append((prefix, missing))
    return sorted(gaps, key=lambda x: x[0])


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------


def relfmt(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_report(all_issues: dict[Path, list[dict]]) -> Path:
    out = ROOT / "numbering-audit.md"
    lines: list[str] = []

    # Counts
    counts = defaultdict(int)
    for issues in all_issues.values():
        for it in issues:
            counts[it["category"]] += 1
    dupe_figs = find_duplicates(FIGURE_CAPTIONS)
    dupe_codes = find_duplicates(CODE_CAPTIONS)
    gap_figs = find_gaps(FIGURE_CAPTIONS)
    gap_codes = find_gaps(CODE_CAPTIONS)

    lines.append("# Numbering Consistency Audit")
    lines.append("")
    total_files = len(iter_html_files())
    lines.append(f"Audit run: {total_files} content HTML pages scanned, "
                 f"{len(all_issues)} flagged with at least one issue. "
                 f"Section files: {sum(len(v) for v in SECTION_FILES.values())}. "
                 f"Figure captions: {sum(len(v) for v in FIGURE_CAPTIONS.values())}. "
                 f"Code-fragment captions: {sum(len(v) for v in CODE_CAPTIONS.values())}.")
    lines.append("")
    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Phantom references | {counts.get('phantom', 0)} |")
    lines.append(f"| Drift / off-by-one | {counts.get('drift', 0)} |")
    lines.append(f"| Letter mismatches (appendix) | {counts.get('letter-mismatch', 0)} |")
    lines.append(f"| Cross-ref href broken | {counts.get('cross-ref-broken', 0)} |")
    lines.append(f"| Duplicate figure labels | {len(dupe_figs)} |")
    lines.append(f"| Duplicate code-fragment labels | {len(dupe_codes)} |")
    lines.append(f"| Gaps in figure sequences | {len(gap_figs)} |")
    lines.append(f"| Gaps in code-fragment sequences | {len(gap_codes)} |")
    lines.append("")

    # 2. Phantom references
    lines.append("## 2. Phantom references")
    lines.append("")
    lines.append("Prose cites a number that does not exist anywhere in the book.")
    lines.append("")
    phantoms: list[tuple[Path, dict]] = []
    for f, issues in all_issues.items():
        for it in issues:
            if it["category"] == "phantom":
                phantoms.append((f, it))
    if not phantoms:
        lines.append("_None found._")
    else:
        lines.append("| File:Line | Kind | Cited as | Nearest existing |")
        lines.append("|---|---|---|---|")
        for f, it in sorted(phantoms, key=lambda x: (relfmt(x[0]), x[1].get("line", 0))):
            cands = ", ".join(it["candidates"]) if it["candidates"] else "(none)"
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | {it['kind']} | "
                f"`{it['phrase']}` | {cands} |"
            )
    lines.append("")

    # 3. Drift / off-by-one
    lines.append("## 3. Drift / off-by-one")
    lines.append("")
    lines.append("Prose cites X.Y but only X.(Y-1) or X.(Y+1) exists. Likely a renumbering miss.")
    lines.append("")
    drifts: list[tuple[Path, dict]] = []
    for f, issues in all_issues.items():
        for it in issues:
            if it["category"] == "drift":
                drifts.append((f, it))
    if not drifts:
        lines.append("_None found._")
    else:
        lines.append("| File:Line | Kind | Cited as | Likely intended |")
        lines.append("|---|---|---|---|")
        for f, it in sorted(drifts, key=lambda x: (relfmt(x[0]), x[1].get("line", 0))):
            cands = ", ".join(it["candidates"]) if it["candidates"] else "(none)"
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | {it['kind']} | "
                f"`{it['phrase']}` | {cands} |"
            )
    lines.append("")

    # 4. Duplicate labels
    lines.append("## 4. Duplicate labels")
    lines.append("")
    lines.append("Same caption label appears on two or more pages.")
    lines.append("")
    if dupe_figs:
        lines.append("### 4a. Figures")
        lines.append("")
        lines.append("| Label | Files |")
        lines.append("|---|---|")
        for label, files in dupe_figs:
            files_str = "<br>".join(f"`{relfmt(p)}`" for p in files)
            lines.append(f"| Figure {label} | {files_str} |")
        lines.append("")
    else:
        lines.append("### 4a. Figures")
        lines.append("")
        lines.append("_None found._")
        lines.append("")
    if dupe_codes:
        lines.append("### 4b. Code Fragments")
        lines.append("")
        lines.append("| Label | Files |")
        lines.append("|---|---|")
        for label, files in dupe_codes:
            files_str = "<br>".join(f"`{relfmt(p)}`" for p in files)
            lines.append(f"| Code Fragment {label} | {files_str} |")
        lines.append("")
    else:
        lines.append("### 4b. Code Fragments")
        lines.append("")
        lines.append("_None found._")
        lines.append("")

    # 5. Gaps
    lines.append("## 5. Gaps in numbered sequences")
    lines.append("")
    lines.append("A chapter has captions 1, 2, 4 but not 3.")
    lines.append("")
    lines.append("### 5a. Figures")
    lines.append("")
    if gap_figs:
        lines.append("| Prefix | Missing |")
        lines.append("|---|---|")
        for prefix, missing in gap_figs:
            lines.append(f"| Figure {prefix}.* | {', '.join(str(m) for m in missing)} |")
    else:
        lines.append("_None found._")
    lines.append("")
    lines.append("### 5b. Code Fragments")
    lines.append("")
    if gap_codes:
        lines.append("| Prefix | Missing |")
        lines.append("|---|---|")
        for prefix, missing in gap_codes:
            lines.append(f"| Code Fragment {prefix}.* | {', '.join(str(m) for m in missing)} |")
    else:
        lines.append("_None found._")
    lines.append("")

    # 6. Letter mismatches
    lines.append("## 6. Letter mismatches (Appendix)")
    lines.append("")
    lines.append("Prose says 'Appendix AD' but the target page's h1 renders differently.")
    lines.append("")
    letter_misses: list[tuple[Path, dict]] = []
    for f, issues in all_issues.items():
        for it in issues:
            if it["category"] == "letter-mismatch":
                letter_misses.append((f, it))
    if not letter_misses:
        lines.append("_None found._")
    else:
        lines.append("| File:Line | Prose says | Target renders as |")
        lines.append("|---|---|---|")
        for f, it in sorted(letter_misses, key=lambda x: (relfmt(x[0]), x[1].get("line", 0))):
            target = it["candidates"][0] if it["candidates"] else "(unknown)"
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | `Appendix {it['label']}` | {target} |"
            )
    lines.append("")

    # 7. Cross-ref href broken
    lines.append("## 7. Cross-reference href broken")
    lines.append("")
    lines.append("An `<a href>` whose anchor text claims one section number but the href points to a different one.")
    lines.append("")
    xrefs: list[tuple[Path, dict]] = []
    for f, issues in all_issues.items():
        for it in issues:
            if it["category"] == "cross-ref-broken":
                xrefs.append((f, it))
    if not xrefs:
        lines.append("_None found._")
    else:
        lines.append("| File:Line | Anchor says | Href resolves to |")
        lines.append("|---|---|---|")
        for f, it in sorted(xrefs, key=lambda x: (relfmt(x[0]), x[1].get("line", 0))):
            target = it["candidates"][0] if it["candidates"] else "(unknown)"
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | `Section {it['label']}` | {target} |"
            )
    lines.append("")

    # 8. Recommended fix priority
    lines.append("## 8. Recommended fix priority")
    lines.append("")
    # Pick top categories by count, surface representative examples
    priority_bullets: list[str] = []
    if counts.get("drift", 0) > 0:
        priority_bullets.append(
            f"**Drift / off-by-one ({counts['drift']} cases)**: highest yield. "
            "Each is a one-token edit in prose to match an adjacent caption number. "
            "Likely all from the same renumber pass."
        )
    if dupe_figs:
        priority_bullets.append(
            f"**Duplicate figure labels ({len(dupe_figs)} cases)**: two pages claim the same Figure X.Y.Z. "
            "Renumber the later occurrence."
        )
    if dupe_codes:
        priority_bullets.append(
            f"**Duplicate code-fragment labels ({len(dupe_codes)} cases)**: same problem as figures."
        )
    if counts.get("phantom", 0) > 0:
        priority_bullets.append(
            f"**Phantom references ({counts['phantom']} cases)**: prose cites a number that does not exist. "
            "Either the target was deleted or never created; decide per case."
        )
    if gap_figs or gap_codes:
        priority_bullets.append(
            f"**Sequence gaps ({len(gap_figs)} figure, {len(gap_codes)} code)**: a missing number in a chapter's sequence. "
            "Either a caption was deleted without renumbering, or a number was skipped intentionally."
        )
    if counts.get("letter-mismatch", 0) > 0:
        priority_bullets.append(
            f"**Appendix letter mismatches ({counts['letter-mismatch']} cases)**: book-wide letter drift. "
            "Do NOT fix piecemeal; this needs a coordinated pass."
        )
    if counts.get("cross-ref-broken", 0) > 0:
        priority_bullets.append(
            f"**Cross-ref href mismatches ({counts['cross-ref-broken']} cases)**: anchor text and href disagree. "
            "Either the anchor text is stale or the href is stale; the more recently edited side is usually correct."
        )
    if not priority_bullets:
        priority_bullets.append("No issues found. Run again after any structural change.")
    for b in priority_bullets:
        lines.append(f"- {b}")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------


def main() -> int:
    sys.stderr.write("Building inventories...\n")
    build_directory_inventory()
    build_appendix_letter_map()
    build_caption_inventory()
    sys.stderr.write(
        f"  sections: {len(SECTION_FILES)}, "
        f"chapters: {len(CHAPTER_DIRS)}, "
        f"parts: {len(PART_DIRS)}, "
        f"appendices: {len(APPENDIX_DISPLAY_TO_DIR)}, "
        f"figures: {len(FIGURE_CAPTIONS)}, "
        f"code fragments: {len(CODE_CAPTIONS)}\n"
    )
    sys.stderr.write("Scanning files...\n")
    all_files = iter_html_files()
    all_issues: dict[Path, list[dict]] = {}
    for i, path in enumerate(all_files):
        if i % 50 == 0:
            sys.stderr.write(f"  {i}/{len(all_files)}\n")
        result = scan_file(path)
        if result.get("issues"):
            all_issues[path] = result["issues"]
    sys.stderr.write(f"Writing report...\n")
    out = write_report(all_issues)
    sys.stderr.write(f"Wrote {out}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
