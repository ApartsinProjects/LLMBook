"""Wrap bare $...$ inline math with <span class="math">.

ROOT CAUSE
  The math pipeline (html2epub/src/html2epub/math_render.py) processes:
    - <span class="math">$...$</span>
    - <div class="math-block">$$...$$</div>
    - text nodes containing $$...$$, \\(...\\), \\[...\\]
  It does NOT process bare single-$ pairs in text nodes, because that
  pattern false-positives on prices (`$5 million`, `$100`).

  But authors mixed conventions. Sections like §3.8.3 contain text like:
    For an input token vector $x \\in \\mathbb{R}^{d_{\\text{model}}}$
    and a router weight matrix $W_g \\in \\mathbb{R}^{...}$ ...
  These have unambiguous TeX content between the dollars and should be
  rendered. Currently they show as literal source text.

FIX
  Walk every <p>, <li>, <td>, <dd>, <figcaption> text node. Skip nodes
  inside <code>, <pre>, <script>, <style>, or <span class="math">. For
  each remaining text node, find unambiguous `$<tex>$` pairs and wrap
  with <span class="math">$<tex>$</span>.

UNAMBIGUOUS PATTERN (to avoid price false-positives)
  - The `$<tex>$` content must contain at least one TeX-flavored char:
    a backslash (`\\`), a math operator (`^`, `_`, `=`, `+`, `\\cdot`, `\\in`),
    or curly braces `{}`.
  - Pure numeric content like `$5$` is left alone (could be price).
  - The opening `$` must be preceded by whitespace, start-of-string, or
    a non-word char (parentheses, comma). The closing `$` must be
    followed by whitespace, punctuation, or end-of-string.

Idempotent.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString  # type: ignore

ROOT = Path(__file__).resolve().parent.parent.parent

# Match $<tex>$ where:
# - opener is at start or after whitespace / punctuation (NOT after \w or $)
# - content contains at least one TeX-y char (backslash, ^, _, {, }, \in, etc.)
# - closer is followed by end or whitespace/punctuation (NOT \w or $)
# Content cannot contain $ or newline.
BARE_DOLLAR_RE = re.compile(
    r'(?<![\w$])'                          # boundary before opener
    r'\$'                                   # opening $
    r'(?P<tex>(?=[^$\n]*?[\\^_{}=])'        # lookahead: must have TeX-y char
    r'[^$\n]+?)'                            # the tex content
    r'\$'                                   # closing $
    r'(?![\w$])'                            # boundary after closer
)

SKIP_TAGS = {"code", "pre", "script", "style"}
PROCESS_TAGS = ("p", "li", "td", "th", "dd", "figcaption", "div")


def in_skip_ancestor(node) -> bool:
    """True if node has an ancestor that should not be touched."""
    for anc in node.parents:
        if anc.name in SKIP_TAGS:
            return True
        cls = anc.get("class") if anc.name else None
        if cls and ("math" in cls or "math-block" in cls):
            return True
    return False


def process_text_node(text: str) -> tuple[str, int]:
    """Wrap bare $TeX$ in <span class="math">$TeX$</span>. Returns (new_text, n)."""
    n = 0
    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        tex = m.group("tex")
        return f'<span class="math">${tex}$</span>'
    new_text = BARE_DOLLAR_RE.sub(repl, text)
    return new_text, n


def patch_file(path: Path) -> tuple[int, int]:
    """Return (n_wrapped, n_paragraphs_touched)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    total_wrapped = 0
    n_paragraphs = 0
    for tag in soup.find_all(PROCESS_TAGS):
        # Skip if tag itself is inside a skip ancestor
        if in_skip_ancestor(tag):
            continue
        # Walk direct text-node children (BeautifulSoup .strings would
        # descend into <code> etc. — use find_all(string=True) with skip
        # ancestor check)
        for txt_node in list(tag.find_all(string=True, recursive=True)):
            parent = txt_node.parent
            if parent is None or in_skip_ancestor(txt_node):
                continue
            s = str(txt_node)
            if "$" not in s:
                continue
            new_s, n = process_text_node(s)
            if n:
                # Replace text node with a sequence (text + tag + text + ...)
                # by re-parsing the substring as HTML fragment and splicing.
                fragment = BeautifulSoup(new_s, "html.parser")
                children = list(fragment.children)
                # Insert new children before the text node, then remove it
                for child in children:
                    txt_node.insert_before(child)
                txt_node.extract()
                total_wrapped += n
                n_paragraphs += 1
    if total_wrapped:
        # Preserve doctype + html-prefix via str(soup); but BS html.parser
        # may not preserve everything perfectly. We use the soup's str and
        # write atomically.
        path.write_text(str(soup), encoding="utf-8")
    return total_wrapped, n_paragraphs


def main() -> int:
    skip_dirs = {"KDP", "node_modules", ".git", "source_fix_backups", "_archive"}
    total_files = 0
    total_modified = 0
    total_wrapped = 0
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if any(part in skip_dirs for part in rel.parts):
            continue
        total_files += 1
        try:
            n_wrapped, n_paragraphs = patch_file(path)
        except Exception as e:
            print(f"ERR {rel}: {e}", file=sys.stderr)
            continue
        if n_wrapped:
            total_modified += 1
            total_wrapped += n_wrapped
            print(f"  {n_wrapped:4d} wraps in {n_paragraphs:3d} paragraphs: {rel}")
    print()
    print(f"Files scanned:  {total_files}")
    print(f"Files modified: {total_modified}")
    print(f"Total wraps:    {total_wrapped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
