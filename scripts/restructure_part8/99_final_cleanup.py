"""Phase 9.9: final cleanup of remaining broken refs.

Targets:
  1. Bare `section-50.5.html` in module-51 (cross-module sibling) ->
     `../module-50-shipping-deploying/section-50.5.html`.
  2. Bare `section-34.1.html` in non-module-34 files ->
     `../module-34-evaluation-foundations/section-34.1.html`.
  3. Bare `section-34.12.html` (was moved cross-part) ->
     `../../part-10-idea-to-product/module-48-compute-planning/section-48.4.html`.
  4. Forward-looking refs in NEW authored sections to anticipated module
     names that don't exist yet:
       part-6-rag-systems -> part-5-retrieval-conversation
       module-23-rag-evaluation -> module-23-rag
       module-25-agent-foundations -> module-26-ai-agents
  5. My phase 9.5 routed 37.1/37.6 to module-34-evaluation-foundations,
     but the new authored 37.X files are in module-37-online-eval-
     observability. Re-route to module-37.

DRY-RUN by default.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "vendor", "docs"}

# (regex_pattern, replacement) — applied per-file
GLOBAL_REWRITES = [
    # Forward-looking refs in new authored sections
    (r'part-6-rag-systems/module-23-rag-evaluation/section-(\d+)\.(\d+)\.html',
     r'part-5-retrieval-conversation/module-23-rag/section-\1.\2.html'),
    (r'part-6-agentic-ai/module-25-agent-foundations/index\.html',
     r'part-6-agentic-ai/module-26-ai-agents/index.html'),
    (r'part-6-agentic-ai/module-25-agent-foundations/section-(\d+)\.(\d+)\.html',
     r'part-6-agentic-ai/module-26-ai-agents/section-\1.\2.html'),
    # 37.X re-route: phase 9.5 sent these to module-34; actual home is module-37
    (r'../module-34-evaluation-foundations/section-37\.1\.html',
     r'../module-37-online-eval-observability/section-37.1.html'),
    (r'../module-34-evaluation-foundations/section-37\.3\.html',
     r'../module-37-online-eval-observability/section-37.3.html'),
    (r'../module-34-evaluation-foundations/section-37\.6\.html',
     r'../module-37-online-eval-observability/section-37.6.html'),
]


def fix_same_folder_cross_module(p: Path, dry_run: bool) -> int:
    """For files in module-51-production-engineering, rewrite bare section-50.X.html
    to ../module-50-shipping-deploying/section-50.X.html. Generalize for other
    cases too."""
    rel = p.relative_to(ROOT).as_posix()
    if "module-51-production-engineering" not in rel:
        return 0
    text = p.read_text(encoding="utf-8")
    orig = text
    # section-50.X.html (same-folder form, but should be ../module-50/)
    text = re.sub(
        r'href="section-50\.(\d+)\.html"',
        r'href="../module-50-shipping-deploying/section-50.\1.html"',
        text,
    )
    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1 if text != orig else 0


def fix_bare_34_refs(p: Path, dry_run: bool) -> int:
    """Bare section-34.X.html refs in files NOT in module-34 — rewrite to absolute path."""
    rel = p.relative_to(ROOT).as_posix()
    if "module-34-evaluation-foundations" in rel:
        return 0
    text = p.read_text(encoding="utf-8")
    orig = text
    # Bare section-34.X.html
    def repl(m: re.Match) -> str:
        X = int(m.group(1))
        # Compute correct relative path based on src file's location
        # Depth: count parts to get up to book root
        src_parts = p.relative_to(ROOT).parts
        # Always reach to module-34-evaluation-foundations under part-8-evaluation-production
        # Compute depth: if src is in part-8 (same part), use ../module-34-.../
        # if src is elsewhere, use ../../part-8-evaluation-production/module-34-.../
        if src_parts[0] == "part-8-evaluation-production":
            return f'href="../module-34-evaluation-foundations/section-34.{X}.html"'
        elif src_parts[0].startswith("part-"):
            return f'href="../../part-8-evaluation-production/module-34-evaluation-foundations/section-34.{X}.html"'
        else:
            # appendix or front-matter — same as part- case
            return f'href="../../part-8-evaluation-production/module-34-evaluation-foundations/section-34.{X}.html"'

    text = re.sub(r'href="section-34\.(\d+)\.html"', repl, text)

    # Bare section-34.12.html -> cross-part to module-48 section-48.4
    def repl_34_12(m: re.Match) -> str:
        src_parts = p.relative_to(ROOT).parts
        if src_parts[0] == "part-10-idea-to-product":
            return f'href="../module-48-compute-planning/section-48.4.html"'
        elif src_parts[0].startswith("part-"):
            return f'href="../../part-10-idea-to-product/module-48-compute-planning/section-48.4.html"'
        else:
            return f'href="../../part-10-idea-to-product/module-48-compute-planning/section-48.4.html"'

    text = re.sub(r'href="section-34\.12\.html"', repl_34_12, text)

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1 if text != orig else 0


def apply_global_rewrites(p: Path, dry_run: bool) -> int:
    text = p.read_text(encoding="utf-8")
    orig = text
    for pat, repl in GLOBAL_REWRITES:
        text = re.sub(pat, repl, text)
    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1 if text != orig else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    files_edited = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        edited = (
            fix_same_folder_cross_module(p, dry_run)
            + fix_bare_34_refs(p, dry_run)
            + apply_global_rewrites(p, dry_run)
        )
        if edited:
            files_edited += 1
    print(f"=== Summary ===")
    print(f"Files edited: {files_edited}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
