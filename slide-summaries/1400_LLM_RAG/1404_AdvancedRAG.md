# 1404_AdvancedRAG — Per-Slide Summary

**Source file:** `1404_AdvancedRAG.pptx`
**Source folder:** `SlidesPool/1400_LLM_RAG/`
**Drive link:** https://drive.google.com/file/d/1eh_xykUPEriX9nuz1Y7yDulYqbPxLSC7/view
**Slide count (exact, via python-pptx):** 56
**Extraction:** Local parse + slide PNG render. Bullets carry the conceptual flow across six advanced RAG technique families.

---

## Slide 1 — Advanced RAG Techniques
Title slide for the deck on advanced RAG techniques.

## Slide 2 — 1. Indirect Embeddings
Section divider for HyDE / HyPE.

## Slide 3 — HyDE: Hypothetical Document Embedding
Sub-section divider for HyDE.

## Slide 4 — Query Expansion via hypothetical answer
HyDE generates a hypothetical answer to the user query with an LLM and embeds that answer (not the raw query) for retrieval, making the query semantically richer.

## Slide 5 — HyPE: Hypothetical Prompt Embedding
Sub-section divider for HyPE.

## Slide 6 — HyPE
HyPE indexes documents by hypothetical questions / prompts generated from them, so a user query matches questions that were pre-derived from the documents.

## Slide 7 — Hypothetical Questions Prompt
A screenshot of the prompt used to generate hypothetical questions per document.

## Slide 8 — LangChain HyDE
Code screenshot showing HyDE as a LangChain retriever.

## Slide 9 — 2 Context Compression
Section divider for context compression (Summarization / MMR).

## Slide 10 — Context Compression Via Summarization/Filtering
Sub-section divider.

## Slide 11 — Context Summarization
Compressor prompt: "Extract only the key facts relevant to answering questions from the text below". Summarize each document individually.

## Slide 12 — Filter with embedding
Two stages: retrieval by distance approximation, then advanced summarize-embed-filter step.

## Slide 13 — MMR: Maximal Marginal Relevance
Sub-section divider for MMR.

## Slide 14 — MMR Filtering
MMR greedily picks chunks that are both relevant to the query and diverse from already selected chunks (different embeddings).

## Slide 15 — Combining Compressors
A figure showing summarization, embedding filter, and MMR composed in a pipeline.

## Slide 16 — LangChain: MMR Retrieval
Code screenshot of MMR retrieval in LangChain.

## Slide 17 — 3. Fusion Methods
Section divider for fusion methods (Multi-hop, Input Fusion, FiD).

## Slide 18 — 3.1 Multi-Hop RAG
Sub-section divider for multi-hop RAG via question decomposition.

## Slide 19 — Multi-Hop Retrieval
A figure illustrating multi-hop retrieval.

## Slide 20 — Decomposing Question
A figure showing the LLM-driven decomposition of a complex question into sub-questions.

## Slide 21 — 3.2 RAG Fusion
Sub-section divider for RAG-Fusion.

## Slide 22 — Background: Reciprocal Rank Fusion
RRF fuses search results from multiple sources where the same document may appear in several; the fused score is the sum of reciprocal ranks across sources.

## Slide 23 — RAG-Fusion
RAG-Fusion generates multiple versions of the user question with an LLM and retrieves documents with all versions, fusing the results.

## Slide 24 — RAG Fusion: Question Generation
A figure showing how an LLM produces multiple reformulations of the question.

## Slide 25 — LangChain: MultiQueryRetrieval
LangChain's MultiQueryRetriever wraps the LLM-based multi-reformulation pattern.

## Slide 26 — 3.2 Fusion-In-Decoder (FID)
Sub-section divider for FiD.

## Slide 27 — RAG Context fusion (for generation)
Three fusion options. Input fusion concatenates retrieved documents into a single context (limited by context window). Output fusion runs generation separately on each document and fuses the answers (by score or LLM judge). Fusion-in-Decoder uses an encoder-decoder generator (T5) to fuse many retrieved documents at the cross-attention layer.

## Slide 28 — Fusion-in-Decoder
FiD encodes every (query, retrieved passage) pair with the encoder, concatenates the resulting embeddings, and lets the decoder generate from the combined input. It can be fine-tuned on a domain-specific dataset.

## Slide 29 — 4. Self-validation and correction
Section divider for LLM-validation, Self-RAG, and CRAG.

## Slide 30 — 4.1 Simple LLM-based Validation
Sub-section divider.

## Slide 31 — Retrieval validations
Use an LLM to check the relevance of retrieved documents before generation and drop the irrelevant ones.

## Slide 32 — 4.2 SELF-RAG
Sub-section divider.

## Slide 33 — Motivation
Self-RAG makes decisions and validations during generation: should we retrieve at all? Is a retrieved document relevant to the query? Is the generated response supported by the document? Is the response helpful given the query? These decisions are framed as "reflection tokens" with binary or scaled answers; the model is trained to emit them, and decoding inspects their probabilities. At inference, fetch documents and reflect (relevancy / support yes-no), generate the next sentence and reflect (usefulness 1..5), and run beam search using the reflection probabilities as overall score.

## Slide 34 — Reflection tokens
Four reflection tokens: Retrieve (is retrieval needed?), Relevant (is the retrieved doc relevant?), Supported (does the doc support the next sentence?), Useful (is the next sentence useful?).

## Slide 35 — Self-RAG Inference
Two prompt templates: [x, d, <|IsRel|>] to score yes/no for the next reflection token, and [x, d, y] to generate the next answer chunk y.

## Slide 36 — RAG vs. SELF-RAG
A figure contrasting standard RAG with the Self-RAG decision-driven flow.

## Slide 37 — Training: Critic Model
The training pipeline: start from Q/A pairs, decompose into question and context, label the dataset with reflection tokens using GPT-4 driven by token-specific prompts. Train a dedicated critique model D and use it for data augmentation, generating RAG trajectories with reflection tokens and training the generator model M on the resulting dataset.

## Slide 38 — Fine-Tune M for reflection token generation
A figure showing fine-tuning of M to emit reflection tokens.

## Slide 39 — Implementation using pretrained LLM
A simplified Self-RAG flow implemented as a LangGraph state machine with IsRel, IsSup, IsUse, and Retrieve nodes.

## Slide 40 — 4.3 Self-Corrective RAG (CRAG)
Sub-section divider for CRAG.

## Slide 41 — CRAG
CRAG classifies retrieved documents into Relevant, Ambiguous, or Irrelevant, aggregates document scores into an overall set score, and corrects retrieved knowledge by refining the Relevant and Ambiguous documents or by rewriting the query for web search. Refinement decomposes documents into strips, scores each strip's relevance, and recombines only the relevant strips before generation.

## Slide 42 — Retrieval and Output evaluators
A figure showing the retrieval and output evaluators in CRAG, using structured output.

## Slide 43 — Query Rewriter
A figure showing the query rewriter step in CRAG.

## Slide 44 — CRAG Inference
A figure showing end-to-end CRAG inference.

## Slide 45 — 5. Generator fine-tuning
Section divider for Retrieval-Augmented Fine-Tuning (RAFT).

## Slide 46 — RAG Generators
RAFT combines RAG with fine-tuning by fine-tuning the generator on domain-specific documents.

## Slide 47 — Mechanics of RAFT
Fine-tune the generator to cope with both relevant and irrelevant documents and to justify the answer using the context. The dataset is built by generating Q/A from unlabeled domain text, associating each question with relevant documents plus distractors (irrelevant), and producing CoT answers containing links from retrieved pieces to the final answer.

## Slide 48 — Generate QA dataset from unlabeled docs
Sub-section divider for QA-from-docs generation.

## Slide 49 — CoT answer generation prompt
A screenshot of the CoT answer generation prompt.

## Slide 50 — Format Prompt
A screenshot of the format prompt used to assemble training records, where the context contains distractors.

## Slide 51 — LlamaIndex: Prepare RAFT dataset
Two screenshots showing how to prepare a RAFT dataset with LlamaIndex.

## Slide 52 — Generator training
Supervised fine-tuning where the ground truth is the CoT answer generated without distractors and the training input is the context with distractors, so the model learns to ignore irrelevant documents.

## Slide 53 — 6. Cache-Augmented RAG
Section divider for CAG.

## Slide 54 — Reminder: Cross-Attention
A figure recalling cross-attention.

## Slide 55 — Background KV-Caching for Autoregressive Models
In attention, Key and Value vectors of all tokens can be cached for subsequent evaluation (token prediction), avoiding recomputation.

## Slide 56 — CAG
RAG stores documents in a database and injects relevant information into the prompt (low latency, unlimited background document set). CAG (Cache-Augmented RAG) stores tokens of background documents in the KV cache and generates with cross-attention against the preloaded tokens (fast inference, limited context). Docs (chunks or doc summaries) are treated as soft tokens.

---

## Deck-level takeaway
The deck is a long survey of advanced RAG techniques organized into six families. Indirect embeddings (HyDE, HyPE) bring query and document representations closer. Context compression (summarization, embedding filter, MMR) cuts noise from the retrieved context. Fusion methods (Multi-hop decomposition, RAG-Fusion with reciprocal rank fusion, Fusion-in-Decoder) integrate evidence across multiple retrieval passes or passages. Self-validation methods make the model judge its own retrieval and generation: simple LLM filtering, Self-RAG with explicit reflection tokens and a trained critic, and CRAG with relevance triage plus query rewriting. Generator fine-tuning (RAFT) teaches the model to ignore distractors and produce CoT answers that cite retrieved pieces. Finally, Cache-Augmented RAG (CAG) preloads documents into the KV cache so generation cross-attends to them directly, trading unlimited corpus for lower latency.
