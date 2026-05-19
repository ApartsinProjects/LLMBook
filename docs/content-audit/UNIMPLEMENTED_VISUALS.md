# Unimplemented Visuals: Cross-Audit Inventory

**Date generated**: 2026-05-19
**Mode**: READ-ONLY tracking pass (no images generated, no figures added)
**Sources scanned**: 7 audit reports + 1 cycle-snapshot delta + on-disk verification

This report consolidates ALL prior unimplemented suggestions for figures, diagrams,
illustrations, and image-bearing callouts across the LLMBook audit corpus, then verifies
against the current on-disk state to distinguish "implemented since the suggestion"
from "still missing".

---

## 1. Executive Summary

### Totals

| Metric | Count |
|---|---:|
| Total visual-related suggestions catalogued (across all audits) | ~700+ |
| Suggestions verified IMPLEMENTED since they were filed | ~94% of dated picks |
| Truly STILL-EMPTY sections (zero figure, zero SVG, zero img) | **9** |
| Stale paths (file renamed/deleted since the audit) | **13** |
| Fun-note (comic/analogy) callout opportunities still open | **345** |
| SVG quality fixes pending (existing diagrams to rework, not new) | **220** |
| Broken figure references (prose cites a non-existent figure) | **1** |

### Breakdown by source report

| Source report | Date | Items proposed | Items implemented (verified) | Items unimplemented |
|---|---|---:|---:|---:|
| `IMAGEGEN_HIGH_MED_REPORT.md` | 2026-05-18 | 93 HIGH placeholders + 15 MED comic fun-notes | ~93 figures landed (cycle 61->62 delta of 93 figure-needed clears) | ~0 figure placeholders remaining; the 15 MED comics are inline analogies that are already in HTML |
| `VISUAL_LEARNING.md` | 2026-05-19 | 11 SVGs + 1 table across 9 sections in Parts 5-9 | 11 SVGs landed (all 9 target files verified to have SVGs now) | 0 |
| `ILLUSTRATOR_R2.md` | 2026-05-19 (cycle 3 R2) | 29 inline SVGs across Parts 5-9 | 29 SVGs landed (all 29 target sections verified to have figures now) | 0 |
| `VISUAL_IDENTITY_R2.md` | 2026-05-19 | Palette/font harmonization across 15 files | All 15 verified harmonized (no Georgia font, no off-palette hex) | 0 (this was edit-existing, not add-new) |
| `FIGURE_FACT_CHECK_R2.md` (R1 + R2) | 2026-05-19 | 7 + 7 caption/SVG fact fixes | All 14 captions edited | 2 SVG-redraw follow-ups deferred (Figure 21.2.2, Figure 73.1.1) |
| `wave25_diagrams.md` | 2026-05-17 | 5 diagram gaps proposed + 10-file tile-map re-skin | Tile-map re-skin done (VISUAL_IDENTITY_R2 landed it); 3 of 5 gaps closed | 2 gaps remain: 35.3 GraphRAG pipeline; 29.4 quadrant. Plus 1 lingering "rainbow" SVG in 59.5 |
| `cycle_62.json` (latest snapshot) | 2026-05-19 (live) | 123 IMAGE_OPPORTUNITY figure-flags | 110 already have a figure/svg/img; 13 are stale paths | **9 truly empty sections** (listed in Section 2 below) |
| `cycle_62.json` (latest snapshot) | 2026-05-19 (live) | 256 IMAGE_OPPORTUNITY fun-note flags | n/a (fun-notes are written analogies; status check requires DOM-level scan, deferred) | **345 callout fun-note gaps** still open (some duplicated with figure-needed counts; canonical figure is ~256 unique) |
| `broken-images-catalog.md` | 2026-05-16 | 31 broken `<img src="...">` references | All 20 regenerated + 11 prose-replaced (per `visual-assets-sweep-report.md`) | 0 |
| `placeholders-audit.md` (figure-replaced) | 2026-05-18 | 6 `<p class="figure-replaced">` blocks | Resolved (zero matches in current HTML) | 0 |
| Inline `<!-- TODO ... figure -->` HTML comments | live | Section-20.2 explicit asset-missing TODO | 0 | **1** explicit TODO (section-20.2 figure 20.2.1 source asset missing) |

### Cycle progression (image opportunity backlog over time)

| Cycle | Total issues | IMAGE_OPPORTUNITY | of which figure-needed | of which fun-note-needed |
|---|---:|---:|---:|---:|
| cycle_56 | 3051 | 482 | 216 | 482 |
| cycle_57 | 3002 | 482 | 216 | 482 |
| cycle_58 | 2856 | 482 | 216 | 482 |
| cycle_59 | 2315 | 482 | 216 | 482 |
| cycle_60 | 2128 | 482 | 216 | 482 |
| cycle_61 | 2033 | 482 | 216 | 482 |
| cycle_62 | **1980** | **379** | **123** | **379** (256 unique) |

Between cycle_61 and cycle_62, the figure backlog dropped from 216 to 123 (delta = 93,
matching the IMAGEGEN_HIGH_MED_REPORT's 93-figure batch). The fun-note backlog also
dropped from 482 to 379 (delta = 103), which lines up with the MED-tier 15 inserts
plus the various R2 fun-note edits.

---

## 2. Top 20 Unimplemented HIGH-priority Suggestions (ranked)

These are the verified-still-empty sections, ranked by (a) pedagogical impact, (b)
implementation effort (small SVG vs full illustration), and (c) section visibility
(foundational chapter vs niche).

Note: the "9 truly empty" sections are ALL in `tools-of-the-trade` modules, which the
`ILLUSTRATOR_R2.md` audit explicitly notes as deliberately skipped (external-reading /
library-catalog content where "figures would be filler"). The ILLUSTRATOR pass author
chose pedagogy-over-completeness on these. Most of these are LOW priority for that
reason. The genuine HIGH-priority candidates are the wave25-residual + R2 follow-up
items in the table below, which sit in CONTENT modules (not tools modules).

| Rank | Section | Source audit | Suggestion | Effort | Impact | Visibility | Priority |
|---:|---|---|---|---|---|---|---|
| 1 | `part-7-.../module-35-advanced-rag/section-35.3.html` | wave25 | 6-box LR pipeline: documents -> entity extraction -> graph construction -> community detection -> community summaries -> query. Section explains the Microsoft GraphRAG pipeline in prose+table only. | Small SVG (6 boxes, LR flow) | **HIGH** (unlocks pipeline mental model) | RAG chapter, foundational | **HIGH** |
| 2 | `part-12-.../module-59-.../section-59.5.html` (Figure 59.5.1 reskin) | wave25 | Re-skin "Production Training Stack" 5-layer SVG: replace rainbow palette (`#9a2828`, `#5f2a8a`) with book navy/green/amber/purple to match the rest of Ch 59. Visual identity break. | Trivial CSS-only hex swap | LOW-MED (visual consistency) | Distributed-training chapter, foundational | MEDIUM |
| 3 | `part-6-.../module-29-.../section-29.4.html` | wave25 | Agency-vs-developer-control quadrant: Claude Code / Cursor / Windsurf / Devin positioned by autonomy axis. Currently a single comparison table. | Small SVG quadrant | MEDIUM (helps mental model) | Specialized agents chapter | MEDIUM |
| 4 | Figure 21.2.2 redraw | `FIGURE_FACT_CHECK_R2.md` follow-up | Current SVG depicts generic error categories; prose discusses FUNSD-specific (checkbox / multi-line / OCR cascade / header confusion). Either redraw SVG to match prose, or soften prose to match generic SVG. The R2 pass softened the prose; this is a deeper SVG rebuild option still on the table. | Small SVG redraw | LOW (caption now matches; this is polish) | OCR/document chapter | LOW |
| 5 | Figure 73.1.1 dedicated illustration | `FIGURE_FACT_CHECK_R2.md` follow-up | Current image is `comic-three-parallelism-kitchens.jpg` borrowed from Ch 59 (factory-line as the analogy stand-in). Caption was rewritten to match what kitchens show. A dedicated factory-line illustration showing maintenance copilot / inspection summarizer / work-order drafter / supplier-risk briefer would land the original four-station-pipeline pedagogy more directly. | Medium (one new gemini-imagegen comic OR commissioned illustration) | MEDIUM (industry chapter, retains pedagogy) | Manufacturing-LLMs niche | LOW-MED |
| 6 | `part-5-.../section-20.2.html` (Figure 20.2.1 source asset) | Inline TODO comment | Figure renamed from `figure-32-2-1` during chapter renumbering; source asset missing on disk. Section is voice-cloning anatomy. Comment reads "regenerate diagram or restore from archive". | Small (regen the diagram) | MEDIUM (specific cited figure, leaves a gap) | Voice/audio chapter | MEDIUM |
| 7 | `part-4-.../module-19-tools-of-the-trade/section-19.12.html` (7152 words!) | cycle_62 IMAGE_OPPORTUNITY | Huge section (7k words) about Transformers library, currently zero figures. ILLUSTRATOR_R2 deliberately skipped (rationale: "API walk-throughs; figures would be filler"). Yet the word count alone makes this readable-fatigue territory. A small ecosystem diagram or one screenshot would help. | Small SVG | MEDIUM | PEFT chapter foundational | MEDIUM |
| 8 | `part-4-.../module-19-tools-of-the-trade/section-19.10.html` (4798w) | cycle_62 | Same as #7: large HF-library deep-dive section, zero visuals. Per ILLUSTRATOR_R2 convention, these were skipped on purpose, but the largest ones are heavy on a reader. | Small SVG | LOW-MED | tools chapter (lower visibility) | LOW |
| 9 | `part-4-.../module-19-tools-of-the-trade/section-19.11.html` (4781w) | cycle_62 | Same as #7-8. | Small SVG | LOW-MED | tools chapter | LOW |
| 10 | `part-4-.../module-19-tools-of-the-trade/section-19.9.html` (3030w) | cycle_62 | Same as #7-9. | Small SVG | LOW | tools chapter | LOW |
| 11 | `part-9-.../module-45-tools-of-the-trade/section-45.3.html` (2978w) | cycle_62 | Evaluation tools-of-the-trade catalog. ILLUSTRATOR_R2 deliberately skipped (section 45.2 was rated "would dilute rather than help"; 45.3 same family). | None recommended | LOW | tools chapter | DROP candidate |
| 12 | `part-9-.../module-45-tools-of-the-trade/section-45.4.html` (1470w) | cycle_62 | Same as #11. | None recommended | LOW | tools chapter | DROP candidate |
| 13 | `part-4-.../module-19-tools-of-the-trade/section-19.5.html` (1358w) | cycle_62 | External-reading/community section per ILLUSTRATOR_R2 ("intended as text-heavy bibliographies"). | None recommended | LOW | tools chapter | DROP candidate |
| 14 | `part-6-.../module-30-tools-of-the-trade/section-30.5.html` (1294w) | cycle_62 | Same category: external reading list. ILLUSTRATOR_R2 explicit skip ("no figure benefit"). | None recommended | LOW | tools chapter | DROP candidate |
| 15 | `part-9-.../module-45-tools-of-the-trade/section-45.5.html` (904w) | cycle_62 | Same external-reading category. | None recommended | LOW | tools chapter | DROP candidate |
| 16 | Top fun-note opportunity: section index files in Part 5 (multimodal) | cycle_62 | 57 unique fun-note opportunities in Part 5 (multimodal). The IMAGEGEN MED tier already shipped 15 hand-crafted analogies, mostly in Parts 1-3. Part 5 had zero MED-tier inserts. | Written prose analogy (no image) | MEDIUM (Part 5 is fact-dense, fewer mental hooks) | Multimodal chapters, foundational for advanced material | MEDIUM |
| 17 | Top fun-note opportunity: industry chapters Part 14 (67-74) | cycle_62 | 64 fun-note opportunities in Part 14. Each industry chapter (legal, finance, healthcare, education, cybersecurity, government, manufacturing, tools) has fewer than 2 comics. | Written prose analogy | MEDIUM (industry sections are dry; analogies improve memorability) | Application chapters, niche | LOW-MED |
| 18 | Fun-note opportunities Part 11 (ethics/trust/governance) | cycle_62 | 26 fun-note opportunities. Governance/ethics sections are policy-heavy and tend to be slogs without anchoring analogies. | Written prose analogy | MEDIUM | Ethics chapters | LOW-MED |
| 19 | Fun-note opportunities Part 12 (systems-at-scale) | cycle_62 | 23 fun-note opportunities. Already has the IMAGEGEN MED-tier "parallelism kitchens" comic; could use 2-3 more for ZeRO stages, FlashAttention, decentralized training. | Written prose analogy | MEDIUM | Scale chapters, technical | LOW-MED |
| 20 | Fun-note opportunities Part 4 (training/adaptation) | cycle_62 | 24 fun-note opportunities. Part 4 already has 6 IMAGEGEN MED-tier comics, but has 76 sections, so more room exists. | Written prose analogy | LOW-MED | Training chapters | LOW |

### Notes on the "DROP candidate" rows

Five rows above (11, 12, 13, 14, 15) are tools-of-the-trade sections that
`ILLUSTRATOR_R2.md` explicitly chose not to illustrate, with the rationale:

> "Tools-of-the-trade external-reading lists (sections 19.5, 30.5, 36.5, 41.5, 45.5)
> are intended as text-heavy bibliographies. No figure benefit."
> "Multimodal tools-of-trade catalogs 25.2 through 25.5 (libraries, datasets,
> models, readings) are catalogs without a single conceptual frame."

The cycle_62 audit plugin is a static rule (word_count >= 1000 + figure_count == 0)
and does not know about this curatorial decision. Recommend keeping these as flagged
but accepting them as a documented exception, OR updating the audit plugin to
exempt `tools-of-the-trade` directories.

---

## 3. Recommended Implementation Order

If the user wants to close the visual gap, this is the proposed sequence:

### Wave A: True content gaps (small SVG diagrams, high pedagogical lift)

1. **GraphRAG pipeline (35.3)**: 6-box LR flow SVG. ~1 hour of inline-SVG drafting in book palette. Closes a foundational RAG-chapter mental-model gap.
2. **Production training stack reskin (59.5.1)**: Trivial CSS hex swap (`#9a2828` -> `#c0392b`, `#5f2a8a` -> `#8e44ad`) to match book palette. ~15 minutes.
3. **Agentic coding quadrant (29.4)**: One small 2x2 quadrant SVG with 4 labeled tools. ~30 minutes.
4. **Voice-cloning Figure 20.2.1 restore**: regenerate the figure-32-2-1 asset under the new chapter-numbering and re-wire the section. ~20 minutes if the source notebook still exists.

### Wave B: Fact-check follow-ups (optional polish)

5. **Figure 21.2.2 SVG redraw**: Replace generic error-bucket SVG with FUNSD-specific buckets (checkbox / multi-line / OCR cascade / header) to match the original prose intent. ~1 hour.
6. **Figure 73.1.1 dedicated comic**: Commission a manufacturing-line illustration (maintenance copilot / inspection summarizer / work-order drafter / supplier-risk briefer) via gemini-imagegen. ~30 minutes including prompt tuning.

### Wave C: Tools-of-the-trade exceptions (decision required)

7. **Section 19.12 (Transformers library, 7152 words)**: Despite the ILLUSTRATOR_R2 skip rationale, a 7k-word library walkthrough does suffer from no-anchor-figure fatigue. One small "Transformers library mental map" SVG (~6 boxes: model class -> tokenizer -> trainer -> pipeline -> hub -> accelerate) could earn its space. Smaller siblings 19.9 / 19.10 / 19.11 follow the same pattern.

### Wave D: Fun-note authoring (no images, written analogies)

8. **Part 5 multimodal fun-note batch**: 15-20 hand-crafted analogies for the busiest multimodal sections (audio cloning, document OCR, VLA models). Pattern matches the IMAGEGEN MED-tier tier ("Encoders, Decoders, and the Tool Shed" style).
9. **Part 14 industry fun-note batch**: 15-20 analogies for the legal/finance/healthcare/manufacturing chapters.
10. **Part 11 + Part 12 fun-note batch**: 10-15 analogies for ethics + scale sections.

### Wave E: SVG quality fixes (existing diagrams, not new content)

11. **220 SVG quality issues** (SVG_TEXT_CLIPPING 120, SVG_TEXT_RIGHT_CLIP 54, SVG_OVERLAP 19, etc.). These are per-SVG redesign tasks. NOT in scope for "new figures" but on the master TODO. See `MASTER_TODO_CONSOLIDATED.md` line "120 SVG_TEXT_CLIPPING (per-file SVG redesign)".

---

## 4. Notes: Suggestions to DROP

### 4a. Stale paths (file renamed/removed in chapter renumbering)

13 figure-needed paths in `cycle_62.json` point to files that no longer exist:

```
part-2-understanding-llms/module-10-interpretability/section-10.6.html
part-14-designing-llm-agent-products/module-67-ideation/section-67.2.html
part-14-designing-llm-agent-products/module-67-ideation/section-67.3.html
part-14-designing-llm-agent-products/module-67-ideation/section-67.6.html
part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.3.html
part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.5.html
part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.6.html
part-14-designing-llm-agent-products/module-69-llm-economics/section-69.1.html
part-14-designing-llm-agent-products/module-69-llm-economics/section-69.2.html
part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html
part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.3.html
part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.4.html
part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.5.html
```

These should be DROPPED from the active backlog. The cycle_62 audit run pre-dates the
v2.0 chapter renumbering for Part 14 (designing-llm-agent-products was rolled into
applications-of-llms-across-industries) and Part 16 (renumbered to Part 15). Re-running
the audit will refresh these paths.

### 4b. Tools-of-the-trade external-reading sections

Per `ILLUSTRATOR_R2.md`:

> "Tools-of-the-trade external-reading lists (sections 19.5, 30.5, 36.5, 41.5, 45.5)
> are intended as text-heavy bibliographies. No figure benefit."

The cycle_62 audit re-flags these. Recommend treating them as a known exception
(update audit plugin to exempt) OR adding a single decorative "weekly cadence wheel"
SVG (per wave25 suggestion for 36.5.9). Implementation cost is high relative to value.

### 4c. Caption-only drift (resolved)

The `broken-images-catalog.md` and `placeholders-audit.md` flagged 1 caption-only
drift (section-33.4 "Figure 33.4.1" should be "Figure 61.4.1"). This is a
cross-reference/renumbering issue handled by a separate agent lane (see
`MASTER_TODO_CONSOLIDATED.md` line "461 FIGURE_SEQUENCE: per-file figure numbering").
Not a missing-figure issue.

### 4d. Sections cited in audits whose modules were merged

Wave25 cited "Wave 17i consolidation" sections including 24.6, 24.13, 26.6, 27.5,
29.1 as needing diagrams. ALL of these were addressed by ILLUSTRATOR_R2's wave-of-29
inserts OR by the existing PNG illustrations being retained. Verified all closed.

---

## 5. Source File Map

For traceability, the suggestions in this report were extracted from:

| Path | Role |
|---|---|
| `docs/content-audit/IMAGEGEN_HIGH_MED_REPORT.md` | 93 HIGH placeholders + 15 MED fun-notes |
| `docs/content-audit/VISUAL_LEARNING.md` | 11 SVG figures + 1 table across Parts 5-9 |
| `docs/content-audit/VISUAL_IDENTITY_R2.md` | 15 file palette/font harmonizations |
| `docs/content-audit/ILLUSTRATOR_R2.md` | 29 inline SVG figure additions |
| `docs/content-audit/FIGURE_FACT_CHECK_R2.md` | 7 caption/SVG fact fixes + 2 follow-ups |
| `docs/content-audit/FIGURE_FACT_CHECK_R2_round2.md` | 7 more caption/alt-text fixes + 2 follow-ups |
| `docs/content-audit/wave25_diagrams.md` | 11 chapter diagram gaps + visual-identity bulk re-skin |
| `docs/content-audit/cycle_snapshots/cycle_62.json` | LATEST: 123 figure flags + 256 fun-note flags |
| `docs/content-audit/MASTER_TODO_CONSOLIDATED.md` | Top-level rollup pointing at 482 (then 379) IMAGE_OPPORTUNITY |
| `docs/content-audit/MASTER_BACKLOG.md` | Mentions "13 sections without sibling image (48.4, 54.6, 57.2, 57.3, 65.4)" - older numbering, partially obsolete |
| `broken-images-catalog.md` | 31 broken image references (all resolved per `visual-assets-sweep-report.md`) |
| `visual-assets-sweep-report.md` | 20 regenerated + 11 prose-replaced + 5 appendix heroes |
| `diagram-generation-report.md` | 15 SVG+PNG diagrams generated |
| `diagram-complexity-audit.md` | Round 1-3 simplification of 51 over-complex diagrams; 10 candidates for round 4 |
| `ch32-diagrams-resume-report.md` | 2 new + 6 wired Ch 32 diagrams |
| `part-12-visual-enrichment-report.md` | 7 Part 12 frontier diagrams |
| `part-12-comprehensive-enrichment-report.md` | Confirms Part 12 callouts done; no new images needed |
| `placeholders-audit.md` | 6 `<p class="figure-replaced">` blocks (resolved) |
| `figure-audit.md` | CSS oversized-image issue (separate concern: image sizing, not missing figures) |

---

## 6. Bottom Line

**The figure-suggestion pipeline is in great shape.** Of all dated picks across 7 audit
passes, more than 94% have landed. The remaining genuine gaps are:

- **3 small SVG diagrams** worth building in content modules (GraphRAG pipeline 35.3,
  agentic coding quadrant 29.4, voice-cloning Figure 20.2.1 source asset).
- **1 trivial palette reskin** (Production training stack 59.5.1 to match book palette).
- **2 optional polish redraws** (Figure 21.2.2 FUNSD-specific buckets, Figure 73.1.1
  dedicated factory illustration).
- **9 "tools-of-the-trade" sections** flagged by the audit but explicitly skipped by
  the curatorial team. DECISION required: implement or update audit to suppress.
- **~256 fun-note (analogy/comic) opportunities** for memorability lift, which are
  written-prose work rather than image work.
- **220 SVG quality issues** in EXISTING diagrams (text clipping, panel asymmetry),
  which is rework not new-content work.
- **1 broken figure reference** (`Figure 18.1.3` cited in Ch 16 prose, no caption
  defines it).

The TOP 4 actionable items together would close roughly **all remaining content-module
figure gaps** in under 3 hours of inline-SVG drafting + 1 trivial CSS hex swap.

---

*End of UNIMPLEMENTED_VISUALS.md*
