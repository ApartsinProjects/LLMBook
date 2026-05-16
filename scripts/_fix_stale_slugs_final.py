"""Final stale-slug rewrite sweep. Catches the remaining 328 broken hrefs
from html-integrity-audit.md by mapping old slugs to current ones.

Based on actual current module / appendix / part directory names in the
repo (confirmed via filesystem walk) the recurring stale patterns are:

Part-level slug renames:
  part-3-using-llms             -> part-3-working-with-llms
  part-5-rag-context            -> part-5-retrieval-conversation
  part-5-rag-knowledge          -> part-5-retrieval-conversation

Module-level slug renames within their current parts:
  module-02-tokenization              -> module-02-tokenization-subword-models
  module-19-peft-lora-qlora           -> module-19-peft
  module-23-rag-architecture          -> module-23-rag
  module-23-rag-pipeline              -> module-23-rag
  module-33-emerging-architectures    -> module-61-frontier-architectures
  module-45-idea-to-product           -> module-45-prototype-to-production
  module-26-agents                    -> module-26-ai-agents
  module-31-multimodal-generation     -> module-31-multimodal

Appendix slug renames (older letters / older names):
  appendix-r-docker-containers  -> appendix-p-docker-containers
  appendix-d-model-cards        -> strip (no equivalent)
  appendix-k-datasets-benchmarks -> strip (no equivalent)
  appendix-k-hardware-compute   -> strip (no equivalent; hardware dropped)
  appendix-e-prompt-templates   -> appendix-d-langchain (closest analog)

Cross-part wrong-placement fixes (module exists, but referenced in wrong part):
  part-9-safety-security-ethics/module-42-strategy-prioritization
      -> part-10-idea-to-product/module-42-strategy-prioritization
  part-12-frontiers/module-33-emerging-architectures
      -> part-12-frontiers/module-61-frontier-architectures

Front matter cleanup:
  front-matter/index.html       -> front-matter/foreword.html (FM index deleted)

Idempotent. Run with --apply.
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

# Direct text replacements (must be processed in declared order to avoid
# partial-match interference)
REPLACEMENTS = [
    # Cross-part wrong placement (do FIRST so subsequent slug renames don't
    # interfere)
    ("part-9-safety-security-ethics/module-42-strategy-prioritization",
     "part-10-idea-to-product/module-42-strategy-prioritization"),
    ("part-12-frontiers/module-33-emerging-architectures",
     "part-12-frontiers/module-61-frontier-architectures"),
    # Part-level slug renames
    ("part-3-using-llms", "part-3-working-with-llms"),
    ("part-5-rag-context", "part-5-retrieval-conversation"),
    ("part-5-rag-knowledge", "part-5-retrieval-conversation"),
    # Module-level slug renames (after part-level so paths are stable)
    ("module-02-tokenization/", "module-02-tokenization-subword-models/"),
    ("module-19-peft-lora-qlora", "module-19-peft"),
    ("module-23-rag-architecture", "module-23-rag"),
    ("module-23-rag-pipeline", "module-23-rag"),
    ("module-33-emerging-architectures", "module-61-frontier-architectures"),
    ("module-45-idea-to-product", "module-45-prototype-to-production"),
    ("module-26-agents/", "module-26-ai-agents/"),
    ("module-31-multimodal-generation", "module-31-multimodal"),
    # Appendix renames
    ("appendix-r-docker-containers", "appendix-p-docker-containers"),
    ("appendix-e-prompt-templates", "appendix-d-langchain"),
    # FM index deleted -> redirect to foreword
    ("front-matter/index.html", "front-matter/foreword.html"),
]

# Slugs to STRIP (no equivalent; replace <a>...</a> with plain text)
DEAD_SLUGS = [
    "appendix-d-model-cards",
    "appendix-k-datasets-benchmarks",
    "appendix-k-hardware-compute",
]


def fix(p: Path, dry_run: bool) -> dict:
    text = p.read_text(encoding="utf-8")
    orig = text
    counts = {"replace": 0, "strip": 0}
    for old, new in REPLACEMENTS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            counts["replace"] += n
    for dead in DEAD_SLUGS:
        # Strip <a> wrappers pointing at dead slugs; keep inner text
        pattern = (rf'<a[^>]*href="[^"]*{re.escape(dead)}[^"]*"[^>]*>'
                    rf'([^<]*)</a>')
        new_text, n = re.subn(pattern, r"\1", text)
        if n:
            counts["strip"] += n
            text = new_text
    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return counts


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
        c = fix(p, dry_run)
        if any(c.values()):
            files_edited += 1
            totals["replace"] += c["replace"]
            totals["strip"] += c["strip"]

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:        {files_edited}")
    print(f"Slug replacements:   {totals['replace']}")
    print(f"Dead-link strips:    {totals['strip']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
