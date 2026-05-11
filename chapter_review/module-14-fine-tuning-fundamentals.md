# Module 14: Fine-Tuning Fundamentals

**Audit date**: 2026-05-11
**Sections reviewed**: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7
**Total word count**: ~26,000 prose words (HTML wc ~44,300)

## Summary
The cleanest chapter in this batch by a wide margin. Section numbering is internally consistent (filename = body H2 prefix throughout), the SFT training loop walkthrough is technically accurate (response masking, packing, bf16, flash-attention-2, gradient checkpointing), the prompting-vs-RAG-vs-fine-tuning decision framework is well-argued, and the educational-psychology key-insight callout (Bjork's "desirable difficulty") is a memorable framing for response masking. Few mechanical defects compared to M10-M13.

## Inconsistencies
- `section-14.4.html` has TWO `<h2>` headings numbered "14.4.5": line 447 "Third-Party Fine-Tuning Platforms" and line 681 "Best Practices for API Fine-Tuning". The second should be 14.4.7 (since 14.4.6 "Cost Analysis Framework" is at line 568). This is a real navigation bug because both anchors will collide.
- `section-14.3.html` line 37 figcaption "Figure 14.3.2" is the FIRST figure in section 14.3, before any 14.3.1 has appeared. Off-by-one.
- `section-14.3.html` line 40 references "Code Fragment 14.3.2" in body, but the next code block is the first one and would normally be 14.3.1.
- `section-14.3.html` line 82 "The following implementation (Code Fragment 14.3.2) shows..." - the same wrong number is reused.
- `section-14.3.html` line 46 SVG `aria-label="Diagram: 1. The SFT Training Loop Intermediate"` - auto-generated label leak ("1." and "Intermediate" suffix).
- `section-14.6.html` H2 sequence: 14.6.1, 14.6.2, jump to 14.6.5, 14.6.6 - sections 14.6.3 and 14.6.4 appear to be missing or mis-numbered (multi-label and token-level may exist as H3s but were dropped from H2 hierarchy).
- `section-14.5.html` `<h1>` is on line 22 (off by one from other sections starting at line 21) - cosmetic but indicates inconsistent template.

## Gaps
- 14.5 (Representation Learning) lists three H2s (Why, Encoder vs Decoder, Contrastive Learning) but the index objective bullet mentions "embedding tasks" plural - hard-negative mining, in-batch negatives, and matryoshka embeddings deserve a callout.
- The chapter advertises "Catastrophic forgetting and continual pre-training vs. instruction fine-tuning" in 14.1 but the actual catastrophic-forgetting mitigation toolkit (replay buffers, LoRA-style isolation, EWC) is discussed only briefly; cross-ref to Chapter 15 PEFT would help.
- LoRA/QLoRA are barely mentioned despite being the dominant industrial fine-tuning method in 2026; the chapter defers all of that to Chapter 15 but a one-paragraph "this code path is full FT, see Chapter 15 for the PEFT version that almost everyone actually uses" callout in 14.3 would set reader expectations.
- No mention of Unsloth or torchtune as TRL alternatives despite both having significant 2025 traction.
- Provider Comparison table in 14.4.3 likely needs a refresh: Anthropic Claude fine-tuning was added in 2024-2025; the section already has a 14.4.4 dedicated to it but the comparison table position suggests it was inserted later without reordering.
- Section 14.7 (Long Context) only has 14.7.1 and 14.7.2 visible H2s in this view; "RoPE scaling, position interpolation" promised in objectives needs verifying for depth.

## Errors
- `section-14.3.html` SFTConfig example uses `processing_class=tokenizer` - this is the post-TRL 0.12 API; readers on older TRL will hit `TypeError`. Pin a TRL version in the snippet or call out the version requirement.
- `attn_implementation="flash_attention_2"` requires `flash-attn` installed and a CUDA capability >= 7.5; the snippet does not guard against absence and will raise `ImportError` on machines without flash-attn.
- The Ricardo/comparative-advantage analogy doesn't appear here (that was M12) but the "desirable difficulty" framing in 14.3 cites Bjork 1994 - the paper is correct but the analogy slightly stretches: Bjork's framework is about retrieval practice, not about gradient masking.
- 14.4 OpenAI fine-tuning example needs verification of current API surface (gpt-4o-mini fine-tuning was in beta in 2024, GA in 2025, with format requirements that have shifted).
- Catastrophic-forgetting illustration (14.3.2) is captioned but the visualization shown is actually the response-masking diagram, not catastrophic forgetting - figure caption and image content disagree.

## Improvements
- Renumber `section-14.4.html` line 681 to "14.4.7" to eliminate the duplicate H2 ID.
- Add a "PEFT preview" callout in 14.3 explicitly stating that full fine-tuning is shown for pedagogical clarity but ~90% of production fine-tunes use LoRA (see Chapter 15).
- Add a small "torchtune / Axolotl / Unsloth" library landscape callout in 14.3 to balance the TRL-only treatment.
- Section 14.4 Provider Comparison should be moved to the END of the section (after Anthropic, third-party platforms) so it doesn't preview content the reader has not yet read.
- Add a one-line "what data format does Chapter 13 produce, and how does it map to ChatML used here?" callout in 14.2 to make the inter-chapter handoff explicit.
- Replace the catastrophic-forgetting figure caption with one that matches the response-masking diagram, OR add a separate forgetting figure.

## One-thing-only fix
Renumber the duplicate `<h2>14.4.5</h2>` at line 681 of section 14.4 to its correct position (14.4.7), then sweep the section TOC and any anchor links pointing at 14.4.5. Two H2s with the same ID is the only navigation-breaking defect in an otherwise solid chapter.
