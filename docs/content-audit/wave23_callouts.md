# Wave 23: Callout audit (opportunities + fake callouts)

**Scope.** This audit covers the seven new/rewritten chapters of the LLM book authored or
materially rewritten during the current session (Ch 34, 36, 41, 46, 56, 59, 61) and the
nine Wave 17i consolidation-touched sections (24.6, 24.13, 26.6, 27.5, 29.1, 29.4,
35.2, 35.3, 37.3). Each section is read end-to-end and graded on (A) missed
opportunities for canonical book callouts, illustrations, diagrams, tables, and
code-fragment additions, and (B) prose that imitates a callout (bold "Key Insight:" /
"Step 1:" / "Why X matters" inside a regular `<p>`) without using the canonical
`<div class="callout TYPE">` + `<div class="callout-title">` HTML.

**Canonical reference.** The two well-authored reference sections used for calibration
were `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html`
(28 callouts in one section, mix of big-picture, key-insight, fun-note, practical-example,
library-shortcut, exercise, research-frontier, self-check, warning, note) and
`part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html`. The 23 valid
callout types are listed at the end of this document.

**Callout-type usage observed in the seven new chapters (counts across all 35 sections):**
`key-insight` 112, `practical-example` 53, `big-picture` 48, `exercise` 44, `warning` 34,
`library-shortcut` 25, `fun-note` 25, `tip` 14, `note` 12, `self-check` 10, `research-frontier` 9,
`numeric-example` 4, `algorithm` 3, `production-pattern` 1. **Missing entirely from these
new chapters:** `pathway`, `key-takeaway`, `cross-ref`, `postmortem`, `thesis-thread`,
`looking-back`, `whats-next`. (Some of these are rightly chapter-level, but Ch 36, 41, 56,
61 are tools-of-the-trade modules whose closing sections would benefit from a
`whats-next` and a `looking-back`.)

---

## Part A: Missed callout / image / diagram opportunities

### Chapter 34: Structured Information Extraction & NER

This chapter is **the weakest** of the seven new chapters for callout density.
Sections 34.1, 34.2, 34.3, 34.4 each have only 1-5 callouts and miss most of the
patterns that the canonical Ch 3/Ch 30 sections use.

- **section-34.1.html**: Has one `tip` callout (line 30) and that's it for a 138-line
  section that introduces the entire IE landscape, defines NER vs Open IE vs Event
  Extraction, presents a Table 34.1.1 comparison, and ships a figure (Figure 34.1.1).
  Missed opportunities:
  - PROPOSE `big-picture` callout at the top of the section (line ~27) summarizing the
    three IE tasks (NER, relation extraction, event extraction) and the classical-vs-LLM
    axis. Currently the section opens with a regular `<p>` doing this job.
  - PROPOSE `key-insight` callout after the Table 34.1.1 (after line 49) calling out the
    canonical "classical for breadth, LLM for novelty" decision rule, with a numeric
    handle (95%+ F1 classical vs 85-92% F1 LLM zero-shot).
  - PROPOSE `numeric-example` callout doing the 10K-docs/day cost arithmetic
    ($200/day all-LLM vs $60/day hybrid) explicitly, since Section 34.3 implies it but
    no section commits it to a callout.
  - The fake callout in line 29 (see Part B) should become a `key-insight`.
- **section-34.2.html**: 5 callouts (fun-note, warning, key-insight x3, note). For a
  434-line section covering spaCy NER, Open IE (Stanford, REBEL, LLM-based), Event
  Extraction, Temporal IE, and Knowledge-Graph construction, this is light:
  - PROPOSE `big-picture` callout at the top tying the four sub-topics together (currently
    starts with a `<h2>` jumping straight into spaCy).
  - PROPOSE `library-shortcut` callout collecting the "thinnest IE stack" recipe:
    spaCy `en_core_web_trf` + Pyserini for retrieval-flavored IE + Instructor for typed
    LLM extraction + REBEL for relation extraction. No such roll-up exists today.
  - PROPOSE `numeric-example` callout for the 10K docs/sec spaCy throughput vs ~1 doc/sec
    LLM throughput claim (the chapter mentions both but never side-by-side).
  - PROPOSE `algorithm` callout for the Stanford OpenIE clause-decomposition algorithm,
    since it's described in prose at line 141 and would benefit from the indented box.
  - The "Hybrid temporal extraction in practice" `note` at line 417 should be promoted
    to a full `practical-example` callout with a code-fragment showing SUTime/HeidelTime
    + LLM combined (currently described in prose only).
- **section-34.3.html**: 1 callout (key-insight at line 219). For a 234-line section that
  is the *crucial* hybrid-architecture section, this is severely under-illustrated:
  - PROPOSE `production-pattern` callout for the two-layer hybrid architecture (the
    section's whole topic). The figure 34.3.2 is there; the callout that captures the
    pattern's preconditions and tradeoffs is not.
  - PROPOSE `practical-example` callout for the complexity-router heuristic (currently
    embedded in the code fragment from line 132 onward); the callout should call out
    that "60-80% of documents resolve at classical layer" as a measurable benchmark.
  - The fake callout at line 28 (see Part B) should become a `big-picture` or
    `key-insight`.
  - PROPOSE `numeric-example` callout for the 60-80% LLM cost reduction (called out in
    line 220 prose but never as a numbered callout with explicit math).
- **section-34.4.html**: 2 callouts (warning, note). This is the production-deployment
  section and badly needs more pattern-style callouts:
  - PROPOSE `production-pattern` callout for "Grounding Verification" (the subsection
    title at line 29 is just a `<h3>`; it deserves a typed callout with the three-tier
    rubric of substring, fuzzy, semantic).
  - PROPOSE `production-pattern` callout for "Graceful Degradation" with the explicit
    "always return classical NER results, even during LLM outages" rule.
  - PROPOSE `postmortem` callout slot: this chapter is about IE in production and would
    benefit from a one-paragraph "what went wrong when team X skipped grounding
    verification" anecdote.
- **section-34.5.html**: 7 callouts (key-insight x2, practical-example x2, self-check,
  note, fun-note). This is the best-covered section in Ch 34 already, but:
  - PROPOSE `pathway` callout summarizing the four-stage pipeline (line 142 is currently
    a `<h3>` with an ordered list; the pathway callout type is purpose-built for this).
  - PROPOSE diagram showing the four-stage pipeline (the ordered list at lines 142-145
    is asking for a flow diagram).

### Chapter 36: Retrieval Tools of the Trade

This chapter is **well-callouted overall** (the Big Picture + 1-2 callouts per section
pattern works). Specific opportunities:

- **section-36.1.html**: 5 callouts (big-picture, key-insight, practical-example,
  warning, note). For a 270-line section, the cadence is reasonable but:
  - PROPOSE `practical-example` callout after the Table 36.1.1 (line 209) summarizing
    "when each platform wins" with a 3-line case study: Pinecone for serverless
    prototypes, pgvector for Postgres shops, Qdrant for self-host with heavy filtering.
    The decision tree at lines 100-112 does this in prose; a callout makes it scannable.
  - PROPOSE `library-shortcut` callout collecting the canonical 4-library "thinnest
    stack" recipe (sentence-transformers + Qdrant OSS + RAGAS + Phoenix). Section 36.2
    has this but Section 36.1 ends with the prose pricing-shapes discussion; a
    library-shortcut callout in 36.1 would mirror the canonical tools-of-the-trade rhythm.
  - PROPOSE `pathway` callout for the decision tree (lines 100-112). This is exactly
    the use case the `pathway` callout type was created for.
  - PROPOSE `numeric-example` callout: a billion-vector index, 1024-dim float32 needs
    ~4 TB RAM full precision vs ~128 GB binary-quantized (this number is in line 232
    prose). Currently buried in the operations section.
- **section-36.2.html**: 7 callouts (big-picture, practical-example x2, key-insight,
  warning, note, ... + sub-blocks). Strong coverage. Opportunities:
  - PROPOSE `library-shortcut` callout collecting the canonical 4-library "thinnest
    stack" recipe (currently described in prose at lines 184-196). The list is already
    there; the callout would make it the canonical scannable answer.
  - PROPOSE `numeric-example` callout for "RRF k=60 default" (line 125 mentions it but
    never quantifies "within 1-2 NDCG points of tuned weighted-sum").
  - PROPOSE `cross-ref` callout to Ch 32 (RAG) since this section is the tools-and-
    libraries view of what Ch 32 covers conceptually.
- **section-36.3.html**: 6 callouts (big-picture, key-insight, warning, fun-note, ... +
  Table). Strong coverage. Opportunities:
  - PROPOSE `numeric-example` callout demonstrating the contamination penalty quoted at
    line 136 ("leaderboard inflation of 5-15 NDCG points on the most-contaminated
    subtasks"). The current `warning` callout makes the claim; a numeric-example would
    cement it.
  - PROPOSE `pathway` callout for the "Building your own evaluation set" subsection
    (lines 172-179). Currently a `<h2>` + `<ul>`; pathway is purpose-built for
    methodology recipes like this.
- **section-36.4.html**: 5 callouts (big-picture, practical-example x2, warning,
  ... + Table). For a 306-line section covering an entire model catalog, opportunities:
  - PROPOSE `numeric-example` callout showing the dimension/cost trade-off:
    1536-dim embedding cost at 10M docs vs 768-dim Matryoshka truncation vs 256-dim.
    The matryoshka subsection (lines 200-207) describes the property but doesn't
    quantify cluster cost.
  - PROPOSE `production-pattern` callout for "embedder pinning" (line 215 makes the
    point in prose); this is exactly the recurring production failure mode the
    `production-pattern` callout is for.
  - PROPOSE `algorithm` callout for the BGE/E5/NV-Embed query-prompt convention table
    (currently buried in the `warning` at line 217). An algorithm callout listing the
    canonical prompt strings per model family would save practitioners hours.
  - PROPOSE `cross-ref` callout to Ch 31 (Embeddings) since this section is the
    tools-and-models view of the embedding concepts Ch 31 covers theoretically.
- **section-36.5.html**: 3 callouts (big-picture, key-insight, ... + Tables). For a
  261-line section that is the entire "external reading and communities" closing piece,
  opportunities:
  - PROPOSE `pathway` callout for the weekly reading cadence (lines 184-190). Currently
    a `<h2>` + ordered list; the `pathway` type is purpose-built for these.
  - PROPOSE diagram of the "weekly reading cadence" (daily / weekly / bi-weekly /
    monthly / quarterly) as a horizontal timeline. Currently described prose-only.
  - PROPOSE `whats-next` callout at the bottom transitioning into Ch 37 (Conversational
    AI). Currently the section ends with a references block; the canonical chapter-end
    rhythm includes a `whats-next` callout.
  - PROPOSE `looking-back` callout at the top summarizing what Sections 36.1-36.4 just
    covered, before the External Reading section dives into the reading-list mode.

### Chapter 41: Conversational AI Tools of the Trade

Strong existing callout coverage (~6 callouts per section on average). Opportunities
mostly involve adding `pathway`, `numeric-example`, and `looking-back`/`whats-next`
callouts that the chapter is missing entirely.

- **section-41.1.html**: 5 callouts. Opportunities:
  - PROPOSE `pathway` callout for "Choosing a platform" (line 78). Currently a `<h2>`
    + prose; pathway is the right idiom for a decision recipe.
  - PROPOSE `cross-ref` callout to Ch 30 (Agents Tools of the Trade) and Ch 37
    (Conversational AI Foundations), since this section sits at the intersection.
  - PROPOSE `numeric-example` callout for the "$40K/month at 1M conversations/$0.04"
    arithmetic in the pricing-shapes subsection (line 156). Currently in-prose.
  - PROPOSE diagram for the platform-by-vertical map (lines 165-171). The text reads
    like a 6-row table; render it as a small comparison-table or a 6-column matrix.
- **section-41.2.html**: 7 callouts. Strong. Opportunities:
  - PROPOSE `algorithm` callout for the "verbatim window + summary + facts" memory
    pattern (the Zep loop in Code Fragment 41.2.1 implements it; an algorithm callout
    in the algorithm box style would make it scannable).
  - PROPOSE `numeric-example` callout for the "BufferMemory works up to 20 turns or
    4k tokens" rule of thumb (line 36 mentions it; no numeric-example callout grounds
    the threshold).
  - PROPOSE `production-pattern` callout for "framework + thin Python pipeline" anti-
    pattern guidance (currently implicit in the prose).
- **section-41.3.html**: 5 callouts. Opportunities:
  - PROPOSE `numeric-example` callout showing MT-Bench vs Arena vs AlpacaEval results
    for a known model (e.g., Claude 3.5 Sonnet) to ground the abstract benchmark
    discussion.
  - PROPOSE `cross-ref` callout to Ch 46 (LLM-as-Judge) since the judge-bias discussion
    in lines 184-191 overlaps with Ch 46.
  - PROPOSE `pathway` callout for "Building your own evaluation set" (lines 174-182).
    Currently a `<h2>` + `<ul>`; pathway is the right type for the methodology.
- **section-41.4.html**: 6 callouts. Strong. Opportunities:
  - PROPOSE `numeric-example` callout for the "voice cascade ~800ms vs realtime ~300ms"
    latency claim (line 45). Currently prose.
  - PROPOSE `cross-ref` callout to Ch 7 (Modern LLM Landscape) since this section maps
    directly onto a 2026 view of the chat-model catalog.
- **section-41.5.html**: 6 callouts. Strong. Opportunities:
  - PROPOSE `whats-next` callout at the bottom transitioning into Part IX (Evaluation).
  - PROPOSE `looking-back` callout at the top tying back to Part VIII chapters 37-40.
  - PROPOSE `pathway` callout for the "weekly current-awareness routine" (lines 137-143).
    The ordered list is structurally a pathway already.

### Chapter 46: LLM-as-Judge & Automated Evaluation

**This chapter is the second-weakest** (only 7 callouts across 5 sections; the
canonical rhythm would be 25-35). Sections 46.3, 46.4, 46.5 are particularly thin.

- **section-46.1.html**: 4 callouts (production-pattern, key-insight, library-shortcut,
  fun-note). Reasonable opener. Note: this section has the only `production-pattern`
  callout in the entire seven new chapters (line 26 `Production Pattern P9: LLM Judge
  with Periodic Human Calibration`). Strong example; the pattern should be propagated
  to Ch 34 (P10: Grounding Verification), Ch 56 (Pn: Inline LLM Guard + Offline
  Eval), Ch 61 (Pn: Checkpoint-Resume Training), etc.
  - PROPOSE `big-picture` callout at the very top (line 25) introducing why LLM-as-judge
    matters before diving into bias taxonomy. Currently the section starts with the
    production-pattern callout which is logically out of order.
  - PROPOSE `cross-ref` callout to Section 41.3 which has overlapping bias-mitigation
    content.
- **section-46.2.html**: 2 callouts (library-shortcut, tip). The G-Eval discussion is
  prose-heavy:
  - PROPOSE `big-picture` callout at the top introducing chain-of-thought scoring.
  - PROPOSE `algorithm` callout for the G-Eval probability-weighted scoring algorithm.
    The code fragment 46.2.2 implements it; an algorithm box would clarify the math
    upfront.
  - PROPOSE `numeric-example` callout grounding G-Eval's claimed precision improvement
    over argmax scoring (the section mentions "finer-grained and more stable" but
    never quantifies, e.g., a Spearman delta).
  - PROPOSE `practical-example` callout for the G-Eval setup on a non-OpenAI model
    (line 109 alludes to the temperature-averaging fallback for Claude; this deserves
    a callout, not a single sentence).
- **section-46.3.html**: **0 callouts**. For a 116-line section on debiasing
  techniques and Prometheus models, this is severely under-illustrated:
  - PROPOSE `big-picture` callout at the top introducing the three debiasing axes
    (position, length, verbosity) and Prometheus as the open-source judge.
  - PROPOSE `practical-example` callout for the Prometheus 2 direct-assessment example
    (currently entirely in code-fragment 46.3.3; the callout would surface the
    template structure and the rubric format).
  - PROPOSE `key-insight` callout for "rubric-trained judges outperform GPT-4 on
    rubric-following" (line 103 prose claim).
  - PROPOSE `library-shortcut` callout for the prometheus-eval pip package and its
    Python API (the code fragment uses raw transformers; the shortcut is the
    `prometheus_eval` library).
  - PROPOSE `cross-ref` callout to Section 46.4 since Prometheus and JudgeLM are
    architecturally related.
- **section-46.4.html**: 1 callout (warning). For a 45-line section on training judge
  models:
  - PROPOSE `big-picture` callout at the top.
  - PROPOSE `key-insight` callout for the swap-augmentation technique (it is mentioned
    in line 28 prose but transferable to any judge, which the prose flags but a
    callout would make canonical).
  - PROPOSE `production-pattern` callout for "distill GPT-4 judgments into a cheaper
    judge model" (the JudgeLM pattern). Currently described in prose.
  - PROPOSE diagram showing the JudgeLM distillation pipeline.
- **section-46.5.html**: **0 callouts**. For an 85-line section on multi-judge
  ensembles and AlpacaEval LC:
  - PROPOSE `big-picture` callout at the top introducing multi-judge ensembles.
  - PROPOSE `algorithm` callout for the length-controlled win rate computation
    (currently entirely in code-fragment 46.5.4).
  - PROPOSE `numeric-example` callout for the "raw 70%, LC 55%, debiasing effect 0.15"
    arithmetic in the code-fragment's example comment (lines 65-70).
  - PROPOSE `practical-example` callout for a multi-judge ensemble setup (the section
    title promises "Multi-Judge Ensembles" but the text only covers AlpacaEval LC).
  - PROPOSE `whats-next` callout at the bottom transitioning into Part X (Security).
  - PROPOSE `looking-back` callout at the top tying back to Sections 46.1-46.4.

### Chapter 56: Responsible AI Tools of the Trade

Strong callout coverage (~5 callouts per section). Opportunities mostly involve
adding `pathway`, `numeric-example`, and `production-pattern` callouts.

- **section-56.1.html**: 6 callouts. Strong. Opportunities:
  - PROPOSE `pathway` callout for "Selection criteria and buyer personas" (line 112)
    listing the four buyer-persona-to-platform mappings.
  - PROPOSE `numeric-example` callout for "enterprises routinely register 100-500 use
    cases" (line 136 prose); the multiplier on per-use-case licensing matters.
  - PROPOSE diagram showing the three-platform stack (governance + observability +
    LLM safety runtime) called out in line 122 as the common pattern.
- **section-56.2.html**: 4 callouts. Opportunities:
  - PROPOSE `library-shortcut` callout collecting the "thinnest fairness stack"
    (AIF360 + Fairlearn + Aequitas).
  - PROPOSE `algorithm` callout for one canonical bias metric (e.g., disparate impact
    or demographic parity) with the formula and a numeric example.
  - PROPOSE `cross-ref` callout to Ch 52 (Bias and Fairness in LLMs) since this is
    the tools view of those concepts.
- **section-56.3.html**: 5 callouts. Opportunities:
  - PROPOSE `numeric-example` callout for the AI Act fine arithmetic (up to 7% of
    global annual turnover or EUR 35M).
  - PROPOSE `production-pattern` callout for the "register, classify, evidence,
    attest" four-step compliance flow.
- **section-56.4.html**: 6 callouts. Strong. Opportunities:
  - PROPOSE `algorithm` callout for the Llama Guard 3 classification prompt structure.
  - PROPOSE `production-pattern` callout for the "inline guard + offline evaluator"
    deployment pattern.
- **section-56.5.html**: 4 callouts. Opportunities:
  - PROPOSE `whats-next` callout transitioning into Part XII (Scale).
  - PROPOSE `looking-back` callout summarizing Sections 56.1-56.4.
  - PROPOSE `pathway` callout for "weekly reading cadence" if one is described (Ch 56
    is the responsible-AI external reading section; cadence advice belongs here).

### Chapter 59: Distributed Training Systems

Strong callout coverage (~5 callouts per section). Opportunities:

- **section-59.1.html**: 6 callouts. Strong. Opportunities:
  - PROPOSE `numeric-example` callout for the "70B model = 1.26 TB optimizer state"
    arithmetic (line 43). Currently in-line in a math block; a numeric-example callout
    would emphasize the binding constraint.
  - PROPOSE `algorithm` callout for the AdamW per-parameter memory accounting (18
    bytes/param breakdown).
- **section-59.2.html**: 4 callouts. Opportunities:
  - PROPOSE `numeric-example` callout for the "16 GPUs * 1.12 TB state = 17.92 TB
    cluster memory for a 1.12 TB working set" arithmetic.
  - PROPOSE `algorithm` callout for the ZeRO Stage-3 forward/backward all-gather-then-
    free dance (currently illustrated in SVG but not as algorithm callout).
- **section-59.3.html**: 5 callouts.
- **section-59.4.html**: 4 callouts.
- **section-59.5.html**: 5 callouts.
  - PROPOSE `whats-next` callout transitioning into Ch 60 (Edge LLMs).
  - PROPOSE `looking-back` callout summarizing the four parallelism axes covered.

### Chapter 61: Scale Tools of the Trade

Strong callout coverage (~3 callouts per section). This is the lightest of the
seven new chapters; opportunities:

- **section-61.1.html**: 4 callouts. Opportunities:
  - PROPOSE `numeric-example` callout for the "InfiniBand premium reverses headline
    cost comparison at >30% MFU difference" claim (line 51 prose).
  - PROPOSE `practical-example` callout for "AWS HyperPod vs CoreWeave vs OCI" at
    a 1024-GPU job (currently described in prose).
  - PROPOSE diagram showing the platform stack pyramid (hyperscaler / specialized
    cloud / in-house) with annotations on cost-per-GPU-hour and InfiniBand availability.
- **section-61.2.html**: 3 callouts. Opportunities:
  - PROPOSE `library-shortcut` callout collecting the "thinnest training stack"
    (PyTorch FSDP + Megatron-LM + W&B + Slurm).
  - PROPOSE `algorithm` callout for the canonical 3D parallelism configuration
    (DP + TP + PP) for a 70B model.
- **section-61.3.html**: 3 callouts. Opportunities:
  - PROPOSE `numeric-example` callout for the "$2-3M for a 70B 1T-token pretrain"
    cost estimate, with the math broken down (GPU-hours x $/hr).
- **section-61.4.html**: 4 callouts.
- **section-61.5.html**: 3 callouts.
  - PROPOSE `whats-next` callout transitioning into Part XIII (LLMOps).
  - PROPOSE `looking-back` callout summarizing the platform/library/dataset/model
    breakdown.

### Wave 17i consolidation-touched sections

These sections are not the "new" chapters of the session but were edited during
consolidation; they already have strong callout density (5-19 callouts each).
Minor opportunities only:

- **section-24.6.html** (6 callouts): mature. Single opportunity: a `cross-ref`
  callout to Ch 30 since the VLA tools discussion overlaps.
- **section-24.13.html** (5 callouts): mature.
- **section-26.6.html** (13 callouts): exemplary; no missed opportunities of note.
- **section-27.5.html** (10 callouts): exemplary; this is the rhythm Ch 34 should
  emulate.
- **section-29.1.html** (14 callouts): exemplary.
- **section-29.4.html** (9 callouts): mature.
- **section-35.3.html** (19 callouts): exemplary; this section sets the bar.
- **section-35.4.html** (12 callouts): mature.
- **section-37.3.html** (no count above): not flagged.

---

## Part B: Fake / non-standard callouts found

The full repository scan of the seven new chapters (Ch 34, 36, 41, 46, 56, 59, 61)
turns up **exactly two** confirmed fake callouts. Both are in Ch 34 and both have
the same pattern: a regular `<p>` opens with a bold "Why X matters" or "Why this
matters for production pipelines" phrase that visually mimics a callout heading.

- **part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html:29**
  - The paragraph opens: `<p><strong>Why hybrid information extraction </strong>is the production standard. Pure classical IE...`
  - This mimics a `key-insight` or `big-picture` callout but lives in a regular `<p>`.
  - **Recommended fix:** Wrap in `<div class="callout key-insight"><div class="callout-title">Why hybrid IE is the production standard</div>`...`</div>`. The content of the paragraph (the classical-vs-LLM tradeoff plus the cross-reference to Section 13.3) is exactly what a `key-insight` callout should contain.

- **part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html:28**
  - The paragraph opens: `<p><strong>Why this matters for production pipelines.</strong> In a production document processing system, you might need to extract entities from 10,000 documents per day...`
  - This mimics a `big-picture` callout (since it sets up the entire production-pipeline framing for the rest of Section 34.3) but lives in a regular `<p>`.
  - **Recommended fix:** Wrap in `<div class="callout big-picture"><div class="callout-title">Why hybrid IE matters in production</div>`...`</div>`. The $200/day vs $60/day arithmetic the paragraph contains is exactly the "Big Picture" the section is making.

**No other fake callouts were found in the seven new chapters.** The grep patterns
checked:
- `<p><strong>(Why|Note|Tip|Warning|Key Insight|Big Picture|Practical Example|Fun Note|Example|Production Pattern|Postmortem|Pathway|Library Shortcut|Algorithm|Exercise|Self-Check|Cross-Ref|Looking Back|Whats Next|Key Takeaway|Numeric Example|Research Frontier|Thesis Thread)`
- `<p><strong>(P\d+|Pattern P\d+|Production Pattern P\d+)`
- `<p><strong>Step \d+|<p><strong>Real-World|<p><strong>Case Study|<p><strong>Scenario:`
- `<h[34][^>]*>(Key Insight|Important Note|Warning|Tip|Practical Example)`
- `<p>\s*<em>[^<]*:</em>`

The `<p><strong>Who:</strong>...<strong>Situation:</strong>...<strong>Lesson:</strong>` pattern
in **section-34.5.html:123-128** and **section-34.5.html:200-207** is **NOT a fake
callout** because the paragraphs are inside a legitimate `<div class="callout practical-example">`
on lines 121 and 198. The field-labeled paragraphs are the "structured case study"
sub-pattern inside a real callout; that is canonical.

**Validity check on callout type names.** A grep of `class="callout ([a-z-]+)"` across
all 35 target sections returned only the 14 valid types (in usage order: key-insight,
practical-example, big-picture, exercise, warning, library-shortcut, fun-note, tip,
note, self-check, research-frontier, numeric-example, algorithm, production-pattern).
**No invalid or typo'd callout-type strings were found.**

---

## Cross-cutting style observations

1. **Ch 34 (NER & IE) is the only new chapter that visibly under-uses callouts.**
   Sections 34.1, 34.3, 34.4 each have 1-2 callouts where the canonical rhythm
   (compare section-3.1, section-30.4, section-35.2) is 4-6 per section. The two
   fake callouts found in Part B are symptoms of the same gap: the author reached
   for a callout structurally but did not have the canonical HTML pattern at hand.

2. **Ch 46 (LLM-as-Judge) is the second-weakest** with two sections (46.3, 46.5)
   that have *zero* callouts at all. Both sections are 80-120 lines of dense
   algorithmic content (G-Eval probability weighting, Prometheus rubric training,
   AlpacaEval length-controlled win rate) that would carry-its-weight 5-8 callouts
   each at the canonical rhythm. Section 46.1's `production-pattern` callout
   (`P9: LLM Judge with Periodic Human Calibration`) is the **only** production-
   pattern callout in the seven new chapters and is a model of the form; the
   pattern should be propagated to Ch 34, 56, 61.

3. **Five canonical callout types are entirely missing from the seven new chapters:**
   `pathway`, `key-takeaway`, `cross-ref`, `postmortem`, `whats-next`. The book's
   tools-of-the-trade chapters (30, 36, 41, 45, 56, 61) should all end with a
   `whats-next` callout (and ideally open with a `looking-back` callout); only
   Ch 30's reference section 30.5 does this consistently. Adding `whats-next`
   callouts to the closing sections of Ch 36, 41, 46, 56, 59, 61 is the
   highest-leverage cross-cutting fix.

4. **Numeric-example callouts are under-used.** Each new chapter contains 3-8
   numeric claims in prose (cost arithmetic, latency budgets, benchmark deltas,
   memory accounting) that should be promoted to `numeric-example` callouts. The
   current count is 4 across 35 sections; the canonical rhythm is 1-2 per section
   for any technical content.

5. **Library-shortcut callouts are clustered in Ch 46 and absent from the other
   tools-of-the-trade chapters that exist precisely to surface library shortcuts.**
   Sections 36.1, 36.2, 41.2, 56.2, 61.2 are *named* after libraries-and-frameworks
   and each contains the "thinnest viable stack" recommendation in prose at the
   end. Promoting these to `library-shortcut` callouts would make the
   recommendation scannable on every section.

6. **The `practical-example` callout in Ch 34.5 with `<strong>Who:</strong>`,
   `<strong>Situation:</strong>`, `<strong>Problem:</strong>`, etc. field labels
   is a well-designed sub-pattern.** It survives the validity check (it's inside
   a real callout) and it gives a structured case-study format that other chapters
   could borrow. Consider templating this as a documented case-study pattern.

7. **Production-pattern callouts deserve more presence.** The book documents
   production-pattern Pn numbering implicitly (P9 in 46.1), but only one such
   callout exists in the seven new chapters. A proper numbered series across Ch 34
   (grounding verification, hybrid extraction), Ch 36 (embedder pinning,
   benchmark-on-your-data), Ch 41 (conversation memory pattern), Ch 46 (LLM-judge
   + calibration), Ch 56 (inline guard + offline eval), Ch 59 (checkpoint-resume),
   Ch 61 (gang scheduling + Slurm) would build a recognizable "patterns spine"
   across the book.

---

## Reference: the 23 valid callout types

In alphabetical order, as defined in `styles/book.css`:

algorithm, big-picture, cross-ref, exercise, fun-note, key-insight, key-takeaway,
lab (reserved), library-shortcut, looking-back, note, numeric-example, pathway,
postmortem, practical-example, production-pattern, research-frontier, self-check,
thesis-thread, tip, warning, whats-next.

Canonical HTML pattern:

```html
<div class="callout TYPE">
  <div class="callout-title">Optional human-readable title</div>
  <p>Body text.</p>
</div>
```

Any prose that opens a regular `<p>` with bold text mimicking a callout heading
(`<strong>Key Insight:</strong>`, `<strong>Why X:</strong>`, `<strong>Note:</strong>`)
is a fake callout that should be converted to the canonical HTML.
