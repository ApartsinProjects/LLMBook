# Appendices Duplication Audit

## Summary
- Appendices scanned: 21 (A through U; 104 HTML files including index pages)
- New duplications flagged: 16 major, 9 minor
- Cross-group leakage: 7 confirmed
- Concept duplication clusters: 6 (MLflow Registry, Observability/Prometheus, Vector Search, Multi-Model Serving, Information Theory, Capstone descriptions)

Earlier audits (Framework Guides C/D/E/F/G and R&D Infrastructure H/I/J/K) were already actioned and are NOT repeated here. This report focuses on **Production Infrastructure (L/M/N/O/P)**, **For-Instructors (Q/R/S/T/U)**, **A/B (Foundations) internal duplication**, and **cross-group leakage** discovered during the scan.

Most damaging finding overall: **Appendices M and N still have stale page-current labels** (`Section M.3`, `Section M.4`, `Section M.5`, `Section M.6`, `Section M.7`, `Section O.3.x`, `Section O.4.x`, `Section O.5.x`, `Section O.6.x`, `Section O.7.x`) that point to the wrong appendix. The content of M/N appears to have been refactored from a single old appendix without renumbering, and the result is heavy thematic overlap with O (MLOps) and L (Inference Serving).

---

## Production Infrastructure group (L/M/N/O/P) - first pass

### 1. M.4 "Production Data Pipelines" duplicates most of Appendix O (MLOps)
**File:** `appendices/appendix-m-data-engineering/section-m.4.html` (466 lines, labeled `Section M.7` in page-current)

M.4 has six H2 sections (still numbered `O.7.1` through `O.7.6`) that are now redundant with the dedicated O appendix:

| M.4 sub-section | Duplicates in O |
|---|---|
| O.7.1 End-to-End Pipeline Architecture | O.3 Deployment Patterns + O.4 Lifecycle |
| O.7.2 Pipeline Orchestration with Airflow | O.3.3 GitOps and Progressive Delivery |
| O.7.3 Data Validation with Great Expectations | (NEW — not in O; KEEP in M, only fit) |
| O.7.4 CI/CD for ML: Automated Model Evaluation | O.3 Deployment Patterns + O.4.5 Lifecycle |
| O.7.5 Multi-Model Serving Architecture | Direct overlap with N.4 (Ray Serve) + L.5 |
| O.7.6 Observability and Monitoring | **Verbatim category overlap with O.1, O.2, O.5** |

The O.7.6 block in M.4 includes ~80 lines of `prometheus_client` Counter/Histogram code that is the same conceptual material as O.1.1 (LLM observability pillars), O.1.2 (OpenLLMetry), and O.5.3 (FinOps cost attribution). M.4 also includes a `Prometheus alerting` discussion that duplicates O.5.2 ("Alerting, Error Budgets").

### 2. L.5 (Scaling and Load Balancing) overlaps O.5 (SLOs/FinOps) and O.1 (Observability)
**Files:** `appendix-l-inference-serving/section-l.5.html` and `appendix-o-mlops/section-o.5.html` + `section-o.1.html`

L.5 covers (a) "GPU Utilization Monitoring" with `pynvml` and Prometheus-format export, (b) "Benchmarking Throughput", (c) "Cost Optimization Strategies" with autoscaling. These overlap with:
- O.1.3 (observability tool landscape) and O.5.2 (Prometheus Alertmanager rules)
- O.5.4 "2024-2026 Cost Optimization Toolkit" (vendor caching, batch APIs, quantization, continuous batching) — L.5.6 ("Cost Optimization Strategies") and O.5.4 are nearly the same list.

The shared sentences: both reference vLLM continuous batching + quantization + autoscaling for cost reduction. **L.5 should focus only on serving-layer scaling (replicas, tensor parallel sharding, in-process queuing) and defer FinOps/observability to O.**

### 3. P.4 (Containerizing Inference Servers) overlaps L.1 + L.2 + L.4
**File:** `appendix-p-docker-containers/section-p.4.html`

P.4 has eight H2s. The first three (vLLM in Docker / TGI in Docker / Ollama in Docker) re-present the same `docker run` commands shown in L.1 (vLLM serving) and L.2 (TGI Docker Deployment). Specifically:
- P.4 §1 `docker run vllm/vllm-openai:latest --model meta-llama/Llama-3.1-8B-Instruct` mirrors L.1 §1.
- P.4 §2 `docker run ghcr.io/huggingface/text-generation-inference:2.4` mirrors **L.2 §2 verbatim** (`section-l.2.html` lines 64–71). Same model, same flags, same volume mount, with only the tag version differing (2.4 vs latest).
- P.4 §6 "Running Quantized Models in Containers" overlaps L.4 (Quantization for Serving) and L.2 §4 (Quantization Options).

L.2 already has its own "2.1 Docker Compose for Persistent Deployments" sub-section with a full compose YAML that is materially the same pattern shown in P.3 (Docker Compose for Multi-Service AI).

### 4. N.4 (Ray Serve) overlaps L.5 + M.4 §5 Multi-Model Serving
**File:** `appendix-n-distributed-ml/section-n.4.html` (still labeled `Section M.5`, sections `O.5.x`)

N.4 §O.5.5 "Ray Serve: Production Model Serving" defines a `RAGPipeline` Ray Serve deployment with vLLM. M.4 §O.7.5 "Multi-Model Serving Architecture" defines `GenerationModel`/`EmbeddingModel`/`Router` Ray Serve deployments with vLLM and sentence-transformers. Two appendices, both showing `@serve.deployment` + vLLM, with overlapping autoscaling-config discussion.

L.5 also references the same vLLM serving stack for the scaling story. **Recommendation: Ray Serve patterns belong in N (distributed compute primitive). Pure deployment-orchestration multi-model patterns belong in O.3 (Deployment Patterns).**

### 5. N.2, N.3 are Databricks content that pre-dates the new N theme
**Files:** `appendix-n-distributed-ml/section-n.2.html`, `section-n.3.html`

Both have stale breadcrumbs pointing to "Appendix M: Distributed ML: PySpark, Databricks, and Ray" and page-current labels `Section M.3` and `Section M.4`. The content (Databricks Workspace, Unity Catalog, MLflow on Databricks, Mosaic AI, Foundation Model APIs, Databricks Vector Search, RAG on Databricks) is a coherent Databricks-platform chapter — but it is filed under N "Distributed ML" whose theme is *parallelism strategies* (N.1 = DDP/FSDP/ZeRO/PP/TP). 

N.2/N.3 thus create overlap on three axes:
- **MLflow:** N.2 §O.3.4 "MLflow Integration on Databricks" + N.3 §O.4.4 "MLflow for LLM Lifecycle Management" + K.2 (MLflow Experiment Tracking) + K.4 §M.4.4 "MLflow Model Registry in Depth" + O.4 "Model Registry and Lifecycle" = five places where MLflow API is introduced.
- **Vector Search:** N.3 §O.4.5 "Databricks Vector Search" + N.3 §O.4.6 "Building RAG Applications on Databricks" overlap with D.3 (LangChain RAG) and Ch 23.
- **Model Serving:** N.2 §O.3.5 "Databricks Model Serving" overlaps with L (Inference Serving) and N.4 §O.5.5 (Ray Serve).

### 6. M vs N: feature stores vs distributed feature serving
**Files:** `appendix-m-data-engineering/section-m.3.html` (Feature Stores: Feast/Tecton/Databricks FE) and N (Distributed ML)

Direct overlap is light, but M.3 §O.6.5 "Databricks Feature Engineering" duplicates the Databricks-centric framing that already saturates N.2 and N.3. There is no separate "distributed feature serving" section in N (the work is done by Feast online stores in M.3 and by Ray Serve in N.4 — these connect but do not duplicate).

### 7. M.4 vs O.3 deployment-flavored overlap
**Files:** `appendix-m-data-engineering/section-m.4.html` and `appendix-o-mlops/section-o.3.html`

M.4 §O.7.4 "CI/CD for ML: Automated Model Evaluation" is the same conceptual unit as O.3.3 "GitOps and Progressive Delivery on Kubernetes" and O.4.5 "Real-World Cases" (Databricks Unity Catalog + MLflow lifecycle). The eval-harness-in-CI pattern is then also in K.5 §M.5.3 "MLflow Evaluate for LLMs".

---

## For-Instructors (Q/R/S/T/U) - first pass

### 8. Q (Course Syllabi) vs R (Reading Pathways)
**Files:** `appendix-q-course-syllabi/index.html` (272 lines), `appendix-r-reading-pathways/index.html` (211 lines)

The two are mostly complementary (Q = formal courses with weekly schedules and capstones; R = self-directed pathways by goal). Real overlap is in the audience taxonomy:

| Q track | R pathway it duplicates |
|---|---|
| Track 2 (Undergrad Research) + Track 4 (Grad Research) | R.4 "Researcher / Graduate Student" |
| Track 5 (Professional Bootcamp) | R.1 "RAG Engineer" + R.2 "Agent Builder" combined |
| Q "Course Instructor" use-case (implicit) | R.7 "Course Instructor" |

R.7 explicitly says "Appendix Q (Course Syllabi)" is the next step for instructors — so the cross-reference is correctly established. However, R.4 and Q Track 2/4 share the same chapter list (Ch 0-5 foundations, Ch 7 scaling, Ch 11 interpretability) with little added value. The Q footer also has a broken link `appendices/appendices/appendix-r-reading-pathways/index.html` (line 229; double "appendices" path).

### 9. Q track 3/5 capstones vs T (Capstone Project) tracks
**Files:** `appendix-q-course-syllabi/index.html` and `appendix-t-capstone-project/index.html`

Q Track 3 capstone: "Multi-agent system with retrieval-augmented generation, an evaluation harness running in CI, deployment with monitoring, cost caps, and a rollback path." 
T Track A: "End-to-end LLM application: data pipeline, retrieval, fine-tuned PEFT model, agent orchestration, eval harness, deployment, monitoring."

Q Track 5 capstone: "Production-ready agentic application... agent with tools, retrieval over a real corpus, evaluation harness, monitoring, cost controls, and a written architecture document."
T Track B: "Same scope as Track A but model adaptation via prompt engineering + RAG instead of weight updates."

Q Track 4 capstone ("Original research project") = T Track C ("Research replication") with slightly different deliverable framing.

**Q is the source-of-truth for course-specific capstones (per-track); T is the source-of-truth for the standalone three-track capstone with rubric. The capstone definitions in Q should reference T's tracks instead of re-defining them.**

### 10. S (Intermediate Projects) vs T (Capstone) vs Q
S is the only place that defines the "1-2 week" intermediate projects (Tokenizer Comparison, Prompt Engineering Pipeline, RAG with Failure-Mode Diagnosis) — no duplication found. **S is cleanly differentiated.**

### 11. U (War Stories) cross-references are well-managed
U references Air Canada, Chevy Watsonville, Bing/Sydney, Samsung, $12K fintech bill. The Air Canada and $12K fintech stories are also referenced in O.1 (warning) and O.5 (postmortem). All references in O.x are explicit backrefs to U. **U is correctly the authoritative location.**

---

## Cross-group leakage

### 12. PEFT/LoRA introduction
**Locations:** C.4 (Section C.4 "PEFT and TRL: Parameter-Efficient Fine-Tuning and RLHF") + N.3 §O.4.1 (Mosaic AI Composer) + Q/R/T capstone references + 35 files mention LoRA/PEFT.

C.4 already opens with a cross-reference to Ch 19 (PEFT) — no remediation needed there. The N.3 leakage is the Databricks-Mosaic-AI section that introduces Composer for fine-tuning, including LoRA-style configs. **Recommendation: N.3 should reference C.4 for the PEFT mechanics rather than show its own LoRA-flavored Composer config.**

### 13. MLflow `import mlflow` / `mlflow.start_run` / `mlflow.log_model`
**Locations:** K.2 (Section M.2 "MLflow Experiment Tracking") + K.4 (Model Registry) + M.2 (Delta Lake §O.2.6 with `mlflow.log_param("delta_version")`) + N.3 (§O.4.4 "MLflow for LLM Lifecycle Management") + O.4 (Model Registry and Lifecycle).

Five appendices touch MLflow. K is meant to be the authoritative location for *experiment-side* MLflow; O.4 is the *registry/lifecycle* canonical. M.2 and N.3 are leakage. **Recommendation: M.2 keeps one `mlflow.log_param` example as a callout pointing to K.2; N.3 §O.4.4 should be deleted or condensed to a backref to O.4.**

### 14. Prometheus + Grafana
**Locations:** L.2 (TGI /metrics endpoint mention), L.5 (full GPU-metrics pynvml + Prometheus integration), M.4 §O.7.6 (prometheus_client Counter/Histogram), O.1 (observability), O.5 (Alertmanager rules).

L.2 only mentions Prometheus-format endpoint (one sentence). L.5 is the heavy serving-side monitoring section. M.4 §O.7.6 is the duplicate. O.1 + O.5 are the canonical application-level + alerting story.
**Recommendation:** L.5 keeps the GPU/serving-specific story with a backref to O.1 for application metrics. M.4 §O.7.6 should be deleted; the Prometheus code lives in O.1/O.5.

### 15. Multi-model RAG/Serving Python pattern (`Router` + `Generator` + `Embedder` Ray Serve)
**Locations:** M.4 §O.7.5 (Multi-Model Serving) + N.4 §O.5.5 (Ray Serve) + L.5 (Cost Optimization §6).

M.4 §O.7.5 defines a `GenerationModel` + `EmbeddingModel` + `Router` Ray Serve composition. N.4 §O.5.5 defines `LLMDeployment` + `RAGPipeline`. These are different code snippets but the same teaching example. **Pick one location — N.4 is the more natural fit (Ray-native).**

### 16. `vllm/vllm-openai:latest` docker invocation
**Locations:** L.1 (vLLM Install via Docker), L.2 (TGI Docker, contrast), L.5 (Cost Optimization), N.4 (uses `vllm.LLM` inside Ray Serve actor), P.4 §1 (vLLM in Docker), I.4 (vLLM install).

I.4 has a section "Installing vLLM" which arguably belongs in L.1 not I (Environment Setup). I.4's vLLM section duplicates L.1's installation discussion.

### 17. Information Theory in Appendix A: TWO sections cover the same material
**Files:** `appendix-a-mathematical-foundations/section-a.4.html` ("Information Theory") and `section-a.6.html` ("Information Theory for Language Models").

A.4 covers: Entropy, Cross-Entropy, KL Divergence, Mutual Information.
A.6 covers: Entropy (4.1.2.1), Cross-Entropy (4.1.2.2), Perplexity (4.1.2.3), KL Divergence (4.1.2.4), Mutual Information (4.1.2.5), code examples (4.1.2.6), visualizations and comparison table.

A.6 even labels itself "originated as a section of Chapter 04 (Transformer Architecture) but was moved here". A.6 has stale outline numbering `4.1.2.x`. **A.4 and A.6 are duplicate appendix sections that should be merged into one.**

### 18. Perplexity coverage between A and B
**Files:** A.6 §4.1.2.3 "Perplexity: An Intuitive Scorecard" and B.4 §"Perplexity: A Deeper Look".

Both define perplexity = exp(cross-entropy). A.6 should keep the introductory mathematical framing; B.4 should keep the ML-evaluation framing and reference A.6. Today B.4 introduces perplexity without referencing A.

### 19. `wandb.init`/`mlflow.log_model` "as a one-liner" in H.1
**File:** `appendix-h-python-for-llm/section-h.1.html`

H.1 §Package Table includes wandb. Critically, H.1 lines 286-288 already include a "wandb in Practice" callout that explicitly backrefs to K.1. **This is a model of how the leakage should be handled** — the package is listed for recognition only, with a backref to the canonical home. Use this same pattern for the MLflow/Ray/Prometheus mentions in M.4/N.3/N.4.

---

## Concept duplication clusters

### A. Tokenization
Discussed in: A.1 (one paragraph), C.1 (HF tokenizers), C.4 (TRL), S.1 (intermediate project), Q/R/T capstone descriptions. **Already cleanly delegated to Ch 2 in the main book; appendices are short references.** No remediation needed.

### B. Distributed training (DDP/FSDP/ZeRO)
Discussed in: N.1 (canonical reference, 130+ lines), B (ML Essentials, brief), Q Track 4 (passing), R.4 (passing). N.1 is the canonical location and is well-isolated. No remediation needed.

### C. Observability / Monitoring / Drift
Split between: K.5 (M.5.4 "Production Observability with W&B Weave" + M.5.5 "Drift Detection and Alerting" + M.5.6 "Cost Tracking and Budget Dashboards"), O.1 (Observability for LLM Systems), O.2 (Monitoring and Drift Detection), O.5 (SLOs/Alerting/FinOps), M.4 §O.7.6 (Observability).

This is the **single largest duplication cluster**. K.5's M.5.4-M.5.6 (W&B Weave + Drift Detection + Cost Tracking) overlap directly with O.1+O.2+O.5. Both K.5 and O cover:
- LLM-specific observability metrics
- Drift detection methodology
- Per-request cost tracking

**Recommendation:** K should focus exclusively on *training-side* tracking (experiments, sweeps, runs, registries used by training scripts). O is the production/operations side. K.5 §M.5.4 onwards is duplicate of O.1+O.2+O.5 and should be condensed to a backref.

### D. Model Registry / Lifecycle
Split between: K.4 (sections M.4.1-M.4.8 "Model Registry"), O.4 (Model Registry and Lifecycle), N.2 §O.3.4 (MLflow Integration on Databricks), N.3 §O.4.4 (MLflow for LLM Lifecycle Management).

K.4 and O.4 both cover MLflow + W&B Registry + promotion stages. K.4 has 8 sub-sections including "M.4.4 MLflow Model Registry in Depth" which is identical in scope to O.4.3 "The Five Registries in the 2024-2026 Market".

**Recommendation:** K.4 should be condensed to "how to push a model to the registry from a training script" (one section), with the lifecycle/promotion/audit content moved to O.4. Or K.4 stays and O.4 backrefs — pick one canonical.

### E. Vector Search
Files: M.1 (PySpark embedding generation), N.3 §O.4.5 (Databricks Vector Search), N.3 §O.4.6 (RAG on Databricks), D.1/D.3 (LangChain vectorstores), E (Orchestration RAG), P.3 (Docker Compose with Chroma).

The Databricks Vector Search content in N.3 is platform-specific and duplicates the standalone-vector-DB content in D. **N.3 §O.4.5 needs a backref to Ch 23 (RAG) and D for the standalone-vs-managed comparison.**

### F. Capstone descriptions
Q (5 track capstones) + T (3 track capstones) + S (3 intermediate projects). Q's Track 3 ≈ T's Track A; Q's Track 4 ≈ T's Track C. **Q should reference T's three-track structure rather than re-state its own per-track capstone scope.**

---

## Recommended fixes

### Priority 1 — must fix (major duplication + stale labels)

1. **DELETE M.4** (`section-m.4.html`, "Production Data Pipelines"). Migrate the one truly M-flavored sub-section (O.7.3 Data Validation with Great Expectations) into M.2 or a new M.5. Replace the M.4 page with a short index pointing to O.3 (deployment), O.1 (observability), and N.4 (Ray Serve).

2. **RELABEL N.2, N.3, N.4** page-current divs from `Section M.3/M.4/M.5` to `Section N.2/N.3/N.4` and breadcrumb from "Appendix M: Distributed ML: PySpark, Databricks, and Ray" to "Appendix N: Distributed ML". This is also a stale-content remnant that may need re-homing: Databricks platform content (N.2 + N.3) is thematically *Data Engineering* (M), not *Distributed ML* (N). Consider moving Databricks back to M and keeping N strictly for parallelism (N.1) + Ray (N.4).

3. **MERGE A.4 + A.6** into a single Information Theory section. A.6 says it "originated as a section of Chapter 04 (Transformer Architecture)" — pick whichever framing is preferred and delete the other.

4. **DELETE K.5 §M.5.4, M.5.5, M.5.6** (W&B Weave Production Observability + Drift Detection + Cost Tracking) and replace with a one-paragraph backref to O.1, O.2, O.5. K.5 should focus on offline-eval *dashboards* (M.5.1-M.5.3 + M.5.7), not production observability.

5. **DELETE P.4 §1 (vLLM) and §2 (TGI) commands** and replace with one short paragraph: "Both vLLM and TGI publish official Docker images; see Section L.1 / L.2 for the exact docker run commands. The patterns shown there work in any container orchestrator." P.4 should focus on container-specific concerns (model weight volumes, multi-stage builds, image-size optimization).

6. **DELETE N.3 §O.4.4 "MLflow for LLM Lifecycle Management"** and §O.4.6 "Building RAG Applications on Databricks"; replace with cross-refs to O.4 and to Ch 23.

7. **DELETE I.4 "Installing vLLM"** sub-section. Cross-ref to L.1 instead.

### Priority 2 — should fix (concept clusters + bad backrefs)

8. **REWRITE K.4 §M.4.4 "MLflow Model Registry in Depth"** to be brief, with the deep treatment moved to O.4. Or vice versa — pick one canonical.

9. **MOVE M.4 §O.7.5 "Multi-Model Serving"** to N.4. M no longer needs a serving section.

10. **CONDENSE Q capstones (Tracks 1, 3, 4, 5)** to one-line summaries that reference T's three tracks. Q should keep the weekly schedule and lab cadence; T owns the capstone definition + rubric.

11. **FIX broken link** in Q at line 229: `appendices/appendices/appendix-r-reading-pathways/index.html` → `../appendix-r-reading-pathways/index.html`.

12. **ADD backrefs** from N.3 §O.4.5 "Databricks Vector Search" to Ch 23 (RAG) and D.3 (LangChain vectorstores) for the standalone-vector-DB comparison.

13. **CONDENSE L.5 §6 "Cost Optimization Strategies"** to serving-specific levers only (quantization sizing, spot instances, batch shape). Strip the vendor-API caching / batch-API / routing levers and backref to O.5.4 which already covers them.

14. **ADD perplexity backref** in B.4 to A.6 (or merged A Information Theory section).

### Priority 3 — nice to have

15. Audit M.3 §O.6.5 (Databricks Feature Engineering) and N.2 §O.3.x (Unity Catalog) for cross-platform coherence — both reference Unity Catalog independently.

16. The cross-ref callout `<div class="callout cross-ref">` is used inconsistently. O.1, O.4, O.5 all use it; L, M, N rarely do. Adopt it consistently.

17. R.7 ("Course Instructor" pathway) and Q (Course Syllabi) reference each other already — but they could share one unified "Instructor Onboarding" sub-section that lives in only one place.

---

## Files with stale page-current labels (low-effort hygiene)

These have page-current divs that still show the old appendix letter (M/O instead of N/M):
- `appendix-m-data-engineering/section-m.3.html` → labeled `Section M.6` (should be `M.3`)
- `appendix-m-data-engineering/section-m.4.html` → labeled `Section M.7` (should be `M.4`)
- `appendix-n-distributed-ml/section-n.2.html` → labeled `Section M.3` (should be `N.2`)
- `appendix-n-distributed-ml/section-n.3.html` → labeled `Section M.4` (should be `N.3`)
- `appendix-n-distributed-ml/section-n.4.html` → labeled `Section M.5` (should be `N.4`)

All H2 sub-section numbers inside M.3, M.4, N.2, N.3, N.4 are also stale (e.g., M.4 has `O.7.1`..`O.7.6` instead of `M.4.1`..`M.4.6`). Same for K.4 (`M.4.x`) and K.5 (`M.5.x`).
