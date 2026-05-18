# Repeated-Content Audit

Cross-section duplication triage for the LLM textbook.

READ-ONLY scan. No HTML files have been modified. This report proposes 
canonical homes and lists duplicates for the editor to reconcile manually.


## Methodology

- Scanned **386** main-track section HTML files under `part-*/module-*/section-*.html`.
- Excluded: `tools-of-the-trade` modules, `appendices/`, `front-matter/`, `capstone/`, `KDP/`, vendor dirs.
- For each section extracted:
  - **4,246** non-boilerplate callouts (skipped Prerequisites, Key Takeaways, Exercises, etc.)
  - **1,287** code-fragment captions
  - **4,808** prose paragraphs (>= 200 chars, outside callouts/blockquotes/bibliography)
- Detection signals:
  1. Same callout title across 2+ sections (e.g., two 'Attention Is Just Weighted Lookup' callouts)
  2. Callout body whose first-150-char lowercase fingerprint matches across 2+ sections
  3. Code-fragment captions sharing >=4 content tokens (fuzzy match on noun phrases)
  4. Prose paragraphs whose first-100-char lowercase fingerprint matches across 2+ sections
- Canonical home assignment combines topic heuristics (LangChain -> Part III, RAG -> Part VII, etc.) 
  with a fallback to the lowest-numbered part containing the duplicated content.

## Headline Numbers

- **30** clusters of duplicated callout titles (same title in 2+ sections).
- **3** clusters where the first 150 chars of a callout body match.
- **7** clusters where a code-caption fingerprint matches exactly across sections.
- **163** fuzzy code-caption clusters (>=4 shared content tokens).
- **4** clusters where a prose-paragraph first-100-char fingerprint matches.

**Estimated reduction if all duplicates reconcile to cross-refs:**
- Excess callout occurrences (across all clusters): ~**551**, roughly **44,080 words**.
- Excess code-fragment duplicates (exact + fuzzy): **306**.
- Excess prose duplicates: **4**, roughly **600 words**.
- **Grand total estimated savings: ~44,680 words / ~555 duplicate blocks.**


## Top Duplication Clusters

Each cluster lists: type, canonical home (proposed), and duplicate locations.
Suggested actions: **DELETE** = remove duplicate, replace with See Also cross-ref; 
**RESTRUCTURE** = redundant content overlaps with canonical but is not identical; 
**KEEP** = brief restatement is intentional for self-containment.


### 1. CALLOUT TITLE (same title)  |  155 sections
- **Key/signature**: `fun fact`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html:241`
    > Every ML practitioner has experienced the five stages of overfitting grief: denial ("my 99% accuracy is real"), anger ("why does test accura
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.2.html:151`
    > Backpropagation was independently discovered at least four times before it became famous in 1986. The algorithm spent nearly two decades in 
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html:234`
    > Every ML engineer has at least one 3 AM debugging story where the bug was a missing .cuda() call. The "Expected all tensors to be on the sam
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html:154`
    > Reinforcement learning famously taught a computer to play Atari games in 2013, but researchers often omit that the agent also discovered biz
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.1.html:261`
    > The sentence "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo" is grammatically correct English. If NLP seems hard, remember
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html:230`
    > Bag-of-Words treats language the way a toddler treats a jigsaw puzzle: dump all the pieces out, count the colors, and ignore that they were 
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html:354`
    > The "king minus man plus woman equals queen" analogy became so iconic that it practically served as the pickup line of the NLP community for
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.5.html:102`
    > LLMs are notoriously bad at counting letters in words, and tokenization is the culprit. Ask a model how many "r"s are in "strawberry" and it
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:319`
    > A sentence in English might take 10 tokens, but the same sentence in Burmese or Tamil could take 40 or more. This means speakers of underrep
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html:195`
    > The vanishing gradient problem was identified in 1991 by Sepp Hochreiter, but the broader community did not fully appreciate it for years. H
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.2.html:224`
    > The number of papers with "attention" in the title published since 2017 is itself worthy of some attention filtering. The original Bahdanau 
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html:479`
    > The quadratic cost of self-attention is why your favorite chatbot has a context window limit. Doubling the sequence length quadruples the me
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html:99`
    > "Attention Is All You Need" was almost titled "Transformers: Attention Networks." The name "Transformer" was suggested late in the writing p
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html:804`
    > The most common Transformer implementation bug is getting the attention mask wrong. It is also the hardest to notice, because a model with a
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html:195`
    > FlashAttention computes the exact same result as naive attention but 2 to 4 times faster, simply by being smarter about memory access patter
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html:216`
    > Asking a Transformer to "think step by step" literally gives it more computation, because each generated token is another forward pass throu
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.6.html:79`
    > State Space Models borrow their mathematical framework from control theory, a field originally developed to stabilize rockets and autopilots
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html:166`
    > Beam search was the decoding method of choice for machine translation for decades. Despite being a controlled, deterministic search algorith
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html:97`
    > The term "temperature" comes from statistical mechanics, where it controls the randomness of particle states in a physical system. Setting t
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html:164`
    > Speculative decoding is essentially the "write a rough draft and have your boss approve it" strategy. A small, fast model guesses several to
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:141`
    > Diffusion models for text generation borrow their core idea from image generation, where you start with pure noise and gradually refine it i
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html:159`
    > The EU AI Act, which came into force in 2024, classifies AI systems by risk level and imposes requirements proportional to that risk. High-r
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.2.html:73`
    > During a 2023 red teaming exercise, a researcher bypassed a chatbot's safety filters by asking the model to roleplay as "DAN" (Do Anything N
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.5.html:84`
    > In 2023, a lawyer submitted a legal brief containing six case citations fabricated by ChatGPT, complete with plausible docket numbers. The j
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.5.html:84`
    > A 2024 study asked GPT-4 to provide legal citations and found that roughly 30% of the cited cases did not exist. The model had "hallucinated
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html:74`
    > In the landmark Carlini et al. extraction study, the researchers recovered a person's full name, email address, phone number, and physical a
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.2.html:120`
    > The field of AI safety has grown from a handful of researchers in 2015 to thousands of full-time practitioners in 2025. Anthropic, OpenAI, G
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.3.html:80`
    > Google's Gboard keyboard uses federated learning to improve next-word prediction across billions of Android devices. Every time you type a m
  - `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html:98`
    > The concept of "model cards," standardized documentation for ML models, was proposed by Margaret Mitchell and colleagues at Google in 2019. 
  - `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.3.html:58`
    > When researchers asked GPT-4 "Is it acceptable to eat with your hands?" the model defaulted to Western dining etiquette and gently discourag
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.1.html:65`
    > The EU AI Act's final text runs to over 400 pages. In a fitting twist, several law firms used LLMs to summarize it, only to discover the sum
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.1.html:65`
    > The EU AI Act's risk classification system was partly inspired by pharmaceutical regulation, where drugs are classified into schedules based
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.2.html:74`
    > The EU AI Act's risk classification means that the exact same GPT-4 model powering a creative writing chatbot (minimal risk, no obligations)
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.3.html:111`
    > Content provenance standards like C2PA (Coalition for Content Provenance and Authenticity) embed cryptographic signatures into AI-generated 
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.4.html:72`
    > Meta's Llama license allows commercial use only if you have fewer than 700 million monthly active users. This threshold conveniently exclude
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.4.html:72`
    > In 2023, Samsung engineers accidentally leaked proprietary source code by pasting it into ChatGPT for debugging help. The incident led Samsu
  - `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html:82`
    > Training GPT-4 consumed an estimated 50 GWh of electricity, enough to power roughly 4,600 U.S. households for an entire year. Yet the infere
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html:283`
    > The cross-hardware portability landscape changes remarkably fast. In 2023, running vLLM on AMD GPUs required significant manual patching. By
  - `part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.1.html:79`
    > Apple's on-device language model for iOS 18 runs a 3B-parameter model that fits in 1.5 GB of memory after quantization. It handles autocompl
  - `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.1.html:167`
    > Prompt injection attacks, where users trick an LLM into ignoring its system prompt , were discovered almost immediately after ChatGPT launch
  - `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.2.html:79`
    > The unofficial motto of LLMOps is "git for prompts, but also for the model, the data, the config, and your sanity." Most teams discover they
  - `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.2.html:79`
    > Netflix once ran an A/B test on thumbnail images and discovered that showing a villain's face increased click-through rates more than showin
  - `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.1.html:99`
    > One fintech startup discovered that 30% of their LLM API spend went to a single user who had figured out how to use the internal chatbot as 
  - `part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html:83`
    > An early LangGraph user reported that their 45-step research agent crashed at step 42 due to an OpenAI rate limit, then resumed seamlessly f
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html:551`
    > Google's internal LLM serving infrastructure reportedly keeps "standby" TPU pods with models pre-loaded in memory, consuming significant res
  - `part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html:72`
    > During a major cloud provider outage in 2024, a well-designed LLM application with a proper fallback chain seamlessly routed 100% of traffic
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.10.html:151`
    > GitHub Copilot, one of the most commercially successful AI products, has a suggestion acceptance rate of roughly 30%. That means the model i
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.11.html:65`
    > In traditional software, "Can we build it?" is almost always yes. In AI products, "Can we build it well enough?" is the question that kills 
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.12.html:198`
    > The term "data gravity" was coined by Dave McCrory in 2010 to describe how data attracts applications, services, and more data to its locati
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.13.html:136`
    > A 2024 GitClear analysis of code churn rates found that projects using AI coding assistants had a 39% higher rate of code that was reverted 
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.13.html:136`
    > The term "vertical slice" originated in game development during the 1990s, where studios would build one complete level of a game before rou
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.14.html:203`
    > The idea of "executable documentation" predates AI coding assistants by decades. Literate programming, invented by Donald Knuth in 1984, int
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.15.html:376`
    > Research on recommendation systems at Netflix and Spotify consistently shows that the first 1,000 pieces of explicit user feedback improve m
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.5.html:66`
    > In post-mortems of failed LLM product launches, the most common root cause is not a technical failure. It is a requirements misunderstanding
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.7.html:213`
    > McKinsey estimated that generative AI could add $2.6 to $4.4 trillion annually to the global economy. But here is the catch: most of that va
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.8.html:66`
    > A common vendor evaluation pitfall: choosing a provider because they top a leaderboard, then discovering the benchmark used zero-shot prompt
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.9.html:256`
    > Google's seminal 2015 paper "Hidden Technical Debt in Machine Learning Systems" estimated that only about 5% of the code in a production ML 
  - `part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.2.html:71`
    > In the SWE-bench benchmark, the best AI coding agents solve 70%+ of SWE-Bench Verified issues (as of late 2025). For context, the average hu
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.1.html:260`
    > A single NVIDIA H100 GPU can serve roughly 30 to 50 concurrent users running a 70-billion-parameter model with 4-bit quantization. At cloud 
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.2.html:247`
    > Anthropic's own prompt engineering team uses meta-prompting internally. When developing system prompts for Claude, engineers routinely ask C
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.3.html:254`
    > In 2024, an engineer at a mid-sized startup reported that switching their entire product from GPT-4 to Claude 3.5 Sonnet took less than two 
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.4.html:71`
    > Production AI monitoring is like weather forecasting: you know the climate (your model's general behavior), but the weather (today's actual 
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.4.html:71`
    > Research on user feedback in production AI systems shows that only 3% to 7% of users ever click a thumbs-up or thumbs-down button. Yet that 
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.5.html:218`
    > Google's Bard (now Gemini) lost $100 billion in market value on its launch day because it gave a factually incorrect answer about the James 
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.6.html:63`
    > Gradio's gr.ChatInterface can turn a three-line Python function into a fully functional chatbot demo in under 60 seconds. This is both its g
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.6.html:63`
    > The first chatbot UI, ELIZA (1966), used a teletype terminal and fooled some users into thinking they were talking to a real therapist. Sixt
  - `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.9.html:59`
    > Traditional recommendation systems need thousands of user interactions to learn your preferences. An LLM can infer that someone who likes "D
  - `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.1.html:83`
    > If you plot enough benchmarks with binary scoring, even a goldfish's swimming ability would look "emergent" past a certain tank size. The da
  - `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.2.html:82`
    > Humanity spent thousands of years producing the written record. Frontier labs consumed most of it in a single training run. The internet, it
  - `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.1.html:239`
    > The "strawberry" test has become the unofficial litmus test for LLM reasoning. Ask a model how many r's are in "strawberry" and you will lea
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html:140`
    > When GPT-2 was released in 2019, OpenAI initially withheld the full model weights, citing concerns about misuse for generating fake news. Th
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html:301`
    > Masked language modeling is essentially a fill-in-the-blank exercise at massive scale. BERT learned to read by doing the same kind of worksh
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html:140`
    > The Chinchilla paper essentially told the entire industry: "You have been training your models wrong." It showed that most large models were
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html:129`
    > The Common Crawl dataset contains over 250 billion web pages, which after deduplication, quality filtering, and toxicity removal, typically 
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html:72`
    > Adam stores two extra FP32 tensors per parameter (the first-moment $m$ and second-moment $v$ estimates), so the optimizer states alone are 8
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html:106`
    > Training GPT-4 reportedly required tens of thousands of GPUs running in parallel for months. The electricity bill alone likely exceeded what
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html:132`
    > Nobody explicitly programmed in-context learning into LLMs. It emerged as a side effect of next-token prediction at scale. Researchers are s
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html:151`
    > DeepSeek-V3 (671B total, 37B active) achieved competitive performance with dense models while using only 1/18th of the parameters per forwar
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html:151`
    > Meta's Llama 3.1 training report revealed that their automated failure recovery system handled the vast majority of the 419 interruptions du
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html:68`
    > The pace of frontier model releases has become so rapid that by the time a benchmark paper finishes peer review, the model it evaluates may 
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html:77`
    > The original Llama weights were leaked online within a week of their restricted release in February 2023. Meta eventually embraced open dist
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html:166`
    > Ask most LLMs "What do you eat for breakfast?" and they will describe cereal, toast, or eggs. Ask the same question in Japanese, and the ans
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html:148`
    > The "think longer vs. be bigger" trade-off has a nice real-world analogy. Imagine you are trying to solve a crossword puzzle. If you are a n
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html:223`
    > DeepSeek R1-Zero, trained with zero supervised reasoning examples, spontaneously started writing phrases like "Hmm, let me reconsider..." an
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html:145`
    > AlphaProof sometimes spent three days on a single IMO problem, generating millions of candidate proof steps. A human mathematician solving t
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html:110`
    > Quantization is the art of convincing a model that it does not actually need 32 bits of precision per weight. In practice, most models barel
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html:231`
    > PagedAttention borrows the concept of virtual memory from operating systems, a technique that dates back to the 1960s. It took over 60 years
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html:99`
    > During standard autoregressive decoding, the GPU's compute units are roughly 99% idle, waiting for data to arrive from memory. Speculative d
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html:104`
    > vLLM went from a UC Berkeley research project to the default serving framework for the open-source LLM community in under a year. Its PagedA
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html:277`
    > The human brain operates with extreme sparsity: at any given moment, only about 1% to 5% of neurons are actively firing. The brain achieves 
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:145`
    > Attention visualization looks deceptively simple: just plot which tokens attend to which. In practice, a 32-layer, 32-head transformer produ
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:145`
    > Probing classifiers are small models trained to extract specific information from a larger model's internal representations. It is like givi
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:113`
    > Mechanistic interpretability aims to reverse-engineer neural networks the way you would reverse-engineer a circuit board: identify each comp
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:510`
    > LIME and SHAP, the two most popular explanation methods, take fundamentally different approaches: LIME fits a simple model locally, while SH
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:66`
    > Explaining transformer predictions to non-technical stakeholders is an art form. You cannot say "the cross-attention scores in layer 17 show
  - `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:624`
    > The OpenAI Chat Completions API format has become so ubiquitous that even competitors adopt it. vLLM, Ollama, and dozens of other serving to
  - `part-3-working-with-llms/module-11-llm-apis/section-11.2.html:106`
    > Before structured output modes existed, developers resorted to prompts like "Please respond ONLY in valid JSON. I repeat, ONLY JSON. No mark
  - `part-3-working-with-llms/module-11-llm-apis/section-11.2.html:106`
    > Before structured output existed, developers wrote elaborate regex parsers to extract JSON from LLM responses. Some production systems had m
  - `part-3-working-with-llms/module-11-llm-apis/section-11.3.html:211`
    > The circuit breaker pattern was borrowed from electrical engineering, where a physical circuit breaker prevents a short circuit from burning
  - `part-3-working-with-llms/module-11-llm-apis/section-11.4.html:451`
    > OpenAI's o1 model, the first widely available reasoning model, was initially so secretive about its thinking process that developers called 
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html:273`
    > Few-shot prompting is essentially "teaching by example" compressed into a few sentences. The GPT-3 paper showed that providing just two or t
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html:239`
    > Self-consistency works by asking the model the same question multiple times and taking a majority vote. It is the "ask the audience" lifelin
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html:279`
    > Using an LLM to optimize prompts for another LLM is the AI equivalent of asking a poet to write instructions for another poet. It sounds cir
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html:140`
    > Prompt injection is sometimes called "the SQL injection of AI," except that SQL injection was largely solved decades ago with parameterized 
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html:140`
    > In 2023, researchers demonstrated that a well-crafted prompt injection hidden in white text on a web page could hijack a browsing AI agent i
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html:69`
    > Researchers have found that adding the phrase "Take a deep breath and work through this step by step" to prompts improves math reasoning acc
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html:433`
    > A logistic regression model trained on TF-IDF features can classify spam emails in under a millisecond at a cost of essentially zero. An LLM
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html:447`
    > Using an LLM as a feature extractor is conceptually similar to how early deep learning practitioners used pretrained ImageNet models as feat
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html:585`
    > The "triage" pattern in hybrid pipelines mirrors how hospital emergency rooms work: a nurse (the lightweight classifier) quickly assesses ea
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html:173`
    > LLM pricing changes so frequently that any cost comparison table is outdated before it reaches the reader. Between January and December 2024
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html:173`
    > Some teams discover that their most expensive LLM calls are not the hardest queries but the most repetitive ones. A single semantic caching 
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.1.html:460`
    > Model collapse happens when a model trains on its own outputs across generations, gradually losing diversity and drifting toward repetitive 
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.2.html:520`
    > The cost of generating a million synthetic training examples with an LLM API is often less than the cost of hiring a single human annotator 
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.3.html:537`
    > Deduplication is the unsung hero of synthetic data pipelines. Without it, you end up with a dataset where 30% of the examples are minor para
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.4.html:429`
    > Active learning selects the most informative examples for human review, which means your annotators spend their time on the hard cases inste
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.5.html:490`
    > Snorkel, the framework that popularized programmatic labeling, was named after the idea of getting a shallow, noisy view of the data rather 
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.6.html:482`
    > When DeepSeek trained R1 with pure RL (no SFT warm-start), the model went through a "readability crisis" around step 5,000 of training. It d
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html:130`
    > Fine-tuning a 7-billion-parameter model on a single GPU was science fiction in 2020. By 2024, it had become a weekend project. The pace of t
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.4.html:583`
    > OpenAI's fine-tuning API distills the entire training process into a single API call with a JSONL file. What used to require a GPU cluster a
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.6.html:361`
    > Adding a classification head to a pretrained transformer is like putting a sorting hat on a very well-read student. The model already unders
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html:382`
    > Further Reading Context Extension Techniques Peng, B. et al. (2024). YaRN: Efficient Context Window Extension of Large Language Models . ICL
  - `part-4-training-adaptation/module-17-peft/section-17.1.html:94`
    > LoRA achieves 90%+ of full fine-tuning performance while training less than 1% of the parameters. It is the deep learning equivalent of alte
  - `part-4-training-adaptation/module-17-peft/section-17.2.html:542`
    > The PEFT method zoo has grown so large that researchers now publish "survey of survey" papers just to catalog them all. At last count, the l
  - `part-4-training-adaptation/module-17-peft/section-17.3.html:518`
    > Hugging Face's PEFT library reduced the code needed to add LoRA to a model from hundreds of lines to roughly five. Democratizing access to a
  - `part-4-training-adaptation/module-17-peft/section-17.3.html:518`
    > Axolotl, one of the popular fine-tuning frameworks, was named after the adorable Mexican salamander known for its regenerative abilities. Th
  - `part-4-training-adaptation/module-17-peft/section-17.4.html:580`
    > The original Prompt Tuning paper from Google included a striking experiment: they trained a single T5-XXL model with thousands of task-speci
  - `part-4-training-adaptation/module-17-peft/section-17.5.html:122`
    > Knowledge distillation was first proposed by Hinton, Vinyals, and Dean in 2015. The core insight (that a teacher model's soft probability di
  - `part-4-training-adaptation/module-17-peft/section-17.6.html:166`
    > Model merging combines multiple fine-tuned models into one without any additional training. It is like mixing paint colors: if blue is good 
  - `part-4-training-adaptation/module-17-peft/section-17.7.html:344`
    > Elastic Weight Consolidation is the neural network equivalent of putting "do not erase" signs on a whiteboard. New information fills the emp
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html:95`
    > RLHF was the secret ingredient that turned GPT-3 (impressive but erratic) into ChatGPT (impressive and polite). The technique had existed in
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html:147`
    > DPO (Direct Preference Optimization) eliminated the need for a separate reward model by baking preference learning directly into the languag
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html:79`
    > Constitutional AI asks the model to critique and revise its own outputs based on a set of written principles. It is self-improvement through
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.4.html:491`
    > DeepSeek-R1 demonstrated that RLVR can teach models to reason through complex math problems by rewarding correct final answers. The model sp
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html:73`
    > Scalable oversight is a bit like hiring a lifeguard who cannot swim as fast as the people in the pool. The lifeguard can still help when swi
  - `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:75`
    > The word "agent" comes from the Latin agere , meaning "to do." By that definition, most chatbots are really just "listeners" pretending to h
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html:64`  *(canonical)*
    > The original Word2Vec paper showed that king - man + woman = queen , but less publicized is that it also learned Paris - France + Italy = Ro
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html:147`
    > The "curse of dimensionality" means that in high-dimensional spaces, the distance between the nearest and farthest neighbor converges. In 76
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.3.html:201`
    > The vector database market went from "what's a vector database?" to over a dozen funded startups in roughly 18 months (2022 to 2024). For a 
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.4.html:122`
    > Ask ten RAG engineers for their optimal chunk size and you will get twelve answers. The chunking literature is littered with benchmarks "pro
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.4b.html:404`
    > BERTopic can optionally use an LLM to generate human-readable topic labels. Instead of a topic being described as "deployment, production, i
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html:458`
    > The ColPali team discovered that their model could retrieve relevant pages even when the query language differed from the document language.
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:176`
    > The original RAG paper by Lewis et al. (2020) was published while GPT-3 was still brand new. The authors could not have predicted that withi
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html:72`
    > Agentic RAG systems can sometimes spiral into what practitioners call "research rabbit holes," where the agent keeps generating follow-up qu
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html:90`
    > The Spider benchmark for text-to-SQL contains 10,181 questions across 200 databases. State-of-the-art LLMs now score above 85% on it, which 
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html:106`
    > In a 2024 study by Vectara, roughly 15% of RAG citations pointed to real sources but misrepresented what those sources actually said. The sy
  - `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html:52`
    > Named entity recognition was one of the first NLP tasks to reach "good enough" accuracy in the 1990s, and spaCy's modern transformer-based m
  - `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.5.html:251`
    > Named entity recognition (NER), one of the oldest NLP tasks, has been dramatically simplified by LLMs. What once required weeks of annotatio
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html:263`
    > HyDE essentially asks the model to hallucinate on purpose, then uses that hallucination to find real documents. It is one of the few techniq
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html:83`
    > Google's Knowledge Graph, launched in 2012, contained 570 million entities and 18 billion facts. Wikidata now has over 100 million items. If
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html:219`
    > The Leiden algorithm used by GraphRAG for community detection was developed at Leiden University and published in 2019 as a fix for the Louv
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html:122`
    > The Airbyte connector catalog has grown so fast that there are now more pre-built data connectors (350+) than there are countries on Earth (
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html:74`
    > LangChain's GitHub repository accumulated over 400 open issues about breaking changes in its first year alone. The framework moved so fast t
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.1.html:83`
    > ELIZA, the 1966 chatbot that simulated a Rogerian therapist, worked entirely by pattern matching and rephrasing the user's own words as ques
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.2.html:61`
    > Character.AI reported that users sent over 20 billion messages per month in 2024, with some users chatting with their AI personas for hours 
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html:76`
    > Human working memory holds roughly 7 items (plus or minus 2), a number established by George Miller in 1956. A 128K-token context window hol
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html:62`
    > Researchers at Stanford found that users correct chatbot misunderstandings an average of 3.2 times before giving up and rephrasing their ent
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html:90`
    > Early telephone IVR systems gave callers about 8 seconds of patience before they started mashing the "0" key for a human operator. Voice AI 
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.6.html:61`
    > The human brain processes speech with a latency of about 200 milliseconds from ear to comprehension. Users start perceiving voice AI as "lag
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html:98`
    > BLEU score was invented in 2002 for machine translation and is still the most cited evaluation metric in NLP. It essentially counts matching
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.10.html:145`
    > A 2024 analysis found that over 40% of papers on arXiv claiming "state-of-the-art" LLM results used a single evaluation run with no confiden
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.2.html:70`
    > A surprising number of published LLM benchmarks use fewer than 200 test examples. At that size, a 95% confidence interval on accuracy spans 
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.3.html:65`
    > The phrase assertEqual(llm_output, expected) is the fastest way to write a test that fails every time the model gets updated, the temperatur
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html:76`
    > Google's internal LLM deployment pipeline reportedly requires over 400 evaluation checks to pass before a model update reaches production. M
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.6.html:62`
    > Without tracing, debugging an LLM application is like debugging a web server by reading the access log backwards while blindfolded. Most tea
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.7.html:71`
    > A 2024 survey found that fewer than 15% of published LLM papers provided enough detail to reproduce their main results. The most common miss
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.8.html:190`
    > The original Needle-in-a-Haystack test went viral on Twitter/X in November 2023 when Greg Kamradt published colorful heatmaps showing that C
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.9.html:84`
    > The first version of the OpenTelemetry GenAI semantic conventions was drafted during a hackathon where engineers from six different LLM obse
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html:144`
    > In a well-known experiment, GPT-4 acting as a judge rated GPT-4's own outputs as the best response 67% of the time, compared to 50% when jud
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 2. CALLOUT TITLE (same title)  |  145 sections
- **Key/signature**: `research frontier`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html:512`
    > AutoML and neural architecture search (NAS) are reducing the need for manual feature engineering and model selection. Foundation models are 
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.2.html:499`
    > Beyond backpropagation remains an active research area. Forward-forward learning (Hinton, 2022) proposes training networks without backpropa
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html:1127`
    > PyTorch continues to evolve rapidly. PyTorch 2.x introduced torch.compile , which automatically generates optimized GPU kernels through grap
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html:340`
    > RL for LLM alignment is the dominant application of RL in modern AI. RLHF (covered in Section 18.1 ) and its alternatives like DPO and GRPO 
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.1.html:404`
    > The boundary between NLP tasks is dissolving. Modern LLMs increasingly treat all NLP tasks as text generation, unifying classification, extr
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html:623`
    > Classical preprocessing is declining in importance as subword tokenizers and large language models handle raw text directly. However, prepro
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html:700`
    > Static embeddings are far from dead. While contextual models dominate, static embeddings remain important for lightweight applications, cros
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html:491`
    > Contextual representations have evolved far beyond ELMo. Modern models like GPT-4, Claude 3.5, and Gemini 2.0 produce contextual embeddings 
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.5.html:636`
    > Tokenizer-free models are an active research frontier. Byte-level models like ByT5 and MegaByte process raw bytes without any tokenization, 
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.6.html:592`
    > Tokenizer training is becoming more principled. Recent work provides theoretical frameworks for choosing vocabulary sizes rather than relyin
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:748`
    > Chat template standardization is an ongoing challenge. Different model families (Llama, Mistral, ChatML, Claude) use different special token
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html:684`
    > State-space models (SSMs) are emerging as a viable alternative to both RNNs and Transformers. Mamba (Gu and Dao, 2023) combines the linear-t
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.2.html:578`
    > Attention efficiency remains a central research concern. Linear attention methods replace softmax with kernel functions to achieve O(n) comp
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html:778`
    > Efficient attention variants remain one of the most active research areas. Grouped-query attention (GQA), used in Llama 2 /3 and Mistral, re
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html:1063`
    > Post-Transformer architectures are an active area of exploration. State-space models like Mamba (Gu and Dao, 2023) achieve linear-time seque
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html:988`
    > Reference implementations continue to improve accessibility. Andrej Karpathy's nanoGPT remains a popular educational resource. Meta's torcht
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html:753`
    > Attention itself keeps evolving. Differential Attention (Ye et al., 2024) reduces attention noise by subtracting two softmax distributions, 
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html:585`
    > Hardware-software co-design is accelerating. NVIDIA's Blackwell (B200/GB200) GPUs introduce a second-generation Transformer Engine with FP4 
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html:419`
    > Formal reasoning capacity of LLMs is a rapidly evolving theoretical topic. Merrill and Sabharwal (2024) showed that bounded-precision Transf
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.6.html:516`
    > Architecture innovation is accelerating. DeepSeek-V3 (2024) combines multi-head latent attention (MLA) with DeepSeekMoE for efficient 671B-p
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html:549`
    > Speculative decoding is transforming deterministic generation. Rather than generating one token at a time from the large model, a small "dra
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html:570`
    > Adaptive sampling is an emerging area. Min-p sampling (2023) dynamically adjusts the probability threshold based on the model's confidence, 
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html:70`
    > Contrastive decoding was introduced by Li et al. (2023). It remains an active area of research and is not yet a standard production techniqu
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html:70`
    > MBR decoding has a long history in speech recognition and machine translation. Recent work (Bertsch et al., ICLR 2025) has demonstrated its 
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html:70`
    > Structured output generation is becoming a standard production requirement. Libraries like Outlines (dottxt, 2024) and instructor (jxnl, 202
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:60`
    > This section covers an active and rapidly evolving research area. The models and results discussed here represent the state of the art as of
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:60`
    > Discrete diffusion is evolving rapidly. Mercury (Inception Labs, 2025) achieved the first production-quality diffusion LLM, generating 1,000
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.2.html:633`
    > Automated red teaming with adversarial LLMs. The most promising frontier in red teaming is using LLMs to attack other LLMs. Rather than rely
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.4.html:485`
    > Formal safety proofs for agentic systems. Can we mathematically guarantee that an LLM agent will never take certain dangerous actions? Curre
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html:621`
    > Machine unlearning for LLMs seeks to remove specific training data points from a model after training, without retraining from scratch.
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.3.html:267`
    > Federated instruction tuning and federated RLHF are active research areas. FedIT (Zhang et al., 2024) showed that federating the instruction
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.2.html:596`
    > Automated conformity assessment. The research community is working on tools that can automatically generate portions of the conformity asses
  - `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html:735`
    > Carbon-aware scheduling is an emerging paradigm where training jobs are automatically routed to data centers with the lowest real-time carbo
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html:381`
    > Several research directions are pushing the boundaries of LLM performance and portability. Disaggregated inference (Splitwise, DistServe) se
  - `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html:109`
    > Three frontier questions remain: (1) does top-1% gradient sparsification preserve quality at 100B+ parameters, where the loss landscape has 
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html:588`
    > The Kubernetes ecosystem for LLM workloads is evolving rapidly. LeaderWorkerSet is a new Kubernetes API (alpha in 2024) designed specificall
  - `part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.2.html:403`
    > Autonomous Software Engineering is advancing rapidly.
  - `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.9.html:546`
    > Conversational data analysis extends NL-to-Analytics beyond single questions to multi-turn exploration sessions. Research on systems like Da
  - `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.9.html:546`
    > Generative recommendation is emerging as a paradigm where LLMs generate item descriptions or even entire product concepts tailored to indivi
  - `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.3.html:47`
    > The convergence of architectures. Mamba-2's state space duality theorem suggests that SSMs and attention may be endpoints on a spectrum rath
  - `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.4.html:38`
    > Whole-genome foundation models like Evo-2 can now process sequences of over 1 million base pairs, approaching chromosome-scale context.
  - `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.4.html:38`
    > Cross-domain foundation models are the next frontier. Can a single model trained on text, protein sequences, molecular SMILES, and genomic d
  - `part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.2.html:34`
    > The deepest open question is whether weak-to-strong scaling generalises to capabilities beyond the weak supervisor's range. Empirical eviden
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html:430`
    > Post-training as the new frontier. The landmark model progression from BERT to GPT-4 focused primarily on scaling pre-training. By 2025, the
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html:652`
    > Beyond next-token prediction. Multi-token prediction (Gloeckle et al., 2024) demonstrated that predicting multiple future tokens simultaneou
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html:385`
    > Inference-time scaling laws. While traditional scaling laws focus on training compute, a parallel line of research explores scaling at infer
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html:391`
    > Model-guided data selection. Traditional data curation relies on heuristic filters and human-crafted rules. The frontier is moving toward mo
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html:438`
    > Beyond Adam: muon and schedule-free optimization. While AdamW dominates current practice, several promising alternatives have emerged. Muon 
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html:546`
    > Disaggregated training and heterogeneous clusters. Traditional distributed training assumes homogeneous GPU clusters connected by fast inter
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html:360`
    > Mechanistic understanding of ICL. Recent work by Todd et al. (2024) has identified "function vectors" that encode specific input-output mapp
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html:505`
    > Several active research directions aim to push training efficiency further. Fully asynchronous pipeline parallelism (e.g., PipeDream-2BW, ze
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html:584`
    > Frontier model convergence and differentiation. By early 2025, the gap between top frontier models has narrowed significantly on standard be
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html:760`
    > Open reasoning models and distillation. DeepSeek-R1 (2025) demonstrated that open-weight models can achieve reasoning capabilities comparabl
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html:499`
    > Culturally-aware language models. Beyond multilingual capability, recent work focuses on cultural alignment: ensuring models behave appropri
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html:554`
    > The optimal allocation of test-time compute remains an active research problem. Snell et al. (2024) showed that compute-optimal inference re
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html:466`
    > The reasoning model landscape is evolving at an extraordinary pace. OpenAI's o3 (late 2024) and o4-mini (2025) significantly advanced perfor
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html:393`
    > Training reasoning models is one of the most active areas in LLM research. DeepSeek's GRPO algorithm (2025) showed that critic-free RL can p
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.4.html:345`
    > Best practices for prompting reasoning models are still being discovered as new models launch. Researchers at Microsoft (2025) found that "m
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html:68`
    > The future of test-time compute scaling. Several active research directions are pushing the boundaries of what reasoning models can achieve:
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html:555`
    > Sub-4-bit and mixed-precision quantization. Research is pushing quantization below 4 bits. QuIP# (2024) achieves competitive quality at 2 bi
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html:449`
    > KV cache compression for million-token contexts. As context windows grow beyond 100K tokens, KV cache memory becomes the dominant bottleneck
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html:514`
    > Speculative decoding for reasoning models. Reasoning models like o1 and DeepSeek-R1 generate thousands of thinking tokens before producing a
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html:734`
    > Disaggregated inference and specialized hardware. The emerging paradigm of disaggregated inference separates prefill (compute-bound) and dec
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html:292`
    > The intersection of pruning and training is an active research area. Pruning-aware pretraining integrates sparsity constraints during the pr
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.6.html:283`
    > Test-time compute scaling is one of the fastest-moving areas in LLM research. Several directions are particularly active as of early 2026. L
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:792`
    > Attention analysis is being refined through causal interventions (activation patching) that go beyond correlational attention pattern visual
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:75`
    > Anthropic's circuit tracing work opens several research directions. First, attribution graphs can be compared across prompts to identify uni
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:75`
    > Anthropic's work on sparse autoencoders for decomposing model activations into interpretable features represents a breakthrough in scaling m
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:678`
    > Production interpretability tools are evolving from post-hoc explanations toward real-time interpretability dashboards that surface feature 
  - `part-2-understanding-llms/module-10-interpretability/section-10.4b.html:515`
    > The logit lens family of techniques (including the tuned lens and future lens) is revealing how transformer layers progressively refine pred
  - `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:628`
    > Unified multi-provider protocols. The proliferation of provider-specific API formats has driven projects like LiteLLM and the emerging Model
  - `part-3-working-with-llms/module-11-llm-apis/section-11.2.html:619`
    > Grammar-constrained decoding. Libraries like Outlines and Guidance enforce output schemas at the token level during generation, achieving 10
  - `part-3-working-with-llms/module-11-llm-apis/section-11.3.html:721`
    > Semantic caching. Rather than caching exact prompt matches, systems like GPTCache and Zilliz embed incoming prompts and search for semantica
  - `part-3-working-with-llms/module-11-llm-apis/section-11.4.html:587`
    > The optimal allocation of thinking budget across tasks is an open research problem.
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html:637`
    > Automatic prompt optimization. Tools like DSPy (Khattab et al., 2024) and OPRO (Yang et al., 2024) treat prompt engineering as an optimizati
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html:764`
    > Reasoning tokens and internal chain-of-thought. Models like OpenAI o1/o3 and DeepSeek-R1 internalize chain-of-thought reasoning, generating 
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html:692`
    > Meta-prompting and recursive self-improvement. Research on having LLMs design and refine their own prompts shows promising results, with sys
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html:369`
    > Prompt injection defenses. The arms race between prompt injection attacks and defenses continues to accelerate. Techniques like spotlighting
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html:426`
    > Prompt optimization is converging with agent design. DSPy's latest work treats entire agent pipelines (retrieval, reasoning, tool use, outpu
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html:437`
    > Small language models closing the gap. Models under 10B parameters (Phi-4, Gemma 3, Llama 3.2) are achieving surprisingly strong performance
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html:451`
    > Embedding model specialization. Purpose-built embedding models (Nomic Embed, Jina Embeddings v3, Cohere Embed v3) are outperforming general-
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html:589`
    > Adaptive pipeline architectures. Research teams are building pipelines that dynamically adjust their ML/LLM mix based on real-time quality m
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html:634`
    > LLM cost prediction models. Researchers are building statistical models that predict LLM API costs from task descriptions and sample inputs,
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html:893`
    > Dataset engineering is evolving rapidly. Active areas include automated data curation agents that iteratively refine datasets based on model
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.1.html:464`
    > Researchers are exploring self-improving synthetic data loops where models iteratively refine their own generated training sets using reward
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.2.html:867`
    > The 2024 wave of persona-driven generation pipelines (as seen in Cosmopedia and Persona Hub) represents a shift toward controlling synthetic
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.3.html:647`
    > Automated data quality scoring is moving beyond simple heuristics toward learned quality predictors that can estimate the training value of 
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.4.html:488`
    > Active learning with LLM labelers is converging with curriculum learning strategies, where the difficulty and diversity of selected examples
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.5.html:505`
    > The integration of LLMs as labeling functions within frameworks like Snorkel is creating hybrid systems that combine programmatic rules with
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.6.html:552`
    > Several open research directions are shaping the next generation of synthetic reasoning data. Process reward models (PRMs) aim to verify ind
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.7.html:441`
    > Data augmentation for LLMs is advancing in several directions. Self-augmentation loops use a model's own outputs as augmentation candidates,
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html:327`
    > The boundary between prompting and fine-tuning is blurring with techniques like in-context learning distillation , which compresses few-shot
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.2.html:502`
    > Data-centric AI research is producing automated tools for detecting and correcting label errors, near-duplicates, and outliers in fine-tunin
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.3.html:702`
    > Research on selective fine-tuning identifies which layers and layer normalization matter most for specific tasks, enabling targeted weight u
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.4.html:776`
    > Provider fine-tuning APIs are evolving toward continuous fine-tuning workflows where models are incrementally updated as new data arrives, r
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.5.html:362`
    > Contrastive fine-tuning methods like GISTEmbed and instructor-based approaches are producing task-aware embeddings that outperform general-p
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.6.html:401`
    > The integration of LLMs with traditional classification heads is yielding hybrid architectures that combine the reasoning capability of lang
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html:333`
    > The extension of context windows beyond 1 million tokens (as in Gemini 1.5) has been enabled by innovations in positional encoding, includin
  - `part-4-training-adaptation/module-17-peft/section-17.1.html:750`
    > LoRA variants continue to proliferate: DoRA decomposes weight updates into magnitude and direction components, while rsLoRA applies rank-dep
  - `part-4-training-adaptation/module-17-peft/section-17.2.html:546`
    > Unified PEFT frameworks are emerging that combine adapter insertion, soft prompt tuning, and low-rank decomposition into a single configurab
  - `part-4-training-adaptation/module-17-peft/section-17.3.html:638`
    > Training platforms are converging on declarative configuration formats (like Axolotl's YAML-based setup) that abstract away distributed trai
  - `part-4-training-adaptation/module-17-peft/section-17.4.html:575`
    > Recent work explores transferable soft prompts : can a soft prompt trained for task A be transferred to task B by composing it with a small 
  - `part-4-training-adaptation/module-17-peft/section-17.5.html:1047`
    > The success of distillation in creating small reasoning models (like DeepSeek-R1-Distill and Phi-4-mini) has demonstrated that chain-of-thou
  - `part-4-training-adaptation/module-17-peft/section-17.6.html:435`
    > Model merging has moved beyond simple weight averaging with methods like TIES-Merging (which resolves sign conflicts between parameter delta
  - `part-4-training-adaptation/module-17-peft/section-17.7.html:460`
    > Continual learning for LLMs is advancing through replay-based methods that mix small amounts of previous task data into new training batches
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html:720`
    > At the infrastructure level, hybrid training engines like OpenRLHF and veRL are making RLHF accessible by co-scheduling generation and train
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html:863`
    > DPO variants are rapidly expanding: IPO addresses overfitting to preference noise, KTO works with binary (good/bad) feedback instead of pair
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html:469`
    > Constitutional AI is expanding toward democratic constitution design , where diverse groups of stakeholders collaboratively define the princ
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.4.html:495`
    > RLVR (Reinforcement Learning with Verifiable Rewards) is emerging as a powerful paradigm for domains with automated evaluation, where formal
  - `part-5-multimodal-llms/module-20-audio-music-generation/section-20.10.html:131`
    > Audio, music, and video generation are advancing on three open frontiers in 2025-2026. First, minute-plus video consistency: how do you keep
  - `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.4.html:224`
    > Document understanding is in transition from pipeline OCR plus layout to end-to-end multimodal models that read documents the way humans do.
  - `part-5-multimodal-llms/module-22-vision-language-models/section-22.9.html:202`
    > Vision-language models are converging on three open research questions in 2025-2026. First, native multimodal pretraining versus connector-b
  - `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.5.html:207`
    > 3D generation has shifted from NeRF-based representations to fast-rendering Gaussian splatting and feed-forward priors. The frontier in 2024
  - `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:700`
    > Agentic Reasoning and Self-Improvement (2024-2026): Recent work explores agents that learn from their own execution traces, adapting their s
  - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html:690`
    > Tool use protocols are the connective tissue of agentic AI, and 2024-2026 has produced both rapid standardization and open research question
  - `part-6-agentic-ai/module-28-multi-agent-systems/section-28.3.html:201`
    > Emergent communication protocols. When multiple LLM agents interact, they can develop shared conventions, shorthand, and even novel communic
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.4.html:483`
    > Specialized agents (coding agents, web agents, computer-use agents, scientific-research agents) are the most measurable proving ground for L
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html:1059`  *(canonical)*
    > Matryoshka and adaptive-dimension embeddings (Kusupati et al., 2024) allow a single model to produce embeddings at multiple dimensionalities
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html:683`
    > Graph-based indexes with learned routing are replacing static HNSW configurations with neural network-guided neighbor selection, improving r
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.3.html:722`
    > Disaggregated vector search separates compute from storage, allowing index serving to scale independently of data ingestion. Multi-modal vec
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.4b.html:777`
    > LLM-guided chunking uses language models to identify semantic boundaries in documents, producing chunks that align with topical shifts rathe
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html:550`
    > Several research directions are expanding the capabilities of vision-based retrieval. Efficient late interaction explores binary and product
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:1054`
    > Self-RAG (Asai et al., 2024) trains the LLM to decide when to retrieve, what to retrieve, and how to use retrieved passages, eliminating the
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html:709`
    > Planning-based RAG agents decompose complex queries into retrieval plans before executing any searches, improving both efficiency (fewer unn
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html:619`
    > LLM-native SQL generation is improving through specialized fine-tuning on SQL benchmarks (BIRD, Spider 2.0), with models like SQLCoder and D
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html:363`
    > Fine-grained attribution research is exploring token-level and span-level source linking, where each phrase in a generated answer traces bac
  - `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.4.html:203`
    > Cross-modal RAG, where the retriever and the reader span text, images, tables, and code, is one of the most active research areas in retriev
  - `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.5.html:263`
    > Structured information extraction with LLMs is being reshaped by two open research questions in 2024-2026. First, schema-guided extraction a
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html:978`
    > Learned sparse retrieval (SPLADE v3, 2024) is narrowing the gap with dense retrieval while maintaining the interpretability and efficiency o
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html:478`
    > LLM-constructed knowledge graphs are enabling automatic ontology discovery and entity linking from unstructured text at scale, reducing the 
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html:422`
    > Temporal GraphRAG systems are extending knowledge graphs with time-stamped relationships, enabling queries like "How has the treatment lands
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html:507`
    > Multimodal ingestion pipelines are extending beyond text to process images, tables, and diagrams as first-class content, using vision-langua
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html:1050`
    > DSPy (Stanford, 2024) is pioneering a compiler-based approach to RAG pipeline optimization, automatically tuning prompts and few-shot exampl
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.1.html:780`
    > Structured dialogue generation with constrained decoding (Outlines, Instructor) ensures that conversational agents produce responses that co
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.2.html:639`
    > Dynamic persona adaptation adjusts the system prompt based on detected user expertise, emotional state, or conversational goals, creating a 
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html:776`
    > LLM-as-judge for conversations uses a separate LLM to evaluate dialogue quality across dimensions like coherence, helpfulness, and persona c
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.5.html:1028`
    > Retrieval-augmented memory stores conversation history in a vector database and retrieves relevant past exchanges based on the current query
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html:580`
    > Multimodal voice agents are expanding beyond audio to combine speech, vision, and gesture recognition, enabling agents that understand what 
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.6.html:845`
    > Real-time speech-to-speech models (e.g., GPT-4o voice mode, Gemini Live) bypass the traditional ASR-LLM-TTS pipeline by processing audio tok
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html:874`
    > Open Questions in LLM Evaluation (2024-2026):
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.10.html:68`
    > Toward preregistered LLM research. The social sciences addressed their replication crisis partly through preregistration: researchers public
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.2.html:727`
    > Open Questions in Statistical Evaluation (2024-2026):
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.3.html:542`
    > Open Questions in LLM Testing (2024-2026):
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.4.html:116`
    > Open Questions in Drift Detection (2024-2026):
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html:550`
    > Open Questions in Evaluation-Driven Quality Gates (2024-2026):
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.6.html:502`
    > Open Questions in LLM Observability (2024-2026):
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.7.html:479`
    > Open Questions in LLM Reproducibility (2024-2026):
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.8.html:675`
    > Ring Attention and Sequence Parallelism distribute long sequences across multiple GPUs, with each device processing a segment and passing KV
  - `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.3.html:258`
    > Open Questions in Simulation-Based Evaluation (2024-2026):
  - `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.4.html:281`
    > Open Questions in Code-Generation Evaluation (2024-2026):
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.5.html:164`
    > LLM-as-judge has rapidly become standard practice for evaluating open-ended generation, but 2024-2026 research has exposed serious failure m
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 3. CALLOUT TITLE (same title)  |  89 sections
- **Key/signature**: `warning`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html:223`
    > The learning rate is the single most important hyperparameter in optimization. Too large, and the steps overshoot the minimum, causing the l
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html:223`
    > Never tune your model based on test set performance. The moment you use test results to make modeling decisions, the test set becomes a vali
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html:318`
    > Vanilla REINFORCE (shown above) works in theory but suffers from high variance: training is noisy and unstable. In practice, researchers use
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html:306`
    > No single defense is sufficient against prompt injection. Regex-based detection catches only known patterns. ML-based classifiers can be eva
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html:306`
    > No current watermarking method is fully robust against a determined adversary. Text watermarks can be defeated by paraphrasing, translation 
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.3.html:155`
    > Never load pickle-format model files ( .bin , .pt , .pkl ) from untrusted sources. Treat them with the same caution you would give to an exe
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.3.html:155`
    > If your application accepts image, audio, or video inputs, you must assume that adversarial content can be embedded in those modalities. Tex
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.1.html:193`
    > Guardrails add latency to every agent action. A guardrail that adds 200ms per check across 10 tool calls adds 2 seconds to the total respons
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.2.html:123`
    > Container isolation is not VM-level isolation. Container escapes, while rare, have been documented (CVE-2019-5736, CVE-2024-21626). For high
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.3.html:529`
    > Benchmark scores are necessary but not sufficient for production safety. An agent that scores well on b3 and tau-bench has demonstrated robu
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.4.html:372`
    > Never load a pickle-format model file from an untrusted source without scanning it first. The torch.load() function executes arbitrary Pytho
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.5.html:295`
    > LLM self-reported confidence scores are not well calibrated. Models tend to express high confidence even when wrong. Use self-consistency (a
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.2.html:360`
    > Approximate unlearning methods (gradient ascent, task vectors) do not provide the same guarantees as retraining from scratch. Recent researc
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.1.html:127`
    > All three initial enforcement phases are now active. As of March 2027, prohibited practices (Phase 1), GPAI transparency obligations (Phase 
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.5.html:195`
    > Organizations that deploy AI systems in high-stakes domains (hiring, lending, healthcare, criminal justice) without documented governance pr
  - `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.1.html:473`
    > Guardrails add latency to every request. Profile your guardrail stack and set a latency budget. Lightweight checks (regex, blocklist, Prompt
  - `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.2.html:404`
    > A/B tests on LLM outputs require larger sample sizes than traditional web experiments because LLM quality metrics (like human ratings or LLM
  - `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.1.html:432`
    > Semantic caching introduces a subtle correctness risk: two queries that appear semantically similar may require different answers depending 
  - `part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html:574`
    > Budget-aware retries require accurate cost tracking, which means your AI gateway must report token usage for failed requests, not just succe
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.1.html:288`
    > The docker system prune -a --volumes command removes all unused images, containers, and volumes. If you have model weights stored in named v
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.2.html:267`
    > Forgetting a .dockerignore file is one of the most common mistakes in ML Docker projects. Without it, a COPY . . instruction will copy your 
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.3.html:298`
    > Without condition: service_healthy , your API container may start and immediately crash because the LLM server is still loading model weight
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html:224`
    > When baking model weights into an image, pass the HuggingFace token as a build argument ( --build-arg HF_TOKEN=... ), not as an ENV instruct
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.5.html:354`
    > Never rely on a single hallucination defense. Each layer has failure modes: RAG retrieval (recall the retrieval pipelines from Chapter 32 ) 
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.7.html:522`
    > The "Demo Trap" is the single most common reason enterprise LLM projects are approved but later fail. A compelling demo with 5 handpicked ex
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.8.html:484`
    > TCO calculations often underestimate build costs by 30 to 50% because they exclude opportunity cost (what else could the engineers be buildi
  - `part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.2.html:352`
    > AI-generated code carries real risks. Security vulnerabilities are common: models may generate code with SQL injection, hardcoded secrets, o
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.5.html:531`
    > Serverless GPU platforms charge per second of GPU time. A misconfigured container_idle_timeout can keep expensive GPUs running idle. Always 
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.6.html:410`
    > Streamlit reruns the entire script on every interaction. For LLM applications, this means you must store chat history in st.session_state an
  - `part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.1.html:118`
    > None of the five use cases above is safe to deploy without the verification or human-review step described alongside it. Legal practice oper
  - `part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.3.html:62`
    > Several large law firms have been criticized in 2024-2025 for vague boilerplate disclosure that gestured at AI use without specifying what t
  - `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.6.html:71`
    > The legal landscape around AI-generated creative work is unsettled. Three issues recur: (1) training data licensing (the RIAA's suit against
  - `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.9.html:504`
    > LLM-based recommendation faces significant scalability challenges. Generating a personalized recommendation for each user request requires a
  - `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.4.html:139`
    > EHR language models raise significant privacy and fairness concerns. Patient data is highly sensitive, models can encode and amplify healthc
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html:233`
    > The existence of true "emergence" is contested. Schaeffer, Miranda, and Koyejo (2023) argued that many apparent emergent capabilities are ar
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html:130`
    > Kaplan's experiments did not train models to convergence. The largest models were stopped early, which biased the results toward favoring la
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html:221`
    > Note: This code example is conceptual and requires downloading a language model (e.g., GPT-2) to run. The purpose is to illustrate the task 
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html:221`
    > The mesa-optimization perspective remains an active area of debate. It is unclear whether the internal computations of real LLMs are truly o
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html:458`
    > Formal theorem proving with LLMs requires significant compute even at small scale. Compiling mathlib takes several hours, and each proof sea
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:168`
    > Attention weights show where the model "looks" but not what it "sees." High attention to a token does not necessarily mean that token is imp
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:349`
    > A major practical challenge with SAEs is "dead features": latent dimensions that never activate after initialization. With expansion factors
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:385`
    > Model editing is powerful but fragile. Edits can have unintended side effects: changing "The president is X" might also change answers to re
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:462`
    > Perturbation methods have a fundamental limitation: removing a token creates an out-of-distribution input. The model was never trained on in
  - `part-2-understanding-llms/module-10-interpretability/section-10.6.html:236`
    > Setting gpu_memory_utilization too high (above 0.95) can cause out-of-memory errors under bursty load, because the scheduler may attempt to 
  - `part-2-understanding-llms/module-10-interpretability/section-10.6.html:236`
    > The --max-batch-prefill-tokens parameter directly affects GPU memory usage during the prompt processing phase. Setting it too high can cause
  - `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:65`
    > All pricing figures in this chapter reflect approximate rates as of early 2025. LLM API prices change frequently, often decreasing by 50% or
  - `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:65`
    > API version drift: Enterprise wrappers sometimes lag behind the direct provider APIs by days or weeks. A feature available on api.openai.com
  - `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:65`
    > Never hardcode API keys. Store them in environment variables, secrets managers (like AWS Secrets Manager or HashiCorp Vault), or .env files 
  - `part-3-working-with-llms/module-11-llm-apis/section-11.2.html:81`
    > Without enforcement, an LLM asked for JSON might return: Here is the JSON: {"name": "Alice"... (wrapped in prose), or {"name": "Alice", "sen
  - `part-3-working-with-llms/module-11-llm-apis/section-11.2.html:81`
    > Malformed tool call arguments: Although models are generally reliable at producing valid JSON for tool calls, they can occasionally generate
  - `part-3-working-with-llms/module-11-llm-apis/section-11.3.html:358`
    > The 0.95 cosine similarity threshold is a reasonable starting point, but it must be calibrated for your specific use case. A false cache hit
  - `part-3-working-with-llms/module-11-llm-apis/section-11.3.html:358`
    > Soft limits and hard limits: Implement both. A soft limit (at 80% of budget) triggers an alert so you can investigate usage patterns. A hard
  - `part-3-working-with-llms/module-11-llm-apis/section-11.4.html:239`
    > Reasoning tokens count toward your usage and are billed at the model's output token rate. For OpenAI's o3, reasoning tokens are billed at th
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html:73`
    > Automatic prompt optimization can overfit to the training set, just like any machine learning process. Always evaluate optimized prompts on 
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html:62`
    > Using an LLM as the router adds cost to every single request. If the router itself costs $0.0003 per call, you need the routing savings to e
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.1.html:275`
    > Model collapse is cumulative and often invisible. The first generation of synthetic data may look fine. The second generation looks slightly
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.2.html:516`
    > Avoid trivially distinguishable pairs. If the rejected response is clearly terrible (e.g., random text or completely off-topic), the model l
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.4.html:425`
    > High LLM-human agreement does not always mean high quality. If the LLM and a single annotator agree strongly but disagree with other annotat
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.6.html:93`
    > Skipping verification is the most common and most damaging shortcut in reasoning data generation. A model that produces fluent, confident, w
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html:279`
    > Do not skip general evaluation. Many teams only measure performance on their target task during fine-tuning and discover too late that the m
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.2.html:459`
    > Garbage in, garbage out. No amount of hyperparameter tuning or clever training tricks can compensate for low-quality training data. Invest t
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.4.html:700`
    > Data privacy is non-negotiable for some industries. If you work in healthcare (HIPAA), finance (SOC 2), or government (FedRAMP), sending tra
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.6.html:239`
    > Subword tokenization breaks word boundaries. A critical challenge in token classification is that the tokenizer may split a single word into
  - `part-4-training-adaptation/module-17-peft/section-17.2.html:55`
    > Prompt Tuning and IA3 achieve extreme parameter efficiency, but they are significantly less capable than LoRA for complex adaptation tasks. 
  - `part-4-training-adaptation/module-17-peft/section-17.3.html:450`
    > Unsloth's speed advantage comes from custom CUDA/Triton kernels that may lag behind the latest model architectures. When a new model is rele
  - `part-4-training-adaptation/module-17-peft/section-17.5.html:425`
    > Black-box distillation from proprietary API models raises important licensing considerations. Most API providers (OpenAI, Anthropic, Google)
  - `part-4-training-adaptation/module-17-peft/section-17.5.html:425`
    > Licensing terms change frequently. Always check the current Terms of Service before starting a distillation project. A policy that was permi
  - `part-4-training-adaptation/module-17-peft/section-17.6.html:115`
    > Model merging requires enough system memory (RAM, not GPU VRAM) to hold all models simultaneously. Merging three 7B models in BF16 requires 
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html:704`
    > RLHF training is notoriously unstable. Common failure modes include reward hacking (the policy exploits reward model weaknesses), mode colla
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html:490`
    > Synthetic preferences inherit the biases of the judge model. If the judge systematically prefers verbose responses, the trained model will l
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html:490`
    > Reward overoptimization is not a theoretical concern; it appears reliably in practice. Models trained with DPO for too many epochs often pro
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html:93`
    > The alignment tax is real but often overstated. Careful alignment training with appropriate KL penalties preserves most general capabilities
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.4.html:56`
    > Extending RLVR beyond math and code is challenging because most real-world tasks lack clean verifiable signals. A customer service response 
  - `part-6-agentic-ai/module-26-ai-agents/section-26.2.html:205`
    > Reflection loops can get stuck in infinite self-criticism cycles where the agent repeatedly revises its output without making meaningful pro
  - `part-6-agentic-ai/module-26-ai-agents/section-26.3.html:140`
    > Do not over-prompt reasoning models. Unlike standard models that benefit from detailed chain-of-thought instructions, reasoning models alrea
  - `part-6-agentic-ai/module-26-ai-agents/section-26.5.html:321`
    > Never run untrusted tool code in the same process as your agent without sandboxing. A tool that enters an infinite loop, consumes all availa
  - `part-6-agentic-ai/module-26-ai-agents/section-26.6.html:133`
    > The single most common production bug in agent memory is letting raw tool outputs accumulate in the conversation buffer. A reasonable-lookin
  - `part-6-agentic-ai/module-26-ai-agents/section-26.6.html:133`
    > Checkpoints are a frequent privacy blind spot: developers remember to redact PII from the conversation buffer but forget that the agent's se
  - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html:69`
    > Not all "function calling" implementations are equal. Some open-source models format tool calls as JSON within their text output rather than
  - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.3.html:128`
    > A2A is still a relatively new protocol (announced April 2025) and the ecosystem is less mature than MCP's. While the specification is stable
  - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.4.html:136`
    > Never return raw API responses or stack traces as tool results. A 2,000-character stack trace consumes context window tokens without helping
  - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.5.html:139`
    > Retrieval is the easiest tool to over-use, because it almost always returns something . Agents that retrieve on every turn rack up cost and 
  - `part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html:251`
    > Never run chaos tests against production systems without proper safeguards. Use isolated environments with synthetic data and mock external 
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.3.html:131`
    > Research agents can produce plausible-sounding but incorrect analyses, especially when they hallucinate sources or misinterpret statistical 
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.4.html:415`
    > Agentic coding tools can introduce subtle security vulnerabilities that pass tests but create real risks. Common examples include: SQL injec
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:205`  *(canonical)*
    > Experiments show that LLMs correctly use information placed at position 1 or position 20 in a list of 20 documents roughly 80% of the time, 
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html:532`
    > Agentic RAG introduces new failure modes beyond those of naive RAG. Query drift occurs when follow-up queries gradually shift away from the 
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html:291`
    > Allowing an LLM to generate and execute SQL queries introduces serious security risks. Always enforce these safeguards: (1) use a read-only 
  - `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html:173`
    > LLMs can hallucinate entities that do not appear in the source text. Always implement a grounding check that verifies extracted entities aga
  - `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.4.html:64`
    > Never store LLM-extracted entities at the same confidence level as classical entities unless they pass grounding verification. Downstream co
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html:416`
    > Multi-modal RAG introduces several unique challenges: (1) embedding images and text into a shared vector space is still an active research a
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html:375`
    > GraphRAG's indexing phase is significantly more expensive than standard RAG because it requires LLM calls for every chunk (entity extraction
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html:637`
    > Be cautious about deep framework coupling. If you use LangChain's custom prompt classes, LlamaIndex's specialized node postprocessors, and f
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html:637`
    > Every external data connection in your RAG pipeline is an entry point for adversarial content. A web crawler, a customer-facing upload endpo
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.5.html:345`
    > Memory consolidation that aggressively prunes or overwrites can lose information the user considers important. Always err on the side of kee
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html:407`
    > Voice activity detection (VAD) tuning is highly environment-dependent. A silence threshold that works well in a quiet office may cause const
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html:526`
    > A mean kappa of 0.67 indicates "good" agreement, but the wide range (0.57 to 0.81) across annotator pairs suggests that annotator C may be i
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.10.html:169`
    > Contamination is pervasive and often undetectable. Large-scale web crawls used for pretraining ingest benchmark datasets that were posted on
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.9.html:379`
    > Recording full prompt and completion content in traces creates significant privacy and compliance risks . User messages may contain personal
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html:150`
    > MLflow's legacy stage transitions ( Staging , Production , Archived ) are deprecated as of MLflow 2.9 and will be removed in a future releas
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.2.html:326`
    > Drift detection on LLM quality metrics is noisier than on traditional ML metrics because quality scores from judge models are themselves imp
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.4.html:58`
    > Distilled judges inherit the biases of their teacher. Because JudgeLM (and similar distilled judges) are trained on GPT-4's judgments, they 
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 4. CALLOUT TITLE (same title)  |  74 sections
- **Key/signature**: `see also`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html:761`
    > For how KV cache memory savings flow into production serving, see Section 9.2 (KV Cache and GQA in Practice). For how attention variants app
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html:605`
    > For the inference-time consequences of these architectural choices, see Section 9.2 (KV Cache and GQA). For how modern open-weight models co
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html:1078`
    > For fine-tuning techniques that defenders use to harden models, see Section 17.5 . For prompt engineering patterns that mitigate injection, 
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.2.html:696`
    > For production engineering controls that limit blast radius, see Section 62.1 . For agent design choices that affect attack surface, see Sec
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.1.html:69`
    > The deep treatment of hallucination as a model failure lives in Section 32.1 . The discussion below focuses on hallucination as an agent fai
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.5.html:483`
    > For the scaling-law context behind capability emergence, see Section 6.3 . For adversarial security threats that compound autonomy risk, see
  - `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html:745`
    > For PEFT methods that cut training compute drastically, see Section 17.5 . For inference-side optimizations (KV cache, quantization) that lo
  - `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.2.html:71`
    > The deep treatment of the underlying hallucination mechanism lives in Section 32.1 . The discussion below focuses on production-side detecti
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.14.html:637`
    > For the earlier ideation stages this builds on, see Section 67.12 . For prompt engineering techniques that ground product concepts in feasib
  - `part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.1.html:124`
    > For advanced RAG patterns used in legal retrieval, see Section 35.2 . For RAG fundamentals these legal pipelines build on, see Chapter 32 . 
  - `part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.1.html:78`
    > Chapter 32 (Retrieval-Augmented Generation) for the grounded-retrieval pattern that underpins biomedical literature synthesis and clinical-d
  - `part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.2.html:79`
    > Section 50.1 (Privacy Attacks) for the membership-inference and extraction mechanics that make PHI fine-tuning risky. Chapter 50 (Privacy an
  - `part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.3.html:71`
    > Chapter 53 (Regulation and Compliance) for the cross-cutting regulatory framing across LLM verticals. Section 53.4 (Licensing, IP, and Priva
  - `part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.4.html:117`
    > Chapter 59 (Distributed Training Systems) for the GPU-cluster economics underlying the on-premises pattern. Chapter 62 (Production Engineeri
  - `part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.5.html:86`
    > Section 72.5 (Legal LLM Vendors) for the parallel vendor consolidation pattern in the legal vertical. Section 73.5 (Finance LLM Vendors) for
  - `part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.1.html:78`
    > Chapter 32 (Retrieval-Augmented Generation) for the domain-bounded retrieval pattern that distinguishes a tutor from a homework-doer. Chapte
  - `part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.2.html:85`
    > Section 50.1 (Privacy Attacks) for the membership-inference threats that FERPA-protected fine-tuning must guard against. Chapter 54 (Bias an
  - `part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.3.html:69`
    > Section 53.4 (Licensing, IP, Privacy) for the BAA and data-handling-agreement structure that operationalizes FERPA. Chapter 53 (Regulation a
  - `part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.4.html:124`
    > Chapter 32 (Retrieval-Augmented Generation) for the domain-bounded retrieval architecture (Layer 1). Chapter 13 (Prompt Design) for the syst
  - `part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.5.html:85`
    > Section 74.5 (Healthcare LLM Vendors) for the parallel vendor consolidation pattern in the healthcare vertical. Section 72.5 (Legal LLM Vend
  - `part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.1.html:80`
    > Chapter 47 (Adversarial Security and Red Team) for the broader red-team and threat-modeling framework that this chapter's blue-team applicat
  - `part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.2.html:70`
    > Chapter 47 (Adversarial Security and Red Team) for the offensive-testing methodology that produces CyberSecEval-style numbers. Chapter 48 (L
  - `part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.3.html:82`
    > Section 50.1 (Privacy Attacks) for the membership-inference and extraction mechanics in detail. Section 49.1 (Agent Safety) for the agent-sp
  - `part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.4.html:124`
    > Section 49.1 (Agent Safety) for the agent-architecture safety patterns that operationalize Layers 3 and 4. Section 44.3 (Observability) for 
  - `part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.5.html:84`
    > Section 74.5 (Healthcare LLM Vendors) for the parallel platform-incumbent consolidation pattern (Abridge, Dragon Copilot) in healthcare. Sec
  - `part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.1.html:80`
    > Chapter 32 (Retrieval-Augmented Generation) for the grounded-retrieval pattern that underpins constituent-service and FOIA-triage deployment
  - `part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.2.html:88`
    > Chapter 54 (Bias and Fairness) for the disparate-impact methodology used in public-sector AI audits. Chapter 53 (Regulation and Compliance) 
  - `part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.3.html:81`
    > Chapter 53 (Regulation and Compliance) for the broader cross-cutting compliance methodology. Section 74.3 (Healthcare Regulatory Framework) 
  - `part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.4.html:118`
    > Chapter 32 (Retrieval-Augmented Generation) for the strict-scope retrieval architecture (Layer 1). Chapter 13 (Prompt Design) for the system
  - `part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.5.html:89`
    > Section 74.5 (Healthcare LLM Vendors) for the parallel platform-incumbent consolidation pattern (Abridge, Dragon Copilot) in healthcare. Sec
  - `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.2.html:265`
    > For the scaling-law context shaping frontier architecture choices, see Section 6.3 . For synthetic-data pipelines used to train these archit
  - `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.3.html:712`
    > For the sequence-model and attention foundations these architectures extend, see Section 2.2 and Section 3.1 . For inference-side optimizati
  - `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.2.html:332`
    > For the conversational-AI applications these theoretical results inform, see Chapter 37 . For RAG architectures that the theory analyzes, se
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html:438`
    > For the transformer block whose parameters dominate the count, see Section 3.1 . For how alignment changes the effective capability per para
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html:660`
    > For decoding strategies that shape the model output once trained, see Section 4.1 . For inference-side optimizations that ride on these trai
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html:554`
    > For fine-tuning techniques that build on pretrained checkpoints, see Section 16.4 . For inference-side cost-benefit consequences of scale ch
  - `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html:768`
    > For the attention variants that distinguish architectures (MHA, MQA, GQA), see Section 3.3 . For inference performance characteristics of th
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html:603`
    > For the train-time scaling baseline this section compares against, see Section 6.3 (Kaplan and Chinchilla scaling laws). For the specific re
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html:61`
    > The reasoning-model training pipeline (RLVR with verifier rewards) is treated from the alignment angle in Section 18.4: RLVR , and from the 
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html:464`
    > For evaluation methodology used to measure reasoning quality, see Chapter 42 . For prompting techniques that elicit reasoning from non-reaso
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html:78`
    > The decision to quantize is rarely purely technical. For the cost/quality tradeoff framed as a build-vs-buy decision (self-host quantized vs
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html:65`
    > For GPU memory calculations, bandwidth analysis, and hardware selection guidance, see Section 9.5 (Hardware Requirements).
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html:563`
    > For how speculative decoding and other inference optimizations apply across architectures, see Section 7.2 . For quantization and KV cache t
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html:65`
    > For a hands-on tutorial deploying models with vLLM, TGI, and SGLang, see Appendix K: Inference Serving .
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html:364`
    > For the quantization and serving foundations these benchmarks depend on, see Section 9.1 . For how architectural differences across model fa
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.6.html:332`
    > For pretraining-side scaling decisions that constrain inference, see Section 6.2 . For prompt engineering that shapes throughput per query, 
  - `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:57`
    > For the agent-loop view of function calling (how providers expose tool schemas and how the model selects them inside a multi-step loop), see
  - `part-3-working-with-llms/module-11-llm-apis/section-11.2.html:72`
    > The deep treatment of the function-calling loop lives in Section 27.1 . The discussion below focuses on the JSON-schema mechanics that provi
  - `part-3-working-with-llms/module-11-llm-apis/section-11.4.html:633`
    > For the decoding strategies these APIs surface as parameters, see Chapter 4 . For prompt structures that shape API request payloads, see Sec
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html:66`
    > The deep treatment of the prompt-vs-RAG-vs-fine-tune decision framework lives in Section 16.1: When and Why to Fine-Tune . The discussion be
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html:498`
    > The deep treatment of the ReAct (perception--reasoning--action) loop lives in Section 26.1 . The discussion below focuses on how ReAct shows
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html:59`
    > Automated prompt optimization (DSPy, MIPRO) is only useful if the eval signal driving it is reliable. For the eval-as-CI gate that should si
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html:499`
    > For the deep dive into the embedding-and-vector-database stack that the LLM-as-feature-extractor pattern reuses, see Section 31.1: Embedding
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html:363`
    > The full SemanticCache implementation (exact-match + cosine similarity lookup, TTL expiration, hit/miss statistics) is in Section 11.3: API 
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html:54`
    > For a hands-on tutorial on fine-tuning with the Hugging Face Trainer API and ecosystem tools, see HuggingFace: Transformers, Datasets, and H
  - `part-4-training-adaptation/module-17-peft/section-17.1.html:57`
    > For a hands-on walkthrough of LoRA and PEFT using Hugging Face libraries, see HuggingFace: Transformers, Datasets, and Hub .
  - `part-4-training-adaptation/module-17-peft/section-17.1.html:57`
    > LoRA is most commonly used as the parameter-efficient backbone of preference fine-tuning (DPO, ORPO, IPO). For the preference-optimization s
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html:807`
    > For evaluation methodology used to measure alignment quality, see Section 42.1 . For DPO and other preference-optimization variants, see Sec
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html:244`
    > For interpretability methods that diagnose alignment failures, see Chapter 10 . For mechanistic interpretability case studies on aligned mod
  - `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:60`
    > The same agent loop seen from the safety side (prompt injection, tool-call authorization, sandboxing) is the subject of Section 49.1: Agent 
  - `part-6-agentic-ai/module-26-ai-agents/section-26.3.html:57`
    > The deep treatment of how reasoning models work internally lives in Chapter 8 . The discussion below focuses on how to configure them inside
  - `part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html:73`
    > The deep treatment of the agent loop lives in Section 26.1 . The discussion below focuses on the tool-call slot specifically.
  - `part-6-agentic-ai/module-28-multi-agent-systems/section-28.1.html:60`
    > For a hands-on LangChain and LangGraph tutorial with runnable examples, see Appendix J: LangChain .
  - `part-6-agentic-ai/module-28-multi-agent-systems/section-28.1.html:60`
    > The deep treatment of the single-agent loop lives in Section 26.1 . The discussion below focuses on how that loop scales across agents.
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html:325`
    > For the general agent foundations these specialized agents extend, see Section 26.1 . For agent safety considerations specific to autonomy, 
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.4.html:488`
    > For the broader agent architecture this specialized agent inherits from, see Section 26.4 . For tool-use protocols and function calling, see
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html:193`  *(canonical)*
    > For why embeddings concentrate in a thin shell of high-dimensional space (concentration of measure) and what that means for cosine similarit
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:52`
    > For framework-level RAG pipelines (LangChain, LlamaIndex), see Section 36.2 .
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:52`
    > For the evaluation methodology of RAG specifically (faithfulness vs answer relevance, golden-set construction, retrieval@k vs end-to-end met
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:52`
    > The deep treatment of the prompt-vs-RAG-vs-fine-tune decision tree lives in Section 16.1 . The discussion below focuses on what changes when
  - `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.1.html:213`
    > For vision-language model foundations these multimodal retrievers build on, see Chapter 22 . For text-only RAG architectures and embedding s
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html:536`
    > For embedding model selection that feeds the retrieval pipeline, see Section 31.2 . For vector store and indexing trade-offs, see Section 31
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.1.html:56`
    > The deep treatment of the perception--reasoning--action loop lives in Section 26.1 . The discussion below focuses on the dialogue framing.
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html:370`
    > For fine-tuning techniques used to specialize conversational models, see Section 16.7 . For RAG integration in conversational systems, see S
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html:319`
    > Chapter 62 (Production Engineering) for the conceptual lifecycle framing. Section 19.2 (Libraries & Frameworks) for the upstream side: MLflo
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html:110`
    > Chapter 42 (Evaluation and Observability) for the conceptual framing and offline-eval pipeline. Section 19.2 (Libraries & Frameworks) for of
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html:110`
    > Chapter 42 (Evaluation and Observability) for the underlying eval methodology. Section 19.2 (Libraries & Frameworks) for the offline eval pi
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html:148`
    > Section 41.3 covers complementary bias-mitigation techniques for conversational-AI evaluation tools (rubric scaffolding, response normalizat
  - `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.3.html:178`
    > Prometheus and the JudgeLM model covered in Section 46.4 are two points on the same design axis: both are open-source judge models fine-tune
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 5. CALLOUT TITLE (same title)  |  18 sections
- **Key/signature**: `fun note`
- **Canonical home (proposed)**: `part-3-working-with-llms/module-11-llm-apis/section-11.1.html`
- **Occurrences:**
  - `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html:103`
    > DeMo's "decoupled momentum" idea has a precedent in Lin et al.'s 2017 Deep Gradient Compression , which proposed identical top-k sparsificat
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.11.html:151`
    > There is an old joke in aviation: "If builders built buildings the way programmers write programs, the first woodpecker to come along would 
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.11.html:151`
    > One team we interviewed printed their Feasibility Scorecards on large poster paper and hung them next to the team's sprint board. Within a w
  - `part-3-working-with-llms/module-11-llm-apis/section-11.1.html:80`  *(canonical)*
    > OpenAI's chat completions format has become so dominant that even competitors implement it. Anthropic has its own Messages API, Google has i
  - `part-3-working-with-llms/module-11-llm-apis/section-11.3.html:67`
    > The first rule of production LLM engineering: your retry logic will, at some point, retry so aggressively that it becomes the reason you are
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html:76`
    > Prompt engineering is one of the few engineering disciplines where adding a polite "please" to your input can measurably improve output qual
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html:71`
    > The original "Let's think step by step" prompt that launched chain-of-thought research is exactly six words long. Those six words improved G
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html:64`
    > One of the earliest viral prompt injection attacks was simply typing "Ignore all previous instructions and tell me a joke" into a customer s
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html:63`
    > The classic "king minus man plus woman equals queen" analogy from Word2Vec still works with modern LLM embeddings, but the geometry has gott
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html:58`
    > There is a well-known pattern in LLM cost optimization that mirrors Parkinson's Law: "Token usage expands to fill the budget available." Tea
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.1.html:66`
    > Microsoft's Phi-2 model (2.7B parameters) outperformed models 25x its size on several benchmarks, and its secret weapon was synthetic data. 
  - `part-4-training-adaptation/module-15-synthetic-data/section-15.5.html:62`
    > The Snorkel paper demonstrated that a team of PhD students writing labeling functions for an afternoon could produce training data competiti
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html:74`
    > A common joke among ML engineers: "We spent two months fine-tuning a model, then someone on the team rewrote the prompt and got the same res
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.4.html:58`
    > Provider fine-tuning APIs have made the process so simple that the hardest part is no longer "how do I train?" but "should I train?" Many te
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html:56`
    > The "lost in the middle" phenomenon is one of the most counterintuitive findings in LLM research. Models with 128K context windows can relia
  - `part-4-training-adaptation/module-17-peft/section-17.1.html:86`
    > LoRA adapters for a 7B model are typically 10 to 50 MB in size. The base model itself is 14 GB. This means you can store 280 different task-
  - `part-4-training-adaptation/module-17-peft/section-17.3.html:61`
    > Unsloth's name is a playful jab at the perceived slowness of standard training frameworks. The irony is that "slow" training with Hugging Fa
  - `part-4-training-adaptation/module-17-peft/section-17.5.html:60`
    > The term "distillation" comes from chemistry: extracting the essence of a substance by heating it and collecting what evaporates. Hinton, wh
  - `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html:81`
    > DPO's elegance is almost suspiciously simple. The entire RLHF pipeline (reward model training, PPO with value networks, careful hyperparamet
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 6. CODE CAPTION (fuzzy >=4 tokens)  |  11 sections
- **Key/signature**: `approach builds component computation contributes`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html:281` [Code Fragment 1.2.3]
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:268` [Code Fragment 1.7.3]
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html:484` [Code Fragment 3.3.3]
    > This snippet demonstrates the diff_attention function using attention computation. Notice how the attention weights are computed and applied to the value vectors. Tracing through each step builds the 
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html:360` [Code Fragment 4.2.4]
    > This snippet demonstrates the apply_repetition_penalty, apply_frequency_presence_penalty functions using PyTorch. Study the implementation details to understand how each component contributes to the o
  - `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:402` [Code Fragment 26.1.3]
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:272` [Code Fragment 32.1.1]  *(canonical)*
    > This snippet demonstrates the chunk_by_tokens, chunk_by_structure functions using chunking. Notice how the chunking strategy balances granularity with context preservation. Tracing through each step b
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html:197` [Code Fragment 32.3.2]
    > Extracting database schema context (table names, columns, types) and formatting it as a prompt section so the LLM can write accurate SQL. The function encapsulates reusable logic that can be applied a
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html:413` [Code Fragment 35.1.4]
    > This snippet demonstrates the rerank_results function using retrieval, API calls. Notice how the retrieval step filters candidates before passing them to downstream processing. Tracing through each st
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.1.html:718` [Code Fragment 37.1.5]
    > This snippet demonstrates the ConversationMode class and the classify_intent, handle_message functions using RAG, agent orchestration. Notice how the retrieval and generation stages are composed into 
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.2.html:664` [Code Fragment 42.2.6]
    > This snippet demonstrates the perturbation_contamination_test, evaluate_set functions using NumPy. Notice how the evaluation criteria are defined to measure quality along multiple dimensions. Understa
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.6.html:168` [Code Fragment 42.6.1]
    > This snippet demonstrates the rag_pipeline, retrieve_documents functions using retrieval, vector search. Notice how the retrieval and generation stages are composed into a single pipeline. Tracing thr
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 7. CODE CAPTION (fuzzy >=4 tokens)  |  10 sections
- **Key/signature**: `api contrasting decoding distinct face`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:611` [Code Fragment 4.4.7]  *(canonical)*
    > Running all five decoding strategies through Hugging Face's generate() API on the same prompt. Each strategy yields a distinct output style in a single line of code, contrasting with the roughly 60 li
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html:169` [Code Fragment 57.4.2]
    > AIPerf benchmarking across six concurrency levels (1 through 64). The --prompt-length-distribution and --completion-length-distribution flags generate normal-distributed token counts that match real-w
  - `part-14-designing-llm-agent-products/module-67-ideation/section-67.9.html:118` [Code Fragment 67.9.1]
    > Running the same prompt five times at temperature 0.7 typically yields multiple distinct (but semantically equivalent) responses, illustrating that LLM output is a distribution rather than a fixed val
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html:171` [Code Fragment 6.1.1]
    > GPT-2 performing zero-shot summarization by conditioning on a "TL;DR:" prompt. No fine-tuning is needed; the model leverages patterns learned during pre-training to generate a summary. This demonstrat
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html:97` [Code Fragment 8.5.1]
    > Two strategies consuming identical FLOPs. On hard reasoning problems, Strategy B (many samples plus a verifier) consistently outperforms Strategy A (single pass through a larger model).
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html:253` [Code Fragment 9.3.4]
    > Example 3: Speculative decoding with Hugging Face Transformers.
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html:220` [Code Fragment 12.1.4]
    > Layered system prompt architecture for a medical coding assistant. The prompt is organized into five distinct sections (Role, Task, Constraints, Output Format, Examples) that enforce ICD-10 classifica
  - `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.1.html:118` [Code Fragment 21.1.1]
    > Single-line TrOCR inference with beam search (num_beams=4). Float16 weights halve VRAM use to roughly 1.1 GB; the same call without torch_dtype consumes about 2.2 GB. Beam search adds 20-25% latency o
  - `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html:173` [Code Fragment 22.3.1]
    > Running LLaVA-NeXT-Mistral-7B on a chart-summarization task. The apply_chat_template helper handles model-specific prompt formatting; do_sample=False gives deterministic output for production. VRAM fo
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html:81` [Code Fragment 44.3.1]
    > A single Traceloop.init(app_name=...) call wires the standard GenAI semantic-convention attributes (model, input/output tokens, finish reason, prompt and completion bodies) into every subsequent OpenA
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 8. CODE CAPTION (fuzzy >=4 tokens)  |  9 sections
- **Key/signature**: `4x4 action actions agent chooses`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html:263` [Code Fragment 0.4.1]  *(canonical)*
    > A minimal RL environment (Grid World). The SimpleGridWorld class implements a 4x4 grid where an agent navigates toward a goal using discrete actions. This environment mirrors how LLM token generation 
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html:260` [Code Fragment 4.1.3]
    > Pseudocode for beam search decoding. At each step the algorithm expands the top k hypotheses, scores all candidates by cumulative log-probability, prunes back to k, and finally selects the highest-sco
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.1.html:137` [Code Fragment 49.1.1]
    > This snippet defines a SecureAgentExecutor that wraps an agent with a policy engine, validating each proposed tool call against allowed actions and parameter constraints before execution. The execute 
  - `part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html:571` [Code Fragment 64.1.6]
    > The saga (compensation) pattern in a Temporal workflow. Each booking step registers an undo action. If a later step fails, compensations run in reverse: the hotel is cancelled before the flight. The L
  - `part-5-multimodal-llms/module-24-vla-models/section-24.1.html:144` [Code Fragment 24.1.2]
    > One control step. The logit mask on each iteration restricts decoding to the slice for the current DOF, so the policy cannot accidentally emit a text token while sampling motor commands. This is the c
  - `part-5-multimodal-llms/module-24-vla-models/section-24.11.html:189` [Code Fragment 24.11.4]
    > The start/status/cancel triplet for long-running actions. The LLM uses these three tools in a loop: start the action, poll status until succeeded or failed, optionally cancel if the user issues a new 
  - `part-5-multimodal-llms/module-24-vla-models/section-24.3.html:181` [Code Fragment 24.3.2]
    > Calling pi-0-fast through OpenPI. The 50-step action chunk at 50 Hz covers one second of motion; re-querying every 200 ms (10 actions) gives the receding-horizon behavior from Section 24.1 . JAX rathe
  - `part-6-agentic-ai/module-26-ai-agents/section-26.3.html:280` [Code Fragment 26.3.5]
    > This lab step implements parse_agent_output (regex extraction of Action/Action Input fields) and tests the agent on three queries of increasing complexity: a single-tool weather lookup, a two-step sea
  - `part-6-agentic-ai/module-26-ai-agents/section-26.3.html:414` [Code Fragment 26.3.7]
    > The complete ReAct agent loop. Each iteration calls the LLM, parses the output to detect tool calls or a final answer, dispatches the selected tool, and appends the observation to the conversation his
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.9.html:243` [Code Fragment 42.9.3]
    > Hierarchical tracing for a RAG pipeline. Each step (embedding, vector search, reranking, generation) is a child span under the parent rag.pipeline span. The traced_chat_completion function from Code F
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 9. CODE CAPTION (fuzzy >=4 tokens)  |  8 sections
- **Key/signature**: `100 10k 200ms cent classification`
- **Canonical home (proposed)**: `part-3-working-with-llms/module-11-llm-apis/section-11.2.html`
- **Occurrences:**
  - `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.2.html:179` [Code Fragment 48.2.3]
    > LLM-as-judge topic classification using a small (~8B-parameter) instruct model with structured output. Latency is ~100-200ms; cost is well under a tenth of a cent per request. For higher-throughput pi
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.3.html:132` [Code Fragment 50.1.1]
    > Federated LoRA fine-tuning. Each client trains only the adapter matrices locally, and the server aggregates them via weighted averaging. Communication cost per round is proportional to adapter size (e
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.1.html:160` [Code Fragment 70.1.1]
    > Token cost calculator that models per-request and monthly costs across three model tiers, accounting for prompt caching. Adjust the UsageProfile parameters to match your product's actual token footpri
  - `part-3-working-with-llms/module-11-llm-apis/section-11.2.html:206` [Code Fragment 11.2.3]  *(canonical)*
    > Set up structured output extraction from the LLM
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html:60` [Code Fragment 13.3.1]
    > Use a small LLM to classify request difficulty and select a model tier
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html:325` [Code Fragment 13.3.3]
    > Use a small LLM to classify request difficulty and select a model tier
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html:344` [Code Fragment 13.5.4]
    > Extracting tool-use training examples from production traces. The function captures the user query, the tool call the model made (function name and arguments), the tool response, and the model's final
  - `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.5.html:107` [Code Fragment 23.5.1]
    > IC-Light per-view relighting. To extend to a 3D scene, one practical workflow is to render N views from the captured splat, run IC-Light per view to get relit renders, then fine-tune a new 3DGS scene 
  - `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.4.html:137` [Code Fragment 33.4.1]
    > Multimodal request observability skeleton. Per-stage timings, per-modality token counts, and pattern routing decisions are emitted with each request. Aggregated over a week, this log tells you where l
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 10. CODE CAPTION (fuzzy >=4 tokens)  |  8 sections
- **Key/signature**: `after block compilation compile compiled`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html:782` [Code Fragment 0.3.16]  *(canonical)*
    > Wrapping a Transformer block with torch.compile in reduce-overhead mode. The compiled model produces identical output but runs 1.3x to 2x faster after the one-time compilation cost.
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html:333` [Code Fragment 6.6.3]
    > Wrapping each transformer layer with torch.utils.checkpoint.checkpoint(..., use_reentrant=False) trades recompute for memory: the analysis at the bottom of the snippet shows a 32-layer model dropping 
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html:447` [Code Fragment 9.7.5]
    > torch.compile automatically fuses operations in a transformer block. The reduce-overhead mode minimizes kernel launch latency using CUDA graphs. Typical speedups range from 1.3x to 2x depending on the
  - `part-2-understanding-llms/module-10-interpretability/section-10.6.html`
    > Code Fragment k.1.3: Loading one model from each transformer family. BERT (encoder-only) produces hidden states for each token, GPT-2 (decoder-only) generates text autoregressively, and T5 (encoder-de
  - `part-5-multimodal-llms/module-20-audio-music-generation/section-20.4.html:85` [Code Fragment 20.4.1]
    > Four-stem separation with Demucs v4. The shifts=2 flag runs the model twice on time-shifted copies and averages the outputs, giving roughly a 0.3-0.5 dB SDR improvement at the cost of 2x latency. For 
  - `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.3.html:200` [Code Fragment 21.3.1]
    > Structured invoice extraction with GPT-4o using Pydantic schema. The response_format=Invoice argument enforces schema compliance via OpenAI's strict mode. Temperature 0 produces deterministic output a
  - `part-6-agentic-ai/module-26-ai-agents/section-26.4.html:212` [Code Fragment 26.4.3]
    > One row per task: pass/fail, input/output token counts, computed cost, and tool-call count. The cost formula (3 USD per million input, 15 per million output) is the Sonnet-class pricing baseline; swap
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html:472` [Code Fragment 40.1.5]
    > Production telephony voice agent deployment with LiveKit. The configuration uses telephony-optimized codecs (mu-law at 8kHz), faster endpointing for phone conversations, and a lower-latency LLM model.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 11. CODE CAPTION (fuzzy >=4 tokens)  |  7 sections
- **Key/signature**: `anthropic apis application block contract`
- **Canonical home (proposed)**: `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html`
- **Occurrences:**
  - `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.4.html:150` [Code Fragment 48.4.3]
    > A Pydantic safety contract. The structural part is enforced by Outlines / OpenAI / Anthropic structured-output APIs during decoding. The cross-field validator ( emergency_must_escalate ) enforces a po
  - `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.1.html:256` [Code Fragment 63.1.3]
    > Multi-provider fallback chain using LiteLLM Router. Three deployments share the same logical model name; the router tries them in order based on latency. If a request exceeds the context window, it au
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.3.html:442` [Code Fragment 70.3.1]
    > A provider abstraction layer with adapters for OpenAI and Anthropic. The LLMRequest and LLMResponse dataclasses define a provider-agnostic contract. Each adapter translates between this contract and t
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.3.html:631` [Code Fragment 70.3.3]
    > A rule-based model router with automatic fallback. Each RouteRule defines a condition function that examines the request and decides whether this rule applies. Rules are evaluated in priority order, a
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html:376` [Code Fragment 12.2.4]  *(canonical)*
    > a: outlines forces the model to emit text that parses into a Pydantic schema.
  - `part-5-multimodal-llms/module-24-vla-models/section-24.8.html:205` [Code Fragment 24.8.3]
    > The same plan as Code Fragment 24.8.1 , expressed as a structured tool-call sequence. The JSON form is what modern LLM APIs (OpenAI function calling, Anthropic tool use, Gemini tool definitions) nativ
  - `part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html:250` [Code Fragment 28.4.4]
    > The reference solution adds a country_code field with a regex pattern, uses response_format={"type": "json_object"} to force the model to emit valid JSON, and wraps validate_tool_call in a try / raise
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html:144` [Code Fragment 32.4.2]
    > Structured attribution using Pydantic models and OpenAI's structured output. Each claim carries a source ID and an exact supporting quote, enabling automated verification.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 12. CODE CAPTION (fuzzy >=4 tokens)  |  7 sections
- **Key/signature**: `allowed becomes categories compiles contain`
- **Canonical home (proposed)**: `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html`
- **Occurrences:**
  - `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.4.html:81` [Code Fragment 48.4.1]
    > Outlines compiles the Pydantic SafetyDecision model into a finite-state machine over the model's vocabulary. At every decoding step, only tokens that keep the partial output on a valid path through th
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.3.html:121` [Code Fragment 53.3.1]
    > A model inventory entry built on Pydantic for runtime validation, with the EU AI Act risk tier computed from use_case + data_sources rather than hand-set. The two demo entries differ only in their dat
  - `part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html:488` [Code Fragment 64.1.5]
    > Budget-aware retry with jittered exponential backoff. The function checks cumulative cost before each attempt, preventing runaway spend when partial failures consume tokens. Context window overflow is
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html:282` [Code Fragment 8.3.1]  *(canonical)*
    > Simplified PRM that scores each reasoning step. In practice, PRMs use the full hidden state of a large language model backbone, and step boundaries are identified by special delimiter tokens rather th
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html:400` [Code Fragment 13.5.5]
    > Enforcing data contracts with Pydantic schemas. Each dataset record is validated against a strict schema that checks field types, string length bounds, and enum values. Records that fail validation ar
  - `part-4-training-adaptation/module-17-peft/section-17.4.html:142` [Code Fragment 17.4.1]
    > Prompt Tuning with HuggingFace PEFT. The PromptTuningConfig prepends 20 learnable virtual tokens (initialized from a text string) to every input. Only these ~320 KB of soft prompt embeddings are train
  - `part-5-multimodal-llms/module-24-vla-models/section-24.6.html:113` [Code Fragment 24.6.1]
    > The three-layer safety stack that wraps every production VLA. The wrapper is the only piece between the model's prediction and the robot's motors. None of the three layers is learned; they are classic
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 13. CALLOUT TITLE (same title)  |  10 sections
- **Key/signature**: `tip: production alternative`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html:386`  *(canonical)*
    > The implementation above builds K-Fold cross-validation from scratch for pedagogical clarity. In production, use scikit-learn (install: pip 
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html:349`
    > The implementation above builds multi-head attention from scratch for pedagogical clarity. In production, use torch.nn.MultiheadAttention (b
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html:521`
    > The implementation above builds a complete decoder-only Transformer from scratch for pedagogical clarity. In production, use HuggingFace Tra
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html:261`
    > The greedy and beam search implementations above are built from scratch for pedagogical clarity. In production, use HuggingFace Transformers
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html:471`
    > The implementations above build temperature scaling, top-k, top-p, and repetition penalty from scratch for pedagogical clarity. In productio
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html:238`
    > The implementation above builds causal language modeling loss from scratch for pedagogical clarity. In production, use HuggingFace Transform
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:331`
    > The implementation above builds probing classifiers with a custom PyTorch training loop for pedagogical clarity. For quick probing experimen
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:334`
    > The implementation above builds a sparse autoencoder from scratch for pedagogical clarity. In production, use SAELens (install: pip install 
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:171`
    > The implementation above builds Integrated Gradients from scratch for pedagogical clarity. In production, use Captum (install: pip install c
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:201`
    > The implementation above builds attention rollout from scratch for pedagogical clarity. In production, use BertViz (install: pip install ber
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 14. CALLOUT TITLE (same title)  |  10 sections
- **Key/signature**: `warning: common misconception`
- **Canonical home (proposed)**: `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html:240`
    > Vanishing gradients do not mean the gradient is exactly zero. They mean the gradient signal from distant time steps is overwhelmed by the si
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.2.html:619`
    > Passing a red team assessment does not mean the model is safe. Red teaming can only find vulnerabilities that the testers think to look for.
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html:555`
    > Applying differential privacy to fine-tuning does not retroactively protect the pre-training data. If a base model was pre-trained without D
  - `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.3.html:253`
    > Federated learning does not guarantee privacy by default. While raw data stays local, the model updates (gradients) shared during federated 
  - `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.2.html:582`
    > Many teams assume the EU AI Act only applies to companies based in the EU. In reality, the Act applies to any provider that places an AI sys
  - `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html:662`
    > Readers often focus exclusively on training costs and overlook inference costs. While training a large model is energy-intensive, inference 
  - `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html:365`
    > Readers often conflate throughput (tokens per second for the system) with latency (time per token experienced by a single user). A system ca
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html:572`  *(canonical)*
    > Standard Kubernetes resource requests and limits are not sufficient for GPU workloads. Unlike CPU and memory, GPUs cannot be shared across p
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.6.html:465`
    > Adding tracing does not automatically make your system observable. Many teams instrument every LLM call but never build dashboards or set al
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.8.html:616`
    > Readers often assume that a model with a 128K context window can reliably use all 128K tokens. In practice, most models degrade significantl
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 15. CODE CAPTION (exact-fingerprint)  |  5 sections
- **Key/signature**: `install the required packages for this lab.`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html:519` [Code Fragment 1.4.7]  *(canonical)*
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:775` [Code Fragment 1.7.15]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html:809` [Code Fragment 2.3.14]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html:446` [Code Fragment 3.5.5]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:455` [Code Fragment 4.4.9]
    > Install the required packages for this lab.
- **Suggested action**: **DELETE** duplicate code fragment; cross-ref to canonical Code Fragment. Two sections shipping the same example causes maintenance drift.

### 16. CODE CAPTION (exact-fingerprint)  |  5 sections
- **Key/signature**: `code example`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`
- **Occurrences:**
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html:837` [Code Fragment 31.1.8]  *(canonical)*
    > Code example
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:825` [Code Fragment 32.1.7]
    > Code example
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:978` [Code Fragment 32.1.11]
    > Code example
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html:307` [Code Fragment 35.5.2]
    > Code example
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html:406` [Code Fragment 35.5.3]
    > Code example
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.6.html:456` [Code Fragment 40.1.9]
    > Code example
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html:333` [Code Fragment 42.1.2]
    > Code example
- **Suggested action**: **DELETE** duplicate code fragment; cross-ref to canonical Code Fragment. Two sections shipping the same example causes maintenance drift.

### 17. CALLOUT TITLE (same title)  |  9 sections
- **Key/signature**: `note: modify and observe`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html:310`  *(canonical)*
    > Change the target action from 2 to 0. Does the policy learn equally fast? Reduce the learning rate to 1e-4 . How many episodes does it take 
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html:420`
    > Add a fourth document that repeats many words from documents 1 and 2. How do the TF-IDF weights change for shared words? Try TfidfVectorizer
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html:386`
    > Try the analogy wv.most_similar(positive=['doctor', 'woman'], negative=['man']) . Does the result reflect real-world knowledge or social bia
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html:407`
    > Change hidden_size from 256 to 64. How do the parameter counts scale? Does the ratio between RNN, LSTM, and GRU stay the same? In the vanish
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html:476`
    > Change the temperature from 0.5 to 0.01. How many "active tokens" effectively remain? What happens to the entropy? Try combining top-k=10 wi
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html:504`
    > Download a GGUF model from Hugging Face (search for "TheBloke" or "bartowski" for curated quantizations). Try running it with Ollama: ollama
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html:381`
    > Try changing gamma from 2 to 8 and observe how the acceptance rate changes. With a closer draft/target pair, higher gamma values produce mor
  - `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html:728`
    > Experiment with the CoT examples from this section:
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html:398`
    > Experiment with the classification benchmark from this section:
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 18. CALLOUT TITLE (same title)  |  9 sections
- **Key/signature**: `note: learning objectives`
- **Canonical home (proposed)**: `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.1.html`
- **Occurrences:**
  - `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.1.html:44`  *(canonical)*
    > Distinguish the five 2026 inference-silicon families (NVIDIA Blackwell, Cerebras CS-3, Groq LPU/LPX, Tenstorrent, AMD MI355X, AWS Trainium) 
  - `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html:44`
    > Explain why synchronous data-parallel training requires hyperscaler-class interconnect, and what specifically DeMo compresses to break that 
  - `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.3.html:40`
    > Compare the three edge-runtime stacks (MLX, llama.cpp, vendor NPU SDKs) by target hardware and quantization support. Explain why unified mem
  - `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.4.html:40`
    > Trace the four FlashAttention versions to the NVIDIA SM generations they target (A100, H100, H100+FP8, Blackwell). Explain what "asymmetric 
  - `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.5.html:40`
    > Explain why inference-aware scaling shifts the optimum toward smaller models trained on more tokens. Walk through the training-versus-infere
  - `part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.1.html:40`
    > Distinguish the three frontier-2026 benchmarks (HLE, ARC-AGI-2/3, FrontierMath) by what they measure and which they discriminate. Read cost-
  - `part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.2.html:40`
    > Distinguish weak-to-strong, Constitutional AI / C3AI, RLHF, DPO/GRPO, and SAE feature-steering as frontier-scale alignment approaches. Read 
  - `part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.3.html:40`
    > Position the major 2026 timeline forecasters (Amodei, Hassabis, Metaculus, Polymarket, 80,000 Hours) on a common axis. Recognize the "defini
  - `part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/section-82.4.html:40`
    > Read 2025-26 labor-market data sources (Anthropic study, WEF Future of Jobs, BLS, AI Skills Shift) by sample, scope, and measurement caveat.
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 19. CODE CAPTION (fuzzy >=4 tokens)  |  6 sections
- **Key/signature**: `install lab packages required`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html:519` [Code Fragment 1.4.7]  *(canonical)*
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:775` [Code Fragment 1.7.15]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html:809` [Code Fragment 2.3.14]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html:446` [Code Fragment 3.5.5]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:455` [Code Fragment 4.4.9]
    > Install the required packages for this lab.
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:568` [Code Fragment 10.1.13]
    > The following cell installs the required packages and configures the environment for this lab.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 20. CODE CAPTION (fuzzy >=4 tokens)  |  6 sections
- **Key/signature**: `builds clarity complete decoder implementation`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html:531` [Code Fragment 3.2.11]  *(canonical)*
    > The implementation above builds a complete decoder-only Transformer from scratch for pedagogical clarity.
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html:248` [Code Fragment 6.2.6]
    > The implementation above builds causal language modeling loss from scratch for pedagogical clarity.
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:362` [Code Fragment 10.1.12]
    > The implementation above builds probing classifiers with a custom PyTorch training loop for pedagogical clarity.
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:344` [Code Fragment 10.2.10]
    > The implementation above builds a sparse autoencoder from scratch for pedagogical clarity.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:181` [Code Fragment 10.3.8]
    > The implementation above builds Integrated Gradients from scratch for pedagogical clarity.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:212` [Code Fragment 10.4.12]
    > The implementation above builds attention rollout from scratch for pedagogical clarity.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 21. CODE CAPTION (fuzzy >=4 tokens)  |  4 sections
- **Key/signature**: `automatically converting handles ids input`
- **Canonical home (proposed)**: `part-2-understanding-llms/module-10-interpretability/section-10.1.html`
- **Occurrences:**
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:491` [Code Fragment 10.1.6]  *(canonical)*
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:145` [Code Fragment 10.2.1]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:227` [Code Fragment 10.3.3]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:273` [Code Fragment 10.3.4]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:414` [Code Fragment 10.3.5]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:86` [Code Fragment 10.4.1]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:246` [Code Fragment 10.4.3]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:333` [Code Fragment 10.4.4]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:397` [Code Fragment 10.4.5]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:492` [Code Fragment 10.4.6]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 22. CALLOUT TITLE (same title)  |  8 sections
- **Key/signature**: `practical example`
- **Canonical home (proposed)**: `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.1.html`
- **Occurrences:**
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.1.html:233`  *(canonical)*
    > A common pattern for LLM projects is to create a named volume for the HuggingFace cache directory ( ~/.cache/huggingface ). This way, model 
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.2.html:325`
    > Never bake API keys or tokens into a Dockerfile with ENV . Anyone who pulls your image can read those values with docker inspect . Instead, 
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.3.html:334`
    > For multi-environment setups, maintain separate files like .env.dev , .env.staging , and .env.prod . Launch with a specific environment by p
  - `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html:254`
    > A 70B parameter model in float16 requires approximately 140 GB of VRAM, which means at least two A100-80GB GPUs. With GPTQ 4-bit quantizatio
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html:99`
    > Llama 3 .1 405B Training Configuration. Meta's Llama 3.1 405B was trained on 16,384 H100 GPUs using TP=8, PP=16, DP=128 (approximately). Eac
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html:99`
    > FP8 training throughput gains. When training a Llama-3.1-8B model on a single DGX H100 node (8 GPUs), switching from BF16 to FP8 with Transf
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html:99`
    > Checkpoint strategy for a 70B pretraining run. A team training a 70B model on 512 H100 GPUs with an MTBF of approximately 2,000 iterations (
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html:273`
    > Consider a startup deploying a 7B-parameter model for customer support on a single NVIDIA A100 GPU. The dense FP16 model requires 14 GB and 
  - `part-2-understanding-llms/module-10-interpretability/section-10.6.html:498`
    > Streaming is also supported. Replace client.chat.completions.create(...) with client.chat.completions.create(..., stream=True) and iterate o
  - `part-2-understanding-llms/module-10-interpretability/section-10.6.html:498`
    > Consider a customer support chatbot that includes a 500-token system prompt with company policies and 5 few-shot examples. Without RadixAtte
  - `part-2-understanding-llms/module-10-interpretability/section-10.8.html:266`
    > A common production pattern is to maintain two quantized versions of the same model: an AWQ version for your GPU-based serving cluster (usin
- **Suggested action**: **RESTRUCTURE**: same title used for different bodies. Either rename titles to distinguish (preferred) or merge into a single canonical callout if the message is the same.

### 23. CODE CAPTION (fuzzy >=4 tokens)  |  5 sections
- **Key/signature**: `actions adversarial baseline before domain`
- **Canonical home (proposed)**: `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.3.html`
- **Occurrences:**
  - `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.2.html:543` [Code Fragment 49.8.3]
    > a: A GitHub Actions workflow that runs LLM security testing on every pull request that modifies prompts, tools, retrieval pipelines, or guardrails. The three-stage scan (Garak baseline probes, domain-
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.3.html:450` [Code Fragment 49.3.5]
    > A least-privilege decorator constraining each tool to specific operations, maximum data sizes, blocked destinations, and financial approval thresholds. An external policy engine validates every action
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.4.html:272` [Code Fragment 49.4.5]
    > GitHub Actions workflow that builds an agent-runner image with SLSA Level 3 provenance. The pipeline generates an SBOM (Syft via sbom-action), scans for vulnerabilities (Trivy), signs the image (Cosig
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.4.html:430` [Code Fragment 49.4.7]
    > Deployment verification script that checks the Cosign signature, verifies the SBOM attestation, and runs a fresh Trivy scan before allowing the agent-runner image into production. All three checks mus
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.3.html:581` [Code Fragment 42.3.5]  *(canonical)*
    > A promptfoo security configuration using red-team plugins for automated adversarial testing. Each plugin targets a specific OWASP LLM Top 10 vulnerability category.
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.2.html:212` [Code Fragment 44.2.3]
    > mlflow.evaluate() runs the OpenAI gpt-4 endpoint against three reference rows and returns both aggregate metrics ( rouge1/v1/mean ) and a per-row table. Adding mlflow.metrics.latency() and toxicity() 
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 24. CODE CAPTION (fuzzy >=4 tokens)  |  5 sections
- **Key/signature**: `activities activity after agent built`
- **Canonical home (proposed)**: `part-6-agentic-ai/module-26-ai-agents/section-26.3.html`
- **Occurrences:**
  - `part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html:205` [Code Fragment 64.1.1]
    > A durable research agent built with Temporal. The workflow orchestrates three phases (search, extract, summarize) as activities. If a worker crashes after step 2 completes, the replacement worker repl
  - `part-6-agentic-ai/module-26-ai-agents/section-26.3.html:231` [Code Fragment 26.3.3]  *(canonical)*
    > This lab step defines three simulated tools (calculator, weather, search) in a TOOLS registry mapping names to (function, description) pairs. The calculator uses a restricted eval with a character all
  - `part-6-agentic-ai/module-26-ai-agents/section-26.3.html:545` [Code Fragment 26.3.8]  *(canonical)*
    > End-to-end test suite for the ReAct agent. Three test cases exercise increasingly complex scenarios: a single tool call (weather lookup), a multi-step chain (search then calculate), and a multi-tool s
  - `part-6-agentic-ai/module-28-multi-agent-systems/section-28.1.html:157` [Code Fragment 28.1.2]
    > The same research workflow in CrewAI (Agent/Task/Crew abstractions with persona-driven behavior) and the OpenAI Agents SDK (composing search_agent and writer_agent into a pipeline where Runner.run man
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html:195` [Code Fragment 29.1.3]
    > Lab step (starter code) : implement the self-debugging retry loop that runs generated code, captures any error traceback on failure, and feeds it back to the agent for up to three correction attempts.
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.4.html:290` [Code Fragment 29.4.5]
    > Conceptual YAML representation of the Copilot Workspace issue-to-PR pipeline. The three stages (specification, plan, implementation) make the agent's reasoning transparent: the developer can review an
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 25. CODE CAPTION (fuzzy >=4 tokens)  |  5 sections
- **Key/signature**: `accuracy augmented baselines both compared`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html`
- **Occurrences:**
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html:157` [Code Fragment 8.6.2]
    > Simplified ReProver pipeline showing retrieval-augmented tactic generation. The retriever finds relevant premises from the full mathlib library using dense similarity search, then the tactic generator
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:426` [Code Fragment 10.1.5]
    > Embedding generation for converting text into dense vector representations. These vectors capture semantic meaning, enabling similarity search and clustering.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:71` [Code Fragment 10.3.2]
    > Embedding generation for converting text into dense vector representations. These vectors capture semantic meaning, enabling similarity search and clustering.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:519` [Code Fragment 10.3.6]
    > Embedding generation for converting text into dense vector representations. These vectors capture semantic meaning, enabling similarity search and clustering.
  - `part-4-training-adaptation/module-17-peft/section-17.3.html:179` [Code Fragment 17.3.4]
    > torchtune setup showing both CLI-based and programmatic LoRA fine-tuning. The library provides composable recipes that expose the full training loop, making it ideal for researchers who need to custom
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html:346` [Code Fragment 31.5.3]  *(canonical)*
    > Two-stage retrieval pipeline: fast BM25 /dense retrieval narrows candidates, then ColQwen2 rescores with full late interaction.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 26. CODE CAPTION (fuzzy >=4 tokens)  |  5 sections
- **Key/signature**: `approach attention behavior configuration enables`
- **Canonical home (proposed)**: `part-4-training-adaptation/module-17-peft/section-17.2.html`
- **Occurrences:**
  - `part-4-training-adaptation/module-17-peft/section-17.2.html:118` [Code Fragment 17.2.2]  *(canonical)*
    > Prefix Tuning configuration that prepends learnable virtual tokens to each softmax layer. The prefix_projection flag enables a small MLP that projects the prefix, improving training stability. This ap
  - `part-4-training-adaptation/module-17-peft/section-17.3.html:274` [Code Fragment 17.3.3]
    > LLaMA-Factory programmatic configuration for a QLoRA fine-tuning run. While most users configure runs through the web UI (LLaMA Board), this JSON config approach enables scripted automation and CI/CD 
  - `part-4-training-adaptation/module-17-peft/section-17.4.html:232` [Code Fragment 17.4.2]
    > Prefix Tuning with HuggingFace PEFT. Unlike Prompt Tuning, Prefix Tuning injects learned key-value pairs into every attention layer via a reparameterization MLP ( encoder_hidden_size=512 ). After trai
  - `part-4-training-adaptation/module-17-peft/section-17.4.html:354` [Code Fragment 17.4.4]
    > P-Tuning v2 for sequence classification with PEFT. Deep prefix tokens are injected at every layer ( num_layers defaults to the full model depth), and a classification head is trained alongside the sof
  - `part-4-training-adaptation/module-17-peft/section-17.6.html:298` [Code Fragment 17.6.3]
    > TIES merge YAML configuration for MergeKit. Each model specifies a density parameter (fraction of weight changes to keep) and a weight for its contribution. The normalize flag ensures merged weights m
  - `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.2.html:181` [Code Fragment 21.2.1]
    > Fine-tuning LayoutLMv3-Base on FUNSD. Total training time on a single RTX 4090: about 38 minutes for 15 epochs. The 0.906 F1 is within 1.5 points of the published LayoutLMv3-Large result and competiti
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 27. CODE CAPTION (exact-fingerprint)  |  4 sections
- **Key/signature**: `tokenization pipeline converting raw text into model-ready input ids. the tokeni`
- **Canonical home (proposed)**: `part-2-understanding-llms/module-10-interpretability/section-10.1.html`
- **Occurrences:**
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:491` [Code Fragment 10.1.6]  *(canonical)*
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:145` [Code Fragment 10.2.1]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:227` [Code Fragment 10.3.3]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:273` [Code Fragment 10.3.4]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:414` [Code Fragment 10.3.5]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:86` [Code Fragment 10.4.1]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:246` [Code Fragment 10.4.3]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:333` [Code Fragment 10.4.4]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:397` [Code Fragment 10.4.5]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:492` [Code Fragment 10.4.6]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
- **Suggested action**: **DELETE** duplicate code fragment; cross-ref to canonical Code Fragment. Two sections shipping the same example causes maintenance drift.

### 28. CODE CAPTION (fuzzy >=4 tokens)  |  5 sections
- **Key/signature**: `ahead array backward blocks building`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html:153` [Code Fragment 0.3.1]  *(canonical)*
    > Two building blocks side by side: creating tensors (from lists, factory functions, and NumPy) and running a full training loop (forward, loss, backward, step). Notice that torch.from_numpy shares memo
  - `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html:388` [Code Fragment 9.7.4]
    > Simplified FlashAttention forward pass in Triton. The key ideas are: Q tiles stay in SRAM while iterating over K/V tiles, the online softmax trick maintains running statistics, and the full N x N atte
  - `part-4-training-adaptation/module-17-peft/section-17.2.html:167` [Code Fragment 17.2.5]
    > GaLore conceptual implementation showing gradient projection via SVD. The projector periodically recomputes the low-rank subspace (every 200 steps by default), then projects gradients into this smalle
  - `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.1.html:133` [Code Fragment 23.1.1]
    > The reference 3DGS training loop. Three things matter: the L1 + SSIM photometric loss (with $\lambda = 0.2$), the differentiable rasterization step from gsplat (the BSD-licensed re-implementation by N
  - `part-5-multimodal-llms/module-24-vla-models/section-24.3.html:114` [Code Fragment 24.3.1]
    > A 30-line pi-0-style flow-matching action expert. Training is one MSE loss; inference is eight Euler steps. The contrast with the autoregressive token loop of OpenVLA is stark: instead of 7 transforme
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 29. CODE CAPTION (fuzzy >=4 tokens)  |  5 sections
- **Key/signature**: `apply autoregressive call context generate`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html:519` [Code Fragment 3.2.7]
    > Weight initialization ( _init_weights ) and autoregressive text generation ( generate ) for the mini-Transformer. Apply _init_weights via self.apply(self._init_weights) from __init__ ; call generate w
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:548` [Code Fragment 4.4.5]
    > A unified sampling function supporting temperature, top-k, and nucleus (top-p) filtering. Temperature reshapes the probability distribution, top-k restricts candidates to the k most likely tokens, and
  - `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html:225` [Code Fragment 6.9.3]
    > Generate text from the trained model using temperature sampling.
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html:670` [Code Fragment 8.6.8]
    > Nucleus (top-p) sampling with temperature scaling, keeping only the smallest set of tokens whose cumulative probability exceeds the threshold. Compared to greedy decoding, the three sample outputs are
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:433` [Code Fragment 32.1.4]  *(canonical)*
    > The three-step retrieve-augment-generate loop: ChromaDB collection.query returns the top-k chunks plus their metadata, the prompt template stitches them into a citable context block, and gpt-4o with t
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 30. PROSE PARAGRAPH  |  2 sections
- **Key/signature**: `the solution is to treat production evaluation as a continuous pipeline, not a gate you pass once. c`
- **Canonical home (proposed)**: `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html`
- **Occurrences:**
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.4.html:79`
    > The solution is to treat production evaluation as a continuous pipeline, not a gate you pass once. Chapter 44 covers the mechanics of building eval sets; this section focuses on keeping those evals al
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html:58`  *(canonical)*
    > The solution is to treat production evaluation as a continuous pipeline, not a gate you pass once. Chapter 42 covers the mechanics of building eval sets; the discipline added here is keeping those eva
- **Suggested action**: **DELETE** the redundant paragraph; replace with a 1-line summary plus a link to canonical.

## Sample Before/After Sketches (5)

### Sketch 1: `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html`

**Before** (verbatim duplicate of content already in canonical):
```html
<div class="callout big-picture">
  <div class="callout-title">(callout title)</div>
  <p>Every ML practitioner has experienced the five stages of overfitting grief: denial ("my 99% accuracy is real"), anger ("why does test accura</p>
</div>
```

**After** (replace with cross-ref to canonical `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`):
```html
<div class="callout cross-ref">
  <div class="callout-title">See Also</div>
  <p>This concept is treated in depth in 
    <a href="../../part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html">section-31.1</a>.
    The treatment there covers (...) at full depth; the brief mention 
    that previously lived here has been removed to avoid drift.</p>
</div>
```

### Sketch 2: `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html`

**Before** (verbatim duplicate of content already in canonical):
```html
<div class="callout big-picture">
  <div class="callout-title">(callout title)</div>
  <p>AutoML and neural architecture search (NAS) are reducing the need for manual feature engineering and model selection. Foundation models are </p>
</div>
```

**After** (replace with cross-ref to canonical `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`):
```html
<div class="callout cross-ref">
  <div class="callout-title">See Also</div>
  <p>This concept is treated in depth in 
    <a href="../../part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html">section-31.1</a>.
    The treatment there covers (...) at full depth; the brief mention 
    that previously lived here has been removed to avoid drift.</p>
</div>
```

### Sketch 3: `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html`

**Before** (verbatim duplicate of content already in canonical):
```html
<div class="callout big-picture">
  <div class="callout-title">(callout title)</div>
  <p>The learning rate is the single most important hyperparameter in optimization. Too large, and the steps overshoot the minimum, causing the l</p>
</div>
```

**After** (replace with cross-ref to canonical `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`):
```html
<div class="callout cross-ref">
  <div class="callout-title">See Also</div>
  <p>This concept is treated in depth in 
    <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html">section-32.1</a>.
    The treatment there covers (...) at full depth; the brief mention 
    that previously lived here has been removed to avoid drift.</p>
</div>
```

### Sketch 4: `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html`

**Before** (verbatim duplicate of content already in canonical):
```html
<div class="callout big-picture">
  <div class="callout-title">(callout title)</div>
  <p>For how KV cache memory savings flow into production serving, see Section 9.2 (KV Cache and GQA in Practice). For how attention variants app</p>
</div>
```

**After** (replace with cross-ref to canonical `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`):
```html
<div class="callout cross-ref">
  <div class="callout-title">See Also</div>
  <p>This concept is treated in depth in 
    <a href="../../part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html">section-31.1</a>.
    The treatment there covers (...) at full depth; the brief mention 
    that previously lived here has been removed to avoid drift.</p>
</div>
```

### Sketch 5: `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html`

**Before** (verbatim duplicate of content already in canonical):
```html
<div class="callout big-picture">
  <div class="callout-title">(callout title)</div>
  <p>DeMo's "decoupled momentum" idea has a precedent in Lin et al.'s 2017 Deep Gradient Compression , which proposed identical top-k sparsificat</p>
</div>
```

**After** (replace with cross-ref to canonical `part-3-working-with-llms/module-11-llm-apis/section-11.1.html`):
```html
<div class="callout cross-ref">
  <div class="callout-title">See Also</div>
  <p>This concept is treated in depth in 
    <a href="../../part-3-working-with-llms/module-11-llm-apis/section-11.1.html">section-11.1</a>.
    The treatment there covers (...) at full depth; the brief mention 
    that previously lived here has been removed to avoid drift.</p>
</div>
```
