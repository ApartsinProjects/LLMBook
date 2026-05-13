"""10th edition Wave 4: 8 cross-field connection callouts. Pre-drafted
in _agent_reports/cross-field.md.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v732-cross-field -->'


def callout(title: str, body: str) -> str:
    return (
        f'<div class="callout key-insight">{SENTINEL}\n'
        f'<div class="callout-title">{title}</div>\n'
        f'{body}\n'
        f'</div>\n'
    )


INSERTIONS = [
    # 1. Attention as Hopfield network -- Section 3.3
    # But Wave 3 already injected an insight at Section 3.3. Use Section 3.3.3 (sub-section) or skip.
    # Use Section 3.2 (attention mechanism)
    ('part-1-foundations/module-03-sequence-models-attention/section-3.2.html',
     '3.2',
     callout(
        'Cross-Field: Attention as Associative Memory',
        '<p>Scaled dot-product attention is mathematically equivalent to memory retrieval in a continuous Hopfield network (Ramsauer et al., 2020). The keys are stored memory patterns; the query is a noisy cue; the softmax selects the closest match. This framing makes two things predictable. First, retrieval degrades when multiple keys are similar to the query, producing "blended" value outputs rather than a clean lookup. Second, the softmax temperature acts as a signal-to-noise knob: lower temperature sharpens retrieval; higher temperature averages across similar memories. Both effects appear measurably in production attention heatmaps.</p>'
     )),

    # 2. Phase transitions / percolation -- Section 33.1
    ('part-10-frontiers/module-33-emerging-architectures/section-33.1.html',
     '33.1',
     callout(
        'Cross-Field: Capability Thresholds as Percolation Phase Transitions',
        '<p>For a k-step reasoning task where each step has accuracy p, end-to-end accuracy &asymp; p&#x1d4f;. This is mathematically identical to the percolation problem in statistical physics: a network "conducts" only when enough links individually conduct. The implication is predictive: the capability transition occurs when p crosses roughly (target accuracy)<sup>1/k</sup>. For a 5-step chain needing 50% end-to-end success, each step needs roughly 87% accuracy (0.87&#8309; &asymp; 0.5). When a model falls below this per-step threshold, <em>task decomposition</em> (breaking into fewer, easier steps) is the correct engineering intervention, not prompt rephrasing. Reference: Arora &amp; Goyal (2023).</p>'
     )),

    # 3. SSMs as Kalman filters -- Section 33.3
    ('part-10-frontiers/module-33-emerging-architectures/section-33.3.html',
     '33.3',
     callout(
        'Cross-Field: SSMs as Kalman Filters Without Noise Tracking',
        '<p>State space models (S4, Mamba) are linear dynamical systems: exactly the structure of a Kalman filter, the gold standard of control-theoretic state estimation. The A matrix\'s eigenvalue spectrum controls memory: eigenvalues near the unit circle preserve information indefinitely; eigenvalues closer to zero cause exponential forgetting. S4\'s HiPPO initialization places eigenvalues specifically to represent polynomial history optimally &mdash; a result from approximation theory. When an SSM fails to recall a specific token from far back in a sequence, the control-theory framing tells you why: the eigenvalue controlling that timescale has decayed too fast.</p>'
     )),

    # 4. In-context learning as Bayesian inference -- Section 33.5
    ('part-10-frontiers/module-33-emerging-architectures/section-33.5.html',
     '33.5',
     callout(
        'Cross-Field: ICL as Bayesian Posterior Computation',
        '<p>Xie et al. (2021) showed that a large language model doing in-context learning behaves like a Bayesian learner: each demonstration updates an implicit posterior over the latent concept the examples represent. This predicts observable behavior. Good demonstrations should be diverse and representative (i.i.d. from the target distribution). Contradictory or biased examples corrupt the posterior and degrade performance measurably. If order of examples strongly affects output, the model is doing sequential rather than full Bayesian updating. Designing few-shot prompts <em>as if designing a Bayesian evidence set</em> produces more reliable results than trial-and-error.</p>'
     )),

    # 5. MoE as EM -- Section 33.3 (already has SSM at 33.3) -- use 33.3.1 or different anchor
    # Skip if 33.3 collides; use sub-heading. Try alternative approach: place at 33.3 with a different prefix match.
    # Actually let's place it in the chapter 6 pretraining sections that cover MoE -- section 6.3
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
     '6.3.7',  # MoE subsection
     callout(
        'Cross-Field: MoE Routing as Expectation-Maximization',
        '<p>A mixture-of-experts layer is a learned mixture model: the router outputs mixing weights; each expert is a conditional distribution. Training follows a hard-EM pattern: assign tokens to experts, update expert weights, repeat. This predicts <strong>expert collapse</strong> precisely: in EM, any component with a higher initial likelihood attracts more data and starves others. The standard fix in classical mixture modeling is adding a Dirichlet prior on mixing weights toward uniformity, which is exactly what the load-balancing auxiliary loss does. Tuning that loss coefficient is equivalent to tuning prior strength in a Bayesian mixture model.</p>'
     )),

    # 6. Boltzmann distribution -- Section 5.2
    ('part-1-foundations/module-05-decoding-text-generation/section-5.2.html',
     '5.2',
     callout(
        'Cross-Field: Sampling Temperature as a Boltzmann Distribution',
        '<p>The softmax over logits at temperature T is the Boltzmann distribution from statistical physics: P(token) = exp(logit/T) / Z, where Z is the partition function. T = 0 is absolute zero: the model always picks the single lowest-energy (highest-logit) token. Higher T populates higher-energy (lower-probability) states. Top-p sampling truncates the partition function at a free-energy threshold. These two parameters are not redundant: <strong>temperature sets the energy scale</strong> of the full distribution; <strong>top-p sets a hard ceiling</strong> on how far up the energy ladder the model can sample. Use both deliberately, not as arbitrary dials.</p>'
     )),

    # 7. Attention as differentiable database -- Section 4.1
    # Already has FFN insight at 4.1. Use a different anchor or skip.
    # Place at 4.2 (build from scratch) instead.
    ('part-1-foundations/module-04-transformer-architecture/section-4.2.html',
     '4.2',
     callout(
        'Cross-Field: Attention as a Differentiable Database',
        '<p>The QKV mechanism is a differentiable key-value store. Queries retrieve values by weighted similarity across all keys, exactly like a fuzzy database lookup. Unlike SQL, attention has no "null result": when no key closely matches the query, it still returns a weighted average of all values, weighted by imperfect similarity. This is the root cause of attention-based confabulation: the model retrieves a plausible but incorrect "nearest match" rather than reporting uncertainty. The KV cache (Chapter 9) is, from this perspective, simply a precomputed cache of database rows, subject to the same latency-versus-memory tradeoffs as any database cache.</p>'
     )),

    # 8. Campbell's law (alignment) -- Section 17.3 (constitutional AI) post-renumber
    # Wave 3 already added Goodhart at 17.1. Place this at 17.3 if exists, else 17.2.
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.3.html',
     '17.3',
     callout(
        'Cross-Field: Reward Hacking as Campbell\'s Law',
        '<p>Donald Campbell identified in 1979 that any quantitative measure used as a target becomes corrupted: "teaching to the test" in education, gaming mortality statistics in healthcare, optimizing GDP while degrading well-being. RLHF is the same phenomenon at the alignment layer. Campbell\'s research predicts the degree of corruption scales with optimization pressure and proxy-target gap. This gives practitioners two operational tools: (1) limit optimization pressure via KL penalty strength, and (2) use process reward models (step-level scoring) rather than outcome reward models, because it is harder to game many correlated measurements than one terminal score.</p>'
     )),
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
        if SENTINEL in text and body in text:
            n_skip += 1
            continue
        pat = re.compile(r'<h2[^>]*>([^<]*)</h2>', re.IGNORECASE)
        inserted = False
        for m in pat.finditer(text):
            if m.group(1).strip().startswith(h2_prefix):
                ins = m.end()
                new = text[:ins] + '\n' + body + text[ins:]
                p.write_text(new, encoding='utf-8')
                n_added += 1
                inserted = True
                print(f'  added: {rel_path} (after h2 "{h2_prefix}")')
                break
        if not inserted:
            # Try <h3> if h2 not found (for sub-sections like 6.3.7)
            pat3 = re.compile(r'<h3[^>]*>([^<]*)</h3>', re.IGNORECASE)
            for m in pat3.finditer(text):
                if m.group(1).strip().startswith(h2_prefix):
                    ins = m.end()
                    new = text[:ins] + '\n' + body + text[ins:]
                    p.write_text(new, encoding='utf-8')
                    n_added += 1
                    inserted = True
                    print(f'  added: {rel_path} (after h3 "{h2_prefix}")')
                    break
        if not inserted:
            print(f'  NOT FOUND <h2>/<h3>{h2_prefix} in {rel_path}')
    print(f'\nAdded {n_added}; skipped {n_skip}; missing {n_missing}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
