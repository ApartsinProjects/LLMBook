# Chapter Plan: Module 02 - Tokenization & Subword Models

## Scope

**What this chapter covers:**
- Why tokenization is the critical bridge between raw text and neural network input
- The vocabulary size tradeoff and its impact on context windows, inference cost, and generation quality
- Three core subword tokenization algorithms: Byte Pair Encoding (BPE), WordPiece, and Unigram
- Byte-level BPE and its role in modern tokenizers (GPT-2 onward)
- Tokenizer-free models (ByT5, MegaByte) as a research frontier
- Practical concerns: special tokens, chat templates, multilingual fertility, multimodal tokenization
- API cost estimation from token counts

**What this chapter does NOT cover:**
- Sentence segmentation or linguistic parsing (covered tangentially in Module 01)
- Full implementation of SentencePiece C++ internals
- Token embedding layers and positional encodings (covered in Module 03)
- Attention mechanisms over token sequences (covered in Module 03)
- Fine-tuning or vocabulary extension strategies (covered in later modules on fine-tuning)

## Learning Objectives

1. Explain the vocabulary-size tradeoff and how tokenization affects context windows, model cost, and generation quality
2. Describe and implement the BPE algorithm, including its merge table and encoding/decoding procedures
3. Compare WordPiece, Unigram (with Viterbi decoding), and byte-level BPE in terms of mechanism, strengths, and typical use cases
4. Discuss tokenizer-free models (ByT5, MegaByte) and the tradeoffs of operating directly on bytes
5. Analyze multilingual tokenizer fertility, special token conventions, and chat template formats
6. Estimate API costs from token counts and evaluate tokenizer behavior on diverse inputs

## Prerequisites

- **Module 00: ML & PyTorch Foundations** (basic Python, data structures, working with dictionaries and loops)
- **Module 01: NLP & Text Representation Foundations** (word embeddings, vocabulary concepts, the idea of mapping text to numbers)
- Familiarity with Python string operations and dictionaries
- Basic understanding of probability (for the Unigram model discussion)

## Chapter Structure

### Section 2.1: Why Tokenization Matters (~3,000 words)
**Level:** Basic / Fundamentals

- **Key concepts:**
  - The "invisible gateway" between raw text and model input
  - Vocabulary size spectrum: character-level, subword, word-level
  - The core tradeoff: smaller vocabulary = longer sequences; larger vocabulary = sparser embeddings
  - Context window consumption and the "token tax" on non-English languages
  - Cost arithmetic: how token count translates to API bills
  - Tokenization artifacts: inconsistent splitting, arithmetic failures, trailing spaces, code tokenization
  - Practical implications for builders

- **Diagrams needed:**
  1. Figure 2.1: Vocabulary size spectrum (character to word) showing the subword sweet spot
  2. Figure 2.2: Context window consumption across languages (same greeting, different token counts)
  3. Figure 2.3: Tokenization artifact propagation pipeline (how splitting errors cascade)

- **Code examples:**
  1. Comparing tokenization granularities (character, word, subword) on sample text
  2. Demonstrating the multilingual "token tax" with tiktoken
  3. Context-sensitive tokenization inconsistencies
  4. Code tokenization with tiktoken

- **Exercises:** 5 (comprehension and short-answer)
  - Vocabulary tradeoff reasoning
  - Token count comparison across languages
  - Identifying tokenization artifacts
  - Cost estimation problem
  - Explaining downstream effects of tokenization choices

---

### Section 2.2: Subword Tokenization Algorithms (~5,000 words)
**Level:** Intermediate / Fundamentals + Lab

- **Key concepts:**
  - Overview: why subword methods exist and the three families
  - **BPE (Byte Pair Encoding):**
    - Training algorithm (iterative most-frequent-pair merging)
    - Merge table as the core data structure
    - Encoding new text with learned merges
  - **WordPiece:**
    - Likelihood-based merge criterion (mutual information)
    - MaxMatch inference algorithm
    - Comparison with BPE
  - **Unigram Language Model:**
    - Top-down pruning approach (start large, remove low-impact tokens)
    - Viterbi decoding for optimal segmentation
    - Probabilistic nature and multiple possible segmentations
  - **Byte-Level BPE:**
    - The 256-byte base alphabet
    - How it eliminates unknown characters
    - Adoption in GPT-2, GPT-3, GPT-4
  - **Tokenizer-Free Models:**
    - ByT5: operating directly on UTF-8 bytes
    - MegaByte: hierarchical byte-level processing
    - Tradeoffs: robustness vs. sequence length and compute cost

- **Diagrams needed:**
  1. Figure 2.4: BPE merge process step-by-step (pair frequency, merge, update)
  2. Figure 2.5: Unigram segmentation lattice with Viterbi path
  3. Figure 2.6: Byte-level BPE byte-to-token merging process

- **Code examples:**
  1. Full BPE implementation from scratch (Lab): counting pairs, merging, building merge table
  2. Encoding new text using learned BPE merge table
  3. Simulated WordPiece MaxMatch tokenization

- **Exercises:** 5 (conceptual and coding)
  - Tracing BPE merges by hand
  - Explaining why WordPiece and BPE can produce different splits
  - Unigram segmentation reasoning
  - Byte-level BPE on a multilingual example
  - Comparing tokenizer-free tradeoffs

---

### Section 2.3: Tokenization in Practice & Multilingual Considerations (~4,500 words)
**Level:** Intermediate / Engineering + Lab

- **Key concepts:**
  - **Special tokens:** BOS, EOS, PAD, UNK, SEP, MASK, and model-specific tokens
  - **Chat templates:**
    - ChatML format (OpenAI-style)
    - Llama 3 chat format
    - Using Hugging Face `apply_chat_template`
    - Why using the correct template matters
  - **Multilingual fertility analysis:**
    - Definition of fertility (tokens per word or per character)
    - Measuring fertility across languages
    - Equity implications: non-English users pay more, get less context
  - **Multimodal tokenization:**
    - Image tokenization via patch embedding (ViT-style)
    - Audio tokenization (codec models, Whisper)
    - Token budget impact of multimodal inputs
  - **API cost estimation:**
    - Input vs. output token pricing
    - Building a cost estimation utility
    - Cost reduction strategies (shorter prompts, caching, model selection)
  - **Lab: Head-to-head tokenizer comparison** across models and languages

- **Diagrams needed:**
  1. Figure 2.7: Chat template anatomy (system, user, assistant delimiters)
  2. Figure 2.8: Image patch embedding to token sequence pipeline
  3. Figure 2.9: Tokenizer landscape (which algorithm each major model family uses)

- **Code examples:**
  1. ChatML template structure
  2. Llama 3 chat template
  3. Using Hugging Face `apply_chat_template` in Python
  4. Multilingual fertility comparison lab (tiktoken + HuggingFace tokenizers)
  5. API cost estimation utility
  6. Head-to-head tokenizer comparison lab

- **Exercises:** 5 (applied and analytical)
  - Constructing a chat template for a given conversation
  - Computing fertility ratios for given text samples
  - Estimating API costs for a multi-turn conversation
  - Analyzing tokenizer behavior on edge cases (emoji, code, URLs)
  - Recommending a tokenizer for a specific use case

---

## Terminology Standards

| Term | Usage |
|---|---|
| **token** | The atomic unit a model processes; may be a character, subword, word, or byte sequence |
| **tokenizer** | The algorithm (and its trained artifacts) that converts raw text into a sequence of token IDs |
| **vocabulary** | The complete set of tokens a tokenizer can produce, each mapped to a unique integer ID |
| **merge** (BPE) | One step of BPE training where the most frequent adjacent pair is combined into a new token |
| **merge table** | The ordered list of all merges learned during BPE training |
| **fertility** | The ratio of tokens to words (or characters) for a given text; measures tokenizer efficiency |
| **special token** | A reserved token with a control function (e.g., BOS, EOS, PAD) rather than text meaning |
| **chat template** | A formatting convention that wraps conversation turns with special tokens for instruction-tuned models |
| **byte-level BPE** | A BPE variant that uses 256 raw byte values as the base alphabet, eliminating unknown characters |
| **Unigram model** | A tokenization method that selects the highest-probability segmentation from a trained token distribution |
| **WordPiece** | A subword method (used by BERT) that merges pairs maximizing likelihood gain |
| **MaxMatch** | The greedy left-to-right inference algorithm used by WordPiece |
| **Viterbi decoding** | A dynamic programming algorithm for finding the optimal segmentation in the Unigram model |

## Cross-References

- **Builds on:**
  - Module 00: ML & PyTorch Foundations (Python fluency, data structures)
  - Module 01: NLP & Text Representation Foundations (word embeddings, vocabulary concepts, text-to-number mapping)

- **Referenced by:**
  - Module 03: Sequence Models & Attention (token embeddings as input to attention layers, positional encoding over token sequences)
  - Module 04+: Any module involving prompt engineering, fine-tuning, or cost optimization (token counting, template formatting)
  - Part II modules on Transformer architecture (embedding layers sized to vocabulary)
  - Part III/IV modules on fine-tuning (vocabulary extension, tokenizer retraining considerations)

## Estimated Total Length

~12,500 words across all three sections, plus code examples and exercises. This falls within the 8,000 to 15,000 word target range.

## Production Notes

- All code examples use `tiktoken` (OpenAI) and `transformers`/`tokenizers` (Hugging Face) as the primary libraries
- SVG diagrams are embedded inline in the HTML for portability
- Each section ends with a "Check Your Understanding" exercise block and a "Key Takeaways" summary
- Voice is warm and conversational: explain the "why" before the "how," use analogies, and address the reader directly
- No em dashes or double dashes anywhere in the text
