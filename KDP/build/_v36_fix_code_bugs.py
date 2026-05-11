"""v3.6 R5 P5: Fix specific code bugs identified in Round 5 deep-read.

1. section-22.4.html: every H2 numbered 22.5.x (file is 22.4) -> 22.4.x
2. section-22.4.html: f-string typo `total_{cost}/total` -> `total_cost/total`
3. section-17.2.html: `eval(...)` on JSON -> `json.loads(...)`
4. section-31.1.html: YAML block tagged `lang-python` -> `lang-yaml`
   (the docker-compose code block)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def fix_22_4() -> int:
    p = ROOT / "part-6-agentic-ai/module-22-ai-agents/section-22.4.html"
    text = p.read_text(encoding="utf-8", errors="replace")
    original = text
    # Renumber every 22.5.x (in H2/H3/Exercise/prose) to 22.4.x
    text, n_h = re.subn(r'(<h[2-4][^>]*>)22\.5\.(\d)', r'\g<1>22.4.\g<2>', text)
    text, n_ex = re.subn(r'\bExercise 22\.5\.', 'Exercise 22.4.', text)
    # Also catch standalone "22.5.X" mentions in prose (where prose said
    # "Section 22.5.3" or "as shown in 22.5.3")
    text, n_prose = re.subn(r'\b22\.5\.(\d)\b', r'22.4.\g<1>', text)
    # Subtract overlaps -- conservative not to double-count
    # f-string typo
    text, n_fs = re.subn(r'\$\{total_\{cost\}/total:\.3f\}',
                          '{total_cost/total:.3f}', text)
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"  22.4: H2/H3 renumbers={n_h}, Exercise={n_ex}, prose 22.5.X={n_prose}, f-string={n_fs}")
        return 1
    return 0


def fix_17_2() -> int:
    p = ROOT / "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html"
    text = p.read_text(encoding="utf-8", errors="replace")
    original = text
    # eval(result.choices[0].message.content) -> json.loads(...)
    text = re.sub(
        r'(judgment\s*=\s*)eval(\(\s*result\.choices\[0\]\.message\.content\))',
        r'\1json.loads\2',
        text,
    )
    # Make sure 'import json' appears before such usage. Easier: add a
    # comment line if eval was replaced.
    if text != original:
        # Insert "import json" right before the line if not present
        if "import json" not in text:
            text = re.sub(
                r'(<pre><code[^>]*>)([^<]*?json\.loads)',
                r'\1import json\n\2',
                text,
                count=1,
            )
        p.write_text(text, encoding="utf-8")
        print(f"  17.2: replaced eval() with json.loads()")
        return 1
    return 0


def fix_31_1() -> int:
    p = ROOT / "part-8-evaluation-production/module-31-production-engineering/section-31.1.html"
    text = p.read_text(encoding="utf-8", errors="replace")
    original = text
    # Find any <code class="...lang-python..."> block whose content starts
    # with a docker-compose YAML signature (version:, services:)
    n = 0

    def _maybe_swap(match: re.Match) -> str:
        nonlocal n
        full = match.group(0)
        body = match.group(2)
        # YAML signals
        if re.match(r"\s*(?:version:\s*['\"]?\d|services:|FROM\s)", body):
            new_open = re.sub(r"lang-python", "lang-yaml", match.group(1))
            n += 1
            return new_open + body + match.group(3)
        return full

    text = re.sub(
        r"(<code\s+[^>]*class=\"[^\"]*lang-python[^\"]*\"[^>]*>)(.*?)(</code>)",
        _maybe_swap,
        text,
        flags=re.DOTALL,
    )
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"  31.1: relabeled {n} YAML blocks from lang-python -> lang-yaml")
        return 1
    return 0


def main() -> int:
    print("Fixing R5 P5 code bugs:")
    fix_22_4()
    fix_17_2()
    fix_31_1()
    return 0


if __name__ == "__main__":
    sys.exit(main())
