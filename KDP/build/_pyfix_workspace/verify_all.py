"""Re-extract each target's pygments block from the current HTML and try ast.parse."""
from __future__ import annotations
import sys
import ast
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_block import find_block, spans_to_text

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
WORK = Path(__file__).parent


def main() -> None:
    manifest = (WORK / "MANIFEST.tsv").read_text(encoding="utf-8").strip().splitlines()
    failures = []
    # Note: the originally-listed line numbers may no longer point to the
    # right block after replacement (lines shifted). So instead match every
    # python block in each file and try to parse it.
    seen_files = set()
    for line in manifest:
        parts = line.split("\t")
        relpath = parts[1]
        seen_files.add(relpath)
    import re
    pat = re.compile(r'<pre><code class="pygments-highlighted lang-python">(.*?)</code></pre>', re.DOTALL)
    for relpath in sorted(seen_files):
        text = (ROOT / relpath).read_text(encoding="utf-8")
        blocks = pat.findall(text)
        n_ok = n_fail = 0
        for i, b in enumerate(blocks):
            raw = spans_to_text(b)
            try:
                ast.parse(raw)
                n_ok += 1
            except SyntaxError as e:
                n_fail += 1
                failures.append((relpath, i, str(e)))
        print(f"  {relpath}: {n_ok}/{n_ok+n_fail} pythons parse")
    print()
    print(f"Total failures: {len(failures)}")
    for f in failures:
        print(f"  {f[0]} block#{f[1]}: {f[2]}")


if __name__ == "__main__":
    main()
