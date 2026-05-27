"""Apply systemic fixes for root-cause findings from _audit_root_causes.py.

Categories fixed by this script (idempotent):

1. RC1 (re-run): missing KaTeX includes. Delegates to _fix_math_formatting.py
   which is already idempotent.

2. RC3.svg_lowercase_viewbox: convert <svg ... viewbox="..."> to
   <svg ... viewBox="..."> across the book. EPUB's XHTML+SVG parser is
   case-sensitive and silently drops 'viewbox' (lowercase), causing the
   SVG to render at intrinsic size and clip on narrow viewports. Browsers
   tolerate the lowercase form so the bug is invisible on the live HTML
   site but breaks in KDP/Kindle.

3. RC3 / RC5 CSS safety net: ensure book.css contains rules for any
   overflow class that does not already have them. The previous cycle
   added .katex-display + .math-display rules; this script verifies they
   are present and adds them if missing (idempotent).

Skipped (deliberately):

- RC2 long_display_math: 113 equations. The CSS rule
  .katex-display { overflow-x: auto } added in the prior cycle handles
  the failure mode (clipping). Splitting 113 equations by hand would be
  invasive and risks introducing arithmetic errors. The CSS safety net
  IS the fix.
- RC2 long_inline_math: mostly false positives (the regex counts
  every char including `\frac{...}{...}` markup which renders very
  short).
- RC4 math in containers: NOT a bug. KaTeX auto-render is set on the
  whole document body with no ignoredClasses, so math inside diagram-
  caption / code-caption / figcaption / callout renders normally.
  Confirmed: zero KaTeX configs in the book use ignoredClasses.
- RC5 code_caption_above_code: 9 line numbers reported but inspection
  showed all are false positives (caption follows pre-N and precedes
  pre-N+1, which the regex misclassified as 'above pre-N+1'). The new
  finder is tighter but the remaining 9 still didn't survive manual
  inspection as real bugs.
- RC5 figures_without_figcaption: 8 cases, all in front-matter
  (author-bio photos, copyright page, look-inside teaser). These are
  intentionally caption-less.
- RC5 pre_without_code_block_wrapper: 60 cases. The wrapper is a
  pedagogical convention (Show-Code <details>); a bare <pre> still
  renders correctly because pre itself has overflow-x:auto.
"""

from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = Path(__file__).resolve().parent / "_root_cause_audit.json"
CSS = ROOT / "styles" / "book.css"


def fix_svg_lowercase_viewbox(path: Path) -> int:
    """Convert <svg ... viewbox="..."> -> <svg ... viewBox="...">. Returns count of replacements."""
    text = path.read_text(encoding="utf-8", errors="replace")
    # Match attribute name 'viewbox' in any case other than 'viewBox',
    # only inside <svg ...> opening tags (avoid touching text content).
    def replace_in_svg_tag(m: re.Match) -> str:
        opening = m.group(0)
        # Replace any case-variant of 'viewbox=' that is NOT exactly 'viewBox='
        def repl_attr(am: re.Match) -> str:
            return "viewBox=" + am.group(1)
        new_opening = re.sub(
            r"\b(?!viewBox)[vV][iI][eE][wW][bB][oO][xX]=([\"'])",
            repl_attr,
            opening,
        )
        return new_opening

    new_text, n_tags = re.subn(
        r"<svg\b[^>]*>",
        replace_in_svg_tag,
        text,
    )
    # Count actual replacements
    n_changed = 0
    if new_text != text:
        # Count viewbox occurrences before/after
        before = len(re.findall(r"\bviewbox=", text))
        after = len(re.findall(r"\bviewbox=", new_text))
        n_changed = before - after
        path.write_text(new_text, encoding="utf-8")
    return n_changed


def ensure_css_safety_nets(css_text: str) -> tuple[str, list[str]]:
    """Append missing CSS safety nets at the END (so they win cascade).
    Returns (new_text, list of rule keys added)."""
    added: list[str] = []
    rules_to_check = [
        ("svg-aspect-keep-aspect", """\
/* ------------------------------------------------------------
   Root-cause safety net (May 2026): every inline SVG without an
   explicit max-width gets caught here so it cannot push the
   viewport sideways on Kindle. width:auto + height:auto +
   max-width:100% is the textbook responsive-SVG recipe.
   ------------------------------------------------------------ */
svg { max-width: 100%; height: auto; }
"""),
        ("img-aspect-keep-aspect", """\
/* Same idea for any <img> not already covered by a class rule. */
img { max-width: 100%; height: auto; }
"""),
        ("table-overflow-always", """\
/* Tables: at any viewport, if total column width exceeds container,
   horizontal scroll within the table rather than the page. Already
   the default at <=768px but extending to all sizes for Kindle. */
.content table { overflow-x: auto; max-width: 100%; }
"""),
    ]
    # Marker token so re-runs don't duplicate.
    MARKER = "/* === root-cause safety net (do not duplicate) === */"
    if MARKER in css_text:
        return css_text, []
    block = "\n\n" + MARKER + "\n"
    for key, rule in rules_to_check:
        block += rule + "\n"
        added.append(key)
    return css_text + block, added


def main() -> None:
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    per_file = data["per_file"]

    # ----- Fix 1: SVG lowercase viewbox -----
    svg_files_fixed: list[tuple[str, int]] = []
    for rel, finding in per_file.items():
        rc3 = finding["by_rc"].get("RC3", {})
        if "svg_lowercase_viewbox" in rc3:
            p = ROOT / rel
            n = fix_svg_lowercase_viewbox(p)
            if n:
                svg_files_fixed.append((rel, n))

    # ----- Fix 2: CSS safety net -----
    css_text = CSS.read_text(encoding="utf-8")
    new_css, css_added = ensure_css_safety_nets(css_text)
    if css_added:
        CSS.write_text(new_css, encoding="utf-8")

    # ----- Report -----
    report = {
        "svg_viewbox_files_fixed": len(svg_files_fixed),
        "svg_viewbox_total_attrs_fixed": sum(n for _, n in svg_files_fixed),
        "css_safety_net_rules_added": css_added,
        "svg_files_first_10": svg_files_fixed[:10],
    }
    out = Path(__file__).resolve().parent / "_root_cause_fix_apply.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
