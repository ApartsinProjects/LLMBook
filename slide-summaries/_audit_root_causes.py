"""Comprehensive book-wide root-cause audit.

Detects formatting / rendering issues across ALL HTML in:
  - part-*/module-*/section-*.html
  - appendices/appendix-*/section-*.html
  - front-matter/*.html

Categorizes each finding by root cause (RC1-RC5) so a downstream
fixer can apply systemic remediations.

Root causes:
  RC1: Missing KaTeX include in files that contain math.
  RC2: Overflow-prone math (display equations >120 chars without \\\\ break,
       inline math >60 chars).
  RC3: Overflow-prone non-math (wide tables, long pre/code lines,
       SVGs without max-width, missing img max-width).
  RC4: Math inside special containers (callout/caption/figcaption) where
       KaTeX auto-render config might skip rendering.
  RC5: HTML structure inconsistencies (caption above code/figure instead of
       below, missing alt, callout typos, pre without code-block-wrapper).
"""

from __future__ import annotations
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

SECTION_GLOBS = [
    "part-*/module-*/section-*.html",
    "appendices/appendix-*/section-*.html",
    "front-matter/*.html",
]

VALID_CALLOUT_CLASSES = {
    # Authoritative list: every class with a defined ::after icon or
    # bespoke styling in styles/book.css. Keep this set in sync with
    # the grep `grep -oE '\.callout\.[a-z\-]+' styles/book.css`.
    "algorithm", "big-picture", "cross-ref", "exercise",
    "fun-note", "key-insight", "key-takeaway", "lab",
    "library-shortcut", "looking-back", "note", "numeric-example",
    "postmortem", "practical-example", "production-pattern",
    "research-frontier", "self-check", "thesis-thread", "tip",
    "under-the-hood", "warning", "whats-next",
}


def find_files() -> list[Path]:
    out: list[Path] = []
    for g in SECTION_GLOBS:
        out.extend(sorted(ROOT.glob(g)))
    return out


# Regexes
RE_DOLLAR_MATH = re.compile(r"\$\$[^$]+\$\$|(?<!\\)\$[^\s$][^$\n]*?[^\\\s]\$")
RE_DISPLAY_MATH = re.compile(r"\$\$([^$]+?)\$\$", re.DOTALL)
RE_INLINE_MATH = re.compile(r"(?<!\\)\$([^\n$]+?)(?<!\\)\$")
RE_KATEX = re.compile(r"katex", re.IGNORECASE)
RE_BEGIN_ALIGN = re.compile(r"\\begin\{align\}")  # without star

RE_DIAGRAM_CAPTION = re.compile(r'<div class="diagram-caption"[^>]*>(.*?)</div>', re.DOTALL)
RE_CODE_CAPTION = re.compile(r'<div class="code-caption"[^>]*>(.*?)</div>', re.DOTALL)
RE_FIGCAPTION = re.compile(r'<figcaption[^>]*>(.*?)</figcaption>', re.DOTALL)
RE_CALLOUT = re.compile(r'<div class="callout ([a-z\-]+)"[^>]*>', re.IGNORECASE)
RE_CALLOUT_BLOCK = re.compile(r'<div class="callout [a-z\-]+"[^>]*>', re.IGNORECASE)
RE_PRE_BLOCK = re.compile(r"<pre[^>]*>(.*?)</pre>", re.DOTALL)
RE_CODE_INLINE_LINES = re.compile(r"<code[^>]*>(.*?)</code>", re.DOTALL)
RE_TABLE = re.compile(r"<table[^>]*>(.*?)</table>", re.DOTALL)
RE_TABLE_ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL)
RE_TABLE_CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.DOTALL)
RE_SVG = re.compile(r"<svg([^>]*)>", re.IGNORECASE)
RE_IMG = re.compile(r"<img\b([^>]*)/?>", re.IGNORECASE)
RE_FIGURE = re.compile(r"<figure[^>]*>(.*?)</figure>", re.DOTALL)


def has_math(text: str) -> bool:
    return bool(RE_DOLLAR_MATH.search(text))


def file_depth(p: Path) -> int:
    return len(p.relative_to(ROOT).parts) - 1


# ---------- RC1: Missing KaTeX -----------------------------------------
def check_missing_katex(head: str, body: str) -> bool:
    if not has_math(body):
        return False
    return not bool(RE_KATEX.search(head))


# ---------- RC2: Overflow math -----------------------------------------
def check_overflow_math(body: str) -> dict:
    findings: dict = {}
    long_display: list[tuple[int, int, str]] = []
    for m in RE_DISPLAY_MATH.finditer(body):
        content = m.group(1).strip()
        # Strip aligned/cases environments - they already have line breaks
        if "\\begin{aligned}" in content or "\\begin{align}" in content or "\\begin{cases}" in content or "\\begin{matrix}" in content or "\\begin{pmatrix}" in content or "\\begin{bmatrix}" in content:
            continue
        # If no \\ line breaks AND content > 120 chars, flag as overflow
        if "\\\\" not in content and len(content) > 120:
            line = body.count("\n", 0, m.start()) + 1
            long_display.append((line, len(content), content[:80]))
    if long_display:
        findings["long_display_math"] = long_display

    # Inline math: > 80 chars rendered length
    long_inline: list[tuple[int, int]] = []
    for m in RE_INLINE_MATH.finditer(body):
        content = m.group(1)
        # Skip prose-like (currency)
        if "\\" not in content and not re.search(r"[_^{}=]", content):
            continue
        if len(content) > 80:
            line = body.count("\n", 0, m.start()) + 1
            long_inline.append((line, len(content)))
    if long_inline:
        findings["long_inline_math"] = long_inline

    # \begin{align} without star (auto-numbering breaks KaTeX silently sometimes)
    if RE_BEGIN_ALIGN.search(body):
        findings["align_without_star"] = len(RE_BEGIN_ALIGN.findall(body))
    return findings


# ---------- RC3: Overflow non-math -------------------------------------
def check_overflow_nonmath(body: str) -> dict:
    findings: dict = {}

    # B1: pre/code lines > 90 chars
    long_lines: list[tuple[int, int]] = []
    for m in RE_PRE_BLOCK.finditer(body):
        inner = m.group(1)
        # remove HTML tags first
        plain = re.sub(r"<[^>]+>", "", inner)
        plain = (plain.replace("&lt;", "<").replace("&gt;", ">")
                 .replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'"))
        for ln in plain.splitlines():
            if len(ln) > 90:
                line = body.count("\n", 0, m.start()) + 1
                long_lines.append((line, len(ln)))
                break  # one per pre block is enough
    if long_lines:
        findings["long_code_lines"] = long_lines

    # C1: wide tables (>=6 columns OR any cell text > 100 chars)
    wide_tables: list[tuple[int, str]] = []
    for tm in RE_TABLE.finditer(body):
        tbody = tm.group(1)
        rows = RE_TABLE_ROW.findall(tbody)
        if not rows:
            continue
        max_cols = 0
        long_cell = False
        for row in rows:
            cells = RE_TABLE_CELL.findall(row)
            max_cols = max(max_cols, len(cells))
            for cell in cells:
                ctext = re.sub(r"<[^>]+>", "", cell).strip()
                if len(ctext) > 100:
                    long_cell = True
        if max_cols >= 6 or long_cell:
            line = body.count("\n", 0, tm.start()) + 1
            wide_tables.append((line, f"cols={max_cols} long_cell={long_cell}"))
    if wide_tables:
        findings["wide_tables"] = wide_tables

    # C2/C3: SVG without viewBox; SVG with width/height but no max-width
    svg_no_viewbox = 0
    svg_no_maxwidth = 0
    svg_lowercase_viewbox = 0
    for sm in RE_SVG.finditer(body):
        attrs = sm.group(1)
        # SVG is XML-strict in EPUB/Kindle. Browsers tolerate lowercase
        # 'viewbox', but EPUB's XHTML+SVG parser silently drops it, so the
        # SVG renders at intrinsic-size on Kindle and gets clipped.
        if "viewBox" in attrs:
            pass  # correct
        elif re.search(r"\bviewbox\s*=", attrs, re.IGNORECASE):
            svg_lowercase_viewbox += 1
        else:
            svg_no_viewbox += 1
        has_w_h = "width=" in attrs and "height=" in attrs
        has_maxw = "max-width" in attrs
        if has_w_h and not has_maxw:
            svg_no_maxwidth += 1
    if svg_lowercase_viewbox:
        findings["svg_lowercase_viewbox"] = svg_lowercase_viewbox
    if svg_no_viewbox:
        findings["svg_without_viewbox"] = svg_no_viewbox
    if svg_no_maxwidth:
        findings["svg_without_max_width"] = svg_no_maxwidth

    # C4: img without alt
    img_no_alt = 0
    for im in RE_IMG.finditer(body):
        attrs = im.group(1)
        if "alt=" not in attrs:
            img_no_alt += 1
    if img_no_alt:
        findings["img_without_alt"] = img_no_alt

    return findings


# ---------- RC4: Math in special containers -----------------------------
def check_math_in_containers(body: str) -> dict:
    findings: dict = {}
    n_diag = sum(1 for m in RE_DIAGRAM_CAPTION.finditer(body) if has_math(m.group(1)))
    n_codecap = sum(1 for m in RE_CODE_CAPTION.finditer(body) if has_math(m.group(1)))
    n_figcap = sum(1 for m in RE_FIGCAPTION.finditer(body) if has_math(m.group(1)))
    if n_diag:
        findings["math_in_diagram_caption"] = n_diag
    if n_codecap:
        findings["math_in_code_caption"] = n_codecap
    if n_figcap:
        findings["math_in_figcaption"] = n_figcap
    return findings


# ---------- RC5: HTML inconsistencies -----------------------------------
def check_html_inconsistencies(body: str) -> dict:
    findings: dict = {}

    # D1/D2: callout class names not in taxonomy, missing callout-title
    bad_callout_classes: list[str] = []
    callouts_no_title: list[str] = []
    for cm in RE_CALLOUT.finditer(body):
        cls = cm.group(1).lower()
        if cls not in VALID_CALLOUT_CLASSES:
            bad_callout_classes.append(cls)
        # Check that within ~200 chars there's a callout-title
        snippet = body[cm.end():cm.end() + 400]
        if "callout-title" not in snippet:
            callouts_no_title.append(cls)
    if bad_callout_classes:
        findings["bad_callout_classes"] = sorted(set(bad_callout_classes))
    if callouts_no_title:
        findings["callouts_without_title"] = callouts_no_title

    # B3: code-caption ABOVE the pre block (project rule: must be BELOW).
    # A caption is "above" only if the SAME pre block doesn't have another
    # code-caption immediately preceding it (within ~50 chars after </pre>).
    # We detect by looking at each <pre>: is the nearest code-caption
    # before this <pre> closer than the nearest after?
    code_cap_above: list[int] = []
    cap_positions = [m.start() for m in re.finditer(r'<div class="code-caption"', body)]
    pre_positions = [m.start() for m in RE_PRE_BLOCK.finditer(body)]
    pre_ends = [m.end() for m in RE_PRE_BLOCK.finditer(body)]
    for pp, pe in zip(pre_positions, pre_ends):
        # Find nearest cap before pp (within 100 chars - tight whitespace gap)
        # and nearest cap after pe (within 500 chars - the proper "below" slot).
        cap_before = max((c for c in cap_positions if c < pp), default=None)
        cap_after = min((c for c in cap_positions if c > pe), default=None)
        tight_above = cap_before is not None and (pp - cap_before) < 300
        tight_below = cap_after is not None and (cap_after - pe) < 500
        if tight_above and not tight_below:
            line = body.count("\n", 0, pp) + 1
            code_cap_above.append(line)
    if code_cap_above:
        findings["code_caption_above_code"] = code_cap_above

    # B4: <pre> blocks NOT wrapped in code-block-wrapper
    pre_unwrapped: list[int] = []
    for m in RE_PRE_BLOCK.finditer(body):
        # Look at 200 chars before this <pre> for a code-block-wrapper opener
        before = body[max(0, m.start() - 200): m.start()]
        if "code-block-wrapper" not in before:
            line = body.count("\n", 0, m.start()) + 1
            pre_unwrapped.append(line)
    if pre_unwrapped:
        findings["pre_without_code_block_wrapper"] = len(pre_unwrapped)

    # C5/C6: <figure> without <figcaption>, or figcaption above img
    figs_no_cap = 0
    figcap_above = 0
    for fm in RE_FIGURE.finditer(body):
        inner = fm.group(1)
        if "<figcaption" not in inner:
            figs_no_cap += 1
            continue
        # Find positions of figcaption vs img/svg
        cap_pos = inner.find("<figcaption")
        img_pos = inner.find("<img")
        svg_pos = inner.find("<svg")
        media_pos = min((p for p in (img_pos, svg_pos) if p >= 0), default=-1)
        if media_pos >= 0 and cap_pos < media_pos:
            figcap_above += 1
    if figs_no_cap:
        findings["figures_without_figcaption"] = figs_no_cap
    if figcap_above:
        findings["figcaption_above_media"] = figcap_above

    return findings


# ---------- Audit driver -----------------------------------------------
def audit_file(p: Path) -> dict:
    text = p.read_text(encoding="utf-8", errors="replace")
    head_match = re.search(r"<head>(.*?)</head>", text, re.DOTALL)
    head = head_match.group(1) if head_match else ""
    body_match = re.search(r"<body[^>]*>(.*)</body>", text, re.DOTALL)
    body = body_match.group(1) if body_match else text

    findings: dict = {"by_rc": {}}

    if check_missing_katex(head, body):
        findings["by_rc"]["RC1"] = {"missing_katex_include": True}

    rc2 = check_overflow_math(body)
    if rc2:
        findings["by_rc"]["RC2"] = rc2

    rc3 = check_overflow_nonmath(body)
    if rc3:
        findings["by_rc"]["RC3"] = rc3

    rc4 = check_math_in_containers(body)
    if rc4:
        findings["by_rc"]["RC4"] = rc4

    rc5 = check_html_inconsistencies(body)
    if rc5:
        findings["by_rc"]["RC5"] = rc5

    return findings if findings["by_rc"] else {}


def main() -> None:
    files = find_files()
    report: dict = {"per_file": {}, "rc_totals": defaultdict(int), "subkey_totals": defaultdict(int)}
    for p in files:
        f = audit_file(p)
        if f:
            rel = p.relative_to(ROOT).as_posix()
            report["per_file"][rel] = f
            for rc, sub in f["by_rc"].items():
                report["rc_totals"][rc] += 1
                for k, v in sub.items():
                    bucket = f"{rc}:{k}"
                    if isinstance(v, bool):
                        report["subkey_totals"][bucket] += 1
                    elif isinstance(v, int):
                        report["subkey_totals"][bucket] += v
                    else:
                        report["subkey_totals"][bucket] += len(v)
    report["rc_totals"] = dict(report["rc_totals"])
    report["subkey_totals"] = dict(report["subkey_totals"])
    report["total_files_scanned"] = len(files)
    report["files_with_findings"] = len(report["per_file"])

    out = Path(__file__).resolve().parent / "_root_cause_audit.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Scanned {len(files)} files, findings in {len(report['per_file'])}.")
    print("RC totals (files w/ at least 1):")
    for rc, n in sorted(report["rc_totals"].items()):
        print(f"  {rc}: {n}")
    print("Sub-key totals:")
    for k, v in sorted(report["subkey_totals"].items()):
        print(f"  {k}: {v}")
    print(f"Report: {out}")


if __name__ == "__main__":
    main()
