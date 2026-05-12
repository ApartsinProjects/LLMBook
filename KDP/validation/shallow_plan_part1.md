# Shallow Audit Plan: Part I (Chapters 0-5)

**Total findings: 70**
**Date:** 2026-05-12

## DOMINANT FINDING: Cross-cutting "Section X.Y" Broken Label Bug

**14 of 70 findings.** A previous auto-linker pass replaced concept-name strings with cross-reference labels but never substituted back the actual concept name. Now bare "Section 4.1" / "Section 6.1" / "Section 8.1" text appears in places where "Cross-Entropy Loss" / "Softmax" / "BERT" / "chain-of-thought" was intended. **Same systemic issue identified in Parts II+III, V+VI.** Book-wide fix needed.

Examples in Part I:
- `section-0.1.html` line 129: "the standard is Section 4.1 Loss" → should be "Cross-Entropy Loss"
- `section-0.2.html` line 88 (activation table row): `<strong>Section 4.1</strong>` → should be `<strong>Softmax</strong>`
- `section-0.2.html` line 198: "consider Section 4.1 instead" → "consider Layer Normalization instead"
- `section-4.3.html` line 186: "RoPE has become the dominant Section 4.1 in modern LLMs" → "dominant positional encoding scheme"
- `section-4.3.html` line 343: "information propagates through Section 4.1 across layers" → "through attention layers"
- `section-4.3.html` line 351: "Linear attention replaces the Section 4.1 kernel" → "replaces the softmax kernel"
- `section-4.3.html` line 385: "With standard Section 4.1 and many heads" → "With standard multi-head attention"
- `section-4.3.html` (BERT section): "Section 6.1 (Devlin et al., 2018)" → "BERT (Devlin et al., 2018)"
- `section-4.4.html` (operations table): row label "Section 4.1" → "Softmax"

**Action:** book-wide grep + manual disambiguation pass.

## OTHER HIGH-PRIORITY FINDINGS

| # | File | Issue |
|---|---|---|
| 9 | section-0.4 | PPO L^CLIP formula absent. Foundational for RLHF. |
| 10 | section-0.4 | KL penalty formula absent. Same section. |
| 11 | section-0.4 | REINFORCE/PPO code indentation bug — methods nested in __init__. |
| 32 | section-4.1 | Information theory pointer-only (no inline perplexity definition). |
| 35, 47, 51 | sections 4.1, 4.4, 5.1 | Code indentation bugs across multiple files. |

## MEDIUM-PRIORITY MISSING-INTUITION

- WordPiece scoring formula (section-2.2)
- Viterbi algorithm named without explanation (section-2.2)
- GRU update gate simplification (section-3.1)
- MHA tensor-shape trace (section-3.3)
- Beam search "curse" mechanism (section-5.1)
- Typical sampling worked example (section-5.2)
- Speculative decoding rejection sampling numeric (section-5.3)

## MISSING-FAILURE-MODE additions worth making

- Word2Vec bias / WEAT warning (section-1.3)
- Attention is not interpretation (Jain & Wallace 2019) — section-3.3
- BPE tokenizer corpus-specificity (section-2.2)
- Repetition penalty extreme values break grammar (section-5.2)
- Diffusion LM logical-coherence gap (section-5.4)

## CROSS-CUTTING CODE INDENTATION BUG

5 sections (0.4, 4.1, 4.4, 5.1) plus bugs in Parts II+III have HTML pre-block rendering that nests methods inside __init__. Likely fix at HTML build pipeline (stray leading whitespace handling).

## SECTIONS RATED GOOD (~10)

0.2 (most), 0.3, 1.1, 1.2 (most), 1.4, 2.1, 2.3 (most), 3.1, 3.2, 3.3 (most), 4.1 (most), 4.2 (most), 4.4 (most), 4.5, 5.1 (most), 5.2 (most), 5.3 (most), 5.4 (most).

Part I has strong foundational content; all real failures are mechanical artifacts (broken labels, indentation, missing forward refs).
