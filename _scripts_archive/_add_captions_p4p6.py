"""Add captions to uncaptioned <pre> code blocks in Parts 4-6."""
import re
import os

# All the caption data: file -> list of (approx_line, caption_text)
# We'll match by finding uncaptioned <pre> blocks in order and applying captions sequentially

CAPTIONS = {
    # ============ PART 4 ============
    "part-4-training-adapting/module-13-synthetic-data/section-13.1.html": [
        "This snippet loads training data with pandas and inspects class distributions and text length statistics to diagnose imbalance before synthetic augmentation. The value_counts() and describe() calls reveal how skewed the original dataset is across label categories.",
        "This snippet defines a SyntheticDataConfig dataclass that centralizes generation parameters including target_distribution percentages, quality_threshold cutoffs, and dedup_similarity limits. The generate_batch method dispatches to an LLM with temperature and max_tokens controls.",
        "This snippet deduplicates synthetic examples by computing SHA-256 content hashes and measuring pairwise cosine similarity against a configurable threshold. The deduplicate function returns only examples whose similarity to all previously accepted items falls below the cutoff.",
    ],
    "part-4-training-adapting/module-13-synthetic-data/section-13.3.html": [
        "This snippet generates synthetic responses by varying system prompts across persona types such as formal_expert and casual_explainer. The generate_with_variation function iterates over style configurations and collects completions with their associated persona metadata.",
    ],
    "part-4-training-adapting/module-13-synthetic-data/section-13.4.html": [
        "This snippet implements a multi-stage quality filter that chains rule-based checks (length bounds, repetition ratio) with an LLM-based quality scorer. The filter_synthetic_data function applies each stage sequentially and logs rejection reasons per example.",
        "This snippet builds a composable FilterPipeline class where individual filters for length, quality score, and repetition are chained via the add_filter method. The run method applies all registered filters in sequence and collects per-stage pass/fail statistics.",
        "This snippet constructs a Distilabel pipeline that pairs a TextGeneration step with an UltraFeedback scoring step. The pipeline definition wires the generation output into the scorer input and sets batch_size and num_generations parameters for throughput control.",
    ],
    "part-4-training-adapting/module-13-synthetic-data/section-13.5.html": [
        "This snippet structures annotation tasks as JSON records containing text, candidate_labels, and guidelines fields. The format_for_annotation function produces a standardized payload that both human annotators and LLM judges can consume identically.",
        "This snippet calculates annotation quality metrics using numpy, including per-annotator agreement rates, label distribution entropy, and annotator reliability scores. The compute_metrics function returns a summary dictionary keyed by metric name.",
        "This snippet computes inter-annotator agreement using Cohen's kappa via sklearn.metrics.cohen_kappa_score. The function iterates over annotator pairs, averages pairwise kappa values, and flags pairs whose agreement falls below the acceptable_threshold.",
    ],
    "part-4-training-adapting/module-13-synthetic-data/section-13.6.html": [
        "This snippet applies privacy and governance checks by running regex-based PII detectors for emails, phone numbers, and SSNs, then measuring demographic bias ratios. The audit_dataset function returns a GovernanceReport with per-check pass/fail counts.",
        "This snippet measures dataset diversity by computing pairwise cosine distances in embedding space and reporting the mean, minimum, and standard deviation. The diversity_score function uses sentence-transformers to encode all examples before distance calculation.",
        "This snippet defines a DataGovernanceRecord dataclass that logs provenance fields including generation_model, generation_date, filtering_steps, and license. The to_json method serializes the record for storage alongside the synthetic dataset.",
    ],
    "part-4-training-adapting/module-13-synthetic-data/section-13.7.html": [
        "This snippet generates reasoning traces with rejection sampling by running the model multiple times per problem and keeping only traces whose extracted final_answer matches the ground truth. The sample_and_filter function tracks acceptance rates across attempts.",
        "This snippet structures reasoning traces as JSON objects containing problem, chain_of_thought steps, final_answer, and correctness fields. Each step in the chain includes a step_number, reasoning string, and intermediate_result for fine-grained training signal.",
    ],
    "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html": [
        "This snippet defines an estimate_training_resources function that calculates GPU memory, training time, and estimated cost based on model_size_billions, method (full vs. LoRA vs. QLoRA), and dataset_size_tokens. The branching logic shows how LoRA reduces memory by roughly 60% compared to full fine-tuning.",
        "This snippet implements catastrophic forgetting mitigation strategies via a ForgettingMitigation dataclass that configures replay_ratio, ewc_lambda, and lr_schedule parameters. The apply_replay_mixing function interleaves original pretraining samples at the specified ratio during fine-tuning.",
    ],
    "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.2.html": [
        "This snippet defines a typed DataPipelineConfig dataclass centralizing hyperparameters for the fine-tuning data pipeline, including max_seq_length, packing_strategy, validation_split, and preprocessing_workers. The build_pipeline method chains tokenization, filtering, and batching steps using these settings.",
    ],
    "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.4.html": [
        "This snippet formats training examples as JSONL for the OpenAI fine-tuning API, where each line contains a messages array with system, user, and assistant roles. The format_for_openai function validates message structure and writes one JSON object per line to the output file.",
        "This snippet compares fine-tuning costs across API providers (OpenAI, Anthropic) and self-hosted GPU options by computing training cost, monthly inference spend, and break-even points. The CostEstimator class returns a ranked DataFrame sorted by total_6mo_cost.",
    ],
    "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.5.html": [
        "This snippet implements a should_finetune_embeddings decision function that compares baseline_ndcg against a target threshold, checks available training pairs, and estimates compute cost. It returns a recommendation with reasoning based on expected NDCG lift versus resource investment.",
    ],
    "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.6.html": [
        "This snippet implements class-weighted cross-entropy loss for imbalanced datasets by computing inverse-frequency weights with torch.tensor and passing them to nn.CrossEntropyLoss. The WeightedTrainer subclass overrides compute_loss to apply these per-class weights during each forward pass.",
    ],
    "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.7.html": [
        "This snippet implements a reorder_context_for_retrieval function that mitigates the lost-in-the-middle problem by placing the highest-relevance passages at the beginning and end of the context window. The alternating insertion logic ensures the model attends to the most important chunks first and last.",
    ],
    "part-4-training-adapting/module-15-peft/section-15.1.html": [
        "This snippet configures a LoRA adapter with LoraConfig specifying r=16 rank, lora_alpha=32 scaling factor, and target_modules for query and value projection layers. The get_peft_model call wraps the base model and prints the fraction of trainable versus frozen parameters.",
    ],
    "part-4-training-adapting/module-15-peft/section-15.3.html": [
        "This YAML configuration for Axolotl specifies the base_model path, LoRA rank/alpha, dataset references, and training hyperparameters such as micro_batch_size and learning_rate. The sequence_len and gradient_accumulation_steps settings control memory usage during the fine-tuning run.",
    ],
    "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html": [
        "This pseudocode outlines the PPO-based RLHF training loop, which iterates over prompts to sample responses from the current policy pi_theta, scores them with reward model R, and updates the policy using clipped surrogate loss with a KL penalty weighted by beta against the reference policy pi_ref.",
    ],
    "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.3.html": [
        "This snippet measures alignment tax across capability dimensions by evaluating the model on benchmarks for reasoning, coding, factuality, and instruction following before and after alignment. The AlignmentTaxReport dataclass stores per-dimension deltas and flags any regression exceeding the tolerance threshold.",
    ],
    # ============ PART 5 ============
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.1.html": [
        "This snippet encodes sentences using SentenceTransformer with the all-MiniLM-L6-v2 model and mean pooling, then computes pairwise cosine similarity with util.cos_sim. The output matrix reveals which sentence pairs are semantically closest in the 384-dimensional embedding space.",
        "This snippet implements the InfoNCE (Multiple Negatives Ranking) loss function using torch.nn.functional.cosine_similarity and cross_entropy. The sim_matrix is scaled by a temperature parameter before the loss treats each diagonal element as the positive pair against all off-diagonal negatives.",
        "This snippet demonstrates ColBERT-style MaxSim late-interaction scoring by computing token-level cosine similarities between query and document embeddings, taking the max over document tokens for each query token, then summing. This per-token maximum approach preserves fine-grained matching signal lost in single-vector models.",
        "This snippet calls the OpenAI embeddings API with the text-embedding-3-large model and a dimensions parameter to control output size. The normalize_l2 helper ensures unit-length vectors before storing them, and numpy dot products verify that truncated embeddings preserve relative similarity rankings.",
    ],
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.2.html": [
        "This snippet implements brute-force k-nearest-neighbor search using numpy dot products (or cosine distance) over the full vector set. The timing wrapper shows that linear scan latency grows linearly with n_vectors, establishing the baseline that approximate methods aim to beat.",
        "This snippet builds an HNSW index with faiss.IndexHNSWFlat, setting M=32 neighbors and efConstruction=200 during build time. The search-time efSearch parameter is then varied to show the recall-versus-latency tradeoff compared to brute-force, demonstrating sub-millisecond queries on one million vectors.",
        "This snippet creates an IVF (Inverted File) index with faiss.IndexIVFFlat using 1024 Voronoi cells and trains it on the dataset. The nprobe parameter controls how many cells are searched at query time, trading recall for speed, and the output compares recall@10 at different nprobe values.",
        "This snippet combines IVF partitioning with Product Quantization in faiss.IndexIVFPQ, compressing each 768-dimensional vector into m=48 sub-quantizers of nbits=8. The result dramatically reduces memory (shown by the index size comparison) while maintaining reasonable recall through asymmetric distance computation.",
        "This snippet uses the FAISS index_factory string interface to compose complex index types in a single line, such as 'IVF4096,PQ48' or 'OPQ48,IVF4096,PQ48'. The factory pattern simplifies experimentation by letting users swap index architectures without rewriting index construction code.",
    ],
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.3.html": [
        "This snippet sets up a ChromaDB collection with SentenceTransformerEmbeddingFunction, adds documents with metadata dictionaries, and queries with a where filter clause. The results object contains ids, distances, and documents, demonstrating ChromaDB's combined vector and metadata filtering capabilities.",
        "This snippet implements Reciprocal Rank Fusion (RRF) to merge ranked result lists from multiple retrievers. The rrf_score formula 1/(k + rank) with k=60 downweights lower-ranked items, and the function returns a unified ranking sorted by aggregated scores across all input lists.",
    ],
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.4.html": [
        "This snippet uses unstructured.partition.pdf to parse a PDF into typed elements (NarrativeText, Table, Image), applying hi_res strategy with an OCR language parameter. The element_type attribute on each returned chunk enables downstream routing of tables versus narrative text.",
        "This snippet implements fixed-size chunking with configurable chunk_size and overlap parameters, slicing the input text on token boundaries. The overlap ensures that sentences split across chunk borders are still captured in at least one chunk, and the function returns a list of text segments.",
        "This snippet uses LangChain's RecursiveCharacterTextSplitter with a hierarchy of separators (paragraph breaks, newlines, sentences, words) to split documents. The recursive approach tries the coarsest separator first and falls back to finer splits only when chunks exceed chunk_size.",
        "This snippet implements incremental indexing with content hashing by computing SHA-256 digests of each document chunk and comparing against previously stored hashes. Only new or modified chunks are embedded and upserted, avoiding redundant embedding API calls when the corpus is updated.",
    ],
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.5.html": [
        "This pseudocode outlines the ColBERT training and retrieval loop, including embed_pages for document encoding, embed_queries for query encoding, and maxsim_score for late-interaction scoring. The training loop optimizes contrastive loss while the retrieval path scores query-document pairs at the token level.",
    ],
    "part-5-retrieval-conversation/module-20-rag/section-20.1.html": [
        "This pseudocode describes the core RAG pipeline: encode query q with embedding model E, retrieve top-k passages from knowledge base KB by cosine similarity, concatenate them into a context string, and pass the augmented prompt to generator G. The output is a grounded response conditioned on retrieved evidence.",
    ],
    # ============ PART 6 ============
    "part-6-agentic-ai/module-22-ai-agents/section-22.1.html": [
        "This pseudocode formalizes the ReAct agent loop: given a user task T, tool set, and LLM M, the agent iterates through Thought, Action, and Observation steps up to max_steps S. The loop terminates when the LLM emits a final_answer action or the step budget is exhausted, returning the accumulated trajectory.",
    ],
    "part-6-agentic-ai/module-22-ai-agents/section-22.2.html": [
        "This snippet demonstrates MemGPT-style tiered memory management using the Letta client SDK. The create_agent call configures working memory (system prompt context), archival memory (vector-indexed long-term store), and recall memory (conversation history), with explicit insert and search operations on each tier.",
        "This snippet initializes Mem0 with separate memory type configurations for short_term (session buffer), long_term (persistent vector store), and episodic (experience summaries). The add and search methods show how memories are stored with user_id scoping and retrieved by semantic similarity with a top_k limit.",
    ],
    "part-6-agentic-ai/module-22-ai-agents/section-22.3.html": [
        "This snippet builds a LangGraph StateGraph for a research agent with typed state (ResearchState), conditional branching via should_continue, and tool-calling nodes. The add_conditional_edges method routes between the agent node and tool_executor based on whether the LLM output contains tool calls or a final answer.",
    ],
    "part-6-agentic-ai/module-22-ai-agents/section-22.4.html": [
        "This snippet uses the Anthropic SDK with extended thinking enabled (thinking={\"type\": \"enabled\", \"budget_tokens\": 10000}) for complex planning tasks. The response includes both a thinking block with the model's internal reasoning chain and a text block with the final structured plan.",
    ],
    "part-6-agentic-ai/module-22-ai-agents/section-22.5.html": [
        "This snippet runs an agent evaluation on the SWE-bench Lite benchmark using run_evaluation with a predictions JSONL file. The results include per-instance pass/fail outcomes, and the script computes overall resolve_rate by dividing successful patches by total instances.",
    ],
    "part-6-agentic-ai/module-23-tool-use-protocols/section-23.1.html": [
        "This snippet registers a get_weather tool with the OpenAI function-calling API using a JSON Schema definition for parameters (location string, unit enum). The chat completion loop checks for tool_calls in the response, executes the matching function, and appends the result as a tool message for the next turn.",
        "This snippet defines the same get_weather tool using Anthropic's tool_use format with an input_schema block. The response handling extracts tool_use content blocks, calls the local function, and returns results via a tool_result message type, illustrating the differences from OpenAI's function-calling protocol.",
    ],
    "part-6-agentic-ai/module-23-tool-use-protocols/section-23.2.html": [
        "This snippet builds an MCP server using the Python SDK's Server class, registering tools via @server.tool() decorators with typed parameters. The run_database_query tool validates SQL against an allowed_tables list before execution, and the server is started with stdio transport for local process communication.",
    ],
    "part-6-agentic-ai/module-23-tool-use-protocols/section-23.3.html": [
        "This JSON defines an A2A Agent Card with name, description, capabilities (including streaming and pushNotifications), and a skills array listing supported task types. The endpoint URL and authentication requirements tell client agents how to connect and what operations the agent supports.",
    ],
    "part-6-agentic-ai/module-23-tool-use-protocols/section-23.4.html": [
        "This snippet uses Pydantic models with Field validators to define structured tool input and output schemas, including parameter constraints like ge=0 for amounts and regex patterns for account IDs. The @validator decorators enforce business rules (e.g., transfer amount limits) before the tool function executes.",
    ],
    "part-6-agentic-ai/module-23-tool-use-protocols/section-23.5.html": [
        "This snippet implements Corrective RAG (CRAG) as a LangGraph StateGraph with retrieve, grade_documents, web_search, and generate nodes. The grade_documents node scores each retrieved document's relevance and conditionally routes to web_search if all scores fall below the threshold, improving answer quality for out-of-distribution queries.",
    ],
    "part-6-agentic-ai/module-24-multi-agent-systems/section-24.1.html": [
        "This snippet builds a research agent as a LangGraph StateGraph with typed ResearchState, conditional routing via should_continue, and a tool_executor node. The add_conditional_edges call directs flow between the LLM agent and tool execution based on whether the response contains pending tool calls.",
        "This snippet defines the same research workflow using CrewAI's Agent, Task, and Crew abstractions. The Agent receives a role, goal, and backstory for persona-driven behavior, the Task specifies expected_output format, and Crew.kickoff orchestrates execution with a sequential process.",
        "This snippet implements the research agent using the OpenAI Agents SDK, composing a search_agent and writer_agent into a pipeline where Runner.run passes the search output as input to the writer. The handoff between agents is managed by the SDK's built-in orchestration rather than explicit graph edges.",
    ],
    "part-6-agentic-ai/module-24-multi-agent-systems/section-24.2.html": [
        "This snippet implements the supervisor pattern with LangGraph, where a supervisor_node uses an LLM to select the next worker agent (researcher, writer, or FINISH) based on current state. The conditional routing dispatches to the chosen worker's node, and results flow back through the supervisor until it signals completion.",
    ],
    "part-6-agentic-ai/module-24-multi-agent-systems/section-24.4.html": [
        "This snippet implements a debate pattern between two LangGraph agents with a SqliteSaver checkpoint for state persistence. The advocate and critic nodes exchange arguments over multiple rounds, and a judge_node evaluates both positions to produce a final verdict with confidence scores.",
    ],
    "part-6-agentic-ai/module-24-multi-agent-systems/section-24.5.html": [
        "This snippet builds a human-in-the-loop multi-agent workflow using LangGraph with SqliteSaver checkpointing and an interrupt_before parameter on sensitive nodes. The approval_gate node pauses execution and waits for human input via graph.update_state before the agent proceeds with the approved or modified action.",
    ],
    "part-6-agentic-ai/module-25-specialized-agents/section-25.1.html": [
        "This snippet defines a CodeAgent class that generates code via an LLM, executes it in a subprocess with a configurable timeout, and captures stdout/stderr. The execute_code method runs the generated script in a temporary file with subprocess.run, enforcing a timeout to prevent runaway processes.",
    ],
    "part-6-agentic-ai/module-25-specialized-agents/section-25.2.html": [
        "This snippet builds a browser automation agent using Playwright MCP tools via the Anthropic client. The agent loop sends tool_use responses back as tool_result messages, enabling the LLM to chain actions like navigate, click, and extract_text across multiple page interactions.",
    ],
    "part-6-agentic-ai/module-25-specialized-agents/section-25.3.html": [
        "This snippet implements a computer-use agent loop using Anthropic's computer_use_20250124 tool type, which accepts screenshot inputs as base64-encoded images. The loop captures screenshots with pyautogui, sends them to the model, and executes returned mouse/keyboard actions until the task is complete or max_steps is reached.",
    ],
    "part-6-agentic-ai/module-25-specialized-agents/section-25.4.html": [
        "This snippet creates a data analysis agent using the E2B Sandbox for isolated code execution. The agent generates pandas and matplotlib code, runs it inside the sandbox via sandbox.run_code, and retrieves both text output and generated plot files, ensuring untrusted code cannot affect the host system.",
    ],
    "part-6-agentic-ai/module-26-agent-safety-production/section-26.1.html": [
        "This snippet defines a SecureAgentExecutor that wraps an agent with a policy engine, validating each proposed tool call against allowed actions and parameter constraints before execution. The execute method checks policy.is_allowed for every action and raises PolicyViolation if a tool call falls outside the permitted set.",
    ],
    "part-6-agentic-ai/module-26-agent-safety-production/section-26.2.html": [
        "This snippet uses the E2B Sandbox to execute agent-generated code in an isolated container with configurable timeout. The sandbox.run_code call returns separate stdout and stderr streams, and the with-block ensures automatic cleanup of the container after execution completes or times out.",
    ],
    "part-6-agentic-ai/module-26-agent-safety-production/section-26.3.html": [
        "This snippet integrates Langfuse tracing with the @observe decorator to capture agent execution spans, including tool calls and LLM invocations. The langfuse.trace call creates a parent span, and nested @observe functions automatically record latency, token counts, and metadata for each sub-step.",
        "This snippet implements a BudgetEnforcer class that tracks cumulative token usage and estimated cost across agent steps. The check_budget method raises BudgetExceeded if either max_tokens or max_cost_usd thresholds are breached, providing a hard stop for runaway agent loops.",
    ],
    "part-6-agentic-ai/module-26-agent-safety-production/section-26.4.html": [
        "This snippet defines a ResilientAgent class with exponential backoff retry logic, circuit-breaker state tracking, and graceful degradation to cached responses. The execute method retries failed LLM calls up to max_retries times with increasing delays, and falls back to a cached_response when the circuit breaker trips open.",
    ],
    "part-6-agentic-ai/module-26-agent-safety-production/section-26.5.html": [
        "This snippet uses Pydantic BaseModel classes to define explicit contracts between a PlannerOutput (with steps list and confidence float) and an ExecutorInput that validates the plan. The strict typing ensures that malformed plans are rejected at the boundary before the executor agent processes them.",
        "This snippet implements a ChaosInjector test harness that randomly injects failures (timeouts, malformed responses, rate limits) into agent tool calls at a configurable failure_rate. The inject method wraps real tool functions and probabilistically raises exceptions, enabling systematic resilience testing of agent error handling.",
    ],
}

def add_captions_to_file(filepath, captions):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pre_pattern = re.compile(r'</pre>', re.DOTALL)
    matches = list(pre_pattern.finditer(content))

    # Find which matches are uncaptioned
    uncaptioned_positions = []
    for m in matches:
        end_pos = m.end()
        after = content[end_pos:end_pos + 200].strip()
        if not after.startswith('<div class="code-caption">'):
            uncaptioned_positions.append(end_pos)

    if len(uncaptioned_positions) != len(captions):
        print(f"  WARNING: {filepath} has {len(uncaptioned_positions)} uncaptioned blocks but {len(captions)} captions provided!")
        return False

    # Count existing captions to determine starting fragment number
    existing_count = len(matches) - len(uncaptioned_positions)
    # Actually, we need to number sequentially across ALL code blocks in the file
    # Let's find all pre blocks and figure out which already have captions and what numbers
    existing_caption_pattern = re.compile(r'<div class="code-caption"><strong>Code Fragment (\d+):', re.DOTALL)
    existing_numbers = [int(m.group(1)) for m in existing_caption_pattern.finditer(content)]

    # We need to assign numbers to uncaptioned blocks based on their position among all pre blocks
    all_pre_matches = list(re.compile(r'</pre>').finditer(content))

    # Build a map: for each </pre>, is it captioned or not?
    fragment_num = 0
    assignments = {}  # position -> fragment number to assign

    for m in all_pre_matches:
        end_pos = m.end()
        after = content[end_pos:end_pos + 200].strip()
        fragment_num += 1
        if not after.startswith('<div class="code-caption">'):
            assignments[end_pos] = fragment_num

    # Now insert captions in reverse order to preserve positions
    caption_idx = len(captions) - 1
    for pos in reversed(uncaptioned_positions):
        frag_num = assignments[pos]
        caption_html = f'\n<div class="code-caption"><strong>Code Fragment {frag_num}:</strong> {captions[caption_idx]}</div>'
        content = content[:pos] + caption_html + content[pos:]
        caption_idx -= 1

    # Now we need to renumber ALL captions sequentially
    # First, find all code-caption divs and renumber them
    def renumber_captions(text):
        counter = [0]
        def replacer(match):
            counter[0] += 1
            return f'<div class="code-caption"><strong>Code Fragment {counter[0]}:'
        return re.sub(
            r'<div class="code-caption"><strong>Code Fragment \d+:',
            replacer,
            text
        )

    content = renumber_captions(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


base = "E:/Projects/LLMCourse"
total_added = 0
total_files = 0

for rel_path, captions in CAPTIONS.items():
    filepath = os.path.join(base, rel_path)
    if not os.path.exists(filepath):
        print(f"MISSING: {filepath}")
        continue

    print(f"Processing {rel_path} ({len(captions)} captions)...")
    success = add_captions_to_file(filepath, captions)
    if success:
        total_added += len(captions)
        total_files += 1
        print(f"  Added {len(captions)} captions")
    else:
        print(f"  SKIPPED due to mismatch")

print(f"\nDone: {total_added} captions added across {total_files} files")
