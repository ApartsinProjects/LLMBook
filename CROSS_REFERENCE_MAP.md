# Cross-Reference Map

This file defines concepts that appear intentionally in multiple chapters at different
levels of depth or in different contexts. The Cross-Reference Architect (Agent #13)
reads this file to ensure all progressive-depth occurrences are linked to each other
with context-differentiating language.

When adapting the pipeline for a different book, create a new `CROSS_REFERENCE_MAP.md`
with the same format, listing the new book's progressive-depth concepts.

## Current Book Structure (10 Parts, 36 Chapters)

| Part | Directory | Chapters |
|------|-----------|----------|
| I: Foundations | `part-1-foundations/` | 00-05 |
| II: Understanding LLMs | `part-2-understanding-llms/` | 06-09, 18 |
| III: Working with LLMs | `part-3-working-with-llms/` | 10-12 |
| IV: Training & Adapting | `part-4-training-adapting/` | 13-17 |
| V: Retrieval & Conversation | `part-5-retrieval-conversation/` | 19-21 |
| VI: Agentic AI | `part-6-agentic-ai/` | 22-26 |
| VII: Multimodal & Applications | `part-7-multimodal-applications/` | 27-28 |
| VIII: Evaluation & Production | `part-8-evaluation-production/` | 29-31 |
| IX: Safety & Strategy | `part-9-safety-strategy/` | 32-33 |
| X: Frontiers | `part-10-frontiers/` | 34-35 |

## Progressive Depth Concepts

Each occurrence MUST link to the others with context-differentiating language that
explains WHY the concept appears again.

| Concept | Locations | Context Differences |
|---------|-----------|-------------------|
| Attention mechanism/formula | 3.3 (introduction), 4.1 (inside Transformer), 4.3 (variants) | Math intro, full architecture, optimization variants |
| GQA (Grouped Query Attention) | 4.3 (architecture), 7.2 (model landscape), 9.2 (memory optimization) | How it works, which models use it, inference speedup |
| MoE (Mixture of Experts) | 4.3 (architecture), 7.2 (production models) | Architecture details, real-world deployment |
| Embeddings | 1.3 (word vectors), 12.2 (feature extraction), 19.1 (retrieval) | Foundational concept, ML pipeline component, search infrastructure |
| Catastrophic forgetting | 14.1 (introduction), 14.3 (hyperparameters), 16.3 (continual learning) | What it is, how to mitigate, advanced solutions |
| Temperature parameter | 5.2 (sampling), 10.1 (API usage), 16.1 (distillation) | Generation control, practical API setting, training hyperparameter |
| Tokenization | 2.1-2.3 (deep dive), 10.1 (API cost), 19.4 (chunking) | How it works, cost implications, retrieval impact |
| Prompt injection | 11.4 (attack patterns), 32.1 (production defense) | Taxonomy and examples, production mitigation strategies |
| RLHF/DPO | 17.1-17.2 (deep dive), 8.3 (reasoning models) | Training methodology, how it shaped frontier models |
| MCP (Model Context Protocol) | 23 (tool use and protocols), 26 (agent safety and production) | Practical tool connection and protocol ecosystem, production governance |
| Agent safety | 26 (agent safety and production), 32.1 (production defense) | Agent-specific risks (sandboxing, tool misuse, autonomous actions), broader production safety and ethics |
| Agent evaluation | 29 (evaluation and observability), 30 (observability and monitoring) | Agent-specific benchmarks (SWE-bench, WebArena, GAIA, TAU-bench), general LLM evaluation methodology |
| Memory (agent context) | 22 (AI agents, MemGPT/Letta), 20.1-20.3 (RAG), 19.1-19.2 (embeddings) | Persistent agent memory and conversation state, retrieval-augmented generation, vector storage infrastructure |
| Interpretability | 18 (deep dive in Part II), 17.3 (alignment diagnostics) | Full interpretability toolkit (probing, logit lens, SAEs), alignment-focused interpretation |
| Reasoning and test-time compute | 8 (deep dive), 7.3 (model landscape context) | Dedicated chapter on CoT, search, verification; brief survey of reasoning-capable models |

## How to Update This File

When a new section is added or a concept is taught in an additional location:
1. Check if the concept already appears in the table above
2. If yes, add the new location and context description
3. If no, add a new row if the concept appears in 2+ chapters at different depth levels
4. Run the Cross-Reference Architect on affected chapters to insert the links

## Cross-Link Phrasing Guidance

When linking between progressive occurrences, use context-differentiating language:

**From earlier (simpler) to later (deeper/applied):**
- "We introduced [concept] in Section X.Y; here we examine how it behaves in production at scale."
- "Building on the [concept] foundations from Section X.Y, this section focuses on [different angle]."

**From later (applied) back to earlier (foundational):**
- "For the mathematical foundations of [concept], see Section X.Y; here we focus on its practical implications for [context]."

**Between peer occurrences (different contexts at similar depth):**
- "While Section X.Y examines [concept] from a [context A] perspective, here we explore its role in [context B]."
