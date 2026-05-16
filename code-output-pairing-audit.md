# Code Output / Caption Pairing Audit

Scanned **389** HTML files. 1452 Python code blocks of 1618 total. 23197 caption/prose containers scanned for cross-references. Caption inventory: **1091** distinct Code-Fragment labels.

## 1. Summary

| Pattern | Count | Files affected |
|---|---:|---:|
| A. Code blocks missing expected output | 167 | 111 |
| B. Caption/prose references with pairing issues | 266 | 73 |
| Orphan `<div class="code-output">` blocks (anchor check) | 8 | 6 |

| Overlap | Files |
|---|---:|
| A only | 78 |
| B only | 40 |
| Both A and B | 33 |

Pattern B sub-breakdown:

| Status | Count |
|---|---:|
| phantom | 0 |
| remote | 0 |
| stale | 266 |
| ambiguous | 0 |

## 2. Pattern A - Code blocks that should produce output but have none

Each row is a `<pre><code class='...lang-python...'>` block whose top-level statements include a `print(...)`, an f-string, a REPL-style display call (`.head()`, `.summary()`, ...), or a `for`/`with`/`if` block containing `print(...)`, but no `<div class="code-output">` follows it. Excludes definition-only blocks.

**Of 167 total blocks:** 72 have a `Code Fragment X.Y.Z` caption (higher priority), 95 are uncaptioned (often Library-Shortcut callouts).

### 2.1 Captioned blocks missing output (72)

| File:Line | Caption | Output construct | Code preview |
|---|---|---|---|
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html`:88 | `0.1.2` | `print(f'Mean MSE: {-scores.mean():.4f} (+/- {scores.std():.4f})')` | `# Production equivalent using scikit-learn from sklearn.model_selection import c` |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html`:487 | `0.4.3` | `for-loop with print()` | `import matplotlib.pyplot as plt import numpy as np milestones = { 1957: "Percept` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html`:434 | `1.3.3` | `plt.show()` | `import matplotlib.pyplot as plt # Cosine similarity heatmap: compute pairwise si` |
| `part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html`:500 | `1.4.1` | `for-loop with print()` | `from gensim.models import Word2Vec # Sample corpus (in practice, use a larger da` |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html`:143 | `3.3.1` | `print(f'Output: {out.shape}')` | `import torch import torch.nn as nn # Built-in MHA: same functionality, one line ` |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html`:308 | `5.3.4` | `print(result.variables)` | `# LMQL: declarative constraints on LLM output # pip install lmql import lmql @lm` |
| `part-11-idea-to-product/module-34-idea-to-product/section-34.1.html`:82 | `34.1.1` | `print(f'Prompt: {prompt}')` | `# Demonstrating non-deterministic LLM output across repeated calls import openai` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html`:82 | `35.1.1` | `print('=' * 65)` | `# Token cost calculator: estimates per-request and monthly costs # for an LLM-po` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.1.html`:358 | `35.1.2` | `print(json.dumps(checklist, indent=2))` | `# Launch readiness checklist generator # Produces a structured checklist with st` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html`:106 | `35.2.1` | `print(critique)` | `# Stress-test a product hypothesis using an LLM as devil's advocate import opena` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html`:149 | `35.2.2` | `print(criteria)` | `# Generate acceptance criteria from a feature description ACCEPTANCE_CRITERIA_PR` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html`:204 | `35.2.3` | `print(improved)` | `# Meta-prompting: use an LLM to critique and improve a draft prompt META_CRITIC_` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.2.html`:249 | `35.2.4` | `print(analysis)` | `# Summarize evaluation failures and suggest next experiments import json def sum` |
| `part-11-idea-to-product/module-35-shipping-scaling/section-35.3.html`:503 | `35.3.3` | `bare string 'Model router with rule-based routing an` | `"""Model router with rule-based routing and automatic fallback.""" from __future` |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html`:428 | `8.1.3` | `for-loop with print()` | `import anthropic client = anthropic.Anthropic() # Using Claude's extended thinki` |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html`:592 | `10.1.8` | `plt.show()` | `import matplotlib.pyplot as plt import seaborn as sns def plot_attention_head(at` |
| `part-3-working-with-llms/module-11-llm-apis/section-11.4.html`:371 | `11.4.6` | `with-block containing print()` | `# Stream a reasoning response from Anthropic with extended thinking # Shows thin` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html`:448 | `12.1.5` | `print(messages[0]['content'])` | `# Prompt template system: separate static logic from dynamic data # Enables vers` |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html`:271 | `12.3.3` | `print(prompt[:300])` | `# Meta-prompting: use one LLM call to generate a system prompt for another # Use` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html`:250 | `15.2.5` | `print(f'Loaded {len(dataset)} examples with columns: {dataset.column_names}')` | `# pip install datasets transformers from datasets import load_dataset from trans` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html`:188 | `15.3.2` | `print(f"{'Per-device':>12} {'Grad Accum':>12} {'GPUs':>6} {'Effective BS':>14}")` | `# Calculating effective batch size def compute_effective_batch_size( per_device_` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html`:432 | `15.3.7` | `if-block containing print()` | `# Load a small instruction-tuned model and capture baseline outputs # for compar` |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.6.html`:233 | `15.6.3` | `print(f"Input: {tokenizer.decode(sample['input_ids'][0])}")` | `# Sequence pair classification (NLI example) from transformers import AutoModelF` |
| `part-4-training-adapting/module-16-peft/section-16.1.html`:225 | `16.1.2` | `print('Merged model saved. Upload to HF Hub or serve with vLLM.')` | `# Set up parameter-efficient fine-tuning with LoRA adapters # Freeze the base mo` |
| `part-4-training-adapting/module-16-peft/section-16.2.html`:415 | `16.2.7` | `for-loop with print()` | `# rsLoRA vs standard LoRA scaling comparison import torch import math def lora_f` |
| `part-4-training-adapting/module-16-peft/section-16.4.html`:199 | `16.4.2` | `print('Prefix Tuning config:', peft_config)` | `# Injects learned KV pairs at every attention layer from transformers import Aut` |
| `part-4-training-adapting/module-16-peft/section-16.5.html`:493 | `16.5.4` | `print('Distillation complete. Evaluate student against teacher.')` | `# Load and prepare the distillation dataset with teacher-generated labels # Each` |
| `part-4-training-adapting/module-16-peft/section-16.5.html`:796 | `16.5.6` | `for-loop with print()` | `# Load teacher (gpt2-medium, frozen) and student (gpt2, trainable). # The studen` |
| `part-4-training-adapting/module-16-peft/section-16.6.html`:307 | `16.6.4` | `print("Merge complete. Test with: transformers AutoModelForCausalLM.from_pretrai...` | `# pip install mergekit # Option 1: CLI (most common) # mergekit-yaml merge_ties.` |
| `part-4-training-adapting/module-16-peft/section-16.7.html`:245 | `16.7.3` | `print(f'per-param penalties: {per_param}')` | `# EWC penalty: numeric walkthrough with two parameters import numpy as np theta_` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html`:190 | `17.1.2` | `print(f'Training samples: {len(pref_dataset)}')` | `from datasets import load_dataset # Stage 2: Reward Model Training from trl impo` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html`:346 | `17.1.4` | `print(f'ratio={r_t}, A={A_t} -> clipped_ratio={clipped_r}, loss={loss}')` | `# PPO clipping: numeric walkthrough eps = 0.2 # Case 1: positive advantage, rati` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html`:468 | `17.1.7` | `print(f'mean={mean:.2f}, std={std:.4f}')` | `# GRPO group normalization: numeric walkthrough import numpy as np rewards = np.` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html`:632 | `17.2.8` | `print(f'Dataset size: {len(dataset)}')` | `# Load a preference dataset: each example has a prompt, a chosen # (better) resp` |
| `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.4.html`:390 | `17.4.4` | `print(response)` | `# Using open reasoning models for inference from transformers import AutoModelFo` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html`:765 | `18.1.8` | `print(f'Small: {model_small.get_sentence_embedding_dimension()} dims')` | `from sentence_transformers import SentenceTransformer import numpy as np model_s` |
| `part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html`:1006 | `18.4.9` | `print(f'Document: {len(document)} chars, {document.count(chr(10))} lines')` | `document = ( "# Introduction to Machine Learning\n\n" "Machine learning is a bra` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html`:307 | `19.1.3` | `print(f'Top chunks: {ids[0]}, scores: {dists[0]}')` | `# Library shortcut: local embeddings + FAISS (pip install sentence-transformers ` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html`:420 | `19.1.5` | `print(result['result'])` | `# Library shortcut: RAG with LangChain (pip install langchain langchain-openai l` |
| `part-5-retrieval-conversation/module-19-rag/section-19.1.html`:776 | `19.1.8` | `print(f'Knowledge base: {len(knowledge_base)} documents')` | `knowledge_base = [ {"id": "doc1", "title": "Vacation Policy", "text": "All full-` |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html`:564 | `19.2.5` | `print(results)` | `# pip install ragas from ragas import evaluate from ragas.metrics import faithfu` |
| `part-5-retrieval-conversation/module-19-rag/section-19.2.html`:636 | `19.2.7` | `print('Baseline results:')` | `from sentence_transformers import SentenceTransformer, CrossEncoder import numpy` |
| `part-5-retrieval-conversation/module-19-rag/section-19.8.html`:117 | `19.8.2` | `for-loop with print()` | `from unstructured.partition.auto import partition # Parse a PDF with OCR fallbac` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html`:704 | `20.3.5` | `for-loop with print()` | `# Mem0: Drop-in memory for any LLM application # pip install mem0ai from mem0 im` |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html`:942 | `20.3.8` | `print(f'Buffer: {len(stm.get_messages())} messages')` | `class ShortTermMemory: def __init__(self, max_turns=10): self.messages = [] self` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html`:99 | `22.1.1` | `print(f'Function: {tool_call.function.name}')` | `from openai import OpenAI client = OpenAI() tools = [ { "type": "function", "fun` |
| `part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html`:157 | `22.1.2` | `for-loop with print()` | `import anthropic client = anthropic.Anthropic() tools = [ { "name": "get_weather` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.1.html`:181 | `26.1.3` | `print(f'Revised prompt: {revised_prompt}')` | `# DALL-E 3 image generation via the OpenAI API # with quality, size, and style p` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.1.html`:372 | `26.1.5` | `for-loop with print()` | `# Zero-shot image classification with CLIP: compute cosine similarity # between ` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.2.html`:193 | `26.2.3` | `print(f'Detected language: {info.language} (probability {info.language_probabili...` | `# Production-ready speech-to-text with faster-whisper # Uses CTranslate2 backend` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.3.html`:157 | `26.3.2` | `for-loop with print()` | `# LayoutLMv3 for document entity extraction # Processes text content, 2D boundin` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html`:415 | `26.5.6` | `print(f'Configured {len(eval_tasks)} evaluation tasks across 3 generalization le...` | `# VLA model evaluation framework # Structured evaluation across generalization a` |
| `part-7-multimodal-applications/module-26-multimodal/section-26.7.html`:691 | `26.7.8` | `print(f'Image size: {image.size}')` | `import requests from PIL import Image from io import BytesIO # Fetch a sample im` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.1.html`:296 | `27.1.3` | `print(f"Resolved: {results['resolved']} / {results['total']}")` | `# Evaluating an agent on SWE-bench (conceptual) from swebench.harness.run_evalua` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.4.html`:202 | `27.4.3` | `print(recommender.chat('I need a laptop for data science work'))` | `from openai import OpenAI client = OpenAI() class ConversationalRecommender: def` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.5.html`:165 | `27.5.3` | `print(scan_for_vulnerabilities(vulnerable_code))` | `# LLM-powered code vulnerability scanner def scan_for_vulnerabilities(code: str,` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.6.html`:186 | `27.6.3` | `print(response.choices[0].message.content)` | `# Creative writing assistant with style control response = client.chat.completio` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.7.html`:357 | `27.7.3` | `print(response.choices[0].message.content)` | `# Using an LLM for mathematical reasoning response = client.chat.completions.cre` |
| `part-7-multimodal-applications/module-27-llm-applications/section-27.7.html`:553 | `27.7.5` | `if-block containing print()` | `import torch import torchaudio import urllib.request import os # Download a samp` |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html`:495 | `28.11.5` | `print(protocol.summarize())` | `# Lab: Complete evaluation protocol for a retrieval-augmented QA system from dat` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.1.html`:374 | `29.1.4` | `print(answer)` | `# implement bedrock_chat import boto3, json def bedrock_chat(prompt: str, model_` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.5.html`:153 | `29.5.2` | `print(response.choices[0].message.content)` | `import openai # Point the standard OpenAI client at the LiteLLM Proxy client = o` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html`:282 | `29.7.5` | `bare string "Using Ollama's API from Python (OpenAI-` | `"""Using Ollama's API from Python (OpenAI-compatible endpoint).""" from openai i` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html`:349 | `29.7.7` | `bare string 'MLX text generation with streaming.'` | `"""MLX text generation with streaming.""" from mlx_lm import load, generate # Lo` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.7.html`:480 | `29.7.10` | `bare string 'Benchmark two quantization levels on th` | `"""Benchmark two quantization levels on the same prompts.""" import time import ` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.9.html`:659 | `29.9.2a` | `print('Manual Benchmark (10 sequential requests):')` | `import requests import time import statistics def measure_request(prompt, max_to` |
| `part-8-evaluation-production/module-29-production-engineering/section-29.9.html`:762 | `29.9.5a` | `print(stats[['Name', 'Request Count', 'Median Response Time', '95% Response Time...` | `import pandas as pd # Analyze the Locust CSV output stats = pd.read_csv("results` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html`:935 | `30.1.9` | `print(f'Messages: {len(msgs)} (sandwich pattern)')` | `class SandwichDefense: """Layer 3: Wrap user input with defensive instructions."` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html`:269 | `30.12.4` | `print(f'Using sigma={optimizer.noise_multiplier:.4f} for ({EPSILON}, {DELTA})-DP...` | `# DP-SGD fine-tuning with Opacus import torch from torch.utils.data import DataL` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.2.html`:199 | `30.2.3` | `print(check_faithfulness(source, 'The Eiffel Tower is 330 meters tall.'))` | `# implement check_faithfulness from transformers import pipeline nli = pipeline(` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html`:460 | `30.10.3` | `print(f"{'Language':<12} {'Tokens':>7} {'Chars':>6} {'Tok/Char':>9}")` | `# Measuring tokenization efficiency across languages # Demonstrates the "tokeniz` |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.8.html`:110 | `30.8.1` | `for-loop with print()` | `# PyRIT automated red teaming example from pyrit.orchestrator import PromptSendi` |

### 2.2 Uncaptioned blocks missing output (95)

Top 25 files by uncaptioned-block count:

| File | # blocks |
|---|---:|
| `appendices/appendix-c-python-for-llm/section-c.1.html` | 5 |
| `appendices/appendix-n-distributed-ml/section-n.4.html` | 4 |
| `appendices/appendix-b-ml-essentials/section-b.4.html` | 3 |
| `appendices/appendix-n-distributed-ml/section-n.1.html` | 3 |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.2.html` | 3 |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html` | 3 |
| `appendices/appendix-h-prompt-templates/section-h.3.html` | 2 |
| `appendices/appendix-i-datasets-benchmarks/section-i.1.html` | 2 |
| `part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html` | 2 |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` | 2 |
| `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` | 2 |
| `part-1-foundations/module-04-transformer-architecture/section-4.2.html` | 2 |
| `part-1-foundations/module-05-decoding-text-generation/section-5.3.html` | 2 |
| `part-10-frontiers/module-33-emerging-architectures/section-33.3.html` | 2 |
| `part-10-frontiers/module-33-emerging-architectures/section-33.7.html` | 2 |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html` | 2 |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html` | 2 |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html` | 2 |
| `part-6-agentic-ai/module-23-multi-agent-systems/section-23.1.html` | 2 |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html` | 2 |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html` | 2 |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` | 2 |
| `appendices/appendix-h-prompt-templates/section-h.2.html` | 1 |
| `appendices/appendix-h-prompt-templates/section-h.4.html` | 1 |
| `appendices/appendix-h-prompt-templates/section-h.5.html` | 1 |

## 3. Pattern B - Caption/prose references with pairing issues

Prose or caption text mentions `Code Fragment X.Y.Z` but the target is either missing, in another file, or far away (> 3000 chars) in the same file. Self-references (a caption mentioning its own number) are excluded.

### 3.2 `stale` references (266)

Sorted by distance descending. The largest distances are almost always references in end-of-chapter exercises pointing back to fragments earlier in the chapter; these are valid long-range references, not refactor leftovers. Pay attention to references with distances **< 10,000 chars** in particular: those are most likely to be unintended.

| File:Line | Container | Cited as | Detail | Context |
|---|---|---|---|---|
| `part-7-multimodal-applications/module-26-multimodal/section-26.5.html`:514 | `li` | `26.5.6` | target in same file but 3253 chars away | Evaluation design. Using Code Fragment 26.5.6, design an evaluation suite for a kitchen robot that t |
| `part-8-evaluation-production/module-28-evaluation-observability/section-28.7.html`:355 | `p` | `28.7.6` | target in same file but 3356 chars away | Code Fragment 28.7.6 below shows how to build and run the container with configuration overrides and |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html`:215 | `p` | `11.1.4` | target in same file but 3428 chars away | Code Fragment 11.1.4 demonstrates the approach described above. |
| `part-3-working-with-llms/module-11-llm-apis/section-11.1.html`:245 | `p` | `11.1.5` | target in same file but 3477 chars away | Anthropic's prompt caching feature is particularly valuable when you repeatedly send requests with a |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html`:499 | `li` | `9.7.6` | target in same file but 3573 chars away | Profiling practice. Using Code Fragment 9.7.6, profile an inference pass through a HuggingFace model |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html`:186 | `p` | `12.4.2` | target in same file but 3691 chars away | Code Fragment 12.4.2 demonstrates injection defenses. |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.2.html`:197 | `p` | `30.2.2` | target in same file but 3751 chars away | Natural Language Inference (NLI) models classify whether a claim is entailed by, contradicts, or is  |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html`:269 | `p` | `12.3.2` | target in same file but 3897 chars away | Code Fragment 12.3.2 illustrates a chat completion call. |
| `part-3-working-with-llms/module-11-llm-apis/section-11.3.html`:387 | `p` | `11.3.7` | target in same file but 3912 chars away | Helicone is an open-source observability proxy focused on request logging, cost tracking, and analyt |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.7.html`:66 | `p` | `15.7.1` | target in same file but 4070 chars away | The simplest context extension method is linear scaling, also called position interpolation. Instead |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html`:748 | `li` | `30.10.6` | target in same file but 4151 chars away | Tokenization audit. Using Code Fragment 30.10.6, extend the analysis to 20 languages spanning Latin, |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.7.html`:158 | `p` | `30.7.2` | target in same file but 4272 chars away | An alternative to gradient ascent is task vector negation. A "task vector" is the difference between |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html`:476 | `p` | `10.1.6` | target in same file but 4513 chars away | The tuned lens provides cleaner, more interpretable results than the raw logit lens, especially in e |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.4.html`:201 | `p` | `15.4.3` | target in same file but 4523 chars away | Code Fragment 15.4.3 shows how to call the fine-tuned model using the standard chat completions API. |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html`:425 | `p` | `12.3.5` | target in same file but 4639 chars away | Code Fragment 12.3.5 shows the RLHF loop. |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html`:750 | `li` | `30.10.6` | target in same file but 4750 chars away | Pluralistic reward analysis. Modify Code Fragment 30.10.6 to accept synthetic annotator scores drawn |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html`:91 | `p` | `6.8.1` | target in same file but 4890 chars away | Code Fragment 6.8.1 shows how to configure multi-axis parallelism in Megatron-Core. The TransformerC |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html`:210 | `p` | `10.3.3` | target in same file but 4922 chars away | Code Fragment 10.3.3 shows how to use SHAP with a language model by wrapping the model's prediction  |
| `part-4-training-adapting/module-16-peft/section-16.1.html`:223 | `p` | `16.1.2` | target in same file but 4945 chars away | Code Fragment 16.1.2 configures LoRA adapters. |
| `part-4-training-adapting/module-16-peft/section-16.2.html`:106 | `p` | `16.2.2` | target in same file but 5004 chars away | The following implementation (Code Fragment 16.2.2) shows how to enable DoRA with a single configura |
| `part-3-working-with-llms/module-11-llm-apis/section-11.4.html`:116 | `p` | `11.4.2` | target in same file but 5088 chars away | Anthropic's approach to reasoning uses the existing Messages API with an additional thinking configu |
| `part-5-retrieval-conversation/module-19-rag/section-19.5.html`:188 | `p` | `19.5.3` | target in same file but 5098 chars away | Once the schema context is prepared, the next step is generating executable SQL from the user's natu |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html`:119 | `p` | `15.1.1` | target in same file but 5119 chars away | Fine-tuning a 7-billion-parameter model on a single GPU was science fiction in 2020. By 2024, it had |
| `part-4-training-adapting/module-16-peft/section-16.2.html`:157 | `p` | `16.2.4` | target in same file but 5124 chars away | Code Fragment 16.2.4 demonstrates the bottleneck adapter pattern using LLaMA -Adapter style chapters |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html`:446 | `p` | `12.1.5` | target in same file but 5139 chars away | Code Fragment 12.1.5 defines a prompt template. |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html`:121 | `p` | `12.2.2` | target in same file but 5163 chars away | Code Fragment 12.2.2 illustrates a chat completion call. |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html`:194 | `p` | `15.2.2` | target in same file but 5215 chars away | When fine-tuning on multiple tasks (summarization, Q&A, code generation), you rarely have equal amou |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.2.html`:248 | `p` | `15.2.5` | target in same file but 5291 chars away | The Hugging Face datasets library provides a streaming, memory-efficient pipeline for loading, filte |
| `part-2-understanding-llms/module-10-interpretability/section-10.2.html`:419 | `p` | `10.2.4` | target in same file but 5334 chars away | Code Fragment 10.2.4 demonstrates how nnsight wraps any PyTorch model to enable inspection and modif |
| `part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html`:543 | `p` | `25.6.6` | target in same file but 5353 chars away | Extend the PolicyEngine from Code Fragment 25.6.6 with support for time-based rules (e.g., "no refun |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html`:204 | `p` | `10.3.3` | target in same file but 5355 chars away | SHAP (SHapley Additive exPlanations) adapts Shapley values from cooperative game theory to feature   |
| `part-2-understanding-llms/module-10-interpretability/section-10.2.html`:418 | `p` | `10.2.4` | target in same file but 5390 chars away | Code Fragment 10.2.4 demonstrates this approach. |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.7.html`:275 | `p` | `30.7.3` | target in same file but 5479 chars away | Measuring whether unlearning actually worked requires checking three dimensions: whether the model h |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html`:372 | `p` | `10.1.4` | target in same file but 5534 chars away | Lesson: Probing reveals what information a model has versus what it uses; when a model "knows" somet |
| `part-2-understanding-llms/module-09-inference-optimization/section-9.6.html`:99 | `p` | `9.6.1` | target in same file but 5590 chars away | Reasoning model APIs follow the same chat completion interface as standard models, but with addition |
| `part-2-understanding-llms/module-10-interpretability/section-10.3.html`:493 | `p` | `10.3.6` | target in same file but 5693 chars away | Concept erasure removes specific information from model representations, ensuring the model cannot   |
| `part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.4.html`:518 | `p` | `15.4.8` | target in same file but 5737 chars away | Fireworks AI differentiates itself through its optimized inference engine (FireAttention) and its su |
| `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html`:560 | `p` | `30.3.4` | target in same file but 5909 chars away | Code Fragment 30.3.4 demonstrates the pattern: ask an LLM to rate offensiveness from the perspective |
| `part-4-training-adapting/module-14-synthetic-data/section-14.4.html`:287 | `p` | `14.4.3` | target in same file but 6184 chars away | Code Fragment 14.4.3 demonstrates this approach. |
| `part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html`:184 | `p` | `12.1.2` | target in same file but 6185 chars away | Code Fragment 12.1.2 contrasts a vague prompt with a constrained one, showing how specificity transf |

... and 226 more `stale` rows.

## 4. Anchor verification - Section 30.3.4 orphan-output bug

The previously-fixed bug was a `<div class="code-output">` block that appeared in the source file without an immediately preceding `<pre>...</pre>`. We scan the entire book for any other `code-output` div whose previous element-level sibling is not a `<pre>` (or a `code-block-wrapper` containing one).

Found **8** orphan output blocks across **6** files.

| File:Line | Output preview |
|---|---|
| `appendices/appendix-c-python-for-llm/section-c.1.html`:152 | Output: CUDA available: True Device count: 1 GPU name: NVIDIA A100-SXM4-80GB GPU memory: 79.6 GB |
| `appendices/appendix-c-python-for-llm/section-c.1.html`:158 | Output: Training examples: 8923 |
| `appendices/appendix-d-environment-setup/section-d.2.html`:48 | Output: nvcc: NVIDIA (R) Cuda compiler driver Cuda compilation tools, release 12.4, V12.4.131 True |
| `part-2-understanding-llms/module-10-interpretability/section-10.1.html`:312 | Output: Epoch 5: loss=1.2043 Epoch 10: loss=0.5871 Layer 0: POS accuracy = 0.612 Layer 3: POS accuracy = 0.784 Layer 6: POS accuracy = 0.891 |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.2.html`:178 | Output: You are Chef Marco, a passionate Italian home cooking instructor. \#\# Background You grew up in a small kitchen in Bologna, learnin |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html`:322 | Output: [summary] Discussed database options: PostgreSQL vs MongoDB. User leaning toward P... (score: 0.847) [fact] User is building a recip |
| `part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html`:592 | Output: Memory: User is vegetarian (relevance: 0.891) Memory: User loves Italian food (relevance: 0.847) Memory: User has a gluten allergy ( |
| `part-6-agentic-ai/module-21-ai-agents/section-21.5.html`:261 | Output: Completed. Step 1 (lookup_order): success, 0.3s, \$0.002 Step 2 (issue_refund): success, 0.5s, \$0.003 |

## 5. Recommended next steps

- **Pattern A (167 blocks):** For each block, decide if (a) the code is illustrative and we should add a `# Output:` comment to a `<div class="code-output">`, (b) the original output was lost during refactoring and needs reconstruction (run the code, paste the result), or (c) the `print(...)` is incidental and we should leave it. Highest priority: blocks whose caption explicitly says "prints X" or "outputs Y".
- **Pattern B / stale (266 refs):** Target exists in the same file but is more than ~50 lines away. Often a leftover from a refactor that moved the fragment but did not move the surrounding prose.
- **Orphan `code-output` divs (8 found):** Re-pair each block with the correct preceding `<pre>` or delete the output if the code was removed during a refactor (this is the Section 30.3.4 anchor pattern).
- **Re-run after fixes:** `/c/Python314/python scripts/_audit_code_output_pairing.py`
