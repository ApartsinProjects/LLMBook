# Task Registry: LLMBook Content Expansion (2026-04-04)

## Status Legend
- [x] Completed
- [~] In progress (background agent)
- [ ] Pending

---

## Phase 1: Appendix Stub Completion

- [x] Appendix K (HuggingFace): 5 sections written
- [x] Appendix L (LangChain): 5 sections written
- [x] Appendix M (LangGraph): 5 sections written
- [x] Appendix N (CrewAI): 5 sections written
- [x] Appendix O (LlamaIndex): 5 sections written
- [x] Appendix P (Semantic Kernel): 5 sections written
- [x] Appendix Q (DSPy): 5 sections written
- [x] Appendix R (Experiment Tracking): R.1-R.3 existed, R.4 (Model Registry), R.5 (LLM Eval Dashboards) written
- [x] Appendix S (Inference Serving): 5 sections written (vLLM, TGI, SGLang, Quantization, Scaling)
- [x] Appendix T (Distributed ML): 5 sections written (Databricks, Delta Lake, Ray, Feature Stores, Pipelines)
- [x] Appendix U (Docker Containers): 4 sections written
- [x] Appendix V (Tooling Ecosystem): 3 sections written

## Phase 2: Missing Content from missing_topics2.md

- [x] OpenTelemetry for LLM Applications (section-30.5)
- [x] AI Gateways and Model Routing (section-31.5)
- [x] Voice Agents and Speech Interfaces (section-21.6)
- [x] RAG Ingestion Pipelines (Airbyte, Unstructured, Tika, Dagster) - section-20.8
- [x] Supply-chain Security for Agent Sandboxes (Trivy, Syft, Cosign, SLSA) - section-26.7
- [x] SWE-bench Agentic Software Engineering Evaluation - section-25.6
- [x] Edge/On-device LLM Deployment (MLX, ExecuTorch, Ollama) - section-31.7
- [x] Human Feedback Tooling (Label Studio, Argilla, LangSmith) - section-29.12
- [x] GraphRAG Implementation (section-20.7)
- [x] Reproducible Agent Benchmarks: covered in section-22.8

## Phase 3: Missing Content from research_topics_gaps.md

- [x] Evaluation Harnesses (Inspect, lighteval, lm-eval-harness) - section-29.9
- [x] LLM-as-Judge Reliability (G-Eval, Prometheus, JudgeLM) - section-29.10
- [x] Automated Red Teaming (HarmBench, JailbreakBench, garak) - section-32.11
- [x] Agentic Security Benchmarks (b3, InjecAgent, tau-bench) - section-26.6
- [x] Research Replication Benchmarks (PaperBench, CORE-Bench, MLE-bench) - section-22.8
- [x] Long-context Benchmarks (LongBench v2, RULER, NIAH) - section-29.11
- [x] GraphRAG Research Module - section-20.7
- [x] Formal Reasoning with Proof Assistants (LeanDojo, miniF2F) - section-8.6
- [x] Expand Unlearning with WMDP Benchmark - expanded section-27.7
- [x] Expand Interpretability with SAE Scaling + sparsify - expanded section-18.2
- [x] Cross-cultural NLP and Pluralistic Alignment - section-32.10
- [x] GPU Kernel Programming (Triton tutorial) - section-9.7
- [x] Embodied Multimodal Agents (OpenVLA, Octo, Habitat) - section-27.5
- [x] Green AI / Environmental Impact - section-32.11
- [x] Privacy Attacks and Differential Privacy - section-32.12
- [x] Human-AI Interaction Patterns and UX Evaluation - section-21.7

## Phase 4: Missing Content from llmbook_missing_content_table.md

- [x] Workflow Orchestration / Durable Execution (Temporal, Inngest) - section-31.6
- [x] Dataset Engineering for Applications (logs, conversations, data contracts) - section-12.8
- [x] Reliability Engineering for LLM Apps (failure taxonomy, SLOs, chaos testing) - section-31.8
- [x] Research Methodology for LLM Papers (experiment design, ablations, artifacts) - section-29.13
- [x] Enterprise Integration Patterns (auth, RBAC, tenant isolation, governance) - section-33.7
- [x] Economic Design of LLM Systems (token budgeting, cascade, caching costs) - section-33.8
- [x] Code/Work Workflows and Agentic Systems (Claude Code, Claude Works, Codex, Devin, Cursor) - section-25.7

## Phase 4b: Additional Content (gap_scale.md, Two Minute Papers, awesome-* repos)

- [x] AI for Scientific Discovery & Research Automation - section-24.8
- [x] LLM Applications Across Industries - section-24.9
- [x] Automatic Prompt & Context Engineering (DSPy, OPRO, TextGrad) - section-11.6
- [x] Analysis and Quality of AI-Generated Code - section-25.8
- [x] Production LLM Training Systems (Megatron, Elastic Training, Fault Tolerance) - section-6.8
- [x] Kubernetes-Native LLM Operations (Scheduling, Serving, GPU Management) - section-31.9
- [x] LLM Performance Benchmarking and Cross-Hardware Portability - section-29.14
- [x] LLM-Powered Robotics - section-27.6
- [x] 3D Gaussian Splatting for LLM-Guided Scene Editing - section-27.7
- [x] World Models: Video Generation, Simulation, Embodied Reasoning - section-34.4
- [x] 71 library shortcut callouts added across Parts 1-9

## Phase 4c: Frontier Topics (10 candidates under evaluation)

### Group A: Engineering Frontier
- [ ] Reliability engineering for agents under production stress
- [ ] Observability, testing, and CI/CD for agent workflows
- [ ] Memory architectures that improve execution
- [ ] Efficient multi-tool orchestration and tool economy
- [ ] Self-improving and adaptive agents in deployment loops

### Group B: Foundational/Theoretical
- [ ] A theory of reasoning in LLMs
- [ ] World models and internal representations of reality
- [ ] Memory as a computational primitive
- [ ] Mechanistic understanding and interpretability of learned computation
- [ ] The nature of agency: when does a model become an agent?

## Phase 5: Low Priority / Optional

- [x] Grammar-constrained Decoding Expansion (LMQL, SGLang, Outlines FSM, jsonformer, Guidance, comparison table, 5 bib entries)

## Phase 6: Pre-commit Tasks

- [ ] Launch scout agents for all new chapters/sections (search content, libs, 2025-2026 trends)
- [x] Update Table of Contents (toc.html) with all new sections and appendices K-T
- [x] Fix math blocks across entire book ($$\textbf mixing prose with LaTeX) - script + audit check completed
- [x] SVG text clipping audit check + fix (128 issues fixed, 5 intentional remaining)
- [x] Math blocks fix script (fix_math_blocks.py ran, 0 remaining issues)
- [x] LaTeX formula fixes: Bradley-Terry, DPO, PPO, KTO, IPO, SimPO, ORPO across 4 alignment files
- [x] LaTeX syntax audit check (p1_latex_syntax.py) + fix script (fix_latex_funcs.py): 16 blocks in 15 files
- [x] Prose-in-formula fixes: 11 files cleaned by background agent
- [x] SVG text right-clip audit check (p1_svg_text_right_clip.py) + fix script: 37 SVGs in 35 files
- [x] KV memory formula fix (section-9.2.html)
- [~] Extend audit script with new checks, run full audit, fix all issues
  - [x] 7 new audit checks created: BROKEN_FIGURE_REF, FIGURE_SEQUENCE, MIXED_CAPTION_STYLE, TOC_LINK_TARGET, ORPHAN_TAG_BEFORE_MAIN, UNESCAPED_AMPERSAND_TITLE, TRIPLE_DOLLAR_MATH
  - [x] Fixed: 74 unescaped ampersands in titles, 6 triple-dollar math, 7 TOC links, 2 orphan divs
  - [x] Agent-created checks: TH_SCOPE_MISMATCH (937 issues), CHAPTER_LABEL_ON_ANCHOR
  - [x] 5 analysis agents completed (Parts 1-2, 3-4, 5-6, 7-8, 9-10+appendices)
  - [x] Fix 937 th scope mismatch issues (fix_th_scope.py, 161 files)
  - [x] Fix 91 unclosed p-in-div issues (fix_unclosed_p.py, 32 files)
  - [x] Fix 1439 manual highlight spans in code blocks (fix_manual_highlights.py, 31 files)
  - [x] Fix remaining broken figure refs (0 remaining after current audit)
  - [x] Consolidate callout system: 13 types, quiz->self-check, key-takeaway->key-insight, practical-tip/best-practice->tip
  - [x] Fix Knowledge Check h3 -> callout-title Self-Check (62 files)
  - [x] Fix double bibliography icons (51 files)
  - [x] Fix unclosed callout divs (8 files)
  - [x] New audit checks: FM4_PROMISE, SECTION_STRUCTURE, SVG_OVERLAP
  - [x] Fix 360 double-encoded ampersands across 190 files
  - [x] Remove 46 fun-notes from 25 module index files
  - [x] Fix element ordering in 8 chapter indexes (prereqs before objectives)
  - [x] Fix Part 2 missing chapter cards (Modules 08, 18)
  - [x] Add audit checks: CHAPTER_STARTER, INDEX_ORDER, PART_INDEX, SECTION_CALLOUT
  - [x] Fix PART_LABEL_FORMAT check (accept Roman numerals, 148 false positives eliminated)
  - [x] Fix P0 duplicate Code Fragment 5.3.3 (renumbered to 5.3.3-8)
  - [x] Fix remaining P1 issues (PLACEHOLDER_CONTENT, UNCLOSED_P, BARE_CODE, misc agents completed)
  - [x] Fix 227 unclosed callout divs via SECTION_STRUCTURE nesting checker (depth-tracking stack)
  - [x] Fix SECTION_STRUCTURE nesting checker false positives (1015 reduced to 227 real issues, then 0)
  - [x] Fix 6 UNUSED_VENDOR issues (unused KaTeX/Prism removed from 6 files)
  - [x] Refine PLACEHOLDER_CONTENT check (72 false positives eliminated)
  - [x] Final P0+P1 audit: 0 P0, 0 P1 remaining (207 P2 cosmetic issues)
- [x] Create CONTENT_GUIDELINES.md (prevention guide for content-generating agents)
- [x] Audit appendices vs book content for duplication (5 critical, 390 missing cross-refs)
  - [x] Add cross-reference callouts (Appendix K/S/G already cross-referenced in relevant chapters)
  - [x] Deduplicate Appendix B vs Module 0 (reframed as companion, cross-refs added)
  - [x] Deduplicate Appendix S vs Module 9.2/9.4 (residual dupes removed, bidirectional links)
- [x] Split FM.1 into FM.1a (What This Book Covers) + FM.1b (Who Should Read This Book)
- [x] Renumber front matter index (FM.1 through FM.9)
- [x] Fix appendix header font color in CSS (#5a6672 to #ffffff)
- [x] Author bio updates (removed workshop line from first author, added defense/grants to second author)
- [~] Update front matter to reflect current book content and features
- [x] Resolve duplicate content in sections 29.6 and 30.2 (30.2 kept as canonical, 29.6 redirects)
- [x] Reorganize scripts/ into subfolders: fix/ (24), detect/ (18), generate/ (8), data/ (4), _archive/ (113)
- [x] Archive 23 root-level one-shot _*.py scripts into scripts/_archive/
- [x] Merge old _scripts_archive/ (64 files) into scripts/_archive/
- [x] Move author photos to images/, remove empty dirs, clean root
- [x] Add scripts/README.md to book-skills documenting generalizable scripts
- [x] Resolve duplicate content in sections 29.6 and 30.2 (30.2 kept as canonical, 29.6 redirects)
- [~] Update front matter to reflect current book content and features
- [x] Merge duplicate part-6 directories (88 files rewritten, old archived to _archive/old-part-dirs/)
- [x] Merge duplicate part-7 directories (same pass, 114 total path rewrites)
- [x] Clean each subfolder of old/orphan files (132 build artifacts + 99 old part files archived)
- [x] Cross-reference hyperlinks pass (346 links across 166 files)
- [x] Fix 22 broken figure refs across 12 files
- [x] Fix P0 audit issues (broken xrefs, dup figures, SVG title)
- [x] Update front matter to reflect current 10-part structure and appendices A-V
- [x] Standardize .part-overview CSS to match .overview (accent border-left, max-width 750px)
- [x] Remove non-canonical content from indexes (bare fun-notes, time-estimate, stray h2)
- [ ] Commit and push all changes

## Phase 6b: Depth and Cross-referencing

- [~] Model internals depth pass, Parts 1-4 (reasoning models, architectures, DPO variants, PEFT)
- [~] Model internals depth pass, Parts 5-10 (RAG, agents, multimodal, evaluation, safety)
- [~] Cross-reference hyperlinks pass across all HTML (agent completed, needs review)
- [ ] Update MetaAgent skills for depth/inner working requirements

## Phase 6c: Missing Features (from FM4_PROMISE + SECTION_STRUCTURE audit)

### Agent: exercise-designer (07) + writing agents
- [x] Add level badges to Modules 0-5 (Part 1) and Module 7 (199 badges across 27 files)
- [x] Add Warning callout to Module 35 (AI and Society)

### Agent: research-scientist (18) + writing agents
- [x] Add Research Frontier section to Module 23 (Tool Use and Protocols)
- [x] Add Research Frontier section to Module 24 (Multi-Agent Systems)
- [x] Add Research Frontier section to Module 26 (Agent Safety and Production)

### Agent: chapter-lead (00) + writing agents
- [x] Add annotated bibliography to Module 23 (11 refs)
- [x] Add annotated bibliography to Module 24 (12 refs)

### Agent: exercise-designer (07) - lab format standardization
- [x] Create LAB_COVERAGE audit check (p2_lab_coverage.py)
- [x] Lab gap analysis: 16/36 modules have labs, 20 need labs created
  - Missing labs: Modules 0-12, 27-31, 34-35
  - Existing labs: Modules 13-26, 32-33 (Parts 4-6, 9)
- [ ] Create 20 hands-on labs for modules without labs (Phase 7 content generation)

## Phase 7: Full Agent Passes

- [ ] Agent pass 1: Full book-writing agent pass over ALL HTML files
- [ ] Agent pass 2: Illustrations, diagrams, mental models, and analogies for key concepts
- [ ] Agent pass 3: Optimize and streamline book structure (redundancy, flow, chapter ordering)
- [ ] Agent pass 4: For each code example, add library shortcut (search popular libs implementing same in fewer lines)

---

## Previously Completed (from earlier sessions)

- [x] Create 5 new audit check plugins from deep review findings
- [x] Reorder front matter sections for readability
- [x] Update author bios
- [x] Fix section-22.1 audit issues
- [x] Compact pathway chapter guides (291 pw-reason descriptors across 20 pathways)
- [x] Add prerequisites to 9 syllabus pages
- [x] Promote repeating styles to book.css (syllabus-table, agent-card)
- [x] Fix 27 broken cross-reference links
- [x] Fix 9 orphan content files (epigraph/prereqs outside main)
- [x] Fix 9 vague headings
- [x] Fix 45 section ordering violations
- [x] Remove 351 redundant SVG titles from 192 files
- [x] Delete 5 orphaned agent avatars
- [x] Add 7 new audit check plugins
- [x] Generate 24 pathway/course icons via Gemini
