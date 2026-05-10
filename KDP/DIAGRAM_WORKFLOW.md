# Diagram Design Workflow — High-Quality Technical Visuals via Gemini

Most diagrams in the book today are Mermaid-rendered flowcharts — boxes with arrows. They have known problems: bad layouts, ugly text, no visual encoding of meaning, illegible at small Kindle sizes (see [`validation/figure_audit.md`](validation/figure_audit.md) and [`validation/diagram_audit.md`](validation/diagram_audit.md) for specifics).

This document defines a **design + test workflow** for creating high-quality technical infographics using **Gemini Pro Image** (gemini-3-pro-image-preview). Goal: visuals that *teach* by showing the actual mechanism, not just labelling boxes.

---

## Principles

### Avoid these patterns
- Boxes connected by arrows (Mermaid default)
- "Things go in → process → things come out"
- Square / vertical stacks of equally-weighted shapes
- Pure text labels with no visual anchor
- Diagrams that could be replaced by a single sentence

### Aim for these patterns
- **Visual metaphor of the actual mechanism** — show what's happening, not just label it
- **Visual hierarchy** — most important element is biggest / brightest / centered
- **Information density** — each element teaches something specific
- **Asymmetric layouts** — when the data has asymmetry (e.g., training vs. inference), reflect it
- **Concrete examples** — show real numbers, real tokens, real attention patterns where possible
- **Annotation, not labels** — arrows and callouts pointing to specific features

### Examples of what "good" looks like

| Topic | Bad version | Good version |
|-------|-------------|--------------|
| Self-attention | 4 boxes labeled Q, K, V, Output, arrows | Heatmap of attention weights over actual tokens, with annotations: "this token attends here because of subject-verb agreement" |
| Tokenization (BPE) | "Text → Tokens" arrow | Visual byte stream being merged step-by-step into tokens, with frequency counts shown growing |
| Residual stream | Box with "+" symbol | Side-view of the stream as a flowing river, layers as tributaries adding/subtracting features at known positions |
| Transformer block | Stack of boxes labeled LayerNorm, MHA, FFN | Cross-section showing the activation transformation through each sublayer, with example values colored by magnitude |
| Loss landscape | Generic 3D parabola | Actual loss surface from a real training run, with the optimization trajectory traced over it |

---

## Workflow

### Phase 1 — Concept

1. **Identify the figure** that needs improving (use figure_audit.md as input)
2. **Read the surrounding chapter prose** carefully. What concept is the diagram supposed to teach?
3. **Verify your understanding** of the concept (check the chapter's prose, then verify against an authoritative source — Karpathy lectures, Vaswani et al., the relevant paper)
4. **Articulate in one sentence** what a reader should learn from looking at the diagram
5. **List the 3-5 visual elements** that must be present to teach that concept

### Phase 2 — Design prompt

Build a prompt with these components, in order:

```
[ART STYLE]
Diagram for a technical AI textbook. Clean modern flat-vector style.
[Layout: portrait/landscape, aspect ratio]. Light off-white background.
High contrast text. Color palette: deep navy (#0d1226), gold (#d4b96a),
muted teal (#7fc6c0), soft red (#e94560). Use color sparingly and
purposefully - color must encode information, not just decorate.

[CONCEPT]
[1 sentence: what is the diagram showing?]

[ELEMENTS]
The diagram contains the following labeled elements:
1. [Element A]: [description, position, color encoding]
2. [Element B]: [description, position, color encoding]
3. [Element C]: [description, position, color encoding]

[VISUAL HIERARCHY]
[What is the most important element? How is it visually emphasized?]

[ANNOTATIONS]
[What arrows/callouts/labels point at what? What is each label's exact text?]

[AVOID]
- Generic boxes-and-arrows flowcharts
- Equal weighting of all elements
- Decorative color (every color must mean something)
- Vague labels like "process" or "output"
- Watermarks or signatures

[OUTPUT]
PNG, [aspect: 4:3 / 3:4 / 16:9], at least 1600 px on longest side,
suitable for printing at 300 DPI in a book chapter.
```

### Phase 3 — Generate

Use `gemini-3-pro-image-preview` (highest quality). Sample command:

```bash
python KDP/build/regenerate_figure.py \
    --figure 4.1.5 \
    --prompt-file KDP/diagrams/prompts/fig-4.1.5-pre-post-ln.md \
    --output part-1-foundations/module-04-transformer-architecture/images/fig-4.1.5-pre-post-ln-v2.png
```

(That script doesn't exist yet — it's the next file to write when you commit to this workflow.)

### Phase 4 — Audit before applying

**CRITICAL**: do not auto-replace the figure. Use this checklist:

- [ ] **Is the technical content correct?** Print the image, read it carefully against the chapter prose. Are the labels right? Are the relationships shown accurate?
- [ ] **Does the visual hierarchy match the importance?** The "key" element should be the eye's first stop.
- [ ] **At thumbnail size (200 px wide), is anything legible?** Most readers scroll, the eye samples thumbnails first.
- [ ] **Does it work in monochrome?** Many Kindle devices are e-ink. Open in a B&W viewer.
- [ ] **Does it teach something the prose doesn't already?** If the diagram is just a visual restatement, it adds noise; cut it.
- [ ] **Compare side-by-side with the old version**. The new one should be unambiguously better — if it's only "different", iterate.

### Phase 5 — Iterate

If the first generation isn't right:
- **Wrong content**: rewrite the prompt's CONCEPT and ELEMENTS sections, retry
- **Wrong layout**: add explicit positioning constraints ("X is in the upper-left third")
- **Wrong style**: tighten the ART STYLE section ("more like an Edward Tufte data graphic, less like a corporate slide deck")
- **Labels misspelled**: usually unfixable in image generation; generate art-only and overlay text in Affinity/Figma

Generate 3-5 variants per concept. Keep the best one.

---

## Test approach (small batch first)

Don't redo all 50+ Mermaid diagrams at once. Start with **3 high-value figures** and validate the workflow:

1. **Figure 4.1.5 — Pre-LN vs Post-LN normalization**
   - Concept: Pre-LN and Post-LN are two different orderings of the residual + layer normalization, with empirically different training stability
   - Visual approach: side-by-side architecture comparison, with arrows showing the FLOW of activations and where normalization happens; color the residual stream consistently to show how normalization position changes what flows through it

2. **Figure 4.2.2 — Decoder-only Transformer architecture**
   - Concept: a single Transformer block stacked N times, with token embeddings in and softmax-over-vocab out
   - Visual approach: the canonical "stacked block with residual bypass curves" diagram from Vaswani et al. (Figure 1, decoder side), with ghost copies showing the × N

3. **Figure 4.3.3 — RoPE (Rotary Position Embeddings)**
   - Concept: positional information is encoded by *rotating* query and key vectors in 2D pairs by an angle proportional to position
   - Visual approach: actual 2D rotation visualization with vectors at different rotation angles, NOT text labels saying "pos=0 → no rotation"

Document outcomes in `KDP/diagrams/results/<figure>-iteration-N.md` with the prompt used, the output, and notes on what worked / failed.

---

## Promoting iteratively

For each successful redesign:
1. Save final PNG to source location: `images/fig-N.M.K-name-v2.png`
2. Update the corresponding `<img src="">` in the source HTML
3. Keep the original PNG (e.g., rename to `fig-N.M.K-name-v1-mermaid.png`) so the change is reversible
4. Rebuild the EPUB to verify in Kindle Previewer
5. After 3 confirmed wins, commit the workflow to the rest of the figures

---

## Tools

- **Gemini Pro Image** (`gemini-3-pro-image-preview`) via `KDP/cover/generate_cover_gemini.py` (extend or fork for figures)
- **Figma / Affinity Designer** for typography overlay if labels are wrong
- **Inkscape** if you need to clean up SVG output later
- **Kindle Previewer 3** for verification on real devices

---

## Estimated effort

| Activity | Time per figure |
|----------|----------------:|
| Concept articulation + prompt drafting | 20-30 min |
| Generation + iteration (3-5 variants) | 15-30 min |
| Audit + verification | 10-15 min |
| Source HTML update + commit | 5 min |
| **Total per figure** | **~1 hour** |

For 50 figures: ~50 hours of work. Realistic phasing: 5 figures/week over 10 weeks, alongside other book work.

---

## Anti-pattern: don't try to fix Mermaid

Tweaking Mermaid templates to produce better output is a dead end. Mermaid's strengths are speed and version control of source, not visual quality. If you commit to high-quality diagrams, accept that they are *artifacts*, not generated from text source. Trade off: you lose the ability to "diff" diagram source between editions, but you gain the ability to actually teach with them.

If you want both: keep Mermaid sources in `scripts/mermaid/` as fallback documentation of the *concept* a diagram represents, then redraw the diagram via Gemini for the published version.
