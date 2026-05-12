"""v6.44b: Fix progressive over-indentation in Python code blocks.

Pattern (broken):
    class Foo:
        def __init__(self):
            self.x = 1
            def fit(self, ...):     <-- WRONG: indent 12, should be 4
                body at indent 16    <-- consequently also wrong
            def predict(self, ...): <-- WRONG: indent 12, should be 4
                body at indent 16
        result = Foo()              <-- module-level code over-indented too

Fix algorithm:
  1. Walk lines, tracking the structural "scope stack" of class/def declarations.
  2. When a `def` or `class` appears at an indent that's LARGER than its
     proper scope position (parent class indent + 4 for methods, or 0 for
     top-level), it's misplaced. Compute its dedent_delta.
  3. Apply that dedent_delta to the line AND every subsequent line that's at
     >= the def's original indent (they're in the def's lexical scope and
     need to follow it down).
  4. Rebuild the source. Validate via ast.parse(). Only write back if the
     fix produces parseable Python.

Conservative: only attempts a fix when the original block has a detectable
"over-nested def in body" pattern. Falls back to no-op if validation fails.
"""
from __future__ import annotations
import ast
import csv
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def lead(line: str) -> int:
    return len(line) - len(line.lstrip())


def find_overnested_def(lines: list[str]) -> tuple[int, int] | None:
    """Find the first 'def' or 'class' line that appears to be over-nested.
    Returns (line_index, dedent_amount) or None if no such line found.

    A line is over-nested if:
      - it is `def NAME(...)` or `class NAME` indented at depth I
      - the immediately preceding non-blank, non-comment line at indent < I
        is BODY code (not a def/class declaration), AND that body code is
        at indent I-4 ... indicating the new def is a nested function inside
        the previous def's body.

    AND: there exists an EARLIER `def`/`class` at indent I (sibling level)
    or the surrounding scope has methods at I, suggesting this def SHOULD
    be at indent I or shallower (not at I+4).
    """
    decl_re = re.compile(r'^(?:async\s+)?(def|class)\s+\w+')
    # First pass: collect all decl lines with their indent
    decls = []  # (line_idx, indent, kind)
    for i, line in enumerate(lines):
        s = line.lstrip()
        if not s or s.startswith('#'):
            continue
        ind = lead(line)
        m = decl_re.match(s)
        if m:
            decls.append((i, ind, m.group(1)))

    # Find the first decl whose indent is bigger than expected
    for k in range(1, len(decls)):
        i, ind, kind = decls[k]
        prev_i, prev_ind, prev_kind = decls[k - 1]
        if ind <= prev_ind:
            continue  # this decl is at sibling-or-shallower level, fine
        # This decl is INSIDE the previous decl's scope.
        # Heuristic: if the indent is exactly prev_ind + 4 (the canonical
        # body indent of prev_decl), AND we can see >= 2 body code lines
        # between prev_i and i at exactly that indent, then this decl is
        # almost certainly a misplaced sibling rather than a true nested
        # function.
        if ind != prev_ind + 4:
            continue
        # Get the new decl's signature (need to look at original line)
        new_sig = lines[i].lstrip()
        # Check 1: is the new decl an obvious class method (takes self/cls)?
        is_method_sig = bool(re.match(
            r'(?:async\s+)?def\s+\w+\s*\(\s*(?:self|cls)\b', new_sig
        ))
        # Check 2: is it a dunder (__init__, __len__, __getitem__, etc.)?
        is_dunder = bool(re.match(r'(?:async\s+)?def\s+__\w+__\s*\(', new_sig))
        # Count body lines between prev decl and this one at the same indent
        body_count = 0
        for j in range(prev_i + 1, i):
            ll = lines[j].lstrip()
            if not ll or ll.startswith('#'):
                continue
            ind_j = lead(lines[j])
            if ind_j == ind and not decl_re.match(ll):
                body_count += 1
        # Trigger if:
        #   - strong signal (dunder OR method-sig) AND any body separation, OR
        #   - weaker signal but >= 2 body lines between
        if (is_method_sig or is_dunder) and body_count >= 1:
            dedent = ind - prev_ind
            return (i, dedent)
        if body_count >= 2:
            dedent = ind - prev_ind
            return (i, dedent)

    # Second pass: detect "class wrongly nested as sibling-of-method"
    # Pattern: a `class X(...)` appears at the same indent as the previous
    # sibling `def method`. If that class has its OWN methods (def lines
    # at class_indent+4), AND its body contains lines that look like
    # module-level code (e.g. assignments where LHS is a name = call),
    # the class was meant to be at module level (indent 0).
    for k in range(1, len(decls)):
        i, ind, kind = decls[k]
        prev_i, prev_ind, prev_kind = decls[k - 1]
        if kind != 'class':
            continue
        if ind == 0:
            continue  # already at module level
        if ind != prev_ind:
            continue  # not at sibling level
        if prev_kind != 'def':
            continue  # previous wasn't a method
        # The new `class` is at the same indent as a method. Check if its
        # body contains "module-level-looking" content.
        # Find body lines after this class
        for j in range(i + 1, min(i + 40, len(lines))):
            ll = lines[j].lstrip()
            if not ll or ll.startswith('#'):
                continue
            ind_j = lead(lines[j])
            if ind_j <= ind:
                break  # exited the class scope
            # If a body line at deep indent looks like top-level code
            # (e.g., `var = ClassName(...)` for an instance creation,
            # or `print(...)` calls), this class is mis-placed.
            if re.match(r'\w+\s*=\s*[A-Z]\w+\s*\(', ll):
                return (i, ind)  # dedent class to module level
            if re.match(r'(?:print|if __name__|sys\.exit)\s*[\(=]', ll):
                return (i, ind)
    return None


def apply_dedent(lines: list[str], start_idx: int, dedent: int) -> list[str]:
    """Dedent line at start_idx and all subsequent lines whose indent is
    >= the line at start_idx's original indent. Stop at the first line
    that is at LOWER indent (we've left the scope)."""
    if start_idx >= len(lines):
        return lines
    start_indent = lead(lines[start_idx])
    out = list(lines)
    for j in range(start_idx, len(lines)):
        s = out[j].lstrip()
        if not s:
            continue  # blank line preserved
        ind = lead(out[j])
        if j > start_idx and ind < start_indent:
            break  # exited the scope
        if ind >= dedent:
            out[j] = ' ' * (ind - dedent) + s
        else:
            # Can't dedent further; leave as-is to avoid corruption
            pass
    return out


def fix_block(code: str) -> tuple[str, bool]:
    """Returns (fixed_code, was_modified). Iteratively un-nests misplaced defs.
    Aborts if at any point ast.parse fails on the result."""
    lines = code.split('\n')
    iterations = 0
    while iterations < 20:  # bail-out: shouldn't take more than ~20 dedents
        spot = find_overnested_def(lines)
        if not spot:
            break
        i, dedent = spot
        lines = apply_dedent(lines, i, dedent)
        iterations += 1
    new_code = '\n'.join(lines)
    if new_code == code:
        return code, False
    # Final validation: must still be parseable Python
    try:
        ast.parse(new_code)
    except SyntaxError:
        # Fix made it worse; abort
        return code, False
    return new_code, True


def strip_pygments(html_block: str) -> str:
    """Extract raw source from <pre><code> with Pygments markup."""
    s = re.sub(r'<[^>]+>', '', html_block)
    return html.unescape(s)


def encode_for_pre(code: str) -> str:
    """Re-encode for HTML: escape < > &, but no Pygments coloring."""
    return (code.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))


def main() -> int:
    fixed_blocks = 0
    files_changed = 0
    failed = 0
    PRE_RE = re.compile(
        r'(<pre>\s*<code[^>]*lang-python[^>]*>)(.+?)(</code>\s*</pre>)',
        re.DOTALL,
    )

    for p in sorted(ROOT.glob('part-*/module-*/section-*.html')):
        text = p.read_text(encoding='utf-8', errors='replace')

        def repl(m: re.Match) -> str:
            nonlocal fixed_blocks, failed
            head, body, tail = m.group(1), m.group(2), m.group(3)
            raw_code = strip_pygments(body)
            new_code, changed = fix_block(raw_code)
            if not changed:
                return m.group(0)
            # Replace the body with re-encoded raw code, dropping Pygments
            # spans. The book.js auto-rehighlight (Prism) will color it.
            new_body = '\n' + encode_for_pre(new_code) + '\n'
            fixed_blocks += 1
            return head + new_body + tail

        new_text = PRE_RE.sub(repl, text)
        if new_text != text:
            files_changed += 1
            p.write_text(new_text, encoding='utf-8')

    print(f'Fixed {fixed_blocks} Python code blocks across {files_changed} files.')
    print(f'(Original Pygments coloring is dropped on fixed blocks; Prism re-highlights.)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
