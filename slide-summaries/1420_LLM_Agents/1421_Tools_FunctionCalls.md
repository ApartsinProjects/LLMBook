# 1421_Tools_FunctionCalls — Per-Slide Summary

**Source file:** `1421_Tools_FunctionCalls.pptx`
**Source folder:** `SlidesPool/1420_LLM_Agents/`
**Drive link:** https://drive.google.com/file/d/1NS0uqg6sQUUsMrrQkCQNH1UqUkS5KC4E/view
**Slide count (exact, via python-pptx):** 29
**Extraction:** Local parse + slide PNG render. Bullets carry the conceptual flow; code screenshots illustrate OpenAI and LangChain tool APIs.

---

## Slide 1 — Function Calling
Title slide for the deck on LLM function calling.

## Slide 2 — Agentic AI
Agentic AI is goal-directed decision making: translate a goal into multiple actionable steps, maintain and update memory, and interact with the environment through tools.

## Slide 3 — Tools/Function Calling
Section divider for tools and function calling.

## Slide 4 — Enable LLM to interact with the world
Section divider framing tools as the LLM's interface to the outside world.

## Slide 5 — Function Calling
Components: a host application (the user program), the LLM (text generator), and a function (cloud or local API). Host responsibilities are to describe the function and its interface to the LLM, receive function-call requests from the LLM, execute them, and format the results back into the LLM's prompt.

## Slide 6 — Function Calling Flow
A flow diagram showing the host-LLM-function loop.

## Slide 7 — OpenAI: Define Tools/Functions
Code screenshot showing the OpenAI JSON schema for declaring tools / functions.

## Slide 8 — OpenAI: Tool Usage
Code screenshot showing the OpenAI client receiving a tool-call request and the host executing and returning results.

## Slide 9 — LangChain: Search Tool
Code screenshot using a built-in LangChain search tool.

## Slide 10 — LangChain: Custom Tool
Two screenshots defining a custom LangChain tool by subclassing or by providing a function.

## Slide 11 — LangChain: @Tool Decorator
Three screenshots using the @tool decorator, which automatically creates a tool object from a Python function's signature and docstring.

## Slide 12 — LangChain: Rich Tool Directory
Six screenshots of LangChain's tool directory, including search, math, file, and database tools.

## Slide 13 — Fine-Tuning for Function Calling
Section divider for fine-tuning models to emit better tool calls, starting with OpenAI's fine-tuning API.

## Slide 14 — Fine-Tuning with labeled data
Diagram of the supervised pipeline that fine-tunes a model on (input, tool-call) labels.

## Slide 15 — OpenAI Finetuning API
Code screenshot of the OpenAI fine-tuning API for tool-call models.

## Slide 16 — Toolformer
Section divider for self-supervised fine-tuning for function calling.

## Slide 17 — Tool-former
Toolformer fine-tunes GPT-J (6.7B parameters) to use a custom toolset (question answering, Wikipedia search, calculator, calendar, machine translation). The model learns when to call and what to call, formatting calls as token sequences in its output. The procedure is mostly self-supervised, without annotation.

## Slide 18 — Train the model
Generate synthetic data that contains tool calls and results. Train the LLM to predict the tool-call tokens but mask the loss on the result span (the model doesn't predict the tool's outcome). During inference, recognize tool calls, execute them, and append the result back into the stream.

## Slide 19 — Generation of Training Data
Start from ordinary text-completion training data. Select insertion points (punctuation, noun phrases). Use the LLM to generate multiple possible tool calls (tool-call sampling). Execute the calls and insert results. Filter useful tool calls plus results by requiring that they reduce the completion loss on the rest of the sequence.

## Slide 20 — Sampling Tool Calls
Code screenshot showing the LLM generating tool-call suggestions from the complete text.

## Slide 21 — Filtering
Keep a tool call only if the completion loss with the call and the result is lower than the loss without the call or with only the call.

## Slide 22 — ToolkenGPT
Section divider for ToolkenGPT (tokenized tool calling).

## Slide 23 — Tools as Tokens
ToolkenGPT extends the vocabulary with special toolkens (one token per tool). The LLM is frozen; next-token prediction uses the frozen word projection plus a trainable tool-token projection matrix.

## Slide 24 — Inference
If a tool token is predicted with higher probability than any word token, the model switches to "tool mode": generation pauses, the LLM completes the call signature ("context <tool_name>("), arguments are generated via in-context-learning prompts, the tool runs, the result is injected, and the model returns to reasoning mode. Updating with a new tool requires only adding a new toolken to predict. Training trains the toolken predictor only, not the argument generation, which is handled by ICL.

## Slide 25 — Diagram
A diagram showing the ToolkenGPT architecture and inference loop.

## Slide 26 — Train model
Training requires paired data: input contains the tool invocation result, output contains the toolken. The model autoregressively continues with tool results.

## Slide 27 — LLM-based training data generation
Use an LLM to generate tool-use examples with few-shot prompts seeded by tool descriptions.

## Slide 28 — GORILLA CLI
Section divider for Gorilla CLI.

## Slide 29 — Gorilla CLI
Gorilla CLI is a fine-tuned LLM equipped with a large library of community-created API definitions (an API zoo). Commands such as `$Gorilla "order my pizza"` or `$Gorilla "list all my GCP instances"` are translated into appropriate API calls. The system uses retrieval-augmented tool usage, fetching relevant APIs from the database.

---

## Deck-level takeaway
The deck explains function calling as the bridge between an LLM and the outside world. It starts with the standard host-LLM-tool flow demonstrated through the OpenAI and LangChain APIs (including the @tool decorator and the LangChain tool directory), then moves on to model-side specialization: supervised fine-tuning (OpenAI's API), self-supervised Toolformer (which mines its own training data by filtering tool calls that lower completion loss), and ToolkenGPT (which extends the vocabulary with one toolken per tool, freezing the backbone and training only the toolken projection). The closing slide on Gorilla CLI shows how the same ideas scale to thousands of community APIs via retrieval-augmented tool selection.
