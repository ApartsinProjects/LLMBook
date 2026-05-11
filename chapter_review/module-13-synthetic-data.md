# Module 13: Synthetic Data Generation & LLM Simulation

**Audit date**: 2026-05-11
**Sections reviewed**: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7
**Total word count**: ~30,000 prose words (HTML wc ~48,300)

## Summary
Strong content on Self-Instruct/Evol-Instruct, persona-driven generation, LLM-as-judge curation, active learning, weak supervision (Snorkel), R1-style reasoning data, and classical augmentation. Voice (Synth the AI agent), metaphors (flight simulator, refinery), and code examples are good. The dominant systemic problem is a chapter-wide off-by-one in section numbering: every file 13.3 through 13.7 contains body H2s numbered one higher than the filename (13.3 has "13.4.x" headings, 13.7 has "13.8.x"), which strongly suggests an early section was dropped (almost certainly the original 13.3 "LLM-as-Simulator") without rerunning the body renumber.

## Inconsistencies
- `index.html` line 103: section card "13.3 LLM-as-Simulator & Evaluation Generation" links to `href="section-29.1.html"` - cross-chapter file path, broken from this directory. Either the section was merged into Chapter 29 evaluation, or the href is stale.
- `index.html` lines 113-167: every TOC card from 13.4 onward is one number off (card "13.4" links to file `section-13.3.html`, card "13.5" links to `section-13.4.html`, ..., card "13.8" links to `section-13.7.html`). The chapter ships 7 section files but the index advertises 8 sections.
- `section-13.3.html` body H2s are 13.4.1, 13.4.4, 13.4.5 (file/title is 13.3) - off by one and ALSO non-contiguous (4.2, 4.3 missing visible).
- `section-13.4.html` body H2s 13.5.1, 13.5.4, 13.5.5 - same off-by-one and gaps.
- `section-13.5.html` body H2s 13.6.1, 13.6.2 - off by one.
- `section-13.6.html` body H2s 13.7.1 through 13.7.7 - off by one.
- `section-13.7.html` body H2s 13.8.1 through 13.8.3 - off by one.
- `section-13.1.html` lines 37 and 41 figcaptions both labeled "Figure 13.1.3" (factory image and seed-garden image).
- `section-13.1.html` line 30 Big Picture: "Section 6.1 data curation pipeline from Section 06.4" - duplicated/garbled auto-cross-ref artifact (3 different section numbers in one sentence pointing at the same idea).
- Chapter-label breadcrumb on 13.1 says "Chapter 13 · Section 13.1" while M14/M15 use the chapter title style.

## Gaps
- The dropped section 13.3 "LLM-as-Simulator & Evaluation Generation" has not been replaced by anything that covers user simulation, red-teaming dataset generation, or RAG eval-set construction. Index promises this, none of the seven existing sections delivers it.
- Section 13.2.4 "Preference and Ranking Data Generation" exists but the chapter never explicitly bridges to Chapter 17's DPO/RLHF training pipeline (just one prereq mention); a concrete handoff would help.
- Distilabel coverage in 13.3 is brief; the chapter advertises Distilabel as a "production tool" but the concrete Distilabel pipeline example is lighter than the manual scoring example.
- No discussion of synthetic data licensing constraints (e.g. OpenAI ToS forbidding training competing models on outputs from their models was relaxed in 2025 but the chapter does not mention licensing at all).
- Model-collapse risk is mentioned in objectives and 13.1 but never quantified; a small empirical example or chart showing accuracy vs synthetic-fraction would land the warning.

## Errors
- `section-13.7.html` line 41 H2 "13.8.1 Why Augment? The Diversity Problem" - if the chapter has 7 sections, "13.8" can never be a valid H2; this off-by-one is an actual reader-facing bug in cross-references.
- `index.html` 13.3 link to `section-29.1.html` will 404 (relative path resolves outside the chapter dir).
- The "Microsoft Phi-2 outperformed models 25x its size" claim in 13.1 is a 2023 marketing statement now superseded by Phi-3/Phi-4; the framing dates the chapter.
- Section 13.2 EvolInstruct example (likely; need verify): the depth/breadth evolution prompts are templated correctly but the seed fan-out math (e.g. "100 seeds * 4 evolutions * 5 epochs = 2000 examples") is presented as deterministic, ignoring deduplication losses.
- Per-example human-annotation cost range "$0.10 to $2.00" in 13.1 is plausible for English crowdworker data but understated for SME-required tasks (medical, legal frequently $10-50).

## Improvements
- Chapter-wide renumber pass: sweep H2s/H3s/figure/code-fragment captions across sections 13.3-13.7 and the index hrefs to align with the actual file names.
- Either restore section 13.3 (LLM-as-Simulator) by writing it fresh, or remove its entry from the index and the prereqs of downstream sections that cross-reference it.
- Add a small comparison table of Self-Instruct, Evol-Instruct, Self-Rewarding, Magpie, and OSSInstruct (all are 2023-2025 instruction-generation methods that deserve side-by-side mention).
- A "synthetic-data audit checklist" callout (deduplication, contamination, leakage, license, bias check) would be a high-leverage takeaway box.
- Add a quantitative model-collapse plot or example to anchor the abstract warning.
- Strengthen handoff to Chapter 14 (SFT) and Chapter 17 (DPO) with explicit "the format you produce here is the format Chapter X consumes" callouts.

## One-thing-only fix
Repair the chapter index hrefs and renumber every body H2 in sections 13.3-13.7 down by one (13.4.x to 13.3.x, etc). This is a single mechanical pass that fixes the navigation, the heading numbers, and the cross-references in one shot, and surfaces whether the missing 13.3 should be reconstructed.
