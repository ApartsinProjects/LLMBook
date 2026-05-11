"""v5.1: Final front matter audit fixes - update stale chapter/appendix
counts and strip references to deleted frameworks/modules.

  1. Update '38 chapters / 39 sections' -> '33 chapters' (current count)
  2. Update '22 appendices (A through V)' -> '17 appendices (A through V
     plus K, L for HuggingFace and LangChain)' (M-Q were dropped in v3.1)
  3. Strip 'LangGraph, CrewAI, LlamaIndex, Semantic Kernel, DSPy' from
     framework lists - keep just LangChain and HuggingFace where mentioned
     as appendices
  4. Strip 'Module 35-equivalent governance content' in pathways
  5. section-fm.8 Problem-Solution Key: unwrap any links to deleted
     framework appendices, keep the framework names as plain text
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def safe_read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    n_files = 0
    n_fixes = 0

    fixes_per_file = {
        "front-matter/about-book.html": [
            (r'(numbered 0 through 38) in 11 parts, plus 22 appendices \(A through V\)',
             '33 chapters in 11 parts, plus 17 reference appendices'),
        ],
        "front-matter/foreword.html": [
            (r'framework cheat sheets \(LangChain, LangGraph, CrewAI, LlamaIndex, DSPy, Semantic Kernel\)',
             'framework cheat sheets (HuggingFace and LangChain)'),
            (r'\bThe 22 appendices\b', 'The reference appendices'),
        ],
        "front-matter/look-inside-preview.html": [
            (r'\bwhat\'s in the 39 chapters and 22 appendices\b',
             'what\'s in the 33 chapters and 17 reference appendices'),
            (r'\b39 chapters\b', '33 chapters'),
        ],
        "front-matter/pathways/index.html": [
            # Drop the now-broken Module 35-equivalent governance hint
            (r',\s*Module 35-equivalent governance content', ''),
        ],
        "front-matter/section-fm.1a.html": [
            (r'\(HuggingFace, LangChain, LangGraph, CrewAI, LlamaIndex, Semantic Kernel, DSPy\)',
             '(HuggingFace and LangChain)'),
            (r'39 sections \(numbered 0 through 38\) organized into eleven parts',
             '33 chapters organized into eleven parts'),
            (r'plus 22 appendices covering frameworks, tools, and reference material',
             'plus 17 reference appendices'),
            (r'In addition, 22 appendices \(A through V\) provide reference material and framework deep-dives',
             'In addition, 17 reference appendices provide background material and framework deep-dives (HuggingFace and LangChain)'),
        ],
    }

    for rel, fixes in fixes_per_file.items():
        p = ROOT / rel
        if not p.exists(): continue
        text = safe_read(p)
        original = text
        local = 0
        for old_pat, new_text in fixes:
            text, n = re.subn(old_pat, new_text, text)
            local += n
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += local
            print(f"  {rel.rsplit('/', 1)[-1]}: {local} fixes")

    # section-fm.8 Problem-Solution Key: unwrap broken framework appendix links.
    # Keep the framework name as plain text.
    fm8 = ROOT / "front-matter/section-fm.8.html"
    if fm8.exists():
        text = safe_read(fm8)
        original = text
        # Strip <a href=...appendix-m/n/o/p/q...>NAME</a> -> NAME
        for app in ["appendix-m-langgraph", "appendix-n-crewai", "appendix-o-llamaindex",
                    "appendix-p-semantic-kernel", "appendix-q-dspy"]:
            pat = re.compile(
                rf'<a\s+[^>]*href="[^"]*{re.escape(app)}[^"]*"[^>]*>(.*?)</a>',
                re.DOTALL,
            )
            text, n = pat.subn(r'\1', text)
            if n: print(f"  fm.8: unwrapped {n} links to {app}")
        if text != original:
            fm8.write_text(text, encoding="utf-8")
            n_files += 1

    print(f"\nTotal: {n_fixes} fixes across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
