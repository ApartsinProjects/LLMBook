# Pseudocode vs Real Code Classification Audit

This audit walks every in-scope `.html` file in the LLMBook 
and inspects each captioned code block to decide whether the 
label (Pseudocode, Code Fragment, or Algorithm) matches the 
content. Pseudocode boxes should contain idealized, language-
agnostic steps; Code Fragment boxes should contain real Python 
(or real bash/yaml/json/sql/etc.) that an intern could paste 
and run.

Script: `scripts/_audit_pseudocode_classification.py` 
(Python 3.14, BeautifulSoup, `ast.parse` for Python).

Classification rules (in order):

1. Empty body: pseudocode (defensive).
2. Declared `lang-bash`, `lang-yaml`, `lang-json`, `lang-sql`, 
   `lang-dockerfile`, `lang-javascript`, etc.: real_code.
3. Contains lab placeholder (`???`, `# TODO`, `# Hint`, `<<...>>`): 
   real_code (intentional student gap).
4. Has paired line-start `Input:` and `Output:` headers: pseudocode.
5. Three or more pseudocode markers (`for each`, numbered/lettered 
   steps, leftwards-arrow assignment, etc.): pseudocode.
6. Python-ish content: `ast.parse` it; on success classify by 
   real-imports vs placeholder identifier density.
7. Fallback: mark as ambiguous (NOT included in mismatch totals).

## 1. Summary

- Files scanned: **389**
- Captioned code blocks found: **1116**

Captioned blocks by label:

| Label | Count |
|---|---|
| code_fragment | 1099 |
| pseudocode | 17 |

Content classification (independent of label):

| Detected as | Count |
|---|---|
| ambiguous | 50 |
| pseudocode | 19 |
| real_code | 1047 |

Label-vs-content cross-tab:

| Label | Real code | Pseudocode | Ambiguous |
|---|---|---|---|
| pseudocode | 4 | 13 | 0 |
| code_fragment | 1043 | 6 | 50 |
| algorithm | 0 | 0 | 0 |

**Headline mismatch count: 10**

- Pseudocode caption + real code content: **4**
- Code Fragment caption + pseudocode content: **6**
- Algorithm caption + real code content: **0**

## 2. "Pseudocode" labeled but content is real code

These captions tell the reader they're seeing language-agnostic algorithm steps, but the block parses cleanly as Python (often with real library imports). They should be relabeled as *Code Fragment* (or kept as Pseudocode but rewritten to drop real imports and concrete API calls).

### Pseudocode 4.4.6: The FlashAttention tiling algorithm in pseudocode. By processing Q, K, and V in SRAM-sized blocks and 

- File: `part-1-foundations/module-04-transformer-architecture/section-4.4.html:262`
- Source: `callout-title`, lang=`python`
- Detector: parses cleanly
- Caption: Pseudocode 4.4.6: The FlashAttention tiling algorithm in pseudocode. By processing Q, K, and V in SRAM-sized blocks and rescaling partial softmax accumulators on the fly, it computes exact attention while reducing HBM reads from quadratic t

Evidence (first 5 non-blank lines):

```python
# Triton fused softmax kernel: compute softmax in a single GPU pass
# without materializing the full attention matrix in HBM.
@triton.jit
def softmax_kernel(
    output_ptr, input_ptr,
```

### Pseudocode 5.1.2: Each beam: (sequence_tensor, cumulative_log_prob).

- File: `part-1-foundations/module-05-decoding-text-generation/section-5.1.html:171`
- Source: `callout-title`, lang=`python`
- Detector: parses + real imports
- Caption: Pseudocode 5.1.2: Each beam: (sequence_tensor, cumulative_log_prob).

Evidence (first 5 non-blank lines):

```python
# Beam search: maintain beam_width candidate sequences in parallel,
# expand each, score by cumulative log-prob, and prune at every step.
import torch
import torch.nn.functional as F
def beam_search(model, input_ids, beam_width=4, max_new_tokens=50,
```

### Pseudocode 7.3.3: Best-of-N sampling with reward model scoring.

- File: `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html:240`
- Source: `callout-title`, lang=`python`
- Detector: parses cleanly
- Caption: Pseudocode 7.3.3: Best-of-N sampling with reward model scoring.

Evidence (first 5 non-blank lines):

```python
# Compute-optimal inference: choosing strategy based on difficulty
def compute_optimal_inference(
    problem,
    easy_model, # Small, fast model (e.g., 8B)
    hard_model, # Large, expensive model (e.g., 70B)
```

### Pseudocode 29.3.2: Measuring toxicity disparity across demographic groups using an automated toxicity classifier . The f

- File: `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html:159`
- Source: `code-caption`, lang=`python`
- Detector: parses + real imports
- Caption: Pseudocode 29.3.2: Measuring toxicity disparity across demographic groups using an automated toxicity classifier . The function averages toxicity scores per group and flags cases where any group's score significantly exceeds the others, ind

Evidence (first 5 non-blank lines):

```python
# implement measure_toxicity_disparity
# See inline comments for step-by-step details.
from transformers import pipeline
toxicity_classifier = pipeline(
    "text-classification",
```

## 3. "Code Fragment" labeled but content is pseudocode

These captions promise runnable code but the block is informal (`for each X in Y:`, numbered steps, `Input:` / `Output:` header pair, no real imports). Either relabel as *Pseudocode* / *Algorithm*, or rewrite the block as real Python.

Found 6 cases. All listed below:

### Code Fragment 4.4.1: Pseudocode: Online softmax for FlashAttention.

- File: `part-1-foundations/module-04-transformer-architecture/section-4.4.html:255`
- Source: `code-caption`, lang=`python`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 4.4.1: Pseudocode: Online softmax for FlashAttention.

Evidence (first 5 non-blank lines):

```
Input: Q, K, V matrices in HBM; tile sizes Br, Bc fitting in SRAM
Output: O = softmax(QKT / √dk) V, written to HBM
// Partition Q into T/Br row blocks, K and V into T/Bc column blocks
for each Q block Qi (rows i*Br to (i+1)*Br):
    Load Qi from HBM to SRAM
```

### Code Fragment 5.1.1: Forward pass: get logits for next token.

- File: `part-1-foundations/module-05-decoding-text-generation/section-5.1.html:143`
- Source: `code-caption`, lang=`text`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 5.1.1: Forward pass: get logits for next token.

Evidence (first 5 non-blank lines):

```
Input: model M, prompt tokens x, beam width k, max length T
Output: highest-scoring complete sequence
beams = [(x, 0.0)] // each beam: (sequence, cumulative log-prob)
completed = []
for step = 1 to T:
```

### Code Fragment 5.1.3: Pseudocode for beam search decoding. At each step the algorithm expands the top k hypotheses, score

- File: `part-1-foundations/module-05-decoding-text-generation/section-5.1.html:242`
- Source: `code-caption`, lang=`text`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 5.1.3: Pseudocode for beam search decoding. At each step the algorithm expands the top k hypotheses, scores all candidates by cumulative log-probability, prunes back to k, and finally selects the highest-scoring complete seque

Evidence (first 5 non-blank lines):

```
Algorithm: Beam Search Decoding
Input:  model M, prompt tokens x, beam width k, max length T
Output: the most probable continuation y
  beams := [(score=0.0, tokens=x)]               # one initial beam: the prompt
  for t in 1..T:
```

### Code Fragment 7.3.1: Training a smaller student model to mimic a larger teacher model, transferring knowledge while redu

- File: `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html:170`
- Source: `code-caption`, lang=`text`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 7.3.1: Training a smaller student model to mimic a larger teacher model, transferring knowledge while reducing inference cost.

Evidence (first 5 non-blank lines):

```
Input: problem x, generator M, reward model R, sample count N, temperature T
Output: highest-scoring solution y*
candidates = []
for i = 1 to N:
yi = M.generate(x, temperature=T, do_sample=True)
```

### Code Fragment 8.3.1: Simplified PRM that scores each reasoning step. In practice, PRMs use the full hidden state of a la

- File: `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html:268`
- Source: `code-caption`, lang=`python`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 8.3.1: Simplified PRM that scores each reasoning step. In practice, PRMs use the full hidden state of a large language model backbone, and step boundaries are identified by special delimiter tokens rather than newlines.

Evidence (first 5 non-blank lines):

```
Input: policy model pi, problem dataset D, verifier V, num_iterations T
Output: trained policy pi*
1. for iteration = 1 to T:
a. Sample a batch of problems {p_1, ..., p_B} from D
b. for each problem p_i:
```

### Code Fragment 30.3.2: Probing for bias by comparing model outputs across demographic groups to detect systematic differe

- File: `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html:155`
- Source: `code-caption`, lang=`text`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 30.3.2: Probing for bias by comparing model outputs across demographic groups to detect systematic differences in tone, quality, or stereotyped associations.

Evidence (first 5 non-blank lines):

```
Input: demographic groups G = {g1, ..., gk}, prompt templates T, model M, toxicity classifier C, disparity threshold δ
Output: disparity report D with per-group scores and flagged disparities
1. scores = {}
2. for each group gi in G:
a. scores[gi] = []
```

## 4. "Algorithm" labeled but content is real code

Captions reading *Algorithm N.N.N* should be paired with language-agnostic steps. Anything that parses with imports of real libraries belongs in a *Code Fragment*.

_None found._

## 5. Recommended action plan

- **Relabel 4 "Pseudocode" captions whose content is concrete code.** The fastest fix is to change the caption tag to *Code Fragment*; this preserves the existing block. The anchor case `Pseudocode 29.3.2` in `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` is a clean Python snippet that imports `transformers.pipeline` and should be renamed *Code Fragment 30.3.x*.
- **Audit the 6 "Code Fragment" captions whose content is informal/pseudocode-like.** Each one has paired `Input:` / `Output:` headers or many algorithm markers. Either (a) rewrite the block as runnable Python so the *Code Fragment* label is accurate, or (b) relabel the caption as *Pseudocode* / *Algorithm* and move the block into a `<div class="callout algorithm">` for visual distinction.
- For each rename, search nearby section text for the old label number; if the prose says "as shown in Pseudocode 29.3.2", update the cross-reference to "Code Fragment ..." too.
- Several mislabeled *Code Fragment* blocks in section-30.3.html, section-4.4.html, section-5.1.html, section-7.3.html, and section-8.3.html sit immediately before a real-code companion block. Consider re-pairing them so the algorithm box (pseudocode) and its companion code fragment (real Python) have consistent numbering.
- Add the audit script (`scripts/_audit_pseudocode_classification.py`) to the pre-publish checklist so future content drift is caught.
- Re-run after fixes to confirm the headline mismatch count drops to zero.

---

Generated by `scripts/_audit_pseudocode_classification.py`. Detection is heuristic: ambiguous cases (parses but uses placeholder names, or has no language hint and no markers) are intentionally NOT counted in mismatch totals.