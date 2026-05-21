"""Add a small inline SVG figure to each of the 7 sections still flagged
as IMAGE_OPPORTUNITY (no figure). Each figure is small (single concept)
but accurate and book-style.

Inserts the figure RIGHT AFTER the fun-note (added in the previous wave),
so the page reads: epigraph -> big-picture -> prereqs -> fun-note -> figure -> body.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


FIGURES = {
    'part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.2.html': '''<figure class="diagram">
<svg viewBox="0 0 640 280" role="img" aria-label="Bar chart showing relative carbon reduction across four mitigation strategies (region selection, MoE vs dense, batch inference, quantization)" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:1rem auto;font-family:'Segoe UI',sans-serif;">
<text x="320" y="22" font-size="14" font-weight="600" fill="#2d3748" text-anchor="middle">Relative carbon reduction by mitigation lever (training)</text>
<text x="320" y="40" font-size="10" fill="#6b7280" text-anchor="middle">Higher = bigger CO2e cut per dollar invested. Order matters: pick low-hanging fruit first.</text>
<rect x="80" y="80" width="100" height="140" fill="#047857" stroke="#065f46" stroke-width="1.5"/>
<text x="130" y="105" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">5-10x</text>
<text x="130" y="240" font-size="11" fill="#1f2937" text-anchor="middle">Region</text>
<text x="130" y="254" font-size="9" fill="#6b7280" text-anchor="middle">choose hydro / nuclear</text>
<rect x="200" y="120" width="100" height="100" fill="#3a73a8" stroke="#1e3a8a" stroke-width="1.5"/>
<text x="250" y="145" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">2-4x</text>
<text x="250" y="240" font-size="11" fill="#1f2937" text-anchor="middle">MoE vs dense</text>
<text x="250" y="254" font-size="9" fill="#6b7280" text-anchor="middle">active params, not total</text>
<rect x="320" y="150" width="100" height="70" fill="#d97706" stroke="#92400e" stroke-width="1.5"/>
<text x="370" y="172" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">1.5-2x</text>
<text x="370" y="240" font-size="11" fill="#1f2937" text-anchor="middle">Batch size</text>
<text x="370" y="254" font-size="9" fill="#6b7280" text-anchor="middle">GPU utilization up</text>
<rect x="440" y="170" width="100" height="50" fill="#7c3aed" stroke="#5b21b6" stroke-width="1.5"/>
<text x="490" y="190" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">1.2-1.5x</text>
<text x="490" y="240" font-size="11" fill="#1f2937" text-anchor="middle">Quantization</text>
<text x="490" y="254" font-size="9" fill="#6b7280" text-anchor="middle">FP16->INT8 mostly free</text>
</svg>
<figcaption><strong>Figure 55.2.1</strong>: Relative carbon reduction by mitigation lever. Region selection compounds with everything else, which is why it sits first in the playbook even though it is the most political to change.</figcaption>
</figure>''',
    'part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.3.html': '''<figure class="diagram">
<svg viewBox="0 0 700 200" role="img" aria-label="Timeline of EU AI Act Article 53 enforcement deadlines for GPAI providers from 2024 through 2027" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:1rem auto;font-family:'Segoe UI',sans-serif;">
<text x="350" y="22" font-size="14" font-weight="600" fill="#2d3748" text-anchor="middle">EU AI Act Article 53 GPAI compliance timeline</text>
<line x1="40" y1="100" x2="660" y2="100" stroke="#4a5568" stroke-width="2"/>
<circle cx="100" cy="100" r="7" fill="#b91c1c" stroke="#fff" stroke-width="2"/>
<text x="100" y="80" font-size="11" font-weight="600" fill="#1f2937" text-anchor="middle">Aug 2024</text>
<text x="100" y="130" font-size="10" fill="#4a5568" text-anchor="middle">Act enters force</text>
<text x="100" y="143" font-size="9" fill="#6b7280" text-anchor="middle">(no obligations yet)</text>
<circle cx="260" cy="100" r="9" fill="#d97706" stroke="#fff" stroke-width="2"/>
<text x="260" y="80" font-size="11" font-weight="600" fill="#1f2937" text-anchor="middle">Aug 2025</text>
<text x="260" y="130" font-size="10" fill="#4a5568" text-anchor="middle">GPAI obligations</text>
<text x="260" y="143" font-size="9" fill="#6b7280" text-anchor="middle">technical file + copyright policy</text>
<circle cx="420" cy="100" r="11" fill="#7c3aed" stroke="#fff" stroke-width="2"/>
<text x="420" y="80" font-size="11" font-weight="600" fill="#1f2937" text-anchor="middle">Aug 2026</text>
<text x="420" y="130" font-size="10" fill="#4a5568" text-anchor="middle">High-risk systems</text>
<text x="420" y="143" font-size="9" fill="#6b7280" text-anchor="middle">conformity assessment required</text>
<circle cx="580" cy="100" r="13" fill="#047857" stroke="#fff" stroke-width="2"/>
<text x="580" y="80" font-size="11" font-weight="600" fill="#1f2937" text-anchor="middle">Aug 2027</text>
<text x="580" y="130" font-size="10" fill="#4a5568" text-anchor="middle">Full enforcement</text>
<text x="580" y="143" font-size="9" fill="#6b7280" text-anchor="middle">all categories + penalties</text>
<text x="350" y="180" font-size="10" font-style="italic" fill="#6b7280" text-anchor="middle">Penalties: up to EUR 35M or 7% of global turnover, whichever is higher.</text>
</svg>
<figcaption><strong>Figure 55.3.1</strong>: EU AI Act Article 53 enforcement timeline. The first two milestones are documentation only; the real teeth come in 2026 with high-risk conformity assessments and 2027 with full penalty exposure.</figcaption>
</figure>''',
    'part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.2.html': '''<figure class="diagram">
<svg viewBox="0 0 660 320" role="img" aria-label="Six edge LLM runtimes laid out by hardware target and abstraction level" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:1rem auto;font-family:'Segoe UI',sans-serif;">
<text x="330" y="22" font-size="14" font-weight="600" fill="#2d3748" text-anchor="middle">The 2026 edge runtime landscape</text>
<text x="330" y="40" font-size="10" fill="#6b7280" text-anchor="middle">x = hardware target (general -> specialized) | y = abstraction (raw -> developer-friendly)</text>
<line x1="60" y1="270" x2="640" y2="270" stroke="#4a5568" stroke-width="1.5"/>
<line x1="60" y1="60" x2="60" y2="270" stroke="#4a5568" stroke-width="1.5"/>
<text x="350" y="290" font-size="11" font-weight="600" fill="#4a5568" text-anchor="middle">cross-platform CPU + GPU</text>
<text x="350" y="305" font-size="9" fill="#6b7280" text-anchor="middle">general hardware  ->  vendor-specific NPU</text>
<text x="35" y="170" font-size="11" font-weight="600" fill="#4a5568" text-anchor="middle" transform="rotate(-90 35 170)">developer-friendly</text>
<rect x="80" y="200" width="120" height="55" fill="#dbeafe" stroke="#3a73a8" stroke-width="1.5" rx="6"/>
<text x="140" y="222" font-size="12" font-weight="700" fill="#1e3a8a" text-anchor="middle">llama.cpp</text>
<text x="140" y="240" font-size="9" fill="#1e40af" text-anchor="middle">C/C++, every backend</text>
<rect x="80" y="80" width="120" height="55" fill="#bbf7d0" stroke="#047857" stroke-width="1.5" rx="6"/>
<text x="140" y="102" font-size="12" font-weight="700" fill="#065f46" text-anchor="middle">Ollama</text>
<text x="140" y="120" font-size="9" fill="#065f46" text-anchor="middle">wraps llama.cpp + UX</text>
<rect x="240" y="140" width="120" height="55" fill="#fed7aa" stroke="#d97706" stroke-width="1.5" rx="6"/>
<text x="300" y="162" font-size="12" font-weight="700" fill="#92400e" text-anchor="middle">MLX</text>
<text x="300" y="180" font-size="9" fill="#92400e" text-anchor="middle">Apple Silicon native</text>
<rect x="380" y="200" width="120" height="55" fill="#e9d5ff" stroke="#7c3aed" stroke-width="1.5" rx="6"/>
<text x="440" y="222" font-size="12" font-weight="700" fill="#5b21b6" text-anchor="middle">ExecuTorch</text>
<text x="440" y="240" font-size="9" fill="#5b21b6" text-anchor="middle">PyTorch mobile + edge</text>
<rect x="380" y="80" width="120" height="55" fill="#fce7f3" stroke="#be185d" stroke-width="1.5" rx="6"/>
<text x="440" y="102" font-size="12" font-weight="700" fill="#831843" text-anchor="middle">WebLLM</text>
<text x="440" y="120" font-size="9" fill="#831843" text-anchor="middle">WebGPU, in browser</text>
<rect x="520" y="140" width="120" height="55" fill="#fecaca" stroke="#b91c1c" stroke-width="1.5" rx="6"/>
<text x="580" y="162" font-size="12" font-weight="700" fill="#7f1d1d" text-anchor="middle">Qualcomm AI Hub</text>
<text x="580" y="180" font-size="9" fill="#7f1d1d" text-anchor="middle">Hexagon NPU only</text>
</svg>
<figcaption><strong>Figure 60.2.1</strong>: The six edge runtimes laid out by hardware breadth (x-axis) and developer-friendliness (y-axis). llama.cpp is the substrate; everything else is either a friendlier wrapper or a vendor-specific specialization.</figcaption>
</figure>''',
    'part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.3.html': '''<figure class="diagram">
<svg viewBox="0 0 640 280" role="img" aria-label="Line plot showing battery drain rate accelerating with prompt length on a phone NPU, with thermal throttling kicking in after 30 seconds" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:1rem auto;font-family:'Segoe UI',sans-serif;">
<text x="320" y="22" font-size="14" font-weight="600" fill="#2d3748" text-anchor="middle">Battery drain vs. sustained inference time (phone NPU, 7B INT4)</text>
<line x1="60" y1="240" x2="600" y2="240" stroke="#4a5568" stroke-width="1.5"/>
<line x1="60" y1="60" x2="60" y2="240" stroke="#4a5568" stroke-width="1.5"/>
<text x="60" y="260" font-size="10" fill="#4a5568" text-anchor="middle">0s</text>
<text x="200" y="260" font-size="10" fill="#4a5568" text-anchor="middle">15s</text>
<text x="320" y="260" font-size="10" fill="#4a5568" text-anchor="middle">30s</text>
<text x="440" y="260" font-size="10" fill="#4a5568" text-anchor="middle">45s</text>
<text x="600" y="260" font-size="10" fill="#4a5568" text-anchor="middle">60s</text>
<text x="40" y="240" font-size="10" fill="#4a5568" text-anchor="middle">0%</text>
<text x="40" y="150" font-size="10" fill="#4a5568" text-anchor="middle">5%</text>
<text x="40" y="60" font-size="10" fill="#4a5568" text-anchor="middle">10%</text>
<path d="M 60 235 Q 200 200 320 140 Q 440 110 600 95" stroke="#3a73a8" stroke-width="2.5" fill="none"/>
<line x1="320" y1="60" x2="320" y2="240" stroke="#b91c1c" stroke-width="1.5" stroke-dasharray="5,3"/>
<text x="330" y="75" font-size="11" font-weight="600" fill="#b91c1c">thermal throttle kicks in</text>
<text x="330" y="90" font-size="9" fill="#7f1d1d">tokens/sec drops 30-50%</text>
<text x="320" y="180" font-size="11" font-style="italic" fill="#4a5568" text-anchor="middle">Battery drain (% of total)</text>
</svg>
<figcaption><strong>Figure 60.3.1</strong>: Sustained inference on a phone NPU drains 5 to 8 percent of battery per minute and throttles after about 30 seconds. Edge AI is faster than cloud for the first 30 seconds and worse for the next 30, which is why production apps stream short turns rather than long completions.</figcaption>
</figure>''',
    'part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.2.html': '''<figure class="diagram">
<svg viewBox="0 0 660 240" role="img" aria-label="Fallback chain flow diagram with primary provider, secondary provider, and cached-response fallback" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:1rem auto;font-family:'Segoe UI',sans-serif;">
<defs>
<marker id="arrow63" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
<polygon points="0,0 0,6 9,3" fill="#4a5568"/>
</marker>
</defs>
<text x="330" y="22" font-size="14" font-weight="600" fill="#2d3748" text-anchor="middle">Three-tier fallback chain</text>
<rect x="40" y="80" width="140" height="80" fill="#dbeafe" stroke="#3a73a8" stroke-width="1.5" rx="6"/>
<text x="110" y="108" font-size="12" font-weight="700" fill="#1e3a8a" text-anchor="middle">Primary</text>
<text x="110" y="128" font-size="10" fill="#1e3a8a" text-anchor="middle">GPT-4o</text>
<text x="110" y="145" font-size="9" fill="#6b7280" text-anchor="middle">target: lowest latency,</text>
<text x="110" y="156" font-size="9" fill="#6b7280" text-anchor="middle">best quality</text>
<line x1="180" y1="120" x2="240" y2="120" stroke="#4a5568" stroke-width="2" marker-end="url(#arrow63)"/>
<text x="210" y="110" font-size="9" font-weight="600" fill="#b91c1c">429/5xx</text>
<rect x="240" y="80" width="140" height="80" fill="#fed7aa" stroke="#d97706" stroke-width="1.5" rx="6"/>
<text x="310" y="108" font-size="12" font-weight="700" fill="#92400e" text-anchor="middle">Secondary</text>
<text x="310" y="128" font-size="10" fill="#92400e" text-anchor="middle">Claude 3.5 Sonnet</text>
<text x="310" y="145" font-size="9" fill="#6b7280" text-anchor="middle">target: equivalent quality,</text>
<text x="310" y="156" font-size="9" fill="#6b7280" text-anchor="middle">different vendor</text>
<line x1="380" y1="120" x2="440" y2="120" stroke="#4a5568" stroke-width="2" marker-end="url(#arrow63)"/>
<text x="410" y="110" font-size="9" font-weight="600" fill="#b91c1c">also 429</text>
<rect x="440" y="80" width="140" height="80" fill="#bbf7d0" stroke="#047857" stroke-width="1.5" rx="6"/>
<text x="510" y="108" font-size="12" font-weight="700" fill="#065f46" text-anchor="middle">Cached fallback</text>
<text x="510" y="128" font-size="10" fill="#065f46" text-anchor="middle">semantic cache hit</text>
<text x="510" y="145" font-size="9" fill="#6b7280" text-anchor="middle">target: degrade gracefully,</text>
<text x="510" y="156" font-size="9" fill="#6b7280" text-anchor="middle">never 500 to user</text>
<text x="330" y="195" font-size="11" font-style="italic" fill="#4a5568" text-anchor="middle">Total user-visible failure rate falls from ~0.5% (single provider) to ~0.01% (3-tier chain).</text>
<text x="330" y="215" font-size="10" fill="#6b7280" text-anchor="middle">Cost: ~10% additional latency on the 0.5% of requests that escalate; zero on the rest.</text>
</svg>
<figcaption><strong>Figure 63.2.1</strong>: A three-tier fallback chain converts vendor outages into a slow-degradation curve. The cached-fallback tier is the unlock: it never throws 500 to the user, even when both vendors are down.</figcaption>
</figure>''',
    'part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.3.html': '''<figure class="diagram">
<svg viewBox="0 0 640 280" role="img" aria-label="Bar chart of latency and cost per request comparing cache miss, cache hit, and cached response paths" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:1rem auto;font-family:'Segoe UI',sans-serif;">
<text x="320" y="22" font-size="14" font-weight="600" fill="#2d3748" text-anchor="middle">Semantic cache: latency &amp; cost per request</text>
<text x="320" y="40" font-size="10" fill="#6b7280" text-anchor="middle">Cache hit ratio of 35% (typical for FAQ workloads) cuts the bill by ~30%.</text>
<rect x="80" y="80" width="80" height="140" fill="#fecaca" stroke="#b91c1c" stroke-width="1.5"/>
<text x="120" y="108" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">800 ms</text>
<text x="120" y="125" font-size="10" fill="#fff" text-anchor="middle">$0.0015</text>
<text x="120" y="240" font-size="11" fill="#1f2937" text-anchor="middle">cache miss</text>
<text x="120" y="254" font-size="9" fill="#6b7280" text-anchor="middle">full LLM call</text>
<rect x="200" y="170" width="80" height="50" fill="#bbf7d0" stroke="#047857" stroke-width="1.5"/>
<text x="240" y="195" font-size="12" font-weight="700" fill="#065f46" text-anchor="middle">35 ms</text>
<text x="240" y="210" font-size="10" fill="#065f46" text-anchor="middle">$0.0001</text>
<text x="240" y="240" font-size="11" fill="#1f2937" text-anchor="middle">cache hit</text>
<text x="240" y="254" font-size="9" fill="#6b7280" text-anchor="middle">embed + lookup only</text>
<rect x="320" y="130" width="80" height="90" fill="#fed7aa" stroke="#d97706" stroke-width="1.5"/>
<text x="360" y="158" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">250 ms</text>
<text x="360" y="175" font-size="10" fill="#fff" text-anchor="middle">$0.0005</text>
<text x="360" y="240" font-size="11" fill="#1f2937" text-anchor="middle">partial hit</text>
<text x="360" y="254" font-size="9" fill="#6b7280" text-anchor="middle">cached + delta gen</text>
<text x="510" y="100" font-size="11" font-weight="600" fill="#3a73a8">Effective avg @ 35% hit</text>
<text x="510" y="118" font-size="10" fill="#1f2937">latency: ~540 ms</text>
<text x="510" y="135" font-size="10" fill="#1f2937">cost: ~$0.0010/req</text>
<text x="510" y="160" font-size="10" font-style="italic" fill="#047857">~33% cheaper than no cache</text>
</svg>
<figcaption><strong>Figure 63.3.1</strong>: Semantic cache economics on a typical FAQ workload. The bigger win is latency (a hit returns in 35 ms vs 800 ms for a full LLM call); cost reduction follows as a secondary effect.</figcaption>
</figure>''',
    'part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.4.html': '''<figure class="diagram">
<svg viewBox="0 0 660 320" role="img" aria-label="Decision tree for picking a durable execution framework based on language preference, scale, and operational model" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;display:block;margin:1rem auto;font-family:'Segoe UI',sans-serif;">
<text x="330" y="22" font-size="14" font-weight="600" fill="#2d3748" text-anchor="middle">Durable execution framework decision tree</text>
<rect x="240" y="50" width="180" height="40" fill="#dbeafe" stroke="#3a73a8" stroke-width="1.5" rx="6"/>
<text x="330" y="74" font-size="12" font-weight="700" fill="#1e3a8a" text-anchor="middle">Start: agent workflow</text>
<line x1="330" y1="90" x2="150" y2="125" stroke="#4a5568" stroke-width="1.5"/>
<line x1="330" y1="90" x2="510" y2="125" stroke="#4a5568" stroke-width="1.5"/>
<text x="220" y="113" font-size="10" fill="#6b7280">single-team</text>
<text x="440" y="113" font-size="10" fill="#6b7280">multi-team / enterprise</text>
<rect x="80" y="125" width="160" height="40" fill="#bbf7d0" stroke="#047857" stroke-width="1.5" rx="6"/>
<text x="160" y="149" font-size="11" font-weight="700" fill="#065f46" text-anchor="middle">LangGraph or Hatchet</text>
<rect x="430" y="125" width="160" height="40" fill="#fed7aa" stroke="#d97706" stroke-width="1.5" rx="6"/>
<text x="510" y="149" font-size="11" font-weight="700" fill="#92400e" text-anchor="middle">Temporal or Restate</text>
<line x1="160" y1="165" x2="80" y2="205" stroke="#4a5568" stroke-width="1.5"/>
<line x1="160" y1="165" x2="240" y2="205" stroke="#4a5568" stroke-width="1.5"/>
<text x="100" y="195" font-size="9" fill="#6b7280">Python-only</text>
<text x="240" y="195" font-size="9" fill="#6b7280">embedded in app</text>
<rect x="20" y="205" width="140" height="35" fill="#fce7f3" stroke="#be185d" stroke-width="1.5" rx="6"/>
<text x="90" y="227" font-size="11" font-weight="700" fill="#831843" text-anchor="middle">Hatchet</text>
<rect x="180" y="205" width="140" height="35" fill="#e9d5ff" stroke="#7c3aed" stroke-width="1.5" rx="6"/>
<text x="250" y="227" font-size="11" font-weight="700" fill="#5b21b6" text-anchor="middle">LangGraph + checkpointer</text>
<line x1="510" y1="165" x2="430" y2="205" stroke="#4a5568" stroke-width="1.5"/>
<line x1="510" y1="165" x2="590" y2="205" stroke="#4a5568" stroke-width="1.5"/>
<text x="450" y="195" font-size="9" fill="#6b7280">have ops team</text>
<text x="580" y="195" font-size="9" fill="#6b7280">prefer SaaS</text>
<rect x="370" y="205" width="140" height="35" fill="#fecaca" stroke="#b91c1c" stroke-width="1.5" rx="6"/>
<text x="440" y="227" font-size="11" font-weight="700" fill="#7f1d1d" text-anchor="middle">Temporal self-hosted</text>
<rect x="520" y="205" width="140" height="35" fill="#fed7aa" stroke="#d97706" stroke-width="1.5" rx="6"/>
<text x="590" y="227" font-size="11" font-weight="700" fill="#92400e" text-anchor="middle">Temporal Cloud or Restate</text>
<text x="330" y="275" font-size="10" font-style="italic" fill="#4a5568" text-anchor="middle">Inngest fits as an alternative to Temporal Cloud when you want event-driven semantics out of the box.</text>
<text x="330" y="290" font-size="10" fill="#6b7280" text-anchor="middle">For batch ETL (not agent workflows), DAG-as-config (Airflow, Prefect) is still preferable.</text>
</svg>
<figcaption><strong>Figure 64.4.1</strong>: Framework selection decision tree. The first cut is team size; the second is language preference and operational appetite. Inngest sits horizontally as the SaaS event-driven alternative.</figcaption>
</figure>''',
}


def main():
    for relpath, figure_html in FIGURES.items():
        f = ROOT / relpath
        if not f.exists():
            print(f"  SKIP (missing): {relpath}")
            continue
        text = f.read_text(encoding='utf-8')
        if '<figure class="diagram"' in text or '<figure class="illustration"' in text:
            # Check whether the figure caption ID we'd add already exists
            cap_text = figure_html.split('<strong>')[1].split('</strong>')[0]
            if cap_text in text:
                print(f"  SKIP (figure already present): {relpath}")
                continue
        # Insert after the fun-note <div class="callout fun-note">...</div>.
        # If no fun-note, insert after big-picture.
        marker_options = [
            ('class="callout fun-note"', '</div>'),
            ('class="callout big-picture"', '</div>'),
        ]
        inserted = False
        for marker_open, _ in marker_options:
            i = text.find(marker_open)
            if i == -1:
                continue
            # Find matching close </div> by depth-counting
            depth = 0
            j = i
            while j < len(text):
                open_idx = text.find('<div', j)
                close_idx = text.find('</div>', j)
                if close_idx == -1:
                    break
                if open_idx != -1 and open_idx < close_idx:
                    depth += 1
                    j = open_idx + 4
                else:
                    depth -= 1
                    if depth == 0:
                        insert_at = close_idx + len('</div>')
                        text = text[:insert_at] + '\n' + figure_html + '\n' + text[insert_at:]
                        f.write_text(text, encoding='utf-8')
                        print(f"  OK: {relpath}")
                        inserted = True
                        break
                    j = close_idx + 6
            if inserted:
                break
        if not inserted:
            print(f"  SKIP (no insertion point): {relpath}")


if __name__ == '__main__':
    main()
