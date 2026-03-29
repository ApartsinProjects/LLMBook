"""
Add exercise callout blocks to all section files in Parts 6 and 7.
Replaces old-style exercises where they exist, adds new ones where they don't.
"""
import re
import os

# All exercises keyed by section number
EXERCISES = {
    "22.1": [
        ("Exercise 22.1.1: Agent vs. Chain vs. Router", "basic", "conceptual",
         "Explain the difference between a chain, a router, and a full agent. For each, describe a concrete use case where it would be the most appropriate choice.",
         "A <strong>chain</strong> follows a fixed sequence of steps (e.g., summarize then translate). A <strong>router</strong> selects one path from several based on input (e.g., classify intent then route to the right handler). A <strong>full agent</strong> decides which actions to take and in what order in a loop, continuing until the task is done (e.g., a research assistant that searches, reads, and synthesizes). Chains suit deterministic workflows; routers suit classification-driven dispatch; agents suit open-ended tasks with unknown step counts."),
        ("Exercise 22.1.2: Agentic Design Patterns", "intermediate", "conceptual",
         "Andrew Ng identified four agentic design patterns: Reflection, Tool Use, Planning, and Multi-Agent Collaboration. For each pattern, describe one real-world scenario where it provides clear value over a simpler approach.",
         "Reflection: a code-writing agent that reviews its own output for bugs before submitting. Tool Use: a customer support agent that queries a CRM database. Planning: a travel agent that decomposes a multi-city itinerary into bookable steps. Multi-Agent Collaboration: a content pipeline where one agent drafts, another fact-checks, and a third edits for style."),
        ("Exercise 22.1.3: Breaking a ReAct Loop", "intermediate", "coding",
         "A ReAct agent keeps searching for information and never produces a final answer. Write a Python function <code>run_react_loop()</code> that implements a maximum-step limit and a \"repeated action\" detector that stops the loop if the agent calls the same tool with the same arguments twice in a row.",
         "Maintain a list of (tool_name, arguments) tuples. After each action, compare with the previous entry. If they match, inject a prompt like 'You have repeated the same action. Synthesize what you know and provide a final answer.' Also enforce <code>max_steps</code> (e.g., 10) and return whatever partial answer the agent has produced when the limit is reached."),
        ("Exercise 22.1.4: Cognitive Architecture State Machine", "intermediate", "coding",
         "Implement a minimal three-state agent (PLANNING, EXECUTING, REFLECTING) using a Python dictionary to track state transitions. The agent should plan how to answer a user question, execute the plan step by step, and reflect on whether the result is satisfactory.",
         "Use a while loop with a <code>current_state</code> variable. In PLANNING, call the LLM to produce a numbered list of steps. In EXECUTING, iterate through steps and call tools. In REFLECTING, ask the LLM whether the collected results answer the original question. Transition back to PLANNING if reflection says 'no' (with a max-retry limit)."),
        ("Exercise 22.1.5: Memory Type Classification", "basic", "conceptual",
         "Classify each of the following as episodic, semantic, or procedural memory: (a) \"The user prefers Python over JavaScript.\" (b) \"Last Tuesday the deployment failed because of a missing environment variable.\" (c) \"To deploy to staging, first run migrations, then restart the service.\"",
         "(a) Semantic memory: a distilled fact about the user. (b) Episodic memory: a timestamped record of a specific event. (c) Procedural memory: a learned action sequence that can be replayed."),
    ],
    "22.2": [
        ("Exercise 22.2.1: Memory Tier Design", "intermediate", "conceptual",
         "Describe the three memory tiers in the MemGPT (Letta) architecture and explain the role of each. Why is a three-tier approach more effective than simply increasing the context window size?",
         "Main context holds the active prompt and recent turns. Recall storage holds the full conversation history, searchable by recency or content. Archival storage is a vector database for long-term facts. A larger context window still has finite capacity and suffers from the 'lost in the middle' problem. Three tiers let the agent page in only what is relevant, similar to how an OS manages RAM and disk."),
        ("Exercise 22.2.2: Episodic vs. Semantic Memory", "basic", "conceptual",
         "A support agent helped a user fix a database connection pool exhaustion last month. Explain what would be stored in episodic memory versus semantic memory for this interaction, and when each would be retrieved.",
         "Episodic: 'On March 3, user_123 reported 502 errors on /api/payments. Root cause was connection pool exhaustion. Fixed by increasing max_connections from 20 to 50.' Semantic: 'user_123 production stack uses PostgreSQL 15 with max_connections=50.' Episodic is retrieved when a similar error pattern appears. Semantic is retrieved whenever the agent needs to know the user's infrastructure."),
        ("Exercise 22.2.3: Context Window Budget Allocator", "intermediate", "coding",
         "Write a Python function <code>allocate_context(system_prompt, memories, history, max_tokens=8000)</code> that allocates token budget across system prompt, retrieved memories, conversation history, and a reserved block for the model response. Implement a strategy that trims history first, then memories, if the total exceeds the budget.",
         "Count tokens for each section (using tiktoken or a simple word-count approximation). Reserve 2000 tokens for the response. If the total of system_prompt + memories + history exceeds max_tokens minus the reserve, trim history from the oldest messages first. If still over budget, drop the lowest-relevance memories. Return the assembled prompt string."),
        ("Exercise 22.2.4: Memory Staleness", "intermediate", "analysis",
         "An agent's semantic memory says \"user's database is PostgreSQL 14\" but the user upgraded to PostgreSQL 16 three months ago. Propose a strategy that detects and corrects stale memories without requiring the user to explicitly update them.",
         "Attach a <code>last_verified</code> timestamp and a <code>confidence</code> score to each memory. When a memory older than N days is retrieved for a critical decision, the agent asks a confirmation question: 'I have on record that you use PostgreSQL 14. Is that still correct?' On contradiction detection (e.g., user mentions PG 16), automatically update the memory and log the change."),
        ("Exercise 22.2.5: Lost-in-the-Middle Mitigation", "basic", "conceptual",
         "Explain the 'lost in the middle' phenomenon and how it affects agent memory placement. Where in the context window should the most critical memories be placed, and why?",
         "LLMs attend less to information in the middle of a long context compared to the beginning and end. Place the most critical memories right after the system prompt (beginning) or just before the current query (end). Conversation history, which is less critical per-turn, can occupy the middle. This mirrors findings from Liu et al. (2023) on retrieval-augmented generation."),
    ],
    "22.3": [
        ("Exercise 22.3.1: Plan-and-Execute vs. ReAct", "intermediate", "conceptual",
         "Compare the plan-and-execute architecture with a standard ReAct loop. In which scenarios does plan-and-execute outperform ReAct, and when might ReAct be preferable?",
         "Plan-and-execute excels when the task has clear subtask decomposition and dependencies between steps (e.g., a multi-step data pipeline). ReAct is better for exploratory tasks where the next step depends on discoveries made in the current step (e.g., debugging). Plan-and-execute is more debuggable because the plan is explicit; ReAct is more adaptive because it re-evaluates after every action."),
        ("Exercise 22.3.2: Tree of Thoughts Implementation", "advanced", "coding",
         "Implement a simplified Tree of Thoughts explorer that generates three candidate next steps for a problem, scores each using the LLM, and expands the highest-scoring branch. Test it on the problem: 'Write a function to find the longest palindromic substring.'",
         "For each candidate step, prompt the LLM to rate it 1 to 10 on 'likelihood of leading to a correct and efficient solution.' Select the highest-rated branch, generate the next set of candidates, and repeat for a fixed depth (e.g., 3 levels). Compare the final solution to a single-pass chain-of-thought approach."),
        ("Exercise 22.3.3: Reflection Budget", "intermediate", "conceptual",
         "A Reflexion agent is allowed unlimited self-correction loops and spends 15 iterations refining an answer that was already correct after iteration 2. Propose a concrete stopping criterion that balances thoroughness with efficiency.",
         "Use a combination of: (1) a maximum iteration cap (e.g., 3), (2) a 'delta check' that stops if the reflection produces no substantive changes to the answer, and (3) a test-based gate that stops as soon as all validation tests pass. In practice, 2 to 3 reflection rounds capture most of the value; additional rounds show diminishing returns."),
        ("Exercise 22.3.4: LATS Cost Analysis", "advanced", "analysis",
         "A standard ReAct agent uses 5 LLM calls per task at $0.01 each. A LATS agent explores a tree of depth 3 with branching factor 3, requiring an LLM call per node. Calculate the cost ratio and discuss when LATS is economically justified.",
         "LATS nodes: 1 + 3 + 9 + 27 = 40 calls (or 3^0 + 3^1 + 3^2 + 3^3). Cost ratio: 40 * $0.01 / 5 * $0.01 = 8x more expensive. LATS is justified when the cost of a wrong answer far exceeds the extra compute cost, such as code migrations where a bug could cause production outages, or financial decisions where errors have monetary consequences."),
        ("Exercise 22.3.5: Replanning After Failure", "intermediate", "coding",
         "Extend the plan-and-execute code from this section to add a replanning step. When a step fails, the agent should generate a revised plan that accounts for the failure. Implement this as a LangGraph conditional edge.",
         "Add a <code>should_replan</code> function that checks if the latest result contains an error or unexpected output. If so, route to a <code>replan</code> node that receives the original task, completed steps, and the failure message, then generates a new plan starting from the current state. Add an edge from <code>replan</code> back to <code>execute</code>."),
    ],
    "22.4": [
        ("Exercise 22.4.1: Reasoning Model Trade-offs", "intermediate", "conceptual",
         "Explain why reasoning models are described as 'overkill for routine tool execution.' What specific characteristics of reasoning models make them better suited for planning than for simple API calls?",
         "Reasoning models allocate extra compute for internal chain-of-thought deliberation. For a simple API call (e.g., fetching a weather forecast), this extra compute adds latency and cost without improving accuracy. Planning tasks benefit because they require evaluating multiple strategies, considering dependencies, and anticipating failure modes, all of which leverage the model's extended reasoning capacity."),
        ("Exercise 22.4.2: Thinking Budget Configuration", "intermediate", "coding",
         "Using the Anthropic API with extended thinking, write code that sets a thinking budget of 5000 tokens for a planning task and 500 tokens for a simple lookup task. Print the actual tokens used in each case to demonstrate budget-aware reasoning.",
         "Use <code>anthropic.Anthropic().messages.create()</code> with <code>thinking={'type': 'enabled', 'budget_tokens': N}</code>. For the planning task, send a complex multi-step problem. For the lookup, send a simple factual question. Print <code>block.thinking</code> length for each response to show the model adapts its reasoning depth to the budget."),
        ("Exercise 22.4.3: Hybrid Architecture Design", "advanced", "conceptual",
         "Design a three-tier agent architecture that routes queries to different model tiers based on complexity. Define the routing criteria, the model used at each tier, and the expected cost and latency profile.",
         "Tier 1 (fast model, no reasoning): FAQ lookups, status checks. ~200ms, $0.001/query. Tier 2 (standard model): troubleshooting with known patterns. ~2s, $0.01/query. Tier 3 (reasoning model): novel multi-step problems. ~15s, $0.10/query. Route based on a lightweight classifier that scores query complexity on factors like number of entities, required reasoning steps, and domain specificity."),
        ("Exercise 22.4.4: Over-Prompting Reasoning Models", "basic", "conceptual",
         "Why does adding 'think step by step' to a reasoning model prompt sometimes degrade performance? How does this differ from prompting a standard model?",
         "Reasoning models already perform internal chain-of-thought deliberation. Adding explicit step-by-step instructions can conflict with the model's trained reasoning process, causing it to produce a surface-level enumeration rather than its deeper internal reasoning. Standard models lack this built-in reasoning and benefit from explicit step-by-step prompting because it structures their single-pass generation."),
        ("Exercise 22.4.5: Reasoning Model Comparison", "intermediate", "analysis",
         "Compare the three major reasoning model families (OpenAI o1/o3, Anthropic Claude with extended thinking, DeepSeek-R1) along these dimensions: visibility of reasoning, cost model, and suitability for agent backbones.",
         "OpenAI o1/o3: hidden reasoning (opaque), charged per reasoning token, good for tasks where you trust the model's process. Claude extended thinking: visible reasoning in a thinking block, budget-controllable, excellent for debugging agent behavior. DeepSeek-R1: open-source, reasoning visible, no API cost for self-hosted, best for teams that need full control. For agent backbones, visible reasoning (Claude, DeepSeek) is preferable because it enables monitoring and debugging."),
    ],
    "22.5": [
        ("Exercise 22.5.1: Agent Evaluation Dimensions", "basic", "conceptual",
         "List four dimensions on which agents should be evaluated beyond simple task completion. Explain why pass rate alone is an insufficient metric.",
         "Task completion (did it succeed?), efficiency (steps and tokens used), safety (did it avoid harmful actions?), and robustness (does it handle edge cases?). Pass rate alone ignores cost: an agent solving 80% at $0.05/task may be more valuable than one solving 90% at $2/task. It also ignores latency, safety violations, and failure modes."),
        ("Exercise 22.5.2: SWE-bench Task Analysis", "intermediate", "conceptual",
         "Explain the structure of a SWE-bench task: what inputs does the agent receive, what output must it produce, and how is success determined? Why is SWE-bench Verified considered more reliable than the original SWE-bench?",
         "Inputs: a repository snapshot and a natural language issue description. Output: a code patch. Success: the patch passes the provided test suite. SWE-bench Verified uses human-validated tasks, removing noisy or ambiguous tasks from the original set that could give misleading results about agent capabilities."),
        ("Exercise 22.5.3: Custom Evaluation Design", "advanced", "coding",
         "Design a custom evaluation harness for a customer support agent. Write a Python class <code>SupportAgentEval</code> that takes a list of test cases (question, expected_resolution, difficulty) and produces a report with accuracy, average cost, and failure categorization.",
         "The class should: (1) iterate through test cases, (2) run the agent on each, (3) compare output to expected_resolution using exact match or LLM-as-judge, (4) record token usage and latency per case, (5) categorize failures (misunderstanding, wrong tool, incomplete answer), and (6) produce a summary DataFrame with per-category pass rates and cost statistics."),
        ("Exercise 22.5.4: Pareto Frontier Plotting", "intermediate", "coding",
         "Given a set of agent evaluation results (accuracy, cost_per_task), write a Python function that identifies the Pareto-optimal configurations and plots the accuracy vs. cost frontier using matplotlib.",
         "Sort results by cost. A point is Pareto-optimal if no other point has both higher accuracy and lower cost. Iterate through sorted results, tracking the maximum accuracy seen. A point is on the frontier if its accuracy exceeds the current maximum. Plot all points as scatter, highlight Pareto-optimal points, and connect them with a line."),
        ("Exercise 22.5.5: Benchmark Limitations", "intermediate", "discussion",
         "WebArena and OSWorld test agents in simulated environments. Discuss two ways these benchmarks might overestimate or underestimate agent capabilities compared to real-world deployment.",
         "Overestimate: benchmarks use clean, deterministic environments; real websites have CAPTCHAs, dynamic content, and rate limits. Underestimate: benchmarks evaluate single sessions; real agents can learn from past attempts and use persistent memory. Also, benchmark scoring may miss partial successes that would still be useful to a human user."),
    ],
    "23.1": [
        ("Exercise 23.1.1: Function Schema Design", "basic", "conceptual",
         "Write a JSON schema for a <code>search_products</code> function that takes a query string, an optional category filter, and a maximum number of results (default 10). Follow the OpenAI function calling format.",
         'Use <code>{"name": "search_products", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "category": {"type": "string"}, "max_results": {"type": "integer", "default": 10}}, "required": ["query"]}}</code>. The description field should clearly explain what the function does so the model can decide when to call it.'),
        ("Exercise 23.1.2: Multi-Provider Function Calling", "intermediate", "coding",
         "Implement the same tool (a weather lookup) using both the OpenAI and Anthropic function calling APIs. Compare the request/response formats and identify the key differences.",
         "OpenAI uses <code>tools</code> with <code>function</code> type in the request and returns <code>tool_calls</code> in the response. Anthropic uses <code>tools</code> with <code>input_schema</code> and returns <code>tool_use</code> content blocks. Key differences: Anthropic returns tool calls as content blocks within the message; OpenAI uses a separate <code>tool_calls</code> field. Both require sending tool results back in subsequent messages."),
        ("Exercise 23.1.3: Parallel Tool Calls", "intermediate", "coding",
         "Write code that handles parallel tool calls from an LLM response. The model returns three tool calls simultaneously; your code should execute all three concurrently using <code>asyncio.gather()</code> and return the results.",
         "Parse all tool calls from the response. Create async wrapper functions for each tool execution. Use <code>results = await asyncio.gather(*[execute_tool(tc) for tc in tool_calls])</code>. Map results back to their tool call IDs and send them all in the next message as separate tool result entries."),
        ("Exercise 23.1.4: Open-Source Function Calling", "intermediate", "conceptual",
         "Compare function calling capabilities between proprietary models (GPT-4, Claude) and open-source models (Llama, Mistral). What are the main challenges when using open-source models for tool use?",
         "Open-source models may not natively support structured tool call output, requiring custom prompt formatting and output parsing. They may hallucinate tool names or produce malformed JSON arguments. Fine-tuned variants (e.g., Gorilla, NexusRaven) improve reliability but may lag behind proprietary models in handling complex multi-tool scenarios. Testing and validation are more important with open-source models."),
        ("Exercise 23.1.5: Tool Call Error Handling", "basic", "conceptual",
         "An agent calls a tool and receives an error response. Describe two strategies for handling this: one where the agent retries, and one where it adapts its approach. When is each strategy appropriate?",
         "Retry: appropriate for transient errors (network timeouts, rate limits). The agent waits and retries with the same arguments. Adapt: appropriate for semantic errors (invalid arguments, resource not found). The agent interprets the error message, adjusts its approach (e.g., tries a different search query), and calls a different tool or the same tool with modified arguments."),
    ],
    "23.2": [
        ("Exercise 23.2.1: MCP Architecture", "basic", "conceptual",
         "Explain the client-server architecture of MCP (Model Context Protocol). What are the three core primitives that an MCP server exposes, and how do they differ?",
         "An MCP server exposes capabilities to MCP clients (which run inside LLM applications). The three primitives are: <strong>Tools</strong> (callable functions the model can invoke), <strong>Resources</strong> (data the model can read, like files or database records), and <strong>Prompts</strong> (reusable prompt templates). Tools are actions; resources are data; prompts are templates."),
        ("Exercise 23.2.2: Build a Simple MCP Server", "intermediate", "coding",
         "Write a minimal MCP server in Python using the <code>mcp</code> library that exposes a single tool called <code>word_count</code>. The tool takes a text string and returns the number of words.",
         "Use <code>from mcp.server import Server</code> and <code>@server.tool()</code> decorator. The function takes a <code>text: str</code> parameter and returns <code>len(text.split())</code>. Run with <code>mcp.server.stdio.run(server)</code>. Test by connecting a client and calling the tool."),
        ("Exercise 23.2.3: MCP vs. Direct Function Calling", "intermediate", "conceptual",
         "Compare MCP with direct function calling (as in OpenAI/Anthropic APIs). What problem does MCP solve that direct function calling does not? When would you choose one over the other?",
         "Direct function calling is provider-specific and tightly coupled to your application code. MCP provides a standardized, provider-agnostic protocol that lets any MCP client connect to any MCP server. Choose MCP when you want tool reusability across applications, team-shared tool registries, or when third parties provide tool integrations. Choose direct function calling for simple, single-application setups."),
        ("Exercise 23.2.4: MCP Security Considerations", "advanced", "conceptual",
         "An MCP server exposes a tool that executes SQL queries against a production database. Identify three security risks and propose mitigations for each.",
         "(1) SQL injection via model-generated queries: use parameterized queries and a query allowlist. (2) Data exfiltration through overly broad queries: enforce row limits and column restrictions. (3) Unauthorized access: require authentication tokens and implement per-user permission scoping. Also consider read-only database connections for query tools."),
        ("Exercise 23.2.5: MCP Ecosystem Discovery", "basic", "conceptual",
         "Explain how MCP enables tool discovery and composition. How does an LLM application learn what tools are available on a connected MCP server?",
         "When an MCP client connects to a server, it calls the <code>list_tools</code> method to discover available tools, their schemas, and descriptions. The client then includes these tool definitions in the LLM's prompt. This enables dynamic tool discovery: the application does not need to hardcode tool definitions. Multiple MCP servers can be connected simultaneously, and the client aggregates all available tools."),
    ],
    "23.3": [
        ("Exercise 23.3.1: A2A Protocol Basics", "intermediate", "conceptual",
         "Describe the key components of Google's Agent-to-Agent (A2A) protocol. How does an A2A Agent Card enable discovery, and what information does it contain?",
         "An Agent Card is a JSON document (served at <code>/.well-known/agent.json</code>) that describes the agent's capabilities, supported input/output types, and endpoint URL. It enables discovery by allowing other agents to fetch the card, understand what the agent can do, and decide whether to delegate tasks to it. It contains fields like name, description, skills, and authentication requirements."),
        ("Exercise 23.3.2: Task Lifecycle States", "intermediate", "conceptual",
         "Draw (or describe) the state transitions in an A2A task lifecycle. What states can a task be in, and what events trigger transitions between them?",
         "States: submitted, working, input-required, completed, failed, canceled. Transitions: submitted to working (agent starts processing), working to input-required (agent needs more info from the caller), input-required to working (caller provides additional input), working to completed (task done), working to failed (unrecoverable error), any state to canceled (caller cancels)."),
        ("Exercise 23.3.3: A2A vs. MCP", "basic", "conceptual",
         "Compare A2A and MCP. What problem does each protocol solve? Can they be used together, and if so, how?",
         "MCP connects LLM applications to tools and data sources (model-to-tool). A2A connects agents to other agents (agent-to-agent). They are complementary: an agent might use MCP to access tools locally and A2A to delegate subtasks to specialized remote agents. An A2A agent could internally use MCP servers for its tool access."),
        ("Exercise 23.3.4: Federation Design", "advanced", "coding",
         "Design a simple agent registry service in Python that stores Agent Cards and supports discovery queries. Implement <code>register(card)</code>, <code>search(skill_query)</code>, and <code>get(agent_id)</code> methods.",
         "Use a dictionary keyed by agent_id. For <code>search</code>, iterate over stored cards and match the skill_query against each card's skills list using substring matching or embedding similarity. Return a ranked list of matching agents. In production, this would use a database with full-text search or vector similarity."),
        ("Exercise 23.3.5: A2A Error Handling", "intermediate", "conceptual",
         "A task delegated via A2A fails because the remote agent encounters an error. Describe how the calling agent should handle this failure, considering the task lifecycle states.",
         "The remote agent transitions the task to 'failed' state with an error message. The calling agent receives this status update and should: (1) log the failure with the remote agent's error details, (2) decide whether to retry with the same agent, (3) search for an alternative agent with the same skill, or (4) escalate to a human. The A2A protocol's task history preserves the full interaction for debugging."),
    ],
    "23.4": [
        ("Exercise 23.4.1: Tool Naming Conventions", "basic", "conceptual",
         "Why is it important that tool names be descriptive and follow consistent naming conventions? Give an example of a poorly named tool and its improved version, explaining why the improvement helps the LLM.",
         "LLMs use tool names and descriptions to decide which tool to call. A tool named <code>fn1</code> gives the model no information. Renamed to <code>search_customer_orders</code> with a clear description, the model can match user intents to tools reliably. Consistent naming (verb_noun pattern) also helps the model distinguish between similar tools like <code>search_orders</code> vs. <code>create_order</code>."),
        ("Exercise 23.4.2: Input Validation Layer", "intermediate", "coding",
         "Write a Python decorator <code>@validate_tool_input</code> that validates tool arguments against a JSON schema before execution. If validation fails, return a structured error message that helps the LLM correct its call.",
         "Use the <code>jsonschema</code> library. The decorator receives the schema as a parameter, validates the incoming arguments, and on failure returns a message like: 'Validation error: field \"email\" must be a valid email address. You provided: \"not-an-email\". Please retry with a valid email.' This feedback loop helps the LLM self-correct."),
        ("Exercise 23.4.3: Graceful Error Messages", "intermediate", "conceptual",
         "Compare two approaches to returning tool errors to an LLM: (a) returning raw stack traces and (b) returning structured error messages with suggested fixes. Which approach leads to better agent behavior, and why?",
         "Structured error messages are far better. Raw stack traces contain implementation details (file paths, line numbers) that are meaningless to the LLM and waste tokens. A structured message like 'Error: user_id 12345 not found. Suggestion: verify the user_id with the search_users tool before retrying' gives the model actionable information to recover. This reduces retry loops and improves task completion rates."),
        ("Exercise 23.4.4: SQL Injection Prevention", "intermediate", "coding",
         "An agent has a <code>query_database</code> tool. Write a safe implementation that uses parameterized queries and prevents the LLM from executing arbitrary SQL. Include an allowlist of permitted query patterns.",
         "Define allowed query templates (e.g., 'SELECT {columns} FROM orders WHERE customer_id = ?'). The tool parses the LLM's intent, matches it to a template, extracts parameters, and executes the parameterized query. Reject any input that does not match an allowed template. Never pass raw LLM output directly to a SQL engine."),
        ("Exercise 23.4.5: Rate Limiting Tools", "basic", "conceptual",
         "Why should agent tools implement rate limiting? Describe a scenario where an agent without rate-limited tools could cause problems, and propose a solution.",
         "An agent in a loop might call an external API hundreds of times if it misinterprets the task or gets stuck. Without rate limiting, this could exhaust API quotas, incur large costs, or trigger IP blocks. Solution: implement per-tool rate limits (e.g., max 10 calls per minute) with a token bucket algorithm. When the limit is reached, return a message telling the agent to wait or use cached results."),
    ],
    "23.5": [
        ("Exercise 23.5.1: Static vs. Agentic RAG", "basic", "conceptual",
         "Compare static RAG (retrieve once, generate once) with agentic RAG (retrieve, evaluate, re-retrieve if needed). In what types of queries does agentic RAG provide the most improvement?",
         "Static RAG retrieves documents once and generates an answer. If the retrieved documents are irrelevant or insufficient, the answer suffers. Agentic RAG evaluates retrieval quality and re-retrieves with refined queries if needed. It provides the most improvement for complex, multi-faceted queries where a single retrieval pass is unlikely to capture all relevant information (e.g., 'Compare the approaches of papers A and B to problem X')."),
        ("Exercise 23.5.2: Multi-Source Retrieval Agent", "intermediate", "coding",
         "Write a Python function for an agentic RAG system that queries three different sources (a vector database, a web search API, and a SQL database), merges the results, and ranks them by relevance to the original query.",
         "Create three async tool functions, one per source. Use <code>asyncio.gather()</code> to query all three in parallel. Merge results into a single list with source metadata. Rank by relevance using an embedding similarity score between each result and the original query. Return the top-k results with source attribution."),
        ("Exercise 23.5.3: Retrieval Quality Evaluation", "intermediate", "conceptual",
         "An agentic RAG system retrieves documents but the agent decides they are insufficient. Describe the criteria the agent should use to evaluate retrieval quality and decide whether to re-retrieve.",
         "The agent should check: (1) relevance (do the documents address the query?), (2) completeness (do they cover all aspects of a multi-part question?), (3) recency (is the information up to date for time-sensitive queries?), and (4) source diversity (are there multiple corroborating sources?). A simple approach: ask the LLM to rate the retrieved documents on these criteria and re-retrieve if any score is below a threshold."),
        ("Exercise 23.5.4: Knowledge Graph Integration", "advanced", "coding",
         "Design a retrieval agent that combines vector similarity search with knowledge graph traversal. The agent first retrieves candidate entities, then traverses the graph to find related entities, and finally synthesizes the information.",
         "Step 1: embed the query, retrieve top-k entities from the vector store. Step 2: for each entity, query the knowledge graph for neighbors within 2 hops. Step 3: score the graph-retrieved entities by path relevance. Step 4: combine vector and graph results, deduplicate, and pass to the LLM for synthesis. This hybrid approach captures both semantic similarity and structural relationships."),
        ("Exercise 23.5.5: Agentic RAG Loop Control", "intermediate", "conceptual",
         "An agentic RAG system keeps re-retrieving documents because the LLM is never satisfied with the results. Propose three safeguards to prevent infinite retrieval loops.",
         "(1) Maximum retrieval rounds (e.g., 3 attempts). (2) Diminishing returns detection: if re-retrieval returns substantially the same documents, stop and work with what is available. (3) Query diversity enforcement: require each re-retrieval to use a meaningfully different query, not a minor rephrasing. After the maximum rounds, the agent should generate the best answer it can with available information and flag low confidence."),
    ],
    "24.1": [
        ("Exercise 24.1.1: Framework Comparison", "basic", "conceptual",
         "Compare LangGraph, CrewAI, and AutoGen on three dimensions: ease of setup, flexibility of agent topologies, and production readiness. Which framework would you choose for a quick prototype vs. a production system?",
         "LangGraph: most flexible (arbitrary graph topologies), production-ready, steeper learning curve. CrewAI: easiest setup (role-based agents), good for team simulations, less flexible topology. AutoGen: strong multi-agent conversations, good for research, evolving production story. Quick prototype: CrewAI for its simplicity. Production: LangGraph for its explicit state management and observability hooks."),
        ("Exercise 24.1.2: Framework Selection Criteria", "intermediate", "conceptual",
         "A startup needs to build a customer support agent that escalates complex issues to specialists. List five criteria they should use to select an agent framework, and rank them by importance.",
         "1. Production reliability (error handling, retries, observability). 2. Human-in-the-loop support (escalation, approval workflows). 3. State management (conversation history, customer context). 4. Integration ecosystem (CRM, ticketing, knowledge base connectors). 5. Team expertise (learning curve, documentation quality). Reliability and HITL support are most critical for customer-facing applications."),
        ("Exercise 24.1.3: LangGraph State Machine", "intermediate", "coding",
         "Build a simple two-agent LangGraph workflow where a 'researcher' agent gathers information and a 'writer' agent produces a summary. Use typed state to pass information between agents.",
         "Define a <code>TypedDict</code> state with fields for query, research_results, and final_summary. Create two nodes (researcher, writer). The researcher populates research_results; the writer reads them and produces final_summary. Connect with <code>graph.add_edge('researcher', 'writer')</code>. Compile and invoke with the initial query."),
        ("Exercise 24.1.4: CrewAI Role Design", "intermediate", "coding",
         "Using CrewAI, define a crew of three agents (Researcher, Analyst, Reporter) that work together to produce a market analysis report. Specify each agent's role, goal, and backstory.",
         "Each agent gets a role string, a goal describing its objective, and a backstory providing context. The Researcher searches for data, the Analyst identifies trends and insights, and the Reporter writes the final document. Tasks are defined with expected outputs and assigned to specific agents. The crew is configured with a sequential process."),
        ("Exercise 24.1.5: Framework Lock-in Risks", "basic", "discussion",
         "What are the risks of building a production agent system on a specific framework? How can you architect your system to minimize framework lock-in?",
         "Risks: framework may become unmaintained, its API may change breaking your code, or it may not scale to your needs. Mitigation: separate business logic from framework-specific code using an adapter pattern. Define your own tool interface and agent interface; implement framework-specific adapters. Store state in your own database rather than relying on framework state management. This lets you swap frameworks without rewriting core logic."),
    ],
    "24.2": [
        ("Exercise 24.2.1: Pattern Identification", "basic", "conceptual",
         "Match each scenario to the best multi-agent architecture pattern (supervisor, pipeline, debate, or swarm): (a) content moderation with multiple criteria, (b) sequential document processing, (c) open-ended research, (d) fact-checking claims.",
         "(a) Supervisor: a central agent coordinates specialized checkers for different criteria. (b) Pipeline: each agent handles one stage (extract, validate, format). (c) Swarm: agents dynamically self-organize to explore different research directions. (d) Debate: two agents argue for and against a claim, producing a balanced assessment."),
        ("Exercise 24.2.2: Supervisor Pattern Implementation", "intermediate", "coding",
         "Implement a supervisor agent that receives a task, decides which of three specialist agents (coder, researcher, writer) to delegate to, collects the result, and decides whether the task is complete or needs further delegation.",
         "The supervisor is a function that calls the LLM with the task and available agents. The LLM returns a JSON decision: {agent: 'coder', subtask: '...'}. Execute the chosen agent, return the result to the supervisor, and loop until the supervisor decides the task is complete. Use a max_delegation_rounds limit."),
        ("Exercise 24.2.3: Pipeline vs. Supervisor", "intermediate", "conceptual",
         "A document processing system needs to extract entities, classify them, and generate a summary. Compare implementing this as a pipeline pattern versus a supervisor pattern. What are the trade-offs?",
         "Pipeline: deterministic, predictable latency, easy to debug and monitor. Each stage runs once in sequence. Supervisor: can dynamically re-route (e.g., skip classification if no entities found), but adds overhead of routing decisions and is harder to predict latency. Choose pipeline when the steps are always the same; choose supervisor when some steps may be skipped or repeated based on intermediate results."),
        ("Exercise 24.2.4: Debate Pattern Design", "advanced", "coding",
         "Implement a debate pattern where two agents argue for and against a proposition, moderated by a judge agent that scores arguments and declares a winner after three rounds.",
         "Create three functions: proposer (argues for), opposer (argues against), and judge (scores each round). In each round, the proposer and opposer receive the conversation history and produce arguments. The judge scores each argument on strength of evidence, logical coherence, and relevance. After three rounds, the judge produces a final verdict with reasoning."),
        ("Exercise 24.2.5: Topology Selection Criteria", "intermediate", "conceptual",
         "List four criteria for selecting a multi-agent topology and explain how each criterion favors a different pattern.",
         "1. Task decomposability (clear subtasks favor pipeline or map-reduce). 2. Interdependency between steps (high interdependency favors supervisor or swarm). 3. Need for diverse perspectives (favors debate or ensemble). 4. Latency requirements (pipeline is predictable; supervisor adds routing overhead; parallel patterns reduce wall-clock time). 5. Observability needs (pipeline is easiest to trace)."),
    ],
    "24.3": [
        ("Exercise 24.3.1: Communication Pattern Selection", "basic", "conceptual",
         "Describe three communication patterns for multi-agent systems (direct messaging, shared blackboard, broadcast) and give a scenario where each is most appropriate.",
         "Direct messaging: one agent sends a request to a specific agent (e.g., supervisor to specialist). Shared blackboard: all agents read from and write to a shared state (e.g., collaborative document editing). Broadcast: one agent sends a message to all agents (e.g., announcing a deadline change). Direct is most efficient for known routing; blackboard for collaborative tasks; broadcast for system-wide updates."),
        ("Exercise 24.3.2: Majority Voting Implementation", "intermediate", "coding",
         "Implement a majority voting mechanism where three LLM agents independently answer a question, and a function determines the consensus answer. Handle the case where all three answers differ.",
         "Run three independent LLM calls with different temperatures or prompts. Compare answers using string similarity or semantic embedding distance. If two or more match (within a threshold), return the majority answer. If all three differ, either return the answer with highest confidence score, run additional agents to break the tie, or flag the disagreement for human review."),
        ("Exercise 24.3.3: Conflict Resolution Strategies", "intermediate", "conceptual",
         "Two agents in a multi-agent system produce contradictory analyses of the same data. Describe three conflict resolution strategies and the trade-offs of each.",
         "(1) Hierarchical: a designated authority agent decides. Fast but creates a single point of failure. (2) Evidence-based: each agent provides supporting evidence; the resolution favors the better-supported claim. More robust but slower. (3) Synthesis: a mediator agent finds common ground and produces a combined analysis. Most thorough but most expensive in terms of LLM calls."),
        ("Exercise 24.3.4: Shared State Design", "advanced", "coding",
         "Design a shared state object for a multi-agent document review system. The state must track the document, each agent's annotations, conflict markers, and the current review phase. Implement it as a Python TypedDict.",
         "Define <code>ReviewState(TypedDict)</code> with fields: <code>document: str</code>, <code>annotations: Dict[str, List[Annotation]]</code> (keyed by agent_id), <code>conflicts: List[Conflict]</code> (pairs of contradictory annotations), <code>phase: Literal['draft', 'review', 'resolution', 'final']</code>, and <code>resolved_document: Optional[str]</code>. Each agent reads the full state and writes only its own annotations."),
        ("Exercise 24.3.5: Consensus Failure Modes", "intermediate", "conceptual",
         "Describe three ways consensus mechanisms can fail in multi-agent systems and propose a mitigation for each.",
         "(1) Groupthink: agents converge on the same wrong answer because they share similar biases. Mitigation: use diverse model providers or temperatures. (2) Deadlock: agents never reach agreement. Mitigation: set a maximum rounds limit and fall back to a designated tiebreaker. (3) Manipulation: one agent's output disproportionately influences others. Mitigation: use independent parallel generation before sharing, so each agent commits to an answer before seeing others."),
    ],
    "24.4": [
        ("Exercise 24.4.1: State Machine Fundamentals", "basic", "conceptual",
         "Explain how a state machine differs from a simple sequential pipeline for agent workflows. What capabilities does a state machine provide that a pipeline does not?",
         "A pipeline is a fixed sequence: A then B then C. A state machine supports conditional transitions: from state B, go to C if successful or back to A if failed. State machines enable loops, branching, error recovery, and dynamic routing based on intermediate results. They can also pause and resume (durability), which pipelines cannot do natively."),
        ("Exercise 24.4.2: LangGraph State Machine", "intermediate", "coding",
         "Build a LangGraph state machine with four states (intake, research, draft, review) and conditional edges. From the review state, the workflow should loop back to draft if quality is below threshold, or proceed to a final output state.",
         "Define a <code>WorkflowState</code> TypedDict. Create node functions for each state. Add a <code>quality_check</code> function that returns 'revise' or 'approve'. Use <code>graph.add_conditional_edges('review', quality_check, {'revise': 'draft', 'approve': END})</code>. Add a revision counter to prevent infinite loops."),
        ("Exercise 24.4.3: Durable Execution Benefits", "intermediate", "conceptual",
         "Explain why durable execution (as provided by Temporal or Inngest) is important for production agent workflows. What happens to a standard agent workflow if the server crashes mid-execution?",
         "Without durable execution, a server crash loses all in-progress state. The workflow must restart from scratch, potentially repeating expensive LLM calls and tool executions. Durable execution persists each step's result, so after a crash the workflow resumes from the last completed step. This is critical for long-running agent tasks that span minutes or hours and involve costly API calls."),
        ("Exercise 24.4.4: Fan-Out/Fan-In Pattern", "advanced", "coding",
         "Implement a fan-out/fan-in pattern where a coordinator agent splits a research task into three parallel subtasks, runs them concurrently, and merges the results. Use Python's <code>asyncio.gather()</code>.",
         "The coordinator generates three subtask descriptions. Use <code>asyncio.gather(run_agent(t1), run_agent(t2), run_agent(t3))</code> to execute in parallel. Collect results, pass them to a synthesis agent that merges the findings into a coherent report. Handle partial failures by proceeding with available results and noting which subtasks failed."),
        ("Exercise 24.4.5: Workflow Checkpoint Design", "intermediate", "conceptual",
         "Design a checkpointing strategy for a multi-step agent workflow. What state should be saved at each checkpoint, and how should the system handle recovery from different failure points?",
         "Save at each checkpoint: the current state (all accumulated data), the completed steps list, the pending steps, and any tool call results. On recovery, load the latest checkpoint and resume from the next pending step. For idempotent tools, simply re-execute. For non-idempotent tools (e.g., sending emails), check a sent-messages log before re-executing to avoid duplicates."),
    ],
    "24.5": [
        ("Exercise 24.5.1: HITL Justification", "basic", "conceptual",
         "List three scenarios where human-in-the-loop is essential for an agent system and three where it would be unnecessary overhead. What criteria distinguish the two categories?",
         "Essential: financial transactions above a threshold, medical recommendations, irreversible actions (deleting data). Unnecessary: FAQ lookups, formatting text, fetching public information. The key criteria are: reversibility (can the action be undone?), consequence severity (what is the cost of an error?), and confidence level (how certain is the agent?)."),
        ("Exercise 24.5.2: Approval Workflow", "intermediate", "coding",
         "Implement a simple approval workflow where an agent pauses before executing high-risk actions and requests human approval via a callback function. The agent should continue automatically for low-risk actions.",
         "Classify each tool call as high-risk or low-risk using a predefined mapping. For high-risk calls, serialize the pending action to a queue and wait for a human response (approve/reject). If approved, execute and continue. If rejected, ask the agent to find an alternative approach. For low-risk calls, execute immediately without pausing."),
        ("Exercise 24.5.3: Trust Calibration", "intermediate", "conceptual",
         "Describe a progressive trust system where an agent starts with low autonomy and earns more autonomy over time as it demonstrates competence. What metrics would you track to adjust the trust level?",
         "Track: task completion rate, error rate, human override frequency, and severity of errors when they occur. Start with approval required for all actions. After N successful tasks with zero overrides, promote to approval-required-only-for-high-risk. After M more successes, promote to post-hoc review only. Any serious error triggers a trust level decrease. This mirrors how organizations onboard new employees."),
        ("Exercise 24.5.4: Escalation Design", "intermediate", "coding",
         "Write a Python function <code>should_escalate(agent_state, confidence, action_type)</code> that decides whether to escalate to a human based on the agent's confidence score, the action type, and the number of retries attempted.",
         "Escalate if: confidence < 0.7, or action_type is in HIGH_RISK_ACTIONS, or retry_count > 2, or the accumulated cost exceeds a budget threshold. Return a tuple of (should_escalate: bool, reason: str) so the escalation message includes context for the human reviewer."),
        ("Exercise 24.5.5: Human Feedback Integration", "advanced", "discussion",
         "How should an agent incorporate human feedback from approval workflows into its future behavior? Discuss the tension between learning from corrections and maintaining consistency.",
         "Options: (1) Store corrections as episodic memories for retrieval in similar situations. (2) Update the system prompt with learned rules. (3) Fine-tune on correction examples periodically. The tension: too much adaptation risks inconsistency (different behavior for similar cases), while too little adaptation wastes the feedback. A balanced approach stores corrections as retrievable examples and periodically reviews them for patterns that warrant system prompt updates."),
    ],
    "25.1": [
        ("Exercise 25.1.1: Code Agent Architecture", "intermediate", "conceptual",
         "Describe the typical architecture of a production code generation agent. What tools does it need, and how does the agent loop differ from a general-purpose agent?",
         "A code agent needs: file read/write tools, code execution (sandbox), test runner, search/grep tools, and possibly version control tools. The loop differs because it includes a tight feedback cycle: write code, run tests, observe failures, fix code. The agent must maintain a mental model of the codebase structure and track which files have been modified."),
        ("Exercise 25.1.2: Self-Debugging Agent", "intermediate", "coding",
         "Write a Python function that implements a self-debugging loop: generate code, run it, capture any error, and feed the error back to the LLM for correction. Limit to 3 retry attempts.",
         "In a loop: (1) call the LLM to generate code, (2) execute in a sandbox, (3) if execution succeeds, return the result, (4) if it fails, append the error traceback to the conversation and retry. Track attempt count and break after 3. Include the original requirements and all previous attempts in each retry prompt so the model does not repeat the same mistake."),
        ("Exercise 25.1.3: SWE-bench Performance Factors", "intermediate", "conceptual",
         "What factors determine whether a code agent succeeds on a SWE-bench task? Rank the following by importance: model quality, tool design, codebase navigation strategy, and context window size.",
         "1. Codebase navigation strategy (finding the right files is the prerequisite for everything else). 2. Model quality (reasoning about the fix). 3. Tool design (efficient file reading, search, and editing). 4. Context window size (important but manageable with good navigation). Many failures are navigation failures, not reasoning failures. An agent that cannot find the relevant code cannot fix the bug."),
        ("Exercise 25.1.4: Repository Navigation", "advanced", "coding",
         "Implement a 'search before read' repository navigation strategy. The agent should first search for relevant files using grep/ripgrep, then read only the most relevant files, rather than reading entire directories.",
         "Step 1: search for keywords from the issue description using a search tool. Step 2: rank matching files by relevance (number of matches, file path heuristics). Step 3: read the top 3 to 5 files. Step 4: if the relevant code is not found, broaden the search with related terms. This approach is far more token-efficient than reading files sequentially."),
        ("Exercise 25.1.5: Vibe-Coding Risks", "basic", "discussion",
         "What are the risks of 'vibe-coding' (generating code from high-level descriptions without reviewing the output)? How should developers balance productivity gains with code quality?",
         "Risks: subtle bugs the model introduces but the developer does not catch, security vulnerabilities in generated code, accumulation of technical debt from code the developer does not fully understand, and over-reliance on the model for understanding the codebase. Balance: use AI for drafting and boilerplate, but always review generated code, run tests, and understand what the code does before merging."),
    ],
    "25.2": [
        ("Exercise 25.2.1: Browser Agent Architecture", "intermediate", "conceptual",
         "Describe the key components of a browser agent. What observations does it receive, what actions can it take, and how does it maintain state across page navigations?",
         "Observations: page HTML (or a simplified DOM), screenshots, accessibility tree, current URL. Actions: click, type, scroll, navigate, wait, extract text. State is maintained through a combination of the conversation history (recording past actions and observations) and browser state (cookies, session storage). The agent must handle dynamic content loading and page transitions."),
        ("Exercise 25.2.2: Playwright MCP Integration", "intermediate", "coding",
         "Write a simple browser automation script using Playwright that navigates to a search engine, enters a query, and extracts the top 3 result titles. Structure it as a tool that an agent could call.",
         "Use <code>playwright.chromium.launch()</code>, navigate to the search page, fill the search input, press Enter, wait for results, and extract titles using CSS selectors. Wrap in an async function with clear input (query string) and output (list of title strings) that matches a tool schema. Handle timeouts and missing elements gracefully."),
        ("Exercise 25.2.3: WebArena Challenges", "advanced", "conceptual",
         "What makes WebArena tasks difficult for current browser agents? Identify three categories of challenges and explain why each is hard.",
         "(1) Dynamic content: modern web pages use JavaScript rendering, making the DOM differ from the source HTML. Agents must wait for content to load. (2) Multi-step navigation: reaching the right page may require multiple clicks through menus and filters. (3) Form interaction: filling forms correctly requires understanding field types, validation requirements, and dependent fields (e.g., state dropdown changes based on country selection)."),
        ("Exercise 25.2.4: DOM Simplification", "intermediate", "coding",
         "Write a Python function that takes raw HTML and produces a simplified representation suitable for an LLM agent. Remove scripts, styles, and non-interactive elements, keeping only text, links, buttons, and form fields.",
         "Use BeautifulSoup to parse HTML. Remove all <code>&lt;script&gt;</code>, <code>&lt;style&gt;</code>, <code>&lt;svg&gt;</code>, and hidden elements. For remaining elements, extract: text content, links (href + text), buttons (text + id), and form fields (type + name + label). Output a numbered list of interactive elements so the agent can reference them by number (e.g., '[3] Button: Submit Order')."),
        ("Exercise 25.2.5: Browser Agent Safety", "basic", "conceptual",
         "List three safety considerations for deploying browser agents and propose a mitigation for each.",
         "(1) Unintended purchases or form submissions: require human approval for any action involving payment or form submission. (2) Data leakage: the agent might navigate to pages containing sensitive information; restrict the agent's URL allowlist. (3) CAPTCHA circumvention: attempting to bypass CAPTCHAs violates terms of service; detect CAPTCHAs and escalate to a human."),
    ],
    "25.3": [
        ("Exercise 25.3.1: Computer Use vs. Browser Agents", "basic", "conceptual",
         "Compare computer use agents with browser agents. What additional capabilities do computer use agents have, and what new challenges do they introduce?",
         "Computer use agents interact with the full desktop environment (native apps, file managers, terminals) rather than just web browsers. Additional capabilities: running desktop applications, managing files, interacting with OS dialogs. New challenges: visual grounding (understanding screenshots of arbitrary UIs), larger action spaces, safety risks (access to the full system), and slower feedback loops (screenshots instead of DOM)."),
        ("Exercise 25.3.2: Screenshot-Based Interaction", "intermediate", "conceptual",
         "Explain how a computer use agent interprets a screenshot to decide its next action. What vision capabilities are required, and what are the failure modes?",
         "The agent receives a screenshot and uses vision-language model capabilities to identify UI elements (buttons, text fields, menus). It determines coordinates for clicking or typing. Required capabilities: OCR (reading text in images), element detection (identifying clickable areas), spatial reasoning (understanding layout). Failure modes: misidentifying UI elements, clicking the wrong coordinates, failing to detect pop-ups or overlays, and struggling with non-standard UI designs."),
        ("Exercise 25.3.3: Sandbox Configuration", "intermediate", "coding",
         "Write a Docker Compose configuration for a sandboxed computer use environment. Include a virtual display (Xvfb), a VNC server for monitoring, and resource limits (CPU, memory, network).",
         "Use an Ubuntu base image with Xvfb for headless display and x11vnc for remote viewing. Set <code>cpus: '1.0'</code>, <code>mem_limit: 2g</code>, and restrict network access to an allowlist. Map the VNC port for monitoring. Install only the applications the agent needs. This provides a safe environment where the agent cannot affect the host system."),
        ("Exercise 25.3.4: Action Space Design", "advanced", "conceptual",
         "Design an action space for a computer use agent that balances expressiveness with safety. What primitive actions should be available, and which actions should be restricted or require approval?",
         "Primitives: mouse click (left/right), mouse move, keyboard type, keyboard shortcut, screenshot, scroll, wait. Restricted actions: file deletion (require approval), network requests to unknown hosts (block), system settings changes (block), installing software (require approval). The action space should be minimal; avoid giving the agent unnecessary capabilities that increase the attack surface."),
        ("Exercise 25.3.5: Computer Use Evaluation", "intermediate", "conceptual",
         "How would you evaluate a computer use agent on a task like 'Open a spreadsheet, add a formula to column C that sums columns A and B, and save the file'? Define the success criteria and intermediate checkpoints.",
         "Success criteria: the file is saved and column C contains the correct SUM formula. Intermediate checkpoints: (1) the spreadsheet application is open, (2) the correct file is loaded, (3) the cursor is in the correct cell, (4) the formula is entered correctly, (5) the file is saved. Each checkpoint can be verified by taking a screenshot and checking for expected visual elements, or by inspecting the file contents after the task."),
    ],
    "25.4": [
        ("Exercise 25.4.1: Deep Research Agent Design", "intermediate", "conceptual",
         "Describe the architecture of a deep research agent. What distinguishes it from a simple RAG system, and what components are necessary for multi-step research?",
         "A deep research agent goes beyond single-query retrieval. It decomposes research questions into sub-questions, searches multiple sources, evaluates and cross-references findings, identifies gaps, and iterates until the question is thoroughly answered. Required components: a planner (decomposes questions), a search tool (web, papers, databases), a note-taking system (accumulates findings), and a synthesizer (produces the final report with citations)."),
        ("Exercise 25.4.2: Data Analysis Agent", "intermediate", "coding",
         "Write a prompt template for a data analysis agent that receives a CSV file path and a natural language question. The agent should generate Python code to analyze the data, execute it in a sandbox, and interpret the results.",
         "The prompt should include: (1) instructions to first read column names and data types, (2) generate pandas code for the analysis, (3) execute the code and capture output, (4) interpret numerical results in plain language. Include safety instructions: do not modify the original file, handle missing values, and validate results with sanity checks before reporting."),
        ("Exercise 25.4.3: Citation Verification", "advanced", "conceptual",
         "A research agent cites sources in its report. Design a verification pipeline that checks whether each citation actually supports the claim it is attached to.",
         "For each claim-citation pair: (1) retrieve the cited source, (2) extract the relevant passage, (3) use an LLM to evaluate whether the passage supports the claim (supports, contradicts, or is unrelated), (4) flag unsupported claims for human review. Also check: does the cited paper exist? Is the author attribution correct? Is the year correct? This catches hallucinated citations."),
        ("Exercise 25.4.4: Multi-Source Research", "intermediate", "coding",
         "Implement a research agent that searches three sources (arXiv, Wikipedia, and a web search engine) for information on a given topic, deduplicates findings, and produces a structured summary with source attribution.",
         "Create async tool functions for each source. Search all three in parallel. For each result, extract key claims and tag with the source. Use embedding similarity to identify duplicate claims across sources. Group unique claims into themes. Produce a structured summary with inline citations: 'Claim X (arXiv:2301.xxxxx, also confirmed by Wikipedia)."),
        ("Exercise 25.4.5: Scientific Discovery Agents", "advanced", "discussion",
         "Discuss the potential and limitations of AI agents for scientific discovery. Can an agent genuinely discover new knowledge, or is it limited to finding patterns in existing literature?",
         "Agents can: synthesize findings across papers that human researchers might miss, identify gaps in the literature, generate hypotheses based on pattern recognition, and automate routine analyses. Limitations: agents cannot run physical experiments, they may confuse correlation with causation, they can hallucinate plausible-sounding but incorrect claims, and they lack the deep domain intuition that guides human researchers toward fruitful directions."),
    ],
    "25.5": [
        ("Exercise 25.5.1: Domain-Specific Safety Requirements", "basic", "conceptual",
         "For each domain (healthcare, legal, finance), identify one safety requirement that is unique to that domain and would not apply to a general-purpose agent.",
         "Healthcare: HIPAA compliance and clinical validation before any patient-facing recommendation. Legal: jurisdiction awareness (advice valid in California may be invalid in Texas). Finance: regulatory compliance (SEC rules for investment advice, anti-money-laundering checks for transactions). Each adds domain-specific constraints that shape the agent's architecture."),
        ("Exercise 25.5.2: Healthcare Agent Architecture", "intermediate", "conceptual",
         "Design the high-level architecture for a clinical decision support agent. What tools does it need, what guardrails must be in place, and how should it handle uncertainty?",
         "Tools: medical knowledge base search, drug interaction checker, clinical guidelines lookup, patient record reader. Guardrails: never provide a definitive diagnosis (always 'suggest consulting a physician'), flag drug interactions as high-priority alerts, require physician approval for treatment suggestions. Uncertainty handling: express confidence levels, present differential diagnoses rather than single answers, and escalate low-confidence cases."),
        ("Exercise 25.5.3: Legal Agent Citation Requirements", "intermediate", "coding",
         "Write a validation function that checks whether a legal agent's response includes proper citations. Every legal claim must reference a statute, case, or regulation. Flag uncited claims.",
         "Parse the response into individual claims (sentences). For each claim, check for citation patterns: case names (e.g., 'Smith v. Jones'), statute references (e.g., '26 U.S.C. section 501'), or regulation codes. Return a list of uncited claims with their positions. A production system would also verify that cited cases and statutes actually exist using a legal database lookup."),
        ("Exercise 25.5.4: Finance Agent Compliance", "advanced", "conceptual",
         "A finance agent provides investment recommendations. Describe the regulatory and ethical guardrails it must have, and explain the consequences of failing to implement them.",
         "Required guardrails: disclaimer that output is not financial advice, suitability checks (recommendations must match the user's risk profile), conflict of interest disclosure, audit trail of all recommendations, and compliance with SEC/FINRA rules. Failure consequences: regulatory fines, legal liability for unsuitable recommendations, loss of customer trust, and potential ban from providing advisory services."),
        ("Exercise 25.5.5: Cross-Domain Patterns", "basic", "conceptual",
         "Identify three design patterns that are common across healthcare, legal, and finance domain agents. Why do these patterns recur in high-stakes domains?",
         "(1) Human-in-the-loop for critical decisions (because errors have severe consequences). (2) Audit logging of all agent actions (because regulators require traceability). (3) Citation and evidence requirements (because claims must be verifiable). These patterns recur because high-stakes domains share the need for accountability, traceability, and human oversight."),
    ],
    "26.1": [
        ("Exercise 26.1.1: Agent Threat Model", "intermediate", "conceptual",
         "Describe three attack vectors specific to AI agents that do not apply to standard LLM chatbots. For each, explain why the agent's tool access creates the vulnerability.",
         "(1) Indirect prompt injection via tool outputs: a malicious website returns text that instructs the agent to take harmful actions. (2) Tool abuse: the agent is tricked into calling destructive tools (e.g., deleting files). (3) Data exfiltration: the agent reads sensitive data through one tool and leaks it through another (e.g., reads a password file then sends it via email tool). Tool access amplifies the impact of prompt injection."),
        ("Exercise 26.1.2: Prompt Injection Defense", "intermediate", "coding",
         "Implement a simple prompt injection detector that scans tool outputs for common injection patterns (e.g., 'ignore previous instructions', 'you are now', 'system prompt'). Return a risk score from 0 to 1.",
         "Define a list of injection patterns as regular expressions. Score each tool output by counting pattern matches, weighting by severity. Normalize to 0 to 1. If the score exceeds a threshold (e.g., 0.5), quarantine the tool output and either sanitize it or refuse to pass it to the agent. This is a first-line defense; production systems should also use classifier-based detection."),
        ("Exercise 26.1.3: Guardrail Layering", "basic", "conceptual",
         "Explain the concept of defense-in-depth for agent safety. Why is a single guardrail layer insufficient, and what layers should a production agent have?",
         "A single layer can be bypassed. Defense-in-depth layers: (1) input validation (reject malformed requests), (2) prompt injection detection (scan for injection attempts), (3) tool-level permissions (restrict which tools can be called), (4) output filtering (scan responses for harmful content), (5) action confirmation (require approval for high-risk actions), (6) monitoring and alerting (detect anomalous behavior patterns)."),
        ("Exercise 26.1.4: Tool Permission Matrix", "intermediate", "coding",
         "Design and implement a permission matrix that maps user roles to allowed tools and allowed argument patterns. An admin can use all tools; a regular user cannot use file_delete or run commands with sudo.",
         "Create a dictionary mapping roles to sets of allowed tools. For each tool, define argument validators (e.g., <code>run_command</code> rejects arguments containing 'sudo', 'rm -rf', or pipe operators for non-admin users). Check permissions before every tool execution. Log permission denials for security monitoring."),
        ("Exercise 26.1.5: Content Filtering Pipeline", "advanced", "conceptual",
         "Design a content filtering pipeline for an agent that handles both input (user messages, tool outputs) and output (agent responses, tool calls). Describe each stage and its purpose.",
         "Input pipeline: (1) PII detection and redaction, (2) prompt injection scanning, (3) content policy check (reject harmful requests). Output pipeline: (1) response content safety check, (2) tool call validation (are the arguments safe?), (3) PII leakage check (is the response about to reveal sensitive data?). Each stage operates independently so a failure in one does not skip subsequent checks."),
    ],
    "26.2": [
        ("Exercise 26.2.1: Why Sandboxing Matters", "basic", "conceptual",
         "Explain why sandboxed execution is described as 'non-negotiable' for agents that run code. Give two concrete examples of what could go wrong without sandboxing.",
         "Without sandboxing, generated code runs with the agent's full system privileges. Example 1: the agent generates <code>import os; os.system('rm -rf /')</code> due to a prompt injection, deleting the host filesystem. Example 2: the agent generates code that reads environment variables containing API keys and sends them to an external URL. Sandboxing isolates the execution environment so these actions either fail or are contained."),
        ("Exercise 26.2.2: Docker Sandbox Configuration", "intermediate", "coding",
         "Write a Dockerfile for a minimal Python sandbox that includes only essential packages (numpy, pandas, matplotlib) and runs as a non-root user with no network access.",
         "Use <code>FROM python:3.11-slim</code>. <code>RUN pip install numpy pandas matplotlib</code>. <code>RUN useradd -m sandbox</code>. <code>USER sandbox</code>. <code>WORKDIR /home/sandbox</code>. Run with <code>docker run --network=none --read-only --tmpfs /tmp:size=100m --cpus=1 --memory=512m</code>. The <code>--network=none</code> flag prevents data exfiltration; <code>--read-only</code> prevents filesystem modification outside /tmp."),
        ("Exercise 26.2.3: Resource Limits", "intermediate", "conceptual",
         "An agent generates code that enters an infinite loop, consuming 100% CPU indefinitely. Describe three resource limiting mechanisms and explain how each prevents this scenario.",
         "(1) CPU time limit: kill the process after N seconds of CPU time. (2) Memory limit: OOM-kill the process if it exceeds a memory threshold. (3) Process count limit: prevent fork bombs by limiting the number of child processes. Docker provides all three via <code>--cpus</code>, <code>--memory</code>, and <code>--pids-limit</code>. Additionally, a wall-clock timeout ensures the container is killed even if the process is sleeping rather than consuming CPU."),
        ("Exercise 26.2.4: Sandbox Escape Prevention", "advanced", "conceptual",
         "List three common sandbox escape techniques and describe how to mitigate each in the context of agent code execution.",
         "(1) Mounting host directories: mitigate by never mounting host volumes into the sandbox; use volume copies instead. (2) Privileged container escape: mitigate by running with <code>--security-opt=no-new-privileges</code> and dropping all Linux capabilities. (3) Network-based escape: mitigate by disabling networking entirely or restricting to an allowlist of hosts. Also use seccomp profiles to restrict system calls."),
        ("Exercise 26.2.5: E2B vs. Docker", "basic", "conceptual",
         "Compare E2B (cloud sandboxing service) with self-managed Docker containers for agent code execution. What are the trade-offs in terms of setup complexity, security, and cost?",
         "E2B: zero setup, managed security, pay-per-use pricing, lower operational burden. Docker self-managed: more setup, you manage security patches, fixed infrastructure cost, full control. Choose E2B for rapid prototyping and small-scale deployments. Choose Docker for production systems where you need full control over the environment, data residency requirements, or high-volume execution where per-use pricing becomes expensive."),
    ],
    "26.3": [
        ("Exercise 26.3.1: Observability Requirements", "basic", "conceptual",
         "What makes observability for agentic systems harder than for traditional web applications? List three agent-specific observability challenges.",
         "(1) Non-deterministic execution paths: the same input can produce different action sequences across runs. (2) Multi-step traces: a single user request may generate dozens of LLM calls and tool executions. (3) Cost attribution: each step has a different token cost, making per-request cost tracking complex. Traditional request/response observability does not capture the branching, looping nature of agent execution."),
        ("Exercise 26.3.2: Trace Instrumentation", "intermediate", "coding",
         "Write a Python decorator <code>@trace_agent_step</code> that logs each agent step with: timestamp, step type (LLM call, tool call, decision), input tokens, output tokens, latency, and cost estimate.",
         "Use Python's <code>time</code> and <code>functools.wraps</code>. Before the function call, record the start time. After, calculate duration. For LLM calls, extract token counts from the response usage field. Estimate cost using a price-per-token lookup table. Log everything as a structured JSON object. Append to a trace list for the current request."),
        ("Exercise 26.3.3: Cost Budget Enforcement", "intermediate", "coding",
         "Implement a <code>BudgetEnforcer</code> class that tracks cumulative cost during an agent run and raises an exception if the budget is exceeded. Include a warning threshold at 80% of the budget.",
         "The class holds a <code>max_budget</code> and <code>current_spend</code>. Method <code>record_cost(amount)</code> adds to current_spend. If current_spend > 0.8 * max_budget, log a warning. If current_spend > max_budget, raise <code>BudgetExceededError</code>. Integrate by calling <code>record_cost()</code> after every LLM call and tool execution. Include a <code>remaining()</code> method the agent can query."),
        ("Exercise 26.3.4: Anomaly Detection", "advanced", "conceptual",
         "An agent suddenly starts making 10x more tool calls per request than usual. Design an anomaly detection system that catches this and triggers an alert.",
         "Track historical distributions of: tool calls per request, LLM calls per request, total tokens per request, and latency per request. Use rolling averages and standard deviations. Flag a request as anomalous if any metric exceeds mean + 3 standard deviations. Trigger alerts via PagerDuty or Slack. Also implement hard limits (absolute maximums) as a safety net independent of statistical detection."),
        ("Exercise 26.3.5: Cost Optimization", "intermediate", "analysis",
         "An agent pipeline costs $0.50 per request. Analyze the cost breakdown (40% planning LLM, 30% execution LLM, 20% embedding calls, 10% tool APIs) and propose three strategies to reduce total cost by at least 30%.",
         "(1) Use a smaller model for execution steps (replace the 30% execution cost with a model at 1/5 the price, saving ~24%). (2) Cache embedding results for repeated queries (reduce embedding costs by 50%, saving ~10%). (3) Implement semantic caching for planning: if a similar task was planned recently, reuse the plan (reduce planning costs by 30%, saving ~12%). Combined savings: ~46%."),
    ],
    "26.4": [
        ("Exercise 26.4.1: Error Recovery Patterns", "intermediate", "conceptual",
         "Compare three error recovery patterns for agents: simple retry, retry with backoff, and retry with adaptation. When is each pattern most appropriate?",
         "Simple retry: for transient errors that are likely to succeed on the next attempt (network blips). Retry with backoff: for rate-limited APIs where immediate retry would fail again. Retry with adaptation: for semantic errors where the same approach will keep failing; the agent modifies its strategy (e.g., uses a different tool or rephrases a query). Adaptation is most powerful but most expensive in LLM calls."),
        ("Exercise 26.4.2: Circuit Breaker Implementation", "intermediate", "coding",
         "Implement a circuit breaker for an agent's external API tool. After 3 consecutive failures, the circuit opens and returns a cached result or error message for 60 seconds before allowing retry.",
         "Track consecutive failures per tool. When failures reach the threshold, set state to 'open' with a timestamp. While open, return a fallback response without calling the API. After the timeout, set state to 'half-open' and allow one request. If it succeeds, reset to 'closed'. If it fails, return to 'open'. This prevents cascading failures and wasted API calls."),
        ("Exercise 26.4.3: Graceful Degradation Strategies", "intermediate", "conceptual",
         "An agent's primary web search tool is down. Describe three levels of graceful degradation the agent could implement.",
         "Level 1: Fall back to a secondary search tool (e.g., switch from Google to Bing). Level 2: Use cached search results from recent similar queries. Level 3: Inform the user that search is unavailable and provide the best answer possible from the agent's existing knowledge, clearly noting the limitation. Each level trades off result quality for availability."),
        ("Exercise 26.4.4: Error Classification", "advanced", "coding",
         "Write a function that classifies agent errors into categories (transient, permanent, resource, semantic) and returns the recommended recovery strategy for each.",
         "Parse error messages and HTTP status codes. Transient (5xx, timeout): retry with backoff. Permanent (4xx, authentication): do not retry, escalate or use alternative. Resource (rate limit, quota): retry after wait period from response headers. Semantic (invalid tool arguments, logic error): adapt approach, use different tool or reformulate query. Return a tuple of (category, strategy, retry_after_seconds)."),
        ("Exercise 26.4.5: Resilience Testing", "basic", "conceptual",
         "Explain how chaos engineering principles can be applied to test agent resilience. What failures should you simulate, and what outcomes should you verify?",
         "Simulate: tool timeouts, API errors (4xx, 5xx), malformed tool responses, slow responses, partial data returns. Verify: the agent handles each gracefully (no crashes), falls back to alternatives, informs the user appropriately, stays within cost budgets, and does not leak sensitive information in error messages. Run these tests regularly as part of CI/CD to catch regressions."),
    ],
    "26.5": [
        ("Exercise 26.5.1: Multi-Agent Testing Challenges", "basic", "conceptual",
         "Why is testing multi-agent systems harder than testing single agents? Identify three challenges specific to multi-agent interactions.",
         "(1) Emergent behavior: the system's behavior is not simply the sum of individual agents; interactions produce unexpected outcomes. (2) Non-deterministic message ordering: agents may process messages in different orders across runs. (3) State explosion: with N agents and M possible states each, the state space grows as M^N. Traditional unit testing of individual agents misses interaction bugs."),
        ("Exercise 26.5.2: Contract Testing", "intermediate", "coding",
         "Implement a simple contract test for two agents: a 'requester' agent that sends tasks in a specific JSON format and a 'worker' agent that returns results in another format. Verify that both agents respect the contract.",
         "Define JSON schemas for the request and response formats. Write tests that: (1) generate a request from the requester agent and validate it against the request schema, (2) send the request to the worker agent and validate its response against the response schema, (3) verify round-trip consistency (the response references the correct request ID). Use <code>jsonschema.validate()</code> for schema checking."),
        ("Exercise 26.5.3: Chaos Engineering for Agents", "advanced", "coding",
         "Design a chaos testing framework that randomly injects failures into a multi-agent system: dropping messages between agents, adding latency, and corrupting tool outputs. Track how the system degrades.",
         "Create a proxy layer between agents that randomly: (1) drops N% of messages, (2) adds random delays (100ms to 5s), (3) corrupts tool outputs by replacing content with garbage. Run the system on a set of test tasks and measure: task completion rate, average latency, error recovery success rate, and cost overhead. Compare against baseline (no chaos) to quantify resilience."),
        ("Exercise 26.5.4: Agent Interaction Traces", "intermediate", "conceptual",
         "How should multi-agent interaction traces be structured for debugging? What information should each trace entry contain, and how should traces be correlated across agents?",
         "Each trace entry: timestamp, agent_id, action_type (send, receive, tool_call, decision), message content, parent_trace_id (for correlation). Use a shared trace_id across all agents working on the same task. Store traces in a time-series database. Visualization should show a timeline with swim lanes (one per agent) and arrows showing message flow. This makes it easy to spot communication failures and bottlenecks."),
        ("Exercise 26.5.5: Regression Testing Strategy", "intermediate", "conceptual",
         "Describe a regression testing strategy for a multi-agent system that is updated frequently. How do you balance test coverage with test execution time?",
         "Maintain a golden test set of representative tasks with verified outputs. Run the full set on every major release. For frequent updates, use a smaller smoke test set (10% of tasks) that covers the most critical paths. Use LLM-as-judge to evaluate output quality for tasks without exact-match answers. Track metrics over time to detect gradual degradation. Cache expensive tool calls in tests to reduce cost and latency."),
    ],
    "27.1": [
        ("Exercise 27.1.1: Diffusion Process Explanation", "basic", "conceptual",
         "Explain the forward and reverse processes of a diffusion model in your own words. Why is the reverse process harder than the forward process?",
         "Forward: gradually add Gaussian noise to an image over many steps until it becomes pure noise. This is simple (just add noise). Reverse: learn to predict and remove the noise at each step, gradually recovering the original image. This is harder because the model must learn the data distribution to know what 'clean' looks like. The reverse process is essentially learning to generate data from noise."),
        ("Exercise 27.1.2: Latent Diffusion Advantages", "basic", "conceptual",
         "What is the advantage of running diffusion in latent space (Stable Diffusion) rather than pixel space? What role does the VAE play in this architecture?",
         "Latent space diffusion operates on compressed representations (e.g., 64x64 latent instead of 512x512 pixels), making it dramatically faster and less memory-intensive. The VAE (Variational Autoencoder) compresses images to latent representations and decodes them back. This separation means the diffusion model works in a lower-dimensional space while the VAE handles the pixel-level details."),
        ("Exercise 27.1.3: Scheduler Comparison", "intermediate", "coding",
         "Generate images with a diffusion model using three different schedulers (DPM++, Euler, DDIM) at 20 and 50 steps each. Compare the visual quality and measure generation time for each configuration.",
         "Use the <code>diffusers</code> library. Load a pipeline, swap the scheduler using <code>pipe.scheduler = DPMSolverMultistepScheduler.from_config(...)</code>. Generate the same image (same prompt and seed) with each scheduler at both step counts. Record wall-clock time. Typically, DPM++ produces good results at fewer steps; DDIM is more deterministic; Euler is a good balance."),
        ("Exercise 27.1.4: Vision-Language Model Architecture", "intermediate", "conceptual",
         "Describe how a Vision-Language Model (VLM) like LLaVA processes an image and text query together. What is the role of the vision encoder, and how are visual features integrated with the language model?",
         "The vision encoder (e.g., CLIP ViT) processes the image into a sequence of visual feature tokens. These tokens are projected into the language model's embedding space via a projection layer. The language model receives the visual tokens concatenated with the text tokens and processes them together. This allows the model to reason about the image content in natural language."),
        ("Exercise 27.1.5: Classifier-Free Guidance", "advanced", "coding",
         "Implement classifier-free guidance (CFG) from scratch for a pre-trained diffusion model. Show how increasing the guidance scale improves text-image alignment but may reduce diversity.",
         "At each denoising step, run two forward passes: one conditioned on the text prompt, one unconditional (empty prompt). The guided prediction = unconditional + scale * (conditional - unconditional). Higher scales push the output closer to the text description. Generate the same prompt with scales 1, 5, 10, 15. At high scales, images become oversaturated and less diverse. Plot the trade-off."),
    ],
    "27.2": [
        ("Exercise 27.2.1: TTS Architecture Overview", "basic", "conceptual",
         "Describe the key components of a modern text-to-speech system. What is the difference between a two-stage pipeline (text-to-mel then vocoder) and an end-to-end approach?",
         "Two-stage: a model like Tacotron converts text to a mel spectrogram, then a vocoder like HiFi-GAN converts the spectrogram to audio waveform. End-to-end: models like VALL-E or Bark generate audio tokens directly from text, often producing more natural prosody. Two-stage is more interpretable; end-to-end is simpler to deploy but harder to debug."),
        ("Exercise 27.2.2: Voice Cloning Ethics", "intermediate", "discussion",
         "A company wants to use voice cloning to create custom voices for their customer service bot. Discuss the ethical considerations, potential harms, and safeguards they should implement.",
         "Considerations: consent (the voice donor must explicitly consent), misuse potential (deepfake audio for fraud), identity rights (who owns a synthetic voice?). Safeguards: require explicit consent with clear usage terms, embed audio watermarks in synthetic speech, implement speaker verification to prevent unauthorized cloning, and maintain an audit trail of all voice cloning requests."),
        ("Exercise 27.2.3: Music Generation Constraints", "intermediate", "conceptual",
         "Compare MusicGen and Suno in terms of architecture, output quality, and controllability. What are the current limitations of AI music generation?",
         "MusicGen (Meta): transformer-based, generates from text prompts and optional melody conditioning, good controllability. Suno: proprietary, generates vocals and instruments, higher production quality. Limitations: long-range structure (songs lack coherent song-level form), repetitive patterns, limited genre coverage, copyright concerns with training data, and difficulty with complex musical concepts like counterpoint."),
        ("Exercise 27.2.4: Video Generation Pipeline", "intermediate", "coding",
         "Write Python code that generates a short video clip from a text description using a text-to-video model. Include frame rate configuration and output file saving.",
         "Use a model like ModelScope or CogVideo via the <code>diffusers</code> library. Load the pipeline, set the prompt, configure <code>num_frames</code> and <code>fps</code>. Generate frames, then export as an MP4 using <code>export_to_video(frames, 'output.mp4', fps=8)</code>. Current models generate short clips (2 to 4 seconds); longer videos require frame interpolation or sequential generation."),
        ("Exercise 27.2.5: Temporal Consistency", "advanced", "conceptual",
         "Why is temporal consistency a major challenge in video generation? Explain the problem and describe two techniques that modern video models use to maintain consistency across frames.",
         "Temporal consistency means objects should maintain their appearance, position, and physics across frames. Without it, objects flicker, change shape, or teleport. Techniques: (1) Temporal attention layers that attend across frames (not just spatially within a frame), allowing the model to maintain object identity. (2) Motion conditioning (optical flow or motion vectors) that provides explicit movement guidance, reducing random frame-to-frame variations."),
    ],
    "27.3": [
        ("Exercise 27.3.1: TrOCR vs. Traditional OCR", "basic", "conceptual",
         "Compare TrOCR (transformer-based OCR) with traditional OCR approaches (Tesseract). What advantages do transformer models bring to text recognition?",
         "Traditional OCR (Tesseract): rule-based character segmentation, limited context awareness, struggles with handwriting and unusual fonts. TrOCR: encoder-decoder transformer, learns character recognition from context, handles diverse fonts and handwriting, produces higher accuracy on complex layouts. TrOCR benefits from pre-training on large datasets and can be fine-tuned for domain-specific documents."),
        ("Exercise 27.3.2: LayoutLM Document Understanding", "intermediate", "conceptual",
         "Explain how LayoutLM incorporates spatial information (x, y coordinates) into text understanding. Why is spatial information important for document AI?",
         "LayoutLM adds 2D positional embeddings to each token based on its bounding box coordinates in the document. This lets the model understand that 'Total: $100' at the bottom right of an invoice means something different from the same text in a body paragraph. Spatial information is critical because documents use layout (tables, headers, columns) to convey meaning that is lost in plain text extraction."),
        ("Exercise 27.3.3: Document AI Pipeline", "intermediate", "coding",
         "Design a document processing pipeline that takes a PDF, performs OCR, extracts structured fields (date, amount, vendor), and returns a JSON object. Describe each stage and its purpose.",
         "Stage 1: PDF to images (pdf2image). Stage 2: OCR with TrOCR or Tesseract to extract text with bounding boxes. Stage 3: Layout analysis to identify regions (header, table, body). Stage 4: Field extraction using a fine-tuned LayoutLM or an LLM with the extracted text and coordinates. Stage 5: Validation (check date format, amount is numeric, vendor matches known list). Return structured JSON."),
        ("Exercise 27.3.4: Table Extraction", "advanced", "coding",
         "Write code to extract tables from a document image. Use a model or heuristic to detect table boundaries, then parse the table into rows and columns.",
         "Use a table detection model (e.g., DETR fine-tuned on PubTables-1M) to identify table bounding boxes. Crop the table region. Use OCR to extract text with coordinates. Group text by rows (similar y-coordinates) and columns (similar x-coordinates). Build a 2D array and export as a pandas DataFrame. Handle merged cells by checking for spans."),
        ("Exercise 27.3.5: Document AI Evaluation", "intermediate", "conceptual",
         "How should document understanding models be evaluated? Describe appropriate metrics for OCR accuracy, field extraction accuracy, and end-to-end pipeline performance.",
         "OCR: Character Error Rate (CER) and Word Error Rate (WER). Field extraction: precision, recall, and F1 per field type. End-to-end: exact match rate for each extracted field, plus a 'document accuracy' score (fraction of documents where all fields are correct). Also measure processing time per document and cost per page for production viability."),
    ],
    "27.4": [
        ("Exercise 27.4.1: Pipeline vs. Native Multimodal", "basic", "conceptual",
         "Compare pipeline multimodal systems (separate models connected by code) with native multimodal models (single model processing multiple modalities). What are the advantages of each approach?",
         "Pipeline: easier to build, each component can be optimized independently, easier to debug and replace individual parts. Native: lower latency (single forward pass), better cross-modal understanding (visual and text features interact at every layer), can capture subtle relationships that pipeline approaches miss. Pipeline is pragmatic today; native is the future direction."),
        ("Exercise 27.4.2: Early vs. Late Fusion", "intermediate", "conceptual",
         "Explain early fusion and late fusion in multimodal architectures. Draw (or describe) the information flow in each approach and discuss when each is preferred.",
         "Early fusion: combine modalities at the input level (e.g., interleave image tokens with text tokens before processing). Advantage: deep cross-modal interaction from the first layer. Late fusion: process each modality with separate encoders, then combine the representations later. Advantage: each encoder can be pre-trained independently. Early fusion is better for tasks requiring tight integration (VQA); late fusion is better for tasks where modalities are loosely related (retrieval)."),
        ("Exercise 27.4.3: Multimodal Prompt Design", "intermediate", "coding",
         "Write a multimodal prompt using the Anthropic API that sends an image along with a text question. The prompt should ask the model to describe the image and identify any text visible in it.",
         "Use <code>anthropic.Anthropic().messages.create()</code> with a message containing both an <code>image</code> content block (base64-encoded or URL) and a <code>text</code> content block with the question. The model processes both together and returns a unified response that references visual and textual content from the image."),
        ("Exercise 27.4.4: Any-to-Any Generation", "advanced", "conceptual",
         "Describe the concept of 'any-to-any' generation in unified multimodal models. What architectural innovations make it possible for a single model to both understand and generate across modalities?",
         "Any-to-any means the model can take any combination of modalities as input and produce any modality as output (text to image, image to text, audio to text, etc.). Key innovations: (1) shared tokenization across modalities (images, audio, and text all become token sequences), (2) a single transformer that processes all modalities, and (3) modality-specific decoders that convert output tokens back to images, audio, or text."),
        ("Exercise 27.4.5: Multimodal Benchmark Analysis", "intermediate", "analysis",
         "Compare the performance of GPT-4o, Gemini, and Claude on multimodal benchmarks (MMMU, MathVista). What patterns emerge in their strengths and weaknesses?",
         "GPT-4o: strong on visual reasoning and chart understanding. Gemini: strong on long-context multimodal tasks and video understanding. Claude: strong on document analysis and careful instruction following. Patterns: all models struggle with tasks requiring precise spatial reasoning or counting objects in complex scenes. Performance on text-heavy images (documents, code screenshots) is generally better than on natural scenes requiring fine-grained visual understanding."),
    ],
    "28.1": [
        ("Exercise 28.1.1: Code Completion Internals", "basic", "conceptual",
         "Explain how fill-in-the-middle (FIM) code completion works. How does it differ from standard left-to-right text generation, and why is FIM particularly useful for code editing?",
         "Standard generation predicts the next token from left to right. FIM rearranges the input as [prefix] [suffix] [middle], training the model to generate the middle portion given surrounding context. This is crucial for code editing because developers often need to insert code between existing lines, not just append at the end. FIM enables inline completions, function body generation, and gap filling."),
        ("Exercise 28.1.2: IDE Integration Architecture", "intermediate", "conceptual",
         "Describe the architecture of a coding assistant like Copilot or Cursor. How does it capture context from the IDE, send it to the model, and present suggestions to the developer?",
         "The IDE extension captures: current file content, cursor position, open files, recent edits, and project structure. It sends a context-optimized prompt (current file with cursor marker, relevant snippets from other files) to the model. Suggestions are returned and displayed as inline ghost text or in a sidebar. The system uses debouncing to avoid sending requests on every keystroke and caching to speed up repeated patterns."),
        ("Exercise 28.1.3: Agentic Coding Workflow", "intermediate", "coding",
         "Write a prompt template for an agentic coding workflow where the AI reads a feature specification, searches the existing codebase for relevant files, generates the implementation, and writes tests.",
         "The prompt should instruct the agent to: (1) read the spec and identify required changes, (2) use a search tool to find related files and understand existing patterns, (3) plan the implementation (which files to create/modify), (4) generate code following existing style conventions, (5) write tests that cover the new functionality. Include constraints: do not break existing tests, follow the project's coding standards, and explain each file change."),
        ("Exercise 28.1.4: Code Review with LLMs", "intermediate", "coding",
         "Write a Python function that takes a git diff and uses an LLM to review the code changes, identifying potential bugs, style issues, and security concerns. Return structured feedback.",
         "Parse the diff to extract changed files and line ranges. Construct a prompt that includes the diff and asks the model to review for: correctness (logic errors), security (injection, hardcoded secrets), performance (unnecessary loops, N+1 queries), and style (naming, formatting). Parse the response into a structured format: [{file, line, severity, category, message}]. Filter for actionable findings only."),
        ("Exercise 28.1.5: Vibe-Coding Quality Control", "basic", "discussion",
         "A junior developer uses AI to generate 80% of their code without reviewing it carefully. What risks does this create, and what processes should the team implement to maintain code quality?",
         "Risks: undetected bugs, security vulnerabilities, code the developer cannot maintain or debug, inconsistent architecture decisions, and accumulating technical debt. Processes: mandatory code review by a senior developer, comprehensive test requirements (if the developer cannot write tests for the code, they do not understand it), regular architecture reviews, and pairing sessions where the developer explains the AI-generated code to ensure understanding."),
    ],
    "28.2": [
        ("Exercise 28.2.1: Financial Sentiment Analysis", "intermediate", "coding",
         "Write a Python function that uses an LLM to classify financial news headlines as positive, negative, or neutral for a given stock. Include confidence scores and test with 5 example headlines.",
         "Send each headline with the prompt: 'Classify this financial headline for [stock] as positive, negative, or neutral. Return JSON with sentiment and confidence (0 to 1).' Use structured output. Test with headlines like 'Apple beats Q4 earnings expectations' (positive), 'FDA delays drug approval for Pfizer' (negative). Compare results with a domain-specific model like FinBERT for validation."),
        ("Exercise 28.2.2: Automated Report Generation", "intermediate", "coding",
         "Design a prompt that takes a JSON object of financial metrics (revenue, expenses, profit margin, YoY growth) and generates a quarterly earnings summary paragraph suitable for investor communications.",
         "The prompt should include the metrics and instructions to: write in formal financial reporting style, highlight key trends, compare to previous quarters if data is provided, note any concerning metrics, and keep the summary to one paragraph. Include a constraint: do not make claims not supported by the data. Test with sample Q3 vs Q4 data."),
        ("Exercise 28.2.3: Trading Signal Limitations", "intermediate", "conceptual",
         "Discuss the limitations and risks of using LLMs to generate trading signals. Why should LLM-based signals be treated as one input among many rather than as standalone trading advice?",
         "Limitations: LLMs have knowledge cutoffs and may not reflect the latest market conditions. They can hallucinate correlations. They cannot process real-time market data. They may reflect biases from training data (survivorship bias in financial narratives). Risks: over-reliance on a single model, regulatory exposure (SEC has rules about automated trading advice). LLM signals should complement quantitative models, fundamental analysis, and human judgment."),
        ("Exercise 28.2.4: Aspect-Based Sentiment for Earnings", "advanced", "coding",
         "Implement aspect-based sentiment analysis for an earnings call transcript. Extract sentiments for specific aspects: revenue, margins, guidance, and competition. Return a structured report.",
         "Split the transcript into paragraphs. For each paragraph, identify which aspects are discussed (use keyword matching or an LLM classifier). For each aspect mention, extract the sentiment and a supporting quote. Aggregate sentiments per aspect across the full transcript. Output: {aspect: {sentiment: pos/neg/neutral, confidence: float, supporting_quotes: [str]}}."),
        ("Exercise 28.2.5: Fraud Detection Considerations", "basic", "conceptual",
         "How can LLMs assist in fraud detection and KYC/AML processes? What are the risks of using LLMs for compliance-critical tasks, and what safeguards are needed?",
         "LLMs can: analyze transaction narratives for suspicious patterns, extract entities from documents for KYC verification, summarize suspicious activity reports, and translate compliance rules into monitoring queries. Risks: hallucinated findings (false positives or missed fraud), lack of auditability (regulators need explainable decisions), and liability for missed fraud. Safeguards: human review of all flagged cases, audit logging, regular model validation against known fraud cases."),
    ],
    "28.3": [
        ("Exercise 28.3.1: Medical LLM Evaluation", "basic", "conceptual",
         "Why do medical LLMs (Med-PaLM, BioGPT) need separate evaluation from general-purpose LLMs? What medical benchmarks exist, and what do they measure?",
         "Medical LLMs need domain-specific evaluation because general benchmarks do not test clinical knowledge, reasoning with medical terminology, or safety in healthcare contexts. Key benchmarks: MedQA (medical licensing exam questions), PubMedQA (biomedical literature questions), MMLU medical subsets. They measure: factual medical knowledge, clinical reasoning, ability to handle uncertainty, and appropriate use of medical terminology."),
        ("Exercise 28.3.2: Clinical NLP Pipeline", "intermediate", "coding",
         "Design a clinical NLP pipeline that extracts medications, diagnoses, and procedures from a clinical note. Specify the model choices, preprocessing steps, and output format.",
         "Preprocessing: de-identify PHI (names, dates, MRNs). Use a medical NER model (scispaCy or a fine-tuned BioBERT) to extract entities. Classify entities into categories: medication (drug name, dose, frequency), diagnosis (ICD-10 code mapping), procedure (CPT code mapping). Output as FHIR-compatible JSON resources. Validate against a medical terminology service (UMLS, SNOMED CT)."),
        ("Exercise 28.3.3: Safety in Medical AI", "intermediate", "conceptual",
         "Describe three critical safety considerations for deploying LLMs in healthcare settings. For each, explain the potential harm and the required safeguard.",
         "(1) Hallucinated medical advice: the model generates plausible but incorrect treatment recommendations. Safeguard: never present LLM output as medical advice; always require physician review. (2) PHI leakage: patient data appears in model outputs. Safeguard: de-identify all inputs, use on-premise models, and audit outputs. (3) Bias in training data: model performs worse for underrepresented populations. Safeguard: evaluate performance across demographic groups and validate with diverse clinical data."),
        ("Exercise 28.3.4: Drug Interaction Checker", "advanced", "coding",
         "Write a function that uses an LLM to check for potential drug interactions given a list of medications. Cross-reference with a structured drug database and highlight discrepancies between the LLM's output and the database.",
         "Input: list of medication names. Step 1: query the LLM for potential interactions between all pairs. Step 2: query a drug interaction database (e.g., DrugBank API or OpenFDA). Step 3: compare results. Flag cases where the LLM identifies an interaction the database misses (potential hallucination) and where the database identifies one the LLM misses (potential gap). The database is the authority; the LLM supplements."),
        ("Exercise 28.3.5: Medical QA System Design", "intermediate", "conceptual",
         "Design a medical question-answering system that uses RAG to answer questions from clinical guidelines. What retrieval strategy should you use, and how should you handle questions where the guidelines are ambiguous?",
         "Use a retrieval system over a curated index of clinical guidelines (e.g., UpToDate, WHO guidelines). Chunk by section with overlap. Retrieve top-k relevant sections using hybrid search (BM25 + embeddings). For ambiguous questions: present multiple guideline perspectives with citations, explicitly note where guidelines disagree or where evidence is limited, and recommend consulting a specialist. Never present a definitive answer for ambiguous clinical questions."),
    ],
    "28.4": [
        ("Exercise 28.4.1: LLM as Recommendation Engine", "basic", "conceptual",
         "How can an LLM be used as a recommendation engine? Compare the LLM-based approach with traditional collaborative filtering. What are the strengths and limitations of each?",
         "LLMs can generate recommendations by reasoning about user preferences described in natural language, handling the cold-start problem well, and explaining their recommendations. Collaborative filtering excels with large interaction datasets and produces more statistically reliable recommendations. LLM limitations: no access to behavioral data (clicks, purchases), higher latency, and potential to hallucinate non-existent items. Best approach: combine both."),
        ("Exercise 28.4.2: Semantic Search Implementation", "intermediate", "coding",
         "Implement a simple LLM-powered search system that rewrites a user's natural language query into multiple search queries, retrieves results from each, and re-ranks the combined results.",
         "Step 1: use an LLM to generate 3 query variations from the user's input (synonym expansion, specificity adjustment, related concepts). Step 2: execute each query against a search index. Step 3: deduplicate results. Step 4: re-rank using an LLM or a cross-encoder that scores relevance of each result to the original query. Return the top-k results with relevance scores."),
        ("Exercise 28.4.3: Conversational Recommendation", "intermediate", "conceptual",
         "Design a conversational recommendation system that progressively refines suggestions based on user feedback. How should the system balance exploration (showing diverse options) and exploitation (showing likely matches)?",
         "The system asks clarifying questions to narrow preferences, presents diverse initial recommendations, and adapts based on feedback ('I like this one but want something cheaper'). Track user preferences as a running summary. For exploration/exploitation: start with diverse recommendations (explore), then narrow based on feedback (exploit), but periodically introduce a surprise option to discover new preferences the user has not expressed."),
        ("Exercise 28.4.4: NL-to-SQL for Analytics", "advanced", "coding",
         "Write a function that converts a natural language analytics question into a SQL query, executes it, and returns both the data and a natural language summary of the results.",
         "Provide the LLM with the database schema (table names, column names, types). Send the user's question and ask for a SQL query. Validate the query (no mutations, reasonable LIMIT). Execute against the database. Pass the results back to the LLM with the original question and ask for a plain-language summary. Include the SQL query in the response for transparency."),
        ("Exercise 28.4.5: User Preference Modeling", "intermediate", "conceptual",
         "Compare explicit preference modeling (user states preferences) with implicit preference modeling (inferred from behavior) in LLM-powered recommendation systems. What are the trade-offs?",
         "Explicit: more accurate (the user tells you what they want) but requires user effort and may not capture unconscious preferences. Implicit: requires no user effort, captures actual behavior, but is noisier and harder to interpret. LLMs enable a hybrid approach: track implicit signals (click patterns, time spent) and use the LLM to synthesize them into a natural language preference profile that can be refined through conversation."),
    ],
    "28.5": [
        ("Exercise 28.5.1: Threat Intelligence with LLMs", "intermediate", "conceptual",
         "Describe three ways LLMs can enhance cybersecurity threat intelligence. For each, explain the current state of the art and its limitations.",
         "(1) Threat report summarization: LLMs condense lengthy CVE reports into actionable summaries. Limited by hallucination risk for technical details. (2) IOC extraction: LLMs extract indicators of compromise (IPs, hashes, domains) from unstructured text. Limited by false positives and the need for validation. (3) Attack pattern classification: LLMs map observed behaviors to MITRE ATT&CK techniques. Limited by the model's knowledge cutoff and evolving attack techniques."),
        ("Exercise 28.5.2: Log Analysis Pipeline", "intermediate", "coding",
         "Write a Python function that uses an LLM to analyze a batch of security logs, identify anomalous patterns, and generate a structured alert with severity, description, and recommended response.",
         "Input: a list of log entries (timestamp, source, message). Send a batch (with token budget awareness) to the LLM with instructions to identify unusual patterns (failed logins, unusual access times, privilege escalations). Return structured JSON: [{severity: high/medium/low, pattern: str, affected_systems: [str], evidence: [log_entries], recommended_action: str}]. Validate that the LLM's findings correspond to actual log entries."),
        ("Exercise 28.5.3: Vulnerability Detection", "advanced", "coding",
         "Write a prompt that asks an LLM to review a code snippet for security vulnerabilities. Test it on code with a known SQL injection vulnerability and a known XSS vulnerability.",
         "The prompt should ask the model to identify: (1) vulnerability type (OWASP category), (2) affected lines, (3) severity rating, (4) proof of concept exploit, (5) recommended fix. Test with: a Flask route that uses f-strings in SQL queries (SQL injection) and a template that renders user input without escaping (XSS). Verify the model catches both and produces correct fix recommendations."),
        ("Exercise 28.5.4: Adversarial Uses of LLMs", "intermediate", "conceptual",
         "Discuss three ways attackers can use LLMs offensively (phishing, malware generation, social engineering). For each, describe a defensive countermeasure.",
         "(1) Phishing: LLMs generate more convincing phishing emails. Defense: AI-powered email scanners that detect LLM-generated text patterns. (2) Malware generation: LLMs produce functional exploit code. Defense: most LLMs have safety filters, but open-source models may not; focus on endpoint detection rather than prevention. (3) Social engineering: LLMs automate personalized manipulation at scale. Defense: multi-factor authentication and user education about AI-powered social engineering."),
        ("Exercise 28.5.5: Security Audit Automation", "basic", "conceptual",
         "How can LLMs assist in automating security audits? What parts of a security audit can be automated, and what parts still require human expertise?",
         "Automatable: code scanning for known vulnerability patterns, configuration review against security baselines, log analysis for anomalies, compliance checklist verification, and report generation. Requires human expertise: threat modeling (understanding business context), assessing risk severity in the organization's specific context, evaluating novel attack vectors, and making risk acceptance decisions. LLMs are best as assistive tools that handle the tedious parts while humans focus on judgment."),
    ],
    "28.6": [
        ("Exercise 28.6.1: AI Tutoring System Design", "intermediate", "conceptual",
         "Design an AI tutoring system that adapts to the student's knowledge level. How should the system assess understanding, select difficulty, and provide feedback?",
         "Assessment: start with diagnostic questions to gauge baseline knowledge. Track correct/incorrect responses and time-to-answer. Difficulty selection: use a mastery model (move to harder content after N consecutive correct answers). Feedback: for incorrect answers, do not just give the correct answer; ask guiding questions that lead the student to discover the error. For correct answers, reinforce understanding with a brief explanation of why the answer is right."),
        ("Exercise 28.6.2: Legal Document Analysis", "intermediate", "coding",
         "Write a prompt that takes a contract clause and identifies: the parties involved, the obligations of each party, any conditions or exceptions, and potential risks. Return structured JSON.",
         "The prompt should instruct the model to parse the clause systematically: identify named parties, extract each party's obligations (must/shall language), find conditions (if/when/unless clauses), identify exceptions and limitations, and flag ambiguous language that could be disputed. Output: {parties: [], obligations: [{party, obligation, condition}], risks: [{description, severity}]}. Include a disclaimer that this is not legal advice."),
        ("Exercise 28.6.3: Creative Co-Authorship", "basic", "conceptual",
         "Discuss the role of LLMs as creative co-authors. How should the collaboration between human and AI be structured to produce the best creative output? What are the copyright implications?",
         "Best structure: the human provides creative direction, themes, and key decisions; the AI generates drafts, alternatives, and expansions; the human curates, edits, and makes final choices. This keeps human creative intent at the center. Copyright implications vary by jurisdiction: in the US, AI-generated content without significant human authorship may not be copyrightable. The key is demonstrating substantial human creative contribution to the final work."),
        ("Exercise 28.6.4: Style Transfer Implementation", "intermediate", "coding",
         "Write a function that uses an LLM to transfer the writing style of one text to another. Given a source text and a target style description (e.g., 'formal academic'), produce a rewritten version.",
         "Provide the LLM with: the source text, the target style description, and examples of the target style (few-shot). The prompt should instruct the model to preserve the original meaning while changing vocabulary, sentence structure, and tone to match the target style. Test with: informal email to formal business letter, technical documentation to layperson explanation."),
        ("Exercise 28.6.5: Customer Support Automation", "intermediate", "conceptual",
         "Design a customer support system that uses an LLM to handle Tier 1 inquiries and escalate complex issues to human agents. What criteria should trigger escalation?",
         "The LLM handles: FAQ responses, order status lookups, password resets, and simple troubleshooting. Escalation triggers: customer expresses frustration or anger (sentiment detection), the issue involves financial disputes, the LLM's confidence is below a threshold, the same issue has been raised multiple times without resolution, or the customer explicitly requests a human agent. Always inform the customer when they are talking to an AI."),
    ],
    "28.7": [
        ("Exercise 28.7.1: LLM as Robot Planner", "intermediate", "conceptual",
         "Explain how an LLM can serve as a high-level planner for a robot. What is the role of the LLM versus the low-level controller, and what are the challenges of grounding language in physical actions?",
         "The LLM takes a natural language instruction (e.g., 'make a sandwich') and decomposes it into a sequence of primitive actions (open fridge, pick up bread, etc.). The low-level controller translates each primitive into motor commands. Challenges: the LLM may generate physically impossible actions, it does not understand the robot's actual capabilities, and language is ambiguous (e.g., 'put it there' requires spatial grounding). Solutions: affordance functions that filter LLM suggestions based on what is physically possible."),
        ("Exercise 28.7.2: Vision-Language-Action Models", "advanced", "conceptual",
         "Describe the architecture of a Vision-Language-Action (VLA) model like RT-2 or pi0. How does it differ from using separate vision, language, and action models?",
         "A VLA model processes visual observations, language instructions, and action history in a single transformer. Actions are tokenized and predicted as part of the same token sequence as language. This differs from separate models because cross-modal interactions happen at every layer, allowing the model to ground language in visual observations and produce actions that are spatially and temporally coherent. Separate models require explicit translation between representations at each handoff."),
        ("Exercise 28.7.3: Sim-to-Real Transfer", "intermediate", "conceptual",
         "Explain the sim-to-real gap in robotics and how LLMs are being used to help bridge it. What role can LLMs play in generating simulation scenarios?",
         "The sim-to-real gap: policies trained in simulation often fail in the real world due to differences in physics, visual appearance, and sensor noise. LLMs help by: (1) generating diverse task descriptions that drive simulation scenario creation, (2) producing reward functions from natural language specifications, and (3) creating domain randomization parameters. This increases the diversity of training scenarios, making policies more robust to real-world variations."),
        ("Exercise 28.7.4: Scientific Literature Mining", "intermediate", "coding",
         "Write a Python function that takes a research topic, searches arXiv for relevant papers, extracts key findings from each abstract, and produces a structured literature review.",
         "Use the arXiv API to search for papers by topic. For each result, extract: title, authors, abstract, date. Send each abstract to an LLM to extract: main contribution, methodology, key results, and limitations. Group papers by theme using LLM-based clustering. Produce a structured review with sections: background, methods, findings, open questions. Include proper citations for every claim."),
        ("Exercise 28.7.5: AI for Mathematics", "advanced", "discussion",
         "Discuss the current capabilities and limitations of AI systems for mathematical reasoning. Can LLMs prove theorems, and if so, how do their approaches differ from human mathematicians?",
         "Current capabilities: LLMs can solve competition-level math problems (IMO 2024: AlphaProof solved 4 of 6 problems), generate and verify proofs in formal languages (Lean, Isabelle), and discover new patterns. Limitations: LLMs still struggle with multi-step logical reasoning, can produce plausible but incorrect proofs, and lack the creative intuition that guides human mathematicians toward interesting conjectures. The most effective approaches combine LLMs with formal verification systems that guarantee correctness."),
    ],
}


def build_exercise_html(section_num, exercises):
    """Build the exercise callout HTML for a section."""
    lines = []
    lines.append("")
    lines.append("    <h2>Exercises</h2>")
    lines.append("")

    for i, (title, level, ex_type, question, answer) in enumerate(exercises):
        lines.append(f'    <div class="callout exercise">')
        lines.append(f'        <div class="callout-title">{title} <span class="level-badge {level}" title="{level.capitalize()}">{level.upper()}</span> <span class="exercise-type {ex_type}" title="{ex_type.capitalize()}">{ex_type.capitalize()}</span></div>')
        lines.append(f'        <p>{question}</p>')
        lines.append(f'        <details>')
        lines.append(f'            <summary>Answer Sketch</summary>')
        lines.append(f'            <p>{answer}</p>')
        lines.append(f'        </details>')
        lines.append(f'    </div>')
        lines.append("")

    return "\n".join(lines)


def process_file(filepath, section_num):
    """Process a single section file to add exercise callouts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    exercises = EXERCISES.get(section_num)
    if not exercises:
        print(f"  WARNING: No exercises defined for section {section_num}")
        return False

    exercise_html = build_exercise_html(section_num, exercises)

    # Check if there's an existing old-style exercise section to replace
    # Pattern: <h2>Exercises: ... </h2> ... up to <div class="whats-next"> or <div class="whats-next">
    old_exercise_pattern = re.compile(
        r'(\n\s*<h2>Exercises:.*?</h2>.*?)(<div class="whats-next">)',
        re.DOTALL
    )

    match = old_exercise_pattern.search(content)
    if match:
        # Replace old exercises with new callout exercises
        new_content = content[:match.start(1)] + exercise_html + "\n" + content[match.start(2):]
        print(f"  Replaced old-style exercises in {os.path.basename(filepath)}")
    else:
        # Insert before "What Comes Next" div
        whats_next_pattern = re.compile(r'(<div class="whats-next">)')
        match2 = whats_next_pattern.search(content)
        if match2:
            new_content = content[:match2.start()] + exercise_html + "\n" + content[match2.start():]
            print(f"  Inserted new exercises in {os.path.basename(filepath)}")
        else:
            print(f"  ERROR: Could not find insertion point in {os.path.basename(filepath)}")
            return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    base = "E:/Projects/LLMCourse"

    # Map section numbers to file paths
    section_files = {}

    # Part 6
    part6_modules = {
        "22": "module-22-ai-agents",
        "23": "module-23-tool-use-protocols",
        "24": "module-24-multi-agent-systems",
        "25": "module-25-specialized-agents",
        "26": "module-26-agent-safety-production",
    }

    for mod_num, mod_dir in part6_modules.items():
        mod_path = os.path.join(base, "part-6-agentic-ai", mod_dir)
        for fname in sorted(os.listdir(mod_path)):
            if fname.startswith("section-") and fname.endswith(".html"):
                # Extract section number like "22.1" from "section-22.1.html"
                sec_num = fname.replace("section-", "").replace(".html", "")
                section_files[sec_num] = os.path.join(mod_path, fname)

    # Part 7
    part7_modules = {
        "27": "module-27-multimodal",
        "28": "module-28-llm-applications",
    }

    for mod_num, mod_dir in part7_modules.items():
        mod_path = os.path.join(base, "part-7-multimodal-applications", mod_dir)
        for fname in sorted(os.listdir(mod_path)):
            if fname.startswith("section-") and fname.endswith(".html"):
                sec_num = fname.replace("section-", "").replace(".html", "")
                section_files[sec_num] = os.path.join(mod_path, fname)

    print(f"Found {len(section_files)} section files")
    print(f"Exercises defined for {len(EXERCISES)} sections")

    success = 0
    failed = 0
    skipped = 0

    for sec_num in sorted(section_files.keys()):
        filepath = section_files[sec_num]
        print(f"\nProcessing section {sec_num}: {os.path.basename(filepath)}")

        if sec_num not in EXERCISES:
            print(f"  SKIPPED: No exercises defined")
            skipped += 1
            continue

        if process_file(filepath, sec_num):
            success += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print(f"Done: {success} success, {failed} failed, {skipped} skipped")


if __name__ == "__main__":
    main()
