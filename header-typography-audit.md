# Header Typography Audit

Scanned **389** HTML files under `E:/Projects/BookBlogsHome/LLMBook`.

## 1. Summary

- Total in-content headings scanned (h2 + h3 + h4): **4920**

| Level | Total | Housekeeping | Body | Body numbered | Body unnumbered |
|---|---|---|---|---|---|
| `h2` | 2238 | 488 | 1750 | 1515 (86.6%) | 235 (13.4%) |
| `h3` | 2599 | 732 | 1867 | 847 (45.4%) | 1020 (54.6%) |
| `h4` | 83 | 4 | 79 | 0 (0.0%) | 79 (100.0%) |

- Non-left-aligned in-content headings: **0**
- Files with mixed numbering style at same level (excluding housekeeping headings): **37**

Definitions:
- *Housekeeping* headings are conventional labels like Prerequisites, Exercises, Bibliography, What's Next, Key Takeaways. These are conventionally unnumbered everywhere and are exempt from the numbering audit so they don't fire false "mixed" warnings.
- *Body* headings are everything else: the substantive section/subsection headers the user is asking about.
- Headings inside `<header class="chapter-header">` (the centered page-top hero) are excluded entirely; centering there is intentional.

## 2. Non-Left-Aligned Headings

None. Every in-content h2/h3/h4 resolves to left alignment.

## 3. Files With Mixed Numbering (same level, both styles)

Found **37** file/level pairs spanning **36** files with mixed numbered/unnumbered body headings at the same level.

**Part-level breakdown:**

| Part | Files with mixed numbering |
|---|---|
| `part-2-understanding-llms` | 7 |
| `part-4-training-adapting` | 6 |
| `part-5-retrieval-conversation` | 6 |
| `part-1-foundations` | 5 |
| `part-9-safety-strategy` | 4 |
| `part-8-evaluation-production` | 3 |
| `part-7-multimodal-applications` | 2 |
| `appendices` | 1 |
| `part-11-idea-to-product` | 1 |
| `part-3-working-with-llms` | 1 |

**Detailed file list** (one row per file/level pair, single sample from each style; full lists omitted to keep the report concise):

| File | Level | #num | #unnum | Numbered sample | Unnumbered sample |
|---|---|---|---|---|---|
| `appendices/appendix-p-tooling-ecosystem/section-p.1.html` | h3 | 8 | 4 | 2.1 Maturity and Stability | Step 1: Define Your Constraints |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html` | h3 | 2 | 16 | L2 Regularization (Ridge / Weight Decay) | What Are Features? |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | h3 | 19 | 3 | 0.3.1.1 Creating Tensors | Advanced torch.compile: Dynamic Shapes, Fullgra... |
| `part-1-foundations/module-04-transformer-architecture/section-4.4.html` | h3 | 9 | 1 | 4.4.2.1 Streaming Multiprocessors (SMs) | Online Softmax |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | h3 | 9 | 6 | 4.5.1.1 Transformers as Universal Approximators... | Setup |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | h3 | 3 | 10 | 5.3.6.1 How Providers Implement It | How Grammar-Constrained Decoding Works |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.6.html` | h3 | 3 | 5 | 34.6.2.1 Capturing Human Intent | 34.6.4.1intent.md: The Non-Negotiables |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html` | h3 | 4 | 14 | 7.2.4.1 Multi-head Latent Attention (MLA) | Llama 3 and 3.1 |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html` | h3 | 9 | 6 | 7.4.1.1 Cross-Lingual Transfer | Setup |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | h3 | 4 | 6 | 8.6.2.1 Data Extraction from Lean | Setup |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` | h3 | 4 | 7 | 9.3.3.1 Separate Small Model | Why the Output Distribution Is Preserved (Infor... |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` | h3 | 5 | 11 | 9.4.7.1 llama.cpp | Key features: |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | h3 | 3 | 6 | 9.7.1.1 Arithmetic Intensity Analysis | Setup |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | h3 | 4 | 7 | 10.1.1.1 Common Attention Patterns | Setup |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | h3 | 18 | 2 | 13.5.1.1 Classical IE vs. LLM-Based IE | Event Ontologies and Benchmarks |
| `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` | h3 | 1 | 8 | 14.2.1.1 The Self-Instruct Pipeline | Setup |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html` | h3 | 1 | 9 | 15.3.1.1 Complete SFT Script with TRL | Custom Training Loops with Accelerate |
| `part-4-training-adapting/module-16-peft/section-16.1.html` | h3 | 5 | 9 | 16.1.2.1 The Core Decomposition | QLoRA: 4-Bit Quantized LoRA |
| `part-4-training-adapting/module-16-peft/section-16.5.html` | h3 | 8 | 8 | 16.5.1.1 The Teacher-Student Paradigm | Beyond Distillation: Training Efficient Small M... |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html` | h3 | 8 | 4 | 17.1.2.1 Stage 1: Supervised Fine-Tuning (SFT) | Learning Rate and Schedule |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html` | h3 | 8 | 7 | 17.2.2.1 KTO: Kahneman-Tversky Optimization | Setup |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html` | h3 | 3 | 16 | 18.4.8.1 The BERTopic Pipeline | Parsing Tools |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | h3 | 12 | 9 | 19.1.1.1 The Core RAG Loop | Common Chunking Approaches |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html` | h3 | 9 | 8 | 19.2.1.3 Step-Back Prompting | Measuring RAG Improvements with Ragas |
| `part-5-retrieval-conversation/module-19-rag/section-19.6.html` | h3 | 17 | 5 | 19.6.2.1 Core Concepts | Example 1: RAG Pipeline with LangChain LCEL |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | h3 | 4 | 11 | 20.3.8.1 Platform Comparison | Token-Aware Sliding Window |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` | h2 | 13 | 1 | 20.6.1 From Voice Pipelines to Voice Agents | 22.6.X Voice and Multimodal Interfaces (merged ... |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` | h3 | 5 | 5 | 20.5.6.1 The Pipeline Problem | STT Provider Comparison |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.2.html` | h3 | 6 | 1 | 27.2.5.1 The ABSA Pipeline | Domain-Specific Financial Models |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.6.html` | h3 | 6 | 1 | 27.6.5.1 Prompt-Based Style Transfer | Contract Analysis |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.12.html` | h3 | 12 | 6 | 28.12.1.1 MLPerf Training for LLMs | Setup |
| `part-8-evaluation-production/module-29-production-engineering/section-29.3.html` | h3 | 5 | 3 | 29.3.4.1 Memory Persistence Strategies | Rate Limiting with Token Buckets |
| `part-8-evaluation-production/module-29-production-engineering/section-29.9.html` | h3 | 12 | 6 | 29.9.1.1 Kueue: Admission Control and Quotas | Setup |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | h3 | 17 | 8 | 30.1.1 OWASP Top 10 for LLM Applications | Input Sanitization |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` | h3 | 3 | 6 | 30.11.3.1 DP-SGD with Opacus | The FedAvg Algorithm |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.2.html` | h3 | 7 | 1 | 30.2.5.1 Training Data Extraction Attacks | NLI-Based Hallucination Detection |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | h3 | 4 | 1 | 30.3.2.1 Benchmark Coverage and Its Blind Spots | Toxicity and Stereotype Measurement |

## 4. Aggregate Numbering Convention

Across the whole book, the dominant style per heading level:

| Level | Total | Numbered | Unnumbered | Dominant convention |
|---|---|---|---|---|
| `h2` | 1750 | 1515 | 235 | **numbered** (86.6%) |
| `h3` | 1867 | 847 | 1020 | mixed (n=847, u=1020) |
| `h4` | 79 | 0 | 79 | **unnumbered** (100.0%) |

## 5. Recommended Action Plan

**Alignment.** No issues found: every in-content h2/h3/h4 already resolves to left alignment. The reporter's specific case (`part-9-safety-strategy/module-31-strategy-product-roi/section-31.1.html`, 31.1.2 vs 31.1.3) was verified by inspection: both headings are bare `<h2>N.N.N Title</h2>` with identical alignment in HTML and CSS. The reported visual discrepancy is therefore not reproducible from the source; either the user remembered a different file, or the difference was browser-/zoom-specific (e.g. a long heading wrapping to two lines may appear visually different).

**Numbering.** The book has a clear convention at the h2 and h4 levels but is genuinely split at the h3 level (847 numbered vs 1020 unnumbered).

Recommended book-wide rule:

> **`<h2>`: always numbered** with the section's two-or-three-level prefix (e.g. `31.1.2 Use Case Identification`). Observed: 1515/1750 (86.6%) already comply.
>
> **`<h3>`: choose ONE per chapter and stick to it.** The book uses two narrative styles:
> - *Numbered prose-and-code chapters* (parts 3, 6, 7, 8, 9): use deep numbering `28.11.1.1`. Recommended for reference material.
> - *Narrative tutorial chapters* (parts 1, 2, 5): use bare titles like `Online Softmax`. Recommended for prose-heavy sections.
>
> Pick one convention per **chapter/module**, not per individual file. Mixing within a file (37 cases listed in section 3) is the bug to fix; mixing across the book at h3 is acceptable if each chapter is internally consistent.
>
> **`<h4>`: always unnumbered.** All 79 body h4 headings (Captum, LIME, Foundational Papers, etc.) are already unnumbered, so this rule is already universally followed.

**Concrete fix scope.** 37 file/level pairs across 36 files need standardization. Roughly one-third are h3 in part-1 and part-2 tutorial sections that should be made fully unnumbered, and two-thirds are h3 in parts 4, 5, 8, 9 reference sections that should be made fully numbered.

Suggested one-line fix recipe per file (manual review required, since adding a number requires knowing the section's position):

```bash
# Inspect the mixed level inside a single file:
/c/Python314/python -c "
import re, sys
from bs4 import BeautifulSoup
s = BeautifulSoup(open(sys.argv[1], encoding='utf-8'), 'html.parser')
for h in s.select('main.content h3'):
    print(repr(h.get_text(strip=True)))
" path/to/section.html
```

Then, depending on the chapter's chosen convention, either (a) prepend the proper `N.M.K.L ` prefix to bare h3s, or (b) strip the leading number from numbered h3s.

## Methodology

- Script: `scripts/_audit_header_typography.py`
- Parser: BeautifulSoup (html.parser)
- Excluded directories: .claude, KDP, __pycache__, agents, node_modules, pagefind, scripts, templates, vendor
- Excluded by name prefix: `temp_*`; by substring: `backup`/`backups`
- Headings inside `<header class="chapter-header">` are not counted (centered hero is intentional).
- A heading is "non-left" if it has an inline `style="text-align:..."` or `align="..."` attribute, or sits inside an ancestor whose CSS class imposes centering (`chapter-header`, `diagram-caption`, `caption`, `math-display`, `figure-text`) and no closer ancestor in ['callout', 'content', 'objectives', 'outcomes', 'overview', 'part-overview', 'prereqs', 'prerequisites'] resets text-align.
- A heading is "numbered" if its text begins with `N`, `N.M`, `N.M.K`, `A.N`, `A.N.M`, or the same with a trailing `.` or `:`, followed by whitespace and additional text.

