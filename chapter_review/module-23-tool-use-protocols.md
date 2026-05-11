# Module 23: Tool Use, Function Calling & Protocols

**Audit date**: 2026-05-11
**Sections reviewed**: 23.1, 23.2, 23.3, 23.4, 23.5
**Total word count**: ~16,300 (HTML markup included; section bodies are notably short)

## Summary
Cleanly numbered (no renumbering bug) and well-structured chapter covering function calling, MCP, A2A, custom tools, and agentic RAG. The biggest issues are (1) several sections are too thin for the topic depth advertised in the chapter overview, especially A2A (only 3 H2 sections, ~2,500 words), (2) lab code captions and lab setup are clearly placeholder text (mentioning torch/transformers in an MCP lab), and (3) Code Fragment numbering jumps (skipping 23.1.1, etc.).

## Inconsistencies
- **section-23.1 code fragment numbering**: First captioned fragment is "Code Fragment 23.1.2" (line 118), then 23.1.3, 23.1.4, 23.1.5. There is no 23.1.1. Off-by-one or missing fragment.
- **section-23.1 line 118**: Caption text "Using openai, OpenAI" is auto-generated from imports - not informative. Same problem at line 174 ("Using anthropic"), line 120 ("Implementation of get_weather").
- **section-23.2 line 193**: Lab setup `Code Fragment 23.2.3` caption says "Installs torch, transformers, and numpy for the MCP tool-use protocol lab. These packages provide the model loading, tokenization, and numerical operations needed for the exercises." This is wrong: the MCP lab does not need torch/transformers; it needs the MCP Python SDK (`mcp[cli]` or similar). Caption appears copy-pasted from a different lab.
- **section-23.2 line 204**: "Code Fragment 23.2.4: Step 1 stub: load the required libraries and prepare data..." - explicitly labeled "stub". Lab content is incomplete.
- **section-23.2 line 228**: "Code Fragment 23.2.5: Complete solution for the MCP tool-use lab exercise. Students should implement the full MCP server..." reads "Students" - the book uses "reader" per project style guide; also the prose contradicts itself ("Complete solution" + "Students should implement").
- **section-23.3 (A2A) only has 3 H2 sub-sections** (23.3.1 protocol, 23.3.2 lifecycle, 23.3.3 federation) and one Code Fragment. Disproportionately thin given its standalone-section status.
- **section-23.4 has no labs** despite the chapter pattern of one lab per major section (23.2 has one).
- **Tool-use code fragment 23.1.5 caption** (line 176) is two paragraphs of explanatory text concatenated together - inconsistent with the one-line caption style elsewhere.
- **chapter-nav prev** (line 118): Points to `module-22-ai-agents/section-22.4.html` titled "Research Replication Benchmarks and ML Engineering Agent Evaluation" - this title is not the actual `<title>` of section-22.4.html (which is "Agent Evaluation & Benchmarks"). Cross-chapter nav has a stale label.

## Gaps
- **No discussion of `parallel_tool_calls` or tool-call batching** in 23.1 (a major OpenAI feature) and Anthropic's `disable_parallel_tool_use`.
- **section-23.1 OpenAI section**: Does not mention the `tools` parameter format change (deprecation of `functions` field) or `tool_choice="required"` mode. Both are common 2024-2026 patterns.
- **section-23.2 (MCP)**: Mentions ecosystem stats ("97M+ monthly SDK downloads, 6400+ servers") but does not cite source or as-of date. Does not cover MCP transport types (stdio, SSE, HTTP) in depth.
- **section-23.3 (A2A)**: Missing concrete A2A reference implementation discussion (Google's a2a-protocol GitHub) and how A2A relates/competes with MCP. This comparison is essential reader context.
- **section-23.4 (custom tool design)**: No mention of OpenAI's structured outputs / JSON schema strict mode for tool arguments, which is the production standard now.
- **section-23.5 (agentic RAG)**: Brief; CRAG covered well via LangGraph snippet, but Self-RAG and Adaptive-RAG (mentioned in chapter index card) are not covered in the section body.
- **No bridge to module 26** (agent safety) on tool-related security topics like prompt injection via tool descriptions. Section 23.4 mentions security but does not cross-link.

## Errors
- **section-23.1 line 118 caption**: "Using openai, OpenAI" - placeholder text passed through.
- **section-23.2 line 193 caption (lab setup)**: Wrong dependencies listed (torch/transformers vs MCP SDK).
- **section-23.5 references CRAG via LangGraph**: Verify the StateGraph API surface is current. LangGraph evolves rapidly; a code snippet from mid-2024 may not run unchanged in 2026.
- **MCP ecosystem statistics** ("97M+ monthly SDK downloads, 6400+ servers") in chapter index need a specific date/source citation; without it, claim is unverifiable.
- **A2A protocol description** (section-23.3): Verify the JSON Agent Card schema matches Google's current spec (the protocol's task lifecycle states should be enumerated explicitly).

## Improvements
- **Replace placeholder code captions** in 23.1 ("Using openai, OpenAI", "Implementation of get_weather"), 23.2 ("Step 1 stub", "Complete solution... Students should implement"), with substantive one-line descriptions per the code-pedagogy agent's caption rules.
- **Fix lab code fragment 23.2.3** to install correct MCP dependencies (`pip install mcp` or similar) and remove the mistaken torch/transformers references.
- **Expand section 23.3 (A2A)** to match the depth of 23.2 (MCP). Add transport details, lifecycle diagram, and a concrete agent-card example with explicit MCP comparison.
- **Add Self-RAG and Adaptive-RAG coverage** to 23.5 to match the index card description.
- **Add `parallel_tool_calls` discussion** to 23.1 with a code example.
- **Add MCP comparison table to 23.3** (A2A vs MCP: scope, transports, target use cases).
- **Standardize all "Section X uses LangGraph/openai/anthropic" snippets** with version pinning (`# Tested with langgraph==0.2.X, anthropic==0.34.X`) plus an "as of" timestamp.
- **Add a forward pointer** at end of 23.4 (security) to module 26 (production safety) and a back pointer at module 26 to 23.4.
- **Number Code Fragment 23.1.1 explicitly** (or renumber the existing first fragment as 23.1.1 instead of 23.1.2).

## One-thing-only fix
Replace the placeholder lab content in section-23.2 (the MCP lab): the Code Fragment 23.2.3 setup-cell caption installs the wrong packages (torch/transformers) and Code Fragment 23.2.4 is explicitly labeled "Step 1 stub". Either complete the lab or remove it - currently it tells readers to install ML libraries for an MCP server lab.
