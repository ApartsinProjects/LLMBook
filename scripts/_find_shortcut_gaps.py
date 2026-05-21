"""Quick scan: list every Python code-block-wrapper that matches one of the 5
target hand-rolled patterns (cosine_similarity, retry, chunker, attention,
semantic_cache) AND has no library-shortcut sibling within 8 elements.

READ-ONLY. Used to drive `_add_library_shortcuts.py`.
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

EXCLUDE = {"KDP", "node_modules", ".git", "temp_ebook", "temp_epub",
           "source_fix_backups", "pagefind", "templates", ".claude",
           ".book-update", "vendor", "scripts", "docs", "styles", "build"}


def is_excluded(p: Path) -> bool:
    return any(part in EXCLUDE or part.startswith("temp_")
               for part in p.relative_to(PROJECT_ROOT).parts)


def neighbor_has_library_shortcut(wrapper, lookahead: int = 8) -> bool:
    sib = wrapper
    for _ in range(lookahead):
        sib = sib.find_next_sibling()
        if sib is None:
            break
        if hasattr(sib, "get"):
            cls = sib.get("class") or []
            if "callout" in cls and "library-shortcut" in cls:
                return True
            if sib.name in {"h1", "h2", "h3", "h4"}:
                break
    prev = wrapper.find_previous_sibling()
    if prev is not None and hasattr(prev, "get"):
        cls = prev.get("class") or []
        if "callout" in cls and "library-shortcut" in cls:
            return True
    return False


def classify(src: str) -> str | None:
    # Cosine similarity (hand-rolled, not sklearn import)
    if re.search(r"def\s+\w*[Cc]os(?:ine)?_?[Ss]im\w*\(", src) or \
       re.search(r"np\.dot\([^)]+?\)\s*/\s*\(\s*np\.linalg\.norm", src):
        if not re.search(r"from\s+sklearn\.metrics\.pairwise\s+import\s+cosine_similarity", src):
            return "cosine"
    # Retry / backoff (try + sleep inside loop, no tenacity)
    if re.search(r"for\s+attempt\s+in\s+range\(", src) and \
       re.search(r"\bexcept\b", src) and \
       re.search(r"time\.sleep\b|asyncio\.sleep\(", src) and \
       not re.search(r"\b(?:import|from)\s+tenacity\b", src):
        return "retry"
    # Hand-rolled text chunker
    if re.search(r"def\s+\w*chunk\w*\(.*?text", src, re.DOTALL) and \
       re.search(r"\bchunk_size\b|\bchunk_overlap\b|\boverlap\b", src) and \
       not re.search(r"from\s+langchain", src) and \
       not re.search(r"from\s+llama_index", src):
        return "chunker"
    # Attention from scratch
    if re.search(r"\bq\s*@\s*k\.(T|transpose)", src) and \
       re.search(r"softmax", src) and \
       re.search(r"math\.sqrt|head_dim|d_?k\b", src) and \
       not re.search(r"scaled_dot_product_attention", src):
        return "attention"
    # Semantic cache hand-rolled
    if re.search(r"class\s+\w*[Ss]emantic[Cc]ache\b|def\s+\w*[Ss]emantic[Cc]ache\b", src) and \
       not re.search(r"\bgptcache\b|langchain_community", src):
        return "semantic_cache"
    return None


def main() -> int:
    cases = []
    for p in sorted(PROJECT_ROOT.glob("part-*/**/*.html")):
        if is_excluded(p):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(text, "html.parser")
        for wrapper in soup.find_all("div", class_="code-block-wrapper"):
            code = wrapper.find("code")
            if code is None:
                continue
            cls = code.get("class") or []
            if not any("lang-python" in c for c in cls):
                continue
            src = code.get_text()
            n_lines = src.count("\n")
            if n_lines < 15:
                continue
            kind = classify(src)
            if kind is None:
                continue
            if neighbor_has_library_shortcut(wrapper):
                continue
            cap = wrapper.find("div", class_="code-caption")
            cap_text = cap.get_text(" ", strip=True) if cap else ""
            cases.append((str(p.relative_to(PROJECT_ROOT)), kind, n_lines, cap_text[:90]))

    for path, kind, n, cap in cases:
        print(f"  [{kind:>14}] lines={n:>3} | {path}")
        if cap:
            print(f"                   {cap}")
    print()
    print(f"Total gaps: {len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
