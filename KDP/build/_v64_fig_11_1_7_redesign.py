"""v6.4: Figure 11.1.7 deeper redesign.

PRIOR STATE (v6.0): centered the existing 3-stacked-rectangles SVG so it
sat properly in the viewBox.

THIS REDESIGN: replace the abstract structural diagram with a richer
"anatomy of a prompt" SVG that pairs every structural component with
a concrete fragment of REAL prompt text + the corresponding chat API
JSON. Reader learns the mapping by seeing it demonstrated, not by
labels alone.

Layout (1000x620 viewBox):
  - Three message cards stacked vertically (System / Few-shot / User)
  - Each card shows: role badge + component labels (color-coded) +
    actual example prompt text
  - Right-side mini panel: corresponding messages[] JSON array
  - Bottom: arrow -> Model -> assistant response card

Color system (carries semantic meaning):
  - Purple : System role  (instruction, context, format spec)
  - Blue   : Few-shot examples
  - Green  : User input
  - Orange : Model response (assistant)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SECTION = ROOT / 'part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html'

NEW_SVG = '''<!-- Figure 11.1.7 v6.4 redesign: anatomy of a prompt with concrete example -->
<div class="diagram-container">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 620" role="img"
     aria-labelledby="fig1117-title fig1117-desc"
     style="max-width: 100%; height: auto; font-family: 'Segoe UI', system-ui, sans-serif;">
  <title id="fig1117-title">Anatomy of a prompt mapped to chat API message roles</title>
  <desc id="fig1117-desc">Three vertically stacked message cards (System, Few-shot examples, User) show how the five prompt components (instruction, context, output format, examples, input data) are distributed across the three chat API roles. Each card pairs the abstract component labels with a concrete excerpt of real prompt text. A bottom panel shows the assistant response that the model returns.</desc>

  <defs>
    <marker id="f1117arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#555"/>
    </marker>
    <filter id="f1117shadow" x="-2%" y="-2%" width="104%" height="115%">
      <feDropShadow dx="0" dy="2" flood-opacity="0.08" stdDeviation="2"/>
    </filter>
  </defs>

  <!-- ============== SYSTEM MESSAGE CARD ============== -->
  <g transform="translate(40, 40)">
    <rect width="700" height="135" rx="10" fill="#f5eef8" stroke="#8e44ad" stroke-width="2" filter="url(#f1117shadow)"/>
    <!-- Role badge -->
    <rect x="12" y="12" width="92" height="22" rx="11" fill="#8e44ad"/>
    <text x="58" y="28" fill="#fff" font-size="11" font-weight="700" text-anchor="middle" letter-spacing="0.05em">SYSTEM</text>
    <!-- Component tags (right) -->
    <g font-size="10" font-weight="600">
      <rect x="120" y="12" width="80"  height="22" rx="3" fill="#8e44ad" opacity="0.18"/>
      <text x="160" y="28" fill="#5e2680" text-anchor="middle">instruction</text>
      <rect x="208" y="12" width="68"  height="22" rx="3" fill="#8e44ad" opacity="0.18"/>
      <text x="242" y="28" fill="#5e2680" text-anchor="middle">context</text>
      <rect x="284" y="12" width="105" height="22" rx="3" fill="#8e44ad" opacity="0.18"/>
      <text x="336" y="28" fill="#5e2680" text-anchor="middle">output format</text>
    </g>
    <!-- Example text -->
    <text x="22" y="62" fill="#333" font-size="13" font-style="italic">"You are a senior Python code reviewer. Look for bugs in the snippet below.</text>
    <text x="22" y="82" fill="#333" font-size="13" font-style="italic">Use a calm, instructive tone. The reader is a junior developer.</text>
    <text x="22" y="102" fill="#333" font-size="13" font-style="italic">Output JSON with keys: <tspan font-family="ui-monospace, monospace" fill="#5e2680">bug_type</tspan>,</text>
    <text x="22" y="120" fill="#333" font-size="13" font-style="italic"><tspan font-family="ui-monospace, monospace" fill="#5e2680">severity</tspan> (low / med / high), and <tspan font-family="ui-monospace, monospace" fill="#5e2680">fix</tspan>."</text>
  </g>

  <!-- ============== FEW-SHOT EXAMPLES CARD ============== -->
  <g transform="translate(40, 195)">
    <rect width="700" height="120" rx="10" fill="#eaf4fc" stroke="#3498db" stroke-width="2" stroke-dasharray="4 3" filter="url(#f1117shadow)"/>
    <rect x="12" y="12" width="148" height="22" rx="11" fill="#3498db"/>
    <text x="86" y="28" fill="#fff" font-size="11" font-weight="700" text-anchor="middle" letter-spacing="0.05em">FEW-SHOT (optional)</text>
    <g font-size="10" font-weight="600">
      <rect x="172" y="12" width="80" height="22" rx="3" fill="#3498db" opacity="0.18"/>
      <text x="212" y="28" fill="#1d6fa5" text-anchor="middle">examples</text>
    </g>
    <!-- 1st example -->
    <text x="22" y="62" font-size="11" fill="#666" font-weight="700">User:</text>
    <text x="62" y="62" font-size="12" fill="#333" font-family="ui-monospace, monospace">def add(a, b): return a - b</text>
    <text x="22" y="80" font-size="11" fill="#666" font-weight="700">Assistant:</text>
    <text x="92" y="80" font-size="12" fill="#333" font-family="ui-monospace, monospace">{"bug_type": "logic", "severity": "high", "fix": "return a + b"}</text>
    <!-- ... more examples elided -->
    <text x="22" y="105" font-size="11" fill="#888" font-style="italic">...more (user, assistant) pairs as needed...</text>
  </g>

  <!-- ============== USER MESSAGE CARD ============== -->
  <g transform="translate(40, 335)">
    <rect width="700" height="100" rx="10" fill="#eafaf1" stroke="#27ae60" stroke-width="2" filter="url(#f1117shadow)"/>
    <rect x="12" y="12" width="60" height="22" rx="11" fill="#27ae60"/>
    <text x="42" y="28" fill="#fff" font-size="11" font-weight="700" text-anchor="middle" letter-spacing="0.05em">USER</text>
    <g font-size="10" font-weight="600">
      <rect x="84"  y="12" width="80"  height="22" rx="3" fill="#27ae60" opacity="0.18"/>
      <text x="124" y="28" fill="#0f6b3a" text-anchor="middle">input data</text>
    </g>
    <text x="22" y="62" fill="#333" font-size="13" font-family="ui-monospace, monospace">def divide(a, b):</text>
    <text x="22" y="80" fill="#333" font-size="13" font-family="ui-monospace, monospace">    return a / b   # what about b == 0 ?</text>
  </g>

  <!-- Down-arrow from USER -> MODEL -->
  <line x1="390" y1="445" x2="390" y2="475" stroke="#555" stroke-width="2" marker-end="url(#f1117arrow)"/>

  <!-- Model badge -->
  <g transform="translate(330, 477)">
    <rect width="120" height="36" rx="18" fill="#fff" stroke="#555" stroke-width="2"/>
    <text x="60" y="23" fill="#333" font-size="13" font-weight="700" text-anchor="middle">LLM</text>
  </g>

  <!-- ============== ASSISTANT RESPONSE CARD ============== -->
  <g transform="translate(40, 525)">
    <rect width="700" height="80" rx="10" fill="#fef3e6" stroke="#e67e22" stroke-width="2" filter="url(#f1117shadow)"/>
    <rect x="12" y="12" width="100" height="22" rx="11" fill="#e67e22"/>
    <text x="62" y="28" fill="#fff" font-size="11" font-weight="700" text-anchor="middle" letter-spacing="0.05em">ASSISTANT</text>
    <text x="22" y="58" fill="#333" font-size="13" font-family="ui-monospace, monospace">{"bug_type": "ZeroDivisionError", "severity": "high",</text>
    <text x="22" y="74" fill="#333" font-size="13" font-family="ui-monospace, monospace"> "fix": "raise ValueError if b == 0 before dividing"}</text>
  </g>

  <!-- ============== RIGHT PANEL: chat API JSON ============== -->
  <g transform="translate(770, 40)">
    <rect width="200" height="395" rx="10" fill="#fafafa" stroke="#ccc" stroke-width="1.2"/>
    <text x="100" y="22" fill="#333" font-size="11" font-weight="700" text-anchor="middle">Chat API messages[]</text>
    <line x1="10" y1="30" x2="190" y2="30" stroke="#ddd"/>
    <g font-family="ui-monospace, monospace" font-size="10" fill="#333">
      <text x="10" y="48">[</text>
      <text x="22" y="62">{</text>
      <text x="34" y="76"><tspan fill="#8e44ad">"role"</tspan>: <tspan fill="#0a7d33">"system"</tspan>,</text>
      <text x="34" y="90"><tspan fill="#8e44ad">"content"</tspan>: ...</text>
      <text x="22" y="104">},</text>
      <text x="22" y="120">{</text>
      <text x="34" y="134"><tspan fill="#3498db">"role"</tspan>: <tspan fill="#0a7d33">"user"</tspan>,</text>
      <text x="34" y="148"><tspan fill="#3498db">"content"</tspan>: "def add..."</text>
      <text x="22" y="162">},</text>
      <text x="22" y="178">{</text>
      <text x="34" y="192"><tspan fill="#3498db">"role"</tspan>: <tspan fill="#0a7d33">"assistant"</tspan>,</text>
      <text x="34" y="206"><tspan fill="#3498db">"content"</tspan>: "{...}"</text>
      <text x="22" y="220">},</text>
      <text x="34" y="240" fill="#888" font-style="italic">// more pairs...</text>
      <text x="22" y="260">{</text>
      <text x="34" y="274"><tspan fill="#27ae60">"role"</tspan>: <tspan fill="#0a7d33">"user"</tspan>,</text>
      <text x="34" y="288"><tspan fill="#27ae60">"content"</tspan>: "def divide..."</text>
      <text x="22" y="302">}</text>
      <text x="10" y="316">]</text>
    </g>
    <line x1="10" y1="335" x2="190" y2="335" stroke="#ddd"/>
    <text x="100" y="354" fill="#666" font-size="10" text-anchor="middle">color = card source</text>
    <text x="100" y="372" fill="#666" font-size="10" text-anchor="middle">role string is what</text>
    <text x="100" y="386" fill="#666" font-size="10" text-anchor="middle">the API actually sees</text>
  </g>
</svg>
<div class="diagram-caption"><strong>Figure 11.1.7</strong>: Anatomy of a prompt mapped to chat API roles. The five structural components (instruction, context, output format, examples, input data) are distributed across three message roles. The right panel shows how each card becomes one entry in the <code>messages[]</code> array sent to the model. Color carries the mapping: purple = system, blue = few-shot example pairs, green = the actual user query, orange = the model's response.</div>
</div>'''


def main() -> int:
    text = SECTION.read_text(encoding='utf-8')
    # Match the existing Figure 11.1.7 block (the one we centered in v6.0)
    pat = re.compile(
        r'<!--\s*Figure 11\.1\.7[^>]*-->\s*'
        r'<div class="diagram-container">\s*<svg[^>]+viewBox="0 0 950 340"[^>]*>'
        r'(?:.|\n)*?</svg>\s*<div class="diagram-caption"><strong>Figure 11\.1\.7</strong>:[^<]*</div>\s*</div>',
        re.DOTALL,
    )
    if not pat.search(text):
        # try without the leading comment
        pat = re.compile(
            r'<div class="diagram-container">\s*<svg[^>]+viewBox="0 0 950 340"[^>]*>'
            r'(?:.|\n)*?</svg>\s*<div class="diagram-caption"><strong>Figure 11\.1\.7</strong>:[^<]*</div>\s*</div>',
            re.DOTALL,
        )
    m = pat.search(text)
    if not m:
        print('  ERROR: Figure 11.1.7 block not found')
        return 1
    new_text = text[:m.start()] + NEW_SVG + text[m.end():]
    SECTION.write_text(new_text, encoding='utf-8')
    print(f'  Replaced Figure 11.1.7 ({m.end()-m.start()} chars old, {len(NEW_SVG)} chars new).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
