# Bibliography Audit

_Repository: `E:/Projects/BookBlogsHome/LLMBook`. Generated 2026-05-15._

_Scope: every `<h2>`/`<h3>` whose text matches Further Reading, Bibliography, References, Citations, Sources, etc., and the markup that follows._


## Headline numbers

- **Total bibliography sections found:** 213
- **Distinct heading texts used:** 1
- **Heading levels:** `<h2>` = 0, `<h3>` = 213

## Distribution by heading name

| Heading text | Count |
|---|---|
| Further Reading | 213 |

## Distribution by markup variant

| Variant | Count |
|---|---|
| `bib-entry-card` | 187 |
| `empty` | 23 |
| `ul-bibliography-list` | 2 |
| `comparison-table` | 1 |

## Outer wrapper tag and class

| Tag | Classes | Count |
|---|---|---|
| `section` | `bibliography` | 212 |
| `None` | `None` | 1 |

## Sub-element coverage among the dominant `bib-entry-card` variant (187 sections)

| Sub-element | Sections using it | Notes |
|---|---|---|
| `bib-ref` (entry title link) | 187 | Should be every card. |
| `bib-annotation` (1-line gloss) | 155 | Roughly the descriptive 'why read it' line. |
| `bib-meta` (e.g. emoji + 'Paper'/'Documentation') | 182 (0 partial, 182 full) | 5 sections **omit it entirely**. |
| `bib-category` (mini section group) | 167 | Used to group entries; not all sections do. |

## Empty bibliography sections (23)

These have a `<h3>Further Reading</h3>` heading inside `<section class="bibliography">` but no entries:

| File |
|---|
| `part-1-foundations/module-00-ml-pytorch-foundations/index.html` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/index.html` |
| `part-1-foundations/module-02-tokenization-subword-models/index.html` |
| `part-1-foundations/module-03-sequence-models-attention/index.html` |
| `part-1-foundations/module-04-transformer-architecture/index.html` |
| `part-1-foundations/module-05-decoding-text-generation/index.html` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/index.html` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.3.html` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.4.html` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.2.html` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.2.html` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.3.html` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.5.html` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` |

## Non-card non-empty variants (3)

| File | Variant | Entries | Notes |
|---|---|---|---|
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html` | `comparison-table` | 6 | Uses a `<table class="comparison-table">` Topic/Paper/Why Read columns. |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.5.html` | `ul-bibliography-list` | 6 | Uses `<ul class="bibliography-list">` with `<li><strong>Author (YEAR)</strong>...</li>` style. |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.3.html` | `ul-bibliography-list` | 6 | Uses `<ul class="bibliography-list">` with `<li><strong>Author (YEAR)</strong>...</li>` style. |

## Top inconsistencies

1. **Heading text is uniform** (every section says `Further Reading`), but the **heading level varies**: `<h3>` = 213, `<h2>` = 0. All sections should pick one level.
2. **Three competing markup styles for entries**: the dominant `bib-entry-card` (187 sections), `ul-bibliography-list` (2), and the one-off `comparison-table` (1). This produces visibly different rendering (boxed cards vs bulleted list vs table).
3. **23 empty bibliographies**: heading present but no entries. These are placeholders that should be either populated or removed (concentrated in Part 6 agentic-ai modules 22/23/25 and the Part-1/2 module `index.html` files).
4. **`bib-meta` icon-tag is inconsistent**: 182 card sections use it on every entry, 0 use it on some entries, and 5 omit it entirely. The icon (e.g. 📄 Paper, 📖 Documentation) appears or disappears unpredictably between chapters.
5. **`bib-category` grouping is optional**: 167 of 187 card sections group entries with `<div class="bib-category">`. Readers in those chapters see grouped subsections; in others, the references are an undifferentiated list.

## Substantive section files (>30 KB) with no bibliography heading (36)

| File | Size (KB) |
|---|---|
| `part-6-agentic-ai/module-21-ai-agents/section-21.6.html` | 102.7 |
| `part-6-agentic-ai/module-21-ai-agents/section-21.5.html` | 94.4 |
| `part-6-agentic-ai/module-21-ai-agents/section-21.1.html` | 91.1 |
| `part-6-agentic-ai/module-21-ai-agents/section-21.3.html` | 78.2 |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 71.4 |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 68.7 |
| `part-6-agentic-ai/module-24-specialized-agents/section-24.4.html` | 66.4 |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 57.4 |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 52.7 |
| `appendices/appendix-k-huggingface-ecosystem/section-k.4.html` | 48.3 |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 47.7 |
| `appendices/appendix-t-distributed-ml/section-t.7.html` | 45.6 |
| `appendices/appendix-s-inference-serving/section-s.5.html` | 43.7 |
| `appendices/appendix-r-experiment-tracking/section-r.3.html` | 42.7 |
| `part-6-agentic-ai/module-21-ai-agents/section-21.2.html` | 41.8 |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` | 41.7 |
| `appendices/appendix-k-huggingface-ecosystem/section-k.1.html` | 41.5 |
| `appendices/appendix-u-docker-containers/section-u.3.html` | 40.5 |
| `part-6-agentic-ai/module-24-specialized-agents/section-24.1.html` | 40.4 |
| `appendices/appendix-v-tooling-ecosystem/section-v.2.html` | 40.4 |
| `appendices/appendix-t-distributed-ml/section-t.5.html` | 39.9 |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 39.5 |
| `appendices/appendix-l-langchain/section-l.3.html` | 38.7 |
| `appendices/appendix-l-langchain/section-l.5.html` | 38.3 |
| `appendices/appendix-l-langchain/section-l.1.html` | 38.1 |
| `appendices/appendix-r-experiment-tracking/section-r.4.html` | 37.7 |
| `appendices/appendix-l-langchain/section-l.4.html` | 37.0 |
| `part-6-agentic-ai/module-24-specialized-agents/section-24.2.html` | 36.6 |
| `appendices/appendix-v-tooling-ecosystem/section-v.3.html` | 35.4 |
| `part-6-agentic-ai/module-21-ai-agents/section-21.4.html` | 34.2 |
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 31.2 |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 30.9 |
| `appendices/appendix-t-distributed-ml/section-t.6.html` | 30.7 |
| `appendices/appendix-t-distributed-ml/section-t.3.html` | 30.4 |
| `appendices/appendix-l-langchain/section-l.2.html` | 29.6 |
| `appendices/appendix-u-docker-containers/section-u.4.html` | 29.4 |

## Recommended canonical pattern

Based on the dominant usage:

```html
<section class="bibliography">
  <h3>Further Reading</h3>
  <div class="bib-category">Optional Group Label</div>
  <div class="bib-entry-card">
    <p class="bib-ref"><a href="..." rel="noopener" target="_blank">Author, A. (YEAR). "Title." <em>Venue</em>.</a></p>
    <p class="bib-annotation">One-sentence gloss of why this matters.</p>
    <span class="bib-meta">📄 Paper</span>
  </div>
  <!-- additional cards... -->
</section>
```

Fix list, in priority order:
1. Standardize heading on `<h3>Further Reading</h3>` (already used by 213 of 213 sections).
2. Convert the 2 `ul.bibliography-list` sections and the 1 `comparison-table` section to `bib-entry-card` cards.
3. Populate or remove the 23 empty bibliographies.
4. Decide whether `bib-meta` icon-tags are required or removed, and apply uniformly across all cards.
5. Decide whether to keep `bib-category` grouping; if yes, mandate it; if no, drop the 167 that have it.

