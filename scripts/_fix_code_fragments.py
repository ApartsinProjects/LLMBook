"""
Deep audit-and-fix tool for code fragments in the LLMBook HTML pages.

Scans every `<pre><code class="...lang-python...">...</code></pre>` block in
the project's HTML files and fixes semantic indentation problems introduced
upstream by a build-pipeline regression. Most common breakage patterns:

  - over-indented cascade: code after the first def/class body got nested too
    deep, so `import`s, module-level dataclasses, demo `print` calls all live
    inside a previous class or function.
  - missing function body indent: `def foo():` with body lines at column 0,
    so the def has no body (IndentationError when parsed).
  - missing hanging indent in multi-line calls: `f(` followed by args at
    column 0 (or same indent as the call).
  - module-level statements ending up at column 4 or 8 because of a stray
    leading whitespace prefix on every line.

The script reconstructs corrected source text, validates with `ast.parse`,
re-highlights with pygments (`HtmlFormatter(nowrap=True, classprefix="")`),
and edits the HTML file in place. If the validated reconstruction does not
parse, the block is left untouched and flagged for human review.

For lang-bash / lang-sh / lang-json we only validate (no rewrite for bash,
JSON is parsed; we currently do not rewrite either).

Usage:
    python scripts/_fix_code_fragments.py            # dry run, prints report
    python scripts/_fix_code_fragments.py --write    # write fixes back
"""

from __future__ import annotations

import ast
import argparse
import html as html_mod
import io
import json
import re
import sys
import tokenize
import warnings

warnings.simplefilter("ignore", SyntaxWarning)
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")

EXCLUDE_PARTS = {"KDP", ".claude", "scripts", "node_modules", "vendor", "pagefind"}
EXCLUDE_PREFIXES = ("temp_",)
EXCLUDE_CONTAINS = ("backups",)


PRE_BLOCK_RE = re.compile(
    r'(<pre>\s*<code\b([^>]*)>)(.*?)(</code>\s*</pre>)',
    re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]+>")
CLASS_ATTR_RE = re.compile(r'class\s*=\s*"([^"]*)"', re.IGNORECASE)
LANG_RE = re.compile(r'(?:^|\s)(?:lang-|language-)([a-z0-9]+)')


PYTHON_LEXER = get_lexer_by_name("python")
PYGMENTS_FORMATTER = HtmlFormatter(nowrap=True, classprefix="")


# ---------------------------------------------------------------------------
# Helpers: language detection, source extraction, re-highlight
# ---------------------------------------------------------------------------

def detect_lang(class_attrs: str) -> str | None:
    """Return e.g. 'python', 'bash', 'json', or None if not found."""
    if not class_attrs:
        return None
    m = LANG_RE.search(class_attrs)
    if m:
        return m.group(1).lower()
    return None


def strip_html_to_source(inner: str) -> str:
    """Remove all <span>/<a>/etc tags and decode HTML entities."""
    plain = TAG_RE.sub("", inner)
    plain = html_mod.unescape(plain)
    return plain


def rehighlight_python(src: str) -> str:
    """Highlight Python source the way pygments did the original."""
    out = highlight(src, PYTHON_LEXER, PYGMENTS_FORMATTER)
    # pygments writes a trailing newline; the originals don't have one
    # between the last token and </code>.
    return out.rstrip("\n")


# ---------------------------------------------------------------------------
# Tokenization helper - we can tokenize a possibly-corrupt source by feeding
# it line by line, ignoring tokenize errors. Used to detect multi-line
# constructs.
# ---------------------------------------------------------------------------

def safe_tokenize(src: str):
    """Yield tokens until an error; ignore the rest."""
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            yield tok
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return


# ---------------------------------------------------------------------------
# The detection + fix routines
# ---------------------------------------------------------------------------


@dataclass
class FixResult:
    original: str
    fixed: str | None = None
    issues: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    parsed_before: bool = False
    parsed_after: bool = False
    applied: bool = False


def try_parse(src: str) -> tuple[bool, str | None]:
    try:
        ast.parse(src)
        return True, None
    except SyntaxError as e:
        return False, f"{type(e).__name__}: {e.msg} at line {e.lineno}"


def lines_with_indent(src: str) -> list[tuple[int, int, str]]:
    """Return (lineno, indent, line_text_no_indent_no_newline) for non-blank lines."""
    out = []
    for i, ln in enumerate(src.splitlines(), 1):
        stripped = ln.lstrip(" ")
        if not stripped:
            continue
        indent = len(ln) - len(stripped)
        out.append((i, indent, stripped.rstrip("\n")))
    return out


# ---------------------------------------------------------------------------
# Bracket-aware logical-statement walker
# ---------------------------------------------------------------------------


def split_logical_blocks(src: str) -> list[dict]:
    """
    Split the source into logical statements respecting bracket continuations.

    Each block is a dict with:
        - start_line (1-indexed)
        - end_line   (1-indexed, inclusive)
        - indent     (the indent of the opening line)
        - text       (raw text of the block, joined with \n, NO trailing \n)
        - decorators (lines preceding starting with '@' that should travel
                      with this block; merged into text by the caller)
    Comment-only/blank lines that fall between blocks are NOT consumed by
    this splitter; the caller decides which block they belong to.
    """
    lines = src.splitlines()
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        # eat blank/comment-only lines (still produce as standalone blocks)
        ln = lines[i]
        stripped = ln.strip()
        if stripped == "" or stripped.startswith("#"):
            blocks.append({
                "start_line": i + 1,
                "end_line": i + 1,
                "indent": len(ln) - len(ln.lstrip(" ")) if stripped else 0,
                "text": ln,
                "kind": "blank" if stripped == "" else "comment",
            })
            i += 1
            continue
        indent = len(ln) - len(ln.lstrip(" "))
        # collect continuation lines via bracket-depth and trailing backslash
        text_lines = [ln]
        depth = _bracket_delta(ln)
        in_triple = _triple_quote_open(ln, in_triple=False)
        backslash = ln.rstrip().endswith("\\")
        j = i + 1
        while j < n and (depth > 0 or backslash or in_triple):
            nxt = lines[j]
            text_lines.append(nxt)
            if in_triple:
                in_triple = _triple_quote_open(nxt, in_triple=True)
            else:
                in_triple = _triple_quote_open(nxt, in_triple=False)
                depth += _bracket_delta(nxt)
                depth = max(depth, 0)
                backslash = nxt.rstrip().endswith("\\") and not in_triple
            j += 1
        blocks.append({
            "start_line": i + 1,
            "end_line": j,
            "indent": indent,
            "text": "\n".join(text_lines),
            "kind": "stmt",
        })
        i = j
    return blocks


def _bracket_delta(line: str) -> int:
    """How much does this line change bracket depth, ignoring strings?"""
    depth = 0
    in_str = None
    i = 0
    while i < len(line):
        c = line[i]
        if in_str:
            if c == "\\":
                i += 2
                continue
            if c == in_str:
                in_str = None
            i += 1
            continue
        if c in ("'", '"'):
            # triple?
            if line[i : i + 3] in ('"""', "'''"):
                # search end on same line
                end = line.find(line[i : i + 3], i + 3)
                if end == -1:
                    return depth  # triple opens; signal "in_triple" via caller
                i = end + 3
                continue
            in_str = c
            i += 1
            continue
        if c == "#":
            break
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        i += 1
    return depth


def _triple_quote_open(line: str, in_triple: bool) -> bool:
    """Return whether a triple-quote remains open after this line."""
    # Very rough: count unescaped triple-quotes
    # If already in_triple, look for closing one.
    # We don't distinguish ''' vs """ separately for robustness.
    state = in_triple
    i = 0
    while i < len(line):
        if not state and line[i : i + 3] in ('"""', "'''"):
            # opens
            quote = line[i : i + 3]
            end = line.find(quote, i + 3)
            if end == -1:
                return True
            i = end + 3
            continue
        if state and line[i : i + 3] in ('"""', "'''"):
            state = False
            i += 3
            continue
        if not state and line[i] in ('"', "'"):
            # skip single-line string
            q = line[i]
            i += 1
            while i < len(line) and line[i] != q:
                if line[i] == "\\":
                    i += 2
                    continue
                i += 1
            i += 1
            continue
        if not state and line[i] == "#":
            break
        i += 1
    return state


# ---------------------------------------------------------------------------
# Heuristics
# ---------------------------------------------------------------------------


def _starts_with(stripped_first: str, *prefixes: str) -> bool:
    return any(stripped_first.startswith(p) for p in prefixes)


def is_module_level_ish(text: str) -> bool:
    """
    Decide whether a logical block 'wants' to live at module level (indent 0).

    Conservative: only return True when very confident.
    """
    first = text.lstrip().splitlines()[0] if text.strip() else ""
    if not first:
        return False
    # imports
    if first.startswith("import ") or first.startswith("from "):
        return True
    # if __name__ ==
    if first.startswith("if __name__"):
        return True
    return False


def looks_like_demo(text: str) -> bool:
    """A logical block that looks like demo/usage code."""
    first = text.lstrip().splitlines()[0] if text.strip() else ""
    if first.startswith("print("):
        return True
    if first.startswith("if __name__"):
        return True
    return False


# ---------------------------------------------------------------------------
# Main fix engine: try to flatten an over-indented cascade
# ---------------------------------------------------------------------------


def fix_python_source(src: str) -> FixResult:
    res = FixResult(original=src)
    ok, err = try_parse(src)
    res.parsed_before = ok
    if ok:
        issues = structural_issues(src)
        if not issues:
            # Even fully parsing code can still have missing hanging indent.
            # Try ONLY the hanging-indent repair; if it doesn't change a thing,
            # leave it alone.
            hi_cand, hi_note = repair_missing_hanging_indent(src)
            if hi_cand is not None and hi_cand != src:
                ok2, _ = try_parse(hi_cand)
                if ok2:
                    res.fixed = hi_cand
                    res.parsed_after = True
                    res.applied = True
                    res.notes.append(hi_note)
            return res
        res.issues.extend(issues)
    else:
        res.issues.append(f"parse_fail: {err}")

    # Try a sequence of repair strategies in order.
    # Each strategy is given a chance; we keep the result that produces the
    # CLEANEST AST (parses + no structural issues).
    strategies = [
        repair_summary_print_denest,
        repair_overindent_cascade_v2,
        repair_missing_body_indent,
        repair_missing_hanging_indent,
    ]

    candidate = src
    best = src
    best_score = _score(src)
    for strat in strategies:
        new_candidate, note = strat(candidate)
        if new_candidate is None or new_candidate == candidate:
            continue
        ok2, err2 = try_parse(new_candidate)
        sc = _score(new_candidate) if ok2 else (1e9,)
        if ok2 and sc < best_score:
            best = new_candidate
            best_score = sc
            res.notes.append(note)
        # always chain on the new candidate for next strategy (compose)
        candidate = new_candidate

    # Final candidate: the chained one if it parses cleanly with no issues.
    ok3, _ = try_parse(candidate)
    if ok3:
        sc = _score(candidate)
        if sc < best_score:
            best = candidate
            best_score = sc

    # Apply policy:
    #   - apply if best_score is strictly lower than original AND best does
    #     not introduce any HIGH-severity issue (stranded-method,
    #     return-at-module-level, import-nested-in-class) that wasn't in the
    #     original.
    original_score = _score(src)
    if best is not src and best_score < original_score:
        best_issues = structural_issues(best) if not isinstance(best, type(None)) else []
        orig_issues = structural_issues(src)
        orig_cats = {iss.split(":", 1)[0].split(" ", 1)[0] for iss in orig_issues}
        best_cats = {iss.split(":", 1)[0].split(" ", 1)[0] for iss in best_issues}
        # Don't apply if we INTRODUCED a high-severity issue.
        high_sev = {"stranded-method", "return-at-module-level",
                    "import-nested-in-class", "def-body-only-docstring",
                    "yield-or-await-at-module-level"}
        new_high = (best_cats - orig_cats) & high_sev
        if new_high:
            res.notes.append(f"refusing_due_to_new_high_severity:{new_high}")
        else:
            res.fixed = best
            res.parsed_after = True
            res.applied = True
    else:
        res.parsed_after = ok3
        if ok3 and best_score < original_score:
            res.notes.append("partial_improvement_not_applied")
    return res


_SEVERITY_WEIGHTS = {
    # Don't-apply-this-fix-it's-worse issues (heavy penalty)
    "stranded-method": 10,
    "import-nested-in-class": 5,
    "return-at-module-level": 5,
    "def-body-only-docstring": 4,
    "nested-dataclass-class": 3,
    "yield-or-await-at-module-level": 5,
    # Soft issues - existed before, no urgent need to "fix"
    "dead-code-after-return": 2,
    "class-cascade-suspicious": 3,
    "summary-print-nested-deep": 2,
    # Vague signals - moderate weight (severe cascade in original)
    "cascade-depth": 3,
}


def _score(src: str) -> tuple:
    """Lower is better. (weighted_issues, count, len_diff_from_src)."""
    try:
        ast.parse(src)
    except SyntaxError:
        return (1e9, 0, 0)
    issues = structural_issues(src)
    weighted = 0
    for iss in issues:
        cat = iss.split(":", 1)[0].split(" ", 1)[0]
        # Cascade depth is weighted by the depth level (deeper = worse).
        m_cd = re.match(r"cascade-depth-(\d+)", cat)
        if m_cd:
            depth = int(m_cd.group(1))
            # 24 -> 3, 28 -> 4, 32 -> 5, 36 -> 6, 40 -> 7, etc.
            weighted += max(3, (depth - 16) // 4)
            continue
        weighted += _SEVERITY_WEIGHTS.get(cat, 2)
    return (weighted, len(issues), 0)


# --- structural checks -----------------------------------------------------


def structural_issues(src: str) -> list[str]:
    """Look for non-syntactic semantic problems in already-parsing code."""
    issues = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return ["unparseable"]

    # Walk top-level body
    body = tree.body
    # 0. Module-level Return / Yield / Await are syntactically invalid (they
    #    compile-fail but ast.parse accepts).
    for node in tree.body:
        if isinstance(node, ast.Return):
            issues.append(f"return-at-module-level at line {node.lineno}")
        if isinstance(node, ast.Expr) and isinstance(node.value, (ast.Yield, ast.YieldFrom, ast.Await)):
            issues.append(f"yield-or-await-at-module-level at line {node.lineno}")
    # 0b. Function with no body OTHER than a docstring (likely missing
    #     indent body). Detect: a FunctionDef whose body is exactly one
    #     Expr(Constant(str)).
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if (
                len(node.body) == 1
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                # docstring only - suspicious if there's a stray Return at
                # module level just after.
                # We've already detected module-level Return separately.
                issues.append(f"def-body-only-docstring:{node.name} at line {node.lineno}")
    # 0c. Top-level functions whose first parameter is `self` or `cls`
    # (almost certainly a stranded method that should be inside a class).
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.args.args and node.args.args[0].arg in ("self", "cls"):
                issues.append(
                    f"stranded-method:{node.name} at line {node.lineno}"
                )
    # 1. Are there imports nested deeper than module level?
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # find enclosing scope: easiest is to check if it's in tree.body
            if not _is_in_module_body(node, tree):
                # imports inside functions are legal, but the corruption pattern
                # is imports nested inside an unrelated class body.
                parent = _find_enclosing_class(node, tree)
                if parent is not None:
                    issues.append(
                        f"import-nested-in-class:{getattr(parent,'name','?')} at line {node.lineno}"
                    )
    # 2. Are there demo-print loops inside a function after a return?
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef):
            saw_return = False
            for st in fn.body:
                if saw_return:
                    issues.append(
                        f"dead-code-after-return in {fn.name} at line {st.lineno}"
                    )
                    break
                if isinstance(st, ast.Return):
                    saw_return = True
    # 3. Class body containing assignments that look like module-level dicts
    #    plus another @dataclass class (the cascade signature).
    for cls in ast.walk(tree):
        if isinstance(cls, ast.ClassDef):
            # Inside the class body, look for inner class with decorator and a
            # def after it - classic 35.1.1 over-indent cascade.
            has_assign_then_class = False
            assigns = [s for s in cls.body if isinstance(s, ast.Assign)]
            inner_cls = [s for s in cls.body if isinstance(s, ast.ClassDef)]
            inner_fn = [s for s in cls.body if isinstance(s, ast.FunctionDef)]
            if assigns and inner_cls and inner_fn:
                issues.append(
                    f"class-cascade-suspicious in {cls.name} at line {cls.lineno}"
                )
            # Nested class with @dataclass decorator - virtually never
            # intentional in this book.
            for sub in cls.body:
                if isinstance(sub, ast.ClassDef):
                    for dec in sub.decorator_list:
                        n = (
                            dec.id if isinstance(dec, ast.Name)
                            else (dec.attr if isinstance(dec, ast.Attribute) else None)
                        )
                        # Also catch @dataclass() call form
                        if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                            n = dec.func.id
                        if n in ("dataclass",):
                            issues.append(
                                f"nested-dataclass-class:{sub.name}-in-{cls.name} at line {sub.lineno}"
                            )
    # 3b. Cascade depth signal: maximum indent of a *code* (non-docstring,
    # non-blank) line. We approximate by skipping lines that fall inside a
    # multi-line string. To estimate "inside-string" we use ast.walk and
    # find string-constant nodes that span line ranges.
    string_line_ranges = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            sl = getattr(n, "lineno", None)
            el = getattr(n, "end_lineno", sl)
            if sl is not None and el is not None and el > sl:
                # multi-line string: lines from sl+1 to el (exclusive of opener)
                for ln in range(sl, el + 1):
                    string_line_ranges.add(ln)
    max_indent = 0
    for i, line in enumerate(src.splitlines(), 1):
        if i in string_line_ranges:
            continue
        if line.strip() == "":
            continue
        ind = len(line) - len(line.lstrip(" "))
        if ind > max_indent:
            max_indent = ind
    n_defs_classes = sum(1 for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef)))
    if max_indent >= 24 and n_defs_classes >= 2:
        issues.append(f"cascade-depth-{max_indent}-with-{n_defs_classes}-defs")
    # 4. Demo-summary print detection: a `print(f"\n\n...")` deeply nested
    #    inside an `if` block followed by NOTHING at outer scope, when the
    #    f-string uses a variable accumulated through an enclosing loop.
    #    Heuristic: a print whose first f-string arg starts with \n\n is
    #    likely a post-loop summary line. If it lives more than 4 spaces
    #    deep, and no module-level "summary" line exists, flag it.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Expr):
            continue
        call = node.value
        if not isinstance(call, ast.Call):
            continue
        if not (isinstance(call.func, ast.Name) and call.func.id == "print"):
            continue
        if not call.args:
            continue
        a0 = call.args[0]
        # Look for f-string starting with literal \n\n
        starts_double_nl = False
        if isinstance(a0, ast.JoinedStr):
            if a0.values and isinstance(a0.values[0], ast.Constant) and isinstance(a0.values[0].value, str):
                if a0.values[0].value.startswith("\n\n"):
                    starts_double_nl = True
        elif isinstance(a0, ast.Constant) and isinstance(a0.value, str):
            if a0.value.startswith("\n\n"):
                starts_double_nl = True
        if not starts_double_nl:
            continue
        # Check the indent of this stmt in the source.
        src_line = node.lineno
        line_text = src.splitlines()[src_line - 1] if src_line <= len(src.splitlines()) else ""
        ind = len(line_text) - len(line_text.lstrip(" "))
        if ind >= 4:
            issues.append(
                f"summary-print-nested-deep at line {src_line} (indent={ind})"
            )
    return issues


def _is_in_module_body(target, tree) -> bool:
    return any(node is target for node in tree.body)


def _find_enclosing_class(target, tree):
    """Walk to find a class whose body transitively contains target."""
    candidates = [tree]
    while candidates:
        cur = candidates.pop()
        children = list(ast.iter_child_nodes(cur))
        for ch in children:
            if ch is target and isinstance(cur, ast.ClassDef):
                return cur
            candidates.append(ch)
    return None


# ---------------------------------------------------------------------------
# Repair strategies
# ---------------------------------------------------------------------------


def repair_summary_print_denest(src: str) -> tuple[str | None, str]:
    """
    Find `print(f"\\n\\n...")` lines deeply nested inside if/for/while and
    move them to module level (col 0).
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None, "parse_fail"
    lines = src.splitlines()
    line_shift = [0] * (len(lines) + 2)
    changed = False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Expr):
            continue
        call = node.value
        if not isinstance(call, ast.Call):
            continue
        if not (isinstance(call.func, ast.Name) and call.func.id == "print"):
            continue
        if not call.args:
            continue
        a0 = call.args[0]
        starts_dnl = False
        if isinstance(a0, ast.JoinedStr):
            if a0.values and isinstance(a0.values[0], ast.Constant) and isinstance(a0.values[0].value, str):
                if a0.values[0].value.startswith("\n\n"):
                    starts_dnl = True
        elif isinstance(a0, ast.Constant) and isinstance(a0.value, str):
            if a0.value.startswith("\n\n"):
                starts_dnl = True
        if not starts_dnl:
            continue
        # Find the line range covered by this Expr.
        s_ln = node.lineno
        e_ln = getattr(node, "end_lineno", s_ln)
        # Compute its current indent.
        line_text = lines[s_ln - 1]
        ind = len(line_text) - len(line_text.lstrip(" "))
        if ind < 4:
            continue
        # Force to indent 0.
        sh = -ind
        for ln in range(s_ln, e_ln + 1):
            line_shift[ln] = sh
        changed = True
    if not changed:
        return None, "no_summary_prints"
    new_lines = []
    for i, ln in enumerate(lines, 1):
        sh = line_shift[i]
        if sh < 0 and ln.strip() != "":
            removable = len(ln) - len(ln.lstrip(" "))
            actual = min(removable, -sh)
            new_lines.append(ln[actual:])
        else:
            new_lines.append(ln)
    return "\n".join(new_lines), "summary_print_denested"


def repair_overindent_cascade_v2(src: str) -> tuple[str | None, str]:
    """
    Brute-force cascade fixer.

    Strategy:
      1. Identify candidate "cut points" - line numbers where the cascade
         transitions from legitimate nesting into spurious nesting.
      2. For each cut point, try dedenting EVERY line from that point to the
         end of the source by N spaces (for N in {4, 8, 12, ..., max_indent}).
      3. Score each candidate by:
            - parses cleanly
            - structural_issues count
            - the dedent puts module-level signals (imports, demo prints) at col 0
      4. Pick the lowest-score candidate that beats the original.

    This is intentionally pragmatic; we don't try to be precisely correct,
    we try to be MEASURABLY better than the original.
    """
    blocks = split_logical_blocks(src)
    stmts = [b for b in blocks if b["kind"] == "stmt"]
    if len(stmts) < 3:
        return None, "too_few_statements"

    # Find candidate cut lines: lines where indent JUMPED upward without a
    # block-opening directly preceding it, OR lines that look like they should
    # be at module level (imports, decorators, demo prints) but live deeper.
    candidates: list[int] = []
    indents = [s["indent"] for s in stmts]
    for i, s in enumerate(stmts):
        first = s["text"].lstrip().splitlines()[0].lstrip()
        if i > 0:
            prev = stmts[i - 1]
            prev_first = prev["text"].lstrip().splitlines()[0].lstrip()
            # If indent jumped by 4 but previous statement doesn't end with ':'
            if s["indent"] > prev["indent"] and not _stmt_opens_block(prev["text"]):
                candidates.append(s["start_line"])
        # Strong anchor signals deeper than 0
        if s["indent"] > 0:
            if first.startswith(("from ", "import ", "if __name__")):
                candidates.append(s["start_line"])
            elif first.startswith("@dataclass"):
                # if there's a sibling @dataclass earlier at indent 0,
                # this one likely belongs at 0 too.
                for s2 in stmts[:i]:
                    f2 = s2["text"].lstrip().splitlines()[0].lstrip()
                    if s2["indent"] == 0 and f2.startswith("@dataclass"):
                        candidates.append(s["start_line"])
                        break

    if not candidates:
        # Whole-source dedent might fix it: try dedenting everything by the
        # MIN non-zero indent.
        min_indent = min(s["indent"] for s in stmts if s["indent"] > 0) if any(s["indent"] > 0 for s in stmts) else 0
        if min_indent:
            candidates.append(stmts[0]["start_line"])

    # Additional heuristic candidates: every statement whose first token is
    # `def`, `class`, `@`, `import`, `from`, `if __name__`, AND whose CURRENT
    # indent could plausibly be at module level (i.e., > 0).
    for s in stmts:
        f0 = s["text"].lstrip().splitlines()[0].lstrip()
        if s["indent"] > 0 and f0.startswith(("def ", "class ", "@", "import ", "from ", "if __name__")):
            candidates.append(s["start_line"])
        # ALL_CAPS assignment is a strong module-level signal
        if s["indent"] > 0:
            m = re.match(r"([A-Z_][A-Z0-9_]*)\s*=\s*[\[\{\(]", f0)
            if m:
                candidates.append(s["start_line"])

    candidates = sorted(set(candidates))
    if not candidates:
        return None, "no_cut_candidates"

    original_score = _score(src)

    best = src
    best_score = original_score
    best_note = ""

    # For each candidate cut, try dedenting everything from that line to end.
    # Also try compound dedents: cut + apply increasing dedent amounts.
    max_indent = max(s["indent"] for s in stmts)
    dedent_amounts = sorted({4, 8, 12, 16, max_indent, max_indent - 4, max_indent - 8} - {0, -4, -8})
    dedent_amounts = [a for a in dedent_amounts if a > 0]

    for cut in candidates:
        # Also try: dedent the entire suffix to exactly `cut`'s indent (so cut
        # lands at 0).
        cut_stmt = next((s for s in stmts if s["start_line"] == cut), None)
        if cut_stmt is not None:
            target_dedent = cut_stmt["indent"]
            if target_dedent > 0 and target_dedent not in dedent_amounts:
                dedent_amounts_local = sorted(set(dedent_amounts + [target_dedent]))
            else:
                dedent_amounts_local = dedent_amounts
        else:
            dedent_amounts_local = dedent_amounts
        for amt in dedent_amounts_local:
            cand = _dedent_from_line(src, cut, amt)
            if cand is None:
                continue
            try:
                ast.parse(cand)
            except SyntaxError:
                continue
            sc = _score(cand)
            # require at least no structural issues OR strictly better than original
            if sc < best_score:
                best = cand
                best_score = sc
                best_note = f"cut@{cut}_dedent_{amt}"

    # Cascade-aware stack-based reflow (the strong intervention).
    re_flow = _cascade_aware_reflow(src)
    if re_flow is not None and re_flow != src:
        try:
            ast.parse(re_flow)
            sc = _score(re_flow)
            if sc < best_score:
                best = re_flow
                best_score = sc
                best_note = "cascade_aware_reflow"
        except SyntaxError:
            pass

    # Also try the simpler force-anchors heuristic as a fallback.
    re_flow2 = _force_module_anchors(src)
    if re_flow2 is not None and re_flow2 != src:
        try:
            ast.parse(re_flow2)
            sc = _score(re_flow2)
            if sc < best_score:
                best = re_flow2
                best_score = sc
                best_note = "module_anchors_forced"
        except SyntaxError:
            pass

    if best is src:
        return None, "no_improvement_found"
    return best, best_note


def _dedent_from_line(src: str, cut_line: int, amount: int) -> str | None:
    """Dedent lines [cut_line..end] by `amount` spaces (clamped at 0)."""
    lines = src.splitlines()
    out = []
    for i, ln in enumerate(lines, 1):
        if i < cut_line:
            out.append(ln)
            continue
        if ln.strip() == "":
            out.append(ln)
            continue
        cur = len(ln) - len(ln.lstrip(" "))
        new_indent = max(0, cur - amount)
        out.append(" " * new_indent + ln.lstrip(" "))
    return "\n".join(out)


_TERMINAL_RE = re.compile(r"^(return|raise|break|continue)\b")


def _is_terminal_stmt(first_line: str) -> bool:
    return bool(_TERMINAL_RE.match(first_line))


def _cascade_aware_reflow(src: str) -> str | None:
    """
    Walk statements top-down. Maintain a stack of `(indent, kind)` where `kind`
    is in {'class', 'def', 'flow'} (flow = if/for/while/try/with).

    For each statement, compute its INTENDED indent based on:
      - Where in the stack we should be (semantically determined from the
        statement's role).
      - Whether the previous statement opened a block.

    Module-level anchors (import, from, if __name__) always RESET the stack
    to empty and land at indent 0.

    Strong "should be sibling" signals:
      - A `@decorator` followed by a `class` or `def`: the (decorator, def)
        pair should be at the SAME indent as the previous top-level def/class
        that started a similar "group".
      - An ALL_CAPS_ASSIGN at deeper-than-zero indent: ALWAYS module level.
      - A `print(...)` not contained in a function (heuristic: if the
        previous top-level def with same indent is "complete", then this
        print is module-level).

    The function returns the reflowed source or None if it could not produce
    a CHANGED string.
    """
    blocks = split_logical_blocks(src)
    stmts = [b for b in blocks if b["kind"] == "stmt"]
    if not stmts:
        return None

    plan: list[int] = []  # intended indent per stmt index (stmts order)
    stack: list[tuple[int, str]] = []  # (intended indent of block opener, kind)

    # Heuristic: detect "demo block markers" in the source text. If we see a
    # standalone comment line like `# Example`, `# Usage`, `# Demo`, etc., the
    # NEXT statement is module-level (regardless of stack state). Build a set
    # of stmt line numbers that should be forced to module level.
    force_module_lines: set[int] = set()
    src_lines = src.splitlines()
    DEMO_COMMENT_RE = re.compile(
        r"^\s*#\s*(?:"
        r"Example(?:s)?(?:[:.]|\b)|"
        r"Usage(?:[:.]|\b)|"
        r"Demo(?:[:.]|\b)|"
        r"Try\s+it(?:[:.]|\b)|"
        r"Sample\s+output|"
        r"If\s+__name__|"
        r"Test\b|"
        r"Run\b|"
        r"Quick\s+test|"
        r"Red\s+team|"
        r"Smoke\s+test"
        r")",
        re.IGNORECASE,
    )
    for li, ln_text in enumerate(src_lines, 1):
        if DEMO_COMMENT_RE.match(ln_text):
            # Find next non-blank, non-comment line.
            for li2 in range(li + 1, len(src_lines) + 1):
                t2 = src_lines[li2 - 1]
                if t2.strip() == "" or t2.lstrip().startswith("#"):
                    continue
                force_module_lines.add(li2)
                break

    # Pre-compute: list of names defined as `def NAME(...)` or `class NAME(...)`
    # at any level in the source. Used to detect "calls to user-defined
    # function" as a demo signal.
    defined_names: set[str] = set()
    for ln in src_lines:
        m_d = re.match(r"\s*(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)", ln)
        if m_d:
            defined_names.add(m_d.group(1))
        m_c = re.match(r"\s*class\s+([A-Za-z_][A-Za-z0-9_]*)", ln)
        if m_c:
            defined_names.add(m_c.group(1))

    def push_block(target_indent: int, kind: str):
        stack.append((target_indent, kind))

    def current_inside_body_indent() -> int:
        """Where should a 'body' statement go, given the stack?"""
        if not stack:
            return 0
        return stack[-1][0] + 4

    for i, s in enumerate(stmts):
        first = s["text"].lstrip().splitlines()[0].lstrip()
        opens = _stmt_opens_block(s["text"])

        # ---- Force module level if preceded by a "# Example"-style comment ----
        if s["start_line"] in force_module_lines:
            stack.clear()
            target = 0
            s["planned_indent"] = target
            plan.append(target)
            if opens:
                push_block(target, "flow")
            continue

        # ---- Anchor: imports & top-level guard ----
        # Imports and `if __name__` are almost always at module level. But
        # lazy/local imports inside functions are legal Python and used
        # sometimes. Heuristic: if we are inside a def AND the PREVIOUS
        # statement was also inside this same function (the def is the
        # top-of-stack and we just placed something at body_indent), treat
        # this import as a function-local import.
        if first.startswith(("import ", "from ", "if __name__")):
            inside_def = stack and stack[-1][1] == "def"
            # Was the previous stmt placed at the body indent of this def?
            prev_inside = False
            if inside_def and plan:
                prev_target = plan[-1]
                expected_body = stack[-1][0] + 4
                if prev_target == expected_body:
                    prev_inside = True
            if inside_def and prev_inside:
                # Function-local import.
                target = current_inside_body_indent()
            else:
                stack.clear()
                target = 0
            plan.append(target)
            if opens:
                push_block(target, "flow")
            continue

        # ---- ALL_CAPS module constant assignment ----
        if re.match(r"[A-Z_][A-Z0-9_]*\s*[:=]", first):
            # If the current "expected" body indent is INSIDE a class, this
            # could be a legitimate class attribute. Distinguish:
            #   - If the stack top is a class and the value side references
            #     the class's own name, it's actually a cascade (should be
            #     module level).
            #   - Otherwise treat as class attribute.
            value_part = first.split("=", 1)[1] if "=" in first else ""
            current_class = None
            for st_ind, st_kind in reversed(stack):
                if st_kind == "class":
                    current_class = st_ind
                    break
            class_name_ref = None
            if current_class is not None:
                # Find the class name from stmts: find the most recent class
                # stmt at indent current_class.
                for prior in reversed(stmts[:i]):
                    if prior.get("planned_indent") == current_class and prior["text"].lstrip().startswith("class "):
                        m = re.match(r"class\s+([A-Za-z_][A-Za-z0-9_]*)", prior["text"].lstrip())
                        if m:
                            class_name_ref = m.group(1)
                            break
                # Also look in the full block text (multi-line) of the class
                # opener.
                if class_name_ref is None:
                    # fall back: scan upward stmts for any "class Name:" stmt
                    for prior in reversed(stmts[:i]):
                        pt = prior["text"].lstrip().splitlines()[0].lstrip()
                        m = re.match(r"class\s+([A-Za-z_][A-Za-z0-9_]*)", pt)
                        if m:
                            class_name_ref = m.group(1)
                            break
            if class_name_ref and class_name_ref in s["text"]:
                # Cascade: this assignment references the enclosing class.
                # Must be module-level.
                stack.clear()
                target = 0
                s["planned_indent"] = target
                plan.append(target)
                if opens:
                    push_block(target, "flow")
                continue
            # Normal class attribute path:
            # Use the current body indent if inside a class.
            if stack:
                target = current_inside_body_indent()
            else:
                target = 0
            s["planned_indent"] = target
            plan.append(target)
            if opens:
                push_block(target, "flow")
            continue

        # ---- decorator ----
        if first.startswith("@"):
            # Decorator's indent equals what the next def/class will use.
            # Look at the next stmt to see if it's a def/class.
            nxt = None
            for s2 in stmts[i + 1:]:
                nxt = s2
                break
            if nxt is not None:
                nxt_first = nxt["text"].lstrip().splitlines()[0].lstrip()
                if nxt_first.startswith(("def ", "class ", "async ")):
                    # Determine where THAT def/class should be.
                    # If we're currently inside a class body (top of stack is
                    # class), the next item is conditionally:
                    #   - a method only if it's `def NAME(self, ...)`
                    #   - a top-level def/class otherwise (cascade signal)
                    if stack and stack[-1][1] == "class":
                        if nxt_first.startswith("class "):
                            # @dataclass class inside another class - almost
                            # certainly a cascade. Pop the enclosing class.
                            stack.clear()
                            target = 0
                        else:
                            # @decorator def ... check first param.
                            pm = re.match(r"def\s+\w+\s*\(\s*([^,)]+)?", nxt_first)
                            fp = (pm.group(1).strip() if pm and pm.group(1) else "").split(":")[0].strip()
                            if fp in ("self", "cls"):
                                target = current_inside_body_indent()
                            else:
                                stack.clear()
                                target = 0
                    else:
                        target = 0
                    s["planned_indent"] = target
                    plan.append(target)
                    continue
            # Fall through to generic
            target = current_inside_body_indent() if stack else 0
            s["planned_indent"] = target
            plan.append(target)
            continue

        # ---- def / class ----
        if first.startswith(("def ", "class ", "async def ", "async class ")):
            # First: if the previous stmt was a terminal (return/raise/etc),
            # pop the def-or-flow stack chain since we are likely in a
            # sibling scope now.
            prev_first = stmts[i - 1]["text"].lstrip().splitlines()[0].lstrip() if i > 0 else ""
            if _is_terminal_stmt(prev_first):
                # Pop flow blocks. Also pop the def itself if the new
                # def/class has `self`/`cls` (still a method) or doesn't.
                while stack and stack[-1][1] == "flow":
                    stack.pop()
                # Pop the def: if it was a method, the new def at sibling
                # scope is another method. So check: is the def followed by
                # a class? If stack[-1] is "def" and the next-but-one in stack
                # is "class", pop the def to make the new def a sibling
                # method.
                if stack and stack[-1][1] == "def":
                    # Pop the def; the new def will be planned next.
                    stack.pop()

            # If previous stmt was a decorator at the current planned level,
            # follow it.
            if prev_first.startswith("@") and plan:
                target = plan[-1]
            else:
                # Pop any open `def` blocks that sit between us and any
                # enclosing class - because if we're a `def NAME(self, ...)`,
                # we're a sibling method, not a nested function.
                if first.startswith("def "):
                    pm = re.match(r"def\s+\w+\s*\(\s*([^,)]+)?", first)
                    first_param = pm.group(1).strip() if pm and pm.group(1) else ""
                    first_param_name = first_param.split(":")[0].strip()
                    if first_param_name in ("self", "cls"):
                        # Walk down stack to find enclosing class.
                        while stack and stack[-1][1] != "class":
                            stack.pop()
                        if stack and stack[-1][1] == "class":
                            target = current_inside_body_indent()
                        else:
                            # No enclosing class found - even though `self`
                            # suggests method. Place at module level.
                            target = 0
                    else:
                        # Function with non-self first arg - module level.
                        # Pop everything.
                        stack.clear()
                        target = 0
                elif first.startswith("class "):
                    if stack and stack[-1][1] == "class":
                        # nested class - usually cascade; force module level
                        stack.clear()
                        target = 0
                    else:
                        target = 0
                else:
                    target = 0
            # Adjust stack: pop until we reach a level that makes sense.
            while stack and stack[-1][0] >= target:
                stack.pop()
            s["planned_indent"] = target
            plan.append(target)
            if opens:
                push_block(target, "class" if first.startswith("class ") else "def")
            continue

        # ---- Continuation clauses (else, elif, except, finally) ----
        # These should be at the SAME indent as their matching opener (the
        # most recent flow block at a depth >= current). We pop the
        # innermost flow block and use its indent.
        if first.startswith(("else", "elif", "except", "finally")) or first.startswith(
            ("else:", "elif ", "except:", "except ", "finally:")
        ):
            # Match the most recent flow block at the appropriate level.
            # Find the topmost flow block; that's the if/try whose body we
            # were inside. Pop it.
            if stack and stack[-1][1] == "flow":
                target = stack[-1][0]
                stack.pop()
            elif stack:
                target = current_inside_body_indent()
            else:
                target = 0
            s["planned_indent"] = target
            plan.append(target)
            if opens:
                push_block(target, "flow")
            continue

        # ---- Generic statement (assignment, expression, return, etc.) ----

        # Strong "module-level demo" signal: when we are inside a `def` and we
        # see a statement that calls something defined at module level in this
        # source (a class instantiation, a free function call, etc.) AND that
        # call refers to the function we'd be inside OR to a class whose
        # definition was at indent 0.
        # This catches `pipeline = SafetyPipeline(...)` after `def process`.
        if stack and stack[-1][1] == "def":
            # Find the function name from the def at the top of stack.
            current_fn_name = None
            for prior_idx in range(i - 1, -1, -1):
                pt = stmts[prior_idx]["text"].lstrip().splitlines()[0].lstrip()
                m_dn = re.match(r"def\s+([A-Za-z_][A-Za-z0-9_]*)", pt)
                if m_dn:
                    current_fn_name = m_dn.group(1)
                    break
            demo_signal = False
            if current_fn_name and re.search(
                rf"(^|[^A-Za-z0-9_]){re.escape(current_fn_name)}\s*\(",
                first,
            ):
                demo_signal = True
            else:
                # Look for calls to module-level (intended) class names. A
                # candidate name is one that:
                #   - starts with an uppercase letter
                #   - was defined as `class NAME` somewhere
                # If `first` calls such a name, it's a demo-style line.
                for nm in defined_names:
                    if not nm or not nm[0].isupper():
                        continue
                    if re.search(rf"(^|[^A-Za-z0-9_]){re.escape(nm)}\s*\(", first):
                        demo_signal = True
                        break
            if demo_signal:
                stack.clear()
                target = 0
                s["planned_indent"] = target
                plan.append(target)
                if opens:
                    push_block(target, "flow")
                continue

        # Use body indent of innermost block. If no stack, module-level.
        if stack:
            target = current_inside_body_indent()
        else:
            target = 0
        # Dead-code-after-return / -raise: if the previous stmt was a
        # terminal statement (return / raise / break / continue) inside one
        # `flow` block, pop ONE flow level. The next statement is a sibling
        # of the closed conditional, not necessarily outside all enclosing
        # conditionals.
        if i > 0:
            prev_first = stmts[i - 1]["text"].lstrip().splitlines()[0].lstrip()
            terminal = _is_terminal_stmt(prev_first)
            if terminal and not first.startswith(("else", "elif", "except", "finally")):
                # Pop exactly one flow block (if any).
                if stack and stack[-1][1] == "flow":
                    stack.pop()
                else:
                    # No flow block - the terminal stmt was at the def body
                    # level. The CURRENT stmt is dead code after return,
                    # which strongly suggests the def body has ended and
                    # this stmt belongs at module level. Pop the def too.
                    if stack and stack[-1][1] == "def":
                        # Only do this if the current stmt has a "demo-ish"
                        # shape: an assignment to a non-self name, or a
                        # print/expression call. Methods would be `def`
                        # which is handled separately above.
                        # Pop the def.
                        stack.pop()
                target = current_inside_body_indent() if stack else 0
            # Original-indent regression signal: if the current statement's
            # ORIGINAL indent is meaningfully shallower than the previous
            # statement's ORIGINAL indent, the author drew a "dedent" line.
            # Honor it by popping the stack proportionally.
            #
            # Only apply when both indents are sensible multiples of 4 (not
            # cascade-noise like "1 space" indent leftover) AND the dedent is
            # by at least 4 spaces.
            cur_orig = s["indent"]
            prev_orig = stmts[i - 1]["indent"]
            if (
                cur_orig < prev_orig
                and cur_orig % 4 == 0
                and prev_orig % 4 == 0
                and (prev_orig - cur_orig) >= 4
            ):
                expected_stack_depth = cur_orig // 4
                while len(stack) > expected_stack_depth:
                    stack.pop()
                target = current_inside_body_indent() if stack else 0
        s["planned_indent"] = target
        plan.append(target)
        if opens:
            push_block(target, "flow")
        continue

    # Apply plan to source lines.
    lines = src.splitlines()
    line_shift = [0] * (len(lines) + 2)
    for idx, s in enumerate(stmts):
        sh = plan[idx] - s["indent"]
        for ln in range(s["start_line"], s["end_line"] + 1):
            line_shift[ln] = sh
    # Fill blanks/comments by looking forward.
    plan_by_start = {s["start_line"]: plan[i] for i, s in enumerate(stmts)}
    for bi, b in enumerate(blocks):
        if b["kind"] in ("blank", "comment"):
            nxt_shift = 0
            for cand_b in blocks[bi + 1:]:
                if cand_b["kind"] == "stmt":
                    sl = cand_b["start_line"]
                    if sl in plan_by_start:
                        nxt_shift = plan_by_start[sl] - cand_b["indent"]
                    break
            ln = b["start_line"]
            if b["kind"] == "comment":
                cur = b["indent"]
                if cur + nxt_shift < 0:
                    nxt_shift = -cur
            line_shift[ln] = nxt_shift

    new_lines = []
    for i, ln in enumerate(lines, 1):
        sh = line_shift[i]
        if ln.strip() == "":
            new_lines.append(ln)
            continue
        if sh > 0:
            new_lines.append(" " * sh + ln)
        elif sh < 0:
            cur = len(ln) - len(ln.lstrip(" "))
            act = min(cur, -sh)
            new_lines.append(ln[act:])
        else:
            new_lines.append(ln)
    new_src = "\n".join(new_lines)
    return new_src if new_src != src else None


def _force_module_anchors(src: str) -> str | None:
    """
    For every statement that 'looks like' it should be at module level
    (imports, @dataclass class, demo prints / for-loops / assignments at the
    end that reference module-level names), force it to column 0 and shift
    its body proportionally.

    This is a heavier intervention; only used when simpler dedents don't work.
    """
    blocks = split_logical_blocks(src)
    stmts = [b for b in blocks if b["kind"] == "stmt"]
    if not stmts:
        return None
    # We process statements in order. We maintain an "expected" indent based
    # on whether the previous statement opens a block.
    plan: list[tuple[int, int, int]] = []  # (start_line, end_line, target_indent)
    expected = 0
    prev_opens = False
    prev_indent = 0
    for i, s in enumerate(stmts):
        first = s["text"].lstrip().splitlines()[0].lstrip()
        cur = s["indent"]
        # Decide target.
        if first.startswith(("import ", "from ", "if __name__")):
            target = 0
            expected = 0
            prev_opens = _stmt_opens_block(s["text"])
            prev_indent = target
        elif first.startswith("@"):
            # decorator: same indent as the def/class it decorates.
            # Look ahead.
            target = expected
            # Don't change expected; the next stmt is the def/class proper.
            prev_opens = False
            prev_indent = target
        elif first.startswith(("def ", "class ", "async ")):
            # If the immediately preceding stmt was a decorator at the same
            # logical line group, follow it.
            if i > 0 and stmts[i - 1]["text"].lstrip().startswith("@"):
                target = plan[-1][2]
            else:
                target = expected
            prev_opens = _stmt_opens_block(s["text"])
            prev_indent = target
            expected = target
        else:
            # Generic statement: continues current block.
            if prev_opens:
                target = prev_indent + 4
                expected = target
                prev_opens = False
                prev_indent = target
            else:
                target = expected
        plan.append((s["start_line"], s["end_line"], target))

    # Apply: for each statement block, shift = target - original_indent.
    lines = src.splitlines()
    line_shift = [0] * (len(lines) + 2)
    for idx, (s, e, t) in enumerate(plan):
        orig_indent = stmts[idx]["indent"]
        sh = t - orig_indent
        for ln in range(s, e + 1):
            line_shift[ln] = sh
    # Fill comments/blanks with the NEXT statement's shift.
    for bi, b in enumerate(blocks):
        if b["kind"] in ("blank", "comment"):
            # find next stmt's shift
            nxt_shift = None
            for cand_b in blocks[bi + 1:]:
                if cand_b["kind"] == "stmt":
                    # find its plan
                    for (s, e, t), si in zip(plan, stmts):
                        if si["start_line"] == cand_b["start_line"]:
                            nxt_shift = t - si["indent"]
                            break
                    if nxt_shift is not None:
                        break
            if nxt_shift is None:
                # use last
                if plan:
                    nxt_shift = plan[-1][2] - stmts[-1]["indent"]
                else:
                    nxt_shift = 0
            ln = b["start_line"]
            if b["kind"] == "comment":
                cur = b["indent"]
                if cur + nxt_shift < 0:
                    nxt_shift = -cur
            line_shift[ln] = nxt_shift

    new_lines = []
    for i, ln in enumerate(lines, 1):
        sh = line_shift[i]
        if ln.strip() == "":
            new_lines.append(ln)
            continue
        if sh > 0:
            new_lines.append(" " * sh + ln)
        elif sh < 0:
            removable = len(ln) - len(ln.lstrip(" "))
            act = min(removable, -sh)
            new_lines.append(ln[act:])
        else:
            new_lines.append(ln)
    return "\n".join(new_lines)


def repair_overindent_cascade(src: str) -> tuple[str | None, str]:
    """
    Detect the 35.1.1 / 11.3.3 pattern: after the FIRST `class` or `def`, the
    rest of the source's indent has cascaded deeper and deeper. Flatten by
    walking line by line and reassigning indents based on syntactic anchors.

    Approach: identify cascade boundaries by looking at the sequence of
    indents on logical-statement starts. If the indent monotonically increases
    in a way that's not justified by enclosing constructs, we re-flow.

    Concretely:
      - Tokenize the source.
      - Build a stream of (line, indent, first_token) of statement starts.
      - Walk: maintain a stack of "intended" indents based on whether the
        previous statement ended with `:` (opening a block). When a new
        statement appears at indent >= current expected, but does NOT begin
        a block, AND the previous statement was at a deeper indent than
        the cascade root, dedent it.
    """
    lines = src.splitlines(keepends=False)
    # Convert to logical blocks
    blocks = split_logical_blocks(src)

    # We compute, for each "stmt" block, its first-token information.
    stmts = []
    for b in blocks:
        if b["kind"] != "stmt":
            continue
        first = b["text"].lstrip().splitlines()[0]
        first_stripped = first.lstrip(" ")
        ends_block = _stmt_opens_block(b["text"])
        stmts.append({
            **b,
            "first_stripped": first_stripped,
            "opens_block": ends_block,
        })

    if not stmts:
        return None, "no statements"

    # Strategy: reconstruct intended indent stack.
    # Start with the first statement's indent (often 0) as the "root".
    # Then: each subsequent statement's intended indent is determined by
    # whether the previous one opened a block.
    #   - If prev opened a block: intended >= prev.indent + 4
    #   - Else: intended == prev.indent (sibling) OR less (dedent on a
    #     statement that clearly belongs to an outer scope: decorator, def
    #     starting a top-level fn, etc.)
    # We can't always tell, so we ALSO look for "anchor" signals:
    #   - lines starting with `from `/`import ` -> intended = root indent (usu. 0)
    #   - lines starting with `@dataclass` and the next stmt is `class ...`:
    #     they go together; their indent should match whichever indent the
    #     last "natural" def/class chose.
    #   - lines starting with `if __name__` -> root indent.
    #   - lines starting with `print(` AFTER a class+def cascade: root indent.

    # Phase 1: assign "intended_indent" per statement.
    root_indent = stmts[0]["indent"]
    intended = []
    stack: list[tuple[int, bool]] = []
    # stack entries: (indent, opens_block_for_a_def_or_class)

    prev = None
    for s in stmts:
        cur_indent = s["indent"]
        first = s["first_stripped"]

        if prev is None:
            target = root_indent
            intended.append(target)
            if s["opens_block"]:
                stack.append((target, True))
            prev = s
            continue

        # Anchor checks --------------------------------------------------
        if first.startswith(("import ", "from ")):
            # Imports almost always module-level (root_indent).
            target = root_indent
        elif first.startswith("if __name__"):
            target = root_indent
        elif first.startswith("@"):
            # Decorator: follow the previous sibling's indent. Common in
            # cascade bugs is "@dataclass" landing one nest deeper than
            # the original sibling.
            target = _decorator_target_indent(prev, stack, root_indent, cur_indent)
        elif first.startswith(("class ", "def ")):
            # If the IMMEDIATELY preceding stmt was a decorator at the same
            # intended indent, follow it. Otherwise default to sibling/closer.
            if intended and prev["first_stripped"].startswith("@"):
                target = intended[-1]
            else:
                target = _next_indent_for_def_or_class(prev, stack, intended[-1])
        else:
            # Generic statement.
            target = _next_indent_for_generic(prev, stack, intended[-1])

        # Now update stack based on the relationship between this target
        # and previous targets.
        while stack and stack[-1][0] >= target:
            stack.pop()
        # Wait: we want to keep a stack of CURRENTLY OPEN blocks.
        # Simpler heuristic: rebuild from intended history.
        # For simplicity push if this stmt opens a block.
        if s["opens_block"]:
            stack.append((target, True))
        intended.append(target)
        prev = s

    # Apply the intended indents back to the source. The shift for each
    # statement is (target - cur_indent). We need to apply that shift to
    # EVERY line of that logical block, including continuation lines, AND
    # to comment/blank lines that lie within the block? blank/comment lines
    # are split as their own blocks, so we'll need to interleave.

    # Build a per-line shift table.
    line_shift = [0] * (len(lines) + 1)  # 1-indexed
    stmt_idx = 0
    last_stmt_shift = 0
    last_stmt_indent = root_indent
    last_stmt_target = root_indent
    for b in blocks:
        if b["kind"] == "stmt":
            cur = b["indent"]
            target = intended[stmt_idx]
            shift = target - cur
            last_stmt_shift = shift
            last_stmt_indent = cur
            last_stmt_target = target
            for ln in range(b["start_line"], b["end_line"] + 1):
                line_shift[ln] = shift
            stmt_idx += 1
        else:
            # blank/comment: attach the shift of the *upcoming* statement
            # so that comments above a top-level statement also dedent.
            # We do this in a second pass.
            pass

    # Second pass: comments/blanks - look forward to the next stmt and
    # use that stmt's shift. If none, use last_stmt_shift.
    upcoming = None
    upcoming_shift = last_stmt_shift
    # Walk blocks again, this time backward to fill blank/comment forward-fill.
    # Easier: walk forward; remember last_shift; for blank lines, use the
    # NEXT stmt's shift, not the previous one.
    # Build a list of (range_start, range_end, shift) for stmts in order.
    stmt_runs = []
    stmt_idx = 0
    for b in blocks:
        if b["kind"] == "stmt":
            stmt_runs.append((b["start_line"], b["end_line"], intended[stmt_idx] - b["indent"], b["indent"]))
            stmt_idx += 1
    # For each blank/comment block, find the next stmt run and use its shift.
    for bi, b in enumerate(blocks):
        if b["kind"] in ("blank", "comment"):
            ln = b["start_line"]
            # find next stmt run
            nxt = None
            for run in stmt_runs:
                if run[0] >= ln:
                    nxt = run
                    break
            if nxt is None:
                # use last
                if stmt_runs:
                    nxt = stmt_runs[-1]
                else:
                    nxt = (ln, ln, 0, 0)
            shift = nxt[2]
            # For comments, also match the target indent of the next stmt
            # if the comment's current indent is "way off" (much deeper).
            if b["kind"] == "comment":
                cur_c = b["indent"]
                # If we'd produce negative indent, clamp to 0.
                if cur_c + shift < 0:
                    shift = -cur_c
            line_shift[ln] = shift

    # Now apply shifts.
    new_lines = []
    for i, ln in enumerate(lines, 1):
        sh = line_shift[i]
        if sh == 0 or ln.strip() == "":
            new_lines.append(ln)
            continue
        if sh > 0:
            new_lines.append(" " * sh + ln)
        else:
            # Negative shift: remove that many leading spaces (only if present)
            removable = len(ln) - len(ln.lstrip(" "))
            actual = min(removable, -sh)
            new_lines.append(ln[actual:])
    new_src = "\n".join(new_lines)
    return new_src, "overindent_cascade_reflow"


def _stmt_opens_block(text: str) -> bool:
    """Return True if this statement ends with a ':' that opens a new block."""
    # Strip trailing comments and whitespace from each non-empty line and
    # check the LAST non-empty line's last non-comment char.
    # Bracket-aware: the ':' must be outside brackets.
    # Use tokenize on the snippet.
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        # fallback: last char check
        last = text.rstrip().splitlines()[-1].rstrip()
        # strip trailing comment
        last_noc = re.sub(r"\s*#.*$", "", last)
        return last_noc.rstrip().endswith(":")
    # Find OP ':' at depth 0
    depth = 0
    last_was_colon_at_depth0 = False
    for tok in toks:
        if tok.type == tokenize.OP:
            s = tok.string
            if s in "([{":
                depth += 1
            elif s in ")]}":
                depth -= 1
            elif s == ":" and depth == 0:
                last_was_colon_at_depth0 = True
            else:
                last_was_colon_at_depth0 = False
        elif tok.type in (tokenize.NEWLINE, tokenize.NL):
            pass
        elif tok.type in (tokenize.COMMENT,):
            pass
        elif tok.type in (tokenize.ENDMARKER, tokenize.INDENT, tokenize.DEDENT):
            pass
        else:
            last_was_colon_at_depth0 = False
    return last_was_colon_at_depth0


def _decorator_target_indent(prev, stack, root_indent, cur_indent):
    """Decorators chain at the same level as their target definition."""
    if not stack:
        return root_indent
    # If previous statement was at a deeper indent than expected,
    # decorator usually wants the outer level.
    if prev.get("opens_block"):
        # We must be IN a block (e.g., method decorator in a class). Use
        # prev_indent + 4.
        return prev["indent"] + 4 if prev["indent"] == stack[-1][0] else stack[-1][0] + 4
    return prev["indent"]


def _next_indent_for_def_or_class(prev, stack, last_intended):
    """If prev opened a block (def/class), we go deeper. Otherwise sibling."""
    if prev.get("opens_block"):
        # We are starting the body of prev.
        return prev["indent"] + 4 if prev["indent"] != last_intended else last_intended + 4
    return last_intended


def _next_indent_for_generic(prev, stack, last_intended):
    if prev.get("opens_block"):
        return last_intended + 4 if last_intended <= prev["indent"] else last_intended
    return last_intended


# --- repair_missing_body_indent -------------------------------------------


def repair_missing_body_indent(src: str) -> tuple[str | None, str]:
    """
    Fix the 35.1.2 pattern: `def foo(...):` at column 0 with body lines also
    at column 0. The body should be indented by 4 inside the function.

    Strategy: detect a line starting with `def ` or `class ` that ends in `:`
    where the next non-blank line is at the SAME indent. Push that next block
    down by 4 spaces, recursively for everything that "belongs" to this
    function until we hit a line at the SAME indent that is itself a new
    def/class/import/decorator (i.e., a new sibling).
    """
    blocks = split_logical_blocks(src)
    # Walk through stmts looking for def/class with same-indent next stmt.
    fixes: list[tuple[int, int, int]] = []
    # We need to mark line ranges to push deeper.
    n = len(blocks)
    for i, b in enumerate(blocks):
        if b["kind"] != "stmt":
            continue
        first = b["text"].lstrip().splitlines()[0].lstrip()
        if not (first.startswith("def ") or first.startswith("class ")):
            continue
        if not _stmt_opens_block(b["text"]):
            continue
        # find next stmt
        j = i + 1
        while j < n and blocks[j]["kind"] != "stmt":
            j += 1
        if j >= n:
            continue
        nxt = blocks[j]
        if nxt["indent"] != b["indent"]:
            # already indented properly (deeper), or already dedented (sibling)
            continue
        # The next stmt is at the SAME indent as the def. That's a body-indent
        # problem. We need to push it down until we find a real sibling.
        # A "real sibling" is the next stmt at this same indent whose first
        # token is `def`/`class`/`async`/`@` or `import`/`from`/`if __name__`
        # OR is preceded by a blank line. Otherwise we keep pushing.

        # Walk forward: include all stmts until a sibling.
        body_start = nxt["start_line"]
        body_end = nxt["end_line"]
        k = j + 1
        while k < n:
            bb = blocks[k]
            if bb["kind"] == "stmt":
                if bb["indent"] < b["indent"]:
                    break  # outer scope
                if bb["indent"] == b["indent"]:
                    # Is it a sibling start? Check first token.
                    f0 = bb["text"].lstrip().splitlines()[0].lstrip()
                    if (
                        f0.startswith(("def ", "class ", "async ", "@", "import ", "from "))
                        or f0.startswith("if __name__")
                    ):
                        # Sibling - stop here.
                        break
                body_end = bb["end_line"]
            elif bb["kind"] == "comment":
                # extend through comments
                body_end = bb["end_line"]
            else:
                # blank: extend through but only if next is still body
                # peek
                pass
            k += 1
        fixes.append((body_start, body_end, b["indent"] + 4 - nxt["indent"]))

    if not fixes:
        return None, "no_body_indent_problems"

    lines = src.splitlines()
    # apply shifts
    shifts = [0] * (len(lines) + 2)
    for s, e, sh in fixes:
        for ln in range(s, e + 1):
            shifts[ln] += sh
    new_lines = []
    for i, ln in enumerate(lines, 1):
        sh = shifts[i]
        if sh > 0 and ln.strip() != "":
            new_lines.append(" " * sh + ln)
        else:
            new_lines.append(ln)
    return "\n".join(new_lines), f"missing_body_indent_pushed_{len(fixes)}_fns"


# --- repair_missing_hanging_indent ----------------------------------------


def repair_missing_hanging_indent(src: str) -> tuple[str | None, str]:
    """
    Fix calls like:

        f = client.create(
        a=1,
        b=2,
        )

    by giving continuation lines a hanging indent. We only do this when:
      - the FIRST continuation line starts at column 0 (or at the same
        indent as the opening line), AND
      - the closing bracket is on its own line at the same indent as the
        first continuation line.

    Apply hanging indent equal to opening_line_indent + 4.
    """
    blocks = split_logical_blocks(src)
    lines = src.splitlines()
    n = len(lines)
    shift_for_line = [0] * (n + 2)
    applied = 0
    for b in blocks:
        if b["kind"] != "stmt":
            continue
        if b["end_line"] <= b["start_line"]:
            continue
        opening_line = lines[b["start_line"] - 1]
        opening_indent = len(opening_line) - len(opening_line.lstrip(" "))
        # Look at the second through last lines.
        cont_lines = list(range(b["start_line"] + 1, b["end_line"] + 1))
        if not cont_lines:
            continue
        # Get first continuation indent
        first_cont_indent = None
        for cl in cont_lines:
            t = lines[cl - 1]
            if t.strip() == "":
                continue
            first_cont_indent = len(t) - len(t.lstrip(" "))
            break
        if first_cont_indent is None:
            continue
        # We want first_cont_indent > opening_indent (hanging indent).
        # If first_cont_indent <= opening_indent, push by (opening_indent + 4 - first_cont_indent).
        if first_cont_indent > opening_indent:
            continue
        # Also require that this is actually a multi-line call/dict/list/etc.
        # The opening line must end with an unclosed bracket. Bracket-depth
        # at end of opening line > 0.
        if _bracket_delta(opening_line) <= 0:
            continue
        push = (opening_indent + 4) - first_cont_indent
        if push <= 0:
            continue
        # Apply push to ALL non-blank continuation lines, EXCEPT the closing
        # bracket on its own line - we usually want it at opening_indent.
        # Simpler: apply push to lines whose stripped text doesn't start with a
        # standalone `)`/`]`/`}`. The closer line we leave at opening_indent
        # (push it to opening_indent if it was at 0).
        last_line_no = max(cont_lines)
        for cl in cont_lines:
            t = lines[cl - 1]
            if t.strip() == "":
                continue
            stripped = t.strip()
            # closer-only line on the FINAL line of the block: set to opening_indent.
            if cl == last_line_no and re.fullmatch(r"[)\]}](\s*[,)\]}])*", stripped):
                cur_indent = len(t) - len(t.lstrip(" "))
                shift_for_line[cl] = opening_indent - cur_indent
            else:
                shift_for_line[cl] += push
        applied += 1

    if not applied:
        return None, "no_hanging_indent_problems"
    new_lines = []
    for i, ln in enumerate(lines, 1):
        sh = shift_for_line[i]
        if ln.strip() == "":
            new_lines.append(ln)
            continue
        if sh > 0:
            new_lines.append(" " * sh + ln)
        elif sh < 0:
            removable = len(ln) - len(ln.lstrip(" "))
            actual = min(removable, -sh)
            new_lines.append(ln[actual:])
        else:
            new_lines.append(ln)
    return "\n".join(new_lines), f"hanging_indent_applied_{applied}_calls"


# ---------------------------------------------------------------------------
# Validation for other languages
# ---------------------------------------------------------------------------


def check_bash_block(src: str) -> list[str]:
    """Light validation: backslash continuations should have NL right after."""
    issues = []
    lines = src.splitlines()
    for i, ln in enumerate(lines):
        if ln.rstrip("\n").endswith("\\"):
            # next line should exist
            if i == len(lines) - 1:
                issues.append(f"trailing-backslash-on-last-line:line {i+1}")
    return issues


def check_json_block(src: str) -> list[str]:
    try:
        json.loads(src)
        return []
    except json.JSONDecodeError as e:
        return [f"json-parse-fail:{e.msg} at line {e.lineno}"]


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def iter_target_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.html"):
        rel = p.relative_to(root)
        parts = rel.parts
        if any(part in EXCLUDE_PARTS for part in parts):
            continue
        if any(part.startswith(EXCLUDE_PREFIXES) for part in parts):
            continue
        if any(c in rel.as_posix() for c in EXCLUDE_CONTAINS):
            continue
        yield p


@dataclass
class Report:
    fragments_scanned: int = 0
    files_scanned: int = 0
    by_lang: dict = field(default_factory=dict)
    issues_found: dict = field(default_factory=dict)
    fixed: list = field(default_factory=list)
    unfixed: list = field(default_factory=list)
    parse_failures_remaining: list = field(default_factory=list)

    def to_markdown(self) -> str:
        out = [
            "# Code Fragment Audit & Fix Report\n\n",
            "Generated by `scripts/_fix_code_fragments.py` (re-run to refresh).\n\n",
            "## Scan summary\n",
        ]
        out.append(f"- **Total HTML files scanned:** {self.files_scanned}\n")
        out.append(f"- **HTML files with detected issues (fixed or flagged):** {len(self._file_set())}\n")
        out.append(f"- **Total code fragments scanned:** {self.fragments_scanned}\n")
        out.append("\n## Fragments by language\n")
        for lang, n in sorted(self.by_lang.items()):
            out.append(f"- `{lang}`: {n}\n")
        out.append("\n## Issue categories detected\n")
        for cat, n in sorted(self.issues_found.items(), key=lambda x: -x[1]):
            out.append(f"- `{cat}`: {n}\n")
        out.append(f"\n## Totals (this run)\n")
        out.append(f"- **Fixed this run:** {len(self.fixed)}\n")
        out.append(f"- **Unfixed (flagged for human review):** {len(self.unfixed)}\n")
        out.append(f"- **Parse failures remaining after attempted fix:** {len(self.parse_failures_remaining)}\n")
        out.append(
            "\nNote: the script is idempotent. If the source HTML has already been fixed\n"
            "by a previous run, the fragments will parse cleanly and won't be re-reported\n"
            "as 'fixed' here.\n"
        )

        # Categorize fix notes
        from collections import Counter
        fix_categories = Counter()
        for f in self.fixed:
            note = f.get("note", "")
            cat = note.split("_")[0] if "_" in note else note.split(" ")[0]
            if "cascade" in note:
                fix_categories["cascade_aware_reflow"] += 1
            elif "hanging" in note:
                fix_categories["hanging_indent_applied"] += 1
            elif "summary_print" in note:
                fix_categories["summary_print_denested"] += 1
            elif "missing_body_indent" in note:
                fix_categories["missing_body_indent"] += 1
            elif "module_anchors_forced" in note:
                fix_categories["module_anchors_forced"] += 1
            elif "cut@" in note:
                fix_categories["suffix_dedent"] += 1
            else:
                fix_categories[note or "other"] += 1
        out.append("\n## Fix strategy breakdown\n")
        for cat, n in fix_categories.most_common():
            out.append(f"- `{cat}`: {n}\n")

        # Group fixed fragments by section
        out.append("\n## Fixed fragments (per file)\n")
        from itertools import groupby
        sorted_fixed = sorted(self.fixed, key=lambda x: x["file"])
        for fname, items in groupby(sorted_fixed, key=lambda x: x["file"]):
            items = list(items)
            out.append(f"\n### `{fname}` ({len(items)} fix{'es' if len(items) != 1 else ''})\n")
            for f in items:
                out.append(
                    f"- Fragment {f.get('caption','?')}: {f['note']}\n"
                )

        out.append("\n## Unfixed fragments (human review required)\n")
        sorted_unfixed = sorted(self.unfixed, key=lambda x: x["file"])
        for fname, items in groupby(sorted_unfixed, key=lambda x: x["file"]):
            items = list(items)
            out.append(f"\n### `{fname}` ({len(items)})\n")
            for f in items:
                out.append(
                    f"- Fragment {f.get('caption','?')}: {f['reason']}\n"
                )
        return "".join(out)

    def _file_set(self) -> set:
        s = set()
        for f in self.fixed:
            s.add(f["file"])
        for f in self.unfixed:
            s.add(f["file"])
        return s


CAPTION_RE = re.compile(
    r'<div\s+class="code-caption"[^>]*>\s*<strong>\s*Code\s+Fragment\s+([0-9A-Za-z.]+)\s*:',
    re.IGNORECASE,
)


def caption_for_block(html_text: str, block_end_pos: int) -> str:
    """Look for the caption div immediately after the block; return its number."""
    snippet = html_text[block_end_pos : block_end_pos + 600]
    m = CAPTION_RE.search(snippet)
    if m:
        return m.group(1)
    return "?"


def process_file(path: Path, write: bool, report: Report) -> None:
    text = path.read_text(encoding="utf-8")
    pos = 0
    out_pieces = []
    last_end = 0
    file_changed = False

    for m in PRE_BLOCK_RE.finditer(text):
        full_match_start = m.start()
        full_match_end = m.end()
        open_tag = m.group(1)
        class_attrs = m.group(2) or ""
        inner = m.group(3)
        close_tag = m.group(4)

        report.fragments_scanned += 1

        class_str_match = CLASS_ATTR_RE.search(class_attrs)
        class_str = class_str_match.group(1) if class_str_match else ""
        lang = detect_lang(class_str)
        report.by_lang[lang or "unknown"] = report.by_lang.get(lang or "unknown", 0) + 1

        caption = caption_for_block(text, full_match_end)

        # Append unchanged text from last_end up to this match start.
        out_pieces.append(text[last_end:full_match_start])

        if lang == "python":
            src = strip_html_to_source(inner)
            res = fix_python_source(src)
            for iss in res.issues:
                cat = iss.split(":", 1)[0].split(" ", 1)[0]
                # normalize cascade-depth-NN-with-M
                m_cd = re.match(r"(cascade-depth)-\d+", cat)
                if m_cd:
                    cat = m_cd.group(1)
                report.issues_found[cat] = report.issues_found.get(cat, 0) + 1
            if res.applied and res.fixed is not None and res.parsed_after:
                # Re-highlight and substitute.
                new_inner = rehighlight_python(res.fixed)
                new_block = open_tag + new_inner + close_tag
                out_pieces.append(new_block)
                report.fixed.append({
                    "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "caption": caption,
                    "note": "; ".join(res.notes) or "applied",
                })
                file_changed = True
            else:
                # leave block intact
                out_pieces.append(m.group(0))
                if res.issues:
                    if res.parsed_before:
                        # had structural issues but not severe - skip from
                        # unfixed if there's nothing to do.
                        pass
                    else:
                        report.unfixed.append({
                            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                            "caption": caption,
                            "reason": "; ".join(res.issues + res.notes)[:300],
                        })
                        if not res.parsed_after:
                            report.parse_failures_remaining.append({
                                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                                "caption": caption,
                            })
        elif lang in ("bash", "sh", "shell"):
            src = strip_html_to_source(inner)
            problems = check_bash_block(src)
            if problems:
                report.unfixed.append({
                    "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "caption": caption,
                    "reason": ", ".join(problems),
                })
            out_pieces.append(m.group(0))
        elif lang == "json":
            src = strip_html_to_source(inner)
            problems = check_json_block(src)
            if problems:
                # Don't auto-fix JSON - might be a snippet, not full doc.
                report.unfixed.append({
                    "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "caption": caption,
                    "reason": ", ".join(problems),
                })
            out_pieces.append(m.group(0))
        else:
            out_pieces.append(m.group(0))

        last_end = full_match_end

    out_pieces.append(text[last_end:])
    new_text = "".join(out_pieces)
    if write and file_changed and new_text != text:
        path.write_text(new_text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="apply fixes in place")
    ap.add_argument("--only", help="filter to one path substring")
    ap.add_argument("--report", default="code-fragment-fix-report.md")
    args = ap.parse_args()

    report = Report()
    for f in iter_target_files(ROOT):
        if args.only and args.only not in str(f):
            continue
        report.files_scanned += 1
        try:
            process_file(f, args.write, report)
        except Exception as e:
            print(f"ERROR processing {f}: {type(e).__name__}: {e}", file=sys.stderr)

    out = report.to_markdown()
    (ROOT / args.report).write_text(out, encoding="utf-8")
    # Print summary only (avoid Unicode issues on Windows console).
    summary_lines = [
        f"Total files touched: {len(report._file_set())}",
        f"Total fragments scanned: {report.fragments_scanned}",
        f"Fixed: {len(report.fixed)}",
        f"Unfixed (flagged): {len(report.unfixed)}",
        f"Parse failures remaining: {len(report.parse_failures_remaining)}",
    ]
    for line in summary_lines:
        print(line)
    print(f"Report saved to {ROOT / args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
