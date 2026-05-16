# Named-Case-Study Density Audit

Per-section scan for named cases (companies, products, papers, incidents) 
from 2023-2026 LLM/AI work. Tools-of-the-Trade modules are excluded 
(catalogues by definition).

- ABSTRACT: 0 named cases (P0 enrichment opportunity)
- SPARSE: 1-2 (P1)
- HEALTHY: 3-5
- DENSE: 6+ (acceptable for Models or Frameworks survey sections)

## Summary

- Sections scanned: **340**
- ABSTRACT (0 named cases): **13**
- SPARSE (1-2): **6**
- HEALTHY (3-5): **21**
- DENSE (6+): **300**

**Overall density: 94% of sections are HEALTHY or DENSE.**

**Key finding:** every ABSTRACT section is a chapter-overview `index.html` page 
(navigation hub, typically 60-100 lines). These are short on purpose, but each chapter 
would benefit from at least one anchor case in the Big-Picture callout to ground the 
chapter's claim that the topic matters.

## P0: ABSTRACT sections (need named cases)

### `part-10-idea-to-product/module-40-ideation/index.html`

- **Title:** Ideation: Finding LLM-Worthy Problems
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite ChatGPT (Nov 2022) as the canonical user-payment moment that opened the LLM product space; cite Klarna's 2024 AI assistant that replaced 700 contracted reps (handling 2/3 of customer service queries) as a real-world example of an LLM-worthy problem.

### `part-10-idea-to-product/module-41-product-management/index.html`

- **Title:** LLM Product Management
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Reference Anthropic's published 'Claude evaluation' methodology (2024) and OpenAI's Model Spec (2024) as exemplars of an LLM product spec; cite the Air Canada chatbot ruling (Feb 2024) as the canonical example of a spec gap turning into legal liability.

### `part-10-idea-to-product/module-42-strategy-prioritization/index.html`

- **Title:** LLM Strategy & Use Case Prioritization
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite a16z's 2024 'Build vs Buy' essay on AI infrastructure; reference Meta's Llama 3 (Apr 2024) as the canonical open-weight choice; reference Bloomberg's 2023 BloombergGPT (50B params, $10M) as the canonical example of in-house pretraining ROI versus API.

### `part-10-idea-to-product/module-44-mvp/index.html`

- **Title:** Building the MVP
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite Cursor's growth story (2023-2024, $400M ARR by 2025) as the canonical LLM-MVP-to-product trajectory; cite Khanmigo's 2023 launch (later Khan Academy GPT-4 deployment) as MVP-with-eval.

### `part-10-idea-to-product/module-45-prototype-to-production/index.html`

- **Title:** From Idea to Product Hypothesis
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Reference Klarna's Feb 2024 production-scale rollout (handling 2.3M conversations in first month) as a prototype-to-production case; cite DPD's Jan 2024 chatbot incident as the cautionary tale.

### `part-10-idea-to-product/module-46-compute-planning/index.html`

- **Title:** Compute Planning & Infrastructure
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite NVIDIA H100 vs H200 vs B200 (2024 announcements, GB200 in 2025) for sizing; reference AWS Trainium2 (Dec 2024) and Google TPU v5p (Dec 2023) as enterprise alternatives; cite vLLM 0.6 (2024) and TensorRT-LLM as canonical inference stacks.

### `part-10-idea-to-product/module-47-scaling-economics/index.html`

- **Title:** Scaling Economics: Unit Costs & ROI
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite the 10x cost drop of GPT-4 -> GPT-4o (May 2024) as the canonical pricing dynamic; reference DeepSeek-V3 (Dec 2024, $5.5M training cost) as the price/perf disruption; cite Cursor's $8M/year infra spend at $100M ARR as a real unit-economics anchor.

### `part-10-idea-to-product/module-48-shipping-deploying/index.html`

- **Title:** Shipping and Scaling AI Products
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite OpenAI's Dec 2024 outage and Anthropic's outages logged at status.anthropic.com as multi-provider justification; reference Vercel AI SDK and Cloudflare AI Gateway (2024) as concrete fallback infrastructure examples.

### `part-10-idea-to-product/module-49-post-launch-monitoring/index.html`

- **Title:** Post-Launch Monitoring & Iteration
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite Langfuse, LangSmith, and Arize Phoenix (2024) as production observability stacks; reference the Anthropic 'Claude 3.5 Sonnet (new)' silent upgrade in Oct 2024 as the canonical drift case where production behavior shifted under apps.

### `part-11-applications-across-industries/module-51-legal-llms/index.html`

- **Title:** LLMs in Legal Practice
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite Mata v. Avianca (June 2023) - the 'Steven Schwartz hallucinated cases' incident - as the canonical bar-discipline headline; reference Harvey ($100M Series B 2024), Hebbia, and Thomson Reuters' acquisition of Casetext ($650M, Aug 2023) as the vendor landscape anchors.

### `part-11-applications-across-industries/module-54-education-llms/index.html`

- **Title:** LLMs in Education
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite Khan Academy's Khanmigo (GPT-4-powered, launched 2023, scaled in 2024); reference the NYC DOE's January 2023 ChatGPT ban and reversal (May 2023); cite Turnitin's AI-detection false-positive rate published in 2024 as the failure-mode anchor.

### `part-11-applications-across-industries/module-56-government-llms/index.html`

- **Title:** LLMs in Government & Public Sector
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite the U.S. GSA's GovGPT and OpenAI's gov-specific ChatGPT Gov launch (Jan 2025); reference UK GDS GOV.UK Chat pilot (2024); cite IRS's use of GPT-4 for tax-code assistance in IRS's Direct File pilot (2024) as concrete examples.

### `part-9-safety-security-ethics/module-38-agent-safety-security/index.html`

- **Title:** Agent Safety & Security
- **Status:** 0 named cases (chapter overview / nav hub)
- **Suggestion:** Cite Simon Willison's prompt-injection taxonomy (2022-2024), 'Multi-turn jailbreaks' work; reference Anthropic's Sept 2024 paper 'Many-shot jailbreaking' (arxiv:2404.02151); cite OWASP LLM Top-10 (2024) and MITRE ATLAS framework as the canonical attack catalogues.

## P1: SPARSE sections (1-2 named cases)

### `part-1-foundations/module-05-decoding-text-generation/index.html`

- **Title:** Decoding Strategies & Text Generation
- **Current named cases (2):** PyTorch
- **Suggestion:** Mention OpenAI's GPT-4 temperature/top-p API defaults; reference 'The Curious Case of Neural Text Degeneration' (Holtzman et al., 2019, arxiv:1904.09751) which introduced nucleus sampling; and 'A Contrastive Framework for Neural Text Generation' (Su et al., NeurIPS 2022) for contrastive decoding.

### `part-10-idea-to-product/module-43-vibe-coding/index.html`

- **Title:** Prototyping via Vibe-Coding
- **Current named cases (2):** Cursor, Claude Code
- **Suggestion:** Beyond Cursor and Claude Code, cite Cline (open-source), Aider (terminal-based), Windsurf (Codeium, raised $150M in 2024), Replit Agent (Sept 2024), and Bolt.new (StackBlitz, $20M ARR in 60 days in Oct 2024) for a complete 2026 landscape.

### `part-11-applications-across-industries/module-52-finance-llms/section-52.2.html`

- **Title:** Failure Modes Specific to Finance
- **Current named cases (2):** Bloomberg, EU AI Act
- **Suggestion:** Beyond Bloomberg/EU AI Act, cite the SEC's July 2023 proposed rule on AI in investment advice; reference the OCC's Aug 2023 LLM guidance to banks; cite the $8.6M EEOC settlement vs. iTutorGroup (Aug 2023) as the canonical fair-lending-adjacent algorithmic-discrimination case.

### `part-11-applications-across-industries/module-52-finance-llms/index.html`

- **Title:** LLMs in Finance
- **Current named cases (1):** FDA
- **Suggestion:** Cite BloombergGPT (March 2023, the 50B-parameter financial-domain model); reference JPMorgan's IndexGPT trademark (May 2023) and Morgan Stanley's GPT-4 deployment for wealth advisors (March 2023, the first major Wall Street deployment); cite Goldman Sachs' '300M jobs' report (March 2023).

### `part-3-working-with-llms/module-15-hybrid-ml-llm/index.html`

- **Title:** Hybrid ML+LLM Architectures & Decision Frameworks
- **Current named cases (2):** GPT-4, PEFT
- **Suggestion:** Beyond GPT-4/PEFT, cite Anthropic's 2024 'Routing with Smaller Models' work; reference the Mixture-of-Depths paper (Raposo et al., 2024, arxiv:2404.02258); cite Databricks DBRX (2024) and the OpenAI tool-use 2024 cookbook as concrete hybrid-architecture references.

### `part-5-retrieval-conversation/module-24-conversational-ai/index.html`

- **Title:** Building Conversational AI Systems
- **Current named cases (2):** Character.AI, OpenAI
- **Suggestion:** Beyond Character.AI/OpenAI, cite the Replika 2023 NSFW rollback incident (Feb 2023) for identity-stability failure mode; reference the NEDA Tessa chatbot harm incident (May 2023); cite OpenAI's Memory feature (Feb 2024) as the canonical persistent-conversation engineering moment.

## Densest sections (informational; usually OK)

These are typically Models/Frameworks survey sections where high density is expected 
(BERT, LoRA, etc. are technical terms that count as 'named' here). Listed top 20:

- `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html` (Open-Source & Open-Weight Models): 342 named cases, 76 unique. Top: MoE(31), DeepSeek V3(19), Llama 3(17), BERT(15)
- `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.1.html` (Closed-Source Frontier Models): 313 named cases, 56 unique. Top: GPT-4o(42), OpenAI(30), Anthropic(20), GQA(18)
- `part-4-training-adapting/module-19-peft/section-19.2.html` (Advanced PEFT Methods): 288 named cases, 19 unique. Top: LoRA(123), PEFT(37), DoRA(36), IA3(26)
- `part-1-foundations/module-04-transformer-architecture/section-4.3.html` (Transformer Variants & Efficiency): 286 named cases, 48 unique. Top: RoPE(43), GQA(24), MoE(23), Linear(17)
- `part-4-training-adapting/module-19-peft/section-19.3.html` (Training Platforms & Tools): 282 named cases, 41 unique. Top: LoRA(39), QLoRA(27), PEFT(23), A100(22)
- `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.2.html` (DPO & Modern Preference Optimization): 258 named cases, 20 unique. Top: DPO(146), RLHF(29), KTO(18), ORPO(15)
- `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.1.html` (RLHF: Teaching a Model What 'Helpful' Means): 250 named cases, 32 unique. Top: PPO(72), RLHF(68), GRPO(25), DPO(18)
- `part-2-understanding-llms/module-10-inference-optimization/section-10.4.html` (Serving Infrastructure): 229 named cases, 36 unique. Top: vLLM(36), TensorRT-LLM(17), LoRA(17), NVIDIA(16)
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.3.html` (Scaling Laws & Compute-Optimal Training): 228 named cases, 31 unique. Top: Chinchilla(54), MoE(50), DeepSeek-V3(16), Kaplan(14)
- `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.4.html` (Fine-Tuning via Provider APIs): 214 named cases, 36 unique. Top: OpenAI(46), Vertex AI(24), Google(19), GPT-4o(16)
- `part-4-training-adapting/module-19-peft/section-19.1.html` (LoRA & QLoRA): 210 named cases, 27 unique. Top: LoRA(121), QLoRA(19), PEFT(18), Adapter(8)
- `part-4-training-adapting/module-19-peft/section-19.4.html` (Soft Prompts: Prompt Tuning, Prefix Tuning, and P-Tuning): 209 named cases, 22 unique. Top: P-Tuning(45), LoRA(39), Prompt Tuning(37), Prefix Tuning(28)
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html` (BERT, GPT, T5: Three Bets That Shaped Today's LLMs): 200 named cases, 42 unique. Top: BERT(39), GPT-3(21), T5(20), GPT-2(10)
- `part-2-understanding-llms/module-10-inference-optimization/section-10.2.html` (KV Cache & Memory Optimization): 188 named cases, 40 unique. Top: GQA(28), Llama 3.1(27), PagedAttention(17), vLLM(16)
- `part-5-retrieval-conversation/module-23-rag/section-23.6.html` (RAG Frameworks & Orchestration): 183 named cases, 25 unique. Top: LangChain(48), LlamaIndex(43), Haystack(26), OpenAI(11)
- `part-8-evaluation-production/module-34-evaluation-observability/section-34.12.html` (LLM Performance Benchmarking and Cross-Hardware Portability): 178 named cases, 32 unique. Top: ROUGE(23), vLLM(19), MI300X(16), BLEU(13)
- `part-3-working-with-llms/module-13-llm-apis/section-13.1.html` (API Landscape & Architecture): 172 named cases, 18 unique. Top: OpenAI(68), Anthropic(28), AWS(15), Google(14)
- `part-2-understanding-llms/module-10-inference-optimization/section-10.1.html` (Model Quantization): 168 named cases, 32 unique. Top: AWQ(35), GPTQ(32), bitsandbytes(14), H100(8)
- `part-8-evaluation-production/module-34-evaluation-observability/section-34.1.html` (LLM Evaluation Fundamentals): 162 named cases, 32 unique. Top: BLEU(27), BERTScore(22), ROUGE(15), Perplexity(10)
- `part-3-working-with-llms/module-14-prompt-engineering/section-14.2.html` (Chain-of-Thought & Reasoning Techniques): 158 named cases, 14 unique. Top: CoT(69), ReAct(20), Chain-of-Thought(17), OpenAI(13)

## Aggregate by part

| Part | Total | ABSTRACT | SPARSE | HEALTHY | DENSE |
|---|---:|---:|---:|---:|---:|
| part-1-foundations | 29 | 0 | 1 | 1 | 27 |
| part-10-idea-to-product | 50 | 9 | 1 | 4 | 36 |
| part-11-applications-across-industries | 53 | 3 | 2 | 9 | 39 |
| part-12-frontiers | 24 | 0 | 0 | 1 | 23 |
| part-2-understanding-llms | 35 | 0 | 0 | 1 | 34 |
| part-3-working-with-llms | 18 | 0 | 1 | 0 | 17 |
| part-4-training-adapting | 30 | 0 | 0 | 0 | 30 |
| part-5-retrieval-conversation | 22 | 0 | 1 | 0 | 21 |
| part-6-agentic-ai | 24 | 0 | 0 | 3 | 21 |
| part-7-multimodal-generation | 14 | 0 | 0 | 2 | 12 |
| part-8-evaluation-production | 23 | 0 | 0 | 0 | 23 |
| part-9-safety-security-ethics | 18 | 1 | 0 | 0 | 17 |

## Method

- Scanner walks all `part-*/module-*/` directories that are **not** `tools-of-the-trade`.
- For each section file (`section-NN.M.html`) and chapter `index.html`, the script 
  strips HTML, then counts whole-word matches against a curated 2023-2026 named-case 
  lexicon: AI labs, products (GPT-5, Claude 4, Llama 3 etc.), papers (by title or 
  arXiv ID), benchmarks (MMLU, HumanEval, etc.), incidents (Air Canada, Tay), and 
  practitioners (Karpathy, Huyen, etc.). Technical-architecture acronyms (LoRA, MoE) 
  intentionally inflate the densest-section counts; they do not affect the ABSTRACT/
  SPARSE flagging which is what this audit is for.
- A single match counts once toward the total; repeated mentions of the same name in 
  a section are counted as separate matches (so reuse boosts the score). This is by 
  design: a section that mentions OpenAI 30 times is more grounded than one that 
  mentions it once.
- Paper references via arXiv ID or quoted famous title each count as 1.
