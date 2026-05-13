"""9th edition Wave C2: embed selected production patterns (from
FM.0c Production Patterns Reference) inline at the chapter where each
pattern most applies. The full catalogue stays in FM.0c; this script
adds a compact callout at the point in the prose where the practitioner
needs the pattern, with a 'when not to use this' caveat and a link back
to the catalogue.

5 patterns selected for embedding:
  P1: Generator-Verifier   -> RAG chapter (Section 18.2)
  P2: Token Budget Caps    -> Agent Safety (Section 24.3)
  P3: Eval-Driven Gates    -> Evaluation chapter (Section 27.5)
  P4: Retry Budget         -> LLM API chapter (Section 10.2)
  P5: Soft-Failure Guard   -> Production Engineering (Section 28.4)

Idempotent: sentinel `<!-- v714-pattern -->`.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v714-pattern -->'


def card(pattern_id: str, name: str, what: str, when_not: str,
         catalogue_link: str = '../../front-matter/section-fm.0c-production-patterns.html') -> str:
    return (
        f'<div class="callout production-pattern">{SENTINEL}\n'
        f'<div class="callout-title">Production Pattern {pattern_id}: {name}</div>\n'
        f'<p><strong>What it is:</strong> {what}</p>\n'
        f'<p><strong>When not to use it:</strong> {when_not}</p>\n'
        f'<p><strong>Catalogue:</strong> See the full discussion + variants in '
        f'<a href="{catalogue_link}#pattern-{pattern_id.lower()}">'
        f'FM.0c Pattern {pattern_id}</a>.</p>\n'
        f'</div>\n'
    )


PATTERNS = [
    # (file, h2_prefix_to_insert_after, pattern_html)
    ('part-5-retrieval-conversation/module-18-rag/section-18.2.html',
     '18.2',
     card('P1', 'Generator-Verifier',
          'A fast generator model produces a candidate answer; a slower or more grounded verifier model (or rule, or human) signs off before the user sees it. Inserts a quality gate without paying full inference cost on every token.',
          'Real-time latency budgets under ~500 ms end-to-end. The verifier round-trip is the cost; if you can\'t afford one extra call, fall back to a generator with strong prompting.')),

    ('part-6-agentic-ai/module-24-agent-safety-production/section-24.3.html',
     '24.3',
     card('P2', 'Token Budget Caps',
          'Every agent session is bounded by a hard token-and-tool-call budget enforced by the orchestrator, not by the model. The agent cannot loop forever because the harness stops it, not because the model decided to give up.',
          'One-shot tasks where you control the prompt and the model returns in one call. The pattern is over-engineering for non-agentic LLM uses.')),

    ('part-8-evaluation-production/module-27-evaluation-observability/section-27.5.html',
     '27.5',
     card('P3', 'Eval-Driven Quality Gates',
          'No prompt, model, or fine-tune change ships without passing a fixed regression eval (typically 100-500 examples covering critical behaviors). The CI pipeline runs the eval; failures block deploy.',
          'Pre-launch or single-developer projects with no users yet. Quality gates have a setup cost; pay it once you have users to protect.')),

    ('part-3-working-with-llms/module-10-llm-apis/section-10.2.html',
     '10.2',
     card('P4', 'Retry Budget with Exponential Backoff + Jitter',
          'Every external API call (LLM provider, vector DB, tool) is wrapped with a retry policy that has a fixed budget (typically 3-5 retries), exponential backoff (e.g., 250 ms * 2^n), and per-retry jitter to avoid thundering-herd retries that hit the provider at the same moment.',
          'Low-stakes interactive requests where a user is watching: surface the failure rather than retry. Long waits with no feedback are worse than a clear error.')),

    ('part-8-evaluation-production/module-28-production-engineering/section-28.4.html',
     '28.4',
     card('P5', 'Soft-Failure Guard',
          'Track outcomes that look like success at the protocol level (HTTP 200, parseable JSON, non-empty result) but are still business-failures (wrong answer, empty list, hallucinated content). Each path through the system has a "what counts as soft failure here" definition that gets monitored independently of the hard-failure rate.',
          'Pure infrastructure services with no semantic notion of success/failure (a load balancer, a CDN). Soft-failure tracking requires a domain model.')),
]


def main() -> int:
    n = 0
    for rel_path, prefix, body in PATTERNS:
        p = ROOT / rel_path
        if not p.exists():
            print(f'  MISSING: {rel_path}')
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if SENTINEL in text:
            print(f'  SKIP (already present): {rel_path}')
            continue
        pat = re.compile(r'<h2[^>]*>([^<]*)</h2>', re.IGNORECASE)
        inserted = False
        for m in pat.finditer(text):
            if m.group(1).strip().startswith(prefix):
                ins = m.end()
                new = text[:ins] + '\n' + body + text[ins:]
                p.write_text(new, encoding='utf-8')
                n += 1
                print(f'  added: {rel_path} (after h2 starting "{prefix}")')
                inserted = True
                break
        if not inserted:
            print(f'  NOT FOUND <h2>{prefix}: {rel_path}')
    print(f'\nAdded {n} production-pattern callouts.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
