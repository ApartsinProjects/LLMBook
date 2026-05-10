# Figure Audit — Root Cause Analysis & Improvement Proposals

**Analysis only. No source modified. No regenerations applied.** This document lays out what's wrong with Figure 4.2.2 (the example you flagged), why the same problem affects ~50+ other figures in the book, and a concrete plan for using Gemini to regenerate the worst offenders.

---

## 1. Figure 4.2.2 — what's actually wrong

**Source:** [`part-1-foundations/module-04-transformer-architecture/section-4.2.html`](part-1-foundations/module-04-transformer-architecture/section-4.2.html) line 87
**File:** `images/fig-4.2.2-decoder-only.png` (3288×2442 px, 107 KB, aspect 1.35)
**Caption:** "Architecture of our decoder-only Transformer. N blocks of self-attention + FFN with Pre-LN ordering, followed by a final normalization and linear projection."

### What you see when you look at it

A Mermaid-rendered architecture diagram. The "Transformer Block (×N)" container takes up the upper-left ~60% of the canvas as a vertical stack: LayerNorm → Causal Multi-Head Self-Attention → "+ residual" → LayerNorm → Feed-Forward → "+ residual". The Token+Position Embedding sits to the LEFT of the block. The Final LayerNorm → Linear → Softmax flow extends to the RIGHT of the block.

### Six concrete problems

1. **L-shaped composition is hard to read.** Two flow directions (down through the block, then right out to Final LayerNorm) force the eye to make a sharp left-to-right transition mid-diagram. Standard flowcharts go either top-to-bottom OR left-to-right consistently.
2. **The "x N" repetition isn't visualized.** "Transformer Block (× N)" is a label, not a visual cue. Real Transformer diagrams stack 2-3 ghost copies behind the block to suggest repetition. This one doesn't.
3. **"+ residual" as a separate box is misleading.** In real Transformers, residuals are connections from the input of a sublayer to its output (a curved arrow that bypasses the operation). Showing them as standalone nodes implies they are computational steps, which is wrong, or at minimum confusing for readers learning the architecture for the first time.
4. **No labels on the arrows.** Every arrow is identical. There's no visual difference between "flow of activations" and "residual bypass" connections.
5. **Inefficient whitespace.** The block container is roughly 2× as tall as it needs to be. The right side of the canvas (between the block and Final LayerNorm) is empty. Result: at Kindle sizes the boxes shrink to illegibility.
6. **Aspect ratio fights the page.** 3288×2442 is roughly 4:3 landscape. Kindle pages are portrait. The diagram fits the page width with massive vertical letterboxing, then becomes too small to read.

### What it should look like

The reference standard for this figure is the original "Attention Is All You Need" Figure 1, redrawn for decoder-only:

- **Vertical stack only** (no horizontal flow)
- **Residuals shown as curved bypass arrows** with explicit "Add" nodes (the actual operation)
- **2-3 ghost block outlines** behind the active block, suggesting the "× N" repetition visually
- **One arrow style** for forward activations, **another** for residual bypass (e.g. dotted)
- **Compact, near-square aspect** (e.g. 1200×1500), so it fits Kindle without shrinking
- **Larger labels** on each box

---

## 2. Root cause — this is a systemic pattern, not a one-off

Inventory of the project's figure assets:

| Pattern | Count | Notes |
|---------|------:|-------|
| Total `fig-N.M.K-*.png` files referenced | **130** | Auto-named figures, mostly Mermaid-rendered |
| `<div class="diagram-container">` wrappers in source HTML | **157 pages** affected | Same wrapper as figure 4.2.2 |
| Wide-aspect figures (aspect > 1.6) | **54** | Letterboxed on portrait readers |
| Tall figures (aspect < 0.6) | **40** | Cropped or scrolled on landscape readers |
| Square-ish figures (0.85–1.2) | 11 | Best fit for Kindle |
| Ultra-wide (aspect > 4) | **3** | `fig-20.3-graphrag-pipeline.png` (3.32), `fig-34.10-domain-tokenization.png` (**6.58**!), `fig-2.2.5-byte-level-bpe...` (2.52) |
| Ultra-tall (aspect < 0.4) | **9** | `fig-30.5.1-otel-llm-trace.png` (0.34), `fig-3.1.6-encoder-decoder-seq2seq` (0.34), etc. |

The figures all share a similar visual fingerprint: simple rectangle nodes, sans-serif labels, gray arrows, pastel-blue/orange/purple color fills. Strongly suggests they were all rendered from Mermaid source via `scripts/mermaid/` (which exists in the repo). The Mermaid auto-layout algorithm makes the same composition mistakes everywhere:

- Flowcharts are laid out by topological sort, not by visual balance
- Containers (subgraphs) get ballooned to fit the largest child
- No control over arrow routing → arrows go wherever
- Default colors and fills are weak; no information encoded in color

### Other figures with the same problems as 4.2.2

Sampled from the inventory, these are very likely to have the L-shape / wasted-whitespace / bad-residual problem:

**Highest priority** (in foundational chapters readers see first):
- `fig-3.1.6-encoder-decoder-seq2seq.png` (1035×3066, aspect 0.34 — ultra-tall)
- `fig-3.1.5-the-lstm-cell.png` (3519×1653, aspect 2.13 — wide)
- `fig-3.3.3-multi-head.png` (2874×1815, aspect 1.58 — landscape)
- `fig-4.1.7-residual-stream.png` (3279×1626, aspect 2.02 — wide)
- `fig-4.1.7-pre-post-ln.png` (1905×1686, aspect 1.13 — squarish but Mermaid-style)
- `fig-4.3.6-pre-post-ln2.png` (1569×3978, aspect 0.39 — ultra-tall, very thin)
- `fig-2.2.5-byte-level-bpe-starts-with-256-byte-tokens.png` (3483×1383, aspect 2.52)

**Moderate priority** (production / appendix chapters):
- `fig-30.5.1-otel-llm-trace.png` (1263×3714, aspect 0.34 — Gantt-chart-tall)
- `fig-31.6.3-saga-compensation.png` (801×2583, aspect 0.31 — ultra-tall)
- `fig-26.4.2-error-recovery-decision.png` (1335×3711, aspect 0.36)
- `fig-25.7.1-coding-agent-generations.png` (924×2643, aspect 0.35)

**Worst-aspect outliers** (will not render at all on Kindle):
- `fig-34.10-domain-tokenization.png` — **6.58 aspect** (8049×1224). Unreadable on any reader.
- `fig-31.6.4-retry-taxonomy.png` — 1.50 (better, but mermaid-style)

---

## 3. Improvement strategy with Gemini

### Two regeneration modes

**Mode A: artwork-only redraw via Gemini Pro Image**
- Best for: structural diagrams (architectures, pipelines) where the labels are short and well-defined
- Process: write a careful prompt describing the components, layout style, and intended aspect (~3:4 portrait or square); Gemini generates an SVG-feeling illustration with proper visual hierarchy
- Caveat: text rendering still imperfect; Gemini may invent labels or misspell technical terms

**Mode B: artwork + manual label overlay**
- Best for: precision diagrams (math notation, specific tensor shapes, exact pseudocode)
- Process: prompt Gemini for the artwork only (no text); composite labels in an editor (Affinity, Inkscape, even PIL) afterward
- Caveat: more manual work, but produces the best result

### Suggested prompt template (Mode A) for Figure 4.2.2

```
Diagram for a technical AI textbook, vertical/portrait orientation
(3:4 aspect ratio), clean modern flat-vector style, white background,
high contrast.

Subject: a single decoder-only Transformer architecture, drawn
top-to-bottom in a single column.

Layout (top to bottom):
  1. Box: "Token + Position Embedding" (input)
     ↓ (single arrow down)
  2. A box outlined with a dashed border labeled "Transformer Block × N",
     containing 4 stacked sub-blocks with curved residual bypass arrows:
       a. "LayerNorm" → "Causal Multi-Head Self-Attention" → "+" (with curved bypass arrow from input of LayerNorm)
       b. "LayerNorm" → "Feed-Forward (SwiGLU)" → "+" (with curved bypass arrow from output of step a)
     Behind this main block, draw 2 ghost duplicates offset by ~10px to
     suggest repetition.
     ↓
  3. Box: "Final LayerNorm"
     ↓
  4. Box: "Linear (d_model → vocab)"
     ↓
  5. Box: "Softmax" (output)

Visual encoding:
- Forward activation arrows: solid gray
- Residual bypass arrows: dotted blue, curved
- Box fills: very light blue (#eef4fa) for normal layers, light purple
  (#f4ecf7) for normalization layers, light green (#ecf6ee) for
  output/loss
- Sans-serif labels, 18pt, high contrast

NO TEXT BEYOND THE LABELS LISTED ABOVE.
```

### Per-figure proposal table

For each highest-priority figure, here's a concrete Gemini prompt direction:

| Figure | Current problem | Gemini approach |
|--------|----------------|-----------------|
| `fig-4.2.2-decoder-only.png` | L-shape, no ghost blocks, residuals as boxes | See template above |
| `fig-3.1.5-lstm-cell.png` | Wide aspect, internal cell components hard to follow | Square portrait, cell as central box with explicit gates (input, forget, output) labeled, cell-state line at top with green color encoding |
| `fig-3.1.6-encoder-decoder-seq2seq.png` | Ultra-tall, gets cropped | Two side-by-side stacks (encoder left, decoder right), arrows between them — re-aspected to 4:3 landscape |
| `fig-3.3.3-multi-head.png` | Mermaid auto-layout puts heads in awkward grid | 3-row stack: input embeddings → 8 small parallel head boxes → concatenation → output projection |
| `fig-4.1.7-residual-stream.png` | Wide aspect, fundamental concept buried | Vertical "stream" as central column, with branches for each layer's contribution, labels on branches |
| `fig-4.3.6-pre-post-ln2.png` | Ultra-tall narrow column | Two side-by-side columns: "Post-LN (original)" vs "Pre-LN (modern)" — re-aspected to landscape |
| `fig-30.5.1-otel-llm-trace.png` | Gantt-chart-tall, won't fit | Compress to square; if still doesn't work, mark as "complex - read on tablet" callout |
| `fig-34.10-domain-tokenization.png` | 6.58 aspect — unreadable | Restructure into 3 stacked rows or split into 3 separate figures |

### Estimated effort and order

If you commit to regenerating the worst figures via Gemini:

| Phase | Figures | Time | Impact |
|-------|---------|------|--------|
| 1. Foundation chapters (3, 4) | 6 figures | ~3 hours | Most readers see these — biggest perception of quality |
| 2. Worst aspect outliers (6.58, ultra-tall) | 5 figures | ~2 hours | Readers literally can't see the current versions |
| 3. Production / appendix chapters | 12 figures | ~5 hours | Polish |

Total ~10 hours for ~25 figures redrawn.

### Recommended workflow

1. **Pick a candidate figure**, copy the current image somewhere (e.g., `KDP/validation/_figure_audits/before/`)
2. **Write the prompt** following the template above; verify it includes the EXACT labels, arrow types, and aspect ratio
3. **Generate via** `python KDP/cover/generate_cover_gemini.py` (extend the script to take an arbitrary prompt) OR a new dedicated script
4. **Inspect the output** — does the diagram preserve technical accuracy? Are labels spelled correctly?
5. **Iterate or accept**. If labels are wrong, run with "no text" and overlay manually
6. **Replace** the source PNG. Update the figure caption if the structure changed
7. **Rebuild EPUB** to verify

### What NOT to use Gemini for

- Math-formula diagrams (Gemini gets equations wrong; use KaTeX/MathJax in HTML instead)
- Code samples (already handled via Pygments — don't make them figures)
- Tables (the [tables_audit.md](tables_audit.md) covers these — convert to definition lists, not images)
- Tiny inline icons (the callout icons; use the existing PNG set)

---

## 4. Quick-win recommendations

If you want to spend ~1 hour rather than 10:

1. **Identify the 5 worst figures** by Kindle Previewer test (open EPUB on Paperwhite emulation; look for figures where text is illegible)
2. **For those 5, replace with a "this figure is best viewed on tablet/desktop" callout** + link to the web edition's interactive version. This is the lowest-effort fix that addresses the worst reader experience.
3. **Defer the full redraw to v2**

Quick-win HTML pattern:

```html
<div class="diagram-container">
    <img src="images/fig-X.Y.Z-name.png" alt="..." loading="lazy">
    <div class="diagram-caption"><strong>Figure X.Y.Z:</strong> ...</div>
    <div class="callout note">
        <div class="callout-title">Note</div>
        <p>This diagram has many small labels. For a high-resolution
        interactive version, see the web edition at
        <a href="https://llmbook.apartsin.com/figures/X-Y-Z">llmbook.apartsin.com</a>.</p>
    </div>
</div>
```

---

## 5. Open question: Mermaid source files?

If the original Mermaid source files are in `scripts/mermaid/` or somewhere similar, you could:

- Tweak the Mermaid layout directives (`flowchart TB` vs `LR`, `subgraph` aspect, edge labels)
- Re-render with a custom theme that uses better colors and arrow weights
- Set explicit max-width to match Kindle's ~600 px
- Use Mermaid's "elk" layout engine (better at minimizing edge crossings)

This may be a faster route than regenerating with Gemini for any figure where the Mermaid source still exists.

**Recommended check**: look in `scripts/mermaid/` for `.mmd` or `.mermaid` source files that match the figure names. If they exist, fix the source there and re-render with the existing tooling.
