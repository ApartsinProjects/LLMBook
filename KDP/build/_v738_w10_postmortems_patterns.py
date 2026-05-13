"""11th edition Wave 10 (Tier A): Add 5 postmortem callouts + 5 production
pattern callouts at targeted sections.

Each callout is inserted right after the section's first <h2> heading
(i.e., before the first prose paragraph). Idempotent via per-callout
sentinel comments. Non-destructive (pure additions).

Style:
  Postmortem: <div class="callout postmortem"><!-- v738-pm-{id} -->
  Production: <div class="callout production-pattern"><!-- v738-pp-{id} -->
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# 5 POSTMORTEM CALLOUTS
# Each entry: (relative-path, sentinel-id, callout-title, callout-body-html)
# Insertion: right after the FIRST <h2> in <main>.
# ---------------------------------------------------------------------------
POSTMORTEMS = [
    # 1. Embedding-model swap regression (RAG)
    ('part-5-retrieval-conversation/module-19-rag/section-19.1.html',
     'embed-swap',
     'Postmortem: The Silent Embedding-Model Swap',
     'A team upgraded their embedding model from <code>text-embedding-ada-002</code> to '
     '<code>text-embedding-3-small</code> in a single PR, expecting "better embeddings = '
     'better retrieval." Recall on their golden set dropped 18 percent overnight. '
     'Root cause: the new model produced vectors with different angular geometry, so a '
     'query embedded with v3 found near-zero cosine similarity against documents still '
     'embedded with v2 in the index. They had not re-embedded the corpus. Lesson: '
     'embedding models are part of the retrieval contract, not a swappable hyperparameter. '
     'Either re-embed everything atomically or maintain dual indices during a migration '
     '(see Production Pattern P2 in <a href="../../front-matter/section-fm.0c-production-patterns.html">FM.0c Production Patterns</a>).'),

    # 2. Synthetic-data poisoning during fine-tune
    ('part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.1.html',
     'synth-poison',
     'Postmortem: Synthetic Data That Poisoned the Fine-Tune',
     'A team generated 50K synthetic instruction-response pairs using GPT-4 to fine-tune '
     'a Llama 3 8B chatbot. The teacher prompt accidentally contained the phrase "you are '
     'a helpful assistant from OpenAI." After fine-tuning, ~3 percent of the student '
     'model\'s replies began with "As an AI assistant developed by OpenAI…" — a contractual '
     'and brand disaster. Lesson: synthetic data inherits the teacher\'s biases, '
     'identity claims, and safety patterns. Always run a string-search audit on generated '
     'data for vendor names, refusal templates, and identity claims before training. '
     'Cost of the cleanup: 2 weeks of retraining. Cost of the audit script: 30 minutes.'),

    # 3. Quantization that broke math
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.1.html',
     'quant-math',
     'Postmortem: 4-bit Quantization That Killed Arithmetic',
     'A finance startup quantized their fine-tuned Llama 3 70B model from FP16 to '
     'INT4 to fit on a single A100. Throughput tripled. Then their evaluation harness '
     'flagged a 22-point drop on GSM8K (grade-school math). Investigation showed that '
     'numerical reasoning relies on precise intermediate activations; INT4 quantization '
     'introduced enough noise in the residual stream to flip digits during multi-step '
     'arithmetic. Lesson: quantization quality is task-dependent. Always evaluate on '
     'the tasks that matter <em>before</em> shipping a quantized model, not just on '
     'aggregate benchmarks. The fix here was per-channel quantization on the FFN layers '
     'and FP8 on the attention output, recovering 18 of the 22 points.'),

    # 4. Prompt-version drift between staging and prod
    ('part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html',
     'prompt-drift',
     'Postmortem: The Prompt That Worked in Staging Only',
     'An e-commerce team\'s product-description generator passed all staging tests, '
     'then started producing empty strings 8 percent of the time in production. Root '
     'cause: staging used <code>gpt-4o-2024-08-06</code> (pinned for tests); production '
     'used <code>gpt-4o</code> (the rolling alias). A silent model update changed the '
     'model\'s behavior on a specific prompt phrasing involving nested JSON. Lesson: '
     'pin model versions in production and treat alias upgrades as deployments with '
     'full evaluation. The cost of the incident: 6 hours of broken catalog imports. '
     'The cost of pinning: one extra config line.'),

    # 5. Agent runaway tool-call loop
    ('part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html',
     'agent-runaway',
     'Postmortem: The Agent That Called Search 3,847 Times',
     'A research-summarization agent shipped on Friday. By Monday morning, the on-call '
     'engineer woke up to a $4,200 bill for the weekend. The agent had hit a degenerate '
     'state where each search returned a result it could not synthesize, prompting it '
     'to "search more deeply" — looping for 18 hours straight on a single user query. '
     'Lesson: agents need <em>two</em> orthogonal limits: a per-task tool-call budget '
     '(hard cap, e.g., 20 calls) <em>and</em> a per-task wall-clock budget (e.g., 5 '
     'minutes). Either alone is insufficient: a fast tool can blow through a wall-clock '
     'budget; a slow tool can hide inside a high call-count budget. Both should fire '
     'alarms before they terminate the agent.'),
]

# ---------------------------------------------------------------------------
# 5 PRODUCTION PATTERN CALLOUTS
# ---------------------------------------------------------------------------
PRODUCTION_PATTERNS = [
    # P1. Semantic caching for repeated queries
    ('part-3-working-with-llms/module-11-llm-apis/section-11.1.html',
     'semantic-cache',
     'Production Pattern: Semantic Caching',
     '<strong>When:</strong> any LLM endpoint that receives semantically repetitive '
     'queries (FAQs, tier-1 support, retrieval rephrasings). '
     '<strong>How:</strong> embed the incoming query, search a vector store of '
     '(query-embedding, response) pairs, and serve the cached response if cosine '
     'similarity exceeds a threshold (typically 0.95 for safety, 0.85 for cost-optimised). '
     'Use a TTL (24h-7d) to keep responses fresh. '
     '<strong>Watch for:</strong> threshold drift (false positives serve wrong answers), '
     'context-dependent queries ("what about that?" cannot be cached safely), and '
     'cache poisoning if any user input is also written to the cache. '
     '<strong>Result:</strong> 40-70 percent cost reduction on repetitive workloads, '
     'p50 latency drops from seconds to milliseconds for cache hits.'),

    # P2. Retry budget with exponential backoff + jitter
    ('part-3-working-with-llms/module-11-llm-apis/section-11.2.html',
     'retry-budget',
     'Production Pattern: Retry Budget with Backoff + Jitter',
     '<strong>When:</strong> any provider call that may transiently fail (rate limits, '
     '5xx, network blips). <strong>How:</strong> wrap calls in <code>tenacity</code> '
     '(or equivalent) with exponential backoff (base 2s, cap 30s) <em>plus full jitter</em>, '
     'and a hard cap of 4 retries. Track total retries per request as a metric; if a single '
     'request retries more than 2 times, you have an upstream incident, not a flake. '
     '<strong>Watch for:</strong> the thundering-herd problem when many clients retry in '
     'lockstep — jitter is non-negotiable. Also: idempotency. Retrying a non-idempotent '
     'tool call (charge a card, send an email) twice is worse than failing once. '
     '<strong>Library:</strong> <code>tenacity</code> for Python; OpenAI SDK has built-in '
     'retry but no jitter as of mid-2025.'),

    # P3. Idempotency keys for agent tool calls
    ('part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html',
     'idempotency',
     'Production Pattern: Idempotency Keys for Tool Calls',
     '<strong>When:</strong> any agent that calls tools with side effects (payments, '
     'emails, ticket creation, database writes). <strong>How:</strong> the agent generates '
     'a UUID per logical tool invocation; the tool implementation checks a deduplication '
     'store before executing and returns the cached result on a duplicate key. The key '
     'covers a TTL window (typically 24h). <strong>Watch for:</strong> agents that retry '
     'a "failed" call which actually succeeded but timed out on the response. Without '
     'idempotency, you charge the card twice. <strong>Wire format:</strong> include '
     '<code>idempotency_key</code> in the tool-call JSON; pass it through to the underlying '
     'API (Stripe, Twilio, and most modern APIs accept this header natively).'),

    # P4. Eval-as-CI gates with blocking thresholds
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html',
     'eval-ci',
     'Production Pattern: Eval-as-CI Gates',
     '<strong>When:</strong> any change to prompts, models, retrievers, or post-processors '
     'in a system with paying users. <strong>How:</strong> run a pinned 200-1000 example '
     'golden set on every PR; compute a small set of metrics (task accuracy, LLM-as-judge '
     'score, p95 cost, p95 latency); block the merge if any metric regresses by more than a '
     'pre-declared threshold (typically 2 percent for accuracy, 20 percent for cost). '
     '<strong>Watch for:</strong> noisy LLM-as-judge metrics (run with N=3 and average), '
     'golden-set rot (audit quarterly for stale or contested labels), and selection bias '
     '(your golden set should reflect production traffic, not your favorite test cases). '
     '<strong>Result:</strong> regressions caught at PR review instead of by users.'),

    # P5. One-command rollback for prompt + model changes
    ('part-8-evaluation-production/module-29-production-engineering/section-29.4.html',
     'rollback',
     'Production Pattern: One-Command Rollback',
     '<strong>When:</strong> always. If you cannot roll back, you cannot ship safely. '
     '<strong>How:</strong> treat (model_id, model_version, prompt_id, prompt_version, '
     'retriever_index_version) as a single deployable unit, versioned in a manifest. '
     'A deploy publishes the manifest to a feature flag or config store; rollback flips '
     'the pointer to the previous manifest in under 30 seconds. <strong>Watch for:</strong> '
     'stateful side effects that survive rollback (a retriever index migrated forward cannot '
     'be rolled back without dual-write — see Pattern P2 in <a '
     'href="../../front-matter/section-fm.0c-production-patterns.html">FM.0c</a>). '
     'Also: bake "rollback rehearsal" into your runbook quarterly. The first time you try '
     'to roll back at 3 a.m. is the worst possible time to discover that the previous '
     'manifest is missing a now-required field.'),
]


# ---------------------------------------------------------------------------
def render_callout(kind: str, sentinel: str, title: str, body: str) -> str:
    css_class = 'postmortem' if kind == 'pm' else 'production-pattern'
    return (
        f'<div class="callout {css_class}"><!-- v738-{kind}-{sentinel} -->\n'
        f'<div class="callout-title">{title}</div>\n'
        f'<p>{body}</p>\n'
        f'</div>\n'
    )


# Insert after the first <h2> tag's CLOSING > inside <main>.
# Pattern matches: <h2 ...>...</h2>
H2_RE = re.compile(r'(<h2[^>]*>[^<]*</h2>)', re.IGNORECASE)


def inject(html: str, callout: str, sentinel_marker: str) -> tuple[str, bool]:
    if sentinel_marker in html:
        return html, False  # already injected
    m = H2_RE.search(html)
    if not m:
        return html, False
    insert_pos = m.end()
    new_html = html[:insert_pos] + '\n' + callout + html[insert_pos:]
    return new_html, True


def main():
    inserted = 0
    skipped = 0
    not_found = []

    all_entries = [('pm', e) for e in POSTMORTEMS] + [('pp', e) for e in PRODUCTION_PATTERNS]

    for kind, (rel_path, sentinel, title, body) in all_entries:
        path = ROOT / rel_path
        if not path.exists():
            not_found.append(rel_path)
            continue
        html = path.read_text(encoding='utf-8')
        sentinel_marker = f'<!-- v738-{kind}-{sentinel} -->'
        callout = render_callout(kind, sentinel, title, body)
        new_html, did_insert = inject(html, callout, sentinel_marker)
        if did_insert:
            path.write_text(new_html, encoding='utf-8')
            inserted += 1
            print(f'  + {kind} {sentinel}: {rel_path}')
        else:
            skipped += 1
            print(f'  = {kind} {sentinel}: {rel_path} (already present or no h2)')

    print(f'\nInserted: {inserted}')
    print(f'Skipped : {skipped}')
    if not_found:
        print(f'NOT FOUND ({len(not_found)}):')
        for p in not_found:
            print(f'  ! {p}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
