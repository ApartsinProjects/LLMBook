"""v6.37: Shallow-content audit (heuristic A + B).

Generates KDP/validation/shallow_content.csv flagging:
  - Heuristic A: paragraphs with 4+ named entities and < 80 words ("shopping list")
  - Heuristic B: H2/H3 sections with < 250 words per declared concept

A "named entity" = capitalized multi-word phrase OR a known framework/model name
from a curated list.
"""
from __future__ import annotations
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'KDP' / 'validation' / 'shallow_content.csv'

# Known framework/model/library names that count as "named entities"
KNOWN_NAMES = set(s.lower() for s in [
    'GPT-4', 'GPT-4o', 'GPT-4o-mini', 'GPT-3.5', 'GPT-5', 'o1', 'o3', 'o4',
    'Claude', 'Claude-3', 'Claude-4', 'Sonnet', 'Opus', 'Haiku',
    'Gemini', 'Gemini Pro', 'Gemini Flash', 'Llama', 'Llama-2', 'Llama-3', 'Llama-4',
    'Mistral', 'Mixtral', 'Qwen', 'DeepSeek', 'DeepSeek-R1', 'DeepSeek-V3',
    'Phi', 'Phi-4', 'Cohere', 'Command-R', 'PaLM', 'Chinchilla', 'BERT', 'RoBERTa',
    'T5', 'BART', 'XLM-R',
    'LangChain', 'LangGraph', 'LlamaIndex', 'CrewAI', 'AutoGen', 'DSPy',
    'Semantic Kernel', 'Haystack', 'Pydantic', 'FastAPI', 'PyTorch', 'TensorFlow',
    'JAX', 'transformers', 'datasets', 'tokenizers', 'sentencepiece',
    'vLLM', 'TGI', 'Triton', 'TensorRT', 'TensorRT-LLM', 'DeepSpeed',
    'Megatron', 'FSDP', 'DDP', 'ZeRO',
    'MLflow', 'Weights & Biases', 'WandB', 'Comet', 'Neptune',
    'Pinecone', 'Weaviate', 'Chroma', 'Qdrant', 'Milvus', 'FAISS',
    'OpenAI', 'Anthropic', 'Google', 'Meta', 'NVIDIA',
    'Hugging Face', 'HuggingFace',
    'MCP', 'A2A', 'AGNTCY', 'ACP',
    'Cursor', 'Windsurf', 'Aider', 'Cline', 'Codex', 'Claude Code',
    'Sora', 'Veo', 'Kling', 'Runway',
    'BLEU', 'ROUGE', 'MMLU', 'HELM', 'GPQA', 'ARC-AGI', 'BIG-Bench',
    'RAG', 'GraphRAG', 'HyDE', 'BM25',
    'LoRA', 'QLoRA', 'PEFT', 'RLHF', 'DPO', 'GRPO', 'PPO', 'KTO',
    'Constitutional AI',
])


def normalize_text(html: str) -> str:
    text = re.sub(r'<pre>.*?</pre>', ' ', html, flags=re.DOTALL)
    text = re.sub(r'<section class="bibliography">.*?</section>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def count_entities(text: str) -> tuple[int, list[str]]:
    """Count entities in text. Returns (count, list-of-distinct-names)."""
    entities = set()
    # Find known names (case-insensitive)
    for name in KNOWN_NAMES:
        if re.search(r'\b' + re.escape(name) + r'\b', text, re.I):
            entities.add(name)
    # Capitalized 2-word phrases (e.g. "Hidden Markov Model", "Sparse Autoencoders")
    for m in re.finditer(r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', text):
        # Skip common false-positives
        cand = m.group(1)
        if cand.lower() in {'the transformer', 'the attention', 'this section',
                             'this chapter', 'this book', 'next section'}:
            continue
        if len(cand) > 60:
            continue
        entities.add(cand.lower())
    return len(entities), list(entities)[:8]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows_a = []  # shopping-list paragraphs
    rows_b = []  # low-words-per-concept sections
    sections = sorted(ROOT.glob('part-*/module-*/section-*.html'))

    for p in sections:
        text = p.read_text(encoding='utf-8', errors='replace')
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        main_m = re.search(r'<main[^>]*>(.*?)</main>', text, re.DOTALL)
        if not main_m:
            continue
        body = main_m.group(1)

        # A: per-paragraph "shopping list" check
        for i, m in enumerate(re.finditer(r'<p[^>]*>(.*?)</p>', body, re.DOTALL)):
            ptext = normalize_text(m.group(1))
            words = ptext.split()
            n_words = len(words)
            n_ent, ents = count_entities(ptext)
            if n_ent >= 4 and n_words < 80:
                rows_a.append({
                    'file': rel,
                    'paragraph_idx': i,
                    'word_count': n_words,
                    'entity_count': n_ent,
                    'entities': '; '.join(sorted(ents)),
                    'preview': ptext[:120],
                })

        # B: per-section words-per-concept ratio
        # Each <h2>/<h3> is a "declared concept"; count words between <main> open and </main>.
        h2h3_count = len(re.findall(r'<h[23]\b[^>]*>', body))
        all_text = normalize_text(body)
        section_words = len(all_text.split())
        # Declared concepts = h2/h3 + named callouts
        callout_count = len(re.findall(r'<div class="callout-title">', body))
        declared = max(1, h2h3_count + callout_count)
        wpc = section_words / declared
        if wpc < 250 and h2h3_count >= 3:
            rows_b.append({
                'file': rel,
                'h2h3_count': h2h3_count,
                'callout_count': callout_count,
                'section_words': section_words,
                'words_per_concept': round(wpc, 1),
            })

    # Write CSVs
    with OUT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_a[0].keys()) if rows_a else
                           ['file', 'paragraph_idx', 'word_count', 'entity_count',
                            'entities', 'preview'])
        w.writeheader()
        w.writerows(rows_a)
    OUT_B = OUT.parent / 'shallow_sections.csv'
    with OUT_B.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_b[0].keys()) if rows_b else
                           ['file', 'h2h3_count', 'callout_count',
                            'section_words', 'words_per_concept'])
        w.writeheader()
        w.writerows(rows_b)

    print(f'Heuristic A (shopping-list paragraphs): {len(rows_a)} flagged')
    print(f'Heuristic B (low words-per-concept):    {len(rows_b)} sections flagged')
    print(f'\nReports:\n  {OUT}\n  {OUT_B}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
