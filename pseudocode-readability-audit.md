# Pseudocode Readability & Formatting Audit

Audit of every `<div class="callout algorithm">` block in the LLMBook source tree for readability and formatting consistency. Scored on seven axes: indent consistency, keyword treatment (`<b>` vs Pygments), step numbering, identifier styling, Input/Output declarations, block length, and phase separators.

Script: `scripts/_audit_pseudocode_readability.py` (Python 3.14, BeautifulSoup). READ-ONLY.

- Files scanned: **519**
- Pseudocode blocks found: **21**

## 1. Treatment distribution (rendering pipeline)

| Treatment | Count | Description |
|---|---|---|
| `pyg-python` | 14 | Pygments `lang-python`: real Python code-fragment-style highlighting. |
| `pyg-text-bad` | 3 | Pygments `lang-text`: plain pseudocode tokenized as code, mis-tints numbers/identifiers. |
| `algo-helper` | 4 | Uses `.algo-line-keyword` / `.algo-line-comment` helper spans (book.css already defines them). |
| `bold` | 0 | `<pre><code class="language-none">` with hand-tagged `<b>Input:</b>`, `<b>for</b>`. |
| `mixed` | 0 | Two treatments in same block (e.g. `<b>` plus Pygments spans). |
| `plain` | 0 | No keyword highlighting. |

**Major finding**: the book ships at least four different treatments. `pyg-python` is fine for blocks that contain real Python (FlashAttention tiling, vLLM block table, etc.); `pyg-text-bad` is actively harmful: it tints plain words like `Input`, `for`, `messages`, `Q`, `K` with random Pygments colors and turns step numbers (`1.`, `2.`) into pale-green floats. The two `algo-helper` blocks (section-22.1, section-29.3) use the existing CSS classes the way they were originally designed.

**Recommendation**: convert all `pyg-text-bad` blocks to `algo-helper` style (preserves the existing CSS infrastructure and scales to all 21 blocks).

## 2. Indent consistency

| Verdict | Count |
|---|---|
| OK | 15 |
| surprising | 6 |
| mixed | 0 |

## 3. Per-block matrix

Columns: indent / keyword / numbering / I-O / ident / length.

| # | File:line | Label | Indent | Keyword | Numbering | I-O | Ident | Length | Issues |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `part-1-foundations/module-04-transformer-architecture/section-4.4.html:266` | `4.4.6` | surprising | pyg-python | none | missing-both | plain | dense | 3 |
| 2 | `part-1-foundations/module-05-decoding-text-generation/section-5.1.html:175` | `5.1.2` | OK | pyg-python | none | missing-both | plain | dense | 2 |
| 3 | `part-12-frontiers/module-61-frontier-architectures/section-61.3.html:258` | `32.3.5` | OK | pyg-python | numbered+lettered | OK | plain | OK | 0 |
| 4 | `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html:244` | `8.3.3` | OK | pyg-python | none | missing-both | plain | dense | 2 |
| 5 | `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.3.html:81` | `9.3.4` | OK | pyg-python | partial | OK | plain | OK | 1 |
| 6 | `part-2-understanding-llms/module-10-inference-optimization/section-10.2.html:203` | `-` | OK | pyg-python | none | missing-both | plain | OK | 1 |
| 7 | `part-2-understanding-llms/module-10-inference-optimization/section-10.3.html:59` | `-` | OK | pyg-python | none | missing-both | plain | dense | 2 |
| 8 | `part-4-training-adapting/module-19-peft/section-19.1.html:106` | `-` | OK | pyg-python | none | missing-both | plain | OK | 1 |
| 9 | `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.1.html:234` | `19.1.3` | surprising | algo-helper | numbered+lettered | OK | plain | OK | 1 |
| 10 | `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.5.html:84` | `48.1.1` | OK | algo-helper | numbered+lettered | OK | plain | OK | 0 |
| 11 | `part-5-retrieval-conversation/module-23-rag/section-23.1.html:178` | `22.1.1` | OK | pyg-python | numbered | OK | plain | OK | 0 |
| 12 | `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:291` | `26.1.2` | surprising | algo-helper | numbered+lettered | OK | plain | OK | 1 |
| 13 | `part-6-agentic-ai/module-26-ai-agents/section-26.2.html:65` | `24.3.1` | OK | pyg-python | numbered+lettered | OK | plain | OK | 0 |
| 14 | `part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html:77` | `26.1.1` | surprising | pyg-text-bad | numbered+lettered | OK | plain | OK | 2 |
| 15 | `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html:69` | `27.2.1` | OK | algo-helper | numbered+lettered | OK | plain | OK | 0 |
| 16 | `part-6-agentic-ai/module-28-multi-agent-systems/section-28.2.html:79` | `27.2.1` | OK | pyg-python | numbered+lettered | OK | plain | OK | 0 |
| 17 | `part-8-evaluation-production/module-34-evaluation-observability/section-34.1.html:62` | `-` | OK | pyg-python | none | missing-both | plain | OK | 1 |
| 18 | `part-8-evaluation-production/module-34-evaluation-observability/section-34.2.html:91` | `27.2.1` | OK | pyg-python | numbered+lettered | OK | plain | OK | 0 |
| 19 | `part-8-evaluation-production/module-35-production-engineering/section-35.3.html:76` | `34.3.1` | surprising | pyg-text-bad | partial | OK | plain | OK | 3 |
| 20 | `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html:161` | `-` | OK | pyg-python | none | missing-both | plain | dense | 2 |
| 21 | `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.8.html:68` | `35.8.1` | surprising | pyg-text-bad | numbered+lettered | OK | plain | OK | 2 |

## 4. Per-block detail

### 1. Pseudocode 4.4.6: The FlashAttention tiling algorithm in pseudocode. By processing Q, K, and V in S...

- File: `part-1-foundations/module-04-transformer-architecture/section-4.4.html:266`
- pre class=`-`  code class=`pygments-highlighted lang-python`
- Indent: **surprising** (odd-width indent steps [1])
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **none** (consistent)
- Input/Output: **missing-both** (missing both Input: and Output:)
- Identifier styling: **plain** (consistent)
- Length / phases: **dense** (43 body lines, no blank-line phase separators)
- **Issues**: indent=surprising, io=missing-both, length=dense

Snippet (first 6 lines):

```
import torch
# Triton fused softmax kernel: compute softmax in a single GPU pass
# without materializing the full attention matrix in HBM.
@triton.jit
def softmax_kernel(
output_ptr, input_ptr,
```

### 2. Pseudocode 34.3.1: Token bucket rate limiting algorithm

- File: `part-8-evaluation-production/module-35-production-engineering/section-35.3.html:76`
- pre class=`-`  code class=`lang-text pygments-highlighted`
- Indent: **surprising** (odd-width indent steps [1, 1])
- Keyword treatment: **pyg-text-bad** (consistent)
- Step numbering: **partial** (only 2 numbered steps)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: indent=surprising, keyword=pyg-text-bad, numbering=partial

Snippet (first 6 lines):

```
Input: capacity C, refill rate R (tokens/sec), request cost cost
Output: allow or reject

1. Initialize tokens = C, last_time = now()
2. on each request:
  a. elapsed = now() − last_time
```

### 3. Pseudocode 5.1.2: Each beam: (sequence_tensor, cumulative_log_prob).

- File: `part-1-foundations/module-05-decoding-text-generation/section-5.1.html:175`
- pre class=`-`  code class=`pygments-highlighted lang-python`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **none** (consistent)
- Input/Output: **missing-both** (missing both Input: and Output:)
- Identifier styling: **plain** (consistent)
- Length / phases: **dense** (48 body lines, no blank-line phase separators)
- **Issues**: io=missing-both, length=dense

Snippet (first 6 lines):

```
# Beam search: maintain beam_width candidate sequences in parallel,
# expand each, score by cumulative log-prob, and prune at every step.
import torch
import torch.nn.functional as F
def beam_search(model, input_ids, beam_width=4, max_new_tokens=50,
    eos_token_id=None, length_penalty=1.0):
```

### 4. Pseudocode 8.3.3: Best-of-N sampling with reward model scoring.

- File: `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html:244`
- pre class=`-`  code class=`pygments-highlighted lang-python`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **none** (consistent)
- Input/Output: **missing-both** (missing both Input: and Output:)
- Identifier styling: **plain** (consistent)
- Length / phases: **dense** (36 body lines, no blank-line phase separators)
- **Issues**: io=missing-both, length=dense

Snippet (first 6 lines):

```
# Compute-optimal inference: choosing strategy based on difficulty
def compute_optimal_inference(
    problem,
    easy_model, # Small, fast model (e.g., 8B)
    hard_model, # Large, expensive model (e.g., 70B)
    reward_model, # For scoring candidate solutions
```

### 5. Under the Hood: The Draft-Verify Loop

- File: `part-2-understanding-llms/module-10-inference-optimization/section-10.3.html:59`
- pre class=`-`  code class=`lang-python pygments-highlighted`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **none** (consistent)
- Input/Output: **missing-both** (missing both Input: and Output:)
- Identifier styling: **plain** (consistent)
- Length / phases: **dense** (20 body lines, no blank-line phase separators)
- **Issues**: io=missing-both, length=dense

Snippet (first 6 lines):

```
def speculative_step(target, draft, ids, gamma=5):
    # 1. Draft phase: gamma tokens autoregressively
    qprobs = []
    for _ in range(gamma):
        logits = draft(ids).logits[:,-1,:]
        q = F.softmax(logits, -1)
```

### 6. Pseudocode 26.1.1: Function calling loop

- File: `part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html:77`
- pre class=`-`  code class=`lang-text pygments-highlighted`
- Indent: **surprising** (odd-width indent steps [1, 1])
- Keyword treatment: **pyg-text-bad** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: indent=surprising, keyword=pyg-text-bad

Snippet (first 6 lines):

```
Input: user message M, tool schemas {T1, ..., Tn}, LLM model, max iterations K
Output: final text response

1. messages = [system_prompt, M]
2. for i = 1 to K:
  a. response = LLM(messages, tools={T1, ..., Tn})
```

### 7. Algorithm: Toxicity Disparity Scoring Pipeline

- File: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html:161`
- pre class=`-`  code class=`pygments-highlighted lang-python`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **none** (consistent)
- Input/Output: **missing-both** (missing both Input: and Output:)
- Identifier styling: **plain** (consistent)
- Length / phases: **dense** (21 body lines, no blank-line phase separators)
- **Issues**: io=missing-both, length=dense

Snippet (first 6 lines):

```
# implement measure_toxicity_disparity
# See inline comments for step-by-step details.
from transformers import pipeline
toxicity_classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
```

### 8. Pseudocode 35.8.1: Automated red teaming pipeline

- File: `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.8.html:68`
- pre class=`-`  code class=`lang-text pygments-highlighted`
- Indent: **surprising** (odd-width indent steps [1, 1])
- Keyword treatment: **pyg-text-bad** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: indent=surprising, keyword=pyg-text-bad

Snippet (first 6 lines):

```
Input: target system S, attack library A = {a1, ..., am}, scorer function score(), trials N, severity threshold θ
Output: vulnerability report V with attack success rates and severity rankings

1. V = []
2. for each attack ai in A:
  a. successes = 0
```

### 9. Pseudocode 9.3.4: The RLVR training loop generates solutions, scores them with an automatic verifie...

- File: `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.3.html:81`
- pre class=`-`  code class=`lang-python pygments-highlighted`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **partial** (only 2 numbered steps)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: numbering=partial

Snippet (first 6 lines):

```
Input: policy model pi, problem dataset D, verifier V, num_iterations T
Output: trained policy pi*
1. for iteration = 1 to T:
a. Sample a batch of problems {p_1, ..., p_B} from D
b. for each problem p_i:
Generate solution s_i (reasoning trace + final answer) using pi
```

### 10. Under the Hood: vLLM's Block Table

- File: `part-2-understanding-llms/module-10-inference-optimization/section-10.2.html:203`
- pre class=`-`  code class=`pygments-highlighted lang-python`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **none** (consistent)
- Input/Output: **missing-both** (missing both Input: and Output:)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: io=missing-both

Snippet (first 6 lines):

```
from dataclasses import dataclass
from dataclasses import field
@dataclass
class PhysicalBlock:
    block_id: int
    ref_count: int = 0 # >1 means shared, needs CoW
```

### 11. Under the Hood: LoRA Backward Pass

- File: `part-4-training-adapting/module-19-peft/section-19.1.html:106`
- pre class=`-`  code class=`pygments-highlighted lang-python`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **none** (consistent)
- Input/Output: **missing-both** (missing both Input: and Output:)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: io=missing-both

Snippet (first 6 lines):

```
from torch import nn
import torch
class LoRALinear(nn.Module):
    def __init__(self, d_in, d_out, rank, alpha):
        super().__init__()
        self.W0 = nn.Parameter(torch.randn(d_in, d_out), requires_grad=False)
```

### 12. Pseudocode 19.1.3: PPO training loop for RLHF

- File: `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.1.html:234`
- pre class=`-`  code class=`language-none`
- Indent: **surprising** (odd-width indent steps [1])
- Keyword treatment: **algo-helper** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: indent=surprising

Snippet (first 6 lines):

```
Input: SFT model pi_sft, reward model R, reference policy pi_ref = pi_sft, KL weight beta
Output: aligned policy pi*

1. Initialize policy pi = pi_sft, value network V (same architecture as pi)
2. for each training iteration:
 a. Sample batch of prompts {x_1, ..., x_B}
```

### 13. Pseudocode 26.1.2: This pseudocode formalizes the ReAct agent loop: given a user task T, tool set, ...

- File: `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:291`
- pre class=`-`  code class=`language-none`
- Indent: **surprising** (odd-width indent steps [1, 1])
- Keyword treatment: **algo-helper** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: indent=surprising

Snippet (first 6 lines):

```
Input: user task T, tool set {tool_1, ..., tool_n}, LLM M, max steps S
Output: final answer or action result

1. Initialize context = [system_prompt, T]
2. for step = 1 to S:
  a. Thought: response = M(context)
```

### 14. Under the Hood: Position Bias in LLM-as-Judge

- File: `part-8-evaluation-production/module-34-evaluation-observability/section-34.1.html:62`
- pre class=`-`  code class=`pygments-highlighted lang-python`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **none** (consistent)
- Input/Output: **missing-both** (missing both Input: and Output:)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)
- **Issues**: io=missing-both

Snippet (first 6 lines):

```
def judge_with_swap(judge, question, a, b):
    v1 = judge(question, a, b)      # a first
    v2 = judge(question, b, a)      # b first
    if v1 == "first" and v2 == "second":  return "a wins"
    if v1 == "second" and v2 == "first":  return "b wins"
    return "tie / unreliable"   # judge disagreed with itself
```

### 15. Pseudocode 32.3.5: The Mamba selective scan algorithm, showing how input-dependent parameters (B, C...

- File: `part-12-frontiers/module-61-frontier-architectures/section-61.3.html:258`
- pre class=`-`  code class=`lang-python pygments-highlighted`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)

Snippet (first 6 lines):

```
Input: sequence u = [u1, ..., uL], model parameters (A, B_proj, C_proj, Δ_proj)
Output: output sequence y = [y1, ..., yL]
1. Initialize hidden state h = 0
2. for t = 1 to L:
3. // Input-dependent parameter computation
a. Bt = B_proj(ut) // project input to get B
```

### 16. Pseudocode 48.1.1: The AI Safety via Debate algorithm, where two adversarial models argue opposing ...

- File: `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.5.html:84`
- pre class=`-`  code class=`language-none`
- Indent: **OK** (uniform)
- Keyword treatment: **algo-helper** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)

Snippet (first 6 lines):

```
Input: question Q, debater models DA and DB, human judge J, max rounds R
Output: verified answer with confidence score
1. answerA = DA(Q, role="advocate for YES")
2. answerB = DB(Q, role="advocate for NO")
3. transcript = [(answerA, answerB)]
4. for r = 1 to R:
```

### 17. Pseudocode 22.1.1: The naive RAG pipeline: encode the query, retrieve relevant documents, augment t...

- File: `part-5-retrieval-conversation/module-23-rag/section-23.1.html:178`
- pre class=`-`  code class=`lang-python pygments-highlighted`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **numbered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)

Snippet (first 6 lines):

```
Input: user query q, knowledge base KB, embedding model E, LLM G, top-k parameter k
Output: grounded response with citations
1. Encode: q_vec = E(q) // embed the query
2. Retrieve: docs = top_k_similar(q_vec, KB, k) // vector similarity search
3. Augment: prompt = format(q, docs) // insert docs into prompt template
e.g., "Given the following context: {docs}\n\nAnswer: {q}"
```

### 18. Pseudocode 24.3.1: The plan-and-execute algorithm with replanning. The LLM first decomposes a task ...

- File: `part-6-agentic-ai/module-26-ai-agents/section-26.2.html:65`
- pre class=`-`  code class=`lang-python pygments-highlighted`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)

Snippet (first 6 lines):

```
Input: task T, tool set Tools, LLM M, max replans R
Output: final answer
1. plan = M("Decompose T into numbered steps") // planning phase
2. results = []
3. for step_idx = 0 to len(plan):
a. result = execute_step(plan[step_idx], Tools, results)
```

### 19. Pseudocode 27.2.1: The MCP initialization handshake, host opens a transport, exchanges initialize /...

- File: `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html:69`
- pre class=`-`  code class=`language-none`
- Indent: **OK** (uniform)
- Keyword treatment: **algo-helper** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)

Snippet (first 6 lines):

```
Input: MCP host (LLM application), MCP server (tool provider)
Output: established session with discovered capabilities
1. Host opens transport (stdio pipe or HTTP/SSE connection)
2. Host sends initialize request:
{ protocolVersion, clientInfo, capabilities }
3. Server responds with initialize result:
```

### 20. Pseudocode 27.2.1: The supervisor (hub-and-spoke) pattern as a multi-round dispatch loop. At each r...

- File: `part-6-agentic-ai/module-28-multi-agent-systems/section-28.2.html:79`
- pre class=`-`  code class=`lang-python pygments-highlighted`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)

Snippet (first 6 lines):

```
Input: task T, specialist agents {A1, ..., An} with descriptions, LLM M, max rounds R
Output: synthesized result
1. Initialize results = []
2. for round = 1 to R:
  a. route = M("Given task T and results so far, select next agent or DONE")
  b. if route == DONE:
```

### 21. Pseudocode 27.2.1: Bootstrap confidence interval using the percentile method

- File: `part-8-evaluation-production/module-34-evaluation-observability/section-34.2.html:91`
- pre class=`-`  code class=`lang-python pygments-highlighted`
- Indent: **OK** (uniform)
- Keyword treatment: **pyg-python** (consistent)
- Step numbering: **numbered+lettered** (consistent)
- Input/Output: **OK** (present)
- Identifier styling: **plain** (consistent)
- Length / phases: **OK** (OK)

Snippet (first 6 lines):

```
Input: scores S = [s1, ..., sn], metric function f, resamples B, confidence level α
Output: point estimate, (lower, upper) confidence interval
1. Compute point estimate: θ̂ = f(S)
2. for b = 1 to B:
a. Draw S*b = sample n values from S with replacement
b. Compute θ*b = f(S*b)
```

## 5. CSS treatment for `.callout.algorithm`

Current rule for `.callout.algorithm pre`:

```css
.callout.algorithm pre {
    background: #faf8ff;
    color: #1a1a2e;
    border: 1px solid #c5b8e0;
    border-left: 4px solid #4a55a2;
    padding-left: 1.2em;
    font-family: 'IBM Plex Mono', 'Consolas', 'Courier New', monospace;
    font-variant-numeric: tabular-nums;
    tab-size: 2;
    font-size: 0.88rem;
    line-height: 1.65;
}
```

Helper classes already defined in `book.css` (used by 3 of the 21 blocks; the remaining ~14 `pyg-text-bad` blocks should be converted to use these spans):

```css
.callout.algorithm .algo-line-keyword {
    color: #3949ab;
    font-weight: 700;
}
.callout.algorithm .algo-line-comment {
    color: #6b6b6b;
    font-style: italic;
}
```


Rule for `.lang-text`:

```css
.lang-text .mf,
.callout.algorithm pre code.lang-text .mi,
.callout.algorithm pre code.lang-text .n,
.callout.algorithm pre code.lang-text .nb,
.callout.algorithm pre code.lang-text .o,
.callout.algorithm pre code.lang-text .p {
    color: inherit;
    font-weight: inherit;
}
```

## 6. Punch list

### 6.1 Block-level fixes

Blocks ordered by issue count.

| File:line | Label | Issues |
|---|---|---|
| `part-1-foundations/module-04-transformer-architecture/section-4.4.html:266` | `4.4.6` | indent=surprising, io=missing-both, length=dense |
| `part-8-evaluation-production/module-35-production-engineering/section-35.3.html:76` | `34.3.1` | indent=surprising, keyword=pyg-text-bad, numbering=partial |
| `part-1-foundations/module-05-decoding-text-generation/section-5.1.html:175` | `5.1.2` | io=missing-both, length=dense |
| `part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html:244` | `8.3.3` | io=missing-both, length=dense |
| `part-2-understanding-llms/module-10-inference-optimization/section-10.3.html:59` | `-` | io=missing-both, length=dense |
| `part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html:77` | `26.1.1` | indent=surprising, keyword=pyg-text-bad |
| `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html:161` | `-` | io=missing-both, length=dense |
| `part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.8.html:68` | `35.8.1` | indent=surprising, keyword=pyg-text-bad |
| `part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.3.html:81` | `9.3.4` | numbering=partial |
| `part-2-understanding-llms/module-10-inference-optimization/section-10.2.html:203` | `-` | io=missing-both |
| `part-4-training-adapting/module-19-peft/section-19.1.html:106` | `-` | io=missing-both |
| `part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.1.html:234` | `19.1.3` | indent=surprising |
| `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:291` | `26.1.2` | indent=surprising |
| `part-8-evaluation-production/module-34-evaluation-observability/section-34.1.html:62` | `-` | io=missing-both |

### 6.2 Global CSS additions

Add to `styles/book.css` near the existing `.callout.algorithm pre` rule (around line 1327) to give pseudocode a distinctive, calmer treatment that visually separates it from runnable Code Fragments:

```css
/* Pseudocode: stronger left accent, monospace numbers,
   subtle inset shadow, and tighter line height for scan-ability. */
.callout.algorithm pre {
    /* Existing: background #faf8ff; border #c5b8e0. */
    border-left: 4px solid #4a55a2;        /* match callout accent */
    padding-left: 1.2em;                   /* indent body from rule */
    box-shadow: inset 0 0 0 1px rgba(74, 85, 162, 0.06);
    font-family: 'IBM Plex Mono', 'Consolas', monospace;
    font-variant-numeric: tabular-nums;    /* line up 1./2./10. */
    tab-size: 2;                           /* 2-space tab visualization */
    line-height: 1.6;
}

/* Phase separator: any blank line is rendered with extra top margin
   when wrapped in <p class='algo-phase'></p>, OR add CSS-only via
   a sibling selector if blank lines are preserved in <pre>. */
.callout.algorithm pre code .algo-phase {
    display: block;
    margin-top: 0.6em;
}

/* Input/Output labels: stronger weight, color-tinted */
.callout.algorithm pre b:first-child,
.callout.algorithm pre code > b:first-of-type {
    color: #2e3990;
    letter-spacing: 0.02em;
}

/* Suppress Pygments coloring when language is `lang-text`: numbers
   should not be highlighted as floats, identifiers should not be
   highlighted as Python names. */
.callout.algorithm pre code.lang-text .mf,
.callout.algorithm pre code.lang-text .mi,
.callout.algorithm pre code.lang-text .n,
.callout.algorithm pre code.lang-text .nb,
.callout.algorithm pre code.lang-text .o,
.callout.algorithm pre code.lang-text .p {
    color: inherit;                       /* drop syntax tint */
    font-weight: inherit;
}
.callout.algorithm pre code.lang-text .k,
.callout.algorithm pre code.lang-text .kn {
    color: #3949ab;                       /* keep keyword color */
    font-weight: 700;
}
```

### 6.3 Editorial conventions to enforce

1. **Pipeline choice**: standardize on the existing **algo-helper** treatment: `<pre><code class="language-none">` + `<span class="algo-line-keyword">Input:</span>` + `<span class="algo-line-comment">// note</span>`. The CSS at `book.css:1334-1341` already supports this, and two blocks (section-22.1, section-29.3) already use it. Convert the ~14 `pyg-text-bad` blocks (Pygments tokenizing plain pseudocode as `lang-text`) to this scheme. Keep the ~5 `pyg-python` blocks (FlashAttention tiling, vLLM Block Table, speculative decoding, LoRA backward, position-bias judge) as Pygments since they contain real Python.

2. **Indent**: 2 spaces per nesting level, never tabs. Document in `CONTENT_GUIDELINES.md`.

3. **Numbering**: `1.` for top-level steps, `a.` `b.` `c.` for sub-steps under a numbered step. No mixed Roman/Arabic.

4. **I/O contract**: every pseudocode block opens with two lines: `<b>Input:</b> ...` and `<b>Output:</b> ...`, separated from the body by one blank line.

5. **Identifier styling**: variables and function calls bare; only the *keywords* in `KEYWORDS` get `<b>...</b>`. Drop any `<i>` or `<code>` inside the pseudocode block.

6. **Phase separators**: blocks with >= 20 body lines should use one blank line between init / main loop / cleanup / return phases.

---

Generated by `scripts/_audit_pseudocode_readability.py`. All scores are heuristic; spot-check before mass-editing.