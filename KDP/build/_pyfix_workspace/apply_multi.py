"""Apply multi-target files by processing replacements in reverse line order
so earlier replacements don't shift later offsets.
"""
from __future__ import annotations
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from regen_block import regen

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
WORK = Path(__file__).parent

import ast

# (frag_num, relpath, original_line)
MULTI_TARGETS = [
    # section-37.4.html: lines 70 and 265
    ("11", "part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html", 70),
    ("12", "part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html", 265),
    # section-42.5.html: lines 142, 281, 362
    ("15", "part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html", 142),
    ("16", "part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html", 281),
    ("17", "part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html", 362),
    # section-66.1.html: lines 159, 395, 573, 703
    ("18", "part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html", 159),
    ("19", "part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html", 395),
    ("20", "part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html", 573),
    ("21", "part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html", 703),
]


PAT = re.compile(
    r'<pre><code class="pygments-highlighted lang-python">(.*?)</code></pre>',
    re.DOTALL,
)


def block_at_line(text: str, line_number: int) -> tuple[int, int]:
    """Find block that CONTAINS the given line number (1-indexed)."""
    line_starts = [0]
    for i, c in enumerate(text):
        if c == "\n":
            line_starts.append(i + 1)
    target_offset = line_starts[line_number - 1]
    nearest = None
    for m in PAT.finditer(text):
        s, e = m.span()
        if s <= target_offset <= e:
            return s, e
        # Distance from line start to nearest block edge
        d = min(abs(target_offset - s), abs(target_offset - e))
        if nearest is None or d < nearest[2]:
            nearest = (s, e, d)
    if nearest:
        return nearest[0], nearest[1]
    raise SystemExit(f"no block found near line {line_number}")


def main() -> None:
    # Group by file
    by_file: dict[str, list[tuple[str, int]]] = {}
    for num, relpath, ln in MULTI_TARGETS:
        by_file.setdefault(relpath, []).append((num, ln))
    for relpath, targets in by_file.items():
        # Sort by line DESCENDING so we replace from bottom up
        targets.sort(key=lambda x: -x[1])
        html_path = ROOT / relpath
        text = html_path.read_text(encoding="utf-8")
        for num, ln in targets:
            src = (WORK / f"frag_{num}.py").read_text(encoding="utf-8")
            ast.parse(src)
            s, e = block_at_line(text, ln)
            new_block = regen(src)
            text = text[:s] + new_block + text[e:]
            print(f"  {relpath}:{ln} frag_{num}.py -> offset {s} (replaced {e-s} bytes with {len(new_block)})")
        html_path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
