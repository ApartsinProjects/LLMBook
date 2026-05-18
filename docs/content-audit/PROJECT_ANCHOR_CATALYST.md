# Project Anchor Catalyst Report

**Agent**: 23-project-catalyst (cycle 1, scout pass)
**Branch**: v2.0
**Date**: 2026-05-18
**Status**: Scout-only. No HTML edited this round.

## Premise

A "project anchor" is a small, end-of-chapter mini-project callout that turns
a multi-section concept chapter into a hands-on build. Across 82 chapter
`index.html` files, only 5 currently mention a project, lab, capstone or
exercise in their bottom-of-chapter content, and none of them use a canonical
`callout hands-on` block on the chapter index page. The other 77 chapters end
in a section-card list immediately followed by `<div class="whats-next">`,
which means the reader closes a hands-on topic (RAG, agents, fine-tuning,
eval) without ever being told "now go build this end-to-end".

There is already a `/capstone/` directory at the back of the book with an
ambitious 4-to-6 week capstone project. The gap this report addresses is the
missing **bridge between a chapter and the capstone**: short, 1-to-4-hour
mini-projects that anchor a single chapter's multi-section material.

## Scouting Method

1. Listed all `part-*/module-*/index.html` files (82 chapters).
2. Grepped for project/lab/exercise/build/capstone/homework keywords in
   chapter index pages.
3. For each candidate, inspected sections list, learning objectives,
   prerequisites, and the size and shape of the topic to decide whether a
   project anchor would land naturally.
4. Ranked candidates by **pedagogical payoff** (does adding a project anchor
   produce a portfolio-worthy build that uses multiple sections?), gated by
   feasibility (can a reader actually finish it in 1-4 hours with the
   chapter's tools?).
5. Skipped "Tools of the Trade" chapters and pure-survey chapters
   (frontier theory, frontier architectures, AGI trajectories, industry
   case studies, ethics/regulation/compliance) as low-payoff for a build
   anchor. They are better served by reflection or research prompts.

## Existing Coverage (Baseline)

Chapters that already mention a project-shape element on their index page:

- `part-14-designing-llm-agent-products/module-70-shipping-products` (mentions a capstone lab in prose, not a callout)
- `part-14-designing-llm-agent-products/module-69-llm-economics` (none in callout form)
- `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner` (mentions "capstone" in the chapter overview prose, not a callout)
- `part-2-understanding-llms/module-06-pretraining-scaling-laws` (passing mention)
- `part-15-applications-of-llms-across-industries/module-75-education-llms` (passing mention)
- `part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories` (passing mention)

No chapter index page currently uses a `callout hands-on` block to anchor a
project at the end of the chapter. That is the gap.

The CSS class is already approved per `CONTENT_GUIDELINES.md` §8.7:
`callout hands-on` with title text "Hands-On".

## Insertion Point Pattern

All chapter index pages share this bottom structure:

```html
</ul>                              <!-- end of sections-list -->
<div class="whats-next">           <!-- INSERT BEFORE THIS -->
  <h3>What's Next?</h3>
  ...
</div>
<nav class="chapter-nav"> ... </nav>
```

The recommended insertion is a single `<div class="callout hands-on">` block
placed immediately after the closing `</ul>` of `sections-list` and
immediately before `<div class="whats-next">`. This keeps the reader on the
chapter page just long enough to see the build, then funnels them forward.

---

## Part 1: Full Ranked Candidate List

Top 15 chapters where a project anchor would have the highest pedagogical
payoff (ranked by combined criteria: hands-on payoff, multi-section
integration, portfolio value, and reader excitement).

| Rank | Module | Chapter Title | Why Ranked Here |
|---|---|---|---|
| 1 | 32 | RAG Fundamentals | 4 sections (foundations, indexing, agentic, text-to-SQL); the canonical end-to-end build in modern LLM engineering; portfolio-killer if completed. |
| 2 | 26 | AI Agent Foundations | 6 sections covering loop, planning, reasoning, eval, deployment, memory. Reader can ship a research agent. |
| 3 | 17 | Parameter-Efficient Fine-Tuning, Distillation & Model Merging | LoRA/QLoRA section, training platforms, soft prompts, distillation. End-to-end "fine-tune Llama-3 in a Colab" is the iconic ML build. |
| 4 | 46 | LLM-as-Judge & Automated Evaluation | 5 sections: judge prompts, bias, debiasing, training judges, ensembles. Pairs naturally with the RAG project from Module 32. |
| 5 | 37 | Building Conversational AI Systems | 6 sections covering architecture, persona, memory, multi-turn. End-to-end chatbot is the hands-on classic. |
| 6 | 27 | Tool Use, Function Calling & Protocols | 6 sections (function calling, MCP, A2A, custom tools, retrieval-as-tool, orchestration). Reader can build their first MCP-enabled assistant. |
| 7 | 31 | Embeddings, Vector Databases & Semantic Search | 7 sections from embeddings to FAISS to chunking. Project: build a semantic search engine over a personal corpus. |
| 8 | 12 | Prompt Engineering & Advanced Techniques | 5 sections from foundational design to automated optimization (DSPy). End with "build a DSPy-optimized chain". |
| 9 | 15 | Synthetic Data Generation & LLM Simulation | 7 sections covering pipelines, QA, labeling, weak supervision, synthetic reasoning. End: build a synthetic dataset and train a baseline classifier on it. |
| 10 | 35 | Advanced RAG: Knowledge Graphs, Ingestion & Frameworks | Builds on Module 32; project: add knowledge-graph retrieval to the Module 32 RAG. |
| 11 | 28 | Multi-Agent Systems | 4 sections: framework landscape, architecture, HITL, testing. Project: build a 2-agent debate or supervisor-worker system. |
| 12 | 34 | Structured Information Extraction & NER | 5 sections; hybrid spaCy+LLM pipeline already framed as a capstone in prose. Project: extract structured data from a public corpus. |
| 13 | 18 | Alignment: RLHF, DPO & Preference Tuning | DPO is the most accessible alignment build a reader can run on a 6GB GPU. Project: DPO-tune a small model on a preference dataset. |
| 14 | 16 | Fine-Tuning Fundamentals | SFT, data prep, provider APIs. Project: fine-tune a small model on a domain task via OpenAI/Together API. |
| 15 | 44 | Online Evaluation, Observability, and Production Monitoring | Dashboards, drift, model rotation. Project: instrument the RAG/agent from Modules 32 or 26 with W&B/Langfuse. |

### Honorable mentions (also strong, but slightly lower payoff or harder feasibility for a 1-4 hour build):

- Module 09 (Inference Optimization) - benchmark vLLM vs. transformers locally
- Module 11 (LLM APIs) - build a provider-agnostic LiteLLM client
- Module 13 (Hybrid ML/LLM) - LLM-as-feature-extractor classifier
- Module 21 (Document Understanding) - VLM-based PDF-to-JSON pipeline
- Module 22 (Vision-Language Models) - LLaVA-style image captioner on Colab
- Module 40 (Voice & Realtime) - GPT-4o Realtime voice agent
- Module 42 (Evaluation Foundations) - pytest-style eval harness
- Module 47 (Adversarial Security) - red-team your own RAG using PyRIT
- Module 48 (Guardrails) - layered guardrail stack with NeMo Guardrails

---

## Part 2: Detailed Project Specs (Top 5)

Each spec below is ready to be turned into a `<div class="callout hands-on">`
block on the chapter's index page. Wording avoids em-dashes and double dashes
per global style rules.

---

### Spec 1 (Module 32: RAG Fundamentals)

**Project name**: Build a Q&A bot over a documentation site you actually use

**Goal (1 paragraph)**:
Pick a documentation site you read regularly (FastAPI, PyTorch, your
employer's wiki) and build a retrieval-augmented Q&A bot over it. By the
end you will have a working RAG pipeline that ingests a real corpus,
indexes it in a vector store, answers natural-language questions with
source citations, and recovers gracefully when the retrieved chunks are
weak. This project is the canonical RAG build and pulls in every
section of the chapter.

**Steps**:
1. Scrape or download a documentation corpus (use `sitemap.xml` plus
   `httpx`, or git-clone a docs repo). Aim for 200 to 2,000 pages.
2. Build an ingestion pipeline (Section 32.1a): chunk with
   `RecursiveCharacterTextSplitter` (target ~500 tokens with 80 overlap),
   embed with `text-embedding-3-small` or `bge-small-en-v1.5`, store in
   Chroma or FAISS.
3. Implement a baseline retriever (top-5 cosine) and add a cross-encoder
   reranker (`bge-reranker-base`) so you can compare retrieval quality
   before and after.
4. Wire the retrieved chunks into a prompt that asks for an answer **with
   inline source citations** (Section 32.4) and prints "I do not know" if
   the top score falls below a threshold.
5. Evaluate (Section 32.1b): hand-write 20 ground-truth Q&A pairs; compute
   answer-correctness (LLM-as-judge) and retrieval recall@5; log results.
6. Stretch goal: swap in HyDE (Section 32.2) for ambiguous queries and
   compare against the baseline.

**Expected outcome**:
A working command-line or Streamlit Q&A bot that answers questions about
your chosen documentation, prints `[source: page.html]` citations, and
reports its accuracy on your eval set. You will have first-hand experience
with every concept in the chapter.

**Difficulty**: weekend (6 to 10 hours).

---

### Spec 2 (Module 26: AI Agent Foundations)

**Project name**: Build a research agent that answers questions about any
Wikipedia article

**Goal**:
Build a Wikipedia research agent that, given a query, plans a small set
of sub-questions, fetches the relevant Wikipedia article, reads it in
chunks, and synthesizes a grounded answer with citations. This is the
smallest meaningful agent that exercises the ReAct loop, planning, tool
use, evaluation, and memory in one project.

**Steps**:
1. Implement the core ReAct loop (Section 26.1): `Thought -> Action ->
   Observation` with a single tool, `wikipedia_search(query)` that returns
   the top 3 article snippets.
2. Add a planner (Section 26.2) that decomposes a complex query like
   "Why did the Roman Empire fall?" into 3 sub-questions before any tool
   call.
3. Add a `wikipedia_fetch(title)` tool that returns the full article and
   a chunker so the agent can read it in pieces (Section 26.5).
4. Add the agent's plan memory (Section 26.6): keep a running log of
   what has been searched, what has been read, and what is still open.
5. Add an evaluator (Section 26.4): pass the final answer to an LLM judge
   that scores groundedness and completeness against the sub-questions.
6. Stretch goal: swap the planner LLM for a reasoning model (Section 26.3)
   and compare the action trace length and answer quality.

**Expected outcome**:
A CLI agent that takes a question, traces its plan in real time, fetches
2 to 5 Wikipedia articles, and produces a 200-word answer with citations
and a self-rated confidence score. The trace will read like a small
research notebook.

**Difficulty**: weekend (4 to 8 hours).

---

### Spec 3 (Module 17: Parameter-Efficient Fine-Tuning)

**Project name**: Fine-tune Llama-3.2-3B as a writing-style mimic in a free
Colab T4

**Goal**:
Pick an author whose distinctive style you can collect (Hemingway,
Vonnegut, Borges, or anyone with substantial public-domain text) and
fine-tune Llama-3.2-3B with QLoRA so that it rewrites neutral prose in
that author's voice. This project uses LoRA, training platforms, multi-
adapter inference, and merging, in a single end-to-end loop that runs in
a free Colab T4.

**Steps**:
1. Build a dataset (Section 17.1): collect 100 to 500 paragraphs of the
   target author. For each, ask a strong LLM (GPT-4o or Claude) to
   produce a "neutralized" paraphrase. The training pair is
   `(neutralized -> author-style)`.
2. Set up the training environment (Section 17.3): Colab T4, Unsloth's
   `FastLanguageModel.get_peft_model`, 4-bit QLoRA, rank 16, alpha 32.
3. Train (Section 17.1): 2 to 3 epochs, 2 to 4 hours wall-clock on a T4.
   Log loss curves to W&B.
4. Sample (Section 17.1): pick 10 neutral sentences, generate the
   author-style rewrite from both the base model and the fine-tuned
   adapter; print them side by side.
5. Optionally merge the adapter back into the base model (Section 17.5)
   and push to Hugging Face Hub.
6. Stretch goal: train a second adapter for a different author and serve
   both with LoRAX or S-LoRA (Section 17.1) so the same base model can
   produce either voice via an adapter-routing header.

**Expected outcome**:
A LoRA adapter on Hugging Face that, when applied to Llama-3.2-3B,
produces noticeably author-flavored rewrites. You will have run a full
fine-tuning cycle on a free GPU and understand exactly which knobs change
loss curves.

**Difficulty**: weekend (one Colab session plus an afternoon of dataset
prep).

---

### Spec 4 (Module 46: LLM-as-Judge & Automated Evaluation)

**Project name**: Score the RAG bot from Module 32 with a debiased
multi-judge panel

**Goal**:
Take the Q&A bot you built in Module 32 (or any answer-generating LLM
system) and score it with three independent LLM judges: GPT-4o-mini,
Claude Haiku, and Llama-3.1-70B via Together. Apply position-swap
debiasing, length normalization, and majority voting, then compare the
panel verdict against your own human ratings. This is the project that
turns "I think it works" into "I can prove it".

**Steps**:
1. Carry over 20 to 50 ground-truth Q&A pairs from the Module 32 project.
2. Write the judge prompt template (Section 46.1): pairwise comparison of
   `(answer_a, answer_b)` against `(question, reference)` with explicit
   rubric (groundedness, completeness, conciseness).
3. Run each judge once per pair, then re-run with the answers swapped
   (Section 46.3). Discard non-deterministic verdicts.
4. Apply length normalization: regress judge score on output length and
   subtract the fitted bias (Section 46.3).
5. Aggregate (Section 46.5): majority vote across the three judges, with
   abstention when they disagree by more than one rank.
6. Calibrate: rate 20 of the same pairs yourself, compute Cohen's kappa
   between you and the panel, and report agreement.

**Expected outcome**:
A `judge_run.jsonl` log, an agreement-with-human number, and a clear
sense of where each individual judge fails (position, length, self-
preference). You will have hands-on intuition for why production LLM eval
panels exist.

**Difficulty**: 3 to 4 hours, assuming the Module 32 outputs already exist.

---

### Spec 5 (Module 37: Building Conversational AI Systems)

**Project name**: Build a long-term-memory chatbot that remembers you across
sessions

**Goal**:
Build a chatbot that has a defined persona, a short-term sliding-window
memory inside a session, and a long-term vector memory that persists
across sessions. After a few conversations it should be able to answer
"What did I tell you about my dog last week?" correctly. This is the
end-to-end "conversational AI" build that exercises every section of the
chapter at once.

**Steps**:
1. Pick a persona (Section 37.2): write a system prompt that locks in
   tone, name, role, and refusal style.
2. Implement short-term memory (Section 37.3): keep the last N turns in a
   `deque`; when the window overflows, summarize the oldest 50% with a
   cheap model and keep the rest verbatim.
3. Add long-term memory (Section 37.5a): on every user turn, embed and
   write the turn to Chroma with a `user_id` and timestamp. On every
   turn, retrieve the top-K relevant memories and inject them into the
   system prompt as "What you remember about this user".
4. Implement persistence: store conversation history in SQLite keyed on
   `user_id` so the chatbot survives a process restart.
5. Implement consolidation (Section 37.5b): every 20 turns, run a
   summarizer over the user's memories and replace raw turns with a
   distilled profile snippet.
6. Evaluate (Section 37.5b): run a 3-session role-play. In session 3,
   ask 5 questions about facts mentioned in sessions 1 and 2; measure
   recall.

**Expected outcome**:
A persistent chatbot you can run from the CLI that recognizes returning
users, mentions facts from prior sessions appropriately, and survives
restarts. This is the smallest meaningful "conversational AI with
memory" build, and it ports directly into a portfolio project.

**Difficulty**: weekend (6 to 8 hours).

---

## Part 3: Implementation Notes (for a Future Wave)

When a future wave implements these project anchors, it should:

### A. Use the canonical callout class

```html
<div class="callout hands-on">
  <div class="callout-title">Hands-On: Project Anchor</div>
  <p><strong>Project: [name]</strong></p>
  <p>[1-paragraph goal]</p>
  <ol>
    <li>[step 1]</li>
    ...
  </ol>
  <p><strong>Expected outcome</strong>: [outcome]</p>
  <p><strong>Difficulty</strong>: [time estimate]</p>
</div>
```

Per `CONTENT_GUIDELINES.md` §8.7, the title text "Hands-On" pairs with
`class="callout hands-on"`. Using "Project Anchor" as the trailing label
inside the title keeps the existing audit happy while still labeling the
section semantically.

### B. Insertion point in every chapter index

Place the new block **between** the closing `</ul>` of `sections-list` and
the opening `<div class="whats-next">`. Exact files to edit (top 5 only):

- `part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html`
  (after line 133, before line 134 in the current revision)
- `part-6-agentic-ai/module-26-ai-agents/index.html`
  (after line 128, before line 129)
- `part-4-training-adaptation/module-17-peft/index.html`
  (after the sections-list closing `</ul>`)
- `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/index.html`
  (after line 106, before line 107)
- `part-8-conversational-ai-with-llms/module-37-conversational-ai/index.html`
  (after line 138, before line 139)

### C. Cross-reference each step to the right section

Every numbered step should hyperlink the relevant `section-NN.M.html` so
the project doubles as a study guide. Example:

```html
<li>Build an ingestion pipeline (<a href="section-32.1a.html">Section 32.1a</a>):
chunk with RecursiveCharacterTextSplitter ...</li>
```

### D. Connect each project anchor to the capstone

Each chapter's project anchor should end with a one-sentence "and this
becomes part of your capstone (see <a href='../../capstone/index.html'>Capstone</a>)
if you complete it well." That stitches the small builds into the big build.

### E. Avoid these failure modes

- Do not add a project anchor that just repeats a section's existing
  in-prose lab. Check the bottom of each section's main file first.
- Do not exceed 6 numbered steps per anchor. Anything longer belongs in
  the capstone.
- Do not call them "exercises" or "homework". They are projects, and
  the framing should be "you can ship this".
- Do not introduce em-dashes or double dashes anywhere in the prose
  (global style rule).

### F. Audit hook

After implementation, add a new audit check `PROJECT_ANCHOR_PRESENT`
that asserts each non-survey chapter's `index.html` contains at least
one `<div class="callout hands-on">` block before the first
`<div class="whats-next">`. This is symmetric to the existing
`CHAPTER_STARTER` audit that gated the overview and learning objectives
backfill (see `docs/content-audit/CHAPTER_STARTER_BACKFILL_REPORT.md`).

## Summary

| Metric | Value |
|---|---|
| Chapters scanned | 82 |
| Chapters with any existing project mention on index | 6 (~7%) |
| Chapters with a canonical `callout hands-on` on index | 0 |
| Top candidates ranked | 15 |
| Detailed specs written | 5 (Modules 32, 26, 17, 46, 37) |
| Recommended insertion point | between `sections-list` and `whats-next` |
| Recommended callout class | `callout hands-on` |
| Recommended title text | "Hands-On: Project Anchor" |
| Estimated implementation cost (top 5) | one focused agent wave, ~30 minutes per chapter |
| Estimated implementation cost (all 15) | ~2 focused agent waves |

**Verdict**: ACTION-ORIENTED CONTENT GAP. The book teaches everything a
reader needs to build serious LLM systems, but the chapter index pages do
not currently end with a "now go build this" anchor. Adding 15 project
anchors (1 per high-payoff chapter) is the smallest change that would make
the book feel meaningfully more action-oriented without disturbing any
existing prose. A future wave can implement the top 5 specs above first,
then iterate.
