"""Migration step 7: Dissolve Modules 25, 27, 31 by moving their sections
to their target homes per the restructuring plan.

Module 25 (Agent Safety, Production) -> three destinations:
  25.1, 25.2, 25.6, 25.7 -> part-9/module-38-agent-safety-security (4 sections)
  25.3, 25.4             -> part-10/module-48-shipping-deploying (append)
  25.5                   -> part-6/module-28-multi-agent-systems (append)

Module 27 (LLM Applications) -> seven destinations:
  27.1 -> part-10/module-43-vibe-coding (the chapter's sole section)
  27.2 -> part-11/module-52-finance-llms (append)
  27.3 -> part-11/module-53-healthcare-llms (append)
  27.4 -> part-11/module-59-recommendation-search (the chapter's sole section)
  27.5 -> part-11/module-55-cybersecurity-llms (append)
  27.6 -> part-11/module-58-creative-industries (the chapter's sole section)
  27.7 -> part-7/module-32-embodied-world-models (append, becomes 32.5)

Module 31 (Strategy/PM/ROI) -> four destinations:
  31.1, 31.4 -> part-10/module-42-strategy-prioritization (2 sections)
  31.2       -> part-10/module-41-product-management (1 section)
  31.3, 31.7 -> part-10/module-47-scaling-economics (2 sections)
  31.5, 31.6 -> part-10/module-46-compute-planning (2 sections)

Procedure: for each (source, target_dir, target_section_num):
  - Delete any scaffold stub at target_dir/section-<num>.html if it exists
  - git mv source to target_dir/section-<num>.html
  - Update internals (page-current, breadcrumb, pagefind-meta) to match
    new chapter/section context.

After all 7 + 7 + 7 = 21 moves, the three dissolved module dirs should be
empty and can be removed.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# Dissolution map: (source_relpath, target_relpath, new_section_num, new_chap_num, new_chap_title, part_roman, part_title)
DISSOLUTIONS = [
    # Module 25 -> Part 9 Agent Safety (modules 38)
    ("part-6-agentic-ai/module-25-agent-safety-production/section-25.1.html",
     "part-9-safety-security-ethics/module-38-agent-safety-security/section-38.1.html",
     "38.1", 38, "Agent Safety & Security", "IX", "Safety, Security & Ethics"),
    ("part-6-agentic-ai/module-25-agent-safety-production/section-25.2.html",
     "part-9-safety-security-ethics/module-38-agent-safety-security/section-38.2.html",
     "38.2", 38, "Agent Safety & Security", "IX", "Safety, Security & Ethics"),
    ("part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html",
     "part-9-safety-security-ethics/module-38-agent-safety-security/section-38.3.html",
     "38.3", 38, "Agent Safety & Security", "IX", "Safety, Security & Ethics"),
    ("part-6-agentic-ai/module-25-agent-safety-production/section-25.7.html",
     "part-9-safety-security-ethics/module-38-agent-safety-security/section-38.4.html",
     "38.4", 38, "Agent Safety & Security", "IX", "Safety, Security & Ethics"),
    # Module 25 -> Part 10 Shipping (module 48; original 35 had 4 sections so we append at 48.5, 48.6)
    ("part-6-agentic-ai/module-25-agent-safety-production/section-25.3.html",
     "part-10-idea-to-product/module-48-shipping-deploying/section-48.5.html",
     "48.5", 48, "Shipping & Deploying AI Products", "X", "Idea to Product"),
    ("part-6-agentic-ai/module-25-agent-safety-production/section-25.4.html",
     "part-10-idea-to-product/module-48-shipping-deploying/section-48.6.html",
     "48.6", 48, "Shipping & Deploying AI Products", "X", "Idea to Product"),
    # Module 25 -> Part 6 Multi-Agent (module 28; existing had sections 28.1-28.X, append at 28.6)
    ("part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html",
     "part-6-agentic-ai/module-28-multi-agent-systems/section-28.6.html",
     "28.6", 28, "Multi-Agent Systems", "VI", "Agentic AI"),

    # Module 27 -> various
    ("part-7-multimodal-generation/module-27-llm-applications/section-27.1.html",
     "part-10-idea-to-product/module-43-vibe-coding/section-43.2.html",
     "43.2", 43, "Prototyping via Vibe-Coding", "X", "Idea to Product"),
    ("part-7-multimodal-generation/module-27-llm-applications/section-27.2.html",
     "part-11-applications-across-industries/module-52-finance-llms/section-52.7.html",
     "52.7", 52, "LLMs in Finance", "XI", "Applications Across Industries"),
    ("part-7-multimodal-generation/module-27-llm-applications/section-27.3.html",
     "part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html",
     "53.7", 53, "LLMs in Healthcare & Biomedical", "XI", "Applications Across Industries"),
    ("part-7-multimodal-generation/module-27-llm-applications/section-27.4.html",
     "part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html",
     "59.2", 59, "LLM-Powered Recommendation & Search", "XI", "Applications Across Industries"),
    ("part-7-multimodal-generation/module-27-llm-applications/section-27.5.html",
     "part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html",
     "55.7", 55, "LLMs in Cybersecurity", "XI", "Applications Across Industries"),
    ("part-7-multimodal-generation/module-27-llm-applications/section-27.6.html",
     "part-11-applications-across-industries/module-58-creative-industries/section-58.2.html",
     "58.2", 58, "LLMs in Creative Industries", "XI", "Applications Across Industries"),
    ("part-7-multimodal-generation/module-27-llm-applications/section-27.7.html",
     "part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html",
     "32.8", 32, "Embodied AI, World Models & Multimodal Reasoning", "VII", "Multimodal Generation"),

    # Module 31 -> Part 10 chapters
    ("part-9-safety-security-ethics/module-31-strategy-product-roi/section-31.1.html",
     "part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html",
     "42.3", 42, "LLM Strategy & Use Case Prioritization", "X", "Idea to Product"),
    ("part-9-safety-security-ethics/module-31-strategy-product-roi/section-31.4.html",
     "part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html",
     "42.4", 42, "LLM Strategy & Use Case Prioritization", "X", "Idea to Product"),
    ("part-9-safety-security-ethics/module-31-strategy-product-roi/section-31.2.html",
     "part-10-idea-to-product/module-41-product-management/section-41.2.html",
     "41.2", 41, "LLM Product Management", "X", "Idea to Product"),
    ("part-9-safety-security-ethics/module-31-strategy-product-roi/section-31.3.html",
     "part-10-idea-to-product/module-47-scaling-economics/section-47.3.html",
     "47.3", 47, "Scaling Economics: Unit Costs & ROI", "X", "Idea to Product"),
    ("part-9-safety-security-ethics/module-31-strategy-product-roi/section-31.7.html",
     "part-10-idea-to-product/module-47-scaling-economics/section-47.4.html",
     "47.4", 47, "Scaling Economics: Unit Costs & ROI", "X", "Idea to Product"),
    ("part-9-safety-security-ethics/module-31-strategy-product-roi/section-31.5.html",
     "part-10-idea-to-product/module-46-compute-planning/section-46.3.html",
     "46.3", 46, "Compute Planning & Infrastructure", "X", "Idea to Product"),
    ("part-9-safety-security-ethics/module-31-strategy-product-roi/section-31.6.html",
     "part-10-idea-to-product/module-46-compute-planning/section-46.4.html",
     "46.4", 46, "Compute Planning & Infrastructure", "X", "Idea to Product"),
]


def update_section_internals(p: Path, new_section_num: str, new_chap_num: int,
                              new_chap_title: str, part_roman: str,
                              part_title: str) -> None:
    """Rewrite breadcrumb + page-current + meta inside the moved section."""
    text = p.read_text(encoding="utf-8")
    orig = text

    # page-current
    text = re.sub(r'<div class="page-current">[^<]+</div>',
                   f'<div class="page-current">Section {new_section_num}</div>',
                   text)
    # bc-current span
    text = re.sub(r'<span class="bc-current">Section [^<]+</span>',
                   f'<span class="bc-current">Section {new_section_num}</span>',
                   text)
    # Breadcrumb part link
    text = re.sub(
        r'(<a href="(?:\.\./)+index\.html">)Part [IVXLCDM]+: [^<]+(</a>)',
        rf'\1Part {part_roman}: {part_title}\2',
        text,
    )
    # Breadcrumb chapter anchor
    text = re.sub(
        r'(<a href="index\.html">)Chapter \d+(?::[^<]*)?(</a>)',
        rf'\1Chapter {new_chap_num}: {new_chap_title}\2',
        text,
    )
    # Pagefind chapter meta
    text = re.sub(
        r'data-pagefind-meta="chapter:Chapter \d+(?:: [^"]+)?"',
        f'data-pagefind-meta="chapter:Chapter {new_chap_num}: {new_chap_title}"',
        text,
    )
    # Pagefind part meta
    text = re.sub(
        r'data-pagefind-meta="part:Part [IVXLCDM]+: [^"]+"',
        f'data-pagefind-meta="part:Part {part_roman}: {part_title}"',
        text,
    )
    if text != orig:
        p.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    n = 0
    for src_rel, dst_rel, new_num, new_chap, new_title, p_roman, p_title in DISSOLUTIONS:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            print(f"  SKIP {src_rel}: source missing")
            continue
        if dst.exists():
            # Delete scaffold stub at target
            print(f"  RM scaffold stub {dst.relative_to(ROOT)}")
            if not dry_run:
                dst.unlink()
        print(f"  git mv {src_rel} -> {dst_rel}")
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "mv", str(src), str(dst)],
                            cwd=ROOT, check=False)
            update_section_internals(dst, new_num, new_chap, new_title,
                                       p_roman, p_title)
            n += 1

    # Clean up empty source dirs
    for src_dir in (ROOT / "part-6-agentic-ai/module-25-agent-safety-production",
                     ROOT / "part-7-multimodal-generation/module-27-llm-applications",
                     ROOT / "part-9-safety-security-ethics/module-31-strategy-product-roi"):
        if src_dir.exists():
            # Move any leftover non-section files (illustrations.json, images/)
            for leftover in list(src_dir.iterdir()):
                if leftover.name in ("index.html",):
                    # Drop the now-dead index.html (no longer a chapter)
                    if not dry_run:
                        subprocess.run(["git", "rm", str(leftover)],
                                        cwd=ROOT, check=False)
                else:
                    # Move illustrations.json / images/ — but to where? Leave for now.
                    pass
            try:
                if not dry_run:
                    # Force-remove via git
                    subprocess.run(["git", "rm", "-r", str(src_dir)],
                                    cwd=ROOT, check=False)
                    print(f"  Removed {src_dir.relative_to(ROOT)}")
            except OSError as e:
                print(f"  WARN: could not remove {src_dir.relative_to(ROOT)}: {e}")

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n{mode}: moved {n} sections from dissolved modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
