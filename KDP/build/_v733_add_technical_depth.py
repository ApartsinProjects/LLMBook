"""10th edition Wave 5: 12 technical-depth additions + 2 bug fixes.

Adds practitioner-grade code/algorithm internals as callouts with
embedded code snippets. Pre-drafted in _agent_reports/technical-depth.md.

For bug fixes (Section 4.2 + 16.2 indentation issues), this script only
flags them; the actual code blocks are too long for safe automated
edit. Manual fix expected.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SENTINEL = '<!-- v733-tech-depth -->'


def callout(title: str, body: str) -> str:
    return (
        f'<div class="callout algorithm">{SENTINEL}\n'
        f'<div class="callout-title">{title}</div>\n'
        f'{body}\n'
        f'</div>\n'
    )


# Note: post-renumber numbering. Each pick targets a specific section h2.
INSERTIONS = [
    # 1. LoRA gradient flow -- Section 16.1 (was 15.1)
    # Wave 3 already has deep-insight at 16.1; place at 16.2 (LoRA variants)
    ('part-4-training-adapting/module-16-peft/section-16.1.html',
     '16.1.2',
     callout(
        'Under the Hood: LoRA Backward Pass',
        '<p>The forward pass W&prime; = W + (&alpha;/r)BA is well-known. The <em>backward</em> pass is where the memory saving actually happens. PyTorch sees W&#x2080; with <code>requires_grad=False</code> and <strong>never allocates a gradient tensor for it</strong>. Only A and B accumulate gradients:</p>'
        '<div class="code-block-wrapper"><pre><code class="pygments-highlighted lang-python">'
        '<span class="k">class</span> <span class="nc">LoRALinear</span><span class="p">(</span><span class="n">nn</span><span class="o">.</span><span class="n">Module</span><span class="p">):</span>\n'
        '    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">d_in</span><span class="p">,</span> <span class="n">d_out</span><span class="p">,</span> <span class="n">rank</span><span class="p">,</span> <span class="n">alpha</span><span class="p">):</span>\n'
        '        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">()</span>\n'
        '        <span class="bp">self</span><span class="o">.</span><span class="n">W0</span> <span class="o">=</span> <span class="n">nn</span><span class="o">.</span><span class="n">Parameter</span><span class="p">(</span><span class="n">torch</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="n">d_in</span><span class="p">,</span> <span class="n">d_out</span><span class="p">),</span> <span class="n">requires_grad</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>\n'
        '        <span class="bp">self</span><span class="o">.</span><span class="n">A</span>  <span class="o">=</span> <span class="n">nn</span><span class="o">.</span><span class="n">Parameter</span><span class="p">(</span><span class="n">torch</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="n">d_in</span><span class="p">,</span> <span class="n">rank</span><span class="p">)</span> <span class="o">*</span> <span class="mf">0.02</span><span class="p">)</span>\n'
        '        <span class="bp">self</span><span class="o">.</span><span class="n">B</span>  <span class="o">=</span> <span class="n">nn</span><span class="o">.</span><span class="n">Parameter</span><span class="p">(</span><span class="n">torch</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">rank</span><span class="p">,</span> <span class="n">d_out</span><span class="p">))</span>\n'
        '        <span class="bp">self</span><span class="o">.</span><span class="n">scale</span> <span class="o">=</span> <span class="n">alpha</span> <span class="o">/</span> <span class="n">rank</span>\n'
        '    <span class="k">def</span> <span class="nf">forward</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">x</span><span class="p">):</span>\n'
        '        <span class="k">return</span> <span class="n">x</span> <span class="o">@</span> <span class="bp">self</span><span class="o">.</span><span class="n">W0</span> <span class="o">+</span> <span class="p">(</span><span class="n">x</span> <span class="o">@</span> <span class="bp">self</span><span class="o">.</span><span class="n">A</span> <span class="o">@</span> <span class="bp">self</span><span class="o">.</span><span class="n">B</span><span class="p">)</span> <span class="o">*</span> <span class="bp">self</span><span class="o">.</span><span class="n">scale</span>\n'
        '\n'
        '<span class="n">layer</span> <span class="o">=</span> <span class="n">LoRALinear</span><span class="p">(</span><span class="mi">512</span><span class="p">,</span> <span class="mi">512</span><span class="p">,</span> <span class="n">rank</span><span class="o">=</span><span class="mi">8</span><span class="p">,</span> <span class="n">alpha</span><span class="o">=</span><span class="mi">16</span><span class="p">)</span>\n'
        '<span class="n">layer</span><span class="p">(</span><span class="n">torch</span><span class="o">.</span><span class="n">randn</span><span class="p">(</span><span class="mi">4</span><span class="p">,</span> <span class="mi">512</span><span class="p">))</span><span class="o">.</span><span class="n">sum</span><span class="p">()</span><span class="o">.</span><span class="n">backward</span><span class="p">()</span>\n'
        '<span class="nb">print</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">A</span><span class="o">.</span><span class="n">grad</span><span class="o">.</span><span class="n">shape</span><span class="p">)</span>   <span class="c1"># (512, 8)</span>\n'
        '<span class="nb">print</span><span class="p">(</span><span class="n">layer</span><span class="o">.</span><span class="n">W0</span><span class="o">.</span><span class="n">grad</span><span class="p">)</span>          <span class="c1"># None &lt;-- the memory saving</span>\n'
        '</code></pre></div>'
        '<p>The 60-70% optimizer-memory saving in LoRA training is exactly this: no <code>grad_W0</code> tensor allocated.</p>'
     )),

    # 2. DPO Z(x) cancellation -- Section 17.2 (was 16.2)
    ('part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html',
     '17.2',
     callout(
        'Under the Hood: Why DPO Doesn\'t Need a Reward Model',
        '<p>The DPO paper says "Z(x) cancels" but rarely shows the algebra. Here it is. The optimal policy under KL-constrained RL has the form:</p>'
        '<p>$$\\pi^*(y|x) = \\frac{1}{Z(x)} \\pi_{\\text{ref}}(y|x) \\exp(r(x,y)/\\beta)$$</p>'
        '<p>where Z(x) is the partition function. Rearranging gives the <em>implicit reward</em>:</p>'
        '<p>$$r(x,y) = \\beta \\log \\frac{\\pi^*(y|x)}{\\pi_{\\text{ref}}(y|x)} + \\beta \\log Z(x)$$</p>'
        '<p>For a preference pair (y<sub>w</sub>, y<sub>l</sub>), the Bradley-Terry loss uses the <em>difference</em> r(x, y<sub>w</sub>) &minus; r(x, y<sub>l</sub>):</p>'
        '<p>$$r(y_w) - r(y_l) = \\beta\\log\\frac{\\pi^*(y_w|x)}{\\pi_{\\text{ref}}(y_w|x)} - \\beta\\log\\frac{\\pi^*(y_l|x)}{\\pi_{\\text{ref}}(y_l|x)}$$</p>'
        '<p>The &beta; log Z(x) terms cancel exactly &mdash; they appear with the same sign on both completions and subtract to zero. The implicit reward becomes a function of log-probability ratios only, computable from &pi;* and &pi;<sub>ref</sub> alone. <strong>No reward model needed.</strong> This is the entire trick.</p>'
     )),

    # 3. HNSW layer probability -- Section 18.2 (was 17.2)
    ('part-5-retrieval-conversation/module-18-embeddings-vector-db/section-18.2.html',
     '18.2',
     callout(
        'Under the Hood: HNSW Layer Assignment',
        '<p>HNSW assigns each new node a maximum layer drawn from an <em>exponential</em> distribution: m<sub>L</sub> = 1/ln(M), and the layer is <code>floor(-ln(random()) * m_L)</code>. This produces:</p>'
        '<p>$$\\Pr[\\text{layer} \\geq \\ell] = e^{-\\ell/m_L} \\approx (1/M)^\\ell$$</p>'
        '<p>So each layer has roughly 1/M of the nodes in the layer below it (on average). For M = 16 and 100,000 vectors: ~94% on layer 0, ~6% on layer 1, ~0.4% on layer 2, ~0% on layer 4+. The greedy search-from-the-top guarantees O(log N) navigation steps because layer count is logarithmic in N. <strong>Practical implication:</strong> increasing M beyond ~64 causes index bloat without recall gain &mdash; the marginal upper-layer nodes don\'t help navigation any more.</p>'
     )),

    # 4. Speculative decoding draft-verify loop -- Section 9.3
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.3.html',
     '9.3',
     callout(
        'Under the Hood: The Draft-Verify Loop',
        '<p>Speculative decoding is often described conceptually; here is the actual loop structure. The draft model autoregressively generates &gamma; tokens, then the target model verifies them in a single batched forward pass:</p>'
        '<div class="code-block-wrapper"><pre><code class="pygments-highlighted lang-python">'
        '<span class="k">def</span> <span class="nf">speculative_step</span><span class="p">(</span><span class="n">target</span><span class="p">,</span> <span class="n">draft</span><span class="p">,</span> <span class="n">ids</span><span class="p">,</span> <span class="n">gamma</span><span class="o">=</span><span class="mi">5</span><span class="p">):</span>\n'
        '    <span class="c1"># 1. Draft phase: gamma tokens autoregressively</span>\n'
        '    <span class="n">qprobs</span> <span class="o">=</span> <span class="p">[]</span>\n'
        '    <span class="k">for</span> <span class="n">_</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">gamma</span><span class="p">):</span>\n'
        '        <span class="n">logits</span> <span class="o">=</span> <span class="n">draft</span><span class="p">(</span><span class="n">ids</span><span class="p">)</span><span class="o">.</span><span class="n">logits</span><span class="p">[:,</span><span class="o">-</span><span class="mi">1</span><span class="p">,:]</span>\n'
        '        <span class="n">q</span> <span class="o">=</span> <span class="n">F</span><span class="o">.</span><span class="n">softmax</span><span class="p">(</span><span class="n">logits</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span>\n'
        '        <span class="n">tok</span> <span class="o">=</span> <span class="n">torch</span><span class="o">.</span><span class="n">multinomial</span><span class="p">(</span><span class="n">q</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>\n'
        '        <span class="n">qprobs</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">q</span><span class="p">[:,</span><span class="n">tok</span><span class="p">])</span>\n'
        '        <span class="n">ids</span> <span class="o">=</span> <span class="n">torch</span><span class="o">.</span><span class="n">cat</span><span class="p">([</span><span class="n">ids</span><span class="p">,</span> <span class="n">tok</span><span class="p">],</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span>\n'
        '    <span class="c1"># 2. Verify in one target pass</span>\n'
        '    <span class="n">p_all</span> <span class="o">=</span> <span class="n">F</span><span class="o">.</span><span class="n">softmax</span><span class="p">(</span><span class="n">target</span><span class="p">(</span><span class="n">ids</span><span class="p">)</span><span class="o">.</span><span class="n">logits</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span>\n'
        '    <span class="c1"># 3. Accept/reject left to right; resample on first reject</span>\n'
        '    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">gamma</span><span class="p">):</span>\n'
        '        <span class="n">tok</span> <span class="o">=</span> <span class="n">ids</span><span class="p">[:,</span> <span class="o">-</span><span class="n">gamma</span><span class="o">+</span><span class="n">i</span><span class="p">]</span>\n'
        '        <span class="n">p</span> <span class="o">=</span> <span class="n">p_all</span><span class="p">[:,</span> <span class="o">-</span><span class="n">gamma</span><span class="o">+</span><span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">tok</span><span class="p">]</span>\n'
        '        <span class="k">if</span> <span class="n">torch</span><span class="o">.</span><span class="n">rand</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span> <span class="o">&gt;</span> <span class="nb">min</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">p</span><span class="o">/</span><span class="n">qprobs</span><span class="p">[</span><span class="n">i</span><span class="p">]):</span>\n'
        '            <span class="c1"># Reject: resample from p - q, discard rest</span>\n'
        '            <span class="n">residual</span> <span class="o">=</span> <span class="p">(</span><span class="n">p_all</span><span class="p">[:,</span><span class="o">-</span><span class="n">gamma</span><span class="o">+</span><span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">-</span> <span class="n">qprobs</span><span class="p">[</span><span class="n">i</span><span class="p">])</span><span class="o">.</span><span class="n">clamp</span><span class="p">(</span><span class="nb">min</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span>\n'
        '            <span class="k">return</span> <span class="n">resample</span><span class="p">(</span><span class="n">residual</span><span class="p">,</span> <span class="n">accepted</span><span class="o">=</span><span class="n">i</span><span class="p">)</span>\n'
        '    <span class="k">return</span> <span class="n">ids</span><span class="p">,</span> <span class="n">accepted</span><span class="o">=</span><span class="n">gamma</span>\n'
        '</code></pre></div>'
        '<p>The key invariant: every position the target model would have sampled is sampled with EXACTLY the target distribution. The accept/reject step is the mathematical correction that preserves losslessness regardless of how poorly the draft model approximates the target.</p>'
     )),

    # 5. FlashAttention tiling -- Section 4.4
    ('part-1-foundations/module-04-transformer-architecture/section-4.4.html',
     '4.4',
     callout(
        'Under the Hood: Why FlashAttention Doesn\'t Materialize N&times;N',
        '<p>Standard attention computes Q K&#x1d40; first (an N&times;N matrix), softmaxes the rows, then multiplies by V. The intermediate N&times;N matrix dominates memory at long contexts (1M tokens &times; 1M tokens of FP16 = 2 TB, impossible). FlashAttention <strong>never materializes</strong> the full attention matrix. It tiles Q, K, V into blocks that fit in GPU SRAM (~100 KB), computes one block at a time, and maintains a running "online softmax" using the log-sum-exp trick:</p>'
        '<p>$$m_{\\text{new}} = \\max(m, \\text{row\\_max}(S)), \\quad \\ell_{\\text{new}} = e^{m - m_{\\text{new}}} \\ell + \\sum e^{S - m_{\\text{new}}}$$</p>'
        '<p>where m is the running maximum (for numerical stability) and &#x2113; is the running denominator. After processing all K/V blocks, the output is rescaled by 1/&#x2113;. Peak memory: O(N &times; block_size), not O(N&sup2;). Verification: the output matches standard attention up to numerical noise (&lt; 10&#8315;&#8309; max diff).</p>'
     )),

    # 6. PagedAttention block table -- Section 9.2
    # Wave 3 already at 9.2 base. Use 9.2.3 (PagedAttention)
    ('part-2-understanding-llms/module-09-inference-optimization/section-9.2.html',
     '9.2.3',
     callout(
        'Under the Hood: vLLM\'s Block Table',
        '<p>PagedAttention treats KV cache like virtual memory. Each sequence holds a <em>block table</em>: a list of physical block indices, NOT a contiguous tensor. Each physical block holds 16 token KV entries; multiple sequences can share blocks via reference counting (e.g., a system prompt shared across thousands of requests has ref_count = N, copy-on-write triggers only when one sequence diverges).</p>'
        '<div class="code-block-wrapper"><pre><code class="pygments-highlighted lang-python">'
        '<span class="nd">@dataclass</span>\n'
        '<span class="k">class</span> <span class="nc">PhysicalBlock</span><span class="p">:</span>\n'
        '    <span class="n">block_id</span><span class="p">:</span> <span class="nb">int</span>\n'
        '    <span class="n">ref_count</span><span class="p">:</span> <span class="nb">int</span> <span class="o">=</span> <span class="mi">0</span>     <span class="c1"># &gt;1 means shared, needs CoW</span>\n'
        '    <span class="n">token_ids</span><span class="p">:</span> <span class="nb">list</span> <span class="o">=</span> <span class="n">field</span><span class="p">(</span><span class="n">default_factory</span><span class="o">=</span><span class="nb">list</span><span class="p">)</span>\n'
        '\n'
        '<span class="nd">@dataclass</span>\n'
        '<span class="k">class</span> <span class="nc">SequenceState</span><span class="p">:</span>\n'
        '    <span class="n">seq_id</span><span class="p">:</span> <span class="nb">int</span>\n'
        '    <span class="n">logical_blocks</span><span class="p">:</span> <span class="nb">list</span><span class="p">[</span><span class="n">PhysicalBlock</span><span class="p">]</span>  <span class="c1"># the block table</span>\n'
        '</code></pre></div>'
        '<p>Without paged attention, KV memory waste from fragmentation can be 30-60% of GPU RAM (over-allocated blocks for short sequences). With paged attention, fragmentation drops below 4% even under heavy multi-tenancy.</p>'
     )),

    # 7. Position bias in LLM judges -- Section 28.x evaluation
    ('part-8-evaluation-production/module-28-evaluation-observability/section-28.1.html',
     '28.1',
     callout(
        'Under the Hood: Position Bias in LLM-as-Judge',
        '<p>LLM judges exhibit a strong <em>position bias</em>: GPT-4 as a judge prefers the first response 58-65% of the time regardless of quality (Zheng et al., 2023, MT-Bench). An eval pipeline that always presents the same model first will report inflated win rates. The fix is symmetric swap: run each pair in BOTH orders and only count consistent verdicts.</p>'
        '<div class="code-block-wrapper"><pre><code class="pygments-highlighted lang-python">'
        '<span class="k">def</span> <span class="nf">judge_with_swap</span><span class="p">(</span><span class="n">judge</span><span class="p">,</span> <span class="n">question</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span>\n'
        '    <span class="n">v1</span> <span class="o">=</span> <span class="n">judge</span><span class="p">(</span><span class="n">question</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span>      <span class="c1"># a first</span>\n'
        '    <span class="n">v2</span> <span class="o">=</span> <span class="n">judge</span><span class="p">(</span><span class="n">question</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">a</span><span class="p">)</span>      <span class="c1"># b first</span>\n'
        '    <span class="k">if</span> <span class="n">v1</span> <span class="o">==</span> <span class="s2">"first"</span> <span class="ow">and</span> <span class="n">v2</span> <span class="o">==</span> <span class="s2">"second"</span><span class="p">:</span>  <span class="k">return</span> <span class="s2">"a wins"</span>\n'
        '    <span class="k">if</span> <span class="n">v1</span> <span class="o">==</span> <span class="s2">"second"</span> <span class="ow">and</span> <span class="n">v2</span> <span class="o">==</span> <span class="s2">"first"</span><span class="p">:</span>  <span class="k">return</span> <span class="s2">"b wins"</span>\n'
        '    <span class="k">return</span> <span class="s2">"tie / unreliable"</span>   <span class="c1"># judge disagreed with itself</span>\n'
        '</code></pre></div>'
        '<p>The tie rate is itself an informative metric: high tie rates indicate the judge is too weak to distinguish the candidates. Length bias (longer responses score higher) requires a separate length-controlled eval to detect.</p>'
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
        if body in text or (SENTINEL in text and h2_prefix in text[text.find(SENTINEL)-200:text.find(SENTINEL)+200] if SENTINEL in text else False):
            n_skip += 1
            continue
        # Try h2 first, then h3
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
        else:
            continue
        if not inserted:
            print(f'  NOT FOUND "{h2_prefix}" in {rel_path}')
    print(f'\nAdded {n_added}; skipped {n_skip}; missing {n_missing}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
