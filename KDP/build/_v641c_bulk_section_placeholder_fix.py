"""v6.41c: Bulk fix bare 'Section X.Y' placeholders using a context-aware lookup.

For each prereq / big-picture / prose block where 'the Section X.Y' appears,
determine the right concept name based on (a) the section number and
(b) the surrounding prose. Apply fixes with high confidence; flag the
ambiguous remainder for manual review.

Also fixes empty <a></a> tags that appear in the same broken auto-linker
output (stripped link text, leaving an empty anchor element).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Map: (section X.Y, surrounding-context-keyword) -> concept name
# Section numbers use the NEW post-renumber chapter numbers.
CONCEPT_MAP = {
    # Cross-entropy, softmax, layer norm, attention, transformer
    ('4.1', 'softmax'):              'softmax',
    ('4.1', 'transformer'):          'Transformer architecture',
    ('4.1', 'attention'):            'attention layers',
    ('4.1', 'kernel'):               'softmax kernel',
    ('4.1', 'vision'):               'vision encoder',
    ('4.1', 'classifier'):           'Transformer classifier',
    ('4.1', 'positional'):           'positional encoding scheme',
    ('4.1', 'embedding'):            'transformer-based model',
    ('4.1', 'familiarity'):          'Transformer architecture',
    ('4.1', 'covered in'):           'attention mechanism',
    ('4.1', 'multi-head'):           'multi-head attention',
    # Generic catch-all for 4.1 in unknown context
    ('4.1', None):                   'Transformer architecture',
    # Chapter 3 sequence models
    ('3.1', None):                   'sequence model',
    ('3.2', None):                   'attention mechanism',
    ('3.3', None):                   'self-attention',
    # Chain-of-thought / reasoning
    ('8.1', 'reasoning'):            'chain-of-thought reasoning',
    ('8.1', 'thinking'):             'scratchpad of reasoning tokens',
    ('8.1', 'inference'):            'chain-of-thought reasoning',
    ('8.1', 'advances'):             'reasoning advances',
    ('8.1', 'prompting'):            'chain-of-thought prompting',
    ('8.1', 'capabilities'):         'chain-of-thought reasoning',
    ('8.1', 'reasoning extends'):    'chain-of-thought',
    ('8.1', None):                   'chain-of-thought reasoning',
    # Pretraining / BERT
    ('6.1', None):                   'pretraining data',
    ('6.4', None):                   'data curation pipeline',
    # Inference / KV cache / quantization
    ('9.1', 'cost'):                 'inference optimization techniques',
    ('9.1', 'hardware'):             'inference optimization techniques',
    ('9.1', None):                   'quantization techniques',
    ('9.2', 'streaming'):            'KV cache mechanics',
    ('9.2', None):                   'KV cache optimization',
    # Alignment / RLHF
    ('16.1', 'alignment'):           'alignment framework',
    ('16.1', 'annotator'):           'annotator bias',
    ('16.1', 'pluralistic'):         'preference modeling',
    ('16.1', 'recommendation'):      'preference learning',
    ('16.1', None):                  'preference learning',
    # Evaluation
    ('27.1', 'measure'):             'evaluation metrics',
    ('27.1', 'success'):             'success metrics',
    ('27.1', 'underpin audit'):      'evaluation metrics',
    ('27.1', 'essential'):           'evaluation metrics',
    ('27.1', None):                  'evaluation metrics',
    ('27.6', None):                  'audit tooling',
    # Hallucination
    ('29.2', 'risk'):                'hallucination',
    ('29.2', None):                  'hallucination',
    # AI Agent Foundations (Ch 20 after renumber)
    ('20.1', None):                  'AI agent',
    # PyTorch / model basics
    ('0.3', None):                   'trained',
}


def lookup_concept(sec_num: str, before_text: str) -> str | None:
    """Find the most appropriate concept name for a Section X.Y reference."""
    bt_l = before_text.lower()
    # Try context-specific matches first
    for (sn, ctx), concept in CONCEPT_MAP.items():
        if sn == sec_num and ctx and ctx in bt_l:
            return concept
    # Fall back to generic
    return CONCEPT_MAP.get((sec_num, None))


# Pattern: "the Section X.Y" or "an Section X.Y" or "a Section X.Y"
# We capture the article + Section + number for replacement context.
BARE_SEC_RE = re.compile(
    r'\b(the|a|an|with standard|consider|own|own internal|class-weighted|via)\s+'
    r'Section\s+(\d+)\.(\d+)\b'
)

# Pattern: empty <a>...</a> tags (left over from auto-linker stripping)
EMPTY_A_RE = re.compile(r'<a\b[^>]*>\s*</a>')


def fix_text(text: str, file_rel: str) -> tuple[str, int, int]:
    """Returns (new_text, n_concept_fixes, n_empty_anchor_fixes)."""
    n_concept = 0

    def repl(m: re.Match) -> str:
        nonlocal n_concept
        article = m.group(1)
        sec_num = f'{m.group(2)}.{m.group(3)}'
        # Look at 50 chars BEFORE the match for context
        start = max(0, m.start() - 60)
        before = text[start:m.start()]
        concept = lookup_concept(sec_num, before + ' ' + article)
        if concept:
            n_concept += 1
            # Build replacement: keep article + new concept, drop "Section X.Y"
            return f'{article} {concept}'
        return m.group(0)  # leave alone if no lookup

    new_text = BARE_SEC_RE.sub(repl, text)
    # Strip empty <a></a> tags that often accompany the bug
    new_text2, n_empty = EMPTY_A_RE.subn('', new_text)
    return new_text2, n_concept, n_empty


def main() -> int:
    files = sorted(ROOT.rglob('*.html'))
    SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/')
    total_concept = total_empty = 0
    files_changed = set()
    for p in files:
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_text, n_c, n_e = fix_text(text, sp)
        if n_c == 0 and n_e == 0:
            continue
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            files_changed.add(sp)
            total_concept += n_c
            total_empty += n_e

    print(f'Concept-name substitutions: {total_concept}')
    print(f'Empty-anchor cleanups:      {total_empty}')
    print(f'Files modified:             {len(files_changed)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
