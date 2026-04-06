# Part II Building Report: Modules 06, 07, 08

Four-agent consolidated review covering Visual Learning, Exercise Design, Examples/Analogies, and Code Pedagogy.

Date: 2026-03-26

## Inventory Summary

| Section | SVGs | Code Blocks | Code Outputs | Quiz Qs | Tables |
|---------|------|-------------|--------------|---------|--------|
| 6.1 Landmark Models | 2 | 2 | 1 | 4 | 0 |
| 6.2 Pre-training Objectives | 2 | 4 | 2 | 4 | 1 |
| 6.3 Scaling Laws | 2 | 2 | 2 | 4 | 1 |
| 6.4 Data Curation | 1 | 2 | 2 | 4 | 2 |
| 6.5 Optimizers & Training | 1 | 3 | 2 | 4 | 1 |
| 6.6 Distributed Training | 2 | 3 | 1 | 4 | 2 |
| 6.7 In-Context Learning | 1 | 2 | 1 | 4 | 1 |
| 7.1 Closed-Source Models | 1 | 0 | 0 | ~4 | 2 |
| 7.2 Open-Source Models | 1 | 1 | 0 | ~4 | 0 |
| 7.3 Reasoning Models | 2 | 1 | 0 | ~4 | 0 |
| 7.4 Multilingual LLMs | 1 | 1 | 0 | ~4 | 0 |
| 8.1 Model Quantization | 2 | ~3 | ~2 | ~4 | 1 |
| 8.2 KV Cache & Memory | 1 | 1 | 1 | ~4 | 0 |
| 8.3 Speculative Decoding | 1 | 1 | 1 | ~4 | 0 |
| 8.4 Serving Infrastructure | 2 | 4 | 4 | 5 | 0 |

## Top 30 Findings (Ranked by Priority)

### Critical: Missing Content or Structural Gaps

1. **[Visual] Section 7.1 has zero code examples or outputs.** This is the only section across all three modules with no code at all. Even a conceptual API-call example (comparing providers) or a cost-calculation snippet would ground the discussion. Priority: HIGH.

2. **[Code] Sections 7.2, 7.3, 7.4 lack code output blocks.** These sections contain code, but none of them show expected output. Without output, readers cannot verify whether they understand the code correctly. The code in 7.2 (MLA implementation) and 7.3 (distilled reasoning model) would especially benefit from showing realistic output. Priority: HIGH.

3. **[Exercise] Module 07 quizzes are entirely recall/comprehension (Bloom's levels 1 and 2).** Every quiz question across 7.1 through 7.4 asks "explain" or "compare," with no application, analysis, or evaluation questions. Add at least one exercise per section that asks the learner to make a decision (e.g., "Given these constraints, which model family would you recommend and why?"). Priority: HIGH.

4. **[Visual] Section 6.5 (Optimizers) has only one SVG for the grokking phenomenon.** The section covers five distinct topics (SGD, Adam, AdamW, memory-efficient optimizers, learning rate schedules), yet only grokking gets a diagram. A cosine decay schedule visualization and a memory comparison bar chart are both strongly needed. Priority: HIGH.

5. **[Example] No analogy in 6.6 (Distributed Training) explains tensor parallelism versus pipeline parallelism.** These two concepts are routinely confused by learners. A concrete analogy (such as comparing to a factory assembly line vs. dividing a single task across workers) would be valuable. Priority: HIGH.

6. **[Code] Section 7.1 (Closed-Source Models) has zero runnable code.** Even a minimal example showing how to call the OpenAI API, the Claude API, or the Gemini API would add practical value. Learners reading about frontier models should see how they are accessed programmatically. Priority: HIGH.

7. **[Visual] Section 10.3 (Speculative Decoding) uses only one SVG.** The acceptance/rejection sampling math deserves a visual showing probability distributions overlapping (draft vs. target), which would make the min(1, p/q) acceptance criterion intuitive. Priority: MEDIUM-HIGH.

8. **[Exercise] No "modify and observe" exercises exist anywhere in Modules 06, 07, or 08.** All exercises are quiz questions with hidden answers. There are no prompts asking the learner to change a parameter in a code example and predict or observe the result. This is a significant gap in active learning design. Priority: HIGH.

### Significant: Quality and Consistency Issues

9. **[Visual] Section 6.7 (In-Context Learning) has only one SVG for a section with four distinct theoretical frameworks.** The implicit gradient descent view and the task vector concept both lend themselves to diagramming but have no visual support. Priority: MEDIUM-HIGH.

10. **[Analogy] Section 10.1 (Quantization) lacks an intuitive analogy for how quantization works.** A comparison to reducing color depth in an image (millions of colors to 256 colors) would immediately ground the abstract math. Priority: MEDIUM-HIGH.

11. **[Analogy] Section 6.4 (Data Curation) uses no analogies to explain MinHash LSH.** The concept of "fingerprinting" documents could be compared to how Shazam identifies songs from audio fingerprints, making the locality-sensitive hashing idea far more approachable. Priority: MEDIUM.

12. **[Code] The code example in 6.7 (task vector extraction) is conceptual only and cannot run without a model.** A note or comment should explicitly state that this code requires a specific model download, or the example should be restructured to work with a small publicly available model. Priority: MEDIUM.

13. **[Visual] Section 7.4 (Multilingual LLMs) has only one diagram.** The tokenization efficiency disparity across languages is a central point and deserves a bar chart SVG showing token counts per language for equivalent sentences. The code output already contains this data, but a visual would be more impactful. Priority: MEDIUM.

14. **[Exercise] No exercises test Bloom's "Create" level across all 15 sections.** Quizzes cap out at "Analyze" (level 4). Consider adding at least one exercise per module that asks learners to design something (e.g., "Design a data mixing strategy for a model targeting medical applications"). Priority: MEDIUM.

15. **[Code] Section 6.2 (Pre-training Objectives) FIM code does not show output.** The code block for `apply_fim` does not include a `code-output` block. Learners cannot see what the FIM transformation looks like in practice without running the code. Priority: MEDIUM.

16. **[Analogy] Section 10.2 (KV Cache) compares PagedAttention to OS virtual memory but does not note where the analogy breaks down.** The comparison is excellent, but it should mention that, unlike OS paging, KV cache blocks are never swapped to disk and eviction policies differ significantly. Priority: MEDIUM.

17. **[Visual] Diagram captions are consistently good across all sections.** Every SVG has a descriptive caption with a figure number. This is a strength. No action needed.

18. **[Code] Section 6.3 (Scaling Laws) is the only section with a true "lab" exercise.** The curve-fitting code is excellent and could be a template for other sections. Consider replicating this pattern in 6.4 (data quality measurement), 8.1 (quantization quality comparison), and 8.3 (speculative decoding speedup estimation). Priority: MEDIUM.

19. **[Visual] Section 7.2 (Open-Source Models) DeepSeek V3 diagram is dense but excellent.** The four-quadrant architecture diagram clearly communicates all four innovations. However, it is the only SVG in the section. A timeline of open-weight model releases (similar to the encoder-only timeline in 6.1) would add useful context. Priority: MEDIUM.

20. **[Example] Section 7.3 (Reasoning Models) lacks a worked example showing the difference between ORM and PRM scoring on a concrete math problem.** The diagram shows the concept abstractly, but walking through a specific problem (e.g., a simple algebra mistake at step 3) would make the distinction concrete. Priority: MEDIUM.

### Minor: Polish and Enhancement Opportunities

21. **[Exercise] Section 10.2 quiz questions are not visible in the initial read but are confirmed to exist.** Verify that quiz formatting is consistent with the details/summary pattern used elsewhere. Priority: LOW-MEDIUM.

22. **[Code] Section 7.3 code example uses `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` without noting model size or download requirements.** A brief comment about disk/memory requirements (approximately 14 GB for BF16) would help learners plan. Priority: LOW-MEDIUM.

23. **[Visual] All SVGs use a consistent color scheme (primary #1a1a2e, accent #0f3460, highlight #e94560).** This visual consistency is a strength across all 15 sections. No action needed.

24. **[Analogy] Section 6.3 (Scaling Laws) effectively uses the "straight line on a log-log plot" framing but could benefit from a real-world analogy.** Comparing power laws to familiar phenomena (e.g., earthquake magnitude scaling, city population distributions) would help learners who are not comfortable with log-log plots. Priority: LOW.

25. **[Code] Section 6.6 (Distributed Training) gradient checkpointing code correctly shows memory savings but does not show the compute overhead.** Adding a timing comparison (with and without checkpointing) would make the 33% compute tradeoff tangible. Priority: LOW.

26. **[Exercise] All quizzes use the details/summary HTML pattern correctly.** Every quiz question has a collapsible answer. This is consistent and well-implemented. No action needed.

27. **[Visual] Section 10.4 (Serving Infrastructure) has strong diagram coverage with two SVGs, four code examples, and four code outputs.** This is the most code-rich section in Module 08 and serves as a good model for other sections. No action needed.

28. **[Analogy] Section 10.3 (Speculative Decoding) uses the "draft and verify" terminology clearly but could add a brief analogy.** Comparing to an editor reviewing a writer's draft (accept most text, fix a few sentences) would make the concept immediately accessible. Priority: LOW.

29. **[Code] Code blocks across all sections use consistent syntax highlighting with the Catppuccin color scheme.** The syntax highlighting is applied uniformly. No action needed.

30. **[Exercise] Section 6.1 (Landmark Models) quiz question about T5 is the strongest application-level question in Module 06.** It asks learners to explain the text-to-text framework's advantage, requiring synthesis. Other sections should aspire to this level. Priority: informational.

## Summary Statistics

| Metric | Module 06 | Module 07 | Module 08 | Total |
|--------|-----------|-----------|-----------|-------|
| Sections | 7 | 4 | 4 | 15 |
| SVG Diagrams | 11 | 5 | 6 | 22 |
| Code Blocks | 18 | ~3 | ~9 | ~30 |
| Code Outputs | 11 | 0 | ~8 | ~19 |
| Quiz Questions | 28 | ~16 | ~17 | ~61 |
| Tables | 7 | 2 | 1 | 10 |

## Key Strengths

- Consistent visual design across all sections (shared CSS, color palette, layout)
- Every section opens with a "Big Picture" callout that orients the reader
- Every section closes with "Key Takeaways" and a "Check Your Understanding" quiz
- SVG diagrams are captioned with figure numbers throughout
- Code examples include realistic output blocks in Module 06 and 08
- Math notation is rendered clearly using HTML entities
- Quiz answers use the details/summary pattern for self-paced learning

## Priority Action Items

1. Add code examples with output to all Module 07 sections (finding 1, 2, 6)
2. Create "modify and observe" exercises across all three modules (finding 8)
3. Add application/evaluation-level quiz questions to Module 07 (finding 3)
4. Add missing diagrams: 6.5 (LR schedule), 6.7 (implicit GD), 7.4 (tokenization bar chart) (findings 4, 9, 13)
5. Add grounding analogies where currently missing: 6.6 parallelism, 8.1 quantization, 6.4 MinHash (findings 5, 10, 11)
