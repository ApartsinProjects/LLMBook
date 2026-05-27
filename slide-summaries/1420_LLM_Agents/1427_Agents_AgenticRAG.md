# 1427_Agents_AgenticRAG — Per-Slide Summary

**Source file:** `1427_Agents_AgenticRAG.pptx`
**Source folder:** `SlidesPool/1420_LLM_Agents/`
**Drive link:** https://drive.google.com/file/d/1qINPuU2B1U7lnkc44hvZKjBGYUAugf88/view
**Slide count (exact, via python-pptx):** 11
**Extraction:** Local parse + slide PNG render. Code screenshots illustrate the LangGraph implementation step by step.

---

## Slide 1 — Agentic RAG
Title slide for the deck on agentic RAG.

## Slide 2 — Agentic RAG
Agentic RAG decomposes and rewrites the user question to retrieve more helpful context.

## Slide 3 — LangGraph
A diagram of the LangGraph state machine that implements the agentic-RAG loop.

## Slide 4 — Preprocess Documents
Two screenshots preprocessing documents into the vector store.

## Slide 5 — Create Retrieval Tool
Two screenshots creating the retrieval tool that the agent will call.

## Slide 6 — Generate Retrieval Query
A screenshot of the prompt and chain that generates the retrieval query (possibly different from the user's question).

## Slide 7 — Grade Document: Prompt and Scheme
A screenshot of the document-grading prompt and structured schema (relevant or not).

## Slide 8 — Grade Document: Conditional Edge
A screenshot of the conditional edge that routes to answer generation or to question rewriting based on the grade.

## Slide 9 — Rewrite Question
A screenshot of the chain that rewrites the question to improve retrieval on the next pass.

## Slide 10 — Generate Answer
A screenshot of the answer-generation chain.

## Slide 11 — Create graph
Two screenshots wiring the nodes into a LangGraph graph.

---

## Deck-level takeaway
Agentic RAG turns retrieval and generation into a stateful loop: the agent first generates a retrieval query, fetches documents, grades each document for relevance, and either rewrites the question and retries or proceeds to answer generation. The deck implements this end-to-end in LangGraph with one node per step (preprocess, retrieve, grade, rewrite, generate) and a conditional edge that routes based on the document grade, producing a self-correcting RAG loop driven entirely by the language model.
