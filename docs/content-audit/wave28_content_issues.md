# Wave 28: content-issue audit (duplication, focus, lack)

Index audited: book_content_index.jsonl (554 records, 433 teaching sections).
Date: 2026-05-17.

Heuristics used:
- Duplication: Jaccard on substantive heading-token sets, augmented by
  SequenceMatcher ratio on `big_picture` text. Flag at Jaccard >= 0.35 or
  (Jaccard >= 0.20 and big_picture similarity >= 0.45). Pairs in which BOTH
  ends are recognised structural templates (Tools-of-the-Trade closing,
  Vendors & Further Reading, hands-on lab scaffolding with
  Prerequisites/Setup/Objective/Expected Output/Exercises) are clustered
  separately, since their similarity is by-design and not actionable.
- Loss of focus: sections with 7-25 sub-headings where the top recurring
  heading token covers less than 15% of headings, or >= 6 distinct themes
  appear at frequency >= 2 with low coherence, plus a -1 penalty when the
  section title explicitly signals a broad survey (e.g. 'foundations',
  'in 90 minutes', 'landscape').
- Under-content: word_count < 2000 OR sub-headings < 3 OR no big_picture
  OR callouts < 1; severity = number of flags triggered.
- Over-content: body byte_size > 150 KB.
- Per-chapter health: imbalance when smallest section < one-third of
  largest and < 20 KB; no bibliography on any section; one section without
  images while every sibling has them.

## Top issues

1. **[over-content]** §19.2 Libraries & Frameworks
   317 KB body / 14098 words on a single page (`part-4-training-adaptation/module-19-tools-of-the-trade/section-19.2.html`). Split into multiple sub-sections or move deep-dive material to appendix.
2. **[duplication (template)]** 33 template-vs-template pairs across 23 sections
   Closing-section template (Tools of the Trade §N.5 + Part-15 'Vendors and Further Reading'). Action: confirm intentional template (preserve), and ensure each instance customises content beyond boilerplate headings.
3. **[duplication (substantive)]** §25.3 Datasets & Benchmarks ↔ §25.4 Models
   Jaccard 0.50, big_picture sim 0.07. Shared tokens: video, music, audio, image, comparing. Paths: `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.3.html` and `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.4.html`. Verify cross-reference exists, otherwise consolidate.
4. **[focus]** §9.3 Speculative Decoding
   25 headings; top theme 'speculative' covers only 3/25; themes: speculative, draft, model, based. `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html`
5. **[focus]** §9.7 GPU Kernel Programming for LLM Optimization
   25 headings; top theme 'triton' covers only 3/25; themes: triton, kernel, step, gpu. `part-2-understanding-llms/module-09-inference-optimization/section-9.9.html`
6. **[focus]** §31.3 Vector Database Systems
   25 headings; top theme 'filtering' covers only 3/25; themes: filtering, amp, vector, reciprocal. `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html`
7. **[under-content (systemic)]** 5 sections in chapter ('part-9-llm-evaluation-observability', 46) flagged severe
   Multiple stub sections in the same chapter. Either expand each to median size or merge into siblings.
8. **[under-content]** §71.3 Datasets & Benchmarks
   flags: wc=287, h2/3=2, no big_picture, callouts=0; `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.3.html`
9. **[missing-bibliography]** 13 chapters with 0% bibliography coverage
   Includes: ('part-5-multimodal-llms', 24), ('part-10-llm-security-runtime-safety', 51), ('part-11-llm-ethics-trust-governance', 56), ('part-12-llm-systems-at-scale', 61). Add at least Further Reading callout on chapter-wrap section.
10. **[mismatched-scopes]** Chapter ('part-4-training-adaptation', 19) sections range 6.9-316.8 KB
   Largest section is 46x the smallest in the same chapter. Rebalance or split.


## Duplication candidates

### Template clusters (deliberate scaffolding, audit but do not blindly merge)

- **Total template-vs-template pairs**: 33 across 23 sections.

  - **Closing-section template** (`Tools of the Trade §N.5` + Part-15 `Vendors and Further Reading`):
    - 24 pairs across 17 sections.
    - Sample paths: `part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.5.html`; `part-14-applications-of-llms-across-industries/module-67-legal-llms/section-67.5.html`; `part-14-applications-of-llms-across-industries/module-68-finance-llms/section-68.5.html`; `part-14-applications-of-llms-across-industries/module-69-healthcare-llms/section-69.5.html`
    - Shared scaffolding headings: "Communities", "Foundational Papers", "Canonical External References", "Cross-References Inside This Book", "What Comes Next".
    - Verdict: by-design template, not uncoordinated duplication. **Do not merge.**
    - Action: audit each instance has 3-5 specific links beyond the boilerplate; decide whether `External Reading & Communities` should remain its own §N.5 or roll into §N.4 as a tail-callout.

  - **Hands-on lab template** (Prerequisites / Setup / Objective / Expected Output / Exercises):
    - 9 pairs across 6 sections.
    - Sample paths: `part-6-agentic-ai/module-26-ai-agents/section-26.3.html`; `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html`; `part-6-agentic-ai/module-28-multi-agent-systems/section-28.1.html`; `part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html`
    - Shared scaffolding headings: Prerequisites, Setup, Objective, Expected Output, Exercises.
    - Verdict: standard lab structure - intentional pedagogical pattern. **Do not merge.**
    - Action: confirm each lab actually delivers distinct content under those headings (different setup steps, different exercises, different expected output). Use this list as a checklist for lab quality review.

### Substantive (non-template) duplication candidates

- **§25.3 Datasets & Benchmarks** ↔ **§25.4 Models**
  - heading-Jaccard 0.50; big_picture similarity 0.07; INTRA-CHAPTER (likely deliberate split; check for cross-ref)
  - top shared tokens: `video, music, audio, image, comparing`
  - paths: `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.3.html` , `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.4.html`
  - action: MERGE or pick one as canonical; convert the other to a stub with pointer.

- **§25.1 Platforms** ↔ **§25.4 Models**
  - heading-Jaccard 0.50; big_picture similarity 0.05; INTRA-CHAPTER (likely deliberate split; check for cross-ref)
  - top shared tokens: `music, audio, image, video`
  - paths: `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.1.html` , `part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.4.html`
  - action: MERGE or pick one as canonical; convert the other to a stub with pointer.

- **§10.8 Models** ↔ **§14.4 Models**
  - heading-Jaccard 0.40; big_picture similarity 0.05; CROSS-CHAPTER (check for uncoordinated duplication)
  - top shared tokens: `api, open, closed, default, weight, picking, small, tier`
  - paths: `part-2-understanding-llms/module-10-interpretability/section-10.10.html` , `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html`
  - action: Verify both sections explicitly cross-reference each other; otherwise consolidate.

## Loss-of-focus sections

- **§9.3 Speculative Decoding** (`part-2-understanding-llms/module-09-inference-optimization/section-9.4.html`)
  - 25 sub-headings; reasons: top heading token 'speculative' covers only 12% of 25 headings; 8 distinct recurring themes
  - top heading themes (token, freq): speculative (3), draft (2), model (2), based (2), tree (2), implementation (2)
  - first 6 headings: _Prerequisites; The Core Principle; Acceptance and Rejection Sampling; Why the Output Distribution Is Preserved (Informal Proof); Expected Speedup; Draft Model Strategies_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§9.7 GPU Kernel Programming for LLM Optimization** (`part-2-understanding-llms/module-09-inference-optimization/section-9.9.html`)
  - 25 sub-headings; reasons: top heading token 'triton' covers only 12% of 25 headings; 8 distinct recurring themes
  - top heading themes (token, freq): triton (3), kernel (3), step (3), gpu (2), programming (2), flashattention (2)
  - first 6 headings: _Prerequisites; Why Custom Kernels Matter; Arithmetic Intensity Analysis; Triton: Python-Based GPU Kernel Programming; A First Triton Kernel: Vector Addition; Fused Softmax Kernel_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§31.3 Vector Database Systems** (`part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html`)
  - 25 sub-headings; reasons: top heading token 'filtering' covers only 12% of 25 headings; 6 distinct recurring themes
  - top heading themes (token, freq): filtering (3), amp (3), vector (2), reciprocal (2), rank (2), fusion (2)
  - first 6 headings: _Prerequisites; Vector Database Architecture; Purpose-Built Vector Databases; Pinecone; Qdrant; Weaviate_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§10.4 Explaining Transformers** (`part-2-understanding-llms/module-10-interpretability/section-10.4.html`)
  - 24 sub-headings; reasons: top heading token 'explanation' covers only 12% of 24 headings; 8 distinct recurring themes
  - top heading themes (token, freq): explanation (3), attention (3), explanations (3), interpretability (3), methods (2), captum (2)
  - first 6 headings: _Prerequisites; The Explanation Problem; Attention Rollout; Gradient-Weighted Attention; Layer-wise Relevance Propagation (LRP); Perturbation-Based Explanations_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§26.5 End-to-End Agent System Architecture: A Deployment Blueprint** (`part-6-agentic-ai/module-26-ai-agents/section-26.5.html`)
  - 19 sub-headings; reasons: top heading token 'production' covers only 11% of 19 headings; 8 distinct recurring themes; first_para keywords overlap with only 4% of heading tokens; (title signals broad-scope coverage, penalty applied)
  - top heading themes (token, freq): production (2), request (2), rate (2), limiting (2), circuit (2), breakers (2)
  - first 6 headings: _Prerequisites; The Eight Components of a Production Agent; Reference Architecture: Request Flow; Tool Router and Execution Sandbox; Production Concerns: Rate Limiting, Circuit Breakers, and Graceful Degradation; Rate Limiting_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§41.5 External Reading and Communities** (`part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.5.html`)
  - 16 sub-headings; reasons: top heading token 'current' covers only 12% of 16 headings; first_para keywords overlap with only 0% of heading tokens
  - top heading themes (token, freq): current (2), research (2), lists (2), reading (2), foundational (1), papers (1)
  - first 6 headings: _Foundational papers and textbooks; Academic venues for current research; Vendor engineering blogs; Community hubs and Q&amp;A; The voice-agent subculture; Curated resource lists_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§3.1 How a Transformer Computes One Token** (`part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html`)
  - 25 sub-headings; reasons: top heading token 'information' covers only 12% of 25 headings; 6 distinct recurring themes; (title signals broad-scope coverage, penalty applied)
  - top heading themes (token, freq): information (3), positional (3), encoding (3), attention (3), forward (2), residual (2)
  - first 6 headings: _Prerequisites; The Paper That Changed Everything; Information Theory: The Language of Learning; High-Level Architecture; Input Representation and Positional Encoding; Token Embeddings_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§3.2 Build a Transformer from Scratch** (`part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html`)
  - 23 sub-headings; reasons: top heading token 'training' covers only 13% of 23 headings
  - top heading themes (token, freq): training (3), complete (2), implementation (2), data (2), prerequisites (1), building (1)
  - first 6 headings: _Prerequisites; What We Are Building; The Complete Implementation; Imports and Configuration; Causal Self-Attention; Feed-Forward Network_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§3.4 GPU Fundamentals & Systems** (`part-1-llm-building-blocks/module-03-transformer-architecture/section-3.6.html`)
  - 21 sub-headings; reasons: top heading token 'gpu' covers only 14% of 21 headings; 7 distinct recurring themes; (title signals broad-scope coverage, penalty applied)
  - top heading themes (token, freq): gpu (3), memory (3), architecture (2), bound (2), softmax (2), triton (2)
  - first 6 headings: _Prerequisites; Why GPU Architecture Matters; GPU Architecture Overview; Streaming Multiprocessors (SMs); Memory Hierarchy; Compute-Bound vs. Memory-Bound Operations_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§70.4 Post-Launch Product Monitoring and Iteration** (`part-14-designing-llm-agent-products/module-70-shipping-products/section-70.4.html`)
  - 21 sub-headings; reasons: top heading token 'drift' covers only 14% of 21 headings
  - top heading themes (token, freq): drift (3), production (2), continuous (2), monitoring (2), prerequisites (1), evaluation (1)
  - first 6 headings: _Prerequisites; Production Evaluation Is Continuous, Not One-Shot; Drift Detection: Knowing When Quality Degrades; Types of Drift in LLM Products; Automated Drift Checks; Cost Monitoring and Optimization_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§43.1 RAG Evaluation: Ragas, BEIR, Faithfulness and Groundedness** (`part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.1.html`)
  - 21 sub-headings; reasons: 8 distinct recurring themes; first_para keywords overlap with only 0% of heading tokens
  - top heading themes (token, freq): metrics (4), end (4), faithfulness (4), groundedness (4), evaluation (4), rag (4)
  - first 6 headings: _Prerequisites; The Three-Layer Eval Cake; Retrieval Metrics; Generation Metrics; End-to-End Metrics; Faithfulness vs Groundedness (Commonly Confused)_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§52.1 Bias, Fairness, and Ethics** (`part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html`)
  - 20 sub-headings; reasons: 8 distinct recurring themes; first_para keywords overlap with only 5% of heading tokens
  - top heading themes (token, freq): bias (3), cultural (3), prerequisites (2), toxicity (2), cross (2), pluralistic (2)
  - first 6 headings: _Prerequisites; Sources of Bias; Measuring Bias; Toxicity and Stereotype Measurement; Model Cards and Datasheets; Cross-Cultural NLP and Pluralistic Alignment_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§2.1 Why RNNs Couldn't Scale to Modern LLMs** (`part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html`)
  - 19 sub-headings; reasons: 8 distinct recurring themes; first_para keywords overlap with only 5% of heading tokens
  - top heading themes (token, freq): sequence (3), problem (3), rnn (3), cell (3), gradient (2), lstm (2)
  - first 6 headings: _Prerequisites; The Sequence Modeling Problem; RNN Fundamentals; The Vanilla RNN Cell; The Vanishing and Exploding Gradient Problem; LSTM and GRU: Gated Recurrent Networks_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§1.3 Word Embeddings: Word2Vec, GloVe & FastText** (`part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html`)
  - 17 sub-headings; reasons: top heading token 'word2vec' covers only 12% of 17 headings
  - top heading themes (token, freq): word2vec (2), training (2), similarity (2), word (2), embeddings (2), prerequisites (1)
  - first 6 headings: _Prerequisites; The Distributional Hypothesis; Word2Vec: How It Works; The Architecture (It Is Surprisingly Simple); Negative Sampling: Making Training Tractable; Training Word2Vec from Scratch_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§12.2 Chain-of-Thought & Reasoning Techniques** (`part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html`)
  - 17 sub-headings; reasons: 8 distinct recurring themes; first_para keywords overlap with only 4% of heading tokens
  - top heading themes (token, freq): thought (3), reasoning (3), chain (2), prompting (2), shot (2), cot (2)
  - first 6 headings: _Prerequisites; Chain-of-Thought Prompting; Zero-Shot CoT; Few-Shot CoT; Self-Consistency; Implementation_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§61.5 External Reading and Communities** (`part-12-llm-systems-at-scale/module-61-scale-tools/section-61.5.html`)
  - 14 sub-headings; reasons: top heading token 'papers' covers only 14% of 14 headings
  - top heading themes (token, freq): papers (2), technical (2), reading (2), community (2), reports (2), conferences (1)
  - first 6 headings: _Conferences and academic venues; Foundational papers to read; Engineering blogs and technical writeups; Communities and forums; Newsletters and podcasts; Books on LLM systems and scale_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§64.1 Workflow Orchestration and Durable Execution** (`part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html`)
  - 14 sub-headings; reasons: top heading token 'agents' covers only 14% of 14 headings
  - top heading themes (token, freq): agents (2), durable (2), level (2), retry (2), prerequisites (1), llm (1)
  - first 6 headings: _Prerequisites; Why LLM Agents Need Durable Execution; Temporal: Infrastructure-Level Durability; The OpenAI Agents SDK Integration; Inngest: Event-Driven Durable Functions; LangGraph Persistence: Application-Level Checkpointing_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§26.3 Reasoning Models as Agent Backbones** (`part-6-agentic-ai/module-26-ai-agents/section-26.3.html`)
  - 14 sub-headings; reasons: top heading token 'reasoning' covers only 14% of 14 headings
  - top heading themes (token, freq): reasoning (2), thinking (2), practice (2), prerequisites (1), model (1), revolution (1)
  - first 6 headings: _Prerequisites; The Reasoning Model Revolution; Extended Thinking in Practice; Thinking Budgets and Cost Management; Architectural Patterns for Reasoning Agents; Lab: Build a ReAct Agent_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§28.1 Framework Landscape** (`part-6-agentic-ai/module-28-multi-agent-systems/section-28.1.html`)
  - 14 sub-headings; reasons: top heading token 'framework' covers only 14% of 14 headings; 6 distinct recurring themes; (title signals broad-scope coverage, penalty applied)
  - top heading themes (token, freq): framework (2), same (2), agent (2), three (2), frameworks (2), setup (2)
  - first 6 headings: _Prerequisites; The Framework Landscape in 2026; The Same Agent in Three Frameworks; Lab: Build the Same Agent in Three Frameworks; Framework Selection Guide; Objective_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§28.4 Testing Multi-Agent Systems** (`part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html`)
  - 14 sub-headings; reasons: top heading token 'testing' covers only 14% of 14 headings
  - top heading themes (token, freq): testing (2), multi (2), agent (2), chaos (2), setup (2), prerequisites (1)
  - first 6 headings: _Prerequisites; The Testing Challenge; Contract Testing for Multi-Agent Systems; Chaos Engineering for Agents; Lab: Chaos Test a Multi-Agent Pipeline; Objective_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§23.5 Scene Relighting & 3D Editing** (`part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.5.html`)
  - 11 sub-headings; reasons: 6 distinct recurring themes; first_para keywords overlap with only 0% of heading tokens
  - top heading themes (token, freq): inverse (2), rendering (2), relighting (2), language (2), grounded (2), editing (2)
  - first 6 headings: _Inverse Rendering Fundamentals; IC-Light: The Pretrained Relighting Prior; Relightable 3D Gaussians (2024); Language-Grounded 3D Editing; Failure Modes and the Consistency Tax; Composition and Export_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§56.5 External Reading and Communities** (`part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.5.html`)
  - 10 sub-headings; reasons: top heading token 'foundational' covers only 10% of 10 headings
  - top heading themes (token, freq): foundational (1), papers (1), canonical (1), works (1), conferences (1), academic (1)
  - first 6 headings: _Foundational papers and canonical works; Conferences and academic venues; Standards and governance frameworks; Organizations, think tanks, and civil society; Blogs, newsletters, and podcasts; Practitioner communities_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§24.13 Sim-to-Real Gap** (`part-5-multimodal-llms/module-24-vla-models/section-24.13.html`)
  - 10 sub-headings; reasons: top heading token 'anatomy' covers only 10% of 10 headings
  - top heading themes (token, freq): anatomy (1), gap (1), domain (1), randomization (1), workhorse (1), system (1)
  - first 6 headings: _Anatomy of the Gap; Domain Randomization, the Workhorse; System Identification; Real-World Fine-Tuning; Hardware-in-the-Loop Validation; Deployment Patterns in 2026_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§24.5 Comparing VLA Models** (`part-5-multimodal-llms/module-24-vla-models/section-24.5.html`)
  - 10 sub-headings; reasons: top heading token 'capability' covers only 10% of 10 headings
  - top heading themes (token, freq): capability (1), matrix (1), success (1), rates (1), public (1), benchmarks (1)
  - first 6 headings: _The Capability Matrix; Success Rates on the Public Benchmarks; Decision Tree: Which VLA Do You Pick; The Action Vocabulary Axis; Licensing and the Open-Weights Frontier; What Changed in the Last 12 Months_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

- **§24.6 VLA Limitations** (`part-5-multimodal-llms/module-24-vla-models/section-24.6.html`)
  - 10 sub-headings; reasons: top heading token 'sim' covers only 10% of 10 headings
  - top heading themes (token, freq): sim (1), real (1), gap (1), dexterity (1), ceiling (1), safety (1)
  - first 6 headings: _The Sim-to-Real Gap; The Dexterity Ceiling; The Safety Story Nobody Has Solved; The Language-Understanding Cliff; The Evaluation Problem; When VLAs Are the Wrong Tool_
  - action: split into focused sub-sections, or rescope title + big_picture to honestly cover what is taught.

## Under-content sections

_Pages whose content size is below threshold or missing structural elements._

### Severe (3+ flags) (17)

- **§71.3 Datasets & Benchmarks** (`part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.3.html`): wc 287, h2/3 2, callouts 0; flags: wc=287, h2/3=2, no big_picture, callouts=0
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§71.4 Models** (`part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.4.html`): wc 311, h2/3 2, callouts 0; flags: wc=311, h2/3=2, no big_picture, callouts=0
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§46.5 Multi-Judge Ensembles and Production Patterns** (`part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.5.html`): wc 394, h2/3 1, callouts 0; flags: wc=394, h2/3=1, no big_picture, callouts=0
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§46.3 Debiasing Techniques: Position, Length, and Verbosity** (`part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.3.html`): wc 492, h2/3 1, callouts 0; flags: wc=492, h2/3=1, no big_picture, callouts=0
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§71.5 External Reading & Communities** (`part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.5.html`): wc 154, h2/3 3, callouts 0; flags: wc=154, no big_picture, callouts=0
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§79.5 External Reading & Communities** (`part-14-applications-of-llms-across-industries/module-74-tools-of-the-trade/section-74.5.html`): wc 183, h2/3 2, callouts 1; flags: wc=183, h2/3=2, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§79.3 Datasets & Benchmarks** (`part-14-applications-of-llms-across-industries/module-74-tools-of-the-trade/section-74.3.html`): wc 188, h2/3 3, callouts 0; flags: wc=188, no big_picture, callouts=0
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§46.4 Training Judge Models** (`part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.4.html`): wc 256, h2/3 1, callouts 1; flags: wc=256, h2/3=1, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§79.4 Models** (`part-14-applications-of-llms-across-industries/module-74-tools-of-the-trade/section-74.4.html`): wc 301, h2/3 2, callouts 2; flags: wc=301, h2/3=2, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§34.1 The Information Extraction Landscape** (`part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html`): wc 465, h2/3 2, callouts 1; flags: wc=465, h2/3=2, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§45.4 Models** (`part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.4.html`): wc 469, h2/3 2, callouts 1; flags: wc=469, h2/3=2, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§46.2 Judge Reliability and Common Biases** (`part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html`): wc 603, h2/3 1, callouts 2; flags: wc=603, h2/3=1, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§46.1 Why LLM-as-Judge Matters** (`part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html`): wc 688, h2/3 1, callouts 4; flags: wc=688, h2/3=1, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§51.1 Platforms** (`part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.1.html`): wc 797, h2/3 4, callouts 0; flags: wc=797, no big_picture, callouts=0
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§34.3 Hybrid IE Architectures with LLMs** (`part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html`): wc 844, h2/3 2, callouts 1; flags: wc=844, h2/3=2, no big_picture
  - action: EXPAND with at least one worked example and 2-3 sub-headings, or fold into adjacent section.
- **§51.2 Libraries & Frameworks** (`part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.2.html`): wc 887, h2/3 4, callouts 0; flags: wc=887, no big_picture, callouts=0
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§79.2 Libraries & Frameworks** (`part-14-applications-of-llms-across-industries/module-74-tools-of-the-trade/section-74.2.html`): wc 1036, h2/3 4, callouts 0; flags: wc=1036, no big_picture, callouts=0
  - action: ADD missing pieces (big_picture, at least one callout, more headings).

### Moderate (2 flags) (33)

- **§45.5 External Reading & Communities** (`part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.5.html`): wc 149, h2/3 3, callouts 1; flags: wc=149, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§51.5 External Reading & Communities** (`part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.5.html`): wc 200, h2/3 4, callouts 1; flags: wc=200, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§14.5 External Reading & Communities** (`part-3-working-with-llms/module-14-tools-of-the-trade/section-14.5.html`): wc 360, h2/3 4, callouts 1; flags: wc=360, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§30.5 External Reading & Communities** (`part-6-agentic-ai/module-30-tools-of-the-trade/section-30.6.html`): wc 363, h2/3 4, callouts 1; flags: wc=363, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§19.5 External Reading & Communities** (`part-4-training-adaptation/module-19-tools-of-the-trade/section-19.6.html`): wc 367, h2/3 3, callouts 1; flags: wc=367, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§34.4 Production IE Deployment Patterns** (`part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.4.html`): wc 409, h2/3 4, callouts 2; flags: wc=409, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§25.5 External Reading & Communities** (`part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.5.html`): wc 478, h2/3 3, callouts 2; flags: wc=478, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **App A.2 Probability and Statistics** (`appendices/appendix-a-mathematical-foundations/section-a.2.html`): wc 492, h2/3 4, callouts 1; flags: wc=492, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§10.9 External Reading & Communities** (`part-2-understanding-llms/module-10-interpretability/section-10.11.html`): wc 492, h2/3 4, callouts 2; flags: wc=492, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§51.4 Models** (`part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.4.html`): wc 573, h2/3 3, callouts 1; flags: wc=573, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **App A.3 Calculus for Machine Learning** (`appendices/appendix-a-mathematical-foundations/section-a.3.html`): wc 582, h2/3 4, callouts 1; flags: wc=582, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§14.3 Datasets & Benchmarks** (`part-3-working-with-llms/module-14-tools-of-the-trade/section-14.3.html`): wc 698, h2/3 5, callouts 3; flags: wc=698, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§5.5 External Reading & Communities** (`part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.6.html`): wc 736, h2/3 4, callouts 2; flags: wc=736, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **App A.4 Information Theory** (`appendices/appendix-a-mathematical-foundations/section-a.4.html`): wc 741, h2/3 4, callouts 2; flags: wc=741, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§83.5 External Reading & Communities** (`part-15-llm-agentic-ai-research-frontiers/module-78-tools-of-the-trade/section-78.5.html`): wc 777, h2/3 1, callouts 6; flags: wc=777, h2/3=1
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§10.7 Datasets & Benchmarks** (`part-2-understanding-llms/module-10-interpretability/section-10.9.html`): wc 777, h2/3 4, callouts 3; flags: wc=777, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§51.3 Datasets & Benchmarks** (`part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.3.html`): wc 782, h2/3 4, callouts 1; flags: wc=782, no big_picture
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§5.4 Models** (`part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.5.html`): wc 836, h2/3 4, callouts 2; flags: wc=836, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§10.5 Platforms** (`part-2-understanding-llms/module-10-interpretability/section-10.6.html`): wc 875, h2/3 5, callouts 3; flags: wc=875, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **App A.1 Linear Algebra Essentials** (`appendices/appendix-a-mathematical-foundations/section-a.1.html`): wc 887, h2/3 4, callouts 2; flags: wc=887, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§5.3 Datasets & Benchmarks** (`part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.4.html`): wc 910, h2/3 5, callouts 3; flags: wc=910, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§45.3 Datasets & Benchmarks** (`part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.3.html`): wc 957, h2/3 4, callouts 1; flags: wc=957, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§79.1 Platforms** (`part-14-applications-of-llms-across-industries/module-74-tools-of-the-trade/section-74.1.html`): wc 993, h2/3 5, callouts 2; flags: wc=993, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§42.12 Classical ML Evaluation Metrics** (`part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html`): wc 1000, h2/3 7, callouts 5; flags: wc=1000, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§30.3 Datasets & Benchmarks** (`part-6-agentic-ai/module-30-tools-of-the-trade/section-30.4.html`): wc 1022, h2/3 4, callouts 1; flags: wc=1022, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§14.4 Models** (`part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html`): wc 1114, h2/3 5, callouts 4; flags: wc=1114, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§30.4 Models** (`part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html`): wc 1162, h2/3 4, callouts 2; flags: wc=1162, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§25.2 Libraries & Frameworks** (`part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.2.html`): wc 1188, h2/3 3, callouts 2; flags: wc=1188, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§25.4 Models** (`part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.4.html`): wc 1198, h2/3 4, callouts 3; flags: wc=1198, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§25.3 Datasets & Benchmarks** (`part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.3.html`): wc 1216, h2/3 4, callouts 2; flags: wc=1216, no big_picture
  - action: ADD missing pieces (big_picture, at least one callout, more headings).

### Mild (1 flag) (116)

- **App A.5 Connecting the Pieces** (`appendices/appendix-a-mathematical-foundations/section-a.5.html`): wc 426, h2/3 4, callouts 1; flags: wc=426
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **Capstone: Capstone Project: End-to-End LLM System** (`capstone/index.html`): wc 642, h2/3 6, callouts 2; flags: wc=642
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§75.5 Education LLM Vendors and Further Reading** (`part-14-applications-of-llms-across-industries/module-70-education-llms/section-70.5.html`): wc 740, h2/3 4, callouts 2; flags: wc=740
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§83.3 Datasets & Benchmarks** (`part-15-llm-agentic-ai-research-frontiers/module-78-tools-of-the-trade/section-78.3.html`): wc 750, h2/3 3, callouts 6; flags: wc=750
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§75.3 Regulatory and Policy Framework for Education LLMs** (`part-14-applications-of-llms-across-industries/module-70-education-llms/section-70.3.html`): wc 759, h2/3 7, callouts 2; flags: wc=759
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§76.5 Cybersecurity LLM Vendors and Further Reading** (`part-14-applications-of-llms-across-industries/module-71-cybersecurity-llms/section-71.5.html`): wc 768, h2/3 4, callouts 2; flags: wc=768
  - action: EXPAND to ~3500 words or MERGE into a sibling section.
- **§74.5 Healthcare LLM Vendors and Further Reading** (`part-14-applications-of-llms-across-industries/module-69-healthcare-llms/section-69.5.html`): wc 807, h2/3 4, callouts 2; flags: wc=807
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§73.5 Finance LLM Vendors and Further Reading** (`part-14-applications-of-llms-across-industries/module-68-finance-llms/section-68.5.html`): wc 814, h2/3 4, callouts 2; flags: wc=814
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§72.5 Legal LLM Vendors and Further Reading** (`part-14-applications-of-llms-across-industries/module-67-legal-llms/section-67.5.html`): wc 829, h2/3 4, callouts 2; flags: wc=829
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§77.4 Public-Sector Grounded Assistant Architecture** (`part-14-applications-of-llms-across-industries/module-72-government-llms/section-72.4.html`): wc 831, h2/3 3, callouts 2; flags: wc=831
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§76.2 Offensive (Red Team) Use Cases** (`part-14-applications-of-llms-across-industries/module-71-cybersecurity-llms/section-71.2.html`): wc 850, h2/3 6, callouts 2; flags: wc=850
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§57.2 Enterprise Integration Patterns for LLM Systems** (`part-12-llm-systems-at-scale/module-57-compute-planning/section-57.2.html`): wc 875, h2/3 4, callouts 4; flags: wc=875
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§74.3 Regulatory Framework for Healthcare LLMs** (`part-14-applications-of-llms-across-industries/module-69-healthcare-llms/section-69.3.html`): wc 887, h2/3 8, callouts 2; flags: wc=887
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§69.1 ROI Measurement & Value Attribution** (`part-14-designing-llm-agent-products/module-69-llm-economics/section-69.1.html`): wc 899, h2/3 4, callouts 4; flags: wc=899
  - action: ADD missing pieces (big_picture, at least one callout, more headings).
- **§83.1 Platforms** (`part-15-llm-agentic-ai-research-frontiers/module-78-tools-of-the-trade/section-78.1.html`): wc 899, h2/3 4, callouts 4; flags: wc=899
  - action: ADD missing pieces (big_picture, at least one callout, more headings).

## Over-content sections

- **§19.2 Libraries & Frameworks** (`part-4-training-adaptation/module-19-tools-of-the-trade/section-19.2.html`): 317 KB body, 14098 words, 13 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.
- **§37.3 Memory & Context Management** (`part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html`): 203 KB body, 8190 words, 32 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.
- **§47.1 LLM Security Threats** (`part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html`): 188 KB body, 11607 words, 36 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.
- **§40.1 Voice Agents and Speech Interfaces** (`part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html`): 172 KB body, 9483 words, 32 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.
- **§45.2 Libraries & Frameworks** (`part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.2.html`): 171 KB body, 10646 words, 9 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.
- **§31.4 Document Processing & Chunking** (`part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.6.html`): 170 KB body, 7997 words, 36 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.
- **§10.4 Explaining Transformers** (`part-2-understanding-llms/module-10-interpretability/section-10.4.html`): 160 KB body, 8348 words, 24 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.
- **§0.3 PyTorch in 90 Minutes: Tensors to Training Loop** (`part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html`): 152 KB body, 8486 words, 38 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.
- **§13.5 Dataset Engineering for LLM Applications** (`part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html`): 152 KB body, 6080 words, 25 sub-headings
  - action: consider splitting at major H2 boundaries; or moving deep-dive material into an appendix/sidebar.

## Per-chapter health

| Chapter key | sections | avg KB | min KB | max KB | callouts/sec | bib coverage | image coverage |
|-------------|---------:|------:|------:|------:|------------:|------------:|--------------:|
| App appendix-a | 6 | 14.2 | 8.5 | 26.5 | 1.7 | 17% | 17% |
| Capstone:Capstone Project: End-to-End L | 1 | 9.0 | 9.0 | 9.0 | 2.0 | 0% | 100% |
| Capstone:Requirements & Deliverables | 1 | 27.6 | 27.6 | 27.6 | 5.0 | 0% | 0% |
| P1 ch0 | 4 | 97.0 | 68.9 | 152.3 | 22.2 | 100% | 100% |
| P1 ch1 | 7 | 70.6 | 42.1 | 105.2 | 19.6 | 100% | 100% |
| P1 ch2 | 3 | 102.0 | 77.1 | 139.5 | 21.7 | 100% | 100% |
| P1 ch3 | 5 | 99.4 | 60.8 | 135.6 | 20.6 | 100% | 100% |
| P1 ch4 | 4 | 95.8 | 85.7 | 106.2 | 22.2 | 100% | 100% |
| P1 ch5 | 5 | 42.0 | 9.5 | 125.7 | 8.8 | 20% | 20% |
| P10-llm-security-runtime-safety ch47 | 2 | 134.0 | 80.3 | 187.7 | 25.0 | 100% | 100% |
| P10-llm-security-runtime-safety ch48 | 5 | 24.3 | 20.0 | 28.9 | 6.8 | 100% | 80% |
| P10-llm-security-runtime-safety ch49 | 4 | 55.9 | 29.6 | 85.7 | 13.8 | 100% | 100% |
| P10-llm-security-runtime-safety ch50 | 2 | 87.3 | 57.5 | 117.1 | 16.5 | 100% | 100% |
| P10-llm-security-runtime-safety ch51 | 5 | 8.7 | 5.4 | 10.9 | 0.6 | 0% | 0% |
| P11-llm-ethics-trust-governance ch52 | 2 | 87.4 | 61.0 | 113.7 | 19.0 | 100% | 100% |
| P11-llm-ethics-trust-governance ch53 | 4 | 53.6 | 28.8 | 91.3 | 8.2 | 100% | 100% |
| P11-llm-ethics-trust-governance ch54 | 10 | 23.2 | 17.3 | 30.3 | 6.9 | 100% | 90% |
| P11-llm-ethics-trust-governance ch55 | 2 | 62.0 | 37.5 | 86.5 | 11.0 | 100% | 100% |
| P11-llm-ethics-trust-governance ch56 | 5 | 42.7 | 41.2 | 43.7 | 5.0 | 0% | 0% |
| P12-llm-systems-at-scale ch57 | 4 | 29.3 | 10.4 | 81.3 | 7.0 | 25% | 50% |
| P12-llm-systems-at-scale ch58 | 5 | 17.5 | 15.9 | 18.5 | 8.4 | 100% | 100% |
| P12-llm-systems-at-scale ch59 | 5 | 36.4 | 31.8 | 41.0 | 4.8 | 100% | 100% |
| P12-llm-systems-at-scale ch60 | 1 | 60.5 | 60.5 | 60.5 | 10.0 | 100% | 100% |
| P12-llm-systems-at-scale ch61 | 5 | 42.4 | 39.7 | 45.0 | 3.4 | 0% | 0% |
| P13-llmops-lifecycle ch62 | 2 | 72.1 | 66.8 | 77.4 | 23.0 | 100% | 100% |
| P13-llmops-lifecycle ch63 | 1 | 60.8 | 60.8 | 60.8 | 14.0 | 100% | 100% |
| P13-llmops-lifecycle ch64 | 1 | 85.7 | 85.7 | 85.7 | 13.0 | 100% | 100% |
| P13-llmops-lifecycle ch65 | 5 | 46.1 | 24.3 | 102.5 | 7.2 | 20% | 80% |
| P13-llmops-lifecycle ch66 | 1 | 123.3 | 123.3 | 123.3 | 12.0 | 100% | 100% |
| P14-designing-llm-agent-products ch67 | 15 | 45.4 | 13.0 | 77.7 | 9.3 | 87% | 80% |
| P14-designing-llm-agent-products ch68 | 6 | 22.5 | 12.3 | 54.5 | 7.2 | 50% | 50% |
| P14-designing-llm-agent-products ch69 | 3 | 12.1 | 9.8 | 15.9 | 4.7 | 0% | 67% |
| P14-designing-llm-agent-products ch70 | 6 | 70.7 | 40.7 | 110.5 | 12.0 | 100% | 100% |
| P14-designing-llm-agent-products ch71 | 5 | 17.9 | 4.4 | 48.0 | 2.6 | 0% | 0% |
| P15-applications-of-llms-across-industries ch72 | 5 | 11.6 | 9.7 | 14.2 | 3.8 | 20% | 0% |
| P15-applications-of-llms-across-industries ch73 | 5 | 10.9 | 10.1 | 11.8 | 3.0 | 20% | 0% |
| P15-applications-of-llms-across-industries ch74 | 5 | 11.0 | 9.6 | 12.1 | 3.0 | 20% | 0% |
| P15-applications-of-llms-across-industries ch75 | 5 | 10.4 | 8.5 | 11.3 | 3.0 | 20% | 0% |
| P15-applications-of-llms-across-industries ch76 | 5 | 10.3 | 9.0 | 11.6 | 3.0 | 20% | 0% |
| P15-applications-of-llms-across-industries ch77 | 5 | 11.3 | 9.4 | 12.8 | 3.4 | 20% | 0% |
| P15-applications-of-llms-across-industries ch78 | 10 | 22.0 | 10.6 | 92.0 | 5.4 | 50% | 10% |
| P15-applications-of-llms-across-industries ch79 | 5 | 8.2 | 5.1 | 12.1 | 1.0 | 0% | 0% |
| P16-llm-agentic-ai-research-frontiers ch80 | 4 | 58.1 | 33.9 | 95.2 | 14.5 | 100% | 100% |
| P16-llm-agentic-ai-research-frontiers ch81 | 4 | 46.8 | 39.0 | 50.7 | 8.2 | 100% | 100% |
| P16-llm-agentic-ai-research-frontiers ch82 | 5 | 16.4 | 14.8 | 18.4 | 7.6 | 100% | 80% |
| P16-llm-agentic-ai-research-frontiers ch83 | 5 | 11.9 | 10.9 | 13.8 | 5.4 | 100% | 20% |
| P2-understanding-llms ch10 | 9 | 79.5 | 8.2 | 160.4 | 14.2 | 44% | 67% |
| P2-understanding-llms ch6 | 9 | 66.7 | 40.9 | 89.4 | 15.3 | 89% | 89% |
| P2-understanding-llms ch7 | 3 | 90.2 | 82.2 | 100.0 | 16.7 | 100% | 100% |
| P2-understanding-llms ch8 | 6 | 64.7 | 44.3 | 108.4 | 13.8 | 100% | 100% |
| P2-understanding-llms ch9 | 7 | 90.0 | 57.2 | 123.7 | 16.6 | 100% | 100% |
| P3-working-with-llms ch11 | 4 | 94.4 | 82.9 | 118.6 | 21.8 | 100% | 100% |
| P3-working-with-llms ch12 | 5 | 73.9 | 48.1 | 92.9 | 19.2 | 100% | 100% |
| P3-working-with-llms ch13 | 5 | 95.1 | 62.3 | 152.1 | 18.0 | 100% | 100% |
| P3-working-with-llms ch14 | 5 | 32.8 | 7.1 | 91.2 | 5.8 | 20% | 40% |
| P4-training-adaptation ch15 | 7 | 86.5 | 57.7 | 135.2 | 16.0 | 100% | 100% |
| P4-training-adaptation ch16 | 7 | 80.6 | 58.7 | 117.4 | 17.7 | 100% | 100% |
| P4-training-adaptation ch17 | 7 | 82.3 | 57.3 | 134.4 | 18.4 | 100% | 100% |
| P4-training-adaptation ch18 | 5 | 81.3 | 37.4 | 122.6 | 20.2 | 100% | 100% |
| P4-training-adaptation ch19 | 5 | 119.1 | 6.9 | 316.8 | 14.2 | 0% | 60% |
| P5-multimodal-llms ch20 | 10 | 28.1 | 25.3 | 36.2 | 6.8 | 100% | 100% |
| P5-multimodal-llms ch21 | 4 | 31.2 | 29.4 | 33.7 | 6.0 | 100% | 100% |
| P5-multimodal-llms ch22 | 9 | 25.9 | 22.1 | 32.1 | 5.4 | 100% | 100% |
| P5-multimodal-llms ch23 | 5 | 24.6 | 22.1 | 26.7 | 6.6 | 100% | 100% |
| P5-multimodal-llms ch24 | 13 | 25.9 | 17.1 | 33.8 | 5.9 | 0% | 100% |
| P5-multimodal-llms ch25 | 5 | 13.0 | 8.2 | 15.6 | 2.2 | 0% | 0% |
| P6-agentic-ai ch26 | 6 | 64.2 | 33.5 | 102.0 | 14.5 | 100% | 100% |
| P6-agentic-ai ch27 | 6 | 43.8 | 25.7 | 100.3 | 12.5 | 100% | 100% |
| P6-agentic-ai ch28 | 4 | 41.9 | 33.3 | 51.1 | 13.5 | 100% | 100% |
| P6-agentic-ai ch29 | 4 | 44.7 | 27.2 | 72.6 | 12.5 | 100% | 100% |
| P6-agentic-ai ch30 | 5 | 28.0 | 6.5 | 95.5 | 4.0 | 20% | 20% |
| P7-retrieval-information-extraction-with-llms ch31 | 5 | 107.6 | 72.5 | 169.9 | 22.4 | 100% | 100% |
| P7-retrieval-information-extraction-with-llms ch32 | 4 | 83.7 | 45.3 | 127.3 | 21.5 | 100% | 100% |
| P7-retrieval-information-extraction-with-llms ch33 | 4 | 26.9 | 22.9 | 31.9 | 6.0 | 100% | 100% |
| P7-retrieval-information-extraction-with-llms ch34 | 5 | 28.0 | 10.4 | 54.9 | 3.4 | 0% | 0% |
| P7-retrieval-information-extraction-with-llms ch35 | 5 | 86.9 | 51.0 | 126.7 | 18.6 | 100% | 100% |
| P7-retrieval-information-extraction-with-llms ch36 | 5 | 38.2 | 34.4 | 44.6 | 4.2 | 0% | 0% |
| P8-conversational-ai-with-llms ch37 | 4 | 125.0 | 87.2 | 202.9 | 22.2 | 100% | 100% |
| P8-conversational-ai-with-llms ch40 | 5 | 57.2 | 23.5 | 172.4 | 12.6 | 100% | 100% |
| P8-conversational-ai-with-llms ch41 | 5 | 44.5 | 40.4 | 48.7 | 5.8 | 0% | 0% |
| P9-llm-evaluation-observability ch42 | 12 | 71.4 | 23.0 | 118.0 | 14.8 | 100% | 92% |
| P9-llm-evaluation-observability ch43 | 5 | 45.5 | 42.2 | 50.4 | 13.2 | 100% | 100% |
| P9-llm-evaluation-observability ch44 | 4 | 23.7 | 14.2 | 42.6 | 7.0 | 75% | 50% |
| P9-llm-evaluation-observability ch45 | 5 | 58.4 | 4.2 | 170.7 | 8.8 | 20% | 20% |
| P9-llm-evaluation-observability ch46 | 5 | 11.7 | 4.3 | 15.5 | 1.4 | 0% | 0% |

### Per-chapter missing pieces

- **App appendix-a** [small section in big chapter]: smallest section App A.5 Connecting the Pieces = 8.5KB vs max 26.5KB
- **part-1-llm-building-blocks ch5** [small section in big chapter]: smallest section §5.5 External Reading & Communities = 9.5KB vs max 125.7KB
- **part-10-llm-security-runtime-safety ch48** [section without image while siblings have]: §48.4 Policy DSLs and Constrained Decoding as Safety (others all illustrated)
- **part-10-llm-security-runtime-safety ch51** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-11-llm-ethics-trust-governance ch54** [section without image while siblings have]: §54.6 Model Cards: Anatomy, Examples, Use in Procurement (others all illustrated)
- **part-11-llm-ethics-trust-governance ch56** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-12-llm-systems-at-scale ch57** [small section in big chapter]: smallest section §57.2 Enterprise Integration Patterns for LLM Systems = 10.4KB vs max 81.3KB
- **part-12-llm-systems-at-scale ch57** [section without image while siblings have]: §57.2 Enterprise Integration Patterns for LLM Systems, §57.3 GPU Procurement Strategy and Spot-Reserved Economics (others all illustrated)
- **part-12-llm-systems-at-scale ch61** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-13-llmops-lifecycle ch65** [section without image while siblings have]: §65.4 Containerizing LLM Inference Servers (others all illustrated)
- **part-14-designing-llm-agent-products ch67** [small section in big chapter]: smallest section §67.2 Problem-Discovery Heuristics = 13.0KB vs max 77.7KB
- **part-14-designing-llm-agent-products ch68** [small section in big chapter]: smallest section §68.5 The Vertical-Slice Pattern in Depth = 12.3KB vs max 54.5KB
- **part-14-designing-llm-agent-products ch69** [no bibliography anywhere]: 3 sections, 0 with bibliography
- **part-14-designing-llm-agent-products ch69** [section without image while siblings have]: §69.3 Token Cost Forecasting and Multi-Vendor Arbitrage (others all illustrated)
- **part-14-designing-llm-agent-products ch71** [small section in big chapter]: smallest section §71.5 External Reading & Communities = 4.4KB vs max 48.0KB
- **part-14-designing-llm-agent-products ch71** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-14-applications-of-llms-across-industries ch78** [small section in big chapter]: smallest section §78.3 Manufacturing Regulatory and Standards Framework = 10.6KB vs max 92.0KB
- **part-14-applications-of-llms-across-industries ch79** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-15-llm-agentic-ai-research-frontiers ch82** [section without image while siblings have]: §82.5 What 2026 Settled (and What Remains Open) (others all illustrated)
- **part-2-understanding-llms ch10** [small section in big chapter]: smallest section §10.9 External Reading & Communities = 8.2KB vs max 160.4KB
- **part-2-understanding-llms ch6** [section without image while siblings have]: §6.9 Lab: Pretrain a Tiny Language Model (others all illustrated)
- **part-3-working-with-llms ch14** [small section in big chapter]: smallest section §14.5 External Reading & Communities = 7.1KB vs max 91.2KB
- **part-4-training-adaptation ch19** [small section in big chapter]: smallest section §19.5 External Reading & Communities = 6.9KB vs max 316.8KB
- **part-4-training-adaptation ch19** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-4-training-adaptation ch19** [section without image while siblings have]: §19.1 Platforms, §19.5 External Reading & Communities (others all illustrated)
- **part-5-multimodal-llms ch24** [no bibliography anywhere]: 13 sections, 0 with bibliography
- **part-5-multimodal-llms ch25** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-6-agentic-ai ch30** [small section in big chapter]: smallest section §30.5 External Reading & Communities = 6.5KB vs max 95.5KB
- **part-7-retrieval-information-extraction-with-llms ch34** [small section in big chapter]: smallest section §34.4 Production IE Deployment Patterns = 10.4KB vs max 54.9KB
- **part-7-retrieval-information-extraction-with-llms ch34** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-7-retrieval-information-extraction-with-llms ch36** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-8-conversational-ai-with-llms ch41** [no bibliography anywhere]: 5 sections, 0 with bibliography
- **part-9-llm-evaluation-observability ch42** [section without image while siblings have]: §42.12 Classical ML Evaluation Metrics (others all illustrated)
- **part-9-llm-evaluation-observability ch44** [small section in big chapter]: smallest section §44.5 Drift Detection in Production = 14.2KB vs max 42.6KB
- **part-9-llm-evaluation-observability ch44** [section without image while siblings have]: §44.5 Drift Detection in Production, §44.6 Model-Rotation Strategy (others all illustrated)
- **part-9-llm-evaluation-observability ch45** [small section in big chapter]: smallest section §45.5 External Reading & Communities = 4.2KB vs max 170.7KB
- **part-9-llm-evaluation-observability ch46** [small section in big chapter]: smallest section §46.4 Training Judge Models = 4.3KB vs max 15.5KB
- **part-9-llm-evaluation-observability ch46** [no bibliography anywhere]: 5 sections, 0 with bibliography

## Suggested follow-ups

Priority order for cleanup (rough one-PR-per-bullet sizing):

1. **Split §19.2** (Libraries & Frameworks, 317 KB / 14,098 words). Single
   biggest page in the book. Either split at H2 boundaries into §19.2a/b/c
   or relocate the long appendix-style content into a separate appendix.
2. **Industry chapters (Part 15, chs 72-77 + 79)** are uniformly thin (~10 KB,
   0% images, 20% or less bibliography coverage). Either accept that these
   are intentional 'short industry briefs' and document the design, or
   commission a unified expansion: at minimum a hero image, big_picture
   callout, and Further Reading section per chapter.
3. **Chapter 46 (LLM-as-Judge) needs structural work**: every section under
   the 'severe' threshold (no big_picture, 1 heading, no callouts). Either
   expand each section to median size or consolidate ch46 into 2-3 longer
   sections.
4. **Tools-of-the-Trade modules (§5, §14, §19, §25, §30, §45, §51, §71,
   §79, §83)** share a 5-section template (Platforms/Libraries/Datasets/
   Models/External Reading). Almost all have no big_picture and missing
   callouts. Decide between (a) consolidate into ONE 'Tools of the Trade'
   page per part, or (b) standardize the template with big_picture +
   1 callout per sub-section.
5. **13 chapters with 0% bibliography coverage** (listed in per-chapter
   missing pieces). Add a Further Reading callout to chapter-wrap section.
6. **Loss-of-focus sections §9.3, §9.7, §31.3** have 25 sub-headings each
   with no dominant theme. Consider splitting into 2-3 focused subsections
   or rescoping the title + big_picture to honestly cover the breadth.
7. **Non-template duplicates**: verify §10.8 ↔ §14.4 'Models' cross-ref
   exists; for §25.x intra-chapter overlap, either consolidate or add
   explicit cross-pointers.
8. **Validation loop**: regenerate `book_content_index.jsonl` after fixes,
   re-run `tmp_audit_wave28.py`, diff this report. Targets: substantive
   duplicates -> 0, severe under-content -> < 5, over-content -> 0.

Reference numbers: book median = 3037 words / 37.9 KB per section.

---

_Generated by `tmp_audit_wave28.py` from `book_content_index.jsonl` (554 records, 433 sections)._