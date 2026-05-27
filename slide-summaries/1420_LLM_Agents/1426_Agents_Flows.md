# 1426_Agents_Flows — Per-Slide Summary

**Source file:** `1426_Agents_Flows.pptx`
**Source folder:** `SlidesPool/1420_LLM_Agents/`
**Drive link:** https://drive.google.com/file/d/13QX16zOi2348zzUzEJh8DgB0eudrdM5z/view
**Slide count (exact, via python-pptx):** 44
**Extraction:** Local parse + slide PNG render. Bullets describe Reflection, RefleXion, Code Assistant, and WebVoyager patterns; code screenshots implement each in LangGraph.

---

## Slide 1 — Agentic Flows
Title slide for the deck on agentic flow patterns.

## Slide 2 — Reflection
Reflection improves quality by critiquing previous actions.

## Slide 3 — Generation Node
Code screenshot of the generation node.

## Slide 4 — Reflection Node
Code screenshot of the reflection node that critiques the generated output.

## Slide 5 — LangGraph reflection
Code screenshot of the LangGraph reflection chain; MessageGraph uses message-based state.

## Slide 6 — RefleXion
Section divider for RefleXion.

## Slide 7 — RefleXion
A Revisor node improves the answer and generates citations from external data, while keeping memory of all critiques and using a search tool to refine. Use case: search the web, generate an answer supported by reference citations. Two roles: Responder (agent with self-reflection that reflects on its response and improves on self-criticism) and Revisor (responds based on previous reflections and appends references).

## Slide 8 — Expected LLM responses (structured)
Two screenshots showing the expected structured response with reflection. A special prompt asks the LLM to return JSON with these fields.

## Slide 9 — Structural query for responder & reflector
Two chains are received: a generator LLM chain and a validator. The validator ensures the LLM returns valid JSON with the requested fields, providing a fixing request and repeating until parsed successfully.

## Slide 10 — Responder prompt template
A screenshot of the responder prompt template.

## Slide 11 — Initialize responder
Initialize the responder using BaseModel classes as the tool schema to generate structured output that can be parsed; ToolParser parses the function call into the structure, using a dummy function as class name that is converted to a search in the tool node.

## Slide 12 — Revision output
A screenshot of the revision output schema.

## Slide 13 — Revision chain
A screenshot of the revision chain wiring.

## Slide 14 — Tool node
The tool node does the actual parsing of function calls.

## Slide 15 — RefleXion agent in LangGraph
Two screenshots assembling the RefleXion agent in LangGraph by adding RefleXion nodes.

## Slide 16 — Code Assistant
Section divider for the Code Assistant example.

## Slide 17 — The Flow
The Code Assistant generates LangChain code, providing LangChain documentation as context.

## Slide 18 — Context using LangChain Docs
A screenshot showing how LangChain docs are loaded as context.

## Slide 19 — Code Generator: prompt and schema
A screenshot showing the prompt and the structured schema for code generation.

## Slide 20 — Code Generator: Model
A screenshot of the code generator model setup.

## Slide 21 — State
A screenshot defining the graph state.

## Slide 22 — Generate Node
A screenshot of the generate node.

## Slide 23 — Code Check Node: Execute Code
Two screenshots of the code-check node that actually executes the generated code and inspects results.

## Slide 24 — Reflect Node
Replace the reflection step with a reflection chain.

## Slide 25 — Conditional edge
A conditional edge decides whether to regenerate (after reflection) or finish.

## Slide 26 — Graph
The full Code Assistant graph.

## Slide 27 — Web Voyager Agent
Section divider for WebVoyager.

## Slide 28 — WebVoyager
WebVoyager browses and searches the web to find an answer, controlling mouse and keyboard via tools through the Playwright framework. Tools are represented as special nodes rather than as LLM tools.

## Slide 29 — Graph State
A screenshot of the WebVoyager graph state, using HTML accessibility attributes from the ARIA standard.

## Slide 30 — Tools: Click
A screenshot of the Click tool.

## Slide 31 — Tool: Type Text
A screenshot of the Type Text tool.

## Slide 32 — Tool: Scroll
A screenshot of the Scroll tool.

## Slide 33 — Additional Tools
Three screenshots of additional tools.

## Slide 34 — Annotate page
Encode the page screenshot as an image and annotate buttons and text areas with bounding boxes.

## Slide 35 — Annotate and Format
Prepare the bounding boxes as part of the LLM prompt.

## Slide 36 — Annotation results
A screenshot of the annotated page.

## Slide 37 — Parse LLM output into action
A screenshot of the parser that turns LLM output into a concrete action.

## Slide 38 — Page Processing: predict action
A runnable side effect updates the "prediction" key in the output state.

## Slide 39 — Update state with Scratchpad Memory
A screenshot updating the state with the scratchpad memory.

## Slide 40 — Build Graph
Two screenshots building a graph with one node per tool.

## Slide 41 — Conditional Edge
A screenshot of the conditional edge wiring.

## Slide 42 — Usage: Start with google
A screenshot of usage starting from Google.

## Slide 43 — Call and print actions
A screenshot calling the agent and printing the resulting actions.

## Slide 44 — Example
Two screenshots showing example WebVoyager runs.

---

## Deck-level takeaway
The deck assembles three increasingly ambitious agentic-flow patterns in LangGraph. Reflection adds a critique-and-revise loop on top of a generation node. RefleXion adds a Responder + Revisor pair backed by structured JSON output and citation-generating tool calls, useful for grounded web answers. The Code Assistant generates LangChain code with documentation as context and uses execute-then-reflect cycles. WebVoyager closes the deck with a vision-driven web browsing agent built on Playwright: it annotates screenshots with ARIA-derived bounding boxes, lets the LLM choose actions over those boxes (click, type, scroll), and orchestrates the loop in LangGraph with one node per tool plus scratchpad memory.
