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
| drift | 23 | 0 | 0 | 23 |
| rag | 14 | 0 | 0 | 14 |
| diffusion | 10 | 0 | 0 | 10 |
| lora | 8 | 0 | 0 | 8 |
| quantization | 8 | 0 | 0 | 8 |
| pruning | 8 | 0 | 0 | 8 |
| perplexity | 7 | 0 | 0 | 7 |
| chain-of-thought | 7 | 0 | 0 | 7 |
| self-consistency | 5 | 0 | 0 | 5 |
| rlhf | 5 | 0 | 0 | 5 |
| kv cache | 5 | 0 | 0 | 5 |
| bpe | 4 | 0 | 0 | 4 |
| tf-idf | 3 | 0 | 0 | 3 |
| speculative decoding | 3 | 0 | 0 | 3 |
| context length | 3 | 0 | 0 | 3 |
| dpo | 4 | 1 | 0 | 3 |
| knowledge distillation | 3 | 0 | 0 | 3 |
| position bias | 3 | 0 | 0 | 3 |
| ppo | 2 | 0 | 0 | 2 |
| self-attention | 2 | 0 | 0 | 2 |
| cross-attention | 2 | 0 | 0 | 2 |
| rope | 2 | 0 | 0 | 2 |
| differential privacy | 2 | 0 | 0 | 2 |
| constitutional ai | 2 | 0 | 0 | 2 |
| context window | 2 | 0 | 0 | 2 |
| yarn | 2 | 0 | 0 | 2 |
| qlora | 2 | 0 | 0 | 2 |
| kto | 2 | 0 | 0 | 2 |
| orpo | 2 | 0 | 0 | 2 |
| react | 2 | 0 | 0 | 2 |

## Sections with shallow orphan introductions (top 50)

| Section | Entity | Phrase | depth | link |
|---|---|---|---:|---:|
| S0.4 | PPO | Proximal Policy Optimization (PPO) | 0 | n |
| S1.2 | TF-IDF | TF-IDF is still used today | 0 | n |
| S1.2 | TF-IDF | With BoW/TF-IDF, we CAN: | 0 | n |
| S1.4 | TF-IDF | TF-IDF | 0 | n |
| S1.6 | BPE | byte-level BPE | 0 | n |
| S1.6 | BPE | Byte-level BPE | 0 | n |
| S10.8 | Quantization | Quantization speed | 0 | n |
| S11.1 | drift | API version drift: | 0 | n |
| S12.2 | Chain-of-Thought | "Chain-of-Thought Prompting Elicits Reasoning in L | 0 | n |
| S12.2 | Self-Consistency | "Self-Consistency Improves Chain of Thought Reason | 0 | n |
| S12.2 | Self-consistency | Self-consistency | 0 | n |
| S12.2 | Self-consistency | Self-consistency and verification. | 0 | n |
| S12.2 | chain-of-thought | Why does chain-of-thought work mechanistically? | 0 | n |
| S12.2 | chain-of-thought | Reasoning tokens and internal chain-of-thought. | 0 | n |
| S13.5 | position bias | position bias | 0 | n |
| S16.1 | RAG | RAG | 0 | n |
| S16.7 | Context length | Context length and context utilization | 0 | n |
| S16.7 | RoPE | RoPE scaling methods (especially YaRN) | 0 | n |
| S17.1 | LoRA | LoRA | 0 | n |
| S17.1 | LoRA | Why does LoRA work with so few parameters? | 0 | n |
| S17.2 | DoRA | DoRA | 0 | n |
| S17.2 | LoRA | LoRA dominates the PEFT landscape, but it | 0 | n |
| S17.2 | LoRA | LoRA | 0 | n |
| S17.2 | LoRA | LoRA+ | 0 | n |
| S17.2 | QLoRA | QLoRA | 0 | n |
| S17.3 | RLHF | RLHF/DPO | 0 | n |
| S17.4 | LoRA | LoRA | 0 | n |
| S17.4 | QLoRA | QLoRA | 1 | n |
| S17.5a | Knowledge distillation | Knowledge distillation | 0 | n |
| S17.5b | Chain-of-thought | Chain-of-thought
 (CoT) distillation | 0 | n |
| S17.5b | Knowledge distillation | Knowledge distillation | 0 | n |
| S17.7 | LoRA | LoRA rank scheduling | 0 | n |
| S18.1 | Goodhart's Law | Goodhart's Law | 0 | n |
| S18.1 | PPO | Value model (PPO) | 0 | n |
| S18.1 | RLHF | RLHF | 0 | n |
| S18.1 | RLHF | Why is RLHF fundamentally different from SFT? | 0 | n |
| S18.2a | DPO | Why DPO avoids reward model training (and why that | 0 | n |
| S18.2b | DPO | DPO | 0 | n |
| S18.2b | IPO | IPO | 1 | n |
| S18.2b | KTO | KTO | 0 | n |
| S18.2b | ORPO | ORPO | 0 | n |
| S18.3 | Constitutional AI | Constitutional AI | 0 | n |
| S19.2 | KTO | KTO | 0 | n |
| S19.2 | ORPO | ORPO | 0 | n |
| S2.3a | cross-attention | cross-attention | 0 | n |
| S2.3a | self-attention | self-attention | 0 | n |
| S2.3b | Cross-attention | Cross-attention | 0 | n |
| S2.3b | Multi-head attention | Multi-head attention | 1 | n |
| S20.3 | diffusion | latent audio diffusion | 0 | n |
| S20.9 | diffusion | video-native diffusion inpainting | 0 | n |

... and 123 more orphans.
