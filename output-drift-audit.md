# Output-Drift Audit
_Read-only static check of every Python code block immediately followed by a `<div class="code-output">` pane. Each detector is conservative: false positives are intentionally minimised, but some discrepancies will still slip through.
- HTML files scanned: **389**
- Code/output pairs found: **615**
- Pairs with unparseable Python (skipped): **68**
- Total findings: **25**
- Files with at least one finding: **15**

## 1. Summary by signal
| Signal | Count |
|---|---|
| `field_name_drift` | 0 |
| `key_count_mismatch` | 0 |
| `format_decimal_drift` | 1 |
| `iteration_count_drift` | 1 |
| `added_print_drift` | 18 |
| `removed_print_drift` | 5 |
| `type_mismatch_drift` | 0 |
| `template_order_drift` | 0 |

## 2. Per-file findings
### `appendices/appendix-d-environment-setup/section-d.6.html`

- L74: **added_print_drift** -- print label '[WARN] No CUDA GPU detected. CPU-only mode.' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `appendices/appendix-n-distributed-ml/section-n.5.html`

- L70: **added_print_drift** -- print label 'Computed embeddings for' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-10-frontiers/module-33-emerging-architectures/section-33.10.html`

- L286: **added_print_drift** -- print label 'Token range' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-3-working-with-llms/module-11-llm-apis/section-11.3.html`

- L192: **added_print_drift** -- print label 'Circuit OPENED after' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print
- L477: **added_print_drift** -- print label 'Budget exceeded for' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-4-training-adapting/module-14-synthetic-data/section-14.2.html`

- L0: **added_print_drift** -- print label 'Error on attempt' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-4-training-adapting/module-14-synthetic-data/section-14.3.html`

- L0: **added_print_drift** -- print label 'Exact dedup' not present in output
- L0: **added_print_drift** -- print label 'Semantic dedup' not present in output
- L0: **added_print_drift** -- print label 'MinHash dedup' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html`

- L236: **added_print_drift** -- print label 'Total mixed dataset' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-4-training-adapting/module-16-peft/section-16.5.html`

- L0: **iteration_count_drift** -- for i in range(2) but output shows 4 lines starting with 'Epoch' (after subtracting 0 outside-loop print prefixes)
  - _fix:_ match `range(N)` to the number of lines in the output

### `part-7-multimodal-applications/module-26-multimodal/section-26.6.html`

- L270: **added_print_drift** -- print label "Landmark '" not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html`

- L406: **removed_print_drift** -- output label 'Pairwise kappas' not printed by any code print()
- L406: **removed_print_drift** -- output label 'Mean kappa' not printed by any code print()
  - _fix:_ either remove the orphan output line or re-add the print

### `part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html`

- L118: **added_print_drift** -- print label 'System fingerprint' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print
- L451: **added_print_drift** -- print label 'System A accuracy' not present in output
- L451: **added_print_drift** -- print label 'Difference' not present in output
- L451: **added_print_drift** -- print label 'Significant at 0.05' not present in output
- L451: **removed_print_drift** -- output label 'Research Question' not printed by any code print()
- L451: **removed_print_drift** -- output label 'Benchmarks' not printed by any code print()
- L451: **removed_print_drift** -- output label 'Ablations' not printed by any code print()
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html`

- L774: **added_print_drift** -- print label 'Anonymized' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.10.html`

- L147: **format_decimal_drift** -- `CO2` formatted with .4f but output shows 1 decimals (504.0)
  - _fix:_ align the `.Nf` format spec with the panel

### `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html`

- L0: **added_print_drift** -- print label 'No adapter for' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

### `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.9.html`

- L313: **added_print_drift** -- print label 'Documentation completeness' not present in output
  - _fix:_ either add the missing line to the output panel or delete the print

## 3. Top 10 worst offenders
### #1: `part-4-training-adapting/module-16-peft/section-16.5.html` (L0, severity 3)

**Signal**: `iteration_count_drift` -- for i in range(2) but output shows 4 lines starting with 'Epoch' (after subtracting 0 outside-loop print prefixes)

**Code (excerpt)**:

```python
# Complete distillation lab: load teacher/student, train with KL
# divergence loss, evaluate perplexity before and after distillation.
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from torch.utils.data import DataLoader
import torch, torch.nn.functional as F, math
from tqdm import tqdm
device = "cuda" if torch.cuda.is_available() else "cpu"
teacher = AutoModelForCausalLM.from_pretrained("gpt2-medium").to(device)
teacher.eval()
for p in teacher.parameters(): p.requires_grad = False
student = AutoModelForCausalLM.from_pretrained("distilgpt2").to(device)
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token
 ...
```

**Output (excerpt)**:

```
Epoch 1: 100%|██████████| 250/250 [01:42<00:00, 2.44it/s]
Epoch 1: 4.7261
Epoch 2: 100%|██████████| 250/250 [01:38<00:00, 2.53it/s]
Epoch 2: 3.8934
Teacher: 24.87
Original: 46.13
Distilled: 36.41
```

### #2: `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.10.html` (L147, severity 3)

**Signal**: `format_decimal_drift` -- `CO2` formatted with .4f but output shows 1 decimals (504.0)

**Code (excerpt)**:

```python
# pip install codecarbon
from codecarbon import EmissionsTracker
tracker = EmissionsTracker(project_name="llm-training")
tracker.start()
# ... your training code here ...
emissions_kg = tracker.stop()
print(f"CO2: {emissions_kg:.4f} kg, Energy: {tracker.final_emissions_data.energy_consumed:.4f} kWh")
```

**Output (excerpt)**:

```
=== Llama 2 7B ===
Total energy: 53,760,000 kWh
CO2 emissions: 21,504.0 tonnes
FLOPs/token: 4.20e+10
Energy/param: 7,680.0000 Wh
Tokens/kWh: 37

=== Llama 2 70B ===
Total energy: 985,497,600 kWh
CO2 emissions: 394,199.0 tonnes
... (3 more lines)
```

### #3: `appendices/appendix-d-environment-setup/section-d.6.html` (L74, severity 1)

**Signal**: `added_print_drift` -- print label '[WARN] No CUDA GPU detected. CPU-only mode.' not present in output

**Code (excerpt)**:

```python
"""
LLM Environment Verification Script
Run this to confirm your setup is ready for the textbook exercises.
"""
import sys

def check_python():
    v = sys.version_info
    assert v.major == 3 and v.minor >= 10, f"Need Python 3.10+, got {v.major}.{v.minor}"
    print(f"[OK] Python {v.major}.{v.minor}.{v.micro}")

def check_torch():
    import torch
    print(f"[OK] PyTorch {torch.__version__}")
... (40 more lines)
```

**Output (excerpt)**:

```
=== LLM Environment Check ===
[OK] Python 3.11.9
[OK] PyTorch 2.5.1
[OK] CUDA 12.4, GPU: NVIDIA A100-SXM4-80GB
     VRAM: 79.6 GB
[OK] Transformers 4.46.2
[OK] datasets 3.1.0
[OK] peft 0.13.2
[OK] trl 0.12.1
[OK] bitsandbytes 0.44.1
... (7 more lines)
```

### #4: `appendices/appendix-n-distributed-ml/section-n.5.html` (L70, severity 1)

**Signal**: `added_print_drift` -- print label 'Computed embeddings for' not present in output

**Code (excerpt)**:

```python
import ray

# Initialize Ray (connects to local cluster or starts one)
ray.init()

# A remote function runs as a distributed task
@ray.remote(num_gpus=1)
def compute_embeddings(texts, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    return model.encode(texts, show_progress_bar=False)

# Launch 4 parallel tasks across available GPUs
text_batches = [texts[i::4] for i in range(4)]
... (5 more lines)
```

**Output (excerpt)**:

```
Megatron-LM configuration:
  Tensor parallel: 2
  Pipeline parallel: 2
  Data parallel: 1
  Total GPUs: 4
  Model: GPT-2 (1.5B parameters)
```

### #5: `part-10-frontiers/module-33-emerging-architectures/section-33.10.html` (L286, severity 1)

**Signal**: `added_print_drift` -- print label 'Token range' not present in output

**Code (excerpt)**:

```python
# Chronos-style time series tokenization
# Continuous values -> scaled -> quantized into discrete bins
import numpy as np
# Simulated daily temperature readings (Celsius)
temperatures = np.array([18.2, 19.1, 17.8, 20.5, 22.1, 21.3, 19.7,
    18.5, 23.0, 24.2, 22.8, 21.0, 19.5, 18.0])
# Step 1: Scale by absolute mean (Chronos normalization)
abs_mean = np.abs(temperatures).mean()
scaled = temperatures / abs_mean
print(f"Abs mean: {abs_mean:.2f}, Scaled range: [{scaled.min():.3f}, {scaled.max():.3f}]")
# Step 2: Quantize into N bins between [-15, +15]
n_bins = 4096
bin_edges = np.linspace(-15, 15, n_bins + 1)
tokens = np.digitize(scaled, bin_edges) - 1 # 0-indexed bin IDs
... (3 more lines)
```

**Output (excerpt)**:

```
Abs mean: 20.26, Scaled range: [0.888, 1.194]
Token IDs (first 7): [2169 2181 2163 2199 2221 2210 2188]
tokens range: [2157, 2221] out of 4096 bins
```

### #6: `part-3-working-with-llms/module-11-llm-apis/section-11.3.html` (L192, severity 1)

**Signal**: `added_print_drift` -- print label 'Circuit OPENED after' not present in output

**Code (excerpt)**:

```python
# Implement a circuit breaker pattern for resilient LLM calls
# Combines budget checks, caching, model fallback, and static responses
import time
from dataclasses import dataclass, field
from enum import Enum
class CircuitState(Enum):
    CLOSED = "closed" # Normal operation
    OPEN = "open" # Provider is down, use fallback
    HALF_OPEN = "half_open" # Testing if provider recovered
@dataclass
class CircuitBreaker:
    failure_threshold: int = 5 # Failures before opening
    recovery_timeout: float = 60.0 # Seconds before testing recovery
    failure_count: int = field(default=0, init=False)
... (41 more lines)
```

**Output (excerpt)**:

```
Circuit state: closed
Ready: True
```

### #7: `part-3-working-with-llms/module-11-llm-apis/section-11.3.html` (L477, severity 1)

**Signal**: `added_print_drift` -- print label 'Budget exceeded for' not present in output

**Code (excerpt)**:

```python
# Enforce per-user token budgets to prevent runaway API costs
# Track usage across configurable time windows (hourly, daily, monthly)
import time
from dataclasses import dataclass, field
from collections import defaultdict
@dataclass
class TokenBudget:
    """Track and enforce token spending limits."""
    limits: dict = field(default_factory=dict) # entity -> max tokens per period
    usage: dict = field(default_factory=lambda: defaultdict(int))
    period_start: dict = field(default_factory=dict)
    period_seconds: float = 86400 # Default: daily budget
    def set_limit(self, entity: str, max_tokens: int):
        self.limits[entity] = max_tokens
... (34 more lines)
```

**Output (excerpt)**:

```
Request allowed. user:alice remaining: 99,520 tokens
user:bob remaining: 2,000 tokens
user:bob can make 500-token request: True
```

### #8: `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` (L0, severity 1)

**Signal**: `added_print_drift` -- print label 'Error on attempt' not present in output

**Code (excerpt)**:

```python
# Self-Instruct generation loop: iteratively grow the instruction
# pool by generating, deduplicating, and quality-filtering examples.
from tqdm import tqdm
def run_self_instruct(seeds, target_count=50, max_attempts=100):
    pool = list(seeds)
    all_instructions = [s['instruction'] for s in pool]
    attempts, duplicates_filtered = 0, 0
    pbar = tqdm(total=target_count, initial=len(pool), desc="Generating")
    while len(pool) < target_count and attempts < max_attempts:
        attempts += 1
        try:
            new_example = generate_new_instruction(pool)
            if is_duplicate(new_example['instruction'], all_instructions):
                duplicates_filtered += 1
... (10 more ...
```

**Output (excerpt)**:

```
Generating: 100%|████████████████████| 30/30 [00:42<00:00, 1.40s/it]

Generated 30 examples (8 duplicates filtered)
```

### #9: `part-4-training-adapting/module-14-synthetic-data/section-14.3.html` (L0, severity 1)

**Signal**: `added_print_drift` -- print label 'Exact dedup' not present in output

**Code (excerpt)**:

```python
# Check for train/test contamination using n-gram overlap detection
# Prevent data leakage that would inflate benchmark scores
import hashlib
from collections import defaultdict
def exact_dedup(examples: list[dict], key: str = "instruction") -> list[dict]:
    """Remove exact duplicates based on normalized text hash."""
    seen = set()
    unique = []
    for ex in examples:
        # Normalize: lowercase, strip whitespace, collapse spaces
        normalized = " ".join(ex[key].lower().split())
        text_hash = hashlib.sha256(normalized.encode()).hexdigest()
        if text_hash not in seen:
            seen.add(text_hash)
... (76 more lines)
```

**Output (excerpt)**:

```
Filtering: 3 -> 1 accepted
 length: 1 removed (33.3%)
 quality: 0 removed (0.0%)
 repetition: 1 removed (33.3%)
```

### #10: `part-4-training-adapting/module-14-synthetic-data/section-14.3.html` (L0, severity 1)

**Signal**: `added_print_drift` -- print label 'Semantic dedup' not present in output

**Code (excerpt)**:

```python
# Check for train/test contamination using n-gram overlap detection
# Prevent data leakage that would inflate benchmark scores
import hashlib
from collections import defaultdict
def exact_dedup(examples: list[dict], key: str = "instruction") -> list[dict]:
    """Remove exact duplicates based on normalized text hash."""
    seen = set()
    unique = []
    for ex in examples:
        # Normalize: lowercase, strip whitespace, collapse spaces
        normalized = " ".join(ex[key].lower().split())
        text_hash = hashlib.sha256(normalized.encode()).hexdigest()
        if text_hash not in seen:
            seen.add(text_hash)
... (76 more lines)
```

**Output (excerpt)**:

```
Filtering: 3 -> 1 accepted
 length: 1 removed (33.3%)
 quality: 0 removed (0.0%)
 repetition: 1 removed (33.3%)
```

## 4. Recommended next steps

- **Re-run flagged code blocks** locally where they are reproducible (non-API examples) and paste the actual stdout back into the `<div class="code-output">` pane.
- **For `key_count_mismatch` findings**, verify whether the example shrunk the returned dict in code but did not update the panel (or vice versa). These are usually quick edits.
- **For `format_decimal_drift` findings**, decide whether the panel or the code is canonical and rewrite the other to match. Watch for `.2f` vs `:.4f` mismatches in metric tables.
- **For `added_print_drift` and `removed_print_drift`** confirm that the print or the output line was deliberately edited; the conservative heuristic will miss many subtle cases.
- **Wire this check into CI** so future code edits without corresponding output panel updates surface immediately.
