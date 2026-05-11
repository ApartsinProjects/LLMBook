# Module 02: Tokenization & Subword Models

**Audit date**: 2026-05-11
**Sections reviewed**: 2.1, 2.2, 2.3
**Total word count**: ~14,000

## Summary
The strongest chapter of the six in this batch. Section 2.1 builds the vocabulary-vs-sequence-length tradeoff carefully and uses concrete numbers (66 char-tokens vs 11 subword tokens for the same sentence). The BPE walkthrough in 2.2 is excellent: pseudocode + working Python + production HF tokenizers shortcut. Section 2.3's coverage of chat templates, fertility, and API cost is the most practical content in Part 1. Tone is tight and the "Token" agent's epigraphs are genuinely funny. The auto-link bug is much less prevalent here than in modules 0-1.

## Inconsistencies
- **Auto-link bug appears once** (`section-2.3.html` line 94): "Used in masked language modeling (**Section 6.1**-style)" — the link text should be "BERT" or "MLM", not the section number.
- **Figure 2.2.2 caption is reused** for two distinct images in `section-2.2.html`: line 81-83 (BPE puzzle factory illustration) and line 142 (BPE merge tree diagram). The diagram on line 142 has alt text "Unigram model selects highest probability segmentation via Viterbi algorithm" — which is for a *different* algorithm entirely. The image was placed under the wrong heading.
- **Figure 2.3.2 caption** ("Special tokens are the traffic cops") appears at line 53 of `section-2.3.html`. A second image is later captioned "Figure 2.3.2: Anatomy of a chat template" implicitly via the same number. Pick distinct numbers.
- **Code Fragment 2.2.12** is numbered out of sequence (the previous fragment is 2.2.4 or so) — looks like an autoincrement that lost track.
- **`section-2.3.html`** Code Fragment 2.3.2 (line 153) says "<a class='cross-ref' …>Llama 3</a> chat template" with an inline link, but Code Fragment 2.3.24 follows immediately (line 179) with no fragment 2.3.3 through 2.3.23 in between.
- **Chapter label inconsistency**: `index.html` says "Chapter 02: Tokenization & Subword Models" but the section files use "Chapter 02: Tokenization and Subword Models". Same fix as in module 0.

## Gaps
- **WordPiece's "MaxMatch" algorithm is named in the chapter index** but never actually defined in section 2.2. The reader is told "WordPiece is a variant of BPE that uses a likelihood-based merge criterion" but the encoding-time longest-match algorithm is missing.
- **Unigram language model with Viterbi decoding** is mentioned three times (chapter index, section 2.2 overview, image alt text) but the Viterbi step is never spelled out. The reader is left guessing how a probabilistic model produces a discrete segmentation.
- **No coverage of how token IDs are assigned**. The text talks about "the merge table" being all you need, but never says how the vocabulary tokens are integer-indexed at the end. A 3-line explanation would close the loop before the embedding-layer connection in chapter 3.
- **`section-2.1.html`** mentions Gemini 1.5 Pro's 1M-token context window "as of 2025". By the book's own 2026 publication date this is mid-stale; Gemini 2.5 supports the same or larger windows now. The hedging language is fine but a small refresh would be nice.
- **Special-token tables in 2.3** list role markers (`<|system|>`, `<|user|>`) but never explain the actual `>` `|` byte-level encoding choice. Readers wonder why special tokens have the `<|...|>` format vs. plain `[CLS]`.
- **Multimodal tokenization** is in the section title but appears to get only a brief mention. The chapter index card promises it.
- **No exercises in any of the three sections.** Modules 0 and 1 had at least Self-Check callouts. The reader leaves chapter 2 with no way to validate understanding.

## Errors
- **`section-2.2.html` line 142** image alt text says "Unigram model selects highest probability segmentation via Viterbi algorithm" but the figure is captioned "Figure 2.2.2: BPE iteratively merges the most frequent character pair." The alt text and the caption describe two different algorithms; one of them is wrong.
- **`section-2.1.html` line 169** sample output for tiktoken on "Tokenization determines the model's vocabulary and sequence length." shows 11 tokens including " determines" with a leading space — this is correct for tiktoken's representation but the rendered list `['Token', 'ization', ' determines', …]` may confuse readers who do not know that tiktoken includes the leading space in tokens. A one-sentence note explaining the leading-space convention would help.
- **`section-2.1.html` line 130** the Information Theory callout asserts "BPE and WordPiece independently rediscover" Shannon's source coding theorem. This overstates the case: BPE was designed for compression with no entropy framing, and WordPiece was framed as likelihood maximization. The "independently rediscover" claim is a stretch and not standard in the literature.
- **The "strawberry has 2 r's" Fun Fact** (`section-2.1.html` line 87) is a folk claim. The actual tokenization of "strawberry" by GPT-4 (cl100k_base) is a single token; the failure is more subtle (no per-character access in the embedding). The Fun Fact's tokenization "['str', 'aw', 'berry']" is illustrative but not what tiktoken actually returns. Either show the real tiktoken output or label it as illustrative.
- **`section-2.2.html` BPE pseudocode** uses Python-like syntax inside an `<algorithm>` callout that has the `lang-python` highlighter applied. Result: tokens like `argmax(a,b) ∈ pairs freq(a, b)` are highlighted as if they were Python identifiers. Switch to `lang-text` for pseudocode.
- **`section-2.3.html`** chat template example outputs (line 172) show double newlines `\n\n` between role markers. The Llama 3 *actual* template uses single newlines; the apply_chat_template output shown adds a blank line that does not appear in real model output. Worth verifying with `transformers` 4.4x.

## Improvements
- **Add a small Unigram-LM walkthrough** with 3-4 steps showing Viterbi picking the best segmentation of a single word. Without this, "top-down vs bottom-up" is just a slogan.
- **Add a per-language tokenizer-comparison table to 2.3** with concrete token-counts for the same UN Declaration sentence in 5 languages × 4 tokenizers (GPT-4, Llama 3, T5, Gemma). The current text describes the fertility issue but does not show it numerically.
- **Code Fragment 2.2.12 and the pseudocode block** would benefit from being placed *next to* the working Python implementation that follows, so readers can map line-by-line. Currently they are separated by ~30 lines of prose.
- **Section 2.2 needs a "fully worked example"** showing the BPE training on `low low low lower lower lowest newest widest` end-to-end with merge table. The corpus is shown (line 200) but the resulting merges and final tokenization of a held-out word are not displayed.
- **Section 2.3's "Tokenizer Equity" callout** (line 39) is excellent but should be paired with a per-language pricing table at the end of the section (price/1k tokens × fertility-multiplier = effective price/equivalent-content). The point lands harder when readers see "Japanese users pay 3.2x more for the same paragraph."
- **Add a Self-Check / Quiz** at the end of each section. The pattern in modules 0/1 is a clear signal; module 2 should match.
- **Replace the strawberry Fun Fact** with a verified example: load tiktoken, encode "strawberry", show the actual tokens, then explain why the LLM still gets character counts wrong (no character-level access during attention).
- **Section 2.3's chat-template pre-block** (line 192-) uses inline color styles. Move these to `book.css` to comply with the "no inline style blocks" rule in CLAUDE.md.

## One-thing-only fix
Fix the Figure 2.2.2 mislabel: the image at line 142 of `section-2.2.html` (alt text "Unigram model selects highest probability segmentation via Viterbi") is labeled as a BPE figure. Either swap the image for the actual BPE merge-tree diagram or move the image to the Unigram subsection where it belongs. This is a content correctness issue, not a polish issue, because the chapter explicitly contrasts BPE vs Unigram.
