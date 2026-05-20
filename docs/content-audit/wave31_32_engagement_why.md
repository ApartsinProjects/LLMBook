# Wave 31+32: engagement / "why" audit

Audit scope: the "new" tools-of-the-trade chapters (Ch 36, 41, 56, 61), the
distributed-training chapter (Ch 59), the Wave 17i-touched sections (24.6, 24.13,
26.6, 27.5, 29.1, 29.4, 35.2, 35.3, 37.3), and the Wave 9 promotions (Ch 34, Ch
46). For each, this report flags (A) engagement / illustration opportunities and
(B) "why" / counterfactual / cross-field opportunities.

Voice reference points: Section 1.3 ("King minus man plus woman equals queen. I
tried this with my coworkers and HR got involved."), Section 3.1 ("Why Multiple
Heads?", "Common Misconception: Attention Does Not 'Focus on Important Words'",
"Fun Fact" callouts), Section 6.3 (the compute-optimal vs. token-optimal
explanation), Section 26.1 (why LLM-as-agent is not just LLM-with-tools).

## Top engagement gaps (prioritized)

The highest-leverage propositions, ranked by audience impact:

1. **Ch 36 (Retrieval Tools) is the single driest chapter in the new wave.** Five
   sections, ~1,400 lines, almost no anecdote, no comical analogy, no
   counterfactual reasoning, no XKCD-style explanation. The chapter reads as a
   well-organized vendor encyclopedia. PROPOSE: at least one fun-note per
   section (vector-DB market history, the BM25 / BEIR humbling, why
   sentence-transformers won the API war), one mental-map figure for embedder
   tiers in 36.4, a comical illustration for "vector DB lock-in" in 36.1, and a
   "Why this works" callout in 36.2 explaining why orchestration frameworks
   leak. The chapter has only one fun-note in 5 sections (the BM25 BEIR finding
   in 36.3); the canonical voice from Ch 3 / Ch 6 demands 3-5x that density.
2. **Ch 41 (Conv-AI Tools) section 41.1 has no "why does this category exist"
   framing.** The seven platform categories are listed without an evolutionary
   story (intent-classifier era -> generative-first era -> LLM-overlay-on-FSM
   era). PROPOSE: a 1-paragraph historical arc at the top of 41.1.1 explaining
   why Dialogflow CX exists in its current shape, and an XKCD-style illustration
   of "who builds vs who runs" (the designer / engineer / ops trifecta).
3. **Ch 56 (Responsible AI Tools) reads as a buyer's guide for compliance
   officers, not as a book on responsible AI.** Almost no human story.
   PROPOSE: section 56.1 needs an opening anecdote (e.g., the COMPAS-or-NYC LL
   144 story, or the IBM Watson Health unwind) to ground the platform list in
   actual harm; 56.2 needs a "Why this works" connection to classical statistics
   (the impossibility theorems behind fairness metrics); 56.4 needs a
   counterfactual on "what if we tried to prove safety mathematically rather
   than red-team it?".
4. **Ch 61 (Scale Tools) is missing the "why frontier labs build vs rent" arc.**
   The chapter lists xAI Colossus, Meta RSC, OpenAI on Azure as static facts
   rather than as a strategic story. PROPOSE: a fun-note on the Colossus
   122-day build (vs. AWS / Azure waitlist mythology), a mental-map figure of
   the four-tier platform stack (hyperscaler / specialized GPU cloud / HPC
   scheduler / parallel storage), and a counterfactual callout: "what if
   InfiniBand had not existed?" answering with the RoCE-on-Ethernet Meta story
   already in the section.
5. **Ch 59 (Distributed Training) is the best of the new wave on "why" but
   lacks comical illustration.** It has Key Insight callouts for BSP and the
   barrier-as-feature, but no humor, no XKCD-style metaphor for what 3D
   parallelism actually feels like. PROPOSE: comical illustration for "the
   straggler GPU" (one slow kid in line everyone is waiting on, the "tail
   latency tax"), and a mental-map figure of the parallelism cube (data x
   tensor x pipeline) showing which corners are inhabited by which production
   systems.
6. **Section 24.13 (sim-to-real) has good content but no historical anecdote.**
   PROPOSE: fun-note on Tobin et al. 2017 "Domain Randomization" Frisbee-throwing
   robot reveal at IROS (the photo of the robot covered in random-color
   stickers is community-famous).
7. **Ch 36 section 36.2 is the worst case of "list of libraries" with no
   why-this-API-won story.** PROPOSE: a "Why sentence-transformers killed raw
   HF AutoModel" paragraph at 36.2.1 explaining that the win was the two-line
   API + automatic normalization + cross-encoder symmetry, not the model
   quality.
8. **Ch 41 section 41.2 has the framework half-life fun-note but no comical
   illustration of the framework treadmill.** PROPOSE: an XKCD-style
   illustration of "the LangChain abstraction migration cycle" (Chain ->
   LCEL -> LangGraph in 24 months) and a cross-field connection to "Conway's
   Law" and dependency hell.
9. **No section in the new wave draws the connection to control theory / DSP
   / distributed-systems literature.** The single most underused cross-field
   bridge: NCCL all-reduce is a distributed-consensus problem with a closed-form
   bandwidth-optimal solution (Patarasuk and Yuan 2009); Megatron tensor
   parallelism is matrix factorization; the BSP barrier is the inverse of
   eventual consistency; agent memory architectures echo virtual-memory
   systems (Multics, the OS-as-LLM framing in MemGPT). 26.6 starts this
   well; the rest of the new wave should pick up the thread.
10. **No hero image / chapter-opener images for any of Ch 36 / 41 / 56 / 61.**
    They get by on the platform-landscape SVGs but lack the iconic
    chapter-opener of the older Part-1 chapters. Each chapter deserves one
    visually striking opener (the retrieval funnel, the conversation loop, the
    governance dashboard, the GPU pod).

## Per-chapter findings

### Chapter 36 - Retrieval Tools of the Trade

#### Engagement

- **section-36.1**: PROPOSE fun-note **"The vector DB that ate the database
  market"** - historical anecdote on Pinecone's 2022-2023 rise after the ChatGPT
  moment, the parallel rise of Weaviate / Qdrant / Chroma, and the Postgres
  counter-revolution via pgvector ("the database that ate the vector database").
  Placement: after 36.1.1 (Serverless and hosted vector databases).
  Size: 1 callout (~150 words).
- **section-36.1**: PROPOSE comical illustration **"vector DB lock-in / cat in
  a Pinecone bag"** - XKCD-style, the index format as a one-way door. The text
  already has "every platform's index format is proprietary"; the image makes
  it memorable. Size: 1 illustration.
- **section-36.1**: PROPOSE mental-map figure **"vector store selection
  decision tree"** - the section 36.1.5 decision tree is in prose; making it a
  fork-shaped figure (managed-or-self-hosted -> hybrid-or-vector-only ->
  multi-tenant-or-single -> filter-heavy-or-not) would make the chapter
  navigable.
- **section-36.2**: PROPOSE fun-note **"The sentence-transformers conquering"** -
  why a 200-line wrapper around HuggingFace AutoModel became the de facto API.
  The win was not the model; it was the .encode() one-liner plus matching
  CrossEncoder, plus L2-normalization-by-default. Cite Reimers and Gurevych
  2019, then note that sentence-transformers' import count surpassed transformers
  for retrieval workflows by 2023. Size: 1 callout.
- **section-36.2**: PROPOSE mental-map **"The five layers of a retrieval
  stack"** - embedder | vector store | BM25 | fusion | reranker - as one
  schematic figure. The "thinnest viable stack" section 36.2.8 lists them but
  a figure cements the architecture. Size: 1 figure.
- **section-36.3**: ALREADY HAS a strong fun-note ("The BM25 baseline still
  beats half of the dense retrievers on BEIR"). PROPOSE one more:
  **"The Trec-DL contamination kabuki"** - the cat-and-mouse game where TREC
  judges deeper to fix MS MARCO sparse judgments, then the deeper judgments
  leak into training, then a new contamination-resistant benchmark, then
  contamination again. The pattern is universal in IR and worth naming.
- **section-36.4**: PROPOSE mental-map figure **"the embedder tier hierarchy"** -
  closed API (OpenAI / Cohere / Voyage / Mistral) at the top, open-weight large
  (NV-Embed / Linq-Embed / GTE-Qwen2 7B-class) below, open-weight medium
  (BGE-M3, Stella, Snowflake Arctic) below that, matryoshka-truncated /
  domain-tuned at the bottom. With per-tier "pick when" labels. Currently the
  comparison table at 36.4.6 does this in tabular form; a tier figure is more
  memorable. Size: 1 figure.
- **section-36.4**: PROPOSE comical illustration **"3072 dimensions but only
  one truth"** - matryoshka representation visualized as a Russian-doll stack
  with each shell labeled with quality / cost / storage tradeoffs. Helps cement
  the matryoshka property. Size: 1 illustration.
- **section-36.5**: PROPOSE one fun-note **"The two literatures that do not
  talk to each other"** - the existing "two literatures" key insight is great
  but currently in a callout-warning; turn it into a story anecdote (e.g., the
  SIGIR 2024 talk that name-checked LangChain and was met with confusion). Size:
  1 callout rewrite + 1 anecdote.

#### "Why" depth

- **section-36.1**, 36.1.1: PROPOSE **"Why pgvector reversed the architecture
  trend"** - the section says pgvector is the right pick under 50M vectors but
  does not explain the deeper why: avoiding the dual-write consistency problem.
  Add a paragraph: "Why a Postgres extension beat a purpose-built vector DB at
  this scale": dual-write coordination + ACID transactions on (vector, metadata)
  pairs + reuse of existing backup, replication, monitoring. Cross-field
  connection to **distributed systems** (the dual-write problem is the same
  problem databases solved 40 years ago). Size: 1 paragraph.
- **section-36.1**, 36.1.4 (selection axes): PROPOSE counterfactual **"What if
  filter selectivity were the wrong axis to optimize?"** Currently the section
  treats filter-aware ANN (Qdrant's filterable HNSW) as the "right" answer for
  selective queries. The counterfactual: pre-filtering with a separate BM25
  inverted index then ANN over the candidate set is what Elastic / OpenSearch
  do, and it works fine when the corpus fits in one engine. The "right" answer
  depends on whether your engine can fuse the two indexes; the modern lesson is
  that vector-DB-native filter-aware ANN is one of three valid patterns.
- **section-36.2**, 36.2.1 (Embedding libraries): PROPOSE **"Why
  sentence-transformers won"** - explain WHY this library beat raw HuggingFace
  AutoModel for retrieval (single-line API, batched normalization, cross-encoder
  symmetry, model-card-driven prompts). Currently the section just lists; add
  one paragraph of "why this matters" - the API ergonomics are 90% of the
  adoption story, model quality is 10%. Cross-field connection to **software
  engineering** (the "library API as user interface" principle).
- **section-36.2**, 36.2.3 (Orchestration frameworks): PROPOSE counterfactual
  **"What if frameworks owned the data flow?"** - the current "framework
  abstractions leak" key-insight is correct but defensive. The deeper question:
  why do frameworks fail at production scale? Answer: their abstraction layer
  is on the wrong axis. The right abstraction is **observability + caching +
  retries** (cross-cutting concerns); the wrong abstraction is **chunking +
  retrieval + prompting** (business logic that varies per use case). The
  Conway's-Law-flavored insight is worth a paragraph.
- **section-36.3**, 36.3.5 (MS MARCO comparing): PROPOSE **"Why TREC-DL exists
  when MS MARCO exists"** - the deeper why is that MS MARCO's sparse judgments
  mean MRR@10 is a noisy estimate; TREC-DL's deep judgments are an unbiased
  estimator of NDCG@10. Connection to **classical statistics** (sample-size /
  power calculation, the same reason large pre-registered RCTs beat
  meta-analyses of small studies). Currently the section calls them "sparse
  judgments" without explaining why sparsity is statistically bad. Size: 1
  paragraph.
- **section-36.4**, 36.4.3 (Late interaction): PROPOSE counterfactual **"What
  if we computed full cross-attention between query tokens and document tokens
  at retrieval time?"** Currently the section describes ColBERT as a "third
  family" without explaining the algorithmic compromise. Add: cross-attention
  over query-document is quadratic in (|Q| + |D|) and would be infeasible at
  scale; ColBERT's late-interaction MaxSim is the linear-in-|Q|+|D|
  approximation that preserves most of the recall. Cross-field connection to
  **information theory** (the MaxSim is a lower bound on the full mutual
  information). Size: 1 paragraph.
- **section-36.4**, 36.4.7 (Matryoshka): PROPOSE **"Why Matryoshka works"** -
  the section says the trick "lets a single embedder serve many dimensions"
  without explaining why this is non-trivial. The why: the loss function
  during training is a sum over prefix-lengths, forcing the network to encode
  the most important information in the first k dimensions for all k. Connection
  to **classical statistics** (principal components analysis - PCA puts the
  highest-variance information in the first components by construction;
  Matryoshka does this with a learned encoder rather than an eigendecomposition).
  Size: 1 paragraph.
- **section-36.5**, 36.5.2: PROPOSE counterfactual **"What if BM25 had been
  invented in 2010 instead of 1994?"** - the section emphasizes that BM25 is
  "a 1994-era algorithm" without giving readers a sense of why this is
  remarkable. The deeper insight: BM25 captures most of the information a
  retriever can extract from term frequency, and 30 years of research have
  added 10-15% NDCG on top. Connection to **classical statistics** (the
  Cramer-Rao bound: there is a ceiling on how much information you can extract
  from a fixed feature representation; BM25 is near that ceiling for
  bag-of-words features). Size: 1 paragraph.

### Chapter 41 - Conversational AI Tools of the Trade

#### Engagement

- **section-41.1**: PROPOSE fun-note **"The intent-classifier era's last
  stand"** - 2019-2023 the world ran on Dialogflow ES / Lex / Rasa-1.x intent
  classifiers; in 2023 the LLM collapsed the NLU stack into one model and the
  industry burned 5 years of intent ontologies overnight. The "Loebner Prize
  history" fun-note in 41.3.9 already does this for chat benchmarks; do
  the same for platforms. Size: 1 callout.
- **section-41.1**: PROPOSE comical illustration **"the four buyer
  personas"** - the General Counsel, the CDO, the CISO, and the ML researcher
  walk into a procurement meeting and each picks a different platform. The
  section literally enumerates them; an image makes the joke land.
- **section-41.1**: PROPOSE mental-map **"who builds vs who runs"** - the
  designer-led / engineer-led / ops-led axes mapped to platforms. The
  41.1.7 SVG covers the platforms; add a smaller 2D figure for the
  decision axes. Size: 1 figure (small).
- **section-41.2**: PROPOSE comical illustration **"the framework migration
  treadmill"** - Chain -> LCEL -> LangGraph in 24 months, captioned "I rewrote
  my agent three times and I judge everyone who still uses Chains" - matches
  the canonical voice ("I judge everyone who still writes for loops"). Size:
  1 illustration.
- **section-41.2**: PROPOSE cross-field callout **"Memory is virtual memory,
  again"** - the three-tier memory pattern (verbatim + summary + facts) is
  exactly the L1 / L2 / DRAM hierarchy in CPU design; MemGPT explicitly draws
  the analogy. Add a callout that names the connection. Size: 1 callout.
- **section-41.3**: ALREADY HAS the great Loebner-Prize fun-note. PROPOSE one
  more: **"The benchmark contamination Olympics"** - MT-Bench / Arena are now
  in every model's training data; the field re-invents a fresh benchmark
  every 18 months. The Cobra Effect (perverse incentives) is the right
  metaphor. Size: 1 callout.
- **section-41.4**: HAS two fun-notes already ("size-vs-capability scaling no
  longer monotonic", "The Arena's hidden taxonomy"). The "Cost-per-conversation"
  paragraph at 41.4.7 could use one more: **"$0.20 per conversation, times a
  million conversations a month, equals 2 engineering salaries"** - a concrete
  scale-shock anecdote.
- **section-41.5**: ALREADY has two fun-notes. Could add a **mental-map figure
  of the chat-AI community ecosystem** (vendor / academic / practitioner /
  framework discord) so readers see the layers. Size: 1 figure.

#### "Why" depth

- **section-41.1**, 41.1.1 (Managed cloud platforms): PROPOSE **"Why
  state-machine platforms survived the LLM transition"** - Dialogflow CX and
  Rasa CALM both kept their state-machine DNA after adding LLM overlays.
  Why? Because regulated industries demand a static, reviewable policy graph.
  The deeper why: LLM policies are stochastic and unverifiable; auditors need
  a finite-state object they can enumerate. Connection to **formal verification**
  (the state-machine pattern is the only one with model-checking tooling).
  Currently the case study mentions it; promote to a "why this works" callout.
- **section-41.1**, 41.1.5 (Enterprise CCaaS): PROPOSE counterfactual **"What
  would Cresta look like without ChatGPT?"** - the company existed pre-2023 as
  an agent-assist platform; the LLM era moved it from a coach to a participant.
  The pivot pattern (existing CCaaS adds LLM = success; new LLM-first startup
  enters CCaaS = struggle) is a worth-naming industry dynamic.
- **section-41.2**, 41.2.1 (Conversation memory primitives): PROPOSE **"Why
  ConversationSummaryBufferMemory is the default"** - the section says it is the
  hybrid but does not explain why this specific shape (verbatim recent +
  summary old) won. The why: it matches human conversational memory, which is
  also a recent verbatim + older gist mixture (Murdock 1962 serial-position
  curve). Cross-field connection to **cognitive psychology**. Size: 1 paragraph.
- **section-41.2**, 41.2.2 (Conversation orchestration): PROPOSE counterfactual
  **"What if Anthropic Messages API had owned state like OpenAI Assistants?"** -
  the section presents the choice neutrally. The deeper why: Anthropic chose
  stateless-history because client-owned state is more auditable, more
  rewindable, and avoids the "what is in my Thread" debugging problem. Currently
  the trade-off is named but the design rationale is not.
- **section-41.2**, 41.2.4 (Voice runtimes): PROPOSE **"Why STT-LLM-TTS
  cascades hit a latency wall"** - the section says realtime APIs are faster
  but does not say why the cascade is slow. The why: serial latencies compound
  (STT 100-200ms + LLM TTFT 200ms + TTS 100-200ms = 500-700ms total), plus the
  end-of-speech detection is non-trivial. Realtime APIs collapse the cascade
  into one unified speech-to-speech model. Cross-field connection to **digital
  signal processing** and **control theory** (the latency budget is set by
  human turn-taking psychology, ~300ms; below that conversation feels
  natural, above that it feels stilted). Size: 1 paragraph.
- **section-41.3**, 41.3.3 (Preference benchmarks): PROPOSE **"Why LLM-as-judge
  replaced BLEU"** - the section names the shift but does not explain why
  preference-based metrics correlate with what users want better than n-gram
  overlap. The why: BLEU measures surface similarity to one reference; chat
  has many valid responses, so BLEU systematically penalizes diversity. Cross-field
  connection to **information retrieval evaluation** (NDCG already deals with
  this on the IR side via graded relevance; chat eval is catching up). Size:
  1 paragraph.
- **section-41.3**, 41.3.6 (Comparing the datasets): PROPOSE counterfactual
  **"What if we had not started with MultiWOZ?"** - the section treats MultiWOZ
  as canonical. The deeper question: the multi-domain belief-tracking
  architecture that MultiWOZ encouraged became the dominant TOD design for
  5+ years, including in production systems that did not need it. The
  benchmark shaped the architecture, not the reverse. This is the same dynamic
  as ImageNet -> CNN architectures, but rarely named in dialogue research.
- **section-41.4**, 41.4.4 (Open-weight chat models): PROPOSE **"Why
  Llama-3+ killed the closed-vs-open performance gap for chat"** - the section
  says "the gap is closing" but does not say why. The why: chat capability is
  primarily a post-training data problem (RLHF, preference data); the pretraining
  gap matters less. Once Meta released a strong base model with a public
  instruction-tuning recipe, anyone could close the gap. Cross-field connection
  to **economics of open-source** (the pretraining cost is a one-time
  investment; the post-training cost is recurring; opening the base model
  changes the cost structure). Size: 1 paragraph.

### Chapter 56 - Responsible AI Tools of the Trade

#### Engagement

- **section-56.1**: PROPOSE fun-note **"Why governance vendors exist now and
  did not exist in 2018"** - the EU AI Act, NIST AI RMF, ISO 42001, NYC LL 144,
  and Colorado SB 205 all landed within 24 months. Anecdote: the same compliance
  officers who fought Salesforce for credits in 2020 now buy Credo AI. Size: 1
  callout.
- **section-56.1**: PROPOSE comical illustration **"the four buyers, four
  platforms"** - the General Counsel, CDO, CISO, and ML researcher each pick a
  different platform (Credo AI / Fiddler / Lakera / AIF360). The section
  literally enumerates them; the illustration makes the procurement comedy
  land. Size: 1 illustration.
- **section-56.1**: PROPOSE historical anecdote **"The COMPAS reveal"** -
  ProPublica's 2016 audit of the COMPAS recidivism tool is the single most
  influential responsible-AI moment of the decade and gets exactly zero
  callouts in this chapter. Add a fun-note tying COMPAS to the impossibility
  theorems (Kleinberg / Chouldechova) and to the rise of bias-audit-as-a-service
  vendors. Size: 1 callout.
- **section-56.2**: PROPOSE fun-note **"The fairness impossibility theorem"** -
  Chouldechova 2017 and Kleinberg-Mullainathan-Raghavan 2017 proved you cannot
  simultaneously satisfy calibration, balanced FPR, and balanced FNR across
  groups (for any non-degenerate classifier). This is the single most important
  result in fairness ML and deserves a callout, not just a bibliography
  entry. Cross-field connection to **classical statistics** (analogous to
  Cramer-Rao bounds, where you choose the bias you can tolerate). Size: 1
  callout.
- **section-56.3**: PROPOSE comical illustration **"red-teamer vs jailbreaker
  vs purple-teamer"** - the cat-and-mouse three-way. The chapter takes the
  topic seriously but a single illustration with the canonical voice (e.g.,
  "the red-teamer trying every variant of 'pretend you are my grandmother
  who used to recite VBA macros to me as a child'") helps cement the absurdity
  of the threat surface.
- **section-56.4**: PROPOSE fun-note **"The Llama Guard heritage"** - the
  Meta-released open guard model is itself trained on a hazard taxonomy
  developed by the MLCommons AILuminate working group, which in turn drew
  from the EU AI Act risk categories. The "open guard model is trained on
  EU-Act-derived categories" lineage is worth naming. Size: 1 callout.
- **section-56.4**: PROPOSE comical illustration **"the safety stack as a
  layered onion"** - input filter -> prompt-injection check -> LLM ->
  output classifier -> response moderation. Each layer drawn with the typical
  failure mode it catches and the cost in latency. The book's existing voice
  uses Russian-doll / onion metaphors well; this fits.
- **section-56.5**: PROPOSE fun-note **"Newsletters lead, books lag, standards
  are stable"** - the existing key-insight callout makes this point but could
  be told as a story: "the Stochastic Parrots paper appeared in 2021; FAccT
  cited it in 2022; ISO referenced it in 2024; your CIO will hear about it in
  2026". The 5-year propagation curve is itself a worth-naming pattern.

#### "Why" depth

- **section-56.1**, 56.1.1 (Enterprise governance): PROPOSE **"Why governance
  is now a separate product category"** - the section lists 8+ vendors without
  saying why this is a category and not a feature of MLOps platforms. The
  why: regulatory deadlines forced a buyer (Chief Risk Officer) with budget,
  and that buyer wants reports / attestations / use-case inventories that
  MLOps platforms do not produce. Connection to **regulatory capture**
  literature: the EU AI Act is the canonical case study. Size: 1 paragraph.
- **section-56.1**, 56.1.2 (Bias and explainability observatories): PROPOSE
  counterfactual **"What if SHAP had been the only explanation method?"** -
  the section treats Fiddler and other "explainability platforms" as multi-method
  catalogs. The deeper why: SHAP became the de facto explanation method because
  it has solid game-theoretic foundations (Shapley values from cooperative game
  theory). Connection to **economics / mechanism design** - Shapley values are
  the unique allocation satisfying efficiency, symmetry, dummy, additivity.
  This deserves a "why this works" callout.
- **section-56.2**, fairness library design: PROPOSE counterfactual **"What if
  you cannot satisfy all three fairness criteria?"** - this is literally the
  Chouldechova impossibility result. The section's Fairlearn / AIF360 catalog
  lists "mitigation algorithms" without naming that all of them are picking
  which metric to optimize *because the others are mutually exclusive*. The
  "why" answer is the impossibility theorem above. Currently the section feels
  like a list of recipes; the impossibility result is the structural reason
  the list exists.
- **section-56.3**, red-team libraries: PROPOSE **"Why automated red-teaming
  works at all"** - the section lists PyRIT / garak / Counterfit without
  explaining why an automated attacker can find jailbreaks a human cannot.
  The why: the search space is high-dimensional (prompt token space) and
  gradient-style methods (GCG) plus mutation-style methods (PAIR, TAP) cover
  it better than human creativity. Cross-field connection to **adversarial
  machine learning** (the GCG paper is an adaptation of Wallace et al.
  universal triggers from text classification). Size: 1 paragraph.
- **section-56.4**, content-safety models: PROPOSE counterfactual **"What if
  we tried to prove safety mathematically rather than measure it
  empirically?"** - the section describes Llama Guard / ShieldLM / Aegis as
  classifier models. The deeper why: provable safety would require either
  (a) a finite-state policy the model cannot exit (Section 41.1's Dialogflow
  CX), or (b) a formal verification of the model itself (currently infeasible
  for transformer-scale models). The classifier-on-output design is the
  pragmatic compromise between the two. Connection to **formal methods** and
  to the "alignment versus capability" debate.
- **section-56.5**, 56.5.5 (Blogs and newsletters): PROPOSE **"Why
  responsible-AI moves on three independent clocks"** - the existing key-insight
  about newsletters / papers / standards is on the right track but could be
  named more sharply as an instance of the **policy diffusion** literature
  (Walker 1969, Rogers 1962). Academic insight propagates to policy on a
  5-year delay; commercial vendors follow on a 1-year delay; practitioners
  catch up on a weekly cadence. Size: 1 paragraph.

### Chapter 59 - Distributed Training Systems

This chapter is the *best* of the new wave on "why" depth. Multiple Key Insight
callouts: "Compute is cheap, memory bandwidth is not", "All-reduce factors into
reduce-scatter + all-gather", "Heads are pre-sharded", "TP is the only
parallelism that benefits from SHARP", "The bubble pays for memory savings",
"At 1000+ GPUs, the system is the algorithm", "Silent corruption is the worst
failure mode", "The barrier is a feature, not a bug", "Effective batch is the
only universal knob". The "why" depth is strong; engagement is where it could
improve.

#### Engagement

- **section-59.1**: PROPOSE comical illustration **"the straggler"** - the
  warning callout at 59.1.4 names tail latency and bounce-buffered transfers,
  but a single illustration ("one slow GPU is everyone's slow GPU") would
  cement why the barrier hurts. The "1000-GPU cluster slowed by one
  overheated card" anecdote deserves an image. Size: 1 illustration.
- **section-59.1**: PROPOSE fun-note **"The Hogwild! moment"** - Hogwild!
  (Niu et al. 2011) is briefly cited as the original async case. Add an
  anecdote: the paper title was a deliberate counter-cultural jab at the
  HPC tradition; "Hogwild!" became one of the most-cited paper titles of
  the 2010s in distributed ML. The async vs sync war and Hogwild's role in
  showing async could work for sparse SGD is a great history. Size: 1 callout.
- **section-59.2**: PROPOSE mental-map figure **"the parallelism cube"** -
  3 axes (data / tensor / pipeline), 8 corners (none, D-only, T-only, P-only,
  DT, DP, TP, DTP). Each corner labeled with which production system
  inhabits it (DDP, Megatron tensor-only, GPipe, FSDP+Megatron, etc.). The
  3D parallelism story is in 59.4 but a single figure showing the cube
  helps. Size: 1 figure.
- **section-59.3**: PROPOSE fun-note **"Why Megatron picked column-parallel
  first"** - the Megatron-LM paper's design choice (column-parallel for the
  up-projection, row-parallel for the down-projection) is so that activations
  flow naturally through the FFN without redundant all-reduces. The "why
  these two specific patterns and not others" is an engineering aesthetic
  worth naming. Currently 59.3 explains it; a fun-note about *who* figured it
  out (the NVIDIA team in 2019, motivated by GPT-2 scaling) adds humanity.
- **section-59.4**: PROPOSE fun-note **"The pipeline bubble was already
  understood in compilers"** - pipeline parallelism's bubble is mathematically
  identical to instruction-pipeline stalls in CPU design. The 1F1B schedule
  is the same trick as out-of-order execution: keep the pipeline full by
  starting the next micro-batch before the previous finishes. Cross-field
  connection to **computer architecture**. Size: 1 callout.
- **section-59.5**: PROPOSE comical illustration **"the silent corruption
  detective"** - one GPU's MFU drops 3% but no error log fires. The detective
  poses with a flame graph. The warning callout already names this; an
  illustration makes it memorable.

#### "Why" depth

- **section-59.1**, 59.1.3 (Collective primitives): ALREADY explains the
  ring-all-reduce bandwidth optimality. PROPOSE one more: **"Why NCCL's auto-tune
  switches to tree topology at small messages"** is mentioned but not explained.
  The why: ring all-reduce is O(N) latency; tree is O(log N) latency. The
  crossover point depends on the latency-to-bandwidth ratio; modern fabrics
  have ~us latency per hop, so trees win below ~MB messages. Cross-field
  connection to **distributed systems** (the latency-bandwidth product is the
  same trade-off TCP windowing optimizes). Currently the section gives the
  numbers; add the principle. Size: 1 paragraph.
- **section-59.2** (ZeRO and FSDP): PROPOSE counterfactual **"What if we
  sharded gradients differently?"** - the section explains ZeRO stages 1/2/3.
  Add: ZeRO-1 shards optimizer state but replicates parameters and gradients;
  ZeRO-2 adds gradient sharding; ZeRO-3 adds parameter sharding. The natural
  extension is "ZeRO-4 shards activations" - which is what FSDP-with-CPU-offload
  does, and it works but trades GPU memory for PCIe bandwidth, often a poor
  trade. The "why ZeRO stops at stage 3" question is the right framing.
- **section-59.3** (Megatron tensor parallelism): PROPOSE counterfactual
  **"What if we had sharded along the input axis instead of the output axis?"**
  - column-parallel vs row-parallel is a design choice with mathematical
  consequences (which all-reduces are needed, in which direction). The
  section explains the chosen pattern; add a paragraph explaining what the
  alternative would have cost (extra all-reduces in the forward pass).
- **section-59.4** (Pipeline parallelism): the "bubble pays for memory
  savings" insight is already strong. PROPOSE complement **"Why the bubble is
  the fundamental cost"** - the bubble is irreducible without micro-batching,
  and micro-batching has a hard floor (the per-stage compute must be larger
  than the activation memory; below that you trade compute for memory in a
  net-loss way). Connection to **queueing theory** (Little's Law: the
  in-flight items in the pipeline equal arrival rate times service time, so
  doubling the pipeline depth halves the per-batch latency only if the arrival
  rate doubles).
- **section-59.5** (Operational concerns): PROPOSE **"Why frontier labs build
  proprietary stacks on top of these primitives"** - the section's bibliography
  cites NCCL / DeepSpeed / Megatron as foundations but does not explain why
  Anthropic / OpenAI / Google build proprietary stacks on top. The why:
  per-cluster topology, per-cluster failure rates, per-cluster network
  topology all differ enough that "stock Megatron" is 70% performance, not
  95%. The 25% gap is what a proprietary stack closes. Connection to
  **systems performance engineering** (the last 30% is hand-tuned in every
  large-scale system, from Google's MapReduce to NASDAQ's matching engine).

### Chapter 61 - Scale Tools of the Trade

#### Engagement

- **section-61.1**: PROPOSE fun-note **"The 122-day Memphis sprint"** - the
  xAI Colossus build is already mentioned but not as an anecdote. Add: xAI
  did a 100K H100 stand-up in 122 days using on-site mobile generators
  because the local grid could not supply the load fast enough. The "rent
  diesel generators because the substation upgrade would take 18 months"
  story is the canonical 2024 hyperscale-buildout anecdote. Size: 1 callout.
- **section-61.1**: PROPOSE comical illustration **"InfiniBand or
  Ethernet?"** - the section's key insight about InfiniBand-vs-Ethernet
  bisection bandwidth is correct but dry. An illustration of "the cheap GPU
  cloud with 100Gb Ethernet" being a "pile of GPUs, not a cluster" would
  cement the point. Meta's RoCE-on-Ethernet design is a counter-example
  that deserves the joke.
- **section-61.1**: PROPOSE mental-map **"the four-layer scale stack"** - the
  41.1.7 SVG covers some of this but a clearer mental map of (hyperscaler /
  specialized GPU / scheduler / storage / observability) layers, with
  arrows showing which combinations are common, would help readers
  orient. Size: 1 figure.
- **section-61.2**: PROPOSE fun-note **"The Megatron-DeepSpeed-FSDP triumvirate"** -
  three frameworks doing largely the same thing, born of different orgs
  (NVIDIA / Microsoft / Meta), all now interoperating. The political /
  technical history is worth naming. Size: 1 callout.
- **section-61.3** (datasets): PROPOSE fun-note **"The Common Crawl
  embarrassment"** - many production LLMs were trained on a near-identical
  Common Crawl base; the only differentiation was filtering and weighting.
  Anecdote: the Pile, RedPajama, FineWeb, all RW versions of the same
  underlying corpus. The "they all read the same internet" insight is
  worth naming.
- **section-61.4** (models): PROPOSE comical illustration **"the model release
  treadmill"** - every 4-6 months a new frontier model release shifts the
  Pareto frontier. The illustration could show a treadmill with last-quarter's
  state-of-the-art falling off the back.
- **section-61.5** (communities): PROPOSE fun-note **"The arxiv-to-Twitter
  pipeline"** - a frontier-scale lab's release lands on arxiv at 9am PT,
  on Twitter / X by 9:01am, in HN comments by 9:05, in Latent Space by
  Thursday, in published peer review never. The cadence is worth naming.

#### "Why" depth

- **section-61.1**, 61.1.1 (Hyperscalers): PROPOSE **"Why HyperPod exists at
  AWS"** - the section describes HyperPod features without explaining why AWS
  built it. The why: SageMaker's ephemeral-training-job model was wrong for
  multi-week pre-training; HyperPod's persistent cluster model is closer to
  what Meta / OpenAI / Anthropic actually run. The product name change marks
  a strategic acknowledgement that AI training is a long-running stateful
  workload, not a batch job. Connection to **enterprise computing history**
  (the swing from mainframe -> distributed -> mainframe -> distributed -> "AI
  factory" is the same pattern as every previous workload cycle). Size: 1
  paragraph.
- **section-61.1**, 61.1.2 (Specialized GPU clouds): PROPOSE counterfactual
  **"What if CoreWeave had not pivoted from Bitcoin mining?"** - the section
  notes the pivot but does not explain the strategic insight: GPU-rental
  infrastructure is a different business than GPU-purchase financing. The
  CoreWeave story is the closest analog to the early-2010s pivot from
  Bitcoin mining to cryptocurrency mining-as-a-service, but at 1000x the
  capital intensity. Cross-field connection to **infrastructure economics**.
- **section-61.1**, 61.1.4 (HPC schedulers): PROPOSE **"Why Slurm survived
  the Kubernetes era"** - the section treats Slurm and Kubernetes as
  parallel options. The why Slurm survives: gang-scheduling is a hard problem
  Kubernetes only partially solved (via Volcano, which is itself non-trivial).
  Slurm's HPC heritage (decades of optimization for tightly-coupled MPI jobs)
  is the moat. Connection to **operating systems** (the gang-scheduling
  problem is the multi-resource bin-packing problem from OS scheduler theory).
  Size: 1 paragraph.
- **section-61.1**, 61.1.5 (Parallel storage): PROPOSE **"Why a parallel
  filesystem is required at scale"** - the section says training jobs need
  parallel storage but does not explain why object storage (S3 etc.) is not
  enough. The why: object storage has per-request latency that compounds with
  small reads (a 1KB file read is dominated by the round-trip, not the bytes);
  parallel filesystems give POSIX semantics with aggregate throughput because
  they parallelize the metadata. Connection to **storage systems** (the
  metadata-bottleneck vs throughput-bottleneck distinction is canonical from
  GFS and HDFS papers). Size: 1 paragraph.
- **section-61.2** (Frameworks): PROPOSE counterfactual **"What if PyTorch
  had not won?"** - the section lists Megatron-LM, DeepSpeed, FSDP (all
  PyTorch-native), then Pathways / JAX for TPUs. The deeper why: PyTorch
  won because eager execution + Python-native ergonomics + the HF Transformers
  hub gave it network effects TF could not match. The cluster-systems-frameworks
  ride on top of PyTorch's win. Connection to **platform economics** (the
  "developer mindshare" moat).
- **section-61.3** (Datasets at scale): the section lists OOD-style benchmarks.
  PROPOSE **"Why we still rely on Common Crawl"** - the why: nothing else has
  the scale (petabytes of text). The legal / quality issues are well-known
  but the alternatives (curated web text, synthetic data) cannot match the
  raw token count. Connection to **data-economics** (the marginal value of
  the Nth token approaches zero, but the first 10T tokens still need to
  come from somewhere). Size: 1 paragraph.
- **section-61.4** (Models at scale): PROPOSE counterfactual **"What if
  Meta had kept Llama closed?"** - the section names Llama as the canonical
  open-weight family without exploring how strategically anomalous its
  release was. The Meta strategy (open the base, monetize the platform) is
  similar to Google's Android strategy, and equally controversial inside Meta.
  Connection to **business strategy** (the "open source as competitive
  weapon" pattern).
- **section-61.5** (Communities): PROPOSE **"Why the AI Engineer / SemiAnalysis
  / TLDR-AI ecosystem replaced traditional trade press"** - the section
  lists them as venues. The deeper why: AI moves too fast for monthly
  trade press; the newsletter / podcast / Twitter triumvirate is the
  practitioner-to-practitioner communication channel. Connection to
  **media economics** (the journalist's role has been replaced by the
  practitioner's newsletter; AI Snake Oil and Import AI are examples).

### Sections from Wave 17i

#### Section 24.6 (VLA Limitations)

Section is already engaging. ALREADY HAS: fun-note ("pick up the block that
is not red"), warning callouts, research-frontier callout. Key takeaway works.

- PROPOSE one fun-note **"The unwrap-the-candy-bar benchmark"** that hooks the
  reader on the dexterity ceiling. Currently the section says "none of them
  can reliably do unwrap the candy bar" - this deserves an anecdote (e.g.,
  the DeepMind 2024 internal demo where the candy bar wrapper triggered an
  emergency stop). Size: 1 callout.

#### Section 24.13 (Sim-to-Real Gap)

ALREADY HAS: fun-note opportunities not fully exploited.

- PROPOSE **"the rainbow-colored Frisbee robot"** fun-note - Tobin et al. 2017
  Domain Randomization paper had a photograph of a robot grasping a randomly
  colored Frisbee that became the icon of sim-to-real research. The
  randomization-as-distribution-coverage insight deserves the story.
- PROPOSE counterfactual **"What if we had not done sim-to-real?"** - the
  section explains how sim-to-real works but not the counterfactual: pure
  on-robot RL was tried (Levine et al. 2016 arm farm) and failed at scale
  because the wall-clock cost of real-world rollouts was prohibitive. Sim-
  to-real is the engineering compromise. Connection to **reinforcement
  learning history** (the AlphaGo Zero / self-play paradigm only works because
  the simulator is free; in robotics it is not).

#### Section 26.6 (Agent Memory)

Already excellent. Has Key Insight, Mental Model, callout warnings, fun-note
opportunity in the resume-test framing.

- PROPOSE **"the Multics OS connection"** callout - MemGPT explicitly draws
  the analogy of agent memory to operating-system virtual memory. The
  Multics / Unix history is worth naming. Cross-field connection to
  **operating systems** is implicit in MemGPT; making it explicit helps
  readers from a systems background.
- PROPOSE comical illustration **"the SQL-query that revealed too much"** for
  the PII-in-checkpoint warning. The book voice rewards specific anecdotes.

#### Section 27.5 (Tool Use Protocols)

Has Key Insights and practical-example callouts.

- PROPOSE fun-note **"The MCP standard war"** - Model Context Protocol vs.
  OpenAI's function-calling vs. Anthropic's tool-use vs. Google's
  function-calling were 2024's mini-standards-war. The history is worth a
  short anecdote (Anthropic's November 2024 open MCP standard was the catalyst
  that pushed others toward interop). Size: 1 callout.

#### Section 29.1 (Specialized Agents)

Has Key Insight + warning callouts.

- ALREADY HAS the swe-bench narrative. PROPOSE adding a comical illustration
  of **"the agent that reads everything fails"** - the canonical
  navigation-vs-generation insight from this section. Size: 1 illustration.
- PROPOSE counterfactual **"What if SWE-bench had been an end-to-end task
  rather than a localized-edit task?"** - the section names that
  search-first-then-edit wins; the deeper why is that SWE-bench's evaluation
  protocol rewards minimal correct edits, not full-task completion. The
  benchmark shaped the agent design. Connection to **evaluation
  methodology** (the same dynamic as MultiWOZ shaping TOD architecture).

#### Section 29.4 (Specialized Agents Tools)

Has Key Insight, practical-example, warning callouts.

- ALREADY HAS extensive content. PROPOSE adding **mental-map figure** of
  the specialized-agent landscape (code agents / research agents / data
  agents / browser agents) with each labeled by representative vendors
  (Cursor / Cognition / Anthropic Computer Use / etc.).
- PROPOSE fun-note **"The Cursor moat"** - Cursor's 2024 success was not
  the AI; OpenAI / Anthropic both had similar code completion. The moat
  was editor integration, codebase-aware retrieval, and the keyboard
  shortcuts. Cross-field connection to **software ergonomics** (the IDE
  is a product, not just a UI). Size: 1 callout.

#### Section 35.3 (Advanced RAG: query rewriting)

Has Key Insight + fun-note.

- ALREADY good. PROPOSE one cross-field callout **"HyDE is a denoising
  autoencoder"** - Hypothetical Document Embeddings (HyDE) is structurally
  a denoising autoencoder: generate a noisy candidate (hypothetical doc),
  embed it, retrieve the noise-free real document. The autoencoder
  literature (Hinton 2006) provides the theoretical framing. Cross-field
  connection to **representation learning**.

#### Section 35.4 (Advanced RAG: contextual / hierarchical retrieval)

Has Key Insight + fun-note.

- ALREADY good. PROPOSE counterfactual **"What if Anthropic had patented
  contextual retrieval?"** - the September 2024 Anthropic blog post defined
  the technique, then open-sourced the prompt. The strategic choice to
  evangelize rather than patent shaped the adoption curve. Connection to
  **open-source-as-strategy** (same pattern as Llama).

#### Section 37.3 (Conversational memory)

Excellent section already, multiple Key Insights, fun-note, library-shortcut.

- ALREADY engaging. PROPOSE one mental-map figure of **"the memory layer
  cake"** (verbatim window / summary buffer / vector recall / cross-session
  profile / structured facts) showing what each layer does at what time
  scale. The section talks through them sequentially; a single figure
  helps. Size: 1 figure.

### Chapter 34 (Structured IE / NER, Wave 9 promotion)

#### Engagement

- **section-34.1**: PROPOSE fun-note **"Why hybrid won over pure LLM"** - the
  section already says hybrid is the production standard. Add a story: a 2023
  startup pitched pure-LLM extraction at $0.05 per document; investors did the
  math and demanded hybrid. The "always run spaCy first" tip in the section is
  the right pattern but deserves a war story. Size: 1 callout.
- **section-34.1**: PROPOSE comical illustration **"the LLM that invented an
  entity from thin air"** - the canonical hallucination failure mode for IE
  pipelines. Voice match: the book's "I judge everyone who still writes for
  loops" style fits "I judge everyone who still trusts an LLM to extract
  entities without a classical NER baseline".
- **section-34.2**: ALREADY HAS a fun-note + multiple Key Insights. Good.
- **section-34.5**: ALREADY HAS fun-note + Key Insights. Good.

#### "Why" depth

- **section-34.1**: PROPOSE **"Why CRF beats LLM on common entities"** - the
  section's table shows 95% F1 for classical vs 85-92% for LLM zero-shot. The
  why: CRFs are trained on millions of labeled examples of "this is a date";
  LLM zero-shot is one-shot inference. Connection to **classical statistics**
  (sample complexity: parametric models beat in-context learning on tasks
  with abundant labels). Size: 1 paragraph.
- **section-34.2**: PROPOSE counterfactual **"What if we did not have spaCy?"**
  - the section uses spaCy as the canonical classical baseline. The why:
  spaCy's combination of pipeline simplicity + production speed + permissive
  license made it the de facto choice; Stanford CoreNLP and NLTK were
  alternatives but lost on speed and ergonomics. Connection to **the
  Reimers and Gurevych pattern** (the right API beats the right model).
- **section-34.3** (Hybrid IE): the section description already says "Why
  this matters for production pipelines" but the content is implementation
  details. PROPOSE moving the "why hybrid" framing to an explicit "why this
  works" callout at the top. Connection to **classical control theory** (the
  hybrid system as a cascade of a cheap, fast first-stage and an expensive,
  flexible second-stage is the same pattern as PID-plus-MPC in process control).

### Chapter 46 (LLM-as-Judge, Wave 9 promotion)

#### Engagement

- **section-46.1**: ALREADY HAS the canonical "narcissism bias" fun-note. Good.
- PROPOSE chapter-opener illustration: **"GPT-4 grading its own homework"** -
  XKCD-style, the model holding a red pen with its own essay. The narcissism
  bias deserves the image, not just the callout.

#### "Why" depth

- **section-46.1**: ALREADY HAS the bias-taxonomy Key Insight. PROPOSE cross-field
  connection **"Position bias in LLM judges and primacy effects in human
  judging"** - human judges also show position bias (Asch conformity, primacy
  effects in serial position curves). The LLM is reproducing a documented
  human cognitive bias. Cross-field connection to **cognitive psychology**.
  Size: 1 paragraph.

## Cross-cutting recommendations

1. **Establish a "fun-note density floor" of 1-2 per section across Ch 36, 41,
   56, 61.** The reference chapters (Ch 1, 3, 6, 26) average 2-4 fun-notes per
   section; the new tools chapters average 0-1. Pick anecdotes from the recurring
   themes already in the prose (vendor histories, benchmark contamination,
   framework wars, regulatory deadlines) and convert one paragraph per section
   into a callout.

2. **Add one mental-map figure per chapter** in the format of the figure 24.6.1
   and 36.4 candidates above. The new tools chapters all have at least one
   landscape SVG (the platform map), but only Ch 41 has a second decision-axis
   figure (41.2.11). Each chapter should have: (a) the landscape SVG (mostly
   done), (b) a decision-axes figure (mostly missing), (c) a tier / hierarchy
   figure (mostly missing).

3. **Add one cross-field connection per section in the tools chapters.** The
   strongest opportunities, ranked: (i) classical statistics in Ch 36 (BM25 is
   near the Cramer-Rao bound), Ch 46 (judge biases mirror human cognitive
   biases), Ch 56 (Shapley values from cooperative game theory), (ii) distributed
   systems in Ch 36 (the dual-write problem), Ch 41 (memory hierarchy as virtual
   memory), Ch 59 (queueing theory for pipeline bubble), Ch 61 (metadata
   bottlenecks in parallel storage), (iii) control theory in Ch 41 (latency
   budget set by turn-taking psychology), Ch 34 (hybrid IE as cascaded control),
   (iv) information theory in Ch 36 (ColBERT MaxSim as MI lower bound), Ch 36
   (matryoshka as learned PCA), (v) cognitive psychology in Ch 41 (the
   verbatim-plus-gist memory model matches Murdock 1962), Ch 46 (judge biases).

4. **Add "Why X exists" framings systematically** in the tools chapters.
   Every section that lists vendors / libraries / models should answer: why
   does this category exist as a separate thing? What gap did the canonical
   reference fill? What did the prior generation get wrong? Ch 59 (the
   distributed-training chapter) does this well throughout; the tools chapters
   mostly skip it.

5. **Treat the "what if X had been built differently?" counterfactual as a
   standard callout type.** The canonical voice in Ch 26.1 ("LLM-as-agent is
   not just LLM-with-tools") works because it names the easy wrong answer and
   then refutes it. The tools chapters rarely do this; they describe what is
   without describing what is not. The opportunities are abundant: what if
   pgvector did not exist? What if Anthropic owned conversation state? What
   if InfiniBand had not existed? What if Common Crawl had been licensed?

6. **Add at least one chapter-opener / hero image to each of Ch 36, 41, 56, 61.**
   Currently they rely on the platform-landscape SVGs as the visual anchor.
   The older chapters (Ch 1, 3) have iconic hero images that set the tone; the
   new chapters lack them.

7. **Comical illustrations have the highest ROI for engagement.** They are
   cheap (one SVG per chapter) and they cement memorable analogies. The
   priority candidates: vector DB lock-in cat (Ch 36), the four-buyer
   procurement meeting (Ch 56), the framework treadmill (Ch 41), the
   straggler GPU (Ch 59), the model release treadmill (Ch 61).

8. **The Wave 17i sections (24.6, 26.6, 35.2, 35.3, 37.3) are mostly well-done.**
   The largest additions for those are cross-field connection callouts (Multics
   VM in 26.6, HyDE-as-autoencoder in 35.3, primacy effects in 46.1) and one
   anecdote each (the rainbow Frisbee in 24.13, the Cursor moat in 29.4).

9. **The Wave 9 promotions (Ch 34, Ch 46) are short.** Ch 46 in particular is
   only 126 lines for section 46.1; the entire chapter likely needs a content
   density review separate from this engagement audit. The "why" content is
   correct but thin.

10. **Voice consistency: the books canonical voice uses real-world failure
    anecdotes ("I tried this with my coworkers and HR got involved", "the cat
    was unimpressed", "I judge everyone who still writes for loops") and is
    distinctly underrepresented in Ch 36, 41, 56, 61.** A single "voice pass"
    across these four chapters (rewriting 1-2 sentences per section to match
    the canonical tone) is likely the highest-impact single change.
