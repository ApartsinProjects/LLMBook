# Diagram Audit Framework

**Scope**: 390 figures in the book (252 Gemini cartoons, 129 Mermaid
flowcharts, 8 matplotlib charts, 1 missing).

## Three axes per figure

### A. Information / Didactic Value
Does the figure teach the reader something the prose cannot? Rate one of:

- **HIGH**: figure is the primary carrier of the lesson (worked example,
  quantitative relationship, named architecture stack, multi-panel
  comparison). The prose alone would leave a real gap.
- **MEDIUM**: figure reinforces / structures what the prose says (concept
  map, decision tree, taxonomy). Reader benefits but could survive without.
- **LOW**: figure restates what the prose already said in box-arrow form.
  Pure decoration. (Per the v6.48 Diagram Policy, these are candidates
  for DROP.)
- **MISLEADING / WRONG**: figure depicts something incorrect or
  confusingly. Must FIX or DROP.

### B. Visualization Type Fit
Is the chosen visualization type the right tool for this message? Three
options:

- **Mermaid (Vector Diagram)**: best for architectures, pipelines,
  decision trees, state machines, taxonomies. Boxes + arrows; minimal
  visual style; renders crisp at any zoom.
- **Matplotlib (Quantitative Chart)**: best for numeric relationships
  (scaling laws, throughput curves, distributions). Has axes, units,
  legend. The math is the message.
- **Gemini Infographic / Illustration**: best for conceptual metaphors,
  narrative openers, intuition-building cartoons. Warm, friendly,
  memorable. Use when the lesson is "imagine X like Y."

**Wrong-tool symptoms**:
- A Gemini cartoon where the lesson is quantitative (use matplotlib)
- A Mermaid flowchart where the lesson is metaphorical (use Gemini)
- A matplotlib chart where the lesson is structural (use Mermaid)

### C. Publishing Quality
Mechanical defects regardless of content:

- **Text overlap / clipping**: labels cut off at panel edges, captions
  bleed into other elements, text on top of other text.
- **Text size**: too small to read at thumbnail size (Kindle Paperwhite
  is 1072 px wide; text below 12 px effective is unreadable).
- **Color**: insufficient contrast (light text on light bg), grayscale-
  hostile (color is the ONLY discriminator, breaks on b&w Kindle),
  off-palette (clashes with other figures in the same chapter).
- **Resolution**: rasterized at < 1.5× target size (visible pixelation
  on retina-class screens), or > 3× (wasted bytes).
- **Layout**: huge white margins (over-padded), cramped (insufficient
  margin), no clear focal point.
- **Caption alignment**: caption doesn't match figure content, or
  references a numbered subpart (e.g. "(a)") that doesn't exist in the
  visual.

## Per-figure report row

```
figure_id        e.g. "fig-6.3.2"
section          e.g. "module-06-pretraining-scaling-laws/section-6.3"
image_kind       gemini-png | mermaid-png | matplotlib-png
A_value          HIGH | MEDIUM | LOW | MISLEADING
A_reasoning      one-sentence why
B_fit            CORRECT | WRONG-should-be-X
B_reasoning      one-sentence why
C_quality        OK | DEFECT-list (overlap, size, color, etc.)
C_reasoning      one-sentence why
recommended_action  KEEP | FIX | REWORK-AS-X | DROP
```

## Execution plan

The 390 figures split into 6 parallel chunks for inspection by deep-
explanation agents:

| Chunk | Range | Approx figures |
|---|---|---|
| 1 | Part I (Foundations, chapters 0-5) | ~75 |
| 2 | Part II+III (Understanding + Working with LLMs, chapters 6-12) | ~80 |
| 3 | Part IV (Training, chapters 13-16) | ~60 |
| 4 | Part V+VI (Retrieval + Agents, chapters 17-24) | ~90 |
| 5 | Part VII+VIII (Multimodal + Production, chapters 25-28) | ~60 |
| 6 | Part IX+X+XI (Safety + Frontiers + Idea-to-Product, chapters 29-34) | ~50 |

Each agent receives:
- The list of figures in its chunk with file paths
- The 3-axis rubric above
- An output template that produces a CSV row per figure

Findings consolidated into a master `diagram_audit_full.csv` and a
prose summary `DIAGRAM_AUDIT_HIGHLIGHTS.md`.

## What gets done with the findings

For each row:
- **A=LOW**: feed to the v6.48 Drop policy.
- **A=MISLEADING**: queue for regeneration with corrected content.
- **B=WRONG-should-be-matplotlib**: queue for matplotlib generator script
  (replace Gemini cartoon or Mermaid flowchart).
- **B=WRONG-should-be-Gemini**: queue for Gemini infographic generation.
- **C=DEFECT**: queue for regeneration with style fixes (text size,
  contrast, clipping).
- **KEEP**: no action.

The deliverable is a punch-list, not edits — execution happens in a
separate pass (one figure at a time, with verification).
