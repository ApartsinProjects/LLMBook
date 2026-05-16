"""Audit code-block / output / caption pairing across the LLMBook.

Two paired patterns are scanned:

  Pattern A: For every Python code block, decide whether it would actually
             produce output at module level (top-level `print(...)`, top-level
             expression statement returning a value, top-level `for` loop with
             `print(...)`, top-level f-string expression). If yes, flag the
             block when no `<div class="code-output">` immediately follows it.

  Pattern B: For captions / prose that mention "Code Fragment X.Y.Z" (e.g.
             "as shown in Code Fragment 12.3.4 below"), check whether a code
             fragment with that label exists nearby in the same file. Three
             outcomes are tracked:
                - phantom (label does not exist anywhere)
                - remote (label exists in another file)
                - stale  (label exists in this file but is far away, > 3000 chars)

  Anchor verification: search the rest of the book for the Section 30.3.4
             "orphan output" pattern (a <div class="code-output"> that does
             NOT immediately follow a <pre><code>...</code></pre>) so we can
             confirm the previously-fixed bug does not reappear.

Output: code-output-pairing-audit.md at the project root.

Usage: /c/Python314/python scripts/_audit_code_output_pairing.py
"""
from __future__ import annotations

import ast
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------------------------------------------------------
# Paths / exclusions (mirror the existing audits)
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIR_PARTS = {
    "KDP",
    ".claude",
    "scripts",
    "node_modules",
    "pagefind",
    "templates",
    "vendor",
    "agents",
    "__pycache__",
    "temp_epub",
}


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    for ex in EXCLUDE_DIR_PARTS:
        if ex in parts:
            return True
    for p in path.parts:
        pl = p.lower()
        if pl.startswith("temp_") or "backups" in pl:
            return True
        if pl.endswith(".bak.html") or pl.endswith(".bak"):
            return True
    return False


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*.html"):
        if is_excluded(p.relative_to(ROOT)):
            continue
        files.append(p)
    return sorted(files)


# ---------------------------------------------------------------------------
# Caption inventory (label -> list[(file, char_offset)])
# ---------------------------------------------------------------------------

CAPTION_CODE_RE = re.compile(
    r"^\s*code\s+fragment\s+(\d+(?:\.[\dA-Za-z]+)+)", re.IGNORECASE
)

# Where the caption is *anchored* in the source file (character offset
# corresponding to its `sourceline`). Used for proximity checks.
CAPTION_LOCATIONS: dict[str, list[tuple[Path, int]]] = defaultdict(list)


def _path_nl_offsets(text: str) -> list[int]:
    offs = [0]
    for idx, ch in enumerate(text):
        if ch == "\n":
            offs.append(idx + 1)
    return offs


def build_caption_inventory(files: list[Path]) -> None:
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        soup = BeautifulSoup(text, "html.parser")
        nl_offs = _path_nl_offsets(text)
        for cap in soup.find_all("div", class_="code-caption"):
            t = cap.get_text(" ", strip=True)
            m = CAPTION_CODE_RE.match(t)
            if not m:
                continue
            line = cap.sourceline or 1
            char_off = nl_offs[line - 1] if 1 <= line <= len(nl_offs) else 0
            CAPTION_LOCATIONS[m.group(1)].append((path, char_off))


# ---------------------------------------------------------------------------
# AST analysis for "would this code produce output?"
# ---------------------------------------------------------------------------

# Common heredoc/Jinja escapes inside Pygments markup that ast.parse rejects.
JINJA_LIKE_RE = re.compile(r"\{\{.*?\}\}|\{%.*?%\}")


def extract_code_text(code_el: Tag) -> str:
    """Reconstruct source text from a Pygments / Prism-decorated <code> tree."""
    # get_text already inlines all the span content; we keep newlines.
    return code_el.get_text("", strip=False)


def get_code_classes(code_el: Tag) -> list[str]:
    cls = code_el.get("class") or []
    if isinstance(cls, str):
        return [cls]
    return list(cls)


def is_python_code(code_el: Tag) -> bool:
    cls = get_code_classes(code_el)
    return any("lang-python" in c.lower() for c in cls)


def parse_safely(src: str) -> ast.Module | None:
    """Best-effort parse. Returns None on SyntaxError."""
    # Strip Jinja-like placeholders (`{{ x }}`) which appear in templates.
    cleaned = JINJA_LIKE_RE.sub("PLACEHOLDER", src)
    try:
        return ast.parse(cleaned)
    except SyntaxError:
        return None
    except (ValueError, RecursionError):
        return None


def stmt_produces_output(node: ast.stmt) -> tuple[bool, str]:
    """Decide whether a top-level statement would print something.

    Returns (will_print, reason) where reason is a short human-readable label
    used in the report (truncated to one line).
    """
    # 1) Direct `print(...)` call
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
        func = node.value.func
        # `print(...)`
        if isinstance(func, ast.Name) and func.id == "print":
            return True, _summarise(node, prefix="print")
        # `pprint(...)`
        if isinstance(func, ast.Name) and func.id in {"pprint", "display"}:
            return True, _summarise(node, prefix=func.id)
        # `sys.stdout.write(...)`
        if isinstance(func, ast.Attribute):
            full = _dotted_name(func)
            if full in {
                "sys.stdout.write",
                "sys.stderr.write",
                "logger.info",
                "logging.info",
                "logger.debug",
                "logging.debug",
                "logger.warning",
                "logging.warning",
                "logger.error",
                "logging.error",
                "console.print",
                "rich.print",
            }:
                return True, _summarise(node, prefix=full)

    # 2) Top-level bare expression that yields a value in a REPL.
    #    e.g. `df.head()`, `model.summary()`, a literal, etc.
    if isinstance(node, ast.Expr):
        v = node.value
        # f-strings, plain strings, numbers used as section dividers: count
        # as "output-producing" if they appear bare at module level.
        if isinstance(v, ast.JoinedStr):
            return True, "f-string at module level"
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            # Bare docstring at top of module is NOT output (we'll skip
            # when it's the first statement). Otherwise treat as output.
            return True, f"bare string {repr(v.value)[:40]}"
        if isinstance(v, ast.Call):
            func = v.func
            # `something.head()`, `.tail()`, `.show()`, `.summary()`,
            # `.describe()`, `.info()`, `.plot()` - common pandas/sklearn
            # REPL-style display calls.
            if isinstance(func, ast.Attribute) and func.attr in {
                "head",
                "tail",
                "describe",
                "info",
                "summary",
                "show",
                "plot",
                "value_counts",
                "items",
            }:
                return True, _summarise(node, prefix="." + func.attr + "()")
        # Bare name like `df` or `model` at module level - displayed in REPL,
        # but in a .py script it's silent. Conservative: do NOT flag.

    # 3) Top-level `for` loop with `print(...)` (or similar) in body.
    if isinstance(node, ast.For):
        for child in ast.walk(node):
            if child is node:
                continue
            if isinstance(child, ast.Call):
                func = child.func
                if isinstance(func, ast.Name) and func.id == "print":
                    return True, "for-loop with print()"

    # 4) `with` block containing print at top level
    if isinstance(node, ast.With):
        for child in ast.walk(node):
            if child is node:
                continue
            if isinstance(child, ast.Call):
                func = child.func
                if isinstance(func, ast.Name) and func.id == "print":
                    return True, "with-block containing print()"

    # 5) `if __name__ == "__main__":` block; treat as output-producing if it
    #    contains a print().
    if isinstance(node, ast.If):
        for child in ast.walk(node):
            if child is node:
                continue
            if isinstance(child, ast.Call):
                func = child.func
                if isinstance(func, ast.Name) and func.id == "print":
                    return True, "if-block containing print()"
    return False, ""


def _dotted_name(attr: ast.Attribute) -> str:
    parts: list[str] = []
    cur: ast.expr = attr
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
    return ".".join(reversed(parts))


def _summarise(node: ast.stmt, prefix: str = "") -> str:
    try:
        s = ast.unparse(node)
    except Exception:
        s = prefix or "<expr>"
    s = " ".join(s.split())
    return s[:80] + ("..." if len(s) > 80 else "")


def block_is_definition_only(tree: ast.Module) -> bool:
    """A fragment that is ONLY imports + function/class definitions + simple
    constants is definition-only - output wouldn't make sense."""
    for stmt in tree.body:
        if isinstance(stmt, (
            ast.Import, ast.ImportFrom,
            ast.FunctionDef, ast.AsyncFunctionDef,
            ast.ClassDef,
        )):
            continue
        # Module-level assignments to constants / config dicts are OK
        if isinstance(stmt, ast.Assign):
            continue
        if isinstance(stmt, ast.AnnAssign):
            continue
        # Bare docstring at top
        if (isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)):
            # Treat single bare string as docstring; multiple strings as
            # output statements (which means it's NOT definition-only).
            continue
        # Anything else (Expr, For, If, With, Try, ...) breaks the "definition only"
        return False
    return True


def analyse_code_for_output(src: str) -> tuple[bool, str]:
    """Return (would_produce_output, reason). reason is empty if not."""
    tree = parse_safely(src)
    if tree is None:
        return False, ""
    # Definition-only? then no output expected.
    if block_is_definition_only(tree):
        return False, ""
    # Scan top-level statements.
    # Find FIRST statement that produces output and return its reason.
    for stmt in tree.body:
        produces, reason = stmt_produces_output(stmt)
        if produces:
            return True, reason
    return False, ""


# ---------------------------------------------------------------------------
# Pattern A: code blocks that should have output but don't
# ---------------------------------------------------------------------------


def next_sibling_is_code_output(pre: Tag) -> bool:
    """True if `<div class="code-output">` follows this `<pre>` within the same
    parent block, allowing at most one `<div class="code-caption">` to come
    between them (in either order). Both orderings appear in the book:

      Canonical:    <pre>, <code-output>, <code-caption>
      Variant A.1:  <pre>, <code-caption>, <code-output>
      Variant A.2:  <pre><code-caption>, <code-output>   (no whitespace)
    """
    sib = pre.next_sibling
    skipped_caption = False
    while sib is not None:
        if isinstance(sib, NavigableString):
            if sib.strip() == "":
                sib = sib.next_sibling
                continue
            # Non-whitespace text breaks the chain.
            return False
        if isinstance(sib, Tag):
            classes = sib.get("class") or []
            if isinstance(classes, str):
                classes = [classes]
            if "code-output" in classes:
                return True
            if "code-caption" in classes and not skipped_caption:
                skipped_caption = True
                sib = sib.next_sibling
                continue
            return False
        sib = sib.next_sibling
    return False


def find_line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _find_caption_label_for_pre(pre: Tag) -> str:
    """Walk forward siblings of a `<pre>` looking for the first
    `<div class="code-caption">`. Stop at the next `<pre>` (so we don't
    attribute a sibling code block's caption to ours)."""
    sib = pre.next_sibling
    while sib is not None:
        if isinstance(sib, NavigableString):
            sib = sib.next_sibling
            continue
        if isinstance(sib, Tag):
            if sib.name == "pre":
                return ""
            classes = sib.get("class") or []
            if isinstance(classes, str):
                classes = [classes]
            if "code-caption" in classes:
                t = sib.get_text(" ", strip=True)
                m = re.match(
                    r"\s*Code\s+Fragment\s+(\d+(?:\.[\dA-Za-z]+)+)",
                    t, re.IGNORECASE,
                )
                if m:
                    return m.group(1)
                return ""
            # Section/heading: we've moved past this block; no caption
            if sib.name in {"h2", "h3", "h4", "h5"}:
                return ""
        sib = sib.next_sibling
    return ""


# ---------------------------------------------------------------------------
# Pattern B: caption/prose references to code fragments
# ---------------------------------------------------------------------------

CODE_FRAGMENT_REF_RE = re.compile(
    r"\bCode\s+Fragment\s+(\d+(?:\.[\dA-Za-z]+)+)(?![\dA-Za-z\.])",
    re.IGNORECASE,
)

# How close (in characters within the same file) we consider a reference to
# be "next to" its target. 3000 chars is roughly ~50 lines.
PROXIMITY_THRESHOLD = 3000


def classify_reference(
    ref_file: Path,
    ref_offset: int,
    label: str,
) -> tuple[str, str]:
    """Return (status, detail) where status is one of:
        - "ok"         : target in same file within threshold
        - "stale"      : target in same file but > threshold chars away
        - "remote"     : target is only in other files
        - "phantom"    : target does not exist anywhere
        - "ambiguous"  : multiple targets across files (rare)
    detail is a human-readable summary used in the report.
    """
    locs = CAPTION_LOCATIONS.get(label, [])
    if not locs:
        return "phantom", "no caption with this label anywhere"

    same_file = [(p, off) for (p, off) in locs if p == ref_file]
    if not same_file:
        files_str = ", ".join(sorted({relfmt(p) for (p, _) in locs})[:3])
        return "remote", f"label exists only in {files_str}"

    # Among same-file targets, the closest one
    nearest = min(same_file, key=lambda po: abs(po[1] - ref_offset))
    distance = abs(nearest[1] - ref_offset)
    if distance <= PROXIMITY_THRESHOLD:
        return "ok", f"target {distance} chars away"
    return "stale", f"target in same file but {distance} chars away"


# ---------------------------------------------------------------------------
# Anchor verification: orphan <div class="code-output"> blocks
# ---------------------------------------------------------------------------


def is_orphan_code_output(div: Tag) -> bool:
    """True if this `<div class="code-output">` does NOT have a preceding
    `<pre>...</pre>` (a `<div class="code-caption">` is allowed between them).
    We walk previous siblings and look for the nearest non-whitespace tag.
    """
    sib = div.previous_sibling
    skipped_caption = False
    while sib is not None:
        if isinstance(sib, NavigableString):
            if sib.strip() == "":
                sib = sib.previous_sibling
                continue
            # Non-whitespace text just before -> orphan
            return True
        if isinstance(sib, Tag):
            if sib.name == "pre":
                return False
            classes = sib.get("class") or []
            if isinstance(classes, str):
                classes = [classes]
            # Some books wrap <pre> in <div class="code-block-wrapper">. We
            # treat a wrapper-class sibling as paired if it contains a <pre>.
            if "code-block-wrapper" in classes:
                if sib.find("pre") is not None:
                    return False
            # Allow a single <div class="code-caption"> between pre and output
            if "code-caption" in classes and not skipped_caption:
                skipped_caption = True
                sib = sib.previous_sibling
                continue
            return True
        sib = sib.previous_sibling
    return True


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def relfmt(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------


def scan_file(path: Path) -> dict:
    try:
        html_text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    soup = BeautifulSoup(html_text, "html.parser")
    out = {
        "pattern_a": [],   # missing output
        "pattern_b": [],   # caption/prose refs
        "orphans":   [],   # anchor verification: orphan code-output blocks
        "n_code_blocks_scanned": 0,
        "n_python_blocks": 0,
        "n_captions_scanned": 0,
    }

    # --- Pattern A and orphan check use <pre><code>
    for pre in soup.find_all("pre"):
        code = pre.find("code")
        if code is None:
            continue
        out["n_code_blocks_scanned"] += 1
        if not is_python_code(code):
            continue
        out["n_python_blocks"] += 1
        src = extract_code_text(code)
        if not src.strip():
            continue
        produces, reason = analyse_code_for_output(src)
        if not produces:
            continue
        if next_sibling_is_code_output(pre):
            continue
        # Find caption associated with THIS block: walk forward siblings
        # until we hit a `<div class="code-caption">` (or run out of siblings
        # / hit another <pre> meaning we're past our block).
        caption_label = _find_caption_label_for_pre(pre)
        # Use BeautifulSoup's sourceline for accurate line numbers
        line = pre.sourceline or 0
        out["pattern_a"].append({
            "line": line,
            "caption_label": caption_label,
            "reason": reason,
            "code_preview": " ".join(src.split())[:120],
        })

    # --- Pattern B: scan caption / prose for "Code Fragment X.Y.Z" refs
    # We look in three sources:
    #   (a) <p> tags in body (prose)
    #   (b) <figcaption>, <div class="code-caption">, <div class="diagram-caption">
    #   (c) <li> tags (sometimes used for ordered lists referencing fragments)
    candidates: list[Tag] = []
    candidates.extend(soup.find_all("p"))
    candidates.extend(soup.find_all("figcaption"))
    candidates.extend(soup.find_all("li"))
    candidates.extend(soup.find_all("div", class_=["code-caption", "diagram-caption"]))

    seen_refs: set[tuple[str, int]] = set()
    # Build sourceline -> char-offset lookup table for proximity checks.
    nl_offsets = [0]
    for idx, ch in enumerate(html_text):
        if ch == "\n":
            nl_offsets.append(idx + 1)

    def line_to_offset(line: int) -> int:
        if 1 <= line <= len(nl_offsets):
            return nl_offsets[line - 1]
        return 0

    for cap in candidates:
        text = cap.get_text(" ", strip=True)
        if not text:
            continue
        out["n_captions_scanned"] += 1
        # Determine own caption label (so we don't flag self-reference)
        own_label = ""
        m_own = re.match(
            r"\s*Code\s+Fragment\s+(\d+(?:\.[\dA-Za-z]+)+)",
            text, re.IGNORECASE,
        )
        if m_own and "code-caption" in (cap.get("class") or []):
            own_label = m_own.group(1)
        line = cap.sourceline or 0
        offset = line_to_offset(line)
        for m in CODE_FRAGMENT_REF_RE.finditer(text):
            label = m.group(1)
            if label == own_label:
                continue
            key = (label, offset)
            if key in seen_refs:
                continue
            seen_refs.add(key)
            status, detail = classify_reference(path, offset, label)
            if status == "ok":
                continue  # nothing to report
            out["pattern_b"].append({
                "line": line,
                "label": label,
                "status": status,
                "detail": detail,
                "context": text[:180],
                "container": cap.name + (
                    "." + ".".join(cap.get("class") or [])
                    if cap.get("class") else ""
                ),
            })

    # --- Orphan check (anchor verification)
    for div in soup.find_all("div", class_="code-output"):
        if not is_orphan_code_output(div):
            continue
        line = div.sourceline or 0
        # Flatten preview: collapse all whitespace and escape table-breaking
        # characters so we can include it inline in a markdown table row.
        preview = " ".join(div.get_text(" ", strip=True).split())
        preview = preview.replace("|", "\\|").replace("#", "\\#")
        out["orphans"].append({
            "line": line,
            "preview": preview[:140],
        })

    return out


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def write_report(
    files: list[Path],
    results: dict[Path, dict],
) -> Path:
    out_path = ROOT / "code-output-pairing-audit.md"
    lines: list[str] = []

    # Summary numbers
    total_files = len(files)
    n_code_blocks = sum(r["n_code_blocks_scanned"] for r in results.values())
    n_python_blocks = sum(r["n_python_blocks"] for r in results.values())
    n_captions = sum(r["n_captions_scanned"] for r in results.values())
    a_findings: list[tuple[Path, dict]] = []
    b_findings: list[tuple[Path, dict]] = []
    orphan_findings: list[tuple[Path, dict]] = []
    for p, r in results.items():
        for it in r["pattern_a"]:
            a_findings.append((p, it))
        for it in r["pattern_b"]:
            b_findings.append((p, it))
        for it in r["orphans"]:
            orphan_findings.append((p, it))

    a_files = {p for p, _ in a_findings}
    b_files = {p for p, _ in b_findings}
    both_files = a_files & b_files
    a_only_files = a_files - b_files
    b_only_files = b_files - a_files

    b_by_status: Counter = Counter()
    for _, it in b_findings:
        b_by_status[it["status"]] += 1

    lines.append("# Code Output / Caption Pairing Audit")
    lines.append("")
    lines.append(
        f"Scanned **{total_files}** HTML files. "
        f"{n_python_blocks} Python code blocks of {n_code_blocks} total. "
        f"{n_captions} caption/prose containers scanned for cross-references. "
        f"Caption inventory: **{len(CAPTION_LOCATIONS)}** distinct Code-Fragment labels."
    )
    lines.append("")

    # -----------------------------------------------------------------
    # 1. Summary
    # -----------------------------------------------------------------
    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Pattern | Count | Files affected |")
    lines.append("|---|---:|---:|")
    lines.append(f"| A. Code blocks missing expected output | {len(a_findings)} | {len(a_files)} |")
    lines.append(f"| B. Caption/prose references with pairing issues | {len(b_findings)} | {len(b_files)} |")
    lines.append(f"| Orphan `<div class=\"code-output\">` blocks (anchor check) | {len(orphan_findings)} | {len({p for p, _ in orphan_findings})} |")
    lines.append("")
    lines.append("| Overlap | Files |")
    lines.append("|---|---:|")
    lines.append(f"| A only | {len(a_only_files)} |")
    lines.append(f"| B only | {len(b_only_files)} |")
    lines.append(f"| Both A and B | {len(both_files)} |")
    lines.append("")
    lines.append("Pattern B sub-breakdown:")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---:|")
    for st in ("phantom", "remote", "stale", "ambiguous"):
        lines.append(f"| {st} | {b_by_status.get(st, 0)} |")
    lines.append("")

    # -----------------------------------------------------------------
    # 2. Pattern A findings
    # -----------------------------------------------------------------
    lines.append("## 2. Pattern A - Code blocks that should produce output but have none")
    lines.append("")
    lines.append(
        "Each row is a `<pre><code class='...lang-python...'>` block whose top-level "
        "statements include a `print(...)`, an f-string, a REPL-style display call "
        "(`.head()`, `.summary()`, ...), or a `for`/`with`/`if` block containing `print(...)`, "
        "but no `<div class=\"code-output\">` follows it. Excludes definition-only blocks."
    )
    lines.append("")
    if not a_findings:
        lines.append("_No findings._")
    else:
        # Group by file, sort
        a_findings.sort(key=lambda fp: (relfmt(fp[0]), fp[1]["line"]))
        # Split into two buckets: blocks WITH a Code Fragment caption (higher
        # priority - these are first-class fragments where output is expected)
        # and blocks WITHOUT (often inline `Library Shortcut` snippets which
        # may have been written illustratively).
        captioned = [(f, it) for f, it in a_findings if it["caption_label"]]
        uncaptioned = [(f, it) for f, it in a_findings if not it["caption_label"]]
        lines.append(
            f"**Of {len(a_findings)} total blocks:** "
            f"{len(captioned)} have a `Code Fragment X.Y.Z` caption (higher priority), "
            f"{len(uncaptioned)} are uncaptioned (often Library-Shortcut callouts)."
        )
        lines.append("")
        # Show ALL captioned (these matter most)
        lines.append(f"### 2.1 Captioned blocks missing output ({len(captioned)})")
        lines.append("")
        if captioned:
            lines.append("| File:Line | Caption | Output construct | Code preview |")
            lines.append("|---|---|---|---|")
            for f, it in captioned:
                cap_lbl = f"`{it['caption_label']}`"
                preview = it["code_preview"].replace("|", "\\|")
                reason = it["reason"].replace("|", "\\|")
                lines.append(
                    f"| `{relfmt(f)}`:{it['line']} | {cap_lbl} | "
                    f"`{reason}` | `{preview[:80]}` |"
                )
        else:
            lines.append("_None._")
        lines.append("")
        # Show grouped summary for uncaptioned + a sample
        lines.append(f"### 2.2 Uncaptioned blocks missing output ({len(uncaptioned)})")
        lines.append("")
        # Group by file
        by_file: Counter = Counter()
        for f, _ in uncaptioned:
            by_file[relfmt(f)] += 1
        if by_file:
            lines.append("Top 25 files by uncaptioned-block count:")
            lines.append("")
            lines.append("| File | # blocks |")
            lines.append("|---|---:|")
            for filename, n in by_file.most_common(25):
                lines.append(f"| `{filename}` | {n} |")
        else:
            lines.append("_None._")
    lines.append("")

    # -----------------------------------------------------------------
    # 3. Pattern B findings
    # -----------------------------------------------------------------
    lines.append("## 3. Pattern B - Caption/prose references with pairing issues")
    lines.append("")
    lines.append(
        "Prose or caption text mentions `Code Fragment X.Y.Z` but the target is either "
        "missing, in another file, or far away (> 3000 chars) in the same file. "
        "Self-references (a caption mentioning its own number) are excluded."
    )
    lines.append("")
    if not b_findings:
        lines.append("_No findings._")
    else:
        b_findings.sort(key=lambda fp: (fp[1]["status"], relfmt(fp[0]), fp[1]["line"]))
        # Split by status
        by_status: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
        for f, it in b_findings:
            by_status[it["status"]].append((f, it))
        for status in ("phantom", "stale", "remote", "ambiguous"):
            rows = by_status.get(status, [])
            if not rows:
                continue
            lines.append(f"### 3.{ ['phantom','stale','remote','ambiguous'].index(status) + 1} `{status}` references ({len(rows)})")
            lines.append("")
            # For stale references, also explain why they're flagged: most
            # come from "Hands-On Lab" or "Try This" callouts that reference
            # fragments earlier in the chapter - in those cases the long
            # distance is by-design and not actually a bug.
            if status == "stale":
                lines.append(
                    "Sorted by distance descending. The largest distances are "
                    "almost always references in end-of-chapter exercises pointing "
                    "back to fragments earlier in the chapter; these are valid "
                    "long-range references, not refactor leftovers. Pay attention "
                    "to references with distances **< 10,000 chars** in particular: "
                    "those are most likely to be unintended."
                )
                lines.append("")
                # Sort by distance ascending (smallest first - more likely bug)
                def _extract_dist(it):
                    m = re.search(r"(\d+)\s*chars", it["detail"])
                    return int(m.group(1)) if m else 0
                rows = sorted(rows, key=lambda fp: _extract_dist(fp[1]))
            lines.append("| File:Line | Container | Cited as | Detail | Context |")
            lines.append("|---|---|---|---|---|")
            # Cap each section at 40 rows
            for f, it in rows[:40]:
                ctx = it["context"].replace("|", "\\|").replace("\n", " ")
                detail = it["detail"].replace("|", "\\|")
                lines.append(
                    f"| `{relfmt(f)}`:{it['line']} | `{it['container']}` | "
                    f"`{it['label']}` | {detail} | {ctx[:100]} |"
                )
            if len(rows) > 40:
                lines.append("")
                lines.append(f"... and {len(rows) - 40} more `{status}` rows.")
            lines.append("")

    # -----------------------------------------------------------------
    # 4. Anchor verification
    # -----------------------------------------------------------------
    lines.append("## 4. Anchor verification - Section 30.3.4 orphan-output bug")
    lines.append("")
    lines.append(
        "The previously-fixed bug was a `<div class=\"code-output\">` block that "
        "appeared in the source file without an immediately preceding "
        "`<pre>...</pre>`. We scan the entire book for any other "
        "`code-output` div whose previous element-level sibling is not a `<pre>` "
        "(or a `code-block-wrapper` containing one)."
    )
    lines.append("")
    if not orphan_findings:
        lines.append(
            "**No orphan `<div class=\"code-output\">` blocks elsewhere in the book.** "
            "The Section 30.3.4 fix did not have to be applied anywhere else."
        )
    else:
        lines.append(
            f"Found **{len(orphan_findings)}** orphan output blocks across "
            f"**{len({p for p, _ in orphan_findings})}** files."
        )
        lines.append("")
        lines.append("| File:Line | Output preview |")
        lines.append("|---|---|")
        orphan_findings.sort(key=lambda fp: (relfmt(fp[0]), fp[1]["line"]))
        for f, it in orphan_findings:
            prev = it["preview"].replace("|", "\\|")
            lines.append(f"| `{relfmt(f)}`:{it['line']} | {prev[:140]} |")
    lines.append("")

    # -----------------------------------------------------------------
    # 5. Recommended next steps
    # -----------------------------------------------------------------
    lines.append("## 5. Recommended next steps")
    lines.append("")
    bullets: list[str] = []
    if a_findings:
        bullets.append(
            f"**Pattern A ({len(a_findings)} blocks):** For each block, decide if "
            "(a) the code is illustrative and we should add a `# Output:` comment "
            "to a `<div class=\"code-output\">`, (b) the original output was lost "
            "during refactoring and needs reconstruction (run the code, paste the "
            "result), or (c) the `print(...)` is incidental and we should leave it. "
            "Highest priority: blocks whose caption explicitly says \"prints X\" or "
            "\"outputs Y\"."
        )
    if b_by_status.get("phantom", 0) > 0:
        bullets.append(
            f"**Pattern B / phantom ({b_by_status['phantom']} refs):** Captions or prose "
            "say \"Code Fragment X.Y.Z\" but no such fragment exists. Either retarget "
            "to an existing fragment or rewrite the sentence."
        )
    if b_by_status.get("stale", 0) > 0:
        bullets.append(
            f"**Pattern B / stale ({b_by_status['stale']} refs):** Target exists in the "
            "same file but is more than ~50 lines away. Often a leftover from a "
            "refactor that moved the fragment but did not move the surrounding prose."
        )
    if b_by_status.get("remote", 0) > 0:
        bullets.append(
            f"**Pattern B / remote ({b_by_status['remote']} refs):** Reference points "
            "to a fragment in another file. May be intentional cross-section "
            "reference; consider hyperlinking these explicitly with `<a href=...>` "
            "instead of plain text."
        )
    if orphan_findings:
        bullets.append(
            f"**Orphan `code-output` divs ({len(orphan_findings)} found):** Re-pair "
            "each block with the correct preceding `<pre>` or delete the output if "
            "the code was removed during a refactor (this is the Section 30.3.4 "
            "anchor pattern)."
        )
    if not bullets:
        bullets.append(
            "**No action required.** Both patterns came back clean and no other "
            "orphan output divs were found. Re-run after any structural change "
            "(renumbering, deletion of code fragments, restructure of sections)."
        )
    bullets.append(
        "**Re-run after fixes:** "
        "`/c/Python314/python scripts/_audit_code_output_pairing.py`"
    )
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------


def main() -> int:
    sys.stderr.write("Discovering HTML files...\n")
    files = iter_html_files()
    sys.stderr.write(f"  {len(files)} files in scope\n")
    sys.stderr.write("Building caption inventory...\n")
    build_caption_inventory(files)
    sys.stderr.write(
        f"  {len(CAPTION_LOCATIONS)} distinct Code-Fragment labels\n"
    )
    sys.stderr.write("Scanning files...\n")
    results: dict[Path, dict] = {}
    for i, p in enumerate(files):
        r = scan_file(p)
        if r and (r["pattern_a"] or r["pattern_b"] or r["orphans"]):
            results[p] = r
        else:
            # Still keep counters; create an empty record so the totals add up.
            results[p] = r
        if (i + 1) % 100 == 0:
            sys.stderr.write(
                f"  {i + 1}/{len(files)} scanned, "
                f"{sum(1 for v in results.values() if v.get('pattern_a') or v.get('pattern_b') or v.get('orphans'))} flagged\n"
            )
    sys.stderr.write("Writing report...\n")
    out = write_report(files, results)
    sys.stderr.write(f"Report written to {out}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
