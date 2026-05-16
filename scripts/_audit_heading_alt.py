"""Accessibility audit: heading hierarchy + alt-text quality.

Scope: all .html files under the book root EXCEPT KDP/, .claude/, temp_*,
scripts/, *backups*, node_modules/, pagefind/, templates/.

Part 1 - Heading hierarchy:
  1. Skipped levels (e.g. h1 -> h3 with no h2 between).
  2. Multiple <h1> per page.
  3. Demoted <h1> after the first (mid-page corruption sign).
  4. Empty headings (whitespace only).
  5. Heading containing a block element (sanity confirmation).

Part 2 - Alt-text quality:
  1. Missing alt attribute entirely.
  2. Empty alt="" INSIDE a <figure> (figures are content).
  3. Boilerplate alt text (image, picture, graphic, "diagram of", etc).
  4. Alt text shorter than 8 characters inside <figure>.
  5. Alt text longer than 250 characters.

Writes the report to heading-alt-audit.md at the project root.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "heading-alt-audit.md"

SKIP_DIR_NAMES = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    "build", ".git", "source_fix_backups", "__pycache__",
}
SKIP_PREFIXES = ("temp_",)
SKIP_NAME_FRAGMENTS = ("backups",)

HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")

# Block elements that should not appear inside a heading.
BLOCK_ELEMENTS = {
    "p", "div", "section", "article", "aside", "header", "footer",
    "nav", "main", "figure", "blockquote", "pre", "ul", "ol", "li",
    "table", "tr", "td", "th", "thead", "tbody", "tfoot", "form",
    "fieldset", "address", "hr",
}

# Boilerplate substrings (case insensitive). Matched as substring.
BOILERPLATE_PATTERNS = [
    "image",
    "picture",
    "graphic",
    "diagram of",
    "screenshot of",
    "illustration of",
]

# Chapter / section number-only patterns (e.g. "Chapter 3", "Section 1.2").
NUMBER_ONLY_RE = re.compile(
    r"^\s*(chapter|section|part|appendix)\s+[\w.\-]+\s*$",
    re.IGNORECASE,
)


def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    if parts & SKIP_DIR_NAMES:
        return True
    for part in p.parts:
        if part.startswith(SKIP_PREFIXES):
            return True
        if any(frag in part for frag in SKIP_NAME_FRAGMENTS):
            return True
    return False


def collect_html_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.rglob("*.html")):
        if should_skip(p):
            continue
        files.append(p)
    return files


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def tag_line(tag: Tag) -> int:
    """Best-effort line number for a BeautifulSoup tag."""
    line = getattr(tag, "sourceline", None)
    return int(line) if line else 0


# ----------------------------------------------------------------------
# Part 1: Heading hierarchy
# ----------------------------------------------------------------------

def audit_headings(soup: BeautifulSoup) -> dict:
    """Return a dict of per-file heading issues."""
    issues = {
        "skipped": [],          # (line, from_level, to_level)
        "multiple_h1": [],      # (line,) for each h1 after the first
        "demoted_h1_after": [], # (line,) h1 that appears AFTER a non-h1 heading
        "empty": [],            # (line, tag_name)
        "block_in_heading": [], # (line, heading_tag, block_tag)
    }

    headings = soup.find_all(HEADING_TAGS)
    if not headings:
        return issues

    prev_level = 0
    h1_count = 0
    seen_non_h1 = False

    for h in headings:
        name = h.name.lower()
        level = int(name[1])
        line = tag_line(h)

        # 1. Empty heading text
        text = h.get_text(strip=True)
        if not text:
            issues["empty"].append((line, name))

        # 2. Block element inside heading
        for child in h.find_all(True):
            if child.name and child.name.lower() in BLOCK_ELEMENTS:
                issues["block_in_heading"].append((line, name, child.name.lower()))
                break  # one note per heading is enough

        # 3. Multiple h1
        if level == 1:
            h1_count += 1
            if h1_count > 1:
                issues["multiple_h1"].append((line,))
            if seen_non_h1:
                # an h1 appeared AFTER we already saw an h2/h3/etc
                issues["demoted_h1_after"].append((line,))
        else:
            seen_non_h1 = True

        # 4. Skipped levels — only flag when going DEEPER
        if prev_level > 0 and level > prev_level + 1:
            issues["skipped"].append((line, prev_level, level))

        prev_level = level

    return issues


# ----------------------------------------------------------------------
# Part 2: Alt-text quality
# ----------------------------------------------------------------------

def is_inside_figure(img: Tag) -> bool:
    parent = img.parent
    while parent is not None and isinstance(parent, Tag):
        if parent.name and parent.name.lower() == "figure":
            return True
        parent = parent.parent
    return False


def get_page_title(soup: BeautifulSoup) -> str:
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    title = soup.find("title")
    if title:
        return title.get_text(strip=True)
    return ""


def is_boilerplate(alt: str, page_title: str) -> str | None:
    """Return a short reason string if boilerplate, else None."""
    a = alt.strip().lower()
    if not a:
        return None
    for pat in BOILERPLATE_PATTERNS:
        if pat in a:
            return f"contains '{pat}'"
    if NUMBER_ONLY_RE.match(alt.strip()):
        return "just a number/section reference"
    if page_title and a == page_title.strip().lower():
        return "exact match of page title"
    return None


def audit_images(soup: BeautifulSoup) -> dict:
    """Return a dict of per-file alt-text issues."""
    issues = {
        "missing_alt": [],       # (line, src)
        "empty_in_figure": [],   # (line, src)
        "boilerplate": [],       # (line, src, alt, reason)
        "too_short": [],         # (line, src, alt)
        "too_long": [],          # (line, src, alt_len)
    }

    page_title = get_page_title(soup)

    for img in soup.find_all("img"):
        src = img.get("src", "").strip() or "(no src)"
        line = tag_line(img)
        in_figure = is_inside_figure(img)

        if "alt" not in img.attrs:
            issues["missing_alt"].append((line, src))
            continue

        alt = img.get("alt", "")
        alt_stripped = alt.strip()
        alt_len = len(alt_stripped)

        if alt_stripped == "":
            if in_figure:
                issues["empty_in_figure"].append((line, src))
            # empty alt outside figure = decorative = OK
            continue

        # Boilerplate
        reason = is_boilerplate(alt_stripped, page_title)
        if reason:
            issues["boilerplate"].append((line, src, alt_stripped, reason))

        # Too short (only inside figure)
        if in_figure and alt_len < 8:
            issues["too_short"].append((line, src, alt_stripped))

        # Too long
        if alt_len > 250:
            issues["too_long"].append((line, src, alt_len))

    return issues


# ----------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------

def main() -> int:
    files = collect_html_files()
    print(f"Auditing {len(files)} HTML files...", file=sys.stderr)

    per_file_heading: dict[Path, dict] = {}
    per_file_alt: dict[Path, dict] = {}
    parse_errors: list[tuple[Path, str]] = []

    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
            soup = BeautifulSoup(text, "html.parser")
        except Exception as exc:
            parse_errors.append((p, str(exc)))
            continue
        per_file_heading[p] = audit_headings(soup)
        per_file_alt[p] = audit_images(soup)

    write_report(per_file_heading, per_file_alt, parse_errors, len(files))
    print(f"Wrote {REPORT_PATH}", file=sys.stderr)
    return 0


# ----------------------------------------------------------------------
# Report writer
# ----------------------------------------------------------------------

def has_any_heading_issue(d: dict) -> bool:
    return any(d.get(k) for k in ("skipped", "multiple_h1", "demoted_h1_after", "empty", "block_in_heading"))


def has_any_alt_issue(d: dict) -> bool:
    return any(d.get(k) for k in ("missing_alt", "empty_in_figure", "boilerplate", "too_short", "too_long"))


def count_total_issues(d: dict) -> int:
    return sum(len(v) for v in d.values())


def write_report(
    headings: dict,
    alts: dict,
    parse_errors: list,
    total_files: int,
) -> None:
    lines: list[str] = []
    lines.append("# Heading hierarchy & alt-text accessibility audit")
    lines.append("")
    lines.append(f"Total HTML files scanned: {total_files}")
    if parse_errors:
        lines.append(f"Parse errors: {len(parse_errors)}")
    lines.append("")

    # ------- Summary table -------
    def total_and_pages(category_key: str, source: dict) -> tuple[int, int]:
        total = 0
        pages = 0
        for issues in source.values():
            cnt = len(issues.get(category_key, []))
            total += cnt
            if cnt:
                pages += 1
        return total, pages

    summary_rows = [
        ("Heading: skipped level (h1->h3 etc)", "skipped", headings),
        ("Heading: multiple <h1> on page", "multiple_h1", headings),
        ("Heading: <h1> after non-h1 (demoted)", "demoted_h1_after", headings),
        ("Heading: empty heading", "empty", headings),
        ("Heading: block element inside heading", "block_in_heading", headings),
        ("Alt: missing alt attribute", "missing_alt", alts),
        ("Alt: empty alt inside <figure>", "empty_in_figure", alts),
        ("Alt: boilerplate text", "boilerplate", alts),
        ("Alt: too short (<8 chars in figure)", "too_short", alts),
        ("Alt: too long (>250 chars)", "too_long", alts),
    ]

    lines.append("## Summary")
    lines.append("")
    lines.append("| Issue | Total | Pages affected |")
    lines.append("|---|---:|---:|")
    for label, key, source in summary_rows:
        t, pages = total_and_pages(key, source)
        lines.append(f"| {label} | {t} | {pages} |")
    lines.append("")

    # ------- Heading hierarchy issues -------
    lines.append("## Heading hierarchy issues")
    lines.append("")
    flagged_files = [p for p, d in sorted(headings.items()) if has_any_heading_issue(d)]
    if not flagged_files:
        lines.append("_No heading hierarchy issues found._")
        lines.append("")
    else:
        lines.append(f"Files with heading issues: **{len(flagged_files)}**")
        lines.append("")

        # Separate "single h1->h3 skip" boilerplate from richer cases.
        # A simple page = exactly one skipped (1->3) issue and nothing else.
        simple_skip_pages: list[Path] = []
        complex_files: list[Path] = []
        for p in flagged_files:
            d = headings[p]
            only_skip_1_3 = (
                len(d["skipped"]) == 1
                and d["skipped"][0][1] == 1
                and d["skipped"][0][2] == 3
                and not d["multiple_h1"]
                and not d["demoted_h1_after"]
                and not d["empty"]
                and not d["block_in_heading"]
            )
            if only_skip_1_3:
                simple_skip_pages.append(p)
            else:
                complex_files.append(p)

        lines.append(
            f"### Bulk pattern: single h1 -> h3 skip ({len(simple_skip_pages)} pages)"
        )
        lines.append("")
        lines.append(
            "These pages share the same templating pattern: a single `<h1>` section title "
            "followed directly by `<h3>` subsections, with no intermediate `<h2>`. This is "
            "consistent across the section template and should be fixed at the template level "
            "by either re-leveling subsections to `<h2>` or by inserting an `<h2>` chapter banner."
        )
        lines.append("")
        # Group by parent directory for a compact view.
        by_dir: dict[str, list[Path]] = defaultdict(list)
        for p in simple_skip_pages:
            parent = rel(p).rsplit("/", 1)[0] if "/" in rel(p) else "(root)"
            by_dir[parent].append(p)
        lines.append("| Directory | Pages affected |")
        lines.append("|---|---:|")
        for d_name in sorted(by_dir.keys()):
            lines.append(f"| `{d_name}/` | {len(by_dir[d_name])} |")
        lines.append("")

        if complex_files:
            lines.append(f"### Non-template heading issues ({len(complex_files)} pages)")
            lines.append("")
            for p in complex_files:
                d = headings[p]
                lines.append(f"#### `{rel(p)}`")
                for line, frm, to in d["skipped"]:
                    lines.append(f"- L{line}: skipped level (h{frm} -> h{to})")
                for (line,) in d["multiple_h1"]:
                    lines.append(f"- L{line}: extra <h1> (more than one on page)")
                for (line,) in d["demoted_h1_after"]:
                    lines.append(f"- L{line}: <h1> appears after a non-h1 heading (possible corruption)")
                for line, name in d["empty"]:
                    lines.append(f"- L{line}: <{name}> is empty (whitespace only)")
                for line, name, block in d["block_in_heading"]:
                    lines.append(f"- L{line}: <{name}> contains block element <{block}>")
                lines.append("")

    # ------- Alt-text issues -------
    lines.append("## Alt-text issues")
    lines.append("")

    def trunc(s: str, n: int = 80) -> str:
        s = s.replace("\n", " ").replace("\r", " ")
        if len(s) <= n:
            return s
        return s[: n - 1] + "..."

    # Missing alt
    missing = []
    for p, d in sorted(alts.items()):
        for line, src in d["missing_alt"]:
            missing.append((rel(p), line, src))
    lines.append(f"### Missing `alt` attribute ({len(missing)} total)")
    lines.append("")
    if not missing:
        lines.append("_None._")
    else:
        for f, line, src in missing[:200]:
            lines.append(f"- `{f}` L{line}: `{src}`")
        if len(missing) > 200:
            lines.append(f"- ... and {len(missing) - 200} more")
    lines.append("")

    # Empty alt inside <figure>
    empty_fig = []
    for p, d in sorted(alts.items()):
        for line, src in d["empty_in_figure"]:
            empty_fig.append((rel(p), line, src))
    lines.append(f"### Empty `alt=\"\"` inside `<figure>` ({len(empty_fig)} total)")
    lines.append("")
    if not empty_fig:
        lines.append("_None._")
    else:
        for f, line, src in empty_fig[:200]:
            lines.append(f"- `{f}` L{line}: `{src}`")
        if len(empty_fig) > 200:
            lines.append(f"- ... and {len(empty_fig) - 200} more")
    lines.append("")

    # Boilerplate
    boiler = []
    for p, d in sorted(alts.items()):
        for line, src, alt, reason in d["boilerplate"]:
            boiler.append((rel(p), line, src, alt, reason))
    lines.append(f"### Boilerplate alt text ({len(boiler)} total)")
    lines.append("")
    if not boiler:
        lines.append("_None._")
    else:
        for f, line, src, alt, reason in boiler[:200]:
            lines.append(f"- `{f}` L{line} [{reason}]: alt=\"{trunc(alt, 120)}\"")
        if len(boiler) > 200:
            lines.append(f"- ... and {len(boiler) - 200} more")
    lines.append("")

    # Too short
    short = []
    for p, d in sorted(alts.items()):
        for line, src, alt in d["too_short"]:
            short.append((rel(p), line, src, alt))
    lines.append(f"### Alt text too short (<8 chars, inside `<figure>`) ({len(short)} total)")
    lines.append("")
    if not short:
        lines.append("_None._")
    else:
        for f, line, src, alt in short[:200]:
            lines.append(f"- `{f}` L{line}: alt=\"{alt}\" src=`{src}`")
        if len(short) > 200:
            lines.append(f"- ... and {len(short) - 200} more")
    lines.append("")

    # Too long
    long_ = []
    for p, d in sorted(alts.items()):
        for line, src, alt_len in d["too_long"]:
            long_.append((rel(p), line, src, alt_len))
    lines.append(f"### Alt text too long (>250 chars) ({len(long_)} total)")
    lines.append("")
    if not long_:
        lines.append("_None._")
    else:
        for f, line, src, alt_len in long_[:200]:
            lines.append(f"- `{f}` L{line}: alt length = {alt_len} chars, src=`{src}`")
        if len(long_) > 200:
            lines.append(f"- ... and {len(long_) - 200} more")
    lines.append("")

    # ------- Worst-offender pages -------
    lines.append("## Worst-offender pages (3+ combined issues)")
    lines.append("")
    combined: list[tuple[Path, int, int, int]] = []
    for p in set(list(headings.keys()) + list(alts.keys())):
        h_count = count_total_issues(headings.get(p, {}))
        a_count = count_total_issues(alts.get(p, {}))
        total = h_count + a_count
        if total >= 3:
            combined.append((p, h_count, a_count, total))
    combined.sort(key=lambda r: (-r[3], rel(r[0])))
    if not combined:
        lines.append("_No pages with 3+ combined issues._")
    else:
        lines.append("| Page | Heading issues | Alt issues | Total |")
        lines.append("|---|---:|---:|---:|")
        for p, hc, ac, t in combined[:60]:
            lines.append(f"| `{rel(p)}` | {hc} | {ac} | {t} |")
        if len(combined) > 60:
            lines.append(f"\n_... and {len(combined) - 60} more pages._")
    lines.append("")

    # ------- Parse errors -------
    if parse_errors:
        lines.append("## Parse errors")
        lines.append("")
        for p, msg in parse_errors:
            lines.append(f"- `{rel(p)}`: {msg}")
        lines.append("")

    # ------- Recommended fix priority -------
    missing_total = sum(len(d["missing_alt"]) for d in alts.values())
    empty_fig_total = sum(len(d["empty_in_figure"]) for d in alts.values())
    boiler_total = sum(len(d["boilerplate"]) for d in alts.values())
    short_total = sum(len(d["too_short"]) for d in alts.values())
    long_total = sum(len(d["too_long"]) for d in alts.values())
    multi_h1_total = sum(len(d["multiple_h1"]) for d in headings.values())
    demoted_total = sum(len(d["demoted_h1_after"]) for d in headings.values())
    skipped_total = sum(len(d["skipped"]) for d in headings.values())
    empty_h_total = sum(len(d["empty"]) for d in headings.values())
    block_h_total = sum(len(d["block_in_heading"]) for d in headings.values())

    lines.append("## Recommended fix priority")
    lines.append("")
    raw_bullets: list[str] = []
    if missing_total:
        raw_bullets.append(
            f"**Add `alt` attributes to {missing_total} images** missing one entirely. "
            "Screen readers fall back to the filename and this is a WCAG 1.1.1 violation."
        )
    if demoted_total or multi_h1_total:
        raw_bullets.append(
            f"**Fix {multi_h1_total} multi-h1 and {demoted_total} demoted-h1 pages.** "
            "A second `<h1>` mid-document is almost always template corruption and should be downgraded to `<h2>`."
        )
    if empty_h_total or block_h_total:
        raw_bullets.append(
            f"**Repair {empty_h_total} empty headings and {block_h_total} headings containing block elements.** "
            "These usually indicate broken templating and should be reviewed by hand."
        )
    if skipped_total:
        raw_bullets.append(
            f"**Re-level {skipped_total} skipped-heading instances** (e.g. h1 -> h3). "
            "Fix at the section template by either inserting an `<h2>` chapter banner or "
            "demoting the section subheads from `<h3>` to `<h2>`."
        )
    if empty_fig_total:
        raw_bullets.append(
            f"**Replace empty `alt=\"\"` inside `<figure>` ({empty_fig_total} cases).** "
            "Figures are content; an empty alt tells the screen reader to skip a meaningful image."
        )
    if boiler_total or short_total:
        raw_bullets.append(
            f"**Rewrite {boiler_total} boilerplate and {short_total} ultra-short alts** "
            "with concrete descriptions. 'Image of X' and 'Diagram' add no information."
        )
    if long_total:
        raw_bullets.append(
            f"**Trim {long_total} overlong alts (>250 chars)** by moving detail to the figure caption."
        )
    if not raw_bullets:
        lines.append("_No actionable issues detected._")
    else:
        for i, b in enumerate(raw_bullets, 1):
            lines.append(f"{i}. {b}")
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
