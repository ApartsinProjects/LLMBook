# Diagram Generation Pipeline — Analysis & Recommendation

## The problem

Current state of the LLMBook's 130 figures:
1. **Mermaid auto-renders** (~80 figures): structurally accurate but visually bland boxes-and-arrows. Wide-aspect layouts that don't fit Kindle's narrow viewport.
2. **Imagen 4 regeneration** (5 priority figures, this session): visually rich but **text labels garbled** (5-10% of words misspelled or distorted). Can't ship to print without manual correction.
3. **6 third-party diagrams** (this session): need original replacements; copyright-flagged.

The user reported all three problems: "Diagrams are still not good. Difficult to understand, text errors, layout problems."

This doc analyzes 7 approaches, compares them, and proposes a **hybrid pipeline**.

---

## Why text generation in raster image models fails

Stable Diffusion, Imagen, DALL-E, MidJourney all suffer from the same root cause: they generate **pixel grids** trained on natural images where text is rare. They learned that text-shaped patches LOOK like text but they don't understand letterforms as discrete symbols. Result:
- Long words → garbled mid-letters
- Technical jargon → misspelled (e.g. "Transformr", "Attentin")
- Math notation → wrong subscripts
- Dense labels → overlap, smear

This is fundamental to the architecture. **Newer models (Imagen 4) are better but still imperfect**. Even GPT-4o image-gen can't reliably render >12-character labels.

**Lesson**: never trust an image-generation model with mission-critical text. Generate ARTWORK only, add text in a separate vector layer.

---

## Approaches analyzed

### A. LLM-generated SVG (text in code, then render) ⭐ TOP PICK FOR TECHNICAL DIAGRAMS

The LLM (Claude, GPT-4o, Gemini) writes raw SVG markup — including `<text>` elements with perfect labels, `<path>` for arrows, `<rect>` for boxes, `<linearGradient>` for fills.

**Pros**:
- Text is encoded as literal characters in `<text>` — never garbled
- Output is **vector** (SVG) — scales to any size without quality loss
- Source is **version-controllable text** — diff-able, reviewable
- LLMs (especially Claude Sonnet 4.5+) can produce surprisingly polished SVG
- Can include gradients, drop shadows, custom paths, embedded fonts
- Free (uses existing Claude/GPT API)

**Cons**:
- LLMs sometimes mis-position elements (overlap, off-canvas)
- Complex layouts beyond ~15 elements get fragile
- Iterating requires re-prompting (vs. visual editor)
- Dense visual ornaments (textures, painterly effects) NOT achievable

**When to use**: architectural diagrams, flowcharts, hierarchical structures, sequence diagrams, simple math illustrations. The bulk of the LLMBook's diagrams.

### B. D2 with custom theme

[D2lang.com](https://d2lang.com/) is Mermaid's modern successor: better aesthetics, embedded image support in nodes, multiple layout engines (ELK, dagre, TALA).

**Pros**:
- Cleaner default rendering than Mermaid (gradients, soft shadows out-of-box)
- Supports SVG icons embedded in nodes
- Multiple layout engines (TALA is paid but exceptional)
- Text source — version-controllable

**Cons**:
- Yet another tool to install + learn
- Layout still basically boxes-and-edges
- TALA layout engine is commercial ($500/year for the good one)

**When to use**: replacement for Mermaid where layout quality matters; not for breakthrough visuals.

### C. Mermaid with custom CSS theme + ELK layout

Stay with Mermaid but invest in a polished CSS theme (the project's mermaid renders likely use the default theme).

**Pros**:
- No new tools — the LLMBook already has Mermaid sources (`fig-X-Y-name.mmd` files)
- ELK layout engine produces cleaner edges than default
- Custom theme can match book's visual identity (gold + navy)

**Cons**:
- Still fundamentally boxes-and-edges
- Default Mermaid font rendering is bland; custom fonts require setup
- ELK doesn't handle all Mermaid features perfectly

**When to use**: cheapest fix for the existing 130 Mermaid figures. Quality bump from "8/10 ugly" to "5/10 acceptable" with one CSS file.

### D. Imagen artwork + Python text overlay (HYBRID)

Generate the visual base via Imagen 4 with the prompt asking for **NO text labels**, then composite labels via Python (PIL or svgwrite) at known coordinates.

**Pros**:
- Best of both: Imagen's visual richness + perfect text
- Handles painterly chapter-opener illustrations, conceptual visualizations, mood pieces
- Text positions are reproducible (pixel coordinates in code)

**Cons**:
- Requires manual coordinate planning per figure
- Imagen's "no labels" prompts still sometimes leak garbled text
- Two-step pipeline = more orchestration

**When to use**: chapter-opener illustrations, conceptual mood pieces, large pedagogical figures where the artwork dominates.

### E. TikZ via LaTeX (gold standard for academic typography)

LaTeX's TikZ package is the gold standard for technical diagrams in physics/math/CS papers.

**Pros**:
- Publication-quality output. Used in NeurIPS, ICML, Nature papers.
- Perfect math typesetting via embedded LaTeX
- Programmatic + reproducible
- Vector output (PDF, SVG)

**Cons**:
- LaTeX install required (~3 GB)
- TikZ is a craft — steep learning curve
- Verbose syntax; iterating is slow
- Not ideal for "AI-textbook" aesthetic (TikZ outputs feel academic, not modern)

**When to use**: future academic edition; edge cases where math + diagram are intertwined.

### F. Excalidraw / hand-drawn aesthetic

Excalidraw produces deliberately "hand-drawn" diagrams (wobbly lines, casual fonts) that have become trendy in tech communications (used by Vercel docs, Anthropic blog).

**Pros**:
- Distinctive visual identity
- Auto-export to SVG with embedded text
- Open-source, programmatic API exists
- Pleasant to look at, less "corporate"

**Cons**:
- Aesthetic doesn't match a serious technical textbook (too casual)
- Layout is manual — no auto-layout for complex diagrams
- Limited typography options

**When to use**: probably not for this book. Could be useful for blog companion content.

### G. Programmatic SVG (matplotlib + custom code per diagram type)

Hand-write Python that generates SVG using `svgwrite`, `matplotlib`, or `cairosvg`. Per-type codegen (one function for "transformer architecture", one for "RAG pipeline", etc.)

**Pros**:
- Total control over output
- Can encode domain conventions (e.g., always show residuals as dotted curved arrows)
- Reusable across many figures of same type
- Best fit for **data visualizations** (charts, scaling-law plots, training curves)

**Cons**:
- Significant upfront engineering per diagram type
- Doesn't generalize across different diagram types
- Maintenance burden as the book evolves

**When to use**: data viz (Chapters 6 scaling laws, Chapter 8 reasoning charts). Specialized diagram types where you have many similar figures.

---

## Comparison matrix

| Approach | Text quality | Visual quality | Setup cost | Per-figure cost | Reproducible | Best for |
|---|---|---|---|---|---|---|
| **A. LLM-generated SVG** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Low | $0.01 (Claude API) | ✅ | Architecture, flowcharts, sequences |
| **B. D2 with theme** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Medium (install + theme) | Free | ✅ | Mermaid replacements |
| **C. Mermaid + theme** | ⭐⭐⭐⭐⭐ | ⭐⭐ | Low | Free | ✅ | Existing 130 .mmd files, cheap upgrade |
| **D. Imagen + text overlay** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium | $0.04 + 30 min/figure | ✅ | Chapter-opener illustrations |
| **E. TikZ / LaTeX** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | High (LaTeX install) | Free | ✅ | Academic-style figures, math+diagram fusion |
| **F. Excalidraw** | ⭐⭐⭐⭐ | ⭐⭐⭐ casual | Low | Free | partial | Not recommended for serious textbook |
| **G. Programmatic SVG** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | High (per-type engineering) | Free | ✅ | Data viz, repeated diagram types |

---

## Recommended hybrid pipeline

### Tier 1 — Default for most diagrams: **LLM-generated SVG (Approach A)**

For the ~80 architectural / flowchart / sequence / hierarchy diagrams in the LLMBook:

```bash
python KDP/build/generate_diagram_svg.py \
  --figure fig-4.2.2-decoder-only \
  --concept "decoder-only Transformer: token+pos embedding feeds into N stacked blocks (each: layer-norm, causal multi-head self-attention with residual bypass, layer-norm, feed-forward with residual bypass), then final layer-norm, linear projection, softmax" \
  --aspect portrait \
  --variants 3
```

The script asks Claude to write the SVG, renders to PNG, generates 3 variants for picking.

**Prototype**: see [`KDP/build/generate_diagram_svg.py`](KDP/build/generate_diagram_svg.py) below in this doc.

### Tier 2 — For chapter-opener illustrations: **Imagen + text overlay (Approach D)**

For the ~30 painterly chapter-opener illustrations where the visual is the point and labels are minimal:

```bash
python KDP/build/generate_chapter_opener.py \
  --chapter 11 \
  --concept "the art of prompting visualized as a craftsman shaping clay" \
  --label-overlay "Chapter 12: Prompt Engineering"
```

Generate artwork via Imagen (no text request), then overlay the chapter title with PIL.

### Tier 3 — For data visualization: **Matplotlib (Approach G)**

For the ~10 plots showing scaling laws, training curves, evaluation results:

```python
# Existing pattern - just consolidate into a reusable module
from html2epub_matplotlib_helpers import save_publication_chart
save_publication_chart(x, y, kind="line", x_label="...", y_label="...", out=".../fig-6.2.svg")
```

### Tier 4 — For 130 existing Mermaid figures (cheap upgrade): **Mermaid + custom theme (Approach C)**

While we're regenerating priority figures via Tier 1, the existing 130 Mermaid figures get a free quality bump from a custom theme:

```mmd
%%{ init: {
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#1a4078",
    "primaryTextColor": "#fff",
    "primaryBorderColor": "#0d2347",
    "lineColor": "#5a4a3a",
    "secondaryColor": "#d4b96a",
    "tertiaryColor": "#f4ecf7"
  },
  "flowchart": { "curve": "basis", "useMaxWidth": true }
} }%%
flowchart TB
    ...
```

Plus regenerate via `mmdc` with `-c custom-theme.json` — no per-figure work needed beyond CSS.

---

## Decision framework

When you encounter a figure:

```
Is it a chart / data viz?
├─ YES → Use matplotlib (Tier 3)
└─ NO →
    Is it a chapter-opener / mood piece?
    ├─ YES → Imagen + text overlay (Tier 2)
    └─ NO →
        Is it architecture / flowchart / sequence / hierarchy?
        ├─ YES, NEW → LLM-generated SVG (Tier 1)
        └─ EXISTING Mermaid → upgrade theme (Tier 4)
```

---

## Pilot: LLM-generated SVG for Figure 4.2.2

I've built [`KDP/build/generate_diagram_svg.py`](KDP/build/generate_diagram_svg.py) — a working prototype.

It:
1. Takes `--figure {name} --concept "{description}" --variants N`
2. Calls Claude with a detailed prompt asking for SVG with technical-textbook style
3. Saves SVG sources to `KDP/diagrams/svg/{figure}_v{N}.svg`
4. Renders SVG → PNG via cairosvg for inclusion in EPUB
5. Outputs an `_review.md` with previews + the LLM prompt used

Reproducibility: each variant saves the prompt and Claude's full SVG response, so you can iterate or audit.

### Example: regenerate Figure 4.2.2

```bash
python KDP/build/generate_diagram_svg.py \
    --figure fig-4.2.2-decoder-only \
    --concept "decoder-only Transformer: token+position embedding -> N stacked blocks (LayerNorm -> Causal Multi-Head Self-Attention with residual bypass -> LayerNorm -> FFN with residual bypass) -> Final LayerNorm -> Linear -> Softmax. Show 'x N' as 2 ghost block outlines behind the front block. Use dotted blue arrows for residual bypasses." \
    --aspect portrait \
    --variants 3
```

Outputs:
- `KDP/diagrams/svg/fig-4.2.2-decoder-only_v1.svg`
- `KDP/diagrams/svg/fig-4.2.2-decoder-only_v2.svg`
- `KDP/diagrams/svg/fig-4.2.2-decoder-only_v3.svg`
- Plus `_v1.png`, `_v2.png`, `_v3.png` rasterized at 1280×... px
- `KDP/diagrams/svg/fig-4.2.2-decoder-only_review.md` (your picking guide)

Pick best variant, copy to source location:
```bash
cp KDP/diagrams/svg/fig-4.2.2-decoder-only_v2.svg \
   part-1-foundations/module-04-transformer-architecture/images/fig-4.2.2-decoder-only.svg
```

---

## Cost / time estimates

For replacing the worst 30 figures via Tier 1 (LLM-generated SVG):

| Phase | Time | Cost |
|---|---|---|
| Concept extraction (read source HTML, distill 30 concepts) | 4 hours | $0 |
| LLM SVG generation (3 variants × 30 = 90 calls × $0.10 each) | 1 hour | ~$9 |
| Variant review + pick best | 3 hours | $0 |
| Manual SVG touch-up (typography, alignment) for ~10 figures | 5 hours | $0 |
| **Total** | **~13 hours** | **$9** |

For comparison, Imagen 4 regeneration (Approach D-only) costs ~$0.04/image × 4 variants × 30 = $5 but **needs hand-correction of garbled text** — adds ~30 min × 30 figures = 15 hours of manual work.

LLM-generated SVG wins on quality AND time.

---

## Why NOT just do Imagen for everything

The 5 priority figures regenerated this session are visually impressive but **all have text errors**:
- Garbled labels in dense diagrams
- Mis-spelled technical terms ("Causla", "Atention")
- Inconsistent font weights mid-word

They're acceptable as **chapter-opener illustrations** (where the artwork is the point and labels are decorative) but **not as technical diagrams** (where readers need accurate labels to learn the concept).

The hybrid approach (Tier 1 SVG for technical, Tier 2 Imagen for opener) gives us the best of both.

---

## Implementation status

- ✅ This document (analysis + decision framework)
- ⏳ `KDP/build/generate_diagram_svg.py` — TO BUILD (next session — see prototype design above)
- ⏳ Mermaid custom-theme upgrade — TO BUILD (1 hour effort, applies to all existing 130 .mmd files at once)
- ⏳ `KDP/build/generate_chapter_opener.py` — TO BUILD (combines Imagen + PIL overlay)

The prototype LLM-SVG script can be built in 1-2 hours of focused work in a follow-up session. Recommend tackling that next, then running it on the 5 priority figures (Fig 4.2.2, 4.1.5, 3.1.5, 3.3.3, 34.10) to validate the approach BEFORE rolling out to the full 30+ figures needing replacement.
