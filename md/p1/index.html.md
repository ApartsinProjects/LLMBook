## Part Overview
Part I establishes the core knowledge you will draw on throughout the rest of the book. We begin with machine learning and PyTorch fundamentals, then move into natural language processing, tokenization, sequence modeling, the Transformer architecture, and text generation. By the end of these six chapters, you will have a solid understanding of how text becomes numbers, how models learn patterns, and how the Transformer produces coherent language.
Chapters: 6 (Chapters 0 through 5) covering approximately 50,000 words of content with hands-on labs, worked examples, and exercises.
Big Picture
Every concept in this book rests on the foundations built here. Part I gives you the mathematical intuition, NLP building blocks, and Transformer fluency needed to understand, use, and customize large language models with confidence.
[Chapter 00 ML and PyTorch Foundations](module-00-ml-pytorch-foundations_index.html.md)
Prerequisite refresher covering core machine learning concepts (supervised learning, loss functions, gradient descent, regularization) and hands-on PyTorch programming. Also introduces reinforcement learning foundations for later RLHF work.
- [0.1 ML Basics: Features, Optimization & Generalization](module-00-ml-pytorch-foundations_section-0.1.html.md)
- [0.2 Deep Learning Essentials](module-00-ml-pytorch-foundations_section-0.2.html.md)
- [0.3 PyTorch Tutorial](module-00-ml-pytorch-foundations_section-0.3.html.md)
- [0.4 Reinforcement Learning Foundations](module-00-ml-pytorch-foundations_section-0.4.html.md)
[Chapter 01 Foundations of NLP and Text Representation](module-01-foundations-nlp-text-representation_index.html.md)
How machines understand text: from bag-of-words and TF-IDF through Word2Vec, GloVe, and contextual embeddings like ELMo and BERT. Builds intuition for dense vector spaces that power all modern NLP.
- [1.1 Introduction to NLP and the LLM Revolution](module-01-foundations-nlp-text-representation_section-1.1.html.md)
- [1.2 Text Preprocessing and Classical Representations](module-01-foundations-nlp-text-representation_section-1.2.html.md)
- [1.3 Word Embeddings: Word2Vec, GloVe and FastText](module-01-foundations-nlp-text-representation_section-1.3.html.md)
- [1.4 Contextual Embeddings: ELMo & the Path to Transformers](module-01-foundations-nlp-text-representation_section-1.4.html.md)
[Chapter 02 Tokenization and Subword Models](module-02-tokenization-subword-models_index.html.md)
The critical bridge between raw text and model input. Covers BPE, WordPiece, Unigram, and SentencePiece tokenizers, with practical guidance on choosing and training tokenizers for your domain.
- [2.1 Why Tokenization Matters](module-02-tokenization-subword-models_section-2.1.html.md)
- [2.2 Subword Tokenization Algorithms](module-02-tokenization-subword-models_section-2.2.html.md)
- [2.3 Tokenization in Practice & Multilingual Considerations](module-02-tokenization-subword-models_section-2.3.html.md)
[Chapter 03 Sequence Models and the Attention Mechanism](module-03-sequence-models-attention_index.html.md)
From RNNs and LSTMs to the attention mechanism that revolutionized NLP. Understand the limitations of recurrent models and why attention became the foundation for Transformers.
- [3.1 Recurrent Neural Networks & Their Limitations](module-03-sequence-models-attention_section-3.1.html.md)
- [3.2 The Attention Mechanism](module-03-sequence-models-attention_section-3.2.html.md)
- [3.3 Scaled Dot-Product & Multi-Head Attention](module-03-sequence-models-attention_section-3.3.html.md)
[Chapter 04 The Transformer Architecture](module-04-transformer-architecture_index.html.md)
Deep dive into the Transformer: multi-head self-attention, positional encoding, feed-forward networks, layer normalization, and the encoder-decoder design. The architecture that powers every modern LLM.
- [4.1 Transformer Architecture Deep Dive](module-04-transformer-architecture_section-4.1.html.md)
- [4.2 Build a Transformer from Scratch](module-04-transformer-architecture_section-4.2.html.md)
- [4.3 Transformer Variants & Efficiency](module-04-transformer-architecture_section-4.3.html.md)
- [4.4 GPU Fundamentals & Systems](module-04-transformer-architecture_section-4.4.html.md)
- [4.5 Transformer Expressiveness Theory](module-04-transformer-architecture_section-4.5.html.md)
[Chapter 05 Decoding Strategies and Text Generation](module-05-decoding-text-generation_index.html.md)
How language models produce text: greedy decoding, beam search, temperature sampling, top-k, top-p (nucleus), and advanced strategies like speculative decoding and structured generation.
- [5.1 Deterministic Decoding Strategies](module-05-decoding-text-generation_section-5.1.html.md)
- [5.2 Stochastic Sampling Methods](module-05-decoding-text-generation_section-5.2.html.md)
- [5.3 Advanced Decoding & Structured Generation](module-05-decoding-text-generation_section-5.3.html.md)
- [5.4 Diffusion-Based Language Models](module-05-decoding-text-generation_section-5.4.html.md)
## What Comes Next
Continue to [Part II: Understanding LLMs](../part-2-understanding-llms/index.html).