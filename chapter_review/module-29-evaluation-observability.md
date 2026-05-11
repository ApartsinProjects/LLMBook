# Module 29: Evaluation, Experiment Design & Observability

**Audit date**: 2026-05-11
**Sections reviewed**: 29.1, 29.2, 29.3, 29.4, 29.5, 29.6, 29.7, 29.8, 29.9, 29.10, 29.11, 29.12 (12 sections; merged from former Chapters 29 + 30 in v3.2)
**Total word count**: ~80,800 words (raw HTML)

## Summary
The largest chapter in the book by section count, and the most internally inconsistent in this batch. The v3.2 merger of the old "Chapter 30: Observability" into Chapter 29 was clearly a structural rename that did not propagate into the section bodies: most absorbed sections (29.4, 29.5, 29.6, 29.7, 29.8, 29.9, 29.10, 29.11, 29.12) still carry their pre-merger H2 numbers (e.g., `30.5.1`, `29.10.1`, `29.13.1`, `29.14.1`). Code fragments inside many of these sections are also numbered after the *old* chapter (`# Code Fragment 29.9.5: …` in section 29.9), so a reader following inline pointers walks straight off the cliff. The chapter's prose is otherwise high quality and the techniques covered are all current.

## Inconsistencies
- **Stale section-number H2s after the v3.2 merge** (this is the dominant defect):
  - 29.4 has `30.2.1`, `30.2.2`, `30.2.3`, `30.2.4` — should be 29.4.1-29.4.4.
  - 29.5 has `29.6.1` through `29.6.4`.
  - 29.6 has `30.1.1` through `30.1.5`.
  - 29.7 has `30.3.1` through `30.3.4`.
  - 29.8 has `29.10.1` through `29.10.3` (and probably more below).
  - 29.9 has `29.11.1` through `29.11.5`.
  - 29.10 has `30.5.1` through `30.5.4`.
  - 29.11 has `29.13.1` through `29.13.5`.
  - 29.12 has `29.14.1` through `29.14.3`.
- **29.1**: chapter-opener `Figure 29.1.2` (line 47) — no `Figure 29.1.1` exists. The CSS class `figcaption` and the diagram caption later in the section are *also* `Figure 29.1.2` (line 173), creating a duplicate.
- **29.2**: opens with `Figure 29.2.2` (line 38). No `Figure 29.2.1`. The bootstrap procedure diagram (line 211) is *also* `Figure 29.2.2`.
- **29.3**: opens with `Figure 29.3.2` (line 38). No `Figure 29.3.1`. The pyramid diagram (line 80) duplicates `Figure 29.3.2`.
- **29.4**: opens with `Figure 29.4.2` (line 47). No `Figure 29.4.1`. Drift diagram (line 109) is also `Figure 29.4.2`.
- **29.5**: opens with `Figure 29.5.2` (line 37). No `Figure 29.5.1`. Quality-gate diagram (line 98) duplicates `Figure 29.5.2`.
- (The "missing first figure, duplicated second" pattern appears in nearly every section — looks like a templated bug in the chapter-opener generation.)
- **29.6**, code fragment 29.6.1 caption (line 157) reads: "This snippet demonstrates the rag_pipeline, retrieve_documents functions using retrieval, vector search. Notice how the retrieval and generation stages are composed into a single pipeline. Tracing through each step builds the intuition needed when debugging or extending similar systems." — this is generic boilerplate that does not actually describe what the snippet *does* (Langfuse instrumentation), and reads like an LLM-generated padding template.
- **29.8**, code fragments 29.8.1 and 29.8.2 share the *exact same* caption text "Detecting and quantifying position bias in an LLM judge" (lines 120 and 122) — duplicated.
- **29.8**, line 142 says "Code Fragment 29.8.8 implements the G-Eval scoring pipeline" but the actual G-Eval code is 29.8.3 / 29.8.4; 29.8.8 does not exist.
- **29.8**, line 59 prose says "Code Fragment 29.8.3 demonstrates how to detect and quantify position bias" — but 29.8.3 is the G-Eval scoring code; the position-bias code is 29.8.1/29.8.2.
- **29.9** (the most damaged section): line 140 has caption "Code Fragment 29.9.1: Code Fragment 29.9.2: Needle-in-a-Haystack evaluation" — the caption literally contains a duplicated "Code Fragment X:" prefix. The same line 142 contains *six* `<div class="code-caption">` elements collapsed onto one HTML line (29.9.2 through 29.9.7), all inside a single `</div>` sequence. They appear to have been concatenated by a build step and never separated.
- **29.9** code-block headers also drift: `# Code Fragment 29.9.2`, `# Code Fragment 29.9.5`, `# Code Fragment 29.9.7`, `# Code Fragment 29.9.4` are written *inside* the `<pre>` blocks themselves but the surrounding `<div class="code-caption">` calls them 29.9.1, 29.9.2, 29.9.3, etc. — internal vs caption numbering disagree throughout.
- **29.11**, code-block header line 47 reads `# Code Fragment 29.11.2: Setting reproducible seeds for LLM experiments` — but the surrounding caption is `Code Fragment 29.11.1` (line 104). The "1 vs 2" mismatch appears in every code block in 29.11 and 29.12.
- **29.12** has a section header inside a code-block comment: `# Code Fragment 29.14.2: MaxText configuration for Llama-style model on TPU v5p` (still using the pre-merge `29.14` numbering), but the wrapping caption is `Code Fragment 29.14.2a` (line 202) — the `a` suffix is unique in the chapter and looks accidental.
- **Index page** (`index.html`, lines 53-57) says "Observability, monitoring, and reproducibility practices are covered in the companion **Chapter 30**." Chapter 30 was merged into 29, so this sentence is dead-link-style stale.
- **Index page** describes Chapter 29 has 14 learning objectives (line 67-82) — many of those objectives map to the now-merged former Chapter 30 content; readers are not told to expect ~12 sections rather than the more typical ~7.

## Gaps
- The post-merge chapter has **no transition prose** between former-Chapter-29 sections (29.1-29.3) and former-Chapter-30 sections (29.4 onward). After section 29.3 the reader plunges into "drift detection" with no signposting that the topic has shifted from offline evaluation to production observability.
- No "What's Next" footer on most internal sections; navigation between 29.x sections is bare prev/next links only.
- Bibliography sections in 29.4-29.12 are inconsistent — some sections (29.1, 29.2) have full bibliographies; others (29.10, 29.11, 29.12) appear to have only inline links.
- The `Chapter 30` reference in the index sets up an expectation of further reading that does not exist.
- 29.9 (long-context evaluation) does not connect to Chapter 9 inference-optimization content on RoPE scaling, even though it discusses YaRN.

## Errors
- **29.4**, code fragment 29.4.2 caption is "Install langfuse" (line 189) — the caption is the bash command itself, not a description.
- **29.7**, code fragment 29.7.1 caption is "config/experiment.yaml" (line 140) — again, the caption is the filename, not a description of what the file does.
- **29.5**, line 111 prose says "Code Fragment 29.5.3 below implements a quality gate evaluator that enforces these principles" but the actual code is captioned `Code Fragment 29.5.1` (line 231). Fragment 29.5.3 does not exist in the section.
- **29.5**, line 252 says "Code Fragment 29.5.2 shows how to implement prompt regression testing" — actually 29.5.2 (line 322) does match this description, so this reference is correct. (Listed for contrast.)
- **29.11** Cohen's kappa thresholds (line 166): "values below 0.4 indicate poor agreement, 0.4 to 0.6 indicates moderate agreement, and above 0.8 indicates strong agreement". Standard Landis & Koch thresholds are 0.41-0.60 *moderate*, 0.61-0.80 *substantial*, 0.81+ *almost perfect*. The 0.6-to-0.8 band is omitted here, leaving a gap.
- **29.10** says "GenAI Semantic Conventions" (OpenTelemetry); the conventions are still in *experimental* status as of 2025-2026 — chapter does not mention this stability caveat, which matters for production.
- **29.9**: section discusses "the gap between claimed and effective context length" but does not mention the standard Lost-in-the-Middle (Liu et al. 2023) result, which is the canonical citation for this phenomenon.
- **29.12**, MLPerf section: claims "AIPerf benchmarking across six concurrency levels (1 through 64)" — six levels of {1, 2, 4, 8, 16, 32, 64} would be seven values; off-by-one or includes/excludes endpoints unclearly.

## Improvements
- **The single highest-priority fix**: re-number every absorbed-from-Chapter-30 section so H2s use 29.x.y not 30.x.y / 29.13.x / 29.14.x. This is mechanical and should be a one-pass sed-style rename across 29.4, 29.5, 29.6, 29.7, 29.8, 29.10, 29.11, 29.12, plus updating internal cross-references.
- Re-run figure renumbering to fix the "missing 1, duplicated 2" pattern in nearly every section.
- 29.9: split the collapsed code-caption divs at line 142 back into separate `<div>` elements aligned with the actual code blocks above them.
- Replace stub captions ("Install langfuse", "config/experiment.yaml", etc.) with descriptive captions.
- Update the chapter overview in `index.html` to drop the "companion Chapter 30" reference and acknowledge the merger.
- Add a clear visual separator between sec 29.1-29.3 (offline eval) and sec 29.4+ (production observability), e.g., an inter-section callout titled "Part 2: Production Observability".
- 29.11 Cohen's kappa: add the 0.6-0.8 "substantial" band per Landis & Koch.

## One-thing-only fix
Run a global rename across sections 29.4-29.12 to fix every H2 that still uses `30.x.y` or `29.13.x` / `29.14.x` numbering inherited from the pre-v3.2 chapter layout. The existing prose and figure references will then line up, and downstream sections (Chapter 31 etc.) that point into "Chapter 29 sections" stop being subtly wrong. Without this fix, a reader using the H2 headings as their navigation anchor sees a chapter that appears to be sections 29.1-29.3 followed by sections 30.x — internally incoherent.
