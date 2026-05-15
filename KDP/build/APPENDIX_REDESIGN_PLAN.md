# Appendix Redesign Plan

Plan-only document. No file system changes are applied here. The
companion script `_audit_appendices_full.py` (also in this directory)
regenerates the underlying inventory data
(`AUDIT_appendices_full.md`, `AUDIT_appendices_full.json`) at any time.

## Phase 1: Audit

### 1.1 Inventory summary

24 appendices exist on disk after the v14.5 / Part XII migration:

```
A  B  C  D  E         (Foundations and Setup,         5 sectioned)
F  G  H  I  J         (Reference Materials,           5 sectioned)
K  L                  (Framework Guides,              2 sectioned)
R  S  T  U  V         (Infrastructure and Ecosystem,  5 sectioned)
AD AE AF AG           (Cross-Cutting Catalogs,        4 single-page)
AI                    (Freshness Index,               1 single-page)
AJ AK                 (Course Materials,              2 single-page)
```

Totals: 17 sectioned appendices, 7 single-page reference catalogs,
24 in all. Combined size approximately 2.27 MB HTML, 116k words.

Largest: Appendix T (Distributed ML), 17,069 words, 7 sections,
340 KB. Smallest: Appendix AI (Freshness Index), 1,155 words, single page.

### 1.2 Gap confirmation

Brief confirmed exactly. The current letter sequence is:

```
A B C D E F G H I J K L _ _ _ _ _ R S T U V _ _ _ _ _ _ _ AD AE AF AG _ AI AJ AK
                       M N O P Q                W X Y Z AA AB AC      AH
```

- `M-Q`: merged into Appendix L during v14.x consolidation.
- `W-AC`: moved to Part XII in v14.5 (industry-specific guides).
- `AH`: conceptual map, dropped in v14.5.

These are five distinct, non-trivial gaps in the consumer-visible labeling.

### 1.3 Top redundancies identified

The topic-keyword scan confirms several overlap candidates. The five
most actionable redundancies, in priority order:

1. **AD (Master Reference Tables) overlaps with H, J, AG.**
   Tables T5 (Model Provider Comparison) is essentially a compact H;
   T14 (Benchmark Saturation) overlaps J; T1-T15 is a "scannable
   decision card" that AG (Problem-Solution Key) duplicates from a
   different angle. AD is 33 KB, 15 tables, only 8 inbound refs.
   Decision: keep AD as a thin index that links into H, J, and the
   primary source chapters, rather than duplicating the table content.

2. **AE (Production Patterns) is the secondary home of content that
   already lives in module-29 (Production Engineering) and modules
   18, 19, 21, 24, 27, 28, 30, 34.** AE is referenced 20 times
   (mostly from itself and the index), with only 9 references from
   actual body chapters. The page is high-value but reads like a
   25-page chapter; it would be a more honest fit either as a true
   appendix sized to the others or as a "patterns sidebar" inside
   each module-29 section. Decision: keep AE; rename to "Production
   Reliability Patterns" to clarify that it is operationally focused;
   keep as single-page so it can be printed as a wall poster.

3. **V (LLM Tooling Ecosystem) substantially overlaps K, L, R, S.**
   Topic-keyword: V has langchain hits=57, huggingface hits=6,
   serving hits=23, tracking hits=2, model_cards hits=46. V is 95 KB
   across 3 sections; only 7 inbound refs total. Decision: V is the
   weakest "framework" appendix and the most redundant. Recommend
   demoting it to a single-page "Ecosystem Map" (table of named
   tools with one-line descriptions and chapter pointers), retiring
   the 95 KB of prose, and folding the long-form content into K,
   L, R, S where appropriate.

4. **C (Python for LLM) and D (Environment Setup) overlap heavily.**
   C has langchain=10, tracking=13, serving=1, huggingface=8;
   D has langchain=8, tracking=12, serving=19, huggingface=4. The
   two read like one appendix split arbitrarily. C is 80 KB / 4 sec;
   D is 57 KB / 6 sec. Decision: keep as two appendices but rebalance,
   migrate hands-on cloud/Conda content from C into D, leave C focused
   on libraries and patterns. (Lower priority than 1-3 above.)

5. **AJ (Reading Pathways) and AK (Course Syllabi) overlap each
   other and the front-matter `fm-how-to-use` page.** AJ has 8 goal
   based routes; AK has 5 course syllabi. fm-how-to-use already cites
   both. AJ outbound = 60, AK outbound = 94, both modest. Decision:
   keep both, but RELOCATE both to front-matter (right after
   `fm-how-to-use.html`). They are reading-orientation pages, not
   reference content. This eliminates the AJ/AK appendix slots and
   removes a navigational anomaly (the only appendices a reader visits
   *before* starting the book).

(Other overlaps detected but lower-priority: B<->A on math foundations,
H<->S on model context windows, T<->R on tracking, K<->AG on
huggingface patterns. None justify a structural change.)

### 1.4 Single-page appendix substance check

| Appendix | Words | Tables | Status                                             |
| -------- | -----:| ------:| -------------------------------------------------- |
| AD       | 2,317 | 15     | SUBSTANTIAL: 15 comparison tables. Keep.           |
| AE       | 1,771 | 0      | SUBSTANTIAL: 22 named production patterns. Keep.   |
| AF       | 2,023 | 1      | SUBSTANTIAL: rubric + projects + war stories. Keep. |
| AG       | 1,933 | 11     | SUBSTANTIAL: 11 problem-to-chapter lookup tables. Keep. |
| AI       | 1,155 | 2      | LIGHT: 2024-2026 citation list. Keep but small.    |
| AJ       | 1,632 | 0      | SUBSTANTIAL: 8 reading routes. Move to front-matter. |
| AK       | 1,909 | 8      | SUBSTANTIAL: 5 syllabi with full module schedules. Move to front-matter. |

All seven are non-stub. AI is the lightest and could be merged with
the back-of-book bibliography, but it stands on its own as a
"what's new in 2026" snapshot. Recommendation: keep AI as-is.

### 1.5 AJ and AK as front-matter

Yes. Reading-pathway content is consumed BEFORE the book is read, not
during reference. Their natural location is the front matter, next to
`fm-how-to-use.html`. `fm-how-to-use` already references AJ and AK
four times, so the dependency is correct but the placement is inverted.
Moving them eliminates two appendix slots (AJ, AK) and one structural
weirdness.

## Phase 2: Proposed redesign

### 2.1 Recommended numbering scheme

A contiguous A-T scheme that groups by purpose:

```
Foundations and Setup                    A  Mathematical Foundations   (was A,  6 sec)
                                         B  Machine Learning Essentials (was B,  4 sec)
                                         C  Python Libraries and Patterns (was C,  4 sec)
                                         D  Development Environment Setup (was D,  6 sec)
                                         E  Git, DVC, and Reproducibility (was E,  4 sec)
Reference Materials                      F  Glossary                    (was F,  5 sec)
                                         G  GPU Hardware and Compute    (was G,  5 sec)
                                         H  Model Cards and Selection   (was H,  3 sec)
                                         I  Prompt Template Catalog     (was I,  8 sec)
                                         J  Datasets and Benchmarks     (was J,  5 sec)
Framework Guides                         K  HuggingFace Ecosystem       (was K,  5 sec)
                                         L  LangChain and LangGraph     (was L,  5 sec)
Infrastructure and MLOps                 M  Experiment Tracking         (was R,  5 sec)
                                         N  Inference Serving           (was S,  5 sec)
                                         O  Distributed ML              (was T,  7 sec)
                                         P  Docker and Containers       (was U,  4 sec)
                                         Q  LLM Tooling Ecosystem Map   (was V,  3 sec -> single-page)
Cross-Cutting Catalogs                   R  Master Reference Tables     (was AD, single)
                                         S  Production Reliability Patterns (was AE, single)
                                         T  Pedagogy Kit                (was AF, single)
                                         U  Problem-Solution Key        (was AG, single)
                                         V  2026 Freshness Index        (was AI, single)
(moved to front-matter)                  -- Reading Pathways            (was AJ -> front-matter)
                                         -- Course Syllabi              (was AK -> front-matter)
```

Final count: 22 appendices, A through V, contiguous, plus two pages
relocated to front-matter. The gap from L to R closes; the gap from V
to AD closes; the gap from AG to AI closes. No skipped letters.

Why this scheme rather than the brief's suggested R=AD, S=AE etc.?
Same content placement, but it uses every letter A-V instead of leaving
a discontinuity at W and ending at X. It also signals (via grouping
boundaries that align with the chapter cards in `appendices/index.html`)
which appendices are "deep dives" vs "cross-cutting catalogs."

### 2.2 What gets merged, moved, demoted, deleted

| Action  | From                                            | To                                                    | Reason |
| ------- | ----------------------------------------------- | ----------------------------------------------------- | ------ |
| Renumber| `appendix-r-experiment-tracking/`               | `appendix-m-experiment-tracking/`                     | Close L->R gap |
| Renumber| `appendix-s-inference-serving/`                 | `appendix-n-inference-serving/`                       | "" |
| Renumber| `appendix-t-distributed-ml/`                    | `appendix-o-distributed-ml/`                          | "" |
| Renumber| `appendix-u-docker-containers/`                 | `appendix-p-docker-containers/`                       | "" |
| Demote +renumber | `appendix-v-tooling-ecosystem/`        | `appendix-q-tooling-map/` (1 page, table only)         | Massive overlap with K, L, R, S |
| Renumber| `appendix-ad-master-reference-tables/`          | `appendix-r-master-reference-tables/`                 | Close V->AD gap |
| Renumber| `appendix-ae-production-patterns/`              | `appendix-s-production-patterns/`                     | "" |
| Renumber| `appendix-af-pedagogy-kit/`                     | `appendix-t-pedagogy-kit/`                            | "" |
| Renumber| `appendix-ag-problem-solution-key/`             | `appendix-u-problem-solution-key/`                    | "" |
| Renumber| `appendix-ai-freshness-2026/`                   | `appendix-v-freshness-2026/`                          | Close AG->AI gap |
| Move    | `appendix-aj-reading-pathways/`                 | `front-matter/fm-reading-pathways.html`               | Pre-read content |
| Move    | `appendix-ak-course-syllabi/`                   | `front-matter/fm-course-syllabi.html`                 | Pre-read content |

No outright deletions. Nothing is lost. The Tooling Ecosystem demotion
turns 3 sections into one page-table; the original content's most
unique paragraphs migrate as bullets to K, L, R (M after rename), S
(N after rename) where each tool is most at home.

### 2.3 Keep as standalone (no change beyond letter)

A, B, C, D, E, F, G, H, I, J, K, L stay where they are. Only their
"next" navigation link changes if L's neighbor changes letter.

## Phase 3: Edit plan

### 3.1 File system changes

For each renumber, three operations:

1. `mv appendices/appendix-<old>-<slug>/` -> `appendices/appendix-<new>-<slug>/`
2. Inside the renamed directory, rename every `section-<old>.<n>.html`
   to `section-<new>.<n>.html`. Image references inside images/ do
   not need to change.
3. Update each renamed file's `<head>`, `chapter-label`, `part-label`,
   `<h1>`, and footer to use the new letter.

For AJ/AK move to front-matter:

1. `cp appendices/appendix-aj-reading-pathways/index.html` to
   `front-matter/fm-reading-pathways.html`, fix all `../` paths
   (currently `../..`) to single-level `../`.
2. Same for AK as `front-matter/fm-course-syllabi.html`.
3. Replace appendix-style header (`Appendix AJ:` / `part-label =
   Appendices`) with front-matter style (`part-label = Front Matter`,
   no Appendix prefix in h1).
4. Delete the original appendix-aj/ and appendix-ak/ directories.

For V demotion to single-page Tooling Map:

1. Author a new `appendix-q-tooling-map/index.html` with one table:
   tool name | category | one-line description | source chapter or
   appendix link.
2. Migrate any unique long-form prose from V's section-v.1, v.2, v.3
   into the relevant K/L/M/N appendices (one or two paragraphs each).
3. Delete the old `appendix-v-tooling-ecosystem/` directory.

### 3.2 TOC updates required

`toc.html` references the appendices 66 times. Every reference to
`appendix-r-`, `appendix-s-`, `appendix-t-`, `appendix-u-`, `appendix-v-`,
`appendix-ad-`, `appendix-ae-`, `appendix-af-`, `appendix-ag-`,
`appendix-ai-`, `appendix-aj-`, `appendix-ak-` needs to be updated to
the new letter (or removed for AJ/AK in favor of front-matter links).

Estimated TOC edits: approximately 40 hrefs (per-appendix sub-link)
plus ~24 visible labels (e.g., "Appendix R: ..." -> "Appendix M: ...").

### 3.3 Appendix-index.html (`appendices/index.html`) updates

The Appendices landing page needs to be rewritten so the chapter-cards
appear in the new letter order. It also needs to:

- Drop the "Course Materials" section heading (its content moves to
  front-matter); the AJ and AK chapter-cards are deleted.
- Drop the "Industry-Specific Practitioner Guides" empty section
  heading that v14.5 left behind (lines 202-209 in current file).
- Adjust the "Cross-Cutting Reference Catalogs" section heading to
  list R-V instead of AD-AI.
- Change the section-overview paragraph that today says "Appendices A-V
  are reference material..." to the new structure.

### 3.4 Cross-reference updates required

Outbound from `part-1` through `part-12` modules: based on the inbound
scan above, the affected referrers are:

| Old reference                          | Count | Locations |
| -------------------------------------- | -----:| --------- |
| `appendix-r-experiment-tracking`       |     ? | (see below) |
| `appendix-s-inference-serving`         |    10 | part-1, 2, 3, 4, 5, 6, 8, 9 modules |
| `appendix-t-distributed-ml`            |     1 | one module references |
| `appendix-u-docker-containers`         |     0 | none |
| `appendix-v-tooling-ecosystem`         |     0 | none (in body parts) |
| `appendix-ad-master-reference-tables`  |     1 | one module |
| `appendix-ae-production-patterns`      |     9 | part-3, 5, 6, 8 |
| `appendix-af-pedagogy-kit`             |     1 | one module |
| `appendix-ag-problem-solution-key`     |     0 | none |
| `appendix-ai-freshness-2026`           |     1 | one module |
| `appendix-aj-reading-pathways`         |     0 | (only front-matter links) |
| `appendix-ak-course-syllabi`           |     0 | (only front-matter links) |

Plus inter-appendix references: many appendices link to each other
(see `outbound_refs` in `AUDIT_appendices_full.json`). Notable:

- Appendix S (Inference Serving) links into appendix-r-* (tracking)
  3 times; needs to become appendix-m-* after rename.
- Appendix T (Distributed ML) links into appendix-s-* (serving) 6
  times; needs to become appendix-n-*.
- Appendix V (Tooling Ecosystem) cites appendix-s, r, k, l; the V demotion
  changes the directionality.
- Appendix AG (Problem-Solution Key) cites appendix-l (33), appendix-k
  (32), appendix-f (30); only the letter labels change in prose.
- Appendix AI (Freshness Index) cites appendix-ag (1), appendix-aj (1).

**Estimated total cross-reference updates**: approximately 320 href
edits and label edits across all HTML, broken down as:

- ~150 inter-appendix hrefs (most are `appendix-r-*`, `appendix-s-*`,
  `appendix-t-*`, `appendix-u-*` from existing appendices)
- ~25 body-chapter hrefs from modules
- ~70 in toc.html, appendices/index.html, front-matter/
- ~50 visible prose mentions ("see Appendix AD" -> "see Appendix R")
- ~25 single-page h1 / chapter-label / page-title prefixes inside the
  renamed appendix files themselves

A scripted find-replace, guarded by an explicit OLD->NEW table, would do
the bulk of this. Manual review for the 50 prose mentions is required.

### 3.5 Navigation chain updates

Every renamed appendix needs its first section.prev and last section.next
adjusted to point at the *new* neighbor letter directories. The pattern
(see `_audit_appendix_chain.py`) is:

```
section-<L>.1.html .prev -> index.html
index.html       .prev -> ../appendix-<L-1>-<slug>/section-<L-1>.<last>.html
index.html       .next -> section-<L>.1.html
section-<L>.<last>.html .next -> ../appendix-<L+1>-<slug>/index.html
```

For 12 renumbered appendices the chain links touch:

- 12 `index.html` files (prev pointer to previous appendix)
- 12 first-section files (no change beyond letter in own name)
- 12 last-section files (next pointer to next appendix)

Approximate edits: 36 navigation rewrites.

### 3.6 Section-file h1 prefix updates

Section files do not currently prefix h1 with the letter (they use
"A.1 Linear Algebra Refresher"). The letter appears in the
`chapter-label`, page-title, and any `.section-number` span. Updates
per renamed appendix:

- `<title>Appendix R: ... | Building Conversational AI ...</title>` ->
  `<title>Appendix M: ... | Building Conversational AI ...</title>`
- `<div class="chapter-label" data-pagefind-meta="chapter">Appendix R</div>`
  -> `<div class="chapter-label" data-pagefind-meta="chapter">Appendix M</div>`
- Section h2 like `R.1 Why Track Experiments` -> `M.1 Why Track Experiments`
- File names: every `section-r.<n>.html` -> `section-m.<n>.html`

A renamed sectioned appendix has roughly 5-7 section files; each one
needs the title, chapter-label, and section-number labels updated.
That is approximately 4 string edits per section file, times approximately 30
section files across the 6 renamed sectioned appendices (R, S, T, U,
plus V demoted) ≈ 120 string edits.

### 3.7 Single-page appendix updates

For AD, AE, AF, AG, AI (all becoming R-V) and V demoted to Q:

- One `<title>` edit
- One `chapter-label` edit
- One `<h1>` edit if it includes the letter prefix
- Inline references to "T1, T2..." stay; they are local table IDs

Approximately 5 string edits per page, 6 pages = 30 edits.

## Phase 4: Priority order

### P0: Must-do (errors of placement that confuse navigation)

- **P0.1** Move AJ (Reading Pathways) to `front-matter/fm-reading-pathways.html`.
  Reading-orientation content does not belong in back matter.
- **P0.2** Move AK (Course Syllabi) to `front-matter/fm-course-syllabi.html`.
  Same reason as P0.1.
- **P0.3** Remove the empty "Industry-Specific Practitioner Guides"
  section heading from `appendices/index.html` (lines 202-209). v14.5
  left a header with no chapter cards under it.

### P1: Should-do (renumbering for consistency)

- **P1.1** Rename `appendix-r-` through `appendix-v-` to fill the
  L-to-R gap: R->M, S->N, T->O, U->P, V->Q (with V also demoted to a
  single-page tooling map).
- **P1.2** Rename `appendix-ad-` through `appendix-ai-` to fill the
  V-to-AD and AG-to-AI gaps: AD->R, AE->S, AF->T, AG->U, AI->V.
- **P1.3** Update `appendices/index.html` to reflect the new order
  and revised group headings.
- **P1.4** Update `toc.html` to the new letters.
- **P1.5** Update all inbound hrefs from body chapters (estimated
  ~25 edits), inter-appendix hrefs (~150), and prose mentions (~50).
- **P1.6** Update each renamed appendix's chapter-nav prev/next chain
  to the new neighbors (~36 nav rewrites).

### P2: Nice-to-have (content quality wins)

- **P2.1** Demote Appendix V (Tooling Ecosystem) from 3-sectioned to
  single-page Tooling Map. The current 95 KB is mostly duplicative of
  K, L, R, S; a one-page table is the right form factor.
- **P2.2** Rebalance Appendix C and Appendix D: move cloud/conda
  hands-on from C into D, leaving C focused on libraries and patterns.
  (Lower priority; current split is not broken, just sub-optimal.)
- **P2.3** Trim Appendix AI (Freshness Index) where references duplicate
  the per-chapter "Further Reading" sections in body modules.
- **P2.4** Add an explicit "Cross-cutting catalogs" note in each
  affected chapter telling readers where the catalog references that
  chapter (R has T1-T15; S has P1-P22; U has 50+ problem entries).
  This makes the catalogs more discoverable.

### Execution sequencing

P0 first (low blast radius, fixes user-facing weirdness).
P1 in a single atomic batch (rename + xref + nav + toc); attempt
within one branch and verify with the existing
`_audit_appendix_chain.py`, `_audit_broken_hrefs.py`, and html2pub
build before merging.
P2 as separate follow-up branches.

Estimated total tooling work: 320 href edits + 36 nav rewrites + 30
single-page label edits + 120 section-label edits + ~25 prose
rewrites + appendix-index reflow ≈ 530 individual edits, almost all
scriptable from a single OLD->NEW table.

---

## Appendix to this plan: Recommended OLD->NEW mapping table

```text
Renumber (no structural change):
  appendix-r-experiment-tracking       -> appendix-m-experiment-tracking
  appendix-s-inference-serving         -> appendix-n-inference-serving
  appendix-t-distributed-ml            -> appendix-o-distributed-ml
  appendix-u-docker-containers         -> appendix-p-docker-containers
  appendix-ad-master-reference-tables  -> appendix-r-master-reference-tables
  appendix-ae-production-patterns      -> appendix-s-production-patterns
  appendix-af-pedagogy-kit             -> appendix-t-pedagogy-kit
  appendix-ag-problem-solution-key     -> appendix-u-problem-solution-key
  appendix-ai-freshness-2026           -> appendix-v-freshness-2026

Demote (3 sections -> 1 page):
  appendix-v-tooling-ecosystem         -> appendix-q-tooling-map  (single page only)

Relocate (out of appendices entirely):
  appendix-aj-reading-pathways         -> front-matter/fm-reading-pathways.html
  appendix-ak-course-syllabi           -> front-matter/fm-course-syllabi.html
```

For sectioned appendices the per-file rename is mechanical:
```
section-r.1.html -> section-m.1.html  (and 2, 3, 4, 5)
section-s.1.html -> section-n.1.html  (and 2-5)
section-t.1.html -> section-o.1.html  (and 2-7)
section-u.1.html -> section-p.1.html  (and 2-4)
```

Sections under the demoted V become bullets inside Q's single
`index.html`; the section-v.*.html files are deleted (after their
unique paragraphs are migrated to K, L, M, N as appropriate).
