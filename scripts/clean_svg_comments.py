"""Strip comments containing '--' (invalid XML) from an SVG. Also collapse them to safe forms."""
import re
import sys

def clean(path: str) -> None:
    text = open(path, "r", encoding="utf-8").read()
    # Remove comments that contain double-dash sequences inside their body.
    def fix_comment(m: re.Match) -> str:
        body = m.group(1)
        # Replace -- with em-dash text safely.
        body = body.replace("--", " ")
        return f"<!--{body}-->"
    text = re.sub(r"<!--(.*?)-->", fix_comment, text, flags=re.DOTALL)
    open(path, "w", encoding="utf-8").write(text)
    print(f"cleaned {path}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        clean(p)
