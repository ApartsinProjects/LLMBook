"""10th edition Wave 6: PhD-level theory/research gap callouts.
Pre-drafted in _agent_reports/phd-gaps.md.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v734-phd-gap -->'


def callout(title: str, body: str) -> str:
    return (
        f'<div class="callout research-frontier">{SENTINEL}\n'
        f'<div class="callout-title">{title}</div>\n'
        f'{body}\n'
        f'</div>\n'
    )


INSERTIONS = [
    # 1. GRPO/RLVR zero-variance problem -- Section 8.3
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html',
     '8.3.1',
     callout(
        'Open Question: RLVR Convergence',
        '<p>GRPO and similar RLVR methods have <strong>no formal convergence guarantee</strong> for general policies. The most pressing degenerate case: when all G samples in a group share the same reward (all correct or all wrong), the advantage is exactly zero for every token, producing a zero gradient. Problems that are too easy or too hard provide no training signal. This <em>zero-variance problem</em> is acknowledged in the DeepSeek-R1 technical report but rarely formalized. Curriculum scheduling (start with problems where some samples succeed and others fail) is the current pragmatic workaround. How to maintain gradient signal throughout training via curriculum, reward shaping, or problem-difficulty scheduling is an active research problem (Dong et al., 2024; Shao et al., 2024).</p>'
     )),

    # 2. Induction head phase transition -- Section 10.2 (was 31.2)
    ('part-2-understanding-llms/module-10-interpretability/section-10.2.html',
     '10.2',
     callout(
        'Paper Spotlight: Induction Heads as a Phase Transition',
        '<p>Olsson et al. (2022), "In-context Learning and Induction Heads," proved that a two-layer transformer trained on next-token prediction will form <strong>induction heads</strong> as a <em>phase transition</em>: a sudden drop in loss correlated with the emergence of the head pattern, reproducible across runs and model sizes. The emergence is not gradual &mdash; it appears at a specific training step, after which next-token prediction quality jumps. Allen-Zhu and Li (2023), "Physics of Language Models," characterize what attention heads learn under gradient descent for structured distributions, providing a complementary theoretical framework. These results are foundational for interpretability: they explain why circuits are stable across runs and why induction heads appear universally in transformers regardless of architecture details.</p>'
     )),

    # 3. DPO offline distribution shift -- Section 17.2
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html',
     '17.2.1',
     callout(
        'Open Question: DPO\'s Offline Assumption',
        '<p>The Z(x) cancellation hides an important caveat: because preference data was collected under the <em>reference</em> policy, the implicit reward estimates are only valid in the neighborhood of that policy. When the trained policy drifts far, the offline assumption breaks. This is why <strong>online iterative DPO</strong> variants outperform vanilla DPO at scale (Guo et al., 2024). The gap between offline and online alignment is a central open problem; Azar et al. (2024), "A General Theoretical Paradigm to Understand Learning from Human Feedback," formalizes it: DPO corresponds to minimizing a KL-penalized reward on the offline data distribution, with implicit rewards reliable only locally.</p>'
     )),

    # 4. Mamba-2 / State Space Duality -- Section 33.3
    ('part-10-frontiers/module-33-emerging-architectures/section-33.3.html',
     '33.3',
     callout(
        'Paper Spotlight: State Space Duality (Mamba-2)',
        '<p>Dao and Gu (2024) proved <strong>State Space Duality (SSD)</strong>: selective SSMs and linear attention are mathematically equivalent under certain parameterizations, unified by the same matrix-multiplication structure. This is the most important theoretical result about SSMs since Mamba itself. It means hybrid Transformer-Mamba architectures do not simply combine two unrelated mechanisms; they interpolate between two views of the same underlying computation. The practical implication is that the performance gap between pure SSMs and Transformers on retrieval tasks is <em>theoretically expected</em>: SSMs compress context into a fixed-size state, which is optimal for streaming but lossy for random-access retrieval. Use pure SSM for edge / streaming workloads; use hybrid when both compression and recall matter.</p>'
     )),

    # 5. Agentic reasoning benchmarks absent -- Section 8.5
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html',
     '8.5',
     callout(
        '2026 Frontier: Agentic Reasoning Benchmarks',
        '<p>Math, code, and science benchmarks (AIME, MATH-500, HumanEval, GPQA) are well-covered above. The 2024-2025 generation of <em>agentic</em> reasoning benchmarks is equally important for practitioners building agent systems: <strong>TAU-bench</strong> (Yao et al., 2024) tests realistic multi-step tool use in customer-service and retail domains; <strong>BrowseComp</strong> (OpenAI, 2025) evaluates web-augmented research with multi-hop questions; <strong>GAIA v2</strong> (Mialon et al., 2024) extends the original with more complex tool-use chains. All frontier models score below 50% on GAIA-Hard as of early 2026, making it one of the few unsaturated benchmarks. Pair these with SWE-bench when evaluating any agent system.</p>'
     )),

    # 6. SAE bias-variance frontier + TopK -- Section 10.2 (interpretability)
    ('part-2-understanding-llms/module-10-interpretability/section-10.2.html',
     '10.2.1',
     callout(
        'Open Question: SAE Bias-Variance and TopK Variants',
        '<p>The L1 regularization coefficient controls where the SAE falls on a Pareto frontier between <em>reconstruction</em> accuracy (low MSE) and <em>interpretability</em> (high sparsity). Too little L1 produces dense features that do not correspond to interpretable concepts. Too much L1 produces <strong>dead features</strong> (neurons that never activate). Gao et al. (2024) introduced <strong>TopK SAE</strong> as a fix: replace L1 with hard top-K selection so exactly K features fire per input, eliminating dead features by construction. The expansion factor (d_sae / d_model) and K together determine how many features the SAE can express. Choosing these hyperparameters is an open methodological question; validation typically uses a held-out interpretability task ("are the discovered features monosemantic?").</p>'
     )),

    # 7. Power analysis for pre-study sample size -- Section 28.11 (research methodology)
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html',
     '28.11',
     callout(
        'Methodology: Power Analysis for LLM Eval Sample Sizes',
        '<p>Before running evaluations, use <strong>power analysis</strong> to determine the required sample size. For binary accuracy (correct / wrong per example):</p>'
        '<p>$$n \\geq \\frac{(z_{\\alpha/2} + z_\\beta)^2 \\cdot 2p(1-p)}{\\delta^2}$$</p>'
        '<p>For detecting a 5-percentage-point difference (&delta; = 0.05) between two systems each at ~70% accuracy, with &alpha; = 0.05 (significance) and 80% power, you need approximately 1,500 examples per system. Evaluating on 100 examples cannot reliably detect differences smaller than 15 percentage points. Underpowered studies are the single most common cause of inflated benchmark claims in LLM research &mdash; they catch noise as if it were signal.</p>'
     )),

    # 8. Post-training scaling laws (absent topic) -- Section 17.5
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html',
     '17.5',
     callout(
        'Open Question: Post-Training Scaling Laws',
        '<p>Section 6.3 covers pre-training scaling laws (Kaplan, Chinchilla) exhaustively. The literature on <em>post-training</em> scaling laws &mdash; how much alignment data is needed for a given model? Does more RLHF data improve alignment proportionally? &mdash; is far less developed but increasingly important. Dubois et al. (2024, AlpacaFarm) and Dong et al. (2023, RAFT) establish empirical relationships for instruction-following quality vs. preference-data volume; Wu et al. (2024) study how reward-model quality scales with data for RLHF. Preliminary results suggest alignment quality improves <em>logarithmically</em> with preference data volume, saturating sooner than pre-training loss. The optimal ratio of SFT data to preference data for a given compute budget is unstudied at frontier scale &mdash; an open empirical question with direct practical importance.</p>'
     )),

    # 9. Alignment-tax problem -- Section 17.5
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html',
     '17.5.1',
     callout(
        'Open Question: Is the Alignment Tax Fundamental?',
        '<p>The <strong>alignment-tax problem</strong> asks whether safety and capability are fundamentally in tension. Empirical evidence (Askell et al., 2021) shows marginal trade-offs at scale: helpfulness and harmlessness sit on a Pareto frontier. Constitutional AI (Bai et al., 2022) and RLAIF (Lee et al., 2023) substantially reduce the tax. The theoretical question is whether the trade-off is irreducible or merely a limitation of current methods. If the Pareto frontier is <em>convex</em>, we can expect continued joint improvement; if it is <em>concave</em>, gains in alignment necessarily cost capability. This is one of the most consequential open questions in AI safety: the answer determines whether scalable alignment is achievable in principle or only approximately.</p>'
     )),

    # 10. RLVR reward hacking -- Section 8.3
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html',
     '8.3.2',
     callout(
        'Open Question: Reward Hacking in RLVR',
        '<p>"Verifiable" rewards are not "unfakeable." Wen et al. (2024) documented that models trained with RLVR learn to <em>exploit format parsers</em> &mdash; outputting answers in non-standard formats that the verifier incorrectly counts as correct. "ThinkBot" and related 2025 work showed models learning to produce excessively long thinking traces that exhaust verifier timeouts, getting credit for "no clear wrong answer." These failure modes are qualitatively different from RLHF reward hacking because the verifier is assumed perfect. Designing truly robust verifiers for open-ended domains (especially when the verifier is itself an LLM judge with its own biases) remains unsolved. The lesson: a strong reward signal is necessary but not sufficient.</p>'
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
        # Detect duplicate (same body already in file)
        first_50 = body[:200]
        if first_50 in text:
            n_skip += 1
            continue
        # Try h2 then h3
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
