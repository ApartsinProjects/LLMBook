# 1425_Memory_MemGPT — Per-Slide Summary

**Source file:** `1425_Memory_MemGPT.pptx`
**Source folder:** `SlidesPool/1420_LLM_Agents/`
**Drive link:** https://drive.google.com/file/d/1boUrhYpF5dpogIp5dweyO4gbfJCZum82/view
**Slide count (exact, via python-pptx):** 17
**Extraction:** Local parse + slide PNG render. Bullets carry the conceptual content; code screenshots illustrate a LangGraph reimplementation.

---

## Slide 1 — MemGPT
Title slide for the deck on MemGPT.

## Slide 2 — MemGPT
Sub-title: self-editing memory.

## Slide 3 — MemGPT
MemGPT distinguishes Working / Short-Term Memory (STM), the current context window (e.g., 4K tokens), like RAM, from Recall / Long-Term Memory (LTM), an external store or vector database, like disk. The language model is given control over its own memory and decides when and what to read or write, behaving like an operating system. The objective is document-based dialog. Memory control swaps content between LTM and STM (like paging), with memory operations exposed as tools.

## Slide 4 — MemGPT Event Loop
The system responds to events (user message, document upload, timer) by producing memory system calls via the function-calling mechanism. A task stack and context switching let it solve subtasks and return to the main task, or save state when a new task arrives.

## Slide 5 — Hierarchical Memory
A queue manager decides what stays in the FIFO queue (evict, summarize, or reorder) and stores evicted items in recall storage. The LLM decides what to recall via the recall and archival search function.

## Slide 6 — MemGPT Event-Driven
Two interrupt types: Alert (memory pressure, limited context space) and Pause interrupt (no other alerts handled until the current task is done).

## Slide 7 — MemGPT Memory Management Prompt
A figure of the memory-management prompt that drives the LLM's decisions about read / write operations.

## Slide 8 — MemGPT in LangGraph
Section divider for a toy reimplementation in LangGraph.

## Slide 9 — MemGPT Implementation in LangGraph
The implementation persists and fetches long-term memory in a DB and defines memory operations as tools. Nodes: load initial memory, agent, tool node (search the web, load / save into vector store).

## Slide 10 — Define Memory Tools
Two screenshots defining the memory-operation tools.

## Slide 11 — Add Search Tool (LTM)
Two screenshots adding the search tool and defining state as pulled memories (STM); the state inherits the "messages" field from the built-in MessageState.

## Slide 12 — The prompt
Section header for the memory-management prompt used by this implementation.

## Slide 13 — Agent function
Code screenshot of the agent function that injects recalled memories into the prompt.

## Slide 14 — Recall memories
Memory recall is based on the last 2K tokens of the conversation history.

## Slide 15 — Edge: Route to a tool Node
Code screenshot of the conditional edge that routes to the tool node.

## Slide 16 — Build graph
Two screenshots assembling the full LangGraph graph.

## Slide 17 — Run the agent
Two screenshots running the resulting MemGPT-style agent.

---

## Deck-level takeaway
MemGPT treats an LLM like an operating system, separating in-context working memory (STM) from external long-term storage (LTM) and giving the model explicit tools to page content between them. The model's "OS calls" include search and write operations against vector storage and a queue manager that evicts or summarizes when context pressure rises. The deck then walks through a toy reimplementation in LangGraph: memory tools, agent node that injects recalled memories, the conditional edge that routes to tools, and the assembled graph that runs a self-editing memory dialogue.
