> "The first step toward understanding a language is deciding where one word ends and another begins."
>
> ![Token](../../front-matter/images/agents/token.png) [Token](../../front-matter/wisdom-council.html#token), Boundary-Obsessed AI Agent
![Tokenization and Subword Models chapter illustration](images/chapter-opener.png)
**Figure 2.0.1**: Before a language model can read a single word, it must first slice text into pieces; tokenization is the invisible gatekeeper that decides where one "word" ends and the next begins.
## Chapter Overview
Before a language model can process a single word, it must first decide what a "word"
even means. Tokenization is the gateway between raw text and the numerical world of
[neural networks](../module-00-ml-pytorch-foundations/index.html), and the choices made at this stage ripple through every aspect of model
behavior: the languages it handles well, the cost of running it, the errors it makes,
and the size of its context window.
This chapter starts by building intuition for why tokenization matters so much,
exploring the fundamental tradeoff between vocabulary size and sequence length. We then
take a deep dive into the algorithms that power modern tokenizers: Byte Pair Encoding,
WordPiece, Unigram, and their byte-level variants. Along the way, you will implement
BPE from scratch and compare tokenizers across languages and modalities. Finally, we
examine practical concerns: special tokens, chat templates, multilingual fertility,
[multimodal tokenization](../../part-7-multimodal-applications/module-27-multimodal/index.html), and how tokenization directly impacts your API bill.
### Prerequisites
- [Chapter 00: ML & PyTorch Foundations](../module-00-ml-pytorch-foundations/index.html) (basic Python, data structures)
- [Chapter 01: NLP & Text Representation Foundations](../module-01-foundations-nlp-text-representation/index.html) (word embeddings, vocabulary concepts)
- Familiarity with Python string operations and dictionaries
- Basic understanding of probability (for the Unigram model discussion)
### Learning Objectives
- Explain the vocabulary-size tradeoff and how tokenization affects context windows, model cost, and [generation quality](module-05-decoding-text-generation_index.html.md)
- Describe and implement the BPE algorithm, including its merge table and encoding/decoding procedures
- Compare WordPiece, Unigram (with Viterbi decoding), and byte-level BPE in terms of mechanism, strengths, and typical use cases across [modern LLM families](../../part-2-understanding-llms/module-07-modern-llm-landscape/index.html)
- Discuss tokenizer-free models (ByT5, MegaByte) and the tradeoffs of operating directly on bytes
- Analyze multilingual tokenizer fertility, special token conventions, and chat template formats
- Estimate [API costs](../../part-3-working-with-llms/module-10-llm-apis/index.html) from token counts and evaluate tokenizer behavior on diverse inputs
## Sections
- [2.1
  Why Tokenization Matters
  🟢
  📐
  The vocabulary tradeoff, how tokenization shapes context windows and inference cost,
  tokenization artifacts and their downstream effects.](module-02-tokenization-subword-models_section-2.1.html.md)
- [2.2
  Subword Tokenization Algorithms
  🟡
  📐
  🔧
  BPE algorithm and merge tree, WordPiece MaxMatch, Unigram with Viterbi decoding,
  byte-level BPE, tokenizer-free models (ByT5, MegaByte). Lab: train BPE from scratch.](module-02-tokenization-subword-models_section-2.2.html.md)
- [2.3
  Tokenization in Practice & Multilingual Considerations
  🟡
  ⚙️
  🔧
  Special tokens and chat templates, multilingual fertility analysis, multimodal tokenization,
  API cost estimation. Lab: compare tokenizers across languages and models.](module-02-tokenization-subword-models_section-2.3.html.md)
### What's Next?
In the next section, [Section 2.1: Why Tokenization Matters](module-02-tokenization-subword-models_section-2.1.html.md), we explore why tokenization choices matter so deeply for model performance, vocabulary efficiency, and multilingual coverage.
📚 Bibliography & Further Reading
### Foundational Papers
Gage, P. (1994). "A New Algorithm for Data Compression." *C Users Journal*, 12(2), 23–38. [Wikipedia: Byte Pair Encoding](https://en.wikipedia.org/wiki/Byte_pair_encoding)
The original BPE algorithm for data compression, later adapted by Sennrich et al. for subword tokenization in NLP.
Sennrich, R., Haddow, B., & Birch, A. (2016). "Neural Machine Translation of Rare Words with Subword Units." *ACL 2016*. [arxiv.org/abs/1508.07909](https://arxiv.org/abs/1508.07909)
Applies BPE to machine translation, demonstrating that subword tokenization elegantly handles rare and compound words.
Kudo, T. (2018). "Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates." *ACL 2018*. [arxiv.org/abs/1804.10959](https://arxiv.org/abs/1804.10959)
Introduces the Unigram language model tokenizer and subword regularization, showing that sampling multiple segmentations improves robustness.
Schuster, M. & Nakajima, K. (2012). "Japanese and Korean Voice Search." *IEEE ICASSP 2012*. [doi.org/10.1109/ICASSP.2012.6289079](https://doi.org/10.1109/ICASSP.2012.6289079)
Introduces the WordPiece algorithm used in BERT and many Google models for vocabulary construction.
Xue, L. et al. (2022). "ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models." *TACL*, 10, 291–306. [arxiv.org/abs/2105.13626](https://arxiv.org/abs/2105.13626)
Explores tokenizer-free models that operate directly on UTF-8 bytes, trading longer sequences for elimination of vocabulary-related biases.
Yu, L. et al. (2023). "MEGABYTE: Predicting Million-Byte Sequences with Multiscale Transformers." *NeurIPS 2023*. [arxiv.org/abs/2305.07185](https://arxiv.org/abs/2305.07185)
Proposes a multi-scale architecture for byte-level modeling, enabling efficient processing of very long byte sequences.
### Key Books
Jurafsky, D. & Martin, J. H. (2024). *Speech and Language Processing* (3rd ed. draft), Chapter 2: Regular Expressions, Text Normalization, Edit Distance. [web.stanford.edu/~jurafsky/slp3/2.pdf](https://web.stanford.edu/~jurafsky/slp3/2.pdf)
Covers text normalization, word segmentation, and the linguistic foundations of tokenization in an accessible format.
Kudo, T. & Richardson, J. (2018). "SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing." *EMNLP 2018*. [arxiv.org/abs/1808.06226](https://arxiv.org/abs/1808.06226)
Describes the SentencePiece library that implements BPE and Unigram tokenization in a language-agnostic manner, used by many modern LLMs.
### Tools & Libraries
Hugging Face Tokenizers. [github.com/huggingface/tokenizers](https://github.com/huggingface/tokenizers)
A fast, Rust-backed tokenizer library supporting BPE, WordPiece, and Unigram, with Python bindings and integration into the Transformers ecosystem.
tiktoken: OpenAI's fast BPE tokenizer. [github.com/openai/tiktoken](https://github.com/openai/tiktoken)
OpenAI's open-source BPE tokenizer used by GPT-3.5 and GPT-4, useful for estimating token counts and API costs.
SentencePiece. [github.com/google/sentencepiece](https://github.com/google/sentencepiece)
Google's unsupervised text tokenizer supporting BPE and Unigram models, used in T5, LLaMA, and many multilingual models.