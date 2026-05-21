"""Detect pages that contain math markup but do not load a math renderer.

If a page has $$...$$ / <div class="math-block"> / <span class="math"> /
$\\command$ math but never includes the KaTeX auto-render script (or MathJax),
the math renders as raw dollar-sign text. This was a recurring regression when
content passes added math to sections whose <head> lacked the renderer.
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "MATH_WITHOUT_RENDERER"
DESCRIPTION = "Page has math markup but no KaTeX/MathJax renderer loaded (math shows as raw text)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

RENDERER = re.compile(r'renderMathInElement|katex\.min\.js|MathJax|mathjax', re.I)
MATH_BLOCK = re.compile(r'class="math-block"')
MATH_SPAN = re.compile(r'class="math"')
DISPLAY_DD = re.compile(r'\$\$')
INLINE_TEX = re.compile(r'\$[^$\n]*\\[A-Za-z]+[^$\n]*\$')
STRIP = re.compile(r'<pre\b.*?</pre>|<code\b.*?</code>|<script\b.*?</script>',
                   re.DOTALL | re.IGNORECASE)


def run(filepath, html, context):
    if RENDERER.search(html):
        return []
    # math markers that need a renderer
    line = None
    msg_kind = None
    m = MATH_BLOCK.search(html) or MATH_SPAN.search(html)
    if m:
        msg_kind = 'class="math" block'
        line = html.count('\n', 0, m.start()) + 1
    else:
        body = STRIP.sub('', html)
        m2 = DISPLAY_DD.search(body) or INLINE_TEX.search(body)
        if m2:
            msg_kind = 'LaTeX $ delimiters'
            # line number is approximate (computed on stripped body)
            line = 1
    if not msg_kind:
        return []
    return [Issue(PRIORITY, CHECK_ID, filepath, line or 1,
                  f'Page has math ({msg_kind}) but no KaTeX/MathJax renderer; '
                  f'math will render as raw text. Add the KaTeX auto-render <head> block.')]
