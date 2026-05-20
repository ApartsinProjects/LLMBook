# Cross-Reference Verification Report (Wave 33)

Date: 2026-05-18
Scope: book-wide HTML (parts, modules, sections, appendices, capstone, front matter)
Files scanned: 563
Section index: 464 distinct section files

Scanner: `scripts/wave33_xref_verify.py`
Findings JSON: `docs/content-audit/_xref_findings.json`

## Summary (after surgical fixes applied this wave)

| Category | Count after fixes | Notes |
|---|---:|---|
| Broken xrefs (target missing on disk) | **0** | No new broken xrefs introduced |
| Stale section labels (cross-chapter drift) | **0** | All 9 fixed this wave |
| Bad anchor text (X.Y -> X.Ya variant drift) | 303 | Top 30 fixed; 303 remaining for future waves |
| Unlinked "Section X.Y" prose mentions | 487 | Reported, not fixed |
| Unlinked "Chapter N" prose mentions | 326 | Reported, not fixed |
| Mismatched concept-link (target heading does not contain concept) | 47 | Reported, needs human review |

Total xref signals scanned: ~1163 (linked anchors with section/chapter labels) plus 813 unlinked prose mentions.

Pre-fix counts were: bad_anchor_text 364, stale_section_labels 23 (under the broader pre-refinement detector; the refined detector reported 9 true cross-chapter cases after filtering false positives in section-card index pages).

## 1. Bad anchor text (303 remaining)

The link points to the right content, but the visible label cites a section
number that no longer matches the target (most commonly because the original
section was split into "a" and "b" sub-files: e.g. 9.1 was split into 9.1a and
9.1b, so "Section 9.1" in old prose now lands at section-9.1.html and the
label should read "Section 9.1").

### Remaining patterns (top)

| Cited | Target | Count |
|---|---|---:|
| 3.1 | 3.1a | 40 |
| 9.1 | 9.1a | 34 |
| 47.1 | 47.1a | 34 |
| 31.1 | 31.1a | 28 |
| 32.1 | 32.1a | 25 |
| 9.4 | 9.4a | 15 |
| 10.6 | 10.6a | 15 |
| 7.1 | 7.1a | 12 |
| 35.1 | 35.1a | 12 |
| 18.2 | 18.2a | 12 |
| 37.5 | 37.5a | 11 |
| 5.2 | 5.2a | 10 |
| 19.2 | 19.10 | 9 |
| 17.5 | 17.5a | 8 |
| 0.3 | 0.3a | 7 |
| 2.3 | 2.3a | 7 |
| 3.2 | 3.2a | 7 |
| 30.2 | 30.2a | 5 |
| 19.3 | 19.3b | 5 |

These are mechanical "append the variant suffix" replacements; safe for a
batch text-edit pass in a future wave.

### Top files (remaining)

| Count | File |
|---:|---|
| 12 | `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html` |
| 9 | `part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.2.html` |
| 7 | `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` |
| 6 | `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html` |
| 6 | `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` |
| 6 | `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.1.html` |
| 5 | `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.3.html` |
| 5 | `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` |
| 5 | `part-2-understanding-llms/module-09-inference-optimization/section-9.8.html` |
| 5 | `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.14.html` |

## 2. Stale section labels (all fixed this wave)

Cases where the link text cited a section number from a different chapter than the link's target. After this wave: 0 remaining.

Fixes applied this wave:

1. `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`: "Section 44.1 (Model Registry and Lifecycle)" -> "Section 66.2 (Model Registry and Lifecycle)"
2. `part-14-applications-of-llms-across-industries/module-70-education-llms/section-70.4.html`: "Section 31.1" -> "Section 32.1"
3. `part-14-applications-of-llms-across-industries/module-72-government-llms/section-72.4.html`: "Section 31.1" -> "Section 32.1"
4. `part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.4.html`: "Section 31.1" -> "Section 32.1"
5. `part-4-training-adaptation/module-17-peft/section-17.3.html`: "Section 44.1: Online Evaluation and Observability" -> "Section 66.2: Online Evaluation and Observability"
6. `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.2.html`: "Section 31.1" -> "Section 32.1"
7. `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.1.html`: "Section 31.1" -> "Section 32.1"
8. `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.2.html`: "Section 31.1" -> "Section 32.1"
9. `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.2.html`: "Section 45.2" -> "Section 44.3"

## 3. Unlinked references in prose (reported, not fixed)

Naked text mentions of "Section X.Y" or "Chapter N" inside `<p>` paragraphs that are NOT wrapped in `<a>` tags. These should be linked in a future wave.

- 487 unlinked "Section X.Y" mentions across the book
- 326 unlinked "Chapter N" mentions across the book

Top files for unlinked section refs:

| Count | File |
|---:|---|
| 10 | `part-5-multimodal-llms/module-20-audio-music-generation/section-20.9.html` |
| 9 | `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.1.html` |
| 9 | `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.3.html` |
| 8 | `part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html` |
| 8 | `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.5.html` |
| 7 | `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.4.html` |
| 7 | `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.1.html` |
| 7 | `part-2-understanding-llms/module-09-inference-optimization/section-9.6.html` |

Top files for unlinked chapter refs:

| Count | File |
|---:|---|
| 11 | `part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.5.html` |
| 8 | `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.5.html` |
| 8 | `part-14-designing-llm-agent-products/module-70-shipping-products/index.html` |
| 7 | `appendices/appendix-a-mathematical-foundations/index.html` |
| 6 | `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.5.html` |
| 6 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.5.html` |
| 6 | `part-6-agentic-ai/module-28-multi-agent-systems/index.html` |

## 4. Mismatched concept-link (47 cases)

Anchors with `class="concept-link"` whose link text (a concept name) does not appear in the target page's `<h1>` or `<h2>`. Sample:

| File | Link text | Target H1/H2 |
|---|---|---|
| `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html` | `perplexity` | `Classical ML Evaluation Metrics` |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html` | `GGUF` | `Interpretability Tools & Transformers Deep Dive` |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.3.html` | `Hugging Face` | `Interpretability Tools & Transformers Deep Dive` |
| `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html` | `Text Generation Inference` | `Platforms` |
| `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html` | `continuous batching` | `Serving Stack & vLLM Deep Dive` |
| `part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html` | `hallucination` | `Why LLMs Hallucinate and How to Catch Them` |

(Three concept-link mismatches will pass after a heading-text update; the rest need human review to decide whether the concept's canonical home should change.)

Note: this is a lightweight heuristic (substring match on H1/H2). The "hallucination" -> "Why LLMs Hallucinate..." case is correctly the canonical home but the substring "hallucination" appears as part of "hallucinate"; the scanner uses a word-prefix check that did not catch it. The full set should be triaged with a relaxed word-stem matcher in a future wave.

## 5. Methodology and constraints

- `module-42` and `module-44` excluded (recent dedup work).
- "Bad anchor text" only flagged when the anchor's plain text is under 120 chars AND not `class="section-card"`. Section-card wrappers contain large blocks of section descriptions that happen to mention other sections (false positive otherwise).
- "Stale section label" is the subset where the cited section's chapter number differs from the target's chapter number.
- Concept-link mismatch uses a permissive heuristic (heading must contain at least one significant word from the concept name).
- Broken xref detection uses absolute-path resolution from each source file's directory.

## 6. Top 30 anchor-text fixes applied this wave

All in `part-1-llm-building-blocks/`:

| # | File | Before | After |
|---:|---|---|---|
| 1 | `module-00-ml-pytorch-foundations/section-0.1.html` | `PyTorch training loops in Section 0.3` | `PyTorch training loops in Section 0.3` |
| 2 | `module-00-ml-pytorch-foundations/section-0.1.html` | `Section 0.3` | `Section 0.3` |
| 3 | `module-00-ml-pytorch-foundations/section-0.2.html` | `Transformer architectures (Section 3.2)` | `Transformer architectures (Section 3.3)` |
| 4 | `module-00-ml-pytorch-foundations/section-0.2.html` | `Section 0.3` | `Section 0.3` |
| 5 | `module-00-ml-pytorch-foundations/section-0.2.html` | `Section 0.3: PyTorch Tutorial` | `Section 0.3: PyTorch Tutorial` |
| 6 | `module-00-ml-pytorch-foundations/section-0.5.html` | `Section 18.2` | `Section 18.3` |
| 7 | `module-01-foundations-nlp-text-representation/section-1.1.html` | `self-attention (covered in Section 2.3)` | `self-attention (covered in Section 2.3)` |
| 8 | `module-01-foundations-nlp-text-representation/section-1.3.html` | `Section 31.1` | `Section 31.1` |
| 9 | `module-01-foundations-nlp-text-representation/section-1.4.html` | `Section 3.1` | `Section 3.1` |
| 10 | `module-02-sequence-models-attention/section-2.1.html` | `Section 3.1` | `Section 3.1` |
| 11 | `module-02-sequence-models-attention/section-2.1.html` | `Section 2.3` | `Section 2.3` |
| 12 | `module-02-sequence-models-attention/section-2.2.html` | `PyTorch (Section 0.3)` | `PyTorch (Section 0.3)` |
| 13 | `module-02-sequence-models-attention/section-2.2.html` | `Section 2.3` | `Section 2.3` |
| 14 | `module-02-sequence-models-attention/section-2.2.html` | `Section 2.3: Scaled Dot-Product & Multi-Head Attention` | `Section 2.3: Scaled Dot-Product & Multi-Head Attention` |
| 15 | `module-02-sequence-models-attention/section-2.3.html` | `Section 3.1` | `Section 3.1` |
| 16 | `module-02-sequence-models-attention/section-2.3.html` | `Section 3.2` | `Section 3.3` |
| 17 | `module-02-sequence-models-attention/section-2.4.html` | `Section 3.1: How a Transformer Computes One Token` | `Section 3.1: How a Transformer Computes One Token` |
| 18 | `module-02-sequence-models-attention/section-2.4.html` | `Section 3.2` | `Section 3.3` |
| 19 | `module-03-transformer-architecture/index.html` | `Section 3.1: Transformer Architecture Deep Dive` | `Section 3.1: Transformer Architecture Deep Dive` |
| 20 | `module-03-transformer-architecture/section-3.1.html` | `Section 2.3` | `Section 2.3` |
| 21 | `module-03-transformer-architecture/section-3.2.html` | `Section 2.3` | `Section 2.3` |
| 22 | `module-03-transformer-architecture/section-3.2.html` | `Section 3.2: Encoder, Decoder, and Encoder-Decoder Architectures` | `Section 3.3: Encoder, Decoder, and Encoder-Decoder Architectures` |
| 23 | `module-03-transformer-architecture/section-3.3.html` | `Section 0.3` | `Section 0.3` |
| 24 | `module-03-transformer-architecture/section-3.3.html` | `Section 2.3` | `Section 2.3` |
| 25 | `module-03-transformer-architecture/section-3.3.html` | `Section 3.1` | `Section 3.1` |
| 26 | `module-03-transformer-architecture/section-3.4.html` | `Section 3.1` | `Section 3.1` |
| 27 | `module-03-transformer-architecture/section-3.5.html` | `Section 7.1` | `Section 7.1` |
| 28 | `module-03-transformer-architecture/section-3.5.html` | `Section 2.3` | `Section 2.3` |
| 29 | `module-03-transformer-architecture/section-3.5.html` | `Section 3.1` | `Section 3.1` |
| 30 | `module-03-transformer-architecture/section-3.5.html` | `Section 3.2` | `Section 3.3` |

All 30 fixes were exact text-label rewrites; no hrefs changed, so target paths remain identical. Pass verification (post-fix): zero broken xrefs introduced.

## 7. Future-wave recommendations

1. Continue the same X.Y -> X.Ya variant-suffix patch across the remaining 303 bad-anchor-text cases. Pattern frequencies above show this is a deterministic batch.
2. Triage the 47 mismatched concept-link cases with human review: for ambiguous concepts (HuggingFace, GGUF, Text Generation Inference), pick the canonical home and re-point all occurrences.
3. Linkify "Section X.Y" and "Chapter N" prose mentions (487 + 326 = 813 total). This is a separate cross-reference wave; the high-leverage hot-spots are listed above.
