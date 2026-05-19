# Bibliography R2 - Parts 13-16 Chapter Index Pages

Round 2 of the bibliography backfill. Scope: chapter `index.html` files in Parts 13-16 (modules 62-83). The R1 attempt covered Parts 11-12 (modules 52-62) and committed module-62 in this part as a transition. This round completes the chapter-index bibliographies through the end of the book.

## Method

For each chapter index page missing a `<details class="bibliography-collapsible">` section between `<div class="whats-next">` and `<nav class="chapter-nav">`, insert 4 canonical entries (two per sub-heading) chosen for topical fit, recency where appropriate, and verifiability against the corresponding arXiv / Nature / NEJM / Science / ACM DL URL. Every entry follows the `bib-entry-card` markup pattern set by module-62 in R1.

## Chapters touched (22 files, all in Parts 13-16)

### Part XIII: LLMOps Lifecycle
- `part-13-llmops-lifecycle/module-63-ai-gateways-routing/index.html` - RouteLLM, FrugalGPT, GPTCache, RouterBench
- `part-13-llmops-lifecycle/module-64-workflow-orchestration/index.html` - Durable Functions, Workflow taxonomy, DSPy, AutoGen
- `part-13-llmops-lifecycle/module-65-containers-kubernetes/index.html` - Borg/Omega/K8s, Llumnix, InferLine, NVIDIA NIM
- `part-13-llmops-lifecycle/module-66-reliability-slos-registry/index.html` - SRE Workbook, OpenLambda, ML metadata, Model Cards

### Part XIV: Designing LLM/Agent Products
- `part-14-designing-llm-agent-products/module-67-ideation/index.html` - Yang et al. HCI, SE4ML, AI Chains, Why Johnny Can't Prompt
- `part-14-designing-llm-agent-products/module-68-vibe-coding/index.html` - Copilot RCT, Expectation vs. Experience, SWE-bench, SWE-agent
- `part-14-designing-llm-agent-products/module-69-llm-economics/index.html` - FrugalGPT, Pope et al. inference scaling, NBER GenAI@Work, HBS Jagged Frontier
- `part-14-designing-llm-agent-products/module-70-shipping-products/index.html` - Hidden Technical Debt, Kohavi A/B Testing, Buschek suggestions, GPT-4 System Card
- `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/index.html` - DSPy, AutoGen, HELM, MCP

### Part XIV: Applications of LLMs Across Industries
- `part-14-applications-of-llms-across-industries/module-67-legal-llms/index.html` - Dahl et al. Legal Fictions, Magesh et al. Hallucination-Free?, LegalBench, FairLex
- `part-14-applications-of-llms-across-industries/module-68-finance-llms/index.html` - BloombergGPT, PIXIU, FinQA, Lopez-Lira & Tang
- `part-14-applications-of-llms-across-industries/module-69-healthcare-llms/index.html` - Med-PaLM (Nature), Med-PaLM 2, NEJM Catalyst ambient AI, MedHALT
- `part-14-applications-of-llms-across-industries/module-70-education-llms/index.html` - Kasneci et al. ChatGPT for Good, MathDial, GenAI Can Harm Learning, UNESCO IESALC
- `part-14-applications-of-llms-across-industries/module-71-cybersecurity-llms/index.html` - Greshake indirect injection, Zou GCG, Pearce zero-shot repair, OWASP Top 10 for LLMs
- `part-14-applications-of-llms-across-industries/module-72-government-llms/index.html` - NIST AI 600-1, EU AI Act, Eubanks Automating Inequality, Henman public-sector AI
- `part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/index.html` - Colabianchi chatbot for operators, Stogiannos industrial LLMs survey, Zhai chat-vs-search, Epstein et al. Science creative AI
- `part-14-applications-of-llms-across-industries/module-74-tools-of-the-trade/index.html` - Foundation Models, GPTs Are GPTs labor impact, HELM, Augmented LMs

### Part XV: LLM & Agentic AI Research Frontiers
- `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/index.html` - Mamba, Mamba-2 / SSM-attention duality, ESM-2, RT-2
- `part-15-llm-agentic-ai-research-frontiers/module-76-frontier-theory/index.html` - Toy Models of Superposition, Scaling Monosemanticity, Chinchilla, Emergence Mirage
- `part-15-llm-agentic-ai-research-frontiers/module-77-agi-trajectories/index.html` - DeepMind Levels of AGI, ARC Prize 2024, METR autonomy, Catastrophic AI Risks
- `part-15-llm-agentic-ai-research-frontiers/module-78-tools-of-the-trade/index.html` - HuggingFace transformers, DeepSpeed, BIG-bench, Chatbot Arena

## Conventions

- Two H3 sub-sections per chapter, ~2 entries each (4 total).
- Each `bib-note` explains why the reference is canonical for the chapter's topic.
- Mix of arXiv preprints, journal papers (Nature, Science, NEJM Catalyst, Communications of the ACM), conference papers, and reputable institutional reports (OpenAI System Card, NIST AI 600-1, EU AI Act, OWASP, UNESCO, NVIDIA, Anthropic Transformer Circuits).
- Links chosen to be stable: arXiv canonical IDs, DOI URLs, USENIX / NeurIPS / ACM DL when arXiv is not the primary venue.
- No em dashes used (style requirement); inline notes are short, semicolon-separated where needed.

## R2 result

After R2: 22 of 22 chapter index pages in Parts 13-16 carry a bibliography section (module-62 was completed in R1 and was left intact; modules 63-83 received their new bibliographies in R2). Combined with R1 (Parts 11-12, modules 52-62) and the prior R0 backfill in earlier parts, the book's chapter-index bibliographies are now uniform from at least Part XI onward.
