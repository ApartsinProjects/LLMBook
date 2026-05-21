"""Restyle library-shortcut callout code blocks: wrap in <details class="code-collapsible">.

Each <pre><code> inside a <div class="callout library-shortcut"> is restructured to:

  <details class="code-collapsible">
    <summary>Show code</summary>
    <div class="code-block-wrapper">
      <pre><code class="language-python">...existing code...</code></pre>
    </div>
    <div class="code-caption">Code Fragment X.Y.N: <description></div>
  </details>

Behavior:
 - If the pre block is already inside <div class="code-block-wrapper">, the
   wrapper is reused (we only add the <details> outside and possibly add a
   <div class="code-caption"> inside the wrapper if it's missing).
 - If the pre block is bare, we wrap it in <div class="code-block-wrapper">
   before wrapping in <details>.
 - Idempotent: if a callout already has <details class="code-collapsible"> with
   the canonical structure, it is skipped.
 - Fragment numbering: scans the section for the highest existing
   Code Fragment X.Y.N integer N for the current section and starts numbering
   new fragments at N+1.
 - Captions are generated from the callout title (library name) and, when
   available, the leading comment in the code snippet. No em dashes per
   project style.

Usage:
    /c/Python314/python scripts/_collapse_library_shortcut_code.py            # dry-run
    /c/Python314/python scripts/_collapse_library_shortcut_code.py --apply    # write
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

EXCLUDE = {"KDP", "node_modules", ".git", "temp_ebook", "temp_epub",
           "source_fix_backups", "pagefind", "templates", ".claude",
           ".book-update", "vendor", "scripts", "docs", "styles",
           "build", "_archive", "__pycache__", "agents", "downloads",
           "_concept-figs"}


def is_excluded(p: Path) -> bool:
    rel = p.relative_to(PROJECT_ROOT)
    for part in rel.parts:
        if part in EXCLUDE or part.startswith("temp_"):
            return True
    return False


CALLOUT_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+library-shortcut"[^>]*>',
    re.IGNORECASE,
)
CALLOUT_TITLE_RE = re.compile(
    r'<div\s+class="callout-title"[^>]*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
FRAGMENT_NUM_RE = re.compile(
    r'Code\s+Fragment\s+(\d+(?:\.\d+)+)(?:\.(\d+))?',
    re.IGNORECASE,
)
# Match <pre>...</pre>
PRE_RE = re.compile(r'<pre\b[^>]*>(.*?)</pre>', re.IGNORECASE | re.DOTALL)
# Match a code-block-wrapper opening tag
CBW_OPEN_RE = re.compile(r'<div\s+class="code-block-wrapper"[^>]*>', re.IGNORECASE)


def find_div_close(html: str, after_open: int) -> int:
    """Find the matching </div> for a <div> whose open tag ends at after_open.

    Returns the index where the closing </div> tag starts, or -1 if not found.
    """
    depth = 1
    pos = after_open
    tag_re = re.compile(r'<(/?)div\b', re.IGNORECASE)
    while pos < len(html) and depth > 0:
        m = tag_re.search(html, pos)
        if not m:
            return -1
        if m.group(1) == "/":
            depth -= 1
        else:
            depth += 1
        pos = m.end()
        if depth == 0:
            return m.start()
    return -1


def find_section_prefix(filepath: Path) -> str:
    """Extract the section number prefix (e.g. '1.3', '37.5a') from a section filename.

    section-1.3.html -> '1.3'
    section-3.1a.html -> '3.1a'
    """
    m = re.match(r'section-([\d\.]+[a-z]?)\.html$', filepath.name, re.IGNORECASE)
    if m:
        return m.group(1)
    return ""


def existing_fragment_numbers(html: str, section_prefix: str) -> set[int]:
    """Find all Code Fragment {section_prefix}.N references in the section.

    Returns a set of integer N values used.
    """
    used = set()
    if not section_prefix:
        return used
    # Escape the section prefix because it may have a dot in it
    escaped = re.escape(section_prefix)
    pattern = re.compile(
        rf'Code\s+Fragment\s+{escaped}\.(\d+)(?:[a-z])?\b',
        re.IGNORECASE,
    )
    for m in pattern.finditer(html):
        try:
            used.add(int(m.group(1)))
        except ValueError:
            pass
    return used


def next_fragment_int(used: set[int]) -> int:
    """Return the smallest positive integer not in `used` (starting at 1)."""
    n = 1
    while n in used:
        n += 1
    return n


def extract_library_name_from_title(title_html: str) -> str:
    """Extract a friendly library name from a callout-title.

    Examples:
      'Library Shortcut'                                    -> ''
      'Library Shortcut: LiteLLM for ...'                   -> 'LiteLLM'
      'Library Shortcut: BioNeMo for Genomic Language ...'  -> 'BioNeMo'
      'Library Shortcut: langgraph (state-machine ...)'     -> 'langgraph'
    """
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', title_html).strip()
    # Strip "Library Shortcut" prefix
    text = re.sub(r'^Library\s+Shortcut\s*:?\s*', '', text, flags=re.IGNORECASE).strip()
    if not text:
        return ""
    # Take the first chunk before " for ", " (", " to ", " in ", " on ", etc.
    text = re.split(r'\s+(?:for|to|in|on|with|via)\s+|\s*\(', text, maxsplit=1)[0]
    return text.strip()


def extract_leading_code_comment(code_html: str) -> str:
    """Extract a *leading* comment from a code snippet (only if the snippet
    starts with one, not trailing comments on later lines).

    Returns the comment text without the leading '# ' or empty string.
    """
    # Convert HTML to plain text first for a cleaner heuristic.
    text = re.sub(r'<[^>]+>', '', code_html)
    text = (text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                .replace('&quot;', '"').replace('&#39;', "'"))
    leading_comments = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            # Allow blank lines at the top
            if leading_comments:
                break
            continue
        if stripped.startswith('#') and not stripped.startswith('#!'):
            comment = stripped.lstrip('#').strip()
            if comment:
                leading_comments.append(comment)
        else:
            # First non-comment, non-blank line; stop collecting.
            break
    if leading_comments:
        # Use the first comment as the caption seed
        first = leading_comments[0]
        # Skip uninformative comments like just "(Using pre-trained vectors)"
        if len(first) > 8:
            return first
    return ""


def extract_callout_intro(body_html: str) -> tuple[str, str]:
    """Pull the first descriptive <p> inside a library-shortcut callout body.

    Returns (raw_inner_html, plain_text). Skips the trailing "pip install ..." <p>.
    Both strings are empty if no useful paragraph is found.
    """
    paras = re.findall(r'<p\b[^>]*>(.*?)</p>', body_html, re.IGNORECASE | re.DOTALL)
    for p in paras:
        text = re.sub(r'<[^>]+>', '', p)
        text = (text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                    .replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' '))
        text = re.sub(r'\s+', ' ', text).strip()
        if text.lower().startswith('pip install'):
            continue
        if text and len(text) > 12:
            return p, text
    return "", ""


def _scrub_emdash(s: str) -> str:
    """Replace em/en dashes and ASCII double dashes with commas (project style)."""
    return s.replace('—', ', ').replace('–', ', ').replace('--', ', ')


def _detect_library_from_intro(intro_text: str) -> str:
    """Try to find a bolded library name like '<strong>sentence-transformers</strong>'
    in the raw intro paragraph (before stripping tags). Caller passes raw HTML.
    """
    m = re.search(r'<strong>([^<]+)</strong>', intro_text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""


def generate_caption(
    library_name: str,
    code_html: str,
    fragment_label: str,
    intro_text: str = "",
    intro_html: str = "",
) -> str:
    """Generate a one-sentence code-caption description.

    Strategy:
      1. If a leading comment exists in the snippet, use it (the author
         usually wrote it as a one-line summary).
      2. Else if the callout intro mentions the library in a bold tag, build
         a sentence like "Three-line example using <code>sentence-transformers</code>."
      3. Else use the library name from the title (or "this library").
    """
    comment = extract_leading_code_comment(code_html)
    sentence = ""
    if comment:
        comment_clean = comment.rstrip('. ').strip()
        comment_clean = _scrub_emdash(comment_clean)
        if comment_clean:
            comment_clean = comment_clean[0].upper() + comment_clean[1:]
        sentence = f"{comment_clean}."
    else:
        bold_lib = _detect_library_from_intro(intro_html) if intro_html else ""
        chosen = library_name or bold_lib or "the library"
        sentence = f"Minimal working example using <code>{chosen}</code>."
    sentence = _scrub_emdash(sentence)
    return (
        f'<strong>{fragment_label}:</strong> {sentence}'
    )


def already_collapsed(callout_body: str) -> bool:
    """Check if the callout body already contains a <details class="code-collapsible">."""
    return bool(re.search(
        r'<details\s+class="code-collapsible"',
        callout_body, re.IGNORECASE,
    ))


def transform_callout_body(
    body_html: str,
    section_prefix: str,
    fragment_int: int | None,
) -> tuple[str, int]:
    """Transform a single library-shortcut callout body.

    Returns (new_body, num_transformations).

    `fragment_int` may be None if the callout already has a code-caption
    (in which case no new caption is generated).
    """
    if already_collapsed(body_html):
        return body_html, 0

    # Find the library name from the callout title
    title_m = CALLOUT_TITLE_RE.search(body_html)
    library_name = ""
    if title_m:
        library_name = extract_library_name_from_title(title_m.group(1))

    intro_html, intro_text = extract_callout_intro(body_html)

    # Find the first <pre>...</pre> in the body and the smallest enclosing
    # <div class="code-block-wrapper"> if it exists.
    pre_m = PRE_RE.search(body_html)
    if not pre_m:
        return body_html, 0

    pre_start, pre_end = pre_m.span()
    code_html_inside_pre = pre_m.group(1)

    # Determine the span we'll wrap. Look for a code-block-wrapper that
    # contains this <pre>.
    wrap_start = pre_start
    wrap_end = pre_end
    has_wrapper = False

    # Find the latest code-block-wrapper opening tag before pre_start whose
    # closing </div> is after pre_end.
    for cbw_m in CBW_OPEN_RE.finditer(body_html):
        if cbw_m.start() < pre_start:
            cbw_close = find_div_close(body_html, cbw_m.end())
            if cbw_close >= pre_end:
                wrap_start = cbw_m.start()
                # The full wrapper extent ends at cbw_close + len('</div>')
                # We need to include the closing </div> too.
                # find_div_close returns the position of "</div>", so include 6 chars
                wrap_end = cbw_close + len("</div>")
                has_wrapper = True
                break

    wrap_block = body_html[wrap_start:wrap_end]

    # Decide whether to insert a caption.
    has_caption = 'code-caption' in wrap_block

    fragment_label = (
        f"Code Fragment {section_prefix}.{fragment_int}"
        if fragment_int is not None
        else ""
    )

    if has_wrapper:
        # Reuse existing wrapper. Append caption inside if missing.
        new_wrap = wrap_block
        if not has_caption:
            # Insert caption just before the closing </div> of the wrapper.
            caption_html = (
                f'<div class="code-caption">'
                f'{generate_caption(library_name, code_html_inside_pre, fragment_label, intro_text, intro_html)}'
                f'</div>'
            )
            # Find last </div> in wrap_block, insert before it
            last_close = new_wrap.rfind("</div>")
            if last_close >= 0:
                new_wrap = (
                    new_wrap[:last_close]
                    + caption_html
                    + new_wrap[last_close:]
                )
        details_block = (
            '<details class="code-collapsible">'
            '<summary>Show code</summary>'
            + new_wrap +
            '</details>'
        )
    else:
        # Bare <pre>: wrap it in code-block-wrapper plus details
        caption_html = (
            f'<div class="code-caption">'
            f'{generate_caption(library_name, code_html_inside_pre, fragment_label, intro_text)}'
            f'</div>'
        )
        wrapper_block = (
            '<div class="code-block-wrapper">'
            + body_html[pre_start:pre_end] +
            caption_html +
            '</div>'
        )
        details_block = (
            '<details class="code-collapsible">'
            '<summary>Show code</summary>'
            + wrapper_block +
            '</details>'
        )

    # Substitute the wrap span with the details_block.
    new_body = body_html[:wrap_start] + details_block + body_html[wrap_end:]
    return new_body, 1


def transform_html(html: str, section_prefix: str) -> tuple[str, int]:
    """Transform all library-shortcut callouts in this HTML.

    Returns (new_html, num_callouts_changed).

    Strategy:
     - Forward pass: scan all callouts, assign fragment numbers only to those
       that will need a NEW caption (so existing captions are preserved and
       new numbers stay in document order).
     - Reverse pass: apply edits so earlier offsets remain valid.
    """
    used = existing_fragment_numbers(html, section_prefix)

    # Forward pass: collect callout spans + assign numbers.
    plan = []  # list of (body_start, body_end, fragment_int_or_None)
    matches = list(CALLOUT_OPEN_RE.finditer(html))
    for m in matches:
        body_start = m.end()
        body_end = find_div_close(html, body_start)
        if body_end < 0:
            continue
        body = html[body_start:body_end]
        if already_collapsed(body):
            continue
        if not PRE_RE.search(body):
            # Skip callouts without code; not our problem.
            continue
        # Determine if a NEW caption will be required: scan the same span we
        # plan to wrap (largest enclosing code-block-wrapper around the first
        # <pre>), and check whether it already contains a code-caption.
        # If so, we don't need to reserve a fragment number.
        needs_new_caption = _scan_needs_new_caption(body)
        if needs_new_caption:
            n = next_fragment_int(used)
            used.add(n)
        else:
            n = None
        plan.append((body_start, body_end, n))

    # Reverse pass: apply edits.
    changes = 0
    for body_start, body_end, fragment_int in reversed(plan):
        body = html[body_start:body_end]
        new_body, k = transform_callout_body(body, section_prefix, fragment_int)
        if k > 0:
            html = html[:body_start] + new_body + html[body_end:]
            changes += k
    return html, changes


def _scan_needs_new_caption(body_html: str) -> bool:
    """Quick scan: does this callout body need a NEW caption?

    Returns True if the first <pre>...</pre> isn't already adjacent to a
    code-caption inside its enclosing wrapper (or the callout body if no
    wrapper).
    """
    pre_m = PRE_RE.search(body_html)
    if not pre_m:
        return False
    pre_start, pre_end = pre_m.span()
    # Find an enclosing code-block-wrapper.
    for cbw_m in CBW_OPEN_RE.finditer(body_html):
        if cbw_m.start() < pre_start:
            cbw_close = find_div_close(body_html, cbw_m.end())
            if cbw_close >= pre_end:
                wrap_start = cbw_m.start()
                wrap_end = cbw_close + len("</div>")
                return 'code-caption' not in body_html[wrap_start:wrap_end]
    # No wrapper: certainly needs a caption.
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write changes")
    ap.add_argument("--root", default=str(PROJECT_ROOT), help="Book root")
    ap.add_argument("--limit", type=int, default=None, help="Limit number of files (debug)")
    args = ap.parse_args()

    root = Path(args.root)
    files = sorted(
        f for f in root.rglob("part-*/module-*/section-*.html")
        if not is_excluded(f)
    )

    total_files_touched = 0
    total_callouts_changed = 0
    files_processed = 0

    for f in files:
        if args.limit and files_processed >= args.limit:
            break
        files_processed += 1
        html = f.read_text(encoding="utf-8", errors="replace")
        if "callout library-shortcut" not in html:
            continue
        section_prefix = find_section_prefix(f)
        new_html, n = transform_html(html, section_prefix)
        if n > 0:
            total_callouts_changed += n
            total_files_touched += 1
            rel = f.relative_to(root)
            print(f"[{n:2d}] {rel}")
            if args.apply:
                f.write_text(new_html, encoding="utf-8")
    print()
    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"{mode}: {total_callouts_changed} callouts changed in {total_files_touched} files")


if __name__ == "__main__":
    main()
