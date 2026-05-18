# Forcibly-Merged Section Candidates for Splitting

Surfaced by `GIANT_SECTION` plugin (joint line-count + h2-count thresholds)
combined with `SECTION_PAGE_LAYOUT` duplicate-h2 / "(merged content)" markers.

## Tier 1 — Definite splits (3)

These have explicit evidence of forced merge (duplicate h2 numbering, "(merged content)" markers, or extreme line counts):

| File | Lines | h2 | Evidence | Recommended split |
|---|---:|---:|---|---|
| `module-40-voice-realtime-multimodal/section-40.1.html` | 1522 | 18 | "(merged content)" marker at L599 + duplicate 40.1.1-40.1.7 numbering | Keep first half (Voice Pipelines, 40.1.1-40.1.6); move STT/TTS/Pipelines half to a NEW section-40.6 |
| `module-50-privacy-data-protection/section-50.1.html` | 935 | 18 | Duplicate 50.1.1-50.1.5 numbering | Two clear halves; split into 50.1 + 50.2 |
| `module-52-bias-fairness/section-52.1.html` | 816 | 12 | Duplicate 52.1.1-52.1.4 numbering | Two clear halves; split into 52.1 + 52.2 |

## Tier 2 — Probable splits (4)

Strong P0 signal (both >1200 lines AND >10 h2) but no explicit merge marker. May be legitimately deep, but worth investigation:

| File | Lines | h2 | Notes |
|---|---:|---:|---|
| `module-19-tools-of-the-trade/section-19.2.html` | **2249** | 13 | Largest section in the book by 700+ lines. Likely a fine-tuning-tools omnibus that should split into 2-3 sections |
| `module-37-conversational-ai/section-37.3.html` | 1431 | 12 | Conversational AI memory chapter — likely legitimately deep (sliding window + summary + vector + cross-session + MemGPT) but candidate for splitting memory-mechanisms from memory-products |
| `module-03-transformer-architecture/section-3.1.html` | 1116 | 15 | Transformer fundamentals — many small subsections; could split into "residual stream + attention" and "MLP + normalization + heads" |
| `module-03-transformer-architecture/section-3.3.html` | 1224 | 13 | Same chapter — also large; check overlap with 3.1 |

## Tier 3 — Borderline (8)

Long single-axis (>1000 lines OR >12 h2) but other axis is normal. Likely fine but flagged for review:

- `module-00-ml-pytorch-foundations/section-0.3.html` (1192 lines, 12 h2)
- `module-01-foundations-nlp-text-representation/section-1.7.html` (1010 lines, 10 h2)
- `module-02-sequence-models-attention/section-2.3.html` (1027 lines, 11 h2)
- `module-03-transformer-architecture/section-3.2.html` (1060 lines, 9 h2)
- `module-05-tools-of-the-trade/section-5.2.html` (1198 lines, 11 h2)
- `module-47-adversarial-security-red-team/section-47.1.html` (1335 lines, 2 h2) — long-form, few subsections
- `module-45-tools-of-the-trade/section-45.2.html` (1129 lines, 9 h2)
- `module-31-embeddings-vector-db/section-31.1.html` (1172 lines, 9 h2)

## Tier 4 — Tools-of-the-Trade pattern (15)

These have many h2 (each h2 is a tool/library entry) but reasonable line counts (200-400). This is the canonical Tools-of-the-Trade format; NOT forcibly merged:

- `module-61-scale-tools/section-61.2.html` through `61.5.html` (4 sections, ~205-328 lines each, 13-15 h2 each)
- `module-41-conv-ai-tools/section-41.1` through `41.5.html` (similar)
- `module-56-responsible-ai-tools/section-56.2.html`, `56.3.html`
- `module-59-distributed-training-systems/section-59.3.html`
- `module-30-tools-of-the-trade/section-30.1.html`

**Decision**: leave Tier 4 as-is. They follow the canonical TOTT pattern.

## How to split (recommended procedure)

For each Tier 1 / Tier 2 candidate:

1. **Identify the natural break.** For 40.1: line 599 (the "(merged content)" marker). For 50.1 / 52.1: the point where 50.1.1 / 52.1.1 starts repeating.
2. **Read both halves**, decide which represents the original section and which is the merge graft.
3. **Pick destination**:
   - If next section (e.g. 40.2) is a different topic, create a NEW section file (40.6.html).
   - If the merged content belongs in an existing section, MERGE it there.
4. **Renumber subsection h2 ids** (e.g. second-half 40.1.1 → 40.6.1).
5. **Update chapter-index `<ul class="sections-list">`** to include the new section.
6. **Search book-wide for cross-references** to the moved content and rewrite them.
7. **Re-run plugin audit** to confirm no new structural issues.

## Risks of splitting

- Breaks existing URLs (people who linked to `section-40.1.html#40-1-7-X` may fail).
- May break the linear prev/next chapter-nav chain.
- Cross-references inside the moved content need rewriting (relative paths may change directory depth).

**Recommendation**: do Tier 1 first (clear duplicates, low ambiguity); revisit Tier 2 after confirming Tier 1 worked.
