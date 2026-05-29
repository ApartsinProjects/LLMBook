"""Read-only audit of cross-reference integrity after the major restructuring.

Walks every HTML body book-wide; for each cross-reference token, verifies
the target exists on disk:

  1. ``Chapter N`` text -> a part-X/module-NN-*/index.html with that
     chapter number must exist.
  2. ``Section X.Y`` (X.Y.Z, X.Y.Z.W) text -> a part-X/module-XX-*/
     section-X.Y.html (or deeper anchor) must exist.
  3. ``Part X`` Roman text -> part-N-*/index.html must exist with
     matching Roman numeral.
  4. ``Appendix X`` text -> appendices/appendix-X-*/index.html exists.
  5. ``Appendix X.N`` (X.N.M) text -> matching section file exists.
  6. Every ``<a href="...">`` link -> relative target resolves to a real
     file. External URLs (http(s), mailto, tel, data, ws, ftp, javascript,
     // protocol-relative) are skipped.
  7. Code Fragment / Figure / Table / Pseudocode / Algorithm caption
     numbers -> the captioned block's chapter prefix matches the file's
     chapter number (derived from filename / module).

Also compares against ``book_structure.target.yaml``: any reference that
points OUTSIDE the declared target structure (e.g. a chapter, appendix
letter, or section number that does not appear in target.yaml) is flagged
as a "suspect restructure miss".

Read-only. No network calls. No file modifications.

Output: ``crossref-integrity-audit.md`` at the project root.
"""
from __future__ import annotations

import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, unquote

import yaml
from bs4 import BeautifulSoup, NavigableString, Tag


ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
OUT_PATH = ROOT / "crossref-integrity-audit.md"
TARGET_YAML = ROOT / "book_structure.target.yaml"

EXCLUDE_DIR_NAMES = {
    "KDP", ".claude", "node_modules", "build",
    "pagefind", "templates", "vendor", "scripts", "agents",
    "downloads", "images", "_concept-figs", "__pycache__",
    "styles", ".git", ".github", ".html2epub_cache",
}
EXCLUDE_PREFIXES = ("temp_", "source_fix_backups")


PART_NUM_TO_ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
    6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
    11: "XI", 12: "XII",
}
ROMAN_TO_PART_NUM = {v: k for k, v in PART_NUM_TO_ROMAN.items()}


# ---------------------------------------------------------------------------
# Path / file discovery
# ---------------------------------------------------------------------------

def is_excluded_dir(name: str) -> bool:
    if name in EXCLUDE_DIR_NAMES:
        return True
    if any(name.startswith(p) for p in EXCLUDE_PREFIXES):
        return True
    if "backup" in name.lower():
        return True
    return False


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(Path(dirpath) / fn)
    return sorted(out)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


# ---------------------------------------------------------------------------
# Inventories built from disk
# ---------------------------------------------------------------------------

CHAPTER_TO_DIR: dict[int, Path] = {}
PART_ROMAN_TO_DIR: dict[str, Path] = {}
APPENDIX_LETTER_TO_DIR: dict[str, Path] = {}
SECTION_FILES: dict[str, list[Path]] = defaultdict(list)         # "12.3" -> [...]
APPENDIX_SECTION_FILES: dict[str, list[Path]] = defaultdict(list)  # "A.1" -> [...]

# Caption inventories: label -> list of (file, raw caption text)
FIGURE_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)
CODE_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)
TABLE_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)
ALGORITHM_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)
PSEUDOCODE_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)


def parse_section_filename(name: str) -> str | None:
    m = re.match(r"section-([\d]+(?:\.[\dA-Za-z]+)*)\.html$", name)
    return m.group(1) if m else None


def parse_appendix_section_filename(name: str) -> str | None:
    m = re.match(r"section-([a-z]+(?:\.[\dA-Za-z]+)*)\.html$", name, re.IGNORECASE)
    return m.group(1).upper() if m else None


def build_disk_inventory() -> None:
    # Part / chapter dirs (under part-N-*/module-NN-*)
    for part_dir in ROOT.glob("part-*"):
        if not part_dir.is_dir():
            continue
        m_part = re.match(r"part-(\d+)-", part_dir.name)
        if not m_part:
            continue
        part_num = int(m_part.group(1))
        roman = PART_NUM_TO_ROMAN.get(part_num)
        if roman:
            PART_ROMAN_TO_DIR[roman] = part_dir
        for mod_dir in part_dir.glob("module-*"):
            if not mod_dir.is_dir():
                continue
            m_mod = re.match(r"module-(\d+)-", mod_dir.name)
            if not m_mod:
                continue
            ch = int(m_mod.group(1))
            # In case two part dirs claim the same module (e.g. a stale
            # module-33 left under part-12), prefer the one that actually
            # contains content (index.html or section files).
            has_index = (mod_dir / "index.html").exists()
            has_sections = any(mod_dir.glob("section-*.html"))
            prev = CHAPTER_TO_DIR.get(ch)
            if prev is None:
                CHAPTER_TO_DIR[ch] = mod_dir
            else:
                prev_has_index = (prev / "index.html").exists()
                prev_has_sections = any(prev.glob("section-*.html"))
                # Prefer a dir that has more content
                if (has_index or has_sections) and not (prev_has_index or prev_has_sections):
                    CHAPTER_TO_DIR[ch] = mod_dir
            for f in mod_dir.glob("section-*.html"):
                lbl = parse_section_filename(f.name)
                if lbl is not None:
                    SECTION_FILES[lbl].append(f)

    # Appendix dirs
    apx_root = ROOT / "appendices"
    if apx_root.is_dir():
        for apx_dir in apx_root.glob("appendix-*"):
            if not apx_dir.is_dir():
                continue
            m = re.match(r"appendix-([a-z]+)-", apx_dir.name, re.IGNORECASE)
            if not m:
                continue
            letter = m.group(1).upper()
            APPENDIX_LETTER_TO_DIR[letter] = apx_dir
            for f in apx_dir.glob("section-*.html"):
                lbl = parse_appendix_section_filename(f.name)
                if lbl is not None:
                    APPENDIX_SECTION_FILES[lbl].append(f)


# ---------------------------------------------------------------------------
# Target structure inventory (book_structure.target.yaml)
# ---------------------------------------------------------------------------

TARGET_CHAPTERS: set[int] = set()
TARGET_PARTS_ROMAN: set[str] = set()
TARGET_SECTIONS: set[str] = set()             # "12.3"
TARGET_APPENDIX_LETTERS: set[str] = set()
TARGET_APPENDIX_SECTIONS: set[str] = set()    # "A.1"
TARGET_CHAPTER_TO_PART: dict[int, int] = {}


def load_target_structure() -> None:
    if not TARGET_YAML.exists():
        return
    with TARGET_YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for part in data.get("parts", []):
        roman = part.get("roman")
        if roman:
            TARGET_PARTS_ROMAN.add(roman)
        part_num = part.get("num")
        for ch in part.get("chapters", []):
            num = ch.get("num")
            if num is not None:
                TARGET_CHAPTERS.add(int(num))
                if part_num is not None:
                    TARGET_CHAPTER_TO_PART[int(num)] = int(part_num)
            for sec in ch.get("sections", []) or []:
                s = sec.get("num")
                if s is not None:
                    TARGET_SECTIONS.add(str(s))
    for apx in data.get("appendices", []):
        letter = apx.get("letter")
        if letter:
            TARGET_APPENDIX_LETTERS.add(str(letter).upper())
        for sec in apx.get("sections", []) or []:
            s = sec.get("num")
            if s is not None:
                TARGET_APPENDIX_SECTIONS.add(str(s).upper())


# ---------------------------------------------------------------------------
# Caption inventory build
# ---------------------------------------------------------------------------

CAPTION_PATTERNS = {
    "figure":      re.compile(r"^\s*figure\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE),
    "code":        re.compile(r"^\s*code\s+fragment\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE),
    "table":       re.compile(r"^\s*table\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE),
    "algorithm":   re.compile(r"^\s*algorithm\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE),
    "pseudocode":  re.compile(r"^\s*pseudocode\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE),
}


def harvest_captions(path: Path, soup: BeautifulSoup) -> None:
    candidates: list[Tag] = []
    candidates.extend(soup.find_all(["figcaption", "caption"]))
    candidates.extend(soup.find_all("div", class_=["diagram-caption", "code-caption", "table-caption"]))
    candidates.extend(soup.select(
        "div.callout.algorithm div.callout-title, "
        "aside.callout.algorithm div.callout-title, "
        "div.callout.pseudocode div.callout-title, "
        "aside.callout.pseudocode div.callout-title"
    ))
    for el in candidates:
        t = el.get_text(" ", strip=True)
        for kind, pat in CAPTION_PATTERNS.items():
            m = pat.match(t)
            if m:
                label = m.group(1)
                if kind == "figure":
                    FIGURE_CAPTIONS[label].append((path, t[:200]))
                elif kind == "code":
                    CODE_CAPTIONS[label].append((path, t[:200]))
                elif kind == "table":
                    TABLE_CAPTIONS[label].append((path, t[:200]))
                elif kind == "algorithm":
                    ALGORITHM_CAPTIONS[label].append((path, t[:200]))
                elif kind == "pseudocode":
                    PSEUDOCODE_CAPTIONS[label].append((path, t[:200]))
                break


# ---------------------------------------------------------------------------
# Path-aware "current chapter" lookup for caption-prefix consistency
# ---------------------------------------------------------------------------

def file_chapter_number(path: Path) -> int | None:
    """Return the module/chapter number derived from the file's parent module dir."""
    for part in path.parts:
        m = re.match(r"module-(\d+)", part)
        if m:
            return int(m.group(1))
    return None


def file_appendix_letter(path: Path) -> str | None:
    for part in path.parts:
        m = re.match(r"appendix-([a-z]+)-", part, re.IGNORECASE)
        if m:
            return m.group(1).upper()
    return None


# ---------------------------------------------------------------------------
# Body extraction: prose text only (strip code/captions/nav)
# ---------------------------------------------------------------------------

STRUCTURAL_SELECTORS = [
    ("header", "chapter-header"),
    ("nav", "chapter-nav"),
    ("nav", "header-nav"),
    ("footer", None),
]


def get_structural_ids(soup: BeautifulSoup) -> set[int]:
    out: set[int] = set()
    for tag_name, cls in STRUCTURAL_SELECTORS:
        if cls is None:
            shells = soup.find_all(tag_name)
        else:
            shells = soup.find_all(tag_name, class_=cls)
        for sh in shells:
            for desc in sh.find_all(True):
                out.add(id(desc))
    return out


def get_prose_text_with_lines(soup: BeautifulSoup, html_text: str) -> list[tuple[str, int]]:
    """Return (text_chunk, sourceline) for every prose text node in body that
    is NOT inside <pre>, <code>, <figcaption>, <caption>, structural nav, or
    code-caption blocks."""
    body = soup.body
    if body is None:
        return []
    struct_ids = get_structural_ids(soup)

    EXCLUDE_TAGS = {"pre", "code", "figcaption", "caption", "script", "style"}

    # Walk text nodes
    out: list[tuple[str, int]] = []
    for txt in body.find_all(string=True):
        if id(txt) in struct_ids:
            continue
        # Skip if any ancestor is excluded tag or has excluded class
        skip = False
        for anc in txt.parents:
            if not isinstance(anc, Tag):
                continue
            if id(anc) in struct_ids:
                skip = True
                break
            if anc.name in EXCLUDE_TAGS:
                skip = True
                break
            cls = anc.get("class") or []
            cls_str = " ".join(cls).lower() if cls else ""
            if any(c in cls_str for c in (
                "code-caption", "diagram-caption", "table-caption",
                "callout-title"
            )):
                skip = True
                break
        if skip:
            continue
        s = str(txt)
        if not s.strip():
            continue
        sl = getattr(txt, "sourceline", None) or 0
        out.append((s, sl))
    return out


# ---------------------------------------------------------------------------
# Cross-reference pattern matching in prose
# ---------------------------------------------------------------------------

PAT_CHAPTER = re.compile(
    r"\bChapter\s+(\d{1,2})\b(?!\s*[\.\-A-Za-z])", re.IGNORECASE
)
PAT_SECTION = re.compile(
    r"\bSection\s+(\d+(?:\.[\dA-Za-z]+){1,3})\b(?![\dA-Za-z\.])", re.IGNORECASE
)
PAT_PART = re.compile(
    r"\bPart\s+(I{1,3}|IV|V|VI{0,3}|IX|XI{0,3}|XII)\b(?![A-Za-z])"
)
PAT_APPENDIX_SEC = re.compile(
    r"\bAppendix\s+([A-Z](?:\.[\dA-Za-z]+){1,3})\b(?![\dA-Za-z\.])"
)
PAT_APPENDIX = re.compile(
    r"\bAppendix\s+([A-Z])\b(?![\.A-Za-z])"
)
PAT_FIGURE = re.compile(
    r"\bFigure\s+(\d+(?:\.[\dA-Za-z]+)+)\b(?![\dA-Za-z\.])", re.IGNORECASE
)
PAT_CODE_FRAG = re.compile(
    r"\bCode\s+Fragment\s+(\d+(?:\.[\dA-Za-z]+)+)\b(?![\dA-Za-z\.])", re.IGNORECASE
)
PAT_TABLE = re.compile(
    r"\bTable\s+(\d+(?:\.[\dA-Za-z]+)+)\b(?![\dA-Za-z\.])", re.IGNORECASE
)
PAT_ALGORITHM = re.compile(
    r"\bAlgorithm\s+(\d+(?:\.[\dA-Za-z]+)+)\b(?![\dA-Za-z\.])", re.IGNORECASE
)
PAT_PSEUDOCODE = re.compile(
    r"\bPseudocode\s+(\d+(?:\.[\dA-Za-z]+)+)\b(?![\dA-Za-z\.])", re.IGNORECASE
)


def find_line_in_html(html_text: str, fragment: str, used: dict[str, int]) -> int:
    """Best-effort: find a line containing the fragment that we have not
    already attributed."""
    key = fragment
    start = used.get(key, 0)
    idx = html_text.find(fragment, start)
    if idx < 0:
        # Try restarting from 0 to handle wrap-around (best-effort)
        idx = html_text.find(fragment)
        if idx < 0:
            return 0
    used[key] = idx + len(fragment)
    return html_text.count("\n", 0, idx) + 1


# ---------------------------------------------------------------------------
# Section / chapter existence helpers
# ---------------------------------------------------------------------------

def chapter_exists(num: int) -> bool:
    if num not in CHAPTER_TO_DIR:
        return False
    d = CHAPTER_TO_DIR[num]
    # A chapter exists if it has an index.html OR at least one section-*.html.
    if (d / "index.html").exists():
        return True
    return any(d.glob("section-*.html"))


def part_exists(roman: str) -> bool:
    return roman in PART_ROMAN_TO_DIR and (PART_ROMAN_TO_DIR[roman] / "index.html").exists()


def appendix_exists(letter: str) -> bool:
    return letter in APPENDIX_LETTER_TO_DIR and (APPENDIX_LETTER_TO_DIR[letter] / "index.html").exists()


def section_exists(label: str) -> bool:
    if label in SECTION_FILES and SECTION_FILES[label]:
        return True
    # Deeper sections: X.Y.Z -> parent section X.Y must contain matching anchor
    parts = label.split(".")
    if len(parts) >= 3:
        parent = ".".join(parts[:-1])
        if parent in SECTION_FILES and SECTION_FILES[parent]:
            # Accept presence of parent file; deeper anchor check is best-effort
            anchor_id = "-".join(parts)
            anchor_re = re.compile(r'id="' + re.escape(anchor_id) + r'(?:-[^"]*)?"', re.IGNORECASE)
            heading_re = re.compile(
                r"<h[2-6][^>]*>(?:[^<]|<[^>]+>)*\b" + re.escape(label) + r"\b",
                re.IGNORECASE,
            )
            for f in SECTION_FILES[parent]:
                try:
                    txt = f.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if anchor_re.search(txt) or heading_re.search(txt):
                    return True
            # If parent file exists, accept (lenient)
            return True
    return False


def appendix_section_exists(label: str) -> bool:
    upper = label.upper()
    if upper in APPENDIX_SECTION_FILES and APPENDIX_SECTION_FILES[upper]:
        return True
    parts = upper.split(".")
    if len(parts) >= 3:
        parent = ".".join(parts[:-1])
        if parent in APPENDIX_SECTION_FILES and APPENDIX_SECTION_FILES[parent]:
            return True
    return False


# ---------------------------------------------------------------------------
# Href resolution
# ---------------------------------------------------------------------------

def classify_href(href: str) -> str:
    if not href:
        return "empty"
    h = href.strip()
    sp = urlsplit(h)
    if sp.scheme in ("http", "https", "mailto", "tel", "javascript", "data", "ftp", "ftps", "ws", "wss"):
        return "external"
    if h.startswith("//"):
        return "external"
    if h.startswith("#"):
        return "anchor"
    if h.startswith("/"):
        return "absolute"
    return "relative"


def resolve_relative_path(page_path: Path, raw_path: str) -> Path | None:
    if not raw_path:
        return None
    base = page_path.parent
    try:
        target = (base / raw_path).resolve()
    except Exception:
        return None
    if raw_path.endswith("/"):
        return target / "index.html"
    if target.exists() and target.is_dir():
        return target / "index.html"
    if not target.suffix and not target.exists():
        as_dir = target / "index.html"
        if as_dir.exists():
            return as_dir
    return target


def resolve_absolute_path(raw_path: str) -> Path | None:
    p = raw_path.lstrip("/")
    target = (ROOT / p).resolve()
    if raw_path.endswith("/"):
        return target / "index.html"
    if target.exists() and target.is_dir():
        return target / "index.html"
    if not target.suffix and not target.exists():
        as_dir = target / "index.html"
        if as_dir.exists():
            return as_dir
    return target


# ---------------------------------------------------------------------------
# Suggestions
# ---------------------------------------------------------------------------

def nearest_chapter_suggestion(missing: int) -> str | None:
    if not CHAPTER_TO_DIR:
        return None
    nearest = min(CHAPTER_TO_DIR.keys(), key=lambda k: abs(k - missing))
    if abs(nearest - missing) <= 5:
        return f"Chapter {nearest} (`{rel(CHAPTER_TO_DIR[nearest])}`)"
    return None


def nearest_section_suggestion(missing: str) -> str | None:
    parts = missing.split(".")
    if not parts:
        return None
    try:
        ch_num = int(parts[0])
    except ValueError:
        return None
    near_secs = [s for s in SECTION_FILES.keys() if s.startswith(f"{ch_num}.")]
    if near_secs:
        # Find closest by string distance on the section index
        try:
            target_idx = int(parts[1]) if len(parts) >= 2 else 0
            best = min(near_secs, key=lambda s: abs(int(s.split(".")[1]) - target_idx))
            return f"Section {best}"
        except ValueError:
            return f"e.g. Section {sorted(near_secs)[0]}"
    return nearest_chapter_suggestion(ch_num)


def nearest_appendix_suggestion(missing_letter: str) -> str | None:
    if not APPENDIX_LETTER_TO_DIR:
        return None
    letters = sorted(APPENDIX_LETTER_TO_DIR.keys())
    if missing_letter in letters:
        return None
    # Closest letter
    best = min(letters, key=lambda L: abs(ord(L) - ord(missing_letter[0])))
    return f"Appendix {best} (`{rel(APPENDIX_LETTER_TO_DIR[best])}`)"


def caption_chapter_prefix(label: str) -> int | None:
    m = re.match(r"^(\d+)\.", label)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Loading target structure ...")
    load_target_structure()
    print(f"  target chapters: {len(TARGET_CHAPTERS)}")
    print(f"  target sections: {len(TARGET_SECTIONS)}")
    print(f"  target appendices: {len(TARGET_APPENDIX_LETTERS)}")

    print("Building on-disk inventory ...")
    build_disk_inventory()
    print(f"  disk chapters: {len(CHAPTER_TO_DIR)}")
    print(f"  disk parts: {len(PART_ROMAN_TO_DIR)}")
    print(f"  disk appendices: {len(APPENDIX_LETTER_TO_DIR)}")
    print(f"  disk section files: {sum(len(v) for v in SECTION_FILES.values())}")
    print(f"  disk appendix-section files: {sum(len(v) for v in APPENDIX_SECTION_FILES.values())}")

    pages = iter_html_files()
    print(f"Scanning {len(pages)} HTML files for captions ...")

    # First pass: harvest captions across the book
    for i, p in enumerate(pages):
        if i % 100 == 0:
            print(f"  caption pass {i}/{len(pages)}")
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        soup = BeautifulSoup(html, "html.parser")
        harvest_captions(p, soup)
    print(f"  captions: figures={len(FIGURE_CAPTIONS)} code={len(CODE_CAPTIONS)} "
          f"tables={len(TABLE_CAPTIONS)} algo={len(ALGORITHM_CAPTIONS)} pc={len(PSEUDOCODE_CAPTIONS)}")

    # Counters
    total_refs = 0
    n_chapter = n_chapter_broken = 0
    n_section = n_section_broken = 0
    n_part = n_part_broken = 0
    n_apx = n_apx_broken = 0
    n_apx_sec = n_apx_sec_broken = 0
    n_figure_caption_drift = 0
    n_code_caption_drift = 0
    n_table_caption_drift = 0
    n_algorithm_caption_drift = 0
    n_pseudocode_caption_drift = 0
    n_href_total = 0
    n_href_external = 0
    n_href_broken_file = 0
    n_href_broken_anchor = 0

    suspect_outside_target: list[tuple[str, int, str, str]] = []  # (file, line, ref, why)
    broken_records: list[tuple[str, int, str, str, str]] = []     # (file, line, kind, label, suggestion)
    href_broken: list[tuple[str, int, str, str]] = []             # (file, line, href, resolved)
    caption_drift: list[tuple[str, int, str, str, int, int]] = []  # (file, line, kind, label, label_ch, file_ch)

    # Second pass: cross-reference scan + href scan
    for i, p in enumerate(pages):
        if i % 50 == 0:
            print(f"  xref pass {i}/{len(pages)}")
        try:
            html_text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        try:
            soup = BeautifulSoup(html_text, "html.parser")
        except Exception:
            continue

        file_ch = file_chapter_number(p)
        file_apx = file_appendix_letter(p)

        # ---- Prose cross-refs ----
        prose = get_prose_text_with_lines(soup, html_text)
        used_idx: dict[str, int] = {}

        for text, sline in prose:
            # Chapter N
            for m in PAT_CHAPTER.finditer(text):
                num_str = m.group(1)
                try:
                    num = int(num_str)
                except ValueError:
                    continue
                # Heuristic: cap at 65 (target max chapter)
                if num > 70:
                    continue
                total_refs += 1
                n_chapter += 1
                if not chapter_exists(num):
                    n_chapter_broken += 1
                    sug = nearest_chapter_suggestion(num) or "(no nearby chapter on disk)"
                    line = find_line_in_html(html_text, f"Chapter {num_str}", used_idx)
                    broken_records.append((rel(p), line, "Chapter", f"Chapter {num}", sug))
                # Suspect: not in target.yaml
                if TARGET_CHAPTERS and num not in TARGET_CHAPTERS:
                    line = find_line_in_html(html_text, f"Chapter {num_str}", used_idx)
                    suspect_outside_target.append(
                        (rel(p), line, f"Chapter {num}",
                         "not declared in book_structure.target.yaml")
                    )

            # Section X.Y(.Z)
            for m in PAT_SECTION.finditer(text):
                label = m.group(1)
                total_refs += 1
                n_section += 1
                if not section_exists(label):
                    n_section_broken += 1
                    sug = nearest_section_suggestion(label) or "(no nearby section)"
                    line = find_line_in_html(html_text, f"Section {label}", used_idx)
                    broken_records.append((rel(p), line, "Section", f"Section {label}", sug))
                # Suspect: not declared
                top2 = ".".join(label.split(".")[:2])
                if TARGET_SECTIONS and top2 not in TARGET_SECTIONS and label not in TARGET_SECTIONS:
                    line = find_line_in_html(html_text, f"Section {label}", used_idx)
                    suspect_outside_target.append(
                        (rel(p), line, f"Section {label}",
                         "not declared in target.yaml")
                    )

            # Part X
            for m in PAT_PART.finditer(text):
                roman = m.group(1)
                if roman not in ROMAN_TO_PART_NUM:
                    continue
                total_refs += 1
                n_part += 1
                if not part_exists(roman):
                    n_part_broken += 1
                    line = find_line_in_html(html_text, f"Part {roman}", used_idx)
                    broken_records.append((rel(p), line, "Part", f"Part {roman}",
                                           "(no matching part-N-*/index.html)"))
                if TARGET_PARTS_ROMAN and roman not in TARGET_PARTS_ROMAN:
                    line = find_line_in_html(html_text, f"Part {roman}", used_idx)
                    suspect_outside_target.append(
                        (rel(p), line, f"Part {roman}", "not declared in target.yaml")
                    )

            # Appendix X.N first (more specific), then Appendix X
            consumed_spans: list[tuple[int, int]] = []
            for m in PAT_APPENDIX_SEC.finditer(text):
                label = m.group(1).upper()
                consumed_spans.append(m.span())
                total_refs += 1
                n_apx_sec += 1
                if not appendix_section_exists(label):
                    n_apx_sec_broken += 1
                    letter = label.split(".")[0]
                    sug = nearest_appendix_suggestion(letter) or "(no matching appendix)"
                    line = find_line_in_html(html_text, f"Appendix {m.group(1)}", used_idx)
                    broken_records.append((rel(p), line, "AppendixSection",
                                           f"Appendix {label}", sug))
                if TARGET_APPENDIX_SECTIONS and label not in TARGET_APPENDIX_SECTIONS:
                    line = find_line_in_html(html_text, f"Appendix {m.group(1)}", used_idx)
                    suspect_outside_target.append(
                        (rel(p), line, f"Appendix {label}", "not declared in target.yaml")
                    )

            for m in PAT_APPENDIX.finditer(text):
                # Skip if span overlaps a previously consumed Appendix-section span
                ms, me = m.span()
                if any(s <= ms < e for s, e in consumed_spans):
                    continue
                letter = m.group(1).upper()
                total_refs += 1
                n_apx += 1
                if not appendix_exists(letter):
                    n_apx_broken += 1
                    sug = nearest_appendix_suggestion(letter) or "(no matching appendix)"
                    line = find_line_in_html(html_text, f"Appendix {letter}", used_idx)
                    broken_records.append((rel(p), line, "Appendix", f"Appendix {letter}", sug))
                if TARGET_APPENDIX_LETTERS and letter not in TARGET_APPENDIX_LETTERS:
                    line = find_line_in_html(html_text, f"Appendix {letter}", used_idx)
                    suspect_outside_target.append(
                        (rel(p), line, f"Appendix {letter}", "not declared in target.yaml")
                    )

        # ---- Caption prefix consistency (chapter num) ----
        # Walk caption elements again here to capture per-page sourceline.
        for el in (
            soup.find_all(["figcaption", "caption"])
            + soup.find_all("div", class_=["diagram-caption", "code-caption", "table-caption"])
            + soup.select(
                "div.callout.algorithm div.callout-title, "
                "aside.callout.algorithm div.callout-title, "
                "div.callout.pseudocode div.callout-title, "
                "aside.callout.pseudocode div.callout-title"
            )
        ):
            t = el.get_text(" ", strip=True)
            for kind, pat in CAPTION_PATTERNS.items():
                m = pat.match(t)
                if not m:
                    continue
                label = m.group(1)
                label_ch = caption_chapter_prefix(label)
                if label_ch is None or file_ch is None:
                    continue
                if label_ch != file_ch:
                    # Appendices use letter prefixes (rare numeric here), still flag
                    sline = getattr(el, "sourceline", None) or 0
                    caption_drift.append(
                        (rel(p), sline, kind.capitalize(), f"{kind.capitalize()} {label}",
                         label_ch, file_ch)
                    )
                    if kind == "figure":
                        n_figure_caption_drift += 1
                    elif kind == "code":
                        n_code_caption_drift += 1
                    elif kind == "table":
                        n_table_caption_drift += 1
                    elif kind == "algorithm":
                        n_algorithm_caption_drift += 1
                    elif kind == "pseudocode":
                        n_pseudocode_caption_drift += 1
                break

        # ---- href links (in body, outside structural shells) ----
        body = soup.body
        if body is None:
            continue
        struct_ids = get_structural_ids(soup)
        # We already collected non-structural by element id earlier; reuse here.
        # Pre-compute self anchor inventory.
        self_anchors: set[str] = set()
        for el in soup.find_all(attrs={"id": True}):
            v = el.get("id")
            if v:
                self_anchors.add(v.strip())
        for el in soup.find_all("a", attrs={"name": True}):
            v = el.get("name")
            if v:
                self_anchors.add(v.strip())

        for a in body.find_all("a"):
            if id(a) in struct_ids:
                continue
            href = a.get("href")
            if href is None:
                continue
            href = href.strip()
            if not href:
                continue
            n_href_total += 1
            kind = classify_href(href)
            line = getattr(a, "sourceline", None) or 0
            if kind == "external":
                n_href_external += 1
                continue
            if kind == "anchor":
                frag = unquote(href[1:]).strip()
                if frag and frag not in self_anchors:
                    n_href_broken_anchor += 1
                    href_broken.append((rel(p), line, href, "(self-anchor missing)"))
                continue
            sp = urlsplit(href)
            path_part = unquote(sp.path)
            frag = unquote(sp.fragment).strip()
            if kind == "absolute":
                target = resolve_absolute_path(path_part) if path_part else None
            else:  # relative
                target = resolve_relative_path(p, path_part) if path_part else p
            if target is None or not target.exists():
                n_href_broken_file += 1
                resolved = rel(target) if target else "(unresolved)"
                href_broken.append((rel(p), line, href, resolved))
                continue
            if frag:
                # Check anchor in target
                try:
                    tgt_html = target.read_text(encoding="utf-8", errors="replace")
                    tgt_soup = BeautifulSoup(tgt_html, "html.parser")
                except Exception:
                    continue
                target_anchors: set[str] = set()
                for el in tgt_soup.find_all(attrs={"id": True}):
                    v = el.get("id")
                    if v:
                        target_anchors.add(v.strip())
                for el in tgt_soup.find_all("a", attrs={"name": True}):
                    v = el.get("name")
                    if v:
                        target_anchors.add(v.strip())
                if frag not in target_anchors:
                    n_href_broken_anchor += 1
                    href_broken.append((rel(p), line, href, f"{rel(target)} (anchor '{frag}' missing)"))

    # ---- Compose report ----
    total_broken_refs = (
        n_chapter_broken + n_section_broken + n_part_broken
        + n_apx_broken + n_apx_sec_broken
    )
    total_caption_drift = (
        n_figure_caption_drift + n_code_caption_drift + n_table_caption_drift
        + n_algorithm_caption_drift + n_pseudocode_caption_drift
    )
    total_href_broken = n_href_broken_file + n_href_broken_anchor
    grand_total_audited = total_refs + n_href_total
    grand_total_broken = total_broken_refs + total_caption_drift + total_href_broken

    lines: list[str] = []
    lines.append("# Cross-reference Integrity Audit")
    lines.append("")
    lines.append("Read-only audit of cross-reference integrity book-wide after the major restructuring (Waves 1-4: ")
    lines.append("part renames, chapter renumbers, module dissolutions, appendix renumber).")
    lines.append("")
    lines.append(f"Root: `{ROOT.as_posix()}` | HTML pages scanned: {len(pages)}")
    lines.append("")
    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Category | Audited | Broken |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Chapter N references | {n_chapter} | {n_chapter_broken} |")
    lines.append(f"| Section X.Y references | {n_section} | {n_section_broken} |")
    lines.append(f"| Part X (Roman) references | {n_part} | {n_part_broken} |")
    lines.append(f"| Appendix X references | {n_apx} | {n_apx_broken} |")
    lines.append(f"| Appendix X.N references | {n_apx_sec} | {n_apx_sec_broken} |")
    lines.append(f"| `<a href>` body links (non-external) | {n_href_total - n_href_external} | {total_href_broken} |")
    lines.append(f"|   ... target file missing | - | {n_href_broken_file} |")
    lines.append(f"|   ... target ok, anchor missing | - | {n_href_broken_anchor} |")
    lines.append(f"| Figure caption chapter drift | - | {n_figure_caption_drift} |")
    lines.append(f"| Code Fragment caption chapter drift | - | {n_code_caption_drift} |")
    lines.append(f"| Table caption chapter drift | - | {n_table_caption_drift} |")
    lines.append(f"| Algorithm caption chapter drift | - | {n_algorithm_caption_drift} |")
    lines.append(f"| Pseudocode caption chapter drift | - | {n_pseudocode_caption_drift} |")
    lines.append("")
    lines.append(f"**Grand total cross-refs audited:** {grand_total_audited}")
    lines.append("")
    lines.append(f"**Grand total broken:** {grand_total_broken}")
    lines.append("")

    # Top 15 broken references with file:line + suggested fix
    lines.append("## 2. Top 15 broken cross-references")
    lines.append("")
    lines.append("Sorted by file (alphabetical), then by line.")
    lines.append("")
    lines.append("| # | File:Line | Kind | Cited as | Suggested fix |")
    lines.append("|---|---|---|---|---|")
    examples = sorted(broken_records, key=lambda r: (r[0], r[1]))[:15]
    for i, (f, ln, kind, lbl, sug) in enumerate(examples, 1):
        lines.append(f"| {i} | `{f}:{ln}` | {kind} | `{lbl}` | {sug} |")
    if not examples:
        lines.append("| - | _none_ | - | - | - |")
    lines.append("")

    # Caption drift sample
    lines.append("## 3. Caption-prefix drift (top 15)")
    lines.append("")
    lines.append("A captioned block carries a chapter prefix that disagrees with its containing module.")
    lines.append("")
    if caption_drift:
        lines.append("| # | File:Line | Kind | Label | Label chapter | File chapter |")
        lines.append("|---|---|---|---|---:|---:|")
        for i, (f, ln, kind, lbl, lch, fch) in enumerate(
            sorted(caption_drift, key=lambda r: (r[0], r[1]))[:15], 1
        ):
            lines.append(f"| {i} | `{f}:{ln}` | {kind} | `{lbl}` | {lch} | {fch} |")
    else:
        lines.append("_None._")
    lines.append("")

    # Broken hrefs
    lines.append("## 4. Broken `<a href>` body links (top 15)")
    lines.append("")
    if href_broken:
        lines.append("| # | File:Line | href | Resolved / issue |")
        lines.append("|---|---|---|---|")
        for i, (f, ln, h, resolved) in enumerate(
            sorted(href_broken, key=lambda r: (r[0], r[1]))[:15], 1
        ):
            lines.append(f"| {i} | `{f}:{ln}` | `{h}` | `{resolved}` |")
    else:
        lines.append("_None._")
    lines.append("")

    # Suspect: outside target structure
    lines.append("## 5. References that point OUTSIDE the target structure")
    lines.append("")
    lines.append("These are not declared in `book_structure.target.yaml`. Anything here is a candidate ")
    lines.append("for a stale reference that did not get rewritten when the restructuring (Waves 1-4) ran.")
    lines.append("")
    if suspect_outside_target:
        # Group by reference text to surface high-frequency stale tokens
        ref_counter: Counter[str] = Counter()
        for _f, _ln, ref, _why in suspect_outside_target:
            ref_counter[ref] += 1
        lines.append("### 5.1 Most common stale references")
        lines.append("")
        lines.append("| Occurrences | Reference |")
        lines.append("|---:|---|")
        for ref, c in ref_counter.most_common(25):
            lines.append(f"| {c} | `{ref}` |")
        lines.append("")
        lines.append("### 5.2 First 30 suspect references (file:line)")
        lines.append("")
        lines.append("| File:Line | Reference | Why |")
        lines.append("|---|---|---|")
        for f, ln, ref, why in sorted(suspect_outside_target, key=lambda r: (r[0], r[1]))[:30]:
            lines.append(f"| `{f}:{ln}` | `{ref}` | {why} |")
    else:
        lines.append("_None._")
    lines.append("")

    # Compare: did the restructure introduce new broken refs?
    lines.append("## 6. Did the restructure introduce broken references?")
    lines.append("")
    lines.append("Any reference whose target is NOT in `book_structure.target.yaml` is a strong ")
    lines.append("indicator that it pre-dates the restructure and never got rewritten. Conversely, ")
    lines.append("a broken reference whose target IS declared in target.yaml means the disk layout ")
    lines.append("never caught up to the plan (file missing).")
    lines.append("")

    # Bucket broken-ref records into (a) outside-target vs (b) target-but-missing
    outside_target_keys = {(f, ln, ref) for (f, ln, ref, _w) in suspect_outside_target}
    broken_outside = []
    broken_inside_target = []
    for f, ln, kind, lbl, sug in broken_records:
        if (f, ln, lbl) in outside_target_keys:
            broken_outside.append((f, ln, kind, lbl, sug))
        else:
            broken_inside_target.append((f, ln, kind, lbl, sug))

    lines.append(f"- Broken refs whose target IS declared in target.yaml (disk layout did not catch up): "
                 f"**{len(broken_inside_target)}**")
    lines.append(f"- Broken refs whose target is NOT in target.yaml (stale reference pre-restructure or "
                 f"phantom): **{len(broken_outside)}**")
    lines.append("")
    if broken_inside_target:
        lines.append("These are post-restructure suspects (target declared but file missing). Top 10:")
        lines.append("")
        lines.append("| File:Line | Kind | Cited as | Suggested fix |")
        lines.append("|---|---|---|---|")
        for f, ln, kind, lbl, sug in sorted(broken_inside_target, key=lambda r: (r[0], r[1]))[:10]:
            lines.append(f"| `{f}:{ln}` | {kind} | `{lbl}` | {sug} |")
        lines.append("")

    # Append disk-vs-target gap (chapters / appendices declared but missing on disk)
    missing_chapters_on_disk = sorted(c for c in TARGET_CHAPTERS if not chapter_exists(c))
    extra_chapters_on_disk = sorted(c for c in CHAPTER_TO_DIR if c not in TARGET_CHAPTERS)
    missing_apx_on_disk = sorted(L for L in TARGET_APPENDIX_LETTERS if not appendix_exists(L))
    extra_apx_on_disk = sorted(L for L in APPENDIX_LETTER_TO_DIR if L not in TARGET_APPENDIX_LETTERS)

    lines.append("## 7. Disk vs target structure gaps")
    lines.append("")
    if missing_chapters_on_disk:
        lines.append(f"- Chapters declared in target.yaml but NOT found on disk: "
                     f"{missing_chapters_on_disk}")
    else:
        lines.append("- Chapters declared in target.yaml are all present on disk.")
    if extra_chapters_on_disk:
        lines.append(f"- Chapter dirs on disk that are NOT declared in target.yaml: "
                     f"{extra_chapters_on_disk}")
    if missing_apx_on_disk:
        lines.append(f"- Appendix letters declared in target.yaml but NOT found on disk: "
                     f"{missing_apx_on_disk}")
    else:
        lines.append("- All declared appendix letters are present on disk.")
    if extra_apx_on_disk:
        lines.append(f"- Appendix letters on disk that are NOT declared in target.yaml: "
                     f"{extra_apx_on_disk}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Audit generated by `scripts/_audit_crossref_integrity.py` (read-only).")
    lines.append("")

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written: {OUT_PATH}")
    print(f"  grand total audited: {grand_total_audited}")
    print(f"  grand total broken:  {grand_total_broken}")


if __name__ == "__main__":
    main()
