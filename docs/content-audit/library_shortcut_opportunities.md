# Library Shortcut Opportunities Audit

Scope: Tools-of-the-Trade style sections in the new chapters - especially Ch 36, 41, 56, 61, plus the patterns-heavy chapters Ch 34, 46, 59 and the Wave 17i sections.

Goal: identify places where the prose names a concept (e.g. "rerankers", "knowledge graphs", "fairness metrics") and a one-line `<div class="callout library-shortcut">` callout with the canonical implementing library would help the reader skip from concept to practical solution. Avoid esoteric tools; only mainstream-but-advanced libraries.

Reference template (already in use, e.g. Section 32.1):
```html
<div class="callout library-shortcut">
<div class="callout-title">Library Shortcut: RecursiveCharacterTextSplitter</div>
<p>In production, prefer <code>langchain_text_splitters.RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)</code> instead of a hand-rolled window loop. It handles paragraph and sentence boundaries, falls back through a list of separators, and ships with token-aware variants for free. The hand-rolled version above is useful to see the mechanics; the library version is what you would ship.</p>
</div>
```

For each opportunity below: (a) concept being discussed, (b) suggested library + 1-line justification, (c) suggested callout placement.

---

## Chapter 34: Structured Information Extraction & NER

### Section 34.1: The Information Extraction Landscape
1. **Concept**: classical NER vs LLM-based IE comparison.  
   **Library**: `spaCy en_core_web_trf` (already named) - add a `library-shortcut` callout right after Table 34.1.1 pointing readers to spaCy 3.7+'s native transformer pipelines as the production default; cross-link to BAML/Instructor for the structured-output side.  
   **Placement**: after `<figcaption>Figure 34.1.1</figcaption>`, before the closing `</main>`.

### Section 34.2: Classical and Open Information Extraction
2. **Concept**: Open IE (Stanford OpenIE, REBEL).  
   **Library**: `gliner` or `gliclass` - 2024-2026 zero-shot NER library that often outperforms spaCy on novel entity types without retraining; underused in prose. Single-line callout right after the REBEL paragraph.  
   **Placement**: after "...REBEL bridges the gap..." paragraph in 34.2.3.1.
3. **Concept**: LLM-based Open IE with structured output (code uses `instructor` already).  
   **Library**: `instructor` (already in code, but no callout). Promote to a `library-shortcut` callout right above Code Fragment 34.2.3 so readers can skip the boilerplate.  
   **Placement**: just before `<div class="code-block-wrapper">` for Code Fragment 34.2.3.
4. **Concept**: Event extraction with Pydantic schema.  
   **Library**: `BAML` (Boundary AI) - already mentioned in 34.2.2 code (`baml_client`) but never gets a proper callout naming when to choose BAML over Instructor. Add a short library-shortcut callout naming the choice.  
   **Placement**: after Code Fragment 34.2.2 ("BAML definition file: extract_events.baml").

### Section 34.3: Hybrid IE Architectures with LLMs
5. **Concept**: Pydantic schema-driven LLM extraction with retry-on-validation-failure.  
   **Library**: `instructor` - prose explicitly uses `instructor.from_openai(OpenAI())` but never frames it as the recommended shortcut to write less boilerplate. Add a single-line library-shortcut callout.  
   **Placement**: after Code Fragment 34.3.6.

### Section 34.5: Coreference Resolution and Document Pipelines
6. **Concept**: Classical coreference (mentions `coreferee` and `neuralcoref`).  
   **Library**: `fastcoref` or `maverick-coref` - faster than `coreferee`, more accurate, both add a single `nlp.add_pipe` line to spaCy. Add a library-shortcut callout.  
   **Placement**: in 34.5.7.1 right after "spaCy integration: `coreferee` and `neuralcoref`..." bullet.
7. **Concept**: Coreference for legal contracts (real-world scenario).  
   **Library**: `LegalCoref` or domain-tuned `Allen-AI ABACUS` (more rarely used). Skip in this section (too niche) unless reader specifically asks.

---

## Chapter 36: Retrieval Tools of the Trade

The chapter already has very high library-shortcut density - most major libraries are linked. The few gaps are around adjacent libraries that would help readers skip to a complete RAG pipeline.

### Section 36.1: Platforms
8. **Concept**: Hybrid search across BM25 + dense (when the vector DB does not natively support it).  
   **Library**: `pgvector` + `pg_trgm` + `tsvector` (Postgres trigram + full-text index). The section already lists pgvector but does not show readers the canonical hybrid-on-Postgres recipe. Add a small library-shortcut callout pointing to `pgvector-haystack` integration or to the `lantern` extension.  
   **Placement**: after the "Hybrid filter performance is the single biggest production differentiator at scale" paragraph in 36.1.3.

### Section 36.2: Libraries and Frameworks
9. **Concept**: Chunking section 36.2.10 lists LangChain text-splitters, LlamaIndex node parsers, Chonkie.  
   **Library**: `semantic-text-splitter` (Rust + Python bindings) - often outperforms LangChain's text-splitter on long-form prose and is 10-50x faster. Mainstream but not yet famous. Worth a one-liner callout.  
   **Placement**: end of section 36.2.10.
10. **Concept**: Reranking - the section names BGE-Reranker, Cohere Rerank, Jina, mxbai-rerank.  
    **Library**: `rerankers` (Answer.AI) - the unified Python wrapper that lets you swap rerankers via a model string. Already implicitly mainstream but never gets a callout.  
    **Placement**: at the end of section 36.2.2 (Reranking libraries).
11. **Concept**: RAG observability with traces.  
    **Library**: `Langfuse` (already linked) - promote to a library-shortcut callout naming it as the "if you only set up one observability tool, set up this one" choice for OSS self-host.  
    **Placement**: end of 36.2.6 (Evaluation and observability libraries).
12. **Concept**: Document parsing for visually-rich PDFs.  
    **Library**: `Marker` (Vik Paruchuri / Datalab) - 2024-25 open-source PDF-to-markdown converter that often beats Unstructured.io and LlamaParse on tables. Mainstream-but-newer.  
    **Placement**: end of section 36.2.4 (Document loaders and parsers).

### Section 36.4: Models
13. **Concept**: Matryoshka truncation - section mentions every leading 2024-26 embedder is matryoshka-trained.  
    **Library**: `sentence-transformers` with `truncate_dim=` parameter, or the `MatryoshkaLoss` for training your own. Promote to a library-shortcut callout explaining how to truncate in one line of Python.  
    **Placement**: end of 36.4.7 Matryoshka and dimension tradeoffs.

---

## Chapter 41: Conversational AI Tools of the Trade

### Section 41.1: Platforms
14. **Concept**: Voice agents over Twilio telephony (mentions Vocode, LiveKit, Pipecat).  
    **Library**: `pipecat-ai` (already linked) - promote to a library-shortcut callout in 41.1.3 explaining how 30 lines of Pipecat plus a Twilio webhook = a functioning AI phone bot.  
    **Placement**: end of 41.1.3 Voice-first and realtime platforms.

### Section 41.2: Libraries and Frameworks
15. **Concept**: Conversation memory primitives (section 41.2.1 lists buffer, summary, KG, vector memories).  
    **Library**: `mem0` (already linked) and `zep-python` (already linked) - promote one of them (mem0 has OSS license and lower setup cost) to a clear library-shortcut callout for the "I want long-term memory now" reader.  
    **Placement**: at the end of 41.2.1.
16. **Concept**: Streaming chat UIs.  
    **Library**: `Vercel AI SDK` `useChat` hook (already linked, just one line per token-stream). Promote to a library-shortcut callout in 41.2.3.  
    **Placement**: end of 41.2.3 Chat UI frameworks.
17. **Concept**: Multi-provider LLM routing.  
    **Library**: `LiteLLM` (already linked). Promote to a library-shortcut callout explaining the 3-line provider-switch pattern.  
    **Placement**: in 41.2.5 (after the description of LiteLLM).
18. **Concept**: Multi-agent orchestration (mentioned in a note at the end of 41.2.7).  
    **Library**: `autogen` and `crewai` (linked). One-line shortcut callout explaining "use AutoGen for code-heavy multi-agent flows; CrewAI for role-based collaboration" would help readers skip the decision.  
    **Placement**: end of the note at 41.2.7.

### Section 41.4: Models
19. **Concept**: Open-weights chat models (Llama, Qwen, Mistral). All linked.  
    **Library**: `vLLM` or `SGLang` - both already used elsewhere in the book, but never get a library-shortcut callout in the conversational AI section, where high-throughput serving is the natural follow-on question. Add one.  
    **Placement**: at the bottom of 41.4.3 Open-weights chat models.

---

## Chapter 46: LLM-as-Judge & Automated Evaluation

### Section 46.1: Why LLM-as-Judge Matters
20. **Concept**: Pairwise comparison bias detection.  
    **Library**: `DeepEval` (already shown in an existing callout). The existing callout is already a `library-shortcut` - good. **No new callout needed here.**
21. **Concept**: LLM evaluation with custom metrics.  
    **Library**: `RAGAS` (already linked in Ch 36; not in Ch 46). Add a library-shortcut callout pointing to RAGAS's `LLMContextRecall`, `Faithfulness`, etc. as the easiest path for RAG-judge work.  
    **Placement**: end of 46.1, just before the Fun Fact.

### Section 46.2: Judge Reliability and Common Biases
22. **Concept**: G-Eval with chain-of-thought scoring.  
    **Library**: Existing `DeepEval` callout covers this - good.
23. **Concept**: Prompt-debiasing techniques.  
    **Library**: `langchain-evaluators` or `promptfoo` (which has a built-in bias scorer). Add a small library-shortcut at the end of the prose introduction to debiasing techniques.  
    **Placement**: would belong in 46.3 (Debiasing Techniques) but section currently has no closing callout - add one.

### Section 46.3: Debiasing Techniques
24. **Concept**: Open-source judge models (Prometheus 2).  
    **Library**: `prometheus-eval` (Python wrapper for the Prometheus 2 model). Already implicitly mainstream. Worth a callout naming the package, since prose only names the model.  
    **Placement**: after Code Fragment 46.3.3.

### Section 46.4: Training Judge Models
25. **Concept**: Fine-tuning a judge model (JudgeLM).  
    **Library**: `TRL` (Transformer Reinforcement Learning by HuggingFace) - already mainstream in the book elsewhere, but never tied to judge-model training here. Add a library-shortcut callout pointing to TRL's `RewardTrainer` and `DPOTrainer` as the canonical paths.  
    **Placement**: after the description of JudgeLM training pipeline.

### Section 46.5: Multi-Judge Ensembles and Production Patterns
26. **Concept**: AlpacaEval length-controlled win rate.  
    **Library**: `alpaca-eval` (already linked in the code comment but not callout). Promote.  
    **Placement**: end of section.
27. **Concept**: LLM-as-judge ensembles.  
    **Library**: `OpenAI Evals` framework (`openai-evals`). Add a library-shortcut for readers who want a battle-tested harness rather than rolling their own.  
    **Placement**: end of 46.5, before the closing `</main>`.

---

## Chapter 56: Responsible AI Tools of the Trade

### Section 56.1: Platforms
28. **Concept**: Runtime LLM safety guarding.  
    **Library**: `NeMo Guardrails` (already linked) - promote to a library-shortcut callout in 56.1.3 with the canonical 5-line Colang policy example.  
    **Placement**: end of 56.1.3 LLM-specific safety and policy runtimes.
29. **Concept**: Prompt-injection scanning at the application boundary.  
    **Library**: `llm-guard` (already linked) - promote to a library-shortcut callout naming it as the OSS default.  
    **Placement**: end of 56.1.3.

### Section 56.2: Libraries and Frameworks
30. **Concept**: Fairness metric and mitigation.  
    **Library**: `Fairlearn` (already linked) - the prose explains pick-when but does not show the 5-line `MetricFrame` example. Add a library-shortcut callout with the canonical snippet.  
    **Placement**: end of 56.2.1 Fairness metric and mitigation libraries.
31. **Concept**: LLM red-teaming and policy-violation probes.  
    **Library**: `garak` and `PyRIT` (both linked). Promote one to a library-shortcut callout showing the 3-line "run all probes" pattern.  
    **Placement**: end of 56.2.4 LLM bias and red-team suites.
32. **Concept**: Differential-privacy training.  
    **Library**: `opacus` (PyTorch DP, would be linked in 56.2.6 if not already) - add a one-liner library-shortcut for readers building DP-trained models.  
    **Placement**: in 56.2.6 (Privacy and federated-learning libraries, if present in 56.2.5+).
33. **Concept**: Watermarking text outputs.  
    **Library**: `transformers` `WatermarkingConfig` (HuggingFace shipped a SynthID-Text implementation in 2024). Add a library-shortcut showing the 3-line generate-with-watermark pattern.  
    **Placement**: in 56.2.5 Watermarking libraries.

### Section 56.3: Datasets and Benchmarks
34. **Concept**: Running BBQ / BOLD evaluations.  
    **Library**: `lm-evaluation-harness` (EleutherAI) - the canonical harness for almost every academic LLM benchmark; the section mentions HELM but lm-eval-harness is the broader-adoption one. Add a library-shortcut callout.  
    **Placement**: end of 56.3 (assuming the section lists bias datasets - confirm in the actual file).

### Section 56.4: Models (Guard models, Constitutional AI implementations)
35. **Concept**: Safety classifier models (Llama Guard 3, ShieldGemma).  
    **Library**: `transformers` with `meta-llama/Llama-Guard-3-8B`. Add a library-shortcut callout showing the canonical 5-line "classify this prompt as safe/unsafe" snippet.  
    **Placement**: end of 56.4 (verify section content).

---

## Chapter 59: Distributed Training Systems

### Section 59.1: Distributed Training Fundamentals
36. **Concept**: Communication primitives (all-reduce, all-gather).  
    **Library**: `torch.distributed` + `NCCL` (PyTorch already in the canon, but no callout). Add a library-shortcut callout in 59.1.4 showing the canonical `init_process_group` + `all_reduce` pattern.  
    **Placement**: end of 59.1.4 Collective communication primitives (verify section number).

### Section 59.2: ZeRO and FSDP
37. **Concept**: ZeRO / FSDP enablement.  
    **Library**: `accelerate` (HuggingFace) - the easiest path to FSDP without touching FSDP APIs directly. Add a library-shortcut callout: "If you just want FSDP to work, set `--num_processes=N` and `--use_fsdp` on `accelerate launch`."  
    **Placement**: end of 59.2.
38. **Concept**: Megatron-style sharding.  
    **Library**: `megatron-core` (NVIDIA) and `nanotron` (HuggingFace) - the section mentions Megatron in prose but never gives a library-shortcut. Add one explicitly naming `megatron-lm` for research and `nanotron` for hacker-friendly recipes.  
    **Placement**: in 59.2.

### Section 59.3: Tensor Parallelism
39. **Concept**: Tensor parallelism primitives (column-parallel, row-parallel matmul).  
    **Library**: `megatron.core.tensor_parallel` (already explicitly named in prose but not callout). Promote to library-shortcut.  
    **Placement**: in 59.3.7 or 59.3.8.

### Section 59.4: Pipeline Parallelism
40. **Concept**: 1F1B and interleaved pipeline schedules.  
    **Library**: `DeepSpeed` and `torch.distributed.pipelining`. Add a library-shortcut callout showing the 3-line pattern for converting an `nn.Sequential` model into a pipeline-parallel schedule.  
    **Placement**: in 59.4.

### Section 59.5: Operations
41. **Concept**: Distributed checkpointing.  
    **Library**: `torch.distributed.checkpoint` (DCP). Add a library-shortcut callout naming DCP as the "if you only use one thing, use this" for sharded checkpoint write/read.  
    **Placement**: in 59.5 near the checkpointing discussion.
42. **Concept**: Training observability.  
    **Library**: `wandb` and `mlflow` - already named in 61.1.6 but section 59.5 talks about training observability and never gives a library-shortcut. Add one.  
    **Placement**: in 59.5.

---

## Chapter 61: Scale Tools of the Trade

This chapter has lots of inline links already; the gaps are in adjacent libraries that complete the workflow.

### Section 61.1: Platforms
43. **Concept**: Slurm job submission.  
    **Library**: `submitit` (HuggingFace / Meta AI) - the canonical Python wrapper for `sbatch`. Add a library-shortcut callout showing the 5-line "submit a training job to Slurm from Python" pattern.  
    **Placement**: in 61.1.4 HPC schedulers and orchestrators, end of the Slurm bullet.

### Section 61.2: Libraries and Frameworks (verify section content)
44. **Concept**: Inference serving.  
    **Library**: `vLLM`, `SGLang`, `TensorRT-LLM` - all already named in the book. Add one consolidated library-shortcut callout: "For self-hosted inference, default to vLLM. Move to SGLang for very high QPS with prefix caching. TensorRT-LLM only if you have NVIDIA enterprise support."  
    **Placement**: in 61.2.
45. **Concept**: Distributed training launchers.  
    **Library**: `accelerate launch`, `torchrun`, `deepspeed`, `MosaicML composer`. Add one library-shortcut callout naming `accelerate` as the gentlest entry point.  
    **Placement**: in 61.2.
46. **Concept**: Inference quantization.  
    **Library**: `bitsandbytes`, `AutoGPTQ`, `AutoAWQ`, `llmcompressor` (vLLM team). Add a library-shortcut callout naming `llmcompressor` for vLLM-compatible quantization (the 2024-25 standard).  
    **Placement**: in 61.2.

### Section 61.3: Datasets and Benchmarks (verify)
47. **Concept**: Pretraining dataset filtering.  
    **Library**: `datatrove` (HuggingFace) and `nemo-curator` (NVIDIA). Add a library-shortcut callout naming `datatrove` as the OSS default for "dedupe, filter, classify" pipelines on terabyte-scale datasets.  
    **Placement**: in 61.3.

### Section 61.4: Models
48. **Concept**: Lineage browsing for open-weights models.  
    **Library**: `huggingface_hub` + the model card metadata. Add a library-shortcut callout showing the 3-line model-card download pattern for license checking before deployment.  
    **Placement**: in 61.4.

### Section 61.5: Communities / External Reading (verify)
49. **Concept**: GPU benchmarking and profiling.  
    **Library**: `nvidia-dcgm`, `nsys`, `torch.profiler`. Add a one-liner library-shortcut: "First-pass profile: `torch.profiler` plus `dcgmi dmon`. Deep dive: `nsys profile`."  
    **Placement**: in 61.5.

---

## Wave 17i Sections

### Section 24.6: VLA Limitations
50. **Concept**: Safety wrapper for a VLA (three-layer pattern).  
    **Library**: `MoveIt` (ROS 2) for collision avoidance; `Drake` (TRI / MIT) for physics-based safety envelopes. Currently treated as "your team writes this"; a single library-shortcut pointing to MoveIt Servo + collision_object API would help.  
    **Placement**: after Code Fragment 24.6.1.

### Section 24.13: Sim-to-Real Gap
51. **Concept**: Domain randomization in simulation.  
    **Library**: `Isaac Lab` (NVIDIA) and `Gymnasium` randomization wrappers. Add a library-shortcut callout naming Isaac Lab as the production-grade default for VLA sim-to-real research in 2026.  
    **Placement**: in 24.13.2.

### Section 26.6: Memory Architecture for Agents
52. **Concept**: Plan / scratchpad memory.  
    **Library**: `LangGraph` `StateGraph` typed-state fields - already implicitly the canonical implementation. Add a library-shortcut callout pointing readers to it for the "I just want a plan-step tracker" use case.  
    **Placement**: end of 26.6.2 Working Memory for Multi-Step Plans.
53. **Concept**: Agent-state checkpointing.  
    **Library**: `langgraph-checkpoint-postgres` or `langgraph-checkpoint-sqlite` - the canonical persistence path. Add a library-shortcut callout.  
    **Placement**: in 26.6's checkpointing subsection.

### Section 27.5: Retrieval as a Tool Call
54. **Concept**: Retrieval tool schema design.  
    **Library**: `pydantic` (in code) - already used implicitly. Promote to a one-line library-shortcut callout pointing to `pydantic.BaseModel` + `json_schema()` as the canonical way to ship a function-call schema.  
    **Placement**: after Code Fragment in 27.5.2 Shaping a Retrieval Tool.
55. **Concept**: Corrective RAG / CRAG / Adaptive RAG patterns in tool form.  
    **Library**: `LangGraph` plus `langchain-community.retrievers.web_research` (or `tavily-python` for web fallback). Add a library-shortcut callout for the "I want corrective grading without writing my own" reader.  
    **Placement**: in 27.5's corrective-retrieval subsection.

### Section 29.1: Code Generation Agents
56. **Concept**: SWE-bench-style code agent benchmarking.  
    **Library**: `swe-bench` and `swe-agent`. Add a library-shortcut callout in 29.1.1 (The Anatomy of a Code Agent) pointing readers to swe-agent as the reference implementation.  
    **Placement**: in 29.1.1 or 29.1.2.
57. **Concept**: Self-debug loop.  
    **Library**: `pytest` + sandbox runtime (`Docker SDK for Python`, `firejail`, or `nsjail`). Add a library-shortcut callout naming the canonical sandbox tools.  
    **Placement**: in 29.1's self-debug loop section.

### Section 29.4: Production Agentic Coding Systems
58. **Concept**: MCP (Model Context Protocol) for code tools.  
    **Library**: `mcp` Python SDK (Anthropic) - the canonical implementation for the MCP protocol. Currently mentioned but not given a library-shortcut. Add one.  
    **Placement**: in 29.4's discussion of MCP-based tool servers.

### Section 35.3: RAG with Knowledge Graphs
59. **Concept**: LLM-based knowledge-graph construction from text.  
    **Library**: `LangChain LLMGraphTransformer` and `LlamaIndex KnowledgeGraphIndex`. Add a library-shortcut callout naming LLMGraphTransformer as the easiest path: "from text to a Neo4j graph in 10 lines".  
    **Placement**: in 35.3's "LLM-based KG construction" subsection.
60. **Concept**: Cypher-based retrieval.  
    **Library**: `neo4j` Python driver + `langchain-neo4j`. Add a library-shortcut callout: "Use `Neo4jGraph(url, username, password)` + `GraphCypherQAChain` for end-to-end natural-language-to-Cypher retrieval."  
    **Placement**: in 35.3's Cypher subsection.

### Section 35.4: GraphRAG
61. **Concept**: GraphRAG community detection + summarization.  
    **Library**: `graphrag` (Microsoft) - the canonical implementation. Currently the prose names "Microsoft GraphRAG" but never explicitly tells the reader the pip-installable package name. Add a one-line library-shortcut.  
    **Placement**: at the start of 35.3 or right after the indexing pipeline description.
62. **Concept**: LazyGraphRAG and DRIFT variants.  
    **Library**: Same `graphrag` package supports both via config flags. Add a small library-shortcut callout listing the two flag options.  
    **Placement**: at the bottom of 35.3.

### Section 37.3: Memory & Context Management
63. **Concept**: Sliding window memory.  
    **Library**: `langchain.memory.ConversationBufferWindowMemory` (already linked); promote to a library-shortcut callout.  
    **Placement**: in 37.3's sliding-window subsection.
64. **Concept**: Self-managing agent memory (MemGPT/Letta).  
    **Library**: `letta` (formerly MemGPT). Add a library-shortcut callout: "`pip install letta` + a Postgres URL = persistent multi-session memory for an agent."  
    **Placement**: in 37.3's MemGPT/Letta subsection.

---

## Summary Counts

| Chapter / Section | New library shortcuts to add |
|---|---|
| Ch 34 (5 sections) | 7 |
| Ch 36 (5 sections) | 6 |
| Ch 41 (5 sections) | 6 |
| Ch 46 (5 sections) | 6 |
| Ch 56 (5 sections) | 7 |
| Ch 59 (5 sections) | 7 |
| Ch 61 (5 sections) | 7 |
| Wave 17i (9 sections) | 13 |
| **Total** | **59** |

## Highest-leverage picks (top 10 if you only ship a few)

1. **Section 34.5 `fastcoref` callout** (item 6) - the coref section names old libraries; the modern one is unmentioned.
2. **Section 36.2 `rerankers` (Answer.AI) callout** (item 10) - one-line API to swap rerankers, currently invisible.
3. **Section 36.2 `Marker` PDF parser callout** (item 12) - 2024-25 OSS that beats Unstructured on tables.
4. **Section 41.2 `mem0` callout** (item 15) - the explicit drop-in for "long-term memory now".
5. **Section 46.5 `OpenAI Evals` callout** (item 27) - readers building eval harnesses miss the official one.
6. **Section 56.2 `Fairlearn MetricFrame` snippet callout** (item 30) - one snippet teaches the whole library.
7. **Section 59.2 `accelerate launch --use_fsdp` callout** (item 37) - the easiest entry to FSDP.
8. **Section 59.4 `torch.distributed.pipelining` callout** (item 40) - the official-PyTorch path is underused.
9. **Section 35.4 `graphrag` pip-installable callout** (item 61) - prose names the technique but not the package.
10. **Section 37.3 `letta` callout** (item 64) - readers asking "how do I get memory now" deserve a direct pointer.

These ten land in sections that already discuss the concept but currently leave readers to figure out the right library on their own.

---

## Style guidance for these callouts

- Keep each callout to 2-4 sentences.
- Always name the canonical package name and the canonical 1-3 line snippet.
- Explicitly contrast with the hand-rolled version above (per the existing template style).
- Use `<code>` for package and class names.
- Match the existing `library-shortcut` callout class.
