# Module 15: Parameter-Efficient Fine-Tuning (PEFT)

**Audit date**: 2026-05-11
**Sections reviewed**: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7
**Total word count**: ~28,000 prose words (HTML wc ~46,400; section 15.5 absorbed-distillation alone is ~9,900)

## Summary
Module 15 has the most severe structural problem in the entire batch. Chapter 16 (Distillation and Model Merging) was merged into Chapter 15, but the merger was incomplete: the chapter index never added cards for the absorbed sections 15.5/15.6/15.7, the body H2s in those sections still use 16.1.x/16.2.x/16.3.x numbering, and the chapter still has a "Next: Chapter 16" link that points at a chapter that no longer exists. Content quality where it lands (LoRA mathematics, QLoRA NF4, DoRA, soft prompts, knowledge distillation case studies) is strong, but readers reaching the chapter via TOC will never see half of what was added.

## Inconsistencies
- `index.html` lists only 4 section cards (15.1-15.4) but the directory ships 7 section files. Sections 15.5 Knowledge Distillation, 15.6 Model Merging, and 15.7 Continual Learning are completely invisible from the chapter TOC.
- `index.html` line 132-133 "What's Next?" callout says "Chapter 16: Distillation and Model Merging" - but that chapter was merged INTO this chapter. Stale forward link.
- `index.html` line 76 prereq: "Hugging Face [Section 4.1] library" - cross-ref text "Section 4.1" is the wrong link label for what should be "transformers" or similar.
- `section-15.5.html` body H2s are 16.1.1 through 16.1.8 (file is 15.5; absorbed from old Chapter 16 Section 1).
- `section-15.6.html` body H2s are 16.2.1 through 16.2.7 (file is 15.6; absorbed from old Chapter 16 Section 2). Also non-contiguous: 16.2.1, 16.2.2, 16.2.3, 16.2.4, 16.2.7 (5 and 6 missing or moved).
- `section-15.7.html` body H2s are 16.3.1, 16.3.2, 16.3.5, 16.3.6 (file is 15.7; gaps where 16.3.3 and 16.3.4 should be).
- `section-15.1.html` H2 sequence: 15.1.1, 15.1.2, 15.1.3, 15.1.7, 15.1.8 - numbers 4, 5, 6 are missing.
- `section-15.2.html` H2 sequence: 15.2.1, 15.2.5, 15.2.6, 15.2.7, 15.2.8, 15.2.9, 15.2.10 - numbers 2, 3, 4 are missing.
- `section-15.4.html` H2 sequence is contiguous (15.4.1 - 15.4.7) - good outlier.
- `section-15.3.html` H2 sequence is contiguous (15.3.1 - 15.3.8) - good.
- Index "Section 15.2" card mentions "for deep coverage of soft prompt methods, see Section 15.4" - good cross-ref but the card itself omits absorbed content.

## Gaps
- Knowledge distillation, model merging (TIES, DARE, MoErging, evolutionary merge), and continual learning are all missing from the chapter index even though their content exists. Readers using TOC navigation will not discover them.
- Cross-reference handoffs to Chapter 17 alignment for distillation-from-RLHF-models are missing despite being a natural pairing.
- `section-15.1.html` H2 jump from 15.1.3 to 15.1.7 strongly suggests three sub-sections (rank/alpha tuning details, target module selection, QLoRA mathematics) were dropped or absorbed without renumber. Verify content completeness on QLoRA NF4 / double-quant / paged optimizers - the index lists these but they may have been removed.
- `section-15.2.html` similar 4 missing sub-sections (15.2.2, 15.2.3, 15.2.4) - probably DoRA depth, LoRA+ details, adapter layers detail.
- Section 15.5 distillation has no explicit cross-ref to Chapter 13 (synthetic-reasoning data), which is the natural consumer of distilled CoT traces.
- Section 15.6 model merging never mentions MergeKit, the most commonly used 2025 tooling, despite covering TIES/DARE/Task Arithmetic by name.
- No coverage of LoRA hot-swapping for serving (PEFT library supports, vLLM has it as of 2024) despite production-deployment focus elsewhere.

## Errors
- The chapter "Next" link points at Chapter 16 (does not exist post-merger) - breaks navigation when reader reaches the bottom of any section.
- Section 15.6 "16.2.7 Evolutionary Model Merging" - sakana.ai's evolutionary merge is well-known but the H2 numbers (16.2.x) are wrong post-merger.
- Section 15.5 line 53 H2 "16.1.1 Classical Distillation Framework" - should be 15.5.1.
- LoRA `W' = W + (alpha/r) * BA` scaling - verify whether the section presents the alpha-scaled or raw `BA` formula (book overview says "W' = W + BA" without the scaling factor).
- Index objectives mention "Prefix Tuning" but Prefix Tuning is in section 15.4 (Soft Prompts), not in 15.2 (Advanced PEFT). The objective bullet conflates the two.
- Section 15.7 "16.3.5 Elastic Weight Consolidation (EWC)" - EWC's Fisher information matrix calculation is non-trivial; verify the math is correct. The H2 number is wrong regardless.

## Improvements
- HIGH PRIORITY: rebuild `index.html` to include cards for 15.5 Knowledge Distillation, 15.6 Model Merging, and 15.7 Continual Learning.
- Renumber body H2s in 15.5, 15.6, 15.7 from 16.x.y to 15.x.y across all heading, caption, and image-filename references.
- Update the "What's Next?" link to point at Chapter 17 (Alignment, RLHF, DPO).
- Renumber H2 sequences in 15.1 and 15.2 to be contiguous (or restore the missing sub-sections if they were dropped accidentally).
- Add a chapter-opening map showing how the seven sections relate: Foundations (15.1-15.2 PEFT), Tooling (15.3), Soft Prompts (15.4), Compression/Composition (15.5-15.6), Lifecycle (15.7).
- Add MergeKit reference in 15.6.
- Add a cross-ref from 15.5 distillation to 13.6/13.7 reasoning-data synthesis.

## One-thing-only fix
Add the three missing section cards (15.5 Knowledge Distillation, 15.6 Model Merging, 15.7 Continual Learning) to `index.html` and update the "What's Next?" link to Chapter 17. This single edit makes ~40% of the chapter's content discoverable. The body-H2 renumber from 16.x to 15.x is the second-priority fix once readers can actually find those sections.
