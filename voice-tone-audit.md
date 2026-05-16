# Voice & Tone Consistency Audit

Scan root: `E:\Projects\BookBlogsHome\LLMBook`
Excluded dirs: .book-update, .claude, .git, KDP, _concept-figs, agents, build, downloads, images, node_modules, pagefind, scripts, source_fix_backups, styles, temp_ebook, temp_epub, templates, tmp_whats_next, vendor

## Summary
- Files scanned: 522
- Em-dash hits in prose: 7 (P0 - user banned)
- Double-dash drift hits in prose: 1 (P0)
- Banned hype-word hits: 196 (P1)
- Files with severe pronoun drift (you+we+reader, each substantial): 0 (P2)
- Files with Oxford-comma inconsistency: 5 (P2)
- Chapter-index pages with past-tense drift: 4 (P2)
- Book-wide hedging rate: 1.06 hedges per 1000 words
- Over-hedged chapters (>1.5x avg, >=2k words): 88
- Over-confident sections (0 hedging, >=2k words): 6

## P0: Em-dash hits in prose (user-banned character)

- `appendices/appendix-a-mathematical-foundations/section-a.5.html` (2x)
  - L85: `mathematical background you have built — linear algebra, probability, calculus,`
  - L85: `ility, calculus, and information theory — now grounds practical ML concepts: lear`
- `part-11-applications-across-industries/module-57-manufacturing-llms/index.html` (2x)
  - L178: `/IEC 42001:2023, Information technology — Artificial intelligence — Management sy`
  - L178: `on technology — Artificial intelligence — Management system</a>, the AI managemen`
- `part-12-frontiers/module-61-frontier-architectures/section-61.4.html` (1x)
  - L335: `atory elements, or codon-level patterns — fewer tokens means longer effective con`
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.8.html` (1x)
  - L464: `the expected progress reduction is ~6% — viable for multi-week pretraining.</div`
- `part-2-understanding-llms/module-10-inference-optimization/section-10.7.html` (1x)
  - L658: `V (read it again and write the output) — three round-trips to HBM, which is the`

## P0: Double-dash drift `--` in prose

- `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` (1x)
  - L635: `n.  [0.715] The cat sat on the mat. &lt;-- BEST  [0.074] Purple elephants danced w`

## P1: Banned hype words

**Book-wide totals:**
- `essential (marketing)`: 76
- `state-of-the-art (adj)`: 60
- `paradigm shift`: 21
- `definitive`: 18
- `must-read`: 10
- `cutting-edge`: 6
- `groundbreaking`: 3
- `game-changer`: 1
- `world-class`: 1

**Top files by hype-word count:**
- `part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.5.html` (total 7): state-of-the-art (adj)=4, essential (marketing)=2, groundbreaking=1
  - `groundbreaking`: ...: "Dr. Sarah Chen published a groundbreaking paper on protein folding. She...
  - `essential (marketing)`: ...hybrid extraction pipelines. Essential reading for teams building extraction...
- `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html` (total 5): essential (marketing)=2, state-of-the-art (adj)=2, paradigm shift=1
  - `paradigm shift`: ...t six months later. 
 
 
 The Paradigm Shift: Pre-train, Then Fine-tune...
  - `essential (marketing)`: ...t layers for different tasks. Essential reading for understanding the transit...
- `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html` (total 4): paradigm shift=2, essential (marketing)=1, state-of-the-art (adj)=1
  - `paradigm shift`: ...: The four eras of NLP. Each paradigm shift was driven by a breakthrough...
  - `essential (marketing)`: ...o the topics in this section. Essential reading for anyone building a solid N...
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html` (total 4): essential (marketing)=3, definitive=1
  - `definitive`: ...uage Model Applications.  The definitive catalog of LLM security risks...
  - `essential (marketing)`: ...severity and exploitability. Essential reading for any engineer building pro...
- `part-10-idea-to-product/module-41-product-management/section-41.2.html` (total 3): must-read=2, definitive=1
  - `definitive`: ...Customers Love . Wiley.  The definitive guide to modern product manag...
  - `must-read`: ...han manual work because users must read, evaluate, and correct the AI...
- `part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html` (total 3): paradigm shift=1, game-changer=1, state-of-the-art (adj)=1
  - `paradigm shift`: ...s like Perplexity represent a paradigm shift from "ten blue links" to dire...
  - `game-changer`: ...s)
- "Offline mode would be a game-changer" (9 mentions)
...

 
  Code F...
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html` (total 3): state-of-the-art (adj)=2, paradigm shift=1
  - `paradigm shift`: ...context learning considered a paradigm shift? 
 
 Show Answer 
 In-context...
  - `state-of-the-art (adj)`: ...ring. ALBERT-xxlarge achieved state-of-the-art results with 70% fewer parameters tha...
- `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.1.html` (total 3): essential (marketing)=2, paradigm shift=1
  - `paradigm shift`: ..."thinking" mode) represent a paradigm shift: spending more compute at inf...
  - `essential (marketing)`: ...s, and deployment guardrails. Essential reading for understanding how frontie...
- `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html` (total 3): paradigm shift=2, cutting-edge=1
  - `cutting-edge`: ...es next:  Having surveyed the cutting-edge reasoning capabilities of mod...
  - `paradigm shift`: ...ion. 
 
 
 Big Picture 
  The paradigm shift from train-time to test-time...
- `part-2-understanding-llms/module-10-inference-optimization/section-10.6.html` (total 3): paradigm shift=2, essential (marketing)=1
  - `paradigm shift`: ...to get better answers?"  This paradigm shift, known as  test-time compute...
  - `essential (marketing)`: ...odes, and safety mitigations. Essential reading for understanding the alignme...
- `part-4-training-adapting/module-19-peft/section-19.3.html` (total 3): cutting-edge=1, essential (marketing)=1, state-of-the-art (adj)=1
  - `cutting-edge`: ...Plan accordingly if you need cutting-edge model support. 
 
 16.3.7 Clo...
  - `essential (marketing)`: ..., and parameters across GPUs. Essential reading for anyone scaling beyond a s...
- `part-4-training-adapting/module-21-tools-of-the-trade/section-21.3.html` (total 3): state-of-the-art (adj)=3
  - `state-of-the-art (adj)`: ...when you want to reproduce a state-of-the-art instruction-tuned model. The core concept...
- `part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html` (total 2): definitive=1, essential (marketing)=1
  - `definitive`: ...n  (2nd ed.). MIT Press.  The definitive RL textbook, covering everyth...
  - `essential (marketing)`: ...ts discussed in this section. Essential reading for practitioners choosing be...
- `part-1-foundations/module-02-tokenization-subword-models/section-2.1.html` (total 2): essential (marketing)=2
  - `essential (marketing)`: ...ed by nearly all modern LLMs. Essential reading for understanding why tokeniz...
- `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` (total 2): essential (marketing)=2
  - `essential (marketing)`: ...evaluating tokenizer equity. Essential reading for teams deploying multiling...
- `part-1-foundations/module-04-transformer-architecture/section-4.3.html` (total 2): must-read=1, essential (marketing)=1
  - `must-read`: ...e O(T^2) memory bottleneck. A must-read for understanding how hardwar...
  - `essential (marketing)`: ...istral, and most modern LLMs. Essential reading for understanding how product...
- `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` (total 2): cutting-edge=1, essential (marketing)=1
  - `cutting-edge`: .... These methods represent the cutting edge of practical text generation....
  - `essential (marketing)`: ...entical output distributions. Essential reading for production LLM deployment...
- `part-10-idea-to-product/module-45-prototype-to-production/section-45.1.html` (total 2): definitive=2
  - `definitive`: ...er than presenting outputs as definitive facts. Where possible, expose...
- `part-10-idea-to-product/module-46-compute-planning/section-46.3.html` (total 2): essential (marketing)=2
  - `essential (marketing)`: ...s, and Spot Fleet strategies. Essential knowledge for teams optimizing cloud GP...
- `part-10-idea-to-product/module-47-scaling-economics/section-47.4.html` (total 2): essential (marketing)=1, state-of-the-art (adj)=1
  - `essential (marketing)`: ...eakdowns for each model tier. Essential reference for the cost calculations and...
  - `state-of-the-art (adj)`: ..., which looks beyond today's state of the art to emerging architectures and AI...
- `part-11-applications-across-industries/module-56-government-llms/section-56.5.html` (total 2): essential (marketing)=2
  - `essential (marketing)`: ...l commission report (2023) is essential reading for anyone deploying automate...
- `part-12-frontiers/module-61-frontier-architectures/section-61.4.html` (total 2): state-of-the-art (adj)=2
  - `state-of-the-art (adj)`: ...redient brought AlphaFold2 to state-of-the-art that pure-LM approaches lacked....
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html` (total 2): essential (marketing)=1, state-of-the-art (adj)=1
  - `essential (marketing)`: ...el size and data duplication. Essential reading for understanding privacy ris...
  - `state-of-the-art (adj)`: ...Hugging Face  represents the state of the art in open data curation. Starting...
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.5.html` (total 2): essential (marketing)=1, state-of-the-art (adj)=1
  - `essential (marketing)`: ...d mid-training interventions. Essential reading for understanding the real-wo...
  - `state-of-the-art (adj)`: ...ed attention when it achieved state-of-the-art results on the nanogpt-speedrun bench...
- `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html` (total 2): state-of-the-art (adj)=2
  - `state-of-the-art (adj)`: ...rare tokens. BioBERT achieved state-of-the-art results on
 biomedical NER, relation...
- `part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html` (total 2): paradigm shift=2
  - `paradigm shift`: ...ng Objectives 
 
 Explain the paradigm shift from train-time to test-time...
- `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.1.html` (total 2): paradigm shift=1, essential (marketing)=1
  - `paradigm shift`: ...reasoning models represent a paradigm shift. 
  Train-time compute  is th...
  - `essential (marketing)`: ...tperforms train-time scaling. Essential reading for understanding the compute...
- `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.6.html` (total 2): essential (marketing)=1, state-of-the-art (adj)=1
  - `essential (marketing)`: ...ased formal proving research. Essential reading for anyone building formal pr...
  - `state-of-the-art (adj)`: ...le for interactive use. 
 
 
 State-of-the-Art Results on miniF2F (as of early 2026)...
- `part-2-understanding-llms/module-10-inference-optimization/section-10.3.html` (total 2): must-read=1, essential (marketing)=1
  - `must-read`: ...a single decode step, the GPU must read all model weights from memory...
  - `essential (marketing)`: ...ing using a rejection scheme. Essential reading for understanding why specula...
- `part-2-understanding-llms/module-11-interpretability/section-11.1.html` (total 2): definitive=2
  - `definitive`: ...int for investigation, not as definitive evidence of model reasoning....
- `part-3-working-with-llms/module-13-llm-apis/section-13.1.html` (total 2): definitive=1, essential (marketing)=1
  - `definitive`: ...mpletions API Reference.  The definitive reference for the most widely...
  - `essential (marketing)`: ...ng, and all model parameters. Essential reading for anyone building on the Op...
- `part-3-working-with-llms/module-13-llm-apis/section-13.4.html` (total 2): must-read=1, essential (marketing)=1
  - `must-read`: ...processes invoices: the model must read the document (vision), extrac...
  - `essential (marketing)`: ...s,  tool use , and streaming. Essential reference for implementing the OpenAI e...
- `part-3-working-with-llms/module-14-prompt-engineering/section-14.3.html` (total 2): paradigm shift=1, essential (marketing)=1
  - `paradigm shift`: ...mpts on multi-step tasks. The paradigm shift: prompts are parameters to be...
  - `essential (marketing)`: ...vered in this section, and is essential reading for anyone implementing self-...
- `part-3-working-with-llms/module-14-prompt-engineering/section-14.4.html` (total 2): definitive=1, essential (marketing)=1
  - `definitive`: ...0 for LLM Applications .  The definitive industry standard for LLM sec...
  - `essential (marketing)`: ...chniques available, making it essential reading for anyone building defenses...
- `part-4-training-adapting/module-17-synthetic-data/section-17.1.html` (total 2): cutting-edge=1, essential (marketing)=1
  - `cutting-edge`: ...at all. Magpie represents the cutting edge of synthetic data generation...
  - `essential (marketing)`: ...ings throughout this section. Essential reading before deploying any syntheti...
- `part-4-training-adapting/module-17-synthetic-data/section-17.6.html` (total 2): essential (marketing)=1, state-of-the-art (adj)=1
  - `essential (marketing)`: ...urprisingly strong reasoning. Essential reading for this section's core conce...
  - `state-of-the-art (adj)`: ...ller students) is the current state of the art for building small reasoning mode...
- `part-4-training-adapting/module-19-peft/section-19.4.html` (total 2): essential (marketing)=1, state-of-the-art (adj)=1
  - `essential (marketing)`: ...ine-tuning at 11B parameters. Essential reading for anyone considering soft p...
  - `state-of-the-art (adj)`: ..., & Bossan, B. (2022).  PEFT: State-of-the-art Parameter-Efficient Fine-Tuning methods...
- `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.2.html` (total 2): essential (marketing)=1, state-of-the-art (adj)=1
  - `essential (marketing)`: ...d model and RL loop entirely. Essential reading for anyone working on prefere...
  - `state-of-the-art (adj)`: ...-free reward signal. Achieves state-of-the-art results with simpler implementation t...
- `part-4-training-adapting/module-21-tools-of-the-trade/section-21.4.html` (total 2): state-of-the-art (adj)=2
  - `state-of-the-art (adj)`: ...fine-tunes, Llama 4 Scout for state-of-the-art open quality. Check the Llama Comm...
- `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.2.html` (total 2): definitive=1, essential (marketing)=1
  - `definitive`: ...d Graphs."  IEEE TPAMI .  The definitive HNSW paper. Explains the mult...
  - `essential (marketing)`: ...production vector databases. Essential reading for understanding index tunin...
- ...86 more files with hype words

## P2: Pronoun consistency (you / we / reader)

_No files mix all three pronoun forms heavily._

## P2: Tense drift in chapter-index pages (should be present tense)

- `part-1-foundations/module-04-transformer-architecture/index.html` (1 past-tense hits)
  - `Chapter 3 introduced`
- `part-4-training-adapting/module-19-peft/index.html` (1 past-tense hits)
  - `Chapter 18 introduced`
- `part-7-multimodal-generation/module-32-embodied-world-models/index.html` (1 past-tense hits)
  - `Chapter 31  covered`
- `part-9-safety-security-ethics/module-38-agent-safety-security/index.html` (1 past-tense hits)
  - `Chapter 37  covered`

## P2: Oxford-comma inconsistency within file

- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.4.html` -- Oxford: 3x, non-Oxford: 3x
- `front-matter/fm-what-this-book-covers.html` -- Oxford: 4x, non-Oxford: 5x
- `part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.2.html` -- Oxford: 3x, non-Oxford: 4x
- `part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.1.html` -- Oxford: 3x, non-Oxford: 4x
- `part-6-agentic-ai/module-29-specialized-agents/section-29.3.html` -- Oxford: 7x, non-Oxford: 3x

## P2: Hedging variance

Book-wide hedging rate (files >=500 words): 1.06 hedges per 1000 words.

**Over-hedged chapters (rate > 1.5x book average, >=2k words):**
- `part-12-frontiers/module-61-frontier-architectures/section-61.1.html` -- 5.11/1k (18 hedges in 3523 words). Top: may=9, might=5, could=4
- `part-1-foundations/module-02-tokenization-subword-models/section-2.1.html` -- 5.09/1k (23 hedges in 4523 words). Top: might=11, may=8, could=3
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html` -- 4.55/1k (20 hedges in 4396 words). Top: could=16, may=2, perhaps=2
- `part-8-evaluation-production/module-34-evaluation-observability/section-34.5.html` -- 3.80/1k (12 hedges in 3155 words). Top: may=8, might=2, could=2
- `part-4-training-adapting/module-17-synthetic-data/section-17.1.html` -- 3.80/1k (14 hedges in 3684 words). Top: may=9, might=2, could=2
- `part-12-frontiers/module-62-frontier-theory/section-62.3.html` -- 3.67/1k (12 hedges in 3272 words). Top: may=8, might=2, could=2
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.8.html` -- 3.50/1k (15 hedges in 4281 words). Top: may=9, could=4, might=2
- `part-12-frontiers/module-62-frontier-theory/section-62.4.html` -- 3.49/1k (11 hedges in 3148 words). Top: may=8, might=3
- `part-3-working-with-llms/module-14-prompt-engineering/section-14.2.html` -- 3.40/1k (15 hedges in 4408 words). Top: may=9, might=4, could=2
- `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.5.html` -- 3.31/1k (13 hedges in 3931 words). Top: may=9, might=2, could=2
- `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html` -- 3.28/1k (14 hedges in 4268 words). Top: could=11, may=2, arguably=1
- `part-10-idea-to-product/module-45-prototype-to-production/section-45.3.html` -- 3.26/1k (14 hedges in 4294 words). Top: may=10, could=4
- `part-9-safety-security-ethics/module-38-agent-safety-security/section-38.2.html` -- 3.20/1k (8 hedges in 2501 words). Top: could=7, may=1
- `part-12-frontiers/module-61-frontier-architectures/section-33.4.html` -- 3.14/1k (16 hedges in 5089 words). Top: may=7, could=6, might=2
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.7.html` -- 3.07/1k (9 hedges in 2931 words). Top: may=5, might=2, could=1
- `part-12-frontiers/module-62-frontier-theory/section-62.1.html` -- 2.99/1k (12 hedges in 4011 words). Top: may=8, might=2, could=2
- `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.6.html` -- 2.95/1k (8 hedges in 2710 words). Top: might=4, could=3, may=1
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.2.html` -- 2.93/1k (12 hedges in 4094 words). Top: may=7, could=5
- `part-12-frontiers/module-62-frontier-theory/section-62.2.html` -- 2.92/1k (10 hedges in 3421 words). Top: may=5, could=3, might=2
- `part-2-understanding-llms/module-11-interpretability/section-11.3.html` -- 2.88/1k (14 hedges in 4855 words). Top: might=6, may=6, could=2
- `part-5-retrieval-conversation/module-23-rag/section-23.2.html` -- 2.88/1k (13 hedges in 4511 words). Top: may=8, might=3, could=2
- `part-8-evaluation-production/module-34-evaluation-observability/section-34.9.html` -- 2.85/1k (11 hedges in 3854 words). Top: may=9, might=1, could=1
- `part-2-understanding-llms/module-11-interpretability/section-11.1.html` -- 2.72/1k (13 hedges in 4783 words). Top: may=6, could=4, might=3
- `part-12-frontiers/module-61-frontier-architectures/section-61.2.html` -- 2.64/1k (10 hedges in 3793 words). Top: may=8, might=1, perhaps=1
- `part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html` -- 2.63/1k (7 hedges in 2661 words). Top: may=6, might=1
- `part-2-understanding-llms/module-11-interpretability/section-11.2.html` -- 2.62/1k (16 hedges in 6112 words). Top: might=7, could=6, may=3
- `part-2-understanding-llms/module-11-interpretability/section-11.4.html` -- 2.61/1k (15 hedges in 5744 words). Top: may=7, might=6, could=2
- `part-1-foundations/module-05-decoding-text-generation/section-5.1.html` -- 2.57/1k (12 hedges in 4667 words). Top: might=5, could=4, may=3
- `part-10-idea-to-product/module-46-compute-planning/section-46.4.html` -- 2.56/1k (10 hedges in 3899 words). Top: may=6, could=3, might=1
- `part-8-evaluation-production/module-34-evaluation-observability/section-34.2.html` -- 2.55/1k (9 hedges in 3529 words). Top: may=4, could=4, might=1

**Over-confident sections (0 hedging words in >=2k words):**
- `part-5-retrieval-conversation/module-23-rag/section-23.8.html` -- 4087 words, 0 hedges
- `part-4-training-adapting/module-19-peft/section-19.6.html` -- 3591 words, 0 hedges
- `part-8-evaluation-production/module-35-production-engineering/section-35.2.html` -- 3057 words, 0 hedges
- `part-10-idea-to-product/module-43-vibe-coding/section-43.1.html` -- 2324 words, 0 hedges
- `part-10-idea-to-product/module-41-product-management/section-41.1.html` -- 2105 words, 0 hedges
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.4.html` -- 2102 words, 0 hedges

## Top recurring offenders (weighted score)

- `part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.5.html` -- 28 pts (hype=7)
- `appendices/appendix-a-mathematical-foundations/section-a.5.html` -- 20 pts (em-dash=2)
- `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html` -- 20 pts (hype=5)
- `part-11-applications-across-industries/module-57-manufacturing-llms/index.html` -- 20 pts (em-dash=2)
- `part-12-frontiers/module-61-frontier-architectures/section-61.4.html` -- 18 pts (em-dash=1, hype=2)
- `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html` -- 16 pts (hype=4)
- `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` -- 16 pts (--=1, hype=2)
- `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.1.html` -- 16 pts (hype=4)
- `part-10-idea-to-product/module-41-product-management/section-41.2.html` -- 12 pts (hype=3)
- `part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html` -- 12 pts (hype=3)
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.1.html` -- 12 pts (hype=3)
- `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.1.html` -- 12 pts (hype=3)
- `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html` -- 12 pts (hype=3)
- `part-2-understanding-llms/module-10-inference-optimization/section-10.6.html` -- 12 pts (hype=3)
- `part-4-training-adapting/module-19-peft/section-19.3.html` -- 12 pts (hype=3)
- `part-4-training-adapting/module-21-tools-of-the-trade/section-21.3.html` -- 12 pts (hype=3)
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.8.html` -- 10 pts (em-dash=1)
- `part-2-understanding-llms/module-10-inference-optimization/section-10.7.html` -- 10 pts (em-dash=1)
- `part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html` -- 8 pts (hype=2)
- `part-1-foundations/module-02-tokenization-subword-models/section-2.1.html` -- 8 pts (hype=2)
- `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` -- 8 pts (hype=2)
- `part-1-foundations/module-04-transformer-architecture/section-4.3.html` -- 8 pts (hype=2)
- `part-10-idea-to-product/module-45-prototype-to-production/section-45.1.html` -- 8 pts (hype=2)
- `part-10-idea-to-product/module-46-compute-planning/section-46.3.html` -- 8 pts (hype=2)
- `part-10-idea-to-product/module-47-scaling-economics/section-47.4.html` -- 8 pts (hype=2)
- `part-11-applications-across-industries/module-56-government-llms/section-56.5.html` -- 8 pts (hype=2)
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.4.html` -- 8 pts (hype=2)
- `part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.5.html` -- 8 pts (hype=2)
- `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html` -- 8 pts (hype=2)
- `part-2-understanding-llms/module-09-reasoning-test-time-compute/index.html` -- 8 pts (hype=2)

## Recommended deterministic fixes (scriptable)

- Replace `—` -> `, ` book-wide (7 occurrences in prose). Manual review: some may want `;`, `:`, or parens depending on context.
- Replace ` -- ` -> `, ` book-wide (1 occurrences in prose, excluding code/CLI flags).
- Audit `essential (marketing)` (76 occurrences) - consider a non-hype substitute or removal.
- Audit `state-of-the-art (adj)` (60 occurrences) - consider a non-hype substitute or removal.
- Audit `paradigm shift` (21 occurrences) - consider a non-hype substitute or removal.
- Audit `definitive` (18 occurrences) - consider a non-hype substitute or removal.
- Audit `must-read` (10 occurrences) - consider a non-hype substitute or removal.
- Audit `cutting-edge` (6 occurrences) - consider a non-hype substitute or removal.
- Audit `groundbreaking` (3 occurrences) - consider a non-hype substitute or removal.
- Audit `game-changer` (1 occurrences) - consider a non-hype substitute or removal.
- Audit `world-class` (1 occurrences) - consider a non-hype substitute or removal.
- Rewrite past tense in chapter-index pages to present tense in 4 files.
- Pick a single Oxford-comma policy per file in 5 files; the dominant style book-wide is detectable per-section.
