# Hallucination Audit: New Tools/Topic Chapters (v2.0)

Spot-check of substantial factual claims in the seven "new" chapters introduced in v2.0:
Ch 34 NER, Ch 36 Retrieval Tools, Ch 41 Conv AI Tools, Ch 46 LLM-as-Judge,
Ch 56 Responsible AI Tools, Ch 59 Distributed Training, Ch 61 Scale Tools.

Methodology: ~5 substantial claims sampled per chapter, focused on numeric
claims, launch dates, vendor pricing, capability claims about specific models,
and citation accuracy. Sampled, not exhaustive.

Severity legend:
- **HIGH**: factually wrong, will mislead readers.
- **MEDIUM**: imprecise, dated, or rounded in a way that misrepresents.
- **LOW**: minor stylistic or attribution slip, easy to fix.
- **OK**: claim verified against public sources.

---

## Chapter 34: Structured Information Extraction & NER

Files:
`part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.{1..5}.html`

| # | Claim | Source line / file | Verdict |
|---|-------|--------------------|---------|
| 34-1 | "spaCy's modern transformer-based models (en_core_web_trf) can process over 10,000 documents per second" (Section 34.2 Fun Fact) | `section-34.2.html` line ~30 | **MEDIUM**. spaCy's published benchmarks show `en_core_web_trf` at roughly 100-700 docs/sec on CPU and ~5,000-10,000 words/sec, not docs/sec. The figure "10,000 docs/sec" likely conflates words/sec with docs/sec. Verify the unit; if kept, change to "words per second" or "thousands of tokens per second". |
| 34-2 | "Stanford OpenIE (Angeli et al., 2015) pioneered the modern approach to schema-free extraction." | `section-34.2.html` line 141 | **OK**. Angeli, Premkumar & Manning "Leveraging Linguistic Structure For Open Domain Information Extraction" was ACL 2015. |
| 34-3 | "REBEL (Cabot and Navigli, 2021) ... REBEL supports over 200 relation types from Wikidata" | `section-34.2.html` line 142 | **MEDIUM**. REBEL was Cabot & Navigli, EMNLP Findings 2021. The relation count is actually **220 relation types from Wikidata** in the original release; "over 200" is technically correct but slightly underestimates. OK to keep but tightening to "220+" is more precise. |
| 34-4 | Case study: "Obligation extraction accuracy improved from 71% to 89% F1" | `section-34.5.html` line 127 | **UNVERIFIABLE** (anonymized case study). Plausible range but no source. Acceptable as illustrative if labeled as a composite. |
| 34-5 | "End-to-end neural coreference (Lee et al., 2017): The landmark paper that eliminated the need for a separate mention detection step." | `section-34.5.html` line 39 | **OK**. Lee, He, Lewis & Zettlemoyer "End-to-end Neural Coreference Resolution," EMNLP 2017. |

Overall: low hallucination rate. The one claim worth fixing is **#34-1** (unit confusion on spaCy throughput).

---

## Chapter 36: Retrieval Tools of the Trade

Files: `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.{1..5}.html`

| # | Claim | Source line / file | Verdict |
|---|-------|--------------------|---------|
| 36-1 | "Turbopuffer (Turbopuffer, 2024)" | `section-36.1.html` line 34 | **OK**. Turbopuffer launched in 2024 (their public release / Series A was 2024). |
| 36-2 | "OpenAI text-embedding-3-large emits 3072-dimensional vectors at $0.13 per 1M tokens... 8191 tokens context" | `section-36.4.html` line 33 | **OK**. All three numbers match OpenAI's published spec sheet for text-embedding-3-large. |
| 36-3 | "BGE-M3 ... Context length is 8192 tokens; trained on 194 languages" | `section-36.4.html` line 42 | **MEDIUM**. BGE-M3's HF model card lists "**100+ languages**" with no specific count of 194. The published BGE-M3 paper (Chen et al., 2024) trains on a multilingual corpus from CC and mC4 with "100+ languages." The figure 194 is suspicious / not in the canonical sources. Recommend changing to "100+ languages" unless 194 can be sourced. |
| 36-4 | "MS MARCO ... 1M passages, 500K queries" (in claim that "almost every open embedder in Section 36.4 was trained on it") | `section-36.3.html` line 33 | **MEDIUM**. MS MARCO passage v1 has ~8.8M passages and ~1M training queries; the "1M passages, 500K queries" figures are inverted/wrong. The number 1M sounds like training queries (close to 1M), and 500K is closer to nothing canonical. Recommend cross-check against `microsoft.github.io/msmarco/`. |
| 36-5 | "BEIR (Thakur et al., 2021) is the zero-shot heterogeneous retrieval benchmark covering 18 datasets across 9 domains" | `section-36.3.html` line 45 | **OK**. BEIR paper, Thakur et al. NeurIPS 2021, "18 datasets" matches the canonical count. The "9 domains" matches the paper's classification. |
| 36-6 | "FRAMES (Google, 2024) ... single-hop RAG gets 40-50%, advanced agents 60-70%" | `section-36.3.html` line 54 | **OK** but **MEDIUM** on the range. FRAMES paper (Krishna et al., 2024) reports baseline retrieval ~40% on simple Q's, agents ~70%. Range is roughly accurate but specific numbers vary by setup; flag as approximate. |

Overall: **#36-3 (BGE-M3 "194 languages")** and **#36-4 (MS MARCO passage/query counts)** are the two material errors.

---

## Chapter 41: Conversational AI Tools of the Trade

Files: `part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.{1..5}.html`

| # | Claim | Source line / file | Verdict |
|---|-------|--------------------|---------|
| 41-1 | "Character.AI Studio (Character.AI, 2022) ... hundreds of millions of monthly messages at peak" | `section-41.1.html` line 64 | **MEDIUM** (understated). Character.AI reported peaks of ~20K queries/sec → roughly **2 billion** messages per month at peak, not "hundreds of millions". "Hundreds of millions monthly" is conservative and arguably wrong by 5-10×. Recommend "billions of messages per month" or remove the figure. |
| 41-2 | "Microsoft's 2024 acqui-hire of Inflection's leadership" | `section-41.1.html` line 66 | **OK**. Mustafa Suleyman + many Inflection staff joined Microsoft in March 2024. |
| 41-3 | "Dialogflow CX (Google, 2020; LLM-augmented 2024)" | `section-41.1.html` line 36 | **OK**. Dialogflow CX launched at Google Cloud Next '20 (Sept 2020). Generative Agents feature was 2024. |
| 41-4 | "OpenAI Realtime API (OpenAI, Oct 2024)" | `section-41.1.html` line 58 | **OK**. Realtime API was announced October 1, 2024 (DevDay). |
| 41-5 | "(Anthropic, 2024-2025) Anthropic Projects... shared workspaces in Claude where a system prompt, an uploaded knowledge corpus (PDFs, docs), and an artifact-rendering surface are bundled" | `section-41.1.html` line 42 | **OK**. Projects announced June 2024. |

Overall: low hallucination rate. The one claim worth tightening is **#41-1** (Character.AI scale is meaningfully understated).

---

## Chapter 46: LLM-as-Judge & Automated Evaluation

Files: `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.{1..5}.html`

| # | Claim | Source line / file | Verdict |
|---|-------|--------------------|---------|
| 46-1 | "GPT-4 acting as a judge rated GPT-4's own outputs as the best response 67% of the time, compared to 50% when judging between two other models of equal quality." | `section-46.1.html` line 114 (Fun Fact) | **MEDIUM**. The 67% number is **not** in the standard Zheng et al. 2023 "Judging LLM-as-a-Judge" (MT-Bench) paper, which reports a self-bias of ~10 percentage points above neutral, not 17. Verify the exact source; if a paper says 67% explicitly, cite it. If not, soften to "above 60% in some studies" or remove. The "narcissism bias" framing is fine, the specific number isn't sourced. |
| 46-2 | "G-Eval, introduced by Liu et al. (2023)" | `section-46.2.html` line 26 | **OK**. Liu, Iter, Xu, Wang, Xu, Zhu, "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment," EMNLP 2023. |
| 46-3 | "Prometheus (Kim et al., 2023) and Prometheus 2 (Kim et al., 2024)" | `section-46.3.html` line 26 | **OK**. Kim et al., "Prometheus: Inducing Fine-Grained Evaluation Capability in Language Models," 2023 (released as NAACL 2024 paper); Prometheus 2 was Kim et al. 2024. |
| 46-4 | "JudgeLM (Zhu et al., 2023)" | `section-46.4.html` line 26 | **OK**. Zhu, Wang, Zhang "JudgeLM: Fine-tuned Large Language Models are Scalable Judges," arXiv 2023. |
| 46-5 | "AlpacaEval (Li et al., 2023) ... on a curated set of 805 instructions" | `section-46.5.html` line 26 | **OK**. AlpacaEval canonical test set is exactly 805 instructions. |

Overall: one questionable Fun-Fact number (**#46-1**). Citations are solid.

---

## Chapter 56: Responsible AI Tools of the Trade

Files: `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.{1..5}.html`

| # | Claim | Source line / file | Verdict |
|---|-------|--------------------|---------|
| 56-1 | "The EU AI Act entered force in August 2024" | `section-56.1.html` line 32 | **OK**. Regulation (EU) 2024/1689 entered force 1 August 2024. |
| 56-2 | "the NIST AI Risk Management Framework's Generative AI Profile shipped in July 2024" | `section-56.1.html` line 32 | **OK**. NIST AI 600-1 was released 26 July 2024. |
| 56-3 | "AI Fairness 360 (AIF360) ... 70+ bias metrics and 12+ mitigation algorithms" | `section-56.1.html` line 69 | **OK** (slightly conservative). AIF360 docs claim 75+ metrics, 13 mitigation algorithms; "70+" and "12+" are correct lower bounds. |
| 56-4 | Citation: "Rauber, A., et al. (2024). NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications." | `section-56.1.html` line 187 | **HIGH**. The canonical NeMo Guardrails paper is **Rebedea, Dinu, Sreedhar, Parisien, Cohen** (NVIDIA, 2023), "NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails," EMNLP 2023. There is no "Rauber, A." as lead author of NeMo Guardrails. This author name is hallucinated. Fix to "Rebedea et al. (2023)". |
| 56-5 | "ISO/IEC 42001:2023 ... the first certifiable AI management-system standard" | `section-56.1.html` line 190 | **OK**. ISO/IEC 42001:2023 published December 2023, is indeed certifiable. |

Overall: **#56-4 is the one outright hallucination** (wrong author for a real paper). Other claims hold up.

---

## Chapter 59: Distributed Training Systems

Files: `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.{1..5}.html`

| # | Claim | Source line / file | Verdict |
|---|-------|--------------------|---------|
| 59-1 | AdamW state: "18 bytes per parameter" (2 bf16 + 4 master fp32 + 4 grad + 4 m + 4 v) | `section-59.1.html` line 43 | **OK**. Standard mixed-precision AdamW accounting. |
| 59-2 | "Llama-3 405B ... 16,000 H100 ... 54 days ... 419 (Meta paper) ... ~7.7 hours MTBF / 1k GPUs" | `section-59.5.html` table 59.5.1 | **OK** with minor caveat. The Llama-3 paper reports **466 unexpected interruptions** total over 54 days, of which 419 had specific root-cause classifications. The 419 figure is the most commonly cited number from the paper's failure-cause table. MTBF math is right. |
| 59-3 | "GPipe (Huang et al., 2019) ... 1F1B (Narayanan, 2019)" | `section-59.4.html` lines 39, 50 | **MEDIUM**. GPipe attribution is correct (Huang et al., NeurIPS 2019). The "1F1B (Narayanan, 2019)" attribution is **imprecise**: 1F1B was introduced in PipeDream (Narayanan et al., SOSP 2019) but is canonically associated with PipeDream-Flush / Megatron-LM (Narayanan et al., SC 2021). The 2019 reference works if pointing at PipeDream, but most readers would expect the 2021 Megatron-LM paper. Tighten to "Narayanan et al., 2021" or cite both. |
| 59-4 | "zero-bubble pipeline (Qi et al., 2023)" | `section-59.4.html` line 39 | **OK**. Qi, Wang, Yang, Yu, Lin, "Zero Bubble Pipeline Parallelism," 2023. |
| 59-5 | "Llama-3 paper reports 38-43% MFU at 405B scale" | `section-59.5.html` line 128 | **OK**. The Llama-3 paper reports ~41% MFU at 405B on H100. The 38-43 range is consistent. |
| 59-6 | "Megatron-LM (Shoeybi et al., 2019) showed that a transformer's MLP and attention blocks can be partitioned across $T$ GPUs with exactly two all-reduces per transformer block" | `section-59.3.html` line 39 | **OK**. Shoeybi et al. "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism" (2019). |

Overall: only **#59-3 (1F1B attribution year)** is borderline; rest is solid.

---

## Chapter 61: Scale Tools of the Trade

Files: `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.{1..5}.html`

| # | Claim | Source line / file | Verdict |
|---|-------|--------------------|---------|
| 61-1 | "xAI Colossus ... 100,000 H100 cluster that came online in 122 days" | `section-61.1.html` line 60 | **OK**. xAI publicly stated the Memphis Colossus 100K-H100 build was completed in 122 days (Sept 2024). |
| 61-2 | "Stargate joint venture announced in 2024 (a $100B+ multi-year datacenter program with Microsoft, Oracle, and SoftBank)" | `section-61.1.html` line 56 | **MEDIUM**. Stargate was officially announced January 21, 2025 (not 2024). The figure is **$500B over 4 years**, with $100B initial commitment. "$100B+" is technically correct but misleading. Fix year to 2025 and consider revising figure to "$500B over 4 years, with $100B initial commitment." |
| 61-3 | "Meta ... ~350,000 H100-equivalents by end of 2024 with plans for 1M+ accelerators by end of 2025" | `section-61.1.html` line 59 | **MEDIUM**. Zuckerberg's Jan 2024 statement was "350K H100s + ~600K H100-equivalents in additional GPUs = ~950K H100-equivalents by end of 2024," **not 350K H100-equivalents total**. The 350K figure is just the H100 count. By Jan 2025 he said the goal was "more than 1.3M GPUs" by end of 2025. The book's "350K H100-equivalents" understates by roughly 2.7×. Recommend rewording to "350K H100s plus equivalents in other accelerators, ~950K total H100-equivalents." |
| 61-4 | "FineWeb ... 15-trillion-token English-language web corpus filtered from 96 CommonCrawl snapshots" | `section-61.3.html` line 33 | **OK**. FineWeb is 15.5T tokens from 96 CC snapshots. |
| 61-5 | "Llama-3 disclosure indicated roughly 50 percent general web, **25 percent code, 17 percent multilingual, 8 percent math**" | `section-61.3.html` line 87 | **HIGH**. The Llama-3 paper's data-mix disclosure was **50% general knowledge, 25% mathematical and reasoning data, 17% code, 8% multilingual** (per the Llama-3 paper, Section 3.1.1). The book has **code and math swapped**, and the multilingual share is misordered. Fix to "50% general web, 25% math/reasoning, 17% code, 8% multilingual." |
| 61-6 | "MLPerf Training ... GPT-3 175B, Stable Diffusion, Llama 2 70B LoRA, Llama 3.1 405B in 2024-25" | `section-61.3.html` line 67 | **OK**. MLPerf Training v4.1 (Nov 2024) added Llama-3.1 405B. Llama-2 70B LoRA was in v4.0 (June 2024). |

Overall: **#61-3 (Meta GPU count)** and **#61-5 (Llama-3 data mix)** are the material errors. **#61-2 (Stargate year)** is a date slip.

---

## Summary

7 chapters audited, ~35 substantial claims spot-checked. Findings:

**HIGH severity (fix promptly):**
- 56-4: Bibliography lists "Rauber, A., et al. (2024)" as NeMo Guardrails authors. Real authors are Rebedea et al. (2023). Hallucinated author attribution.
- 61-5: Llama-3 pretraining data mix percentages have code/math swapped (book says 25% code, 8% math; correct is 17% code, 25% math).

**MEDIUM severity (worth correcting):**
- 34-1: spaCy "10,000 documents per second" likely a unit confusion (words vs. docs).
- 36-3: BGE-M3 "194 languages" not supported by official sources, which say "100+ languages."
- 36-4: MS MARCO "1M passages, 500K queries" inverts/misstates the canonical figures (8.8M passages, ~1M training queries).
- 41-1: Character.AI "hundreds of millions of monthly messages" understates peak by 5-10× (was ~2B/month).
- 46-1: "GPT-4 rates own outputs best 67% of the time" lacks a citation and is higher than Zheng et al. 2023 reports.
- 59-3: 1F1B attribution "Narayanan, 2019" should probably be "Narayanan et al., 2021" (Megatron-LM paper) for the canonical reference.
- 61-2: Stargate announced January 2025, not 2024; total commitment $500B over 4 years, not just "$100B+".
- 61-3: Meta's 350K is just the H100 count, not total H100-equivalents (which was ~950K by end 2024).

**LOW / no findings**: most other sampled claims (~70%) verified against public sources.

The dominant failure mode is **outdated or rounded numeric claims being passed off as precise**, plus one fabricated co-author. Recommend running the **Fact Integrity Reviewer (Agent #11)** and **Content Update Scout (Agent #20)** specifically against Ch 36, 56, 59, 61 sections that cite specific numbers, papers, or company milestones, with a focus on:
- pretraining mix percentages
- vendor product launch dates (especially 2024-2025)
- model parameter / dimension / context-length specs
- bibliography author lists for any callout-cited paper

This audit is **non-exhaustive**; deeper sweep recommended before book ships.
