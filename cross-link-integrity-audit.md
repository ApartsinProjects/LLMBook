# Cross-Link Integrity Audit

Read-only audit of cross-link RELEVANCE, complementing `html-integrity-audit.md`
(which catches broken hrefs). This audit catches links where the destination is
reachable but the link text or surrounding claim no longer matches what is at
the destination (the v6-v9 reshuffles moved targets while leaving prose untouched).

Root: `E:/Projects/BookBlogsHome/LLMBook` | HTML pages scanned: 476

## Summary

- Cross-links checked (excluding nav / external / anchor / self / broken): 4905
- Resolvable + relevant: 4482
- P0 (mismatched topic): 133
- P1 (number drift, topic right): 290
- P2 (stale label, dropped resource): 0
- P3 (over-promise): 0

_Skipped: 3086 external, 20 anchor-only, 10 self, 3680 structural-nav, 366 broken hrefs._

## P0: Mismatched topic

Anchor text describes one topic; destination page is about something else.
These are the lies-by-omission: the reader clicks expecting X and lands on Y.

- (18 occurrences) Text: `Hugging Face`
  Destination: Fine-Tuning for Representation Learning
  Example: `part-12-frontiers/module-61-frontier-architectures/section-61.3.html:621` href=`../../part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.5.html`
  Other: `part-2-understanding-llms/module-10-inference-optimization/section-10.1.html:92`, `part-2-understanding-llms/module-10-inference-optimization/section-10.3.html:203`, `part-2-understanding-llms/module-10-inference-optimization/section-10.4.html:260`, `part-2-understanding-llms/module-11-interpretability/section-11.2.html:590`, `part-2-understanding-llms/module-11-interpretability/section-11.3.html:359` (...)

- (15 occurrences) Text: `Hugging Face`
  Destination: Structured Output & Tool Integration
  Example: `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html:374` href=`../../part-3-working-with-llms/module-13-llm-apis/section-13.2.html`
  Other: `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html:192`, `part-1-foundations/module-03-sequence-models-attention/section-3.3.html:456`, `part-1-foundations/module-04-transformer-architecture/section-4.2.html:744`, `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html:250`, `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.5.html:243` (...)

- (12 occurrences) Text: `structured output`
  Destination: API Engineering Best Practices
  Example: `part-11-applications-across-industries/module-52-finance-llms/section-52.7.html:308` href=`../../part-3-working-with-llms/module-13-llm-apis/section-13.3.html`
  Other: `part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html:42`, `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.4.html:42`, `part-2-understanding-llms/module-10-inference-optimization/section-10.4.html:257`, `part-3-working-with-llms/module-14-prompt-engineering/section-14.4.html:39`, `part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.2.html:42` (...)

- (9 occurrences) Text: `catastrophic forgetting`
  Destination: Supervised Fine-Tuning (SFT)
  Example: `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html:293` href=`../../part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.3.html`
  Other: `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.2.html:469`, `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.4.html:326`, `part-2-understanding-llms/module-11-interpretability/section-11.3.html:466`, `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.2.html:465`, `part-4-training-adapting/module-19-peft/section-19.1.html:40` (...)

- (6 occurrences) Text: `learning rate`
  Destination: Supervised Fine-Tuning (SFT)
  Example: `part-12-frontiers/module-61-frontier-architectures/section-61.2.html:64` href=`../../part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.3.html`
  Other: `part-4-training-adapting/module-19-peft/section-19.2.html:410`, `part-4-training-adapting/module-19-peft/section-19.5.html:484`, `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.1.html:440`, `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.1.html:653`, `part-5-retrieval-conversation/module-23-rag/section-23.5.html:471`

- (6 occurrences) Text: `open-weight models`
  Destination: Closed-Source Frontier Models
  Example: `part-10-idea-to-product/module-46-compute-planning/section-46.3.html:274` href=`../../part-2-understanding-llms/module-08-modern-llm-landscape/section-8.1.html`
  Other: `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.2.html:402`, `part-4-training-adapting/module-17-synthetic-data/section-17.1.html:38`, `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.3.html:381`, `part-8-evaluation-production/module-34-evaluation-observability/section-34.7.html:409`, `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html:459`

- (4 occurrences) Text: `rate limiting`
  Destination: Frontend & User Interfaces
  Example: `part-4-training-adapting/module-17-synthetic-data/section-17.3.html:527` href=`../../part-8-evaluation-production/module-35-production-engineering/section-35.2.html`
  Other: `part-5-retrieval-conversation/module-23-rag/section-23.6.html:832`, `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html:151`, `part-8-evaluation-production/module-34-evaluation-observability/section-34.3.html:163`

- (3 occurrences) Text: `Evol-Instruct`
  Destination: LLM Evaluation Fundamentals
  Example: `part-12-frontiers/module-61-frontier-architectures/section-61.2.html:82` href=`../../part-8-evaluation-production/module-34-evaluation-observability/section-34.1.html`
  Other: `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.3.html:301`, `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.2.html:59`

- (3 occurrences) Text: `Hugging Face`
  Destination: HuggingFace: Transformers, Datasets, and Hub
  Example: `appendices/appendix-b-ml-essentials/section-b.4.html:142` href=`../appendix-c-huggingface-ecosystem/index.html`
  Other: `appendices/appendix-h-python-for-llm/section-h.4.html:34`, `capstone/index.html:39`

- (3 occurrences) Text: `knowledge graph`
  Destination: Deep Research & Agentic RAG
  Example: `part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.5.html:257` href=`../../part-5-retrieval-conversation/module-23-rag/section-23.4.html`
  Other: `part-5-retrieval-conversation/module-24-conversational-ai/section-24.3.html:694`, `part-6-agentic-ai/module-27-tool-use-protocols/section-27.5.html:128`

- (2 occurrences) Text: `Open-weight models`
  Destination: Closed-Source Frontier Models
  Example: `part-4-training-adapting/module-19-peft/section-19.5.html:218` href=`../../part-2-understanding-llms/module-08-modern-llm-landscape/section-8.1.html`
  Other: `part-7-multimodal-generation/module-31-multimodal/section-31.4.html:530`

- (2 occurrences) Text: `Section 19.5: Knowledge Distillation`
  Destination: Parameter-Efficient Fine-Tuning (PEFT)
  Example: `part-4-training-adapting/module-19-peft/section-19.3.html:656` href=`../module-19-peft/index.html`
  Other: `part-4-training-adapting/module-19-peft/section-19.4.html:569`

- (2 occurrences) Text: `bag-of-words`
  Destination: Introduction to NLP & the LLM Revolution
  Example: `part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.2.html:49` href=`../../part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html`
  Other: `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.4.html:809`

- (2 occurrences) Text: `context window`
  Destination: Build a Transformer from Scratch
  Example: `part-5-retrieval-conversation/module-23-rag/index.html:78` href=`../../part-1-foundations/module-04-transformer-architecture/section-4.2.html`
  Other: `part-5-retrieval-conversation/module-23-rag/section-23.5.html:47`

- (2 occurrences) Text: `emergent behavior`
  Destination: Distributed Training at Scale
  Example: `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.4.html:454` href=`../../part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.6.html`
  Other: `part-6-agentic-ai/module-28-multi-agent-systems/section-28.6.html:45`

- (2 occurrences) Text: `open-weight model`
  Destination: Closed-Source Frontier Models
  Example: `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.4.html:365` href=`../../part-2-understanding-llms/module-08-modern-llm-landscape/section-8.1.html`
  Other: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.6.html:38`

- (2 occurrences) Text: `red teaming`
  Destination: Bias, Fairness & Ethics
  Example: `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.3.html:522` href=`../../part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html`
  Other: `part-8-evaluation-production/module-34-evaluation-observability/section-34.3.html:51`

- (2 occurrences) Text: `structured outputs`
  Destination: API Engineering Best Practices
  Example: `part-2-understanding-llms/module-10-inference-optimization/section-10.3.html:416` href=`../../part-3-working-with-llms/module-13-llm-apis/section-13.3.html`
  Other: `part-7-multimodal-generation/module-31-multimodal/section-31.3.html:233`

- Text: `10.3 Hardware Landscape`
  Destination: Speculative Decoding
  Example: `appendices/appendix-g-problem-solution-key/index.html:598` href=`../../part-2-understanding-llms/module-10-inference-optimization/section-10.3.html`

- Text: `Catastrophic forgetting`
  Destination: Supervised Fine-Tuning (SFT)
  Example: `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.1.html:209` href=`../module-18-fine-tuning-fundamentals/section-18.3.html`

- Text: `Chapter 11: Interpretability and Mechanistic Understanding`
  Destination: Building Conversational AI with LLMs and Agents
  Example: `part-2-understanding-llms/module-10-inference-optimization/section-10.7.html:676` href=`../../index.html`

- Text: `Error Recovery, Resilience and Graceful Degradation`
  Destination: Post-Launch Monitoring and Iteration
  Example: `part-10-idea-to-product/module-48-shipping-deploying/section-48.5.html:214` href=`section-48.4.html`

- Text: `IP-Adapter`
  Destination: Document Understanding & OCR
  Example: `part-7-multimodal-generation/module-32-embodied-world-models/section-32.6.html:43` href=`../module-31-multimodal/section-31.3.html`

- Text: `Instructor library`
  Destination: Structured Output & Tool Integration
  Example: `part-3-working-with-llms/module-14-prompt-engineering/index.html:78` href=`../module-13-llm-apis/section-13.2.html`

- Text: `Mixture-of-Experts`
  Destination: Open-Source & Open-Weight Models
  Example: `part-12-frontiers/module-61-frontier-architectures/section-61.3.html:384` href=`../../part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html`

- Text: `Mixture-of-experts`
  Destination: Open-Source & Open-Weight Models
  Example: `part-2-understanding-llms/module-10-inference-optimization/section-10.5.html:263` href=`../module-08-modern-llm-landscape/section-8.2.html`

- Text: `Pretraining Foundations (Section 7.1)`
  Destination: BERT, GPT, T5: Three Bets That Shaped Today's LLMs
  Example: `appendices/appendix-b-ml-essentials/section-b.1.html:53` href=`../../part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html`

- Text: `Production Observability and Cost Control`
  Destination: Agentic Security Benchmarks for Tool-Using Systems
  Example: `part-9-safety-security-ethics/module-38-agent-safety-security/section-38.2.html:264` href=`section-38.3.html`

- Text: `RAG pipeline`
  Destination: Embeddings, Vector Databases & Semantic Search
  Example: `part-10-idea-to-product/module-45-prototype-to-production/section-45.5.html:68` href=`../../part-5-retrieval-conversation/module-22-embeddings-vector-db/index.html`

- Text: `Rate limiting`
  Destination: Frontend & User Interfaces
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html:688` href=`../../part-8-evaluation-production/module-35-production-engineering/section-35.2.html`

- Text: `Structured output`
  Destination: API Engineering Best Practices
  Example: `part-8-evaluation-production/module-34-evaluation-observability/section-34.3.html:423` href=`../../part-3-working-with-llms/module-13-llm-apis/section-13.3.html`

- Text: `architecture deep dive in Chapter 08`
  Destination: Chapter 9: Reasoning Models & Test-Time Compute
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.10.html:260` href=`../../part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html`

- Text: `context limit`
  Destination: Build a Transformer from Scratch
  Example: `part-5-retrieval-conversation/module-24-conversational-ai/section-24.4.html:539` href=`../../part-1-foundations/module-04-transformer-architecture/section-4.2.html`

- Text: `drift monitoring`
  Destination: Testing LLM Applications
  Example: `part-4-training-adapting/module-19-peft/section-19.7.html:72` href=`../../part-8-evaluation-production/module-34-evaluation-observability/section-34.3.html`

- Text: `encoder-decoder`
  Destination: GPU Fundamentals & Systems
  Example: `part-7-multimodal-generation/module-31-multimodal/section-31.3.html:50` href=`../../part-1-foundations/module-04-transformer-architecture/section-4.4.html`

- Text: `full regulatory landscape`
  Destination: Safety, Ethics & Regulation
  Example: `part-10-idea-to-product/module-48-shipping-deploying/section-48.1.html:277` href=`../../part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html`

- Text: `function calling`
  Destination: Memory Architecture for Agents: Taxonomy, Storage, and Policies
  Example: `part-12-frontiers/module-62-frontier-theory/section-62.4.html:63` href=`../../part-6-agentic-ai/module-26-ai-agents/section-26.6.html`

- Text: `generates responses`
  Destination: Decoding Strategies & Text Generation
  Example: `part-5-retrieval-conversation/module-24-conversational-ai/section-24.1.html:63` href=`../../part-1-foundations/module-05-decoding-text-generation/index.html`

- Text: `generative fluency of LLMs`
  Destination: Decoding Strategies & Text Generation
  Example: `part-5-retrieval-conversation/module-23-rag/section-23.1.html:156` href=`../../part-1-foundations/module-05-decoding-text-generation/index.html`

- Text: `knowledge distillation`
  Destination: Parameter-Efficient Fine-Tuning (PEFT)
  Example: `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.3.html:152` href=`../../part-4-training-adapting/module-19-peft/index.html`

- Text: `knowledge graphs`
  Destination: Deep Research & Agentic RAG
  Example: `part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html:585` href=`../../part-5-retrieval-conversation/module-23-rag/section-23.4.html`

- Text: `latest models from each provider`
  Destination: Modern LLM Landscape & Model Internals
  Example: `part-3-working-with-llms/module-13-llm-apis/section-13.1.html:504` href=`../../part-2-understanding-llms/module-08-modern-llm-landscape/index.html`

- Text: `mixture-of-experts`
  Destination: Open-Source & Open-Weight Models
  Example: `part-12-frontiers/module-61-frontier-architectures/section-61.1.html:143` href=`../../part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html`

- Text: `monitoring dashboard`
  Destination: LLM Evaluation & Quality Metrics
  Example: `part-10-idea-to-product/module-45-prototype-to-production/section-45.1.html:60` href=`../../part-8-evaluation-production/module-34-evaluation-observability/index.html`

- Text: `named entity recognition (NER)`
  Destination: Contextual Embeddings: ELMo & the Path to Transformers
  Example: `part-5-retrieval-conversation/module-24-conversational-ai/section-24.1.html:60` href=`../../part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html`

- Text: `plan and execute`
  Destination: Memory Architecture for Agents: Taxonomy, Storage, and Policies
  Example: `part-5-retrieval-conversation/module-23-rag/section-23.3.html:581` href=`../../part-6-agentic-ai/module-26-ai-agents/section-26.6.html`

- Text: `positional encodings`
  Destination: Build a Transformer from Scratch
  Example: `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.7.html:38` href=`../../part-1-foundations/module-04-transformer-architecture/section-4.2.html`

- Text: `quantization fundamentals`
  Destination: Parameter-Efficient Fine-Tuning (PEFT)
  Example: `part-8-evaluation-production/module-35-production-engineering/section-35.7.html:42` href=`../../part-4-training-adapting/module-19-peft/index.html`

- Text: `rate limit`
  Destination: Frontend & User Interfaces
  Example: `part-6-agentic-ai/module-27-tool-use-protocols/section-27.4.html:114` href=`../../part-8-evaluation-production/module-35-production-engineering/section-35.2.html`

- Text: `safety and compliance`
  Destination: Ideation: Finding LLM-Worthy Problems
  Example: `part-10-idea-to-product/module-46-compute-planning/section-46.4.html:42` href=`../module-40-ideation/index.html`

_(... and 6 more unique mismatch patterns, capped.)_

## P1: Number drift (topic right, citation stale)

Anchor cites a chapter / section / appendix number that no longer matches the
destination, but the destination IS still about the same topic. Rewrite the prose
to cite the new number; the href is already correct.

- Chapter 9 -> Chapter 10: Inference Optimization & Efficient Serving (21 occurrences)
  Example: `part-1-foundations/module-04-transformer-architecture/section-4.4.html:425` text=`Chapter 09`
  Other: `part-1-foundations/module-05-decoding-text-generation/section-5.4.html:404`, `part-10-idea-to-product/module-47-scaling-economics/section-47.4.html:38`, `part-10-idea-to-product/module-47-scaling-economics/section-47.4.html:42`, `part-12-frontiers/module-61-frontier-architectures/index.html:77`, `part-12-frontiers/module-61-frontier-architectures/section-33.4.html:443` (...)

- Chapter 6 -> Chapter 7: Pre-training, Scaling Laws & Data Curation (13 occurrences)
  Example: `front-matter/fm-how-to-use.html:96` text=`Chapter 06 (Pre-training and Scaling Laws)`
  Other: `part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html:135`, `part-1-foundations/module-05-decoding-text-generation/section-5.4.html:402`, `part-1-foundations/module-05-decoding-text-generation/section-5.4.html:604`, `part-12-frontiers/module-61-frontier-architectures/index.html:76`, `part-12-frontiers/module-61-frontier-architectures/section-33.4.html:51` (...)

- Chapter 7 -> Chapter 8: Modern LLM Landscape & Model Internals (13 occurrences)
  Example: `part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html:516` text=`Chapter 07`
  Other: `part-1-foundations/module-02-tokenization-subword-models/section-2.2.html:81`, `part-1-foundations/module-05-decoding-text-generation/section-5.4.html:403`, `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.8.html:514`, `part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html:83`, `part-2-understanding-llms/module-10-inference-optimization/index.html:88` (...)

- Appendix P -> Appendix L: Inference Serving: vLLM, TGI, and SGLang (6 occurrences)
  Example: `appendices/appendix-k-experiment-tracking/section-k.4.html:111` text=`Appendix P`
  Other: `appendices/appendix-k-experiment-tracking/section-k.4.html:207`, `appendices/appendix-m-distributed-ml/section-m.3.html:228`, `appendices/appendix-m-distributed-ml/section-m.5.html:34`, `appendices/appendix-m-distributed-ml/section-m.5.html:258`, `appendices/appendix-m-distributed-ml/section-m.7.html:118`

- Chapter 8 -> Chapter 9: Reasoning Models & Test-Time Compute (6 occurrences)
  Example: `part-2-understanding-llms/module-08-modern-llm-landscape/index.html:128` text=`Chapter 08`
  Other: `part-2-understanding-llms/module-10-inference-optimization/section-10.6.html:42`, `part-4-training-adapting/module-17-synthetic-data/section-17.6.html:48`, `part-4-training-adapting/module-17-synthetic-data/section-17.6.html:49`, `part-6-agentic-ai/module-26-ai-agents/index.html:75`, `part-6-agentic-ai/module-26-ai-agents/section-26.3.html:42`

- Chapter 9 -> Chapter 10: Model Quantization (6 occurrences)
  Example: `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html:142` text=`Chapter 09: Quantization and Inference Optimization`
  Other: `part-1-foundations/module-04-transformer-architecture/section-4.1.html:771`, `part-1-foundations/module-04-transformer-architecture/section-4.3.html:51`, `part-10-idea-to-product/module-46-compute-planning/section-46.3.html:38`, `part-12-frontiers/module-61-frontier-architectures/section-61.3.html:379`, `part-8-evaluation-production/module-35-production-engineering/section-35.3.html:160`

- Appendix D -> Appendix C: HuggingFace: Transformers, Datasets, and Hub (5 occurrences)
  Example: `appendices/appendix-m-distributed-ml/section-m.1.html:547` text=`Appendix D`
  Other: `appendices/appendix-m-distributed-ml/section-m.4.html:45`, `appendices/appendix-m-distributed-ml/section-m.4.html:160`, `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.1.html:44`, `part-4-training-adapting/module-19-peft/section-19.1.html:47`

- Chapter 17 -> Chapter 18: Fine-Tuning Fundamentals (3 occurrences)
  Example: `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.5.html:195` text=`Chapter 17`
  Other: `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html:58`, `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.4.html:66`

- Section 9.5 -> Section 10.5: Model Pruning & Sparsity (3 occurrences)
  Example: `part-2-understanding-llms/module-10-inference-optimization/index.html:140` text=`9.5 Model Pruning & Sparsity Structured and unstructured pruning techniques, magnitude and gradient-based
              `
  Other: `part-2-understanding-llms/module-10-inference-optimization/section-10.3.html:130`, `part-2-understanding-llms/module-10-inference-optimization/section-10.6.html:97`

- Appendix G -> Appendix K: Experiment Tracking: W&B and MLflow (2 occurrences)
  Example: `appendices/appendix-m-distributed-ml/section-m.4.html:319` text=`Appendix G`
  Other: `appendices/appendix-m-distributed-ml/section-m.4.html:585`

- Appendix K -> Appendix D: LangChain: Chains, Agents, and Retrieval (2 occurrences)
  Example: `appendices/appendix-k-experiment-tracking/section-k.5.html:360` text=`Appendix K`
  Other: `part-6-agentic-ai/module-28-multi-agent-systems/section-28.1.html:50`

- Chapter 11 -> Chapter 10: Inference Optimization & Efficient Serving (2 occurrences)
  Example: `part-2-understanding-llms/module-10-inference-optimization/section-10.4.html:47` text=`Chapter 11: Inference Optimization & Efficient Serving`
  Other: `part-2-understanding-llms/module-10-inference-optimization/section-10.6.html:314`

- Chapter 25 -> Chapter 26: AI Agent Foundations (2 occurrences)
  Example: `part-6-agentic-ai/module-29-specialized-agents/index.html:112` text=`Chapter 25`
  Other: `part-6-agentic-ai/module-29-specialized-agents/section-29.4.html:467`

- Chapter 52 -> Chapter 37: Safety, Ethics & Regulation (2 occurrences)
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.11.html:910` text=`Chapter 52: Safety, Ethics & Regulation`
  Other: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.12.html:39`

- Part X -> Part XII (2 occurrences)
  Example: `part-10-idea-to-product/module-47-scaling-economics/section-47.4.html:601` text=`Part X: Frontiers`
  Other: `part-9-safety-security-ethics/index.html:100`

- Part XI -> Part X (2 occurrences)
  Example: `part-12-frontiers/index.html:70` text=`Part XI`
  Other: `part-12-frontiers/module-61-frontier-architectures/index.html:185`

- Section 30.10 -> Section 37.10: Environmental Impact & Green AI (2 occurrences)
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:186` text=`30.10 Environmental Impact & Green AI Carbon and water footprint of training and inference. Measurement methodology,
   `
  Other: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:261`

- Section 30.11 -> Section 37.11: Privacy Attacks & Differential Privacy for LLMs (2 occurrences)
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:197` text=`30.11 Privacy Attacks & Differential Privacy for LLMs Membership inference, training-data extraction, model inversion. D`
  Other: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:272`

- Section 30.6 -> Section 37.6: LLM Licensing, IP & Privacy (2 occurrences)
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:143` text=`30.6 LLM Licensing, IP & Privacy Model license families (proprietary, open-weight, restricted-use), copyright in trainin`
  Other: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:221`

- Section 30.7 -> Section 37.7: Machine Unlearning (2 occurrences)
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:154` text=`30.7 Machine Unlearning Removing specific training data influence from a deployed model. Approximate unlearning
        `
  Other: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:231`

- Section 30.8 -> Section 37.8: Red Teaming Frameworks & LLM Security Testing (2 occurrences)
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:164` text=`30.8 Red Teaming Frameworks & LLM Security Testing Structured adversarial probing of deployed models. Attack taxonomies,`
  Other: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:241`

- Section 30.9 -> Section 37.9: EU AI Act Compliance in Practice (2 occurrences)
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:175` text=`30.9 EU AI Act Compliance in Practice Translating the EU AI Act's risk tiers into concrete engineering deliverables: con`
  Other: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html:251`

- Section 9.1 -> Section 10.1: Model Quantization (2 occurrences)
  Example: `part-2-understanding-llms/module-10-inference-optimization/index.html:96` text=`9.1 Model Quantization Quantization math (absmax, zero-point, per-group), data types (INT8, INT4, FP8, NF4),
           `
  Other: `part-2-understanding-llms/module-10-inference-optimization/section-10.6.html:97`

- Appendix G -> Appendix M: Distributed ML: PySpark, Databricks, and Ray
  Example: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.11.html:687` text=`Appendix G`

- Appendix M.1 -> Appendix L.1: vLLM: PagedAttention, Continuous Batching, and OpenAI-Compatible API
  Example: `appendices/appendix-l-inference-serving/index.html:49` text=`M.1 vLLM: PagedAttention, Continuous Batching, and OpenAI-Compatible API`

- Appendix M.2 -> Appendix L.2: Text Generation Inference (TGI): Deployment and Configuration
  Example: `appendices/appendix-l-inference-serving/index.html:55` text=`M.2 Text Generation Inference (TGI): Deployment and Configuration`

- Appendix M.3 -> Appendix L.3: SGLang: Structured Generation and RadixAttention
  Example: `appendices/appendix-l-inference-serving/index.html:61` text=`M.3 SGLang: Structured Generation and RadixAttention`

- Appendix M.4 -> Appendix L.4: Quantization for Serving: GPTQ, AWQ, and GGUF
  Example: `appendices/appendix-l-inference-serving/index.html:67` text=`M.4 Quantization for Serving: GPTQ, AWQ, and GGUF`

- Appendix M.5 -> Appendix L.5: Scaling and Load Balancing for Production
  Example: `appendices/appendix-l-inference-serving/index.html:73` text=`M.5 Scaling and Load Balancing for Production`

- Appendix N.1 -> Appendix M.1: PySpark for LLM Data Pipelines
  Example: `appendices/appendix-m-distributed-ml/index.html:49` text=`N.1 PySpark for LLM Data Pipelines`

- Appendix N.2 -> Appendix M.2: Delta Lake and Lakehouse Architecture
  Example: `appendices/appendix-m-distributed-ml/index.html:55` text=`N.2 Delta Lake and Lakehouse Architecture`

- Appendix N.3 -> Appendix M.3: Databricks: Workspace, Notebooks, and Unity Catalog
  Example: `appendices/appendix-m-distributed-ml/index.html:61` text=`N.3 Databricks: Workspace, Notebooks, and Unity Catalog`

- Appendix N.4 -> Appendix M.4: Databricks AI and Foundation Models
  Example: `appendices/appendix-m-distributed-ml/index.html:67` text=`N.4 Databricks AI and Foundation Models`

- Appendix N.5 -> Appendix M.5: Ray Train, Ray Serve, and Ray Data
  Example: `appendices/appendix-m-distributed-ml/index.html:73` text=`N.5 Ray Train, Ray Serve, and Ray Data`

- Appendix N.6 -> Appendix M.6: Feature Stores: Feast, Tecton, and Databricks Feature Engineering
  Example: `appendices/appendix-m-distributed-ml/index.html:79` text=`N.6 Feature Stores: Feast, Tecton, and Databricks Feature Engineering`

- Appendix N.7 -> Appendix M.7: Production Data Pipelines and Model Serving at Scale
  Example: `appendices/appendix-m-distributed-ml/index.html:85` text=`N.7 Production Data Pipelines and Model Serving at Scale`

- Appendix O.1 -> Appendix N.1: Docker Fundamentals: Images, Containers, and Volumes
  Example: `appendices/appendix-n-docker-containers/index.html:53` text=`O.1 Docker Fundamentals: Images, Containers, and Volumes`

- Appendix O.2 -> Appendix N.2: Writing Dockerfiles for ML and LLM Projects
  Example: `appendices/appendix-n-docker-containers/index.html:59` text=`O.2 Writing Dockerfiles for ML and LLM Projects`

- Appendix O.3 -> Appendix N.3: Docker Compose for Multi-Service AI Applications
  Example: `appendices/appendix-n-docker-containers/index.html:65` text=`O.3 Docker Compose for Multi-Service AI Applications`

- Appendix O.4 -> Appendix N.4: Containerizing LLM Inference Servers
  Example: `appendices/appendix-n-docker-containers/index.html:71` text=`O.4 Containerizing LLM Inference Servers`

- Chapter 10 -> Chapter 9: Reasoning Models & Test-Time Compute
  Example: `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.5.html:447` text=`Chapter 10: Reasoning Models & Test-Time Compute`

- Chapter 13 -> Chapter 14: Prompt Engineering & Advanced Techniques
  Example: `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.2.html:168` text=`Chapter 13`

- Chapter 13 -> Chapter 20: Alignment: RLHF, DPO & Preference Tuning
  Example: `appendices/appendix-c-huggingface-ecosystem/section-c.4.html:43` text=`Chapter 13: Alignment and RLHF`

- Chapter 15 -> Chapter 17: Synthetic Data Generation & LLM Simulation
  Example: `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html:206` text=`Chapter 15`

- Chapter 18 -> Chapter 19: Parameter-Efficient Fine-Tuning (PEFT)
  Example: `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html:58` text=`Chapter 18`

- Chapter 20 -> Chapter 11: Interpretability & Mechanistic Understanding
  Example: `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.7.html:204` text=`Chapter 20`

- Chapter 20 -> Chapter 19: Knowledge Distillation for LLMs
  Example: `part-1-foundations/module-05-decoding-text-generation/section-5.2.html:93` text=`knowledge distillation in Chapter 20`

- Chapter 20 -> Chapter 19: Parameter-Efficient Fine-Tuning (PEFT)
  Example: `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.2.html:210` text=`Chapter 20`

- Chapter 24 -> Chapter 20: Alignment: RLHF, DPO & Preference Tuning
  Example: `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.5.html:57` text=`Chapter 24: Alignment: RLHF, DPO & Preference Tuning`

- Chapter 25 -> Chapter 37: Safety, Ethics & Regulation
  Example: `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html:312` text=`Chapter 25`

_(... and 159 more unique drift patterns, capped.)_

## P2: Stale label (dropped resource)

Anchor text refers to a resource that was dropped in v9 (Master Reference Tables,
2026 Freshness Index, Appendix AD/AE/AI). The href may resolve to a different
appendix now, but the prose still names the old one. Rephrase to drop the
reference or re-point to the actual current resource.

_None detected._

## P3: Over-promise

Claim makes a specific promise ("for the GitHub Actions recipe",
"see the YAML example") that the destination section may not fulfill.
Detection is heuristic; we do not actively flag P3 yet (manual spot-check needed).

_None auto-detected. Consider a manual sweep for prose like "for the X recipe", "see the example below"._

## Top patterns

### P0 mismatch frequency

| Occurrences | Citation -> Destination |
|---:|---|
| 1 | `Chapter 8 -> Chapter 9` |

### P1 number-drift frequency

| Occurrences | Citation -> Destination |
|---:|---|
| 27 | `Chapter 9 -> Chapter 10` |
| 14 | `Chapter 6 -> Chapter 7` |
| 13 | `Chapter 7 -> Chapter 8` |
| 6 | `Appendix P -> Appendix L` |
| 6 | `Chapter 8 -> Chapter 9` |
| 5 | `Appendix D -> Appendix C` |
| 3 | `Chapter 17 -> Chapter 18` |
| 3 | `Section 9.5 -> Section 10.5` |
| 2 | `Appendix K -> Appendix D` |
| 2 | `Appendix G -> Appendix K` |
| 2 | `Chapter 20 -> Chapter 19` |
| 2 | `Part X -> Part XII` |
| 2 | `Part XI -> Part X` |
| 2 | `Section 9.1 -> Section 10.1` |
| 2 | `Chapter 11 -> Chapter 10` |
| 2 | `Chapter 25 -> Chapter 26` |
| 2 | `Section 30.6 -> Section 37.6` |
| 2 | `Section 30.7 -> Section 37.7` |
| 2 | `Section 30.8 -> Section 37.8` |
| 2 | `Section 30.9 -> Section 37.9` |

### P2 dropped-resource labels

_None._

### Files with most relevance issues (top 20)

| Issues | File |
|---:|---|
| 18 | `part-9-safety-security-ethics/module-37-safety-ethics-regulation/index.html` |
| 12 | `part-8-evaluation-production/module-34-evaluation-observability/index.html` |
| 10 | `part-5-retrieval-conversation/module-23-rag/index.html` |
| 9 | `part-2-understanding-llms/module-07-pretraining-scaling-laws/index.html` |
| 9 | `part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html` |
| 9 | `part-7-multimodal-generation/module-31-multimodal/index.html` |
| 9 | `part-8-evaluation-production/module-35-production-engineering/index.html` |
| 8 | `part-2-understanding-llms/module-10-inference-optimization/index.html` |
| 8 | `part-4-training-adapting/module-18-fine-tuning-fundamentals/index.html` |
| 8 | `part-4-training-adapting/module-19-peft/index.html` |
| 7 | `appendices/appendix-m-distributed-ml/index.html` |
| 7 | `part-10-idea-to-product/module-45-prototype-to-production/index.html` |
| 7 | `part-3-working-with-llms/module-15-hybrid-ml-llm/index.html` |
| 7 | `part-4-training-adapting/module-17-synthetic-data/index.html` |
| 7 | `part-4-training-adapting/module-20-alignment-rlhf-dpo/index.html` |
| 7 | `part-6-agentic-ai/module-26-ai-agents/index.html` |
| 6 | `part-3-working-with-llms/module-14-prompt-engineering/index.html` |
| 6 | `part-2-understanding-llms/module-08-modern-llm-landscape/index.html` |
| 5 | `appendices/appendix-l-inference-serving/index.html` |
| 5 | `part-2-understanding-llms/module-11-interpretability/index.html` |

## Method notes

Audit logic (`scripts/_audit_crosslink_relevance.py`):

1. Walk every `<a href>` in `<body>` (skipping `nav.chapter-nav`, `nav.header-nav`, 
   `header.chapter-header`, `footer`).
2. Skip external, anchor-only, self, and broken-target links.
3. For each link, read the destination file's `<h1>` and path-derived identity 
   (chapter number from `module-NN-*`, section from `section-N.M.html`, etc.).
4. P1 = anchor mentions a chapter/section/appendix/part number that does not match 
   the destination's actual number, but the topic noun-phrase still overlaps the 
   destination `<h1>` (>=1 content word in common).
5. P0 = number cited and destination differ AND the topic noun-phrase has zero 
   overlap with the destination `<h1>` (or anchor text has >=2 strong content words 
   and zero overlap with the destination, even without a number).
6. P2 = anchor text contains a dropped-resource label ('Master Reference Tables', 
   'Freshness Index', 'Appendix AD/AE/AI'), independent of href resolution.
7. Word overlap is computed over lowercased content words (>=3 chars, not stopwords), 
   crudely singularized. Some false negatives are inevitable on synonyms.

Limitations:

- Single-word anchor text ("here", "see", "this section") is not checked for topic match.
- Synonym mismatch ('RAG' vs 'Retrieval-Augmented Generation') may slip through if both 
  forms appear in the destination's `<h1>` we'll match.
- P3 (over-promise like "GitHub Actions recipe" pointing to a page that does not 
  contain that recipe) is not auto-detected; the section is reserved for manual notes.
- Some agents are actively editing files (C/D/E/F/G, H/I/J/K, Tools-of-the-Trade, 
  whats-next blocks); their changes may not be reflected here.

---

Audit generated by `scripts/_audit_crosslink_relevance.py` (read-only).
