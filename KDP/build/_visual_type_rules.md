# Visual Type Decision Rules (v6.2)

When choosing how to represent a concept visually in this book, use this
decision tree. The goal is to match the visual type to the kind of
information being communicated.

---

## Decision Tree

```
Is the concept QUANTITATIVE (has axes, numeric values)?
├── YES → Matplotlib chart (bar, line, scatter, heatmap, etc.)
│         scripts/svg_to_matplotlib/gen_figure_*.py
│
└── NO → Does it have STRUCTURAL relationships
         (boxes + arrows, hierarchy, sequence, flow)?
         ├── YES, simple/sequential flow → Mermaid diagram
         │        scripts/mermaid/*.mmd → mmdc → .png
         │
         ├── YES, complex/architectural → Inline SVG
         │        Hand-authored in the .html file
         │
         ├── Many-to-many key→value mapping → HTML table
         │        with .data-table styling
         │
         └── NO → Is the concept METAPHORICAL or EMOTIONAL
                  (chapter opener, decorative, conceptual analogy)?
                  ├── YES → Gemini illustration
                  │         agents/book-skills/scripts/generate_icons_gemini.py
                  │
                  └── NO → Reconsider whether the concept needs a figure at all.
                          Often a well-written paragraph is the right answer.
```

---

## Concrete Examples

| Concept | Visual type | Why |
|---------|-------------|-----|
| GPT model parameter growth 2018-2024 | **Matplotlib** line chart | Has axes (year, log-params); reader needs to read off values |
| Softmax distribution at 3 temperatures | **Matplotlib** small-multiples bar chart | Quantitative; reader compares peaks |
| Power law L = a·N^(-α) | **Matplotlib** log-log line chart | Slope reading; mathematical claim |
| Encoder-decoder Transformer architecture | **Inline SVG** | Many boxes + arrows; reader traces data flow |
| RNN unrolled through time | **Mermaid** flowchart | Sequential boxes; same-shape repetition |
| BPE merge sequence | **Mermaid** flowchart | Step-by-step process |
| Skip-gram NN architecture | **Mermaid** flowchart | Layered structure |
| Bahdanau attention computation | **Mermaid** flowchart | Computation pipeline |
| Regulatory requirement → LLM capability → regulation | **Table** | Many-to-many mapping; reader scans rows |
| EU AI Act risk tier hierarchy | **Mermaid** flowchart | Tree structure; tier labels |
| Pre-training as a long apprenticeship | **Gemini** illustration | Pure metaphor; no structure to trace |
| Chapter opener for "Multimodal Generation" | **Gemini** illustration | Decorative; sets tone |
| Prompt template anatomy (System/Few-shot/User) | **Inline SVG** | Structural decomposition with sub-components |

---

## Anti-Patterns (DO NOT DO)

### ❌ Cartoon where alt text claims "chart"
Do not generate a Gemini illustration when the alt text or caption
implies a real chart will be present.

**Bad:** Figure 6.5.2 — alt text says "A graph showing learning rate
warmup followed by decay" but image is a kitchen-warmup cartoon.

**Fix:** Generate the chart in Matplotlib using the existing code in
the section.

### ❌ SVG with parallel columns and no arrows when caption says "mapping"
Do not draw 3 columns of boxes when the caption claims they are
"mapped" to each other. Either add explicit arrows OR use a table.

**Bad:** Figure 28.2.2 (original) — three colored columns side-by-side
with nothing connecting them, captioned "Each requirement maps to
specific LLM capabilities."

**Fix:** Convert to a 3-column table where each row IS the mapping.
(Done in v6.2.)

### ❌ Radar chart with fewer than 6 axes
Radar charts distort relative magnitudes through quadratic area
scaling; below 6 axes the distortion dominates.

**Bad:** Figure 33.1.1 — 4-axis radar (Data=4, Tech=3, Org=2,
Talent=3); the gap at "Org=2" looks less than half as bad as it is.

**Fix:** Horizontal bar chart with a reference line at the
"minimum viable" score.

### ❌ Two near-duplicate figures across sections
If two sections need essentially the same chart, make ONE canonical
and cross-reference from the other.

**Bad:** Figure 14.1.3 and Figure 15.7.3 both show crossing-curves
(task perf rising, general perf falling) with nearly identical visuals.

**Fix:** Keep 14.1 as canonical; 15.7 references 14.1 with a callout
explaining the continual-learning framing.

### ❌ Decorative cartoon immediately before a real chart
If the same concept is illustrated by both a cartoon and a chart in
the same section, drop the cartoon.

**Bad:** Figure 6.1.2 (rocket cartoon) appears 14 lines before
Figure 6.1.6 (real parameter-growth matplotlib chart).

**Fix:** Remove the cartoon; the chart conveys the same idea precisely.

---

## Style Standards (set in v5.9 / v6.2)

| Element | Convention |
|---------|-----------|
| **Chapter index `<h1>`** | TITLE ONLY (no "Chapter NN:" prefix). The `<div class="chapter-label">` above carries the number. |
| **Section `<h1>`** | TITLE ONLY (no "X.Y" prefix). The chapter-label / breadcrumb above carries the number. |
| **Subsection `<h2>` inside section files** | "X.Y.Z Title" (numbered, e.g., "27.7.1 From NeRFs to Gaussian Splatting") |
| **Sub-subsection `<h3>` inside section files** | "X.Y.Z.W Title" (numbered) |
| **Special h2/h3 (no number)** | "Prerequisites", "What Comes Next", "Self-Check", "Exercises", "Key Takeaways" |
| **Bibliography container** | `<details class="bibliography-collapsible" open>` with `<summary><strong>References</strong></summary>` |
| **Bibliography inner title** | `<div class="bibliography-title">References &amp; Further Reading</div>` |
| **Figure caption** | `<strong>Figure N.M.K</strong>: descriptive caption.` (numbered sequentially within section) |
| **Code caption** | `<div class="code-caption"><strong>Code Fragment N.M.K:</strong> caption.</div>` (BELOW the code block) |
| **Table caption** | `<caption>` element with `caption-side: bottom` |

---

## Production Pipelines

| Pipeline | When | How |
|----------|------|-----|
| Gemini batch | Multiple chapter-opener illustrations | `agents/book-skills/scripts/generate_icons_gemini.py --engine gemini --batch` (50% discount) |
| Gemini single | One illustration | `C:/Users/apart/.claude/skills/gemini-imagegen/scripts/generate_image.py` |
| Mermaid | Flowcharts, sequence, hierarchy | Save `.mmd`, run `mmdc -i in.mmd -o out.png -c scripts/mermaid/mermaid-config.json -w 1200 -s 3` |
| Matplotlib | Data charts | `scripts/svg_to_matplotlib/gen_figure_*.py` using `chart_style.py` for consistent fonts/DPI |
| Inline SVG | Architecture diagrams that need exact control | Hand-author in the section HTML; use the `<defs>` + `<filter>` patterns from existing SVG figures |
| Table | Many-to-many mappings | `<table class="data-table">` with `<caption>` |

---

*Generated 2026-05-11 as part of v6.2 normalization. Update this file when
new visual types are introduced or conventions change.*
