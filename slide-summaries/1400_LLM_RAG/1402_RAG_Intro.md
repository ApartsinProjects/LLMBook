# 1402_RAG_Intro — Per-Slide Summary

**Source file:** `1402_RAG_Intro.pptx`
**Source folder:** `SlidesPool/1400_LLM_RAG/`
**Drive link:** https://drive.google.com/file/d/1u4bBnYmpXpmE7EvnIHHmILifj34IvcJO/view
**Slide count (exact, via python-pptx):** 22
**Extraction:** Local parse + slide PNG render. Several slides are diagram/code-only and inferred from titles + context.

---

## Slide 1 — RAG
Title slide for the introduction to Retrieval-Augmented Generation.

## Slide 2 — Injecting knowledge to LLM
The motivating problem: LLMs need knowledge to follow instructions and answer questions. There are two existing knowledge sources, each with a defect. *Parametric* knowledge is baked into the LLM's weights — public knowledge during pretraining, domain-specific knowledge during fine-tuning — but updating it requires retraining, the amount of knowledge per parameter is limited, and the storage is opaque (leading to hallucination). *In-context* knowledge is supplied directly in the prompt and is therefore always up-to-date, but the context window is bounded (200K-1M tokens, roughly 2500 pages). The driving example: "How to build a chatbot that answers questions based on the *newest* patent applications" — neither option works cleanly.

## Slide 3 — Retrieval Augmented Generation
The RAG resolution: retrieve relevant chunks at query time and inject them into the prompt, getting parametric LLM fluency *combined with* in-context freshness. A diagram (one embedded image) illustrates the retrieve-then-generate flow.

## Slide 4 — RAG: key components
A reference diagram of the four-component RAG architecture (one embedded image): an index of documents, a retriever that fetches relevant chunks for a query, a generator (LLM) that consumes the chunks + the query, and the loop that connects them.

## Slide 5 — RAG in transformers library
The HuggingFace transformers library has a built-in `RAG` model. Default configuration: DPR retriever pretrained on Wikipedia QA, BART generator, jointly fine-tuned on various QA datasets. One code screenshot.

## Slide 6 — RAG in LangChain
LangChain's RAG pipeline. The slide highlights the *recursive splitter*: split documents recursively along a hierarchy of pre-allocated delimiters (paragraph → sentence) while aiming for a fixed chunk size. Speaker notes include "import", suggesting the slide demonstrates module imports for the LangChain RAG pipeline.

## Slide 7 — Fine-Tune domain-specific sentence embedding similarity
Title spells out the technique: use a contrastive loss + Siamese architecture to fine-tune a sentence-similarity model on domain data, then use the resulting encoder for both query and document embedding. The point: out-of-the-box embeddings often fail on specialized vocabulary.

## Slide 8 — DPR: Dense Passage Retrieval
The canonical neural retriever used by the HuggingFace RAG model. *Dual encoders* (separate encoders for questions and answers), making it a *bi-encoder* (two sets of weights, in contrast to a cross-encoder). Trained with contrastive loss.

## Slide 9 — DPR in Python
Code screenshot showing how to use pretrained DPR models from HuggingFace.

## Slide 10 — DPR-based RAG
Code-heavy slide (three embedded images) building an end-to-end DPR-based RAG: encode the corpus once, encode the query at inference, retrieve nearest passages, hand the top-k to the generator.

## Slide 11 — RAG prompt Engineering
Two prompt-engineering rules for RAG: explicitly *instruct the model to use the supplied sources* (otherwise it may answer from parametric knowledge and ignore them) and make *query intent explicit* (e.g., "Answer based only on the following passages" rather than just pasting them).

## Slide 12 — Chunking Strategies
The chunk-size trade-off. *Short chunks* focus tightly on a specific subject but may lack the semantic context needed for a good match. *Long chunks* carry more context but may be too broad to match a focused query. Two illustrative diagrams.

## Slide 13 — Code Representation: Abstract Syntax Trees
A bridge slide: when the documents being retrieved are *code*, the natural unit is not a paragraph but a syntactic unit (function, class, block). ASTs give structured access to those units. Two illustrative diagrams.

## Slide 14 — Structural format-specific chunking
The general principle: use the document's structure to choose chunk boundaries. For code, use AST units; the slide names `tree-sitter` as a multi-language AST parser that makes this practical.

## Slide 15 — Document Chunking in LangChain
LangChain's chunkers in practice: recursive splitting along a prioritized list of separators (lines → sentences → words) targeting a fixed character-count chunk size, plus a sentence-level chunker that groups 5 sentences per chunk. Two code screenshots.

## Slide 16 — Multi-document and metadata-filtered Retrieval
Two retrieval extensions used in real systems: retrieve *k* chunks (not just one) and *filter retrieval by metadata* (e.g., only consider documents tagged with a particular date range, source, or category).

## Slide 17 — Reranking in retrieval postprocessing
A two-stage retrieval: first retrieve candidates cheaply by embedding similarity, then re-rank (and drop irrelevant) candidates by a more expensive content-aware model. This is the standard pattern when you want recall from cheap retrieval and precision from a heavier model.

## Slide 18 — LangChain Reranker
Two concrete LangChain rerankers. *Compressor*: reduce, summarize, or filter the document set before passing to the LLM. *LLMReranker*: feed both the query and each retrieved document into the LLM and ask it to rerank; the generator then receives chunks in the new order, with some dropped.

## Slide 19 — Memory-Augmented RAG
Real conversations are dialogs, so the retrieved context is not just the user's *current* question — it must include relevant *previous turns*. Memory-augmented RAG adds dynamic storage for tracking conversation context, retrieves from it alongside the document corpus, and injects both into the prompt.

## Slide 20 — Memory Augmented RAG: question-answering
A worked example (one embedded image) of memory-augmented RAG in action on a Q&A dialog.

## Slide 21 — Errors in RAG
A section divider before discussing the canonical RAG failure modes (likely missing retrieval, hallucinated source, irrelevant chunks).

## Slide 22 — LLM adaptation strategies
The closing slide places RAG inside the broader space of *LLM adaptation strategies* (one summary image): prompt engineering, fine-tuning, RAG, and combinations of these — giving the reader a mental map of where RAG fits and when an alternative would be more appropriate.

---

## Deck-level takeaway

A 22-slide construction of Retrieval-Augmented Generation from the ground up: motivation (parametric vs. in-context limits) → architecture (retriever + index + generator) → libraries (HuggingFace RAG, LangChain) → the dense retriever (DPR) → all the practical knobs that turn a toy RAG into a working one (prompt engineering, chunking strategies including AST-based code chunking, multi-document retrieval, metadata filtering, two-stage reranking, conversation memory). The pedagogical signature is that every concept is paired with a working code snippet from either HuggingFace or LangChain, making this less a theory deck and more an opinionated walkthrough of "how you actually build one of these".
