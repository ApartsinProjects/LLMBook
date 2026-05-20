# Wave 2: Collapsed-Indentation Python Code Fragment Fixes

Generated: 2026-05-20
Source: TODO 1 in `ACTIONABLE_TODOS.md` (from `CRITICAL_READER_AUDIT.md` item 14 + item 1 fleet)
Branch: v2.0

## Summary

The Pygments/HTML pipeline produced "staircase" indentation in several
flagship Python code blocks: nested `def`s appeared inside a TypedDict/dataclass
body, `return` statements landed at a deeper indent than the surrounding block
(making subsequent code unreachable and the structure wrong), and one f-string
was split across two physical lines without string concatenation (a genuine
non-parseable error).

A subtle point: most of these blocks still passed `ast.parse` because dead code
after a `return` at the *same* indent is legal Python, and methods inside a
TypedDict are legal Python. The bug is *structural* (wrong logic, methods buried
in the wrong class, code unreachable), not always a parse error. Verification
therefore checked both `ast.parse` success **and** the top-level node structure
(a TypedDict/dataclass must contain only field annotations; module-level `def`s
must be at module level; graph-building / demo code must be at module level).

7 of the 8 listed fragments had a live bug and were fixed. The 8th (the second
location flagged in `section-32.3.html`) was already structurally correct in the
current renumbered file; every Python block in that file now parses with clean
structure.

Verification harness (kept for reuse):
- `docs/content-audit/_scan_pyblocks.py` - scans a file for every Python
  `<pre><code>` block, de-HTMLs it, runs `ast.parse`, and prints top-level node
  kinds so a nested-`def` staircase is visible at a glance.
- `docs/content-audit/_verify_codeblock.py` - de-HTMLs a single block by line
  range and reports parse status + top-level structure.

Fix style: blocks with multi-level staircases (tokens in order but many lines at
the wrong indent) were rewritten as clean `<pre><code class="language-python">`
plain-text blocks (the sanctioned correctness-over-highlighting fallback).
Single-line indent bugs were fixed in place, preserving the Pygments `<span>`
markup.

## Fragments fixed

### 1. FLAGSHIP - `part-6-agentic-ai/module-26-ai-agents/section-26.2.html`
LangGraph plan-and-execute (Code Fragment 26.2.1).
- **Before:** `def create_plan`, `def execute_step`, `def should_replan` were all
  indented 4 spaces, so they parsed as **methods of the `PlanExecuteState`
  TypedDict**. Inside `should_replan`, `return "synthesize"` was followed by a
  deeper-indented block (the LLM re-check + `return "replan"` + `return "execute"`)
  that was unreachable, and the entire graph-building section
  (`graph = StateGraph(...)` plus 9 `add_node`/`add_edge` calls) was buried inside
  `should_replan`'s `if` branch at indent 16.
- **After:** `PlanExecuteState` contains only its 5 field annotations; the three
  functions are module-level; the `if ... return "synthesize"` early-return is
  followed (at function-body indent) by the LLM re-check and `return "execute"`;
  the graph-building block is at module level.
- **Method:** full rewrite to `language-python`.
- **Top-level now:** `[imports, class PlanExecuteState (0 methods), def create_plan,
  def execute_step, def should_replan, graph assignment, 9 calls]`.

### 2. `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html`
G-Eval probability-weighted scoring (Code Fragment 46.2.2), the chapter's central example.
- **Before:** the `client.chat.completions.create(...)` call and everything after
  it (`content`, `logprobs`, `score_probs`, the `if logprobs ...` block) dropped to
  indent 0, falling **outside the `geval_score` function body**. The
  `# Compute probability-weighted score` block, the `if score_probs / else`, and the
  `return {...}` were over-indented inside the `for lp in ...` loop.
- **After:** the whole body sits at function-body indent; the probability-weighting
  `if/else` and the `return` are at function-body level (after the for-loop), not
  inside the loop.
- **Method:** full rewrite to `language-python` (prompt-template string preserved
  verbatim).

### 3. `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.1.html`
BackpressureQueue (Code Fragment 62.1.2).
- **Before:** `@property utilization`, `async def enqueue`, and `def health_status`
  were progressively over-indented (the staircase started at `@property` at indent
  8). `return "healthy"` was nested inside the `if util > threshold:` block, so it
  was unreachable.
- **After:** all four members (`__init__`, `utilization`, `enqueue`,
  `health_status`) are class-methods at indent 4; `return "healthy"` is at
  method-body level after the `if`.
- **Method:** full rewrite to `language-python`.

### 4. `part-4-training-adaptation/module-17-peft/section-17.2.html` (GaLore)
GaLoreProjector (Code Fragment 17.2.6).
- **Before:** `self.step += 1`, the `# Project gradient` comment, and
  `return self.projector.T @ grad` were nested inside the `if self.step % ... == 0:`
  block (indent 12). `def back_project` was nested inside `project` at indent 12,
  with its body at indent 16.
- **After:** SVD recompute stays inside the `if`; `self.step += 1` and the
  projection `return` are at method-body level; `back_project` is a class-method at
  indent 4.
- **Method:** full rewrite to `language-python`.
- **Top-level now:** `class GaLoreProjector` with exactly 3 methods.

### 5. `part-4-training-adaptation/module-17-peft/section-17.2.html` (rsLoRA)
rsLoRA vs standard LoRA scaling (Code Fragment 17.2.8).
- **Before:** `return lora_output * scaling` was at indent 8, inside the `else:`
  branch. So the `use_rslora=True` path computed `scaling` and then fell through to
  return `None`.
- **After:** the `return` is at function-body indent (4), after the `if/else`, so
  both branches return the scaled output.
- **Method:** single-line whitespace fix; Pygments `<span>` markup preserved.

### 6. `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html`
Corrective RAG / CRAG state machine (Code Fragment 32.2.4a).
- **Before:** inside `grade_documents`, the relevance-grading f-string was written
  across two physical lines without concatenation:
  `f"Rate relevance 0-1.\nQuery: {state['query']}` (newline) `\nDocument: ...Score:"`.
  A non-triple-quoted f-string cannot span lines, so this raised
  `SyntaxError: unterminated f-string literal` - the only block in the file that
  genuinely failed to parse.
- **After:** split into two adjacent f-string literals (implicit concatenation),
  matching the multi-line f-string style used elsewhere in the file; identical
  rendered prompt text (the stray leading-indent whitespace that had leaked into
  the broken string was dropped as an artifact).
- **Method:** targeted fix; Pygments `<span>` markup preserved.

### 7. `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html`
FormalProvingResult / BenchmarkEvaluation pass@k (Code Fragment 8.6.3).
- **Before:** inside `premise_retrieval_accuracy`, `recalls.append(recall)` and the
  final `return sum(recalls)/len(recalls)` were over-indented inside the
  `if gold_premises:` block (so the method returned on the first loop iteration).
  `def summary` was nested inside that loop at indent 12, and the
  `# Example evaluation` driver code (`eval_run = ...` + `print(...)`) was buried at
  indent 16 instead of module level.
- **After:** `recalls.append` stays inside the `if`; the `return` is at method-body
  level after the for-loop; `summary` is a class-method at indent 4; the example
  driver is at module level.
- **Method:** full rewrite to `language-python`.
- **Executable check:** the de-HTMLed block runs and reproduces the documented
  output exactly (`total: 4, proved: 3, pass@1: 0.25, pass@10: 0.5, pass@100: 0.75,
  avg_time: 72.475`), confirming the logic reconstruction is faithful.

### 8. Second `section-32.3.html` location (flagged ~L212)
- **Status:** no live bug. The multi-source `asyncio.gather` fan-out block (the
  five `async def search_*` functions) and every other Python block in the file
  parse with clean top-level structure. Either a prior wave fixed it or the
  renumber merged the two flagged line refs. No edit needed; verified by full-file
  scan.

## Non-issues observed (left untouched, out of scope)

These showed as parse "failures" in the scanner but are not collapsed-indentation
Python bugs and are not among the flagged fragments:
- `section-26.2.html` Algorithm 26.2.1 block: pseudocode (`Input: ...`, numbered
  steps) tagged `lang-python`. Renders fine; intentional pseudocode.
- Four `pip install ...` one-liners tagged `lang-python`
  (`section-26.2.html` "pip install letta", `section-46.2.html` "pip install
  deepeval", `section-17.2.html` "pip install bitsandbytes peft transformers trl",
  `section-32.3.html` "pip install -U langchain ..."). Shell commands, single line,
  render correctly.

Per the task constraint ("only touch the flagged code blocks"), these language-label
quirks were not modified.

## Result

- 7 of 8 listed fragments fixed (the 8th was already correct).
- 5 required a full block rewrite (multi-level staircase or unterminated f-string):
  26.2 PlanExecuteState, 46.2 G-Eval, 62.1 BackpressureQueue, 17.2 GaLoreProjector,
  8.6 FormalProvingResult.
- 2 were surgical (single-line) fixes preserving Pygments markup: 17.2 rsLoRA
  `return` indent, 32.3 CRAG f-string split.
- Every edited block verified to `ast.parse` with correct top-level structure; the
  8.6 block additionally verified by execution against its printed output.
