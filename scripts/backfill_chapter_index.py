"""Backfill canonical chapter-index elements:
  - Epigraph (with AI-agent attribution)
  - Looking-Back callout
  - Prerequisites block (<div class="prereqs">)
  - What's-Next block (only 1 chapter needs this)

The script is idempotent: it only inserts what is missing per the audit.
For chapters that already have a `Note: Prerequisites` callout, it converts
the callout to the canonical `<div class="prereqs">` form (preserving the
existing list items).

Usage:
  python scripts/backfill_chapter_index.py [--dry-run]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(r'E:/Projects/BookBlogsHome/LLMBook')

# ------------------------------------------------------------
# AGENT CAST (slug -> color, persona description for cite block)
# ------------------------------------------------------------

AGENT_COLORS = {
    'tensor': '#3498db', 'lexica': '#9b59b6', 'token': '#d35400',
    'attn': '#e94560', 'norm': '#95a5a6', 'sage': '#7f8c8d',
    'pip': '#3498db', 'chinchilla': '#8e44ad', 'spectra': '#3498db',
    'bert': '#f39c12', 'greedy': '#27ae60', 'quant': '#1abc9c',
    'kv': '#16a085', 'probe': '#34495e', 'prompt': '#16a085',
    'synth': '#f1c40f', 'finetune': '#27ae60', 'lora': '#27ae60',
    'reward': '#2ecc71', 'distill': '#1abc9c', 'pixel': '#1abc9c',
    'vec': '#8e44ad', 'rag': '#2980b9', 'echo': '#f39c12',
    'compass': '#34495e', 'census': '#9b59b6', 'label': '#d35400',
    'eval': '#7f8c8d', 'sentinel': '#e67e22', 'guard': '#c0392b',
    'scale': '#2c3e50', 'deploy': '#2c3e50', 'frontier': '#e94560',
    'context': '#7f8c8d', 'cosine': '#9b59b6', 'merge': '#27ae60',
    'sched': '#34495e', 'sparky': '#f39c12', 'hallux': '#c0392b',
    'batch': '#16a085', 'loss': '#e67e22', 'dropout': '#95a5a6',
}

# Human-readable agent display names (for alt and cite).
AGENT_NAMES = {
    'tensor': 'Tensor', 'lexica': 'Lexica', 'token': 'Token',
    'attn': 'Attn', 'norm': 'Norm', 'sage': 'Sage',
    'pip': 'Pip', 'chinchilla': 'Chinchilla', 'spectra': 'Spectra',
    'bert': 'Bert', 'greedy': 'Greedy', 'quant': 'Quant',
    'kv': 'KV', 'probe': 'Probe', 'prompt': 'Prompt',
    'synth': 'Synth', 'finetune': 'Finetune', 'lora': 'LoRA',
    'reward': 'Reward', 'distill': 'Distill', 'pixel': 'Pixel',
    'vec': 'Vec', 'rag': 'RAG', 'echo': 'Echo',
    'compass': 'Compass', 'census': 'Census', 'label': 'Label',
    'eval': 'Eval', 'sentinel': 'Sentinel', 'guard': 'Guard',
    'scale': 'Scale', 'deploy': 'Deploy', 'frontier': 'Frontier',
    'context': 'Context', 'cosine': 'Cosine', 'merge': 'Merge',
    'sched': 'Sched', 'sparky': 'Sparky', 'hallux': 'Hallux',
    'batch': 'Batch', 'loss': 'Loss', 'dropout': 'Dropout',
}

# ------------------------------------------------------------
# Chapter metadata: {file_rel: {prev_label, prev_href, prev_topic,
#                               adj_label, adj_href, adj_topic,
#                               agent, persona, quote, bridge_summary,
#                               next_summary_topic, prereqs_html_list}}
# ------------------------------------------------------------

# Each row authors all four optional blocks. For chapters already
# present in the book that already passed the audit on a given block,
# we never overwrite (the script checks for existing markers).
#
# `prereqs_items` is a list of HTML <li>...</li> fragments.
# `looking_back_html` is the inner HTML of the <div class="callout looking-back">.
# `epigraph_quote` is the line in quotes (no surrounding quotes).
# `agent` is the canonical slug used for color + img.
# `persona` is the description shown after the comma (e.g. "Sage").
# `next_paragraph` is the inner paragraph of the whats-next block (only
# used for the single chapter that lacks one).

CHAPTERS = {
    # Part 1: LLM Building Blocks
    'part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html': {
        'agent': 'tensor', 'persona': 'Fundamentals-Obsessed',
        'epigraph_quote': "Every expert was once a beginner who refused to skip the fundamentals.",
        'looking_back_html': "This is where the book begins. You arrive with Python, curiosity, and (we assume) some prior exposure to machine learning. Everything before this chapter is the front matter that told you what the book covers, who it is for, and how to read it. From here on, every chapter <em>builds</em>: by the end of Part I you will have written a working Transformer; by the end of the book you will have shipped an agent into production.",
        'prereqs_items': [
            "Python proficiency (functions, classes, list comprehensions, decorators)",
            "Basic linear algebra: vectors, matrices, dot products",
            "Basic probability: distributions, expectation, Bayes' theorem",
            "No prior ML experience required",
        ],
    },
    'part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html': {
        'agent': 'lexica', 'persona': 'Distributional',
        'epigraph_quote': "A word is characterized by the company it keeps.",
        'looking_back_html': "Chapter 0 gave you the PyTorch foundations: tensors, autograd, the training loop. Now we turn from generic deep learning to the specific problem this book is about: how do you represent <em>text</em> as numbers a model can learn from? The chapter starts with the classical answers (bag-of-words, n-grams, TF-IDF), shows what they got wrong, and ends with the embedding revolution (Word2Vec, GloVe) that made transformers possible.",
        'prereqs_items': [
            'Familiarity with PyTorch training basics from <a href="../module-00-ml-pytorch-foundations/index.html">Chapter 0: ML and PyTorch Foundations</a>',
            "Linear algebra: vectors, dot products, matrix multiplication",
            "Basic NumPy and Python comfort",
        ],
    },
    'part-1-llm-building-blocks/module-02-sequence-models-attention/index.html': {
        'agent': 'attn', 'persona': 'Sequence-Tracking',
        'epigraph_quote': "Attention is all you need, but understanding it is what you'll keep.",
        'looking_back_html': "Chapter 1 turned words into vectors. Sequences of words demand a different idea: a model that carries information from one position to the next. This chapter walks the road from RNNs and LSTMs to attention, then to self-attention; by the end you'll see why the Transformer (next chapter) replaced everything that came before.",
        'prereqs_items': [
            'Word embeddings and tokenization from <a href="../module-01-foundations-nlp-text-representation/index.html">Chapter 1</a>',
            'PyTorch nn.Module and training loops from <a href="../module-00-ml-pytorch-foundations/index.html">Chapter 0</a>',
            "Basic calculus (gradients, chain rule) at an intuitive level",
        ],
    },
    'part-1-llm-building-blocks/module-03-transformer-architecture/index.html': {
        'agent': 'attn', 'persona': 'Architecturally-Inclined',
        'epigraph_quote': "The Transformer didn't just win; it ended the debate about which architecture deserved the GPU budget.",
        'looking_back_html': "Chapter 2 traced the path from RNNs to self-attention. Now we assemble the full Transformer block: multi-head attention, positional encodings, residual streams, and the layer norms that keep gradients sane. This is the architecture every model in the rest of the book is built on.",
        'prereqs_items': [
            'Self-attention intuition from <a href="../module-02-sequence-models-attention/index.html">Chapter 2</a>',
            'Word embeddings and tokenization from <a href="../module-01-foundations-nlp-text-representation/index.html">Chapter 1</a>',
            'PyTorch building blocks (Linear, LayerNorm, Embedding) from <a href="../module-00-ml-pytorch-foundations/index.html">Chapter 0</a>',
        ],
    },
    'part-1-llm-building-blocks/module-04-decoding-text-generation/index.html': {
        'agent': 'greedy', 'persona': 'Sampling-Discerning',
        'epigraph_quote': "A trained model proposes; a decoder disposes.",
        'looking_back_html': "Chapter 3 built the Transformer that outputs a distribution over the next token. This chapter is everything that happens <em>after</em> that distribution: greedy, beam, top-k, top-p, temperature, and the speculative-decoding tricks that make real-time chat feasible.",
        'prereqs_items': [
            'Transformer architecture from <a href="../module-03-transformer-architecture/index.html">Chapter 3</a>',
            "Basic probability (softmax, distributions, log-likelihood)",
            "Comfort reading PyTorch inference code",
        ],
    },
    'part-1-llm-building-blocks/module-05-tools-of-the-trade/index.html': {
        'agent': 'pip', 'persona': 'Toolbox-Curating',
        'epigraph_quote': "Knowing the names of the right tools is half the job; the other half is knowing when to put them down.",
        'looking_back_html': "Chapters 0 through 4 built the conceptual core: ML, NLP, attention, the Transformer, and decoding. This chapter is the practical toolkit that ties them together: PyTorch + Hugging Face + tokenizers + the small habits that distinguish a working LLM engineer from someone who has only read about it.",
        'prereqs_items': [
            'All concepts from <a href="../module-00-ml-pytorch-foundations/index.html">Chapters 0</a> through <a href="../module-04-decoding-text-generation/index.html">4</a>',
            "Comfortable Python development setup (virtualenv, pip, git)",
            "Familiarity with the Hugging Face ecosystem helps but is not required",
        ],
    },
    # Part 2: Understanding LLMs
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html': {
        'agent': 'scale', 'persona': 'Computationally-Devout',
        'epigraph_quote': "The biggest lesson from 70 years of AI research: general methods that leverage computation are ultimately the most effective.",
        'looking_back_html': "Part I built up to a working Transformer. That Transformer needs to be <em>trained</em> on something, and that something is most of the internet. This chapter zooms out from the architecture to the training recipe: data, objectives, and the scaling laws that predict performance before a million dollars of compute is spent.",
        'prereqs_items': [
            'Transformer architecture from <a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>',
            'Tokenization and subword models from <a href="../../part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html">Chapter 1</a>',
            'PyTorch training loops from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html">Chapter 0</a>',
            "Comfort with basic information theory (cross-entropy, perplexity)",
        ],
    },
    'part-2-understanding-llms/module-07-modern-llm-landscape/index.html': {
        'agent': 'sage', 'persona': 'Landscape-Surveying',
        'epigraph_quote': "If you cannot name the model families and their lineages, you cannot reason about which one to ship.",
        'looking_back_html': 'Chapter 6 covered how a frontier model gets pretrained. This chapter surveys the model zoo that pretraining produced: GPT-4 and 5, Claude 3.5 and 4, Llama 3 and 4, Gemini, Mistral, Qwen, DeepSeek, and the smaller open-weight crowd. We map them by training recipe, parameter count, license, and the deployment niche each one wins.',
        'prereqs_items': [
            'Pretraining and scaling laws from <a href="../module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
            'Transformer architecture from <a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>',
            "General familiarity with the contemporary model landscape (no deep operational experience needed)",
        ],
    },
    'part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html': {
        'agent': 'sage', 'persona': 'Step-by-Step',
        'epigraph_quote': "If you can spend more compute at inference, you can sometimes skip a thousand hours of training.",
        'looking_back_html': 'Chapter 7 mapped the model landscape; this chapter dives into the new axis that o1, R1, and Claude Sonnet 4.5 opened: <em>test-time compute</em>. We cover chain-of-thought, tree search, self-consistency, and the reasoning-model class that turns inference into a search problem.',
        'prereqs_items': [
            'Modern LLM families from <a href="../module-07-modern-llm-landscape/index.html">Chapter 7</a>',
            'Decoding strategies from <a href="../../part-1-llm-building-blocks/module-04-decoding-text-generation/index.html">Chapter 4</a>',
            "Basic notions of search and dynamic programming",
        ],
    },
    'part-2-understanding-llms/module-09-inference-optimization/index.html': {
        'agent': 'quant', 'persona': 'Bandwidth-Conscious',
        'epigraph_quote': "Inference is where the money is spent and where the latency is felt.",
        'looking_back_html': 'Chapter 8 spent extra compute at inference for quality; this chapter spends less compute at inference for cost and latency. Quantization, KV caching, paged attention, FlashAttention, speculative decoding, and continuous batching all sit on the same Transformer (<a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>) you already understand.',
        'prereqs_items': [
            'Transformer internals from <a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>',
            'Decoding strategies from <a href="../../part-1-llm-building-blocks/module-04-decoding-text-generation/index.html">Chapter 4</a>',
            "Basic GPU memory model (HBM, on-chip SRAM)",
        ],
    },
    'part-2-understanding-llms/module-10-interpretability/index.html': {
        'agent': 'probe', 'persona': 'Mechanistically-Curious',
        'epigraph_quote': "If we cannot read what the model has learned, we cannot trust where it is taking us.",
        'looking_back_html': 'Chapters 6 through 9 explained <em>how</em> LLMs are built and run. This chapter asks <em>what</em> they have actually learned: linear probes, mechanistic circuits, sparse autoencoders, and the open question of whether we can ever explain a model to itself.',
        'prereqs_items': [
            'Transformer architecture from <a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>',
            'Pretraining dynamics from <a href="../module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
            "Basic linear algebra (eigenvectors, projections)",
        ],
    },
    # Part 3
    'part-3-working-with-llms/module-11-llm-apis/index.html': {
        'agent': 'pip', 'persona': 'API-Wrangling',
        'epigraph_quote': "The fastest path from idea to working LLM feature is almost always a hosted API.",
        'looking_back_html': 'Part II explained what LLMs are. Part III starts using them. This chapter covers the API surface every LLM provider exposes: chat, completion, streaming, function calling, structured outputs, and the rate-limit and cost dance that follows.',
        'prereqs_items': [
            'Modern LLM landscape from <a href="../../part-2-understanding-llms/module-07-modern-llm-landscape/index.html">Chapter 7</a>',
            "Python HTTP basics (requests, async/await)",
            "Comfort with JSON and REST",
        ],
    },
    'part-3-working-with-llms/module-12-prompt-engineering/index.html': {
        'agent': 'prompt', 'persona': 'Verbally-Persuasive',
        'epigraph_quote': "A prompt is a program written in English; debug it like one.",
        'looking_back_html': 'Chapter 11 connected you to the API. This chapter teaches the discipline of <em>what to say</em>: zero-shot, few-shot, chain-of-thought, self-consistency, ReAct, and the small craft of getting consistent answers from a probabilistic system.',
        'prereqs_items': [
            'LLM API basics from <a href="../module-11-llm-apis/index.html">Chapter 11</a>',
            'Reasoning models from <a href="../../part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html">Chapter 8</a>',
            "An OpenAI or Anthropic API key for the hands-on labs",
        ],
    },
    'part-3-working-with-llms/module-13-hybrid-ml-llm/index.html': {
        'agent': 'compass', 'persona': 'Architecturally-Pragmatic',
        'epigraph_quote': "An LLM is not the answer to every problem; sometimes the answer is half LLM and half boring ML.",
        'looking_back_html': 'Chapter 12 taught you how to ask an LLM a question. This chapter teaches you when <em>not</em> to ask. We cover hybrid architectures that mix classical ML for the high-volume slice with LLM calls for the long tail, and how to decide which is which.',
        'prereqs_items': [
            'LLM API and prompt patterns from <a href="../module-11-llm-apis/index.html">Chapters 11</a> and <a href="../module-12-prompt-engineering/index.html">12</a>',
            'Classical ML foundations from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html">Chapter 0</a>',
            "Comfort with cost, latency, and accuracy tradeoffs",
        ],
    },
    'part-3-working-with-llms/module-14-tools-of-the-trade/index.html': {
        'agent': 'pip', 'persona': 'Workflow-Optimizing',
        'epigraph_quote': "The right SDK shaves a week off your prototype; the wrong one adds two months of integration work.",
        'looking_back_html': 'Chapters 11 through 13 covered the API, the prompt, and the hybrid decision. This chapter is the SDK toolbox: LangChain, LiteLLM, Instructor, Outlines, structured outputs, observability, and the small libraries that let you build LLM apps quickly without locking yourself to one vendor.',
        'prereqs_items': [
            'LLM API basics from <a href="../module-11-llm-apis/index.html">Chapter 11</a>',
            'Prompt engineering patterns from <a href="../module-12-prompt-engineering/index.html">Chapter 12</a>',
            "Python development comfort (pip, virtualenv, git)",
        ],
    },
    # Part 4
    'part-4-training-adaptation/module-15-synthetic-data/index.html': {
        'agent': 'synth', 'persona': 'Self-Generating',
        'epigraph_quote': "When real data runs out, the model trains on its own children.",
        'looking_back_html': 'Part III used LLMs through APIs. Part IV trains and adapts them. This chapter starts with the data problem: how to generate training data when the real version is scarce, private, or simply nonexistent. Self-instruct, Evol-Instruct, distillation, and the contamination traps that follow.',
        'prereqs_items': [
            'Working with LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            'Prompt engineering from <a href="../../part-3-working-with-llms/module-12-prompt-engineering/index.html">Chapter 12</a>',
            'Pretraining objectives from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
        ],
    },
    'part-4-training-adaptation/module-16-fine-tuning-fundamentals/index.html': {
        'agent': 'finetune', 'persona': 'Gradient-Loving',
        'epigraph_quote': "Fine-tuning is pretraining in miniature, on your own data, with your own bugs.",
        'looking_back_html': 'Chapter 15 produced the training data; this chapter trains a model on it. Full fine-tuning, instruction tuning, SFT, the optimizer choices, and the failure modes (catastrophic forgetting, overfitting on a tiny corpus) that every team meets the first time.',
        'prereqs_items': [
            'Pretraining objectives from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
            'Synthetic data from <a href="../module-15-synthetic-data/index.html">Chapter 15</a>',
            'PyTorch training loops from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html">Chapter 0</a>',
            "Access to at least one capable GPU for the hands-on labs",
        ],
    },
    'part-4-training-adaptation/module-17-peft/index.html': {
        'agent': 'lora', 'persona': 'Parameter-Efficient',
        'epigraph_quote': "You can adapt a 70-billion-parameter model by training less than 1 percent of it.",
        'looking_back_html': 'Chapter 16 was full fine-tuning, which is expensive. This chapter is the cheap version: LoRA, QLoRA, adapters, prefix tuning, and the merging, distillation, and quantization tricks that turn a 70B-parameter giant into something you can fine-tune on a single GPU.',
        'prereqs_items': [
            'Fine-tuning fundamentals from <a href="../module-16-fine-tuning-fundamentals/index.html">Chapter 16</a>',
            'Inference optimization from <a href="../../part-2-understanding-llms/module-09-inference-optimization/index.html">Chapter 9</a>',
            'Transformer internals from <a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>',
        ],
    },
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html': {
        'agent': 'reward', 'persona': 'Preference-Optimizing',
        'epigraph_quote': "We don't tell models what to say; we teach them which answer we'd rather have.",
        'looking_back_html': 'Chapters 16 and 17 taught a model the shape of a task. This chapter teaches it the shape of <em>good</em>: RLHF, DPO, KTO, IPO, ORPO, and the constitutional-AI style techniques that turn a capable model into a helpful, honest, harmless one.',
        'prereqs_items': [
            'Fine-tuning from <a href="../module-16-fine-tuning-fundamentals/index.html">Chapter 16</a>',
            'Reinforcement-learning basics from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html">Chapter 0</a>',
            'Pretraining dynamics from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
        ],
    },
    'part-4-training-adaptation/module-19-tools-of-the-trade/index.html': {
        'agent': 'pip', 'persona': 'Workflow-Optimizing',
        'epigraph_quote': "The training stack is half framework, half plumbing, and entirely opinionated.",
        'looking_back_html': 'Chapters 15 through 18 built models. This chapter is the framework grid: TRL, Unsloth, Axolotl, PEFT, DeepSpeed, accelerate, plus the small command-line habits that turn a one-off experiment into a reproducible pipeline.',
        'prereqs_items': [
            'Fine-tuning experience from <a href="../module-16-fine-tuning-fundamentals/index.html">Chapter 16</a>',
            'PEFT methods from <a href="../module-17-peft/index.html">Chapter 17</a>',
            "Python project hygiene (envs, requirements, CLI tools)",
        ],
    },
    # Part 5
    'part-5-multimodal-llms/module-20-audio-music-generation/index.html': {
        'agent': 'echo', 'persona': 'Pitch-Perfect',
        'epigraph_quote': "Speech, music, and video are just more tokens; the trick is choosing the right vocabulary.",
        'looking_back_html': 'Part IV trained text models. Part V opens the modalities: audio, vision, 3D, and the cross-modal reasoning that ties them together. This chapter starts with audio: Whisper, MusicGen, AudioLDM, the codec models, and the production pipelines that handle speech and music together.',
        'prereqs_items': [
            'Modern LLM landscape from <a href="../../part-2-understanding-llms/module-07-modern-llm-landscape/index.html">Chapter 7</a>',
            'Transformer architecture from <a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>',
            "Basic familiarity with audio formats (waveforms, spectrograms, sampling rate)",
        ],
    },
    'part-5-multimodal-llms/module-21-document-understanding-ocr/index.html': {
        'agent': 'label', 'persona': 'Document-Parsing',
        'epigraph_quote': "The hardest data is the data your colleagues already think they have.",
        'looking_back_html': 'Chapter 20 handled audio; this chapter handles the other dirty modality every enterprise meets: documents. PDFs, scanned forms, tables, and the OCR-plus-VLM pipelines that turn them into structured outputs an LLM can reason over.',
        'prereqs_items': [
            'Modern LLM landscape from <a href="../../part-2-understanding-llms/module-07-modern-llm-landscape/index.html">Chapter 7</a>',
            'LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            "Familiarity with one VLM (GPT-4o, Claude, Gemini) at the API level",
        ],
    },
    'part-5-multimodal-llms/module-22-vision-language-models/index.html': {
        'agent': 'pixel', 'persona': 'Pipeline-Skeptical',
        'epigraph_quote': "Vision-language models did not learn to see; they learned to align.",
        'looking_back_html': 'Chapters 20 and 21 covered audio and documents. This chapter is the rest of the visual world: CLIP, LLaVA, GPT-4o, Claude Vision, Gemini, and the omni-modal architectures that read images, listen, and reply in any modality.',
        'prereqs_items': [
            'Transformer architecture from <a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>',
            'Document understanding from <a href="../module-21-document-understanding-ocr/index.html">Chapter 21</a>',
            'LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
        ],
    },
    'part-5-multimodal-llms/module-23-3d-generation-neural-scenes/index.html': {
        'agent': 'pixel', 'persona': 'Splat-Curious',
        'epigraph_quote': "Three dimensions is two dimensions plus a lot of opinions about light.",
        'looking_back_html': 'Chapter 22 mapped the 2D vision world. This chapter goes one dimension up: NeRFs, Gaussian splatting, neural scene representations, and the LLM-driven prompting that lets you generate, edit, or relight a 3D scene from text.',
        'prereqs_items': [
            'Vision-language models from <a href="../module-22-vision-language-models/index.html">Chapter 22</a>',
            "Basic 3D-graphics literacy (meshes, lighting, cameras) helps but is not strictly required",
            "Comfort with the modern multimodal API surface",
        ],
    },
    'part-5-multimodal-llms/module-24-vla-models/index.html': {
        'agent': 'compass', 'persona': 'Embodied',
        'epigraph_quote': "An LLM that can move a robot must first be told what an arm even is.",
        'looking_back_html': 'Chapters 22 and 23 stayed inside the screen. This chapter steps out: Vision-Language-Action (VLA) models such as RT-2, OpenVLA, and Pi 0 turn a VLM into a policy that drives real or simulated robots. We cover the architecture, the training data, and the safety story.',
        'prereqs_items': [
            'Vision-language models from <a href="../module-22-vision-language-models/index.html">Chapter 22</a>',
            'Reinforcement-learning basics from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html">Chapter 0</a>',
            "Some prior exposure to robotics or control helps but is optional",
        ],
    },
    'part-5-multimodal-llms/module-25-tools-of-the-trade/index.html': {
        'agent': 'pip', 'persona': 'Multimodal-Outfitted',
        'epigraph_quote': "Multimodal stacks are still one OS install away from being a hobby.",
        'looking_back_html': 'Chapters 20 through 24 walked the modalities one by one. This chapter is the multimodal toolkit: which library handles audio well, which one handles documents, which one is opinionated about VLMs, and how to wire them together without a YAML graveyard.',
        'prereqs_items': [
            'At least one of <a href="../module-20-audio-music-generation/index.html">Chapter 20</a>, <a href="../module-21-document-understanding-ocr/index.html">21</a>, <a href="../module-22-vision-language-models/index.html">22</a>, <a href="../module-23-3d-generation-neural-scenes/index.html">23</a>, or <a href="../module-24-vla-models/index.html">24</a>',
            'LLM API tooling from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/index.html">Chapter 14</a>',
            "Python and shell comfort",
        ],
    },
    # Part 6
    'part-6-agentic-ai/module-26-ai-agents/index.html': {
        'agent': 'compass', 'persona': 'Goal-Seeking',
        'epigraph_quote': "An agent is an LLM that has been given chores.",
        'looking_back_html': 'Part V finished the modalities. Part VI gives the model a goal and a way to act on it. This chapter introduces the agent loop: planning, tool use, memory, reflection, and the small architectural decisions that separate a chatbot from an autonomous system.',
        'prereqs_items': [
            'LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            'Prompt engineering and ReAct from <a href="../../part-3-working-with-llms/module-12-prompt-engineering/index.html">Chapter 12</a>',
            'Reasoning models from <a href="../../part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html">Chapter 8</a>',
        ],
    },
    'part-6-agentic-ai/module-27-tool-use-protocols/index.html': {
        'agent': 'pip', 'persona': 'Tool-Calling',
        'epigraph_quote': "Function calling turned the LLM into a programmer with hands.",
        'looking_back_html': 'Chapter 26 introduced the agent loop. This chapter zooms in on the most consequential link in that loop: how the model invokes external tools. Function calling, JSON schemas, MCP, and the patterns that keep tool calls reliable as agents grow.',
        'prereqs_items': [
            'Agent foundations from <a href="../module-26-ai-agents/index.html">Chapter 26</a>',
            'Function calling and structured outputs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            "Comfort with JSON schemas and small server-side glue code",
        ],
    },
    'part-6-agentic-ai/module-28-multi-agent-systems/index.html': {
        'agent': 'echo', 'persona': 'Co-Operative',
        'epigraph_quote': "One agent answers; two agents argue; three agents form a committee.",
        'looking_back_html': 'Chapter 27 made one agent productive. This chapter coordinates several at once: planner-executor pairs, debate, hierarchies, and the open question of when multi-agent designs actually beat one well-prompted model.',
        'prereqs_items': [
            'Single-agent loops from <a href="../module-26-ai-agents/index.html">Chapter 26</a>',
            'Tool use from <a href="../module-27-tool-use-protocols/index.html">Chapter 27</a>',
            "Distributed-systems intuition (state, retries, race conditions)",
        ],
    },
    'part-6-agentic-ai/module-29-specialized-agents/index.html': {
        'agent': 'compass', 'persona': 'Domain-Specialized',
        'epigraph_quote': "A specialized agent is a system prompt, a toolset, and a hundred edge cases.",
        'looking_back_html': 'Chapter 28 generalized the agent design. This chapter specializes: coding agents, research agents, support agents, and the small per-domain choices (memory, tools, evaluation) that make each one usable.',
        'prereqs_items': [
            'Single-agent and multi-agent designs from <a href="../module-26-ai-agents/index.html">Chapters 26</a> through <a href="../module-28-multi-agent-systems/index.html">28</a>',
            'Tool use from <a href="../module-27-tool-use-protocols/index.html">Chapter 27</a>',
            "Familiarity with at least one concrete agent product (Claude Code, Cursor, Devin)",
        ],
    },
    'part-6-agentic-ai/module-30-tools-of-the-trade/index.html': {
        'agent': 'pip', 'persona': 'Stack-Building',
        'epigraph_quote': "The agent framework you choose will outlast the agent you build with it.",
        'looking_back_html': 'Chapters 26 through 29 designed agents. This chapter surveys the frameworks that host them: LangGraph, OpenAI Agents SDK, Claude Code, Mastra, smolagents, and the open question of which abstraction layer is worth its complexity.',
        'prereqs_items': [
            'Agent foundations from <a href="../module-26-ai-agents/index.html">Chapter 26</a>',
            'LLM tooling stack from <a href="../../part-3-working-with-llms/module-14-tools-of-the-trade/index.html">Chapter 14</a>',
            "Python and shell comfort for hands-on framework comparisons",
        ],
    },
    # Part 7
    'part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/index.html': {
        'agent': 'vec', 'persona': 'Vector-Native',
        'epigraph_quote': "Search is half the answer to most LLM problems.",
        'looking_back_html': 'Part VI built agents. Part VII gives them memory and external knowledge. This chapter is the substrate: embeddings, vector databases, ANN indexes, hybrid search, and the small but consequential question of which model to use for the encoder.',
        'prereqs_items': [
            'Word embeddings from <a href="../../part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/index.html">Chapter 1</a>',
            'LLM API basics from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            "Familiarity with SQL or any structured database",
        ],
    },
    'part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html': {
        'agent': 'rag', 'persona': 'Bookishly-Wise',
        'epigraph_quote': "Retrieval Augmented Generation: read first, then answer.",
        'looking_back_html': 'Chapter 31 built the search substrate. This chapter assembles it into RAG: chunking, retrieval, reranking, grounding, citation, and the standard failure modes (hallucinated citations, retrieval drift, prompt poisoning).',
        'prereqs_items': [
            'Embeddings and vector DB basics from <a href="../module-31-embeddings-vector-db/index.html">Chapter 31</a>',
            'Prompt engineering from <a href="../../part-3-working-with-llms/module-12-prompt-engineering/index.html">Chapter 12</a>',
            'LLM API surface from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
        ],
    },
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/index.html': {
        'agent': 'rag', 'persona': 'Cross-Modal-Curious',
        'epigraph_quote': "When the corpus contains charts as well as paragraphs, your retriever must read pictures.",
        'looking_back_html': 'Chapter 32 was text-only RAG. This chapter crosses modalities: image+text retrieval, multimodal embeddings, document-aware retrieval, and the production patterns that let you ground an answer in a PDF, a chart, or a video frame.',
        'prereqs_items': [
            'Text RAG from <a href="../module-32-rag/index.html">Chapter 32</a>',
            'Vision-language models from <a href="../../part-5-multimodal-llms/module-22-vision-language-models/index.html">Chapter 22</a>',
            'Document understanding from <a href="../../part-5-multimodal-llms/module-21-document-understanding-ocr/index.html">Chapter 21</a>',
        ],
    },
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/index.html': {
        'agent': 'label', 'persona': 'Schema-Strict',
        'epigraph_quote': "Half of every LLM project is turning prose into a table.",
        'looking_back_html': 'Chapter 33 retrieved from messy data; this chapter <em>extracts</em>: NER, relation extraction, structured outputs, JSON-schema guardrails, and the small reliability tricks (validation, retry, dual-LLM verification) that make extraction production-grade.',
        'prereqs_items': [
            'LLM APIs and structured outputs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            'Prompt engineering from <a href="../../part-3-working-with-llms/module-12-prompt-engineering/index.html">Chapter 12</a>',
            "Comfort with JSON schemas and Pydantic or similar typed-validation libraries",
        ],
    },
    'part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/index.html': {
        'agent': 'rag', 'persona': 'Production-Tested',
        'epigraph_quote': "Naive RAG is a great demo and a bad product.",
        'looking_back_html': 'Chapter 32 covered RAG basics; this chapter levels up: graph-based RAG, agentic retrieval, late-interaction models like ColBERT, hybrid retrieval, knowledge-graph grounding, and the LightRAG/GraphRAG family of 2025-era systems.',
        'prereqs_items': [
            'RAG fundamentals from <a href="../module-32-rag/index.html">Chapter 32</a>',
            'Agent foundations from <a href="../../part-6-agentic-ai/module-26-ai-agents/index.html">Chapter 26</a>',
            'Embeddings and ANN basics from <a href="../module-31-embeddings-vector-db/index.html">Chapter 31</a>',
        ],
    },
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/index.html': {
        'agent': 'pip', 'persona': 'Retrieval-Stack-Building',
        'epigraph_quote': "Choose the retrieval stack you can maintain at 2 a.m., not the one that wins a benchmark.",
        'looking_back_html': 'Chapters 31 through 35 walked through retrieval theory. This chapter is the tooling: LlamaIndex, LangChain retrievers, Qdrant, Weaviate, Chroma, pgvector, Cohere Rerank, and the small operational decisions that hold a RAG pipeline together.',
        'prereqs_items': [
            'Vector-DB and embedding basics from <a href="../module-31-embeddings-vector-db/index.html">Chapter 31</a>',
            'RAG fundamentals from <a href="../module-32-rag/index.html">Chapter 32</a>',
            "Python and Docker comfort for hands-on tool comparisons",
        ],
    },
    # Part 8
    'part-8-conversational-ai-with-llms/module-37-conversational-ai/index.html': {
        'agent': 'compass', 'persona': 'Dialogue-Designing',
        'epigraph_quote': "A chat is a state machine pretending to be a conversation.",
        'looking_back_html': 'Part VII gave the model a knowledge base. Part VIII gives it a voice. This chapter covers conversational AI: turn structure, system prompts, memory, persona, and the dialogue-management patterns that turn an LLM into a chatbot people actually use.',
        'prereqs_items': [
            'LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            'Prompt engineering from <a href="../../part-3-working-with-llms/module-12-prompt-engineering/index.html">Chapter 12</a>',
            'Retrieval and memory from <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html">Chapter 32</a>',
        ],
    },
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/index.html': {
        'agent': 'echo', 'persona': 'Realtime-Wrangling',
        'epigraph_quote': "Latency is a feature, not a bug, when you can hear the silence.",
        'looking_back_html': 'Chapter 37 built text chat. This chapter adds the voice and the realtime modality: streaming ASR, TTS, speech-to-speech models, the Realtime API surface, and the latency budgets that make voice agents feel responsive.',
        'prereqs_items': [
            'Conversational AI fundamentals from <a href="../module-37-conversational-ai/index.html">Chapter 37</a>',
            'Audio fundamentals from <a href="../../part-5-multimodal-llms/module-20-audio-music-generation/index.html">Chapter 20</a>',
            "Comfort with streaming APIs and async Python",
        ],
    },
    'part-8-conversational-ai-with-llms/module-41-conv-ai-tools/index.html': {
        'agent': 'pip', 'persona': 'Conversation-Stack-Building',
        'epigraph_quote': "A chatbot is 5 percent LLM and 95 percent integration.",
        'looking_back_html': 'Chapters 37 and 40 designed conversational agents. This chapter surveys the conversational stack: Vapi, Retell, ElevenLabs, Pipecat, LiveKit, Voiceflow, Rasa, and the platform pieces that turn a working demo into a deployable product.',
        'prereqs_items': [
            'Conversational AI from <a href="../module-37-conversational-ai/index.html">Chapter 37</a>',
            'Voice and realtime from <a href="../module-40-voice-realtime-multimodal/index.html">Chapter 40</a>',
            "Python and JavaScript familiarity for the hands-on integrations",
        ],
    },
    # Part 9
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html': {
        'agent': 'eval', 'persona': 'Chronically-Skeptical',
        'epigraph_quote': "An LLM you cannot evaluate is an LLM you cannot ship.",
        'looking_back_html': 'Parts I through VIII built systems. Part IX measures them. This chapter is the foundation: what to evaluate, why automatic metrics so often mislead, and how to design an evaluation that catches the failure modes that matter.',
        'prereqs_items': [
            'Fine-tuning basics from <a href="../../part-4-training-adaptation/module-16-fine-tuning-fundamentals/index.html">Chapter 16</a>',
            'Prompt engineering from <a href="../../part-3-working-with-llms/module-12-prompt-engineering/index.html">Chapter 12</a>',
            "Basic statistics (confidence intervals, hypothesis testing)",
        ],
    },
    'part-9-llm-evaluation-observability/module-43-specialized-evaluation/index.html': {
        'agent': 'eval', 'persona': 'Trace-Sniffing',
        'epigraph_quote': "Specialized evaluation is what general-purpose benchmarks miss.",
        'looking_back_html': 'Chapter 42 covered general evaluation. This chapter goes deeper: RAG eval (Ragas, BEIR), agentic eval (AgentBench, SWE-Bench, GAIA, tau-bench), simulation-based eval, code-gen eval, and multimodal eval, all the families where scalar text benchmarks fall short.',
        'prereqs_items': [
            'Evaluation foundations from <a href="../module-42-evaluation-foundations/index.html">Chapter 42</a>',
            'RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html">Chapter 32</a>',
            'Agent foundations from <a href="../../part-6-agentic-ai/module-26-ai-agents/index.html">Chapter 26</a>',
        ],
    },
    'part-9-llm-evaluation-observability/module-44-online-eval-observability/index.html': {
        'agent': 'deploy', 'persona': 'Perpetually-Shipping',
        'epigraph_quote': "Offline evals tell you it works; online observability tells you it is still working.",
        'looking_back_html': 'Chapters 42 and 43 evaluated models in the lab. This chapter watches them in production: traces, dashboards, drift detection, online A/B tests, and the observability stack (LangSmith, Phoenix, Helicone, Langfuse) that keeps an LLM product healthy after launch.',
        'prereqs_items': [
            'Offline evaluation from <a href="../module-42-evaluation-foundations/index.html">Chapter 42</a>',
            'Specialized evaluation from <a href="../module-43-specialized-evaluation/index.html">Chapter 43</a>',
            "Some prior exposure to production monitoring (Datadog, Prometheus) helps",
        ],
    },
    'part-9-llm-evaluation-observability/module-45-tools-of-the-trade/index.html': {
        'agent': 'eval', 'persona': 'Spec-First',
        'epigraph_quote': "The eval framework you live with is the one whose dashboard your manager opens.",
        'looking_back_html': 'Chapters 42 through 44 framed evaluation; this chapter is the toolbox: OpenAI Evals, Inspect, Ragas, DeepEval, Promptfoo, LangSmith, Phoenix, and the small per-team choices about where evaluation should live in your CI.',
        'prereqs_items': [
            'Evaluation foundations from <a href="../module-42-evaluation-foundations/index.html">Chapter 42</a>',
            'Production observability from <a href="../module-44-online-eval-observability/index.html">Chapter 44</a>',
            "Comfort with CI/CD basics (GitHub Actions or similar)",
        ],
    },
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/index.html': {
        'agent': 'eval', 'persona': 'Judge-Wary',
        'epigraph_quote': "If a model can grade itself, you must grade the grader.",
        'looking_back_html': 'Chapters 42 through 45 built the eval stack. This chapter turns the LLM into the judge: pairwise preferences, rubric scoring, calibration, position bias, and the audit techniques that keep LLM-as-judge from quietly drifting.',
        'prereqs_items': [
            'Evaluation foundations from <a href="../module-42-evaluation-foundations/index.html">Chapter 42</a>',
            'Specialized evaluation from <a href="../module-43-specialized-evaluation/index.html">Chapter 43</a>',
            'Prompt engineering from <a href="../../part-3-working-with-llms/module-12-prompt-engineering/index.html">Chapter 12</a>',
        ],
    },
    # Part 10
    'part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/index.html': {
        'agent': 'guard', 'persona': 'Red-Team-Ready',
        'epigraph_quote': "If you have not tried to break your model, an attacker already has.",
        'looking_back_html': 'Part IX measured your model in good faith. Part X assumes someone is in bad faith. This chapter walks the adversarial landscape: prompt injection, jailbreaks, training-time poisoning, model extraction, and the red-teaming protocols every production team should run.',
        'prereqs_items': [
            'Evaluation foundations from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html">Chapter 42</a>',
            'LLM API surface from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            "Basic security mindset (threat modeling, attacker perspective)",
        ],
    },
    'part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/index.html': {
        'agent': 'guard', 'persona': 'Defense-In-Depth',
        'epigraph_quote': "A guardrail is the apology you wrote before the model misbehaved.",
        'looking_back_html': 'Chapter 47 showed how attackers break models. This chapter is the defensive layer: input filters, output filters, classifier-based guardrails, content moderation, and the production rails (NeMo Guardrails, Llama Guard, Granite Guardian, OpenAI Moderation) that catch what the prompt could not.',
        'prereqs_items': [
            'Adversarial attacks from <a href="../module-47-adversarial-security-red-team/index.html">Chapter 47</a>',
            'Online observability from <a href="../../part-9-llm-evaluation-observability/module-44-online-eval-observability/index.html">Chapter 44</a>',
            "Familiarity with classifier deployment basics",
        ],
    },
    'part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/index.html': {
        'agent': 'guard', 'persona': 'Autonomy-Auditing',
        'epigraph_quote': "The more autonomous the agent, the more important the kill switch.",
        'looking_back_html': 'Chapter 48 set up guardrails for chat. This chapter raises the stakes: agents that take actions in the world. We cover permission models, sandboxing, approval flows, capability minimization, and the runtime monitors that catch a misbehaving agent before it touches production.',
        'prereqs_items': [
            'Agent foundations from <a href="../../part-6-agentic-ai/module-26-ai-agents/index.html">Chapter 26</a>',
            'Guardrails from <a href="../module-48-guardrails-runtime-safety/index.html">Chapter 48</a>',
            'Tool use from <a href="../../part-6-agentic-ai/module-27-tool-use-protocols/index.html">Chapter 27</a>',
        ],
    },
    'part-10-llm-security-runtime-safety/module-50-privacy-data-protection/index.html': {
        'agent': 'sentinel', 'persona': 'Privacy-Preserving',
        'epigraph_quote': "Your model can leak data it never wrote down, by paraphrasing what it learned.",
        'looking_back_html': 'Chapters 47 through 49 protected the system. This chapter protects the user: PII handling, differential privacy, memorization risks, GDPR/CCPA obligations, on-device inference, and the data-handling discipline every LLM-enabled product owes its customers.',
        'prereqs_items': [
            'Adversarial security from <a href="../module-47-adversarial-security-red-team/index.html">Chapter 47</a>',
            'Pretraining and memorization from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
            "Basic familiarity with privacy regulation (GDPR/CCPA at a high level)",
        ],
    },
    'part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/index.html': {
        'agent': 'guard', 'persona': 'Defense-Stack-Building',
        'epigraph_quote': "The security stack is the one part of LLMs where boring is a feature.",
        'looking_back_html': 'Chapters 47 through 50 covered the threat model. This chapter is the operational stack: NeMo Guardrails, Llama Guard, Granite Guardian, OpenAI Moderation, Lakera, Garak, and the day-to-day tooling that keeps an LLM product defensible.',
        'prereqs_items': [
            'At least one of <a href="../module-47-adversarial-security-red-team/index.html">Chapter 47</a> through <a href="../module-50-privacy-data-protection/index.html">50</a>',
            'LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            "Familiarity with running classifiers and small models in production",
        ],
    },
    # Part 11
    'part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html': {
        'agent': 'census', 'persona': 'Fairness-Forward',
        'epigraph_quote': "A model that is unbiased on the benchmark is not the same as a model that is fair to your user.",
        'looking_back_html': 'Part X kept the system safe. Part XI keeps it trustworthy. This chapter begins with bias, fairness, and hallucinations: the failure modes that erode user trust the fastest. Measurement, mitigation, and the tradeoffs between accuracy, calibration, and group-level outcomes.',
        'prereqs_items': [
            'Evaluation foundations from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html">Chapter 42</a>',
            'Specialized evaluation from <a href="../../part-9-llm-evaluation-observability/module-43-specialized-evaluation/index.html">Chapter 43</a>',
            "Basic statistics (distributions, group means, hypothesis tests)",
        ],
    },
    'part-11-llm-ethics-trust-governance/module-53-regulation-compliance/index.html': {
        'agent': 'compass', 'persona': 'Regulation-Aware',
        'epigraph_quote': "Regulation is the price of being taken seriously.",
        'looking_back_html': 'Chapter 52 measured bias and harm. This chapter maps the regulatory response: the EU AI Act, the US executive orders and state-level laws, the UK and APAC frameworks, and the compliance work product (risk registers, transparency reports, conformity assessments) that LLM teams now ship alongside the model.',
        'prereqs_items': [
            'Bias and fairness from <a href="../module-52-bias-fairness/index.html">Chapter 52</a>',
            'Evaluation foundations from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html">Chapter 42</a>',
            "Familiarity with at least one regulatory environment (privacy, finance, healthcare)",
        ],
    },
    'part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/index.html': {
        'agent': 'sentinel', 'persona': 'Provenance-Tracking',
        'epigraph_quote': "If we cannot prove what a model wrote, we cannot prove what a human did not.",
        'looking_back_html': 'Chapter 53 covered the rules; this chapter starts on the technical primitives that satisfy them. Watermarking, provenance metadata, C2PA, SynthID, DeepMind\'s text watermarking, and the broader problem of tracking AI-generated content as it moves through the internet.',
        'prereqs_items': [
            'Regulation and compliance from <a href="../module-53-regulation-compliance/index.html">Chapter 53</a>',
            'Decoding and sampling from <a href="../../part-1-llm-building-blocks/module-04-decoding-text-generation/index.html">Chapter 4</a>',
            'Inference optimization from <a href="../../part-2-understanding-llms/module-09-inference-optimization/index.html">Chapter 9</a>',
        ],
    },
    'part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/index.html': {
        'agent': 'compass', 'persona': 'Documentation-Disciplined',
        'epigraph_quote': "The model card is the receipt your auditor asks for.",
        'looking_back_html': 'Chapter 54 marked AI-generated outputs; this chapter documents the systems that produced them. Model cards, datasheets for datasets, system cards, audit trails, and the explainability disclosures that high-stakes decisions now require.',
        'prereqs_items': [
            'Regulation and compliance from <a href="../module-53-regulation-compliance/index.html">Chapter 53</a>',
            'Watermarking and provenance from <a href="../module-54-watermarking-provenance/index.html">Chapter 54</a>',
            'Pretraining and data curation from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
        ],
        'next_paragraph': 'This chapter begins with <a href="section-54.6.html">Section 54.6: Model Cards: Anatomy, Examples, Use in Procurement</a>. Each section walks one transparency artifact from anatomy to procurement workflow, so we recommend reading them in order.',
    },
    'part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/index.html': {
        'agent': 'compass', 'persona': 'Carbon-Aware',
        'epigraph_quote': "Every gradient step has a carbon cost; every inference too.",
        'looking_back_html': 'Chapter 54 covered transparency; this chapter covers a different kind of disclosure: environmental impact. We work through training-time vs inference-time energy, regional grid carbon intensity, water use, and the small efficiency choices that compound across millions of inferences.',
        'prereqs_items': [
            'Compute planning from <a href="../../part-12-llm-systems-at-scale/module-57-compute-planning/index.html">Chapter 57</a>',
            'Inference optimization from <a href="../../part-2-understanding-llms/module-09-inference-optimization/index.html">Chapter 9</a>',
            'Pretraining and scaling laws from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
        ],
    },
    'part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/index.html': {
        'agent': 'sage', 'persona': 'Governance-Tooling',
        'epigraph_quote': "Responsibility is a habit; tools are the way teams form habits.",
        'looking_back_html': 'Chapters 52 through 55 built the responsible-AI agenda. This chapter is the operational toolkit: Fairlearn, Aequitas, AI Fairness 360, model-card generators, datasheet templates, the C2PA SDK, the carbon-tracking libraries, and the audit frameworks that teams use to convert principles into pipelines.',
        'prereqs_items': [
            'Bias and fairness from <a href="../module-52-bias-fairness/index.html">Chapter 52</a>',
            'Regulation from <a href="../module-53-regulation-compliance/index.html">Chapter 53</a>',
            'Transparency disclosures from <a href="../module-54b-transparency-and-disclosure/index.html">Chapter 54 (transparency)</a>',
        ],
    },
    # Part 12
    'part-12-llm-systems-at-scale/module-57-compute-planning/index.html': {
        'agent': 'scale', 'persona': 'Capacity-Planning',
        'epigraph_quote': "The cluster is the budget; everything else is interpretation.",
        'looking_back_html': 'Part XI covered governance; Part XII covers the physical system that you have to govern. This chapter starts at the top: compute planning. GPU/TPU choice, cluster sizing, interconnect, power and cooling, the build-vs-rent decision, and the FLOPs accounting that turns scaling laws into a procurement spec.',
        'prereqs_items': [
            'Scaling laws from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
            'Inference optimization from <a href="../../part-2-understanding-llms/module-09-inference-optimization/index.html">Chapter 9</a>',
            "Basic distributed-systems literacy (nodes, networks, throughput)",
        ],
    },
    'part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/index.html': {
        'agent': 'frontier', 'persona': 'Silicon-Curious',
        'epigraph_quote': "Tomorrow's model fits in the silicon you have not bought yet.",
        'looking_back_html': 'Chapter 57 planned the cluster. This chapter inventories the cutting edge: H100, H200, Blackwell, MI300, TPU v5e and v5p, Trainium, Cerebras, Groq, and the emerging analog and photonic stacks. Performance numbers, software stack maturity, and where each chip family is winning.',
        'prereqs_items': [
            'Compute planning from <a href="../module-57-compute-planning/index.html">Chapter 57</a>',
            'Inference optimization from <a href="../../part-2-understanding-llms/module-09-inference-optimization/index.html">Chapter 9</a>',
            "Familiarity with GPU memory hierarchy (HBM, on-chip SRAM) helps",
        ],
    },
    'part-12-llm-systems-at-scale/module-59-distributed-training-systems/index.html': {
        'agent': 'scale', 'persona': 'Distributed-Disciplined',
        'epigraph_quote': "Distributed training is what happens when one GPU is not enough and one strategy is not either.",
        'looking_back_html': 'Chapter 58 chose the hardware; this chapter coordinates many copies of it. DDP, FSDP, ZeRO, tensor parallelism, pipeline parallelism, sequence parallelism, and the small but consequential question of which sharding strategy fits your model and your interconnect.',
        'prereqs_items': [
            'Compute planning from <a href="../module-57-compute-planning/index.html">Chapter 57</a>',
            'Pretraining and optimizers from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
            'PyTorch training internals from <a href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html">Chapter 0</a>',
        ],
    },
    'part-12-llm-systems-at-scale/module-60-edge-on-device-llms/index.html': {
        'agent': 'quant', 'persona': 'Edge-Squeezing',
        'epigraph_quote': "The smartest model is the one you can run on the device your user already owns.",
        'looking_back_html': 'Chapter 59 trained at the largest scale; this chapter deploys at the smallest. Quantization, distillation, MLX, GGUF, Apple Neural Engine, mobile NPUs, and the engineering tradeoffs that let a useful LLM fit in a phone or a laptop.',
        'prereqs_items': [
            'Inference optimization from <a href="../../part-2-understanding-llms/module-09-inference-optimization/index.html">Chapter 9</a>',
            'PEFT and quantization from <a href="../../part-4-training-adaptation/module-17-peft/index.html">Chapter 17</a>',
            'Frontier hardware from <a href="../module-58-frontier-systems-hardware/index.html">Chapter 58</a>',
        ],
    },
    'part-12-llm-systems-at-scale/module-61-scale-tools/index.html': {
        'agent': 'scale', 'persona': 'Stack-Building',
        'epigraph_quote': "Choose tools whose bill of materials you can explain to your CFO.",
        'looking_back_html': 'Chapters 57 through 60 built the systems story. This chapter inventories the tools that operate them: NeMo, Megatron, DeepSpeed, FSDP, JAX, vLLM, TensorRT-LLM, llama.cpp, and the orchestration glue (Slurm, Kubernetes) that keeps a large cluster productive.',
        'prereqs_items': [
            'Distributed training from <a href="../module-59-distributed-training-systems/index.html">Chapter 59</a>',
            'Inference optimization from <a href="../../part-2-understanding-llms/module-09-inference-optimization/index.html">Chapter 9</a>',
            "Comfort with at least one container or workload-manager system",
        ],
    },
    # Part 13
    'part-13-llmops-lifecycle/module-62-production-engineering-core/index.html': {
        'agent': 'deploy', 'persona': 'Perpetually-Shipping',
        'epigraph_quote': "Production is where the bug reports begin.",
        'looking_back_html': 'Part XII supplied the iron and the framework. Part XIII covers the lifecycle of an LLM service. This chapter starts with the core: deployment patterns, API design, prompt versioning, model registry, and the small engineering habits that distinguish a long-lived service from a hack-week demo.',
        'prereqs_items': [
            'LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            'Evaluation foundations from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html">Chapter 42</a>',
            "Web-service engineering basics (REST, async, caching)",
        ],
    },
    'part-13-llmops-lifecycle/module-63-ai-gateways-routing/index.html': {
        'agent': 'deploy', 'persona': 'Gateway-Guarding',
        'epigraph_quote': "Behind every good LLM product is a gateway that vendors do not see.",
        'looking_back_html': 'Chapter 62 deployed a single model. This chapter handles the rest: AI gateways (Portkey, Kong AI Gateway, LiteLLM Router), model routing, fallback chains, vendor abstraction, cost-aware routing, and the day when one provider has an outage and your product cannot afford to.',
        'prereqs_items': [
            'Production engineering core from <a href="../module-62-production-engineering-core/index.html">Chapter 62</a>',
            'LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            "Familiarity with at least one API gateway or service-mesh tool",
        ],
    },
    'part-13-llmops-lifecycle/module-64-workflow-orchestration/index.html': {
        'agent': 'deploy', 'persona': 'Workflow-Watching',
        'epigraph_quote': "Orchestration is the difference between an LLM script and an LLM platform.",
        'looking_back_html': 'Chapter 63 routed requests; this chapter routes <em>workflows</em>. Temporal, Inngest, Airflow with LLM operators, Prefect, durable execution, retries with backoff, and the workflow patterns that turn long-running LLM jobs into reliable async pipelines.',
        'prereqs_items': [
            'Production engineering from <a href="../module-62-production-engineering-core/index.html">Chapter 62</a>',
            'Agent foundations from <a href="../../part-6-agentic-ai/module-26-ai-agents/index.html">Chapter 26</a>',
            "Familiarity with at least one workflow engine (Airflow, Temporal, Step Functions)",
        ],
    },
    'part-13-llmops-lifecycle/module-65-containers-kubernetes/index.html': {
        'agent': 'deploy', 'persona': 'Container-Disciplined',
        'epigraph_quote': "Kubernetes does not understand GPUs by default; you teach it.",
        'looking_back_html': 'Chapter 64 orchestrated workflows; this chapter packages the workers. Containers, Kubernetes, KServe, KubeAI, GPU operators, node autoscalers, and the production-grade serving stack that GPU-aware Kubernetes has become.',
        'prereqs_items': [
            'Production engineering from <a href="../module-62-production-engineering-core/index.html">Chapter 62</a>',
            'Scale tools (vLLM, TensorRT-LLM) from <a href="../../part-12-llm-systems-at-scale/module-61-scale-tools/index.html">Chapter 61</a>',
            "Working knowledge of Docker and Kubernetes",
        ],
    },
    'part-13-llmops-lifecycle/module-66-reliability-slos-registry/index.html': {
        'agent': 'deploy', 'persona': 'SLO-Defending',
        'epigraph_quote': "A 99.9 percent SLO is a contract; a 99.9 percent vibe is a footnote.",
        'looking_back_html': 'Chapters 62 through 65 deployed and orchestrated LLM systems. This chapter is the operational discipline: SLOs, error budgets, incident response, postmortems, model registry, prompt-as-code, blue/green deployments, and the small habits that distinguish a reliable platform from one that hopes.',
        'prereqs_items': [
            'Production engineering from <a href="../module-62-production-engineering-core/index.html">Chapter 62</a>',
            'AI gateways from <a href="../module-63-ai-gateways-routing/index.html">Chapter 63</a>',
            'Containers and Kubernetes from <a href="../module-65-containers-kubernetes/index.html">Chapter 65</a>',
        ],
    },
    # Part 14
    'part-14-designing-llm-agent-products/module-67-ideation/index.html': {
        'agent': 'sage', 'persona': 'Idea-Vetting',
        'epigraph_quote': "Most LLM features deserve to die in the brainstorm.",
        'looking_back_html': 'Part XIII operated systems. Part XIV designs products on top of them. This chapter starts at the very beginning: ideation. How to spot an LLM-shaped problem, validate it cheaply, write a spec a team can ship against, and avoid the magical-AI demo that does not survive contact with real users.',
        'prereqs_items': [
            'LLM APIs from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            'Prompt engineering from <a href="../../part-3-working-with-llms/module-12-prompt-engineering/index.html">Chapter 12</a>',
            "Familiarity with at least one product-development methodology (lean, Shape Up)",
        ],
    },
    'part-14-designing-llm-agent-products/module-68-vibe-coding/index.html': {
        'agent': 'pip', 'persona': 'Vibe-Coding',
        'epigraph_quote': "The prototype that ships in a weekend wins the budget meeting on Monday.",
        'looking_back_html': 'Chapter 67 found the right idea; this chapter ships its prototype. Vibe coding with Claude Code, Cursor, Replit Agent, v0, Bolt, and the small disciplines (prompts as commits, tests as guardrails) that make AI-assisted development productive instead of brittle.',
        'prereqs_items': [
            'Ideation from <a href="../module-67-ideation/index.html">Chapter 67</a>',
            'Agent foundations from <a href="../../part-6-agentic-ai/module-26-ai-agents/index.html">Chapter 26</a>',
            "Strong software-engineering hygiene (version control, tests, code review)",
        ],
    },
    'part-14-designing-llm-agent-products/module-69-llm-economics/index.html': {
        'agent': 'compass', 'persona': 'Economically-Disciplined',
        'epigraph_quote': "Unit economics is the part of the LLM product that decides whether it can be a product.",
        'looking_back_html': 'Chapter 68 prototyped the product; this chapter measures whether it can scale. Cost per request, cost per user, gross margin, fixed vs variable inference cost, monetization patterns, and the financial model that turns an LLM demo into a defensible business.',
        'prereqs_items': [
            'Prototyping and shipping from <a href="../module-68-vibe-coding/index.html">Chapter 68</a>',
            'LLM API and rate-limit economics from <a href="../../part-3-working-with-llms/module-11-llm-apis/index.html">Chapter 11</a>',
            "Basic financial modeling (CAC, LTV, gross margin)",
        ],
    },
    'part-14-designing-llm-agent-products/module-70-shipping-products/index.html': {
        'agent': 'deploy', 'persona': 'Product-Shipping',
        'epigraph_quote': "Shipping is the only part of the product no demo can fake.",
        'looking_back_html': 'Chapters 67 through 69 designed the product. This chapter ships and scales it: launch playbooks, growth, pricing, support, abuse handling, account management, and the post-launch operations that turn an LLM product from a hit demo into a durable business.',
        'prereqs_items': [
            'Ideation from <a href="../module-67-ideation/index.html">Chapter 67</a>',
            'Economics from <a href="../module-69-llm-economics/index.html">Chapter 69</a>',
            'Production engineering from <a href="../../part-13-llmops-lifecycle/module-62-production-engineering-core/index.html">Chapter 62</a>',
        ],
    },
    'part-14-designing-llm-agent-products/module-71-tools-of-the-trade/index.html': {
        'agent': 'pip', 'persona': 'Product-Building',
        'epigraph_quote': "The product stack is the framework, the analytics, the support tool, and the LLM you almost forgot about.",
        'looking_back_html': 'Chapters 67 through 70 built and shipped products. This chapter is the toolkit: Replit Agent, Cursor, Claude Code, v0, Bolt, Vercel, PostHog, Stripe, and the smaller analytics and ops tools every LLM product team converges on.',
        'prereqs_items': [
            'Ideation and prototyping from <a href="../module-67-ideation/index.html">Chapters 67</a> and <a href="../module-68-vibe-coding/index.html">68</a>',
            'Shipping from <a href="../module-70-shipping-products/index.html">Chapter 70</a>',
            "Familiarity with one product stack (Vercel, AWS, GCP, Azure)",
        ],
    },
    # Part 15
    'part-15-applications-of-llms-across-industries/module-72-legal-llms/index.html': {
        'agent': 'sage', 'persona': 'Legally-Cautious',
        'epigraph_quote': "Legal LLMs answer questions that lawyers wrote three thousand years ago.",
        'looking_back_html': 'Part XIV built product fundamentals. Part XV applies them to industries. This chapter starts in legal: contract analysis, e-discovery, legal research, drafting assistance, and the unique evaluation and compliance challenges of an LLM whose answers may end up in court.',
        'prereqs_items': [
            'RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html">Chapter 32</a>',
            'Structured extraction from <a href="../../part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/index.html">Chapter 34</a>',
            'Specialized evaluation from <a href="../../part-9-llm-evaluation-observability/module-43-specialized-evaluation/index.html">Chapter 43</a>',
        ],
    },
    'part-15-applications-of-llms-across-industries/module-73-finance-llms/index.html': {
        'agent': 'sage', 'persona': 'Risk-Aware',
        'epigraph_quote': "In finance, every LLM answer is also a risk number.",
        'looking_back_html': 'Chapter 72 covered legal; this chapter covers finance. Research, trading, risk management, KYC, fraud, compliance, structured-data interrogation, and the high-stakes evaluation and governance discipline that finance demands.',
        'prereqs_items': [
            'RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html">Chapter 32</a>',
            'Evaluation foundations from <a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html">Chapter 42</a>',
            'Bias and fairness from <a href="../../part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html">Chapter 52</a>',
        ],
    },
    'part-15-applications-of-llms-across-industries/module-74-healthcare-llms/index.html': {
        'agent': 'sage', 'persona': 'Clinically-Cautious',
        'epigraph_quote': "Healthcare LLMs are graded on lives, not on tokens.",
        'looking_back_html': 'Chapters 72 and 73 covered legal and finance. This chapter is healthcare: clinical decision support, biomedical literature, EHR drafting, medical imaging assistance, drug discovery, and the regulatory, privacy, and safety requirements that domain demands.',
        'prereqs_items': [
            'RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html">Chapter 32</a>',
            'Privacy and data protection from <a href="../../part-10-llm-security-runtime-safety/module-50-privacy-data-protection/index.html">Chapter 50</a>',
            'Regulation and compliance from <a href="../../part-11-llm-ethics-trust-governance/module-53-regulation-compliance/index.html">Chapter 53</a>',
        ],
    },
    'part-15-applications-of-llms-across-industries/module-75-education-llms/index.html': {
        'agent': 'sage', 'persona': 'Education-Minded',
        'epigraph_quote': "The best tutor knows where the student is, not where the textbook is.",
        'looking_back_html': 'Chapter 74 covered healthcare. This chapter is education: tutoring, content generation, assessment, accessibility, and the unique evaluation problem of teaching versus telling.',
        'prereqs_items': [
            'Conversational AI from <a href="../../part-8-conversational-ai-with-llms/module-37-conversational-ai/index.html">Chapter 37</a>',
            'RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html">Chapter 32</a>',
            'Bias and fairness from <a href="../../part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html">Chapter 52</a>',
        ],
    },
    'part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/index.html': {
        'agent': 'guard', 'persona': 'Threat-Hunting',
        'epigraph_quote': "Cybersecurity LLMs work because the haystack is finally machine-readable.",
        'looking_back_html': 'Chapter 75 covered education; this chapter covers cybersecurity. Threat intelligence, log analysis, automated remediation, malware reverse engineering, and the dual-use risks of an LLM that can both defend and attack.',
        'prereqs_items': [
            'Adversarial security from <a href="../../part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/index.html">Chapter 47</a>',
            'Agent foundations from <a href="../../part-6-agentic-ai/module-26-ai-agents/index.html">Chapter 26</a>',
            'RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html">Chapter 32</a>',
        ],
    },
    'part-15-applications-of-llms-across-industries/module-77-government-llms/index.html': {
        'agent': 'compass', 'persona': 'Public-Interest',
        'epigraph_quote': "Government LLMs serve the citizens who pay for them, not the vendor who built them.",
        'looking_back_html': 'Chapter 76 covered cybersecurity. This chapter covers government: public-sector deployments, defense, civic services, accessibility, FOIA and records management, and the procurement, transparency, and oversight requirements that public-sector AI now carries.',
        'prereqs_items': [
            'Regulation and compliance from <a href="../../part-11-llm-ethics-trust-governance/module-53-regulation-compliance/index.html">Chapter 53</a>',
            'Privacy and data protection from <a href="../../part-10-llm-security-runtime-safety/module-50-privacy-data-protection/index.html">Chapter 50</a>',
            'Transparency disclosures from <a href="../../part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/index.html">Chapter 54 (transparency)</a>',
        ],
    },
    'part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/index.html': {
        'agent': 'compass', 'persona': 'Industry-Translating',
        'epigraph_quote': "Industrial LLMs are graded on tolerance, not on tokens per second.",
        'looking_back_html': 'Chapter 77 covered government; this chapter covers the rest of the industrial economy: manufacturing, creative industries, search and recommendation, plus the LLM-augmented stacks emerging across logistics and customer support.',
        'prereqs_items': [
            'RAG fundamentals from <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html">Chapter 32</a>',
            'Agent foundations from <a href="../../part-6-agentic-ai/module-26-ai-agents/index.html">Chapter 26</a>',
            'Production engineering from <a href="../../part-13-llmops-lifecycle/module-62-production-engineering-core/index.html">Chapter 62</a>',
        ],
    },
    'part-15-applications-of-llms-across-industries/module-79-tools-of-the-trade/index.html': {
        'agent': 'pip', 'persona': 'Vertical-Specializing',
        'epigraph_quote': "Vertical AI is twenty percent model and eighty percent integration into someone else's workflow.",
        'looking_back_html': 'Chapters 72 through 78 walked one industry at a time. This chapter is the vertical tooling: domain-specific LLMs (BloombergGPT, Med-PaLM, Sec-PaLM), vertical RAG stacks, sector-specific evals, and the integration patterns that show up in any vertical AI product.',
        'prereqs_items': [
            'At least one of <a href="../module-72-legal-llms/index.html">Chapters 72</a> through <a href="../module-78-manufacturing-llms/index.html">78</a>',
            'RAG and embedding tooling from <a href="../../part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/index.html">Chapter 36</a>',
            'Evaluation tooling from <a href="../../part-9-llm-evaluation-observability/module-45-tools-of-the-trade/index.html">Chapter 45</a>',
        ],
    },
    # Part 16
    'part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/index.html': {
        'agent': 'frontier', 'persona': 'Architecturally-Curious',
        'epigraph_quote': "Today's frontier architecture is tomorrow's footnote in Chapter 3.",
        'looking_back_html': 'Part XV applied LLMs to industries. Part XVI looks at what comes next. This chapter surveys the frontier architectures: mixture-of-experts, Mamba and state-space models, hybrid attention, native multimodal, very-long-context architectures, and the speculative ideas that might define the next generation.',
        'prereqs_items': [
            'Transformer architecture from <a href="../../part-1-llm-building-blocks/module-03-transformer-architecture/index.html">Chapter 3</a>',
            'Pretraining and scaling laws from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
            'Modern LLM landscape from <a href="../../part-2-understanding-llms/module-07-modern-llm-landscape/index.html">Chapter 7</a>',
        ],
    },
    'part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/index.html': {
        'agent': 'frontier', 'persona': 'Theoretically-Inclined',
        'epigraph_quote': "We do not understand transformers; we just deploy them really well.",
        'looking_back_html': 'Chapter 80 surveyed new architectures. This chapter looks deeper: what theory we have for why transformers learn, why they generalize, why scaling laws hold, and where mechanistic interpretability, in-context learning, and emergence sit in our scientific understanding.',
        'prereqs_items': [
            'Interpretability from <a href="../../part-2-understanding-llms/module-10-interpretability/index.html">Chapter 10</a>',
            'Pretraining and scaling laws from <a href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html">Chapter 6</a>',
            'Reasoning models from <a href="../../part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html">Chapter 8</a>',
        ],
    },
    'part-16-llm-agentic-ai-research-frontiers/module-82-agi-trajectories/index.html': {
        'agent': 'frontier', 'persona': 'AGI-Forecasting',
        'epigraph_quote': "AGI is whatever capability is two years away.",
        'looking_back_html': 'Chapter 81 covered the theory we have. This chapter covers the theory we wish we had: forecasting capabilities, timelines, scaling-vs-data-vs-compute scenarios, the safety landscape ahead, and the open questions that decide whether the next decade is exciting or terrifying.',
        'prereqs_items': [
            'Frontier theory from <a href="../module-81-frontier-theory/index.html">Chapter 81</a>',
            'Agent foundations from <a href="../../part-6-agentic-ai/module-26-ai-agents/index.html">Chapter 26</a>',
            'Reasoning models from <a href="../../part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html">Chapter 8</a>',
        ],
    },
    'part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/index.html': {
        'agent': 'frontier', 'persona': 'Pre-Print-Reading',
        'epigraph_quote': "The frontier toolkit is mostly arxiv tabs and a habit of running other people’s code.",
        'looking_back_html': 'Chapters 80 through 82 surveyed the frontier. This chapter is the toolkit for keeping up: arxiv-sanity, alphaXiv, Hugging Face Daily Papers, Papers with Code, reading lists, replication tools, and the small habits that distinguish someone who follows the field from someone who chases it.',
        'prereqs_items': [
            'Modern LLM landscape from <a href="../../part-2-understanding-llms/module-07-modern-llm-landscape/index.html">Chapter 7</a>',
            'Evaluation tooling from <a href="../../part-9-llm-evaluation-observability/module-45-tools-of-the-trade/index.html">Chapter 45</a>',
            "An arxiv account and the patience to read pre-prints",
        ],
    },
}


# ------------------------------------------------------------
# Authoring helpers
# ------------------------------------------------------------

def build_epigraph(agent: str, persona: str, quote: str) -> str:
    color = AGENT_COLORS[agent]
    display = AGENT_NAMES[agent]
    img_src = f'../../front-matter/images/agents/{agent}.png'
    return (
        '<blockquote class="epigraph">\n'
        f'<p>"{quote}"</p>\n'
        f'<span class="agent-avatar-inline" style="background-color: {color};">'
        f'<img alt="{display}" height="28" src="{img_src}" width="28"/></span>'
        f'<cite>{display}, <span class="agent-desc">{persona} AI Agent</span></cite>\n'
        '</blockquote>'
    )


def build_looking_back(inner_html: str) -> str:
    return (
        '<div class="callout looking-back">\n'
        '<div class="callout-title">Looking Back</div>\n'
        f'<p>{inner_html}</p>\n'
        '</div>'
    )


def build_prereqs(items: list[str]) -> str:
    li_html = '\n'.join(f'<li>{x}</li>' for x in items)
    return (
        '<div class="prereqs">\n'
        '<h3 id="prerequisites">Prerequisites</h3>\n'
        '<ul>\n'
        f'{li_html}\n'
        '</ul>\n'
        '</div>'
    )


def build_whats_next(inner_paragraph: str) -> str:
    return (
        '<div class="whats-next">\n'
        "<h3>What's Next?</h3>\n"
        f'<p>{inner_paragraph}</p>\n'
        '</div>'
    )


# ------------------------------------------------------------
# Detect existing structures
# ------------------------------------------------------------

EPIGRAPH_RE = re.compile(r'<blockquote\s+class="epigraph"', re.I)
LOOKING_BACK_RE = re.compile(r'class="callout\s+looking-back"', re.I)
PREREQS_DIV_RE = re.compile(r'class="prereqs"', re.I)
PREREQS_HEADING_RE = re.compile(r'>\s*Prerequisites\s*<', re.I)
WHATS_NEXT_RE = re.compile(r'class="whats-next"', re.I)
NOTE_PREREQS_CALLOUT_RE = re.compile(
    r'<div\s+class="callout\s+note">\s*'
    r'<div\s+class="callout-title">\s*(?:Note:\s*)?Prerequisites\s*</div>\s*'
    r'(<ul>[\s\S]*?</ul>)\s*'
    r'</div>',
    re.I,
)


def needs_epigraph(html: str) -> bool:
    return not EPIGRAPH_RE.search(html)


def needs_looking_back(html: str) -> bool:
    return not LOOKING_BACK_RE.search(html)


def needs_prereqs(html: str) -> bool:
    return not (PREREQS_DIV_RE.search(html) or PREREQS_HEADING_RE.search(html))


def needs_whats_next(html: str) -> bool:
    return not WHATS_NEXT_RE.search(html)


# ------------------------------------------------------------
# Insertion logic
# ------------------------------------------------------------

def insert_epigraph(html: str, block: str) -> str:
    """Insert epigraph after the pagefind-meta-injected spans (or after the
    chapter-opener figure if those spans are absent)."""
    # Try pagefind-meta-injected first
    meta_pat = re.compile(
        r'(<span class="pagefind-meta-injected"[^>]*data-pagefind-meta="chapter:[^"]*"[^>]*>\s*</span>)',
        re.I,
    )
    m = meta_pat.search(html)
    if m:
        insert_at = m.end()
        return html[:insert_at] + '\n' + block + html[insert_at:]
    # Fall back to after the chapter-opener figure
    fig_pat = re.compile(
        r'(<figure\s+class="illustration\s+chapter-opener"[^>]*>[\s\S]*?</figure>)',
        re.I,
    )
    m = fig_pat.search(html)
    if m:
        insert_at = m.end()
        return html[:insert_at] + '\n' + block + html[insert_at:]
    # Last resort: right after <main ...>
    main_pat = re.compile(r'(<main\s+class="content"[^>]*>)', re.I)
    m = main_pat.search(html)
    if m:
        insert_at = m.end()
        return html[:insert_at] + '\n' + block + html[insert_at:]
    return html


def insert_looking_back(html: str, block: str) -> str:
    """Insert looking-back after the epigraph (after </blockquote>), or after
    pagefind-meta if epigraph is absent."""
    epi_pat = re.compile(r'(<blockquote\s+class="epigraph"[\s\S]*?</blockquote>)', re.I)
    m = epi_pat.search(html)
    if m:
        insert_at = m.end()
        return html[:insert_at] + '\n' + block + html[insert_at:]
    # Fall back to after pagefind-meta
    meta_pat = re.compile(
        r'(<span class="pagefind-meta-injected"[^>]*data-pagefind-meta="chapter:[^"]*"[^>]*>\s*</span>)',
        re.I,
    )
    m = meta_pat.search(html)
    if m:
        insert_at = m.end()
        return html[:insert_at] + '\n' + block + html[insert_at:]
    # Last resort: after <main ...>
    main_pat = re.compile(r'(<main\s+class="content"[^>]*>)', re.I)
    m = main_pat.search(html)
    if m:
        insert_at = m.end()
        return html[:insert_at] + '\n' + block + html[insert_at:]
    return html


def insert_prereqs(html: str, block: str) -> str:
    """Insert prereqs block. Prefer to convert an existing Note: Prerequisites
    callout if present; otherwise insert before the <h2>Sections</h2>."""
    if NOTE_PREREQS_CALLOUT_RE.search(html):
        # Convert the existing callout to canonical prereqs div, preserving items
        def repl(m: re.Match) -> str:
            ul = m.group(1)
            return (
                '<div class="prereqs">\n'
                '<h3 id="prerequisites">Prerequisites</h3>\n'
                f'{ul}\n'
                '</div>'
            )
        return NOTE_PREREQS_CALLOUT_RE.sub(repl, html, count=1)
    # Otherwise insert before <h2>Sections</h2> (preferred), failing that before
    # <ul class="sections-list">.
    sec_h2 = re.search(r'<h2>\s*Sections\s*</h2>', html, re.I)
    if sec_h2:
        return html[:sec_h2.start()] + block + '\n' + html[sec_h2.start():]
    secul = re.search(r'<ul\s+class="sections-list"', html, re.I)
    if secul:
        return html[:secul.start()] + block + '\n' + html[secul.start():]
    return html


def insert_whats_next(html: str, block: str) -> str:
    """Insert whats-next block after </ul class="sections-list"> and before
    <nav class="chapter-nav">."""
    nav_pat = re.compile(r'(<nav\s+class="chapter-nav")', re.I)
    m = nav_pat.search(html)
    if m:
        return html[:m.start()] + block + '\n' + html[m.start():]
    return html


# ------------------------------------------------------------
# Main loop
# ------------------------------------------------------------

def main(dry_run: bool = False):
    results = {
        'epigraph_added': [], 'epigraph_skipped': [],
        'looking_back_added': [], 'looking_back_skipped': [],
        'prereqs_added': [], 'prereqs_converted': [], 'prereqs_skipped': [],
        'whats_next_added': [], 'whats_next_skipped': [],
        'errors': [],
    }
    for rel, spec in CHAPTERS.items():
        path = ROOT / rel
        if not path.exists():
            results['errors'].append(f'missing file: {rel}')
            continue
        text = path.read_text(encoding='utf-8')
        original = text

        # 1) Epigraph
        if needs_epigraph(text):
            block = build_epigraph(spec['agent'], spec['persona'], spec['epigraph_quote'])
            new_text = insert_epigraph(text, block)
            if new_text != text:
                text = new_text
                results['epigraph_added'].append(rel)
            else:
                results['errors'].append(f'epigraph insert failed: {rel}')
        else:
            results['epigraph_skipped'].append(rel)

        # 2) Looking-back
        if needs_looking_back(text):
            block = build_looking_back(spec['looking_back_html'])
            new_text = insert_looking_back(text, block)
            if new_text != text:
                text = new_text
                results['looking_back_added'].append(rel)
            else:
                results['errors'].append(f'looking-back insert failed: {rel}')
        else:
            results['looking_back_skipped'].append(rel)

        # 3) Prereqs
        if needs_prereqs(text):
            # Try to convert existing Note: Prerequisites callout first
            if NOTE_PREREQS_CALLOUT_RE.search(text):
                new_text = insert_prereqs(text, '')  # block ignored in conversion path
                if new_text != text:
                    text = new_text
                    results['prereqs_converted'].append(rel)
                else:
                    results['errors'].append(f'prereqs convert failed: {rel}')
            else:
                block = build_prereqs(spec['prereqs_items'])
                new_text = insert_prereqs(text, block)
                if new_text != text:
                    text = new_text
                    results['prereqs_added'].append(rel)
                else:
                    results['errors'].append(f'prereqs insert failed: {rel}')
        else:
            results['prereqs_skipped'].append(rel)

        # 4) What's-Next (only for the 1 chapter)
        if 'next_paragraph' in spec and needs_whats_next(text):
            block = build_whats_next(spec['next_paragraph'])
            new_text = insert_whats_next(text, block)
            if new_text != text:
                text = new_text
                results['whats_next_added'].append(rel)
            else:
                results['errors'].append(f'whats-next insert failed: {rel}')

        if text != original and not dry_run:
            path.write_text(text, encoding='utf-8')

    # Summary
    print('=' * 60)
    for k, v in results.items():
        if isinstance(v, list):
            print(f'{k}: {len(v)}')
    if results['errors']:
        print('\nERRORS:')
        for e in results['errors']:
            print(' ', e)
    return results


if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    main(dry_run=dry)
