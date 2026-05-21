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

- Files scanned: **546**
- Captioned code blocks found: **1215**

Captioned blocks by label:

| Label | Count |
|---|---|
| code_fragment | 1199 |
| pseudocode | 16 |

Content classification (independent of label):

| Detected as | Count |
|---|---|
| ambiguous | 64 |
| pseudocode | 19 |
| real_code | 1132 |

Label-vs-content cross-tab:

| Label | Real code | Pseudocode | Ambiguous |
|---|---|---|---|
| pseudocode | 3 | 13 | 0 |
| code_fragment | 1129 | 6 | 64 |
| algorithm | 0 | 0 | 0 |

**Headline mismatch count: 9**

- Pseudocode caption + real code content: **3**
- Code Fragment caption + pseudocode content: **6**
- Algorithm caption + real code content: **0**

## 2. "Pseudocode" labeled but content is real code

These captions tell the reader they're seeing language-agnostic algorithm steps, but the block parses cleanly as Python (often with real library imports). They should be relabeled as *Code Fragment* (or kept as Pseudocode but rewritten to drop real imports and concrete API calls).

### Pseudocode 4.4.6: The FlashAttention tiling algorithm in pseudocode. By processing Q, K, and V in SRAM-sized blocks and 

- File: `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html:266`
- Source: `callout-title`, lang=`python`
- Detector: parses + real imports
- Caption: Pseudocode 4.4.6: The FlashAttention tiling algorithm in pseudocode. By processing Q, K, and V in SRAM-sized blocks and rescaling partial softmax accumulators on the fly, it computes exact attention while reducing HBM reads from quadratic t

Evidence (first 5 non-blank lines):

```python
# Input: queries Q, keys K, values V (each shape [N, d]), block sizes Br x Bc tuned to SRAM
# Output: attention output O = softmax(QK^T / sqrt(d)) V (shape [N, d]) without materializing the full N x N attention matrix in HBM
import torch
# Triton fused softmax kernel: compute softmax in a single GPU pass
# without materializing the full attention matrix in HBM.
```

### Pseudocode 5.1.2: Each beam: (sequence_tensor, cumulative_log_prob).

- File: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html:175`
- Source: `callout-title`, lang=`python`
- Detector: parses + real imports
- Caption: Pseudocode 5.1.2: Each beam: (sequence_tensor, cumulative_log_prob).

Evidence (first 5 non-blank lines):

```python
# Input: model, input_ids (start tokens), beam_width, max_new_tokens, optional eos_token_id, length_penalty
# Output: top-scoring sequence(s) after length-normalized beam search
# Beam search: maintain beam_width candidate sequences in parallel,
# expand each, score by cumulative log-prob, and prune at every step.
import torch
```

### Pseudocode 35.3.2: Measuring toxicity disparity across demographic groups using an automated toxicity classifier . The f

- File: `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html:160`
- Source: `code-caption`, lang=`python`
- Detector: parses + real imports
- Caption: Pseudocode 35.3.2: Measuring toxicity disparity across demographic groups using an automated toxicity classifier . The function averages toxicity scores per group and flags cases where any group's score significantly exceeds the others, ind

Evidence (first 5 non-blank lines):

```python
# Input: model under test, demographic groups G, prompt template T(group), per-group sample size N
# Output: per-group mean toxicity and pairwise disparities, flagging groups with disproportionately toxic continuations
# implement measure_toxicity_disparity
# See inline comments for step-by-step details.
from transformers import pipeline
```

## 3. "Code Fragment" labeled but content is pseudocode

These captions promise runnable code but the block is informal (`for each X in Y:`, numbered steps, `Input:` / `Output:` header pair, no real imports). Either relabel as *Pseudocode* / *Algorithm*, or rewrite the block as real Python.

Found 6 cases. All listed below:

### Code Fragment 3.4.3: The critical algorithmic trick is online softmax: computing the softmax incrementally as new blocks

- File: `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html:237`
- Source: `code-caption`, lang=`text`
- Detector: unclassed with markers
- Caption: Code Fragment 3.4.3: The critical algorithmic trick is online softmax: computing the softmax incrementally as new blocks arrive.

Evidence (first 5 non-blank lines):

```
# Pseudocode: Online softmax for FlashAttention
# Processing one row of the attention matrix in blocks
max_so_far = -infinity
sum_exp = 0
output_accumulator = zeros(d_v)
```

### Code Fragment 3.4.1: Pseudocode: Online softmax for FlashAttention.

- File: `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html:259`
- Source: `code-caption`, lang=`python`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 3.4.1: Pseudocode: Online softmax for FlashAttention.

Evidence (first 5 non-blank lines):

```
Input: Q, K, V matrices in HBM; tile sizes Br, Bc fitting in SRAM
Output: O = softmax(QKT / √dk) V, written to HBM
// Partition Q into T/Br row blocks, K and V into T/Bc column blocks
for each Q block Qi (rows i*Br to (i+1)*Br):
    Load Qi from HBM to SRAM
```

### Code Fragment 4.1.1: Forward pass: get logits for next token.

- File: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html:147`
- Source: `code-caption`, lang=`text`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 4.1.1: Forward pass: get logits for next token.

Evidence (first 5 non-blank lines):

```
Input: model M, prompt tokens x, beam width k, max length T
Output: highest-scoring complete sequence
beams = [(x, 0.0)] // each beam: (sequence, cumulative log-prob)
completed = []
for step = 1 to T:
```

### Code Fragment 4.1.3: Pseudocode for beam search decoding. At each step the algorithm expands the top k hypotheses, score

- File: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html:249`
- Source: `code-caption`, lang=`text`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 4.1.3: Pseudocode for beam search decoding. At each step the algorithm expands the top k hypotheses, scores all candidates by cumulative log-probability, prunes back to k, and finally selects the highest-scoring complete seque

Evidence (first 5 non-blank lines):

```
Algorithm: Beam Search Decoding
Input:  model M, prompt tokens x, beam width k, max length T
Output: the most probable continuation y
  beams := [(score=0.0, tokens=x)]               # one initial beam: the prompt
  for t in 1..T:
```

### Code Fragment 52.1.2: Probing for bias by comparing model outputs across demographic groups to detect systematic differe

- File: `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html:156`
- Source: `code-caption`, lang=`text`
- Detector: Input/Output algorithm header pair
- Caption: Code Fragment 52.1.2: Probing for bias by comparing model outputs across demographic groups to detect systematic differences in tone, quality, or stereotyped associations.

Evidence (first 5 non-blank lines):

```
Input: demographic groups G = {g1, ..., gk}, prompt templates T, model M, toxicity classifier C, disparity threshold δ
Output: disparity report D with per-group scores and flagged disparities
1. scores = {}
2. for each group gi in G:
a. scores[gi] = []
```

### Code Fragment 8.3.1: Simplified PRM that scores each reasoning step. In practice, PRMs use the full hidden state of a la

- File: `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html:271`
- Source: `code-caption`, lang=`text`
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

## 4. "Algorithm" labeled but content is real code

Captions reading *Algorithm N.N.N* should be paired with language-agnostic steps. Anything that parses with imports of real libraries belongs in a *Code Fragment*.

_None found._

## 5. Recommended action plan

- **Relabel 3 "Pseudocode" captions whose content is concrete code.** The fastest fix is to change the caption tag to *Code Fragment*; this preserves the existing block. The anchor case `Pseudocode 29.3.2` in `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` is a clean Python snippet that imports `transformers.pipeline` and should be renamed *Code Fragment 30.3.x*.
- **Audit the 6 "Code Fragment" captions whose content is informal/pseudocode-like.** Each one has paired `Input:` / `Output:` headers or many algorithm markers. Either (a) rewrite the block as runnable Python so the *Code Fragment* label is accurate, or (b) relabel the caption as *Pseudocode* / *Algorithm* and move the block into a `<div class="callout algorithm">` for visual distinction.
- For each rename, search nearby section text for the old label number; if the prose says "as shown in Pseudocode 29.3.2", update the cross-reference to "Code Fragment ..." too.
- Several mislabeled *Code Fragment* blocks in section-30.3.html, section-4.4.html, section-5.1.html, section-7.3.html, and section-8.3.html sit immediately before a real-code companion block. Consider re-pairing them so the algorithm box (pseudocode) and its companion code fragment (real Python) have consistent numbering.
- Add the audit script (`scripts/_audit_pseudocode_classification.py`) to the pre-publish checklist so future content drift is caught.
- Re-run after fixes to confirm the headline mismatch count drops to zero.

---

Generated by `scripts/_audit_pseudocode_classification.py`. Detection is heuristic: ambiguous cases (parses but uses placeholder names, or has no language hint and no markers) are intentionally NOT counted in mismatch totals.