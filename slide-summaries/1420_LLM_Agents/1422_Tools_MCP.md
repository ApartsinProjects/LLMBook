# 1422_Tools_MCP — Per-Slide Summary

**Source file:** `1422_Tools_MCP.pptx`
**Source folder:** `SlidesPool/1420_LLM_Agents/`
**Drive link:** https://drive.google.com/file/d/164axMMa2adWtmvVZGE7FUsmGF1jsGg1j/view
**Slide count (exact, via python-pptx):** 15
**Extraction:** Local parse + slide PNG render. Bullets describe the MCP role taxonomy and capabilities; figures illustrate JSON-RPC envelopes and host integrations.

---

## Slide 1 — MCP: Model Context Protocol
Title slide for the deck on the Model Context Protocol.

## Slide 2 — Without MCP
Without MCP, M applications and N tools require M-by-N custom integrations.

## Slide 3 — With MCP
With MCP the problem becomes M + N: each app and each tool implements one standard interface.

## Slide 4 — MCP Terminology
Host is the user application (Claude Desktop, Cursor IDE). Server exposes tools through the MCP protocol. Client is a standard or custom MCP client, one instance per tool, maintaining a persistent connection and optionally state.

## Slide 5 — MCP Server capabilities
Four capability types. Tools are executable functions or APIs. Resources are read-only content (e.g., context). Prompts are predefined templates for the host to feed the LLM. Sampling is a server-initiated request back to the client / host.

## Slide 6 — Example: Code Generation
A code-generation MCP server provides a code interpreter (tool), a code-style prompt template, documentation on APIs as resources, and sampling for the LLM to review generated code.

## Slide 7 — Communication Protocols: JSON-RPC
MCP messages follow JSON-RPC: request, response, and server-initiated notification, shown across three screenshots.

## Slide 8 — Transport Protocols
Two transports. STDIO writes to standard input / output pipes, used for local communication. HTTP plus SSE (Server-Sent Events) supports remote communication with server push over HTTP.

## Slide 9 — Interaction lifecycle
Section divider for the interaction lifecycle.

## Slide 10 — Understanding Capabilities
Tools are model-controlled (the LLM in the host decides when to use them, e.g., querying real-time weather). Resources are application-controlled (the host decides when to read them, e.g., configuration or files). Prompts are user-controlled and are surfaced through the host UI (e.g., common workflows). Sampling is server-initiated (e.g., requesting analysis of intermediate data during an agentic flow).

## Slide 11 — Capabilities for Complex Interactions
A figure illustrating that server-side side effects typically require user approval mediated by the host.

## Slide 12 — Prompt capability example
A code-review prompt example: the server returns a message list, with parameters supplied by the host.

## Slide 13 — MCP SDK
A code screenshot showing a toy MCP server implemented with the SDK.

## Slide 14 — Built-in MCP Client in UI hosts
Two screenshots showing Claude Desktop and Cursor IDE as built-in MCP clients configured with MCP servers.

## Slide 15 — MCP Server Directory
A figure of the MCP server directory listing public servers.

---

## Deck-level takeaway
The deck pitches MCP as the standard interface that turns the M-by-N integration problem (apps times tools) into M + N. The role taxonomy (Host, Server, Client) and the four capability types (Tools, Resources, Prompts, Sampling) cover not just function calls but also read-only context, prompt templates, and server-initiated LLM requests. The protocol layer is JSON-RPC over either local STDIO or remote HTTP plus SSE. The closing slides ground the abstraction in real integrations: Claude Desktop and Cursor IDE ship MCP clients, and the public MCP server directory provides ready-made servers to plug in.
