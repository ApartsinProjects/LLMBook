"""Final pre-v10 staleness sweep: stale part labels, dead module slugs,
stale appendix slug, broken capstone refs.

Catches what earlier cross-link / dropped-refs agents missed because
files were in-flight at the time those agents ran.

Patterns (deterministic):

1. Stale Part labels in prose:
   "Part VII: AI Applications"      -> "Part VII: Multimodal Generation"
   "Part IX: Safety and Strategy"   -> "Part IX: Safety, Security & Ethics"
   "Part X: Frontiers"              -> "Part XII: Frontiers"
   "Part XI: From Idea to AI Product" -> "Part X: From Idea to Product"

2. Dead module slugs in hrefs (these modules no longer exist):
   "module-25-agent-safety-production" -> "module-38-agent-safety-security"
   "module-31-strategy-product-roi"    -> "module-42-strategy-prioritization"
   "module-27-llm-applications"        -> dissolved; topic split across
       module-43-vibe-coding, module-52-finance-llms, module-53-healthcare-llms,
       module-54-education-llms, module-55-cybersecurity-llms,
       module-58-creative-industries, module-59-recommendation-search.
       Without per-row context we can't pick the right target; for these,
       strip the <a> wrapper, keep inner text plain. Author can rewire later.

3. Stale appendix slug:
   "appendix-e-tooling-ecosystem" -> "appendix-e-orchestration-frameworks"

4. Broken capstone refs:
   "../capstone/index.html" -> the capstone content moved to
   appendix-t-capstone-project (v9 reshuffle); rewrite href.

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

# (pattern, replacement, descriptive label)
TEXT_REPLACEMENTS = [
    # Stale Part labels in prose
    ("Part VII: AI Applications", "Part VII: Multimodal Generation"),
    ("Part IX: Safety and Strategy", "Part IX: Safety, Security & Ethics"),
    ("Part X: Frontiers", "Part XII: Frontiers"),
    ("Part XI: From Idea to AI Product", "Part X: From Idea to Product"),
    # Dead module slugs (deterministic redirects)
    ("module-25-agent-safety-production", "module-38-agent-safety-security"),
    ("module-31-strategy-product-roi", "module-42-strategy-prioritization"),
    # Stale appendix slug
    ("appendix-e-tooling-ecosystem", "appendix-e-orchestration-frameworks"),
    # Broken capstone path
    ("../capstone/index.html",
     "../appendices/appendix-t-capstone-project/index.html"),
    ("/capstone/index.html",
     "/appendices/appendix-t-capstone-project/index.html"),
]

# Pattern for module-27-llm-applications (no single redirect target).
# Strip the <a> wrapper, keep inner text.
MODULE_27_HREF_RE = re.compile(
    r'<a[^>]*href="[^"]*module-27-llm-applications[^"]*"[^>]*>([^<]*)</a>'
)


def fix(p: Path, dry_run: bool) -> dict:
    text = p.read_text(encoding="utf-8")
    orig = text
    changes = {"text": 0, "module-27": 0}
    for old, new in TEXT_REPLACEMENTS:
        if old in text:
            n_occ = text.count(old)
            text = text.replace(old, new)
            changes["text"] += n_occ
    # module-27 strip
    def m27_repl(m: re.Match) -> str:
        changes["module-27"] += 1
        return m.group(1)
    text = MODULE_27_HREF_RE.sub(m27_repl, text)
    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    totals = {"text": 0, "module-27": 0}
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
    print(f"Files edited:          {files_edited}")
    print(f"Text replacements:     {totals['text']}")
    print(f"module-27 strips:      {totals['module-27']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
