"""8th edition Wave 23 / B-pass: insert "Canonical Reference" callouts at
the top of sections that re-explain a topic that has a canonical home
elsewhere.

Source of truth: contents_consolidation.md (six topics flagged with deep
explanatory-prose duplication across 3+ chapters).

Strategy (pragmatic, non-destructive):
- For each duplicating section, inject ONE concise callout right after
  the section's first <h2> headline (i.e., before the first prose
  paragraph). The callout points the reader to the canonical home so
  they know where the authoritative treatment lives.
- Idempotent: identifies its own injections by a sentinel comment
  `<!-- v695-canonical-ref -->` and skips files that already have it.
- Non-destructive: never deletes prose. Pages keep current explanations.
  The author can manually trim at leisure; readers immediately benefit
  from the navigation hint.

Callout style (matches existing visual identity):
  <div class="callout cross-ref"><!-- v695-canonical-ref -->
    <div class="callout-title">Canonical reference</div>
    <p>The deep treatment of <em>{topic}</em> lives in <a href="...">{section}</a>.
    The discussion below adds {context-specific-framing}.</p>
  </div>
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SENTINEL = '<!-- v695-canonical-ref -->'

# (relative-path, topic, link-rel, anchor-text, context)
ENTRIES = [
    # 1. ReAct loop -- canonical home: 20.1
    ('part-3-working-with-llms/module-11-prompt-engineering/section-11.2.html',
     'the ReAct (perception--reasoning--action) loop',
     '../../part-6-agentic-ai/module-20-ai-agents/section-20.1.html',
     'Section 20.1',
     'how ReAct shows up as a prompting pattern'),
    ('part-5-retrieval-conversation/module-19-conversational-ai/section-19.1.html',
     'the perception--reasoning--action loop',
     '../../part-6-agentic-ai/module-20-ai-agents/section-20.1.html',
     'Section 20.1',
     'the dialogue framing'),
    ('part-6-agentic-ai/module-21-tool-use-protocols/section-21.1.html',
     'the agent loop',
     '../module-20-ai-agents/section-20.1.html',
     'Section 20.1',
     'the tool-call slot specifically'),
    ('part-6-agentic-ai/module-22-multi-agent-systems/section-22.1.html',
     'the single-agent loop',
     '../module-20-ai-agents/section-20.1.html',
     'Section 20.1',
     'how that loop scales across agents'),

    # 2. Hallucination -- canonical homes: 18.1 (mechanism) + 29.2 (safety)
    ('part-5-retrieval-conversation/module-19-conversational-ai/section-19.1.html',
     'the hallucination mechanism',
     '../module-18-rag/section-18.1.html',
     'Section 18.1',
     'why hallucination matters in dialogue'),
    ('part-6-agentic-ai/module-24-agent-safety-production/section-24.1.html',
     'hallucination as a model failure',
     '../../part-5-retrieval-conversation/module-18-rag/section-18.1.html',
     'Section 18.1',
     'hallucination as an agent failure mode'),
    ('part-8-evaluation-production/module-28-production-engineering/section-28.4.html',
     'the underlying hallucination mechanism',
     '../../part-5-retrieval-conversation/module-18-rag/section-18.1.html',
     'Section 18.1',
     'production-side detection'),

    # 3. Prompting vs RAG vs FT -- canonical: FM.0a T1 + 14.1
    ('part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html',
     'the prompt-vs-RAG-vs-fine-tune decision framework',
     '../../front-matter/section-fm.0a-reference-tables.html',
     'FM.0a Table T1',
     'when prompting alone is sufficient'),
    ('part-5-retrieval-conversation/module-18-rag/section-18.1.html',
     'the prompt-vs-RAG-vs-fine-tune decision tree',
     '../../part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html',
     'Section 14.1',
     'what changes when retrieval is on the table'),

    # 4. Catastrophic forgetting -- canonical: 14.1
    ('part-4-training-adapting/module-15-peft/index.html',
     'catastrophic forgetting',
     '../module-14-fine-tuning-fundamentals/section-14.1.html',
     'Section 14.1',
     'how PEFT mitigates the same effect'),

    # 5. Reasoning models / o-series -- canonical: Chapter 8
    ('part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html',
     'reasoning models and test-time compute',
     '../module-08-reasoning-test-time-compute/index.html',
     'Chapter 8',
     'a landscape-level overview only'),
    ('part-6-agentic-ai/module-20-ai-agents/section-20.3.html',
     'how reasoning models work internally',
     '../../part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html',
     'Chapter 8',
     'how to configure them inside an agent loop'),

    # 6. Function calling -- canonical: 21.1
    ('part-3-working-with-llms/module-10-llm-apis/section-10.2.html',
     'the function-calling loop',
     '../../part-6-agentic-ai/module-21-tool-use-protocols/section-21.1.html',
     'Section 21.1',
     'the JSON-schema mechanics that providers expose'),
]


def make_callout(topic: str, link: str, anchor_text: str, context: str) -> str:
    return (
        f'<div class="callout cross-ref">{SENTINEL}\n'
        f'<div class="callout-title">Canonical reference</div>\n'
        f'<p>The deep treatment of {topic} lives in '
        f'<a href="{link}">{anchor_text}</a>. The discussion below focuses on '
        f'{context}.</p>\n'
        f'</div>\n'
    )


def main() -> int:
    n_added = 0
    n_skip_existing = 0
    n_missing = 0
    for rel_path, topic, link, anchor, context in ENTRIES:
        p = ROOT / rel_path
        if not p.exists():
            print(f'  MISSING: {rel_path}')
            n_missing += 1
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if SENTINEL in text:
            n_skip_existing += 1
            continue
        callout = make_callout(topic, link, anchor, context)
        # Insert right after the first <h2> closing tag inside <main>
        main_idx = text.lower().find('<main')
        if main_idx == -1:
            print(f'  SKIP (no <main>): {rel_path}')
            continue
        h2_match = re.search(r'</h2>', text[main_idx:], re.IGNORECASE)
        if not h2_match:
            print(f'  SKIP (no <h2>): {rel_path}')
            continue
        ins = main_idx + h2_match.end()
        new = text[:ins] + '\n' + callout + text[ins:]
        p.write_text(new, encoding='utf-8')
        print(f'  added: {rel_path}')
        n_added += 1
    print(f'\nAdded {n_added} canonical-reference callouts; '
          f'skipped {n_skip_existing} already present; missing {n_missing}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
