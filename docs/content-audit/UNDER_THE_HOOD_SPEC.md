# "Under the Hood" callout: spec + audit rules

A first-class callout that explains the INTERNAL MECHANISM of a concept,
model, algorithm, or training procedure in prose: architecture, data flow,
why it works, how it is trained. Distinct from the `algorithm` callout (which
carries step-by-step pseudocode) and `key-insight` (which states a takeaway).

## Markup (exact)
```html
<div class="callout under-the-hood">
<div class="callout-title">Under the Hood: <Concept Name></div>
<p><2 to 4 sentences on the internal mechanism. Name the moving parts, the
data flow, and the reason it works. At most ONE formula via $...$ inline or
$$...$$ display. Cite the source paper inline if applicable.></p>
</div>
```
- CSS class `under-the-hood` is defined in `styles/book.css` (slate palette,
  gear icon). No other markup needed.
- Title ALWAYS starts with `Under the Hood: `.
- Keep the body tight (60-130 words). This is an explainer, not a section.
- No em dashes (use commas/semicolons/colons).
- If the host page has math, it must already load KaTeX (it does for any page
  with math after the KaTeX-include fix); a `$...$` formula will render.

## Placement
Insert immediately AFTER the paragraph that first introduces/names the concept
in that section, before the next heading. Add no prose reference line (the box
is self-introducing).

## Per-page budget
Up to 1-3 `under-the-hood` boxes per section page is fine (for 1-3 DISTINCT
concepts). Do not exceed 3 per page; if a page has more gaps, keep the 3
highest-value and leave the rest. Never put two boxes for the same concept on
one page.

## Accuracy: research before authoring
Before writing a box, VERIFY the mechanism. Use WebSearch / WebFetch to check
the source paper or authoritative docs when the detail is non-trivial
(architecture specifics, training recipe, hyperparameters, the exact form of a
loss or update rule). Prefer the primary paper (arXiv) and official docs. Cite
inline (with an arXiv link where available). Never state a mechanism you are
not confident is correct; if research is inconclusive, write a more general
but still-correct description rather than a precise-but-wrong one. No
fabricated numbers, no invented equations.

## Cycle workflow
Run in cycles until every section has been analyzed:
1. Decide the key unexplained concepts/models/algorithms for a batch of
   sections (from the candidate registry).
2. Research each concept's internals (web/papers) as needed.
3. Author the `under-the-hood` box(es), respecting dedup + per-page budget.
4. Validate, then move to the next batch.

## When to ADD a box (all must hold)
1. The section NAMES a key concept / model / algorithm / training method /
   architectural feature.
2. The section's PROSE does NOT already explain how it works internally
   (a name-drop or a one-line "X does Y" without the mechanism = gap).
3. No `under-the-hood` box for the SAME concept exists anywhere else in the
   book (global dedup; see registry).

## When to SKIP
- The mechanism is already explained in prose, a formula, an `algorithm`
  callout, or a deep-dive paragraph in THIS section (e.g. RoPE in 3.5, ALiBi
  in 3.5.2.4, RMSNorm in 3.5.5.3, MoE routing in 7.3, speculative decoding in
  9.4 are all already explained -> SKIP).
- The concept already has an `under-the-hood` box in another section (the
  FIRST/most-foundational section that introduces it wins; later mentions get
  nothing, or at most a cross-ref in existing prose).
- Catalog/list entries in tools-of-the-trade sections (a library name in a
  list is not a "concept introduction").
- Pure-application industry-brief sections (Part 14) that reference a model
  without teaching it.

## Global dedup registry
One concept = one box, book-wide. Canonical concept keys (lowercased,
hyphen-normalized) e.g.: `moe-routing`, `rope`, `flash-attention`,
`speculative-decoding`, `rlhf-ppo`, `dpo`, `grpo`, `lora`, `qlora`,
`kv-cache`, `gqa`, `mla`, `bpe`, `hnsw`, `ivf`, `product-quantization`,
`colbert-maxsim`, `mamba-ssm`, `q-former`, `clip-contrastive`, `diffusion`,
`rag-pipeline`, `reranker-cross-encoder`, `dp-sgd`, `zero-sharding`,
`mixture-of-depths`, `mtp`, `rvq`. Before adding, check the registry file
`.book-update/uth-registry.jsonl` (concept_key -> section). If present, SKIP.

## Examples of GOOD candidates (mechanism usually name-dropped, not taught)
- "AdamW" optimizer mechanics (decoupled weight decay vs L2)
- "Sliding window attention" (Mistral) windowed receptive field
- "Speculative decoding draft model" if a section mentions it without the
  accept/reject rule (note: 9.4 already explains it -> skip there)
- "Constitutional AI" self-critique loop
- "Mixture of Depths" token routing through layers
- "FP8 / mixed precision" scaling, "tensor/pipeline parallelism" splits
- "BM25" term-frequency saturation, "reciprocal rank fusion"
- "Reranker cross-encoder" joint scoring vs bi-encoder
