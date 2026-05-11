# Module 28: LLM Applications Across Industries

**Audit date**: 2026-05-11
**Sections reviewed**: 28.1, 28.2, 28.3, 28.4, 28.5, 28.6, 28.7
**Total word count**: ~44,200 words (raw HTML)

## Summary
A breadth-over-depth tour of seven domains (vibe-coding, finance, healthcare, search, security, education/legal/creative, robotics+science). The conceptual material is solid and the per-domain "Real-World Scenario" callouts are a real strength. The chapter is undermined, however, by pervasive auto-generated code captions ("Implementation example", "Implementation of foo"), several inline cross-reference numbers that do not match what is actually present in the section, and substantial topical overlap with Chapter 27 (SayCan and robot planning are covered in both 27.6 and 28.7). Section 28.7 also abruptly switches into what looks like an unfinished lab at the end (Code Fragments 28.7.5-28.7.8 are dangling examples without a wrapping lab section).

## Inconsistencies
- **28.1**: Section opens with `Figure 28.1.2` (chapter-opener illustration). No `Figure 28.1.1` is defined; the diagram explaining FIM later in the section is *also* labelled `Figure 28.1.2` (line 51), making this a duplicate-number-and-missing-1 problem.
- **28.1**, line 86: comparison-table title reads "2. AI-Native IDEs and Coding Assistants Intermediate" — the leading "2." and trailing "Intermediate" are auto-generation leakage that should not be visible to readers.
- **28.2**: Code captions read "Code Fragment 28.2.1: Implementation example" and "Code Fragment 28.2.2: Implementation example" — both literally say "Implementation example", giving the reader nothing useful. Same pattern in 28.3 (28.3.1, 28.3.2: "Implementation example") and 28.4 (28.4.1: "Implementation of recommend_items", 28.4.3: "Implementation of __init__, chat") and 28.5 (28.5.1: "Implementation of extract_threat_intel") and 28.6 (28.6.1: "Implementation of socratic_tutor", 28.6.2: "Implementation of analyze_contract").
- **28.2**, line 350: prose says "Code Fragment 28.2.4 demonstrates this approach for product review analysis" but the next code block is captioned 28.2.4 with caption "Implementation of extract_aspect_sentiments"; then a *later* paragraph (line 477 area) again references "Code Fragment 28.2.3 demonstrates this approach" pointing to a *different* topic (emotion detection) — code fragment 28.2.3 was actually `extract_trading_signal`, not emotion. The reference is wrong; 28.2.5 is the emotion code.
- **28.6**, line 525: "Code Fragment 28.6.2 demonstrates this pattern" appears in the "Data-to-Text Generation" subsection, but Code Fragment 28.6.2 is `analyze_contract` (legal) and the data-to-text code is actually 28.6.6 (line 587).
- **28.7** (Robotics): the SayCan / Code-as-Policies / Inner Monologue material extensively overlaps with Section 27.6 (LLM-Powered Robotics). Both sections contain a "SayCan architecture" diagram and an LLM-as-task-planner code sketch. There is no "see Section 27.6 for deeper coverage" cross-reference in either direction, so the reader gets the same content twice with no signposting.
- **28.7**, lines 559-663: code fragments 28.7.5-28.7.8 (urllib/torch/torchaudio download, "Load a small model (choose 'base'...)", "Load a summarization model", "One-liner ASR pipeline using Whisper") look like an orphaned Whisper/summarization lab that has been pasted into the end of a section about scientific discovery. There is no introductory prose tying these snippets together.
- **28.5**, line 248 caption for `Figure 28.5.2`: the figure is referenced before it appears (figure is at line 248, callout reference at line 229), and the prose talks about "asymmetry" but the figure caption talks about "dual nature" — close but not the same framing.
- **28.6**, line 587 caption gives the topic ("Data-to-text generation") but the eight earlier captions in the same section all say "Implementation of …" — inconsistent caption style within a single section.

## Gaps
- **28.1** prerequisites omit Section 22.3 (code agents) even though the Big Picture explicitly says "the code agent patterns from Section 22.3 provide the architectural foundation for these tools" — a small but jarring inconsistency.
- **28.2** prerequisites are missing entirely from the visible top of the section (the index lists Chapter 11 etc., but the inline "Prerequisites" block only contains a short paragraph that does not enumerate specific sections).
- **28.3** (Healthcare): no discussion of *evaluation* of medical LLMs (MedQA, USMLE-style benchmarks); they are mentioned in 28.3.2 but never tied back to Chapter 29's evaluation framework.
- **28.4** (Search/Recommendation): does not discuss query rewriting failure modes or recall-vs-precision tradeoffs that production search teams face, even though this is canonical reading material for the domain.
- **28.5** (Cybersecurity): missing any reference to Section 32.x safety material on adversarial prompting, even though jailbreaking is an obvious bridge between offensive cybersecurity and LLM safety.
- **28.7** (Robotics): no cross-reference to Section 27.5 (VLA models) or 27.6 (robot planning) that would tell the reader "for the architectural deep dive, see Chapter 27". Given the v3.2 restructure, this gap is now load-bearing.
- The chapter has no "What you will *not* learn" or "Out of scope" callouts despite being a 7-domain survey; readers risk thinking they have full coverage of, say, healthcare AI when they have only seen 8 pages.

## Errors
- **28.1**, fun fact line 44: "the best AI coding agents solve about 50% of real GitHub issues" — as of early 2026 SWE-bench Verified scores from leading labs exceed 70% (Sonnet 4 / Opus 4 / GPT-5-class models). The 50% figure is ~12 months stale.
- **28.2**, line 416 mentions "FINRA (Financial Industry Regulatory Authority)" which is correct but introduces it inline without first explaining acronyms; later text uses "SEC" without expanding.
- **28.3** mentions "MoLFormer (IBM Research), trained on 1.1 billion SMILES sequences with rotary positional embeddings" — MoLFormer-XL was trained on ~1.1B molecules (yes), but the architecture uses linear attention with rotary embeddings; calling out only "rotary" understates the linear-attention contribution.
- **28.4** code samples show recommendation systems prompting LLMs to score items — but pass *all* items inline, which would not scale beyond a few hundred candidates. There is no acknowledgment of the candidate-generation step that real recsys pipelines use.
- **28.7**, line 47: refers to Figure 28.7.1 (SayCan architecture). The figure caption is correct, but the prose says "the LLM proposes actions scored by affordance models, and the robot executes the highest-scoring feasible action" without any clarification that this is essentially the same content as Section 27.6.1.1.
- The SayCan code in 28.7 (Code Fragment 28.7.1) is "Conceptual: LLM as robot task planner" — it does not actually call any LLM; it defines dataclasses and pseudocode. Marking it `Conceptual:` in the caption helps, but the surrounding prose treats it as runnable.
- **28.6**, Socratic tutor scenario claims "Students who used the Socratic tutor scored 12% higher on exams". This is presented as a Real-World Scenario but no source is cited; if it is a hypothetical, the case study should be flagged as such (other scenarios in the chapter conflate hypothetical and reported results).

## Improvements
- Replace every "Implementation example" / "Implementation of foo, bar" caption with a one-sentence functional description (the code-caption-agent at `agents/book-skills/agents/40-code-caption-agent.md` is exactly the tool for this).
- Renumber 28.1 figures (28.1.2 appears twice, 28.1.1 is missing).
- Add explicit "see Chapter 27" cross-references in 28.7 robotics paragraphs to prevent duplicate coverage from looking like a bug.
- Either expand the Whisper/summarization snippets at the end of 28.7 into a proper lab with header + objective + steps, or move them out of the section.
- Update SWE-bench number in 28.1 fun fact.
- Add a short "Out of scope" or "Where to go deeper" subsection to each domain so readers know what they are missing (e.g., 28.3 should point at Anthropic's Claude-for-medicine evaluations, MedPaLM 2 etc.).
- Cross-link 28.5 (security) to Section 32.x safety material on prompt injection.

## One-thing-only fix
Sweep the entire chapter with the code-caption-agent (`agents/book-skills/agents/40-code-caption-agent.md`) to replace the ~25 placeholder "Implementation example" / "Implementation of foo, bar" captions with descriptive ones. This is the single change that most changes the perceived professional quality of the chapter, and it makes the wrong-cross-reference issues in 28.2 and 28.6 (where prose references captions that no longer mean anything) actionable.
