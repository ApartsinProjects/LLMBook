"""v768: Fix the highest-priority math correctness bugs from the audit.

1. `\$...$` escape that breaks math (sections 9.7, 30.11)
2. L_CLM/L_MLM/L_MTP missing minus signs in section 6.2
3. LayerNorm denominator inconsistency (section 4.1 vs 4.3)
4. Standardize \\Sigma -> \\sum book-wide
5. Plain English in math: top-priority instances
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


total = 0


def patch(p: Path, old: str, new: str, label: str) -> None:
    global total
    if not p.exists():
        print(f'  SKIP missing {p}')
        return
    s = p.read_text(encoding='utf-8')
    if old in s:
        s = s.replace(old, new)
        p.write_text(s, encoding='utf-8')
        total += 1
        print(f'  [{label}] {p.relative_to(ROOT)}')
    else:
        print(f'  [skip {label}: not found] {p.relative_to(ROOT)}')


def regex_patch(p: Path, pat_str: str, rep: str, label: str,
                flags: int = 0) -> None:
    global total
    if not p.exists():
        return
    s = p.read_text(encoding='utf-8')
    new, n = re.subn(pat_str, rep, s, flags=flags)
    if n:
        p.write_text(new, encoding='utf-8')
        total += n
        print(f'  [{label} x{n}] {p.relative_to(ROOT)}')


# 1. Fix escaped-dollar bugs in section 9.7 and 30.11
# Pattern: \$<math content>$  -> $<math content>$
# Be conservative: only inside the specific affected files
for fp in [
    ROOT / 'part-2-understanding-llms/module-09-inference-optimization/section-9.7.html',
    ROOT / 'part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.11.html',
]:
    if not fp.exists():
        continue
    s = fp.read_text(encoding='utf-8')
    # Replace \$...$ where the content is clearly math (contains letters or operators)
    pat = re.compile(r'\\(\$[A-Za-z0-9_\\^{}\(\)\+\-\*\/\.\, ]{1,80}\$)')
    new, n = pat.subn(r'\1', s)
    if n:
        fp.write_text(new, encoding='utf-8')
        total += n
        print(f'  [escaped-dollar fix x{n}] {fp.relative_to(ROOT)}')

# 2. L_CLM, L_MLM, L_MTP missing minus sign in section 6.2
sec62 = ROOT / 'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html'
if sec62.exists():
    patch(sec62,
          '$$L_{CLM} = \\sum_{t=1}^{T} \\log P(x_t | x_{1..t-1}; \\theta)$$',
          '$$L_{CLM} = -\\sum_{t=1}^{T} \\log P(x_t \\mid x_{1..t-1}; \\theta)$$',
          'L_CLM minus')
    # MLM with sum over masked positions
    regex_patch(sec62,
                r'\$\$L_\{MLM\} = \\sum_\{i \\in M\} \\log P\(([^)]+)\)\$\$',
                r'$$L_{MLM} = -\\sum_{i \\in M} \\log P(\1)$$',
                'L_MLM minus')
    # MTP loss (multi-token prediction)
    regex_patch(sec62,
                r'\$\$L_\{MTP\} = \\sum_\{k=1\}\^\{N\} \\sum_\{t=1\}\^\{T-k\} \\log P_k\(([^)]+)\)\$\$',
                r'$$L_{MTP} = -\\sum_{k=1}^{N} \\sum_{t=1}^{T-k} \\log P_k(\1)$$',
                'L_MTP minus')

# 3. LayerNorm denominator: section 4.1 line 459 missing sqrt around sigma^2 + epsilon
sec41 = ROOT / 'part-1-foundations/module-04-transformer-architecture/section-4.1.html'
if sec41.exists():
    patch(sec41,
          '$$\\operatorname{LayerNorm}(x) = \\gamma \\odot (x - \\mu ) / ( \\sigma + \\epsilon ) + \\beta$$',
          '$$\\operatorname{LayerNorm}(x) = \\gamma \\odot \\frac{x - \\mu}{\\sqrt{\\sigma^{2} + \\epsilon}} + \\beta$$',
          'LayerNorm denom')

# Also section 4.3 LayerNorm without epsilon
sec43 = ROOT / 'part-1-foundations/module-04-transformer-architecture/section-4.3.html'
if sec43.exists():
    patch(sec43,
          '$$\\text{LayerNorm}(x) = \\frac{x - \\mu}{\\sigma} \\cdot \\gamma + \\beta',
          '$$\\text{LayerNorm}(x) = \\frac{x - \\mu}{\\sqrt{\\sigma^{2} + \\epsilon}} \\cdot \\gamma + \\beta',
          'LayerNorm 4.3 sqrt')

# 4. Standardize \Sigma -> \sum (in math contexts only)
# Conservative: replace " \Sigma " or "\Sigma_" or "\Sigma\b" inside $$...$$ blocks
def sigma_to_sum_in_file(p: Path) -> int:
    if should_skip(p):
        return 0
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return 0
    # Replace inside math-block divs and inline math spans
    n_total = 0

    def repl_block(m: re.Match) -> str:
        nonlocal n_total
        body = m.group(0)
        # Inside this $$ block, replace \Sigma -> \sum
        new_body, c = re.subn(r'\\Sigma\b', r'\\sum', body)
        n_total += c
        return new_body

    # Both display ($$...$$) and inline ($...$) math
    new_s = re.sub(r'\$\$.*?\$\$', repl_block, s, flags=re.DOTALL)
    new_s = re.sub(r'\$[^$]+\$', repl_block, new_s)
    if new_s != s:
        p.write_text(new_s, encoding='utf-8')
    return n_total


sigma_total = 0
sigma_files = 0
for hp in ROOT.rglob('*.html'):
    if should_skip(hp):
        continue
    n = sigma_to_sum_in_file(hp)
    if n:
        sigma_total += n
        sigma_files += 1
print(f'  [\\Sigma->\\sum: {sigma_total} replacements across {sigma_files} files]')
total += sigma_total

# 5. Plain English in math: top instances
# 5a. section 0.1 line 290: "Total Error = Bias^2 + Variance + Irreducible Noise"
sec01 = ROOT / 'part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html'
if sec01.exists():
    patch(sec01,
          '$$Total Error = Bias^2 + Variance + Irreducible Noise$$',
          '$$\\text{Total Error} = \\text{Bias}^{2} + \\text{Variance} + \\text{Irreducible Noise}$$',
          '0.1 Total Error')

# 5b. section 7.4 line 86: schematic Performance(lang)
sec74 = ROOT / 'part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html'
if sec74.exists():
    patch(sec74,
          '$$Performance(lang) \\propto Data(lang) + Transfer(other_{langs}) - Interference(other_{langs})$$',
          '$$\\text{Performance}(\\text{lang}) \\propto \\text{Data}(\\text{lang}) + \\text{Transfer}(\\text{other languages}) - \\text{Interference}(\\text{other languages})$$',
          '7.4 Performance schematic')

# 5c. section 8.5: optimization schematic
sec85 = ROOT / 'part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html'
if sec85.exists():
    patch(sec85,
          '$$maximize Accuracy(N, T, K) subject to 2 * N * T * K \\leq C$$',
          '$$\\text{maximize}\\;\\; \\text{Accuracy}(N, T, K) \\quad \\text{subject to}\\;\\; 2 \\cdot N \\cdot T \\cdot K \\leq C$$',
          '8.5 maximize schematic')

# 5d. section 1.3 line 347: king - man + woman
sec13 = ROOT / 'part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html'
if sec13.exists():
    patch(sec13,
          '$$king - man + woman \\approx queen$$',
          '$$\\vec{\\text{king}} - \\vec{\\text{man}} + \\vec{\\text{woman}} \\approx \\vec{\\text{queen}}$$',
          '1.3 king-man+woman')

# 5e. section 4.1 line 429 output = SubLayer
patch(sec41,
      '$$output = SubLayer(x) + x$$',
      '$$\\text{output} = \\text{SubLayer}(x) + x$$',
      '4.1 output SubLayer')

# 5f. section 4.3 line 360 Standard:/Linear:
patch(sec43,
      '$$\\begin{aligned}Standard: \\operatorname{softmax}(QK^{T}) V \\; [O(T^{2})] \\\\ \nLinear: \\phi (Q) ( \\phi (K)^{T} V) \\; [O(T)]\\end{aligned}$$',
      '$$\\begin{aligned}\\text{Standard:}\\;\\; & \\operatorname{softmax}(QK^{T}) V \\quad [O(T^{2})] \\\\ \n\\text{Linear:}\\;\\; & \\phi(Q) (\\phi(K)^{T} V) \\quad [O(T)]\\end{aligned}$$',
      '4.3 Standard/Linear schematic')

# 5g. section 5.1 line 281: score(y)
sec51 = ROOT / 'part-1-foundations/module-05-decoding-text-generation/section-5.1.html'
if sec51.exists():
    patch(sec51,
          '$$score(y) = \\log P(y_1,...,y_T) / T^\\alpha$$',
          '$$\\text{score}(y) = \\log P(y_1, \\ldots, y_T) / T^{\\alpha}$$',
          '5.1 score')

# 5h. section 5.3 line 65: score = log P_expert - log P_amateur
sec53 = ROOT / 'part-1-foundations/module-05-decoding-text-generation/section-5.3.html'
if sec53.exists():
    patch(sec53,
          '$$score(x) = \\log P_{expert}(x) - \\log P_{amateur}(x)$$',
          '$$\\text{score}(x) = \\log P_{\\text{expert}}(x) - \\log P_{\\text{amateur}}(x)$$',
          '5.3 score expert/amateur')

# 5i. section 3.2 line 101 softmax_j
sec32 = ROOT / 'part-1-foundations/module-03-sequence-models-attention/section-3.2.html'
if sec32.exists():
    patch(sec32,
          '$$\\alpha_{ij} = softmax_j(e_{ij}) = \\exp(e_{ij}) / \\sum_k \\exp(e_{ik})$$',
          '$$\\alpha_{ij} = \\operatorname{softmax}_j(e_{ij}) = \\frac{\\exp(e_{ij})}{\\sum_k \\exp(e_{ik})}$$',
          '3.2 softmax_j')

# 5j. section 3.3 mask
sec33 = ROOT / 'part-1-foundations/module-03-sequence-models-attention/section-3.3.html'
if sec33.exists():
    patch(sec33,
          '$$mask_{ij} = True \\; \\text{if} \\; j &gt; i \\; (future position)$$',
          '$$\\text{mask}_{ij} = \\text{True} \\;\\text{if}\\; j > i \\;\\text{(future position)}$$',
          '3.3 mask True')

# 5k. section 7.3 line 114: A_i mean/std
sec73 = ROOT / 'part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html'
if sec73.exists():
    patch(sec73,
          '$$A_i = (r_i - mean(r_1,...,r_G)) / std(...)$$',
          '$$A_i = \\frac{r_i - \\operatorname{mean}(r_1, \\ldots, r_G)}{\\operatorname{std}(\\ldots)}$$',
          '7.3 mean/std')

# 5l. section 7.3 UCB(node)
patch(sec73 if sec73.exists() else ROOT,
      '$$\\text{UCB}(node) = V(node) / N(node) + c \\cdot \\sqrt{\\ln N(parent) / N(node)}$$',
      '$$\\text{UCB}(\\text{node}) = \\frac{V(\\text{node})}{N(\\text{node})} + c \\cdot \\sqrt{\\frac{\\ln N(\\text{parent})}{N(\\text{node})}}$$',
      '7.3 UCB plain words')

print(f'\ntotal math fixes: {total}')
