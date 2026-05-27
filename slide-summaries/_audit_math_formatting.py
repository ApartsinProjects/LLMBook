"""Audit math + formatting issues across the book HTML.

Detects:
1. Files with $..$ or $$..$$ math but missing KaTeX <head> includes
2. Math inside <div class="diagram-caption">
3. Math inside <div class="code-caption">
4. Long math lines (>120 chars between $$..$$)
5. Math inside callout boxes
6. Bare/unmatched $ characters in prose
7. $..$ math accidentally inside <pre> or <code> tags
8. Unmatched braces in math
9. Plus a few non-math formatting heuristics
"""

from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Glob: all section-*.html across parts/modules + appendices
SECTION_GLOBS = [
    "part-*/module-*/section-*.html",
    "appendices/appendix-*/section-*.html",
]


def find_section_files() -> list[Path]:
    out: list[Path] = []
    for g in SECTION_GLOBS:
        out.extend(sorted(ROOT.glob(g)))
    return out


# Regexes
RE_KATEX_INCLUDE = re.compile(r"katex", re.IGNORECASE)
RE_DOLLAR_MATH = re.compile(r"\$\$[^$]+\$\$|(?<!\\)\$[^\s$][^$\n]*?[^\\\s]\$")
RE_DISPLAY_MATH = re.compile(r"\$\$([^$]+)\$\$", re.DOTALL)
RE_DIAGRAM_CAPTION = re.compile(
    r'<div class="diagram-caption"[^>]*>(.*?)</div>', re.DOTALL
)
RE_CODE_CAPTION = re.compile(
    r'<div class="code-caption"[^>]*>(.*?)</div>', re.DOTALL
)
RE_CALLOUT_BLOCK = re.compile(
    r'<div class="callout [^"]*"[^>]*>(.*?)(?=<div class="callout |</main>|</body>)', re.DOTALL
)
RE_PRE_BLOCK = re.compile(r"<pre[^>]*>(.*?)</pre>", re.DOTALL)


def has_math(text: str) -> bool:
    return bool(RE_DOLLAR_MATH.search(text))


def has_katex_include(head: str) -> bool:
    return "katex" in head.lower()


def find_unmatched_braces_in_math(text: str) -> list[str]:
    """Find $..$ or $$..$$ spans with unmatched { } braces."""
    bad: list[str] = []
    # display math
    for m in re.finditer(r"\$\$(.*?)\$\$", text, re.DOTALL):
        body = m.group(1)
        if body.count("{") != body.count("}"):
            bad.append(body.strip()[:120])
    # inline math (single-line)
    for m in re.finditer(r"(?<!\\)\$([^\n$]+?)(?<!\\)\$", text):
        body = m.group(1)
        # Skip prices like $50 to $200 (no LaTeX commands inside)
        if "\\" not in body and not re.search(r"[_^{}=]", body):
            continue
        if body.count("{") != body.count("}"):
            bad.append(body.strip()[:120])
    return bad


def find_bare_dollars(text: str) -> int:
    """Heuristic: count dollar signs that don't seem to belong to math.

    Skips HTML entities, escaped dollars, and dollar signs inside known math.
    """
    # Strip <pre>/<code>, math, and HTML entities first.
    cleaned = re.sub(r"<pre.*?</pre>", "", text, flags=re.DOTALL)
    cleaned = re.sub(r"<code[^>]*>.*?</code>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\$\$.*?\$\$", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"(?<!\\)\$[^\n$]+?(?<!\\)\$", "", cleaned)
    cleaned = re.sub(r"&#36;|&dollar;", "", cleaned)
    cleaned = cleaned.replace("\\$", "")
    return cleaned.count("$")


def find_long_math_lines(text: str, threshold: int = 120) -> list[tuple[int, int]]:
    """Return (line_number, length) of $$..$$ spans whose content exceeds threshold."""
    bad: list[tuple[int, int]] = []
    for m in re.finditer(r"\$\$([^$]+?)\$\$", text, re.DOTALL):
        body = m.group(1).strip()
        if len(body) > threshold:
            line = text.count("\n", 0, m.start()) + 1
            bad.append((line, len(body)))
    return bad


def find_math_in_div(text: str, div_re: re.Pattern) -> list[str]:
    bad: list[str] = []
    for m in div_re.finditer(text):
        inner = m.group(1)
        if has_math(inner):
            bad.append(inner.strip()[:200])
    return bad


def find_math_in_pre(text: str) -> list[str]:
    bad: list[str] = []
    for m in RE_PRE_BLOCK.finditer(text):
        inner = m.group(1)
        # A real $..$ pair inside non-Python comments
        if re.search(r"\$[A-Za-z_\\][^$\n]{0,40}\$", inner):
            # Skip likely shell variables or jinja
            if "\\" in inner or "_{" in inner or "^{" in inner:
                bad.append(inner.strip()[:120])
    return bad


def find_math_in_callouts(text: str) -> int:
    count = 0
    for m in re.finditer(
        r'<div class="callout [^"]+"[^>]*>(.*?)</div>\s*</div>', text, re.DOTALL
    ):
        inner = m.group(1)
        if has_math(inner):
            count += 1
    return count


# Non-math heuristics
RE_CODE_NO_LANG = re.compile(r'<pre[^>]*>\s*<code(?![^>]*class="language-)')
RE_FIGURE_NO_CAPTION = re.compile(r"<figure[^>]*>(?:(?!</figure>).)*?</figure>", re.DOTALL)


def find_code_blocks_without_language(text: str) -> int:
    return len(RE_CODE_NO_LANG.findall(text))


def find_figures_without_figcaption(text: str) -> int:
    bad = 0
    for m in RE_FIGURE_NO_CAPTION.finditer(text):
        block = m.group(0)
        if "<figcaption" not in block:
            bad += 1
    return bad


def audit_file(p: Path) -> dict:
    text = p.read_text(encoding="utf-8", errors="replace")
    head_match = re.search(r"<head>(.*?)</head>", text, re.DOTALL)
    head = head_match.group(1) if head_match else ""
    body_match = re.search(r"<body[^>]*>(.*)</body>", text, re.DOTALL)
    body = body_match.group(1) if body_match else text

    findings: dict = {}

    if has_math(body):
        if not has_katex_include(head):
            findings["missing_katex_include"] = True

    long_math = find_long_math_lines(body)
    if long_math:
        findings["long_math_lines"] = long_math

    math_diag = find_math_in_div(body, RE_DIAGRAM_CAPTION)
    if math_diag:
        findings["math_in_diagram_caption"] = math_diag

    math_codecap = find_math_in_div(body, RE_CODE_CAPTION)
    if math_codecap:
        findings["math_in_code_caption"] = math_codecap

    unmatched = find_unmatched_braces_in_math(body)
    if unmatched:
        findings["unmatched_braces"] = unmatched

    bare = find_bare_dollars(body)
    if bare:
        findings["bare_dollars"] = bare

    math_callouts = find_math_in_callouts(body)
    if math_callouts:
        findings["math_in_callouts"] = math_callouts

    math_pre = find_math_in_pre(body)
    if math_pre:
        findings["math_in_pre"] = math_pre

    code_nolang = find_code_blocks_without_language(body)
    if code_nolang:
        findings["code_without_language"] = code_nolang

    figs_nocap = find_figures_without_figcaption(body)
    if figs_nocap:
        findings["figures_without_figcaption"] = figs_nocap

    return findings


def main() -> None:
    files = find_section_files()
    report: dict = {"per_file": {}, "totals": {}}
    totals: dict = {}
    for p in files:
        f = audit_file(p)
        if f:
            rel = p.relative_to(ROOT).as_posix()
            report["per_file"][rel] = f
            for k, v in f.items():
                if isinstance(v, bool):
                    totals[k] = totals.get(k, 0) + 1
                elif isinstance(v, int):
                    totals[k] = totals.get(k, 0) + v
                else:
                    totals[k] = totals.get(k, 0) + len(v)
    report["totals"] = totals
    report["total_files_scanned"] = len(files)
    report["files_with_findings"] = len(report["per_file"])

    out = Path(__file__).resolve().parent / "_math_formatting_audit.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Scanned {len(files)} files, findings in {len(report['per_file'])} files.")
    print("Totals:")
    for k, v in sorted(totals.items()):
        print(f"  {k}: {v}")
    print(f"Report written to: {out}")


if __name__ == "__main__":
    main()
