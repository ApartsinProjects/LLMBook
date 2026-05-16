"""Zero out the remaining P1 broken-href cases via mapping table.

Patterns spotted in current html-integrity-audit.md:

1. module-38-agent-safety-security cross-refs in wrong part:
   part-6-agentic-ai/module-38-agent-safety-security
   -> part-9-safety-security-ethics/module-38-agent-safety-security

2. module-38 section refs with legacy 25.X numbering:
   section-25.1.html / 25.2 / 25.3 / 25.4 -> section-38.1 / 38.2 / 38.3 / 38.4

3. module-61 section-33.X.html refs (legacy file names migrated to 61.X):
   section-33.1 -> section-61.1
   section-33.2 -> section-61.2
   section-33.3 -> section-61.3
   section-33.10 -> stripped (no equivalent)

4. module-23-rag-fundamentals -> module-23-rag (slug shortened)

5. module-48-shipping-scaling -> module-48-shipping-deploying (slug fixed)

6. front-matter//appendices/ (double slash) -> ../appendices/

7. part-9-llm-applications/module-50-coding-with-llms -> strip <a>
   (no clean target; vibe-coding moved to module-43)

8. module-42-strategy-prioritization/section-31.X.html -> section-42.X.html

9. section-62.5/.6/.7 (don't exist) -> strip <a> wrapper

10. module-26-agents -> module-26-ai-agents (slug renamed)

11. appendix-g-python-for-llm -> appendix-g-python-for-llm IS correct after v11.
    But if older links reference appendix-h-python-for-llm (pre-v11), redirect.

Idempotent.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}

# Pattern -> replacement. Order matters; do more-specific first.
REPLACEMENTS = [
    # Module 38 in wrong part (must come BEFORE section-25 numbering fix
    # so the path is canonical when section-25 -> section-38 runs)
    ("part-6-agentic-ai/module-38-agent-safety-security",
     "part-9-safety-security-ethics/module-38-agent-safety-security"),

    # Module 38 section renumbering (legacy 25.X)
    ("module-38-agent-safety-security/section-25.1.html",
     "module-38-agent-safety-security/section-38.1.html"),
    ("module-38-agent-safety-security/section-25.2.html",
     "module-38-agent-safety-security/section-38.2.html"),
    ("module-38-agent-safety-security/section-25.3.html",
     "module-38-agent-safety-security/section-38.3.html"),
    ("module-38-agent-safety-security/section-25.4.html",
     "module-38-agent-safety-security/section-38.4.html"),
    ("module-38-agent-safety-security/section-25.5.html",
     "module-38-agent-safety-security/section-38.5.html"),

    # Module 61 legacy section-33.X.html (mapping by numerical order)
    ("module-61-frontier-architectures/section-33.1.html",
     "module-61-frontier-architectures/section-61.1.html"),
    ("module-61-frontier-architectures/section-33.2.html",
     "module-61-frontier-architectures/section-61.2.html"),
    ("module-61-frontier-architectures/section-33.3.html",
     "module-61-frontier-architectures/section-61.3.html"),

    # Module 23 RAG slug
    ("module-23-rag-fundamentals", "module-23-rag"),

    # Module 48 shipping slug
    ("module-48-shipping-scaling", "module-48-shipping-deploying"),

    # Module 26 agents slug (older form -> ai-agents)
    ("module-26-agents/", "module-26-ai-agents/"),

    # Module 42 strategy: section-31.X (legacy) -> section-42.X
    ("module-42-strategy-prioritization/section-31.1.html",
     "module-42-strategy-prioritization/section-42.1.html"),
    ("module-42-strategy-prioritization/section-31.2.html",
     "module-42-strategy-prioritization/section-42.2.html"),
    ("module-42-strategy-prioritization/section-31.3.html",
     "module-42-strategy-prioritization/section-42.3.html"),
    ("module-42-strategy-prioritization/section-31.4.html",
     "module-42-strategy-prioritization/section-42.4.html"),

    # Front-matter double-slash typo
    ("front-matter//appendices/", "front-matter/../appendices/"),

    # v11 cascade: any leftover appendix-h-python-for-llm -> appendix-g
    ("appendix-h-python-for-llm", "appendix-g-python-for-llm"),
]

# Slugs to STRIP: <a> wrapper goes away, inner text remains.
STRIP_SLUGS = [
    "part-9-llm-applications/module-50-coding-with-llms",
    "module-62-frontier-theory/section-62.5.html",
    "module-62-frontier-theory/section-62.6.html",
    "module-62-frontier-theory/section-62.7.html",
]


def fix(p: Path, dry_run: bool) -> dict:
    text = p.read_text(encoding="utf-8")
    orig = text
    c = {"replace": 0, "strip": 0}
    for old, new in REPLACEMENTS:
        if old in text:
            c["replace"] += text.count(old)
            text = text.replace(old, new)
    for dead in STRIP_SLUGS:
        pattern = (rf'<a[^>]*href="[^"]*{re.escape(dead)}[^"]*"[^>]*>'
                    rf'([^<]*)</a>')
        text, n = re.subn(pattern, r"\1", text)
        c["strip"] += n
    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    totals = {"replace": 0, "strip": 0}
    files_edited = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        ch = fix(p, dry_run)
        if any(ch.values()):
            files_edited += 1
            for k in totals:
                totals[k] += ch[k]

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:      {files_edited}")
    print(f"Slug replacements: {totals['replace']}")
    print(f"Dead-link strips:  {totals['strip']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
