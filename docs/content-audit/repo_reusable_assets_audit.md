# Repo Reusable Assets Audit

Walking `E:\Projects\BookBlogsHome\LLMBook` (v2.0 branch) to identify reusable
assets (agents, scripts, templates, CSS, preserved content) that could improve
the book in its current state. Read-only audit; no files were edited.

---

## 1. Agents in `agents/book-skills/agents/*.md` (42 files)

Quick inventory. For each, a one-line description plus a "Run NOW" flag for
agents that would have immediate, high-value impact on the v2.0 state of the book.

| # | File | One-line description | Run NOW? |
|---|------|----------------------|----------|
| 00 | `00-chapter-lead.md` | Chapter Lead: orchestrates other agents end-to-end per chapter. | Yes, for any new-chapter regenerations |
| 01 | `01-curriculum-alignment.md` | Curriculum Alignment Reviewer: ensures chapter serves the whole course. | |
| 02 | `02-deep-explanation.md` | Deep Explanation Designer: ensures depth, intuition, justification beyond procedure. | Yes (Ch 36/41/56/61 are platform inventories that under-explain "why") |
| 03 | `03-teaching-flow.md` | Teaching Flow Reviewer: lecturer-style classroom readiness check. | |
| 04 | `04-student-advocate.md` | Student Advocate: non-expert reader's perspective on clarity. | |
| 05 | `05-cognitive-load.md` | Cognitive Load Optimizer: controls density / pacing. | Yes for Ch 36 / 61 (huge tool catalogs in one section) |
| 06 | `06-example-analogy.md` | Example and Analogy Designer: concrete examples + analogies. | |
| 07 | `07-exercise-designer.md` | Exercise Designer: practice problems reinforcing concepts. | |
| 08 | `08-code-pedagogy.md` | Code Pedagogy Engineer: produces pedagogically effective code blocks. | |
| 09 | `09-visual-learning.md` | Visual Learning Designer: produces SVGs / matplotlib figures. | |
| 10 | `10-misconception-analyst.md` | Misconception Analyst: predicts likely student errors. | |
| 11 | `11-fact-integrity.md` | Fact Integrity Reviewer: technical fact-checking, citations, benchmarks. | **Yes (priority)** — see hallucination_audit.md |
| 12 | `12-terminology-keeper.md` | Terminology and Notation Keeper: vocabulary / symbol consistency. | |
| 13 | `13-cross-reference.md` | Cross-Reference Architect: inserts internal links into HTML. | Yes (new chapters under-linked back to Parts 1-3) |
| 14 | `14-narrative-continuity.md` | Narrative Continuity Editor: chapter-as-story coherence. | |
| 15 | `15-style-voice.md` | Style and Voice Editor: voice / reading-experience consistency. | |
| 16 | `16-engagement-designer.md` | Engagement Designer: liveliness without losing seriousness. | |
| 17 | `17-senior-editor.md` | Senior Developmental Editor: O'Reilly/Manning-grade structural editor. | |
| 18 | `18-research-scientist.md` | Research Scientist and Frontier Mapper: deeper science, open questions, frontier callouts, citation accuracy. | **Yes (priority)** for Ch 34 / 46 / 56 / 59 |
| 19 | `19-structural-architect.md` | Structural Refactoring Architect: chapter/section-level organization. | |
| 20 | `20-content-update-scout.md` | Content Update Scout: external awareness, currency, version-number freshness, deprecated-tool flagging. | **Yes (priority)** for Ch 36 / 41 / 56 / 61 (vendor info dates fast) |
| 21 | `21-self-containment-verifier.md` | Self-Containment Verifier: every chapter understandable on its own. | |
| 22 | `22-opening-hook-designer.md` | Opening / Hook Designer: chapter titles, framing, first-page hooks. | |
| 23 | `23-project-catalyst.md` | Project Catalyst Designer: "you could build this" mini-project ideas. | |
| 24 | `24-aha-moment-engineer.md` | Aha-Moment Engineer: identifies and stages key "Oh, NOW I get it" moments. | **Yes (priority)** — new tool chapters are heavy on lists, light on insight reveals |
| 25 | `25-visual-identity-director.md` | Visual Identity Director: callout/figure/icon system enforcement. | |
| 26 | `26-demo-simulation-designer.md` | Demo and Simulation Designer: interactive demos, notebooks, sliders. | |
| 27 | `27-memorability-designer.md` | Memorability Designer: mnemonics, recurring contrasts, mental schemas. | **Yes** — Ch 36 (vector DB landscape), Ch 61 (training stack) badly need compact mental maps |
| 28 | `28-skeptical-reader.md` | Skeptical Reader: challenges generic / textbook-standard prose. | Yes (Ch 41, 56, 61 prose feels formulaic) |
| 29 | `29-prose-clarity-editor.md` | Prose Clarity Editor: simplification + sentence flow + jargon gatekeeping. | |
| 30 | `30-readability-pacing-editor.md` | Readability and Pacing Editor: micro-chunking + fatigue detection. | |
| 31 | `31-illustrator.md` | Illustrator: generates humorous + pedagogical illustrations via Gemini, embeds figures. | **Yes (priority)** — new chapters mostly have one hero illustration each at best |
| 32 | `32-epigraph-writer.md` | Epigraph Writer: opening-quote selection / verification. | |
| 33 | `33-application-example.md` | Application Example Agent: inserts "Practical Example" mini-case-studies. | |
| 34 | `34-fun-injector.md` | Fun Injector: 1-2 well-placed humor moments per chapter. | Yes for Ch 34 / 46 / 56 / 59 / 61 (formal-tool prose feels dry) |
| 35 | `35-bibliography.md` | Bibliography Agent: hyperlinked references section per chapter. | Yes (Ch 36 / 41 / 56 / 61 references are thin / inconsistent) |
| 36 | `36-meta-agent.md` | Meta Agent: audits other agents' output, edits skill files. | |
| 37 | `37-controller.md` | Chapter Controller: dispatches specialists to fix gaps. | |
| 38 | `38-publication-qa.md` | Publication QA: Playwright-based final visual gate. | Yes pre-shipping |
| 39 | `39-figure-fact-checker.md` | Figure and Diagram Fact Checker: verifies numbers in figures, SVGs, code outputs. | **Yes (priority)** — pairs with Fact Integrity to catch Llama-3 mix error etc. |
| 40 | `40-code-caption-agent.md` | Code Caption / Reference Agent: enforces caption + opening comment + prose reference for every code block. | |
| 41 | `41-lab-designer.md` | Hands-On Lab Designer: 30-90 minute guided labs at section ends. | Yes — new chapters have ~zero lab content |

### Top "Run NOW" list (highest leverage given current book state)

1. **#11 Fact Integrity Reviewer + #39 Figure Fact Checker** — paired against Ch 36, 56, 59, 61. The hallucination audit (sibling file) already documented at least 2 HIGH-severity and 8 MEDIUM factual errors; a systematic pass would catch the rest.
2. **#20 Content Update Scout** — pretraining-corpus, vendor-pricing, version-number freshness across Ch 36 / 41 / 56 / 61. These chapters age in months, not years.
3. **#18 Research Scientist** — Ch 34 (Open IE, coreference), Ch 46 (judge model literature), Ch 56 (NIST/EU AI Act), Ch 59 (frontier training papers). Frontier callouts are mostly missing in these chapters.
4. **#24 Aha-Moment Engineer + #27 Memorability Designer** — Ch 36 and Ch 61 are dense list-after-list; readers will not retain anything without compact mental schemas (e.g. "the four axes of vector DB choice", "the three layers of LLM safety", "the three orthogonal parallelism axes").
5. **#31 Illustrator** — Ch 36 / 41 / 56 / 61 each have ~1 SVG diagram and no hero/humor illustrations. New chapters look text-heavy compared to Parts 1-4.
6. **#41 Lab Designer** — none of the new chapters have hands-on labs. Adding even one lab per chapter (e.g. "deploy a Qdrant + bge-m3 + reranker locally" in Ch 36) materially upgrades them.
7. **#34 Fun Injector** — tool chapters in particular read as catalogs; 1-2 fun notes per chapter would lift voice without breaking authority.

### Secondary tier (would help but lower leverage right now)
- #13 Cross-Reference Architect, #35 Bibliography Agent — references in new chapters are thinner than Parts 1-4.
- #28 Skeptical Reader — flags the "every vendor gets one positive paragraph" feeling.
- #38 Publication QA — only needed pre-ship, not mid-development.

---

## 2. Scripts in `scripts/*.py` (project-level, ~190 files)

The project root has a very large script archive split into:

| Category | Count | Status |
|----------|-------|--------|
| `_audit_*.py` (audit scripts) | ~40 | Mix of current and one-shot. Many produced reports now in repo root. |
| `_fix_*.py` (one-shot fixes) | ~50 | Already-run. Should probably move to `scripts/_archive/`. |
| `_migration_step*.py` (v9 → v10 migration) | 8 | Already-run. Archive candidates. |
| `_appendix_reshuffle_v*.py` | 5 | Already-run. Archive candidates. |
| `v9_wave*.py` (v9 restructuring waves) | ~20 | Already-run. Archive candidates. |
| `wave11_*.py` … `wave31_*.py` (subsequent waves) | ~50 | Already-run; some recent. Archive candidates. |
| `restructure_*/` subdirs (part 7/8/9/10 restructures) | 4 dirs | Already-run. Archive candidates. |
| Active maintenance scripts | ~10 | Still useful (book.js, build_content_index.py, build_book_structure.py, rebuild_toc.py, etc.) |
| `audit/`, `detect/`, `fix/`, `generate/` subdirs | 4 dirs | Reusable utilities. |

### Categorization (sampled, representative)

| Script | Status |
|--------|--------|
| `_build_book_structure.py` | **Still useful** — regenerates `book_structure.yaml`. |
| `_rebuild_chapter_indexes.py` | **Still useful** — chapter index regeneration. |
| `_rebuild_part_indexes.py` | **Still useful** — Part index regeneration. |
| `_rebuild_toc.py` | **Still useful**. |
| `build_content_index.py` | **Still useful** — produces `book_content_index.jsonl` for search/scout agents. |
| `audit_inline_svgs.py` | **Still useful** — pairs with v2.0 SVG-heavy new chapters. |
| `audit_html_wellformed.py` | **Still useful** — gate pre-ship. |
| `audit_callout_bibliography.py` | **Still useful** — Ch 36/41/56/61 bibliographies need this. |
| `audit_hyperlinks.py` | **Still useful**. |
| `audit_practical_examples.py` | **Still useful** — Ch 56/61 are light on Practical Example callouts. |
| `verify_toc_links.py` | **Still useful**. |
| `fill_bibliographies.py` | **Possibly useful** but could be subsumed by Agent #35. |
| `wave31_fix_escaped_dollar.py` | **Already-run; archive.** |
| `wave29_convert_h2_to_callouts.py` | **Already-run; archive.** |
| `wave28_strong_and_fakeq.py` | **Already-run; archive.** |
| `wave27c_id_dedup_final.py` | **Already-run; archive.** |
| `wave22_biblio_and_math.py` | **Already-run; archive.** |
| `wave20_style_unification.py` | **Already-run; archive.** |
| `v9_wave9*` family | **Already-run; archive** (these split RAG/LLMOps and promoted NER/judge into their own chapters; the work that created the new chapters this audit targets). |
| `_migration_step1..step8` | **Already-run; archive** (v9 → v10 path/rename migration). |
| `_appendix_reshuffle_v8/v9/v10/v11` | **Already-run; archive.** |
| `restructure_part7/`, `part8/`, `part9/`, `part10_split/` | **Already-run; archive whole directories.** |
| `_visual_assets_sweep.py` | **Still useful**. |
| `compress_book_images.py` | **Still useful** pre-ship. |
| `_add_library_shortcuts.py` | **Still useful** — Ch 36 / 41 / 61 could use more Library Shortcut callouts. |
| `_find_shortcut_gaps.py` | **Still useful** — pair with above. |
| `_fix_caption_drift_in_moved_sections.py` | **Already-run; archive.** |

**Recommendation:** create `scripts/_archive/` and move all `wave*`, `v9_wave*`, `_migration_step*`, `_appendix_reshuffle_v*`, and `restructure_*/` directories there. This will cut the scripts/ directory from ~190 to ~40 active scripts, dramatically improving navigability.

---

## 3. Utility scripts in `agents/book-skills/scripts/`

| Subdir / file | Notes |
|---|---|
| `generate_icons_gemini.py` | Icon batch generator (Gemini Imagen + batch API). **Useful** — has not been run against v2.0 new chapter content; may be missing icons for new callout types if any were added. |
| `audit/run.py` + `audit/checks/*.py` (~70 plugin checks) | **High-value, under-used against new chapters.** Plugin runner with checks like `p0_broken_xref`, `p1_caption_misalignment`, `p1_figure_sequence`, `p1_chapter_starter`, `p2_callout_type_mismatch`, etc. **Worth running NOW against all 7 new chapters.** |
| `fix/` (~13 fix scripts) | Reusable fixes for accessibility, SVG clipping, code blocks, math, captions, structural HTML. Most have not been run against the new chapters; especially `fix_caption_numbering.py`, `fix_structural_html.py`, `fix_code_blocks.py`. |
| `detect/` (~4 detection scripts) | `audit_html_quality.py`, `audit_svg_quality.py`, `audit_print_contrast.py`, `validate_format.py`. Older pre-plugin system; superseded by `audit/`. |

**Recommendation:** **Run `python -m scripts.audit.run` against Ch 34, 36, 41, 46, 56, 59, 61 immediately.** The plugin runner reports lots of structural issues we have not surfaced yet (caption misalignment, figure sequence, vague headings, missing meta descriptions, etc.) The 70 checks are quite comprehensive.

---

## 4. `.book-update/` preserved content

| Path | Notes |
|---|---|
| `.book-update/v9-preserved-content/multimodal-reasoning-cross-modal-retrieval-section-41.7.html` | A section file from an old numbering scheme (when "section 41.7" meant multimodal reasoning under Part 6). Looks like a fragment preserved across the v9 → v10 restructure. **Not unused in a problematic way** — it's archived content. Verify the content was actually merged into Ch 33 (cross-modal RAG) before any cleanup. |
| `.book-update/v9-preserved-content/world-models-and-embodied-reasoning-section-41.4.html` | Same situation. Likely now lives in Ch 41 or Part 6. |
| `.book-update/cleanup_orphan_sections.py` | Looks like the script that produced the v9 preservation. Already-run. |
| `.book-update/standardize_bib.py` | Bibliography standardizer. **Possibly still useful** for ongoing bibliography work; has a stats JSON next to it (`standardize_bib_stats.json`). |
| `.book-update/test_bib.py` | Companion test for the standardizer. Useful. |
| `.book-update/config.json` | Configuration for the standardizer pass. |

**Recommendation:** verify the two preserved HTML files have either been reincorporated into the new structure or can be archived to a longer-term backup outside the active repo. Bibliography standardizer is still relevant; bring `standardize_bib.py` into the regular toolset.

---

## 5. Templates

| Template | Status |
|---|---|
| `templates/section.html` | **Looks current** (v9 wave fully integrated). Stylesheet path is `../../styles/book.css` ✓. Contains epigraph, big-picture callout, sample callouts. Single source of truth for new section pages. |
| `templates/chapter-index.html` | Present. Worth verifying it matches what `_rebuild_chapter_indexes.py` actually emits for v2.0 (esp. bibliography section, what's-next, illustration block). |
| `templates/part-index.html` | Present. Same caveat. |
| `agents/book-skills/templates/section-template.html` | **DIVERGENT from project template.** Skill template uses placeholder syntax (`{{NUM}}`, `{{SECTION_TITLE}}`) and includes `<meta name="description">` + KaTeX + Prism scaffolding. The project's `templates/section.html` lacks the KaTeX block and uses different placeholders. **Update needed:** these two should be kept in sync, or the skill template should be authoritative (since the skill is the reusable artifact). |
| `agents/book-skills/templates/chapter-index-template.html` | Likely needs the same sync check. |
| `agents/book-skills/templates/part-index-template.html` | Likely needs the same sync check. |
| `agents/book-skills/templates/chapter-status-template.md` | Tracks per-chapter audit status. Helpful for managing wave passes. |
| `agents/book-skills/templates/book-template.css` | Reference CSS in the skill. **Stale** — see CSS section below. |

### Recommendation for templates

The project's `templates/` and the skill's `agents/book-skills/templates/` have **drifted apart**. Pick one of two paths:
1. **Treat the skill templates as authoritative**, regenerate project templates from skill, archive duplicates.
2. **Treat the project templates as authoritative**, update skill to match for portability.

Option 1 is cleaner for skill reuse. Option 2 reflects what the book actually ships. Either way: **document which is authoritative in README.md.**

---

## 6. CSS / Palette

| File | Lines | Status |
|---|---|---|
| `styles/book.css` | 4,238 | **Current; authoritative.** Used by every page. |
| `styles/pygments.css` | (separate) | Pygments syntax highlighting; current. |
| `styles/icons/` | dir | Callout icons (PNG/SVG, 48×48). Current. |
| `agents/book-skills/styles/book.css` | 2,790 | **OUTDATED.** ~1,400 lines behind project; the skill's reusable CSS does not contain the styling that ships with the book. |
| `agents/book-skills/agent-shared.css` | Small | Older simpler color palette (`--primary`, `--accent`, `--highlight`, `--bg`); appears unused by current chapter pages. |
| `agents/book-skills/styles/icons/` | dir | Icon copies; should be checked against project icons. |

### Opportunities for CSS improvement
- **Sync skill CSS to project CSS**: required if the skill is supposed to bootstrap a new book project.
- **Audit `book.css` for unused selectors**: at 4,238 lines, there are almost certainly stale rules from earlier waves (e.g. `.level-badge` from when chapter sections had beginner/intermediate/advanced badges, classes for callout types that may have been retired, etc.). A PurgeCSS or hand-curated `audit_unused_css.py` run would shrink the stylesheet.
- **`agent-shared.css` looks vestigial**: investigate whether anything still depends on it. If nothing does, retire it.
- **Print stylesheet**: `audit_print_contrast.py` (in `agents/book-skills/scripts/detect/`) exists but has not been run recently against the full book. Worth running pre-ship.
- **Palette consolidation**: the new chapters' SVG diagrams (Ch 34, 36, 59, 61) use ad-hoc colors (`#27ae60`, `#8e44ad`, `#f39c12`, `#3498db`, `#1a4078`, `#1f7a3a`, `#a67c1a`) rather than the book palette variables. Migrating SVG colors to CSS custom properties would unify the visual identity (work for Agent #25 Visual Identity Director).

---

## 7. Recommended next workflow

Given the current state of the book (v2.0 with 7 new chapters in Parts 7, 8, 9,
11, 12), the highest-leverage next sequence:

### Phase A — Mechanical hygiene (1-2 days)
1. Run `python -m scripts.audit.run` against the 7 new chapter directories.
   Apply auto-fixes; manually triage residuals.
2. Run `_audit_callout_format.py`, `_audit_caption_typos.py`,
   `_audit_crossref_integrity.py`, `_audit_pseudocode_classification.py`
   against the same set.
3. Run `_audit_library_shortcut_opportunities.py` and `_find_shortcut_gaps.py`
   to identify where Ch 36/41/61 should have more Library Shortcut callouts.
4. Move already-run wave scripts to `scripts/_archive/`.

### Phase B — Fact and currency pass (3-5 days)
1. **Agent #11 Fact Integrity Reviewer** + **Agent #39 Figure Fact Checker** in
   Audit mode against Ch 36, 56, 59, 61. Use the existing
   `hallucination_audit.md` as a starting list of suspect claims.
2. **Agent #20 Content Update Scout** in Audit mode against Ch 36, 41, 56, 61
   (vendor product names, launch dates, pricing). Refresh dated content.
3. Run `_audit_stale_apis.py` and `_audit_nav_staleness.py` book-wide.
4. Fix the two HIGH-severity items from the hallucination audit (Rauber → Rebedea;
   Llama-3 data mix percentages).

### Phase C — Pedagogical lift (1-2 weeks)
1. **Agent #18 Research Scientist** in Suggest mode against Ch 34, 46, 56, 59.
   Add Research Frontier callouts where the chapters currently stop at "what
   tools exist."
2. **Agent #24 Aha-Moment Engineer** + **Agent #27 Memorability Designer**
   against Ch 36 (vector DB landscape), Ch 41 (platform map), Ch 61 (training
   stack). Add 2-3 compact mental schemas per chapter (e.g. four-axis platform
   maps, three-layer safety stack).
3. **Agent #41 Lab Designer** to insert one hands-on lab per new chapter.
4. **Agent #31 Illustrator** to fill the 5-8 illustrations-per-chapter target
   in Ch 36 / 41 / 56 / 61 (currently each has 1-2 only).

### Phase D — Polish (3-5 days)
1. **Agent #34 Fun Injector** for 1-2 humor moments per new chapter.
2. **Agent #28 Skeptical Reader** against Ch 41, 56, 61 (most generic prose).
3. **Agent #35 Bibliography Agent** to fill out reference sections.
4. **Agent #38 Publication QA** for final visual gate.
5. Sync `agents/book-skills/styles/book.css` ↔ `styles/book.css` so the skill
   is shippable to a new book project. Update skill templates accordingly.

### Crosscutting / always-on
- `_audit_crossref_integrity.py`, `_audit_internal_links.py`, `verify_toc_links.py`
  after every wave.
- The audit plugin runner (`scripts/audit/run.py`) on every CI run.

---

## Summary of asset health

| Asset class | Health | Action |
|---|---|---|
| Agents (42 markdown files) | Healthy, comprehensive | Run priority subset NOW |
| Project scripts (~190 .py) | **Bloated** with already-run wave scripts | Archive ~140 to `_archive/` |
| Skill utility scripts (~90 across audit/fix/detect) | Healthy, under-used on new chapters | Run plugin audit on new chapters |
| `.book-update/v9-preserved-content/` | 2 HTML fragments, possibly already merged | Verify and archive |
| `.book-update/standardize_bib.py` | Healthy, still relevant | Keep, run on new chapters |
| Project `templates/` | Current | Keep |
| Skill `templates/` | **Out of sync with project** | Sync, designate authoritative |
| `styles/book.css` | Authoritative; possibly has dead rules | Audit for unused CSS pre-ship |
| Skill `styles/book.css` | **1,400 lines stale** | Sync from project |
| `agents/book-skills/agent-shared.css` | **Possibly unused** | Investigate, retire if dead |

The single biggest win available right now is the **"Run NOW" agent batch**
(Fact Integrity + Figure Fact Checker + Content Update Scout + Research
Scientist + Aha-Moment + Memorability + Illustrator + Lab Designer) **applied
specifically to the 7 new chapters identified in the hallucination audit.**
