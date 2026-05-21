# Wave 9: Authoring 14 Missing Chapters — Plan

**Status**: queued for execution.
**Branch**: `v2.0`.
**Goal**: Fill the 14 chapter-number gaps in the v9 canonical numbering so the final book has 84 contiguous chapters (0–83), plus absorb Math/ML appendices into Part I Ch 0.

The 14 gap positions are reserved by Wave 8:

| Part | Gap chapters | Topic |
|---|---|---|
| 7 (Retrieval & IE) | 34, 35, 36 | NER (promoted from sec 15.5), RAG Fundamentals split, Advanced RAG split, Retrieval Tools |
| 8 (Conv AI) | 40, 41 | Voice & Realtime Multimodal Assistants (merge 24.5 + Ch 38 streaming), Conv AI Tools |
| 9 (Eval) | 46 | LLM-as-Judge & Automated Evaluation (promote sec 44.8) |
| 11 (Ethics) | 56 | Responsible AI Tools |
| 12 (Scale) | 59, 60, 61 | Distributed Training Systems, Edge & On-Device LLMs, Scale Tools |
| 13 (LLMOps) | 63, 64, 65, 66 | AI Gateways & Routing, Workflow Orchestration, Containers/K8s, Reliability/SLOs/Registry, LLMOps Tools |

Plus Math/ML absorption into Part I Ch 0 sec 0.1, 0.2, 0.3.

---

## Rule #1 — Always check for existing content FIRST

**Before authoring any new chapter or section, the first step is to check whether the content already exists somewhere we can re-home.** Writing from scratch is the last resort, not the first.

Four checking layers:

### Check 1 — Preserved content from earlier waves

`.book-update/v9-preserved-content/` holds content extracted during Wave 1:
- `world-models-and-embodied-reasoning-section-41.4.html` — unique World Models content from deleted Ch 41
- `multimodal-reasoning-cross-modal-retrieval-section-41.7.html` — unique Multimodal Reasoning content from deleted Ch 41

These were NOT authored to be lost — they're staged for re-homing.

**Action**: every Wave 9 chapter MUST first scan this folder for relevant material.

### Check 2 — Git history of dropped sections / chapters

Sections and chapters dropped during the restructure may have had unique content:

| Wave | Dropped item | Possible reuse target |
|---|---|---|
| Wave 1 | Sec 8.3 (Reasoning Models & Test-Time Compute) | Already canonical in old Ch 9 — content survives there, just check for stragglers |
| Wave 1 | Sec 73.6, 74.6, 76.6 (industry overview sections) | Likely some unique vendor/case material — scan before declaring "duplicate" |
| Wave 1 | Sec 79.2 (Education/Legal/Creative cross-cut) | Possible unique content split between Education, Legal, Creative chapters |
| Wave 1 | Ch 31 (Multimodal overview) sections 31.1–31.4 | Overview-only, no deep content; safe to drop |
| Wave 1 | Ch 41 (Embodied AI aggregator) sec 41.1, 41.2, 41.3, 41.5, 41.6, 41.8 | Pure duplicates of Ch 36/39/40; safe to drop |
| Wave 1 | Sec 45.6 | Already merged into Ch 44 as sec 44.12 |
| Wave 7 | Apx E, F, G (Projects, Capstone, War Stories) | Pure pedagogy; not for re-homing in main book |

**Action**: for each Wave 9 new chapter, run `git log -p <previous-commit-hash> -- <topic-relevant-paths>` to find any unique citations, examples, code, or diagrams in dropped material.

### Check 3 — Sections that moved but didn't fully unpack

Section-level moves staged for Wave 9 (per v9 plan, deferred from Wave 4):

| Section | From | Target Wave 9 home |
|---|---|---|
| sec 15.5 (Structured Information Extraction & NER, 79 KB monster) | Old Ch 15 (Hybrid ML+LLM) | New Ch 34 (Structured Information Extraction & NER) — promote whole section, split internally into 5 sub-sections |
| sec 44.8 (LLM-as-Judge) | Old Ch 44 (Eval Foundations) | New Ch 46 (LLM-as-Judge & Automated Evaluation) — promote + expand to 5 sections |
| sec 7.6, 7.8 (Distributed Training Systems, Production Training) | Old Ch 7 (Pre-training) | New Ch 59 (Distributed Training Systems) |
| sec 70.5 (Application Architecture & Deployment) | Old Ch 70 (Shipping AI Products) | New Ch 64 (Containers, K8s & Deployment) |
| Old Ch 62 sec 62.3 (AI Gateways) | Part 13 Ch 62 | New Ch 63 (AI Gateways & Model Routing) |
| Old Ch 62 sec 62.4 (Workflow Orchestration) | Part 13 Ch 62 | New Ch 64 (Workflow Orchestration & Durable Execution) |
| Old Ch 62 sec 62.5 (Edge & On-Device LLM Deployment) | Part 13 Ch 62 | New Ch 60 (Edge & On-Device LLMs) |
| Old Ch 62 sec 62.7-62.11 (Docker/K8s) | Part 13 Ch 62 | New Ch 64 (Containers, K8s & Deployment) |
| Old Ch 62 sec 62.1, 62.2, 62.6 (Scaling, LLMOps, Reliability) | Part 13 Ch 62 | New Ch 65 (Reliability, SLOs & Model Registry) |
| Sec 24.5 (Voice Agents) | Part 8 Ch 24 (Conv AI) | New Ch 40 (Voice & Realtime Multimodal Assistants) — merge with Ch 38 streaming |
| Old Ch 38 (Streaming Multimodal, 4 sections) | Part 8 (currently sits there since Wave 4) | New Ch 40 (Voice & Realtime) — merge with sec 24.5 |
| Old Ch 23 (RAG, 9 sections) | Part 7 Ch 32 (currently) | Split into new Ch 32 (RAG Fundamentals: sections 23.1, 23.2, 23.4, 23.5) and new Ch 35 (Advanced RAG: sections 23.3, 23.6-23.9 + knowledge graphs) |

**Action**: for each Wave 9 new chapter that has section-level source content already in the book, the authoring is **promote + organize + cross-reference**, not "write from scratch."

### Check 4 — Images and figures from dropped/moved content

When chapters were deleted (Wave 1, Wave 4, Wave 5), their `images/` folders went with them. Some of those images are still relevant for the re-homed content.

`scripts/v9_wave3_restore_images.py` already restored 77 images from git history during Wave 3 merges. The same pattern applies here:

**Action**: for each new Wave 9 chapter, list `images/` from the source chapter(s) in git history; restore relevant images via `git show <commit>:<image_path> > target_images_dir/<filename>`.

---

## Rule #2 — Authoring quality bar (when new content is needed)

If Checks 1–4 don't yield enough material for a chapter, then new content is authored. The quality bar:

1. **Match the book's existing voice** — see `templates/section.html` for the canonical structure (epigraph, big-picture, H2 sub-sections, callouts, code, figures, bibliography).
2. **5–8 sections per chapter, 5–60 KB body text per section** (the same band the restructure enforces).
3. **Every section has ≥3 bibliography entries** to primary sources.
4. **Every section has at least one callout** (big-picture, key-insight, practical-example, warning, fun-fact, etc.).
5. **Code examples are runnable as written** — no `# ...` placeholders.
6. **Figures use the book's SVG style** (book.css palette: navy/green/purple/amber/red; ≤8 boxes per diagram, ≤3-word labels).

---

## Execution plan (per chapter)

The Wave 9 sequence for each gap chapter:

### Step A — Inventory existing material
1. Search `.book-update/v9-preserved-content/` for relevant content
2. Run `git log --all -- <topic-keyword>` to find dropped sections that may have unique citations or examples
3. Identify sections that already cover this topic (per the v9 plan section-move table)
4. List existing images that should be restored

### Step B — Plan the chapter
Outline 5–7 sections covering the chapter's scope. For each section:
- Source: either "promote from sec X.Y" or "merge sec X.Y + sec Z.W" or "new authoring"
- Estimated size
- Key citations to preserve (from Check 2 + 3)

### Step C — Execute
1. Create the module directory: `part-N-slug/module-NN-chapter-slug/`
2. Move existing sections into it (git mv); rewrite section numbers
3. Restore images from git history
4. Author any genuinely-new sections
5. Author the chapter index.html with section list
6. Update the part's index.html chapter cards
7. Rewrite cross-references that now point at the new chapter

### Step D — Audit gate
1. Run `scripts/html_integrity_audit.py` — must be P0 = P1 = P2 = P3 = 0
2. Run linear nav walk — coverage must be 100%
3. Verify ToC has the new chapter
4. Commit

---

## Parallelization

Wave 9 chapters cluster naturally into 6 batches that can run in parallel:

| Batch | Chapters | Topic affinity | Suggested agent |
|---|---|---|---|
| Batch 1 — Retrieval | Part 7 Ch 34, 35, 36 | NER + RAG fundamentals + Advanced RAG | 1 agent |
| Batch 2 — Conv AI | Part 8 Ch 40, 41 | Voice/Realtime + Conv AI Tools | 1 agent |
| Batch 3 — Eval | Part 9 Ch 46 | LLM-as-Judge | 1 agent |
| Batch 4 — Ethics Tools | Part 11 Ch 56 | Responsible AI tools | 1 agent |
| Batch 5 — Scale | Part 12 Ch 59, 60, 61 | Distributed training, edge, scale tools | 1 agent |
| Batch 6 — LLMOps | Part 13 Ch 63, 64, 65, 66 | Gateways, orchestration, containers, reliability, LLMOps tools | 1 agent |

Plus a separate task:

| Task | What | Agent |
|---|---|---|
| Math/ML absorption | Move Apx A.1–A.6, B.1–B.4 content into Part 1 Ch 0 new sections 0.1 (Math), 0.2 (Probability & Info Theory), 0.3 (Classical ML — absorbs unique B.1-B.3 content). Move Apx B.4 (Eval Metrics) to Part 9 Ch 42 opening section. Rewrite the 22 inbound refs to Apx B.4 to point at new home. | 1 agent |

Plus appendix cleanup:

| Task | What | Agent |
|---|---|---|
| Appendix renumber | After Math/ML absorption, drop Apx A and B. Rename C (Course Syllabi) → A, D (Reading Pathways) → B. Rewrite all inbound refs. | Sequential after Math/ML task |

**Total**: 6 chapter-authoring agents + 1 math/ML agent in parallel; appendix renumber follows. Wall-clock estimate: ~3 hours parallel + 1 hour for the appendix-renumber sequential step.

---

## Success criteria

After Wave 9 completes:

```
Chapters:     84 (was 70 + 14 newly authored/promoted)
Sections:     ~420 (estimated; varies based on authoring decisions)
Appendices:   2 (Course Syllabi, Reading Pathways)
Audit:        P0 = P1 = P2 = P3 = 0
Linear nav:   100% coverage end-to-end
ToC:          16 parts, 84 chapters, 2 appendices, all references resolve
```

Then the content quality pass (`docs/content-quality-pass-plan.md`) runs against the final book.

---

## Anti-patterns to avoid

1. **Authoring from scratch when content already exists.** Always Check 1–4 first.
2. **Dropping a citation or callout because the prose summary moved.** Citations are independent value; preserve every unique one.
3. **Writing for the sake of filling the gap.** A 4-section chapter with deep content beats a 7-section chapter with padding. If after Check 1–4 there's only material for 4 sections, the chapter is 4 sections.
4. **Forgetting to restore images.** Wave 3's image-restoration pattern works; reuse it.
5. **Audit-skipping commits.** Every Wave 9 commit ends with the audit gate.

---

## Trigger conditions

This plan runs **after**:
- Wave 8 cascade renumber complete ✓
- Wave 10 ToC + manifest refresh complete ✓

Currently both prerequisites are met. Wave 9 can execute as soon as scheduled.
