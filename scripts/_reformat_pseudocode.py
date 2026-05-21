"""Reformat pseudocode blocks per pseudocode-readability-audit.md.

Works directly on the raw HTML source as text, NOT via BeautifulSoup
round-trip, because BS4 normalizes leading-whitespace inside <code> blocks
and that destroys the visual indentation of Pygments-highlighted pseudocode.

Five sub-tasks, each idempotent:

  T1  Convert pyg-text-bad pseudocode blocks to algo-helper style.
      Targets: 27.1 (26.1.1), 35.3 (34.3.1), 37.8 (35.8.1).

  T2  Add `# Input:` and `# Output:` comment header lines to 8 dense
      pyg-python pseudocode blocks.

  T3  Renumber + algo-helper convert RLVR (Pseudocode 9.3.4) first <pre>.

  T4  Standardize 1-space sub-step indent to 2-space in pseudocode blocks.

  T5  Insert phase-separator blank lines in dense pyg-python pseudocode
      blocks (before `def ` / `class ` / `@` at indent 0).

Run with `--apply` to write; default is dry-run.
"""

from __future__ import annotations

import argparse
import ast
import io
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent


# --------------------------------------------------------------------------- #
# Block locator
# --------------------------------------------------------------------------- #


def find_algorithm_pre_block(html: str, title_marker: str,
                             which: int = 0) -> tuple[int, int, int, int] | None:
    """Find the `<div class="callout algorithm">` whose callout-title contains
    `title_marker`, then return positions of the N-th `<pre ...>` content:

      Returns (pre_open_start, pre_open_end, pre_close_start, pre_close_end)
      where pre_open_start..pre_open_end covers the opening <pre ...>, and
      pre_close_start..pre_close_end covers the matching `</pre>`.

    `which=0` -> first <pre>, `which=1` -> second, etc.
    """
    # Find every callout-algorithm <div> and its closing.
    for m in re.finditer(r'<div class="callout algorithm">', html):
        start = m.start()
        # Find the matching </div> by counting nesting. We assume the structure
        # uses a fixed depth: outer <div class="callout algorithm">, optional
        # title <div>, optional <div class="code-block-wrapper">, <pre>, </pre>,
        # close wrappers.
        # Heuristic: find the title line and verify marker.
        title_m = re.search(r'<div class="callout-title">([^<]*?)</div>',
                            html[start:start + 4000])
        if not title_m or title_marker not in title_m.group(1):
            continue
        # Now find Nth <pre ...> inside this callout block.
        # We'll match nested-div boundaries by counting from this <div>.
        depth = 0
        pos = start
        pre_count = 0
        while pos < len(html):
            div_open = html.find("<div", pos)
            div_close = html.find("</div>", pos)
            pre_open = html.find("<pre", pos)

            # Pick the nearest event.
            candidates = [c for c in
                          [(div_open, "div_open"),
                           (div_close, "div_close"),
                           (pre_open, "pre_open")]
                          if c[0] != -1]
            if not candidates:
                break
            nearest = min(candidates, key=lambda c: c[0])
            np, kind = nearest

            if kind == "div_open":
                depth += 1
                pos = np + 1
            elif kind == "div_close":
                depth -= 1
                pos = np + len("</div>")
                if depth < 0:
                    # We exited the callout-algorithm <div>.
                    return None
            else:  # pre_open
                if pre_count == which:
                    pre_open_end = html.index(">", np) + 1
                    pre_close = html.index("</pre>", pre_open_end)
                    pre_close_end = pre_close + len("</pre>")
                    return (np, pre_open_end, pre_close, pre_close_end)
                pre_count += 1
                # Skip past the </pre>.
                pre_open_end = html.index(">", np) + 1
                pre_close = html.index("</pre>", pre_open_end)
                pos = pre_close + len("</pre>")

    return None


def find_inner_code(html: str, pre_open_end: int, pre_close: int) -> tuple[int, int] | None:
    """Inside pre[open..close], find the first <code ...>...</code>. Return
    (code_inner_start, code_inner_end) for the inner content.
    """
    seg = html[pre_open_end:pre_close]
    m = re.search(r'<code[^>]*>', seg)
    if not m:
        return None
    inner_start = pre_open_end + m.end()
    cm = seg.find("</code>", m.end())
    if cm == -1:
        return None
    inner_end = pre_open_end + cm
    return inner_start, inner_end


# --------------------------------------------------------------------------- #
# T1: pyg-text-bad -> algo-helper
# --------------------------------------------------------------------------- #


T1_TARGETS = [
    ("part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html", "26.1.1"),
    ("part-8-evaluation-production/module-35-production-engineering/section-35.3.html", "34.3.1"),
    ("part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.8.html", "35.8.1"),
]


def t1_convert(html: str, title_marker: str) -> tuple[str, bool]:
    """Find the algo-text-bad <pre> in the algorithm callout matching
    title_marker and convert to algo-helper. Returns (new_html, changed)."""
    loc = find_algorithm_pre_block(html, title_marker)
    if not loc:
        return html, False
    pre_open_start, pre_open_end, pre_close, pre_close_end = loc
    # Read the <pre ...> tag and <code ...> tag.
    pre_open_html = html[pre_open_start:pre_open_end]
    code_loc = find_inner_code(html, pre_open_end, pre_close)
    if not code_loc:
        return html, False
    code_inner_start, code_inner_end = code_loc

    # Get the existing <code ...> tag itself (between pre_open_end and code_inner_start).
    code_tag_html = html[pre_open_end:code_inner_start]
    code_class_m = re.search(r'class="([^"]*)"', code_tag_html)
    code_class = code_class_m.group(1) if code_class_m else ""
    if "language-none" in code_class:
        return html, False  # already algo-helper, idempotent
    if "lang-text" not in code_class:
        return html, False  # not the target

    inner_text_html = html[code_inner_start:code_inner_end]
    # Strip any existing pygments spans by collapsing tags via regex.
    # pyg-text-bad blocks are typically plain text already (no spans), but
    # be defensive.
    inner_plain = re.sub(r"<[^>]+>", "", inner_text_html)
    # Decode common HTML entities that the original Pygments output may have
    # introduced (left as-is in plain text we have via str.find).
    # We keep entities as-is; the new content stays as HTML.

    # Convert plain text to algo-helper.
    new_inner = []
    for line in inner_plain.split("\n"):
        rline = line.rstrip()
        # Detect trailing or full `//` comment.
        com_m = re.search(r"(\s*)(//.*)$", rline)
        comment_html = None
        body = rline
        if com_m:
            ws_before = com_m.group(1)
            comment = com_m.group(2)
            comment_html = f'{ws_before}<span class="algo-line-comment">{comment}</span>'
            body = rline[:com_m.start()].rstrip()
        # Wrap Input:/Output:/keyword.
        kw_m = re.match(r"^(\s*)(Input|Output):(.*)$", body)
        if kw_m:
            ind, label, rest = kw_m.group(1), kw_m.group(2), kw_m.group(3)
            body = f'{ind}<span class="algo-line-keyword">{label}:</span>{rest}'
        new_line = body + (comment_html if comment_html else "")
        new_inner.append(new_line)
    new_inner_html = "\n".join(new_inner)

    # Replace the <pre>..</pre> block.
    new_block = (f'<pre class=""><code class="language-none">{new_inner_html}'
                 f'\n</code></pre>')
    return html[:pre_open_start] + new_block + html[pre_close_end:], True


# --------------------------------------------------------------------------- #
# T2: # Input / # Output for pyg-python pseudocode
# --------------------------------------------------------------------------- #


T2_TARGETS = [
    (
        "part-1-foundations/module-04-transformer-architecture/section-4.4.html",
        "4.4.6",
        "queries Q, keys K, values V (each shape [N, d]), block sizes Br x Bc tuned to SRAM",
        "attention output O = softmax(QK^T / sqrt(d)) V (shape [N, d]) without materializing the full N x N attention matrix in HBM",
    ),
    (
        "part-1-foundations/module-05-decoding-text-generation/section-5.1.html",
        "5.1.2",
        "model, input_ids (start tokens), beam_width, max_new_tokens, optional eos_token_id, length_penalty",
        "top-scoring sequence(s) after length-normalized beam search",
    ),
    (
        "part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html",
        "8.3.3",
        "problem, easy_model (small/fast), hard_model (large/expensive), reward_model, difficulty_threshold",
        "best response selected from N candidates under the compute-optimal strategy",
    ),
    (
        "part-2-understanding-llms/module-10-inference-optimization/section-10.2.html",
        "vLLM's Block Table",
        "logical KV-cache blocks per sequence, physical block pool, page size",
        "block-table mapping logical to physical blocks with copy-on-write for shared prefixes",
    ),
    (
        "part-2-understanding-llms/module-10-inference-optimization/section-10.3.html",
        "Draft-Verify Loop",
        "target model, draft model (smaller), token sequence ids, draft length gamma",
        "accepted tokens (1 to gamma+1 each step) under speculative decoding's verification rule",
    ),
    (
        "part-4-training-adapting/module-19-peft/section-19.1.html",
        "LoRA Backward Pass",
        "frozen base weights W0 (d_in x d_out), trainable LoRA factors A (d_in x rank), B (rank x d_out), scaling alpha",
        "output y = x @ (W0 + (alpha/rank) * A @ B); gradients flow only through A and B",
    ),
    (
        "part-8-evaluation-production/module-34-evaluation-observability/section-34.1.html",
        "Position Bias in LLM-as-Judge",
        "judge LLM, question, candidate answers a and b",
        "winner ('a wins', 'b wins', 'tie / unreliable') after running the judge on both orderings",
    ),
    (
        "part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html",
        "Toxicity Disparity Scoring",
        "model under test, demographic groups G, prompt template T(group), per-group sample size N",
        "per-group mean toxicity and pairwise disparities, flagging groups with disproportionately toxic continuations",
    ),
]


def t2_inject(html: str, title_marker: str,
              in_desc: str, out_desc: str) -> tuple[str, bool]:
    loc = find_algorithm_pre_block(html, title_marker)
    if not loc:
        return html, False
    pre_open_start, pre_open_end, pre_close, pre_close_end = loc
    code_loc = find_inner_code(html, pre_open_end, pre_close)
    if not code_loc:
        return html, False
    code_inner_start, code_inner_end = code_loc

    # Read code class to verify it's lang-python.
    code_tag_html = html[pre_open_end:code_inner_start]
    if "lang-python" not in code_tag_html:
        return html, False

    inner = html[code_inner_start:code_inner_end]
    # Idempotence: skip if either "# Input:" or "# Output:" already at top.
    head_plain = re.sub(r"<[^>]+>", "", inner)[:300]
    if "# Input:" in head_plain and "# Output:" in head_plain:
        return html, False
    if re.match(r"^\s*Input:", head_plain) or re.match(r"^\s*Output:", head_plain):
        return html, False

    inject = (
        f'<span class="c1"># Input: {in_desc}</span>\n'
        f'<span class="c1"># Output: {out_desc}</span>\n'
    )
    new_html = (html[:code_inner_start] + inject + inner +
                html[code_inner_end:])
    return new_html, True


# --------------------------------------------------------------------------- #
# T3: RLVR renumber
# --------------------------------------------------------------------------- #


T3_RLVR_FILE = "part-2-understanding-llms/module-09-reasoning-test-time-compute/section-9.3.html"
T3_RLVR_LABEL = "9.3.4"

T3_RLVR_NEW_PRE = (
    '<pre class=""><code class="language-none">'
    '<span class="algo-line-keyword">Input:</span> policy model pi, problem dataset D, verifier V, num_iterations T\n'
    '<span class="algo-line-keyword">Output:</span> trained policy pi*\n'
    '\n'
    '1. for iteration = 1 to T:\n'
    '  a. Sample a batch of problems {p_1, ..., p_B} from D\n'
    '  b. for each problem p_i:\n'
    '    Generate solution s_i (reasoning trace + final answer) using pi\n'
    '  c. for each solution s_i:\n'
    '    r_i = V(s_i, ground_truth_i) <span class="algo-line-comment">// automatic verification</span>\n'
    '    <span class="algo-line-comment">// e.g., r_i = 1 if answer matches, 0 otherwise</span>\n'
    '  d. Optionally add format rewards (e.g., +0.1 for using &lt;think&gt; tags)\n'
    '  e. Update pi using policy optimizer (PPO or GRPO) to maximize\n'
    '    expected reward while staying close to reference policy\n'
    '2. return pi* (the final policy)\n'
    '</code></pre>'
)


def t3_renumber_rlvr(html: str) -> tuple[str, bool]:
    loc = find_algorithm_pre_block(html, T3_RLVR_LABEL, which=0)
    if not loc:
        return html, False
    pre_open_start, pre_open_end, pre_close, pre_close_end = loc
    code_loc = find_inner_code(html, pre_open_end, pre_close)
    if not code_loc:
        return html, False
    code_inner_start, code_inner_end = code_loc
    code_tag_html = html[pre_open_end:code_inner_start]
    # If already language-none, skip (idempotent).
    if "language-none" in code_tag_html:
        return html, False
    if "lang-python" not in code_tag_html:
        return html, False
    return (html[:pre_open_start] + T3_RLVR_NEW_PRE + html[pre_close_end:],
            True)


# --------------------------------------------------------------------------- #
# T4: 2-space indent standardization
# --------------------------------------------------------------------------- #


T4_TARGETS = [
    ("part-4-training-adapting/module-20-alignment-rlhf-dpo/section-20.1.html", "19.1.3"),
    ("part-6-agentic-ai/module-26-ai-agents/section-26.1.html", "26.1.2"),
    ("part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html", "26.1.1"),
    ("part-8-evaluation-production/module-35-production-engineering/section-35.3.html", "34.3.1"),
    ("part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.8.html", "35.8.1"),
]


def t4_widen(html: str, title_marker: str) -> tuple[str, int]:
    """Find the first <pre>...</pre> in the matching algorithm callout. For
    each line of the inner content that starts with exactly 1 leading space
    (a 1-space indent of a sub-step), widen to 2 spaces. Lines with 3 spaces
    widen to 4 (preserve relative depth). Idempotent."""
    loc = find_algorithm_pre_block(html, title_marker, which=0)
    if not loc:
        return html, 0
    pre_open_start, pre_open_end, pre_close, pre_close_end = loc
    code_loc = find_inner_code(html, pre_open_end, pre_close)
    if not code_loc:
        return html, 0
    code_inner_start, code_inner_end = code_loc
    # Only modify algo-helper or lang-text inner content (pseudocode), not
    # lang-python (real Python).
    code_tag_html = html[pre_open_end:code_inner_start]
    if "lang-python" in code_tag_html:
        return html, 0

    inner = html[code_inner_start:code_inner_end]
    new_lines = []
    changed = 0
    for line in inner.split("\n"):
        n_leading = len(line) - len(line.lstrip(" "))
        if n_leading == 1:
            new_lines.append(" " + line)
            changed += 1
        elif n_leading == 3:
            new_lines.append(" " + line)
            changed += 1
        else:
            new_lines.append(line)
    if changed == 0:
        return html, 0
    new_inner = "\n".join(new_lines)
    return (html[:code_inner_start] + new_inner + html[code_inner_end:],
            changed)


# --------------------------------------------------------------------------- #
# T5: phase-separator blank lines in dense pyg-python blocks
# --------------------------------------------------------------------------- #


T5_TARGETS = [
    ("part-1-foundations/module-04-transformer-architecture/section-4.4.html", "4.4.6"),
    ("part-1-foundations/module-05-decoding-text-generation/section-5.1.html", "5.1.2"),
    ("part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html", "8.3.3"),
    ("part-2-understanding-llms/module-10-inference-optimization/section-10.3.html", "Draft-Verify Loop"),
    ("part-9-safety-security-ethics/module-37-safety-ethics-regulation/section-37.3.html", "Toxicity"),
]


# Detect a line whose RENDERED text (after stripping HTML spans) starts at
# column 0 with `def `, `class `, or `@`. We use a per-line regex check.

DEF_LINE_RE = re.compile(
    r'^(<span class="(?:k|kn|nd)">(?:def|class|@\w*)</span>'
    r'|<span class="o">@</span>'
    r'|<span class="nd">@)'
)


def line_renders_to_top_level_def(line_html: str) -> bool:
    """Strip leading HTML, then check if the rendered text starts with `def `,
    `class `, or `@` at column 0."""
    # The Pygments-highlighted format wraps every token in a span. The very
    # first character of the rendered text is the first character inside the
    # first span after any leading whitespace.
    # We strip all tags and check the first non-empty chars.
    plain = re.sub(r"<[^>]+>", "", line_html)
    if not plain:
        return False
    # Top-level: no leading whitespace.
    if plain[:1] in (" ", "\t"):
        return False
    return (plain.startswith("def ") or plain.startswith("class ") or
            plain.startswith("@"))


def line_is_blank(line_html: str) -> bool:
    return re.sub(r"<[^>]+>", "", line_html).strip() == ""


def line_is_comment(line_html: str) -> bool:
    plain = re.sub(r"<[^>]+>", "", line_html).strip()
    return plain.startswith("#")


def t5_phase_separators(html: str, title_marker: str) -> tuple[str, int]:
    loc = find_algorithm_pre_block(html, title_marker, which=0)
    if not loc:
        return html, 0
    pre_open_start, pre_open_end, pre_close, pre_close_end = loc
    code_loc = find_inner_code(html, pre_open_end, pre_close)
    if not code_loc:
        return html, 0
    code_inner_start, code_inner_end = code_loc
    code_tag_html = html[pre_open_end:code_inner_start]
    if "lang-python" not in code_tag_html:
        return html, 0

    inner = html[code_inner_start:code_inner_end]
    lines = inner.split("\n")
    out: list[str] = []
    inserts = 0
    for i, line in enumerate(lines):
        if i > 0 and line_renders_to_top_level_def(line):
            prev = out[-1] if out else ""
            if not line_is_blank(prev) and not line_is_comment(prev):
                out.append("")
                inserts += 1
        out.append(line)
    if inserts == 0:
        return html, 0
    new_inner = "\n".join(out)
    return (html[:code_inner_start] + new_inner + html[code_inner_end:],
            inserts)


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #


def extract_pyg_python_source_inner(html: str, title_marker: str,
                                    which: int = 0) -> str | None:
    """Extract the plain Python source from a pyg-python <code> block (drop
    all HTML tags, decode common entities)."""
    loc = find_algorithm_pre_block(html, title_marker, which=which)
    if not loc:
        return None
    pre_open_start, pre_open_end, pre_close, pre_close_end = loc
    code_loc = find_inner_code(html, pre_open_end, pre_close)
    if not code_loc:
        return None
    code_inner_start, code_inner_end = code_loc
    code_tag_html = html[pre_open_end:code_inner_start]
    if "lang-python" not in code_tag_html:
        return None
    inner = html[code_inner_start:code_inner_end]
    plain = re.sub(r"<[^>]+>", "", inner)
    plain = (plain.replace("&lt;", "<")
                  .replace("&gt;", ">")
                  .replace("&amp;", "&")
                  .replace("&quot;", '"')
                  .replace("&#39;", "'"))
    return plain


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #


@dataclass
class FileChange:
    relpath: str
    actions: list[str] = field(default_factory=list)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    file_cache: dict[str, str] = {}
    pre_existing_ast_err: dict[tuple[str, str], str | None] = {}
    actions_by_file: dict[str, list[str]] = {}

    def load(relpath: str) -> str:
        if relpath not in file_cache:
            file_cache[relpath] = (PROJECT_ROOT / relpath).read_text(
                encoding="utf-8", errors="replace")
        return file_cache[relpath]

    def store(relpath: str, html: str) -> None:
        file_cache[relpath] = html

    def record(relpath: str, action: str) -> None:
        actions_by_file.setdefault(relpath, []).append(action)

    # Snapshot pre-existing AST status for python pseudocode blocks so we don't
    # blame ourselves for prior breakage.
    def snapshot_ast(relpath: str, marker: str) -> None:
        html = load(relpath)
        src = extract_pyg_python_source_inner(html, marker, which=0)
        if src is None:
            pre_existing_ast_err[(relpath, marker)] = None
            return
        try:
            ast.parse(src)
            pre_existing_ast_err[(relpath, marker)] = None
        except SyntaxError as e:
            pre_existing_ast_err[(relpath, marker)] = str(e)

    def normalize_err(msg: str | None) -> str | None:
        if msg is None:
            return None
        # Drop line numbers so we can compare "before vs after" robustly.
        return re.sub(r"line \d+", "line N", msg)

    def check_ast_regression(relpath: str, marker: str) -> None:
        html = load(relpath)
        src = extract_pyg_python_source_inner(html, marker, which=0)
        if src is None:
            return
        try:
            ast.parse(src)
        except SyntaxError as e:
            prev = normalize_err(pre_existing_ast_err.get((relpath, marker)))
            now = normalize_err(str(e))
            if prev is None or prev != now:
                print(f"[!] AST regression in {relpath} ({marker}): {e}",
                      file=sys.stderr)

    # Snapshot AST for every target that has a pyg-python block.
    for relpath, marker, *_ in T2_TARGETS:
        snapshot_ast(relpath, marker)
    for relpath, marker in T5_TARGETS:
        snapshot_ast(relpath, marker)

    # ---- T1 ----
    for relpath, marker in T1_TARGETS:
        html = load(relpath)
        new_html, changed = t1_convert(html, marker)
        if changed:
            store(relpath, new_html)
            record(relpath, f"T1[algo-helper:{marker}]")

    # ---- T2 ----
    for relpath, marker, in_desc, out_desc in T2_TARGETS:
        html = load(relpath)
        new_html, changed = t2_inject(html, marker, in_desc, out_desc)
        if changed:
            store(relpath, new_html)
            record(relpath, f"T2[io:{marker}]")
            check_ast_regression(relpath, marker)

    # ---- T3 ----
    html = load(T3_RLVR_FILE)
    new_html, changed = t3_renumber_rlvr(html)
    if changed:
        store(T3_RLVR_FILE, new_html)
        record(T3_RLVR_FILE, f"T3[rlvr-renumber]")

    # ---- T4 ----
    for relpath, marker in T4_TARGETS:
        html = load(relpath)
        new_html, n = t4_widen(html, marker)
        if n > 0:
            store(relpath, new_html)
            record(relpath, f"T4[indent:{marker}:{n}lines]")

    # ---- T5 ----
    for relpath, marker in T5_TARGETS:
        html = load(relpath)
        new_html, n = t5_phase_separators(html, marker)
        if n > 0:
            store(relpath, new_html)
            record(relpath, f"T5[phase:{marker}:{n}inserts]")
            check_ast_regression(relpath, marker)

    # ---- Write ----
    if args.apply:
        for relpath, html in file_cache.items():
            if relpath in actions_by_file:
                (PROJECT_ROOT / relpath).write_text(html, encoding="utf-8")

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] Files changed: {len(actions_by_file)}")
    print()
    for relpath in sorted(actions_by_file):
        print(f"  {relpath}")
        for a in actions_by_file[relpath]:
            print(f"    {a}")
    print()
    total = sum(len(v) for v in actions_by_file.values())
    print(f"Total actions: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
