# Module 17: Alignment, RLHF, DPO & Preference Tuning

**Audit date**: 2026-05-11
**Sections reviewed**: 17.1, 17.2, 17.3, 17.4, 17.5
**Total word count**: ~22,500 prose words (HTML wc ~34,400; section 17.5 absorbed from old Chapter 32.14)

## Summary
Content depth on RLHF (Bradley-Terry, PPO with KL penalty, GRPO), DPO (full derivation and KTO/ORPO/SimPO/IPO variants), Constitutional AI, RLVR/DeepSeek-R1, and the absorbed alignment frontiers (scalable oversight, weak-to-strong, interpretability-based alignment) is the deepest in the entire batch. The chapter's failure mode is concentrated in section 17.5: it was wholesale absorbed from old Chapter 32.14 (or 35.1) without renumbering, retains the wrong part/chapter breadcrumbs, points figure captions and image paths into a different part of the book, and is invisible from the chapter index.

## Inconsistencies
- `index.html` lists 4 section cards (17.1-17.4) but the directory ships 5 files. Section 17.5 "Alignment Research Frontiers" is missing from the chapter TOC.
- `section-17.5.html` line 20 part-label `<a href="../../part-10-frontiers/index.html">Part X: Frontiers</a>` - section 17.5 is in Part IV (Training and Adapting), not Part X.
- `section-17.5.html` line 21 chapter-label `<a href="../../part-10-frontiers/module-32-safety-ethics-regulation/index.html">Chapter 35: AI and Society</a>` - the breadcrumb claims this section belongs to Chapter 35, in Module 32. Both wrong.
- `section-17.5.html` H2 numbering: lines 41, 101, 116, 131, 147 use `35.1.1`, `35.1.2`, `35.1.3`, `35.1.4`, `35.1.5`. The whole hierarchy says 35.1.x while the file is 17.5.
- `section-17.5.html` figcaptions: line 39 "Figure 32.14.1", line 56 "Figure 32.14.2". Image src paths point to `../../part-10-frontiers/module-32-safety-ethics-regulation/images/ch35-...` (cross-part reference; if Chapter 32 still exists those still resolve, but they should be co-located with the chapter that owns them).
- `section-17.5.html` line 72 `Pseudocode 35.1.1` caption.
- `section-17.1.html` H2 sequence: 17.1.1, 17.1.2, 17.1.3, 17.1.4, 17.1.5, 17.1.7, 17.1.8, 17.1.6 (17.1.6 ends up at line 666 after 17.1.8). Out-of-order numbering.
- `section-17.3.html` H2 sequence: 17.3.1, 17.3.2, 17.3.5, 17.3.6 (17.3.3 and 17.3.4 missing).
- `section-17.4.html` H2 sequence: 17.4.1, 17.4.4, 17.4.5 (17.4.2 and 17.4.3 missing).
- `index.html` "What's Next?" line 135 says "Part V: Retrieval and Conversation" (correct), but `chapter-nav` previous link points at `module-15-peft/section-15.7.html` which is fine - however the path skips through nothing for what was Chapter 16 (now merged), which is fine but perhaps disorienting given the renumbering.

## Gaps
- Section 17.5 (frontiers) is invisible from the chapter index and from the typical reader's TOC navigation.
- The chapter never explicitly cross-references the dropped Chapter 16 - readers expecting distillation/merging coverage (which moved to Chapter 15) are not redirected.
- Index objectives mention "GRPO algorithm and its role in DeepSeek-R1" once (in 17.1) but GRPO also appears in 17.4 RLVR; only the second mention develops the math. Cross-reference both.
- DPO 17.2 covers KTO/ORPO/SimPO/IPO but does not mention SLiC or RLOO - the latter is increasingly common in 2025.
- The scalable oversight discussion in 17.5 mentions debate/recursive reward modeling/CAI but does not cross-reference back to 17.3 Constitutional AI, even though that section already covers CAI in detail. Readers will see the same material twice.
- No discussion of DPO's preference dataset format vs RLHF's prompt-then-pair format - a practical handoff to Chapter 13's preference-data section would help.

## Errors
- `section-17.5.html` is presented as a chapter-end frontier section but the breadcrumbs claim it belongs to a different chapter; click-through navigation will jump readers out of Chapter 17 unexpectedly.
- Section 17.5 line 38 image path `../../part-10-frontiers/module-32-safety-ethics-regulation/images/ch35-opener-scales-of-alignment.png` - if old Chapter 32 was renamed/restructured, this path may 404. At minimum it cross-couples the chapter to a directory it should be independent of.
- Section 17.1 line 666 H2 "17.1.6 RLHF Infrastructure at Scale" appears AFTER H2 "17.1.8 Practical Tips" - the 17.1.6 was inserted/moved without resequencing.
- Bradley-Terry preference model derivation in 17.1 should connect explicitly to the sigmoid/logistic interpretation; verify the math carries through to the DPO derivation in 17.2 (the two should share notation).
- "DeepSeek-R1 training pipeline" claim in 17.4: the actual R1 paper used a multi-stage pipeline (cold-start SFT → RL → SFT on filtered RL outputs → RL again). Verify the section's description matches.
- The "Superalignment team was dissolved in 2024" framing in 17.5 is correct (it was dissolved May 2024) but the section may be slightly stale on what replaced it.

## Improvements
- HIGH PRIORITY: Add a section card for 17.5 to the chapter index, fix the part-label and chapter-label breadcrumbs to "Part IV" / "Chapter 17", and renumber all 35.1.x H2s to 17.5.x.
- Move the absorbed images from `../../part-10-frontiers/module-32-...` into `module-17-alignment-rlhf-dpo/images/` and update src paths.
- Resequence section 17.1 H2s contiguously (17.1.1 - 17.1.8) and patch the missing 17.3.x and 17.4.x sub-sections (or remove the gaps).
- Add a "Roadmap" diagram at the top of the chapter showing the alignment family tree: SFT → RM → PPO → DPO → KTO/IPO/ORPO/SimPO → GRPO/RLVR. The taxonomy is present in prose but a single visual would make the relationships explicit.
- Cross-reference 17.3 (CAI) from 17.5 (Scalable Oversight) so the two CAI passes do not feel duplicative.
- Add a concrete preference-dataset format example bridging Chapter 13 output and 17.2 input.

## One-thing-only fix
Re-home section 17.5: rewrite the part/chapter breadcrumbs to "Part IV" / "Chapter 17", renumber every `35.1.x` H2 to `17.5.x`, fix the figure caption numbers (32.14.x to 17.5.x), move the images into the chapter's own `images/` directory, and add the missing section card to `index.html`. This single chapter-localizing pass turns a stranded frontier essay into a discoverable, self-consistent chapter conclusion.
