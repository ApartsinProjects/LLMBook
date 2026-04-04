"""Fix all known broken cross-reference links (BROKEN_XREF audit, April 2026).

Categories handled:
  1. Old chapter-based paths -> new module-based paths (appendix-k)
  2. Renamed/moved module slugs (various parts)
  3. Missing appendices/index.html -> toc.html or appropriate alternative
  4. Nav links to not-yet-written sections (remove the link element)
  5. Index cards linking to not-yet-written sections (remove the card element)
"""
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:\Projects\LLMCourse")
SKIP = {"vendor", "node_modules", ".git", "deprecated", "__pycache__", "templates", "agents"}

# ---- Simple string replacements: old href substring -> new href substring ----
REPLACEMENTS = [
    # appendix-k: old chapter paths -> new module paths
    (
        "../../chapters/chapter-03-transformer-architecture/index.html",
        "../../part-1-foundations/module-04-transformer-architecture/index.html",
    ),
    (
        "../../chapters/chapter-07-text-generation-decoding/index.html",
        "../../part-1-foundations/module-05-decoding-text-generation/index.html",
    ),
    (
        "../../chapters/chapter-09-fine-tuning/index.html",
        "../../part-4-training-adapting/module-14-fine-tuning-fundamentals/index.html",
    ),
    (
        "../../chapters/chapter-10-alignment-rlhf/index.html",
        "../../part-4-training-adapting/module-17-alignment-rlhf-dpo/index.html",
    ),
    # appendix-r: appendix-n-langchain -> appendix-l-langchain
    (
        "../appendix-n-langchain/index.html",
        "../appendix-l-langchain/index.html",
    ),
    # section-27.5: tool-use-function-calling -> tool-use-protocols
    (
        "../../part-6-agentic-ai/module-23-tool-use-function-calling/section-23.1.html",
        "../../part-6-agentic-ai/module-23-tool-use-protocols/section-23.1.html",
    ),
    # section-29.10: module-27-multimodal-models -> module-27-multimodal
    (
        "../../part-7-multimodal-applications/module-27-multimodal-models/index.html",
        "../../part-7-multimodal-applications/module-27-multimodal/index.html",
    ),
    # section-31.6: module-23-tool-use -> module-23-tool-use-protocols
    (
        "../../part-6-agentic-ai/module-23-tool-use/index.html",
        "../../part-6-agentic-ai/module-23-tool-use-protocols/index.html",
    ),
    # section-31.7: module-16-quantization-distillation -> module-16-distillation-merging
    (
        "../../part-4-training-adapting/module-16-quantization-distillation/index.html",
        "../../part-4-training-adapting/module-16-distillation-merging/index.html",
    ),
    # section-32.10: module-03-text-representation -> module-03-sequence-models-attention
    (
        "../../part-1-foundations/module-03-text-representation/section-3.2.html",
        "../../part-1-foundations/module-03-sequence-models-attention/section-3.2.html",
    ),
    # section-32.10: module-20-rag-fundamentals -> module-20-rag
    (
        "../../part-5-retrieval-conversation/module-20-rag-fundamentals/section-20.1.html",
        "../../part-5-retrieval-conversation/module-20-rag/section-20.1.html",
    ),
    # section-32.11: module-16-distributed-training -> module-16-distillation-merging
    (
        "../../part-4-training-adapting/module-16-distributed-training/index.html",
        "../../part-4-training-adapting/module-16-distillation-merging/index.html",
    ),
    # section-32.11: module-08-architecture-deep-dive -> module-08-reasoning-test-time-compute
    (
        "../../part-2-understanding-llms/module-08-architecture-deep-dive/index.html",
        "../../part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html",
    ),
    # section-32.11: module-15-efficient-adaptation -> module-15-peft
    (
        "../../part-4-training-adapting/module-15-efficient-adaptation/index.html",
        "../../part-4-training-adapting/module-15-peft/index.html",
    ),
    # section-28.5: appendices/index.html -> toc.html (no appendices landing page)
    (
        'href="../../appendices/index.html"',
        'href="../../toc.html"',
    ),
]


def find_html_files():
    for f in BOOK_ROOT.rglob("*.html"):
        if not any(s in f.parts for s in SKIP):
            yield f


def apply_replacements(filepath, html):
    """Apply simple string replacements. Return (new_html, list_of_changes)."""
    changes = []
    for old, new in REPLACEMENTS:
        if old in html:
            html = html.replace(old, new)
            changes.append(f"  replaced: {old[:80]}")
    return html, changes


def fix_appendix_i_up_link(filepath, html):
    """Fix appendix-i index.html: ../index.html up link -> ../../toc.html."""
    changes = []
    if "appendix-i-prompt-templates" in str(filepath) and filepath.name == "index.html":
        old = 'href="../index.html" class="up"'
        new = 'href="../../toc.html" class="up"'
        if old in html:
            html = html.replace(old, new)
            changes.append("  fixed up-link: ../index.html -> ../../toc.html")
        # Also check reversed attribute order
        old2 = 'class="up" href="../index.html"'
        new2 = 'class="up" href="../../toc.html"'
        if old2 in html:
            html = html.replace(old2, new2)
            changes.append("  fixed up-link: ../index.html -> ../../toc.html")
    return html, changes


def remove_nav_to_missing_section(filepath, html):
    """Remove <a class='next'> nav links that point to sections that do not exist."""
    changes = []
    missing_targets = [
        "section-u.5.html",
        "section-v.4.html",
        "section-v.5.html",
    ]
    for target in missing_targets:
        # Check if this file actually references the missing target
        if target not in html:
            continue
        # Resolve to see if it truly is missing
        resolved = (filepath.parent / target).resolve()
        if resolved.exists():
            continue
        # Remove <a class="next" href="TARGET">...</a> nav links
        pattern = re.compile(
            r'\s*<a\s+class="next"\s+href="' + re.escape(target) + r'"[^>]*>[^<]*</a>',
            re.IGNORECASE,
        )
        new_html, count = pattern.subn("", html)
        if count:
            html = new_html
            changes.append(f"  removed nav-next link to missing {target}")
    return html, changes


def remove_cards_to_missing_sections(filepath, html):
    """Remove section-card <a> blocks that link to missing section files."""
    changes = []
    missing_targets = [
        "section-u.5.html",
        "section-v.4.html",
        "section-v.5.html",
    ]
    for target in missing_targets:
        if target not in html:
            continue
        resolved = (filepath.parent / target).resolve()
        if resolved.exists():
            continue
        # Match the full section-card <a> block (multiline)
        pattern = re.compile(
            r'\s*<a\s+href="' + re.escape(target) + r'"\s+class="section-card">\s*'
            r'<span class="section-number">[^<]*</span>\s*'
            r'<span class="section-title">[^<]*</span>\s*'
            r'</a>',
            re.DOTALL,
        )
        new_html, count = pattern.subn("", html)
        if count:
            html = new_html
            changes.append(f"  removed section-card for missing {target}")
    return html, changes


def fix_file(filepath):
    html = filepath.read_text(encoding="utf-8", errors="replace")
    original = html
    all_changes = []

    html, ch = apply_replacements(filepath, html)
    all_changes.extend(ch)

    html, ch = fix_appendix_i_up_link(filepath, html)
    all_changes.extend(ch)

    html, ch = remove_nav_to_missing_section(filepath, html)
    all_changes.extend(ch)

    html, ch = remove_cards_to_missing_sections(filepath, html)
    all_changes.extend(ch)

    if html != original:
        filepath.write_text(html, encoding="utf-8", newline="\n")

    return all_changes


def main():
    total_files = 0
    total_fixes = 0

    for filepath in sorted(find_html_files()):
        changes = fix_file(filepath)
        if changes:
            rel = filepath.relative_to(BOOK_ROOT)
            print(f"{rel}:")
            for c in changes:
                print(c)
            total_files += 1
            total_fixes += len(changes)

    print(f"\nFixed {total_fixes} broken links across {total_files} files.")


if __name__ == "__main__":
    main()
