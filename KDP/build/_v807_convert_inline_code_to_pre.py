"""v807: Convert multi-line inline-code patterns in Answer Sketches
to proper <pre><code> blocks with syntax highlighting.

PATTERN
=======
Author wrote answer sketches like:
  <p><code>line1</code><br>
  <code>line2</code><br>
  <code>line3</code><br>
  followed by prose.</p>

This renders as monospaced italic inline text with no syntax color.
EPUB readers can't break long inline code lines well.

FIX
===
Find consecutive `<code>...</code><br>` runs (2+) inside a <p>.
Replace each run with:
  </p><pre><code class="lang-python pygments-highlighted">line1
  line2
  line3
  </code></pre><p>
Then run pygments via the existing syntax_highlight hook at build time.

ASSUMPTION: All inline-code-line patterns in the book are Python.
(Sampled across 5 files — all are Python imports/torch/tiktoken/etc.)
"""
from pathlib import Path
import re
import html

ROOT = Path(__file__).resolve().parents[2]

SKIP = ['node_modules', '.git', 'output', 'backup', 'agents/', 'templates/',
        'KDP/build', 'KDP/html2pub', 'pagefind']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


n_files = 0
n_blocks = 0

# Pattern: <p>...<code>X</code><br>...<code>Y</code>...(any combo of these)...</p>
# But we want to convert ONLY consecutive code+br runs at the start, leaving prose intact.
# Approach: find runs of `<code>...</code><br>` at the start of a <p>, capture them, replace.

for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    orig = s

    # Find every <p> that contains a run of code+br at its start
    def process_paragraph(m):
        global n_blocks
        para_open = m.group(1)
        body = m.group(2)
        # Find the leading run of `<code>...</code><br>\s*` lines
        run_pattern = re.compile(
            r'^\s*((?:<code(?:\s[^>]*)?>[^<]+</code><br>\s*)+)',
            re.DOTALL
        )
        rm = run_pattern.match(body)
        if not rm:
            return m.group(0)  # no leading code run; keep as is
        code_run = rm.group(1)
        rest = body[rm.end():].strip()
        # Extract each code line
        code_lines = re.findall(
            r'<code(?:\s[^>]*)?>([^<]+)</code><br>',
            code_run
        )
        if len(code_lines) < 2:
            return m.group(0)  # only one line; keep inline
        # Decode HTML entities and join with newlines
        text_lines = []
        for cl in code_lines:
            decoded = html.unescape(cl)
            # Replace &nbsp; (already decoded to \xa0) with two spaces (indent)
            decoded = decoded.replace('\xa0\xa0', '  ').replace('\xa0', ' ')
            text_lines.append(decoded)
        code_block_text = '\n'.join(text_lines)
        n_blocks += 1
        # Compose replacement: close current <p>, insert <pre><code>, optionally re-open <p>
        pre_block = (
            f'</p>\n<pre><code class="lang-python pygments-highlighted">'
            + code_block_text
            + '</code></pre>'
        )
        if rest:
            pre_block += f'\n<p>{rest}</p>'
        else:
            pre_block += '\n<p></p>'  # empty stub (will be cleaned up)
        # Note: the original <p> open tag is replaced (we close it explicitly above)
        return para_open + pre_block.lstrip('</p>\n')   # no-op if no rest

    # Use a regex that captures <p>...</p> non-greedy (but allows inner tags)
    # Reduced complexity: find runs only when the leading content starts with <code>
    pattern = re.compile(
        r'(<p>)\s*((?:<code(?:\s[^>]*)?>[^<]+</code><br>\s*){2,}[^<]*?(?:<[^p][^>]*>[^<]*</[^>]+>[^<]*)*)\s*</p>',
        re.DOTALL
    )

    def replace_p(m):
        global n_blocks
        body = m.group(2)
        # Find leading run of code+br
        rm = re.match(r'^\s*((?:<code(?:\s[^>]*)?>[^<]+</code><br>\s*)+)', body, re.DOTALL)
        if not rm:
            return m.group(0)
        code_run = rm.group(1)
        rest = body[rm.end():].strip()
        code_lines = re.findall(r'<code(?:\s[^>]*)?>([^<]+)</code><br>', code_run)
        if len(code_lines) < 2:
            return m.group(0)
        text_lines = []
        for cl in code_lines:
            decoded = html.unescape(cl)
            decoded = decoded.replace('\xa0', ' ')
            text_lines.append(decoded.rstrip())
        code_block_text = '\n'.join(text_lines)
        n_blocks += 1
        out = (
            f'<pre><code class="lang-python pygments-highlighted">'
            + code_block_text
            + '</code></pre>'
        )
        if rest:
            out += f'\n<p>{rest}</p>'
        return out

    s = pattern.sub(replace_p, s)

    if s != orig:
        p.write_text(s, encoding='utf-8')
        n_files += 1

print(f'Converted inline-code blocks to <pre><code>: {n_blocks} blocks across {n_files} files.')
