"""Step 3: Slim evaluation chapters from 13 to 5 sections.

Keeps:
  29.1  LLM Evaluation Fundamentals
  29.6  Evaluation-Driven Quality Gates
  29.10 LLM-as-Judge
  22.5  Agent Evaluation & Benchmarks
  33.4  LLM Vendor Evaluation & Build vs. Buy

Deletes (with inbound-link rewrites to nearest survivor):
  13.3  LLM-as-Simulator & Evaluation Generation     -> 29.1
  21.7  Human-AI Interaction Patterns & Evaluation   -> 21.1
  22.8  Research Replication Benchmarks              -> 22.5
  25.6  SWE-bench & Agentic SE Evaluation            -> 22.5
  29.3  RAG & Agent Evaluation                       -> 29.1
  29.9  Evaluation Harness Ecosystems                -> 29.1
  29.12 Human Feedback Tooling                       -> 29.10
  30.4  Arena-Style and Crowdsourced Evaluation      -> 29.1

Run from project root:
    /c/Python314/python KDP/build/_step3_slim_eval.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE_DIRS = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# (deleted_path, redirect_target_basename)
DELETIONS = [
    ("part-4-training-adapting/module-13-synthetic-data/section-13.3.html", "section-29.1"),
    ("part-5-retrieval-conversation/module-21-conversational-ai/section-21.7.html", "section-21.1"),
    ("part-6-agentic-ai/module-22-ai-agents/section-22.8.html", "section-22.5"),
    ("part-6-agentic-ai/module-25-specialized-agents/section-25.6.html", "section-22.5"),
    ("part-8-evaluation-production/module-29-evaluation-observability/section-29.3.html", "section-29.1"),
    ("part-8-evaluation-production/module-29-evaluation-observability/section-29.9.html", "section-29.1"),
    ("part-8-evaluation-production/module-29-evaluation-observability/section-29.12.html", "section-29.10"),
    ("part-8-evaluation-production/module-30-observability-monitoring/section-30.4.html", "section-29.1"),
]


def main() -> int:
    n_files = 0
    n_links = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in [d[0] for d in DELETIONS]:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        chapter_n = 0
        for delpath, target in DELETIONS:
            old_base = Path(delpath).stem
            text, n = re.subn(rf'\b{re.escape(old_base)}\.html', f'{target}.html', text)
            chapter_n += n
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_links += chapter_n
            print(f"  {chapter_n:>3}x  {rel}")

    print(f"\nRewrote {n_links} links across {n_files} files\n")
    print("Deleting:")
    for delpath, _ in DELETIONS:
        f = ROOT / delpath
        if f.exists():
            f.unlink()
            print(f"  rm {delpath}")
        else:
            print(f"  (gone) {delpath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
