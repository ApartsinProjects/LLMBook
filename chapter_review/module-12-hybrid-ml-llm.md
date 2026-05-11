# Module 12: Hybrid ML + LLM Architectures & Decision Frameworks

**Audit date**: 2026-05-11
**Sections reviewed**: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6
**Total word count**: ~30,000 prose words (HTML wc ~51,800; section 12.5 alone is ~14,900)

## Summary
Module 12 is the strongest chapter in this batch on substance: the four-axis decision framework, the comparative-advantage framing, classical-vs-LLM benchmarks, cascading triage, TCO modeling, and information extraction with BAML/spaCy/Instructor are all well-grounded. However it shows the worst structural / numbering hygiene of any chapter here: section 12.6 has body H2s numbered "12.8.1-12.8.7" (file is 12.6); section 12.5 is enormous and visibly imbalanced (~15K words versus ~6K average); and the index advertises a section "12.8" that no longer exists.

## Inconsistencies
- `index.html` line 145: section card title is "12.8 Dataset Engineering for LLM Applications" but href is `section-12.6.html`. Pick a number.
- `section-12.6.html` lines 37-480: every H2 is "12.8.x" (e.g. "12.8.1 Log-to-Dataset Pipelines", "12.8.7 Data Mixing Strategies"). The file's title and breadcrumb (line 20: "Chapter 12 · Section 12.6") say 12.6. Mass renumber required.
- `section-12.6.html` line 50 figcaption "Figure 12.6.1" but the image filename is `fig-12.8.1-log-to-dataset-pipeline.png` and same disagreement persists across all images in the section.
- `section-12.6.html` line 53: code begins with comment `# Code Fragment 12.6.5: Extracting training examples from production logs` baked into the code itself - the code-fragment number ID is hardcoded into a comment that should be metadata.
- `section-12.1.html` line 49 figcaption "Figure 12.1.2" used as the FIRST illustration; line 124 also "Figure 12.1.2" for the diagram - duplicate numbering inside one section.
- `section-12.1.html` line 44 prereqs: "Section 0.1" appears twice with two different links and similar duplicated cross-ref artifact ("from Section 06.2" linking to a different section than "scaling laws").
- Chapter index objectives list "spaCy NER" but section 12.5 is the single longest section in the entire chapter (~15K words) and likely needs splitting given the chapter average.
- The chapter-level breadcrumb on section 12.6 says "Chapter 12 · Section 12.6" while every other section in M12 uses the standard "<chapter title>" breadcrumb pattern. Inconsistent header markup.

## Gaps
- Section 12.5 ("Structured Information Extraction") is dramatically oversized at ~15K words versus 6K average. Likely should be split (NER/RE basics + LLM extraction + AutoML are arguably three sub-topics).
- The index objective bullet "Build cascading model systems that route queries from small to large models based on complexity signals" is well-served in 12.3, but the routing-vs-fallback distinction (covered in 10.3 LiteLLM) is not cross-referenced - readers doing 12.3 will rebuild what 10.3 already gave them.
- Section 12.6 (Dataset Engineering) sits awkwardly in a "Hybrid ML+LLM" chapter; thematically it belongs in Part IV alongside synthetic data (Chapter 13) or fine-tuning (Chapter 14). Its prereqs link forward to Chapter 13 and 17 - that forward dependency suggests the section was placed here for length rather than topical fit.
- TCO discussion in 12.4 references "build vs. buy breakeven analysis" but never gives actual numbers for self-hosted GPU per-hour amortized vs API per-token; an example chart with axes would make the breakeven concrete.
- No explicit treatment of latency budgets per pipeline stage when using a cascade (e.g. classifier 10ms + LLM 300ms + rules 1ms = 311ms budget) despite this being a recurring practical question.

## Errors
- `section-12.1.html` line 44 prereq cross-reference: the two URLs `module-00-ml-pytorch-foundations/section-0.1.html` are valid but Module 0 was previously dropped per the v3.1/v3.2 restructure notes; verify whether this link target still exists.
- `section-12.6.html` Code Fragment carries a hardcoded "Code Fragment 12.6.5" label in a code comment but appears in section 12.8.1 of the body; the number 5 is suspicious as the first appearance of a code block in this section.
- The "five-minute baseline" tip in 12.1 claims "scikit-learn in five minutes" can hit "80% of the desired accuracy" - this is a useful heuristic but presented as a general law; intent-classification on noisy short user queries can take a day to baseline well.
- Comparative-advantage analogy in 12.1 attributes Ricardo's principle to 1817 - correct date, but the application stretches the analogy (countries trade goods; here we route queries; not all readers will find the parallel illuminating).
- Section 12.5 BAML/Instructor coverage may have outdated API surface (BAML major rev was Q1 2026); spot-check the example code against current docs.

## Improvements
- Run a renumber pass on section 12.6 to convert all 12.8.x H2s/captions/image filenames to 12.6.x, OR if 12.8 was the canonical number, rename the file.
- Split section 12.5 into 12.5 (extraction primitives: NER, RE, event) and a new section (BAML/Instructor production patterns, AutoML).
- Add a small decision tree (mermaid diagram) summarizing "task type to recommended architecture" at the top of 12.1; the prose covers the same logic but the visual would be high-leverage.
- Cross-reference 10.3 LiteLLM Router from 12.3 (cascading) since they solve overlapping problems differently.
- Move section 12.6 to Part IV as its prereqs already point forward into Chapter 13 and 17.
- Add concrete dollar/latency numbers to the 12.4 TCO discussion: "GPT-4o: $0.0025/1K input * 50K queries/day = $X/month vs A100 self-host at $Y/month including ops overhead Z hours."

## One-thing-only fix
Renumber `section-12.6.html` body H2s, image filenames, and caption numbers from `12.8.x` to `12.6.x` (or whatever target number the index actually wants) and reconcile the chapter index entry. Until that is done, the section appears to be from a different chapter and its cross-references are invalid.
