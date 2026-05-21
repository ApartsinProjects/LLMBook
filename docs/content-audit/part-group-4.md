# Content Audit, Parts 13-16 + Appendices

Audit date: 2026-05-17. Read-only review of part-13-llmops-lifecycle, part-14-designing-llm-agent-products, part-14-applications-of-llms-across-industries, part-15-llm-agentic-ai-research-frontiers, and the three appendices (math-foundations, course-syllabi, reading-pathways). Note: directory has only three appendices (a, b, c), not the four mentioned in the audit brief; there is no `appendix-b-ml-essentials/` and no `appendix-d-reading-pathways/` directory. Appendix B is currently Course Syllabi and Appendix C is Reading Pathways. The ML-Essentials appendix is referenced inside Appendix B but the link points back to Part 1 Ch 0, confirming it was deferred and never created.

The book just finished a major restructure (waves 1-9) and the artifacts of that restructure are clearly visible across these parts: placeholder section descriptions ("Promoted from old Ch 62 monster.", "Core production engineering.", "A comprehensive chapter from the Building Conversational AI textbook.", "A chapter from the Building Conversational AI textbook."), stale chapter and section numbers in headings, breadcrumbs, prev/next labels, and cross-reference labels (link hrefs are mostly correct, but the displayed text shows the pre-restructure numbering), spurious chapter cards in part indexes that point at sections in other modules, and a Part-16 part index where the chapter cards skip the directory numbering by 2-3 each.

## Cross-cutting observations

Several issues recur across every part in this group; rather than restate them per chapter, I am listing them once here and only calling out exceptions inside the per-chapter blocks below.

- **Part numerals everywhere are stale.** Part 13 says "Part X", Part 14 says "Part XI", Part 15 says "Part XI", Part 16 says "Part XII". Every section's breadcrumb, every chapter's chapter-nav "Up" link, and every section's pagefind part metadata carries the old Roman numeral. Correct numerals: Part XIII (13), Part XIV (14), Part XIV (15), Part XV (16).
- **Section H2 IDs use new numbering but visible H2 text uses old numbering.** Almost every section in this group has H2 elements like `<h2 id="51-1-1-...">53.1.1 Latency Optimization Strategies</h2>` where the id reflects something close to the new section number but the visible heading uses an entirely different (old) chapter/section number (53.1.1, 33.x.y, 64.x.y, etc.). This same drift appears in Figure captions ("Figure 53.1.1", "Figure 53.3.1", "Figure A.0.1", "Figure D.0.1"), Table captions ("Table 57.4.1", "Table p.0.1" through "p.0.8"), Pseudocode boxes ("Pseudocode 34.3.1"), and inline prose.
- **Prerequisites blocks and Looking-Back callouts reference old chapter numbers.** Phrases like "as covered in Section 45.1", "from Chapter 44", "from Chapter 23 (RAG)", "from Chapter 25 (Agent Safety)", "from Chapter 37" appear constantly. The hrefs mostly point at the correct new files, but the displayed labels are wrong.
- **Chapter-nav "What Comes Next" and prev/next blurbs name the wrong chapter number.** Almost every chapter index in Parts 13-16 has at least one "Chapter NN" reference in the next-chapter blurb where the number is from the pre-restructure plan rather than the new numbering.
- **Single-section chapters in Part 13 (63, 64, 66) are deliberately skeletal,** but their section descriptions are placeholder text rather than even one-sentence content summaries.
- **Tools-of-the-Trade chapters (71, 79, 83) have all five section descriptions as the placeholder string "A chapter from the Building Conversational AI textbook." or "A comprehensive chapter from the Building Conversational AI textbook."**
- **Em dashes appear in chapter indexes and big-picture paragraphs.** The user's instructions forbid em dashes in generated text. The current HTML has several. This is a content-style issue, not a structural one; flagged here once for the whole group rather than per-chapter.

## Part 13: LLMOps Lifecycle (modules 62-66)

### Part-13 index (E:\Projects\BookBlogsHome\LLMBook\part-13-llmops-lifecycle\index.html)

- **Title**: KEEP (`Part XIII: LLMOps & Lifecycle Management`). Reasonable.
- **Big picture**: PROPOSE rewrite. The big-picture callout is just the meta description repeated verbatim ("AI gateways and routing, workflow orchestration, containers, reliability and SLOs, model registry and lifecycle."). Propose: "Production LLMs need more than a working prompt: they need gateways that route across providers, durable workflows that survive crashes, containers that pin GPU and CUDA versions, and SLOs that catch hallucination spikes before users do. This part covers the operational layer that turns a working agent into a service teams can run."
- **Chapter cards**: BROKEN. The chapter-card-list `<div>` is empty (`<!-- Chapter cards added by rebuild script -->`), and the four chapter cards that actually render are siblings of that empty list rather than children. More important: **Chapter 62 (Production Engineering Core) is completely missing from this index**. Module-62-production-engineering-core exists with two sections (62.1, 62.2) but does not appear anywhere in the part index. Either Ch 62 needs to be added back as the first chapter card, or the two sections need to be redistributed into 63-66 with an explicit Ch 62 removal. The dir name `module-62-production-engineering-core` and the in-chapter title strongly suggest it should be the first chapter and the section listing should be 62.1 Scaling, Performance & Production Guardrails, 62.2 LLMOps & Continuous Improvement.
- **Ordering**: KEEP within the visible cards (63 gateways, 64 orchestration, 65 containers/k8s, 66 reliability) but ADD Ch 62 at the front.
- **Stale refs**: meta description and h1 are clean. No other stale refs in the part index proper.

### Chapter 62: Production Engineering for LLM Systems

- **Title**: KEEP (`Production Engineering for LLM Systems`). Fits well as the entry chapter to Part 13 covering scaling, guardrails, and LLMOps lifecycle.
- **Description (big-picture)**: PROPOSE "Production LLM systems must survive unpredictable traffic and produce safe responses every time. This chapter covers the performance engineering layer (latency, batching, quantization, caching) and the LLMOps practices (prompt versioning, A/B canaries, soft-failure detection, feedback loops) that turn a prototype into a continuously improving service." Current text is just the meta-description echo.
- **Section descriptions**:
  - 62.1 Scaling, Performance & Production Guardrails: PLACEHOLDER `Core production engineering.` PROPOSE "Latency optimization at every layer (caching, batching, quantization, infrastructure), backpressure with token-bucket rate limiting, and the input/output guardrails that keep responses safe under load."
  - 62.2 LLMOps & Continuous Improvement: PLACEHOLDER `Core production engineering.` PROPOSE "Treat prompts as code: content-addressable prompt registries, A/B canary deploys with shadow eval, statistically-rigorous experimentation, and feedback loops that turn user signal into the next fine-tune and the next eval set."
- **Ordering**: KEEP. Performance/guardrails before LLMOps reads correctly.
- **Stale refs**: ABUNDANT.
  - section-62.1.html line 27 breadcrumb: "Part X: LLM Operations and Production Infrastructure" -> "Part XIII: LLMOps & Lifecycle Management"
  - section-62.1.html line 38 big-picture: "prompt injection defenses from Section 14.4" -> Section 12.4 (per the href). "Section 10.1", "Section 10.2" -> use actual new numbers (9.1, 9.2).
  - section-62.1.html line 42 prerequisites: "Section 45.1: Application Architecture and Deployment" -> Section 70.5
  - section-62.1.html line 44 h2: `53.1.1 Latency Optimization Strategies` -> 62.1.1
  - section-62.1.html line 49 figure caption: "Figure 53.1.1" -> Figure 62.1.1
  - section-62.1.html "Pseudocode 34.3.1" -> Pseudocode 62.1.1 (or similar)
  - section-62.2.html line 27 breadcrumb: "Part X..." -> Part XIII
  - section-62.2.html line 38 big-picture: "Chapter 44", "Section 44.6" -> Chapter 42, Section 42.6 (per hrefs)
  - section-62.2.html line 42 prerequisites: "Section 45.1: Application Architecture and Deployment" -> Section 70.5
  - section-62.2.html line 43 h2: `53.2.1 Prompt Versioning` -> 62.2.1
  - section-62.2.html line 61 cross-ref: "Section 23.1" -> Section 32.1
- **Home fit**: Ch 62 belongs in Part 13. Confirmed. The retained two-section size is fine after the split; expand them in content-quality pass.
- **Chapter-nav damage**: index.html line 47 prev points to module-57-compute-planning labeled "Chapter 61: Compute Planning". Line 48 In-Part says "Part X". Line 49 next points to "Chapter 63: Ideation: Finding LLM-Worthy Problems" pointing to module-67-ideation in Part 14. Should be Chapter 63 AI Gateways in this part. This is wrong in three ways.

### Chapter 63: AI Gateways & Model Routing

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. The chapter-index big-picture is fine ("Production LLM deployments need gateways for rate limiting, model routing for cost/quality optimization, and observability...").
- **Section descriptions**: 
  - 63.1 AI Gateways and Model Routing: PLACEHOLDER `Promoted from old Ch 62 monster.` PROPOSE "Why a centralized gateway tier (LiteLLM, Portkey, Kong AI Gateway) becomes essential past a single model, plus semantic caching, fallback chains, and per-request cost telemetry."
- **Ordering**: N/A (one section).
- **Stale refs**:
  - section-63.1.html line 36 breadcrumb: "Part X..." -> Part XIII
  - section-63.1.html line 47 big-picture: "deployment architecture from Section 45.1" -> Section 70.5; "API patterns from Chapter 13" -> Chapter 11
  - section-63.1.html line 51 prerequisites: "Section 45.1", "Section 45.3" (linking to module-62-production-engineering-core/section-62.1.html), "Section 25.4" -> use new numbers (70.5, 62.1, 49.4)
  - section-63.1.html line 55 figure caption: "Figure 53.3.1" -> Figure 63.1.1
  - section-63.1.html line 57 h2: `53.3.1 The Case for an AI Gateway Layer` -> 63.1.1
- **Home fit**: Ch 63 is a deliberately skeletal one-section chapter. Acceptable per restructure plan. Content quality pass will expand. Note: alphabetically a gateway chapter feeling like "production engineering core" makes sense as a Ch 62-3 sibling.

### Chapter 64: Workflow Orchestration & Durable Execution

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Reasonable. Contains an em dash on line 26 ("LLM-powered applications often span hours of work — chained tool calls,..."), flag per global no-em-dash rule.
- **Section descriptions**:
  - 64.1 Workflow Orchestration and Durable Execution: PLACEHOLDER `Promoted from old Ch 62 monster.` PROPOSE "When an agent workflow has to survive crashes, retries, and provider outages for hours: Temporal, Inngest, LangGraph persistence, and the patterns that make agent state durable."
- **Ordering**: N/A.
- **Stale refs**:
  - section-64.1.html line 27 breadcrumb: "Part X..." -> Part XIII
  - section-64.1.html line 38 big-picture: "Section 45.1", "Chapter 26" -> Section 70.5, Chapter 26 (Ch 26 OK)
  - section-64.1.html line 42 prerequisites: "Section 45.1", "Section 45.4", "Section 45.5", "Chapter 27", "Section 25.4" -> new numbers
  - section-64.1.html line 44 h2: `53.4.1 Why LLM Agents Need Durable Execution` -> 64.1.1
- **Home fit**: Acceptable as skeletal chapter.

### Chapter 65: Containers, Kubernetes & Deployment

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Five-section structure is well organized.
- **Section descriptions**:
  - 65.1 Docker Fundamentals: PLACEHOLDER. PROPOSE "Images, containers, layers, volumes, and the day-1 commands. Why Docker solves the CUDA/Python-version reproducibility problem that venv and conda cannot."
  - 65.2 Writing Dockerfiles for ML and LLM Projects: PLACEHOLDER. PROPOSE "Multi-stage builds, GPU base images, dependency-cache ordering, and the patterns that drop ML image sizes by 60% and build times from 30 minutes to under 2."
  - 65.3 Docker Compose for Multi-Service AI Applications: PLACEHOLDER. PROPOSE "Declaratively orchestrate the LLM server, vector DB, Redis cache, API gateway, and Postgres in one compose.yml: networks, healthchecks, dependency ordering, and per-service scaling."
  - 65.4 Containerizing LLM Inference Servers: PLACEHOLDER. PROPOSE "Official vLLM/TGI/Ollama images, GPU passthrough patterns, model-weight cache volumes, quantized serving, and OpenAI-compatible endpoints out of the box."
  - 65.5 Kubernetes-Native LLM Operations: KEEP existing implicit body (no current section-desc to replace; chapter-index section card lacks one, but section file has rich content). PROPOSE adding: "GPU-aware batch scheduling (Kueue, Volcano), Kubeflow Training Operator, KServe with vLLM/TGI runtimes, NVIDIA GPU Operator and MIG partitioning, and autoscaling tuned for LLM inference."
- **Ordering**: KEEP. Fundamentals -> Dockerfiles -> Compose -> Inference-server containers -> Kubernetes builds correctly from simple to complex and from single-container to multi-node.
- **Stale refs**:
  - All five section files have `Part X: LLM Operations and Production Infrastructure` in the breadcrumb. Fix to Part XIII.
  - section-65.3.html line ~"In Section E.1, we launched individual containers" -> "In Section 65.1, ..." (the "Section E.1" tag implies leftover from an "Appendix E" numbering before the Docker content moved into Part 13).
  - section-65.4.html line 38 big-picture: cross-link label "Section Q.2: Text Generation Inference (TGI)" -> this is a stale Appendix-Q label inside a concept-link `title=`. Update to a real new section ID.
  - section-65.5.html line 38 prerequisites: "Section 45.1", "Section 45.3", "Section 7.6", "Chapter 09" -> use new numbers (70.5, 62.1, 6.6, 9)
  - section-65.5.html line 41 h2: `53.7.1 GPU Scheduling for LLM Training` -> 65.5.1
- **Home fit**: All five sections fit Ch 65 cohesively. No moves needed.

### Chapter 66: Reliability, SLOs & Model Registry

- **Title**: PROPOSE "Reliability, SLOs & Incident Response" (drop "Model Registry"). The single section that exists (Reliability Engineering for LLM Applications) is about hard/soft failure taxonomy, retries, circuit breakers, SLO design, incident response, chaos engineering. There is nothing about a model registry. Either add a registry section or drop the registry phrase from the chapter title.
- **Description (big-picture)**: KEEP. Reasonable phrasing.
- **Section descriptions**:
  - 66.1 Reliability Engineering for LLM Applications: PLACEHOLDER `Promoted from old Ch 62 monster.` PROPOSE "Hard infrastructure failures vs. soft semantic failures (hallucination, refusal, format drift), classical resilience patterns (retries, circuit breakers, fallback chains), LLM-specific guardrails, SLO design, incident response, and chaos engineering."
- **Ordering**: N/A.
- **Stale refs**:
  - section-66.1.html line 36 breadcrumb: "Part X..." -> Part XIII
  - section-66.1.html line 52 prerequisites: "Section 45.1: Application Architecture and Deployment", "Chapter 44: Observability and Monitoring", "Section 26.1: Foundations of AI Agents" -> 70.5, 42 (or 44 if observability is its own ch), 26.1
  - section-66.1.html line 56 figure caption: "Figure 53.6.1" -> Figure 66.1.1
  - section-66.1.html line 58 h2: `53.6.1 LLM Failure Taxonomy`, line 64 `53.6.1.1 Hard Failures`, line 66 `53.6.1.2 Soft Failures` -> 66.1.1, 66.1.1.1, 66.1.1.2
- **Home fit**: Single section is OK as skeletal placeholder. The chapter title's reference to "Model Registry" is misleading because there is no registry content. Either expand or rename per the title proposal above.

## Part 14: Designing LLM-Based Products (modules 67-71)

### Part-14 index (E:\Projects\BookBlogsHome\LLMBook\part-14-designing-llm-agent-products\index.html)

- **Title**: PROPOSE replace "Part XI" with "Part XIV" everywhere in this file (line 7 meta description, line 8 title, line 21 h1, line 24 part-label/h1, line 25 chapter-subtitle).
- **Big picture**: PROPOSE rewrite. The current text is meta-description echo. Replace with: "From the first idea sketched on a napkin to a shipped LLM product with unit economics that work. This part covers ideation discipline, product management for AI-native software, vibe-coding workflows, scaling economics, and the launch-and-iterate loop that separates a viable AI product from a demo."
- **Chapter cards**: SEVERELY BROKEN.
  - Chapter card for Ch 68 (Ideation) has section numbers `63.1`, `63.2`, `63.3` instead of 67.1, 67.2, 67.3. Wrong chapter number too (should be 67, not 68).
  - Chapter card for Ch 69 "LLM Product Management" has section numbers `64.1`, `64.2`, `64.3` and links to module-67-ideation/section-67.4-67.6. This duplicates module 67's directory and uses old chapter numbering.
  - Chapter card for Ch 70 "LLM Strategy & Use Case Prioritization" has section numbers `65.1`, `65.2`, `65.3`, `65.4`. The 65.3 and 65.4 entries are duplicates of 65.1 and 65.2 (same hrefs).
  - Chapter card for Ch 71 "Prototyping via Vibe-Coding" has section numbers `66.1`, `66.2`, `66.3` and points to module-68-vibe-coding sections 68.1-68.3.
  - Chapter card for Ch 67 (sic) "Building the MVP" has section numbers `67.1`, `67.2`, `67.3` and points to module-68-vibe-coding sections 68.4-68.6.
  - Chapter card for Ch 68 (second time) "From Idea to Product Hypothesis" lists module-67-ideation sections 67.9-67.15 under section numbers 68.1-68.7.
  - Chapter card for Ch 69 (second time) "Scaling Economics: Unit Costs & ROI" points to module-69-llm-economics with section numbers 69.1-69.3 (these are correct).
  - Chapter card for Ch 70 (second time) "Shipping and Scaling AI Products" points to module-70-shipping-products with section numbers 70.1-70.6 (correct).
  - Chapter card for Ch 71 (second time) "Tools of the Trade: Idea-to-Product Toolkit" lists 71.1-71.8 where 71.6, 71.7, 71.8 are duplicates of 71.1 and 71.2 with `#anchor` fragments.
  - **Net result**: the part index shows 9 cards labelled with 5 chapter numbers (67, 68, 68, 69, 69, 70, 70, 71, 71). The directory has 5 modules (67-71). The index either needs collapsing to one card per directory or the content needs splitting into more modules to match the cards.

- **Ordering**: BROKEN. Even setting aside the duplicate cards, the visible ordering (Ideation -> Product Mgmt -> Strategy -> Vibe -> MVP -> Hypothesis -> Economics -> Shipping -> Tools) is illogical (Strategy before MVP, Hypothesis after MVP, MVP before Hypothesis). Proposed canonical ordering: 67 Ideation -> 68 Vibe-Coding (or 68 Hypothesis-to-Spec) -> 69 Economics -> 70 Shipping -> 71 Tools. Need to decide if the 15-section monolith of module-67-ideation gets split into multiple modules and what their order should be.
- **Stale refs**: meta description and h1 all say "Part XI".
- **Home fit / consolidation**: This is the biggest structural issue in this part. Module-67-ideation contains 15 sections covering Ideation (67.1-67.3), Product Management (67.4-67.6 with stale breadcrumb "Chapter 64"), Strategy (67.7-67.8 with stale breadcrumb "Chapter 65"), and From Idea to Product Hypothesis (67.9-67.15 with stale breadcrumb "Chapter 68"). Each of these four conceptual chapters has its own breadcrumb still pointing at the OLD chapter number embedded in the section html. The wave-9 restructure clearly intended these to remain in one ideation module but the section files still carry the old chapter labels and the part index still presents them as separate chapters. Either the index needs to collapse to 5 modules (67 ideation now-omnibus, 68 vibe, 69 economics, 70 shipping, 71 tools) or the module needs splitting into 4 directories. The current state is broken either way.

### Chapter 67: Ideation: Finding LLM-Worthy Problems

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. The big-picture in module-67-ideation/index.html is well-written.
- **Section descriptions**:
  - 67.1, 67.2, 67.3 have real descriptions. KEEP all three.
  - The module-67 directory contains 12 more section files (67.4-67.15) that are NOT listed in module-67-ideation/index.html but ARE listed in the Part-14 index under spurious chapter cards. The chapter index needs to either include them or the part index needs to stop pointing at them.
- **Ordering**: 67.1 problem-shape, 67.2 discovery heuristics, 67.3 bet-my-money test maps neatly to "what problems work -> how to find them -> how to gate them". KEEP.
- **Stale refs**:
  - Line 22 breadcrumb: "Part XI: Designing LLM-Based Products" -> Part XIV
  - Line 54 What-Comes-Next: link href is `../module-67-ideation/index.html` (self-link), text says "Chapter 62: LLM Product Management". Should point to the next chapter (68) and say its name correctly.
  - Line 57 prev: "Chapter 62: Production Engineering" with link to part-13/module-62. Should be the previous part-14-context chapter, or stay this way as the cross-part link (acceptable since Ch 67 is first chapter in part 14, prev = last chapter in part 13).
  - Line 58 In-Part: "Part XI" -> Part XIV
  - Line 59 next: href `../module-67-ideation/index.html` (self-link again) text "Chapter 64: LLM Product Management" — broken in both target and label.
- **Home fit**: 67.1-67.3 fit. 67.4-67.15 belong to other conceptual chapters (see consolidation note below).

#### Section 67.4-67.15: orphan sections inside module-67-ideation

Each of these section files has a breadcrumb that names a chapter that does not exist as a directory:

- 67.4 From Hypothesis to Product Spec: breadcrumb "Chapter 64: LLM Product Management"; H2 IDs labelled `59.1.1`, `59.1.2`. Belongs in a Product Management chapter that does not currently exist as its own directory.
- 67.5 LLM Product Management: breadcrumb "Chapter 64"; H2 ID labelled `31.3.1` (very stale).
- 67.6 UX and Iteration for LLM Products: breadcrumb "Chapter 64".
- 67.7 LLM Strategy & Use Case Prioritization: breadcrumb "Chapter 65"; H2 ID labelled `65.1.1` (close to right).
- 67.8 LLM Vendor Evaluation & Build vs. Buy: breadcrumb "Chapter 65"; H2 ID labelled `65.2.1` (close to right).
- 67.9 What Makes AI Products Different: breadcrumb "Chapter 68"; H2 ID labelled `63.1.1`.
- 67.10 Choosing the Model's Role: breadcrumb "Chapter 68"; H2 labelled `63.2.1`.
- 67.11 Risk and Feasibility Assessment: breadcrumb "Chapter 68"; H2 labelled `63.3.1`.
- 67.12 The Observe-Steer Development Loop: breadcrumb "Chapter 68"; H2 labelled `63.5.1`.
- 67.13 The Founder's Prototype Loop: breadcrumb "Chapter 68"; H2 labelled `63.6.1`.
- 67.14 Documentation as Control Surface: breadcrumb "Chapter 68"; H2 labelled `63.7.1`.
- 67.15 From Prototype to MVP: breadcrumb "Chapter 68"; H2 labelled `63.9.1`.

Proposed resolution (consolidation): either split module-67-ideation into 67-ideation (3 sections), 67b-product-mgmt (3 sections from 67.4-67.6), 67c-strategy (2 sections from 67.7-67.8), 67d-hypothesis (7 sections from 67.9-67.15) and renumber to 67-70 accordingly, or update module-67-ideation/index.html to list all 15 sections and remove the spurious chapter cards from the part index. The latter is the lower-effort path but produces a 15-section chapter that is awkward to read.

### Chapter 68: Prototyping via Vibe-Coding

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Reasonable.
- **Section descriptions**:
  - 68.1 has real description. KEEP.
  - 68.2 Vibe-Coding & AI-Assisted Software Engineering: PLACEHOLDER `A comprehensive chapter from the Building Conversational AI textbook.` PROPOSE "Cursor, Claude Code, Cline, Copilot Workspace, Windsurf, Aider, Continue: how AI-assisted coding works in 2026, where the productivity gains come from, and where they evaporate."
  - 68.3 has real description. KEEP.
  - **Three additional sections (68.4 Building the MVP, 68.5 The Vertical-Slice Pattern in Depth, 68.6 Pilot Triggers: Keep, Pivot, or Kill) exist in the directory but are NOT listed in module-68-vibe-coding/index.html.** They are only referenced from the spurious Part-14 index chapter card "Chapter 67 Building the MVP". The chapter index needs to either include them (which expands the chapter scope from vibe-coding to "vibe-coding + MVP-building") or split them out into their own module-67b-mvp directory.
- **Ordering**: If 68.4-68.6 stay in this module, the natural order is 68.1 What is vibe-coding -> 68.2 AI-assisted SWE -> 68.3 IDE landscape -> 68.4 Building the MVP -> 68.5 Vertical-slice pattern -> 68.6 Keep/pivot/kill triggers. This is a coherent "from tools to outcomes" arc.
- **Stale refs**:
  - Line 22 breadcrumb: "Part XI" -> Part XIV
  - Line 54 What-Comes-Next: link self-references module-68-vibe-coding/index.html, text says "Chapter 65: Building the MVP". Should point to module-69 Economics and say so.
  - Line 57 prev: "Chapter 65: LLM Strategy & Use Case Prioritization" but link points to module-67-ideation. Should be Ch 67 Ideation.
  - Line 58 In-Part: "Part XI" -> Part XIV
  - Line 59 next: self-link to module-68-vibe-coding/index.html, text "Chapter 67: Building the MVP". Should be Ch 69 Economics.

### Chapter 69: Scaling Economics: Unit Costs & ROI

- **Title**: KEEP. Reasonable, descriptive.
- **Description (big-picture)**: KEEP. Strong economic-anchors section (GPT-4 to GPT-4o, DeepSeek-V3, Cursor cost data).
- **Section descriptions**:
  - 69.1 ROI Measurement & Value Attribution: PLACEHOLDER `A chapter from the Building Conversational AI textbook.` PROPOSE "Frameworks for tying LLM spend to user outcomes: per-task value attribution, counterfactual ROI in production, and the metrics that survive a CFO review."
  - 69.2 Economic Design of LLM Systems: PLACEHOLDER. PROPOSE "Architectural choices with cost consequences: model tiering, caching strategy, when to fine-tune vs. prompt, and the unit-economic patterns that scale to millions of requests per day."
  - 69.3 Token Cost Forecasting and Multi-Vendor Arbitrage: PLACEHOLDER. PROPOSE "Forecasting token spend, routing across providers for cost/quality optimization, and the 2026 vendor-pricing dynamics that make multi-provider strategy mandatory."
- **Ordering**: KEEP. ROI measurement -> Economic design -> Vendor arbitrage is foundations -> application.
- **Stale refs**:
  - Line 22 breadcrumb: "Part XI" -> Part XIV
  - Line 54 What-Comes-Next: link is `../module-70-shipping-products/index.html` text says "Chapter 69: Shipping and Scaling AI Products". Number is wrong (should be Ch 70).
  - Line 57 prev: "Chapter 68: From Idea to Product Hypothesis" linked to module-67-ideation. This is the orphan-content problem; should be Ch 68 Vibe-Coding.
  - Line 58 In-Part: "Part XI" -> Part XIV.

### Chapter 70: Shipping and Scaling AI Products

- **Title**: KEEP. Reasonable.
- **Description (big-picture)**: KEEP. Strong outage-anchor framing (OpenAI Dec 2024, Anthropic status page, Vercel AI SDK, Cloudflare AI Gateway).
- **Section descriptions**:
  - 70.1, 70.2, 70.3, 70.4 have real descriptions. KEEP.
  - 70.5 Application Architecture & Deployment: PLACEHOLDER `A comprehensive chapter from the Building Conversational AI textbook.` PROPOSE "End-to-end deployment architecture for LLM applications: client tiers, API gateway, model-serving layer, vector store, observability, and the failure-isolation patterns that keep one bad call from cascading."
  - 70.6 Frontend & User Interfaces: PLACEHOLDER. PROPOSE "Streaming, chat UIs, generative UI patterns, optimistic state, edit-and-continue flows, and the UX primitives that make LLM products feel responsive."
- **Ordering**: 70.1 launch economics -> 70.2 copilots across lifecycle -> 70.3 portability/multi-provider -> 70.4 post-launch monitoring -> 70.5 architecture -> 70.6 frontend. The placement of 70.5 (architecture) and 70.6 (frontend) AFTER post-launch monitoring is awkward. PROPOSE move 70.5 and 70.6 earlier in the chapter, immediately after 70.1 (launch economics): 70.1 Launch + AI Unit Economics -> 70.2 Application Architecture & Deployment -> 70.3 Frontend & User Interfaces -> 70.4 AI Copilots Across the Lifecycle -> 70.5 Portability/Multi-Provider -> 70.6 Post-Launch Monitoring. Architecture and frontend are foundational; copilots, portability, and monitoring are operational/strategic concerns that come after.
- **Stale refs**:
  - Line 24 breadcrumb: "Part XI" -> Part XIV.
  - Lines 36, 41, 42, 46, 56, 62, 63: multiple Chapter references: "Chapter 66 took you to a prototype", "the build methodology from Chapter 66", "from Chapter 45", "from Chapter 44", "from Chapter 31", "from Chapter 66", "from Chapters 36 through 38". All these need updating to the new numbering (68 vibe, 62 production, 42 eval, etc.).
  - Lines 62-63 prereqs: "Chapter 66: From Idea to Product Hypothesis" (link to module-67-ideation), "Chapter 45: Production Engineering" (link to module-62-production-engineering-core). Link targets are right, labels are wrong.
  - section-70.1.html line 42: "Section 66.6" in label but link points to module-67-ideation/section-67.14. The orphan-content cross-references in section 70.1 are extensive: "Chapter 44", "Chapter 45" repeated; need to be 42, 62.
  - section-70.5.html line 7 meta description: "A comprehensive chapter from the Building Conversational AI textbook" — placeholder.
  - section-70.5.html line 42 prereqs: "Section 13.1: API Landscape and Architecture" -> Section 11.1.
  - section-70.5.html line 624 What-Comes-Next: "Section 45.2: Frontend & User Interfaces" -> Section 70.6.
- **Home fit**: Sections all fit. Ordering rearrangement above would improve cohesion.

### Chapter 71: Tools of the Trade: Idea-to-Product Toolkit

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Good 2026 anchor list.
- **Section descriptions**: ALL FIVE have placeholder `A chapter from the Building Conversational AI textbook.` PROPOSE:
  - 71.1 Platforms: "AI-native code editors (Cursor, Claude Code, Cline, GitHub Copilot Workspace, Aider, Windsurf), the project-management stack (Linear, Notion), design (Figma + AI), and the analytics layer (Mixpanel, PostHog, Amplitude) that 2026 product teams rely on."
  - 71.2 Libraries & Frameworks: "LangChain, LlamaIndex, Pydantic AI, Instructor, Vercel AI SDK, and the orchestration libraries that connect models to product UIs."
  - 71.3 Datasets & Benchmarks: "Public product-discovery datasets, user-research repositories, and the benchmark sets that show up in pitch decks."
  - 71.4 Models: "The frontier and open-weight models that 2026 product teams compare on cost, latency, quality, and licensing terms."
  - 71.5 External Reading & Communities: "Product-builder Substacks, founder Slacks, and the public postmortems that have shaped the field's collective intuition about what ships and what doesn't."
- **Ordering**: KEEP (matches the Tools-of-Trade template across all parts).
- **Stale refs**:
  - Line 22 breadcrumb: "Part X: Building LLM and Agent Products" -> Part XIV
  - Line 28 pagefind meta: "Part X: Building LLM and Agent Products" -> Part XIV
  - Line 35 big-picture: "Part X covered going from idea to shipped product." -> Part XIV.
  - Line 74 What-Comes-Next: "Part XI surveys industries: legal, finance, healthcare, education, cyber, code, and the rest. Chapter 70 closes Part XI..." -> Part XIV; "Chapter 76 closes Part XIV with the per-vertical vendor map" (or whichever is the correct last chapter of part 15).
  - Line 78 In-Part: "Part XI" -> Part XIV.

## Part 15: Applications of LLMs Across Industries (modules 72-78 + 79-tools)

### Part-15 index (E:\Projects\BookBlogsHome\LLMBook\part-14-applications-of-llms-across-industries\index.html)

- **Title**: PROPOSE replace "Part XI: LLM Applications Across Industries" -> "Part XIV: LLM Applications Across Industries". Affects meta description (line 7), title (line 8), h1 (line 25), part-label (line 24), chapter-subtitle (line 26).
- **Subtitle vs. content mismatch**: Subtitle (line 26) says "Seven vertical applications of LLMs" and lists 7 verticals: Legal, Finance, Healthcare, Education, Cybersecurity, Government, Manufacturing. Meta description (line 7) says "nine verticals". But the part-14 index lists 11 chapter cards (72-77 + 78 + spurious 79 Creative + spurious 80 Recommendation + 81 Tools). Reconcile: either expand subtitle to match or reduce chapter list to match subtitle.
- **Big picture**: KEEP. Good framing.
- **Chapter cards**: HEAVILY BROKEN.
  - Chapter 67 Legal: cards 72.1-72.5 correct.
  - Chapter 68 Finance: cards 73.1-73.5 correct, BUT spurious card 73.6 "LLMs in Finance & Trading" with href `module-68-finance-llms/index.html` (self-link). Drop.
  - Chapter 69 Healthcare: cards 74.1-74.5 correct, BUT spurious card 74.6 "Healthcare & Biomedical AI" with href `module-69-healthcare-llms/index.html`. Drop.
  - Chapter 70 Education: cards 75.1-75.5 correct.
  - Chapter 71 Cybersecurity: cards 76.1-76.5 correct, BUT spurious card 76.6 "Cybersecurity & LLMs" with href `module-71-cybersecurity-llms/index.html`. Drop.
  - Chapter 72 Government: cards 77.1-77.5 correct.
  - Chapter 73 Manufacturing: cards 78.1-78.5 correct.
  - Chapter 74 "LLMs in Creative Industries": three cards labeled 79.1, 79.2, 79.3 but their hrefs are `module-73-manufacturing-llms/section-73.6.html`, `module-73-manufacturing-llms/index.html`, and `module-73-manufacturing-llms/section-73.7.html`. The Creative-Industries content actually lives in module-78 section files 78.6 and 78.7. No `module-74-creative-llms/` directory exists. Either rename/move these section files into their own module-74-creative-llms directory and renumber them 79.1, 79.2, etc., or drop this chapter card entirely.
  - Chapter 75 "LLM-Powered Recommendation & Search": three cards labeled 80.1, 80.2, 80.3 but hrefs are `module-73-manufacturing-llms/section-73.8.html`, `section-73.9.html`, `section-73.10.html`. Same issue. Plus this Chapter-80 label collides with Part-16's first chapter (Frontier Architectures), which is also labeled Chapter 75 in its directory name and index header. The numbering MUST be reconciled.
  - Chapter 76 "Tools of the Trade": cards 81.1-81.5 point to `module-74-tools-of-the-trade/section-79.1-79.5`. The directory is `module-74-tools-of-the-trade` but it self-labels as Chapter 74 internally and is listed here as Chapter 76. Need to pick one number and update both.
- **Ordering**: Within the seven industry chapters (72-78), KEEP. Reasonable progression: Legal (high regulation + high upside) -> Finance (regulated + numerical) -> Healthcare (FDA + ambient doc) -> Education (FERPA + tutoring) -> Cybersecurity (offense+defense) -> Government (admin law) -> Manufacturing (OT/IT). Creative/Recommendation content (78.6-78.10) currently lives in the manufacturing module, which is wrong; it needs its own home.
- **Stale refs**: meta description (line 7) and h1 (line 25) say "Part XI".
- **Home fit / consolidation**:
  - The 78.6-78.10 sections in module-73-manufacturing-llms do not belong in manufacturing. PROPOSE move 78.6, 78.7 to a new module-74-creative-industries-llms; move 78.8, 78.9, 78.10 to a new module-75-recommendation-search-llms. Then renumber. This resolves both the directory-mismatch and the section-naming.
  - Or, alternatively, drop the Creative/Recommendation cards entirely (the subtitle says seven verticals).
  - module-74-tools-of-the-trade should be renamed to module-76-tools-of-the-trade (or whatever number it actually gets after consolidation) and its internal title updated.

### Chapter 67: LLMs in Legal Practice

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Strong Mata v. Avianca anchor and Harvey/Casetext/Hebbia vendor framing.
- **Section descriptions**: 72.1-72.4 KEEP. 72.5 KEEP. All five have real one-liners.
- **Ordering**: 72.1 use cases -> 72.2 failures -> 72.3 regulatory rules -> 72.4 architecture -> 72.5 vendors+further reading. KEEP. This is the canonical template used across the industry chapters in this part.
- **Stale refs**:
  - Line 21 breadcrumb: "Part XI" -> Part XIV.
  - Line 64 What-Comes-Next: "Chapter 52" -> Chapter 68.
  - Line 68 In-Part: "Part XI" -> Part XIV.
  - section-67.5.html line 48: "Chapter 23 (RAG)" link goes to module-32-rag. -> Chapter 32.
  - section-67.5.html line 49: "Chapter 37 (Safety, Ethics & Regulation)" link goes to module-47-adversarial-security-red-team. The new chapter number is 47 (or 48 if that's adversarial), not 37.
  - section-67.5.html line 50: "Section 74.2 (Education, Legal & Creative Industries)" link goes to module-73-manufacturing-llms/index.html. Stale, pre-renumbering.
  - section-67.5.html line 51: "Section 37.6 (Privacy & IP)" link goes to module-53-regulation-compliance/section-53.4.html. New number is 53.4.
  - section-67.5.html line 52: "Section 29.4 (Coding agents)" link goes to module-29-specialized-agents/section-29.4.html. New number is 29.4 (OK).
  - section-67.5.html line 56: "Section 67.3" — correct.
  - section-67.5.html line 62: "Chapter 52 on finance" link goes to module-73. -> Chapter 68.

### Chapter 68: LLMs in Finance

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Strong Bloomberg/Morgan-Stanley/JPMorgan/Goldman 2023 anchors.
- **Section descriptions**: 73.1-73.5 KEEP. 73.6 "LLMs in Finance & Trading" is a SPURIOUS self-link with placeholder desc; drop the card from the chapter index.
- **Ordering**: KEEP (matches template).
- **Stale refs**:
  - Line 21 breadcrumb: "Part XI" -> Part XIV.
  - Line 32 big-picture: "Section 68.6 is the longer production-pattern companion." -> drop reference, no 73.6 exists.
  - Line 69 What-Comes-Next: "Chapter 53" -> Chapter 69.
  - Line 73 In-Part: "Part XI" -> Part XIV.
  - section-68.5.html line 49: "Section 68.6 (LLMs in Finance & Trading)" link goes to module-69-healthcare-llms/section-69.1.html (very wrong; goes to a healthcare section). Drop the reference or fix the target.
  - section-68.5.html line 51: "Chapter 42 (LLM Strategy & Use Case Prioritization)" link to module-67-ideation. -> Chapter 67.
  - section-68.5.html line 52: "Chapter 51 (Legal)" link to module-67-legal-llms. -> Chapter 67.
  - section-68.5.html line 53: "Chapter 25 (Agent Safety & Production)" link to module-49-agent-safety-autonomy. -> Chapter 49.
  - section-68.5.html line 63: "Chapter 53 on healthcare" link to module-74. -> Chapter 69. Plus same "Section 68.6 is a longer companion piece" with wrong target.
- **Home fit**: 73.1-73.5 fit. Drop the 73.6 phantom.

### Chapter 69: LLMs in Healthcare & Biomedical

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Captures the burnout-vs-regulation tension well.
- **Section descriptions**: 74.1-74.5 KEEP. 74.6 "Healthcare & Biomedical AI" is a SPURIOUS self-link; drop.
- **Ordering**: KEEP.
- **Stale refs**:
  - Line 21 breadcrumb: "Part XI" -> Part XIV.
  - Line 30 big-picture: "Section 69.6 is the longer production-pattern companion." -> drop.
  - Line 67 What-Comes-Next: "Chapter 54" -> Chapter 70.
  - Line 71 In-Part: "Part XI" -> Part XIV.
  - section-69.5.html line 50: "Section 69.6 (Healthcare & Biomedical AI)" link goes to module-70-education-llms/section-70.1.html (completely wrong target). Drop.
  - section-69.5.html line 51: "Section 37.6 (Privacy & IP)" link to module-53-regulation-compliance/section-53.4.html. -> Section 53.4.
  - section-69.5.html line 52: "Section 37.11 (Privacy attacks)" link to module-50-privacy-data-protection/section-50.1.html. -> Section 50.1.
  - section-69.5.html line 53: "Chapter 24 (Conversational AI)" link to module-37-conversational-ai. -> Chapter 37.
  - section-69.5.html line 65: "Section 69.6" + "Chapter 54 on education". -> drop 74.6 ref, change Ch 54 to Ch 75.

### Chapter 70: LLMs in Education

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Excellent Khanmigo + NYC DOE + Turnitin anchors.
- **Section descriptions**: 75.1-75.5 all KEEP. Clean.
- **Ordering**: KEEP.
- **Stale refs**:
  - Line 21 breadcrumb: "Part XI" -> Part XIV.
  - Line 64 What-Comes-Next: "Chapter 55 on cybersecurity" -> Chapter 71.
  - Line 68 In-Part: "Part XI" -> Part XIV.
  - section-70.1.html line 34: "Chapter 24" -> Chapter 37; "Chapter 23" -> Chapter 32; "Chapter 37" -> Chapter 47 (or whatever the new safety-ethics chapter number is). All hrefs are correct, labels wrong.

### Chapter 71: LLMs in Cybersecurity

- **Title**: KEEP.
- **Description (big-picture)**: KEEP.
- **Section descriptions**: 76.1-76.5 KEEP. 76.6 "Cybersecurity & LLMs" is a SPURIOUS self-link; drop.
- **Ordering**: KEEP. 76.1 blue team -> 76.2 red team -> 76.3 attack surface -> 76.4 trust boundaries -> 76.5 vendors is defense-first then offense-then-architecture, which reads well.
- **Stale refs**:
  - Line 21 breadcrumb: "Part XI" -> Part XIV.
  - Line 30 big-picture: "Section 71.6 is the longer production-pattern companion." -> drop.
  - Line 67 What-Comes-Next: "Chapter 56 on government" -> Chapter 72.
  - Line 71 In-Part: "Part XI" -> Part XIV.
  - section-71.5.html line 49: "Section 71.6 (Cybersecurity & LLMs)" link goes to module-72-government-llms/section-72.1.html. Drop.
  - section-71.5.html line 50: "Chapter 37 (Safety, Ethics & Regulation)" -> chapter 47/48.
  - section-71.5.html line 51: "Chapter 38 (Agent Safety & Security)" link goes to module-49-agent-safety-autonomy. -> Chapter 49.
  - section-71.5.html line 52: "Chapter 25 (Agent Safety & Production)" link goes to module-49 same. Duplicate ref. Pick one.
  - section-71.5.html line 64: "Chapter 56 on government" -> Chapter 72.

### Chapter 72: LLMs in Government & Public Sector

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Strong ChatGPT Gov, GOV.UK Chat, IRS Direct File anchors.
- **Section descriptions**: 77.1-77.5 KEEP. Clean.
- **Ordering**: KEEP.
- **Stale refs**:
  - Line 21 breadcrumb: "Part XI" -> Part XIV.
  - Line 64 What-Comes-Next: "Chapter 57" -> Chapter 73.
  - Line 68 In-Part: "Part XI" -> Part XIV.
  - section-72.5.html line 54: "Section 37.5" -> Section 53.3 (href target).
  - section-72.5.html line 55: "Section 37.9" -> Section 53.2.
  - section-72.5.html line 56: "Chapter 46 (Compute Planning)" -> Chapter 57.
  - section-72.5.html line 57: "Chapter 55 (Cybersecurity)" -> Chapter 71.
  - section-72.5.html line 69: "Chapter 57 on manufacturing" -> Chapter 73.

### Chapter 73: LLMs in Manufacturing & Supply Chain

- **Title**: KEEP.
- **Description (big-picture)**: KEEP. Strong "advisor with human on contracts" framing.
- **Section descriptions**: 78.1-78.5 KEEP.
- **Ordering**: KEEP (matches template).
- **Stale refs**:
  - Line 21 breadcrumb: "Part XI" -> Part XIV.
  - All H2s in the chapter index use old numbering: line 32 `<h2>57.1 Use Cases...</h2>`, line 55 `<h2>57.2 Failure Modes...</h2>`, line 76 `<h2>57.3 Regulatory and Standards...</h2>`, line 86 `<h2>57.4 Architectural Pattern...</h2>`, line 98 `Table 57.4.1`, line 100 `Table 57.4.1: OT-safe LLM patterns...`, line 151 `<h2>57.5 Postmortems...</h2>`, line 157 `<h2>57.6 Where to Read More</h2>`. All should be 78.1-78.6.
  - Line 159 cross-ref: "Section 32.8 (Robotics, Embodied AI & Scientific Discovery)" link goes to module-24-vla-models. -> Section 24.x.
  - Line 160: "Section 38.1 (Agent Safety & Prompt Injection Defense)" link to module-49-agent-safety-autonomy/section-49.1.html. -> Section 49.1.
  - Line 161: "Section 37.5 (LLM Risk Governance & Audit)" -> Section 53.3.
  - Line 162: "Section 46.2 (Enterprise Integration Patterns)" -> Section 57.2.
  - Line 163: "FM.12 (production-patterns playbook (now part of Chapter 35 LLMOps coverage))" — this is a literal restructure artifact. The "FM.12" is gone, "Chapter 35" -> Chapter 62 LLMOps. Either drop or rewrite as "the LLMOps coverage in Chapter 62".
  - Line 219 next: "Chapter 74: LLMs in Creative Industries" with href to module-73-manufacturing-llms/index.html (self-link). Needs target fix or drop.
- **Home fit / consolidation**: Sections 73.6, 78.7 are CREATIVE INDUSTRIES content (Music, Video, Design, Marketing Copy; Suno, Udio, ElevenLabs licensing). Sections 73.8, 78.9, 78.10 are RECOMMENDATION & SEARCH content (Pinterest Lens, Spotify DJ, etc.). These five sections do not belong in module-73-manufacturing-llms. They should move to module-74-creative-llms (78.6, 78.7) and module-75-recommendation-search-llms (78.8-78.10), or be dropped if the chapter list is collapsed to seven verticals.

### Chapter "79" / "80" (orphan content in module-78)

The Part-15 index references three Creative-Industries sections (79.1, 79.2, 79.3) and three Recommendation-&-Search sections (80.1, 80.2, 80.3). All six point at section files inside module-73-manufacturing-llms. The section files themselves have breadcrumbs referencing Chapter 74 (for 78.6, 78.7) and Chapter 75 (for 78.8, 78.9, 78.10), confirming the original split-out intent. The split-out was never executed. Either execute it (create module-74-creative-llms and module-75-recommendation-search-llms, move and renumber the sections) or remove the orphan content from the Part-15 index.

### Chapter 74 (current dir name) / 81 (Part-15-index label): Tools of the Trade

- **Title**: PICK ONE: either Chapter 74 (matches dir name) or Chapter 76 (matches Part-15 index card label and the natural ordering if creative+recommendation chapters exist). Currently the page's title and h1 say "Chapter 74: Tools of the Trade: Industry Solution Stack" but the Part-15 index labels its card "Chapter 76". The dir name `module-74-tools-of-the-trade` collides with the (planned) module-74-creative-llms.
- **Description (big-picture)**: KEEP wording but fix "Part X" -> "Part XIV".
- **Section descriptions**: ALL FIVE placeholders `A chapter from the Building Conversational AI textbook.` PROPOSE:
  - 79.1 Platforms: "The Harvey/Hebbia (legal), BloombergGPT/FactSet/Hebbia (finance), Abridge/Suki/Glass/Hippocratic (healthcare), Khanmigo/Magic School/Duolingo Max (education), Security Copilot/Charlotte AI (cyber), Palantir AIP/Anduril (government), Siemens Industrial Copilot/Foxconn Foxbrain (manufacturing) vendor map for 2026."
  - 79.2 Libraries & Frameworks: "Vertical-specific connectors in langchain-community (FHIR for healthcare, EDGAR for finance, CourtListener for legal, OPC-UA for manufacturing), plus the open-weight LLMs (Llama, Qwen, Mistral) that ship inside regulated deployments."
  - 79.3 Datasets & Benchmarks: "Industry-grounded eval sets: LegalBench, MedQA/USMLE, FinBench, EduMT, etc., plus the vendor-supplied benchmarks each vertical leans on."
  - 79.4 Models: "Frontier and open-weight models common in each vertical, with the 2026 licensing and HIPAA/SOC2/FedRAMP coverage that determine deployability."
  - 79.5 External Reading & Communities: "The per-vertical Substacks, working-group blogs, regulator dockets, and conference proceedings worth tracking."
- **Ordering**: KEEP.
- **Stale refs**:
  - Line 22 breadcrumb: "Part XI" -> Part XIV.
  - Line 28 pagefind meta: "Part XI" -> Part XIV.
  - Line 35 big-picture: "Part XI surveyed how LLMs are applied" -> Part XIV.
  - Line 73 What-Comes-Next: "Part XII (Frontiers) closes the book. Chapter 65 wraps up with the frontier-research toolbox." -> Part XV; "Chapter 78 wraps up..." (or whatever Part-16 Tools chapter resolves to).
  - Line 76 prev: nav-num "Chapter 75" but the chapter card label here implies Ch 81 prev should be Ch 80 Recommendation. Link points to module-78. Pick one.
  - Line 78 In-Part: "Part XI" -> Part XIV.
  - Line 78 next: nav-num "Chapter 77: Frontier Architectures & Scaling" with link to part-15/module-80. The directory is module-80 and self-labels Ch 80 inside Part 16. Pick a single numbering.

## Part 16: LLM & Agentic AI Research Frontiers (modules 80-83)

### Part-16 index (E:\Projects\BookBlogsHome\LLMBook\part-15-llm-agentic-ai-research-frontiers\index.html)

- **Title**: PROPOSE replace "Part XII: Frontiers" -> "Part XV: LLM & Agentic AI Research Frontiers". Affects meta description (line 7), title (line 8), h1 (line 25), part-label (line 24), part-subtitle (line 26).
- **Big picture**: KEEP wording but fix "Part XII" -> Part XV.
- **Chapter cards numbering mismatch**:
  - Card 1: `<span class="mod-num">Chapter 77</span> Frontier Architectures & Scaling`, links to module-75-frontier-architectures/section-80.x.html, with section-num spans `82.1`, `82.2`, `82.3`, `82.4`. The directory is module-80, the section files are 80.x, the module's own title says "Chapter 75". The Part-16 index labels it Chapter 77.
  - Card 2: `<span class="mod-num">Chapter 78</span> Frontier Theory & Cognition`, links to module-76-frontier-theory/section-81.x.html. Directory says 81, index card says 83.
  - **Chapter 84 is missing entirely** (Frontier Systems & Hardware lives in part-12/module-58-frontier-systems-hardware, not in part-15).
  - Card 3: `Chapter 85 AGI Trajectories & Open Questions`, links to module-77-agi-trajectories. Directory says 82, index card says 85.
  - Card 4: `Chapter 86 Tools of the Trade: Frontier Research Stack`, links to module-78-tools-of-the-trade. Directory says 83, index card says 86.
- **Resolution**: PICK ONE numbering and apply across all of: (a) Part-16 index `mod-num` and `sec-num` spans, (b) each module's directory name, (c) each module index's h1 and title and breadcrumb, (d) each section's breadcrumb and h1. Right now we have THREE numberings active simultaneously (80-83 in dirs, 80-83 in module-index self-labels, 82/83/85/86 in part-15 index). My recommendation: keep the directory numbering (80, 81, 82, 83) and rename the Part-16-index chapter cards to match. The Ch-84 (Frontier Systems & Hardware) chapter physically lives in Part 12 module 58. If the intent was for it to live in Part 16, move the directory. If the intent was for Part 16 to skip it (because hardware is properly a Part-12 systems concern), drop the Ch-84 references from the Part-16 chapter-nav blurbs.
- **Ordering**: KEEP within whatever numbering scheme is chosen. Architectures -> Theory -> AGI Trajectories -> Tools-of-Trade is the standard part shape.

### Chapter 75 (per dir): Frontier Architectures & Scaling

- **Title**: KEEP if directory numbering wins; otherwise rename "Chapter 77" to match Part-16 index.
- **Description (big-picture)**: KEEP. Reasonable.
- **Looking-back callout** (line 36) has multiple stale refs:
  - "Theory of reasoning, memory, interpretability, and the agency question live in Chapter 62" -> Chapter 76 (Frontier Theory).
  - "hardware and systems live in Chapter 63" -> Chapter 58 (Part-12 module-58-frontier-systems-hardware) OR whatever the moved/renamed chapter is.
  - "AGI trajectories live in Chapter 64" -> Chapter 77.
- **Prerequisites** (lines 75-79) refs:
  - "Chapter 04: Transformer Architecture" -> Chapter 3 (part-1/module-03-transformer-architecture).
  - "Chapter 06: Pretraining & Scaling Laws" -> Chapter 6 (numbering is right, but in part-2/module-06-pretraining-scaling-laws).
  - "Chapter 10: Inference Optimization" -> Chapter 9 (module-09-inference-optimization).
- **Section descriptions**:
  - 80.1 Emergent Abilities: Real or Mirage?: PLACEHOLDER. PROPOSE "The 2022 emergent-abilities claim, Schaeffer et al.'s 2023 critique, and the current consensus that discrete-metric scaling artifacts explain most of the 'phase transition' phenomenology."
  - 80.2 Scaling Frontiers: What Comes Next: PLACEHOLDER. PROPOSE "The data wall, synthetic-data strategies, test-time compute as a new scaling axis, and the energy/economic ceilings the next decade will run into."
  - 80.3 Alternative Architectures Beyond Transformers: PLACEHOLDER. PROPOSE "Mamba, RWKV, state-space models, and the hybrid (attention + SSM) designs that 2025-26 frontier labs experimented with."
  - 80.4 has a real description. KEEP.
- **Ordering**: KEEP. Emergence -> Scaling -> Alternatives -> Beyond-text-domains is well-shaped.
- **Stale refs in section files**:
  - section-75.1.html line 24 breadcrumb: "Part XII" -> Part XV.
  - section-75.1.html line 39: "Section 7.4: Scaling Laws" -> Section 6.3 (href).
  - section-75.1.html line 39: "Section 34.1: Evaluation Fundamentals" -> Section 42.1 (href).
  - section-75.1.html line 67: "Section 7.4" -> Section 6.3.
  - section-75.1.html line 121: "Section 34.1" -> Section 42.1.
  - section-75.1.html line 135: "Section 7.3" -> Section 6.2.
  - section-75.1.html line 143: "mixture-of-experts" link to "Section 7.3" -> Section 7.3 (per href; this OK).
  - All H2 IDs in section-80.1, 80.2 use "33-1-1", "33-2-1" etc. (old Chapter 33 numbering). Update to 80.1.1, 80.2.1, etc.
- **Chapter-nav**:
  - Line 106 What's-Next: "Part XI takes you from an idea to a shipped AI product" -> Part XIV.
  - Line 109 prev: "Chapter 76: Tools of the Trade: Industry Solution Stack" link to part-14/module-74-tools-of-the-trade. Number depends on Part-15 resolution.
  - Line 111 next: "Chapter 78: Frontier Theory & Cognition" -> Chapter 76 (if dir-numbering wins).

### Chapter 76 (per dir): Frontier Theory & Cognition

- **Title**: KEEP if dir-numbering wins; else "Chapter 78".
- **Description (big-picture)**: KEEP. Strong opening (Apple "Illusion of Reasoning", Anthropic attribution-graph).
- **Section descriptions**: 81.1, 81.2, 81.3 have real descs. 81.4 description is TRUNCATED mid-sentence (line 59): "Is your smart thermostat an agent? It senses temperature, makes decisions, and takes actions without your involvement. What about a spam filter? A self-driving car? The answer depends on how you defin" — ends mid-word "defin". COMPLETE the description: "...how you define agency. This section proposes a working definition (goal directedness + autonomy + persistence + tool use) and tests it against the menagerie of systems that 2025-26 labs called 'agents'."
- **Ordering**: KEEP. Reasoning -> Memory -> Interpretability -> Agency builds from cognitive function to system property.
- **Stale refs**:
  - All section files: breadcrumb "Part XII" -> Part XV.
  - section-76.4.html H2 ID `33-8-1-defining-agency-a-framework` is old Chapter 33 numbering.
  - Line 64 What-Comes-Next: "Chapter 63" (link to part-12/module-58-frontier-systems-hardware). The Ch-63 label is from the old numbering. Either retarget to whatever the new label is or note that Frontier Systems & Hardware lives in Part 12 (Ch 58).
  - Line 67 prev: "Chapter 77: Frontier Architectures & Scaling" -> Chapter 75.
  - Line 69 next: "Chapter 84: Frontier Systems & Hardware" linking to part-12/module-58. The chapter exists but is in Part 12, not Part 16. Either move it or update the next-link to point to module-82 (skipping the cross-part hop).

### Chapter 77 (per dir): AGI Trajectories & Open Questions

- **Title**: KEEP if dir-numbering wins; else "Chapter 85".
- **Description (big-picture)**: KEEP. Strong HLE / ARC-AGI-2 / FrontierMath anchors.
- **Section descriptions**:
  - 82.1 PLACEHOLDER. PROPOSE "Humanity's Last Exam (Center for AI Safety), ARC-AGI-2 (Chollet), and FrontierMath Tier 4: the three benchmarks built to outlast the 2026 scaling cycle."
  - 82.2 PLACEHOLDER. PROPOSE "Weak-to-strong generalization, Constitutional AI, scalable mechanistic interpretability, and the alignment programs that have to scale faster than the capability programs."
  - 82.3 PLACEHOLDER. PROPOSE "The compressed (2027-2028), mainstream (2028-2032), and skeptical (post-2033) timelines, with the evidence each one rests on and the disagreement-cruxes worth tracking."
  - 82.4 PLACEHOLDER. PROPOSE "Anthropic's labor-market study, the augmentation-vs-automation finding, the 2024-25 layoffs question, and the skill-emergence pattern across professions."
  - 82.5 EMPTY desc. PROPOSE "The four threads worth carrying out of this book and into your next decade of practice: what 2026 settled, what stayed open, and the practitioner-attitude that produces good work under deep uncertainty."
- **Ordering**: KEEP. Benchmarks -> Alignment -> Timelines -> Economics -> Synthesis is well-shaped as a closing chapter.
- **Stale refs**:
  - All section files: breadcrumb "Part XII" -> Part XV.
  - section-82.1 through 82.5: ALL H2s use old `64.x.y` numbering in visible text (e.g., line "64.1.1 Humanity's Last Exam (HLE)") even though the H2 IDs use `82-1-1`. The visible text needs updating to match.
  - Line 75 What-Comes-Next: "Chapter 65" -> Chapter 78.
  - Line 78 prev: "Chapter 84" -> Chapter 76 (or wherever Frontier Theory ends up).

### Chapter 78 (per dir): Tools of the Trade: Frontier Research Stack

- **Title**: KEEP if dir-numbering wins; else "Chapter 86".
- **Description (big-picture)**: KEEP. Good arxiv/Papers-with-Code/lab-blogs/LMArena/Artificial-Analysis framing.
- **Section descriptions**: ALL FIVE placeholders `A chapter from the Building Conversational AI textbook.` PROPOSE:
  - 83.1 Platforms: "arXiv, Papers with Code, Hugging Face Papers, OpenReview, the lab publication pages (Anthropic Research, OpenAI Research, DeepMind Blog), and the live evaluation trackers (LMArena, Artificial Analysis, EvalCrafter) that frontier researchers refresh daily."
  - 83.2 Libraries & Frameworks: "lm-evaluation-harness, llm-evals, EleutherAI's pythia/gpt-neox, TransformerLens, and the interpretability tooling (saelens, neuronpedia) that the open-source frontier-research community standardized on."
  - 83.3 Datasets & Benchmarks: "MMLU, GPQA-Diamond, HLE, ARC-AGI-2, FrontierMath, SWE-Bench Verified, GAIA, OSWorld, and the eval sets that frontier labs use to claim progress."
  - 83.4 Models: "Frontier-tier (GPT-5, Claude 4 family, Gemini 2, DeepSeek-R3) and open-weight reasoning (Llama-3.3, Qwen-3, DeepSeek-V4, Mistral Large 3) models with the 2026 capability cards."
  - 83.5 External Reading & Communities: "AI Alignment Forum, LessWrong, the safety-research Substacks, the major lab-blog RSS feeds, and the workshops at NeurIPS/ICML/ICLR worth following for frontier-relevant work."
- **Ordering**: KEEP.
- **Stale refs**:
  - Line 22 breadcrumb: "Part XII" -> Part XV.
  - Line 28 pagefind meta: "Part XII" -> Part XV.
  - Line 35 big-picture: "Part XII looked at the frontiers" -> Part XV.
  - Line 76 prev: "Chapter 85: AGI Trajectories" -> Chapter 77.
  - Line 77 In-Part: "Part XII" -> Part XV.

## Appendices

The user's brief listed Appendix A (Mathematical Foundations), B (ML Essentials), C (Course Syllabi), D (Reading Pathways). The actual filesystem has Appendix A (math), B (course syllabi), C (reading pathways). There is NO ML Essentials appendix; it was deferred and the Course Syllabi appendix's reference list links to part-1/module-00-ml-pytorch-foundations as a stand-in. The numbering of Appendix B and C in their HTML page titles is also inconsistent: the Course Syllabi page calls itself "Appendix A: Course Syllabi" and the Reading Pathways page calls itself "Appendix B: Reading Pathways". The dir names use the correct b/c letters but the displayed labels do not.

### Appendices index (E:\Projects\BookBlogsHome\LLMBook\appendices\index.html)

- **Title**: KEEP.
- **Big picture**: PROPOSE rewrite. Current copy promises three groups (Foundations / Production Infrastructure / For Instructors) but the page renders only two `<h2>` placeholders ("Foundations" and "For Instructors") with NO cards/content under them, and the "Production Infrastructure" group is mentioned in the part-overview but absent from the actual rendered page. Either drop the Production-Infrastructure promise (since Docker/K8s now live in part-13/module-65) or add an empty placeholder with a pointer.
- **Cards missing**: The two `<h2>` headers have no children. Add appendix cards (Appendix A: Mathematical Foundations; Appendix B: Course Syllabi; Appendix C: Reading Pathways) with one-line descriptions and links.
- **Stale refs**: line 41 prev points to part-15/module-83/section-83.5. Reasonable as a "previous-page" link from the book end.
- **Home fit / consolidation**: The page is essentially a stub. Needs real card content.

### Appendix A: Mathematical Foundations

- **Title**: KEEP. Reasonable.
- **Description (big-picture)**: KEEP wording but fix the meta description placeholder.
- **Section descriptions**:
  - A.1 Linear Algebra Essentials, A.2 Probability and Statistics, A.3 Calculus for Machine Learning, A.4 Information Theory, A.5 Connecting the Pieces: all five lack `<span class="section-desc">` entirely (the section-card has only number + title, no description). ADD one-line descs:
    - A.1: "Vectors, matrices, eigendecomposition, SVD: the operations every transformer layer performs."
    - A.2: "Discrete and continuous distributions, expectation, variance, Bayes' rule, and the maximum-likelihood objective behind language modeling."
    - A.3: "Gradients, chain rule, backpropagation, and the optimizer family (SGD, Adam, AdamW) that trains every model in this book."
    - A.4: "Entropy, cross-entropy, KL divergence, and why the language-modeling loss is exactly the natural choice."
    - A.5: "How linear algebra, probability, calculus, and information theory plug together inside a single attention block."
  - A.6 Information Theory for Language Models: KEEP existing desc. **However, A.6 is redundant with A.4**. Either merge A.6 into A.4 (single information-theory section) or rename A.4 to "Information Theory (foundations)" and A.6 to "Information Theory for Language Models (applications)" and put A.6 inside the same chapter.
- **Ordering**: PROPOSE move A.5 (Connecting the Pieces) to be the FINAL section after A.6, since "Connecting the Pieces" is naturally a synthesis section. Current order A.1, A.2, A.3, A.4, A.5, A.6 has the synthesis before the application; flip to A.1, A.2, A.3, A.4, A.6, A.5 (or merge A.6 into A.4 then keep A.5 last).
- **Stale refs**:
  - Line 7 meta description: placeholder.
  - Line 39 pagefind meta: chapter:Appendix A — OK.
  - Line 42 figure caption: "Figure A.0.1" OK.
  - Line 49 prose: "underpin everything in Chapter 04" -> Chapter 3 (part-1/module-03-transformer-architecture).
  - Line 49: "Chapter 00 (ML and PyTorch Foundations)" -> Chapter 0.
  - Line 49: "Chapter 06 (Pretraining and Scaling Laws)" -> Chapter 6.
  - Line 49: "Chapter 34 (Evaluation)" -> Chapter 42.
  - Line 56: "Chapter 04's attention mechanism formulas" -> Chapter 3.
  - Line 56: "Chapter 06" -> Chapter 6.
  - Line 56: "Chapter 19" -> Chapter 17 (part-4/module-17-peft).
  - section-a.6.html line ?: H2 ID `4-1-2-information-theory-the-language-of-learning` carries old Chapter-4 numbering.
- **Home fit / standalone hold-up**: Appendix A's content (linear algebra, probability, calculus, information theory) is universally applicable. It holds up as standalone reference material. Several other parts of the book reference Appendix A (Course Syllabi explicitly recommends it as Track-1 fallback reading). **Confirm: hold-up YES, has unique role.** ML Essentials (the originally planned Appendix B) was supposed to cover PyTorch fundamentals, model-training mechanics, evaluation basics; this content currently lives in part-1/module-00-ml-pytorch-foundations and is NOT duplicated here. Appendix A and the part-1/module-00 content are complementary, not duplicative.

### Appendix B (dir): Course Syllabi

- **Title**: PROPOSE FIX. Page title and h1 say "Appendix A: Course Syllabi" but directory is `appendix-b-course-syllabi`. Either rename to Appendix B everywhere (preferred, matches dir) or rename the directory. Cross-reference inside Appendix C also calls this "Appendix A (Course Syllabi)".
- **Description (big-picture)**: KEEP. Reasonable framing.
- **Section content**: This appendix has no section files; the entire content is on the index page (5 tracks with week-by-week tables). KEEP this structure.
- **Ordering**: KEEP. Five tracks ordered by level (undergrad eng -> undergrad research -> grad eng -> grad research -> professional bootcamp) reads correctly.
- **Stale refs (extensive)**:
  - Line 22 breadcrumb: "Appendix A" -> Appendix B (per dir name).
  - Line 23 h1: "Course Syllabi" — OK as title text, but pagefind metadata (line 25) says "Appendix A: Course Syllabi" — should be Appendix B.
  - Line 55: "Section 6.1 (Platforms)" linked to part-1/module-05-tools-of-the-trade/section-5.1.html -> Section 5.1.
  - Line 55: "Appendix A" link to appendix-a-mathematical-foundations/index.html. -> OK if Appendix A stays as math.
  - In the week-by-week tables (lines 63-217): VERY many old chapter references in the display text (Chapter 0, 1, 2 are OK; Chapter 3, 4, 5 reasonable). Stale ones: "Chapter 13" -> 11; "Chapter 14" -> 12; "Chapter 22" -> 31; "Chapter 23" -> 32; "Chapter 24" -> 37; "Chapter 34" -> 42; "Chapter 35" -> 62; "Chapter 25" (agent safety) -> 49; "Chapter 26", "Chapter 27", "Chapter 28", "Chapter 29" OK (match new numbering); "Chapter 11" (interpretability) -> 10 (per href to module-10); "Chapter 17" (synthetic data) -> 15 (per href); "Chapter 18" (fine-tuning) -> 16; "Chapter 19" (PEFT) -> 17; "Chapter 20" (alignment) -> 18; "Chapter 31" (multimodal) -> 20 (per href to module-20-audio-music-generation); "Chapter 33" (frontiers) -> 80 (per href to part-15/module-80); "Chapter 37" (safety) -> 47 (per href to module-47-adversarial-security-red-team); "Chapter 8" (modern LLM landscape) -> 7 (per href to module-07-modern-llm-landscape); "Chapter 9" (reasoning) -> 8; "Chapter 10" (inference opt) -> 9; "Chapter 15" (hybrid) -> 13; "Chapter 31" (Strategy, week-10 bootcamp) -> 67.
  - Line 225: "Appendix B (ML Essentials)" link to part-1/module-00-ml-pytorch-foundations. As noted at the top of this section, the ML Essentials appendix doesn't exist; the link is correct but the label should say "the ML & PyTorch foundations chapter (part-1 Ch 0)" rather than "Appendix B".
  - Line 226: "Section 6.1 (Platforms)" -> Section 5.1; "Section 6.2 (Libraries & Frameworks)" -> Section 5.2.
  - Line 227: **EMPTY `<li>` with " for worked-through fixes to common end-of-chapter problems."** Either delete or fill in. Looks like the link target was removed and the leading anchor got deleted leaving just " for worked-through...".
  - Line 228: "HuggingFace Transformers Deep Dive" link to module-10-interpretability/section-10.6.html#12-2-huggingface-... -> Section 10.6 (and the anchor hash is old chapter numbering "12-2"); "LangChain Deep Dive" link with "#16-2-langchain-..." anchor -> the anchor is also old numbering.
  - Line 229: "Reading Pathways" link to appendix-c-reading-pathways/index.html. Fine target.
  - Line 233 prev: nav-num "Section O.4" — clearly an old appendix-letter numbering from pre-restructure when this appendix lived in a different position.
  - Line 235 next: nav-num "Appendix B" with title "Reading Pathways" linking to appendix-c-reading-pathways. The Reading Pathways page is in appendix-c-reading-pathways/ but is labelled as "Appendix B" inside the next-link and inside its own page title (see Appendix C below). Reconcile.
- **Clarity (pedagogical)**: Five tracks are clearly articulated, table formats consistent, prerequisites and capstones spelled out. Strong pedagogical document. After fixing the chapter-number labels, this holds up well.

### Appendix C (dir): Reading Pathways

- **Title**: PROPOSE FIX. Page title and h1 say "Appendix B: Reading Pathways" but directory is `appendix-c-reading-pathways`. Match dir.
- **Description (big-picture)**: KEEP. Reasonable.
- **Section structure**: All 8 pathways are on the index page (no separate section files). OK structure.
- **Pathway labels (the 8 pathways)**: All KEEP. RAG Engineer (weekend) -> Agent Builder (2 weeks) -> ML Practitioner Transitioning -> Researcher/Grad Student -> Interpretability & Safety -> Founder/PM -> Course Instructor -> Curious Generalist. Coverage of audiences is good.
- **Ordering**: KEEP. Pathways are ordered roughly by time commitment and audience.
- **Stale refs (extensive)**:
  - Line 20 breadcrumb: "Appendix B" -> Appendix C (per dir).
  - Line 22: Subtitle followed by a STRAY `<div class="page-current">Section D.7</div>` — leftover from when this content lived as Section D.7 of a different appendix. Remove.
  - Line 24 pagefind meta: "chapter:Chapter 0 (Section 0.1): Reading Pathways" — completely wrong, should be "Appendix C: Reading Pathways".
  - Line 27 figure caption: "Figure D.0.1" -> Figure C.0.1.
  - Pathway 1 (RAG): "Chapter 13" -> 11; "Chapter 14" -> 12; "Chapter 22" -> 31; "Chapter 23" -> 32; "Section 34.1" -> Section 42.1; "Section 35.1" -> Section 70.5 (per href).
  - Pathway 2 (Agent): "Chapter 13" -> 11; "Section 14.2" -> Section 12.2; "Chapter 26" OK; "Chapter 27" OK; "Chapter 28" OK; "Chapter 29" OK; "Chapter 25" (Agent Safety & Production) link to module-49-agent-safety-autonomy -> Chapter 49; "Chapter 34" -> Chapter 42.
  - Pathway 3 (ML Practitioner): "Chapter 0" OK; "Chapter 3" OK; "Chapter 4" -> Chapter 3; "Chapter 7" -> Chapter 6; "Chapter 8" -> Chapter 7; "Chapter 15" -> Chapter 13; "Chapter 18" -> Chapter 16; "Chapter 19" -> Chapter 17; "Chapter 34" -> Chapter 42.
  - Pathway 4 (Researcher): "Full Part I (Chapters 0–5)" — Part 1 is Ch 0-5 in new numbering OK; "Full Part II (Chapters 6-9 + 31)" — should be Ch 6-10 (Part 2 has modules 06-10); "+ 31" is unclear (could be old multimodal Ch 31). "Chapter 11 (Interpretability)" -> Chapter 10; "Full Part IV (Chapters 13-16)" -> Part 4 is modules 15-19. "Chapter 33 (Emerging Architectures & Frontiers)" -> Chapter 75 (Part 16); "Section 34.11" -> probably Section 42.5 (per href).
  - Pathway 5 (Interpretability & Safety): "Chapter 4" -> 3; "Chapter 7" -> 6; "Chapter 11" -> 10; "Chapter 25" (Agent Safety) link to module-49 -> Chapter 49; "Chapter 37" (Safety/Ethics/Regulation) link to module-47-adversarial-security-red-team -> Chapter 47; "Section 33.7 (Mechanistic interpretability at scale)" — no link, dead reference. Probably wants to link to Part 16 Section 76.3.
  - Pathway 6 (Founder/PM): "Chapter 8" -> 7; "Section 14.1" -> Section 12.1; "Section 18.1" -> Section 16.1; "Chapter 27 (LLM Applications by Industry)" no link, almost certainly meant Part 15 (Ch 72 onward); "Chapter 31 (Strategy, PM & ROI)" link to module-67-ideation -> Chapter 67 (or wherever the strategy content lands after Part 14 fix); "Chapter 45 (Building LLM and Agent Products)" link to module-67-ideation -> Chapter 67 (duplicate); "Chapter 48 (Shipping & Scaling)" link to module-70-shipping-products -> Chapter 70.
  - Pathway 7 (Course Instructor): "FM.7 Copyright & Legal" — references front-matter/copyright.html (OK, FM.7 is fine if that's the FM numbering); "Appendix A (Course Syllabi)" linked to appendix-b-course-syllabi -> Appendix B.
  - Pathway 8 (Curious Generalist): "Chapter 8" -> 7; "Chapter 9" -> 8; "Chapter 26" OK; "Chapter 33 (Frontiers)" -> Chapter 75.
  - Line 188 prev: "Appendix A: Course Syllabi" linked to appendix-b-course-syllabi -> Appendix B.
  - Line 190 next: "Appendix E: Intermediate Projects" linked to ../index.html. **No Appendix D or E exists in the appendix directory**, so this link is broken (points to appendices index page that doesn't have those entries). Either drop the next-link or actually create Appendix D and E.
- **Clarity (pedagogical)**: Eight pathways are well-articulated with time estimates, named skills, and skip-recommendations. Once chapter labels are updated, this is a strong pedagogical document.

## Summary of issue counts (by part)

| Part | Placeholder section-descs | Stale Part Roman numerals | Stale chapter/section references | Broken / spurious chapter cards |
|---|---|---|---|---|
| Part 13 | 9 section cards (4 of 5 chapters affected, plus Ch 62 missing from part index) | All breadcrumbs say "Part X" | Most section files (62.1, 62.2, 63.1, 64.1, 65.5, 66.1) | Ch 62 missing entirely from part-index |
| Part 14 | 18 section cards / index files | All say "Part XI" (also self-collisions among module 67 sections) | Pervasive across module-67 section files; module-70 has Chapter 66/45/44/31 stale refs | Part-14 index has 9 chapter cards for 5 dirs, duplicates and orphans |
| Part 15 | 12 section/index files | All say "Part XI" | Many cross-chapter labels (Ch 23, Ch 25, Ch 37, Ch 24, Ch 53, Ch 54, Ch 55, etc.) | Part-15 index has spurious 73.6, 74.6, 76.6 self-links and orphan Ch 79/80 sections in module-78 |
| Part 16 | 16 section/index files | All say "Part XII" | Looking-back callout in 80 (Chs 62, 63, 64); prereq labels mismatched | Part-16 index uses 82, 83, 85, 86 labels for modules 80, 81, 82, 83 (skips 84) |
| Appendices | All 5 sections of App A; 8 pathway code refs | N/A | Extensive in App B (Course Syllabi) tables; App C pathways have stale Ch nums throughout; App C has stray `<div class="page-current">Section D.7</div>`; App C "Appendix E" dangling next-link | App index has empty h2 headers, no cards |
