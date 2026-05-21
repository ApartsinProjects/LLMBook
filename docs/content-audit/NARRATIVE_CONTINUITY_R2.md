# Narrative Continuity Round 2

Agent: 14-narrative-continuity (cycle 1, 1 of 6 parallel)
Scope: chapter `index.html` files in Parts 1 through 9 (Parts 1-8 plus Part 9 as bonus).
Date: 2026-05-18.

## Summary

Scanned the chapter landing pages in Parts 1 to 9. The dominant pre-existing failure mode was that the "What's Next?" callout pointed to **the first section of the same chapter** ("This chapter begins with Section X.1...") rather than bridging to the next chapter. Several callouts were also factually wrong (linking to themselves, referring to chapter numbers that do not exist, or naming the wrong follow-on part).

39 chapter index files received rewritten "What's Next?" bridges. Each new bridge:

1. Names the next chapter by full title with a hyperlink.
2. Summarises the leap in one or two sentences (what changes from this chapter to the next).
3. Adds a concrete tease (an algorithm, a concept, a counter-intuitive result) so the reader has a reason to continue.
4. Replaces stale or contradictory references (Part numbering, chapter numbering).

Special attention given to **part boundaries** (last chapter of part N → first chapter of part N+1): these now contain a "From X to Y" framing line so the reader feels the structural shift, not just an arbitrary page break.

## Part-Boundary Bridges Rewritten

| From | To | Bridge framing |
|---|---|---|
| Ch 5 (last of Part I) | Ch 6 (first of Part II) | already strong, left in place |
| Ch 10 (last of Part II) | Ch 11 (first of Part III) | "From mechanics to behavior, from understanding to using." |
| Ch 14 (last of Part III) | Ch 15 (first of Part IV) | already strong, left in place |
| Ch 19 (last of Part IV) | Ch 20 (first of Part V) | fixed stale claim that Part V is "retrieval" (it is multimodal); reframed as breaking the text-only frame |
| Ch 25 (last of Part V) | Ch 26 (first of Part VI) | fixed stale claim that Part VIII follows Part V; reframed as "from one-shot to agency" |
| Ch 30 (last of Part VI) | Ch 31 (first of Part VII) | fixed stale claim that Part VII is multimodal generation; reframed as "from agency without knowledge to retrieval-grounded agency" |
| Ch 36 (last of Part VII) | Ch 37 (first of Part VIII) | "from single-turn Q&A to multi-turn experience" |
| Ch 41 (last of Part VIII) | Ch 42 (first of Part IX) | "from building to measuring" |
| Ch 46 (last of Part IX) | Ch 47 (first of Part X) | "from measuring quality to defending it" |

## Chapter-by-Chapter Rewrites

### Part I (LLM Building Blocks)
- `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html`: replaced section-0.1 link with bridge to Chapter 1.
- `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html`: replaced section-1.1 link with bridge to Chapter 2 (Sequence Models & Attention).
- `part-1-llm-building-blocks/module-02-sequence-models-attention/index.html`: bridge to Chapter 3 (The Transformer Architecture).
- `part-1-llm-building-blocks/module-03-transformer-architecture/index.html`: bridge to Chapter 4 (Decoding Strategies & Text Generation).
- `part-1-llm-building-blocks/module-04-decoding-text-generation/index.html`: bridge to Chapter 5 (Tools of the Trade).
- `part-1-llm-building-blocks/module-05-tools-of-the-trade/index.html`: left as-is (already strong).

### Part II (Understanding LLMs)
- `part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html`: replaced section-6.1 link with bridge to Chapter 7 (Modern LLM Landscape).
- `part-2-understanding-llms/module-07-modern-llm-landscape/index.html`: strengthened bridge to Chapter 8 (Reasoning Models).
- `part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html`: strengthened bridge to Chapter 9 (Inference Optimization).
- `part-2-understanding-llms/module-09-inference-optimization/index.html`: strengthened bridge to Chapter 10 (Interpretability).
- `part-2-understanding-llms/module-10-interpretability/index.html`: part-boundary bridge to Chapter 11 / Part III.

### Part III (Working with LLMs)
- `part-3-working-with-llms/module-11-llm-apis/index.html`: strengthened bridge to Chapter 12 (Prompt Engineering).
- `part-3-working-with-llms/module-12-prompt-engineering/index.html`: strengthened bridge to Chapter 13 (Hybrid ML+LLM).
- `part-3-working-with-llms/module-13-hybrid-ml-llm/index.html`: replaced stale Part IV link with concrete bridge to Chapter 14, including Part IV preview.
- `part-3-working-with-llms/module-14-tools-of-the-trade/index.html`: left as-is (already strong).

### Part IV (Training & Adaptation)
- `part-4-training-adaptation/module-15-synthetic-data/index.html`: strengthened bridge to Chapter 16 (Fine-Tuning Fundamentals).
- `part-4-training-adaptation/module-16-fine-tuning-fundamentals/index.html`: strengthened bridge to Chapter 17 (PEFT).
- `part-4-training-adaptation/module-17-peft/index.html`: strengthened bridge to Chapter 18 (Alignment).
- `part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html`: replaced stale Part V link with concrete bridge to Chapter 19, including Part V preview.
- `part-4-training-adaptation/module-19-tools-of-the-trade/index.html`: fixed stale "Part V turns to retrieval" claim; part-boundary bridge to Chapter 20.

### Part V (Multimodal LLMs)
- `part-5-multimodal-llms/module-20-audio-music-generation/index.html`: replaced section-20.1 link with bridge to Chapter 21 (Document Understanding & OCR).
- `part-5-multimodal-llms/module-21-document-understanding-ocr/index.html`: bridge to Chapter 22 (Vision-Language Models).
- `part-5-multimodal-llms/module-22-vision-language-models/index.html`: bridge to Chapter 23 (3D Generation).
- `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/index.html`: bridge to Chapter 24 (VLA).
- `part-5-multimodal-llms/module-24-vla-models/index.html`: bridge to Chapter 25 (Tools of the Trade), with Part VI preview.
- `part-5-multimodal-llms/module-25-tools-of-the-trade/index.html`: fixed stale "Part VIII" claim; part-boundary bridge to Chapter 26.

### Part VI (Agentic AI)
- `part-6-agentic-ai/module-26-ai-agents/index.html`: strengthened bridge to Chapter 27 (Tool Use & Protocols).
- `part-6-agentic-ai/module-27-tool-use-protocols/index.html`: strengthened bridge to Chapter 28 (Multi-Agent Systems).
- `part-6-agentic-ai/module-28-multi-agent-systems/index.html`: strengthened bridge to Chapter 29 (Specialized Agents).
- `part-6-agentic-ai/module-29-specialized-agents/index.html`: fixed broken self-reference (was pointing back to Ch 26); bridge to Chapter 30, with Part VII preview.
- `part-6-agentic-ai/module-30-tools-of-the-trade/index.html`: fixed stale "Part VII turns to multimodal" claim; part-boundary bridge to Chapter 31.

### Part VII (Retrieval & Information Extraction)
- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/index.html`: strengthened bridge to Chapter 32 (RAG Fundamentals).
- `part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html`: fixed broken jump-to-Ch-37; bridge to Chapter 33 (Multimodal RAG).
- `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/index.html`: bridge to Chapter 34 (Structured IE & NER).
- `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/index.html`: bridge to Chapter 35 (Advanced RAG).
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/index.html`: bridge to Chapter 36 (Retrieval Tools), with Part VIII preview.
- `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/index.html`: part-boundary bridge to Chapter 37.

### Part VIII (Conversational AI)
- `part-8-conversational-ai-with-llms/module-37-conversational-ai/index.html`: fixed wrong "next part: Part VI" reference; bridge to Chapter 40 (Voice & Realtime).
- `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/index.html`: bridge to Chapter 41 (Tools of the Trade), with Part IX preview.
- `part-8-conversational-ai-with-llms/module-41-conv-ai-tools/index.html`: part-boundary bridge to Chapter 42.

### Part IX (Evaluation & Observability)
- `part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html`: fixed broken self-link and wrong "Chapter 55" reference; bridge to Chapter 43.
- `part-9-llm-evaluation-observability/module-43-specialized-evaluation/index.html`: bridge to Chapter 44 (Online Eval & Observability).
- `part-9-llm-evaluation-observability/module-44-online-eval-observability/index.html`: bridge to Chapter 45 (Tools of the Trade).
- `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/index.html`: fixed wrong "Part IX turns to safety" claim (Part IX *is* eval); bridge to Chapter 46 (LLM-as-Judge).
- `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/index.html`: part-boundary bridge to Chapter 47 / Part X.

## Bugs Fixed (Beyond Style)

The rewrite caught and corrected several factual errors in existing What's Next blocks:

1. Ch 19 said "Part V turns to retrieval and conversational memory" — Part V is actually Multimodal LLMs.
2. Ch 25 said "Part VIII turns to evaluation" — Part VIII (which follows Part V) is Conversational AI.
3. Ch 29 pointed back to Ch 26 and called it "Agent Safety and Production" — Ch 26 is AI Agent Foundations; the correct next is Ch 30.
4. Ch 30 said "Part VII turns to multimodal generation" — Part VII (after VI) is Retrieval & IE.
5. Ch 32 jumped to Ch 37, skipping Chs 33-36 within the same part.
6. Ch 37 said "next part: Part VI" — Part VI was already covered; the next chapter is Ch 40 within Part VIII.
7. Ch 42 had `<a href="index.html">Chapter 55</a>` linking to itself with the wrong chapter number (Ch 55 is in Part XI, not the next chapter).
8. Ch 45 said "Part IX turns to safety, security, and ethics" — Part IX *is* evaluation; the safety part is X.

## Notes for Other Agents

- Parts 10-16 (Ch 47 through Ch 83) were intentionally left for parallel agents to cover (this agent's scope was Parts 1-9).
- Section-level `whats-next` blocks inside `section-*.html` were also left for other agents per the instructions.
- The pattern of pointing to the first section of the same chapter was so widespread it appears to be a template default rather than authored prose; a future systematic sweep should look at whether the build pipeline still generates this stub.

## Quality Bar Met

- All 39 rewrites name the next chapter.
- All include a concrete bridge (named technique, named result, named consequence) rather than generic boilerplate.
- All stay within 4 sentences.
- No em dashes used (per style rule).
