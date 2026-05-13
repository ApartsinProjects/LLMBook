"""Fix bare English text inside $$...$$ math blocks by wrapping multi-word
phrases in \\text{}.

CONSERVATIVE STRATEGY:
- Only rewrites contiguous runs of 2+ bare English words (4+ letters each)
  separated by single spaces. These are almost certainly labels, not
  juxtaposed variables. Example:
    $$Accept probability = ...$$ -> $$\\text{Accept probability} = ...$$
    $$tokens per cycle = ...$$    -> $$\\text{tokens per cycle} = ...$$
- Also rewrites a few SINGLE-word bare identifiers from a high-confidence
  list (specific labels like "VRAM", "Speedup", "Perplexity") that are
  unambiguous.
- Does NOT touch math content inside \\text{}, \\mathrm{}, \\operatorname{},
  or after a backslash (which is a LaTeX command).
- Does NOT touch inline math <span class="math">$...$</span>; only
  display $$...$$ blocks.

Idempotent.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

DISPLAY_MATH = re.compile(r'(\$\$)([\s\S]*?)(\$\$)')

# A bare English-letter word, 4+ chars
WORD = r'[A-Za-z][A-Za-z]{3,}'

# High-confidence single-word labels that are unambiguous
KNOWN_LABELS = (
    'VRAM', 'Speedup', 'Perplexity', 'Accuracy', 'Bandwidth', 'Throughput',
    'Latency', 'Recall', 'Precision', 'Coverage', 'Memory', 'Bytes',
    'Parameters', 'Tokens', 'Capacity', 'Compute', 'Storage',
)

# Patterns that should NEVER be inside text (LaTeX commands)
LATEX_TOKEN = re.compile(r'\\[a-zA-Z]+')


def fix_math_block(math: str) -> str:
    """Inside a math expression, find bare multi-word phrases and wrap
    them in \\text{}. Skips content already inside \\text/\\mathrm/etc."""

    # Mask out content inside \cmd{...} commands (one level of nesting).
    # We use placeholder substitution so the regex below doesn't see
    # already-wrapped text.
    placeholders: list[str] = []
    SAFE_CMD = re.compile(
        r'\\(?:text|mathrm|mathbb|mathcal|mathbf|operatorname|textbf|textit|'
        r'textrm|texttt|mbox)\{[^{}]*\}')

    def stash(m: re.Match) -> str:
        idx = len(placeholders)
        placeholders.append(m.group(0))
        return f'\x00P{idx}P\x00'

    masked = SAFE_CMD.sub(stash, math)

    # Find runs of 2+ bare words separated by single spaces.
    # The negative lookbehind for `\` ensures we're not after a LaTeX
    # command character.
    MULTI_WORD = re.compile(
        rf'(?<![\\\w])({WORD}(?:\s+{WORD})+)(?!\w)')

    def wrap_multi(m: re.Match) -> str:
        phrase = m.group(1)
        # Don't wrap if it contains backslash-introduced commands
        # (which the mask removed).
        return f'\\text{{{phrase}}}'

    masked = MULTI_WORD.sub(wrap_multi, masked)

    # Then wrap single known labels
    for label in KNOWN_LABELS:
        # Only wrap if it's a standalone word AND not already preceded by
        # \text or similar
        pat = re.compile(rf'(?<![\\\w])({re.escape(label)})(?!\w)')
        masked = pat.sub(rf'\\text{{\1}}', masked)

    # Restore masked commands
    def unstash(m: re.Match) -> str:
        idx = int(m.group(1))
        return placeholders[idx]
    unmasked = re.sub(r'\x00P(\d+)P\x00', unstash, masked)

    return unmasked


def process_file(text: str) -> tuple[str, int]:
    n_fixed = 0

    def replace_block(m: re.Match) -> str:
        nonlocal n_fixed
        before, body, after = m.group(1), m.group(2), m.group(3)
        new_body = fix_math_block(body)
        if new_body != body:
            n_fixed += 1
        return before + new_body + after

    return DISPLAY_MATH.sub(replace_block, text), n_fixed


def main() -> int:
    fix = '--fix' in sys.argv
    n_files = 0
    n_blocks = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_text, local = process_file(text)
        if local:
            n_files += 1
            n_blocks += local
            if fix and new_text != text:
                p.write_text(new_text, encoding='utf-8')
    print(f'Files {"fixed" if fix else "needing fix"}: {n_files}')
    print(f'Math blocks rewritten: {n_blocks}')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
