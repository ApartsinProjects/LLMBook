# Concept SVG Authoring: Done Report

Publication-quality inline SVG diagrams authored for concept sections that lacked a relevant figure. Each SVG uses the book palette (#1e88e5 / #43a047 / #e53935 / #fb8c00 / #8e24aa), gradient fills (`linearGradient`), drop shadows (`feDropShadow`), rounded corners (`rx`), `system-ui` font, `role="img"` + descriptive `aria-label`, and a prose reference before the figure. All wrapped in `<figure class="diagram">` with a `<figcaption>`. Every SVG validated as well-formed XML; no em dashes; `&#NNN;` used for all symbols.

## Authored (7 figures)

| Section | Figure | Diagram type | Concept shown |
|---|---|---|---|
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html` | Figure 3.3.3 | Data-flow + matrix | Causal self-attention: QKV projection, scaled dot-product score grid, lower-triangular causal mask (future = &#8722;&#8734;), softmax, weighted sum of values. Mirrors the `torch.tril` mask in the code below it. |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html` | Figure 8.3.2 | Process loop | GRPO training loop: one problem &#8594; G sampled solutions &#8594; verifier scores (1/0) &#8594; group-relative advantage A&#7522; = (r&#7522; &#8722; mean)/std &#8594; policy update + KL. Calls out the zero-variance dead zone and "no critic needed". |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | Figure 8.6.2 | Prove-check loop | LLM (intuition engine) proposes a tactic, proof assistant (verification engine) accepts (goal advances / QED) or rejects (backtrack); optional premise retrieval. Binary, unhackable reward. |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.6.html` | Figure 1.6.1 | Before/after + loop | BPE bottom-up merge: characters &#8594; count pairs &#8594; merge most frequent &#8594; ordered merge table; "lowest" loses tokens as "es" then "est" form. Note that WordPiece reuses the loop with likelihood gain. |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | Figure 9.7.1 | Comparison (matrices) | Unstructured (scattered zeros, same shape, needs sparse kernel) vs structured pruning (whole rows/cols removed, smaller dense matrix, faster on any GPU). |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | Figure 13.5.2 | Funnel | Preference-data construction: 4 production signals (thumbs, regeneration, A/B, quality score) &#8594; pair builder &#8594; DPO triplet (prompt / chosen / rejected / margin); bias warning. |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.6.html` | Figure 9.6.2 | Comparison (architecture) | Co-located vs disaggregated inference: shared GPU (phases interfere) vs compute-optimized prompt machines + bandwidth-optimized token machines with KV-cache transfer over RDMA/InfiniBand. |

## Skipped (2 targets, with reasons)

| Section | Reason |
|---|---|
| `part-2-understanding-llms/module-10-interpretability/section-10.6.html` | Pure platforms catalog (title is literally "Platforms"; lists vLLM/TGI/TensorRT/Together/Anyscale/Modal and GPU rental markets). Already has a relevant SVG (Figure 10.6.1, the three-layer inference stack). A second diagram would be noise. |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html` | Already visually saturated: 7 figures (1.4.1 through 1.4.7) covering polysemy, static vs contextual embeddings, the ELMo computation graph, ELMo architecture, the layer information hierarchy, the GPS analogy, and the representation-evolution timeline. Per the idempotency rule, adding more visuals here would be redundant. |

## Renumbering notes
- `section-1.6.html`: new BPE figure inserted before the existing Unigram/byte-level figures, so `fix_caption_order_only.py` renumbered them to 1.6.2 (Unigram Viterbi) and 1.6.3 (byte-level BPE). No prose references to those figure numbers existed, so nothing broke.
- `section-9.7.html`: new contrast figure inserted in 9.7.3 (before the 2:4 figure in document order), so it became 9.7.1 and the 2:4 figure became 9.7.2. Updated my prose reference and the 2:4 image alt-text to match.

## Verification
- All 7 SVGs parsed clean via `xml.dom.minidom`.
- `fix_caption_order_only.py` run on every edited file (figure captions in document order, unique).
