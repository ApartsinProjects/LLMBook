"""Wrap bare English words inside $$...$$ display math with \\text{...}.

The MATH_BARE_TEXT audit flags display-math expressions with bare English
words that should be inside \\text{} (or \\mathrm{}). Example:
   $$Total Error = Bias^{2} + Variance + Irreducible Noise$$
should become:
   $$\\text{Total Error} = \\text{Bias}^{2} + \\text{Variance} + \\text{Irreducible Noise}$$

This script applies the canonical safe transformation: wrap any sequence of
2+ consecutive bare alphabetic words (not preceded by `\\`) in `\\text{...}`,
and convert any standalone bare English word that's clearly NOT a LaTeX
operator into either `\\text{word}` (multi-letter) or itself (single letter
variable names like `x`, `y`, `K`, `N`).

Heuristics (conservative; only fixes obvious cases):
- 2+ consecutive words separated by space (e.g., "Total Error", "context word"):
  wrap the whole phrase in \\text{}.
- A single bare word inside a subscript that looks like part of a variable
  name (e.g., x_{one-hot}, x_{point}): wrap in \\text{}.
- Bare known-operator names (Concat, TopK, Standard, Linear, etc.) when
  not already prefixed with \\: prepend with \\operatorname.

Skips:
- Single-letter variables (a, x, K, etc.).
- Words already inside \\text{}, \\mathrm{}, \\operatorname{}.
- Sub/sup subscripts that look mathematical (single-letter, e.g., `_i`, `_t`).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    '_archive', 'node_modules', '.git', 'pagefind', 'KDP',
    'build', 'vendor', '.claude', '__pycache__', '.book-update',
}

# Display-math span: $$ ... $$ (non-greedy, can span lines)
MATH_BLOCK_RE = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)

# Operator-like names that should become \operatorname. Only put REAL
# math operators here, NOT variable names. Bias, Variance, etc. are
# variable names representing squared-bias / variance terms; they should
# be \text{}-wrapped, not \operatorname{}.
OPERATORS = {
    'Concat', 'TopK', 'Attention', 'MultiHead', 'Softmax', 'LayerNorm',
}

# Words to leave alone (KaTeX commands without backslash; these would
# normally be wrong but may be intentional in some contexts)
KEEP_AS_IS = set()


def wrap_bare_phrases(formula: str) -> tuple[str, int]:
    """Apply transformations to one formula's interior. Returns (new_text, num_fixes)."""
    fixes = 0

    # Step 0: protect existing \text{...}, \mathrm{...}, \operatorname{...}
    # and \begin{...}/\end{...} environment names by replacing with placeholders.
    protected = []

    def stash(m):
        protected.append(m.group(0))
        return f'\x00P{len(protected)-1}\x01'

    # Protect existing wrapped content
    formula_p = re.sub(r'\\(text|mathrm|mathit|mathbf|mathsf|mathtt|operatorname)\{[^}]*\}',
                       stash, formula)
    # Protect \begin{aligned}, \end{aligned}, etc.
    formula_p = re.sub(r'\\(begin|end)\{[^}]+\}', stash, formula_p)
    # Protect LaTeX commands like \alpha, \sum, \frac{}{}, etc.
    formula_p = re.sub(r'\\[A-Za-z]+', stash, formula_p)

    # Step 1: wrap consecutive bare English phrases (2+ words).
    # Pattern: word + space + word, optionally repeated. Only ASCII letters.
    def phrase_repl(m):
        nonlocal fixes
        fixes += 1
        wrapped = r'\text{' + m.group(0) + '}'
        # Protect this newly wrapped phrase so step 2 doesn't touch it.
        protected.append(wrapped)
        return f'\x00P{len(protected)-1}\x01'
    formula_p = re.sub(
        r'\b([A-Za-z][A-Za-z\-]+(?:\s+[A-Za-z][A-Za-z\-]+)+)\b',
        phrase_repl,
        formula_p,
    )

    # Step 2: handle remaining single bare CAPITALIZED multi-letter words.
    # If the word is a known math operator -> \operatorname.
    # Otherwise -> \text{} (likely an English variable name like Bias).
    # Single-letter capitals (K, N, T) are left alone; they're math variables.
    def word_repl(m):
        nonlocal fixes
        word = m.group(0)
        if word in OPERATORS:
            fixes += 1
            return r'\operatorname{' + word + '}'
        # Multi-letter capitalized word, not an operator -> wrap in \text
        if len(word) >= 2 and word[0].isupper():
            fixes += 1
            return r'\text{' + word + '}'
        return word
    formula_p = re.sub(r'\b[A-Z][A-Za-z]+\b', word_repl, formula_p)

    # Step 3: handle bare lowercase multi-letter words that look like English
    # (typically used as variable names where a single letter would be more
    # conventional). Wrap in \text{}. Excludes words that look like LaTeX
    # function names if any reach this step.
    def lower_repl(m):
        nonlocal fixes
        word = m.group(0)
        # Skip if it's a LaTeX command remnant (shouldn't reach here, but defensive)
        if word in {'cos', 'sin', 'tan', 'log', 'exp', 'sqrt', 'sup', 'inf',
                    'min', 'max', 'lim', 'arg', 'det', 'dim', 'gcd', 'pi',
                    'mod', 'div', 'and', 'or', 'not', 'in'}:
            return word
        fixes += 1
        wrapped = r'\text{' + word + '}'
        protected.append(wrapped)
        return f'\x00P{len(protected)-1}\x01'
    # Match 3+ letter lowercase words (2-letter words are too risky: 'as',
    # 'if', 'on', etc. could be valid variable names; we draw the line at 3+).
    # Use letter-boundary lookarounds instead of \b because \b treats `_` as
    # a word char, which would miss "head" in `head_{1}`.
    formula_p = re.sub(r'(?<![A-Za-z])[a-z]{3,}(?![A-Za-z])', lower_repl, formula_p)

    # Step 3: handle bare words in subscripts: x_{point}, x_{one-hot}, zero_{point}
    # The subscript content should be wrapped in \text{}.
    def subscript_repl(m):
        nonlocal fixes
        prefix = m.group(1)  # variable name + _
        content = m.group(2)
        # Skip if content is single letter / digit (e.g., x_i, x_1)
        if len(content) <= 1 or content.isdigit():
            return m.group(0)
        # Skip if content is already a placeholder (was already wrapped)
        if '\x00P' in content:
            return m.group(0)
        # Skip if content looks like a complex LaTeX expression
        if any(c in content for c in '\\{}[]+=^'):
            return m.group(0)
        fixes += 1
        return f'{prefix}{{\\text{{{content}}}}}'
    # Match patterns like `x_{point}`, `zero_{point}`
    formula_p = re.sub(
        r'([A-Za-z_]+_)\{([A-Za-z][\w\-]+)\}',
        subscript_repl,
        formula_p,
    )

    # Restore protected sections
    for i, p in enumerate(protected):
        formula_p = formula_p.replace(f'\x00P{i}\x01', p)

    return formula_p, fixes


SCRIPT_RE = re.compile(r'<script\b.*?</script>', re.DOTALL | re.IGNORECASE)


def fix_file(path: Path, apply: bool) -> int:
    text = path.read_text(encoding='utf-8')
    total_fixes = 0

    # PROTECT all <script>...</script> blocks before running math substitution
    # to avoid matching '$$' inside JS string literals (KaTeX delimiter config).
    scripts = []
    def stash_script(m):
        scripts.append(m.group(0))
        return f'\x00SCRIPT{len(scripts)-1}\x01'
    protected = SCRIPT_RE.sub(stash_script, text)

    def block_repl(m):
        nonlocal total_fixes
        formula = m.group(1)
        new_formula, n = wrap_bare_phrases(formula)
        total_fixes += n
        if new_formula != formula:
            return f'$${new_formula}$$'
        return m.group(0)

    new_text = MATH_BLOCK_RE.sub(block_repl, protected)
    # Restore scripts
    for i, sc in enumerate(scripts):
        new_text = new_text.replace(f'\x00SCRIPT{i}\x01', sc)
    if total_fixes and apply:
        path.write_text(new_text, encoding='utf-8')
    return total_fixes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--files', nargs='+', help='specific files')
    args = ap.parse_args()
    if args.files:
        paths = [Path(f) for f in args.files]
    else:
        paths = [p for p in ROOT.rglob('section-*.html')
                 if not any(s in p.parts for s in SKIP_DIRS)]
    total = 0
    for p in paths:
        n = fix_file(p, args.apply)
        if n:
            try:
                rel = p.relative_to(ROOT)
            except ValueError:
                rel = p
            print(f"  {rel}: {n} fix(es)")
            total += n
    print(f"\nTotal: {total} fixes {'applied' if args.apply else 'would apply (dry run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == '__main__':
    main()
