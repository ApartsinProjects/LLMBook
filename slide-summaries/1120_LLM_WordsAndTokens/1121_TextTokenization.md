# 1121_TextTokenization — Per-Slide Summary

**Source file:** `1121_TextTokenization.pptx`
**Source folder:** `SlidesPool/1120_LLM_WordsAndTokens/`
**Drive link:** https://drive.google.com/file/d/1BNXlMcR4ynvstN6SQkBl05_v60ubJRhk/view
**Slide count (exact, via python-pptx):** 13
**Extraction:** Local parse + slide PNG render. Many slides are code-screenshot-heavy; this text-only pass relies on titles and bullet content.

---

## Slide 1 — Tokenization
Title slide for the lecture on text tokenization.

## Slide 2 — Words and Tokens
Image-only slide that visually motivates the difference between an intuitive "word" and a model-facing "token", setting up the distinction the rest of the deck operationalizes.

## Slide 3 — Tokenization + Encoding
A two-step pipeline-illustration slide showing that tokenization (splitting text into pieces) is followed by encoding (assigning integer IDs that the model actually consumes).

## Slide 4 — Naïve tokenization: white-space splitting (notice punctuation)
The simplest baseline: split on whitespace. The slide highlights its primary failure mode — punctuation glued to words ("hello," "world!") becomes its own confusing token.

## Slide 5 — Split by a pattern using regular expressions
Step up from whitespace splitting: use a regex to capture word characters and punctuation separately. Code screenshots illustrate the pattern and its output.

## Slide 6 — Create Vocabulary
After splitting, build a fixed vocabulary from the training corpus. The crucial problem highlighted: "Can't process documents that have unseen tokens" — the open-vocabulary problem that drives every later technique in this deck.

## Slide 7 — Off-the-shelf tokenizers: Spacy, NLTK
Practical shortcut: library tokenizers (Spacy, NLTK) come with vocabularies trained on huge corpora, sparing you the build-it-yourself step.

## Slide 8 — Special tokens
Introduce non-word tokens that carry structural meaning: `<|pad|>` to pad short sentences to a fixed length, `<|sep|>` to separate two documents (useful for similarity tasks), `<|endoftext|>` to mark document boundaries. Each model defines its own special tokens, added to the tokenizer's vocabulary.

## Slide 9 — Clean and reduce the vocabulary
Classical text-cleaning steps to shrink the vocabulary: case folding (Case = case), stemming (working → work), lemmatization (best → good), and stop-word removal ("this", "it"). The slide notes that these are essential for statistics-based features but *usually not used* with modern LLMs — a crucial pedagogical point that explains why students will see these techniques in classical NLP textbooks but rarely in current code.

## Slide 10 — Sub-word tokenizer
The central conceptual move of the lecture. Three options: *word-level* (one token per word, but explodes the vocabulary and treats `work`, `working`, `worked`, `works` as unrelated), *character-level* (tiny vocabulary but individual tokens carry no semantic information), and the *sub-word* compromise that balances both. BPE (Byte-Pair Encoding) is named as the canonical sub-word algorithm used in GPT-2/GPT-3.

## Slide 11 — Byte-Pair Encoding / Tokenizer
The BPE algorithm. Start with characters as the only tokens. Iteratively (a) find the most frequent adjacent token pair, (b) create a new token for that pair, (c) replace its occurrences in the text. The size of the dictionary is controlled by the number of iterations; smaller (character-level) tokens remain in the dictionary, which is what lets BPE encode unknown words. Distinction is made between mid-word and end-of-word tokens (e.g., `er` vs. `er\w`). At parse time, learned merge rules are applied *in the order they were learned* (BPE remembers rank) until no merge applies.

## Slide 12 — Pretrained BPE tokenizer
A walkthrough (seven code screenshots) showing how to use a pretrained BPE tokenizer in practice — loading the tokenizer, encoding text, inspecting the resulting token IDs and decoded tokens.

## Slide 13 — WordPiece Tokenizer
The BERT-family alternative to BPE. Almost identical to BPE but uses *relative* frequency instead of raw frequency to choose merges, and marks within-word continuation tokens with `##` (e.g., `unhappy` → `un` `##happy`). This `##` convention is a recurring visual signature anywhere you see HuggingFace BERT outputs.

---

## Deck-level takeaway

A focused 13-slide tour of tokenization that walks the reader from the most naive splitter (whitespace) to modern sub-word algorithms used by current LLMs (BPE in GPT, WordPiece in BERT). The pedagogical signature is the explicit handling of the *open-vocabulary problem*: every technique in the deck is motivated by what happens when the model encounters a word it has never seen, and sub-word tokenization is presented as the resolution that has won out. Classical preprocessing steps (stemming, lemmatization, stop-word removal) are mentioned and then explicitly relegated to legacy status, which is exactly the kind of "here's what you'll see in old code and why we don't do it anymore" framing that helps a reader navigate the field's history.
