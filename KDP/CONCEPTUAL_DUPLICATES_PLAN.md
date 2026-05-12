# Conceptual Duplicate Content — Detection & Consolidation

## Difference from `DUPLICATE_CONTENT_PLAN.md`

The earlier plan addresses **textual duplicates**: same prose copied or lightly edited across files. That covers verbatim repetition.

This plan addresses **conceptual duplicates**: two passages that explain the SAME concept in DIFFERENT words. The reader meets the same explanation 2-3 times across the book, just rephrased. Symptoms:
- "The Transformer's attention mechanism..." reappears in 5 chapters
- KV cache mechanics explained from scratch in §9.2 AND in §22.x AND in appendix S
- "What is a token" defined in 4 places

These are textually different but semantically duplicate, so the v6.32 string-matching audit cannot find them.

## Detection methodology

### Step 1 — semantic embedding of every section

For each section page (213 sections):
- Strip code blocks, captions, callouts → keep prose only
- Split into paragraphs of ≥ 100 words
- Embed each paragraph with a small sentence-transformer model (`all-MiniLM-L6-v2`, 384-dim, ~80MB, runs CPU in seconds)

Output: `KDP/validation/paragraph_embeddings.npy` (shape ~5000 × 384, ~7.5 MB).

Why a small model: fast (full book in <2 min on CPU), good enough for sentence-level similarity, no GPU needed.

### Step 2 — concept-cluster discovery

Two complementary approaches:

**Approach A: cluster paragraphs by topic**
- HDBSCAN clustering on the embedding matrix with `min_cluster_size=3`
- Each cluster = paragraphs that talk about the same thing
- For each cluster: list the (file, paragraph idx) members, the first 80 chars of each
- Manually inspect clusters of size 4+ across 3+ files → those are conceptual duplicates

**Approach B: known-concept anchored search**
- Use the `concept_anchors.json` from the Hyperlinks Plan (canonical home per concept)
- For each concept, embed its 1-paragraph definition (the canonical one)
- Find all paragraphs in the book with cosine similarity ≥ 0.75 to that definition
- Flag any non-canonical paragraph as a duplicate-explanation candidate

Approach B has fewer false positives because we know what we're looking for.

### Step 3 — manual triage CSV

Generate `KDP/validation/conceptual_duplicates.csv`:

```
concept, canonical_section, duplicate_section, similarity, duplicate_paragraph_preview, action
attention, section-4.1, section-22.1, 0.83, "Self-attention computes a weighted...", REVIEW
attention, section-4.1, section-23.1, 0.79, "The attention head receives queries...", REVIEW
KV cache, section-9.2, section-22.6, 0.81, "To avoid recomputing keys for each...", REVIEW
...
```

The `action` column is filled in by manual review:
- `KEEP-BOTH`: this duplicate is intentional (chapter intro reinforces the concept)
- `MERGE`: rewrite the duplicate as a 1-2 sentence cross-reference to canonical
- `DELETE`: remove the paragraph entirely (its surrounding paragraphs already make the point)

## Consolidation rules

### Rule 1: every concept has ONE canonical home

Defined by the `concept_anchors.json` (Hyperlinks Plan deliverable). When in doubt, the chapter whose TOPIC IS the concept wins. E.g. attention's canonical home is Chapter 4 (Transformer Architecture), not Chapter 22 (which uses attention).

### Rule 2: non-canonical mentions get a "lift, then link" rewrite

Pattern: replace the duplicate paragraph with:
```html
<p>Recap: <strong>concept name</strong> — one-sentence intuition. See
<a href="...">Section X.Y</a> for the full derivation.</p>
```

That preserves the connective-tissue role (the reader still gets the local context) but stops re-explaining.

### Rule 3: refresh callouts before refreshing prose

If the duplicate is in a callout (`callout key-insight` or `callout big-picture`), check whether the callout is REINFORCING the canonical explanation or RE-DERIVING it. Reinforcement is fine; re-derivation should be cut.

### Rule 4: preserve at least one non-canonical depth treatment per concept

Some concepts benefit from being explained twice with different emphases (once mathematically, once operationally). Preserve those — the second pass is intentional pedagogy, not duplication.

Example: gradient descent. Math explanation in Appendix B; engineering-flavored re-introduction in Chapter 6. Both stay.

## What this catches that v6.32 missed

The v6.32 string audit found 1 verbatim duplicate paragraph. This semantic audit will find an estimated **40-150** conceptual duplicates, based on:
- 213 sections × ~5 paragraphs that introduce a named concept = ~1000 concept-introducing paragraphs
- ~60 distinct first-tier concepts in the book (transformer, attention, tokenization, RAG, …)
- Average concept appears in ~3 sections; canonical home is 1 → ~120 non-canonical appearances

## Open questions / risks

- **Embedding model bias**: `all-MiniLM-L6-v2` may incorrectly cluster paragraphs that share TONE but not TOPIC. Mitigation: use Approach B (anchored to known concepts) as the primary tool; Approach A only as a discovery step.
- **Context loss when consolidating**: a paragraph may explain the concept AND introduce a section-specific lemma in the same breath. Crude deletion would lose the lemma. Manual review must preserve the section-specific content.
- **Drift from canonical home**: if Chapter 4's attention explanation is itself stale or shallow (see `SHALLOW_CONTENT_PLAN.md`), pointing more readers at it amplifies the problem. Run the Shallow Content Audit BEFORE this plan.

## Effort estimate

| Phase                                                          | Effort   |
|----------------------------------------------------------------|----------|
| 1. Install sentence-transformers + write embedding script      | 1 hr     |
| 2. Embed all paragraphs                                        | < 1 hr (CPU) |
| 3. HDBSCAN clustering + cluster review (Approach A)            | 4 hrs    |
| 4. Anchored search per concept (Approach B)                    | 3 hrs    |
| 5. Manual triage of 100-150 candidates                         | 8 hrs    |
| 6. Apply lift-and-link rewrites                                | 6 hrs    |
| **Total**                                                      | **~22 hrs** |

## Where this fits in the master plan

```
v7.0  Content Update Plan         50 hrs  →  add 2026 content
v7.1  Hyperlinks Plan             13 hrs  →  build concept anchor table
v7.2  Shallow Content Plan        27 hrs  →  fix depth gaps
v7.3  Conceptual Duplicates       22 hrs  →  collapse re-explanations
v7.4  Textual Duplicates           5 hrs  →  catch any remaining string dupes
                                  -------
                                  ~117 hrs total content audit
```

After v7.x, the book is genuinely connected (every concept has one deep home + many cross-refs to it) and dense (no shopping-list filler).
