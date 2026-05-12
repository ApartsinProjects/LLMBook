"""v6.45b: Extended bare-Section fix for broader prose patterns.

The v6.41 pass caught 'the/a/an/with standard/consider Section X.Y'.
v6.45 finds another ~161 patterns where Section X.Y appears as bare prose
in different syntactic positions (adjective-noun, possessive, etc.).

Conservative approach: a section-number-to-concept lookup is applied only
when the surrounding prose strongly suggests broken substitution (i.e. not
a recognized cross-reference construction like 'see Section X.Y').
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Section number -> concept name (using new post-renumber section numbers)
CONCEPT_BY_SECTION = {
    # Foundations
    '0.1': 'cross-entropy',
    '0.2': 'softmax',
    '0.3': 'PyTorch primitives',
    '0.4': 'reinforcement learning',
    # NLP / embeddings
    '1.1': 'NLP foundations',
    '1.3': 'word embeddings',
    '1.4': 'contextual embeddings',
    # Tokenization
    '2.1': 'tokenization',
    '2.2': 'BPE',
    '2.3': 'chat templates',
    # Sequence models / attention
    '3.1': 'RNN/LSTM',
    '3.2': 'attention',
    '3.3': 'self-attention',
    # Transformer
    '4.1': 'softmax',  # most common in this position is softmax/attention
    '4.5': 'chain-of-thought',
    # Decoding
    '5.2': 'sampling',
    # Pretraining
    '6.1': 'pretraining data',
    '6.4': 'data curation',
    # Reasoning
    '8.1': 'chain-of-thought',
    '8.2': 'reasoning models',
    # Inference
    '9.1': 'quantization',
    '9.2': 'KV cache',
    # Prompt
    '11.2': 'chain-of-thought prompting',
    '11.3': 'prompt patterns',
    # PEFT
    '15.1': 'LoRA',
    # Alignment
    '16.1': 'RLHF',
    '16.2': 'DPO',
    '16.3': 'Constitutional AI',
    # Embeddings/RAG
    '17.1': 'embedding models',
    '18.1': 'RAG',
    # Agent
    '20.1': 'AI agent',
    '20.6': 'agent memory',
    '21.1': 'tool use',
    '21.2': 'MCP',
    # Eval
    '27.1': 'evaluation metrics',
    '27.6': 'observability',
    '27.8': 'LLM-as-judge',
    # Safety
    '29.2': 'hallucination',
    '29.3': 'bias',
    '29.4': 'governance',
    '29.7': 'machine unlearning',
}

# Words that, when preceding "Section N.M", indicate a LEGITIMATE
# cross-reference (don't touch these).
LEGIT_PRECEDING = {
    'see', 'in', 'from', 'where', 'when', 'while', 'and', 'or', 'is', 'as',
    'before', 'after', 'covered', 'shown', 'cited', 'introduced', 'discussed',
    'reference', 'review', 'recall', 'revisit', 'subsection', 'chapter',
    'section', 'sub', 'per', 'via', 'inspired', 'detailed', 'explained',
    'mentioned', 'returned', 'returns', 'across', 'beyond', 'until', 'than',
    'described', 'follows', 'follow', 'figure', 'table', 'recap',
    'check', 'verify', 'compare', 'pair', 'paired', 'previously',
    'reviewing', 'overview', 'using', 'similar', 'unlike', 'like',
    'between', 'against', 'further', 'building', 'extends', 'extending',
    'parallel', 'now', 'visit', 'visited', 'introduces', 'analogous',
    'parallels', 'continuation', 'continued', 'continuing', 'connect',
    'connecting', 'connected', 'method', 'methods', 'approach',
    'approaches', 'topic', 'topics', 'chapter’s', "chapter's",
    'appendix', 'spans', 'span', 'covers', 'covering', 'concept',
    'concepts',
}

# Pattern: "<preceding-word> Section N.M" not followed by html/. or anchor end
PATTERN = re.compile(r'(\b\w+\b)(\s+)Section\s+(\d+)\.(\d+)\b')


def fix_text(text: str) -> tuple[str, int]:
    n = 0
    # Skip text inside <a> tags
    parts = re.split(r'(<a\b[^>]*>.*?</a>)', text, flags=re.DOTALL)

    def fix_part(s):
        nonlocal n
        def repl(m):
            nonlocal n
            prev = m.group(1).lower()
            if prev in LEGIT_PRECEDING:
                return m.group(0)
            sec = f'{m.group(3)}.{m.group(4)}'
            concept = CONCEPT_BY_SECTION.get(sec)
            if not concept:
                return m.group(0)
            n += 1
            # Replace "Section N.M" with the concept name
            return f'{m.group(1)}{m.group(2)}{concept}'
        return PATTERN.sub(repl, s)

    for i, part in enumerate(parts):
        if i % 2 == 0:  # outside <a>
            parts[i] = fix_part(part)
    return ''.join(parts), n


def main() -> int:
    SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/validation/')
    total = 0
    files_changed = 0
    for p in ROOT.rglob('*.html'):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_text, n = fix_text(text)
        if n > 0 and new_text != text:
            p.write_text(new_text, encoding='utf-8')
            total += n
            files_changed += 1
    print(f'Applied {total} extended-pattern fixes across {files_changed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
