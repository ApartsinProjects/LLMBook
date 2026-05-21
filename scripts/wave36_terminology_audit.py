"""Wave 36: terminology-keeper audit (REPORT-ONLY).

Scan all section HTML files for entity-name inconsistencies. Output a clean
report at docs/content-audit/TERMINOLOGY_INCONSISTENCIES.md.

We skip occurrences inside <code> or <pre> (package names with intentional
casing) and inside bibliography blocks (author name casing is intentional).

Each canonical-term group lists:
  - canonical spelling (recommended)
  - total non-canonical (inconsistent) occurrences book-wide
  - top 10 offending file paths with non-canonical occurrence counts
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts"}

# Strip out content we should not flag:
#   * <code>...</code>  (inline package names like openai, langchain)
#   * <pre>...</pre>    (code blocks)
#   * <div class="code-block-wrapper">...</div>  (code blocks)
#   * <a href="...">    (URLs and anchor refs)
#   * <script>, <style>, <header>, <footer>, <nav>
#   * HTML attributes (e.g. class="pytorch-icon")
#   * bibliography lists (author casing intentional)
SCRIPT_STYLE_RE = re.compile(r'<(script|style)[^>]*>.*?</\1>', re.DOTALL | re.IGNORECASE)
HEADER_FOOTER_RE = re.compile(r'<(header|footer|nav)[^>]*>.*?</\1>', re.DOTALL | re.IGNORECASE)
CODE_INLINE_RE = re.compile(r'<code\b[^>]*>.*?</code>', re.DOTALL | re.IGNORECASE)
PRE_RE = re.compile(r'<pre\b[^>]*>.*?</pre>', re.DOTALL | re.IGNORECASE)
CODE_BLOCK_RE = re.compile(
    r'<div\s+class="code-block-wrapper"[^>]*>.*?</div>\s*(?:<div\s+class="code-output"[^>]*>.*?</div>\s*)?',
    re.DOTALL | re.IGNORECASE,
)
BIB_RE = re.compile(
    r'<(?:ul|ol)\b[^>]*class="[^"]*(?:bibliography|references)[^"]*"[^>]*>.*?</(?:ul|ol)>',
    re.DOTALL | re.IGNORECASE,
)
BIB_SECTION_RE = re.compile(
    r'<section\b[^>]*(?:id|class)="[^"]*(?:bibliography|references|further-reading)[^"]*"[^>]*>.*?</section>',
    re.DOTALL | re.IGNORECASE,
)
HREF_RE = re.compile(r'<a\s[^>]*>.*?</a>', re.DOTALL | re.IGNORECASE)  # drop anchor text? no -- keep
# We only want to drop the URL parts. Keep visible anchor text.
ATTR_RE = re.compile(r'\s(?:href|src|class|id|alt|title|data-[a-z-]+)="[^"]*"', re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')
COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)


def strip_to_prose(html: str) -> str:
    """Strip code, pre, scripts, bibs, HTML attributes; keep visible prose."""
    s = COMMENT_RE.sub(' ', html)
    s = SCRIPT_STYLE_RE.sub(' ', s)
    s = HEADER_FOOTER_RE.sub(' ', s)
    s = CODE_BLOCK_RE.sub(' ', s)
    s = CODE_INLINE_RE.sub(' ', s)
    s = PRE_RE.sub(' ', s)
    s = BIB_RE.sub(' ', s)
    s = BIB_SECTION_RE.sub(' ', s)
    s = ATTR_RE.sub(' ', s)
    s = TAG_RE.sub(' ', s)
    return s


# =================================================================
# Canonical term groups.
# Each group has:
#   "canonical": the recommended spelling
#   "variants": list of (regex, label) pairs flagged as non-canonical
# Regexes use word boundaries via (?<![\w-]) (?![\w-]).
# We use case-sensitive matching where casing distinguishes variants.
# =================================================================

def wb(pat: str) -> str:
    return r'(?<![\w-])' + pat + r'(?![\w-])'


GROUPS = [
    # ------------- MODELS -------------
    {
        "name": "Llama-3 (model family)",
        "canonical": "Llama-3",
        "variants": [
            (re.compile(wb(r'LLaMA-3'), re.NOFLAG), "LLaMA-3"),
            (re.compile(wb(r'LLaMA 3'), re.NOFLAG), "LLaMA 3"),
            (re.compile(wb(r'LLAMA-3'), re.NOFLAG), "LLAMA-3"),
            (re.compile(wb(r'LLAMA 3'), re.NOFLAG), "LLAMA 3"),
            (re.compile(wb(r'llama-3'), re.NOFLAG), "llama-3"),
            (re.compile(wb(r'llama 3'), re.NOFLAG), "llama 3"),
            (re.compile(wb(r'Llama 3'), re.NOFLAG), "Llama 3 (use hyphen: Llama-3)"),
        ],
    },
    {
        "name": "Llama-2 (model family)",
        "canonical": "Llama-2",
        "variants": [
            (re.compile(wb(r'LLaMA-2'), re.NOFLAG), "LLaMA-2"),
            (re.compile(wb(r'LLaMA 2'), re.NOFLAG), "LLaMA 2"),
            (re.compile(wb(r'LLAMA-2'), re.NOFLAG), "LLAMA-2"),
            (re.compile(wb(r'llama-2'), re.NOFLAG), "llama-2"),
            (re.compile(wb(r'llama 2'), re.NOFLAG), "llama 2"),
            (re.compile(wb(r'Llama 2'), re.NOFLAG), "Llama 2 (use hyphen: Llama-2)"),
        ],
    },
    {
        "name": "GPT-4 (model)",
        "canonical": "GPT-4",
        "variants": [
            (re.compile(wb(r'gpt-4'), re.NOFLAG), "gpt-4"),
            (re.compile(wb(r'Gpt-4'), re.NOFLAG), "Gpt-4"),
            (re.compile(wb(r'GPT 4'), re.NOFLAG), "GPT 4 (use hyphen: GPT-4)"),
        ],
    },
    {
        "name": "GPT-3.5 (model)",
        "canonical": "GPT-3.5",
        "variants": [
            (re.compile(wb(r'gpt-3\.5'), re.NOFLAG), "gpt-3.5"),
            (re.compile(wb(r'GPT 3\.5'), re.NOFLAG), "GPT 3.5 (use hyphen: GPT-3.5)"),
        ],
    },
    {
        "name": "BERT (model)",
        "canonical": "BERT",
        "variants": [
            (re.compile(wb(r'Bert'), re.NOFLAG), "Bert"),
            (re.compile(wb(r'bert'), re.NOFLAG), "bert"),
        ],
    },
    {
        "name": "RoBERTa (model)",
        "canonical": "RoBERTa",
        "variants": [
            (re.compile(wb(r'Roberta'), re.NOFLAG), "Roberta"),
            (re.compile(wb(r'roberta'), re.NOFLAG), "roberta"),
            (re.compile(wb(r'ROBERTA'), re.NOFLAG), "ROBERTA"),
        ],
    },
    {
        "name": "Mixtral (model)",
        "canonical": "Mixtral",
        "variants": [
            (re.compile(wb(r'mixtral'), re.NOFLAG), "mixtral"),
            (re.compile(wb(r'MIXTRAL'), re.NOFLAG), "MIXTRAL"),
        ],
    },
    {
        "name": "Mistral (model)",
        "canonical": "Mistral",
        "variants": [
            (re.compile(wb(r'mistral'), re.NOFLAG), "mistral"),
            (re.compile(wb(r'MISTRAL'), re.NOFLAG), "MISTRAL"),
        ],
    },
    {
        "name": "Gemini (model)",
        "canonical": "Gemini",
        "variants": [
            (re.compile(wb(r'gemini'), re.NOFLAG), "gemini"),
            (re.compile(wb(r'GEMINI'), re.NOFLAG), "GEMINI"),
        ],
    },
    {
        "name": "Claude (model)",
        "canonical": "Claude",
        "variants": [
            (re.compile(wb(r'CLAUDE'), re.NOFLAG), "CLAUDE"),
            # not flagging 'claude' lowercase here -- could be code or person name
        ],
    },
    {
        "name": "DeepSeek (model)",
        "canonical": "DeepSeek",
        "variants": [
            (re.compile(wb(r'Deepseek'), re.NOFLAG), "Deepseek"),
            (re.compile(wb(r'deepseek'), re.NOFLAG), "deepseek"),
            (re.compile(wb(r'DEEPSEEK'), re.NOFLAG), "DEEPSEEK"),
        ],
    },
    {
        "name": "Qwen (model)",
        "canonical": "Qwen",
        "variants": [
            (re.compile(wb(r'QWEN'), re.NOFLAG), "QWEN"),
            (re.compile(wb(r'qwen'), re.NOFLAG), "qwen"),
        ],
    },
    # ------------- METHODS -------------
    {
        "name": "LoRA (method)",
        "canonical": "LoRA",
        "variants": [
            (re.compile(wb(r'Lora'), re.NOFLAG), "Lora"),
            (re.compile(wb(r'lora'), re.NOFLAG), "lora"),
            (re.compile(wb(r'LORA'), re.NOFLAG), "LORA"),
        ],
    },
    {
        "name": "QLoRA (method)",
        "canonical": "QLoRA",
        "variants": [
            (re.compile(wb(r'Qlora'), re.NOFLAG), "Qlora"),
            (re.compile(wb(r'qlora'), re.NOFLAG), "qlora"),
            (re.compile(wb(r'QLORA'), re.NOFLAG), "QLORA"),
        ],
    },
    {
        "name": "RLHF (method)",
        "canonical": "RLHF",
        "variants": [
            (re.compile(wb(r'Rlhf'), re.NOFLAG), "Rlhf"),
            (re.compile(wb(r'rlhf'), re.NOFLAG), "rlhf"),
        ],
    },
    {
        "name": "DPO (method)",
        "canonical": "DPO",
        "variants": [
            (re.compile(wb(r'Dpo'), re.NOFLAG), "Dpo"),
            (re.compile(wb(r'dpo'), re.NOFLAG), "dpo"),
        ],
    },
    {
        "name": "Chain-of-Thought (method)",
        "canonical": "Chain-of-Thought",
        "variants": [
            # Use canonical capitalization Chain-of-Thought (or CoT abbrev).
            (re.compile(wb(r'Chain[\s-]of[\s-]thought'), re.NOFLAG), "Chain-of-thought (lower t)"),
            (re.compile(wb(r'chain[\s-]of[\s-]thought'), re.NOFLAG), "chain-of-thought"),
            (re.compile(wb(r'chain[\s-]of[\s-]Thought'), re.NOFLAG), "chain-of-Thought"),
            (re.compile(wb(r'Chain of Thought'), re.NOFLAG), "Chain of Thought (use hyphens)"),
            (re.compile(wb(r'CHAIN-OF-THOUGHT'), re.NOFLAG), "CHAIN-OF-THOUGHT"),
        ],
    },
    {
        "name": "CoT (abbreviation)",
        "canonical": "CoT",
        "variants": [
            (re.compile(wb(r'COT'), re.NOFLAG), "COT"),
            (re.compile(wb(r'cot'), re.NOFLAG), "cot"),
        ],
    },
    {
        "name": "RoPE (method)",
        "canonical": "RoPE",
        "variants": [
            (re.compile(wb(r'Rope'), re.NOFLAG), "Rope"),
            (re.compile(wb(r'rope'), re.NOFLAG), "rope"),
        ],
    },
    {
        "name": "FlashAttention (method)",
        "canonical": "FlashAttention",
        "variants": [
            (re.compile(wb(r'Flash Attention'), re.NOFLAG), "Flash Attention"),
            (re.compile(wb(r'flash attention'), re.NOFLAG), "flash attention"),
            (re.compile(wb(r'flash-attention'), re.NOFLAG), "flash-attention"),
            (re.compile(wb(r'Flash-Attention'), re.NOFLAG), "Flash-Attention"),
            (re.compile(wb(r'flashattention'), re.NOFLAG), "flashattention"),
        ],
    },
    {
        "name": "PagedAttention (method)",
        "canonical": "PagedAttention",
        "variants": [
            (re.compile(wb(r'Paged Attention'), re.NOFLAG), "Paged Attention"),
            (re.compile(wb(r'paged attention'), re.NOFLAG), "paged attention"),
            (re.compile(wb(r'paged-attention'), re.NOFLAG), "paged-attention"),
            (re.compile(wb(r'pagedattention'), re.NOFLAG), "pagedattention"),
        ],
    },
    {
        "name": "Mixture-of-Experts (method)",
        "canonical": "Mixture-of-Experts",
        "variants": [
            (re.compile(wb(r'Mixture of Experts'), re.NOFLAG), "Mixture of Experts"),
            (re.compile(wb(r'mixture of experts'), re.NOFLAG), "mixture of experts"),
            (re.compile(wb(r'mixture-of-experts'), re.NOFLAG), "mixture-of-experts"),
        ],
    },
    {
        "name": "MoE (abbreviation)",
        "canonical": "MoE",
        "variants": [
            (re.compile(wb(r'MOE'), re.NOFLAG), "MOE"),
            (re.compile(wb(r'moe'), re.NOFLAG), "moe"),
        ],
    },
    {
        "name": "RAG (method)",
        "canonical": "RAG",
        "variants": [
            (re.compile(wb(r'Rag'), re.NOFLAG), "Rag"),
            # not flagging 'rag' lowercase since it is a common English word
        ],
    },
    {
        "name": "ReAct (method)",
        "canonical": "ReAct",
        "variants": [
            (re.compile(wb(r'REACT'), re.NOFLAG), "REACT"),
            # not flagging 'React' (could be React framework) or 'react' (verb)
        ],
    },
    {
        "name": "BM25 (method)",
        "canonical": "BM25",
        "variants": [
            (re.compile(wb(r'bm25'), re.NOFLAG), "bm25"),
            (re.compile(wb(r'Bm25'), re.NOFLAG), "Bm25"),
        ],
    },
    {
        "name": "GPTQ (method)",
        "canonical": "GPTQ",
        "variants": [
            (re.compile(wb(r'Gptq'), re.NOFLAG), "Gptq"),
            (re.compile(wb(r'gptq'), re.NOFLAG), "gptq"),
        ],
    },
    {
        "name": "AWQ (method)",
        "canonical": "AWQ",
        "variants": [
            (re.compile(wb(r'Awq'), re.NOFLAG), "Awq"),
            (re.compile(wb(r'awq'), re.NOFLAG), "awq"),
        ],
    },
    {
        "name": "GGUF (format)",
        "canonical": "GGUF",
        "variants": [
            (re.compile(wb(r'Gguf'), re.NOFLAG), "Gguf"),
            (re.compile(wb(r'gguf'), re.NOFLAG), "gguf"),
        ],
    },
    {
        "name": "BPE (method)",
        "canonical": "BPE",
        "variants": [
            (re.compile(wb(r'Bpe'), re.NOFLAG), "Bpe"),
            (re.compile(wb(r'bpe'), re.NOFLAG), "bpe"),
        ],
    },
    # ------------- LIBRARIES -------------
    {
        "name": "PyTorch (library)",
        "canonical": "PyTorch",
        "variants": [
            (re.compile(wb(r'Pytorch'), re.NOFLAG), "Pytorch"),
            (re.compile(wb(r'pytorch'), re.NOFLAG), "pytorch"),
            (re.compile(wb(r'PYTORCH'), re.NOFLAG), "PYTORCH"),
            (re.compile(wb(r'Py Torch'), re.NOFLAG), "Py Torch"),
        ],
    },
    {
        "name": "TensorFlow (library)",
        "canonical": "TensorFlow",
        "variants": [
            (re.compile(wb(r'Tensorflow'), re.NOFLAG), "Tensorflow"),
            (re.compile(wb(r'tensorflow'), re.NOFLAG), "tensorflow"),
            (re.compile(wb(r'TENSORFLOW'), re.NOFLAG), "TENSORFLOW"),
            (re.compile(wb(r'Tensor Flow'), re.NOFLAG), "Tensor Flow"),
            (re.compile(wb(r'tensor flow'), re.NOFLAG), "tensor flow"),
        ],
    },
    {
        "name": "LangChain (library)",
        "canonical": "LangChain",
        "variants": [
            (re.compile(wb(r'Langchain'), re.NOFLAG), "Langchain"),
            (re.compile(wb(r'langchain'), re.NOFLAG), "langchain"),
            (re.compile(wb(r'LANGCHAIN'), re.NOFLAG), "LANGCHAIN"),
            (re.compile(wb(r'Lang Chain'), re.NOFLAG), "Lang Chain"),
            (re.compile(wb(r'lang chain'), re.NOFLAG), "lang chain"),
        ],
    },
    {
        "name": "LlamaIndex (library)",
        "canonical": "LlamaIndex",
        "variants": [
            (re.compile(wb(r'Llamaindex'), re.NOFLAG), "Llamaindex"),
            (re.compile(wb(r'llamaindex'), re.NOFLAG), "llamaindex"),
            (re.compile(wb(r'Llama Index'), re.NOFLAG), "Llama Index"),
            (re.compile(wb(r'llama index'), re.NOFLAG), "llama index"),
        ],
    },
    {
        "name": "Hugging Face (vendor/library)",
        "canonical": "Hugging Face",
        "variants": [
            (re.compile(wb(r'HuggingFace'), re.NOFLAG), "HuggingFace (one word)"),
            (re.compile(wb(r'huggingface'), re.NOFLAG), "huggingface"),
            (re.compile(wb(r'Huggingface'), re.NOFLAG), "Huggingface"),
            (re.compile(wb(r'hugging face'), re.NOFLAG), "hugging face"),
            (re.compile(wb(r'HUGGING FACE'), re.NOFLAG), "HUGGING FACE"),
        ],
    },
    {
        "name": "vLLM (library)",
        "canonical": "vLLM",
        "variants": [
            (re.compile(wb(r'VLLM'), re.NOFLAG), "VLLM"),
            (re.compile(wb(r'Vllm'), re.NOFLAG), "Vllm"),
            (re.compile(wb(r'vllm'), re.NOFLAG), "vllm"),
        ],
    },
    {
        "name": "DeepSpeed (library)",
        "canonical": "DeepSpeed",
        "variants": [
            (re.compile(wb(r'Deepspeed'), re.NOFLAG), "Deepspeed"),
            (re.compile(wb(r'deepspeed'), re.NOFLAG), "deepspeed"),
            (re.compile(wb(r'DEEPSPEED'), re.NOFLAG), "DEEPSPEED"),
            (re.compile(wb(r'Deep Speed'), re.NOFLAG), "Deep Speed"),
            (re.compile(wb(r'deep speed'), re.NOFLAG), "deep speed"),
        ],
    },
    {
        "name": "FAISS (library)",
        "canonical": "FAISS",
        "variants": [
            (re.compile(wb(r'Faiss'), re.NOFLAG), "Faiss"),
            (re.compile(wb(r'faiss'), re.NOFLAG), "faiss"),
        ],
    },
    {
        "name": "NumPy (library)",
        "canonical": "NumPy",
        "variants": [
            (re.compile(wb(r'Numpy'), re.NOFLAG), "Numpy"),
            (re.compile(wb(r'numpy'), re.NOFLAG), "numpy"),
            (re.compile(wb(r'NUMPY'), re.NOFLAG), "NUMPY"),
        ],
    },
    {
        "name": "Pandas (library)",
        "canonical": "pandas",
        "variants": [
            # The library brands itself lowercase. Flag Pandas/PANDAS as inconsistent.
            (re.compile(wb(r'Pandas'), re.NOFLAG), "Pandas (canonical is lowercase 'pandas')"),
            (re.compile(wb(r'PANDAS'), re.NOFLAG), "PANDAS"),
        ],
    },
    {
        "name": "scikit-learn (library)",
        "canonical": "scikit-learn",
        "variants": [
            (re.compile(wb(r'Scikit-learn'), re.NOFLAG), "Scikit-learn"),
            (re.compile(wb(r'Scikit-Learn'), re.NOFLAG), "Scikit-Learn"),
            (re.compile(wb(r'sklearn'), re.NOFLAG), "sklearn (use 'scikit-learn' in prose)"),
            (re.compile(wb(r'SKLEARN'), re.NOFLAG), "SKLEARN"),
            (re.compile(wb(r'scikit learn'), re.NOFLAG), "scikit learn (use hyphen)"),
        ],
    },
    {
        "name": "spaCy (library)",
        "canonical": "spaCy",
        "variants": [
            (re.compile(wb(r'Spacy'), re.NOFLAG), "Spacy"),
            (re.compile(wb(r'spacy'), re.NOFLAG), "spacy"),
            (re.compile(wb(r'SPACY'), re.NOFLAG), "SPACY"),
        ],
    },
    {
        "name": "NLTK (library)",
        "canonical": "NLTK",
        "variants": [
            (re.compile(wb(r'Nltk'), re.NOFLAG), "Nltk"),
            (re.compile(wb(r'nltk'), re.NOFLAG), "nltk"),
        ],
    },
    {
        "name": "Pinecone (vendor/library)",
        "canonical": "Pinecone",
        "variants": [
            (re.compile(wb(r'pinecone'), re.NOFLAG), "pinecone"),
            (re.compile(wb(r'PINECONE'), re.NOFLAG), "PINECONE"),
        ],
    },
    {
        "name": "Weaviate (library)",
        "canonical": "Weaviate",
        "variants": [
            (re.compile(wb(r'weaviate'), re.NOFLAG), "weaviate"),
            (re.compile(wb(r'WEAVIATE'), re.NOFLAG), "WEAVIATE"),
        ],
    },
    {
        "name": "Qdrant (library)",
        "canonical": "Qdrant",
        "variants": [
            (re.compile(wb(r'qdrant'), re.NOFLAG), "qdrant"),
            (re.compile(wb(r'QDRANT'), re.NOFLAG), "QDRANT"),
        ],
    },
    {
        "name": "Milvus (library)",
        "canonical": "Milvus",
        "variants": [
            (re.compile(wb(r'milvus'), re.NOFLAG), "milvus"),
            (re.compile(wb(r'MILVUS'), re.NOFLAG), "MILVUS"),
        ],
    },
    {
        "name": "Elasticsearch (library)",
        "canonical": "Elasticsearch",
        "variants": [
            (re.compile(wb(r'ElasticSearch'), re.NOFLAG), "ElasticSearch (two-word)"),
            (re.compile(wb(r'elastic search'), re.NOFLAG), "elastic search"),
            (re.compile(wb(r'Elastic Search'), re.NOFLAG), "Elastic Search"),
            (re.compile(wb(r'elasticsearch'), re.NOFLAG), "elasticsearch (in prose, use 'Elasticsearch')"),
            (re.compile(wb(r'ELASTICSEARCH'), re.NOFLAG), "ELASTICSEARCH"),
        ],
    },
    {
        "name": "Triton (library)",
        "canonical": "Triton",
        "variants": [
            (re.compile(wb(r'triton'), re.NOFLAG), "triton"),
            (re.compile(wb(r'TRITON'), re.NOFLAG), "TRITON"),
        ],
    },
    {
        "name": "ONNX (library)",
        "canonical": "ONNX",
        "variants": [
            (re.compile(wb(r'Onnx'), re.NOFLAG), "Onnx"),
            (re.compile(wb(r'onnx'), re.NOFLAG), "onnx"),
        ],
    },
    {
        "name": "JAX (library)",
        "canonical": "JAX",
        "variants": [
            (re.compile(wb(r'Jax'), re.NOFLAG), "Jax"),
            # not flagging 'jax' lowercase since it can appear in code module names
        ],
    },
    {
        "name": "Docker (platform)",
        "canonical": "Docker",
        "variants": [
            (re.compile(wb(r'docker'), re.NOFLAG), "docker (in prose)"),
            (re.compile(wb(r'DOCKER'), re.NOFLAG), "DOCKER"),
        ],
    },
    {
        "name": "Kubernetes (platform)",
        "canonical": "Kubernetes",
        "variants": [
            (re.compile(wb(r'kubernetes'), re.NOFLAG), "kubernetes (in prose)"),
            (re.compile(wb(r'KUBERNETES'), re.NOFLAG), "KUBERNETES"),
        ],
    },
    # ------------- VENDORS / PLATFORMS -------------
    {
        "name": "OpenAI (vendor)",
        "canonical": "OpenAI",
        "variants": [
            (re.compile(wb(r'Open AI'), re.NOFLAG), "Open AI (two words)"),
            (re.compile(wb(r'open ai'), re.NOFLAG), "open ai"),
            (re.compile(wb(r'OPENAI'), re.NOFLAG), "OPENAI"),
            (re.compile(wb(r'Openai'), re.NOFLAG), "Openai"),
            # not flagging 'openai' lowercase since it is the package name; we strip
            # <code> already, so any 'openai' remaining is likely prose
            (re.compile(wb(r'openai'), re.NOFLAG), "openai (in prose, use 'OpenAI')"),
        ],
    },
    {
        "name": "Anthropic (vendor)",
        "canonical": "Anthropic",
        "variants": [
            (re.compile(wb(r'ANTHROPIC'), re.NOFLAG), "ANTHROPIC"),
            (re.compile(wb(r'anthropic'), re.NOFLAG), "anthropic (in prose, use 'Anthropic')"),
        ],
    },
    {
        "name": "Google DeepMind (vendor)",
        "canonical": "Google DeepMind",
        "variants": [
            (re.compile(wb(r'Google Deepmind'), re.NOFLAG), "Google Deepmind"),
            (re.compile(wb(r'google deepmind'), re.NOFLAG), "google deepmind"),
            (re.compile(wb(r'DeepMind Google'), re.NOFLAG), "DeepMind Google (order)"),
        ],
    },
    {
        "name": "DeepMind (vendor)",
        "canonical": "DeepMind",
        "variants": [
            (re.compile(wb(r'Deepmind'), re.NOFLAG), "Deepmind"),
            (re.compile(wb(r'deepmind'), re.NOFLAG), "deepmind"),
            (re.compile(wb(r'DEEPMIND'), re.NOFLAG), "DEEPMIND"),
            (re.compile(wb(r'Deep Mind'), re.NOFLAG), "Deep Mind"),
        ],
    },
    {
        "name": "Mistral AI (vendor)",
        "canonical": "Mistral AI",
        "variants": [
            (re.compile(wb(r'Mistral\.ai'), re.NOFLAG), "Mistral.ai"),
            (re.compile(wb(r'mistral ai'), re.NOFLAG), "mistral ai"),
        ],
    },
    {
        "name": "Databricks (vendor)",
        "canonical": "Databricks",
        "variants": [
            (re.compile(wb(r'databricks'), re.NOFLAG), "databricks"),
            (re.compile(wb(r'DataBricks'), re.NOFLAG), "DataBricks"),
            (re.compile(wb(r'DATABRICKS'), re.NOFLAG), "DATABRICKS"),
        ],
    },
    {
        "name": "Snowflake (vendor)",
        "canonical": "Snowflake",
        "variants": [
            (re.compile(wb(r'snowflake'), re.NOFLAG), "snowflake"),
            (re.compile(wb(r'SNOWFLAKE'), re.NOFLAG), "SNOWFLAKE"),
        ],
    },
    {
        "name": "Vertex AI (platform)",
        "canonical": "Vertex AI",
        "variants": [
            (re.compile(wb(r'VertexAI'), re.NOFLAG), "VertexAI (one word)"),
            (re.compile(wb(r'vertex ai'), re.NOFLAG), "vertex ai"),
            (re.compile(wb(r'vertex AI'), re.NOFLAG), "vertex AI"),
        ],
    },
    {
        "name": "SageMaker (platform)",
        "canonical": "SageMaker",
        "variants": [
            (re.compile(wb(r'Sagemaker'), re.NOFLAG), "Sagemaker"),
            (re.compile(wb(r'sagemaker'), re.NOFLAG), "sagemaker"),
            (re.compile(wb(r'Sage Maker'), re.NOFLAG), "Sage Maker"),
            (re.compile(wb(r'SAGEMAKER'), re.NOFLAG), "SAGEMAKER"),
        ],
    },
    {
        "name": "Bedrock (platform)",
        "canonical": "Bedrock",
        "variants": [
            (re.compile(wb(r'BEDROCK'), re.NOFLAG), "BEDROCK"),
            # not flagging 'bedrock' lowercase since it is a common English word
        ],
    },
    {
        "name": "Azure OpenAI (platform)",
        "canonical": "Azure OpenAI",
        "variants": [
            (re.compile(wb(r'Azure Open AI'), re.NOFLAG), "Azure Open AI"),
            (re.compile(wb(r'azure openai'), re.NOFLAG), "azure openai"),
            (re.compile(wb(r'AzureOpenAI'), re.NOFLAG), "AzureOpenAI (one word)"),
        ],
    },
    # ------------- ACRONYMS / CONCEPTS -------------
    {
        "name": "KV cache (concept)",
        "canonical": "KV cache",
        "variants": [
            (re.compile(wb(r'KV-cache'), re.NOFLAG), "KV-cache (use space)"),
            (re.compile(wb(r'kv-cache'), re.NOFLAG), "kv-cache"),
            (re.compile(wb(r'kv cache'), re.NOFLAG), "kv cache"),
            (re.compile(wb(r'Kv cache'), re.NOFLAG), "Kv cache"),
            (re.compile(wb(r'Kv-cache'), re.NOFLAG), "Kv-cache"),
            (re.compile(wb(r'kvcache'), re.NOFLAG), "kvcache"),
            (re.compile(wb(r'KVcache'), re.NOFLAG), "KVcache"),
            (re.compile(wb(r'KV Cache'), re.NOFLAG), "KV Cache (lower 'cache')"),
        ],
    },
    {
        "name": "Self-attention (concept)",
        "canonical": "self-attention",
        "variants": [
            (re.compile(wb(r'Self Attention'), re.NOFLAG), "Self Attention"),
            (re.compile(wb(r'self attention'), re.NOFLAG), "self attention"),
            (re.compile(wb(r'SELF-ATTENTION'), re.NOFLAG), "SELF-ATTENTION"),
            (re.compile(wb(r'selfattention'), re.NOFLAG), "selfattention"),
            # NOTE: "Self-attention" (capitalized at sentence-start) is OK; we
            # only flag truly inconsistent forms.
        ],
    },
    {
        "name": "Multi-head attention (concept)",
        "canonical": "multi-head attention",
        "variants": [
            (re.compile(wb(r'Multi Head Attention'), re.NOFLAG), "Multi Head Attention"),
            (re.compile(wb(r'multi head attention'), re.NOFLAG), "multi head attention"),
            (re.compile(wb(r'Multihead attention'), re.NOFLAG), "Multihead attention"),
            (re.compile(wb(r'multihead attention'), re.NOFLAG), "multihead attention"),
        ],
    },
    {
        "name": "Cross-attention (concept)",
        "canonical": "cross-attention",
        "variants": [
            (re.compile(wb(r'Cross Attention'), re.NOFLAG), "Cross Attention"),
            (re.compile(wb(r'cross attention'), re.NOFLAG), "cross attention"),
            (re.compile(wb(r'Crossattention'), re.NOFLAG), "Crossattention"),
            (re.compile(wb(r'crossattention'), re.NOFLAG), "crossattention"),
        ],
    },
    {
        "name": "Fine-tuning (concept)",
        "canonical": "fine-tuning",
        "variants": [
            (re.compile(wb(r'finetuning'), re.NOFLAG), "finetuning"),
            (re.compile(wb(r'Finetuning'), re.NOFLAG), "Finetuning"),
            (re.compile(wb(r'fine tuning'), re.NOFLAG), "fine tuning"),
            (re.compile(wb(r'Fine tuning'), re.NOFLAG), "Fine tuning"),
            (re.compile(wb(r'FINE-TUNING'), re.NOFLAG), "FINE-TUNING"),
        ],
    },
    {
        "name": "Pre-training (concept)",
        "canonical": "pre-training",
        "variants": [
            (re.compile(wb(r'pretraining'), re.NOFLAG), "pretraining"),
            (re.compile(wb(r'Pretraining'), re.NOFLAG), "Pretraining"),
            (re.compile(wb(r'pre training'), re.NOFLAG), "pre training"),
            (re.compile(wb(r'Pre training'), re.NOFLAG), "Pre training"),
        ],
    },
    {
        "name": "Instruction tuning (concept)",
        "canonical": "instruction tuning",
        "variants": [
            (re.compile(wb(r'instruction-tuning'), re.NOFLAG), "instruction-tuning"),
            (re.compile(wb(r'Instruction-tuning'), re.NOFLAG), "Instruction-tuning"),
            (re.compile(wb(r'instructiontuning'), re.NOFLAG), "instructiontuning"),
        ],
    },
    {
        "name": "Tokenizer (concept)",
        "canonical": "tokenizer",
        "variants": [
            (re.compile(wb(r'Tokeniser'), re.NOFLAG), "Tokeniser (British spelling)"),
            (re.compile(wb(r'tokeniser'), re.NOFLAG), "tokeniser"),
        ],
    },
    {
        "name": "Tokenization (concept)",
        "canonical": "tokenization",
        "variants": [
            (re.compile(wb(r'Tokenisation'), re.NOFLAG), "Tokenisation (British spelling)"),
            (re.compile(wb(r'tokenisation'), re.NOFLAG), "tokenisation"),
        ],
    },
    {
        "name": "Context window (concept)",
        "canonical": "context window",
        "variants": [
            (re.compile(wb(r'context-window'), re.NOFLAG), "context-window (use space)"),
            (re.compile(wb(r'Context-Window'), re.NOFLAG), "Context-Window"),
            (re.compile(wb(r'Context Window'), re.NOFLAG), "Context Window (title case in prose)"),
        ],
    },
    {
        "name": "Context length (concept)",
        "canonical": "context length",
        "variants": [
            (re.compile(wb(r'context-length'), re.NOFLAG), "context-length"),
            (re.compile(wb(r'Context-Length'), re.NOFLAG), "Context-Length"),
        ],
    },
    {
        "name": "Hallucination (concept)",
        "canonical": "hallucination",
        "variants": [
            (re.compile(wb(r'Hallucinations'), re.NOFLAG), "Hallucinations (mid-sentence)"),
            # The plural form 'hallucinations' is fine; we only flag inconsistent casing
            (re.compile(wb(r'HALLUCINATION'), re.NOFLAG), "HALLUCINATION"),
        ],
    },
    # ------------- BENCHMARKS -------------
    {
        "name": "MMLU (benchmark)",
        "canonical": "MMLU",
        "variants": [
            (re.compile(wb(r'mmlu'), re.NOFLAG), "mmlu"),
            (re.compile(wb(r'Mmlu'), re.NOFLAG), "Mmlu"),
        ],
    },
    {
        "name": "HellaSwag (benchmark)",
        "canonical": "HellaSwag",
        "variants": [
            (re.compile(wb(r'Hellaswag'), re.NOFLAG), "Hellaswag"),
            (re.compile(wb(r'hellaswag'), re.NOFLAG), "hellaswag"),
            (re.compile(wb(r'HELLASWAG'), re.NOFLAG), "HELLASWAG"),
            (re.compile(wb(r'Hella Swag'), re.NOFLAG), "Hella Swag"),
        ],
    },
    {
        "name": "GSM8K (benchmark)",
        "canonical": "GSM8K",
        "variants": [
            (re.compile(wb(r'gsm8k'), re.NOFLAG), "gsm8k"),
            (re.compile(wb(r'Gsm8k'), re.NOFLAG), "Gsm8k"),
            (re.compile(wb(r'GSM-8K'), re.NOFLAG), "GSM-8K"),
        ],
    },
    {
        "name": "HumanEval (benchmark)",
        "canonical": "HumanEval",
        "variants": [
            (re.compile(wb(r'Humaneval'), re.NOFLAG), "Humaneval"),
            (re.compile(wb(r'humaneval'), re.NOFLAG), "humaneval"),
            (re.compile(wb(r'Human Eval'), re.NOFLAG), "Human Eval (two words)"),
            (re.compile(wb(r'human eval'), re.NOFLAG), "human eval"),
        ],
    },
    {
        "name": "TruthfulQA (benchmark)",
        "canonical": "TruthfulQA",
        "variants": [
            (re.compile(wb(r'Truthfulqa'), re.NOFLAG), "Truthfulqa"),
            (re.compile(wb(r'truthfulqa'), re.NOFLAG), "truthfulqa"),
            (re.compile(wb(r'Truthful QA'), re.NOFLAG), "Truthful QA"),
        ],
    },
    {
        "name": "BIG-bench (benchmark)",
        "canonical": "BIG-bench",
        "variants": [
            (re.compile(wb(r'BigBench'), re.NOFLAG), "BigBench"),
            (re.compile(wb(r'big-bench'), re.NOFLAG), "big-bench"),
            (re.compile(wb(r'Big-bench'), re.NOFLAG), "Big-bench"),
            (re.compile(wb(r'big bench'), re.NOFLAG), "big bench"),
        ],
    },
    {
        "name": "SuperGLUE (benchmark)",
        "canonical": "SuperGLUE",
        "variants": [
            (re.compile(wb(r'Superglue'), re.NOFLAG), "Superglue"),
            (re.compile(wb(r'SuperGlue'), re.NOFLAG), "SuperGlue"),
            (re.compile(wb(r'superglue'), re.NOFLAG), "superglue"),
            (re.compile(wb(r'Super GLUE'), re.NOFLAG), "Super GLUE"),
        ],
    },
    # ------------- PAPER TITLES -------------
    {
        "name": "\"Attention Is All You Need\" (paper title)",
        "canonical": "Attention Is All You Need",
        "variants": [
            (re.compile(wb(r'Attention is All You Need'), re.NOFLAG), "Attention is All You Need (lower 'is')"),
            (re.compile(wb(r'Attention Is all You Need'), re.NOFLAG), "Attention Is all You Need"),
            (re.compile(wb(r'attention is all you need'), re.NOFLAG), "attention is all you need"),
            (re.compile(wb(r'Attention is all you need'), re.NOFLAG), "Attention is all you need"),
            (re.compile(wb(r'Attention Is All you Need'), re.NOFLAG), "Attention Is All you Need"),
        ],
    },
    {
        "name": "Transformer (architecture)",
        "canonical": "Transformer",
        "variants": [
            # In titles and proper architecture names, capitalize Transformer.
            # We flag obvious all-lower or all-upper variants; we cannot easily
            # disambiguate "transformer" generic in code.
            (re.compile(wb(r'TRANSFORMER'), re.NOFLAG), "TRANSFORMER"),
        ],
    },
    {
        "name": "OWASP Top 10 (standard)",
        "canonical": "OWASP Top 10",
        "variants": [
            (re.compile(wb(r'OWASP top 10'), re.NOFLAG), "OWASP top 10"),
            (re.compile(wb(r'OWASP Top-10'), re.NOFLAG), "OWASP Top-10"),
            (re.compile(wb(r'OWASP top-10'), re.NOFLAG), "OWASP top-10"),
            (re.compile(wb(r'OWASP TOP 10'), re.NOFLAG), "OWASP TOP 10"),
            (re.compile(wb(r'OWASP TOP-10'), re.NOFLAG), "OWASP TOP-10"),
        ],
    },
    {
        "name": "EU AI Act (regulation)",
        "canonical": "EU AI Act",
        "variants": [
            (re.compile(wb(r'EU AI act'), re.NOFLAG), "EU AI act"),
            (re.compile(wb(r'EU Ai Act'), re.NOFLAG), "EU Ai Act"),
            (re.compile(wb(r'eu ai act'), re.NOFLAG), "eu ai act"),
            (re.compile(wb(r'European AI Act'), re.NOFLAG), "European AI Act (use 'EU AI Act')"),
        ],
    },
    {
        "name": "NIST AI RMF (framework)",
        "canonical": "NIST AI RMF",
        "variants": [
            (re.compile(wb(r'NIST AI Rmf'), re.NOFLAG), "NIST AI Rmf"),
            (re.compile(wb(r'NIST AI rmf'), re.NOFLAG), "NIST AI rmf"),
            (re.compile(wb(r'NIST RMF'), re.NOFLAG), "NIST RMF (missing 'AI')"),
        ],
    },
    {
        "name": "SOC 2 (certification)",
        "canonical": "SOC 2",
        "variants": [
            (re.compile(wb(r'SOC2'), re.NOFLAG), "SOC2 (no space)"),
            (re.compile(wb(r'Soc 2'), re.NOFLAG), "Soc 2"),
            (re.compile(wb(r'soc 2'), re.NOFLAG), "soc 2"),
            (re.compile(wb(r'SOC-2'), re.NOFLAG), "SOC-2"),
        ],
    },
    {
        "name": "HIPAA (regulation)",
        "canonical": "HIPAA",
        "variants": [
            (re.compile(wb(r'Hipaa'), re.NOFLAG), "Hipaa"),
            (re.compile(wb(r'hipaa'), re.NOFLAG), "hipaa"),
            (re.compile(wb(r'HIPPA'), re.NOFLAG), "HIPPA (misspelling)"),
        ],
    },
    {
        "name": "GDPR (regulation)",
        "canonical": "GDPR",
        "variants": [
            (re.compile(wb(r'Gdpr'), re.NOFLAG), "Gdpr"),
            (re.compile(wb(r'gdpr'), re.NOFLAG), "gdpr"),
        ],
    },
    {
        "name": "OpenTelemetry (standard)",
        "canonical": "OpenTelemetry",
        "variants": [
            (re.compile(wb(r'Opentelemetry'), re.NOFLAG), "Opentelemetry"),
            (re.compile(wb(r'opentelemetry'), re.NOFLAG), "opentelemetry"),
            (re.compile(wb(r'Open Telemetry'), re.NOFLAG), "Open Telemetry (two words)"),
            (re.compile(wb(r'open telemetry'), re.NOFLAG), "open telemetry"),
            (re.compile(wb(r'OTEL'), re.NOFLAG), "OTEL (use 'OTel')"),
            (re.compile(wb(r'Otel'), re.NOFLAG), "Otel"),
        ],
    },
]


# =================================================================
# Scan
# =================================================================
def gather_sections() -> list[Path]:
    paths: list[Path] = []
    for p in ROOT.rglob("*.html"):
        if set(p.parts) & SKIP_DIRS:
            continue
        if not (p.name.startswith("section-") or p.name == "index.html"):
            continue
        paths.append(p)
    return sorted(paths)


def scan_file(path: Path) -> dict[str, dict]:
    """Return: { group_name: {variant_label: count, ...} } for non-canonical hits."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    prose = strip_to_prose(raw)
    out: dict[str, dict] = {}
    for grp in GROUPS:
        hits: Counter = Counter()
        for rx, label in grp["variants"]:
            n = len(rx.findall(prose))
            if n > 0:
                hits[label] += n
        if hits:
            out[grp["name"]] = dict(hits)
    return out


def main():
    paths = gather_sections()
    print(f"Scanning {len(paths)} section files...", file=sys.stderr)

    # group_name -> { path_str: { variant: count, ... } }
    by_group: dict[str, dict[str, dict]] = defaultdict(dict)
    # group_name -> total non-canonical hits
    totals: Counter = Counter()
    # group_name -> per-variant totals
    variant_totals: dict[str, Counter] = defaultdict(Counter)

    for p in paths:
        hits = scan_file(p)
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        for gname, variants in hits.items():
            by_group[gname][rel] = variants
            for v, n in variants.items():
                totals[gname] += n
                variant_totals[gname][v] += n

    # Build a canonical-spelling map
    canonical = {grp["name"]: grp["canonical"] for grp in GROUPS}

    # Sort groups by total hits descending
    sorted_groups = sorted(by_group.items(), key=lambda kv: -totals[kv[0]])

    # Emit report
    out_lines: list[str] = []
    out_lines.append("# Terminology Inconsistencies Audit (Wave 36, REPORT-ONLY)")
    out_lines.append("")
    out_lines.append(
        "Scan of all section HTML files for entity-name inconsistencies. "
        "Occurrences inside `<code>`, `<pre>`, code blocks, and bibliography "
        "lists are excluded (those are package names or intentional author casing)."
    )
    out_lines.append("")
    out_lines.append(f"- Section files scanned: **{len(paths)}**")
    out_lines.append(f"- Canonical-term groups with at least one inconsistency: **{len(by_group)}**")
    out_lines.append(f"- Total inconsistent occurrences book-wide: **{sum(totals.values())}**")
    out_lines.append("")
    out_lines.append("## Top inconsistency clusters (ranked by total non-canonical hits)")
    out_lines.append("")
    out_lines.append("| Rank | Canonical term | Non-canonical hits | Sections affected |")
    out_lines.append("|---:|---|---:|---:|")
    for rank, (gname, files) in enumerate(sorted_groups[:30], start=1):
        out_lines.append(
            f"| {rank} | `{canonical[gname]}` ({gname}) | {totals[gname]} | {len(files)} |"
        )
    out_lines.append("")
    out_lines.append("---")
    out_lines.append("")
    out_lines.append("## Per-term detail")
    out_lines.append("")

    for gname, files in sorted_groups:
        out_lines.append(f"### {gname}")
        out_lines.append("")
        out_lines.append(f"- **Recommended canonical spelling**: `{canonical[gname]}`")
        out_lines.append(f"- **Total non-canonical occurrences**: {totals[gname]}")
        out_lines.append(f"- **Sections affected**: {len(files)}")
        out_lines.append("- **Non-canonical variants observed:**")
        for v, n in variant_totals[gname].most_common():
            out_lines.append(f"  - `{v}`: {n} occurrence(s)")
        out_lines.append("")
        # top 10 offending files (by sum of variant counts)
        ranked_files = sorted(
            files.items(),
            key=lambda kv: -sum(kv[1].values()),
        )[:10]
        out_lines.append("- **Top offending files (up to 10):**")
        for fpath, variants in ranked_files:
            n = sum(variants.values())
            vs = ", ".join(f"{v}={c}" for v, c in sorted(variants.items(), key=lambda kv: -kv[1]))
            out_lines.append(f"  - `{fpath}`: {n} hit(s); {vs}")
        out_lines.append("")

    out_path = ROOT / "docs" / "content-audit" / "TERMINOLOGY_INCONSISTENCIES.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out_lines), encoding="utf-8")

    # Print short stdout summary
    print(f"Report: {out_path.relative_to(ROOT)}")
    print(f"Sections scanned: {len(paths)}")
    print(f"Inconsistency clusters: {len(by_group)}")
    print(f"Total inconsistent hits: {sum(totals.values())}")
    print("\nTop 15 clusters:")
    for rank, (gname, _files) in enumerate(sorted_groups[:15], start=1):
        print(f"  {rank:>2}. {totals[gname]:>5} hits  --  canonical: {canonical[gname]:<25}  ({gname})")


if __name__ == "__main__":
    main()
