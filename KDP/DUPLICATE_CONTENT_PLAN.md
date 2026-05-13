# Duplicate Content Detection & Consolidation Plan

## Background

The book grew organically across 22 versions. Concepts that were introduced early sometimes get re-introduced in later chapters with similar prose. This bloats page count, weakens authority ("did the author already explain this?"), and creates maintenance debt ("which copy of this paragraph is canonical?").

We need a systematic pass to find the duplicates, decide which copy is canonical, and replace the others with cross-references.

## Detection methodology

Two complementary signals, both run by `_v632_duplicate_content_audit.py` (now running in background):

### Signal 1: paragraph-level MinHash near-duplicates

For every `<p>` paragraph in `<main>` longer than 220 normalized chars:

1. Normalize: lowercase, strip HTML, strip punctuation, collapse whitespace.
2. Build word-level 5-gram shingles.
3. Compute a 64-slot MinHash signature.
4. Compare every pair across DIFFERENT files; flag pairs with Jaccard >= 0.55.

A 5-gram MinHash with that threshold catches:
- Verbatim copy-paste between sections
- Lightly edited reuse (same paragraph with model names swapped)
- Same explanation re-worded with the same key terms

It does NOT flag:
- Two paragraphs explaining the same concept in different words (semantic dupe — needs LLM)
- Short transitional sentences ("In this section we will...")

### Signal 2: repeated heading text

Heading text is a strong tell that two sections cover the same topic. If `<h2>The Attention Mechanism</h2>` appears in three sections, we have three explanations of attention.

The audit emits `duplicate_headings.csv` listing every heading that appears in 2+ files.

### Out of scope for this pass

- **Semantic duplicates** (same concept, different prose): would need embedding-based similarity. Deferred to a v6.40+ pass with `sentence-transformers`.
- **Figure / diagram duplicates**: already audited in v6.11 (lame-diagram audit).
- **Code duplicates**: covered by the separate "trivial code" audit.

## Output

Two CSVs land in `KDP/validation/`:

- `duplicate_content.csv` — pairs of (fileA, fileB, similarity, paragraph previews)
- `duplicate_headings.csv` — repeated headings + the files that contain them

Expected scale based on the book's structure (~5000 paragraphs):
- ~50-150 paragraph pairs above the 0.55 threshold
- ~30-80 headings repeated in 2+ sections

## Consolidation plan (not yet executed)

For each cluster of duplicate paragraphs / repeated headings, decide:

### Decision tree

```
Is the second occurrence intentional reinforcement (e.g., spaced repetition)?
├── YES → leave both. Optionally add a cross-reference: "We first met X in Section 4.1."
└── NO
    ├── Is one copy clearly more authoritative (deeper, more recent, in the canonical chapter)?
    │   ├── YES → delete the weaker copy and replace with a 1-2 sentence pointer.
    │   └── NO  → merge into the canonical chapter; rewrite the other location as a cross-reference.
```

### Canonicality rules

Concept → canonical home (from `concept_anchors.json` in the Hyperlinks Plan):

| Concept                  | Canonical chapter                                  |
|--------------------------|----------------------------------------------------|
| Attention mechanism      | Chapter 4 (Transformer Architecture)               |
| Tokenization             | Chapter 2 (Tokenization & Subword Models)          |
| Pretraining loss/objective | Chapter 6 (Pretraining & Scaling Laws)           |
| RAG architecture         | Chapter 21 (RAG)                                   |
| Tool use / function calling | Chapter 24 (Tool Use & Protocols)               |
| LoRA / QLoRA             | Chapter 16 (PEFT)                                  |
| RLHF / DPO               | Chapter 18 (Alignment)                             |
| Evaluation metrics       | Chapter 30 (Evaluation & Observability)            |
| (full list — 80 entries — lives in `concept_anchors.json`)     |

When a paragraph in Chapter 23 explains attention from scratch, the canonical home is Chapter 4. Replace Chapter 23's paragraph with: "Attention recap — see [Section 4.1](…) for the full derivation. The key property we need here is that …".

### Acceptance criteria for the consolidation pass

- No paragraph pair exceeds Jaccard 0.55 across files
- Every "repeated heading" cluster has a documented decision in `KDP/validation/duplicate_decisions.md` (KEEP-BOTH / MERGE-TO-X / REWRITE-AS-XREF)
- Word count drops by 5-15% (the realistic compression ratio for textbook-style writing with this level of redundancy)
- No factual content lost — every concept still has a fully-explained home, just only one

## Effort estimate

| Phase                                  | Effort  |
|----------------------------------------|---------|
| 1. Run audit (background, this commit) | done    |
| 2. Manual review of duplicate.csv       | 4 hrs   |
| 3. Build canonical home table           | 2 hrs   |
| 4. Write consolidation script           | 3 hrs   |
| 5. Apply + spot-check 20 sample sections| 4 hrs   |
| **Total**                              | ~13 hrs |

Best run AFTER the Hyperlinks Plan — once cross-references exist, consolidation gets cheaper because we are already pointing at canonical homes.

## Order of operations across the three big content passes

1. **Hyperlinks plan** (~13 hrs) — establishes the concept→canonical-page table
2. **Duplicate content** (~13 hrs, this doc) — uses the same table to collapse re-explanations
3. **Hyperlink Pass C manual review** (~4 hrs, part of Hyperlinks plan) — adds "see also" links from consolidated areas

Total integrated effort: ~30 hours of focused work for a book-wide content audit.
