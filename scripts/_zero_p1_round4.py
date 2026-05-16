"""Round 4 P1 zero-out: final mechanical fixes.

1. part-10-idea-to-product/index.html has stale section links inside its
   chapter cards (46.4, 47.3, 47.4, 48.5, 48.6 were all deleted in the
   duplication fixes; the chapter-card section lists never refreshed).
   Strip those <li>...<a href='section-X.Y.html'>...</a>...</li>.

2. module-46/47/48 chapter indexes: same stale section-card refs.

3. Strip dead-section <a> wrappers (sections don't exist):
   section-42.5, section-55.6, section-58.7, section-59.5,
   section-62.5..9

4. Slug renames (audit-revealed):
   module-29-multi-agent -> module-28-multi-agent-systems
   module-35-llmops-mlops -> module-35-production-engineering

5. Strip module-42/section-31.5 ref (section was renamed AND renumbered)

6. Fix appendix-p-course-syllabi/index.html line 229 bare appendix-q
   ref: 'appendix-q-reading-pathways/' -> '../appendix-q-reading-pathways/'

7. Fix part-2-understanding-llms/module-02-tokenization-subword-models
   ref: module-02 lives in part-1, not part-2. Rewrite to
   part-1-foundations/module-02-tokenization-subword-models/.

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


def fix(p: Path, dry_run: bool) -> dict:
    text = p.read_text(encoding="utf-8")
    orig = text
    c = {"replace": 0, "strip": 0, "li_strip": 0}

    # 7. Wrong-part for module-02 (lives in part-1, not part-2)
    text = text.replace(
        "part-2-understanding-llms/module-02-tokenization-subword-models",
        "part-1-foundations/module-02-tokenization-subword-models",
    )

    # 4. Module slug renames
    renames = [
        ("module-29-multi-agent/", "module-28-multi-agent-systems/"),
        ("module-35-llmops-mlops/", "module-35-production-engineering/"),
    ]
    for old, new in renames:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            c["replace"] += n

    # 6. appendix-p line 229 bare appendix-q ref
    text = text.replace(
        'href="appendix-q-reading-pathways/',
        'href="../appendix-q-reading-pathways/',
    )

    # 3, 5. Strip dead-section <a> wrappers
    dead_patterns = [
        r"module-42-strategy-prioritization/section-(31\.5|42\.5)\.html",
        r"module-55-cybersecurity-llms/section-55\.6\.html",
        r"module-58-creative-industries/section-58\.7\.html",
        r"module-59-recommendation-search/section-59\.5\.html",
        r"module-62-frontier-theory/section-62\.(5|6|7|8|9)\.html",
        r"module-46-compute-planning/section-46\.(3|4)\.html",
        r"module-47-scaling-economics/section-47\.(3|4)\.html",
        r"module-48-shipping-deploying/section-48\.(5|6)\.html",
        r"(^|/)section-42\.5\.html",
        r"(^|/)section-55\.6\.html",
        r"(^|/)section-58\.7\.html",
        r"(^|/)section-59\.5\.html",
        r"(^|/)section-62\.(5|6|7|8|9)\.html",
        r"(^|/)section-46\.(3|4)\.html",
        r"(^|/)section-47\.(3|4)\.html",
        r"(^|/)section-48\.(5|6)\.html",
    ]
    for pat in dead_patterns:
        text, n = re.subn(
            rf'<a[^>]*href="[^"]*{pat}[^"]*"[^>]*>([^<]*)</a>',
            lambda m: m.group(m.lastindex) if m.lastindex else "",
            text,
        )
        c["strip"] += n

    # 1, 2. Strip <li>...<a href="section-X.Y.html">...</a></li> when
    # X.Y is one of the deleted sections (in part-10 index + module
    # indexes)
    dead_li = [
        "section-46.3.html", "section-46.4.html",
        "section-47.3.html", "section-47.4.html",
        "section-48.5.html", "section-48.6.html",
    ]
    for fn in dead_li:
        # Match li wrapper around a link to fn
        pattern = re.compile(
            rf'<li>\s*<a[^>]*href="[^"]*{re.escape(fn)}[^"]*"[^>]*>'
            rf'[\s\S]*?</a>\s*</li>'
        )
        text, n = pattern.subn("", text)
        c["li_strip"] += n
        # Also section-card form
        pattern2 = re.compile(
            rf'<a class="section-card" href="[^"]*{re.escape(fn)}[^"]*"[^>]*>'
            rf'[\s\S]*?</a>'
        )
        text, n = pattern2.subn("", text)
        c["li_strip"] += n

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    totals = {"replace": 0, "strip": 0, "li_strip": 0}
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
    print(f"Files edited:      {files_edited}")
    print(f"Slug replacements: {totals['replace']}")
    print(f"Dead-link strips:  {totals['strip']}")
    print(f"<li> / card strips:{totals['li_strip']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
