# Wave 3: Content-Currency Remainder + Thin-Section Expansion

**Date:** 2026-05-20
**Branch:** v2.0
**Scope:** Two objective tasks, run after the prior currency agent (see `CONTENT_CURRENCY_DONE.md`).
**Mode:** Implement (surgical edits in place).

---

## Headline finding

The book is already in a high state of currency and content-completeness. The
prior currency agent plus several enrichment waves (post 2026-05-17) closed the
overwhelming majority of the objective findings in `CONTENT_UPDATE_SCOUT.md` and
`wave28_content_issues.md`. This pass made a small number of confident, verifiable
edits and, after a full-book scan, found that the "thin section" premise of
Task B no longer holds.

Both tasks were approached conservatively: a reference was only changed when the
current canonical value is unambiguous, and no already-substantial section was
padded.

---

## Task A: Content-currency remainder

### Method

- Searched the live `section-*.html` and chapter `index.html` bodies (not the
  stale audit JSONL) for the objective patterns named in the brief: bare `GPT-4`
  used as a current-frontier reference, `cl100k_base` presented as current,
  `Gemma 2` / `Phi-3` / `Qwen 2` model-family drift, `MMLU` as "hardest current
  benchmark", and old library version pins.
- Cross-checked every hit against the avoid-list (7.1, 9.5, 31.1, 31.5, 53.5,
  57.1, 63.3, 68.1, 36.3, 36.4, 61.1, plus 2.3, 3.5, 3.8, 7.3, 9.3, 18.x, 20.1,
  22.1, 22.3, 26.2, 32.1, 32.3, 40.1, 42.1, 59.x, 75.2).
- Skipped `<pre><code>`, inline `<code>` identifiers, HuggingFace model IDs,
  URLs, SVG figure text, and bibliography citations (which correctly name the
  original paper/version).

### Edits made (4 currency edits across 3 files)

1. **`part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.1.html`**
   - Research Frontier callout: `"Instruction-tuned models (GPT-4, Claude,
     Gemini)"` -> `"Instruction-tuned frontier models (GPT-4o and the o-series,
     Claude, Gemini, current as of 2026)"`; `"SLMs like Phi-4, Gemma 2"` ->
     `"SLMs like Phi-4, Gemma 3, SmolLM2"`. (Scout findings P1-1, P1-2.)
   - "LLMs Unify Everything" note: `"a single LLM like GPT-4 or Claude"` ->
     `"GPT-4o or Claude"`. (Scout finding P1-1.)

2. **`part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.3.html`**
   - "Canonical 'Fits on a Phone' Reference Models for 2026" list: replaced the
     `Gemma 2 2B` bullet with `Gemma 3 1B / 4B (Google, March 2025)`, noting it
     superseded Gemma 2 2B and that the 4B variant adds vision + 128K context.
   - "Reference models that fit" summary bullet: `Gemma 2 2B` ->
     `Gemma 3 1B/4B (the current Gemma generation, succeeding Gemma 2 2B)`.
   - (Scout finding P1-2 / P12-3, model-family drift where text implies "latest".)

3. **`part-12-llm-systems-at-scale/module-60-edge-on-device-llms/index.html`**
   - Chapter landing-page section description for 60.3: `Phi-3.5 / Gemma 2 /
     Apple Foundation` -> `Phi-3.5 / Gemma 3 / Apple Foundation` (consistency
     with the section-60.3 edit).

### Edit that doubles as currency + expansion (1 edit, counted under Task B too)

4. **`part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.3.html`**
   - Added one paragraph after the Mamba-2 / SSD subsection naming the current
     production hybrid SSM-transformer models the scout flagged as missing:
     Jamba (AI21, 2024), Zamba (Zyphra, 2024), Falcon-H1 (TII, 2025), and xLSTM
     (Beck et al., 2024). (Scout finding P16-1.) Section 75.3 is not on the
     avoid-list; 75.2 is. This is both a currency fix and a substantive content
     addition.

### Objective items checked and deliberately NOT changed (already current)

- **Tokenizer / `cl100k_base` (P1-3):** section 1.7 already distinguishes
  `cl100k_base` (GPT-4/3.5) from `o200k_base` (GPT-4o) in prose, code
  (`encoding_for_model("gpt-4o")`), and a CJK-ratio note. Section 1.8's lab uses
  `cl100k_base` deliberately to compare tokenizers; adding another o200k note
  there would be redundant. tiktoken bibliography already lists o200k_base.
- **Reasoning-model survey (P2-5):** section 8.2 body already covers o1, o3,
  o4-mini, DeepSeek R1 (+ R1-Zero, distill variants), Gemini 2.5 thinking, QwQ.
  Only the fixed `<title>`/`<h1>` ("o1, o3, R1, QwQ") is a snapshot; left
  unchanged to preserve TOC / cross-link title consistency.
- **MMLU:** does not appear in any part `section-*.html` body as "the hardest
  current benchmark"; the one mention (section 3.7, on avoid-list-adjacent) is a
  generic "MMLU multi-step questions" aside. Frontier-benchmark sections already
  cite MMLU-Pro, GPQA-Diamond, HLE, ARC-AGI-2, FrontierMath (per Round 2).
- **Qwen / Gemma elsewhere:** `Qwen2.5`, `Qwen3-VL`, and `Gemma-2 2B (Google,
  2024) and Gemma-3 ...` in section 61.4 are already current/correct; `Qwen2-MoE`
  and `Gemma 2` in section 3.8 are historical architecture-table rows and 3.8 is
  on the avoid-list.
- **Library pins:** `torch==2.5.*` / `torch==2.5.1+cu124` (sections 5.2, 5.3) are
  inline `<code>` teaching examples of pinning practice, hedged ("NumPy 2.x is
  the current line"), not "this is the latest" claims; left per the
  do-not-touch-code constraint and the conservative rule.
- **Context windows / hardware:** Gemini 2.5 Pro (2M / 1M), Grok 4 (July 2025),
  B200/H200/GB200 already current.

---

## Task B: Expand genuinely-thin concept sections

### Method

The `wave28_content_issues.md` under-content list was generated 2026-05-17 from
`book_content_index.jsonl`, whose `word_count` figures predate a large
enrichment wave. Spot-checking proved the counts are stale by roughly 3x:

| Section | wave28 wc | actual prose chars (live) |
|---|---|---|
| 46.3 Debiasing Techniques | 492 | ~9,180 (figure + 2 code frags + 6 callouts + quiz + bib) |
| 46.4 Training Judge Models | 256 | ~6,920 |
| 34.1 IE Landscape | 465 | ~6,160 |
| 46.5 Multi-Judge Ensembles | 394 | ~14,400 |

I therefore re-scanned **all 443 `part-*/**/section-*.html` files** (plus the
appendices and capstone) measuring actual `<main>` prose with `<pre>/<code>/svg/
figure/table/details` stripped, and counted naked narrative `<p>` tags.

### Finding: no genuinely-thin concept sections remain

- Only ~13 sections fall under 4,500 prose chars, and all are catalog/tools
  pages ("Models", "Datasets & Benchmarks", "Libraries & Frameworks",
  "Platforms", "External Reading") in Tools-of-the-Trade modules, which the
  brief explicitly says to leave.
- The thinnest *non-catalog, non-tools concept* section has **10 narrative
  paragraphs and ~7,340 prose chars** (67.3 "Bar Association and Regulatory
  Rules"). The next few (60.1 "Why Edge Deployment", 53.3 "Risk Governance",
  57.2 "Enterprise Integration", 34.1 "IE Landscape", 46.x judge sections) are
  all 5,000-7,500 prose chars with multiple callouts, figures, code, and tables.
- None match the brief's target signature ("a core-concept section with only
  1-2 short paragraphs where a reader would expect more").
- The math-foundations appendix sections (A.1-A.5) are short in *prose* only
  because they are equation-dense quick-reference material; A.5 "Connecting the
  Pieces" is a deliberate one-diagram synthesis page. The capstone is a project
  brief. Padding any of these would change their nature.

### Outcome

No padding was added. The single substantive content expansion this wave is the
section-75.3 hybrid-architecture paragraph above, which fills a real coverage
gap (named production hybrids) rather than inflating an already-complete section.
Forcing 10-15 additions onto well-developed sections would have degraded the
book, contrary to the brief's "do not pad / do not gold-plate" instruction.

---

## Summary

- **Currency edits:** 5 total (section-1.1 x2, section-60.3 x2, module-60
  index.html x1, section-75.3 x1; the 75.3 edit is both currency and expansion).
- **Sections expanded:** 1 (section-75.3, hybrid SSM-transformer models),
  which is also a currency fix.
- **Files touched:** 4
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.1.html`
  - `part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.3.html`
  - `part-12-llm-systems-at-scale/module-60-edge-on-device-llms/index.html`
  - `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.3.html`
- **Constraints honored:** no em dashes / double dashes; no `<pre><code>`, URL,
  or identifier edits; terminology conventions preserved (pretraining, Hugging
  Face, chain-of-thought, fine-tuning); well under the 35-file / 75-minute caps.
- **Audit:** `python -m agents.book-skills.scripts.audit.run --priority P0+P1
  --root .` reports 0 P0/P1 issues.
