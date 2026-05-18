"""Named-entity-based duplicate-content detector for the book.

The idea
--------
Each section of the book talks about a recurring set of named entities:
libraries (PyTorch, vLLM, langchain), models (GPT-4, Claude 4.7,
Llama-3, Mixtral), methods (LoRA, RLHF, DPO, YaRN), platforms
(MLflow, HuggingFace Hub, Databricks, Vertex AI), benchmarks (MMLU,
HellaSwag, RULER, NIAH), and key concepts (KV cache, attention,
lost-in-the-middle, position bias). When two sections introduce or
extensively cover the SAME entities, they are probably duplicating
content.

This script:
  1. Builds a per-section index of named entities using a curated
     dictionary plus pattern matching (capitalized multi-word terms,
     python imports, inline <code>).
  2. Computes cross-section overlap using Jaccard similarity on the
     entity sets.
  3. Detects "multiple introduction" entities: those that appear
     inside a <strong>...</strong> bold-defining context in more than
     one section.
  4. Hashes 60-word sliding windows of visible prose and flags
     verbatim duplicates across sections (catches accidental
     copy-paste).
  5. Reports the top hot-entities (mentioned in many sections; the
     authors should pick ONE canonical home for each).

Usage
-----
    /c/Python314/python scripts/dedup_detector.py
    /c/Python314/python scripts/dedup_detector.py --chapter 42
    /c/Python314/python scripts/dedup_detector.py --top 30
    /c/Python314/python scripts/dedup_detector.py --jaccard-threshold 0.4

Outputs JSON to stdout and a human-readable markdown report to
`docs/content-audit/DEDUP_REPORT.md`.
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_mod
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts"}

# =================================================================
# Curated entity dictionary. Casing reflects how the book mentions
# each term. Used as case-INSENSITIVE matches with word-boundary regex.
# Entities are grouped only for documentation; matching is flat.
# =================================================================
ENTITY_DICT = {
    "models": [
        "GPT-4", "GPT-4o", "GPT-4o-mini", "GPT-5", "GPT-3.5", "GPT-2",
        "Claude 3", "Claude 3.5 Sonnet", "Claude 4.7", "Claude Opus",
        "Claude Sonnet", "Claude Haiku", "Claude Sonnet 4.7", "Claude Opus 4",
        "Llama-3", "Llama 3", "Llama-2", "Llama 3.1", "Llama 3.2", "Llama 3.3",
        "Llama Guard", "Llama-3-8B",
        "Mistral", "Mixtral", "Mixtral-8x7B", "Mistral-7B",
        "Gemini", "Gemini 1.5", "Gemini 2.0", "Gemini 2.5", "Gemini Pro",
        "Gemma", "Gemma 2", "PaLM", "PaLM-2",
        "Qwen", "Qwen-2", "Qwen-2.5", "DeepSeek", "DeepSeek-V3", "DeepSeek-R1",
        "Phi-3", "Phi-2", "MobileLLM",
        "BERT", "RoBERTa", "T5", "BART", "ELECTRA",
        "Stable Diffusion", "DALL-E", "Midjourney",
        "Mamba", "Mamba-2", "RWKV", "Hyena", "S4",
    ],
    "libraries": [
        "PyTorch", "TensorFlow", "JAX", "Flax", "Keras",
        "transformers", "Hugging Face", "huggingface_hub", "datasets",
        "sentence-transformers", "tokenizers", "accelerate", "peft",
        "trl", "bitsandbytes", "vLLM", "TGI", "SGLang", "TensorRT-LLM",
        "DeepSpeed", "FSDP", "Megatron-LM", "ColossalAI",
        "langchain", "LlamaIndex", "DSPy", "Haystack", "guidance",
        "instructor", "outlines", "marvin",
        "OpenAI Python", "anthropic SDK", "openai", "anthropic",
        "gensim", "spaCy", "NLTK", "scikit-learn", "numpy", "pandas",
        "matplotlib", "seaborn", "plotly",
        "FAISS", "Pinecone", "Weaviate", "Qdrant", "ChromaDB", "Milvus",
        "pgvector", "Vespa", "Elasticsearch", "OpenSearch",
        "Triton", "ONNX", "ONNX Runtime", "OpenVINO",
        "Ray", "Dask", "PySpark", "Delta Lake", "Iceberg",
        "Playwright", "BeautifulSoup", "Selenium",
        "Docker", "Kubernetes", "Helm",
        "Apache Kafka", "Redis", "PostgreSQL",
        "promptfoo", "Inspect AI", "lm-eval-harness", "BIG-bench",
        "Ragas", "DeepEval", "Phoenix", "TruLens", "Giskard",
    ],
    "methods": [
        "LoRA", "QLoRA", "DoRA", "RoSA", "AdaLoRA", "VeRA",
        "RLHF", "DPO", "IPO", "KTO", "ORPO", "SimPO", "GRPO", "PPO", "REINFORCE",
        "RLAIF", "Constitutional AI",
        "YaRN", "NTK-aware", "RoPE", "ALiBi", "position interpolation",
        "FlashAttention", "FlashAttention-2", "FlashAttention-3",
        "PagedAttention", "Continuous batching", "speculative decoding",
        "Medusa", "EAGLE", "EAGLE-2",
        "Mixture-of-Experts", "MoE", "Switch Transformer", "GLaM",
        "Chain-of-Thought", "CoT", "Tree-of-Thoughts", "ToT",
        "Self-Consistency", "Self-Refine", "Reflexion",
        "ReAct", "RAG", "Self-RAG", "GraphRAG", "HyDE", "RAGAS",
        "BM25", "TF-IDF", "RRF", "Reciprocal Rank Fusion",
        "knowledge distillation", "pruning", "quantization",
        "GPTQ", "AWQ", "GGUF", "INT8", "FP16", "BF16", "FP8",
        "BLEU", "ROUGE", "BERTScore", "METEOR",
        "perplexity", "bits-per-byte", "BPB",
        "Needle-in-a-Haystack", "NIAH", "RULER",
        "byte-pair encoding", "BPE", "WordPiece", "SentencePiece",
        "Constitutional AI", "Direct Preference Optimization",
        "lost-in-the-middle",
    ],
    "platforms": [
        "MLflow", "Weights & Biases", "W&B", "Comet", "Neptune", "ClearML",
        "Langfuse", "LangSmith", "Helicone", "Phoenix",
        "Hugging Face Hub", "HuggingFace Hub", "HF Hub",
        "Databricks", "Snowflake", "Vertex AI", "SageMaker", "Bedrock",
        "Azure OpenAI", "Google Cloud", "AWS",
        "OpenAI", "Anthropic", "Google DeepMind", "Mistral AI", "Cohere",
        "Together AI", "Replicate", "Modal", "Fireworks", "Anyscale",
        "Groq", "Cerebras", "SambaNova",
        "vLLM Serve", "TGI", "Ollama", "LM Studio", "llama.cpp",
        "OpenTelemetry", "OTel", "Jaeger", "Grafana", "Prometheus",
        "Datadog", "Honeycomb", "New Relic", "Splunk",
        "FedRAMP", "SOC 2", "HIPAA", "GDPR", "EU AI Act", "NIST AI RMF",
    ],
    "benchmarks": [
        "MMLU", "MMLU-Pro", "HellaSwag", "ARC", "GSM8K", "MATH",
        "HumanEval", "MBPP", "BigCodeBench", "SWE-bench", "LiveCodeBench",
        "MT-Bench", "Chatbot Arena", "AlpacaEval", "Arena-Hard",
        "LongBench", "LongBench v2", "RULER", "NIAH",
        "HELM", "BIG-bench", "BigBench", "SuperGLUE", "GLUE",
        "TruthfulQA", "ToxicChat", "ToxiGen", "BBQ",
        "LegalBench", "FinanceBench", "MedQA", "Med-PaLM",
        "WikiText", "C4", "The Pile", "RedPajama", "Common Crawl",
        "TriviaQA", "NaturalQuestions", "SQuAD",
    ],
    "concepts": [
        "attention", "self-attention", "multi-head attention", "cross-attention",
        "KV cache", "kv-cache",
        "embedding", "embeddings", "vector database", "semantic search",
        "tokenization", "tokenizer",
        "context window", "context length",
        "fine-tuning", "instruction tuning", "alignment",
        "prompt injection", "jailbreak", "guardrail",
        "hallucination", "groundedness", "factuality",
        "Pareto frontier", "scaling laws", "chinchilla",
        "covariate shift", "distribution shift", "drift",
        "position bias", "verbosity bias", "self-enhancement",
        "Goodhart's Law",
        "OWASP", "OWASP Top 10",
        "GenAI Semantic Conventions",
    ],
}

ALL_ENTITIES: list[str] = sorted(
    {e for group in ENTITY_DICT.values() for e in group},
    key=lambda x: -len(x),  # longer first so multi-word matches win
)

# Build one big regex: word-boundaries, case-insensitive
def _build_entity_regex(entities: list[str]) -> re.Pattern:
    # Escape, then sort by length descending so longer matches win
    parts = [re.escape(e) for e in entities]
    pat = r'(?<![\w-])(?:' + '|'.join(parts) + r')(?![\w-])'
    return re.compile(pat, re.IGNORECASE)


ENTITY_RE = _build_entity_regex(ALL_ENTITIES)

# Canonicalize: lowercase, collapse hyphens/spaces
def _canon(e: str) -> str:
    return re.sub(r'[\s-]+', ' ', e.lower()).strip()


CANON_TO_DISPLAY: dict[str, str] = {}
for e in ALL_ENTITIES:
    CANON_TO_DISPLAY.setdefault(_canon(e), e)


# =================================================================
# HTML cleaning
# =================================================================
SCRIPT_STYLE_RE = re.compile(r'<(script|style)[^>]*>.*?</\1>', re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')
WS_RE = re.compile(r'\s+')
CODE_BLOCK_RE = re.compile(
    r'<div\s+class="code-block-wrapper"[^>]*>.*?</div>\s*(?:<div\s+class="code-output"[^>]*>.*?</div>\s*)?',
    re.DOTALL | re.IGNORECASE,
)
STRONG_RE = re.compile(r'<strong[^>]*>([^<]{2,80})</strong>', re.IGNORECASE)
HEADER_FOOTER_RE = re.compile(
    r'<(header|footer|nav)[^>]*>.*?</\1>', re.DOTALL | re.IGNORECASE,
)


def extract_visible_text(html: str) -> str:
    """Return visible prose (drop scripts, styles, code blocks, nav)."""
    s = SCRIPT_STYLE_RE.sub(' ', html)
    s = HEADER_FOOTER_RE.sub(' ', s)
    s = CODE_BLOCK_RE.sub(' ', s)  # drop code so library imports don't pollute prose hashes
    s = TAG_RE.sub(' ', s)
    s = html_mod.unescape(s)
    s = WS_RE.sub(' ', s).strip()
    return s


# =================================================================
# Per-section extraction
# =================================================================
def section_id(path: Path) -> str:
    """Return a stable short id like 'P9.M42.S42.8' or 'P14.M71.idx'."""
    parts = path.relative_to(ROOT).parts
    # parts like part-9-..., module-42-..., section-42.8.html
    part_m = re.match(r'part-(\d+)', parts[0]) if parts else None
    mod_m = re.match(r'module-(\d+\w*)', parts[1]) if len(parts) > 1 else None
    sec_m = re.match(r'section-([\d.]+\w*)\.html', parts[-1])
    if part_m and mod_m and sec_m:
        return f"S{sec_m.group(1)}"
    if part_m and mod_m and parts[-1] == "index.html":
        return f"M{mod_m.group(1)}.idx"
    return parts[-1]


def extract_entities(text: str) -> Counter:
    """Return Counter of entity occurrences in visible text."""
    counts: Counter = Counter()
    for m in ENTITY_RE.finditer(text):
        canon = _canon(m.group(0))
        counts[canon] += 1
    return counts


def extract_strong_terms(html: str) -> set[str]:
    """Return strong-bolded multi-char terms (likely definitional intros)."""
    terms: set[str] = set()
    for m in STRONG_RE.finditer(html):
        t = TAG_RE.sub('', m.group(1)).strip()
        if not t:
            continue
        if len(t) < 3 or len(t) > 60:
            continue
        # Skip common phrases that aren't entities
        if t.lower() in {"who", "what", "when", "where", "why", "how",
                          "situation", "problem", "dilemma", "decision",
                          "how:", "result", "lesson", "watch for", "result:",
                          "key insight", "key takeaway", "tip", "note", "warning",
                          "real-world scenario", "fix", "fix:", "lesson:",
                          "production pattern"}:
            continue
        terms.add(t)
    return terms


def sliding_hashes(text: str, window: int = 60) -> set[str]:
    """SHA1 hashes of word-windows. Detects verbatim duplicates."""
    words = text.split()
    out: set[str] = set()
    for i in range(0, len(words) - window + 1, max(1, window // 4)):
        chunk = ' '.join(words[i:i + window])
        h = hashlib.sha1(chunk.encode('utf-8')).hexdigest()[:16]
        out.add(h)
    return out


# =================================================================
# Main
# =================================================================
def gather_sections(chapter: str | None = None) -> list[Path]:
    paths: list[Path] = []
    for p in ROOT.rglob("*.html"):
        if set(p.parts) & SKIP_DIRS:
            continue
        if not (p.name.startswith("section-") or p.name == "index.html"):
            continue
        if chapter and f"module-{chapter}-" not in str(p):
            continue
        paths.append(p)
    return sorted(paths)


def build_index(paths: list[Path]) -> dict:
    idx = {}
    for p in paths:
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        text = extract_visible_text(html)
        ents = extract_entities(text)
        strong = extract_strong_terms(html)
        # Strong-bolded entities that match dictionary
        strong_canon = set()
        for s in strong:
            for m in ENTITY_RE.finditer(s):
                strong_canon.add(_canon(m.group(0)))
        hashes = sliding_hashes(text)
        idx[section_id(p)] = {
            "path": str(p.relative_to(ROOT)).replace('\\', '/'),
            "n_words": len(text.split()),
            "entities": dict(ents),
            "strong_entities": sorted(strong_canon),
            "strong_terms": sorted(strong),
            "hashes": list(hashes),
        }
    return idx


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def analyze(idx: dict, top: int, jth: float) -> dict:
    # Hot entities (sections that mention them)
    entity_to_sections: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for sid, info in idx.items():
        for e, n in info["entities"].items():
            entity_to_sections[e].append((sid, n))
    # Sort by total mention count
    hot = sorted(
        entity_to_sections.items(),
        key=lambda kv: -sum(n for _, n in kv[1]),
    )[:top]
    hot_out = []
    for e, occ in hot:
        total = sum(n for _, n in occ)
        nsec = len(occ)
        # Top 5 sections by count
        top_sections = sorted(occ, key=lambda x: -x[1])[:5]
        hot_out.append({
            "entity": CANON_TO_DISPLAY.get(e, e),
            "total_mentions": total,
            "sections": nsec,
            "top_sections": [{"sid": sid, "n": n} for sid, n in top_sections],
        })

    # Multiple-introduction: entity appears in <strong> of >=2 sections
    multi_intro: dict[str, list[str]] = defaultdict(list)
    for sid, info in idx.items():
        for e in info["strong_entities"]:
            multi_intro[e].append(sid)
    multi_intro_out = [
        {"entity": CANON_TO_DISPLAY.get(e, e), "sections": sids}
        for e, sids in multi_intro.items()
        if len(sids) >= 2
    ]
    multi_intro_out.sort(key=lambda x: -len(x["sections"]))

    # High-overlap pairs
    sids = list(idx.keys())
    pairs_out = []
    for i in range(len(sids)):
        ents_i = set(idx[sids[i]]["entities"].keys())
        if len(ents_i) < 5:
            continue
        for j in range(i + 1, len(sids)):
            ents_j = set(idx[sids[j]]["entities"].keys())
            if len(ents_j) < 5:
                continue
            jc = jaccard(ents_i, ents_j)
            if jc >= jth:
                # Compute the shared entities
                shared = sorted(ents_i & ents_j,
                                key=lambda e: -(idx[sids[i]]["entities"].get(e, 0)
                                                 + idx[sids[j]]["entities"].get(e, 0)))[:10]
                pairs_out.append({
                    "a": sids[i], "b": sids[j],
                    "jaccard": round(jc, 3),
                    "n_shared": len(ents_i & ents_j),
                    "n_a": len(ents_i), "n_b": len(ents_j),
                    "shared": [CANON_TO_DISPLAY.get(e, e) for e in shared],
                })
    pairs_out.sort(key=lambda p: -p["jaccard"])

    # Verbatim duplicates: hashes shared across >=2 sections
    hash_to_sections: dict[str, list[str]] = defaultdict(list)
    for sid, info in idx.items():
        for h in info["hashes"]:
            hash_to_sections[h].append(sid)
    verbatim = []
    seen_pairs: set[tuple[str, str]] = set()
    for h, sids in hash_to_sections.items():
        if len(sids) < 2:
            continue
        # Avoid same-section repeats
        uniq = sorted(set(sids))
        if len(uniq) < 2:
            continue
        # Record unique unordered pairs
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                pair = (uniq[i], uniq[j])
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                verbatim.append({"a": uniq[i], "b": uniq[j], "hash": h})
    # Aggregate by pair
    verbatim_by_pair: dict[tuple[str, str], int] = defaultdict(int)
    for v in verbatim:
        verbatim_by_pair[(v["a"], v["b"])] += 1
    verbatim_out = [
        {"a": a, "b": b, "n_chunks": n}
        for (a, b), n in verbatim_by_pair.items()
        if n >= 1
    ]
    verbatim_out.sort(key=lambda v: -v["n_chunks"])

    return {
        "hot_entities": hot_out,
        "multi_introductions": multi_intro_out,
        "high_overlap_pairs": pairs_out,
        "verbatim_pairs": verbatim_out,
    }


def render_markdown(analysis: dict, idx: dict) -> str:
    lines = []
    lines.append("# Duplicate-Content Detection Report")
    lines.append("")
    lines.append(f"Scanned {len(idx)} sections.")
    lines.append("")
    lines.append("## Top Hot Entities (mention count across sections)")
    lines.append("")
    lines.append("| Entity | Total Mentions | Sections | Top Carriers |")
    lines.append("|---|---:|---:|---|")
    for h in analysis["hot_entities"]:
        top = ", ".join(f"{s['sid']}({s['n']})" for s in h["top_sections"])
        lines.append(f"| {h['entity']} | {h['total_mentions']} | {h['sections']} | {top} |")
    lines.append("")
    lines.append("## Multiple Introductions (entity bolded in >=2 sections)")
    lines.append("")
    lines.append("Entities that appear in `<strong>` tags in 2+ sections likely have")
    lines.append("multiple introductions. The book should pick ONE canonical home for each.")
    lines.append("")
    lines.append("| Entity | # Sections | Sections |")
    lines.append("|---|---:|---|")
    for m in analysis["multi_introductions"][:50]:
        lines.append(
            f"| {m['entity']} | {len(m['sections'])} | "
            f"{', '.join(m['sections'][:10])} |"
        )
    lines.append("")
    lines.append("## High-Overlap Section Pairs (Jaccard on entities)")
    lines.append("")
    lines.append("Pairs of sections whose entity sets overlap heavily are candidates")
    lines.append("for content consolidation.")
    lines.append("")
    lines.append("| A | B | Jaccard | Shared | Top Shared Entities |")
    lines.append("|---|---|---:|---:|---|")
    for p in analysis["high_overlap_pairs"][:50]:
        lines.append(
            f"| {p['a']} | {p['b']} | {p['jaccard']} | "
            f"{p['n_shared']}/{p['n_a']}+{p['n_b']} | "
            f"{', '.join(p['shared'][:8])} |"
        )
    lines.append("")
    lines.append("## Verbatim Paragraph Duplicates (60-word windows)")
    lines.append("")
    lines.append("Pairs of sections that share verbatim 60-word chunks. High counts")
    lines.append("indicate accidental copy-paste that should be deduplicated.")
    lines.append("")
    lines.append("| A | B | Duplicate chunks |")
    lines.append("|---|---|---:|")
    for v in analysis["verbatim_pairs"][:30]:
        lines.append(f"| {v['a']} | {v['b']} | {v['n_chunks']} |")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Named-entity dedup detector")
    parser.add_argument("--chapter", help="Limit to a single module number (e.g. 42)")
    parser.add_argument("--top", type=int, default=40, help="Top-N hot entities")
    parser.add_argument("--jaccard-threshold", type=float, default=0.35,
                        help="Jaccard threshold for high-overlap pairs")
    parser.add_argument("--out", default=None, help="Markdown output path")
    parser.add_argument("--json-out", default=None, help="JSON output path")
    args = parser.parse_args()

    paths = gather_sections(args.chapter)
    idx = build_index(paths)
    analysis = analyze(idx, args.top, args.jaccard_threshold)
    md = render_markdown(analysis, idx)

    suffix = f"-ch{args.chapter}" if args.chapter else ""
    md_path = Path(args.out) if args.out else ROOT / "docs" / "content-audit" / f"DEDUP_REPORT{suffix}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md, encoding="utf-8")
    print(f"Markdown report: {md_path.relative_to(ROOT)}")

    if args.json_out:
        json_path = Path(args.json_out)
        json_path.write_text(json.dumps({"index": idx, "analysis": analysis},
                                        indent=2), encoding="utf-8")
        print(f"JSON dump: {json_path.relative_to(ROOT)}")

    # Print a short summary to stdout
    print(f"\nSections scanned: {len(idx)}")
    print(f"Hot entities (top 10):")
    for h in analysis["hot_entities"][:10]:
        print(f"  {h['total_mentions']:>4}x in {h['sections']:>3} sections: {h['entity']}")
    print(f"\nMulti-introduction entities: {len(analysis['multi_introductions'])}")
    print(f"High-overlap pairs (Jaccard>={args.jaccard_threshold}): {len(analysis['high_overlap_pairs'])}")
    print(f"Verbatim duplicate pairs: {len(analysis['verbatim_pairs'])}")


if __name__ == "__main__":
    main()
