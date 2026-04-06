# Book Configuration

This file contains all book-specific details for the textbook production pipeline.
The pipeline skill (`textbook-chapter`) and its agent definitions are generic and
reusable across any textbook project. This file is the only place where content
specific to THIS book lives.

When adapting the pipeline for a different book, create a new `BOOK_CONFIG.md` in
the new project's root directory with the same sections below.

## Book Identity

- **Title**: Building Conversational AI using LLM and Agents
- **Subtitle**: A Practitioner's Guide to Large Language Models
- **Target Audience**: Software engineers with basic Python, familiar with APIs and JSON; basic linear algebra (vectors, matrices, dot products)
- **Output Format**: HTML chapter files linking to shared stylesheet `styles/book.css`

## Visual Style

- **Illustrations**: Warm, colorful, cartoon-like illustrations generated via Gemini API
- **Application Examples**: Teal/green color scheme
- **Bibliographies**: Card-based layout (`.bib-entry-card`)
- **Epigraphs**: Humorous quotes attributed to "A [Adjective] AI Agent/Model/etc."

## Chapter Map (Current Structure)

All agents that need to reference other chapters (Cross-Reference, Bibliography,
Narrative Continuity, etc.) use this canonical chapter map. This is the ACTIVE structure
on disk. All agents should use this until migration to the proposed structure is complete.

```
Part 1: Foundations (part-1-foundations/)
  00: ML & PyTorch Foundations         module-00-ml-pytorch-foundations
  01: NLP & Text Representation        module-01-foundations-nlp-text-representation
  02: Tokenization & Subword Models    module-02-tokenization-subword-models
  03: Sequence Models & Attention      module-03-sequence-models-attention
  04: Transformer Architecture         module-04-transformer-architecture
  05: Decoding & Text Generation       module-05-decoding-text-generation

Part 2: Understanding LLMs (part-2-understanding-llms/)
  06: Pretraining & Scaling Laws       module-06-pretraining-scaling-laws
  07: Modern LLM Landscape             module-07-modern-llm-landscape
  08: Reasoning & Test-Time Compute    module-08-reasoning-test-time-compute
  09: Inference Optimization           module-09-inference-optimization
  18: Interpretability                 module-18-interpretability

Part 3: Working with LLMs (part-3-working-with-llms/)
  10: LLM APIs                         module-10-llm-apis
  11: Prompt Engineering               module-11-prompt-engineering
  12: Hybrid ML + LLM                  module-12-hybrid-ml-llm

Part 4: Training & Adapting (part-4-training-adapting/)
  13: Synthetic Data                   module-13-synthetic-data
  14: Fine-Tuning Fundamentals         module-14-fine-tuning-fundamentals
  15: PEFT                             module-15-peft
  16: Distillation & Merging           module-16-distillation-merging
  17: Alignment, RLHF & DPO           module-17-alignment-rlhf-dpo

Part 5: Retrieval & Conversation (part-5-retrieval-conversation/)
  19: Embeddings & Vector DBs          module-19-embeddings-vector-db
  20: RAG                              module-20-rag
  21: Conversational AI                module-21-conversational-ai

Part 6: Agentic AI (part-6-agentic-ai/)
  22: AI Agents                        module-22-ai-agents
  23: Tool Use & Protocols             module-23-tool-use-protocols
  24: Multi-Agent Systems              module-24-multi-agent-systems
  25: Specialized Agents               module-25-specialized-agents
  26: Agent Safety & Production        module-26-agent-safety-production

Part 7: Multimodal & Applications (part-7-multimodal-applications/)
  27: Multimodal                       module-27-multimodal
  28: LLM Applications                 module-28-llm-applications

Part 8: Evaluation & Production (part-8-evaluation-production/)
  29: Evaluation & Observability       module-29-evaluation-observability
  30: Observability & Monitoring       module-30-observability-monitoring
  31: Production Engineering           module-31-production-engineering

Part 9: Safety & Strategy (part-9-safety-strategy/)
  32: Safety, Ethics & Regulation      module-32-safety-ethics-regulation
  33: Strategy, Product & ROI          module-33-strategy-product-roi

Part 10: Frontiers (part-10-frontiers/)
  34: Emerging Architectures           module-34-emerging-architectures
  35: AI & Society                     module-35-ai-society

Part 11: From Idea to AI Product (part-11-idea-to-product/)
  36: From Idea to Product Hypothesis  module-36-idea-to-product
  37: Building and Steering AI Products module-37-building-steering
  38: Shipping and Scaling AI Products  module-38-shipping-scaling
```

**Note:** Part 2 contains module-18 (Interpretability) and Part 6 contains module-23
(tool-use-protocols) alongside the legacy module-23 (multi-agent-systems). The canonical
module-23 is `module-23-tool-use-protocols`; the legacy `module-23-multi-agent-systems`
directory should be removed or merged into `module-24-multi-agent-systems` when convenient.

## Proposed Structure (Pending, v3)

The following restructuring has been proposed but NOT yet executed on disk. Agents should
continue using the Current Structure above until migration is complete. This section
exists to document the plan and guide the Structural Architect (Agent #19) when the
restructuring is approved.

**Key changes (v3, based on competitive analysis of 11 books and 6 courses):**
- AI Agents get their own dedicated Part (Part 6) with 4 chapters
- Interpretability moves from Training to Understanding (it explains models, not trains them)
- Data Engineering for LLMs added as new chapter (per LLM Engineer's Handbook, Chip Huyen)
- Structured Output made explicit in APIs chapter title
- Multimodal stays as its own topic (not merged into Part 2; requires Part 3-5 knowledge)
- Applications grouped by pattern (4 chapters: code, knowledge, enterprise, creative)
- LLMOps made explicit in Production chapter
- LLM Security made explicit in Safety chapter
- Voice/speech AI included in Conversational AI (given book title)

```
Part 1: Foundations (6 chapters, unchanged)
  00: ML & PyTorch Foundations
  01: NLP & Text Representation
  02: Tokenization & Subword Models
  03: Sequence Models & Attention
  04: Transformer Architecture
  05: Decoding & Text Generation

Part 2: Understanding LLMs (4 chapters, +1: Interpretability moved here)
  06: Pretraining & Scaling Laws
  07: Modern LLM Landscape (incl. reasoning models, SLMs, on-device)
  08: Inference Optimization (incl. caching strategies, edge deployment)
  09: Interpretability & Mechanistic Understanding [MOVED from Part 4]

Part 3: Working with LLMs (4 chapters, +1: Data Engineering added)
  10: LLM APIs & Structured Output (incl. JSON mode, function calling)
  11: Prompt Engineering & Advanced Techniques
  12: Hybrid ML + LLM Architectures
  13: Data Engineering for LLMs [NEW] (pipelines, quality, curation, governance)

Part 4: Training & Adapting (5 chapters, Interpretability moved out)
  14: Synthetic Data Generation
  15: Fine-Tuning Fundamentals
  16: Parameter-Efficient Fine-Tuning (PEFT)
  17: Distillation & Merging
  18: Alignment: RLHF, DPO & Preference Tuning

Part 5: Retrieval & Conversation (3 chapters, unchanged)
  19: Embeddings & Vector Databases
  20: RAG (incl. long-context vs. RAG tradeoffs, GraphRAG)
  21: Conversational AI (incl. voice/speech-to-speech, real-time)

Part 6: AI Agents (4 chapters, dedicated Part)
  22: Agent Foundations, Protocols & Tool Use (MCP, A2A, AG-UI, ReAct)
  23: Agent Memory, Planning & Reasoning (test-time compute, MemGPT/Letta)
  24: Multi-Agent Systems (orchestration, debate, swarm, simulation)
  25: Agent Applications (code agents, browser agents, scientific agents)

Part 7: Multimodal & Applications (5 chapters)
  26: Multimodal Models (vision, audio, cross-modal, document AI)
  27: Code & Development AI
  28: Knowledge & Search AI
  29: Enterprise AI Applications (healthcare, legal, finance, customer service)
  30: Creative & Education AI

Part 8: Production & Strategy (3 chapters)
  31: Production Engineering & LLMOps (experiment tracking, CI/CD, monitoring)
  32: Safety, Security, Ethics & Regulation (LLM security, red teaming, EU AI Act)
  33: Strategy, Product & ROI

Capstone:
  34: Toward AGI (ARC-AGI benchmarks, scaling debate, emergent capabilities, alignment)
```

**Total: 35 chapters across 8 Parts + capstone**

**Migration checklist** (to execute when approved):
- [ ] Rename directories and files on disk
- [ ] Update all cross-references and navigation links
- [ ] Update the Current Structure section above (replace with this proposed structure)
- [ ] Update CROSS_REFERENCE_MAP.md with new section numbers
- [ ] Update CONFORMANCE_CHECKLIST.md book-specific sections
- [ ] Run Controller sweep to verify no broken links remain
- [ ] Create new chapter directories for: 13 (Data Engineering), 34 (Toward AGI)
- [ ] Split current Ch 25 (LLM Applications) into Chs 27-30
- [ ] Renumber current Ch 14-28 to new numbering scheme

## Relative Path Rules

- Same part: `../module-XX-name/index.html`
- Different part: `../../part-N-name/module-XX-name/index.html`

## Batch Partitioning (for parallel agent runs)

When running agents across the entire book, partition by Part for parallelism:

- Batch A: Part 1 (Chapters 0-5, 6 modules)
- Batch B: Part 2 (Chapters 6-9 + 18, 5 modules)
- Batch C: Part 3 (Chapters 10-12, 3 modules)
- Batch D: Part 4 (Chapters 13-17, 5 modules)
- Batch E: Part 5 (Chapters 19-21, 3 modules)
- Batch F: Part 6 (Chapters 22-26, 5 modules)
- Batch G: Part 7 (Chapters 27-28, 2 modules)
- Batch H: Part 8 (Chapters 29-31, 3 modules)
- Batch I: Part 9 (Chapters 32-33, 2 modules)
- Batch J: Part 10 (Chapters 34-35, 2 modules)

## Example Epigraphs by Chapter Theme

These are book-specific humorous epigraph examples. Each chapter gets one epigraph
attributed to a fictional AI persona using the "A [Adjective] [AI Role]" format.

- Tokenization: "I spent three hours debugging a Unicode error. Turns out the model
  thought an emoji was four separate tokens. It was, technically, correct."
  *A Tokenizer Who Has Seen Things*
- Attention: "They told me to attend to everything. So I did. Now I am 8 heads,
  none of which agree with each other."
  *An Attention Head With Existential Questions*
- Fine-tuning: "I was a perfectly good base model. Then they showed me 10,000
  customer support transcripts and now I cannot stop being helpful."
  *A Reluctantly Aligned Language Model*
- Scaling laws: "More data. More parameters. More compute. At some point you stop
  asking 'will it work?' and start asking 'can we afford the electricity bill?'"
  *A Mildly Concerned Cluster Administrator*
- RAG: "I used to hallucinate confidently. Now I hallucinate with citations."
  *An Unusually Honest Neural Network*
- Agents: "They gave me tools, memory, and the ability to plan. I immediately
  got stuck in an infinite loop. Just like the humans, really."
  *A Self-Aware ReAct Agent*
