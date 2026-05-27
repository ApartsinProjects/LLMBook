# 1428_Agents_Planning — Per-Slide Summary

**Source file:** `1428_Agents_Planning.pptx`
**Source folder:** `SlidesPool/1420_LLM_Agents/`
**Drive link:** https://drive.google.com/file/d/1M4UnPBwcubo6V2Ivnze-R1Zevr6k2Qv0/view
**Slide count (exact, via python-pptx):** 25
**Extraction:** Local parse + slide PNG render. Bullets describe three planning patterns; code screenshots illustrate LangGraph implementations.

---

## Slide 1 — Agents: Planning
Title slide for the deck on planning-driven agents.

## Slide 2 — Plan ahead
Sub-title introducing ReWoo (Reasoning WithOut Observation).

## Slide 3 — Generate plan in a single pass
A diagram of generating the full plan in a single LLM pass.

## Slide 4 — Tasks include tool calls with variables
Plan tasks include tool calls with variables; variable values come from previous tasks.

## Slide 5 — Define state
A screenshot defining the graph state: parse the plan_string response into steps and a results dictionary of variables E1...

## Slide 6 — Planner
Two screenshots showing the planner LLM and prompt.

## Slide 7 — Plan Example
Three screenshots showing an example plan with tool calls and variable references.

## Slide 8 — Planner Node
A screenshot of the planner node implementation.

## Slide 9 — Executor
A screenshot of the executor node that runs the planned tool calls in order, substituting variables.

## Slide 10 — Solver
The solver generates the final response from the executed plan.

## Slide 11 — Build Graph
Two screenshots wiring the planner, executor, and solver into a LangGraph graph.

## Slide 12 — Plan and Execute
Section divider for the iterative Plan-and-Execute pattern.

## Slide 13 — Flow
Make multiple web searches to achieve the task and update the plan after each task result, rather than committing to a single plan up front.

## Slide 14 — Tool: Search
A screenshot of the search tool.

## Slide 15 — Execution Agent
Two screenshots of the execution agent that runs each step.

## Slide 16 — State
A screenshot defining the graph state.

## Slide 17 — Planning: Scheme and chain
A screenshot of the planning schema and chain.

## Slide 18 — Re-Plan Step
A screenshot of the re-plan step that revises the plan after observing results.

## Slide 19 — Create Graph Nodes
A screenshot creating the graph nodes (planner, executor, re-planner).

## Slide 20 — Conditional Edge
A screenshot of the conditional edge that decides whether to continue execution or stop.

## Slide 21 — Graph
Two screenshots of the assembled graph; the async node is internally wrapped as a stateful step.

## Slide 22 — Baby-AGI
Section divider for Baby-AGI as the first fully autonomous agent example.

## Slide 23 — Core Agent
A diagram of the Baby-AGI core agent loop.

## Slide 24 — Original Baby-AGI Flow
The original Baby-AGI flow: task creation, task prioritization, task execution.

## Slide 25 — UI Interface
A screenshot of the Baby-AGI UI interface.

---

## Deck-level takeaway
The deck contrasts three planning patterns for autonomous agents. ReWoo generates the entire plan in a single LLM pass, with tool-call tasks that consume variables from earlier tasks, then executes the plan and solves to a final answer. Plan-and-Execute is iterative: plan, execute one step, observe, re-plan, repeat until a stopping condition is met, which handles open-ended web-search-style tasks better. Baby-AGI, as a historical anchor, runs the same loop with explicit task creation, task prioritization, and task execution sub-modules, illustrating the first fully autonomous agent and its UI.
