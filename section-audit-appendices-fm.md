# Section Audit: Appendices A-T and Front Matter

**Date:** 2026-05-16
**Scope:** 20 appendix directories (A-T) with all `index.html` + `section-X.M.html` files, plus 7 front-matter files in `front-matter/`.
**Mode:** Read-only. No files modified.
**Format reference:** Same five quality dimensions as the Parts 1-3 audit (uniform format, working links, section naming, captions, styles).

## Headline finding

The appendices are structurally close to the canonical format but suffer from **stale-letter drift** in two appendix directories (L, M) that were renumbered after content was authored, plus several **format-inconsistency clusters** in title suffixes, callout palette, index layout, and front-matter stale references. Front matter is internally consistent in format but contains several stale references to the dropped Problem-Solution Key (former Appendix G) and to a 21-appendix layout that no longer exists.

| Dimension              | Status  | Critical issues | Total issues |
| ---------------------- | ------- | --------------: | -----------: |
| Uniform format         | Mixed   |               6 |           14 |
| Working links          | Broken  |               7 |           ~75 broken hrefs (mostly P, Q, FM) |
| Section naming         | Mixed   |               5 |           ~30 (L, M, A.6, captions) |
| Captions               | Mixed   |               1 |           66 wrong-letter Code Fragment IDs |
| Styles / callouts      | Mixed   |               2 |           16 (non-standard classes + missing assets) |

## Per-dimension findings

### 1. Uniform format

**1a. Title-tag suffix inconsistency.** 26 of 69 section files lack the `| Building Conversational AI with LLMs and Agents` suffix; 43 have it. The split is appendix-by-appendix, not random:

- **Without suffix (26 files):** appendices A (6 sections), B (4), G (4), H (8), I (4).
- **With suffix (43 files):** appendices C, D, E, F, J, K, L, M, N, O.

Both styles validate as HTML, but Pagefind / search result formatting expects the long form. **Action:** standardize on the long form `Section X.M: Title | Building Conversational AI with LLMs and Agents` for all 69 section files.

**1b. Appendix index title-tag suffix.** Same split for appendix index pages:

- **Without suffix (5 indices):** A, B, G, H, I.
- **With suffix (15 indices):** C, D, E, F, J, K, L, M, N, O, P, Q, R, S, T.

Additionally, **appendix N's index title is wrong**: `<title>Appendix P: MLOps | …</title>` should be `Appendix N: MLOps`.

**1c. Appendix D title-tag short form.** `appendix-d-langchain/index.html` title says `Appendix D: LangChain` but the h1 + parent-index-card use the long form `LangChain: Chains, Agents, and Retrieval`. Minor; recommend matching the long form in the title.

**1d. Appendix G display-name drift (3 variants).**

- File path: `appendix-g-python-for-llm/`
- `<title>`: `Appendix G: Python for Working with LLMs`
- `<h1>`: `Python Libraries and Patterns for LLM Development`
- Parent index card: `Python Libraries and Patterns for LLM Development`
- Appendices/index.html subtitle text mentions "the problem-solution key for navigating the book by task" (treats G as the dropped P-S Key).

Three different names + stale parent text. Pick one canonical title and propagate.

**1e. Pagefind `part` meta value inconsistency.** Two values in use:

- `data-pagefind-meta="part:Building Conversational AI with LLMs and Agents"` (in indices A, B, C, D, E, G, H, I, J, K, O - that is 11 of 20).
- `data-pagefind-meta="part:Appendices"` (in indices F, L, M, N, P, Q, R, S, T - that is 9 of 20).

Search facets / breadcrumb decoration will group inconsistently. Standardize on one (recommend `Appendices`).

**1f. Appendix-index layout: three different patterns in use.** Class for the section list varies:

- `<ul class="sections-list">` style: A, B, C, D, E, G, H, I, J, K, O (11 indices).
- `<div class="section-card-list">` style: F, L, M, N (4 indices).
- No section list at all (lookup-only): P, Q, R, S, T (5 indices).

The `library-shortcut` callout block and the `<div class="whats-next">` block are present only in F, L, M, N (the "section-card-list" cluster). Other indices lack these. Pick one canonical structure (recommend the F/L/M/N variant — library-shortcut + section-card-list + whats-next — applied to A-O; P-T can keep lookup style but should still have library-shortcut where relevant).

**1g. Appendix A orphan section in `section-grid`.** `appendix-a-mathematical-foundations/index.html` lists A.1-A.5 inside `<ul class="sections-list">`, then drops A.6 into a separate `<div class="section-grid">` block. A.6 ("Information Theory for Language Models") visually duplicates A.4 ("Information Theory"). Either merge A.6 into A.4 or fold A.6 into the same list.

**1h. Front-matter `<a href="index.html">Front Matter</a>` link targets a non-existent file.** All 7 front-matter pages have this link inside `<div class="part-label">`; `front-matter/index.html` does not exist. The link silently 404s. Either create `front-matter/index.html` or change the href to `../toc.html` (or to one of the FM pages).

**1i. Footer separator encoding.** 77 files use the literal `·` (U+00B7 middle dot); 20 files use the `&middot;` HTML entity. Renders identically; minor encoding mix only. Not a functional issue.

### 2. Working links

Found **132 broken `href` targets** across appendices + FM, concentrated in three buckets:

**2a. Real broken module/part names (truly broken, content fixes):**

| File | Broken href | Likely target |
| --- | --- | --- |
| `appendices/appendix-d-langchain/section-d.2.html` | `../../part-5-retrieval-conversation/module-24-context-management/index.html` | `module-24-conversational-ai/` |
| `appendices/appendix-e-orchestration-frameworks/section-e.2.html` | `../../part-5-retrieval-conversation/module-24-vector-databases/index.html` | `module-22-embeddings-vector-db/` |
| `appendices/appendix-h-environment-setup/section-h.6.html` | `../../part-9-llm-applications/module-50-coding-with-llms/index.html` (2x) | `part-10-idea-to-product/module-43-vibe-coding/` or `module-50-tools-of-the-trade/` |
| `appendices/appendix-m-distributed-ml/index.html` | `../../part-2-understanding-llms/module-07-pretraining/index.html` | `module-07-pretraining-scaling-laws/` |

**2b. Wrong-relative-depth links in P and Q (`../X` vs `../../X`):** Both `appendix-p-course-syllabi/index.html` and `appendix-q-reading-pathways/index.html` use `../part-N-…/…` (resolves to `appendices/part-N-…`, which does not exist) instead of `../../part-N-…/…`. Same problem with `../toc.html` (should be `../../toc.html`) and with the self-referential `../appendices/appendix-X/…` (should be just `appendix-X/…` or `../appendix-X/…`).

- **Appendix P:** ~46 broken hrefs of this kind, plus one double-`appendices/` typo at line 229: `appendices/appendices/appendix-q-reading-pathways/index.html`.
- **Appendix Q:** ~35 broken hrefs of the same kind.

These two files dominate the broken-link count. A scripted relative-path fix would resolve nearly all of them in one pass.

**2c. Front-matter "Front Matter" label link.** As noted in 1h above, all 7 FM pages link `index.html` (in `front-matter/`) that does not exist. 7 broken hrefs.

**2d. Stale `Problem-Solution Key` references (functionally dead links, content drift).**

| File | Stale text | Action |
| --- | --- | --- |
| `appendices/index.html` line 30 | "…agent frameworks, and the problem-solution key for navigating the book by task." | Remove or rewrite Framework Guides description. |
| `appendices/appendix-p-course-syllabi/index.html` line 227 | "Appendix G (Problem-Solution Key) for worked-through fixes to common end-of-chapter problems." | Drop bullet or replace with current Appendix G title. |
| `front-matter/fm-how-to-use.html` line 43 | "Appendix G: Problem-Solution Key is a lookup table…" | Rewrite or remove the entire "4. Reference (When Something Breaks)" callout. |
| `front-matter/fm-what-this-book-covers.html` line 52 | "Twenty-One Reference Appendices… G: Problem-Solution Key… U: War Stories" | Rewrite to "Twenty Reference Appendices", reletter G…T per v11. |

### 3. Section naming (filenames vs in-file labels)

**3a. Title-element section identifier mismatches (5 files).** The on-disk filename gives an identifier (e.g., `section-l.3.html` -> L.3), but the `<title>` tag claims a different one:

| File | `<title>` says | Should be |
| --- | --- | --- |
| `appendices/appendix-l-data-engineering/section-l.3.html` | `Section L.6: Feature Stores…` | `Section L.3: …` |
| `appendices/appendix-l-data-engineering/section-l.4.html` | `Section L.7: Production Data Pipelines…` | `Section L.4: …` |
| `appendices/appendix-m-distributed-ml/section-m.2.html` | `Section L.3: Databricks: Workspace…` | `Section M.2: …` |
| `appendices/appendix-m-distributed-ml/section-m.3.html` | `Section L.4: Databricks AI and Foundation Models` | `Section M.3: …` |
| `appendices/appendix-m-distributed-ml/section-m.4.html` | `Section L.5: Ray Train, Ray Serve, and Ray Data` | `Section M.4: …` |

Same drift propagates to `<div class="page-current">` blocks and `<meta name="description">`. Title-text content (e.g., "Feature Stores: Feast, Tecton, and Databricks Feature Engineering") is correct; only the numbering is stale.

**3b. Stale section-number prefixes in body `<h2>`/`<h3>` headings (6 files).** Heading text uses the **prior** appendix letter as a prefix:

| File | Heading prefix used | Should be |
| --- | --- | --- |
| `appendix-l-data-engineering/section-l.3.html` | `O.6.1`, `O.6.2`, … | `L.3.1`, `L.3.2`, … |
| `appendix-l-data-engineering/section-l.4.html` | `O.7.1`, `O.7.2`, … | `L.4.1`, … |
| `appendix-m-distributed-ml/section-m.2.html` | `O.3.1`, `O.3.2`, … | `M.2.1`, … |
| `appendix-m-distributed-ml/section-m.3.html` | `O.4.1`, `O.4.2`, … | `M.3.1`, … |
| `appendix-m-distributed-ml/section-m.4.html` | `O.5.1`, `O.5.2`, … | `M.4.1`, … |
| `appendix-a-mathematical-foundations/section-a.6.html` | `4.1.2.x` (Chapter 4!) | `A.6.x` |

Sections L.3, L.4, M.2-M.4 are clearly an old "Appendix O" body that was moved into the L/M slots without a renumbering pass. A.6 has Chapter 4 heading IDs (a copy from Chapter 4 content that was never relabeled).

**3c. Index → section transition labels are correct.** All `chapter-nav` prev/next links resolve to existing files (0 broken nav targets). `<a class="next">` nav-num matches the href in 100% of section files. Only the title/header text is stale (above).

**3d. Cross-section content references inside index files mention wrong letters.** Found in:

- `appendix-l-data-engineering/index.html`: "When to read this" tip says "Read sections **M.1 and M.2** when…" - should be **L.1 and L.2**.
- `appendix-m-distributed-ml/index.html`: "Picking the right parallelism" tip says "The **N.1** decision table lays out…" - should be **M.1**.
- `appendix-m-distributed-ml/index.html`: "What Comes Next" lists "appendices L (Inference), M (Data), N (this one), O (MLOps), P (Docker)" - all letters off by one (current layout is K=Inference, L=Data, M=Distributed ML (this one), N=MLOps, O=Docker).
- `appendix-l-data-engineering/index.html`: closing line "Appendix L is the upstream substrate; N is the training engine; O is the production lifecycle." - stale (M is training, N is operations).

### 4. Captions

**4a. Figure captions.** 50 total figure captions across appendices + FM; **only 1 wrong-letter**:

- `appendix-m-distributed-ml/section-m.3.html`: `Figure L.4.1` -> should be `Figure M.3.1`.

All other figcaptions are properly numbered.

**4b. Code Fragment captions.** 242 total captions; **66 have wrong-letter or wrong-case identifiers** (27% of all code captions):

| File / cluster | Pattern observed | Should be |
| --- | --- | --- |
| `appendix-a/section-a.6.html` (1 caption) | `Code Fragment 4.1.1:` | `Code Fragment A.6.1:` |
| `appendix-b/section-b.4.html` (2 of 4 captions) | `Code Fragment b.4.1:` (lowercase) | `Code Fragment B.4.1:` |
| `appendix-c/section-c.{1..5}.html` (38 captions across 5 files) | `Code Fragment k.1.1:` (uses letter `k`) | `Code Fragment C.1.1:` |
| `appendix-g/section-g.{1,2,4}.html` (6 captions across 3 files) | `Code Fragment c.1.5:` (uses letter `c`) | `Code Fragment G.1.5:` |
| `appendix-m/section-m.{2,3,4}.html` (21 captions across 3 files) | `Code Fragment L.3.1:` (uses letter `L`) | `Code Fragment M.2.1:` etc. |

Total: 66 captions to fix. All five clusters are clear stale-letter holdovers from prior appendix layouts (`k` for old HuggingFace at appendix K; `c` for old Python at appendix C; `L` for the old data-engineering pre-split; `4` for material formerly inside Chapter 4).

**4c. Table captions.** 0 `<div class="table-caption">` blocks found in any appendix or FM file. (No issues to flag - either tables in these files are uncaptioned, which may be by design, or all caption-worthy tables use a different markup.)

### 5. Styles / callouts (palette adherence + asset consistency)

**5a. Non-standard callout classes (16 instances).** The standard palette (`big-picture`, `key-insight`, `note`, `tip`, `warning`, `exercise`, `fun-note`, `practical-example`, `research-frontier`, `self-check`, `library-shortcut`, `looking-back`, `cross-ref`, `algorithm`, `production-pattern`, `postmortem`, `numeric-example`, `thesis-thread`) does not include `key-takeaway` or `pathway`. Found:

| Class | Count | Files |
| --- | --- | --- |
| `callout key-takeaway` | 12 | `appendix-e/section-e.2.html`, `appendix-e/section-e.3.html`, `appendix-f/section-f.2.html`, `appendix-f/section-f.3.html`, `appendix-h/section-h.6.html`, `appendix-h/section-h.7.html`, `appendix-m/section-m.1.html`, `appendix-n/section-n.{1..5}.html` |
| `callout pathway` | 4 | `front-matter/fm-how-to-use.html` (all 4 instances) |

**Action:** map `key-takeaway` -> `key-insight` (closest standard equivalent) and `pathway` -> `tip` or `practical-example`. CSS for these classes may render fine, but they are off-palette per the audit spec.

**5b. Missing `book.js` script include (3 files).** Standard head includes `<script defer src="../../scripts/book.js"></script>`; missing in:

- `appendices/appendix-a-mathematical-foundations/section-a.6.html`
- `appendices/appendix-p-course-syllabi/index.html`
- `appendices/appendix-q-reading-pathways/index.html`

**5c. Missing hero / chapter-opener illustration in 5 appendix indices.**

| Appendix | Has `<figure class="illustration">` | `images/chapter-opener.*` on disk |
| --- | :---: | :---: |
| F (Agent Frameworks) | No | Has `diagram-framework-selection.{png,svg}` but no opener |
| L (Data Engineering) | No | `chapter-opener.png` exists, unused |
| M (Distributed ML) | No | No images at all |
| N (MLOps) | No | No images at all |

A-E, G-K, O, P-T all have a chapter opener. F/L/M/N indices are missing illustrations; M and N also lack the underlying PNG. **Action:** generate or move chapter openers for F/L/M/N, or remove the unused L `chapter-opener.png`.

**5d. `figure` class compound: `illustration chapter-opener`.** Appendices P, Q, R, S, T use `<figure class="illustration chapter-opener">` (compound class); A-K and O use `<figure class="illustration">` (single class). Functionally equivalent (CSS likely matches `illustration` selector), but inconsistent. Pick one.

## Per-appendix risk summary

| Apx | Format | Links | Section IDs | Captions | Style | Notes / Effort |
| --- | :----: | :---: | :---------: | :------: | :---: | --------------------------------------------- |
| A   |   M    |   ok  |     M (A.6) |  M (1)   |   ok  | 4.x heading IDs + grid-orphan A.6; ~1 h |
| B   |   M    |   ok  |          ok |  M (2)   |   ok  | lowercase `b.4.x` captions; ~15 min |
| C   |   M    |   ok  |          ok |  M (38)  |   ok  | `k.x.y` captions across all 5 files; ~30 min |
| D   |   M    |   1   |          ok |    ok    |   ok  | title-tag short form + 1 broken module ref |
| E   |   M    |   1   |          ok |    ok    | 2 nonstd | 1 broken module ref; 2 key-takeaway |
| F   |   M    |   ok  |          ok |    ok    | 2 nonstd, no img | 2 key-takeaway; no hero image |
| G   |   M    |   ok  |          ok |  M (6)   |   ok  | `c.x.y` captions; title-name drift |
| H   |   M    |   1   |          ok |    ok    | 2 nonstd | 2 broken refs (same); 2 key-takeaway |
| I   |   M    |   ok  |          ok |    ok    |   ok  | title suffix missing only |
| J   |   ok   |   ok  |          ok |    ok    |   ok  | clean |
| K   |   ok   |   ok  |          ok |    ok    |   ok  | clean |
| L   |   M    |   ok  |   M (L.3, L.4) |  ok    |   ok  | O.6/O.7 prefixes in L.3/L.4 body + stale tip text |
| M   |   M    |   1   |  M (M.2-M.4, fig)|  M (21)|   1 nonstd | wrong N index title; M.x are old "O" content |
| N   |   M    |   ok  |          ok |    ok    | 5 nonstd | wrong title "Appendix P"; 5 key-takeaway |
| O   |   ok   |   ok  |          ok |    ok    |   ok  | clean |
| P   |   M    |  ~50  |          ok |    ok    | no book.js | massive relative-path fix needed; P-S Key ref |
| Q   |   M    |  ~35  |          ok |    ok    | no book.js | massive relative-path fix needed |
| R   |   M    |   ok  |          ok |    ok    | no bp callout | lookup-style; missing big-picture |
| S   |   M    |   ok  |          ok |    ok    | no bp callout | lookup-style; missing big-picture |
| T   |   M    |   ok  |          ok |    ok    | no bp callout | lookup-style; missing big-picture |

Legend: ok = clean; M = mixed / needs work; numbers = specific count.

## Front-matter findings (recap)

| File | Title format | Stale refs | Other |
| --- | :---: | :---: | --- |
| `foreword.html` | ok | ok | uses `<div class="part-label">` style; index.html target missing |
| `look-inside-preview.html` | ok | ok | same; index.html target missing |
| `fm-what-this-book-covers.html` | ok | "Twenty-One Reference Appendices" + G..U lettering + G: Problem-Solution Key | needs full rewrite of paragraph at line 52 |
| `fm-who-should-read.html` | ok | ok | index.html target missing |
| `fm-how-to-use.html` | ok | "Appendix G: Problem-Solution Key" callout | 4x non-standard `pathway` callout class; index.html missing |
| `about-authors.html` | ok | ok | index.html target missing |
| `copyright.html` | ok | ok | index.html target missing |

All 7 front-matter files share the same head/footer/script structure and use the `<div class="part-label">` pattern (consistent). The main content issues are (a) the missing `front-matter/index.html`, (b) the stale Problem-Solution Key reference in fm-how-to-use and fm-what-this-book-covers, and (c) the non-standard `pathway` callout class in fm-how-to-use.

## Key cross-cutting risks

1. **The L / M number-drift cluster is the largest single defect.** Five section files (L.3, L.4, M.2, M.3, M.4) carry title, page-current, h2/h3 prefixes, and Code Fragment captions from a prior "Appendix O" layout. The structural and body content is otherwise correct. A single search-and-replace per file (`O.x.y` -> `L.x.y` or `M.x.y`; `Section O.x` -> `Section L.x` or `M.x`; `Code Fragment L.x.y` -> `Code Fragment M.x.y`) plus a one-line title fix would resolve all five files.

2. **The P / Q relative-path cluster is the largest broken-link defect.** ~80 of ~132 broken hrefs come from these two index pages using `../part-N` and `../appendices/appendix-X` where they should use `../../part-N` and `../appendix-X` (or just `appendix-X`). Mechanical fix.

3. **Stale Problem-Solution Key references will confuse new readers.** Three high-visibility pages (`appendices/index.html`, `fm-how-to-use.html`, `fm-what-this-book-covers.html`) still describe Appendix G as the Problem-Solution Key. v11 dropped that appendix and re-purposed G to Python Libraries and Patterns. Rewrite needed in three places.

4. **Title-suffix split (with vs without `| Building Conversational AI…`) is appendix-block-correlated.** A, B, G, H, I lack the suffix; everyone else has it. Whichever block was authored first or last differed from the other. Standardize.

5. **Callout palette has two non-standard names in circulation (`key-takeaway`, `pathway`).** 16 instances total. Map to standard equivalents.

6. **Appendix N's index `<title>` says "Appendix P".** A one-line fix, but high-visibility (tab title, search results).

7. **Missing chapter-opener images for F, L, M, N indices.** Visual gap when the rest of the appendices have them. Either generate openers or remove the partial L image.

## Recommended execution order

1. **Mechanical fixes first** (1-2 h total, mostly find-and-replace):
   - Fix N's index title (`Appendix P` -> `Appendix N`).
   - Standardize 26 + 5 section / index titles missing the ` | Building Conversational AI…` suffix.
   - Standardize pagefind `part:` meta value (`Appendices`) across all 20 indices.
   - Strip / encode footer separator consistently (pick `·` or `&middot;`).
   - Map non-standard callouts: `key-takeaway` -> `key-insight`; `pathway` -> `tip`.

2. **L/M number-drift cleanup** (2 h):
   - For each of L.3, L.4, M.2-M.4, rewrite title, page-current, h2/h3 prefixes, and Code Fragment captions to the current letter.
   - Fix the one stray `Figure L.4.1` -> `Figure M.3.1` in section-m.3.html.

3. **P / Q broken-link sweep** (1 h, scripted):
   - Replace `../part-` with `../../part-` and `../toc.html` with `../../toc.html` in `appendix-p-course-syllabi/index.html` and `appendix-q-reading-pathways/index.html`.
   - Fix double-`appendices/` typo in P line 229.

4. **Stale Problem-Solution Key content** (1-2 h, prose rewrite):
   - Rewrite `appendices/index.html` Part Overview paragraph (drop P-S Key reference).
   - Rewrite `fm-what-this-book-covers.html` "Twenty-One Reference Appendices" paragraph (currently shows G..U; should be G..T, and G is Python Libraries, not P-S Key).
   - Rewrite `fm-how-to-use.html` "4. Reference (When Something Breaks)" callout (currently describes the dropped P-S Key).
   - Remove the duplicate G bullet from `appendix-p-course-syllabi/index.html` line 227.

5. **Other broken module references** (30 min):
   - Fix the 4 wrong-module-slug hrefs in D.2, E.2, H.6 (2x), M-index.

6. **Caption-letter sweep across A.6, B.4, C.x, G.x, M.x** (30 min, scripted):
   - 66 Code Fragment captions to update.

7. **Front-matter index.html decision** (15 min):
   - Either create `front-matter/index.html` (front-matter cover page) or rewrite the 7 part-label hrefs to point at `../toc.html`.

8. **Appendix-index layout standardization** (2-3 h, design + apply):
   - Decide whether A-K + O should adopt the F/L/M/N style (library-shortcut + section-card-list + whats-next) or vice versa, then apply.
   - Add `big-picture` callouts to R, S, T (currently absent).
   - Add chapter-opener illustrations to F, L, M, N indices (or generate the underlying images for M, N).
   - Fold A.6 back into the A index sections-list (or merge into A.4 if duplicative).

**Total estimated authoring effort:** ~10-12 hours (mostly mechanical edits; one prose rewrite cluster for the Problem-Solution Key references; one design decision for the index-layout standardization).
