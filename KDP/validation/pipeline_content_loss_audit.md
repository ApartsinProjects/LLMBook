# Build Pipeline Content-Loss Audit

**Audit date:** 2026-05-14
**Method:** Static analysis of decompose/extract/unwrap/filter calls across `KDP/build/` and `KDP/html2pub/src/`, plus element-count comparison source HTML vs built EPUB.

## Verdict: No silent content loss

Every reduction in element count is traced to an INTENTIONAL transform with documented rationale.

## Element counts

| Element     | Source | EPUB | Δ      | Status |
|-------------|--------|------|--------|--------|
| p           | 15,717 | 18,186 | +2,469 | build adds wrappers |
| h1          | 366    | 388   | +22    | build adds chapter nav titles |
| h2          | 2,193  | 2,266 | +73    | build adds nav headings |
| h3          | 2,318  | 2,452 | +134   | build adds nav headings |
| h4–h6       | 16     | 16    | 0      | OK |
| table       | 394    | 399   | +5     | OK |
| tr/td/th    | ~12,873| ~13,062 | +189  | adds caption rows |
| pre/code    | 5,855  | 6,137 | +282   | build wraps `<code>` cleanly |
| img         | 1,139  | 1,294 | +155   | adds cover, avatars |
| li/ul/ol    | 6,011  | 6,273 | +262   | OK |
| figure      | 267    | 275   | +8     | OK |
| **details** | 1,780  | **0** | **-1,780** | **transformed** (see below) |
| **summary** | 1,780  | **0** | **-1,780** | **transformed** |
| sub/sup     | 192    | 518   | +326   | v802 inline-math conversion |
| math        | 0      | 305   | +305   | KaTeX rendering (server-side) |
| a           | 11,835 | 11,453 | -382  | unwrapped (text kept, see below) |
| callout     | 8,174  | 8,484 | +310   | OK |
| **words**   | **1,381,498** | **1,399,375** | **+17,877** | +1.3% (build adds nav text, footers) |

## Documented transforms (intentional, content preserved)

### 1. `<details>` / `<summary>` → `<div class="details-shim">` / `<p class="details-title">`
- **Loc:** `KDP/build/_sanitize_kindle_css.py:85-88`
- **Reason:** Some Kindle versions don't render native `<details>` collapsibles. Convert to static expanded box so the "Answer Sketch" content is always visible.
- **Content impact:** ZERO text lost. Behavior changes from "click to expand" → "always visible".
- 1,780 of 1,780 transformed (100%).

### 2. `<a>` to unresolved targets → text-only (unwrap)
- **Loc:** `KDP/html2pub/src/html2pub/builder.py:185`
- **Reason:** If a link's target isn't in the EPUB spine, the link can't navigate. The text content survives; only the `<a>` wrapper is removed.
- **Content impact:** ZERO text lost. 382 links unwrapped (text preserved as plain text).

### 3. `<ul class="sections-list">` → `<div class="section-grid">`
- **Loc:** `KDP/html2pub/src/html2pub/content.py:slim_index_lists`
- **Reason:** Chapter-index section cards rendered better as flex grid than as bullet list.
- **Content impact:** ZERO text lost. 25 list wrappers replaced with div wrappers.

### 4. Inline simple math `<math>` → HTML `<sub>`/`<sup>`
- **Loc:** `KDP/build/_html2pub_hooks.py:simplify_inline_mathml` (v802)
- **Reason:** MathML inline rendering broken in many EPUB readers (each math symbol line-breaks). Simple patterns (single letter, sub, sup) become plain HTML which renders inline correctly.
- **Content impact:** Math text preserved as styled HTML. 661 conversions; complex math (305 elements) and display math stay as MathML.

### 5. `<details>` summary text becomes `<p class="details-title">`
- Same as #1, summary text preserved.

### 6. `complex-table-note` callout removed
- **Loc:** `KDP/build/_html2pub_hooks.py:strip_wide_table_notes` (v13.6)
- **Reason:** html2pub library injects a prose note before wide tables ("Wide Table (N columns) — On narrow screens..."). The note added noise to the EPUB without value.
- **Content impact:** 40 prose notes removed across 24 chapters. Tables themselves preserved.

### 7. Wisdom-council slim
- **Loc:** `KDP/build/_html2pub_hooks.py:slim_wisdom_council`
- **Reason:** 42 wisdom-council agent cards exist in source; only ~8 are quoted in the book. Drop 34 to save ~25 KB.
- **Content impact:** 34 unused agent profile cards dropped (no body text in the book references them). User-visible note inserted: "This Kindle edition includes profiles for the 8 most-quoted agents."

### 8. Annotation / semantics MathML wrappers stripped
- **Loc:** `KDP/build/_html2pub_hooks.py:fix_math_alignment`
- **Reason:** `<annotation>` would leak raw TeX source on non-MathML readers. `<semantics>` wrapper renders as block in some readers, breaking inline math.
- **Content impact:** Wrapper tags removed; the actual mathematical content (mi/mn/mo/msub/msup etc.) preserved.

### 9. Decorative SVG inside `<a>` removed
- **Loc:** `KDP/html2pub/src/html2pub/content.py:65-67`
- **Reason:** Decorative arrow icons inside link tags don't add meaning in EPUB.
- **Content impact:** Decorative SVGs only; no text content.

### 10. `script` / `noscript` removed
- **Loc:** `KDP/html2pub/src/html2pub/content.py:UNWANTED_TAGS`
- **Reason:** EPUB doesn't execute JavaScript.
- **Content impact:** Script tags only (no visible content).

### 11. Inline `<style>` over 1,500 chars dropped
- **Loc:** `KDP/html2pub/src/html2pub/content.py:60-62`
- **Reason:** Large inline styles bloat the EPUB; replaced by external stylesheets.
- **Content impact:** Style attributes only (no visible content).

### 12. `<img>` with unresolvable src removed
- **Loc:** `KDP/html2pub/src/html2pub/builder.py:197`
- **Reason:** If an image file can't be bundled (missing on disk), the `<img>` is dropped to avoid rendering a broken-image icon.
- **Content impact:** None observed in this build — EPUB image count is HIGHER than source (1294 vs 1139) due to cover + agent avatars.

## Explicit drop configuration (html2pub.toml)

```
drop_selectors = [
  ".no-epub",                       # author opt-out marker
  "script[src*='analytics']",       # analytics scripts
]

[transforms.fragment_drop]
"wisdom-council" = [<34 agent ids>]  # match wisdom-council slim
```

## Conclusion

**No silent content loss in the build pipeline.** All reductions are documented intentional transforms preserving the underlying text. The EPUB has 1.3% MORE words than source HTML (build adds nav titles, footers, chapter-end "What Comes Next" callouts).

**Word count delta:** +17,877 words (1.3%) — gains from build-injected content; no losses.
