"""10th edition Wave 3: insert 8 deep-insight callouts at high-impact
sections. Pre-drafted in _agent_reports/deep-insights.md.

Each callout uses the `<div class="callout key-insight">` style and is
inserted RIGHT AFTER the first <h2> in the target section (so it
appears prominently near the top).

Idempotent: sentinel `<!-- v731-deep-insight -->`.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v731-deep-insight -->'


def callout(title: str, body: str) -> str:
    return (
        f'<div class="callout key-insight">{SENTINEL}\n'
        f'<div class="callout-title">{title}</div>\n'
        f'{body}\n'
        f'</div>\n'
    )


# Each entry: (path, h2_prefix, callout_html)
# Post-renumber: Ch 31 (Interp) -> Ch 10; Ch 10-30 shift +1; Ch 32-34 shift +1
INSERTIONS = [
    # 1. Exposure bias / teacher forcing gap -- Section 3.3
    ('part-1-foundations/module-03-sequence-models-attention/section-3.3.html',
     '3.3',
     callout(
        'Mental Model: Exposure Bias and the Teacher-Forcing Gap',
        '<p>During training, the model at each position sees the <em>true</em> previous token from the ground-truth sequence (teacher forcing). At inference, that previous token is the model\'s own prediction, which may be wrong. If the model makes an error at step 5, step 6 now operates on input it never saw during training. Researchers call this <strong>exposure bias</strong>. It explains why models can produce fluent but hallucinated text: each token looks reasonable given local context, but small errors compound. Scheduled sampling (Bengio et al., 2015) and prefix-tuning approaches partially address this; no current training objective fully eliminates the gap. This is also why RLHF (which trains on model-generated sequences) tends to improve over SFT alone.</p>'
     )),

    # 2. Goodhart's Law -- Section 17.1 (was 16.1)
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html',
     '17.1',
     callout(
        'Mental Model: Reward Hacking as Goodhart\'s Law',
        '<p>This failure mode has a name in economics: <strong>Goodhart\'s Law</strong> (Charles Goodhart, 1975): "Any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes." The reward model was validated on the distribution of responses it was trained on. PPO then searches for outputs that maximize this proxy, inevitably finding regions where the proxy diverges from what it was measuring. The KL penalty is an engineering acknowledgment of Goodhart\'s Law: it limits how far the policy moves from the SFT distribution, which limits how far the proxy can be stretched. This same dynamic appears in every system that optimizes a learned proxy: RLVR reward models (Section 8.3), embedding quality metrics, evaluation benchmarks that become gameable once the community focuses on them.</p>'
     )),

    # 3. FFN as static content-addressable memory -- Section 4.1
    ('part-1-foundations/module-04-transformer-architecture/section-4.1.html',
     '4.1',
     callout(
        'Mental Model: FFN Layers as Static Memory',
        '<p>The FFN is computing the same operation as attention but with <em>static</em> rather than dynamic keys and values. When the input activates neuron j (because xW&#x2081; row-j exceeds zero after ReLU), the corresponding row of W&#x2082; is added to the residual stream &mdash; like retrieving the value associated with a key match. The difference from attention: FFN keys and values are baked into the weights and cannot change at inference, while attention keys and values are recomputed from current context. This explains an empirical pattern: factual knowledge (Paris is the capital of France) lives in FFN layers and can be edited by patching individual FFN rows (Geva et al., 2021). Grammatical and syntactic patterns, which integrate information across positions, live in attention. The two are complementary memory systems at different timescales, not redundant.</p>'
     )),

    # 4. Three sources of irreducible loss -- Section 6.3
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
     '6.3',
     callout(
        'Mental Model: Three Sources of the Loss Floor',
        '<p>The irreducible loss L<sub>&infin;</sub> conflates three distinct sources of unpredictability. First, <strong>semantic ambiguity</strong>: "The doctor told the nurse she should..." has multiple valid completions. Second, <strong>stylistic variation</strong>: identical semantic intent, different word choices, and the model cannot predict which an author will make. Third, <strong>data noise</strong>: OCR errors, encoding artifacts, duplicate documents with inconsistent content. <em>Only the third is reducible through data curation.</em> A cleaner corpus genuinely lowers effective L<sub>&infin;</sub>, which is why the Llama 3 data team\'s 90% filtering rate produced measurably better models than raw Common Crawl at the same token count. When your model\'s loss plateaus, ask: am I hitting the linguistic floor, or the data-quality floor?</p>'
     )),

    # 5. KV cache as lossless reuse -- Section 9.2
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.2.html',
     '9.2',
     callout(
        'Mental Model: KV Cache as Lossless Computation Reuse',
        '<p>The O(n&sup2;) complexity of uncached generation is worth making concrete. To generate token k, attention must compute K, V for all k positions and run attention against all k keys. Without caching, this happens fresh for each of n tokens we generate: 1 + 2 + ... + n = n(n+1)/2 = O(n&sup2;). What makes KV cache different from a general cache: <em>its entries can never be invalidated.</em> Key and value projections for position 5, given tokens 1-5, do not change when you generate position 6, 7, or 100. Past context is frozen. KV cache is not approximation or heuristic &mdash; it is lossless reuse of computation that cannot possibly differ. Memory cost (linear in sequence length &times; batch size) is the exact price for converting quadratic compute to linear.</p>'
     )),

    # 6. Concentration of measure -- Section 19.1 (was 17.1)
    # The embeddings chapter, post-renumber is module-18-embeddings-vector-db at section-18.1
    ('part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.1.html',
     '18.1',
     callout(
        'Mental Model: Concentration of Measure in High-Dim Spaces',
        '<p>There is a geometric reason cosine similarity can mislead in high dimensions: <strong>concentration of measure</strong>. In d-dim space, randomly drawn unit vectors have pairwise cosine similarities concentrating tightly around zero, std dev &approx; 1/&radic;d. In 768-dim BERT, std dev &approx; 0.036. The similarity between a query and a completely irrelevant document may differ from the similarity to the most relevant document by only 0.1-0.3 units. Small differences become significant decisions. Concentration also explains why approximate-nearest-neighbor algorithms can skip large fractions of the search space and still achieve 95%+ recall: if most vectors have similar similarity scores, the true nearest and second-nearest are often nearly interchangeable. Calibrate similarity thresholds empirically on YOUR embedding model and corpus &mdash; do not borrow them across domains.</p>'
     )),

    # 7. GRPO as Monte Carlo value estimation -- Section 8.3
    ('part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html',
     '8.3',
     callout(
        'Mental Model: GRPO as Monte Carlo Value Estimation',
        '<p>GRPO\'s within-group normalization is not merely a computational trick; it is a <strong>Monte Carlo approximation</strong> of the value function that PPO\'s critic would compute. The PPO critic estimates V(s) = E[r|s] for any state. GRPO estimates the same quantity empirically: sample G completions, take their mean reward. The advantage A&#x1d62; = (r&#x1d62; - r&#x0304;)/&sigma; measures how much better solution i is than average. The practical implication: variance is controlled by G, the group size. Larger G = more accurate value estimate (and more stable training) at G&times; more inference cost per training step. The failure mode is reward homogeneity: if all G samples receive the same reward (all correct or all wrong), the standard deviation is zero, the advantage is undefined, training produces no update. This "dead zone" is why RLVR training stalls on problems that are simultaneously too easy and too hard.</p>'
     )),

    # 8. Why LoRA targets attention not FFN -- Section 16.1 (was 15.1)
    ('part-4-training-adapting/module-16-peft/section-16.1.html',
     '16.1',
     callout(
        'Mental Model: Why LoRA Targets Attention, Not FFN',
        '<p>A natural question: why does LoRA target attention matrices rather than FFN layers that contain most of the parameters? The answer connects to the functional distinction. FFN layers store factual knowledge as <em>static</em> key-value pairs baked into weights (see Section 4.1). Adapting FFN rows overwrites stored facts &mdash; expensive, risks erasing useful pre-trained knowledge. Attention projections, by contrast, determine how tokens route information: which positions can speak to which. Adapting Q, K, V, O reshapes routing patterns without touching factual stores. This is why fine-tuning with LoRA applied only to attention achieves strong task performance with minimal catastrophic forgetting: you are teaching new communication patterns while leaving knowledge intact. When a task requires injecting genuinely new factual knowledge (not just new behavior), LoRA on FFN or full fine-tuning becomes necessary.</p>'
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
        if SENTINEL in text:
            n_skip += 1
            continue
        # Find first h2 whose inner text starts with h2_prefix
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
            print(f'  NOT FOUND <h2>{h2_prefix} in {rel_path}')
    print(f'\nAdded {n_added}; skipped {n_skip}; missing {n_missing}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
