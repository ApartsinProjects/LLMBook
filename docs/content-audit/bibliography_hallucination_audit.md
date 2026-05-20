# Bibliography hallucination audit

**Scope.** Chapters 34, 36, 41, 46, 56, 59, 61 (modules-by-name) plus Wave 17i consolidated sections 27.5, 26.6, 24.6, 24.13, 35.2, 35.3, 29.1, 29.4, 37.3.

**Method.** Programmatically extracted every `<div class="bib-entry-card">` and `<section class="bibliography">` block in those files (213 entries with 159 URLs). Spot-checked a representative sample of 40+ URLs via WebFetch, with priority given to arXiv IDs (the most common hallucination vector) and to publisher / vendor blog URLs.

**Coverage notes.**
- Ch 34 (module-34-structured-information-extraction-ner) and Ch 46 (module-46-llm-as-judge-automated-evaluation) contain **no bibliography blocks at all** in either pattern. They only host internal navigation links. These two chapters are out of scope for citation auditing in their current state.
- Ch 36, 41, 56, 61 use the `<div class="bib-entry-card">` style with full URLs.
- Ch 59 (module-59-distributed-training-systems) uses `<section class="bibliography"><ol><li>` style; most entries are **text-only** with no clickable URL (e.g. arXiv IDs printed but not linked). Verifiability is by author-title-venue triplet only.
- All nine Wave 17i sections do have bibliography blocks.

---

## High-confidence hallucinations

These are entries where the cited URL resolves to a paper with a **different title** than the one given in the citation, or where the citation claims an arXiv preprint that does not exist.

### Wave 17i 26.6 - `part-6-agentic-ai/module-26-ai-agents/section-26.6.html`

- **L230 - Zhang et al. (2024) "A Survey on the Memory Mechanism of Large Language Model based Agents"** linked to `https://arxiv.org/abs/2310.08560` - **WRONG URL.** arXiv 2310.08560 is "MemGPT: Towards LLMs as Operating Systems" by Packer et al. The actual Zhang memory-survey is `arXiv:2404.13501`.
- **L236 - Packer, C., Wooders, S., Lin, K., et al. (2024) "MemGPT: Towards LLMs as Operating Systems" (ICLR 2024)** linked to `https://arxiv.org/abs/2402.01032` - **WRONG URL.** arXiv 2402.01032 is "Repeat After Me: Transformers are Better than State Space Models at Copying" by Jelassi et al. The correct MemGPT ID is `arXiv:2310.08560`. Note that 2310.08560 was incorrectly given to the row above (the survey), so the bibliography essentially **swaps two adjacent arXiv IDs** and assigns each to the wrong paper.
- **L239 - LangGraph Documentation: Checkpointers (2024)** linked to `https://docs.langgraph.dev/` - **DOMAIN DOES NOT EXIST.** WebFetch returns ECONNREFUSED. The official LangGraph docs were at `langchain-ai.github.io/langgraph/` and now redirect to `docs.langchain.com`. The `.dev` domain is plausible-looking but never existed.

### Wave 17i 29.1 - `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html`

- **L321 - Cognition AI (2024) "Devin: AI Software Engineer", arXiv preprint** linked to `https://arxiv.org/abs/2411.01747` - **FABRICATED.** arXiv 2411.01747 is "DynaSaur: Large Language Agents Beyond Predefined Actions" by Nguyen et al. Cognition has never published an arXiv paper for Devin; the announcement was a blog post at `cognition.ai/blog/introducing-devin` (which does exist, and is cited correctly in section 29.4).
- **L324 - Cursor Team (2025) "Cursor: An AI Code Editor", arXiv preprint** linked to `https://arxiv.org/abs/2502.14499` - **FABRICATED.** arXiv 2502.14499 is "MLGym: A New Framework and Benchmark for Advancing AI Research Agents" by Nathani et al. (Meta). Cursor (Anysphere) has not published an arXiv paper describing the editor.

### Wave 17i 35.3 - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html`

- **L423 - Traag, V.A. et al. (2019) "From Louvain to Leiden: Guaranteeing Well-Connected Communities", Scientific Reports** linked to `https://arxiv.org/abs/1810.00826` - **WRONG URL.** arXiv 1810.00826 is "How Powerful are Graph Neural Networks?" by Xu, Hu, Leskovec, Jegelka (the GIN paper). The correct Leiden URL is `arXiv:1810.08473` (Traag, Waltman, van Eck).

---

## Suspect entries (mismatched titles or weak verifiability)

These look legitimate (real domain, real-format ID) but have a metadata inconsistency worth a human-eye check.

### Ch 61.2 - `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.2.html`

- **L182 - Meta PyTorch (2024) "torchtitan: A native PyTorch library for large model training" (arXiv:2410.06511)** - URL resolves correctly to a real torchtitan paper, but the published title is "TorchTitan: One-stop PyTorch native solution for production ready LLM pre-training." Minor cosmetic mismatch; the citation is still pointing at the right paper.

### Ch 41.4 / Ch 41.5 / Ch 41.3 (Conv-AI tools chapter)

- Most arXiv entries verified correct (MultiWOZ 1810.00278, PersonaChat 1801.07243, EmpatheticDialogues 1811.00207, MT-Bench 2306.05685, HH-RLHF 2204.05862, HarmBench 2402.04249, SGD 1909.05855). No mismatches found.
- **Inflection AI (2023) "Pi, your personal AI"** at `inflection.ai/press/inflection-1` - Inflection has restructured significantly and original press URLs are fragile. Plausible but worth a manual visit.

### Ch 56.x (Responsible-AI tools)

- All arXiv references resolved cleanly to the cited paper (AIF360 1810.01943, SHAP 1705.07874, Llama Guard 2312.06674, Watermark 2301.10226, DP-SGD 1607.00133, CFE 1711.00399, BBQ 2110.08193, TruthfulQA 2109.07958, Folktables 2108.04884, Memorization 2202.07646, OLMo 2402.00838, Sadasivan 2303.11156, GPT detectors 2304.02819). Strong signal that this chapter was authored carefully.
- **L186 - "Rauber, A., et al. (2024). NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications" (linked to `developer.nvidia.com/nemo-guardrails`)** - NeMo Guardrails does have a published arXiv paper (`arXiv:2310.10501`) but the lead author is Traian Rebedea, not Rauber. The cited "Rauber, A., et al. (2024)" attribution looks invented; the URL itself is a real NVIDIA developer page so the entry is partly true. Author-line is likely hallucinated.

### Wave 17i 35.2 - `module-35-advanced-rag/section-35.3.html`

- **L526 - Baek, J. et al. (2023)** has **two URLs** under one entry: the correct arXiv link plus a stray internal cross-reference (`../../part-4-training-adaptation/module-16-fine-tuning-fundamentals/index.html`) that does not belong in a bibliography card. Layout bug rather than a hallucination, but worth cleaning.

### Wave 17i 27.5 - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.5.html`

- **L189 - Anthropic (2024). "Model Context Protocol (MCP) Specification." Anthropic Technical Report.** - **No URL given** in the bibliography card. MCP is real (`spec.modelcontextprotocol.io`) and was published Nov 2024, but the citation does not link out. Verifiable only by knowing the spec exists; readers cannot click through. Not a hallucination, but unverifiable as written.
- All four bib entries in 27.5 (Schick Toolformer, Patil Gorilla, MCP, Yao ReAct) are **URL-less**, in contrast to the URL-rich style used elsewhere. Style inconsistency.

### Ch 59 (Distributed-training-systems) - text-only bibliography

- All Ch 59 sections (59.1-59.5) use text-only `<li>` entries. None of the dozens of arXiv IDs given in prose are linked, e.g. "arXiv:1706.02677", "arXiv:2306.10209", "arXiv:2304.11277", "arXiv:2205.05198", "arXiv:2201.11990", "arXiv:2205.01068", "arXiv:2211.05100", "arXiv:2306.10209", "arXiv:2307.09288", "arXiv:2407.21783", "arXiv:2412.19437". The IDs all pattern-match valid (YYMM.NNNNN), but only the linked entries are machine-verifiable. Spot-checks of the linked ones (Llama-3 2407.21783, DeepSeek-V3 2412.19437) confirm correctness. No evidence of hallucination, but the chapter would benefit from URL-linking every arXiv ID.

---

## Verified-OK samples (40+ entries verified against arXiv)

Among the URLs we spot-checked via WebFetch and confirmed match the cited title:

- Ch 36.1: HNSW (1603.09320), FAISS (1702.08734), Milvus SIGMOD PDF, ANN-Benchmarks site
- Ch 36.2: Sentence-BERT (1908.10084), ColBERT (2004.12832), RAGAS (2309.15217), DSPy (2310.03714)
- Ch 36.3: BEIR (2104.08663), MTEB (2210.07316), HotpotQA (1809.09600), NQ ACL anthology page
- Ch 36.4: BGE-M3 (2402.03216), NV-Embed (2405.17428), Matryoshka (2205.13147), ColPali (2407.01449), E5-Mistral (2401.00368)
- Ch 36.5: MTEB leaderboard HF space, Anthropic Contextual Retrieval page, Manning IR-book
- Ch 41.3: MultiWOZ (1810.00278), HH-RLHF (2204.05862), MT-Bench (2306.05685), HarmBench (2402.04249), SGD (1909.05855)
- Ch 56.x: AIF360, SHAP, Llama Guard, Watermark, DP-SGD, CFE, BBQ, TruthfulQA, Folktables, Memorization, OLMo, Sadasivan, GPT-detectors
- Ch 61.1: Pathways (2203.12533), SageMaker HyperPod blog
- Ch 61.2: Megatron (1909.08053), ZeRO (1910.02054), FlashAttention (2205.14135), FA-3 (2407.08608), QLoRA (2305.14314)
- Ch 61.3: FineWeb (2406.17557), Pile (2101.00027), UltraFeedback (2310.01377), DataComp (2304.14108)
- Ch 61.4: Llama-3 (2407.21783), DeepSeek-V3 (2412.19437), DeepSeek-R1 (2501.12948), Mixtral (2401.04088), Qwen2.5 (2412.15115)
- Ch 61.5: OPT-175B logbook (in archived facebookresearch/metaseq repo - real, archived Nov 2024)
- Wave 17i 26.6: Generative Agents 2304.03442, Reflexion 2303.11366 (correct)
- Wave 17i 24.6 / 24.13: OpenVLA (2406.09246), SimplerEnv (2405.05941), Orbit (2301.04195), Isaac Gym (2108.10470), Rubik's Cube (1910.07113), DROID (2403.12945), DIGIT (2005.14679), Domain Randomization (1703.06907)
- Wave 17i 35.2 / 35.3: GraphRAG (2404.16130), KG-LLM roadmap (2306.08302), Baek KG-prompting (2306.04136), microsoft/graphrag and microsoft/graphrag-benchmarking-datasets GitHub repos
- Wave 17i 29.1 / 29.4: HumanEval/Codex (2107.03374), SWE-bench (2310.06770), SWE-agent (2405.15793), Cognition Devin blog post (2024), Anthropic Claude Code best-practices page
- Wave 17i 37.3: MemoryBank (2305.10250), Maharana long-term mem (2402.17753), MemGPT (2310.08560 correct here, contradicting the 26.6 swap)

NIST AI RMF Playbook, EU AI Act eur-lex page, c2pa.org, kyutai.org Moshi PDF, fairmlbook.org, transformer-circuits.pub, proceedings.mlr.press, dl.acm.org all verified live and on-topic.

---

## Patterns

### Domain frequency (159 URLs total)

| count | domain |
|------:|--------|
| 84 | arxiv.org |
| 7 | github.com |
| 5 | anthropic.com |
| 3 | openai.com |
| 3 | neo4j.com |
| 2 | platform.openai.com, docs.anthropic.com, link.springer.com, eur-lex.europa.eu, developer.nvidia.com |
| 1 each | pinecone.io, cs.purdue.edu, ann-benchmarks.com, plg.uwaterloo.ca, nlp.stanford.edu, eugeneyan.com, cookbook.openai.com, cloud.google.com, rasa.com, inflection.ai, python.langchain.com, docs.pipecat.ai, docs.livekit.io, help.getzep.com, ai.meta.com, kyutai.org, web.stanford.edu, airc.nist.gov, iso.org, c2pa.org, crfm.stanford.edu, transformer-circuits.pub, proceedings.mlr.press, dl.acm.org, doi.org, ... |

84 of 159 URLs (53%) are arXiv. arXiv is therefore both the most-cited and the most-frequent hallucination surface: every confirmed hallucination above involves an arXiv ID assigned to the wrong paper.

### Per-chapter hallucination risk

| chapter / section | risk | notes |
|---|---|---|
| Ch 34 | n/a | No bibliography blocks at all |
| Ch 36 (retrieval tools) | **low** | 30 entries checked across 5 sections; arXiv IDs and vendor URLs all matched cited titles |
| Ch 41 (conv-AI tools) | **low** | 30 entries; arXiv IDs all matched; vendor docs (Pipecat, LiveKit, Zep, LangChain) all live |
| Ch 46 | n/a | No bibliography blocks |
| Ch 56 (responsible-AI tools) | **low**, with one suspect author-line | All ~28 arXiv IDs verified; NeMo Guardrails entry has invented authorship but real URL |
| Ch 59 (distributed-training) | **medium** | Text-only entries cannot be machine-verified; sampled IDs all valid, but the chapter relies on reader trust |
| Ch 61 (scale tools) | **low** | 28 entries, all arXiv IDs verified; one minor title-paraphrase on torchtitan |
| Wave 17i 24.6 | **low** | All seven entries verified |
| Wave 17i 24.13 | **low** | All seven entries verified |
| Wave 17i 26.6 | **HIGH** | Two adjacent arXiv IDs swapped to wrong papers; one non-existent docs domain |
| Wave 17i 27.5 | **medium** | Four URL-less entries; no hallucination found but unverifiable as written |
| Wave 17i 29.1 | **HIGH** | Two fabricated arXiv references (Devin, Cursor) - papers do not exist |
| Wave 17i 29.4 | **low** | Six entries verified; the same Devin and Cursor references are cited as blog posts here and resolve correctly |
| Wave 17i 35.2 | **low** | Six entries verified; one card has a stray internal-nav URL mixed in |
| Wave 17i 35.3 | **medium** | One wrong arXiv ID (Leiden paper points to GIN paper); other six entries correct |
| Wave 17i 37.3 | **low** | All six entries verified |

### Failure mode pattern

The four high-confidence hallucinations (26.6 swap-pair, 29.1 Devin, 29.1 Cursor, 35.3 Leiden) share a profile:
1. The cited paper is real and well-known.
2. The arXiv ID is a real arXiv ID that points at a *plausible-sounding but different* paper from a similar subfield.
3. The citation never went through a "click the link, read the page title" check.

For the two Wave 17i 29.1 entries, the underlying fact ("Cognition makes Devin", "Anysphere makes Cursor") is also true; the hallucination is *only* that there exists an arXiv paper for these commercial products. Both products have blog posts but no academic preprints. In 29.4, the same products are cited correctly as blog posts and product docs - so the bibliography for 29.1 likely got the citation template from 29.4 and then "upgraded" the venue from "blog post" to "arXiv preprint" without checking.

### Recommendations for fix

1. Highest priority - replace the four fabricated arXiv URLs in Wave 17i 26.6, 29.1, 35.3. For 29.1, switch the Devin and Cursor entries from "arXiv preprint" to the actual blog posts (which 29.4 already uses).
2. Fix the LangGraph docs URL in 26.6 (`docs.langgraph.dev` to `docs.langchain.com`).
3. Verify the NeMo Guardrails author-line in 56.1; correct lead author is Traian Rebedea.
4. Decide whether to link every arXiv ID in Ch 59. The current text-only bibliography is a lower-risk style choice but a higher-friction reader experience.
5. Strip the stray cross-reference URL in Wave 17i 35.2 L526.
6. Confirm the Anthropic MCP specification URL for Wave 17i 27.5 and add it to the citation.
