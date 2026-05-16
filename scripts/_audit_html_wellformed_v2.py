"""HTML wellformedness audit v2.

Scope: all .html files under the book root EXCEPT KDP/, .claude/, temp_*,
scripts/, *backups*, node_modules/, pagefind/, templates/.

Phases:
  1. (delegated)  Run scripts/_fix_unclosed_headings.py separately first.
  2. AUTOFIX:     <br> -> <br/>  (confidence ~0.99).
  3. REPORT:      empty callouts, block-in-<p>, tag balance imbalances,
                  empty heading text, suspicious inline styles.

Writes the report to wellformedness-audit.md at the project root.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIR_NAMES = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    "build", ".git", "source_fix_backups", "__pycache__",
}
SKIP_PREFIXES = ("temp_",)
SKIP_NAME_FRAGMENTS = ("backups",)


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


# ----------------------------------------------------------------------
# Phase 2: <br> -> <br/> autofix
# ----------------------------------------------------------------------

# Match <br> exactly (allow optional whitespace before >), NOT <br/>, <br />,
# <br class="...">, etc. We want only the literal tag without attributes.
BR_RE = re.compile(r"<br\s*>", flags=re.IGNORECASE)


def fix_br_in_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(_m):
        nonlocal count
        count += 1
        return "<br/>"

    new_text = BR_RE.sub(repl, text)
    return new_text, count


def phase2_autofix_br(files: list[Path], dry_run: bool = False) -> dict[Path, int]:
    """Replace <br> with <br/> in all files. Return per-file counts."""
    results: dict[Path, int] = {}
    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new_text, n = fix_br_in_text(text)
        if n > 0:
            results[p] = n
            if not dry_run:
                # Validate parses cleanly before committing
                try:
                    BeautifulSoup(new_text, "html.parser")
                except Exception:
                    # Should be impossible for a textual substitution, but
                    # bail out defensively.
                    continue
                p.write_text(new_text, encoding="utf-8")
    return results


# ----------------------------------------------------------------------
# Phase 3 reporters
# ----------------------------------------------------------------------

BLOCK_TAGS_IN_P = {"div", "ul", "ol", "table", "blockquote", "figure",
                   "section", "article", "aside", "header", "footer", "nav",
                   "p", "h1", "h2", "h3", "h4", "h5", "h6", "pre",
                   "details", "dl"}

COUNT_TAGS = ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
              "ul", "ol", "li", "table", "tr", "td", "th",
              "figure", "span", "a", "code", "pre")


def line_of(element) -> int:
    """Return source line of a BS4 element, or 0 if unknown."""
    return getattr(element, "sourceline", 0) or 0


def report_empty_callouts(soup: BeautifulSoup) -> list[tuple[int, str, str]]:
    """Return list of (line, callout_class, surrounding_context_snippet)."""
    found = []
    for div in soup.find_all("div", class_="callout"):
        classes = div.get("class") or []
        cls_str = " ".join(classes)
        # Get children excluding whitespace text nodes
        body_children = [
            c for c in div.children
            if not (isinstance(c, str) and c.strip() == "")
        ]
        # Strip out the title div if present
        non_title = []
        for c in body_children:
            if getattr(c, "name", None) == "div":
                c_classes = c.get("class") or []
                if "callout-title" in c_classes:
                    continue
            non_title.append(c)
        # Check if body has actual content
        is_empty = False
        if not non_title:
            is_empty = True
        else:
            # Concatenate any text content
            text = "".join(
                (c.get_text(strip=True) if hasattr(c, "get_text") else str(c).strip())
                for c in non_title
            )
            if not text:
                is_empty = True
        if is_empty:
            line = line_of(div)
            # Build short context
            snippet = str(div)[:200].replace("\n", " ")
            found.append((line, cls_str, snippet))
    return found


def report_block_in_p(soup: BeautifulSoup) -> list[tuple[int, str]]:
    """Find <p> elements containing block-level descendants.

    Note: BS4's html.parser auto-corrects most of these on parse (it closes
    <p> when a block child is encountered). To catch the SOURCE problem we
    do a separate regex-based scan against raw text instead.
    """
    return []  # see regex-based scan in audit_file


P_BLOCK_RE = re.compile(
    r"<p\b[^>]*>(?:(?!</p>).)*?<(?:div|ul|ol|table|blockquote|figure|"
    r"section|article|aside|header|footer|nav|h[1-6]|pre|details|dl)\b",
    flags=re.IGNORECASE | re.DOTALL,
)


def report_block_in_p_regex(text: str) -> list[tuple[int, str]]:
    """Return list of (line, snippet) where a block element opens inside <p>."""
    found = []
    for m in P_BLOCK_RE.finditer(text):
        # Compute line number from offset
        line = text.count("\n", 0, m.start()) + 1
        snippet = text[m.start():m.start() + 120].replace("\n", " ")
        found.append((line, snippet))
    return found


def report_tag_balance(text: str) -> dict[str, tuple[int, int]]:
    """Return {tag: (opens, closes)} for tracked tags from raw text."""
    out: dict[str, tuple[int, int]] = {}
    for tag in COUNT_TAGS:
        # Opens: <tag> or <tag ...>, NOT </tag>, NOT <tag/>
        open_re = re.compile(rf"<{tag}\b(?![^>]*/>)[^>]*>", re.IGNORECASE)
        close_re = re.compile(rf"</{tag}\s*>", re.IGNORECASE)
        opens = len(open_re.findall(text))
        closes = len(close_re.findall(text))
        out[tag] = (opens, closes)
    return out


def report_empty_headings(soup: BeautifulSoup) -> list[tuple[int, str]]:
    found = []
    for level in range(1, 7):
        for h in soup.find_all(f"h{level}"):
            text = h.get_text(strip=True)
            if not text:
                line = line_of(h)
                found.append((line, str(h)[:120].replace("\n", " ")))
    return found


SUSPICIOUS_STYLE_RES = [
    (
        re.compile(
            r'<ul\b[^>]*style\s*=\s*"[^"]*text-align\s*:\s*center[^"]*"[^>]*>',
            re.IGNORECASE,
        ),
        "centered <ul> (bullets center-aligned, almost always wrong)",
    ),
    (
        re.compile(
            r'<ol\b[^>]*style\s*=\s*"[^"]*text-align\s*:\s*center[^"]*"[^>]*>',
            re.IGNORECASE,
        ),
        "centered <ol> (numbered list center-aligned, almost always wrong)",
    ),
]

# For centered <p>: only flag if it's inside a callout body. We use BS4 for
# this contextual check (regex can't reliably tell).


def report_suspicious_styles(text: str, soup: BeautifulSoup) -> list[tuple[int, str, str]]:
    """Return list of (line, style_description, snippet)."""
    found = []
    for pat, label in SUSPICIOUS_STYLE_RES:
        for m in pat.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            snippet = m.group(0)[:160]
            found.append((line, label, snippet))
    # Centered <p> inside a callout: high-confidence wrong.
    for p_tag in soup.find_all("p"):
        style = p_tag.get("style", "")
        if "text-align" in style and "center" in style:
            # Check if any ancestor div has class containing 'callout'
            for ancestor in p_tag.parents:
                ancestor_classes = ancestor.get("class") if hasattr(ancestor, "get") else None
                if ancestor_classes and any("callout" in c for c in ancestor_classes):
                    found.append((
                        line_of(p_tag),
                        "centered <p> inside a callout (body should be left-aligned)",
                        str(p_tag)[:160].replace("\n", " "),
                    ))
                    break
    return found


# ----------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------

def audit_file(p: Path):
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    try:
        soup = BeautifulSoup(text, "html.parser")
    except Exception as e:
        return {"parse_error": str(e)}

    return {
        "empty_callouts": report_empty_callouts(soup),
        "block_in_p": report_block_in_p_regex(text),
        "tag_balance": report_tag_balance(text),
        "empty_headings": report_empty_headings(soup),
        "suspicious_styles": report_suspicious_styles(text, soup),
    }


def validate_files_parse(files: list[Path]) -> list[Path]:
    """Return list of files that fail to parse cleanly."""
    failed = []
    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
            BeautifulSoup(text, "html.parser")
        except Exception:
            failed.append(p)
    return failed


def write_report(report_lines: list[str], out_path: Path) -> None:
    out_path.write_text("\n".join(report_lines), encoding="utf-8")


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Do not edit files for Phase 2.")
    ap.add_argument("--skip-phase2", action="store_true",
                    help="Skip the <br> -> <br/> autofix.")
    args = ap.parse_args()

    files = collect_html_files()
    print(f"Scanning {len(files)} HTML files...", file=sys.stderr)

    # ------------------------------------------------------------------
    # Phase 2: <br> -> <br/>
    # ------------------------------------------------------------------
    if args.skip_phase2:
        br_fixes: dict[Path, int] = {}
    else:
        br_fixes = phase2_autofix_br(files, dry_run=args.dry_run)
    total_br = sum(br_fixes.values())
    print(f"Phase 2: br fixes = {total_br} across {len(br_fixes)} file(s)",
          file=sys.stderr)

    # Re-validate that all (newly written) files still parse
    failed_parse = validate_files_parse(files)
    if failed_parse:
        print(f"WARNING: {len(failed_parse)} file(s) failed to parse after fix:",
              file=sys.stderr)
        for f in failed_parse:
            print(f"  {rel(f)}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Phase 3: report
    # ------------------------------------------------------------------
    all_empty_callouts: dict[Path, list] = {}
    all_block_in_p: dict[Path, list] = {}
    all_tag_imbalance: dict[Path, dict[str, tuple[int, int]]] = {}
    all_empty_headings: dict[Path, list] = {}
    all_suspicious: dict[Path, list] = {}
    parse_errors: dict[Path, str] = {}

    for p in files:
        result = audit_file(p)
        if result is None:
            continue
        if "parse_error" in result:
            parse_errors[p] = result["parse_error"]
            continue

        if result["empty_callouts"]:
            all_empty_callouts[p] = result["empty_callouts"]
        if result["block_in_p"]:
            all_block_in_p[p] = result["block_in_p"]
        # Compute imbalances only
        imbal = {
            t: (o, c) for t, (o, c) in result["tag_balance"].items()
            if o != c
        }
        if imbal:
            all_tag_imbalance[p] = imbal
        if result["empty_headings"]:
            all_empty_headings[p] = result["empty_headings"]
        if result["suspicious_styles"]:
            all_suspicious[p] = result["suspicious_styles"]

    # ------------------------------------------------------------------
    # Build markdown report
    # ------------------------------------------------------------------
    out: list[str] = []
    out.append("# HTML Wellformedness Audit")
    out.append("")
    out.append(f"Generated by `scripts/_audit_html_wellformed_v2.py`. "
               f"Scope: {len(files)} HTML files.")
    out.append("")

    # ------ Summary table
    out.append("## 1. Summary")
    out.append("")
    out.append("| Category | Auto-fixed | Reported |")
    out.append("|---|---:|---:|")
    # Category 1 (unclosed headings) is handled by _fix_unclosed_headings.py.
    # We report its outcome based on whether anything was fixed on this run.
    # Since the user runs Phase 1 separately, we just note the script ran.
    out.append(f"| 1. Unclosed headings (h1-h6) | (see _fix_unclosed_headings.py) | - |")
    out.append(f"| 2. Empty callouts | - | {sum(len(v) for v in all_empty_callouts.values())} "
               f"across {len(all_empty_callouts)} file(s) |")
    out.append(f"| 3. Block-level inside `<p>` | - | {sum(len(v) for v in all_block_in_p.values())} "
               f"across {len(all_block_in_p)} file(s) |")
    out.append(f"| 4. Tag balance imbalances | - | {len(all_tag_imbalance)} file(s) |")
    out.append(f"| 5. Empty heading text | - | {sum(len(v) for v in all_empty_headings.values())} "
               f"across {len(all_empty_headings)} file(s) |")
    out.append(f"| 6. Suspicious inline styles | - | {sum(len(v) for v in all_suspicious.values())} "
               f"across {len(all_suspicious)} file(s) |")
    out.append(f"| 7. `<br>` -> `<br/>` | {total_br} across {len(br_fixes)} file(s) | - |")
    out.append("")
    if parse_errors:
        out.append(f"**Parse errors:** {len(parse_errors)} file(s) failed to parse.")
        out.append("")

    # ------ Phase 2 auto-fix details
    out.append("## 2. Auto-fixed: `<br>` -> `<br/>`")
    out.append("")
    if br_fixes:
        out.append(f"Replaced {total_br} bare `<br>` with `<br/>` in "
                   f"{len(br_fixes)} file(s).")
        out.append("")
        out.append("| File | Count |")
        out.append("|---|---:|")
        for p in sorted(br_fixes, key=lambda x: (-br_fixes[x], rel(x))):
            out.append(f"| `{rel(p)}` | {br_fixes[p]} |")
        out.append("")
    else:
        out.append("None found.")
        out.append("")

    # ------ Empty callouts
    out.append("## 3. Empty callouts (REPORT-ONLY)")
    out.append("")
    if all_empty_callouts:
        out.append(f"Found {sum(len(v) for v in all_empty_callouts.values())} "
                   f"empty callout(s) across {len(all_empty_callouts)} file(s).")
        out.append("")
        # Limit to ~40 entries to keep report short.
        shown = 0
        for p in sorted(all_empty_callouts, key=rel):
            for (line, cls, snippet) in all_empty_callouts[p]:
                if shown >= 60:
                    break
                out.append(f"- `{rel(p)}:{line}` class=`{cls}`")
                out.append(f"  - `{snippet}`")
                shown += 1
            if shown >= 60:
                break
        total = sum(len(v) for v in all_empty_callouts.values())
        if shown < total:
            out.append(f"")
            out.append(f"...and {total - shown} more (truncated).")
        out.append("")
    else:
        out.append("None found.")
        out.append("")

    # ------ Block-in-<p>
    out.append("## 4. Block-level inside `<p>` (REPORT-ONLY)")
    out.append("")
    if all_block_in_p:
        total = sum(len(v) for v in all_block_in_p.values())
        out.append(f"Found {total} occurrence(s) across "
                   f"{len(all_block_in_p)} file(s). Showing first 5 per file.")
        out.append("")
        out.append("| File | Count | First 5 line(s) |")
        out.append("|---|---:|---|")
        for p in sorted(all_block_in_p, key=lambda x: -len(all_block_in_p[x])):
            entries = all_block_in_p[p]
            first5 = ", ".join(str(line) for (line, _) in entries[:5])
            out.append(f"| `{rel(p)}` | {len(entries)} | {first5} |")
        out.append("")
    else:
        out.append("None found.")
        out.append("")

    # ------ Tag balance imbalances
    out.append("## 5. Tag balance imbalances (REPORT-ONLY)")
    out.append("")
    if all_tag_imbalance:
        # Rank files by sum of |imbalance| across tags
        ranked = sorted(
            all_tag_imbalance.items(),
            key=lambda kv: -sum(abs(o - c) for (o, c) in kv[1].values()),
        )
        out.append(f"Showing top 15 of {len(all_tag_imbalance)} file(s) with "
                   f"any imbalance for the tracked set "
                   f"({', '.join(COUNT_TAGS)}). "
                   f"Note: HTML5 makes closing tags optional for "
                   f"`p`/`li`/`option`/`td`/`tr`/`th`, so imbalances in "
                   f"those are commonly benign.")
        out.append("")
        out.append("| File | Worst tag | Opens | Closes | Skew | Other imbalanced tags |")
        out.append("|---|---|---:|---:|---:|---|")
        for p, imbal in ranked[:15]:
            worst_tag = max(imbal, key=lambda t: abs(imbal[t][0] - imbal[t][1]))
            o, c = imbal[worst_tag]
            skew = c - o
            sign = "+" if skew > 0 else ""
            others = [
                f"{t}({oo}/{cc})"
                for t, (oo, cc) in imbal.items() if t != worst_tag
            ]
            out.append(f"| `{rel(p)}` | `{worst_tag}` | {o} | {c} | "
                       f"{sign}{skew} | "
                       f"{', '.join(others) if others else '-'} |")
        out.append("")
        # Highlight files with structural concerns: imbalance in heading or
        # container tags is more interesting than e.g. <p>.
        STRUCTURAL = ("h1", "h2", "h3", "h4", "h5", "h6", "div", "table",
                      "figure", "pre", "code", "ul", "ol")
        structural_issues = []
        for p, imbal in all_tag_imbalance.items():
            for tag, (o, c) in imbal.items():
                if tag in STRUCTURAL:
                    structural_issues.append((rel(p), tag, o, c))
        if structural_issues:
            out.append("### Structural imbalances (higher concern)")
            out.append("")
            out.append("Imbalances in heading/container tags often signal "
                       "real corruption. Closing tags exceeding opens is "
                       "particularly suspicious -- stray `</tag>` strings "
                       "that the parser will try to match against unrelated "
                       "opens, or were left behind by an earlier fix.")
            out.append("")
            out.append("| File | Tag | Opens | Closes | Skew |")
            out.append("|---|---|---:|---:|---:|")
            for fpath, tag, o, c in sorted(
                structural_issues, key=lambda x: -abs(x[2] - x[3])
            ):
                skew = c - o
                sign = "+" if skew > 0 else ""
                out.append(f"| `{fpath}` | `{tag}` | {o} | {c} | {sign}{skew} |")
            out.append("")
    else:
        out.append("None found.")
        out.append("")

    # ------ Empty heading text
    out.append("## 6. Empty heading text (REPORT-ONLY)")
    out.append("")
    if all_empty_headings:
        total = sum(len(v) for v in all_empty_headings.values())
        out.append(f"Found {total} empty heading(s) across "
                   f"{len(all_empty_headings)} file(s).")
        out.append("")
        for p in sorted(all_empty_headings, key=rel):
            for (line, snippet) in all_empty_headings[p]:
                out.append(f"- `{rel(p)}:{line}` -- `{snippet}`")
        out.append("")
    else:
        out.append("None found.")
        out.append("")

    # ------ Suspicious inline styles
    out.append("## 7. Suspicious inline styles (REPORT-ONLY)")
    out.append("")
    if all_suspicious:
        total = sum(len(v) for v in all_suspicious.values())
        out.append(f"Found {total} occurrence(s) across "
                   f"{len(all_suspicious)} file(s). Showing up to 60 entries.")
        out.append("")
        shown = 0
        for p in sorted(all_suspicious, key=rel):
            for (line, label, snippet) in all_suspicious[p]:
                if shown >= 60:
                    break
                out.append(f"- `{rel(p)}:{line}` -- {label}")
                out.append(f"  - `{snippet}`")
                shown += 1
            if shown >= 60:
                break
        if shown < total:
            out.append("")
            out.append(f"...and {total - shown} more (truncated).")
        out.append("")
    else:
        out.append("None found.")
        out.append("")

    # ------ Parse errors
    if parse_errors:
        out.append("## 8. Parse errors")
        out.append("")
        for p, err in parse_errors.items():
            out.append(f"- `{rel(p)}` -- {err}")
        out.append("")

    # ------ Recommendations
    out.append("## 9. Recommended fix priority")
    out.append("")
    bullets = []

    if total_br > 0:
        bullets.append(
            f"**Done.** `<br>` -> `<br/>` autofix applied: {total_br} replacement(s) "
            f"in {len(br_fixes)} file(s)."
        )
    if all_empty_callouts:
        n_files = len(all_empty_callouts)
        bullets.append(
            f"**High priority:** empty callouts in {n_files} file(s) likely "
            "lost body content during a build regression. Inspect each and "
            "restore the body paragraph(s) or delete the empty wrapper."
        )
    if all_block_in_p:
        bullets.append(
            f"**Medium priority:** block-in-`<p>` in "
            f"{len(all_block_in_p)} file(s) is invalid HTML5. Browsers "
            "silently close the `<p>` before the block; rewriting the source "
            "to wrap the block outside the paragraph eliminates the warning."
        )
    if all_tag_imbalance:
        # Compute structural-only count to make the priority concrete.
        STRUCTURAL = ("h1", "h2", "h3", "h4", "h5", "h6", "div", "table",
                      "figure", "pre", "code", "ul", "ol")
        structural_files = [
            rel(p) for p, imbal in all_tag_imbalance.items()
            if any(t in STRUCTURAL for t in imbal)
        ]
        if structural_files:
            bullets.append(
                f"**High priority:** {len(structural_files)} file(s) have "
                "structural-tag imbalance (heading/container). These are "
                "frequently real corruption (stray close tags left behind "
                "by an earlier botched fix, missing opens, etc.). Inspect "
                "the 'Structural imbalances' subsection of Section 5 of this "
                "report and remove or restore tags accordingly."
            )
        else:
            bullets.append(
                f"**Medium priority:** {len(all_tag_imbalance)} file(s) show tag "
                "open/close imbalance. Common false positives: `p`/`li`/`option` "
                "(optional close tags in HTML5). Real risk is for `div`, `table`, "
                "`figure`, `pre`, `code` -- inspect the top of the table first."
            )
    if all_empty_headings:
        bullets.append(
            f"**Low priority:** {sum(len(v) for v in all_empty_headings.values())} "
            "empty heading(s) -- decide whether to add a title or remove the heading."
        )
    if all_suspicious:
        bullets.append(
            f"**Low priority:** {sum(len(v) for v in all_suspicious.values())} "
            "suspicious inline-style occurrence(s). Most are callout bodies "
            "where centered text is probably wrong. Review case by case."
        )
    if parse_errors:
        bullets.insert(0, f"**Critical:** {len(parse_errors)} file(s) fail to parse.")

    if not bullets:
        bullets.append("No issues found.")

    for b in bullets:
        out.append(f"- {b}")
    out.append("")

    # Write report
    report_path = ROOT / "wellformedness-audit.md"
    write_report(out, report_path)
    print(f"Report written to: {report_path}", file=sys.stderr)
    print(f"Phase 2 autofix: br -> br/ = {total_br} replacement(s) in "
          f"{len(br_fixes)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
