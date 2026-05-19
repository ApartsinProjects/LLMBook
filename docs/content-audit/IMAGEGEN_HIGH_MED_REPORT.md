# Image-Generation HIGH + MED Tier Preparation Report

Date: 2026-05-18
Branch: v2.0
Scope: 108 sections (93 HIGH + 15 MED)
Pipeline: per-section illustration prompts authored, placeholder figure markup wired (`data-imagegen-status="pending"`), fun-note callouts inserted for MED tier comic gaps.

## Summary

- HIGH tier figure placeholders inserted: 93
- MED tier comic fun-notes inserted: 15
- Sections audited (figure-sequence regressions): 0
- Em-dashes used: 0 (compliant with style guide)

The Gemini 2.5 Flash Image batch run can be driven directly from `.book-update/imagegen-manifest.jsonl` or `.book-update/imagegen-manifest.csv`.

## Target Selection Logic

HIGH = `figure_count == 0` AND `word_count > 1000` AND `needs_figure` in gap list, capped to 93 by per-part quota (heaviest content parts get larger quotas).

MED = priority parts 1 to 3 with `comic_count == 0` AND `needs_comic` in gap list AND `word_count >= 800`, capped to 15.

## Per-Chapter Breakdown

### HIGH (figure placeholders)

| Part | Count |
|---|---|
| appendices | 1 |
| part-1-llm-building-blocks | 4 |
| part-2-understanding-llms | 6 |
| part-3-working-with-llms | 1 |
| part-4-training-adaptation | 8 |
| part-5-multimodal-llms | 4 |
| part-6-agentic-ai | 6 |
| part-7-retrieval-information-extraction-with-llms | 4 |
| part-8-conversational-ai-with-llms | 1 |
| part-9-llm-evaluation-observability | 12 |
| part-10-llm-security-runtime-safety | 4 |
| part-11-llm-ethics-trust-governance | 5 |
| part-12-llm-systems-at-scale | 3 |
| part-14-designing-llm-agent-products | 10 |
| part-14-applications-of-llms-across-industries | 18 |
| part-15-llm-agentic-ai-research-frontiers | 6 |
| **TOTAL** | **93** |

### MED (fun-note callouts)

| Part | Count |
|---|---|
| part-1-llm-building-blocks | 6 |
| part-2-understanding-llms | 6 |
| part-3-working-with-llms | 3 |
| **TOTAL** | **15** |

## Placeholder Markup Pattern

Each HIGH section receives one `<figure class="illustration">` immediately before the first `<h2>` sub-section, with:

```html
<!-- TODO: imagegen placeholder; batch-fill via Gemini 2.5 Flash Image -->
<figure class="illustration">
  <img alt="..." src="images/fig-X.Y.1-<slug>.jpg"
       width="1200" height="675"
       data-imagegen-prompt="..."
       data-imagegen-status="pending"/>
  <figcaption><strong>Figure X.Y.1</strong>: ...</figcaption>
</figure>
```

All HIGH sections had `figure_count == 0` to begin with, so each placeholder takes the first slot (`Figure X.Y.1`) and no existing figure numbers needed shifting.

## Sample Prompts (one per chapter style)

### Part I, Section 3.6 (Beyond Attention, SSMs, MoE, Modern Variants)

Clean, modern flat-design diagram, Kurzgesagt-meets-XKCD palette. 16:9 ratio, 1200x675. Three labeled panels illustrating "Beyond Attention: SSMs, MoE, and Modern Variants": (1) starting state or core question, (2) key mechanism or transformation, (3) outcome or trade-off. Context: Section 3.3 covered variations on attention itself: positional schemes, sparse and linear attention, and the choice of normalization. Soft gradient background, white callout cards, thin rounded strokes, muted teal-orange-violet accents. No watermarks, no photos, no faces.

### Part VI, Section 27.6 (Efficient Multi-Tool Orchestration)

Clean, modern flat-design diagram, Kurzgesagt-meets-XKCD palette. 16:9 ratio, 1200x675. Three labeled panels illustrating "Efficient Multi-Tool Orchestration and Tool Economy": (1) starting state or core question, (2) key mechanism or transformation, (3) outcome or trade-off. Context: As LLM agents gain access to more tools, the economics of tool use become a first-class engineering concern. Soft gradient background, white callout cards, thin rounded strokes, muted teal-orange-violet accents. No watermarks, no photos, no faces.

### Part IX, Section 42.8 (Long-Context Benchmarks)

Clean, modern flat-design diagram, Kurzgesagt-meets-XKCD palette. 16:9 ratio, 1200x675. Three labeled panels illustrating "Long-Context Benchmarks and Context Extension Methods": (1) starting state or core question, (2) key mechanism or transformation, (3) outcome or trade-off. Context: The "context length" listed on a model card is a theoretical maximum, not a guarantee of effective utilization. Soft gradient background, white callout cards, thin rounded strokes, muted teal-orange-violet accents. No watermarks, no photos, no faces.

### Part XIV, Section 72.5 (Government LLM Vendors)

Clean, modern flat-design diagram, Kurzgesagt-meets-XKCD palette. 16:9 ratio, 1200x675. Three labeled panels illustrating "Government LLM Vendors and Postmortems": (1) starting state or core question, (2) key mechanism or transformation, (3) outcome or trade-off. Context: The government LLM vendor landscape in 2026 sits at the intersection of FedRAMP-authorized cloud providers, specialty defense and intelligence platforms (Palantir, Anduril), Soft gradient background, white callout cards, thin rounded strokes, muted teal-orange-violet accents. No watermarks, no photos, no faces.

### Part XV, Section 75.4 (LLMs as Universal Sequence Machines)

Clean, modern flat-design diagram, Kurzgesagt-meets-XKCD palette. 16:9 ratio, 1200x675. Three labeled panels illustrating "Beyond Text: LLMs as Universal Sequence Machines": (1) starting state or core question, (2) key mechanism or transformation, (3) outcome or trade-off. Context: The transformer architecture was invented for machine translation, but its core mechanism (self-attention over sequences of tokens) is domain-agnostic. Soft gradient background, white callout cards, thin rounded strokes, muted teal-orange-violet accents. No watermarks, no photos, no faces.

## Sample MED Fun-Notes

### Section 3.3 (Transformer Variants and Efficiency): "Encoders, Decoders, and the Tool Shed"

A workshop has three tools that look almost identical at first: a saw cuts in one direction, a plane shaves a flat surface, and a router does both with attachments. Encoder-only models are the saws (read once, classify), decoder-only models are the planes (generate forward), and encoder-decoder models are the routers (read then generate). Pick the wrong one and you can still get the job done; pick the right one and the work becomes effortless.

### Chapter 3 index (Transformer Architecture): "The Architecture That Ate AI"

In 1995 a strange new building called Bilbao Guggenheim opened in northern Spain, and within a decade every museum on Earth was hiring Frank Gehry. The 2017 Transformer paper had the same effect on AI. Every modern LLM, every multimodal model, almost every protein folder is a variation on the same titanium-clad blueprint, and every chapter after this one assumes you can read it.

### Section 1.4 (Contextual Embeddings: ELMo): "One Word, Many Personalities"

Think of the word "bank" as an actor who changes costume between scenes: a financial institution in one act, a riverbank in another, a verb of trust in a third. Word2Vec hired one actor and asked them to play all three roles in the same outfit, which is why the result feels blurry. ELMo finally let the actor change costumes between scenes, which is the entire reason contextual embeddings won.

## Audit Deltas

After insertion the figure-sequence audit returned **0 issues** across all 93 HIGH sections: every section has a contiguous figure sequence starting at 1. Structural validation (well-formed `<figure>` open/close pairs, presence of `data-imagegen-status="pending"`, presence of a `<figcaption>` with `<strong>Figure ...</strong>`) returned 0 issues, except a single false-positive on the appendix where the figure label uses lowercase letters (`Figure a.1.1`), which is the correct house convention.

No em-dashes were introduced.

## Artifacts Produced

| File | Purpose |
|---|---|
| `.book-update/image_high_targets.txt` | List of 93 HIGH section paths |
| `.book-update/image_med_targets.txt` | List of 15 MED section paths |
| `.book-update/imagegen-manifest.jsonl` | Per-section record for batch image generation |
| `.book-update/imagegen-manifest.csv` | Same data, CSV form |
| `.book-update/imagegen_inserter.py` | Per-section placeholder inserter |
| `.book-update/med_analogies.py` | Hand-crafted MED fun-note analogies |
| `.book-update/build_manifest.py` | Manifest builder from current source |

## Next Steps for the Image Batch Run

1. Use `.book-update/imagegen-manifest.jsonl` as input to a Gemini 2.5 Flash Image batch driver.
2. For each HIGH record, send `prompt` to Gemini, save the returned JPG to `filename`, and update the corresponding `<img>` from `data-imagegen-status="pending"` to `data-imagegen-status="generated"`.
3. MED records do not need an image (they are written analogies). The fun-note callouts are already live in the HTML.
