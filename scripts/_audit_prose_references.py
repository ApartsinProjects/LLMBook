"""Audit prose-style references inside the LLM Book that the existing
numbering audit does not cover.

This audit complements ``_audit_numbering_consistency.py``. The earlier audit
walked ONLY prose (with `<pre>`, `<code>`, captions, navigation chrome stripped
out). This one looks at the parts that were intentionally excluded:

  Category 1: References INSIDE code fragments and comments
              (`# See Figure X.Y.Z`, `// Discussed in Section 12.3`, etc.)

  Category 2: Prose mentions that should be hyperlinks but are plain text
              (`Figure 12.3.4` appears as text instead of <a>Figure 12.3.4</a>)

  Category 3: Image alt text that references a figure number
              (`alt="Figure 11.1.2: ..."` whose label disagrees with the
              surrounding <figcaption>)

  Category 4: Captions that cross-reference other figures / code fragments
              ("See also Figure X.Y.Z" inside a <figcaption>)

Output: prose-reference-audit.md at the project root.

Usage: python scripts/_audit_prose_references.py
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

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
# Inventory construction (shared with the existing audit)
# ---------------------------------------------------------------------------

SECTION_FILES: dict[str, list[Path]] = defaultdict(list)
CHAPTER_DIRS: dict[int, list[Path]] = defaultdict(list)
APPENDIX_LETTERS: set[str] = set()
PART_NUM_TO_ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
    6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
    11: "XI", 12: "XII",
}
PART_DIRS: dict[str, Path] = {}

FIGURE_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)
CODE_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)
ALGORITHM_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)
PSEUDOCODE_CAPTIONS: dict[str, list[tuple[Path, str]]] = defaultdict(list)


def parse_filename_section_label(filename: str) -> str | None:
    m = re.match(r"section-(\d+(?:\.\d+)*)\.html$", filename)
    return m.group(1) if m else None


def build_directory_inventory() -> None:
    for path in ROOT.rglob("section-*.html"):
        rel = path.relative_to(ROOT)
        if is_excluded(rel):
            continue
        label = parse_filename_section_label(path.name)
        if not label:
            continue
        SECTION_FILES[label].append(path)

    for path in ROOT.glob("part-*/module-*/index.html"):
        rel = path.relative_to(ROOT)
        if is_excluded(rel):
            continue
        m = re.match(r"module-(\d+)", path.parent.name)
        if m:
            CHAPTER_DIRS[int(m.group(1))].append(path)

    for path in ROOT.glob("part-*/index.html"):
        rel = path.relative_to(ROOT)
        if is_excluded(rel):
            continue
        m = re.match(r"part-(\d+)", path.parent.name)
        if m:
            roman = PART_NUM_TO_ROMAN.get(int(m.group(1)))
            if roman:
                PART_DIRS[roman] = path

    # Appendix display letters
    idx = ROOT / "appendices" / "index.html"
    if idx.exists():
        soup = BeautifulSoup(idx.read_text(encoding="utf-8", errors="replace"), "html.parser")
        for span in soup.select("div.chapter-card span.mod-num"):
            m = re.match(r"Appendix\s+([A-Z][A-Z]?)$", span.get_text(strip=True))
            if m:
                APPENDIX_LETTERS.add(m.group(1))


CAPTION_FIGURE_RE = re.compile(
    r"^\s*figure\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE
)
CAPTION_CODE_RE = re.compile(
    r"^\s*code\s+fragment\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE
)
CAPTION_ALGO_RE = re.compile(
    r"^\s*algorithm\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE
)
CAPTION_PSEUDOCODE_RE = re.compile(
    r"^\s*pseudocode\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE
)


def build_caption_inventory() -> None:
    for path in iter_html_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        soup = BeautifulSoup(text, "html.parser")
        # Figures
        candidates = (
            soup.find_all(["figcaption", "caption"])
            + soup.find_all("div", class_=["diagram-caption"])
        )
        for el in candidates:
            t = el.get_text(" ", strip=True)
            m = CAPTION_FIGURE_RE.match(t)
            if m:
                FIGURE_CAPTIONS[m.group(1)].append((path, t[:200]))
        # Code captions
        for el in soup.find_all("div", class_=["code-caption"]):
            t = el.get_text(" ", strip=True)
            m = CAPTION_CODE_RE.match(t)
            if m:
                CODE_CAPTIONS[m.group(1)].append((path, t[:200]))
            m = CAPTION_ALGO_RE.match(t)
            if m:
                ALGORITHM_CAPTIONS[m.group(1)].append((path, t[:200]))
            m = CAPTION_PSEUDOCODE_RE.match(t)
            if m:
                PSEUDOCODE_CAPTIONS[m.group(1)].append((path, t[:200]))
        # Algorithm/Pseudocode sometimes live in <div class="callout-title">
        # of a "callout algorithm" block.
        for el in soup.select("div.callout.algorithm div.callout-title, "
                              "aside.callout.algorithm div.callout-title"):
            t = el.get_text(" ", strip=True)
            m = CAPTION_PSEUDOCODE_RE.match(t)
            if m:
                PSEUDOCODE_CAPTIONS[m.group(1)].append((path, t[:200]))
            m = CAPTION_ALGO_RE.match(t)
            if m:
                ALGORITHM_CAPTIONS[m.group(1)].append((path, t[:200]))


# ---------------------------------------------------------------------------
# Existence checks
# ---------------------------------------------------------------------------


def section_exists(label: str) -> bool:
    if label in SECTION_FILES and SECTION_FILES[label]:
        return True
    parts = label.split(".")
    if len(parts) >= 3:
        parent = ".".join(parts[:-1])
        if parent in SECTION_FILES and SECTION_FILES[parent]:
            anchor = "-".join(parts)
            anchor_re = re.compile(
                r'id="' + re.escape(anchor) + r'(?:-[^"]*)?"', re.IGNORECASE
            )
            heading_re = re.compile(
                r"<h[2-4][^>]*>(?:[^<]|<[^>]+>)*\b"
                + re.escape(label) + r"\b",
                re.IGNORECASE,
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
    return num in CHAPTER_DIRS and bool(CHAPTER_DIRS[num])


def figure_exists(label: str) -> bool:
    return label in FIGURE_CAPTIONS


def code_fragment_exists(label: str) -> bool:
    return label in CODE_CAPTIONS


def algorithm_exists(label: str) -> bool:
    return label in ALGORITHM_CAPTIONS or label in PSEUDOCODE_CAPTIONS


# ---------------------------------------------------------------------------
# Source line attribution
# ---------------------------------------------------------------------------


def find_line(html_text: str, phrase: str, used: set[int]) -> int:
    start = 0
    first = 0
    while True:
        idx = html_text.find(phrase, start)
        if idx < 0:
            return first
        line = html_text.count("\n", 0, idx) + 1
        if first == 0:
            first = line
        if line not in used:
            used.add(line)
            return line
        start = idx + 1


# ---------------------------------------------------------------------------
# Reference patterns
# ---------------------------------------------------------------------------

# Used for matching inside code comments AND inside captions/alt text.
PATTERNS = {
    "figure": re.compile(
        r"\bFigure\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
        re.IGNORECASE,
    ),
    "section": re.compile(
        r"\bSection\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
        re.IGNORECASE,
    ),
    "code_fragment": re.compile(
        r"\bCode\s+Fragment\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
        re.IGNORECASE,
    ),
    "algorithm": re.compile(
        r"\bAlgorithm\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
        re.IGNORECASE,
    ),
    "pseudocode": re.compile(
        r"\bPseudocode\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
        re.IGNORECASE,
    ),
    "chapter": re.compile(r"\bChapter\s+(\d{1,2})\b", re.IGNORECASE),
}


def target_exists(kind: str, label: str) -> bool:
    if kind == "figure":
        return figure_exists(label)
    if kind == "section":
        return section_exists(label)
    if kind == "code_fragment":
        return code_fragment_exists(label)
    if kind == "algorithm":
        return algorithm_exists(label)
    if kind == "pseudocode":
        return algorithm_exists(label)
    if kind == "chapter":
        try:
            return chapter_exists(int(label))
        except ValueError:
            return False
    return False


# ---------------------------------------------------------------------------
# Category 1: inside <pre><code> comments
# ---------------------------------------------------------------------------

# Comment-style spans produced by Pygments / Prism for line comments
COMMENT_CSS_CLASSES = {"c", "c1", "cm", "cp", "cpf", "ch", "cs",
                       "token", "comment", "hljs-comment"}


def is_comment_span(el: Tag) -> bool:
    cls = el.get("class") or []
    if not cls:
        return False
    # Pygments uses single-class spans like <span class="c1">
    if any(c in COMMENT_CSS_CLASSES for c in cls):
        return True
    # Prism uses <span class="token comment">; classes is a list
    if "token" in cls and "comment" in cls:
        return True
    return False


_COMMENT_LINE_PREFIX_RE = re.compile(
    r"^\s*(?:#|//|/\*|\*|--)\s*(.*?)(?:\s*\*/)?\s*$"
)


def scan_code_comments(path: Path, html_text: str, soup: BeautifulSoup) -> list[dict]:
    """Find references inside <pre><code> in two ways:
      1. Pygments / Prism comment <span> elements (highlighted code).
      2. Plain (unhighlighted) code: walk each line and pick out comment lines.
    """
    issues: list[dict] = []
    used_lines: dict[str, set[int]] = defaultdict(set)
    seen_phrases: set[tuple[str, int]] = set()

    def emit(kind: str, label: str, phrase: str, context: str) -> None:
        if target_exists(kind, label):
            return
        line = find_line(html_text, phrase, used_lines[phrase])
        key = (phrase, line)
        if key in seen_phrases:
            return
        seen_phrases.add(key)
        issues.append({
            "category": "in_code",
            "kind": kind,
            "label": label,
            "phrase": phrase,
            "comment": context[:140],
            "line": line,
        })

    for pre in soup.find_all("pre"):
        for code in pre.find_all(["code"]):
            # (1) Highlighted comment spans
            for span in code.find_all("span"):
                if not is_comment_span(span):
                    continue
                txt = span.get_text(" ", strip=True)
                if not txt:
                    continue
                for kind, pat in PATTERNS.items():
                    for m in pat.finditer(txt):
                        emit(kind, m.group(1), m.group(0), txt)

            # (2) Plain code: walk each line, only flag comment lines.
            # We get the full text (preserving line breaks) and inspect each
            # line that starts with a comment marker.
            full = code.get_text("\n", strip=False)
            for raw_line in full.splitlines():
                cm = _COMMENT_LINE_PREFIX_RE.match(raw_line)
                if not cm:
                    continue
                body = cm.group(1) or ""
                if not body:
                    continue
                for kind, pat in PATTERNS.items():
                    for m in pat.finditer(body):
                        emit(kind, m.group(1), m.group(0), raw_line.strip())
    return issues


# ---------------------------------------------------------------------------
# Category 2: prose mentions that should be hyperlinks but are plain text
# ---------------------------------------------------------------------------

# Tags that contain navigation chrome / inventory we should not scan for
# "could-be-hyperlinks". Same list as the existing audit, plus a few tweaks.
CHROME_SELECTORS = [
    "nav.chapter-nav",
    "nav.header-nav",
    "footer",
    "header",
    "div.chapter-card",
    "aside.references",
    "div.further-reading",
    "div.bibliography",
    "pre",
    "code",
    "span.katex",
    "svg",
    "figcaption",
    "div.diagram-caption",
    "div.code-caption",
    "aside.section-internal-toc",
    "div.chapter-label",
    "div.part-label",
]


def strip_chrome(soup: BeautifulSoup) -> Tag:
    main = soup.find("main") or soup.body or soup
    if main is None:
        return soup
    copy = BeautifulSoup(str(main), "html.parser")
    for sel in CHROME_SELECTORS:
        for el in copy.select(sel):
            el.decompose()
    return copy


def scan_unlinked_mentions(
    path: Path, html_text: str, soup: BeautifulSoup,
) -> list[dict]:
    """A prose mention `Figure 12.3.4` is flagged as 'unlinked-could-link'
    when:
      - the target exists,
      - the text node containing the mention has no ancestor <a href>, and
      - the same paragraph does NOT already contain a hyperlink with the same
        label (paragraph-local de-dup).
    """
    body = strip_chrome(soup)
    issues: list[dict] = []
    used_lines: dict[str, set[int]] = defaultdict(set)

    # Iterate over text nodes (NavigableString) and find references.
    # We need (a) the source line and (b) whether the ancestor chain includes
    # an <a> element.
    for text_node in body.find_all(string=True):
        if isinstance(text_node, NavigableString) is False:
            continue
        # Skip if inside a tag we treat as chrome (extra safety though
        # strip_chrome should have removed them).
        parent = text_node.parent
        if parent is None:
            continue
        # Skip if any ancestor is an <a>
        already_in_link = False
        anc = parent
        depth = 0
        while anc is not None and depth < 20:
            if isinstance(anc, Tag) and anc.name == "a":
                already_in_link = True
                break
            anc = anc.parent
            depth += 1
        if already_in_link:
            continue

        # Find the closest paragraph-ish ancestor to do paragraph-local dedup
        para = parent
        depth = 0
        while para is not None and depth < 30:
            if isinstance(para, Tag) and para.name in (
                "p", "li", "div", "td", "blockquote", "aside"
            ):
                break
            para = para.parent
            depth += 1
        para_text = para.get_text(" ", strip=True) if isinstance(para, Tag) else ""
        # Collect labels already present as hyperlinks in this paragraph
        already_linked_labels: set[tuple[str, str]] = set()
        if isinstance(para, Tag):
            for a in para.find_all("a"):
                at = a.get_text(" ", strip=True)
                for kind, pat in PATTERNS.items():
                    m = pat.search(at)
                    if m:
                        already_linked_labels.add((kind, m.group(1)))

        text = str(text_node)
        for kind, pat in PATTERNS.items():
            for m in pat.finditer(text):
                label = m.group(1)
                phrase = m.group(0)
                if not target_exists(kind, label):
                    # Phantom plain-text reference
                    line = find_line(html_text, phrase, used_lines[phrase])
                    issues.append({
                        "category": "unlinked-phantom",
                        "kind": kind,
                        "label": label,
                        "phrase": phrase,
                        "line": line,
                    })
                    continue
                # Same paragraph already linked once? lower priority
                low_priority = (kind, label) in already_linked_labels
                line = find_line(html_text, phrase, used_lines[phrase])
                issues.append({
                    "category": "unlinked-could-link",
                    "kind": kind,
                    "label": label,
                    "phrase": phrase,
                    "line": line,
                    "low_priority": low_priority,
                })
    return issues


# ---------------------------------------------------------------------------
# Category 3: image alt-text references
# ---------------------------------------------------------------------------


def scan_alt_text(
    path: Path, html_text: str, soup: BeautifulSoup,
) -> list[dict]:
    issues: list[dict] = []
    used_lines: dict[str, set[int]] = defaultdict(set)
    for img in soup.find_all("img"):
        alt = img.get("alt") or ""
        if not alt:
            continue
        # The "owning" figcaption: the nearest <figure> ancestor's figcaption
        # (if any) is the canonical label. We use that to compare.
        owner_label = ""
        fig = img.find_parent("figure")
        if fig is not None:
            fc = fig.find("figcaption")
            if fc:
                fct = fc.get_text(" ", strip=True)
                fm = CAPTION_FIGURE_RE.match(fct)
                if fm:
                    owner_label = fm.group(1)

        # Check each pattern in alt text
        for kind, pat in PATTERNS.items():
            for m in pat.finditer(alt):
                label = m.group(1)
                phrase = m.group(0)
                line = find_line(html_text, phrase, used_lines[phrase])
                if not target_exists(kind, label):
                    issues.append({
                        "category": "alt-phantom",
                        "kind": kind,
                        "label": label,
                        "phrase": phrase,
                        "line": line,
                        "alt": alt[:140],
                        "owner_label": owner_label,
                    })
                    continue
                # If this is a figure ref inside an <img alt> that belongs to a
                # <figure> with its own <figcaption>, flag mismatch between
                # the two.
                if kind == "figure" and owner_label and label != owner_label:
                    issues.append({
                        "category": "alt-mismatch",
                        "kind": kind,
                        "label": label,
                        "phrase": phrase,
                        "line": line,
                        "alt": alt[:140],
                        "owner_label": owner_label,
                    })
    return issues


# ---------------------------------------------------------------------------
# Category 4: caption cross-references
# ---------------------------------------------------------------------------

CAPTION_CONTAINERS = [
    ("figcaption", None),
    ("div", "diagram-caption"),
    ("div", "code-caption"),
]


def scan_caption_xrefs(
    path: Path, html_text: str, soup: BeautifulSoup,
) -> list[dict]:
    issues: list[dict] = []
    used_lines: dict[str, set[int]] = defaultdict(set)

    # We treat the FIRST X.Y.Z label in a caption as the "own" label and
    # only flag references to OTHER labels as cross-references.
    candidates: list[Tag] = []
    candidates.extend(soup.find_all("figcaption"))
    candidates.extend(soup.find_all("caption"))
    candidates.extend(soup.find_all("div", class_=["diagram-caption", "code-caption"]))

    for cap in candidates:
        text = cap.get_text(" ", strip=True)
        if not text:
            continue
        # Determine "own" label for each kind
        own_labels: dict[str, str] = {}
        for kind, pat in PATTERNS.items():
            mm = pat.search(text)
            if mm:
                own_labels[kind] = mm.group(1)
        # Identify each match and skip if it equals the own label
        for kind, pat in PATTERNS.items():
            seen_first = False
            own = own_labels.get(kind, "")
            for m in pat.finditer(text):
                label = m.group(1)
                phrase = m.group(0)
                # The first occurrence of the same kind is the caption's own
                # numbering; skip it.
                if not seen_first and label == own:
                    seen_first = True
                    continue
                line = find_line(html_text, phrase, used_lines[phrase])
                if target_exists(kind, label):
                    # Valid cross-reference; informational only
                    continue
                issues.append({
                    "category": "caption-phantom",
                    "kind": kind,
                    "label": label,
                    "phrase": phrase,
                    "line": line,
                    "caption": text[:160],
                })
    return issues


# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------


def scan_file(path: Path) -> dict:
    try:
        html_text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {"issues": []}
    soup = BeautifulSoup(html_text, "html.parser")
    issues: list[dict] = []
    issues.extend(scan_code_comments(path, html_text, soup))
    issues.extend(scan_unlinked_mentions(path, html_text, soup))
    issues.extend(scan_alt_text(path, html_text, soup))
    issues.extend(scan_caption_xrefs(path, html_text, soup))
    return {"issues": issues}


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def relfmt(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_report(all_issues: dict[Path, list[dict]]) -> Path:
    out = ROOT / "prose-reference-audit.md"
    lines: list[str] = []

    # Aggregate
    counts: Counter = Counter()
    for f, issues in all_issues.items():
        for it in issues:
            counts[it["category"]] += 1

    cat1 = []   # in-code
    cat2_ok = []  # unlinked-could-link
    cat2_ph = []  # unlinked-phantom
    cat3_ph = []
    cat3_mm = []
    cat4 = []
    for f, issues in all_issues.items():
        for it in issues:
            c = it["category"]
            if c == "in_code":
                cat1.append((f, it))
            elif c == "unlinked-could-link":
                cat2_ok.append((f, it))
            elif c == "unlinked-phantom":
                cat2_ph.append((f, it))
            elif c == "alt-phantom":
                cat3_ph.append((f, it))
            elif c == "alt-mismatch":
                cat3_mm.append((f, it))
            elif c == "caption-phantom":
                cat4.append((f, it))

    total_files = len(iter_html_files())
    total_problems = (
        len(cat1) + len(cat2_ph) + len(cat3_ph) + len(cat3_mm) + len(cat4)
    )

    lines.append("# Prose Reference Audit")
    lines.append("")
    lines.append(
        f"Audit run: **{total_files}** content HTML pages scanned. "
        f"Inventories: {sum(len(v) for v in FIGURE_CAPTIONS.values())} figure captions, "
        f"{sum(len(v) for v in CODE_CAPTIONS.values())} code-fragment captions, "
        f"{sum(len(v) for v in ALGORITHM_CAPTIONS.values()) + sum(len(v) for v in PSEUDOCODE_CAPTIONS.values())} algorithm/pseudocode blocks, "
        f"{sum(len(v) for v in SECTION_FILES.values())} section files, "
        f"{len(CHAPTER_DIRS)} chapters."
    )
    lines.append("")
    lines.append("This audit complements the existing `numbering-audit.md`. "
                 "The earlier pass walked PROSE only; this one scans inside code-fragment "
                 "comments, inside `<img alt>` attributes, inside caption cross-references, "
                 "and across plain-text prose mentions that could be hyperlinked.")
    lines.append("")
    # Headline status line
    status_problems = (
        len(cat1) + len(cat2_ph) + len(cat3_ph) + len(cat3_mm) + len(cat4)
    )
    if status_problems == 0:
        lines.append(
            f"**Headline:** No genuine reference breakage across any of the four problem "
            f"categories. The only finding is **{len(cat2_ok)}** plain-text mentions of "
            f"existing targets that *could* be hyperlinked (Cat. 2a; see Section 3)."
        )
    else:
        lines.append(
            f"**Headline:** {status_problems} genuine reference problems found across "
            f"{len([f for f in all_issues if any(it['category'] in ('in_code', 'unlinked-phantom', 'alt-phantom', 'alt-mismatch', 'caption-phantom') for it in all_issues[f])])} "
            f"files (plus {len(cat2_ok)} plain-text mentions that could be hyperlinks)."
        )
    lines.append("")

    # Summary table
    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Category | Problems found |")
    lines.append("|---|---:|")
    lines.append(f"| Cat. 1 — Phantom refs inside code comments | {len(cat1)} |")
    lines.append(f"| Cat. 2a — Plain-text mentions that should be hyperlinks | {len(cat2_ok)} |")
    lines.append(f"| Cat. 2b — Plain-text mentions whose target does not exist | {len(cat2_ph)} |")
    lines.append(f"| Cat. 3a — `<img alt>` references with no matching target | {len(cat3_ph)} |")
    lines.append(f"| Cat. 3b — `<img alt>` figure label disagrees with surrounding caption | {len(cat3_mm)} |")
    lines.append(f"| Cat. 4 — Caption cross-refs to non-existent targets | {len(cat4)} |")
    lines.append(f"| **Total problems** (excluding Cat. 2a hyperlink suggestions) | **{total_problems}** |")
    lines.append("")

    # ----------------------------------------------------------------
    # Category 1
    # ----------------------------------------------------------------
    lines.append("## 2. Category 1 — Phantom references inside code comments")
    lines.append("")
    lines.append("References found inside `<pre><code>` comment spans whose target does "
                 "not exist anywhere in the book.")
    lines.append("")
    if not cat1:
        lines.append("_None found._")
    else:
        lines.append("| File:Line | Kind | Cited as | Comment context |")
        lines.append("|---|---|---|---|")
        for f, it in sorted(cat1, key=lambda x: (relfmt(x[0]), x[1]["line"])):
            ctx = it["comment"].replace("|", "\\|")
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | {it['kind']} | "
                f"`{it['phrase']}` | `{ctx}` |"
            )
    lines.append("")

    # ----------------------------------------------------------------
    # Category 2 — top 30 by frequency
    # ----------------------------------------------------------------
    lines.append("## 3. Category 2 — Plain-text mentions that could be hyperlinks")
    lines.append("")
    lines.append("Prose contains `Figure X.Y.Z` / `Section X.Y` etc. as plain text, "
                 "but the target exists and is normally linked elsewhere. Highest-value "
                 "candidates are labels mentioned unlinked **on three or more pages**; "
                 "single-mention occurrences are common (e.g. when discussing two figures "
                 "by name in the same paragraph) and lower priority.")
    lines.append("")
    # Filter to NON-low-priority only for the priority count
    primary_only = [
        (f, it) for f, it in cat2_ok if not it.get("low_priority")
    ]
    by_label: Counter = Counter()
    by_label_files: dict[tuple[str, str], set[Path]] = defaultdict(set)
    for f, it in primary_only:
        key = (it["kind"], it["label"])
        by_label[key] += 1
        by_label_files[key].add(f)

    lines.append(f"Total non-low-priority plain-text mentions: **{len(primary_only)}** "
                 f"across **{len(by_label)}** distinct labels.")
    lines.append("")
    lines.append("### Top 30 labels by un-linked-mention count")
    lines.append("")
    top = by_label.most_common(30)
    if not top:
        lines.append("_None found._")
    else:
        lines.append("| Rank | Label | Count | Distinct files | Example file:line |")
        lines.append("|---:|---|---:|---:|---|")
        # Build map (kind,label) -> first (file, line)
        first_seen: dict[tuple[str, str], tuple[Path, int]] = {}
        for f, it in primary_only:
            key = (it["kind"], it["label"])
            if key not in first_seen:
                first_seen[key] = (f, it["line"])
        for rank, ((kind, label), n) in enumerate(top, start=1):
            files_n = len(by_label_files[(kind, label)])
            f, line = first_seen[(kind, label)]
            display = (
                f"{kind.replace('_', ' ').title()} {label}"
                if kind != "chapter"
                else f"Chapter {label}"
            )
            lines.append(
                f"| {rank} | `{display}` | {n} | {files_n} | "
                f"`{relfmt(f)}`:{line} |"
            )
    lines.append("")

    # Sub-section: phantoms (these matter regardless of count)
    lines.append("### Cat. 2b — Plain-text mentions whose target does not exist")
    lines.append("")
    if not cat2_ph:
        lines.append("_None found._")
    else:
        # Show first 60 to keep the report manageable
        lines.append(f"Found **{len(cat2_ph)}** phantom plain-text mentions. Showing the first 60.")
        lines.append("")
        lines.append("| File:Line | Kind | Cited as |")
        lines.append("|---|---|---|")
        for f, it in sorted(cat2_ph, key=lambda x: (relfmt(x[0]), x[1]["line"]))[:60]:
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | {it['kind']} | `{it['phrase']}` |"
            )
    lines.append("")

    # ----------------------------------------------------------------
    # Category 3
    # ----------------------------------------------------------------
    lines.append("## 4. Category 3 — Image alt-text reference issues")
    lines.append("")
    lines.append("### Cat. 3a — alt-text cites a number that does not exist")
    lines.append("")
    if not cat3_ph:
        lines.append("_None found._")
    else:
        lines.append("| File:Line | Kind | Cited as | Surrounding figure | Alt-text |")
        lines.append("|---|---|---|---|---|")
        for f, it in sorted(cat3_ph, key=lambda x: (relfmt(x[0]), x[1]["line"])):
            alt = it["alt"].replace("|", "\\|")
            owner = it.get("owner_label", "") or "(no <figure> parent)"
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | {it['kind']} | `{it['phrase']}` | "
                f"`{owner}` | {alt} |"
            )
    lines.append("")
    lines.append("### Cat. 3b — alt-text figure number disagrees with surrounding figcaption")
    lines.append("")
    if not cat3_mm:
        lines.append("_None found._")
    else:
        lines.append("| File:Line | Alt says | Figcaption says | Alt-text |")
        lines.append("|---|---|---|---|")
        for f, it in sorted(cat3_mm, key=lambda x: (relfmt(x[0]), x[1]["line"])):
            alt = it["alt"].replace("|", "\\|")
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | `Figure {it['label']}` | "
                f"`Figure {it['owner_label']}` | {alt} |"
            )
    lines.append("")

    # ----------------------------------------------------------------
    # Category 4
    # ----------------------------------------------------------------
    lines.append("## 5. Category 4 — Caption cross-references to non-existent targets")
    lines.append("")
    lines.append("`<figcaption>`, `<caption>`, `div.diagram-caption`, `div.code-caption` "
                 "that reference another figure / section / code-fragment whose target does not exist.")
    lines.append("")
    if not cat4:
        lines.append("_None found._")
    else:
        lines.append("| File:Line | Kind | Cited as | Caption context |")
        lines.append("|---|---|---|---|")
        for f, it in sorted(cat4, key=lambda x: (relfmt(x[0]), x[1]["line"])):
            ctx = it["caption"].replace("|", "\\|")
            lines.append(
                f"| `{relfmt(f)}`:{it['line']} | {it['kind']} | "
                f"`{it['phrase']}` | {ctx} |"
            )
    lines.append("")

    # ----------------------------------------------------------------
    # Action plan
    # ----------------------------------------------------------------
    lines.append("## 6. Recommended action plan")
    lines.append("")
    bullets: list[str] = []
    # Headline: are any of the four real-problem categories non-empty?
    clean_categories = (len(cat1) == 0 and len(cat2_ph) == 0
                        and len(cat3_ph) == 0 and len(cat3_mm) == 0
                        and len(cat4) == 0)
    if clean_categories:
        bullets.append(
            "**No genuine reference breakage found.** All four problem categories "
            "(in-code phantoms, alt-text phantoms, alt-text mismatches, caption "
            "cross-references) returned zero hits. This strongly suggests the existing "
            "numbering audit + manual cleanup have already caught all phantom citations."
        )
    if cat3_mm:
        bullets.append(
            f"**FIX FIRST: alt-text vs. figcaption mismatches ({len(cat3_mm)} cases)** — "
            "These are accessibility bugs: a screen-reader hears 'Figure X.Y.Z' for an image "
            "whose printed caption says a different number. Edit each `alt` attribute to "
            "match the surrounding `<figcaption>`."
        )
    if cat3_ph:
        bullets.append(
            f"**Investigate alt-text phantom references ({len(cat3_ph)} cases)** — "
            "alt-text cites a figure/section/algorithm number that does not exist. "
            "Usually leftover from copy-paste during renumbering; rewrite the alt."
        )
    if cat4:
        bullets.append(
            f"**Fix caption cross-references ({len(cat4)} cases)** — "
            "Captions that say 'See also Figure X.Y.Z' for a non-existent target are "
            "user-visible broken promises. Each is a one-line edit."
        )
    if cat1:
        bullets.append(
            f"**Review in-code comments ({len(cat1)} cases)** — Code-fragment comments "
            "like `# See Figure X.Y.Z` cite a non-existent figure. Comments are often "
            "ignored during renumber passes; update or remove."
        )
    if cat2_ph:
        bullets.append(
            f"**Triage plain-text phantom mentions ({len(cat2_ph)} cases)** — "
            "Prose mentions a figure/section/code-fragment number that does not exist "
            "anywhere. These were missed by the numbering audit because they live in "
            "code blocks or other excluded contexts; verify and rewrite each."
        )
    # Hyperlink suggestions — only mention if a meaningful number
    if primary_only:
        n_dup3 = sum(1 for cnt in by_label.values() if cnt >= 3)
        bullets.append(
            f"**Optional hyperlinking pass ({len(primary_only)} plain-text mentions "
            f"across {len(by_label)} distinct labels; {n_dup3} labels mentioned 3+ "
            "times unlinked)** — The top labels in Section 3 are good candidates for a "
            "single search-and-replace pass that wraps `Figure X.Y.Z` in "
            "`<a href=...>Figure X.Y.Z</a>`. Skip cases where the paragraph already "
            "links the same label (Cat. 2a does NOT include those — they are flagged "
            "internally as low-priority and excluded from the top-30)."
        )
        bullets.append(
            "**Note on Cat. 2a scope** — Cat. 2a includes plain-text `Chapter NN` "
            "references in module-overview and appendix introductions where the chapter "
            "is named alongside its title (e.g. 'Chapter 28 (Evaluation)') and is "
            "*already* linked elsewhere on the page. These are stylistic choices and "
            "may not be worth bulk-rewriting; review the top-30 list before deciding."
        )
    bullets.append(
        "**Re-run after fixes** — re-run `python scripts/_audit_prose_references.py` "
        "after any structural change (renumbering, deletion of figures, restructure "
        "of sections)."
    )
    for b in bullets:
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
    build_caption_inventory()
    sys.stderr.write(
        f"  sections={len(SECTION_FILES)}, "
        f"chapters={len(CHAPTER_DIRS)}, "
        f"figures={len(FIGURE_CAPTIONS)}, "
        f"code_fragments={len(CODE_CAPTIONS)}, "
        f"algorithms={len(ALGORITHM_CAPTIONS)}, "
        f"pseudocode={len(PSEUDOCODE_CAPTIONS)}\n"
    )

    files = iter_html_files()
    sys.stderr.write(f"Scanning {len(files)} HTML files...\n")

    all_issues: dict[Path, list[dict]] = {}
    for i, p in enumerate(files):
        result = scan_file(p)
        if result["issues"]:
            all_issues[p] = result["issues"]
        if (i + 1) % 100 == 0:
            sys.stderr.write(f"  {i + 1}/{len(files)} scanned, "
                             f"{len(all_issues)} flagged\n")

    sys.stderr.write(f"Done scanning. {len(all_issues)} files have issues.\n")
    out = write_report(all_issues)
    sys.stderr.write(f"Report written to {out}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
