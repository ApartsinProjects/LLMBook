# Lab Audit Report

Generated: 2026-03-28

## Task 1: Existing Lab Fragments

All dedicated lab files live in `_lab_fragments/`:

| File | Topic | Current Chapter |
|------|-------|-----------------|
| `lab-12.2.html` | Build a Self-Instruct Data Generation Pipeline | Ch 13 (Synthetic Data) |
| `lab-13.3.html` | Fine-tuning fundamentals (data prep / training loop) | Ch 14 (Fine-Tuning) |
| `lab-14.1.html` | Fine-Tune a Model with LoRA and Compare Rank Settings | Ch 15 (PEFT) |
| `lab-15.1.html` | Distillation / model merging | Ch 16 (Distillation) |
| `lab-16.2.html` | Alignment (RLHF / DPO) | Ch 17 (Alignment) |
| `lab-17.1.html` | Interpretability | Ch 18 (Interpretability) |
| `lab-18.1.html` | Embeddings / vector DB | Ch 19 (Embeddings) |
| `lab-18.4.html` | Embeddings / vector DB (advanced) | Ch 19 (Embeddings) |
| `lab-19.1.html` | RAG pipeline | Ch 20 (RAG) |
| `lab-19.2.html` | RAG (advanced retrieval) | Ch 20 (RAG) |
| `lab-20.3.html` | Conversational AI | Ch 21 (Conversational AI) |

Note: Lab fragment filenames use pre-renumber chapter numbers. The "Current Chapter" column shows the correct chapter after the restructure to 36 chapters.

No `.ipynb` notebook files exist anywhere in the repository.

Other lab-related assets:
- `agents/skills-backup-2026-03-27/46-lab-designer.md` (agent skill definition)
- `agents/07-exercise-designer.html` (agent for exercises)
- `part-1-foundations/phase2-visual-exercise-report.md` (exercise audit for Part 1)


## Task 2: Lab Coverage by Chapter

### Legend
- HAS LAB = dedicated lab fragment exists in `_lab_fragments/`
- INLINE = section files contain hands-on exercises or substantial code blocks
- NONE = no lab fragment and no substantial inline hands-on content

| Chapter | Title | Lab Fragment | Inline Exercises | Code Blocks | Status |
|---------|-------|-------------|------------------|-------------|--------|
| 00 | ML/PyTorch Foundations | none | section-0.2, 0.3, 0.4 | 28 | INLINE |
| 01 | Foundations of NLP | none | section-1.2, 1.4 | few | INLINE (light) |
| 02 | Tokenization / Subword | none | section-2.2, 2.3 | few | INLINE (light) |
| 03 | Sequence Models / Attention | none | section-3.1 | few | INLINE (light) |
| 04 | Transformer Architecture | none | section-4.1, 4.2, 4.3 | few | INLINE (light) |
| 05 | Decoding / Text Generation | none | none | 1 | NONE |
| 06 | Pretraining / Scaling Laws | none | none | 0 | NONE |
| 07 | Modern LLM Landscape | none | none | 16 | INLINE (code only) |
| 08 | Reasoning / Test-Time Compute | none | none | 0 | NONE |
| 09 | Inference Optimization | none | none | 28 | INLINE (code only) |
| 10 | LLM APIs | none | none | 29 | INLINE (code only) |
| 11 | Prompt Engineering | none | section-11.4 | 3 | INLINE (light) |
| 12 | Hybrid ML+LLM | none | none | 25 | INLINE (code only) |
| 13 | Synthetic Data | lab-12.2 | none | 19 | HAS LAB |
| 14 | Fine-Tuning Fundamentals | lab-13.3 | section-14.3 | 28 | HAS LAB |
| 15 | PEFT (LoRA) | lab-14.1 | none | 14 | HAS LAB |
| 16 | Distillation / Merging | lab-15.1 | none | 10 | HAS LAB |
| 17 | Alignment (RLHF/DPO) | lab-16.2 | none | 17 | HAS LAB |
| 18 | Interpretability | lab-17.1 | section-18.2 | 25 | HAS LAB |
| 19 | Embeddings / Vector DB | lab-18.1, lab-18.4 | section-19.1 | 23 | HAS LAB |
| 20 | RAG | lab-19.1, lab-19.2 | section-20.1 | varies | HAS LAB |
| 21 | Conversational AI | lab-20.3 | none | 19 | HAS LAB |
| 22 | AI Agents | none | none | 3 | NONE |
| 23 | Tool Use & Protocols | none | none | 0 | NONE |
| 24 | Multi-Agent Systems | none | none | 0 | NONE |
| 25 | Specialized Agents | none | none | 0 | NONE |
| 26 | Agent Safety & Production | none | none | 0 | NONE |
| 27 | Multimodal | none | none | 0 | NONE |
| 28 | LLM Applications | none | none | 3 | NONE |
| 29 | Evaluation / Observability | none | none | 0 | NONE |
| 30 | Observability / Monitoring | none | none | 0 | NONE |
| 31 | Production Engineering | none | none | 0 | NONE |
| 32 | Safety / Ethics / Regulation | none | section-32.1 | 5 | INLINE (light) |
| 33 | Strategy / Product / ROI | none | section-33.3 | 6 | INLINE (light) |
| 34 | Emerging Architectures | none | none | 0 | NONE |
| 35 | AI and Society | none | none | 0 | NONE |


## Task 3: Lab Outlines for Chapters Missing Labs

### Chapter 00: ML/PyTorch Foundations
- Build a mini neural network from scratch in PyTorch (forward pass, loss, backprop)
- Train a simple classifier on a toy dataset, plot training curves
- Compare SGD vs. Adam optimizers; visualize gradient flow
- Checkpoint the model, reload, and verify reproducibility

### Chapter 01: Foundations of NLP / Text Representation
- Implement bag-of-words and TF-IDF from scratch using only NumPy
- Build a word2vec skip-gram model on a small corpus with Gensim
- Visualize word embeddings with t-SNE; test analogy arithmetic (king - man + woman)
- Compare dense vs. sparse representations on a text classification task

### Chapter 02: Tokenization / Subword Models
- Train a BPE tokenizer from scratch on a custom corpus using `tokenizers` library
- Compare tokenization outputs across GPT-2, LLaMA, and multilingual models
- Measure vocabulary coverage and unknown-token rates on domain-specific text
- Visualize how subword merges evolve during training

### Chapter 03: Sequence Models / Attention
- Implement a basic self-attention mechanism from scratch in PyTorch
- Build a minimal RNN language model, then swap in attention; compare perplexity
- Visualize attention weight heatmaps for sample sentences

### Chapter 04: Transformer Architecture
- Code a single Transformer encoder block from scratch (multi-head attention, FFN, LayerNorm)
- Verify output matches `nn.TransformerEncoderLayer` from PyTorch
- Experiment with positional encoding variants (sinusoidal vs. learned)
- Profile memory and compute for different sequence lengths

### Chapter 05: Decoding / Text Generation
- Implement greedy, top-k, top-p, and temperature sampling from logits
- Compare output diversity across strategies on the same prompt
- Build a simple beam search decoder; measure BLEU against reference text
- Visualize token probability distributions at each decoding step

### Chapter 06: Pretraining / Scaling Laws
- Reproduce a mini scaling-law experiment: train tiny GPT-2 models at 3 sizes on the same data
- Plot loss vs. compute, loss vs. parameters, and loss vs. tokens
- Estimate the compute-optimal allocation using Chinchilla ratios

### Chapter 07: Modern LLM Landscape
- Query 3 different open-source models (e.g., Llama, Mistral, Phi) via the same prompt set
- Compare outputs on reasoning, coding, and creative tasks with a rubric
- Profile inference speed and memory footprint for each model

### Chapter 08: Reasoning / Test-Time Compute
- Compare chain-of-thought prompting vs. standard prompting on math and logic tasks
- Implement a simple self-consistency strategy (sample N responses, majority vote)
- Measure accuracy gains from increased test-time compute budget

### Chapter 09: Inference Optimization
- Quantize a model with bitsandbytes (4-bit and 8-bit); compare latency and perplexity
- Serve a model with vLLM; benchmark throughput under concurrent requests
- Implement basic KV-cache reuse and measure speedup on long contexts

### Chapter 10: LLM APIs
- Build a rate-limited, retry-aware API client for OpenAI (or compatible endpoint)
- Implement streaming responses and token counting
- Compare structured output extraction with and without the Instructor library
- Add basic cost tracking and logging per request

### Chapter 11: Prompt Engineering
- Implement zero-shot, few-shot, and chain-of-thought prompts for a classification task
- Build a prompt template system with variable injection and output parsing
- Test prompt sensitivity: measure accuracy variance from minor rephrasing
- Implement a self-reflection loop where the model critiques and revises its answer

### Chapter 12: Hybrid ML+LLM
- Build a pipeline that uses a traditional ML classifier as a router, dispatching to an LLM only for hard cases
- Compare latency and cost of the hybrid approach vs. LLM-only baseline
- Implement a confidence-based fallback mechanism

### Chapter 22: AI Agents
- Build a ReAct agent loop from scratch: thought, action, observation cycle
- Implement two tools (web search mock + calculator) and wire them into the agent
- Add a simple memory/scratchpad for multi-step reasoning
- Test on 5 tasks; log tool-call traces and measure success rate

### Chapter 23: Tool Use & Protocols
- Implement an MCP server with two tools and connect it to an agent
- Build a tool registry that dynamically discovers and loads tools
- Compare function-calling approaches across different API providers

### Chapter 24: Multi-Agent Systems
- Create a two-agent debate system where agents argue opposing positions and a judge picks the winner
- Implement a supervisor/worker pattern with task delegation
- Measure quality improvement of multi-agent vs. single-agent on a summarization task

### Chapter 25: Specialized Agents
- Build a code-generation agent with iterative testing and self-repair
- Implement a research agent that searches, summarizes, and synthesizes from multiple sources

### Chapter 26: Agent Safety & Production
- Implement sandboxed tool execution with permission boundaries
- Build a human-in-the-loop approval gate for high-risk agent actions
- Test agent guardrails against adversarial task descriptions

### Chapter 27: Multimodal
- Use a vision-language model to caption images and answer visual questions
- Build a document-AI pipeline: OCR + LLM extraction of structured fields from invoices
- Compare pipeline (OCR then LLM) vs. native multimodal model accuracy

### Chapter 28: LLM Applications
- Build a code-review assistant that reads a diff and produces inline comments
- Implement a summarization pipeline with extractive pre-filtering and abstractive generation
- Create a simple Q&A chatbot with Gradio as the front end

### Chapter 29: Evaluation / Observability
- Implement BLEU, ROUGE, and BERTScore evaluation on a summarization dataset
- Build an LLM-as-judge evaluator and measure inter-rater agreement with human labels
- Set up basic tracing with Langfuse: log prompts, completions, latencies, and costs

### Chapter 30: Observability / Monitoring
- Set up a drift-detection dashboard using token-distribution statistics
- Implement alerting on latency and error-rate thresholds for a served model
- Build a logging pipeline that captures prompt/response pairs with metadata

### Chapter 31: Production Engineering
- Containerize a model-serving endpoint with Docker and a simple health check
- Implement a circuit-breaker pattern for LLM API calls
- Set up a blue/green deployment simulation with two model versions
- Load-test with concurrent users and measure p50/p95/p99 latencies

### Chapter 32: Safety / Ethics / Regulation
- Build a content-moderation pipeline: classify inputs with a safety model, block or flag harmful content
- Implement a model card generator that documents capabilities, limitations, and bias audits
- Red-team a chatbot: craft adversarial prompts and evaluate guardrail effectiveness

### Chapter 33: Strategy / Product / ROI
- Build a cost calculator that estimates monthly spend from token volumes and model choice
- Create a decision matrix comparing build-vs-buy for 3 hypothetical use cases
- Design an A/B test framework for comparing two LLM configurations on user satisfaction

### Chapter 34: Emerging Architectures
- Compare inference characteristics of a state-space model (Mamba) vs. a Transformer on a sequence task
- Benchmark a linear-attention variant on long-context inputs

### Chapter 35: AI and Society
- Audit a model for demographic bias using a fairness benchmark
- Build a transparency report template for an LLM deployment


## Task 4: Library/Tool Coverage Gaps

### Serving Frameworks

| Tool | Mentioned? | Files | Code Examples? | Recommended Chapter |
|------|-----------|-------|---------------|---------------------|
| vLLM | Yes (31 files) | Chapters 5, 7, 9, 10, 15, 18, 29, 31, 33 | Some | Good coverage |
| SGLang | Yes (10 files) | Chapters 5, 9, 10, 18 | Minimal | Chapter 9 should add code example |

### Structured Output

| Tool | Mentioned? | Files | Code Examples? | Recommended Chapter |
|------|-----------|-------|---------------|---------------------|
| Instructor | Yes (16 files) | Chapters 5, 10, 11, 12, 14, 21, 27, 28 | Some | Good coverage |
| Outlines | Yes (16 files) | Chapters 5, 9, 10, 13, 14, 17, 18, 19, 21, 22, 28, 33 | Minimal | Chapter 10 should add code example |

### Observability

| Tool | Mentioned? | Files | Code Examples? | Recommended Chapter |
|------|-----------|-------|---------------|---------------------|
| LangSmith | Yes (10 files) | Chapters 11, 12, 20, 24, 29, 33 | Minimal | Chapter 29 should add code walkthrough |
| Langfuse | Yes (7 files) | Chapters 24, 29, 31 | Minimal | Chapter 29 should add code walkthrough |

### Agent Frameworks

| Tool | Mentioned? | Files | Code Examples? | Recommended Chapter |
|------|-----------|-------|---------------|---------------------|
| CrewAI | Yes (7 files) | Chapters 10, 11, 24, 33 | Minimal | Chapter 24 should add code example |
| Smolagents | Yes (3 files) | Chapter 24 | None | Chapter 22 or 24 should add code example |

### Fine-Tuning Tools

| Tool | Mentioned? | Files | Code Examples? | Recommended Chapter |
|------|-----------|-------|---------------|---------------------|
| Unsloth | Yes (5 files) | Chapter 15 | Minimal | Chapter 15 should add code walkthrough |
| Axolotl | Yes (5 files) | Chapters 14, 15 | Minimal | Chapter 14 should add config-file example |

### Vector Databases

| Tool | Mentioned? | Files | Code Examples? | Recommended Chapter |
|------|-----------|-------|---------------|---------------------|
| ChromaDB | Yes (10 files) | Chapters 19, 20, 33 | Some | Adequate |
| Qdrant | Yes (10 files) | Chapters 12, 19, 20, 31, 33 | Some | Adequate |

### UI Frameworks

| Tool | Mentioned? | Files | Code Examples? | Recommended Chapter |
|------|-----------|-------|---------------|---------------------|
| Gradio | Yes (5 files) | Chapters 7, 29, 31 | Minimal | Chapter 28 (Applications) or 31 should add code example |
| Chainlit | Yes (3 files) | Chapter 31 | None | Chapter 21 (Conversational AI) or 28 should add code example |

### Summary of Gaps

**Tools with no code examples (need additions):**
1. **Smolagents**: Add to Chapter 22 (AI Agents) or 24 (Multi-Agent), with a minimal agent example
2. **Chainlit**: Add to Chapter 21 (Conversational AI) or 28 (Applications), with a chat UI example
3. **SGLang**: Add to Chapter 9 (Inference Optimization), with a serving/constrained-decoding snippet

**Tools with only textual mentions (need code walkthroughs):**
4. **Langfuse**: Chapter 29 (Evaluation/Observability), add a tracing setup example
5. **LangSmith**: Chapter 29 (Evaluation/Observability), add a tracing setup example
6. **CrewAI**: Chapter 24 (Multi-Agent Systems), add a crew definition example
7. **Unsloth**: Chapter 15 (PEFT), add a fast LoRA training example
8. **Axolotl**: Chapter 14 (Fine-Tuning), add a YAML config example
9. **Gradio**: Chapter 28 (Applications), add a demo app example
10. **Outlines**: Chapter 10 (LLM APIs), add a constrained-generation code snippet


## Overall Recommendations

1. **Chapters 00 through 12 and 22 through 35 have zero dedicated lab files.** The _lab_fragments directory only covers Chapters 13 through 21 (using pre-renumber filenames). Priority should go to creating labs for the highest-enrollment parts: Chapters 00 (PyTorch), 10 (APIs), 11 (Prompting), 22 (Agents), and 29 (Evaluation).

2. **Part I (Foundations, Chapters 00 through 05)** has decent inline exercises in some sections but no standalone labs. These chapters are the most hands-on friendly and would benefit most from structured lab files.

3. **Part VI (Agentic AI, Chapters 22 through 26)** is the weakest area: minimal code blocks and no labs. Given the practical nature of these topics, this is the biggest gap.

4. **Parts VIII and IX (Evaluation/Production/Safety/Strategy, Chapters 29 through 33)** are more conceptual by nature, but at least Chapter 31 (Production Engineering) should have a deployment lab.

5. **Part X (Frontiers, Chapters 34 through 35)** are new chapters that need both content and lab coverage.

6. **No Jupyter notebooks exist.** Consider whether `.ipynb` files would complement the HTML lab fragments for download/execution.
