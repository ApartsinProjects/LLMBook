"""Detect bare English words inside math delimiters (without \\text{}).

Pattern (BAD):
  $$Keep token x_{i} \\text{if} P(x_{i}) \\geq min_p \\times max_{j} P(x_{j})$$

KaTeX renders bare English words in math-italic, producing weird-looking
output. The fix is to wrap English words in \\text{...} OR use \\mathrm
for operator names like \\min, \\max, etc.

Detection: inside $$...$$ or $...$, look for consecutive English-letter
sequences of length >= 4 that are NOT inside \\text{}, \\mathrm{},
\\operatorname{}, \\mathit{}, \\mathbf{}, etc.

Common operator names that are flagged by KaTeX as undefined: min, max,
log, ln, exp, sin, cos, tan (when written as plain text not as
\\min, \\max etc.).
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "MATH_BARE_TEXT"
DESCRIPTION = 'Bare English words inside math delimiters (should be wrapped in \\text{} or \\mathrm{})'

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Find math blocks (display or inline)
DISPLAY_MATH_RE = re.compile(r'\$\$([\s\S]+?)\$\$')
INLINE_MATH_RE = re.compile(r'(?<!\$)\$([^$\n]+?)\$(?!\$)')

# KaTeX operators that ARE supported as-is (these are fine bare):
KATEX_OPS = {
    'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'arcsin', 'arccos', 'arctan',
    'sinh', 'cosh', 'tanh', 'coth', 'log', 'ln', 'exp', 'lim', 'sup', 'inf',
    'min', 'max', 'arg', 'gcd', 'lcm', 'det', 'dim', 'ker', 'hom', 'mod',
    'and', 'or', 'not', 'iff', 'forall', 'exists', 'in', 'to', 'mapsto',
}

# But these need backslash prefix (\\min). Without it, KaTeX renders them
# as italic letter sequences. So we WANT to flag bare "min" not preceded
# by backslash.

# Word inside math: any letter sequence of 4+ chars that doesn't have a
# backslash before it
BARE_WORD_RE = re.compile(r'(?<![\\\w])[A-Za-z]{4,}')


def _check_math(content, filepath, html, math_start, is_display, issues):
    # Only worth flagging DISPLAY math ($$...$$) — inline $...$ math often
    # produces false positives because tight inline math is rare and the
    # detector confuses prose between two math snippets for math content.
    if not is_display:
        return
    # Skip very short math (< 20 chars) — likely a single symbol like $x_i$
    if len(content.strip()) < 20:
        return
    # Remove \text{...}, \mathrm{...}, \mathbf{...}, \mathit{...},
    # \operatorname{...} contents before checking — those are intentionally
    # text. Allow nested braces by running multiple passes.
    cleaned = content
    for _ in range(3):
        new = re.sub(
            r'\\(?:text|mathrm|mathbf|mathit|operatorname|mathsf|mathtt|mathcal|texttt|textbf|textit)\{[^{}]*\}',
            '',
            cleaned,
        )
        if new == cleaned:
            break
        cleaned = new
    # Remove LaTeX command names
    cleaned = re.sub(r'\\[a-zA-Z]+', '', cleaned)
    # Strip subscripts/superscripts braced content (a_{abc} is OK math)
    cleaned = re.sub(r'\{[^{}]*\}', '', cleaned)

    bare_words = BARE_WORD_RE.findall(cleaned)
    # Threshold: flag only when 2+ bare English words remain. A single
    # variable name like "loss" can be acceptable; multiple together
    # signals true prose-in-math.
    if len(bare_words) >= 2:
        line = html[:math_start].count('\n') + 1
        snippet = content[:80].replace('\n', ' ')
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Bare words {bare_words[:4]} inside $$...$$ display math '
            f'(should be \\text{{...}} or \\mathrm{{...}}): "{snippet}..."'
        ))


def run(filepath, html, context):
    issues = []
    if not filepath.name.endswith('.html'):
        return issues
    # Skip <pre> and <code> blocks (code may legitimately have $1.50 etc.)
    # The detector is for prose math only.
    # Naive approach: strip <pre>...</pre> regions first.
    clean = re.sub(r'<pre[\s\S]*?</pre>', '', html)

    for m in DISPLAY_MATH_RE.finditer(clean):
        _check_math(m.group(1), filepath, html, m.start(), True, issues)
    for m in INLINE_MATH_RE.finditer(clean):
        _check_math(m.group(1), filepath, html, m.start(), False, issues)
    return issues
