"""Read-only audit for broken template headers across the book.

Finds:
  A. Appendix section files whose h1 starts with '^' (or other placeholder
     chars) instead of a real letter (A/B/C/.../V).
  B. Part-12 chapter landings whose h2 section anchors are bare text with
     placeholder prefixes like '^.1', '_.1', or '?.1' instead of properly
     wrapped <h2 id="..."> tags.
  C. Whole-book chapter landings whose h1 is missing, empty, numeric-only,
     or starts with a placeholder character.

The canonical template (from _normalize_page_headers.py):
    <header class="chapter-header">
      <nav class="header-nav">...</nav>
      <div class="header-search">...</div>
      <div class="page-breadcrumb">[Part X: ...] [Chapter N]</div>
      <h1>Chapter Title</h1>
      <p class="chapter-subtitle">...</p> (optional)

Skips KDP/, .claude/, node_modules/, build/, temp_*.

Usage: /c/Python314/python scripts/_audit_header_breakage.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    "KDP", ".claude", "node_modules", "build", "pagefind",
    "source_fix_backups", ".git", "__pycache__", "audit",
    "_exercise_payloads",
}

# Things that look like an unfilled placeholder for a letter or number.
PLACEHOLDER_CHARS = {"^", "_", "?", "{", "}", "$", "X", "N"}


def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    if parts & SKIP_DIRS:
        return True
    for part in p.parts:
        if part.startswith("temp_"):
            return True
    return False


def get_h1_text(soup: BeautifulSoup) -> str | None:
    h1 = soup.find("h1")
    if not h1:
        return None
    return h1.get_text(strip=True)


def starts_with_placeholder(text: str) -> bool:
    """A real heading starts with a letter or digit; placeholders start with
    a non-alphanumeric punctuation character that obviously was meant to be
    substituted out (e.g. '^.1', '_.1', '?.1', '{LETTER}.1')."""
    if not text:
        return False
    first = text[0]
    if first.isalnum():
        return False
    return first in PLACEHOLDER_CHARS


def audit_appendix_sections() -> list[dict]:
    """Find appendix section files with h1 starting with a placeholder."""
    findings = []
    apx_root = ROOT / "appendices"
    if not apx_root.exists():
        return findings
    for path in sorted(apx_root.rglob("section-*.html")):
        if should_skip(path):
            continue
        try:
            soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        except Exception as e:
            findings.append({"file": path, "issue": f"read-failure: {e}"})
            continue
        h1 = get_h1_text(soup)
        if h1 is None:
            findings.append({"file": path, "issue": "missing-h1"})
            continue
        if starts_with_placeholder(h1):
            findings.append({"file": path, "issue": f"placeholder-h1", "h1": h1[:80]})
        elif not h1:
            findings.append({"file": path, "issue": "empty-h1"})
    return findings


def audit_part12_landings() -> list[dict]:
    """Part-12 chapter landings: check both h1 validity AND the section-anchor
    h2s. The breakage we're chasing is bare text like '^.1 Use Cases...' or
    '_.1 Use Cases...' that should have been '<h2 id="36.1">36.1 ...</h2>'."""
    findings = []
    p12 = ROOT / "part-12-llm-applications-across-industries"
    if not p12.exists():
        return findings
    for mod_dir in sorted(p12.glob("module-*-*/")):
        landing = mod_dir / "index.html"
        if not landing.exists():
            continue
        if should_skip(landing):
            continue
        try:
            html_text = landing.read_text(encoding="utf-8")
        except Exception as e:
            findings.append({"file": landing, "issue": f"read-failure: {e}"})
            continue
        soup = BeautifulSoup(html_text, "html.parser")
        h1 = get_h1_text(soup)
        record: dict = {"file": landing}
        problems = []
        if h1 is None:
            problems.append("missing-h1")
        elif not h1:
            problems.append("empty-h1")
        elif starts_with_placeholder(h1):
            problems.append(f"placeholder-h1: {h1[:60]!r}")

        # Scan main content for bare-text section-anchor placeholders.
        # Pattern: a placeholder char then '.' then a digit (e.g. ^.1, _.2, ?.3).
        main = soup.find("main") or soup
        # We look at the *raw text* of main, line by line, because the breakage
        # is that the line never got wrapped in <h2>.
        bare_lines = []
        for line in main.get_text("\n").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            # Match e.g. ^.1, _.2, ?.3, $.1 followed by space + title text
            m = re.match(r"^([\^_\?\$\{\}])\.(\d+)\s+(.+)$", stripped)
            if m:
                bare_lines.append(stripped[:80])
        if bare_lines:
            problems.append(f"bare-text-section-headers: {len(bare_lines)} lines")
            record["bare_lines"] = bare_lines

        # Also check: does the page have at least one <h2> in main?
        h2s = main.find_all("h2") if hasattr(main, "find_all") else []
        h2_texts = [h.get_text(strip=True) for h in h2s]
        # If h1 looks fine but there are NO h2s and there ARE bare lines, that
        # strongly indicates the entire section-header level got dropped.
        if bare_lines and not h2_texts:
            problems.append("zero-h2-but-has-bare-section-text")

        # Check h2 texts for placeholder prefixes too.
        for h2t in h2_texts:
            if starts_with_placeholder(h2t):
                problems.append(f"placeholder-h2: {h2t[:60]!r}")

        if problems:
            record["problems"] = problems
            findings.append(record)
    return findings


def audit_all_chapter_landings() -> list[dict]:
    """Audit every chapter landing in the book (any part) for h1 anomalies."""
    findings = []
    for part_dir in sorted(ROOT.glob("part-*-*/")):
        if should_skip(part_dir):
            continue
        for mod_dir in sorted(part_dir.glob("module-*-*/")):
            landing = mod_dir / "index.html"
            if not landing.exists():
                continue
            if should_skip(landing):
                continue
            try:
                soup = BeautifulSoup(
                    landing.read_text(encoding="utf-8"), "html.parser"
                )
            except Exception as e:
                findings.append({"file": landing, "issue": f"read-failure: {e}"})
                continue
            h1 = get_h1_text(soup)
            if h1 is None:
                findings.append({"file": landing, "issue": "missing-h1"})
            elif not h1:
                findings.append({"file": landing, "issue": "empty-h1"})
            elif starts_with_placeholder(h1):
                findings.append(
                    {"file": landing, "issue": "placeholder-h1", "h1": h1[:80]}
                )
            elif re.fullmatch(r"[\d.\s]+", h1):
                findings.append(
                    {"file": landing, "issue": "numeric-only-h1", "h1": h1[:80]}
                )
    return findings


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def main() -> int:
    print("=" * 72)
    print("LLMBook Header Breakage Audit")
    print(f"Root: {ROOT}")
    print("=" * 72)

    print("\n--- A. Appendix sections with placeholder h1 -----------------------")
    apx = audit_appendix_sections()
    if not apx:
        print("  (clean)")
    for f in apx:
        line = f"  {rel(f['file'])}: {f['issue']}"
        if "h1" in f:
            line += f"  h1={f['h1']!r}"
        print(line)

    print("\n--- B. Part-12 chapter landings (template breakage) ----------------")
    p12 = audit_part12_landings()
    if not p12:
        print("  (clean)")
    for f in p12:
        print(f"  {rel(f['file'])}:")
        for prob in f.get("problems", []):
            print(f"      - {prob}")
        for bl in f.get("bare_lines", [])[:8]:
            print(f"        bare> {bl}")
        extra = len(f.get("bare_lines", [])) - 8
        if extra > 0:
            print(f"        bare> ...and {extra} more")

    print("\n--- C. All chapter landings (h1 anomalies, whole book) -------------")
    all_ch = audit_all_chapter_landings()
    if not all_ch:
        print("  (clean)")
    for f in all_ch:
        line = f"  {rel(f['file'])}: {f['issue']}"
        if "h1" in f:
            line += f"  h1={f['h1']!r}"
        print(line)

    print("\n=== Summary =========================================================")
    print(f"  Appendix sections with placeholder h1:    {len(apx)}")
    print(f"  Part-12 landings with template breakage:  {len(p12)}")
    print(f"  Chapter landings with h1 anomalies:       {len(all_ch)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
