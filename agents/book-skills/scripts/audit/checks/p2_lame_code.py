"""Detect "lame" code fragments: blocks that contain no real logic.

Per user feedback: "Code Fragment 42.10.3 absolutely lame, just dataclass
or checklist does not justify code fragment, convert to table or add
logic/3rd party library or drop."

Patterns flagged:
1. Pure dataclass: `@dataclass class X:` followed only by field definitions
   (no methods, no logic, no 3rd-party imports).
2. Pure dict literal: code body is just `X = {...}` or `data = {...}` with
   no function calls or control flow.
3. Pure config YAML/JSON: code body is `key: value` pairs only with no
   imports or runtime invocations.
4. Pure list of strings/dicts (e.g., reproducibility checklist) with no
   logic to consume them.

Body inspection:
- Strip Pygments span tags to get raw code text.
- Count tokens: `def`, `class`, `for`, `while`, `if`, `try`, `with`, `return`
- Count library imports beyond stdlib (heuristic: top-level `import X`
  where X is not in stdlib).
- If the code has 0 control-flow keywords AND 0 third-party imports AND
  is just data, flag as LAME.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "LAME_CODE"
DESCRIPTION = "Code fragment has no logic (pure data/dataclass/config); convert to table or drop"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CODE_BLOCK_RE = re.compile(
    r'<pre[^>]*><code\s+class="pygments-highlighted\s+lang-(\w+)"[^>]*>([\s\S]*?)</code></pre>',
    re.IGNORECASE,
)
CAPTION_RE = re.compile(
    r'<div\s+class="code-caption">\s*<strong>\s*(Code Fragment\s+[\d.]+)\s*[:.]?\s*</strong>([^<]+)</div>',
    re.IGNORECASE,
)

# Control-flow keywords that indicate "real code"
LOGIC_KEYWORDS = {
    'def', 'class', 'for', 'while', 'if', 'elif', 'else', 'try', 'except',
    'finally', 'with', 'return', 'yield', 'lambda', 'async', 'await',
    'raise', 'break', 'continue', 'match', 'case',
}

# Third-party libraries common in this book (heuristic)
THIRD_PARTY = {
    'numpy', 'np', 'torch', 'tensorflow', 'tf', 'jax', 'transformers',
    'openai', 'anthropic', 'google', 'langchain', 'llama_index', 'llamaindex',
    'peft', 'trl', 'datasets', 'sentence_transformers', 'sklearn', 'pandas',
    'pd', 'matplotlib', 'plt', 'seaborn', 'sns', 'wandb', 'mlflow', 'pydantic',
    'fastapi', 'flask', 'requests', 'httpx', 'aiohttp', 'asyncio', 'pytest',
    'instructor', 'outlines', 'dspy', 'guidance', 'modal', 'ray', 'celery',
    'vllm', 'tgi', 'sglang', 'unsloth', 'bitsandbytes', 'optuna', 'redis',
    'opentelemetry', 'pagefind', 'pygments', 'pillow', 'pil', 'pyarrow',
    'sqlalchemy', 'psycopg2', 'pinecone', 'qdrant_client', 'qdrant',
    'chromadb', 'weaviate', 'faiss', 'redis', 'rasa', 'crewai', 'autogen',
    'letta', 'mem0', 'baml', 'mergekit', 'verl', 'torchtitan', 'nanotron',
    'gradio', 'streamlit', 'chainlit', 'beautifulsoup', 'bs4', 'pypdf2',
    'pdfplumber', 'spacy', 'nltk', 'tokenizers', 'tiktoken',
}


def _strip_html(code_html: str) -> str:
    """Strip Pygments span tags to recover raw code text."""
    text = re.sub(r'<[^>]+>', '', code_html)
    # Decode common entities
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&amp;', '&').replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    return text


def _is_lame(code: str, lang: str) -> tuple[bool, str]:
    """Returns (is_lame, reason)."""
    lines = [l.rstrip() for l in code.strip().split('\n') if l.strip()]
    if len(lines) < 3:
        return False, ''  # too short to flag

    # YAML / JSON: lame if no anchors or complex structure (just key:value)
    if lang.lower() in ('yaml', 'yml', 'json'):
        # YAML lame if no `&` references, no `<<:` merge, no `!tag` and few keys
        has_anchors = re.search(r'[&*]\w+', code) or '<<:' in code or '!' in code
        if not has_anchors and len(lines) < 30:
            return True, f'pure {lang.upper()} config: convert to table or callout'

    if lang.lower() in ('python', 'py'):
        # Count control-flow keywords
        n_logic = 0
        for kw in LOGIC_KEYWORDS:
            n_logic += len(re.findall(rf'\b{kw}\b', code))
        # Count imports
        imports = re.findall(r'^\s*(?:from|import)\s+(\w+)', code, re.MULTILINE)
        n_third = sum(1 for imp in imports if imp.lower() in THIRD_PARTY)

        # Pure dataclass / dict: heavy on field definitions, light on logic
        n_fields = len(re.findall(r'^\s+\w+\s*[:=]\s', code, re.MULTILINE))
        n_def = len(re.findall(r'\bdef\s+\w+', code))
        # @dataclass usage
        is_dataclass = '@dataclass' in code or '@pydantic' in code or 'BaseModel' in code

        if is_dataclass and n_def == 0:
            return True, 'pure dataclass with no methods: convert to table or add usage example'
        # Pure dict / list literal
        if n_logic <= 1 and n_third == 0 and n_fields > 5:
            return True, f'data-only ({n_fields} fields, {n_logic} logic keywords); convert to table or drop'

    return False, ''


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    # Skip tools-of-the-trade and appendix (reference material is allowed to be flat)
    rel = str(filepath).lower().replace('\\', '/')
    if any(x in rel for x in (
        '/tools-of-the-trade/', '/appendices/', '/appendix-',
        'tools-of-the-trade', 'scale-tools', 'retrieval-tools',
        'conv-ai-tools', 'responsible-ai-tools',
    )):
        return issues

    # Iterate code blocks; find each followed by a caption within ~10 lines
    for m in CODE_BLOCK_RE.finditer(html):
        lang = m.group(1)
        code_html = m.group(2)
        code = _strip_html(code_html)
        is_lame, reason = _is_lame(code, lang)
        if not is_lame:
            continue
        # Find the caption that follows
        rest = html[m.end():m.end() + 2000]
        cm = CAPTION_RE.search(rest)
        label = cm.group(1) if cm else 'Code Fragment ?'
        line = html.count('\n', 0, m.start()) + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'LAME_CODE: {label} — {reason}',
        ))
    return issues
