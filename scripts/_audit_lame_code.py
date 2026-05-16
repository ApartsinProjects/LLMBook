"""
Audit lame code fragments across the LLMBook.

A "lame" fragment parses cleanly but teaches nothing -- toy types with all-boolean
attributes, dummy implementations whose method bodies just store inputs in dicts
without validation, demos whose `print` output is identical to the input, classes
that wrap a `mark_complete(name)` setter and call it "compliance", and so on.

Anchor case: Code Fragment 30.4.1 had a ComplianceChecker dataclass storing 8
boolean flags, with mark_complete(name) simply setting checks[name] = True.
No regulation was actually checked.

For each <pre><code class="...lang-python..."> fragment we compute 8 signals
(score 0/1 each). Fragments with combined score >= 3 are flagged.

We also identify caption/code mismatch: when the caption claims a library or
concept (OpenAI, Anthropic, LangChain, exponential backoff, bootstrap CI, ...)
that the code does not actually demonstrate.

Output: lame-code-audit.md (top 30 worst offenders + mismatch list + summary).
"""

from __future__ import annotations

import ast
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

# Resolve project root relative to this script (scripts/_audit_lame_code.py).
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORT_PATH = PROJECT_ROOT / "lame-code-audit.md"

EXCLUDE_DIRS = {
    "KDP",
    ".claude",
    "scripts",
    "node_modules",
    "pagefind",
    "templates",
    ".git",
    ".html2pub_cache",
    ".github",
}
EXCLUDE_PREFIXES = ("temp_",)
EXCLUDE_CONTAINS = ("backups",)


def is_excluded(path: Path) -> bool:
    """Skip files under excluded directories or whose ancestors match prefixes."""
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
        if any(part.startswith(p) for p in EXCLUDE_PREFIXES):
            return True
        if any(c in part.lower() for c in EXCLUDE_CONTAINS):
            return True
    return False


# Caption / library claim heuristics.
# A claim consists of (regex on caption, set of strings the code must contain).
# Use specific positive constructions ("with X", "using X", "X library") and
# avoid hedging clauses ("such as X", "like X", "e.g. X", "replace with X").
# Negative-lookbehind on common hedge words keeps the claim primary, not aspirational.
HEDGE = r"(?<!such as )(?<!like )(?<!e\.g\. )(?<!e\.g\., )(?<!replace with )(?<!or )"

LIBRARY_CLAIMS: list[tuple[re.Pattern, list[str]]] = [
    (re.compile(rf"{HEDGE}\binstructor\b", re.I), ["instructor"]),
    (re.compile(rf"{HEDGE}\bopenai (?:api|sdk|client)\b", re.I),
     ["openai", "OpenAI", "from openai"]),
    (re.compile(rf"{HEDGE}\banthropic (?:api|sdk|client|messages)\b", re.I),
     ["anthropic", "Anthropic"]),
    (re.compile(rf"{HEDGE}\blangchain\b", re.I),
     ["langchain", "from langchain"]),
    (re.compile(rf"{HEDGE}\bllamaindex\b|\bllama[- ]index\b", re.I),
     ["llama_index", "llamaindex"]),
    (re.compile(rf"{HEDGE}\bhugging[- ]?face\b", re.I),
     ["transformers", "huggingface", "datasets", "AutoModel", "AutoTokenizer", "from huggingface_hub"]),
    (re.compile(rf"{HEDGE}\bpytorch\b", re.I),
     ["torch", "import torch"]),
    (re.compile(rf"{HEDGE}\btensorflow\b|\bkeras\b", re.I),
     ["tensorflow", "keras"]),
    (re.compile(rf"{HEDGE}\bpydantic\b", re.I),
     ["pydantic", "BaseModel"]),
    (re.compile(rf"{HEDGE}\bfastapi\b", re.I),
     ["fastapi", "FastAPI"]),
    (re.compile(rf"{HEDGE}\bspaCy\b|\bspacy\b", re.I),
     ["spacy"]),
    (re.compile(rf"{HEDGE}\bnumpy\b", re.I),
     ["numpy", "np.", "import numpy"]),
    (re.compile(rf"{HEDGE}\bpandas\b", re.I),
     ["pandas", "pd.", "import pandas"]),
    (re.compile(rf"{HEDGE}\bscikit[- ]learn\b|\bsklearn\b", re.I),
     ["sklearn", "from sklearn"]),
    (re.compile(rf"{HEDGE}\bweaviate\b", re.I), ["weaviate"]),
    (re.compile(rf"{HEDGE}\bchromadb\b", re.I), ["chromadb", "chroma"]),
    (re.compile(rf"{HEDGE}\bpinecone\b", re.I), ["pinecone"]),
    (re.compile(rf"{HEDGE}\bfaiss\b", re.I), ["faiss"]),
    (re.compile(rf"{HEDGE}\bqdrant\b", re.I), ["qdrant"]),
    (re.compile(rf"{HEDGE}\bmilvus\b", re.I), ["milvus"]),
    (re.compile(rf"{HEDGE}\bdeepeval\b", re.I), ["deepeval"]),
    (re.compile(rf"{HEDGE}\bragas\b", re.I), ["ragas"]),
    (re.compile(rf"{HEDGE}\bwandb\b|\bweights ?& ?biases\b", re.I), ["wandb"]),
    (re.compile(rf"{HEDGE}\bmlflow\b", re.I), ["mlflow"]),
    (re.compile(rf"{HEDGE}\bdvc\b", re.I), ["dvc"]),
    # peft/lora: only match when it's the central claim (e.g. "LoRA fine-tuning" or "PEFT library")
    # and only require lora-related identifiers in the code.
    (re.compile(rf"{HEDGE}\b(?:peft library|peft framework)\b", re.I),
     ["peft", "LoraConfig", "get_peft_model", "PeftModel"]),
    (re.compile(rf"{HEDGE}\btrl library\b", re.I),
     ["trl", "SFTTrainer", "DPOTrainer", "GRPOTrainer", "PPOTrainer"]),
]

# Library names that should appear (case-insensitively) anywhere in the source if
# the caption mentions them as the central topic and the code claims to demonstrate them.
# We check these as a STAND-ALONE signal: if the caption literally says "using X" or "with X"
# at the very start, the code must reference X.
PRIMARY_CLAIM_RE = re.compile(
    r"^\s*(?:Using|With|Calling|Invoking|Running|Loading|Demonstrating|Showcasing)\s+"
    r"(?:the\s+)?(\w[\w. \-]{1,30})",
    re.I,
)

# Concept claims (caption phrase -> AST/text features that should be present).
CONCEPT_CLAIMS: list[tuple[re.Pattern, list[str], str]] = [
    (re.compile(r"\bexponential\s+backoff\b", re.I),
     ["**", "* 2", "<<", "backoff", "tenacity"],
     "exponential backoff (** or *2 or tenacity)"),
    (re.compile(r"\bretry\b", re.I),
     ["for", "while", "tenacity", "retry"],
     "retry loop"),
    (re.compile(r"\bbootstrap\s+confidence\s+interval", re.I),
     ["resample", "np.random.choice", "random.choices", "percentile", "for _ in range"],
     "bootstrap resampling"),
    (re.compile(r"\bcosine\s+similarity\b", re.I),
     ["dot", "norm", "cosine", "/", "linalg"],
     "cosine similarity math"),
    (re.compile(r"\brate\s+limit\b", re.I),
     ["sleep", "time.", "ratelimit", "limiter", "for", "while", "429"],
     "rate-limit handling (sleep/loop/429)"),
    (re.compile(r"\bbeam\s+search\b", re.I),
     ["beam", "heap", "sort", "top"],
     "beam expansion"),
    (re.compile(r"\bdeduplicat", re.I),
     ["set(", "hash", "minhash", "dedup", "seen"],
     "deduplication"),
    (re.compile(r"\bcache\b|\bcaching\b", re.I),
     ["cache", "lru_cache", "redis", "dict"],
     "cache mechanism"),
]


def normalise_caption(text: str) -> str:
    """Strip the 'Code Fragment N.N.N:' prefix."""
    return re.sub(r"^\s*Code Fragment\s*[\d.]+\s*:\s*", "", text).strip()


@dataclass
class FragmentFinding:
    file: Path
    line: int
    fragment_id: Optional[str]
    caption: str
    code: str
    signals: dict = field(default_factory=dict)
    mismatch: list[str] = field(default_factory=list)

    @property
    def score(self) -> int:
        return sum(self.signals.values())

    @property
    def top_signals(self) -> list[str]:
        return sorted(
            (k for k, v in self.signals.items() if v),
            key=lambda k: SIGNAL_WEIGHT.get(k, 0),
            reverse=True,
        )


SIGNAL_WEIGHT = {
    "all_boolean_dataclass": 5,
    "boolean_dict_checklist": 6,  # the ComplianceChecker pattern
    "setter_only_methods": 5,
    "mark_complete_on_dict": 6,   # explicit mark_X(name) -> dict[name] = True
    "todo_only_body": 6,           # the body is just a `# TODO:` comment
    "placeholder_return": 4,
    "identity_print_demo": 4,
    "pure_dispatch_class": 3,
    "trivial_conditionals": 3,
    "no_concrete_data_values": 2,
    "missing_library_import": 4,  # downweighted: many false positives
}


# ---------- AST-based signal detectors ----------

def signal_all_boolean_dataclass(tree: ast.AST) -> bool:
    """A @dataclass with 5+ fields all annotated `bool` (typically `= False`)."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        has_dataclass = any(
            (isinstance(d, ast.Name) and d.id == "dataclass")
            or (isinstance(d, ast.Attribute) and d.attr == "dataclass")
            or (isinstance(d, ast.Call) and (
                (isinstance(d.func, ast.Name) and d.func.id == "dataclass")
                or (isinstance(d.func, ast.Attribute) and d.func.attr == "dataclass")
            ))
            for d in node.decorator_list
        )
        # Many books use plain classes too; treat as dataclass-like if 5+
        # AnnAssign children with bool annotations.
        bool_fields = 0
        total_fields = 0
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                total_fields += 1
                ann = stmt.annotation
                if isinstance(ann, ast.Name) and ann.id == "bool":
                    bool_fields += 1
        if bool_fields >= 5 and bool_fields == total_fields and (has_dataclass or total_fields >= 5):
            return True
    return False


def signal_boolean_dict_checklist(tree: ast.AST) -> bool:
    """A class with a `checks` (or similar) dict field whose default has 5+ False values.

    Matches the ComplianceChecker pattern:
        @dataclass
        class Foo:
            checks: dict = field(default_factory=lambda: {
                "a": False, "b": False, "c": False, "d": False, "e": False,
            })
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.AnnAssign):
                continue
            # Look at the default value: field(default_factory=lambda: {...})
            val = stmt.value
            if val is None:
                continue
            # Drill through field(default_factory=lambda: {...}).
            if isinstance(val, ast.Call):
                # Walk into keyword args for default_factory.
                lam = None
                for kw in val.keywords:
                    if kw.arg == "default_factory":
                        if isinstance(kw.value, ast.Lambda):
                            lam = kw.value
                if lam is not None and isinstance(lam.body, ast.Dict):
                    return _dict_is_mostly_false(lam.body)
            # Also handle a literal default ` = {"a": False, ...}`.
            if isinstance(val, ast.Dict):
                if _dict_is_mostly_false(val):
                    return True
    return False


def _dict_is_mostly_false(d: ast.Dict) -> bool:
    """True if dict has >=5 entries and all values are `False`."""
    if len(d.values) < 5:
        return False
    return all(isinstance(v, ast.Constant) and v.value is False for v in d.values)


def signal_mark_complete_on_dict(tree: ast.AST) -> bool:
    """A method named `mark_*` or `complete_*` that just sets `self.dict[name] = True`."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        name = node.name.lower()
        if not (name.startswith("mark_") or name.startswith("complete") or name.startswith("set_")
                or "mark" in name and "complete" in name):
            continue
        body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
        # Pattern A: single-statement subscript assign to True.
        # Pattern B: if-guard + subscript assign to True.
        def _is_set_true(stmt) -> bool:
            return (
                isinstance(stmt, ast.Assign)
                and len(stmt.targets) == 1
                and isinstance(stmt.targets[0], ast.Subscript)
                and isinstance(stmt.targets[0].value, ast.Attribute)
                and isinstance(stmt.value, ast.Constant)
                and stmt.value.value is True
            )
        if len(body) == 1 and _is_set_true(body[0]):
            return True
        if (len(body) == 1
                and isinstance(body[0], ast.If)
                and len(body[0].body) == 1
                and _is_set_true(body[0].body[0])):
            return True
    return False


def signal_setter_only_methods(tree: ast.AST) -> bool:
    """All methods in some class just assign one attribute or set a dict key.

    Examples that match:
        def set_x(self, v): self.x = v
        def mark_complete(self, name): self.flags[name] = True
        def mark_x(self): self.checks["x"] = True
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        methods = [s for s in node.body if isinstance(s, ast.FunctionDef)]
        # Exclude dunder methods from the "only" check; require >= 2 setter-like methods.
        non_dunder = [m for m in methods if not m.name.startswith("__")]
        if len(non_dunder) < 2:
            continue
        if all(_is_setter_like(m) for m in non_dunder):
            return True
    return False


def _is_setter_like(fn: ast.FunctionDef) -> bool:
    """A method whose body is at most one assignment to self.attr or self.dict[k]."""
    body = [s for s in fn.body if not isinstance(s, ast.Expr) or not isinstance(s.value, ast.Constant)]
    # Strip leading docstring.
    if len(body) != 1:
        return False
    stmt = body[0]
    if not isinstance(stmt, ast.Assign):
        return False
    if len(stmt.targets) != 1:
        return False
    target = stmt.targets[0]
    # self.X = something
    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
        return True
    # self.dict[key] = value
    if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Attribute):
        if isinstance(target.value.value, ast.Name) and target.value.value.id == "self":
            return True
    return False


def signal_placeholder_return(tree: ast.AST) -> bool:
    """A function whose body returns an empty dict/list/None or a docstring + return."""
    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    if not funcs:
        return False
    placeholders = 0
    for fn in funcs:
        body = [s for s in fn.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
        # body has at most a `return` statement
        if len(body) == 1 and isinstance(body[0], ast.Return):
            val = body[0].value
            if val is None:
                placeholders += 1
            elif isinstance(val, ast.Constant) and val.value is None:
                placeholders += 1
            elif isinstance(val, ast.Dict) and not val.keys:
                placeholders += 1
            elif isinstance(val, ast.List) and not val.elts:
                placeholders += 1
            elif isinstance(val, ast.Call) and isinstance(val.func, ast.Name) and val.func.id in {"dict", "list"} and not val.args and not val.keywords:
                placeholders += 1
        # Two-line body: x = {} ; return x  (uninitialized result)
        elif len(body) == 2 and isinstance(body[0], ast.Assign) and isinstance(body[1], ast.Return):
            init = body[0].value
            if isinstance(init, ast.Dict) and not init.keys:
                placeholders += 1
            elif isinstance(init, ast.List) and not init.elts:
                placeholders += 1
    # Require at least one full placeholder function in the fragment.
    return placeholders >= 1 and placeholders >= max(1, len(funcs) // 2)


def signal_pure_dispatch_class(tree: ast.AST) -> bool:
    """A class that just stores callables in a dict and calls them by name."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        # Look for a method that does self.handlers[name](*args) or similar.
        has_register = False
        has_dispatch = False
        has_real_logic = False
        for stmt in node.body:
            if not isinstance(stmt, ast.FunctionDef):
                continue
            src = ast.dump(stmt)
            if "Subscript" in src and "Call" in src:
                has_dispatch = True
            if any(k in stmt.name.lower() for k in ("register", "add_", "set_")):
                has_register = True
            # Count "real" statements (more than 3 lines of code or contains a loop/conditional with multiple branches)
            stmts_in_body = [s for s in stmt.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
            if len(stmts_in_body) > 3:
                has_real_logic = True
        if has_register and has_dispatch and not has_real_logic:
            return True
    return False


def signal_trivial_conditionals(tree: ast.AST) -> bool:
    """All `if`s in the fragment are trivial membership/None checks."""
    ifs = [n for n in ast.walk(tree) if isinstance(n, ast.If)]
    if len(ifs) < 2:
        return False
    trivial = 0
    for node in ifs:
        test = node.test
        if isinstance(test, ast.Compare):
            # `x in y` or `x is None` or `x == None`
            if any(isinstance(op, (ast.In, ast.NotIn, ast.Is, ast.IsNot)) for op in test.ops):
                trivial += 1
                continue
            if any(
                isinstance(c, ast.Constant) and (c.value is None or isinstance(c.value, bool))
                for c in test.comparators
            ):
                trivial += 1
                continue
        # `not x` / bare attribute
        if isinstance(test, (ast.Name, ast.Attribute, ast.UnaryOp)):
            trivial += 1
    return trivial >= len(ifs) and len(ifs) >= 2


def signal_identity_print_demo(code: str, tree: ast.AST) -> bool:
    """A demo block that prints back exactly its input (no transformation)."""
    # Look for: print(some_dict) where the dict was just constructed.
    # Heuristic: `print(VAR)` where VAR is assigned a literal dict/list and never mutated.
    prints = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call)
              and isinstance(n.func, ast.Name) and n.func.id == "print"]
    if not prints:
        return False
    # If the only thing printed is a variable that was just assigned a literal and never modified.
    suspicious = 0
    for p in prints:
        if len(p.args) != 1:
            continue
        arg = p.args[0]
        if not isinstance(arg, ast.Name):
            continue
        # Search the tree for that name on lhs and check for any AugAssign / subscript writes / method calls.
        name = arg.id
        assigned_to_literal = False
        was_mutated = False
        for n in ast.walk(tree):
            if isinstance(n, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in n.targets
            ):
                if isinstance(n.value, (ast.Dict, ast.List, ast.Constant, ast.Tuple)):
                    assigned_to_literal = True
            if isinstance(n, ast.AugAssign) and isinstance(n.target, ast.Name) and n.target.id == name:
                was_mutated = True
            if isinstance(n, ast.Assign) and any(
                isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == name
                for t in n.targets
            ):
                was_mutated = True
            # Method calls like name.append(...)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                if isinstance(n.func.value, ast.Name) and n.func.value.id == name:
                    was_mutated = True
        if assigned_to_literal and not was_mutated:
            suspicious += 1
    return suspicious >= 1


def signal_todo_only_body(code: str, tree: ast.AST) -> bool:
    """The entire code fragment is just a TODO comment (or 2-3 TODO comments)."""
    # Strip comments and whitespace from the source.
    no_comments = "\n".join(line.split("#")[0].rstrip() for line in code.splitlines())
    stripped = no_comments.strip()
    # If there's basically nothing left and the source had a TODO comment, flag it.
    if not stripped and re.search(r"#\s*TODO\b|#\s*FIXME\b", code, re.I):
        return True
    # Or: function body is just `pass` after a TODO comment.
    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    if funcs and re.search(r"#\s*TODO\b", code, re.I):
        all_pass = True
        for fn in funcs:
            body = [s for s in fn.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))]
            if not (len(body) == 1 and isinstance(body[0], ast.Pass)):
                all_pass = False
                break
        if all_pass:
            return True
    return False


def signal_no_concrete_data_values(code: str) -> bool:
    """Detect placeholder strings instead of realistic data."""
    placeholder_phrases = [
        r"\bsample text\b",
        r"\bexample input\b",
        r"\bexample text\b",
        r"\byour text here\b",
        r"\bsome text\b",
        r"\binput here\b",
        r"\bsome data\b",
        r"\binput goes here\b",
        r"['\"]foo['\"]",
        r"['\"]bar['\"]",
        r"['\"]baz['\"]",
        r"['\"]example['\"]",
        r"['\"]placeholder['\"]",
    ]
    hits = sum(bool(re.search(p, code, re.I)) for p in placeholder_phrases)
    return hits >= 2


# ---------- Caption / library mismatch ----------

def detect_library_mismatch(caption: str, code: str) -> list[str]:
    """Return library names claimed in caption but absent from code."""
    missing = []
    for pat, signals in LIBRARY_CLAIMS:
        if pat.search(caption):
            if not any(s in code for s in signals):
                # Pull the library name from the caption verbatim.
                m = pat.search(caption)
                if m:
                    missing.append(m.group(0).strip())
    return missing


def detect_concept_mismatch(caption: str, code: str) -> list[str]:
    """Return concepts claimed in caption but unsupported by code."""
    missing = []
    for pat, signals, label in CONCEPT_CLAIMS:
        if pat.search(caption):
            if not any(s in code for s in signals):
                missing.append(label)
    return missing


# ---------- HTML extraction ----------

def extract_text(node) -> str:
    """Strip HTML tags but preserve inner text and whitespace."""
    return node.get_text("", strip=False)


def extract_python_code(pre_node) -> str:
    """Get plain Python source from a pygments-highlighted <pre><code>."""
    return pre_node.get_text("", strip=False)


def find_fragment_id_from_caption(caption_text: str) -> Optional[str]:
    m = re.search(r"Code Fragment\s*([\d.]+)", caption_text)
    return m.group(1).rstrip(".") if m else None


def _find_preceding_pre(caption) -> Optional[object]:
    """Find the <pre> code block paired with this caption.

    Layout 1 (most common): <pre>...</pre> ... <div class="code-caption"> CAPTION
    Layout 2 (appendix-c.1): <div class="code-caption"> CAPTION ... <pre>...</pre>

    Heuristic: if the caption's immediately-previous non-whitespace sibling is a
    <pre> or <div class="code-output">, use backward (layout 1). Otherwise,
    look forward (layout 2).
    """
    # Look at adjacent text/sibling structure to decide.
    prev_sib = caption.find_previous_sibling()
    # Walk back through whitespace-only nodes.
    if prev_sib is not None and hasattr(prev_sib, "name"):
        if prev_sib.name == "pre":
            return prev_sib
        if prev_sib.name == "div":
            cls = prev_sib.get("class") or []
            if "code-output" in cls or "code-block-wrapper" in cls:
                # The pre is inside this wrapper.
                pre = prev_sib.find("pre")
                if pre is not None:
                    return pre
                # Otherwise scan backward further.
        # If previous sibling is a heading or paragraph, scan in same direction.
    # Layout 1 attempt: walk backward looking for <pre>, stopping at headings/captions.
    back = _walk_for_pre(caption, direction="prev")
    if back is not None:
        return back[0]
    # Layout 2 attempt: walk forward.
    fwd = _walk_for_pre(caption, direction="next")
    if fwd is not None:
        return fwd[0]
    return None


def _walk_for_pre(caption, direction: str):
    """Walk in one direction looking for a <pre>.

    Stop conditions: another <div class="code-caption"> or a major heading
    boundary (<h1>, <h2>, <hr>). Returns (pre_tag, steps) or None.
    """
    cur = caption
    steps = 0
    while True:
        cur = cur.find_previous() if direction == "prev" else cur.find_next()
        if cur is None or steps > 200:
            return None
        if not hasattr(cur, "name") or cur.name is None:
            continue
        steps += 1
        if cur.name in {"h1", "h2", "h3", "hr"}:
            return None
        if cur.name == "div":
            cls = cur.get("class") or []
            if "code-caption" in cls:
                return None
        if cur.name == "pre":
            return (cur, steps)


def iter_fragments_in_html(html_path: Path):
    """Yield (line_number, caption_div, code_pre) for each python fragment with a caption.

    Pairing strategy: collect all <pre> tags and all captions in document order, then
    pair each caption with the nearest <pre> that is not already paired with another
    caption. Captions and code blocks alternate in two orders across the book:
      - Layout A (most common): code, [output,] caption.
      - Layout B (appendices c, k, m, ...): caption, callout-with-code.
    """
    try:
        text = html_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    # All <pre> tags whose code is python.
    pres = []
    for pre in soup.find_all("pre"):
        code_tag = pre.find("code")
        cls_list = (code_tag.get("class") if code_tag else pre.get("class")) or []
        cls = " ".join(cls_list) if isinstance(cls_list, list) else str(cls_list)
        if "python" in cls.lower():
            pres.append(pre)
    captions = soup.find_all("div", class_="code-caption")
    # Pair captions to <pre> using content similarity + order-preserving constraint.
    pre_lines = {id(p): _line_of(p, text) for p in pres}
    cap_lines = {id(c): _line_of(c, text) for c in captions}
    pre_sorted = sorted(pres, key=lambda p: pre_lines[id(p)])
    cap_sorted = sorted(captions, key=lambda c: cap_lines[id(c)])

    # Extract content signatures.
    pre_sigs = [(_code_signature(pre), pre) for pre in pre_sorted]
    cap_sigs = [(_caption_signature(cap), cap) for cap in cap_sorted]

    # Score each (cap, pre) pair: distance penalty + content overlap bonus.
    # Then use a monotone alignment.
    n = len(cap_sigs)
    m = len(pre_sigs)
    pairs = []
    pre_idx = 0
    for cap_sig, cap in cap_sigs:
        cap_line = cap_lines[id(cap)]
        best_pre = None
        best_score = float("inf")
        best_j = pre_idx
        for j in range(pre_idx, m):
            pre_sig, pre = pre_sigs[j]
            pre_line = pre_lines[id(pre)]
            line_dist = abs(pre_line - cap_line)
            content_overlap = _overlap_score(cap_sig, pre_sig)
            # Lower score = better. Content overlap is a strong signal (subtract).
            score = line_dist - content_overlap * 100
            if score < best_score:
                best_score = score
                best_pre = pre
                best_j = j
        if best_pre is not None:
            pairs.append((cap_line, cap, best_pre))
            pre_idx = best_j + 1
    pairs.sort(key=lambda x: x[0])
    for line, caption, pre in pairs:
        yield line, caption, pre


def _code_signature(pre) -> set[str]:
    """Bag of significant tokens from the first comment / first 60 chars of code."""
    code = pre.get_text("", strip=False)
    # Take the first 200 chars.
    head = code[:200]
    tokens = re.findall(r"[A-Za-z][A-Za-z_0-9]{2,}", head.lower())
    return {t for t in tokens if t not in _STOP}


def _caption_signature(cap) -> set[str]:
    text = cap.get_text(" ", strip=True)
    text = re.sub(r"^\s*Code Fragment\s*[\d.]+\s*:\s*", "", text)
    tokens = re.findall(r"[A-Za-z][A-Za-z_0-9]{2,}", text.lower())
    return {t for t in tokens if t not in _STOP}


_STOP = {
    "the", "and", "for", "with", "from", "this", "that", "code", "fragment",
    "use", "using", "import", "via", "via", "into", "implementation",
    "library", "shows", "example", "shortcut", "snippet", "demonstrates",
    "function", "method", "class", "model", "data", "create", "build",
    "definition", "implementation",
}


def _overlap_score(a: set[str], b: set[str]) -> int:
    """Number of tokens common to both signatures."""
    return len(a & b)


def _line_of(tag, text: str) -> int:
    """Approximate 1-based line number where `tag` appears in `text`."""
    s = str(tag)[:120]
    idx = text.find(s)
    if idx < 0:
        # Try a shorter prefix.
        s = str(tag)[:60]
        idx = text.find(s)
    if idx < 0:
        return 0
    return text.count("\n", 0, idx) + 1


# ---------- Main scoring ----------

def _parse_or_recover(code: str) -> Optional[ast.AST]:
    """Try ast.parse(code). If that fails, try common recoveries."""
    try:
        return ast.parse(code)
    except SyntaxError:
        pass
    # Attempt: wrap the snippet in a dummy function body (handles dangling indent).
    try:
        indented = "\n".join("    " + line for line in code.splitlines())
        return ast.parse(f"def __wrapped():\n{indented}\n    pass\n")
    except SyntaxError:
        pass
    # Attempt: dedent (strip common leading indent).
    try:
        import textwrap
        return ast.parse(textwrap.dedent(code))
    except SyntaxError:
        return None


def score_fragment(code: str, caption: str) -> tuple[dict, list[str]]:
    signals = {k: False for k in SIGNAL_WEIGHT}
    mismatch: list[str] = []

    # Parse Python. Many book fragments are incomplete (single methods, partial
    # class bodies, snippets that begin with `if/else` because the surrounding
    # function was elided). Try to recover by re-parsing with an extra indent
    # stripped or by wrapping in a dummy function.
    tree = _parse_or_recover(code)
    if tree is None:
        # Cannot evaluate AST signals; only test the textual ones.
        if signal_no_concrete_data_values(code):
            signals["no_concrete_data_values"] = True
        if re.search(r"#\s*TODO\b|#\s*FIXME\b", code, re.I):
            # Crude: if it's mostly TODO comments and short, flag it.
            non_comment = "\n".join(line.split("#")[0].rstrip() for line in code.splitlines())
            if len(non_comment.strip()) < 20:
                signals["todo_only_body"] = True
        mismatch.extend(detect_library_mismatch(caption, code))
        mismatch.extend(detect_concept_mismatch(caption, code))
        return signals, mismatch

    # AST signals.
    signals["all_boolean_dataclass"] = signal_all_boolean_dataclass(tree)
    signals["boolean_dict_checklist"] = signal_boolean_dict_checklist(tree)
    signals["mark_complete_on_dict"] = signal_mark_complete_on_dict(tree)
    signals["setter_only_methods"] = signal_setter_only_methods(tree)
    signals["placeholder_return"] = signal_placeholder_return(tree)
    signals["pure_dispatch_class"] = signal_pure_dispatch_class(tree)
    signals["trivial_conditionals"] = signal_trivial_conditionals(tree)
    signals["identity_print_demo"] = signal_identity_print_demo(code, tree)
    signals["todo_only_body"] = signal_todo_only_body(code, tree)
    signals["no_concrete_data_values"] = signal_no_concrete_data_values(code)

    # Caption mismatch / missing-library signal.
    lib_missing = detect_library_mismatch(caption, code)
    concept_missing = detect_concept_mismatch(caption, code)
    mismatch = lib_missing + concept_missing
    if lib_missing:
        signals["missing_library_import"] = True

    return signals, mismatch


def main() -> int:
    html_files: list[Path] = []
    for path in PROJECT_ROOT.rglob("*.html"):
        if is_excluded(path.relative_to(PROJECT_ROOT)):
            continue
        html_files.append(path)
    print(f"Scanning {len(html_files)} HTML files...", file=sys.stderr)

    findings: list[FragmentFinding] = []
    parse_errors = 0
    fragments_total = 0
    for html_path in html_files:
        for line, caption_div, code_pre in iter_fragments_in_html(html_path):
            fragments_total += 1
            caption_text = caption_div.get_text(" ", strip=True)
            caption_norm = normalise_caption(caption_text)
            code = extract_python_code(code_pre)
            # Decode HTML entities the get_text didn't unescape (e.g. &lt;).
            # BeautifulSoup get_text already unescapes &amp;/&lt;/&gt;.
            if _parse_or_recover(code) is None:
                parse_errors += 1
                # Continue: textual signals still apply.

            signals, mismatch = score_fragment(code, caption_norm)
            score = sum(signals.values())
            if score < 3 and not mismatch:
                continue
            f = FragmentFinding(
                file=html_path.relative_to(PROJECT_ROOT),
                line=line,
                fragment_id=find_fragment_id_from_caption(caption_text),
                caption=caption_norm,
                code=code,
                signals={k: bool(v) for k, v in signals.items() if v},
                mismatch=mismatch,
            )
            findings.append(f)

    print(f"Scanned {fragments_total} python fragments; {parse_errors} parse errors; flagged {len(findings)}", file=sys.stderr)
    write_report(findings, fragments_total)
    return 0


# ---------- Report writer ----------

def format_signals(signals: dict) -> str:
    return ", ".join(sorted(signals.keys()))


def write_report(findings: list[FragmentFinding], total_fragments: int) -> None:
    findings.sort(key=lambda f: (f.score + (3 if f.mismatch else 0)), reverse=True)

    score_buckets = Counter()
    for f in findings:
        bucket = f.score + (3 if f.mismatch else 0)
        if bucket >= 6:
            score_buckets["6+"] += 1
        else:
            score_buckets[str(bucket)] += 1

    mismatch_findings = [f for f in findings if f.mismatch]
    mismatch_findings.sort(key=lambda f: len(f.mismatch), reverse=True)

    lines: list[str] = []
    lines.append("# Lame Code Audit")
    lines.append("")
    lines.append("Generated by `scripts/_audit_lame_code.py`.")
    lines.append("")
    lines.append(f"Scanned **{total_fragments}** Python code fragments across the book.")
    lines.append(f"Flagged **{len(findings)}** fragments with lameness score >= 3 or caption/code mismatch.")
    lines.append("")
    lines.append("Each fragment is scored 0-1 on the following signals:")
    lines.append("")
    for k, w in sorted(SIGNAL_WEIGHT.items(), key=lambda kv: -kv[1]):
        lines.append(f"- `{k}` (weight {w})")
    lines.append("")
    lines.append("A caption/code **mismatch** (caption claims a library or concept absent from the code) adds +3 to effective score.")
    lines.append("")
    lines.append("**False-positive note:** the `missing_library_import` signal can fire when the caption "
                 "and code legitimately demonstrate complementary approaches (e.g. a caption that mentions "
                 "FAISS but the paired demo uses ChromaDB to show an alternative). Treat that signal as "
                 "'caption may need an edit' rather than 'code is lame'. The `todo_only_body`, "
                 "`boolean_dict_checklist`, `mark_complete_on_dict`, and `placeholder_return` signals are "
                 "the strongest indicators of pedagogically lame code.")
    lines.append("")
    # Surface signal counts so the reader can see what's actually firing.
    signal_counts: Counter = Counter()
    for f in findings:
        for k in f.signals:
            signal_counts[k] += 1
    lines.append("**Signal frequency across flagged fragments:**")
    lines.append("")
    for sig, count in signal_counts.most_common():
        lines.append(f"- `{sig}`: {count}")
    lines.append("")
    # Anchor-case observation: if the 30.4.1 pattern (boolean_dict_checklist /
    # mark_complete_on_dict) is empty, point that out explicitly.
    if signal_counts.get("boolean_dict_checklist", 0) == 0 and signal_counts.get("mark_complete_on_dict", 0) == 0:
        lines.append("> **Anchor-case finding:** The `boolean_dict_checklist` + `mark_complete_on_dict` pattern (the original Code Fragment 30.4.1 lameness) is **not** found anywhere else in the book. The 30.4.1 fix appears to have eliminated this specific anti-pattern globally.")
        lines.append("")

    # ---- Summary table ----
    lines.append("## 1. Summary by Effective Score")
    lines.append("")
    lines.append("| Bucket | Count |")
    lines.append("|---|---|")
    for key in ("6+", "5", "4", "3"):
        lines.append(f"| {key} | {score_buckets.get(key, 0)} |")
    lines.append("")

    # ---- Top 30 ----
    lines.append("## 2. Top 30 Worst Offenders")
    lines.append("")
    lines.append("Sorted by effective score (lameness signals + 3 if mismatch). The 'Top signals' column lists the two highest-weighted signals that triggered.")
    lines.append("")
    lines.append("| # | File | Line | Fragment | Score | Mismatch | Top signals | Caption (truncated) |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for i, f in enumerate(findings[:30], 1):
        top = f.top_signals[:2]
        sig_str = ", ".join(f"`{s}`" for s in top) if top else "-"
        mismatch_str = "; ".join(f.mismatch) if f.mismatch else "-"
        cap = f.caption[:90].replace("|", "\\|").replace("\n", " ")
        if len(f.caption) > 90:
            cap += "..."
        eff = f.score + (3 if f.mismatch else 0)
        frag_id = f.fragment_id or "-"
        lines.append(f"| {i} | `{f.file.as_posix()}` | {f.line} | {frag_id} | {eff} | {mismatch_str} | {sig_str} | {cap} |")
    lines.append("")

    # ---- Mismatch list ----
    lines.append("## 3. Caption/Code Mismatch (Pedagogically Worst)")
    lines.append("")
    if not mismatch_findings:
        lines.append("_None detected._")
    else:
        lines.append("These fragments claim a specific library or concept in the caption but the code does not contain it. This is the worst kind of lameness because it teaches an incorrect mental model.")
        lines.append("")
        lines.append("| # | File | Line | Fragment | Missing | Caption (truncated) |")
        lines.append("|---|---|---|---|---|---|")
        for i, f in enumerate(mismatch_findings[:40], 1):
            missing_str = "; ".join(f.mismatch)
            cap = f.caption[:120].replace("|", "\\|").replace("\n", " ")
            if len(f.caption) > 120:
                cap += "..."
            frag_id = f.fragment_id or "-"
            lines.append(f"| {i} | `{f.file.as_posix()}` | {f.line} | {frag_id} | {missing_str} | {cap} |")
    lines.append("")

    # ---- Recommended rewrites for top 5 ----
    lines.append("## 4. Recommended Rewrites (Top 5)")
    lines.append("")
    for i, f in enumerate(findings[:5], 1):
        lines.append(f"### {i}. `{f.file.as_posix()}` (Code Fragment {f.fragment_id or '-'})")
        lines.append("")
        lines.append(f"**Caption:** {f.caption}")
        lines.append("")
        lines.append(f"**Signals:** {format_signals(f.signals)}")
        if f.mismatch:
            lines.append(f"  ")
            lines.append(f"**Mismatch:** {'; '.join(f.mismatch)}")
        lines.append("")
        # Excerpt: first 12 lines of code.
        snippet = f.code.strip().splitlines()[:12]
        lines.append("```python")
        lines.extend(snippet)
        if len(f.code.strip().splitlines()) > 12:
            lines.append("# ... (truncated)")
        lines.append("```")
        lines.append("")
        lines.append("**Sketch:** " + propose_rewrite(f))
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report to {REPORT_PATH}", file=sys.stderr)


def propose_rewrite(f: FragmentFinding) -> str:
    """A short one-paragraph rewrite sketch tailored to the signals."""
    s = set(f.signals.keys())
    parts = []
    if "todo_only_body" in s:
        parts.append(
            "The fragment is a placeholder (`# TODO:` and nothing else). Replace it with a working "
            "starter that the reader can run end-to-end: 6-15 lines that load data, exercise the API, "
            "and print one realistic result. If it must remain a lab stub, mark it explicitly as 'student "
            "exercise' and pair it with a separate solution fragment in the same section."
        )
    if "boolean_dict_checklist" in s or "mark_complete_on_dict" in s:
        parts.append(
            "Replace the boolean-dict checklist with a list of `Requirement` objects, each mapping a "
            "domain rule to a real `check(config) -> (passed, evidence)` callable (the 30.4.1 pattern). "
            "Cite the standard/article/spec each rule enforces and surface a remediation hint on failure."
        )
    if "all_boolean_dataclass" in s:
        parts.append(
            "Drop the all-bool dataclass; model each requirement as a named callable that returns "
            "(bool, evidence). The reader needs to see what gets checked, not just which flag flips."
        )
    if "setter_only_methods" in s:
        parts.append(
            "Drop the `mark_*` / `set_*` setters; have each method compute its result from inputs and "
            "return a concrete value (number, structured dict with evidence, or domain object)."
        )
    if "placeholder_return" in s:
        parts.append(
            "Implement the function body using a published spec or a small real algorithm; "
            "even a 5-line implementation that returns derived data beats `return {}`."
        )
    if "missing_library_import" in s and f.mismatch:
        libs = ", ".join(sorted(set(f.mismatch)))
        parts.append(
            f"The caption claims {libs}, but the code never imports or calls it. Either rewrite the "
            f"code to use {libs} (with a credible API shape) or edit the caption to describe what the "
            f"code actually does."
        )
    if "identity_print_demo" in s:
        parts.append(
            "Choose a demo input whose processed output is visibly different from the input; "
            "show one passing and one failing case so the reader sees the function discriminate."
        )
    if "pure_dispatch_class" in s:
        parts.append(
            "Either embed one or two real handler implementations inline (not just registration) "
            "or convert the class into a stand-alone dispatch function with a worked example."
        )
    if "trivial_conditionals" in s:
        parts.append(
            "Replace `if key in dict` / `if x is None` checks with domain conditions "
            "(threshold violations, format constraints, range checks against a spec)."
        )
    if "no_concrete_data_values" in s:
        parts.append(
            "Swap `'sample text'` / `'foo'` for realistic data drawn from the chapter's running example."
        )
    if not parts:
        parts.append("Rewrite to perform real domain logic rather than placeholder bookkeeping.")
    return " ".join(parts)


if __name__ == "__main__":
    sys.exit(main())
