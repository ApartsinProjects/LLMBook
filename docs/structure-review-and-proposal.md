# Book Structure: Analysis and Proposed Restructure (v3)

**Status**: proposal, awaiting review.
**Generated**: 2026-05-17, post-appendix-renumbering.
**Revision history**:
  - v1 — initial: 13 parts → 13 parts, 87 → 78 chapters; mostly merge/dedupe.
  - v2 — split Part V into Retrieval+IE and Dialogue+Assistants (13 → 14 parts).
  - **v3 (this version)** — split Part X (Operations) into LLM @ Scale and LLMOps; move Multimodal to V (model-cluster); better part names. **15 parts.**
**Current state on disk**: 13 parts, 87 chapters, 413 sections, 7 appendices, audit clean.

---

## 1. Editorial criteria

| Criterion | Target |
|---|---|
| **A. Separation of concerns** | One cohesive theme per part, one topic per chapter |
| **B. No duplication** | Each subject appears once in the ToC; cross-refs handle repetition |
| **C. Reasonable counts** | 5–7 chapters per part, 3–8 sections per chapter |
| **D. Consistent abstraction** | Sibling chapters cover comparable scope |
| **E. Reading order** | The narrative flows from model → patterns → quality → runtime → applied → frontier |

---

## 2. Conceptual grouping of parts

The 15 parts cluster into 6 thematic blocks:

| Block | Parts | What it covers |
|---|---|---|
| **A. Models** | I–V | What an LLM is, how it works, how to train and adapt it, what modalities it covers |
| **B. Patterns on top of models** | VI–VIII | Retrieval, dialogue, agents — the application-level patterns that any LLM supports |
| **C. Quality** | IX–X | Evaluation, observability, safety, security, ethics — non-functional concerns |
| **D. Runtime** | XI–XII | Scale (compute / performance) and ops (workflow / lifecycle) |
| **E. Applied** | XIII–XIV | Designing products and shipping into specific industries |
| **F. Future** | XV | Frontier research, theory, hardware, AGI trajectories |

This grouping is the *why* behind the order. The block boundaries are also natural pause points for a course track.

---

## 3. Proposed structure (final)

| # | Part | Ch | What it contains |
|---|---|---:|---|
| **I** | **Foundations** | 7 | Math / ML / PyTorch prerequisites, NLP basics, tokenization, attention, transformer architecture, decoding strategies, Foundations Tools |
| **II** | **Understanding LLMs** | 5 | Pre-training & scaling laws, modern LLM landscape, reasoning models & test-time compute, inference optimization & efficient serving, interpretability + Understanding Tools |
| **III** | **Working with LLMs** | 4 | LLM APIs, prompt engineering & advanced techniques, hybrid ML+LLM architectures, Working-with-LLMs Tools |
| **IV** | **LLM Training & Adaptation** | 5 | Synthetic data generation, fine-tuning fundamentals, PEFT (LoRA / QLoRA / soft prompts), alignment (RLHF / DPO / preference tuning), Training Tools |
| **V** | **Multimodal LLMs** | 7 | Vision-language & Omni models, image/video generation, audio & music generation, document understanding & OCR, 3D generation & neural scenes, embodied AI / VLA / robotics, Multimodal Tools |
| **VI** | **Retrieval & Information Extraction** | 6 | Embeddings & vector databases, structured information extraction & NER, RAG fundamentals, advanced RAG / knowledge graphs, cross-modal RAG, Retrieval Tools |
| **VII** | **Dialogue & Conversational AI** | 5 | Dialogue architecture & personas, memory & context management, multi-turn conversation flows, voice & realtime multimodal assistants, Conversational AI Tools |
| **VIII** | **Agentic AI** | 5 | Agent foundations, tool use / MCP / A2A protocols, multi-agent systems, specialized agents (code, browser, research), Agent Tools |
| **IX** | **Evaluation & Observability** | 4 | Evaluation fundamentals & quality metrics, specialized evaluation (RAG / agents / multimodal), online evaluation & production monitoring, Eval Tools |
| **X** | **Safety, Security & Ethics** | 9 | Adversarial security & red teaming, guardrails & runtime safety, agent safety & sandboxing, privacy & data protection, bias / fairness / hallucination, regulation & compliance, watermarking / provenance / transparency, frontier safety & sustainability, Safety Tools |
| **XI** | **LLM Systems at Scale** | 5 | Compute planning & GPU procurement, distributed training systems, hardware & chip diversity, edge & on-device LLMs, Scale Tools |
| **XII** | **LLMOps & Production Engineering** | 5 | AI gateways & model routing, workflow orchestration & durable execution, containers / Kubernetes / deployment, reliability engineering / SLOs / model registry, LLMOps Tools |
| **XIII** | **Designing LLM Products** | 7 | Ideation / strategy / product hypothesis, LLM product management, prototyping via vibe-coding, building the MVP, scaling economics & ROI, shipping & scaling AI products, Product Tools |
| **XIV** | **Industry Applications** | 8 | Legal, finance, healthcare, education, cybersecurity, government, manufacturing + creative + recommendation (merged), Industry Tools |
| **XV** | **Frontiers** | 4 | Frontier architectures & scaling, frontier theory & cognition, AGI trajectories & open questions, Frontier Tools |

**Totals**: 15 parts, **86 chapters**, ~370 sections (target). Every part lands in the 4–9 chapter band.

---

## 4. Why the order changes

### Multimodal moved from VIII → V (model-cluster)

**Argument**: A multimodal LLM is an extension of the LLM itself — a different *kind* of model, not a different *use* of one. The model cluster (Foundations → Understanding → Working → Training → Multimodal) covers the spectrum of "what LLMs are." The pattern cluster (Retrieval → Dialogue → Agents) covers "what you build with them."

**Side benefits**:
- Cross-Modal RAG (currently Part VII Ch 42) moves naturally into Retrieval (VI Ch 5), which makes the retrieval-as-pattern story contiguous.
- The voice/streaming-realtime content (currently Part VII Ch 38) moves into Dialogue (VII Ch 4) as the realtime-API basis for voice assistants.
- Embodied AI / VLA (current Ch 39, 40, 41) consolidates into one Multimodal chapter; the agent-overlap (VLA is an agentic pattern) becomes a cross-reference from Part VIII.

### Operations split into XI (Scale) + XII (LLMOps)

**Argument**: Old Part X mixed two different disciplines into one bag.

- **Scale** = computational concerns at the inference/training/hardware layer (vLLM, distributed training systems, GPU procurement, edge silicon, chip diversity).
- **Ops** = workflow / lifecycle / process discipline (gateways, orchestration, containers, reliability engineering, model registry).

They share vocabulary (both touch Kubernetes, both touch monitoring) but the *concerns* are different — one is "make it fast on the GPU," the other is "make it reliable in production."

**Side benefits**:
- Hardware content currently in Part XIII Frontiers (Ch 84 "Frontier Systems & Hardware") finds a stable home in Part XI ("Hardware & chip diversity" chapter) — hardware isn't really frontier-only, it's a scaling concern.
- Distributed training systems currently buried as Part II sections 7.6, 7.8 get a chapter in Part XI.
- The 11-section monster Ch 62 (currently in Part X) cleanly splits across the two new parts.

### Why XI (Scale) before XII (LLMOps)

You provision compute and serving infrastructure (Scale) before you wire up the operational disciplines that run on top (Ops). Same direction as the bottom-up reading order in the rest of the book.

---

## 5. Where NER / structured extraction lives

In the new Part VI Ch 2: **Structured Information Extraction & NER** *(was buried as section 15.5 inside a hybrid-architecture chapter)*. Pairs naturally with the surrounding chapters:

- VI.1 Embeddings & Vector DBs (unstructured → similarity)
- **VI.2 Structured IE & NER (unstructured → structured)**
- VI.3 RAG Fundamentals (retrieval-as-context)
- VI.4 Advanced RAG / Knowledge Graphs (entity → graph → graph-augmented retrieval)
- VI.5 Cross-Modal RAG (extending retrieval to images / video / audio)
- VI.6 Retrieval Tools

Knowledge-graph construction (currently scattered across 15.5, 23.3, 23.7) becomes a contiguous arc: NER (VI.2) → graph construction (VI.4) → graph-augmented retrieval (VI.4).

---

## 6. Summary of structural changes

The table below maps every change from current disk state (13 parts, 87 chapters) to the proposed structure (15 parts, 86 chapters).

| New # | Part | Old # / source | Ch (before → after) | Notes |
|---:|---|---|---:|---|
| I    | Foundations | I | 7 → 7 | unchanged |
| II   | Understanding LLMs | II | 6 → 5 | merge old Ch 11 + Ch 12 |
| III  | Working with LLMs | III | 4 → 4 | sec 15.5, 15.6 move to new VI |
| IV   | LLM Training & Adaptation | IV | 5 → 5 | unchanged |
| **V** | **Multimodal LLMs** | **VII** | **13 → 7** | drop Ch 31 (overview duplicate) and Ch 41 (aggregator); merge Ch 35+37 (VLM+Omni), Ch 39+40 (VLA+Robotics); move Ch 38 (streaming) to new VII; move Ch 42 (cross-modal RAG) to new VI |
| **VI** | **Retrieval & Information Extraction** | **V (partial) + III sec 15.5** | new | 6-chapter split from old V; NER promoted from sec 15.5 to chapter |
| **VII** | **Dialogue & Conversational AI** | **V (partial) + old VII Ch 38** | new | 5-chapter split from old V; absorbs streaming-realtime chapter from Multimodal |
| VIII | Agentic AI | VI | 5 → 5 | unchanged |
| IX   | Evaluation & Observability | VIII | 5 → 4 | merge Ch 45 (1-section orphan) into Ch 44; rename Ch 47 sections to start at .1 |
| X    | Safety, Security & Ethics | IX | 12 → 9 | merge Ch 53+54, Ch 56+57, Ch 58+59 |
| **XI** | **LLM Systems at Scale** | **X (partial) + II 7.6/7.8 + XIII Ch 84** | new | Compute, distributed training, hardware, edge |
| **XII** | **LLMOps & Production Engineering** | **X (partial)** | new | Gateways, orchestration, K8s, reliability, registry |
| XIII | Designing LLM Products | XI | 9 → 7 | merge Ch 63+65+68 (three near-duplicate ideation chapters) |
| XIV  | Industry Applications | XII | 10 → 8 | merge Ch 78+79+80 |
| XV   | Frontiers | XIII | 5 → 4 | move hardware chapter (Ch 84) into new XI |
| **TOTAL** | | | **87 → 86** | |

---

## 7. Execution plan

Each phase is independently reversible and ends in an integrity-clean state (P0=P1=P2=P3=0, linear nav 100%, ToC matches disk).

### Phase 0 — Templatization & manifest setup *(prep work, makes every future restructure easier)*

The book already has templating infrastructure that has fallen behind disk reality during recent restructures. Phase 0 brings it back in sync and turns it into the single source of truth.

**Artifacts:**

| File | Purpose |
|---|---|
| `book_structure.yaml` | **Manifest of current state** — every part / chapter / section. Refresh from disk in Phase 0; thereafter it's the source of truth. |
| `book_structure.target.yaml` | **Declarative target state** — same shape, plus `_action` and `_source(s)` per chapter so the migration is described, not coded. |
| `templates/section.html`, `chapter-index.html`, `part-index.html` | Skeleton HTML with `{{PLACEHOLDER}}` tokens for new content. |
| `templates/README.md` | The conventions doc — callouts, exercise badges, cross-ref classes, mandatory elements. |
| `agents/book-skills/templates/*` | Mirror set used by the authoring agents. |

**Scripts that turn the manifest into reality:**

| Script | Role |
|---|---|
| `scripts/structure_diff.py` | Show the migration plan: parts/chapters that are unchanged / rename / merge / split / move / new. Always the first command run. |
| `scripts/_scaffold_new_chapters.py` | Create new chapter dirs/files for entries with `_action: new_part` or `new`. |
| `scripts/_resolve_template_placeholders.py` | Fill `{{PLACEHOLDER}}` tokens with concrete values. |
| `scripts/rebuild_curated_toc.py` | Regenerate `toc.html` from disk. |
| `scripts/rebuild_linear_nav.py` | Recompute prev / up / next anchors for every section. |
| `scripts/_rebuild_part_indexes.py`, `_rebuild_chapter_indexes.py` | Regenerate the index pages from current state. |
| `scripts/html_integrity_audit.py` | The gate that runs after every phase. |

**Phase 0 acceptance tests:**

1. `python scripts/structure_diff.py` runs and shows the v3 migration plan with no errors.
2. `book_structure.yaml` exactly matches disk: 13 parts, 87 chapters, 413 sections, 7 appendices.
3. `book_structure.target.yaml` is loadable and exactly matches the v3 proposal: 15 parts, 86 chapters, 7 appendices.
4. All scripts in the table above are present and executable.

**Why this matters for the future:** after Phase 0, any new restructure is a four-step operation: (1) edit `book_structure.target.yaml`, (2) run `structure_diff.py` to see the plan, (3) run the migration scripts, (4) run the audit. No ad-hoc shell scripts, no hand-rolled regexes that break months later. This is the lesson learned from the seven restructures in this session — every one of them invented its own pattern, which is why we have stale labels and orphan numbering to clean up now.

---

### Phase 1 — Lossy deletions (re-home unique content first)
1. Re-home unique content from Ch 31 (Multimodal overview), Ch 41 (Embodied AI aggregator), Ch 45 (orphan section 45.6).
2. Delete Ch 31 and Ch 41 (Part VII shells).
3. Merge Ch 45's single section into Ch 44.

### Phase 2 — Sibling merges within parts
4. Part II: merge Ch 11 + Ch 12 (Interpretability + Tools).
5. Part VII (current): merge Ch 35 + Ch 37 (VLM + Omni).
6. Part VII: merge Ch 39 + Ch 40 (VLA + Robotics).
7. Part IX: merge Ch 53 + Ch 54 (Bias + Hallucination).
8. Part IX: merge Ch 56 + Ch 57 (Watermarking + Transparency).
9. Part IX: merge Ch 58 + Ch 59 (Environmental + Frontier Safety).
10. Part XI (current): merge Ch 63 + Ch 65 + Ch 68 (Ideation/Strategy/Hypothesis).
11. Part XII (current): merge Ch 78 + Ch 79 + Ch 80 (Manufacturing/Creative/Recommendation).

### Phase 3 — Cross-part content moves (Part V split, Multimodal reorder)
12. Move Part III sec 15.5 (Structured IE & NER) to become a chapter in new Part VI.
13. Move current Part VII Ch 38 (Streaming Multimodal) to new Part VII (Dialogue) as Voice & Realtime chapter.
14. Move current Part VII Ch 42 (Cross-Modal RAG) to new Part VI.
15. Split old Part V into new Part VI (Retrieval & IE, 6 ch) and new Part VII (Dialogue & CAI, 5 ch).
16. Split old Ch 23 (9 sections) across new Part VI Ch 3 (RAG Fundamentals) and Ch 4 (Advanced RAG / KG).
17. Move current Part VII (Multimodal) into the new Part V slot (model cluster).

### Phase 4 — Part X (Operations) split
18. Move current Part II sec 7.6, 7.8 (Distributed Training Systems) into new Part XI Ch 2.
19. Move current Part XIII Ch 84 (Frontier Systems & Hardware) into new Part XI Ch 3.
20. Split current Part X Ch 62 (11 sections) across:
    - New Part XI Ch 4 (Edge / On-Device)
    - New Part XII Ch 1 (Gateways)
    - New Part XII Ch 2 (Orchestration)
    - New Part XII Ch 3 (Containers / K8s)
    - New Part XII Ch 4 (Reliability / SLOs / Registry)
21. Move current Part X Ch 61 (Compute Planning) into new Part XI Ch 1.

### Phase 5 — Cascade renumbering
After all moves/deletions, run the canonical renumbering cascade so chapters are 0–N contiguous. Part numbering shifts: current VI–XIII become VIII–XV.

Mechanics (proven from the Parts 10–13 and Appendix C–G renumberings):
- `.__tmp__` intermediates to avoid collisions
- In-file metadata rewrite (title, meta, breadcrumb, page-current, pagefind-meta, anchor IDs, body refs)
- Cross-file href rewrite across the entire book
- Regenerate toc.html, part indexes, chapter indexes
- Rebuild linear nav chain

### Phase 6 — Audit gates between every phase
- P0 critical = 0
- P1 broken refs = 0
- P2 placeholders = 0
- P3 prose drift = 0
- Linear nav chain 100% coverage
- ToC matches disk

### Phase 7 — Re-sync manifest (closes the loop)
After all moves and renumbering, re-run the yaml refresh so `book_structure.yaml` matches the new disk reality. This is the manifest the *next* restructure will diff against. Without Phase 7, the next round inherits stale state and we're back to ad-hoc scripts.

```
python scripts/_refresh_book_structure_yaml.py  # captures new state
git diff book_structure.yaml book_structure.target.yaml  # should show ZERO diff
```

The zero-diff check is the success criterion: target became reality.

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Content loss during chapter merges | Extract unique H2 subsections from the absorbed chapter as new H2 blocks in the absorber; only delete the shell after content moved. |
| Broken cross-references during reorder | Phase boundaries each end with the full integrity audit. Cascade renumbering script handles slug + section-number rewrites in one pass. |
| Reader / search bookmark rot | Where chapters are merged, the new file's H2 anchor IDs preserve sensible anchors. Major moves get explicit `<a id="old-X-Y">` aliases for backward compatibility. |
| Two new parts increase numeric churn | One cascade renumbering at Phase 5 absorbs all shifts in a single audit-gated pass. |
| Hardware content split between Part XI and XV | Part XV Frontiers covers *frontier* hardware (chips not yet shipping, decentralized training research). Part XI covers production-ready hardware decisions (chip diversity, GPU procurement). Clear boundary. |

---

## 9. Open questions

1. **Part III at 4 chapters** — below the 5-chapter target. Acceptable as a deliberately compact "first foray" before the deeper parts split the workload, OR should we expand to 5 (e.g., split Ch 14 Prompt Engineering into "Foundational Prompts" + "Advanced Prompts")? Recommendation: **keep at 4**.

2. **Part IX (Evaluation) at 4 chapters** — same band-edge question. Recommendation: **keep at 4**; evaluation breaks cleanly into 4 cohesive topics.

3. **Part XV (Frontiers) at 4 chapters** after losing the Hardware chapter to Part XI. Recommendation: **keep at 4**; Frontiers is intrinsically a small, opinionated part.

4. **Should Appendices be promoted into a "Part XVI"?** They currently sit as `appendices/` outside the Roman numbering. Recommendation: **keep as-is**; Appendices have different reading dynamics (reference vs. linear).

---

## 10. Decision needed

Confirm the proposed structure and I execute Phases 0–7 in order with audit gates between phases. Estimated outcome:

- **13 parts → 15 parts** (+2 from the two splits, Multimodal reordered)
- **87 chapters → 86 chapters** (≈ same total, much better distributed)
- **413 sections → ~370 sections** (-10%)
- Every part in 4–9 chapter band, every chapter in 3–8 section band
- NER / structured extraction promoted to chapter status in Part VI
- Knowledge-graph arc contiguous in Part VI
- Voice / realtime unified in Part VII (no longer split across Conversation and Multimodal)
- Hardware content centralized in Part XI (no longer split across Part II, X, XIII, XV)
- Distributed training systems promoted to chapter status in Part XI
- Scale vs Ops separated by discipline
- Multimodal recognized as a model-cluster topic, not an application-cluster topic
- Zero duplicated topics across the table of contents

Estimated execution time at the script-level: 6 phases × audit gate, comparable in scope to the previous Parts 10–13 renumbering.
