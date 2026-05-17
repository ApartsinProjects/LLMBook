# Caption typo audit

Scope: every `.html` page under the project root (KDP, scripts, node_modules, pagefind, templates, agents, vendor, temp_*, *backups* directories excluded). Only these caption containers are inspected: `<div class="comparison-table-title">`, `<figcaption>`, `<div class="code-caption">`, `<div class="diagram-caption">`.

- HTML files scanned: **546**
- Caption elements inspected: **2447**
- Files modified by auto-fix: **0**
- Total auto-fixes applied: **0**
- Unbalanced-paren captions (review queue): **13**
- Colon-style deviations (review queue): **1**

## 1. Summary

| Category | Action | Count |
|---|---|---:|
| Missing space + opening paren (`Xas of YYYY)`) | AUTO-FIX | 0 |
| Unbalanced parentheses in caption text | REPORT | 13 |
| Colon-style deviations after Figure/Code/Table label | REPORT | 1 |
| Trailing punctuation variants (info only) | REPORT | 2447 |

## 2. Auto-fixes applied (Category 1)

_No auto-fixes were necessary._

## 3. Unbalanced parentheses (manual review queue)

Each row shows a caption whose `(` count does not equal its `)` count. These are NOT auto-fixed; resolution depends on intent (missing open vs. missing close, emoticon, table-cell artifact, etc.).

| File | Line | Kind | ( count | ) count | Caption text |
|---|---:|---|---:|---:|---|
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.2.html` | 470 | code-caption | 1 | 0 | Code Fragment 0.2.4: For a single linear layer y = Wx + b with mean-squared-error loss, write the four lines of code to compute (dW. |
| `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.3.html` | 45 | figcaption | 3 | 4 | Figure 58.3.1 : What runs on the device in your pocket and on your desk. The 2026 edge frontier is set by unified memory, not by discrete-GPU VRAM: a 32 GB Mac... |
| `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.3.html` | 86 | code-caption | 1 | 0 | Code Fragment 58.3.1: Apple's iOS 19 ships a routing layer that classifies user requests in three tiers: on-device (the ~3B Apple Foundation Model handles it. |
| `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.4.html` | 47 | figcaption | 3 | 4 | Figure 58.4.1 : Four FlashAttention versions in four years, one per NVIDIA hardware generation. The kernel rewrites itself because the SM architecture and tens... |
| `part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html` | 464 | code-caption | 1 | 0 | Code Fragment 66.1.7: A well-designed guardrail pipeline validates inputs before they reach the model (rejecting prompt injections, enforcing length limits. |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html` | 122 | figcaption | 1 | 2 | Figure 6.4.1 : The data curation pipeline in action: raw web crawls enter one end and (hopefully) clean, high-quality training data emerges from the other. lan... |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | 114 | code-caption | 3 | 2 | Code Fragment 9.7.10: For a matrix multiplication of shapes $(M, K) \times (K, N)$, the computation requires \$2MKN$ FLOPs while transferring \$2(MK + KN +. |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 868 | code-caption | 1 | 0 | Code Fragment 13.5.12: Sketch a 10-line Pydantic schema for a fine-tuning record (system, user, assistant. |
| `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html` | 113 | code-caption | 1 | 0 | Code Fragment 14.2.1: The first-party SDKs always expose provider-specific features first (Anthropic's prompt caching landed in the anthropic SDK months before... |
| `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.3.html` | 368 | code-caption | 1 | 0 | Code Fragment 16.3.11: While TRL's SFTTrainer handles most fine-tuning needs, some workflows require custom training loops (for example, multi-task losses, cus... |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.1.html` | 108 | code-caption | 2 | 1 | Code Fragment m.2.1: Workspaces are organized around three core abstractions: clusters (managed Spark runtimes with optional GPU nodes), notebooks (interactive... |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.2.html` | 1880 | code-caption | 1 | 0 | Code Fragment m.1.2: When the model no longer fits on one GPU, the cheapest upgrade is FSDP (FSDP2, the rewritten API. |
| `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.2.html` | 156 | code-caption | 2 | 1 | Code Fragment f.3.3: Llama Guard (Meta, v3 in 2024, v4 in 2025) is a Llama-based classifier fine-tuned against a configurable taxonomy (violence, self-harm, se... |

## 4. Colon-style deviations after Figure/Code/Table label

Canonical forms (both accepted):

- `<strong>Figure X.Y.Z</strong>: caption text`
- `<strong>Figure X.Y.Z:</strong> caption text`

Deviation reasons: `missing-colon`, `double-colon`, `period-after-label`, `no-colon-no-text`, `label-tag-malformed`.

### label-tag-malformed (1)

| File | Line | Kind | Caption text |
|---|---:|---|---|
| `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html` | 160 | code-caption | Pseudocode 35.3.2: Measuring toxicity disparity across demographic groups using an automated toxicity classifier . The function averages toxicity scores per gr... |

## 5. Trailing punctuation summary (info only)

Overall mix:

| Trailing char | Captions | % |
|---|---:|---:|
| `.` | 1842 | 75.3% |
| `none` | 603 | 24.6% |
| `?` | 2 | 0.1% |

**Dominant style:** `.` (1842 of 2447 captions, 75.3%).
 Captions predominantly end with a period before `</...>`.

Per caption-kind mix:

| Kind | Period `.` | Question `?` | Exclaim `!` | None |
|---|---:|---:|---:|---:|
| comparison-table-title | 331 | 0 | 0 | 0 |
| figcaption | 378 | 2 | 0 | 15 |
| code-caption | 873 | 0 | 0 | 573 |
| diagram-caption | 260 | 0 | 0 | 15 |

---

Audit produced by `scripts/_audit_caption_typos.py`.
