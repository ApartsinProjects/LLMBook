# math2epub Lessons Learned

Accumulated knowledge from debugging math rendering in Kindle Previewer 3 (KPV3).
Each entry: what we tried, what broke, why, and what to do instead. New lessons go at the bottom with a date.

---

## L1. MathML in KPV3 is unusably broken (2026-05-15)

**Tried**: KaTeX with `output: 'mathml'`, generating EPUB 3 with `properties="mathml"` on the spine item.

**Broke**: On KPV3 with Enhanced Typesetting enabled, every `<msub>` and `<msup>` element renders with the base atom **invisible**. So `y_i` shows as just a tiny floating `i` with no `y`. `x^2` shows as a tiny floating `2`. Fractions render but baseline is wrong.

**Why**: KPV3's MathML layout engine has a bug in script-element positioning. Confirmed by isolating to `htmlAndMathml` (same bug), `mathml` only (same), and `<semantics>` stripped (same). It is not a wrapper issue, it is the layout engine.

**Do**: Do not ship MathML to Kindle even though EPUB 3 spec allows it. Use SVG or PNG.

---

## L2. SVG with `<defs>` and `<use>` shadow DOM is partially stripped (2026-05-15)

**Tried**: MathJax SVG output with default `fontCache: 'local'`. Each glyph is a `<defs><path id="MJX-1-..." d="..."/></defs>` plus `<use xlink:href="#MJX-1-..."/>` references.

**Broke**: Kindle's CSS/security pass strips `<defs>` but leaves the `<use>` references behind. Result: the SVG shows blank space where math should be.

**Why**: Kindle's HTML sanitizer treats `<defs>` outside the visible flow as a candidate for removal. The references in `<use>` then resolve to nothing in the rendered DOM.

**Do**: Set `fontCache: 'none'` in MathJax SVG output. This inlines each glyph as a literal `<path d="..."/>` inside the visible SVG. Larger output, but bulletproof.

---

## L3. `currentColor` does not resolve through `<use>` shadow DOM (2026-05-15)

**Tried**: MathJax SVG with `fill="currentColor"` and `stroke="currentColor"` on glyphs (the default).

**Broke**: Even with `fontCache: 'none'`, some inlined glyph paths still carried `fill="currentColor"`. In KPV3, `currentColor` did not resolve to the parent text color: it resolved to black on white pages and to nothing (invisible) on sepia/dark themes.

**Why**: Kindle's theme switcher overrides text color via a different mechanism than CSS inheritance, and `currentColor` does not pick it up.

**Do**: Post-process the SVG output to replace `fill="currentColor"` with `fill="#000"` and `stroke="currentColor"` with `stroke="#000"`. This loses dark-theme support but makes the math visible.

---

## L4. SVG `ex`/`em` width/height attributes are interpreted as pixels by Kindle (2026-05-15)

**Tried**: Default MathJax SVG output has `width="2.484ex" height="1.464ex"` attributes.

**Broke**: KPV3 interpreted those as `2.484px` and `1.464px`. Math glyphs rendered at sub-pixel size, illegible.

**Why**: Kindle's reflowable engine treats unitless or non-px length values inconsistently. `ex` units in particular are not honored.

**Do**: Post-process the SVG to convert `ex` and `em` to `px`. Conversion factor: with MathJax `em: 24, ex: 12` per-render options, multiply `ex` by 12 and `em` by 24 to get pixels. The skill's `render_svg.py` does this.

---

## L5. `data:` URIs in `<img src="...">` are stripped by KDP's converter (2026-05-15)

**Tried**: Embed PNG images as `<img src="data:image/png;base64,...">` to avoid bundling files in the EPUB.

**Broke**: Browser preview rendered correctly. After KDP conversion (kindlegen / KPV3 convert), the `<img>` elements showed broken-image icons. Inspecting the converted KPF showed the `src` attribute had been removed.

**Why**: KDP's reflowable converter has a security policy that strips `data:` URIs. Not documented but consistent across multiple test EPUBs.

**Do**: Bundle PNGs as real files in `EPUB/img/eq###.png` and reference with relative paths in `<img src="img/eq###.png">`.

---

## L6. `svg { max-width: 100% }` causes table-cell expansion artifact (2026-05-15)

**Tried**: A 4-column comparison table where each cell contained one math expression rendered via a different pipeline.

**Broke**: SVG cells looked huge (math three times larger than surrounding text). MathML, HTML, and PNG cells looked correctly sized. Misled into thinking the SVG pipeline was over-scaled.

**Why**: Kindle injects a default rule `svg { max-width: 100% }`. Inside a `<td>`, the SVG expanded to fill the cell width. In real prose (no surrounding fixed-width container), the SVG renders at its intrinsic `width="..."` attribute.

**Do**: Always test math in **prose layout** (paragraphs), not in tables. The `_math_compare_prose.py` script in `KDP/build/` is the reference for prose-layout comparison.

---

## L7. HTML named entities are fatal in XHTML (2026-05-15)

**Tried**: Plain-HTML math fallback using `&radic;` (√), `&Sigma;` (Σ), `&mdash;` (em dash), `&nbsp;`.

**Broke**: `epubcheck` reported `FATAL(RSC-016): The entity "mdash" was referenced, but not declared`.

**Why**: XHTML does not predeclare HTML named entities. Only the five XML entities (`&lt; &gt; &amp; &quot; &apos;`) are safe without a DTD reference.

**Do**: Use literal Unicode characters (`√ Σ Σ`) or numeric character references (`&#8212;`). The skill's renderers and helpers never emit named entities.

---

## L8. `<br>` and unescaped tex strings break XHTML parse (2026-05-15)

**Tried**: Building a comparison table by string-interpolating LaTeX source like `<code>$\frac{1}{n}$</code><br>` into XHTML.

**Broke**: `<br>` is invalid (must be `<br/>`). And the LaTeX contained `<` `>` `&` characters which broke the parse before we even reached the `<br>`.

**Do**: Always self-close void elements (`<br/>`, `<hr/>`, `<img/>`). Always XML-escape tex strings before interpolating: `tex.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')`. The skill's renderers do not generate XHTML directly; the caller is responsible for escaping when embedding.

---

## L9. KaTeX `<semantics><annotation>...</annotation></semantics>` wrapper confuses some readers (2026-05-15)

**Tried**: KaTeX MathML output with default settings includes a `<semantics>...<annotation encoding="application/x-tex">y_i</annotation></semantics>` wrapper that contains the original LaTeX source.

**Broke**: Some EPUB readers rendered the raw LaTeX source text alongside the math. KPV3 was inconsistent.

**Do**: Even if we abandoned MathML, the skill's `render_mathml` helper (kept for reference but not shipped as production) strips `<semantics>` and `<annotation>` wrappers before returning markup. The pattern: `re.sub(r"<semantics>(.*?)<annotation\b[^>]*>.*?</annotation>\s*</semantics>", r"\1", html, flags=re.DOTALL)`.

---

## L10. matplotlib `fontset='cm'` gives Computer Modern look (2026-05-15)

**Tried**: Default matplotlib mathtext rendering (Sans-Serif fallback).

**Broke**: Output looked like Helvetica math. Visually clashed with the book's Georgia serif body text.

**Do**: Set `matplotlib.rcParams['mathtext.fontset'] = 'cm'`. Computer Modern matches the LaTeX look readers expect and pairs well with serif body text. Alternative: `'stix'` for STIX Two Math (also serif, slightly more modern).

---

## L11. PNG DPI vs intrinsic image size for inline math (2026-05-15)

**Tried**: 72 DPI PNG (matplotlib default) for inline math.

**Broke**: Math looked blurry. Worse on high-resolution Kindle Paperwhite (300 DPI screen).

**Do**: Use `dpi=300` for both fig creation and savefig. Combined with `bbox_inches='tight'` and `pad_inches=0.05`, the PNG comes out at a physical size that matches inline text height when constrained by CSS `max-height: 1.5em`.

---

## L16. MathML lost the empirical bake-off (2026-05-16)

**Tried**: a dense 26-expression × 2-pipeline comparison page (`examples/math_recipe_comparison.py`), rendering each expression in MathML (KaTeX `output:'mathml'`) and in our plain HTML, side by side. The goal: empirically find which math cases benefit from MathML and which from HTML, then write a per-case recipe.

**Broke**: MathML rendered as **tiny colored marks** in every cell, regardless of expression complexity. The actual MathML markup was valid (`<math xmlns="..."><mrow><msub><mi>y</mi><mi>i</mi></msub></mrow></math>` for `y_i`); the renderer just couldn't display it readably.

**Why** (three converging causes):
   1. The page CSS didn't declare math fonts, so the renderer fell back to `.notdef` glyphs (visible as the "colored marks").
   2. The page's table cell `font-size: 0.85em` cascaded INTO the `<math>` element, shrinking the already-broken rendering.
   3. Kindle Previewer 3's MathML pipeline has the msub/msup base-atom bug (LESSONS L1), so even with proper fonts, sub/superscript expressions render with the base offscreen.

**Tried to recover**: added `math { font-family: "Cambria Math", "STIX Two Math", ...; font-size: 1.05em; vertical-align: middle; }` to the comparison page CSS. This makes the MathML readable on browsers WITH math fonts installed (recent Chrome on macOS, Firefox, Safari). It still does not fix Kindle.

**Do**: **plain HTML is the visible pipeline for ALL math cases.** MathML is only worth shipping as an accessibility supplement in `<span class="visually-hidden">` for screen-reader users, NOT as the visible rendering. The recipe table now lives in SKILL.md.

---

## L13. Plain HTML is the production default, not the fallback (2026-05-15)

**Reframed**: Initial documentation called plain HTML the "ugly last-resort fallback" because CSS fractions sit slightly off-baseline compared to LaTeX-typeset fractions. After visual comparison in prose context across all four pipelines, plain HTML is in fact the strongest production choice for the LLMBook.

**Why**: four properties that no rasterized pipeline can match:
   1. **Reflow.** When a reader changes font size, plain-HTML math grows with body text. SVG and PNG are pinned to intrinsic pixel dimensions.
   2. **Weight match.** Italic `y` rendered as `<i>y</i>` uses the same font as italic body text. SVG comes out heavier (L12). PNG raster glyphs are anti-aliased differently from the typeface.
   3. **Universal converter survival.** `<i>`, `<sub>`, `<sup>`, `<span>`, and CSS borders are universally supported by every KDP conversion path. SVG has been partially stripped by KDP in past versions (L2, L5).
   4. **Tiny markup.** A typical inline expression is 20-50 bytes. A 300-equation book is 6 KB of math markup. The same book as PNG would be 900 KB.

**Trade-off accepted**: CSS fractions sit a hair off-baseline compared to LaTeX. Multi-line aligned derivations are hard. For the LLMBook the trade is worthwhile; for a math textbook with dense linear algebra, SVG might still win.

**Do**: write math using helpers in `scripts/html_math.py` (`var`, `frac`, `hat`, `bar`, `sqrt`, `summation`, `integral`, `product`, `GREEK`, `OPS`). See `examples/html_examples.py` for the full pattern catalog including prose, display, table, formula gallery, reference, and edge cases.

---

## L14. XHTML named entities are still fatal even when invoked inline (2026-05-15)

**Tried**: While building `examples/html_examples.py`, used `&hellip;` for ellipsis, `&minus;` for typographic minus, `&radic;` for square root, `&mu;` / `&sigma;` for Greek letters, all inline in XHTML body text.

**Broke**: `epubcheck` fatal: `The entity "hellip" was referenced, but not declared`. Each unrecognized named entity is a separate fatal. (Same root cause as L7; documenting the recurrence because it caught me twice.)

**Do**: never use HTML named entities except the five XML-predefined ones (`&lt; &gt; &amp; &quot; &apos;`). For everything else, use numeric character references (`&#8722;` for minus, `&#8730;` for radical, `&#956;` for mu) or literal Unicode characters (`−`, `√`, `μ`). The helpers in `html_math.py` return literal Unicode or numeric refs, never named entities; callers who build XHTML by hand must remember this rule.

---

## L15. CSS comments containing angle-bracketed tag names break XHTML parsing (2026-05-15)

**Tried**: Embedded the math-CSS inline in `<style>...</style>` of an XHTML page. The CSS contained a developer comment `/* surrounding <i> already does this ... */`.

**Broke**: `epubcheck` fatal: `The element type "i" must be terminated by the matching end-tag "</i>"`. The XHTML parser treated `<style>` content as PCDATA (per XML rules) and found a stray `<i>` inside the CSS comment with no closing tag.

**Why**: HTML5 treats `<style>` as raw text. XHTML treats it as PCDATA, where markup characters are parsed. CSS comments are not parsed CSS-syntactically until they reach the CSS engine.

**Do**: either wrap inline `<style>` content in `<![CDATA[ ... ]]>` to opt out of XML parsing, OR keep CSS comments free of angle-bracketed tag-shaped tokens (use uppercase tag names like `I` `SUB` `SUP`, or words like "italic span", or no examples at all). Both fixes are now applied in `examples/html_examples.py`.

---

## L12. SVG glyph weight reads heavier than serif body text (2026-05-15)

**Observed**: In a prose-context render comparing SVG vs plain HTML inline math, `y_i` rendered via the SVG pipeline visually appears as a heavier/bolder italic than the same `<i>y</i><sub><i>i</i></sub>` in pure HTML, which matches body weight perfectly. Confirmed in KPV3 screenshot of `math-compare-prose.epub`.

**Why** (suspected): three contributing factors, untangled by experiment:
   1. `scale: 1.8` in tex2svg.js inflates both glyph height and stroke thickness proportionally. The eye reads thicker strokes at the same height as a bolder weight, even when the typeface is the same.
   2. MathJax's default math font (TeX/STIX-derived) has a heavier italic stroke contrast than typical body serifs (Georgia, in the LLMBook case).
   3. Post-process replaces `fill="currentColor"` with `fill="#000"` (pure black), preventing any inherited softer text color from lightening the glyph.

**Do** (not yet decided): pick one of three remedies and re-test:
   a. Drop `scale` from 1.8 down to 1.4 or 1.2. Glyph height will shrink and need a CSS `vertical-align`/`max-height` adjustment to keep inline math at body height. Risk: the glyph may regress to "too small" as we saw earlier (which is why we went up to 1.8).
   b. Switch SVG font to a lighter family by configuring MathJax `font: 'mathjax-modern'` or shipping our own font set. More invasive.
   c. Use `fill="#222"` instead of `#000` so the math reads at the same color weight as the body text color (typically `#222` in the LLMBook CSS). Cheapest experiment; one-line change in render_svg.py post-process.

Pending: implement (c) first, re-render `math-compare-prose.epub`, screenshot, compare to HTML. If still too heavy, layer (a). Reserve (b) for a separate iteration.

---

## L13. Automated KaTeX->PNG pipeline beats MathML-only AND manual-HTML for a 300-equation Kindle EPUB (2026-05-21)

**Context**: The LLMBook EPUB shipped math as KaTeX `output:'mathml'`. A reader reported
every display equation rendering as a vertical stack of single atoms in **Thorium**
(`L=-` / `1` / `n` / `Sigma` ... each on its own line).

**Root cause (confirmed in headless Chromium = Thorium's engine)**: `epub_overrides.css`
forced `display: inline !important` on `math, mrow, mi, mn, mo, mtext, semantics` (plus
`math[display=block] *` and `math *{overflow:hidden}`). That overrides the browser's
native MathML layout: `<mfrac>`/`<msub>` keep `display: block math` while siblings are
forced inline, so the row stacks. Diagnostic: the built chapter as-is gave a **171px**
math-block; deleting those overrides gave **45px** (correct single line). Lesson:
**never force `display` on MathML token elements** -- style only `.katex`/`.math-block`
wrappers, never the `m*` elements.

**Strategic verdict (web research, 2026)**: MathML on Kindle is gated on Enhanced
Typesetting, which any single disqualifier silently turns off (notably **>25 SVGs**,
inline-block tables, fixed layout, >300 HTML files, >30MB/file). Publishers report
"renders in Kindle Previewer 3 but breaks on devices." MathML-only is the *least*
reliable choice; **PNG is the de-facto STEM-on-Kindle standard**.

**What shipped (automated, NOT matplotlib)**: matplotlib mathtext can't handle
`\mathcal`, `\begin{aligned}`, `\operatorname`, etc., and the book's LaTeX is already
KaTeX-validated -- so render with **KaTeX + Playwright/Chromium** (same engine as the
website -> pixel-identical math). Pipeline wired into html2pub:
  1. `math_render.py` stamps `data-tex` + `data-mathdisplay` on each katex wrapper.
  2. Build writes `.book-update/math-manifest.json` (293 complex/display eqs; ~890 simple
     inline stay `<sub>/<sup>` via `simplify_inline_mathml` -- those reflow/scale/match
     body weight, so DON'T PNG them).
  3. `scripts/build_math_png_cache.py`: renders every entry in ONE Playwright page
     (`katex.render(...,{output:'html'})` via `page.evaluate`, data as a JS arg so it's
     never HTML-embedded -> no `</script>`/escaping breakage), `device_scale_factor=3`,
     white bg, `.katex-display{display:inline-block;margin:0}` so `element.screenshot()`
     is tight, then pngquant. Key = `sha1(rewritten_tex|display)` -> content-addressed +
     incremental. **Gotcha**: element ids must NOT start with a digit (CSS `#<hex>` is
     invalid) -- prefix them (`#eq_<key>`).
  4. `builder.py replace_mathml_with_png()` (after the post_process hook, where `images`
     exists) swaps remaining MathML for `<img>`, **adding PNG bytes straight into
     `images.bundled_bytes`** (bypasses `_reencode`, which would JPEG-ify a white-bg PNG
     and blur strokes). The img loop is guarded to skip `../img/` srcs.
  5. `html2pub.toml [math] png_cache = ".book-update/math-png-cache"` enables it; empty
     keeps MathML. Two-pass: build (manifest) -> cache script -> build (inject).

**Sizing (critical)**: render at 3x, set explicit logical `width`/`height` attrs = px/3.
Kindle honors the width/height *attributes* but **ignores CSS `max-width`/`max-height`
on `<img>`**. Cap display equations to ~560 CSS px (no CSS max-width to lean on). CSS:
`img.math-png-display{display:block;margin:1em auto;max-width:100%}`,
`img.math-png-inline{vertical-align:middle}`. Alt = de-LaTeX'd source, <=140 chars.

**Result**: 0 `<math>` left, 293 deduped PNGs (~2.7MB), book 35.5MB, EPUBCheck 0 errors,
equations render pixel-perfect in Chromium/Thorium (= every reader incl. Kindle). This
supersedes the SKILL.md "PNG = last resort, manual" stance **for large auto-built
books**: KaTeX+Playwright makes PNG fully automated and high-fidelity. Keep simple inline
as `<sub>/<sup>` (best of both).

**Accessibility option (not shipped)**: per DAISY 2024+, do NOT put `alttext`/`altimg`/
aria on `<math>`; keep the visible PNG (`<img alt>`) and optionally a TeX/MathML sibling
in `<details>` or `semantics><annotation>` (Kindle ET supports `<annotation>`).

---

## Open questions (revisit later)

- Does Kindle iOS app handle SVG `<use>` shadow DOM the same as KPV3? Unknown.
- Does `htmlAndMathml` with `aria-hidden` on the visual span improve accessibility while still rendering visually? Possibly, but increases markup size 3x. Not worth it for math-heavy books.
- Can we use AVIF or WebP instead of PNG for smaller files? Kindle support is spotty. PNG is the safe default.

---

## L14. KaTeX errors render as SILENT empty boxes; scan for them (2026-05-22)

render_math.js uses `throwOnError:false`, so a TeX parse error becomes a
`<span class="katex-error">` (class is `katex-error`, NOT `katex`). The builder's
render() looks for class `katex` and, for `$$..$$` text-node placeholders, DROPS
anything that isn't -> the equation ships as an EMPTY box (no error; EPUBCheck and
KPV both pass). Six such equations shipped before we caught them. Error modes:
  * `\texttt{\text{WORD}}` -> the \text->\mathrm pre-pass makes \mathrm run inside
    text mode (illegal in KaTeX). Use `\texttt{WORD}` (no nested \text).
  * underscore inside `\text{...}` e.g. `\text{(gCO_2/kWh)}` -> "_ in text mode".
    Use `\mathrm{(gCO_2/kWh)}`.
  * stray inner `$` in a numeric range: `$0.4$-$0.6$` -> the inner `$` breaks it.
    Use one span: `$0.4\text{-}0.6$`.
  * HTML entities decode before KaTeX (get_text/str), so `&lt;`/`&gt;` become `<`/`>`
    and a bare `&` breaks KaTeX (alignment char).
DETECT all of them: extract every `$..$`/`$$..$$`/.math span the SAME way the
builder does, run the SAME render_math.js, flag any output containing
`katex-error`. See scripts/diag_katex_errors.py (0/1198 fail after fixes).
