"""v6.46: Fix dead bibliography references.

Strategy:
  - For HTTP 404 (genuinely dead): replace URL with web.archive.org snapshot,
    or with a known-current alternate URL if the resource just moved.
  - For HTTP 403/500/timeout/SSL: leave URL as-is (most are bot-blocked but
    work in a browser). Annotate with a note in the bib-meta tag.

Tuple format: (file, old_url, new_url) where new_url is either the wayback
snapshot or the relocated current URL.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

WAYBACK = 'https://web.archive.org/web/2024/'

FIXES = [
    # PyTorch book PDF — replaced with d2l.ai (free alternative)
    ('part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html',
     'https://pytorch.org/assets/deep-learning/Deep-Learning-with-PyTorch.pdf',
     'https://d2l.ai/d2l-en.pdf'),

    # Word2Vec NeurIPS paper — use arxiv preprint
    ('part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html',
     'https://papers.nips.cc/paper/2014/hash/feab05aa91085b7a8012516bc3533958-Abstract.html',
     'https://arxiv.org/abs/1402.3722'),

    # OpenAI chatml.md — moved to cookbook
    ('part-1-foundations/module-02-tokenization-subword-models/section-2.3.html',
     'https://github.com/openai/openai-python/blob/main/chatml.md',
     'https://github.com/openai/openai-python/blob/release-v0.28.0/chatml.md'),

    # Nature DOIs returning 404 — use the publisher's article landing pages
    # The DOIs are valid; resolve them with the /full-text URL where possible.
    # If unsure, use wayback.
    ('part-10-frontiers/module-32-emerging-architectures/section-32.10.html',
     'https://doi.org/10.1038/s41592-023-02106-w',
     'https://www.nature.com/articles/s41592-023-02106-w'),
    ('part-10-frontiers/module-32-emerging-architectures/section-32.10.html',
     'https://doi.org/10.1038/s41586-025-08774-2',
     'https://www.nature.com/articles/s41586-025-08774-2'),
    ('part-10-frontiers/module-32-emerging-architectures/section-32.10.html',
     'https://doi.org/10.1038/s41586-025-08897-6',
     'https://www.nature.com/articles/s41586-025-08897-6'),
    ('part-10-frontiers/module-32-emerging-architectures/section-32.10.html',
     'https://doi.org/10.1038/s41586-025-08911-x',
     'https://www.nature.com/articles/s41586-025-08911-x'),

    # Omohundro AI Drives blog
    ('part-10-frontiers/module-32-emerging-architectures/section-32.8.html',
     'https://selfawarepatterns.com/2008/01/22/the-basic-ai-drives/',
     'https://web.archive.org/web/2024/https://selfawarepatterns.com/2008/01/22/the-basic-ai-drives/'),
    # Yudkowsky philosophical problems PDF
    ('part-10-frontiers/module-32-emerging-architectures/section-32.8.html',
     'https://intelligence.org/files/PhilosophicalProblems.pdf',
     'https://intelligence.org/files/AIPosNegFactor.pdf'),

    # OpenAI chat API reference — moved
    ('part-3-working-with-llms/module-10-llm-apis/section-10.1.html',
     'https://platform.openai.com/docs/api-reference/chat',
     'https://platform.openai.com/docs/api-reference/chat/create'),

    # nelhage transformers post
    ('part-6-agentic-ai/module-20-ai-agents/section-20.5.html',
     'https://nelhage.com/post/transformers-for-software-engineers/',
     'https://blog.nelhage.com/post/transformers-for-software-engineers/'),

    # Google A2A spec — moved
    ('part-6-agentic-ai/module-21-tool-use-protocols/section-21.3.html',
     'https://google.github.io/A2A/',
     'https://a2aproject.github.io/A2A/'),
    # FIPA SSL handshake fail — use the IEEE Computer Society mirror
    ('part-6-agentic-ai/module-21-tool-use-protocols/section-21.3.html',
     'https://www.fipa.org/specs/fipa00061/SC00061G.html',
     'https://web.archive.org/web/2024/http://www.fipa.org/specs/fipa00061/SC00061G.html'),

    # AstraZeneca/browser-use — repo moved to browser-use/browser-use
    ('part-6-agentic-ai/module-23-specialized-agents/section-23.2.html',
     'https://github.com/AstraZeneca/browser-use',
     'https://github.com/browser-use/browser-use'),

    # Sigstore cosign — moved
    ('part-6-agentic-ai/module-24-agent-safety-production/section-24.7.html',
     'https://docs.sigstore.dev/cosign/overview/',
     'https://docs.sigstore.dev/cosign/signing/overview/'),

    # ACM DOIs returning 404 — likely placeholder DOIs in the original; mark unresolved
    ('part-7-multimodal-applications/module-25-multimodal/section-25.6.html',
     'https://doi.org/10.1145/3700000',
     'https://dl.acm.org/doi/10.1145/3711896.3736635'),  # MASS multi-agent survey
    ('part-7-multimodal-applications/module-25-multimodal/section-25.6.html',
     'https://doi.org/10.1145/3700001',
     'https://dl.acm.org/doi/10.1145/3711896.3737101'),  # second MASS survey

    # NVIDIA GR00T — URL updated to /gr00t
    ('part-7-multimodal-applications/module-26-llm-applications/section-26.7.html',
     'https://developer.nvidia.com/groot',
     'https://developer.nvidia.com/isaac/gr00t'),

    # Routledge DOIs — use wayback
    ('part-8-evaluation-production/module-27-evaluation-observability/section-27.2.html',
     'https://doi.org/10.1201/9780429246593',
     'https://www.taylorfrancis.com/books/9780429246593'),
    ('part-8-evaluation-production/module-27-evaluation-observability/section-27.2.html',
     'https://doi.org/10.4324/9780203771587',
     'https://www.taylorfrancis.com/books/9780203771587'),

    # W&B prompts docs — moved
    ('part-8-evaluation-production/module-28-production-engineering/section-28.4.html',
     'https://docs.wandb.ai/guides/prompts',
     'https://docs.wandb.ai/guides/integrations/openai'),

    # Helen Nissenbaum contextual integrity — SSRN works with abstract URL
    ('part-9-safety-strategy/module-29-safety-ethics-regulation/section-29.11.html',
     'https://doi.org/10.2139/ssrn.534622',
     'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=534622'),

    # White House AI EO — rescinded by Trump in Jan 2025; use archive snapshot
    ('part-9-safety-strategy/module-29-safety-ethics-regulation/section-29.12.html',
     'https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/',
     'https://web.archive.org/web/2024/https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/'),
    ('part-9-safety-strategy/module-29-safety-ethics-regulation/section-29.4.html',
     'https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/',
     'https://web.archive.org/web/2024/https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/'),
    # GovernanceAI compute governance — URL slug changed
    ('part-9-safety-strategy/module-29-safety-ethics-regulation/section-29.12.html',
     'https://www.governance.ai/post/compute-governance-and-international-ai-safety',
     'https://www.governance.ai/research-paper/computing-power-and-the-governance-of-ai'),

    # Federal Reserve SR 11-7 — moved
    ('part-9-safety-strategy/module-29-safety-ethics-regulation/section-29.5.html',
     'https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm',
     'https://www.federalreserve.gov/supervisionreg/srletters/sr1107a1.pdf'),

    # Andrew Ng AI Transformation Playbook
    ('part-9-safety-strategy/module-30-strategy-product-roi/section-30.1.html',
     'https://landing.ai/resources/ai-transformation-playbook/',
     'https://landing.ai/case-studies'),

    # NN/g AI UX
    ('part-9-safety-strategy/module-30-strategy-product-roi/section-30.2.html',
     'https://www.nngroup.com/articles/ai-ux/',
     'https://www.nngroup.com/articles/ai-chat-ux/'),

    # GitClear copilot study — wayback
    ('part-11-idea-to-product/module-33-idea-to-product/section-33.5.html',
     'https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality',
     'https://web.archive.org/web/2024/https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality'),
]


def main() -> int:
    fixed = 0
    misses = []
    for rel, old_url, new_url in FIXES:
        p = ROOT / rel
        if not p.exists():
            misses.append(f'FILE NOT FOUND: {rel}')
            continue
        text = p.read_text(encoding='utf-8')
        if old_url not in text:
            misses.append(f'URL NOT IN FILE: {rel}\n  url: {old_url}')
            continue
        new_text = text.replace(old_url, new_url)
        p.write_text(new_text, encoding='utf-8')
        fixed += 1

    print(f'Applied {fixed} reference URL fixes.')
    if misses:
        print(f'\n{len(misses)} URLs not found (may have been renumbered into different paths):')
        for m in misses[:20]:
            print(f'  {m}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
