"""
Code-fragment value audit.

Flags `<pre><code class="...lang-python...">` fragments that add no pedagogical
or technical value: pure-data blocks, constants-only blocks, string-template-only
blocks, identity-print demos, mock/fake APIs, wrapper-without-implementation
classes, and pseudo-API blocks with invented method names.

A fragment is flagged when it matches a "no-value" pattern OR scores >=2 across
the seven value signals. For each flagged fragment we emit a REWRITE SKETCH that
proposes a real third-party library or API call and the lesson it would teach.

This audit is READ-ONLY: it only writes the report file.

Output: code-value-audit.md
"""

from __future__ import annotations

import ast
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORT_PATH = PROJECT_ROOT / "code-value-audit.md"

EXCLUDE_DIRS = {
    "KDP",
    ".claude",
    "scripts",
    "node_modules",
    "pagefind",
    "templates",
    ".git",
    ".html2epub_cache",
    ".github",
    "agents",
}
EXCLUDE_PREFIXES = ("temp_",)
EXCLUDE_CONTAINS = ("backups",)


def is_excluded(path: Path) -> bool:
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
        if any(part.startswith(p) for p in EXCLUDE_PREFIXES):
            return True
        if any(c in part.lower() for c in EXCLUDE_CONTAINS):
            return True
    return False


# ---------- Value signal weights ----------

# Higher weight = more clearly low-value.
SIGNAL_WEIGHT = {
    "pure_data_block": 5,           # dataclass/TypedDict/Pydantic with no logic
    "constants_only": 5,            # only X = "..." / Y = 42 lines
    "string_template_only": 4,      # f-string templates with no rendering
    "identity_print_demo": 4,       # variable -> print with no transform
    "mock_or_fake_api": 6,          # def call_llm(...): return "fake response"
    "wrapper_without_impl": 5,      # __getattr__ delegation / pure passthrough
    "pseudo_api_block": 5,          # invented methods on .client / .api object
    "no_imports_no_calls": 3,       # no imports, no function calls, no I/O
    "trivial_print_only": 3,        # only prints and string literals
}


@dataclass
class FragmentFinding:
    file: Path
    line: int
    fragment_id: Optional[str]
    caption: str
    code: str
    signals: dict = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    @property
    def score(self) -> int:
        return sum(SIGNAL_WEIGHT[k] for k, v in self.signals.items() if v)

    @property
    def top_signals(self) -> list[str]:
        return sorted(
            (k for k, v in self.signals.items() if v),
            key=lambda k: SIGNAL_WEIGHT.get(k, 0),
            reverse=True,
        )

    @property
    def signal_count(self) -> int:
        return sum(1 for v in self.signals.values() if v)


# ---------- AST-based signal detectors ----------

PYDANTIC_BASE_NAMES = {"BaseModel", "BaseSettings"}
TYPED_DICT_NAMES = {"TypedDict", "NamedTuple"}
DATACLASS_DECORATORS = {"dataclass", "attrs", "define"}


def _is_dataclass_or_schema(cls: ast.ClassDef) -> bool:
    """True if class is a dataclass / Pydantic BaseModel / TypedDict / NamedTuple."""
    # Decorator-based: @dataclass, @pydantic.dataclass, @attrs.define
    for d in cls.decorator_list:
        name = None
        if isinstance(d, ast.Name):
            name = d.id
        elif isinstance(d, ast.Attribute):
            name = d.attr
        elif isinstance(d, ast.Call):
            if isinstance(d.func, ast.Name):
                name = d.func.id
            elif isinstance(d.func, ast.Attribute):
                name = d.func.attr
        if name in DATACLASS_DECORATORS:
            return True
    # Base-class: BaseModel / TypedDict / NamedTuple
    for b in cls.bases:
        name = None
        if isinstance(b, ast.Name):
            name = b.id
        elif isinstance(b, ast.Attribute):
            name = b.attr
        if name in PYDANTIC_BASE_NAMES | TYPED_DICT_NAMES:
            return True
    return False


def _class_methods(cls: ast.ClassDef) -> list[ast.FunctionDef]:
    return [s for s in cls.body if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _class_fields(cls: ast.ClassDef) -> list[ast.AnnAssign]:
    """Return AnnAssign nodes that look like field declarations."""
    fields_ = []
    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            fields_.append(stmt)
    return fields_


def signal_pure_data_block(tree: ast.AST, code: str) -> bool:
    """Pydantic model / dataclass / TypedDict with only field declarations and no methods or validators.

    Flag when:
      - There is at least one such class.
      - It has >=3 field annotations.
      - It has no methods, no validators, no Field() arguments beyond defaults.
      - The fragment itself contains NO function calls outside the class definition
        (i.e. there is no `model = MyModel(...)` demo that exercises it).
    """
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    data_classes = [c for c in classes if _is_dataclass_or_schema(c)]
    if not data_classes:
        return False

    qualifying = False
    for cls in data_classes:
        methods = [m for m in _class_methods(cls) if not m.name.startswith("__")]
        validators = []
        for m in methods:
            for d in m.decorator_list:
                dname = None
                if isinstance(d, ast.Name):
                    dname = d.id
                elif isinstance(d, ast.Attribute):
                    dname = d.attr
                elif isinstance(d, ast.Call):
                    if isinstance(d.func, ast.Name):
                        dname = d.func.id
                    elif isinstance(d.func, ast.Attribute):
                        dname = d.func.attr
                if dname and "validator" in (dname or "").lower():
                    validators.append(m)
        fields_ = _class_fields(cls)
        # Skip if class has any non-dunder method or validator.
        if methods or validators:
            continue
        if len(fields_) < 3:
            continue
        # Check Field()-style arguments. If the Field() call has constraint kwargs
        # (ge/le/gt/lt/min_length/max_length/regex/pattern) that IS pedagogy, skip.
        has_constraints = False
        for f in fields_:
            if isinstance(f.value, ast.Call):
                fn = f.value.func
                fn_name = None
                if isinstance(fn, ast.Name):
                    fn_name = fn.id
                elif isinstance(fn, ast.Attribute):
                    fn_name = fn.attr
                if fn_name == "Field":
                    for kw in f.value.keywords:
                        if kw.arg in {"ge", "le", "gt", "lt", "min_length", "max_length",
                                      "regex", "pattern", "multiple_of", "min_items",
                                      "max_items"}:
                            has_constraints = True
                            break
            if has_constraints:
                break
        if has_constraints:
            continue
        qualifying = True
        break

    if not qualifying:
        return False
    # Textual short-circuit: if the source contains an obvious usage line
    # (an `assert`, a `print(` with formatted output, a function `def test_`,
    # an instantiation of a known LLM SDK), treat as non-pure.
    usage_markers = [
        r"\bassert\s+",
        r"^\s*print\s*\(",
        r"def\s+test_",
        r"openai\.|anthropic\.",
        r"client\.(?:chat|messages|completions|embeddings)\b",
        r"\.from_(?:pretrained|documents|texts)\b",
        r"\.invoke\s*\(",
        r"raise\s+ValidationError",
        r"@(?:app|router)\.(?:get|post|put|delete|patch)\b",
    ]
    for pat in usage_markers:
        if re.search(pat, code, re.M):
            return False
    # Then use ast walk to confirm there are no calls outside the class definitions.
    outside_calls = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        in_class = False
        for cls in data_classes:
            if _is_descendant(node, cls):
                in_class = True
                break
        if not in_class:
            outside_calls += 1
    # Allow a tiny amount of demo (like an unused print) but no real instantiation.
    return outside_calls <= 1


def _is_descendant(node: ast.AST, ancestor: ast.AST) -> bool:
    """Walk the AST: True if `node` appears anywhere in subtree rooted at `ancestor`."""
    for n in ast.walk(ancestor):
        if n is node:
            return True
    return False


def signal_constants_only(tree: ast.AST) -> bool:
    """Module body is only Assign-to-literal lines.

    True when:
      - body has >=3 statements.
      - >=80% are simple Assign(targets=[Name], value=literal).
      - no function calls anywhere in the AST.
    """
    if not isinstance(tree, ast.Module):
        return False
    if len(tree.body) < 3:
        return False
    literals = 0
    others = 0
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            if len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
                if isinstance(stmt.value, (ast.Constant, ast.List, ast.Tuple, ast.Dict, ast.Set)):
                    literals += 1
                    continue
                # f-strings / joined strings of constants count too if they are simple.
                if isinstance(stmt.value, ast.JoinedStr):
                    # Pure f-string templates handled elsewhere; here treat as literal-ish.
                    literals += 1
                    continue
        # imports do not count against us but do not count toward "constants".
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            continue
        # Docstring expression at top doesn't count.
        if (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)):
            continue
        others += 1
    total = literals + others
    if total < 3:
        return False
    if literals / total < 0.8:
        return False
    # Refuse to flag if there is any function call in the source.
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            return False
    return True


def signal_string_template_only(tree: ast.AST, code: str) -> bool:
    """Fragment only defines string templates (PromptTemplate / f-string assignment)
    and never renders/formats/calls them."""
    if not isinstance(tree, ast.Module):
        return False
    assigns = [s for s in tree.body if isinstance(s, ast.Assign)]
    if not assigns:
        return False
    # Count string-template assigns.
    string_assigns = 0
    for s in assigns:
        v = s.value
        if isinstance(v, ast.Constant) and isinstance(v.value, str) and len(v.value) > 40:
            string_assigns += 1
        elif isinstance(v, ast.JoinedStr):
            string_assigns += 1
        elif isinstance(v, ast.Call):
            # PromptTemplate(template="...") or similar.
            fn = v.func
            fn_name = None
            if isinstance(fn, ast.Name):
                fn_name = fn.id
            elif isinstance(fn, ast.Attribute):
                fn_name = fn.attr
            if fn_name and "Template" in fn_name:
                string_assigns += 1
    if string_assigns < 1:
        return False
    # Are there ANY other function calls (rendering / formatting / API calls)?
    other_calls = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        # Calls that ARE the template constructor count as zero "rendering".
        fn = node.func
        fn_name = None
        if isinstance(fn, ast.Name):
            fn_name = fn.id
        elif isinstance(fn, ast.Attribute):
            fn_name = fn.attr
        if fn_name and "Template" in fn_name:
            continue
        # .format() / .render() / .invoke() / generate() / create() count as rendering.
        if fn_name in {"format", "render", "invoke", "generate", "create", "complete",
                       "chat", "completions", "messages", "send", "predict", "ainvoke",
                       "stream", "run"}:
            other_calls += 1
        else:
            other_calls += 1
    # No rendering at all: flag.
    if other_calls == 0:
        # And the templates must be substantive (contain {placeholder} or be long).
        if re.search(r"\{[^{}]+\}", code) or any(
                isinstance(s.value, ast.Constant) and isinstance(s.value.value, str)
                and len(s.value.value) > 80
                for s in assigns):
            return True
    return False


def signal_mock_or_fake_api(tree: ast.AST, code: str) -> bool:
    """Function definition that returns a hard-coded "fake" / "mock" / placeholder value."""
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if not funcs:
        return False
    suspicious_names = {"call_llm", "ask_llm", "query_llm", "complete", "generate",
                        "chat", "respond", "predict", "answer", "ask", "llm_call",
                        "model_call", "api_call", "call_model", "call_api"}
    for fn in funcs:
        name_lower = fn.name.lower()
        is_suspicious = (name_lower in suspicious_names
                         or any(k in name_lower for k in ("llm", "api", "model", "chat", "fake",
                                                          "mock", "stub", "dummy")))
        if not is_suspicious:
            continue
        # Body: skip leading docstring, then look at remaining statements.
        body = list(fn.body)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
            body = body[1:]
        if not body:
            continue
        # Pattern A: single return of a string/dict constant.
        if len(body) == 1 and isinstance(body[0], ast.Return):
            v = body[0].value
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                return True
            if isinstance(v, ast.Dict):
                # all values constant => looks like a fake response payload.
                if all(isinstance(val, ast.Constant) for val in v.values):
                    return True
            if isinstance(v, ast.JoinedStr):
                # f"fake response to {prompt}"
                return True
        # Pattern B: body has random.choice / random.choices on a small list of canned strings.
        for stmt in body:
            for node in ast.walk(stmt):
                if isinstance(node, ast.Call):
                    fn_ = node.func
                    fn_name = None
                    if isinstance(fn_, ast.Attribute):
                        fn_name = fn_.attr
                    if fn_name in {"choice", "choices", "sample"}:
                        return True
    # Also flag a top-level lambda named call_llm or similar.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            target = node.targets[0] if node.targets else None
            if isinstance(target, ast.Name) and target.id.lower() in suspicious_names:
                if isinstance(node.value, ast.Lambda):
                    return True
    # Look for explicit "fake" / "mock" comments above suspicious defs.
    if re.search(r"#.*(fake|mock|stub|dummy|placeholder).*(response|llm|api|client)", code, re.I):
        # And there's a def of one of the suspicious names.
        for fn in funcs:
            if fn.name.lower() in suspicious_names:
                return True
    return False


def signal_wrapper_without_impl(tree: ast.AST) -> bool:
    """A class that wraps another with pure delegation (__getattr__ to inner)."""
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    for cls in classes:
        methods = _class_methods(cls)
        if not methods:
            continue
        # Look for __getattr__ that forwards to self.<inner>.
        getattr_method = None
        for m in methods:
            if m.name == "__getattr__":
                getattr_method = m
                break
        if getattr_method is None:
            continue
        # The other methods are __init__ + maybe __repr__.
        non_dunder = [m for m in methods if not m.name.startswith("__")]
        if non_dunder:
            continue
        # The getattr_method body should be exactly `return getattr(self.<x>, name)`.
        body = [s for s in getattr_method.body
                if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
        if len(body) == 1 and isinstance(body[0], ast.Return):
            r = body[0].value
            if isinstance(r, ast.Call) and isinstance(r.func, ast.Name) and r.func.id == "getattr":
                return True
        # Or any return that just returns an attr of an attribute (delegation).
        if len(body) == 1 and isinstance(body[0], ast.Return):
            r = body[0].value
            if isinstance(r, ast.Attribute) and isinstance(r.value, ast.Attribute):
                return True
    return False


def signal_pseudo_api_block(tree: ast.AST, code: str) -> bool:
    """Invented method names on a `.client` / `.api` / `.agent` object.

    Restrictive detector: only flag when the fragment has NO imports of a known
    library (so the receiver cannot be a real client) AND the method name
    matches a "wishful prose" verb phrase (do_the_thing / solve_problem /
    figure_it_out / plan_and_execute / handle_request / answer_question).
    """
    # If the fragment imports any well-known third-party SDK, the receiver
    # is almost certainly a real client and we should NOT flag.
    KNOWN_LIB_IMPORTS = {
        "openai", "anthropic", "langchain", "langchain_core", "langchain_openai",
        "langchain_anthropic", "langchain_community", "langgraph", "llama_index",
        "llamaindex", "transformers", "datasets", "peft", "trl", "torch",
        "tensorflow", "keras", "sklearn", "numpy", "pandas", "spacy",
        "sentence_transformers", "chromadb", "weaviate", "pinecone", "qdrant_client",
        "faiss", "mlflow", "wandb", "dvc", "fastapi", "pydantic", "instructor",
        "boto3", "google", "vertexai", "cohere", "mistralai", "psycopg2",
        "psycopg", "redis", "requests", "httpx", "aiohttp", "tenacity",
        "ragas", "deepeval", "litellm", "guidance", "outlines", "dspy",
        "unsloth", "bitsandbytes", "accelerate", "evaluate", "tokenizers",
        "huggingface_hub", "arxiv", "wikipedia", "duckduckgo_search",
        "tavily", "serpapi", "tweepy",
    }
    has_known_import = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name.split(".")[0] in KNOWN_LIB_IMPORTS:
                    has_known_import = True
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in KNOWN_LIB_IMPORTS:
                has_known_import = True
    if has_known_import:
        return False

    # Suspicious receivers: a bare local variable that prose treats as "the agent".
    suspicious_receivers = {
        "client", "llm", "agent", "api", "chain", "rag",
    }
    # Wishful-prose verb pattern: handle_the_X, solve_X, do_X_task, ask_X_about_Y.
    WISHFUL_RE = re.compile(
        r"^(?:do_the_|solve_|figure_(?:out|it_)|plan_and_|handle_the_|"
        r"answer_(?:the_|user_)|ask_(?:the_|user_)|think_(?:about_|through_)|"
        r"reason_about_|understand_|interpret_the_|explain_the_|magic_|magically_)"
    )
    invented = 0
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        attr = node.func.attr
        receiver = node.func.value
        recv_name = None
        if isinstance(receiver, ast.Name):
            recv_name = receiver.id
        elif isinstance(receiver, ast.Attribute):
            recv_name = receiver.attr
        if recv_name is None:
            continue
        if recv_name.lower() not in suspicious_receivers:
            continue
        if WISHFUL_RE.match(attr):
            invented += 1
            continue
        if re.search(r"_(?:problem|the_answer|the_question|the_magic|the_thing)$", attr):
            invented += 1
    return invented >= 1


def signal_no_imports_no_calls(tree: ast.AST) -> bool:
    """Module has no imports, no function calls -> just data layout.

    Differentiated from constants_only by allowing class definitions and
    function defs. Useful for catching pure schema files.
    """
    if not isinstance(tree, ast.Module):
        return False
    has_import = any(isinstance(s, (ast.Import, ast.ImportFrom)) for s in ast.walk(tree))
    has_call = any(isinstance(s, ast.Call) for s in ast.walk(tree))
    if has_import or has_call:
        return False
    # And the module has at least one definition (function / class).
    has_def = any(isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                  for s in tree.body)
    has_assign = any(isinstance(s, ast.Assign) for s in tree.body)
    return (has_def or has_assign)


def signal_identity_print_demo(tree: ast.AST, code: str) -> bool:
    """Variable assigned to a literal, then printed unchanged."""
    prints = [n for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
              and n.func.id == "print"]
    if not prints:
        return False
    for p in prints:
        if len(p.args) != 1:
            continue
        arg = p.args[0]
        if not isinstance(arg, ast.Name):
            continue
        name = arg.id
        # The variable assigned to a literal exactly once, never mutated.
        assigns = []
        mutations = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name) and t.id == name:
                        assigns.append(n)
                    if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == name:
                        mutations.append(n)
            if isinstance(n, ast.AugAssign):
                if isinstance(n.target, ast.Name) and n.target.id == name:
                    mutations.append(n)
                if isinstance(n.target, ast.Subscript) and isinstance(n.target.value, ast.Name) and n.target.value.id == name:
                    mutations.append(n)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                if isinstance(n.func.value, ast.Name) and n.func.value.id == name:
                    if n.func.attr in {"append", "extend", "update", "add", "insert", "pop",
                                       "remove", "clear", "setdefault"}:
                        mutations.append(n)
        if len(assigns) == 1 and not mutations:
            v = assigns[0].value
            if isinstance(v, (ast.Constant, ast.Dict, ast.List, ast.Tuple, ast.Set)):
                return True
    return False


def signal_trivial_print_only(tree: ast.AST) -> bool:
    """Only top-level statements are prints of string literals (no logic at all)."""
    if not isinstance(tree, ast.Module):
        return False
    if len(tree.body) < 2:
        return False
    print_only = 0
    others = 0
    for stmt in tree.body:
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            fn = stmt.value.func
            if isinstance(fn, ast.Name) and fn.id == "print":
                if all(isinstance(a, ast.Constant) for a in stmt.value.args):
                    print_only += 1
                    continue
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            continue
        # Docstrings ok.
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            continue
        others += 1
    return print_only >= 2 and others == 0


# ---------- HTML extraction + caption-aware skipping ----------

def normalise_caption(text: str) -> str:
    return re.sub(r"^\s*Code Fragment\s*[\dA-Za-z.]+\s*:\s*", "", text).strip()


def caption_legitimately_minimal(caption: str) -> bool:
    """Captions that label a fragment as intentionally minimal / pedagogy of structure.

    Skip these from the audit -- they are by design.
    """
    pats = [
        r"\bpseudocode\b",
        r"\balgorithm\b\s+\d+",  # "Algorithm 3.2"
        r"\bdata model\b",
        r"\bschema\b",
        r"\bdata class\b",
        r"\binterface\b\s+(?:definition|design)",
        r"\bopenapi\b",
        r"\bjson\s+schema\b",
        r"\btype hints?\b",
        r"\bsignature\b\s+(?:design|definition)",
        r"\bcontracts?\b",
        r"\b(?:public|library)\s+api\b",
        r"^Code Fragment .*?:\s*Configuration\b",
        r"^Code Fragment .*?:\s*Settings\b",
        r"^Code Fragment .*?:\s*Constants\b",
        # Chat templates / prompt formats are themselves the lesson; the rendering
        # almost always lives in the immediately-following fragment.
        r"\bchat (?:template|format)\b",
        r"\bprompt (?:template|format|comparison)\b",
        r"\bvague\s+vs\.?\s+specific\b",
        r"\bcomparing .* prompts?\b",
        r"\bzero-shot (?:prompt|template)\b",
        # System prompts presented as a definition.
        r"\bsystem prompt\b\s+(?:definition|design|template)",
        # "Conceptual" / "architecture" diagrams expressed in code.
        r"\bconceptual\s+(?:pipeline|architecture|design|sketch)\b",
        r"\barchitecture\s+(?:sketch|diagram)\b",
        # Few-shot prompt patterns -- the data IS the lesson.
        r"\bfew-shot\s+(?:classification|prompt|example)\b",
    ]
    for p in pats:
        if re.search(p, caption, re.I):
            return True
    # Captions claiming validators / Field(...) constraints / OpenAPI: the lesson IS the schema.
    if re.search(r"\bField\s*\(", caption):
        return True
    if re.search(r"\bvalidator\b", caption, re.I):
        return True
    return False


def extract_python_code(pre_node) -> str:
    return pre_node.get_text("", strip=False)


def find_fragment_id_from_caption(caption_text: str) -> Optional[str]:
    m = re.search(r"Code Fragment\s*([\d.A-Za-z]+)", caption_text)
    return m.group(1).rstrip(".") if m else None


def _line_of(tag, text: str) -> int:
    s = str(tag)[:120]
    idx = text.find(s)
    if idx < 0:
        s = str(tag)[:60]
        idx = text.find(s)
    if idx < 0:
        return 0
    return text.count("\n", 0, idx) + 1


_STOP = {
    "the", "and", "for", "with", "from", "this", "that", "code", "fragment",
    "use", "using", "import", "via", "into", "implementation",
    "library", "shows", "example", "shortcut", "snippet", "demonstrates",
    "function", "method", "class", "model", "data", "create", "build",
    "definition",
}


def _code_signature(pre) -> set[str]:
    code = pre.get_text("", strip=False)
    head = code[:200]
    tokens = re.findall(r"[A-Za-z][A-Za-z_0-9]{2,}", head.lower())
    return {t for t in tokens if t not in _STOP}


def _caption_signature(cap) -> set[str]:
    text = cap.get_text(" ", strip=True)
    text = re.sub(r"^\s*Code Fragment\s*[\dA-Za-z.]+\s*:\s*", "", text)
    tokens = re.findall(r"[A-Za-z][A-Za-z_0-9]{2,}", text.lower())
    return {t for t in tokens if t not in _STOP}


def _overlap_score(a: set[str], b: set[str]) -> int:
    return len(a & b)


def iter_fragments_in_html(html_path: Path):
    """Yield (line, caption_div, code_pre) for each python fragment with a caption."""
    try:
        text = html_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    pres = []
    for pre in soup.find_all("pre"):
        code_tag = pre.find("code")
        cls_list = (code_tag.get("class") if code_tag else pre.get("class")) or []
        cls = " ".join(cls_list) if isinstance(cls_list, list) else str(cls_list)
        if "python" in cls.lower():
            pres.append(pre)
    captions = soup.find_all("div", class_="code-caption")
    pre_lines = {id(p): _line_of(p, text) for p in pres}
    cap_lines = {id(c): _line_of(c, text) for c in captions}
    pre_sorted = sorted(pres, key=lambda p: pre_lines[id(p)])
    cap_sorted = sorted(captions, key=lambda c: cap_lines[id(c)])

    pre_sigs = [(_code_signature(pre), pre) for pre in pre_sorted]
    cap_sigs = [(_caption_signature(cap), cap) for cap in cap_sorted]

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


# ---------- Parsing ----------

def _parse_or_recover(code: str) -> Optional[ast.AST]:
    try:
        return ast.parse(code)
    except SyntaxError:
        pass
    try:
        indented = "\n".join("    " + line for line in code.splitlines())
        return ast.parse(f"def __wrapped():\n{indented}\n    pass\n")
    except SyntaxError:
        pass
    try:
        import textwrap
        return ast.parse(textwrap.dedent(code))
    except SyntaxError:
        return None


# ---------- Scoring ----------

def score_fragment(code: str, caption: str) -> dict:
    signals = {k: False for k in SIGNAL_WEIGHT}
    tree = _parse_or_recover(code)
    if tree is None:
        return signals

    signals["pure_data_block"] = signal_pure_data_block(tree, code)
    signals["constants_only"] = signal_constants_only(tree)
    signals["string_template_only"] = signal_string_template_only(tree, code)
    signals["identity_print_demo"] = signal_identity_print_demo(tree, code)
    signals["mock_or_fake_api"] = signal_mock_or_fake_api(tree, code)
    signals["wrapper_without_impl"] = signal_wrapper_without_impl(tree)
    signals["pseudo_api_block"] = signal_pseudo_api_block(tree, code)
    signals["no_imports_no_calls"] = signal_no_imports_no_calls(tree)
    signals["trivial_print_only"] = signal_trivial_print_only(tree)
    return signals


# ---------- Rewrite sketch generator ----------

def propose_rewrite(f: FragmentFinding) -> str:
    """Return a 3-6 sentence rewrite sketch tailored to signals and caption."""
    s = set(f.top_signals)
    cap_lower = f.caption.lower()
    parts: list[str] = []

    # Choose library/topic from caption keywords.
    library_hint = _pick_library_from_caption(cap_lower)

    if "mock_or_fake_api" in s:
        parts.append(
            "Replace the canned response with a real call. Use the `openai` Python "
            "SDK (`client.chat.completions.create(model='gpt-4o-mini', messages=[...])`) "
            "or `anthropic` (`client.messages.create(model='claude-3-5-sonnet', "
            "max_tokens=512, messages=[...])`). Show the actual response object the "
            "reader will see in their terminal, so they recognise the shape (`.choices[0]"
            ".message.content` or `.content[0].text`)."
        )
        parts.append(
            "Lesson: how a real LLM call looks at the SDK layer and what fields the "
            "response carries (usage tokens, finish_reason, model id)."
        )
    if "pure_data_block" in s:
        parts.append(
            f"Pair the schema with one runnable validation example. Construct the "
            f"model from a realistic payload (e.g. an OpenAI tool-call argument or a "
            f"chat-completion response), then catch a `ValidationError` on a deliberate "
            f"bad payload. Print the `.errors()` list so the reader sees what Pydantic "
            f"actually emits."
        )
        parts.append(
            "Lesson: Pydantic is more than typing -- it raises actionable errors at "
            "the boundary between an LLM's free-form output and the rest of your code."
        )
    if "constants_only" in s:
        parts.append(
            "Inline the constants in prose (a short table or a sentence each) and "
            "keep the code block for something that USES them: load them with "
            "`pydantic_settings.BaseSettings` from environment, demonstrate "
            "`os.getenv()` with a sane default, or show how they feed into a real "
            "client constructor."
        )
        parts.append(
            "Lesson: configuration is interesting when it's wired into something; "
            "in isolation it's just data."
        )
    if "string_template_only" in s:
        parts.append(
            "Pair the template with a render+call. Use `langchain_core.prompts."
            "ChatPromptTemplate.from_messages(...).invoke({...})` (or python's "
            "`.format(**vars)`), then ship the rendered messages to "
            "`client.chat.completions.create(...)` and print the model's reply. "
            "Show both the template AND the resulting LLM output side by side."
        )
        parts.append(
            "Lesson: templates are abstract until you see what they produce; the "
            "reader needs to see one filled-in instance and its response."
        )
    if "wrapper_without_impl" in s:
        parts.append(
            "Either delete the wrapper and use the underlying client directly, or "
            "add concrete behaviour to the wrapper -- e.g. caching with `functools."
            "lru_cache`, retries via `tenacity.retry(stop=stop_after_attempt(5), "
            "wait=wait_exponential())`, or request logging that prints token usage. "
            "Showing the wrapper without a reason is just indirection."
        )
        parts.append(
            "Lesson: a wrapper earns its place when it adds caching, retries, "
            "telemetry, or contract checks -- not when it merely re-exposes the "
            "delegate's methods."
        )
    if "pseudo_api_block" in s:
        parts.append(
            "Replace invented method names with the real SDK shape for the named "
            "library. If the chapter is about LangChain agents, show "
            "`AgentExecutor(agent=agent, tools=tools).invoke({'input': '...'})`; "
            "for OpenAI tool use, show `client.chat.completions.create(tools=[...])` "
            "and the `tool_calls` list in the response."
        )
        parts.append(
            "Lesson: when readers paste the code into a REPL it MUST work; invented "
            "methods like `agent.solve_problem(...)` quietly teach a wrong API "
            "surface."
        )
    if "identity_print_demo" in s:
        parts.append(
            "Pick an input the reader can transform: e.g., tokenise a sentence with "
            "`transformers.AutoTokenizer.from_pretrained('gpt2').encode('...')` "
            "and print BOTH the original string AND the token-id list. Make the "
            "before/after asymmetric so the reader sees the work."
        )
        parts.append(
            "Lesson: a demo earns its place by showing a transformation, not by "
            "echoing its inputs."
        )
    if "no_imports_no_calls" in s and not parts:
        parts.append(
            "Wire the fragment into something live. Add `import` lines for the "
            "library it conceptually demonstrates, and add at least one call that "
            "exercises a public method against realistic data."
        )
    if "trivial_print_only" in s and not parts:
        parts.append(
            "Replace `print('Hello, world')` style filler with a real computation "
            "whose printed result depends on inputs. For an LLM book, that often "
            "means a tokeniser, an embedding, an API call, or a numpy/pandas "
            "transformation."
        )
    if not parts:
        parts.append(
            "Rewrite so the code performs a real computation or makes a real "
            "library call -- not a data layout the reader could have inferred from "
            "prose."
        )

    if library_hint:
        parts.append(f"Suggested library/API: **{library_hint}**.")

    return " ".join(parts)


_LIB_HINT_MAP = [
    (r"\bopenai\b", "openai (chat.completions.create)"),
    (r"\banthropic\b|\bclaude\b", "anthropic (messages.create)"),
    (r"\bpydantic\b", "pydantic (BaseModel + ValidationError)"),
    (r"\blangchain\b", "langchain_core (ChatPromptTemplate + Runnable.invoke)"),
    (r"\bllamaindex\b|\bllama[- ]index\b", "llama_index (VectorStoreIndex.from_documents)"),
    (r"\bhugging[- ]?face\b|\btransformers\b", "transformers (AutoTokenizer / AutoModel.from_pretrained)"),
    (r"\bsentence[- ]?transformer", "sentence_transformers (SentenceTransformer.encode)"),
    (r"\bnumpy\b", "numpy (linalg, einsum, broadcasting)"),
    (r"\bpandas\b", "pandas (DataFrame transforms)"),
    (r"\bsklearn\b|\bscikit[- ]learn\b", "scikit-learn (cross_val_score, ColumnTransformer)"),
    (r"\bpytorch\b|\btorch\b", "torch (nn.Module + autograd)"),
    (r"\btensorflow\b|\bkeras\b", "tensorflow / keras"),
    (r"\bfastapi\b", "fastapi (App + Pydantic request model)"),
    (r"\btenacity\b|\bretry\b|\bbackoff\b", "tenacity (@retry with wait_exponential)"),
    (r"\bchromadb\b|\bchroma\b", "chromadb (collection.add + query)"),
    (r"\bweaviate\b", "weaviate (client.collections.create)"),
    (r"\bpinecone\b", "pinecone (Index.upsert + query)"),
    (r"\bqdrant\b", "qdrant-client (upsert + search)"),
    (r"\bfaiss\b", "faiss (IndexFlatL2 + .add + .search)"),
    (r"\bmlflow\b", "mlflow (start_run + log_metric + log_param)"),
    (r"\bwandb\b|\bweights ?& ?biases\b", "wandb (wandb.init + wandb.log)"),
    (r"\bdvc\b", "dvc (dvc add + dvc.api.read)"),
    (r"\bopenllmetry\b|\bopentelemetry\b", "opentelemetry / traceloop SDK"),
    (r"\btrl\b|\bppo\b|\bdpo\b", "trl (SFTTrainer, DPOTrainer)"),
    (r"\bpeft\b|\blora\b", "peft (LoraConfig + get_peft_model)"),
    (r"\bdatasets\b", "datasets (load_dataset + map + filter)"),
    (r"\bspacy\b", "spacy (en_core_web_sm pipeline)"),
    (r"\bgithub\b\s+api", "requests + GitHub REST API"),
    (r"\barxiv\b", "arxiv (Search + Result)"),
    (r"\bredis\b", "redis-py (Redis.set / Redis.get)"),
]


def _pick_library_from_caption(cap_lower: str) -> Optional[str]:
    for pat, hint in _LIB_HINT_MAP:
        if re.search(pat, cap_lower):
            return hint
    return None


# ---------- Main ----------

def main() -> int:
    html_files: list[Path] = []
    for path in PROJECT_ROOT.rglob("*.html"):
        if is_excluded(path.relative_to(PROJECT_ROOT)):
            continue
        html_files.append(path)
    print(f"Scanning {len(html_files)} HTML files...", file=sys.stderr)

    findings: list[FragmentFinding] = []
    fragments_total = 0
    parse_errors = 0
    skipped_legitimate = 0

    for html_path in html_files:
        for line, caption_div, code_pre in iter_fragments_in_html(html_path):
            fragments_total += 1
            caption_text = caption_div.get_text(" ", strip=True)
            caption_norm = normalise_caption(caption_text)
            code = extract_python_code(code_pre)

            # Skip captions that legitimately describe data-only or schema-only content.
            if caption_legitimately_minimal(caption_norm):
                skipped_legitimate += 1
                continue

            tree_check = _parse_or_recover(code)
            if tree_check is None:
                parse_errors += 1
                continue

            signals = score_fragment(code, caption_norm)
            score_pts = sum(SIGNAL_WEIGHT[k] for k, v in signals.items() if v)
            triggered = sum(1 for v in signals.values() if v)

            # Threshold: at least one strong signal (mock_or_fake_api / wrapper / pure_data
            # / constants_only / string_template_only / pseudo_api) OR weighted score >= 3.
            heavy = bool(signals["mock_or_fake_api"] or signals["wrapper_without_impl"]
                         or signals["pure_data_block"] or signals["constants_only"]
                         or signals["pseudo_api_block"]
                         or signals["string_template_only"])
            if not (heavy or score_pts >= 4 or triggered >= 2):
                continue

            findings.append(FragmentFinding(
                file=html_path.relative_to(PROJECT_ROOT),
                line=line,
                fragment_id=find_fragment_id_from_caption(caption_text),
                caption=caption_norm,
                code=code,
                signals={k: True for k, v in signals.items() if v},
            ))

    print(
        f"Scanned {fragments_total} python fragments; "
        f"skipped {skipped_legitimate} legit (schema/data-model captions); "
        f"{parse_errors} parse errors; flagged {len(findings)}",
        file=sys.stderr,
    )
    write_report(findings, fragments_total, skipped_legitimate, parse_errors)
    return 0


# ---------- Report writer ----------

def write_report(findings: list[FragmentFinding], total: int,
                 skipped: int, parse_errs: int) -> None:
    findings.sort(key=lambda f: (f.score, f.signal_count, str(f.file)), reverse=True)

    signal_counts: Counter = Counter()
    for f in findings:
        for k in f.signals:
            signal_counts[k] += 1

    lines: list[str] = []
    lines.append("# Code-Fragment Value Audit")
    lines.append("")
    lines.append("Generated by `scripts/_audit_code_value.py`.")
    lines.append("")
    lines.append(
        "This audit flags Python code fragments that add no pedagogical or technical "
        "value: pure-data schemas with no behaviour, constants-only blocks, "
        "string-template-only assignments, identity-print demos, mock/fake API "
        "functions returning canned responses, pure-delegation wrappers, and "
        "pseudo-API blocks using invented method names."
    )
    lines.append("")
    lines.append(
        "Each fragment is scored across nine value signals. A fragment is flagged "
        "when it matches at least one strong no-value pattern (e.g. mock/fake API), "
        "reaches a weighted score of 4, or trips two or more signals."
    )
    lines.append("")
    lines.append(f"- Total Python fragments scanned: **{total}**")
    lines.append(f"- Fragments skipped (captions legitimately describe schemas / data models): **{skipped}**")
    lines.append(f"- Fragments with parse errors (excluded): **{parse_errs}**")
    lines.append(f"- Fragments flagged as low-value: **{len(findings)}**")
    lines.append("")
    lines.append(
        "**Calibration note:** This audit is intentionally conservative. The initial "
        "loose-threshold run produced 46 candidates, of which ~40 were false positives "
        "from real PEFT/transformers code where the detector misjudged method names like "
        "`load_adapter`, `get_or_create_collection`, `search_by_metadata` as 'invented' "
        "(they are real third-party SDK methods). The tightened rules require either an "
        "explicit mock/fake function or a fragment with imports of zero known libraries "
        "AND an English-sentence-shaped method name (e.g. `solve_the_problem`)."
    )
    lines.append("")
    lines.append(
        f"**Parse-error caveat:** {parse_errs} fragments failed AST parsing (typically "
        "due to broken indentation in fragment extraction) and were excluded. Most are "
        "high-value implementation code (federated LoRA, bootstrap tests, etc.) but a "
        "few could harbour low-value patterns the audit cannot reach. The "
        "`code-fragment-fix-report.md` and `missing-imports-audit.md` cover related "
        "issues in those fragments."
    )
    lines.append("")
    lines.append("## Signal weights (higher = stronger signal of no-value)")
    lines.append("")
    for k, w in sorted(SIGNAL_WEIGHT.items(), key=lambda kv: -kv[1]):
        lines.append(f"- `{k}` (weight {w})")
    lines.append("")
    lines.append("## Signal frequency across flagged fragments")
    lines.append("")
    if signal_counts:
        for sig, count in signal_counts.most_common():
            lines.append(f"- `{sig}`: {count}")
    else:
        lines.append("_None_")
    lines.append("")

    # -------- Top 30 worst offenders --------
    lines.append("## Top 30 Worst Offenders")
    lines.append("")
    lines.append("Sorted by weighted score (sum of signal weights), then by number of signals tripped.")
    lines.append("")
    lines.append(
        "| # | File | Line | Fragment | Score | # signals | Top signals | Caption (truncated) |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")
    for i, f in enumerate(findings[:30], 1):
        top = f.top_signals[:2]
        sig_str = ", ".join(f"`{s}`" for s in top) if top else "-"
        cap = f.caption[:90].replace("|", "\\|").replace("\n", " ")
        if len(f.caption) > 90:
            cap += "..."
        frag_id = f.fragment_id or "-"
        lines.append(
            f"| {i} | `{f.file.as_posix()}` | {f.line} | {frag_id} | "
            f"{f.score} | {f.signal_count} | {sig_str} | {cap} |"
        )
    lines.append("")

    # -------- Full rewrite sketches for top 10 --------
    lines.append("## Rewrite Sketches (Top 10)")
    lines.append("")
    for i, f in enumerate(findings[:10], 1):
        lines.append(f"### {i}. `{f.file.as_posix()}` (Code Fragment {f.fragment_id or '-'}, line {f.line})")
        lines.append("")
        lines.append(f"**Caption:** {f.caption}")
        lines.append("")
        lines.append(f"**Signals tripped:** {', '.join(f.signals.keys())} (score: {f.score})")
        lines.append("")
        snippet = f.code.strip().splitlines()[:14]
        lines.append("```python")
        lines.extend(snippet)
        if len(f.code.strip().splitlines()) > 14:
            lines.append("# ... (truncated)")
        lines.append("```")
        lines.append("")
        # Effort estimate.
        if any(k in f.signals for k in ("pure_data_block", "constants_only", "no_imports_no_calls")):
            effort = "S"  # mostly add a runnable example
        elif "mock_or_fake_api" in f.signals or "pseudo_api_block" in f.signals:
            effort = "M"  # need to wire to a real SDK
        elif "wrapper_without_impl" in f.signals:
            effort = "M"
        elif "string_template_only" in f.signals:
            effort = "S"
        else:
            effort = "XS"
        lines.append(f"**Rewrite sketch (effort {effort}):** {propose_rewrite(f)}")
        lines.append("")

    # -------- Recommended priority --------
    lines.append("## Recommended Editorial Priority")
    lines.append("")
    # Group findings by part folder for prioritisation.
    by_part: dict[str, list[FragmentFinding]] = {}
    for f in findings:
        first = f.file.parts[0] if f.file.parts else "(root)"
        by_part.setdefault(first, []).append(f)
    lines.append("Findings by top-level folder (sorted by count):")
    lines.append("")
    lines.append("| Folder | Flagged | Highest-score example |")
    lines.append("|---|---|---|")
    for folder, items in sorted(by_part.items(), key=lambda kv: -len(kv[1])):
        top = max(items, key=lambda f: f.score)
        example = f"Fragment {top.fragment_id or '-'} ({top.score} pts)"
        lines.append(f"| `{folder}` | {len(items)} | {example} |")
    lines.append("")
    lines.append("**Priority guidance:**")
    lines.append("")
    lines.append(
        "1. **Fix `mock_or_fake_api` first.** A function that returns a hard-coded "
        "string named `call_llm` actively teaches the wrong mental model -- readers "
        "leave with an API shape that does not exist."
    )
    lines.append("")
    lines.append(
        "2. **Then `pseudo_api_block`.** Invented method names compile but fail at "
        "the REPL; this destroys trust in the entire chapter."
    )
    lines.append("")
    lines.append(
        "3. **Then `pure_data_block` and `constants_only`.** These are pedagogically "
        "soft but waste page-budget. Move the data into prose and reclaim the "
        "code block for a runnable example."
    )
    lines.append("")
    lines.append(
        "4. **Defer `wrapper_without_impl` and `string_template_only`.** These are "
        "structural smells; rewriting them often requires changes to adjacent "
        "fragments and prose, so batch them per-section."
    )
    lines.append("")
    lines.append(
        "5. **Treat `identity_print_demo` and `trivial_print_only` as last-pass "
        "polish.** They are not actively misleading; they just don't earn their "
        "page-budget."
    )
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report to {REPORT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
