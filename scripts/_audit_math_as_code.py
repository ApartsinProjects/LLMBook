"""Detect <pre><code class="...lang-X..."> blocks where content is actually math,
not code. Heuristic: contains math operators (||, ^, ∑, ∫, ∇, →) AND lacks
clear language indicators (no import, def, class, =, function-call patterns)."""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}

# Math signals: norms ||...||, summations, expectation E[...], theta_param,
# ^2, ∑, ∫, ∇, →
MATH_PATTERN = re.compile(
    r'(\|\|.*?\|\|'
    r'|\^[0-9-]'
    r'|\bE\s*\[\s*\|'
    r'|\\(?:sum|int|mathbb|mathcal|theta|phi|lambda|gamma|sigma|epsilon|tau|alpha|beta|delta)'
    r'|\bP\s*\(\s*[a-z]\s*\|'
    r'|→|⊗|⊙|∑|∇|∫|×'
    r')',
    re.MULTILINE,
)

# Code signals
CODE_PATTERN = re.compile(
    r'(?:^|\n)\s*(?:import |from |def |class |@\w+|return |if __name__|print\(|with |for \w+ in)'
)

candidates = []
for p in sorted(ROOT.rglob('*.html')):
    if set(p.parts) & SKIP:
        continue
    text = p.read_text(encoding='utf-8')
    # Find pre>code blocks (after Pygments highlighting, real code has many <span> tags;
    # math-as-code blocks have raw text without span)
    for m in re.finditer(
        r'<pre[^>]*><code class="[^"]*lang-([a-z]+)[^"]*">([\s\S]*?)</code></pre>',
        text,
    ):
        lang = m.group(1)
        body_html = m.group(2)
        # Strip any pygments tags
        body = re.sub(r'<span[^>]*>([\s\S]*?)</span>', r'\1', body_html)
        body = re.sub(r'<[^>]+>', '', body).strip()
        # Skip empty
        if len(body) < 5 or len(body) > 5000:
            continue
        # Short single-line blocks (one-liners) are common code; skip if has = and no math
        if MATH_PATTERN.search(body) and not CODE_PATTERN.search(body):
            # Likely math-as-code
            rel = str(p.relative_to(ROOT)).replace('\\', '/')
            candidates.append((rel, lang, body[:200]))

print(f'Math-as-code candidates: {len(candidates)}')
for f, lang, snippet in candidates[:40]:
    print(f'  {f}')
    print(f'    lang={lang}: {snippet[:140]}')
