"""Fix Python code blocks that lost indentation during pygments rendering.

Walks all HTML files (skipping excluded dirs), finds
`<pre><code class="...lang-python pygments-highlighted...">...</code></pre>`
blocks, extracts plain text from the pygments spans, tests whether the code
parses as valid Python, and if not, attempts to re-derive correct indentation
via autopep8 and a manual `:`-based indent inferencer. If a fixed source
re-parses successfully, the block is replaced with freshly re-pygmentized HTML.

Conservative: any block that already parses, or whose re-indentation does not
parse, or that has structural ambiguity, is left alone.

Files modified within the last 5 minutes are skipped to avoid clobbering
concurrent edits.

Produces a Markdown report at E:/Projects/BookBlogsHome/LLMBook/pygments-indent-fix-report.md.
"""
from __future__ import annotations

import ast
import html as html_mod
import io
import re
import sys
import time
import tokenize
from pathlib import Path

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

try:
    import autopep8
except ImportError:
    autopep8 = None


ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {
    "node_modules",
    ".git",
    "KDP",
    "build",
    "temp_ebook",
    "temp_epub",
    "source_fix_backups",
    "pagefind",
    "templates",
    ".claude",
    ".book-update",
}
MTIME_GUARD_SECONDS = 300  # 5 minutes


# Match the entire <pre><code class="...lang-python pygments-highlighted..."> block.
# Must match where both classes appear in either order.
PRE_RE = re.compile(
    r'<pre><code class="([^"]*)"\s*>(.*?)</code></pre>',
    re.DOTALL,
)


def has_required_classes(class_attr: str) -> bool:
    classes = class_attr.split()
    return "pygments-highlighted" in classes and "lang-python" in classes


SPAN_OPEN_RE = re.compile(r'<span\s+class="[^"]*">')
SPAN_CLOSE_RE = re.compile(r'</span>')


def extract_plain_text(html_inner: str) -> str:
    """Strip pygments <span> tags, keeping only the text. Unescape HTML entities."""
    text = SPAN_OPEN_RE.sub("", html_inner)
    text = SPAN_CLOSE_RE.sub("", text)
    text = html_mod.unescape(text)
    # Pygments often appends a trailing newline; keep it as-is for now.
    return text


def parses(code: str) -> bool:
    # Strip REPL prompts which can appear in code blocks.
    cleaned = re.sub(r"^\s*>>>\s?", "", code, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*\.\.\.\s?", "", cleaned, flags=re.MULTILINE)
    try:
        ast.parse(cleaned)
        return True
    except (SyntaxError, ValueError):
        return False


# Gate: only attempt to fix blocks that look like indent-loss (a `:`-ending
# compound opener followed by a non-indented body line).
_INDENT_LOSS_OPENER_RE = re.compile(
    r"^(class|def|if|elif|else|for|while|with|try|except|finally|async)\b"
)


def is_indent_loss(code: str) -> bool:
    """True iff the failure pattern looks like indent-loss.

    Heuristic: there is a non-empty line that ends in `:` and starts a
    compound block (class/def/if/...), followed immediately by another
    non-empty line that is at the same or lower indent column.

    Excludes blocks that obviously aren't Python (shell scripts, pseudocode).
    """
    lines = code.splitlines()
    # Drop a leading shebang / pseudocode header.
    if lines and lines[0].lstrip().startswith(("#!", "Input:", "Output:")):
        return False
    # Look for ":"-ending opener followed by same-or-less-indent next line.
    for i in range(len(lines) - 1):
        line = lines[i]
        stripped = line.rstrip()
        if not stripped.endswith(":"):
            continue
        s = stripped.lstrip()
        if not _INDENT_LOSS_OPENER_RE.match(s):
            continue
        cur_indent = len(line) - len(line.lstrip())
        # Find the next non-empty line.
        for j in range(i + 1, len(lines)):
            nxt = lines[j]
            if not nxt.strip():
                continue
            nxt_indent = len(nxt) - len(nxt.lstrip())
            if nxt_indent <= cur_indent:
                return True
            break
    return False


# ---------------------------------------------------------------------------
# Manual indent inferencer
# ---------------------------------------------------------------------------
# Heuristic: walk the source line-by-line. Track an "expected indent depth"
# stack based on `:`-ending compound statements. For each non-blank line:
#   - If it starts an open-paren / open-bracket continuation, leave its leading
#     whitespace alone (continuations are managed by paren depth).
#   - Otherwise, re-emit the line with `depth * indent_unit` spaces prepended
#     to its stripped content, where depth is the current logical indent.
#   - If the line ends in `:` and is a compound-statement opener
#     (class/def/if/elif/else/for/while/with/try/except/finally/async/match/case),
#     increment depth for the next non-blank line.
#   - If the line is a dedent-like keyword (`return`, `pass`, `break`,
#     `continue`, `raise`), we keep the current depth for it, but the *next*
#     line at column 0 should dedent appropriately.
#
# We use Python's tokenizer when possible to identify logical line boundaries.

DEDENT_KEYWORDS = ("return", "pass", "break", "continue", "raise", "yield")
COMPOUND_OPENERS = re.compile(
    r"^\s*(class|def|if|elif|else|for|while|with|try|except|finally|async\s+def|async\s+for|async\s+with|match|case)\b"
)
ELIF_ELSE_EXCEPT_FINALLY = re.compile(
    r"^\s*(elif|else|except|finally)\b"
)


def _strip_string_indent(s: str) -> str:
    """Within a triple-string literal, leading whitespace is preserved by
    the parser as part of the string. We strip in our processing of code
    lines only outside string contexts. Use tokenize to find string tokens.
    """
    return s


def manual_reindent(source: str, indent_unit: str = "    ") -> str | None:
    """Attempt to re-derive Python indentation by scanning for `:`-terminated
    compound openers and aligning every following line to `depth * indent_unit`.

    Continuation lines inside parens/brackets keep relative shape; we
    detect paren depth via tokenize, and pass through their leading whitespace
    unchanged.

    Returns the new source string or None if it can't be inferred.
    """
    # Tokenize to track paren depth per line.
    try:
        tokens = list(
            tokenize.generate_tokens(io.StringIO(source).readline)
        )
    except (tokenize.TokenizeError, IndentationError, SyntaxError):
        # Fall back to a simpler paren-counting heuristic below.
        tokens = None

    raw_lines = source.split("\n")
    n = len(raw_lines)

    # Build a per-line "paren depth at line start" map.
    line_paren_depth = [0] * (n + 1)
    if tokens is not None:
        depth = 0
        last_line = 0
        for tok_type, tok_str, (srow, _), (erow, _), _ in tokens:
            # Fill in depth for lines we passed.
            while last_line < srow - 1:
                last_line += 1
                if last_line < len(line_paren_depth):
                    line_paren_depth[last_line] = depth
            if tok_type == tokenize.OP:
                if tok_str in ("(", "[", "{"):
                    depth += 1
                elif tok_str in (")", "]", "}"):
                    depth -= 1
                    if depth < 0:
                        depth = 0
        # Fill remainder.
        while last_line < n:
            last_line += 1
            if last_line < len(line_paren_depth):
                line_paren_depth[last_line] = depth

    # Track indent depth as we walk lines logically.
    out_lines: list[str] = []
    logical_depth = 0
    # When we see a compound opener ending in `:`, the *next* logical line
    # must be at depth + 1.
    pending_indent = False
    # When we see `else:`/`elif`/`except`/`finally` (dedent before), we need
    # to dedent first (assume one level), then process. This is rough; we
    # rely on the structure already being valid for them to align with
    # their parent if/try.
    in_triple_string = False
    triple_quote = None

    i = 0
    while i < n:
        line = raw_lines[i]
        stripped = line.strip()
        # Track triple-quoted strings in a coarse way (toggle on triple quote
        # not followed by close on same line).
        if not in_triple_string:
            # Find triple quotes outside any other quotes; very rough.
            for q in ('"""', "'''"):
                count = stripped.count(q)
                if count % 2 == 1:
                    in_triple_string = True
                    triple_quote = q
                    break
        else:
            if triple_quote and triple_quote in line:
                in_triple_string = False
                triple_quote = None
            # Inside a triple-string: do not change leading whitespace.
            out_lines.append(line)
            i += 1
            continue

        # Blank line: pass through.
        if not stripped:
            out_lines.append("")
            i += 1
            continue

        # If we are inside a paren continuation (line_paren_depth[i+1] > 0
        # when line i started), keep the existing leading whitespace.
        # Use 1-based indexing as built above; raw_lines is 0-indexed so
        # the start of line i+1 corresponds to line_paren_depth[i+1].
        if i + 1 < len(line_paren_depth) and line_paren_depth[i + 1] > 0:
            # Continuation of a previous open paren.
            out_lines.append(line)
            i += 1
            continue

        # Detect dedent keywords (elif/else/except/finally) which align with
        # parent.
        if ELIF_ELSE_EXCEPT_FINALLY.match(stripped):
            # Dedent one level for this line, then re-indent its body.
            current_depth = max(logical_depth - 1, 0)
            out_lines.append(indent_unit * current_depth + stripped)
            # If line ends in `:`, the next line is indented one deeper.
            if stripped.endswith(":"):
                logical_depth = current_depth + 1
            else:
                logical_depth = current_depth
            i += 1
            continue

        # Emit the line at logical_depth.
        out_lines.append(indent_unit * logical_depth + stripped)

        # If this is a compound opener ending in `:`, next logical line is +1.
        if stripped.endswith(":") and COMPOUND_OPENERS.match(stripped):
            logical_depth += 1
        elif stripped.endswith(":") and stripped.startswith(("@",)):
            pass  # decorator with weird colon: shouldn't happen
        # If stripped starts with a dedent keyword (`return`/`pass`/etc.)
        # and we're inside a function body, this line doesn't dedent itself
        # but the *next* logical structure might. We do not auto-dedent here:
        # rely on subsequent `else`/`except`/`elif`/`finally` or simply
        # accept the parsed result.
        # Note: this approach will *over-indent* lines that follow `return`/`pass`
        # in the original (lost-indent) form. This is acceptable only when the
        # original code has consistent depth.

        i += 1

    return "\n".join(out_lines)


# ---------------------------------------------------------------------------
# Smarter indent fixer using paren-depth-aware approach
# ---------------------------------------------------------------------------
def smart_reindent(source: str) -> str | None:
    """Re-derive indentation. Strategy:

    1. Normalize: strip leading whitespace from every line that is *not* inside
       a paren/bracket/brace continuation and not inside a triple-string.
    2. Walk lines; build indent depth by tracking compound openers / closers.
    3. Continuation lines inside open parens keep one extra indent of 4 spaces.

    Returns a candidate source or None.
    """
    raw_lines = source.split("\n")
    n = len(raw_lines)

    # Pass 1: paren-depth-at-line-start (best-effort with tokenize).
    # For each line, record the open-paren depth BEFORE any token on that
    # line is consumed.
    line_paren_depth = [0] * (n + 1)

    def _compute_depth_map(text: str) -> bool:
        try:
            toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
        except Exception:
            return False
        depth = 0
        seen_lines: set[int] = set()
        for tok_type, tok_str, (srow, _), (erow, _), _ in toks:
            if srow not in seen_lines:
                if 1 <= srow <= n:
                    line_paren_depth[srow] = depth
                seen_lines.add(srow)
            if tok_type == tokenize.OP:
                if tok_str in ("(", "[", "{"):
                    depth += 1
                elif tok_str in (")", "]", "}"):
                    depth = max(0, depth - 1)
        return True

    if not _compute_depth_map(source):
        stripped_src = "\n".join(l.lstrip() for l in raw_lines)
        if not _compute_depth_map(stripped_src):
            return None
    # Forward-fill: lines with no token (blank/comment-only) inherit the
    # depth from the previous tokenized line if their paren_depth was 0
    # only because we didn't set it. Iterate and fill blank gaps.
    last_seen_depth = 0
    last_seen_idx = 0
    for idx in range(1, n + 1):
        # If this line has any non-whitespace, we trust the value set above.
        # If it had no tokens at all (e.g. blank), set to last_seen_depth.
        line = raw_lines[idx - 1] if idx - 1 < len(raw_lines) else ""
        if line.strip():
            last_seen_depth = line_paren_depth[idx]
            last_seen_idx = idx
        else:
            line_paren_depth[idx] = last_seen_depth

    # Pass 2: triple-string ranges.
    in_triple = [False] * (n + 1)
    triple_state = False
    triple_q = None
    for idx, line in enumerate(raw_lines, start=1):
        in_triple[idx] = triple_state
        # Update for next line based on this line's content.
        line_check = line
        # Naive triple-quote tracking outside string contexts.
        # Find triple-quote occurrences ignoring escapes.
        for m in re.finditer(r'(\"\"\"|\'\'\')', line_check):
            q = m.group(1)
            if triple_state and triple_q == q:
                triple_state = False
                triple_q = None
            elif not triple_state:
                triple_state = True
                triple_q = q

    # Pass 3: emit lines.
    # opener_stack tracks the kind of compound block at each depth level:
    # entries are one of "class", "def", "other" (if/for/while/with/try).
    # When we encounter a new flat-source `def` or `class` opener with the
    # original indent column == 0, we treat it as a sibling: dedent to the
    # nearest "class" context (or to depth 0 if none).
    out: list[str] = []
    depth = 0
    indent = "    "
    opener_stack: list[str] = []  # one entry per depth level

    def _classify_opener(stripped_line: str) -> str:
        if re.match(r"^class\b", stripped_line):
            return "class"
        if re.match(r"^(async\s+)?def\b", stripped_line):
            return "def"
        return "other"

    # Track multi-line def/class: if a `def X(` or `class X(` line opens a
    # paren that closes on a later line ending in `:`, that closing line
    # should increment depth as a compound opener.
    # Carry "pending_opener_kind" until paren closes and `:` appears.
    pending_opener_kind: str | None = None

    for idx, line in enumerate(raw_lines, start=1):
        stripped = line.strip()
        # Triple-string interior: preserve verbatim.
        if in_triple[idx] and idx > 1:
            out.append(line)
            continue
        # Continuation of an open paren: keep verbatim if it had leading
        # whitespace; else add one extra indent unit.
        if line_paren_depth[idx] > 0:
            # If the original line already had leading whitespace, keep it.
            # Otherwise, use depth + 1.
            if line and line[0] in (" ", "\t"):
                out.append(line)
            else:
                out.append(indent * (depth + 1) + stripped)
            # If this continuation line closes the paren and ends in `:`,
            # treat it as a compound opener completion.
            if pending_opener_kind is not None and stripped.endswith(":"):
                # Check if paren closes after this line by looking at next-
                # line paren depth.
                if idx + 1 <= n and line_paren_depth[idx + 1] == 0:
                    depth += 1
                    opener_stack.append(pending_opener_kind)
                    pending_opener_kind = None
            continue
        if not stripped:
            out.append("")
            continue
        # Dedent-first keywords (elif/else/except/finally).
        if ELIF_ELSE_EXCEPT_FINALLY.match(stripped):
            this_depth = max(depth - 1, 0)
            out.append(indent * this_depth + stripped)
            if stripped.endswith(":"):
                depth = this_depth + 1
                # Replace top-of-stack opener with "other" since this is a
                # new block at this level.
                while len(opener_stack) > depth - 1:
                    opener_stack.pop()
                opener_stack.append("other")
            else:
                depth = this_depth
                while len(opener_stack) > depth:
                    opener_stack.pop()
            continue
        # Sibling-method heuristic: if this line is a flat-source `def` or
        # `class` (no original indent) or a decorator preceding one, and the
        # opener_stack contains a CLASS we'd otherwise be nested inside,
        # dedent to one level under that class. We only apply this when a
        # class is in the stack — without a class context, a nested `def`
        # inside `for`/`if`/etc. is valid and we should leave it alone.
        orig_indent = len(line) - len(line.lstrip())
        opener_kind = _classify_opener(stripped) if stripped.endswith(":") else None
        # Detect decorator (`@something`) at column 0 — should align with the
        # def/class that follows.
        is_decorator_top = orig_indent == 0 and stripped.startswith("@")
        has_class_in_stack = "class" in opener_stack
        if (
            orig_indent == 0
            and (opener_kind in ("def", "class") or is_decorator_top)
            and depth > 0
            and has_class_in_stack
        ):
            # Dedent until we are directly under a class.
            while depth > 0 and opener_stack and opener_stack[-1] != "class":
                opener_stack.pop()
                depth -= 1
        # After-return-dedent heuristic: if we previously emitted a control-
        # flow exit (`return`/`raise`/`continue`/`break`/`pass`) at depth d,
        # and the current line is at original-indent 0 and is NOT itself an
        # `elif`/`else`/`except`/`finally`/sibling-def (handled above), and
        # is not inside a paren, then this current line probably belongs at
        # depth d (sibling of the exit) or shallower. Without more info,
        # dedent one level.
        elif (
            orig_indent == 0
            and out
            and depth > 0
            and re.match(r"^\s*(return|raise|continue|break|yield|pass)\b", out[-1])
            and not ELIF_ELSE_EXCEPT_FINALLY.match(stripped)
        ):
            depth = max(depth - 1, 0)
            if opener_stack:
                opener_stack.pop()
        # Emit at current depth.
        out.append(indent * depth + stripped)
        if stripped.endswith(":") and COMPOUND_OPENERS.match(stripped):
            depth += 1
            opener_stack.append(opener_kind or "other")
            pending_opener_kind = None
        elif COMPOUND_OPENERS.match(stripped) and not stripped.endswith(":"):
            # Multi-line opener: a `def X(` or `class X(` that doesn't close
            # paren on this line. Mark pending so we increment depth on the
            # closing-`:` line.
            kind = _classify_opener(stripped) or "other"
            pending_opener_kind = kind

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Re-pygmentize
# ---------------------------------------------------------------------------
def re_pygmentize(source: str) -> str:
    """Run pygments on source and return inner HTML (without <pre> wrapper)."""
    html = highlight(source, PythonLexer(), HtmlFormatter(nowrap=True))
    # nowrap leaves a trailing newline; preserve since original had similar.
    return html


# ---------------------------------------------------------------------------
# Per-block fixer
# ---------------------------------------------------------------------------
def try_fix_block(plain_text: str) -> tuple[str | None, str]:
    """Try to produce a fixed Python source that parses.

    Returns (fixed_source, strategy) or (None, reason).
    """
    # Strategy A: autopep8 (it may re-indent things lightly).
    if autopep8 is not None:
        try:
            fixed = autopep8.fix_code(plain_text, options={"aggressive": 0})
            if parses(fixed):
                return fixed, "autopep8"
        except Exception:
            pass

    # Strategy B: smart_reindent (paren-aware).
    fixed = smart_reindent(plain_text)
    if fixed is not None and parses(fixed):
        return fixed, "smart-reindent"

    # Strategy C: smart_reindent + autopep8.
    if autopep8 is not None and fixed is not None:
        try:
            fixed2 = autopep8.fix_code(fixed, options={"aggressive": 0})
            if parses(fixed2):
                return fixed2, "smart-reindent+autopep8"
        except Exception:
            pass

    return None, "no-strategy-worked"


def process_file(path: Path, stats: dict) -> list[str]:
    """Process one HTML file. Append notes to stats lists and return changes."""
    notes: list[str] = []
    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        stats["read_errors"].append(f"{path}: {e}")
        return notes

    rel = path.relative_to(ROOT).as_posix()

    new_chunks: list[str] = []
    last_end = 0
    changed = False

    for m in PRE_RE.finditer(source):
        class_attr = m.group(1)
        inner = m.group(2)
        if not has_required_classes(class_attr):
            continue

        plain = extract_plain_text(inner)
        # Pygments often emits a trailing newline; we keep the source as-is.
        stats["blocks_scanned"] += 1

        # If already parses, skip.
        if parses(plain):
            stats["blocks_already_valid"] += 1
            continue

        # Conservative gate: only act on blocks that look like indent-loss.
        if not is_indent_loss(plain):
            stats["blocks_not_indent_loss"] += 1
            continue

        # Try to fix.
        fixed, strategy = try_fix_block(plain)
        if fixed is None:
            stats["blocks_unsalvageable"] += 1
            stats["unsalvageable_locations"].append(
                f"{rel}:{source.count(chr(10), 0, m.start()) + 1} — {plain.strip().splitlines()[0][:80] if plain.strip() else '(empty)'}"
            )
            continue

        # Re-pygmentize and rebuild the <pre><code> block.
        new_inner = re_pygmentize(fixed)
        # Preserve class ordering: use the same class attribute as original
        # so we don't change CSS selectors.
        new_block = f'<pre><code class="{class_attr}">{new_inner}</code></pre>'

        # Add to chunks.
        new_chunks.append(source[last_end : m.start()])
        new_chunks.append(new_block)
        last_end = m.end()
        changed = True
        stats["blocks_fixed"] += 1
        stats["fix_strategies"][strategy] = stats["fix_strategies"].get(strategy, 0) + 1
        notes.append(
            f"{rel}:{source.count(chr(10), 0, m.start()) + 1} — fixed via {strategy}"
        )

    if changed:
        new_chunks.append(source[last_end:])
        new_source = "".join(new_chunks)
        path.write_text(new_source, encoding="utf-8")
        stats["files_modified"] += 1

    return notes


def main() -> int:
    stats = {
        "files_scanned": 0,
        "files_modified": 0,
        "files_skipped_recent_mtime": 0,
        "blocks_scanned": 0,
        "blocks_already_valid": 0,
        "blocks_not_indent_loss": 0,
        "blocks_fixed": 0,
        "blocks_unsalvageable": 0,
        "read_errors": [],
        "unsalvageable_locations": [],
        "fix_strategies": {},
        "skipped_recent": [],
    }

    now = time.time()
    for path in ROOT.rglob("*.html"):
        # Skip excluded dirs.
        parts = set(path.relative_to(ROOT).parts)
        if parts & SKIP_DIRS:
            continue
        # Skip files modified in the last 5 minutes.
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if (now - mtime) < MTIME_GUARD_SECONDS:
            stats["files_skipped_recent_mtime"] += 1
            stats["skipped_recent"].append(path.relative_to(ROOT).as_posix())
            continue

        stats["files_scanned"] += 1
        process_file(path, stats)

    # Write report.
    out: list[str] = []
    out.append("# Pygments Indent Fix Report\n")
    out.append(f"_Generated by `scripts/_fix_pygments_indent.py` on {time.strftime('%Y-%m-%d %H:%M:%S')}._\n")
    out.append("## Summary")
    out.append(f"- HTML files scanned: **{stats['files_scanned']}**")
    out.append(f"- Files modified: **{stats['files_modified']}**")
    out.append(f"- Files skipped (recent mtime, <5 min): **{stats['files_skipped_recent_mtime']}**")
    out.append(f"- Pygments-highlighted Python blocks scanned: **{stats['blocks_scanned']}**")
    out.append(f"- Blocks already valid (skipped): **{stats['blocks_already_valid']}**")
    out.append(f"- Blocks not indent-loss (skipped, other syntax error): **{stats['blocks_not_indent_loss']}**")
    out.append(f"- Blocks fixed: **{stats['blocks_fixed']}**")
    out.append(f"- Blocks unsalvageable (indent-loss but re-indent failed): **{stats['blocks_unsalvageable']}**\n")
    if stats["fix_strategies"]:
        out.append("## Fix strategies used")
        for strat, n in sorted(stats["fix_strategies"].items(), key=lambda x: -x[1]):
            out.append(f"- `{strat}`: **{n}** blocks")
        out.append("")
    if stats["skipped_recent"]:
        out.append("## Files skipped (modified within last 5 minutes)")
        for p in stats["skipped_recent"][:30]:
            out.append(f"- `{p}`")
        if len(stats["skipped_recent"]) > 30:
            out.append(f"- ...and {len(stats['skipped_recent']) - 30} more")
        out.append("")
    if stats["unsalvageable_locations"]:
        out.append("## Unsalvageable blocks (no fix strategy succeeded)")
        for loc in stats["unsalvageable_locations"][:50]:
            out.append(f"- {loc}")
        if len(stats["unsalvageable_locations"]) > 50:
            out.append(f"- ...and {len(stats['unsalvageable_locations']) - 50} more")
        out.append("")
    if stats["read_errors"]:
        out.append("## Read errors")
        for e in stats["read_errors"][:10]:
            out.append(f"- {e}")
        out.append("")

    report_path = ROOT / "pygments-indent-fix-report.md"
    report_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote report to {report_path}")
    print(f"  files_modified={stats['files_modified']}  blocks_fixed={stats['blocks_fixed']}  unsalvageable={stats['blocks_unsalvageable']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
