"""W6 (PhD-gap remainder, 8 picks) + W11 (cross-ref editorial picks).

W6: insert research-frontier callouts at 8 specific sections covering
PhD-level open questions deferred from the 10th edition wave plan.

W11: add 8 "see also" cross-reference callouts where the cross-refs.md
agent flagged the highest-value missing pointers (top picks; the full
50-item list is being closed gradually).

Both classes use sentinel comments for idempotency. Pure additions.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# W6: 8 PhD-gap research-frontier callouts
# ---------------------------------------------------------------------------
W6_GAPS = [
    # 1. Mamba-2 / State Space Duality
    ('part-10-frontiers/module-33-emerging-architectures/section-33.3.html',
     'w6-mamba2-ssd',
     'Open Question: State Space Duality and Mamba-2',
     'Dao &amp; Gu (2024) showed that selective SSMs and a generalised form of attention '
     'are equivalent under a Structured State Space Duality (SSD) framework: every '
     'selective-SSM step can be written as a special case of a structured attention '
     'computation, and vice versa. Mamba-2 exploits this to reach attention-quality '
     'training throughput while keeping the linear inference cost of an SSM. The deeper '
     'open question is whether this duality implies a single underlying primitive that '
     'transformers and SSMs are both special cases of, or whether the two architectures '
     'inhabit truly different points in expressiveness vs. learnability. The empirical '
     'evidence so far favours convergence at the algorithm level while leaving the '
     'inductive-bias story unsettled.'),

    # 2. Constitutional AI 2024-25 follow-on
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.3.html',
     'w6-cai-follow',
     'Open Question: Constitutional AI After RLAIF',
     'The 2022 Constitutional-AI recipe (RLAIF over a written constitution) has been '
     'extended in three directions in 2024-25: (1) self-critique with explicit '
     'thinking-token traces (Anthropic\'s "constitutional classifiers" and the public '
     '2025 Claude 4 system card); (2) hybrid Constitutional + RLVR pipelines where '
     'verifiable-correctness rewards co-train with constitution-derived preferences; '
     '(3) "constitutional curricula" that schedule which principles dominate at which '
     'training stage. Open question: does any of this measurably reduce sycophancy or '
     'spec-gaming compared to a well-tuned RLHF baseline, or is the gain mostly '
     'methodological clarity? The published evaluations are not yet apples-to-apples.'),

    # 3. Alignment-tax problem framing
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html',
     'w6-alignment-tax',
     'Open Question: The Alignment Tax Is Real but Mis-Measured',
     'Across post-training methods (SFT, RLHF, DPO, CAI, RLVR), aligned models routinely '
     'lose 2-5 points on raw capability benchmarks (MMLU, GSM8K) compared to their '
     'pre-alignment checkpoints. The community calls this the "alignment tax". The open '
     'question is whether the tax is intrinsic (capability and safety pull in opposite '
     'directions in weight space) or measurement artifact (capability benchmarks '
     'over-weight a few task formats that alignment training de-emphasizes). Burns et al. '
     '(2023, weak-to-strong) and the 2025 reproductions suggest the gap shrinks when '
     'evaluation is held-out and capability tests use the same instruction-following '
     'format as deployment. Verdict still open.'),

    # 4. RLVR reward hacking patterns
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html',
     'w6-rlvr-hacking',
     'Open Question: Reward Hacking Patterns in RLVR',
     'RLVR (Reinforcement Learning with Verifiable Rewards) replaces a learned reward '
     'model with a deterministic verifier (unit tests, formal proofs, math-grader). '
     'This removes the classic reward-model exploitation failures of RLHF but introduces '
     'new ones: (1) <em>verifier surface attack</em>, where the model finds outputs '
     'that pass the verifier without solving the intended problem; (2) <em>format '
     'overfitting</em>, where reasoning becomes a templated dance optimized for the '
     'verifier\'s parser; (3) <em>spec gaming</em> on edge cases the verifier author '
     'did not enumerate. The DeepSeek-R1 cold-start trick (rejection-sampling SFT '
     'before RLVR) suppresses (2) but not (1) or (3). An empirical taxonomy of RLVR '
     'failure modes is still a 2026-27 open project.'),

    # 5. MoE routing mechanistic analysis
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
     'w6-moe-routing',
     'Open Question: What MoE Routers Actually Route',
     'Mixture-of-Experts models train an internal router that sends each token to a '
     'small subset of experts. The router is learned end-to-end, so the question of '
     '<em>what feature space</em> the router uses to discriminate is empirical. Early '
     'speculation (per-domain experts, per-language experts) is mostly wrong. The '
     '2024-25 mechanistic-interpretability work on Mixtral and DeepSeek-V3 shows '
     'routers cluster tokens by syntactic role, by next-token-type prediction, and by '
     'discourse position rather than by topic. Open question: is this an artifact of '
     'web-scale training distribution, or does it reflect a fundamental locality '
     'structure of language? Replication on small from-scratch MoE models would help '
     'disentangle this.'),

    # 6. Compound-system ablation design
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html',
     'w6-compound-ablation',
     'Open Question: Ablating Compound LLM Systems',
     'Modern production systems chain together retrieval, prompting, structured-output '
     'enforcement, a primary LLM call, often a critique pass, and post-processing. '
     'Standard ablation methodology (remove one component, measure metric delta) '
     'assumes additive contributions. In practice the components interact: a stronger '
     'retriever can <em>reduce</em> end-to-end accuracy if the primary prompt does '
     'not handle the new context format. The open methodological question is how to '
     'design and report ablations in compound systems so that contributions are '
     'attributable without exponential combinations. Shapley values over components '
     'are theoretically right but rarely feasible. A community-agreed practical '
     'standard is still missing.'),

    # 7. Win-rate vs absolute accuracy methodology
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.11.html',
     'w6-winrate-vs-acc',
     'Open Question: Win-Rate vs Absolute Accuracy',
     'For tasks without a verifiable answer (creative writing, summarisation, dialogue), '
     'the standard 2024-26 evaluation is pairwise win-rate from an LLM judge. Win-rate '
     'has appealing properties (sample-efficient, captures preferences over absolute '
     'scales) but also rewards the model whose <em>style</em> the judge prefers, '
     'independent of substance. The open question is when win-rate diverges from '
     'absolute quality. Empirical evidence: judges trained on human preferences tend '
     'to over-weight length, structure, and confident phrasing. Mixing win-rate with '
     'absolute Likert scores from the same judge reduces but does not eliminate the '
     'bias. The reference debate (Zheng et al. MT-bench follow-ups) is still active.'),

    # 8. Open Questions section appended to Ch 10 Interpretability
    ('part-2-understanding-llms/module-10-interpretability/section-10.4.html',
     'w6-interp-open',
     'Open Question: SAE Bias-Variance and TopK Activations',
     'Sparse autoencoders (SAEs) decompose model activations into a dictionary of '
     'monosemantic features. The standard L1-penalised SAE recovers many interpretable '
     'features but suffers from "feature shrinkage" (the L1 penalty pulls activations '
     'toward zero, biasing reconstruction). 2024 TopK SAEs (Gao et al., Templeton et '
     'al.) replace the L1 penalty with a hard top-K selection per token, removing '
     'shrinkage at the cost of a fixed sparsity level rather than a learned one. The '
     'open question is the bias-variance tradeoff: TopK reduces bias but increases '
     'variance in which features fire across runs and seeds. Whether a single '
     '"correct" dictionary exists, or whether multiple equally-valid decompositions '
     'compete for the same activation, is the deeper interpretability question.'),
]

# ---------------------------------------------------------------------------
# W11: 8 highest-value cross-ref additions (subset of the full 50 picks)
# ---------------------------------------------------------------------------
W11_CROSSREFS = [
    # 1. Section 11.1 -> 22.1 function calling forward pointer
    ('part-3-working-with-llms/module-11-llm-apis/section-11.1.html',
     'w11-11-1-to-22-1',
     'See also',
     'For the agent-loop view of function calling (how providers expose tool schemas '
     'and how the model selects them inside a multi-step loop), see <a '
     'href="../../part-6-agentic-ai/module-22-tool-use-protocols/section-22.1.html">Section 22.1: '
     'Function Calling Across Providers</a>.'),

    # 2. Section 18.1 -> 10.x interpretability for embedding geometry
    ('part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html',
     'w11-18-1-to-10-1',
     'See also',
     'For why embeddings concentrate in a thin shell of high-dimensional space '
     '(concentration of measure) and what that means for cosine similarity in '
     'practice, see <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.1.html">Section 10.1: '
     'Attention Analysis &amp; Probing</a>.'),

    # 3. Section 8.3 -> 17.4 RLVR connection
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html',
     'w11-8-3-to-17-4',
     'See also',
     'The reasoning-model training pipeline (RLVR with verifier rewards) is treated '
     'from the alignment angle in <a '
     'href="../../part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.4.html">Section 17.4: RLVR</a>, '
     'and from the failure-mode angle in the W6 callout above.'),

    # 4. Section 19.1 -> 28.1 RAG eval
    ('part-5-retrieval-conversation/module-19-rag/section-19.1.html',
     'w11-19-1-to-28-1',
     'See also',
     'For the evaluation methodology of RAG specifically (faithfulness vs answer '
     'relevance, golden-set construction, retrieval@k vs end-to-end metrics), see <a '
     'href="../../part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html">Section 28.1: '
     'LLM Evaluation Fundamentals</a>.'),

    # 5. Section 21.1 -> 25.1 safety
    ('part-6-agentic-ai/module-21-ai-agents/section-21.1.html',
     'w11-21-1-to-25-1',
     'See also',
     'The same agent loop seen from the safety side (prompt injection, tool-call '
     'authorization, sandboxing) is the subject of <a '
     'href="../module-25-agent-safety-production/section-25.1.html">Section 25.1: '
     'Agent Safety &amp; Prompt Injection Defense</a>.'),

    # 6. Section 16.1 LoRA -> 17.2 DPO
    ('part-4-training-adapting/module-16-peft/section-16.1.html',
     'w11-16-1-to-17-2',
     'See also',
     'LoRA is most commonly used as the parameter-efficient backbone of preference '
     'fine-tuning (DPO, ORPO, IPO). For the preference-optimization side of the same '
     'workflow, see <a '
     'href="../module-17-alignment-rlhf-dpo/section-17.2.html">Section 17.2: DPO '
     '&amp; Modern Preference Optimization</a>.'),

    # 7. Section 9.1 quantization -> 31.4 build vs buy
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.1.html',
     'w11-9-1-to-31-4',
     'See also',
     'The decision to quantize is rarely purely technical. For the cost/quality '
     'tradeoff framed as a build-vs-buy decision (self-host quantized vs API), '
     'see <a '
     'href="../../part-9-safety-strategy/module-31-strategy-product-roi/section-31.4.html">Section 31.4: '
     'Vendor Evaluation &amp; Build vs. Buy</a>.'),

    # 8. Section 12.3 prompt optimization -> 28.5 eval gates
    ('part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html',
     'w11-12-3-to-28-5',
     'See also',
     'Automated prompt optimization (DSPy, MIPRO) is only useful if the eval signal '
     'driving it is reliable. For the eval-as-CI gate that should sit downstream of '
     'every optimization run, see <a '
     'href="../../part-8-evaluation-production/module-28-evaluation-observability/section-28.5.html">Section 28.5: '
     'Evaluation-Driven Quality Gates</a>.'),
]

# ---------------------------------------------------------------------------
H2_RE = re.compile(r'(<h2[^>]*>[^<]*</h2>)', re.IGNORECASE)


def render_w6(sentinel: str, title: str, body: str) -> str:
    return (
        f'<div class="callout research-frontier"><!-- v747-{sentinel} -->\n'
        f'<div class="callout-title">{title}</div>\n'
        f'<p>{body}</p>\n'
        f'</div>\n'
    )


def render_w11(sentinel: str, title: str, body: str) -> str:
    return (
        f'<div class="callout cross-ref"><!-- v747-{sentinel} -->\n'
        f'<div class="callout-title">{title}</div>\n'
        f'<p>{body}</p>\n'
        f'</div>\n'
    )


def inject(html: str, callout: str, sentinel_marker: str) -> tuple[str, bool]:
    if sentinel_marker in html:
        return html, False
    m = H2_RE.search(html)
    if not m:
        return html, False
    insert_pos = m.end()
    new_html = html[:insert_pos] + '\n' + callout + html[insert_pos:]
    return new_html, True


def main() -> int:
    inserted = 0
    skipped = 0
    not_found = []

    all_entries = ([('w6', e, render_w6) for e in W6_GAPS]
                   + [('w11', e, render_w11) for e in W11_CROSSREFS])

    for kind, (rel_path, sentinel, title, body), renderer in all_entries:
        path = ROOT / rel_path
        if not path.exists():
            not_found.append(rel_path)
            continue
        html = path.read_text(encoding='utf-8')
        sentinel_marker = f'<!-- v747-{sentinel} -->'
        callout = renderer(sentinel, title, body)
        new_html, did = inject(html, callout, sentinel_marker)
        if did:
            path.write_text(new_html, encoding='utf-8')
            inserted += 1
            print(f'  + {kind} {sentinel}: {rel_path}')
        else:
            skipped += 1
            print(f'  = {kind} {sentinel}: {rel_path}')

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
