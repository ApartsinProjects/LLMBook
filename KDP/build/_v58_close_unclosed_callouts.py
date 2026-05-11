"""v5.8+: Close unclosed callout div boxes.

Three files have an outer <div class="callout ..."> that is missing its
closing </div>. The next callout/heading/section then renders nested
inside the previous one in browsers that try to recover, or breaks
visually because the styled box never closes.

Affected files (per nested-box audit):
  - part-8-evaluation-production/module-29-evaluation-observability/section-29.9.html (11)
  - part-10-frontiers/module-18-interpretability/section-18.2.html (6)
  - part-4-training-adapting/module-15-peft/section-15.5.html (1)

Algorithm:
  Walk the HTML scanning <div .../> open and </div> close tokens. Track
  the open-div stack with class info. When we encounter a NEW <div> open
  whose class matches a callout flavor (callout XXX, but not callout-title)
  AND the same kind of callout is already open on the stack at top level,
  we insert a </div> RIGHT BEFORE the new opening tag and pop the old one.
  This effectively "auto-closes" the leaking callout.

We only fix top-level callout siblings to avoid breaking legitimate
inner structures (a <div class="callout-title"> child stays untouched).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Note: <div ...> opens and </div> closes. We only care about divs/asides.
TOK = re.compile(
    r'<(?P<close>/)?(?P<tag>div|aside)(?:\s+class="(?P<cls>[^"]*)")?[^>]*>',
    re.IGNORECASE,
)

CALLOUT_CLASSES = (
    'callout note', 'callout warning', 'callout tip', 'callout key-insight',
    'callout key-takeaway', 'callout big-picture', 'callout practical-example',
    'callout fun-note', 'callout exercise', 'callout self-check',
    'callout research-frontier', 'callout pathway', 'callout lab',
    'callout library-shortcut', 'callout prerequisites', 'callout objectives',
    'callout algorithm',
)


def is_callout_box(cls: str) -> bool:
    if 'callout-title' in cls: return False
    return 'callout' in cls


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    edits = []  # list of insertion points (offset, '</div>\n')
    stack = []  # list of (tag, is_callout)

    for m in TOK.finditer(text):
        is_close = bool(m.group('close'))
        tag = m.group('tag').lower()
        cls = (m.group('cls') or '').strip()
        is_co = is_callout_box(cls)

        if is_close:
            # Pop the matching tag
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][0] == tag:
                    stack.pop(j)
                    break
            continue

        # Opening tag
        # Are we opening a callout box while a callout is still on the stack?
        if is_co:
            # find topmost callout in stack
            outer_idx = None
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][1]:
                    outer_idx = j
                    break
            if outer_idx is not None:
                # Insert </div> right BEFORE this opening tag
                edits.append((m.start(), '</div>\n'))
                # Pop the outer callout from stack so the new one is top-level
                stack.pop(outer_idx)

        stack.append((tag, is_co))

    if not edits:
        return 0

    # Apply edits in reverse order to preserve offsets
    edits.sort(reverse=True)
    new_text = text
    for off, s in edits:
        new_text = new_text[:off] + s + new_text[off:]

    p.write_text(new_text, encoding="utf-8")
    return len(edits)


def main() -> int:
    targets = [
        ROOT / 'part-8-evaluation-production/module-29-evaluation-observability/section-29.9.html',
        ROOT / 'part-10-frontiers/module-18-interpretability/section-18.2.html',
        ROOT / 'part-4-training-adapting/module-15-peft/section-15.5.html',
    ]
    total = 0
    for p in targets:
        if not p.exists():
            print(f'  (missing) {p}')
            continue
        n = fix_file(p)
        if n:
            total += n
            print(f'  inserted {n} </div> in {p.relative_to(ROOT)}')
        else:
            print(f'  no fix needed: {p.relative_to(ROOT)}')

    print(f'\nTotal </div> inserts: {total}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
