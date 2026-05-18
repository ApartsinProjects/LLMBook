# Chapter Index Backfill Report

Backfilling the four canonical structural elements that the `CHAPTER_INDEX_LAYOUT`
audit check flagged as missing on chapter-index pages (`part-NN-*/module-NN-*/index.html`).

## Scope

The audit flagged 180 `CHAPTER_INDEX_LAYOUT` issues across 83 chapter-index files:

| Element              | Issues  | Files touched | Status |
|----------------------|---------|---------------|--------|
| Prerequisites        | 83      | 83            | done   |
| Looking-back callout | 55      | 55            | done   |
| Canonical epigraph   | 41      | 41            | done   |
| What's-next block    | 1       | 1             | done   |
| **Total**            | **180** | **83 unique** | **done** |

After the backfill the audit reports `CHAPTER_INDEX_LAYOUT: 0` for all four
canonical elements (verified by re-running `scripts/run_book_audit.py`).

## Authoring script

All edits were produced by `scripts/backfill_chapter_index.py`. The script is
idempotent: it only inserts a missing canonical element, never overwriting an
existing one. The per-chapter content table at the top of the script encodes
agent, persona, epigraph quote, looking-back bridge text, and prerequisite list
items for every flagged chapter.

## Canonical forms used

### Epigraph (inserted directly after the `pagefind-meta-injected` chapter span)

```html
<blockquote class="epigraph">
<p>"One-line quote compressing the chapter's spine."</p>
<span class="agent-avatar-inline" style="background-color: #COLOR;"><img alt="Name" height="28" src="../../front-matter/images/agents/SLUG.png" width="28"/></span><cite>Name, <span class="agent-desc">Persona AI Agent</span></cite>
</blockquote>
```

Avatar paths use `../../front-matter/images/agents/SLUG.png` because chapter-index
files live two directories below the repo root.

### Looking-back callout (inserted after the epigraph)

```html
<div class="callout looking-back">
<div class="callout-title">Looking Back</div>
<p>This chapter built on [prev chapter topic] from <a href="...">Chapter PREV</a>...</p>
</div>
```

### Prerequisites block (canonical, inserted just before `<h2>Sections</h2>`)

```html
<div class="prereqs">
<h3 id="prerequisites">Prerequisites</h3>
<ul>
<li>...</li>
</ul>
</div>
```

For the 28 chapters that already shipped a `Note: Prerequisites` callout-note,
the script converted the existing block in place (preserving its `<ul>` items)
rather than duplicating content. For the remaining 55 chapters the prereqs are
freshly authored from the chapter title and the book's pedagogical sequence.

### What's-next block (only chapter 54 transparency needed it)

```html
<div class="whats-next">
<h3>What's Next?</h3>
<p>This chapter begins with <a href="section-54.6.html">Section 54.6: ...</a>...</p>
</div>
```

## Per-part counts

Counts of CHAPTER_INDEX_LAYOUT issues resolved, by part:

| Part                                  | Files | Epigraph | Looking-back | Prereqs | What's-next |
|---------------------------------------|-------|----------|--------------|---------|-------------|
| Part I LLM Building Blocks            | 6     | 0        | 1            | 6       | 0           |
| Part II Understanding LLMs            | 5     | 0        | 0            | 5       | 0           |
| Part III Working with LLMs            | 4     | 1        | 1            | 4       | 0           |
| Part IV Training & Adaptation         | 5     | 0        | 1            | 5       | 0           |
| Part V Multimodal LLMs                | 6     | 5        | 6            | 6       | 0           |
| Part VI Agentic AI                    | 5     | 0        | 1            | 5       | 0           |
| Part VII Retrieval & IE               | 6     | 4        | 4            | 6       | 0           |
| Part VIII Conversational AI           | 3     | 2        | 2            | 3       | 0           |
| Part IX Evaluation & Observability    | 5     | 3        | 4            | 5       | 0           |
| Part X Security & Runtime Safety      | 5     | 3        | 4            | 5       | 0           |
| Part XI Ethics, Trust, Governance     | 6     | 4        | 6            | 6       | 1           |
| Part XII LLM Systems at Scale         | 5     | 4        | 5            | 5       | 0           |
| Part XIII LLMOps Lifecycle            | 5     | 5        | 5            | 5       | 0           |
| Part XIV Designing LLM Agent Products | 5     | 3        | 4            | 5       | 0           |
| Part XV Industry Applications         | 8     | 7        | 8            | 8       | 0           |
| Part XVI Research Frontiers           | 4     | 0        | 3            | 4       | 0           |
| **Total**                             | **83**| **41**   | **55**       | **83**  | **1**       |

The single what's-next residual is in
`part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/index.html`,
whose section list starts at 54.6 (it is the second half of the watermarking/transparency
split). The block was hand-authored to point at Section 54.6.

## Authoring principles

- **Avatar cast.** Used the established wisdom-council agents only (sage, compass,
  frontier, deploy, eval, rag, prompt, lexica, attn, scale, quant, etc.). Colors
  taken from `scripts/_archive/wave21_epigraph_agentify.py`.
- **Prerequisite chains.** Identified the 1 to 4 nearest pedagogical prerequisites
  per chapter (e.g. Chapter 43 Specialized Evaluation requires Chapter 42 Evaluation
  Foundations plus Chapter 32 RAG plus Chapter 26 Agent Foundations). Linked
  with relative `href` paths from the chapter-index file.
- **Looking-back bridges.** Each callout names the previous chapter topic and
  the conceptual bridge forward into the current chapter. Bridges respect part
  boundaries: Chapter 26 names Part V as its predecessor, Chapter 42 names Part
  VIII, etc.
- **Epigraphs.** Each quote compresses the chapter's spine into one line and is
  attributed to an agent whose persona matches the chapter's theme.
- **No em-dashes.** The script's content table uses commas, semicolons, colons,
  parentheses, or new sentences exclusively.
- **Idempotent.** The script can be re-run safely; it skips chapters that
  already pass each individual check.

## Verification

Before the backfill:

```
prereqs: 83
looking-back: 55
epigraph: 41
whats-next: 1
```

After re-running `python scripts/run_book_audit.py --json`:

```
prereqs: 0
looking-back: 0
epigraph: 0
whats-next: 0
```

`CHAPTER_INDEX_LAYOUT` total dropped from 180 to 0. The overall book audit
issue count dropped from 1646 to 1251 in the same run, with additional
secondary improvements in `SECTION_PAGE_LAYOUT` and `SECTION_STRUCTURE`
because chapter-index improvements unblock those checks.

## Files

- Script: `scripts/backfill_chapter_index.py`
- Touched chapter-index files: 83 (full list in the script's `CHAPTERS` dict)
