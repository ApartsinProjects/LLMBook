# LLMBook Pending Tasks & Restructuring Plan

Captured: 2026-05-16. Single source of truth for what's open across the
current editorial pass. Sections:

1. [Backlog from current session](#1-backlog-from-current-session)
2. [Major restructuring (Parts 7, 9, 11, 12 + Chapter 25)](#2-major-restructuring)
3. [Cross-cutting work after restructuring](#3-cross-cutting-work)
4. [Decisions needed from author](#4-decisions-needed)
5. [Templating audit findings (May 2026)](#6-templating-audit)
6. [Appendix restructuring + thin-part remediation (added 2026-05-16)](#7-appendix-restructuring)
7. [book-update skill: install + push to git](#8-book-update-skill)

---

## 1. Backlog from current session

### 1.1 Substantive edits

- **18 library-shortcut callouts** to add (`library-shortcut-audit.md`). Top
  pattern: hand-rolled `cosine_similarity` (9 instances in Part 5, modules
  18-20) → faiss/sklearn shortcut. Second pattern: hand-rolled retry loops
  (4 instances) → tenacity shortcut. Other: hand-rolled chunkers, semantic
  cache, attention math.
- **Pseudocode reformat** (`pseudocode-readability-audit.md`):
  - Convert 4 blocks to `algo-helper` style (kills Pygments mis-tinting):
    sections 17.5 (Debate), 22.2 (MCP handshake), 17.1 (PPO), 21.1 (ReAct).
  - Add Input:/Output: headers to 8 dense Python-as-pseudocode blocks.
  - Fix step numbering in 3 blocks (32.3.5 Mamba, 8.3.4 RLVR, 28.3.1
    Token Bucket).
  - Standardize a/b/c sub-step indent to 2 spaces in 5 blocks.
  - Add phase-separator blank lines to 5 blocks ≥ 20 lines.
- **2 flagged pseudocode blocks** (from earlier audit): kept and renumbered
  this session (ReAct 21.1.2, MCP 22.2.1) — could still be replaced with
  proper sequence diagrams if author prefers.
- **Code Fragment Python re-format**: section-22.1.1 (OpenAI tools schema)
  has nested-block indent collapsed to a single level. The fix is a book-
  wide re-render: extract raw Python from each `<pre><code class="lang-python">`
  → run through `black` → re-render through Pygments → substitute back.
  Risk: large diff; need careful diff review.
- **Part 12 chapters 36 + 37 bibliography callouts**: chapters 36 (Legal)
  and 37 (Finance) got "Where to Read More" expansions in this session but
  not a dedicated `<div class="callout bibliography">`. Add for both. The
  in-flight enrichment agent for chapters 38-42 already includes this.

### 1.2 Audit punch lists not yet acted on

- **8 orphan code-output blocks** (e.g. section-30.3.4) — `<div class="code-output">`
  with no preceding `<pre>` parent.
- **14 wide-cell tables** flagged for column overflow.
- **62 overlong alt-texts** (>250 chars) — split into shorter primary alt
  + long-description supplement.
- **12 caption-colon typos** — `Figure 22.1.2` should be `Figure 22.1.2:`.
- **5 mismatched figure references** — `Figure 20.1.2` references but no
  such figure exists.

### 1.3 Hero / opener images

- **43 of 86 landing pages are barren** (no `<figure>` or hero image before
  the first `<h2>`):
  - All 12 part landings.
  - 17 chapter landings (Part 6 entirely; Part 12 entirely; plus Ch 1, 8,
    33, 34, 35).
  - 6 appendix landings (Q, R, S, T, U, appendices/index.html).
  - 8 front-matter pages (foreword, copyright, syllabi, how-to-use,
    reading-pathways, what-this-book-covers, who-should-read, look-inside).
- Requires image-generation pipeline (Gemini / SDXL / etc.). Treat as a
  separate workstream with a `_audit_opener_images.py` rerun once images
  land.

### 1.4 Other quality flags

- Earlier "wide-cell tables", "alt-text" etc. audits all live in
  `KDP/validation/_raw/audit_full.json` — not yet folded into this list.
- "Industry-Specific Practitioner Guides" prose at `appendices/index.html`
  line 36-38 mentions "Appendices W-AC" that don't exist (industries now
  live in Part 12). The heading at line 202 is empty after this session's
  fix; the prose at L36-38 still claims W-AC exist. Either remove that
  paragraph or update to point at Part 12.

---

## 2. Major restructuring

### 2.1 Goals (from author)

1. **Part 7 = Multimodal Generation**: extend with latest modalities &
   modes; consolidate by moving industry-specific sections OUT to Part 12.
2. **Part 9 = Safety + Security + Guardrails + Ethics**: drop Strategy
   (move to Part 11); absorb the safety/security half of Chapter 25.
3. **Part 11 = Complete Idea → Product cycle**: expand from 2 chapters to
   ~8-10 chapters covering Ideation → PM → Strategy → Vibe-Coding (new
   chapter name) → MVP (new chapter) → Compute → Scaling Economics →
   Shipping → Post-Launch Monitoring. Absorb Module 31 (Strategy) from
   Part 9 and the production/ops half of Chapter 25.
4. **Part 12 = Consolidated industry applications**: absorb Module 27
   (LLM Applications Across Industries) content into the existing
   industry chapters (36-42); promote section 27.1 (Vibe-Coding) into
   its own Part 11 chapter.

### 2.2 Chapter 25 split

| Current section | Title | New home |
|---|---|---|
| 25.1 | Agent Safety & Prompt Injection Defense | Part 9 (new Agent Safety chapter or merge into 30) |
| 25.2 | Sandboxed Execution Environments | Part 9 (Agent Safety chapter) |
| 25.3 | Production Observability & Cost Control | Part 11 (Shipping & Deploying chapter) |
| 25.4 | Error Recovery, Resilience & Graceful Degradation | Part 11 (Shipping & Deploying chapter) |
| 25.5 | Testing Multi-Agent Systems | Part 6 (keep — fits in Agentic AI) or move to Part 8 (Eval) |
| 25.6 | Agentic Security Benchmarks for Tool-Using Systems | Part 9 (Agent Safety chapter) |
| 25.7 | Supply-Chain Security for Agent Sandboxes | Part 9 (Agent Safety chapter) |

After split, Module 25 is effectively dissolved. Decision needed: keep the
slot empty (gap in numbering), or fully renumber Part 6 (24 = last chapter).

### 2.3 Module 27 dissolution into Part 12 / Part 11

| Current section | Title | New home |
|---|---|---|
| 27.1 | Vibe-Coding & AI-Assisted Software Engineering | Part 11 → new "Prototyping via Vibe-Coding" chapter |
| 27.2 | LLMs in Finance & Trading | Part 12 module-37 (Finance) — MERGE |
| 27.3 | Healthcare & Biomedical AI | Part 12 module-38 (Healthcare) — MERGE |
| 27.4 | LLM-Powered Recommendation & Search | Part 12 → new "Recommendation & Search" chapter (call it 43?) |
| 27.5 | Cybersecurity & LLMs | Part 12 module-40 (Cybersecurity) — MERGE |
| 27.6 | Education, Legal & Creative Industries | Split: Education → mod-39, Legal → mod-36; "Creative Industries" → new Part 12 chapter |
| 27.7 | Robotics, Embodied AI & Scientific Discovery | Part 7 module-26 (Multimodal — Embodied) — MERGE into existing 26.5/26.6 |

After dissolution, Module 27 is gone. Part 7 has only Module 26.

### 2.4 New Part 11 structure (proposed)

The complete idea → product cycle, in order:

| New chapter | Title | Source |
|---|---|---|
| Part-11 Ch 1 | **Ideation: Finding LLM-Worthy Problems** | NEW (author new chapter, draws from 34.1, 34.3) |
| Part-11 Ch 2 | **LLM Product Management** | Old 31.2 + 34.x; new chapter |
| Part-11 Ch 3 | **LLM Strategy & Use Case Prioritization** | Old 31.1, 31.4 |
| Part-11 Ch 4 | **Prototyping via Vibe-Coding** | Old 27.1 promoted to chapter + new content |
| Part-11 Ch 5 | **Building the MVP** | NEW (draws from 34.7 + new) |
| Part-11 Ch 6 | **From Prototype to Production Hypothesis** | Old 34 minus what moves elsewhere |
| Part-11 Ch 7 | **Compute Planning & Infrastructure** | Old 31.5, 31.6 |
| Part-11 Ch 8 | **Scaling Economics: Unit Costs & ROI** | Old 31.3, 31.7 |
| Part-11 Ch 9 | **Shipping & Deploying AI Products** | Old 35 + 25.3, 25.4 |
| Part-11 Ch 10 | **Post-Launch Monitoring & Iteration** | Old 35.4 + new |

That's 10 chapters in Part 11 (up from 2). Decision needed: stop at 10 or
fold some pairs together?

### 2.5 New Part 7 structure (proposed: extend with latest content)

| Section | Title | Status |
|---|---|---|
| 26.1 | Image Generation & Vision-Language Models | Keep, refresh with 2026 frontier (Imagen 4, FLUX.1.1, etc.) |
| 26.2 | Audio, Music & Video Generation | Keep, refresh (Veo 2, Sora 2, Suno v5, Udio v3) |
| 26.3 | Document Understanding & OCR | Keep |
| 26.4 | Unified Multimodal Models & Omni-Architectures | Keep (Gemini 2.5, GPT-5o, Llama-4 omni) |
| 26.5 | Embodied Multimodal Agents & VLA | Keep + absorb 27.7 robotics |
| 26.6 | LLM-Powered Robotics | Keep + absorb 27.7 |
| 26.7 | 3D Gaussian Splatting & Neural Scenes | Keep |
| NEW 26.8 | **3D Asset Generation & World Models** | NEW (Genie 3, DreamGen, Stable Zero123, latent NeRF, Trellis) |
| NEW 26.9 | **Multimodal Editing & Inpainting** | NEW (cover edit modes: image/video editing, audio remixing, scene relighting) |
| NEW 26.10 | **Multimodal Reasoning & Cross-Modal Retrieval** | NEW (CLIP descendants, BLIP-3, evaluation of cross-modal grounding) |
| NEW 26.11 | **Streaming & Real-Time Multimodal** | NEW (Gemini Live, GPT-4o Realtime, low-latency vision) |

Decision needed: how many new sections? Web research needed for 2026
frontier content.

### 2.6 New Part 9 structure (proposed)

| Module | Title | Source |
|---|---|---|
| 30 | Safety, Ethics & Regulation | Current 30 (12 sections) — keep |
| NEW | **Agent Safety & Sandboxing** | New chapter from 25.1, 25.2, 25.6, 25.7 |
| (drop) | ~~LLM Strategy, Product Management & ROI~~ | Move to Part 11 |

### 2.7 New Part 12 structure (proposed)

| Chapter | Title | Source / Change |
|---|---|---|
| 36 | LLMs in Legal Practice | Current + absorb 27.6 (Legal sub-section) |
| 37 | LLMs in Finance | Current + MERGE 27.2 |
| 38 | LLMs in Healthcare & Biomedical | Current + MERGE 27.3 |
| 39 | LLMs in Education | Current + absorb 27.6 (Education sub-section) |
| 40 | LLMs in Cybersecurity | Current + MERGE 27.5 |
| 41 | LLMs in Government & Public Sector | Current |
| 42 | LLMs in Manufacturing & Supply Chain | Current |
| NEW 43 | **LLMs in Creative Industries** | NEW from 27.6 Creative sub-section + new content (Adobe Firefly, Runway Gen-4, Suno, ElevenLabs) |
| NEW 44 | **LLM-Powered Recommendation & Search** | NEW from 27.4 + new content |

---

## 3. Cross-cutting work after restructuring

### 3.1 Renumbering (largest workstream)

- **If we keep numbers stable**: gaps appear (no Module 25, no Module 27,
  Module 31 in Part 11 numbering scheme). Cross-references stay valid.
- **If we fully renumber**: every chapter number changes downstream of the
  first move. Every cross-reference (`Chapter 27`, `Section 27.6`, etc.)
  needs rewriting. Every URL/filename needs rewriting (or a redirect
  scheme).

**Recommendation**: fully renumber, with a coordinated migration script
that:
1. Builds a mapping `(old_id) → (new_id)` for every chapter, section, and
   captioned fragment.
2. Rewrites all cross-references in HTML body text.
3. Rewrites all internal hrefs.
4. Renames files (`section-27.2.html` → `section-37.X.html`) and
   directories where module slug changes.
5. Updates `toc.html`, `appendices/index.html`, every part landing's
   chapter-card list, every chapter-nav anchor.
6. Updates `data-pagefind-meta` chapter/part values.
7. Updates every code/table/figure caption number that embeds chapter
   prefix (e.g. `Code Fragment 27.6.3` → new id).
8. Rebuilds Pagefind index after all renames.

### 3.2 Cross-reference verification

Build a `_audit_cross_ref_integrity.py` that:
1. Walks every HTML body looking for `Chapter N`, `Section X.Y`,
   `Part X`, `Appendix X[.N]`, `Figure X.Y.Z`, `Table X.Y.Z`, `Code Fragment X.Y.Z`.
2. Resolves each against the (post-renumber) actual target.
3. Reports any reference that resolves to a non-existent target.

Run before AND after the restructure.

### 3.3 Navigation rebuilds

- Re-run `_normalize_page_headers.py` to refresh breadcrumb labels.
- Re-run `_redesign_chapter_nav.py` to rebuild bottom nav with new
  numbering.
- Re-run `_fix_whatsnext_hyperlinks.py` to re-link cross-references in
  What's Next callouts.
- Rebuild `toc.html` (both short-form and detailed-form) from on-disk
  truth.
- Rebuild `appendices/index.html` cards.

### 3.4 New chapter authoring

New chapters needed:
- Part 11: Ideation, MVP (and possibly: Vibe-Coding chapter intro, etc.)
- Part 9: Agent Safety chapter (or expanded Module 30)
- Part 12: Creative Industries, Recommendation & Search
- Part 7: 4 new sections (3D Asset Generation, Multimodal Editing,
  Multimodal Reasoning, Streaming Multimodal)

Each new chapter needs:
- index.html with full template (breadcrumb, h1, subtitle, big-picture
  callout, section list, whats-next, chapter-nav)
- Section files
- Hero image (or stub for image-gen pipeline)
- Bibliography callout
- Cross-links from related chapters

### 3.5 Content merges (sections moving and combining)

Each move-and-merge needs:
1. Read source section's full content.
2. Read target chapter's relevant section.
3. Decide which framing wins; merge prose; preserve all callouts, figures,
   code fragments.
4. Renumber any code/table/figure captions to match the new chapter.
5. Add cross-link from old location to new location (one-time redirect
   note, or remove old file entirely).

### 3.6 URL stability

If renaming files/dirs:
- Decide whether to add HTTP 301 redirects (requires server config) or
  leave dead links (acceptable for a self-published book site).
- Update KDP / EPUB build pipeline to use new filenames.
- Update sitemap.xml and any external links / search-engine indexing.

---

## 4. Decisions needed from author

1. **Renumbering policy**: stable-with-gaps OR fully-renumber?
2. **Part 11 chapter count**: 10 chapters as proposed, or compress?
3. **Part 7 new section count**: 4 new (26.8-26.11) as proposed, more, or
   fewer?
4. **Part 12 new chapters**: Creative Industries (43) and Recommendation &
   Search (44) — confirm titles?
5. **Module 25 handling**: dissolve completely (no Module 25), or keep a
   skeleton in Part 6 with just 25.5 (Testing Multi-Agent Systems)?
6. **Module 30 vs new Agent Safety chapter**: expand Module 30 to ~16
   sections, or split off a new chapter?
7. **Filename strategy**: rename files to match new numbers
   (`section-37.8.html` etc.), or keep old names and only update labels?
8. **Image generation pipeline**: which tool (Gemini / SDXL / midjourney
   / nano-banana / Imagen 4)? Will the author provide prompts, or should
   they be auto-generated from chapter subtitles?
9. **Where to Read More vs Bibliography callout**: keep BOTH (Where to
   Read More = in-book cross-refs; Bibliography = external citations),
   or merge into one Bibliography-style callout?
10. **Cycle order**: confirm the Part 11 chapter order
    (Ideation → PM → Strategy → Vibe-Coding → MVP → Prototype-to-Prod →
    Compute → Scaling Economics → Shipping → Post-Launch). Some
    pre-iteration ordering questions: should Strategy come BEFORE PM
    (i.e., decide-what-business-this-is before product), or after?

---

## 5. Phasing (recommended)

If author approves the plan, recommended phase order:

**Phase A — Inventory & freeze**:
- Generate the canonical (old_id → new_id) mapping table.
- Generate the (source_section → target_location) movement table.
- Commit current state as a "pre-restructure" tag.

**Phase B — File moves and merges (one chapter at a time)**:
- Move Module 27 → Part 12 chapters (one section at a time).
- Move Module 31 → Part 11.
- Split Module 25 → Part 9 + Part 11.
- Run cross-ref audit after each move; fix breakages immediately.

**Phase C — New chapter scaffolding**:
- Create empty templates for new Part 11 chapters (Ideation, MVP,
  Prototyping, etc.).
- Create empty templates for new Part 12 chapters (Creative, Rec&Search).
- Create empty templates for new Part 7 sections.

**Phase D — Renumbering (if "full" chosen)**:
- Apply the (old_id → new_id) mapping book-wide.
- Rename files and dirs.
- Update all internal cross-references.
- Re-run normalize_page_headers, redesign_chapter_nav, whatsnext_hyperlinks.

**Phase E — Content authoring**:
- Write Ideation chapter (Part 11 Ch 1).
- Write MVP chapter.
- Write Creative Industries chapter (Part 12).
- Write Recommendation & Search chapter (Part 12).
- Write 4 new Part 7 sections (26.8-26.11) with 2026 frontier research.
- Expand Module 30 or new Agent Safety chapter.

**Phase F — Polish**:
- Re-run all `_audit_*.py` scripts.
- Hero image pipeline.
- Library-shortcut callouts.
- Bibliography callouts.
- Final cross-ref integrity pass.

---

## 6. Templating audit findings (May 2026)

Top 20 unification opportunities from `_audit_templating_opportunities.py`.
Full per-finding detail in `_audit_templating_opportunities.py` report.

**Highest leverage:**

1. **Pagefind init script duplicated in 352 files** (~30 lines each). Move
   the `window.addEventListener("DOMContentLoaded", ...)` block to
   `scripts/book.js`. Strips ~10K LoC.
2. **Edition string drift**: pages say "Fifteenth Edition", templates still
   say "Fourteenth". New pages generated from templates would silently
   regress. Fix: `BOOK_CONFIG.md` as single source of truth, templates
   read `{{ edition }}`.
3. **`<head>` + `<header class="chapter-header">` + `<nav class="chapter-nav">`
   partials**: 3 partials replace ~50 lines × 376 files = ~18,800 LoC.
4. **KaTeX renderMathInElement onload payload** duplicated across 77 math
   files. Move to `vendor/katex/katex-init.js`.
5. **551 inline `style="..."` attributes**, 78 distinct values. Worst:
   SVG gradient stops (`#f8f9fa`/`#e9ecef` opacity 0.7/0.3 — 68 each),
   `font-family: 'Segoe UI'` (50), figure captions (19). Define classes
   `.svg-stop-light`, `.svg-stop-mid`, `.font-ui`, `.fig-caption-inline`.
6. **19 distinct agent-avatar inline colors** — extract to
   `agents.json` registry + per-agent class.
7. **6 verbatim-duplicate `<div class="prerequisites">`** in module-22
   siblings — hoist to chapter index.
8. **1454 bibliography card structures** across 220 files — drive from
   `refs.json` + single render template.
9. **CSS magic numbers**: `#555` ×15, `#1a1a2e` ×13, `#e94560` ×11 — emit
   to `:root` CSS variables.
10. **CSS magic pixels**: `1px` ×90, `8px` ×51, `4px` ×39 — define a
    4px spacing scale `--space-1/2/3`.

The single root cause for items 2, 11, 12, 18 is "no central BOOK_CONFIG
consumed at build time". Wiring `BOOK_CONFIG.md` into the `html2pub` build
is the highest-leverage single change.

---

## 7. Appendix restructuring + thin-part remediation

### 7.1 Appendix restructure (4 thematic groups; absorb duplicates)

**Current state**: 22 appendices (A-U + Glossary), grouped into
"Foundations/Setup", "Reference Materials", "Framework Guides",
"Infrastructure/MLOps", "Ecosystem Overview", "Cross-Cutting Reference
Catalogs", "Pedagogy Kit", "Problem-Solution Key", "Freshness".

**Author goals**:
- Consolidate "LLM Tooling Ecosystem" (P) into "Framework Guides".
- Consolidate "E Git/DVC" into "Infrastructure and MLOps".
- Drop the "Reference Materials" group heading (the items are too technical
  to deserve their own group; either move to other groups or drop).
- Final 4 thematic groups.

**Proposed 4-group structure**:

**Group 1 — Foundations (theoretical background)**
| New letter | Old letter | Title | Note |
|---|---|---|---|
| A | A | Mathematical Foundations | Keep |
| B | B | Machine Learning Essentials | Keep |
| C | C | Python Libraries and Patterns for LLM Development | Keep |
| D | D | Development Environment Setup | Keep |
| NEW | — | **Information Theory & NLP Theoretical Background** | NEW (deeper theory the author wants) |

**Group 2 — Framework Guides**
| New letter | Old letter | Title | Note |
|---|---|---|---|
| E | J | HuggingFace: Transformers, Datasets, and Hub | Renumber J → E |
| F | K | LangChain: Chains, Agents, and Retrieval | Renumber K → F |
| G | P + (parts of K) | LLM Tooling Ecosystem | Merge P into K-as-F, OR keep as separate G |
| H | G | Model Cards and Selection Guide | "Quick-reference" for picking a model — Framework-adjacent |

**Group 3 — Infrastructure, MLOps & Cross-Cutting Reference Catalog**
| New letter | Old letter | Title | Note |
|---|---|---|---|
| I | E | Git, DVC, and Reproducibility | E → I (Infrastructure group) |
| J | F | GPU Hardware and Cloud Compute | F → J |
| K | L | Experiment Tracking: W&B and MLflow | L → K |
| L | M | Inference Serving: vLLM, TGI, and SGLang | M → L |
| M | N | Distributed ML: PySpark, Databricks, Ray | N → M |
| N | O | Docker and Containers for LLM Deployment | O → N |
| O | Q | Master Reference Tables | Q → O |
| P | R | Production Patterns Reference | R → P |

**Group 4 — Pedagogical Kit & Capstone**
| New letter | Old letter | Title | Note |
|---|---|---|---|
| Q | S | Pedagogy Kit (Capstone, Projects, War Stories) | S → Q (this is the capstone home) |
| R | T | Problem-Solution Key | T → R |
| S | U | 2026 Freshness Index | U → S |
| T | H | Prompt Template Catalog | H → T (moves from "Reference" → Pedagogy) |
| U | I | Datasets, Benchmarks, and Leaderboards | I → U (student/instructor resource) |

**Glossary** stays standalone (no letter — just "Glossary"), as fixed
earlier this session.

**Drop**: Nothing actually dropped — all 22 appendices preserved, just
regrouped + 1 new theory appendix added → 23 lettered appendices (A-U) +
Glossary.

**Alternative (slimmer) plan**: actually drop G (Model Cards) and merge
its content into Framework Guides prose; drop H (Prompt Templates) and
merge its content into Pedagogy Kit; drop I (Datasets) and merge its
content into 2026 Freshness. → 18 appendices instead of 23. Decision
needed.

### 7.2 Part 10 (Frontiers) — currently single module (Module 33)

Module 33 has 11 sections, plenty of material to split:

| Old section | Title | New home |
|---|---|---|
| 33.1 | Emergent Abilities: Real or Mirage? | New Module A (Frontier Architectures) |
| 33.2 | Scaling Frontiers: What Comes Next | New Module A |
| 33.3 | Alternative Architectures Beyond Transformers | New Module A (Mamba, SSM, MoE) |
| 33.4 | World Models: Video Generation, Simulation, Embodied | **Move to Part 7** (Multimodal Generation) |
| 33.5 | A Theory of Reasoning in LLMs | New Module B (Frontier Theory) |
| 33.6 | Memory as a Computational Primitive | New Module B |
| 33.7 | Mechanistic Interpretability at Scale | New Module B |
| 33.8 | The Nature of Agency | New Module B |
| 33.9 | Efficient Multi-Tool Orchestration | **Move to Part 6** (Agentic AI) |
| 33.10 | LLMs as Universal Sequence Machines | New Module A |
| 33.11 | What 2026 Settled (and What Remains Open) | New Module B (closing section) |

**Proposed Part 10 structure** (2 modules):

| Module | Title | Sections |
|---|---|---|
| Module A (formerly 33) | **Frontier Architectures & Scaling** | 33.1, 33.2, 33.3, 33.10 |
| Module B (NEW) | **Frontier Theory & Open Questions** | 33.5, 33.6, 33.7, 33.8, 33.11 |

(Sections 33.4 and 33.9 move out as noted above.)

### 7.3 Part 7 (Multimodal) — single module after Module 27 dissolves

Per existing restructuring plan, Module 27 dissolves into Parts 11 and 12.
After that, Part 7 would have only Module 26 — same single-module problem.

**Proposed Part 7 structure** (2 modules):

| Module | Title | Sections |
|---|---|---|
| Module 26 | **Multimodal Generation Foundations** | 26.1 Image, 26.2 Audio/Music/Video, 26.3 Document/OCR, 26.4 Unified/Omni, plus new section "Streaming & Real-Time Multimodal" |
| Module 27 (NEW; reuses freed-up number) | **Embodied AI, World Models & Multimodal Reasoning** | 26.5 VLA, 26.6 Robotics, 26.7 3D Gaussian, 33.4 World Models (absorbed from Part 10), plus new sections "3D Asset Generation", "Multimodal Editing", "Multimodal Reasoning" |

This gives Part 7 two solid chapters and preserves all current 26.X
content. Module 27 number is freed up by the old Module 27 dissolution.

### 7.4 Audit of chapter counts per part (post-restructure)

| Part | Chapters | Notes |
|---|---|---|
| 1 (Foundations) | 6 | OK |
| 2 (Understanding LLMs) | 5 | OK |
| 3 (Working with LLMs) | 3 | OK (thin but coherent) |
| 4 (Training & Adapting) | 4 | OK |
| 5 (Retrieval & Conversation) | 3 | OK |
| 6 (Agentic AI) | 5 (or 4 if Ch 25 dissolves) | OK either way |
| 7 (Multimodal) | **2 after fix** | Was 2 → 1 → fixed back to 2 |
| 8 (Evaluation & Production) | 2 | OK (thin; possible promotion of section to module if needed) |
| 9 (Safety + Security + Guardrails + Ethics) | **2-3 after restructure** | 30 + new Agent Safety chapter + possibly 25.1-25.2-25.6-25.7 reorganized |
| 10 (Frontiers) | **2 after fix** | Was 1 → fixed to 2 |
| 11 (Idea → Product) | 8-10 | Big expansion per existing plan |
| 12 (Applications) | 7 → 9 | + Creative Industries + Recommendation & Search |

### 7.5 Naming consistency audit

Currently the Parts have inconsistent title style:
- "Part I: Foundations" (terse noun)
- "Part II: Understanding LLMs" (gerund)
- "Part III: Working with LLMs" (gerund)
- "Part IV: Training and Adapting" (gerund pair)
- "Part V: Retrieval and Conversation" (noun pair)
- "Part VI: Agentic AI" (terse noun)
- "Part VII: AI Applications" (terse noun — also misleading; should be "Multimodal Generation")
- "Part VIII: Evaluation and Production" (noun pair)
- "Part IX: Safety and Strategy" (noun pair — should change to "Safety, Security, Guardrails, Ethics")
- "Part X: Frontiers" (terse noun)
- "Part XI: From Idea to AI Product" (phrase) ← inconsistent with others
- "Part XII: LLM Applications Across Industries" (noun phrase)

**Recommended uniform style**: "noun-phrase" (matches the majority).
Proposed renames:
- VII: "Multimodal Generation"
- IX: "Safety, Security & Ethics"
- X: "Frontiers" (keep)
- XI: "Idea to Product"
- XII: "Applications Across Industries"

Decision needed: lock the style.

### 7.6 Appendix renumbering implication

If we accept the Section 7.1 plan with renumbering A-U + Glossary, then
**every cross-reference in the book to an appendix needs rewriting**:
- All `Appendix K` → `Appendix F` (LangChain) etc.
- All `K.1.2` code/figure caption letters → corresponding new letter.
- All href paths if directories are renamed.

This is the same kind of coordinated rewrite as the chapter renumbering
in §2.1. Same script can handle it.

### 7.7 Decisions needed (appendix + thin parts)

11. **Appendix restructure**: full 4-group regrouping per §7.1, or
    minimal "consolidate duplicates only" (just merge P into K, move E to
    Infrastructure section heading)?
12. **Drop appendices** G (Model Cards), H (Prompt Templates), I
    (Datasets) — yes, fold their content elsewhere; or no, keep them?
13. **Add NEW Foundations appendix** (Information Theory + deeper NLP
    theory)?
14. **Appendix-letter renumbering**: rename directories + files to reflect
    new letters, or keep old directory names + only update labels?
15. **Part X (Frontiers) split**: 2 modules as proposed (Frontier
    Architectures + Frontier Theory), or different split? Confirm 33.4 →
    Part 7 and 33.9 → Part 6 moves.
16. **Part VII second module**: confirm Module 27 reuse for "Embodied +
    World Models + Multimodal Reasoning" with sections drawn from 26.5,
    26.6, 26.7, 33.4 + new content.
17. **Part naming style**: lock "noun-phrase" pattern; rename VII, IX, XI,
    XII per §7.5.

---

## 8. book-update skill: install + push to git

Skill scaffolded at `~/.claude/skills/book-update/`. Includes:

```
SKILL.md             # Entry point: 6 modes, deps, global rules
modes/
  scout.md           # Find stale/missing/sparse content (read-only)
  refresh.md         # Apply scout findings
  enrich.md          # Add callouts/hyperlinks/bibliography
  illustrate.md      # Hero images via gemini-imagegen
  diagram.md         # Figures via technical-diagram-designer
  code-refresh.md    # Stale code + library-shortcut callouts
adapters/
  llmbook.md         # LLMBook-specific layout, callout taxonomy, scripts
scripts/
  detect_book_layout.py    # Auto-detect adapter on first run
references/          # Placeholder for prompt templates
```

Smoke-tested: detector emits valid `config.json` for LLMBook (adapter=llmbook,
edition string, callout class list, all paths).

**Next steps**:

- Pick a final skill name. `book-update` is provisional. Alternatives:
  `book-refresh`, `book-maintain`, `book-pipeline`, `book-author-tools`.
- Decide install location:
  - Already installed at `~/.claude/skills/book-update/` (Claude Code
    auto-discovers it via the system).
  - Need to push to the shared `claude-skills` GitHub repo so it's
    versioned + sharable with collaborators.
- Find the local clone of `claude-skills` (the broken symlink at
  `~/.claude/skills/book-skills` points at `/e/Projects/LLMCourse/agents/book-skills`
  which doesn't exist on this machine; the actual clone may be elsewhere).

**Decision needed (18)**: confirm skill name + provide local-clone path for
the claude-skills repo, OR I can `gh repo clone` it fresh into a chosen
location.

