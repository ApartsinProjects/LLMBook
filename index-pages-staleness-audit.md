# Index Pages Staleness Audit

## Summary

- Part indexes audited: 12
- Chapter indexes audited: 66
- Pages with stale content: **52** (all 12 part indexes + 40 chapter indexes)
- Most common staleness pattern: **section-card numbers in chapter indexes use the OLD chapter number** (e.g. module-10 cards still labeled `9.1`-`9.7`). 26 of 66 chapter indexes exhibit this.

Other recurring patterns:
- Part indexes describe content that has been moved or renumbered (Part 7 still describes the old "AI Applications" content from Part 11; Part 9 still has a Chapter 31 Strategy card that moved to Part 10; Part 12 still has a single Chapter 33 monolith card instead of its 5 actual chapters).
- 5 part indexes reference module directories that do NOT exist (`module-25-agent-safety-production`, `module-31-strategy-product-roi`, `module-33-emerging-architectures`, `module-45-idea-to-product`, `module-48-shipping-scaling`).
- Cross-part links across the chapter indexes routinely point at dissolved modules (Ch 25, Ch 27, Ch 31, Ch 33 old shapes).
- Part 10 chapter indexes for the 8 short-prose chapters (40-44, 46, 47, 49) are unfilled "TODO author this" stubs.
- 12 chapter indexes have broken prev/next nav (point back to the part index rather than the actual sibling module).
- "AI Applications" (old Part 7 title) and "Safety and Strategy" (old Part 9 title) survive in multiple nav blocks.

---

## P0: Severely stale (multiple wrong claims; needs full rewrite)

### part-7-multimodal-generation/index.html
- **Subtitle**: STALE. Says "Multimodal models and real-world LLM applications across industries, from code generation to healthcare to scientific discovery." Yaml says: "Multimodal models and real-world LLM applications across industries, from code generation to healthcare to scientific discovery." (yaml subtitle is *also* stale; the actual part contains only Multimodal Generation, Embodied AI, and Tools of the Trade). Should describe Multimodal Generation only.
- **Part Overview**: WRONG. Describes "in-depth treatment of LLM applications in software engineering, finance, healthcare, cybersecurity, education, and scientific discovery." That content now lives in Part 11.
- **Chapter count**: WRONG. "Chapters: 2 (Chapters 27 and 28)". Actual: 3 (modules 31, 32, 33).
- **Big-Picture callout**: WRONG. "surveys the rich landscape of LLM-powered applications from code generation to healthcare" - that's Part 11 content.
- **Chapter cards**: MISSING Ch 32 (Embodied AI, World Models & Multimodal Reasoning), MISSING Ch 33 (Tools of the Trade). HAS a stale "Chapter 27 LLM LLM Applications Across Industries" card with links to non-existent `module-27-llm-applications/section-27.1.html` through `section-27.7.html`.
- **Section numbering in Ch 31 card**: STALE. Lists `26.1` through `26.7`; should be `31.1` through `31.7`.
- **Next nav target**: Correct (`module-31-multimodal/index.html`).
- **ACTION**: full rewrite needed.

### part-2-understanding-llms/index.html
- **Part Overview**: WRONG. "Chapters: 5 (Chapters 6 through 9, plus Chapter 11: Interpretability)". Actual: 6 chapters (7-12).
- **Chapter cards numbering**: STALE. Cards labeled "Chapter 06/07/08/09" should be "Chapter 07/08/09/10". The Interpretability card is correctly labeled "Chapter 11" but section numbers inside are `10.x`, should be `11.x`.
- **Chapter cards missing**: MISSING Ch 10 (Inference Optimization, but actually present labeled as "Chapter 09" - so chapter 10's content IS there, just numbered wrong). MISSING Ch 12 (Tools of the Trade: Models & Tokenizers).
- **Section numbering in cards**: ALL STALE. Cards have `6.1-6.9`, `7.1-7.4`, `8.1-8.6`, `9.1-9.7`, `10.1-10.4`; should be `7.1-7.9`, `8.1-8.4`, `9.1-9.6`, `10.1-10.7`, `11.1-11.4`.
- **ACTION**: full rewrite needed.

### part-3-working-with-llms/index.html
- **Part Overview**: WRONG. "Chapters: 3 (Chapters 10 through 12)". Actual: 4 (chapters 13-16).
- **Chapter cards**: Has Ch 13/14/15 correctly labeled, but section numbers `11.x`, `12.x`, `13.x` inside the cards are STALE (should be `13.x`, `14.x`, `15.x`).
- **Missing card**: Ch 16 (Tools of the Trade: LLM API Stack).
- **ACTION**: full rewrite needed.

### part-4-training-adapting/index.html
- **Part Overview**: WRONG. "Chapters: 5 (Chapters 13 through 17)". Actual: 5 (chapters 17-21) but Part 4 has 5 chapters not "13 through 17".
- **Chapter cards**: Have Ch 17/18/19/20 correctly labeled, but section numbers `14.x`, `15.x`, `16.x`, `17.x` are STALE (should be `17.x`, `18.x`, `19.x`, `20.x`).
- **Missing card**: Ch 21 (Tools of the Trade: Training & Adaptation Stack).
- **Chapter 20 card description**: WRONG. Body text says "Creating smaller, faster models: knowledge distillation from teacher to student, model merging techniques (TIES, SLERP, DARE)..." That's the OLD Chapter 17/19 content; actual Ch 20 = Alignment: RLHF, DPO & Preference Tuning.
- **ACTION**: full rewrite needed.

### part-5-retrieval-conversation/index.html
- **Part Overview**: WRONG. "Chapters: 3 (Chapters 19 through 21)". Actual: 4 (chapters 22-25).
- **Chapter cards**: Have Ch 22/23/24 correctly labeled, but section numbers `18.x`, `19.x`, `20.x` are STALE (should be `22.x`, `23.x`, `24.x`).
- **Missing card**: Ch 25 (Tools of the Trade: Retrieval & Conversation Stack).
- **ACTION**: full rewrite needed.

### part-6-agentic-ai/index.html
- **Part Overview**: WRONG. "Chapters: 5 (Chapters 22 through 26)". Actual: 5 (chapters 26-30).
- **Chapter cards**: Correctly labeled Ch 26/27/28/29, but section numbers `21.x`, `22.x`, `23.x`, `24.x` are STALE (should be `26.x`, `27.x`, `28.x`, `29.x`).
- **Bad chapter card**: HAS "Chapter 25 Agent Safety, Production & Operations" with links to non-existent `module-25-agent-safety-production/` (this content moved to Ch 38 in Part 9).
- **Missing card**: Ch 30 (Tools of the Trade: Agent Stack).
- **Missing section in Ch 27 card**: Section 27.6 not listed.
- **Missing section in Ch 28 card**: Section 28.6 not listed.
- **What Comes Next**: WRONG. "Continue to Part VII: AI Applications". Part 7 is now Multimodal Generation, not AI Applications.
- **ACTION**: full rewrite needed.

### part-8-evaluation-production/index.html
- **Part Overview**: WRONG. "Chapters: 3 (Chapters 29, 30, and 31)". Actual: 3 (chapters 34-36).
- **Chapter cards**: Have Ch 34/35 correctly labeled, but section numbers `28.x`, `29.x` are STALE (should be `34.x`, `35.x`).
- **Missing card**: Ch 36 (Tools of the Trade: Eval & Production Stack).
- **Chapter 35 card description**: WRONG. Body text says "Production observability with tracing tools, monitoring for drift, experiment reproducibility, and arena-style evaluation at scale." That's Ch 34 content; actual Ch 35 = LLMOps & Deployment Engineering.
- **Nav prev title**: STALE. "Part VII AI Applications" - Part 7 is now Multimodal Generation.
- **What Comes Next prose**: "Part IX: Safety and Strategy" - Part 9 is now "LLM Safety, Security, and Ethics".
- **ACTION**: full rewrite needed.

### part-9-safety-security-ethics/index.html
- **Part Overview**: WRONG. "Chapters: 2 (Chapters 32 and 33)". Actual: 3 (chapters 37-39).
- **Chapter cards**: HAS Ch 37 with correct number, but section numbers `30.x` inside are STALE (should be `37.x`).
- **Bad chapter card**: HAS "Chapter 31 LLM Strategy, Product Management & ROI" with links to non-existent `module-31-strategy-product-roi/` (that content moved to Part 10).
- **Missing cards**: Ch 38 (Agent Safety & Security), Ch 39 (Tools of the Trade: Safety & Guardrails Stack).
- **What Comes Next**: WRONG. Links to "Part X Frontiers" via `../part-12-frontiers/`. Should link to Part 10: Building LLM and Agent Products.
- **ACTION**: full rewrite needed.

### part-10-idea-to-product/index.html
- **`<title>` tag**: STALE. Says "Part XI: From Idea to AI Product" - this is Part X (10), title was renamed to "Building LLM and Agent Products".
- **Meta description**: STALE. Says "Part XI: From Idea to AI Product".
- **Part Overview prose**: Mentions only two chapters (45 and 48). Actual: 11 chapters (40-50).
- **Chapter cards**: Only 2 cards; need 11.
- **Both existing cards have broken module hrefs**: `module-45-idea-to-product/` (should be `module-45-prototype-to-production/`) and `module-48-shipping-scaling/` (should be `module-48-shipping-deploying/`).
- **Section numbering in cards**: STALE. `34.x` should be `45.x`; `35.x` should be `48.x`.
- **Missing cards**: Ch 40, 41, 42, 43, 44, 46, 47, 49, 50.
- **Nav prev**: WRONG. Points to `../part-12-frontiers/index.html` labeled "Part X Frontiers". Should point to Part 9.
- **ACTION**: full rewrite needed.

### part-11-applications-across-industries/index.html
- **`<title>` tag**: STALE. Says "Part XII: LLM LLM Applications Across Industries" - this is Part XI (11).
- **Meta description**: STALE. Says "Part XII: LLM LLM Applications Across Industries".
- **Part Overview**: WRONG. Opens with "Part XII takes the techniques..." - should be Part XI.
- **Chapter cards**: 7 cards present (51-57), MISSING cards for Ch 58 (Creative Industries), Ch 59 (Recommendation & Search), Ch 60 (Tools of the Trade: Industry Solution Stack).
- **What Comes Next**: Stale. Self-links to "Part XII" via `index.html` (this IS Part XI), references dropped "2026 freshness index" resource.
- **Nav prev nav-num**: WRONG. Says "Part XI" but should be "Part X" (current part is XI, so prev is X).
- **ACTION**: full rewrite needed.

### part-12-frontiers/index.html
- **Part Overview**: WRONG. "Chapters: 2 (Chapters 34 and 35)". Actual: 5 (chapters 61-65). Says "Part X surveys the frontier..." - this is now Part XII (12).
- **Chapter card**: SINGLE card "Chapter 33 Emerging Architectures & Scaling Frontiers" with links to non-existent `module-33-emerging-architectures/section-33.1.html` through `section-33.11.html`. This is the OLD monolithic Part 10 Chapter 33; it has since been split into 5 chapters (61-65).
- **Missing cards**: Ch 61 (Frontier Architectures), Ch 62 (Frontier Theory), Ch 63 (Frontier Systems & Hardware), Ch 64 (AGI Trajectories), Ch 65 (Tools of the Trade: Frontier Research Stack).
- **What Comes Next**: WRONG. Says "continue to Part XI: From Idea to AI Product" - Part 12 is the last part; nothing comes next (Appendices follow).
- **Nav prev**: WRONG. Says "Part IX Safety and Strategy" - Part 9 is now "LLM Safety, Security, and Ethics".
- **Next nav target**: BROKEN. Points to `module-33-emerging-architectures/index.html`.
- **ACTION**: full rewrite needed.

### part-1-foundations/index.html
- **Part Overview**: WRONG. "Chapters: 6 (Chapters 0 through 5)". Actual: 7 chapters (0-6, with chapter 6 = Tools of the Trade).
- **Missing card**: Ch 06 (Tools of the Trade: Foundations Stack).
- Otherwise structurally correct (section numbers match).
- **ACTION**: add Ch 06 card; update chapter count.

---

## P1: Chapter indexes with severely stale section card numbers (full rewrite of section cards needed)

The following 26 chapter indexes still use the OLD chapter number on their internal section cards. The section files themselves are correctly named (e.g. `section-22.1.html`), but the visible `<span class="section-num">` value is the pre-renumbering number. The hrefs in these cards are correct.

Each entry follows the pattern: **current chapter / stale displayed prefix**.

- `part-2-understanding-llms/module-07-pretraining-scaling-laws/index.html` - Ch 7 cards display `6.1`-`6.9` (should be `7.1`-`7.9`). Section 7.1 title in card is "The Landmark Models"; yaml says "BERT, GPT, T5: Three Bets That Shaped Today's LLMs".
- `part-2-understanding-llms/module-08-modern-llm-landscape/index.html` - Ch 8 cards display `7.1`-`7.4` (should be `8.1`-`8.4`).
- `part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html` - Ch 9 cards display `8.1`-`8.6` (should be `9.1`-`9.6`).
- `part-2-understanding-llms/module-10-inference-optimization/index.html` - Ch 10 cards display `9.1`-`9.7` (should be `10.1`-`10.7`).
- `part-2-understanding-llms/module-11-interpretability/index.html` - Ch 11 cards display `10.1`-`10.4` (should be `11.1`-`11.4`).
- `part-3-working-with-llms/module-13-llm-apis/index.html` - Ch 13 cards display `11.1`-`11.4` (should be `13.1`-`13.4`).
- `part-3-working-with-llms/module-14-prompt-engineering/index.html` - Ch 14 cards display `12.1`-`12.5` (should be `14.1`-`14.5`).
- `part-3-working-with-llms/module-15-hybrid-ml-llm/index.html` - Ch 15 cards display `13.1`-`13.6` (should be `15.1`-`15.6`).
- `part-4-training-adapting/module-17-synthetic-data/index.html` - Ch 17 cards display `14.1`-`14.7` (should be `17.1`-`17.7`).
- `part-4-training-adapting/module-18-fine-tuning-fundamentals/index.html` - Ch 18 cards display `15.1`-`15.7` (should be `18.1`-`18.7`).
- `part-4-training-adapting/module-19-peft/index.html` - Ch 19 cards display `16.1`-`16.7` (should be `19.1`-`19.7`).
- `part-4-training-adapting/module-20-alignment-rlhf-dpo/index.html` - Ch 20 cards display `17.1`-`17.5` (should be `20.1`-`20.5`).
- `part-5-retrieval-conversation/module-22-embeddings-vector-db/index.html` - Ch 22 cards display `18.1`-`18.5` (should be `22.1`-`22.5`).
- `part-5-retrieval-conversation/module-23-rag/index.html` - Ch 23 cards display `19.1`-`19.9` (should be `23.1`-`23.9`).
- `part-5-retrieval-conversation/module-24-conversational-ai/index.html` - Ch 24 cards display `20.1`-`20.5` (should be `24.1`-`24.5`).
- `part-6-agentic-ai/module-26-ai-agents/index.html` - Ch 26 cards display `21.1`-`21.6` (should be `26.1`-`26.6`). Section 26.1 title in card "The Agent Paradigm" but yaml says "What Makes an LLM an Agent (and What Doesn't)".
- `part-6-agentic-ai/module-27-tool-use-protocols/index.html` - Ch 27 cards display `22.1`-`22.5` (should be `27.1`-`27.6`; missing 27.6).
- `part-6-agentic-ai/module-28-multi-agent-systems/index.html` - Ch 28 cards display `23.1`-`23.3` (should be `28.1`-`28.3`, plus `28.6`).
- `part-6-agentic-ai/module-29-specialized-agents/index.html` - Ch 29 cards display `24.1`-`24.4` (should be `29.1`-`29.4`).
- `part-7-multimodal-generation/module-31-multimodal/index.html` - Ch 31 cards display `26.1`-`26.7` (should be `31.1`-`31.7`).
- `part-8-evaluation-production/module-34-evaluation-observability/index.html` - Ch 34 cards display `28.1`-`28.12` (should be `34.1`-`34.12`).
- `part-8-evaluation-production/module-35-production-engineering/index.html` - Ch 35 cards display `29.1`-`29.9` (should be `35.1`-`35.9`).
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html` - Ch 37 cards display `30.1`-`30.12` (should be `37.1`-`37.12`). Also has a **duplicate sections-list block** appended at line 219; second copy duplicates sections 30.6-30.11.
- `part-10-idea-to-product/module-45-prototype-to-production/index.html` - Ch 45 cards display `34.1`-`34.7` (should be `45.1`-`45.7`).
- `part-10-idea-to-product/module-48-shipping-deploying/index.html` - Ch 48 cards display `35.1`-`35.4` (should be `48.1`-`48.6`; only 4 of 6 sections shown).
- `part-12-frontiers/module-61-frontier-architectures/index.html` - Ch 61 section cards reference `section-33.1.html` through `section-33.11.html` and display `33.1`-`33.11`; only `section-33.4.html` and `section-33.11.html` actually exist in this directory. Real sections that exist are `section-61.1.html` through `section-61.4.html`, plus stale `section-33.4` / `section-33.11`. The chapter index doesn't show any of the 4 actual 61.x sections.

---

## P2: Stale prose (Big Picture, What's Next, cross-references)

### part-6-agentic-ai/module-26-ai-agents/index.html
- **Looking Back**: References "Chapter 21 through 24" (stale numbering for Ch 27-30 / Ch 25 etc).
- **Big-Picture callout**: "production agent deployment (Chapter 25)". Ch 25 is now Tools of the Trade in Part 5; the agent safety content moved to Ch 38 in Part 9.
- **Prereq label**: "Chapter 08 Reasoning & Test-Time Compute"; should be Chapter 09 (yaml).

### part-7-multimodal-generation/module-31-multimodal/index.html
- **Big-Picture callout**: "These capabilities unlock the application patterns surveyed in Chapter 27." Ch 27 = Tool Use, Function Calling & Protocols, not Applications. The old "Chapter 27 LLM Applications" content moved to Part 11.
- **What's Next**: Self-links to "../module-31-multimodal/index.html" labeled "Chapter 27 LLM Applications". Should link to Ch 32 (Embodied AI).
- **Prereq labels**: "Chapter 06 Inside LLMs" (Ch 06 is now Tools of the Trade), "Chapter 07 Training LLMs" (Ch 07 is now Pre-training, Scaling Laws).
- **Nav prev/next nav-title**: STALE. "AI Applications" - Part 7 = Multimodal Generation.

### part-7-multimodal-generation/module-32-embodied-world-models/index.html
- **Why this matters callout**: Links to non-existent `../../part-6-agentic-ai/module-26-agents/index.html` (correct path is `module-26-ai-agents`).
- Otherwise content matches yaml. Best-written chapter index in this part.

### part-2-understanding-llms/module-07-pretraining-scaling-laws/index.html
- **Title meta**: "Chapter 06: Pre-training..." should be "Chapter 7".
- **Looking Back**: "Chinchilla, Kaplan, and the Chinchilla-vs-Kaplan reconciliation all live here." OK content but references "Chapter 04" (correct) and "Chapter 07" (was self-ref, now Modern LLM Landscape).
- **Section 7.1 title**: "The Landmark Models" but yaml says "BERT, GPT, T5: Three Bets That Shaped Today's LLMs".
- **Section 7.6 description**: References "Chapter 20: Distillation & Merging" (Ch 20 is now Alignment; distillation/merging is in Ch 19).

### part-2-understanding-llms/module-10-inference-optimization/index.html
- **Section 10.6 description**: "Bridges to Chapter 08." Chapter 08 is Modern LLM Landscape; reasoning-related content is in Ch 09.
- **Prereq label**: "Chapter 09 Inference Optimization" - this IS Ch 10 (self-reference issue).

### part-3-working-with-llms/module-13-llm-apis/index.html
- **Prereq labels**: "Chapter 05 Decoding Strategies", "Chapter 09 Inference Optimization". Ch 9 is now Reasoning Models; module-10 = Ch 10 Inference Optimization.

### part-3-working-with-llms/module-15-hybrid-ml-llm/index.html
- Multiple cross-refs to Chapter 28 (evaluation), Chapter 31 (Strategy). Ch 28 = Multi-Agent Systems now; Ch 31 → moved to Part 10.

### part-4-training-adapting/module-21-tools-of-the-trade/index.html
- Has bad sibling link `../module-20-evaluating-training/` (no such module).

### part-5-retrieval-conversation/module-22-embeddings-vector-db/index.html
- **Big-Picture callout**: "powers RAG systems in Chapter 23 and grounds conversational AI in Chapter 24" - correct chapter numbers but verifies. (OK actually.)

### part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html
- **Looking Back**: References Chapters III-VIII (acceptable).
- **Chapter Overview prose**: "preparing the ground for the strategic and ROI considerations in Chapter 31". Chapter 31 dissolved; that content is now Part 10.
- **What's Next**: Links to non-existent `../module-31-strategy-product-roi/`.
- **Nav prev/up nav-title**: "Safety and Strategy" - Part 9 = "LLM Safety, Security, and Ethics".

### part-12-frontiers/module-61-frontier-architectures/index.html
- **Title meta and `<title>`**: STALE "Chapter 33: Emerging Architectures & Scaling Frontiers". Now Chapter 61, title "Frontier Architectures & Scaling".
- **Looking Back**: "Part X covers what it has not." Now Part 12.
- **Prereq labels**: "Chapter 06" (now Tools of Trade not Pretraining), "Chapter 09" (now Reasoning not Inference). The hrefs do point to the right modules (07 and 10).
- **Section cards**: ALL point to non-existent `section-33.1.html` through `section-33.11.html`. Real files: section-61.1 through 61.4, plus stale section-33.4 and section-33.11.

### part-11-applications-across-industries/module-51-legal-llms/index.html, module-52-finance-llms, module-53-healthcare-llms, module-54-education-llms, module-55-cybersecurity-llms, module-56-government-llms, module-57-manufacturing-llms
- These chapter pages embed body-text headings `<h2>36.1`, `<h2>36.2` etc. - stale (old Chapter 36 numbering; now Ch 51-57). Multiple modules.
- All seven reference non-existent `part-7-multimodal-generation/module-27-llm-applications` (where Ch 27 LLM Applications used to live; now dissolved).
- Module 52 also references non-existent `part-9-safety-security-ethics/module-31-strategy-product-roi`.
- Modules 55, 57 reference non-existent `part-6-agentic-ai/module-25-agent-safety-production`.

### part-1-foundations/module-00-ml-pytorch-foundations/index.html
- **Chapter Overview**: "from NLP fundamentals (Chapter 01) ... AI agents (Chapter 26)." Ch 26 is still AI Agent Foundations (correct).
- **Section 0.1 card title**: "ML Basics: Features, Optimization & Generalization"; yaml says "What Every LLM Engineer Needs From Classical ML".
- **Section 0.3 card title**: "PyTorch Tutorial"; yaml says "PyTorch in 90 Minutes: Tensors to Training Loop".
- **Section 0.4 desc**: "See also AI Agents (Chapter 26)" - correct.
- Section 0.1 desc references "pretraining and scaling (Chapter 06)" - now Ch 07.
- Section 0.3 desc references "PEFT (Chapter 19) and inference optimization (Chapter 09)" - inference optimization is now Ch 10.

### part-1-foundations/module-04-transformer-architecture/index.html
- **Section 4.1 card title**: "Transformer Architecture Deep Dive"; yaml says "How a Transformer Computes One Token".
- **Section 4.2 description**: "building on Chapter 01's embedding foundations" - correct.
- **Section 4.3 description**: "with variants revisited in Chapter 07" - Ch 07 is now Pretraining (was previously Modern LLM Landscape).

### part-1-foundations/module-06-tools-of-the-trade/index.html
- Otherwise correct, but **nav next** points back to part index instead of next chapter (Chapter 7, Part II).

### part-2-understanding-llms/module-12-tools-of-the-trade/index.html
- **Nav next** points back to part index instead of Ch 13 in Part III.
- **Nav prev** points to part index instead of Ch 11.

### part-3-working-with-llms/module-16-tools-of-the-trade/index.html
- **STUB**. Big-Picture says "TODO author this big-picture callout"; What's Next says "TODO author this." Nav prev and next both wrong.

### part-10-idea-to-product/module-40-ideation/index.html
- **STUB**. Big-Picture "TODO author this", What's Next "TODO author this", section card title "(authoring stub)". Nav prev / next broken.

### part-10-idea-to-product/module-41-product-management/index.html
- **STUB**. Same TODO pattern. Nav prev / next broken.

### part-10-idea-to-product/module-42-strategy-prioritization/index.html
- **STUB**. Same TODO pattern. Section cards: 4 stubs. Nav prev / next broken.

### part-10-idea-to-product/module-43-vibe-coding/index.html
- **STUB**. Same TODO pattern. Nav prev / next broken.

### part-10-idea-to-product/module-44-mvp/index.html
- **STUB**. Same TODO pattern. Nav prev / next broken.

### part-10-idea-to-product/module-46-compute-planning/index.html
- **STUB**. Same TODO pattern. Nav prev / next broken.

### part-10-idea-to-product/module-47-scaling-economics/index.html
- **STUB**. Same TODO pattern. Nav prev / next broken.

### part-10-idea-to-product/module-48-shipping-deploying/index.html
- **NOT a stub but has broken cross-link**: `../module-45-idea-to-product/` (correct dir is `module-45-prototype-to-production`).
- Section card numbering stale (35.x instead of 48.x).

### part-10-idea-to-product/module-49-post-launch-monitoring/index.html
- **STUB**. Same TODO pattern. Nav prev / next broken.

### part-12-frontiers/module-63-frontier-systems-hardware/index.html
- Nav next + prev navs both point to part index instead of siblings.

### part-12-frontiers/module-64-agi-trajectories/index.html
- Same broken nav prev + next.

---

## P3: Stale subtitle, metadata, or single nav issue

### part-9-safety-security-ethics/index.html (also P0)
- Already covered above.

### part-10-idea-to-product/index.html (also P0)
- `<title>`: "Part XI: From Idea to AI Product" - should be "Part X: Building LLM and Agent Products".
- meta description: same.

### part-11-applications-across-industries/index.html (also P0)
- `<title>`: "Part XII" - should be "Part XI".
- meta description: same.

### part-5-retrieval-conversation/module-23-rag/index.html, module-24-conversational-ai/index.html
- (covered in P1 above for section-num staleness)

### part-9-safety-security-ethics/module-38-agent-safety-security/index.html (not yet inspected in detail)
- Likely OK structurally given consistent numbering through the rest of the part-9 modules; section files match `38.1`-`38.4` per yaml.

### part-9-safety-security-ethics/module-39-tools-of-the-trade/index.html (not inspected)
- Section files `39.1`-`39.5` exist matching yaml.

### Modules NOT checked individually but inferred correct based on the section-num scan
The following chapter indexes do NOT have stale section-num spans (their section card numbers match the actual chapter number). They may still have other staleness (cross-refs, prereq labels, broken nav, prose). Confirmed-clean for the section-cards check only:
- All Part 1 modules (00, 01, 02, 03, 04, 05, 06) except 06's nav-next.
- Part 2 module 12 (Tools of the Trade) - structurally OK, only nav broken.
- Part 4 module 21 (Tools of the Trade) - has one broken sibling link to `module-20-evaluating-training`.
- Part 5 module 25 (Tools of the Trade).
- Part 6 module 30 (Tools of the Trade).
- Part 7 module 32 (Embodied AI) - one broken cross-link to module-26-agents.
- Part 7 module 33 (Tools of the Trade).
- Part 8 module 36 (Tools of the Trade).
- Part 9 modules 38 (Agent Safety) and 39 (Tools of the Trade).
- Part 11 modules 51-60 (industry chapters) - content uses `<h2>36.x` in-body headings that are stale.
- Part 12 modules 62, 63, 64, 65 - section numbers OK but 63/64 have broken nav.

---

## Cross-cutting issues to fix in a single pass

1. **Replace stale section-card-number prefixes** in 26 chapter indexes (P1 list).
2. **Add missing chapter cards** to part indexes 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 (all 12 part indexes are missing at least one card; several missing many).
3. **Fix bad module hrefs** in chapter cards: 5 part indexes link to non-existent modules.
4. **Re-author stub chapter indexes**: 9 modules (3-module 16; 10-modules 40, 41, 42, 43, 44, 46, 47, 49).
5. **Fix nav prev/next**: 13 chapter indexes (modules listed in P2/P3).
6. **Remove "AI Applications" Part-7 references** in 3 pages and "Safety and Strategy" Part-9 references in 4 pages.
7. **Remove "2026 freshness index" mention** in `part-11-applications-across-industries/index.html` (dropped resource).
8. **Resolve duplicate sections-list block** in `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html` (lines 219-282 duplicate of 91-218 partial).
9. **Resolve stale `<h2>36.x` body headings** in 7 industry chapters (51-57); these are content chapters, not just indexes, but the heading prefix needs to be `51.x`, `52.x`, etc.
10. **Fix `<title>` tag and meta description** for Part X (says "XI") and Part XI (says "XII").
