"""Wave 45: Section ordering fixes.

Swap prerequisites and big-picture in the 7 files where they appear in the
wrong order. The canonical order is epigraph -> big-picture -> prerequisites,
but these files have prerequisites first.

Strategy: extract both blocks, swap their positions.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    'part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.5.html',
    'part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.6.html',
    'part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html',
    'part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html',
    'part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html',
    'part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html',
    'part-1-llm-building-blocks/module-03-transformer-architecture/section-3.6.html',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.3.html',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.4.html',
]

# Patterns to match the wrapper divs
PREREQ_RE = re.compile(
    r'<div\s+class="prerequisites">.*?</div>\s*(?=<|$)',
    re.DOTALL | re.IGNORECASE,
)
BIGPIC_RE = re.compile(
    r'<div\s+class="callout big-picture">.*?</div>\s*</div>\s*(?=<|$)',
    re.DOTALL | re.IGNORECASE,
)


def swap_in_file(p: Path) -> bool:
    text = p.read_text(encoding='utf-8')
    prereq_m = PREREQ_RE.search(text)
    bigpic_m = BIGPIC_RE.search(text)
    if not prereq_m or not bigpic_m:
        return False
    # Ensure prerequisites comes before big-picture
    if prereq_m.start() > bigpic_m.start():
        return False  # already correct
    prereq_block = prereq_m.group()
    bigpic_block = bigpic_m.group()
    # Build new text: replace prereq with bigpic, and replace bigpic with prereq
    # We work right-to-left to keep offsets valid.
    new_text = (
        text[:prereq_m.start()]
        + bigpic_block
        + text[prereq_m.end():bigpic_m.start()]
        + prereq_block
        + text[bigpic_m.end():]
    )
    p.write_text(new_text, encoding='utf-8')
    return True


def main():
    n_swapped = 0
    for rel in FILES:
        p = ROOT / rel
        if not p.exists():
            print(f'  SKIP (no file): {rel}')
            continue
        ok = swap_in_file(p)
        if ok:
            n_swapped += 1
            print(f'  SWAPPED: {rel}')
        else:
            print(f'  NO CHANGE: {rel}')
    print(f'\nTotal swapped: {n_swapped}')


if __name__ == '__main__':
    main()
