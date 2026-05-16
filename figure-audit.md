# Figure / Image Sizing Audit

Scope: every `<img>` element in the `.html` content pages of the LLMBook tree, excluding `KDP/`, `.claude/`, `temp_*`, `scripts/`, `*backups*`, `node_modules/`, `agents/`, and `templates/`.

- HTML files scanned: **389**
- `<img>` elements inspected: **647**
- Stylesheet checked: `styles/book.css`

This is a read-only audit. No HTML, CSS, or image files were changed.

---

## 1. Stylesheet check (soft constraint)

The user's expected rule is `img { max-width: 100%; height: auto; }` at global scope so every image downscales to its container.

**`styles/book.css` does NOT contain a global `img` rule.** The only related rules are:

| Selector | File:Line | Effect |
|---|---|---|
| `.diagram-container svg` | book.css:1715-1719 | `width: 100%; max-width: 100%; height: auto;` (SVG only, not `<img>`) |
| `.illustration img` | book.css:1740-1742 | `max-width: 100%; border-radius: 8px;` |
| `.illustration img` (mobile) | book.css:2430 | repeats `max-width: 100%; height: auto;` under `@media (max-width: 1024px)` |
| `svg` (mobile only) | book.css:2429 | `max-width: 100%; height: auto;` (only under `@media (max-width: 1024px)`) |

**Gap.** PNG/JPG images wrapped in `<div class="diagram-container">` (which is how virtually all numbered figures in the book are wrapped) have **no max-width constraint at all** because the rule at line 1715 selects `svg` only. There are **154** such raster images, and at least **52** of them are sourced from files wider than 1500px, which is wider than the 820px content column. That is the root cause of the two user-reported oversized figures.

**Suggested addition (DO NOT apply without user confirmation).** Add one global rule near line 1710 (just before the existing `.diagram-container` block):

```css
img { max-width: 100%; height: auto; }
```

Plus, to defend against the explicit `width="..."`/`height="..."` HTML attributes used on a few chapter-opener and avatar images, the `height: auto` half of the rule will force the browser to recalculate the height when the width is clamped to 100% of the parent. This is the standard responsive-image idiom and is also what Kindle Previewer 3 / KDP expects.

A narrower fix (lower blast radius) is `.diagram-container img { max-width: 100%; height: auto; }`, but a global rule is safer because it also catches future `<img>` insertions outside `.diagram-container`/`.illustration`.

---

## 2. Per-category counts (hard constraint)

| Category | Count | Examples (file:line) |
|---|---:|---|
| Images with explicit `width >= 800` px | 1 | `part-9-safety-strategy/module-30-safety-ethics-regulation/index.html:32` (`width="1376"`) |
| Images with explicit `height >= 800` px | 0 | (none) |
| Images with both `width` and `height` set | 250 | 248 are 28x28 inline agent avatars (Sage/Tensor/etc.), benign. The other 2 are: `part-9-safety-strategy/module-30-safety-ethics-regulation/index.html:32` (1376x768) and the chapter-opener `<img>` in the same template pattern |
| Images inside `<figure>` lacking `class="illustration"` | 8 | see table below |
| Images linking to a `.svg` >1MB on disk | 0 | (none) |
| Raster `<img>` inside `.diagram-container` (no CSS max-width applies) | **154** | see "Raster diagrams >=1500px" table below |
| Raster `.diagram-container` images whose source file is >=1500 px wide OR extreme aspect ratio (>=4:1) | **52** | see table below |

### `<figure>` elements without `class="illustration"`

These figures bypass the `.illustration img` responsive rule. They will still rely on the parent or any new global `img` rule.

| File:Line | Wrapper class | src |
|---|---|---|
| `front-matter/fm-what-this-book-covers.html:69` | `diagram` | `images/fm-3-1-dependency-diagram.png` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html:167` | (no class) | `images/figure-12.4.2.png` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html:212` | (no class) | `images/figure-14.1.3.png` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.7.html:60` | (no class) | `images/figure-14.7.1.png` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html:108` | `diagram-container` | `images/hf-rlhf-training.png` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html:113` | `diagram-container` | `images/huyenchip-rlhf-pipeline.png` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.1.html:200` | (no class) | `images/fig-31.1.1-ai-readiness-bars.png` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html:287` | (no class) | `images/figure-30.5.1.png` |

### Raster diagrams with source-file width >=1500 px (top 20 worst offenders by aspect ratio)

These render unbounded in a desktop browser when the viewport is wider than the source image, and they are precisely the images at risk of overflowing the print/Kindle page area.

| File:Line | Source dims (W x H) | Aspect | src |
|---|---|---:|---|
| `part-7-multimodal-applications/module-26-multimodal/section-26.1.html:75` | 6210 x 474 | 13.1 : 1 | `fig-26.1.7-ddpm-forward-reverse.png` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html:56` | **5427 x 432** | **12.6 : 1** | **`fig-35.1.1-token-to-dollar-pipeline.png`** (user-flagged "Fig 35.1.2") |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html:218` | 6093 x 852 | 7.15 : 1 | `fig-35.4.6-continuous-steering-loop.png` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html:153` | 3483 x 537 | 6.49 : 1 | `fig-1.3.2-skipgram-network.png` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.3.html:299` | 6456 x 1059 | 6.10 : 1 | `fig-33.3.3-attention-variants-taxonomy.png` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.3.html:99` | 6288 x 1092 | 5.76 : 1 | `fig-33.3.2-mamba-vs-transformer.png` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html:51` | 4050 x 768 | 5.27 : 1 | `fig-26.5.1-vision-language-action-pipeline.png` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.2.html:48` | 5835 x 1347 | 4.33 : 1 | `fig-14.2.4-evol-instruct-operators.png` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.2.html:44` | 5571 x 1560 | 3.57 : 1 | `fig-23.2.1-multi-agent-topologies.png` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.1.html:105` | 4722 x 1350 | 3.50 : 1 | `fig-3.1.7-rnn-unrolled.png` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.4.html:66` | 4125 x 1299 | 3.18 : 1 | `fig-33.4.2-world-model-architecture.png` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html:81` | 2520 x 918 | 2.75 : 1 | `fig-8.1.2-...png` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html:101` | 2463 x 954 | 2.58 : 1 | `fig-8.5.1-...png` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html:198` | 2030 x 909 | 2.23 : 1 | `rag-pipeline-nvidia.png` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.2.html:136` | 4626 x 2115 | 2.19 : 1 | `fig-3.2.5-bahdanau-attention.png` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html:222` | 1800 x 1053 | 1.71 : 1 | `fig-9.3.3-tree-structured-verification...png` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html:230` | 1800 x 1053 | 1.71 : 1 | `fig-6.6.4-pipeline.png` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:72` | **1800 x 1053** | **1.71 : 1** | **`fig-11.1.2-llm-api-ecosystem.png`** (user-flagged "Fig 11.1.2") |

A full list of 52 such files is in `.figure-audit-categories.json` (kept alongside this report for reference; safe to delete).

---

## 3. The two user-reported figures

### Figure 35.1.2 — `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html:56`

Exact tag (line 56):

```html
<img alt="Token-to-dollar pipeline showing how a user request flows through the application layer, prompt assembly, tokenizer, and LLM provider API, where input and output tokens are multiplied by per-token rates and aggregated into a monthly invoice" src="images/fig-35.1.1-token-to-dollar-pipeline.png"/>
```

- **Wrapper**: `<div class="diagram-container">` (line 55). No CSS `max-width` rule applies to `<img>` here — only to `svg`.
- **Source file**: `part-11-idea-to-product/module-35-shipping-scaling/images/fig-35.1.1-token-to-dollar-pipeline.png`
- **Dimensions**: **5427 x 432 px** (aspect ratio 12.56:1) — extreme panorama
- **File size**: 100 KB
- **Naming note**: the file is named `fig-35.1.1-...` but the caption labels it "Figure 35.1.2". Cosmetic mismatch, not a sizing issue.

**Why it overflows.** No global `img { max-width: 100% }` rule exists, and `.diagram-container` only constrains SVG. The browser therefore renders the PNG at its native 5427 px width on any viewport wider than 5427 px, and at its natural pixel size (clipped or scrolled horizontally) on narrower viewports — which is every viewport.

**Suggested fixes (in order of preference, lowest blast radius first)**:

1. **CSS-only, one line, fixes all 154 diagram-container images at once**: add `.diagram-container img { max-width: 100%; height: auto; }` to `book.css`. Recommended.
2. **Even safer**: add a global `img { max-width: 100%; height: auto; }` near the top of `book.css`.
3. **Image-level**: re-export this panorama at, say, 2400 px wide or split it into two stacked panels. Helps Kindle file-size budgets even after the CSS fix.
4. **HTML-level**: do not add explicit `width`/`height` attributes here — they will lock the aspect ratio and still overflow narrow viewports. The CSS fix is sufficient.

### Figure 11.1.2 — `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:72`

Exact tag (line 72):

```html
<img alt="LLM API ecosystem: application connecting to OpenAI, Anthropic, Google, Enterprise, and Open Source providers via common HTTP POST JSON pattern" src="images/fig-11.1.2-llm-api-ecosystem.png"/>
```

- **Wrapper**: `<div class="diagram-container">` (line 71). Same uncapped-`<img>` problem.
- **Source file**: `part-3-working-with-llms/module-11-llm-apis/images/fig-11.1.2-llm-api-ecosystem.png`
- **Dimensions**: **1800 x 1053 px** (aspect ratio 1.71:1)
- **File size**: 472 KB

**Why it overflows.** At desktop sizes the image renders at its native 1800 px width, which is more than 2x the 820 px content column. On wide viewports it spills outside the column and looks oversized relative to the body text. On Kindle/print it scales beyond the typeset area for the same reason.

**Suggested fixes**: identical to figure 35.1.2 — the single CSS rule `.diagram-container img { max-width: 100%; height: auto; }` resolves both at once, plus the other 152 raster diagrams listed above.

---

## 4. Summary

- **Single root cause** explains both user-reported overflows and ~150 latent overflows across the book: `.diagram-container` constrains SVG but not `<img>`, and there is no global `img { max-width: 100% }`.
- **Hard-constraint risk from explicit pixel attributes** is minimal: only 1 image has `width >= 800` (`width="1376"` on the Module 30 chapter opener), and it sits in `<figure class="illustration">` so the `.illustration img { max-width: 100% }` rule already restrains it on the web — though `width="1376"` can still mis-render in older/email/RSS readers that ignore CSS.
- **8 `<figure>` elements** drop the `illustration` class, relying on the (currently missing) global rule. These should be fixed too, but only after the CSS rule lands.

Recommended single-line patch (await user confirmation before applying): add the global rule above and/or `.diagram-container img { max-width: 100%; height: auto; }` to `styles/book.css`.
