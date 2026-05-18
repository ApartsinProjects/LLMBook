# Master TODO — Consolidated (deep audit pass)

Last refresh: 2026-05-18 session continuation. Reviews all 35 audit reports
in `docs/content-audit/` to ensure nothing is lost on context compaction.

## Done this session segment (26 commits on v2.0; cumulative 7906 → 3052 issues = 61.4%)

### Plugins added (10 new + 14 tuned)
1. `p1_structural_violations` (DUPLICATE_SINGLETON, DOUBLE_TITLE_PREFIX, KEY_INSIGHT_BOLD, INDEX_DUPLICATE_OPENER, NON_CANONICAL_BIB)
2. `p2_see_also_canonical` (title="See Also" + ≥1 anchor link)
3. `p2_key_insight_vs_takeaway` (list-in-insight or single-paragraph-in-takeaway)
4. `p2_callout_order` (singleton callout sequence enforcement)
5. `p2_header_template` (part/chapter/section template compliance)
6. `p2_code_fragment_structure` (details-wrapped code, duplicate code-output)
7. `p2_nav_linear_chain` (chapter-nav next pointer linearity)
8. `p2_bold_density` (excessive bold in prose)
9. `p2_lame_code` (dataclass/config-only fragments)
10. `p2_callout_visual_consistency` (icon + tooltip presence per type)

Plus 14 existing plugin tunes (regex fixes, scope exemptions for tools/appendix, balanced-div parsing).

### Catalogues authored
- `CALLOUT_CATALOGUE.md` — 20 canonical callout types (after pathway + thesis-thread retired)
- `HEADER_TEMPLATES.md` — 3 page-header templates (part / chapter / section)

### Background agents completed
- Section-31.4 + section-10.4 split
- Diagram improvement (10 keep, 2 improve)
- ToC/nav/xref verifier (chains repaired for all recent splits)
- Code-sample lame audit (12 files modified)
- See Also callout introduction (88 → 116 total + 170 future opps)
- Image-reuse audit (10 wirings + Key Insight/Takeaway tooltips)
- Comic image generation round 4 (12 new comics)
- Callout reordering (283 of 339 fixed, 83% drop)
- Lab layout audit (17 canonical labs + Hands-On→Lab renames)
- Tools-of-trade content audit (11 callouts flagged for migration, 1 dup)
- Repeated-content detection (179 duplicate blocks, ~6300 words reduction)
- Responsive design audit (~110 lines safety-net CSS)
- Critical-reader audit (55% KEEP, 8-fragment collapsed-indent bug fleet)
- Section h2 → callout conversion (28 sections)
- Figcaption authoring (14 captions; 0 captionless content figures remain)
- Lame code conversion (5 converted + DPO migration + 42.10.1 annotation)
- Scientific-depth opportunities (36 in 8 topic areas)
- Content-placement audit (in flight; agent a3e2a9b)

### Mechanical sweeps (Waves 41-79)

| Wave | Description | Result |
|------|-------------|-------:|
| 41 | skip-link injection | 563 files |
| 42 | img dims (PIL) | 533 + retry |
| 43 | table thead wrap | 213/151 |
| 44 | callout-prefix + th-scope | 51+53 |
| 45 | prereq/big-picture swap | 7+3 |
| 46 | dup code-fragment captions | 20 renumbered |
| 47-49 | lab/exercise hN→callout-title | 19+17+16 |
| 48 | broken xrefs (module renames) | 25 |
| 50 | whats-next link injection | 48 |
| 51 | big-picture lead-strong unwrap | 157 |
| 52 | move callout before bibliography | 9+15 |
| 53 | lab hN→callout-title | 16 |
| 54 | external link target/rel | 6 |
| 55 | h3→h2 promotion | 43+12 |
| 56 | Module-16 whats-next/fun-note/bib | 5 |
| 57 | Comprehensive root-cause | 234 |
| 58 | Bibliography canonicalization | 21 |
| 59 | Callout class realignment | 150 |
| 60 round 4 | Comic image gen + wire | 12 |
| 61 | Merge duplicate bib | 4 |
| 62 | Remove legacy whats-next | 2 |
| 63 | Algorithm/fun-note/note-output/canon-ref | 73 |
| 64 | 10.6 K.X.Y → 10.6.N | 18+dup-fix |
| 65 | PNG → JPEG | 155 (75 MB saved) |
| 66+67 | key-insight↔key-takeaway alignment | 49+49 |
| 68 | Pygments highlight | 120 |
| 69+70 | Drop pathway | 47+43 |
| 71 | broken callout-title + lame intros | 35+16 |
| 72 | section-header→chapter-header, bib collapsed, details code, dup output | 20+329+13+3 |
| 73 | content-after-footer | 3 |
| 74 | Drop thesis-thread | 6 |
| 75 | header normalization | 50 |
| 76 | bare svg → figure | 13 |
| 77 | nav linear chain | 85 |
| 78 | note → See Also | 11 |
| 79 | takeaways div / Looking Forward | 20+2 |

## ⏳ Open Items (organized by category)

### A. Structural editorial (per-section decisions needed)
- **30+ DUPLICATE_SINGLETON sections** (multiple research-frontier in same section)
  - section-6.3, 6.4, 6.7, 8.3, 8.5, 8.6, 9.2, 10.2: multiple research-frontier callouts
  - section-12.1, 15.7, 16.1, 18.1, 18.2, 18.3, 18.5: similar pattern
  - section-26.4, 27.6, 32.1, 32.4, 43.1, 43.2, 70.3, 78.9, 80.4: various
  - Action: each section needs an editorial decision — keep, merge, or convert duplicates
- **5 OVERLAP sections** (callout block contains another callout block due to missing `</div>`)
  - section-1.7, 3.6, 13.5, 16.7, 42.8, 50.1 — needs per-file structural fix
- **8 code fragments with collapsed-indentation bug** (Pygments/HTML pipeline)
  - section-26.2 L96 (LangGraph plan-and-execute)
  - section-46.2 L65 (G-Eval central example)
  - section-62.1 L177 (BackpressureQueue)
  - section-17.2 L399, L449 (GaLoreProjector, rsLoRA)
  - section-32.2 L212, L259
  - section-8.6 L176
  - Action: re-render from source notebook
- **22 code fragments** flagged by LAME_CODE plugin as dataclass-only / config-only (5 already converted)
- **GIANT_SECTION (64)**: candidate sections for further splits (decision per file)

### B. Authoring rounds (need agent dispatch)
- **482 IMAGE_OPPORTUNITY**: more comic/illustration generation rounds
- **474 SECTION_PAGE_LAYOUT**: 224 missing prereqs, 177 missing whats-next, 130 missing bib, 128 missing epigraph (some already done by structural-gap agent)
- **461 FIGURE_SEQUENCE**: per-file figure numbering (counts misalign with referencing prose)
- **342 CHAPTER_INDEX_LAYOUT**: 83 missing Prerequisites, 56 missing Learning Objectives, 55 missing looking-back, 54 missing overview, 41 missing epigraph, 31 missing whats-next
- **182 SECTION_STRUCTURE**: missing epigraph / no callouts / no takeaways
- **120 SVG_TEXT_CLIPPING** (per-file SVG redesign)
- **109 CHAPTER_STARTER**: 56 missing learning-objectives, 52 missing overview
- **94 FM4_PROMISE**: Modules missing one of the four FM.4 elements
- **86 MISSING_OUTPUT**: print() with no .code-output block
- **64 BROKEN_FIGURE_REF**: prose refers to Figure X.Y.Z that doesn't exist
- **63 GENERIC_SVG_LABEL** (aria-label="Diagram" etc.)
- **44 LAB_COVERAGE**: 44 chapters lack a hands-on lab
- **40 PART_INDEX**: part index pages missing whats-next / part-overview / opener
- **40 PART_INDEX_LAYOUT**

### C. Content reconciliation (repeated content)
From `REPEATED_CONTENT_AUDIT.md` — **179 duplicate blocks, ~6300 words reduction**:
- 2 callout-body verbatim duplications
- 12 fuzzy code-caption duplications (5+ shared tokens)
- 4 exact-text code-caption duplications ("Install required packages", "Code example", etc.)
- 7 callout-title repetitions for non-structural titles
- ~154 prose-paragraph fingerprint matches
- Action: per-cluster editorial decision — DELETE+CROSSREF / KEEP / REWRITE / RESTRUCTURE

### D. Content placement (CONTENT_PLACEMENT_AUDIT.md in flight, agent a3e2a9b)
- Theoretical content in tools chapters (already flagged 11 in CRITICAL_READER_AUDIT.md):
  - section-36.3 IR metrics primer (NDCG, MRR, MAP, BM25) → migrate to module 42/43
  - section-36.1 vector-index complexity bounds → module 31
  - section-36.2 RRF formula → module 35
  - section-36.4 ColBERT MaxSim, InfoNCE, Matryoshka → module 35 / 31 / 16
  - section-56.2 fairness metrics + SHAP axioms → module 52 / 10
  - section-56.4 Sadasivan AI-detection asymptote → module 54
  - section-61.2 Flash Attention online-softmax recurrence → module 9 / 3

### E. Critical-reader actions (CRITICAL_READER_AUDIT.md)
- 7 fragments should be sentences/tables (pip install / pseudocode-as-Python)
- 3 of 22 sampled diagrams need REDESIGN (D10, D17, D20)
- Top 10 prioritized actions listed in report's tail

### F. Scientific-depth additions (SCIENTIFIC_DEPTH_OPPORTUNITIES.md)
36 opportunities in 8 areas. Top 5 prioritized:
1. Section 3.1.5 attention forward pass (algorithm callout)
2. Section 9.3.2 speculative decoding rejection sampling proof
3. Section 18.2 DPO vs PPO contrast (extend existing)
4. Sections 31.2.2-31.2.4 HNSW/IVF/PQ (algorithm callouts)
5. Section 26.1.3 ReAct loop (algorithm callout)

### G. Image inventory
- 177/183 comic/figure/opener images wired (96.7%)
- 6 unwired: figure-0.1.2.png, figure-0.1.4.png, figure-5.2.2.png (section deleted), figure-6.3.6.png, figure-6.5.3.png, figure-52-2-2.svg
- Action: wire if topically relevant, else delete

### H. Per-file structural bugs (residual)
- 56 CALLOUT_ORDER violations (32 files need manual reconciliation due to dup-singleton)
- 54 CONSECUTIVE_HEADINGS (real authoring patterns — Steps inside Steps)
- 27 CAPTION_MISALIGN (residual)
- 19 MISSING_IMG_DIMS (18 broken-src image references)
- 16 CALLOUT_NON_CANONICAL (residual lab structure)
- 14 HEADING_HIERARCHY (h1→h3 in appendix sections — accept-or-fix)
- 12 SVG_ARIA_TRUNCATED (per-file)
- 10 MATH_RENDERING (entity edge cases)

### I. Decisions (user input needed)
- 64 GIANT_SECTION candidates: which to split?
- Production-pattern callout: keep canonical (in catalogue) — confirmed
- Tools-of-trade theoretical content migration: per-callout user approval
- 8 code-fragment collapsed-indent bugs: editorial reauthoring needed

### J. Tooling
- `scripts/check_battery.py` — regression-catch script in place
- Pagefind search rebuilt (41,682 words)
- All audit cycles snapshotted in `docs/content-audit/cycle_snapshots/`

## Reports & Reference Files

| Report | Status | Top-line stat |
|--------|--------|---------------|
| `MASTER_BACKLOG.md` | original 2026-05-17 baseline | 120 findings, ~all addressed |
| `MASTER_TODO_2026_05_18.md` | earlier consolidation | superseded by THIS doc |
| `MASTER_TODO_CONSOLIDATED.md` | THIS doc | ~30 categories tracked |
| `SESSION_BACKLOG.md` | session 1 backlog | original waves 1-32 |
| `SESSION_2026_05_18_BACKLOG.md` | session 2 backlog | waves 33-65 |
| `CALLOUT_CATALOGUE.md` | catalogue | 20 canonical types |
| `HEADER_TEMPLATES.md` | templates | 3 page-header templates |
| `REPEATED_CONTENT_AUDIT.md` | duplication triage | 179 dups, 6300 words |
| `CRITICAL_READER_AUDIT.md` | code+diagram value | 55% KEEP, 8 indent bugs |
| `SCIENTIFIC_DEPTH_OPPORTUNITIES.md` | algorithm/architecture audit | 36 opportunities |
| `CONTENT_PLACEMENT_AUDIT.md` | (in flight) | topic↔chapter alignment |
| Wave summaries (33-39) | per-wave reports | mostly closed |
| `random_detector_findings.md` | anomaly scan | closed |
| `comic_illustration_audit.md` | comic backlog | 1 open item |
| `hallucination_audit.md` | content currency | 1 open item |
| `library_shortcut_opportunities.md` | library-shortcut catalog | 3 open items (likely closed by round 4) |

## Hold v2.0; no merge to main per user instruction (Stand: 2026-05-18).
