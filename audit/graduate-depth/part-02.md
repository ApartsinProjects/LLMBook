# Graduate-Depth Audit: Part 2 (Understanding LLMs)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 6.1 | BERT, GPT, T5: three bets | COURSE-READY | |
| 6.2 | Pretraining objectives | COURSE-READY | |
| 6.3 | Scaling laws and compute-optimal | COURSE-READY | |
| 6.4 | Data curation at scale | COURSE-READY | |
| 6.5 | Optimizers and training dynamics | COURSE-READY | |
| 6.6 | Distributed training at scale | COURSE-READY | |
| 6.6a | Mixed precision, 3D parallelism, ring attention | COURSE-READY | |
| 6.7 | In-context learning theory | COURSE-READY | |
| 6.8 | Production training (Megatron, fault tolerance) | COURSE-READY | |
| 6.9 | Lab: pretrain a tiny LM | COURSE-READY | |
| 7.1 | Closed-source frontier models | DEPTH-GAP | Capability/spec catalog of GPT-4o and o-series; no derived mechanism beyond what 6.x already gives. Reads as a vendor map, not a derivation. |
| 7.2 | Gemini, second-tier, multimodal patterns | COURSE-READY | |
| 7.2a | Rate limits, architectural inference, benchmarking | DEPTH-GAP | Production-constraint and benchmark-contamination survey; the load-bearing mechanism (architectural inference) is inference-from-outside, stated not derived. |
| 7.3 | Open-weight models and DeepSeek-V3 internals | COURSE-READY | |
| 7.4 | Multilingual pretraining and encoder lineage | COURSE-READY | |
| 7.4a | Multilingual eval, adaptation pipeline | COURSE-READY | |
| 8.1 | Test-time compute foundations | COURSE-READY | |
| 8.1a | KV cache growth, PRMs vs ORMs | COURSE-READY | |
| 8.2 | Reasoning model architectures (o-series, R1, QwQ) | COURSE-READY | |
| 8.3 | Training reasoning models (RLVR, GRPO) | COURSE-READY | |
| 8.4 | Prompting reasoning models | DEPTH-GAP | Applied decision-framework and do/do-not table; the why-self-consistency-works callout is the only mechanism, otherwise practitioner heuristics without derivation. |
| 8.5 | Compute-optimal inference, MCTS | COURSE-READY | |
| 8.6 | LLMs and formal proving (LeanDojo) | COURSE-READY | |
| 8.6a | AlphaProof, self-play, formal eval | COURSE-READY | |
| 9.1 | Quantization (why, NF4, BF16) | COURSE-READY | |
| 9.2 | PTQ algorithms (GPTQ, AWQ) | COURSE-READY | |
| 9.3 | KV cache and memory optimization | COURSE-READY | |
| 9.4 | Speculative decoding | COURSE-READY | |
| 9.5 | Serving stack and frameworks | CATALOG-OK | |
| 9.6 | Serving framework survey (SGLang, TGI, etc.) | CATALOG-OK | |
| 9.7 | Pruning and sparsity | COURSE-READY | |
| 9.8 | Test-time compute (inference view) | COURSE-READY | |
| 9.9 | Custom kernels and roofline | COURSE-READY | |
| 10.1 | Attention analysis and probing | COURSE-READY | |
| 10.2 | Mechanistic interpretability (SAE, patching) | COURSE-READY | |
| 10.3 | Practical interpretability (attribution, steering) | COURSE-READY | |
| 10.3a | Model editing (ROME, MEMIT), CoT faithfulness | COURSE-READY | |
| 10.4 | Explaining transformers (faithfulness) | COURSE-READY | |
| 10.5 | Interpretability tools ecosystem | CATALOG-OK | |
| 10.6 | LLM platforms and GPU rentals | CATALOG-OK | |
| 10.7 | Model-loading and tokenizer libraries | CATALOG-OK | |
| 10.8 | vLLM deep dive (tutorial) | COURSE-READY | |
| 10.9 | Pretraining corpora and benchmarks | CATALOG-OK | |
| 10.10 | The 2026 model zoo | CATALOG-OK | |
| 10.11 | External reading list | CATALOG-OK | |

## Summary
- COURSE-READY: 33 | DEPTH-GAP: 3 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 7
- Top sections most worth enriching:
  - 7.1 (closed-source frontier): add one load-bearing mechanism the rest of the part does not, e.g. a worked derivation of why native end-to-end multimodal fusion changes the loss/attention computation versus a bolt-on adapter, so the section teaches a principle rather than cataloging GPT-4o and o-series specs.
  - 8.4 (prompting reasoning models): replace the heuristic do/do-not table with a derived account of why RL-internalized CoT collides with externally-imposed CoT (a short mechanism tying the trained reasoning policy to prompt-conditioning), so the guidance is lecturable from first principles.
  - 7.2a (rate limits and architectural inference): promote the architectural-inference subsection from assertion to method by walking one concrete from-the-outside inference end to end (e.g. estimating MoE active-vs-total parameters from latency and pricing signals), turning a production-constraints survey into a transferable analysis skill.
