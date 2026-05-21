"""Wave 101b: Fix the extra </div> that wave 101 left behind.

Wave 101 reconstructed library-shortcut as `open_tag + body + </div>`
but body already included the closing </div> of the shortcut, so the
output has `</div></div>` right before the extracted block.

Idempotent fix: look for the doubled close that immediately precedes
the extracted block (a <div class="code-block-wrapper"> on the next
line) and collapse to a single </div>.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html",
    "part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.1.html",
    "part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html",
    "part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1a.html",
    "part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html",
    "part-2-understanding-llms/module-10-interpretability/section-10.1.html",
]

# Pattern: doubled </div> followed by a code-block-wrapper. Capture
# whitespace between them. Replace with single </div>.
DOUBLE_CLOSE_RE = re.compile(
    r'</div></div>(\s*)\n(\s*)<div\s+class="code-block-wrapper"',
    re.IGNORECASE,
)


def fix(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    new_text, n = DOUBLE_CLOSE_RE.subn(
        lambda m: f'</div>{m.group(1)}\n{m.group(2)}<div class="code-block-wrapper"',
        text,
    )
    if n:
        p.write_text(new_text, encoding="utf-8")
    return n


def main():
    total = 0
    for rel in TARGETS:
        p = ROOT / rel.replace("/", "\\")
        if not p.exists():
            print(f"  ! {rel}: not found")
            continue
        n = fix(p)
        if n:
            total += n
            print(f"  + {rel}: {n} double-close fixed")
        else:
            print(f"  = {rel}: no double-close (already clean?)")
    print(f"\nTotal: {total} fixes")


if __name__ == "__main__":
    main()
