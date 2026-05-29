"""v807b: Catch the remaining 31 inline-code paragraphs that v807
missed (because of &nbsp;/newline patterns the regex didn't match).

Simpler approach: find every <p>...</p> that has ≥2 <code>...</code><br>
sequences, extract them, convert to <pre><code>.
"""
from pathlib import Path
import re
import html as html_lib

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'agents/', 'templates/',
        'KDP/build', 'KDP/html2epub', 'pagefind']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


n_files = 0
n_blocks = 0


def replace_para(match):
    global n_blocks
    para = match.group(0)
    inner = match.group(1)
    # Count code+br
    code_count = len(re.findall(r'<code(?:\s[^>]*)?>[^<]+</code><br>', inner))
    if code_count < 2:
        return para
    # Extract leading run of code+br (possibly with &nbsp; indentation BEFORE each code)
    # The pattern: optional whitespace/&nbsp;, then <code>...</code><br>
    run_pattern = re.compile(
        r'^((?:\s*(?:&nbsp;|\xa0)*<code(?:\s[^>]*)?>[^<]+</code><br>\s*)+)',
        re.DOTALL
    )
    rm = run_pattern.match(inner)
    if not rm:
        return para
    run = rm.group(1)
    rest = inner[rm.end():].strip()
    # Parse each code line, capturing leading indent (in &nbsp;)
    lines = []
    line_pattern = re.compile(
        r'(?:(\s*(?:&nbsp;|\xa0)*))<code(?:\s[^>]*)?>([^<]+)</code><br>',
        re.DOTALL
    )
    for lm in line_pattern.finditer(run):
        indent_raw = lm.group(1) or ''
        # Count nbsp pairs as 2 spaces each
        n_nbsp = indent_raw.count('&nbsp;') + indent_raw.count('\xa0')
        indent = ' ' * (n_nbsp)
        code_text = html_lib.unescape(lm.group(2))
        lines.append(indent + code_text.rstrip())
    if len(lines) < 2:
        return para
    n_blocks += 1
    code_block_text = '\n'.join(lines)
    pre = (
        '<pre><code class="lang-python pygments-highlighted">'
        + code_block_text
        + '</code></pre>'
    )
    if rest:
        return pre + '\n<p>' + rest + '</p>'
    return pre


# Pattern: <p>...</p> that contains at least 2 code+br lines.
# Use non-greedy match for the content.
PARA_RE = re.compile(
    r'<p>((?:[^<]|<(?!p[\s>]|/p>))*?)</p>',
    re.DOTALL
)

for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    orig = s
    s = PARA_RE.sub(replace_para, s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        n_files += 1

print(f'Converted: {n_blocks} more inline-code paragraphs across {n_files} files.')
