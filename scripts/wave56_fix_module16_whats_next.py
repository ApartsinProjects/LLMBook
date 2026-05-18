"""Wave 56: Fix the broken whats-next/fun-note/bibliography structure in
Module 16 sections (16.1-16.5).

Broken pattern observed:
    <div class="whats-next">
    <h2 id="what-comes-next">What Comes Next</h2>
    <p>... next section paragraph (no </p>)
    <div class="callout fun-note">          <-- empty fun-note opens
    <div class="callout-title">Fun Fact</div>  <-- title only, no body
    <details class="bibliography-collapsible" open>   <-- bib opens INSIDE
    ...

Fix:
    <div class="whats-next">
    <h2 id="what-comes-next">What Comes Next</h2>
    <p>... next section paragraph</p>
    </div>
    <details class="bibliography-collapsible" open>
    ...

The empty fun-note callout is deleted (it has no body) and the whats-next div is
properly closed before the bibliography begins.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

# Specific Module 16 sections affected
TARGETS = [
    'part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.1.html',
    'part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.2.html',
    'part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.3.html',
    'part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.4.html',
    'part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.5.html',
]

# Match the broken sequence — </p> directly followed by an empty fun-note +
# bibliography. The whats-next div is unclosed at this point.
# The fun-note has only a callout-title (no body) and is never closed.
BROKEN_RE = re.compile(
    r'(</p>)\s*'
    r'<div\s+class="callout fun-note">\s*'
    r'<div\s+class="callout-title">[^<]+</div>\s*'
    r'(<details\s+class="bibliography-collapsible"[^>]*>)',
    re.DOTALL | re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')

    def repl(m: re.Match) -> str:
        # Close the whats-next div (drop the empty fun-note), then open bib
        return m.group(1) + '\n</div>\n' + m.group(2)

    new_text, n = BROKEN_RE.subn(repl, text)
    if n > 0:
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    for rel in TARGETS:
        p = ROOT / rel.replace('/', '\\') if sys.platform == 'win32' else ROOT / rel
        if not p.exists():
            print(f'  MISSING: {rel}')
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            print(f'  FIXED: {rel} ({n} repair)')
        else:
            print(f'  NO MATCH: {rel}')
    print(f'\nTotal fixes: {n_total}')


if __name__ == '__main__':
    main()
