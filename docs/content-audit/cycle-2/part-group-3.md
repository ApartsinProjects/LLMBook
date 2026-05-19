# Content Audit Cycle 2 — Parts 9-12

Scope: Part 9 (Evaluation & Observability, Ch 42-46), Part 10 (Security & Runtime Safety, Ch 47-51), Part 11 (Ethics, Trust & Governance, Ch 52-56), Part 12 (Systems at Scale, Ch 57-61).

## Top remaining issues

1. **Visible H2/H3 section-number labels are wholesale stale across 58+ section files in Parts 9-12.** Cycle 1's H2-renumber sweep did not reach this group. Every section body still carries the old chapter prefix in its visible `<h2>` and `<h3>` text (and in the matching anchor `id`s). Examples: section-42.1.html h2 says "44.1.1"; section-58.1.html h2 says "63.1.1"; section-52.2.html h2 says "54.1.1"; section-50.2.html h2 says "52.5.1"; section-53.3.html h2 says "55.5.1"; section-55.2.html h2 says "59.5.1". Magnitude: 28 files in Part 9, 12 in Part 10, 8 in Part 11, 10 in Part 12 (= ~58 section bodies, hundreds of headings). The anchor IDs use the matching old number (e.g. `id="34-1-1"`, `id="37-12-1"`, `id="63-1-1"`), so any in-page TOCs and external links are broken in lock-step.

2. **Chapter-level chapter-nav prev/next labels are stale across nearly every chapter index in Parts 9-12.** Visible chapter numbers and titles in the prev/next buttons are off by 2-8 and in many cases the `href` points at the wrong target (often self-linking). Examples observed:
   - Ch 42 next-link: label "Chapter 45: Testing and EDQG", href → module-42 (self)
   - Ch 43 prev "Chapter 45", next "Chapter 47"
   - Ch 44 prev "Chapter 46", next "Chapter 48"
   - Ch 45 prev "Chapter 47", next "Chapter 49"
   - Ch 47 prev "Chapter 48", next "Chapter 50"
   - Ch 48 prev "Chapter 49", next "Chapter 51"
   - Ch 49 prev "Chapter 50", next "Chapter 52" + "Chapter 60 consolidates Part IX"
   - Ch 50 next "Chapter 53: Bias, Fairness, and Disparate Impact" (chapter renamed in cycle 1)
   - Ch 51 prev "Chapter 59 Frontier Safety", next "Chapter 61: Compute Planning"
   - Ch 52 prev "Chapter 52", next "Chapter 54: Hallucination and Truthfulness", href → self (module-52)
   - Ch 53 prev "Chapter 54: Hallucination and Truthfulness", next "Chapter 56: Watermarking, Provenance, and Deepfake Defense"
   - Ch 54 prev "Chapter 55", next "Chapter 57: Transparency...", href → self
   - Ch 55 prev "Chapter 57: Transparency", next "Chapter 59: Frontier Safety", href → self
   - Ch 57 prev "Chapter 60", next "Chapter 62: Production Engineering" + href jumps to Part 13
   - Ch 58 prev "Chapter 78: Frontier Theory" (Part 16!), next "Chapter 85: AGI Trajectories" (Part 16!) — cycle-1 fix DID NOT take
   - Ch 59, 60, 61, 56 each missing prev/next entirely (only "In Part" link)

3. **Three gap-fill chapters remain pure 55-line skeletal stubs.** Cycle 1 flagged Ch 56 (Responsible AI Tools, 5 sections), Ch 59 (Distributed Training Systems, 5 sections), Ch 61 (Scale Tools, 5 sections). All 15 sections are literally 55 lines each, identical template: big-picture sentence, three generic H2s with one-line filler, identical 3-item bibliography ("Anthropic. Building Effective Agents", "Karpathy. State of GPT", "HF Open LLM Leaderboard") that bears no thematic relation to the actual section topic. No authoring has happened.

4. **Part 9 top-level index is structurally broken.** `index.html` has: (a) "Part VIII" label and "Part VIII" prose; (b) "Chapters: 3 (Chapters 34, 35, and 36)" stale text; (c) Ch 42 chapter card lists 42.9 twice (one labeled "OpenTelemetry", one mislabeled "Research Methodology for LLM Papers" — actual filename is 42.10) and omits 42.10, 42.11, 42.12 entirely; (d) Ch 44 chapter card lists 44.4-44.7 only (no 44.1/44.2/44.3 — file system confirms they don't exist, but the question becomes whether sections were planned, demoted, or lost); (e) Ch 46 chapter card is duplicated, once before `</main>` once after with malformed nesting.

5. **Ch 42 in-chapter index has the same 42.9-duplicate / 42.10-12-missing problem and an off-by-everything chapter-nav.** The "What's Next" paragraph links to `Chapter 55: LLM Evaluation & Quality Metrics` (text and href both wrong). The prev points at part-5 module-25 with label "Chapter 43"; the next at module-42 (self) with label "Chapter 45".

6. **Ch 46 (LLM-as-Judge) chapter index still shows "Promoted and expanded from old section 42.8" placeholder description on all five section cards.** Wave 16 auto-derive did NOT cover these. Each section needs a proper big-picture-derived description.

7. **Chapter-index `meta`, `<title>`, breadcrumb, and pagefind-meta blocks frequently embed the OLD chapter number and/or pre-rename title.** Examples:
   - Ch 47 index: meta description "Chapter 47: Safety, Ethics & Regulation" + H1 actually says "Adversarial Security and Red Teaming". Pagefind-meta agrees with the stale meta, so search results will mislabel.
   - Ch 48 index: meta/title/breadcrumb all "Chapter 40: Guardrails and Runtime Safety" (correct title, wrong number)
   - Ch 54 index: meta/title "Chapter 46: Watermarking, Provenance, and Deepfake Defense" — both number wrong and title doesn't match cycle 1's rename to "Provenance, Watermarking & Transparency"

8. **Figure / Table / Code Fragment caption numbers are stale across most authored section bodies.** Spot examples:
   - Ch 42 sections show 13+ figures each labeled "Figure 44.x.y" instead of "42.x.y"
   - Ch 43 sections show captions labeled "Figure 46.x.y" instead of "43.x.y"
   - Ch 47 sec 47.1 has "Figure 49.1.1"
   - Ch 52 sec 52.1 has "Figure 53.1.x"; sec 52.2 has "Figure 54.1.x"
   - Ch 53 sec 53.1 has "Figure 55.1.x"; sec 53.4 has "Figure 55.7.x"
   - Ch 54 sec 54.1 has "Figure 56.1.x"; sec 54.5 has "Figure 56.5.x"; sec 54.10 has "Figure 57.5.x"
   - Ch 55 has "Figure 58.1.x" / "Figure 59.5.x"
   - Ch 58 sec 58.1 has "Figure 63.x.y"
   - Ch 60 sec 60.1 has "Figure 53.5.x" and "Table 53.5.x"
   - In-prose references like "Figure 44.1.1 shows..." mirror the stale captions, so renumbering must update both sites at once.

9. **Cross-section prereq labels frequently use OLD chapter/section numbers even when the href is correct.** Common pattern: `<a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">Section 13.1</a>` (visible "Section 13.1", correct href). Touches prerequisite callouts in nearly every authored section across Parts 9-12, plus inline prose ("from Section 14.1", "from Chapter 23"). Examples: 42.1 has "Section 13.1", "Section 14.1", "Section 0.3", "Section 5.2"; 47.1 has "Section 45.1", "Section 14.4", "Section 44.3"; 50.1 has "Section 49.1"; 52.2 has "Section 49.1", "Section 23.1", "Section 44.1"; 53.1 has "Section 49.3", "Section 14.3", "Chapter 44"; 60.1 has "Chapter 09", "Section 45.1", "Chapter 20".

10. **Part 9 has stale Part-number labels in its TOC index** (`Part VIII` in part-label, alt-text, big-picture, and part-overview). Ch 51's "Part IX's platforms" / "Part X turns to the product side" prose is also wrong (Ch 51 sits in Part X, next part is XI ethics, not "product side"). Ch 45's "Part VIII split into two halves" prose and "Part IX turns to safety, Chapter 51 closes Part IX" are mismatched.

## Per-chapter findings

### Part 9: LLM Evaluation & Observability

**Part 9 index (`part-9-llm-evaluation-observability/index.html`)**
- Line 24: `<div class="part-label">Part VIII</div>` — should be "Part IX"
- Line 29: alt text "Part VIII: Evaluation of LLM-Based Systems"
- Lines 37-40: Part overview prose says "Part VIII covers ... Chapters: 3 (Chapters 34, 35, and 36)"
- Line 45: big-picture prose "Part VIII gives you ..."
- Lines 59-61: Ch 42 card has 42.9 duplicate, missing 42.10-42.12 (real sec 42.10 is "Research Methodology", 42.11 is "Structured-Output Validity Testing", 42.12 is "Classical ML Evaluation Metrics")
- Lines 81-84: Ch 44 card lists only 44.4-44.7 (files confirm 44.1-44.3 missing — investigate whether intended)
- Lines 100-125: Ch 46 card duplicated, with `</main>` between the two copies (malformed HTML)

**Chapter 42 (Evaluation Foundations)**
- Index: same duplicate-42.9 / missing-42.10-12 issue as part index; "What's Next" links to "Chapter 55: LLM Evaluation & Quality Metrics" (self); prev "Chapter 43"→Part 5; next "Chapter 45"→self
- Figure 44.0.1 caption (should be 42.0.1)
- All 12 sections (42.1-42.12) have visible H2 prefix "44.x.y", anchor id "34-x-y", and figure/code captions "Figure 44.x.y"
- Section 42.1: visible "Section 5.2", "Section 13.1", "Section 14.1", "Section 0.3" prose refs with mismatched hrefs; Looking-Back/Big-Picture references "Chapter 42.2", "Chapter 20", "Chapter 23.9", "Chapter 43"; meta-description URL embeds `section-42.12` while link text says "perplexity"

**Chapter 43 (Specialized Evaluation)**
- Index breadcrumb "Part VIII"; prev "Chapter 45", next "Chapter 47"
- 5 sections all carry "Figure 46.x.y" and "Code Fragment 46.x.y" captions

**Chapter 44 (Online Eval & Observability)**
- Index breadcrumb "Part VIII"; only 4 sections (44.4-44.7) listed (44.1-44.3 absent); prev "Chapter 46", next "Chapter 48"
- All 4 sections carry "47.x.y" visible H2 labels

**Chapter 45 (Tools of the Trade)**
- Index: "Part VIII split into two halves"; "Part VIII" in section-desc; "Part IX turns to safety, Chapter 51 closes Part IX" (wrong part, wrong chapter — it should be "Part X turns to safety, Chapter 51 closes Part X")
- prev "Chapter 47", next "Chapter 49"
- All 5 tool-of-the-trade sections show "48.x.y" or "36.x.y" visible H2

**Chapter 46 (LLM-as-Judge)**
- All 5 section cards still labeled "Promoted and expanded from old section 42.8" (Wave 16 auto-derive missed Ch 46)
- All 5 sections carry visible H2 prefix not matching 46.x

### Part 10: LLM Security & Runtime Safety

**Part 10 index** — clean.

**Chapter 47 (Adversarial Security)**
- Index: meta + `<title>` + pagefind-meta all say "Chapter 47: Safety, Ethics & Regulation" while H1 correctly says "Adversarial Security and Red Teaming"
- Figure 49.0.1 caption (should be 47.0.1)
- "Looking Back" para wrongly says "Part IX zooms out" (this IS Part X)
- "Chapter Overview" para says "production engineering foundations from Chapter 45" / "alignment techniques covered in Chapter 20" / "strategic and ROI considerations in Chapter 31"
- Learning Obj #2 says "interpretability methods from Chapter 11"
- Prereq labels Chapter 45 / 14 / 44 / 20 with mismatched hrefs (correct hrefs to current modules 62/12/42/18)
- "What's Next" → "Chapter 50: Agent Safety & Security" (should be Ch 49 to match href)
- Section 47.1: breadcrumb says "Chapter 47: Safety, Ethics & Regulation"; pagefind-meta agrees; in-page TOC uses anchor `id="30-1-x"` with visible label "30.1.x"; Figure 49.1.1 caption; "Section 45.1" prereq; "Section 44.3" inline ref; visible H3 "49.1.1 OWASP Top 10..."
- Section 47.2: same H2/caption staleness pattern

**Chapter 48 (Guardrails)**
- Index meta + title + breadcrumb all say "Chapter 40" (off by 8). Header H1 correct
- prev "Chapter 49", next "Chapter 51"
- All 5 sections carry visible H2 / id with stale numbering

**Chapter 49 (Agent Safety)**
- Index "Chapter 60 consolidates the Part IX safety toolchain" (should be Ch 51, Part X)
- prev "Chapter 50", next "Chapter 52"
- All 4 sections show visible H2 prefix "51.x.y" (= file is 49.x but visible label is 51.x)

**Chapter 50 (Privacy)**
- Index next-card label "Chapter 53 Bias, Fairness, and Disparate Impact" — the title was renamed in cycle 1 to "Bias, Fairness & Hallucinations"
- Index prev "Chapter 51"
- Section 50.1: visible H2 prefix "52.2.x" (correct path is 50.1.x); has DUPLICATE H2 sub-numbering inside file (52.2.1 appears for two different subsections — collision)
- Section 50.2: visible H2 prefix "52.5.x" (way off; correct is 50.2.x)

**Chapter 51 (Tools of the Trade)**
- Index "Part IX's platforms" / "Part X turns to the product side, Chapter 71 closes Part X" (multiple cross-part confusion)
- prev "Chapter 59 Frontier Safety", next "Chapter 61: Compute Planning"
- All 5 sections show "60.x.y" visible H2

### Part 11: LLM Ethics, Trust & Governance

**Part 11 index** — clean (visible structure matches cycle-1 fixes).

**Chapter 52 (Bias, Fairness & Hallucinations)**
- Index: prev "Chapter 52: Privacy" (should be Ch 50), next "Chapter 54: Hallucination and Truthfulness" with `href` pointing at module-52-bias-fairness (SELF) — should be Ch 53
- Section 52.1: H2 prefix "53.1.x"; figure "Figure 53.1.x"; in-prose "Section 49.10" pointing at sec 47.1; bottom-nav "In Chapter | Chapter 52 | Bias, Fairness & Hallucinations" (correct) but the chapter title in breadcrumb header says "Chapter 52: Bias, Fairness, and Disparate Impact" (rename not propagated to the breadcrumb header)
- Section 52.2: pagefind-meta `chapter:Chapter 54: Hallucination and Truthfulness` (still stale); H2 prefix "54.1.x"; figures "Figure 54.1.x"; one missing 54.1.4 in numbering sequence (sees 54.1.1, .2, .3, .5)

**Chapter 53 (Regulation)**
- Index prev "Chapter 54: Hallucination and Truthfulness", next "Chapter 56: Watermarking..."
- Section 53.1: visible H2 "55.1.x"; "Figure 55.1.x"; "Chapter 44" in big-picture (should be 42); "Section 49.3" prereq (should be 52.1); "Section 14.3" prereq (should be 12.3)
- Section 53.2: visible H2 "55.2.x"; "Figure 55.2.x"; numbering gap (55.2.2 not in headers shown)
- Section 53.3: visible H2 "55.5.x"
- Section 53.4: visible H2 "55.7.x"; "Figure 55.7.x"

**Chapter 54 (Provenance, Watermarking & Transparency)**
- Index meta + title + breadcrumb all say "Chapter 46: Watermarking, Provenance, and Deepfake Defense" — both number AND title don't match cycle-1's rename
- Index prev "Chapter 55", next "Chapter 57: Transparency, Documentation, and Auditability" with href → SELF (module-54)
- Section 54.1: visible figure "Figure 56.1.x"
- Section 54.3: "Figure 56.3.x"
- Section 54.5: "Figure 56.5.x"
- Section 54.10: "Figure 57.5.x" (off by 3, suggesting that section was moved from old Ch 57 during cycle 1's rebuild)

**Chapter 55 (Environmental Impact & AI Governance)**
- Index prev "Chapter 57: Transparency...", next "Chapter 59: Frontier Safety and Open Problems" with href → SELF (module-55)
- Section 55.1: visible H2 "58.1.x"; "Figure 58.1.x"
- Section 55.2: visible H2 "59.5.x"; whole section was an "AI Governance" orphan in cycle 1 — visible numbers still reflect the orphan source

**Chapter 56 (Responsible AI Tools of the Trade)**
- Skeletal: all 5 sections exactly 55 lines, generic template content, three placeholder H2s per section (Commercial Platforms / Open-Source Platforms / Selection Criteria, etc.), identical 3-entry generic bibliography
- Index missing prev/next nav (only "In Part" link)

### Part 12: LLM Systems at Scale

**Part 12 index** — clean.

**Chapter 57 (Compute Planning)**
- Index "Chapter 68: Scaling Economics: Unit Costs & ROI" in body text (Ch 68 doesn't exist or is wrong)
- Index prev "Chapter 60", next "Chapter 62" + next-href jumps to part-13 (should be Ch 58)
- 4 sections all carry stale H2 prefix

**Chapter 58 (Frontier Systems & Hardware)**
- Index says "Chapter 64 closes Part XII" — Ch 61 closes Part XII
- **Cycle-1 regression unfixed**: Index prev "Chapter 78: Frontier Theory" with href → part-15 module-81; next "Chapter 85: AGI Trajectories" with href → part-15 module-82. The linear-nav rebuild did NOT touch this chapter.
- All 5 sections carry visible H2 prefix "63.x.y"

**Chapter 59 (Distributed Training Systems)**
- Skeletal: all 5 sections 55 lines, template content
- Index has only "In Part" nav (no prev/next)

**Chapter 60 (Edge & On-Device LLMs)**
- Index missing prev/next nav (only "In Part" link)
- Single section 60.1 has stale numbering: visible H2 "53.5.x", "Figure 53.5.x", "Table 53.5.x" (signal that this was migrated from old Ch 53)
- Section 60.1 prereq labels: "Chapter 09" (correct), "Section 45.1" with href pointing at part-14 module-70 (wrong section number), "Chapter 20" with href pointing at module-18 (correct module-18 is alignment, not what label says)

**Chapter 61 (Scale Tools of the Trade)**
- Skeletal: all 5 sections 55 lines, template content, generic bibliography
- Index missing prev/next nav

## Suggested cycle 3 actions

1. **Run an H2/H3 numbering refresh script across all 58 stale section bodies in Parts 9-12.** The script needs to: (a) parse each section's authoritative chapter number from filename + part folder; (b) renumber every `<h2>` and `<h3>` visible label and matching anchor `id` to use `<chapter>.<section>.<n>` sequence; (c) rewrite all "Figure X.Y.Z" / "Table X.Y.Z" / "Code Fragment X.Y.Z" captions AND their in-prose references to use the new chapter prefix; (d) audit anchor `id` collisions (sec 50.1 already has duplicate 52.2.1 / 52.2.4 stems).

2. **Run a chapter-nav and chapter-index meta refresh across all 24 chapter indices in Parts 9-12.** Walk the canonical chapter order (per Part index card list) and write correct prev/next labels + hrefs; backfill `<meta description>`, `<title>`, and pagefind-meta to match the current H1; ensure breadcrumb chapter title matches the rename (Ch 52, 54, 55 still drag old titles in places). Re-add prev/next blocks to Ch 56, 59, 60, 61, and the prev/next half-broken Ch 51, 52, 54, 55, 57, 58.

3. **Fix Part 9 top-level index structural defects:** Part-VIII labels everywhere, the duplicate Ch 46 card with broken `</main>` nesting, the Ch 42 duplicate 42.9 + missing 42.10/11/12, and the Ch 44 chapter card that lists only 44.4-44.7 (decide whether 44.1-44.3 should be created or whether the chapter genuinely begins at 44.4 and the numbering should shift to 44.1).

4. **Author Ch 56, 59, 61 from skeleton to publishable.** Each chapter has 5 generic 55-line sections that need full content build (big-picture, narrative paragraphs, real bibliography per section, code/diagram callouts). Total ~15 sections to write. The format is identical to existing Tools-of-the-Trade chapters in Parts 5 and 9, so an authoring agent can be templated.

5. **Refresh Ch 46 (LLM-as-Judge) section card descriptions.** All 5 sections still labeled "Promoted and expanded from old section 42.8". Auto-derive from each section's big-picture (Wave 16 missed this chapter).

6. **Sweep cross-reference prose / prereq labels across all authored sections.** Strategy: when a `<a href="...">Section/Chapter N">` element's link-text number doesn't match the href's actual chapter/section number, rewrite the link-text to match the href. This is purely mechanical and would catch hundreds of mismatches (every authored section in Parts 9-12 has 2-5 such mismatches: Section 13.1, 14.1, 23.1, 44.x, 45.1, 49.x, 5.2, 0.3, etc.).

7. **Decide and propagate the Ch 52 / Ch 54 chapter titles.** Part 11 index says Ch 52 = "Bias, Fairness & Hallucinations" and Ch 54 = "Provenance, Watermarking & Transparency"; chapter index pages and breadcrumb headers in sections still drag the pre-rename titles. Pick the canonical strings and propagate.

8. **Fix Ch 58 cross-part nav regression.** The Ch 58 index prev/next still point at Part 16 (Ch 83/85) despite cycle-1 attempting to fix it. The linear-nav rebuilder needs to be re-run for Part 12 specifically.

9. **Clean up part-prose mismatches in Tools-of-the-Trade chapters** (Ch 45: "Part VIII split", "Part IX turns to safety, Chapter 51 closes Part IX"; Ch 51: "Part IX's platforms", "Part X turns to the product side", "Chapter 71 closes Part X"). Each Tools chapter has 3-5 cross-part prose claims that need to be rewritten in light of the current part assignment.

10. **Audit and remove the orphan `</main>` / duplicate chapter-card in Part 9 index** before any rebuild, since downstream renderers (KDP, pagefind) may misbehave on the malformed tree.
