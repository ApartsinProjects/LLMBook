# Comic Wiring Report: Chapters 34 and 36

Wired all 15 cartoon-comic / mental-map illustrations from `.book-update/comic-manifest.jsonl`
(rows with `chap_sec` starting "34." or "36.") into their sections as `<figure class="illustration">`
blocks. All images verified present on disk and confirmed 1024x1024 (so `width="1024" height="1024"`).

## Important context: two image sets on disk

Each target section directory contained an **older** set of comic JPEGs (semantic names, dated
May 18) and the **new** manifest set (dated May 20, e.g. `comic-34.1-2-...jpg`). The manifest points
at the new set. Findings:

- **Chapter 34**: every section (34.1-34.5) already had comics wired using the *old* filenames at the
  exact placements the manifest describes. Visual comparison confirmed the new manifest files are
  cleaner regenerations of the *same* concept. Action: **swapped the `src`** in the existing figures to
  the new manifest filenames and refreshed the `alt` text to describe the new artwork (6 swaps), plus
  **inserted 1 net-new figure** (34.5-14, which had no prior wiring).
- **Chapter 36**: only 36.2 had one old comic (`comic-library-vs-framework.jpg`, a *thin-vs-thick*
  split panel). The manifest's 36.2-22 is a **different** concept (matryoshka nesting dolls) with its
  own distinct placement, so the existing 36.2.1 was **kept** and all 8 manifest comics were
  **inserted as new figures**.

## Chapter 34 (module-34-structured-information-extraction-ner)

| Manifest | Kind | Section | Figure | Action | Placement |
|---|---|---|---|---|---|
| 34.1-2 | MENTAL-MAP | section-34.1 | Figure 34.1.1 | src swap + alt refresh | Top of 34.1.1 (librarian/wizard), after Fun Fact |
| 34.1-4 | COMIC | section-34.1 | Figure 34.1.2 | src swap + alt refresh | In 34.1.1.1, just before Table 34.1.1 (four-panel strip) |
| 34.2-6 | COMIC | section-34.2 | Figure 34.2.4 | src swap + alt refresh | Start of 34.2.2, near the SRL material (detective board) |
| 34.3-9 | COMIC | section-34.3 | Figure 34.3.1 | src swap + alt refresh | In Production Pattern P10 callout (hospital triage) |
| 34.4-12 | COMIC | section-34.4 | Figure 34.4.1 | src swap + alt refresh | Top of 34.4.1 after the Fun Fact (graceful degradation) |
| 34.5-14 | COMIC | section-34.5 | Figure 34.5.1 | **NEW insertion** | Just before "34.5.1.2 LLM-Based Coreference Resolution" (pronoun bubbles to Dr. Sarah Chen) |
| 34.5-15 | MENTAL-MAP | section-34.5 | Figure 34.5.2 | src swap + alt refresh | Start of "34.5.2 Integrated Document Understanding Pipeline" (assembly line) |

Note: section-34.2 retains a pre-existing figure-number gap (1, 3, 4; the events-flypaper comic at
Figure 34.2.3 is NOT in this manifest scope). The renumber script leaves sorted+unique sequences
untouched, every prose ref resolves to a caption, and the audit reports 0 issues, so the gap was left
as-is rather than churning an out-of-scope figure.

## Chapter 36 (module-36-retrieval-tools)

| Manifest | Kind | Section | Figure | Action | Placement |
|---|---|---|---|---|---|
| 36.1-18 | COMIC | section-36.1 | Figure 36.1.2 | NEW insertion | Right after the "Serverless does not mean zero cost at zero load" Key Insight callout |
| 36.1-20 | COMIC | section-36.1 | Figure 36.1.3 | NEW insertion | Right after the "Benchmark on your data, not theirs" Warning |
| 36.2-22 | COMIC | section-36.2 | Figure 36.2.2 | NEW insertion | After the "Framework abstractions leak" Key Insight callout (matryoshka dolls) |
| 36.2-23 | MENTAL-MAP | section-36.2 | Figure 36.2.3 | NEW insertion | End of "36.2.8 The thinnest viable stack" summary paragraph (recipe card) |
| 36.3-26 | COMIC | section-36.3 | Figure 36.3.2 | NEW insertion | After the "BM25 baseline still beats half of the dense retrievers" Fun Fact (park-bench) |
| 36.3-27 | MENTAL-MAP | section-36.3 | Figure 36.3.3 | NEW insertion | Just before "36.3.9 Building your own evaluation set" (tiered cake) |
| 36.4-29 | COMIC | section-36.4 | Figure 36.4.2 | NEW insertion | After the "Read the embedder's prompt convention" Warning (crown vs frown embedders) |
| 36.5-32 | COMIC | section-36.5 | Figure 36.5.1 | NEW insertion | At the end, just before the Further Reading / bibliography (two villages + bridge) |

The pre-existing 36.2.1 (thin-library-vs-thick-framework, 1408x768) was left untouched.

## Procedure followed per comic

1. Confirmed the image file exists in `<section dir>/images/` and is 1024x1024.
2. Located the placement anchor from the manifest `placement` field.
3. Inserted/updated a `<figure class="illustration">` block with screen-reader `alt` text (describes
   the cartoon) and a `<figcaption>` that ties the joke to the technical lesson; added a one-sentence
   prose lead-in before each new figure.
4. Ran `scripts/fix_caption_order_only.py --apply` on all 10 files to keep caption numbers monotonic
   in document order.
5. Re-checked that every figure prose ref resolves to a caption.

No em dashes used. No image files modified or generated.

## Leftover (out of scope, flagged for cleanup)

The 6 old chapter-34 comic JPEGs that were swapped away are now orphaned (0 references):
`comic-librarian-wizard.jpg`, `comic-classical-vs-llm-strip.jpg`, `comic-srl-detective-board.jpg`,
`comic-hospital-triage.jpg`, `comic-graceful-degradation.jpg`, `comic-coreference-pipeline.jpg`.
(`comic-events-flypaper.jpg` is still in use by Figure 34.2.3 and was kept.)

## Validation

`python -m agents.book-skills.scripts.audit.run --priority P0+P1+P2 --root .`
=> **Scanned 558 files. Found 0 issues.** No new FIGURE_SEQUENCE / DUP_FIGURE_NUM /
BROKEN_FIGURE_REF / MISSING_IMG_DIMS issues in the edited files.
