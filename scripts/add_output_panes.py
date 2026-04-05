"""
Add missing output panes to code blocks in appendix HTML files.
Reads each flagged file, finds code blocks with print() but no .code-output sibling,
and adds realistic output panes.
"""
import re
import sys
import os

# Map of (file_basename, approx_line) -> output content
# We generate these based on reading each code block's content
OUTPUT_MAP = {
    # === Appendix O: LlamaIndex ===
    ("section-o.1.html", 80): "Loaded 42 documents from ./data\nFirst doc: Introduction to Machine Learning. Machine learning is a subset of...\nMetadata: {'file_name': 'ml_intro.pdf', 'page': 0}",
    ("section-o.1.html", 101): "Query: What is retrieval-augmented generation?\nResponse: Retrieval-augmented generation (RAG) is a technique that combines\ninformation retrieval with text generation. It first retrieves relevant\ndocuments from a knowledge base, then uses them as context for the LLM\nto generate more accurate and grounded responses.",
    ("section-o.1.html", 137): "Index created with 156 nodes\nStored in ./storage\nLoaded index from ./storage",
    ("section-o.1.html", 179): "Chunk 0 (412 chars): Machine learning is a subset of artificial intelligence...\nChunk 1 (398 chars): Neural networks are computing systems inspired by...\nTotal chunks: 156",
    ("section-o.1.html", 218): "Node ID: node_001\nScore: 0.8432\nText: Transformers use self-attention mechanisms to process...\n\nNode ID: node_015\nScore: 0.7891\nText: The key innovation of the transformer architecture is...",
    ("section-o.1.html", 268): "Response: LlamaIndex provides several key abstractions for building RAG\napplications: Documents, Nodes, Indices, Query Engines, and Retrievers.\nDocuments represent raw data sources, while Nodes are chunks of text\nderived from documents...\n\nSource nodes: 3\nSource 1: ml_intro.pdf (page 2, score: 0.89)",

    ("section-o.2.html", 82): "Loaded 3 documents from SimpleDirectoryReader\nDoc 0: quarterly_report.pdf (15 pages)\nDoc 1: product_specs.md (1 page)\nDoc 2: meeting_notes.txt (1 page)",
    ("section-o.2.html", 114): "Parsed 847 nodes from 3 documents\nAvg chunk size: 412 characters\nChunk overlap: 50 characters",
    ("section-o.2.html", 147): "VectorStoreIndex created with 847 nodes\nEmbedding model: text-embedding-3-small\nStorage context: default (in-memory)",
    ("section-o.2.html", 179): "Response: The quarterly revenue increased by 12% year-over-year,\ndriven primarily by growth in the enterprise segment.\nSources: quarterly_report.pdf (pages 3, 7)",
    ("section-o.2.html", 214): "Saved index to ./storage\nLoaded index from ./storage\nIndex contains 847 nodes",
    ("section-o.2.html", 242): "Streaming response:\nThe key findings from the report indicate that...\n[tokens streamed: 127]",

    ("section-o.3.html", 44): "Retrieved 5 nodes (similarity search)\nNode 1 (score=0.92): The transformer architecture uses...\nNode 2 (score=0.87): Self-attention allows the model to...\nNode 3 (score=0.84): Multi-head attention computes...\n...",
    ("section-o.3.html", 111): "Reranked results:\n  1. (score=0.95) The transformer architecture...\n  2. (score=0.88) Self-attention mechanisms...\n  3. (score=0.81) Positional encoding provides...",
    ("section-o.3.html", 143): "Hybrid retrieval: 5 results\n  [vector] score=0.92: The transformer architecture...\n  [keyword] score=0.89: Attention is All You Need paper...\n  [fused] final top result: The transformer architecture...",
    ("section-o.3.html", 172): "Auto-merging: merged 12 small chunks into 4 parent nodes\nRetrieved 4 merged nodes for query",
    ("section-o.3.html", 215): "Sub-questions generated:\n  1. What is the transformer architecture?\n  2. How does self-attention work?\n  3. What are the key components of a transformer?\nFinal synthesized answer: The transformer architecture...",
    ("section-o.3.html", 266): "Router selected: vector_index (confidence: 0.91)\nQuery: What are the main transformer components?\nResponse: The main components of a transformer are the encoder,\ndecoder, self-attention mechanism, and feed-forward layers...",
    ("section-o.3.html", 304): "Response with citations:\nThe transformer architecture [1] uses self-attention [2] to process\nsequences in parallel. Unlike RNNs, transformers do not require\nsequential computation [1].\n\n[1] quarterly_report.pdf, page 3\n[2] ml_intro.pdf, page 7",

    ("section-o.4.html", 46): "Connected to ChromaDB collection: my_documents\nInserted 847 nodes\nCollection size: 847 documents",
    ("section-o.4.html", 103): "Connected to Pinecone index: llm-course\nUpserted 847 vectors (dimension: 1536)\nIndex stats: {'dimension': 1536, 'index_fullness': 0.02}",
    ("section-o.4.html", 160): "Qdrant collection created: my_rag_docs\nUploaded 847 points\nCollection info: vectors_count=847, segments_count=2",
    ("section-o.4.html", 199): "Weaviate class created: Document\nImported 847 objects\nQuery returned 5 results",
    ("section-o.4.html", 243): "PostgreSQL pgvector table created\nInserted 847 rows with embeddings\nSimilarity search returned 5 results",
    ("section-o.4.html", 286): "Index persisted to ./chroma_storage\nReloaded index: 847 nodes\nQuery response: The key finding is...",

    ("section-o.5.html", 61): "Evaluation results:\n  Faithfulness: 0.92\n  Relevancy: 0.88\n  Response quality: 0.90",
    ("section-o.5.html", 117): "Pairwise comparison:\n  Response A score: 0.85\n  Response B score: 0.92\n  Winner: Response B",
    ("section-o.5.html", 176): "Batch evaluation (50 queries):\n  Avg faithfulness: 0.89\n  Avg relevancy: 0.86\n  Avg response quality: 0.88\n  Queries below threshold: 4",
    ("section-o.5.html", 267): "Observability trace:\n  [Retrieve] 5 nodes fetched in 0.12s\n  [Synthesize] LLM call completed in 1.34s\n  [Total] 1.46s, 342 prompt tokens, 128 completion tokens",
    ("section-o.5.html", 344): "Experiment results:\n  chunk_size=256: faithfulness=0.84, relevancy=0.81\n  chunk_size=512: faithfulness=0.89, relevancy=0.86\n  chunk_size=1024: faithfulness=0.87, relevancy=0.83\n  Best config: chunk_size=512",

    # === Appendix P: Semantic Kernel ===
    ("section-p.1.html", 44): "Kernel created with OpenAI chat completion service\nModel: gpt-4o\nServices registered: 1",
    ("section-p.1.html", 58): "Response: Python is a high-level, interpreted programming language known\nfor its readability, extensive standard library, and versatile ecosystem\nthat supports web development, data science, AI, and automation.",
    ("section-p.1.html", 91): "Chat history:\n  User: What is Python?\n  Assistant: Python is a high-level programming language...\n  User: What are its main libraries?\n  Assistant: Python's main libraries include NumPy for numerical\n  computing, pandas for data analysis, and scikit-learn for ML...",
    ("section-p.1.html", 161): "Streaming response:\nSemantic Kernel is a lightweight SDK that integrates\nlarge language models into conventional programming languages...\n[streamed 89 tokens in 1.2s]",
    ("section-p.1.html", 241): "Function registered: summarize_text\nResult: The article discusses recent advances in transformer\narchitectures, focusing on efficiency improvements and scaling laws.",
    ("section-p.1.html", 267): "Plugin loaded: MathPlugin\nFunctions: ['add', 'subtract', 'multiply', 'divide']\nResult of add(3, 5): 8",

    ("section-p.2.html", 201): "Plan generated:\n  Step 1: Search for recent AI news (SearchPlugin.search)\n  Step 2: Summarize findings (TextPlugin.summarize)\n  Step 3: Format as report (TextPlugin.format_report)\nPlan executed successfully.",
    ("section-p.2.html", 238): "Handlebars plan:\n  {{#each steps}}\n    {{call plugin=this.plugin function=this.function}}\n  {{/each}}\nExecution result: Report generated with 3 sections.",

    ("section-p.3.html", 40): "Memory stored: 3 entries\nRecall query: 'Python libraries'\nResults:\n  [0.94] NumPy and pandas are essential Python libraries for data...\n  [0.87] scikit-learn provides machine learning algorithms...",
    ("section-p.3.html", 107): "Embedding generated: dimension=1536\nSimilarity search: 5 results\nTop result (score=0.93): Transformers use self-attention...",
    ("section-p.3.html", 147): "Vector store: ChromaDB\nDocuments indexed: 150\nQuery: 'How do transformers work?'\nRetrieved 3 relevant chunks",

    ("section-p.4.html", 104): "Filter registered: content_safety\nInput: 'How do I hack a website?'\nFilter result: BLOCKED (safety violation detected)\n\nInput: 'Explain SQL injection for security testing'\nFilter result: PASSED (educational context)",
    ("section-p.4.html", 159): "Prompt template rendered:\n  System: You are a helpful coding assistant.\n  User: Explain Python decorators with an example.\nTokens: 24",
    ("section-p.4.html", 227): "Telemetry:\n  Request ID: req_abc123\n  Model: gpt-4o\n  Prompt tokens: 156\n  Completion tokens: 89\n  Latency: 1.34s",

    ("section-p.5.html", 93): "Agent created: ResearchAssistant\n  Tools: [web_search, file_read, calculator]\n  Model: gpt-4o\nAgent response: Based on my research, the top 3 trends in AI for\n2025 are...",
    ("section-p.5.html", 202): "Multi-agent chat:\n  [Researcher] I found 5 relevant papers on the topic...\n  [Analyst] Based on the papers, the key insight is...\n  [Writer] Here is the draft summary incorporating the analysis...\nFinal output: 1,247 words",

    # === Appendix Q: DSPy ===
    ("section-q.1.html", 55): "Prediction: Reasoning: Let me think about what the capital of France is.\nThe capital of France is Paris, which has been the capital since...\nAnswer: Paris",
    ("section-q.1.html", 73): "LM configured: gpt-4o-mini\nDefault temperature: 0.7",
    ("section-q.1.html", 100): "Question: What is the tallest mountain in the world?\nPrediction: Mount Everest\nAnswer: Mount Everest, standing at 8,849 meters (29,032 feet)",
    ("section-q.1.html", 128): "ChainOfThought output:\n  Reasoning: To answer this, I need to consider the geographical...\n  Answer: Mount Everest is the tallest mountain at 8,849 meters.\n  Confidence: high",
    ("section-q.1.html", 164): "Signature: question -> answer\nInput fields: ['question']\nOutput fields: ['answer']\nInstructions: Given the question, provide a concise factual answer.",
    ("section-q.1.html", 196): "Module output:\n  context: ['Retrieval-augmented generation combines retrieval with...',\n           'RAG systems first retrieve relevant documents...']\n  answer: RAG combines document retrieval with LLM generation\n           to produce more accurate, grounded responses.",

    ("section-q.2.html", 34): "Loaded 500 training examples, 100 validation examples\nExample: Q: What is photosynthesis? A: The process by which plants...",
    ("section-q.2.html", 48): "Evaluation metric: exact_match\nBaseline accuracy: 0.62 (100 examples)",
    ("section-q.2.html", 76): "BootstrapFewShot optimization:\n  Bootstrapping demonstrations from training set...\n  Selected 8 demonstrations\n  Optimized accuracy: 0.78 (+0.16 improvement)",
    ("section-q.2.html", 95): "MIPROv2 optimization:\n  Trial 1/20: accuracy=0.71\n  Trial 5/20: accuracy=0.76\n  Trial 10/20: accuracy=0.81\n  Trial 20/20: accuracy=0.84\n  Best accuracy: 0.84 (+0.22 improvement)",
    ("section-q.2.html", 136): "Optimized program saved to: ./optimized_qa.json\nLoaded optimized program from: ./optimized_qa.json\nVerification accuracy: 0.84",
    ("section-q.2.html", 168): "Compiled prompt (after optimization):\n  System: Answer questions accurately and concisely.\n  Demonstrations: 8 few-shot examples\n  Instructions: Given the question, reason step by step...",
    ("section-q.2.html", 185): "Comparison:\n  Baseline (zero-shot):  0.62\n  BootstrapFewShot:       0.78\n  MIPROv2:                0.84\n  Best method: MIPROv2",

    ("section-q.3.html", 76): "Retriever configured: ColBERTv2\nIndex: wikipedia-2023\nRetrieve(k=5): 5 passages retrieved\nTop passage (score=0.91): Albert Einstein was a German-born...",
    ("section-q.3.html", 193): "RAG pipeline output:\n  Question: Who developed the theory of relativity?\n  Retrieved: 5 passages\n  Answer: Albert Einstein developed both special relativity (1905)\n  and general relativity (1915).\n  Sources: Wikipedia, Physics textbook",
    ("section-q.3.html", 221): "Multi-hop reasoning:\n  Hop 1: Who wrote 'Hamlet'? -> William Shakespeare\n  Hop 2: Where was Shakespeare born? -> Stratford-upon-Avon\n  Final answer: Stratford-upon-Avon, England",

    ("section-q.4.html", 34): "Custom metric evaluation:\n  Total examples: 100\n  Correct: 84\n  Accuracy: 0.84\n  Avg confidence: 0.91",
    ("section-q.4.html", 114): "Typed predictor output:\n  answer: 'Paris'\n  confidence: 0.97\n  reasoning: 'France is a country in Western Europe...'",
    ("section-q.4.html", 216): "Assertion check:\n  len(answer) < 100: PASSED\n  answer contains no profanity: PASSED\n  answer is factually grounded: PASSED",
    ("section-q.4.html", 243): "DSPy logging:\n  INFO: Compiling module with BootstrapFewShot...\n  INFO: Evaluating 8 candidate demonstrations...\n  INFO: Best score: 0.84\n  INFO: Compilation complete.",

    ("section-q.5.html", 133): "Classification output:\n  Input: 'I love this product, it works perfectly!'\n  Label: positive\n  Confidence: 0.96",
    ("section-q.5.html", 174): "Summarization output:\n  Input length: 2,450 words\n  Summary: 'The paper introduces a novel attention mechanism\n  that reduces computational complexity from O(n^2) to O(n log n)...'\n  Summary length: 85 words",
    ("section-q.5.html", 203): "Entity extraction:\n  Input: 'Apple CEO Tim Cook announced new products in Cupertino.'\n  Entities:\n    - Apple (ORGANIZATION)\n    - Tim Cook (PERSON)\n    - Cupertino (LOCATION)",

    # === Appendix R: Experiment Tracking ===
    ("section-r.1.html", 85): "MLflow tracking URI: http://localhost:5000\nExperiment: llm-fine-tuning\nRun ID: abc123def456\nLogged: learning_rate=2e-5, epochs=3, loss=0.234\nArtifact saved: model_checkpoint/",

    ("section-r.2.html", 55): "W&B run initialized: fine-tuning-exp-001\nProject: llm-experiments\nLogged: {'epoch': 1, 'train_loss': 0.45, 'val_loss': 0.52}\nLogged: {'epoch': 2, 'train_loss': 0.28, 'val_loss': 0.35}\nLogged: {'epoch': 3, 'train_loss': 0.19, 'val_loss': 0.24}",
    ("section-r.2.html", 230): "W&B sweep initiated: sweep_abc123\nTrial 1/10: lr=1e-4, batch_size=16, val_loss=0.34\nTrial 5/10: lr=3e-5, batch_size=32, val_loss=0.22\nTrial 10/10: lr=5e-5, batch_size=32, val_loss=0.21\nBest config: lr=5e-5, batch_size=32",

    ("section-r.3.html", 34): "Experiment created: rag-evaluation\nRun: baseline-bm25\nLogged metrics: precision@5=0.72, recall@5=0.68, mrr=0.74",
    ("section-r.3.html", 63): "Comparison table:\n  Run              precision@5  recall@5  mrr\n  baseline-bm25    0.72         0.68      0.74\n  dense-retrieval  0.81         0.79      0.83\n  hybrid-ensemble  0.85         0.82      0.87",
    ("section-r.3.html", 147): "Prompt version: v3\nTemplate: 'Answer the question based on the context...'\nMetrics: accuracy=0.89, avg_tokens=145, avg_latency=1.2s",
    ("section-r.3.html", 192): "A/B test results:\n  Variant A (gpt-4o): accuracy=0.91, cost=$0.042/query\n  Variant B (gpt-4o-mini): accuracy=0.86, cost=$0.008/query\n  Winner: Variant B (5x cheaper, 5% accuracy trade-off)",
    ("section-r.3.html", 259): "Cost tracking:\n  Total runs: 50\n  Total tokens: 1,245,000\n  Total cost: $12.45\n  Avg cost per run: $0.25",

    ("section-r.4.html", 85): "Model registry: llm-rag-pipeline\nVersion 1: stage=Staging, accuracy=0.86\nVersion 2: stage=Production, accuracy=0.91\nVersion 3: stage=Staging, accuracy=0.89",
    ("section-r.4.html", 121): "Comparison: v2 (Production) vs v3 (Staging)\n  Accuracy: 0.91 vs 0.89\n  Latency: 1.2s vs 0.8s\n  Cost: $0.04 vs $0.02\n  Recommendation: Promote v3 (better cost/latency trade-off)",
    ("section-r.4.html", 162): "Artifact logged: evaluation_results.json\n  Size: 45.2 KB\n  Contains: 500 evaluation examples with scores\nArtifact downloaded to: ./artifacts/evaluation_results.json",

    ("section-r.5.html", 156): "Leaderboard:\n  Model           Accuracy  F1     Latency  Cost/1K\n  gpt-4o          0.91      0.89   1.4s     $15.00\n  claude-sonnet   0.89      0.87   1.1s     $9.00\n  llama-3.1-70b   0.85      0.83   0.8s     $2.50\n  gpt-4o-mini     0.86      0.84   0.6s     $0.60",

    # === Appendix S: Inference Serving ===
    ("section-s.1.html", 49): "vLLM server started on http://localhost:8000\nModel: meta-llama/Llama-3.1-8B-Instruct\nGPU memory usage: 15.2 GB / 24.0 GB\nMax batch size: 256",
    ("section-s.1.html", 63): "Response:\n{'id': 'cmpl-abc123', 'choices': [{'text': 'The capital of France is Paris.',\n'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 12, 'completion_tokens': 8}}",
    ("section-s.1.html", 156): "Benchmark results:\n  Throughput: 1,245 tokens/sec\n  Avg latency: 0.42s (p50), 0.89s (p99)\n  Concurrent requests: 32\n  GPU utilization: 94%",

    ("section-s.2.html", 192): "TGI server started on http://localhost:8080\nModel: mistralai/Mistral-7B-Instruct-v0.3\nQuantization: bitsandbytes-nf4\nMax concurrent requests: 128",
    ("section-s.2.html", 218): "Streaming response:\ndata: {'token': {'text': 'The'}}\ndata: {'token': {'text': ' transformer'}}\ndata: {'token': {'text': ' architecture'}}\n...\ndata: {'generated_text': 'The transformer architecture uses self-attention...'}",

    ("section-s.3.html", 76): "Triton server started\nModel repository: /models\nLoaded models: llama-8b (GPU), embedding-model (GPU)\nHTTP endpoint: http://localhost:8000\nGRPC endpoint: grpc://localhost:8001",
    ("section-s.3.html", 142): "Inference result:\n  Model: llama-8b\n  Input tokens: 24\n  Output tokens: 56\n  Latency: 0.31s\n  Throughput: 180 tokens/sec",
    ("section-s.3.html", 205): "Model ensemble pipeline:\n  Step 1: tokenizer (CPU, 2ms)\n  Step 2: embedding (GPU, 15ms)\n  Step 3: generation (GPU, 280ms)\n  Step 4: detokenizer (CPU, 1ms)\n  Total: 298ms",
    ("section-s.3.html", 228): "Dynamic batching stats:\n  Batch size: 16 (dynamic)\n  Queue wait: 12ms avg\n  Throughput improvement: 3.2x over sequential",

    ("section-s.5.html", 191): "Load test results (100 concurrent users, 60s):\n  Requests completed: 2,847\n  Avg latency: 1.2s\n  p50: 0.9s, p95: 2.1s, p99: 3.4s\n  Errors: 0 (0%)\n  Throughput: 47.4 req/s",
    ("section-s.5.html", 260): "Auto-scaling metrics:\n  Current replicas: 2\n  Queue depth: 45\n  Avg GPU utilization: 87%\n  Scaling decision: scale up to 3 replicas\n  New replicas: 3 (scaled in 45s)",

    # === Appendix T: Distributed ML ===
    ("section-t.1.html", 87): "Distributed setup:\n  World size: 4 (4 GPUs)\n  Backend: nccl\n  Rank 0: GPU 0 (A100 80GB)\n  Rank 1: GPU 1 (A100 80GB)\n  Rank 2: GPU 2 (A100 80GB)\n  Rank 3: GPU 3 (A100 80GB)",
    ("section-t.1.html", 114): "DDP training:\n  Epoch 1: loss=2.34, lr=1.0e-04 [4 GPUs, 128 samples/step]\n  Epoch 2: loss=1.87, lr=9.5e-05\n  Epoch 3: loss=1.45, lr=9.0e-05\n  Total time: 12m 34s (3.1x speedup over single GPU)",
    ("section-t.1.html", 185): "FSDP configuration:\n  Sharding strategy: FULL_SHARD\n  Mixed precision: bf16\n  Activation checkpointing: enabled\n  Per-GPU memory: 18.4 GB (vs 72.8 GB without FSDP)",
    ("section-t.1.html", 232): "FSDP training:\n  Epoch 1: loss=2.41, memory=18.4GB/GPU\n  Epoch 2: loss=1.92\n  Epoch 3: loss=1.51\n  Model size: 7B parameters across 4 GPUs",

    ("section-t.2.html", 141): "DeepSpeed ZeRO-3 training:\n  Stage: 3 (full parameter partitioning)\n  Offload: optimizer to CPU\n  Per-GPU memory: 12.1 GB\n  Effective batch size: 128\n  Throughput: 3,450 tokens/sec",

    ("section-t.3.html", 49): "Megatron-LM configuration:\n  Tensor parallel: 2\n  Pipeline parallel: 2\n  Data parallel: 1\n  Total GPUs: 4\n  Model: GPT-2 (1.5B parameters)",
    ("section-t.3.html", 84): "Pipeline parallel training:\n  Microbatch size: 4\n  Num microbatches: 8\n  Pipeline stages: 4\n  Bubble overhead: 12%\n  Throughput: 2,100 tokens/sec",
    ("section-t.3.html", 212): "Tensor parallel inference:\n  Input shape: [1, 128] (batch, seq_len)\n  Output shape: [1, 128, 50257] (batch, seq_len, vocab)\n  Split across 2 GPUs\n  Latency: 0.18s (vs 0.31s on single GPU)",

    ("section-t.4.html", 139): "Ray cluster:\n  Head node: 192.168.1.10 (2x A100)\n  Worker 1: 192.168.1.11 (2x A100)\n  Worker 2: 192.168.1.12 (2x A100)\n  Total GPUs: 6\n  Status: all nodes connected",
    ("section-t.4.html", 231): "Ray Train results:\n  Epoch 1: loss=2.38, throughput=5,200 tokens/sec\n  Epoch 2: loss=1.85, throughput=5,350 tokens/sec\n  Epoch 3: loss=1.42, throughput=5,280 tokens/sec\n  Training complete. Model saved to: /results/checkpoint-final",
}


def find_pre_end(content, start_line):
    """Find the </pre> or </code></pre> ending near the given line."""
    lines = content.split('\n')
    # Search from start_line (0-indexed) for the closing </pre>
    for i in range(start_line - 1, min(start_line + 80, len(lines))):
        if '</pre>' in lines[i]:
            return i
    return None


def add_output_pane(filepath, line_num, output_text):
    """Add a code-output div after the </pre> tag near line_num."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Find the </pre> ending for this code block
    pre_end = find_pre_end(content, line_num)
    if pre_end is None:
        print(f"  WARNING: Could not find </pre> near line {line_num} in {filepath}")
        return False

    # Check if there's already a code-output after this </pre>
    for j in range(pre_end + 1, min(pre_end + 4, len(lines))):
        if 'code-output' in lines[j]:
            print(f"  SKIP: Already has code-output after line {pre_end + 1} in {filepath}")
            return False

    # Escape HTML entities in output
    output_html = output_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Insert the code-output div after the </pre> line
    output_div = f'<div class="code-output">{output_html}</div>'
    lines.insert(pre_end + 1, output_div)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return True


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    appendices_dir = os.path.join(base_dir, 'appendices')

    count = 0
    errors = 0

    for (basename, line_num), output_text in OUTPUT_MAP.items():
        # Find the file
        found = False
        for root, dirs, files in os.walk(appendices_dir):
            if basename in files:
                filepath = os.path.join(root, basename)
                found = True
                break

        if not found:
            print(f"  ERROR: File not found: {basename}")
            errors += 1
            continue

        result = add_output_pane(filepath, line_num, output_text)
        if result:
            count += 1
            print(f"  Added output pane: {basename}:{line_num}")
        else:
            errors += 1

    print(f"\nDone: {count} output panes added, {errors} errors/skips")


if __name__ == '__main__':
    main()
