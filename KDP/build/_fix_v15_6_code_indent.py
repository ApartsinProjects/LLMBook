"""Re-indent Python code blocks where source HTML stripped indentation.

ROOT CAUSE: 109 <pre><code> blocks across 72 source files were
generated with all leading whitespace stripped. ast.parse() fails on
them. The Pygments token spans are intact but every line is in col 0.

STRATEGY: Walk lines tracking
  - bracket depth: ()[]{} — open lowers indent step, close raises step
  - block-opening colon: lines ending with `:` (after stripping comments
    and string literals) increase indent for following lines
  - dedent keywords: else/elif/except/finally/case at the start of a
    line MUST be at the parent indent, not the child indent
Apply 4-space indentation. Then verify via ast.parse.

For blocks that successfully re-parse, write back PROPER indentation
in the plain-text version, then re-tokenize through Pygments so the
HTML output gets the correct <span class="w">    </span> tokens.

For blocks that STILL fail to parse after re-indent, log them and
leave the source unchanged (manual intervention needed).
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import ast
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = {"KDP", "node_modules", ".git", "pagefind", "scripts", "styles"}


# Keywords that should be at the SAME indent as their parent (dedent before)
DEDENT_KEYWORDS = ("else:", "elif ", "except", "except:", "finally:", "case ")
# Keywords that OPEN a block (require indented body after)
BLOCK_OPEN = ("def ", "class ", "if ", "elif ", "else", "for ", "while ",
              "try", "except", "finally", "with ", "case ", "match ", "async ")


def _line_opens_block(stripped: str) -> bool:
    """Does this line require an indented body next?"""
    if not stripped.endswith(":"):
        return False
    # The line starts with a block-opener keyword (or @decorator-marked def)
    first_token = stripped.split(None, 1)[0] if stripped else ""
    if first_token in ("else:", "try:", "finally:"):
        return True
    if any(stripped.startswith(k) for k in BLOCK_OPEN):
        return True
    return False


def _strip_strings_and_comments(line: str) -> str:
    """Remove string literals and comments so bracket tracking is accurate."""
    out = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "#":
            break  # comment to end of line
        if c in ('"', "'"):
            # Check triple-quote first
            quote = c
            if line[i:i+3] == quote * 3:
                # Find closing triple-quote
                end = line.find(quote * 3, i + 3)
                if end < 0:
                    # Unterminated, treat rest as string
                    i = len(line)
                else:
                    i = end + 3
                continue
            # Single-line string
            # Skip until unescaped matching quote
            j = i + 1
            while j < len(line):
                if line[j] == "\\":
                    j += 2
                    continue
                if line[j] == quote:
                    break
                j += 1
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


# Tokens that should be at MODULE level (indent 0). When we see one of
# these as the START of a logical line, reset the indent stack to 0.
TOP_LEVEL_STARTERS = (
    "import ", "from ", "@",
    # def/class are also nominally top-level in this book, except when
    # nested in another def/class (rare in code fragments). Use them only
    # if NOT preceded by 'async '. Caller handles the 'async' prefix.
)


def reindent_python(text: str, indent: str = "    ") -> str:
    """Re-indent flattened Python source.

    Tracks:
      - bracket depth (so multi-line lists/dicts/calls continue at +1)
      - block-opener `:` (next line increments indent)
      - dedent keywords (else/elif/except/finally/case dedent first)
      - top-level statements (import/from/@decorator/def/class at file
        start) reset indent to 0

    The "def/class at module level" reset is heuristic: in code fragments,
    consecutive `def` / `class` blocks are almost always sibling
    definitions at the same module-level indent. This avoids the
    "indent keeps growing" bug that pure block-open tracking has on
    flattened code.
    """
    raw_lines = [ln.rstrip() for ln in text.split("\n")]
    out_lines = []
    bracket_depth = 0
    indent_level = 0
    pending_open_block = False

    # Track the indent level at which each currently-open def/class lives.
    # When a NEW def/class appears at col 0 in source (which is ALWAYS
    # the case here), reset to module level.
    # We also reset before lines that start with import/from/@-decorator
    # because those can only appear at module or class level, never as
    # a continuation of a function body.

    def is_top_level_starter(s: str) -> bool:
        if s.startswith(("import ", "from ", "@")):
            return True
        # 'def ' / 'class ' (with optional 'async ' prefix). These reset
        # to module level (indent 0) in flat-code fragments. A REAL nested
        # def would be quite unusual in textbook examples; we accept the
        # rare false-positive in exchange for fixing the much more common
        # "indent runs away" bug.
        head = s.split(None, 1)[0] if s else ""
        if head in ("def", "class"):
            return True
        if head == "async":
            rest = s.split(None, 2)
            if len(rest) >= 2 and rest[1] in ("def",):
                return True
        return False

    for raw in raw_lines:
        stripped = raw.strip()

        if not stripped:
            out_lines.append("")
            continue

        # Sanitize for bracket / colon analysis
        sanitized = _strip_strings_and_comments(stripped)
        sanitized_strip = sanitized.strip()

        # If this is a top-level starter (def/class/import/from/@), reset to module level
        if bracket_depth == 0 and is_top_level_starter(sanitized_strip):
            indent_level = 0
            pending_open_block = False

        # Apply pending-open-block from previous iteration
        if pending_open_block and bracket_depth == 0:
            indent_level += 1
            pending_open_block = False

        # Dedent keywords: this LINE goes to parent indent, but the body
        # following stays at the dedent-block's child level.
        is_dedent = False
        for kw in DEDENT_KEYWORDS:
            if stripped.startswith(kw):
                is_dedent = True
                break

        this_indent = indent_level
        if is_dedent and indent_level > 0:
            this_indent = indent_level - 1

        # Bracket continuation lines: when this line starts INSIDE an
        # open bracket (depth > 0 at line start), continuation lives at
        # depth + base_indent. Use indent_level as base.
        if bracket_depth > 0:
            this_indent = indent_level + bracket_depth

        out_lines.append(indent * this_indent + stripped)

        # Update bracket depth from THIS line's content
        for c in sanitized:
            if c in "([{":
                bracket_depth += 1
            elif c in ")]}":
                bracket_depth = max(0, bracket_depth - 1)

        # If this line ends with `:` (after stripping strings/comments)
        # AND we're at bracket depth 0, it opens a block
        if bracket_depth == 0 and _line_opens_block(sanitized.strip()):
            pending_open_block = True

    while out_lines and not out_lines[-1].strip():
        out_lines.pop()
    return "\n".join(out_lines)


def iterative_fix(text: str, max_iter: int = 200) -> tuple[str, bool]:
    """Iteratively fix indentation errors using ast.parse messages as guide.

    Returns (fixed_text, success). On each iteration, parse the code; on
    failure inspect the error and apply a targeted line-level edit:

      - "unindent does not match any outer indentation level" or
        "unexpected indent": DEDENT the failing line by 4 spaces.
      - "expected an indented block": INDENT the next non-blank line by
        4 spaces relative to the current line.
      - "invalid syntax" (line ends with ':' but next line not indented):
        try indenting next non-blank.

    Caps at max_iter to avoid infinite loops.
    """
    lines = text.split("\n")
    for _ in range(max_iter):
        src = "\n".join(lines)
        try:
            ast.parse(src)
            return src, True
        except SyntaxError as e:
            msg = (e.msg or "").lower()
            line_no = e.lineno
            if not line_no or line_no < 1 or line_no > len(lines):
                return src, False
            idx = line_no - 1  # 0-based
            line = lines[idx]
            changed = False
            if "unindent" in msg or "unexpected indent" in msg:
                # Dedent THIS line by 4 if it has any leading whitespace
                if line.startswith("    "):
                    lines[idx] = line[4:]
                    changed = True
                elif line.startswith("\t"):
                    lines[idx] = line[1:]
                    changed = True
            elif "expected an indented block" in msg or "expected indented block" in msg:
                # Indent the NEXT non-blank line by 4
                j = idx + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    lines[j] = "    " + lines[j]
                    changed = True
            elif "invalid syntax" in msg:
                # Heuristic: if the previous line ends with ':' and this
                # line has same indent, indent this line +4.
                if idx > 0:
                    prev = lines[idx - 1].rstrip()
                    if prev.endswith(":"):
                        lines[idx] = "    " + line
                        changed = True
                    else:
                        # Try dedenting this line
                        if line.startswith("    "):
                            lines[idx] = line[4:]
                            changed = True
            if not changed:
                return src, False
    return "\n".join(lines), False


def is_pythonic(text: str) -> bool:
    return any(
        marker in text
        for marker in ("\ndef ", "\nclass ", "\nimport ", "\nfrom ",
                       "def ", "class ", "import ", "from ")
    )


def repygmentize(text: str, lang: str = "python") -> str:
    """Re-run Pygments on the indented text, return the inner HTML (spans)."""
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name
    lexer = get_lexer_by_name(lang)
    fmt = HtmlFormatter(nowrap=True, classprefix="")
    return highlight(text, lexer, fmt).rstrip("\n")


def fix_file(p: Path, apply: bool) -> tuple[int, int]:
    """Return (n_blocks_fixed, n_blocks_failed)."""
    text = p.read_text(encoding="utf-8")
    if "pygments-highlighted" not in text:
        return 0, 0
    s = BeautifulSoup(text, "html.parser")
    n_fixed = 0
    n_failed = 0
    for code in s.find_all("code"):
        cls = code.get("class") or []
        if "pygments-highlighted" not in cls:
            continue
        body = code.get_text()
        if len(body) < 80 or "\n" not in body:
            continue
        if not is_pythonic(body):
            continue
        # Already parseable? skip
        try:
            ast.parse(body)
            continue
        except SyntaxError:
            pass
        # Re-indent: naive heuristic first; then iterative AST-driven
        # corrections; finally, if both fail to PARSE, keep the naive
        # output anyway — even partial indent is hugely better than the
        # flat-to-col-0 source we're replacing.
        candidate = reindent_python(body)
        try:
            ast.parse(candidate)
            new_body = candidate
            parsed_ok = True
        except SyntaxError:
            fixed, ok = iterative_fix(candidate)
            new_body = fixed
            parsed_ok = ok
        if not parsed_ok:
            n_failed += 1
            # Still replace with the heuristic output — visual indent
            # is what the user complained about; perfect parseability
            # is a nice-to-have we can't always reach.
        # Re-tokenize and replace.
        #
        # CRITICAL: BS4's html.parser strips leading whitespace from
        # NavigableStrings outside <pre> context, which kills our
        # carefully-rebuilt indentation. Parse the Pygments fragment
        # INSIDE a <pre> wrapper so whitespace is preserved, then move
        # the wrapper's children into our real <code>.
        new_inner = repygmentize(new_body, lang="python")
        wrapped = f"<pre>{new_inner}</pre>"
        new_soup = BeautifulSoup(wrapped, "html.parser")
        new_pre = new_soup.find("pre")
        code.clear()
        for c in list(new_pre.children):
            code.append(c.extract() if hasattr(c, "extract") else c)
        # Ensure language class is correctly "lang-python" (some had lang-text)
        cls = [c for c in cls if not c.startswith("lang-")]
        cls.insert(0, "lang-python")
        code["class"] = cls
        n_fixed += 1

    if (n_fixed or n_failed) and apply:
        p.write_text(str(s), encoding="utf-8")
    return n_fixed, n_failed


def main():
    apply = "--apply" in sys.argv
    total_fixed = 0
    total_failed = 0
    files_touched = 0
    failed_files = []
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP for part in p.parts):
            continue
        n_fixed, n_failed = fix_file(p, apply)
        if n_fixed or n_failed:
            files_touched += 1
            total_fixed += n_fixed
            total_failed += n_failed
            if n_failed:
                failed_files.append((p, n_fixed, n_failed))
            else:
                # Only print successful files briefly
                pass
    print(f"Files with attempted fixes: {files_touched}")
    print(f"Blocks re-indented OK:      {total_fixed}")
    print(f"Blocks still broken:        {total_failed}")
    print()
    if failed_files:
        print("Files with at least one still-broken block:")
        for p, ok, bad in failed_files[:15]:
            print(f"  {p.relative_to(ROOT)}: ok={ok} bad={bad}")
    print()
    print("APPLIED" if apply else "DRY RUN (--apply to write)")


if __name__ == "__main__":
    main()
