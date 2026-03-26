# Chapter Plan: Module 09 - Working with LLM APIs

## Scope

**What this chapter covers:** The full lifecycle of interacting with large language model APIs in production. Specifically: the API landscape across major providers (OpenAI, Anthropic, Google Gemini, AWS Bedrock, Azure OpenAI, and open-source serving frameworks); streaming with Server-Sent Events; the Batch API for cost reduction; structured output enforcement via JSON mode, response schemas, Pydantic, and the Instructor library; function calling and tool use across providers; and production engineering patterns including provider routing (LiteLLM), caching strategies (exact and semantic), retry logic with exponential backoff and jitter, circuit breakers, AI gateways (Portkey, Helicone), token budget enforcement, and graceful degradation.

**What this chapter does NOT cover:** Prompt engineering techniques (Module 10), agent orchestration and multi-step tool use loops (Module 21), fine-tuning APIs (Module 13), RAG pipelines (Module 19), or model serving infrastructure (Module 08). The chapter assumes models are accessed through hosted APIs, not self-hosted inference servers.

**Target audience:** Engineers with Python proficiency and familiarity with HTTP/JSON who want to build reliable, production-grade LLM integrations. Prior understanding of how LLMs generate text (Module 05) and why APIs are structured around token-based inference (Module 08) is assumed.

**Target length:** ~14,000 to 17,000 words across three sections.

---

## Learning Objectives

1. Call the Chat Completions API (OpenAI), Messages API (Anthropic), and Gemini API (Google) with correct parameter usage.
2. Implement streaming responses using Server-Sent Events and understand when streaming is appropriate.
3. Use function calling and tool use to connect LLMs to external systems.
4. Enforce structured output with JSON mode, response schemas, and validation libraries like Instructor and Pydantic.
5. Build provider-agnostic LLM clients using abstraction layers such as LiteLLM.
6. Implement production-grade error handling with retry logic, circuit breakers, and graceful degradation.
7. Design caching strategies (semantic caching, prompt caching) to reduce cost and latency.
8. Set up token budget enforcement, cost tracking, and observability using AI gateways.

---

## Prerequisites

- Module 05: Decoding Strategies and Text Generation (understanding of temperature, top-p, and generation parameters)
- Module 08: Inference Optimization and Efficient Serving (context for why APIs are structured as they are)
- Basic familiarity with Python, HTTP requests, and JSON
- API keys for at least one provider (OpenAI, Anthropic, or Google) for hands-on labs

---

## Current Content Assessment

### Section 9.1: API Landscape & Architecture (~4,500 words)

**Strengths:**
- Comprehensive coverage of the API ecosystem: OpenAI, Anthropic, Google Gemini, AWS Bedrock, Azure OpenAI, and open-source serving (vLLM, Ollama)
- Excellent ecosystem SVG diagram (Figure 9.1) mapping all providers and their HTTP/JSON patterns
- Good code examples: OpenAI basic call, streaming with SSE, Batch API, Anthropic Messages API with prompt caching, Gemini API, open-source endpoint via OpenAI-compatible format
- Provider comparison table covering model names, message format, streaming support, and special features
- Universal request/response cycle diagram (Figure 9.2) is clear and well labeled
- Big Picture callout immediately motivates why the API interface matters
- Authentication and rate limits section addresses a common pain point
- 5 quiz questions with detailed answers
- Key Takeaways section well organized

**Weaknesses / Improvement Opportunities:**
- Missing: explicit code example for AWS Bedrock or Azure OpenAI. The warning callout notes their existence but no runnable code is provided. At minimum, a Bedrock example showing the client configuration difference would help enterprise users.
- The Batch API section could benefit from a cost savings calculation showing the 50% discount in concrete dollar terms.
- No mention of multimodal API usage (sending images to GPT-4o or Claude). Even a brief callout acknowledging this capability with a forward reference would be valuable.
- The streaming section does not mention when streaming is inappropriate (e.g., when you need the complete response for validation before acting on it).
- Missing: rate limit handling code. The section discusses 429 errors conceptually but defers all retry logic to Section 9.3. A minimal retry snippet here would help readers who may not read sequentially.

**Structural Issues:**
- CSS is consistent with other sections in the module.
- Navigation links are correct.

---

### Section 9.2: Structured Output & Tool Integration (~4,500 words)

**Strengths:**
- Clear three-level structured output diagram (Figure 9.3): text parsing, JSON mode, and schema-constrained output
- Thorough progression from JSON mode to JSON Schema to Instructor/Pydantic, showing each escalation step
- Excellent function calling loop diagram (Figure 9.4) with clear flow: model proposes tool call, code executes, result sent back
- Both OpenAI and Anthropic tool use implementations shown side by side
- Nested Pydantic models with enums example demonstrates real-world complexity
- Cross-provider tool use comparison table is a valuable reference
- Parallel and sequential tool call patterns covered with async code
- 5 quiz questions covering key distinctions (JSON mode vs. schema, who executes functions, Instructor advantages)

**Weaknesses / Improvement Opportunities:**
- Missing: BAML as a structured output tool. It is covered in Module 11.5 but not mentioned here despite being a growing alternative to Instructor. A brief forward reference would improve cross-module coherence.
- The Instructor retry logic (automatic re-prompting on validation failure) is mentioned but not demonstrated with a code example. Showing the `max_retries` parameter with a deliberate validation failure would be instructive.
- No discussion of streaming with structured output (e.g., partial JSON parsing as tokens arrive). This is an increasingly common production need.
- Missing: Google Gemini function calling example. Only OpenAI and Anthropic are demonstrated, but the index page lists Google as a covered provider.
- The "Building Reliable Tool Pipelines" topic listed in the index description is only partially addressed. A more explicit pipeline pattern (multiple tools orchestrated in sequence) would fulfill this promise.

**Structural Issues:**
- The section is well structured with clear H2/H3 hierarchy.
- Navigation links are correct.

---

### Section 9.3: API Engineering Best Practices (~5,500 words)

**Strengths:**
- LiteLLM coverage is thorough: basic routing, fallback routing, model aliases
- Error taxonomy table categorizing errors as transient, quota, client, or server is a strong reference
- Exponential backoff with jitter implementation is production-quality code
- Circuit breaker pattern with state machine diagram (Figure 9.5) is well explained and has a complete implementation
- Both exact caching and semantic caching covered with full code examples
- AI gateway section covers both Portkey and Helicone with working code snippets
- Token budget enforcement with soft/hard limits is a practical pattern rarely covered in textbooks
- Graceful degradation ladder diagram (Figure 9.6) shows four levels of fallback
- Production error handling pattern (comprehensive LLMClient class) ties everything together
- 5 quiz questions on practical engineering topics

**Weaknesses / Improvement Opportunities:**
- The semantic caching implementation uses a simplistic cosine similarity threshold. A note about tuning this threshold for different use cases (and the risk of false cache hits) would be valuable.
- Missing: logging and observability beyond AI gateways. No mention of OpenTelemetry, LangSmith, or structured logging patterns for LLM calls. The section focuses on gateways but does not address teams that build their own observability stack.
- The token budget enforcement section does not show integration with LiteLLM or a gateway. Showing how budget limits compose with routing would be more realistic.
- Missing: cost estimation before making an API call (using tiktoken to count tokens and estimate cost). This is a common production need.
- The graceful degradation section describes the concept well but lacks a code example. A brief implementation showing the degradation ladder in action would strengthen the section.
- No mention of async patterns for concurrent API calls beyond what is shown in 9.2. Production systems often need to fan out to multiple models simultaneously.

**Structural Issues:**
- This is the longest section in the module (1,106 lines). The length is justified by the breadth of production patterns covered.
- Navigation links are correct.

---

## Chapter Structure

### Section 9.1: API Landscape & Architecture (~4,500 words)
- Key concepts: LLM API ecosystem, HTTP/JSON interface pattern, Chat Completions API (OpenAI), Messages API (Anthropic), Gemini API (Google), AWS Bedrock, Azure OpenAI, open-source serving (vLLM, Ollama), OpenAI-compatible API format, streaming with SSE, Batch API, prompt caching, authentication, rate limits, provider selection criteria
- **Diagrams:**
  - [EXISTS] API ecosystem overview (Figure 9.1)
  - [EXISTS] Universal request/response cycle (Figure 9.2)
- **Code examples:**
  - [EXISTS] OpenAI Chat Completions basic call
  - [EXISTS] Streaming with SSE
  - [EXISTS] Batch API usage
  - [EXISTS] Anthropic Messages API with prompt caching
  - [EXISTS] Google Gemini API
  - [EXISTS] Open-source endpoint (OpenAI-compatible)
  - [ADD] AWS Bedrock minimal configuration example
- **Exercises:** [EXISTS] 5 quiz questions with detailed answers
- **Improvements:**
  - Add a brief AWS Bedrock code example
  - Add a cost savings calculation for the Batch API
  - Add a callout on multimodal API support with forward reference
  - Note when streaming is inappropriate (validation before action)

### Section 9.2: Structured Output & Tool Integration (~4,500 words)
- Key concepts: structured output problem (text parsing, JSON mode, schema-constrained), OpenAI JSON mode, OpenAI Structured Outputs with JSON Schema, Pydantic models, Instructor library, nested models and enums, function calling (OpenAI and Anthropic), tool use loop, parallel and sequential tool calls, cross-provider tool use comparison
- **Diagrams:**
  - [EXISTS] Three levels of structured output enforcement (Figure 9.3)
  - [EXISTS] Function calling loop (Figure 9.4)
- **Code examples:**
  - [EXISTS] OpenAI JSON mode
  - [EXISTS] OpenAI Structured Outputs with schema
  - [EXISTS] Instructor basic usage
  - [EXISTS] Nested Pydantic models with enums
  - [EXISTS] OpenAI function calling (weather example)
  - [EXISTS] Anthropic tool use
  - [EXISTS] Parallel tool calls with asyncio
  - [ADD] Instructor retry on validation failure
- **Exercises:** [EXISTS] 5 quiz questions with detailed answers
- **Improvements:**
  - Add forward reference to BAML (Module 11.5)
  - Add Instructor retry/validation failure example
  - Add a brief note on streaming with structured output
  - Add Google Gemini function calling example

### Section 9.3: API Engineering Best Practices (~5,500 words)
- Key concepts: LiteLLM provider routing, fallback routing, error taxonomy (transient, quota, client, server), exponential backoff with jitter, circuit breaker pattern (closed, open, half-open), exact caching (hash-based), semantic caching (embedding similarity), AI gateways (Portkey, Helicone), token budget enforcement (soft/hard limits), graceful degradation ladder, production error handling patterns
- **Diagrams:**
  - [EXISTS] Circuit breaker state machine (Figure 9.5)
  - [EXISTS] Graceful degradation ladder (Figure 9.6)
  - [ADD] Observability pipeline diagram (API call > logging > metrics > alerts)
- **Code examples:**
  - [EXISTS] LiteLLM basic routing
  - [EXISTS] LiteLLM fallback routing
  - [EXISTS] Exponential backoff with jitter
  - [EXISTS] Circuit breaker implementation
  - [EXISTS] Exact caching with Redis
  - [EXISTS] Semantic caching with embeddings
  - [EXISTS] Portkey gateway integration
  - [EXISTS] Helicone gateway integration
  - [EXISTS] Token budget enforcement
  - [EXISTS] Production LLMClient class
  - [ADD] Token count estimation with tiktoken
- **Exercises:** [EXISTS] 5 quiz questions with detailed answers
- **Improvements:**
  - Add semantic cache threshold tuning guidance
  - Add observability beyond gateways (OpenTelemetry, structured logging)
  - Add pre-call cost estimation snippet
  - Add a brief graceful degradation code example

---

## Terminology Standards

| Term | Usage | Notes |
|------|-------|-------|
| Chat Completions API | Official OpenAI endpoint name | Always capitalize |
| Messages API | Official Anthropic endpoint name | Always capitalize |
| function calling | Lowercase, OpenAI terminology | Not "tool calling" when referring to OpenAI specifically |
| tool use | Lowercase, Anthropic terminology | Equivalent to OpenAI function calling |
| structured output | Lowercase | Generic concept |
| Structured Outputs | Capitalized | Specific OpenAI feature name with JSON Schema |
| SSE | Abbreviation for Server-Sent Events | Define on first use |
| circuit breaker | Lowercase | Software pattern, not a proper noun |
| semantic caching | Lowercase | Generic technique |
| prompt caching | Lowercase | Anthropic-specific feature; clarify provider context |
| LiteLLM | CamelCase | Library name; always use exact casing |
| Instructor | Capitalized | Library name |
| Pydantic | Capitalized | Library name |

---

## Cross-References

### Upstream Dependencies
- **Module 05 (Decoding Strategies):** Temperature, top-p, frequency penalty, and other generation parameters referenced throughout Section 9.1
- **Module 08 (Inference Optimization):** KV cache, batching, quantization context for understanding why APIs have specific constraints

### Downstream Dependents
- **Module 10 (Prompt Engineering):** Relies on API call mechanics from 9.1, structured output from 9.2
- **Module 11 (Hybrid ML+LLM):** Uses API routing, caching, and cost patterns from 9.3; uses Instructor from 9.2
- **Module 19 (RAG):** Tool use patterns from 9.2 form the basis for retrieval tool integration
- **Module 21 (AI Agents):** Function calling from 9.2 is the foundation for agent tool use
- **Module 25 (Evaluation):** Observability patterns from 9.3 connect to evaluation and monitoring
- **Module 26 (Production):** Production patterns from 9.3 are extended for deployment at scale

### Internal Cross-References
- Section 9.2 references 9.1 for basic API call setup
- Section 9.3 references 9.2 for structured output in caching strategies
- Section 9.3's caching overlaps with Module 11.4's cost optimization discussion; ensure consistent terminology

---

## Estimated Word Count

| Section | Estimated Words |
|---------|----------------|
| 9.1 API Landscape & Architecture | ~4,500 |
| 9.2 Structured Output & Tool Integration | ~4,500 |
| 9.3 API Engineering Best Practices | ~5,500 |
| **Total** | **~14,500** |

---

## Narrative Arc

The chapter follows a progression from **understanding** to **building** to **hardening**:

1. **Section 9.1 (Explore):** The reader discovers the API landscape, learning that despite surface differences across providers, all LLM APIs share a common HTTP/JSON pattern. The section builds confidence by showing that once you understand one API, switching providers is straightforward. The streaming and batch API subsections introduce two fundamental modes of interaction.

2. **Section 9.2 (Build):** Armed with basic API knowledge, the reader learns to make LLMs produce reliable, structured outputs and interact with external systems. The progression from free-text to JSON mode to schema-constrained output to Pydantic validation mirrors how production requirements escalate. Function calling introduces the bidirectional pattern where LLMs request actions from the application.

3. **Section 9.3 (Harden):** The final section shifts from "make it work" to "make it work in production." Every pattern addresses a real failure mode: provider outages (routing, circuit breakers), latency spikes (caching), cost overruns (budgets, gateways), and cascading failures (graceful degradation). The chapter closes with a comprehensive production client that composes all patterns into a single, battle-tested class.

The overarching message: LLM APIs are deceptively simple to call but surprisingly hard to call reliably, cheaply, and at scale. This chapter equips readers with both the basic literacy and the production engineering toolkit to bridge that gap.
