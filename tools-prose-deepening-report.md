# Tools-of-the-Trade Prose Deepening Report

Date: 2026-05-16
Agent: Prose-deepening pass over flat / thin bullets in Tools-of-the-Trade chapters.

Annotation pattern applied per item: identity (vendor/year), objective (what it solves), main concept (mental model), when-to-pick (or anti-rec). 2-4 sentences each.

## Per-section summary

| Section | Items deepened | Words added (approx) | Status |
|---|---|---|---|
| P1 s6.1-s6.5 | 0 | 0 | in flight (currency agent) |
| P2 s12.1-s12.5 | 0 | 0 | in flight (currency agent) |
| P3 s16.1-s16.5 | 0 | 0 | in flight (currency agent) |
| P4 s21.1 | 9 (fabrics + tracking) | ~1100 | done |
| P4 s21.2 | 8 (algorithm + recipe libs) | ~900 | done |
| P4 s21.3 | 12 (SFT + pretrain + DPO data) | ~1300 | done |
| P4 s21.4 | 9 (base + instruct models) | ~1100 | done |
| P4 s21.5 | 0 | 0 | already-annotated style |
| P5 s25.1 | 11 (managed + self-hosted vector DBs) | ~1500 | done |
| P5 s25.2 | 12 (embedding gens + frameworks + rerankers) | ~1700 | done |
| P5 s25.3 | 11 (retrieval + QA + emb training) | ~1500 | done |
| P5 s25.4 | 13 (open embed + API embed + rerankers) | ~1700 | done |
| P5 s25.5 | 0 | 0 | reading-list (out of scope) |
| P6 s30.1 | 9 (protocols + agent platforms) | ~1500 | done |
| P6 s30.2 | 10 (graph + role + minimal runtimes) | ~1500 | done |
| P6 s30.3 | 10 (SWE + browser + tool benchmarks) | ~1400 | done |
| P6 s30.4 | 11 (frontier + open + VLM models) | ~1500 | done |
| P6 s30.5 | 0 | 0 | reading-list (out of scope) |
| P7 s33.1 | 17 (image + video + audio platforms) | ~2400 | done |
| P7 s33.2 | 11 (diffusion + audio + VLM toolkits) | ~1300 | done |
| P7 s33.3 | 11 (image + video + audio data) | ~1500 | done |
| P7 s33.4 | 16 (image + video + audio models) | ~1700 | done |
| P7 s33.5 | 0 | 0 | reading-list (out of scope) |
| P8 s36.1 | 14 (eval + serving + observability) | ~1900 | done |
| P8 s36.2 | 15 (eval + serving + obs SDKs) | ~1700 | done |
| P8 s36.3 | 12 (knowledge + capability + safety bench) | ~1500 | done |
| P8 s36.4 | 4 (judge + reward) | ~600 | done |
| P8 s36.5 | 0 | 0 | reading-list (out of scope) |
| P9 s39.1 | 10 (moderation + red-team + governance) | ~1400 | done |
| P9 s39.2 | 12 (guardrails + red-team + privacy) | ~1500 | done |
| P9 s39.3 | 11 (harmful + bias + truthful) | ~1500 | done |
| P9 s39.4 | 6 (classifier + reward models) | ~900 | done |
| P9 s39.5 | 0 | 0 | reading-list (out of scope) |
| P10 s50.1 | 8 (AI editors) | ~1200 | done |
| P10 s50.2 | 5 (deployment subsection) | ~800 | done; web frameworks already annotated by other agent |
| P10 s50.3 | 4 (dev benchmarks) | ~500 | done |
| P10 s50.4 | 0 | 0 | already annotated by parallel agent |
| P10 s50.5 | 0 | 0 | reading-list (out of scope) |
| P11 s60.1 | 14 (legal + finance + healthcare vendors) | ~2100 | done |
| P11 s60.2 | 18 (FHIR + finance + legal + edu libs) | ~2400 | done |
| P11 s60.3 | 0 | 0 | already annotated |
| P11 s60.4 | 0 | 0 | already annotated |
| P11 s60.5 | 0 | 0 | reading-list (out of scope) |
| P12 s65.1 | 7 (preprint + curated venues) | ~1200 | done |
| P12 s65.2 | 11 (paper-tracking + repro + ref impls) | ~1700 | done |
| P12 s65.3 | 0 | 0 | already strongly annotated |
| P12 s65.4 | 0 | 0 | in flight (Part 12 enrichment agent) |
| P12 s65.5 | 0 | 0 | in flight (Part 12 enrichment agent) |

## Totals
- Sections touched: 32 of 60
- Items deepened: ~290
- Approximate words added: ~36,000
- Sections skipped because in-flight: 13 (Parts 1-3, P12 s65.4-5)
- Sections skipped because reading-list / already annotated: 15

## Notes
- All annotations follow the pattern: identity (vendor/year), objective + problem it solves, core concept / mental model, pick-when (or avoid-when).
- The currency agent (a7f5ae77) updated several sections in parallel; my prose additions coexist with its currency additions (uv, transformers v5, GRPO, new entrants like SmolTalk, Magpie, Turbopuffer, Vespa, Lightricks LTX, Wan 2.5, NV-Embed-v2, etc.). No edits were reverted.
- The Part 12 enrichment agent (a6a59411) is still working on s65.4-s65.5; those sections were left untouched per coordination rules.
- External Reading sections (xx.5) intentionally untouched: their bullets are paper citations and venue lists rather than tool descriptions; the WHAT/OBJECTIVE/CONCEPT/WHEN pattern does not fit reading-list items.
