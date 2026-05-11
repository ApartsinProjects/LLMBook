"""Step 4: Consolidate reasoning + agent chapters.

Deletes (with redirect to nearest survivor):
  11.5 Prompting Reasoning Models    -> 11.2 (Chain-of-Thought)
  24.3 Communication/Consensus       -> 24.2 (Architecture Patterns)
  24.4 State Mgmt/Workflows          -> 24.2 (Architecture Patterns)
  25.3 Computer Use Agents           -> 25.2 (Browser & Web Agents)
  25.5 Domain-Specific Patterns      -> 25.1 (Code Generation Agents)
  25.8 AI Code Quality               -> 25.7 (Code/Work Workflows)

Reasoning content already lives mostly in Module 8; only 11.5 was a
clear duplicate. Others (8.x, 11.2, 13.7, 22.3-4, 34.5) are kept as
they offer genuinely distinct angles.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE_DIRS = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

DELETIONS = [
    ("part-3-working-with-llms/module-11-prompt-engineering/section-11.5.html", "section-11.2"),
    ("part-6-agentic-ai/module-24-multi-agent-systems/section-24.3.html", "section-24.2"),
    ("part-6-agentic-ai/module-24-multi-agent-systems/section-24.4.html", "section-24.2"),
    ("part-6-agentic-ai/module-25-specialized-agents/section-25.3.html", "section-25.2"),
    ("part-6-agentic-ai/module-25-specialized-agents/section-25.5.html", "section-25.1"),
    ("part-6-agentic-ai/module-25-specialized-agents/section-25.8.html", "section-25.7"),
]


def main() -> int:
    n_files = 0
    n_links = 0
    delete_paths = {d[0] for d in DELETIONS}
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in delete_paths:
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
