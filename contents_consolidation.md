# Contents Consolidation Audit

**Date:** 2026-05-13
**Scope:** all 213 sections across 11 parts, 35 chapters, 22 appendices
**Method:** keyword density scan + manual review of the cases where multiple sections develop the same topic at explanatory-prose depth

## Headline finding

Most recurring keywords (evaluation, embedding, transformer architecture) repeat **as references**, which is correct — a textbook should cross-reference. But six specific topics repeat at **explanatory-prose depth** across 3+ chapters, which costs the reader pages and dilutes authority. These six need one canonical home each + cross-references everywhere else.

| Priority | Topic | # sections with deep prose | Canonical home | Action elsewhere |
|---|---|---|---|---|
| 🔴 High | **ReAct / perception-reasoning-action loop** | 6 (sections 11.2, 19.1, 20.1, 21.1, 22.1, plus Ch 20/21/22/24 indexes) | **Section 20.1** | One-sentence reminder + cross-reference |
| 🔴 High | **Hallucination definition + mechanism** | 5 (sections 18.1, 19.1, 24.1, 28.4, 29.x) | **Section 18.1** (RAG context) and **Section 29.x** (safety context) | One-sentence reminder + cross-reference |
| 🔴 High | **Prompting vs RAG vs Fine-tuning decision** | 4 (sections 11.1, 14.1, 18.1 intro, FM.4 Problem-Solution Key) + the new FM.0a T1 table | **FM.0a Table T1 (Four-Tier Hierarchy)** + **Section 14.1 decision tree** | All others cross-reference |
| 🟡 Medium | **Catastrophic forgetting** | 7 across Parts I, II, IV | **Section 14.1** (canonical definition + mitigation) | All others cross-reference |
| 🟡 Medium | **Reasoning models / o-series / test-time compute** | 3 (sections 7.3, 8.x full chapter, 20.3) | **Chapter 8** (full canonical treatment) | Ch 7.3 = landscape overview only; Ch 20.3 = agent-specific configuration only |
| 🟡 Medium | **Function calling pattern** | 3 (sections 10.2, 21.1 full, 23.x agent usage) | **Section 21.1** (canonical + the 11-step Wave 10 diagram) | Others cross-reference |

The above issues account for an estimated 8–12 pages of redundant explanatory prose. None of the other 28 high-frequency keywords needs consolidation; their repetition is appropriate cross-referencing.

---

## Detailed findings

### 1. ReAct / Perception-Reasoning-Action Loop 🔴

**Where the loop is explained from scratch:**
1. `section-11.2.html` (Prompt Engineering): ReAct as a prompting pattern.
2. `section-19.1.html` (Conversational AI): the perception-reasoning-action loop as a dialogue pattern.
3. `section-20.1.html` (AI Agents): the canonical agent loop diagram.
4. `section-21.1.html` (Tool Use): the function-calling loop, which is the ReAct loop with tool-call slot.
5. `section-22.1.html` (Multi-Agent): the agent loop scaled across agents.
6. Plus index-page treatments in Chapters 20, 21, 22, 24.

**Problem:** A reader who follows the cross-references in order is told what ReAct is six times. Each treatment adds slight rewording but no new substance after the third occurrence.

**Recommendation:**
- Canonical home: **Section 20.1** with the four-step diagram and explicit citation of the Yao 2022 paper.
- Section 11.2: keep as "prompting pattern" framing, but replace the loop-from-scratch explanation with one sentence + link.
- Section 19.1: same.
- Section 21.1: keep the 11-step expanded diagram (Wave 10 addition) since it adds detail; remove the parallel ReAct explanation in prose.
- Section 22.1: keep the multi-agent framing; cross-reference Section 20.1 for the underlying loop.
- Chapter 20/21/22/24 index pages: remove explanatory prose; keep only one-line section descriptions.

**Estimated savings:** 3–4 pages.

### 2. Hallucination Definition + Mechanism 🔴

**Where hallucination is defined / mechanism explained:**
1. `section-18.1.html` (RAG): hallucination as the motivation for RAG.
2. `section-19.1.html` (Conversational AI): hallucination in dialogue context.
3. `section-24.1.html` (Agent Safety): hallucination as an agent failure mode.
4. `section-28.4.html` (Production Engineering): hallucination in deployment monitoring.
5. `section-29.x.html` (Safety): hallucination as a safety concern.

**Problem:** five separate definitions, three competing mechanism explanations.

**Recommendation:**
- Two canonical homes are appropriate because hallucination is a cross-cutting concept:
  - **Section 18.1** for the mechanism (parametric knowledge has fixed cutoff + lossy compression).
  - **Section 29.x** for the safety implications.
- Other three sections: one-sentence reminder + cross-reference. Specifically:
  - 19.1 should cross-reference 18.1 for mechanism, 29.x for risk framing.
  - 24.1 should cross-reference both.
  - 28.4 should cross-reference 18.1 mechanism + introduce production-specific detection (which is the new content for that chapter).

**Estimated savings:** 2 pages.

### 3. Prompting vs RAG vs Fine-Tuning Decision 🔴

**Where the decision framework appears:**
1. `section-11.1.html` opening (Prompt Engineering): "When to prompt vs. fine-tune."
2. `section-14.1.html` (Fine-Tuning Fundamentals): the formal 5-question decision tree (Figure 14.1.3, the gem of the book).
3. `section-18.1.html` opening (RAG): "When to RAG vs. fine-tune."
4. `front-matter/section-fm.8.html` (Problem-Solution Key): table mapping tasks to chapters.
5. NEW: `front-matter/section-fm.0a-reference-tables.html` Table T1 (Four-Tier Hierarchy from Wave 18).

**Problem:** five places where the reader is told this exists. The senior-editor reviewer flagged this specifically.

**Recommendation:**
- The Wave 18 Table T1 in FM.0a is now the master reference (front matter, scannable).
- The Section 14.1 decision tree is the formal version. Keep both.
- The other three (11.1 opening, 18.1 opening, FM.8) should reduce to a one-line "see FM.0a T1 or Section 14.1" cross-reference.

**Estimated savings:** 1–2 pages.

### 4. Catastrophic Forgetting 🟡

Appears in at least seven files across Parts I, II, IV:
- Part I: in the pretraining-vs-fine-tuning discussion of Chapter 0.
- Part II: in scaling laws and modern landscape (Chapter 6 + 7).
- Part IV: in fine-tuning fundamentals (Chapter 14.1), PEFT (Chapter 15), and continual learning (Chapter 15.7).

**Recommendation:**
- Canonical: **Section 14.1.4** ("Catastrophic Forgetting" subsection already exists).
- Earlier mentions in Parts I/II should be one-sentence forward-references ("we will see in Section 14.1.4 that fine-tuning can erase capabilities — this is called catastrophic forgetting").

**Estimated savings:** 1 page.

### 5. Reasoning Models / o-series / Test-Time Compute 🟡

The curriculum reviewer flagged this: three chapters discuss reasoning models without scoping signals.
1. `section-7.3.html` (Modern Landscape): reasoning models as part of the model landscape.
2. `chapter-8` entire (Reasoning & Test-Time Compute): the canonical deep treatment.
3. `section-20.3.html` (AI Agents): reasoning models as agent backbones.

**Recommendation (already partially done in Wave 22 reading-pathway upgrade):**
- Section 7.3: open with "landscape overview only; deep treatment in Chapter 8."
- Chapter 8: keep as canonical.
- Section 20.3: open with "applying Chapter 8 to agent loops; the configuration concerns are thinking budgets, when to call o3 vs a faster model in the loop."

**Estimated savings:** 1 page (and a much-improved reader experience).

### 6. Function Calling 🟡

Three chapters cover function calling:
1. `section-10.2.html` (LLM APIs): function calling as an API feature.
2. `section-21.1.html` (Tool Use): the canonical 11-step loop diagram (Wave 10).
3. Chapter 23 (Specialized Agents): function calling in agent contexts.

**Recommendation:**
- Section 21.1 is the canonical home (Wave 10 already moved it here).
- Section 10.2 should keep API-format detail (JSON schema syntax, provider differences) but cross-reference 21.1 for the conceptual loop.
- Chapter 23: cross-reference 21.1.

**Estimated savings:** ~1 page.

---

## What is NOT duplicated and should stay

Most of the high-frequency keywords are appropriate cross-references, not duplication:

- **Evaluation** (184 sections): every chapter that ships code should mention evaluation. This is correct.
- **Embedding** (131 sections): foundational, used throughout. Correct.
- **Tokenization** (89 sections): foundational. Correct.
- **LoRA / QLoRA** (75 / 13): canonical home is Chapter 15; cross-references in 14, 16, 17 are appropriate.
- **Guardrail** (56): canonical in Ch 24/29; references in production chapters are correct.
- **Transformer architecture** (52): canonical in Ch 4; references everywhere are correct.
- **Hallucination, RLHF, few-shot, multi-agent, retrieval-augmented, attention mechanism**: high cross-reference counts are correct; only the explanatory-prose duplications above need consolidation.

---

## Recommended action

**Tier-1 (1–2 weeks of work):** Tackle the three 🔴 items (ReAct, hallucination, prompt-vs-RAG-vs-FT). Each is a search-replace of a paragraph + a one-line cross-reference. Estimated total savings: 6–8 pages.

**Tier-2 (3–5 days):** Tackle the three 🟡 items (catastrophic forgetting, reasoning models scoping, function calling). The scoping signals for reasoning models can land as 3 one-line callouts.

**Tier-3 (defer):** No further consolidation needed. The book's other recurring keywords are appropriately distributed.

---

## Companion improvements (out of scope for this audit but related)

1. **Cross-reference inventory.** Build a script that lists every `<a href="../section-X.Y.html">` and verifies the target exists and the anchor name matches a heading. Many sections probably have stale cross-references that point to renumbered locations.
2. **Anchor links inside sections.** Some sections are long enough that a fragment link (`section-X.Y.html#subsection-name`) would help. Currently almost no internal sub-section anchors exist.
3. **The 5 new front-matter pages from Waves 16-22** (FM.0, FM.0a, FM.0b, FM.0c, FM.0d) are net-new and not duplications of existing content; they are the consolidation target for the recurring decisions practitioners make.

---

*End of audit. Next review: after Tier-1 consolidation lands. Re-running the keyword spread analysis should show the 🔴 keywords drop in section-count by 30–50% while the cross-reference counts stay high.*
