"""Resolve P2 figure-replaced placeholders book-wide.

Pattern (chart-suppression policy leftover from an earlier audit):

  <!-- TODO(audit): broken figure ref "Figure X.Y.Z": ... -->
  <p>...Figure X.Y.Z [verb] [explanation].</p>      (figure-reference sentence)
  <!-- Diagram: ... -->                              (optional)
  <p class="figure-replaced"><em>description</em></p> (placeholder alt-text)

The figure was never authored. The TODO comments tell us to either author
the figure or remove the placeholders. Per author direction, we resolve
in-place by:

  1. Removing the TODO comment.
  2. Stripping the "Figure X.Y.Z ..." sentence from the preceding <p>
     (where present). Keep everything before it.
  3. Demoting the figure-replaced placeholder to plain prose: drop
     `class="figure-replaced"` and unwrap `<em>` so the description reads
     as a normal paragraph that continues the narrative.

Result: each placeholder becomes substantive prose continuation. The
broken figure reference disappears; the descriptive text stays.

Idempotent: TODO comments only appear once per placeholder.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "vendor", "scripts", "docs",
              "styles"}

TODO_PAT = re.compile(
    r'<!-- TODO\(audit\): broken figure ref "(Figure (\d+\.\d+\.\d+))"[^>]*-->'
)


def fix(p: Path, dry_run: bool) -> int:
    text = p.read_text(encoding="utf-8")
    orig = text
    count = 0

    # Process in a loop because each fix changes indices
    while True:
        m = TODO_PAT.search(text)
        if not m:
            break
        fig_label = m.group(1)   # "Figure 37.2.3"
        fig_num = m.group(2)     # "37.2.3"
        # Remove the TODO comment
        text_pre = text[:m.start()]
        text_after = text[m.end():]
        # Strip "Figure X.Y.Z [verb-phrase up to first period]." inside the
        # immediately-following <p>...</p>. The sentence may be the last
        # sentence in that paragraph, or sit mid-paragraph.
        # Regex: " Figure 37.2.3 [^.]{1,300}\."
        # Match optional leading whitespace too.
        sentence_re = re.compile(
            rf' ?{re.escape(fig_label)} [^.<]{{1,400}}\.',
        )
        text_after = sentence_re.sub('', text_after, count=1)
        # Demote figure-replaced placeholder: <p class="figure-replaced"><em>X</em></p> -> <p>X</p>
        # Match the FIRST occurrence after the TODO.
        fr_re = re.compile(
            r'<p class="figure-replaced"><em>(.+?)</em></p>', re.DOTALL,
        )
        text_after = fr_re.sub(r'<p>\1</p>', text_after, count=1)
        # Also strip the optional "<!-- Diagram: ... -->" comment between the
        # paragraph and the placeholder, if present.
        text_after = re.sub(
            r'\n<!-- Diagram:[^>]+-->\n', '\n', text_after, count=1
        )
        text = text_pre + text_after
        count += 1

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return count


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
        n = fix(p, dry_run)
        if n > 0:
            files_edited += 1
            total += n
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:        {files_edited}")
    print(f"Placeholders fixed:  {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
