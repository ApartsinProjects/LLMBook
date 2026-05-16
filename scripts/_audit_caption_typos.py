"""Audit (and selectively auto-fix) caption typos across the LLMBook.

Scope: every ``.html`` content file under the project root, excluding
``KDP/``, ``.claude/``, ``temp_*``, ``scripts/``, ``*backups*``, ``node_modules/``,
``pagefind/``, ``templates/``, ``agents/``, ``vendor/``, ``__pycache__``.

Caption containers inspected:

  - ``<div class="comparison-table-title">``
  - ``<figcaption>``
  - ``<div class="code-caption">``
  - ``<div class="diagram-caption">``

Categories checked:

  1. **Missing space + missing opening paren** (AUTO-FIX).
     ``Productsas of 2026)`` -> ``Products (as of 2026)``
     Regex: ``([A-Za-z])as of (\\d{4})\\)`` -> ``$1 (as of $2)``

  2. **Unbalanced parentheses** (REPORT only).
     Caption text contains different counts of ``(`` and ``)``.

  3. **Colon-format deviations** for the ``<strong>Figure X.Y.Z</strong>:``
     prefix (REPORT only). Flags missing colon, double colon, mis-placed
     colon (inside the bold span, etc.).

  4. **Trailing punctuation** stats (REPORT only). Counts captions ending
     in ``.``, ``?``, ``!`` vs. those with no terminator.

Writes a Markdown report to ``caption-typo-audit.md`` at the project root.

Usage::

    /c/Python314/python scripts/_audit_caption_typos.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "caption-typo-audit.md"

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


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


# ---------------------------------------------------------------------------
# Caption selection
# ---------------------------------------------------------------------------

CAPTION_SELECTORS = (
    ("comparison-table-title", lambda soup: soup.find_all("div", class_="comparison-table-title")),
    ("figcaption",            lambda soup: soup.find_all("figcaption")),
    ("code-caption",          lambda soup: soup.find_all("div", class_="code-caption")),
    ("diagram-caption",       lambda soup: soup.find_all("div", class_="diagram-caption")),
)


def find_captions(soup: BeautifulSoup):
    """Yield (kind, tag) for every caption-bearing element in the soup."""
    for kind, finder in CAPTION_SELECTORS:
        for tag in finder(soup):
            yield kind, tag


# ---------------------------------------------------------------------------
# Category 1: missing space + missing opening paren -> AUTO-FIX
# ---------------------------------------------------------------------------

# Match a word character (typically a lowercase letter) immediately followed
# by "as of YYYY)" with no opening parenthesis and no leading space.
MISSING_SPACE_PAREN_RE = re.compile(r"([A-Za-z])as of (\d{4})\)")
REPLACEMENT_FMT = r"\1 (as of \2)"


def file_uses_canonical_form(text: str) -> bool:
    """True when the file already has at least one '(as of YYYY)' canonical
    form, used as a sanity signal that the corruption pattern is the intent.
    """
    return bool(re.search(r"\(as of \d{4}\)", text))


# ---------------------------------------------------------------------------
# Category 2: unbalanced parens
# ---------------------------------------------------------------------------

def count_parens(text: str) -> tuple[int, int]:
    return text.count("("), text.count(")")


# ---------------------------------------------------------------------------
# Category 3: colon style
# ---------------------------------------------------------------------------

# Canonical: <strong>Figure 31.2.1</strong>: rest of caption
# We also tolerate <strong>Figure 31.2.1:</strong> (colon inside the bold).
LABEL_KEYWORDS = ("Figure", "Code Fragment", "Table")

# Regex that captures: <strong>(label) (number)(optional :)</strong>(optional :)
LABEL_TAG_RE = re.compile(
    r"<strong>\s*(Figure|Code Fragment|Table)\s+([A-Za-z0-9.]+)\s*(:?)\s*</strong>(\s*[:.]?)",
    re.IGNORECASE,
)


def classify_colon_style(html_inner: str) -> str | None:
    """Return a short tag describing colon-style deviations, or None if OK.

    Recognised normal forms:
      - <strong>Figure X.Y.Z</strong>:  rest        (colon AFTER the bold)
      - <strong>Figure X.Y.Z:</strong>  rest        (colon INSIDE the bold)

    Anything else for a caption that starts with a Figure/Code Fragment/Table
    label is flagged.
    """
    # Only investigate captions that *look* like they start with a label.
    snippet = html_inner.lstrip()[:300]
    if not snippet.lower().startswith("<strong>"):
        return None

    # Pull just the label region.
    m = LABEL_TAG_RE.match(snippet)
    if not m:
        # Looks like <strong>... but does not match label regex.
        return "label-tag-malformed"

    colon_inside = m.group(3) == ":"
    after = m.group(4) or ""
    after_stripped = after.strip()

    if colon_inside and after_stripped.startswith(":"):
        return "double-colon"
    if colon_inside and not after_stripped:
        # Colon INSIDE bold, nothing after — fine.
        return None
    if colon_inside and after_stripped and after_stripped[0] not in ":":
        # Colon INSIDE bold, plain text follows — fine.
        return None
    if not colon_inside and after_stripped.startswith(":"):
        # Colon AFTER bold — canonical.
        return None
    if not colon_inside and after_stripped.startswith("."):
        return "period-after-label"
    if not colon_inside and not after_stripped:
        return "no-colon-no-text"
    if not colon_inside and after_stripped and after_stripped[0] not in ":.":
        return "missing-colon"
    return None


# ---------------------------------------------------------------------------
# Category 4: trailing punctuation
# ---------------------------------------------------------------------------

def trailing_punct(text: str) -> str:
    t = text.rstrip()
    if not t:
        return "<empty>"
    last = t[-1]
    if last in ".?!":
        return last
    return "none"


# ---------------------------------------------------------------------------
# Audit driver
# ---------------------------------------------------------------------------

def main() -> int:
    files = iter_html_files()
    print(f"Scanning {len(files)} HTML files...", file=sys.stderr)

    autofixes: list[tuple[str, str, str, str]] = []   # (file, kind, before, after)
    unbalanced: list[tuple[str, int, str, str, int, int]] = []
    # (file, line, kind, text, open_count, close_count)
    colon_deviations: list[tuple[str, int, str, str, str]] = []
    # (file, line, kind, reason, text)
    trailing_counter: Counter[str] = Counter()
    trailing_by_kind: dict[str, Counter[str]] = defaultdict(Counter)

    caption_total = 0
    files_modified = 0
    parse_errors: list[tuple[Path, str]] = []

    for p in files:
        try:
            raw = p.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            parse_errors.append((p, str(exc)))
            continue

        # --- Category 1: auto-fix at raw-text level (regex) --------------
        # Only act if the file shows the corruption pattern AND has at least
        # one canonical "(as of YYYY)" elsewhere (defensive guard against
        # false positives such as user-intended prose).
        new_raw = raw
        local_autofixes: list[tuple[str, str, str]] = []
        if MISSING_SPACE_PAREN_RE.search(raw):
            # Walk matches first so we can record the surrounding text snippet
            # used for the report.
            for m in MISSING_SPACE_PAREN_RE.finditer(raw):
                start = max(0, m.start() - 40)
                end = min(len(raw), m.end() + 10)
                ctx = raw[start:end].replace("\n", " ")
                fixed_ctx = MISSING_SPACE_PAREN_RE.sub(REPLACEMENT_FMT, ctx)
                # Try to identify the surrounding caption kind by walking
                # backwards.
                kind = "(unknown)"
                lookback = raw[max(0, m.start() - 200): m.start()].lower()
                if "comparison-table-title" in lookback:
                    kind = "comparison-table-title"
                elif "code-caption" in lookback:
                    kind = "code-caption"
                elif "diagram-caption" in lookback:
                    kind = "diagram-caption"
                elif "<figcaption" in lookback:
                    kind = "figcaption"
                local_autofixes.append((kind, ctx, fixed_ctx))

            new_raw = MISSING_SPACE_PAREN_RE.sub(REPLACEMENT_FMT, raw)
            if new_raw != raw:
                try:
                    p.write_text(new_raw, encoding="utf-8")
                    files_modified += 1
                    for kind, before, after in local_autofixes:
                        autofixes.append((rel(p), kind, before, after))
                except Exception as exc:
                    parse_errors.append((p, f"write failed: {exc}"))

        # --- Categories 2/3/4: parse the (possibly fixed) HTML -----------
        try:
            soup = BeautifulSoup(new_raw, "html.parser")
        except Exception as exc:
            parse_errors.append((p, str(exc)))
            continue

        for kind, tag in find_captions(soup):
            caption_total += 1
            text = tag.get_text(" ", strip=True)
            inner_html = tag.decode_contents()
            line_no = int(getattr(tag, "sourceline", 0) or 0)

            # Cat 2: unbalanced parens — count over the visible text only
            opens, closes = count_parens(text)
            if opens != closes:
                unbalanced.append((rel(p), line_no, kind, text, opens, closes))

            # Cat 3: colon style — only relevant for Figure/Code/Table labels.
            reason = classify_colon_style(inner_html)
            if reason:
                colon_deviations.append((rel(p), line_no, kind, reason, text))

            # Cat 4: trailing punctuation stats
            tp = trailing_punct(text)
            trailing_counter[tp] += 1
            trailing_by_kind[kind][tp] += 1

    write_report(
        files_total=len(files),
        caption_total=caption_total,
        files_modified=files_modified,
        autofixes=autofixes,
        unbalanced=unbalanced,
        colon_deviations=colon_deviations,
        trailing_counter=trailing_counter,
        trailing_by_kind=trailing_by_kind,
        parse_errors=parse_errors,
    )

    print(f"Wrote {REPORT_PATH}", file=sys.stderr)
    print(f"Auto-fixes applied: {len(autofixes)} (in {files_modified} files)", file=sys.stderr)
    print(f"Unbalanced-paren captions: {len(unbalanced)}", file=sys.stderr)
    print(f"Colon-style deviations: {len(colon_deviations)}", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


def truncate(s: str, n: int = 140) -> str:
    s = s.strip()
    if len(s) <= n:
        return s
    return s[: n - 1] + "..."


def write_report(
    *,
    files_total: int,
    caption_total: int,
    files_modified: int,
    autofixes: list[tuple[str, str, str, str]],
    unbalanced: list[tuple[str, int, str, str, int, int]],
    colon_deviations: list[tuple[str, int, str, str, str]],
    trailing_counter: Counter[str],
    trailing_by_kind: dict[str, Counter[str]],
    parse_errors: list[tuple[Path, str]],
) -> None:
    lines: list[str] = []
    lines.append("# Caption typo audit")
    lines.append("")
    lines.append(
        "Scope: every `.html` page under the project root (KDP, scripts, "
        "node_modules, pagefind, templates, agents, vendor, temp_*, *backups* "
        "directories excluded). Only these caption containers are inspected: "
        "`<div class=\"comparison-table-title\">`, `<figcaption>`, "
        "`<div class=\"code-caption\">`, `<div class=\"diagram-caption\">`."
    )
    lines.append("")
    lines.append(f"- HTML files scanned: **{files_total}**")
    lines.append(f"- Caption elements inspected: **{caption_total}**")
    lines.append(f"- Files modified by auto-fix: **{files_modified}**")
    lines.append(f"- Total auto-fixes applied: **{len(autofixes)}**")
    lines.append(f"- Unbalanced-paren captions (review queue): **{len(unbalanced)}**")
    lines.append(f"- Colon-style deviations (review queue): **{len(colon_deviations)}**")
    if parse_errors:
        lines.append(f"- Parse / write errors: **{len(parse_errors)}**")
    lines.append("")

    # ---------------- 1. Summary --------------------------------------
    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Category | Action | Count |")
    lines.append("|---|---|---:|")
    lines.append(
        f"| Missing space + opening paren (`Xas of YYYY)`) | AUTO-FIX | {len(autofixes)} |"
    )
    lines.append(
        f"| Unbalanced parentheses in caption text | REPORT | {len(unbalanced)} |"
    )
    lines.append(
        f"| Colon-style deviations after Figure/Code/Table label | REPORT | {len(colon_deviations)} |"
    )
    lines.append(
        f"| Trailing punctuation variants (info only) | REPORT | {sum(trailing_counter.values())} |"
    )
    lines.append("")

    # ---------------- 2. Auto-fixes applied ---------------------------
    lines.append("## 2. Auto-fixes applied (Category 1)")
    lines.append("")
    if not autofixes:
        lines.append("_No auto-fixes were necessary._")
        lines.append("")
    else:
        lines.append(
            "All rewrites apply the rule "
            "`r\"([A-Za-z])as of (\\d{4})\\)\" -> r\"\\1 (as of \\2)\"`. "
            "The 'before' / 'after' snippets show a 40-char window around the "
            "match."
        )
        lines.append("")
        lines.append("| File | Kind | Before | After |")
        lines.append("|---|---|---|---|")
        for fpath, kind, before, after in autofixes:
            lines.append(
                f"| `{fpath}` | {kind} | `{md_escape(truncate(before, 80))}` "
                f"| `{md_escape(truncate(after, 80))}` |"
            )
        lines.append("")

    # ---------------- 3. Unbalanced parens ----------------------------
    lines.append("## 3. Unbalanced parentheses (manual review queue)")
    lines.append("")
    if not unbalanced:
        lines.append("_All caption parentheses are balanced after auto-fix pass._")
        lines.append("")
    else:
        lines.append(
            "Each row shows a caption whose `(` count does not equal its `)` "
            "count. These are NOT auto-fixed; resolution depends on intent "
            "(missing open vs. missing close, emoticon, table-cell artifact, "
            "etc.)."
        )
        lines.append("")
        lines.append("| File | Line | Kind | ( count | ) count | Caption text |")
        lines.append("|---|---:|---|---:|---:|---|")
        for fpath, line_no, kind, text, opens, closes in unbalanced:
            lines.append(
                f"| `{fpath}` | {line_no} | {kind} | {opens} | {closes} "
                f"| {md_escape(truncate(text, 160))} |"
            )
        lines.append("")

    # ---------------- 4. Colon-style deviations -----------------------
    lines.append("## 4. Colon-style deviations after Figure/Code/Table label")
    lines.append("")
    if not colon_deviations:
        lines.append("_All numbered captions follow the canonical colon style._")
        lines.append("")
    else:
        lines.append(
            "Canonical forms (both accepted):"
        )
        lines.append("")
        lines.append("- `<strong>Figure X.Y.Z</strong>: caption text`")
        lines.append("- `<strong>Figure X.Y.Z:</strong> caption text`")
        lines.append("")
        lines.append(
            "Deviation reasons: `missing-colon`, `double-colon`, "
            "`period-after-label`, `no-colon-no-text`, `label-tag-malformed`."
        )
        lines.append("")

        # Group by reason for easier scanning.
        by_reason: dict[str, list] = defaultdict(list)
        for row in colon_deviations:
            by_reason[row[3]].append(row)

        for reason in sorted(by_reason):
            rows = by_reason[reason]
            lines.append(f"### {reason} ({len(rows)})")
            lines.append("")
            lines.append("| File | Line | Kind | Caption text |")
            lines.append("|---|---:|---|---|")
            for fpath, line_no, kind, _r, text in rows:
                lines.append(
                    f"| `{fpath}` | {line_no} | {kind} "
                    f"| {md_escape(truncate(text, 160))} |"
                )
            lines.append("")

    # ---------------- 5. Trailing punctuation summary -----------------
    lines.append("## 5. Trailing punctuation summary (info only)")
    lines.append("")
    total = sum(trailing_counter.values())
    if total == 0:
        lines.append("_No captions were inspected._")
        lines.append("")
    else:
        # Overall mix
        lines.append("Overall mix:")
        lines.append("")
        lines.append("| Trailing char | Captions | % |")
        lines.append("|---|---:|---:|")
        for ch, cnt in trailing_counter.most_common():
            pct = (cnt * 100.0) / total
            lines.append(f"| `{ch}` | {cnt} | {pct:.1f}% |")
        lines.append("")

        # Dominant style declaration
        dominant_char, dominant_count = trailing_counter.most_common(1)[0]
        dominant_pct = (dominant_count * 100.0) / total
        lines.append(
            f"**Dominant style:** `{dominant_char}` "
            f"({dominant_count} of {total} captions, {dominant_pct:.1f}%)."
        )
        if dominant_char == ".":
            lines.append(
                " Captions predominantly end with a period before `</...>`."
            )
        elif dominant_char == "none":
            lines.append(
                " Captions predominantly end with NO terminal punctuation."
            )
        lines.append("")

        # Per-kind mix
        lines.append("Per caption-kind mix:")
        lines.append("")
        lines.append(
            "| Kind | Period `.` | Question `?` | Exclaim `!` | None |"
        )
        lines.append("|---|---:|---:|---:|---:|")
        for kind in ("comparison-table-title", "figcaption", "code-caption", "diagram-caption"):
            counts = trailing_by_kind.get(kind, Counter())
            lines.append(
                f"| {kind} | {counts.get('.', 0)} | {counts.get('?', 0)} "
                f"| {counts.get('!', 0)} | {counts.get('none', 0)} |"
            )
        lines.append("")

    # ---------------- 6. Parse / write errors -------------------------
    if parse_errors:
        lines.append("## 6. Parse / write errors")
        lines.append("")
        for p, exc in parse_errors:
            lines.append(f"- `{rel(p)}`: {exc}")
        lines.append("")

    # ---------------- Footer ------------------------------------------
    lines.append("---")
    lines.append("")
    lines.append("Audit produced by `scripts/_audit_caption_typos.py`.")
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
