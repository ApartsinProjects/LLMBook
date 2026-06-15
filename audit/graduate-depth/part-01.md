# Graduate-Depth Audit: Part 1 (LLM Building Blocks)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 0.1 | What Every LLM Engineer Needs From Classical ML | COURSE-READY | |
| 0.2 | Deep Learning Essentials | COURSE-READY | |
| 0.3 | PyTorch Tensors, Autograd & Training Loop | COURSE-READY | |
| 0.4 | PyTorch Debugging, Lab & Modern Performance | COURSE-READY | |
| 0.5 | Reinforcement Learning Framework | COURSE-READY | |
| 0.5a | PPO & the RLHF Pipeline | COURSE-READY | |
| 1.1 | The Story of NLP (Four Eras) | COURSE-READY | |
| 1.2 | Text Preprocessing & From Text to Numbers | COURSE-READY | |
| 1.3 | Word Embeddings: Word2Vec, GloVe & FastText | COURSE-READY | |
| 1.4 | Contextual Embeddings & ELMo | COURSE-READY | |
| 1.4a | Contextual Embeddings Lab, BERT Pretraining & Exercises | COURSE-READY | |
| 1.5 | Why Tokenization Matters | COURSE-READY | |
| 1.6 | Subword Methods (BPE, WordPiece, Unigram) | COURSE-READY | |
| 1.7 | Special Tokens, Chat Templates & Fertility | COURSE-READY | |
| 1.8 | Multilingual Fertility & Multimodal Tokenization | COURSE-READY | |
| 2.1 | Why RNNs Couldn't Scale | COURSE-READY | |
| 2.2 | Bahdanau Additive Attention | COURSE-READY | |
| 2.3 | Q/K/V & Scaled Dot-Product Attention | COURSE-READY | |
| 2.4 | Multi-Head Attention & Quadratic Complexity | COURSE-READY | |
| 3.1 | The Transformer Architecture | COURSE-READY | |
| 3.2 | Weight Init, Causal Mask & Forward Pass | COURSE-READY | |
| 3.3 | Build a Transformer from Scratch (Lab) | COURSE-READY | |
| 3.4 | Training Loop & Tensor-Shape Trace (Lab) | COURSE-READY | |
| 3.5 | Architectural Families & Positional Encoding | COURSE-READY | |
| 3.5a | Efficient Attention, Heads & LayerNorm Placement | COURSE-READY | |
| 3.6 | GPU Fundamentals & Systems | COURSE-READY | |
| 3.7 | Transformer Expressiveness Theory | COURSE-READY | |
| 3.8 | Beyond Attention (SSMs, MoE, MLA) | COURSE-READY | |
| 4.1 | Greedy & Beam Search Decoding | COURSE-READY | |
| 4.2 | Stochastic Sampling (Temperature, Top-k/p) | COURSE-READY | |
| 4.2a | Penalties, Combining Methods & Sampling Lab | COURSE-READY | |
| 4.3 | Advanced Decoding & Structured Generation | COURSE-READY | |
| 4.4 | Diffusion-Based Text Generation | COURSE-READY | |
| 5.1 | Compute Environments (GPU tiers, local stack) | CATALOG-OK | |
| 5.2 | Core Python & ML Libraries | CATALOG-OK | |
| 5.3 | Hugging Face Transformers Inference Patterns | CATALOG-OK | |
| 5.4 | Reference Datasets for Part I | CATALOG-OK | |
| 5.5 | Reference Models for Part I | CATALOG-OK | |
| 5.6 | Courses, Blogs, Communities & Further Reading | CATALOG-OK | |

## Summary
- COURSE-READY: 32 | DEPTH-GAP: 0 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 6
- Part 1 is uniformly lecture-ready. The core mechanism is derived or faithfully sketched in every substantive section (gradient descent and cross-entropy with worked tables in 0.1; backprop with a full numeric chain-rule trace in 0.2; the variance argument for the sqrt(d_k) scaling in 2.3; the online-softmax / log-sum-exp recurrence behind FlashAttention in 3.6; the TC^0 vs universal-approximation reconciliation in 3.7; BPE-as-Shannon-coding and the Unigram/Viterbi loss in 1.6; the Boltzmann-distribution framing of temperature with the T->0 divide-by-zero caveat in 4.2; the Gibbs-sampling lineage of discrete diffusion in 4.4). Assumptions and failure modes are stated explicitly (dying ReLU, vanishing gradients, reward hacking, greedy/beam repetition attractor, double-descent caveat on bias-variance). Module 05 is an intentional tools-of-the-trade survey and is correctly scored CATALOG-OK rather than held to the derivation bar.
- Since no section falls below COURSE-READY, there is no enrichment backlog. The only marginally lighter touch among the COURSE-READY set is the information-theory primer in 3.1, which recaps entropy/cross-entropy/perplexity/KL in prose and routes the formal walk-through to Appendix A.6; it stays COURSE-READY because the four quantities are recapped in-body rather than only linked.
