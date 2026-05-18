# Six Splits Wave Report

Wave of giant-section splits to drive every targeted section under ~800 lines and 8 h2.

## Summary table

| Original section | Original L | Original h2 | New A | A lines | New B | B lines | Break h2 |
|---|---:|---:|---|---:|---|---:|---|
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html` | 1241 | 11 | `section-0.3a.html` | 563 | `section-0.3b.html` | 803 | 0.3.7 Debugging (line 495) |
| `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html` | 1205 | 14 | `section-3.1a.html` | 749 | `section-3.1b.html` | 583 | 3.1.9 Weight Initialization (line 692) |
| `part-4-training-adaptation/module-17-peft/section-17.5.html` | 1165 | 10 | `section-17.5a.html` | 676 | `section-17.5b.html` | 620 | 17.5.6 Licensing (line 608) |
| `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html` | 1181 | 11 | `section-32.1a.html` | 637 | `section-32.1b.html` | 661 | 32.1.6 Indexing Strategies (line 571) |
| `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html` | 1126 | 11 | `section-35.5a.html` | 763 | `section-35.5b.html` | 480 | 35.5.8 Production Considerations (line 697) |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3b.html` | 1210 | 3 | SKIPPED | n/a | SKIPPED | n/a | only 3 h2; cannot split cleanly along h2 boundaries |

Total: 5 sections split, 1 skipped per task instructions ("if it has fewer than 5 h2, SKIP it and report").

`section-0.3b.html` is at 803 lines (3 over the 800 guideline). The natural break before 0.3.7 Debugging keeps the basic-PyTorch foundation cleanly in A and the debugging+lab+modern-features block in B; pushing the break later would have either bisected a tight conceptual unit or left A oversized.

## Conceptual rationale for break points

- **0.3a** (0.3.1 - 0.3.6): tensors, autograd, nn.Module, data loading, the basic training loop, saving/loading. Ends on a self-contained PyTorch foundation.
- **0.3b** (0.3.7 - 0.3.10 + Exercises): debugging tools, common mistakes, FashionMNIST lab, modern PyTorch (torch.compile, AMP, FSDP). Production-oriented continuation.
- **3.1a** (3.1.1 - 3.1.8): paper history, info-theory framing, high-level architecture, input representation, attention, FFN, residuals, LayerNorm. The structural anatomy of a transformer block (the source even has a marker comment at this point saying "If you need a break, this is a natural stopping point").
- **3.1b** (3.1.9 - 3.1.13 + Exercises): weight init, causal mask, complete forward pass, residual stream information flow, parameter counting. Assembles the parts into a working decoder.
- **17.5a** (17.5.1 - 17.5.5): teacher-student framework, white-box vs. black-box distillation, case studies, small-but-capable models, practical pipeline.
- **17.5b** (17.5.6 - 17.5.8 + Exercises + What Comes Next): licensing constraints, speculative distillation, chain-of-thought distillation.
- **32.1a** (32.1.0 - 32.1.5): knowledge-storage spectrum, why-RAG, ingestion, retrieve-and-generate pattern, context window management, RAG vs. fine-tuning.
- **32.1b** (32.1.6 - 32.1.8 + Exercises + What Comes Next): indexing strategies for large corpora, evaluation and failure modes, RAG vs. long-context.
- **35.5a** (35.5.1 - 35.5.6): why-a-framework, deep dives into LangChain, LlamaIndex, Haystack, side-by-side comparison, framework-vs-from-scratch decision.
- **35.5b** (35.5.8 - 35.5.10 + Exercises + What Comes Next): production hardening, compound AI systems and DSPy, retrieval-layer security.

## Cross-reference rewrite results

A generic anchor-aware rewriter scanned all book HTML files and re-routed every `href="...section-X.Y.html[#anchor]"` reference:
- Hrefs with `#anchor`: routed to whichever new file holds that id (A or B).
- Hrefs without `#anchor`: routed to A (the conceptual entry point).

Total: **121 files** had at least one rewritten reference.

Targeted prev/next nav block rewrites (preserving nav-num and nav-title): **9 sections** (the neighbors of each split).

## Audit comparison

| Priority | Baseline | After splits |
|---|---:|---:|
| P0 | 2 | 0 |
| P1 | 124 | 89 |
| P2 | 70 | 61 |
| **Total** | **196** | **150** |

- **Zero new BROKEN_XREF or DUP_FIGURE_NUM regressions** (the critical checks per task instructions).
- The 2 P0 GIANT_SECTION items (0.3, 3.1) are resolved.
- The 3 P1 GIANT_SECTION items targeted here (17.5, 32.1, 35.5) are resolved.
- 1 GIANT_SECTION P1 remains for 19.3b (intentionally skipped: only 3 h2).
- 1 new P1 emerged: `[DECISION_FRAMEWORK_EARLY] section-35.5b.html:90` (a Real-World Scenario callout sits at 19% of the smaller B file; it is content inherited unchanged from the original 35.5 and would require a content rearrangement to push later in the file, out of scope for a mechanical split).
- Pre-existing P2 issues inherited by the new files (CALLOUT_INTERNAL, CONSECUTIVE_HEADINGS, MISSING_OUTPUT) carried over from original section text; not regressions caused by the split.

## Files produced

```
part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3a.html
part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3b.html
part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1a.html
part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1b.html
part-4-training-adaptation/module-17-peft/section-17.5a.html
part-4-training-adaptation/module-17-peft/section-17.5b.html
part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1a.html
part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1b.html
part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5a.html
part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5b.html
```

## Files deleted

```
part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html
part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html
part-4-training-adaptation/module-17-peft/section-17.5.html
part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html
part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html
```

## Skipped

```
part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3b.html
```
1210 lines but only 3 h2 (PySpark, Delta Lake, Feature Stores). A clean h2-boundary split is not possible; would need a finer-grained restructuring (introducing intermediate h2 headings) that is out of scope for this wave.

## Helper scripts

- `scripts/_split_section_pair.py`: generic split engine.
- `scripts/_run_six_splits.py`: driver describing per-section break points, titles, descriptions, and intro paragraphs.
- `scripts/_fixup_splits_whatsnext.py`: rewrites the auto-generated What's Next text to natural prose.
- `scripts/_restore_seealso_callouts.py`: re-inserts See Also callouts that originally sat between whats-next and bibliography (lost in 17.5 and 35.5 by the generic split).
- `scripts/_six_splits_xref_fix.py`: anchor-aware xref rewriter + targeted prev/next block rewriter.
- `scripts/_fix_six_splits_titles.py`: escapes `&` to `&amp;` in `<title>` tags and fixes 35.5b's "next" link to point to section-36.1.html instead of the module index.
- `scripts/_fix_32_1_biblio_and_navamp.py`: re-inserts the bibliography into 32.1a/b (the original used `<details class="bibliography-collapsible" open="">` which the splitter regex did not match) and escapes `&` to `&amp;` inside `nav-title` spans of every new section.
