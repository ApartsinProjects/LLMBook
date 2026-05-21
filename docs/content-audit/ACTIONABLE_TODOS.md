# Actionable TODOs from audit reports
Generated: 2026-05-19

Triage of 123 reports under `docs/content-audit/`. The 10 files listed in the
task brief (scout-only or newly written this session) were skipped per
instructions. Sampling spot-checked current file content for every "open"
finding listed below.

## Summary
- Reports scanned: 113 (123 total minus 10 skipped by instruction)
- Open actionable items: 38
- Already addressed (closed in report or by recent session): 70 reports closed
- Reports that are pure scout/inventory (no action implied): 5
- Tier 1 + Tier 2 giant-section splits all DONE (7 splits in `SEVEN_SPLITS_REPORT.md`, 5 splits in `SIX_SPLITS_REPORT.md`)
- 60+ wave summaries (Waves 33-94) mostly closed; remaining items folded into the lists below

The book has had ~76 commits on v2.0 reducing 7906 → 1975 audit issues
(75.0%). The remaining work splits into authoring-heavy (most of HIGH/MED)
and per-file editorial decisions (most of LOW).

---

## High-priority open items

### TODO 1
- **Source report:** `CRITICAL_READER_AUDIT.md` (item 14 + item 1 fleet)
- **Description:** 8 Python code fragments still have collapsed-indentation
  rendering bugs (nested `def`s inside TypedDict/class bodies, return
  statements inside wrong branch, `for` loop bodies appearing at wrong
  indent). The Pygments/HTML pipeline produced a staircase that hides the
  real structure. Verified still broken: `section-26.2.html` L168 still has
  `def create_plan` indented inside the `PlanExecuteState` TypedDict.
- **Files touched:**
  - `part-6-agentic-ai/module-26-ai-agents/section-26.2.html` L96 (LangGraph plan-and-execute) — flagship example, highest reader harm
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html` L65 (G-Eval central example)
  - `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.1.html` L177 (BackpressureQueue)
  - `part-4-training-adaptation/module-17-peft/section-17.2.html` L399 (GaLoreProjector), L449 (rsLoRA `lora_forward`)
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html` L212, L259
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` L176 (FormalProvingResult `pass_at_k`)
- **Why "high":** these are central worked examples in flagship pedagogical sections; readers who copy them get non-executable Python.
- **Estimated effort:** MEDIUM (1-4hr; re-render from source notebook or hand-fix per fragment)

### TODO 2
- **Source report:** `anomalous_styling_audit.md` Pattern C + verified live
- **Description:** Ch 34 and Ch 46 section files open with h2 numbers that
  do not start at .1 (Ch 34 starts at .2/.4/.5/.7; Ch 46 starts at .2/.3/.4/.5).
  Suggests these sections were stitched from larger merges and never
  renumbered. Confirmed live by reading first h2 in each section.
- **Files touched:**
  - `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html` (first h2 = `34.2.2`)
  - `.../section-34.3.html` (first h2 = `34.3.4`)
  - `.../section-34.4.html` (first h2 = `34.4.5`)
  - `.../section-34.5.html` (first h2 = `34.5.7`)
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html` (first h2 = `46.2.2`)
  - `.../section-46.3.html` (`46.3.3`), `.../section-46.4.html` (`46.4.4`), `.../section-46.5.html` (`46.5.5`)
- **Why "high":** breaks reader expectation of sequential numbering and TOC linking; flagged as P1 by anomalous-styling audit.
- **Estimated effort:** MEDIUM (1-4hr; renumber h2 ids + update prose cross-refs + verify TOC chain)

### TODO 3
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` B.1 + `SECTION_PAGE_LAYOUT` audit
- **Description:** 374 SECTION_PAGE_LAYOUT issues remain: 139 missing prerequisites blocks, 114 missing bibliography-collapsible, 106 missing epigraphs, 15 missing big-picture callouts.
- **Files touched:** all main-content sections book-wide that fail the canonical structural template
- **Why "high":** these are the single largest open backlog category; impacts every section's pedagogical scaffold and TOC navigability.
- **Estimated effort:** LARGE (>4hr; needs the structural-backfill agent already used in `STRUCTURAL_BACKFILL_REPORT.md` to make another sweep; bibliography backfill is partially done but 114 remain per current count)

### TODO 4
- **Source report:** `CONTENT_PLACEMENT_AUDIT.md` + `MASTER_TODO_2026_05_18.md` section D
- **Description:** 11+ theoretical-content callouts sit in Tools-of-the-Trade
  chapters where they don't belong. Each needs editorial decision: MIGRATE to
  the corresponding theory chapter OR keep with cross-ref note. Items 1-3
  below are NEW (not in prior MASTER_TODO):
  1. `section-6.8.html` (Megatron, 3D parallelism, elastic training, checkpointing) → `module-59` (NEW)
  2. `section-44.1.html` (Model Registry, 13 h2s) → `module-66` (NEW)
  3. `section-62.1.html` (4 sub-sections span Mod 09 inference + Mod 48 guardrails) — NEEDS_DECISION
- **Files touched:**
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html`
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html`
  - `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.1.html`
  - Items 4-11 (IR metrics primer, RRF formula, ColBERT MaxSim/InfoNCE/Matryoshka, fairness metrics + SHAP, watermark detection, Flash Attention recurrence, LLM-as-judge algorithm, SSMs/MoE/MLA duplicated in 80.3) — see `CONTENT_PLACEMENT_AUDIT.md` table
- **Why "high":** book is large enough that wrong-chapter placement breaks linear-reader mental model.
- **Estimated effort:** LARGE (>4hr; each migration requires user editorial decision + content move + cross-ref rewrite + verify both source and destination chapters)

### TODO 5
- **Source report:** `REPEATED_CONTENT_AUDIT.md`
- **Description:** 179 duplicate blocks identified (~6,300 words). Specifically: 2 callout-body fingerprint duplications, 7 non-structural callout-title duplications, 7 exact-text code-caption duplications, 87 fuzzy code-caption duplications (~133 excess captions), 4 prose-paragraph duplications. Each cluster needs per-cluster editorial decision: DELETE+CROSSREF / KEEP / REWRITE / RESTRUCTURE.
- **Files touched:** 179 cluster locations across the book (full list in report sections "Top 20 Duplication Clusters" and the JSON sidecar)
- **Why "high":** noticeable to careful readers, signals copy-paste authoring; biggest single content-quality lever still on the table.
- **Estimated effort:** LARGE (>4hr; per-cluster review; most are short generic boilerplate captions that can be rewritten with section-specific text in a single sweep agent)

### TODO 6
- **Source report:** `CONTENT_UPDATE_SCOUT.md`
- **Description:** 77 content-currency findings flagged across all 16 parts.
  Severity 1-5. Includes: GPT-4 → GPT-4o/o3 references in foundational
  chapters, `tiktoken` examples pinned to `cl100k_base` (should call out
  `o200k_base` for o-series), Gemma 2 → Gemma 3, Phi-4 vs Phi-4-mini /
  SmolLM2/3, PyTorch FlexAttention + torch.compile gap, FineWeb/DCLM/Dolma
  forward-references, Llama 3 / Gemma 3 / Qwen 2.5 tokenizer-vocabulary
  expansion, and dozens of similar staleness markers in Parts II-XVI.
- **Files touched:** see `CONTENT_UPDATE_SCOUT.md` per-finding location (each Finding has a `Location:` field). Top concentration: `module-01/section-1.1`, `module-01/section-1.5`, `module-05/section-5.1`, `module-07/section-7.1`, all of Ch 36 / 41 / 56 / 61.
- **Why "high":** book ages in months in the tools/landscape chapters; readers will trust stale numbers.
- **Estimated effort:** LARGE (>4hr; 77 findings each ~5-15 min)

### TODO 7
- **Source report:** `hallucination_audit.md` (MEDIUM severity items still open; HIGH severity already fixed in W33-5)
- **Description:** 6 medium-severity factual claims still un-fixed in the
  book. Verified live:
  - 34-1: spaCy "10,000 documents per second" (`section-34.2.html` lines 39, 79, 86) — likely unit confusion (words vs. docs).
  - 36-3: BGE-M3 "194 languages" — official sources say "100+ languages."
  - 36-4: MS MARCO "1M passages, 500K queries" (`section-36.3.html` L109) — should be 8.8M passages / ~1M queries.
  - 41-1: Character.AI "hundreds of millions of monthly messages" — peak was ~2B/month.
  - 46-1: "GPT-4 rates own outputs best 67% of the time" lacks citation.
  - 59-3: 1F1B attribution "Narayanan, 2019" should be "Narayanan et al., 2021".
  - 61-2: Stargate announced 2025 not 2024; $500B over 4 years not "$100B+".
  - 61-3: Meta 350K H100s is just the H100 count not total H100-equivalents (~950K).
- **Files touched:**
  - `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html`
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.3.html` (L109 MS MARCO numbers)
  - `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.4.html` (BGE-M3 194-languages claim)
  - `part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.1.html` or 41.5 (Character.AI claim)
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html` or 46.2 (GPT-4 67% self-rating)
  - `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.4.html` (1F1B / Narayanan)
  - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html` (Stargate + Meta GPU count, lines 56, 59)
- **Why "high":** factual errors in published prose; trivial to fix per occurrence.
- **Estimated effort:** SMALL (<1hr; each is a sentence-level edit)

### TODO 8
- **Source report:** `XREF_VERIFICATION.md`
- **Description:** 303 "bad anchor text" cross-references where the link target is correct but the visible label cites a section number that no longer matches (e.g. "Section 3.1" labels point to `section-3.1.html` which is now `section-3.1a.html`). Mechanical "append the variant suffix" sweep. Top patterns: 3.1→3.1a (40), 9.1→9.1a (34), 47.1→47.1a (34), 31.1→31.1a (28), 32.1→32.1a (25).
- **Files touched:** ~150-200 section files book-wide, see `_xref_findings.json` for full list
- **Why "high":** confuses readers who click "Section 3.1" and land on labeled 3.1a content.
- **Estimated effort:** MEDIUM (1-4hr; mechanical regex sweep; the cited→target table in the report makes this easy)

### TODO 9
- **Source report:** `IMAGEGEN_HIGH_MED_REPORT.md` (preparation complete) + `MASTER_TODO_2026_05_18.md` G
- **Description:** 108 image placeholders authored (93 HIGH figure + 15 MED comic). Per-section prompts ready in `.book-update/imagegen-manifest.jsonl`. Needs Gemini 2.5 Flash Image batch run + HTML wiring. Plus 482 IMAGE_OPPORTUNITY backlog still open.
- **Files touched:** see `.book-update/imagegen-manifest.jsonl` / `imagegen-manifest.csv`
- **Why "high":** new chapters (Ch 34/36/41/46/56/59/61) are visibly text-heavy compared to Parts 1-4.
- **Estimated effort:** LARGE (>4hr; Gemini API budget ~$8; dispatch + verify + wire each batch)

### TODO 10
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` C.16 + `WAVE_36_FIXES_SUMMARY.md`
- **Description:** 187 SVG redesign issues remain (120 SVG_TEXT_CLIPPING, 56 SVG_TEXT_RIGHT_CLIP, 11 SVG_TEXT_OVERFLOW). Per-file viewBox widening or text-anchor adjustment; risky to auto-fix because each SVG layout is bespoke.
- **Files touched:** ~187 inline SVG figures across the book; the audit produces a per-file inventory.
- **Why "high":** text bleeding past viewBox renders as cut-off labels at default zoom; visible to every reader.
- **Estimated effort:** LARGE (>4hr; per-file editorial; many are decade-old patterns that just need a wider viewBox)

---

## Medium-priority open items

### TODO 11
- **Source report:** `GIANT_SECTION_RECOMMENDATIONS.md` (post-Wave-90 status)
- **Description:** 7 high-confidence splits + Tier-2 candidates were already
  executed (`SEVEN_SPLITS_REPORT.md`, `SIX_SPLITS_REPORT.md`). Remaining
  decisions: 50.1 still has duplicate `<h2 id="exercises">` and
  `<h2 id="exercises-2">` (verified live), suggesting the Tier-1 split was
  not fully cleaned up. Other GIANT_SECTION candidates (64 remaining flagged)
  await per-file editorial decision; many are tagged `catalog by design`.
- **Files touched:** `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html` (cleanup); 64 borderline sections book-wide
- **Why "medium":** duplicates do not affect reader navigation but signal copy-paste in source.
- **Estimated effort:** SMALL for 50.1 (<1hr); MEDIUM-LARGE for remaining 64 (most are KEEP-with-justification)

### TODO 12
- **Source report:** `TERMINOLOGY_INCONSISTENCIES.md`
- **Description:** 1,444 inconsistent occurrences across 45 canonical-term
  groups. Top clusters:
  - `pre-training` vs `pretraining`: 414 hits, 146 sections (DECISION needed first)
  - `Chain-of-Thought` vs `chain-of-thought`: 242 hits (preserve title vs adjectival)
  - `Hugging Face` vs `HuggingFace`: 216 hits (per-instance hand-check)
  - `Llama-3` vs `Llama 3`: 179 hits (canonical in prose, no-hyphen in quoted titles)
  - 41 smaller clusters (KV cache, fine-tuning, OpenAI, Anthropic, Claude, FlashAttention, Llama-2, scikit-learn, instruction tuning, MoE, context window, SOC 2, etc.)
- **Files touched:** see per-cluster file lists in report
- **Why "medium":** professionalism marker; not factually wrong, but a careful reader notices.
- **Estimated effort:** MEDIUM (1-4hr; needs user policy decision on each top cluster before mass-replace)

### TODO 13
- **Source report:** `real_world_scenario_template_audit.md`
- **Description:** 312 of 378 `practical-example` callouts don't follow the strict canonical template (Who/Situation/Result/Lesson + Lesson-nested-bold). 190 also have non-canonical titles (don't start with "Real-World Scenario:"). Extended 8-field canonical (Who/Problem/Dilemma/Decision/How/Situation/Result/Lesson) was approved per W36 but the mass-rewrite is deferred because the missing fields would need to be authored.
- **Files touched:** see per-callout location in `real_world_scenario_template_audit.md` Task A
- **Why "medium":** standardization improves scanability; current variety is intentional but inconsistent.
- **Estimated effort:** LARGE (>4hr; needs an authoring agent per callout to fill missing fields)

### TODO 14
- **Source report:** `MASTER_TODO_CONSOLIDATED.md` B (authoring rounds)
- **Description:** 47 FM4_PROMISE issues: chapters missing one of the four FM.4 elements (26 missing Research Frontier callout, 18 missing exercise/self-check, 2 missing Warn callout, 1 missing Key Insight).
- **Files touched:** ~47 chapter sections book-wide
- **Why "medium":** FM4 is the "promise to the reader" from front matter; each missing element is a broken promise.
- **Estimated effort:** MEDIUM (1-4hr; per-chapter authoring)

### TODO 15
- **Source report:** `MASTER_TODO_CONSOLIDATED.md` H + `MASTER_TODO_SESSION_CAPTURE.md` C.18
- **Description:** 51 CALLOUT_ORDER violations: singleton callouts appear in wrong order (e.g. key-takeaway after self-check, research-frontier before big-picture). Per-file editorial reorder; 32 files need manual reconciliation due to duplicated singletons.
- **Files touched:** ~51 section files
- **Why "medium":** structural canonical-order violations; visible to a careful reader.
- **Estimated effort:** MEDIUM (1-4hr; per-file move-block-up/down)

### TODO 16
- **Source report:** `MASTER_TODO_CONSOLIDATED.md` H + `MASTER_TODO_SESSION_CAPTURE.md` C.17
- **Description:** 52 CONSECUTIVE_HEADINGS: h2 followed immediately by h3 with no transition prose. Each needs 1-3 sentences of bridging text.
- **Files touched:** ~52 section files
- **Why "medium":** reading-flow issue; abrupt heading transitions feel jarring.
- **Estimated effort:** MEDIUM (1-4hr; dispatch as a follow-on agent)

### TODO 17
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` C.5
- **Description:** 9 bare lang-text pseudocode blocks outside algorithm callouts; convert each to a proper algorithm callout or wrap in code-block-wrapper.
- **Files touched:** 9 section files (specific files in `CODE_BLOCK_WRAPPER` audit output)
- **Why "medium":** consistency with the canonical algorithm-callout pattern.
- **Estimated effort:** SMALL (<1hr; mechanical structural rewrap)

### TODO 18
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` C.2 + `library_shortcut_opportunities.md`
- **Description:** 16 `library-shortcut` callouts are missing a `<pre><code>` snippet (either add code or demote to tip callout). Plus 25-35 remaining library-shortcut callouts to add per the original opportunities audit (W39 landed 10 + 15 in flight; opportunities total was 59 across Ch 34/35/36/41/46/56/59/61).
- **Files touched:** 16 + 25-35 = 41-51 section files
- **Why "medium":** library-shortcut callouts are explicitly described as "code-snippet + library name" in CONTENT_GUIDELINES; bare-text variants violate the canonical form.
- **Estimated effort:** MEDIUM (1-4hr; per-callout)

### TODO 19
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` C.3 + C.4
- **Description:** 13 WRONG_NESTING violations (10 labs containing a sub-callout; 1 fun-note containing a cross-ref; 1 exercise containing a self-check; 1 lab containing a warning) + 13 NON_CALLOUT_LAB (Lab heading not followed by `<div class="callout lab">`).
- **Files touched:** 26 section files
- **Why "medium":** structural cleanups for the canonical-callout invariant.
- **Estimated effort:** SMALL-MEDIUM (1-4hr; per-file)

### TODO 20
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` C.6
- **Description:** 4 DIAGRAM_BOTTOM_CAPTION violations: SVG bottom banners duplicating figcaption text.
- **Files touched:**
  - `section-12.1.html:151`
  - `section-59.2.html:168`
  - `section-59.3.html:171`
  - `section-59.4.html:351`
- **Why "medium":** double-caption clutter; either strip the SVG banner or strip the figcaption.
- **Estimated effort:** SMALL (<1hr; 4 mechanical edits)

### TODO 21
- **Source report:** `bibliography_hallucination_audit.md` + verified live
- **Description:** 4 of 6 high-confidence bibliography hallucinations already
  fixed in W33-5. Still open:
  - Wave 17i 27.5 (`section-27.5.html` L210): MCP citation has no URL. Add `spec.modelcontextprotocol.io` or `docs.anthropic.com/mcp`.
  - Ch 59 text-only bibliography: most arXiv IDs in 59.1-59.5 are printed but not linked. Decision needed: link every ID or accept as low-risk style choice.
  - Wave 17i 35.2 L526 (`section-35.3.html`): Baek 2023 entry has a stray internal-nav URL (`../../part-4-training-adaptation/...`) mixed into a bib entry.
- **Files touched:**
  - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.5.html`
  - `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.{1..5}.html`
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html` L526
- **Why "medium":** verifiability + cleanup; isolated cases.
- **Estimated effort:** SMALL (<1hr)

### TODO 22
- **Source report:** `MASTER_TODO_CONSOLIDATED.md` G + `missing-images.md` follow-up
- **Description:** 6 unwired image files in image dirs that are NOT referenced by any HTML page. Either wire if topically relevant, or delete.
  - `figure-0.1.2.png`
  - `figure-0.1.4.png`
  - `figure-5.2.2.png` (section deleted)
  - `figure-6.3.6.png`
  - `figure-6.5.3.png`
  - `figure-52-2-2.svg`
- **Why "medium":** disk-space + asset-inventory hygiene.
- **Estimated effort:** SMALL (<1hr)

### TODO 23
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` C.9 + `MASTER_TODO_CONSOLIDATED.md` H
- **Description:** 9 HEADING_HIERARCHY violations: h1→h3 skip in 5 section files, h2→h4 skip in 2 section files, 2 capstone/specialized cases. Per-file decide accept or fix.
- **Files touched:** 9 section files
- **Why "medium":** accessibility + canonical-template consistency.
- **Estimated effort:** SMALL (<1hr)

### TODO 24
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` C.15-C.16 + `MASTER_TODO_CONSOLIDATED.md` H
- **Description:** 12 SVG_TITLE_TEXT (per-file aria-label improvements remaining after the 61-aria-label sweep) + 21 SVG_OVERLAP (SVG elements overlapping in rendering) + 5 SVG_PANEL_ASYM (asymmetric panel dimensions). All require per-file SVG inspection.
- **Files touched:** ~38 SVG figures book-wide
- **Why "medium":** rendering-quality polish; visible to readers but rarely fatal.
- **Estimated effort:** MEDIUM (1-4hr; per-file)

### TODO 25
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` C.10 + `MASTER_TODO_CONSOLIDATED.md` H
- **Description:** 10 MATH_RENDERING edge cases (KaTeX/MathJax entity oddities like `&#36;` interpreted as `$`, triple-dollar math, unescaped ampersands inside `\text{}`, etc.).
- **Files touched:** 10 section files
- **Why "medium":** math renders wrong in those spots.
- **Estimated effort:** SMALL (<1hr; per-file)

### TODO 26
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` B.6
- **Description:** 44 LAB_COVERAGE: 44 chapters lack a hands-on lab. Adding even one lab per chapter is the explicit recommendation from `repo_reusable_assets_audit.md` (agent #41).
- **Files touched:** 44 chapter sections
- **Why "medium":** "no lab" is a known pedagogical gap especially in the new tools chapters.
- **Estimated effort:** LARGE (>4hr; per-chapter lab authoring)

### TODO 27
- **Source report:** `MASTER_TODO_SESSION_CAPTURE.md` B.7
- **Description:** 62-86 MISSING_OUTPUT: `print()` calls with no `.code-output` block following. Each needs either the print removed or actual output added. Needs author to RUN the code or judge intent.
- **Files touched:** ~62-86 code fragments book-wide
- **Why "medium":** half-finished code examples; readers can't see what the snippet produces.
- **Estimated effort:** LARGE (>4hr; needs runtime + paste)

### TODO 28
- **Source report:** `SELF_CONTAINMENT_R3.md` (final recommendation, post-R3)
- **Description:** Run a sweep of every section titled "Platforms", "Models", "Libraries & Frameworks", "Datasets & Benchmarks", or "External Reading and Communities" to confirm each has a Big Picture or opening orientation paragraph. R3 fixed 79.2 and 45.3; the remaining bare-noun-title sections were not enumerated but are systemic.
- **Files touched:** all Tools-of-the-Trade chapters (Ch 5, 14, 19, 25, 30, 36, 41, 45, 51, 56, 61, 71, 79)
- **Why "medium":** Google-search arrivals on these sections still land in catalog lists without orientation prose.
- **Estimated effort:** MEDIUM (1-4hr; sweep + Big Picture authoring per affected section)

### TODO 29
- **Source report:** `TOC_FM_AUDIT.md` item 11 / "Out of scope on index.html"
- **Description:** `index.html` (book homepage) "What You Will Learn" tile grid (lines 743-782) only lists Parts I-X and XII (skipping XI, with old numbering); each tile body describes content that maps to an older book skeleton. Needs authoring 6 new tiles + rewriting the existing 11 tiles to match current 16-part TOC.
- **Files touched:** `index.html` (root book home page)
- **Why "medium":** first thing visitors see; advertises stale structure.
- **Estimated effort:** MEDIUM (1-4hr; per-tile content authoring)

### TODO 30
- **Source report:** `MASTER_TODO_2026_05_18.md` "Per-file structural issues" + verified
- **Description:** 18 MISSING_IMG_DIMS / BROKEN_FIGURE_REF: 18 image references with `src="figure-32-X-X.svg"` pointing to non-existent files. Need image generation or removal of refs.
- **Files touched:** ~18 section files (specific paths in `MISSING_IMG_DIMS` audit output)
- **Why "medium":** broken images render as blank space.
- **Estimated effort:** MEDIUM (1-4hr; per-image: generate or remove)

---

## Low-priority open items

### TODO 31
- **Source report:** `MASTER_TODO_CONSOLIDATED.md` I (decisions) + `MASTER_TODO_SESSION_CAPTURE.md` D
- **Description:** Decision items awaiting user input (each blocks downstream sweeps):
  - 64 GIANT_SECTION candidates: which to further split vs accept as `catalog by design`
  - Tools-of-the-Trade template policy: consolidate-into-one-page vs standardize 5-section template (per D6)
  - Industry chapters Ch 72-77 scope: accept as "industry briefs" or expand to depth-bar (per D7)
  - Ch 54 split question: Watermarking + Transparency into separate chapter (per D8)
  - Chapter-nav placement: inside vs outside `<main>` (per D9; majority pattern is INSIDE for new chapters, OUTSIDE for old)
  - H2 case-style: Title-Case vs sentence-case (per D10)
  - Orphan 52.2 (Hallucinations) move out of bias chapter (per D11)
  - Orphan 55.2 (AI Governance) move out of env chapter (per D11)
- **Why "low":** these block work but don't degrade the current book until decided.
- **Estimated effort:** N/A (user decision)

### TODO 32
- **Source report:** `EDITING_LEFTOVERS.md`
- **Description:** 82 `noncanonical-callout-prereqs` instances + 9 other categories (formerly-known, todo-comment, placeholder, etc.) totaling 91 findings. The 82 `noncanonical-callout-prereqs` are all on module-index pages where prereqs is a `<div class="prereqs">` (not wrapped in `callout`); the audit flagged this stylistically but it is the canonical pattern per `STRUCTURAL_BACKFILL_REPORT.md` (intentional non-callout `<div class="prereqs">` block). The 9 non-prereqs items are real:
  - `M66.idx` L84: "Moved here from the former section 44.1 per the content-placement audit" — language leak
  - `S37.1` L207: triple-quoted docstring "to-be-filled" placeholder in code
  - 7 more (lab-moved-callout, relocation-language, todo-comment, formerly-known, placeholder, etc.)
- **Files touched:** ~9 cleanups
- **Why "low":** small embarrassments; readers may notice.
- **Estimated effort:** SMALL (<1hr; per-occurrence)

### TODO 33
- **Source report:** `MASTER_TODO_CONSOLIDATED.md` H + `MASTER_TODO_SESSION_CAPTURE.md` C.20
- **Description:** Miscellaneous P0/P1 singleton issues:
  - 1 BROKEN_FIGURE_REF
  - 1 UNESCAPED_AMPERSAND_TITLE
  - 1 UNCLOSED_P_TAG
  - 1 TRIPLE_DOLLAR_MATH
  - 1 DECISION_FRAMEWORK_EARLY
  - 1 INDEX_ORDER
  - 1 SELFCHECK_NON_CANONICAL
  - 2 BOLD_DENSITY
  - 2 KEY_INSIGHT_VS_TAKEAWAY
  - 2 NAV_LINEAR_CHAIN
  - 5 MANUAL_HIGHLIGHT_SPANS
  - 6 STRUCTURAL_VIOLATION
  - 6 CAPTION_MISALIGN (residual)
  - 14 CALLOUT_INTERNAL (residual; 2+ callout-title divs in same callout)
  - 16 CALLOUT_NON_CANONICAL (residual lab structure)
- **Why "low":** singleton mechanical issues; each is a quick per-file fix.
- **Estimated effort:** SMALL-MEDIUM (1-4hr total; each item <10 min)

### TODO 34
- **Source report:** `wave28_content_issues.md` (referenced by `MASTER_BACKLOG.md` items 48-50)
- **Description:** 116 mild under-content sections (1 flag each) + 14 chapter-section-size imbalance cases. Each is a candidate for content expansion, but most are intentional brevity in tools sections.
- **Why "low":** subjective; many are intentionally brief catalog entries.
- **Estimated effort:** MEDIUM (1-4hr; per-section review with author judgment)

### TODO 35
- **Source report:** `wave31_32_engagement_why.md` (in `MASTER_BACKLOG.md` items 55-60)
- **Description:** Per-chapter "why does this category exist" historical arc additions:
  - Ch 41 §41.1 (no historical arc)
  - Ch 56 §56.1 needs COMPAS/NYC LL 144 opener; §56.4 needs "prove safety mathematically" counterfactual
  - Ch 61 Colossus 122-day fun-note + four-tier platform stack mental-map + InfiniBand counterfactual
  - Ch 59 "straggler GPU" illustration + parallelism-cube mental-map figure
  - Ch 34 hybrid-as-cascaded-control framing for 34.3 + spaCy counterfactual for 34.2
- **Why "low":** engagement improvements; book functional without them.
- **Estimated effort:** MEDIUM (1-4hr; per-chapter authoring)

### TODO 36
- **Source report:** `comic_illustration_audit.md`
- **Description:** ~30-40 remaining comic / analogy / mental-map opportunities across Ch 34/36/41/46/56/61. Round 4 generated 12 + Wave 37 generated 13 + Wave 39 round-2 generated 10 (35-37 total); audit catalogued 53 comic + 41 analogy + 12 mental-map slots. ~30-40 not yet placed.
- **Why "low":** engagement boost; gradually filling.
- **Estimated effort:** MEDIUM-LARGE (per-comic: prompt + Gemini generation + wire)

### TODO 37
- **Source report:** `BOILERPLATE_PROSE_SUSPECTS.md` (scout-style report)
- **Description:** 60+ subsections flagged with high boilerplate-prose suspicion score (>3.85), mostly in tools-of-the-trade and "Reading lists / Conferences / Communities" sections. Each subsection is a candidate for either rewrite-as-concrete or accept-as-list-by-design. Top offenders: S41.5 (15 subsections all hit threshold), S61.5 (newsletters/podcasts), S56.5 (practitioner communities), S36.5 (meetups).
- **Why "low":** mostly intentional list-style sections; only rewrite if user wants narrative.
- **Estimated effort:** MEDIUM (1-4hr; per-section review with author judgment)

### TODO 38
- **Source report:** `MASTER_BACKLOG.md` P2/P3 (item 110 area)
- **Description:** P2/P3 polish items not yet addressed:
  - 13 sections without sibling image (48.4, 54.6, 57.2, 57.3, 65.4, etc.)
  - 7 Big Picture verbatim copy of meta description
  - Pygments mis-tokenization of f-string format spec
  - Empty `<li>` for worked-through fixes in appendix-b
  - Hero alt-text fragmentation (truncated mid-word in 7 modules)
  - 5 capstone nav corruption ("Next Next Next Next Next")
  - Stale "Part XI" prose residue in 5 module index files
  - 190 RWS callouts have valid 6/8 fields but title doesn't start with "Real-World Scenario:"
- **Why "low":** all polish, no reader-functional impact.
- **Estimated effort:** MEDIUM-LARGE (per-cluster mechanical sweep)

---

## Reports that look fully closed

These reports show all findings as fixed/applied (verified by report's own
status markers + spot-check of current file content):

- `WAVE_33_FIXES_SUMMARY.md` — Plugin runner + 73 checks, 7 bib hallucinations, 245 double-strong fixes; all marked done
- `WAVE_34_FIXES_SUMMARY.md` — 5 new plugins, 185 What's Next links, 67 Big Picture unwraps, 76 obsolete scripts archived
- `WAVE_35_FIXES_SUMMARY.md` — GA install, 5 new validators, section-40.1 split investigation
- `WAVE_36_FIXES_SUMMARY.md` — 37 hero images + 4,626 callout title prefixes + 87 GIANT_SECTION candidates classified
- `WAVE_38_FIXES_SUMMARY.md` — Master backlog landed; 60 inflated navs removed; 81 chapter-label fixes
- `WAVE_39_FIXES_SUMMARY.md` — Library-shortcut R1, industry big-pictures, bibliographies R1, self-check Q&A R1
- `WAVE_27_PLAN.md` — pre-plan superseded by Waves 33-39
- `wave23_callouts.md` — addressed in Wave 37 (Ch 34 + Ch 46 callouts)
- `wave25_diagrams.md` — addressed in Wave 39a (11 tile-map SVGs re-skinned)
- `wave26_depth.md` — addressed in Wave 37 (Ch 36 / Ch 46 / Ch 56 / Ch 41-59-61 callouts landed)
- `wave28_content_issues.md` — most items addressed in Waves 37-39; residual TODOs captured above under TODO 4 + 28 + 34
- `wave31_32_engagement_why.md` — most items addressed in Waves 37-39; residuals captured under TODO 35
- `SESSION_BACKLOG.md` — historical session map; final state captured in MASTER_TODO_*
- `SESSION_2026_05_18_BACKLOG.md` — historical; superseded by MASTER_TODO_SESSION_CAPTURE
- `REMEDIATION-PLAN.md` — Waves 11-19, all closed
- `MASTER_TODO_2026_05_18.md` — superseded by MASTER_TODO_CONSOLIDATED + MASTER_TODO_SESSION_CAPTURE
- `MASTER_TODO_CONSOLIDATED.md` — running consolidation; open items folded into this doc
- `MASTER_TODO_SESSION_CAPTURE.md` — running consolidation; open items folded into this doc
- `MASTER_BACKLOG.md` — original 120 items; 38 SWEEPABLE + 29 AUTHORING + 12 DECISIONS done; residual fold into TODOs above
- `STRUCTURAL_BACKFILL_REPORT.md` — 260 issues resolved (epigraph + big-picture + prereqs sweep)
- `CHAPTER_INDEX_BACKFILL_REPORT.md` — 180 CHAPTER_INDEX_LAYOUT issues resolved
- `CHAPTER_STARTER_BACKFILL_REPORT.md` — 57 chapters got overview + objectives
- `BIBLIOGRAPHY_BACKFILL_REPORT.md` — 114 sections got bibliographies (verified `SECTION_PAGE_LAYOUT.bibliography == 0`)
- `BIBLIOGRAPHY_R2.md` — 22 chapter index pages in Parts 13-16 got bibliographies
- `TOC_FM_AUDIT.md` — all toc + FM file issues fixed; one residual on `index.html` flagged in TODO 29
- `SEVEN_SPLITS_REPORT.md` — all 7 Tier-1 splits executed
- `SIX_SPLITS_REPORT.md` — 5 of 6 Tier-2 splits executed (19.4 skipped per task rules)
- `SECTION_ORDER_FIX.md` — 30 P1 SECTION_ORDER issues fixed; final P1 = 0
- `STRUCTURAL_ARCHITECT_R2.md` — 24 GIANT_SECTION tags verified/reclassified
- `STYLE_VOICE_R2.md` — closed (style edits applied)
- `SENIOR_EDITOR_R2.md` + `SENIOR_EDITOR_R3.md` — wildcard editorial passes applied
- `PROSE_CLARITY_R2.md` — ~30 surgical prose edits applied
- `STUDENT_ADVOCATE_R2.md` + `STUDENT_ADVOCATE_R3.md` — acronym-on-first-use sweep applied
- `OPENING_HOOKS_R2.md` — closed (hooks applied)
- `NARRATIVE_CONTINUITY_R2.md` — closed (cycle-1.5 narrative review applied)
- `READABILITY_PACING_R2.md` + `READABILITY_PACING_R3.md` — closed (pacing edits applied)
- `AHA_MOMENT_R2.md` — 10 aha-moment callouts added
- `MEMORABILITY_R2.md` — closed (21 new key-takeaway callouts)
- `MISCONCEPTION_R2.md` — closed (misconception callouts added)
- `CROSS_REFERENCE_R2.md` — closed (cross-refs added)
- `CODE_PEDAGOGY_R2.md` — closed (code-fragment improvements applied)
- `CODE_CAPTION_R2.md` — closed (captions fixed)
- `EXAMPLE_ANALOGY_R2.md` — closed (analogies added)
- `ENGAGEMENT_R2.md` + `ENGAGEMENT_R3.md` — closed (engagement edits applied)
- `EPIGRAPHS.md` — closed (17 epigraphs rewritten)
- `EXERCISE_DESIGNER.md` — closed (exercises landed)
- `LAB_DESIGNER.md` — closed (labs landed)
- `FUN_INJECTOR_R1.md` + `FUN_INJECTOR_R2.md` — closed (fun-notes added)
- `ILLUSTRATOR_R2.md` — closed (29 SVGs added)
- `VISUAL_LEARNING.md` — closed (visuals authored)
- `VISUAL_IDENTITY_R2.md` — closed (14 files harmonized, ~120 hex replacements)
- `RESEARCH_SCIENTIST_R2.md` + `RESEARCH_SCIENTIST_R2_part5_9.md` — closed (research-frontier callouts added)
- `FACT_INTEGRITY_R2.md` + `FACT_INTEGRITY_R3.md` — 13 factual errors + 1 typo fixed; remaining MEDIUM hallucinations captured in TODO 7
- `FIGURE_FACT_CHECK_R2.md` + `FIGURE_FACT_CHECK_R2_round2.md` — closed (figure facts verified)
- `SAFETY_ETHICS_DEPTH_REPORT.md` — 13 algorithm/key-insight callouts landed in Part 10+11
- `SCIENTIFIC_DEPTH_ADDITIONS.md` — 24+1 HIGH-priority algorithm callouts authored in 9 modules
- `SCIENTIFIC_DEPTH_OPPORTUNITIES.md` — most HIGH opportunities landed via SCIENTIFIC_DEPTH_ADDITIONS + SAFETY_ETHICS_DEPTH_REPORT; ~10 MED + 3 LOW recorded as deferred but non-blocking
- `SKEPTICAL_READER_R2.md` + `SKEPTICAL_READER_R3.md` — closed (12 overclaim softenings + earlier round)
- `PUBLICATION_QA_R2.md` — closed (cycle-5 round-2: 33 orphan fixes + 17 duplicate-id + 8 em-dashes + 1 TODO comment + 1 double-dash)
- `DEEP_EXPLANATION_R1.md` — closed
- `TEACHING_FLOW_R2.md` — closed
- `CONCEPT_DEPTH_REPORT.md` — superseded by SCIENTIFIC_DEPTH_ADDITIONS
- `COGNITIVE_LOAD.md` — closed (per-section pacing applied)
- `PROJECT_ANCHOR_CATALYST.md` — closed (project anchors landed)
- `CURRICULUM_ALIGNMENT.md` — 15 edits across 13 chapter index pages
- `APPLICATION_EXAMPLES.md` — closed (application examples landed)
- `PREREQ_AUDIT.md` — closed via STRUCTURAL_BACKFILL_REPORT
- `SELF_CONTAINMENT_R2.md` + `SELF_CONTAINMENT_R3.md` — closed (3 Big Pictures added; remaining bare-noun-title sweep captured in TODO 28)
- `DEDUP_REPORT.md` + `DEDUP_REPORT-ch42.md` + `DEDUP_REPORT-ch44.md` + `DEDUP_REPORT-ch49.md` — most dedup decisions applied; residual in TODO 5
- `FIVE_CYCLE_SWEEP_PLAN.md` — historical plan; cycles executed
- `HEADER_TEMPLATES.md` — reference catalogue (3 templates), not a TODO source
- `CALLOUT_CATALOGUE.md` — reference catalogue (20 canonical types), not a TODO source
- `TEMPLATING_OPPORTUNITIES.md` — most templating ideas folded into plugin harness
- `PART_14_REUSE_ANALYSIS.md` — closed (reuse decisions applied)
- `DISPATCH_BUDGET_AND_AGENT_PLAN.md` — closed (agent plan executed across Waves 33-94)
- `DEMO_SIMULATION.md` — closed (demos landed)
- `HUMAN_EDITING_DECISIONS.md` — closed (editorial decisions captured in plugin harness)

---

## Reports that are scout-only (no fix expected)

- `BOILERPLATE_PROSE_SUSPECTS.md` — suspicion scoring; user/editor decides per cluster
- `XREF_GRAPH_REPORT.md` — inbound/outbound xref distribution; informational
- `repo_reusable_assets_audit.md` — agents + scripts inventory (recommendation, not fix list)
- `EDITING_LEFTOVERS.md` — partial scout (82 of 91 findings are intentional `<div class="prereqs">` pattern; 9 actionable items captured in TODO 32)
- `part-group-1.md` + `part-group-2.md` + `part-group-3.md` + `part-group-4.md` — original cycle-3 part-group audits; actionable items already extracted into `MASTER_BACKLOG.md`. The aggregate report itself is a scout artifact.

---

## Notes for the next editorial session

1. **Most leverage right now:** TODO 1 (8 broken code fragments — central pedagogical content) + TODO 7 (6 medium-severity factual errors — trivial to fix per item) + TODO 8 (303 bad-anchor-text — fully mechanical sweep with cited→target table).

2. **Biggest backlog by raw count:** TODO 3 (374 SECTION_PAGE_LAYOUT) + TODO 5 (179 duplicate blocks) + TODO 10 (187 SVG redesigns) + TODO 12 (1,444 terminology inconsistencies). Each can be attacked by an agent with the right brief.

3. **Decisions blocking work:** TODO 31 (8 user-decision items). Until each is resolved, the corresponding sweeps cannot proceed.

4. **Authoring-heavy buckets that need agents:** TODO 9 (image gen, 108+482 placeholders), TODO 26 (44 labs), TODO 27 (62-86 missing-output), TODO 13 (312 RWS callouts), TODO 36 (~30-40 comics).

5. **Hold v2.0** per ongoing user instruction. No items above touch production.
