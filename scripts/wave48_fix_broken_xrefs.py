"""Wave 48: Fix specific broken cross-references identified by the audit.

Maps stale paths (which referenced module names that have since been renamed
or that never existed) to current canonical paths.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Replacements: (old_substring, new_substring)
REPLACEMENTS = [
    # Bias-fairness was in module-54 but got renumbered to module-52
    ('part-11-llm-ethics-trust-governance/module-54-bias-fairness/',
     'part-11-llm-ethics-trust-governance/module-52-bias-fairness/'),
    # Procurement module name shifted
    ('part-13-llmops-lifecycle/module-66-procurement-and-vendor-selection/',
     'part-13-llmops-lifecycle/module-66-reliability-slos-registry/'),
    # Instruction tuning RLHF moved
    ('part-4-training-adaptation/module-21-instruction-tuning-rlhf/',
     'part-4-training-adaptation/module-18-alignment-rlhf-dpo/'),
    # Prompt design module renamed
    ('part-3-prompt-design-context-engineering/module-13-prompt-design/',
     'part-3-working-with-llms/module-12-prompt-engineering/'),
    # Misuse module renamed to guardrails
    ('part-10-llm-security-runtime-safety/module-48-llm-misuse-malicious-use/',
     'part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/'),
    # Wave 16: fix structural-gap agent's incorrect module names
    ('part-3-working-with-llms/module-13-llm-fine-tuning/',
     'part-4-training-adaptation/module-16-fine-tuning-fundamentals/'),
    ('part-1-llm-building-blocks/module-02-attention-transformers/',
     'part-1-llm-building-blocks/module-02-sequence-models-attention/'),
    ('part-4-training-adaptation/module-20-rlhf-alignment/',
     'part-4-training-adaptation/module-18-alignment-rlhf-dpo/'),
]


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        n_file = 0
        for old, new in REPLACEMENTS:
            new_text = text.replace(old, new)
            if new_text != text:
                n_file += text.count(old)
                text = new_text
        if text != orig:
            p.write_text(text, encoding='utf-8')
            files_touched += 1
            n_total += n_file
    print(f'Broken xrefs fixed: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
