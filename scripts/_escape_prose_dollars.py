"""Escape bare `$<digit>` in HTML prose so KaTeX doesn't eat the surrounding
text as inline math.

Root cause: KaTeX auto-render is configured with `$...$` as an inline
delimiter (74 HTML files). Authoring prose like "save $50 ... cost $120"
makes KaTeX find an opening `$` at `$50`, scan forward for the next `$`,
hit `$120`, and treat the entire intermediate text as a math expression.
The math renderer then concatenates and italicizes everything between the
two dollar signs, breaking the visual layout.

Generalized fix: replace bare `$<digit>` with `\$<digit>` everywhere in
HTML body content. KaTeX treats `\$` as a literal dollar and skips it.

Safe-zone exclusions: don't touch text inside `<code>`, `<pre>`,
`<script>`, `<style>`, or any `$$...$$` / `\(...\)` math blocks.

Idempotent: re-runs are no-ops because the regex is anchored to a `$`
that is NOT preceded by a backslash.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "styles", "vendor", "scripts",
              "docs"}

# Match opening tag <tag ...> and capture tag name
TAG_OPEN = re.compile(r'<(code|pre|script|style)(\s[^>]*)?>', re.IGNORECASE)
# Math blocks $$...$$ and \(...\) and \[...\] are safe to leave alone
# We split on these and only process text segments outside them.
MATH_BLOCK = re.compile(r'\$\$.+?\$\$|\\\(.+?\\\)|\\\[.+?\\\]', re.DOTALL)

# Bare $<digit> not preceded by backslash
PROSE_DOLLAR = re.compile(r'(?<!\\)\$(?=\d)')


def split_safe_zones(html: str) -> list[tuple[str, bool]]:
    """Split HTML into (chunk, is_safe_to_edit) segments.

    `is_safe_to_edit=False` means inside <code>, <pre>, <script>, <style>
    or math blocks.
    """
    segments: list[tuple[str, bool]] = []
    pos = 0
    while pos < len(html):
        m = TAG_OPEN.search(html, pos)
        if not m:
            segments.append((html[pos:], True))
            break
        # Text before the tag is editable
        if m.start() > pos:
            segments.append((html[pos:m.start()], True))
        tag = m.group(1).lower()
        # Find matching close
        close_re = re.compile(rf'</{tag}\s*>', re.IGNORECASE)
        cm = close_re.search(html, m.end())
        if not cm:
            # Unclosed — bail, treat rest as non-editable
            segments.append((html[m.start():], False))
            break
        # Include the tag, body, and closing tag as a non-editable block
        segments.append((html[m.start():cm.end()], False))
        pos = cm.end()
    return segments


def escape_prose_dollars(html: str) -> tuple[str, int]:
    """Escape bare $<digit> in editable segments. Return (new_html, count)."""
    segments = split_safe_zones(html)
    total = 0
    out_parts: list[str] = []
    for chunk, editable in segments:
        if not editable:
            out_parts.append(chunk)
            continue
        # Within editable chunk, further split on math blocks so we don't
        # touch the $ inside $$...$$ or \(...\)
        pos = 0
        for mm in MATH_BLOCK.finditer(chunk):
            pre = chunk[pos:mm.start()]
            new_pre, n = PROSE_DOLLAR.subn(r'\\$', pre)
            out_parts.append(new_pre)
            out_parts.append(chunk[mm.start():mm.end()])
            total += n
            pos = mm.end()
        tail = chunk[pos:]
        new_tail, n = PROSE_DOLLAR.subn(r'\\$', tail)
        out_parts.append(new_tail)
        total += n
    return ''.join(out_parts), total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    files_edited = 0
    total_escapes = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        new_text, n = escape_prose_dollars(text)
        if n > 0:
            files_edited += 1
            total_escapes += n
            if not dry_run:
                p.write_text(new_text, encoding="utf-8")
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited: {files_edited}")
    print(f"$-escapes:    {total_escapes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
