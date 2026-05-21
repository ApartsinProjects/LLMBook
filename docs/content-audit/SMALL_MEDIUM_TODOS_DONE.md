# Small/Medium TODOs — Completion Report

**Session:** Mechanical TODO sweep
**Branch:** v2.0
**Date:** 2026-05-20
**Audit baseline:** 80 issues remaining (78 NAV_LINEAR_CHAIN out-of-scope, 1 LAB_COVERAGE, 1 IMAGE_OPPORTUNITY)

## Summary table

| TODO | Description | Status | Files touched | Notes |
|---|---|---|---:|---|
| TODO 2 | Renumber Ch 34/46 h2/h3 ids | DONE | 8 | 21 h2/h3 number rewrites |
| TODO 8 | Bad anchor text label vs href | DONE | ~50 | 101 of 102 label-vs-href mismatches fixed; 1 was a "moved from" note (handled by TODO 32) |
| TODO 15 | CALLOUT_ORDER violations | NO-OP | 0 | Audit reports 0; previously addressed |
| TODO 16 | CONSECUTIVE_HEADINGS | NO-OP | 0 | Audit reports 0; previously addressed |
| TODO 17 | Bare lang-text pseudocode | NO-OP | 0 | Audit reports 0; previously addressed |
| TODO 19 | WRONG_NESTING + NON_CALLOUT_LAB | NO-OP | 0 | Audit reports 0; previously addressed |
| TODO 20 | DIAGRAM_BOTTOM_CAPTION | NO-OP | 0 | Audit reports 0 on listed files; previously addressed |
| TODO 22 | Unwired image confirmation | CONFIRMED | 0 | Brief said "missing from disk" but `figure-5.2.2.png` and `figure-52-2-2.svg` DO exist on disk; both unwired (no HTML refs); no action per brief |
| TODO 23 | HEADING_HIERARCHY | NO-OP | 0 | Audit reports 0; previously addressed |
| TODO 25 | MATH_RENDERING edge cases | NO-OP | 0 | Audit reports 0; previously addressed |
| TODO 30 | BROKEN_FIGURE_REF (figure-32-X-X.svg) | NO-OP | 0 | All `figure-N-M-K.svg/png` refs resolve to existing files |
| TODO 32 | Editing-leftover language leaks | DONE | 3 | 3 actionable items fixed; 6 others verified as legitimate technical content |
| TODO 33 | P0/P1 singletons | DONE | 10 | 11 CALLOUT_NON_CANONICAL (deep-dive type) converted to "note"; all others reported 0 |

## Per-TODO detail

### TODO 2 — Ch 34/46 h2/h3 renumber

Renumbered the h2 (and any nested h3) ids/display numbers in 8 section files so each starts at .1 and increments monotonically.

**Files modified:**

1. `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html`
   - `34.2.2` → `34.2.1` (Classical IE with spaCy)
   - `34.2.3` → `34.2.2` (Open Information Extraction)
   - `34.2.3.1` → `34.2.2.1`, `34.2.3.2` → `34.2.2.2`, `34.2.3.3` → `34.2.2.3`, `34.2.3.4` → `34.2.2.4`, `34.2.3.5` → `34.2.2.5`
2. `section-34.3.html`
   - `34.3.4` → `34.3.1` (Hybrid IE Architectures)
   - `34.3.4.1` → `34.3.1.1` (Building the Hybrid Pipeline)
3. `section-34.4.html`
   - `34.4.5` → `34.4.1` (Production Deployment Patterns)
   - `34.4.5.1` → `34.4.1.1`, `34.4.5.2` → `34.4.1.2`
   - `34.4.6` → `34.4.2` (End-to-End Example)
4. `section-34.5.html`
   - `34.5.7` → `34.5.1` (Coreference Resolution)
   - `34.5.7.1`, `34.5.7.2`, `34.5.7.3` → `34.5.1.1`, `34.5.1.2`, `34.5.1.3`
   - `34.5.8` → `34.5.2` (Integrated Document Understanding Pipeline)
5. `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html`
   - `46.2.2` → `46.2.1` (G-Eval)
6. `section-46.3.html` — `46.3.3` → `46.3.1`
7. `section-46.4.html` — `46.4.4` → `46.4.1`
8. `section-46.5.html` — `46.5.5` → `46.5.1`

Code Fragment / Figure / Exercise numbers were left untouched — they follow a separate counter independent of h2 numbering.

### TODO 8 — Bad anchor text label vs href

After the a/b renumber the legacy `_xref_findings.json` (303 entries from before renumber) became stale. Wrote a fresh scanner that compares the displayed `Section X.Y` label inside `<a>` tags against the section number in the href. Found 102 actual mismatches across 50+ files. Applied a fixer that updates the label to match the href (per brief: "Now that the a/b renumber is done, the targets are section-X.Y.html"). 

After fix: re-scan reports 0 mismatches (the 1 remaining was a "Moved here from the former section 44.1" comment string, handled by TODO 32).

Top-affected files included:
- `part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.2.html` (8 fixes)
- `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html` (5)
- `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.14.html` (5)
- Various module-9, module-10, module-18, module-19, module-31 sections (3-4 each)

### TODOs 15, 16, 17, 19, 20, 23, 25 — Audit-driven categories

For each of these TODOs the corresponding audit check (CALLOUT_ORDER, CONSECUTIVE_HEADINGS, CODE_BLOCK_WRAPPER, WRONG_NESTING, NON_CALLOUT_LAB, DIAGRAM_BOTTOM_CAPTION, HEADING_HIERARCHY, MATH_RENDERING) returned **0 issues** on the current v2.0 tree.

The MASTER_TODO_SESSION_CAPTURE.md counts (51 CALLOUT_ORDER, 52 CONSECUTIVE_HEADINGS, 9 bare lang-text, etc.) are stale; the items were resolved by previous edit cycles before this session ran.

### TODO 22 — Unwired image confirmation

Brief stated: "2 unwired image files: `figure-5.2.2.png` and `figure-52-2-2.svg` — both already missing from disk, so no action needed; just confirm."

Verified: **Both files exist on disk** (not missing):
- `part-1-llm-building-blocks/module-04-decoding-text-generation/images/figure-5.2.2.png`
- `part-14-applications-of-llms-across-industries/module-68-finance-llms/images/figure-52-2-2.svg`

Verified: Neither is referenced in any HTML file (still unwired).

Per brief's "no action needed; just confirm" — left in place. **Flag for human review:** decide delete vs. wire.

### TODO 30 — BROKEN_FIGURE_REF (figure-32-X-X.svg pattern)

Scanned all `section-*.html` (excluding KDP/_archive backups) for `<img src=...figure-N-M-K.(svg|png)>` patterns referencing non-existent files. **0 broken references found.** All such refs resolve to existing assets in the current tree.

### TODO 32 — Editing leftovers (9 items)

Fixed:

1. `part-13-llmops-lifecycle/module-66-reliability-slos-registry/index.html` L84 — Removed "Moved here from the former section 44.1 per the content-placement audit." language leak.
2. `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html` L368-383 — Removed entire "Lab: Pretrain a Tiny Language Model (moved)" stub callout that redirected to Section 6.9.
3. `part-5-multimodal-llms/module-20-audio-music-generation/section-20.2.html` L64 — Removed `<!-- TODO: figure 20.2.1 source asset missing... -->` comment.

Verified as legitimate technical content (no action needed):

4. `section-37.1.html` L207 — "Identify which required slots still need to be filled" is a Python docstring describing dialogue-state functionality, not a placeholder leak.
5. `section-1.7.html` L100 — "Placeholder for tokens not in vocabulary" is a legitimate description of `[UNK]` token semantics.
6. `section-30.2.html` L197 — "Define the prompt with a placeholder for agent scratchpad" is a Python comment describing LangChain `MessagesPlaceholder`.
7. `section-30.2.html` L225 — same context (agent scratchpad placeholder).
8. `section-29.4.html` L249 — "Windsurf (by Codeium, formerly known as the Cascade AI...)" is legitimate product history prose.

### TODO 33 — P0/P1 singletons + CALLOUT_NON_CANONICAL

Audit-check breakdown:
- BROKEN_FIGURE_REF: **0** (previously addressed)
- UNESCAPED_AMPERSAND_TITLE: **0**
- UNCLOSED_P_TAG: **0**
- TRIPLE_DOLLAR_MATH: **0**
- STRUCTURAL_VIOLATION: **0**
- CAPTION_MISALIGN: **0**
- CALLOUT_INTERNAL: **0**
- CALLOUT_NON_CANONICAL: **11** — all of class `deep-dive` (a non-canonical type not in the 21-callout-catalogue).

Fix applied: Converted all 11 `<div class="callout deep-dive">` blocks to `<div class="callout note">` and updated the title prefix from `Deep Dive: ...` to `Note: ...` to satisfy CALLOUT_TITLE_PREFIX. Affected files:

- `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html`
- `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html`
- `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.2.html`
- `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html` (×2)
- `part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html`
- `part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html`
- `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html`
- `part-6-agentic-ai/module-26-ai-agents/section-26.2.html`
- `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html`
- `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html`

NAV_LINEAR_CHAIN (78 issues) intentionally skipped per brief: "being handled by a separate agent".

## Final audit status

`/c/Python314/python -m agents.book-skills.scripts.audit.run --priority P0+P1+P2 --root .`

```
   78  NAV_LINEAR_CHAIN          (out-of-scope: other agent)
    1  LAB_COVERAGE              (out-of-scope)
    1  IMAGE_OPPORTUNITY         (out-of-scope)
Total: 80 issues
```

All in-scope categories cleared (BROKEN_XREF, BROKEN_FIGURE_REF, STRUCTURAL_VIOLATION, CALLOUT_INTERNAL, CALLOUT_NON_CANONICAL, CALLOUT_TITLE_PREFIX, CAPTION_MISALIGN, CONSECUTIVE_HEADINGS, CALLOUT_ORDER, HEADING_HIERARCHY, NON_CALLOUT_LAB, WRONG_NESTING, MATH_RENDERING, TRIPLE_DOLLAR_MATH, UNESCAPED_AMPERSAND_TITLE, UNCLOSED_P_TAG, DIAGRAM_BOTTOM_CAPTION).

## Items flagged for human review

- TODO 22: `figure-5.2.2.png` and `figure-52-2-2.svg` exist on disk but are unreferenced. Brief's premise ("already missing from disk") was incorrect. Need decision: delete (saves ~few hundred KB) vs. wire into appropriate section.
- TODOs 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 18, 21, 24, 26, 27, 28, 29, 31, 34, 35, 36, 37, 38 — out-of-scope authoring-heavy items remain in `ACTIONABLE_TODOS.md`.

## Files touched (count)

- TODO 2: 8 files (Ch 34/46 sections)
- TODO 8: ~50 files (xref label fixes)
- TODO 32: 3 files
- TODO 33: 10 files (11 callouts)

**Total: ~70-75 unique files touched.**
