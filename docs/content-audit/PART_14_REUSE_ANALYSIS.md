# Part 14 Reuse Analysis

**Branch:** v2.0
**Date:** 2026-05-19
**Scope:** Identify Part 14 content that should be relocated to other chapters before Part 14 is dropped.

---

## Executive Summary

Part 14 ("Designing LLM/Agent Products") contains **36 sections** across 5 modules:

- Module 67 (Ideation): 15 sections
- Module 68 (Vibe-Coding): 6 sections
- Module 69 (LLM Economics): 3 sections
- Module 70 (Shipping Products): 7 sections (counting 70.3a and 70.3b separately)
- Module 71 (Tools of the Trade): 5 sections

**Verdict by section:**

| Recommendation | Count | Fraction |
|---|---|---|
| APPLY (clear win) | 2 | ~6% |
| CONSIDER (judgment call) | 4 | ~11% |
| SKIP (drop entirely) | 30 | ~83% |

**Headline finding:** The vast majority of Part 14 content is either (a) strategic/business framing that the book is deliberately moving away from, or (b) technical material that duplicates content already covered in dedicated chapters (Ch 11, 29, 41, 47, 62, 63, 65, 66). Only two narrow content blocks are clear wins for relocation, and four more are judgment calls. **The default answer is SKIP.**

Crucially, Chapter 69 (LLM Economics) is itself being dropped along with Part 14, so any "economics" content cannot be relocated to Ch 69; the question for cost-related content is whether it merits inserting into Ch 11.1 or Ch 57 instead, and the answer is mostly no.

---

## Per-Module Breakdown

### Module 67: Ideation (15 sections)

| Source | Description | Verdict |
|---|---|---|
| 67.1 - Ideation: Finding LLM-Worthy Problems | Strategic / problem-discovery framing | SKIP |
| 67.2 - Problem-Discovery Heuristics | PM methodology (interviews, log mining) | SKIP |
| 67.3 - Bet-My-Money Test and Capability Mapping | Strategic framing | SKIP |
| 67.4 - From Hypothesis to Product Spec | PM methodology | SKIP |
| 67.5 - LLM Product Management | PM-role content (lifecycle, eval ownership) | SKIP |
| 67.6 - UX and Iteration for LLM Products | Conversational UX framing | SKIP |
| 67.7 - LLM Strategy & Use Case Prioritization | Portfolio strategy | SKIP |
| 67.8 - LLM Vendor Evaluation & Build vs. Buy | Strategic decision framework | SKIP |
| 67.9 - What Makes AI Products Different | Probabilistic-behavior framing | SKIP |
| 67.10 - Choosing the Model's Role | Strategic taxonomy (copilot/autopilot/etc.) | SKIP |
| 67.11 - Risk and Feasibility Assessment | Risk-assessment framing | SKIP |
| 67.12 - Observe-Steer Development Loop | Methodology + IEB pattern | SKIP |
| 67.13 - Founder's Prototype Loop | Strategic / founder framing | SKIP |
| 67.14 - Documentation as Control Surface | Governance / process | SKIP |
| 67.15 - From Prototype to MVP | Hardening-checklist methodology | SKIP |

**Module 67 verdict:** SKIP ENTIRELY (15/15). This module is the strategic/business framing the book is explicitly moving away from. Examples that look concrete (Klarna AI assistant, ChatGPT launch dates) are already cited elsewhere in the book or are anchor-quality only, not load-bearing content.

---

### Module 68: Vibe-Coding (6 sections)

| Source | Description | Verdict |
|---|---|---|
| 68.1 - What Vibe-Coding Actually Means | Methodology | SKIP |
| 68.2 - Vibe-Coding & AI-Assisted Software Engineering | FIM, SWE-bench, agentic coding loop | SKIP (duplicates Ch 6.2.5 FIM, Ch 29.1 SWE-bench/ReAct loop, Ch 29.4 vendor landscape) |
| 68.3 - The AI-Native IDE Landscape in 2026 | Cursor/Aider/Claude Code comparison | SKIP (duplicates Ch 29.4 and Ch 71.1) |
| 68.4 - 80/20 Cuts (MVP scoping) | Methodology | SKIP |
| 68.5 - Vertical-Slice Pattern | Methodology | SKIP |
| 68.6 - The Four Pilot Signals | Methodology | SKIP |

**Module 68 verdict:** SKIP ENTIRELY (6/6). All technical content (FIM, SWE-bench, agentic loop, IDE vendor list) is already covered in Ch 6.2.5, Ch 29.1, Ch 29.4. The remainder is PM methodology.

---

### Module 69: LLM Economics (3 sections)

| Source | Description | Verdict |
|---|---|---|
| 69.1 - ROI Measurement & Value Attribution | Business framing (three value categories) | SKIP |
| 69.2 - Economic Design of LLM Systems | Unit-cost decomposition, breakeven formula, per-million-token table, GPT-5.5 vs Gemini Flash 3 prices, H100 vLLM throughput crossover | **CONSIDER** (specific tables and breakeven math are concrete; target is Ch 11.1 or Ch 57.1; but Ch 11.1.7 already has provider comparison and Ch 57 is hardware-cost-focused) |
| 69.3 - Token Cost Forecasting and Multi-Vendor Arbitrage | Bulk discount tiers, multi-vendor patterns | SKIP (overlaps Ch 63.1 LiteLLM + Ch 11.1.9) |

**Module 69 verdict:** Mostly SKIP. The breakeven formula and the per-million-token cost table in 69.2.2-69.2.3 are the only concrete-numbers content worth considering for migration, and even then only as a callout in Ch 11.1, not a full section.

---

### Module 70: Shipping Products (7 sections incl. 70.3a/b)

| Source | Description | Verdict |
|---|---|---|
| 70.1 - Launch Constraints and AI Unit Economics | Billing physics, token cost calculator code, deployment platforms table, OWASP LLM Top 10, EU AI Act, launch readiness checklist | **CONSIDER** (token cost calculator code is unique-ish; OWASP/EU AI Act duplicate Ch 47; checklist is methodology) |
| 70.2 - AI Copilots Across the Lifecycle | Use LLMs to write user stories, devil's advocate prompts | SKIP (pure PM methodology) |
| 70.3a - Vendor Lock-in vs. Cognitive Lock-in / AI Continuity / Portable Monogamy | Strategic framing + provider abstraction layer code | SKIP (strategic framing is exactly the content being dropped; the abstraction-layer code duplicates LiteLLM coverage in Ch 63.1.2) |
| 70.3b - Multi-Provider Routing / Portability Checklist | Multi-provider router implementation, anti-patterns | SKIP (duplicates Ch 63.1.3 fallback chains + Ch 63.1.2 LiteLLM) |
| 70.4 - Post-Launch Product Monitoring and Iteration | Drift detection, A/B testing, user feedback, cost monitoring, dashboard | SKIP (duplicates Ch 44.2 dashboards, Ch 44.4 drift + user feedback, Ch 62.2.2 A/B framework) |
| 70.5 - Application Architecture & Deployment | FastAPI three-layer architecture, SSE streaming, Docker Compose, AWS Bedrock, Modal serverless | SKIP (duplicates Ch 9.4 inference serving, Ch 11.1.2.2 SSE streaming, Ch 65.3 Docker Compose RAG stack) |
| 70.6 - Frontend & User Interfaces | Gradio / Streamlit / Chainlit / Vercel AI SDK chat code | SKIP (duplicates Ch 41.2.3 Chat UI frameworks) |

**Module 70 verdict:** Mostly SKIP. The token cost calculator in 70.1.1 is the only piece worth even considering, and it overlaps both Ch 11.1 (pricing) and the dropped Ch 69.

---

### Module 71: Tools of the Trade (5 sections)

| Source | Description | Verdict |
|---|---|---|
| 71.1 - Platforms | AI-native code editors (Cursor, Claude Code, etc.), text-to-app platforms (Bolt.new $20M ARR), Deployment Patterns sub-section (canary/blue-green/shadow/A/B with Flagger YAML), SLOs/Alerting/FinOps sub-section (Prometheus YAML rules, cost optimization table) | **APPLY (partial)** - The "Deployment Patterns" and "SLOs/FinOps" tot-subsections are chapter-grade with concrete YAML and numbered tables; some content overlaps Ch 66.1 SLOs but the YAML rules and Prometheus alert rules are unique |
| 71.2 - Libraries & Frameworks | 2026 reference stack diagram (Modal/Groq/Cloudflare/Vercel), FastAPI 50-line streaming chat example, MLOps Plumbing sub-section with GitHub Actions YAML for model deployment | **APPLY (partial)** - The "MLOps Plumbing" sub-section (lines 217-301: reproducibility checklist + GitHub Actions workflow YAML + validate_model.py) is a clean, self-contained piece that fits Ch 65 or Ch 66.2; the rest of 71.2 duplicates other tools-of-the-trade content |
| 71.3 - Datasets & Benchmarks | SWE-bench, SWE-Lancer, HumanEval, CodeContests | **CONSIDER** - The SWE-Lancer entry (OpenAI 2025, dollar-denominated Upwork jobs) is a genuinely new benchmark that Ch 29.1 does not mention; could be a one-paragraph addition to Ch 29.1 |
| 71.4 - Models | Model-to-product matrix (Cursor/Claude Code/Copilot defaults) | SKIP (overlaps Ch 7.1b model landscape and Ch 29.4 coding vendors) |
| 71.5 - External Reading & Communities | Books / blogs / podcasts | SKIP (purely a reading list, low value to relocate) |

**Module 71 verdict:** Mostly SKIP, with two narrow APPLY targets (the GitHub Actions CI/CD workflow in 71.2 and the deployment-patterns/SLO tot-subsections in 71.1) and one CONSIDER (SWE-Lancer in 71.3).

---

## APPLY / CONSIDER Recommendations Ranked

### APPLY #1: GitHub Actions Model Deployment Workflow

- **Source:** `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html` lines 174-302 (the "MLOps Plumbing: GitHub Actions for Model Deployment" subsection inside the embedded `tot-subsection`)
- **Description:** Self-contained subsection covering: (a) reproducibility checklist (pin deps, seeds, DVC, hardware logging); (b) a complete GitHub Actions workflow (Code Fragment I.4.3) that pulls a registered MLflow model, runs validation gates, builds a Docker image with `mlflow models build-docker`, and rolls out to staging; (c) a `validate_model.py` helper (Code Fragment I.4.4); (d) a Collaboration Toolkit Summary takeaway list.
- **Target:** `part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.2.html`, after section 66.2.4 (Model Registry) or as a new 66.2.5
- **Rationale:** Ch 66.2 covers W&B/MLflow model registry, aliases, validation gates, and the registry-side `validate_and_promote()` function. It does NOT currently show the CI/CD-side caller (the GitHub Actions YAML and the `validate_model.py` wrapper) that consumes the registry. The 71.2 content explicitly references Ch 66.2's registry-side function and is the missing companion piece.
- **Risk:** Low. The 71.2 subsection already cross-references Ch 66.2 (`Section 19.2 (Libraries & Frameworks)`) and treats Ch 66.2 as the upstream; relocating the CI/CD-caller-side here completes the loop.
- **Edit instructions:** Insert a new subsection "66.2.5 CI/CD Integration: From Registry to Deployment" after the current 66.2.4. Move the prose paragraphs around Code Fragments I.4.3 and I.4.4 (lines 217-302 of 71.2), keeping the cross-reference to 66.2's `validate_and_promote()` function. Drop the surrounding section-71.2 navigation. Rewrite the opening paragraph to remove the "next step after reproducibility checklist" framing (which no longer applies) and replace with "Once a model version is promoted in the registry (Section 66.2.4), CI/CD consumes that alias to validate, containerize, and deploy."

### APPLY #2: SWE-Lancer Benchmark Entry

- **Source:** `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.3.html` lines 91-92 (the SWE-Lancer bullet in 71.3.1)
- **Description:** Single bulleted entry: "SWE-Lancer (OpenAI, 2025) is the monetary-value coding benchmark built from real Upwork freelance jobs, with each task carrying a dollar amount. Pick SWE-Lancer for ROI-framed analysis; the dollar values make procurement conversations more concrete." Plus the comparison figure (71.3.1) positioning SWE-Lancer relative to SWE-bench.
- **Target:** `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html`, immediately after the existing SWE-bench paragraph in the Further Reading or as an inline mention
- **Rationale:** Ch 29.1 already covers SWE-bench in depth but does not mention SWE-Lancer, which is the natural "what comes next" benchmark for coding agents. SWE-Lancer is a 2025-vintage benchmark from OpenAI; adding it keeps Ch 29.1 current.
- **Risk:** Low. One-paragraph or one-bibliography-entry addition.
- **Edit instructions:** Add one bibliography card to the "Coding Agents" bibliography group in section-29.1.html: "Miserendino, S. et al. (2025). SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering? OpenAI." Optionally add one sentence in the exercises area: "For ROI-framed procurement analysis, see also SWE-Lancer, which assigns dollar values to each task."

### CONSIDER #1: Deployment Patterns + SLO Subsections from 71.1

- **Source:** `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html` lines 120-230 (Deployment Patterns: canary/blue-green/shadow/A/B + Flagger YAML) and lines 230-300+ (SLOs, Alerting, and FinOps: Prometheus alert YAML, cost optimization table)
- **Description:** Two large `tot-subsection` blocks. Deployment Patterns has the four-pattern explanation, a Flagger Canary YAML for vLLM, real-world vendor cases (GitHub Copilot, Notion AI, Cursor). SLOs subsection has Prometheus alert rules for cost/hallucination SLOs and a "three cost optimization strategies" comparison table.
- **Target:** Ch 66.1 (Reliability SLOs) for the SLO/Alerting/FinOps piece; Ch 62.2 (A/B Testing Framework) or new section in Ch 62 for the Deployment Patterns piece.
- **Rationale:** The Flagger YAML (concrete config), Prometheus alert YAML, and the cost-optimization comparison table are genuinely additive to Ch 66.1.6 (which has Python `SLOTracker` but no Prometheus YAML) and Ch 62.2.2 (which has A/B testing but no canary/blue-green/shadow taxonomy with Flagger).
- **Risk:** Medium. Some duplication with existing Ch 66.1.6 SLO content; the framing of canary/blue-green/shadow has overlap with the existing "Deployment Patterns Summary" in section 66.2 (line 345 in section-66.2.html). Whoever does this relocation must carefully merge rather than copy-paste, and the rewrite is non-trivial.
- **Edit instructions:** Two-phase. Phase 1: extract the Flagger YAML + the four-pattern comparison table from 71.1 and merge into Ch 66.2.4 or as new Ch 66.2.5, removing the duplicate prose. Phase 2: extract the Prometheus alert rules YAML + cost-strategy comparison table from 71.1 and merge into Ch 66.1.6 (SLOs) as an "Alerting Rules" sub-subsection. Defer this one to a follow-up pass if budget is tight; it is the highest-judgment item in the list.

### CONSIDER #2: Token Cost Calculator from 70.1.1

- **Source:** `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.1.html` lines 93-160 (the `ModelPricing` / `UsageProfile` / `estimate_cost` Python code and the "four forces driving per-request cost" enumeration)
- **Description:** A Python cost calculator that models per-request and projected monthly costs for three model tiers (frontier / mid / small) accounting for prompt-caching hit rates, plus the "Cost-Driven Architecture" worked example (customer-support startup, $2000 to $600 with model routing).
- **Target:** Ch 11.1.7 (Provider Comparison) or end of Ch 11.1.9 (Choosing Between Providers)
- **Rationale:** Ch 11.1 has the provider-comparison table but no concrete cost calculator and no worked monthly-cost projection. The token cost calculator is genuinely useful and Ch 11.1 currently ends without giving the reader a "now plug your numbers in" artifact.
- **Risk:** Medium. The calculator hard-codes specific prices (frontier @ $2.50/$10) that will drift; presents a maintenance liability. The "Cost-Driven Architecture" example refers to model routing in "Ch 67" which is being dropped, so the cross-reference must be updated to point to Ch 63.1 instead.
- **Edit instructions:** Insert as a new sub-subsection "11.1.9.1 Estimating Per-Request and Monthly Costs" at the end of section 11.1.9. Strip the "as of early 2026" hedging by adding a `# CHECK PROVIDER PAGES FOR CURRENT RATES` comment in the code; this is already there but should be made prominent. Update the "model routing strategy" cross-reference from Ch 67 to Ch 63.1.2 (LiteLLM proxy). Skip if the prices in Ch 11 are intended to stay table-driven only.

### CONSIDER #3: Breakeven Formula from 69.2

- **Source:** `part-14-designing-llm-agent-products/module-69-llm-economics/section-69.2.html` lines 119-145 (the breakeven formula 69.2.2 + the per-million-token cost table 69.2.3 + the figure showing utilization-breakeven curve)
- **Description:** The formula `(rented_GPU_hourly_cost / GPU_throughput_tokens_per_hour) < (API_price_per_token × actual_utilization)` with worked example for H100 at $3/hr running Llama-4-70B at 4-bit → 3500 tok/sec → $0.24 per 1M tokens, plus the comparison table and "self-hosting wins at 80% utilization" insight.
- **Target:** Ch 57.1 (Compute Planning), as a new 57.1.5 "Self-Host vs API Breakeven" or end of 57.1.3 (Comparing the GPU options)
- **Rationale:** Ch 57 covers GPU tiers and capacity planning but does NOT currently include the self-host-vs-API economic breakeven analysis. The breakeven formula is genuinely useful and is at the right level for Ch 57. Note: Ch 69 is also being dropped along with Part 14, so this content disappears entirely if not relocated.
- **Risk:** Medium. The mid-2026 prices ($3/M tokens for GPT-5.5, $0.15 for Gemini Flash 3) will date quickly. Also, the framing in 69.2 is "you're a PM deciding architecture" while Ch 57 is "you're an engineer planning compute"; the relocation must rewrite the framing.
- **Edit instructions:** Insert as new 57.1.5 "Self-Host vs API Breakeven Analysis" with the formula, the H100 worked example, and the breakeven-at-80% figure. Drop the per-million-token table (replace with a `link: see Artificial Analysis for current pricing`). Rewrite the opening paragraph to anchor on hardware-utilization economics rather than PM decision-making.

### CONSIDER #4: 2026 AI-Product Reference Stack Diagram (71.2)

- **Source:** `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html` lines 40-115 (the SVG figure showing Next.js + Vercel AI SDK frontend → FastAPI streaming SSE backend → Modal/Groq/Cloudflare Workers AI/Vercel as model layer)
- **Description:** A 2026-vintage architecture diagram naming specific vendors (Modal 200ms cold start, Groq sub-100ms TTFT, Cloudflare 300+ POPs, livekit/vapi for voice).
- **Target:** Ch 41.2 or Ch 9.4 (inference serving)
- **Rationale:** The diagram captures the "where does inference run in 2026" question concretely with specific latency numbers; it would freshen up either inference-serving (Ch 9.4) or conv-AI-stack (Ch 41.2). However, the specific vendor names will date within 18 months.
- **Risk:** Medium. The 50-line streaming-chat code example (Code Fragment 71.2.1) duplicates Ch 11.1.2.2 (SSE streaming) and Ch 41.2.9 (streaming and real-time token handling).
- **Edit instructions:** Lift only the SVG diagram and one accompanying paragraph; place in Ch 9.4 or Ch 41.2 as a high-level orientation figure. Drop the code fragment. Annotate the figure with a "as of mid-2026" caption.

---

## Definitive SKIP List

Every other section in Part 14 should be **deleted without relocation**. The strategic / business / PM framing content (Module 67, Module 68 methodology, 70.2, 70.3a strategic framing, 67-style decision frameworks throughout) is the exact material the book has decided to drop. The technical content that looks worth saving (FastAPI architecture, Docker Compose, OWASP, drift detection, A/B testing, vendor lock-in abstraction layers, multi-provider routing, IDE landscape, FIM, SWE-bench, vendor-product matrices, deployment platforms tables) all duplicates content that is already present in the book's dedicated chapters:

- Ch 6.2.5 covers FIM
- Ch 7.1b covers the model landscape
- Ch 9.4 covers inference serving and FastAPI
- Ch 11.1 covers LLM APIs, streaming, pricing comparison
- Ch 29.1 covers SWE-bench and code-agent patterns
- Ch 29.4 covers coding-tool vendors (Cursor, Claude Code, Devin, Aider, Copilot Workspace)
- Ch 41.1, 41.2 cover conversational-AI platforms and chat UI frameworks (Gradio/Streamlit/Chainlit/Vercel AI SDK)
- Ch 44.2 covers production observability dashboards
- Ch 44.4 covers drift detection and user feedback loops
- Ch 47.1 covers OWASP LLM Top 10 / prompt injection
- Ch 62.1 covers production engineering core (latency, backpressure, guardrails, memory)
- Ch 62.2 covers A/B testing, prompt versioning, model registry
- Ch 63.1 covers AI gateways, LiteLLM, fallback chains, model routing
- Ch 65.2 covers Dockerfile basics
- Ch 65.3 covers Docker Compose RAG stack
- Ch 66.1 covers reliability, resilience patterns, circuit breakers, SLOs, incident response, chaos
- Ch 66.2 covers model registry, aliases, validation gates, deployment patterns summary

Move nothing else. The Part 14 archive at `_archive/part-14-dropped-snapshot/` already exists and serves as the long-term reference if any deeper migration is requested later.

---

## Implementation Order

If/when these recommendations are executed, run in this order:

1. **APPLY #2 (SWE-Lancer)** - 5 minutes, one-line bibliography addition to Ch 29.1.
2. **APPLY #1 (GitHub Actions CI/CD workflow)** - 30 minutes, insert as new Ch 66.2.5 with prose rewrite. Verify cross-references to `validate_and_promote()` resolve.
3. *(Optional)* **CONSIDER #3 (Breakeven formula)** - 45 minutes, insert as Ch 57.1.5 with framing rewrite. Drop dated pricing table.
4. *(Optional)* **CONSIDER #2 (Token cost calculator)** - 30 minutes, insert as Ch 11.1.9.1 with `# CHECK CURRENT RATES` comment and updated cross-reference.
5. *(Defer)* **CONSIDER #1 (Deployment patterns + SLO YAML)** - 1.5 hours, careful merge with existing Ch 66.1.6 and Ch 66.2. High judgment; consider whether the existing chapters already say enough.
6. *(Optional)* **CONSIDER #4 (2026 stack diagram)** - 15 minutes, lift SVG into Ch 9.4 or Ch 41.2.

After step 2, ~94% of the reuse value has been captured. Steps 3-6 are all optional and represent diminishing returns.
