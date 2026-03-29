# Agentic AI Research Report (March 2026)

Research sweep for expanding Part VI of the textbook. Covers landmark papers, frameworks, essential topics, and a proposed chapter structure.

---

## 1. Recent Landmark Papers (2024-2026)

### Agent Architecture Surveys

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| "Agentic AI: A Comprehensive Survey of Architectures, Applications, and Future Directions" (Springer/arXiv 2510.25445) | 2025 | PRISMA survey of 90 studies (2018-2025); dual-paradigm framework: Symbolic/Classical vs. Neural/Generative |
| "The Landscape of Emerging AI Agent Architectures for Reasoning, Planning, and Tool Calling" (arXiv 2404.11584) | 2024 | Systematic survey of agent implementations; focus on reasoning, planning, tool execution |
| "Agentic AI Frameworks: Architectures, Protocols, and Design Challenges" (arXiv 2508.10146) | 2025 | Reviews CrewAI, LangGraph, AutoGen, Semantic Kernel, Google ADK, MetaGPT; evaluates communication, memory, safety |
| "Agentic Artificial Intelligence: Architectures, Taxonomies, and Evaluation of LLM Agents" (arXiv 2601.12560) | 2026 | 143 primary studies; 90%+ from 2024-2025; taxonomy of agent architectures |

### Tool Use and Function Calling

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al.) | 2022 | Foundational ReAct framework; interleaved reasoning traces and actions |
| "Toolformer: Language Models Can Teach Themselves to Use Tools" (Meta) | 2023 | Self-taught tool use without extensive human annotation |
| "LLM-Based Agents for Tool Learning: A Survey" (Springer 2025) | 2025 | Comprehensive survey of tool learning approaches |
| "MetaTool Benchmark" | 2023 | Evaluates tool usage awareness and tool selection capabilities |

### Planning and Reasoning

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| "Tree of Thoughts: Deliberate Problem Solving with LLMs" (Yao et al.) | 2023 | Tree search over reasoning states; 74% vs 4% (CoT) on Game of 24 |
| "Understanding the Planning of LLM Agents: A Survey" (arXiv 2402.02716) | 2024 | Taxonomy: task decomposition, plan selection, external module, reflection, memory |
| "PlanGenLLMs: A Modern Survey of LLM Planning Capabilities" | 2025 | Six criteria: completeness, executability, optimality, representation, generalization, efficiency |
| "Modular Agentic Planner (MAP)" (Nature Communications 2025) | 2025 | Brain-inspired modular architecture; outperforms CoT, multi-agent debate, and ToT |
| "Thought Management System (TMS)" | 2025 | Memory-augmented recursive planning for long-horizon goal-oriented tasks |

### Multi-Agent Systems

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| "Multi-Agent Collaboration Mechanisms: A Survey of LLMs" (arXiv 2501.06322) | 2025 | Framework: actors, types (cooperation/competition/coopetition), structures, strategies, protocols |
| "MALT: Improving Reasoning with Multi-Agent LLM Training" | 2024 | Jointly-trained multi-agent systems with generator, verifier, refinement roles; 14% improvement on MATH |
| "Diversity of Thought Elicits Stronger Reasoning in Multi-Agent Debate" | 2024 | Diverse model ensembles outperform homogeneous ones; medium models beat GPT-4 at 91% GSM-8K |
| "MARS: Multi-Agent Review System" | 2025 | Author-reviewer-meta-reviewer pattern; matches MAD accuracy at 50% reduced cost |
| "Persona Inconstancy in Multi-Agent LLM Collaboration" | 2024 | Identifies conformity, confabulation, and impersonation failure modes |

### Agent Memory

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| "MemGPT: Towards LLMs as Operating Systems" | 2023 | Virtual context management inspired by OS memory hierarchies |
| "A-MEM: Agentic Memory for LLM Agents" (arXiv 2502.12110) | 2025 | Dynamic Zettelkasten-style memory with structured attributes |
| "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory" | 2025 | 26% accuracy improvement, 91% faster, 90% fewer tokens vs. full context |

### Agent Evaluation and Benchmarks

| Benchmark | Year | Focus |
|-----------|------|-------|
| SWE-bench | 2023 | 2,294 real GitHub issues; execution-based testing for code agents |
| WebArena | 2023 | 812 tasks on self-hosted websites; functional correctness |
| AgentBench | 2023 | 8 environments (OS, DB, knowledge graphs, gaming, embodied AI) |
| GAIA | 2023 | 466 real-world questions; 77% human-AI performance gap |
| OSWorld | 2024 (NeurIPS) | 369 tasks on Ubuntu/Windows; real computer environments |
| WorkArena | 2024 | 682 enterprise knowledge work tasks |
| Agent Security Bench (ASB) | 2025 (ICLR) | Security evaluation for agents |
| PlanBench | 2022 | Extensible planning benchmark from IPC domains |
| FutureX | 2025 | Live benchmark for agent prediction with daily updates |

### Agent Safety

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| "Systems Security Foundations for Agentic Computing" (IACR 2025) | 2025 | Security principles; sandboxing; information-flow controls |
| "AGrail: A Lifelong Agent Guardrail" (ACL 2025) | 2025 | Framework for systemic and task-specific risk prevention |
| "Securing AI Agents Against Prompt Injection Attacks" (arXiv 2511.15759) | 2025 | 847 test cases; reduces attack success from 73.2% to 8.7% |
| "From Prompt Injections to Protocol Exploits" (ScienceDirect 2025) | 2025 | End-to-end threat model; 30+ attack techniques cataloged |

### Agentic RAG

| Paper | Year | Key Contribution |
|-------|------|-----------------|
| "Corrective Retrieval Augmented Generation (CRAG)" (arXiv 2401.15884) | 2024 | Retrieval evaluator with confidence scoring; web search fallback |
| "Agentic RAG: A Survey" (arXiv 2501.09136) | 2025 | Comprehensive survey of agentic RAG patterns and architectures |
| "Towards Agentic RAG with Deep Reasoning" | 2025 | Synergy of RAG with reasoning-capable agents |
| "Adaptive-RAG" (KAIST) | 2024 | Dynamic query handling based on complexity classification |

### Protocols and Standards

| Protocol | Year | Key Details |
|----------|------|-------------|
| Model Context Protocol (MCP) | Nov 2024 | Anthropic; 97M+ monthly SDK downloads; open standard; donated to Linux Foundation (Dec 2025) |
| Agent-to-Agent (A2A) | Apr 2025 | Google; 50+ partners; Agent Cards for discovery; HTTP/SSE/JSON-RPC |
| Agent Communication Protocol (ACP) | 2025 | IBM-contributed protocol for agent communication |
| Agent Network Protocol (ANP) | 2025 | Emerging protocol for agent discovery and networking |

---

## 2. Popular Libraries and Frameworks

### Tier 1: Dominant Frameworks

| Framework | GitHub Stars | Key Features | Best For | Chapter Fit |
|-----------|-------------|--------------|----------|-------------|
| **LangChain / LangGraph** | 126K / 26K | Stateful graphs, persistence, streaming, interrupt(), human-in-the-loop | Complex stateful workflows; enterprise production | Ch 22 (tool use), Ch 23 (orchestration) |
| **AutoGen / AG2** | 54K | Conversational multi-agent, flexible behaviors, GAIA benchmark leader | Data science workflows, research agents | Ch 23 (multi-agent) |
| **CrewAI** | 44K | Role-based agents, task decomposition, rapid prototyping (2-4 hours) | Quick multi-agent prototyping | Ch 23 (multi-agent patterns) |
| **LlamaIndex** | 47K | Agentic Document Workflows, event-driven async, workflow debugger | RAG-heavy agent systems, document agents | Ch 22 (tool use), Ch "Agentic RAG" |

### Tier 2: Provider SDKs

| Framework | GitHub Stars | Key Features | Best For | Chapter Fit |
|-----------|-------------|--------------|----------|-------------|
| **OpenAI Agents SDK** | 19K+ | Agents, Handoffs, Guardrails, Tracing; successor to Swarm | Clean multi-agent with OpenAI models | Ch 22, Ch 23 |
| **Anthropic Claude tool_use / Computer Use** | N/A (API) | MCP native, computer use, browser agent (Chrome), Dispatch (mobile) | Computer use agents, browser automation | Ch "Specialized Agents" |
| **Google ADK** | Growing | Event-driven runtime, Gemini Live streaming, multi-agent hierarchy, A2A native | Google ecosystem agents | Ch 22, Ch 23 |

### Tier 3: Specialized / Growing Frameworks

| Framework | GitHub Stars | Key Features | Best For | Chapter Fit |
|-----------|-------------|--------------|----------|-------------|
| **Microsoft Agent Framework** (SK + AutoGen) | ~22K (SK) | .NET + Python, MCP + A2A support, Process Framework, enterprise observability | Enterprise .NET agents | Ch 23 (production) |
| **Pydantic AI** | ~14K | Type-safe, model-agnostic, Logfire observability, YAML agent specs, Capabilities system | Type-safe Python agents | Ch 22 (tool use) |
| **smolagents (Hugging Face)** | ~15K | ~1,000 lines of code, code-first, Hub sharing, sandboxed execution, multimodal | Lightweight agents, education | Ch 22 (foundations) |
| **Mem0** | ~25K | Universal memory layer, graph-based memory (Mem0g), 26% accuracy boost | Agent long-term memory | Ch "Memory" |
| **Letta** (formerly MemGPT) | ~15K | OS-inspired memory hierarchy, tiered memory, self-improving agents | Stateful long-running agents | Ch "Memory" |

### Tier 4: Browser and Computer Use

| Framework | Key Features | Chapter Fit |
|-----------|--------------|-------------|
| **Playwright MCP** (Microsoft) | Accessibility-tree based, 2-5KB snapshots, cross-browser | Ch "Specialized Agents" |
| **browser-use** | Open-source browser automation for agents | Ch "Specialized Agents" |
| **Anthropic Computer Use** | Full desktop control, screenshot-based, Mac support (Mar 2026) | Ch "Specialized Agents" |
| **OSWorld / OS-Harm** | Benchmark + safety evaluation for desktop agents | Ch "Evaluation" |

### Framework Growth Metrics (2024-2026)

- Agent framework repos with 1,000+ stars: 14 (2024) to 89 (2025), a 535% increase
- 68% of production agents built on open-source frameworks
- Gartner: 40% of enterprise apps will embed AI agents by mid-2026 (up from <5% in early 2025)

---

## 3. Essential Topics for a Comprehensive Textbook

### A. Core Agent Patterns
- ReAct (Reasoning + Acting) loop
- Plan-and-Execute (PlanReAct)
- Reflection and self-critique
- Tool use and function calling
- Code generation and execution
- The perception-reasoning-action cycle
- Agent vs. chain vs. workflow distinction

### B. Tool Use and Protocols
- Function calling across providers (OpenAI, Anthropic, Google)
- Model Context Protocol (MCP): architecture, servers, clients, registry
- Agent-to-Agent Protocol (A2A): Agent Cards, task management, collaboration
- OpenAPI tool definitions
- Custom tool creation and schema design
- Tool selection and routing strategies
- The shift from Pipeline to Model-native paradigms

### C. Memory Architectures
- Buffer memory (conversation window)
- Summary memory (compression)
- Vector memory (semantic retrieval)
- Graph memory (relational structures, Mem0g)
- Episodic memory (interaction sequences)
- Semantic memory (facts and concepts)
- Procedural memory (learned expertise)
- OS-inspired memory hierarchies (Letta/MemGPT)
- Zettelkasten-style dynamic indexing (A-MEM)
- Production memory systems (Mem0, Letta, Zep)

### D. Planning Algorithms
- Task decomposition strategies
- Tree of Thoughts (ToT)
- PlanReAct architecture
- Modular Agentic Planner (MAP)
- Thought Management System (TMS)
- World models for planning
- Plan verification and correction
- Multi-step reasoning chains

### E. Multi-Agent Patterns
- Supervisor/Orchestrator-Worker
- Peer-to-peer (Mesh)
- Hierarchical (tree-structured delegation)
- Pipeline (sequential stages)
- Swarm (decentralized emergent coordination)
- Debate and consensus (MAD)
- Review pattern (MARS: Author-Reviewer-Meta-Reviewer)
- Voting and aggregation
- Role specialization and persona assignment
- Agent diversity and its impact on reasoning quality

### F. Agent Evaluation
- SWE-bench, WebArena, AgentBench, GAIA, OSWorld benchmarks
- Execution-based evaluation
- Multi-dimensional evaluation (accuracy, latency, cost, safety)
- Live benchmarks (FutureX)
- Agent-specific metrics (task completion rate, tool call accuracy, planning quality)
- Human evaluation protocols

### G. Agent Safety and Security
- Prompt injection defense (direct, indirect, cross-context)
- Execution sandboxing (Docker, E2B, Modal)
- Information-flow controls
- Guardrails frameworks (AGrail, NeMo Guardrails, Anthropic)
- Protocol-level security (MCP auth, A2A signed cards)
- Data exfiltration prevention
- Loop detection and termination
- 30+ cataloged attack techniques (prompt injection to protocol exploits)

### H. Production Agent Systems
- Monitoring and observability (OpenTelemetry, distributed tracing)
- Cost control (token budgets, caching, model routing)
- Error recovery (retries, circuit breakers, fallback routing)
- State persistence and checkpointing
- Human-in-the-loop (HITL) workflows
- Approval workflows (HumanLayer, LangGraph interrupt())
- Scaling patterns (horizontal agent scaling, load balancing)
- Multi-provider failover

### I. Specialized Agents
- Code agents (Claude Code, Devin, Cursor, SWE-agent, Codex CLI)
- Browser agents (Playwright MCP, browser-use, Claude for Chrome)
- Computer use agents (Anthropic Computer Use, OSWorld)
- Data analysis agents
- Research agents (Deep Research)
- Document agents (LlamaIndex ADW)

### J. Agent-Human Collaboration
- HITL design patterns (reactive validation)
- Approval workflows (@require_approval decorators)
- Escalation and handoff
- Multi-channel communication (Slack, email, Discord via HumanLayer)
- Trust calibration and progressive autonomy
- 99.9% accuracy with HITL vs. 92% AI-only (document extraction)

---

## 4. Proposed Chapter Structure: Expanded Part VI

The current Part VI has 2 chapters (Ch 22, Ch 23) with 9 total sections. The proposal below expands to 5 chapters with 25 sections.

### Chapter 22: AI Agent Foundations (5 sections)
*From passive LLMs to active agents: the core loop, patterns, and architectures.*

| Section | Title | Key Content |
|---------|-------|-------------|
| 22.1 | What Makes an Agent | Perception-reasoning-action cycle; agent vs. chain vs. workflow; autonomy spectrum; the four agentic patterns (reflection, tool use, planning, multi-agent) |
| 22.2 | The ReAct Pattern and Its Variants | ReAct loop; thought-action-observation; PlanReAct; Reflexion; self-critique loops |
| 22.3 | Agent Memory Systems | Buffer, summary, vector, graph, episodic, semantic, procedural memory; MemGPT/Letta OS-inspired hierarchy; A-MEM Zettelkasten; Mem0 production memory; Zep |
| 22.4 | Planning and Reasoning | Task decomposition; Tree of Thoughts; MAP; TMS; plan verification; world models; PlanBench evaluation |
| 22.5 | Reasoning Models as Agent Backbones | o1/o3, DeepSeek-R1, Gemini 2.5 Pro as agent cores; thinking tokens and tool use; extended thinking and agent loops |

**Labs:** Build a ReAct agent from scratch; implement buffer/vector/graph memory; compare planning strategies on PlanBench tasks
**Key Papers:** Yao et al. (ReAct), Yao et al. (ToT), MemGPT, A-MEM, MAP
**Key Frameworks:** smolagents (educational), LangGraph (production)

---

### Chapter 23: Tool Use, Function Calling, and Protocols (5 sections)
*Connecting agents to the world through tools, APIs, and interoperability standards.*

| Section | Title | Key Content |
|---------|-------|-------------|
| 23.1 | Function Calling Across Providers | OpenAI, Anthropic, Google function calling; schema design; parallel and sequential tool calls; forced vs. auto tool choice |
| 23.2 | Model Context Protocol (MCP) | Architecture (hosts, clients, servers); resources, tools, prompts; transport (stdio, SSE, HTTP); registry; building MCP servers |
| 23.3 | Agent-to-Agent Protocol (A2A) | Agent Cards; task lifecycle; capability discovery; context sharing; gRPC support; MCP vs. A2A complementarity |
| 23.4 | Custom Tool Design and Orchestration | Tool schema best practices; tool selection strategies; tool routing; error handling in tool calls; tool composition |
| 23.5 | Agentic RAG | Corrective RAG; Adaptive RAG; multi-hop retrieval agents; query rewriting agents; retrieval evaluation agents; ActiveRAG |

**Labs:** Build an MCP server; implement A2A Agent Cards; build a CRAG pipeline; compare function calling across 3 providers
**Key Papers:** MCP spec, A2A spec, CRAG, Adaptive-RAG, Toolformer
**Key Frameworks:** Anthropic MCP SDK, Google ADK (A2A), LlamaIndex (Agentic RAG)

---

### Chapter 24: Multi-Agent Systems (5 sections)
*Orchestrating multiple specialized agents into collaborative systems.*

| Section | Title | Key Content |
|---------|-------|-------------|
| 24.1 | Agent Frameworks Compared | LangGraph, CrewAI, AutoGen/AG2, OpenAI Agents SDK, Google ADK, smolagents, Pydantic AI, Microsoft Agent Framework; selection criteria; trade-offs |
| 24.2 | Multi-Agent Architecture Patterns | Supervisor, pipeline, mesh, swarm, hierarchical; pattern selection guide; when to use which |
| 24.3 | Agent Communication and Coordination | Debate and consensus (MAD); review pattern (MARS); voting; role specialization; persona assignment; diversity effects on reasoning |
| 24.4 | Agentic Workflows and State Management | Event-driven architectures; state persistence; checkpointing; conditional branching; parallel execution; LangGraph graphs; LlamaIndex workflows |
| 24.5 | Human-in-the-Loop Agent Systems | HITL design patterns; approval workflows; LangGraph interrupt(); HumanLayer SDK; escalation; progressive autonomy; multi-channel integration |

**Labs:** Build supervisor pattern with LangGraph; implement debate protocol with 3 diverse models; build HITL approval workflow; compare CrewAI vs. AutoGen on same task
**Key Papers:** Multi-Agent Collaboration survey, MALT, MARS, Diversity of Thought, Persona Inconstancy
**Key Frameworks:** LangGraph, CrewAI, AutoGen, OpenAI Agents SDK

---

### Chapter 25: Specialized Agents (5 sections)
*Code agents, browser agents, computer use agents, and domain-specific agent applications.*

| Section | Title | Key Content |
|---------|-------|-------------|
| 25.1 | Code Generation and Execution Agents | Claude Code, Devin, Cursor, SWE-agent, Codex CLI; sandboxed execution; test-driven agent loops; SWE-bench evaluation; agent scaffolding vs. model quality |
| 25.2 | Browser Automation Agents | Playwright MCP; accessibility-tree approach; browser-use; Claude for Chrome; BrowserGym; WebArena evaluation |
| 25.3 | Computer Use Agents | Anthropic Computer Use API; screenshot-based interaction; OSWorld benchmark; desktop automation; OS-Harm safety; Agent S breakthrough |
| 25.4 | Research and Data Analysis Agents | Deep Research agents; document agents (LlamaIndex ADW); data analysis pipelines; multi-source synthesis |
| 25.5 | Building Domain-Specific Agents | Customer service agents; legal agents; healthcare agents; financial agents; pattern: domain knowledge + tool set + guardrails |

**Labs:** Build a code agent with test-driven loop; create a browser agent with Playwright MCP; implement a research agent with web search and summarization
**Key Papers:** SWE-bench, WebArena, OSWorld, OS-Harm
**Key Frameworks:** Claude Code, Playwright MCP, LlamaIndex ADW

---

### Chapter 26: Agent Safety, Evaluation, and Production (5 sections)
*Making agents reliable, safe, and production-ready.*

| Section | Title | Key Content |
|---------|-------|-------------|
| 26.1 | Agent Evaluation and Benchmarks | SWE-bench, WebArena, AgentBench, GAIA, OSWorld; execution-based eval; multi-dimensional metrics; live benchmarks; building custom evals |
| 26.2 | Agent Safety and Security | Prompt injection (direct, indirect, cross-context); data exfiltration; protocol exploits; 30+ attack taxonomy; defense-in-depth |
| 26.3 | Sandboxing and Guardrails | Docker/E2B/Modal sandboxes; input/output guardrails; AGrail; NeMo Guardrails; loop detection; resource quotas; egress allowlists |
| 26.4 | Production Observability and Cost Control | OpenTelemetry tracing; agent-level metrics; token budgets; caching; model routing; multi-provider failover; cost tracking dashboards |
| 26.5 | Error Recovery and Resilience | Retries; circuit breakers; state checkpointing; fallback routing; dead-letter handling; graceful degradation; monitoring alerts |

**Labs:** Run agent on SWE-bench subset; implement sandboxed execution; build cost tracking dashboard; add circuit breaker to agent pipeline
**Key Papers:** ASB (ICLR 2025), AGrail (ACL 2025), Systems Security for Agentic Computing, From Prompt Injections to Protocol Exploits
**Key Frameworks:** E2B, Docker, NeMo Guardrails, OpenTelemetry, LangSmith

---

## Summary of Changes

| Aspect | Current | Proposed |
|--------|---------|----------|
| Chapters | 2 (Ch 22, 23) | 5 (Ch 22-26) |
| Sections | 9 | 25 |
| Memory coverage | Brief (in 22.1) | Full chapter section (22.3) with Mem0, Letta, A-MEM |
| Tool protocols | MCP mentioned | Dedicated sections for MCP (23.2) and A2A (23.3) |
| Agentic RAG | Not covered | Dedicated section (23.5) |
| Specialized agents | Code agents only (22.4) | Full chapter (Ch 25): code, browser, computer use, research, domain |
| Safety/evaluation | Minimal | Full chapter (Ch 26) with benchmarks, sandboxing, observability |
| Frameworks | LangGraph, CrewAI | All 12+ major frameworks compared |
| HITL | Brief mention | Dedicated section (24.5) |
| Planning | ReAct only | ToT, MAP, TMS, PlanReAct, task decomposition (22.4) |

---

## Key Numbers to Include in the Textbook

- 97M+ monthly MCP SDK downloads (as of late 2025)
- 6,400+ registered MCP servers (Feb 2026)
- 535% growth in agent framework repos with 1K+ stars (2024-2025)
- 68% of production agents on open-source frameworks
- 40% of enterprise apps projected to embed agents by mid-2026 (Gartner)
- 85% of developers regularly use AI coding tools by end of 2025
- Agent S: 72.6% on OSWorld (surpassing human 72.36%)
- Claude Code: 80.9% on SWE-bench
- CRAG defense: reduces prompt injection success from 73.2% to 8.7%
- HITL accuracy: 99.9% vs. 92% AI-only in document extraction

---

## Note on Renumbering

The proposed expansion adds chapters 24, 25, 26 within Part VI. This means the current Part VII (Multimodal, module-24/25) and later parts would need renumbering. The alternative is to keep chapters 22-23 and add 3 new chapters as 24-26, shifting the rest of the book forward. Given the book already has modules numbered 22-30, the cleanest approach would be:

- Part VI: Ch 22 (Foundations), Ch 23 (Tools/Protocols), Ch 24 (Multi-Agent), Ch 25 (Specialized), Ch 26 (Safety/Eval/Production)
- Part VII onward: renumber from Ch 27+

This is a significant structural change but reflects the field's explosive growth, where agentic AI is now the single largest topic area in LLM development.

---

## Sources

- [Agentic AI Comprehensive Survey (Springer)](https://link.springer.com/article/10.1007/s10462-025-11422-4)
- [Landscape of Emerging AI Agent Architectures (arXiv)](https://arxiv.org/abs/2404.11584)
- [Multi-Agent Collaboration Mechanisms Survey (arXiv)](https://arxiv.org/html/2501.06322v1)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [A Year of MCP Review](https://www.pento.ai/blog/a-year-of-mcp-2025-review)
- [Why MCP Won (The New Stack)](https://thenewstack.io/why-the-model-context-protocol-won/)
- [Google A2A Protocol Announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [A2A Protocol Upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade)
- [AI Agent Frameworks Comparison 2026 (Turing)](https://www.turing.com/resources/ai-agent-frameworks)
- [Top 10 AI Agent Frameworks (o-mega)](https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026)
- [Definitive Guide to Agentic Frameworks 2026](https://softmaxdata.com/blog/definitive-guide-to-agentic-frameworks-in-2026-langgraph-crewai-ag2-openai-and-more/)
- [OpenAI Agents SDK Review](https://mem0.ai/blog/openai-agents-sdk-review)
- [Google ADK Overview](https://google.github.io/adk-docs/get-started/about/)
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Pydantic AI](https://ai.pydantic.dev/)
- [smolagents (Hugging Face)](https://huggingface.co/docs/smolagents/en/index)
- [Best AI Coding Agents 2026 (Codegen)](https://codegen.com/blog/best-ai-coding-agents/)
- [Anthropic Computer Use](https://www.anthropic.com/news/3-5-models-and-computer-use)
- [Anthropic Claude Desktop Agent (Mar 2026)](https://www.cnbc.com/2026/03/24/anthropic-claude-ai-agent-use-computer-finish-tasks.html)
- [OSWorld Benchmark (NeurIPS 2024)](https://os-world.github.io/)
- [AI Agent Benchmarks Guide (Evidently)](https://www.evidentlyai.com/blog/ai-agent-benchmarks)
- [Agent Security Bench (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf)
- [AGrail (ACL 2025)](https://aclanthology.org/2025.acl-long.399.pdf)
- [Securing AI Agents Against Prompt Injection (arXiv)](https://arxiv.org/abs/2511.15759)
- [CRAG Paper (arXiv)](https://arxiv.org/abs/2401.15884)
- [Agentic RAG Survey (arXiv)](https://arxiv.org/html/2501.09136v1)
- [MemGPT Paper (arXiv)](https://arxiv.org/abs/2310.08560)
- [A-MEM Paper (arXiv)](https://arxiv.org/abs/2502.12110)
- [Mem0 Paper (arXiv)](https://arxiv.org/abs/2504.19413)
- [Letta (GitHub)](https://github.com/letta-ai/letta)
- [Playwright MCP (GitHub)](https://github.com/microsoft/playwright-mcp)
- [Agent Orchestration Patterns (HatchWorks)](https://hatchworks.com/blog/ai-agents/orchestrating-ai-agents/)
- [AI Agent Observability (TrueFoundry)](https://www.truefoundry.com/blog/ai-agent-observability-tools)
- [HITL Best Practices (Permit.io)](https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo)
- [ReAct Paper (arXiv)](https://arxiv.org/abs/2210.03629)
- [Tree of Thoughts Paper (arXiv)](https://arxiv.org/pdf/2305.10601)
- [Modular Agentic Planner (Nature)](https://www.nature.com/articles/s41467-025-63804-5)
