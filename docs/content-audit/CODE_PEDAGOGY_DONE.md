# Code Pedagogy Pass: Conservative Improvement Report

**Date**: 2026-05-20
**Scope**: Python code blocks in Parts 4 (Training), 7 (RAG), and 13 (LLMOps)
**Mode**: Conservative inline-edit pass following `agents/book-skills/agents/08-code-pedagogy.md`
**Audit status**: PASS (`/c/Python314/python -m agents.book-skills.scripts.audit.run --priority P0+P1 --root .` returns 0 issues across 558 scanned files)

---

## Summary

This pass applied small, conservative pedagogical improvements to Python code blocks in sections
that the user is most likely to read closely. The focus was on three categories of fixes:

1. **Variable naming**: Renamed single-letter loop variables (`q`, `e`, `p`, `r`) to descriptive
   names (`query`, `entity`, `path`, `result`, `param`) where doing so did not break line length,
   shadow function parameters, or change behaviour.
2. **Network safety hints**: Added inline `# Production code should wrap this in try/except for
   network errors.` comments next to `requests.get` / `requests.post` / `requests.put` calls that
   had no error handling.
3. **Brief inline comments**: Added 1-line clarifying comments to specific dense lines to explain
   the intent without lecturing.

The pass was deliberately under-budget. The task allowed up to 40 files and 3 edits per file; the
real opportunity was much smaller than that limit because the focus parts are already in
relatively good shape after earlier passes (CODE_PEDAGOGY_R2.md, code-correctness-audit.md,
code-fragment-fix-report.md). Most candidate "improvements" were either:

- Single-letter variables inside tight tuple unpacking (`t, n`, `i, j`) where the existing name
  carries clear local meaning
- Loop variables inside function bodies where renaming would shadow a function parameter
- Variables in list comprehensions where the surrounding context makes the meaning obvious
- Code already revised in earlier passes with good comments and structure

The bar for an edit was: would a reasonably attentive reader **immediately** be helped by the
change? If the answer was "no, the existing code is fine," the edit was skipped.

---

## Files Touched (10 total)

### Part 4: Training and Adaptation

#### `part-4-training-adaptation/module-17-peft/section-17.4.html`
- Renamed `p` to `param` in the `PromptedLlama.__init__` freeze loop. Added a one-line comment
  clarifying that the freeze loop is what makes only the soft prompt trainable.

#### `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.5.html`
- Added a `# Production code should wrap this in try/except for network errors.` comment above
  the `requests.post` call that submits a managed fine-tuning job to the Databricks REST API.
  The example otherwise reads as if a single unhandled network error would cause an opaque
  KeyError on the next line when the JSON access fails.

### Part 7: Retrieval and Information Extraction

#### `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html`
- In the lab's semantic-search test loop, renamed `q` to `query` (function param has no scope
  conflict because the loop is at module level after `semantic_search` is defined). The format
  string `f"Query: {q}"` now reads naturally as `f"Query: {query}"`.

#### `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html`
- In the lab's `retrieve()` test driver, renamed `q` to `query` and clarified the surrounding
  comment from `# Test` to `# Test against four representative queries from the lab's policy KB.`
  Both changes target the same code fragment to keep the diff tight.

#### `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.1.html`
- In `encode_images`, renamed `p` to `path` in the `Image.open(p) for p in paths` comprehension.
  This brings the variable name in line with the parameter name (`paths`) and the surrounding
  prose about "image paths."

#### `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html`
- In the spaCy NER post-processing loop, renamed `e` to `entity` and replaced the trivial
  `# Group by entity type` comment with `# Group by entity type (PERSON, ORG, DATE, etc.) for
  readable output.` so the reader sees concrete entity labels.

#### `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html`
- In the `hybrid_retrieve` answer-sketch code, renamed `e` to `entity` in the per-entity graph
  traversal loop. The function is short (12 lines per the exercise prompt) so this lands without
  shadowing.

#### `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html`
- In the Apache Tika `extract_with_tika` helper, added a `# Production code should wrap the
  requests.put calls in try/except for network errors.` comment to the opening comment block.
  The example does two `requests.put` calls back to back so the single comment covers both.

#### `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.2.html`
- In the `rerankers` library shortcut, renamed `r` to `result` in the list comprehension
  building `top_ids = [r.doc_id for r in results.top_k(5)]`. The local name `result` matches
  the surrounding variable `results`.

### Part 13: LLMOps Lifecycle

#### `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html`
- Added a `# Production code should wrap this in try/except for network errors.` comment above
  the `requests.post` call inside the `measure_request` benchmark helper. The example is the
  lab's first introduction to driving an LLM endpoint from Python, so the safety note matters
  most here.
- Renamed `r` to `result` in two list comprehensions (`latencies`, `throughputs`) that consume
  the benchmark dictionary. Aligns the loop variable with the result-dict semantics.

---

## What was deliberately NOT changed

A list of candidate sections inspected but skipped, with rationale, so a future pass can pick
them up if scope expands:

- **`section-15.2.html`** (Self-Instruct pipeline): Long code blocks but the indentation is
  already heavy, and existing comments cover the non-obvious steps. No safe single-line
  improvement found.
- **`section-15.3.html`** (Quality filtering / MinHash): Variables `ex`, `mh`, `lsh`, `j` are
  domain-of-art conventions in deduplication code. Renaming would not aid clarity.
- **`section-15.7.html`** (EDA augmentation): `w` for word in `[w for w in words if ...]` reads
  fine in context; the comprehension is one line and the meaning is unambiguous.
- **`section-16.x`** (Fine-tuning fundamentals): Already well-commented from earlier passes.
  The `mix_datasets` and `compute_class_weights` functions have section-by-section comments
  explaining the math; no obvious deficit.
- **`section-17.3.html`** (Training platforms): Code is mostly CLI shell wrapped in Python
  comments (`# tune run lora_finetune_single_device ...`), not executable Python where variable
  renaming would help.
- **`section-17.5.html`** (Distillation): `T = self.temperature` is the canonical math symbol
  for temperature and matches the surrounding prose. Renaming would harm readability.
- **`section-17.7.html`** (Model merging): `w_a`, `w_b` follow the math (Model A weight,
  Model B weight) and the comments already explain the merge formula. No improvement found.
- **`section-17.8.html`** (Continual learning): `F` (Fisher information), `theta_star`,
  `theta_new` mirror the standard EWC notation in the prose. Mathematical convention beats
  long names.
- **`section-18.x`** (DPO/RLHF): Most files in this module are on the deep-dive and
  mental-model agents' avoid list (18.1, 18.2, 18.3, 18.7). Sections 18.4-18.6 were inspected
  and judged adequate; the code for online DPO and GRPO uses standard policy-optimization
  notation (`policy`, `prompts`, `beta`) already.
- **`section-19.x`** (Tools of the trade): These sections are almost entirely tool walkthroughs
  with code-fragment outputs already showing typical results. Many code blocks are short
  setup snippets like `import wandb; wandb.init(...)` where there is no room for safe
  improvement.
- **`section-31.x`** other than 31.2: Files like 31.1 (foundations), 31.3 (ANN), 31.5 (vector
  DBs), 31.6 (chunking), 31.7 (operations) were inspected. They contain math-heavy code with
  conventional notation (`q`, `K`, `V` for query/key/value in attention; `Q`, `K`, `M` for
  set sizes). Renaming would make the code less aligned with the equations.
- **`section-32.1.html`** and **`section-32.5.html`**: Both contain RAG pipelines with
  function parameters already named `query`, `chunks`, `retrieved_docs`. The few short-name
  variables (`i`, `s`) are tuple-unpacking artefacts. No safe improvement found.
- **`section-32.3.html`**: Agentic RAG with LangGraph; CRAG state machine variables like
  `state`, `docs`, `scores` are already descriptive. The single-character `s` in
  `all(s < 0.5 for s in scores)` is a clean comprehension.
- **`section-33.2.html`** (Multimodal RAG): Variables `qd`, `oai`, `q_emb`, `b64` are
  domain shorthand (`qd` = Qdrant client, `oai` = OpenAI client). Renaming would harm
  alignment with the comments that explicitly call them out.
- **`section-35.1.html`**: Loop variable `q` in `for q in all_queries` would shadow the outer
  function parameter `query`. Best left as `q` until a broader refactor renames the parameter.
- **`section-35.2.html`** and **`section-35.3.html`**: Already well-commented; lab variables
  like `b`, `e`, `r` for baseline/expanded/reranked results encode the experimental design
  succinctly. A rewrite would be defensible but is out of scope for a conservative pass.
- **`section-36.x`** other than 36.2: Almost all code blocks are short library-shortcut
  examples (3-8 lines) with no room for variable-name improvement.
- **`section-62.x` and `section-63.x`**: Production engineering code uses standard async
  patterns. Variables like `t`, `n` inside `(timestamp, num_tokens)` tuple unpacking are
  clearer as `t` and `n` (matching the type annotation `list[tuple[float, int]]`) than as
  long names; expanding them would push lines past 100 chars.
- **`section-64.x`**: Variables `fn`, `T`, `delay`, `attempt` follow the retry-pattern
  conventions and the surrounding type hints make the meaning unambiguous.
- **`section-65.5.html`** Locust load test: Variable names `host`, `wait_time`, `prompts`
  already track the Locust convention; the test class fields are pinned by the framework's
  API.
- **`section-66.x`**: Reliability patterns (retries, circuit breakers, guardrails) use the
  canonical names from the resilience-engineering literature; the agent should not rewrite
  these to look like personal preferences.

---

## Constraints Respected

- **Wall time**: Pass completed well under the 60-minute budget.
- **Files touched**: 10 (limit was 40).
- **Edits per file**: 1-2 each (limit was 3).
- **Logic unchanged**: All edits are renames, comment additions, or both. No function
  signatures, control flow, or imports were touched.
- **No em dashes**: All added comments use commas, colons, semicolons, or parentheses.
- **Edit tool only**: Every change went through `Edit` with exact `old_string` and `new_string`.
- **Avoided files owned by other agents**: No edits to any file in `part-1-llm-building-blocks/`,
  to part-6 modules 26/29/30, or to the specific sections listed in the prompt's avoid list
  (section-2.3, 3.5, 7.3, 22.1, 22.3, 26.2, 32.4, 40.1, 59.2, 59.3, 75.2, 9.3, 18.1, 18.2,
  18.3, 18.7, 42.12).

---

## Audit Result

```
$ /c/Python314/python -m agents.book-skills.scripts.audit.run --priority P0+P1 --root .
======================================================================
Scanned 558 files. Found 0 issues: .
Completed in 17.2s.
```

P0+P1 audit pass: PASS.

---

## Recommendations for a Future Pass

If the budget for code pedagogy is expanded:

1. **Add output panes to bare code blocks**. Several sections (notably 35.1, 35.3, 36.2) end
   library-shortcut blocks without a `<div class="code-output">` showing what the call returns.
   The `08-code-pedagogy.md` rubric requires output for any `print()` or `.head()` call.
2. **Tighten generic captions**. Captions like "Code Fragment N: Pip install tenacity." or
   "Code Fragment N: Defines expand_query and expanded_search" are too short to match the
   rubric's "2 to 3 specific sentences" requirement.
3. **Split overly long blocks**. Sections 19.4 (21 Python blocks), 17.1 (12 blocks), and 31.2
   (10 blocks) sometimes pack a 40-line code block into one `<pre>`. Splitting into 2-3
   blocks with interpretive prose between them would improve learnability, but it requires
   touching multiple HTML structures per block and is too risky for a quick pass.
4. **Replace remaining single-letter math variables in loss-function code** (`T`, `F`, `Q`,
   `K`, `V`) with their long names *only* where the prose does not already gloss them. This
   is delicate work because in attention/DPO/KD code the single letters track the equations
   in the prose.

A focused follow-up pass on those three items would add ~40-80 more edits across 20-30 files.

---

## Final Status

- **Files touched**: 10
- **Edits applied**: 11 (one file received two edits)
- **Audit pass status**: PASS (P0+P1, 0 issues across 558 files)
- **Wall time**: Under budget
