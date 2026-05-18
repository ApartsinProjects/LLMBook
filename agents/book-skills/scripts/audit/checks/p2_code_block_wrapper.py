"""Detect <pre><code class="pygments-highlighted lang-X"> blocks that are NOT
wrapped in <div class="code-block-wrapper">.

The canonical book code structure is:
  <div class="code-block-wrapper">
    <pre><code class="pygments-highlighted lang-X">...</code></pre>
    <div class="code-output">...</div>      # optional
    <div class="code-caption"><strong>Code Fragment N</strong>: ...</div>
  </div>

Bare <pre><code> outside this wrapper renders without the canonical
margins, copy-button, and caption alignment. Authors should wrap.

Exemptions:
  - <pre><code class="pygments-highlighted lang-text"> inside
    <div class="callout algorithm"> (pseudocode is intentionally bare)
  - <pre><code> inside <details class="output-collapse"> (already
    handled by the code-output collapse wave)
  - <pre> with no <code> child (typically a math/preformatted block)
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CODE_BLOCK_WRAPPER"
DESCRIPTION = "<pre><code> block not wrapped in <div class=\"code-block-wrapper\">"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

PRECODE_RE = re.compile(
    r'<pre\b[^>]*>\s*<code\b[^>]*class="[^"]*pygments-highlighted[^"]*"[^>]*>',
    re.IGNORECASE,
)


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    if not filepath.name.startswith("section-") and filepath.name != "index.html":
        return issues
    for m in PRECODE_RE.finditer(html):
        # Look back ~500 chars for the immediate enclosing wrapper
        before = html[max(0, m.start() - 500):m.start()]
        # Wrapped: ok
        if 'code-block-wrapper' in before[-300:]:
            continue
        # Inside algorithm callout: ok (pseudocode intentionally bare)
        if 'callout algorithm' in before[-500:]:
            # Confirm no intervening </div> after the algorithm callout
            algo_open = before.rfind('class="callout algorithm"')
            close_after_algo = before.find('</div>', algo_open) if algo_open >= 0 else -1
            # If a </div> appears after the algorithm open but before us, we left the algorithm
            if close_after_algo < 0 or close_after_algo > len(before) - 100:
                continue
        # Inside a collapsible details: ok
        if '<details' in before[-400:] and '</details>' not in before[before.rfind('<details'):]:
            continue
        # Inside a callout (any kind) without code-block-wrapper: still flag
        line = html.count("\n", 0, m.start()) + 1
        # Extract a short context label
        lang_m = re.search(r'\blang-(\w+)\b', m.group(0))
        lang = lang_m.group(1) if lang_m else "?"
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'<pre><code class="pygments-highlighted lang-{lang}"> at line '
            f'{line} is not wrapped in <div class="code-block-wrapper">; '
            f'add the canonical wrapper to get correct margins, caption '
            f'alignment, and copy-button placement.'
        ))
    return issues
