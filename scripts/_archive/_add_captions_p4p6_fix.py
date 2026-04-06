"""Add captions to remaining uncaptioned <pre> code blocks in Parts 4-6 (files that were skipped)."""
import re
import os

CAPTIONS = {
    "part-4-training-adapting/module-15-peft/section-15.1.html": [
        # Block 1 (line ~207): LoRA config
        "This snippet configures a LoRA adapter with LoraConfig specifying r=16 rank, lora_alpha=32 scaling factor, and target_modules for query and value projection layers. The get_peft_model call wraps the base model and prints the fraction of trainable versus frozen parameters.",
        # Block 4 (line ~423): pip install
        "This command installs the required packages for LoRA fine-tuning: transformers, trl, peft, datasets, accelerate, torch, and bitsandbytes. The bitsandbytes library enables optional 4-bit quantization for QLoRA experiments.",
        # Block 5 (line ~432): Step 1 load model + apply LoRA
        "This lab step loads SmolLM2-135M-Instruct with AutoModelForCausalLM, creates a LoraConfig targeting q_proj and v_proj layers with rank 16 and alpha 32, and calls get_peft_model to wrap the base model. The print_trainable_parameters() call reveals that fewer than 0.1% of parameters are trainable.",
        # Block 6 (line ~467): Step 2 compare ranks
        "This lab step iterates over LoRA ranks [4, 8, 16, 32, 64], creating a fresh model and LoraConfig for each, then summing trainable vs. total parameters. The resulting pandas DataFrame shows that trainable parameter count scales linearly with rank while total model size remains constant.",
        # Block 7 (line ~500): Step 3 train with SFTTrainer
        "This lab step fine-tunes the LoRA adapter using SFTTrainer on 300 examples from the no_robots dataset. The SFTConfig sets learning_rate=2e-4 (10x higher than full fine-tuning), max_seq_length=512, and gradient_accumulation_steps=2 to simulate a larger effective batch size.",
        # Block 8 (line ~541): Step 4 save and merge
        "This lab step saves the LoRA adapter weights with save_pretrained (producing files of only a few hundred KB), then reloads the base model and merges the adapter via PeftModel.from_pretrained and merge_and_unload(). The adapter_size calculation demonstrates the storage savings compared to a full model checkpoint.",
        # Block 9 (line ~568): Step 5 test merged model
        "This lab step generates responses from the merged model on three test prompts using apply_chat_template and model.generate with temperature=0.7. Comparing these outputs against the base model's responses reveals the instruction-following improvements from LoRA fine-tuning.",
        # Block 10 (line ~613): Complete solution
        "This complete solution combines all five lab steps into a single script: applying LoRA to SmolLM2-135M, benchmarking ranks 4 through 64, training with SFTTrainer on no_robots data, saving and merging the adapter, and generating test responses. The condensed version uses the same hyperparameters as the step-by-step walkthrough.",
    ],
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.1.html": [
        # Block 1: sentence embedding with mean pooling
        "This snippet encodes sentences using SentenceTransformer with the all-MiniLM-L6-v2 model and mean pooling, then computes pairwise cosine similarity with util.cos_sim. The output matrix reveals which sentence pairs are semantically closest in the 384-dimensional embedding space.",
        # Block 2: InfoNCE loss
        "This snippet implements the InfoNCE (Multiple Negatives Ranking) loss function using torch.nn.functional.cosine_similarity and cross_entropy. The sim_matrix is scaled by a temperature parameter before the loss treats each diagonal element as the positive pair against all off-diagonal negatives.",
        # Block 4: ColBERT MaxSim
        "This snippet demonstrates ColBERT-style MaxSim late-interaction scoring by computing token-level cosine similarities between query and document embeddings, taking the max over document tokens for each query token, then summing. This per-token maximum approach preserves fine-grained matching signal lost in single-vector models.",
        # Block 5: OpenAI embeddings
        "This snippet calls the OpenAI embeddings API with the text-embedding-3-large model and a dimensions parameter to control output size. The normalize_l2 helper ensures unit-length vectors before storing them, and numpy dot products verify that truncated embeddings preserve relative similarity rankings.",
        # Block 7: pip install
        "This command installs sentence-transformers, numpy, and pandas, which provide the embedding models, numerical operations, and data analysis tools needed for the semantic search lab exercises below.",
        # Block 8: Step 1 load two models
        "This lab step loads two SentenceTransformer models of different sizes (all-MiniLM-L6-v2 at 384 dimensions and all-mpnet-base-v2 at 768 dimensions) and prints their embedding dimensionality. The shape comparison shows the tradeoff between model size and representation capacity.",
        # Block 9: Step 2 encode documents
        "This lab step defines a diverse 15-document corpus spanning programming, biology, and geography, then encodes all documents with both models using batch encode. The resulting embeddings_small and embeddings_large arrays have shapes (15, 384) and (15, 768) respectively.",
        # Block 10: Step 3 semantic search
        "This lab step implements a semantic_search function that encodes the query, computes cosine similarity against all document embeddings, and returns the top_k highest-scoring matches. The test loop runs four diverse queries and prints ranked results with similarity scores.",
        # Block 11: Step 4 benchmark with precision@k
        "This lab step evaluates both embedding models using precision_at_k against a ground_truth dictionary mapping queries to expected document indices. The final output compares average P@3 scores between MiniLM and MPNet, quantifying how model size affects retrieval quality.",
        # Block 12: complete solution
        "This complete solution consolidates model loading, document encoding, the search function, and the precision@3 benchmark into a single script. It reproduces the full lab workflow from embedding creation through retrieval evaluation in a compact form.",
    ],
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.4.html": [
        # Block 1: Unstructured.io parsing
        "This snippet uses unstructured.partition.pdf to parse a PDF into typed elements (NarrativeText, Table, Image), applying hi_res strategy with an OCR language parameter. The element_type attribute on each returned chunk enables downstream routing of tables versus narrative text.",
        # Block 2: fixed-size chunking
        "This snippet implements fixed-size chunking with configurable chunk_size and overlap parameters, slicing the input text on token boundaries. The overlap ensures that sentences split across chunk borders are still captured in at least one chunk, and the function returns a list of text segments.",
        # Block 3: recursive text splitting
        "This snippet uses LangChain's RecursiveCharacterTextSplitter with a hierarchy of separators (paragraph breaks, newlines, sentences, words) to split documents. The recursive approach tries the coarsest separator first and falls back to finer splits only when chunks exceed chunk_size.",
        # Block 6: incremental indexing
        "This snippet implements incremental indexing with content hashing by computing SHA-256 digests of each document chunk and comparing against previously stored hashes. Only new or modified chunks are embedded and upserted, avoiding redundant embedding API calls when the corpus is updated.",
        # Block 8: pip install
        "This command installs sentence-transformers and numpy for the chunking strategy comparison lab. These packages provide the embedding model for semantic chunking and the numerical operations for similarity computation.",
        # Block 9: Step 1 create sample document
        "This lab step defines a structured ML textbook document with Markdown headers (h1, h2, h3) and paragraph breaks that serve as natural topic boundaries. The document covers supervised learning, unsupervised learning, and deep learning, providing clear sections for chunking experiments.",
        # Block 10: Step 2 three chunking strategies
        "This lab step implements three chunking strategies: fixed_chunk slices by character count with overlap, recursive_chunk splits on ## and ### Markdown headers, and semantic_chunk uses SentenceTransformer cosine similarity between consecutive sentences to detect topic shifts below a threshold.",
        # Block 11: Step 3 compare retrieval quality
        "This lab step tests retrieval quality by running four queries with known expected keywords against each chunking strategy's output. The search_chunks function encodes chunks and queries with SentenceTransformer and reports PASS/MISS for each strategy, revealing which preserves topical coherence best.",
        # Block 12: complete solution
        "This complete solution combines the sample document, all three chunking strategies (fixed, recursive, semantic), and the retrieval benchmark into a single script. It reproduces the full lab from document creation through chunking through retrieval evaluation.",
    ],
    "part-5-retrieval-conversation/module-20-rag/section-20.1.html": [
        # Block 1: pseudocode RAG pipeline
        "This pseudocode describes the core RAG pipeline: encode query q with embedding model E, retrieve top-k passages from knowledge base KB by cosine similarity, concatenate them into a context string, and pass the augmented prompt to generator G. The output is a grounded response conditioned on retrieved evidence.",
        # Block 6: pip install
        "This command installs openai, sentence-transformers, and numpy for the RAG lab. The openai package provides the LLM generation API, sentence-transformers handles document embedding, and numpy performs the cosine similarity search.",
        # Block 7: Step 1 create knowledge base
        "This lab step defines a five-document knowledge base simulating an internal company wiki with policies on vacation, remote work, health benefits, expense reimbursement, and performance reviews. Each document has an id, title, and text field containing specific policy details and numerical limits.",
        # Block 8: Step 2 build vector index
        "This lab step encodes all knowledge base documents using SentenceTransformer all-MiniLM-L6-v2 and pre-computes doc_norms for efficient cosine similarity. The resulting doc_embeddings array with shape (5, 384) serves as the retrieval index for incoming queries.",
        # Block 9: Step 3 implement retrieval
        "This lab step implements a retrieve function that encodes the query, computes cosine similarity against all document embeddings using numpy dot products and pre-computed norms, and returns the top_k documents with scores. The test loop verifies that vacation, remote work, health, and expense queries retrieve the correct policy documents.",
        # Block 10: Step 4 RAG generation pipeline
        "This lab step builds the full RAG pipeline by combining retrieval with OpenAI's gpt-4o-mini for generation. The system prompt instructs the model to answer ONLY from retrieved context, cite sources with [Source N], and admit uncertainty, while temperature=0.3 reduces hallucination risk.",
        # Block 11: Step 5 out-of-scope queries
        "This lab step tests the RAG system with three questions that have no answer in the knowledge base (stock price, CEO name, programming languages). A well-prompted system should respond with 'I don't have enough information' rather than hallucinating answers from the irrelevant retrieved context.",
        # Block 12: complete solution
        "This complete solution combines the knowledge base, embedding index, retrieval function, and RAG generation pipeline into a single compact script. It processes both in-scope and out-of-scope queries, demonstrating end-to-end grounded question answering with source citations.",
    ],
    "part-6-agentic-ai/module-23-tool-use-protocols/section-23.2.html": [
        # Block 1: MCP server
        "This snippet builds an MCP server using the Python SDK's Server class, registering tools via @server.tool() decorators with typed parameters. The run_database_query tool validates SQL against an allowed_tables list before execution, and the server is started with stdio transport for local process communication.",
        # Block 2: pip install
        "This command installs torch, transformers, and numpy for the MCP tool-use protocol lab. These packages provide the model loading, tokenization, and numerical operations needed for the exercises.",
        # Block 3: TODO setup
        "This placeholder marks Step 1 of the lab, where students will load the required libraries and prepare data for the MCP server tool-use exercises.",
        # Block 4: complete solution
        "This placeholder marks the complete solution for the MCP tool-use lab exercise. Students should implement the full MCP server with tool registration and request handling.",
    ],
    "part-6-agentic-ai/module-24-multi-agent-systems/section-24.1.html": [
        # Block 1: LangGraph research agent
        "This snippet builds a research agent as a LangGraph StateGraph with typed ResearchState, conditional routing via should_continue, and a tool_executor node. The add_conditional_edges call directs flow between the LLM agent and tool execution based on whether the response contains pending tool calls.",
        # Block 2: CrewAI research agent
        "This snippet defines the same research workflow using CrewAI's Agent, Task, and Crew abstractions. The Agent receives a role, goal, and backstory for persona-driven behavior, the Task specifies expected_output format, and Crew.kickoff orchestrates execution with a sequential process.",
        # Block 3: OpenAI Agents SDK research agent
        "This snippet implements the research agent using the OpenAI Agents SDK, composing a search_agent and writer_agent into a pipeline where Runner.run passes the search output as input to the writer. The handoff between agents is managed by the SDK's built-in orchestration rather than explicit graph edges.",
        # Block 4: pip install
        "This command installs torch, transformers, and numpy for the multi-agent framework selection lab. These packages provide the foundation for the exercises below.",
        # Block 5: TODO setup
        "This placeholder marks Step 1 of the lab, where students will load the required libraries and prepare data for the multi-agent framework selection exercise.",
        # Block 6: complete solution
        "This placeholder marks the complete solution for the multi-agent framework selection lab exercise. Students should implement the full framework comparison with LangGraph, CrewAI, or the OpenAI Agents SDK.",
    ],
    "part-6-agentic-ai/module-26-agent-safety-production/section-26.5.html": [
        # Block 1: Pydantic contracts
        "This snippet uses Pydantic BaseModel classes to define explicit contracts between a PlannerOutput (with steps list and confidence float) and an ExecutorInput that validates the plan. The strict typing ensures that malformed plans are rejected at the boundary before the executor agent processes them.",
        # Block 2: ChaosInjector
        "This snippet implements a ChaosInjector test harness that randomly injects failures (timeouts, malformed responses, rate limits) into agent tool calls at a configurable failure_rate. The inject method wraps real tool functions and probabilistically raises exceptions, enabling systematic resilience testing of agent error handling.",
        # Block 3: pip install
        "This command installs torch, transformers, and numpy for the agent testing and contract-validation lab. These packages provide the foundation for the exercises below.",
        # Block 4: TODO setup
        "This placeholder marks Step 1 of the lab, where students will load the required libraries and prepare data for the agent testing exercises.",
        # Block 5: complete solution
        "This placeholder marks the complete solution for the agent testing lab exercise. Students should implement the full contract validation and chaos testing pipeline.",
    ],
}


def add_captions_to_file(filepath, captions):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pre_end_pattern = re.compile(r'</pre>')
    matches = list(pre_end_pattern.finditer(content))

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

    # Assign fragment numbers based on position among ALL pre blocks
    all_pre_matches = list(pre_end_pattern.finditer(content))
    fragment_num = 0
    assignments = {}
    for m in all_pre_matches:
        end_pos = m.end()
        after = content[end_pos:end_pos + 200].strip()
        fragment_num += 1
        if not after.startswith('<div class="code-caption">'):
            assignments[end_pos] = fragment_num

    # Insert captions in reverse order
    caption_idx = len(captions) - 1
    for pos in reversed(uncaptioned_positions):
        frag_num = assignments[pos]
        caption_html = f'\n<div class="code-caption"><strong>Code Fragment {frag_num}:</strong> {captions[caption_idx]}</div>'
        content = content[:pos] + caption_html + content[pos:]
        caption_idx -= 1

    # Renumber ALL captions sequentially
    counter = [0]
    def replacer(match):
        counter[0] += 1
        return f'<div class="code-caption"><strong>Code Fragment {counter[0]}:'
    content = re.sub(
        r'<div class="code-caption"><strong>Code Fragment \d+:',
        replacer,
        content
    )

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
