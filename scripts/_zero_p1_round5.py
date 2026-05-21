"""Round 5 P1 zero-out: propagate section X.7 -> X.6 renames.

Earlier round renamed:
  module-52/section-52.7.html -> section-52.6.html
  module-53/section-53.7.html -> section-53.6.html
  module-55/section-55.7.html -> section-55.6.html
  module-28/section-28.6.html -> section-28.4.html

Cross-ref rewrite only touched 6 files; index/prev-next links in
sibling section files still reference the old names. Book-wide
text.replace for the four paths.

Idempotent.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}

RENAMES = [
    ("section-52.7.html", "section-52.6.html"),
    ("section-53.7.html", "section-53.6.html"),
    ("section-55.7.html", "section-55.6.html"),
    ("section-28.6.html", "section-28.4.html"),
]

# Stale visible-text fixes near the renamed links (audit pass found
# href="section-52.6.html">Section 52.7< forms; clean those up so the
# rendered label matches the file).
PROSE_RENAMES = [
    ('href="section-52.6.html">Section 52.7',
     'href="section-52.6.html">Section 52.6'),
    ('href="section-53.6.html">Section 53.7',
     'href="section-53.6.html">Section 53.6'),
    ('href="section-55.6.html">Section 55.7',
     'href="section-55.6.html">Section 55.6'),
    ('href="section-28.4.html">Section 28.6',
     'href="section-28.4.html">Section 28.4'),
]

# Page-current labels on the renamed section files themselves
PAGE_CURRENT_FIXES = {
    "part-11-applications-across-industries/module-52-finance-llms/section-52.6.html":
        ('<div class="page-current">Section 52.7</div>',
         '<div class="page-current">Section 52.6</div>'),
    "part-11-applications-across-industries/module-53-healthcare-llms/section-53.6.html":
        ('<div class="page-current">Section 53.7</div>',
         '<div class="page-current">Section 53.6</div>'),
    "part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.6.html":
        ('<div class="page-current">Section 55.7</div>',
         '<div class="page-current">Section 55.6</div>'),
    "part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html":
        ('<div class="page-current">Section 28.6</div>',
         '<div class="page-current">Section 28.4</div>'),
}

# section-card span labels (chapter index pages still using old 1-span
# format where the chapter-index rebuild agent hasn't refreshed yet)
SECTION_CARD_LABEL_FIXES = [
    ('href="section-53.6.html"><span class="section-num">Section 53.7</span>',
     'href="section-53.6.html"><span class="section-num">Section 53.6</span>'),
    ('href="section-52.6.html"><span class="section-num">Section 52.7</span>',
     'href="section-52.6.html"><span class="section-num">Section 52.6</span>'),
    ('href="section-55.6.html"><span class="section-num">Section 55.7</span>',
     'href="section-55.6.html"><span class="section-num">Section 55.6</span>'),
]

# Per-file title-tag fixes after section renames
TITLE_FIXES = {
    "part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html":
        ("<title>Section 28.5: ", "<title>Section 28.4: "),
    "part-11-applications-across-industries/module-52-finance-llms/section-52.6.html":
        ("<title>Section 52.2: ", "<title>Section 52.6: "),
    "part-11-applications-across-industries/module-53-healthcare-llms/section-53.6.html":
        ("<title>Section 53.3: ", "<title>Section 53.6: "),
    "part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.6.html":
        ("<title>Section 55.5: ", "<title>Section 55.6: "),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    files_edited = 0
    total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        for old, new in RENAMES:
            if old in text:
                n = text.count(old)
                text = text.replace(old, new)
                total += n
        for old, new in PROSE_RENAMES:
            if old in text:
                n = text.count(old)
                text = text.replace(old, new)
                total += n
        for old, new in SECTION_CARD_LABEL_FIXES:
            if old in text:
                n = text.count(old)
                text = text.replace(old, new)
                total += n
        # Per-file page-current labels + title-tag fixes
        rel = p.relative_to(ROOT).as_posix()
        if rel in PAGE_CURRENT_FIXES:
            old, new = PAGE_CURRENT_FIXES[rel]
            if old in text:
                text = text.replace(old, new)
                total += 1
        if rel in TITLE_FIXES:
            old, new = TITLE_FIXES[rel]
            if old in text:
                text = text.replace(old, new)
                total += 1
        if text != orig:
            files_edited += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:  {files_edited}")
    print(f"Replacements:  {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
