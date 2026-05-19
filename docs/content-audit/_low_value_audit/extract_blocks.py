"""Extract all <pre><code> blocks from section-*.html files and dump as JSONL.

For each code block we capture:
- file: absolute path
- line_no: 1-based line number where the block starts (first line of <pre>)
- lang: detected language class
- code: the raw inner code text (HTML-decoded)
- n_lines: number of lines in the code
- has_import: bool, code has any 'import ' statement
- has_def: bool, code has 'def ' or 'class '
- has_print: bool, code has 'print('
- has_assignment_only: heuristic boolean
- libs_used: list of library names imported
- surrounding: 200 chars of HTML before and after for context
"""
from __future__ import annotations
import json, re, os, sys, html
from pathlib import Path

SECTION_LIST = Path(__file__).parent / "section_files.txt"
OUT_JSONL = Path("E:/Projects/BookBlogsHome/LLMBook/docs/content-audit/_low_value_audit/code_blocks.jsonl")

PRE_BLOCK_RE = re.compile(
    r"<pre[^>]*>\s*<code\s+class=\"([^\"]*)\"[^>]*>(.*?)</code>\s*</pre>",
    re.DOTALL | re.IGNORECASE,
)

IMPORT_RE = re.compile(r"^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.]+))", re.MULTILINE)


def extract_blocks(html_path: Path):
    text = html_path.read_text(encoding="utf-8", errors="replace")
    line_offsets = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            line_offsets.append(i + 1)

    def char_to_line(pos: int) -> int:
        # binary search would be faster but list is small enough
        # we use upper_bound trick
        lo, hi = 0, len(line_offsets) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_offsets[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    out = []
    for m in PRE_BLOCK_RE.finditer(text):
        lang_class = m.group(1)
        code_raw = m.group(2)
        code = html.unescape(code_raw)
        start = m.start()
        line_no = char_to_line(start)
        # surrounding context window
        ctx_before = text[max(0, start - 500): start]
        ctx_after = text[m.end(): m.end() + 500]
        n_lines = code.count("\n") + 1 if code.strip() else 0
        imports = []
        for im in IMPORT_RE.finditer(code):
            imports.append(im.group(1) or im.group(2))
        has_import = bool(imports)
        has_def = bool(re.search(r"^\s*def\s+|^\s*class\s+", code, re.MULTILINE))
        has_print = "print(" in code
        # is this almost entirely @dataclass / class with fields?
        dataclass_only = bool(
            re.search(r"@dataclass", code) and not re.search(r"^\s*def\s+", code, re.MULTILINE)
        )
        # is it primarily dict / list literal?
        # treat as dict_like if >= 50% of non-empty lines look like key:value or string entries
        nonblank_lines = [ln.rstrip() for ln in code.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
        kvline = re.compile(r"^\s*['\"\w]+\s*[:=]\s*")
        kv_count = sum(1 for ln in nonblank_lines if kvline.match(ln))
        kv_ratio = kv_count / max(len(nonblank_lines), 1)

        # print-heavy: ratio of print(...) lines to total
        print_count = sum(1 for ln in nonblank_lines if "print(" in ln)
        print_ratio = print_count / max(len(nonblank_lines), 1)

        out.append({
            "file": str(html_path).replace("\\", "/"),
            "line_no": line_no,
            "lang_class": lang_class,
            "code": code,
            "n_lines": n_lines,
            "has_import": has_import,
            "imports": imports,
            "has_def": has_def,
            "has_print": has_print,
            "print_count": print_count,
            "print_ratio": print_ratio,
            "dataclass_only": dataclass_only,
            "kv_ratio": kv_ratio,
            "kv_count": kv_count,
            "nonblank_line_count": len(nonblank_lines),
            "ctx_before_tail": ctx_before[-300:],
            "ctx_after_head": ctx_after[:300],
        })
    return out


def main():
    paths = [Path(p.strip()) for p in SECTION_LIST.read_text().splitlines() if p.strip()]
    total = 0
    with OUT_JSONL.open("w", encoding="utf-8") as fout:
        for p in paths:
            try:
                blocks = extract_blocks(p)
            except Exception as e:
                print(f"ERROR {p}: {e}", file=sys.stderr)
                continue
            for b in blocks:
                fout.write(json.dumps(b, ensure_ascii=False) + "\n")
                total += 1
    print(f"Wrote {total} code blocks to {OUT_JSONL}")


if __name__ == "__main__":
    main()
