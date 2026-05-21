# Low-Value Code Fragments Audit (v2.0)

Read-only scouting pass over every `<pre><code>` block in every `section-*.html` file. Goal: surface code blocks that re-state prose, encode taxonomies, or define data shells without doing the interesting work, and recommend a smaller HTML alternative (table, blockquote, diagram, prose).

**No HTML files were edited.** This document is a remediation backlog.

## Executive Summary

- **Total `<pre><code>` blocks scanned:** 1618
- **Python-tagged blocks:** 1424
- **Non-Python blocks (bash, yaml, json, etc., excluded from scope):** 194

| Category | Count | % of python blocks |
| --- | ---:| ---:|
| **DROP** | 28 | 2.0% |
| **SIMPLIFY-TO-TABLE** | 2 | 0.1% |
| **CONVERT-TO-DIAGRAM** | 0 | 0.0% |
| **KEEP** | 1394 | 97.9% |

**Distribution by part (DROP/SIMPLIFY/CONVERT candidates only):**

| Part | Candidates |
| --- | ---:|
| `part-6` | 12 |
| `part-2` | 3 |
| `part-13` | 3 |
| `part-3` | 2 |
| `part-4` | 2 |
| `part-5` | 2 |
| `part-1` | 2 |
| `part-10` | 1 |
| `part-7` | 1 |
| `part-9` | 1 |
| `part-15` | 1 |

**Methodology.** A Python classifier parses every block, strips Pygments spans, and runs a battery of conservative heuristics. KEEP is the default; the classifier only flags blocks that satisfy at least one explicit anti-pattern (data-class-only with the class never re-used, comment-only pseudocode, triple-quoted string masquerading as code, YAML mis-tagged as Python, etc.). The scripts that produced this audit live in `docs/content-audit/_low_value_audit/`.

## Top 30 DROP / SIMPLIFY / CONVERT Candidates

Ranked by severity (audit score combining size, kv-ratio, comment ratio, and lack of library/method/algorithm signal). Code excerpts are truncated; the file + line column points to the exact `<pre>` start for review.

### 1. `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html` line 179

- **Recommendation:** **DROP**  (severity 88)
- **Why:** Pure config/dict literal (kv_ratio=1.00, no library) — render as <table>
- **Replacement:** Replace with an HTML `<table>` of `key | value | meaning`. The Python syntax adds no information here.

```python
# .env  (NEVER commit this; add to .gitignore)
OPENAI_API_KEY=sk-proj-abc123...
ANTHROPIC_API_KEY=sk-ant-...
HF_TOKEN=hf_...
WANDB_API_KEY=...
```

### 2. `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.4.html` line 196

- **Recommendation:** **DROP**  (severity 85)
- **Why:** Comment-only block (6/6 lines are comments) — prose disguised as code; render as prose or shell snippet
- **Replacement:** Drop the code block; convert the bullet points into a numbered list or a shell snippet (`<pre><code class="lang-bash">`). Comments are not code.

```python
# pip install garak
# One command scans for prompt injection, jailbreaks, and encoding attacks:
# garak --model_type openai --model_name gpt-4o \
# --probes injection.direct,dan,encoding \
# --generations 25
# Output: JSON report with pass/fail rates per attack category
```

### 3. `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html` line 170

- **Recommendation:** **DROP**  (severity 85)
- **Why:** Comment-only block (29/29 lines are comments) — prose disguised as code; render as prose or shell snippet
- **Replacement:** Drop the code block; convert the bullet points into a numbered list or a shell snippet (`<pre><code class="lang-bash">`). Comments are not code.

```python
# Comparing standard vs. reasoning model outputs on the same problem
# Problem: "What is the sum of all prime numbers less than 20?"
# === Standard Model (GPT-4o) ===
# Output: "The prime numbers less than 20 are: 2, 3, 5, 7, 11, 13, 17, 19.
# Their sum is 2 + 3 + 5 + 7 + 11 + 13 + 17 + 19 = 77."
# Tokens generated: ~40
# Time: ~0.5s
# === Reasoning Model (o3-mini) ===
... (21 more lines)
```

### 4. `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` line 395

- **Recommendation:** **DROP**  (severity 85)
- **Why:** Comment-only block (10/10 lines are comments) — prose disguised as code; render as prose or shell snippet
- **Replacement:** Drop the code block; convert the bullet points into a numbered list or a shell snippet (`<pre><code class="lang-bash">`). Comments are not code.

```python
# vLLM: chunked prefill is enabled by default (v0.6+)
# To customize the chunk size:
# python -m vllm.entrypoints.openai.api_server \
# --model meta-llama/Llama-3.1-8B-Instruct \
# --enable-chunked-prefill \
# --max-num-batched-tokens 2048

# SGLang: chunked prefill is also enabled by default
... (3 more lines)
```

### 5. `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.9.html` line 293

- **Recommendation:** **DROP**  (severity 85)
- **Why:** Comment-only block (8/8 lines are comments) — prose disguised as code; render as prose or shell snippet
- **Replacement:** Drop the code block; convert the bullet points into a numbered list or a shell snippet (`<pre><code class="lang-bash">`). Comments are not code.

```python
# Step 1: Configure your distributed setup (interactive wizard)
# $ accelerate config
#   Asks: number of GPUs, mixed precision, DeepSpeed, FSDP, etc.
#   Saves config to ~/.cache/huggingface/accelerate/default_config.yaml

# Step 2: Launch your training script on all GPUs
# $ accelerate launch --num_processes 4 train.py

... (2 more lines)
```

### 6. `part-5-multimodal-llms/module-24-vla-models/section-24.7.html` line 132

- **Recommendation:** **DROP**  (severity 85)
- **Why:** Single string-literal block (10/10 lines inside triple-quoted string) — render as <blockquote> or <pre>
- **Replacement:** Replace with `<pre class="prompt-template">...</pre>` or a `<blockquote>` so the reader sees the template as text, not as Python.

```python
SAYCAN_PROMPT = """You are a robot planning assistant. The robot has a fixed ...
Given a goal and the steps already taken, score each candidate skill's likeli...

Goal: {instruction}

Steps so far:
{history}

... (6 more lines)
```

### 7. `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` line 260

- **Recommendation:** **DROP**  (severity 85)
- **Why:** Comment-only block (7/7 lines are comments) — prose disguised as code; render as prose or shell snippet
- **Replacement:** Drop the code block; convert the bullet points into a numbered list or a shell snippet (`<pre><code class="lang-bash">`). Comments are not code.

```python
# Complete solution outline for the self-debugging code agent
# Key components:
# 1. Tool definitions: read_file, write_file, run_command
# 2. Agent loop: call LLM, execute tools, feed results back
# 3. Retry logic with attempt counter and error context
# 4. Metrics collection in a pandas DataFrame
# See section content for the full implementation pattern.
```

### 8. `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html` line 259

- **Recommendation:** **DROP**  (severity 85)
- **Why:** Comment-only block (7/7 lines are comments) — prose disguised as code; render as prose or shell snippet
- **Replacement:** Drop the code block; convert the bullet points into a numbered list or a shell snippet (`<pre><code class="lang-bash">`). Comments are not code.

```python
# Complete solution outline for the browser agent
# Key components:
# 1. Playwright browser setup and MCP tool definitions
# 2. Agent loop with tool calling and result parsing
# 3. Error handling with retry and fallback strategies
# 4. Screenshot-based verification using a vision model
# See the Playwright MCP documentation for server setup.
```

### 9. `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html` line 224

- **Recommendation:** **DROP**  (severity 85)
- **Why:** Comment-only block (9/9 lines are comments) — prose disguised as code; render as prose or shell snippet
- **Replacement:** Drop the code block; convert the bullet points into a numbered list or a shell snippet (`<pre><code class="lang-bash">`). Comments are not code.

```python
# Pagefind ships as an npx-runnable Rust binary, no Node setup required
# 1. Build your static site into ./public (any SSG works)
# 2. Index it:
#    npx pagefind --site public
# 3. Drop the snippet into your template:

# <link rel="stylesheet" href="/pagefind/pagefind-ui.css">
# <script src="/pagefind/pagefind-ui.js"></script>
... (2 more lines)
```

### 10. `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html` line 394

- **Recommendation:** **DROP**  (severity 83)
- **Why:** Single string-literal block (25/27 lines inside triple-quoted string) — render as <blockquote> or <pre>
- **Replacement:** Replace with `<pre class="prompt-template">...</pre>` or a `<blockquote>` so the reader sees the template as text, not as Python.

```python
# Layered system prompt architecture for production use
# Sections: Role, Task, Constraints, Output Format, Examples
SYSTEM_PROMPT = """
## Role
You are a medical coding assistant specializing in ICD-10 classification.
You have 15 years of experience in health information management.
## Task
Given a clinical note, extract the primary diagnosis and assign the
... (19 more lines)
```

### 11. `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html` line 75

- **Recommendation:** **DROP**  (severity 82)
- **Why:** Single string-literal block (9/10 lines inside triple-quoted string) — render as <blockquote> or <pre>
- **Replacement:** Replace with `<pre class="prompt-template">...</pre>` or a `<blockquote>` so the reader sees the template as text, not as Python.

```python
# Few-shot classification example
prompt = """
Review: "This movie was absolutely wonderful!"
Sentiment: Positive
Review: "Terrible acting and a boring plot."
Sentiment: Negative
Review: "The cinematography was stunning but the story fell flat."
Sentiment: Mixed
... (2 more lines)
```

### 12. `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.5.html` line 193

- **Recommendation:** **DROP**  (severity 81)
- **Why:** Comment-only block (13/15 lines are comments) — prose disguised as code; render as prose or shell snippet
- **Replacement:** Drop the code block; convert the bullet points into a numbered list or a shell snippet (`<pre><code class="lang-bash">`). Comments are not code.

```python
# 1. Install and clone the registry; 2. define a model-graded eval YAML;
# 3. run it. Outputs JSONL plus a summary written to /tmp/evallogs/.
pip install evals
# evals/registry/evals/my_judge.yaml
# my-judge:
#   id: my-judge.v1
#   description: GPT-4o judges helpfulness on a 1-5 scale
#   metrics: [accuracy]
... (7 more lines)
```

### 13. `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html` line 178

- **Recommendation:** **DROP**  (severity 80)
- **Why:** Single string-literal block (4/5 lines inside triple-quoted string) — render as <blockquote> or <pre>
- **Replacement:** Replace with `<pre class="prompt-template">...</pre>` or a `<blockquote>` so the reader sees the template as text, not as Python.

```python
# Llama 3 chat template
template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>
What is tokenization?<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
```

### 14. `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html` line 148

- **Recommendation:** **DROP**  (severity 77)
- **Why:** Single string-literal block (6/9 lines inside triple-quoted string) — render as <blockquote> or <pre>
- **Replacement:** Replace with `<pre class="prompt-template">...</pre>` or a `<blockquote>` so the reader sees the template as text, not as Python.

```python
# ChatML template structure
template = """<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
What is tokenization?<|im_end|>
<|im_start|>assistant
"""
# The model generates its response here, ending with <|im_end|>
... (1 more lines)
```

### 15. `part-5-multimodal-llms/module-24-vla-models/section-24.1.html` line 59

- **Recommendation:** **DROP**  (severity 74)
- **Why:** Math formula mislabeled as code — render with KaTeX/MathJax
- **Replacement:** Render with KaTeX/MathJax inline math. The current rendering shows raw ASCII operators which is jarring in a technical book.

```python
p_theta(a_{1:H} | I, l) = prod_{t=1..H} p_theta(a_t | I, l, a_{1:t-1})
```

### 16. `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.3.html` line 83

- **Recommendation:** **DROP**  (severity 61)
- **Why:** YAML/K8s config mis-tagged as lang-python — render as <table> AND fix lang class
- **Replacement:** Re-tag the `<pre><code>` class as `lang-yaml` (so Pygments highlights correctly) and consider replacing each block with a `<table>` of `field | value` for the most critical keys, leaving the full manifest in a collapsible details disclosure.

```python
# compose.yml (or docker-compose.yml)
# Defines a simple API + database stack
services:
api:
build: ./api # Build from local Dockerfile
ports:
- "8000:8000" # Map host port to container port
environment:
... (21 more lines)
```

### 17. `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html` line 84

- **Recommendation:** **DROP**  (severity 58)
- **Why:** YAML/K8s config mis-tagged as lang-python — render as <table> AND fix lang class
- **Replacement:** Re-tag the `<pre><code>` class as `lang-yaml` (so Pygments highlights correctly) and consider replacing each block with a `<table>` of `field | value` for the most critical keys, leaving the full manifest in a collapsible details disclosure.

```python
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
name: h100-80gb
spec:
nodeLabels:
nvidia.com/gpu.product: "NVIDIA-H100-80GB-HBM3"
topology.kubernetes.io/zone: "us-central1-a"
... (31 more lines)
```

### 18. `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.5.html` line 492

- **Recommendation:** **DROP**  (severity 57)
- **Why:** YAML/K8s config mis-tagged as lang-python — render as <table> AND fix lang class
- **Replacement:** Re-tag the `<pre><code>` class as `lang-yaml` (so Pygments highlights correctly) and consider replacing each block with a `<table>` of `field | value` for the most critical keys, leaving the full manifest in a collapsible details disclosure.

```python
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
name: llama-70b-hpa
namespace: llm-serving
spec:
scaleTargetRef:
apiVersion: apps/v1
... (34 more lines)
```

### 19. `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.4.html` line 217

- **Recommendation:** **SIMPLIFY-TO-TABLE**  (severity 54)
- **Why:** Tiny block ending in 1 print() with no library — show as 2-row table
- **Replacement:** Replace the `print()` lines with a two-row HTML table: row 1 lists the expression, row 2 lists the resulting value. The Python ceremony is not the lesson here.

```python
# Comparing DNA tokenization strategies
# Single-nucleotide vs k-mer vs BPE approaches
sequence = "ATCGATCGATCG" * 100 # 1200bp genomic fragment
# Strategy 1: Single nucleotide (Evo-style)
single_tokens = list(sequence)
print(f"Single nucleotide: {len(single_tokens)} tokens, vocab=4")
# Strategy 2: k-mer (original DNABERT, k=6)
kmers = [sequence[i:i+6] for i in range(len(sequence) - 5)]
... (4 more lines)
```

### 20. `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.1.html` line 233

- **Recommendation:** **SIMPLIFY-TO-TABLE**  (severity 51)
- **Why:** Tiny block ending in 1 print() with no library — show as 2-row table
- **Replacement:** Replace the `print()` lines with a two-row HTML table: row 1 lists the expression, row 2 lists the resulting value. The Python ceremony is not the lesson here.

```python
# Create parameterized widgets for training configuration
dbutils.widgets.dropdown("model_name", "meta-llama/Llama-3.1-8B",
    ["meta-llama/Llama-3.1-8B", "mistralai/Mistral-7B-v0.3"])
dbutils.widgets.text("learning_rate", "2e-5")
dbutils.widgets.text("num_epochs", "3")

# Retrieve widget values
model_name = dbutils.widgets.get("model_name")
... (4 more lines)
```

### 21. `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html` line 305

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Implement setup code here
```

### 22. `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html` line 328

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# Complete solution for this lab exercise
# TODO: Full implementation here
```

### 23. `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` line 210

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Define tool schemas for read_file, write_file, run_command
# and implement the agent loop that calls the LLM with tool results
```

### 24. `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` line 219

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Implement retry logic with max_attempts=3
# On each failure, include the error traceback in the next prompt
```

### 25. `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` line 228

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Define 5 challenges with test cases and run the agent on each
```

### 26. `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` line 236

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Track metrics in a DataFrame and implement the give-up path
```

### 27. `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html` line 207

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Initialize Playwright browser and define MCP tool schemas
# Tools: navigate(url), click(selector), type(selector, text), screenshot()
```

### 28. `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html` line 216

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Implement the navigation task with the agent
# Example: search for a product, extract name, price, and rating
```

### 29. `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html` line 225

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Add try/except around tool calls, implement wait-and-retry
# Handle cookie banners, modal dialogs, and timeout errors
```

### 30. `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html` line 234

- **Recommendation:** **DROP**  (severity 40)
- **Why:** Single-line TODO stub — fold into exercise prose
- **Replacement:** Inline the TODO into the exercise prose. A one-line code block adds scrollbar weight without conveying structure.

```python
# TODO: Take screenshot after each action, send to vision model
# for verification before proceeding to the next step
```

## Patterns Observed

Five recurring anti-patterns surfaced. Each is illustrated with one real example from the candidate list.

### Pattern 1: Pure prompt template assigned to a variable

A multi-line triple-quoted string assigned to `SYSTEM_PROMPT` (or `template`, `SAYCAN_PROMPT`, etc.) and then never used in the same block. The reader has to parse Python triple-string syntax around what is actually just prose. Common in chapters 1, 12, and 24.

**Example:** ChatML / Llama-3 chat templates in `section-1.7.html` (lines 148, 178) — the *content* is the special-token sequence, not the `template = """..."""; print(template)` plumbing.

**Remediation:** Replace with `<pre class="prompt-template">` containing only the template text. Reader sees the structure without the assignment ceremony.

### Pattern 2: Comment-only "pseudocode" inside a Python code block

A `<pre><code class="lang-python">` block whose lines are all `#` comments. Frequently shell commands the author wanted in a code box for visual styling, or a numbered list of exercise steps. The Python class is wrong because the Python parser would skip every line.

**Example:** `section-47.4.html` line 196 — six lines of `# pip install garak\n# garak --model_type openai ...`. Should be tagged `lang-bash` (or a shell snippet) and the # marks dropped.

**Remediation:** Re-tag as `lang-bash` (or as `lang-text` for outlines) and remove the comment hashes that exist only to make the lines look like Python.

### Pattern 3: YAML / Kubernetes manifest mis-tagged as Python

Container / orchestration YAML rendered inside `<pre><code class="lang-python">`. The Pygments lexer attempts Python highlighting on `apiVersion: kueue.x-k8s.io/v1beta1` and produces visually noisy output. The block is also leaking indentation in the extracted text (YAML structure looks flat after our strip).

**Example:** All three K8s blocks in `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.3.html` and `section-65.5.html`.

**Remediation:** Re-tag as `lang-yaml`. Pygments will then highlight keys and values appropriately and indentation will be preserved.

### Pattern 4: TODO / placeholder stub as its own code block

A `<pre>` containing just `# TODO: implement X` or two lines of exercise instructions. The visual weight of the code box is disproportionate to the content. Common in exercises in modules 27 and 29.

**Example:** `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` line 210 — `# TODO: Define tool schemas ...` on one line.

**Remediation:** Fold the TODO into the exercise prose as a `<li>` or `<ol>` item. Reserve code blocks for content the reader will actually run or read line by line.

### Pattern 5: Math formula written with ASCII operators in a code block

A one-line block containing `p_theta(a_{1:H} | I, l) = prod_{t=1..H} p_theta(...)` rendered as Python source. The reader sees raw `_`, `{`, and `|` instead of formatted math.

**Example:** `section-24.1.html` line 59, `section-24.4.html` line 113, `section-24.7.html` line 60 (all in `part-5-multimodal-llms/module-24-vla-models`).

**Remediation:** Render with KaTeX (the rest of the book uses it). Inline math goes in `\(...\)`, display math in `\[...\]`.


## Risk Notes

Most candidates are clear-cut. A small number are contestable; flagged below so a human reviewer can override the recommendation.

1. **DNA tokenization (section-75.4.html:217, SIMPLIFY-TO-TABLE).** The block prints three token counts (1200 vs 1195 vs 199) computed from a list comprehension. A pure table would lose the *derivation* (the step size of 6 vs the overlap of 1) that the list comprehension makes visible. **Risk:** demoting to a table erases the pedagogical content. **Suggested action:** leave as code, but add a one-row caption table comparing the three strategies.

2. **Databricks widgets (section-19.1.html:233, SIMPLIFY-TO-TABLE).** Uses `dbutils.widgets`, which IS a real (Databricks) library, but the classifier missed it because `dbutils` is not in the LIB_HANDLE set. The block is genuinely showing how to wire UI widgets to parameter values — KEEP is probably the right call.

3. **Few-shot classification example (section-6.7.html:75, DROP).** The triple-quoted prompt IS the pedagogical artifact (few-shot prompt structure). DROP-to-blockquote is correct, but the *caption* of the existing code block ("Code Fragment 6.7.1") will need to be preserved in any replacement.

4. **TODO stubs (10 candidates across modules 27 and 29).** These are *intentional* hole-fillers for exercises that the reader is meant to fill in. Flagging them as DROP is debatable: the code-block framing signals "this is where your code goes." **Alternative:** keep the code blocks but change the wrapper to `<pre class="exercise-stub">` or similar, so the visual signal is preserved but they are not parsed as production code samples.

5. **`.env` file (section-14.1.html:179, DROP).** Showing the *shape* of a `.env` file is genuinely useful for a reader who has never seen one. Replacing with a table loses the visual cue that this is a plain-text dotenv file. **Alternative:** keep the block but re-tag as `lang-bash` or `lang-dotenv` so it does not get parsed as Python.

6. **All four "comment-only" blocks that show CLI invocations** (garak, accelerate config, evals, pagefind, vLLM) could legitimately be re-tagged as `lang-bash` without dropping anything. The DROP recommendation here is really "drop the wrong lang class" rather than "drop the content."


## Methodology Notes and Reproduction

The classifier and extractor live in `docs/content-audit/_low_value_audit/`:

- `extract_blocks.py` — walks every `section-*.html`, strips Pygments tags, extracts code + 500 char surrounding context, dumps JSONL.
- `classify.py` — applies the hard-KEEP rules first, then DROP / SIMPLIFY / CONVERT rules. Conservative by design: when in doubt, the block is KEEP.
- `code_blocks_classified.jsonl` — full per-block output with reason and severity.

To reproduce: re-run `extract_blocks.py` then `classify.py`. The first step depends on `section_files.txt` (the list of section files to scan).
