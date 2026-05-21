# Content Audit Remediation Plan

Consolidated from 4 parallel audit reports (2,277 lines of findings) covering Parts 1-16 + appendices.

## Wave 11: Mechanical bulk sweeps (single script, low risk)
- Fix appendix title/letter mismatches from Wave 9F rename
- Rewrite stale part-name breadcrumbs / pagefind-meta to canonical names per file's actual part
- Fix substitution corruptions ("Hugging Face softmax library" → "Transformers library", "for softmax" → "for LLMs")
- Fix sections 42.10/42.11 self-titling as 42.9
- Fix module-08 self-referencing "Section 8.3"
- Fix module-10 next-link pointing to self
- Fix module-10 image src double-prefix
- Fix Apx C self-reference Reading Pathways "Section D.7" artifact + dangling "Appendix E" next link
- Move Ch 0 to top of Part 1 index

## Wave 12: Index page rebuilds
- Rebuild appendices/index.html with cards
- Build Part 5 chapter cards (empty)
- Build Part 7 missing cards (31/32/33)
- Build Part 8 missing card (37)
- Build Parts 10/11/12 chapter cards (empty placeholders)
- Add Part 13 missing Ch 62 card
- Fix Part 9 stale chapter numbers (44-48 → 42-46) + duplicate Ch 46
- Fix Part 14 broken index (9 cards for 5 modules)
- Fix Part 15 phantom Ch 79/80
- Fix Part 16 triple-numbering conflict
- De-inflate Tools chapters (demote anchor sub-headings to sub-headings under parent section card)

## Wave 13: Hidden chapter halves in Part 5
- Ch 20 rename "Audio and Music Generation" → "Audio, Music, and Video Generation"; add 20.6-20.10 cards; fix 20.6-20.10 breadcrumbs ("Chapter 33" → 20)
- Ch 22 rename "Vision-Language Models" → "Vision-Language and Omni Models"; add 22.6-22.9 cards; fix breadcrumbs ("Chapter 37" → 22)
- Ch 24 rename "Vision-Language-Action Models" → "VLA Models and LLM-Powered Robotics"; add 24.7-24.13 cards; fix breadcrumbs ("Chapter 40" → 24)

## Wave 14: Ch 41 content rewrite
- Sections 41.1-41.5 currently contain retrieval/RAG tooling content (vector DBs)
- Rewrite to actual Conversational AI tooling (Botpress, Rasa, LangChain conv memory, voice frameworks, PersonaChat/MultiWOZ benchmarks, chat-tuned models)

## Wave 15: Misc structural
- Move Part 2 Tools chapter out of `module-10-interpretability/section-10.5-10.9` to own module dir
- Fix Part 4 Ch 19 (PEFT) scope: rename to "Parameter-Efficient Fine-Tuning, Distillation & Merging"
- Resolve Part 3 Ch 15.5 cross-part jump (drop card or convert to "See also")
- Resolve Part 2 Ch 8 duplicate 8.3 cards
- Fix Part 4 module-18 duplicate sec 18.5 card
- Move orphan section 52.2 (Hallucinations) out of bias chapter
- Move orphan section 55.2 (AI Governance) out of env chapter
- Decide Ch 54 split (Watermarking + Transparency 54.6-54.10)
- Resolve Part 14 module-67 (15 sections in one chapter — split)
- Resolve Part 15 module-78 phantom Ch 79/80 (split out Creative + Recommendation content)

## Wave 16: Replace placeholder section descriptions (per-section, hundreds)
- Use agent-proposed text from reports
- Spawn agents for any sections without proposed text

## Wave 17: Consolidation candidates (6)
- Agentic RAG: 27.5 ↔ 32.2
- Memory: 26.6 ↔ 37.3
- Sim-to-real: 24.6 ↔ 24.13
- GraphRAG: 35.2 ↔ 35.3
- Code-gen agents: 29.1 ↔ 29.4
- Ch 41 ↔ Ch 36 (addressed by Wave 14)

## Wave 18: Re-audit cycle (4 agents)
- Compare findings against Cycle 1
- Apply Cycle 2 edits
- Repeat until findings converge

## Wave 19: Front Matter deep pass
- After content stabilizes

## Stopping criteria
- Audit reports return only minor cosmetic findings
- Each per-chapter section in the audit reduces to "Chapter X: clean" lines
