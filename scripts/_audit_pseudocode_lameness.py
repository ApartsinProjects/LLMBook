"""
Audit pseudocode / algorithm blocks for lameness across the LLMBook.

A "lame" pseudocode block is one that adds no pedagogical value: trivial
INPUT/OUTPUT/FOR-LOOP narration the prose already says in one sentence,
or placeholder operators (do_thing(), process(x)) without conveying any
non-obvious algorithm.

Scope: every captioned `Pseudocode N.N.N` block, every captioned
`Algorithm N.N.N` block, plus every `<div class="callout algorithm">`
block (regardless of title format, so we catch "Under the Hood:" and
"Algorithm: Foo" titles too).

For each block we compute 6 binary signals (0/1). Threshold for flagging
is score >= 2. Recurrences, invariants, complexity claims and named
data structures dispel the lameness signals (overrides applied at the
end).

Signals:
  1. tiny_three_lines       -- <= 3 non-blank lines, no control structure.
  2. placeholder_identifiers -- body dominated by do_X / process / step.
  3. trivial_sequential     -- "Step 1: ... Step 2: ... Step 3: ..." prose.
  4. no_control_flow        -- linear list, no branch/loop/return.
  5. no_algorithmic_insight -- no recurrence, no invariant, no complexity,
                                no real data structure.
  6. wrapper_or_config      -- caption claims algorithm but body is
                                YAML / JSON / dict literal / settings.

Suggestion logic produces:
  - verdict: drop / improve / keep-but-tighten
  - improvement path (rewrite / drop-merge / upgrade-to-Code-Fragment)
  - effort estimate (XS / S / M / L)
  - reason for verdict

READ-ONLY. Writes only the audit Markdown to
E:/Projects/BookBlogsHome/LLMBook/pseudocode-lameness-audit.md.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, NavigableString

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
REPORT_PATH = ROOT / "pseudocode-lameness-audit.md"

EXCLUDE_DIRS = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind",
    "templates", ".git", ".html2pub_cache", ".github",
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


LABEL_RE = re.compile(
    r"(Pseudocode|Algorithm)\s+([A-Za-z]?[\d]+(?:\.\d+)*)",
    re.IGNORECASE,
)


def line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def classify_label(text: str) -> Optional[str]:
    m = LABEL_RE.search(text)
    if not m:
        return None
    tag = m.group(1).lower()
    return "pseudocode" if "pseudo" in tag else "algorithm"


def label_number(text: str) -> Optional[str]:
    m = LABEL_RE.search(text)
    if not m:
        return None
    return m.group(2)


# ---------- Block extraction ----------

@dataclass
class PseudoBlock:
    file: Path
    line: int
    label_kind: str          # "pseudocode" / "algorithm" / "untitled-algorithm"
    label_text: str
    label_number: str
    code_text: str
    code_lang: Optional[str]
    caption_text: str
    source: str              # "code-caption" / "callout-algorithm" / "callout-untitled"


def find_codeblock_for_caption(caption_div):
    """For a <div class=code-caption>, find the related <pre>."""
    def sibling_iter(node, direction):
        sib = (
            node.previous_sibling if direction == "prev"
            else node.next_sibling
        )
        while sib is not None:
            if isinstance(sib, NavigableString):
                if sib.strip() == "":
                    sib = (
                        sib.previous_sibling if direction == "prev"
                        else sib.next_sibling
                    )
                    continue
                return None
            return sib
        return None

    for direction in ("prev", "next"):
        node = sibling_iter(caption_div, direction)
        if node is None:
            continue
        if getattr(node, "name", None) == "pre":
            return node
        pre = node.find("pre") if hasattr(node, "find") else None
        if pre is not None:
            return pre

    parent = caption_div.parent
    if parent is not None:
        pre = parent.find("pre")
        if pre is not None:
            return pre
    return None


def get_lang(node) -> Optional[str]:
    classes = node.get("class") or []
    for c in classes:
        if c.startswith("lang-"):
            return c[len("lang-"):]
    return None


def extract_blocks_from_file(
    path: Path, raw_html: str
) -> list[PseudoBlock]:
    soup = BeautifulSoup(raw_html, "html.parser")
    out: list[PseudoBlock] = []
    seen_pre_ids: set[int] = set()

    # ---- code-caption form ----
    for cap in soup.find_all("div", class_="code-caption"):
        text = cap.get_text(" ", strip=True)
        kind = classify_label(text)
        if kind is None:
            continue
        pre = find_codeblock_for_caption(cap)
        if pre is None:
            continue
        seen_pre_ids.add(id(pre))
        code = pre.find("code") or pre
        code_text = code.get_text()
        lang = (
            get_lang(code) if code.name == "code" else get_lang(pre)
        )
        try:
            offset = raw_html.index(str(cap))
        except ValueError:
            offset = 0
        line = line_of_offset(raw_html, offset)
        out.append(PseudoBlock(
            file=path, line=line,
            label_kind=kind,
            label_text=text[:200],
            label_number=label_number(text) or "",
            code_text=code_text,
            code_lang=lang,
            caption_text=text,
            source="code-caption",
        ))

    # ---- callout-algorithm (any title format) ----
    for callout in soup.find_all("div", class_="callout"):
        classes = callout.get("class", []) or []
        if "algorithm" not in classes:
            continue
        pre = callout.find("pre")
        if pre is None:
            continue
        if id(pre) in seen_pre_ids:
            continue
        seen_pre_ids.add(id(pre))
        title = callout.find("div", class_="callout-title")
        title_text = title.get_text(" ", strip=True) if title else ""
        kind = classify_label(title_text) or "untitled-algorithm"
        code = pre.find("code") or pre
        code_text = code.get_text()
        lang = (
            get_lang(code) if code.name == "code" else get_lang(pre)
        )
        try:
            offset = raw_html.index(
                str(title) if title else str(callout)
            )
        except ValueError:
            offset = 0
        line = line_of_offset(raw_html, offset)
        out.append(PseudoBlock(
            file=path, line=line,
            label_kind=kind,
            label_text=(title_text or "(no title)")[:200],
            label_number=label_number(title_text) or "",
            code_text=code_text,
            code_lang=lang,
            caption_text=title_text,
            source=(
                "callout-algorithm"
                if kind in ("pseudocode", "algorithm")
                else "callout-untitled"
            ),
        ))

    return out


# ---------- Signal detectors ----------

PLACEHOLDER_TOKENS = {
    "do_x", "do_y", "do_z", "do_thing", "do_step", "do_action",
    "process", "process_x", "process_data", "process_input",
    "compute", "compute_x", "compute_step",
    "step", "step1", "step2", "step3",
    "foo", "bar", "baz", "qux",
    "thing", "stuff",
    "func", "func1", "func2",
}

PLACEHOLDER_CALL_RE = re.compile(
    r"\b(?:do_thing|do_step|do_x|do_y|do_z|do_action|"
    r"process_data|process_input|"
    r"compute_step|foo|bar|baz|func\d?)\s*\(",
    re.IGNORECASE,
)

# Control-flow tokens for non-blank-line scan.
CONTROL_FLOW_PATTERNS = [
    re.compile(r"\bfor\b", re.I),
    re.compile(r"\bwhile\b", re.I),
    re.compile(r"\bif\b", re.I),
    re.compile(r"\belse\b", re.I),
    re.compile(r"\belif\b", re.I),
    re.compile(r"\breturn\b", re.I),
    re.compile(r"\byield\b", re.I),
    re.compile(r"\bbreak\b", re.I),
    re.compile(r"\bcontinue\b", re.I),
    re.compile(r"\braise\b", re.I),
    re.compile(r"\bforeach\b", re.I),
    re.compile(r"\brepeat\b", re.I),
    re.compile(r"\buntil\b", re.I),
]

# Recurrences: dp[i] = f(dp[i-1], ...), score[t] = score[t-1] + r, etc.
RECURRENCE_RE = re.compile(
    r"\b[A-Za-z_]\w{0,8}\s*\[\s*[A-Za-z0-9_+\-]+\s*\]\s*"
    r"(?:=|:=|\\u2190|←)",
)

INVARIANT_RE = re.compile(
    r"\b(invariant|loop\s+invariant|precondition|postcondition|"
    r"maintains?|preserve[sd]?)\b",
    re.IGNORECASE,
)
COMPLEXITY_RE = re.compile(
    r"\b(O\([^\)]{1,30}\)|complexity|"
    r"time\s+complexity|space\s+complexity|"
    r"asymptotic|amortized)\b",
    re.IGNORECASE,
)
DATA_STRUCT_TOKENS = (
    "heap", "priority queue", "queue", "stack", "trie", "graph",
    "tree", "deque", "hash table", "hash set", "hash map",
    "lookup table", "kv cache", "kv-cache", "block table",
    "page table", "ring buffer", "lru", "skip list",
    "linked list", "btree", "b-tree", "bloom filter",
    "minhash", "lsh", "hnsw layer", "hnsw graph",
    "transition matrix", "advantage estimator",
    "log-prob",  # signal for likelihood-aware algorithms
)
# Substantive operator tokens that imply real algorithmic content.
SUBSTANTIVE_OPS = (
    "argmax", "argmin", "softmax", "logsumexp",
    "clip(", "min(", "max(",
    "exp(", "log(", "sqrt(",
    "norm", "kl(", "kl_divergence",
    "expected reward", "advantage", "gae",
    "gradient", "backward", "forward pass",
    "policy update", "value update",
    "discount", "bellman",
    "embedding", "vector similarity", "cosine",
    "ratio * a", "clipped surrogate",
    "sample with replacement", "resample",
    "percentile",
    "refill", "token bucket", "leaky bucket",
    "draft", "verify", "speculative",
    "tile", "block", "sram",
    "rebuttal", "verdict", "nash equilibrium",
)

NUMBERED_STEP_RE = re.compile(
    r"^\s*(?:Step\s*)?(\d+|[a-z]|[ivx]+)\s*[.:]\s+[A-Z]",
    re.MULTILINE,
)
ASSIGNMENT_ARROW_RE = re.compile(r"←|\\u2190|:=|<-")


def non_blank_lines(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if ln.strip()]


def strip_code_comments(text: str) -> str:
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("#") or s.startswith("//"):
            continue
        if "#" in ln and not ln.strip().startswith("#"):
            ln = ln[: ln.index("#")]
        out.append(ln)
    return "\n".join(out)


def has_control_flow(text: str) -> bool:
    body = strip_code_comments(text)
    return any(p.search(body) for p in CONTROL_FLOW_PATTERNS)


def has_substantive_op(text: str) -> bool:
    """True if the body mentions a substantive operator name."""
    low = text.lower()
    return any(op in low for op in SUBSTANTIVE_OPS)


def has_real_data_structure(text: str) -> bool:
    body = text.lower()
    return any(d in body for d in DATA_STRUCT_TOKENS)


def looks_like_recurrence(text: str) -> bool:
    return RECURRENCE_RE.search(text) is not None


def has_invariant(text: str) -> bool:
    return INVARIANT_RE.search(text) is not None


def has_complexity_line(text: str) -> bool:
    return COMPLEXITY_RE.search(text) is not None


def numbered_step_count(text: str) -> int:
    return sum(1 for _ in NUMBERED_STEP_RE.finditer(text))


def placeholder_density(text: str) -> tuple[int, int]:
    body = strip_code_comments(text)
    idents = re.findall(r"\b[a-z_][a-z0-9_]*\b", body)
    if not idents:
        return 0, 0
    hits = sum(1 for i in idents if i in PLACEHOLDER_TOKENS)
    return hits, len(idents)


def looks_like_wrapper(text: str, lang: Optional[str]) -> bool:
    """Body is a config / dict / YAML wrapper, not an algorithm."""
    body = text.strip()
    if not body:
        return True
    if lang and lang.lower() in {"yaml", "yml", "json", "toml", "ini"}:
        return True
    lines = non_blank_lines(body)
    if len(lines) >= 2:
        kv_pat = re.compile(r"^\s*[A-Za-z_][\w\-]*\s*[:=]\s*\S")
        kv_count = sum(1 for ln in lines if kv_pat.match(ln))
        if (
            kv_count >= len(lines) * 0.8
            and not any("(" in ln for ln in lines)
            and not any("←" in ln or ":=" in ln for ln in lines)
        ):
            return True
    if body.startswith("{") and body.endswith("}") and len(lines) <= 5:
        return True
    return False


def trivial_sequential(text: str) -> bool:
    """Many numbered steps but no logical structure beyond linear order.

    Detect by: >=3 numbered step starts, AND none of:
      - assignment arrow / dataflow into an indexed structure
      - clear branch with else
      - substantive operator name
    """
    n = numbered_step_count(text)
    if n < 3:
        return False
    if looks_like_recurrence(text):
        return False
    body_low = text.lower()
    # Branches with conditional behavior keep the block useful.
    has_real_branch = (
        re.search(r"^\s*\d+\.[^:]*\bif\b", text, re.M | re.I) is not None
        or re.search(r"^\s*[a-z]\.[^:]*\bif\b", text, re.M | re.I) is not None
    )
    if has_real_branch and has_substantive_op(text):
        return False
    # If body has substantive math/operator names AND has loops, also keep.
    if has_substantive_op(text) and has_control_flow(text):
        return False
    return True


def is_pure_narration(text: str) -> bool:
    """Sequential 'Step N: do X' with no math, no operator, no DS."""
    n = numbered_step_count(text)
    if n < 3:
        return False
    if has_substantive_op(text):
        return False
    if has_real_data_structure(text):
        return False
    if looks_like_recurrence(text):
        return False
    return True


# ---------- Suggestion logic ----------

@dataclass
class Finding:
    block: PseudoBlock
    signals: dict = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    @property
    def score(self) -> int:
        return sum(1 for v in self.signals.values() if v)

    @property
    def active_signals(self) -> list[str]:
        return [k for k, v in self.signals.items() if v]


def suggest_improvement(f: Finding) -> tuple[str, str, str, str]:
    """Return (verdict, path, effort, reason)."""
    b = f.block
    body = b.code_text
    nlines = len(non_blank_lines(body))
    sig = f.signals
    score = f.score

    # Wrapper / config: drop.
    if sig.get("wrapper_or_config"):
        return (
            "drop",
            "drop block; move config to surrounding prose, or convert to a runnable Code Fragment",
            "XS",
            "caption promises an algorithm but body is config / dict / YAML wrapper",
        )

    # Pure placeholder, no real ops: drop.
    if sig.get("placeholder_identifiers") and nlines <= 5:
        return (
            "drop",
            "drop and merge into the prose paragraph above",
            "XS",
            "body is dominated by placeholder names (do_X, process, foo); prose already says the steps",
        )

    # Trivial sequential / pure narration: drop.
    if sig.get("trivial_sequential"):
        return (
            "drop",
            "drop block; rewrite the prose to say 'The pipeline does A, then B, then C.'",
            "XS",
            "numbered 'Step 1 / Step 2 / Step 3' narration with no branching, math, or data structures",
        )

    # Tiny + no control flow + no insight: drop.
    if (
        sig.get("tiny_three_lines")
        and sig.get("no_control_flow")
        and sig.get("no_algorithmic_insight")
    ):
        return (
            "drop",
            "drop block; merge into prose",
            "XS",
            "<=3 lines, no branch, no loop, no recurrence; prose can carry it",
        )

    # Has structure but no insight: improve.
    if sig.get("no_algorithmic_insight") and sig.get("no_control_flow"):
        return (
            "improve",
            "rewrite to show a recurrence / invariant / complexity claim, OR upgrade to a Code Fragment importing a real library",
            "S",
            "block has scaffolding but no recurrence, invariant, complexity, or named data structure to teach",
        )

    if sig.get("no_algorithmic_insight"):
        return (
            "improve",
            "add a recurrence, invariant, or complexity line; name the data structures used",
            "S",
            "has control flow but no concrete algorithmic content to teach",
        )

    if score == 2:
        return (
            "keep-but-tighten",
            "tighten by stating the invariant, complexity, or named data structure explicitly",
            "S",
            "borderline lameness; one or two lines would lift pedagogical value",
        )

    return (
        "improve",
        "rewrite to surface a recurrence, invariant, or data-structure operation",
        "M",
        "multiple lameness signals but block has enough scaffolding to rescue",
    )


# ---------- Audit ----------

def compute_signals(b: PseudoBlock) -> Finding:
    signals: dict[str, bool] = {}
    notes: list[str] = []
    body = b.code_text
    lines = non_blank_lines(body)
    nlines = len(lines)

    # 1: tiny three lines (must also be flat: no def/class/for/while/if)
    tiny = (
        nlines <= 3
        and not any(
            re.search(r"^\s*(def|class|for|while|if|@)", ln)
            for ln in lines
        )
    )
    signals["tiny_three_lines"] = bool(tiny)

    # 2: placeholder identifiers
    hits, total = placeholder_density(body)
    placeholder = (
        (total > 0 and hits / max(1, total) >= 0.30 and hits >= 3)
        or bool(PLACEHOLDER_CALL_RE.search(body))
    )
    signals["placeholder_identifiers"] = bool(placeholder)
    if placeholder:
        notes.append(f"placeholder ident hits={hits}/{total}")

    # 3: trivial sequential narration (or pure narration even if "for each" appears)
    signals["trivial_sequential"] = bool(
        trivial_sequential(body) or is_pure_narration(body)
    )

    # 4: no control flow
    signals["no_control_flow"] = not has_control_flow(body)

    # 5: no algorithmic insight
    insight = (
        looks_like_recurrence(body)
        or has_invariant(body) or has_invariant(b.caption_text)
        or has_complexity_line(body)
        or has_complexity_line(b.caption_text)
        or has_real_data_structure(body)
        or has_real_data_structure(b.caption_text)
        or has_substantive_op(body)
    )
    signals["no_algorithmic_insight"] = not insight

    # 6: wrapper or config
    signals["wrapper_or_config"] = looks_like_wrapper(body, b.code_lang)

    # Overrides: if recurrence/invariant/complexity present, reset
    # the soft signals (the block is teaching something).
    if (
        looks_like_recurrence(body)
        or has_invariant(body) or has_invariant(b.caption_text)
        or has_complexity_line(body) or has_complexity_line(b.caption_text)
    ):
        for k in (
            "trivial_sequential", "no_algorithmic_insight",
            "wrapper_or_config",
        ):
            signals[k] = False

    return Finding(block=b, signals=signals, notes=notes)


def audit() -> dict:
    files = iter_html_files()
    blocks: list[PseudoBlock] = []
    for f in files:
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if (
            "code-caption" not in raw
            and "callout-title" not in raw
            and "callout algorithm" not in raw
        ):
            continue
        blocks.extend(extract_blocks_from_file(f, raw))

    findings = [compute_signals(b) for b in blocks]
    flagged = [f for f in findings if f.score >= 2]
    return {
        "files_scanned": len(files),
        "blocks_total": len(blocks),
        "by_label": Counter(b.label_kind for b in blocks),
        "by_source": Counter(b.source for b in blocks),
        "findings": findings,
        "flagged": flagged,
    }


# ---------- Report ----------

def code_preview(text: str, n: int = 6) -> str:
    lines = non_blank_lines(text)
    return "\n".join(lines[:n])


def safe_caption(s: str, limit: int = 90) -> str:
    s = s.replace("\n", " ").strip()
    if len(s) > limit:
        s = s[: limit - 1] + "..."
    return s.replace("|", "/")


def write_report(result: dict) -> None:
    out: list[str] = []
    push = out.append

    push("# Pseudocode and Algorithm Block Lameness Audit")
    push("")
    push(
        "Audit scope: every captioned `Pseudocode N.N.N` or "
        "`Algorithm N.N.N` block, plus every "
        "`<div class=\"callout algorithm\">` block (any title), "
        "across the LLMBook HTML tree."
    )
    push("")
    push(
        "Goal: identify pseudocode boxes that add no pedagogical "
        "value: trivial INPUT/OUTPUT/FOR-LOOP narration, blocks whose "
        "body is just `do_thing()` / `process(x)` / numbered step "
        "lists, or wrapper / config blocks mislabeled as algorithm."
    )
    push("")
    push(
        "Script: `scripts/_audit_pseudocode_lameness.py` "
        "(Python 3.14, BeautifulSoup)."
    )
    push("")
    push("**Signals** (binary, 1 if present). Flag threshold: score >= 2.")
    push("")
    push(
        "1. `tiny_three_lines` -- 3 lines or fewer, no `def` / `class` / "
        "loop / branch."
    )
    push(
        "2. `placeholder_identifiers` -- body dominated by "
        "`do_X` / `process` / `foo` / `step1` calls."
    )
    push(
        "3. `trivial_sequential` -- 3+ numbered 'Step N: ...' lines, "
        "no branching, no math, no data structure."
    )
    push("4. `no_control_flow` -- no `for` / `while` / `if` / `return`.")
    push(
        "5. `no_algorithmic_insight` -- no recurrence, no invariant, "
        "no complexity claim, no named data structure, no substantive "
        "operator (`argmax`, `softmax`, `KL`, `clip`, `tile`, ...)."
    )
    push(
        "6. `wrapper_or_config` -- caption promises an algorithm but "
        "body is YAML / JSON / dict literal / setting object."
    )
    push("")
    push("**Overrides** (clear soft signals if present):")
    push("")
    push("- Recurrence detected (`dp[i] = ...`, `score[t] := ...`).")
    push("- Invariant / precondition / postcondition language.")
    push("- Complexity claim (`O(...)`, `time complexity`, etc.).")
    push("")
    push("**Exclusions** (NOT flagged even if signals would fire):")
    push("")
    push("- Blocks showing recurrences.")
    push("- Blocks with `invariant:` / `complexity:` line.")
    push(
        "- Multi-branch algorithms (beam search, MCTS, RL training step) "
        "where the structure carries the lesson."
    )
    push(
        "- FlashAttention / paged-attention / speculative-decoding "
        "access-pattern pseudocode."
    )
    push("")

    push("## 1. Summary")
    push("")
    push(f"- Files scanned: **{result['files_scanned']}**")
    push(f"- Pseudocode/algorithm blocks found: **{result['blocks_total']}**")
    push("")
    push("Blocks by label:")
    push("")
    push("| Label | Count |")
    push("|---|---|")
    for k, v in sorted(result["by_label"].items()):
        push(f"| {k} | {v} |")
    push("")
    push("Blocks by source:")
    push("")
    push("| Source | Count |")
    push("|---|---|")
    for k, v in sorted(result["by_source"].items()):
        push(f"| {k} | {v} |")
    push("")
    push(f"**Total flagged (score >= 2): {len(result['flagged'])}**")
    push("")

    sig_total = Counter()
    sig_flagged = Counter()
    for f in result["findings"]:
        for k, v in f.signals.items():
            if v:
                sig_total[k] += 1
                if f.score >= 2:
                    sig_flagged[k] += 1
    push("Signal frequencies (all blocks vs flagged blocks):")
    push("")
    push("| Signal | All | Flagged |")
    push("|---|---|---|")
    for k in (
        "tiny_three_lines",
        "placeholder_identifiers",
        "trivial_sequential",
        "no_control_flow",
        "no_algorithmic_insight",
        "wrapper_or_config",
    ):
        push(f"| {k} | {sig_total.get(k, 0)} | {sig_flagged.get(k, 0)} |")
    push("")

    flagged_sorted = sorted(
        result["flagged"],
        key=lambda f: (-f.score, rel(f.block.file), f.block.line),
    )

    push("## 2. Top 20 worst offenders")
    push("")
    if not flagged_sorted:
        push("_No blocks scored >= 2._")
    else:
        push(
            "| # | File:line | Caption | Score | Signals | Verdict | "
            "Effort |"
        )
        push("|---|---|---|---|---|---|---|")
        for i, f in enumerate(flagged_sorted[:20], start=1):
            b = f.block
            verdict, _p, effort, _r = suggest_improvement(f)
            sigs = ",".join(f.active_signals)
            push(
                f"| {i} | `{rel(b.file)}:{b.line}` | "
                f"{safe_caption(b.label_text, 55)} | "
                f"{f.score} | {sigs} | {verdict} | {effort} |"
            )
    push("")

    push("## 3. Detailed findings (all flagged blocks)")
    push("")
    if not flagged_sorted:
        push("_No flagged blocks._")
    for i, f in enumerate(flagged_sorted, start=1):
        b = f.block
        verdict, path, effort, reason = suggest_improvement(f)
        push(f"### {i}. {b.label_text}")
        push("")
        push(f"- File: `{rel(b.file)}:{b.line}`")
        push(f"- Source: `{b.source}`, lang=`{b.code_lang}`")
        push(
            f"- Score: **{f.score}** -- signals: "
            f"{', '.join(f.active_signals)}"
        )
        push(
            f"- Verdict: **{verdict}** ({effort}) -- {reason}"
        )
        push(f"- Improvement path: {path}")
        if f.notes:
            push(f"- Notes: {'; '.join(f.notes)}")
        push("")
        push("Body (first 6 non-blank lines):")
        push("")
        push("```")
        push(code_preview(b.code_text, 6))
        push("```")
        push("")

    push("## 4. Quick-drop list (low value, prose covers them)")
    push("")
    quick_drops = [
        f for f in flagged_sorted
        if suggest_improvement(f)[0] == "drop"
    ]
    if not quick_drops:
        push("_None._")
    else:
        push(
            "These blocks contain no algorithmic insight that the "
            "surrounding prose does not already carry. Recommended "
            "action: delete the block, ensure the prose paragraph "
            "above states the steps in plain English, and renumber "
            "subsequent labels."
        )
        push("")
        push("| File:line | Caption | Reason |")
        push("|---|---|---|")
        for f in quick_drops:
            b = f.block
            _v, _p, _e, reason = suggest_improvement(f)
            push(
                f"| `{rel(b.file)}:{b.line}` | "
                f"{safe_caption(b.label_text, 70)} | "
                f"{safe_caption(reason, 80)} |"
            )
    push("")

    push("## 5. Worth-improving list (rewrite would add real value)")
    push("")
    worth = [
        f for f in flagged_sorted
        if suggest_improvement(f)[0] in ("improve", "keep-but-tighten")
    ]
    if not worth:
        push("_None._")
    else:
        push(
            "These blocks have enough scaffolding to be rescued. Either "
            "add a recurrence / invariant / complexity line, or upgrade "
            "to a runnable `Code Fragment` that imports a real library "
            "and demonstrates the operation."
        )
        push("")
        push("| File:line | Caption | Improvement path | Effort |")
        push("|---|---|---|---|")
        for f in worth:
            b = f.block
            verdict, p, e, _r = suggest_improvement(f)
            push(
                f"| `{rel(b.file)}:{b.line}` | "
                f"{safe_caption(b.label_text, 55)} | "
                f"{safe_caption(p, 90)} | {e} |"
            )
    push("")

    # Borderline (score = 1) blocks: surface as a watchlist.
    borderline = sorted(
        (f for f in result["findings"] if f.score == 1),
        key=lambda f: (rel(f.block.file), f.block.line),
    )
    push("## 6. Borderline watchlist (score = 1)")
    push("")
    push(
        "These blocks fire exactly one lameness signal. None reach the "
        "flag threshold, but the editor may want to inspect a few -- "
        "a single extra signal (e.g. a numbered-step list with no "
        "operators) would tip them over."
    )
    push("")
    if not borderline:
        push("_None._")
    else:
        push("| File:line | Caption | Signal |")
        push("|---|---|---|")
        for f in borderline:
            b = f.block
            push(
                f"| `{rel(b.file)}:{b.line}` | "
                f"{safe_caption(b.label_text, 70)} | "
                f"{','.join(f.active_signals)} |"
            )
    push("")

    push("## 7. Recommended editorial priority")
    push("")
    n_flagged = len(flagged_sorted)
    n_drop = len(quick_drops)
    n_improve = len(worth)
    if n_flagged == 0:
        push(
            "- No actionable lameness detected by automated signals. "
            "Spot-check manually if recent edits added any tiny "
            "Pseudocode boxes."
        )
    else:
        push(
            f"1. **Drop the quick-drop list** ({n_drop} blocks). "
            "These are pure narration; prose already says what they "
            "say. Deletion is the simplest fix and removes visual clutter."
        )
        push(
            f"2. **Rewrite the worth-improving list** ({n_improve} "
            "blocks). For each, ask: 'What recurrence, invariant, or "
            "complexity claim makes this algorithm non-trivial?' If "
            "the answer is 'nothing', drop it instead. If real "
            "library code would do the job better, upgrade to a "
            "`Code Fragment` and import the real API."
        )
        push(
            "3. **Renumber downstream blocks** after deletes. The "
            "`Pseudocode N.N.N` and `Algorithm N.N.N` captions are "
            "referenced from prose; check cross-references after any drop."
        )
        push(
            "4. **Add a stylistic rule to CONTENT_GUIDELINES.md**: a "
            "Pseudocode box must carry at least one of (recurrence, "
            "invariant, complexity claim, named data structure "
            "operation). If none applies, the content belongs in prose."
        )
        push(
            "5. **Re-run** `scripts/_audit_pseudocode_lameness.py` "
            "after edits to confirm the flagged count drops."
        )
    push("")
    push("---")
    push("")
    push(
        "Generated by `scripts/_audit_pseudocode_lameness.py`. Signals "
        "are heuristic; before deleting a block, read the surrounding "
        "prose to confirm the box really is redundant."
    )

    REPORT_PATH.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    result = audit()
    write_report(result)
    flagged = result["flagged"]
    flagged_sorted = sorted(
        flagged, key=lambda f: (-f.score, rel(f.block.file), f.block.line)
    )
    print(f"Files scanned: {result['files_scanned']}")
    print(f"Pseudocode / algorithm blocks: {result['blocks_total']}")
    for k, v in sorted(result["by_label"].items()):
        print(f"  label={k}: {v}")
    print(f"Total flagged (score>=2): {len(flagged)}")
    print()
    print("Top 5 worst offenders:")
    for i, f in enumerate(flagged_sorted[:5], start=1):
        b = f.block
        sigs = ",".join(f.active_signals)
        verdict, _p, eff, _r = suggest_improvement(f)
        print(
            f"  {i}. {rel(b.file)}:{b.line}  score={f.score}  "
            f"verdict={verdict}/{eff}"
        )
        print(f"     signals={sigs}")
        try:
            print(f"     {b.label_text[:90]}")
        except UnicodeEncodeError:
            print(
                f"     {b.label_text[:90].encode('ascii', 'replace').decode()}"
            )
    print()
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
