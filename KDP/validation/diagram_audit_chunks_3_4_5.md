# Diagram Audit — Chunks 3 + 4 + 5 Findings (Visual Inspection)

Two of six visual-inspection agents (book-09-visual-learning) completed
before the per-session image-dimension limit was hit. Their findings
on Part IV (chapter 13-15) and Parts VII+VIII (chapter 23-26) are
captured below.

The other four chunks (Part I, II+III, V+VI, IX-XI) were not visually
inspected; the text-source Mermaid audit (v6.50) covers Mermaid diagrams
across all of those parts but Gemini cartoons in those parts have not
had visual review.

---

## CHUNK 3 — Part IV (chapters 13–16)

**Scope**: 25 manifest figures + 1 orphan + 9 unregistered chapter-16 figures.

### Critical fixes (caption mismatch, file-id mismatch, orphan)

| # | Figure | Issue | Action |
|---|---|---|---|
| 1 | **fig-13.1.2-annotation-cost.png** | figcaption talks about seed data / gardening but the chart shows annotation cost economics; alt text is correct | FIX caption text |
| 2 | **figure-14.1.4.png** | filename says 14.1.4 but HTML caption says Figure 14.1.3 | RENAME or fix HTML refs |
| 3 | **rlvr-auto-graded-exam.png** | high-quality cartoon orphan, referenced by no HTML | adopt as section-16.4 opener OR delete |

### Structural type mismatches (REWORK-AS-X)

| # | Figure | Problem | Recommendation |
|---|---|---|---|
| 1 | **13.0.1 chapter-opener.png** | Dense infographic with embedded pipeline; SELF-INSTRUCT LOOP duplicated | Split: Gemini opener + Mermaid pipeline in body |
| 2 | **14.0.1 chapter-opener.png** | Mixes loss curves with pipeline; embedded text below Kindle threshold | Separate the loss curves into matplotlib; clean opener |
| 3 | **15.0.1 chapter-opener.png** | Technical schematic with text-heavy legend illegible at Kindle width | Replace with Mermaid for body; new Gemini opener |
| 4 | **14.1.2 fine-tune-decision-tree.png** | Landscape-with-signposts cannot encode branching decision logic | REWORK as Mermaid flowchart |
| 5 | **13.2.3 evol-instruct-evolution.png** | Wizard cartoon doesn't label mutation types | ADD Mermaid flowchart with breadth/depth/complexity stages |
| 6 | **15.1.5 lora-weights-raschka.png** | External slide-deck style (purple header) clashes with book; W and W_A/W_B drawn at same size obscuring rank compression | REDRAW natively |

### DROP candidates (LOW didactic value)

- **13.4.1 labeling-sorting-hat.png** — sorting mechanism not depicted
- **13.4.3 noisy-labels-orchestra.png** — off-key musician not identifiable
- **13.7.1 data-augmentation-kaleidoscope.png** — variation transformation not visible
- **15.2.1 peft-adapter-accessories.png** — low resolution + undifferentiated metaphor

### KEEP (14 figures): all evaluated as HIGH/MEDIUM with appropriate type, no defects.

---

## CHUNK 5 — Parts VII+VIII (chapters 23–26)

**Scope**: 25 figures across multimodal + LLM applications.

### Critical fixes

| # | Figure | Issue | Action |
|---|---|---|---|
| 1 | **24.1.5 fig-24.1.3-prompt-injection-defense-layers.png** | HTML labels Figure 24.1.5 but file is fig-24.1.3 | Update HTML caption to 24.1.3 OR rename file |
| 2 | **26.1.4 fig-26.1.2-fim-prefix-suffix.png** | Same issue: HTML says 26.1.4, file is 26.1.2 | Update HTML caption to 26.1.2 OR rename file |

### Style/quality DEFECTs

| # | Figure | Issue |
|---|---|---|
| 1 | **23.3.1 ch25-research-agent-detective.png** | Caption promises green/yellow/red credibility colors; image only shows green and red strings (no yellow) |
| 2 | **24.1.1 ch26-opener-castle-defense.png** | Embedded labels INPUT FILTERING / SANDBOXING ~9 px effective at Kindle width |
| 3 | **24.4.1 ch26-error-recovery-safety-net.png** | Performer drawn falling UP through nets, contradicts caption's top-catches-first claim |
| 4 | **25.0.1 chapter-opener.png** | Generic placeholder alt text "Multimodal Generation chapter illustration"; in-figure text not in alt |
| 5 | **26.0.1 chapter-opener.png** | CREATIVE WRITING and FINANCE labels each appear twice; placeholder alt text |
| 6 | **26.1.4 fig-26.1.2-fim** | Mangled alt text: truncated filename instead of description |

### REWORK / DROP

| # | Figure | Action | Rationale |
|---|---|---|---|
| 1 | **25.1.7 ddpm-forward-reverse-process.png** | REWORK as native diagram | External Lilian Weng / Ho et al. blog screenshot with photorealistic human face — only realistic photograph in entire book; clashes with cartoon palette; KDP republication rights unclear |
| 2 | **25.3.1 document-ai-reader.png** | DROP | Robot-reading-newspaper is purely decorative; does not depict any OCR architecture |

### KEEP (16 figures): all HIGH/MEDIUM with appropriate type, no defects.

---

## Aggregated action queue

**Highest impact first:**

1. **Fix 2 caption mismatches** (chunk 3 fig-13.1.2, chunk 5 figs 24.1.5 + 26.1.4) — actively misleads readers
2. **Resolve 1 file-id mismatch** (chunk 3 figure-14.1.4 vs Figure 14.1.3 caption)
3. **Resolve 1 orphan image** (chunk 3 rlvr-auto-graded-exam.png — adopt or delete)
4. **Fix 6 alt-text / caption-mismatch defects** (chunk 5)
5. **Rework 1 external-style external image** (chunk 5 25.1.7 DDPM screenshot — copyright + style risk)
6. **Drop 5 low-value Gemini cartoons** (4 from chunk 3, 1 from chunk 5)
7. **Rework 6 structural mismatches** (chunk 3) — 3 chapter openers + 3 specific figures need split into Gemini-plus-technical-diagram

**Out of scope**: chunks 1, 2, 6 — Mermaid covered by v6.50, but Gemini cartoons in those chapters have not been visually inspected.

---

## CHUNK 4 — Parts V+VI (chapters 17–24, 51 figures)

### Critical typos in chapter-opener Gemini renders (PUBLISHABLE DEFECTS)

| Figure | Typo |
|---|---|
| **17.0.1** RLHF opener | "LERWARD SCRARE FUNCTION" (should be reward / KL terms) + step 5 label appears twice |
| **19.0.1** embeddings opener | Title: **"UNDERSTAIDING EMBDDINGS AND VECTOR DATABASES"** (two typos in the heading) |
| **20.0.1** RAG opener | "Relevant **Inotriation**" + "5. LARGE LANGUAGE MODEL" appears twice |

All three should be replaced (rebuilt as Mermaid OR re-generated via Gemini with corrected prompt + spell-check).

### REWORK / DROP

| Figure | Action | Rationale |
|---|---|---|
| **20.3.2 knowledge-graph-subway-map.png** | FIX | 40+ overlapping station labels — illegible at print size |
| **24.2.1 ch24-architecture-patterns.png** | FIX | Three topology diagrams crammed at ~150px each inside a 450px image — too small |
| **23.1.2 ch23-function-calling-loop.png** | REWORK-AS-Mermaid | Cycle metaphor lacks named protocol actors / message labels |
| **21.1.1 dialogue-system-receptionist.png** | DROP | Generic receptionist robot adds no architectural info |

### Other DEFECTs (8 more)

- **17.1.2a hf-rlhf-training.png** — text below 12 px at Kindle width; grayscale-hostile (color-only frozen-vs-trainable distinction)
- **19.1.2 contrastive-learning-magnets.png** — focal point unclear; magnets buried in scientific clutter
- **19.3.1 vector-db-librarian.png** — neon palette risks losing contrast on e-ink
- **20.1 rag-pipeline-nvidia.png** — third-party image with text below 12 px; license statement only as URL in caption
- **20.7 fig-18.7.1-graphrag-pipeline.png** — wide image with sub-description text illegible at Paperwhite width
- **22.1.2 agent-loop-detective.png** — saturated neon palette; muddy on e-ink
- **23.1.1 ch23-opener-tool-belt.png** — rendered at low resolution (~400×400 px); thought-bubble schema text illegible
- **23.5.1 ch23-agentic-rag-librarian.png** — narrow vertical strip; key map-with-checkmarks detail too small

### KEEP (31 figures from chunk 4)

All HIGH/MEDIUM didactic value, correct type, no defects.

---

## ALL CHUNKS — Combined statistics

| Chunk | Scope | Audited | KEEP | FIX | REWORK | DROP |
|---|---|---|---|---|---|---|
| 3 | Part IV (ch 13-16) | 25 + 9 unregistered + 1 orphan | 14 | 7 | 2 | 4 |
| 4 | Parts V+VI (ch 17-24) | 51 | 31 | 15 | 1 | 1 |
| 5 | Parts VII+VIII (ch 23-26) | 25 | 16 | 7 | 1 | 1 |
| 1, 2, 6 | not visually inspected | — | — | — | — | — |
| **Total inspected** | | **101 figures** | **61** | **29** | **4** | **6** |

**Estimated total work to fix**: 29 caption/text/sizing FIX edits + 4 REWORK regenerations + 6 DROP removals = **~39 changes** across the inspected 101 figures.

These findings are derived from the 2 successful image-vision agent runs;
the remaining 4 chunks need a different inspection strategy (one-figure-
at-a-time agent invocations, or human review).
