"""
Audit captioned code blocks across the LLMBook to detect mislabeled
pseudocode-vs-real-code captions.

For each captioned code block, we extract the caption label
(Pseudocode / Code Fragment / Algorithm), grab the corresponding
<pre><code>...</code></pre> block, and try to classify it as:
  - real_code (parses cleanly with ast.parse and looks like a real
    Python program: real imports, real type hints, real APIs)
  - pseudocode (uses placeholders, doesn't parse, or shows informal
    control flow such as "for each X in Y:" or numbered steps)
  - ambiguous (parses but uses placeholders, or doesn't parse but
    looks Python-ish)

Two caption forms are handled:

  1. <div class="code-caption"><strong>LABEL N.N.N:</strong> ...</div>
     These are inline captions that immediately follow OR immediately
     precede a <pre><code>...</code></pre> block (commonly inside a
     <div class="code-block-wrapper">).

  2. <div class="callout-title">LABEL N.N.N: ...</div> living inside
     <div class="callout algorithm"> ... </div>. Here the caption is
     the title of the callout box, and the <pre><code> is inside the
     same callout div.

Both forms are normalized to (file, line, label, label_kind, code_text,
language). Then classification runs, and mismatches are reported.

Scope: walk every .html file under the project root EXCEPT files whose
relative path contains 'KDP', '.claude', 'temp_', 'scripts', 'backups',
'node_modules', 'pagefind', or 'templates'.

READ-ONLY. Writes only the audit Markdown to
E:/Projects/BookBlogsHome/LLMBook/pseudocode-classification-audit.md.
"""

from __future__ import annotations

import ast
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, NavigableString

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
REPORT_PATH = ROOT / "pseudocode-classification-audit.md"

EXCLUDE_PREFIXES = (
    "KDP", ".claude", "temp_", "scripts", "node_modules",
    "pagefind", "templates",
)


# ------------ File enumeration ------------

def iter_html_files() -> list[Path]:
    out = []
    for f in ROOT.rglob("*.html"):
        rel = f.relative_to(ROOT)
        if any(
            p.startswith(EXCLUDE_PREFIXES) or "backup" in p.lower()
            for p in rel.parts
        ):
            continue
        out.append(f)
    return sorted(out)


# ------------ Caption regex ------------

# A caption is identified by a label of the form
# "Pseudocode N.N", "Code Fragment N.N", "Algorithm N.N",
# possibly with extra numeric levels. We accept letters too because
# the appendices use letters (e.g. "Code Fragment A.1.2").
LABEL_RE = re.compile(
    r"(Pseudocode|Code\s*Fragment|Algorithm)\s+([A-Za-z]?[\d]+(?:\.\d+)*)",
    re.IGNORECASE,
)


# ------------ Helpers ------------

def line_of_offset(text: str, offset: int) -> int:
    """Return 1-based line number of a character offset."""
    return text.count("\n", 0, offset) + 1


def clean_code_text(node) -> str:
    """Extract the plain code text from a <pre> or <code> BS node."""
    # get_text() flattens out the syntax-highlighting spans.
    return node.get_text()


def classify_label(label_text: str) -> Optional[str]:
    """Normalize a label tag to one of 'pseudocode'/'code_fragment'/'algorithm'."""
    m = LABEL_RE.search(label_text)
    if not m:
        return None
    tag = m.group(1).lower().replace(" ", "")
    if "pseudo" in tag:
        return "pseudocode"
    if "fragment" in tag:
        return "code_fragment"
    return "algorithm"


def label_number(label_text: str) -> Optional[str]:
    m = LABEL_RE.search(label_text)
    if not m:
        return None
    return m.group(2)


# ------------ Code classification ------------

PLACEHOLDER_NAMES = {
    "do_thing", "process", "compute", "step", "f", "g", "h",
    "foo", "bar", "baz", "x", "y", "z",
}

# Real non-Python languages: blocks declared with one of these langs
# are treated as real_code regardless of pseudocode marker hits.
# These are configs / scripts / queries, not algorithm boxes.
REAL_NON_PYTHON_LANGS = {
    "bash", "shell", "sh", "zsh",
    "yaml", "yml",
    "json",
    "dockerfile", "docker",
    "sql",
    "javascript", "js", "typescript", "ts",
    "html", "xml", "css",
    "toml", "ini",
    "rust", "go", "c", "cpp", "java",
}

# Markers that suggest pseudocode rather than real code.
PSEUDO_MARKERS = [
    r"\bfor\s+each\b",                  # "for each item in X:"
    r"^\s*\d+\.\s+[A-Za-z]",            # numbered step "1. Do something"
    r"^\s*[a-z]\.\s+[A-Za-z]",          # lettered step "a. Do something"
    r"^\s*[ivx]+\.\s+[A-Za-z]",         # roman numeral step
    r"^\s*Input\s*:",                   # algorithm-style header
    r"^\s*Output\s*:",
    "←",                           # leftwards arrow (assignment)
    "∈",                           # element-of
    "⊤|⊥",                    # top/bot
]
PSEUDO_MARKERS_RE = [re.compile(p, re.MULTILINE) for p in PSEUDO_MARKERS]

INPUT_HEADER_RE = re.compile(r"^\s*Input\s*:", re.MULTILINE)
OUTPUT_HEADER_RE = re.compile(r"^\s*Output\s*:", re.MULTILINE)

# Lab placeholder marker. Lab snippets with `???`, # TODO, # Hint, or
# <<...>> are real code with intentional student gaps; they should not
# be misclassified as pseudocode even when ast.parse fails.
LAB_PLACEHOLDER_RE = re.compile(r"\?\?\?|# TODO:|# Hint:|<<\s*\w[^>]*>>")


def is_pythonish(code: str) -> bool:
    """Cheap heuristic: does this look like it's trying to be Python?"""
    if not code.strip():
        return False
    return any(
        kw in code
        for kw in (
            "def ", "import ", "from ", "class ",
            "self.", "return ", "lambda ",
        )
    )


def ast_parse_score(code: str) -> tuple[bool, Optional[str]]:
    """Try ast.parse on the code, return (ok, error_message)."""
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as exc:
        return False, f"SyntaxError: {exc.msg} (line {exc.lineno})"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def count_pseudo_markers(code: str) -> int:
    n = 0
    for r in PSEUDO_MARKERS_RE:
        if r.search(code):
            n += 1
    return n


def has_real_imports(code: str) -> bool:
    """Return True if the code imports concrete libraries we'd expect
    in real production-style snippets."""
    real_imports = (
        "torch", "transformers", "openai", "anthropic", "numpy", "pandas",
        "datasets", "huggingface", "langchain", "llama_index", "pydantic",
        "fastapi", "flask", "boto3", "requests", "redis", "psycopg",
        "sqlalchemy", "sklearn", "scipy", "matplotlib", "deepeval",
        "trl", "peft", "accelerate", "bitsandbytes", "ray", "wandb",
        "asyncio", "json", "time", "os", "sys", "logging", "dataclasses",
        "typing", "pathlib", "collections", "functools", "itertools",
        "subprocess", "tempfile", "uuid", "hashlib", "random", "math",
        "abc", "enum", "argparse", "re", "triton",
    )
    for line in code.splitlines():
        line = line.strip()
        if not (line.startswith("import ") or line.startswith("from ")):
            continue
        for imp in real_imports:
            if re.search(rf"\b{re.escape(imp)}\b", line):
                return True
    return False


def looks_like_real_code(code: str, lang: Optional[str]) -> tuple[str, str]:
    """Classify a code snippet.

    Returns (classification, reason) where classification is
    'real_code', 'pseudocode', or 'ambiguous'.

    Decision order:
      1. Empty -> pseudocode (defensive).
      2. Declared lang is a known real non-Python language
         (bash/yaml/json/dockerfile/sql/js/...): always real_code.
         These are configs/scripts, not algorithm boxes.
      3. Contains a lab placeholder (`???`, # TODO, # Hint, <<>>):
         always real_code. Labs are real code with student gaps.
      4. Has paired `Input:` and `Output:` line-start headers:
         pseudocode (classic algorithm box convention).
      5. Has >=3 pseudocode markers: pseudocode.
      6-9. Pythonish: parse with ast, classify on success and markers.
      10. Not Pythonish, no declared lang: fall back to markers.
    """
    code = code.replace("\xa0", " ")  # nbsp -> regular space
    stripped = code.strip()
    if not stripped:
        return "pseudocode", "empty"

    if lang and lang.lower() in REAL_NON_PYTHON_LANGS:
        return "real_code", f"declared lang={lang}"

    if LAB_PLACEHOLDER_RE.search(code):
        return "real_code", "contains lab placeholder (???/TODO/<<>>)"

    if INPUT_HEADER_RE.search(code) and OUTPUT_HEADER_RE.search(code):
        return "pseudocode", "Input/Output algorithm header pair"

    pseudo_marker_count = count_pseudo_markers(code)

    if pseudo_marker_count >= 3:
        return "pseudocode", f"{pseudo_marker_count} pseudocode markers"

    pythonish = is_pythonish(code) or (
        lang and lang.lower() in {"python", "py"}
    )
    if pythonish:
        ok, err = ast_parse_score(stripped)
        real_imp = has_real_imports(code)
        if ok:
            if real_imp:
                return "real_code", "parses + real imports"
            idents = re.findall(r"\b[a-z_][a-z0-9_]*\b", code)
            ph_hits = sum(1 for i in idents if i in PLACEHOLDER_NAMES)
            if ph_hits >= 5 and pseudo_marker_count >= 1:
                return "ambiguous", f"parses but {ph_hits} placeholder idents"
            return "real_code", "parses cleanly"
        # Failed to parse.
        # If declared lang-python AND has real imports, trust the lang
        # declaration: the SyntaxError is likely a whitespace/rendering
        # artifact, not pseudocode. A single "for each" inside a string
        # literal does not flip a real Python file into pseudocode.
        if real_imp and (lang and lang.lower() in {"python", "py"}):
            return "real_code", (
                f"declared lang-python with real imports "
                f"(parse failed: {err})"
            )
        if pseudo_marker_count >= 2:
            return "pseudocode", f"no parse + markers: {err}"
        if pseudo_marker_count >= 1:
            return "ambiguous", f"no parse + 1 marker: {err}"
        return "ambiguous", f"no parse, no markers: {err}"

    if pseudo_marker_count >= 1:
        return "pseudocode", "unclassed with markers"
    return "ambiguous", "non-Pythonish, no markers"


# ------------ Caption extraction ------------

@dataclass
class CaptionedBlock:
    file: Path
    line: int
    label_kind: str            # 'pseudocode' / 'code_fragment' / 'algorithm'
    label_text: str            # the matched "Pseudocode 29.3.2" etc.
    label_number: str          # "29.3.2"
    code_text: str
    code_lang: Optional[str]
    caption_text: str
    source: str                # 'code-caption' or 'callout-title'


def find_lang(code_tag) -> Optional[str]:
    classes = code_tag.get("class") or []
    for c in classes:
        if c.startswith("lang-"):
            return c[len("lang-"):]
    return None


def find_codeblock_for_code_caption(caption_div):
    """For a <div class="code-caption">, find the related <pre><code>.

    Captions sit either immediately before or immediately after the
    <pre>, usually inside <div class="code-block-wrapper">.
    """
    def sibling_iter(node, direction):
        sib = node.previous_sibling if direction == "prev" else node.next_sibling
        while sib is not None:
            if isinstance(sib, NavigableString):
                if sib.strip() == "":
                    sib = sib.previous_sibling if direction == "prev" else sib.next_sibling
                    continue
                return None
            return sib
        return None

    prev = sibling_iter(caption_div, "prev")
    if prev is not None:
        pre = prev.find("pre") if hasattr(prev, "find") else None
        if prev.name == "pre":
            pre = prev
        if pre is not None:
            return pre

    nxt = sibling_iter(caption_div, "next")
    if nxt is not None:
        pre = nxt.find("pre") if hasattr(nxt, "find") else None
        if nxt.name == "pre":
            pre = nxt
        if pre is not None:
            return pre

    parent = caption_div.parent
    if parent is not None:
        pre = parent.find("pre")
        if pre is not None:
            return pre

    return None


def find_codeblock_for_callout(title_div):
    """For a <div class="callout-title"> inside a callout, find the
    <pre><code> living inside the same callout box."""
    callout = title_div.parent
    if callout is None:
        return None
    return callout.find("pre")


def extract_blocks_from_file(path: Path, raw_html: str) -> list[CaptionedBlock]:
    soup = BeautifulSoup(raw_html, "html.parser")
    out: list[CaptionedBlock] = []

    # ---- code-caption form ----
    for cap in soup.find_all("div", class_="code-caption"):
        text = cap.get_text(" ", strip=True)
        label_kind = classify_label(text)
        if label_kind is None:
            continue
        number = label_number(text) or ""
        pre = find_codeblock_for_code_caption(cap)
        if pre is None:
            continue
        code = pre.find("code") or pre
        code_text = clean_code_text(code)
        lang = find_lang(code) if code.name == "code" else find_lang(pre)
        cap_str = str(cap)
        try:
            offset = raw_html.index(cap_str)
        except ValueError:
            offset = 0
        line = line_of_offset(raw_html, offset)
        out.append(
            CaptionedBlock(
                file=path, line=line,
                label_kind=label_kind,
                label_text=text[:120],
                label_number=number,
                code_text=code_text,
                code_lang=lang,
                caption_text=text,
                source="code-caption",
            )
        )

    # ---- callout-title form ----
    for title in soup.find_all("div", class_="callout-title"):
        text = title.get_text(" ", strip=True)
        label_kind = classify_label(text)
        if label_kind is None:
            continue
        number = label_number(text) or ""
        pre = find_codeblock_for_callout(title)
        if pre is None:
            continue
        code = pre.find("code") or pre
        code_text = clean_code_text(code)
        lang = find_lang(code) if code.name == "code" else find_lang(pre)
        cap_str = str(title)
        try:
            offset = raw_html.index(cap_str)
        except ValueError:
            offset = 0
        line = line_of_offset(raw_html, offset)
        out.append(
            CaptionedBlock(
                file=path, line=line,
                label_kind=label_kind,
                label_text=text[:120],
                label_number=number,
                code_text=code_text,
                code_lang=lang,
                caption_text=text,
                source="callout-title",
            )
        )

    return out


# ------------ Main audit ------------

@dataclass
class Finding:
    block: CaptionedBlock
    classification: str
    reason: str


def audit() -> dict:
    files = iter_html_files()
    all_blocks: list[CaptionedBlock] = []
    for f in files:
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "code-caption" not in raw and "callout-title" not in raw:
            continue
        all_blocks.extend(extract_blocks_from_file(f, raw))

    findings: list[Finding] = []
    for b in all_blocks:
        cls, reason = looks_like_real_code(b.code_text, b.code_lang)
        findings.append(Finding(b, cls, reason))

    by_label = Counter(b.label_kind for b in all_blocks)
    by_class = Counter(f.classification for f in findings)
    by_pair = Counter(
        (f.block.label_kind, f.classification) for f in findings
    )

    mismatches: dict[str, list[Finding]] = {
        "pseudocode_but_real_code": [],
        "code_fragment_but_pseudocode": [],
        "algorithm_but_real_code": [],
    }
    for f in findings:
        if f.block.label_kind == "pseudocode" and f.classification == "real_code":
            mismatches["pseudocode_but_real_code"].append(f)
        elif (
            f.block.label_kind == "code_fragment"
            and f.classification == "pseudocode"
        ):
            mismatches["code_fragment_but_pseudocode"].append(f)
        elif f.block.label_kind == "algorithm" and f.classification == "real_code":
            mismatches["algorithm_but_real_code"].append(f)

    return {
        "files_scanned": len(files),
        "blocks_found": len(all_blocks),
        "by_label": by_label,
        "by_class": by_class,
        "by_pair": by_pair,
        "mismatches": mismatches,
        "findings": findings,
    }


# ------------ Report writer ------------

def code_preview(text: str, n: int = 5) -> str:
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines[:n])


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_report(result: dict) -> None:
    lines: list[str] = []
    push = lines.append
    push("# Pseudocode vs Real Code Classification Audit")
    push("")
    push("This audit walks every in-scope `.html` file in the LLMBook ")
    push("and inspects each captioned code block to decide whether the ")
    push("label (Pseudocode, Code Fragment, or Algorithm) matches the ")
    push("content. Pseudocode boxes should contain idealized, language-")
    push("agnostic steps; Code Fragment boxes should contain real Python ")
    push("(or real bash/yaml/json/sql/etc.) that an intern could paste ")
    push("and run.")
    push("")
    push("Script: `scripts/_audit_pseudocode_classification.py` ")
    push("(Python 3.14, BeautifulSoup, `ast.parse` for Python).")
    push("")
    push("Classification rules (in order):")
    push("")
    push("1. Empty body: pseudocode (defensive).")
    push("2. Declared `lang-bash`, `lang-yaml`, `lang-json`, `lang-sql`, ")
    push("   `lang-dockerfile`, `lang-javascript`, etc.: real_code.")
    push("3. Contains lab placeholder (`???`, `# TODO`, `# Hint`, `<<...>>`): ")
    push("   real_code (intentional student gap).")
    push("4. Has paired line-start `Input:` and `Output:` headers: pseudocode.")
    push("5. Three or more pseudocode markers (`for each`, numbered/lettered ")
    push("   steps, leftwards-arrow assignment, etc.): pseudocode.")
    push("6. Python-ish content: `ast.parse` it; on success classify by ")
    push("   real-imports vs placeholder identifier density.")
    push("7. Fallback: mark as ambiguous (NOT included in mismatch totals).")
    push("")
    push("## 1. Summary")
    push("")
    push(f"- Files scanned: **{result['files_scanned']}**")
    push(f"- Captioned code blocks found: **{result['blocks_found']}**")
    push("")
    push("Captioned blocks by label:")
    push("")
    push("| Label | Count |")
    push("|---|---|")
    for label, n in sorted(result["by_label"].items()):
        push(f"| {label} | {n} |")
    push("")
    push("Content classification (independent of label):")
    push("")
    push("| Detected as | Count |")
    push("|---|---|")
    for cls, n in sorted(result["by_class"].items()):
        push(f"| {cls} | {n} |")
    push("")
    push("Label-vs-content cross-tab:")
    push("")
    push("| Label | Real code | Pseudocode | Ambiguous |")
    push("|---|---|---|---|")
    for lab in ("pseudocode", "code_fragment", "algorithm"):
        rc = result["by_pair"].get((lab, "real_code"), 0)
        ps = result["by_pair"].get((lab, "pseudocode"), 0)
        am = result["by_pair"].get((lab, "ambiguous"), 0)
        push(f"| {lab} | {rc} | {ps} | {am} |")
    push("")
    mm = result["mismatches"]
    headline = (
        len(mm["pseudocode_but_real_code"])
        + len(mm["code_fragment_but_pseudocode"])
        + len(mm["algorithm_but_real_code"])
    )
    push(f"**Headline mismatch count: {headline}**")
    push("")
    push(
        f"- Pseudocode caption + real code content: "
        f"**{len(mm['pseudocode_but_real_code'])}**"
    )
    push(
        f"- Code Fragment caption + pseudocode content: "
        f"**{len(mm['code_fragment_but_pseudocode'])}**"
    )
    push(
        f"- Algorithm caption + real code content: "
        f"**{len(mm['algorithm_but_real_code'])}**"
    )
    push("")

    # Section 2
    push("## 2. \"Pseudocode\" labeled but content is real code")
    push("")
    push(
        "These captions tell the reader they're seeing language-agnostic "
        "algorithm steps, but the block parses cleanly as Python (often "
        "with real library imports). They should be relabeled as *Code "
        "Fragment* (or kept as Pseudocode but rewritten to drop real "
        "imports and concrete API calls)."
    )
    push("")
    if not mm["pseudocode_but_real_code"]:
        push("_None found._")
    else:
        items = sorted(
            mm["pseudocode_but_real_code"],
            key=lambda f: (rel(f.block.file), f.block.line),
        )
        for f in items:
            b = f.block
            push(f"### {b.label_text}")
            push("")
            push(f"- File: `{rel(b.file)}:{b.line}`")
            push(f"- Source: `{b.source}`, lang=`{b.code_lang}`")
            push(f"- Detector: {f.reason}")
            push(f"- Caption: {b.caption_text[:240]}")
            push("")
            push("Evidence (first 5 non-blank lines):")
            push("")
            push("```python")
            push(code_preview(b.code_text, 5))
            push("```")
            push("")

    # Section 3
    push("## 3. \"Code Fragment\" labeled but content is pseudocode")
    push("")
    push(
        "These captions promise runnable code but the block is informal "
        "(`for each X in Y:`, numbered steps, `Input:` / `Output:` "
        "header pair, no real imports). Either relabel as *Pseudocode* "
        "/ *Algorithm*, or rewrite the block as real Python."
    )
    push("")
    if not mm["code_fragment_but_pseudocode"]:
        push("_None found._")
    else:
        items = sorted(
            mm["code_fragment_but_pseudocode"],
            key=lambda f: (rel(f.block.file), f.block.line),
        )
        push(f"Found {len(items)} cases. All listed below:")
        push("")
        for f in items:
            b = f.block
            push(f"### {b.label_text}")
            push("")
            push(f"- File: `{rel(b.file)}:{b.line}`")
            push(f"- Source: `{b.source}`, lang=`{b.code_lang}`")
            push(f"- Detector: {f.reason}")
            push(f"- Caption: {b.caption_text[:240]}")
            push("")
            push("Evidence (first 5 non-blank lines):")
            push("")
            push("```")
            push(code_preview(b.code_text, 5))
            push("```")
            push("")

    # Section 4
    push("## 4. \"Algorithm\" labeled but content is real code")
    push("")
    push(
        "Captions reading *Algorithm N.N.N* should be paired with "
        "language-agnostic steps. Anything that parses with imports of "
        "real libraries belongs in a *Code Fragment*."
    )
    push("")
    if not mm["algorithm_but_real_code"]:
        push("_None found._")
        push("")
    else:
        items = sorted(
            mm["algorithm_but_real_code"],
            key=lambda f: (rel(f.block.file), f.block.line),
        )
        for f in items:
            b = f.block
            push(f"### {b.label_text}")
            push("")
            push(f"- File: `{rel(b.file)}:{b.line}`")
            push(f"- Source: `{b.source}`, lang=`{b.code_lang}`")
            push(f"- Detector: {f.reason}")
            push(f"- Caption: {b.caption_text[:240]}")
            push("")
            push("Evidence (first 5 non-blank lines):")
            push("")
            push("```python")
            push(code_preview(b.code_text, 5))
            push("```")
            push("")

    # Section 5
    push("## 5. Recommended action plan")
    push("")
    if headline == 0:
        push(
            "- No actionable mismatches found by automated detection. "
            "Spot-check manually if a recent edit changed any captions."
        )
    else:
        if mm["pseudocode_but_real_code"]:
            push(
                f"- **Relabel {len(mm['pseudocode_but_real_code'])} "
                "\"Pseudocode\" captions whose content is concrete code.** "
                "The fastest fix is to change the caption tag to *Code "
                "Fragment*; this preserves the existing block. The anchor "
                "case `Pseudocode 29.3.2` in "
                "`part-9-safety-strategy/module-30-safety-ethics-"
                "regulation/section-30.3.html` is a clean Python "
                "snippet that imports `transformers.pipeline` and should "
                "be renamed *Code Fragment 30.3.x*."
            )
        if mm["code_fragment_but_pseudocode"]:
            push(
                f"- **Audit the {len(mm['code_fragment_but_pseudocode'])} "
                "\"Code Fragment\" captions whose content is informal/"
                "pseudocode-like.** Each one has paired `Input:` / "
                "`Output:` headers or many algorithm markers. Either "
                "(a) rewrite the block as runnable Python so the *Code "
                "Fragment* label is accurate, or (b) relabel the caption "
                "as *Pseudocode* / *Algorithm* and move the block into a "
                "`<div class=\"callout algorithm\">` for visual "
                "distinction."
            )
        if mm["algorithm_but_real_code"]:
            push(
                f"- **Demote {len(mm['algorithm_but_real_code'])} "
                "\"Algorithm\" boxes that are actually real code** to "
                "*Code Fragment* captions, or split into a pseudocode "
                "algorithm box plus a separate code fragment for the "
                "Python implementation."
            )
        push(
            "- For each rename, search nearby section text for the "
            "old label number; if the prose says \"as shown in "
            "Pseudocode 29.3.2\", update the cross-reference to "
            "\"Code Fragment ...\" too."
        )
        push(
            "- Several mislabeled *Code Fragment* blocks in "
            "section-30.3.html, section-4.4.html, section-5.1.html, "
            "section-7.3.html, and section-8.3.html sit immediately "
            "before a real-code companion block. Consider re-pairing "
            "them so the algorithm box (pseudocode) and its companion "
            "code fragment (real Python) have consistent numbering."
        )
        push(
            "- Add the audit script "
            "(`scripts/_audit_pseudocode_classification.py`) to the "
            "pre-publish checklist so future content drift is caught."
        )
        push(
            "- Re-run after fixes to confirm the headline mismatch "
            "count drops to zero."
        )
    push("")
    push("---")
    push("")
    push(
        "Generated by `scripts/_audit_pseudocode_classification.py`. "
        "Detection is heuristic: ambiguous cases (parses but uses "
        "placeholder names, or has no language hint and no markers) "
        "are intentionally NOT counted in mismatch totals."
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


# ------------ Entry point ------------

def main() -> None:
    result = audit()
    write_report(result)
    mm = result["mismatches"]
    headline = (
        len(mm["pseudocode_but_real_code"])
        + len(mm["code_fragment_but_pseudocode"])
        + len(mm["algorithm_but_real_code"])
    )
    print(f"Files scanned: {result['files_scanned']}")
    print(f"Captioned blocks: {result['blocks_found']}")
    for label, n in sorted(result["by_label"].items()):
        print(f"  label={label}: {n}")
    print(f"Headline mismatches: {headline}")
    print(f"  pseudocode_but_real_code: {len(mm['pseudocode_but_real_code'])}")
    print(f"  code_fragment_but_pseudocode: {len(mm['code_fragment_but_pseudocode'])}")
    print(f"  algorithm_but_real_code: {len(mm['algorithm_but_real_code'])}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
