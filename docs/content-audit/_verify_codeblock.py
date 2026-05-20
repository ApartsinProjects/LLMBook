"""Extract a <pre><code> block from an HTML file by line range, strip the
Pygments span markup, unescape entities, and run ast.parse to confirm the
de-HTMLed Python parses. Usage:

    python _verify_codeblock.py <file> <start_line> <end_line>

start_line/end_line are 1-based and inclusive; they should bracket the lines
*between* (and not including) the <pre><code ...> opener and the </code></pre>
closer, OR include them (tags are stripped anyway).
"""
import sys
import re
import ast
import html


def strip_html(s: str) -> str:
    # remove all tags
    s = re.sub(r"<[^>]+>", "", s)
    # unescape &amp; &gt; &lt; &#36; etc.
    s = html.unescape(s)
    return s


def main():
    path = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    chunk = lines[start - 1 : end]
    # drop any line that is purely a pre/code open or close tag
    code_lines = []
    for ln in chunk:
        stripped_tagless = strip_html(ln).rstrip("\n")
        # skip the opener/closer lines if they de-HTML to empty
        if re.match(r"^\s*$", stripped_tagless) and ("<pre" in ln or "</code>" in ln or "<code" in ln):
            continue
        code_lines.append(stripped_tagless)
    code = "\n".join(code_lines)
    print("----- DE-HTMLed CODE -----")
    print(code)
    print("----- END -----")
    try:
        tree = ast.parse(code)
        print("AST_PARSE: OK")
        # Report top-level structure for a structural sanity check
        top = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                top.append(f"def {node.name}")
            elif isinstance(node, ast.ClassDef):
                methods = [m.name for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
                top.append(f"class {node.name} (methods inside: {methods})")
            elif isinstance(node, ast.Assign):
                tgt = node.targets[0]
                name = getattr(tgt, "id", None) or ast.dump(tgt)[:30]
                top.append(f"assign {name}")
            else:
                top.append(type(node).__name__)
        print("TOP-LEVEL:", top)
    except SyntaxError as e:
        print(f"AST_PARSE: FAIL line {e.lineno} col {e.offset}: {e.msg}")
        # show the offending line
        cl = code.split("\n")
        if e.lineno and 1 <= e.lineno <= len(cl):
            print("  >>> " + cl[e.lineno - 1])
        sys.exit(1)


if __name__ == "__main__":
    main()
