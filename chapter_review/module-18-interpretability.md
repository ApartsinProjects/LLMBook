# Module 18: Interpretability & Mechanistic Understanding

**Audit date**: 2026-05-11
**Sections reviewed**: 18.1, 18.2, 18.3, 18.4 (4 sections)
**Total word count**: ~40,131 (851 index + 9,925 + 9,627 + 8,342 + 11,386)

## Summary
Module 18 was relocated from Part 2 (Understanding LLMs) to Part 10 (Frontiers) in v3.x but the file metadata, breadcrumbs, prev/next navigation, and "What's Next" prose were never updated. Content quality is technically strong with rigorous coverage of attention probing, mechanistic interpretability, SAEs, activation patching, and attribution methods, but the navigation and structural metadata are completely inconsistent with the chapter's new home.

## Inconsistencies
- **index.html line 17**: `<div class="part-label">Part II: Understanding LLMs</div>` should be Part X: Frontiers.
- **index.html line 138-139**: "What's Next?" says "In the next part, Part III: Working with LLMs..." — wrong; the chapter is now in Part 10. The next part should be Part 11 (or this should chain to Chapter 34).
- **index.html line 142**: prev nav points to `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` (still treats 18 as the last chapter of Part 2). Line 143 also still labels "Part II: Understanding LLMs".
- **All 4 sections (18.1-18.4) header line 20**: `<div class="part-label"><a href="../../part-2-understanding-llms/index.html">Part II: Understanding LLMs</a></div>` — wrong part label and broken anchor at the new location.
- **Section 18.4 footer next-nav (final line)**: `<a class="next" href="../../part-3-working-with-llms/module-10-llm-apis/index.html">Chapter 10: Working with LLM APIs</a>` — chains forward to Chapter 10, which is not the next chapter from a Part-10 perspective. Also the inline "What Comes Next" prose says "we begin Part V by exploring embeddings" (Ch 19) — completely stale.
- **Section 18.1 prereqs (line 34)**: doubled cross-reference text: "builds on Section 4.1 architecture from Section 04.1: Transformer Architecture Deep Dive and Section 6.1 covered in Section 06.1: The Landmark Models." Reads as two duplicated link-mention pairs.
- **Section 18.1 line 88**: caption shows two consecutive `code-caption` divs: `Code Fragment 18.1.1` and `Code Fragment 18.1.20` for the same code block, the latter clearly an auto-generated duplicate label.
- **Section 18.1 line 100-108**: a second `<pre><code>` block ("Production equivalent using scikit-learn") appears inside the BertViz "Library Shortcut" callout but has no introductory text, no caption, and is unrelated to BertViz; it appears to be misplaced content from a probing example.
- **Section 18.2 lines 30 and 40**: two different figures both numbered "Figure 18.2.3" (the coat-rack superposition figure and the residual-stream diagram). The coat-rack should be 18.2.1 or 18.2.2.
- **Section 18.1 line 30**: figure labeled "Figure 18.1.2" but it is the chapter-opener X-ray illustration that should be 18.1.1; the actual 18.1.2 (taxonomy diagram) is also labeled 18.1.2 at line 127.

## Gaps
- index "Big Picture" callout cross-references Chapter 17 alignment, but that arrives BEFORE this chapter in the book; meanwhile readers reaching Chapter 18 in Part 10 need to be reminded that interpretability builds on Ch 4, 6, 7, all of which are far behind.
- No prerequisite link to Chapter 32 even though 18.4 explicitly says interpretability supports "safety requirements discussed in Section 32.1."
- Module 34 Section 34.7 ("Mechanistic Interpretability at Scale") substantially duplicates 18.2 (superposition, SAEs, scaling). Neither chapter cross-references the other to disambiguate scope; readers will be confused why the topic appears twice.
- Section 18.1 prereq table omits `appendix-a-mathematical-foundations/section-a.1.html` (linear algebra) which IS in the index prereqs.
- Section 18.4 references `module-28-llm-applications/section-28.1.html` and `module-29-evaluation-observability/section-29.1.html` in its "What Comes Next" without verifying these exist (Ch 28 was renumbered/affected by v3.2 mergers).

## Errors
- **Section 18.1 line 25 epigraph**: agent-desc mismatch — "Probe, Flashlight Wielding AI Agent" but Section 18.2 line 26 has "Probe, Reverse Engineering AI Agent"; index line 25 has "Probe, Relentlessly Curious AI Agent." Three different one-line bios for the same agent character within one chapter.
- **Section 18.1 lines 84-85**: code calls `plot_attention_head(attentions[5], tokens, layer=5, head=1)` then `plt.savefig(...)` outside the function but `plt` is shadowed by the function returning `fig`; the `plt` import survives, so it works, but the demonstration is sloppy: better to call `fig.savefig(...)`.
- **Section 18.1 code line 169-176**: `ablate_head` hook uses `activation[:, :, 3, :] = 0` to zero out "head index 3" but the comment in the surrounding prose names L5H3, while the file's hook attaches at `blocks.5.attn.hook_z` (correct layer). The hardcoded `3` in the slice will work for `hook_z` (shape `[batch, seq, n_heads, d_head]`), but the inconsistency between the code's hardcoded `3` and a function parameter is confusing for a teaching example.
- **Section 18.1 code output**: shows `clean=0.0847, ablated=0.0213` for "P(nurse-related)" — these are made-up illustrative numbers but no caveat that they will not match real GPT-2 small.
- **Section 18.4 next-nav**: chains to Chapter 10 (regression to Part 3) rather than to Ch 19 or to Chapter 34 (the actual next chapter in Part 10). Hard navigation error.
- Section 18.2 line 30 figcaption says "Figure 18.2.3" but the figure is a coat-rack illustration of superposition, conceptually the very first figure of the section — number is duplicated (see Inconsistencies).
- Module-18 cross-references to `module-04-transformer-architecture/section-4.1.html` appear ~7 times in 18.2 alone, often back-to-back — over-referencing fatigue.

## Improvements
- Bulk-find/replace `Part II: Understanding LLMs` → `Part X: Frontiers` in all five module-18 HTML files; fix the part-label anchor `../../part-2-understanding-llms/index.html` → `../../part-10-frontiers/index.html`.
- Repair index prev/next navigation: prev should be the last section of Module 33 (or whatever closes Part 9), next should be Section 18.1 (already correct), and the chapter's "next" after 18.4 should be Module 34 Section 34.1.
- Resolve the 18.2 vs 34.7 overlap: either consolidate into one place or add a clear scope-divider sentence at the top of each (e.g. 18.2 = "the techniques", 34.7 = "scaling them to frontier models").
- Renumber duplicate Figure 18.2.3 and Figure 18.1.2; run a sweep to ensure each figure number appears exactly once per section.
- Standardise the "Probe" agent bio across the chapter (pick one tagline).
- Move the misplaced "Production equivalent using scikit-learn" snippet in 18.1 next to the actual probing example in section 18.1.2 (where it logically belongs).
- Remove the duplicate Code Fragment caption (`18.1.1` + `18.1.20`) on the same code block in 18.1.

## One-thing-only fix
Update the part-label, breadcrumbs, prev/next nav, and "What's Next?" prose across the 5 module-18 files so the chapter actually reads as the opening of Part 10 (Frontiers) rather than as the last chapter of the deleted Part 2 layout. Current state is jarring on page-one and will mislead every reader.
