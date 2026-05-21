"""
Author missing code-fragment captions across the book.

Detection
---------
For each section/appendix/capstone/front-matter HTML file under the book root
(skipping build/temp/vendor folders), the script finds every <pre> block whose
inner code is at least 30 characters of text. It then checks the next ~600
characters after the </pre> (and any optional <div class="code-output">) for
an existing code-caption (either <div> or <p>). If no caption is found, and
the <pre> is NOT inside a callout that has its own internal heading
(algorithm, library-shortcut, production-pattern), the block is missing a
caption.

Caption format
--------------
    <div class="code-caption"><strong>Code Fragment N.M.K:</strong> Text.</div>

Matches the established convention (1,184 of 1,185 existing captions use this
exact shape). N.M is the chapter.section prefix derived from the filename
(e.g. section-32.8.html -> 32.8, section-a.4.html -> a.4). K is the next
available sequence number, taken from the max existing "Code Fragment N.M.K"
in the file plus one.

Caption text
------------
Heuristic, in order of preference:
  1. The preceding sibling <p>'s first sentence (truncated, noun phrase).
  2. The code's first comment line (#, //, --).
  3. The defined function/class name(s).
  4. The imported library name(s).
  5. A generic "Python implementation of <section topic>" fallback derived
     from the file's <h1>.

Each caption is one sentence under ~25 words. No <em> wrapper (matches the
1,184 existing captions; the brief italic-ish wrapping is reserved for the
strong/colon prefix).

Wrapping
--------
If the <pre> is already inside a code-block-wrapper, the new caption is
inserted before that wrapper's closing </div>. Otherwise the <pre> and any
following <div class="code-output"> are wrapped in a fresh
<div class="code-block-wrapper">...</div> together with the caption.

Idempotency
-----------
Re-runs are safe: blocks that already have a caption in the next ~600 chars
are skipped. Captions that exist anywhere in the same code-block-wrapper are
also detected. The number reservation respects pre-existing captions in the
file (max K + 1).

Usage
-----
    python _author_code_captions.py            # dry run (default)
    python _author_code_captions.py --apply    # write changes
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    'node_modules', '.git', 'KDP', 'build', 'temp_ebook', 'temp_epub',
    'source_fix_backups', 'pagefind', 'templates', '.claude',
    '.book-update', 'vendor', 'scripts', 'docs', 'styles',
    '.html2pub_cache', '_concept-figs', 'agents', 'tmp_whats_next',
    'images', 'downloads',
}

TAG_RE = re.compile(r'<[^>]+>')
PRE_RE = re.compile(r'<pre[^>]*>(?:<code[^>]*>)?(.*?)(?:</code>)?</pre>', re.DOTALL)
CAPTION_PRESENT_RE = re.compile(r'class="code-caption"')
OUTPUT_RE = re.compile(r'\s*<div class="code-output"[^>]*>.*?</div>', re.DOTALL)
EXISTING_NUM_RE_TPL = r'Code Fragment\s+{prefix}\.(\d+)'
WRAPPER_OPEN = '<div class="code-block-wrapper">'

CALLOUT_SKIP_CLASSES = [
    'callout algorithm',
    'callout library-shortcut',
    'callout production-pattern',
    'callout note',  # "Example output" boxes carry <pre class="callout-output-body">
]

# Container divs whose <pre> blocks are decorative rather than source code
DECORATIVE_CONTAINER_CLASSES = [
    'diagram-container',
    'figure',  # plain <figure> elements come through as containers too
]

# <pre> classes that mark non-code content (outputs, terminal logs, etc.)
NON_CODE_PRE_CLASSES = {
    'callout-output-body',
    'console-output',
    'terminal-output',
    'output',
}

# Caption-text heuristics ----------------------------------------------------

STOP_FIRST_WORDS = {
    'this', 'these', 'that', 'those', 'it', 'they', 'there',
    'we', 'you', 'i', 'one', 'each', 'every', 'all', 'both',
}

LANG_HINTS = {
    'python': 'Python',
    'bash': 'Shell',
    'sh': 'Shell',
    'shell': 'Shell',
    'javascript': 'JavaScript',
    'js': 'JavaScript',
    'typescript': 'TypeScript',
    'ts': 'TypeScript',
    'yaml': 'YAML',
    'yml': 'YAML',
    'json': 'JSON',
    'sql': 'SQL',
    'dockerfile': 'Dockerfile',
    'docker': 'Dockerfile',
    'rust': 'Rust',
    'go': 'Go',
    'cuda': 'CUDA',
    'c': 'C',
    'cpp': 'C++',
    'html': 'HTML',
    'css': 'CSS',
    'text': 'Configuration',
}


def strip_tags(html: str) -> str:
    return TAG_RE.sub('', html).strip()


def trim_sentence(text: str, max_words: int = 28) -> str:
    """Return the first sentence/clause of text, capped at max_words words."""
    text = re.sub(r'\s+', ' ', text).strip()
    # cut at sentence-ending punctuation
    m = re.search(r'([.!?])\s', text + ' ')
    if m:
        text = text[: m.start() + 1]
    # word cap: if exceeded, prefer to break at a comma or semicolon
    words = text.split(' ')
    if len(words) > max_words:
        head = ' '.join(words[:max_words])
        # walk back to the last sentence/clause break
        for break_char in (';', ','):
            idx = head.rfind(break_char)
            if idx > len(head) // 2:  # at least past halfway
                text = head[:idx] + '.'
                break
        else:
            text = head.rstrip(',;:') + '.'
    # ensure terminal punctuation
    if text and text[-1] not in '.!?':
        text += '.'
    # capitalize first letter
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def caption_from_paragraph(paragraph_html: str) -> str | None:
    """Build a caption from a preceding <p>'s text."""
    text = strip_tags(paragraph_html)
    if not text or len(text) < 25:
        return None
    # Prefer sub-clauses that explain code: "Here is X", "X looks like:"
    # but most often the preceding p just sets context. Pull the first
    # sentence and prepend a verb that hints at code.
    first = trim_sentence(text, max_words=22)
    if not first:
        return None
    # If sentence starts with a pronoun/discourse marker, swap in a phrase.
    first_word = first.split(' ', 1)[0].lower().rstrip(',.;:')
    if first_word in STOP_FIRST_WORDS:
        # rewrite as "Implementation of the loop described above."
        return None
    return first


GENERIC_COMMENTS = {
    'pytorch implementation', 'python implementation',
    'tensorflow implementation', 'jax implementation',
    'numpy implementation', 'simple example', 'minimal example',
    'reference implementation', 'toy implementation',
    'demo code', 'example code', 'example usage', 'usage example',
    'sketch of the idea', 'pseudo-code', 'pseudocode',
}


def caption_from_code_comment(code_text: str) -> str | None:
    clean = strip_tags(code_text)
    for raw in clean.split('\n')[:6]:
        line = raw.strip()
        for marker in ('#', '//', '--'):
            if line.startswith(marker):
                body = line.lstrip(marker).strip()
                if len(body) < 12:
                    continue
                lo = body.lower().rstrip('.!?:')
                if lo in ('example', 'code', 'test', 'setup', '---'):
                    continue
                if lo in GENERIC_COMMENTS:
                    continue
                if lo.startswith(('!pip', 'pip install', 'usage:')):
                    continue
                # Skip filename-only comments like "app.py" or "src/foo.py (commentary)"
                if re.match(r'^[\w/.-]+\.(py|sh|js|ts|yaml|yml|json|env|conf|toml|md|txt|cfg|ini)\b', lo):
                    continue
                return trim_sentence(body, max_words=20)
    return None


def caption_from_code_structure(code_text: str) -> str | None:
    clean = strip_tags(code_text)
    classes = re.findall(r'\bclass\s+([A-Za-z_]\w*)', clean)
    funcs = re.findall(r'\bdef\s+([A-Za-z_]\w*)', clean)
    if classes:
        names = ', '.join(classes[:2])
        return trim_sentence(f'Defining {names}.', max_words=20)
    if funcs:
        names = ', '.join(funcs[:2])
        return trim_sentence(f'Implementation of {names}.', max_words=20)
    imports = re.findall(r'(?:from|import)\s+([\w.]+)', clean)
    if imports:
        libs = []
        for imp in imports:
            top = imp.split('.')[0]
            if top not in libs:
                libs.append(top)
            if len(libs) == 3:
                break
        return trim_sentence(f'Working with {", ".join(libs)}.', max_words=20)
    return None


def caption_fallback(language: str, h1_title: str) -> str:
    """Final-resort caption: '<Language> implementation of <topic>.'"""
    lang_name = LANG_HINTS.get(language.lower(), language or 'Python')
    # strip leading "Section N.M:" or chapter prefix from h1
    topic = re.sub(r'^[Ss]ection\s+[\d.a-z]+:\s*', '', h1_title).strip()
    topic = re.sub(r'^[A-Z][a-z]+\s+\d+:\s*', '', topic).strip()
    if not topic:
        topic = 'the technique above'
    # lowercase the first word for grammar
    topic = topic[0].lower() + topic[1:] if topic and topic[0].isupper() else topic
    return trim_sentence(f'{lang_name} implementation of {topic}.', max_words=20)


# Structural helpers --------------------------------------------------------

def _div_span(content: str, start: int) -> int:
    """Return absolute end of the div opened at `start`, or -1 on imbalance."""
    depth = 0
    pos = start
    while pos < len(content):
        if content.startswith('<div', pos):
            depth += 1
            pos += 4
            continue
        if content.startswith('</div>', pos):
            depth -= 1
            pos += 6
            if depth == 0:
                return pos
            continue
        pos += 1
    return -1


def find_callout_ranges(content: str) -> list[tuple[int, int]]:
    """Return byte spans of callouts whose code blocks should be skipped."""
    ranges = []
    for cls in CALLOUT_SKIP_CLASSES:
        needle = f'<div class="{cls}"'
        idx = 0
        while True:
            start = content.find(needle, idx)
            if start == -1:
                break
            end = _div_span(content, start)
            if end == -1:
                idx = start + 1
                continue
            ranges.append((start, end))
            idx = end
    return ranges


def find_decorative_ranges(content: str) -> list[tuple[int, int]]:
    """Return byte spans of decorative containers whose <pre>s aren't code."""
    ranges = []
    for cls in DECORATIVE_CONTAINER_CLASSES:
        needle = f'<div class="{cls}"'
        idx = 0
        while True:
            start = content.find(needle, idx)
            if start == -1:
                break
            end = _div_span(content, start)
            if end == -1:
                idx = start + 1
                continue
            ranges.append((start, end))
            idx = end
    # also include <figure>...</figure>
    idx = 0
    while True:
        start = content.find('<figure', idx)
        if start == -1:
            break
        end_tag = content.find('</figure>', start)
        if end_tag == -1:
            idx = start + 1
            continue
        ranges.append((start, end_tag + len('</figure>')))
        idx = end_tag + 1
    return ranges


def in_ranges(pos: int, ranges: list[tuple[int, int]]) -> bool:
    return any(s <= pos < e for s, e in ranges)


def find_enclosing_wrapper(content: str, pre_start: int, pre_end: int) -> tuple[int, int] | None:
    """If the <pre> is inside a code-block-wrapper, return its (start, end)."""
    # look back ~800 chars for a wrapper open with no intervening close
    look_start = max(0, pre_start - 800)
    region = content[look_start:pre_start]
    open_idx = region.rfind(WRAPPER_OPEN)
    if open_idx == -1:
        return None
    abs_open = look_start + open_idx
    # check that no </div> closing the wrapper appears between abs_open and pre_start
    # by div-depth counting from abs_open
    depth = 0
    pos = abs_open
    wrapper_end = -1
    while pos < len(content):
        if content.startswith('<div', pos):
            depth += 1
            pos += 4
            continue
        if content.startswith('</div>', pos):
            depth -= 1
            pos += 6
            if depth == 0:
                wrapper_end = pos
                break
            continue
        pos += 1
    if wrapper_end == -1:
        return None
    if abs_open <= pre_start and pre_end <= wrapper_end:
        return (abs_open, wrapper_end)
    return None


def preceding_paragraph(content: str, pre_start: int) -> str | None:
    """Return the immediately-preceding <p>...</p> text (HTML), or None."""
    # walk backwards skipping whitespace and non-paragraph tags
    cursor = pre_start
    look = content[max(0, cursor - 4000):cursor]
    # find last </p> in look
    p_end = look.rfind('</p>')
    if p_end == -1:
        return None
    # find matching <p
    p_start = look.rfind('<p', 0, p_end)
    if p_start == -1:
        return None
    # require that between </p> and pre_start there are only whitespace
    # and known structural tags
    after_p = look[p_end + 4:]
    # remove all tags from the gap; if there is real text, the paragraph is
    # not directly preceding the code
    gap_text = strip_tags(after_p)
    if len(gap_text) > 80:
        return None
    return look[p_start:p_end + 4]


def section_prefix(stem: str) -> str | None:
    m = re.match(r'section-(\d+)\.(\d+)$', stem)
    if m:
        return f'{m.group(1)}.{m.group(2)}'
    m = re.match(r'section-([a-z])\.(\d+)$', stem)
    if m:
        return f'{m.group(1)}.{m.group(2)}'
    # index pages: chapter index pages can also carry code; use chapter num
    m = re.match(r'index$', stem)
    if m:
        return None  # skip; index files rarely have captioned fragments
    return None


def h1_title(content: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if not m:
        return ''
    return strip_tags(m.group(1))


def code_language(pre_open: str, code_text: str) -> str:
    m = re.search(r'lang-([a-z]+)', pre_open)
    if m:
        return m.group(1)
    # try class="language-foo"
    m = re.search(r'language-([a-z]+)', pre_open)
    if m:
        return m.group(1)
    return 'python'


def caption_text(paragraph_html: str | None,
                 code_text: str,
                 language: str,
                 h1: str) -> str:
    for builder in (
        lambda: caption_from_paragraph(paragraph_html) if paragraph_html else None,
        lambda: caption_from_code_comment(code_text),
        lambda: caption_from_code_structure(code_text),
    ):
        text = builder()
        if text:
            return text
    return caption_fallback(language, h1)


def next_caption_seq(content: str, prefix: str) -> int:
    pattern = re.compile(EXISTING_NUM_RE_TPL.format(prefix=re.escape(prefix)))
    used = [int(n) for n in pattern.findall(content)]
    return (max(used) if used else 0) + 1


# File processing -----------------------------------------------------------

def process_file(path: Path, apply: bool) -> tuple[int, int]:
    """Return (added, skipped_short_or_callout)."""
    prefix = section_prefix(path.stem)
    if prefix is None:
        return (0, 0)
    try:
        content = path.read_text(encoding='utf-8')
    except Exception:
        return (0, 0)

    callout_ranges = find_callout_ranges(content)
    decorative_ranges = find_decorative_ranges(content)
    h1 = h1_title(content)

    blocks = list(PRE_RE.finditer(content))
    if not blocks:
        return (0, 0)

    seq = next_caption_seq(content, prefix)
    insertions: list[tuple[int, int, str]] = []  # (insert_pos, replace_end, html)
    added = 0
    skipped = 0

    for m in blocks:
        pre_start = m.start()
        pre_end = m.end()
        pre_open = m.group(0)[:m.group(0).find('>') + 1]

        # Skip non-code <pre>s (output blocks etc.)
        if any(cls in pre_open for cls in NON_CODE_PRE_CLASSES):
            skipped += 1
            continue

        code_inner = m.group(1)
        code_text_plain = strip_tags(code_inner)
        if len(code_text_plain) < 30:
            skipped += 1
            continue

        if in_ranges(pre_start, callout_ranges):
            skipped += 1
            continue

        if in_ranges(pre_start, decorative_ranges):
            skipped += 1
            continue

        # Skip <pre style="..."> blocks (decorative styled boxes, not code)
        if 'style=' in pre_open and 'pygments' not in pre_open and 'lang-' not in pre_open:
            skipped += 1
            continue

        # Look at content directly after </pre>, possibly skipping a code-output
        tail_start = pre_end
        output_match = OUTPUT_RE.match(content, tail_start)
        if output_match:
            tail_start = output_match.end()

        look_ahead = content[tail_start:tail_start + 600]
        if CAPTION_PRESENT_RE.search(look_ahead):
            continue  # already captioned

        # Determine wrapper status
        wrapper = find_enclosing_wrapper(content, pre_start, pre_end)
        if wrapper:
            # caption belongs just before the wrapper's closing </div>
            wrap_start, wrap_end = wrapper
            # double-check no caption inside the wrapper already
            if CAPTION_PRESENT_RE.search(content[wrap_start:wrap_end]):
                continue

        para_html = preceding_paragraph(content, pre_start)
        language = code_language(m.group(0), code_inner)
        text = caption_text(para_html, code_inner, language, h1)
        k = seq
        seq += 1
        caption_html = (
            f'<div class="code-caption">'
            f'<strong>Code Fragment {prefix}.{k}:</strong> {text}'
            f'</div>'
        )

        if wrapper:
            wrap_end = wrapper[1]
            # insert before the closing </div>
            insert_pos = wrap_end - len('</div>')
            insertions.append((insert_pos, insert_pos, '\n' + caption_html + '\n'))
        else:
            # need to wrap pre [+ optional output] in a code-block-wrapper
            block_start = pre_start
            block_end = tail_start  # includes any output
            wrapped = (
                WRAPPER_OPEN + '\n'
                + content[block_start:block_end].rstrip()
                + '\n' + caption_html
                + '\n</div>'
            )
            insertions.append((block_start, block_end, wrapped))

        added += 1

    if added == 0:
        return (0, skipped)

    if apply:
        # apply in reverse order
        new_content = content
        for ins_start, ins_end, html in sorted(insertions, key=lambda x: x[0], reverse=True):
            new_content = new_content[:ins_start] + html + new_content[ins_end:]
        path.write_text(new_content, encoding='utf-8')

    return (added, skipped)


# Main ----------------------------------------------------------------------

def iter_html_files(root: Path):
    for path in root.rglob('*.html'):
        parts = set(path.parts)
        if parts & SKIP_DIRS:
            continue
        yield path


def main() -> int:
    apply = '--apply' in sys.argv
    files = sorted(iter_html_files(BOOK_ROOT))

    total_added = 0
    files_touched = []
    files_skipped_clean = 0
    files_skipped_no_section = 0

    for path in files:
        if section_prefix(path.stem) is None:
            files_skipped_no_section += 1
            continue
        added, _ = process_file(path, apply)
        if added:
            rel = path.relative_to(BOOK_ROOT)
            files_touched.append((str(rel), added))
            total_added += added
        else:
            files_skipped_clean += 1

    mode = 'APPLIED' if apply else 'DRY RUN'
    print(f'=== Code-fragment caption author ({mode}) ===')
    print(f'HTML files scanned (section-style): {len(files) - files_skipped_no_section}')
    print(f'Files needing captions: {len(files_touched)}')
    print(f'Files already clean: {files_skipped_clean}')
    print(f'Captions {"added" if apply else "would be added"}: {total_added}')

    if files_touched:
        print()
        print('Top files (count, path):')
        for rel, n in sorted(files_touched, key=lambda x: -x[1])[:25]:
            print(f'  {n:3d}  {rel}')
        if len(files_touched) > 25:
            print(f'  ... +{len(files_touched) - 25} more files')

    if not apply and total_added:
        print('\nRe-run with --apply to write changes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
