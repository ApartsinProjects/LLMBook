"""Prep script for adding context-aware fun-note callouts.

For each section missing a fun-note callout, this script extracts:
  - Section title
  - First paragraph (the topic intro)
  - 3-5 named entities most prominent in the section (libraries, models,
    methods) so the fun-note can reference something concrete
  - 2-3 representative h2 subsection titles (so the joke can hook into
    actual content)

Outputs a JSON file the LLM agent can consume to author one fun-note
per section: a 2-3 sentence comic / analogy that ties to the actual
content, not generic template text.

The fun-note format the book uses:
  <div class="callout fun-note">
    <div class="callout-title">Fun Fact</div>
    <p>...one to three sentences of humor / analogy / surprising
       historical anecdote / sharp metaphor...</p>
  </div>

Goal: NOT boilerplate. The script provides each section's context so
the agent can write something specific.
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts"}
REFERENCE_PATHS = ("tools-of-the-trade", "retrieval-tools", "conv-ai-tools",
                   "responsible-ai-tools", "scale-tools", "appendices",
                   "appendix-", "front-matter", "back-matter")

H1_RE = re.compile(r'<h1[^>]*>([^<]+)</h1>', re.IGNORECASE)
H2_RE = re.compile(r'<h2[^>]*>(.*?)</h2>', re.DOTALL | re.IGNORECASE)
FIRST_P_RE = re.compile(r'<p[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)
BIG_PICTURE_RE = re.compile(
    r'<div\s+class="callout big-picture"[^>]*>.*?<p[^>]*>(.*?)</p>',
    re.DOTALL | re.IGNORECASE,
)
FUN_NOTE_RE = re.compile(r'class="callout\s+fun-note"', re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')
CODE_BLOCK_RE = re.compile(
    r'<div\s+class="code-block-wrapper"[^>]*>.*?</div>\s*',
    re.DOTALL | re.IGNORECASE,
)


def visible(s: str) -> str:
    s = TAG_RE.sub(' ', s)
    s = html_mod.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def is_reference(rel: str) -> bool:
    return any(frag in rel.lower() for frag in REFERENCE_PATHS)


# Curated entity dictionary (reuse from dedup_detector)
SIMPLE_ENTITIES = [
    # Models
    "GPT-4", "GPT-5", "GPT-4o", "Claude", "Claude 4.7", "Llama-3", "Mistral",
    "Mixtral", "Gemini 2.5", "DeepSeek", "Phi-3", "Gemma", "Qwen", "PaLM",
    "BERT", "T5",
    # Methods
    "LoRA", "QLoRA", "RLHF", "DPO", "PPO", "GRPO", "RAG", "Chain-of-Thought",
    "ReAct", "BLEU", "ROUGE", "BERTScore", "perplexity", "FlashAttention",
    "PagedAttention", "speculative decoding", "knowledge distillation",
    "MoE", "Mixture-of-Experts",
    # Libraries / platforms
    "PyTorch", "TensorFlow", "transformers", "Hugging Face", "vLLM",
    "langchain", "LlamaIndex", "DSPy", "MLflow", "Weights & Biases",
    "Langfuse", "LangSmith", "Phoenix", "Pinecone", "Weaviate", "FAISS",
    "Qdrant", "ChromaDB", "OpenAI", "Anthropic",
    # Benchmarks
    "MMLU", "HumanEval", "MT-Bench", "Chatbot Arena", "RULER", "LongBench",
    "HellaSwag", "GSM8K", "MATH", "SWE-bench",
]
ENTITY_RE = re.compile(
    r'(?<![\w-])(?:' + '|'.join(re.escape(e) for e in SIMPLE_ENTITIES) + r')(?![\w-])',
    re.IGNORECASE,
)


def gather_section_context(p: Path) -> dict | None:
    """Return None if section has fun-note OR is reference-style."""
    rel = str(p.relative_to(ROOT)).replace('\\', '/')
    if is_reference(rel):
        return None
    try:
        html = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if FUN_NOTE_RE.search(html):
        return None

    # Title
    h1m = H1_RE.search(html)
    title = visible(h1m.group(1)) if h1m else p.name

    # Big-picture summary (preferred) or first paragraph
    big = BIG_PICTURE_RE.search(html)
    intro = visible(big.group(1))[:500] if big else ""
    if not intro:
        pm = FIRST_P_RE.search(CODE_BLOCK_RE.sub(' ', html))
        intro = visible(pm.group(1))[:500] if pm else ""

    # H2 subsection titles (skip "Prerequisites", "Exercises", etc.)
    skip_h2 = {"prerequisites", "exercises", "what's next", "what comes next",
                "bibliography", "further reading", "key takeaways", "self-check"}
    h2s = []
    for m in H2_RE.finditer(html):
        t = visible(m.group(1))
        if t.lower().strip().rstrip(':') in skip_h2:
            continue
        # Strip leading section numbers like "42.1.3"
        clean = re.sub(r'^\d+(?:\.\d+)*\s*', '', t).strip()
        if clean and clean not in h2s:
            h2s.append(clean)
        if len(h2s) >= 5:
            break

    # Top entities in the body
    body = visible(CODE_BLOCK_RE.sub(' ', html))
    ent_counts: Counter = Counter()
    for m in ENTITY_RE.finditer(body):
        canon = m.group(0)
        # Normalize: keep original casing of the dictionary
        for e in SIMPLE_ENTITIES:
            if e.lower() == canon.lower():
                canon = e
                break
        ent_counts[canon] += 1
    top_entities = [e for e, _ in ent_counts.most_common(5)]

    return {
        "section_id": p.stem,
        "path": rel,
        "title": title,
        "intro": intro,
        "subsection_titles": h2s,
        "top_entities": top_entities,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None, help="JSON output path")
    parser.add_argument("--limit", type=int, default=None, help="Limit to N sections")
    args = parser.parse_args()

    out: list[dict] = []
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & SKIP_DIRS:
            continue
        ctx = gather_section_context(p)
        if ctx:
            out.append(ctx)
        if args.limit and len(out) >= args.limit:
            break

    out_path = (Path(args.out) if args.out
                else ROOT / "docs" / "content-audit" / "fun_note_context.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"Sections needing fun-note: {len(out)}")
    print(f"Context JSON: {out_path.relative_to(ROOT)}")
    print(f"\nExamples:")
    for ctx in out[:3]:
        print(f"\n  {ctx['section_id']}: {ctx['title']}")
        print(f"    Subsections: {', '.join(ctx['subsection_titles'][:3])}")
        print(f"    Entities: {', '.join(ctx['top_entities'])}")


if __name__ == "__main__":
    main()
