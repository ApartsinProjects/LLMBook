"""
Audit stale / deprecated API patterns in Python code fragments across the LLMBook.

For each <pre><code class="...lang-python..."> fragment we scan for stale patterns
where the SDK or framework has shipped a breaking-change migration:

  - OpenAI Python SDK pre-1.0 (openai.ChatCompletion.create, openai.Completion.create,
    `from openai import ChatCompletion`, openai.api_key = ...)
  - Pydantic v1 method names (parse_obj, dict(), json(), inner `class Config:`)
  - LangChain pre-0.3 imports (from langchain.chat_models import ChatOpenAI,
    from langchain.embeddings import OpenAIEmbeddings, top-level `from langchain import ...`)
  - LangChain Runnable pre-LCEL style (LLMChain class, agent_executor.run(...))
  - PyTorch model.save() with the full pickle (torch.save(model, ...)) and
    torch.load(..., weights_only=False) explicit opt-out (or implicit default
    pre-2.6)
  - Anthropic SDK pre-1.0 (`from anthropic import Client`)
  - huggingface_hub.snapshot_download(token=...) kwarg
  - transformers.pipeline(task=...) with deprecated task names

For each match we emit (file, line, snippet, suggested migration, confidence).

Confidence buckets:
  - high   = pattern is the literal stale API; migration is mechanical.
  - medium = pattern is ambiguous (e.g. `.dict()` on something that may not be a
             Pydantic model) and needs human eyes.
  - low    = the surrounding caption suggests the snippet is illustrating the OLD
             pattern on purpose (e.g. "before openai v1.0", "Pydantic v1 syntax"),
             so the migration may not be wanted.

Output: stale-api-audit.md (summary + buckets + recommended next steps).
"""

from __future__ import annotations

import ast
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

# Resolve project root relative to this script (scripts/_audit_stale_apis.py).
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORT_PATH = PROJECT_ROOT / "stale-api-audit.md"

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


# ----------- Pattern definitions ----------------------------------------------

@dataclass
class Pattern:
    """A stale-API pattern, with detection regex and migration string."""
    key: str                 # short stable id used in summary tables
    title: str               # human-readable name for the report
    regex: re.Pattern        # what to detect in the fragment source text
    migration: str           # one-line replacement guidance
    confidence: str          # baseline: high / medium / low
    legacy_label: str = ""   # short snippet description ("openai.ChatCompletion.create")


# Each regex is anchored to a fragment-level token. We treat the code as plain
# text rather than parsed AST because many fragments don't parse cleanly.

PATTERNS: list[Pattern] = [
    # OpenAI SDK v0 -> v1
    Pattern(
        key="openai_chatcompletion_create",
        title="openai.ChatCompletion.create",
        regex=re.compile(r"\bopenai\.ChatCompletion\.create\s*\("),
        migration=(
            "openai v1.x: `from openai import OpenAI; client = OpenAI(); "
            "client.chat.completions.create(...)`"
        ),
        confidence="high",
        legacy_label="openai.ChatCompletion.create(...)",
    ),
    Pattern(
        key="openai_completion_create",
        title="openai.Completion.create",
        regex=re.compile(r"\bopenai\.Completion\.create\s*\("),
        migration=(
            "openai v1.x: use `client.chat.completions.create(...)` for chat "
            "models, or `client.completions.create(...)` for instruct models. "
            "The bare `openai.Completion.create` endpoint is legacy."
        ),
        confidence="high",
        legacy_label="openai.Completion.create(...)",
    ),
    Pattern(
        key="openai_embedding_create",
        title="openai.Embedding.create",
        regex=re.compile(r"\bopenai\.Embedding\.create\s*\("),
        migration=(
            "openai v1.x: `from openai import OpenAI; client = OpenAI(); "
            "client.embeddings.create(...)`"
        ),
        confidence="high",
        legacy_label="openai.Embedding.create(...)",
    ),
    Pattern(
        key="openai_moderation_create",
        title="openai.Moderation.create",
        regex=re.compile(r"\bopenai\.Moderation\.create\s*\("),
        migration=(
            "openai v1.x: `client.moderations.create(...)` on an `OpenAI()` client."
        ),
        confidence="high",
        legacy_label="openai.Moderation.create(...)",
    ),
    Pattern(
        key="openai_audio_legacy",
        title="openai.Audio.transcribe / .translate",
        regex=re.compile(r"\bopenai\.Audio\.(transcribe|translate)\s*\("),
        migration=(
            "openai v1.x: `client.audio.transcriptions.create(...)` / "
            "`client.audio.translations.create(...)`."
        ),
        confidence="high",
        legacy_label="openai.Audio.transcribe(...)",
    ),
    Pattern(
        key="openai_image_create",
        title="openai.Image.create",
        regex=re.compile(r"\bopenai\.Image\.create\s*\("),
        migration=(
            "openai v1.x: `client.images.generate(...)`."
        ),
        confidence="high",
        legacy_label="openai.Image.create(...)",
    ),
    Pattern(
        key="openai_file_legacy",
        title="openai.File.create / list",
        regex=re.compile(r"\bopenai\.File\.(create|list|retrieve|delete)\s*\("),
        migration=(
            "openai v1.x: `client.files.create(...)`, `client.files.list()`, etc."
        ),
        confidence="high",
        legacy_label="openai.File.create(...)",
    ),
    Pattern(
        key="from_openai_chatcompletion",
        title="from openai import ChatCompletion",
        regex=re.compile(
            r"^\s*from\s+openai\s+import\s+[^\n]*\bChatCompletion\b",
            re.M,
        ),
        migration=(
            "openai v1.x: `from openai import OpenAI` and call "
            "`OpenAI().chat.completions.create(...)`."
        ),
        confidence="high",
        legacy_label="from openai import ChatCompletion",
    ),
    Pattern(
        key="openai_api_key_attr",
        title="openai.api_key = '...'",
        regex=re.compile(r"\bopenai\.api_key\s*="),
        migration=(
            "openai v1.x: pass at construction (`OpenAI(api_key=...)`) or set "
            "the `OPENAI_API_KEY` env var; do not set `openai.api_key` "
            "module-level."
        ),
        confidence="high",
        legacy_label='openai.api_key = "..."',
    ),
    Pattern(
        key="openai_organization_attr",
        title="openai.organization = '...'",
        regex=re.compile(r"\bopenai\.organization\s*="),
        migration=(
            "openai v1.x: `OpenAI(organization=...)` at construction."
        ),
        confidence="high",
        legacy_label='openai.organization = "..."',
    ),

    # Pydantic v1 -> v2
    Pattern(
        key="pydantic_parse_obj",
        title="BaseModel.parse_obj(...)",
        regex=re.compile(r"\.parse_obj\s*\("),
        migration=(
            "Pydantic v2: `Model.model_validate(...)`. (`.parse_obj` removed in v3.)"
        ),
        confidence="medium",  # could be a non-Pydantic class
        legacy_label=".parse_obj(...)",
    ),
    Pattern(
        key="pydantic_parse_raw",
        title="BaseModel.parse_raw(...)",
        regex=re.compile(r"\.parse_raw\s*\("),
        migration=(
            "Pydantic v2: `Model.model_validate_json(...)`."
        ),
        confidence="medium",
        legacy_label=".parse_raw(...)",
    ),
    Pattern(
        key="pydantic_parse_file",
        title="BaseModel.parse_file(...)",
        regex=re.compile(r"\.parse_file\s*\("),
        migration=(
            "Pydantic v2: removed; read the file and call "
            "`Model.model_validate_json(text)`."
        ),
        confidence="medium",
        legacy_label=".parse_file(...)",
    ),
    Pattern(
        key="pydantic_dict_call",
        title="<model>.dict() (Pydantic v1)",
        # Only flag .dict() with no args -- the AST gate below filters out
        # generic uses on a `dict()` constructor.
        regex=re.compile(r"\.dict\s*\(\s*\)"),
        migration=(
            "Pydantic v2: `instance.model_dump()`. `BaseModel.dict()` is deprecated."
        ),
        confidence="medium",
        legacy_label=".dict()",
    ),
    Pattern(
        key="pydantic_json_call",
        title="<model>.json() (Pydantic v1)",
        regex=re.compile(r"\.json\s*\(\s*\)"),
        migration=(
            "Pydantic v2: `instance.model_dump_json()`. `BaseModel.json()` is "
            "deprecated (note `requests.Response.json()` is unrelated)."
        ),
        confidence="medium",  # heavy false-positive risk; AST gate refines
        legacy_label=".json()",
    ),
    Pattern(
        key="pydantic_inner_config",
        title="class Config: (inner)",
        # match an inner `class Config:` block; we'll gate by pydantic context.
        regex=re.compile(r"^\s*class\s+Config\s*:\s*$", re.M),
        migration=(
            "Pydantic v2: replace inner `class Config:` with "
            "`model_config = ConfigDict(...)`."
        ),
        confidence="medium",
        legacy_label="class Config:",
    ),
    Pattern(
        key="pydantic_validator_v1",
        title="@validator(...) (Pydantic v1)",
        regex=re.compile(r"@validator\s*\("),
        migration=(
            "Pydantic v2: `@field_validator(...)` (per-field) or "
            "`@model_validator(...)` (whole-model)."
        ),
        confidence="medium",
        legacy_label="@validator(...)",
    ),

    # LangChain pre-0.3 split
    Pattern(
        key="lc_chatmodels_openai",
        title="from langchain.chat_models import ChatOpenAI",
        regex=re.compile(
            r"^\s*from\s+langchain\.chat_models\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_openai import ChatOpenAI` "
            "(or the appropriate provider package)."
        ),
        confidence="high",
        legacy_label="from langchain.chat_models import ...",
    ),
    Pattern(
        key="lc_embeddings_openai",
        title="from langchain.embeddings import OpenAIEmbeddings",
        regex=re.compile(
            r"^\s*from\s+langchain\.embeddings\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_openai import OpenAIEmbeddings` "
            "(or the appropriate provider package)."
        ),
        confidence="high",
        legacy_label="from langchain.embeddings import ...",
    ),
    Pattern(
        key="lc_llms_openai",
        title="from langchain.llms import OpenAI/ChatOpenAI",
        regex=re.compile(
            r"^\s*from\s+langchain\.llms\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_openai import OpenAI` (or the "
            "appropriate provider package, e.g. `langchain_anthropic`)."
        ),
        confidence="high",
        legacy_label="from langchain.llms import ...",
    ),
    Pattern(
        key="lc_vectorstores",
        title="from langchain.vectorstores import ...",
        regex=re.compile(
            r"^\s*from\s+langchain\.vectorstores\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_community.vectorstores import ...` "
            "(or the dedicated provider package, e.g. `langchain_chroma`, "
            "`langchain_pinecone`)."
        ),
        confidence="high",
        legacy_label="from langchain.vectorstores import ...",
    ),
    Pattern(
        key="lc_document_loaders",
        title="from langchain.document_loaders import ...",
        regex=re.compile(
            r"^\s*from\s+langchain\.document_loaders\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_community.document_loaders import ...`."
        ),
        confidence="high",
        legacy_label="from langchain.document_loaders import ...",
    ),
    Pattern(
        key="lc_text_splitter",
        title="from langchain.text_splitter import ...",
        regex=re.compile(
            r"^\s*from\s+langchain\.text_splitter\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_text_splitters import ...`."
        ),
        confidence="high",
        legacy_label="from langchain.text_splitter import ...",
    ),
    Pattern(
        key="lc_tools",
        title="from langchain.tools import ...",
        regex=re.compile(
            r"^\s*from\s+langchain\.tools\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_core.tools import ...` or "
            "`from langchain_community.tools import ...` depending on the tool."
        ),
        confidence="medium",
        legacy_label="from langchain.tools import ...",
    ),
    Pattern(
        key="lc_prompts",
        title="from langchain.prompts import ...",
        regex=re.compile(
            r"^\s*from\s+langchain\.prompts\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_core.prompts import ...`."
        ),
        confidence="high",
        legacy_label="from langchain.prompts import ...",
    ),
    Pattern(
        key="lc_schema",
        title="from langchain.schema import ...",
        regex=re.compile(
            r"^\s*from\s+langchain\.schema\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_core.messages import ...` / "
            "`from langchain_core.documents import Document` / "
            "`from langchain_core.outputs import ...`."
        ),
        confidence="high",
        legacy_label="from langchain.schema import ...",
    ),
    Pattern(
        key="lc_callbacks",
        title="from langchain.callbacks import ...",
        regex=re.compile(
            r"^\s*from\s+langchain\.callbacks\s+import\s+", re.M
        ),
        migration=(
            "LangChain 0.3+: `from langchain_core.callbacks import ...` "
            "(or `langchain_community.callbacks` for provider integrations)."
        ),
        confidence="medium",
        legacy_label="from langchain.callbacks import ...",
    ),
    Pattern(
        key="lc_topimport_bare",
        title="from langchain import <symbol>",
        regex=re.compile(
            r"^\s*from\s+langchain\s+import\s+(?!langchain_)([A-Z][A-Za-z_,\s]+)",
            re.M,
        ),
        migration=(
            "LangChain 0.3+: top-level `from langchain import X` is mostly "
            "removed -- use `langchain_core`, `langchain_community`, or a "
            "provider package."
        ),
        confidence="medium",
        legacy_label="from langchain import ...",
    ),
    Pattern(
        key="lc_llmchain",
        title="LLMChain (legacy chains)",
        regex=re.compile(r"\bLLMChain\s*\("),
        migration=(
            "LangChain 0.3+: prefer LCEL (`prompt | llm | StrOutputParser()`). "
            "`LLMChain` is deprecated."
        ),
        confidence="high",
        legacy_label="LLMChain(...)",
    ),
    Pattern(
        key="lc_run_method",
        title="<chain|agent_executor>.run(...)",
        # Only the bare `.run(` of a chain-ish identifier, not random .run().
        regex=re.compile(
            r"\b(chain|agent_executor|qa_chain|conv|conversation)\.run\s*\("
        ),
        migration=(
            "LangChain 0.3+: `.invoke(...)`. The `.run(...)` shortcut is "
            "deprecated on Runnable chains and on AgentExecutor."
        ),
        confidence="medium",
        legacy_label="agent_executor.run(...)",
    ),

    # Anthropic SDK pre-1.0
    Pattern(
        key="anthropic_client_import",
        title="from anthropic import Client",
        regex=re.compile(r"^\s*from\s+anthropic\s+import\s+[^\n]*\bClient\b", re.M),
        migration=(
            "Anthropic v1.x: `from anthropic import Anthropic; client = Anthropic()`. "
            "The bare `Client` symbol is removed in current SDKs."
        ),
        confidence="high",
        legacy_label="from anthropic import Client",
    ),
    Pattern(
        key="anthropic_completion_create",
        title="anthropic.Completion.create",
        regex=re.compile(r"\banthropic\.Completion\.create\s*\("),
        migration=(
            "Anthropic v1.x: `client.messages.create(...)` (the Messages API). "
            "The legacy text-completions endpoint is being retired."
        ),
        confidence="high",
        legacy_label="anthropic.Completion.create(...)",
    ),
    Pattern(
        key="anthropic_client_completions",
        title="client.completions.create (legacy text endpoint)",
        regex=re.compile(r"\bclient\.completions\.create\s*\("),
        migration=(
            "Anthropic v1.x: prefer `client.messages.create(...)` (Messages API); "
            "`client.completions.create(...)` is the legacy text-completions "
            "endpoint."
        ),
        confidence="medium",  # may be intentional in a comparison
        legacy_label="client.completions.create(...)",
    ),

    # PyTorch
    Pattern(
        key="torch_save_full_model",
        title="torch.save(model, ...)",
        regex=re.compile(r"\btorch\.save\s*\(\s*(?:model|net|net_g|m|self\.model)\s*,"),
        migration=(
            "Recommended: `torch.save(model.state_dict(), path)` and reload via "
            "`model.load_state_dict(torch.load(path, weights_only=True))`. "
            "Saving the full module pickles class code and breaks across refactors."
        ),
        confidence="medium",
        legacy_label="torch.save(model, ...)",
    ),
    Pattern(
        key="torch_load_weights_only_false",
        title="torch.load(..., weights_only=False)",
        regex=re.compile(r"\btorch\.load\s*\([^)]*weights_only\s*=\s*False"),
        migration=(
            "PyTorch 2.6+: prefer `weights_only=True` (the new default) for "
            "untrusted checkpoints. Pass False only when you trust the file."
        ),
        confidence="medium",
        legacy_label="torch.load(..., weights_only=False)",
    ),

    # Hugging Face Hub
    Pattern(
        key="hf_token_kwarg",
        title="huggingface_hub.* token= kwarg",
        # Match `snapshot_download(... token=...)`, `hf_hub_download(... token=...)`,
        # and `login(token=...)` -- the modern convention is to set
        # `HUGGINGFACE_HUB_TOKEN` env or use `HfApi(token=...)` at construction.
        regex=re.compile(
            r"\b(snapshot_download|hf_hub_download)\s*\([^)]*\btoken\s*="
        ),
        migration=(
            "Prefer the `HUGGINGFACE_HUB_TOKEN` env var or `HfApi(token=...)` at "
            "construction. The per-call `token=` kwarg still works but the env "
            "var is the canonical setup."
        ),
        confidence="low",  # kwarg still supported; this is a style migration
        legacy_label="snapshot_download(token=...)",
    ),

    # transformers pipeline deprecated tasks
    Pattern(
        key="transformers_deprecated_task",
        title="transformers.pipeline(task=<deprecated>)",
        # task names that were renamed: sentiment-analysis -> text-classification
        # (alias still works but is the legacy one)
        regex=re.compile(
            r"\bpipeline\s*\(\s*(?:task\s*=\s*)?[\"'](sentiment-analysis|ner|"
            r"text2text-generation|conversational)[\"']"
        ),
        migration=(
            "transformers: `sentiment-analysis` -> `text-classification`; "
            "`ner` -> `token-classification`; `conversational` is removed in "
            "transformers 4.42+. Use the chat-template API on the model directly."
        ),
        confidence="medium",
        legacy_label="pipeline('sentiment-analysis' / 'ner' / ...)",
    ),
]

# Patterns indexed by key for the report writer.
PATTERN_BY_KEY = {p.key: p for p in PATTERNS}


# ----------- AST gates --------------------------------------------------------
# Several patterns are too broad on raw regex. We gate them on AST analysis to
# decide whether a match is real, or downgrade confidence.

PYDANTIC_HINTS = {
    "BaseModel", "Field", "validator", "field_validator", "model_validator",
    "ConfigDict", "Extra", "root_validator", "pydantic", "from pydantic",
}


def has_pydantic_context(code: str) -> bool:
    """Cheap check: does the fragment look like it's discussing Pydantic models?"""
    return any(h in code for h in PYDANTIC_HINTS)


def has_requests_context(code: str) -> bool:
    """Heuristic: code imports requests or httpx and the .json() may be on a Response."""
    return (
        "import requests" in code or "from requests" in code
        or "import httpx" in code or "from httpx" in code
        or "response.json" in code or ".get(" in code or ".post(" in code
    )


def has_response_json_call(code: str) -> bool:
    """Match common `<resp>.json()` idioms that are NOT Pydantic.

    Catches both bare names (`response.json()`, `resp.json()`) and suffixed
    forms (`meta_resp.json()`, `auth_response.json()`) since the latter are
    the most common naming convention in real code.
    """
    return bool(re.search(
        r"(?:^|[^A-Za-z_])([A-Za-z_]*(?:response|resp|reply)|r|res|completion)\.json\s*\(\s*\)",
        code,
    ))


def looks_like_pydantic_class_with_inner_config(code: str) -> bool:
    """Does the fragment contain `class X(BaseModel)` followed eventually by `class Config:`?"""
    if "class Config" not in code:
        return False
    if "BaseModel" not in code and "pydantic" not in code:
        return False
    # Try AST; fall back to text check.
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "BaseModel" in code
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        bases_str = " ".join(_dump(b) for b in node.bases)
        if "BaseModel" not in bases_str and "Pydantic" not in bases_str:
            continue
        # Look for inner `class Config:`.
        for inner in node.body:
            if isinstance(inner, ast.ClassDef) and inner.name == "Config":
                return True
    return False


def _dump(node) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        try:
            return ast.dump(node)
        except Exception:
            return ""


# ----------- HTML extraction --------------------------------------------------

def iter_python_fragments(html_path: Path):
    """Yield (line_number, code_text) for each <pre><code class=...python...>."""
    try:
        text = html_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    for pre in soup.find_all("pre"):
        code_tag = pre.find("code")
        cls_list = (code_tag.get("class") if code_tag else pre.get("class")) or []
        cls = " ".join(cls_list) if isinstance(cls_list, list) else str(cls_list)
        if "python" not in cls.lower():
            continue
        code = pre.get_text("", strip=False)
        line = _line_of(pre, text)
        yield line, code


def _line_of(tag, text: str) -> int:
    """Approximate 1-based line number where `tag` appears in `text`."""
    s = str(tag)[:120]
    idx = text.find(s)
    if idx < 0:
        s = str(tag)[:60]
        idx = text.find(s)
    if idx < 0:
        return 0
    return text.count("\n", 0, idx) + 1


def find_nearby_caption(html_path: Path, line: int, window: int = 60) -> str:
    """Read the file and return the caption text near `line` (if any).

    Used only to detect 'intentional old pattern' contexts.
    """
    try:
        text = html_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = html_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    lo = max(0, line - window)
    hi = min(len(lines), line + window)
    blob = "\n".join(lines[lo:hi])
    # Pull out code-caption text if present.
    m = re.search(
        r"<div[^>]+class=[^>]+code-caption[^>]*>(.*?)</div>",
        blob,
        re.DOTALL,
    )
    if m:
        # Strip inner HTML tags.
        cap = re.sub(r"<[^>]+>", " ", m.group(1))
        return re.sub(r"\s+", " ", cap).strip()
    return ""


# ----------- Intentional-old-pattern detection --------------------------------

# When the surrounding caption or section explicitly contrasts old vs new
# (e.g. "Pre-v1 syntax", "Pydantic v1 example", "Before LCEL"), we downgrade
# confidence to low.

INTENTIONAL_OLD_RE = re.compile(
    r"\b(pre[- ]v1|pre[- ]1\.0|v0\.x|v1\.x style|pydantic v1|pydantic 1\.x|"
    r"langchain v0|langchain 0\.[012]|legacy syntax|deprecated example|"
    r"old style|old (?:pattern|api)|before lcel|pre[- ]lcel|"
    r"openai (?:v0|0\.x)|old openai|legacy completions|legacy text endpoint|"
    r"do not (?:do|use) this|antipattern|anti[- ]pattern|wrong way)\b",
    re.I,
)


def is_intentional_old(caption: str, code: str, body_context: str = "") -> bool:
    """Return True if the surrounding text suggests the snippet is illustrating the OLD pattern on purpose."""
    blobs = [caption, body_context]
    for blob in blobs:
        if blob and INTENTIONAL_OLD_RE.search(blob):
            return True
    # Inline comment that calls out "old way" / "deprecated".
    if re.search(r"#\s*(old|deprecated|legacy|don't do this|do not do this|pre[- ]v1)", code, re.I):
        return True
    return False


# ----------- Match record -----------------------------------------------------

@dataclass
class Match:
    file: Path
    line: int
    pattern_key: str
    snippet: str
    confidence: str
    caption: str = ""

    def display_line(self) -> str:
        # The detected snippet may span multiple lines; show first ~120 chars.
        s = self.snippet.strip()
        if len(s) > 120:
            s = s[:117] + "..."
        return s


# ----------- Scoring loop -----------------------------------------------------

def find_matches_in_fragment(
    code: str,
    fragment_line: int,
    file_path: Path,
    caption: str,
) -> list[Match]:
    """Run every pattern against `code`. Returns one Match per hit.

    We apply per-pattern gating to filter false positives or downgrade
    confidence:

      - `.json()` / `.dict()` / `.parse_obj()`: require Pydantic context;
        otherwise drop the match (likely requests.Response.json or
        builtin dict constructor).
      - `class Config:`: require Pydantic context.
      - openai.* legacy: drop matches inside a comment line.
      - All matches in code that visibly looks like a "before/after"
        contrast (intentional old example) get confidence='low'.
    """
    matches: list[Match] = []
    intentional = is_intentional_old(caption, code)

    has_pydantic = has_pydantic_context(code)
    has_response_json = has_response_json_call(code)

    for p in PATTERNS:
        for m in p.regex.finditer(code):
            # Find the line of the match inside the fragment.
            start = m.start()
            # Drop matches that sit inside a Python comment.
            line_start = code.rfind("\n", 0, start) + 1
            line_end = code.find("\n", start)
            if line_end == -1:
                line_end = len(code)
            full_line = code[line_start:line_end]
            stripped = full_line.lstrip()
            if stripped.startswith("#"):
                # Detection inside a comment -- count as low-confidence only
                # if the comment looks like inline documentation of the
                # legacy pattern.
                if not re.search(r"\b(was|used to|previously|deprecated|legacy)\b", full_line, re.I):
                    continue

            # Per-pattern gates -----
            if p.key in {
                "pydantic_parse_obj", "pydantic_parse_raw", "pydantic_parse_file",
                "pydantic_dict_call", "pydantic_json_call",
                "pydantic_validator_v1",
            }:
                if not has_pydantic:
                    # Skip: very high false positive rate without context.
                    continue
                if p.key == "pydantic_json_call" and has_response_json:
                    # Almost certainly response.json() on a requests/httpx Response.
                    # Skip unless we have very strong Pydantic indicators.
                    if "BaseModel" not in code:
                        continue

            if p.key == "pydantic_inner_config":
                if not looks_like_pydantic_class_with_inner_config(code):
                    continue

            # Compute the snippet to display (the full source line, trimmed).
            snippet = full_line.strip()
            if len(snippet) < 4 and line_end < len(code):
                # Include the next line for readability.
                next_line_end = code.find("\n", line_end + 1)
                if next_line_end != -1:
                    snippet = code[line_start:next_line_end].strip()

            # Confidence: pattern baseline, but downgrade if intentional.
            confidence = p.confidence
            if intentional:
                confidence = "low"

            matches.append(Match(
                file=file_path,
                line=fragment_line,
                pattern_key=p.key,
                snippet=snippet,
                confidence=confidence,
                caption=caption[:200],
            ))
    return matches


def main() -> int:
    html_files: list[Path] = []
    for path in PROJECT_ROOT.rglob("*.html"):
        if is_excluded(path.relative_to(PROJECT_ROOT)):
            continue
        html_files.append(path)
    print(f"Scanning {len(html_files)} HTML files...", file=sys.stderr)

    all_matches: list[Match] = []
    fragments_total = 0
    files_with_matches: set[Path] = set()
    for html_path in html_files:
        rel = html_path.relative_to(PROJECT_ROOT)
        for line, code in iter_python_fragments(html_path):
            fragments_total += 1
            caption = find_nearby_caption(html_path, line)
            file_matches = find_matches_in_fragment(code, line, rel, caption)
            if file_matches:
                files_with_matches.add(rel)
                all_matches.extend(file_matches)

    print(
        f"Scanned {fragments_total} python fragments; flagged {len(all_matches)} matches "
        f"across {len(files_with_matches)} files",
        file=sys.stderr,
    )
    write_report(all_matches, fragments_total, len(html_files), len(files_with_matches))
    return 0


# ----------- Report -----------------------------------------------------------

def write_report(
    matches: list[Match],
    total_fragments: int,
    total_files: int,
    files_with_matches: int,
) -> None:
    # Summary by pattern.
    by_pattern: Counter[str] = Counter()
    by_pattern_conf: dict[str, Counter] = defaultdict(Counter)
    for m in matches:
        by_pattern[m.pattern_key] += 1
        by_pattern_conf[m.pattern_key][m.confidence] += 1

    # Bucket by confidence.
    high = [m for m in matches if m.confidence == "high"]
    medium = [m for m in matches if m.confidence == "medium"]
    low = [m for m in matches if m.confidence == "low"]

    # Sort each bucket by (pattern_key, file, line) so similar patterns group.
    for bucket in (high, medium, low):
        bucket.sort(key=lambda m: (m.pattern_key, m.file.as_posix(), m.line))

    lines: list[str] = []
    lines.append("# Stale / Deprecated API Audit")
    lines.append("")
    lines.append(
        "Generated by `scripts/_audit_stale_apis.py`. Read-only scan of every "
        "`<pre><code class='...lang-python...'>` fragment across the LLMBook for "
        "deprecated SDK patterns whose vendors have shipped breaking migrations."
    )
    lines.append("")
    lines.append(
        f"Scanned **{total_files}** HTML files, **{total_fragments}** Python "
        f"fragments. Flagged **{len(matches)}** matches across "
        f"**{files_with_matches}** files."
    )
    lines.append("")
    lines.append(
        "Confidence: **high** = mechanical migration; **medium** = needs human "
        "context (often Pydantic-vs-other-class); **low** = surrounding caption "
        "suggests the snippet shows the OLD pattern on purpose."
    )
    lines.append("")

    # ---- 1. Summary ----
    lines.append("## 1. Summary by Pattern")
    lines.append("")
    lines.append("| Pattern | Title | Total | High | Medium | Low |")
    lines.append("|---|---|---:|---:|---:|---:|")
    # Order: highest-impact stale patterns first.
    pattern_order = [p.key for p in PATTERNS]
    for key in pattern_order:
        n = by_pattern.get(key, 0)
        if n == 0:
            continue
        cc = by_pattern_conf.get(key, Counter())
        title = PATTERN_BY_KEY[key].title
        lines.append(
            f"| `{key}` | {title} | {n} | {cc.get('high', 0)} | "
            f"{cc.get('medium', 0)} | {cc.get('low', 0)} |"
        )
    if not any(by_pattern.values()):
        lines.append("| (none) | No stale patterns detected | 0 | 0 | 0 | 0 |")
    lines.append("")

    lines.append(f"**Totals:** {len(high)} high, {len(medium)} medium, {len(low)} low.")
    lines.append("")

    # ---- 2. High-confidence ----
    lines.append("## 2. High-Confidence Matches (Mechanical Migration)")
    lines.append("")
    if not high:
        lines.append("_None detected._")
        lines.append("")
    else:
        lines.append(
            "These are direct calls into a known-stale SDK API; the migration "
            "is a straightforward text replacement."
        )
        lines.append("")
        lines.append("| # | File | Line | Pattern | Stale snippet | Migration |")
        lines.append("|---|---|---:|---|---|---|")
        for i, m in enumerate(high, 1):
            mig = PATTERN_BY_KEY[m.pattern_key].migration
            snip = m.display_line().replace("|", "\\|")
            mig_disp = mig.replace("|", "\\|")
            lines.append(
                f"| {i} | `{m.file.as_posix()}` | {m.line} | "
                f"`{m.pattern_key}` | `{snip}` | {mig_disp} |"
            )
        lines.append("")

    # ---- 3. Medium-confidence ----
    lines.append("## 3. Medium-Confidence Matches (Need Context)")
    lines.append("")
    if not medium:
        lines.append("_None detected._")
        lines.append("")
    else:
        lines.append(
            "These match the stale pattern textually but the surrounding code "
            "may not be the deprecated library (e.g. `.dict()` could be a "
            "non-Pydantic class; `chain.run()` could be a custom method). "
            "Inspect before bulk-migrating."
        )
        lines.append("")
        lines.append("| # | File | Line | Pattern | Stale snippet | Migration |")
        lines.append("|---|---|---:|---|---|---|")
        for i, m in enumerate(medium, 1):
            mig = PATTERN_BY_KEY[m.pattern_key].migration
            snip = m.display_line().replace("|", "\\|")
            mig_disp = mig.replace("|", "\\|")
            lines.append(
                f"| {i} | `{m.file.as_posix()}` | {m.line} | "
                f"`{m.pattern_key}` | `{snip}` | {mig_disp} |"
            )
        lines.append("")

    # ---- 4. Low-confidence ----
    lines.append("## 4. Low-Confidence Matches (Possibly Intentional)")
    lines.append("")
    if not low:
        lines.append("_None detected._")
        lines.append("")
    else:
        lines.append(
            "These look like deprecated patterns, but the surrounding caption "
            "or inline comment suggests the book is intentionally showing the "
            "OLD pattern (e.g. \"Pydantic v1 syntax\", \"before LCEL\"). "
            "Verify each one is still pedagogically useful before changing."
        )
        lines.append("")
        lines.append("| # | File | Line | Pattern | Stale snippet | Caption (truncated) |")
        lines.append("|---|---|---:|---|---|---|")
        for i, m in enumerate(low, 1):
            snip = m.display_line().replace("|", "\\|")
            cap = (m.caption or "")[:80].replace("|", "\\|")
            if len(m.caption or "") > 80:
                cap += "..."
            lines.append(
                f"| {i} | `{m.file.as_posix()}` | {m.line} | "
                f"`{m.pattern_key}` | `{snip}` | {cap} |"
            )
        lines.append("")

    # ---- 5. Recommended next steps ----
    lines.append("## 5. Recommended Next Steps")
    lines.append("")
    auto_safe = []
    needs_review = []
    for key in pattern_order:
        if by_pattern.get(key, 0) == 0:
            continue
        cc = by_pattern_conf.get(key, Counter())
        if cc.get("high", 0) and cc.get("high", 0) == by_pattern[key]:
            auto_safe.append(key)
        else:
            needs_review.append(key)

    lines.append("**Safe to auto-migrate book-wide** (all matches are high confidence):")
    lines.append("")
    if not auto_safe:
        lines.append("- _None: every detected pattern has at least one ambiguous match._")
    else:
        for key in auto_safe:
            p = PATTERN_BY_KEY[key]
            n = by_pattern[key]
            lines.append(f"- `{key}` ({n} hits): {p.migration}")
    lines.append("")

    lines.append("**Needs review before migration** (mixed confidence):")
    lines.append("")
    if not needs_review:
        lines.append("- _None._")
    else:
        for key in needs_review:
            p = PATTERN_BY_KEY[key]
            cc = by_pattern_conf.get(key, Counter())
            lines.append(
                f"- `{key}` ({cc.get('high', 0)} high, {cc.get('medium', 0)} medium, "
                f"{cc.get('low', 0)} low): {p.migration}"
            )
    lines.append("")

    lines.append("**Suggested order of operations:**")
    lines.append("")
    lines.append(
        "1. Run the auto-safe migrations first (mechanical text substitutions). "
        "These have zero false-positive risk by construction."
    )
    lines.append(
        "2. For medium-confidence Pydantic patterns (`.dict()`, `.json()`, "
        "`.parse_obj()`), spot-check each match to confirm the object is a "
        "`BaseModel` subclass. Many `.json()` calls are on `requests.Response` "
        "and must NOT be changed."
    )
    lines.append(
        "3. For LangChain `chain.run()` / `agent_executor.run()`, prefer "
        "`.invoke({...})` and ensure the input is wrapped in a dict so it "
        "round-trips through the Runnable interface."
    )
    lines.append(
        "4. For PyTorch `torch.save(model, ...)`, decide per-fragment whether "
        "the pedagogical point is checkpointing (state_dict) or full-pickle "
        "demo. Convert the former; leave the latter alone but add a comment."
    )
    lines.append(
        "5. For low-confidence matches, read the caption: if it explicitly "
        "demonstrates the legacy pattern as a contrast, leave it and consider "
        "adding `# deprecated: pre-vX` next to the line."
    )
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report to {REPORT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
