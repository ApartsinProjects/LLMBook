#!/usr/bin/env python3
"""Remove unused KaTeX and Prism vendor includes from HTML files.

Walks all .html files in the project (excluding .git, node_modules,
__pycache__, templates, agents) and strips KaTeX or Prism script/link
tags from pages that do not actually use those libraries.
"""

import os
import re
import sys

ROOT = r"E:\Projects\LLMCourse"
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", "templates", "agents"}

# ---------------------------------------------------------------------------
# Detection patterns
# ---------------------------------------------------------------------------

# Math indicators (look in the <body> only, not in the <head> vendor lines)
MATH_PATTERNS = [
    re.compile(r'\$\$'),                          # display math $$...$$
    re.compile(r'(?<!\w)\$(?!\s).*?\S\$(?!\w)'),  # inline $...$
    re.compile(r'\\[(\[]'),                        # \( or \[
    re.compile(r'class\s*=\s*["\'][^"\']*\bmath\b'),
    re.compile(r'class\s*=\s*["\'][^"\']*\bkatex\b'),
    re.compile(r'<math[\s>]'),                     # MathML
]

# Code / Prism indicators (look in <body>)
CODE_PATTERNS = [
    re.compile(r'<pre[^>]*>\s*<code'),
    re.compile(r'<code\s+class\s*=\s*["\']language-'),
    re.compile(r'class\s*=\s*["\'][^"\']*\btoken\b'),
    re.compile(r'class\s*=\s*["\'][^"\']*\bline-numbers\b'),
    re.compile(r'data-lang\s*='),
]

# ---------------------------------------------------------------------------
# Tag removal patterns (applied to the full file text)
# ---------------------------------------------------------------------------

# KaTeX link and script tags (multi-line safe)
KATEX_TAG_RE = re.compile(
    r'[ \t]*<(?:link|script)[^>]*(?:katex|auto-render)[^>]*(?:/>|>(?:.*?</script>)?)\s*\n?',
    re.DOTALL | re.IGNORECASE,
)

# Prism link and script tags
PRISM_TAG_RE = re.compile(
    r'[ \t]*<(?:link|script)[^>]*(?:prism)[^>]*(?:/>|>(?:.*?</script>)?)\s*\n?',
    re.DOTALL | re.IGNORECASE,
)


def has_math(body: str) -> bool:
    for pat in MATH_PATTERNS:
        if pat.search(body):
            return True
    return False


def has_code(body: str) -> bool:
    for pat in CODE_PATTERNS:
        if pat.search(body):
            return True
    return False


def loads_katex(text: str) -> bool:
    return bool(re.search(r'(?:katex\.min\.css|katex\.min\.js|auto-render)', text, re.IGNORECASE))


def loads_prism(text: str) -> bool:
    return bool(re.search(r'(?:prism-theme\.css|prism\.css|prism\.min\.js|prism-bundle|prism-python)', text, re.IGNORECASE))


def extract_body(html: str) -> str:
    """Return the portion of the HTML after <body...> if present, else the whole thing."""
    m = re.search(r'<body[^>]*>', html, re.IGNORECASE)
    if m:
        return html[m.end():]
    return html


def process_file(filepath: str) -> dict:
    """Process one HTML file. Returns dict with keys: katex_removed, prism_removed."""
    result = {"katex_removed": False, "prism_removed": False}

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        original = f.read()

    if not loads_katex(original) and not loads_prism(original):
        return result  # nothing to do

    body = extract_body(original)
    text = original

    # Check KaTeX
    if loads_katex(original) and not has_math(body):
        text = KATEX_TAG_RE.sub("", text)
        result["katex_removed"] = True

    # Check Prism
    if loads_prism(original) and not has_code(body):
        text = PRISM_TAG_RE.sub("", text)
        result["prism_removed"] = True

    if text != original:
        # Clean up any resulting blank lines in <head> (collapse 3+ newlines to 2)
        text = re.sub(r'\n{3,}', '\n\n', text)
        with open(filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    return result


def main():
    katex_files = []
    prism_files = []
    total_scanned = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Prune excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for fname in filenames:
            if not fname.endswith(".html"):
                continue
            filepath = os.path.join(dirpath, fname)
            total_scanned += 1
            result = process_file(filepath)
            if result["katex_removed"]:
                katex_files.append(os.path.relpath(filepath, ROOT))
            if result["prism_removed"]:
                prism_files.append(os.path.relpath(filepath, ROOT))

    print(f"Scanned {total_scanned} HTML files.\n")

    if katex_files:
        print(f"KaTeX removed from {len(katex_files)} files:")
        for f in sorted(katex_files):
            print(f"  {f}")
    else:
        print("KaTeX: no unnecessary includes found.")

    print()

    if prism_files:
        print(f"Prism removed from {len(prism_files)} files:")
        for f in sorted(prism_files):
            print(f"  {f}")
    else:
        print("Prism: no unnecessary includes found.")

    print(f"\nTotal: {len(katex_files)} KaTeX removals, {len(prism_files)} Prism removals.")


if __name__ == "__main__":
    main()
