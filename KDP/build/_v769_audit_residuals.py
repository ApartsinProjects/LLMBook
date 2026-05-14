"""v769: Sweep remaining plain-English-in-math + audit residuals.

Targets:
1. Plain English words inside $...$ or $$...$$ (wrap with \\text{} or \\operatorname{}).
2. Schematic equations rendered as italic letter products.
3. Bare $$ blocks not wrapped in <div class="math-block">.
4. Anchor-text-vs-href Section X.Y mismatches.
5. Cards A-V missing "Read Appendix X →" link.

Conservative: only touch high-confidence patterns.
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


# Known function names / operators that should be \operatorname{} not bare letters
OPERATORS = ['softmax', 'sigmoid', 'relu', 'gelu', 'silu', 'tanh',
             'mean', 'std', 'var', 'max', 'min', 'argmax', 'argmin',
             'log', 'exp', 'softplus', 'logsumexp',
             'cos', 'sin', 'tan', 'sqrt',
             'score', 'output', 'logits', 'mask', 'expert', 'amateur',
             'parent', 'node', 'rank', 'rmse', 'norm']

# Specific multi-line patterns: english words bare in math
PATCHES = [
    # section 4.1 LayerNorm in math-block (already partly fixed)
    # section 5.1 score(y)
    ('part-1-foundations/module-05-decoding-text-generation/section-5.1.html',
     '$$score(y) = \\log P(y_{1},...,y_{T}) / T^{ \\alpha }$$',
     '$$\\text{score}(y) = \\log P(y_1, \\ldots, y_T) / T^{\\alpha}$$',
     '5.1 score(y)'),

    # section 5.2 V_p smallest set
    ('part-1-foundations/module-05-decoding-text-generation/section-5.2.html',
     '$$V_{p} = smallest set such that \\Sigma _{x \\in Vp} P(x) \\geq p$$',
     '$$V_{p} = \\text{smallest set such that}\\;\\sum_{x \\in V_p} P(x) \\geq p$$',
     '5.2 V_p smallest'),
    ('part-1-foundations/module-05-decoding-text-generation/section-5.2.html',
     '$$V_{p} = \\text{smallest set such that} \\Sigma _{x \\in V_p} P(x) \\geq p$$',
     '$$V_{p} = \\text{smallest set such that}\\;\\sum_{x \\in V_p} P(x) \\geq p$$',
     '5.2 V_p smallest alt'),

    # section 5.2 Keep token x_i
    ('part-1-foundations/module-05-decoding-text-generation/section-5.2.html',
     '$$Keep token x_{i} \\text{if} P(x_{i}) \\geq min_{p} \\times max_{j} P(x_{j})$$',
     '$$\\text{Keep token}\\; x_{i}\\;\\text{if}\\; P(x_{i}) \\geq \\text{min}_{p} \\times \\max_{j} P(x_{j})$$',
     '5.2 Keep token'),

    # section 3.2 softmax_j
    ('part-1-foundations/module-03-sequence-models-attention/section-3.2.html',
     '$$\\alpha_{ij} = softmax_{j}(e_{ij}) = \\exp(e_{ij}) / \\Sigma _{k} \\exp(e_{ik})$$',
     '$$\\alpha_{ij} = \\operatorname{softmax}_j(e_{ij}) = \\frac{\\exp(e_{ij})}{\\sum_k \\exp(e_{ik})}$$',
     '3.2 softmax_j operator'),

    # section 3.1 Jacobian matrix
    ('part-1-foundations/module-03-sequence-models-attention/section-3.1.html',
     '$$J = [[ \\partial f_{1}/\\partial x_{1}, ... ], ...] = [[2,1],[6,3]]$$',
     '$$J = \\begin{bmatrix} \\partial f_1/\\partial x_1 & \\partial f_1/\\partial x_2 \\\\ \\partial f_2/\\partial x_1 & \\partial f_2/\\partial x_2 \\end{bmatrix} = \\begin{bmatrix} 2 & 1 \\\\ 6 & 3 \\end{bmatrix}$$',
     '3.1 Jacobian matrix'),

    # section 4.3 output = (U \odot AttentionOutput(V)) W_o
    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     '$$output = (U \\odot AttentionOutput(V)) W_{o}$$',
     '$$\\text{output} = (U \\odot \\text{AttentionOutput}(V)) W_{o}$$',
     '4.3 output AttentionOutput'),

    # section 4.3 RoPE
    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     '$$\\text{RoPE}(x, pos)_{2i} = x_{2i} \\cos(pos \\cdot \\theta_i) - x_{2i+1} \\sin(pos \\cdot \\theta_i)$$',
     '$$\\text{RoPE}(x, \\text{pos})_{2i} = x_{2i} \\cos(\\text{pos} \\cdot \\theta_i) - x_{2i+1} \\sin(\\text{pos} \\cdot \\theta_i)$$',
     '4.3 RoPE pos'),
    ('part-1-foundations/module-04-transformer-architecture/section-4.3.html',
     '$$\\text{RoPE}(x, pos)_{2i+1} = x_{2i} \\sin(pos \\cdot \\theta_i) + x_{2i+1} \\cos(pos \\cdot \\theta_i)$$',
     '$$\\text{RoPE}(x, \\text{pos})_{2i+1} = x_{2i} \\sin(\\text{pos} \\cdot \\theta_i) + x_{2i+1} \\cos(\\text{pos} \\cdot \\theta_i)$$',
     '4.3 RoPE pos +1'),

    # section 18.4 Number of chunks: N = ...
    ('part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.4.html',
     '$$Number of chunks: N = \\lceil \\frac{L_{doc} - C}{C - O} \\rceil + 1$$',
     '$$\\text{Number of chunks:}\\; N = \\left\\lceil \\frac{L_{\\text{doc}} - C}{C - O} \\right\\rceil + 1$$',
     '18.4 Number of chunks'),

    # section 33.3 TopK = argtop-k(g(x))
    ('part-10-frontiers/module-33-emerging-architectures/section-33.3.html',
     '$$TopK = argtop-k(g(x))$$',
     '$$\\text{TopK} = \\operatorname{arg\\,topk}(g(x))$$',
     '33.3 TopK'),
    ('part-10-frontiers/module-33-emerging-architectures/section-33.3.html',
     '$$Expert_i(x) = \\text{FFN}_i(x)$$',
     '$$\\text{Expert}_i(x) = \\text{FFN}_i(x)$$',
     '33.3 Expert_i'),

    # section 7.3 ORM/PRM schematic
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html',
     '$$ORM: R(problem, full\\_solution)$$',
     '$$\\text{ORM:}\\; R(\\text{problem}, \\text{full solution})$$',
     '7.3 ORM schematic'),

    # section 4.4 arithmetic intensity
    ('part-1-foundations/module-04-transformer-architecture/section-4.4.html',
     '$$Arithmetic Intensity = FLOPs / Bytes transferred$$',
     '$$\\text{Arithmetic Intensity} = \\text{FLOPs} / \\text{Bytes transferred}$$',
     '4.4 Arithmetic Intensity'),

    # section 5.3 (1/|S|)
    ('part-1-foundations/module-05-decoding-text-generation/section-5.3.html',
     '$$\\text{score}(x) = (1/|S|) \\sum_{x_i \\in S} \\log P(x_i | x_{<i})$$',
     '$$\\text{score}(x) = \\frac{1}{|S|} \\sum_{x_i \\in S} \\log P(x_i \\mid x_{<i})$$',
     '5.3 score 1/|S|'),

    # section 6.6 L_aux normalization (reconcile with 6.3)
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html',
     '$$\\mathcal{L}_{aux} = \\alpha \\cdot N \\sum f_i \\cdot p_i$$',
     '$$\\mathcal{L}_{aux} = \\alpha \\cdot N \\cdot \\sum_{i=1}^{N} f_i \\cdot p_i$$',
     '6.6 L_aux'),
]

total = 0
for rel, old, new, label in PATCHES:
    p = ROOT / rel
    if not p.exists():
        print(f'  SKIP missing {rel}')
        continue
    s = p.read_text(encoding='utf-8')
    if old in s:
        s = s.replace(old, new)
        p.write_text(s, encoding='utf-8')
        total += 1
        print(f'  [{label}] {rel}')
    else:
        # Try a normalized whitespace match
        norm_old = re.sub(r'\s+', ' ', old)
        norm_s = re.sub(r'\s+', ' ', s)
        if norm_old in norm_s:
            print(f'  [skip {label}: matches normalized but not exact - manual review]')
        else:
            print(f'  [skip {label}: not found]')

# 6. Add "Read Appendix X →" link to cards A-V in appendices/index.html
ai = ROOT / 'appendices' / 'index.html'
appendix_link_count = [0]


def add_appendix_links_to_cards(html: str) -> str:
    card_re = re.compile(
        r'(<div class="chapter-card">\s*<div class="chapter-card-header">\s*'
        r'<span class="mod-num">Appendix ([A-Z]+)</span>([^<]+)</div>\s*'
        r'<div class="chapter-card-body">\s*<p>([^<]+)</p>\s*)(</div>\s*</div>)',
        re.DOTALL)

    def add_link(m):
        prefix = m.group(1)
        letter = m.group(2)
        suffix = m.group(5)
        full_match = m.group(0)
        if 'Read Appendix' in full_match:
            return full_match
        slug_letter = letter.lower()
        appendix_dir = None
        for d in (ROOT / 'appendices').iterdir():
            if d.is_dir() and d.name.startswith(f'appendix-{slug_letter}-'):
                appendix_dir = d.name
                break
        if not appendix_dir:
            return full_match
        appendix_link_count[0] += 1
        new_link = (f'\n            <p><a href="{appendix_dir}/index.html">'
                    f'Read Appendix {letter} &rarr;</a></p>\n        ')
        return prefix + new_link + suffix

    return card_re.sub(add_link, html)


if ai.exists():
    s = ai.read_text(encoding='utf-8')
    new_s = add_appendix_links_to_cards(s)
    if appendix_link_count[0]:
        ai.write_text(new_s, encoding='utf-8')
        total += appendix_link_count[0]
        print(f'  [appendix card "Read X" links: +{appendix_link_count[0]}]')

print(f'\ntotal residual fixes: {total}')
