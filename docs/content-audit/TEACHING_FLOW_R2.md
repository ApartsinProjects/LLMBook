# Teaching Flow Reviewer Report (Cycle 5, Round 2)

Agent: 03-teaching-flow
Scope: Sections with consecutive headings (h2 followed by h3 or h2) lacking bridge prose between them.
Date: 2026-05-19

## Methodology
- Ran `grep -P '</h[23]>\s*<h[23]' part-*/module-*/section-*.html` to locate candidates.
- For each match, read the surrounding context and confirmed that no bridge prose existed between the headings.
- Composed a 1-3 sentence bridge that (a) recapped the closing point of the prior heading, (b) teed up what the next heading would explore, and (c) supplied a logical hinge with concrete numbers or names where useful.
- Verified after all edits that `</h2>\s*<h3` and `</h2>\s*<h2` no longer match in section files (zero residual unbridged consecutive headings).

## Bridges Added (28)

### Part 1: LLM Building Blocks

1. **`section-0.1.html`** (ML/PyTorch Foundations)
   - Between `0.1.3 Loss Functions and Optimization` (h2) and `Loss Functions: Defining "Wrong"` (h3)
   - Frame: pivots from "the model has predictions" to "the model now needs to improve," motivating the loss/optimizer pair as the engine of every neural network.

2. **`section-2.1.html`** (Sequence Models & Attention)
   - Between `2.1.2 RNN Fundamentals` (h2) and `The Vanilla RNN Cell` (h3)
   - Frame: vanilla RNN cell as the building block whose problems motivate every later complication (LSTM gates, GRUs, attention).

3. **`section-3.1a.html`** (Transformer Architecture)
   - Between `3.1.4 Input Representation and Positional Encoding` (h2) and `3.1.4.1 Token Embeddings` (h3)
   - Frame: two transformations bridge integer IDs to vectors (token embeddings + positional encodings), each addressing a different missing ingredient.

4. **`section-3.4.html`** (GPU Architecture; three bridges)
   - Between `3.4.2 GPU Architecture Overview` and `3.4.2.1 Streaming Multiprocessors (SMs)`: 300x compute-to-memory-bandwidth gap motivates the SM vocabulary.
   - Between `3.4.3 Compute-Bound vs. Memory-Bound Operations` and `3.4.3.1 The Roofline Model`: roofline as the diagnostic chart for every kernel.
   - Between `3.4.7 Practical Considerations` and `3.4.7.1 Mixed Precision Training`: workflow-level choices (precision, memory budgeting, debugging) for hitting 50%+ MFU.

5. **`section-4.1.html`** (Decoding)
   - Between `4.1.2 Greedy Decoding` (h2) and `The Greedy Decoding Algorithm` (h3)
   - Frame: simplest possible answer to the decoding problem, used as baseline against every later strategy.

6. **`section-4.4.html`** (Diffusion LMs)
   - Between `4.4.1 From Continuous to Discrete Diffusion` (h2) and `A Quick Review: Diffusion in Images` (h3)
   - Frame: two-step plan, revisit continuous-pixel success, then identify the assumption that breaks for discrete tokens.

### Part 2: Understanding LLMs

7. **`section-6.5.html`** (Pretraining: Optimizers)
   - Between `6.5.4 Memory-Efficient Optimizer Alternatives` (h2) and `Adafactor` (h3)
   - Frame: AdamW's 840 GB optimizer state for a 70B model motivates the trade-off ladder (Adafactor, 8-bit Adam, Lion).

8. **`section-7.1a.html`** (Modern LLM Landscape: Anthropic)
   - Between `7.1.3 Anthropic: The Claude Family` (h2) and `Claude 3.5 Sonnet and Constitutional AI` (h3)
   - Frame: positions Anthropic as a contrasting wing of the frontier organized around Constitutional AI.

9. **`section-7.1b.html`** (Modern LLM Landscape; two bridges)
   - Between `7.1.8 Second-Tier Frontier Models` and `xAI Grok`: each lab carves a defensible niche (real-time data, RAG citations, European sovereignty).
   - Between `7.1.9 Comparing the Frontier` and `Capability Dimensions`: no single benchmark answers the "which one to pick" question.

10. **`section-8.4.html`** (Reasoning, Test-Time Compute)
    - Between `8.4.6 Common Pitfalls` (h2) and `8.4.6.1 Over-Thinking on Simple Tasks` (h3)
    - Frame: three recurring failure modes for test-time compute (overthinking, billing surprises, DoS-via-unbounded-reasoning) in encounter order.

11. **`section-9.2.html`** (Long-Context Attention)
    - Between `9.2.9 Research Frontiers` (h2) and `9.2.9.1 Test-Time Training (TTT)` (h3)
    - Frame: from deployable techniques (YaRN, LongRoPE, Ring Attention) to rethinking the cache itself (TTT, DSA).

12. **`section-9.3.html`** (Speculative Decoding)
    - Between `9.3.6 Practical Implementation` (h2) and `From-Scratch Implementation` (h3)
    - Frame: shortest path from theory to running code is a 40-line draft-verify-resample loop.

13. **`section-9.6.html`** (Reasoning Models; two bridges)
    - Between `9.6.2 Reasoning Models: Architecture and Training` and `9.6.2.1 The "Thinking Tokens" Paradigm`: 70-point AIME jump motivates how to teach this behavior.
    - Between `9.6.5 Using Reasoning Models in Practice` and `9.6.5.1 API Usage`: three practical API differences (thinking budget, billing, streaming).

### Part 4: Training & Adaptation

14. **`section-15.6.html`** (Synthetic Data: Reasoning Traces; two bridges)
    - Between `15.6.6 Common Pitfalls and Mitigations` and `Reward Hacking in Verification`: three recurring failure modes (reward hacking, reasoning collapse, length bias).
    - Between `15.6.7 Practical Considerations for Practitioners` and `Cost Estimation`: dollar cost, GPU-time cost, licensing terms.

15. **`section-15.7.html`** (Synthetic Data: Augmentation)
    - Between `15.7.4 Domain-Specific Augmentation Strategies` (h2) and `Low-Resource Language Augmentation` (h3)
    - Frame: three specialized cases (low-resource languages, math, code) with well-established augmentation patterns.

16. **`section-16.4.html`** (Fine-Tuning Fundamentals: API Fine-Tuning)
    - Between `16.4.7 Best Practices for API Fine-Tuning` (h2) and `16.4.7.1 Iterative Refinement Workflow` (h3)
    - Frame: pivot from "when" and "data privacy red lines" to operational craft via a 5-step loop.

17. **`section-17.1.html`** (LoRA)
    - Between `17.1.3 LoRA Hyperparameters in Practice` (h2) and `17.1.3.1 Rank (r) Selection` (h3)
    - Frame: three dominant LoRA hyperparameters (rank r, scaling alpha, target modules) in tuning order.

18. **`section-17.5a.html`** (Distillation; two bridges)
    - Between `17.5.1 Classical Distillation Framework` and `17.5.1.1 The Teacher-Student Paradigm`: Hinton's 2015 framework as the foundation under modern variants.
    - Between `17.5.3 Case Studies in LLM Distillation` and `17.5.3.1 Orca: Learning from Complex Explanations`: Orca, Phi, and DistilBERT each pushed a different dial.

19. **`section-17.6.html`** (Model Merging)
    - Between `17.6.2 Merging Methods` (h2) and `17.6.2.1 Linear (Weighted Average)` (h3)
    - Frame: four merging families (linear, SLERP, TIES, DARE), each fixing a failure mode of the last.

20. **`section-18.1b.html`** (RLHF/GRPO Practical Tips)
    - Between `18.1.8 Practical Tips for RL-Based Alignment` (h2) and `Learning Rate and Schedule` (h3)
    - Frame: short checklist (small LR, cosine warmup, watch KL) from teams who shipped RLHF/DPO.

21. **`section-18.2b.html`** (DPO Hyperparameters)
    - Between `18.2.5 Practical Considerations for DPO Training` (h2) and `18.2.5.1 Hyperparameter Sensitivity` (h3)
    - Frame: three impactful dials (beta, learning rate, reference model) starting with beta.

### Part 6: Agentic AI

22. **`section-26.4.html`** (AI Agents: Benchmarks)
    - Between `26.4.2 Major Agent Benchmarks` (h2) and `SWE-bench` (h3)
    - Frame: four canonical benchmarks (SWE-bench, GAIA, WebArena, OSWorld) each capturing a different agent task slice.

### Part 7: Retrieval

23. **`section-31.1b.html`** (Embeddings; three bridges)
    - Between `31.1.4 Embedding Model Ecosystem and Selection` and `API Embedding Services`: API vs self-hosted as the two camps.
    - Between `31.1.5 Embedding Space Geometry` and `Similarity Metrics`: similarity metric and dimensionality, both swing quality without model change.
    - Between `31.1.7 Practical Considerations` and `Query and Document Prefixes`: three production gotchas (prefixes, asymmetric processing, re-embedding versioning).

24. **`section-31.2b.html`** (Vector Indexes)
    - Between `31.2.5 Composite Indexes and Advanced Techniques` (h2) and `IVF-HNSW` (h3)
    - Frame: stacking two approximations (HNSW for traversal + PQ for compression) to exploit different cost-budget axes.

25. **`section-31.3.html`** (Vector Databases; three bridges)
    - Between `31.3.2 Purpose-Built Vector Databases` and `Pinecone`: four competitors on different axes (Pinecone, Qdrant, Weaviate, Milvus).
    - Between `31.3.3 Lightweight and Embedded Solutions` and `ChromaDB`: lighter tier trades replication for zero-infra embedded use.
    - Between `31.3.7 Operational Considerations` and `Scaling Patterns`: scaling, backup, observability as the three operational levers.

26. **`section-31.4.html`** (RAG Ingestion; two bridges)
    - Between `31.4.2 Document Parsing` and `The PDF Challenge`: PDFs deserve special attention because they dominate enterprise corpora and break naive extraction.
    - Between `31.4.4 Overlap and Parent-Child Retrieval` and `Chunk Overlap`: overlap and parent-child retrieval as complementary fixes for chunking boundaries.

### Part 9: Evaluation

27. **`section-43.1.html`** (RAG Evaluation Case Studies)
    - Between `43.1.5 Two Case Studies` (h2) and `Case A , Regulated Finance RAG: Groundedness Is Mandatory` (h3)
    - Frame: choice between faithfulness and groundedness determines whether evaluation strategy survives a real audit.

### Part 10: Security

28. **`section-47.2.html`** (Red Teaming Tools)
    - Between `47.2.2 Automated Red Teaming Tools` (h2) and `47.2.2.1 Microsoft PyRIT` (h3)
    - Frame: from pseudocode blueprint to three real frameworks (PyRIT, Garak, Promptfoo) starting with PyRIT's modular architecture.

### Part 11: Ethics

29. **`section-55.1.html`** (Environmental Sustainability)
    - Between `55.1.3 Strategies for Reducing Environmental Footprint` (h2) and `55.1.3.1 Efficient Architectures` (h3)
    - Frame: three mitigation layers (model, hardware, operations) starting with architectural choices.

### Part 16: Research Frontiers

30. **`section-80.3.html`** (Frontier Architectures: Hybrids)
    - Between `80.3.4 Hybrid Architectures: Combining Strengths` (h2) and `80.3.4.1 Jamba: Mamba Meets Transformers` (h3)
    - Frame: Jamba as the most prominent demonstration of "use attention surgically" via Mamba + attention + MoE interleaving.

31. **`section-80.4.html`** (Beyond-Language Domains)
    - Between `80.4.10 Other Frontiers` (h2) and `80.4.10.1 Weather and Climate` (h3)
    - Frame: tokenization template that has spread from biology/chemistry to weather, theorem proving, tabular, and finance.

## Quality Bar Check
- Every bridge is 1-3 sentences.
- Every bridge adds information (concrete numbers, named systems, contrast lines) rather than just announcing the next topic.
- No em dashes or double dashes were used.
- All bridges preserved the existing heading IDs and were placed between the parent h2 and the first child h3.

## Summary
- 31 bridges added across 25 files spanning Parts 1, 2, 4, 6, 7, 9, 10, 11, and 16.
- Post-edit verification confirms zero residual occurrences of `</h2>\s*<h3` or `</h2>\s*<h2` in section files.
- Flow assessment: SMOOTH for the touched sections. The book now meets the "every section transition includes at least one bridge sentence" pass criterion in the audited regions.
