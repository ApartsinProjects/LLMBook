"""Cycle 11 Step 2: Classify each of the 500 techniques into Tier A/B/C.

Tier A (core algorithms/concepts students must explain/derive/implement):
  Triggers:
    - Listed in 'foundations'/'concepts'/'fundamentals' chapters (parts 1-2, appendices A-D)
    - Mathematical concept central to LLMs (gradient descent, cross-entropy, ...)
    - Architectural pattern central to the field
    - Algorithm with formal name (BPE, beam search, PPO, ...)
    - Mentioned in 8+ sections of the book

Tier B (architectural variants, production patterns, important models):
  Triggers:
    - Specific named model with architectural significance (Mixtral, Mamba, ...)
    - Production pattern (RAG variant, agent framework, serving optimization)
    - Mentioned in 4-7 sections

Tier C (catalog: frontier model release / benchmark / dataset / tool):
  Default.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from _pedagogy_audit_v2 import parse_sections

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
INV = ROOT / 'slide-summaries' / '_techniques_500.json'
OUT = ROOT / 'slide-summaries' / '_techniques_500_tiered.json'

# Names that are unambiguously Tier A (core concepts / load-bearing algorithms)
TIER_A_FORCE = {
    # Math/ML primitives
    'cross-entropy', 'softmax', 'sigmoid', 'relu', 'gelu', 'silu', 'swiglu',
    'dropout', 'layernorm', 'batchnorm', 'rmsnorm', 'adam', 'adamw', 'sgd',
    'gradient descent', 'backpropagation', 'backprop',
    # Tokenization
    'bpe', 'wordpiece', 'sentencepiece', 'unigram',
    # Embeddings
    'word2vec', 'glove', 'fasttext', 'sbert',
    # Attention/architecture
    'attention', 'transformer', 'multi-head attention', 'self-attention',
    'positional encoding', 'rope', 'kv cache', 'kv-cache',
    'multi-query attention', 'mqa', 'grouped-query attention', 'gqa',
    'flashattention',
    # Decoding
    'beam search', 'greedy search', 'top-k', 'top-p', 'nucleus sampling',
    'temperature', 'speculative decoding',
    # Pretraining/scaling
    'scaling laws', 'chinchilla',
    # Models (canonical)
    'bert', 'gpt', 'gpt-2', 'gpt-3', 't5', 'llama', 'bart',
    # PEFT
    'lora', 'qlora', 'adapter', 'prefix tuning', 'prompt tuning',
    'knowledge distillation',
    # Alignment
    'rlhf', 'ppo', 'dpo', 'grpo', 'sft', 'reinforce',
    # Retrieval
    'rag', 'dpr', 'hnsw', 'ivf', 'faiss', 'mmr', 'tf-idf', 'bm25',
    # Reasoning
    'chain-of-thought', 'react', 'self-consistency',
    # Vision/audio
    'clip', 'vit', 'wav2vec', 'whisper', 'ctc',
    # Agents
    'mcp', 'langgraph', 'toolformer',
    # Evaluation
    'llm-as-judge', 'perplexity', 'cross-entropy',
    # NLP classical
    'crf', 'lda', 'lsa',
    # Quantization/serving
    'gptq', 'awq', 'vllm', 'fsdp', 'ddp', 'zero', 'quantization',
    'pagedattention',
    # Math
    'kl divergence',
    # Long-context
    'longformer', 'bigbird',
    # Diffusion (vision/multimodal generation; book has chapters on it)
    'diffusion', 'ddpm', 'ddim',
    # Mixture of experts
    'moe', 'mixture of experts', 'mixtral',
    # Distillation
    'distilbert',
    # Constitutional AI
    'constitutional ai',
    # Mamba
    'mamba',
    # Conformer
    'conformer',
    # CLIP-like
    'siglip', 'blip',
}

# Names that are Tier B (variants, models, production patterns)
TIER_B_FORCE = {
    # Recent flagship models that students should recognize
    'gpt-4', 'gpt-4o', 'claude 3.5 sonnet', 'llama 3', 'llama 3.1',
    'qwen 2.5', 'gemini', 'deepseek v3', 'deepseek r1', 'o1',
    'mistral', 'gemma 2', 'phi-3',
    # Important architectural variants
    'switch transformer', 'retnet', 'roberta', 'deberta', 'mbert',
    'mt5', 'nllb', 'longlora', 'xlm',
    # PEFT variants
    'p-tuning', 'ia3', 'mergekit', 'ties merging', 'task arithmetic',
    'model soup',
    # Alignment variants
    'kto', 'orpo', 'simpo', 'rlaif', 'prm', 'rlvr', 'actor-critic',
    'step-dpo',
    # Decoding/serving
    'medusa', 'eagle', 'lookahead decoding', 'prefix caching',
    'radixattention', 'continuous batching', 'tgi', 'sglang',
    # RAG variants
    'self-rag', 'corrective rag', 'crag', 'adaptive-rag', 'flare',
    'hyde', 'rag-fusion', 'rrf', 'fid', 'raft', 'raptor', 'cag',
    'graphrag', 'colbert',
    # Reasoning
    'tree-of-thoughts', 'reflexion', 'self-refine', 'best-of-n',
    'graph-of-thoughts', 'pal', 'program-of-thoughts', 'rewoo',
    # Audio
    'hubert', 'wavlm', 'beats', 'ast', 'clap', 'encodec', 'soundstream',
    'rvq', 'vq-vae', 'vits', 'bark', 'musicgen', 'musiclm',
    'mimi',
    # Vision-language variants
    'llava', 'qwen-vl', 'pixtral', 'molmo', 'idefics', 'internvl',
    'minicpm-v', 'cambrian', 'nvlm', 'dino', 'sam', 'deit', 'swin',
    # Agents frameworks
    'langchain', 'llamaindex', 'autogen', 'crewai', 'memgpt', 'lats',
    'openai swarm', 'smolagents', 'aider', 'openhands', 'devin', 'gorilla',
    'toolkengpt',
    # Quantization
    'nf4', 'fp8', 'bnb', 'gguf', 'eetq', 'hqq', 'marlin', 'exllamav2',
    # Training systems
    'megatron-lm', 'deepspeed',
    # Long context
    'yarn', 'alibi', 'position interpolation',
    # Misc
    'noam schedule', 'cosine schedule',
    # Embeddings
    'e5', 'gte', 'bge', 'simcse', 'voyage ai', 'jina-embeddings',
    'nomic-embed', 'colpali',
    # Multi-modal generation
    'stable diffusion',
    # Vision-large
    'dinov2',
    # SAE
    'sparse autoencoders',
    # Reward hacking - it's a real concept
    'reward hacking',
    # Differential privacy
    'differential privacy', 'dp-sgd',
    # Topic modeling
    'bertopic', 'lda', 'setfit',
    # Synthetic data
    'synthetic data',
    # Semantic caching
    'semantic caching',
    # Structured output
    'structured output',
    # Topics
    'gradient accumulation',
    # Recommender models
    'tiger', 'llara',
    # Eval
    'ragas', 'ares', 'trulens', 'mteb',
    # Code benchmarks
    'humaneval', 'mbpp', 'swe-bench', 'livecodebench',
    # Reading comp
    'mmlu', 'mmlu-pro', 'gpqa', 'big-bench', 'bbh', 'agieval', 'arc-agi',
    'hellaswag', 'longbench', 'mmmu', 'mm-vet', 'frontiermath',
    # XLM-R + Falcon
    'falcon',
    # NLLB-200
    'nllb-200',
}


# Names that are intrinsically Tier C: benchmarks/datasets/single tools/vendors
TIER_C_FORCE = {
    # Vendors/companies
    'google deepmind', 'nvidia', 'openai', 'anthropic', 'mistral ai',
    'cohere', 'pinecone', 'weaviate', 'chromadb', 'milvus', 'qdrant',
    'huggingface', 'hugging face', 'hugging face spaces',
    'elevenlabs', 'codecarbon',
    # Regulatory/standards
    'hipaa', 'finra', 'ferpa', 'eu ai act', 'nist ai rmf',
    'owasp llm top 10', 'c2pa',
    # Recent niche models
    'o3', 'phi-3.5', 'claude 3 opus', 'claude 3.5 haiku', 'claude 3.7',
    'mistral large', 'llama 3.2', 'llama 3.3',
    'llama 3.2 vision', 'qwq', 'gpt-4v',
    # Audio TTS
    'tortoise', 'f5-tts', 'openvoice', 'xtts', 'voicebox', 'llasa',
    'styletts', 'gpt-sovits', 'chattts', 'audioclip',
    # Benchmarks (catalog)
    'math', 'gaia', 'webarena',
    # Datasets
    'conll 2003',
    # Misc tools
    'guardrails ai', 'nemo guardrails', 'amd mi355x', 'executorch',
    'bertviz', 'lime', 'shap',
    # Anthropic-specific features
    'anthropic tool use', 'anthropic extended thinking',
    'openai function calling',
    # Agents (specific systems)
    'baby-agi', 'agent-q',
    # CI/CD
    'ci/cd', 'api documentation', 'ml engineering',
}


# Names that look like Tier A by frequency but are really infrastructure/catalog/vendor
TIER_DEMOTE_TO_C = {
    'api keys', 'cloud gpu', 'cuda', 'jax', 'mlx', 'csv', 'json mode',
    'json schema', 'iso', 'iso/iec', 'classical ml', 'closed-api',
    'hugging face hub', 'hugging face transformers', 'hugging face datasets',
    'hugging face trainer', 'meta llama', 'llm applications',
    'llm capabilities', 'llm-specific', 'infiniband',
    'ai safety',
    # Vendor product catalog entries
    'beir', 'agentbench', 'alpacaeval', 'arc-agi', 'longbench',
    'mmmu', 'mm-vet', 'frontiermath',
    # Single-app misclassifications
    'asr', 'pii redaction', 'transformerlens',
}

# Items previously in TIER_A_FORCE but better as Tier B (variants/specific models)
TIER_DEMOTE_TO_B = {
    'longformer', 'bigbird', 'gpt-2', 'gpt-3',
    'dac (audio)',
    # These are quantization formats (variants), Tier B is more honest
    'gptq', 'awq',
    # PEFT variants
    'prefix tuning', 'prompt tuning',
    # Specific RAG retrieval primitives
    'hype',
    # Mamba is borderline Tier A but in this book is covered as variant
    'mamba',
    # General "Quantization" h3 is too generic; quantization-as-concept is covered in ch 9
    'quantization',
    # torch.compile - specific tool feature
    'torch.compile',
}


def technique_signal_for(name: str, n_sections: int, source: str) -> str:
    """Return 'A', 'B', or 'C' tier."""
    n = name.lower().strip()
    # Force overrides (in priority order)
    if n in TIER_DEMOTE_TO_C:
        return 'C'
    if n in TIER_DEMOTE_TO_B:
        return 'B'
    if n in TIER_A_FORCE:
        return 'A'
    if n in TIER_B_FORCE:
        return 'B'
    if n in TIER_C_FORCE:
        return 'C'
    # Heuristic by section count (for cycle 11 deep-discovered items)
    if n_sections >= 8:
        return 'A'
    if n_sections >= 4:
        return 'B'
    # Default
    return 'C'


def main():
    inv = json.loads(INV.read_text(encoding='utf-8'))
    techniques = inv['techniques']

    # For each technique, count REAL section appearances using the regex
    # (for those without it already populated, i.e., inherited).
    EXCLUDE_DIRS = {'_downloads', 'node_modules', '.book-update',
                    'source_fix_backups', '_archive', 'KDP', 'slide-summaries',
                    'agents', '.git', 'kdp', 'temp_epub', 'vendor', 'templates',
                    'pagefind', '_concept-figs', 'capstone',
                    'generated-images', 'images', '__pycache__'}

    section_files = [p for p in ROOT.rglob('section-*.html')
                     if not (set(p.parts) & EXCLUDE_DIRS)]

    # Compile all regexes
    compiled = []
    for t in techniques:
        flags = 0 if t['name'] in {
            'SuRe', 'Eagle', 'Falcon', 'Idefics', 'Pixtral', 'Molmo', 'Cambrian',
            'Tortoise', 'Voicebox', 'Llasa', 'Aider', 'Devin', 'OpenHands',
            'Marlin', 'Medusa', 'FLARE', 'CRAG', 'NPO', 'IPO', 'ORM', 'PRM',
            'PAL', 'PoT', 'KTO', 'ORPO', 'SimPO', 'BGE', 'GTE', 'E5',
            'MATH', 'GPQA', 'BBH', 'Bark', 'AGIEval', 'RA-DIT',
        } else re.IGNORECASE
        try:
            compiled.append((t, re.compile(t['regex'], flags)))
        except re.error as e:
            print(f"Bad regex {t['name']}: {e}", file=sys.stderr)

    # Count sections per technique
    file_counts: dict[str, set[str]] = defaultdict(set)
    for path in section_files:
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for t, pat in compiled:
            if pat.search(html):
                file_counts[t['name']].add(str(path))

    # Classify
    out_techniques = []
    counts = {'A': 0, 'B': 0, 'C': 0}
    for t in techniques:
        n_sections = len(file_counts.get(t['name'], set()))
        if t.get('n_sections_appearing', 0):
            n_sections = max(n_sections, t['n_sections_appearing'])
        tier = technique_signal_for(t['name'], n_sections, t.get('source', ''))
        out_techniques.append({
            **t,
            'tier': tier,
            'n_sections_observed': n_sections,
        })
        counts[tier] += 1

    OUT.write_text(json.dumps({
        'total': len(out_techniques),
        'tier_counts': counts,
        'techniques': out_techniques,
    }, indent=2), encoding='utf-8')
    print(f'Saved {OUT}')
    print(f'Tier A: {counts["A"]}')
    print(f'Tier B: {counts["B"]}')
    print(f'Tier C: {counts["C"]}')
    print(f'TOTAL:  {sum(counts.values())}')


if __name__ == '__main__':
    main()
