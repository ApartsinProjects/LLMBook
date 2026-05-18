"""Wave 64: Renumber K.X.Y code-fragment refs in section-10.6 to 10.6.N.

The section moved from an older module-K structure but the captions and
in-prose references retained the K.X.Y prefix. Mapping:
  K.1.N → 10.6.N (N=1..6 → 1..6)
  K.2.N → 10.6.N (N=1..6 → 7..12)  (offset by previous run)
  K.3.N → 10.6.N (N=2..7 → 13..18)

Actually simpler: assign sequential 10.6.1 through 10.6.18 in order.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'part-2-understanding-llms' / 'module-10-interpretability' / 'section-10.6.html'


def main():
    t = PATH.read_text(encoding='utf-8')
    # Find every "Code Fragment K.X.Y" in order
    matches = list(re.finditer(r'Code Fragment K\.\d+\.\d+', t))
    if not matches:
        print('No K.X.Y patterns found')
        return

    # Build mapping: each unique K.X.Y → 10.6.N
    seen = []
    for m in matches:
        label = m.group()
        if label not in seen:
            seen.append(label)
    mapping = {old: f'Code Fragment 10.6.{i+1}' for i, old in enumerate(seen)}

    # Apply replacements globally
    new_text = t
    for old, new in mapping.items():
        new_text = new_text.replace(old, new)

    if new_text != t:
        PATH.write_text(new_text, encoding='utf-8')
        print(f'Renumbered {len(mapping)} unique labels:')
        for old, new in mapping.items():
            print(f'  {old} → {new}')


if __name__ == '__main__':
    main()
