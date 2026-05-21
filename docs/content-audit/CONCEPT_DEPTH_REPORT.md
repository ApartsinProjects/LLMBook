# Concept-Explanation Depth Report

For each bolded technical concept (in the curated entity dictionary),
score the depth signals in the 800-char window AFTER the bold:
  - math block, code block, algorithm callout, numeric example,
    diagram, practical example, step-by-step list.
  - has-link-out = the intro defers to a canonical deep treatment elsewhere.

Depth categories:
  - DEEP (>=2 signals): this is a deep treatment, candidate canonical home
  - SHALLOW + LINKED: defers properly to canonical home
  - SHALLOW + ORPHAN: superficial mention with no link out, no depth — gap

## Entity summary (top 30 by orphan-shallow count)

| Entity | Total | Deep | Shallow+Linked | Shallow+Orphan |
|---|---:|---:|---:|---:|
| drift | 23 | 0 | 1 | 22 |
| rag | 14 | 0 | 0 | 14 |
| perplexity | 7 | 0 | 0 | 7 |
| quantization | 8 | 0 | 1 | 7 |
| diffusion | 10 | 0 | 4 | 6 |
| lora | 8 | 0 | 2 | 6 |
| pruning | 8 | 0 | 3 | 5 |
| chain-of-thought | 7 | 0 | 3 | 4 |
| self-consistency | 5 | 0 | 1 | 4 |
| tf-idf | 3 | 0 | 0 | 3 |
| bpe | 4 | 0 | 1 | 3 |
| rlhf | 5 | 0 | 2 | 3 |
| kv cache | 5 | 0 | 2 | 3 |
| knowledge distillation | 3 | 0 | 0 | 3 |
| position bias | 4 | 0 | 1 | 3 |
| self-attention | 2 | 0 | 0 | 2 |
| cross-attention | 2 | 0 | 0 | 2 |
| speculative decoding | 3 | 0 | 1 | 2 |
| differential privacy | 2 | 0 | 0 | 2 |
| context window | 2 | 0 | 0 | 2 |
| context length | 3 | 0 | 1 | 2 |
| dpo | 4 | 1 | 1 | 2 |
| qlora | 2 | 0 | 0 | 2 |
| react | 2 | 0 | 0 | 2 |
| self-rag | 2 | 0 | 0 | 2 |
| ragas | 2 | 0 | 0 | 2 |
| bleu | 2 | 0 | 0 | 2 |
| bertscore | 2 | 0 | 0 | 2 |
| meteor | 2 | 0 | 0 | 2 |
| ppo | 2 | 0 | 1 | 1 |

## Sections with shallow orphan introductions (top 50)

| Section | Entity | Phrase | depth | link |
|---|---|---|---:|---:|
| S1.2 | TF-IDF | TF-IDF is still used today | 0 | n |
| S1.2 | TF-IDF | With BoW/TF-IDF, we CAN: | 0 | n |
| S1.4 | TF-IDF | TF-IDF | 0 | n |
| S1.6 | BPE | Byte-level BPE | 0 | n |
| S12.2 | Self-consistency | Self-consistency | 0 | n |
| S12.2 | Self-consistency | Self-consistency and verification. | 0 | n |
| S12.2 | chain-of-thought | Why does chain-of-thought work mechanistically? | 0 | n |
| S12.2 | chain-of-thought | Reasoning tokens and internal chain-of-thought. | 0 | n |
| S16.1 | RAG | RAG | 0 | n |
| S16.7 | RoPE | RoPE scaling methods (especially YaRN) | 0 | n |
| S17.1 | LoRA | LoRA | 0 | n |
| S17.1 | LoRA | Why does LoRA work with so few parameters? | 0 | n |
| S17.2 | DoRA | DoRA | 0 | n |
| S17.2 | LoRA | LoRA dominates the PEFT landscape, but it | 0 | n |
| S17.2 | LoRA | LoRA | 0 | n |
| S17.2 | LoRA | LoRA+ | 0 | n |
| S17.2 | QLoRA | QLoRA | 0 | n |
| S17.4 | QLoRA | QLoRA | 1 | n |
| S17.5a | Knowledge distillation | Knowledge distillation | 0 | n |
| S17.5b | Chain-of-thought | Chain-of-thought
 (CoT) distillation | 0 | n |
| S17.5b | Knowledge distillation | Knowledge distillation | 0 | n |
| S18.1 | PPO | Value model (PPO) | 0 | n |
| S18.1 | RLHF | RLHF | 0 | n |
| S18.1 | RLHF | Why is RLHF fundamentally different from SFT? | 0 | n |
| S18.2a | DPO | Why DPO avoids reward model training (and why that | 0 | n |
| S18.2b | DPO | DPO | 0 | n |
| S18.2b | IPO | IPO | 1 | n |
| S18.2b | KTO | KTO | 0 | n |
| S18.2b | ORPO | ORPO | 0 | n |
| S2.3a | cross-attention | cross-attention | 0 | n |
| S2.3a | self-attention | self-attention | 0 | n |
| S2.3b | Cross-attention | Cross-attention | 0 | n |
| S2.3b | Multi-head attention | Multi-head attention | 1 | n |
| S20.3 | diffusion | latent audio diffusion | 0 | n |
| S20.9 | diffusion | video-native diffusion inpainting | 0 | n |
| S21.4 | Drift | Q3: Drift detection. | 0 | n |
| S25.2 | Diffusion | Diffusion Transformer (DiT) and Flow Matching | 0 | n |
| S26.2 | ReAct | Simple ReAct loop: | 0 | n |
| S26.3 | ReAct | Step 2: Build the ReAct prompt template. | 1 | n |
| S3.1a | perplexity | perplexity | 0 | n |
| S3.1b | Self-Attention | Masked Multi-Head Self-Attention | 1 | n |
| S30.2b | self-consistency | self-consistency decoding | 0 | n |
| S31.2 | quantization | anisotropic vector quantization | 0 | n |
| S31.2 | quantization | Hybrid quantization | 0 | n |
| S31.4 | RAG | The quality of your RAG system | 0 | n |
| S32.1a | RAG | RAG (retrieval) | 0 | n |
| S32.1b | RAG | RAG and long context | 0 | n |
| S32.1b | RAG | Corrective RAG (CRAG) | 0 | n |
| S32.1b | RAG | Speculative RAG | 0 | n |
| S32.1b | Self-RAG | Self-RAG | 0 | n |

... and 92 more orphans.
