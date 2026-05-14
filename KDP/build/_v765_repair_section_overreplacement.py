"""v765: Repair regex over-replacement that turned topic nouns into "Section X.Y".

A previous editorial pass (probably a glossary auto-link or section-link
decorator) replaced topic nouns with literal "Section X.Y" strings,
e.g. "RLHF" -> "Section 17.1", "BERT" -> "Section 6.1", "Multi-agent" ->
"Multi-Section 21.1", "sentence-transformers" -> "sentence-Section 4.1",
"chain-of-thought" -> "Section 8.1", "hallucination" -> "Section 30.2",
"Layer Normalization" tooltip -> "Glossary: Section 4.1".

This script reverts the highest-confidence corrupted spots back to the
intended noun. Each rule is conservative: it requires the corrupted
context to be unambiguous (preceding/following words pin the topic).

Idempotent.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('KDP/build/source_fix_backups', 'pagefind', 'node_modules',
        'temp_epub', '.git', 'venv')


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# (regex, replacement, description)
RULES = [
    # "Multi-Section 21.1" -> "Multi-agent" (only valid in agentic-AI context)
    (re.compile(r'\bMulti-Section \d+\.\d+\b'),
     'Multi-agent',
     'Multi-Section X.Y -> Multi-agent'),

    # "sentence-Section 4.1" -> "sentence-transformers"
    (re.compile(r'\bsentence-Section \d+\.\d+\b'),
     'sentence-transformers',
     'sentence-Section X.Y -> sentence-transformers'),

    # 'title="Glossary: Section 4.1"' inside a glossary-link anchor for
    # what was Layer Normalization. Don't touch href; only fix tooltip
    # title for the specific case where the anchor TEXT is "Section 4.1".
    # Conservative: replace only when adjacent anchor text is also wrong.
    (re.compile(
        r'<a class="glossary-link" href="([^"]+)" title="Glossary: '
        r'Section \d+\.\d+">Section \d+\.\d+</a>'),
     r'<a class="glossary-link" href="\1" title="Glossary: Layer '
     r'Normalization">layer normalization</a>',
     'glossary-link "Section 4.1" -> layer normalization'),

    # "<word>-Section X.Y-style" -> "<word>-style" (preserve hyphenation
    # context). Most common: "BERT-style" became "Section 6.1-style".
    # Convert to "BERT-style" since that's the only known case.
    (re.compile(r'\bSection 6\.1-style\b'),
     'BERT-style',
     'Section 6.1-style -> BERT-style'),

    # Phrases:
    # "Section 6.1 cross-encoders" -> "BERT cross-encoders"
    (re.compile(r'\bSection 6\.1 cross-encoders\b'),
     'BERT cross-encoders',
     'Section 6.1 cross-encoders -> BERT cross-encoders'),

    # "Section 6.1 (BERT)" pattern is OK; we don't touch generic "Section 6.1".

    # "Section 17.1 alignment" -> "RLHF alignment"
    (re.compile(r'\bSection 17\.1 alignment\b'),
     'RLHF alignment',
     'Section 17.1 alignment -> RLHF alignment'),

    # "Section 17.1 pretraining" -> "Contrastive pretraining"
    # (multimodal context: CLIP-style contrastive pretraining)
    (re.compile(r'\bSection 17\.1 pretraining\b'),
     'Contrastive pretraining',
     'Section 17.1 pretraining -> Contrastive pretraining'),

    # "Section 17.1 failures" -> "alignment failures"
    (re.compile(r'\bSection 17\.1 failures\b'),
     'alignment failures',
     'Section 17.1 failures -> alignment failures'),

    # "Section 17.1-style" -> "RLHF-style"
    (re.compile(r'\bSection 17\.1-style\b'),
     'RLHF-style',
     'Section 17.1-style -> RLHF-style'),

    # "GRPO vs. Section 17.1" -> "GRPO vs. PPO"
    (re.compile(r'\bGRPO vs\.\s*Section 17\.1\b'),
     'GRPO vs. PPO',
     'GRPO vs. Section 17.1 -> GRPO vs. PPO'),

    # "REINFORCE or Section 17.1 work" -> "REINFORCE or PPO work"
    (re.compile(r'\bREINFORCE or Section 17\.1 work\b'),
     'REINFORCE or PPO work',
     'REINFORCE or Section 17.1 -> REINFORCE or PPO'),

    # "Section 8.1 reasoning" -> "chain-of-thought reasoning"
    (re.compile(r'\bSection 8\.1 reasoning\b'),
     'chain-of-thought reasoning',
     'Section 8.1 reasoning -> chain-of-thought reasoning'),

    # "Section 30.2" used as a noun for "hallucination" topic
    # Pattern: "(Section 30.2)" alone parenthetically is a real cross-ref;
    # only touch it when it is the predicate of a sentence about risk/risk types.
    (re.compile(r'\bThe primary risk is Section 30\.2\b'),
     'The primary risk is hallucination',
     'Section 30.2 -> hallucination (risk context)'),
    (re.compile(r'\btoxicity, Section 30\.2\b'),
     'toxicity, hallucination',
     'Section 30.2 -> hallucination (toxicity list)'),

    # "Section 6.1 data quality audit" -> "Pre-training data quality audit"
    (re.compile(r'\bSection 6\.1 data quality audit\b'),
     'Pre-training data quality audit',
     'Section 6.1 data quality audit -> Pre-training data quality audit'),

    # "Section 6.1, GPT encoder/decoder" -> "BERT, GPT encoder/decoder"
    (re.compile(r'\bSection 6\.1, GPT encoder/decoder\b'),
     'BERT, GPT encoder/decoder',
     'Section 6.1, GPT encoder/decoder -> BERT, GPT encoder/decoder'),

    # "Original Transformer, Section 6.1" -> "Original Transformer, BERT"
    (re.compile(r'\bOriginal Transformer, Section 6\.1\b'),
     'Original Transformer, BERT',
     'Original Transformer, Section 6.1 -> Original Transformer, BERT'),

    # "Pioneering work on using Section 6.1 cross-encoders" already covered

    # "tokenization and Section 17.1" -> "tokenization and modality fusion"
    (re.compile(r'\btokenization and Section 17\.1\b'),
     'tokenization and modality fusion',
     'tokenization and Section 17.1 -> tokenization and modality fusion'),

    # "<chapter ref> covers Section 17.1 alignment" already covered

    # bibliography "Section 17.1 alignment, and safety" -> "RLHF alignment, and safety"
    # already covered by "Section 17.1 alignment" rule above

    # "Section 8.1, alignment" specifically in a "data collection ..." list -> "pre-training, alignment"
    (re.compile(r'\bdata collection, Section 6\.1, alignment\b'),
     'data collection, pre-training, alignment',
     'data collection, Section 6.1, alignment -> data collection, pre-training, alignment'),

    # "Section 4.1-minimizing" -> "Loss-minimizing" (clearly the loss context)
    (re.compile(r'\bSection 4\.1-minimizing\b'),
     'Loss-minimizing',
     'Section 4.1-minimizing -> Loss-minimizing'),

    # "Tasks like arithmetic, Section 8.1 reasoning" already partially handled
    # by the chain-of-thought rule above; but ", Section 8.1 reasoning" without
    # leading "and" stands - covered by "Section 8.1 reasoning" rule.

    # "self-reflection, Section 8.1 reasoning" already covered by 8.1 rule

    # "few-shot examples, Section 8.1" -> "few-shot examples, chain-of-thought"
    (re.compile(r'\bfew-shot examples, Section 8\.1\b'),
     'few-shot examples, chain-of-thought',
     'few-shot examples, Section 8.1 -> few-shot examples, chain-of-thought'),

    # "data collection, pre-training, alignment" already handled

    # "supports both supervised fine-tuning and Section 17.1-style tuning"
    # is covered by Section 17.1-style rule.
]

n_files = 0
counts = {desc: 0 for _, _, desc in RULES}
total = 0
for p in ROOT.rglob('*.html'):
    if should_skip(p):
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    new = s
    file_count = 0
    for pat, rep, desc in RULES:
        new2, c = pat.subn(rep, new)
        if c:
            counts[desc] += c
            file_count += c
            new = new2
    if new != s:
        p.write_text(new, encoding='utf-8')
        n_files += 1
        total += file_count

print(f'Repairs: {total} across {n_files} files')
for desc, c in counts.items():
    print(f'  {c:>4}  {desc}')
