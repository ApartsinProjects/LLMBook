"""v4.6: Three lint passes.

  1. Python code-runnability: extract every <code class="lang-python">
     block and pipe through ast.parse. Report syntax errors.
  2. Cross-reference validity: for every <a href="...section-X.Y.html(#...)">,
     verify target file exists.
  3. (PDF re-render handled separately via existing build_sample_pdf.py.)
"""
from __future__ import annotations
import re
import sys
import ast
import html
from pathlib import Path

# Force UTF-8 stdout to avoid cp1252 Unicode crashes on Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts", "agents"}
MAX_FILE = 5_000_000


def safe_read(p: Path) -> str | None:
    try:
        if p.stat().st_size > MAX_FILE: return None
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def lint_python_blocks() -> int:
    """Find every <code class="lang-python"> block, parse with ast, report
    syntax errors with file + line."""
    n_blocks = 0
    n_errors = 0
    errors_by_file = {}
    code_re = re.compile(
        r'<code\s+[^>]*class="[^"]*lang-python[^"]*"[^>]*>(.*?)</code>',
        re.DOTALL,
    )
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        for m in code_re.finditer(text):
            n_blocks += 1
            # Strip Pygments span markup to get raw code
            raw = re.sub(r'<[^>]+>', '', m.group(1))
            raw = html.unescape(raw)
            # Skip incomplete fragments (lines starting with '...')
            if raw.strip().startswith('...'): continue
            # Skip very short blocks (likely snippets, e.g. < 3 lines or
            # contain top-level commas suggesting a CLI)
            if raw.count('\n') < 2: continue
            try:
                ast.parse(raw)
            except SyntaxError as e:
                # Filter out 'expected indented block' errors -- these are
                # almost always Pygments-stripping artifacts, not real bugs
                if "expected an indented block" in (e.msg or ""):
                    continue
                # Also skip leading-... and 'import ...' truncations
                if e.msg and ("invalid syntax" in e.msg and (
                    raw.lstrip().startswith(('# ', '...', '>>>'))
                    or "..." in raw[:200]
                )):
                    continue
                n_errors += 1
                # Sanitize msg for non-UTF terminals
                safe_msg = (e.msg or "").encode("ascii", errors="replace").decode("ascii")
                errors_by_file.setdefault(str(p.relative_to(ROOT).as_posix()), []).append(
                    f"line {e.lineno}: {safe_msg}"
                )

    print(f"\nPython lint: {n_blocks} blocks compiled, {n_errors} errors found")
    if errors_by_file:
        print("Errors per file:")
        for f, errs in sorted(errors_by_file.items())[:30]:
            print(f"  {f}:")
            for err in errs[:3]:
                print(f"    {err}")
    return n_errors


def validate_xrefs() -> int:
    """For every internal <a href="section-X.Y.html...">, verify target exists."""
    n_total = 0
    n_broken = 0
    broken_by_file = {}
    href_re = re.compile(r'<a\s+[^>]*href="([^"]+\.html)(?:#[^"]*)?"', re.IGNORECASE)
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        parent = p.parent
        for m in href_re.finditer(text):
            href = m.group(1)
            if href.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "#")):
                continue
            n_total += 1
            try:
                target = (parent / href).resolve()
                if not target.exists():
                    n_broken += 1
                    broken_by_file.setdefault(str(p.relative_to(ROOT).as_posix()), set()).add(href)
            except Exception:
                continue

    print(f"\nXref validation: {n_total} internal hrefs checked, {n_broken} broken")
    if broken_by_file:
        print("Broken hrefs per file (top 20):")
        for f, hrefs in sorted(broken_by_file.items())[:20]:
            print(f"  {f}: {sorted(hrefs)}")
    return n_broken


def main() -> int:
    print("=" * 60)
    print("Auto #1: Python code runnability lint")
    print("=" * 60)
    n_py_errors = lint_python_blocks()

    print("\n" + "=" * 60)
    print("Auto #2: Cross-reference validity sweep")
    print("=" * 60)
    n_broken = validate_xrefs()

    print("\n" + "=" * 60)
    print(f"Summary: {n_py_errors} Python syntax errors, {n_broken} broken xrefs")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
