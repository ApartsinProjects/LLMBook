---
name: math2epub
description: Render mathematics into Kindle-safe EPUB content. Three pipelines: plain HTML (recommended default; uses i/sub/sup/span and CSS, survives every KDP conversion, reflows with body text), SVG (MathJax with Kindle-specific post-processing), PNG (matplotlib mathtext at 300dpi). Encapsulates Kindle Previewer 3 quirks (defs/use shadow DOM, currentColor non-resolution, ex/em unit handling, max-width cell expansion, KDP data-URI stripping) so other build scripts can call helper functions and get back markup that survives KDP conversion. Use when adding math to a Kindle/KDP EPUB, fixing math rendering bugs, or comparing pipelines. Triggers on "math in EPUB", "kindle math", "render math for kindle", "math2epub", "html math", "tex to svg for kindle", "math rendering broken".
version: 1.1
---

# math2epub Skill

## What this skill does

Turns mathematics into EPUB-ready markup that renders correctly in Kindle Previewer 3 (KPV3) and survives KDP's reflowable converter.

Three pipelines, listed in order of preference for the LLMBook:

| Pipeline | Output | When to use |
|----------|--------|-------------|
| `html` (primary) | Plain HTML: `<i>`, `<sub>`, `<sup>`, `<span>` plus CSS | Default for almost all math. Reflows with body text, scales with font size, matches body weight, ~20 bytes per expression. |
| `svg`            | Inline `<svg>` markup from MathJax | Multi-line aligned derivations, dense tensor notation, anywhere typographic precision beats reflow. Larger markup (~500 bytes per expression). |
| `png`            | Raster image (bytes) bundled as EPUB file | Last resort for math that neither HTML nor SVG can render. ~2 KB per expression, fixed pixel size. |

One pipeline we explored and rejected (kept as a cautionary lesson in `LESSONS.md`):

- **MathML** (KaTeX `output: 'mathml'`): broken on KPV3. The `<msub>/<msup>` base atom renders offscreen on Enhanced Typesetting. Do not ship.

### Why plain HTML wins for the LLMBook

We initially treated HTML as the ugly fallback. After comparing all four pipelines in prose layout, plain HTML proved best:

- **Weight matches body text.** The italic `y` in `<i>y</i><sub>i</sub>` is the same font as the surrounding prose. SVG glyphs come out visibly heavier (see LESSONS L12).
- **Reflows.** A reader can change font size and the math grows with it. SVG and PNG are pinned to their intrinsic pixel dimensions.
- **Survives every converter.** Tags like `<i>`, `<sub>`, `<sup>`, `<span>`, and CSS borders are universal. SVG has been partially stripped by KDP in past versions (see LESSONS L2 and L5).
- **Tiny.** A 300-equation book is ~6 KB of inline math markup. The same book in PNG would gain ~900 KB.

When NOT to use HTML: multi-line aligned equations (CSS cannot easily replicate LaTeX's `align` environment), deeply nested tensor subscripts, or anywhere the math is so dense that typographic precision matters more than reflow.

## When the skill should activate

- User asks to render math/equations in an EPUB or Kindle book
- A build script is constructing `<math>...</math>` or `$...$` content for KDP output
- User reports "math doesn't render", "equations look broken in Kindle", "fractions are weird"
- User mentions LaTeX + Kindle / EPUB / KDP in the same request

## Workflow

```
1. Decide pipeline      svg = compact, inline; png = bulletproof, display
                |
                v
2. Build item list      [{"id": "eq1", "tex": r"y_i", "display": False}, ...]
                |
                v
3. Call render          from math2epub import render_batch
                        out = render_batch(items, pipeline="svg")
                |
                v
4. Embed into XHTML     inline svg: paste returned string directly
                        png: write bytes to EPUB/img/eq1.png, reference with <img>
                |
                v
5. Set OPF properties   <item ... properties="svg"/> for SVG content
                        nothing extra for PNG
                |
                v
6. Validate             python scripts/validate.py path/to/book.epub
```

## Empirical recipe: which pipeline for which math case

The trial-and-error comparison in `examples/math_recipe_comparison.py` runs 26 staple expressions through both pipelines and a dense table EPUB lets the reader see them side by side. The verdict, validated on KPV3 + Thorium + browser baselines:

**Plain HTML wins as the visible rendering for ALL 26 cases.** MathML only renders cleanly in a browser with the right math fonts and recent MathML Core support (Chrome 109+, Firefox, Safari). Every Kindle reader and every desktop ebook reader we tested either ignores MathML, renders it tiny, or breaks the base atom of msub/msup (the LESSON L1 bug).

The remaining question is whether to ALSO ship hidden MathML for screen-reader accessibility. The answer: **yes for math-heavy books that target a general audience; skip for the LLMBook because its readers are technical and the visible HTML is already semantic.**

### Per-case recipe table

| Math case | Visible HTML pattern | Accessibility (optional) |
|---|---|---|
| Subscript `y_i` | `<i>y</i><sub>i</sub>` via `var('y', sub='i')` | aria-label="y sub i" |
| Superscript `x^2` | `<i>x</i><sup>2</sup>` via `var('x', sup='2')` | aria-label="x squared" |
| Multi-index `z_ij^(k)` | `var('z', sub='ij') + sup('(k)')` | aria-label="z sub i j to the k" |
| Greek letter `α + β` | `GREEK['alpha'] + ' + ' + GREEK['beta']` | aria-label="alpha plus beta" |
| Simple fraction `1/n` | `frac('1', var('n'))` (inline-block + block-level rows) | aria-label="one over n" |
| Compound fraction | `frac(num, den)` works for any compound | spoken form per math style |
| Sum with limits `∑_{i=1}^{n}` | `summation(low='i=1', high='n')` (stacked inline-block) | aria-label="sum from i equals 1 to n" |
| Integral with limits | `integral(low='-inf', high='inf')` | similar |
| Limit / max / min with subscript | `op('lim', sub='n→∞')` | similar |
| Sqrt simple `√x` | `sqrt(var('x'))` (√ + overlined inline-block) | aria-label="square root of x" |
| Sqrt over expression | `sqrt(var('a') + '+' + var('b'))` | similar |
| Hat over letter `ŷ` | `hat(var('y'))` returns Unicode `ŷ` directly | aria-label="y hat" |
| Bar over letter `x̄` | `bar(var('x'))` returns Unicode `x̄` directly | aria-label="x bar" |
| Vector `v⃗` | `vec(var('v'))` returns Unicode `v⃗` directly | aria-label="vector v" |
| Hat over fraction | CSS-positioned `.hat::before` over the `.frac` | spoken form |
| MSE display | full inline-block layout works inline OR display | spoken form |

### Why MathML lost

1. **Kindle Previewer 3 bug**: msub/msup base atom renders offscreen on Enhanced Typesetting. `y_i` shows as just `i`. (LESSONS L1.)
2. **Browser inconsistency**: Chrome only added MathML Core in v109 (Jan 2023). Older versions render `<math>` as colored placeholder marks because they don't recognize the element. Without explicit math-font CSS the rendering is tiny and unreadable.
3. **No font fallback**: MathML uses dedicated math fonts (Cambria Math, STIX Two Math). Kindle and many readers don't ship these, so glyphs come out as `.notdef` boxes or default sans.
4. **Weight mismatch with body**: MathML font is typically heavier than body serif. Math reads as bolder than surrounding prose, which is the inverse of what readers expect.
5. **Tiny markup but invisible result**: MathML is concise to author, but a concise expression that doesn't render is a regression.

Plain HTML, in contrast: uses the body font directly (perfect weight match), works in every reader because the tags involved (`<i>`, `<sub>`, `<sup>`, `<span>`, CSS) are foundational, scales with reader font size, has tiny markup (20-50 bytes for inline expressions).

## API

### Plain HTML pipeline (recommended)

Unlike SVG and PNG which convert LaTeX source, the HTML pipeline expects you to compose markup using small helpers. There is no algorithmic LaTeX-to-HTML translator because plain HTML for math is a typesetting choice, not a syntactic one.

```python
import sys
sys.path.insert(0, ".claude/skills/math2epub/scripts")
from html_math import (
    HTML_MATH_CSS,                                # include in <style>
    var, op, frac, hat, bar, vec, sqrt,            # atoms
    summation, integral, product,                  # big operators with limits
    inline, display, sub, sup,                     # wrappers
    GREEK, OPS,                                    # symbol dicts
)

# Inline: "The output y_i ..."
yi = var("y", sub="i")                            # <i>y</i><sub>i</sub>
prose = f"The output {inline(yi)} for example {inline(var('i'))} ..."

# Display equation: MSE = (1/n) sum (y_hat_i - y_i)^2
mse = display(
    op("MSE") + " = " + frac("1", var("n")) + " "
    + summation(low="i=1", high=var("n")) + " ("
    + hat(var("y")) + sub(var("i")) + " &#8722; "
    + var("y", sub="i") + ")" + sup("2")
)
```

The CSS string `HTML_MATH_CSS` provides all required styles. Inline it inside `<style>` (wrap in `<![CDATA[ ... ]]>` to be safe against `<i>`-shaped tokens inside CSS comments) or write to a file and link.

See `examples/html_examples.py` for a full demo: 6 sections covering prose, display, table, formula gallery (12 staple ML formulas), Greek + operator reference, and typography edge cases.

### SVG and PNG pipelines

```python
from math2epub import render_batch, render

items = [
    {"id": "eq1", "tex": r"y_i", "display": False},
    {"id": "eq2", "tex": r"\frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2",
     "display": True},
]

svgs = render_batch(items, pipeline="svg")        # {id: svg_str}
pngs = render_batch(items, pipeline="png")        # {id: png_bytes}

# Single-expression convenience
svg_str   = render(r"y_i", pipeline="svg", display=False)
png_bytes = render(r"E = mc^2", pipeline="png", display=False)
```

## Output handling rules

### SVG output
- Already post-processed: `fontCache:'none'`, `currentColor` replaced with `#000`, `ex/em` width/height converted to `px`
- Paste directly into XHTML body
- OPF manifest item needs `properties="svg"`
- Do NOT wrap in `<span style="display:inline-block; line-height:0">` for cells in a table: Kindle's `svg { max-width: 100% }` will fight that wrapper
- For inline math, no wrapper needed; the SVG flows like an image

### PNG output
- Returned as raw bytes (PNG file content)
- Write to `EPUB/img/eq###.png` inside the zip
- Reference with `<img src="img/eq###.png" alt="..." class="math-inline"/>` (or `math-display`)
- Do NOT use `data:` URIs. KDP's converter strips data URIs from `<img>` tags. Bundle real files
- CSS: `img.math-inline { vertical-align: middle; max-height: 1.5em; }` and `img.math-display { max-width: 100%; height: auto; }`

## XHTML gotchas

Caught and worked around in `_math_compare_prose.py`. If you write XHTML by hand:

- HTML named entities like `&mdash;` `&radic;` `&Sigma;` `&nbsp;` are **fatal** in XHTML without a DOCTYPE declaring them. Use numeric refs (`&#8212;`) or raw Unicode characters (`Σ`, `√`)
- `<br>` is fatal. Use `<br/>`
- Putting `<code>` inside `<sub>` and forgetting to escape `<` `>` `&` in tex strings will break the parse. Always `tex.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')` before interpolating into XHTML

## Requirements

- Python 3.11+ with `matplotlib` (for PNG pipeline)
- Node.js with `mathjax-full` installed at `E:/Tools/mathjax/node_modules` (for SVG pipeline)
- Override the MathJax install path by setting `MATH2EPUB_MATHJAX` env var
- Override Python by setting `MATH2EPUB_PYTHON` (defaults to `python` on PATH)

## Validation

The skill ships `scripts/validate.py` which wraps epubcheck. It assumes epubcheck is at:
- `E:/Tools/epubcheck/epubcheck-5.1.0/epubcheck.jar`
- Java at `E:/Tools/epubcheck/jdk-17.0.19+10-jre/bin/java`

Override with `MATH2EPUB_EPUBCHECK` and `MATH2EPUB_JAVA` env vars if installed elsewhere.

```bash
python .claude/skills/math2epub/scripts/validate.py KDP/output/book.epub
```

A clean run prints `0 fatals / 0 errors / 0 warnings / 0 infos`. Any other result is a real problem to fix before shipping.

## When NOT to use this skill

- The book has zero math: just skip it
- You need MathML output for an accessibility audit on a non-Kindle reader: use KaTeX directly with `output: 'mathml'` and `aria-hidden` the visual rendering. Do not ship that to Kindle
- You need interactive math (zoom, hover-explain): out of scope, EPUB is static

## Maintenance

Whenever Kindle Previewer 3 ships a new version, re-run `examples/demo.py`, drag the output into KPV3, and verify both pipelines still render correctly. Record any regressions in `LESSONS.md` with a date and KPV version.

If MathJax or matplotlib gets a major version bump, re-run the smoke test before trusting it.

The skill is dual-located:
- Source of truth: `.claude/skills/math2epub/` inside the LLMBook repo (versioned with git)
- Global mirror: `C:/Users/apart/.claude/skills/math2epub/` (NTFS junction pointing to the above)

To verify the junction is intact:

```bash
ls -la /c/Users/apart/.claude/skills/math2epub
```

Should show a `<JUNCTION>` arrow pointing to the project path.
