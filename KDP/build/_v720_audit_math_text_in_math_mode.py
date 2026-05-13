"""Audit math blocks for English words written in raw math mode without
\\text{} wrapping. Such words render as concatenated italic single-letter
variables: "Accept probability" becomes "Acceptprobability" with each
letter as a separate variable, no spacing, no readability.

Two patterns flagged:
  M1: $$ block contains a multi-letter run of A-Z/a-z OUTSIDE \\text{},
      \\mathrm{}, \\mathbb{}, \\mathcal{}, \\mathbf{}, \\operatorname{},
      and not a known TeX command, AND not a recognized math identifier.
  M2: $...$ inline math with the same problem.

Read-only audit. Reports each occurrence with file:line + offending word.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

# Known LaTeX commands we should NOT flag (a non-exhaustive list of common ones).
LATEX_COMMANDS = {
    'frac', 'sqrt', 'sum', 'prod', 'int', 'lim', 'log', 'ln', 'exp',
    'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'arcsin', 'arccos', 'arctan',
    'min', 'max', 'inf', 'sup', 'argmin', 'argmax', 'gcd', 'det', 'tr',
    'dim', 'ker', 'rank',
    'mathbb', 'mathbf', 'mathcal', 'mathrm', 'mathfrak', 'mathit', 'mathsf',
    'mathtt', 'mathnormal', 'boldsymbol', 'symbf', 'text', 'textbf',
    'textit', 'textrm', 'textsf', 'texttt',
    'operatorname', 'tilde', 'hat', 'bar', 'vec', 'dot', 'ddot', 'overline',
    'underline', 'overbrace', 'underbrace', 'widetilde', 'widehat',
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'varepsilon', 'zeta',
    'eta', 'theta', 'vartheta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi',
    'pi', 'varpi', 'rho', 'varrho', 'sigma', 'varsigma', 'tau', 'upsilon',
    'phi', 'varphi', 'chi', 'psi', 'omega',
    'Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta',
    'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Pi', 'Rho', 'Sigma',
    'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega',
    'partial', 'nabla', 'infty', 'forall', 'exists', 'in', 'notin', 'ni',
    'subset', 'supset', 'subseteq', 'supseteq', 'cup', 'cap', 'setminus',
    'emptyset', 'varnothing',
    'leq', 'geq', 'neq', 'le', 'ge', 'ne', 'sim', 'approx', 'equiv',
    'cong', 'simeq', 'propto', 'mapsto', 'to', 'rightarrow', 'leftarrow',
    'leftrightarrow', 'Rightarrow', 'Leftarrow', 'Leftrightarrow',
    'cdot', 'times', 'div', 'pm', 'mp', 'star', 'ast', 'circ', 'bullet',
    'oplus', 'ominus', 'otimes', 'odot', 'wedge', 'vee', 'oslash',
    'left', 'right', 'big', 'Big', 'bigg', 'Bigg',
    'sum_', 'prod_', 'int_',
    'quad', 'qquad', 'space',
    'mathopen', 'mathclose', 'mathbin', 'mathord', 'mathrel', 'mathpunct',
    'displaystyle', 'textstyle', 'scriptstyle', 'scriptscriptstyle',
    'rm', 'bf', 'it', 'sf', 'tt', 'sl', 'em',
    'begin', 'end', 'pmatrix', 'bmatrix', 'vmatrix', 'matrix', 'cases',
    'aligned', 'align', 'array', 'gathered', 'split',
    'top', 'bot', 'bigcup', 'bigcap', 'bigoplus', 'bigotimes',
    'Pr', 'sgn', 'Var', 'Cov', 'argmax', 'argmin', 'softmax', 'sigmoid',
    'mathring', 'dagger', 'ddagger',
    'mod', 'pmod', 'bmod',
    'hline', 'vline', 'cline', 'cdots', 'ldots', 'vdots', 'ddots',
    'newline', 'cr', 'over', 'choose', 'binom',
    'color', 'textcolor',
}

# Recognized 3-4-letter math identifiers commonly used (KL, NLL, etc).
SHORT_IDENTIFIERS = {
    'NaN', 'KL', 'JS', 'NLL', 'MSE', 'MAE', 'BCE', 'CE', 'BLEU', 'ROUGE',
    'PPL', 'AUC', 'ROC', 'FLOPs', 'CDF', 'PDF', 'PMF', 'iid', 'iid.', 'TV',
    'GPU', 'TPU', 'CPU', 'NN', 'CNN', 'RNN', 'LLM', 'MLP', 'GRU', 'LSTM',
    'BERT', 'GPT', 'KV', 'Q', 'K', 'V', 'O', 'NA', 'Acc', 'Cost', 'Value',
}

# Pattern: a run of >=4 letters not preceded by a backslash
SUSPICIOUS_WORD = re.compile(r'(?<![\\a-zA-Z])([A-Za-z]{4,})')

# Math block extraction
DISPLAY_MATH = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
INLINE_MATH = re.compile(r'(?<!\$)\$([^\$\n]+?)\$(?!\$)')


def strip_safe_contexts(math: str) -> str:
    """Strip out content inside \\text{}, \\mathrm{}, \\mathbb{}, etc.,
    AND escape-sequences like \\command, so that what remains is the
    'risky' bare math content."""
    # Strip recursive {...} after \text, \mathrm, etc.
    def strip_braced(s: str, cmd: str) -> str:
        # Replace \cmd{...} with empty string (only one level of nesting)
        pat = re.compile(rf'\\{cmd}\{{[^{{}}]*\}}')
        prev = None
        while prev != s:
            prev = s
            s = pat.sub(' ', s)
        return s

    for cmd in ('text', 'mathrm', 'mathbb', 'mathcal', 'mathbf', 'mathfrak',
                'mathit', 'mathsf', 'mathtt', 'mathnormal', 'operatorname',
                'textbf', 'textit', 'textrm', 'texttt', 'mbox',
                'boldsymbol', 'symbf'):
        math = strip_braced(math, cmd)
    # Strip remaining \command tokens (now just bare commands)
    math = re.sub(r'\\[a-zA-Z]+\*?', ' ', math)
    return math


def find_offending_words(math: str) -> list[str]:
    cleaned = strip_safe_contexts(math)
    out: list[str] = []
    for m in SUSPICIOUS_WORD.finditer(cleaned):
        word = m.group(1)
        if word in SHORT_IDENTIFIERS:
            continue
        out.append(word)
    return out


def main() -> int:
    n_files = 0
    n_blocks = 0
    by_file: dict[str, list[tuple[int, str, str]]] = {}
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        # Strip <script> and <style> blocks so we don't pick up JavaScript
        # string literals containing $ characters (KaTeX auto-render config).
        text = re.sub(r'<script\b[\s\S]*?</script>', ' ', text,
                      flags=re.IGNORECASE)
        text = re.sub(r'<style\b[\s\S]*?</style>', ' ', text,
                      flags=re.IGNORECASE)
        # Also strip <pre> / <code> blocks (code displays may have $).
        text = re.sub(r'<pre\b[\s\S]*?</pre>', ' ', text, flags=re.IGNORECASE)
        text = re.sub(r'<code\b[\s\S]*?</code>', ' ', text, flags=re.IGNORECASE)
        file_hits: list[tuple[int, str, str]] = []
        for m in DISPLAY_MATH.finditer(text):
            math = m.group(1)
            words = find_offending_words(math)
            if words:
                line = text.count('\n', 0, m.start()) + 1
                file_hits.append((line, 'display', ', '.join(words[:5])))
                n_blocks += 1
        for m in INLINE_MATH.finditer(text):
            math = m.group(1)
            words = find_offending_words(math)
            if words:
                line = text.count('\n', 0, m.start()) + 1
                file_hits.append((line, 'inline', ', '.join(words[:5])))
                n_blocks += 1
        if file_hits:
            n_files += 1
            by_file[str(p.relative_to(ROOT))] = file_hits
    print(f'Files with suspect math: {n_files}')
    print(f'Total suspect math blocks: {n_blocks}')
    for fp in sorted(by_file.keys()):
        print(f'\n{fp}:')
        for line, kind, words in by_file[fp][:10]:
            print(f'  L{line:<5} {kind:8s} offending words: {words}')
        if len(by_file[fp]) > 10:
            print(f'  ... and {len(by_file[fp])-10} more')
    return 0


if __name__ == '__main__':
    sys.exit(main())
