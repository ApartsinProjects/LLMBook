# 1423_Memory_Intro — Per-Slide Summary

**Source file:** `1423_Memory_Intro.pptx`
**Source folder:** `SlidesPool/1420_LLM_Agents/`
**Drive link:** https://drive.google.com/file/d/1jTYIbPbmWe6gJ3DHaY3EEONt3yX9VC71/view
**Slide count (exact, via python-pptx):** 12
**Extraction:** Local parse + slide PNG render. Bullets and code screenshots cover three LangChain memory strategies.

---

## Slide 1 — Memory and LLMs
Title slide for the deck on dialogue-system memory.

## Slide 2 — LLM and Dialogue Systems (Chatbots)
The LLM is stateless: it generates a response for a prompt. Dialogue systems need state across turns, with prior user messages and assistant answers. That state is encoded inside the prompt.

## Slide 3 — Dialog state in the prompt
Dialogue state can be all previous user and assistant messages, or summarized / filtered messages. The prompt template can have a single placeholder for the entire dialogue state or many placeholders, one per message.

## Slide 4 — OpenAI Chat Applications
Section divider for the OpenAI chat-message pattern.

## Slide 5 — OpenAI message thread
The OpenAI client takes a message list with prior user and assistant turns as history.

## Slide 6 — OpenAI Chat Application
Two screenshots showing an OpenAI-based chat application that re-sends history each turn.

## Slide 7 — LangChain memory
Section divider for LangChain memory abstractions.

## Slide 8 — Memory Strategies
Three strategies. Infinite Conversational Buffer remembers and provides all previous messages. Windowed Conversational Buffer provides only the last K messages. Conversation Summary uses an LLM to summarize the prior conversation.

## Slide 9 — Simple Conversation Buffer
Five screenshots demonstrating the simple buffer that retains everything.

## Slide 10 — Windowed Conversation Buffer
Four screenshots showing a windowed buffer limited to the last K turns.

## Slide 11 — Conversation Summary Memory
Four screenshots showing summary memory, where the LLM compresses prior turns into a running summary.

## Slide 12 — LangChain: Memory Comparison
A comparison figure showing the trade-offs across the three memory strategies.

---

## Deck-level takeaway
The deck explains the stateless-LLM-plus-stateful-dialogue gap and the three classic ways to bridge it inside the prompt. Infinite buffers are the simplest but unbounded. Windowed buffers cap the cost by retaining only the last K turns. Summary memory uses the LLM itself to compress older turns into a compact running summary. The deck demonstrates each pattern in LangChain and contrasts them with the direct OpenAI message-list approach where the host re-sends history every turn.
