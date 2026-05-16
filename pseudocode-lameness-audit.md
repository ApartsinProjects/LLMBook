# Pseudocode and Algorithm Block Lameness Audit

Audit scope: every captioned `Pseudocode N.N.N` or `Algorithm N.N.N` block, plus every `<div class="callout algorithm">` block (any title), across the LLMBook HTML tree.

Goal: identify pseudocode boxes that add no pedagogical value: trivial INPUT/OUTPUT/FOR-LOOP narration, blocks whose body is just `do_thing()` / `process(x)` / numbered step lists, or wrapper / config blocks mislabeled as algorithm.

Script: `scripts/_audit_pseudocode_lameness.py` (Python 3.14, BeautifulSoup).

**Signals** (binary, 1 if present). Flag threshold: score >= 2.

1. `tiny_three_lines` -- 3 lines or fewer, no `def` / `class` / loop / branch.
2. `placeholder_identifiers` -- body dominated by `do_X` / `process` / `foo` / `step1` calls.
3. `trivial_sequential` -- 3+ numbered 'Step N: ...' lines, no branching, no math, no data structure.
4. `no_control_flow` -- no `for` / `while` / `if` / `return`.
5. `no_algorithmic_insight` -- no recurrence, no invariant, no complexity claim, no named data structure, no substantive operator (`argmax`, `softmax`, `KL`, `clip`, `tile`, ...).
6. `wrapper_or_config` -- caption promises an algorithm but body is YAML / JSON / dict literal / setting object.

**Overrides** (clear soft signals if present):

- Recurrence detected (`dp[i] = ...`, `score[t] := ...`).
- Invariant / precondition / postcondition language.
- Complexity claim (`O(...)`, `time complexity`, etc.).

**Exclusions** (NOT flagged even if signals would fire):

- Blocks showing recurrences.
- Blocks with `invariant:` / `complexity:` line.
- Multi-branch algorithms (beam search, MCTS, RL training step) where the structure carries the lesson.
- FlashAttention / paged-attention / speculative-decoding access-pattern pseudocode.

## 1. Summary

- Files scanned: **389**
- Pseudocode/algorithm blocks found: **21**

Blocks by label:

| Label | Count |
|---|---|
| pseudocode | 17 |
| untitled-algorithm | 4 |

Blocks by source:

| Source | Count |
|---|---|
| callout-algorithm | 16 |
| callout-untitled | 4 |
| code-caption | 1 |

**Total flagged (score >= 2): 2**

Signal frequencies (all blocks vs flagged blocks):

| Signal | All | Flagged |
|---|---|---|
| tiny_three_lines | 0 | 0 |
| placeholder_identifiers | 0 | 0 |
| trivial_sequential | 2 | 2 |
| no_control_flow | 1 | 0 |
| no_algorithmic_insight | 6 | 2 |
| wrapper_or_config | 0 | 0 |

## 2. Top 20 worst offenders

| # | File:line | Caption | Score | Signals | Verdict | Effort |
|---|---|---|---|---|---|---|
| 1 | `part-6-agentic-ai/module-21-ai-agents/section-21.1.html:290` | Pseudocode 20.1.2: This pseudocode formalizes the ReAc... | 2 | trivial_sequential,no_algorithmic_insight | drop | XS |
| 2 | `part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html:68` | Pseudocode 21.2.1: The MCP initialization handshake, h... | 2 | trivial_sequential,no_algorithmic_insight | drop | XS |

## 3. Detailed findings (all flagged blocks)

### 1. Pseudocode 20.1.2: This pseudocode formalizes the ReAct agent loop: given a user task T, tool set, and LLM M, the agent iterates through Thought, Action, and Observation steps up to max_steps S. The l

- File: `part-6-agentic-ai/module-21-ai-agents/section-21.1.html:290`
- Source: `callout-algorithm`, lang=`None`
- Score: **2** -- signals: trivial_sequential, no_algorithmic_insight
- Verdict: **drop** (XS) -- numbered 'Step 1 / Step 2 / Step 3' narration with no branching, math, or data structures
- Improvement path: drop block; rewrite the prose to say 'The pipeline does A, then B, then C.'

Body (first 6 non-blank lines):

```
Input: user task T, tool set {tool_1, ..., tool_n}, LLM M, max steps S
Output: final answer or action result
1. Initialize context = [system_prompt, T]
2. for step = 1 to S:
 a. Thought: response = M(context)
 The LLM reasons about current state, what is known, what is needed
```

### 2. Pseudocode 21.2.1: The MCP initialization handshake, host opens a transport, exchanges initialize / initialized messages, then discovers and calls tools via JSON-RPC. Steps 1-6 are one-time setup; ste

- File: `part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html:68`
- Source: `callout-algorithm`, lang=`text`
- Score: **2** -- signals: trivial_sequential, no_algorithmic_insight
- Verdict: **drop** (XS) -- numbered 'Step 1 / Step 2 / Step 3' narration with no branching, math, or data structures
- Improvement path: drop block; rewrite the prose to say 'The pipeline does A, then B, then C.'

Body (first 6 non-blank lines):

```
Input: MCP host (LLM application), MCP server (tool provider)
Output: established session with discovered capabilities
1. Host opens transport (stdio pipe or HTTP/SSE connection)
2. Host sends initialize request:
{ protocolVersion, clientInfo, capabilities }
3. Server responds with initialize result:
```

## 4. Quick-drop list (low value, prose covers them)

These blocks contain no algorithmic insight that the surrounding prose does not already carry. Recommended action: delete the block, ensure the prose paragraph above states the steps in plain English, and renumber subsequent labels.

| File:line | Caption | Reason |
|---|---|---|
| `part-6-agentic-ai/module-21-ai-agents/section-21.1.html:290` | Pseudocode 20.1.2: This pseudocode formalizes the ReAct agent loop: g... | numbered 'Step 1 / Step 2 / Step 3' narration with no branching, math, or data ... |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html:68` | Pseudocode 21.2.1: The MCP initialization handshake, host opens a tra... | numbered 'Step 1 / Step 2 / Step 3' narration with no branching, math, or data ... |

## 5. Worth-improving list (rewrite would add real value)

_None._

## 6. Borderline watchlist (score = 1)

These blocks fire exactly one lameness signal. None reach the flag threshold, but the editor may want to inspect a few -- a single extra signal (e.g. a numbered-step list with no operators) would tip them over.

| File:line | Caption | Signal |
|---|---|---|
| `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html:202` | Under the Hood: vLLM's Block Table | no_control_flow |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html:76` | Pseudocode 21.1.1: Function calling loop | no_algorithmic_insight |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.2.html:78` | Pseudocode 22.2.1: The supervisor (hub-and-spoke) pattern as a multi-... | no_algorithmic_insight |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html:61` | Under the Hood: Position Bias in LLM-as-Judge | no_algorithmic_insight |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.8.html:67` | Pseudocode 29.8.1: Automated red teaming pipeline | no_algorithmic_insight |

## 7. Recommended editorial priority

1. **Drop the quick-drop list** (2 blocks). These are pure narration; prose already says what they say. Deletion is the simplest fix and removes visual clutter.
2. **Rewrite the worth-improving list** (0 blocks). For each, ask: 'What recurrence, invariant, or complexity claim makes this algorithm non-trivial?' If the answer is 'nothing', drop it instead. If real library code would do the job better, upgrade to a `Code Fragment` and import the real API.
3. **Renumber downstream blocks** after deletes. The `Pseudocode N.N.N` and `Algorithm N.N.N` captions are referenced from prose; check cross-references after any drop.
4. **Add a stylistic rule to CONTENT_GUIDELINES.md**: a Pseudocode box must carry at least one of (recurrence, invariant, complexity claim, named data structure operation). If none applies, the content belongs in prose.
5. **Re-run** `scripts/_audit_pseudocode_lameness.py` after edits to confirm the flagged count drops.

---

Generated by `scripts/_audit_pseudocode_lameness.py`. Signals are heuristic; before deleting a block, read the surrounding prose to confirm the box really is redundant.