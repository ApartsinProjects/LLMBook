"""Focused demo: HTML math in three placement contexts.

After the line-break feedback, this script produces a tight, focused
demo of plain-HTML math in exactly three contexts:

    1. INLINE - math threaded through running prose (must NOT wrap)
    2. DISPLAY - math on its own centered line (also must NOT wrap)
    3. TABLE  - math inside <td> cells (must fit cell, no overflow)

The same set of three expressions runs through each variant so you can
visually verify identical math behaves identically across placements.

Outputs to .claude/skills/math2epub/examples/demo-output/:
    math-variants.html  (browser baseline)
    math-variants.epub  (Kindle Previewer 3 baseline)

Run from anywhere:
    python .claude/skills/math2epub/examples/html_variants_demo.py
"""
from __future__ import annotations

import sys
import uuid
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from html_math import (  # noqa: E402
    HTML_MATH_CSS,
    GREEK,
    var, op, frac, hat, bar, vec, sqrt,
    summation, integral,
    inline, display, sub, sup,
)

# Write to the project's main output folder when running inside the
# LLMBook repo (alongside `building-conversational-ai-llms-agents.epub`),
# otherwise fall back to a local demo-output subdir for standalone use.
def _resolve_out_dir() -> Path:
    candidate = HERE
    for _ in range(6):
        if (candidate / "KDP" / "output").is_dir():
            return candidate / "KDP" / "output"
        candidate = candidate.parent
    return HERE / "demo-output"

OUT_DIR = _resolve_out_dir()
OUT_DIR.mkdir(parents=True, exist_ok=True)


# Same six expressions, used in every variant. Tagged with a one-word label.
EXPRS = [
    ("y_i",
     var("y", sub="i"),
     "Simple subscript: italic variable with italic subscript."),
    ("x^2",
     var("x", sup="2"),
     "Simple superscript: italic variable with superscript exponent."),
    ("y_hat_i",
     hat(var("y")) + sub("i"),
     "Combination: hat over variable, then subscript."),
    ("MSE",
     op("MSE") + " = " + frac("1", var("n")) + " "
     + summation(low=f"{var('i')}=1", high=var("n")) + " ("
     + hat(var("y")) + sub("i") + " &#8722; "
     + var("y", sub="i") + ")" + sup("2"),
     "Full MSE expression: operator name, fraction, summation with limits, subtraction, hat, sub, sup."),
    ("sigma(z)",
     GREEK["sigma"] + "(" + var("z") + ") = "
     + frac("1", "1 + " + var("e") + sup("&#8722;" + var("z"))),
     "Sigmoid expression: Greek letter, fraction, exponent with negative."),
    ("integral",
     integral(low="&#8722;" + GREEK["pi"], high=GREEK["pi"]) + " "
     + var("f") + "(" + var("x") + ") " + var("dx"),
     "Integral with stacked limits: hi/lo float above/below the integral glyph."),
]


# ============================================================================
# Variant 1: INLINE (math threaded through prose paragraphs)
# ============================================================================
def section_inline() -> str:
    parts = ["<h2>1. Inline math</h2>",
             "<p>Math threaded through running prose paragraphs. Each expression "
             "is wrapped in <code>&lt;span class=&quot;math-inline&quot;&gt;</code>, "
             "which uses <code>display:inline-block; white-space:nowrap</code> "
             "so the entire expression stays together as one atom even if the "
             "surrounding line wraps.</p>"]
    for tag, expr, note in EXPRS:
        parts.append(
            f'<p><strong>{tag}.</strong> '
            f'In context: the residual {inline(expr)} captures what we are '
            f'measuring, and we usually report it across many examples. '
            f'<em>{note}</em></p>'
        )
    return "\n".join(parts)


# ============================================================================
# Variant 2: DISPLAY (each expression on its own centered line)
# ============================================================================
def section_display() -> str:
    parts = ["<h2>2. Display math (separate line)</h2>",
             "<p>Each expression rendered as a centered block on its own line. "
             "<code>.math-display</code> uses <code>white-space:nowrap; "
             "overflow-x:auto</code>, so a too-wide equation gets a horizontal "
             "scrollbar instead of breaking mid-formula.</p>"]
    for tag, expr, note in EXPRS:
        parts.append(
            f'<p><strong>{tag}:</strong> {note}</p>\n'
            f'{display(expr)}'
        )
    return "\n".join(parts)


# ============================================================================
# Variant 3: TABLE (math inside <td> cells)
# ============================================================================
def section_table() -> str:
    rows = []
    for tag, expr, note in EXPRS:
        rows.append(
            f'<tr><td><code>{tag}</code></td>'
            f'<td>{inline(expr)}</td>'
            f'<td>{note}</td></tr>'
        )
    return (
        "<h2>3. Table math (math inside cells)</h2>\n"
        "<p>Same expressions in <code>&lt;td&gt;</code> cells. Cells use the "
        "same <code>.math-inline</code> wrapper. The CSS rule "
        "<code>td &gt; .math-inline { max-width: 100% }</code> ensures the "
        "math does not overflow the cell.</p>\n"
        '<table>\n'
        '<thead><tr><th>Tag</th><th>Rendered math</th><th>Notes</th></tr></thead>\n'
        f'<tbody>\n{chr(10).join(rows)}\n</tbody>\n'
        '</table>'
    )


# ============================================================================
# Stress-test row: a deliberately long inline expression on a narrow line
# ============================================================================
def section_stress() -> str:
    long_expr = (
        op("Attention") + "(" + var("Q") + ", " + var("K") + ", " + var("V")
        + ") = " + op("softmax") + "("
        + frac(var("Q") + var("K") + sup("T"), sqrt(var("d") + sub("k")))
        + ") " + var("V")
    )
    return (
        "<h2>4. Stress test: long expression in narrow column</h2>\n"
        "<p>The scaled dot-product attention formula is wider than most prose "
        "expressions. In a narrow column, it should still render as one "
        "horizontal atom and either fit, or scroll, but never break in the "
        "middle of the equation.</p>\n"
        '<div style="max-width: 22em; border: 1px dashed #aaa; padding: 0.6em; margin: 0.6em 0;">\n'
        f"<p>Inline: the transformer head computes {inline(long_expr)}, "
        f"which the rest of the architecture composes via residual connections.</p>\n"
        f"{display(long_expr)}\n"
        '</div>'
    )


# ============================================================================
# Page assembly
# ============================================================================
EXTRA_CSS = """
body { font-family: Georgia, serif; line-height: 1.7; margin: 1em auto;
       max-width: 38em; padding: 0 1em; color: #222; background: #fff; }
h1 { font-size: 1.5em; border-bottom: 2px solid #1a4078; padding-bottom: 0.3em; }
h2 { font-size: 1.2em; color: #1a4078; margin: 2em 0 0.4em;
     border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }
p { margin: 0.4em 0 0.7em; }
code { background: #f4f4f4; padding: 0.1em 0.3em; border-radius: 3px;
       font-size: 0.85em; font-family: Consolas, monospace; }
em { color: #555; font-size: 0.92em; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.95em; }
th, td { border: 1px solid #ddd; padding: 0.5em 0.7em; text-align: left;
         vertical-align: middle; }
th { background: #f0f4fa; color: #1a4078; }
"""


def build_xhtml() -> str:
    body = "\n".join([
        section_inline(),
        section_display(),
        section_table(),
        section_stress(),
    ])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Plain-HTML Math: Three Placement Variants</title>
<style><![CDATA[
{HTML_MATH_CSS}{EXTRA_CSS}
]]></style>
</head>
<body>
<h1>Plain-HTML Math: Three Placement Variants</h1>
<p>Six staple expressions rendered in four placement contexts. The goal:
verify that <strong>nothing breaks mid-formula</strong> regardless of where
the math appears.</p>
{body}
</body>
</html>
"""


def write_epub(xhtml: str, path: Path) -> None:
    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, "math2epub-variants"))
    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>Plain-HTML Math: Three Placement Variants</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-05-16T00:00:00Z</meta>
    <meta property="rendition:layout">reflowable</meta>
  </metadata>
  <manifest>
    <item id="page" href="page.xhtml" media-type="application/xhtml+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine><itemref idref="page"/></spine>
</package>"""
    nav = """<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc"><h1>Contents</h1>
<ol><li><a href="page.xhtml">Math Variants</a></li></ol></nav></body></html>"""
    with zipfile.ZipFile(path, "w") as z:
        zi = zipfile.ZipInfo("mimetype")
        zi.compress_type = zipfile.ZIP_STORED
        z.writestr(zi, "application/epub+zip")
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0"?>\n'
                   '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\n'
                   '<rootfiles><rootfile media-type="application/oebps-package+xml" '
                   'full-path="EPUB/content.opf"/></rootfiles></container>')
        z.writestr("EPUB/content.opf", opf)
        z.writestr("EPUB/nav.xhtml", nav)
        z.writestr("EPUB/page.xhtml", xhtml)


def main() -> None:
    xhtml = build_xhtml()
    html_path = OUT_DIR / "math-variants.html"
    html_path.write_text(xhtml, encoding="utf-8")
    print(f"Wrote {html_path} ({html_path.stat().st_size:,} bytes)")

    epub_path = OUT_DIR / "math-variants.epub"
    write_epub(xhtml, epub_path)
    print(f"Wrote {epub_path} ({epub_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
