# Cross-Reference Hyperlinks Plan

## Goal

Turn the book from a stack of independent chapters into a connected knowledge graph. When a reader encounters a concept, they should be one click away from:

- Where it was **first defined**
- Where it is **deeply explained**
- Where it is **used in practice**
- Where it is **revisited or extended**

The web edition is already a hypertext; we just are not exploiting it. A typical chapter has < 10 cross-references; it should have 30-60.

## Why now

Three triggers:
1. **Layout fixes are done** (v6.20-v6.29). The skeleton is stable; we can edit content safely.
2. **Pagefind search is live** (v6.10-v6.18). Search proves the cross-references exist mentally; explicit links make them clickable.
3. **Bibliography pass is complete** (v6.23, v6.27). External references are healthy; now polish internal ones.

## Three-pass strategy

### Pass A — Concept anchor table (one-time investment)

Build `KDP/validation/concept_anchors.json`. Schema:

```json
{
  "concept_slug": {
    "display": "Attention Mechanism",
    "synonyms": ["self-attention", "scaled dot-product attention", "multi-head attention", "MHA"],
    "primary_definition": "part-1-foundations/module-04-transformer-architecture/section-4.1.html",
    "deep_explanation": "part-1-foundations/module-04-transformer-architecture/section-4.1.html#anchor",
    "applications": [
      "part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html",
      "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.4.html"
    ],
    "extensions": [
      "part-2-understanding-llms/module-09-inference-optimization/section-9.2.html"
    ]
  }
}
```

Initial concept set (~80 entries):
- ML basics: gradient descent, backprop, overfitting, regularization, batch normalization, dropout
- NLP: tokenization (BPE / WordPiece / SentencePiece), embeddings, perplexity, beam search
- Architecture: attention (self / cross / multi-head), transformer block, RoPE, FlashAttention, MoE
- Training: pretraining, fine-tuning, LoRA / QLoRA, RLHF, DPO, distillation
- Inference: KV cache, speculative decoding, quantization, batching, prefix caching
- Retrieval: embeddings, vector DB, BM25, reranker, RAG, hybrid search
- Agents: tool use, MCP, multi-agent, supervisor pattern, ReAct
- Eval: BLEU, ROUGE, perplexity, LLM-as-judge, MMLU, HELM
- Production: latency, throughput, observability, drift, evaluation harness

### Pass B — Auto-linker (mechanical)

Script `_link_concepts.py` reads the anchor table and processes every section page:

1. For each concept, find the **first** plain-text occurrence in the page that is NOT already inside an `<a>` or `<code>` tag.
2. If the page is **not** the primary definition page, wrap the occurrence in `<a href="<primary>">…</a>`.
3. Skip if the occurrence is in a heading, code block, callout-title, or already linked within the same paragraph.
4. Track a `link_budget` per page (max 3 cross-refs per paragraph, 12 per section) to avoid hyperlink soup.

Heuristics already proven on this codebase:
- Use `re.sub` with a capturing group on word boundaries `\b(synonym)\b`
- Process synonyms longest-first (so "scaled dot-product attention" wins over "attention")
- Defer to existing `<a>` tags via DOM-aware match (BeautifulSoup, not raw regex)

### Pass C — Manual review of three classes

Three places where a human still needs to decide direction:

1. **Prerequisite blocks** at the top of each section. Currently many say "covered in Section X.Y" without a link. Audit + auto-link these via the same anchor table.

2. **What's-Next blocks** at the bottom. Already cleaned up in v6.26 to point to the next reading-order section. Add an extra "see also" line listing 1-2 forward references where the same concept resurfaces.

3. **Callout cross-refs**. Big-picture and library-shortcut callouts often mention concepts WITHOUT linking. Pass C wraps these.

## Prerequisites audit (sub-plan, run before Pass A)

The `<div class="prerequisites">` block at the top of each section already lists the concepts the section assumes. These are the highest-value link targets because:

1. The reader is explicitly told "you should know X" — they will click to verify
2. The link target is by definition already canonical for X
3. The text is short and self-contained

Audit script `_v633_audit_prereqs.py`:

```
For each section page:
  Extract <div class="prerequisites"> text
  For each "Section X.Y" / "Chapter NN" mention:
    - Verify the link exists (or warn if it's plain text)
    - Verify the target page actually covers what the prereq claims
    - If plain text, generate a candidate <a href> from the section number
```

Expected outcome: ~150 prereq mentions across the book; ~40% are plain text and can be auto-linked.

## Deliverables

1. `KDP/validation/concept_anchors.json` — concept→pages table (manual + grep-assisted)
2. `KDP/build/_v634_link_concepts.py` — auto-linker
3. `KDP/build/_v633_audit_prereqs.py` — prerequisites audit + auto-fix
4. `KDP/validation/hyperlinks_added.csv` — log of every link inserted (file, paragraph idx, concept, target) for review
5. `KDP/HYPERLINKS_REPORT.md` — before/after stats: links per chapter, link density, concept coverage

## Risk + safeguards

- **Linkitis**: hyperlink soup is worse than no links. Cap at 3 links per paragraph, 12 per section. Track in budget.
- **Wrong target**: auto-linking can pick the wrong "primary" for ambiguous terms (e.g. "regression" — software regression vs statistical regression). Manual review of the anchor table catches this.
- **Stale links**: every cross-reference should survive section renumbering. Use anchor IDs (`section-4.1.html#self-attention`) not raw URLs where possible.
- **Reversibility**: every modified file is committed in a separate v6.34 commit so rollback is one `git revert`.

## Effort estimate

| Pass | Effort | Output |
|------|--------|--------|
| Build concept anchor table | 4 hrs (mostly grep + judgment) | 80-entry JSON |
| Prereq audit + auto-fix | 2 hrs | ~60 prereq links |
| Auto-link first-mentions | 3 hrs | 800-1500 inline links |
| Manual review + tighten | 4 hrs | reject ~10% of auto-suggestions |
| **Total** | **~13 hrs** | book becomes a navigable graph |

Worth doing in one focused session rather than incrementally.
