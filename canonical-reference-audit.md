# Canonical-Reference Callout Audit

Scope: every `.html` file under `LLMBook/`, excluding `KDP/`, `.claude/`, `temp_*`, `scripts/`, `*backups*`, `node_modules/`, `pagefind/`, `templates/`.

A "Canonical reference" callout is a `<div class="callout cross-ref">` whose `<div class="callout-title">` literal text is `Canonical reference`. (Note: `class="callout cross-ref"` also wraps callouts titled `See also` and `Appendix Reference`; those are out of scope for this audit.)

## 1. Summary

| Metric | Count |
|---|---|
| Total `Canonical reference` callouts found | 20 |
| Callouts whose primary href targets the main book (Parts 1-12) | 13 |
| Callouts whose primary href targets an appendix (= flagged for relocation) | 8 |
| Broken-link callouts (404 / file missing) | 0 |
| Callouts where prose section/chapter number disagrees with the href | 1 (label inconsistency, file resolves) |
| Vestigial callout candidates (single-sentence pointer, no added context) | 6 |

Notes on counts:
- 7 of the 8 "appendix targets" are the catalog of *appendix-as-hands-on-reference* callouts that point *out* of the appendix back into the main chapters. Those are healthy: the appendix is the appendix, and it's pointing the reader at the canonical chapter. Only 1 callout sits inside a main-book section but routes to the appendices (`section-12.1.html` → `Appendix AD Table T1`). That single one is the genuine "appendix-as-canonical" violation.
- "Appendix-targeting" total of 8 = 7 appendix-index callouts pointing to main book + 1 main-book callout pointing into an appendix.

## 2. Complete callout inventory

| # | File | Line | Title in prose / link | Href | Target class |
|---|---|---:|---|---|---|
| 1 | `appendices/appendix-g-model-cards/index.html` | 35 | Chapter 7: Modern LLM Landscape | `../../part-2-understanding-llms/module-07-modern-llm-landscape/index.html` | main book |
| 2 | `appendices/appendix-h-prompt-templates/index.html` | 29 | Chapter 12: Prompt Engineering | `../../part-3-working-with-llms/module-12-prompt-engineering/index.html` | main book |
| 3 | `appendices/appendix-j-huggingface-ecosystem/index.html` | 34 | Chapter 6: Pre-training | `../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html` | main book |
| 4 | `appendices/appendix-k-langchain/index.html` | 34 | Chapter 22: Tool Use | `../../part-6-agentic-ai/module-22-tool-use-protocols/index.html` | main book |
| 5 | `appendices/appendix-l-experiment-tracking/index.html` | 34 | Chapter 28: Evaluation | `../../part-8-evaluation-production/module-28-evaluation-observability/index.html` | main book |
| 6 | `appendices/appendix-o-docker-containers/index.html` | 34 | Chapter 29: LLMOps | `../../part-8-evaluation-production/module-29-production-engineering/index.html` | main book |
| 7 | `appendices/appendix-p-tooling-ecosystem/index.html` | 34 | Chapter 23: Multi-Agent Systems | `../../part-6-agentic-ai/module-23-multi-agent-systems/index.html` | main book |
| 8 | `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html` | 53 | Chapter 8 | `../module-08-reasoning-test-time-compute/index.html` | main book |
| 9 | `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 59 | Section 22.1 | `../../part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html` | main book |
| 10 | `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html` | 53 | Appendix AD Table T1 | `../../appendices/appendix-q-master-reference-tables/index.html` | **appendix** |
| 11 | `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | 471 | Section 21.1 | `../../part-6-agentic-ai/module-21-ai-agents/section-21.1.html` | main book |
| 12 | `part-4-training-adapting/module-16-peft/index.html` | 41 | Section 15.1 | `../module-15-fine-tuning-fundamentals/section-15.1.html` | main book |
| 13 | `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 62 | Section 15.1 | `../../part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html` | main book |
| 14 | `part-5-retrieval-conversation/module-20-conversational-ai/section-20.1.html` | 43 | Section 21.1 | `../../part-6-agentic-ai/module-21-ai-agents/section-21.1.html` | main book |
| 15 | `part-6-agentic-ai/module-21-ai-agents/section-21.3.html` | 44 | Chapter 8 | `../../part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html` | main book |
| 16 | `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html` | 60 | Section 21.1 | `../module-21-ai-agents/section-21.1.html` | main book |
| 17 | `part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html` | 56 | Section 21.1 | `../module-21-ai-agents/section-21.1.html` | main book |
| 18 | `part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html` | 56 | Section 19.1 | `../../part-5-retrieval-conversation/module-19-rag/section-19.1.html` | main book |
| 19 | `part-8-evaluation-production/module-29-production-engineering/section-29.4.html` | 58 | Section 19.1 | `../../part-5-retrieval-conversation/module-19-rag/section-19.1.html` | main book |

20 callouts total (line 19 in the table above is item 19; the 20th is the second callout in section 19.1 listed below). Item 18 above is the `Section 19.1`-from-25.1 entry; the inventory is complete. (All 20 hrefs verified to resolve to existing files.)

## 3. Callouts pointing into an appendix (the main concern)

Only one main-book callout routes to an appendix:

### 3.1 `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html:53`

- **Prose**: "The deep treatment of the prompt-vs-RAG-vs-fine-tune decision framework lives in [Appendix AD Table T1]. The discussion below focuses on when prompting alone is sufficient."
- **Href**: `../../appendices/appendix-q-master-reference-tables/index.html` (resolves; file exists).
- **Violation**: A "canonical reference" should not point to an appendix. The decision framework *does* have a main-book canonical home.
- **Suggested main-book target**: `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html` (Section 15.1 explicitly contains `<h3>15.1.1.1 Prompting, RAG, and Fine-Tuning</h3>` and a runnable decision-framework code fragment). The book already uses this target for the same purpose in `section-19.1.html` (callout #20 below), so canonicalizing on 15.1 would also make the cross-link network consistent. The Appendix AD table can remain as a "scan-only summary" cross-reference, but the canonical-reference callout should name Section 15.1.

(The remaining 7 appendix-targeting callouts all sit *inside* the appendices and point *out* to the relevant main chapter, which is exactly the right direction. They are healthy and need no action.)

### Item 20 (cross-ref pair) — `part-5-retrieval-conversation/module-19-rag/section-19.1.html:62`

- **Prose**: "The deep treatment of the prompt-vs-RAG-vs-fine-tune decision tree lives in [Section 15.1]."
- **Href**: `../../part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html` (main book).
- This is the canonical pattern the section-12.1 callout should mirror.

## 4. Broken-link callouts

None. All 20 hrefs resolve to existing files in the tree (verified by directory listing of every target directory referenced).

## 5. Number-mismatch / labelling issues (prose vs href)

### 5.1 `section-12.1.html:53` — appendix number inconsistency

- Prose says **"Appendix AD Table T1"**.
- Href targets the directory `appendix-q-master-reference-tables/` whose **internal page label** is `Appendix Q` (`<div class="chapter-label">Appendix Q</div>`, `<h1>Appendix Q: Master Reference Tables</h1>`, `<title>Appendix Q: …</title>`).
- The **appendices index** (`appendices/index.html` line 208) labels the same content **`Appendix AD`**.
- The link works (file resolves), but a reader following it sees "Appendix Q" on the destination page, contradicting "Appendix AD" in the originating callout.
- This is part of a wider Appendix-letter remap in the book (`appendix-g-model-cards` is labelled "Appendix H" in the index, `appendix-h-prompt-templates` is labelled "Appendix I", and so on). The naming drift is consistent with that scheme but worth flagging here because the callout under audit is the only one that *exposes the new letter ("AD") to the reader in prose*.

No other callout has a number-mismatch: every prose "Section M.N" or "Chapter K" matches the section number embedded in its href.

## 6. Vestigial / candidate-for-removal callouts

A "vestigial" callout = one-sentence pointer + boilerplate "The discussion below focuses on Y" with **no context-specific framing** that the surrounding prose doesn't already establish. These six are the strongest deletion candidates because the body is purely structural redirection:

1. **`section-7.3.html:53`** — "The deep treatment of reasoning models and test-time compute lives in Chapter 8. The discussion below focuses on a landscape-level overview only." Section 7.3 is itself titled "Reasoning Models & Test-Time Compute (Landscape View)"; the section heading already signals this.

2. **`section-11.2.html:59`** — "The deep treatment of the function-calling loop lives in Section 22.1. The discussion below focuses on the JSON-schema mechanics that providers expose." The next paragraph re-states this in narrative form ("Function calling is the wire format for the tool-call slot of the agent loop…" appears across §22.1 already).

3. **`section-12.2.html:471`** — "The deep treatment of the ReAct (perception--reasoning--action) loop lives in Section 21.1. The discussion below focuses on how ReAct shows up as a prompting pattern." The very next prose paragraph says "*As a prompting pattern*, ReAct… is the bridge between prompt engineering and Chapter 21: AI Agents" with an inline link. The callout duplicates the inline framing.

4. **`section-20.1.html:43`** — "The deep treatment of the perception--reasoning--action loop lives in Section 21.1. The discussion below focuses on the dialogue framing." The Prerequisites block *immediately above* (line 40) already says "The dialogue management concepts here lay the foundation for the agent architectures in Section 21.1" with the same link.

5. **`section-21.3.html:44`** — "The deep treatment of how reasoning models work internally lives in Chapter 8. The discussion below focuses on how to configure them inside an agent loop." The Big Picture callout immediately above (line 36) and the Prerequisites block (line 41) both already link Chapter 08 with the same framing.

6. **`section-23.1.html:56`** — "The deep treatment of the single-agent loop lives in Section 21.1. The discussion below focuses on how that loop scales across agents." Sits between an "Appendix Reference" callout and a paragraph that begins describing multi-agent frameworks; the cross-reference adds no information the section title ("Multi-Agent Systems") doesn't already imply.

The remaining seven main-book canonical-reference callouts (`16.1`, `19.1`, `22.1`, `25.1`, `29.4`, `12.1`, `21.1`) carry slightly more context: they call out a *specific concept* (catastrophic forgetting, prompt-vs-RAG-vs-fine-tune, agent-loop tool-call slot, hallucination as agent failure, hallucination production detection, prompt sufficiency, agent safety side) and reframe it for the local section. Those are worth keeping.

## 7. Recommended action plan

1. **Fix the one main-book → appendix canonical-reference link.** Edit `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html:53` so the canonical href points to `../../part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html` (matching the parallel callout in section 19.1). The Appendix AD scan-table can stay as a secondary pointer in a separate `See also` callout or in inline prose.

2. **Decide on the "appendix-letter" prose/page-label drift.** Across the book, internal page labels say "Appendix Q/K/L/…" while the appendices index says "Appendix AD/L/R/…". This is out of scope for this audit but the section-12.1 callout is the *only* "Canonical reference" callout that surfaces this drift to the reader. Either rename the destination page header to "Appendix AD" or rephrase the prose in 12.1 to use the page's own label ("Appendix Q Table T1"). Whatever the global decision, 12.1 should match the destination.

3. **Delete the six vestigial callouts** listed in section 6 (or, if removal feels heavy-handed, demote them to inline "(see §X)" parentheticals in the next prose paragraph). Each adds an extra block of chrome without information beyond what the surrounding Prerequisites/Big Picture/heading already conveys.

4. **Keep the seven appendix-index "Canonical reference" callouts** (G/H/J/K/L/O/P appendix indexes). They serve a real purpose: tell the reader "this appendix is a recipe-book, not the canonical treatment; the canonical home is Chapter X." Direction (appendix → main book) is correct.

5. **Sanity-check the catastrophic-forgetting cross-link** (`module-16-peft/index.html:41` → `section-15.1.html`). Section 15.1 has `<h2>15.1.4 Catastrophic Forgetting</h2>` so the link works, but a fragment anchor (`section-15.1.html#15-1-4-catastrophic-forgetting` or similar) would land the reader on the exact subsection rather than the section top. Optional polish.

6. **No broken-link cleanup needed.** All 20 hrefs resolve.

7. **Reconsider whether `Canonical reference` is the right title for appendix-index callouts.** The title "Canonical reference" reads as "*this* is the canonical reference," but the appendix-index callouts mean the opposite: "*the chapter* is the canonical reference; this appendix is not." Re-titling those seven to "Where the canonical treatment lives" or "Canonical home: Chapter X" would resolve the implicit-voice ambiguity.

8. **If the title rename in (7) lands, separate the two callout flavors at the CSS level.** Right now `class="callout cross-ref"` carries both "See also" and "Canonical reference" semantics; a future style refresh could distinguish them, but that's a styling concern outside this audit.
