# New Sections Enrichment Audit

Read-only audit of recently-created HTML sections, flagging concrete opportunities for callouts, illustrations, diagrams, and comparison tables. Authoring agent should pick what fits the section's voice; this list is a menu, not a mandate.

Legend: `BP=big-picture` `KI=key-insight` `PE=practical-example` `WARN=warning` `TIP=tip` `LIB=library-shortcut` `WIM=why-it-matters` `FF=fun-fact` `N=note`.

---

## 1. For-Instructors Appendices (Appendices O-S)

### appendix-o-course-syllabi/index.html: Course Syllabi
Five course tracks; opens with `big-picture` and one comparison table, then 5 inline tables per track. Currently has only the opener callout; everything else is dense weekly-schedule rows. Sparse on illustration and narrative breaks.
- Add hero `<figure class="illustration">` at the top — five robot students at desks, each wearing a different graduation cap (undergrad/grad/research/bootcamp), with an instructor robot pointing at a wall chart of tracks. Currently no hero image.
- After Track Overview table: add `KI` — "Pick a track by what students will ship, not by what you'll lecture on" (tracks differ by their capstone artifact, not their syllabus reading list).
- Inside Track 1 (Undergraduate Engineering), after the week 14 row: add `PE` — "Sample graded rubric for the RAG capstone" (concrete 5-row mini-rubric so instructors can lift it).
- Inside Track 2 (Undergraduate Research), after capstone paragraph: add `TIP` — "Match the paper's compute to your students' compute" (steer instructors away from picking a 405B replication for a class with one shared 4090).
- Inside Track 5 (Professional Bootcamp), after capstone paragraph: add `WARN` — "Bootcamp burnout: 25 hr/wk for 10 weeks is at the upper end of part-time sustainable; cap office hours or pair students."
- Add diagram (mermaid or technical-diagram-designer) — branching tree: "Foundations spine (Ch 0-5) → Track A: Engineering / Track B: Research / Track C: Strategy", showing which mid-book modules each track pulls from. The five-track narrative buries this dependency graph in prose.
- Note: the Reference appendices list (line 220) has stale links (`appendix-p-course-syllabi`, `appendix-d-langchain` labelled "Appendix K") that an authoring agent should fix while enriching.

### appendix-p-reading-pathways/index.html: Reading Pathways
Eight pathway sections, each with ordered list and skip note. Opens with `big-picture`, ends with `key-insight` decision tree. The "How to Choose" decision tree is good. Pathway sections themselves have no callouts.
- Add hero `<figure class="illustration">` at top — a robot at a multi-trail trailhead with eight signposts ("RAG Engineer ↑", "Agent Builder →", etc.), reading the trail map. Currently no hero.
- After Pathway 1 (RAG Engineer) intro: add `TIP` — "Skip Chapter 14's prompt-engineering deep dive on first pass; come back when retrieval works but answers are wrong."
- After Pathway 2 (Agent Builder), Chapter 25 line: add `WARN` — "Reading Chapter 25 (Agent Safety) before you have a working agent feels theoretical; revisit it after your first failed tool call."
- After Pathway 5 (Interpretability), Chapter 11 line: add `LIB` — quick `TransformerLens` 3-line snippet that hooks one layer of GPT-2, so the pathway has a concrete artifact to point at.
- After Pathway 8 (Curious Generalist): add `FF` — "The Curious Generalist pathway is the only one a smart reader can read on an airplane in one flight" (light, but reinforces the time framing).
- Add comparison-table — "Eight pathways at a glance" (one row per pathway: goal / time / prerequisite skill / ending artifact). The pathway grid is currently 8 vertical `<section>`s; a synoptic table at the top would let readers self-select faster.
- Fix stale references while enriching: line 99 references "Appendix AI", line 134 references "Appendix AD", line 145 has broken "fm-course-syllabi" and "appendix-p-course-syllabi" links — flag for authoring agent.

### appendix-q-intermediate-projects/index.html: Intermediate Projects
Three project descriptions in plain prose, no callouts, no figures, no tables. Short page (~40 lines). Currently the most under-enriched appendix.
- Add hero `<figure class="illustration">` — three robot apprentices standing on graduated step-stools (1-week, 10-day, 2-week) between a small "lab" and a large "capstone" building.
- After the opening paragraph (line 26): add `BP` — "The intermediate-project gap: most syllabi cliff from 60-minute labs to a 6-week capstone with nothing in between. These three close that gap." Currently the opening paragraph makes this point in prose; a `big-picture` would frame the appendix.
- After Project 1 (Tokenizer Comparison Memo): add `TIP` — "Pick a corpus where token-counts will surprise you (legal documents, Hindi-English mixed text, regex patterns) — students learn more from the surprise than from the algorithm."
- After Project 2 (Prompt Engineering Pipeline): add `PE` — fully-worked tiny example, e.g., one specific zero-shot vs CoT decision row, with cost/latency numbers. Currently abstract.
- After Project 3 (RAG Failure-Mode Diagnosis): add `WARN` — "Without the 50-query holdout set, students will hill-climb the one failing query and call it done. Enforce the holdout."
- Add comparison-table — "Three intermediate projects at a glance" (project / duration / which Part it follows / pedagogical purpose / deliverable). Three free-text H3s lose at-a-glance comparability.
- Add diagram — RAG pipeline with failure-trace overlay (chunking → retrieval → reranking → generation, with red arrows showing where Project 3 students inject diagnosis probes). technical-diagram-designer is the right tool.

### appendix-r-capstone-project/index.html: Capstone Project
Three tracks + 5-dimension rubric. One comparison table (the rubric itself). No callouts, no figures, no intro `big-picture`. Short page (~50 lines).
- Add hero `<figure class="illustration">` — three robot students standing on different podiums (full-stack, API-only, research replication) holding up trophies of different shapes (a deployment dashboard, a comparison chart, a paper).
- Before Track A (line 27): add `BP` — "The capstone is the bridge from 'I read about this' to 'I shipped this.' Pick the track that matches the artifact you want on your portfolio, not the one closest to what you already know."
- After Track A (Full-stack): add `TIP` — "Track A students under-budget the deployment and monitoring; reserve the last 2 weeks for it explicitly."
- After Track C (Research replication): add `WARN` — "Choose papers whose compute budget you can reproduce; a DPO replication on a 7B model is feasible, a DeepSeek-R1 replication is not."
- After the rubric table: add `KI` — "Five dimensions, but only one decides the grade." (Failure modes in the report — dimension 4, Limitations — is where students systematically lose points; the rubric paragraph already says this but a `key-insight` would foreground it.)
- After grading note (line 44): add `PE` — "Example B+ vs A- report that both reach the same accuracy: the B+ admits a failure mode the A- pretended did not exist. The B+ wins."
- Add diagram — flowchart of the three tracks' deliverable shapes (GitHub repo / HF artifacts / report / presentation; tracks share spine but diverge on artifact type).

### appendix-s-war-stories/index.html: War Stories for Discussion
Five named production failures with prose narrative + source links. No callouts (just the H3 + paragraphs pattern). No figures. Discussion prompts are missing — the title promises them.
- Add hero `<figure class="illustration">` — a robot detective at a corkboard pinning newspaper clippings of the five incidents, with red strings connecting them to chapter numbers.
- After the opening paragraph (line 26): add `BP` — "Five stories worth discussing in class. Each maps to one or two book chapters and to a specific mitigation pattern in Appendix AE."
- After War story 1 (Air Canada) "What it teaches" paragraph: add `KI` — "A chatbot is a legal entity for the company that deployed it. Treat its outputs as binding statements, because a tribunal will."
- After War story 2 (Chevy of Watsonville): add `WARN` — "Prompt injection is the dominant production failure mode for any chatbot that takes user-supplied text. If your system has no sandbox-then-execute layer, you're one viral screenshot from this story."
- After War story 3 (Bing/Sydney): add `FF` — "Microsoft restricted Bing Chat to 5 turns within 7 days of launch. That number — 5 — became the de facto upper bound for unsupervised conversational alignment for a year." (Short, on-topic, drives the long-conversation-drift point.)
- After War story 4 (Samsung leak): add `LIB` — quick snippet showing the `anthropic` SDK's no-train header, since this is the operational mitigation. ~3 lines.
- After War story 5 (fintech $12k bill): add `PE` — a 4-line kill-switch pseudo-snippet (if `daily_spend > BUDGET: raise CircuitOpen()`), because this is exactly the artifact the story argues for.
- Add comparison-table — "Five war stories at a glance" (incident / year / failure mode / chapter to read / mitigation pattern). Five vertical H3 blocks lose at-a-glance synthesis.
- Add diagram — Sankey-style flow showing the five incidents → failure modes (prompt injection, alignment drift, data leakage, retry storm, hallucinated commitment) → mitigation patterns (P3, P7, P12, P15, P17, P19). technical-diagram-designer.
- The page title says "for Discussion" but there are no discussion prompts — flag for authoring agent: add 2-3 bullet prompts per war story (e.g., "Could prompt caching + lower default model have prevented this? Why or why not?").

---

## 2. Tools-of-the-Trade re-authored sections

### section-6.1.html: Platforms (Foundations Stack)
Currently: 1 comparison table, 1 `tip`, 1 `warning`. Two callouts — could use one more anchor and a clearer hardware visual.
- Add `<figure class="illustration">` at top — robot weighing three platforms on a balance scale (laptop / Colab badge / Kaggle badge), with cloud-GPU dollar signs in the background. Section has no hero.
- After §6.1.1 (Hardware tiers): add `KI` — "Free tiers cover all of Part I. Spend $0 on hardware until Chapter 12." Reinforces the section's central claim.
- After §6.1.2 (Hosted notebook tier): add `LIB` — 3-line snippet `from google.colab import drive; drive.mount("/content/drive")` because saving Colab work is the section's main warning.
- Section is otherwise well-balanced.

### section-6.2.html: Libraries & Frameworks
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`. Solid; only one minor opportunity.
- After §6.2.5 (Versions and compatibility): add `WARN` — "NumPy 2.x dropped `np.float`, `np.int`, and other aliases. If you import research code from 2022-23 and see `AttributeError`, that's the cause; pin `numpy<2` for that environment." Strengthens the version note.
- Otherwise well-enriched.

### section-6.3.html: Datasets & Benchmarks
Currently: 1 comparison table, 1 `warning`, 1 `tip`. Solid.
- After §6.3.5 (What "good enough" looks like): add `KI` — "If you're more than 5% below the target metric, the bug is in optimization or data, not the model." The section closes with this argument in prose; promoting it to a callout would anchor the chapter's learning loop.
- Otherwise well-enriched.

### section-6.4.html: Models
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`. Well-balanced.
- Add `<figure class="illustration">` at top — robot opening a museum case labeled "BERT-base / GPT-2" next to a closed bank vault labeled "GPT-5.5 / Claude Opus / Gemini 3.1". Visualizes the open-vs-closed dichotomy the section turns on.
- Otherwise well-enriched.

### section-6.5.html: External Reading & Communities
Currently: 1 comparison table, 1 `tip`, 1 `key-insight`. Well-balanced.
- After §6.5.2 (Blogs and newsletters): add `FF` — "Distill.pub has been dormant since 2021. The articles still rank in the top 10 results for half their topics. The lesson: clear writing outlives publication cadence." Short, on-topic, fits the section's "favor signal over volume" stance.
- Otherwise well-enriched.

### section-12.1.html: Platforms (Understanding LLMs)
Currently: 1 comparison table, 1 `warning`, 1 `tip`. Solid.
- Add `<figure class="illustration">` at top — robot looking up at a stack of GPUs labeled (top to bottom) "H100 cloud / 4090 desktop / 3060 / Apple Silicon laptop", trying to decide where to put a 70B model labeled "140 GB".
- After §12.1.2 (Hardware tier you actually need): add `KI` — "Quantization moved the goalposts. A 70B model that needed 140 GB in 2023 fits on a 24 GB consumer GPU in 2026." The section makes this point implicitly; promoting it makes the cost arithmetic memorable.
- Otherwise well-enriched.

### section-12.2.html: Libraries & Frameworks (Understanding LLMs)
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`. Well-balanced.
- After §12.2.3 (Mech-interp tier): add `TIP` — "Pin TransformerLens to the commit hash of the paper you're reproducing. Minor-version churn is the #1 reason mech-interp notebooks stop working." (Already alluded to in §12.2.5 but worth its own callout because beginners ignore the rest of the paragraph.)
- Otherwise well-enriched.

### section-12.3.html: Datasets & Benchmarks (Understanding LLMs)
Currently: 1 comparison table, 1 `warning`, 1 `tip`. Solid.
- After §12.3.4 (Mech-interp inspection datasets): add `KI` — "Mech-interp datasets are not for measuring capability; they're for measuring whether the circuit you found is the circuit the model uses." The section already states this; a callout anchors the conceptual difference for readers skimming.
- Otherwise well-enriched.

### section-12.4.html: Models (Understanding LLMs)
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`. Well-balanced.
- After §12.4.2 (Open-weight frontier): add `WARN` — "Open-weight models are not free; they ship with licenses. Llama Community License has acceptable-use restrictions; Qwen3 is Apache 2.0; DeepSeek is MIT. Read before you commercialize." Strengthens the page's licensing breadcrumbs.
- Otherwise well-enriched.

### section-12.5.html: External Reading & Communities (Understanding LLMs)
Currently: 1 comparison table, 1 `tip`, 1 `key-insight`. Well-balanced.
- After §12.5.4 (Mech-interp deep-reading): add `LIB` — One-liner snippet linking to the canonical "Anthropic Circuit Browser" (the interactive feature browser from Scaling Monosemanticity) so readers have one click to go explore. Reinforces the "subscribe to originals" theme.
- Otherwise well-enriched.

### section-16.1.html: Platforms (LLM API Stack)
**EMPTY — TODO scaffold only.** Currently a 38-line stub with "TODO author this section" placeholder content. Flag urgently for the authoring agent: needs full authorship before enrichment is meaningful. Suggested structure when authored: provider landscape (closed / aggregator / self-hosted) + auth & key management + a comparison table + at least `BP`, `KI`, `WARN`.

### section-16.2.html: Libraries & Frameworks (LLM API Stack)
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`. Well-balanced.
- After §16.2.4 (Observability libraries): add `TIP` — "Pick observability before you write the first prompt. Adding tracing after the agent ships is 5x harder than building it in from request 1." Strengthens the "centrality of the observability layer" claim from the intro.
- Otherwise well-enriched.

### section-16.3.html: Datasets & Benchmarks (LLM API Stack)
Currently: 1 comparison table, 1 `warning`, 1 `tip`. Solid.
- After §16.3.3 (Function-calling and tool-use benchmarks): add `KI` — "Tool-use benchmarks are still pre-paradigmatic in 2026. Don't trust a single number; build your own 30-prompt suite that mirrors your agent's actual tool palette." Promotes the section's already-implicit warning.
- Otherwise well-enriched.

### section-16.4.html: Models (LLM API Stack)
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`. Well-balanced.
- After §16.4.4 (Comparing the API-callable model lineup): add `WARN` — "Per-token prices change monthly. Last-cycle's flagship is next cycle's cheap tier. Re-check Artificial Analysis before any cost forecast."
- Add diagram — A simple 2D scatter of "input price ($/1M)" on x, "quality (LM Arena Elo)" on y, with the eight models from the table plotted. Visualizing the Pareto frontier makes the "default to cheap, escalate to flagship" routing pattern obvious. technical-diagram-designer.
- Otherwise well-enriched.

### section-16.5.html: External Reading & Communities (LLM API Stack)
Currently: 1 comparison table, 1 `tip`. Slightly under-enriched (2 callouts) given page length.
- After §16.5.3 (Status and incident pages): add `KI` — "Check the status page first. Half of '2 AM the prompt broke' incidents are upstream outages, not your code."
- After §16.5.4 (Communities): add `WARN` — "Reddit answers age fast. A 2024 r/LocalLLaMA workaround is often obsolete by 2026; verify against the provider doc before adopting." Strengthens the existing 'provider docs are canonical' framing.

---

## 3. Part 12 Frontiers — Modules 63 & 64

### section-63.1.html: Beyond NVIDIA
Currently: 1 comparison table, 1 `key-insight`, 1 `warning`. Solid, but missing a visual that would carry the "non-NVIDIA silicon" story.
- Add hero `<figure class="illustration">` at top — robot at a chip-design workbench with five different chips on the table (NVIDIA B200, Cerebras wafer-scale plate, Groq LPU card, Tenstorrent chiplet, AMD MI355X), labelled.
- After §63.1.2 (Groq LPU): add `FF` — "NVIDIA acquired Groq for $20B in December 2025, six months after Groq's inference-latency crown made headlines weekly. The 'Vera Rubin LPX' rack is what shipped from that deal." Concrete number, on-topic, reinforces the consolidation narrative.
- Add diagram — comparative bar chart showing memory bandwidth (TB/s) of each silicon family. The §63.1.5 key-insight argues "bandwidth matters more than FLOPs at inference" but the comparison table buries the bandwidth column. A bar chart would land the lesson. technical-diagram-designer.
- Otherwise well-enriched.

### section-63.2.html: Decentralized Training
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`, 1 `warning`. Well-enriched.
- Add diagram — sequence flow of DeMo training across heterogeneous workers: "(1) local momentum compute on each worker → (2) top-k sparse gradient extract → (3) sparse sync via Solana attestation → (4) global parameter merge". technical-diagram-designer. The text walks through this but a diagram makes the "bandwidth compression" claim concrete.
- After §63.2.4 (Comparing decentralized stack): add `TIP` — "If you're contributing GPUs to Psyche, expect a 20-30% sustained utilization tax versus a private DDP run. Verifiability isn't free." Sharpens the security/honesty story.
- Otherwise well-enriched.

### section-63.3.html: Edge LLMs
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`, 1 `tip`. Well-enriched.
- Add hero `<figure class="illustration">` at top — robot holding a phone running an LLM, with a cloud datacenter dimmed in the background. Visualizes the "edge for latency, cloud for capability" thesis from the closing `tip`.
- Otherwise well-enriched.

### section-63.4.html: FlashAttention-4
Currently: 1 comparison table, 1 `key-insight`, 1 `warning`. Solid.
- After §63.4.1 (Why each GPU generation rewrites the kernel): add `FF` — "FlashAttention has had four versions in four years. By the time you read this, FA-5 may already be in pre-print." Light, drives the kernel-as-architecture point.
- Add diagram — vertical timeline: "FA-1 (A100, 2022) → FA-2 (Hopper, 2023) → FA-3 (FP8 + warp-specialization, 2024) → FA-4 (Blackwell asymmetric SMs, 2026)", with the architectural change at each step. technical-diagram-designer.
- Otherwise well-enriched.

### section-63.5.html: Training-Inference Co-Design
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`, 1 `warning`. Well-enriched.
- Add diagram — HERMES-style multi-stage inference pipeline: prefill (Blackwell GPU) → token generation (Groq LPU or Cerebras) → retrieval/tool-use (CPU+accelerator) → vision encoder (NPU). Show data handoffs and cross-fabric copy cost. §63.5.4 describes this in prose; technical-diagram-designer would make it a teaching artifact.
- Otherwise well-enriched.

### section-64.1.html: Frontier Benchmarks
Currently: 1 comparison table, 1 `key-insight`, 1 `warning`, 1 `tip`. Well-enriched.
- Add diagram — line chart showing HLE / ARC-AGI-2 / FrontierMath scores over time (2024-2026), with frontier-model release dates annotated. The §64.1.5 closing paragraph reasons about trajectory slope; a chart makes the slope visible. technical-diagram-designer.
- Otherwise well-enriched.

### section-64.2.html: Alignment at Frontier Scale
Currently: 1 comparison table, 1 `key-insight`, 1 `warning`, 1 `practical-example`. Well-enriched.
- After §64.2.3 (Production-scale interpretability): add `FF` — "Golden Gate Claude, the May 2024 SAE demo where clamping one feature made the model obsessed with the Golden Gate Bridge, is the most-shared interpretability artifact in history. It also kicked off the production-scale mech-interp story." Brief, on-topic.
- Add diagram — alignment-stack diagram showing the three layers from the `practical-example` (RLHF/RLAIF → constitution → output classifier) as a tower with attack arrows (jailbreak → prompt injection → unsafe completion) hitting each layer. technical-diagram-designer.
- Otherwise well-enriched.

### section-64.3.html: AGI Timelines
Currently: 1 comparison table, 1 `key-insight`, 1 `warning`, 1 `tip`. Well-enriched.
- Add diagram — horizontal timeline 2026 → 2035 with five forecaster positions plotted as bars (Amodei, Hassabis, Metaculus median, Polymarket, 80kHours), each with its quartile spread. Makes the "factor-of-two disagreement" graphically obvious. technical-diagram-designer.
- Otherwise well-enriched.

### section-64.4.html: Economic Implications & Labor Market
Currently: 1 comparison table, 1 `key-insight`, 1 `warning`, 1 `practical-example`. Well-enriched.
- Add diagram — Sankey or stacked-bar showing 2025 AI interactions split 78.7% augmentation / 21.3% automation, with an arrow toward 2027 indicating uncertainty (two forks: "augmentation share holds >70%" vs "falls toward 50%"). The §64.4.5 closing question hinges on this; a diagram would make the alternative futures concrete. technical-diagram-designer.
- Otherwise well-enriched.

### section-64.5.html: What 2026 Settled
**EMPTY — TODO scaffold only.** Currently a 38-line stub with "TODO author this section" placeholder content. Flag urgently for the authoring agent. The section is the closing essay for the entire book and demands authorship before enrichment.

---

## 4. Part 10 — Building LLM and Agent Products

### section-42.1.html: Strategy & Use Case (intro)
Currently: 1 comparison table (readiness pillars), 1 `key-insight`, 1 `practical-example`, 1 `warning`. Well-enriched.
- Add hero `<figure class="illustration">` at top — boardroom robot pointing at a 60% red bar (failure rate) on a presentation slide, with engineers behind looking thoughtfully. Reinforces the §42.1.1 framing.
- After §42.1.2 (Four readiness pillars): add `TIP` — "If any pillar scores <3, pause and fix that pillar before scoping a flagship; pilot-only until level 3." The text says "an honest score below 3 ... start with a pilot, not a flagship" but a `tip` makes it operational.
- Otherwise well-enriched.

### section-42.2.html: Vendor Evaluation & Build vs Buy
Currently: 1 comparison table (decision matrix), 1 `key-insight`, 1 `warning`, 1 `practical-example`. Well-enriched.
- Add diagram — decision tree starting at "Differentiating?" → "Yes/No" → branching to seven decision matrix rows. The §42.2.1 five-question framework + §42.2.2 stack breakdown is begging for a decision tree. technical-diagram-designer.
- After §42.2.4 ("decision repeats"): add `KI` — "The build-vs-buy answer expires every two quarters. Schedule the re-evaluation in your calendar, not as a one-time decision." Promotes the closing paragraph's argument.
- Otherwise well-enriched.

### section-42.3.html: ROI / Business Case (full chapter section)
**Well-enriched, no additions needed.** 38 callouts and rich existing figures (radar charts, hero illustration). This is the heavy-detail version of the same topic introduced in 42.1.

### section-42.4.html: Vendor Evaluation (full chapter section)
**Well-enriched, no additions needed.** 38 callouts and existing figures. Heavy-detail counterpart to 42.2.

### section-46.1.html: Compute Planning intro
Currently: 1 comparison table (GPU options), 1 `key-insight`, 1 `warning`, 1 `tip`. Well-enriched.
- Add hero `<figure class="illustration">` at top — robot at a planning whiteboard with three columns labeled "training / online inference / batch", each with a GPU sticker; cost-pile chips on the desk.
- After §46.1.3 (Comparing GPU options): add `FF` — "An NVIDIA B200 has 192 GB of memory; the AMD MI355X has 288 GB. For the first time since 2019, AMD ships the largest-memory commodity GPU." On-topic and reinforces the second-source story.
- Add diagram — bar chart of GPUs by memory bandwidth (TB/s), color-coded by training-suitability vs inference-suitability. The `key-insight` argues "bandwidth > FLOPs for inference"; a chart makes it visible. technical-diagram-designer.
- Otherwise well-enriched.

### section-46.2.html: Enterprise Integration Patterns
Currently: 1 comparison table, 1 `key-insight`, 1 `practical-example`, 1 `warning`. Well-enriched.
- Add diagram — central-gateway vs sidecar-SDK architecture diagram, showing the same request flow through both patterns side-by-side. §46.2.2 describes the two patterns; a side-by-side architecture diagram is the natural artifact. technical-diagram-designer.
- After §46.2.1 (Five integration domains): add `TIP` — "Tackle Identity & Access first, Compliance second. Both block production; the others can be added incrementally." Tactical sequencing advice.
- Otherwise well-enriched.

### section-46.3.html: GPU Selection (deep)
**Well-enriched, no additions needed.** 38 existing callouts/figures.

### section-46.4.html: Breakeven Analysis (deep)
**Well-enriched, no additions needed.** 27 existing callouts/figures.

### section-47.1.html: ROI Measurement
Currently: 1 comparison table, 1 `key-insight`, 1 `warning`, 1 `practical-example`. Well-enriched.
- After §47.1.2 (Unit-cost decomposition): add `LIB` — 4-line pseudo-snippet that computes per-request cost from the three layers (inference + orchestration + integration). Concretizes the 40/30/10 split discussed in prose.
- Add diagram — three-layer cost stack (inference / orchestration / integration) with each layer's typical % share, visualizing the §47.1.2 decomposition. technical-diagram-designer.
- Otherwise well-enriched.

### section-47.2.html: Economic Design / Unit Costs
Currently: 1 comparison table, 1 `key-insight`, 1 `warning`, 1 `practical-example`. Well-enriched.
- Add diagram — breakeven chart: x-axis = utilization (0-100%), y-axis = cost per million tokens, with two lines (API flat, self-hosted slope). The §47.2.2 breakeven formula is begging for this. technical-diagram-designer.
- After §47.2.4 ("What changes at the largest scale"): add `KI` — "The self-host crossover is a utilization story, not a scale story. A 1M-request-per-day workload at 30% utilization still loses to the API; the same workload at 80% wins by 3x." Promotes the section's central argument.
- Otherwise well-enriched.

### section-47.3.html: Cost-Quality Tradeoff (deep)
**Well-enriched, no additions needed.** 40 existing callouts/figures.

### section-47.4.html: Cost Management at Scale (deep)
**Well-enriched, no additions needed.** 27 existing callouts/figures.

---

## 5. Appendix G — Problem-Solution Key

### appendix-g-problem-solution-key/index.html
Currently: 1 `key-insight` (the "How to Use This Key") + 11 lookup tables, no figures, no other callouts. It's primarily a reference lookup, so heavy callouts are not appropriate, but a few would help orientation.
- Add hero `<figure class="illustration">` at top — robot at a card catalog with drawers labeled by problem type (classification, extraction, RAG, agents, safety...), pulling out a card that says "Where to look".
- After the opening paragraph (line 90): add `BP` — "11 task categories, ~80 lookup rows. Treat this as the book's index by problem rather than by chapter." Sets reader expectation.
- After "Conversational AI and Chatbots" category (around line 404): add `TIP` — "If your task crosses categories (e.g., conversational RAG), read both rows and pick the heavier chapter set; cross-references inside chapters cover the overlap."
- After "Agents and Automation" (around line 472): add `WARN` — "Agent-related tasks span six chapters (Ch 25-29 + Ch 27). The PSK rows point you to the most relevant single chapter; build from there outward."
- After the last category (Safety, Evaluation, Governance): add `KI` — "Many of the hardest production problems sit in Safety + Evaluation rows. If you're stuck, the answer is usually 'add an eval' before it's 'try a different model.'" Promotes one of the book's recurring theses.
- Note: line 844 has a stale link to `appendix-p-course-syllabi`, line 846 to `appendix-p-freshness-2026` — flag for authoring agent to update navigation while enriching.
- No comparison-table needed (the entire page is comparison tables).
- No diagrams (the lookup-table format already serves the cross-reference purpose).

---

## Summary of enrichment priorities

**Urgent (TODO scaffolds — need authorship first):**
- `section-16.1.html` (Part III platforms)
- `section-64.5.html` (book-closing essay)

**Highest-impact additions (most under-enriched, high-traffic pages):**
1. `appendix-q-intermediate-projects` — no callouts, no figures, no comparison table; add 4-5 enrichments
2. `appendix-r-capstone-project` — no callouts, no hero, has rubric only; add 4-5 enrichments
3. `appendix-s-war-stories` — no callouts, no discussion prompts despite "for Discussion" title; add 5-6 enrichments plus a comparison table

**Hero illustrations missing on chapters that deserve them:**
- All five For-Instructors appendices (O-S)
- All five `Tools of the Trade` Platforms sections (6.1, 12.1, 16.1 once authored)
- 6.4 (Models), 63.1 (Beyond NVIDIA), 63.3 (Edge LLMs), 64.x sections, 42.1, 46.1, Appendix G

**Diagram opportunities best suited for technical-diagram-designer:**
- Appendix O: track branching tree from foundations spine
- Appendix Q: RAG pipeline with failure-trace overlay
- Appendix S: Sankey from incidents → failure modes → mitigation patterns
- 16.4: Pareto scatter of model price vs quality
- 63.1: bandwidth comparison bar chart
- 63.2: DeMo sparse-gradient sync sequence flow
- 63.4: FlashAttention version timeline
- 63.5: HERMES multi-stage inference pipeline
- 64.1: HLE/ARC/FrontierMath trajectory chart
- 64.2: three-layer alignment stack with attack arrows
- 64.3: forecaster timeline bars
- 64.4: augmentation/automation Sankey with 2027 forks
- 42.2: build-vs-buy decision tree
- 46.1: GPU bandwidth bar chart
- 46.2: gateway vs sidecar architecture (side-by-side)
- 47.1: three-layer cost-stack visualization
- 47.2: utilization breakeven chart

**Pages already well-enriched (no additions needed):**
- `section-42.3.html`, `section-42.4.html` (38 callouts each)
- `section-46.3.html`, `section-46.4.html` (38 / 27 callouts)
- `section-47.3.html`, `section-47.4.html` (40 / 27 callouts)

**Stale-link cleanups to bundle with enrichment work:**
- Appendix O: line 220 references `appendix-p-course-syllabi` and mislabels `appendix-d-langchain` as "Appendix K"
- Appendix P: line 99 `Appendix AI`, line 134 `Appendix AD`, line 145 broken `fm-course-syllabi` / `appendix-p-course-syllabi` links
- Appendix G: lines 844/846 stale `appendix-p-*` navigation links
