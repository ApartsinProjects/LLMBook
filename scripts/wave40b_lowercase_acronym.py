"""Wave 40b: Fix lowercase acronym anchor text + cosmetic cleanups.

Patterns (from random_detector findings):
1. Anchor text "llm apis" (should be "LLM APIs")
2. Anchor text "rag" or "Rag" (should be "RAG")
3. Anchor text "dpo" / "rlhf" / "peft" / "lora" in lowercase (should be uppercase)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Anchor text only (between <a...>...</a>) — case-sensitive lowercase to upper
# Limit to specific anchor patterns to avoid mass-rewriting prose.
PATTERNS = [
    (re.compile(r'(<a [^>]*>)llm apis(</a>)', re.IGNORECASE), r'\1LLM APIs\2'),
    (re.compile(r'(<a [^>]*>)llm api(</a>)', re.IGNORECASE), r'\1LLM API\2'),
    # "rag" as anchor text when entirely lowercase (not "RAG")
    (re.compile(r'(<a [^>]*>)rag(</a>)'), r'\1RAG\2'),
    (re.compile(r'(<a [^>]*>)rlhf(</a>)'), r'\1RLHF\2'),
    (re.compile(r'(<a [^>]*>)dpo(</a>)'), r'\1DPO\2'),
    (re.compile(r'(<a [^>]*>)peft(</a>)'), r'\1PEFT\2'),
    (re.compile(r'(<a [^>]*>)lora(</a>)'), r'\1LoRA\2'),
    (re.compile(r'(<a [^>]*>)qlora(</a>)'), r'\1QLoRA\2'),
    (re.compile(r'(<a [^>]*>)moe(</a>)'), r'\1MoE\2'),
    (re.compile(r'(<a [^>]*>)mcp(</a>)'), r'\1MCP\2'),
    (re.compile(r'(<a [^>]*>)kv cache(</a>)', re.IGNORECASE), r'\1KV cache\2'),
]


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        for pat, replacement in PATTERNS:
            new = pat.sub(replacement, text)
            if new != text:
                n_total += len(pat.findall(text))
                text = new
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'Fixed {n_total} lowercase acronym anchors across {n_files} files')


if __name__ == '__main__':
    main()
