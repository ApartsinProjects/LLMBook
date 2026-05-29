"""Code-output drift audit.

Walks every .html file (excluding KDP/, .claude/, temp_*, scripts/, *backups*,
node_modules/, pagefind/, templates/) and inspects every

    <pre><code class="...lang-python..."> ... </code></pre>

that is *immediately* followed by a

    <div class="code-output"> ... </div>

For each (code, output) pair we statically check whether the rendered output is
consistent with what the code would plausibly produce.

The audit is READ-ONLY. Findings are written to
`output-drift-audit.md` at the project root.

Detection signals:
  1. field_name_drift     -- f-string references key K not present in output
  2. key_count_mismatch   -- dict in code has N keys but output shows N+/-1
  3. format_decimal_drift -- f-spec {x:.2f} but output shows .4f or 0 decimals
  4. iteration_count_drift-- range(N) but output shows different # of iterations
  5. removed_print_drift  -- output has a label line that code does not print
  6. added_print_drift    -- code prints a label line that output is missing
  7. type_mismatch_drift  -- code returns dict but output is list-shaped (or v.v.)
  8. string_template_drift-- f-string field order differs from output

Run from the project root:
    /c/Python314/python scripts/_audit_output_drift.py
"""
from __future__ import annotations

import ast
import html as html_lib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORT_PATH = PROJECT_ROOT / "output-drift-audit.md"

EXCLUDE_DIRS = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    ".git", ".html2epub_cache", ".github", "agents", "vendor",
    "source_fix_backups", "__pycache__", "build", "temp_epub",
}
EXCLUDE_PREFIXES = ("temp_",)
EXCLUDE_CONTAINS = ("backups",)


def is_excluded(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
        if any(part.startswith(p) for p in EXCLUDE_PREFIXES):
            return True
        if any(c in part.lower() for c in EXCLUDE_CONTAINS):
            return True
    return False


def collect_html_files() -> list[Path]:
    files = []
    for p in sorted(PROJECT_ROOT.rglob("*.html")):
        if is_excluded(p):
            continue
        files.append(p)
    return files


# ---------------------------------------------------------------------------
# HTML extraction
# ---------------------------------------------------------------------------

def code_text(code_tag: Tag) -> str:
    """Extract plain Python source from a pygments-highlighted <code> block."""
    text = code_tag.get_text()
    # Decode HTML entities that may sneak through.
    text = html_lib.unescape(text)
    # Some files have `<\span>` (typo / publishing artifact) producing
    # stray "\span" tokens after BS get_text(). Strip them.
    text = re.sub(r"<\\span>", "", text)
    text = re.sub(r"\\span", "", text)
    return text


def output_text(div_tag: Tag) -> str:
    """Extract plain text from a code-output div, stripping the label and
    any embedded code-caption divs (which sometimes leak into the panel
    when the HTML is malformed)."""
    # Drop the "Output:" label span if present.
    for label in div_tag.select(".output-label"):
        label.extract()
    # Drop any embedded code-caption that should not be part of the output.
    for cap in div_tag.select(".code-caption"):
        cap.extract()
    text = div_tag.get_text()
    text = html_lib.unescape(text)
    return text.strip()


@dataclass
class Pair:
    file: Path
    rel_path: str
    line: int
    code: str
    output: str
    caption: str


def collect_pairs(path: Path) -> list[Pair]:
    """Find every (lang-python code, immediately-following code-output) pair."""
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    # We compute line numbers from raw string by tracking the offset of each
    # <pre> in the file. BeautifulSoup loses positions, so we re-derive.
    soup = BeautifulSoup(raw, "html.parser")
    pairs: list[Pair] = []

    rel_path = path.relative_to(PROJECT_ROOT).as_posix()

    for pre in soup.find_all("pre"):
        code = pre.find("code")
        if code is None:
            continue
        cls = " ".join(code.get("class", []))
        if "lang-python" not in cls:
            continue
        # Find the next significant sibling.
        nxt = pre.next_sibling
        while isinstance(nxt, NavigableString) and not nxt.strip():
            nxt = nxt.next_sibling
        # Sometimes the pre is the last child of a wrapper -- then ascend.
        if not (isinstance(nxt, Tag) and "code-output" in (nxt.get("class") or [])):
            # Some pages wrap with extra divs; allow climbing one parent.
            parent = pre.parent
            if parent is not None:
                idx = list(parent.children).index(pre)
                # Look at remaining siblings of the parent's children list.
                rest = list(parent.children)[idx + 1:]
                nxt = None
                for sib in rest:
                    if isinstance(sib, NavigableString) and not sib.strip():
                        continue
                    nxt = sib
                    break
        if not (isinstance(nxt, Tag) and "code-output" in (nxt.get("class") or [])):
            continue
        code_src = code_text(code)
        out_src = output_text(nxt)
        if not code_src.strip() or not out_src.strip():
            continue

        # Approximate the source line of the <pre> in the raw file. We
        # locate the next-following `code-output` marker since `<pre>` may
        # be wrapped in a div. The most reliable anchor is the output text:
        # search for its first non-empty line in the raw HTML.
        line = 0
        snippet = ""
        out_first = ""
        for cand_line in out_src.splitlines():
            cand_line = cand_line.strip()
            if cand_line and len(cand_line) >= 8:
                out_first = cand_line[:60]
                break
        if out_first:
            try:
                idx = raw.find(out_first)
                if idx >= 0:
                    line = raw.count("\n", 0, idx) + 1
            except Exception:
                line = 0
        if line == 0:
            # Fall back: find first 30 chars of code's first non-comment line.
            for cl in code_src.splitlines():
                cl = cl.strip()
                if not cl or cl.startswith("#"):
                    continue
                snippet = cl[:30]
                break
            if snippet:
                try:
                    idx = raw.find(snippet)
                    if idx >= 0:
                        line = raw.count("\n", 0, idx) + 1
                except Exception:
                    line = 0

        # Caption: code-output may be followed by code-caption div.
        caption = ""
        sib = nxt.next_sibling
        while isinstance(sib, NavigableString) and not sib.strip():
            sib = sib.next_sibling
        if isinstance(sib, Tag) and "code-caption" in (sib.get("class") or []):
            caption = sib.get_text(" ", strip=True)

        pairs.append(Pair(
            file=path,
            rel_path=rel_path,
            line=line,
            code=code_src,
            output=out_src,
            caption=caption,
        ))
    return pairs


# ---------------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------------

def safe_parse(src: str) -> Optional[ast.AST]:
    # Strip leading "$ " bash markers or pip install lines.
    if not src.strip():
        return None
    try:
        return ast.parse(src)
    except SyntaxError:
        # Try to slice off any trailing/leading non-Python noise (rare).
        return None


@dataclass
class FStringField:
    """One {field} interpolation in an f-string."""
    expr_text: str            # raw expression source (e.g. "x['k']")
    base_keys: list[str]      # subscript keys like 'k' (str only)
    attr_chain: list[str]     # attribute accesses
    var_name: Optional[str]   # leftmost Name (e.g. 'x')
    format_spec: str          # e.g. ".2f", "5d", "<10"
    conversion: Optional[str] # !r, !s, !a


def _expr_to_text(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def _walk_subscripts(node: ast.AST, keys: list[str]) -> None:
    """Collect string keys from chained Subscript nodes."""
    if isinstance(node, ast.Subscript):
        sl = node.slice
        if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
            keys.append(sl.value)
        _walk_subscripts(node.value, keys)


def _walk_attrs(node: ast.AST, attrs: list[str]) -> None:
    if isinstance(node, ast.Attribute):
        attrs.append(node.attr)
        _walk_attrs(node.value, attrs)


def _leftmost_name(node: ast.AST) -> Optional[str]:
    while isinstance(node, (ast.Attribute, ast.Subscript, ast.Call)):
        if isinstance(node, ast.Call):
            node = node.func
        else:
            node = node.value
    if isinstance(node, ast.Name):
        return node.id
    return None


def extract_fstring_fields(joined: ast.JoinedStr) -> list[FStringField]:
    out: list[FStringField] = []
    for piece in joined.values:
        if not isinstance(piece, ast.FormattedValue):
            continue
        keys: list[str] = []
        attrs: list[str] = []
        _walk_subscripts(piece.value, keys)
        _walk_attrs(piece.value, attrs)
        spec = ""
        if isinstance(piece.format_spec, ast.JoinedStr):
            spec_parts = []
            for sp in piece.format_spec.values:
                if isinstance(sp, ast.Constant):
                    spec_parts.append(str(sp.value))
            spec = "".join(spec_parts)
        conversion = None
        if piece.conversion != -1:
            conversion = chr(piece.conversion)
        out.append(FStringField(
            expr_text=_expr_to_text(piece.value),
            base_keys=keys,
            attr_chain=attrs,
            var_name=_leftmost_name(piece.value),
            format_spec=spec,
            conversion=conversion,
        ))
    return out


# ---------------------------------------------------------------------------
# Signal extractors
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    pair: Pair
    signal: str
    detail: str

    def short(self) -> str:
        return f"{self.signal}: {self.detail}"


def _strings_in_print(call: ast.Call) -> list[str]:
    """Return all string literal pieces inside a print() call (across args)."""
    out: list[str] = []
    for arg in call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            out.append(arg.value)
        elif isinstance(arg, ast.JoinedStr):
            for v in arg.values:
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    out.append(v.value)
    return out


def _all_print_calls(tree: ast.AST) -> list[ast.Call]:
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id == "print":
                out.append(node)
    return out


def _print_template_text(call: ast.Call) -> str:
    """Return a flat string of the print template (literal parts joined)."""
    parts: list[str] = []
    for arg in call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            parts.append(arg.value)
        elif isinstance(arg, ast.JoinedStr):
            for v in arg.values:
                if isinstance(v, ast.Constant):
                    parts.append(str(v.value))
                elif isinstance(v, ast.FormattedValue):
                    parts.append("{}")
    return " ".join(p for p in parts if p)


# --- Signal 1: field-name drift -------------------------------------------

# Conservative key list: we only flag keys that look like clear English
# identifiers (>=4 chars, no obvious abbreviations).
def _is_audit_worthy_key(k: str) -> bool:
    if len(k) < 4:
        return False
    if not k.replace("_", "").isalpha():
        return False
    # Skip generic single-letter tokens or pythonic dunders.
    if k.startswith("__"):
        return False
    return True


def signal_field_name_drift(pair: Pair, tree: ast.AST) -> list[str]:
    """A print f-string references key X but X never appears in output.

    Strong signal only: the output text contains a CLOSE VARIANT of the key
    that the literal template text DOES NOT explain. If the f-string's own
    literal pieces contain that variant (e.g. label "Compressed tokens" +
    interpolated value `d['compressed_tokens']`), the variant in the output
    was emitted by the code itself, not drift -- so we must skip.
    """
    findings: list[str] = []
    out_lower = pair.output.lower()
    # Collect ALL literal pieces across every print() in the snippet.
    all_template_literals = ""
    for call in _all_print_calls(tree):
        for arg in call.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                all_template_literals += " " + arg.value
            elif isinstance(arg, ast.JoinedStr):
                for v in arg.values:
                    if isinstance(v, ast.Constant):
                        all_template_literals += " " + str(v.value)
    tmpl_low = all_template_literals.lower()

    for call in _all_print_calls(tree):
        for arg in call.args:
            if not isinstance(arg, ast.JoinedStr):
                continue
            fields = extract_fstring_fields(arg)
            for f in fields:
                for k in f.base_keys:
                    if not _is_audit_worthy_key(k):
                        continue
                    if k.lower() in out_lower:
                        continue
                    variants = _variants_of(k)
                    matched_variant = None
                    for v in variants:
                        if v.lower() == k.lower():
                            continue
                        if v.lower() not in out_lower:
                            continue
                        # SKIP: variant is also a substring of the code's
                        # own literal template (i.e. label text, not output drift).
                        if v.lower() in tmpl_low:
                            continue
                        matched_variant = v
                        break
                    if matched_variant is None:
                        continue
                    findings.append(
                        f"f-string key {k!r} not in output, but variant {matched_variant!r} present"
                    )
    return _unique(findings)


def _variants_of(key: str) -> list[str]:
    """Return plausible variant spellings of a key (singular/plural, underscores)."""
    v = {key}
    if key.endswith("s"):
        v.add(key[:-1])
    else:
        v.add(key + "s")
    if "_" in key:
        v.add(key.replace("_", ""))
        v.add(key.replace("_", " "))
    return list(v)


# --- Signal 2: key-count mismatch -----------------------------------------

def signal_key_count_mismatch(pair: Pair, tree: ast.AST) -> list[str]:
    """A returned/printed dict literal has N keys but output shows N+/-1.

    Heuristic: find dict literals assigned to a variable and then printed.
    Specifically: when the code does `print(d)` and `d = {literal}`, count
    the keys and compare to the count of top-level "key:" pairs in the
    output. To stay conservative we only trigger when the output is clearly
    a single-dict pretty print (starts with `{`).
    """
    findings: list[str] = []
    out = pair.output.strip()
    if not out.startswith("{") or not out.endswith("}"):
        return findings

    # Count top-level pairs in the output: rough split on commas at depth 0.
    out_keys = _count_topdepth_dict_keys(out)
    if out_keys < 2:
        return findings

    # Find the last assigned dict literal whose name is printed in the code.
    assigns: dict[str, ast.Dict] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if (len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.Dict)):
                assigns[node.targets[0].id] = node.value

    last_print_var: Optional[str] = None
    for call in _all_print_calls(tree):
        if (len(call.args) == 1 and isinstance(call.args[0], ast.Name)
                and call.args[0].id in assigns):
            last_print_var = call.args[0].id
    if last_print_var is None:
        return findings
    d = assigns[last_print_var]
    code_keys = len(d.keys)
    if code_keys != out_keys and abs(code_keys - out_keys) <= 3 and code_keys >= 2:
        findings.append(
            f"dict literal `{last_print_var}` has {code_keys} keys, output shows {out_keys}"
        )
    return findings


def _count_topdepth_dict_keys(s: str) -> int:
    """Count comma-separated key:value pairs at depth 1 inside a {...} block."""
    if not (s.startswith("{") and s.endswith("}")):
        return 0
    depth = 0
    count = 0
    in_str: Optional[str] = None
    has_content = False
    for ch in s:
        if in_str:
            if ch == in_str:
                in_str = None
            continue
        if ch in ("'", '"'):
            in_str = ch
            continue
        if ch == "{" or ch == "[" or ch == "(":
            depth += 1
            if depth == 1:
                has_content = False
            continue
        if ch == "}" or ch == "]" or ch == ")":
            depth -= 1
            continue
        if depth == 1:
            if ch == ":":
                # only count colons at depth-1 (one per pair)
                count += 1
            if ch.strip():
                has_content = True
    return count


# --- Signal 3: print-format mismatch (decimals) ---------------------------

DEC_SPEC_RE = re.compile(r"\.(?P<n>\d+)f\b")

def signal_format_decimal_drift(pair: Pair, tree: ast.AST) -> list[str]:
    """f-string format spec .Nf but output shows different decimal count.

    To anchor each f-string field to the right output line we compute a
    *prefix anchor*: the literal text at the very START of the f-string,
    which usually includes a unique line label (e.g. "Before norm:" vs
    "After norm:"). We only consider output lines that start with this
    prefix.
    """
    findings: list[str] = []
    out = pair.output
    for call in _all_print_calls(tree):
        for arg in call.args:
            if not isinstance(arg, ast.JoinedStr):
                continue
            fields = extract_fstring_fields(arg)
            # The "anchor" prefix is the first constant chunk of the f-string.
            anchor = ""
            if arg.values and isinstance(arg.values[0], ast.Constant):
                anchor = str(arg.values[0].value).strip()
            # Strip trailing punctuation/operators.
            anchor_clean = anchor.rstrip(":= ").strip()
            # If the anchor isn't usable, fall back to label-only matching.
            for f in fields:
                m = DEC_SPEC_RE.search(f.format_spec or "")
                if not m:
                    continue
                n_expected = int(m.group("n"))
                label = _label_for_field(arg, f)
                if not label:
                    continue
                label = label.strip().rstrip(":")
                if not label:
                    continue
                # Build candidate output lines: prefer those that start with
                # the anchor. If none, fall back to any line containing the
                # label.
                candidate_lines = []
                if anchor_clean and len(anchor_clean) >= 4:
                    for outline in out.splitlines():
                        if outline.lstrip().lower().startswith(
                                anchor_clean.lower()[:max(8, len(anchor_clean) // 2)]):
                            candidate_lines.append(outline)
                if not candidate_lines:
                    for outline in out.splitlines():
                        if label.lower() in outline.lower():
                            candidate_lines.append(outline)
                            break  # only fallback to first match
                drift_found = False
                for outline in candidate_lines:
                    idx = outline.lower().find(label.lower())
                    if idx < 0:
                        continue
                    tail = outline[idx + len(label):]
                    tail = tail[:80]
                    m_num = re.search(
                        r"(?<![0-9])-?\d+\.(\d+)(?:[eE][+-]?\d+)?", tail
                    )
                    if not m_num:
                        continue
                    pre = tail[: m_num.start()]
                    if "|" in pre:
                        continue
                    n_actual = len(m_num.group(1))
                    if n_actual != n_expected and abs(n_actual - n_expected) >= 1:
                        findings.append(
                            f"`{label}` formatted with .{n_expected}f "
                            f"but output shows {n_actual} decimals "
                            f"({m_num.group(0)})"
                        )
                        drift_found = True
                        break
                    else:
                        # number matches expected decimals; no drift; stop.
                        drift_found = False
                        break
                # else: no candidate line - skip
    return _unique(findings)


def _label_for_field(joined: ast.JoinedStr, target: FStringField) -> str:
    """Return the literal text immediately preceding `target` in the f-string.

    Conservative: only return labels that look like meaningful identifiers
    (a sequence of word characters and spaces ending in `:` or `=`, length
    >= 3 alphanumerics, no commas/pipes in the matched label).
    """
    prev_text = ""
    for v in joined.values:
        if isinstance(v, ast.Constant):
            prev_text += str(v.value)
        elif isinstance(v, ast.FormattedValue):
            cur_expr = _expr_to_text(v.value)
            if cur_expr == target.expr_text:
                # take the trailing fragment of prev_text up to last newline,
                # comma, or pipe.
                tail = re.split(r"[\n|,]", prev_text)[-1]
                # Only accept a label that is a clean word sequence ending
                # in : or = (not capturing any leading garbage).
                m = re.search(r"(?:^|\s)([A-Za-z][\w \-]{2,28})\s*[:=]\s*$", tail)
                if not m:
                    return ""
                lbl = m.group(1).strip()
                # Discard labels whose alphabetic-content is too short.
                if len(re.sub(r"[^A-Za-z0-9]", "", lbl)) < 3:
                    return ""
                return lbl
            prev_text = ""
    return ""


def _unique(seq: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for s in seq:
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


# --- Signal 4: iteration-count drift --------------------------------------

# Conservative: only fire when:
#   - code has a top-level for-loop `for i in range(N):` and N is a constant
#   - the loop body has a print() that includes the loop variable somehow
#   - the output has lines that look like an indexed-iteration block
#   - the count of those lines != N AND |diff| <= 5

def signal_iteration_count_drift(pair: Pair, tree: ast.AST) -> list[str]:
    findings: list[str] = []
    # Count how many sibling print()s OUTSIDE any for-loop share each prefix --
    # those add to the expected line count.
    outside_prefix_count: Counter = Counter()
    for_targets: list[ast.For] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for_targets.append(node)
    in_loop_nodes: set[int] = set()
    for fnode in for_targets:
        for sub in ast.walk(fnode):
            in_loop_nodes.add(id(sub))
    for call in _all_print_calls(tree):
        if id(call) in in_loop_nodes:
            continue
        for a in call.args:
            pref = ""
            if isinstance(a, ast.JoinedStr):
                if a.values and isinstance(a.values[0], ast.Constant):
                    pref = str(a.values[0].value).strip()[:25]
            elif isinstance(a, ast.Constant) and isinstance(a.value, str):
                pref = a.value.strip()[:25]
            if pref and len(pref) >= 4:
                outside_prefix_count[pref] += 1

    for node in for_targets:
        n = _range_const(node.iter)
        if n is None or n < 2 or n > 50:
            continue
        body_prints = [c for c in ast.walk(node) if isinstance(c, ast.Call)
                       and isinstance(c.func, ast.Name) and c.func.id == "print"]
        if not body_prints:
            continue
        prefixes: list[str] = []
        for bp in body_prints:
            for a in bp.args:
                if isinstance(a, ast.JoinedStr):
                    if a.values and isinstance(a.values[0], ast.Constant):
                        prefixes.append(str(a.values[0].value).strip()[:25])
                elif isinstance(a, ast.Constant) and isinstance(a.value, str):
                    prefixes.append(a.value.strip()[:25])
        prefixes = [p for p in prefixes if p and len(p) >= 4]
        if not prefixes:
            continue
        out_lines = pair.output.splitlines()
        for pref in prefixes:
            # Compute extra lines that might be contributed by outside-loop
            # prints sharing this prefix (e.g. "Step 0: ..." printed before
            # the loop body). We subtract those before comparing.
            extra = 0
            for outside_pref, k in outside_prefix_count.items():
                if (outside_pref.startswith(pref[: min(6, len(pref))])
                        or pref.startswith(outside_pref[: min(6, len(outside_pref))])):
                    extra += k
            matches = [ln for ln in out_lines if ln.lstrip().startswith(pref)]
            actual = len(matches) - extra
            if actual >= 2 and actual != n and abs(actual - n) <= 5:
                findings.append(
                    f"for i in range({n}) but output shows {actual} lines "
                    f"starting with {pref!r} (after subtracting {extra} "
                    f"outside-loop print prefixes)"
                )
                break
        if findings:
            break
    return findings


def _range_const(call: ast.AST) -> Optional[int]:
    if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
            and call.func.id == "range"):
        return None
    args = call.args
    if len(args) == 1 and isinstance(args[0], ast.Constant) and isinstance(args[0].value, int):
        return args[0].value
    if len(args) == 2 and all(isinstance(a, ast.Constant) and isinstance(a.value, int) for a in args):
        return args[1].value - args[0].value
    return None


# --- Signal 5 / 6: removed_print / added_print drift ----------------------

# Strategy: For each print() in code, compute a label-shaped prefix
# (text before the first {} in an f-string, or the leading text of the
# string arg). For each output line, check whether *some* code print could
# have produced it. Conversely, for each code print prefix, check whether
# *some* output line starts with it.

LABEL_PREFIX_RE = re.compile(r"^([^\{]+?)[\:=]")

def _print_label_prefixes(tree: ast.AST) -> list[str]:
    out: list[str] = []
    for call in _all_print_calls(tree):
        # Combine literal prefix.
        prefix = ""
        for arg in call.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                prefix = arg.value
                break
            if isinstance(arg, ast.JoinedStr):
                if arg.values and isinstance(arg.values[0], ast.Constant):
                    prefix = str(arg.values[0].value)
                break
        if not prefix:
            continue
        m = LABEL_PREFIX_RE.match(prefix)
        if m:
            label = m.group(1).strip()
        else:
            label = prefix.strip()
        # Heuristic: only useful when label is at least 4 chars and contains
        # at least one letter and is not just punctuation.
        if len(label) >= 4 and re.search(r"[A-Za-z]", label):
            out.append(label)
    return out


_GENERIC_LABELS = {
    "value", "result", "results", "data", "ok", "done", "info",
    "warning", "error", "x", "y", "z", "true", "false", "none", "the",
    "this", "that", "step", "score", "scores", "item", "items",
    "input", "output", "type", "name", "id", "index", "key", "values",
    "count", "total", "mean", "std", "min", "max", "sum", "n", "k",
    "loss", "acc", "accuracy", "predicted", "actual", "label",
}

def signal_added_print_drift(pair: Pair, tree: ast.AST) -> list[str]:
    """A code print() has a distinctive label that NO output line contains."""
    findings: list[str] = []
    labels = _print_label_prefixes(tree)
    out_low = pair.output.lower()
    for lbl in labels:
        lbl_low = lbl.lower()
        if lbl_low in out_low:
            continue
        if lbl_low in _GENERIC_LABELS:
            continue
        if "{" in lbl or "}" in lbl:
            continue
        # Require at least 2 alphabetic tokens or 8 alphanumeric chars
        # (i.e. not a single short word). This filters generic
        # single-word labels like 'Score', 'Step', 'Errors'.
        alpha = re.sub(r"[^A-Za-z0-9]", "", lbl)
        n_tokens = len([t for t in re.split(r"\s+", lbl) if re.search(r"[A-Za-z]", t)])
        if len(alpha) < 8 and n_tokens < 2:
            continue
        if not pair.output.strip():
            continue
        # Also discard labels that are substrings of any line in the output.
        if any(lbl_low in line.lower() for line in pair.output.splitlines()):
            continue
        findings.append(f"print label {lbl!r} not present in output")
    return _unique(findings)[:3]


def signal_removed_print_drift(pair: Pair, tree: ast.AST) -> list[str]:
    """Output contains a label-shaped line that NO code print() emits.

    Conservative: only triggers when the output line clearly looks like a
    label line ("Label: value") and none of the code prints' literal
    prefixes match.

    Skip the whole pair if ANY print() starts with a {variable} (which
    means its prefix is data-driven and we can't statically know what
    label it will produce).
    """
    findings: list[str] = []
    code_prefixes = [p.lower() for p in _print_label_prefixes(tree)]
    if not code_prefixes:
        return findings

    # Detect if any print() starts with a {variable} -- if so the prefix
    # is determined by runtime data and we should not flag labels.
    for call in _all_print_calls(tree):
        for arg in call.args:
            if isinstance(arg, ast.JoinedStr) and arg.values:
                first = arg.values[0]
                # If the first piece is a FormattedValue or a Constant whose
                # value is empty, the print is data-driven.
                if isinstance(first, ast.FormattedValue):
                    return findings
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    if not first.value.strip():
                        return findings

    # Collect strings the code prints anywhere (literal pieces in any
    # print(); ignores f-string interpolated values).
    literal_pieces: list[str] = []
    for call in _all_print_calls(tree):
        for s in _strings_in_print(call):
            literal_pieces.append(s.lower())
    # Also include all string constants anywhere in the source -- e.g.
    # iterables like `[("OpenAI", ...), ("Anthropic", ...)]` are not in
    # print() literal pieces but their strings may appear in output via
    # an interpolated variable.
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            literal_pieces.append(node.value.lower())
    literal_blob = "\n".join(literal_pieces)

    out_lines = [ln.rstrip() for ln in pair.output.splitlines() if ln.strip()]
    PROSE_STARTERS = {
        "the", "a", "an", "this", "that", "these", "those", "we", "you", "i",
        "it", "they", "he", "she", "in", "on", "of", "for", "with", "to",
        "as", "if", "but", "and", "or", "so", "then", "when", "while",
        "first", "second", "third", "next", "let", "let's",
    }
    for ln in out_lines:
        m = re.match(r"^([A-Z][\w \-/]{2,28})\s*[:=]\s*(.+)$", ln)
        if not m:
            continue
        label = m.group(1).strip()
        label_low = label.lower()
        # Drop prose-y labels: start with an article/conjunction word.
        first_word = label_low.split()[0] if label_low.split() else ""
        if first_word in PROSE_STARTERS:
            continue
        if label_low in literal_blob:
            continue
        if any(label_low.startswith(p[:len(label_low)]) for p in code_prefixes):
            continue
        if any(p.startswith(label_low) for p in code_prefixes):
            continue
        if label_low in _GENERIC_LABELS or label_low in {
            "output", "stdout", "stderr", "note", "messages", "given",
            "interpretation", "filtering", "generating",
        }:
            continue
        alpha = re.sub(r"[^A-Za-z0-9]", "", label)
        n_tokens = len([t for t in re.split(r"\s+", label) if re.search(r"[A-Za-z]", t)])
        if len(alpha) < 8 and n_tokens < 2:
            continue
        if "http" in ln.lower() or "://" in ln:
            continue
        findings.append(f"output label {label!r} not printed by any code print()")
    return _unique(findings)[:3]


# --- Signal 7: type mismatch ----------------------------------------------

def signal_type_mismatch(pair: Pair, tree: ast.AST) -> list[str]:
    """A function returns a dict literal but output is list-shaped (or v.v.)."""
    findings: list[str] = []
    # Find every `return <dict|list>` in a function body and a `print(call())`
    # statement that calls that function. Conservative: only top-level prints.
    func_returns: dict[str, str] = {}  # func_name -> "dict" | "list"
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Return) and sub.value is not None:
                    if isinstance(sub.value, ast.Dict):
                        func_returns[node.name] = "dict"
                        break
                    if isinstance(sub.value, (ast.List, ast.ListComp)):
                        func_returns[node.name] = "list"
                        break
    if not func_returns:
        return findings
    out = pair.output.strip()
    if not out:
        return findings
    out_is_dict = out.startswith("{") and out.endswith("}")
    out_is_list = out.startswith("[") and out.endswith("]")
    if not (out_is_dict or out_is_list):
        return findings
    # Find a top-level print(call_to_known_func()).
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "print"):
            continue
        for arg in node.args:
            inner = arg
            if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name):
                fn = inner.func.id
                ret = func_returns.get(fn)
                if ret is None:
                    continue
                if ret == "dict" and out_is_list:
                    findings.append(
                        f"function {fn}() returns dict literal but output is list-shaped"
                    )
                if ret == "list" and out_is_dict:
                    findings.append(
                        f"function {fn}() returns list literal but output is dict-shaped"
                    )
    return _unique(findings)


# --- Signal 8: string-template field-order drift --------------------------

# Conservative: only fire when:
#   - code has a single print(f"a={a} b={b} c={c}")
#   - output line has a=X b=Y c=Z pattern but in a different order

KV_RE = re.compile(r"(\b[\w]{2,30}\b)\s*=\s*([^\s,]+)")

def signal_template_order_drift(pair: Pair, tree: ast.AST) -> list[str]:
    findings: list[str] = []
    for call in _all_print_calls(tree):
        for arg in call.args:
            if not isinstance(arg, ast.JoinedStr):
                continue
            # Build expected order from literal "label=" prefixes.
            order_expected: list[str] = []
            cur = ""
            for v in arg.values:
                if isinstance(v, ast.Constant):
                    cur += str(v.value)
                elif isinstance(v, ast.FormattedValue):
                    m = re.search(r"(\b[\w_]{2,30}\b)\s*=\s*$", cur)
                    if m:
                        order_expected.append(m.group(1))
                    cur = ""
            if len(order_expected) < 3:
                continue
            # Check each line of output for matching k=v patterns.
            for ln in pair.output.splitlines():
                kvs = KV_RE.findall(ln)
                if len(kvs) < len(order_expected):
                    continue
                actual_order = [k for k, _ in kvs[: len(order_expected)]]
                if (set(actual_order) == set(order_expected)
                        and actual_order != order_expected):
                    findings.append(
                        f"f-string field order {order_expected} but output "
                        f"line has {actual_order}"
                    )
                    return _unique(findings)
    return findings


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

SIGNALS = [
    ("field_name_drift", signal_field_name_drift),
    ("key_count_mismatch", signal_key_count_mismatch),
    ("format_decimal_drift", signal_format_decimal_drift),
    ("iteration_count_drift", signal_iteration_count_drift),
    ("added_print_drift", signal_added_print_drift),
    ("removed_print_drift", signal_removed_print_drift),
    ("type_mismatch_drift", signal_type_mismatch),
    ("template_order_drift", signal_template_order_drift),
]


def audit_pair(pair: Pair) -> list[Finding]:
    tree = safe_parse(pair.code)
    if tree is None:
        return []
    out: list[Finding] = []
    for name, fn in SIGNALS:
        try:
            for detail in fn(pair, tree):
                out.append(Finding(pair=pair, signal=name, detail=detail))
        except Exception:
            # Skip detector failures; we are best-effort.
            continue
    return out


def _excerpt(text: str, n_lines: int = 12, max_chars: int = 600) -> str:
    lines = text.splitlines()
    if len(lines) > n_lines:
        lines = lines[:n_lines] + [f"... ({len(text.splitlines()) - n_lines} more lines)"]
    s = "\n".join(lines)
    if len(s) > max_chars:
        s = s[:max_chars] + " ..."
    return s


def main() -> int:
    files = collect_html_files()
    print(f"Scanning {len(files)} HTML files ...", file=sys.stderr)
    all_pairs: list[Pair] = []
    parse_failures = 0
    for p in files:
        try:
            pairs = collect_pairs(p)
        except Exception as e:
            print(f"  ! failed on {p}: {e}", file=sys.stderr)
            continue
        all_pairs.extend(pairs)
    print(f"Found {len(all_pairs)} python-code/output pairs", file=sys.stderr)

    findings: list[Finding] = []
    for pair in all_pairs:
        if safe_parse(pair.code) is None:
            parse_failures += 1
            continue
        findings.extend(audit_pair(pair))

    print(f"  {parse_failures} pair(s) had unparseable Python (skipped)",
          file=sys.stderr)
    print(f"  {len(findings)} total drift findings across signals",
          file=sys.stderr)

    # Group findings by file.
    by_file: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        by_file[f.pair.rel_path].append(f)

    # Rank "worst offenders" by total finding count then by signal weight.
    file_scores: list[tuple[str, int]] = [
        (path, len(items)) for path, items in by_file.items()
    ]
    file_scores.sort(key=lambda kv: (-kv[1], kv[0]))

    signal_counts: Counter = Counter(f.signal for f in findings)

    lines: list[str] = []
    lines.append("# Output-Drift Audit\n")
    lines.append(
        "_Read-only static check of every Python code block immediately followed "
        "by a `<div class=\"code-output\">` pane. Each detector is conservative: "
        "false positives are intentionally minimised, but some discrepancies will "
        "still slip through.\n"
    )
    lines.append(f"- HTML files scanned: **{len(files)}**\n")
    lines.append(f"- Code/output pairs found: **{len(all_pairs)}**\n")
    lines.append(f"- Pairs with unparseable Python (skipped): **{parse_failures}**\n")
    lines.append(f"- Total findings: **{len(findings)}**\n")
    lines.append(f"- Files with at least one finding: **{len(by_file)}**\n\n")

    # 1. Summary by signal
    lines.append("## 1. Summary by signal\n")
    lines.append("| Signal | Count |\n|---|---|\n")
    for name, _ in SIGNALS:
        lines.append(f"| `{name}` | {signal_counts.get(name, 0)} |\n")
    lines.append("\n")

    # 2. Per-file findings.
    lines.append("## 2. Per-file findings\n")
    if not by_file:
        lines.append("_No drift detected._\n\n")
    else:
        for path, items in sorted(by_file.items()):
            lines.append(f"### `{path}`\n\n")
            # Group items at the same line.
            items_by_line: dict[int, list[Finding]] = defaultdict(list)
            for it in items:
                items_by_line[it.pair.line].append(it)
            for line in sorted(items_by_line):
                bullet_items = items_by_line[line]
                for it in bullet_items:
                    lines.append(
                        f"- L{line}: **{it.signal}** -- {it.detail}\n"
                    )
                # One recommended fix per (line,) cluster.
                rec = _recommended_fix(bullet_items)
                if rec:
                    lines.append(f"  - _fix:_ {rec}\n")
            lines.append("\n")

    # 3. Top 10 worst offenders.
    lines.append("## 3. Top 10 worst offenders\n")
    # Score by both count and severity (key_count / type_mismatch /
    # template_order are higher-confidence signals).
    SEV = {
        "key_count_mismatch": 4,
        "type_mismatch_drift": 4,
        "template_order_drift": 3,
        "format_decimal_drift": 3,
        "iteration_count_drift": 3,
        "field_name_drift": 2,
        "added_print_drift": 1,
        "removed_print_drift": 1,
    }
    sev_scored: list[tuple[Finding, int]] = [
        (f, SEV.get(f.signal, 1)) for f in findings
    ]
    sev_scored.sort(key=lambda kv: (-kv[1], kv[0].pair.rel_path, kv[0].pair.line))
    top = sev_scored[:10]
    if not top:
        lines.append("_None._\n\n")
    else:
        for i, (f, sev) in enumerate(top, 1):
            lines.append(
                f"### #{i}: `{f.pair.rel_path}` (L{f.pair.line}, severity {sev})\n\n"
            )
            lines.append(f"**Signal**: `{f.signal}` -- {f.detail}\n\n")
            lines.append("**Code (excerpt)**:\n\n")
            lines.append("```python\n")
            lines.append(_excerpt(f.pair.code, n_lines=14, max_chars=700))
            lines.append("\n```\n\n")
            lines.append("**Output (excerpt)**:\n\n")
            lines.append("```\n")
            lines.append(_excerpt(f.pair.output, n_lines=10, max_chars=500))
            lines.append("\n```\n\n")

    # 4. Recommended next steps.
    lines.append("## 4. Recommended next steps\n\n")
    lines.append(
        "- **Re-run flagged code blocks** locally where they are reproducible "
        "(non-API examples) and paste the actual stdout back into the "
        "`<div class=\"code-output\">` pane.\n"
    )
    lines.append(
        "- **For `key_count_mismatch` findings**, verify whether the example "
        "shrunk the returned dict in code but did not update the panel "
        "(or vice versa). These are usually quick edits.\n"
    )
    lines.append(
        "- **For `format_decimal_drift` findings**, decide whether the panel "
        "or the code is canonical and rewrite the other to match. Watch for "
        "`.2f` vs `:.4f` mismatches in metric tables.\n"
    )
    lines.append(
        "- **For `added_print_drift` and `removed_print_drift`** confirm that "
        "the print or the output line was deliberately edited; the conservative "
        "heuristic will miss many subtle cases.\n"
    )
    lines.append(
        "- **Wire this check into CI** so future code edits without "
        "corresponding output panel updates surface immediately.\n"
    )

    REPORT_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT_PATH} ({sum(len(l) for l in lines)} bytes)",
          file=sys.stderr)
    return 0


def _recommended_fix(items: list[Finding]) -> str:
    sigs = {it.signal for it in items}
    if "key_count_mismatch" in sigs:
        return "regenerate the dict-pretty-print or trim/extend the code to match output"
    if "type_mismatch_drift" in sigs:
        return "either reshape the return value or rewrite the output panel"
    if "format_decimal_drift" in sigs:
        return "align the `.Nf` format spec with the panel"
    if "iteration_count_drift" in sigs:
        return "match `range(N)` to the number of lines in the output"
    if "template_order_drift" in sigs:
        return "reorder the f-string fields or the output line"
    if "field_name_drift" in sigs:
        return "rename the key in code or panel so they match"
    if "added_print_drift" in sigs:
        return "either add the missing line to the output panel or delete the print"
    if "removed_print_drift" in sigs:
        return "either remove the orphan output line or re-add the print"
    return ""


if __name__ == "__main__":
    raise SystemExit(main())
