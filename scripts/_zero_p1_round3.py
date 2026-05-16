"""Round 3 P1 zero-out: cross-part bare-module refs + dead-section strips.

Pattern: from section files in part-X, links use `../module-YY-slug/...`
but module-YY lives in part-Y (different part). Resolves wrong. Fix:
prepend `../part-Y-slug/` so href becomes `../../part-Y-slug/module-YY-...`
(equivalent: replace `../module-YY-` with `../../part-Y-slug/module-YY-`).

Module location map (cross-part, the ones that recur in audits):
  module-26-ai-agents              -> part-6-agentic-ai
  module-27-tool-use-protocols     -> part-6-agentic-ai
  module-28-multi-agent-systems    -> part-6-agentic-ai
  module-29-specialized-agents     -> part-6-agentic-ai
  module-31-multimodal             -> part-7-multimodal-generation
  module-32-embodied-world-models  -> part-7-multimodal-generation
  module-37-safety-ethics-regulation -> part-9-safety-security-ethics
  module-38-agent-safety-security  -> part-9-safety-security-ethics
  module-42-strategy-prioritization -> part-10-idea-to-product
  module-46-compute-planning       -> part-10-idea-to-product
  module-07-pretraining-scaling-laws -> part-2-understanding-llms

Plus dead-section strips (sections don't exist):
  module-46/section-46.3, .4 (deleted in dup fix)
  module-47/section-47.3, .4 (deleted in dup fix)
  module-48/section-48.5, .6 (deleted in dup fix)
  module-42/section-42.5 (no such section)
  module-62/section-62.5, .6, .7 (only 1-4 exist)
  module-37/section-37.4 (deleted)

Plus slug renames:
  module-07-tokenization -> module-02-tokenization-subword-models
  module-11-mechanistic-interpretability -> module-11-interpretability
  section-6.2 -> section-7.2 (chapter renumber in module-07)

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

# Module slug -> part slug
MODULE_TO_PART = {
    "module-26-ai-agents": "part-6-agentic-ai",
    "module-27-tool-use-protocols": "part-6-agentic-ai",
    "module-28-multi-agent-systems": "part-6-agentic-ai",
    "module-29-specialized-agents": "part-6-agentic-ai",
    "module-31-multimodal": "part-7-multimodal-generation",
    "module-32-embodied-world-models": "part-7-multimodal-generation",
    "module-37-safety-ethics-regulation": "part-9-safety-security-ethics",
    "module-38-agent-safety-security": "part-9-safety-security-ethics",
    "module-42-strategy-prioritization": "part-10-idea-to-product",
    "module-46-compute-planning": "part-10-idea-to-product",
    "module-07-pretraining-scaling-laws": "part-2-understanding-llms",
}

# Slug renames
SLUG_RENAMES = [
    ("module-07-tokenization/", "module-02-tokenization-subword-models/"),
    ("module-11-mechanistic-interpretability/", "module-11-interpretability/"),
    # section-6.2 in module-07 -> section-7.2 (chapter renumbered from 6 to 7)
    ("module-07-pretraining-scaling-laws/section-6.",
     "module-07-pretraining-scaling-laws/section-7."),
]

# Strip dead-section refs
DEAD_SECTIONS = [
    r"module-46-compute-planning/section-46\.(3|4)\.html",
    r"module-47-scaling-economics/section-47\.(3|4)\.html",
    r"module-48-shipping-deploying/section-48\.(5|6)\.html",
    r"module-42-strategy-prioritization/section-42\.(5|6|7|8)\.html",
    r"module-62-frontier-theory/section-62\.(5|6|7|8|9)\.html",
    r"module-37-safety-ethics-regulation/section-37\.(4|13|14)\.html",
]


def fix(p: Path, dry_run: bool) -> dict:
    text = p.read_text(encoding="utf-8")
    orig = text
    c = {"crosspart": 0, "rename": 0, "strip": 0, "bare_section": 0}

    # 1. Cross-part bare-module fixes: ../module-YY -> ../../part-Y-slug/module-YY
    # Match href="../module-YY-slug/..." where module-YY is in MODULE_TO_PART
    # and source file is in a DIFFERENT part.
    src_part = None
    for parent in p.parts:
        if parent.startswith("part-"):
            src_part = parent
            break
    for mod, part in MODULE_TO_PART.items():
        if src_part == part:
            continue  # Same-part links use ../ correctly
        # Replace '../module-YY-' with '../../part-Y-slug/module-YY-'
        old = f'"../{mod}/'
        new = f'"../../{part}/{mod}/'
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            c["crosspart"] += n
        # Also handle bare module/ at start of href (no ../ prefix)
        old2 = f'"{mod}/'
        # Only replace when it appears as href="module-..." (not within longer paths)
        text2 = re.sub(rf'href="{re.escape(mod)}/',
                        f'href="../../{part}/{mod}/', text)
        if text2 != text:
            c["bare_section"] += 1
            text = text2

    # 2. Slug renames
    for old, new in SLUG_RENAMES:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            c["rename"] += n

    # 3. Strip dead-section refs
    for pat in DEAD_SECTIONS:
        text, n = re.subn(
            rf'<a[^>]*href="[^"]*{pat}[^"]*"[^>]*>([^<]*)</a>',
            r"\1", text,
        )
        c["strip"] += n

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    totals = {"crosspart": 0, "rename": 0, "strip": 0, "bare_section": 0}
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
    print(f"Files edited:               {files_edited}")
    print(f"Cross-part path fixes:      {totals['crosspart']}")
    print(f"Bare-section path fixes:    {totals['bare_section']}")
    print(f"Slug renames:               {totals['rename']}")
    print(f"Dead-section strips:        {totals['strip']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
