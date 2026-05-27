"""Cycle 10: Discover named technique candidates beyond the curated 153.

Strategy:
  1. Walk every section-*.html under the book.
  2. Pull h2/h3 titles that look like technique names (start with [A-Z]).
  3. Pull <strong>…</strong> phrases that look like model/algorithm names.
  4. Track per-candidate counts: in how many distinct files, in how many h2/h3 titles.
  5. Apply an alias/normalisation table so 'GPT-4o' == 'GPT4o', 'Llama 3.1' == 'Llama-3.1'.
  6. Filter to: appears in >=2 distinct files AND at least one occurrence as
     a leading h2/h3 title token.
  7. Categorise via keyword rules.
  8. Assign weight: 1.0 if >=5 sections, 0.6 if 3-4, 0.3 if 2.
  9. Add a hand-vetted expansion list (recent LLMs, alignment, RAG variants,
     multimodal, audio TTS, embedding models, quantization formats, serving
     opts, benchmarks, agents) - keeping ONLY those that are actually mentioned
     in the book (>=2 sections or >=1 section if explicit verification).
 10. Merge with the existing 153 inventory to avoid duplicates.
 11. Save to _expanded_techniques.json.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from _pedagogy_audit_v2 import TECHNIQUES as CURATED_TECHNIQUES, parse_sections

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
EXCLUDE_DIRS = {'_downloads', 'node_modules', '.book-update',
                'source_fix_backups', '_archive', 'KDP', 'slide-summaries',
                'agents', '.git', 'kdp'}


# ---------- Hand-curated expansion list ----------
# Each entry: (display_name, regex, category, hint_weight)
# These get included only if regex hits >= 2 sections in the actual book.
EXPANSION_CANDIDATES = [
    # Recent LLMs (model-architecture)
    ("Claude 3.5 Sonnet", r"Claude\s*3\.5\s*Sonnet", "model-architecture", 1.0),
    ("Claude 3.5 Haiku", r"Claude\s*3\.5\s*Haiku", "model-architecture", 0.6),
    ("Claude 3.7", r"Claude\s*3\.7", "model-architecture", 0.6),
    ("Claude 3 Opus", r"Claude\s*3\s*Opus", "model-architecture", 0.6),
    ("GPT-4o", r"GPT-?4o\b", "model-architecture", 1.0),
    ("GPT-4", r"\bGPT-?4\b(?!o)", "model-architecture", 1.0),
    ("o1", r"\bo1(?:-(?:mini|preview|pro))?\b", "model-architecture", 1.0),
    ("o3", r"\bo3(?:-(?:mini|pro))?\b", "model-architecture", 0.6),
    ("Llama 3", r"\bLLaMA?\s*3\b(?!\.)", "model-architecture", 1.0),
    ("Llama 3.1", r"\bLLaMA?\s*3\.1\b", "model-architecture", 1.0),
    ("Llama 3.2", r"\bLLaMA?\s*3\.2\b", "model-architecture", 0.6),
    ("Llama 3.3", r"\bLLaMA?\s*3\.3\b", "model-architecture", 0.6),
    ("Llama 3.2 Vision", r"LLaMA?\s*3\.2[- ]?Vision|LLaMA?\s*3\.2\s*\d+B\s*Vision", "vlm", 0.6),
    ("Qwen 2.5", r"\bQwen\s*2\.5\b", "model-architecture", 1.0),
    ("Qwen-VL", r"\bQwen-?VL\b|Qwen2?-VL", "vlm", 0.6),
    ("Phi-3", r"\bPhi-?3(?:\.5)?\b", "model-architecture", 0.6),
    ("Phi-3.5", r"\bPhi-?3\.5\b", "model-architecture", 0.3),
    ("Gemma 2", r"\bGemma[- ]?2\b", "model-architecture", 0.6),
    ("DeepSeek V3", r"DeepSeek[- ]?V3", "model-architecture", 1.0),
    ("DeepSeek R1", r"DeepSeek[- ]?R1", "model-architecture", 1.0),
    ("QwQ", r"\bQwQ\b", "model-architecture", 0.3),
    ("Mistral Large", r"\bMistral[- ]?Large\b", "model-architecture", 0.6),
    ("Falcon", r"\bFalcon\b(?:[- ]?(?:7|40|180)B)?", "model-architecture", 0.6),
    ("Gemini", r"\bGemini\b(?:[- ]?(?:1\.5|2|Pro|Flash|Ultra))?", "model-architecture", 1.0),

    # Modern alignment
    ("KTO", r"\bKTO\b|Kahneman-Tversky", "alignment", 0.6),
    ("ORPO", r"\bORPO\b", "alignment", 0.6),
    ("SimPO", r"\bSimPO\b", "alignment", 0.6),
    ("IPO", r"\bIPO\b(?!\s*(?:offering|date))", "alignment", 0.3),
    ("RLAIF", r"\bRLAIF\b", "alignment", 0.6),
    ("PRM", r"Process\s*Reward\s*Model|\bPRM\b", "alignment", 0.6),
    ("ORM", r"Outcome\s*Reward\s*Model|\bORM\b", "alignment", 0.3),
    ("Step-DPO", r"Step[- ]?DPO", "alignment", 0.3),
    ("NPO", r"\bNPO\b|Negative\s*Preference", "alignment", 0.3),

    # Reasoning patterns
    ("Self-Consistency", r"Self[- ]?Consistency", "reasoning", 1.0),
    ("Graph-of-Thoughts", r"Graph[- ]?of[- ]?Thoughts?", "reasoning", 0.3),
    ("Algorithm-of-Thoughts", r"Algorithm[- ]?of[- ]?Thoughts?", "reasoning", 0.3),
    ("PAL", r"Program[- ]?Aided\s*L(?:M|anguage)", "reasoning", 0.6),
    ("Program-of-Thoughts", r"Program[- ]?of[- ]?Thoughts?|\bPoT\b", "reasoning", 0.6),
    ("Self-Refine", r"Self[- ]?Refine", "reasoning", 0.6),
    ("Best-of-N", r"\bBest[- ]?of[- ]?N\b", "reasoning", 0.6),
    ("Verifier-guided sampling", r"verifier[- ]guided\s*sampling|verifier\s*sampling", "reasoning", 0.3),

    # RAG variants
    ("Self-RAG", r"\bSelf[- ]?RAG\b", "retrieval", 0.6),
    ("Corrective RAG", r"Corrective\s*RAG|\bCRAG\b", "retrieval", 0.6),
    ("SuRe", r"\bSuRe\b", "retrieval", 0.3),
    ("ITER-RETGEN", r"ITER[- ]?RETGEN", "retrieval", 0.3),
    ("Adaptive-RAG", r"Adaptive[- ]?RAG", "retrieval", 0.6),
    ("FLARE", r"\bFLARE\b", "retrieval", 0.6),
    ("RA-DIT", r"\bRA[- ]DIT\b", "retrieval", 0.3),
    ("REPLUG", r"\bREPLUG\b", "retrieval", 0.3),

    # Recent multimodal
    ("Idefics", r"\bIdefics\b(?:2|3)?", "vlm", 0.3),
    ("Pixtral", r"\bPixtral\b", "vlm", 0.3),
    ("Molmo", r"\bMolmo\b", "vlm", 0.3),
    ("NVLM", r"\bNVLM\b", "vlm", 0.3),
    ("Cambrian", r"\bCambrian\b", "vlm", 0.3),
    ("InternVL", r"\bInternVL\b", "vlm", 0.3),
    ("MiniCPM-V", r"\bMiniCPM-?V\b", "vlm", 0.3),

    # Audio TTS/voice
    ("Tortoise", r"\bTortoise(?:[- ]?TTS)?\b", "audio", 0.3),
    ("F5-TTS", r"\bF5[- ]?TTS\b", "audio", 0.3),
    ("OpenVoice", r"\bOpenVoice\b", "audio", 0.3),
    ("XTTS", r"\bXTTS\b(?:[- ]?v2)?", "audio", 0.3),
    ("Voicebox", r"\bVoicebox\b", "audio", 0.3),
    ("Llasa", r"\bLlasa\b", "audio", 0.3),
    ("StyleTTS", r"Style[- ]?TTS", "audio", 0.3),
    ("GPT-SoVITS", r"GPT[- ]?SoVITS", "audio", 0.3),
    ("ChatTTS", r"\bChatTTS\b", "audio", 0.3),

    # Embedding models
    ("E5", r"\bE5\b(?:[- ]?large|mistral)?", "embedding", 0.6),
    ("GTE", r"\bGTE\b(?:[- ]?large|small)?", "embedding", 0.3),
    ("BGE", r"\bBGE\b(?:[- ]?(?:M3|large|base|small))?", "embedding", 0.6),
    ("Voyage AI", r"\bVoyage(?: AI)?\b", "embedding", 0.3),
    ("jina-embeddings", r"jina[- ]?embeddings?|Jina\s*Embeddings", "embedding", 0.3),
    ("nomic-embed", r"nomic[- ]?embed", "embedding", 0.3),
    ("ColBERT", r"\bColBERT\b(?:v2)?", "embedding", 0.6),
    ("ColPali", r"\bColPali\b", "embedding", 0.3),

    # Quantization formats
    ("FP8", r"\bFP8\b|float8", "serving", 0.6),
    ("NF4", r"\bNF4\b|NormalFloat-?4", "serving", 0.6),
    ("BNB", r"\bbitsandbytes\b|\bBNB\b", "serving", 0.6),
    ("EETQ", r"\bEETQ\b", "serving", 0.3),
    ("HQQ", r"\bHQQ\b", "serving", 0.3),
    ("Marlin", r"\bMarlin\b(?:[- ]?kernel)?", "serving", 0.3),
    ("ExLlamaV2", r"ExLlamaV2|exllama2|EXL2", "serving", 0.3),
    ("GGUF", r"\bGGUF\b|llama\.cpp", "serving", 0.6),

    # Serving / inference optimizations
    ("Medusa", r"\bMedusa\b(?:[- ]?heads?)?", "serving", 0.6),
    ("Eagle", r"\bEAGLE\b(?:[- ]?\d)?", "serving", 0.3),
    ("Lookahead Decoding", r"Lookahead\s*Decoding", "serving", 0.3),
    ("Prefix Caching", r"prefix\s*cach", "serving", 0.6),
    ("RadixAttention", r"RadixAttention", "serving", 0.3),
    ("Continuous Batching", r"continuous\s*batching", "serving", 0.6),
    ("PagedAttention", r"PagedAttention", "serving", 0.6),

    # Benchmarks
    ("LiveCodeBench", r"LiveCodeBench", "benchmark", 0.3),
    ("BIG-Bench", r"BIG[- ]?Bench(?:[- ]?Hard)?|\bBBH\b", "benchmark", 0.6),
    ("AGIEval", r"\bAGIEval\b", "benchmark", 0.3),
    ("MMLU-Pro", r"MMLU[- ]?Pro", "benchmark", 0.3),
    ("MMLU", r"\bMMLU\b(?!-Pro)", "benchmark", 1.0),
    ("GPQA", r"\bGPQA\b", "benchmark", 0.3),
    ("ARC-AGI", r"ARC[- ]?AGI", "benchmark", 0.3),
    ("SWE-bench", r"SWE[- ]?bench", "benchmark", 0.6),
    ("HumanEval", r"\bHumanEval\b\+?", "benchmark", 0.6),
    ("MATH", r"\bMATH\b\s*benchmark|MATH\s*dataset", "benchmark", 0.3),
    ("HellaSwag", r"\bHellaSwag\b", "benchmark", 0.3),

    # Agents
    ("LATS", r"\bLATS\b|Language\s*Agent\s*Tree", "agents", 0.3),
    ("Agent-Q", r"\bAgent[- ]?Q\b", "agents", 0.3),
    ("OpenHands", r"\bOpenHands\b", "agents", 0.3),
    ("Devin", r"\bDevin\b(?:\s*AI)?", "agents", 0.3),
    ("Aider", r"\bAider\b", "agents", 0.3),
    ("OpenAI Swarm", r"OpenAI\s*Swarm", "agents", 0.3),
    ("SmolAgents", r"\bSmolAgents\b|smolagents", "agents", 0.3),
]


def category_for(name: str, context_text: str = "") -> str:
    n = name.lower()
    if any(k in n for k in ['gpt', 'llama', 'qwen', 'mistral', 'gemma', 'phi-', 'falcon',
                            'claude', 'gemini', 'deepseek', 'mixtral', 'mamba', 'bert',
                            'palm', 't5', 'bart', 'rwkv', 'mistral-', 'yi-']):
        return 'model-architecture'
    if any(k in n for k in ['rope', 'flash', 'kv ', 'mqa', 'gqa', 'alibi', 'attention']):
        return 'attention'
    if any(k in n for k in ['bpe', 'wordpiece', 'sentencepiece', 'tokeniz']):
        return 'tokenization'
    if any(k in n for k in ['embed', 'word2vec', 'glove', 'fasttext', 'sbert', 'colbert', 'bge', 'gte']):
        return 'embedding'
    if any(k in n for k in ['rag', 'retrieval', 'dpr', 'hnsw', 'faiss', 'ivf']):
        return 'retrieval'
    if any(k in n for k in ['lora', 'qlora', 'adapter', 'peft', 'tuning']):
        return 'peft'
    if any(k in n for k in ['rlhf', 'ppo', 'dpo', 'grpo', 'rlvr', 'sft', 'kto', 'orpo', 'simpo', 'rlaif']):
        return 'alignment'
    if any(k in n for k in ['cot', 'chain-of-thought', 'react', 'reflection', 'tree-of', 'self-consist', 'self-refine']):
        return 'reasoning'
    if any(k in n for k in ['vllm', 'sglang', 'tgi', 'medusa', 'eagle', 'speculative', 'paged', 'batching']):
        return 'serving'
    if any(k in n for k in ['fsdp', 'ddp', 'zero', 'deepspeed', 'megatron']):
        return 'training-sys'
    if any(k in n for k in ['agent', 'langchain', 'langgraph', 'crewai', 'autogen', 'mcp']):
        return 'agents'
    if any(k in n for k in ['clip', 'vit', 'llava', 'blip', 'qwen-vl', 'siglip', 'dino', 'sam', 'molmo',
                            'idefics', 'pixtral', 'nvlm', 'internvl']):
        return 'vlm'
    if any(k in n for k in ['wav2vec', 'hubert', 'whisper', 'audio', 'speech', 'tts', 'voice', 'sound',
                            'music', 'encodec', 'codec', 'mimi']):
        return 'audio'
    if any(k in n for k in ['eval', 'judge', 'ragas']):
        return 'eval'
    if any(k in n for k in ['mmlu', 'humaneval', 'swe-bench', 'gpqa', 'bench', 'glue', 'squad', 'arc-agi', 'agieval']):
        return 'benchmark'
    if any(k in n for k in ['recsys', 'recom']):
        return 'recsys'
    if any(k in n for k in ['gptq', 'awq', 'fp8', 'nf4', 'gguf', 'bnb', 'hqq', 'quant']):
        return 'serving'
    return 'tooling'


def normalize(name: str) -> str:
    """Lower-case + strip hyphens / spaces for alias detection."""
    return re.sub(r'[\s\-_]', '', name.lower())


def weight_for(n_sections: int) -> float:
    if n_sections >= 5:
        return 1.0
    if n_sections >= 3:
        return 0.6
    return 0.3


def is_in_skip_path(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & EXCLUDE_DIRS)


def discover():
    section_files: list[Path] = []
    for path in ROOT.glob('**/section-*.html'):
        if is_in_skip_path(path):
            continue
        section_files.append(path)
    print(f'Scanning {len(section_files)} section files.')

    # Already-curated names (normalised) to avoid duplicates
    curated_norms = {normalize(name) for name, _, _, _ in CURATED_TECHNIQUES}

    # Names that need CASE-SENSITIVE matching to avoid English-word collisions
    # (e.g. "SuRe", "Eagle", "Falcon", "Idefics", "Pixtral").
    CASE_SENSITIVE = {
        'SuRe', 'Eagle', 'Falcon', 'Idefics', 'Pixtral', 'Molmo', 'Cambrian',
        'Tortoise', 'Voicebox', 'Llasa', 'Aider', 'Devin', 'OpenHands',
        'Marlin', 'Medusa', 'FLARE', 'CRAG', 'NPO', 'IPO', 'ORM', 'PRM',
        'PAL', 'PoT', 'KTO', 'ORPO', 'SimPO', 'BGE', 'GTE', 'E5',
        'MATH', 'GPQA', 'BBH', 'Bark', 'AGIEval', 'RA-DIT',
        'Best-of-N', 'Self-Refine', 'Self-RAG', 'OpenAI Swarm',
    }

    def compile_case_aware(name: str, rx: str) -> re.Pattern:
        # If the regex contains literal name AND that name is in CASE_SENSITIVE, compile case-sensitive
        # Otherwise compile case-insensitive (matches existing v2 behavior)
        if name in CASE_SENSITIVE:
            return re.compile(rx)
        return re.compile(rx, re.IGNORECASE)

    # Step A: Verify each EXPANSION_CANDIDATE actually appears in the book
    # (counted by distinct files + h2/h3 title hits).
    cand_compiled = []
    for nm, rx, cat, w in EXPANSION_CANDIDATES:
        try:
            cand_compiled.append((nm, compile_case_aware(nm, rx), cat, w))
        except re.error as e:
            print(f'Bad regex for {nm}: {e}', file=sys.stderr)

    cand_files = defaultdict(set)
    cand_title_hits = defaultdict(int)
    cand_total_hits = defaultdict(int)

    for path in section_files:
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        sections = parse_sections(html)
        # Per-file: track which candidates fire in this file
        seen_in_file = set()
        for sec in sections:
            for nm, pat, _, _ in cand_compiled:
                title_hit = bool(pat.search(sec['title']))
                body_hits = len(pat.findall(sec['body']))
                if title_hit:
                    cand_title_hits[nm] += 1
                if title_hit or body_hits:
                    seen_in_file.add(nm)
                    cand_total_hits[nm] += body_hits + (1 if title_hit else 0)
        for nm in seen_in_file:
            cand_files[nm].add(str(path))

    expansion_results = []
    for nm, pat, cat, w_hint in cand_compiled:
        n_files = len(cand_files[nm])
        if n_files < 2:
            continue
        if normalize(nm) in curated_norms:
            continue
        weight = weight_for(n_files)
        # Cap by hint weight (so e.g. niche models stay 0.3 even if mentioned a lot)
        weight = min(weight, max(w_hint, 0.3))
        expansion_results.append({
            'name': nm,
            'regex': pat.pattern,
            'category': cat,
            'weight': weight,
            'found_in_n_sections': n_files,
            'title_hits': cand_title_hits[nm],
            'total_hits': cand_total_hits[nm],
            'source': 'curated-expansion',
        })

    # Step B: Free-form discovery from h2/h3 titles & <strong>…</strong> markers.
    # Pattern: starts with an uppercase letter, optionally hyphen/digit/letters,
    # up to 4 tokens, plausible name length.
    title_token_re = re.compile(
        r'^([A-Z][A-Za-z0-9]+(?:[-/\s][A-Z0-9][A-Za-z0-9]*){0,3})(?:[:\s\(]|$)'
    )
    strong_re = re.compile(
        r'<strong>([A-Z][A-Za-z0-9\-]+(?:[- ][A-Z][A-Za-z0-9\-]+){0,3})</strong>'
    )

    cand2_files = defaultdict(set)
    cand2_title_hits = defaultdict(int)

    BLOCKLIST = {
        'figure', 'figures', 'table', 'tables', 'algorithm', 'example',
        'examples', 'definition', 'theorem', 'lemma', 'proof', 'note', 'tip',
        'warning', 'remark', 'exercise', 'exercises', 'lab', 'labs', 'self',
        'summary', 'overview', 'introduction', 'background', 'context',
        'references', 'bibliography', 'appendix', 'chapter', 'section',
        'part', 'preface', 'foreword', 'conclusion', 'glossary', 'index',
        'putting', 'key', 'what', 'why', 'how', 'when', 'where', 'who',
        'common', 'standard', 'basic', 'simple', 'classic', 'modern',
        'general', 'specific', 'practical', 'theoretical', 'core',
        'main', 'next', 'previous', 'first', 'second', 'third',
        'fundamental', 'advanced', 'beginner', 'expert', 'intermediate',
        'apparatus', 'glossary', 'further', 'official', 'recommended',
        'a', 'an', 'the', 'in', 'on', 'with', 'and', 'or', 'is', 'are',
        'pre', 'post', 'mini', 'meta', 'multi', 'cross', 'inter',
        # Lab/exercise boilerplate
        'prerequisites', 'objective', 'objectives', 'step', 'steps', 'setup',
        'expected', 'stretch', 'extension', 'extensions', 'comparing',
        'foundational', 'building', 'tools', 'benchmarks', 'cost', 'surveys',
        'observability', 'choosing', 'communities', 'comparison', 'audio',
        'evaluation', 'task', 'tasks', 'problem', 'problems', 'goal', 'goals',
        'method', 'methods', 'approach', 'approaches', 'pipeline', 'pipelines',
        'training', 'inference', 'serving', 'deployment', 'production',
        'model', 'models', 'dataset', 'datasets', 'recipe', 'recipes',
        'application', 'applications', 'use', 'using', 'choose', 'pick',
        'tooling', 'guide', 'guides', 'tutorial', 'tutorials', 'tier',
        'level', 'levels', 'walkthrough', 'demo', 'demos', 'reading',
        'optional', 'required', 'additional', 'related', 'similar', 'other',
        'definitions', 'notation', 'symbols', 'units', 'conventions',
        'history', 'origin', 'origins', 'motivation', 'rationale',
        'limitation', 'limitations', 'trade', 'tradeoff', 'tradeoffs',
        'pros', 'cons', 'advantages', 'disadvantages', 'benefits',
        'caveat', 'caveats', 'pitfall', 'pitfalls', 'gotcha', 'gotchas',
        'recipe', 'cookbook', 'checklist', 'template', 'templates',
        'definition', 'output', 'input', 'inputs', 'outputs',
        'concept', 'concepts', 'idea', 'ideas', 'principle', 'principles',
        'rule', 'rules', 'policy', 'policies', 'guideline', 'guidelines',
        'experiment', 'experiments', 'result', 'results', 'analysis',
        'discussion', 'remark', 'remarks', 'note', 'notes',
        'why', 'when', 'where', 'who', 'what', 'how',
        'big', 'small', 'large', 'huge', 'tiny',
        'real', 'fake', 'true', 'false', 'good', 'bad', 'better', 'best',
        'why', 'this', 'these', 'those', 'each', 'every', 'all', 'some',
        'no', 'none', 'any', 'both', 'either', 'neither',
        'numerical', 'analytical', 'empirical', 'experimental',
        'visual', 'visualizing', 'visualization', 'visualizations',
        'understanding', 'learning', 'thinking', 'reasoning',
        'managing', 'controlling', 'measuring', 'monitoring', 'tracking',
        'optimizing', 'tuning', 'configuring', 'scaling',
        'data', 'code', 'text', 'image', 'images', 'video', 'videos',
        'sample', 'samples', 'batch', 'batches', 'token', 'tokens',
        'layer', 'layers', 'block', 'blocks', 'module', 'modules',
        'class', 'classes', 'function', 'functions', 'method', 'methods',
        'object', 'objects', 'instance', 'instances',
        'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
        'one', 'zero', 'half',
    }

    def looks_like_technique(name: str) -> bool:
        """Heuristic: must look like a model/algorithm name, not a plain English phrase."""
        words = re.split(r'[-/\s]', name)
        # Reject if any single token is in BLOCKLIST
        for w in words:
            if w.lower() in BLOCKLIST:
                return False
        # Reject generic "X N" labels like Pattern 1, Phase 1, Stage 2, Step 3, Tier 1, Level 5
        if re.fullmatch(r'(?:Pattern|Phase|Stage|Step|Tier|Level|Part|Chapter|Module|Section)\s+\d+', name):
            return False
        # Reject very-generic 3-letter acronyms that overlap with category names
        if name in {'LLM', 'RAG', 'PEFT', 'GPU', 'CPU', 'API', 'SDK', 'CLI', 'GUI', 'TPU',
                    'MLM', 'NLP', 'ML', 'AI', 'NN', 'SQL', 'JSON', 'YAML', 'HTML', 'CSS',
                    'FFT', 'STFT', 'DTW', 'FIR', 'IIR', 'DSP', 'CPU', 'PSU', 'RAM', 'SSD'}:
            return False
        if len(name) <= 2 or len(name) > 50:
            return False
        # Strong signal: contains a digit (e.g., GPT-4, Llama-3.1, Phi-3, T5, NF4, BPE-50k)
        if re.search(r'\d', name):
            return True
        # Strong signal: contains hyphen with at least one all-caps token
        if '-' in name and any(re.fullmatch(r'[A-Z]{2,}', w) for w in words):
            return True
        # Strong signal: any token is an acronym (all-caps, >=2 letters, <=8)
        for w in words:
            if re.fullmatch(r'[A-Z]{2,8}', w):
                return True
        # CamelCase with lowercase letters mixed in (e.g., LlamaIndex, BERTopic, FastText)
        if re.fullmatch(r'[A-Z][a-z]+(?:[A-Z][a-z]+){1,}', name):
            return True
        # Reject everything else (plain capitalized phrases)
        return False

    for path in section_files:
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        sections = parse_sections(html)
        seen_in_file: dict[str, bool] = {}
        for sec in sections:
            m = title_token_re.match(sec['title'])
            if m:
                cand_name = m.group(1).strip()
                if looks_like_technique(cand_name):
                    seen_in_file.setdefault(cand_name, False)
                    seen_in_file[cand_name] = True  # title hit
            for sm in strong_re.findall(sec['body']):
                if looks_like_technique(sm):
                    seen_in_file.setdefault(sm, False)
        for cand_name, was_title in seen_in_file.items():
            cand2_files[cand_name].add(str(path))
            if was_title:
                cand2_title_hits[cand_name] += 1

    # Collapse aliases: bucket by normalize(name); pick most common spelling.
    bucket_files: dict[str, set] = defaultdict(set)
    bucket_titles: dict[str, int] = defaultdict(int)
    bucket_spellings: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    for name, files in cand2_files.items():
        key = normalize(name)
        bucket_files[key] |= files
        bucket_titles[key] += cand2_title_hits[name]
        bucket_spellings[key][name] += len(files)

    expansion_free = []
    already_norms = curated_norms | {normalize(r['name']) for r in expansion_results}

    for key, files in bucket_files.items():
        if len(files) < 2:
            continue
        if bucket_titles[key] < 1:
            continue
        if key in already_norms:
            continue
        # Skip if matches curated regex (alias missed by normalize)
        spelling = max(bucket_spellings[key].items(), key=lambda kv: kv[1])[0]
        matched_curated = False
        for cname, cregex, _, _ in CURATED_TECHNIQUES:
            try:
                if re.search(cregex, spelling, re.IGNORECASE):
                    matched_curated = True
                    break
            except re.error:
                continue
        if matched_curated:
            continue
        cat = category_for(spelling)
        expansion_free.append({
            'name': spelling,
            'regex': r'\b' + re.escape(spelling) + r'\b',
            'category': cat,
            'weight': weight_for(len(files)),
            'found_in_n_sections': len(files),
            'title_hits': bucket_titles[key],
            'total_hits': bucket_titles[key],
            'source': 'free-form-discovery',
        })

    # Sort by sections found
    expansion_results.sort(key=lambda r: (-r['found_in_n_sections'], r['name'].lower()))
    expansion_free.sort(key=lambda r: (-r['found_in_n_sections'], r['name'].lower()))

    # Apply a sanity cap on free-form: only keep those with >=3 sections OR title_hits>=2
    free_kept = [r for r in expansion_free
                 if r['found_in_n_sections'] >= 3 or r['title_hits'] >= 2]

    # Final merged inventory
    final = []
    # Keep all curated, marked with source
    for name, regex, cat, w in CURATED_TECHNIQUES:
        final.append({
            'name': name, 'regex': regex, 'category': cat, 'weight': w,
            'source': 'curated-original',
        })
    final.extend(expansion_results)
    final.extend(free_kept)

    # Save
    out = ROOT / 'slide-summaries' / '_expanded_techniques.json'
    out.write_text(
        json.dumps({
            'total': len(final),
            'curated_original': len(CURATED_TECHNIQUES),
            'curated_expansion_kept': len(expansion_results),
            'free_form_kept': len(free_kept),
            'free_form_total_candidates': len(expansion_free),
            'techniques': final,
        }, indent=2),
        encoding='utf-8',
    )
    print(f'Saved {out}')
    print(f'  curated original: {len(CURATED_TECHNIQUES)}')
    print(f'  curated-expansion kept: {len(expansion_results)}')
    print(f'  free-form kept: {len(free_kept)} (of {len(expansion_free)} candidates)')
    print(f'  TOTAL: {len(final)}')

    # Show top 30 curated-expansion adds
    print('\nTop 20 curated-expansion adds (by n_sections):')
    for r in expansion_results[:20]:
        print(f"  {r['name']:25s} n_sec={r['found_in_n_sections']:3d}  titles={r['title_hits']:2d}  w={r['weight']}  ({r['category']})")

    print('\nTop 25 free-form discoveries (by n_sections):')
    for r in free_kept[:25]:
        print(f"  {r['name']:35s} n_sec={r['found_in_n_sections']:3d}  titles={r['title_hits']:2d}  w={r['weight']}  ({r['category']})")


if __name__ == '__main__':
    discover()
