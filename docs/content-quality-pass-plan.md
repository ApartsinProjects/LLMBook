# Deep Content Quality Pass — Plan

**Status**: queued for after structural waves 5/6/8/9/10 complete.
**Branch**: `v2.0` (will be merged to `main` after content pass).
**Scope**: ~84 chapters, ~375 sections in the v9 final structure.
**Goal**: Every section is focused, non-redundant, and either deep-enough or appropriately concise. Cross-references replace duplication; visual aids appear only where they clarify.

---

## 1. What this pass does

For each section in the book, ask four questions:

| # | Question | Action if "no" |
|---|---|---|
| Q1 | Does the section's prose stay on the topic its title and chapter promise? | Flag for content trim or re-home |
| Q2 | Is anything in this section better covered in another section? | **Consolidate first, then cross-reference. Never silently drop unique information** — see §2a below. |
| Q3 | Would this section be more valuable with deeper technical content (architecture details, algorithms, code, concept derivations)? | Author additions where warranted |
| Q4 | Would a diagram, table, or illustration genuinely make a hard idea easier? | Author the visual; skip if cosmetic |

The rule for Q3 and Q4: **additions only if they increase the section's value**. No filler, no decorative figures, no code dumps for show.

---

## 2a. Q2 consolidation rule — no information loss

When Layer A flags two (or more) sections as covering the same topic, the rule is **consolidate, don't delete**. The process:

1. **List unique claims, examples, and citations from each source.** For each section in the cluster, extract:
   - Distinct technical claims or definitions (does this section say something the others don't?)
   - Distinct worked examples, code snippets, or numerical results
   - Distinct citations (papers, blog posts, library docs)
   - Distinct figures, diagrams, or tables
   - Distinct caveats or "watch out for X" callouts

2. **Designate the canonical home** per the rule in §4 (most authoritative, most depth, earliest in book on ties).

3. **Merge unique material into the canonical home.** Each unique item from a non-canonical source must end up in:
   - The canonical section's body (preferred), OR
   - A new H3 subsection inside the canonical, OR
   - A footnote / callout if it's a side observation

4. **Only after merge complete: replace non-canonical occurrences with cross-references** that point at the canonical section.

5. **Never silently drop a unique citation or callout** — even if the prose summary is redundant, the citation may have been the reader's only path to the original source.

6. **Audit trail.** Each consolidation produces a one-line record in `docs/content-pass/consolidation-log.md`:
   ```
   <date>  consolidated [topic]
     canonical home: <path>
     absorbed from:  <path1>, <path2>, ...
     unique items moved: <n citations>, <n callouts>, <n examples>
   ```

This applies symmetrically: if a section is being **deleted** entirely (e.g., aggregator chapter), every unique piece of its content must be re-homed first. The audit trail is the proof.

---

## 2. Three-layer pipeline

The content pass runs in three layers, each parallelizable across parts:

### Layer A — Audit (read-only, parallelizable)
For each section:
1. Extract section title, H2 outline, body summary, current word count, current figure/table count
2. Compare against the chapter's stated scope (chapter index meta description)
3. Identify obvious topic-drift (paragraphs that wander into another chapter's territory)
4. Compute a *similarity signal* against all other sections (Jaccard over keyword sets) to surface potential redundancies
5. Emit a per-section report with flagged items

**Parallelism**: 1 agent per part (16 parts in v9) → 16 audits in parallel. Each agent has the part's chapter list + the cross-part Tools-of-the-Trade content for context. Reports under `docs/content-pass/audit-part-XX.md`.

### Layer B — Cross-reference proposals (depends on Layer A)
For each topic identified in Layer A as covered in multiple places, decide the canonical home (the section with most authoritative depth) and propose cross-references for the others to inline-link to it.

**Output**: `docs/content-pass/cross-ref-proposals.md` with a table of:
- Topic
- Canonical home
- Sections that should reference it instead of repeating

**Parallelism**: 1 agent owns the cross-cluster (e.g., all retrieval-related sections regardless of part), produces proposals.

### Layer C — Enhancements (parallelizable per chapter)
Author the actual improvements based on Layer A + B outputs:
- Trim or move drifting content
- Insert cross-references with `<a class="cross-ref">` markup
- Author deep-dive H3 subsections where warranted (algorithms, code blocks, conceptual derivations)
- Author SVG diagrams and tables where Q4 said yes

**Parallelism**: 1 agent per chapter — that's ~84 agents at full scale. To keep tractable, batch 4–5 chapters per agent (16–20 agents total). Each agent commits its chapter's improvements as one commit.

---

## 3. Content alignment audit (Layer A details)

### A.1 Topic-drift detection
For each section, run:
```
keywords(section) ∩ keywords(chapter description)
```
If overlap is below threshold (Jaccard < 0.15), section is flagged as drifted.

### A.2 Redundancy detection
Build a TF-IDF vector per section, compute cosine similarity across all section pairs. Pairs above 0.5 similarity get flagged. Manual review decides whether to:
- Merge (combine into one)
- Differentiate (rewrite to highlight contrast)
- Cross-ref (canonical home + pointers)

### A.3 Section size profile
For each section, compute body text size and number of:
- Code blocks
- Figures
- Tables
- H2 / H3 subsections
- Cross-references already present

Outlier sizes (<5 KB or >60 KB body) flagged for trim or split.

### A.4 Bibliography coverage
Each section should cite primary sources for its claims. Sections with <3 bibliography entries flagged for citation enrichment.

---

## 4. Cross-reference opportunities (Layer B details)

### Canonical home decision rule
For a topic appearing in N sections, the canonical home is the section that:
1. Has the topic in its title or H1
2. If tied, the one with the most body text on the topic
3. If tied, the section earlier in the book (so forward-references go to context already established)

### Cross-ref markup
The book uses:
```html
<a class="cross-ref" href="../../part-X/module-Y/section-N.M.html">visible text</a>
```

Cross-refs appear inline in prose, not at end of sections (preserves reading flow).

### Known cross-cluster topics (preliminary list from v5/v9 analysis)
Each of these clusters needs canonical home + cross-refs:

| Cluster | Likely canonical home | Mentioned in |
|---|---|---|
| Reasoning models | Part II Ch (Reasoning) | Part III prompt eng, Part VI agents, Part IX eval |
| RAG | Part VII Ch (RAG Fundamentals) | Part VI agents (agentic RAG), Part VIII (memory), Part XIII industries |
| Tool use | Part VI Ch (Tool Use Protocols) | Part III APIs, Part VIII voice agents |
| Long context | Part II Ch (Pre-training/Scaling) | Part IV fine-tuning, Part IX eval |
| Quantization | Part II Ch (Inference Opt) | Part IV PEFT, Part XII Scale |
| KV cache | Part II Ch (Inference Opt) | Part XII Scale, Part XIII LLMOps |
| Multi-agent topologies | Part VI Ch (Multi-Agent) | Part XV industry chapters |
| Eval metrics (perplexity, F1, BLEU) | Part IX Ch (Eval Foundations) | Part I Ch 0 (ML basics), Part IV (training) |
| LangChain | Part VI Ch (Agent Tools) | Part VII (RAG), Part VIII (dialogue) |
| HuggingFace | Part II Ch (Interpretability+Tools merged) | Part IV (training), Part V (multimodal) |
| Compute planning | Part XII Ch (Compute Planning) | Part II (pretraining), Part XIII LLMOps |
| Vision-language models | Part V Ch (VLM/Omni) | Part XV multimodal applications |
| Voice / TTS | Part VIII Ch (Voice & Realtime) | Part V (audio gen), Part XV industries |
| Safety / guardrails | Part X Ch (Guardrails) | Part VI agent safety, Part XV industries |
| Bias / fairness | Part XI Ch (Bias/Hallucination) | Part XV industries (every domain has bias concerns) |
| Differential privacy | Part X Ch (Privacy) | Part IV training (private SGD), Part XV finance/healthcare |

---

## 5. Content enhancement opportunities (Layer C details)

### When to ADD content (Q3 = yes)

Add a deep-dive H3 subsection if **all three** apply:
1. The section's existing treatment is shallow (no algorithm, no concrete example, just exposition)
2. The topic is technically rich enough to warrant 200+ words of substance
3. The reader would otherwise need to leave the book to find this

Examples of likely additions:
- **Pre-training Ch 7**: deeper treatment of scaling-law fitting math + worked example
- **Inference Optimization Ch 10**: explicit algorithm for KV cache eviction policies
- **Reasoning Ch 9**: code example of self-consistency sampling
- **PEFT Ch 18**: LoRA rank choice heuristic with empirical numbers
- **Alignment Ch 19**: DPO loss derivation with one screen of math
- **RAG Fundamentals (new VII Ch 3)**: walk-through of a Ragas eval run
- **Agent Foundations (new VI Ch 28)**: ReAct loop pseudocode + termination heuristics
- **LLMOps Ch 64 Containers**: minimal but production-ready Dockerfile for vLLM
- **Eval Foundations (new IX Ch 43)**: bootstrap CI calculation for accuracy
- **LLM-as-Judge (new IX Ch 44)**: judge debiasing — position bias and length bias
- **Industry Healthcare Ch 76**: HIPAA-aligned deployment checklist
- **Frontier Architectures (new XVI Ch 81)**: Mamba state-space recurrence equations

### When NOT to add (Q3 = no)

- Section already has 30+ KB of well-structured content (adding makes it bloated)
- The topic has its own dedicated chapter (add cross-ref instead)
- The "deep dive" would duplicate Tools-of-the-Trade canonical content

### Code example rules
- Maximum 60 lines per block (longer goes in a linked notebook reference)
- Always runnable as written (no `# ...` placeholders)
- Always Python unless the topic mandates another language
- Use the syntax-highlighting pattern already in the book

---

## 6. Visual aids (Layer C, Q4)

### Diagram rules
- SVG only (no PNG decorative figures)
- Match book palette (navy/green/purple/amber/red — defined in book.css)
- ≤ 8 boxes per diagram
- ≤ 3 words per box label

### Tables rules
- Markdown source, rendered to HTML via the book's table CSS
- ≤ 6 columns
- Use `<div class="comparison-table">` wrapper for side-by-side comparisons

### When to ADD a visual (Q4 = yes)
- Pipeline diagrams: input → step1 → step2 → output (improves comprehension)
- Comparison tables: when 3+ options have 3+ dimensions of comparison
- Conceptual diagrams: forces feedback loops, state machines, attention patterns

### When NOT to add a visual (Q4 = no)
- One-step process (text is faster to read)
- Decorative "concept art" (no information density)
- Tables with <3 entries or <3 columns (use a list)

---

## 7. Parallelization plan

### Layer A audit (16 agents, ~2 hours real wall-clock)
Spawn 16 agents in parallel via the Agent tool, one per part. Each agent:
1. Reads chapter index pages for its part
2. Reads each section file in its part
3. Computes the audit metrics (size, H2 count, keyword overlap, citation count)
4. Writes `docs/content-pass/audit-part-XX.md`

Each report has section-level rows with: word count, H2 count, code blocks, figures, citation count, topic-drift flag, redundancy candidates.

### Layer B cross-ref proposals (4 agents, parallel)
Four agents, one per cross-cluster theme:
- Agent 1: model-cluster topics (reasoning, training, PEFT, inference opt)
- Agent 2: pattern-cluster topics (RAG, tool use, agents, conversation)
- Agent 3: quality-cluster topics (eval, safety, ethics)
- Agent 4: runtime+applied topics (scale, ops, products, industries)

Each consumes Layer A reports for its theme and produces a cross-ref proposal table.

### Layer C enhancements (16-20 agents, parallel)
Group chapters by topic-affinity (so agents have coherent context):
- Agent 1: Part I Ch 0–2 (foundations)
- Agent 2: Part I Ch 3–5 (transformer + decoding)
- Agent 3: Part II all (Understanding LLMs)
- Agent 4: Part III all (Working with LLMs)
- ...
- Agent 16: Part XV–XVI

Each agent:
1. Reads its assigned chapters
2. Reads Layer A + B output for those chapters
3. Authors enhancements (trim, cross-ref, deep dive, visual aid)
4. Commits as one commit per chapter

### Coordination
- All agents run on a fresh checkout of `v2.0` (post-Wave-10 state)
- Each agent commits to a feature branch named `content-pass-part-N` or `content-pass-ch-N-M`
- After all agents finish: PR merge all branches into `v2.0`
- Final audit + integrity check
- Merge `v2.0` into `main`, tag `production-v2.0`

---

## 8. Success criteria

After the content pass, the book passes these gates:

| Gate | Target |
|---|---|
| Topic-drift count (Jaccard < 0.15 sections) | 0 |
| Redundancy pairs (cosine > 0.5) | 0 |
| Sections without ≥3 bibliography entries | <5% of total |
| Sections < 5 KB body text | <2% of total (template sections like X.3/X.4/X.5 in some Tools chapters allowed) |
| Sections > 60 KB body text | <5% of total |
| Cross-refs per section (avg) | ≥3 |
| Sections lacking big-picture callout | 0 |
| HTML integrity audit | P0 = P1 = P2 = P3 = 0 |
| Linear nav coverage | 100% |
| ToC matches disk | yes |

---

## 9. Estimated effort

| Layer | Agents | Effort per agent | Total wall-clock |
|---|---|---|---|
| Layer A audit | 16 | 30 min | ~30 min (parallel) |
| Layer B cross-refs | 4 | 1 hour | ~1 hour (parallel) |
| Layer C enhancements | 16-20 | 2-3 hours | ~3 hours (parallel) |
| Coordination/merge | — | — | 1 hour |
| Final audit + polish | — | — | 1 hour |
| **TOTAL** | | | **~6 hours of parallel work** |

Compare to sequential execution: ~80-100 hours. The parallelism is the entire reason this is feasible.

---

## 10. Open questions

1. **Word-count targets per section**: should we set explicit minimums/maximums, or trust the agents to judge? Current default: 5–60 KB body text band.
2. **Citation density**: are 3 bibliography entries per section the right floor? Some short reference sections (X.5 External Reading in Tools chapters) genuinely don't need their own citations.
3. **Visual aid licensing**: SVG diagrams authored by agents — are they considered original work, or do they need attribution? Assumption: original.
4. **Multi-version reconciliation**: if a topic moved during Waves 1-9, body refs may point at the old location. Layer A audit should explicitly check for this.

---

## 11. Trigger

This plan is staged for execution **after**:
1. Wave 5 (part splits) complete
2. Wave 6 (reordering) complete
3. Wave 8 (cascade renumber) complete
4. Wave 9 (author missing content for new chapters) complete
5. Wave 10 (final audit) complete

At that point, the book has its final v9 structure (16 parts, ~84 chapters), and the content pass can proceed against stable section numbering.
