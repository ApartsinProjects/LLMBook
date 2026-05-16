"""
Audit pseudocode / algorithm blocks for readability and formatting
consistency across the LLMBook.

For every `<div class="callout algorithm">` block we score seven axes:

  1. indent_consistency   -- leading-space indent uniform across nested
                              lines (2 spaces? 4? mixed?).
  2. keyword_treatment    -- <b>for</b>/<b>if</b>... style vs Pygments
                              span highlighting (`pygments-highlighted
                              lang-text`). Either is acceptable, but
                              the book should not mix.
  3. step_numbering       -- numbered (1./2./3.) vs unnumbered;
                              numbered+lettered (1a/1b) vs mixed.
  4. identifier_styling   -- <i>x</i>, <code>x</code>, or bare text
                              for variables. Flag mismatch within a
                              single block.
  5. io_declarations      -- starts with both `Input:` and `Output:`
                              lines (or formal-equivalent text).
  6. block_length         -- raw line count, flag >= 20 lines without
                              blank-line phase separators.
  7. phase_separators     -- blank lines breaking init / loop / cleanup.

Reports the file/line, fragment label, all 7 axis scores, and a flat
issue list per block. Also dumps CSS findings: the current
.callout.algorithm pre rules and which language treatments are in use.

READ-ONLY. Writes only the audit Markdown to
E:/Projects/BookBlogsHome/LLMBook/pseudocode-readability-audit.md.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
REPORT_PATH = ROOT / "pseudocode-readability-audit.md"
CSS_PATH = ROOT / "styles" / "book.css"

EXCLUDE_DIRS = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind",
    "templates", ".git", ".html2pub_cache", ".github",
    "build", "vendor", "downloads",
}
EXCLUDE_PREFIXES = ("temp_",)
EXCLUDE_CONTAINS = ("backups",)


def is_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    for part in rel.parts:
        if part in EXCLUDE_DIRS:
            return True
        if any(part.startswith(p) for p in EXCLUDE_PREFIXES):
            return True
        if any(c in part.lower() for c in EXCLUDE_CONTAINS):
            return True
    return False


def iter_html_files() -> list[Path]:
    return sorted(f for f in ROOT.rglob("*.html") if not is_excluded(f))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


LABEL_RE = re.compile(
    r"(Pseudocode|Algorithm)\s+([A-Za-z]?[\d]+(?:\.\d+)*)",
    re.IGNORECASE,
)


@dataclass
class Block:
    file: Path
    line: int
    title: str
    label_number: str
    pre_class: str           # "language-none" | "pygments-highlighted lang-text" | other
    code_class: str
    code_text_raw: str       # text including <b>/<span> stripped
    inner_html: str          # raw HTML inside <code>
    has_bold_keywords: bool
    has_pygments_spans: bool
    has_italic_idents: bool
    has_code_idents: bool


def extract_blocks(path: Path, raw: str) -> list[Block]:
    soup = BeautifulSoup(raw, "html.parser")
    out: list[Block] = []
    for callout in soup.find_all("div", class_="callout"):
        classes = callout.get("class", []) or []
        if "algorithm" not in classes:
            continue
        pre = callout.find("pre")
        if pre is None:
            continue
        title_div = callout.find("div", class_="callout-title")
        title = title_div.get_text(" ", strip=True) if title_div else ""
        m = LABEL_RE.search(title)
        label_num = m.group(2) if m else ""

        code = pre.find("code") or pre
        pre_classes = " ".join(pre.get("class", []) or [])
        code_classes = " ".join(code.get("class", []) or [])

        inner_html = code.decode_contents()
        text_raw = code.get_text()
        has_bold = "<b>" in inner_html.lower()
        has_spans = "pygments-highlighted" in code_classes or (
            "<span" in inner_html and "class=" in inner_html
        )
        has_italic = "<i>" in inner_html.lower()
        has_code_inline = "<code" in inner_html.lower()

        try:
            offset = raw.index(str(title_div) if title_div else str(callout))
        except ValueError:
            offset = 0
        line = line_of_offset(raw, offset)

        out.append(Block(
            file=path, line=line,
            title=title, label_number=label_num,
            pre_class=pre_classes, code_class=code_classes,
            code_text_raw=text_raw, inner_html=inner_html,
            has_bold_keywords=has_bold,
            has_pygments_spans=has_spans,
            has_italic_idents=has_italic,
            has_code_idents=has_code_inline,
        ))
    return out


# ---------- Axis scorers ----------

def non_blank_lines(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if ln.strip()]


def leading_spaces(line: str) -> int:
    n = 0
    for ch in line:
        if ch == " ":
            n += 1
        elif ch == "\t":
            return -1
        else:
            break
    return n


def indent_levels(text: str) -> dict:
    """Return distribution of leading-space counts for non-blank lines."""
    lines = non_blank_lines(text)
    levels = Counter()
    tab_lines = 0
    for ln in lines:
        sp = leading_spaces(ln)
        if sp == -1:
            tab_lines += 1
        else:
            levels[sp] += 1
    return {"levels": levels, "tab_lines": tab_lines}


def indent_consistency(text: str) -> tuple[str, list[str]]:
    """Return (verdict, notes). verdict in OK / mixed / surprising."""
    info = indent_levels(text)
    notes: list[str] = []
    if info["tab_lines"]:
        notes.append(f"{info['tab_lines']} tab-indented lines")
    levels = info["levels"]
    if not levels:
        return "OK", notes
    nonzero = sorted(k for k in levels if k > 0)
    if not nonzero:
        return "OK", notes
    # Check for a consistent step (2 or 4).
    diffs = [b - a for a, b in zip([0] + nonzero, nonzero)]
    diffs = [d for d in diffs if d > 0]
    if not diffs:
        return "OK", notes
    # Common step is the GCD; flag if multiple non-multiples of 2 appear.
    common_steps = set(diffs)
    if len(common_steps) > 2:
        notes.append(
            f"indent levels {nonzero} -> diffs {diffs}"
        )
        return "mixed", notes
    odd_steps = [d for d in diffs if d % 2 == 1]
    if odd_steps:
        notes.append(f"odd-width indent steps {odd_steps}")
        return "surprising", notes
    if 1 in nonzero or 3 in nonzero:
        notes.append(f"1- or 3-space indent present: {nonzero}")
        return "surprising", notes
    return "OK", notes


KEYWORDS = (
    "Input", "Output", "for", "while", "if", "else", "elif",
    "return", "yield", "do", "until", "repeat", "break", "continue",
)


def keyword_treatment(b: Block) -> tuple[str, list[str]]:
    """Classify into one of:
      pyg-python   -- Pygments highlighting on real Python code (lang-python)
      pyg-text-bad -- Pygments lang-text mis-tinting plain pseudocode
      algo-helper  -- uses .algo-line-keyword / .algo-line-comment spans
      bold         -- language-none + hand-tagged <b>
      mixed        -- two of the above coexist in same block
      plain        -- no highlighting at all
    """
    notes: list[str] = []
    code_cls = b.code_class.lower()
    inner_low = b.inner_html.lower()
    has_algo_helper = "algo-line-keyword" in inner_low or "algo-line-comment" in inner_low
    has_pyg_lang_python = "lang-python" in code_cls or "language-python" in code_cls
    has_pyg_lang_text = (
        "lang-text" in code_cls or "language-text" in code_cls
    )
    has_pyg_spans = (
        b.has_pygments_spans and not has_algo_helper
    )

    # Detect mixed
    treatments = []
    if has_pyg_spans and has_pyg_lang_python:
        treatments.append("pyg-python")
    elif has_pyg_spans and has_pyg_lang_text:
        treatments.append("pyg-text-bad")
    elif has_pyg_spans:
        treatments.append("pyg-other")
    if has_algo_helper:
        treatments.append("algo-helper")
    if b.has_bold_keywords:
        treatments.append("bold")

    if len(treatments) >= 2:
        notes.append(f"multiple: {treatments}")
        return "mixed", notes
    if len(treatments) == 1:
        return treatments[0], notes
    notes.append("no keyword highlighting")
    return "plain", notes


NUMBERED_RE = re.compile(
    r"^\s*(\d+)\s*\.\s",
    re.MULTILINE,
)
LETTERED_RE = re.compile(
    r"^\s*([a-z])\s*\.\s",
    re.MULTILINE,
)
ROMAN_RE = re.compile(
    r"^\s*([ivx]+)\s*\.\s",
    re.MULTILINE,
)


def step_numbering(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    n_num = len(NUMBERED_RE.findall(text))
    n_let = len(LETTERED_RE.findall(text))
    n_rom = len(ROMAN_RE.findall(text))
    nlines = len(non_blank_lines(text))
    body_lines = [
        ln for ln in non_blank_lines(text)
        if not re.match(r"^\s*(Input|Output)", ln)
    ]
    eligible = max(1, len(body_lines))
    if n_num == 0 and n_let == 0 and n_rom == 0:
        return "none", notes
    if n_num >= 3 and n_let >= 1:
        return "numbered+lettered", notes
    if n_num >= 3:
        # Check coverage: does numbering cover most non-Input/Output lines?
        cov = n_num / eligible
        if cov < 0.4:
            notes.append(f"only {n_num}/{eligible} body lines numbered")
            return "partial", notes
        return "numbered", notes
    if n_num >= 1 and n_num < 3:
        notes.append(f"only {n_num} numbered steps")
        return "partial", notes
    if n_let or n_rom:
        notes.append("lettered/roman steps but no top-level numbers")
        return "lettered-only", notes
    return "partial", notes


IO_INPUT_RE = re.compile(
    r"^\s*(Input|INPUT|Inputs|Given|Require)\s*[:\-]",
    re.IGNORECASE | re.MULTILINE,
)
IO_OUTPUT_RE = re.compile(
    r"^\s*(Output|OUTPUT|Outputs|Ensure|Return)\s*[:\-]",
    re.IGNORECASE | re.MULTILINE,
)


def io_declarations(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    has_in = bool(IO_INPUT_RE.search(text))
    has_out = bool(IO_OUTPUT_RE.search(text))
    if has_in and has_out:
        return "OK", notes
    if has_in and not has_out:
        notes.append("missing Output:")
        return "missing-output", notes
    if has_out and not has_in:
        notes.append("missing Input:")
        return "missing-input", notes
    notes.append("missing both Input: and Output:")
    return "missing-both", notes


def identifier_styling(b: Block) -> tuple[str, list[str]]:
    notes: list[str] = []
    flags = []
    if b.has_italic_idents:
        flags.append("italic")
    if b.has_code_idents:
        flags.append("code")
    # pygments spans color identifiers but are a different system; ignore.
    if len(flags) == 0:
        return "plain", notes
    if len(flags) == 1:
        return flags[0], notes
    notes.append(f"mixed identifier styling: {flags}")
    return "mixed", notes


def block_length_and_phases(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    lines = text.splitlines()
    nblank_lines = len(non_blank_lines(text))
    # Count blank-line phase separators inside the body
    blank_separators = 0
    saw_content = False
    prev_blank = False
    for ln in lines:
        if ln.strip():
            saw_content = True
            prev_blank = False
        else:
            if saw_content and not prev_blank:
                blank_separators += 1
            prev_blank = True
    # Don't count trailing blanks
    if lines and not lines[-1].strip():
        blank_separators = max(0, blank_separators - 1)

    if nblank_lines >= 20 and blank_separators == 0:
        notes.append(
            f"{nblank_lines} body lines, no blank-line phase separators"
        )
        return "dense", notes
    if nblank_lines >= 25 and blank_separators < 2:
        notes.append(
            f"{nblank_lines} body lines, only {blank_separators} phase separators"
        )
        return "dense", notes
    return "OK", notes


# ---------- Audit ----------

@dataclass
class Finding:
    block: Block
    indent: str
    indent_notes: list[str]
    keyword: str
    keyword_notes: list[str]
    numbering: str
    numbering_notes: list[str]
    io: str
    io_notes: list[str]
    ident: str
    ident_notes: list[str]
    length: str
    length_notes: list[str]
    issue_count: int = 0
    issues: list[str] = field(default_factory=list)


def score(b: Block) -> Finding:
    ind, ind_n = indent_consistency(b.code_text_raw)
    kw, kw_n = keyword_treatment(b)
    num, num_n = step_numbering(b.code_text_raw)
    io, io_n = io_declarations(b.code_text_raw)
    idt, idt_n = identifier_styling(b)
    ln, ln_n = block_length_and_phases(b.code_text_raw)

    issues: list[str] = []
    if ind != "OK":
        issues.append(f"indent={ind}")
    if kw in ("mixed", "plain", "pyg-text-bad"):
        issues.append(f"keyword={kw}")
    if num in ("partial", "lettered-only"):
        issues.append(f"numbering={num}")
    if io != "OK":
        issues.append(f"io={io}")
    if idt == "mixed":
        issues.append(f"ident={idt}")
    if ln == "dense":
        issues.append(f"length={ln}")

    return Finding(
        block=b, indent=ind, indent_notes=ind_n,
        keyword=kw, keyword_notes=kw_n,
        numbering=num, numbering_notes=num_n,
        io=io, io_notes=io_n,
        ident=idt, ident_notes=idt_n,
        length=ln, length_notes=ln_n,
        issue_count=len(issues), issues=issues,
    )


# ---------- CSS check ----------

def read_css_section() -> dict:
    """Read the .callout.algorithm CSS rules from book.css."""
    info = {
        "callout_algorithm_pre": "",
        "language_none_pre": "",
        "language_text_pre": "",
        "algo_helpers": "",
    }
    if not CSS_PATH.exists():
        return info
    text = CSS_PATH.read_text(encoding="utf-8", errors="replace")
    # Find .callout.algorithm pre {...}
    m = re.search(
        r"\.callout\.algorithm\s+pre\s*\{[^}]*\}",
        text, re.IGNORECASE | re.DOTALL,
    )
    if m:
        info["callout_algorithm_pre"] = m.group(0)
    # language-none rules
    for sel in (r"\.language-none", r"\.lang-none"):
        m = re.search(rf"{sel}[^\{{]*\{{[^}}]*\}}", text, re.IGNORECASE)
        if m:
            info["language_none_pre"] = m.group(0)
            break
    m = re.search(
        r"\.lang-text[^\{]*\{[^}]*\}", text, re.IGNORECASE,
    )
    if m:
        info["language_text_pre"] = m.group(0)
    # Look for algo-line-* helpers
    for m in re.finditer(
        r"\.callout\.algorithm\s+\.algo-[\w-]+[^\{]*\{[^}]*\}",
        text, re.IGNORECASE | re.DOTALL,
    ):
        info["algo_helpers"] += m.group(0) + "\n"
    return info


# ---------- Report ----------

def truncate(s: str, n: int) -> str:
    s = s.replace("\n", " ").strip()
    if len(s) > n:
        s = s[: n - 1] + "..."
    return s.replace("|", "/")


def code_snippet(text: str, n: int = 6) -> str:
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    return "\n".join(lines[:n])


def write_report(blocks: list[Block], findings: list[Finding],
                 css: dict, files_scanned: int) -> None:
    out: list[str] = []
    push = out.append

    push("# Pseudocode Readability & Formatting Audit")
    push("")
    push(
        "Audit of every `<div class=\"callout algorithm\">` block in the "
        "LLMBook source tree for readability and formatting consistency. "
        "Scored on seven axes: indent consistency, keyword treatment "
        "(`<b>` vs Pygments), step numbering, identifier styling, "
        "Input/Output declarations, block length, and phase separators."
    )
    push("")
    push(
        "Script: `scripts/_audit_pseudocode_readability.py` "
        "(Python 3.14, BeautifulSoup). READ-ONLY."
    )
    push("")
    push(f"- Files scanned: **{files_scanned}**")
    push(f"- Pseudocode blocks found: **{len(blocks)}**")
    push("")

    # Treatment distribution
    kw_counts = Counter(f.keyword for f in findings)
    push("## 1. Treatment distribution (rendering pipeline)")
    push("")
    push("| Treatment | Count | Description |")
    push("|---|---|---|")
    push(
        f"| `pyg-python` | {kw_counts.get('pyg-python', 0)} | "
        "Pygments `lang-python`: real Python code-fragment-style highlighting. |"
    )
    push(
        f"| `pyg-text-bad` | {kw_counts.get('pyg-text-bad', 0)} | "
        "Pygments `lang-text`: plain pseudocode tokenized as code, mis-tints numbers/identifiers. |"
    )
    push(
        f"| `algo-helper` | {kw_counts.get('algo-helper', 0)} | "
        "Uses `.algo-line-keyword` / `.algo-line-comment` helper spans (book.css already defines them). |"
    )
    push(
        f"| `bold` | {kw_counts.get('bold', 0)} | "
        "`<pre><code class=\"language-none\">` with hand-tagged `<b>Input:</b>`, `<b>for</b>`. |"
    )
    push(
        f"| `mixed` | {kw_counts.get('mixed', 0)} | Two treatments in same block (e.g. `<b>` plus Pygments spans). |"
    )
    push(
        f"| `plain` | {kw_counts.get('plain', 0)} | No keyword highlighting. |"
    )
    push("")
    push(
        "**Major finding**: the book ships at least four different treatments. "
        "`pyg-python` is fine for blocks that contain real Python "
        "(FlashAttention tiling, vLLM block table, etc.); `pyg-text-bad` is "
        "actively harmful: it tints plain words like `Input`, `for`, "
        "`messages`, `Q`, `K` with random Pygments colors and turns step "
        "numbers (`1.`, `2.`) into pale-green floats. The two `algo-helper` "
        "blocks (section-22.1, section-29.3) use the existing CSS classes "
        "the way they were originally designed."
    )
    push("")
    push(
        "**Recommendation**: convert all `pyg-text-bad` blocks to "
        "`algo-helper` style (preserves the existing CSS infrastructure and "
        "scales to all 21 blocks)."
    )
    push("")

    # Indent distribution
    ind_counts = Counter(f.indent for f in findings)
    push("## 2. Indent consistency")
    push("")
    push("| Verdict | Count |")
    push("|---|---|")
    for k in ("OK", "surprising", "mixed"):
        push(f"| {k} | {ind_counts.get(k, 0)} |")
    push("")

    # Per-block axis matrix
    push("## 3. Per-block matrix")
    push("")
    push("Columns: indent / keyword / numbering / I-O / ident / length.")
    push("")
    push(
        "| # | File:line | Label | Indent | Keyword | Numbering | I-O | Ident | Length | Issues |"
    )
    push("|---|---|---|---|---|---|---|---|---|---|")
    for i, f in enumerate(
        sorted(findings, key=lambda f: (rel(f.block.file), f.block.line)),
        start=1,
    ):
        b = f.block
        push(
            f"| {i} | `{rel(b.file)}:{b.line}` | "
            f"`{b.label_number or '-'}` | "
            f"{f.indent} | {f.keyword} | {f.numbering} | "
            f"{f.io} | {f.ident} | {f.length} | {f.issue_count} |"
        )
    push("")

    # Detailed findings
    push("## 4. Per-block detail")
    push("")
    for i, f in enumerate(
        sorted(findings, key=lambda f: (-f.issue_count, rel(f.block.file), f.block.line)),
        start=1,
    ):
        b = f.block
        push(f"### {i}. {truncate(b.title, 100)}")
        push("")
        push(f"- File: `{rel(b.file)}:{b.line}`")
        push(
            f"- pre class=`{b.pre_class or '-'}`  code class=`{b.code_class or '-'}`"
        )
        push(
            f"- Indent: **{f.indent}** ({'; '.join(f.indent_notes) or 'uniform'})"
        )
        push(
            f"- Keyword treatment: **{f.keyword}** ({'; '.join(f.keyword_notes) or 'consistent'})"
        )
        push(
            f"- Step numbering: **{f.numbering}** ({'; '.join(f.numbering_notes) or 'consistent'})"
        )
        push(
            f"- Input/Output: **{f.io}** ({'; '.join(f.io_notes) or 'present'})"
        )
        push(
            f"- Identifier styling: **{f.ident}** ({'; '.join(f.ident_notes) or 'consistent'})"
        )
        push(
            f"- Length / phases: **{f.length}** ({'; '.join(f.length_notes) or 'OK'})"
        )
        if f.issues:
            push(f"- **Issues**: {', '.join(f.issues)}")
        push("")
        push("Snippet (first 6 lines):")
        push("")
        push("```")
        snippet = code_snippet(b.code_text_raw, 6)
        # Replace non-ASCII to avoid encoding errors on Windows console.
        push(snippet)
        push("```")
        push("")

    # CSS findings
    push("## 5. CSS treatment for `.callout.algorithm`")
    push("")
    if css["callout_algorithm_pre"]:
        push("Current rule for `.callout.algorithm pre`:")
        push("")
        push("```css")
        push(css["callout_algorithm_pre"])
        push("```")
    else:
        push("_No `.callout.algorithm pre` rule found._")
    push("")
    if css["algo_helpers"]:
        push(
            "Helper classes already defined in `book.css` (used by 3 of the "
            "21 blocks; the remaining ~14 `pyg-text-bad` blocks should be "
            "converted to use these spans):"
        )
        push("")
        push("```css")
        push(css["algo_helpers"].strip())
        push("```")
    push("")
    if css["language_none_pre"]:
        push("Rule for `.language-none`:")
        push("")
        push("```css")
        push(css["language_none_pre"])
        push("```")
    if css["language_text_pre"]:
        push("")
        push("Rule for `.lang-text`:")
        push("")
        push("```css")
        push(css["language_text_pre"])
        push("```")
    push("")

    push("## 6. Punch list")
    push("")
    push("### 6.1 Block-level fixes")
    push("")
    push("Blocks ordered by issue count.")
    push("")
    push("| File:line | Label | Issues |")
    push("|---|---|---|")
    for f in sorted(findings, key=lambda f: (-f.issue_count, rel(f.block.file), f.block.line)):
        if f.issue_count == 0:
            continue
        b = f.block
        push(
            f"| `{rel(b.file)}:{b.line}` | `{b.label_number or '-'}` | "
            f"{', '.join(f.issues)} |"
        )
    push("")

    push("### 6.2 Global CSS additions")
    push("")
    push(
        "Add to `styles/book.css` near the existing `.callout.algorithm pre` "
        "rule (around line 1327) to give pseudocode a distinctive, calmer "
        "treatment that visually separates it from runnable Code Fragments:"
    )
    push("")
    push("```css")
    push("/* Pseudocode: stronger left accent, monospace numbers,")
    push("   subtle inset shadow, and tighter line height for scan-ability. */")
    push(".callout.algorithm pre {")
    push("    /* Existing: background #faf8ff; border #c5b8e0. */")
    push("    border-left: 4px solid #4a55a2;        /* match callout accent */")
    push("    padding-left: 1.2em;                   /* indent body from rule */")
    push("    box-shadow: inset 0 0 0 1px rgba(74, 85, 162, 0.06);")
    push("    font-family: 'IBM Plex Mono', 'Consolas', monospace;")
    push("    font-variant-numeric: tabular-nums;    /* line up 1./2./10. */")
    push("    tab-size: 2;                           /* 2-space tab visualization */")
    push("    line-height: 1.6;")
    push("}")
    push("")
    push("/* Phase separator: any blank line is rendered with extra top margin")
    push("   when wrapped in <p class='algo-phase'></p>, OR add CSS-only via")
    push("   a sibling selector if blank lines are preserved in <pre>. */")
    push(".callout.algorithm pre code .algo-phase {")
    push("    display: block;")
    push("    margin-top: 0.6em;")
    push("}")
    push("")
    push("/* Input/Output labels: stronger weight, color-tinted */")
    push(".callout.algorithm pre b:first-child,")
    push(".callout.algorithm pre code > b:first-of-type {")
    push("    color: #2e3990;")
    push("    letter-spacing: 0.02em;")
    push("}")
    push("")
    push("/* Suppress Pygments coloring when language is `lang-text`: numbers")
    push("   should not be highlighted as floats, identifiers should not be")
    push("   highlighted as Python names. */")
    push(".callout.algorithm pre code.lang-text .mf,")
    push(".callout.algorithm pre code.lang-text .mi,")
    push(".callout.algorithm pre code.lang-text .n,")
    push(".callout.algorithm pre code.lang-text .nb,")
    push(".callout.algorithm pre code.lang-text .o,")
    push(".callout.algorithm pre code.lang-text .p {")
    push("    color: inherit;                       /* drop syntax tint */")
    push("    font-weight: inherit;")
    push("}")
    push(".callout.algorithm pre code.lang-text .k,")
    push(".callout.algorithm pre code.lang-text .kn {")
    push("    color: #3949ab;                       /* keep keyword color */")
    push("    font-weight: 700;")
    push("}")
    push("```")
    push("")

    push("### 6.3 Editorial conventions to enforce")
    push("")
    push(
        "1. **Pipeline choice**: standardize on the existing **algo-helper** "
        "treatment: `<pre><code class=\"language-none\">` + "
        "`<span class=\"algo-line-keyword\">Input:</span>` + "
        "`<span class=\"algo-line-comment\">// note</span>`. The CSS at "
        "`book.css:1334-1341` already supports this, and two blocks "
        "(section-22.1, section-29.3) already use it. Convert the "
        "~14 `pyg-text-bad` blocks (Pygments tokenizing plain pseudocode as "
        "`lang-text`) to this scheme. Keep the ~5 `pyg-python` blocks "
        "(FlashAttention tiling, vLLM Block Table, speculative decoding, "
        "LoRA backward, position-bias judge) as Pygments since they contain "
        "real Python."
    )
    push("")
    push(
        "2. **Indent**: 2 spaces per nesting level, never tabs. Document in "
        "`CONTENT_GUIDELINES.md`."
    )
    push("")
    push(
        "3. **Numbering**: `1.` for top-level steps, `a.` `b.` `c.` for "
        "sub-steps under a numbered step. No mixed Roman/Arabic."
    )
    push("")
    push(
        "4. **I/O contract**: every pseudocode block opens with two lines: "
        "`<b>Input:</b> ...` and `<b>Output:</b> ...`, separated from the "
        "body by one blank line."
    )
    push("")
    push(
        "5. **Identifier styling**: variables and function calls bare; only "
        "the *keywords* in `KEYWORDS` get `<b>...</b>`. Drop any `<i>` or "
        "`<code>` inside the pseudocode block."
    )
    push("")
    push(
        "6. **Phase separators**: blocks with >= 20 body lines should use "
        "one blank line between init / main loop / cleanup / return phases."
    )
    push("")
    push("---")
    push("")
    push(
        "Generated by `scripts/_audit_pseudocode_readability.py`. "
        "All scores are heuristic; spot-check before mass-editing."
    )

    REPORT_PATH.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    files = iter_html_files()
    blocks: list[Block] = []
    for f in files:
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "callout algorithm" not in raw and 'class="callout algorithm' not in raw:
            continue
        blocks.extend(extract_blocks(f, raw))
    findings = [score(b) for b in blocks]
    css = read_css_section()
    write_report(blocks, findings, css, len(files))

    # Console summary (ASCII-safe)
    kw_counts = Counter(f.keyword for f in findings)
    ind_counts = Counter(f.indent for f in findings)
    io_counts = Counter(f.io for f in findings)
    num_counts = Counter(f.numbering for f in findings)
    print(f"Files scanned: {len(files)}")
    print(f"Pseudocode blocks: {len(blocks)}")
    print()
    print("Keyword treatment:")
    for k, v in kw_counts.most_common():
        print(f"  {k}: {v}")
    print()
    print("Indent verdict:")
    for k, v in ind_counts.most_common():
        print(f"  {k}: {v}")
    print()
    print("Numbering:")
    for k, v in num_counts.most_common():
        print(f"  {k}: {v}")
    print()
    print("Input/Output:")
    for k, v in io_counts.most_common():
        print(f"  {k}: {v}")
    print()
    issue_total = sum(f.issue_count for f in findings)
    n_with_issues = sum(1 for f in findings if f.issue_count > 0)
    print(f"Blocks with >=1 issue: {n_with_issues}/{len(blocks)}")
    print(f"Total issue tokens:    {issue_total}")
    print()
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
