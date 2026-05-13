"""8th edition: comprehensive audit of </main> placement.

Catches three failure modes that all produce the same symptom (bottom
of page renders full-viewport-width because content is OUTSIDE the
page-width-constrained <main class="content"> container):

  V1. </main> immediately followed by <section class="bibliography">
      (caught by v692; now folded in here for completeness).
  V2. </main> appears, then significant content (lab, exercises,
      whats-next, bibliography) appears AFTER it but before </body>.
      This is the 12.6 case.
  V3. Duplicate <footer> tags or duplicate </main> tags suggest a
      botched insertion.

For V2 the heuristic is: find the FIRST </main> in the file; if any
of these element classes appear AFTER it but BEFORE </body>, the
file is broken:
    section.bibliography
    div.whats-next
    div.lab
    h2 with text "Exercises" or "References"
    div.callout exercise

Read-only audit. Reports each file + which classes leaked out.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

LEAK_PATTERNS = [
    ('bibliography',
     re.compile(r'<section[^>]*class="bibliography"', re.IGNORECASE)),
    ('whats-next',
     re.compile(r'<div[^>]*class="whats-next"', re.IGNORECASE)),
    ('lab',
     re.compile(r'<div[^>]*class="lab"', re.IGNORECASE)),
    ('exercises-h2',
     re.compile(r'<h2[^>]*>\s*Exercises\s*</h2>', re.IGNORECASE)),
    ('callout-exercise',
     re.compile(r'<div[^>]*class="callout exercise"', re.IGNORECASE)),
    ('chapter-nav',
     re.compile(r'<nav[^>]*class="chapter-nav"', re.IGNORECASE)),
    ('footer',
     re.compile(r'<footer', re.IGNORECASE)),
]


def main() -> int:
    n_bad = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        # Find first </main>
        m = re.search(r'</main\s*>', text, re.IGNORECASE)
        if not m:
            continue
        # Find </body>
        body_match = re.search(r'</body\s*>', text, re.IGNORECASE)
        if not body_match:
            continue
        tail = text[m.end():body_match.start()]
        # Strip <script> and <style> contents from tail (we don't care
        # about content classes appearing inside scripts).
        tail_clean = re.sub(r'<script[\s\S]*?</script>', '', tail,
                            flags=re.IGNORECASE)
        tail_clean = re.sub(r'<style[\s\S]*?</style>', '', tail_clean,
                            flags=re.IGNORECASE)
        leaks = []
        for name, pat in LEAK_PATTERNS:
            if pat.search(tail_clean):
                leaks.append(name)
        # Also count: >1 </main> or >1 <footer>
        nmain = len(re.findall(r'</main\s*>', text, re.IGNORECASE))
        nfooter = len(re.findall(r'<footer', text, re.IGNORECASE))
        extras = []
        if nmain > 1:
            extras.append(f'{nmain}x </main>')
        if nfooter > 1:
            extras.append(f'{nfooter}x <footer>')
        if leaks or extras:
            n_bad += 1
            tags = ', '.join(leaks + extras)
            print(f'  {p.relative_to(ROOT)} : {tags}')
    print(f'\nFiles with </main>-placement issues: {n_bad}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
