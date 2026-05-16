"""
Audit the LLMBook for opportunities to add a `library-shortcut` callout next to
a long Code Fragment that hand-rolls a concept with a well-known library
equivalent.

READ-ONLY. Run with Python 3.14:
    /c/Python314/python scripts/_audit_library_shortcut_opportunities.py

Approach
--------
1. Walk every .html under part-*/, skipping KDP/, .claude/, build/, temp_*, etc.
2. For each <div class="code-block-wrapper"> with a <pre><code class="...lang-python..."> body
   that has more than MIN_PY_LINES lines, decode and clean the source text.
3. Match a list of keyword + AST patterns. Each pattern maps to:
      - a "library shortcut" name (the library you would use instead)
      - a one-line suggestion ("use tenacity.retry instead of this hand-rolled retry loop")
      - a value heuristic (5x shorter, illuminating comparison, ...).
4. Skip when the next sibling within LOOKAHEAD elements is a
   <div class="callout library-shortcut"> (already handled).
5. Skip when a Library Shortcut callout already sits earlier in the same
   <section>/parent block (some files put the callout above the long fragment).
6. Emit a ranked Markdown punch list to library-shortcut-audit.md and stdout.

This script DOES NOT modify any HTML.
"""

from __future__ import annotations

import ast
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, NavigableString, Tag

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORT_PATH = PROJECT_ROOT / "library-shortcut-audit.md"

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
    "build",
    "dist",
}
EXCLUDE_PREFIXES = ("temp_", "_temp")


def is_excluded(path: Path) -> bool:
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
        if any(part.startswith(p) for p in EXCLUDE_PREFIXES):
            return True
    return False


# --------------------------------------------------------------------------- #
# Pattern library
# --------------------------------------------------------------------------- #
#
# Each pattern has:
#   id          : short stable key
#   library     : the library we recommend
#   suggestion  : one-line punch-list message ("use X instead of hand-rolled Y")
#   any_re      : list of regex; at least one must match the cleaned code text
#   require_re  : list of regex; ALL must match (used to tighten broad keywords)
#   exclude_re  : list of regex; if ANY match, the pattern is rejected
#                  (useful for "already imports tiktoken" -> skip)
#   min_lines   : per-pattern minimum python line count (overrides global default)
#   weight      : priority score added to ranking (1.0 default; 1.5+ for very
#                  illuminating comparisons like BPE -> tiktoken).
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Pattern:
    id: str
    library: str
    suggestion: str
    any_re: tuple[re.Pattern, ...]
    require_re: tuple[re.Pattern, ...] = ()
    exclude_re: tuple[re.Pattern, ...] = ()
    min_lines: int = 15
    weight: float = 1.0


def _re(p: str, flags: int = re.MULTILINE) -> re.Pattern:
    return re.compile(p, flags)


PATTERNS: list[Pattern] = [
    # ---------- BPE / tokenizer training ---------- #
    Pattern(
        id="bpe_from_scratch",
        library="tiktoken / sentencepiece / HuggingFace tokenizers",
        suggestion="add Library Shortcut: BPE training in 3 lines via `tokenizers.BpeTrainer` (or use a pretrained tiktoken encoding)",
        any_re=(
            _re(r"\bdef\s+(?:get_pairs|merge_pair|train_bpe|bpe_train|byte_pair|learn_bpe)\b"),
            _re(r"\bmost_common_pair\b|\bget_stats\b\s*\("),
            _re(r"\bmerges\s*=\s*\{\}"),
        ),
        require_re=(_re(r"\bpair\w*\b"),),
        exclude_re=(_re(r"^\s*from\s+tokenizers\b"), _re(r"^\s*import\s+tiktoken\b")),
        min_lines=18,
        weight=1.6,
    ),

    # ---------- WordPiece / Unigram tokenizer ---------- #
    Pattern(
        id="wordpiece_from_scratch",
        library="HuggingFace tokenizers (WordPieceTrainer)",
        suggestion="use `tokenizers.trainers.WordPieceTrainer` instead of this hand-rolled WordPiece loop",
        any_re=(_re(r"\bdef\s+\w*word_?piece\w*\b"), _re(r"\bWordPiece\b")),
        require_re=(_re(r"\bdef\s+\w+\("),),
        exclude_re=(_re(r"^\s*from\s+tokenizers\b"),),
        min_lines=20,
        weight=1.3,
    ),

    # ---------- Retry / exponential backoff ---------- #
    Pattern(
        id="retry_backoff",
        library="tenacity",
        suggestion="use `@tenacity.retry(stop=stop_after_attempt(5), wait=wait_exponential())` instead of hand-rolled retry/backoff",
        any_re=(
            _re(r"\bfor\s+attempt\s+in\s+range\(", re.MULTILINE),
            _re(r"\bfor\s+\w*retry\w*\s+in\s+range\(", re.MULTILINE),
            _re(r"\bbackoff\s*=\s*(?:2|min|base)\s*\*\*", re.MULTILINE),
            _re(r"\btime\.sleep\(\s*(?:backoff|delay|wait)\b", re.MULTILINE),
        ),
        require_re=(
            _re(r"\bexcept\b"),
            _re(r"\btime\.sleep\b|asyncio\.sleep\("),
        ),
        exclude_re=(
            _re(r"^\s*import\s+tenacity\b"),
            _re(r"^\s*from\s+tenacity\b"),
            _re(r"^\s*import\s+backoff\b"),
            _re(r"^\s*from\s+backoff\b"),
        ),
        min_lines=15,
        weight=1.4,
    ),

    # ---------- Rate limiter ---------- #
    Pattern(
        id="rate_limiter",
        library="aiolimiter / limits / ratelimit",
        suggestion="use `aiolimiter.AsyncLimiter(rate, period)` instead of this hand-rolled rate limiter",
        any_re=(
            _re(r"\bclass\s+\w*(?:Rate|Token)\w*(?:Limiter|Bucket)\b"),
            _re(r"\btokens_per_(?:second|minute)\b"),
            _re(r"\btoken_bucket\b"),
        ),
        require_re=(
            _re(r"\bdef\s+\w+\("),
            _re(r"\btime\.(?:time|monotonic)\("),
        ),
        exclude_re=(
            _re(r"^\s*from\s+aiolimiter\b"),
            _re(r"^\s*import\s+aiolimiter\b"),
            _re(r"^\s*from\s+ratelimit\b"),
        ),
        min_lines=18,
        weight=1.4,
    ),

    # ---------- Cosine similarity / vector similarity ---------- #
    Pattern(
        id="cosine_similarity",
        library="numpy or sklearn.metrics.pairwise.cosine_similarity",
        suggestion="use `sklearn.metrics.pairwise.cosine_similarity(A, B)` or `(A @ B.T) / (||A|| * ||B||)` from numpy",
        any_re=(
            _re(r"\bdef\s+\w*cos(?:ine)?_?sim\w*\("),
            _re(r"np\.dot\(.+?\)\s*/\s*\(\s*np\.linalg\.norm"),
        ),
        require_re=(_re(r"\bnp\.linalg\.norm\b|\bmath\.sqrt\b"),),
        exclude_re=(
            _re(r"^\s*from\s+sklearn\.metrics\.pairwise\s+import\s+cosine_similarity"),
        ),
        min_lines=10,  # cosine sim is dense -- even short versions beg the shortcut
        weight=1.5,
    ),

    # ---------- Nearest neighbor / vector search ---------- #
    Pattern(
        id="vector_nn_search",
        library="faiss / scipy.spatial.cKDTree",
        suggestion="use `faiss.IndexFlatIP` or `scipy.spatial.cKDTree.query` instead of this brute-force NN loop",
        any_re=(
            _re(r"\bfor\s+\w+\s+in\s+(?:enumerate\()?(?:embeddings|vectors|corpus|index)"),
            _re(r"\bdef\s+\w*(?:nearest|topk|top_k|knn|search)\w*\("),
        ),
        require_re=(
            _re(r"\bcos(?:ine)?_?sim\w*\(|np\.dot\("),
            _re(r"\bsort(?:ed)?\(|\bnp\.argsort\(|\bnp\.argpartition\(|\bheapq\."),
        ),
        exclude_re=(
            _re(r"^\s*import\s+faiss\b"),
            _re(r"^\s*from\s+faiss\b"),
        ),
        min_lines=18,
        weight=1.4,
    ),

    # ---------- Chunker / text splitter ---------- #
    Pattern(
        id="text_splitter",
        library="langchain.text_splitter.RecursiveCharacterTextSplitter",
        suggestion="use `RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)` instead of this hand-rolled chunker",
        any_re=(
            _re(r"\bdef\s+\w*(?:chunk|split|segment)\w*\b.*?(?:text|document|doc|content)", re.DOTALL),
        ),
        require_re=(
            _re(r"\bchunk_size\b|\bchunk_overlap\b|\bwindow_size\b|\boverlap\b"),
            _re(r"\bfor\s+\w+\s+in\s+range\(.*?(?:chunk|step|window)", re.DOTALL),
        ),
        exclude_re=(
            _re(r"^\s*from\s+langchain\b"),
            _re(r"^\s*from\s+llama_index\b"),
        ),
        min_lines=18,
        weight=1.3,
    ),

    # ---------- MCP protocol hand-rolled ---------- #
    Pattern(
        id="mcp_protocol",
        library="mcp Python SDK (modelcontextprotocol/python-sdk)",
        suggestion="use the official `mcp` Python SDK (`from mcp.server import Server`) instead of hand-rolling the JSON-RPC envelope",
        any_re=(
            _re(r"\b['\"](?:jsonrpc|method|params|id)['\"]\s*:\s*['\"]2\.0['\"]"),
            _re(r"\b['\"](?:initialize|tools/list|tools/call|resources/list)['\"]"),
            _re(r"\bMCP\b.*\bclass\b|\bclass\s+\w*MCP\w*\b"),
        ),
        require_re=(_re(r"\bclass\s+\w+\b|\bdef\s+\w+\("),),
        exclude_re=(
            _re(r"^\s*from\s+mcp\b"),
            _re(r"^\s*import\s+mcp\b"),
        ),
        min_lines=20,
        weight=1.5,
    ),

    # ---------- Hand-rolled embeddings (compute similarity, average, ...) ---------- #
    Pattern(
        id="hand_rolled_embedding_class",
        library="sentence-transformers",
        suggestion="use `SentenceTransformer('all-MiniLM-L6-v2').encode(texts)` instead of this hand-rolled embedding class",
        any_re=(
            _re(r"\bclass\s+\w*Embedder\b|\bclass\s+\w*Embedding(?:Model|Service)\b"),
            _re(r"\bdef\s+\w*embed\w*\("),
        ),
        require_re=(
            _re(r"\bencode\b|\bembed\b"),
            _re(r"\bnumpy\b|\bnp\.\b|\btorch\b"),
        ),
        exclude_re=(
            _re(r"^\s*from\s+sentence_transformers\b"),
            _re(r"\bSentenceTransformer\("),
            # OpenAI / Anthropic / Cohere clients are valid hosted embedders.
            _re(r"\bclient\.embeddings\.create\b"),
        ),
        min_lines=20,
        weight=1.2,
    ),

    # ---------- LRU/TTL cache hand-rolled ---------- #
    Pattern(
        id="lru_ttl_cache",
        library="cachetools (TTLCache / LRUCache) or functools.lru_cache",
        suggestion="use `cachetools.TTLCache(maxsize, ttl)` or `@functools.lru_cache(maxsize=...)` instead of this hand-rolled cache",
        any_re=(
            _re(r"\bclass\s+\w*(?:LRU|TTL|Cache)\w*\b"),
            _re(r"\bdef\s+\w*cache\w*\b"),
        ),
        require_re=(
            _re(r"\bOrderedDict\b|\bdict\b\s*=|\bself\.cache\b"),
            _re(r"\bevict\b|\bttl\b|\btime\.time\(\)\b|popitem\("),
        ),
        exclude_re=(
            _re(r"^\s*from\s+cachetools\b"),
            _re(r"^\s*from\s+functools\s+import\s+lru_cache\b"),
        ),
        min_lines=20,
        weight=1.2,
    ),

    # ---------- JSON-mode structured output / parser ---------- #
    Pattern(
        id="hand_rolled_json_parser",
        library="pydantic + instructor (or outlines)",
        suggestion="use `instructor.patch(client)` + a Pydantic `response_model=` instead of regex/strip-based JSON-mode parsing",
        any_re=(
            _re(r"\bdef\s+\w*parse_json\w*\("),
            _re(r"\bdef\s+\w*extract_json\w*\("),
            _re(r"\bre\.search\(.*?\\\{|\\\}.*?response", re.DOTALL),
            _re(r"\.strip\([\"']```\w*['\"]"),
        ),
        require_re=(
            _re(r"\bjson\.loads\b"),
            _re(r"\bopenai\b|\banthropic\b|\bclient\.\w+\.create\b"),
        ),
        exclude_re=(
            _re(r"^\s*import\s+instructor\b"),
            _re(r"^\s*from\s+instructor\b"),
            _re(r"^\s*from\s+outlines\b"),
        ),
        min_lines=18,
        weight=1.4,
    ),

    # ---------- Scaled dot-product attention from scratch ---------- #
    Pattern(
        id="attention_from_scratch",
        library="torch.nn.functional.scaled_dot_product_attention",
        suggestion="use `F.scaled_dot_product_attention(q, k, v, is_causal=True)` for the kernel-fused, flash-attention-backed version",
        any_re=(
            _re(r"\bscores\s*=\s*(?:torch\.matmul|q\s*@\s*k)"),
            _re(r"\bq\s*@\s*k\.(?:T|transpose)"),
            _re(r"\battention_weights?\s*=\s*F\.softmax|softmax\(.*?scores", re.DOTALL),
        ),
        require_re=(
            _re(r"\bmath\.sqrt|\bd_?k\b|\bhead_dim\b"),
            _re(r"\bsoftmax\b"),
        ),
        exclude_re=(
            _re(r"\bscaled_dot_product_attention\b"),
        ),
        min_lines=20,
        weight=1.3,
    ),

    # ---------- Hand-rolled HTTP retry around requests/httpx ---------- #
    Pattern(
        id="http_retry",
        library="httpx + tenacity",
        suggestion="use `tenacity.retry(retry=retry_if_exception_type(httpx.HTTPError))` instead of nesting requests.get inside a hand-rolled try/while",
        any_re=(
            _re(r"\brequests\.(?:get|post)\b|\bhttpx\.(?:get|post)\b"),
        ),
        require_re=(
            _re(r"\bfor\s+(?:attempt|retry|i)\s+in\s+range\(|while\s+attempt"),
            _re(r"\bexcept\b.*?(?:HTTPError|RequestException|ConnectionError|TimeoutError)", re.DOTALL),
            _re(r"\btime\.sleep\("),
        ),
        exclude_re=(
            _re(r"^\s*from\s+tenacity\b|^\s*import\s+tenacity\b"),
        ),
        min_lines=18,
        weight=1.3,
    ),

    # ---------- Hand-rolled config / env loading ---------- #
    Pattern(
        id="env_config",
        library="pydantic-settings",
        suggestion="use `pydantic_settings.BaseSettings` instead of repeated `os.environ.get(...)` defaulting + type coercion",
        any_re=(
            _re(r"\bclass\s+\w*(?:Config|Settings)\b"),
        ),
        require_re=(
            _re(r"\bos\.environ\.get\b|\bos\.getenv\b"),
            _re(r"\bint\(|\bfloat\(|\bbool\("),
        ),
        exclude_re=(
            _re(r"^\s*from\s+pydantic_settings\b"),
            _re(r"^\s*from\s+pydantic\b\s+import\s+BaseSettings\b"),
        ),
        min_lines=20,
        weight=1.0,
    ),

    # ---------- JSON Schema validation ---------- #
    Pattern(
        id="json_schema_validation",
        library="jsonschema or pydantic",
        suggestion="use `jsonschema.validate(instance, schema)` or a Pydantic model instead of hand-rolling type/required checks",
        any_re=(
            _re(r"\bdef\s+validate(?:_\w+)?\("),
        ),
        require_re=(
            _re(r"\brequired\b|\btype\s*==\s*['\"]string['\"]|isinstance\("),
            _re(r"\braise\s+ValueError\b|return\s+False"),
            _re(r"\bschema\b|\bproperties\b"),
        ),
        exclude_re=(
            _re(r"^\s*import\s+jsonschema\b"),
            _re(r"^\s*from\s+jsonschema\b"),
            _re(r"\bpydantic\b.*\bBaseModel\b"),
        ),
        min_lines=20,
        weight=1.1,
    ),

    # ---------- Hand-rolled vector DB client ---------- #
    Pattern(
        id="vector_db_client",
        library="chromadb / weaviate-client / pinecone-client / pgvector",
        suggestion="use `chromadb.Client().get_or_create_collection(...)` (or pgvector) instead of this dict-backed vector store",
        any_re=(
            _re(r"\bclass\s+\w*Vector(?:Store|DB|Database|Index)\b"),
        ),
        require_re=(
            _re(r"\bdef\s+add\b|\bdef\s+upsert\b|\bdef\s+insert\b"),
            _re(r"\bdef\s+(?:query|search|topk|top_k)\b"),
            _re(r"\bself\.(?:vectors|embeddings|index|store|data)\b"),
        ),
        exclude_re=(
            _re(r"^\s*import\s+chromadb\b"),
            _re(r"^\s*import\s+weaviate\b"),
            _re(r"^\s*from\s+pinecone\b"),
            _re(r"^\s*import\s+pinecone\b"),
        ),
        min_lines=25,
        weight=1.5,
    ),

    # ---------- Streaming SSE parser ---------- #
    Pattern(
        id="sse_parser",
        library="httpx-sse",
        suggestion="use `httpx_sse.connect_sse(...)` (or the OpenAI SDK's built-in `stream=True`) instead of a hand-rolled `data:` line parser",
        any_re=(
            _re(r"\bdata:\s*['\"]"),
            _re(r"\.startswith\(['\"]data:['\"]"),
            _re(r"\bline\.startswith\(b?['\"]data:['\"]"),
        ),
        require_re=(
            _re(r"\bfor\s+line\s+in\s+\w+(?:\.iter_lines|\.iter_content|\.aiter_lines)"),
            _re(r"\bjson\.loads\b"),
        ),
        exclude_re=(
            _re(r"^\s*import\s+httpx_sse\b"),
            _re(r"^\s*from\s+httpx_sse\b"),
        ),
        min_lines=18,
        weight=1.3,
    ),

    # ---------- Prompt template (string formatting + variable injection) ---------- #
    Pattern(
        id="prompt_template",
        library="langchain.prompts.PromptTemplate or llama_index.PromptTemplate",
        suggestion="use `PromptTemplate.from_template(\"...{var}...\")` from LangChain or jinja2 instead of hand-rolling .format/regex injection",
        any_re=(
            _re(r"\bclass\s+\w*Prompt(?:Template|Builder|Manager|Registry)\b"),
        ),
        require_re=(
            _re(r"\.format\(\*\*\w+\)|\.replace\(['\"]\{|\bsubstitute\("),
            _re(r"\bdef\s+render\(|\bdef\s+build\(|\bdef\s+format\("),
            _re(r"\bself\.template\b|\bself\.prompt\b"),
        ),
        exclude_re=(
            _re(r"^\s*from\s+langchain\.prompts\b"),
            _re(r"^\s*from\s+llama_index\b"),
            _re(r"^\s*import\s+jinja2\b"),
        ),
        min_lines=22,
        weight=1.0,
    ),

    # ---------- One-hot encoding ---------- #
    Pattern(
        id="one_hot",
        library="numpy.eye / sklearn.preprocessing.OneHotEncoder / torch.nn.functional.one_hot",
        suggestion="use `np.eye(vocab_size)[indices]` or `F.one_hot(t, num_classes=K)` instead of looping with zero vectors",
        any_re=(
            _re(r"\bdef\s+\w*one_?hot\w*\("),
        ),
        require_re=(
            _re(r"\bzeros\(|\bnp\.zeros\("),
            _re(r"\bfor\s+\w+\s+in\b"),
        ),
        exclude_re=(
            _re(r"\bnp\.eye\b"),
            _re(r"\bF\.one_hot\b"),
            _re(r"\bOneHotEncoder\b"),
        ),
        min_lines=12,
        weight=1.1,
    ),
]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def iter_html_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.glob("part-*/**/*.html")):
        if is_excluded(path.relative_to(root)):
            continue
        yield path


def extract_python_source(code_tag: Tag) -> str:
    """Pull plain Python from the pygments-highlighted spans."""
    # BeautifulSoup .get_text() already drops the spans but preserves text.
    text = code_tag.get_text()
    return text


def python_line_count(src: str) -> int:
    """Count meaningful (non-blank, non-comment-only) Python lines."""
    n = 0
    for raw in src.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        n += 1
    return n


def parse_ast_safely(src: str) -> ast.AST | None:
    try:
        return ast.parse(src)
    except SyntaxError:
        return None


def fragment_caption(wrapper: Tag) -> tuple[str | None, str | None]:
    """Return (fragment number like '11.1.2', caption text) if present."""
    cap = wrapper.find("div", class_="code-caption")
    if cap is None:
        return None, None
    text = cap.get_text(" ", strip=True)
    m = re.match(r"Code Fragment\s+(\d+(?:\.\d+)+)\s*:\s*(.+)", text)
    if m:
        return m.group(1), m.group(2)
    return None, text


def has_library_shortcut_neighbor(wrapper: Tag, lookahead: int = 6) -> bool:
    """True if a sibling within `lookahead` next-siblings is a library-shortcut callout."""
    sib = wrapper
    seen = 0
    while seen < lookahead:
        sib = sib.find_next_sibling()
        if sib is None:
            break
        seen += 1
        if not isinstance(sib, Tag):
            continue
        cls = sib.get("class") or []
        if "callout" in cls and "library-shortcut" in cls:
            return True
        # If we hit another code-block-wrapper or a section header, stop.
        if sib.name in {"h1", "h2", "h3", "h4"}:
            break
        if "code-block-wrapper" in cls:
            break
    # Also check the immediately preceding sibling for a paired shortcut.
    prev = wrapper.find_previous_sibling()
    if isinstance(prev, Tag):
        cls = prev.get("class") or []
        if "callout" in cls and "library-shortcut" in cls:
            return True
    return False


def section_already_shortcuts_topic(soup: BeautifulSoup, suggestion_libs: str) -> bool:
    """Heuristic: avoid double-flagging when the file already has multiple
    library-shortcut callouts mentioning the same library."""
    libs = set(re.findall(r"[A-Za-z][\w\-\.]+", suggestion_libs.lower()))
    if not libs:
        return False
    for cb in soup.find_all("div", class_="callout"):
        cls = cb.get("class") or []
        if "library-shortcut" not in cls:
            continue
        text = cb.get_text(" ", strip=True).lower()
        for lib in libs:
            if len(lib) >= 5 and lib in text:
                return True
    return False


# --------------------------------------------------------------------------- #
# Match logic
# --------------------------------------------------------------------------- #

@dataclass
class Candidate:
    path: Path
    fragment_id: str | None
    caption: str | None
    pattern: Pattern
    line_count: int
    snippet: str
    score: float = 0.0

    def score_for_ranking(self) -> float:
        # Long fragment + high-weight pattern => high score.
        size_factor = min(self.line_count / 25.0, 3.0)
        return self.pattern.weight * size_factor


def match_patterns(src: str) -> list[Pattern]:
    matches: list[Pattern] = []
    for p in PATTERNS:
        # Exclusion check first.
        if any(rx.search(src) for rx in p.exclude_re):
            continue
        # Required regex.
        if any(not rx.search(src) for rx in p.require_re):
            continue
        # Any-of regex.
        if not any(rx.search(src) for rx in p.any_re):
            continue
        # Minimum lines.
        if python_line_count(src) < p.min_lines:
            continue
        matches.append(p)
    return matches


def scan_file(path: Path, root: Path) -> list[Candidate]:
    text = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    out: list[Candidate] = []

    for wrapper in soup.find_all("div", class_="code-block-wrapper"):
        code = wrapper.find("code")
        if code is None:
            continue
        cls = code.get("class") or []
        if not any("lang-python" in c for c in cls):
            continue
        src = extract_python_source(code)
        lines = python_line_count(src)
        if lines < 15:
            continue

        # Skip if already has a library-shortcut sibling.
        if has_library_shortcut_neighbor(wrapper):
            continue

        patterns = match_patterns(src)
        if not patterns:
            continue

        frag_id, caption = fragment_caption(wrapper)
        for p in patterns:
            if section_already_shortcuts_topic(soup, p.library):
                # Already covered by an existing library-shortcut elsewhere in
                # the same file with the same library.
                continue
            # Build a 4-line snippet of the relevant region (first hit).
            snippet = ""
            for rx in p.any_re:
                m = rx.search(src)
                if m:
                    start = max(0, m.start() - 40)
                    end = min(len(src), m.end() + 80)
                    snippet = src[start:end].strip().replace("\n", " | ")
                    snippet = re.sub(r"\s+", " ", snippet)[:160]
                    break
            cand = Candidate(
                path=path.relative_to(root),
                fragment_id=frag_id,
                caption=caption,
                pattern=p,
                line_count=lines,
                snippet=snippet,
            )
            cand.score = cand.score_for_ranking()
            out.append(cand)
    return out


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

def write_report(candidates: list[Candidate]) -> None:
    candidates.sort(key=lambda c: (-c.score, str(c.path), c.fragment_id or ""))

    lines = []
    lines.append("# Library Shortcut Opportunities Audit\n")
    lines.append(f"Scanned: {len(set(c.path for c in candidates))} files\n")
    lines.append(f"Candidates: {len(candidates)}\n\n")

    by_pattern: dict[str, list[Candidate]] = defaultdict(list)
    for c in candidates:
        by_pattern[c.pattern.id].append(c)

    lines.append("## Summary by pattern\n\n")
    lines.append("| Pattern | Library | Hits |\n|---|---|---|\n")
    for pid in sorted(by_pattern, key=lambda k: -len(by_pattern[k])):
        sample = by_pattern[pid][0]
        lines.append(f"| `{pid}` | {sample.pattern.library} | {len(by_pattern[pid])} |\n")
    lines.append("\n")

    lines.append("## Top candidates (highest score first)\n\n")
    for i, c in enumerate(candidates[:40], 1):
        frag = c.fragment_id or "(no caption)"
        cap = c.caption or ""
        lines.append(
            f"### {i}. `{c.path}` — Code Fragment {frag} ({c.line_count} lines, score={c.score:.2f})\n"
        )
        if cap:
            lines.append(f"- **Caption**: {cap}\n")
        lines.append(f"- **Pattern**: `{c.pattern.id}`\n")
        lines.append(f"- **Library**: {c.pattern.library}\n")
        lines.append(f"- **Suggestion**: {c.pattern.suggestion}\n")
        if c.snippet:
            lines.append(f"- **Match snippet**: `{c.snippet}`\n")
        lines.append("\n")

    REPORT_PATH.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    root = PROJECT_ROOT
    candidates: list[Candidate] = []
    file_count = 0
    for path in iter_html_files(root):
        file_count += 1
        try:
            candidates.extend(scan_file(path, root))
        except Exception as e:
            print(f"[error] {path}: {e!r}", file=sys.stderr)

    write_report(candidates)
    print(f"Scanned {file_count} files. Found {len(candidates)} candidates. Report: {REPORT_PATH}")

    # Also print the top 20 to stdout in compact form.
    candidates.sort(key=lambda c: (-c.score, str(c.path), c.fragment_id or ""))
    print("\nTop candidates (truncated):\n")
    for i, c in enumerate(candidates[:25], 1):
        print(
            f"{i:>2}. [{c.score:.2f}] {c.pattern.id:<28} "
            f"frag={c.fragment_id or '?':<10} lines={c.line_count:<3} "
            f"{c.path}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
