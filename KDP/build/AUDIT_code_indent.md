# Code-block indent / formatting audit (detail2)

Scope: `<pre><code>` blocks under `part-*`, `appendices/`, `front-matter/`, `capstone/`.

## Summary

- Files scanned: **366**
- Code blocks scanned: **1523**
- Code blocks with at least one issue: **776**
- Individual issue rows: **953**

### Counts by category

| Category | Count |
|---|---|
| `WIDE_LINE` | 614 |
| `PYTHON_NO_BODY_INDENT` | 216 |
| `INCONSISTENT_INDENT` | 123 |

### Top 20 files by issue count

| File | Issues |
|---|---|
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 11 |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 11 |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 10 |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 9 |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 9 |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 9 |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 8 |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 8 |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 8 |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 8 |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 8 |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 8 |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 7 |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 7 |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 7 |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 7 |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 7 |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 7 |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 7 |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 7 |

## Sample issues per category

### WIDE_LINE  (614 total)

| File | Approx line | Lang | Detail | First non-blank line |
|---|---|---|---|---|
| `appendices/appendix-a-mathematical-foundations/section-a.6.html` | 188 | `python` | 2 line(s) > 80 chars (max 89) | `# Entropy, cross-entropy, and perplexity from scratch with NumPy.` |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 121 | `python` | 1 line(s) > 80 chars (max 102) | `# BLEU + ROUGE with Hugging Face evaluate library.` |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 186 | `python` | 1 line(s) > 80 chars (max 81) | `# PyTorch implementation` |
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 50 | `python` | 1 line(s) > 80 chars (max 86) | `# PyTorch implementation` |
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 217 | `python` | 1 line(s) > 80 chars (max 89) | `# pip install sentence-transformers` |
| `appendices/appendix-c-python-for-llm/section-c.2.html` | 55 | `bash` | 1 line(s) > 80 chars (max 83) | `# Create an environment with a specific Python version` |
| `appendices/appendix-c-python-for-llm/section-c.4.html` | 50 | `python` | 4 line(s) > 80 chars (max 96) | `# Most modern models use chat templates` |
| `appendices/appendix-c-python-for-llm/section-c.4.html` | 74 | `python` | 1 line(s) > 80 chars (max 93) | `# implement tokenize_fn` |
| `appendices/appendix-d-environment-setup/section-d.3.html` | 35 | `text` | 1 line(s) > 80 chars (max 83) | `# Install Miniconda (lightweight Conda distribution)` |
| `appendices/appendix-d-environment-setup/section-d.3.html` | 44 | `bash` | 1 line(s) > 80 chars (max 91) | `# Requires system Python 3.10+ and CUDA toolkit already installed` |
| `appendices/appendix-d-environment-setup/section-d.3.html` | 55 | `bash` | 1 line(s) > 80 chars (max 91) | `# Standard Python venv + pip path; works on every platform.` |
| `appendices/appendix-d-environment-setup/section-d.4.html` | 33 | `bash` | 1 line(s) > 80 chars (max 114) | `# Core Hugging Face ecosystem` |
| `appendices/appendix-d-environment-setup/section-d.6.html` | 33 | `python` | 2 line(s) > 80 chars (max 88) | `"""` |
| `appendices/appendix-e-git-collaboration/section-e.4.html` | 50 | `python` | 1 line(s) > 80 chars (max 81) | `# PyTorch implementation` |
| `appendices/appendix-j-datasets-benchmarks/section-j.1.html` | 93 | `python` | 1 line(s) > 80 chars (max 92) | `# Stream FineWeb-Edu without downloading the full 1.3 trillion token dataset.` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.1.html` | 140 | `python` | 3 line(s) > 80 chars (max 93) | `from transformers import (` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 301 | `python` | 1 line(s) > 80 chars (max 88) | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.4.html` | 54 | `python` | 1 line(s) > 80 chars (max 81) | `from transformers import AutoModelForCausalLM, AutoTokenizer` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.4.html` | 216 | `python` | 1 line(s) > 80 chars (max 91) | `from trl import DPOTrainer, DPOConfig` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.4.html` | 307 | `python` | 2 line(s) > 80 chars (max 83) | `from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 129 | `python` | 4 line(s) > 80 chars (max 86) | `from huggingface_hub import ModelCard, ModelCardData` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 296 | `python` | 1 line(s) > 80 chars (max 85) | `# Create and deploy a Space from the command line` |
| `appendices/appendix-l-langchain/section-l.1.html` | 41 | `python` | 1 line(s) > 80 chars (max 82) | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.1.html` | 75 | `python` | 1 line(s) > 80 chars (max 81) | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.2.html` | 78 | `python` | 1 line(s) > 80 chars (max 83) | `from langchain.memory import ConversationSummaryMemory` |
| `appendices/appendix-l-langchain/section-l.3.html` | 41 | `python` | 1 line(s) > 80 chars (max 100) | `from langchain_community.document_loaders import (` |
| `appendices/appendix-l-langchain/section-l.3.html` | 112 | `python` | 1 line(s) > 80 chars (max 83) | `from langchain_text_splitters import (` |
| `appendices/appendix-l-langchain/section-l.3.html` | 171 | `python` | 1 line(s) > 80 chars (max 84) | `from langchain_openai import OpenAIEmbeddings` |
| `appendices/appendix-l-langchain/section-l.4.html` | 94 | `python` | 1 line(s) > 80 chars (max 86) | `from pydantic import BaseModel, Field` |
| `appendices/appendix-l-langchain/section-l.4.html` | 188 | `python` | 1 line(s) > 80 chars (max 124) | `from langchain.output_parsers import OutputFixingParser` |

### PYTHON_NO_BODY_INDENT  (216 total)

| File | Approx line | Lang | Detail | First non-blank line |
|---|---|---|---|---|
| `appendices/appendix-a-mathematical-foundations/section-a.3.html` | 58 | `python` | body of opener 'with torch.no_grad():' drops to opener indent at line 16 | `# Simplified gradient descent in PyTorch` |
| `appendices/appendix-a-mathematical-foundations/section-a.4.html` | 50 | `python` | body of opener 'def entropy(probs):' drops to opener indent at line 10 | `# implement entropy` |
| `appendices/appendix-a-mathematical-foundations/section-a.6.html` | 188 | `python` | body of opener 'def entropy(probs):' drops to opener indent at line 7 | `# Entropy, cross-entropy, and perplexity from scratch with NumPy.` |
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 50 | `python` | body of opener 'if torch.cuda.is_available():' drops to opener indent at line 11 | `# PyTorch implementation` |
| `appendices/appendix-c-python-for-llm/section-c.4.html` | 74 | `python` | body of opener 'def tokenize_fn(examples):' drops to opener indent at line 12 | `# implement tokenize_fn` |
| `appendices/appendix-d-environment-setup/section-d.6.html` | 33 | `python` | body of opener 'for lib in ["datasets", "peft", "trl", "' drops to opener indent at line 51 | `"""` |
| `appendices/appendix-j-datasets-benchmarks/section-j.1.html` | 93 | `python` | body of opener 'for i, example in enumerate(high_quality' drops to opener indent at line 22 | `# Stream FineWeb-Edu without downloading the full 1.3 trillion token dataset.` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.1.html` | 44 | `python` | body of opener 'for ent in entities:' drops to opener indent at line 15 | `from transformers import pipeline` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.1.html` | 83 | `python` | body of opener 'with torch.no_grad():' drops to opener indent at line 18 | `from transformers import AutoTokenizer, AutoModelForSequenceClassification` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 88 | `python` | body of opener 'for i, example in enumerate(stream):' drops to opener indent at line 18 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 98 | `python` | body of opener 'def tokenize_fn(examples):' drops to opener indent at line 16 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 247 | `python` | body of opener 'def preprocess_classification(examples):' drops to opener indent at line 10 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 265 | `python` | body of opener 'def align_labels(examples):' drops to opener indent at line 30 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 301 | `python` | body of opener 'def preprocess_qa(examples):' drops to opener indent at line 52 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 107 | `python` | body of opener 'def tokenize_fn(examples):' drops to opener indent at line 17 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 108 | `python` | body of opener 'class LRLoggingCallback(TrainerCallback)' drops to opener indent at line 12 | `from transformers import TrainerCallback, EarlyStoppingCallback` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 224 | `python` | body of opener 'for step, batch in enumerate(train_loade' drops to opener indent at line 62 | `from accelerate import Accelerator` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 364 | `python` | body of opener 'def compute_metrics(eval_pred):' drops to opener indent at line 28 | `import evaluate` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 44 | `python` | body of opener 'for m in models:' drops to opener indent at line 25 | `from huggingface_hub import (` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 253 | `python` | body of opener 'def generate_text(prompt, max_tokens, te' drops to opener indent at line 22 | `# File: app.py (this file goes in your Space repository)` |
| `appendices/appendix-l-langchain/section-l.1.html` | 75 | `python` | body of opener 'for chunk in model.stream([HumanMessage(' drops to opener indent at line 9 | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.1.html` | 245 | `python` | body of opener 'def mock_retriever(query: dict) -> str:' drops to opener indent at line 8 | `from langchain_core.runnables import RunnablePassthrough, RunnableParallel` |
| `appendices/appendix-l-langchain/section-l.2.html` | 112 | `python` | body of opener 'for i in range(10):' drops to opener indent at line 18 | `from langchain.memory import ConversationTokenBufferMemory` |
| `appendices/appendix-l-langchain/section-l.2.html` | 142 | `python` | body of opener 'def get_session_history(session_id: str)' drops to opener indent at line 15 | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.2.html` | 201 | `python` | body of opener 'def get_session_history(session_id: str)' drops to opener indent at line 10 | `from langchain_community.chat_message_histories import RedisChatMessageHistory` |
| `appendices/appendix-l-langchain/section-l.3.html` | 112 | `python` | body of opener 'class DataProcessor:' drops to opener indent at line 29 | `from langchain_text_splitters import (` |
| `appendices/appendix-l-langchain/section-l.3.html` | 268 | `python` | body of opener 'def format_docs(docs):' drops to opener indent at line 35 | `from langchain_openai import ChatOpenAI, OpenAIEmbeddings` |
| `appendices/appendix-l-langchain/section-l.4.html` | 45 | `python` | body of opener 'class TicketClassification(BaseModel):' drops to opener indent at line 20 | `from pydantic import BaseModel, Field` |
| `appendices/appendix-l-langchain/section-l.4.html` | 94 | `python` | body of opener 'class DocumentAnalysis(BaseModel):' drops to opener indent at line 21 | `from pydantic import BaseModel, Field` |
| `appendices/appendix-l-langchain/section-l.4.html` | 131 | `python` | body of opener 'class Recipe(BaseModel):' drops to opener indent at line 12 | `from langchain_core.output_parsers import PydanticOutputParser` |

### INCONSISTENT_INDENT  (123 total)

| File | Approx line | Lang | Detail | First non-blank line |
|---|---|---|---|---|
| `appendices/appendix-a-mathematical-foundations/section-a.6.html` | 188 | `python` | structural indent widths suspect: [1] | `# Entropy, cross-entropy, and perplexity from scratch with NumPy.` |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 121 | `python` | structural indent widths suspect: [15] | `# BLEU + ROUGE with Hugging Face evaluate library.` |
| `appendices/appendix-l-langchain/section-l.5.html` | 106 | `python` | structural indent widths suspect: [4, 15] | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-r-experiment-tracking/section-r.3.html` | 65 | `python` | structural indent widths suspect: [4, 5] | `import mlflow` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html` | 97 | `python` | structural indent widths suspect: [1] | `# ReLU and softmax from scratch: ReLU zeros out negatives,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 316 | `python` | structural indent widths suspect: [1] | `# Load FashionMNIST with torchvision, apply normalization,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 429 | `python` | structural indent widths suspect: [1] | `# Save model weights` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 460 | `python` | structural indent widths suspect: [1] | `# Check gradients after a backward pass` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 472 | `python` | structural indent widths suspect: [1] | `# Register a forward hook that prints the output shape` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 790 | `python` | structural indent widths suspect: [1] | `# Strict mode: fails if any graph break is detected` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 952 | `python` | structural indent widths suspect: [1] | `# Distributed Data Parallel: initialize a process group, wrap the model,` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 105 | `python` | structural indent widths suspect: [1] | `# Complete text preprocessing pipeline` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.1.html` | 407 | `python` | structural indent widths suspect: [1] | `# How code gets tokenized (using tiktoken)` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.2.html` | 288 | `python` | structural indent widths suspect: [1] | `# Luong (dot-product) attention: score = decoder_state @ encoder_outputs^T.` |
| `part-1-foundations/module-04-transformer-architecture/section-4.1.html` | 653 | `python` | structural indent widths suspect: [1] | `# Build a causal (lower-triangular) boolean mask that blocks each token` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 111 | `python` | structural indent widths suspect: [1] | `"""` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 454 | `python` | structural indent widths suspect: [4, 8, 12, 13] | `# Weight initialization + autoregressive text generation for our mini-Transforme` |
| `part-1-foundations/module-04-transformer-architecture/section-4.3.html` | 204 | `python` | structural indent widths suspect: [1] | `# Rotary Position Embedding (RoPE): rotate pairs of dimensions by` |
| `part-1-foundations/module-04-transformer-architecture/section-4.3.html` | 457 | `python` | structural indent widths suspect: [1] | `# Simplified Differential Attention (conceptual)` |
| `part-1-foundations/module-04-transformer-architecture/section-4.4.html` | 267 | `python` | structural indent widths suspect: [1] | `# Triton fused softmax kernel: compute softmax in a single GPU pass` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 437 | `python` | structural indent widths suspect: [1] | `import numpy as np` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 518 | `python` | structural indent widths suspect: [1] | `import matplotlib.pyplot as plt` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 171 | `python` | structural indent widths suspect: [1] | `# Using the Outlines library for structured generation` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 309 | `python` | structural indent widths suspect: [1] | `# LMQL: declarative constraints on LLM output` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 699 | `python` | structural indent widths suspect: [1] | `# Structured output with Instructor + Pydantic: force the LLM to return` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html` | 358 | `python` | structural indent widths suspect: [1] | `# Launch readiness checklist generator` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 106 | `python` | structural indent widths suspect: [1] | `# Stress-test a product hypothesis using an LLM as devil's advocate` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 149 | `python` | structural indent widths suspect: [1] | `# Generate acceptance criteria from a feature description` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 204 | `python` | structural indent widths suspect: [1] | `# Meta-prompting: use an LLM to critique and improve a draft prompt` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 249 | `python` | structural indent widths suspect: [1] | `# Summarize evaluation failures and suggest next experiments` |

## All issues (flat)

| File | Approx line | Lang | Category | Detail | First line |
|---|---|---|---|---|---|
| `appendices/appendix-a-mathematical-foundations/section-a.3.html` | 58 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'with torch.no_grad():' drops to opener indent at line 16 | `# Simplified gradient descent in PyTorch` |
| `appendices/appendix-a-mathematical-foundations/section-a.4.html` | 50 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def entropy(probs):' drops to opener indent at line 10 | `# implement entropy` |
| `appendices/appendix-a-mathematical-foundations/section-a.6.html` | 188 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Entropy, cross-entropy, and perplexity from scratch with NumPy.` |
| `appendices/appendix-a-mathematical-foundations/section-a.6.html` | 188 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def entropy(probs):' drops to opener indent at line 7 | `# Entropy, cross-entropy, and perplexity from scratch with NumPy.` |
| `appendices/appendix-a-mathematical-foundations/section-a.6.html` | 188 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `# Entropy, cross-entropy, and perplexity from scratch with NumPy.` |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 121 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [15] | `# BLEU + ROUGE with Hugging Face evaluate library.` |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 121 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 102) | `# BLEU + ROUGE with Hugging Face evaluate library.` |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 186 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# PyTorch implementation` |
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 50 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'if torch.cuda.is_available():' drops to opener indent at line 11 | `# PyTorch implementation` |
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 50 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `# PyTorch implementation` |
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 217 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `# pip install sentence-transformers` |
| `appendices/appendix-c-python-for-llm/section-c.2.html` | 55 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Create an environment with a specific Python version` |
| `appendices/appendix-c-python-for-llm/section-c.4.html` | 50 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 96) | `# Most modern models use chat templates` |
| `appendices/appendix-c-python-for-llm/section-c.4.html` | 74 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def tokenize_fn(examples):' drops to opener indent at line 12 | `# implement tokenize_fn` |
| `appendices/appendix-c-python-for-llm/section-c.4.html` | 74 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 93) | `# implement tokenize_fn` |
| `appendices/appendix-d-environment-setup/section-d.3.html` | 35 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Install Miniconda (lightweight Conda distribution)` |
| `appendices/appendix-d-environment-setup/section-d.3.html` | 44 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 91) | `# Requires system Python 3.10+ and CUDA toolkit already installed` |
| `appendices/appendix-d-environment-setup/section-d.3.html` | 55 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 91) | `# Standard Python venv + pip path; works on every platform.` |
| `appendices/appendix-d-environment-setup/section-d.4.html` | 33 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 114) | `# Core Hugging Face ecosystem` |
| `appendices/appendix-d-environment-setup/section-d.6.html` | 33 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for lib in ["datasets", "peft", "trl", "' drops to opener indent at line 51 | `"""` |
| `appendices/appendix-d-environment-setup/section-d.6.html` | 33 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 88) | `"""` |
| `appendices/appendix-e-git-collaboration/section-e.4.html` | 50 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# PyTorch implementation` |
| `appendices/appendix-j-datasets-benchmarks/section-j.1.html` | 93 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for i, example in enumerate(high_quality' drops to opener indent at line 22 | `# Stream FineWeb-Edu without downloading the full 1.3 trillion token dataset.` |
| `appendices/appendix-j-datasets-benchmarks/section-j.1.html` | 93 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `# Stream FineWeb-Edu without downloading the full 1.3 trillion token dataset.` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.1.html` | 44 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for ent in entities:' drops to opener indent at line 15 | `from transformers import pipeline` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.1.html` | 83 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'with torch.no_grad():' drops to opener indent at line 18 | `from transformers import AutoTokenizer, AutoModelForSequenceClassification` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.1.html` | 140 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 93) | `from transformers import (` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 88 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for i, example in enumerate(stream):' drops to opener indent at line 18 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 98 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def tokenize_fn(examples):' drops to opener indent at line 16 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 247 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def preprocess_classification(examples):' drops to opener indent at line 10 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 265 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def align_labels(examples):' drops to opener indent at line 30 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 301 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def preprocess_qa(examples):' drops to opener indent at line 52 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.2.html` | 301 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 107 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def tokenize_fn(examples):' drops to opener indent at line 17 | `from datasets import load_dataset` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 108 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class LRLoggingCallback(TrainerCallback)' drops to opener indent at line 12 | `from transformers import TrainerCallback, EarlyStoppingCallback` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 224 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for step, batch in enumerate(train_loade' drops to opener indent at line 62 | `from accelerate import Accelerator` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.3.html` | 364 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def compute_metrics(eval_pred):' drops to opener indent at line 28 | `import evaluate` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.4.html` | 54 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `from transformers import AutoModelForCausalLM, AutoTokenizer` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.4.html` | 216 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 91) | `from trl import DPOTrainer, DPOConfig` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.4.html` | 307 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 83) | `from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 44 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for m in models:' drops to opener indent at line 25 | `from huggingface_hub import (` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 129 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 86) | `from huggingface_hub import ModelCard, ModelCardData` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 253 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def generate_text(prompt, max_tokens, te' drops to opener indent at line 22 | `# File: app.py (this file goes in your Space repository)` |
| `appendices/appendix-k-huggingface-ecosystem/section-k.5.html` | 296 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Create and deploy a Space from the command line` |
| `appendices/appendix-l-langchain/section-l.1.html` | 41 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.1.html` | 75 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for chunk in model.stream([HumanMessage(' drops to opener indent at line 9 | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.1.html` | 75 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.1.html` | 245 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def mock_retriever(query: dict) -> str:' drops to opener indent at line 8 | `from langchain_core.runnables import RunnablePassthrough, RunnableParallel` |
| `appendices/appendix-l-langchain/section-l.2.html` | 78 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `from langchain.memory import ConversationSummaryMemory` |
| `appendices/appendix-l-langchain/section-l.2.html` | 112 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for i in range(10):' drops to opener indent at line 18 | `from langchain.memory import ConversationTokenBufferMemory` |
| `appendices/appendix-l-langchain/section-l.2.html` | 142 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def get_session_history(session_id: str)' drops to opener indent at line 15 | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.2.html` | 201 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def get_session_history(session_id: str)' drops to opener indent at line 10 | `from langchain_community.chat_message_histories import RedisChatMessageHistory` |
| `appendices/appendix-l-langchain/section-l.3.html` | 41 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 100) | `from langchain_community.document_loaders import (` |
| `appendices/appendix-l-langchain/section-l.3.html` | 112 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class DataProcessor:' drops to opener indent at line 29 | `from langchain_text_splitters import (` |
| `appendices/appendix-l-langchain/section-l.3.html` | 112 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `from langchain_text_splitters import (` |
| `appendices/appendix-l-langchain/section-l.3.html` | 171 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `from langchain_openai import OpenAIEmbeddings` |
| `appendices/appendix-l-langchain/section-l.3.html` | 268 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def format_docs(docs):' drops to opener indent at line 35 | `from langchain_openai import ChatOpenAI, OpenAIEmbeddings` |
| `appendices/appendix-l-langchain/section-l.4.html` | 45 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class TicketClassification(BaseModel):' drops to opener indent at line 20 | `from pydantic import BaseModel, Field` |
| `appendices/appendix-l-langchain/section-l.4.html` | 94 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class DocumentAnalysis(BaseModel):' drops to opener indent at line 21 | `from pydantic import BaseModel, Field` |
| `appendices/appendix-l-langchain/section-l.4.html` | 94 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `from pydantic import BaseModel, Field` |
| `appendices/appendix-l-langchain/section-l.4.html` | 131 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class Recipe(BaseModel):' drops to opener indent at line 12 | `from langchain_core.output_parsers import PydanticOutputParser` |
| `appendices/appendix-l-langchain/section-l.4.html` | 188 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 124) | `from langchain.output_parsers import OutputFixingParser` |
| `appendices/appendix-l-langchain/section-l.4.html` | 234 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class MovieReview(BaseModel):' drops to opener indent at line 13 | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.5.html` | 41 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def calculate(expression: Annotated[str,' drops to opener indent at line 14 | `from langchain_core.tools import tool` |
| `appendices/appendix-l-langchain/section-l.5.html` | 41 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `from langchain_core.tools import tool` |
| `appendices/appendix-l-langchain/section-l.5.html` | 106 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [4, 15] | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-l-langchain/section-l.5.html` | 157 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class LoggingHandler(BaseCallbackHandler' drops to opener indent at line 25 | `from langchain_core.callbacks import BaseCallbackHandler` |
| `appendices/appendix-l-langchain/section-l.5.html` | 157 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `from langchain_core.callbacks import BaseCallbackHandler` |
| `appendices/appendix-l-langchain/section-l.5.html` | 223 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def run_agent(user_input: str, max_steps' drops to opener indent at line 46 | `from langchain_openai import ChatOpenAI` |
| `appendices/appendix-r-experiment-tracking/section-r.1.html` | 78 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for step, batch in enumerate(dataloader)' drops to opener indent at line 13 | `# Training loop with W&B logging` |
| `appendices/appendix-r-experiment-tracking/section-r.1.html` | 107 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for example in eval_examples:' drops to opener indent at line 10 | `# Log a table of model predictions` |
| `appendices/appendix-r-experiment-tracking/section-r.1.html` | 164 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def train():' drops to opener indent at line 33 | `# Define a sweep configuration` |
| `appendices/appendix-r-experiment-tracking/section-r.1.html` | 164 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# Define a sweep configuration` |
| `appendices/appendix-r-experiment-tracking/section-r.2.html` | 54 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for epoch in range(3):' drops to opener indent at line 23 | `import mlflow` |
| `appendices/appendix-r-experiment-tracking/section-r.2.html` | 92 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'with open("predictions.txt", "w") as f:' drops to opener indent at line 18 | `with mlflow.start_run():` |
| `appendices/appendix-r-experiment-tracking/section-r.2.html` | 177 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'with mlflow.start_run():' drops to opener indent at line 13 | `# Log a model to the registry` |
| `appendices/appendix-r-experiment-tracking/section-r.2.html` | 208 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for run in runs:' drops to opener indent at line 21 | `from mlflow import MlflowClient` |
| `appendices/appendix-r-experiment-tracking/section-r.3.html` | 65 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [4, 5] | `import mlflow` |
| `appendices/appendix-r-experiment-tracking/section-r.3.html` | 100 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def train_fn():' drops to opener indent at line 41 | `import wandb` |
| `appendices/appendix-r-experiment-tracking/section-r.3.html` | 147 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def objective(trial):' drops to opener indent at line 25 | `import optuna` |
| `appendices/appendix-r-experiment-tracking/section-r.3.html` | 191 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 82) | `import numpy as np` |
| `appendices/appendix-r-experiment-tracking/section-r.3.html` | 214 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for run_id in run_ids:' drops to opener indent at line 25 | `import matplotlib.pyplot as plt` |
| `appendices/appendix-r-experiment-tracking/section-r.3.html` | 258 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for config in configs:' drops to opener indent at line 20 | `# Automated comparison workflow` |
| `appendices/appendix-r-experiment-tracking/section-r.4.html` | 156 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def validate_and_promote(model_name: str' drops to opener indent at line 39 | `import mlflow` |
| `appendices/appendix-r-experiment-tracking/section-r.4.html` | 156 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 81) | `import mlflow` |
| `appendices/appendix-r-experiment-tracking/section-r.4.html` | 202 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'if accuracy < 0.90:' drops to opener indent at line 56 | `# Example GitHub Actions workflow (YAML) for model deployment` |
| `appendices/appendix-r-experiment-tracking/section-r.4.html` | 202 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Example GitHub Actions workflow (YAML) for model deployment` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 39 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for example in eval_dataset:' drops to opener indent at line 43 | `import wandb` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 103 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for example in eval_dataset[:max_rows]:' drops to opener indent at line 35 | `import wandb` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 103 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `import wandb` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 148 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `import mlflow` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 200 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def generate_response(prompt: str, syste' drops to opener indent at line 34 | `import weave` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 246 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class DriftDetector:' drops to opener indent at line 43 | `import numpy as np` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 246 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `import numpy as np` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 309 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for key, tokens in self.costs.items():' drops to opener indent at line 38 | `import wandb` |
| `appendices/appendix-r-experiment-tracking/section-r.5.html` | 309 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 86) | `import wandb` |
| `appendices/appendix-s-inference-serving/section-s.1.html` | 156 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `from openai import OpenAI` |
| `appendices/appendix-s-inference-serving/section-s.2.html` | 205 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for line in response.iter_lines():' drops to opener indent at line 26 | `import requests` |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 73 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def extract_entity(s, text):' drops to opener indent at line 17 | `import sglang as sgl` |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 73 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 106) | `import sglang as sgl` |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 117 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for i, f in enumerate(forks):' drops to opener indent at line 11 | `@sgl.function` |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 117 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `@sgl.function` |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 137 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def generate_json_record(s, description)' drops to opener indent at line 13 | `@sgl.function` |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 137 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `@sgl.function` |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 226 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def classify_sentiment(s, review):' drops to opener indent at line 9 | `@sgl.function` |
| `appendices/appendix-s-inference-serving/section-s.3.html` | 226 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `@sgl.function` |
| `appendices/appendix-s-inference-serving/section-s.5.html` | 176 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def collect_gpu_metrics():' drops to opener indent at line 31 | `import pynvml` |
| `appendices/appendix-s-inference-serving/section-s.5.html` | 176 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 85) | `import pynvml` |
| `appendices/appendix-s-inference-serving/section-s.5.html` | 246 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'async def send_request(session, prompt):' drops to opener indent at line 48 | `import asyncio` |
| `appendices/appendix-s-inference-serving/section-s.5.html` | 246 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 95) | `import asyncio` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 90 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def detect_lang(text: str) -> str:' drops to opener indent at line 22 | `# Filter to English, require minimum text length and quality score` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 90 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Filter to English, require minimum text length and quality score` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 126 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def sha256_hash(text: str) -> str:' drops to opener indent at line 10 | `import hashlib` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 151 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# --- Near-duplicate removal via MinHash LSH ---` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 200 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def pack_sequences(token_id_lists: pd.Se' drops to opener indent at line 31 | `from pyspark.sql.types import StructType, StructField` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 200 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `from pyspark.sql.types import StructType, StructField` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 235 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def clean_text(texts: pd.Series) -> pd.S' drops to opener indent at line 30 | `import re` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 266 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def tokenize_text(texts: pd.Series) -> p' drops to opener indent at line 27 | `from transformers import AutoTokenizer` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 341 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def embed_texts(texts: pd.Series) -> pd.' drops to opener indent at line 40 | `import torch` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 407 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def upsert_to_pinecone(rows):' drops to opener indent at line 36 | `# Write embeddings to Parquet for offline use` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 473 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# --- Diagnosing and fixing partition skew ---` |
| `appendices/appendix-t-distributed-ml/section-t.1.html` | 518 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# --- Databricks cluster autoscaling configuration (JSON, not Python) ---` |
| `appendices/appendix-t-distributed-ml/section-t.2.html` | 133 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'except Exception as e:' drops to opener indent at line 12 | `# Schema enforcement: this will FAIL because "quality_label" is not in the schem` |
| `appendices/appendix-t-distributed-ml/section-t.2.html` | 133 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Schema enforcement: this will FAIL because "quality_label" is not in the schem` |
| `appendices/appendix-t-distributed-ml/section-t.3.html` | 186 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for epoch in range(3):' drops to opener indent at line 27 | `import mlflow` |
| `appendices/appendix-t-distributed-ml/section-t.3.html` | 235 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 99) | `from databricks.sdk import WorkspaceClient` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 78 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `from composer import Trainer` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 117 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 115) | `from openai import OpenAI` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 142 | `sql` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `-- Classify customer support tickets by category using ai_classify()` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 172 | `sql` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `-- Use ai_query() for custom prompts inside a Delta Live Tables pipeline` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 216 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 122) | `import mlflow` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 376 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def chunk_text(text: str, chunk_size: in' drops to opener indent at line 22 | `from pyspark.sql import SparkSession` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 376 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 92) | `from pyspark.sql import SparkSession` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 420 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class DatabricksRAGChain(mlflow.pyfunc.P' drops to opener indent at line 64 | `import mlflow` |
| `appendices/appendix-t-distributed-ml/section-t.4.html` | 420 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 87) | `import mlflow` |
| `appendices/appendix-t-distributed-ml/section-t.5.html` | 52 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def compute_embeddings(texts, model_name' drops to opener indent at line 13 | `import ray` |
| `appendices/appendix-t-distributed-ml/section-t.5.html` | 52 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `import ray` |
| `appendices/appendix-t-distributed-ml/section-t.5.html` | 89 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def train_fn(config):' drops to opener indent at line 39 | `import ray.train` |
| `appendices/appendix-t-distributed-ml/section-t.5.html` | 164 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def train_fn_deepspeed(config):' drops to opener indent at line 32 | `from ray.train.torch import TorchTrainer` |
| `appendices/appendix-t-distributed-ml/section-t.5.html` | 216 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def tokenize_batch(batch, tokenizer_name' drops to opener indent at line 22 | `import ray.data` |
| `appendices/appendix-t-distributed-ml/section-t.5.html` | 263 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class LLMDeployment:' drops to opener indent at line 20 | `from ray import serve` |
| `appendices/appendix-t-distributed-ml/section-t.6.html` | 225 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `from databricks.feature_engineering import FeatureEngineeringClient, FeatureLook` |
| `appendices/appendix-t-distributed-ml/section-t.7.html` | 69 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `from airflow import DAG` |
| `appendices/appendix-t-distributed-ml/section-t.7.html` | 251 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class GenerationModel:' drops to opener indent at line 20 | `# Kubernetes deployment for multi-model serving with Ray Serve` |
| `appendices/appendix-u-docker-containers/section-u.2.html` | 120 | `bash` | WIDE_LINE | 3 line(s) > 80 chars (max 112) | `# Install the NVIDIA Container Toolkit on Ubuntu` |
| `appendices/appendix-u-docker-containers/section-u.4.html` | 104 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Run Ollama server` |
| `appendices/appendix-v-tooling-ecosystem/section-v.2.html` | 262 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 118) | `from haystack import Pipeline` |
| `appendices/appendix-v-tooling-ecosystem/section-v.2.html` | 309 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class RAG(dspy.Module):' drops to opener indent at line 17 | `import dspy` |
| `appendices/appendix-v-tooling-ecosystem/section-v.3.html` | 60 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class AgentState(TypedDict):' drops to opener indent at line 11 | `from langgraph.graph import StateGraph, END` |
| `appendices/appendix-v-tooling-ecosystem/section-v.3.html` | 60 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 86) | `from langgraph.graph import StateGraph, END` |
| `appendices/appendix-v-tooling-ecosystem/section-v.3.html` | 106 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 91) | `from crewai import Agent, Task, Crew, LLM` |
| `appendices/appendix-v-tooling-ecosystem/section-v.3.html` | 153 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def search(query: str) -> str:' drops to opener indent at line 8 | `from agents import Agent, Runner, function_tool` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html` | 249 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 84) | `# Demonstrating overfitting vs. regularization` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html` | 337 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# K-Fold cross-validation from scratch` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html` | 97 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# ReLU and softmax from scratch: ReLU zeros out negatives,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html` | 97 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def softmax(z):' drops to opener indent at line 12 | `# ReLU and softmax from scratch: ReLU zeros out negatives,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html` | 226 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 94) | `# RobustMLP: a production-style feedforward network with BatchNorm,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html` | 306 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 120) | `# Complete training loop with cosine LR scheduling, gradient clipping,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 316 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Load FashionMNIST with torchvision, apply normalization,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 429 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Save model weights` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 460 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Check gradients after a backward pass` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 460 | `python` | PYTHON_NO_BODY_INDENT | line opens block but next line not indented (1 -> 1); opener: 'if param.grad is not None:' | `# Check gradients after a backward pass` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 472 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Register a forward hook that prints the output shape` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 472 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def print_shape_hook(module, input, outp' drops to opener indent at line 5 | `# Register a forward hook that prints the output shape` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 494 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Profile a few training batches with torch.profiler to identify` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 562 | `python` | WIDE_LINE | 9 line(s) > 80 chars (max 118) | `#!/usr/bin/env python3` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 790 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Strict mode: fails if any graph break is detected` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 952 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Distributed Data Parallel: initialize a process group, wrap the model,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 952 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for batch_x, batch_y in train_loader:' drops to opener indent at line 24 | `# Distributed Data Parallel: initialize a process group, wrap the model,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 1009 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Complete DDP training setup with DistributedSampler` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html` | 191 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 91) | `# REINFORCE algorithm: a policy network outputs action probabilities,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html` | 252 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 103) | `# PPO sketch: collect trajectories, compute advantage estimates,` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html` | 527 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `import numpy as np` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 105 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Complete text preprocessing pipeline` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 105 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def preprocess(text: str) -> list[str]:' drops to opener indent at line 11 | `# Complete text preprocessing pipeline` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 105 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Complete text preprocessing pipeline` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 178 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `# Same pipeline using spaCy (modern, production-grade)` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 283 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Bigrams capture some word order` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 431 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def dist(w1, w2):' drops to opener indent at line 14 | `# One-hot encoding: every word becomes a sparse high-dimensional vector` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html` | 583 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for i, d in enumerate(docs):' drops to opener indent at line 8 | `import numpy as np, math, collections` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html` | 297 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 83) | `# Word analogy: king - man + woman = ?` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html` | 535 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# t-SNE projection: compress 100-dimensional word vectors to 2D` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html` | 194 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 91) | `# Demonstrating contextual embeddings: same word, different vectors` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html` | 446 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def embed(sentence, target_word):' drops to opener indent at line 8 | `from transformers import AutoTokenizer, AutoModel` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html` | 446 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 112) | `from transformers import AutoTokenizer, AutoModel` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html` | 601 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 94) | `from numpy.linalg import norm` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.1.html` | 407 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# How code gets tokenized (using tiktoken)` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.1.html` | 407 | `python` | PYTHON_NO_BODY_INDENT | line opens block but next line not indented (1 -> 1); opener: 'if n <= 1:' | `# How code gets tokenized (using tiktoken)` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.1.html` | 598 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 94) | `import tiktoken` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.2.html` | 246 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 93) | `# pip install sentencepiece` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.2.html` | 546 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def merge(words, pair):' drops to opener indent at line 12 | `from collections import Counter` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.2.html` | 546 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 121) | `from collections import Counter` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` | 709 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for m in messages:' drops to opener indent at line 5 | `def llama3_chat(messages):` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` | 709 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 104) | `def llama3_chat(messages):` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` | 759 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 105) | `from collections import Counter` |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` | 881 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 104) | `import matplotlib.pyplot as plt` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.1.html` | 111 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 83) | `# Vanilla RNN cell from scratch: h_t = tanh(W_hh @ h + W_xh @ x + b).` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.1.html` | 513 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 100) | `# Seq2seq architecture: an LSTM encoder compresses input into a context` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.2.html` | 288 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Luong (dot-product) attention: score = decoder_state @ encoder_outputs^T.` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.2.html` | 288 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class LuongDotAttention(nn.Module):' drops to opener indent at line 5 | `# Luong (dot-product) attention: score = decoder_state @ encoder_outputs^T.` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.2.html` | 362 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Compare Bahdanau vs Luong attention: identical encoder outputs,` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.2.html` | 406 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 88) | `# Full attention decoder: at each step, attend over encoder outputs,` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 290 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# Causal (autoregressive) masking: build an upper-triangular boolean mask` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 369 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 98) | `# Multi-head self-attention: project input into h separate (Q, K, V) triples,` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 513 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Benchmark attention wall-clock time as sequence length doubles.` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 607 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# End-to-end demo: embed a 5-word sentence, run multi-head attention,` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 827 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `import matplotlib.pyplot as plt` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 867 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `def multi_head_attention(X, n_heads, d_model, W_q, W_k, W_v, W_o, mask=None):` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 911 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `import torch` |
| `part-1-foundations/module-04-transformer-architecture/section-4.1.html` | 283 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'if mask is not None:' drops to opener indent at line 36 | `# MultiHeadAttention from scratch using PyTorch` |
| `part-1-foundations/module-04-transformer-architecture/section-4.1.html` | 283 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `# MultiHeadAttention from scratch using PyTorch` |
| `part-1-foundations/module-04-transformer-architecture/section-4.1.html` | 592 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Built-in RMSNorm (PyTorch 2.4+), fused for GPU efficiency` |
| `part-1-foundations/module-04-transformer-architecture/section-4.1.html` | 629 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 90) | `# GPT-2 style weight initialization: N(0, 0.02) for most layers,` |
| `part-1-foundations/module-04-transformer-architecture/section-4.1.html` | 653 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Build a causal (lower-triangular) boolean mask that blocks each token` |
| `part-1-foundations/module-04-transformer-architecture/section-4.1.html` | 653 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def causal_mask(seq_len, device):' drops to opener indent at line 5 | `# Build a causal (lower-triangular) boolean mask that blocks each token` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 111 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `"""` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 111 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class TransformerConfig:' drops to opener indent at line 14 | `"""` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 139 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 91) | `# Causal self-attention with a triangular mask: each token can only` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 349 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# Full decoder-only transformer: stack N blocks, add token + position` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 454 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [4, 8, 12, 13] | `# Weight initialization + autoregressive text generation for our mini-Transforme` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 454 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def _init_weights(self, module: nn.Modul' drops to opener indent at line 20 | `# Weight initialization + autoregressive text generation for our mini-Transforme` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 454 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 82) | `# Weight initialization + autoregressive text generation for our mini-Transforme` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 586 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def lr_at(step: int) -> float:' drops to opener indent at line 33 | `# --- Complete training loop with warmup, gradient clipping, and periodic eval -` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 586 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 89) | `# --- Complete training loop with warmup, gradient clipping, and periodic eval -` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 722 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 97) | `# Download the tiny Shakespeare dataset` |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 740 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `from transformers import AutoModelForCausalLM, AutoTokenizer` |
| `part-1-foundations/module-04-transformer-architecture/section-4.3.html` | 204 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Rotary Position Embedding (RoPE): rotate pairs of dimensions by` |
| `part-1-foundations/module-04-transformer-architecture/section-4.3.html` | 204 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def apply_rope(x, freqs_cos, freqs_sin):' drops to opener indent at line 8 | `# Rotary Position Embedding (RoPE): rotate pairs of dimensions by` |
| `part-1-foundations/module-04-transformer-architecture/section-4.3.html` | 457 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Simplified Differential Attention (conceptual)` |
| `part-1-foundations/module-04-transformer-architecture/section-4.3.html` | 457 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def diff_attention(Q1, K1, Q2, K2, V):' drops to opener indent at line 4 | `# Simplified Differential Attention (conceptual)` |
| `part-1-foundations/module-04-transformer-architecture/section-4.4.html` | 221 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 95) | `# Pseudocode: Online softmax for FlashAttention` |
| `part-1-foundations/module-04-transformer-architecture/section-4.4.html` | 267 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Triton fused softmax kernel: compute softmax in a single GPU pass` |
| `part-1-foundations/module-04-transformer-architecture/section-4.4.html` | 267 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def fused_softmax(x):' drops to opener indent at line 32 | `# Triton fused softmax kernel: compute softmax in a single GPU pass` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 437 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import numpy as np` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 437 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def layer_norm(x, eps=1e-5):' drops to opener indent at line 4 | `import numpy as np` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 437 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `import numpy as np` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 459 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `def softmax(x, axis=-1):` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 518 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import matplotlib.pyplot as plt` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 518 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def sinusoidal_encoding(seq_len, d_model' drops to opener indent at line 4 | `import matplotlib.pyplot as plt` |
| `part-1-foundations/module-04-transformer-architecture/section-4.5.html` | 547 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `import torch` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.1.html` | 92 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def greedy_decode(model, input_ids, max_' drops to opener indent at line 22 | `# Greedy decoding: at each step pick the single highest-probability token.` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.1.html` | 174 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 101) | `# Beam search: maintain beam_width candidate sequences in parallel,` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.1.html` | 248 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Production equivalent using model.generate()` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.1.html` | 256 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 96) | `# Demonstrating the effect of length normalization` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.1.html` | 296 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def score(logprobs, alpha=0.0):' drops to opener indent at line 16 | `# Length normalization: divide log-probabilities by sequence length` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.1.html` | 296 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 115) | `# Length normalization: divide log-probabilities by sequence length` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.1.html` | 405 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 90) | `# Library shortcut: Hugging Face generate() replaces our manual loops.` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.2.html` | 109 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 122) | `# Temperature scaling: divide logits by T before softmax.` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.2.html` | 126 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 91) | `# Nucleus (top-p) sampling: sort tokens by probability, accumulate until` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.2.html` | 178 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 93) | `# Top-k sampling: keep only the k highest-scoring tokens,` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.2.html` | 255 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 91) | `# Min-p sampling: discard any token whose probability falls below` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.2.html` | 303 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 101) | `# Repetition and frequency/presence penalties: scale down logits of` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.2.html` | 405 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 104) | `# Side-by-side comparison: run the same logit vector through greedy,` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 84 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 97) | `# Contrastive decoding: subtract a weaker "amateur" model's log-probs` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 127 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 106) | `# Using Outlines with regex constraints` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 171 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Using the Outlines library for structured generation` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 171 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 107) | `# Using the Outlines library for structured generation` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 309 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# LMQL: declarative constraints on LLM output` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 309 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'async def analyze_product(review: str):' drops to opener indent at line 20 | `# LMQL: declarative constraints on LLM output` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 309 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 91) | `# LMQL: declarative constraints on LLM output` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 357 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 94) | `# SGLang: structured generation with prefix caching` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 533 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 88) | `# Text watermarking: hash the previous token to split the vocabulary into` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 597 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def mbr_decode(candidates, utility_fn):' drops to opener indent at line 16 | `# Minimum Bayes Risk decoding: generate N candidates, score each by` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 699 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Structured output with Instructor + Pydantic: force the LLM to return` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 699 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class SentimentResult(BaseModel):' drops to opener indent at line 13 | `# Structured output with Instructor + Pydantic: force the LLM to return` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 699 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Structured output with Instructor + Pydantic: force the LLM to return` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.4.html` | 132 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 94) | `# Conceptual comparison of generation steps` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.4.html` | 152 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 126) | `# Simplified discrete diffusion process (conceptual)` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.4.html` | 195 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def forward_diffusion(tokens: torch.Tens' drops to opener indent at line 16 | `# Simplified discrete diffusion for text (conceptual).` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.4.html` | 195 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 81) | `# Simplified discrete diffusion for text (conceptual).` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.4.html` | 265 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Conceptual pseudocode for TraceRL training loop` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.4.html` | 473 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `def sample_with_strategy(prompt, max_tokens=30, temperature=1.0,` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.10.html` | 169 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'else:' drops to opener indent at line 8 | `import numpy as np` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.10.html` | 269 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `# Chronos-style time series tokenization` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.3.html` | 554 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# pip install einops` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.3.html` | 572 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 91) | `# pip install jax flax optax` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.4.html` | 467 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 95) | `# world_model_lab.py` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.4.html` | 640 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 104) | `# Training loop (simplified)` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.6.html` | 82 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# MemGPT-style hierarchical memory: core, working, conversation, and archival ti` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.7.html` | 87 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 86) | `# Train a sparse autoencoder (SAE) on transformer hidden states to discover` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.8.html` | 100 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Compare four agency levels (completion, tool-augmented, task agent, persistent` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.9.html` | 89 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 110) | `# Dynamic tool router: selects relevant tools per query using keyword overlap,` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.9.html` | 185 | `python` | WIDE_LINE | 13 line(s) > 80 chars (max 130) | `# Tool result caching with exact-match and semantic similarity layers.` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.9.html` | 397 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `## Step 2 : Extract and visualize attention patterns` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.9.html` | 443 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 88) | `## Step 3 : Activation patching for circuit discovery` |
| `part-10-frontiers/module-33-emerging-architectures/section-33.9.html` | 517 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `## Step 4 : DSPy structured reasoning pipeline` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.1.html` | 282 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 84) | `# Retry-with-fallback pattern for agent tool calls` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.2.html` | 262 | `python` | WIDE_LINE | 22 line(s) > 80 chars (max 134) | `# AI Role Canvas: from structured definition to automated engineering decisions` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.2.html` | 420 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 122) | `role: drafter` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.4.html` | 411 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 130) | `import json, hashlib, time` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.5.html` | 383 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for r in records:' drops to opener indent at line 12 | `import json, csv, sys` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.5.html` | 383 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 93) | `import json, csv, sys` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.6.html` | 570 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for slo in ieb["slos"]:' drops to opener indent at line 10 | `import yaml, json, datetime as dt` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.6.html` | 570 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 107) | `import yaml, json, datetime as dt` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.7.html` | 469 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 147) | `def respond(prompt, log):` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html` | 82 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 202) | `# Token cost calculator: estimates per-request and monthly costs` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html` | 358 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Launch readiness checklist generator` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html` | 358 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def generate_checklist(product_name: str' drops to opener indent at line 65 | `# Launch readiness checklist generator` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html` | 358 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `# Launch readiness checklist generator` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html` | 502 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 115) | `PRICE = {"gpt-4o": (5, 15), "haiku": (0.25, 1.25), "llama-3-70b": (0.7, 0.9)}  #` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 106 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Stress-test a product hypothesis using an LLM as devil's advocate` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 106 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def stress_test_hypothesis(hypothesis: s' drops to opener indent at line 6 | `# Stress-test a product hypothesis using an LLM as devil's advocate` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 106 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Stress-test a product hypothesis using an LLM as devil's advocate` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 149 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Generate acceptance criteria from a feature description` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 149 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def generate_acceptance_criteria(feature' drops to opener indent at line 15 | `# Generate acceptance criteria from a feature description` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 204 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Meta-prompting: use an LLM to critique and improve a draft prompt` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 204 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def meta_prompt_critique(draft_prompt: s' drops to opener indent at line 12 | `# Meta-prompting: use an LLM to critique and improve a draft prompt` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 249 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Summarize evaluation failures and suggest next experiments` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html` | 249 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def summarize_eval_failures(failures: li' drops to opener indent at line 7 | `# Summarize evaluation failures and suggest next experiments` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.3.html` | 277 | `python` | WIDE_LINE | 76 line(s) > 80 chars (max 157) | `"""Provider abstraction layer for LLM-powered applications.` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.3.html` | 443 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 93) | `"""Prompt loader with provider-specific variant support."""` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.3.html` | 504 | `python` | WIDE_LINE | 15 line(s) > 80 chars (max 113) | `"""Model router with rule-based routing and automatic fallback."""` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.3.html` | 809 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 103) | `class LLMClient:` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html` | 514 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 106) | `import hashlib, json` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html` | 73 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `# Loading and using BERT for masked language modeling` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html` | 180 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# T5: Text-to-Text approach for multiple tasks` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 183 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1, 4] | `# Implementing causal language modeling loss from scratch` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 183 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def causal_lm_loss(logits, labels):' drops to opener indent at line 9 | `# Implementing causal language modeling loss from scratch` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 210 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [4, 7, 8] | `# Causal language modeling loss from scratch.` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 210 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def causal_lm_loss(logits: torch.Tensor,' drops to opener indent at line 22 | `# Causal language modeling loss from scratch.` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 210 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Causal language modeling loss from scratch.` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 250 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `# Multi-token prediction: conceptual implementation` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 335 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `# Simulating T5 span corruption` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 392 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'if random.random() > fim_rate:' drops to opener indent at line 7 | `# Fill-in-the-Middle (FIM) transformation` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 446 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for i, logits in enumerate(logits_list, ' drops to opener indent at line 30 | `# Multi-token prediction (Meta, "Better & Faster LLMs via Multi-Token Prediction` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 446 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 89) | `# Multi-token prediction (Meta, "Better & Faster LLMs via Multi-Token Prediction` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html` | 243 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `# Load Mixtral 8x7B with 4-bit quantization (~25 GB vs ~94 GB at FP16).` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html` | 406 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Fit a power-law scaling curve L(N) = a * N^b + c to empirical loss` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html` | 136 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 98) | `# MinHash + LSH deduplication: hash character n-grams into signatures,` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html` | 208 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 134) | `# Minimal quality filtering pipeline` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html` | 210 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `# Warmup + cosine decay LR schedule: ramp linearly for warmup_steps,` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html` | 251 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 84) | `# Warmup-Stable-Decay (WSD) schedule: warmup, hold at peak_lr for a` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html` | 160 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for batch in train_loader:' drops to opener indent at line 47 | `# FSDP (Fully Sharded Data Parallel) training with PyTorch.` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html` | 160 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 94) | `# FSDP (Fully Sharded Data Parallel) training with PyTorch.` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html` | 285 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 89) | `# Gradient checkpointing in PyTorch` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html` | 210 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def apply_task_vector(model, task_vector' drops to opener indent at line 24 | `# Task vector extraction: the DIFFERENCE between a fine-tuned model and its base` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html` | 210 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 87) | `# Task vector extraction: the DIFFERENCE between a fine-tuned model and its base` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html` | 305 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import torch.distributed.checkpoint as dcp` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html` | 305 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def save_checkpoint(model, optimizer, st' drops to opener indent at line 12 | `import torch.distributed.checkpoint as dcp` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` | 79 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `# Define a tiny GPT model (~10M params) for training experiments.` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` | 143 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 85) | `# Load WikiText-2, tokenize into fixed-length chunks, and train` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` | 189 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Generate text from the trained model using temperature sampling.` |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html` | 231 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `# Library shortcut: replace the entire manual training loop with` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html` | 339 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 91) | `# Example: Making an API call to compare providers` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html` | 361 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [4, 5, 8] | `# Compare LLM providers via the OpenAI-compatible chat completion format.` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html` | 361 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'if not p["api_key"]:' drops to opener indent at line 22 | `# Compare LLM providers via the OpenAI-compatible chat completion format.` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html` | 361 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 124) | `# Compare LLM providers via the OpenAI-compatible chat completion format.` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html` | 548 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 139) | `def chat(prompt):` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html` | 128 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Conceptual illustration of fine-grained FP8 quantization` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html` | 128 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def quantize_fp8_fine_grained(tensor, bl' drops to opener indent at line 8 | `# Conceptual illustration of fine-grained FP8 quantization` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html` | 371 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Loading and using BioBERT for biomedical named entity recognition` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html` | 526 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for text in examples:' drops to opener indent at line 23 | `# Compare a general-purpose sentiment model vs a finance-tuned one on financial ` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html` | 526 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 93) | `# Compare a general-purpose sentiment model vs a finance-tuned one on financial ` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html` | 197 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Conceptual: Monte Carlo estimation for PRM training data` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html` | 414 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def answer(prompt: str) -> str:' drops to opener indent at line 43 | `# Compute-optimal inference: spend more tokens on harder problems.` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html` | 414 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 121) | `# Compute-optimal inference: spend more tokens on harder problems.` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html` | 462 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 92) | `# Lab: Measure accuracy vs. N on GSM8K math problems` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html` | 606 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for _ in range(n):' drops to opener indent at line 8 | `from collections import Counter` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html` | 514 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `import torch` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html` | 550 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 89) | `import torch.nn as nn` |
| `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html` | 593 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# The library way: 3 lines` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html` | 211 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for _ in range(n):' drops to opener indent at line 24 | `import anthropic` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html` | 211 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 85) | `import anthropic` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html` | 431 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 86) | `import anthropic` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html` | 100 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `Input: problem p, policy pi, reference policy pi_ref, group size G, KL weight be` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | 69 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Conceptual illustration of LeanDojo data extraction` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | 69 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class ProofState:' drops to opener indent at line 9 | `# Conceptual illustration of LeanDojo data extraction` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | 69 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Conceptual illustration of LeanDojo data extraction` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | 101 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `# ReProver-style retrieval-augmented proving pipeline` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | 164 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 114) | `# Evaluation framework for formal proving benchmarks` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | 250 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 115) | `# AlphaProof-style self-play training loop (conceptual)` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | 399 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Expert iteration for formal theorem proving` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html` | 618 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 104) | `import torch.nn.functional as F` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` | 170 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `# Library shortcut: PyTorch built-in symmetric quantization` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` | 284 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `# Example 1: Loading a model in 4-bit NF4 with bitsandbytes` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` | 349 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 99) | `# Example 4: Benchmarking quantization quality` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` | 421 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def perplexity(model, encodings, max_len' drops to opener indent at line 22 | `# Benchmark how INT8/INT4 quantization degrades perplexity vs the FP16 baseline.` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.1.html` | 421 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 116) | `# Benchmark how INT8/INT4 quantization degrades perplexity vs the FP16 baseline.` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html` | 91 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Example 1: Calculate KV cache size for various models` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html` | 149 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'with torch.no_grad():' drops to opener indent at line 24 | `# KV cache: store the K and V projections of every past position so we never` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.2.html` | 206 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class PhysicalBlock:' drops to opener indent at line 7 | `@dataclass` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.3.html` | 362 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Example 3: Speculative decoding with Hugging Face Transformers` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` | 105 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `# Example 1: Launch vLLM server and benchmark throughput` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` | 168 | `python` | WIDE_LINE | 17 line(s) > 80 chars (max 96) | `# Example 4: Comprehensive benchmarking script` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` | 377 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 87) | `# Example 3: Local inference with Ollama` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` | 580 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'if first_token_t is None:' drops to opener indent at line 24 | `# Comprehensive serving benchmark: measure TTFT, throughput, and TBT under load.` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html` | 580 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 100) | `# Comprehensive serving benchmark: measure TTFT, throughput, and TBT under load.` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html` | 97 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 112) | `# Activation-aware pruning: register a forward hook to measure per-neuron` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | 112 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 90) | `# FlashAttention conceptual implementation in Triton (simplified)` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | 226 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `# Fused softmax in Triton: three passes fused into one kernel launch` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | 286 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for start_n in range(0, N, BLOCK_N):' drops to opener indent at line 62 | `# --- FlashAttention forward pass in Triton (simplified, single-head) ---` |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | 286 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 85) | `# --- FlashAttention forward pass in Triton (simplified, single-head) ---` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 105 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `from bertviz import head_view` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 171 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Attention + ablation validation workflow` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 171 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def ablate_head(activation, hook):' drops to opener indent at line 13 | `# Attention + ablation validation workflow` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 226 | `python` | WIDE_LINE | 17 line(s) > 80 chars (max 116) | `# Probing classifier for linguistic properties` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 323 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Control task for validating probe results` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 477 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'with torch.no_grad():' drops to opener indent at line 19 | `# Tokenization pipeline: text -> token IDs -> embeddings.` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 477 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Tokenization pipeline: text -> token IDs -> embeddings.` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 590 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def plot_attention_head(attn_matrix, tok' drops to opener indent at line 10 | `import matplotlib.pyplot as plt` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 643 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def extract_hidden(model, tokenizer, tex' drops to opener indent at line 19 | `from sklearn.linear_model import LogisticRegression` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 708 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 109) | `import torch, numpy as np, matplotlib.pyplot as plt, seaborn as sns` |
| `part-2-understanding-llms/module-10-interpretability/section-10.2.html` | 137 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 87) | `# Sparse Autoencoder for Mechanistic Interpretability` |
| `part-2-understanding-llms/module-10-interpretability/section-10.2.html` | 281 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class SparseAutoencoder(nn.Module):' drops to opener indent at line 31 | `# Sparse Autoencoder (SAE) for mechanistic interpretability.` |
| `part-2-understanding-llms/module-10-interpretability/section-10.2.html` | 281 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 87) | `# Sparse Autoencoder (SAE) for mechanistic interpretability.` |
| `part-2-understanding-llms/module-10-interpretability/section-10.2.html` | 607 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Loading a pre-trained Sparse Autoencoder from Gemma Scope using SAELens.` |
| `part-2-understanding-llms/module-10-interpretability/section-10.2.html` | 665 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Training an SAE with EleutherAI's sparsify (conceptual)` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 134 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def sim(i, j):' drops to opener indent at line 21 | `# Embedding generation: turn text into dense vectors so we can compare meanings.` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 134 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 82) | `# Embedding generation: turn text into dense vectors so we can compare meanings.` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 211 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# SHAP-based attribution for language models` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 259 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 92) | `# Representation Engineering: Control Vectors` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 395 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 84) | `# Testing CoT faithfulness via truncation experiments` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 498 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Concept Erasure with LEACE` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 498 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 87) | `# Concept Erasure with LEACE` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 560 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for n in range(1, len(steps) + 1):' drops to opener indent at line 35 | `# CoT faithfulness probe: truncate the chain-of-thought at different points` |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 560 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 90) | `# CoT faithfulness probe: truncate the chain-of-thought at different points` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 153 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [4, 7, 8, 12] | `# Attention rollout: combine attention maps across all layers into a single` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 153 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for attn in attentions:' drops to opener indent at line 28 | `# Attention rollout: combine attention maps across all layers into a single` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 153 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 98) | `# Attention rollout: combine attention maps across all layers into a single` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 191 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `# Production equivalent using BertViz` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 230 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Gradient-Weighted Attention` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 319 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 91) | `# Layer-wise Relevance Propagation for Transformers (simplified)` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 383 | `python` | WIDE_LINE | 9 line(s) > 80 chars (max 95) | `# Perturbation-based attribution methods` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 477 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 101) | `# Unified comparison framework for explanation methods` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 611 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def hook(module, inputs, output):' drops to opener indent at line 12 | `# Same task in three frameworks: extract activations from layer 5 of GPT-2.` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 736 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 94) | `# LIME explanation for a text classifier (model-agnostic)` |
| `part-2-understanding-llms/module-10-interpretability/section-10.4.html` | 915 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 98) | `# Faithfulness evaluation for attribution methods` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 98 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Send a chat completion request with system and user messages` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 173 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 103) | `# Set up the OpenAI client and send a chat completion request` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 221 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Call Claude using the Anthropic Messages API` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 251 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 87) | `# Configure and execute the API request` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 305 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def ask(model: str, prompt: str) -> str:' drops to opener indent at line 14 | `# LiteLLM: one client interface, every major provider.` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 305 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# LiteLLM: one client interface, every major provider.` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 336 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 105) | `# LiteLLM: unified interface for 100+ LLM providers.` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 350 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Call Claude on AWS Bedrock using boto3 with IAM authentication` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html` | 394 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Send a chat completion request to the OpenAI API` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 105 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 102) | `# Use OpenAI structured outputs with a JSON schema constraint` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 136 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 113) | `# Instructor: validate LLM output as Pydantic models automatically.` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 161 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Use Instructor to extract structured Pydantic objects from LLM responses` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 202 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Set up structured output extraction from the LLM` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 268 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Marvin: turn plain Python function signatures into LLM calls.` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 268 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def sentiment(text: str) -> str:' drops to opener indent at line 7 | `# Marvin: turn plain Python function signatures into LLM calls.` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 286 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Define tools for function calling and handle tool_calls in the response` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 343 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `# Use Google Gemini function calling for structured output` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.2.html` | 404 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Run multiple LLM calls concurrently using asyncio` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.3.html` | 106 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `# LiteLLM Router with built-in failure isolation` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.3.html` | 138 | `python` | WIDE_LINE | 12 line(s) > 80 chars (max 108) | `# Implement a circuit breaker pattern for resilient LLM calls` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.3.html` | 210 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 90) | `# Build a semantic cache that hashes prompts to avoid redundant API calls` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.3.html` | 271 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 114) | `# Build a semantic cache that hashes prompts to avoid redundant API calls` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.3.html` | 432 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 113) | `# Enforce per-user token budgets to prevent runaway API costs` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.3.html` | 554 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 116) | `# Build a semantic cache that hashes prompts to avoid redundant API calls` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.4.html` | 66 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Call OpenAI's o3 reasoning model via the Responses API` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.4.html` | 166 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 81) | `# Google Gemini thinking mode with token budget control` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.4.html` | 372 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 101) | `# Stream a reasoning response from Anthropic with extended thinking` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.4.html` | 433 | `python` | WIDE_LINE | 12 line(s) > 80 chars (max 110) | `# Build a modality router that dispatches inputs to the correct API` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html` | 297 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 118) | `# Few-shot entity extraction with edge-case examples` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html` | 346 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Instructor: extract structured entities directly as a Pydantic model.` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html` | 390 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Layered system prompt architecture for production use` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html` | 465 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Prompt template system: separate static logic from dynamic data` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html` | 465 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class PromptTemplate:' drops to opener indent at line 9 | `# Prompt template system: separate static logic from dynamic data` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | 71 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Zero-shot Chain-of-Thought: append "step by step" to trigger reasoning.` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | 71 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def solve_with_cot(problem: str) -> str:' drops to opener indent at line 8 | `# Zero-shot Chain-of-Thought: append "step by step" to trigger reasoning.` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | 124 | `text` | WIDE_LINE | 4 line(s) > 80 chars (max 126) | `# Few-shot Chain-of-Thought: exemplar reasoning chains teach the model` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | 239 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `# Self-consistency: sample multiple CoT paths, then majority-vote` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | 423 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Step-back prompting: abstract the principle first, then solve` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | 423 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def step_back_solve(question: str) -> st' drops to opener indent at line 8 | `# Step-back prompting: abstract the principle first, then solve` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` | 423 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 191) | `# Step-back prompting: abstract the principle first, then solve` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html` | 176 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# Reflexion: solve coding tasks with persistent lesson memory` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html` | 272 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Meta-prompting: use one LLM call to generate a system prompt for another` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html` | 272 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def generate_expert_prompt(task_descript' drops to opener indent at line 8 | `# Meta-prompting: use one LLM call to generate a system prompt for another` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html` | 428 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# DSPy: declarative prompting with typed signatures and automatic optimization` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html` | 428 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class FactCheck(dspy.Signature):' drops to opener indent at line 10 | `# DSPy: declarative prompting with typed signatures and automatic optimization` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html` | 135 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 87) | `# Prompt compression with LLMLingua-2: reduce token count while preserving seman` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html` | 74 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# DSPy: Declarative prompt optimization` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html` | 74 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class AnswerQuestion(dspy.Signature):' drops to opener indent at line 9 | `# DSPy: Declarative prompt optimization` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html` | 139 | `python` | WIDE_LINE | 10 line(s) > 80 chars (max 106) | `# OPRO-style prompt optimization (simplified implementation)` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html` | 277 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 87) | `# Prompt compression with LLMLingua` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html` | 394 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 102) | `from llmlingua import PromptCompressor` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html` | 168 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Train a TF-IDF + Logistic Regression baseline classifier` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html` | 224 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 93) | `# Zero-shot classification with Hugging Face: no labeled training data needed.` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html` | 118 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Generate text embeddings via OpenAI's API for downstream ML tasks.` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html` | 118 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def get_embeddings(texts: list[str], mod' drops to opener indent at line 12 | `# Generate text embeddings via OpenAI's API for downstream ML tasks.` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html` | 118 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `# Generate text embeddings via OpenAI's API for downstream ML tasks.` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html` | 208 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# Feature ablation: compare structured-only, embeddings-only, and combined featu` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html` | 119 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `# Use a small LLM to classify request difficulty and select a model tier` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html` | 227 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Implement a cascade router that tries cheap models first` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html` | 316 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def route_request(text: str) -> dict:' drops to opener indent at line 31 | `# Use a small LLM to classify request difficulty and select a model tier` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html` | 173 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 93) | `# Find the Pareto frontier of model configurations by cost and accuracy` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html` | 252 | `text` | WIDE_LINE | 3 line(s) > 80 chars (max 85) | `# Estimate token usage and API cost for different model configurations` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.4.html` | 309 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 106) | `# Cost impact analysis for semantic caching` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 153 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Use spaCy for classical named entity recognition` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 267 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 94) | `# LLM-based Open Information Extraction with structured output` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 357 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 88) | `# LLM-based event extraction with timeline construction` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 615 | `python` | WIDE_LINE | 12 line(s) > 80 chars (max 104) | `# Combine spaCy NER with LLM extraction in a two-layer pipeline` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 837 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 107) | `# LLM-based coreference resolution with structured output` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 1052 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# LLM-based keyword extraction with thematic grouping` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 1052 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def extract_keywords_llm(text: str, max_' drops to opener indent at line 7 | `# LLM-based keyword extraction with thematic grouping` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html` | 1095 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# LLM-based feature engineering for tabular ML` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 60 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class ConversationTurn:' drops to opener indent at line 45 | `import json` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 60 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 84) | `import json` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 118 | `python` | WIDE_LINE | 9 line(s) > 80 chars (max 125) | `import re` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 193 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 92) | `from dataclasses import dataclass` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 269 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 97) | `def extract_tool_use_examples(` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 339 | `python` | WIDE_LINE | 13 line(s) > 80 chars (max 124) | `from pydantic import BaseModel, Field, field_validator` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 397 | `python` | WIDE_LINE | 28 line(s) > 80 chars (max 127) | `import hashlib` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 497 | `text` | WIDE_LINE | 4 line(s) > 80 chars (max 98) | `from pathlib import Path` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 626 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 107) | `# LoRA from scratch: add trainable low-rank matrices A and B` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 683 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 105) | `# Test forward pass` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 716 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 88) | `# Library shortcut: same LoRA injection in 5 lines with HuggingFace PEFT.` |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html` | 751 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 88) | `# Benchmark training cost: measure memory and step time for` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.1.html` | 153 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Define the generate_preference_pair function` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.1.html` | 153 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def generate_preference_pair(instruction' drops to opener indent at line 5 | `# Define the generate_preference_pair function` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.1.html` | 198 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Define data structures for synthetic data generation configuration` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.1.html` | 198 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class QualityMetrics:' drops to opener indent at line 8 | `# Define data structures for synthetic data generation configuration` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.1.html` | 271 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 85) | `# Deduplicate synthetic examples using content hashing` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` | 618 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 95) | `# Self-Instruct core: sample seed examples and prompt the LLM to` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` | 660 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 107) | `# ROUGE-L deduplication: reject generated instructions that are` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` | 691 | `python` | PYTHON_NO_BODY_INDENT | body of opener "if is_duplicate(new_example['instruction" drops to opener indent at line 16 | `# Self-Instruct generation loop: iteratively grow the instruction` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` | 691 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 98) | `# Self-Instruct generation loop: iteratively grow the instruction` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` | 731 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 95) | `# Quality filtering and export: discard short/low-quality examples` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.2.html` | 789 | `python` | WIDE_LINE | 21 line(s) > 80 chars (max 238) | `# Complete Self-Instruct lab: seed pool, instruction generation,` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.3.html` | 174 | `python` | WIDE_LINE | 19 line(s) > 80 chars (max 121) | `# Check for train/test contamination using n-gram overlap detection` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.3.html` | 353 | `python` | WIDE_LINE | 46 line(s) > 80 chars (max 141) | `# Build a composable filter pipeline for synthetic data quality control` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.4.html` | 186 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Calculate annotation quality metrics using numpy` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.4.html` | 289 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Label Studio: Setting up a pre-labeling backend with LLM` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.5.html` | 130 | `python` | WIDE_LINE | 29 line(s) > 80 chars (max 123) | `# Apply privacy and governance checks to the synthetic dataset` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.5.html` | 240 | `python` | WIDE_LINE | 37 line(s) > 80 chars (max 135) | `# Measure dataset diversity using embedding-based metrics` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.5.html` | 356 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 83) | `# Define a data governance record for tracking synthetic data provenance` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.6.html` | 159 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 106) | `# Generate reasoning traces with rejection sampling` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 70 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def synonym_replace(sentence, n=2):' drops to opener indent at line 24 | `# Easy Data Augmentation (EDA): four simple text transformations.` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 102 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Back-translation augmentation: English -> pivot language -> English.` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 102 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def back_translate(text, src="en", pivot' drops to opener indent at line 6 | `# Back-translation augmentation: English -> pivot language -> English.` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 102 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Back-translation augmentation: English -> pivot language -> English.` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 130 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Contextual augmentation: use BERT's masked LM to predict` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 153 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 87) | `# LLM-powered paraphrasing: generate multiple style-varied rewordings` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 206 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Entity-aware augmentation: swap named entities (people, places)` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 206 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def augment_with_entity_swap(example, en' drops to opener indent at line 5 | `# Entity-aware augmentation: swap named entities (people, places)` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 206 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Entity-aware augmentation: swap named entities (people, places)` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 296 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def filter_augmented(original, augmented' drops to opener indent at line 19 | `# Quality filter: keep augmented examples within a semantic similarity` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 394 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for v in variants:' drops to opener indent at line 11 | `def augment(prompt, label, n=5):` |
| `part-4-training-adapting/module-14-synthetic-data/section-14.7.html` | 394 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 85) | `def augment(prompt, label, n=5):` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html` | 125 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 105) | `# Decision framework: choose the lightest adaptation that meets requirements` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html` | 220 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 91) | `# Strategies for mitigating catastrophic forgetting` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html` | 60 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 86) | `# Alpaca format: instruction, input (optional), output` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html` | 103 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 82) | `# ChatML / Messages format (OpenAI-compatible)` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html` | 196 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 91) | `# Load and preprocess a dataset from Hugging Face Hub` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html` | 283 | `python` | WIDE_LINE | 11 line(s) > 80 chars (max 110) | `# Define typed configuration for the fine-tuning data pipeline` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html` | 391 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 130) | `# Define the data_quality_audit function` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html` | 191 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 85) | `# Calculating effective batch size` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html` | 279 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 102) | `# Sanity check: verify training is working correctly` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html` | 623 | `python` | WIDE_LINE | 18 line(s) > 80 chars (max 123) | `# Complete SFT lab solution: load model, prepare data, train,` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.4.html` | 56 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 93) | `# Format training data as JSONL for the OpenAI fine-tuning API` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.4.html` | 379 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 96) | `# Fine-tune a Claude model via the Anthropic API` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.5.html` | 197 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 84) | `# Fine-tune a sentence-transformer to your domain.` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.5.html` | 258 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 84) | `# Practical: deciding whether to fine-tune embeddings` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.6.html` | 168 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `# Load a pre-trained model for sequence classification fine-tuning` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.6.html` | 234 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Sequence pair classification (NLI example)` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.6.html` | 234 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def tokenize_nli(examples):' drops to opener indent at line 13 | `# Sequence pair classification (NLI example)` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.6.html` | 280 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 98) | `# Implement class-weighted loss for imbalanced dataset fine-tuning` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.7.html` | 125 | `python` | WIDE_LINE | 12 line(s) > 80 chars (max 112) | `# Two chunking strategies: fixed-window with overlap and semantic splitting` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.7.html` | 210 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Practical strategies for mitigating lost-in-the-middle` |
| `part-4-training-adapting/module-16-peft/section-16.1.html` | 111 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class LoRALinear(nn.Module):' drops to opener indent at line 11 | `class LoRALinear(nn.Module):` |
| `part-4-training-adapting/module-16-peft/section-16.1.html` | 192 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Configure LoRA adapter parameters: rank, alpha, target modules` |
| `part-4-training-adapting/module-16-peft/section-16.1.html` | 231 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Set up parameter-efficient fine-tuning with LoRA adapters` |
| `part-4-training-adapting/module-16-peft/section-16.1.html` | 300 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Configure LoRA adapter parameters: rank, alpha, target modules` |
| `part-4-training-adapting/module-16-peft/section-16.1.html` | 651 | `python` | WIDE_LINE | 14 line(s) > 80 chars (max 144) | `# Complete LoRA lab solution: load model, apply adapter, train,` |
| `part-4-training-adapting/module-16-peft/section-16.2.html` | 110 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Configure QLoRA adapter parameters on top of the quantized base` |
| `part-4-training-adapting/module-16-peft/section-16.2.html` | 141 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Prefix Tuning: prepend learnable key-value vectors to each attention layer` |
| `part-4-training-adapting/module-16-peft/section-16.2.html` | 161 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Adapter layers: insert small bottleneck modules between transformer layers` |
| `part-4-training-adapting/module-16-peft/section-16.2.html` | 185 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# IA3 configuration: learns only rescaling vectors` |
| `part-4-training-adapting/module-16-peft/section-16.2.html` | 367 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# GaLore conceptual implementation` |
| `part-4-training-adapting/module-16-peft/section-16.2.html` | 417 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def lora_forward(x, A, B, alpha, rank, u' drops to opener indent at line 15 | `# rsLoRA vs standard LoRA scaling comparison` |
| `part-4-training-adapting/module-16-peft/section-16.3.html` | 81 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Load a model with Unsloth for 2x faster LoRA fine-tuning` |
| `part-4-training-adapting/module-16-peft/section-16.3.html` | 231 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Install LLaMA-Factory` |
| `part-4-training-adapting/module-16-peft/section-16.3.html` | 231 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'with open("train_config.json", "w") as f' drops to opener indent at line 32 | `# Install LLaMA-Factory` |
| `part-4-training-adapting/module-16-peft/section-16.3.html` | 273 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# torchtune uses YAML configs and CLI recipes` |
| `part-4-training-adapting/module-16-peft/section-16.3.html` | 320 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Fine-tune with TRL's SFTTrainer for supervised instruction tuning` |
| `part-4-training-adapting/module-16-peft/section-16.4.html` | 199 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Injects learned KV pairs at every attention layer` |
| `part-4-training-adapting/module-16-peft/section-16.4.html` | 240 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 99) | `# Note: HuggingFace PEFT implements P-Tuning v1 as PromptEncoderConfig` |
| `part-4-training-adapting/module-16-peft/section-16.4.html` | 286 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 94) | `# Uses deep prefix tuning (all layers) with a classification head` |
| `part-4-training-adapting/module-16-peft/section-16.4.html` | 433 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# One base model, many task-specific soft prompts loaded on demand` |
| `part-4-training-adapting/module-16-peft/section-16.4.html` | 533 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 106) | `class PromptedLlama(nn.Module):` |
| `part-4-training-adapting/module-16-peft/section-16.5.html` | 227 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `# Compute the KL-divergence distillation loss between teacher and student` |
| `part-4-training-adapting/module-16-peft/section-16.5.html` | 494 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Load and prepare the distillation dataset with teacher-generated labels` |
| `part-4-training-adapting/module-16-peft/section-16.5.html` | 825 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Distillation loss: KL divergence on temperature-scaled soft targets` |
| `part-4-training-adapting/module-16-peft/section-16.5.html` | 857 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Training loop: forward both teacher and student on each batch,` |
| `part-4-training-adapting/module-16-peft/section-16.5.html` | 906 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 91) | `# Evaluate perplexity: compare original student, distilled student,` |
| `part-4-training-adapting/module-16-peft/section-16.5.html` | 963 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 96) | `# Complete distillation lab: load teacher/student, train with KL` |
| `part-4-training-adapting/module-16-peft/section-16.6.html` | 114 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 94) | `# Linear merge of a single weight with different alpha values` |
| `part-4-training-adapting/module-16-peft/section-16.6.html` | 242 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 87) | `# Implement model merging by interpolating weight tensors` |
| `part-4-training-adapting/module-16-peft/section-16.6.html` | 307 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 104) | `# pip install mergekit` |
| `part-4-training-adapting/module-16-peft/section-16.7.html` | 78 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 90) | `# Load evaluation datasets for comparing distilled vs. base models` |
| `part-4-training-adapting/module-16-peft/section-16.7.html` | 130 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Load both the teacher and student models for side-by-side evaluation` |
| `part-4-training-adapting/module-16-peft/section-16.7.html` | 182 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Replay dataset: mix domain data with general replay samples` |
| `part-4-training-adapting/module-16-peft/section-16.7.html` | 262 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 101) | `# Evaluate the distilled model on downstream tasks using PyTorch` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html` | 240 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `Input: SFT model pi_sft, reward model R, reference policy pi_ref = pi_sft, KL we` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html` | 262 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 97) | `# Stage 3: PPO Training with TRL` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html` | 432 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Library shortcut: PPO alignment with TRL (pip install trl)` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html` | 491 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 90) | `# GRPO: Group Relative Policy Optimization (simplified)` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html` | 105 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Numeric walkthrough of a single DPO loss evaluation` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html` | 193 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# DPO Training with TRL` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html` | 395 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 90) | `# Synthetic preference generation with LLM-as-judge` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html` | 745 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 101) | `# Evaluate alignment: check how often the DPO-trained model assigns` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html` | 792 | `python` | WIDE_LINE | 10 line(s) > 80 chars (max 132) | `# Complete DPO lab: load preferences, implement loss from scratch,` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.3.html` | 150 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Constitutional AI: Phase 1 - Self-Critique and Revision` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.3.html` | 328 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Measuring alignment tax across capability dimensions` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.4.html` | 218 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 96) | `# GRPO with Verifiable Rewards for Math Reasoning` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.4.html` | 291 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 90) | `# Simplified DeepSeek-R1 style training pipeline` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html` | 85 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `Input: question Q, debater models DA and DB, human judge J, max rounds R` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html` | 209 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Simplified InfoNCE / Multiple Negatives Ranking Loss` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html` | 209 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def multiple_negatives_ranking_loss(quer' drops to opener indent at line 11 | `# Simplified InfoNCE / Multiple Negatives Ranking Loss` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html` | 370 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# ColBERT-style MaxSim scoring (simplified)` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html` | 370 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def colbert_score(query_tokens, doc_toke' drops to opener indent at line 10 | `# ColBERT-style MaxSim scoring (simplified)` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html` | 600 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 84) | `# Fine-tuning a sentence transformer on domain-specific data` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html` | 827 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `def semantic_search(query, model, doc_embeddings, documents, top_k=3):` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html` | 880 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 85) | `import pandas as pd` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html` | 944 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 97) | `from sentence_transformers import SentenceTransformer` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.3.html` | 285 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# ChromaDB: lightweight embedded vector database` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html` | 339 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 102) | `# Semantic chunking based on embedding similarity` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html` | 487 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 103) | `# Parent-child chunking strategy` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html` | 1047 | `python` | WIDE_LINE | 15 line(s) > 80 chars (max 124) | `import numpy as np` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html` | 1154 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `queries_expected = [` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html` | 1231 | `python` | WIDE_LINE | 11 line(s) > 80 chars (max 126) | `import numpy as np` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 197 | `text` | WIDE_LINE | 3 line(s) > 80 chars (max 84) | `Input: user query q, knowledge base KB, embedding model E, LLM G, top-k paramete` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 292 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement ingest_chunks` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 292 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def ingest_chunks(chunks, source_doc):' drops to opener indent at line 12 | `# implement ingest_chunks` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 326 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 90) | `# Library shortcut: local embeddings + FAISS (pip install sentence-transformers ` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 395 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement naive_rag` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 395 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def naive_rag(query, k=5):' drops to opener indent at line 4 | `# implement naive_rag` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 439 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 96) | `# Library shortcut: RAG with LangChain (pip install langchain langchain-openai l` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 795 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 254) | `knowledge_base = [` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html` | 988 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 170) | `from sentence_transformers import SentenceTransformer` |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html` | 242 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement hyde_retrieve` |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html` | 242 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def hyde_retrieve(query, collection, k=5' drops to opener indent at line 6 | `# implement hyde_retrieve` |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html` | 638 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 87) | `from sentence_transformers import SentenceTransformer, CrossEncoder` |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html` | 845 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 112) | `from sentence_transformers import SentenceTransformer, CrossEncoder` |
| `part-5-retrieval-conversation/module-19-rag/section-19.3.html` | 216 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `# Define KnowledgeGraphStore; implement __init__, add_triples, find_neighbors` |
| `part-5-retrieval-conversation/module-19-rag/section-19.4.html` | 74 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement decompose_query` |
| `part-5-retrieval-conversation/module-19-rag/section-19.4.html` | 74 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def decompose_query(query):' drops to opener indent at line 8 | `# implement decompose_query` |
| `part-5-retrieval-conversation/module-19-rag/section-19.4.html` | 334 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement synthesize_research` |
| `part-5-retrieval-conversation/module-19-rag/section-19.4.html` | 334 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def synthesize_research(original_query, ' drops to opener indent at line 4 | `# implement synthesize_research` |
| `part-5-retrieval-conversation/module-19-rag/section-19.4.html` | 539 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 113) | `# Agentic RAG with LlamaIndex: a router agent picks WHICH index to query.` |
| `part-5-retrieval-conversation/module-19-rag/section-19.5.html` | 55 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement ask_about_table` |
| `part-5-retrieval-conversation/module-19-rag/section-19.5.html` | 55 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def ask_about_table(df: pd.DataFrame, qu' drops to opener indent at line 7 | `# implement ask_about_table` |
| `part-5-retrieval-conversation/module-19-rag/section-19.5.html` | 332 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def csv_to_queryable(csv_path, table_nam' drops to opener indent at line 18 | `# implement csv_to_queryable` |
| `part-5-retrieval-conversation/module-19-rag/section-19.6.html` | 320 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Implementation example` |
| `part-5-retrieval-conversation/module-19-rag/section-19.6.html` | 567 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement embed, retrieve, generate` |
| `part-5-retrieval-conversation/module-19-rag/section-19.6.html` | 567 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def embed(text: str) -> list[float]:' drops to opener indent at line 13 | `# implement embed, retrieve, generate` |
| `part-5-retrieval-conversation/module-19-rag/section-19.7.html` | 419 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from openai import OpenAI` |
| `part-5-retrieval-conversation/module-19-rag/section-19.7.html` | 419 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def evaluate_comprehensiveness(query, an' drops to opener indent at line 5 | `from openai import OpenAI` |
| `part-5-retrieval-conversation/module-19-rag/section-19.7.html` | 532 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for e in entities:' drops to opener indent at line 7 | `def hybrid_retrieve(query, k=10):` |
| `part-5-retrieval-conversation/module-19-rag/section-19.8.html` | 199 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 98) | `from langchain.text_splitter import RecursiveCharacterTextSplitter` |
| `part-5-retrieval-conversation/module-19-rag/section-19.8.html` | 282 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 86) | `import hashlib` |
| `part-5-retrieval-conversation/module-19-rag/section-19.8.html` | 345 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 107) | `from prefect import flow, task` |
| `part-5-retrieval-conversation/module-19-rag/section-19.9.html` | 60 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 103) | `def build_attributed_prompt(query, retrieved_chunks):` |
| `part-5-retrieval-conversation/module-19-rag/section-19.9.html` | 100 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 84) | `from pydantic import BaseModel` |
| `part-5-retrieval-conversation/module-19-rag/section-19.9.html` | 143 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `from transformers import pipeline` |
| `part-5-retrieval-conversation/module-19-rag/section-19.9.html` | 324 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for claim, doc_id in citations:' drops to opener indent at line 10 | `from transformers import pipeline` |
| `part-5-retrieval-conversation/module-19-rag/section-19.9.html` | 324 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 96) | `from transformers import pipeline` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.1.html` | 152 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement update_dialogue_state, get_missing_slots` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.1.html` | 152 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def get_missing_slots(state: dict) -> li' drops to opener indent at line 46 | `# implement update_dialogue_state, get_missing_slots` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.1.html` | 152 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# implement update_dialogue_state, get_missing_slots` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.1.html` | 310 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `# Implementation example` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.1.html` | 422 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 87) | `from dataclasses import dataclass, field` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.1.html` | 622 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 91) | `from enum import Enum` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.2.html` | 96 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from dataclasses import dataclass, field` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.2.html` | 96 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class PersonaSpec:' drops to opener indent at line 5 | `from dataclasses import dataclass, field` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.2.html` | 96 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 105) | `from dataclasses import dataclass, field` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.2.html` | 220 | `python` | WIDE_LINE | 11 line(s) > 80 chars (max 122) | `class CharacterConsistencyManager:` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.2.html` | 298 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `from openai import OpenAI` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.2.html` | 488 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement check_response_consistency` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 136 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 108) | `import tiktoken` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 215 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 91) | `from openai import OpenAI` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 344 | `python` | WIDE_LINE | 12 line(s) > 80 chars (max 115) | `# Define MemoryEntry, VectorMemoryStore; implement __init__, store, retrieve` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 706 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 93) | `# Mem0: Drop-in memory for any LLM application` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 765 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 88) | `# Memory consolidation pipeline` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 984 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 82) | `from openai import OpenAI` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 1033 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 88) | `from sentence_transformers import SentenceTransformer` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 1093 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 86) | `class MemoryChat:` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html` | 1193 | `python` | WIDE_LINE | 12 line(s) > 80 chars (max 153) | `from openai import OpenAI` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.4.html` | 261 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `from dataclasses import dataclass, field` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.4.html` | 338 | `python` | WIDE_LINE | 18 line(s) > 80 chars (max 148) | `from dataclasses import dataclass, field` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.4.html` | 549 | `python` | WIDE_LINE | 17 line(s) > 80 chars (max 109) | `# Define ContextPriority, ContextBlock, ContextBudgetManager; implement __init__` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` | 266 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 112) | `import asyncio` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` | 464 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 101) | `from dataclasses import dataclass` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` | 973 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Implementation example` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` | 973 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'async def create_voice_bot():' drops to opener indent at line 12 | `# Implementation example` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` | 1106 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `import base64` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html` | 147 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from pydantic_ai import Agent` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html` | 147 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def get_weather(location: str, unit: str' drops to opener indent at line 6 | `from pydantic_ai import Agent` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html` | 203 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from pydantic_ai import Agent` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html` | 203 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def get_weather(location: str, unit: str' drops to opener indent at line 7 | `from pydantic_ai import Agent` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html` | 94 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `# Building a simple MCP server with the Python SDK` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html` | 143 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from langchain_core.tools import tool` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.2.html` | 143 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def get_weather(city: str) -> str:' drops to opener indent at line 5 | `from langchain_core.tools import tool` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.3.html` | 61 | `json` | WIDE_LINE | 3 line(s) > 80 chars (max 147) | `{` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.4.html` | 61 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 93) | `from pydantic import BaseModel, Field, validator` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.5.html` | 61 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `from langgraph.graph import StateGraph, END` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html` | 137 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# OpenAI Agents SDK: Research Agent` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html` | 181 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Install dependencies for the multi-agent framework selection lab` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html` | 186 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Lab starter: framework selection skeleton. Students fill in the TODOs.` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html` | 216 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 135) | `# Full solution for the framework-selection lab.` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.2.html` | 82 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `Input: task T, specialist agents {A1, ..., An} with descriptions, LLM M, max rou` |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.3.html` | 61 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 111) | `from langgraph.graph import StateGraph, END` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html` | 89 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 95) | `class SecureAgentExecutor:` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html` | 134 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from nemoguardrails import RailsConfig, LLMRails` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.3.html` | 77 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `from langfuse import Langfuse` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.3.html` | 113 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `class BudgetEnforcer:` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 65 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 82) | `import asyncio` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 141 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for attempt in range(self.max_retries):' drops to opener indent at line 37 | `import asyncio` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 245 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 95) | `import re` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 321 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 189) | `INJECTION_ATTACKS = [` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 344 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 107) | `TOOL_MISUSE_ATTACKS = [` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 365 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 149) | `LOOP_ATTACKS = [` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 381 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 97) | `def run_red_team():` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html` | 517 | `text` | WIDE_LINE | 13 line(s) > 80 chars (max 160) | `import re` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` | 59 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from pydantic import BaseModel` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` | 59 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class ResearchOutput(BaseModel):' drops to opener indent at line 6 | `from pydantic import BaseModel` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` | 59 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `from pydantic import BaseModel` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` | 100 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 109) | `import random` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` | 165 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Lab starter: agent contract validation. Students fill in the TODOs.` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` | 191 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class WeatherQuery(BaseModel):' drops to opener indent at line 16 | `# Full solution for the agent contract validation lab.` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` | 191 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 93) | `# Full solution for the agent contract validation lab.` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html` | 53 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `from dataclasses import dataclass` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html` | 126 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 88) | `from typing import Any, Callable` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html` | 304 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import openai` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html` | 365 | `python` | WIDE_LINE | 9 line(s) > 80 chars (max 101) | `from functools import wraps` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html` | 442 | `python` | WIDE_LINE | 18 line(s) > 80 chars (max 125) | `import json` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.7.html` | 61 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 102) | `#!/usr/bin/env bash` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.7.html` | 129 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 101) | `import subprocess` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.7.html` | 181 | `bash` | WIDE_LINE | 2 line(s) > 80 chars (max 111) | `#!/usr/bin/env bash` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.7.html` | 223 | `yaml` | WIDE_LINE | 1 line(s) > 80 chars (max 98) | `# .github/workflows/build-agent-runner.yml` |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.7.html` | 401 | `bash` | WIDE_LINE | 2 line(s) > 80 chars (max 103) | `#!/usr/bin/env bash` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.1.html` | 497 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `# LLaVA visual question answering: load the LLaVA-v1.6-Mistral model` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.2.html` | 114 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Bark: token-based speech generation with paralinguistic cues` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.2.html` | 196 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `# Production-ready speech-to-text with faster-whisper` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.2.html` | 379 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Using CogVideoX (open-source) via diffusers` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.3.html` | 52 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 84) | `# TrOCR: Transformer-based OCR for printed and handwritten text` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.3.html` | 75 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `from doctr.io import DocumentFile` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.3.html` | 236 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 108) | `# VLM-based document extraction: send an invoice image to GPT-4o` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.4.html` | 324 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Gemini 2.5: native multimodal with early fusion` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.4.html` | 362 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Any-to-any generation: analyze an image, then generate a new one based on the ` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.4.html` | 409 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `from transformers import pipeline` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html` | 70 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 100) | `# RT-2 style action tokenization` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html` | 178 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 82) | `# Fine-tuning OpenVLA with LoRA for a new robot platform` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html` | 257 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 114) | `# Setting up a robot simulation environment with Habitat` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html` | 327 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 98) | `# Domain randomization for sim-to-real transfer` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html` | 418 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class EvaluationResult:' drops to opener indent at line 66 | `# VLA model evaluation framework` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html` | 418 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 95) | `# VLA model evaluation framework` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.6.html` | 59 | `python` | WIDE_LINE | 14 line(s) > 80 chars (max 124) | `# SayCan-style affordance scoring with an LLM planner` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.6.html` | 175 | `python` | WIDE_LINE | 32 line(s) > 80 chars (max 138) | `# VLM-based navigation goal parsing and semantic map building` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.6.html` | 286 | `python` | WIDE_LINE | 30 line(s) > 80 chars (max 129) | `# Multi-robot task allocation with an LLM coordinator` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.6.html` | 440 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Edge deployment configuration for NVIDIA Jetson with quantized LLM` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.6.html` | 440 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class JetsonDeploymentConfig:' drops to opener indent at line 9 | `# Edge deployment configuration for NVIDIA Jetson with quantized LLM` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.6.html` | 440 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 91) | `# Edge deployment configuration for NVIDIA Jetson with quantized LLM` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.7.html` | 104 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Spherical harmonics evaluation for view-dependent color` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.7.html` | 104 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def sh_basis(direction: np.ndarray) -> n' drops to opener indent at line 11 | `# Spherical harmonics evaluation for view-dependent color` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.7.html` | 104 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 98) | `# Spherical harmonics evaluation for view-dependent color` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.7.html` | 193 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `# Simplified Score Distillation Sampling (SDS) loop for 3DGS` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.7.html` | 301 | `python` | WIDE_LINE | 10 line(s) > 80 chars (max 101) | `# Language-embedded Gaussian editing: conceptual pipeline` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.7.html` | 492 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 103) | `# Training a 3DGS model using gsplat` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.7.html` | 695 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 122) | `import requests` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.1.html` | 71 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Using a FIM model directly (DeepSeek-Coder example)` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.1.html` | 71 | `python` | PYTHON_NO_BODY_INDENT | line opens block but next line not indented (1 -> 0); opener: 'while left <= right:' | `# Using a FIM model directly (DeepSeek-Coder example)` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.1.html` | 71 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 93) | `# Using a FIM model directly (DeepSeek-Coder example)` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.1.html` | 256 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 105) | `# Simplified agentic coding loop (conceptual)` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.2.html` | 127 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 93) | `# Implementation example` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.2.html` | 357 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 119) | `import json` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.3.html` | 102 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Implementation example` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.3.html` | 215 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Implementation example` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html` | 52 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# implement recommend_items` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html` | 177 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `# Building a simple LLM-powered search with RAG` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html` | 202 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 83) | `from openai import OpenAI` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html` | 346 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import json` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html` | 346 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def nl_to_sql(question: str, schema: str' drops to opener indent at line 11 | `import json` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html` | 346 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 93) | `import json` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html` | 391 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `def generate_chart_spec(question: str, query_results: list[dict]) -> dict:` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html` | 549 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Map-reduce text analytics over a corpus` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.5.html` | 165 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def scan_for_vulnerabilities(code: str, ' drops to opener indent at line 16 | `# LLM-powered code vulnerability scanner` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.5.html` | 165 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `# LLM-powered code vulnerability scanner` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.6.html` | 52 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 83) | `# implement socratic_tutor` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.6.html` | 263 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Style transfer: convert between registers, tones, and reading levels` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.6.html` | 431 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 94) | `# LLM-based grammatical error correction with explanations` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.6.html` | 533 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 88) | `# Data-to-text generation: convert a statistics table to narrative text` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.7.html` | 97 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `# Conceptual: LLM as robot task planner` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.7.html` | 553 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `import torch` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html` | 117 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 94) | `# implement compute_perplexity_and_bpb` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html` | 297 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 104) | `# Implementation example` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html` | 354 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement llm_judge_evaluate` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html` | 354 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def llm_judge_evaluate(question: str, an' drops to opener indent at line 7 | `# implement llm_judge_evaluate` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html` | 354 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 192) | `# implement llm_judge_evaluate` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html` | 734 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 83) | `# Define EvalCase, EvalResult, EvalHarness; implement __init__, evaluate, summar` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 82 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from opentelemetry import trace` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 82 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `from opentelemetry import trace` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 120 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 89) | `import openai` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 191 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 88) | `from opentelemetry import trace, context` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 335 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Auto-instrument all supported LLM libraries with one call` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 335 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Auto-instrument all supported LLM libraries with one call` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 386 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `from opentelemetry import metrics` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 651 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import pandas as pd` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.10.html` | 690 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# Register the best model` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html` | 268 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `import json` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html` | 367 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 95) | `import numpy as np` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html` | 496 | `python` | WIDE_LINE | 10 line(s) > 80 chars (max 109) | `# Lab: Complete evaluation protocol for a retrieval-augmented QA system` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.12.html` | 476 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `def rouge_1(reference, candidate):` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.12.html` | 566 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from transformers import pipeline` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.12.html` | 566 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def llm_judge(question, reference_answer' drops to opener indent at line 10 | `from transformers import pipeline` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.2.html` | 92 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `Input: scores S = [s1, ..., sn], metric function f, resamples B, confidence leve` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.2.html` | 106 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement bootstrap_ci` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.2.html` | 237 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# implement mcnemar_test` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.2.html` | 451 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `import random` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.2.html` | 556 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 84) | `from dataclasses import dataclass` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.3.html` | 93 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 112) | `import pytest` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.3.html` | 169 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 98) | `# implement call_llm, test_summarizer_output_length, test_json_output_structure` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.3.html` | 214 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 107) | `# pip install respx httpx` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.3.html` | 237 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# pip install hypothesis` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.3.html` | 237 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def test_sanitizer_never_crashes(user_in' drops to opener indent at line 6 | `# pip install hypothesis` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.3.html` | 298 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `import re` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.6.html` | 119 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement rag_pipeline, retrieve_documents, generate_answer` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.6.html` | 119 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def rag_pipeline(query: str) -> str:' drops to opener indent at line 8 | `# implement rag_pipeline, retrieve_documents, generate_answer` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.6.html` | 168 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement answer_question, search_knowledge_base, call_llm` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.6.html` | 168 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def answer_question(question: str) -> di' drops to opener indent at line 12 | `# implement answer_question, search_knowledge_base, call_llm` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.6.html` | 363 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 96) | `from dataclasses import dataclass` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html` | 71 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 99) | `# Detecting and quantifying position bias in an LLM judge` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html` | 240 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 94) | `# Prometheus 2: rubric-based evaluation with an open-source judge` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html` | 329 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# AlpacaEval length-controlled win rate debiasing` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html` | 387 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `# Meta-evaluation: measuring LLM judge reliability` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.9.html` | 327 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import torch` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.9.html` | 441 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `def measure_contamination_baseline(` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.1.html` | 252 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `import litserve as ls` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.1.html` | 376 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement bedrock_chat` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.1.html` | 376 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def bedrock_chat(prompt: str, model_id: ' drops to opener indent at line 5 | `# implement bedrock_chat` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.1.html` | 376 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `# implement bedrock_chat` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.2.html` | 185 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# implement chat` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.2.html` | 262 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 100) | `# Streamlit dashboard setup` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.3.html` | 95 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 82) | `import time` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.3.html` | 398 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def check_safety(conversation: list[dict' drops to opener indent at line 18 | `# implement check_safety` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.3.html` | 398 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# implement check_safety` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.4.html` | 166 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `import json, hashlib` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.5.html` | 156 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import openai` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.5.html` | 273 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `import asyncio` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.5.html` | 335 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# litellm_config.yaml:` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.5.html` | 369 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 92) | `import numpy as np` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.5.html` | 435 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 96) | `from datetime import datetime, timedelta` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 119 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1, 5, 9] | `import asyncio` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 119 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class ResearchRequest:' drops to opener indent at line 14 | `import asyncio` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 225 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1, 5] | `from temporalio import activity, workflow` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 225 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'async def query_database(sql: str) -> st' drops to opener indent at line 12 | `from temporalio import activity, workflow` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 288 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1, 5] | `import inngest` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 462 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `from langgraph.graph import StateGraph, START, END` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 462 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def review_node(state: ResearchState) ->' drops to opener indent at line 29 | `from langgraph.graph import StateGraph, START, END` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 553 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for attempt in range(1, max_attempts + 1' drops to opener indent at line 52 | `import random` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | 553 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `import random` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.6.html` | -1 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for comp_name, comp_args in reversed(com' drops to opener indent at line 42 | `@workflow.defn` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | 143 | `bash` | WIDE_LINE | 1 line(s) > 80 chars (max 111) | `# Build llama.cpp from source` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | 282 | `dockerfile` | WIDE_LINE | 1 line(s) > 80 chars (max 88) | `# Modelfile: a custom medical assistant configuration` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | 317 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1, 5] | `"""Using Ollama's API from Python (OpenAI-compatible endpoint)."""` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | 536 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `"""MLX text generation with streaming."""` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | -1 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `"""Export a model for ExecuTorch deployment (simplified workflow)."""` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | -1 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'with open("phi2_mobile.pte", "wb") as f:' drops to opener indent at line 36 | `"""Export a model for ExecuTorch deployment (simplified workflow)."""` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | -1 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1, 5] | `"""Benchmark two quantization levels on the same prompts."""` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html` | -1 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def benchmark_model(model_name: str, pro' drops to opener indent at line 53 | `"""Benchmark two quantization levels on the same prompts."""` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 69 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 133) | `from enum import Enum` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 152 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 87) | `import asyncio` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 218 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 89) | `# pip install tenacity` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 232 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'class FallbackChain:' drops to opener indent at line 14 | `from dataclasses import dataclass, field` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 232 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 96) | `from dataclasses import dataclass, field` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 300 | `python` | WIDE_LINE | 17 line(s) > 80 chars (max 135) | `import time` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 387 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 91) | `import json` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.8.html` | 492 | `python` | WIDE_LINE | 10 line(s) > 80 chars (max 141) | `from dataclasses import dataclass, field` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.9.html` | 660 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `import requests` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.9.html` | 660 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def measure_request(prompt, max_tokens=5' drops to opener indent at line 6 | `import requests` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.9.html` | 660 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `import requests` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 160 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 87) | `# implement sanitize_input` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 204 | `text` | WIDE_LINE | 3 line(s) > 80 chars (max 107) | `Input: user message M, injection patterns P = {p1, ..., pk}, LLM classifier C, t` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 231 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `import re` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 259 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 95) | `# pip install presidio-analyzer presidio-anonymizer` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 474 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 85) | `# implement llamaguard_safety_check` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 613 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# WARNING: This demonstrates the vulnerability. Never run untrusted pickle files` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 837 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 101) | `import re` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 895 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `class PIIRedactor:` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 941 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 90) | `class SandwichDefense:` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 991 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 93) | `class SafetyPipeline:` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html` | 1082 | `python` | WIDE_LINE | 26 line(s) > 80 chars (max 195) | `import re, json` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.10.html` | 140 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 100) | `# pip install codecarbon` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.10.html` | 318 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 84) | `# Carbon-aware region selection for training jobs` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.10.html` | 414 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Tracking training emissions with CodeCarbon` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.10.html` | 704 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `from codecarbon import EmissionsTracker` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` | 120 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 100) | `# End-to-end privacy pipeline: scrub, train with DP, filter outputs` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` | 182 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 84) | `# Membership Inference Attack: loss-threshold method` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` | 362 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 87) | `# PII detection and scrubbing pipeline` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` | 430 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 106) | `# pip install presidio-analyzer presidio-anonymizer` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` | 495 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 99) | `# Lab: Memorization measurement and DP mitigation` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` | 722 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 102) | `import copy` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html` | 823 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 90) | `import flwr as fl` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.2.html` | 100 | `text` | WIDE_LINE | 3 line(s) > 80 chars (max 88) | `# implement self_consistency_check` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.2.html` | 199 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement check_faithfulness` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.2.html` | 199 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def check_faithfulness(source: str, clai' drops to opener indent at line 6 | `# implement check_faithfulness` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | 101 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def bias_probe(template: str, groups: li' drops to opener indent at line 17 | `# implement bias_probe` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | 138 | `text` | WIDE_LINE | 2 line(s) > 80 chars (max 118) | `Input: demographic groups G = {g1, ..., gk}, prompt templates T, model M, toxici` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | 244 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement generate_model_card` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | 244 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def generate_model_card(model_name: str,' drops to opener indent at line 4 | `# implement generate_model_card` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | 244 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# implement generate_model_card` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | 577 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Measuring cultural value bias in LLM responses` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.4.html` | 195 | `python` | INCONSISTENT_INDENT | structural indent widths suspect: [1] | `# implement get_sector_requirements` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.4.html` | 195 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'def get_sector_requirements(sector: str)' drops to opener indent at line 4 | `# implement get_sector_requirements` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.5.html` | 111 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `# Define RiskTier, ModelInventoryEntry; implement needs_review` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.5.html` | 158 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `import json, hashlib` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.6.html` | 95 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 90) | `# implement check_license_compatibility` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.6.html` | 140 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 108) | `# implement dp_sgd_step` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.7.html` | 116 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# implement gradient_ascent_unlearn` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.7.html` | 160 | `python` | PYTHON_NO_BODY_INDENT | body of opener 'for key in base_weights:' drops to opener indent at line 17 | `# implement compute_task_vector, negate_task_vector` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.7.html` | 160 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 89) | `# implement compute_task_vector, negate_task_vector` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.8.html` | 70 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 113) | `Input: target system S, attack library A = {a1, ..., am}, scorer function score(` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.8.html` | 221 | `python` | WIDE_LINE | 18 line(s) > 80 chars (max 107) | `# Custom red team framework for tool-use testing` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.8.html` | 386 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 88) | `# Building a domain-specific adversarial prompt library` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.9.html` | 85 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 87) | `# Risk classification helper for LLM applications` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.9.html` | 467 | `python` | WIDE_LINE | 16 line(s) > 80 chars (max 99) | `# Automated EU AI Act compliance checker` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.1.html` | 149 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 105) | `from dataclasses import dataclass, field` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.1.html` | 373 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 96) | `from dataclasses import dataclass` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.1.html` | 419 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 88) | `# Business Case Template (structured as a Python dict for automation)` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.1.html` | 645 | `text` | WIDE_LINE | 3 line(s) > 80 chars (max 95) | `{` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.2.html` | 64 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 103) | `# Define RiskLevel, LLMProductSpec; implement model_tier_recommendation` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.2.html` | 135 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `from dataclasses import dataclass` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.2.html` | 391 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 96) | `from dataclasses import dataclass` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html` | 391 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 86) | `from dataclasses import dataclass` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html` | 567 | `text` | WIDE_LINE | 4 line(s) > 80 chars (max 152) | `from dataclasses import dataclass, field` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html` | 626 | `text` | WIDE_LINE | 1 line(s) > 80 chars (max 85) | `class ROICalculator:` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html` | 707 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 100) | `# implement sensitivity_analysis` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html` | 772 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 95) | `# implement multi_year_projection` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html` | 841 | `text` | WIDE_LINE | 3 line(s) > 80 chars (max 95) | `# implement executive_report` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.3.html` | 928 | `text` | WIDE_LINE | 8 line(s) > 80 chars (max 115) | `from dataclasses import dataclass, replace` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.4.html` | 62 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 82) | `from dataclasses import dataclass, field` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.4.html` | 182 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 87) | `from dataclasses import dataclass` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.4.html` | 412 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# implement tco_comparison` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html` | 147 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 86) | `from dataclasses import dataclass` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html` | 210 | `python` | WIDE_LINE | 6 line(s) > 80 chars (max 101) | `from dataclasses import dataclass` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html` | 295 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 90) | `from dataclasses import dataclass` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.5.html` | 514 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 89) | `import random` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` | 57 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 83) | `# Example: FastAPI middleware for OIDC token validation in an LLM service` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` | 118 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 91) | `# Example: LLM-specific RBAC policy engine` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` | 201 | `python` | WIDE_LINE | 2 line(s) > 80 chars (max 95) | `# Example: Tenant-isolated RAG pipeline with namespace separation` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` | 411 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 105) | `# Example: Risk-based approval routing for LLM tool calls` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` | 487 | `yaml` | WIDE_LINE | 1 line(s) > 80 chars (max 81) | `# Example: Governance configuration for an enterprise LLM platform` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.6.html` | 715 | `python` | WIDE_LINE | 3 line(s) > 80 chars (max 90) | `# Example: Enterprise chatbot orchestrator combining all integration patterns` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 58 | `python` | WIDE_LINE | 8 line(s) > 80 chars (max 113) | `# Example: Three-tier token budget enforcement` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 129 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 113) | `# Example: Cost-aware cascade router with confidence-based escalation` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 190 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 91) | `# pip install litellm` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 211 | `python` | WIDE_LINE | 7 line(s) > 80 chars (max 101) | `# Example: Semantic cache with similarity threshold and TTL` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 307 | `python` | WIDE_LINE | 9 line(s) > 80 chars (max 107) | `# Example: Prompt cost analyzer and optimizer` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 366 | `python` | WIDE_LINE | 5 line(s) > 80 chars (max 121) | `# Example: Evaluation budget manager with stratified sampling` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 426 | `python` | WIDE_LINE | 4 line(s) > 80 chars (max 100) | `# Example: Cost observability with anomaly detection` |
| `part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html` | 493 | `python` | WIDE_LINE | 1 line(s) > 80 chars (max 86) | `# Lab: Complete cost-aware LLM middleware` |