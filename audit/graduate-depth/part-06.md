# Graduate-Depth Audit: Part 6 (Agentic AI)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 26.1 | What Makes an LLM an Agent | COURSE-READY | |
| 26.2 | Planning & Agentic Reasoning | COURSE-READY | |
| 26.3 | Reasoning Models as Agent Backbones | COURSE-READY | |
| 26.4 | Agent Evaluation & Benchmarks | COURSE-READY | |
| 26.5 | End-to-End Agent System Architecture | COURSE-READY | |
| 26.5a | Cost Control, Permissions, Recovery, Wiring | COURSE-READY | |
| 26.6 | Memory Architecture for Agents | COURSE-READY | |
| 27.1 | Function Calling Across Providers | COURSE-READY | |
| 27.2 | Model Context Protocol (MCP) | COURSE-READY | |
| 27.3 | Agent-to-Agent Protocol (A2A) | DEPTH-GAP | No JSON-RPC request/response wire trace and no worked task-delegation code; Agent Card lifecycle is described narratively, only a static Agent Card JSON is shown. |
| 27.4 | Custom Tool Design | COURSE-READY | |
| 27.5 | Retrieval as a Tool Call | COURSE-READY | |
| 27.6 | Multi-Tool Orchestration & Tool Economy | COURSE-READY | |
| 27.6a | Tool Orchestration Patterns & Interp Lab | COURSE-READY | |
| 28.1 | Framework Landscape | CATALOG-OK | |
| 28.2 | Architecture Patterns | COURSE-READY | |
| 28.3 | Human-in-the-Loop Agent Systems | COURSE-READY | |
| 28.4 | Testing Multi-Agent Systems | COURSE-READY | |
| 29.1 | Code Generation Agents | COURSE-READY | |
| 29.2 | Browser & Web Agents | COURSE-READY | |
| 29.3 | Research & Data Analysis Agents | DEPTH-GAP | Deep-research plan-execute-reflect loop is only narrated; no planner/reflection loop trace or pseudocode and no gap-detection/source-credibility-scoring algorithm. Only a single data-analysis sandbox snippet carries any mechanism. |
| 29.4 | Production Agentic Coding Systems (2026) | CATALOG-OK | |
| 30.1 | Platforms | CATALOG-OK | |
| 30.2 | Agent Libraries | CATALOG-OK | |
| 30.3 | Multi-Agent Patterns & Topologies | CATALOG-OK | |
| 30.4 | Datasets & Benchmarks | CATALOG-OK | |
| 30.5 | Models | CATALOG-OK | |
| 30.6 | External Reading & Communities | CATALOG-OK | |

## Summary
- COURSE-READY: 20 | DEPTH-GAP: 2 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 7
- Top sections most worth enriching:
  1. 27.3 (A2A): add an Algorithm box for the task lifecycle state machine plus a worked JSON-RPC delegation trace (client posts tasks/send, server streams status updates submitted -> working -> input-required -> completed), matching the depth MCP gets in 27.2.
  2. 29.3 (Research & Data Analysis): add a plan-execute-reflect pseudocode/loop trace for a deep-research agent and a source-credibility / gap-detection scoring sketch, so the section teaches the mechanism rather than describing it.
