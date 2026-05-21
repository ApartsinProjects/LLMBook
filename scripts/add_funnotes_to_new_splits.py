"""Add fun-notes to the 8 new split sections to clear P3 advisories.

Each fun-note follows the canonical book pattern: <div class="callout fun-note">
with title "Fun Fact" / "Did You Know" / "Mental Model" / "Trivia". Witty,
technically accurate, ~2-4 sentences each.

Inserts the fun-note right after the Big Picture callout in each section.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FUN_NOTES = {
    'part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.2.html': """<div class="callout fun-note">
<div class="callout-title">Fun Fact: The "deploy near hydro" trick</div>
<p>Google's GCP <code>europe-north1</code> region (Hamina, Finland) draws over 95 percent of its annual energy from hydroelectric power, with the rest from wind. Routing inference there instead of <code>us-central1</code> (Iowa, ~40 percent coal) can cut your per-token grid carbon by an order of magnitude with one config change and zero accuracy loss. The hard part is that data-sovereignty rules often force you back to the high-carbon region the moment your users are in the US, which is why "deploy near hydro" is half a trick and half a luxury.</p>
</div>""",
    'part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.3.html': """<div class="callout fun-note">
<div class="callout-title">Did You Know: The first EU AI Act fine will be a paperwork fine</div>
<p>The Article 53 GPAI obligations that take effect in 2025-2027 are almost entirely <em>disclosure</em> rules: keep a technical file, publish a copyright-policy summary, report energy use. The first enforcement actions will not be over a model behaving badly; they will be over a vendor failing to publish the right document by the right date. Compliance teams who treat the Act like a safety regulation will be surprised; those who treat it like SOX-for-models will be ready.</p>
</div>""",
    'part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.2.html': """<div class="callout fun-note">
<div class="callout-title">Mental Model: llama.cpp is the "ffmpeg of LLMs"</div>
<p>llama.cpp is to LLM inference what ffmpeg is to video: a single C/C++ binary that handles a sprawling matrix of input formats, hardware backends, and output configurations, written by a small set of contributors who do not care about your build system. Every other edge runtime (Ollama, LM Studio, LocalAI, Jan, Llamafile) is a wrapper around llama.cpp with a friendlier UX layer on top. When in doubt about whether a quantization works on a device, the llama.cpp issue tracker is the canonical answer.</p>
</div>""",
    'part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.3.html': """<div class="callout fun-note">
<div class="callout-title">Fun Fact: Your phone NPU is faster at INT4 than your laptop GPU at FP16</div>
<p>The 2025-era Snapdragon 8 Elite Hexagon NPU pushes about 45 TOPS at INT4, which beats a discrete RTX 3060 (~12 TFLOPS FP16) on quantized 7B-class inference for short prompts. The catch: only if the model fits in 8 GB unified memory, only if you tolerate a smaller context window, and only if you accept the thermal throttling that kicks in after ~30 seconds of sustained generation. Edge AI is faster than you think and shorter-lived than you hope.</p>
</div>""",
    'part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.2.html': """<div class="callout fun-note">
<div class="callout-title">Trivia: OpenRouter started as a Discord bot</div>
<p>OpenRouter (founded 2023) began as a side project to let a single Discord community switch between GPT-4 and Claude without juggling API keys. By 2025 it routes over a billion tokens per day across 100+ models and bills it on a single invoice. The "unified billing across vendors" feature that LiteLLM Proxy now implements as a first-class concept started as a workaround for a server admin who got tired of expense reports.</p>
</div>""",
    'part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.3.html': """<div class="callout fun-note">
<div class="callout-title">Mental Model: A semantic cache is a poor man's distillation</div>
<p>Semantic caching with a 0.95 similarity threshold turns your most-frequent live prompts into a free, zero-training distillation of the production model into a cheap lookup. Every cache hit is a question that the big model has already answered, at marginal cost zero. The catch: cached answers go stale with the corpus, and "the model would have answered differently today" is a hard failure to detect without periodic invalidation, which is why the canonical pattern is "TTL of one week, force-invalidate on model upgrade".</p>
</div>""",
    'part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.4.html': """<div class="callout fun-note">
<div class="callout-title">Fun Fact: Temporal's founders previously wrote Cadence at Uber</div>
<p>Temporal (Maxim Fateev, Samar Abbas) was founded in 2019 by the same engineers who built Cadence at Uber to coordinate the trip-pricing workflows that move billions of dollars a year. Cadence is still open-source and still runs at Uber; Temporal is the commercial fork with a slicker SDK and managed-service offering. If you ever wonder why durable execution feels like industrial-strength infrastructure rather than a startup demo, it is because the design predates the LLM agent use case by half a decade and was forged on workloads that could not lose a single dollar.</p>
</div>""",
}


def main():
    for relpath, fun_note in FUN_NOTES.items():
        f = ROOT / relpath
        if not f.exists():
            print(f"  SKIP (missing): {relpath}")
            continue
        text = f.read_text(encoding='utf-8')
        if 'class="callout fun-note"' in text:
            print(f"  SKIP (already has fun-note): {relpath}")
            continue
        # Insert after the Big Picture callout closing </div>. Use the
        # FIRST big-picture occurrence (there might be nested ones).
        marker = '<div class="callout big-picture">'
        i = text.find(marker)
        if i == -1:
            print(f"  SKIP (no big-picture): {relpath}")
            continue
        # Find the matching close </div>. Naive: count div opens/closes
        # starting from the marker.
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
                    # Insert after this </div>
                    insert_at = close_idx + len('</div>')
                    text = text[:insert_at] + '\n' + fun_note + '\n' + text[insert_at:]
                    f.write_text(text, encoding='utf-8')
                    print(f"  OK: {relpath}")
                    break
                j = close_idx + 6


if __name__ == '__main__':
    main()
