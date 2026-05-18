# Critical Reader Audit: Code Fragments and Diagrams

**Scope.** 38 code fragments and 22 inline SVG diagrams sampled across Parts 2 through 13. Tools-of-the-trade modules and appendices excluded. Date: 2026-05-18.

## Aggregate verdict totals

| Verdict   | Code | Diagrams | Total | Share |
|-----------|------|----------|-------|-------|
| KEEP      |  18  |   15     |  33   |  55%  |
| REDESIGN  |  11  |    4     |  15   |  25%  |
| CONVERT   |   2  |    3     |   5   |   8%  |
| DROP      |   7  |    0     |   7   |  12%  |

The headline finding: roughly 55% of fragments earn their place. The dominant pathology is **collapsed indentation in long Python fragments**, where the Pygments/HTML pipeline appears to have flattened nested `def`s and `if` branches into a continuous staircase. These read as code, look colorful, and are silently wrong. A second cluster is **`pip install` lines wrapped in `<pre><code>` blocks** that should be a single sentence at section start.

## Code fragments

| # | File | Line | Verdict | Justification |
|---|------|------|---------|---------------|
| 1 | part-4/module-17/section-17.2.html | 122 | DROP | `pip install bitsandbytes peft transformers trl` only. Move to a sentence. |
| 2 | part-4/module-17/section-17.2.html | 138 | KEEP | Canonical `LoraConfig` with `use_dora=True`; runnable and referenced. |
| 3 | part-4/module-17/section-17.2.html | 169 | KEEP | `PrefixTuningConfig` shows the API and the projection-MLP knob. |
| 4 | part-4/module-17/section-17.2.html | 189 | REDESIGN | `AdaptionPromptConfig` example, but caption claims bottleneck adapters when the API shown is LLaMA-Adapter; clarify or rewrite. |
| 5 | part-4/module-17/section-17.2.html | 213 | KEEP | `IA3Config` with target modules; tight and on-API. |
| 6 | part-4/module-17/section-17.2.html | 399 | REDESIGN | `GaLoreProjector` class has wrong nested indentation: `back_project` falls inside `project`, `step` increment misordered. |
| 7 | part-4/module-17/section-17.2.html | 425 | KEEP | `GaLoreAdamW8bit` library shortcut; clean call. |
| 8 | part-4/module-17/section-17.2.html | 449 | REDESIGN | `lora_forward` rsLoRA comparison: `return` is inside the `else` branch, so the `if` branch falls through. Output block is also drifted (shows rsLoRA norms but caption never references them). |
| 9 | part-4/module-18/section-18.2.html | 114 | KEEP | DPO numeric walkthrough; computes margin and loss in 8 lines, prose in 18.2 is explicitly anchored to it. |
| 10 | part-4/module-18/section-18.2.html | 202 | KEEP | TRL `DPOTrainer` end-to-end recipe; output block included. |
| 11 | part-4/module-18/section-18.2.html | 277 | DROP | `pip install trl` then GRPO snippet duplicating Code Fragment 18.2.6's trainer pattern; consolidate. |
| 12 | part-4/module-18/section-18.2.html | 559 | KEEP | Online DPO loop, conceptual but pedagogically distinct from offline DPO. |
| 13 | part-6/module-26/section-26.2.html | 78 | CONVERT | Pseudocode highlighted as `lang-python` but uses `1.`, `2.`, `a.`, `b.` numbering. Convert to an ordered list inside the algorithm callout. |
| 14 | part-6/module-26/section-26.2.html | 96 | REDESIGN | LangGraph plan-and-execute: `create_plan` and `execute_step` are nested inside the `PlanExecuteState` TypedDict; `return "execute"` is dead-coded. The whole 50-line block is structurally broken. High priority. |
| 15 | part-6/module-26/section-26.2.html | 158 | KEEP | PydanticAI shortcut is short, runnable, on-API. |
| 16 | part-6/module-26/section-26.2.html | 211 | DROP | `pip install letta` plus minimal client demo duplicates Code Fragment 26.2.3a's content; library-shortcut callout is enough. |
| 17 | part-7/module-31/section-31.2.html | 76 | KEEP | NumPy brute-force kNN: clean, well-scoped, output is implicit. |
| 18 | part-7/module-31/section-31.2.html | 119 | KEEP | FAISS shortcut directly mirrors the from-scratch version above. |
| 19 | part-7/module-31/section-31.2.html | 255 | KEEP | `IndexHNSWFlat` setup; real API with explanatory comments. |
| 20 | part-7/module-32/section-32.2.html | 85 | KEEP | `decompose_query` via OpenAI structured outputs; runnable and concrete. |
| 21 | part-7/module-32/section-32.2.html | 212 | REDESIGN | `multi_source_search`: nested `async def search_one` is incorrectly placed inside `multi_source_search` body but appears outdented; `return results` at end is unreachable. |
| 22 | part-7/module-32/section-32.2.html | 259 | REDESIGN | `evaluate_and_refine` has its `for iteration` body containing a single iteration that returns regardless; the loop is decorative. |
| 23 | part-9/module-42/section-42.5.html | 142 | KEEP | Quality-gate dataclass + scorer, clean. |
| 24 | part-9/module-46/section-46.2.html | 65 | REDESIGN | `geval_score`: function body fully de-indented after line 90; almost every statement reads at module scope. Critical fragment for the section. |
| 25 | part-9/module-46/section-46.2.html | 134 | KEEP | DeepEval shortcut; on-API and replaces a 60-line manual logprob block. |
| 26 | part-9/module-46/section-46.2.html | 159 | KEEP | Claude logprob-free fallback; numeric and runnable. |
| 27 | part-10/module-47/section-47.2.html | 123 | KEEP | PyRIT example with full orchestrator + scorer wiring. |
| 28 | part-10/module-47/section-47.2.html | 179 | CONVERT | Bash-style `pip install garak` and a comment block; convert to a fenced bash one-liner or a paragraph. |
| 29 | part-10/module-47/section-47.2.html | 497 | KEEP | YAML GitHub Actions workflow for security CI; useful real-world artifact. |
| 30 | part-11/module-54/section-54.3.html | 61 | KEEP | C2PA manifest JSON: long, but each field is load-bearing and explicitly referenced in the next paragraph. |
| 31 | part-11/module-54/section-54.3.html | 119 | KEEP | `sign_image` wrapper around c2patool subprocess; concrete reference impl. |
| 32 | part-13/module-62/section-62.1.html | 177 | REDESIGN | `BackpressureQueue`: `@property` decorator nested inside `__init__`, `async def enqueue` indented as if inside the property. Same indentation-staircase bug as 26.2.1. |
| 33 | part-13/module-62/section-62.1.html | 304 | KEEP | Prometheus client metrics for LLM serving; real API. |
| 34 | part-3/module-12/section-12.3.html | 80 | KEEP | Reflection loop sketch with for-iteration budget; clean. |
| 35 | part-3/module-12/section-12.3.html | 285 | KEEP | Meta-prompting example; concrete and on-API. |
| 36 | part-3/module-12/section-12.3.html | 441 | KEEP | DSPy declarative signature; minimal, captures the framework's value prop. |
| 37 | part-2/module-08/section-8.6.html | 81 | DROP | `ProofState` dataclass with no methods, only an example instance. Should be a small table or inline prose. |
| 38 | part-2/module-08/section-8.6.html | 176 | REDESIGN | `FormalProvingResult`/`BenchmarkEvaluation`: dataclass plus `pass_at_k` method, but the method body is indentation-collapsed. |

## Diagrams

| # | File | Line | Verdict | Justification |
|---|------|------|---------|---------------|
| D1 | part-4/module-17/section-17.2.html | 76 | KEEP | DoRA magnitude/direction split: real concept, 6 labeled nodes. |
| D2 | part-4/module-17/section-17.2.html | 311 | KEEP | Multi-adapter serving: base + 4 adapters + router, all clause-labeled. |
| D3 | part-4/module-18/section-18.2.html | 152 | KEEP | RLHF vs DPO pipeline: aria-label is just "Diagram" (fix it), but content is excellent and central to the section. |
| D4 | part-4/module-18/section-18.2.html | 370 | KEEP | Preference-dataset creation flow; useful map. |
| D5 | part-6/module-26/section-26.2.html | (none in this section) | - | Section uses a callout image; no SVG to audit. |
| D6 | part-7/module-31/section-31.2.html | 181 | KEEP | HNSW layered graph; non-obvious, hard to describe in prose. |
| D7 | part-7/module-31/section-31.2.html | 376 | KEEP | Product Quantization codebook diagram; classic visual aid. |
| D8 | part-7/module-32/section-32.2.html | 124 | KEEP | Agentic RAG loop: 4 named stages plus the failure-loop arrow. |
| D9 | part-7/module-32/section-32.2.html | 375 | KEEP | CRAG state machine; readable. |
| D10 | part-7/module-32/section-32.2.html | 537 | REDESIGN | Generic-shape "agentic RAG topology" with single-word boxes and disconnected arrow at top. |
| D11 | part-9/module-42/section-42.5.html | 87 | KEEP | Three-stage quality gate; has a real aria-label. |
| D12 | part-3/module-12/section-12.3.html | 140 | KEEP | Reflection loop: generate, critique, revise; matches prose well. |
| D13 | part-3/module-12/section-12.3.html | 364 | KEEP | Prompt-chain pipeline with model assignments per stage; informative. |
| D14 | part-3/module-12/section-12.3.html | 530 | KEEP | OPRO optimization loop; non-obvious flow. |
| D15 | part-8/module-37/section-37.3.html | 94 | KEEP | Layered memory architecture (context, short-term, long-term, persistent); 4 zones, full-clause labels. Fix aria-label. |
| D16 | part-13/module-62/section-62.1.html | 64 | KEEP | Latency optimization strategies; useful overview. |
| D17 | part-13/module-62/section-62.1.html | 207 | REDESIGN | Backpressure queue diagram has many boxes but several arrows lack target; dense and partly illegible at default zoom. |
| D18 | part-13/module-62/section-62.2.html | 89 | KEEP | "The Recipe Binder" mental model: novel framing, good labels. |
| D19 | part-13/module-62/section-62.2.html | 226 | KEEP | A/B testing framework topology. |
| D20 | part-13/module-62/section-62.2.html | 331 | REDESIGN | Generic 3-box pipeline ("Experiment tracking setup"); converting to a 3-row table would carry the same content. |
| D21 | part-11/module-54/section-54.3.html | (relies on JSON only) | - | No SVG; manifest tree could be drawn but current text serves. |
| D22 | part-2/module-08/section-8.6.html | (no diagrams in section 8.6) | - | Section is code-heavy, no SVGs to audit. |

(D5, D21, D22 are scoping non-issues, included so totals make sense.)

## Top 10 actionable items

These are the highest-impact fixes ordered by reader harm and ease of repair.

1. **Fix the collapsed-indentation bug fleet.** Items 6, 8, 14, 21, 22, 24, 32, 38 all share the same defect: long Python fragments where Pygments has produced a staircase of ever-deepening indentation, hiding the real structure. These are not just cosmetic; readers who copy them get broken code. A targeted script that re-pretty-prints these blocks from the original source would fix many at once.
2. **Code Fragment 26.2.1 (LangGraph plan-and-execute)** is the single most damaging case: 50 lines of a flagship agent pattern with nested defs inside a TypedDict. Replace with the working version or drop in favor of the adjacent PydanticAI shortcut.
3. **Code Fragment 46.2.2 (G-Eval)** is the worst offender in Part 9; its broken indentation undermines the section's central worked example. Re-render from the source notebook.
4. **Convert pseudocode-as-Python.** Item 13 (Algorithm 24.3.1) uses `1.`, `2.`, `a.`, `b.` numbering that the Pygments highlighter happily mangles. Either re-mark as an ordered list inside the algorithm callout or use a `lang-pseudocode` class with monospace styling.
5. **Drop or merge `pip install` fragments.** Items 1, 11, 16, and several others wrap a single shell command in a `<pre>` block as if it were pedagogical code. Each one costs vertical space without teaching anything. Consolidate to a one-sentence install note at the section header.
6. **Item 37 (ProofState dataclass).** Pure data with no methods, no behavior to demonstrate. Either replace with a small table of the four fields (goal, hypotheses, tactic, premises, result_goal) or fold into the prose introducing LeanDojo.
7. **Generic diagram cleanup (D10, D17, D20).** Three diagrams add no information that a 3-row table or two sentences could not carry. D17 (backpressure) is the most pedagogical of these and should be redrawn; D10 and D20 should be converted.
8. **Aria-label hygiene.** Many diagrams use `aria-label="Diagram"` (e.g., D3, D8, D9, D15). Auto-script a pass that copies the figcaption text into the aria-label.
9. **Fragment-numbering drift.** Several sections reference "Code Fragment 18.2.6" or "Code Fragment 26.2.5" in prose while the actual element is labeled `18.2.2` or `26.2.1`. Item 14's section also has "Exercise 20.3.x" headers inside Chapter 26. A renumbering audit pass on captions and inline references is overdue.
10. **Caption duplication.** Item 28 (PyRIT) has both a `code-caption` div and a separate `<p class="caption">` immediately after, repeating the same fragment ID. Consolidate the duplicate captions throughout the book.

Net assessment: the code-heavy parts of this book offer a high signal-to-noise ratio when fragments are correctly rendered. The bulk of remediation effort should target the rendering pipeline, not the content choices.
