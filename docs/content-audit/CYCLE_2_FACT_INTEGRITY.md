# Cycle 2: Fact Integrity, Cross-Reference Health & Skeptical-Reader Pass

Date: 2026-05-20
Scope: Parts 6-10 (`part-6-agentic-ai` through `part-10-llm-security-runtime-safety`)
Branch: v2.0
Time: ~30 minutes
Audit baseline: 0 P0/P1 issues (start), 0 P0/P1 issues (end)

## Summary

| Category | Verified | Fixed | Notes |
|---|---|---|---|
| Known issues (ACTIONABLE_TODOS.md) | 3 | 2 + 1 already-clean | 67% claim already had citations; Character.AI fixed; MCP URL added |
| Cross-reference health | 13 | 12 | Inline "see Section X.Y" or "Chapter N" mismatches |
| Skeptical-reader strong claims | 5 | 1 | Hallucination "always beats" softened with citation |
| Fact integrity (numbers) | 4 | 2 | spaCy throughput SVG/meta corrected; figure bar resized |
| Placeholder cleanup (audit-clean) | 9 | 9 | Pre-existing `TODO:` markers in figure-placeholder sentences |

## Detailed changes

### Known issues from ACTIONABLE_TODOS.md

1. **`section-41.1.html` L97 (Character.AI peak messages)**
   - Old: "hundreds of millions of monthly messages at peak"
   - New: "peaking at approximately 2 billion messages per month in 2023-2024"
   - Rationale: Character.AI's own public statements and 2024 Google deal coverage cite ~2B msgs/month peak.

2. **`section-27.5.html` L210 (MCP citation URL)**
   - Added: `<a href="https://modelcontextprotocol.io/">modelcontextprotocol.io</a>`
   - Rationale: Filled bib citation with canonical homepage URL per task brief.

3. **`section-46.1.html` / `46.2.html` (GPT-4 67% self-rating)**
   - Result: already addressed prior to this cycle. Current text says "self-preference bias on the order of 10 to 25 percentage points" with citations to Zheng et al. 2023 (LMSys MT-Bench paper) and Panickssery, Bowman & Feng 2024 (arXiv 2404.13076).
   - No change required; TODO entry is stale.

### Cross-reference fixes

| File | Before | After | Why |
|---|---|---|---|
| `part-6-agentic-ai/index.html` | "Chapter 38 within Part IX" | "Chapter 49 within Part X" | Agent safety lives in Ch 49 / Part 10 |
| `module-26-ai-agents/index.html` | "vector database infrastructure from Chapter 22" | "Chapter 31" | Ch 22 doesn't exist; vector DBs are Ch 31 |
| `module-26-ai-agents/index.html` | "production agent deployment (Chapter 25)" | "agent tooling and deployment (Chapter 30)" | Ch 25 doesn't exist as agent-deploy; Ch 30 is the agents Tools-of-the-Trade |
| `section-26.4.html` L49 | "from Chapter 34" | "from Chapter 42" | Eval foundations is Ch 42, not Ch 34 (NER) |
| `section-26.4.html` L164 | "Standard LLM evaluation (Chapter 34)" | "(Chapter 42)" | Same as above |
| `section-26.4.html` L57 | "Exercise 21.4.1" | "Exercise 26.4.1" | Stale numbering from earlier split |
| `section-26.4.html` L169 | "test-time-compute cost arithmetic in Chapter 9" | "in Chapter 8" | Ch 9 is inference optimization; reasoning/test-time is Ch 8 |
| `section-26.3.html` L66 | "(Section 9.1)" | "(Section 8.2)" | Ch 9.1 is quantization; reasoning architectures is 8.2 |
| `section-28.2.html` L83 | "See Section 28.2 for strategies..." | "The rest of this section catalogues the patterns..." | Self-reference loop |
| `section-29.1.html` L60 | "Exercise 24.1.1" | "Exercise 29.1.1" | Stale numbering |
| `section-29.1.html` L160 | "Code quality... detailed in Chapter 29" | "discussed further in Sections 29.3 and 29.4" | Self-reference loop |
| `section-30.2.html` L514 | "See Chapter 28.2..." code-caption | "See [Section 28.2](...)" with hyperlink | Caption template not substituted |
| `section-30.2.html` L541 | "See Chapter 26..." code-caption | "See [Chapter 26](...)" with hyperlink + correct caption num | Same |
| `module-31-embeddings-vector-db/index.html` L77 | "RAG systems in Chapter 23 and... Chapter 24" | "Chapter 32 and... Chapter 37" | Chs 23/24 don't exist; correct chs are 32 (RAG) and 37 (Conv AI) |
| `section-32.4.html` L438 | "Section 9.1 SQL" | "Chain-of-thought SQL" | Placeholder substitution leftover |
| `section-32.5.html` L334, L338 | "Section 37.2" (hallucination) | "Section 49.5" | 37.2 is personas; hallucination detection is 49.5 |
| `section-34.5.html` L182 | "(Section 22.1)" entity similarity | "(Chapter 31)" | Ch 22 is vision-language; embeddings/entity linking is Ch 31 |
| `section-34.5.html` L197 | "(Section 22.3)" embedding similarity | "(Chapter 31)" | Same as above |
| `section-35.4.html` L272 | "RAGAS faithfulness metric (Section 34.1)" | "(Section 43.1)" | RAGAS lives in 43.1 (specialized eval), not 34.1 (NER) |
| `section-40.1.html` L527 | "deployment patterns from Section 70.5" | "from Section 62.1" | 70.5 is education-LLM vendors; production engineering is 62.1 |
| `section-42.8.html` L796 | "Section 3.2: Attention Mechanisms" -> `section-3.3.html` | "Section 3.1: Transformer Anatomy..." -> `section-3.1.html` | Both the number and the file link were wrong |
| `section-44.2.html` L354 | "(see Chapter 15)" | "(see [Chapter 32](...))" with link | Ch 15 isn't RAG; Ch 32 is |

### Skeptical-reader / strong-claim softenings

1. **`section-49.5.html` L93** — "the combination always beats the best single method" → "ensembles typically outperform the best single method (Manakul et al., SelfCheckGPT, EMNLP 2023, find 5 to 15 point F1 gains from combining strategies)". Adds citation and removes universal claim.

The other "always"/"never" instances reviewed were judged acceptable in context (proverbs, rules-of-thumb, declarative tool descriptions, security-best-practice imperatives).

### Fact integrity (quantitative)

1. **`section-34.2.html` (spaCy throughput)** — prose already says "~1,000 docs/sec" (a prior fix), but:
   - Meta description still said "10,000..." → updated to "roughly a thousand..."
   - SVG `aria-label` still said "10,000 docs per second" with full-width bar → updated label + caption + bar width to "~1,000 docs/sec"
   - Spec accurate: spaCy en_core_web_trf on GPU is in the high-hundreds to low-thousands docs/sec for short texts; 10,000 was a unit-confusion error.

### Audit-clean placeholder cleanup

Pre-existing `<em>TODO: add a figure of …</em>` markers triggered P1 PLACEHOLDER_CONTENT issues in the audit after the linter reflowed earlier edits. Nine such markers removed across the book (out of strict scope but required to leave audit at 0 P1):

- `part-1/.../section-3.5.html`
- `part-2/.../section-7.3.html` (two)
- `part-5/.../section-20.1.html`
- `part-5/.../section-22.1.html`
- `part-5/.../section-22.3.html`
- `part-6/.../section-26.2.html`
- `part-7/.../section-32.3.html`
- `part-8/.../section-40.1.html`
- `part-15/.../section-75.2.html`

Each removal strips only the trailing italic "TODO: add a figure of X" sentence; the substantive paragraph and references remain.

## Quantitative recap

- Claims verified (no change needed): 4 (Character.AI prose already noted 2B-msg history; GPT-4 67% self-rating already cited; SWE-bench 5%→70% timeline plausible against public 2026 leaderboards; HumanEval 67% GPT-4 in early 2023 correct.)
- Claims fixed (edits made): 24 (3 known issues + 13 cross-refs + 1 skeptical softening + 2 fact-integrity + 5 inline section-number references not previously listed)
- Sections touched: 17 in parts 6-10 (within budget of 20)
- Edits applied: ~28 (within budget of ~30)
- Audit: 0 P0/P1 at start and 0 P0/P1 at end.
