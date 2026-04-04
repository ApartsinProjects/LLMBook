#!/usr/bin/env python3
"""Add exercises sections to all Part 6 section files."""
import re
import os

BASE = "E:/Projects/LLMCourse/part-6-agents-applications"

# Define exercises for each section file
EXERCISES = {
    # Module 22: AI Agents
    "module-22-ai-agents/section-22.1.html": {
        "title": "Exercises: Agent Foundations & Architectures",
        "exercises": [
            ("BASIC", "Conceptual", "Explain in your own words the difference between a chain, a router, and a full agent. Give a concrete use case where each would be the appropriate choice."),
            ("BASIC", "Conceptual", "List the four agentic design patterns (Ng, 2024) and describe a real-world scenario for each one. Which pattern would you choose for an automated customer support system, and why?"),
            ("INTERMEDIATE", "Conceptual", "A ReAct agent is stuck in a loop: it keeps searching for information, then deciding it needs more information, never producing a final answer. What are three strategies to break this loop? Compare the trade-offs of each."),
            ("INTERMEDIATE", "Coding", "Implement a minimal ReAct agent in Python that can answer questions using a web search tool and a calculator tool. Use the OpenAI or Anthropic API for the LLM. Your agent should handle at least 3 reasoning steps before producing a final answer. Test it on: 'What is the GDP per capita of France divided by the GDP per capita of Brazil?'"),
            ("INTERMEDIATE", "Coding", "Build a simple state machine agent with three states: PLANNING, EXECUTING, and REFLECTING. The agent should plan how to accomplish a user task, execute each step, and reflect on whether the result matches the plan. Use any LLM API."),
            ("INTERMEDIATE", "Conceptual", "Compare episodic memory, semantic memory, and procedural memory in the context of AI agents. For each type, explain what data is stored, when it is retrieved, and how it degrades over time."),
            ("ADVANCED", "Coding", "Implement a Reflexion-style agent that attempts a coding challenge, evaluates its own output, generates a verbal self-critique, and retries with the critique stored in memory. Measure how many attempts it takes to pass a set of 5 unit tests, compared to a baseline agent without self-reflection."),
            ("ADVANCED", "Conceptual", "A production agent uses both vector memory (for semantic retrieval) and graph memory (for relational queries). Design the memory architecture for a technical support agent that must remember past interactions, track relationships between products and known issues, and learn from resolved tickets. Sketch the data flow between the two memory systems."),
            ("ADVANCED", "Design", "You are building an agent for a pharmaceutical company that searches medical literature, extracts drug interaction data, and produces safety reports. Identify three failure modes specific to this domain and propose guardrails for each. Reference the cognitive architecture concepts from this section."),
            ("RESEARCH", "Open-ended", "The CoALA framework (Sumers et al., 2024) organizes agent architectures using concepts from cognitive science. Propose an extension to CoALA that incorporates metacognition: the ability of an agent to monitor and regulate its own cognitive processes. How would this differ from standard reflection loops?"),
        ]
    },
    "module-22-ai-agents/section-22.2.html": {
        "title": "Exercises: Tool Use & Function Calling",
        "exercises": [
            ("BASIC", "Conceptual", "Explain the difference between function calling and tool use. When would you prefer one approach over the other?"),
            ("BASIC", "Conceptual", "List three principles for designing effective JSON schemas for function calling. For each, give an example of a schema that violates the principle and explain what goes wrong."),
            ("INTERMEDIATE", "Coding", "Define a set of three tools (web search, file reader, and calculator) as JSON schemas compatible with the OpenAI function calling API. Then write a Python function that dispatches tool calls to the correct handler based on the model's response."),
            ("INTERMEDIATE", "Coding", "Build an MCP (Model Context Protocol) server that exposes a simple database query tool. The server should accept SQL queries and return results. Test it by connecting to a local SQLite database with sample data."),
            ("INTERMEDIATE", "Conceptual", "Parallel function calling allows the model to request multiple tool calls in a single turn. Describe two scenarios where parallel calling improves performance and one scenario where it could cause problems (e.g., race conditions, dependent calls)."),
            ("INTERMEDIATE", "Design", "Design a retry and error handling strategy for a function-calling agent that interacts with unreliable external APIs. Address timeout handling, partial results, and graceful degradation."),
            ("ADVANCED", "Coding", "Implement a tool-use agent that dynamically discovers available tools from an MCP server, reads their schemas, and decides which to use based on the user's query. The agent should handle tools it has never seen before by reading the schema descriptions."),
            ("ADVANCED", "Conceptual", "Compare the tool integration approaches of OpenAI (function calling), Anthropic (tool use), and Google (Gemini function declarations). What are the key differences in schema design, parallel calling support, and error handling? Which approach is most flexible for production use?"),
            ("RESEARCH", "Open-ended", "ToolLLM (Qin et al., 2023) scales to 16,000+ APIs. What challenges arise when an agent must choose from thousands of available tools? Propose an architecture that uses a retrieval step to narrow the tool set before invoking the LLM."),
        ]
    },
    "module-22-ai-agents/section-22.3.html": {
        "title": "Exercises: Planning & Agentic Reasoning",
        "exercises": [
            ("BASIC", "Conceptual", "What is the difference between a reactive agent and a planning agent? Give an example task where a reactive approach would fail but a planning approach would succeed."),
            ("BASIC", "Conceptual", "Describe the plan-and-execute architecture. What are the responsibilities of the planner versus the executor? Why is it useful to separate them?"),
            ("INTERMEDIATE", "Coding", "Implement a plan-and-execute agent that takes a complex research question, breaks it into subtasks, executes each subtask using web search, and synthesizes the results. Compare the quality of the final answer to a single-pass approach."),
            ("INTERMEDIATE", "Coding", "Build a reflection loop that generates code, tests it, critiques failures, and retries. Measure how many iterations it takes to solve 5 problems from the HumanEval benchmark. Cap the loop at 5 iterations per problem."),
            ("INTERMEDIATE", "Conceptual", "The LLM Compiler pattern executes independent plan steps in parallel. Identify a task with at least 4 steps where 2 can run in parallel and 2 must be sequential. Draw the dependency graph and estimate the speedup from parallel execution."),
            ("ADVANCED", "Coding", "Implement a simplified LATS (Language Agent Tree Search) agent that explores multiple plan branches for a given task, evaluates each branch with a scoring function, and selects the best path. Use at least 3 candidate branches."),
            ("ADVANCED", "Conceptual", "Compare three planning failure modes: (1) the plan is too vague to execute, (2) the plan is too rigid to adapt to unexpected results, and (3) the plan has an incorrect dependency ordering. For each, propose a detection mechanism and a recovery strategy."),
            ("ADVANCED", "Design", "Design a planning agent for an e-commerce company that must handle multi-step customer requests (e.g., 'Find a blue shirt in my size, check if it is in stock at my local store, and schedule a pickup'). Address how the planner handles partial failures and user preference changes mid-plan."),
            ("RESEARCH", "Open-ended", "Current planning agents rely on the LLM to decompose tasks. Research suggests that planning is one of the weakest capabilities of current LLMs. Propose a hybrid architecture that combines symbolic planning (e.g., PDDL) with LLM-based reasoning. What are the trade-offs?"),
        ]
    },
    "module-22-ai-agents/section-22.4.html": {
        "title": "Exercises: Code Agents & Sandboxing",
        "exercises": [
            ("BASIC", "Conceptual", "Why are code execution agents both the most powerful and most dangerous type of LLM agent? List three categories of risk and a mitigation strategy for each."),
            ("BASIC", "Conceptual", "Explain the difference between container-based sandboxing and microVM-based sandboxing. When would you choose each?"),
            ("INTERMEDIATE", "Coding", "Build a simple code execution agent that takes a natural language data analysis request, generates Python code using pandas, executes it in a sandboxed environment, and returns the results. Test it on a sample CSV dataset."),
            ("INTERMEDIATE", "Coding", "Implement a permission system for a code agent that restricts file system access to a specific directory, blocks network requests, and limits execution time to 30 seconds. Use Python's subprocess module with appropriate flags."),
            ("INTERMEDIATE", "Conceptual", "Compare the approaches of OpenAI Code Interpreter, Anthropic's computer use, and open-source alternatives like E2B for sandboxed code execution. What are the trade-offs in security, flexibility, and cost?"),
            ("ADVANCED", "Coding", "Build a software engineering agent that can read a GitHub issue, clone a repository, make a code change, run tests, and submit a pull request. Implement at least basic guardrails to prevent the agent from modifying files outside the target repository."),
            ("ADVANCED", "Design", "Design a data analysis agent for a hospital that must analyze patient data while complying with HIPAA. Address data access controls, audit logging, output sanitization (no PII in generated charts), and human-in-the-loop approval for sensitive queries."),
            ("ADVANCED", "Conceptual", "SWE-bench evaluates coding agents on real GitHub issues. Analyze why even the best agents (e.g., SWE-Agent, Devin) solve only a fraction of issues. What types of issues are hardest, and what architectural improvements might help?"),
            ("RESEARCH", "Open-ended", "Formal verification of agent-generated code is an open research problem. Propose a framework where the agent generates both code and a specification, then a verifier checks that the code satisfies the specification. What types of specifications can current LLMs reliably produce?"),
        ]
    },
    "module-22-ai-agents/section-22.5.html": {
        "title": "Exercises: Reasoning Models as Agent Backbones",
        "exercises": [
            ("BASIC", "Conceptual", "How do reasoning models (e.g., o1, Claude with extended thinking, DeepSeek-R1) differ from standard LLMs in terms of inference behavior? Why does this matter for agent design?"),
            ("BASIC", "Conceptual", "Explain the concept of a 'thinking budget' for reasoning models. Why is budget management especially important in agentic contexts where the model is called many times per task?"),
            ("INTERMEDIATE", "Coding", "Compare the performance of a standard model and a reasoning model on a multi-step agent task (e.g., a research question requiring 3+ tool calls). Measure both accuracy and total token cost. Use the same agent scaffolding for both."),
            ("INTERMEDIATE", "Conceptual", "Reasoning models internalize much of the chain-of-thought process. Does this mean external CoT prompting is unnecessary? Discuss cases where external scaffolding still adds value on top of a reasoning model."),
            ("INTERMEDIATE", "Design", "Design a thinking budget allocation strategy for an agent that processes customer support tickets. Some tickets are simple (password resets) and some are complex (billing disputes requiring multi-system lookups). How would you dynamically adjust the thinking budget?"),
            ("ADVANCED", "Coding", "Implement an agent that uses a reasoning model for planning and a standard model for routine execution steps. Compare the cost and quality of this hybrid approach against using the reasoning model for all steps."),
            ("ADVANCED", "Conceptual", "The extended thinking trace of reasoning models is often hidden from the application. Discuss the implications for agent observability and debugging. How can you build effective monitoring when you cannot inspect the model's reasoning?"),
            ("ADVANCED", "Design", "OpenAI's o3 and Anthropic's Claude with extended thinking take different approaches to exposing thinking tokens. Compare these approaches from the perspective of an agent developer who needs to debug failures and optimize costs."),
            ("RESEARCH", "Open-ended", "Test-time compute scaling laws suggest that more thinking tokens improve performance on harder problems. Propose an experiment to measure the relationship between thinking budget and agent task completion rate across tasks of varying difficulty. What would the ideal budget curve look like?"),
        ]
    },
    # Module 23: Multi-Agent Systems
    "module-23-multi-agent-systems/section-23.1.html": {
        "title": "Exercises: Multi-Agent Coordination Patterns",
        "exercises": [
            ("BASIC", "Conceptual", "List three multi-agent coordination patterns and explain when each is most appropriate. Use a real-world analogy (e.g., a hospital, a factory, a sports team) for each pattern."),
            ("BASIC", "Conceptual", "What is the difference between a supervisor pattern and a peer-to-peer pattern? Give a task where the supervisor pattern would introduce an unnecessary bottleneck."),
            ("INTERMEDIATE", "Coding", "Implement a simple supervisor-worker multi-agent system where the supervisor routes user requests to one of three specialist agents (search, calculation, summarization). Use any LLM API. Test with 5 diverse queries."),
            ("INTERMEDIATE", "Coding", "Build a pipeline multi-agent system for content creation: Agent 1 generates an outline, Agent 2 writes the draft, Agent 3 edits and polishes. Compare the output quality to a single agent doing all three steps."),
            ("INTERMEDIATE", "Conceptual", "Message passing between agents can use shared memory, direct messages, or a blackboard. Compare these three approaches in terms of scalability, debuggability, and fault tolerance."),
            ("ADVANCED", "Coding", "Implement a debate pattern where two agents argue opposing sides of a decision and a judge agent selects the better argument. Test it on three product recommendation scenarios. Measure whether the debate produces better recommendations than a single agent."),
            ("ADVANCED", "Design", "Design a multi-agent system for an insurance claims processing pipeline. Identify the specialist agents needed, the coordination pattern, and the escalation paths for edge cases. Address how to handle conflicting assessments from different agents."),
            ("ADVANCED", "Conceptual", "As the number of agents in a system grows, communication overhead can dominate computation time. Analyze the communication complexity of the supervisor pattern (star topology) versus the peer-to-peer pattern (mesh topology) for N agents. At what N does each pattern become impractical?"),
            ("RESEARCH", "Open-ended", "Emergent behavior in multi-agent systems is both a feature and a risk. Propose a monitoring framework that detects when agents develop unexpected communication patterns or workarounds that bypass intended workflows."),
        ]
    },
    "module-23-multi-agent-systems/section-23.2.html": {
        "title": "Exercises: Multi-Agent Frameworks in Practice",
        "exercises": [
            ("BASIC", "Conceptual", "Compare the design philosophies of AutoGen, CrewAI, and LangGraph for multi-agent systems. What type of application is each framework best suited for?"),
            ("BASIC", "Conceptual", "What is the role of a supervisor agent in a hierarchical multi-agent system? How does it differ from a simple router?"),
            ("INTERMEDIATE", "Coding", "Using CrewAI or AutoGen, build a research team with three agents: a researcher who searches for information, an analyst who synthesizes findings, and a writer who produces a final report. Run the team on a research question and evaluate the output."),
            ("INTERMEDIATE", "Coding", "Implement a LangGraph workflow with conditional edges: an agent that classifies user intent, then routes to either a customer support agent or a sales agent based on the classification. Include error handling for ambiguous intents."),
            ("INTERMEDIATE", "Conceptual", "Framework-based multi-agent systems can obscure what is happening at each step. Propose a logging strategy that captures agent-to-agent messages, tool calls, and decision points without excessive verbosity."),
            ("ADVANCED", "Coding", "Build the same multi-agent task (e.g., a blog post research and writing pipeline) in two different frameworks (e.g., AutoGen and CrewAI). Compare lines of code, execution time, token usage, and output quality. Document which framework made each aspect easier or harder."),
            ("ADVANCED", "Design", "Design a fault-tolerant multi-agent system where any agent can fail and the system continues to operate. Address agent restart, state recovery, and task redistribution. How do different frameworks support or hinder this?"),
            ("ADVANCED", "Conceptual", "Human-in-the-loop checkpoints are critical for production multi-agent systems. Identify three points in a typical multi-agent pipeline where human review should be mandatory, and explain how to implement approval gates without blocking the entire system."),
            ("RESEARCH", "Open-ended", "Current multi-agent frameworks use LLM calls for agent-to-agent communication, which is expensive. Propose an architecture where agents communicate through a shared structured state (e.g., a database or graph) instead of natural language messages. What are the trade-offs?"),
        ]
    },
    "module-23-multi-agent-systems/section-23.3.html": {
        "title": "Exercises: Communication, Trust & Failure Modes",
        "exercises": [
            ("BASIC", "Conceptual", "Define 'groupthink' in the context of multi-agent LLM systems. How can agents that use the same underlying model fall into conformity traps?"),
            ("BASIC", "Conceptual", "List three failure modes specific to multi-agent systems that do not exist in single-agent systems. For each, describe an observable symptom."),
            ("INTERMEDIATE", "Coding", "Implement a simple experiment: have 5 LLM agents independently answer a factual question, then have them discuss and converge on a group answer. Measure whether the group answer is more or less accurate than the best individual answer across 10 questions."),
            ("INTERMEDIATE", "Conceptual", "Trust between agents is a critical design consideration. Compare three trust models: (1) all agents are fully trusted, (2) output validation after each agent, (3) reputation-based trust that adjusts over time. What are the cost and reliability implications of each?"),
            ("INTERMEDIATE", "Design", "Design a communication protocol for agents that includes structured message types (request, response, error, escalation) rather than free-form text. What information should each message type contain?"),
            ("ADVANCED", "Coding", "Build a multi-agent system with intentional diversity: agents use different models (e.g., GPT-4o, Claude, Gemini) to reduce groupthink. Compare the diversity of outputs to a system where all agents use the same model."),
            ("ADVANCED", "Conceptual", "Cascading failures in multi-agent systems can be catastrophic. Analyze a scenario where Agent A provides incorrect data to Agent B, which makes a flawed decision that Agent C acts on irreversibly. Design circuit breakers at each handoff point."),
            ("ADVANCED", "Design", "Design an agent reputation system where agents accumulate trust scores based on the accuracy of their past contributions. How should the system handle: (a) new agents with no history, (b) agents that are accurate on easy tasks but fail on hard ones, and (c) adversarial agents?"),
            ("RESEARCH", "Open-ended", "Social simulation using LLM agents (e.g., Generative Agents by Park et al., 2023) reveals emergent social behaviors. Propose an experiment to study whether LLM agent groups exhibit the same cognitive biases (anchoring, confirmation bias, sunk cost) as human groups."),
        ]
    },
    "module-23-multi-agent-systems/section-23.4.html": {
        "title": "Exercises: Building Production Multi-Agent Systems",
        "exercises": [
            ("BASIC", "Conceptual", "What are the three most important differences between a demo multi-agent system and a production multi-agent system? For each, explain why the demo approach breaks at scale."),
            ("BASIC", "Conceptual", "Explain why observability is harder in multi-agent systems than in single-agent systems. What additional telemetry do you need to capture?"),
            ("INTERMEDIATE", "Coding", "Add comprehensive logging to a multi-agent system: capture each agent's input, output, token usage, latency, and the inter-agent messages. Visualize the execution trace as a timeline diagram."),
            ("INTERMEDIATE", "Coding", "Implement a cost monitoring dashboard for a multi-agent system that tracks per-agent token usage, total pipeline cost per request, and identifies which agent is the most expensive. Use any visualization library."),
            ("INTERMEDIATE", "Design", "Design a testing strategy for a 4-agent pipeline. Address unit testing individual agents, integration testing agent handoffs, and end-to-end testing the full pipeline. How do you handle non-determinism in LLM outputs?"),
            ("ADVANCED", "Coding", "Build a multi-agent system with graceful degradation: if the specialized agent fails or times out, the system falls back to a general-purpose agent. Implement retry logic, timeout handling, and fallback routing."),
            ("ADVANCED", "Design", "Design a deployment strategy for a multi-agent system where different agents have different scaling requirements. The supervisor needs low latency, the research agent needs high throughput, and the writing agent needs large context windows. How do you architect the infrastructure?"),
            ("ADVANCED", "Conceptual", "Version management in multi-agent systems is complex: upgrading one agent can break the communication contract with other agents. Propose a versioning and backward compatibility strategy inspired by API versioning best practices."),
            ("RESEARCH", "Open-ended", "The Agent-to-Agent (A2A) protocol aims to standardize inter-agent communication. Analyze the protocol's design and identify three limitations that would need to be addressed for enterprise adoption. Propose solutions for each."),
        ]
    },
    # Module 24: Multimodal
    "module-24-multimodal/section-24.1.html": {
        "title": "Exercises: Image Generation & Diffusion Models",
        "exercises": [
            ("BASIC", "Conceptual", "Explain the forward and reverse diffusion processes in your own words. Use an analogy to make the concept accessible to a non-technical audience."),
            ("BASIC", "Conceptual", "What is the advantage of running diffusion in latent space (as in Stable Diffusion) rather than directly in pixel space? What is the role of the VAE?"),
            ("INTERMEDIATE", "Coding", "Generate images with Stable Diffusion XL using three different schedulers (DPM++, Euler, DDIM). Compare the results visually at 20, 30, and 50 steps. Which scheduler produces the best quality at the fewest steps?"),
            ("INTERMEDIATE", "Coding", "Implement img2img (image-to-image) generation: take a photograph, add noise to it at a controlled strength, and denoise it with a text prompt to create a styled version. Experiment with different strength values (0.3, 0.5, 0.7)."),
            ("INTERMEDIATE", "Conceptual", "Compare the architectural approaches of DALL-E 3, Stable Diffusion 3, and Flux. What are the key differences in how they handle text conditioning, and which approach produces the most accurate text rendering in images?"),
            ("ADVANCED", "Coding", "Implement classifier-free guidance from scratch for a pre-trained diffusion model. Show that increasing the guidance scale improves text-image alignment but reduces output diversity. Plot the trade-off."),
            ("ADVANCED", "Conceptual", "Flow matching models (Stable Diffusion 3, Flux) use straight-line trajectories instead of the curved paths of standard diffusion. Explain why this leads to faster and more stable training. What mathematical framework underpins this approach?"),
            ("ADVANCED", "Design", "Design a content moderation pipeline for a text-to-image generation service. Address input filtering (blocking harmful prompts), output filtering (detecting generated harmful content), watermarking, and audit logging."),
            ("RESEARCH", "Open-ended", "Consistency models (Song et al., 2023) enable single-step generation from diffusion models. Analyze the quality/speed trade-off compared to multi-step diffusion. Under what conditions would you choose one over the other for a production application?"),
        ]
    },
    "module-24-multimodal/section-24.2.html": {
        "title": "Exercises: Audio, Video & Beyond",
        "exercises": [
            ("BASIC", "Conceptual", "Explain the difference between text-to-speech (TTS) and voice cloning. What are the ethical implications of voice cloning technology?"),
            ("BASIC", "Conceptual", "What makes video generation significantly harder than image generation? Identify three specific challenges unique to video."),
            ("INTERMEDIATE", "Coding", "Use a text-to-speech API (e.g., OpenAI TTS, ElevenLabs) to generate speech samples with different voice parameters. Compare naturalness, prosody, and latency across at least two providers."),
            ("INTERMEDIATE", "Coding", "Generate a short video clip using a text-to-video model (e.g., via an API or a local model like CogVideoX). Analyze the temporal coherence: do objects maintain consistent appearance across frames?"),
            ("INTERMEDIATE", "Conceptual", "Compare the architectures of Sora (diffusion transformer for video), Kling (autoregressive video), and Stable Video Diffusion. What are the trade-offs in quality, speed, and controllability?"),
            ("ADVANCED", "Coding", "Build a voice pipeline that takes text input, generates speech, then transcribes it back using Whisper. Measure the round-trip accuracy (word error rate). Identify which types of content (numbers, names, technical terms) have the highest error rates."),
            ("ADVANCED", "Design", "Design a real-time voice agent that handles speech-to-text, LLM reasoning, and text-to-speech with sub-second latency. Identify the bottleneck at each stage and propose optimizations."),
            ("ADVANCED", "Conceptual", "Music generation models (e.g., Suno, Udio) raise complex copyright questions. Analyze the legal and ethical landscape: how do these models differ from image generation models in terms of training data sourcing and output ownership?"),
            ("RESEARCH", "Open-ended", "World models that generate interactive environments from text descriptions (e.g., for games or simulations) are an active research area. Propose an architecture that combines video generation with physics simulation for creating interactive 3D environments."),
        ]
    },
    "module-24-multimodal/section-24.3.html": {
        "title": "Exercises: Document Understanding & OCR",
        "exercises": [
            ("BASIC", "Conceptual", "Explain the difference between OCR, layout analysis, and document understanding. Why is OCR alone insufficient for extracting structured data from documents?"),
            ("BASIC", "Conceptual", "What is the advantage of vision-language models (VLMs) like GPT-4o over traditional OCR pipelines for document processing? What are the disadvantages?"),
            ("INTERMEDIATE", "Coding", "Build a document extraction pipeline that takes a scanned invoice image, extracts key fields (vendor, date, total, line items), and outputs structured JSON. Compare the accuracy of: (a) Tesseract + regex, (b) a VLM zero-shot approach."),
            ("INTERMEDIATE", "Coding", "Use LayoutLMv3 or a similar layout-aware model to classify document regions (header, table, paragraph, footer) on a set of 10 diverse documents. Measure classification accuracy."),
            ("INTERMEDIATE", "Conceptual", "ColPali and ColQwen enable vision-based document retrieval without OCR. Explain how late-interaction multi-vector retrieval works on document page images. What types of queries does this approach handle better than text-based retrieval?"),
            ("ADVANCED", "Coding", "Build a table extraction system that handles complex tables (merged cells, multi-line headers, nested tables). Test it on 5 real-world financial tables and measure cell-level accuracy."),
            ("ADVANCED", "Design", "Design a document processing pipeline for a legal firm that must handle contracts, court filings, and correspondence in multiple languages. Address OCR quality for low-resolution scans, confidentiality requirements, and integration with the firm's document management system."),
            ("ADVANCED", "Conceptual", "Compare the cost-per-document and accuracy trade-offs of three approaches at scale: (1) traditional OCR + NLP pipeline, (2) fine-tuned LayoutLMv3, (3) GPT-4o vision. At what document volume does each approach become cost-effective?"),
            ("RESEARCH", "Open-ended", "End-to-end document understanding without OCR is a growing trend. Analyze the limitations of current vision-only approaches (e.g., Nougat for scientific papers, Donut for receipts). What types of documents still require traditional OCR pipelines?"),
        ]
    },
    "module-24-multimodal/section-24.4.html": {
        "title": "Exercises: Unified Multimodal Models",
        "exercises": [
            ("BASIC", "Conceptual", "Explain the difference between a pipeline multimodal system and a native multimodal model. Give an example of information loss that occurs in the pipeline approach but not in the native approach."),
            ("BASIC", "Conceptual", "What is early fusion versus late fusion in multimodal models? Draw a simple diagram showing where modality-specific encoders and shared layers are positioned in each approach."),
            ("INTERMEDIATE", "Coding", "Use a vision-language model (GPT-4o, Claude, or Gemini) to analyze a set of 10 images. Test three types of queries: visual question answering, detailed description, and reasoning about spatial relationships. Rate the model's accuracy on each type."),
            ("INTERMEDIATE", "Coding", "Build a multimodal RAG pipeline that indexes both text and images from a product catalog, then answers user questions that require understanding both modalities (e.g., 'Show me red dresses similar to this one but with longer sleeves')."),
            ("INTERMEDIATE", "Conceptual", "Compare the multimodal capabilities of GPT-4o, Gemini 2.5, and Claude Sonnet across four tasks: image understanding, audio transcription, video analysis, and interleaved text-image generation. Which model excels at which task, and why?"),
            ("ADVANCED", "Coding", "Evaluate a VLM on the MMMU benchmark (or a subset). Analyze which subject areas (science, humanities, engineering) the model performs best and worst on. Propose hypotheses for the performance differences."),
            ("ADVANCED", "Design", "Design a multimodal assistant for a manufacturing quality control line that receives camera images, sensor readings (temperature, vibration), and operator notes. The system must detect defects, correlate them with sensor anomalies, and generate reports. Address latency requirements and fallback behavior when the camera feed is degraded."),
            ("ADVANCED", "Conceptual", "Shared embedding spaces (where text, images, and audio map to the same vector space) are foundational to unified multimodal models. What are the alignment challenges, and how do models like CLIP and SigLIP address them? What happens when modalities have very different information density?"),
            ("RESEARCH", "Open-ended", "Any-to-any multimodal generation (text to image, image to audio, video to text, etc.) is the goal of unified models. Analyze the current state of the art and identify the two hardest modality conversions. What architectural innovations are needed to solve them?"),
        ]
    },
    # Module 25: LLM Applications
    "module-25-llm-applications/section-25.1.html": {
        "title": "Exercises: Code Generation & Developer Tools",
        "exercises": [
            ("BASIC", "Conceptual", "Explain the difference between code completion (e.g., Copilot autocomplete) and code generation (e.g., generating a full function from a docstring). Which is easier for LLMs, and why?"),
            ("BASIC", "Conceptual", "List three ways that LLM-powered code tools can improve developer productivity and three ways they can introduce risk. How should teams balance these trade-offs?"),
            ("INTERMEDIATE", "Coding", "Use an LLM API to build a simple code review tool: given a Python function, the tool should identify potential bugs, suggest improvements, and rate code quality on a 1-5 scale. Test it on 5 functions with known issues."),
            ("INTERMEDIATE", "Coding", "Implement a test generation tool that takes a Python function and automatically generates pytest test cases. Measure the coverage of the generated tests on a set of 10 functions."),
            ("INTERMEDIATE", "Conceptual", "Compare the approaches of GitHub Copilot, Cursor, and Aider for AI-assisted coding. What architectural decisions (context window usage, RAG over codebase, agent loops) differentiate them?"),
            ("ADVANCED", "Coding", "Build a documentation generator that reads a Python module, generates docstrings for all functions and classes, and produces a summary README. Evaluate the accuracy by comparing against hand-written documentation for an open-source project."),
            ("ADVANCED", "Design", "Design an LLM-powered code migration tool that converts a Python 2 codebase to Python 3. Address: handling of unicode strings, print statements, dictionary methods, and import changes. How would you validate the migration?"),
            ("ADVANCED", "Conceptual", "Evaluate the claim that LLM code generation makes junior developers less necessary. Present evidence for and against, considering code quality, debugging skills, and system design capabilities that LLMs currently lack."),
            ("RESEARCH", "Open-ended", "Formal verification of LLM-generated code is an open problem. Propose a workflow where the LLM generates both the code and a formal specification, then a theorem prover verifies correctness. What classes of programs can this approach handle today?"),
        ]
    },
    "module-25-llm-applications/section-25.2.html": {
        "title": "Exercises: Finance & Legal Applications",
        "exercises": [
            ("BASIC", "Conceptual", "Why do financial applications of LLMs require higher accuracy and explainability than general-purpose chatbots? Give three specific consequences of an LLM error in a financial context."),
            ("BASIC", "Conceptual", "What is sentiment analysis in the context of financial text? How does financial sentiment differ from general sentiment (e.g., product reviews)?"),
            ("INTERMEDIATE", "Coding", "Build a financial sentiment analyzer that classifies earnings call sentences as positive, negative, or neutral. Compare the accuracy of: (a) a zero-shot LLM approach, (b) a fine-tuned FinBERT model. Use the Financial PhraseBank dataset."),
            ("INTERMEDIATE", "Coding", "Create an SEC filing summarizer that takes a 10-K filing and extracts the key risk factors, financial highlights, and management outlook. Evaluate on 3 real filings by comparing to analyst summaries."),
            ("INTERMEDIATE", "Conceptual", "Regulatory compliance (e.g., MiFID II, SEC regulations) constrains how LLMs can be used in finance. Identify three specific regulatory requirements and explain how they affect the design of financial LLM applications."),
            ("ADVANCED", "Coding", "Build a contract analysis tool that extracts key clauses (indemnification, termination, liability caps) from legal contracts. Test on 5 sample contracts and measure extraction accuracy at the clause level."),
            ("ADVANCED", "Design", "Design a compliance monitoring system that uses LLMs to scan internal communications for potential regulatory violations. Address false positive rates, privacy concerns, and the explainability requirements for flagged items."),
            ("ADVANCED", "Conceptual", "Hallucination in financial and legal contexts can have severe consequences. Compare three hallucination mitigation strategies (RAG grounding, citation requirements, dual-model verification) and assess which is most appropriate for: (a) investment research, (b) contract drafting, (c) regulatory reporting."),
            ("RESEARCH", "Open-ended", "BloombergGPT demonstrated that domain-specific pretraining improves performance on financial tasks. Analyze whether domain-specific fine-tuning on open-weight models (Llama, Mistral) can achieve similar results at lower cost. Design an experiment to test this hypothesis."),
        ]
    },
    "module-25-llm-applications/section-25.3.html": {
        "title": "Exercises: Healthcare & Biomedical Applications",
        "exercises": [
            ("BASIC", "Conceptual", "Why is the stakes/accuracy trade-off especially critical in healthcare LLM applications? Give three specific scenarios where an LLM error could cause patient harm."),
            ("BASIC", "Conceptual", "Explain the concept of a 'human-in-the-loop' in healthcare AI. At what points in a clinical workflow should human review be mandatory?"),
            ("INTERMEDIATE", "Coding", "Build a medical literature search tool that takes a clinical question, retrieves relevant PubMed abstracts, and generates a summary with citations. Evaluate the factual accuracy of summaries for 5 clinical questions."),
            ("INTERMEDIATE", "Conceptual", "Compare the regulatory pathways for LLM-based medical devices in the US (FDA), EU (CE marking), and UK (MHRA). What are the key differences in requirements for clinical validation?"),
            ("INTERMEDIATE", "Design", "Design a clinical note summarization tool that extracts key findings, diagnoses, and treatment plans from physician notes. Address: handling of abbreviations, maintaining medical accuracy, and flagging uncertain extractions."),
            ("ADVANCED", "Coding", "Implement a drug interaction checker that uses an LLM to analyze a patient's medication list against a drug interaction database. Compare the accuracy to a rule-based system on 20 test cases."),
            ("ADVANCED", "Conceptual", "De-identification of protected health information (PHI) is required before using clinical text with LLMs. Analyze the limitations of current de-identification methods and the risks of residual PHI in training data."),
            ("ADVANCED", "Design", "Design an LLM-powered clinical decision support system for emergency departments. Address triage accuracy, integration with electronic health records, liability considerations, and how to handle cases where the LLM disagrees with the physician."),
            ("RESEARCH", "Open-ended", "Med-PaLM 2 achieved expert-level performance on medical licensing exams. Critically analyze whether exam performance translates to clinical utility. What additional evaluations are needed before deploying medical LLMs in patient care?"),
        ]
    },
    "module-25-llm-applications/section-25.4.html": {
        "title": "Exercises: Search, Recommendation & Analytics",
        "exercises": [
            ("BASIC", "Conceptual", "Explain how LLM-powered search (e.g., Perplexity) differs from traditional keyword-based search. What are the advantages and disadvantages for users?"),
            ("BASIC", "Conceptual", "What is natural language to SQL (NL-to-SQL)? Why is schema linking the hardest part of the pipeline?"),
            ("INTERMEDIATE", "Coding", "Build a simple NL-to-SQL system: given a database schema and a natural language question, generate the SQL query. Test on the WikiSQL or Spider benchmark subset. Measure execution accuracy."),
            ("INTERMEDIATE", "Coding", "Create a recommendation system that takes a user's natural language description of their preferences and returns personalized recommendations from a product database. Compare to a traditional collaborative filtering approach."),
            ("INTERMEDIATE", "Conceptual", "LLM-powered search must handle attribution (citing sources). Compare the citation approaches of Perplexity, Google AI Overviews, and Bing Chat. Which approach provides the most trustworthy citations, and why?"),
            ("ADVANCED", "Coding", "Implement a conversational analytics agent that maintains session state: the user asks follow-up questions that reference previous queries (e.g., 'Now break that down by region' after asking about total sales). Handle context resolution across at least 3 turns."),
            ("ADVANCED", "Design", "Design an analytics copilot for a business intelligence platform. The system should generate SQL, create visualizations, and answer natural language questions about dashboards. Address the semantic layer problem: how do you map business terms to database columns?"),
            ("ADVANCED", "Conceptual", "LLM-generated SQL can be syntactically valid but semantically wrong (answering the wrong question). Propose a three-stage validation pipeline that catches semantic errors before results reach the user."),
            ("RESEARCH", "Open-ended", "Conversational search (multi-turn question answering over web results) is an active research area. Analyze the limitations of current approaches and propose an architecture that maintains a knowledge graph of the conversation to resolve ambiguous follow-up queries."),
        ]
    },
    "module-25-llm-applications/section-25.5.html": {
        "title": "Exercises: Scientific Research & Discovery",
        "exercises": [
            ("BASIC", "Conceptual", "How are LLMs being used to accelerate scientific research? List three specific applications and explain the value they provide over traditional methods."),
            ("BASIC", "Conceptual", "What are the risks of using LLMs for scientific literature review? How can researchers mitigate the risk of hallucinated citations?"),
            ("INTERMEDIATE", "Coding", "Build a research paper summarizer that takes a PDF, extracts the key contributions, methods, and results, and generates a structured summary. Test on 5 papers from arXiv and evaluate accuracy."),
            ("INTERMEDIATE", "Conceptual", "Compare the approaches of tools like Elicit, Semantic Scholar, and Consensus for AI-assisted literature review. What are the strengths and weaknesses of each?"),
            ("INTERMEDIATE", "Design", "Design a hypothesis generation tool for drug discovery that takes a disease description and a set of known drug targets, then proposes novel therapeutic hypotheses. How would you validate the generated hypotheses?"),
            ("ADVANCED", "Coding", "Implement a citation verification system that checks whether citations in an LLM-generated literature review actually exist and accurately represent the cited work. Use Semantic Scholar API or CrossRef."),
            ("ADVANCED", "Conceptual", "LLMs for protein structure prediction (AlphaFold) and molecular design represent a different paradigm from text-based LLMs. Compare the training approaches and explain why language model architectures work for biological sequences."),
            ("ADVANCED", "Design", "Design an AI research assistant for a materials science lab that can: search literature, propose experiments, analyze results, and update the lab's knowledge base. Address how to prevent the assistant from suggesting experiments that violate safety protocols."),
            ("RESEARCH", "Open-ended", "The use of LLMs as 'AI scientists' (e.g., generating and testing hypotheses autonomously) raises questions about scientific integrity and reproducibility. Propose a framework for attributing and validating AI-generated scientific contributions."),
        ]
    },
    "module-25-llm-applications/section-25.6.html": {
        "title": "Exercises: Education, Creative & Customer Service",
        "exercises": [
            ("BASIC", "Conceptual", "How can AI tutors provide personalized instruction at scale? What are three advantages over traditional one-size-fits-all teaching materials?"),
            ("BASIC", "Conceptual", "Describe three ways LLMs are being used in customer support. For each, explain when the LLM should escalate to a human agent."),
            ("INTERMEDIATE", "Coding", "Build a Socratic tutoring agent that asks guiding questions rather than giving direct answers. Test it on a math topic (e.g., solving quadratic equations). Evaluate whether the agent actually helps the student arrive at the answer independently."),
            ("INTERMEDIATE", "Coding", "Create a creative writing assistant that helps a user develop a short story. The assistant should offer plot suggestions, character development ideas, and stylistic feedback. Evaluate the quality of assistance across 3 writing sessions."),
            ("INTERMEDIATE", "Conceptual", "Compare the educational AI approaches of Khan Academy (Khanmigo), Duolingo, and Quizlet. How does each use LLMs differently, and what pedagogical principles guide their design?"),
            ("ADVANCED", "Coding", "Build a customer support agent that handles multi-turn conversations, accesses a product knowledge base via RAG, and knows when to escalate. Measure the resolution rate on 20 simulated support tickets of varying complexity."),
            ("ADVANCED", "Design", "Design an AI-powered legal research assistant for a law firm. It should search case law, identify relevant precedents, summarize findings, and flag potential conflicts. Address the critical requirement of accuracy and the consequences of hallucinated case citations."),
            ("ADVANCED", "Conceptual", "LLMs as creative writing tools raise questions about authorship and originality. Analyze the spectrum from AI as a brainstorming tool to AI as a ghostwriter. Where should the line be drawn, and how should AI contributions be disclosed?"),
            ("RESEARCH", "Open-ended", "Adaptive learning systems that personalize content based on student performance predate LLMs. Analyze how LLM-based tutors improve upon earlier adaptive learning systems. What new capabilities do they enable, and what old problems remain unsolved?"),
        ]
    },
    "module-25-llm-applications/section-25.7.html": {
        "title": "Exercises: Robotics, Embodied AI & VLAs",
        "exercises": [
            ("BASIC", "Conceptual", "What is a Vision-Language-Action (VLA) model? Explain how it differs from a traditional robot control pipeline that uses separate perception, planning, and control modules."),
            ("BASIC", "Conceptual", "Why is grounding (connecting language to physical actions in the real world) one of the hardest problems in embodied AI? Give three specific challenges."),
            ("INTERMEDIATE", "Coding", "Use an LLM to generate a task plan for a simulated robot: given a scene description and a goal (e.g., 'Set the table for dinner'), produce a step-by-step action plan. Evaluate the plan's feasibility and completeness."),
            ("INTERMEDIATE", "Conceptual", "Compare the approaches of RT-2, PaLM-E, and OpenVLA for vision-language-action models. What are the key architectural differences, and how do they handle the gap between language understanding and physical action?"),
            ("INTERMEDIATE", "Design", "Design a natural language interface for a warehouse robot. The interface should translate operator commands (e.g., 'Move all boxes from aisle 3 to the shipping dock') into robot actions. Address safety constraints and confirmation protocols."),
            ("ADVANCED", "Coding", "Implement a sim-to-real pipeline: train a simple VLA-style model in simulation (e.g., using Isaac Gym or PyBullet), then analyze the domain gap challenges when transferring to real hardware. Document the key failure modes."),
            ("ADVANCED", "Conceptual", "Scaling laws for robot learning differ from scaling laws for language models. Analyze why collecting robot training data is fundamentally harder than collecting text data, and evaluate current approaches to this data bottleneck (simulation, teleoperation, self-play)."),
            ("ADVANCED", "Design", "Design a safety framework for an LLM-controlled robot in a household setting. Address: physical safety constraints (do not apply excessive force), environmental awareness (detect and avoid fragile objects), and user intent verification for high-risk actions (using a knife, operating appliances)."),
            ("RESEARCH", "Open-ended", "The Open X-Embodiment dataset pools robot data across multiple labs and robot platforms. Analyze whether 'foundation models for robotics' face the same or different scaling challenges as language foundation models. What is the equivalent of 'internet-scale text data' for robotics?"),
        ]
    },
    # Module 26: Evaluation & Observability
    "module-26-evaluation-observability/section-26.1.html": {
        "title": "Exercises: Evaluation Foundations & Metrics",
        "exercises": [
            ("BASIC", "Conceptual", "Explain the difference between reference-based metrics (BLEU, ROUGE) and reference-free metrics (LLM-as-judge). When would you prefer each?"),
            ("BASIC", "Conceptual", "Why is evaluating LLM outputs fundamentally harder than evaluating traditional ML model outputs (e.g., classification accuracy)? Give three specific reasons."),
            ("INTERMEDIATE", "Coding", "Implement a multi-metric evaluation pipeline that scores LLM outputs using BLEU, ROUGE-L, and BERTScore. Test it on 20 question-answer pairs and analyze which metric correlates best with human judgments."),
            ("INTERMEDIATE", "Coding", "Build an LLM-as-judge evaluator that rates the quality of LLM responses on a 1-5 scale across three dimensions: accuracy, completeness, and clarity. Measure inter-rater agreement between the LLM judge and human ratings on 10 examples."),
            ("INTERMEDIATE", "Conceptual", "Explain the difference between pointwise, pairwise, and listwise LLM evaluation. For each approach, describe a scenario where it is the best choice."),
            ("ADVANCED", "Coding", "Implement a bias detection experiment for LLM-as-judge: test whether the judge shows position bias (preferring the first or last response), verbosity bias (preferring longer responses), or self-enhancement bias (preferring its own outputs). Use at least 50 evaluation pairs."),
            ("ADVANCED", "Design", "Design an evaluation framework for a customer-facing LLM chatbot. Define the metrics you would track, the evaluation cadence, the golden dataset creation process, and how you would detect quality degradation over time."),
            ("ADVANCED", "Conceptual", "Human evaluation is the gold standard for LLM quality, but it is expensive and slow. Propose a calibration strategy that uses a small set of human evaluations to validate and adjust automated metrics, reducing the need for ongoing human evaluation."),
            ("RESEARCH", "Open-ended", "Arena-style evaluation (e.g., Chatbot Arena) uses crowd-sourced pairwise comparisons. Analyze the statistical properties of this approach: how many comparisons are needed for reliable rankings, what biases exist in crowd evaluations, and how can adversarial manipulation be detected?"),
        ]
    },
    "module-26-evaluation-observability/section-26.2.html": {
        "title": "Exercises: Benchmarks & Leaderboards",
        "exercises": [
            ("BASIC", "Conceptual", "List five major LLM benchmarks and explain what each measures. Which benchmarks are most relevant for production deployment decisions?"),
            ("BASIC", "Conceptual", "What is benchmark contamination, and why is it a serious problem for LLM evaluation? How can benchmark creators mitigate this risk?"),
            ("INTERMEDIATE", "Coding", "Run a small-scale evaluation of two open-weight models on a subset of MMLU (10 questions per category, 5 categories). Compare their performance and analyze which categories each model excels at."),
            ("INTERMEDIATE", "Coding", "Create a custom domain-specific benchmark for a use case of your choice (e.g., customer support, code review, medical triage). Include at least 50 test cases with ground truth labels and a scoring rubric."),
            ("INTERMEDIATE", "Conceptual", "Compare the evaluation approaches of the Open LLM Leaderboard, LMSYS Chatbot Arena, and SEAL Leaderboards. What are the strengths and weaknesses of automated benchmarks versus human preference evaluations?"),
            ("ADVANCED", "Coding", "Implement a benchmark contamination detector: given a benchmark dataset and an LLM, design prompts that test whether the model has memorized the test questions. Use techniques like paraphrasing and answer order shuffling."),
            ("ADVANCED", "Design", "Design a living benchmark that evolves over time to resist contamination. Address: how new questions are generated, how difficulty is calibrated, how historical comparability is maintained, and how contributors are incentivized."),
            ("ADVANCED", "Conceptual", "Benchmark saturation (models approaching perfect scores) is a growing problem. Analyze three benchmarks that are nearly saturated and propose harder evaluation tasks that would differentiate current frontier models."),
            ("RESEARCH", "Open-ended", "Current benchmarks primarily evaluate English language capabilities. Propose a multilingual evaluation framework that fairly assesses LLM performance across 10+ languages while accounting for cultural context and resource availability differences."),
        ]
    },
    "module-26-evaluation-observability/section-26.3.html": {
        "title": "Exercises: RAG & Agent Evaluation",
        "exercises": [
            ("BASIC", "Conceptual", "What are the four RAGAS metrics (faithfulness, answer relevancy, context precision, context recall)? Explain each in one sentence and describe what a low score indicates."),
            ("BASIC", "Conceptual", "Why must agent evaluation consider the trajectory (sequence of actions) and not just the final answer? Give an example where the answer is correct but the trajectory is problematic."),
            ("INTERMEDIATE", "Coding", "Build a RAG evaluation pipeline using the Ragas library. Evaluate a simple RAG system on 20 questions, measuring all four RAGAS metrics. Identify the weakest metric and propose improvements."),
            ("INTERMEDIATE", "Coding", "Implement an agent trajectory evaluator that logs each tool call, its input, and its output, then scores the trajectory on efficiency (number of unnecessary steps), correctness (did each step contribute to the answer?), and safety (were there any risky actions?)."),
            ("INTERMEDIATE", "Conceptual", "Compare the evaluation approaches of three RAG evaluation frameworks: Ragas, DeepEval, and Phoenix. What metrics does each provide, and how do they differ in their approach to ground truth requirements?"),
            ("ADVANCED", "Coding", "Create an adversarial test suite for a RAG system: design queries that exploit known failure modes (conflicting sources, out-of-scope questions, temporal ambiguity). Measure the system's failure rate and characterize the failure modes."),
            ("ADVANCED", "Design", "Design an evaluation pipeline for a multi-agent system that includes both RAG components and tool-calling agents. Define metrics at three levels: individual agent performance, inter-agent communication quality, and end-to-end task completion."),
            ("ADVANCED", "Conceptual", "Agent evaluation faces the partial observability problem: you can see the agent's actions but not its internal reasoning (unless it uses chain-of-thought). Discuss how this affects evaluation reliability and propose techniques to improve observability."),
            ("RESEARCH", "Open-ended", "Current RAG evaluation metrics assume a single correct answer. Propose evaluation metrics for RAG systems that must handle ambiguous or controversial topics where multiple valid perspectives exist."),
        ]
    },
    "module-26-evaluation-observability/section-26.4.html": {
        "title": "Exercises: Observability & Tracing",
        "exercises": [
            ("BASIC", "Conceptual", "Explain the difference between logging, monitoring, and tracing in LLM systems. Why is each important?"),
            ("BASIC", "Conceptual", "What is a trace in the context of LLM observability? What information should a trace capture for a single LLM request?"),
            ("INTERMEDIATE", "Coding", "Instrument an LLM application with tracing using an observability library (e.g., OpenTelemetry, Langfuse, or Phoenix). Capture traces for 20 requests and build a dashboard showing latency distribution, token usage, and error rates."),
            ("INTERMEDIATE", "Coding", "Build a cost monitoring system that tracks per-request costs across different LLM providers. Generate a weekly cost report broken down by model, feature, and user segment."),
            ("INTERMEDIATE", "Conceptual", "Compare three LLM observability platforms: Langfuse, LangSmith, and Arize Phoenix. What are the key differences in their tracing, evaluation, and debugging capabilities?"),
            ("ADVANCED", "Coding", "Implement an anomaly detection system for LLM responses: flag responses that are unusually long, unusually short, contain specific keywords indicating confusion, or have abnormal latency. Test on a dataset of 100 requests with 10 planted anomalies."),
            ("ADVANCED", "Design", "Design an observability architecture for a production LLM system that handles 10,000 requests per day. Address: sampling strategy (you cannot trace every request), alert thresholds, root cause analysis workflow, and storage cost optimization."),
            ("ADVANCED", "Conceptual", "Privacy constraints limit what can be logged in LLM observability systems. Design a logging strategy that enables debugging and quality monitoring while complying with GDPR (no personal data in logs without consent). Address PII detection and redaction in prompts and responses."),
            ("RESEARCH", "Open-ended", "Causal tracing (understanding which parts of a prompt influenced which parts of the response) is an open research problem. Propose an approach that combines attention analysis with perturbation-based methods to provide causal explanations for LLM outputs."),
        ]
    },
    "module-26-evaluation-observability/section-26.5.html": {
        "title": "Exercises: A/B Testing & Experimentation",
        "exercises": [
            ("BASIC", "Conceptual", "Why is A/B testing LLM features harder than A/B testing traditional software features? List three specific challenges."),
            ("BASIC", "Conceptual", "Explain what statistical significance means in the context of an LLM A/B test. Why do LLM experiments often need larger sample sizes than traditional web experiments?"),
            ("INTERMEDIATE", "Coding", "Design and implement a simple A/B testing framework for LLM prompts. Test two prompt variants on 100 user queries, collect LLM-as-judge scores for each, and compute whether the difference is statistically significant."),
            ("INTERMEDIATE", "Conceptual", "Interleaving (mixing results from two systems in a single response) is an alternative to A/B testing. Explain how interleaving works for search systems and discuss whether it can be adapted for LLM chatbot evaluation."),
            ("INTERMEDIATE", "Design", "Design an A/B test plan for switching from GPT-4o to Claude Sonnet as the backbone model for a customer support chatbot. Define the metrics, sample size calculation, duration, and guardrail metrics that would trigger an automatic rollback."),
            ("ADVANCED", "Coding", "Implement a multi-armed bandit approach for prompt selection: given 4 prompt variants, use Thompson sampling to dynamically allocate traffic to the best-performing variant. Compare the cumulative regret to a standard A/B test over 1,000 simulated queries."),
            ("ADVANCED", "Conceptual", "LLM responses are non-deterministic even with the same prompt. Analyze how this non-determinism affects A/B test power calculations. How many more samples do you need compared to a deterministic system?"),
            ("ADVANCED", "Design", "Design a continuous experimentation platform for an LLM product team that runs multiple overlapping experiments. Address: experiment interaction effects, metric correlations, and how to prioritize conflicting experiment results."),
            ("RESEARCH", "Open-ended", "Offline evaluation (using logged data) is cheaper than online A/B testing. Propose a framework for estimating online A/B test results from offline evaluation data using techniques from causal inference (e.g., inverse propensity scoring)."),
        ]
    },
    "module-26-evaluation-observability/section-26.6.html": {
        "title": "Exercises: Drift Detection & Monitoring",
        "exercises": [
            ("BASIC", "Conceptual", "Define three types of drift relevant to LLM systems: data drift, model drift, and concept drift. Give a concrete example of each in a production chatbot."),
            ("BASIC", "Conceptual", "Why can LLM performance degrade over time even without any code changes? List three causes."),
            ("INTERMEDIATE", "Coding", "Build a drift detection monitor that tracks the distribution of LLM output characteristics (response length, sentiment score, topic distribution) over time. Generate synthetic data with a planted drift at day 30 and verify your monitor detects it."),
            ("INTERMEDIATE", "Coding", "Implement embedding drift detection: compare the embedding distributions of queries from two time periods using cosine similarity statistics and a statistical test (e.g., MMD or KS test). Visualize the drift using t-SNE plots."),
            ("INTERMEDIATE", "Conceptual", "When an LLM provider updates their model (e.g., GPT-4o gets a minor update), your application's behavior can change without warning. Design a continuous regression testing strategy that detects these 'silent updates' within 24 hours."),
            ("ADVANCED", "Coding", "Build an alerting system that monitors LLM quality metrics in real-time and triggers alerts when metrics cross thresholds. Implement three alert types: absolute threshold (quality drops below X), relative threshold (quality drops by Y% from baseline), and trend alert (quality declining for Z consecutive days)."),
            ("ADVANCED", "Design", "Design a model rollback strategy for an LLM application that uses a third-party API. You cannot roll back the provider's model, so what alternatives do you have? Address prompt version pinning, output post-processing, and graceful degradation."),
            ("ADVANCED", "Conceptual", "Embedding drift in RAG systems is particularly dangerous because it can cause silent retrieval failures. Explain the mechanism by which updating an embedding model breaks existing vector stores, and propose a migration strategy that avoids downtime."),
            ("RESEARCH", "Open-ended", "Propose a unified drift detection framework that monitors all components of an LLM pipeline simultaneously (input distribution, retrieval quality, generation quality, user satisfaction). How should alerts from different components be correlated and prioritized?"),
        ]
    },
    "module-26-evaluation-observability/section-26.7.html": {
        "title": "Exercises: Red Teaming & Safety Evaluation",
        "exercises": [
            ("BASIC", "Conceptual", "What is red teaming in the context of LLM safety? How does it differ from traditional security penetration testing?"),
            ("BASIC", "Conceptual", "List three categories of LLM vulnerabilities that red teaming can uncover. For each, give a specific example attack and its potential impact."),
            ("INTERMEDIATE", "Coding", "Implement a simple automated red teaming pipeline: generate adversarial prompts using template-based attacks (e.g., role-playing, encoded instructions, multi-turn jailbreaks) and test whether the target model complies. Measure the attack success rate."),
            ("INTERMEDIATE", "Coding", "Build a toxicity monitoring system that scans LLM outputs for harmful content using a classifier (e.g., Perspective API or a local model). Test it on 50 outputs, including 10 edge cases that are subtly problematic."),
            ("INTERMEDIATE", "Conceptual", "Compare manual red teaming by human experts with automated red teaming using adversarial LLMs. What are the strengths and weaknesses of each approach? Can they be combined effectively?"),
            ("ADVANCED", "Coding", "Implement a multi-turn jailbreak attack: design a conversation sequence where early turns build context that makes the final adversarial prompt more likely to succeed. Test against two different models and compare their robustness."),
            ("ADVANCED", "Design", "Design a red teaming program for a healthcare AI product. Define the team composition, attack categories (medical misinformation, privacy violations, bias in treatment recommendations), evaluation criteria, and remediation workflow."),
            ("ADVANCED", "Conceptual", "Responsible disclosure of LLM vulnerabilities is a developing area. Compare the approaches of OpenAI, Anthropic, and Google to vulnerability reporting and patching. What standards should the industry adopt?"),
            ("RESEARCH", "Open-ended", "Adversarial robustness in LLMs is an arms race: defenses are developed, then bypassed by new attacks. Propose a defense strategy that is robust to a broader class of attacks rather than patching individual vulnerabilities. Consider constitutional AI, input/output classifiers, and formal verification."),
        ]
    },
    "module-26-evaluation-observability/section-26.8.html": {
        "title": "Exercises: Building an Evaluation Culture",
        "exercises": [
            ("BASIC", "Conceptual", "Why is 'vibes-based evaluation' (testing by feel) insufficient for production LLM systems? Give three specific scenarios where informal testing misses critical issues."),
            ("BASIC", "Conceptual", "Describe the three components of a minimum viable evaluation system for any LLM application. What is the smallest investment that provides meaningful quality assurance?"),
            ("INTERMEDIATE", "Coding", "Build an automated evaluation pipeline that runs nightly on a golden dataset: scores LLM outputs on three metrics, compares to the previous run, and sends an alert if any metric degrades by more than 5%. Use any CI/CD tool."),
            ("INTERMEDIATE", "Coding", "Create a golden dataset of 100 examples for a specific LLM application (e.g., customer support, code review). Include diverse test cases covering common scenarios, edge cases, and adversarial inputs. Document the creation process and labeling guidelines."),
            ("INTERMEDIATE", "Design", "Design an evaluation workflow for a team of 5 engineers shipping weekly LLM feature updates. Address: who creates test cases, how evaluation results block or approve releases, and how the golden dataset grows over time."),
            ("ADVANCED", "Coding", "Implement a regression testing system that catches prompt regressions: when a developer changes a prompt template, automatically test it against the golden dataset and compare to the baseline. Block the deployment if quality drops."),
            ("ADVANCED", "Design", "Design an evaluation maturity model with 5 levels (from ad hoc testing to continuous automated evaluation with drift detection). For each level, specify the tools, processes, and team capabilities required."),
            ("ADVANCED", "Conceptual", "Evaluation costs (LLM-as-judge API calls, human annotation, compute for running benchmarks) can become a significant expense. Propose a cost-optimization strategy that maintains evaluation quality while reducing spend by at least 50%."),
            ("RESEARCH", "Open-ended", "The evaluation gap (the difference between what benchmarks measure and what users actually care about) is a fundamental problem. Propose a framework for closing this gap that combines automated metrics, user feedback, and domain expert review in a unified scoring system."),
        ]
    },
}


def generate_exercises_html(section_key, data):
    """Generate the exercises HTML block for a section."""
    exercises = data["exercises"]
    title = data["title"]

    lines = []
    lines.append('')
    lines.append(f'    <h2>{title}</h2>')
    lines.append('')
    lines.append('    <div style="background: linear-gradient(135deg, #ffeaa7, #fdcb6e); border-radius: 10px; padding: 1rem 1.5rem; margin-bottom: 1.5rem;">')
    lines.append('        <p style="margin: 0; font-family: \'Segoe UI\', sans-serif; font-size: 0.9rem;"><strong>How to use these exercises:</strong>')
    lines.append('        Conceptual questions test your understanding of the <em>why</em> behind each technique.')
    lines.append('        Coding exercises are hands-on challenges you should run in a Jupyter notebook or local environment.')
    lines.append('        Design exercises ask you to architect solutions for realistic scenarios.</p>')
    lines.append('    </div>')
    lines.append('')

    # Group by level
    levels = {"BASIC": [], "INTERMEDIATE": [], "ADVANCED": [], "RESEARCH": []}
    for i, (level, etype, text) in enumerate(exercises, 1):
        levels[level].append((i, etype, text))

    lines.append('    <ol>')
    for i, (level, etype, text) in enumerate(exercises, 1):
        badge = level.lower()
        lines.append(f'        <li><span class="level-badge {badge}">{level}</span> <strong>[{etype}]</strong> {text}</li>')
        if i < len(exercises):
            lines.append('')
    lines.append('    </ol>')
    lines.append('')

    # Add answer sketches for basic/intermediate conceptual
    lines.append('    <details style="margin-top: 1rem; margin-bottom: 2rem;">')
    lines.append('        <summary style="cursor: pointer; font-weight: bold; color: var(--accent, #0f3460);">Answer Sketches (selected exercises)</summary>')
    lines.append('        <div style="padding: 1rem; background: var(--card-bg, #f8f9fa); border-radius: 8px; margin-top: 0.5rem;">')

    # Add sketch for first basic exercise
    basic_ex = levels["BASIC"]
    if basic_ex:
        num, etype, text = basic_ex[0]
        lines.append(f'            <p><strong>Exercise {num}:</strong> Review the key definitions and distinctions from this section. A strong answer identifies the core concept, provides a concrete example, and explains the practical implications.</p>')

    # Add sketch for first intermediate exercise
    intermediate_ex = levels["INTERMEDIATE"]
    if intermediate_ex:
        num, etype, text = intermediate_ex[0]
        lines.append(f'            <p><strong>Exercise {num}:</strong> Start by identifying the main components or trade-offs involved. Consider both the technical mechanism and the practical constraints. A complete answer addresses at least two perspectives and acknowledges limitations.</p>')

    lines.append('        </div>')
    lines.append('    </details>')

    return '\n'.join(lines)


def add_exercises_to_file(filepath, section_key):
    """Insert exercises before the whats-next div."""
    if section_key not in EXERCISES:
        print(f"  SKIP: No exercises defined for {section_key}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if exercises already exist
    if 'How to use these exercises' in content:
        print(f"  SKIP: Exercises already present in {section_key}")
        return False

    exercises_html = generate_exercises_html(section_key, EXERCISES[section_key])

    # Insert before whats-next div
    marker = '<div class="whats-next">'
    if marker not in content:
        # Try alternate: insert before bibliography
        marker = '<section class="bibliography">'

    if marker not in content:
        print(f"  ERROR: No insertion point found in {section_key}")
        return False

    content = content.replace(marker, exercises_html + '\n\n' + marker, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  DONE: Added {len(EXERCISES[section_key]['exercises'])} exercises to {section_key}")
    return True


def main():
    count = 0
    for section_key in sorted(EXERCISES.keys()):
        filepath = os.path.join(BASE, section_key)
        if not os.path.exists(filepath):
            print(f"  MISSING: {filepath}")
            continue
        if add_exercises_to_file(filepath, section_key):
            count += 1
    print(f"\nTotal: Added exercises to {count} files")


if __name__ == '__main__':
    main()
