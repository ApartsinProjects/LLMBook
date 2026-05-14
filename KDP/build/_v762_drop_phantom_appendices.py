"""v762: Drop references to non-existent Appendix M, N, O, P, Q.

The book's appendix list jumps from L straight to R. Earlier drafts
planned five framework appendices (LangGraph, CrewAI, LlamaIndex,
Semantic Kernel, DSPy) that were never written. Stale prose still
refers to them, and `appendices/index.html` even lists them with
descriptions as if they exist.

Strategy:
  - Remove the 5 fake cards from appendices/index.html.
  - Replace inline "see Appendix M (LangGraph)" / "Appendix O
    (LlamaIndex)" / etc. with "see the LangGraph / LlamaIndex / ...
    documentation" (or drop the parenthetical entirely when no
    replacement is needed).
  - Fix broken links that pointed at the wrong appendix (a couple of
    "see Appendix M" anchors actually pointed at appendix-l).

Idempotent.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# 1. Remove the 5 phantom-appendix cards from appendices/index.html
ai_path = ROOT / 'appendices' / 'index.html'
ai = ai_path.read_text(encoding='utf-8')
phantom_cards_re = re.compile(
    r'\s*<div class="chapter-card">\s*<div class="chapter-card-header">\s*'
    r'<span class="mod-num">Appendix [MNOPQ]</span>[\s\S]*?</div>\s*</div>',
    re.DOTALL)
ai_new = phantom_cards_re.sub('', ai)
n_cards_removed = len(phantom_cards_re.findall(ai))
ai_path.write_text(ai_new, encoding='utf-8')
print(f'appendices/index.html: removed {n_cards_removed} phantom cards')

# 2. Inline reference rewrites
INLINE_FIXES = [
    # appendix-k-huggingface-ecosystem
    ('see Appendix L (LangChain) or Appendix O (LlamaIndex) instead.',
     'see Appendix L (LangChain) instead, or consult the LlamaIndex '
     'documentation directly.'),
    # appendix-l-langchain index.html
    ('see Chapter 19 (RAG). For agent patterns, see Chapter 21 and '
     'Appendix M (LangGraph) for stateful agent graphs.',
     'see Chapter 19 (RAG). For agent patterns, see Chapter 21; '
     'LangGraph (LangChain\'s graph-based extension) is covered '
     'briefly in Section L.5 and in its own documentation.'),
    ('If your use case requires complex stateful agent workflows with '
     'branching logic, consider Appendix M (LangGraph), which extends '
     'LangChain with graph-based state management. For a '
     'retrieval-first approach with deep indexing features, see '
     'Appendix O (LlamaIndex).',
     'If your use case requires complex stateful agent workflows with '
     'branching logic, consider LangGraph (LangChain\'s graph-based '
     'extension). For a retrieval-first approach with deep indexing '
     'features, consult the LlamaIndex documentation.'),
    # appendix-l-langchain section-l.5.html
    ('see <a href="../appendix-l-langchain/index.html">Appendix M: '
     'LangGraph</a>',
     'see the LangGraph documentation'),
    # appendix-r-experiment-tracking section-r.5.html
    ('See Chapter 13 on RAG architectures and '
     '<a href="../appendix-l-langchain/index.html">Appendix N</a> on '
     'LangChain',
     'See Chapter 19 on RAG architectures and '
     '<a href="../appendix-l-langchain/index.html">Appendix L</a> on '
     'LangChain'),
    # appendix-v-tooling-ecosystem index.html
    ('Each tool covered here has a dedicated deep-dive appendix: '
     'Appendix K (HuggingFace), Appendix L (LangChain), Appendix M '
     '(LangGraph), Appendix N (CrewAI), Appendix O (LlamaIndex), '
     'Appendix P (Semantic Kernel), Appendix Q (DSPy), Appendix R '
     '(Experiment Tracking), Appendix S (Inference Serving), '
     'Appendix T (Distributed ML), and Appendix U (Docker).',
     'The tools that have a dedicated deep-dive appendix are '
     'Appendix K (HuggingFace), Appendix L (LangChain), Appendix R '
     '(Experiment Tracking), Appendix S (Inference Serving), '
     'Appendix T (Distributed ML), and Appendix U (Docker). LangGraph, '
     'CrewAI, LlamaIndex, Semantic Kernel, and DSPy are surveyed here '
     'with pointers to their primary documentation.'),
    # part-5-retrieval/module-19-rag/section-19.1.html
    ('For a hands-on tutorial building RAG pipelines with LlamaIndex, '
     'see <a href="../../appendices/appendix-k-huggingface-ecosystem/'
     'index.html">Appendix O: LlamaIndex</a>.',
     'For framework-level RAG pipelines, see Appendix L (LangChain), '
     'or consult the LlamaIndex documentation directly.'),
]

n_inline = 0
files_touched = set()
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if 'KDP/build/source_fix_backups' in sp or '/pagefind/' in sp:
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    new = s
    for old, new_v in INLINE_FIXES:
        if old in new:
            new = new.replace(old, new_v)
            n_inline += 1
            files_touched.add(p)
    if new != s:
        p.write_text(new, encoding='utf-8')

print(f'inline rewrites: {n_inline} across {len(files_touched)} files')
for f in sorted(files_touched):
    print(f'  - {f.relative_to(ROOT)}')

# 3. Final verification: any remaining "Appendix [MNOPQ]" mentions?
remaining = []
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if 'KDP/build/source_fix_backups' in sp:
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for m in re.finditer(r'Appendix [MNOPQ]\b', s):
        remaining.append((p.relative_to(ROOT), m.group(0)))
print(f'\nremaining phantom-appendix mentions: {len(remaining)}')
for r in remaining[:10]:
    print(f'  {r[0]}: {r[1]}')
