#!/usr/bin/env python3
"""Fix generic 'Library Shortcut' callout titles to include library name and purpose.

Scans all .html files under part-*/, appendices/, and front-matter/
(skipping _archive), finds <div class="callout library-shortcut"> blocks
with a generic title "Library Shortcut", infers library name + purpose
from the prose and code inside, and rewrites the title.

Usage:
    python fix_library_shortcut_titles.py          # dry-run
    python fix_library_shortcut_titles.py --fix     # apply changes
"""

import argparse
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# ---------------------------------------------------------------------------
# Library name normalization map (lowercase -> display name)
# ---------------------------------------------------------------------------
LIBRARY_DISPLAY = {
    'litellm': 'LiteLLM',
    'litellm router': 'LiteLLM',
    'litellm proxy': 'LiteLLM Proxy',
    'langfuse': 'Langfuse',
    'openai': 'OpenAI',
    'anthropic': 'Anthropic',
    'sentence-transformers': 'Sentence Transformers',
    'sentence_transformers': 'Sentence Transformers',
    'transformers': 'HuggingFace Transformers',
    'hugging face transformers': 'HuggingFace Transformers',
    'bertviz': 'BertViz',
    'garak': 'Garak',
    'guardrails ai': 'Guardrails AI',
    'guardrails': 'Guardrails AI',
    'nemo guardrails': 'NeMo Guardrails',
    'umap': 'UMAP',
    'dspy': 'DSPy',
    'deepeval': 'DeepEval',
    'ragas': 'RAGAS',
    'peft': 'PEFT',
    'trl': 'TRL',
    'pytorch': 'PyTorch',
    'torch': 'PyTorch',
    'gensim': 'Gensim',
    'spacy': 'spaCy',
    'nltk': 'NLTK',
    'tiktoken': 'tiktoken',
    'vllm': 'vLLM',
    'fastapi': 'FastAPI',
    'wandb': 'Weights & Biases',
    'mlflow': 'MLflow',
    'langchain': 'LangChain',
    'llamaindex': 'LlamaIndex',
    'llama_index': 'LlamaIndex',
    'chromadb': 'ChromaDB',
    'pinecone': 'Pinecone',
    'instructor': 'Instructor',
    'outlines': 'Outlines',
    'bionemo': 'BioNeMo',
    'alphafold3': 'AlphaFold3',
    'alphafold': 'AlphaFold',
    'rdkit': 'RDKit',
    'deepchem': 'DeepChem',
    'torchdrug': 'TorchDrug',
    'mamba': 'Mamba',
    'rwkv': 'RWKV',
    'ctranslate2': 'CTranslate2',
    'optimum': 'Optimum',
    'autogptq': 'AutoGPTQ',
    'bitsandbytes': 'bitsandbytes',
    'unsloth': 'Unsloth',
    'modal': 'Modal',
    'codecarbon': 'CodeCarbon',
    'presidio': 'Presidio',
    'llm guard': 'LLM Guard',
    'inspect ai': 'Inspect AI',
    'openllmetry': 'OpenLLMetry',
    'pybreaker': 'pybreaker',
    'arize phoenix': 'Arize Phoenix',
    'phoenix': 'Arize Phoenix',
    'nnsight': 'nnsight',
    'transformer_lens': 'TransformerLens',
    'transformerlens': 'TransformerLens',
    'huggingface evaluate': 'HuggingFace Evaluate',
    'evaluate': 'HuggingFace Evaluate',
    'datasets': 'HuggingFace Datasets',
    'tokenizers': 'HuggingFace Tokenizers',
    'chronos': 'Chronos',
    'chronos-forecasting': 'Chronos',
    'sklearn': 'scikit-learn',
    'scikit-learn': 'scikit-learn',
    'semantic kernel': 'Semantic Kernel',
    'crewai': 'CrewAI',
    'autogen': 'AutoGen',
    'esm': 'ESM',
    'esm-2': 'ESM-2',
    'esm-3': 'ESM-3',
    'fair-esm': 'fair-esm',
    'tenacity': 'Tenacity',
    'marvin': 'Marvin',
    'gptcache': 'GPTCache',
}

# ---------------------------------------------------------------------------
# Topic keyword -> purpose label.  Checked against BOTH the callout prose
# and the code block content (first comment, function names, etc.).
# ---------------------------------------------------------------------------
TOPIC_PURPOSE = [
    # --- Very specific patterns first ---
    (r'attention\s+vis|head_view|model_view', 'Attention Visualization'),
    (r'activation\s+patch', 'Activation Patching'),
    (r'sparse\s+autoencoder|SAE\b|feature\s+discover', 'Feature Extraction'),
    (r'needle.*haystack|NIAH', 'Needle-in-a-Haystack Evaluation'),
    (r'PII\s+(?:redact|detect|remov|mitigat)|anonymi[zs]|Presidio', 'PII Detection'),
    (r'red.?team|adversarial.*test|vulnerability.*scan|garak\b|PyRIT', 'Red Teaming'),
    (r'carbon\s+footprint|energy.*track|power\s+draw|CodeCarbon', 'Carbon Footprint Tracking'),
    (r'semantic\s+cach|GPTCache', 'Semantic Caching'),
    (r'circuit\s+break|CircuitBreaker|pybreaker\.CircuitBreaker', 'Circuit Breaker'),

    # --- Domain-specific ---
    (r'pretrain.*genomic|DNA.*model|nucleotide|BioNeMo', 'Genomic Language Models'),
    (r'protein|ESM\b|amino\s+acid|AlphaFold', 'Protein Language Models'),
    (r'molecular|SMILES|drug\s+discover|RDKit|DeepChem|TorchDrug', 'Molecular Language Models'),
    (r'time\s+series|forecast|Chronos', 'Time Series Forecasting'),

    # --- Safety/guardrails (before evaluation, because safety blocks may
    #     contain evaluation-sounding keywords like "judge" in pseudocode) ---
    (r'PromptInjection|input\s+saniti|input_scanner|llm_guard', 'Input Sanitization'),
    (r'nemo_guardrails|safety\s+rail|check\s+jailbreak|rails.*input.*flows', 'Safety Guardrails'),
    (r'guardrail.*(?:AI|framework)|content\s+filter', 'Safety Guardrails'),

    # --- Evaluation patterns (before generic retrieval/classification) ---
    (r'FaithfulnessMetric|faithfulness.*scor|score_faithfulness', 'Faithfulness Evaluation'),
    (r'AnswerRelevancyMetric|relevancy.*metric', 'Answer Relevancy Evaluation'),
    (r'judge.*prompt|llm.*judge|G-Eval', 'LLM-as-Judge Evaluation'),
    (r'toxicity|stereotype|bias\s+measur|fairness\s+eval', 'Bias and Toxicity Evaluation'),
    (r'evaluat.*(?:framework|suite)|scoring\s+framework|deepeval\.(?:metrics|test_case)', 'Evaluation Framework'),

    # --- Structured output (before classification) ---
    (r'structured\s+output|json.*mode|pydantic.*valid|response_model|instructor\.from', 'Structured Output'),
    (r'@marvin|decorator.*llm', 'LLM-Powered Extraction'),

    # --- Observability and ops ---
    (r'prompt.*drift|prompt.*version|prompt.*manag|get_prompt', 'Prompt Management'),
    (r'instrument.*(?:LLM|API|call)|trace.*(?:LLM|span)|OpenLLMetry|opentelemetry', 'LLM Observability'),
    (r'cost.*(?:optim|rout|cascade|aware)|routing_strategy|cost.based.routing', 'Cost-Aware Routing'),
    (r'rate\s+limit|budget\s+enforc|request\s+manag|tpm_limit|rpm\b', 'Rate Limiting'),
    (r'(?:exponential\s+backoff|tenacity|@retry|stop_after_attempt)', 'Retry and Resilience'),
    (r'unified.*(?:interface|provider|API)|provider\s+abstract|litellm.*completion', 'Unified Provider Interface'),

    # --- Core ML tasks ---
    (r'cosine\s+sim|semantic\s+sim|sentence.*sim', 'Semantic Similarity'),
    (r'visualiz.*embed|embed.*visual|project.*2[dD]|t-?SNE|UMAP.*(?:project|fit_transform)', 'Embedding Visualization'),
    (r'(?:contextual|sentence|production)\s+embed', 'Sentence Embeddings'),
    (r'generate\(\)|do_sample|temperature.*top|top.?p.*sampl|nucleus.*sampl', 'Text Generation'),
    (r'interpretab|mechanistic', 'Interpretability'),
    (r'classif|sentiment|zero.?shot', 'Classification'),
    (r'function.*call|tool.*use|tool.*call', 'Function Calling'),
    (r'reasoning|chain.?of.?thought|system\s+2', 'Reasoning'),
    (r'speculative\s+decod', 'Speculative Decoding'),
    (r'fine.?tun', 'Fine-Tuning'),
    (r'LoRA|QLoRA|adapter', 'LoRA Adapters'),
    (r'quantiz', 'Quantization'),
    (r'distill', 'Distillation'),
    (r'alignment|RLHF|DPO', 'Alignment'),

    # --- Broad patterns last ---
    (r'(?<!retrieval_)retriev|rag\b|search.*document', 'Retrieval'),
    (r'tokeniz(?:ation|er\b)|BPE\b|WordPiece|SentencePiece', 'Tokenization'),
    (r'deploy|serving|endpoint', 'Deployment'),
    (r'pretrain|data\s+load', 'Data Loading'),
]


def normalize_library(name):
    """Normalize a library name to its display form."""
    key = name.strip().lower()
    if key in LIBRARY_DISPLAY:
        return LIBRARY_DISPLAY[key]
    return name.strip()


def collect_html_files():
    """Collect HTML files from part-*/, appendices/, and front-matter/."""
    files = []
    for pattern in ['part-*/**/section-*.html', 'appendices/**/section-*.html',
                     'front-matter/**/section-*.html']:
        for f in BOOK_ROOT.glob(pattern):
            if '_archive' not in str(f):
                files.append(f)
    return sorted(set(files))


def extract_callout_blocks(text):
    """Extract library-shortcut callout blocks with their positions.

    Returns list of (start, end, block_content) for blocks with generic titles.
    """
    blocks = []
    marker = '<div class="callout library-shortcut">'
    idx = 0
    while True:
        start = text.find(marker, idx)
        if start == -1:
            break
        # Find the closing </div> by tracking nesting depth
        depth = 0
        pos = start
        end = -1
        while pos < len(text):
            open_m = text.find('<div', pos)
            close_m = text.find('</div>', pos)
            if close_m == -1:
                break
            if open_m != -1 and open_m < close_m:
                depth += 1
                pos = open_m + 4
            else:
                depth -= 1
                if depth == 0:
                    end = close_m + len('</div>')
                    break
                pos = close_m + 6
        if end == -1:
            idx = start + len(marker)
            continue
        block = text[start:end]
        # Check if title is generic
        if re.search(r'<div class="callout-title">\s*Library Shortcut\s*</div>', block):
            blocks.append((start, end, block))
        idx = end
    return blocks


def extract_primary_library(block):
    """Extract the primary library name from the <strong> tag in the first <p>."""
    m = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
    if not m:
        return None
    first_p = m.group(1)
    # Find <strong> tags (skip ones inside <a> that are just links)
    strongs = re.findall(r'<strong>(?:<a[^>]*>)?([^<]+?)(?:</a>)?</strong>', first_p)
    if strongs:
        return normalize_library(strongs[0])
    # Check <code> tags for library names
    codes = re.findall(r'<code>([^<]+)</code>', first_p)
    for code in codes:
        if code.lower() in LIBRARY_DISPLAY:
            return normalize_library(code)
    return None


def infer_library_from_imports(block):
    """Fallback: detect library from import statements in code."""
    imports = re.findall(r'(?:from|import)\s+([\w.]+)', block)
    priority = [
        'litellm', 'langfuse', 'deepeval', 'ragas', 'instructor', 'marvin',
        'openai', 'anthropic', 'sentence_transformers', 'transformers',
        'peft', 'trl', 'datasets', 'tokenizers', 'dspy', 'langchain',
        'llama_index', 'outlines', 'guardrails', 'nemo_guardrails',
        'bertviz', 'nnsight', 'transformer_lens', 'gensim', 'spacy',
        'nltk', 'chromadb', 'pinecone', 'qdrant_client', 'weaviate',
        'wandb', 'mlflow', 'tenacity', 'pybreaker',
        'torch', 'sklearn', 'tiktoken', 'vllm', 'fastapi',
        'bitsandbytes', 'auto_gptq', 'optimum', 'unsloth', 'modal',
        'umap',
    ]
    for lib in priority:
        for imp in imports:
            if imp == lib or imp.startswith(lib + '.'):
                return normalize_library(lib)
    if imports:
        return normalize_library(imports[0])
    return None


def detect_purpose(block):
    """Detect purpose using topic keywords against the full block content."""
    # Strip HTML tags for matching
    plain = re.sub(r'<[^>]+>', ' ', block)
    for pattern, purpose in TOPIC_PURPOSE:
        if re.search(pattern, plain, re.IGNORECASE):
            return purpose
    return None


def is_meta_callout(block):
    """Check if this is a meta/explanatory callout (e.g., in front-matter)."""
    prose = re.sub(r'<[^>]+>', '', block).lower()
    if 'bridge the gap between understanding' in prose:
        return True
    if 'single library call' in prose:
        return True
    return False


def build_title(library, purpose):
    """Build the new title string."""
    if not library:
        return None
    if purpose:
        return f"Library Shortcut: {library} for {purpose}"
    return f"Library Shortcut: {library}"


def process_file(filepath, fix=False):
    """Process one file. Returns list of change dicts."""
    text = filepath.read_text(encoding='utf-8')
    blocks = extract_callout_blocks(text)
    if not blocks:
        return []

    changes = []
    # Process in reverse order so replacements don't shift offsets
    for start, end, block in reversed(blocks):
        if is_meta_callout(block):
            continue

        library = extract_primary_library(block)
        if not library:
            library = infer_library_from_imports(block)

        purpose = detect_purpose(block)
        new_title = build_title(library, purpose)
        line_no = text[:start].count('\n') + 1

        if not new_title:
            changes.append({
                'old': 'Library Shortcut',
                'new': '(SKIPPED: could not infer library)',
                'line': line_no,
                'file': filepath,
                'applied': False,
            })
            continue

        changes.append({
            'old': 'Library Shortcut',
            'new': new_title,
            'line': line_no,
            'file': filepath,
            'applied': True,
        })

        if fix:
            new_block = block.replace(
                '<div class="callout-title">Library Shortcut</div>',
                f'<div class="callout-title">{new_title}</div>',
                1
            )
            text = text[:start] + new_block + text[end:]

    if fix and any(c['applied'] for c in changes):
        filepath.write_text(text, encoding='utf-8')

    changes.reverse()
    return changes


def main():
    parser = argparse.ArgumentParser(description='Fix generic Library Shortcut titles')
    parser.add_argument('--fix', action='store_true', help='Apply fixes (default: dry-run)')
    args = parser.parse_args()

    files = collect_html_files()
    print(f"Scanning {len(files)} HTML files...\n")

    all_changes = []
    for f in files:
        changes = process_file(f, fix=args.fix)
        all_changes.extend(changes)

    if not all_changes:
        print("No generic 'Library Shortcut' titles found.")
        return

    applied = [c for c in all_changes if c['applied']]
    skipped = [c for c in all_changes if not c['applied']]

    print(f"{'FIXED' if args.fix else 'WOULD FIX'} {len(applied)} generic title(s):\n")
    for c in applied:
        rel = c['file'].relative_to(BOOK_ROOT)
        print(f"  {rel}:{c['line']}")
        print(f"    OLD: {c['old']}")
        print(f"    NEW: {c['new']}")
        print()

    if skipped:
        print(f"SKIPPED {len(skipped)} callout(s) (could not infer):\n")
        for c in skipped:
            rel = c['file'].relative_to(BOOK_ROOT)
            print(f"  {rel}:{c['line']}")
            print()


if __name__ == '__main__':
    main()
