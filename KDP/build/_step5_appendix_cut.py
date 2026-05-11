"""Step 5: Drop the framework-specific tail appendices.

Keeps:
  K  HuggingFace Ecosystem  (foundational)
  L  LangChain              (most popular agent framework)

Deletes:
  M  LangGraph              -> readers redirected to L (LangChain) for orchestration
  N  CrewAI                 -> readers redirected to L
  O  LlamaIndex             -> readers redirected to K (RAG/embeddings)
  P  Semantic Kernel        -> readers redirected to L
  Q  DSPy                   -> readers redirected to K (programmatic prompting)

Rationale: 5 framework-specific appendices = 25 sections / 47K words of
content that ages out within months. Books that try to be exhaustive
framework references compete with online docs and lose. Better to keep
two solid foundations (K, L) and let readers consult vendor docs for
specialized frameworks.
"""
from __future__ import annotations
import shutil
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE_DIRS = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

DELETE_DIRS = [
    ("appendices/appendix-m-langgraph", "appendix-l-langchain"),
    ("appendices/appendix-n-crewai", "appendix-l-langchain"),
    ("appendices/appendix-o-llamaindex", "appendix-k-huggingface-ecosystem"),
    ("appendices/appendix-p-semantic-kernel", "appendix-l-langchain"),
    ("appendices/appendix-q-dspy", "appendix-k-huggingface-ecosystem"),
]


def main() -> int:
    n_files = 0
    n_links = 0
    delete_dir_names = {Path(d[0]).name for d in DELETE_DIRS}

    # 1. Rewrite inbound cross-references
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        # Skip the doomed appendix files themselves
        if any(part in delete_dir_names for part in p.parts):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        chapter_n = 0
        for del_dir, target_dir in DELETE_DIRS:
            del_name = Path(del_dir).name
            # Replace any 'appendix-X-...' path component with target
            text, n = re.subn(rf'(?<=[/"]){re.escape(del_name)}(?=/)', target_dir, text)
            chapter_n += n
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_links += chapter_n
            print(f"  {chapter_n:>3}x  {p.relative_to(ROOT).as_posix()}")

    print(f"\nRewrote {n_links} links across {n_files} files\n")

    # 2. Delete the appendix directories
    print("Deleting appendix directories:")
    for del_dir, _ in DELETE_DIRS:
        d = ROOT / del_dir
        if d.exists():
            shutil.rmtree(d)
            print(f"  rm -r {del_dir}")
        else:
            print(f"  (gone) {del_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
