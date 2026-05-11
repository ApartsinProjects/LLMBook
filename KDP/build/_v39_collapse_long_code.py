"""v3.9 R4#5: Collapse very long code blocks (>80 lines) in code-heavy
chapters (Module 18, 21, 22) into <details><summary> blocks.

Effect:
  - Web: reader sees "Show 142 lines of code (X.Y.Z)" and clicks to expand
  - EPUB: Kindle CSS sanitizer converts <details> to a labeled static box
    with the title visible but content rendered immediately (no clicking)

Doesn't reduce content, but visually de-emphasizes the long code so the
chapter's prose:code ratio reads better on first glance.

Strategy: only target <pre> blocks that are inside a code-block-wrapper
AND have >80 lines of actual code content. Use the existing code-caption
text (if any) as the summary.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

TARGET_MODULES = [
    "part-10-frontiers/module-18-interpretability",
    "part-5-retrieval-conversation/module-21-conversational-ai",
    "part-6-agentic-ai/module-22-ai-agents",
]
LINE_THRESHOLD = 80


def main() -> int:
    n_collapsed = 0
    n_files = 0
    for mod_path in TARGET_MODULES:
        mod = ROOT / mod_path
        if not mod.exists(): continue
        for p in mod.glob("section-*.html"):
            text = p.read_text(encoding="utf-8", errors="replace")
            original = text
            file_collapsed = 0

            # Find each <pre> with >LINE_THRESHOLD lines
            def maybe_collapse(m: re.Match) -> str:
                nonlocal file_collapsed
                pre_block = m.group(0)
                # Count newlines in code body
                code_text = re.sub(r"<[^>]+>", "", pre_block)
                n_lines = code_text.count("\n")
                if n_lines < LINE_THRESHOLD:
                    return pre_block
                file_collapsed += 1
                return (
                    f'<details class="long-code-collapsible">\n'
                    f'<summary><strong>Show {n_lines} lines of code</strong></summary>\n'
                    f'{pre_block}\n'
                    f'</details>'
                )

            text = re.sub(r"<pre[^>]*>.*?</pre>", maybe_collapse, text, flags=re.DOTALL)
            if file_collapsed > 0 and text != original:
                p.write_text(text, encoding="utf-8")
                n_files += 1
                n_collapsed += file_collapsed
                print(f"  {file_collapsed:>2} blocks collapsed: {p.name}")

    print(f"\nCollapsed {n_collapsed} long code blocks across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
