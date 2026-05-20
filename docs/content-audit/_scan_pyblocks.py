"""Scan an HTML file for every Python <pre><code> block, de-HTML it, and run
ast.parse. Reports each block's opening line, PASS/FAIL, and (on pass) the
top-level node kinds so structural staircases (e.g. a def nested in a TypedDict)
are visible. Usage:  python _scan_pyblocks.py <file> [file2 ...]
"""
import sys
import re
import ast
import html

OPEN_RE = re.compile(r"<pre><code[^>]*\b(?:lang-python|language-python)\b")


def strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s)


def scan(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    i = 0
    n = len(lines)
    nblocks = 0
    nfail = 0
    while i < n:
        if OPEN_RE.search(lines[i]):
            start = i  # 0-based
            # find the closing </code></pre>
            j = i
            buf = []
            # the opener line may also contain code after the tag
            first = lines[i]
            # remove everything up to and including the opening code tag
            first_code = re.sub(r"^.*?<pre><code[^>]*>", "", first)
            if "</code></pre>" in first_code:
                first_code = first_code.split("</code></pre>")[0]
                buf.append(strip_html(first_code).rstrip("\n"))
                end = i
            else:
                buf.append(strip_html(first_code).rstrip("\n"))
                j = i + 1
                end = None
                while j < n:
                    if "</code></pre>" in lines[j]:
                        pre = lines[j].split("</code></pre>")[0]
                        buf.append(strip_html(pre).rstrip("\n"))
                        end = j
                        break
                    buf.append(strip_html(lines[j]).rstrip("\n"))
                    j += 1
            code = "\n".join(buf)
            nblocks += 1
            label = f"{path}:{start+1}"
            try:
                tree = ast.parse(code)
                top = []
                for node in tree.body:
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        top.append(f"def {node.name}")
                    elif isinstance(node, ast.ClassDef):
                        methods = [m.name for m in node.body
                                   if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
                        top.append(f"class {node.name}{methods if methods else ''}")
                    else:
                        top.append(type(node).__name__)
                print(f"PASS {label}  top={top}")
            except SyntaxError as e:
                nfail += 1
                print(f"FAIL {label}  line {e.lineno}: {e.msg}")
                cl = code.split("\n")
                if e.lineno and 1 <= e.lineno <= len(cl):
                    print(f"     >>> {cl[e.lineno-1]!r}")
            i = (end if end is not None else j) + 1
        else:
            i += 1
    return nblocks, nfail


def main():
    total = 0
    fails = 0
    for path in sys.argv[1:]:
        b, f = scan(path)
        total += b
        fails += f
    print(f"\nSUMMARY: {total} python blocks scanned, {fails} FAILED to parse")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
