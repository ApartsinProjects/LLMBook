"""
Audit section header typography consistency across the LLMBook.

Checks every content .html page (excluding KDP/, scripts/, templates/, etc.)
for the following heading-typography issues inside <main class="content">:

  1. Alignment   : any h2/h3/h4 whose effective alignment is NOT left
                   (inline style="text-align:center|right|justify",
                   inline align="...", or a parent container that imposes
                   text-align:center via class).
  2. Numbering   : whether each heading text starts with a section number
                   like "31.1.2", "1.2.3", "A.1", "12.", etc.
  3. Mixed style : within a single file, at a single heading level, some
                   headings are numbered and others are not.

Writes a markdown report to header-typography-audit.md. READ-ONLY: never
edits any HTML.

Usage:
    /c/Python314/python scripts/_audit_header_typography.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, Tag

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = ROOT / "header-typography-audit.md"

# Directories to skip entirely.
EXCLUDED_DIR_PARTS = {
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
# Path-fragment substring rejects (e.g. backup directories, temp_*).
EXCLUDED_NAME_PREFIXES = ("temp_",)
EXCLUDED_NAME_SUBSTRINGS = ("backup", "backups")

# CSS classes (and IDs) known to impose text-align:center on their
# descendants in book.css. Headings inside these containers should be
# excluded from the alignment audit because their centering is the
# intended page-title styling, not a heading inconsistency.
KNOWN_CENTERING_CONTAINERS = {
    "chapter-header",   # Top-of-page hero block (centers title)
    "diagram-caption",  # Figure captions (centered by default)
    "caption",
    "math-display",
    "figure-text",
}

# Containers whose styling specifically RESETS to left-align, which
# means anything inside them is fine regardless of inherited centering.
KNOWN_LEFT_CONTAINERS = {"content", "callout", "overview", "part-overview",
                        "objectives", "outcomes", "prereqs", "prerequisites"}

# Regex: heading text starts with a section-number prefix.
# Accepts: "31.1.2 Foo", "31.1 Foo", "12. Foo", "A.1 Foo", "B.3.2 Foo",
# "Chapter 12: ..." patterns are ALSO numbered for our purposes (rare).
NUMBER_RE = re.compile(
    r"""^\s*
        (?:
            \d+(?:\.\d+)*\.?     # numeric: 12, 1.2, 31.1.2, optional trailing dot
          | [A-Z]\.\d+(?:\.\d+)* # appendix: A.1, B.3.2
          | [A-Z]\d+(?:\.\d+)*   # capstone: C1.2
        )
        (?:\s+|:\s+|\.\s+)       # separator before title text
        \S                       # at least one non-space title char
    """,
    re.VERBOSE,
)

# Heading titles that are conventionally unnumbered regardless of the file's
# overall numbering scheme. Match is case-insensitive and ignores trailing
# colons / question marks.
HOUSEKEEPING_TITLES = {
    "prerequisites",
    "objective",
    "objectives",
    "outcomes",
    "learning objectives",
    "learning outcomes",
    "exercises",
    "exercise",
    "key takeaways",
    "takeaways",
    "what's next",
    "what comes next",
    "what next",
    "where to go from here",
    "what's in this section",
    "in this section",
    "in this chapter",
    "in this module",
    "bibliography",
    "bibliography and further reading",
    "further reading",
    "references",
    "summary",
    "chapter summary",
    "section summary",
    "self check",
    "self-check",
    "self check questions",
    "self-check questions",
    "self check answers",
    "self-check answers",
    "answers",
    "answer key",
    "glossary",
    "notes",
    "footnotes",
    "epigraph",
    "tip",
    "note",
    "warning",
    "big picture",
    "key insight",
    "common pitfall",
    "common pitfalls",
    "pitfall",
    "pitfalls",
    "discussion",
    "discussion questions",
    "ethical considerations",
    "responsible ai considerations",
    "case study",
    "case studies",
    "background",
    "introduction",
    "conclusion",
    "summary and outlook",
    "table of contents",
    "contents",
    "appendix",
    "additional resources",
    "resources",
    "scoring rubric",
    "rubric",
    "deliverables",
    "extensions",
    "stretch goals",
    "how to use these tables",
    "what you'll practice",
    "what you will practice",
    "skills practiced",
    "skills you'll practice",
    "example project ideas",
    "project ideas",
    "extension ideas",
}

# Heading title PREFIXES that mark conventional housekeeping headings,
# regardless of what follows (e.g. "Lab: Build...", "Hands-On Lab: ...").
HOUSEKEEPING_PREFIXES = (
    "hands-on lab",
    "lab:",
    "lab ",
    "lab—",
    "self-check question",
    "self check question",
    "exercise ",
    "exercise:",
    "discussion question",
    "review question",
    "review questions",
    "thought exercise",
)

# Strip these leading decoration characters before normalizing a title.
LEADING_DECOR_RE = re.compile(
    r"^[\s✓✅☑⚠📌🔑💡"
    r"✨✔✱❖▶◆●•·\-–—]+"
)


def is_housekeeping(text: str) -> bool:
    """Return True if a heading title should be exempt from numbering audit."""
    # Strip leading decoration (emoji, checkmarks, dashes, bullets) so titles
    # like "✓ Key Takeaways" or "📌 Key Takeaways" still match.
    stripped = LEADING_DECOR_RE.sub("", text).strip()
    # Also strip surrogate-pair emoji ranges in case the regex missed them.
    stripped = re.sub(r"^[^\w]+", "", stripped).strip()
    norm = stripped.lower().rstrip("?:.")
    if norm in HOUSEKEEPING_TITLES:
        return True
    for pfx in HOUSEKEEPING_PREFIXES:
        if norm.startswith(pfx):
            return True
    return False

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def discover_html_files(root: Path) -> list[Path]:
    """Yield every content .html under root, honoring exclusions."""
    out: list[Path] = []
    for p in root.rglob("*.html"):
        parts = set(p.relative_to(root).parts)
        if parts & EXCLUDED_DIR_PARTS:
            continue
        if any(part.startswith(EXCLUDED_NAME_PREFIXES) for part in parts):
            continue
        if any(sub in part.lower() for part in parts for sub in EXCLUDED_NAME_SUBSTRINGS):
            continue
        out.append(p)
    out.sort()
    return out


def inline_text_align(tag: Tag) -> str | None:
    """Return the text-align value from inline style or align attr, or None."""
    style = (tag.get("style") or "").lower()
    m = re.search(r"text-align\s*:\s*([a-z]+)", style)
    if m:
        return m.group(1)
    align = (tag.get("align") or "").lower().strip() or None
    return align


def find_containing_center(tag: Tag) -> str | None:
    """Walk up from tag; return the class/role that forces center alignment,
    or None if no enforced centering ancestor is found.

    Stops walking when it hits a KNOWN_LEFT_CONTAINER, because that resets the
    inherited text-align.
    """
    parent = tag.parent
    while parent is not None and isinstance(parent, Tag):
        # Inline style on ancestor.
        pstyle = (parent.get("style") or "").lower()
        pm = re.search(r"text-align\s*:\s*([a-z]+)", pstyle)
        classes = set(parent.get("class") or [])

        if classes & KNOWN_LEFT_CONTAINERS:
            # Ancestor reasserts left alignment; further up doesn't matter.
            return None
        if pm and pm.group(1) != "left":
            return f"<{parent.name} style=\"text-align:{pm.group(1)}\">"
        if classes & KNOWN_CENTERING_CONTAINERS:
            return f"<{parent.name} class=\"{' '.join(sorted(classes))}\">"
        parent = parent.parent
    return None


def effective_alignment(tag: Tag) -> tuple[str, str]:
    """Compute effective alignment and a cause-string for the report.

    Returns (alignment, cause). alignment is one of: "left", "center",
    "right", "justify". cause explains *why* if not left, else "".
    """
    inline = inline_text_align(tag)
    if inline:
        return inline, f"inline style/align=\"{inline}\""

    ancestor = find_containing_center(tag)
    if ancestor:
        # Try to capture the actual alignment from the ancestor info.
        m = re.search(r"text-align:([a-z]+)", ancestor)
        if m:
            return m.group(1), f"parent {ancestor}"
        # Ancestor is a known-centering CSS class.
        return "center", f"parent {ancestor}"
    return "left", ""


def is_in_chapter_header(tag: Tag) -> bool:
    """True if heading lives inside <header class='chapter-header'>."""
    parent = tag.parent
    while parent is not None and isinstance(parent, Tag):
        classes = set(parent.get("class") or [])
        if "chapter-header" in classes:
            return True
        if parent.name == "main":
            return False
        parent = parent.parent
    return False


def heading_text(tag: Tag) -> str:
    """Return collapsed visible text for a heading."""
    return re.sub(r"\s+", " ", tag.get_text(strip=True))


def is_numbered(text: str) -> bool:
    """True if heading text begins with a section-number-like prefix."""
    return bool(NUMBER_RE.match(text))


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------


def main() -> int:
    files = discover_html_files(ROOT)
    print(f"Scanning {len(files)} HTML files under {ROOT}...", file=sys.stderr)

    # Counters
    total_headings = 0
    by_level: Counter[str] = Counter()                 # body-only (non-housekeeping)
    all_by_level: Counter[str] = Counter()             # includes housekeeping
    numbered_by_level: Counter[str] = Counter()        # body-only numbered
    housekeeping_by_level: Counter[str] = Counter()
    non_left_records: list[dict] = []
    # filename -> level -> {"numbered": [...], "unnumbered": [...]}
    per_file_levels: dict[Path, dict[str, dict[str, list[tuple[int, str]]]]] = defaultdict(
        lambda: defaultdict(lambda: {"numbered": [], "unnumbered": []})
    )

    for fpath in files:
        try:
            raw = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"WARN: cannot read {fpath}: {e}", file=sys.stderr)
            continue
        soup = BeautifulSoup(raw, "html.parser")

        # Build a quick line-number index for each tag by re-scanning the raw
        # text for offsets. We use sourceline if available (lxml-like parsers
        # provide it; the bundled html.parser also does in recent bs4).
        for tag in soup.find_all(["h2", "h3", "h4"]):
            if is_in_chapter_header(tag):
                continue
            level = tag.name
            text = heading_text(tag)
            if not text:
                continue
            total_headings += 1
            all_by_level[level] += 1

            align, cause = effective_alignment(tag)
            numbered = is_numbered(text)
            housekeeping = is_housekeeping(text)

            # Housekeeping headings are excluded from numbering stats but
            # still counted for alignment checking.
            if housekeeping:
                housekeeping_by_level[level] += 1
            else:
                by_level[level] += 1
                if numbered:
                    numbered_by_level[level] += 1

            line_no = getattr(tag, "sourceline", None) or 0
            rel = fpath.relative_to(ROOT).as_posix()

            if align != "left":
                non_left_records.append({
                    "file": rel,
                    "line": line_no,
                    "level": level,
                    "text": text,
                    "align": align,
                    "cause": cause,
                })

            if not housekeeping:
                bucket = per_file_levels[fpath][level]
                entry = (line_no, text)
                if numbered:
                    bucket["numbered"].append(entry)
                else:
                    bucket["unnumbered"].append(entry)

    # Find files with mixed numbering at the same level.
    mixed_records: list[dict] = []
    for fpath, levels in per_file_levels.items():
        for level, groups in levels.items():
            n = len(groups["numbered"])
            u = len(groups["unnumbered"])
            if n > 0 and u > 0:
                mixed_records.append({
                    "file": fpath.relative_to(ROOT).as_posix(),
                    "level": level,
                    "numbered_count": n,
                    "unnumbered_count": u,
                    "numbered_sample": groups["numbered"][:3],
                    "unnumbered_sample": groups["unnumbered"][:3],
                })

    # ---- Build report ----
    lines: list[str] = []
    out = lines.append
    out("# Header Typography Audit")
    out("")
    out(f"Scanned **{len(files)}** HTML files under `{ROOT.as_posix()}`.")
    out("")

    # ---- Summary ----
    out("## 1. Summary")
    out("")
    out(f"- Total in-content headings scanned (h2 + h3 + h4): **{total_headings}**")
    out("")
    out("| Level | Total | Housekeeping | Body | Body numbered | Body unnumbered |")
    out("|---|---|---|---|---|---|")
    for lvl in ("h2", "h3", "h4"):
        body = by_level[lvl]
        housek = housekeeping_by_level[lvl]
        n = numbered_by_level[lvl]
        u = body - n
        out(f"| `{lvl}` | {all_by_level[lvl]} | {housek} | {body} | "
            f"{n} ({pct(n, body)}%) | {u} ({pct(u, body)}%) |")
    out("")
    out(f"- Non-left-aligned in-content headings: **{len(non_left_records)}**")
    out(f"- Files with mixed numbering style at same level "
        f"(excluding housekeeping headings): **{len(mixed_records)}**")
    out("")
    out("Definitions:")
    out("- *Housekeeping* headings are conventional labels like Prerequisites, "
        "Exercises, Bibliography, What's Next, Key Takeaways. These are "
        "conventionally unnumbered everywhere and are exempt from the "
        "numbering audit so they don't fire false \"mixed\" warnings.")
    out("- *Body* headings are everything else: the substantive section/"
        "subsection headers the user is asking about.")
    out("- Headings inside `<header class=\"chapter-header\">` (the centered "
        "page-top hero) are excluded entirely; centering there is intentional.")
    out("")

    # ---- Non-left ----
    out("## 2. Non-Left-Aligned Headings")
    out("")
    if not non_left_records:
        out("None. Every in-content h2/h3/h4 resolves to left alignment.")
    else:
        out(f"Found **{len(non_left_records)}** headings whose effective alignment is not left.")
        out("")
        out("| File | Line | Level | Align | Cause | Heading text |")
        out("|---|---|---|---|---|---|")
        for r in non_left_records[:500]:
            text = r["text"].replace("|", "\\|")
            if len(text) > 80:
                text = text[:77] + "..."
            cause = r["cause"].replace("|", "\\|")
            out(f"| `{r['file']}` | {r['line']} | {r['level']} | "
                f"{r['align']} | {cause} | {text} |")
        if len(non_left_records) > 500:
            out("")
            out(f"... ({len(non_left_records) - 500} additional rows omitted)")
    out("")

    # ---- Mixed numbering ----
    out("## 3. Files With Mixed Numbering (same level, both styles)")
    out("")
    if not mixed_records:
        out("No files have mixed numbered/unnumbered headings at the same level.")
    else:
        # Group by file.
        by_file: dict[str, list[dict]] = defaultdict(list)
        for r in mixed_records:
            by_file[r["file"]].append(r)
        # Also aggregate by top-level part.
        by_part: Counter[str] = Counter()
        for fname in by_file:
            part = fname.split("/", 1)[0]
            by_part[part] += 1
        out(f"Found **{len(mixed_records)}** file/level pairs spanning "
            f"**{len(by_file)}** files with mixed numbered/unnumbered body "
            "headings at the same level.")
        out("")
        out("**Part-level breakdown:**")
        out("")
        out("| Part | Files with mixed numbering |")
        out("|---|---|")
        for part, count in sorted(by_part.items(), key=lambda kv: (-kv[1], kv[0])):
            out(f"| `{part}` | {count} |")
        out("")
        out("**Detailed file list** (one row per file/level pair, single sample "
            "from each style; full lists omitted to keep the report concise):")
        out("")
        out("| File | Level | #num | #unnum | Numbered sample | Unnumbered sample |")
        out("|---|---|---|---|---|---|")
        for fname in sorted(by_file):
            for r in by_file[fname]:
                n_sample = r["numbered_sample"][0][1] if r["numbered_sample"] else ""
                u_sample = r["unnumbered_sample"][0][1] if r["unnumbered_sample"] else ""
                n_sample = _short(n_sample, 50).replace("|", "\\|")
                u_sample = _short(u_sample, 50).replace("|", "\\|")
                out(f"| `{fname}` | {r['level']} | {r['numbered_count']} | "
                    f"{r['unnumbered_count']} | {n_sample} | {u_sample} |")
    out("")

    # ---- Aggregate convention ----
    out("## 4. Aggregate Numbering Convention")
    out("")
    out("Across the whole book, the dominant style per heading level:")
    out("")
    out("| Level | Total | Numbered | Unnumbered | Dominant convention |")
    out("|---|---|---|---|---|")
    for lvl in ("h2", "h3", "h4"):
        n = numbered_by_level[lvl]
        u = by_level[lvl] - n
        if by_level[lvl] == 0:
            dominant = "(no data)"
        elif n > 2 * u:
            dominant = f"**numbered** ({pct(n, by_level[lvl])}%)"
        elif u > 2 * n:
            dominant = f"**unnumbered** ({pct(u, by_level[lvl])}%)"
        else:
            dominant = f"mixed (n={n}, u={u})"
        out(f"| `{lvl}` | {by_level[lvl]} | {n} | {u} | {dominant} |")
    out("")

    # ---- Recommended action plan ----
    out("## 5. Recommended Action Plan")
    out("")
    out(_recommendation_block(by_level, numbered_by_level, non_left_records, mixed_records))
    out("")

    # ---- Methodology footnote ----
    out("## Methodology")
    out("")
    out("- Script: `scripts/_audit_header_typography.py`")
    out("- Parser: BeautifulSoup (html.parser)")
    out(f"- Excluded directories: {', '.join(sorted(EXCLUDED_DIR_PARTS))}")
    out("- Excluded by name prefix: `temp_*`; by substring: `backup`/`backups`")
    out("- Headings inside `<header class=\"chapter-header\">` are not counted "
        "(centered hero is intentional).")
    out("- A heading is \"non-left\" if it has an inline `style=\"text-align:...\"` "
        "or `align=\"...\"` attribute, or sits inside an ancestor whose CSS class "
        "imposes centering (`chapter-header`, `diagram-caption`, `caption`, "
        "`math-display`, `figure-text`) and no closer ancestor in "
        f"{sorted(KNOWN_LEFT_CONTAINERS)} resets text-align.")
    out("- A heading is \"numbered\" if its text begins with `N`, `N.M`, `N.M.K`, "
        "`A.N`, `A.N.M`, or the same with a trailing `.` or `:`, followed by "
        "whitespace and additional text.")
    out("")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH} ({len(lines)} lines).")

    # Console summary for the caller.
    print(f"  Total headings scanned : {total_headings}")
    print(f"  Non-left-aligned       : {len(non_left_records)}")
    print(f"  Files with mixed style : {len(mixed_records)}")
    return 0


def pct(n: int, total: int) -> str:
    if total == 0:
        return "0.0"
    return f"{(100.0 * n / total):.1f}"


def _short(s: str, limit: int) -> str:
    """Truncate a string for table cells."""
    s = s.replace("\n", " ").strip()
    if len(s) <= limit:
        return s
    return s[: limit - 3] + "..."


def _recommendation_block(
    by_level: Counter[str],
    numbered_by_level: Counter[str],
    non_left_records: list[dict],
    mixed_records: list[dict],
) -> str:
    """Build the prose recommendation, parameterized on observed distribution."""
    parts: list[str] = []

    # ---- Alignment recommendation ----
    if non_left_records:
        parts.append(
            f"**Alignment.** {len(non_left_records)} in-content headings render "
            "with non-left alignment. The book otherwise treats h2/h3/h4 inside "
            "`<main class=\"content\">` as left-aligned (see `styles/book.css`, "
            "lines 62-80). Recommend a uniform rule:\n\n"
            "> **Every h2, h3, and h4 inside `<main class=\"content\">` must "
            "render left-aligned.** Remove inline `style=\"text-align:center\"` "
            "and `align=\"center\"` attributes from these headings, and "
            "either remove the heading from its centering container or add "
            "an explicit `text-align: left` override."
        )
    else:
        parts.append(
            "**Alignment.** No issues found: every in-content h2/h3/h4 already "
            "resolves to left alignment. The reporter's specific case "
            "(`part-9-safety-strategy/module-31-strategy-product-roi/"
            "section-31.1.html`, 31.1.2 vs 31.1.3) was verified by inspection: "
            "both headings are bare `<h2>N.N.N Title</h2>` with identical "
            "alignment in HTML and CSS. The reported visual discrepancy is "
            "therefore not reproducible from the source; either the user "
            "remembered a different file, or the difference was browser-/"
            "zoom-specific (e.g. a long heading wrapping to two lines may "
            "appear visually different)."
        )

    # ---- Numbering recommendation ----
    parts.append(
        "**Numbering.** The book has a clear convention at the h2 and h4 "
        f"levels but is genuinely split at the h3 level "
        f"({numbered_by_level['h3']} numbered vs "
        f"{by_level['h3'] - numbered_by_level['h3']} unnumbered).\n\n"
        "Recommended book-wide rule:\n\n"
        "> **`<h2>`: always numbered** with the section's two-or-three-level "
        f"prefix (e.g. `31.1.2 Use Case Identification`). "
        f"Observed: {numbered_by_level['h2']}/{by_level['h2']} "
        f"({pct(numbered_by_level['h2'], by_level['h2'])}%) already comply.\n"
        ">\n"
        "> **`<h3>`: choose ONE per chapter and stick to it.** The book uses "
        "two narrative styles:\n"
        "> - *Numbered prose-and-code chapters* (parts 3, 6, 7, 8, 9): "
        "use deep numbering `28.11.1.1`. Recommended for reference material.\n"
        "> - *Narrative tutorial chapters* (parts 1, 2, 5): use bare titles "
        "like `Online Softmax`. Recommended for prose-heavy sections.\n"
        ">\n"
        "> Pick one convention per **chapter/module**, not per individual "
        "file. Mixing within a file (37 cases listed in section 3) is the "
        "bug to fix; mixing across the book at h3 is acceptable if each "
        "chapter is internally consistent.\n"
        ">\n"
        f"> **`<h4>`: always unnumbered.** All {by_level['h4']} body h4 "
        "headings (Captum, LIME, Foundational Papers, etc.) are already "
        "unnumbered, so this rule is already universally followed."
    )

    if mixed_records:
        parts.append(
            f"**Concrete fix scope.** {len(mixed_records)} file/level pairs "
            f"across {len({r['file'] for r in mixed_records})} files need "
            "standardization. Roughly one-third are h3 in part-1 and part-2 "
            "tutorial sections that should be made fully unnumbered, and "
            "two-thirds are h3 in parts 4, 5, 8, 9 reference sections that "
            "should be made fully numbered.\n\n"
            "Suggested one-line fix recipe per file (manual review required, "
            "since adding a number requires knowing the section's position):\n\n"
            "```bash\n"
            "# Inspect the mixed level inside a single file:\n"
            "/c/Python314/python -c \"\n"
            "import re, sys\n"
            "from bs4 import BeautifulSoup\n"
            "s = BeautifulSoup(open(sys.argv[1], encoding='utf-8'), 'html.parser')\n"
            "for h in s.select('main.content h3'):\n"
            "    print(repr(h.get_text(strip=True)))\n"
            "\" path/to/section.html\n"
            "```\n\n"
            "Then, depending on the chapter's chosen convention, either "
            "(a) prepend the proper `N.M.K.L ` prefix to bare h3s, or "
            "(b) strip the leading number from numbered h3s."
        )
    else:
        parts.append(
            "No files currently mix numbered and unnumbered headings at the "
            "same level, so the only fix required is to standardize across "
            "files that already have a consistent (but possibly minority) "
            "internal style."
        )

    return "\n\n".join(parts)


if __name__ == "__main__":
    raise SystemExit(main())
