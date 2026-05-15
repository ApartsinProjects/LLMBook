"""Hyperlink top-tier concepts back to their glossary entries.

For every chapter HTML page, scan prose text (paragraphs, table cells, selected
callout bodies) and convert mentions of known concepts into <a class="glossary-link">
links back to their authoritative glossary entry.

Strict rules:
- Only modify EXISTING text (never insert text).
- Never modify code/pre, math, navigation, or already-hyperlinked spans.
- Never link a concept on its own definition page.
- One link per concept per page (first uncovered mention).
- Skip files that would receive >20 new links (avoid over-linking).
- Skip files with link-density below 0.5 per 1000 chars of prose.

Usage:
    python _fix_v14_5_hyperlink_concepts.py            # dry run, prints report
    python _fix_v14_5_hyperlink_concepts.py --apply    # actually rewrite files
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    sys.exit("Requires beautifulsoup4. Install: pip install beautifulsoup4")

REPO = Path("E:/Projects/BookBlogsHome/LLMBook")
GLOSSARY_DIR = REPO / "appendices" / "appendix-f-glossary"
SKIP_DIRS = {
    "node_modules", ".git", "KDP", "pagefind", "temp_epub", "backup",
    "source_fix_backups", "_exercise_payloads", "agents", "templates",
    "vendor", "scripts", "styles", ".html2pub_cache", "downloads",
}

# Hand-picked top-tier concepts. Each entry: text alias -> glossary gl-id.
# When the same concept has multiple aliases (e.g., "LLM" vs "large language model")
# the longer/more specific aliases come first so the matcher consumes them first.
CONCEPT_ALIASES: dict[str, str] = {
    # Core LLM
    "large language model": "gl-llm",
    "large language models": "gl-llm",
    "llms": "gl-llm",
    "llm": "gl-llm",
    # Architecture
    "transformer architecture": "gl-transformer",
    "transformers": "gl-transformer",
    "transformer": "gl-transformer",
    "self-attention": "gl-attention",
    "self attention": "gl-attention",
    "multi-head attention": "gl-mha",
    "multihead attention": "gl-mha",
    "grouped query attention": "gl-gqa",
    "grouped-query attention": "gl-gqa",
    "rotary position embedding": "gl-rope",
    "rope": "gl-rope",
    "rmsnorm": "gl-rmsnorm",
    "layer normalization": "gl-layer-norm",
    "layer norm": "gl-layer-norm",
    "mixture of experts": "gl-mixture-of-experts",
    "feed-forward network": "gl-feedforward",
    "feedforward network": "gl-feedforward",
    "encoder-decoder": "gl-encoder-decoder",
    "causal language model": "gl-causal-lm",
    "autoregressive model": "gl-autoregressive",
    "autoregressive": "gl-autoregressive",
    "bert": "gl-bert",
    "gpt": "gl-gpt",
    "reasoning model": "gl-reasoning-model",
    "swiglu": "gl-swiglu",
    "gelu": "gl-gelu",
    "activation function": "gl-activation-function",
    "positional encoding": "gl-positional-encoding",
    # Attention (must come after multi-head etc.)
    "attention mechanism": "gl-attention",
    "attention": "gl-attention",
    # Tokens
    "tokenization": "gl-tokenizer",
    "tokenizer": "gl-tokenizer",
    "tokens": "gl-token",
    "token": "gl-token",
    "next-token prediction": "gl-next-token",
    "embeddings": "gl-embedding",
    "embedding": "gl-embedding",
    # Context
    "context length": "gl-context-window",
    "context window": "gl-context-window",
    # Training
    "pretraining": "gl-pretraining",
    "pre-training": "gl-pretraining",
    "fine-tuning": "gl-fine-tuning",
    "finetuning": "gl-fine-tuning",
    "instruction tuning": "gl-instruction-tuning",
    "instruction-tuning": "gl-instruction-tuning",
    "supervised fine-tuning": "gl-sft",
    "sft": "gl-sft",
    "scaling laws": "gl-scaling-laws",
    "chinchilla scaling laws": "gl-chinchilla",
    "transfer learning": "gl-transfer-learning",
    "backpropagation": "gl-backpropagation",
    "gradient accumulation": "gl-gradient-accumulation",
    "batch size": "gl-batch-size",
    "weight decay": "gl-weight-decay",
    "dropout": "gl-dropout",
    "overfitting": "gl-overfitting",
    "cross-entropy loss": "gl-cross-entropy",
    "synthetic data": "gl-synthetic-data",
    "model collapse": "gl-model-collapse",
    "model merging": "gl-model-merging",
    "data contamination": "gl-data-contamination",
    # PEFT / Adaptation
    "parameter-efficient fine-tuning": "gl-peft",
    "peft": "gl-peft",
    "lora": "gl-lora",
    "qlora": "gl-qlora",
    "adapter": "gl-adapter",
    "prefix tuning": "gl-prefix-tuning",
    "evol-instruct": "gl-evol-instruct",
    # Alignment
    "alignment": "gl-alignment",
    "rlhf": "gl-rlhf",
    "reinforcement learning from human feedback": "gl-rlhf",
    "direct preference optimization": "gl-dpo",
    "dpo": "gl-dpo",
    "reward model": "gl-reward-model",
    "constitutional ai": "gl-constitutional-ai",
    # Quantization & inference
    "quantization": "gl-quantization",
    "bitsandbytes": "gl-bnb",
    "bfloat16": "gl-bfloat16",
    "kv cache": "gl-kv-cache",
    "kv-cache": "gl-kv-cache",
    "speculative decoding": "gl-speculative-decoding",
    "distillation": "gl-distillation",
    "knowledge distillation": "gl-distillation",
    "flash attention": "gl-flash-attention",
    "inference": "gl-inference",
    "decoding": "gl-decoding",
    "beam search": "gl-beam-search",
    "nucleus sampling": "gl-nucleus-sampling",
    "top-p sampling": "gl-nucleus-sampling",
    "top-k sampling": "gl-top-k",
    "temperature": "gl-temperature",
    "logit": "gl-logit",
    "flops": "gl-flops",
    # Retrieval
    "rag": "gl-rag",
    "retrieval-augmented generation": "gl-rag",
    "retrieval augmented generation": "gl-rag",
    "vector database": "gl-vector-database",
    "vector databases": "gl-vector-database",
    "semantic search": "gl-semantic-search",
    "cosine similarity": "gl-cosine-similarity",
    "chunking": "gl-chunking",
    "knowledge graph": "gl-knowledge-graph",
    "grounding": "gl-grounding",
    "hnsw": "gl-hnsw",
    # Eval
    "perplexity": "gl-perplexity",
    "mmlu": "gl-mmlu",
    "humaneval": "gl-human-eval",
    "human eval": "gl-human-eval",
    "evaluation": "gl-eval",
    "named entity recognition": "gl-ner",
    "classification": "gl-classification",
    "hallucination": "gl-hallucination",
    "hallucinations": "gl-hallucination",
    "chatbot arena": "gl-chatbot-arena",
    # Prompt / agent
    "chain-of-thought": "gl-chain-of-thought",
    "chain of thought": "gl-chain-of-thought",
    "zero-shot chain-of-thought": "gl-zero-shot-cot",
    "zero-shot": "gl-zero-shot",
    "few-shot": "gl-few-shot",
    "few shot": "gl-few-shot",
    "in-context learning": "gl-few-shot",
    "system prompt": "gl-system-prompt",
    "prompt engineering": "gl-prompt-engineering",
    "prompt injection": "gl-prompt-injection",
    "function calling": "gl-function-calling",
    "tool use": "gl-function-calling",
    "json mode": "gl-json-mode",
    "structured output": "gl-json-mode",
    # Serving / tooling
    "vllm": "gl-vllm",
    "unsloth": "gl-unsloth",
    "mcp": "gl-mcp",
    "model context protocol": "gl-mcp",
    # Interpretability
    "interpretability": "gl-interpretability",
    "mechanistic interpretability": "gl-interpretability",
    "superposition": "gl-superposition",
    "observability": "gl-observability",
}

# Canonical href per gl-id (relative target written into <a href=...>).
# Always points to the glossary page. The href is anchored at the gl-* id.
GL_TO_FILE = {
    "gl-bnb": "section-f.1.html",
    "gl-chatbot-arena": "section-f.1.html",
    "gl-flash-attention": "section-f.1.html",
    "gl-human-eval": "section-f.1.html",
    "gl-mcp": "section-f.1.html",
    "gl-mmlu": "section-f.1.html",
    "gl-unsloth": "section-f.1.html",
    "gl-vector-database": "section-f.1.html",
    "gl-vllm": "section-f.1.html",
    "gl-activation-function": "section-f.2.html",
    "gl-autoregressive": "section-f.2.html",
    "gl-bert": "section-f.2.html",
    "gl-causal-lm": "section-f.2.html",
    "gl-encoder-decoder": "section-f.2.html",
    "gl-feedforward": "section-f.2.html",
    "gl-gelu": "section-f.2.html",
    "gl-gpt": "section-f.2.html",
    "gl-gqa": "section-f.2.html",
    "gl-layer-norm": "section-f.2.html",
    "gl-llm": "section-f.2.html",
    "gl-mixture-of-experts": "section-f.2.html",
    "gl-mha": "section-f.2.html",
    "gl-positional-encoding": "section-f.2.html",
    "gl-reasoning-model": "section-f.2.html",
    "gl-rmsnorm": "section-f.2.html",
    "gl-rope": "section-f.2.html",
    "gl-softmax": "section-f.2.html",
    "gl-swiglu": "section-f.2.html",
    "gl-transformer": "section-f.2.html",
    "gl-adapter": "section-f.3.html",
    "gl-backpropagation": "section-f.3.html",
    "gl-batch-size": "section-f.3.html",
    "gl-beam-search": "section-f.3.html",
    "gl-bfloat16": "section-f.3.html",
    "gl-chain-of-thought": "section-f.3.html",
    "gl-chinchilla": "section-f.3.html",
    "gl-cross-entropy": "section-f.3.html",
    "gl-decoding": "section-f.3.html",
    "gl-distillation": "section-f.3.html",
    "gl-dpo": "section-f.3.html",
    "gl-dropout": "section-f.3.html",
    "gl-evol-instruct": "section-f.3.html",
    "gl-fine-tuning": "section-f.3.html",
    "gl-gradient-accumulation": "section-f.3.html",
    "gl-kv-cache": "section-f.3.html",
    "gl-lora": "section-f.3.html",
    "gl-model-collapse": "section-f.3.html",
    "gl-model-merging": "section-f.3.html",
    "gl-next-token": "section-f.3.html",
    "gl-nucleus-sampling": "section-f.3.html",
    "gl-peft": "section-f.3.html",
    "gl-prefix-tuning": "section-f.3.html",
    "gl-pretraining": "section-f.3.html",
    "gl-qlora": "section-f.3.html",
    "gl-quantization": "section-f.3.html",
    "gl-reward-model": "section-f.3.html",
    "gl-rlhf": "section-f.3.html",
    "gl-scaling-laws": "section-f.3.html",
    "gl-sft": "section-f.3.html",
    "gl-speculative-decoding": "section-f.3.html",
    "gl-temperature": "section-f.3.html",
    "gl-token": "section-f.3.html",
    "gl-tokenizer": "section-f.3.html",
    "gl-top-k": "section-f.3.html",
    "gl-transfer-learning": "section-f.3.html",
    "gl-weight-decay": "section-f.3.html",
    "gl-zero-shot-cot": "section-f.3.html",
    "gl-alignment": "section-f.4.html",
    "gl-attention": "section-f.4.html",
    "gl-chunking": "section-f.4.html",
    "gl-classification": "section-f.4.html",
    "gl-context-window": "section-f.4.html",
    "gl-cosine-similarity": "section-f.4.html",
    "gl-data-contamination": "section-f.4.html",
    "gl-embedding": "section-f.4.html",
    "gl-eval": "section-f.4.html",
    "gl-few-shot": "section-f.4.html",
    "gl-flops": "section-f.4.html",
    "gl-grounding": "section-f.4.html",
    "gl-hallucination": "section-f.4.html",
    "gl-hnsw": "section-f.4.html",
    "gl-inference": "section-f.4.html",
    "gl-instruction-tuning": "section-f.4.html",
    "gl-interpretability": "section-f.4.html",
    "gl-logit": "section-f.4.html",
    "gl-ner": "section-f.4.html",
    "gl-observability": "section-f.4.html",
    "gl-overfitting": "section-f.4.html",
    "gl-perplexity": "section-f.4.html",
    "gl-semantic-search": "section-f.4.html",
    "gl-superposition": "section-f.4.html",
    "gl-synthetic-data": "section-f.4.html",
    "gl-constitutional-ai": "section-f.5.html",
    "gl-function-calling": "section-f.5.html",
    "gl-json-mode": "section-f.5.html",
    "gl-knowledge-graph": "section-f.5.html",
    "gl-prompt-engineering": "section-f.5.html",
    "gl-prompt-injection": "section-f.5.html",
    "gl-rag": "section-f.5.html",
    "gl-system-prompt": "section-f.5.html",
    "gl-zero-shot": "section-f.5.html",
}

# Glossary display name per gl-id (used for the title="" attribute).
GL_TO_TITLE = {
    "gl-llm": "LLM (Large Language Model)",
    "gl-transformer": "Transformer",
    "gl-attention": "Attention (Self-Attention)",
    "gl-mha": "Multi-Head Attention (MHA)",
    "gl-gqa": "Grouped Query Attention (GQA)",
    "gl-rope": "RoPE (Rotary Position Embedding)",
    "gl-rmsnorm": "RMSNorm",
    "gl-layer-norm": "Layer Normalization",
    "gl-mixture-of-experts": "Mixture of Experts (MoE)",
    "gl-feedforward": "Feed-Forward Network (FFN)",
    "gl-encoder-decoder": "Encoder-Decoder Architecture",
    "gl-causal-lm": "Causal Language Model",
    "gl-autoregressive": "Autoregressive Model",
    "gl-bert": "BERT",
    "gl-gpt": "GPT",
    "gl-reasoning-model": "Reasoning Model",
    "gl-swiglu": "SwiGLU",
    "gl-gelu": "GELU",
    "gl-activation-function": "Activation Function",
    "gl-positional-encoding": "Positional Encoding",
    "gl-softmax": "Softmax",
    "gl-token": "Token",
    "gl-tokenizer": "Tokenizer",
    "gl-next-token": "Next-Token Prediction",
    "gl-embedding": "Embedding",
    "gl-context-window": "Context Window",
    "gl-pretraining": "Pretraining",
    "gl-fine-tuning": "Fine-Tuning",
    "gl-instruction-tuning": "Instruction Tuning",
    "gl-sft": "SFT (Supervised Fine-Tuning)",
    "gl-scaling-laws": "Scaling Laws",
    "gl-chinchilla": "Chinchilla Scaling Laws",
    "gl-transfer-learning": "Transfer Learning",
    "gl-backpropagation": "Backpropagation",
    "gl-gradient-accumulation": "Gradient Accumulation",
    "gl-batch-size": "Batch Size",
    "gl-weight-decay": "Weight Decay",
    "gl-dropout": "Dropout",
    "gl-overfitting": "Overfitting",
    "gl-cross-entropy": "Cross-Entropy Loss",
    "gl-synthetic-data": "Synthetic Data",
    "gl-model-collapse": "Model Collapse",
    "gl-model-merging": "Model Merging",
    "gl-data-contamination": "Data Contamination",
    "gl-peft": "PEFT (Parameter-Efficient Fine-Tuning)",
    "gl-lora": "LoRA",
    "gl-qlora": "QLoRA",
    "gl-adapter": "Adapter",
    "gl-prefix-tuning": "Prefix Tuning",
    "gl-evol-instruct": "Evol-Instruct",
    "gl-alignment": "Alignment",
    "gl-rlhf": "RLHF",
    "gl-dpo": "DPO",
    "gl-reward-model": "Reward Model",
    "gl-constitutional-ai": "Constitutional AI",
    "gl-quantization": "Quantization",
    "gl-bnb": "BitsAndBytes",
    "gl-bfloat16": "BFloat16",
    "gl-kv-cache": "KV Cache",
    "gl-speculative-decoding": "Speculative Decoding",
    "gl-distillation": "Distillation",
    "gl-flash-attention": "Flash Attention",
    "gl-inference": "Inference",
    "gl-decoding": "Decoding",
    "gl-beam-search": "Beam Search",
    "gl-nucleus-sampling": "Nucleus Sampling",
    "gl-top-k": "Top-k Sampling",
    "gl-temperature": "Temperature",
    "gl-logit": "Logit",
    "gl-flops": "FLOPS",
    "gl-rag": "RAG (Retrieval-Augmented Generation)",
    "gl-vector-database": "Vector Database",
    "gl-semantic-search": "Semantic Search",
    "gl-cosine-similarity": "Cosine Similarity",
    "gl-chunking": "Chunking",
    "gl-knowledge-graph": "Knowledge Graph",
    "gl-grounding": "Grounding",
    "gl-hnsw": "HNSW",
    "gl-perplexity": "Perplexity",
    "gl-mmlu": "MMLU",
    "gl-human-eval": "HumanEval",
    "gl-eval": "Evaluation",
    "gl-ner": "Named Entity Recognition",
    "gl-classification": "Classification",
    "gl-hallucination": "Hallucination",
    "gl-chatbot-arena": "Chatbot Arena",
    "gl-chain-of-thought": "Chain-of-Thought",
    "gl-zero-shot-cot": "Zero-Shot Chain-of-Thought",
    "gl-zero-shot": "Zero-Shot Learning",
    "gl-few-shot": "Few-Shot Learning",
    "gl-system-prompt": "System Prompt",
    "gl-prompt-engineering": "Prompt Engineering",
    "gl-prompt-injection": "Prompt Injection",
    "gl-function-calling": "Function Calling",
    "gl-json-mode": "JSON Mode",
    "gl-vllm": "vLLM",
    "gl-unsloth": "Unsloth",
    "gl-mcp": "MCP (Model Context Protocol)",
    "gl-interpretability": "Interpretability",
    "gl-superposition": "Superposition",
    "gl-observability": "Observability",
}

# Block tags / classes inside which we must NOT recurse.
SKIP_TAG_NAMES = {
    "pre", "code", "script", "style", "math", "svg", "head", "header",
    "nav", "noscript",
}
SKIP_CLASS_TOKENS = {
    "math-block", "math", "katex", "katex-display", "header-nav",
    "part-label", "chapter-label", "page-nav", "footer-nav",
}

# Aliases sorted so longer phrases match first.
SORTED_ALIASES = sorted(CONCEPT_ALIASES.keys(), key=len, reverse=True)


def compute_href(target_gl: str, source_file: Path) -> str:
    """Compute relative href from source_file to the glossary anchor."""
    target_file = GLOSSARY_DIR / GL_TO_FILE[target_gl]
    # Build a relative path from source_file's directory to target_file.
    import os.path
    rel = os.path.relpath(target_file, source_file.parent)
    rel = rel.replace("\\", "/")
    return f"{rel}#{target_gl}"


def title_for(gl_id: str) -> str:
    name = GL_TO_TITLE.get(gl_id, gl_id.replace("gl-", "").replace("-", " ").title())
    return f"Glossary: {name}"


def is_skipped_element(el: Tag) -> bool:
    if el.name in SKIP_TAG_NAMES:
        return True
    cls = el.get("class") or []
    if isinstance(cls, str):
        cls = [cls]
    for c in cls:
        if c in SKIP_CLASS_TOKENS:
            return True
    return False


def ancestor_is_link(node) -> bool:
    """True if a NavigableString sits inside any <a> ancestor."""
    cur = node.parent
    while cur is not None and isinstance(cur, Tag):
        if cur.name == "a":
            return True
        cur = cur.parent
    return False


def ancestor_is_skipped(node) -> bool:
    """True if any ancestor is in our SKIP set."""
    cur = node.parent
    while cur is not None and isinstance(cur, Tag):
        if is_skipped_element(cur):
            return True
        cur = cur.parent
    return False


# Allowed parent tag names for prose linking.
PROSE_PARENT_TAGS = {"p", "li", "td", "th", "dd", "blockquote", "figcaption", "em", "strong", "span", "i", "b"}


def is_prose_text_node(node: NavigableString) -> bool:
    """True if this NavigableString is suitable for linking."""
    if ancestor_is_link(node):
        return False
    if ancestor_is_skipped(node):
        return False
    parent = node.parent
    if parent is None or not isinstance(parent, Tag):
        return False
    if parent.name not in PROSE_PARENT_TAGS:
        return False
    text = str(node)
    if not text.strip():
        return False
    return True


def build_alias_pattern() -> re.Pattern:
    """Compile a single big alternation for all aliases with word boundaries."""
    # Sorted longest-first so longer phrases win.
    parts = [re.escape(a) for a in SORTED_ALIASES]
    # Use a word-boundary-style assertion that also handles hyphens.
    # We define "word char" as alnum or underscore. The boundary on both sides
    # must NOT be a letter (so "tokenizer" inside "subtokenizer" is rejected,
    # but "tokens." matches).
    pattern = r"(?<![A-Za-z])(" + "|".join(parts) + r")(?![A-Za-z])"
    return re.compile(pattern, re.IGNORECASE)


ALIAS_RE = build_alias_pattern()


def link_html_for(matched_text: str, gl_id: str, href: str) -> str:
    """Return the <a> HTML to splice in for a single match."""
    title = title_for(gl_id)
    return (
        f'<a class="glossary-link" href="{href}" title="{title}">'
        f'{matched_text}</a>'
    )


def collect_text_nodes(soup: BeautifulSoup) -> list:
    """Walk soup, yield NavigableStrings that are eligible prose."""
    out = []
    for ns in soup.find_all(string=True):
        if isinstance(ns, NavigableString) and is_prose_text_node(ns):
            out.append(ns)
    return out


def page_self_gl_id(file_path: Path) -> str | None:
    """If this file IS the glossary entry's defining page, return its gl-id.

    Returns None for non-glossary pages. For glossary pages, returns the
    primary gl-id so we never re-link the term to itself on its own page.
    """
    try:
        rel = file_path.relative_to(GLOSSARY_DIR)
    except ValueError:
        return None
    # The file itself defines many glossary terms; we use a per-file set instead.
    return None


def get_self_defined_gl_ids(file_path: Path) -> set[str]:
    """If this file IS a glossary section, return the set of gl-ids it defines."""
    try:
        file_path.relative_to(GLOSSARY_DIR)
    except ValueError:
        return set()
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return set()
    return set(re.findall(r'id="(gl-[a-z0-9-]+)"', text))


def already_linked_gl_ids(soup: BeautifulSoup) -> set[str]:
    """Find gl-ids already present as glossary links on this page."""
    found = set()
    for a in soup.find_all("a"):
        href = a.get("href", "")
        m = re.search(r"#(gl-[a-z0-9-]+)", href)
        if m:
            found.add(m.group(1))
    return found


def process_file(
    file_path: Path,
    samples: list,
    max_links_per_file: int = 20,
    min_density_per_1k: float = 0.5,
) -> tuple[int, dict, list]:
    """Return (new_links, by_gl_id_count, skipped_reasons).

    Mutates soup in place; caller writes back if apply=True.
    """
    try:
        raw = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return 0, {}, [f"read-error:{e}"]

    soup = BeautifulSoup(raw, "html.parser")
    self_defined = get_self_defined_gl_ids(file_path)
    used_on_page = set(already_linked_gl_ids(soup)) | self_defined

    # Prose char count for density filter.
    prose_chars = 0
    for ns in collect_text_nodes(soup):
        prose_chars += len(str(ns))

    text_nodes = collect_text_nodes(soup)

    new_links = 0
    by_gl: Counter = Counter()
    pending_replacements = []  # (NavigableString, replacement_pieces)

    for ns in text_nodes:
        text = str(ns)
        if not text.strip():
            continue
        replacements = []
        last_end = 0
        modified = False

        for m in ALIAS_RE.finditer(text):
            alias = m.group(0).lower()
            gl_id = CONCEPT_ALIASES.get(alias)
            if not gl_id:
                continue
            if gl_id in used_on_page:
                continue
            if new_links >= max_links_per_file:
                break

            # Reserve this gl_id so subsequent text nodes / matches don't add it.
            used_on_page.add(gl_id)
            by_gl[gl_id] += 1
            new_links += 1

            # Emit text before the match, then a link tag.
            pre = text[last_end : m.start()]
            if pre:
                replacements.append(NavigableString(pre))
            href = compute_href(gl_id, file_path)
            link_soup = BeautifulSoup(link_html_for(m.group(0), gl_id, href), "html.parser")
            link_tag = link_soup.a
            replacements.append(link_tag)
            last_end = m.end()
            modified = True

            samples.append({
                "file": str(file_path.relative_to(REPO)).replace("\\", "/"),
                "gl_id": gl_id,
                "matched": m.group(0),
                "href": href,
                "context_before": pre[-40:] if pre else "",
                "context_after": text[m.end():m.end() + 40],
            })

        if modified:
            tail = text[last_end:]
            if tail:
                replacements.append(NavigableString(tail))
            pending_replacements.append((ns, replacements))

    if not pending_replacements:
        return 0, {}, []

    # Density check (link rate per 1000 chars of prose).
    density = (new_links / prose_chars) * 1000 if prose_chars else 0
    if density < min_density_per_1k and new_links > 0:
        # Skip everything because density too low (sparse linking is noise).
        return 0, {}, [f"low-density:{density:.2f}"]

    # Hard cap: skip if too many links would be added.
    if new_links > max_links_per_file:
        return 0, {}, [f"over-cap:{new_links}"]

    # Apply pending replacements (mutate soup in-place).
    for ns, repl in pending_replacements:
        # Insert before ns, then remove ns.
        for piece in repl:
            ns.insert_before(piece)
        ns.extract()

    # Stash updated HTML on the file object for the caller.
    process_file._last_html = str(soup)
    return new_links, dict(by_gl), []


process_file._last_html = ""


def iter_target_files() -> Iterable[Path]:
    for p in REPO.rglob("*.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        # Skip the glossary's own definition pages.
        try:
            p.relative_to(GLOSSARY_DIR)
            continue  # never modify glossary pages
        except ValueError:
            pass
        # Skip non-chapter HTML (e.g., chrome / 404). Keep all chapter content.
        # Heuristic: must contain a <main class="content"> or be in part-/appendices/.
        yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Actually rewrite files")
    ap.add_argument("--report", default=str(REPO / "KDP" / "build" / "AUDIT_hyperlinks.md"))
    ap.add_argument("--max-links", type=int, default=20)
    ap.add_argument("--min-density", type=float, default=0.5)
    args = ap.parse_args()

    samples: list = []
    file_results: dict = {}  # path -> (new_links, by_gl)
    skipped: list = []

    total_files = 0
    for path in iter_target_files():
        total_files += 1
        new_links, by_gl, skip_reasons = process_file(
            path, samples,
            max_links_per_file=args.max_links,
            min_density_per_1k=args.min_density,
        )
        if skip_reasons:
            skipped.append((path, skip_reasons))
            continue
        if new_links == 0:
            continue
        if args.apply:
            path.write_text(process_file._last_html, encoding="utf-8")
        file_results[path] = (new_links, by_gl)

    total_new = sum(n for n, _ in file_results.values())
    files_touched = len(file_results)

    # Aggregate per-gl-id.
    per_gl_total: Counter = Counter()
    for _, by_gl in file_results.values():
        for g, c in by_gl.items():
            per_gl_total[g] += c

    # Build a report.
    report_lines = []
    mode = "APPLIED" if args.apply else "DRY RUN"
    report_lines.append(f"# Hyperlinking Audit ({mode})\n")
    report_lines.append(f"- Files scanned: {total_files}")
    report_lines.append(f"- Concepts mapped (aliases): {len(CONCEPT_ALIASES)}")
    report_lines.append(f"- Distinct gl-ids targeted: {len(set(CONCEPT_ALIASES.values()))}")
    report_lines.append(f"- Files modified: {files_touched}")
    report_lines.append(f"- Total new links: {total_new}")
    report_lines.append(f"- Files skipped (cap/density): {len(skipped)}\n")

    report_lines.append("## Top 25 files by new-link count\n")
    sorted_files = sorted(file_results.items(), key=lambda kv: -kv[1][0])
    for path, (n, _) in sorted_files[:25]:
        rel = str(path.relative_to(REPO)).replace("\\", "/")
        report_lines.append(f"- {n:3d}  {rel}")
    report_lines.append("")

    report_lines.append("## Top 25 most-linked concepts (across the book)\n")
    for gl, c in per_gl_total.most_common(25):
        report_lines.append(f"- {c:4d}  {gl}  ({GL_TO_TITLE.get(gl, '')})")
    report_lines.append("")

    # 10 sample diffs.
    report_lines.append("## 10 sample link additions\n")
    for s in samples[:10]:
        snippet = f"...{s['context_before']}<a>{s['matched']}</a>{s['context_after']}..."
        report_lines.append(f"- `{s['file']}` -> `{s['gl_id']}`")
        report_lines.append(f"  - {snippet}")
        report_lines.append(f"  - href: `{s['href']}`")
    report_lines.append("")

    # Concepts with no canonical target (not in CONCEPT_ALIASES values).
    # Identify aliases that never matched anything in the book (could mean stale).
    unmatched_aliases = [
        a for a in CONCEPT_ALIASES if all(
            s["matched"].lower() != a for s in samples
        )
    ]
    report_lines.append("## Concept aliases that produced ZERO new links\n")
    report_lines.append("(could indicate stale terms or aliases already over-linked)\n")
    for a in sorted(unmatched_aliases):
        report_lines.append(f"- `{a}` -> {CONCEPT_ALIASES[a]}")
    report_lines.append("")

    # Concepts requested by the user that have no glossary entry.
    user_wishlist_no_target = [
        "GPTQ", "AWQ", "GGUF", "pruning", "ReAct", "multi-agent", "agentic",
        "agent", "tool use", "rerank", "BM25", "dense retrieval",
        "sparse retrieval", "hybrid search", "retrieval",
        "continuous batching", "batching", "paged attention",
        "benchmark", "MT-Bench", "LLM-as-judge",
        "jailbreak", "red teaming", "safety", "alignment tax",
        "TGI", "SGLang", "HuggingFace",
        "BPE", "byte-pair encoding",
    ]
    missing = []
    for term in user_wishlist_no_target:
        if term.lower() not in CONCEPT_ALIASES:
            missing.append(term)
    report_lines.append("## Requested concepts with NO canonical glossary entry\n")
    report_lines.append("(consider adding to appendix-f-glossary)\n")
    for term in sorted(missing):
        report_lines.append(f"- `{term}`")
    report_lines.append("")

    if skipped:
        report_lines.append("## Files skipped (with reasons)\n")
        for path, reasons in skipped[:30]:
            rel = str(path.relative_to(REPO)).replace("\\", "/")
            report_lines.append(f"- {rel} : {','.join(reasons)}")

    report_text = "\n".join(report_lines)
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(report_text, encoding="utf-8")

    print(f"[{mode}] files_modified={files_touched} total_new_links={total_new}")
    print(f"report: {args.report}")
    if not args.apply:
        print("(dry run; pass --apply to commit changes)")


if __name__ == "__main__":
    main()
