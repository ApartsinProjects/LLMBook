# Chapter Plan: Module 07 - Modern LLM Landscape & Model Internals

## Scope

**What this chapter covers:** A comprehensive survey of the current LLM ecosystem across four dimensions: closed-source frontier models (GPT-4o, Claude, Gemini, and competitors); open-source and open-weight models with architectural deep dives (Llama, Mistral, DeepSeek V3, Qwen, Phi); the paradigm shift toward reasoning models and test-time compute scaling (o1/o3, DeepSeek-R1, process reward models, MCTS); and the multilingual and cross-cultural dimensions of modern LLMs (cross-lingual transfer, low-resource languages, cultural bias, vocabulary extension).

**What this chapter does NOT cover:** Pre-training fundamentals (Module 06), inference optimization and serving infrastructure (Module 08), fine-tuning and alignment methods (Modules 13, 16), prompt engineering techniques (Module 10), or RAG and retrieval systems (Module 19). While DeepSeek V3's MLA is discussed for its KV cache implications, the detailed treatment of KV cache optimization belongs to Module 08. RLHF/DPO training of reasoning models is mentioned in context but the full treatment is in Module 16.

**Target audience:** Students who understand the Transformer architecture (Module 04), decoding strategies (Module 05), and pre-training fundamentals (Module 06). This module bridges theoretical understanding with practical knowledge of which models exist, what they can do, and how they differ.

**Target length:** ~15,000 to 18,000 words across four sections.

---

## Learning Objectives

1. Compare frontier closed-source models on capability dimensions including reasoning, multimodality, context length, and pricing.
2. Explain the architectural innovations in DeepSeek V3 (MLA, FP8, auxiliary-loss-free MoE) and their impact on efficiency.
3. Articulate the difference between train-time and test-time compute scaling, and identify when each is preferable.
4. Implement best-of-N sampling with a reward model and explain process vs. outcome reward models.
5. Evaluate multilingual LLM capabilities and understand the challenges of cross-lingual transfer.
6. Navigate the Hugging Face ecosystem to discover, download, and run open-weight models locally.
7. Describe Monte Carlo Tree Search applied to language generation and the AlphaProof approach.

---

## Prerequisites

- Module 04 (Transformer Architecture): attention mechanism, multi-head attention, feed-forward layers
- Module 05 (Decoding Strategies): greedy, beam search, sampling methods, temperature, top-k/top-p
- Module 06 (Pre-training, Scaling Laws & Data Curation): pre-training objectives, scaling laws, data curation fundamentals, distributed training basics
- Basic familiarity with Python and the Hugging Face Transformers library

---

## Detailed Section Structure

### Section 7.1: Closed-Source Frontier Models

**Key concepts:**
- The frontier model landscape: major providers and their positioning
- OpenAI: GPT-4o (multimodal unification, native audio/image/text), o-series reasoning models (o1, o3, chain-of-thought at scale)
- Anthropic: Claude 3.5 Sonnet (Constitutional AI), Claude 4 family (Opus, Sonnet, Haiku; extended thinking, tool use, computer use)
- Google DeepMind: Gemini 2.0/2.5 (native multimodality, million-token context, thinking mode, deep research)
- Second-tier frontier models: xAI Grok (real-time data), Cohere Command R+ (RAG-optimized), Mistral Large (European alternative)
- Capability comparison across dimensions: reasoning, coding, multimodality, context length, latency
- Pricing tiers and rate limits: cost per million tokens, throughput limits
- Architectural insights from the outside: what we can infer from behavior, tokenizer analysis, context length patterns
- The convergence trend: frontier models becoming more similar over time

**Diagrams present:**
- SVG: Frontier model landscape (capability vs. cost positioning chart)

**Code examples:**
- Pricing comparison data structure (per-million-token costs for major providers)
- Tokenizer behavior inspection across providers

**Exercises:**
- Quiz: 5 questions on model selection criteria, pricing analysis, architectural inferences

**Tables:**
- Gemini model comparison (Flash, Pro, Ultra with context, modality, pricing)
- Capability dimensions matrix (reasoning, coding, multimodal, context, speed across major models)
- Pricing comparison (input/output per million tokens)

**Callouts:** Big Picture (opening), Note (pricing tiers), Key Insight (Claude's extended thinking), Warning (benchmark limitations)

---

### Section 7.2: Open-Source & Open-Weight Models

**Key concepts:**
- Open-source vs. open-weight distinction: licensing, reproducibility, training data access
- Meta Llama: Llama 3/3.1 (GQA, RoPE, 128K context), Llama 4 (MoE leap, native multimodal)
- Mistral and Mixtral: sliding window attention, MoE with 8 experts (2 active), Mistral's rapid iteration
- DeepSeek V3 architecture deep dive:
  - Multi-head Latent Attention (MLA): KV compression via low-rank projection, 10x cache reduction
  - FP8 mixed-precision training at 671B parameters: E4M3/E5M2, per-tensor dynamic scaling
  - Auxiliary-loss-free MoE load balancing: bias terms instead of penalty losses
  - Multi-Token Prediction (MTP): predict next N tokens simultaneously
- Qwen 2.5: Alibaba's competitive offering, strong multilingual and coding performance
- Microsoft Phi series: small but capable models via knowledge distillation and curated data
- Specialized open models: code (CodeLlama, StarCoder2), vision-language (LLaVA), speech (Whisper)
- The Hugging Face ecosystem: Model Hub, Transformers library, Datasets, Spaces, GGUF format

**Diagrams present:**
- SVG: DeepSeek V3 architecture overview (MLA, MoE routing, MTP heads)

**Code examples:**
- Loading and running an open-weight model with Hugging Face Transformers (pipeline, model card)
- Simplified MLA implementation concept (low-rank KV projection)
- FP8 quantization illustration (fine-grained scaling)
- Auxiliary-loss-free MoE load balancing concept (bias accumulation)
- Running models locally with Ollama (pull, run, API access)

**Exercises:**
- Quiz: 5 questions on open-weight vs. open-source, MLA mechanics, MoE routing, Hugging Face usage

**Tables:**
- Small model comparison (Phi-3/4, Gemma 2, Qwen 2.5 at 1B-14B with benchmarks)

**Callouts:** Big Picture (opening), Note (MoE economics), Key Insight (MLA's impact on inference cost)

---

### Section 7.3: Reasoning Models & Test-Time Compute

**Key concepts:**
- Inference-time scaling: the paradigm shift from train-time to test-time compute, new scaling curves
- Chain-of-thought at scale: o1/o3 (hidden reasoning traces, multi-step verification), DeepSeek-R1 (open reasoning, RL-trained chain-of-thought)
- Distilling reasoning into smaller models: R1-Zero emergent reasoning, distillation to 7B/14B models
- Process Reward Models (PRMs) vs. Outcome Reward Models (ORMs): step-level vs. final-answer supervision
- Training PRMs: Monte Carlo estimation of step correctness, human annotation approaches
- Best-of-N sampling: generate N candidates, score with reward model, return best; accuracy scaling with N
- Monte Carlo Tree Search for language: MCTS fundamentals adapted to text, selection/expansion/simulation/backpropagation
- LATS (Language Agent Tree Search): combining MCTS with LLM generation
- AlphaProof: mathematical reasoning via formal verification and MCTS
- Compute-optimal inference: when to allocate more test-time compute vs. using a larger model

**Diagrams present:**
- SVG: Train-time vs. test-time compute scaling curves
- SVG: PRM vs. ORM (step-level vs. outcome-level reward signals)
- SVG: MCTS tree for language generation (selection, expansion, simulation, backpropagation)

**Code examples:**
- Using a distilled reasoning model via Hugging Face
- Monte Carlo estimation for PRM training data generation
- Best-of-N sampling with reward model scoring (full implementation with generation, scoring, selection)
- Compute-optimal inference strategy selection (difficulty-based routing)

**Exercises:**
- Quiz: 5 questions on PRM vs. ORM tradeoffs, best-of-N scaling, MCTS mechanics, compute-optimal inference

**Lab exercise:** Implement best-of-N with a reward model; measure accuracy vs. compute on GSM8K math reasoning tasks

**Tables:**
- Compute-optimal inference strategies (method, compute cost, quality gain, best for)

**Callouts:** Big Picture (opening), Key Insight (inference-time scaling as new paradigm, compute-optimal inference), Note (emergent reasoning in R1-Zero, majority voting vs. reward model), Warning (practical consideration on latency)

---

### Section 7.4: Multilingual & Cross-Cultural LLMs

**Key concepts:**
- Multilingual pre-training: how one model learns many languages, shared representations across languages
- Cross-lingual transfer: zero-shot transfer via shared embedding spaces, universal grammar hypothesis in neural networks
- The curse of multilinguality: capacity dilution as more languages are added, language-specific vs. shared parameters
- Low-resource language challenges: data scarcity, tokenization inefficiency (more tokens per meaning unit), fertility rate disparities
- Solutions for low-resource languages: data augmentation, translation-based approaches, focused continued pre-training
- Cultural bias in LLMs: Western-centric defaults (names, values, common sense), measuring bias across cultures
- Multilingual evaluation benchmarks: MMLU-multilingual, MGSM, XL-Sum, FLORES, TyDi QA, GlobalBench
- Adapting English-centric models to new languages:
  - Vocabulary extension: adding language-specific tokens, initializing new embeddings
  - Continued pre-training: language-adaptive pre-training, catastrophic forgetting mitigation
  - Cross-lingual instruction tuning: translating instruction datasets, quality considerations
- Multilingual model families: Aya (Cohere for AI), BLOOM, mT5, Qwen, SeaLLM

**Diagrams present:**
- SVG: Cross-lingual transfer (shared representation space across languages)
- SVG: Multilingual benchmark performance by language resource level

**Code examples:**
- Tokenization inefficiency demonstration across languages (comparing token counts)
- Cultural bias demonstration (prompting same question in different cultural contexts)
- Vocabulary extension implementation (adding new tokens, initializing embeddings)
- Continued pre-training configuration for language adaptation

**Exercises:**
- Quiz: 5 questions on cross-lingual transfer, tokenization costs, cultural bias, vocabulary extension

**Tables:**
- Multilingual evaluation benchmarks (name, task, languages, metric)
- Multilingual model families (model, languages, size, approach, license)

**Callouts:** Big Picture (opening), Key Insight (curse of multilinguality), Warning (tokenization as hidden tax), Note (Aya initiative), Key Insight (vocabulary extension as practical technique)

---

## Areas for Improvement

### Content Gaps
1. **Section 7.1:** No discussion of model deprecation and version transitions. Students should understand that frontier models are moving targets, with models like GPT-4 Turbo being replaced by GPT-4o, and pricing changes happening frequently. A brief note on how to stay current would be practical.
2. **Section 7.1:** Missing coverage of Amazon Nova models and AWS Bedrock as a model marketplace. For enterprise students, this is an important option.
3. **Section 7.2:** The Gemma model family (Google's open-weight offering) receives no dedicated subsection despite being mentioned in the module index. A brief treatment of Gemma 2/3 would fill this gap.
4. **Section 7.2:** No discussion of model licensing nuances (Llama's community license vs. Apache 2.0 vs. proprietary). This is practically important for production deployments.
5. **Section 7.3:** The section lacks discussion of how reasoning models handle hallucination differently from standard models. Reasoning traces can make hallucinations more transparent (or more convincing). This is a key practical consideration.
6. **Section 7.3:** No coverage of the DeepSeek-R1 training pipeline in detail (the GRPO algorithm). A brief outline would help students understand how reasoning behavior emerges.
7. **Section 7.4:** No hands-on lab exercise. Unlike sections 7.2 and 7.3, this section is purely conceptual. A lab evaluating a multilingual model on a few languages, or demonstrating vocabulary extension, would strengthen it.
8. **Section 7.4:** Limited discussion of language-specific safety considerations. Content moderation in non-English languages is significantly harder and this gap has real-world implications.

### Weak Explanations
1. **Section 7.2:** The MLA explanation jumps from high-level concept to code without sufficient mathematical intuition. A worked example showing the dimensionality reduction (e.g., 128-dim KV projected to 16-dim latent) would make the 10x compression claim concrete.
2. **Section 7.3:** The MCTS section is dense and may be challenging for students without game-AI background. A simpler "MCTS for Tic-Tac-Toe" analogy before the language application would help.
3. **Section 7.4:** The vocabulary extension code example is thorough but lacks explanation of why random initialization with scaling works and what alternatives exist (e.g., initializing from subword averages).

### Structural Issues
1. **Section length imbalance:** Section 7.3 (949 lines) and 7.4 (888 lines) are significantly longer than 7.1 (674 lines). This creates uneven reading time across sections.
2. **Lab consistency:** Sections 7.2 and 7.3 have explicit lab exercises, but 7.1 and 7.4 do not. Adding at least a guided exploration exercise to 7.1 (API comparison) and 7.4 (multilingual evaluation) would improve consistency.
3. **Date sensitivity:** Section 7.1 contains pricing and capability data that will become outdated. Consider adding a "last updated" note and structuring the comparison tables for easy updates.

---

## Terminology Standards

| Term | Standard Usage | Avoid |
|------|---------------|-------|
| Open-source | "open-source" (with hyphen) for fully open (code + data + weights) | Conflating with "open-weight" |
| Open-weight | "open-weight" for models with downloadable weights but not full training recipe | "open-source" when data/code is not available |
| MoE / Mixture of Experts | "Mixture of Experts (MoE)" on first mention, then "MoE" | "mixture of experts" (capitalize as proper noun in model context) |
| MLA | "Multi-head Latent Attention (MLA)" on first mention | "multi-latent attention" or other variants |
| PRM / ORM | "Process Reward Model (PRM)" and "Outcome Reward Model (ORM)" on first mention | "step reward model" or "answer reward model" |
| Test-time compute | "test-time compute" or "inference-time compute" | "thinking time" (too informal for technical text) |
| Chain-of-thought / CoT | "chain-of-thought (CoT)" on first mention | "thinking traces" (use only as informal synonym) |
| MCTS | "Monte Carlo Tree Search (MCTS)" on first mention | "tree search" alone (too generic) |
| Frontier model | "frontier model" (lowercase) | "Frontier Model" (no capitalization needed) |
| Context window | "context window" or "context length" | "token limit" (imprecise) |

---

## Cross-References

### Upstream (prerequisites from earlier modules)
- Module 04 (Transformer Architecture): self-attention, multi-head attention, feed-forward layers (foundational for all architecture discussions)
- Module 05 (Decoding Strategies): autoregressive generation, sampling methods (used in best-of-N, speculative decoding connections)
- Module 06 (Pre-training): scaling laws (referenced in reasoning model compute tradeoffs), pre-training objectives (CLM, MTP referenced in DeepSeek V3), distributed training (FP8, MoE concepts)

### Downstream (modules that build on this one)
- Module 08 (Inference Optimization): MLA's KV cache compression connects to Section 10.2; MoE sparse activation connects to serving efficiency
- Module 09 (Working with LLM APIs): practical API access to frontier models surveyed in Section 7.1
- Module 10 (Prompt Engineering): chain-of-thought prompting builds on Section 7.3's reasoning model discussion
- Module 13 (Fine-Tuning): open-weight models from Section 7.2 are the starting points for fine-tuning
- Module 14 (PEFT): LoRA and QLoRA typically applied to open-weight models surveyed here
- Module 16 (Alignment): RLHF and DPO methods build on reward model concepts from Section 7.3
- Module 21 (AI Agents): reasoning and planning capabilities from Section 7.3 are the foundation for agent architectures
- Module 25 (Evaluation): multilingual benchmarks from Section 7.4 appear in evaluation methodology

---

## Estimated Total Word Count

| Section | Estimated Words |
|---------|----------------|
| 7.1 Closed-Source Frontier Models | ~3,800 |
| 7.2 Open-Source & Open-Weight Models | ~4,500 |
| 7.3 Reasoning Models & Test-Time Compute | ~5,200 |
| 7.4 Multilingual & Cross-Cultural LLMs | ~4,800 |
| **Total** | **~18,300** |

(Estimates based on HTML content line counts, excluding CSS/boilerplate, code blocks counted at reduced weight.)

---

## Narrative Arc

The module acts as a comprehensive field guide to the modern LLM ecosystem, moving from the known and accessible to the cutting-edge and global.

**The landscape from above (Section 7.1):** We begin with the models students are most likely to have encountered: ChatGPT, Claude, Gemini. This section grounds the module in practical reality. Students learn what these models can do, what they cost, and what architectural choices we can infer from their behavior. The key tension introduced is: these models are powerful but opaque.

**Opening the hood (Section 7.2):** The natural response to opacity is open-weight models. This section provides the detailed architectural understanding that closed-source models deny us. DeepSeek V3 serves as the centerpiece, a model that rivals frontier closed-source models while publishing its full architecture. Students gain hands-on experience downloading and running models locally, transforming LLMs from mysterious APIs into tangible software artifacts.

**The reasoning revolution (Section 7.3):** With a solid understanding of model architectures, we explore the paradigm shift toward reasoning models. This is the most technically demanding section, introducing a fundamentally different approach to improving AI: spending more compute at inference time rather than at training time. Students implement best-of-N sampling and learn the theoretical framework behind MCTS and reward-guided search.

**The global perspective (Section 7.4):** The module closes by widening the lens beyond English-language AI. This section challenges students to consider who these models serve and who they leave behind. The technical content (vocabulary extension, continued pre-training) is complemented by sociotechnical analysis of cultural bias and evaluation across languages.

The overall arc progresses from consumer-facing products to engineering internals to cutting-edge research to societal implications, giving students a complete understanding of where the field stands today.
