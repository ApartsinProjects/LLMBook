"""10th edition Wave 9 + 10: best-practice tip/warning callouts +
postmortems and production patterns. Pre-drafted in
_agent_reports/best-practices.md and inline below.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v737-bp -->'


def tip(title: str, body: str) -> str:
    return (
        f'<div class="callout tip">{SENTINEL}\n'
        f'<div class="callout-title">Tip: {title}</div>\n'
        f'<p>{body}</p>\n'
        f'</div>\n'
    )


def warning(title: str, body: str) -> str:
    return (
        f'<div class="callout warning">{SENTINEL}\n'
        f'<div class="callout-title">Warning: {title}</div>\n'
        f'<p>{body}</p>\n'
        f'</div>\n'
    )


def postmortem(title: str, body: str) -> str:
    return (
        f'<div class="callout postmortem">{SENTINEL}\n'
        f'<div class="callout-title">Postmortem: {title}</div>\n'
        f'<p>{body}</p>\n'
        f'</div>\n'
    )


def pattern(pid: str, name: str, what: str, when_not: str) -> str:
    return (
        f'<div class="callout production-pattern">{SENTINEL}\n'
        f'<div class="callout-title">Production Pattern {pid}: {name}</div>\n'
        f'<p><strong>What it is:</strong> {what}</p>\n'
        f'<p><strong>When not to use it:</strong> {when_not}</p>\n'
        f'</div>\n'
    )


# Post-renumber section numbers. Each is (rel_path, anchor_h2_prefix, callout)
INSERTIONS = [
    # === IMPLEMENTATION BEST PRACTICES (Wave 9) ===

    # I1: Log the triple
    ('part-3-working-with-llms/module-11-llm-apis/section-11.3.html',
     '11.3',
     tip('Log the Triple, Not Just the Output',
         'Every LLM call should emit one log record containing three fields: the full rendered prompt, the retrieved context chunks (for RAG), and the model output. Logging only the output is the most common observability mistake: when a response goes wrong, you need to know what input produced it. Tools like Langfuse and Phoenix make structured triple-logging a one-line decorator. Make it the default for every LLM call in your codebase, not an afterthought.')),

    # I2: Strict prompt template
    ('part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html',
     '12.1',
     warning('String Concatenation Produces Silent Failures',
             'Building prompts with <code>f"You are {role}. Answer: {question}"</code> silently produces "You are None. Answer: None" when variables are missing. Use Jinja2 with <code>StrictUndefined</code> and a Pydantic model for slot values: any missing field raises at render time, before the API call is made. This catches the most common prompt bug at the cheapest possible moment.')),

    # I3: Pin model versions
    ('part-3-working-with-llms/module-11-llm-apis/section-11.1.html',
     '11.1',
     warning('Never Use Unversioned Model Names in Production',
             'Calling <code>model="gpt-4o"</code> or <code>model="claude-sonnet"</code> means the model your code runs against changes whenever the provider updates the alias, with no entry in your deploy log. Use dated identifiers (<code>gpt-4o-2025-05-13</code>) and pin them in a central config. Upgrade versions deliberately, on a schedule, with a regression eval. Treat a model alias change as a silent dependency upgrade.')),

    # I5: Eval retrieval and generation separately
    ('part-5-retrieval-conversation/module-19-rag/section-19.1.html',
     '19.1',
     tip('Evaluate Retrieval and Generation Separately',
         'Measure Recall@k and MRR for the retriever on a golden query set, independently of end-to-end answer quality. A capable generator can partially compensate for poor retrieval, masking the underlying problem until the generator changes. Run retrieval evals on every index rebuild, embedding-model upgrade, or chunking-strategy change. Keep a small (200-query) retrieval golden set; treat a Recall@5 drop &gt;5pp as a deployment blocker.')),

    # I6: Constrain tool schemas
    ('part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html',
     '22.1',
     warning('Constrain Tool Schemas Tightly',
             'A tool defined as <code>{action: {type: string, description: "what to do"}}</code> gives the model unlimited latitude to invent actions. Use <code>"enum": ["read", "summarize", "send_draft"]</code> to restrict to operations you have audited and tested. For arguments that are IDs or paths, add <code>"pattern"</code> or <code>"format"</code> constraints. JSON Schema validation at the tool boundary is your last line of defense before an agent takes a real-world action you did not intend to permit.')),

    # === RESEARCH BEST PRACTICES ===

    # R2: Seed and replicate
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html',
     '28.1',
     tip('Seed and Replicate Stochastic Evaluations',
         'When evaluating at temperature &gt; 0, set a fixed random seed and run at least three independent seeds. Report mean and standard deviation alongside your point estimate. A result sensitive to the seed choice is not a stable result. For greedy evaluation (T=0), one run is sufficient because outputs are deterministic per model and prompt. Many published LLM evals are single-seed temperature-1 runs &mdash; treat those numbers as provisional until replicated.')),

    # R5: Failure analysis
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.2.html',
     '28.2',
     tip('Include a Failure Analysis Section in Every Evaluation',
         'For any evaluation reporting aggregate metrics, sample 20-50 errors, categorize them by failure type (hallucination, format error, topic drift, instruction-following failure), and report the distribution. This transforms a number into an actionable diagnosis. Readers of a benchmark result need to know not just that the model scores 78%, but that 60% of failures are in "multi-step reasoning" and 30% are format noncompliance. One page of error taxonomy is worth ten pages of aggregate tables.')),

    # === MODEL-BUILDING BEST PRACTICES ===

    # M1: Grad norm spikes
    ('part-4-training-adapting/module-15-fine-tuning-fundamentals/section-15.3.html',
     '15.3',
     tip('Alert on Gradient Norm Spikes, Not Just Loss Spikes',
         'Log <code>grad_norm</code> alongside training loss at every step. Compute a 100-step rolling average and alert when the current norm exceeds 3&times; the average: this is the leading indicator of training instability. By the time loss diverges, many checkpoints of corrupted weights have been written. With early detection you can roll back to the last stable checkpoint, reduce the learning rate, and resume without restarting from scratch. The <code>max_grad_norm</code> clip configured in TRL is a guard rail, not a substitute for monitoring.')),

    # M5: Overfit one batch
    ('part-4-training-adapting/module-16-peft/section-16.1.html',
     '16.1.1',
     tip('Overfit One Batch Before Starting Any Training Run',
         'Before launching a multi-hour fine-tuning job, run 100 steps on a single batch of 8-16 examples with no regularization (<code>weight_decay=0</code>, no dropout). Loss should reach near zero. If it does not, you have a bug: wrong masking (loss computed on prompt tokens), broken chat template, mismatched tokenizer, or learning rate orders of magnitude too low. This 5-minute check has saved countless wasted GPU-hours. If loss goes to zero, kill the run and launch properly.')),

    # M6: Track DPO reward margin
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html',
     '17.2.2',
     tip('Monitor the Reward Margin, Not Just the DPO Loss',
         'Log the mean chosen reward minus rejected reward at each step. This margin should grow during healthy DPO training. A margin stuck near zero means the model is not differentiating between chosen and rejected responses, even if the loss is decreasing (the loss can decrease by reducing confidence in BOTH responses equally). TRL\'s DPOTrainer logs this as <code>rewards/margins</code>; make it a primary dashboard metric, not just a sanity check.')),

    # === WAVE 10: 5 MORE POSTMORTEMS ===

    # PM6: Embedding model swap regression
    ('part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.3.html',
     '18.3',
     postmortem('The Silent Embedding-Model Swap',
                'A team upgraded their embedding model from <code>text-embedding-ada-002</code> to <code>text-embedding-3-small</code> for a 60% cost reduction. They re-indexed the corpus. Within a week, retrieval-quality complaints spiked 4&times;: queries returning unrelated documents. Root cause: they had embedded the corpus with the new model but the production query path still loaded a cached query-embedding model that used the OLD weights. New corpus vectors and old query vectors lived in different embedding spaces; cosine similarity between them was meaningless. Fix: explicit version tag on every index entry; on query, verify embedding-model version matches index version, fail loudly if not. Lesson: embedding-model upgrades require atomic switchover of BOTH the indexer AND the query encoder, with a regression eval in between.')),

    # PM7: Synthetic data poisoning
    ('part-4-training-adapting/module-14-synthetic-data/section-14.3.html',
     '14.3',
     postmortem('The 5% That Poisoned the Pretrain',
                'Team F pretrained a 7B model on a curated corpus where 5% of the data was synthetically generated (to fill gaps in technical writing). Loss curves looked clean throughout training. After deployment, the model showed strange repetition patterns and a tendency to emit specific phrasings ("It is important to note that...") at unnaturally high frequency. Root cause: the synthetic-generation prompt had a stylistic tic that the model learned. The 5% concentration was enough to bias generation patterns even though it didn\'t move loss measurably. Fix: stylistic-diversity audit on synthetic data; cap synthetic share at 1-2% per data domain; and at minimum run perplexity-based dedup against synthetic-vs-organic to detect over-clustering. Lesson: synthetic data does not need to be wrong to poison; it needs only to be uniform.')),

    # PM8: Quantization regression
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.1.html',
     '9.1',
     postmortem('The Math Benchmark That Quantization Killed',
                'Team G deployed an INT4 quantized version of their fine-tuned 13B model in production. End-to-end accuracy on their internal eval dropped 1pp &mdash; acceptable. Two weeks in, math-heavy customer queries showed 18pp accuracy drop. Internal eval had under-sampled math. Root cause: INT4 quantization preserves average-case behavior but destroys precision for arithmetic where small numerical errors compound across reasoning steps. Fix: stratified eval covering math, code, reasoning, and other arithmetic-sensitive categories before any quantization-level deployment. Use INT8 or BF16 for arithmetic-heavy queries (route by classifier). Lesson: aggregate accuracy metrics hide subgroup-specific regressions; always stratify your eval by capability category.')),

    # === WAVE 10: 5 MORE PRODUCTION PATTERNS ===

    # P6: Per-user budget caps
    ('part-9-safety-strategy/module-31-strategy-product-roi/section-31.7.html',
     '31.7',
     pattern('P6', 'Per-User Token Budget Caps',
             'Every user account is bound by a hard monthly token budget enforced at the gateway, not by application logic. Free tier 100K tokens/month, paid tier 1M tokens/month, etc. The budget tracker increments on every API call; once exhausted, requests return 429 until the next billing period.',
             'Single-tenant internal tools where users are trusted (employees) and unit-economics are bounded by salary not API spend.')),

    # P7: Provider router with classifier
    ('part-3-working-with-llms/module-11-llm-apis/section-11.4.html',
     '11.4',
     pattern('P7', 'Difficulty-Aware Model Routing',
             'A small classifier (or LLM-as-router with a cheap model) inspects each query and routes to the appropriate model: simple FAQ queries to a 7B model, complex reasoning to GPT-4o, math to a reasoning model. Logged routing decisions enable continuous improvement of the classifier.',
             'Single-domain applications where queries are uniform in difficulty (e.g., a code-completion endpoint with one model). The router\'s overhead exceeds its value when there\'s no real difficulty distribution to exploit.')),

    # P8: Prompt-caching strategy
    ('part-3-working-with-llms/module-11-llm-apis/section-11.2.html',
     '11.2',
     pattern('P8', 'Aggressive Prompt-Caching for Static System Prompts',
             'Use provider-side prompt caching (Anthropic, OpenAI) for system prompts that don\'t change between requests. The first request pays full price; subsequent requests with the same prefix pay 10-90% less. Saves both cost and TTFT. Tag long static prefixes (system instructions, few-shot examples, retrieved context) with cache-control breakpoints.',
             'Highly variable prompts where the cacheable prefix is short relative to the variable suffix. The cache hit rate must exceed ~30% to break even on the cache-write overhead.')),

    # P9: LLM judge with calibration set
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html',
     '28.8',
     pattern('P9', 'LLM Judge with Periodic Human Calibration',
             'Use an LLM as judge for routine eval (cheap, scalable). Maintain a small (200-500 examples) human-judged calibration set. Periodically (weekly) run the LLM judge against the calibration set; report agreement rate (Cohen\'s kappa). When agreement drops below a threshold (e.g., kappa &lt; 0.6), pause LLM-judged decisions until the judge model or prompt is recalibrated.',
             'Domains where ground-truth is genuinely unavailable (creative writing, novel research). Without a calibration anchor, LLM judges drift unmonitored.')),

    # P10: Eval-driven canary deploy
    ('part-8-evaluation-production/module-29-production-engineering/section-29.4.html',
     '29.4',
     pattern('P10', 'Shadow-Eval Canary Deploys',
             'After each prompt or model change, route 5% of live traffic to BOTH old and new versions for 24h. Run an LLM-as-judge on the paired outputs. Alert if the new version loses on more than 15% of comparisons. Auto-promote if the new version wins by &gt;10% with statistical significance.',
             'Pre-launch or single-developer projects with no users yet. Canary infrastructure has setup cost; pay it once you have enough traffic that 5% provides statistical signal in a day.')),
]


def main() -> int:
    n_added = 0
    n_skip = 0
    n_missing = 0
    for rel_path, h2_prefix, body in INSERTIONS:
        p = ROOT / rel_path
        if not p.exists():
            print(f'  MISSING: {rel_path}')
            n_missing += 1
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if body[:200] in text:
            n_skip += 1
            continue
        for pat in (re.compile(r'<h2[^>]*>([^<]*)</h2>', re.IGNORECASE),
                    re.compile(r'<h3[^>]*>([^<]*)</h3>', re.IGNORECASE)):
            inserted = False
            for m in pat.finditer(text):
                if m.group(1).strip().startswith(h2_prefix):
                    ins = m.end()
                    new = text[:ins] + '\n' + body + text[ins:]
                    p.write_text(new, encoding='utf-8')
                    n_added += 1
                    inserted = True
                    print(f'  added: {rel_path} (after "{h2_prefix}")')
                    break
            if inserted:
                break
        if not inserted:
            print(f'  NOT FOUND "{h2_prefix}" in {rel_path}')
    print(f'\nAdded {n_added}; skipped {n_skip}; missing {n_missing}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
