"""Re-highlight code blocks that have `class="lang-XYZ"` but no
syntax-highlighted spans (i.e., never went through Pygments).

Root cause: code blocks authored with `<code class="lang-bash">...</code>`
or `<code class="lang-python">...</code>` get the language tag but the
Pygments highlighting step was skipped. Pygments CSS only paints content
when the `<code>` has class `pygments-highlighted` AND the body is split
into typed spans (e.g., `<span class="k">def</span>`). Without those,
the code renders as plain dark-mode monospace with no color coding.

Generalized fix: detect `<code class="lang-X">PLAIN_TEXT</code>` blocks
(no `<span>` inside, > 10 chars) and run Pygments over them. Replace
the inner content with the HTML-formatted tokens and add
`pygments-highlighted` to the class list.

Idempotent: blocks already containing `<span>` markup are left alone.

Supported languages: python, bash, yaml, json, javascript, typescript,
sql, rust, go, c, cpp.
"""
from __future__ import annotations
import argparse
import html as html_lib
import re
import sys
from pathlib import Path

from pygments import highlight
from pygments.lexers import (
    PythonLexer, BashLexer, YamlLexer, JsonLexer,
    JavascriptLexer, TypeScriptLexer, SqlLexer,
    RustLexer, GoLexer, CLexer, CppLexer, TextLexer,
)
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "styles", "vendor", "scripts",
              "docs"}

LANG_MAP = {
    "python": PythonLexer(),
    "py":     PythonLexer(),
    "bash":   BashLexer(),
    "sh":     BashLexer(),
    "shell":  BashLexer(),
    "yaml":   YamlLexer(),
    "yml":    YamlLexer(),
    "json":   JsonLexer(),
    "js":     JavascriptLexer(),
    "javascript": JavascriptLexer(),
    "ts":     TypeScriptLexer(),
    "typescript": TypeScriptLexer(),
    "sql":    SqlLexer(),
    "rust":   RustLexer(),
    "rs":     RustLexer(),
    "go":     GoLexer(),
    "c":      CLexer(),
    "cpp":    CppLexer(),
    "cc":     CppLexer(),
}

# Formatter that emits Pygments spans with no wrapping <div> / <pre>.
FORMATTER = HtmlFormatter(nowrap=True, noclasses=False)

# Match <code class="lang-X">BODY</code> where BODY has no <span> inside.
CODE_PAT = re.compile(
    r'<code class="lang-([a-zA-Z0-9_+\-]+)">((?:(?!</code>).)*?)</code>',
    re.DOTALL,
)


def highlight_block(lang: str, body: str) -> str:
    """Run Pygments. Body is HTML-escaped already (because it lived inside
    <code>...</code>), so we unescape first, then re-escape via Pygments."""
    lexer = LANG_MAP.get(lang.lower())
    if lexer is None:
        return None  # signal: unsupported
    raw = html_lib.unescape(body)
    out = highlight(raw, lexer, FORMATTER)
    # Pygments adds a trailing newline; strip it.
    return out.rstrip("\n")


def fix(p: Path, dry_run: bool) -> int:
    text = p.read_text(encoding="utf-8")
    orig = text
    count = 0
    edits: list[tuple[int, int, str]] = []
    for m in CODE_PAT.finditer(text):
        lang = m.group(1)
        body = m.group(2)
        # Skip if already spanned
        if "<span" in body:
            continue
        # Skip very short content
        if len(body.strip()) < 10:
            continue
        # Skip 'text' lang (intentionally plain)
        if lang.lower() == "text":
            continue
        new_body = highlight_block(lang, body)
        if new_body is None:
            continue  # unsupported language; leave alone
        # New code opening tag: <code class="pygments-highlighted lang-XYZ">
        new_open = f'<code class="pygments-highlighted lang-{lang}">'
        new_close = '</code>'
        replacement = new_open + new_body + new_close
        edits.append((m.start(), m.end(), replacement))
        count += 1
    # Apply right-to-left
    for start, end, repl in reversed(edits):
        text = text[:start] + repl + text[end:]
    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    files_edited = 0
    total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n = fix(p, dry_run)
        if n > 0:
            files_edited += 1
            total += n
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:    {files_edited}")
    print(f"Blocks rendered: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
