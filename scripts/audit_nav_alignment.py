"""Audit navigation surface alignment with current section structure.

After the v2.0 a/b split-section renumbering, this one-off script verifies that
four navigation surfaces match the on-disk structure:

  1. toc.html (root)                            -- top-level book TOC
  2. appendices/appendix-b-course-syllabi/      -- syllabus references
  3. appendices/appendix-c-reading-pathways/    -- pathway references
  4. front-matter/*.html                        -- foreword, fm-*, look-inside,
                                                  about-authors, copyright

Checks (per task spec, Method A-D):

  A. Stale a/b refs (section-X.Ya.html / X.Yb / "Section X.Ya" / X.Yb labels)
  A'. Stale section numbers (href to a section that should have shifted)
  A''.Stale subsection refs ("Section X.Y.Z")
  B. Stale chapter/part counts (e.g. "Sixteen parts", "83 chapters")
  C. Broken internal hrefs (every <a href=> target exists on disk)
  D. Section title wording matches the target's <title>/<h1>

Usage:
    /c/Python314/python scripts/audit_nav_alignment.py
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag, urlparse

ROOT = Path(__file__).resolve().parent.parent

# -------- The on-disk truth ----------------------------------------------

# Live, canonical parts (in display order): folder name keyed by part number.
PARTS = {
    1:  "part-1-llm-building-blocks",
    2:  "part-2-understanding-llms",
    3:  "part-3-working-with-llms",
    4:  "part-4-training-adaptation",
    5:  "part-5-multimodal-llms",
    6:  "part-6-agentic-ai",
    7:  "part-7-retrieval-information-extraction-with-llms",
    8:  "part-8-conversational-ai-with-llms",
    9:  "part-9-llm-evaluation-observability",
    10: "part-10-llm-security-runtime-safety",
    11: "part-11-llm-ethics-trust-governance",
    12: "part-12-llm-systems-at-scale",
    13: "part-13-llmops-lifecycle",
    14: "part-14-applications-of-llms-across-industries",
    15: "part-15-llm-agentic-ai-research-frontiers",
}

# Roman numeral for each part
ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
    8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII", 13: "XIII",
    14: "XIV", 15: "XV",
}

NAV_SURFACES: list[Path] = [
    ROOT / "toc.html",
    ROOT / "appendices" / "appendix-b-course-syllabi" / "index.html",
    ROOT / "appendices" / "appendix-c-reading-pathways" / "index.html",
    ROOT / "front-matter" / "foreword.html",
    ROOT / "front-matter" / "fm-what-this-book-covers.html",
    ROOT / "front-matter" / "fm-who-should-read.html",
    ROOT / "front-matter" / "fm-how-to-use.html",
    ROOT / "front-matter" / "look-inside-preview.html",
    ROOT / "front-matter" / "about-authors.html",
    ROOT / "front-matter" / "copyright.html",
]


# -------- HTML parsing helpers -------------------------------------------

class _HrefCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[tuple[str, int]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for k, v in attrs:
            if k.lower() == "href" and v:
                self.hrefs.append((v, self.getpos()[0]))
                break


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.in_title = False
        self.in_h1 = False
        self.title = ""
        self.h1 = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True
        elif tag.lower() == "h1":
            self.in_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False
        elif tag.lower() == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self.in_h1:
            self.h1 += data
        self.parts.append(data)


def extract_hrefs(html: str) -> list[tuple[str, int]]:
    p = _HrefCollector()
    p.feed(html)
    return p.hrefs


def page_title(html: str) -> tuple[str, str, str]:
    p = _TextExtractor()
    p.feed(html)
    return p.title.strip(), p.h1.strip(), " ".join(p.parts)


# -------- Disk structure scan --------------------------------------------

def build_section_index() -> dict[tuple[int, int, int], Path]:
    """Map (part, chapter, section) -> absolute Path to section html."""
    index: dict[tuple[int, int, int], Path] = {}
    for part_num, folder in PARTS.items():
        part_dir = ROOT / folder
        if not part_dir.is_dir():
            continue
        for module_dir in sorted(part_dir.glob("module-*/")):
            mname = module_dir.name
            # module-NN-... or module-NNx-...
            m = re.match(r"module-(\d+)([a-z]?)-", mname)
            if not m:
                continue
            chap = int(m.group(1))
            for sect in sorted(module_dir.glob("section-*.html")):
                sm = re.match(r"section-(\d+)\.(\d+)\.html", sect.name)
                if not sm:
                    continue
                ch, snum = int(sm.group(1)), int(sm.group(2))
                index[(part_num, ch, snum)] = sect.resolve()
    return index


def part_for_chapter(chap: int) -> int | None:
    """Return part number containing the given chapter, or None."""
    for part_num, folder in PARTS.items():
        part_dir = ROOT / folder
        for module_dir in part_dir.glob("module-*/"):
            m = re.match(r"module-(\d+)([a-z]?)-", module_dir.name)
            if m and int(m.group(1)) == chap:
                return part_num
    return None


def section_count_per_part() -> dict[int, int]:
    counts: dict[int, int] = {}
    for part_num, folder in PARTS.items():
        n = 0
        for f in (ROOT / folder).rglob("section-*.html"):
            if "_archive" in f.parts:
                continue
            n += 1
        counts[part_num] = n
    return counts


def chapter_count_per_part() -> dict[int, int]:
    counts: dict[int, int] = {}
    for part_num, folder in PARTS.items():
        n = sum(1 for _ in (ROOT / folder).glob("module-*/"))
        counts[part_num] = n
    return counts


# -------- Check implementations ------------------------------------------

class Finding:
    __slots__ = ("file", "line", "kind", "msg")

    def __init__(self, file: Path, line: int, kind: str, msg: str) -> None:
        self.file = file
        self.line = line
        self.kind = kind
        self.msg = msg

    def __str__(self) -> str:
        rel = self.file.relative_to(ROOT) if self.file.is_absolute() else self.file
        return f"  [{self.kind}] {rel}:{self.line}: {self.msg}"


# Pattern A: stale a/b refs
_AB_PATTERNS = [
    re.compile(r"section-(\d+)\.(\d+)([ab])\.html", re.IGNORECASE),
    re.compile(r"\bSection\s+(\d+)\.(\d+)([ab])\b"),
    re.compile(r"\b(\d+)\.(\d+)([ab])\b"),  # bare like "5.2a"
]


def check_stale_ab(file: Path, html: str, findings: list[Finding]) -> None:
    for line_idx, line in enumerate(html.splitlines(), start=1):
        for pat in _AB_PATTERNS:
            for m in pat.finditer(line):
                # Avoid matching CSS hex like #a1b2c3 or random a/b that
                # do not look like section labels. Limit to leading 1-2 digit
                # chapter and 1-3 digit section.
                ch, sn, suf = m.group(1), m.group(2), m.group(3)
                if 0 <= int(ch) <= 99 and 1 <= int(sn) <= 999:
                    findings.append(Finding(
                        file, line_idx, "STALE_AB",
                        f"references {m.group(0)} (a/b split sections were renumbered)",
                    ))


# Pattern C: broken hrefs
def check_broken_hrefs(file: Path, html: str, findings: list[Finding]) -> None:
    base = file.parent
    for href, line in extract_hrefs(html):
        url, _ = urldefrag(href)
        if not url:
            continue
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https", "mailto", "tel", "javascript"):
            continue
        if parsed.scheme:  # any other scheme
            continue
        target = (base / url).resolve()
        if not target.exists():
            try:
                rel = target.relative_to(ROOT)
            except ValueError:
                rel = target
            findings.append(Finding(
                file, line, "BROKEN_HREF",
                f"href={href!r} -> {rel} does not exist",
            ))


# Pattern A''': inline "Chapter N (something)" or "Section N.M (something)" prose
# refs where the disk truth doesn't match the chapter number.
_CHAP_PROSE_PAT = re.compile(r"\bChapter\s+(\d+)\b")
_SECT_PROSE_PAT = re.compile(r"\bSection\s+(\d+)\.(\d+)\b")
_SECT_HREF_PAT = re.compile(r"section-(\d+)\.(\d+)\.html")


def check_unlinked_chapter_ref(file: Path, html: str, findings: list[Finding]) -> None:
    """For prose like 'Chapter N (description)' that is NOT wrapped in an <a href>,
    check that chapter N still exists on disk."""
    # We need to find prose chapter refs without href attribute on the immediate parent.
    # Heuristic: look at each line and exclude lines that look like an <a> tag opening
    # at the chapter ref position.
    valid_chapters: set[int] = set()
    for part_num, folder in PARTS.items():
        for module_dir in (ROOT / folder).glob("module-*/"):
            m = re.match(r"module-(\d+)([a-z]?)-", module_dir.name)
            if m:
                valid_chapters.add(int(m.group(1)))
    for line_idx, line in enumerate(html.splitlines(), start=1):
        for m in _CHAP_PROSE_PAT.finditer(line):
            n = int(m.group(1))
            # Skip if it's clearly inside an href or aria-label
            window_start = max(0, m.start() - 50)
            window = line[window_start:m.end()]
            if 'href=' in window and '"' in window[window.rfind('href='):]:
                continue
            if 'aria-label' in window:
                continue
            if n not in valid_chapters:
                findings.append(Finding(
                    file, line_idx, "STALE_CHAPTER_PROSE_REF",
                    f"prose says 'Chapter {n}' but no module-{n:02d} exists on disk",
                ))


# Pattern A': link to section file whose chapter number doesn't match the part
def check_section_chapter_in_part(file: Path, html: str, findings: list[Finding]) -> None:
    """Catch e.g. a link in part-X-foo/.../section-Y.Z.html where chapter Y
    actually lives in a different part folder."""
    base = file.parent
    section_pat = re.compile(
        r"(?:^|[\"'/])(part-\d+[\w-]*)/(?:module-(\d+)[\w-]*/)?section-(\d+)\.(\d+)\.html"
    )
    for href, line in extract_hrefs(html):
        url, _ = urldefrag(href)
        m = section_pat.search(url)
        if not m:
            continue
        part_folder = m.group(1)
        mod_chap = int(m.group(2)) if m.group(2) else None
        ch = int(m.group(3))
        # Find part number from part_folder
        part_num = None
        for pn, pf in PARTS.items():
            if pf == part_folder:
                part_num = pn
                break
        if part_num is None:
            continue
        # Find the actual part containing chapter ch on disk
        actual_part = part_for_chapter(ch)
        if actual_part is None:
            continue
        if actual_part != part_num:
            findings.append(Finding(
                file, line, "WRONG_PART_FOR_CHAPTER",
                f"href {url!r} puts chapter {ch} in {part_folder} but disk says it's in {PARTS[actual_part]}",
            ))


# Pattern B: stale aggregate counts in front matter
def check_aggregate_counts(file: Path, html: str, findings: list[Finding],
                            sections_total: int, chapters_total: int) -> None:
    text = html
    # "Sixteen parts" / "fifteen parts" patterns
    patterns_parts_word = [
        (re.compile(r"\bsixteen parts\b", re.IGNORECASE), 16),
        (re.compile(r"\bfifteen parts\b", re.IGNORECASE), 15),
        (re.compile(r"\bfourteen parts\b", re.IGNORECASE), 14),
    ]
    for pat, claimed in patterns_parts_word:
        for m in pat.finditer(text):
            if claimed != 15:
                line_idx = text[: m.start()].count("\n") + 1
                findings.append(Finding(
                    file, line_idx, "STALE_PART_COUNT_WORD",
                    f"says '{m.group(0)}' but book has 15 parts",
                ))
    patterns_chapters = [
        re.compile(r"(\d+)\s+chapters?\s+across\s+(\w+)\s+parts", re.IGNORECASE),
        re.compile(r"\b(\d+)\s+chapters?\b", re.IGNORECASE),
    ]
    for pat in patterns_chapters[:1]:
        for m in pat.finditer(text):
            claimed_chaps = int(m.group(1))
            claimed_parts_word = m.group(2).lower()
            word_to_int = {
                "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
                "fourteen": 14, "fifteen": 15, "sixteen": 16,
            }
            claimed_parts = word_to_int.get(claimed_parts_word, 0)
            line_idx = text[: m.start()].count("\n") + 1
            if claimed_chaps != chapters_total or claimed_parts != 15:
                findings.append(Finding(
                    file, line_idx, "STALE_AGGREGATE_COUNT",
                    f"says '{m.group(0)}' but disk has {chapters_total} chapters across 15 parts",
                ))


# Pattern D: section title mismatch in TOC chapter entries
def check_chapter_title_wording(file: Path, html: str, findings: list[Finding]) -> None:
    """For toc.html, check that each <a href="...module-NN-foo/index.html"> entry's
    visible <span class="toc-chapter-title"> matches the on-disk <title>'s
    chapter title."""
    if file.name != "toc.html":
        return
    base = file.parent
    # Find toc-chapter list items: <a href="..."> ... <span class="toc-chapter-num">N</span> <span class="toc-chapter-title">TITLE</span>
    item_pat = re.compile(
        r'<a\s+href="([^"]+module-(\d+)[\w-]*/index\.html)"[^>]*>\s*'
        r'<span\s+class="toc-chapter-num"[^>]*>([^<]+)</span>\s*'
        r'<span\s+class="toc-chapter-title">([^<]+)</span>',
        re.DOTALL,
    )
    for m in item_pat.finditer(html):
        href = m.group(1)
        disk_chap = int(m.group(2))
        visible_num = m.group(3).strip()
        visible_title = m.group(4).strip()
        # Replace HTML entities
        visible_title_norm = (
            visible_title.replace("&amp;", "&")
            .replace("&nbsp;", " ")
            .replace("&#39;", "'")
        )
        # Find the target file and read its <title>
        target = (base / href).resolve()
        line_idx = html[: m.start()].count("\n") + 1
        if not target.exists():
            continue  # broken_hrefs will catch this
        try:
            tgt_html = target.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # The chapter <title> is like "Chapter NN: TITLE | Book"
        tm = re.search(r"<title>\s*Chapter\s+(\d+)\s*:\s*([^|<]+?)(?:\s*\|.*?)?</title>", tgt_html)
        if not tm:
            continue
        disk_num = int(tm.group(1))
        disk_title = tm.group(2).strip().replace("&amp;", "&")

        # Visible number must equal disk chapter number
        if visible_num != str(disk_num):
            findings.append(Finding(
                file, line_idx, "TOC_VISIBLE_NUM_MISMATCH",
                f"href={href} chapter on disk is {disk_num} but visible label is '{visible_num}'",
            ))

        # Visible title should match disk title (loose comparison)
        if visible_title_norm.replace("\n", " ").strip() != disk_title.replace("\n", " ").strip():
            # Allow tiny variations (e.g. "&" vs "and"); only flag if substantially different
            if not titles_equivalent(visible_title_norm, disk_title):
                findings.append(Finding(
                    file, line_idx, "TOC_TITLE_MISMATCH",
                    f"href={href}: visible title '{visible_title_norm}' vs disk title '{disk_title}'",
                ))


def titles_equivalent(a: str, b: str) -> bool:
    """Loose title comparison ignoring whitespace, case, &/and."""
    def norm(s: str) -> str:
        s = s.lower().replace("&", "and")
        s = re.sub(r"\s+", " ", s).strip()
        return s
    return norm(a) == norm(b)


# Stale chapter/section counts on TOC part headers
# The separator can be either the HTML entity &middot; or a literal middle-dot.
TOC_PART_COUNT_PAT = re.compile(
    r'<section[^>]*id="part-(\d+)"[^>]*data-part-num="(\d+)"[\s\S]*?'
    r'<span class="toc-part-count">(\d+)\s+chapters?\s*(?:&middot;|·)\s*(\d+)\s+sections?</span>'
)


def check_toc_part_counts(file: Path, html: str, findings: list[Finding],
                          chap_per_part: dict[int, int],
                          sect_per_part: dict[int, int]) -> None:
    if file.name != "toc.html":
        return
    for m in TOC_PART_COUNT_PAT.finditer(html):
        part_id = int(m.group(1))
        part_data_num = int(m.group(2))
        claimed_chaps = int(m.group(3))
        claimed_sects = int(m.group(4))
        line_idx = html[: m.start()].count("\n") + 1
        # data-part-num should equal part_id (canonical 1..15)
        if part_data_num != part_id:
            findings.append(Finding(
                file, line_idx, "TOC_PART_DATA_NUM_MISMATCH",
                f"part-{part_id} has data-part-num={part_data_num}; should be {part_id}",
            ))
        # Chapter and section counts must match disk
        disk_chaps = chap_per_part.get(part_id, 0)
        disk_sects = sect_per_part.get(part_id, 0)
        if claimed_chaps != disk_chaps:
            findings.append(Finding(
                file, line_idx, "TOC_PART_CHAP_COUNT",
                f"part-{part_id}: claims {claimed_chaps} chapters, disk has {disk_chaps}",
            ))
        if claimed_sects != disk_sects:
            findings.append(Finding(
                file, line_idx, "TOC_PART_SECT_COUNT",
                f"part-{part_id}: claims {claimed_sects} sections, disk has {disk_sects}",
            ))


def check_toc_part_roman(file: Path, html: str, findings: list[Finding]) -> None:
    """Verify Part roman numeral matches the part id."""
    if file.name != "toc.html":
        return
    pat = re.compile(
        r'<section[^>]*id="part-(\d+)"[^>]*>[\s\S]*?'
        r'<span\s+class="toc-part-prefix">Part\s+([IVX]+)</span>'
    )
    for m in pat.finditer(html):
        pid = int(m.group(1))
        roman = m.group(2)
        line_idx = html[: m.start()].count("\n") + 1
        expected = ROMAN.get(pid)
        if expected and roman != expected:
            findings.append(Finding(
                file, line_idx, "TOC_PART_ROMAN_MISMATCH",
                f"part-{pid}: shows 'Part {roman}'; expected 'Part {expected}'",
            ))


# -------- Driver ----------------------------------------------------------

def audit() -> tuple[list[Finding], dict[int, int], dict[int, int]]:
    findings: list[Finding] = []
    chap_per_part = chapter_count_per_part()
    sect_per_part = section_count_per_part()
    total_chapters = sum(chap_per_part.values())
    total_sections = sum(sect_per_part.values())

    for surface in NAV_SURFACES:
        if not surface.exists():
            findings.append(Finding(surface, 0, "MISSING_FILE",
                                    "nav surface file does not exist"))
            continue
        html = surface.read_text(encoding="utf-8", errors="replace")
        check_stale_ab(surface, html, findings)
        check_broken_hrefs(surface, html, findings)
        check_section_chapter_in_part(surface, html, findings)
        check_unlinked_chapter_ref(surface, html, findings)
        check_aggregate_counts(surface, html, findings,
                                total_sections, total_chapters)
        check_chapter_title_wording(surface, html, findings)
        check_toc_part_counts(surface, html, findings, chap_per_part, sect_per_part)
        check_toc_part_roman(surface, html, findings)

    return findings, chap_per_part, sect_per_part


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="only print summary")
    args = parser.parse_args()

    findings, chap_per_part, sect_per_part = audit()

    if not args.quiet:
        print("=" * 78)
        print("Disk truth")
        print("=" * 78)
        total_chap = total_sect = 0
        for pn in sorted(PARTS):
            c = chap_per_part[pn]
            s = sect_per_part[pn]
            total_chap += c
            total_sect += s
            print(f"  Part {pn:>2} ({ROMAN[pn]:>4}) {PARTS[pn]:<60} {c:>3} ch  {s:>3} sect")
        print(f"  {'TOTAL':<73} {total_chap:>3} ch  {total_sect:>3} sect")
        print(f"  Parts: {len(PARTS)}")
        print()

    if not findings:
        print("0 findings. Navigation surfaces are aligned.")
        return 0

    # Group by file
    by_file: dict[Path, list[Finding]] = defaultdict(list)
    for f in findings:
        by_file[f.file].append(f)

    kinds: dict[str, int] = defaultdict(int)
    for f in findings:
        kinds[f.kind] += 1

    print("=" * 78)
    print(f"FINDINGS: {len(findings)}  ({len(by_file)} files affected)")
    print("=" * 78)
    for kind, n in sorted(kinds.items(), key=lambda x: -x[1]):
        print(f"  {kind:<35} {n:>4}")
    print()

    for file in sorted(by_file):
        print(f"--- {file.relative_to(ROOT) if file.is_absolute() else file} "
              f"({len(by_file[file])} findings)")
        for f in by_file[file]:
            print(str(f))
        print()

    return 1


if __name__ == "__main__":
    sys.exit(main())
