# Appendix C-N Consolidation Plan

**Author**: Architecture planning pass, 2026-05-16
**Status**: DESIGN (no files moved yet)

---

## Investigation summary

### Tools-of-the-Trade chapter map (verified)

Every part owns one ToT chapter. All twelve use the same five-section template: 1=Platforms, 2=Libraries & Frameworks, 3=Datasets & Benchmarks, 4=Models, 5=External Reading & Communities.

| Part | Module | ToT title | Approx size (lines) |
| ---- | ------ | --------- | ------------------- |
| 1 Foundations | module-06 | Foundations Stack | 576 total |
| 2 Understanding LLMs | module-12 | Models & Tokenizers | ~580 |
| 3 Working with LLMs | module-16 | LLM API Stack | ~560 |
| 4 Training & Adapting | module-21 | Training & Adaptation Stack | ~620 |
| 5 Retrieval & Conversation | module-25 | Retrieval & Conversation Stack | ~620 |
| 6 Agentic AI | module-30 | Agent Stack | ~600 |
| 7 Multimodal & Generation | module-33 | Multimodal Stack | ~580 |
| 8 Evaluation & Production | module-36 | Eval & Production Stack | ~620 |
| 9 Safety & Security & Ethics | module-39 | Safety & Guardrails Stack | ~620 |
| 10 Idea-to-Product | module-50 | Idea-to-Product Toolkit | ~640 |
| 11 Applications Across Industries | module-60 | Industry Solution Stack | ~620 |
| 12 Frontiers | module-65 | Frontier Research Stack | ~640 |

Each ToT chapter is currently a short *reference card* (5 sections at 65-140 lines each) that one-line-mentions tools with links and frequently defers depth to "see Appendix X". Example: section 21.2 already says "Appendix J covers W&B and MLflow wiring."

### Appendix C-N section inventory

| Appendix | Sections | Total lines | Section list |
| -------- | -------- | ----------- | ------------ |
| C HuggingFace Ecosystem | 5 | 1,820 | C.1 Transformers (Models, Pipelines, AutoClasses); C.2 Datasets & Tokenizers; C.3 Trainer & Accelerate; C.4 PEFT & TRL; C.5 Hub & Spaces |
| D LangChain | 5 | ~1,500 | D.1 Core Abstractions (Models, Prompts, Chains); D.2 Memory; D.3 Document Loaders/Retrievers; D.4 Output Parsers; D.5 Agents, Tools, Callbacks |
| E Orchestration Frameworks | 3 | ~800 | E.1 Orchestration overview (LangChain/LlamaIndex/Haystack/DSPy); E.2 LlamaIndex deep dive; E.3 Haystack & DSPy |
| F Agent Frameworks | 3 | ~870 | F.1 Agent frameworks survey (LangGraph/CrewAI/AutoGen/Agents SDK/Semantic Kernel/smolagents/PydanticAI); F.2 Multi-Agent Patterns; F.3 Production Agent Deployment |
| G Python for LLM | 4 | ~790 | G.1 Essential Libraries; G.2 Virtual Envs/Dependency Mgmt; G.3 Jupyter/Colab; G.4 LLM scripting patterns |
| H Environment Setup | 8 | 1,055 | H.1 Hardware; H.2 CUDA & Drivers; H.3 CUDA-to-PyTorch wheels; H.4 Installing Key Libraries; H.5 Cloud Options; H.6 IDE Setup; H.7 API Keys & Secrets; H.8 Verifying Setup |
| I Git Collaboration | 4 | ~700 | I.1 Git Basics for ML; I.2 DVC; I.3 Linking Runs to Commits; I.4 Reproducibility & CI/CD |
| J Experiment Tracking | 5 | ~1,160 | J.1 W&B; J.2 MLflow; J.3 Experiment Compare & HPO; J.4 Model Registry & Deployment; J.5 LLM Eval Dashboards |
| K Inference Serving | 5 | ~1,600 | K.1 vLLM; K.2 TGI; K.3 SGLang; K.4 Quantization (GPTQ/AWQ/GGUF); K.5 Scaling & Load Balancing |
| L Data Engineering | 4 | ~1,765 | L.1 PySpark for LLM Data; L.2 Delta Lake / Lakehouse; L.3 Feature Stores (Feast/Tecton/Databricks FE); L.4 Production Pipelines |
| M Distributed ML | 4 | ~1,470 | M.1 Distributed Training (DDP/FSDP/ZeRO/PP/TP); M.2 Databricks Workspace/Unity Catalog; M.3 Databricks AI & Foundation Models; M.4 Ray Train/Serve/Data |
| N MLOps | 5 | ~620 | N.1 Observability for LLM Systems; N.2 Monitoring & Drift; N.3 Deployment Patterns; N.4 Model Registry & Lifecycle; N.5 SLOs/Alerting/FinOps |

**Approximate cross-reference count** in part content (excluding audit reports, KDP build logs, and TOC): ~58 hrefs across 52 part-section HTML files. Adding internal links from index/toc, the rewritable surface is ~70-90 hrefs. Audit-report mentions and KDP build artifact mentions push the raw count over 1,200 but those are not user-facing book content.

---

## Section A — Mapping table (current location → proposed new home)

| Appx | Section | Topic | Natural home (part) | Destination ToT module | Overlap w/ current ToT |
| ---- | ------- | ----- | ------------------- | ---------------------- | ---------------------- |
| C.1 | Transformers (pipelines/AutoClasses) | Inference & usage | Part 2 (Understanding LLMs) | module-12 §12.2 already one-lines `transformers` | Yes — 12.2 lists `transformers` & `accelerate` |
| C.2 | Datasets & Tokenizers | Data + tokenization | Part 1 (Foundations) for tokenizers OR Part 4 (Training) for datasets | module-06 §6.2 / module-21 §21.3 | 6.2 names `datasets` & `tokenizers` |
| C.3 | Trainer & Accelerate | Training | Part 4 (Training) | module-21 §21.2 | 21.2 already names accelerate, TRL |
| C.4 | PEFT & TRL | PEFT/RLHF | Part 4 (Training) | module-21 §21.2 | 21.2 names TRL and shows GRPOTrainer |
| C.5 | Hub & Spaces | Sharing/versioning | Part 1 or Part 4 | module-06 §6.1 Platforms (or 21.1) | 6.1 names HF Hub |
| D.1 | LangChain Core (Models/Prompts/Chains) | API orchestration | Part 3 (Working with LLMs) | module-16 §16.2 | 16.2 lists LangChain |
| D.2 | LangChain Memory | Conversation memory | Part 5 (Conversation) | module-25 §25.2 | 25.2 lists memory libs |
| D.3 | Document Loaders / Retrievers | RAG | Part 5 (RAG) | module-25 §25.2 | 25.2 lists LangChain retrievers |
| D.4 | Output Parsers | Structured output | Part 3 (LLM APIs) | module-16 §16.2 | Light mention |
| D.5 | LC Agents / Tools / Callbacks | Agents | Part 6 (Agents) — *legacy* | module-30 §30.2 (mark as legacy) | 30.2 already calls LC Agents "mostly legacy" |
| E.1 | Orchestration overview | RAG orchestration | Part 5 | module-25 §25.2 | Yes |
| E.2 | LlamaIndex deep dive | RAG | Part 5 | module-25 §25.2 | Yes |
| E.3 | Haystack & DSPy | RAG/prompting | Part 5 (Haystack) + Part 3 (DSPy prompt optimization) — split | module-25 §25.2 + module-16 §16.2 | Yes |
| F.1 | Agent frameworks survey | Agents | Part 6 | module-30 §30.2 | Yes — 30.2 already surveys them |
| F.2 | Multi-Agent Patterns | Agents | Part 6 | module-30 §30.2 *or* into chapter 28 prose | Partially in §28 |
| F.3 | Production Agent Deployment | Agent ops | Part 8 (Production) | module-36 §36.2/§36.3 | Yes — 36.2 has observability SDKs |
| G.1 | Essential libraries | Foundations | Part 1 | module-06 §6.2 | Heavy overlap |
| G.2 | Virtual envs / dependency mgmt | Setup | Part 1 | module-06 §6.1 (Platforms) | Some |
| G.3 | Jupyter / Colab | Notebooks | Part 1 | module-06 §6.1 | Some |
| G.4 | Common LLM scripting patterns | Patterns | Part 1 | module-06 §6.2 / §6.4 | None |
| H.1 | Hardware | Setup | Part 1 | module-06 §6.1 (Platforms) | Light |
| H.2-H.3 | CUDA & drivers / wheels | Setup | Part 1 | module-06 §6.1 | None |
| H.4 | Installing Key Libraries | Setup | Part 1 | module-06 §6.1/§6.2 | Light |
| H.5 | Cloud Options | Setup | Part 1 | module-06 §6.1 | Yes — 6.1 has platforms |
| H.6 | IDE setup | Setup | Part 1 | module-06 §6.1 | Light |
| H.7 | API keys & secrets | Setup | Part 3 (where users first call APIs) | module-16 §16.1 | None |
| H.8 | Verifying setup | Setup | Part 1 | module-06 §6.5 | None |
| I.1 | Git basics for ML | Workflow | Part 1 | module-06 §6.1 | None |
| I.2 | DVC | Data versioning | Part 4 (Training data) | module-21 §21.3 | None |
| I.3 | Linking runs to commits | Experiment tracking | Part 4 | module-21 §21.2 | None |
| I.4 | Reproducibility & CI/CD | Production | Part 8/10 | module-36 or module-50 §50.2 | None |
| J.1 | W&B | Experiment tracking | Part 4 (training) | module-21 §21.2 | One-line mention |
| J.2 | MLflow | Experiment tracking | Part 4 | module-21 §21.2 | One-line mention |
| J.3 | Experiment compare / HPO | Tracking | Part 4 | module-21 §21.2 | None |
| J.4 | Model registry & deployment | MLOps | Part 8 | module-36 §36.2 | Some |
| J.5 | LLM eval dashboards | Eval/observability | Part 8 | module-36 §36.2 (observability SDKs) | Heavy overlap with LangSmith/Langfuse/Phoenix list already there |
| K.1 | vLLM | Inference serving | Part 2 (Inference Optimization) | module-12 §12.2 | One-line |
| K.2 | TGI | Inference serving | Part 2 | module-12 §12.2 | None |
| K.3 | SGLang | Inference serving | Part 2 | module-12 §12.2 | None |
| K.4 | Quantization for serving | Inference | Part 2 | module-12 §12.2 | Yes — bitsandbytes listed |
| K.5 | Scaling/load balancing | Production | Part 8 or Part 10 | module-36 §36.2 OR module-50 §50.2 | None |
| L.1 | PySpark | Data engineering | Part 4 (training data) | module-21 §21.3 | None |
| L.2 | Delta Lake / Lakehouse | Data | Part 4 | module-21 §21.3 | None |
| L.3 | Feature stores | Data | Part 4 / Part 8 | module-21 §21.3 | None |
| L.4 | Production pipelines / serving at scale | Production | Part 8/10 | module-36 §36.2 / module-50 §50.2 | None |
| M.1 | Distributed training (DDP/FSDP/ZeRO/TP/PP) | Training | Part 4 | module-21 §21.2 | Light |
| M.2 | Databricks workspace / Unity Catalog | Platform | Part 4 (training) | module-21 §21.1 (Platforms) | None |
| M.3 | Databricks AI & Foundation Models | Platform | Part 4 | module-21 §21.1 | None |
| M.4 | Ray Train/Serve/Data | Distributed | Part 4 (Train) + Part 8 (Serve) | module-21 §21.2 + module-36 §36.2 | None |
| N.1 | Observability for LLM Systems | Eval/observability | Part 8 | module-36 §36.2 | Heavy (LangSmith/Langfuse/Phoenix/Helicone already there) |
| N.2 | Monitoring & drift | Production | Part 8 | module-36 §36.2 | Some |
| N.3 | Deployment patterns | Production | Part 8 / Part 10 | module-50 §50.2 (Idea-to-Product) | Some |
| N.4 | Model registry & lifecycle | MLOps | Part 8 | module-36 §36.2 | Overlap with J.4 |
| N.5 | SLOs, alerting, FinOps | Production | Part 8 / Part 10 | module-50 §50.2 | None |

---

## Section B — Strategies evaluated

### Strategy 1 — Fold each appendix wholesale into its single best-matching ToT chapter

**Concrete picture**: Appendix C (5 sections, 1,820 lines) becomes new sections 6.6-6.10 *or* 21.6-21.10. Appendix J (5 sections, 1,160 lines) becomes 21.6-21.10. Appendix N (5 sections, 620 lines) becomes 36.6-36.10. Each appendix preserves its internal coherence.

**Pros**

- Migration is mechanical: rename `section-c.N.html` → `section-X.(5+N).html`, fix headers, fix breadcrumbs, fix cross-refs.
- Readers who currently bookmark "Appendix C" still find a single contiguous block.
- Preserves the original authoring voice and pedagogy of each appendix.
- Internal cross-refs *within* each appendix (e.g. C.3 references C.1) remain trivial to rewrite — same module.

**Cons**

- ToT chapters BALLOON. The current ToT-Foundations is 576 lines across 6 files. Adding Appendix C (1,820), G (790), H (1,055), I (700) → ~4,365 lines or **~10x**. ToT becomes the longest chapter in Part 1, longer than the chapters it summarizes.
- Each ToT chapter's existing 5-section schema (Platforms / Libraries / Datasets / Models / External Reading) breaks down: Appendix C.1 "Transformers Library" doesn't fit *any* of those slots cleanly — it's a deep dive, not a card.
- Forces an awkward two-tier ToT chapter: §6.1-6.5 are reference cards, §6.6+ are full tutorials. Reader's mental model collapses.
- Several appendices serve **multiple parts** (M splits training/serving; D spans Parts 3/5/6; K splits Parts 2/8). Whole-appendix consolidation forces a choice that's wrong for ~30% of the material.
- The existing one-line mentions in ToT §X.2 become duplicates of the moved deep-dive sections.

### Strategy 2 — Distribute appendix sections across the part(s) where they're actually used

**Concrete picture**: Appendix C.1 (Transformers) goes to Part 2 module-12 as new §12.6. C.2 splits — tokenizer half to module-06 §6.6, dataset half to module-21 §21.6. C.3 (Trainer/Accelerate) to module-21 §21.6 or §21.7. C.4 (PEFT/TRL) to module-21 §21.8. C.5 (Hub) to module-06 §6.6 as platforms deep dive. Sections live near where they're first needed.

**Pros**

- Content lives next to the chapter that motivates it. A reader hitting PEFT (chapter 19) finds the deep-dive in the same Part's ToT, not three Parts away in an appendix.
- ToT chapter growth is bounded — each part gets only what's relevant to it (typically 2-4 new sections each, not 8-12).
- Matches how ToT chapters are *already* written: they're the natural reference home for the part's stack.
- Cross-refs simplify — instead of "see Appendix J for W&B" we get "see §21.6" (same part).
- Appendices D, E, F deduplicate naturally: orchestration framework material lands once in Part 5 ToT (module-25); agent framework material once in Part 6 ToT (module-30); LangChain "Agents" subsection becomes a sidebar inside Part 6's framework survey because it's already legacy.

**Cons**

- Migration is more complex: each section needs an individual destination decision and individual renumbering.
- Reader who wants "everything about LangChain" loses a single landing page (mitigation: keep an appendix index stub that hot-links to the distributed sections — see Section D below).
- Some sections legitimately cut two ways (M.4 Ray Train+Serve, L.4 production pipelines+serving). Each requires a judgement call or a split.
- Higher cross-reference rewrite cost — ~58 hrefs to retarget rather than just renaming.

### Recommendation: **Strategy 2 (Distribute)**.

Reasoning: the ToT chapters are *already* the part-local reference home, and they *already* one-line each tool with a link out. Strategy 2 collapses each "one-line + link to appendix" into one consolidated section in the same chapter. ToT chapter size grows ~2-3x (manageable) rather than ~10x. The pedagogical principle "content lives where it's first needed" matches the author's stated goal. Cross-reference rewriting is mechanical (Python regex over part HTML), not hard. The single drawback — losing the per-appendix landing page — is fixed by retaining a one-page appendix stub that lists "this content has moved; see…" with deep links.

---

## Section C — Per-appendix migration plan

### Appendix C — HuggingFace Ecosystem → Parts 1/2/4

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| C.1 Transformers | Models/Pipelines/AutoClasses | Part 2 / module-12 | section-12.6.html "HuggingFace Transformers Deep Dive" |
| C.2 Datasets & Tokenizers | Loading/preprocess/stream | Split: tokenizer half → Part 1 / module-06 §6.6, dataset half → Part 4 / module-21 §21.6 | section-6.6.html "HuggingFace Tokenizers Deep Dive"; section-21.6.html "HuggingFace Datasets Deep Dive" |
| C.3 Trainer & Accelerate | Training | Part 4 / module-21 | section-21.7.html "Trainer & Accelerate" |
| C.4 PEFT & TRL | PEFT/RLHF | Part 4 / module-21 | section-21.8.html "PEFT & TRL Deep Dive" |
| C.5 Hub & Spaces | Hub | Part 1 / module-06 | section-6.7.html "HuggingFace Hub" (Platforms-adjacent) |

Folder fate: delete `appendices/appendix-c-huggingface-ecosystem/` after migration; preserve a redirect stub (see Section D).

### Appendix D — LangChain → Parts 3/5/6

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| D.1 Core (Models/Prompts/Chains) | LangChain core | Part 3 / module-16 | section-16.6.html "LangChain Core" |
| D.2 Memory | Conversation memory | Part 5 / module-25 | section-25.6.html "LangChain Memory" |
| D.3 Document loaders/retrievers | RAG building blocks | Part 5 / module-25 | section-25.7.html "LangChain Document Loaders & Retrievers" |
| D.4 Output parsers | Structured output | Part 3 / module-16 | section-16.7.html "LangChain Output Parsers" |
| D.5 Agents/Tools/Callbacks | Legacy agent loop | Part 6 / module-30 | section-30.6.html "LangChain Agents (Legacy) & Callbacks" |

Delete `appendix-d-langchain/`.

### Appendix E — Orchestration Frameworks → Part 5 (+ Part 3 for DSPy)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| E.1 Orchestration overview | LC/LI/Haystack/DSPy | Part 5 / module-25 | section-25.8.html "Orchestration Framework Overview" |
| E.2 LlamaIndex deep dive | LI | Part 5 / module-25 | section-25.9.html "LlamaIndex Deep Dive" |
| E.3 Haystack & DSPy | Haystack + DSPy | Split: Haystack → §25.10, DSPy → Part 3 §16.8 "DSPy: Programmatic Prompting" | section-25.10.html; section-16.8.html |

Delete `appendix-e-orchestration-frameworks/`.

### Appendix F — Agent Frameworks → Part 6 (+ Part 8 for production)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| F.1 Agent frameworks survey | LangGraph/CrewAI/AutoGen/SDK/SK/smolagents/PydanticAI | Part 6 / module-30 | section-30.7.html "Agent Frameworks Deep Dive" — merges with existing §30.2 prose |
| F.2 Multi-Agent Patterns | Topologies in practice | Part 6 / module-30 | section-30.8.html "Multi-Agent Patterns" |
| F.3 Production Agent Deployment | Obs/cost/guardrails | Part 8 / module-36 | section-36.6.html "Production Agent Deployment" |

Delete `appendix-f-agent-frameworks/`.

### Appendix G — Python for LLM → Part 1

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| G.1 Essential libraries | NumPy/SciPy/pandas | Part 1 / module-06 | section-6.8.html "Essential Python Libraries Deep Dive" — merge w/ §6.2 |
| G.2 Virtual envs / deps | uv/poetry/conda | Part 1 / module-06 | section-6.9.html "Virtual Environments & Dependency Management" |
| G.3 Jupyter / Colab | Notebooks | Part 1 / module-06 | section-6.10.html "Jupyter & Colab" |
| G.4 LLM scripting patterns | Patterns | Part 1 / module-06 | section-6.11.html "Common LLM Scripting Patterns" |

Delete `appendix-g-python-for-llm/`.

### Appendix H — Environment Setup → Part 1 (+ Part 3 for keys)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| H.1 Hardware | GPU/RAM/disk | Part 1 / module-06 | section-6.12.html "Hardware Requirements" |
| H.2 CUDA & drivers | NVIDIA | Part 1 / module-06 | section-6.13.html "CUDA & Driver Setup" |
| H.3 CUDA-to-PyTorch wheels | Linking | Part 1 / module-06 | section-6.14.html "Linking CUDA to PyTorch" |
| H.4 Installing key libraries | Install | Part 1 / module-06 | section-6.15.html "Installing Key Libraries" |
| H.5 Cloud options | Lambda/RunPod/Modal etc. | Part 1 / module-06 | section-6.16.html "Cloud Compute Options" |
| H.6 IDE setup | VS Code/PyCharm | Part 1 / module-06 | section-6.17.html "IDE & Editor Integrations" |
| H.7 API keys & secrets | Keys | Part 3 / module-16 | section-16.9.html "API Keys & Secrets Management" |
| H.8 Verifying setup | Smoke tests | Part 1 / module-06 | section-6.18.html "Verifying Your Setup" |

Note: module-06 expands from 5→18 sections — heavy. Mitigation: rename §6.1 Platforms split into "Platforms (existing card)" and group the 12 new sections as a clearly-titled "Setup & Environment Deep Dive" subgroup using H2 headers within the chapter index. Alternative: keep H.1-H.6, H.8 as a *separate* dedicated chapter, e.g. promote it to a new "Chapter 6b: Environment Setup" *before* ToT — but that creates renumbering pressure on Part 1.

Delete `appendix-h-environment-setup/`.

### Appendix I — Git Collaboration → Part 1 (+ Part 4 + Part 10)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| I.1 Git basics for ML | Git | Part 1 / module-06 | section-6.19.html "Git Basics for ML Projects" |
| I.2 DVC | Data versioning | Part 4 / module-21 | section-21.9.html "Data Version Control (DVC)" |
| I.3 Linking runs to commits | Tracking | Part 4 / module-21 | section-21.10.html "Linking Experiment Runs to Git Commits" |
| I.4 Reproducibility & CI/CD | CI/CD | Part 10 / module-50 | section-50.6.html "Reproducibility & CI/CD for ML" |

Delete `appendix-i-git-collaboration/`.

### Appendix J — Experiment Tracking → Part 4 (+ Part 8)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| J.1 W&B | Tracking | Part 4 / module-21 | section-21.11.html "Weights & Biases Deep Dive" |
| J.2 MLflow | Tracking | Part 4 / module-21 | section-21.12.html "MLflow Deep Dive" |
| J.3 Experiment compare & HPO | HPO | Part 4 / module-21 | section-21.13.html "Experiment Comparison & HPO" |
| J.4 Model registry & deployment | Registry | Part 8 / module-36 | section-36.7.html "Model Registry & Deployment Workflows" |
| J.5 LLM eval dashboards | LLM obs | Part 8 / module-36 | section-36.8.html "LLM Evaluation Dashboards" — merge w/ existing §36.2 obs-SDK list |

Delete `appendix-j-experiment-tracking/`.

### Appendix K — Inference Serving → Part 2 (+ Part 8)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| K.1 vLLM | Serving | Part 2 / module-12 (or module-10 if positioning by use) | section-12.7.html "vLLM Deep Dive" |
| K.2 TGI | Serving | Part 2 / module-12 | section-12.8.html "Text Generation Inference (TGI)" |
| K.3 SGLang | Structured gen | Part 2 / module-12 | section-12.9.html "SGLang" |
| K.4 Quantization for serving | GPTQ/AWQ/GGUF | Part 2 / module-12 | section-12.10.html "Quantization for Serving" |
| K.5 Scaling & load balancing | Scaling | Part 8 / module-36 | section-36.9.html "Inference Scaling & Load Balancing" |

Delete `appendix-k-inference-serving/`.

### Appendix L — Data Engineering → Part 4 (+ Part 8)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| L.1 PySpark | Data | Part 4 / module-21 | section-21.14.html "PySpark for LLM Data Pipelines" |
| L.2 Delta Lake / Lakehouse | Data | Part 4 / module-21 | section-21.15.html "Delta Lake & Lakehouse" |
| L.3 Feature stores | Feast/Tecton | Part 4 / module-21 | section-21.16.html "Feature Stores" |
| L.4 Production pipelines | Pipelines + serving | Part 8 / module-36 | section-36.10.html "Production Data Pipelines & Serving at Scale" |

Delete `appendix-l-data-engineering/`.

### Appendix M — Distributed ML → Part 4 (+ Part 8)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| M.1 Distributed training | DDP/FSDP/ZeRO/TP/PP | Part 4 / module-21 | section-21.17.html "Distributed Training Deep Dive" |
| M.2 Databricks workspace | Platform | Part 4 / module-21 | section-21.18.html "Databricks Workspace & Unity Catalog" — could fold into §21.1 Platforms instead |
| M.3 Databricks AI & FM | Platform | Part 4 / module-21 | section-21.19.html "Databricks AI & Foundation Models" |
| M.4 Ray Train/Serve/Data | Distributed | Split: Train → §21.20; Serve+Data → Part 8 §36.11 "Ray Serve & Ray Data" | section-21.20.html; section-36.11.html |

Delete `appendix-m-distributed-ml/`.

### Appendix N — MLOps → Part 8 (+ Part 10)

| Old section | Title | New home | New slug |
| ----------- | ----- | -------- | -------- |
| N.1 Observability for LLM Systems | Obs | Part 8 / module-36 | section-36.12.html "LLM System Observability" — merge w/ §36.2 obs-SDK list |
| N.2 Monitoring & drift | Monitoring | Part 8 / module-36 | section-36.13.html "Monitoring & Drift Detection" |
| N.3 Deployment patterns | Deployment | Part 10 / module-50 | section-50.7.html "Deployment Patterns" |
| N.4 Model registry & lifecycle | Registry | Part 8 / module-36 | section-36.14.html — *or merge with §36.7 (from J.4)* |
| N.5 SLOs / alerting / FinOps | Ops | Part 10 / module-50 | section-50.8.html "SLOs, Alerting & FinOps" |

Delete `appendix-n-mlops/`.

### Resulting ToT chapter section counts after migration

- module-06 (Part 1): 5 → 19 sections (+G, +H1-6+H8, +I.1)
- module-12 (Part 2): 5 → 10 sections (+C.1, +C.2 tokenizer split, +K.1-K.4)
- module-16 (Part 3): 5 → 9 sections (+D.1, +D.4, +E.3 DSPy half, +H.7)
- module-21 (Part 4): 5 → 20 sections (+C.2 dataset half, +C.3, +C.4, +I.2-I.3, +J.1-J.3, +L.1-L.3, +M.1-M.4 train half)
- module-25 (Part 5): 5 → 10 sections (+D.2, +D.3, +E.1, +E.2, +E.3 Haystack half)
- module-30 (Part 6): 5 → 8 sections (+D.5, +F.1, +F.2)
- module-36 (Part 8): 5 → 14 sections (+F.3, +J.4, +J.5, +K.5, +L.4, +M.4 serve half, +N.1, +N.2, +N.4)
- module-50 (Part 10): 5 → 8 sections (+I.4, +N.3, +N.5)
- module-33, module-39, module-60, module-65: unchanged

**Hot spots: module-06 (19) and module-21 (20)** are uncomfortably long. Mitigations: (a) split Part 1's environment-setup material into a sibling chapter module-06b "Environment & Workflow" (Part 1 module-renumber-light); (b) accept the size, since these are reference chapters readers skim, not read straight through; (c) group sections under intra-chapter H2 subheaders in the index page ("Core Tools" / "Environment Setup" / "Workflow & Git").

---

## Section D — What stays at appendix layer?

Confirmed: appendices A, B, O, P, Q, R, S, T all stay as appendices.

| Appx | Why it stays |
| ---- | ------------ |
| A Mathematical Foundations | Cross-cutting reference for all parts. No single "Tools" chapter is the right home for linear algebra/probability/calculus/info theory. |
| B ML Essentials | Same — foundational reference referenced from many chapters. |
| O Docker / Containers | Cross-cutting; touches Parts 4 (training images), 8 (production), 10 (shipping). Could arguably split, but ~4 sections lose more coherence than they gain. Keep at appendix. |
| P Course Syllabi | Pedagogical wrapper — explicitly course-shaped, not tool-shaped. |
| Q Reading Pathways | Navigational meta-doc. |
| R Intermediate Projects | Project briefs that cut across parts. |
| S Capstone Project | Cross-cutting integrated project. |
| T War Stories | Pedagogical narrative material, not reference. |

Open question for the author: Appendix O (Docker) is borderline. Containerization is closer to "Tools" than to "Mathematical Foundations." It could fold into module-50 (Part 10 Idea-to-Product) Tools-of-the-Trade. Recommend **defer**: revisit O after the C-N consolidation lands and you observe how Part 10 ToT shaped up.

---

## Section E — Renumbering & URL impact

### Letter-gap vs cascade

**Option E1: Letter-gap (no renumber).** A, B, O, P, Q, R, S, T retain their letters. Letters C-N become unused. Reader sees "Appendix A, B, O, P, Q, R, S, T" — a jump that looks like content was excised. Cheapest: only delete folders + redirect stubs; no renaming of existing appendices.

**Option E2: Cascade (renumber).** A, B remain. O→C, P→D, Q→E, R→F, S→G, T→H. Result: 8 contiguous appendices A-H. Requires: (a) rename 6 folders; (b) rewrite ~? hrefs to the cascaded ones; (c) rename all `section-o.N.html` → `section-c.N.html`, all `section-p.N.html` → `section-d.N.html`, etc.

**Recommend E1 (letter-gap)** for the *first* cascade, with an explicit note in `appendices/index.html` explaining the gap ("Appendices C–N were consolidated into part-specific Tools of the Trade chapters in v12; see redirect stubs"). Reasons: the renumber cost is high (every cross-ref to O.4 becomes a new letter), the gap is self-explanatory once explained once, and it makes git history clearer. A future v13 can do the cascade renumber when the dust settles.

### Redirect stubs

For each deleted appendix folder, keep a single `appendices/appendix-X-<topic>/index.html` stub (zero section files) with:

1. A "this content has moved" banner.
2. A 5-15 row table mapping old section slug → new section URL.
3. A meta refresh tag pointing to the most-likely-needed destination if the user lands on `/appendix-c-huggingface-ecosystem/`.

This preserves bookmarks and old SEO links (Pagefind index, Google links from the public-facing book site).

---

## Section F — Cross-reference rewrite

### Scope

- **~58 hrefs to `appendices/appendix-{c..n}-…/`** in part HTML files (book content).
- **~22 hrefs in TOC and appendix indices** (`toc.html`, `appendices/index.html`, inter-appendix references).
- **~30+ hrefs internal to the appendices themselves** (e.g. C.3 → C.1, K.5 → K.4) — these become *intra-module* hrefs after migration (e.g. `section-21.7.html` → `section-21.6.html`) and so are *easier* to rewrite (same-folder relatives).
- **~10 hrefs in `front-matter/` and `index.html`** (book home).
- **Audit reports and KDP build artifacts** (~600+ raw mentions) — these are historical/derivative and should NOT be rewritten; they're snapshots.

### Approximate total to rewrite: 100-120 hrefs.

### Rewrite mapping table

A single CSV `migration-map.csv` with columns `old_href, new_href` drives the rewrite. Example rows:

```
appendices/appendix-c-huggingface-ecosystem/index.html,part-2-understanding-llms/module-12-tools-of-the-trade/section-12.6.html
appendices/appendix-c-huggingface-ecosystem/section-c.1.html,part-2-understanding-llms/module-12-tools-of-the-trade/section-12.6.html
appendices/appendix-c-huggingface-ecosystem/section-c.2.html,part-4-training-adapting/module-21-tools-of-the-trade/section-21.6.html
appendices/appendix-c-huggingface-ecosystem/section-c.3.html,part-4-training-adapting/module-21-tools-of-the-trade/section-21.7.html
…
```

Relative-path resolution must respect the source file's depth — a file at depth 2 (`part-4-training-adapting/module-21-tools-of-the-trade/section-21.7.html`) refers to a destination at the same depth with `../../module-12-tools-of-the-trade/section-12.6.html` etc. A migration script should compute relative paths from `migration-map.csv` absolute paths.

---

## Section G — Migration script outline

A four-stage Python script `scripts/migrate_appendix_c_to_n.py` (no code, just structure):

**Stage 0 — Dry-run & inventory**

- Parse `book_structure.yaml` to confirm the proposed mapping is internally consistent.
- Build `migration-map.csv` from the per-appendix table in Section C.
- Glob all `**/*.html` in the book root, classify each as "part content / appendix content / toc / index / front-matter / build artifact / audit report".
- Emit a JSON report `reports/migration-dryrun.json` listing every href that will change.

**Stage 1 — Copy and renumber section files**

- For each row in `migration-map.csv` whose source is a `section-?.N.html`:
  - Read source.
  - Rewrite `<h1>`, `<title>`, `<meta description>`, breadcrumb (`<div class="page-breadcrumb">`), `Section X.N` markers, `data-pagefind-meta` chapter/part injections.
  - Rewrite intra-appendix relative hrefs to new intra-module relative hrefs.
  - Write to destination directory.
- Detect collisions (two sources mapping to the same destination) — fail loudly.

**Stage 2 — Rewrite index pages**

- For each affected ToT chapter index (`module-XX/index.html`): regenerate the "Sections in This Chapter" `<a class="section-card">` block from the new section count.
- For each affected ToT chapter index: regenerate `<h2>What Comes Next</h2>` block if needed.
- For each deleted appendix folder: write a redirect-stub `index.html` (Section E).

**Stage 3 — Rewrite cross-references book-wide**

- Walk every `.html` outside `KDP/`, `appendices-duplication-audit.md`, `*-audit.md`, `*-report.md`.
- For each `href` matching one of the old paths in `migration-map.csv`: compute the new relative path from the source file's location and rewrite.
- Update `toc.html`: delete C-N entries, link appendix O-T directly, optionally re-letter (Option E2).
- Update `appendices/index.html`: same.
- Update `book_structure.yaml`: remove C-N entries, add new section nodes to the appropriate modules.

**Stage 4 — Validation**

- Re-run any existing link checker (`scripts/check-internal-links.py` or similar).
- Run `pagefind` index regeneration.
- Confirm no broken hrefs (each href resolves to an existing file).
- Optional: regenerate the KDP build to confirm html2epub still produces a valid EPUB.

---

## Section H — Risks

### Content collisions

1. **Tools-of-the-Trade §X.2 already mentions the appendix tools.** Migration must merge, not duplicate. Example: §21.2 already lists `accelerate`, `trl`, `peft`. Importing C.3 (Trainer & Accelerate) and C.4 (PEFT & TRL) verbatim creates duplication. **Mitigation**: each migration includes a *merge* step where the destination's existing one-line mention is replaced by a forward link to the new deep-dive section, e.g. "`accelerate`: multi-GPU/multi-node loader. → See §21.7 for a deep dive."
2. **§36.2 already enumerates LangSmith/Langfuse/Phoenix/Helicone.** Appendix N.1 also covers observability for LLM systems. **Mitigation**: when merging N.1 into module-36, the existing §36.2 entries become a "summary table" and N.1 becomes the canonical reference subsection. Verify no fact contradicts the other.
3. **J.4 and N.4 both cover model registry.** Likely partial duplication. **Mitigation**: read both before migration; merge into a single §36.7 "Model Registry & Lifecycle".
4. **§30.2 already says "LangChain Agents is mostly legacy"** which is what D.5 covers. Importing D.5 alongside is fine if D.5 is positioned as the historical reference, but the framing must be consistent.

### Section-count balance

Already noted in Section C: module-06 grows to 19 sections (4x), module-21 grows to 20 (4x), module-36 grows to 14 (3x). Reader-experience risk: a "chapter" no longer reads as a chapter. Mitigations: (a) group sections under intra-chapter H2 dividers in the index page; (b) split very large chapters into two sister chapters (e.g., module-06 → 06a Foundations Stack + 06b Environment Setup); (c) accept it (these are reference chapters).

### Reader navigation impact

- Bookmarked `appendices/appendix-c-huggingface-ecosystem/` URLs break. **Mitigation**: redirect stubs (Section E).
- The "Appendix C" naming convention disappears for moved content. Anyone who knows the appendix label loses recognition. **Mitigation**: appendix redirect stub names the new home; a deprecation note in front-matter explains the v12 reorganization.
- Pagefind search index needs regeneration; saved-search results may surface deleted pages. **Mitigation**: regenerate pagefind index as part of Stage 4.
- KDP / EPUB build (16th edition is the current target): the EPUB TOC entries change. **Mitigation**: rebuild KDP output; bump edition number to 16th.

### Authoring / merge-conflict risk

- Other parallel edits to ToT chapters during migration will conflict. **Mitigation**: lock ToT chapters and appendices C-N to migration-only edits for the duration of the cascade.

### Build pipeline risk

- The `html2epub` toml config may have explicit appendix C-N references for ordering. **Mitigation**: audit `html2epub.toml` and `book_structure.yaml` as part of Stage 0.

### Hot links from outside

- The public book site (per BOOK_CONFIG.md) is indexed by search engines on appendix C-N URLs. **Mitigation**: HTTP 301 redirects (in the hosting layer) parallel to in-book redirect stubs. Out of scope of this migration script but worth noting.

---

## Acceptance criteria for the migration when executed

1. All section files originally under `appendices/appendix-{c..n}-…/section-?.N.html` exist at their new ToT-chapter location with rewritten titles, breadcrumbs, and slugs.
2. Every appendix C-N folder contains only a redirect-stub `index.html` (no section files) OR is fully deleted (decision pending).
3. No href in book content (excluding audit reports and KDP build logs) resolves to a deleted file.
4. Each affected ToT chapter's `index.html` lists the new section count correctly under "Sections in This Chapter".
5. `pagefind` regenerates without error.
6. `toc.html` reflects the new structure.
7. `book_structure.yaml` reflects the new structure.
8. The EPUB build (`html2epub`) succeeds end-to-end.

---

### Critical Files for Implementation

- `E:/Projects/BookBlogsHome/LLMBook/book_structure.yaml`
- `E:/Projects/BookBlogsHome/LLMBook/toc.html`
- `E:/Projects/BookBlogsHome/LLMBook/appendices/index.html`
- `E:/Projects/BookBlogsHome/LLMBook/html2epub.toml`
- `E:/Projects/BookBlogsHome/LLMBook/part-4-training-adapting/module-21-tools-of-the-trade/index.html` (largest growth — bellwether)
