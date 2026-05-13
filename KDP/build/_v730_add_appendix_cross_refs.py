"""Add canonical-content cross-reference callouts to appendices that
duplicate book content without linking back to it.

From v729 audit, these appendices have HIGH overlap with main chapters
but ZERO chapter cross-refs:
- appendix-h-model-cards    -> Ch 07 (Modern LLM Landscape)
- appendix-l-langchain      -> Ch 22 (Tool Use & Protocols)
- appendix-r-experiment-tracking -> Ch 28 (Evaluation & Observability)
- appendix-u-docker-containers -> Ch 29 (Production Engineering)
- appendix-v-tooling-ecosystem -> Ch 23 (Multi-Agent Systems)

Plus medium-overlap with low cross-refs:
- appendix-k-huggingface-ecosystem -> Ch 06 (Pretraining + Scaling Laws)

Inserts a `<div class="callout cross-ref">` right after the
chapter-opener / epigraph / first <p>, pointing to the canonical chapter.

Idempotent: sentinel `<!-- v730-appendix-xref -->`.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v730-appendix-xref -->'

# (appendix_index_path, chapter_index_href, chapter_title, framing)
INSERTIONS = [
    ('appendices/appendix-h-model-cards/index.html',
     '../../part-2-understanding-llms/module-07-modern-llm-landscape/index.html',
     'Chapter 7: Modern LLM Landscape',
     'the framework for evaluating and comparing models'),
    ('appendices/appendix-k-huggingface-ecosystem/index.html',
     '../../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html',
     'Chapter 6: Pre-training, Scaling Laws &amp; Data Curation',
     'the conceptual foundations of why models are trained the way they are'),
    ('appendices/appendix-l-langchain/index.html',
     '../../part-6-agentic-ai/module-22-tool-use-protocols/index.html',
     'Chapter 22: Tool Use, Function Calling &amp; Protocols',
     'the protocol-level treatment of tool calling and MCP'),
    ('appendices/appendix-r-experiment-tracking/index.html',
     '../../part-8-evaluation-production/module-28-evaluation-observability/index.html',
     'Chapter 28: LLM Evaluation &amp; Quality Metrics',
     'the evaluation-design and observability framework that uses these tools'),
    ('appendices/appendix-u-docker-containers/index.html',
     '../../part-8-evaluation-production/module-29-production-engineering/index.html',
     'Chapter 29: LLMOps &amp; Deployment Engineering',
     'the production-engineering patterns that decide when and how to containerize'),
    ('appendices/appendix-v-tooling-ecosystem/index.html',
     '../../part-6-agentic-ai/module-23-multi-agent-systems/index.html',
     'Chapter 23: Multi-Agent Systems',
     'the architectural patterns the tools listed here implement'),
]


def make_callout(target_href: str, target_title: str, framing: str) -> str:
    return (
        f'<div class="callout cross-ref">{SENTINEL}\n'
        f'<div class="callout-title">Canonical reference</div>\n'
        f'<p>This appendix is a hands-on reference. For {framing}, '
        f'see <a href="{target_href}">{target_title}</a>. '
        f'Use this appendix when you need quick API recall or a code recipe; '
        f'use the chapter when you need to understand <em>why</em> a pattern works.</p>\n'
        f'</div>\n'
    )


def main() -> int:
    n_added = 0
    n_skip = 0
    for rel_path, target_href, target_title, framing in INSERTIONS:
        p = ROOT / rel_path
        if not p.exists():
            print(f'  MISSING: {rel_path}')
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if SENTINEL in text:
            n_skip += 1
            continue
        callout = make_callout(target_href, target_title, framing)
        # Insert right after the first <p> following <main class="content">
        main_idx = text.lower().find('<main')
        if main_idx == -1:
            print(f'  SKIP (no <main>): {rel_path}')
            continue
        # Find the first <p>...</p> after <main>
        p_match = re.search(r'<p[^>]*>[\s\S]*?</p>', text[main_idx:])
        if not p_match:
            print(f'  SKIP (no <p> after <main>): {rel_path}')
            continue
        ins = main_idx + p_match.end()
        new_text = text[:ins] + '\n' + callout + text[ins:]
        p.write_text(new_text, encoding='utf-8')
        n_added += 1
        print(f'  added: {rel_path}')
    print(f'\nAdded {n_added} cross-ref callouts; skipped {n_skip} already present.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
