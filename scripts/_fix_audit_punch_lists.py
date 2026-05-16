#!/usr/bin/env python
"""Dispatch script for applying mechanical fixes from audit punch lists.

Idempotent. Re-runnable. Each category (A-F) is its own function returning
(fixed_count, skipped_count, skip_reasons).

Run:
    /c/Python314/python scripts/_fix_audit_punch_lists.py [A|B|C|D|E|F|all]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Tuple, List, Optional

from bs4 import BeautifulSoup, NavigableString, Tag


ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_PARTS = {"KDP", "node_modules", "pagefind", "scripts", "agents",
                 ".claude", "templates"}


# --------------------------------------------------------------------------
# Path resolver: maps audit-era relative paths to current paths.
# --------------------------------------------------------------------------

def _build_section_index() -> dict[str, Path]:
    """Index all current section/index .html files by basename."""
    index: dict[str, list[Path]] = {}
    for p in ROOT.rglob("*.html"):
        # Skip excluded directories
        parts = set(p.relative_to(ROOT).parts[:1])
        if parts & EXCLUDE_PARTS:
            continue
        if any(seg.startswith("temp_") or "backup" in seg.lower() for seg in p.parts):
            continue
        index.setdefault(p.name, []).append(p)
    return index


def _resolve_audit_path(audit_rel: str, section_index: dict[str, list[Path]]) -> Optional[Path]:
    """Resolve an audit-era relative path against the current tree.

    Try exact relative first; fall back to basename match.
    """
    direct = ROOT / audit_rel.replace("\\", "/")
    if direct.is_file():
        return direct

    basename = Path(audit_rel).name
    candidates = section_index.get(basename, [])
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        # Prefer the one with the closest path stem match
        target_stem = "/".join(Path(audit_rel).parts[-3:])
        for c in candidates:
            if str(c).replace("\\", "/").endswith(target_stem):
                return c
        # Otherwise prefer the one in the same part if possible
        target_part = next((seg for seg in Path(audit_rel).parts if seg.startswith("part-")), None)
        if target_part:
            for c in candidates:
                if target_part in c.parts:
                    return c
        return candidates[0]
    return None


# --------------------------------------------------------------------------
# Generic helpers
# --------------------------------------------------------------------------

def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _write(p: Path, content: str) -> None:
    p.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------
# Category A: Caption colon typos (12 captions missing a colon)
# --------------------------------------------------------------------------

# Category A targets: each entry is a unique caption text snippet that
# identifies the diagram-caption div (post-restructure, file paths and figure
# numbers may have shifted, but the caption prose is unchanged).
CATEGORY_A_CAPTION_MARKERS = [
    "The three-layer architecture separates API concerns",
    "Token streaming pipeline and how each frontend framework",
    "Complete request flow with rate limiting, backpressure queue",
    "The LLMOps lifecycle connects four phases",
    "The OWASP Top 10 for LLM applications organized",
    "A production hallucination pipeline routes",
    "Two geometric views of unlearning in weight space",
    "The four-phase Use Case Discovery Workshop",
    "The LLM Product Metrics Pyramid showing",
    "Side-by-side ROI comparison showing how SaaS",
    "The LLM technology stack with build vs. buy",
    "Monthly compute budget breakdown showing how inference",
]


def category_a_caption_colons(section_index: dict[str, list[Path]]) -> Tuple[int, int, List[str]]:
    """Add colon after 'Figure X.Y.Z' label in diagram-caption divs.

    Searches by content marker (caption prose), since file numbering shifted
    during the book restructure. For each marker, find the diagram-caption div
    that contains it; if its <strong> label has no colon, append one.
    Idempotent.
    """
    fixed = 0
    skipped = 0
    reasons: List[str] = []

    # Build a content-keyed index of all section/index HTML once.
    file_index: list[tuple[Path, str]] = []
    for p in ROOT.rglob("*.html"):
        parts = set(p.relative_to(ROOT).parts[:1])
        if parts & EXCLUDE_PARTS:
            continue
        if any(seg.startswith("temp_") or "backup" in seg.lower() for seg in p.parts):
            continue
        try:
            file_index.append((p, p.read_text(encoding="utf-8")))
        except Exception:
            continue

    for marker in CATEGORY_A_CAPTION_MARKERS:
        candidates = [(p, h) for p, h in file_index if marker in h]
        if not candidates:
            skipped += 1
            reasons.append(f"A: marker not found in any file: '{marker[:40]}...'")
            continue
        # Use the first candidate
        path, html = candidates[0]
        soup = BeautifulSoup(html, "html.parser")

        changed_this_file = False
        for div in soup.select("div.diagram-caption"):
            div_text = div.get_text()
            if marker not in div_text:
                continue
            strong = div.find("strong")
            if not strong:
                continue
            strong_text = strong.get_text()
            # Canonical form check: ends with ":"
            if strong_text.rstrip().endswith(":"):
                continue
            # Next sibling check: starts with ":"
            nxt = strong.next_sibling
            if isinstance(nxt, NavigableString) and str(nxt).lstrip().startswith(":"):
                continue
            # Apply fix: put colon inside the <strong>.
            strong.string = strong_text.rstrip() + ":"
            changed_this_file = True
            break

        if changed_this_file:
            _write(path, str(soup))
            fixed += 1

    return fixed, skipped, reasons


# --------------------------------------------------------------------------
# Category B: Orphan code-output blocks (8 blocks)
# --------------------------------------------------------------------------

# The audit lists these explicitly. Map each to a decision:
#   "wrap"     -> the previous <pre> exists and belongs with this output; wrap in code-block-wrapper.
#   "note"     -> the output is standalone explanatory output; convert to <div class="callout note">.
CATEGORY_B_TARGETS = [
    # (audit_rel, line_hint, output_preview, decision)
    ("appendices/appendix-c-python-for-llm/section-c.1.html", 152,
     "CUDA available: True", "note"),
    ("appendices/appendix-c-python-for-llm/section-c.1.html", 158,
     "Training examples: 8923", "note"),
    ("appendices/appendix-d-environment-setup/section-d.2.html", 48,
     "nvcc: NVIDIA", "note"),
    ("part-2-understanding-llms/module-10-interpretability/section-10.1.html", 312,
     "Epoch 5: loss=", "note"),
    ("part-5-retrieval-conversation/module-20-conversational-ai/section-20.2.html", 178,
     "You are Chef Marco", "note"),
    ("part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html", 322,
     "Discussed database options", "note"),
    ("part-5-retrieval-conversation/module-20-conversational-ai/section-20.3.html", 592,
     "User is vegetarian", "note"),
    ("part-6-agentic-ai/module-21-ai-agents/section-21.5.html", 261,
     "Step 1 (lookup_order): success", "note"),
]


def category_b_orphan_outputs(section_index: dict[str, list[Path]]) -> Tuple[int, int, List[str]]:
    """For each orphan code-output div, convert to a callout note.

    Content-marker driven (paths shifted post-restructure). For each (marker,
    decision) pair, find the file containing it, then find the unique orphan
    code-output div whose text includes the marker. An orphan code-output is
    a `<div class="code-output">` whose previous element-sibling is not a
    `<pre>` or a code-block-wrapper containing one.
    """
    fixed = 0
    skipped = 0
    reasons: List[str] = []

    markers = [(preview, decision) for _, _, preview, decision in CATEGORY_B_TARGETS]

    # Build a file index to find each marker.
    file_index: list[tuple[Path, str]] = []
    for p in ROOT.rglob("*.html"):
        parts = set(p.relative_to(ROOT).parts[:1])
        if parts & EXCLUDE_PARTS:
            continue
        if any(seg.startswith("temp_") or "backup" in seg.lower() for seg in p.parts):
            continue
        try:
            file_index.append((p, p.read_text(encoding="utf-8")))
        except Exception:
            continue

    # Group markers by file for one-pass editing.
    # Prefer files where the marker appears inside an ORPHAN code-output div
    # (one whose previous element-sibling is not a <pre>).
    file_to_markers: dict[Path, list[tuple[str, str]]] = {}
    for marker, decision in markers:
        cand_orphan = []
        cand_anywhere = []
        for p, h in file_index:
            if marker not in h:
                continue
            cand_anywhere.append(p)
            # Parse and check if marker is in an orphan code-output.
            try:
                soup_check = BeautifulSoup(h, "html.parser")
            except Exception:
                continue
            for div in soup_check.select("div.code-output"):
                if marker not in div.get_text():
                    continue
                prev = div.find_previous_sibling()
                if isinstance(prev, Tag):
                    if prev.name == "pre":
                        continue  # paired, not orphan
                    if prev.name == "div" and "code-block-wrapper" in (prev.get("class") or []):
                        continue
                cand_orphan.append(p)
                break
        cand_files = cand_orphan if cand_orphan else cand_anywhere
        if not cand_files:
            skipped += 1
            reasons.append(f"B: marker not found: '{marker}'")
            continue
        file_to_markers.setdefault(cand_files[0], []).append((marker, decision))

    for path, entries in file_to_markers.items():
        html = _read(path)
        soup = BeautifulSoup(html, "html.parser")

        outputs = soup.select("div.code-output")
        for div in outputs:
            prev = div.find_previous_sibling()
            if isinstance(prev, Tag):
                if prev.name == "pre":
                    continue
                if prev.name == "div" and "code-block-wrapper" in (prev.get("class") or []):
                    continue

            text = div.get_text(" ", strip=True)
            matched_entry = None
            for marker, decision in entries:
                if marker in text:
                    matched_entry = (marker, decision)
                    break
            if matched_entry is None:
                continue

            _, decision = matched_entry

            if decision == "note":
                new_callout = soup.new_tag("div", attrs={"class": "callout note"})
                title = soup.new_tag("div", attrs={"class": "callout-title"})
                title.string = "Example output"
                new_callout.append(title)
                body = soup.new_tag("pre", attrs={"class": "callout-output-body"})
                output_text = re.sub(r"^\s*Output:?\s*", "", text)
                body.string = output_text
                new_callout.append(body)
                div.replace_with(new_callout)
                fixed += 1
            elif decision == "wrap":
                if not (isinstance(prev, Tag) and prev.name == "pre"):
                    skipped += 1
                    reasons.append(f"B: no preceding <pre> in {path.name}")
                    continue
                wrapper = soup.new_tag("div", attrs={"class": "code-block-wrapper"})
                prev.insert_before(wrapper)
                wrapper.append(prev.extract())
                wrapper.append(div.extract())
                fixed += 1

        _write(path, str(soup))

    return fixed, skipped, reasons


# --------------------------------------------------------------------------
# Category C: Broken figure references
# --------------------------------------------------------------------------

# Live-scan results from the post-restructure tree: 7 broken Figure X.Y.Z
# citations. Audit listed 5; we handle all 7 found in the current tree, since
# they all pattern-match the same template (prose cites a figure followed by
# a <p class="figure-replaced"><em>...</em></p> placeholder that was never
# turned into a real diagram). The TODO marker preserves the editorial intent
# without making up content.
CATEGORY_C_BROKEN_FIGURE_REFS = [
    # (citation, expected-substring-of-paragraph) -- the expected-substring
    # disambiguates when a number occurs multiple times.
    ("Figure 37.2.3", "arranges these along a spectrum"),
    ("Figure 37.3.3", "compares what each document covers"),
    ("Figure 37.4.3", "maps the regulatory obligations by sector"),
    ("Figure 37.5.2", "illustrates how each entry links to the previous"),
    ("Figure 37.6.2", "shows the three-step process"),
    ("Figure 41.2.4", "depicts this rapid iteration cycle"),
    ("Figure 52.2.2", "maps the regulatory landscape for financial"),
]


def category_c_broken_figures(section_index: dict[str, list[Path]]) -> Tuple[int, int, List[str]]:
    """Mark broken figure refs with TODO HTML comments.

    The 7 broken figure citations all follow the same template: prose cites a
    Figure X.Y.Z immediately followed by a `<p class="figure-replaced"><em>...
    </em></p>` placeholder. The right action is to flag each with an HTML
    comment for later authoring -- removing the prose would lose editorial
    intent, and guessing at content would be worse.
    """
    from bs4 import Comment

    fixed = 0
    skipped = 0
    reasons: List[str] = []

    # Build file index keyed by citation.
    file_index: list[tuple[Path, str]] = []
    for p in ROOT.rglob("*.html"):
        parts = set(p.relative_to(ROOT).parts[:1])
        if parts & EXCLUDE_PARTS:
            continue
        if any(seg.startswith("temp_") or "backup" in seg.lower() for seg in p.parts):
            continue
        try:
            file_index.append((p, p.read_text(encoding="utf-8")))
        except Exception:
            continue

    for citation, context_marker in CATEGORY_C_BROKEN_FIGURE_REFS:
        marker_text = f'TODO(audit): broken figure ref "{citation}"'

        candidates = [(p, h) for p, h in file_index if context_marker in h and citation in h]
        if not candidates:
            skipped += 1
            reasons.append(f"C: cannot find broken ref '{citation}' (context: '{context_marker[:30]}')")
            continue
        path, html = candidates[0]

        # Idempotent: if already marked, skip.
        if marker_text in html:
            continue

        soup = BeautifulSoup(html, "html.parser")
        changed = False
        # Find the <p> that contains both the citation and the context.
        for p_tag in soup.find_all("p"):
            text = p_tag.get_text()
            if citation in text and context_marker in text:
                comment = Comment(f' {marker_text}: target figure does not exist; either author the diagram or remove this sentence and the following figure-replaced placeholder ')
                p_tag.insert_before(comment)
                changed = True
                break
        if changed:
            _write(path, str(soup))
            fixed += 1
        else:
            skipped += 1
            reasons.append(f"C: citation '{citation}' not located in expected context in {path.name}")

    return fixed, skipped, reasons


# --------------------------------------------------------------------------
# Category D: Pseudocode reformat fixes
# --------------------------------------------------------------------------

# The audit listed these in pre-restructure paths. Resolve by content marker.
PSEUDOCODE_KEYWORD_TARGETS = [
    # (anchor_text, file_marker)
    # 1. Debate algorithm (section-17.5.html old -> section-20.5.html new)
    ("AI Safety via Debate", "Pseudocode 35.1.1"),
    # 2. MCP handshake (section-22.2.html old -> section-27.2.html new)
    ("MCP initialization handshake", "Pseudocode 22.2.1"),
    # 3. PPO training loop (section-17.1.html old -> section-20.1.html new)
    ("PPO training loop", "Pseudocode 16.1.3"),
    # 4. ReAct loop (section-21.1.html old -> section-26.1.html new)
    ("formalizes the ReAct agent loop", "Pseudocode 26.1.2"),  # already algo-helper? check
]


PSEUDOCODE_KEYWORDS = {"Input:", "Output:", "for", "while", "if", "else", "return",
                       "Initialize", "while", "do", "end"}


def _convert_pseudocode_to_algo_helper(pre_tag: Tag) -> bool:
    """Convert a pyg-text-bad or bold-styled pseudocode block to algo-helper.

    Returns True if changed, False if already in algo-helper form.
    """
    code = pre_tag.find("code")
    if code is None:
        return False

    code_classes = code.get("class") or []
    # Idempotent: if class includes language-none + we have algo-line-keyword,
    # then it's already converted.
    has_helper = bool(code.find("span", class_="algo-line-keyword"))
    if has_helper and "language-none" in code_classes:
        return False

    # Extract plain text from code (stripping Pygments markup but keeping text).
    raw_text = code.get_text()

    # Build a new <code> with language-none and algo-line-keyword spans.
    new_code = BeautifulSoup("", "html.parser").new_tag("code")
    new_code["class"] = ["language-none"]

    # Process line by line.
    lines = raw_text.split("\n")
    for i, line in enumerate(lines):
        # Match leading keyword like "Input:", "Output:", "for", "while", "if", "return", "Initialize"
        stripped = line.lstrip()
        leading_ws = line[: len(line) - len(stripped)]
        m = re.match(r"^(Input:|Output:|for\b|while\b|if\b|else\b|return\b|Initialize\b|do\b|end\b)", stripped)
        if m:
            kw = m.group(1)
            rest = stripped[len(kw):]
            new_code.append(NavigableString(leading_ws))
            span = BeautifulSoup("", "html.parser").new_tag("span")
            span["class"] = ["algo-line-keyword"]
            span.string = kw
            new_code.append(span)
            new_code.append(NavigableString(rest))
        else:
            # Check for inline comments like "// foo"
            m2 = re.search(r"(.*?)(//.*)$", line)
            if m2:
                pre_part, comment_part = m2.group(1), m2.group(2)
                new_code.append(NavigableString(pre_part))
                cspan = BeautifulSoup("", "html.parser").new_tag("span")
                cspan["class"] = ["algo-line-comment"]
                cspan.string = comment_part
                new_code.append(cspan)
            else:
                new_code.append(NavigableString(line))
        if i < len(lines) - 1:
            new_code.append(NavigableString("\n"))

    code.replace_with(new_code)

    # Also strip pygments-highlighted from pre if present.
    pre_classes = pre_tag.get("class") or []
    pre_tag["class"] = [c for c in pre_classes if c != "pygments-highlighted"]
    return True


def _renumber_steps(pre_tag: Tag) -> Tuple[bool, str]:
    """Complete step numbering for blocks that only number their top two steps.

    Strategy: read the code as plain text, find lines starting with "1." or "2.",
    then continue numbering any unnumbered lines that look like steps (indentation
    similar to the numbered ones, not sub-steps starting with 'a.', 'b.', etc.)
    until end. Returns (changed, reason_if_unchanged).
    """
    code = pre_tag.find("code")
    if code is None:
        return False, "no-code-tag"
    raw = code.get_text()
    lines = raw.split("\n")

    # Find numbered top-level steps.
    numbered_step_re = re.compile(r"^(\s*)(\d+)\.\s")
    sub_step_re = re.compile(r"^(\s*)[a-z]\.\s")
    blank_re = re.compile(r"^\s*$")

    top_level_indent: Optional[str] = None
    last_num = 0
    for line in lines:
        m = numbered_step_re.match(line)
        if m:
            indent = m.group(1)
            n = int(m.group(2))
            if top_level_indent is None:
                top_level_indent = indent
            elif indent != top_level_indent:
                continue  # this is a nested numbered step, ignore
            if n > last_num:
                last_num = n

    if last_num < 2 or top_level_indent is None:
        return False, "no-numbered-steps"

    # Walk lines; if a line at top_level_indent is unnumbered, not blank, not a
    # sub-step letter, and not an "Input:"/"Output:" line, renumber it.
    new_lines: list[str] = []
    next_num = last_num + 1
    started_numbering = False
    found_seq = False
    for line in lines:
        m = numbered_step_re.match(line)
        if m and m.group(1) == top_level_indent:
            new_lines.append(line)
            found_seq = True
            started_numbering = True
            continue
        if not started_numbering:
            new_lines.append(line)
            continue
        # We've started numbering. Decide if this is an unnumbered top-level step.
        if blank_re.match(line):
            new_lines.append(line)
            continue
        if sub_step_re.match(line):
            new_lines.append(line)
            continue
        # Identify whether this is at top-level indent and looks like a step.
        # Heuristic: the line begins with top_level_indent followed by a non-whitespace.
        if line.startswith(top_level_indent) and not line.startswith(top_level_indent + " ") and not line.startswith(top_level_indent + "\t"):
            # And not e.g. "Input:" / "Output:" labels
            stripped = line.lstrip()
            if stripped.lower().startswith(("input:", "output:")):
                new_lines.append(line)
                continue
            # Renumber: prepend top_level_indent + "{next_num}. " then content.
            content = stripped
            # Only renumber if it isn't already prefixed with a digit.
            if not re.match(r"^\d+\.\s", content):
                new_lines.append(f"{top_level_indent}{next_num}. {content}")
                next_num += 1
                continue
        new_lines.append(line)

    if next_num == last_num + 1:
        return False, "nothing-to-renumber"
    if not found_seq:
        return False, "no-numbered-seq-found"

    new_text = "\n".join(new_lines)
    if new_text == raw:
        return False, "no-change"

    # Idempotency check: don't replace if the result equals current text.
    # Replace the code contents
    code.clear()
    code.append(NavigableString(new_text))
    return True, "ok"


def _fix_broken_interspersed_numbering(pre_tag: Tag) -> bool:
    """Strip bogus top-level numbers off lines that are continuations.

    RLVR block has:
        1. for iteration = 1 to T:
        a. Sample ...
        b. for each problem ...
            3. Generate solution ...     <-- bogus, should be unnumbered continuation
        c. for each solution ...
            4. r_i = V(...) ...           <-- bogus
            5. (e.g., ...)                <-- bogus
        d. ...
        e. Update ...
            6. expected reward ...        <-- bogus
        2. return pi*

    The top-level sequence is "1. ... 2." with sub-step letters a-e under step 1.
    The "3.", "4.", "5.", "6." labels are interspersed mid-substep and should
    be removed (the lines become continuation lines, sometimes joined to the
    preceding sub-step).
    """
    code = pre_tag.find("code")
    if code is None:
        return False
    raw = code.get_text()
    lines = raw.split("\n")

    # Identify top-level numbered steps and sub-step letters.
    # Top level: zero or one leading space + N. + space
    # Sub-step:  one or more leading spaces + [a-z]. + space
    top_re = re.compile(r"^( {0,1})(\d+)\.\s")
    sub_re = re.compile(r"^( +)[a-z]\.\s")

    # Find legitimate top-level numbers: those preceded by content that suggests
    # a new top-level step.
    # Strategy: keep the FIRST top-level (1.) and the LAST one (which is the
    # max number, but seen out-of-sequence). Strip the rest.
    # The audit pattern: top-level "1." appears once, then "2." appears at the
    # very end. Numbers 3+ in between are wrong.
    top_locs: list[tuple[int, int]] = []  # (line_idx, num)
    for i, line in enumerate(lines):
        m = top_re.match(line)
        if m:
            top_locs.append((i, int(m.group(2))))

    if len(top_locs) < 3:
        return False  # not the broken pattern

    # Identify "good" top-level numbers: 1 (first) and 2 (last sequential).
    # The pattern here is 1 (at top), 3, 4, 5, 6 (interspersed), 2 (at end).
    # Mark for stripping: numbers that are out of sequence (i.e., greater than
    # the next legitimate step).
    # A simpler heuristic: the first "1." is good; everything else with a number
    # >= 3 interspersed before "2." is bad and should be stripped.
    first_line_of_one = top_locs[0]
    last_line_of_two = next((loc for loc in reversed(top_locs) if loc[1] == 2), None)
    if last_line_of_two is None:
        return False

    # Lines to strip: those with top number in [3, last_line_of_two[0])
    strip_indices: set[int] = set()
    for idx, num in top_locs:
        if idx == first_line_of_one[0]:
            continue
        if idx == last_line_of_two[0]:
            continue
        if first_line_of_one[0] < idx < last_line_of_two[0]:
            strip_indices.add(idx)

    if not strip_indices:
        return False

    new_lines: list[str] = []
    for i, line in enumerate(lines):
        if i in strip_indices:
            # Strip the "N. " prefix; keep the rest.
            stripped = top_re.sub(r"\1", line)
            new_lines.append(stripped)
        else:
            new_lines.append(line)

    new_text = "\n".join(new_lines)
    if new_text == raw:
        return False
    code.clear()
    code.append(NavigableString(new_text))
    return True


def _standardize_substep_indent(pre_tag: Tag) -> bool:
    """Standardize a/b/c sub-step indent to 2 spaces.

    Two cases handled:
      1. Existing 1-space indent ` a.` -> `  a.`
      2. Zero indent `a.` at start of line, but ONLY when context shows the
         block uses top-level digit numbering (e.g., `1.`, `2.`) — in which
         case the unindented letters are sub-steps that should be indented.

    Operates on text nodes directly to preserve existing markup (e.g.
    algo-line-keyword spans).
    """
    code = pre_tag.find("code")
    if code is None:
        return False

    # Inspect full text to decide case.
    full = code.get_text()
    has_one_space_letters = bool(re.search(r"(?:^|\n) {1}[a-z]\.\s", full))
    has_zero_indent_letters = bool(re.search(r"(?:^|\n)[a-z]\.\s", full))
    has_top_level_numbering = bool(re.search(r"(?:^|\n)\d+\.\s", full))

    changed = False
    if has_one_space_letters:
        pat = re.compile(r"(^|\n)( {1})([a-z])\.\s")
        for node in list(code.descendants):
            if not isinstance(node, NavigableString):
                continue
            s = str(node)
            new_s = pat.sub(r"\1  \3. ", s)
            if new_s != s:
                node.replace_with(NavigableString(new_s))
                changed = True

    if not changed and has_zero_indent_letters and has_top_level_numbering:
        # Indent zero-space sub-step letters to 2 spaces.
        # Pattern: \n + [a-z] + . + space (no leading whitespace).
        pat = re.compile(r"(^|\n)([a-z])\.\s")
        for node in list(code.descendants):
            if not isinstance(node, NavigableString):
                continue
            s = str(node)
            new_s = pat.sub(r"\1  \2. ", s)
            if new_s != s:
                node.replace_with(NavigableString(new_s))
                changed = True

        if not changed:
            # Span-per-token Pygments markup hides the newline-then-letter
            # pattern across nodes. Rebuild code element with plain text:
            # collapse spans, then re-apply indent. (Acceptable trade-off:
            # we lose Pygments coloring on this block, which the audit calls
            # 'pyg-text-bad' anyway.)
            new_text = re.sub(r"(^|\n)([a-z])\.\s", r"\1  \2. ", full)
            if new_text != full:
                code.clear()
                code.append(NavigableString(new_text))
                changed = True

    return changed


# Per-block decisions for category D.
# Tuple: (anchor_marker_substring, action)
#   action in {"keyword", "renumber", "indent"} or combinations as list.
CATEGORY_D_TARGETS = [
    # 4 keyword-conversion blocks (covert pyg-text-bad / bold to algo-helper).
    {
        # Debate algorithm; current label "Pseudocode 48.1.1" in section-20.5.html.
        "marker": "AI Safety via Debate algorithm",
        "actions": ["keyword"],
    },
    {
        # MCP handshake; current label "Pseudocode 22.2.1" (kept).
        "marker": "MCP initialization handshake",
        "actions": ["keyword"],
    },
    {
        # PPO training loop; current label "Pseudocode 16.1.3" (kept).
        "marker": "PPO training loop for RLHF",
        "actions": ["keyword"],
    },
    {
        # ReAct loop; current label "Pseudocode 26.1.2".
        "marker": "formalizes the ReAct agent loop",
        "actions": ["keyword", "indent"],
    },
    # 3 step-numbering blocks (complete the partial top-level numbering).
    {
        "marker": "Mamba selective scan algorithm",  # Pseudocode 61.3.X (post-restructure)
        "actions": ["renumber"],
    },
    {
        "marker": "RLVR training loop generates",  # Pseudocode 9.3.4
        "actions": ["renumber_fix"],
    },
    {
        "marker": "bucket rate limiting algorithm",  # Pseudocode 34.3.1
        "actions": ["renumber", "indent"],
    },
    # Indent-standardization blocks (1-space -> 2-space sub-step indent).
    # The audit flagged 5 blocks with "surprising" 1-space indent. Two are
    # already covered above (Token bucket, ReAct). The remaining three need
    # only the indent fix.
    {
        "marker": "Function calling loop",  # Pseudocode 26.1.1
        "actions": ["indent"],
    },
    {
        "marker": "Automated red teaming pipeline",  # Pseudocode 35.8.1
        "actions": ["indent"],
    },
    {
        "marker": "supervisor (hub-and-spoke) pattern",  # Pseudocode 27.2.1
        # The supervisor block uses Pygments per-token markup and 0-indent
        # sub-step letters (different case from the 1-space audit). Apply
        # zero-indent handling which rebuilds the code element.
        "actions": ["indent"],
    },
]


def category_d_pseudocode(section_index: dict[str, list[Path]]) -> Tuple[int, int, List[str]]:
    """Apply pseudocode keyword/numbering/indent fixes."""
    fixed = 0
    skipped = 0
    reasons: List[str] = []

    for target in CATEGORY_D_TARGETS:
        marker = target["marker"]
        actions = target["actions"]

        # Find the file containing the marker
        candidates = []
        for path in ROOT.rglob("section-*.html"):
            parts = set(path.relative_to(ROOT).parts[:1])
            if parts & EXCLUDE_PARTS:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                continue
            if marker in content:
                candidates.append(path)
        if not candidates:
            skipped += 1
            reasons.append(f"D: marker not found for '{marker}'")
            continue
        # Use first match
        path = candidates[0]
        html = _read(path)
        soup = BeautifulSoup(html, "html.parser")

        # Locate the algorithm callout containing the marker.
        pre_to_fix = None
        for callout in soup.select("div.callout.algorithm"):
            text = callout.get_text()
            if marker in text:
                pre_to_fix = callout.find("pre")
                if pre_to_fix is not None:
                    break

        if pre_to_fix is None:
            skipped += 1
            reasons.append(f"D: no <pre> in callout for '{marker}'")
            continue

        block_changed = False
        for action in actions:
            if action == "keyword":
                if _convert_pseudocode_to_algo_helper(pre_to_fix):
                    block_changed = True
            elif action == "renumber":
                changed, _ = _renumber_steps(pre_to_fix)
                if changed:
                    block_changed = True
            elif action == "renumber_fix":
                # Special case: block has interspersed bogus top-level numbers
                # mixed with sub-step letters. Strip incorrect top-level numbers
                # off lines that are clearly continuations of the letter-prefixed
                # sub-steps.
                if _fix_broken_interspersed_numbering(pre_to_fix):
                    block_changed = True
            elif action == "indent":
                if _standardize_substep_indent(pre_to_fix):
                    block_changed = True

        if block_changed:
            _write(path, str(soup))
            fixed += 1
        else:
            # Idempotent no-op (already fixed) — don't count as skipped.
            pass

    return fixed, skipped, reasons


# --------------------------------------------------------------------------
# Category E: Wide-cell tables (14 tables)
# --------------------------------------------------------------------------

# For each wide cell, the audit gives a substring that uniquely identifies it.
# Files paths shifted post-restructure, so we search by content marker.
CATEGORY_E_MARKERS = [
    "AI transparency labels are in the UI",
    "General-purpose AI model providers must publish technical documentation",
    "Check provider ToS for training data generation permissions",
    'You may not use outputs to "develop any artificial intelligence models',
    "considers tokens whose cumulative probability reaches",
    "Scales weights by",
    "Weight initialization, noise in diffusion models",
    "R1 is the first open-weights",
    "Cost-competitive training; integrated in Intel cloud partners",
    "Standardizes how streaming agent events are surfaced",
    "Multiple evaluation methods; statistical analysis; honest reporting",
    "Structured reasoning explores the solution space more efficiently",
    "Abstractive keyphrases, categorization, domain-specific extraction",
    "Safety-critical outputs, evidence-based citations, regulatory compliance",
]


def _insert_breaks_at_sentence_boundaries(td: Tag, marker_substr: str) -> bool:
    """Insert <br/> elements at sentence boundaries in a wide table cell.

    Idempotent: if td already contains <br/> tags, skip.
    """
    if td.find("br"):
        return False
    # Only operate if the marker substring appears in the cell text.
    text = td.get_text()
    if marker_substr not in text:
        return False
    # Strategy: take the cell's full text, split at ". " boundaries, rebuild
    # with <br/> tags. Only act if there are >=2 sentences and total length > 100.
    if len(text) < 100:
        return False
    sentences = re.split(r"(?<=[\.!?])\s+", text.strip())
    # Skip if only one sentence
    if len(sentences) < 2:
        return False
    # Skip cells that contain rich markup (img, a, span); we don't want to
    # destroy structure. Only act on cells whose only children are text nodes
    # or simple inline tags.
    for child in td.children:
        if isinstance(child, Tag) and child.name not in ("a", "code", "em", "strong", "i", "b", "br"):
            return False
    # Clear and rebuild.
    td.clear()
    for i, sent in enumerate(sentences):
        if i > 0:
            td.append(BeautifulSoup("<br/>", "html.parser"))
        td.append(NavigableString(sent.strip()))
    return True


def category_e_wide_tables(section_index: dict[str, list[Path]]) -> Tuple[int, int, List[str]]:
    """Insert line breaks in wide table cells using content markers."""
    fixed = 0
    skipped = 0
    reasons: List[str] = []

    # Build a small index for fast lookup.
    file_index: list[tuple[Path, str]] = []
    for p in ROOT.rglob("*.html"):
        parts = set(p.relative_to(ROOT).parts[:1])
        if parts & EXCLUDE_PARTS:
            continue
        if any(seg.startswith("temp_") or "backup" in seg.lower() for seg in p.parts):
            continue
        try:
            file_index.append((p, p.read_text(encoding="utf-8")))
        except Exception:
            continue

    for marker in CATEGORY_E_MARKERS:
        candidates = [(p, h) for p, h in file_index if marker in h]
        if not candidates:
            skipped += 1
            reasons.append(f"E: marker not found: '{marker[:40]}...'")
            continue
        path, html = candidates[0]
        soup = BeautifulSoup(html, "html.parser")
        changed = False
        for td in soup.find_all(["td", "th"]):
            if marker in td.get_text():
                if _insert_breaks_at_sentence_boundaries(td, marker):
                    changed = True
                    break
        if changed:
            _write(path, str(soup))
            fixed += 1

    return fixed, skipped, reasons


# --------------------------------------------------------------------------
# Category F: Overlong alt-text (62 images)
# --------------------------------------------------------------------------

# Threshold: alt > 250 chars. Split into:
#   - primary alt: first ~140 chars at a natural boundary (sentence/clause).
#   - figcaption supplemental description: the rest, wrapped in
#     <span class="alt-supplemental">...</span> appended to the figcaption if
#     a figcaption exists; otherwise stored as aria-describedby pointer.

# We do this generically: every <img alt="..."> whose alt > 250 chars and which
# is inside a <figure> with a <figcaption> gets the trim treatment.

def _split_alt_text(alt: str, limit: int = 140) -> tuple[str, str]:
    """Split alt into (short, long_remainder)."""
    if len(alt) <= limit:
        return alt, ""
    # Find a sentence boundary near `limit`.
    # Prefer ". ", then "; ", then ", ", then " ".
    for sep in [". ", "; ", ", ", " "]:
        # Find the last occurrence of sep within [80, limit+30].
        window = alt[: limit + 30]
        idx = window.rfind(sep)
        if 50 <= idx <= limit + 30:
            short = alt[: idx + (1 if sep == " " else len(sep) - 1)].rstrip(" ,;")
            long_rem = alt[idx + len(sep):].lstrip()
            # Make sure short ends with a sentence-ish boundary.
            if not short.endswith((".", "!", "?")):
                short = short.rstrip(",;:") + "."
            return short, long_rem
    # Fallback: hard split at limit
    return alt[:limit].rstrip() + "...", alt[limit:].lstrip()


def category_f_overlong_alt(section_index: dict[str, list[Path]]) -> Tuple[int, int, List[str]]:
    """Trim overlong alt attributes; move detail to figcaption."""
    fixed = 0
    skipped = 0
    reasons: List[str] = []

    # Discover all candidates by scanning every HTML file once.
    for path in ROOT.rglob("*.html"):
        parts = set(path.relative_to(ROOT).parts[:1])
        if parts & EXCLUDE_PARTS:
            continue
        if any(seg.startswith("temp_") or "backup" in seg.lower() for seg in path.parts):
            continue
        try:
            html = _read(path)
        except Exception:
            continue
        if "alt=" not in html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        any_changed = False
        for img in soup.find_all("img"):
            alt = img.get("alt", "")
            if not alt or len(alt) <= 250:
                continue
            # Idempotency: if a sibling figcaption already contains a
            # <span class="alt-supplemental">, skip.
            parent = img.parent
            figure = img.find_parent("figure")
            figcap = figure.find("figcaption") if figure else None
            if figcap and figcap.find("span", class_="alt-supplemental"):
                continue
            short, long_rem = _split_alt_text(alt, limit=140)
            if not long_rem:
                continue
            # Update alt
            img["alt"] = short
            # Append supplemental to figcaption if present
            if figcap is not None:
                # Add a span with the long description.
                sup = soup.new_tag("span", attrs={"class": "alt-supplemental", "hidden": ""})
                sup.string = long_rem
                figcap.append(sup)
            else:
                # If no figcaption, append a hidden description sibling and
                # set aria-describedby.
                # Generate a stable id from the image src
                src = img.get("src", "")
                base = re.sub(r"[^a-z0-9]+", "-", Path(src).stem.lower()).strip("-")
                if not base:
                    base = f"img-{abs(hash(short)) % 100000}"
                desc_id = f"{base}-desc"
                if not parent.find(id=desc_id):
                    span = soup.new_tag("span", attrs={"id": desc_id, "class": "alt-supplemental", "hidden": ""})
                    span.string = long_rem
                    img.insert_after(span)
                img["aria-describedby"] = desc_id
            any_changed = True
            fixed += 1
        if any_changed:
            _write(path, str(soup))

    return fixed, skipped, reasons


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    target = argv[1].upper() if len(argv) > 1 else "ALL"
    if target == "ALL":
        targets = ["A", "B", "C", "D", "E", "F"]
    else:
        targets = [t.strip() for t in target.split(",") if t.strip()]

    section_index = _build_section_index()

    results: dict[str, tuple[int, int, list[str]]] = {}
    if "A" in targets:
        results["A"] = category_a_caption_colons(section_index)
    if "B" in targets:
        results["B"] = category_b_orphan_outputs(section_index)
    if "C" in targets:
        results["C"] = category_c_broken_figures(section_index)
    if "D" in targets:
        results["D"] = category_d_pseudocode(section_index)
    if "E" in targets:
        results["E"] = category_e_wide_tables(section_index)
    if "F" in targets:
        results["F"] = category_f_overlong_alt(section_index)

    print("\n=== Audit punch-list dispatch summary ===")
    for cat in ["A", "B", "C", "D", "E", "F"]:
        if cat not in results:
            continue
        fixed, skipped, reasons = results[cat]
        print(f"  Category {cat}: fixed={fixed}, skipped={skipped}")
        for r in reasons:
            print(f"    - {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
