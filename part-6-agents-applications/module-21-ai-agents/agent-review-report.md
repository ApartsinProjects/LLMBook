# Module 21: AI Agents, 36-Agent Deep Review Report

**Date:** 2026-03-26
**Files reviewed:** index.html, section-21.1.html, section-21.2.html, section-21.3.html, section-21.4.html

---

## Agent 00: Chapter Lead

**Overall assessment: STRONG**

The module covers a coherent and well-scoped topic: AI agents from foundations through planning to code execution. The four sections map cleanly to the learning objectives listed in index.html. The sections flow logically: foundations (21.1) to tool use (21.2) to planning (21.3) to code agents (21.4).

**Issues:**
- No chapter-plan.md exists beyond a placeholder README.md (minor, not blocking)
- Missing epigraphs on all four sections (other modules have them)
- Missing section-level opening "why should I care" hooks on most subsections within each section

---

## Agent 01: Curriculum Alignment

**Overall alignment: STRONG**

All learning objectives from index.html are covered:
- Perception-reasoning-action loop: 21.1 Section 1-3 (thorough)
- Function calling with OpenAI/Anthropic: 21.2 Sections 2-3 (thorough with code)
- Tool schema design: 21.2 Section 4 (solid)
- ReAct agents: 21.1 Section 3 (thorough with code)
- Planning strategies: 21.3 Sections 2-5 (thorough)
- Human-in-the-loop: 21.3 Section 6 (solid)
- Code generation agents: 21.4 Sections 1-5 (thorough)
- Token budgets: 21.1 Section 6 (solid)
- Agent evaluation metrics: partially covered in 21.1 Section 7 (failure modes) but **no dedicated evaluation/metrics section**

**Coverage Gap:**
- TIER 1: Learning objective "Evaluate agent performance using task completion, efficiency, and safety metrics" has no dedicated coverage. Section 21.1 discusses failure modes but does not cover benchmarks (SWE-bench, GAIA, AgentBench, etc.) or evaluation frameworks.

**Scope Creep:** None detected. All content is well-scoped.

---

## Agent 02: Deep Explanation

**Overall depth: STRONG**

All four major concepts pass the four-question test (what, why, how, when). Particularly strong:
- The perception-reasoning-action loop explanation in 21.1
- The function calling lifecycle in 21.2
- LATS explanation in 21.3

**Issues:**
- TIER 2: Section 21.3 LATS: the UCT formula is used but the intuition behind exploration vs. exploitation tradeoff could use one more sentence of explanation
- TIER 3: Section 21.2 MCP: the protocol details (JSON-RPC transport) are mentioned but not explained; a sentence on why JSON-RPC was chosen would help
- TIER 3: Section 21.4 mentions Firecracker microVMs vs. gVisor but does not explain the security tradeoff between them

---

## Agent 03: Teaching Flow

**Overall flow: SMOOTH**

Concept ordering is correct across all sections. Each section builds on the previous one. The progression from abstract (what is an agent) to concrete (build a code agent) is well-paced.

**Issues:**
- TIER 2: Section 21.1 jumps from ReAct (Section 3) to cognitive architectures (Section 4) without a bridge sentence
- TIER 2: Section 21.3 transitions from LATS (Section 4) to LLM Compiler (Section 5) abruptly; these are quite different approaches and need a connecting sentence
- TIER 3: No forward preview in 21.4 about what Module 22 (multi-agent systems) will cover

---

## Agent 04: Student Advocate

**Clarity: MOSTLY CLEAR**
**Microlearning structure: WELL-STRUCTURED**

The sections are well-chunked with clear subsections. Code examples appear promptly after concepts.

**Issues:**
- TIER 2: Section 21.1 introduces "cognitive architecture" (Section 4) without defining it first; a student would wonder what this term means
- TIER 2: Section 21.2 A2A protocol section (Section 7) is brief; students may wonder how A2A differs from simple REST APIs between services
- TIER 3: Section 21.3 uses "UCT (Upper Confidence Bound for Trees)" without explaining what "upper confidence bound" means intuitively

---

## Agent 05: Cognitive Load

**Overall load: MANAGEABLE**

Sections are well-paced with code, diagrams, tables, and callouts breaking up prose. The density is appropriate for intermediate/advanced content.

**Issues:**
- TIER 3: Section 21.1 Section 4 (cognitive architectures + state machines) introduces AgentState, AgentContext, StatefulAgent, and state machine transitions in one subsection; could benefit from a brief "what just happened" summary after the code block
- TIER 3: Section 21.2 Section 6 (MCP) + Section 7 (A2A) are dense with new protocols; a comparison callout would help

---

## Agent 06: Example and Analogy

**Overall quality: STRONG**

Good use of concrete examples throughout: weather API, product search, sales analysis, competitor research.

**Issues:**
- TIER 2: Section 21.1 introduces the perception-reasoning-action loop but the only analogy is implicit; adding an explicit analogy (e.g., comparing to a detective investigating a case) would strengthen retention
- TIER 2: Section 21.2 MCP section uses the USB analogy but it appears only once; reinforcing it would help
- TIER 3: Section 21.3 LATS could benefit from a game-tree analogy (chess) to ground the tree search concept

---

## Agent 07: Exercise Designer

**Exercise quality: GOOD**

Each section has a Knowledge Check quiz with 4-5 questions. Questions require genuine understanding, not just recall.

**Issues:**
- TIER 2: No hands-on coding exercises in 21.1 (only conceptual questions); adding a "build a minimal ReAct agent" exercise would reinforce the code shown
- TIER 3: Section 21.3 lab is good but could add a "stretch goal" for students who finish early

---

## Agent 08: Code Pedagogy

**Code quality: STRONG**

All code examples are pedagogically motivated, well-commented, and build progressively. The progression from simple (reflect_and_improve) to complex (StatefulAgent, SandboxedAnalyst) is excellent.

**Issues:**
- TIER 2: Section 21.2 Anthropic code example (line 289) uses model name "claude-sonnet-4-20250514" which may need updating as models evolve; consider using a comment noting the model name should be updated
- TIER 3: Section 21.1 ReAct agent uses text parsing (ACTION: tool_name(args)); the note correctly says production would use native function calling, but a brief "here is what the native version looks like" pointer to 21.2 would strengthen the bridge
- TIER 3: Section 21.4 CodeSecurityChecker blocks `open` builtin, but the data analysis code uses `pd.read_csv` which internally calls open; a note about this nuance would be educational

---

## Agent 09: Visual Learning

**Visual quality: STRONG**

Excellent SVG diagrams throughout: perception-reasoning-action loop, function calling lifecycle, planning comparison, reflection loop, LATS tree, code interpreter loop, data analysis pipeline, agent state machine. All use the consistent book color palette.

**Issues:**
- TIER 2: Section 21.2 MCP/A2A section: no diagram comparing MCP (vertical) vs A2A (horizontal) connections; this concept cries out for a visual
- TIER 3: Section 21.1 four agentic patterns diagram is good but could label the connecting relationships between patterns

---

## Agent 10: Misconception Analyst

**Issues:**
- TIER 1: Section 21.1 "Agents vs. Chains vs. Workflows" could lead students to think these are strict categories when in practice the boundaries are blurry. Add a note: "In practice, many systems combine elements of all three."
- TIER 2: Section 21.4 "static code filtering alone is never sufficient" is stated correctly but students may still over-rely on it. The callout is good but could be more prominent.
- TIER 3: Students may confuse MCP (tool protocol) with A2A (agent protocol); adding a one-line disambiguation when A2A is first mentioned would help

---

## Agent 11: Fact Integrity

**Factual accuracy: STRONG**

All technical claims verified. ReAct attribution (Yao et al., 2022) is correct. LATS, BabyAGI, and LLM Compiler are correctly attributed.

**Issues:**
- TIER 2: Section 21.2 states Anthropic recommends "under 20" tools; this should be qualified as a performance recommendation, not a hard limit
- TIER 2: Section 21.3 attributes plan-and-execute to "LangGraph team and inspired by the BabyAGI project"; while accurate, noting that plan-and-execute as a general AI pattern predates both would be more precise
- TIER 3: Section 21.2 says Google proposed A2A "in 2025"; confirm this is the correct year (it is: April 2025)

---

## Agent 12: Terminology Keeper

**Consistency: STRONG**

Terms are used consistently across sections. "Tool use" and "function calling" are correctly treated as synonyms with an explicit note.

**Issues:**
- TIER 3: Section 21.1 uses "perception-reasoning-action loop" and later "perception-reasoning-action cycle"; standardize to one term
- TIER 3: Section 21.3 refers to "plan-and-execute" with hyphens consistently, which is good

---

## Agent 13: Cross-Reference

**Cross-references: GOOD**

References to Module 19 (RAG), Module 20 (conversational AI), and Module 22 (multi-agent) exist. Tool use in 21.1 correctly points to "Section 21.2 covers this in depth."

**Issues:**
- TIER 2: Section 21.1 mentions RAG (Module 19) for semantic memory but does not link back to Module 10 for prompt engineering techniques used in agent prompts
- TIER 2: Section 21.4 SWE agents section does not reference Module 22 (multi-agent), but SWE agents like Devin use multi-agent architectures internally
- TIER 3: Section 21.2 native tool use training could reference Module 08 or 09 (API training, RLHF)

---

## Agent 14: Narrative Continuity

**Continuity: STRONG**

The chapter reads as one coherent narrative. The thematic thread of "the agent loop" runs through all four sections. The Big Picture callout at the top of each section effectively frames the content.

**Issues:**
- TIER 3: The closing of 21.4 could briefly reflect on the full module journey (from "what is an agent" to "building production code agents")

---

## Agent 15: Style and Voice

**Voice: CONSISTENT**

The writing is authoritative, clear, and appropriately semi-formal. Technical precision is maintained without stiffness.

**Issues:**
- TIER 1: No em dashes or double dashes found in prose (PASS)
- TIER 3: A few passages in 21.3 are slightly more formal/dense than the rest; minor smoothing would help
- TIER 3: The phrase "This mechanism underpins every practical agent" in 21.2 Big Picture is slightly hyperbolic; adding "nearly" would be more precise

---

## Agent 16: Engagement Designer

**Engagement: GOOD**

Good variety of callout types (Big Picture, Key Insight, Note, Warning). Code examples and diagrams maintain interest.

**Issues:**
- TIER 1: Missing epigraphs on all four sections; other modules have humorous/thought-provoking opening quotes that set the tone
- TIER 2: Section 21.1 could open with a more vivid hook; the current opening is solid but not grabbing
- TIER 3: Section 21.3 is the most "textbook-like" section and could use a surprising fact or counterintuitive example early on

---

## Agent 17: Senior Editor

**Editorial quality: STRONG**

Prose is clear and professional. Sentence variety is good. No major wording issues.

**Issues:**
- TIER 3: A few sentences could be tightened (minor wordiness in some paragraphs)
- TIER 3: Some callout titles use the gear icon (&#9881;) inconsistently with the "Key Insight" label in 21.3 and 21.4

---

## Agent 18: Research Scientist

**Research depth: GOOD**

Good citations: ReAct (Yao et al., 2022), LATS, LLM Compiler (UC Berkeley, 2023), Self-Debugging (Chen et al., 2023), BabyAGI.

**Issues:**
- TIER 2: Missing mention of Toolformer (Schick et al., 2023) which is a foundational paper on tool-use training
- TIER 3: Could mention the "Voyager" agent (Minecraft) as an example of open-ended exploration agents
- TIER 3: Could mention the "OS-Copilot" or "OpenDevin" projects as current examples of SWE agents

---

## Agent 19: Structural Architect

**Structure: STRONG**

Four sections with clear progression. Each section follows the pattern: Big Picture > numbered main sections > code examples > quiz > takeaways. Internal hierarchy is consistent.

**Issues:**
- TIER 3: Section 21.3 has numbered sections ("1. Why Planning Matters") through "7. Combining Patterns" plus a Lab; this is a lot of sections and could benefit from grouping into two H2-level themes

---

## Agent 20: Content Update Scout

**Currency: CURRENT**

Content reflects 2024-2025 state of the art. MCP, A2A, E2B, Modal are all current.

**Issues:**
- TIER 2: Missing mention of the OpenAI Agents SDK (released early 2025) which is becoming a popular framework for building agents
- TIER 2: Missing mention of Claude's "computer use" capability as a form of code/tool agent
- TIER 3: Missing mention of the "function calling" vs. "tool use" terminology evolution (OpenAI initially called it "function calling," now uses "tools")

---

## Agent 21: Self-Containment Verifier

**Self-containment: STRONG**

All concepts are explained within the module or reference earlier modules. No external knowledge is assumed beyond stated prerequisites.

**Issues:**
- TIER 3: Section 21.3 mentions "Monte Carlo Tree Search" without a brief explanation of what Monte Carlo methods are; most software engineers would know this, but a parenthetical would be safe

---

## Agent 22: Title and Hook Architect

**Titles: GOOD**

Section titles are clear and descriptive. Subtitles add specificity.

**Issues:**
- TIER 1: Missing epigraphs on all sections (high-impact engagement tool used in other modules)
- TIER 2: Section 21.1 title "Foundations of AI Agents" is functional but not compelling; consider "What Makes an AI Agent Think?" or similar
- TIER 3: Section 21.3 subtitle is long; consider trimming

---

## Agent 23: Project Catalyst

**Project ideas: GOOD**

The labs in 21.3 and 21.4 are excellent hands-on projects. The ReAct agent in 21.1 is buildable.

**Issues:**
- TIER 2: No explicit "You could build this" callout in 21.2; suggesting a personal MCP server project would be motivating
- TIER 3: A capstone suggestion tying all four sections together would be valuable

---

## Agent 24: Aha-Moment Engineer

**Aha moments: GOOD**

The ReAct trace example in 21.1 is an effective aha moment. The reactive vs. planning agent diagram in 21.3 clearly shows the contrast.

**Issues:**
- TIER 2: Section 21.2 could benefit from a "before/after tool use" example showing the same query with and without tools, demonstrating why tools are necessary
- TIER 3: Section 21.4 self-debugging section could show a concrete before/after of error correction

---

## Agent 25: First-Page Converter

**Openings: GOOD**

Big Picture callouts effectively establish why each section matters.

**Issues:**
- TIER 1: No epigraphs (would add personality and tone-setting to each section opener)
- TIER 2: Section 21.1 opening could start with a more vivid scenario (e.g., "Imagine asking an AI to plan your vacation, book the flights, and write the packing list")

---

## Agent 26: Visual Identity Director

**Visual consistency: STRONG**

All diagrams use the same color palette (blue #3498db, purple #8e44ad, green #27ae60, yellow #f39c12, red #e94560). Callout system is consistent. Code blocks use the same dark theme.

**Issues:**
- TIER 1: Missing epigraph styling (other modules have blockquote.epigraph CSS); needs to be added
- TIER 3: Figure numbering is inconsistent; 21.1 uses "Figure 21.1, 21.2, 21.3" while 21.3 uses "Figure 1, 2, 3" and 21.4 uses "Figure 1, 2"; standardize to "Figure 21.X" format

---

## Agent 27: Research Frontier Mapper

**Frontier coverage: MINIMAL**

No explicit "where this is heading" or "open research questions" section exists.

**Issues:**
- TIER 2: Missing a brief "open questions" callout or section at the end of 21.4 discussing: agent benchmarking challenges, long-horizon agent reliability, constitutional AI for agents, multi-modal agents

---

## Agent 28: Demo/Simulation Designer

**Interactive elements: ADEQUATE**

Code examples are runnable and demonstrative.

**Issues:**
- TIER 3: Section 21.1 could suggest a "try modifying the max_steps parameter and observe how it affects agent behavior" demo
- TIER 3: Section 21.4 could suggest uploading a personal CSV to the data analysis agent

---

## Agent 29: Memorability Designer

**Memorability: GOOD**

Key phrases: "perception-reasoning-action loop," "start with the simplest approach that works," "tool descriptions are the most important part."

**Issues:**
- TIER 2: No compact schema or mnemonic for the four agentic patterns; a "RTPM" acronym (Reflection, Tool use, Planning, Multi-agent) or similar would aid recall
- TIER 3: The "seatbelt and airbag" analogy for code filtering + sandboxing in 21.4 is excellent and memorable

---

## Agent 30: Skeptical Reader

**Distinctiveness: GOOD**

The module differentiates itself through practical code-first approach, real API examples (OpenAI + Anthropic), and coverage of MCP/A2A which many textbooks miss.

**Issues:**
- TIER 2: The ReAct explanation in 21.1 is standard textbook fare; adding a unique perspective or a "common mistake when implementing ReAct" would differentiate
- TIER 3: The plan-and-execute section in 21.3 is solid but not surprising; could add a "when planning goes wrong" example

---

## Agent 31: Plain Language Rewriter

**Language clarity: STRONG**

Prose is generally clear and direct. Technical terms are well-explained.

**Issues:**
- TIER 3: Section 21.3 Big Picture: "Without planning, an agent reacts to each user message in isolation, choosing one tool at a time" could be simplified to "Without planning, an agent picks one tool at a time and hopes for the best"
- TIER 3: A few sentences in 21.2 Section 9 (native tool use training) use slightly academic phrasing

---

## Agent 32: Sentence Flow Smoother

**Prose rhythm: GOOD**

Sentence lengths are varied. Paragraphs flow well.

**Issues:**
- TIER 3: Section 21.1 opening paragraph has three sentences of similar length and structure; varying the rhythm would improve readability
- TIER 3: A few paragraphs start with "This..." which is a weak opener

---

## Agent 33: Jargon Gatekeeper

**Jargon management: GOOD**

Most terms are defined on first use. Acronyms are expanded.

**Issues:**
- TIER 2: "UCT (Upper Confidence Bound for Trees)" in 21.3 needs a brief intuitive explanation (it balances trying known-good paths vs. exploring unknown ones)
- TIER 3: "Firecracker microVMs" in 21.4 should briefly explain what Firecracker is (Amazon's lightweight VM technology)
- TIER 3: "gVisor" in 21.4 should briefly explain what it is (Google's application kernel for container security)

---

## Agent 34: Micro-Chunking Editor

**Chunking: GOOD**

Sections are well-chunked with clear H2/H3/H4 hierarchy. Lists, tables, and code blocks break up prose effectively.

**Issues:**
- TIER 3: Section 21.1 Section 5 (Agent Memory Systems) could use a comparison table for the three memory types instead of sequential subsections
- TIER 3: Section 21.2 Section 9 (Native Tool Use Training) is two paragraphs with no visual break; a brief list or callout would improve scannability

---

## Agent 35: Reader Fatigue Detector

**Fatigue risk: LOW**

Good pacing throughout. Code examples, diagrams, and callouts prevent monotony. The longest pure-prose stretches are 3-4 paragraphs, which is acceptable.

**Issues:**
- TIER 3: Section 21.3 middle sections (LATS code + LLM Compiler code) are back-to-back dense code blocks; a brief "take a breath" summary between them would help
- TIER 3: Section 21.4 is the longest section and comes last; fatigue may set in. The lab at the end is engaging, which helps.

---

## Summary of All Fixes by Tier

### TIER 1 (Blocking/High-Impact): 4 fixes
1. Add epigraphs to all four sections (Agents 16, 22, 25, 26)
2. Add epigraph CSS styling to all sections (Agent 26)
3. Add a brief note in 21.1 that chains/workflows/agents are a spectrum, not strict categories (Agent 10)
4. Standardize figure numbering to "Figure 21.X" format across all sections (Agent 26)

### TIER 2 (Important): 22 fixes
1. Add bridge sentence between ReAct and cognitive architectures in 21.1 (Agent 03)
2. Add bridge sentence between LATS and LLM Compiler in 21.3 (Agent 03)
3. Define "cognitive architecture" before using it in 21.1 (Agent 04)
4. Add intuitive explanation of UCT in 21.3 (Agents 04, 33)
5. Add detective analogy for perception-reasoning-action loop in 21.1 (Agent 06)
6. Reinforce USB analogy for MCP in 21.2 (Agent 06)
7. Add LATS game-tree analogy in 21.3 (Agent 06)
8. Qualify Anthropic "under 20 tools" recommendation in 21.2 (Agent 11)
9. Add note about plan-and-execute predating LangGraph/BabyAGI in 21.3 (Agent 11)
10. Add cross-reference to Module 10 (prompt engineering) in 21.1 (Agent 13)
11. Mention Toolformer in 21.2 (Agent 18)
12. Add MCP/A2A comparison callout in 21.2 (Agent 05)
13. Add "mnemonic" for four agentic patterns in 21.1 (Agent 29)
14. Add brief open research questions callout in 21.4 (Agent 27)
15. Add "before/after tool use" contrast in 21.2 (Agent 24)
16. Explain MCP vs A2A distinction more clearly when A2A first appears (Agent 10)
17. Note about OpenAI Agents SDK in 21.2 (Agent 20)
18. Add more vivid opening scenario to 21.1 (Agent 25)
19. Add "You could build this" project callout to 21.2 (Agent 23)
20. Add forward reference from 21.4 to Module 22 (Agent 03)
21. Note model name may change in Anthropic code example (Agent 08)
22. Add "common mistake" note for ReAct implementation (Agent 30)

### TIER 3 (Polish): 30+ minor fixes
(Listed above but lower priority; will apply where feasible)

---

## Overall Module Assessment

| Dimension | Rating |
|-----------|--------|
| Curriculum alignment | STRONG |
| Technical accuracy | STRONG |
| Explanation depth | STRONG |
| Teaching flow | SMOOTH |
| Code quality | STRONG |
| Visual design | STRONG |
| Engagement | GOOD (needs epigraphs) |
| Memorability | GOOD |
| Accessibility | MOSTLY CLEAR |
| Currency | CURRENT |

**Overall: STRONG module that needs epigraphs, a few bridge sentences, and minor polish.**
