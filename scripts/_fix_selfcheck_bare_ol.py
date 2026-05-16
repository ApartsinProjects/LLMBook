"""Convert non-standard self-check callouts (bare <ol> of questions, no
<details> answer blocks) to the canonical structure used in the rest of
the book.

Anchor case: section-30.3.html had this exact bug. 9 more files have it
(per callout-format-audit.md).

Transformation per matched callout:
   Before:
     <div class="callout self-check">
       <div class="callout-title">Self-Check Questions</div>     (sometimes "Self-Check")
       <ol>
         <li>Question 1?</li>
         <li>Question 2?</li>
       </ol>
     </div>

   After:
     <div class="callout self-check">
       <div class="callout-title">Self-Check</div>
       <p class="quiz-question">1. Question 1?</p>
       <details><summary>Show Answer</summary><div class="answer">[ANSWER PENDING - refer to the section text for guidance.]</div></details>
       <p class="quiz-question">2. Question 2?</p>
       <details><summary>Show Answer</summary><div class="answer">[ANSWER PENDING - refer to the section text for guidance.]</div></details>
     </div>

Placeholder answers are explicitly marked so an editorial follow-up pass
finds them. They are better than leaving the reader with no expansion at
all (which is the current state).

Run from project root:
    python scripts/_fix_selfcheck_bare_ol.py [--dry-run]
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

PLACEHOLDER_ANSWER = (
    "[Answer pending editorial revision. Refer to the section text "
    "for guidance on this question.]"
)


def should_skip(p: Path) -> bool:
    return bool(set(p.parts) & SKIP_PARTS)


# Match a self-check callout that contains an <ol> and no <details>.
# Greedy through to the closing </div> of the callout.
# Use a non-greedy body and require the </div> to close the OUTER div by
# counting braces - simpler: match the well-known shape produced by the
# bug, which is: callout open, title div, ol, /callout.
SELFCHECK_RE = re.compile(
    r'<div class="callout self-check"[^>]*>\s*'
    r'<div class="callout-title">([^<]+)</div>\s*'
    r'<ol>(.*?)</ol>\s*'
    r'</div>',
    flags=re.DOTALL,
)

# Per-question <li>...</li> within the ol
LI_RE = re.compile(r'<li>(.*?)</li>', flags=re.DOTALL)


def transform_callout(match: re.Match) -> str:
    title_text = match.group(1).strip()
    ol_body = match.group(2)
    # Canonical title is just "Self-Check"
    new_title = "Self-Check"
    questions = [m.group(1).strip() for m in LI_RE.finditer(ol_body)]
    if not questions:
        # Don't transform empty self-checks (shouldn't happen but be safe)
        return match.group(0)

    parts = [
        '<div class="callout self-check">',
        f'<div class="callout-title">{new_title}</div>',
    ]
    for i, q in enumerate(questions, 1):
        # Question text - leave inline tags intact
        parts.append(f'<p class="quiz-question">{i}. {q}</p>')
        parts.append(
            '<details><summary>Show Answer</summary>'
            f'<div class="answer">{PLACEHOLDER_ANSWER}</div></details>'
        )
    parts.append('</div>')
    return '\n'.join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files_changed = 0
    callouts_changed = 0
    questions_total = 0
    for p in ROOT.rglob("*.html"):
        if should_skip(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new_text, n = SELFCHECK_RE.subn(transform_callout, text)
        if n > 0:
            # Count questions added
            qs_here = sum(
                len(LI_RE.findall(m.group(2)))
                for m in SELFCHECK_RE.finditer(text)
            )
            rel = p.relative_to(ROOT)
            print(f"  {rel}: {n} callout(s), {qs_here} question(s) normalized")
            if not args.dry_run:
                p.write_text(new_text, encoding="utf-8")
            files_changed += 1
            callouts_changed += n
            questions_total += qs_here

    print()
    print(f"TOTAL: {callouts_changed} self-check callout(s) across {files_changed} files; "
          f"{questions_total} question(s) given placeholder answers")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
