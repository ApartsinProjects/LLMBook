"""Conservative classifier for low-value code blocks.

Philosophy: when in doubt, KEEP. The point is to surface the most egregious
low-value blocks, not to second-guess the author on borderline cases. The user
explicitly said: "Code that imports and uses a real library ... and demonstrates
a method" is HIGH value — don't flag.

Hard KEEP rules (applied first; if any matches, the block is KEEP):
- Block imports any "real library" by name OR a call like `lib.method(`,
  `client.x.y(`, `model.generate(`, etc. on a library handle (model, tokenizer,
  client, pipeline, llm, agent, chain, graph, trainer, vsc, db, conn, df, ...).
- Block has any `def ` (a function) and the body has control-flow keywords
  beyond `import`.
- Block has 2+ control-flow constructs (`for`, `while`, `if`, `elif`, `try`,
  `with`, `yield`, `return`) outside imports.
- Block contains algorithm hints (softmax, attention, matmul, einsum, sample,
  gradient, loss, beam_search, ...).
- Block contains a real numerical computation (np.array, torch.tensor,
  .matmul, .mean, .sum, .var, .shape, .reshape, .view, .gather, .scatter).

DROP rules (only fire if ALL hard-KEEP rules fail):
- Block is *purely* @dataclass / pydantic BaseModel / Enum with no methods,
  AND the field names are NOT referenced in the following 500 chars of
  surrounding prose/code.
- Block is a pure dict/list literal with kv_ratio >= 0.75, no defs/classes,
  AND no real-library imports/methods. (This catches config tables.)
- Block is print-only: print_ratio >= 0.7 and nonblank >= 3, no real lib,
  no control flow.

SIMPLIFY-TO-TABLE rules:
- A block whose final 1-3 lines are trailing `print(simple_var)` and the
  block has <= 12 lines, no real library, no def.

CONVERT-TO-DIAGRAM rules:
- A block defines 4+ classes (no methods) — likely a taxonomy.
- A block defines a dict-of-dicts that's identified as a state machine
  by surrounding prose (the words "state machine", "transition", "policy",
  "decision tree", "FSM" within 300 chars before).

NOTE: For each DROP candidate we also count how many of its field names
appear in the *following 1000 chars* (prose & next code) — if more than 2,
demote to KEEP, since the example is referenced.
"""
from __future__ import annotations
import json, re
from pathlib import Path

JSONL_IN = Path(__file__).parent / "code_blocks.jsonl"
JSONL_OUT = Path(__file__).parent / "code_blocks_classified.jsonl"

# --- Real library names (head of dotted module path) ---
REAL_LIBS = {
    "transformers", "langchain", "langgraph", "langchain_core", "langchain_community",
    "langchain_openai", "langchain_anthropic", "langchain_huggingface",
    "openai", "anthropic", "vllm", "litellm",
    "peft", "trl", "accelerate", "deepspeed", "fairscale", "bitsandbytes",
    "torch", "numpy", "pandas", "polars", "sklearn", "scipy",
    "datasets", "sentence_transformers", "tokenizers", "tiktoken",
    "evaluate", "wandb", "mlflow", "ray", "modal",
    "faiss", "chromadb", "weaviate", "pinecone", "qdrant_client",
    "fastapi", "pydantic", "redis", "kafka", "celery", "kueue",
    "matplotlib", "seaborn", "plotly", "altair",
    "tensorflow", "keras", "jax", "jnp", "flax",
    "diffusers", "controlnet_aux", "cv2", "PIL", "imageio",
    "whisper", "librosa", "soundfile",
    "duckdb", "sqlalchemy", "psycopg",
    "spacy", "nltk", "gensim", "instructor",
    "gradio", "streamlit", "dspy",
    "guardrails", "presidio_analyzer", "promptlayer", "weave",
    "boto3", "google", "azure",
    "regex", "fasttext",
    "crewai", "autogen", "openai_agents", "smolagents", "haystack",
    "pydantic_ai", "phidata",
    "flash_attn", "xformers", "triton",
    "umap", "hdbscan",
    "mamba_ssm", "rwkv",
    "trax", "xla",
    "sae_lens", "transformer_lens", "circuit_tracer",
    "codecarbon", "carbontracker",
    "bm25s", "ranx", "rerankers",
    "openllmetry", "langfuse", "promptfoo", "opik", "phoenix",
    "deepeval", "ragas",
    "airflow", "prefect", "dagster",
    "polars", "ibis",
    "llm_guard",
    "graphrag", "neo4j",
    "vertexai", "google_cloud_aiplatform",
    "kubernetes", "kopf",
    "argilla", "label_studio",
    "kr8s", "kustomize",
    "ml_energy",
    "tweepy", "praw", "stripe",
    "playwright", "selenium",
    "requests", "httpx", "aiohttp",
    "asyncio", "anyio", "trio",
    "megatron", "axolotl", "litgpt",
    "vlm", "moondream",
    "easyocr", "doctr",
    "lightllm", "tensorrt_llm", "sglang",
    "databricks", "snowflake",
    "fakeredis", "moto",
    "presidio", "opacus",
    "openllmetry", "opentelemetry",
    "pytest", "hypothesis",
    "mcp", "anyio",
    "stripe", "shopify",
    "openllmetry",
    "tensorrt", "onnxruntime",
    "mlperf", "olmes",
    "pyspark", "spark",
    "torchao", "auto_gptq", "autoawq",
    "datadog",
    "supabase", "firebase",
    "minio", "boto",
    "neo4j", "memgraph",
    "milvus", "pymilvus",
    "rouge", "rouge_score", "sacrebleu", "bert_score",
}
LIB_PREFIXES = {l.split(".")[0] for l in REAL_LIBS}

# Library-handle objects whose method call indicates a high-value demo
LIB_HANDLE_NAMES = {
    "client", "model", "tokenizer", "pipeline", "llm", "chain", "graph",
    "trainer", "agent", "crew", "executor", "retriever", "vectorstore",
    "embedder", "optimizer", "scheduler", "tracker", "logger", "metric",
    "scanner", "guard", "splitter", "loader", "writer", "reader",
    "validator", "judge", "evaluator", "rag", "indexer", "summarizer",
    "translator", "transcriber", "ocr", "asr", "tts",
    "cot", "react", "rea", "ner", "sae", "lens",
    "df", "ds", "data", "dataset", "dataloader",
    "session", "run", "experiment", "params", "config",
    "trace", "span", "context", "store",
    "torch", "np", "tf", "pd", "F", "nn",
    "bm25", "vsc", "kc", "redis_client", "minio_client",
    "supabase", "firebase",
    "tracker",
    "reducer",  # umap
}

ALG_HINTS = [
    "softmax", "attention", "matmul", "einsum",
    "sigmoid", "relu", "gelu", "tanh", "layernorm",
    "beam_search", "top_k", "top_p", "sampling", "logits",
    "tokenize", "encode_plus", "input_ids", "attention_mask",
    "loss", "backward", "step()", "zero_grad",
    "cross_entropy", "log_softmax", "argmax", "argmin",
    "masked_fill", "tril", "triu",
    "embedding", "linear", "transformer",
    "forward(", "predict(", "generate(", "fit(", "transform(",
    ".mean(", ".sum(", ".var(", ".shape", ".size(",
    "scatter", "gather", "repeat_kv",
    "rotary", "rope",
    "gradient_checkpointing",
    "kl_div", "log_likelihood",
    "ppo", "dpo", "grpo", "rlhf",
    "lora", "qlora", "ia3",
]


CONTROL_FLOW_RE = re.compile(r"^\s*(for|while|if|elif|else|try|except|finally|with|yield|return|raise|async\s+def|async\s+for|async\s+with)\b", re.MULTILINE)
DEF_RE = re.compile(r"^\s*def\s+(\w+)", re.MULTILINE)
CLASS_RE = re.compile(r"^\s*class\s+(\w+)", re.MULTILINE)
DATACLASS_RE = re.compile(r"@dataclass(?:\(|\s|$)")
BASEMODEL_RE = re.compile(r"class\s+\w+\(\s*BaseModel\s*\)")
ENUM_RE = re.compile(r"class\s+\w+\([^)]*Enum[^)]*\)")
NAMEDTUPLE_RE = re.compile(r"=\s*NamedTuple\(|class\s+\w+\(\s*NamedTuple\s*\)")
DICT_LITERAL_LINE = re.compile(r"^\s*[\"'\w\-]+\s*[:=]\s*", re.MULTILINE)
ENV_LINE = re.compile(r"^\s*[A-Z_]+\s*=", re.MULTILINE)
SHELL_LINE = re.compile(r"^\s*(\$\s+|pip\s+install|nvcc|conda|python\s+-c\b|export\s+|curl\s+|wget\s+|git\s+|docker\s+|kubectl\s+|aws\s+|gcloud\s+)", re.MULTILINE)


def head(name: str) -> str:
    return (name or "").split(".")[0]


def has_real_library(code: str, imports: list[str]) -> bool:
    """Return True if the block clearly imports a real library."""
    for im in imports or []:
        if head(im) in LIB_PREFIXES:
            return True
    # Also catch literal "from <lib> import X" / "import <lib>" that the
    # extractor missed due to inline comments etc.
    for m in re.finditer(r"^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.]+))", code, re.MULTILINE):
        n = m.group(1) or m.group(2)
        if head(n) in LIB_PREFIXES:
            return True
    return False


def has_library_method_call(code: str) -> bool:
    """Detect `handle.method(` or chained `handle.a.b.method(` where `handle` is
    a likely library object."""
    for name in LIB_HANDLE_NAMES:
        if re.search(rf"\b{re.escape(name)}(?:\.\w+)+\(", code):
            return True
    # Also: standalone function call like np.array(, torch.tensor(, openai.chat.x.y(
    for lib in ("np", "torch", "tf", "pd", "plt", "F", "nn", "OpenAI", "Anthropic",
                "openai", "anthropic", "spacy", "instructor", "umap"):
        if re.search(rf"\b{lib}(?:\.\w+)+\(", code):
            return True
    return False


def has_algorithm(code: str) -> bool:
    code_l = code.lower()
    return any(h in code_l for h in ALG_HINTS)


def has_control_flow(code: str) -> int:
    return len(CONTROL_FLOW_RE.findall(code))


def has_real_function(code: str) -> bool:
    """A def with body that's more than `pass` or a docstring."""
    defs = DEF_RE.findall(code)
    if not defs:
        return False
    # crude: at least one def must be followed by a non-trivial body
    return bool(re.search(r"^\s*def\s+\w+[^:]*:\s*\n(\s+(?!\s*(\"\"\"|'''|pass|return\s*$|\.\.\.))\S)", code, re.MULTILINE))


def field_names_from_class(code: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"^\s{2,}(\w+)\s*:\s*[\w\[\]\.,\s\"']+(?:=|\n|$)", code, re.MULTILINE)]


def classify(b: dict) -> dict:
    code = b["code"]
    lang = (b.get("lang_class") or "").lower()
    is_python = "python" in lang
    if not is_python:
        b["category"] = "NON_PYTHON"
        b["severity"] = 0
        b["reason"] = "Not python — skipped per scope"
        return b

    # ===== HARD KEEP RULES =====
    imports = b.get("imports") or []
    n_classes = len(CLASS_RE.findall(code))
    n_defs = len(DEF_RE.findall(code))
    n_lines = b["n_lines"]
    nonblank = b["nonblank_line_count"]
    print_count = b["print_count"]
    print_ratio = b["print_ratio"]
    kv_ratio = b["kv_ratio"]

    has_lib = has_real_library(code, imports)
    has_method = has_library_method_call(code)
    has_alg = has_algorithm(code)
    cf = has_control_flow(code)
    has_fn = has_real_function(code)

    is_dataclass = bool(DATACLASS_RE.search(code))
    is_pydantic = bool(BASEMODEL_RE.search(code))
    is_enum = bool(ENUM_RE.search(code))
    is_namedtuple = bool(NAMEDTUPLE_RE.search(code))
    is_pure_data = (is_dataclass or is_pydantic or is_enum or is_namedtuple) and n_defs == 0

    # If the block is essentially a data class with no methods, BUT has a real
    # library and library method call, it still counts as low-value if the
    # *purpose* of the block is the data shape. Heuristic: if the dataclass
    # *defines fields* and has no other library-method call beyond imports
    # and the @dataclass decorator, mark as pure_data candidate.
    if is_pure_data and not has_method and not has_alg and cf == 0:
        # Still: count field references in the following 1000 chars
        fields = field_names_from_class(code)
        ctx_after = b.get("ctx_after_head", "")
        # heavy reference => keep
        ref_count = sum(1 for f in fields if re.search(rf"\b{re.escape(f)}\b", ctx_after))
        if ref_count >= 2 or len(fields) >= 8:
            # Lots of fields referenced; or huge dataclass — keep
            pass
        else:
            # Real DROP candidate
            b["category"] = "DROP"
            b["severity"] = round(80 - n_lines * 0.5 + min(len(fields), 10) * 3 +
                                  (15 if is_dataclass else 0) + (15 if is_pydantic else 0) +
                                  (10 if is_enum else 0), 1)
            b["reason"] = (
                f"Pure data-class block: {len(fields)} fields, no methods, "
                f"only {ref_count} field refs in next 500 chars — render as <table>"
            )
            return b

    # ----- KEEP if any of these hold -----
    if has_lib and (has_method or has_alg or n_defs >= 1):
        b["category"] = "KEEP"
        b["severity"] = 0
        b["reason"] = "Real library with method/alg/fn usage"
        return b

    if has_alg:
        b["category"] = "KEEP"
        b["severity"] = 0
        b["reason"] = "Contains algorithm hints"
        return b

    if has_fn or cf >= 3:
        b["category"] = "KEEP"
        b["severity"] = 0
        b["reason"] = f"Non-trivial function or control flow (cf={cf}, n_defs={n_defs})"
        return b

    # ----- CONVERT-TO-DIAGRAM -----
    # 4+ class defs and no real fn body
    if n_classes >= 4 and not has_fn:
        b["category"] = "CONVERT-TO-DIAGRAM"
        b["severity"] = round(60 + n_classes * 5, 1)
        b["reason"] = f"Defines {n_classes} classes with no real logic — taxonomy diagram preferable"
        return b

    # State-machine dict-of-dicts
    state_dict_match = re.search(r"=\s*\{\s*[\"'][\w\-]+[\"']\s*:\s*\{", code)
    ctx = (b.get("ctx_before_tail") or "") + " " + (b.get("ctx_after_head") or "")
    if state_dict_match and re.search(r"\b(state machine|FSM|transition|state-machine|decision tree|policy|graph)\b", ctx, re.IGNORECASE):
        b["category"] = "CONVERT-TO-DIAGRAM"
        b["severity"] = round(70 + (kv_ratio * 25), 1)
        b["reason"] = "State machine / transition dict referenced in surrounding prose — diagram preferable"
        return b

    # ----- DROP: print-only -----
    if print_ratio >= 0.7 and nonblank >= 3 and not has_lib and cf == 0:
        b["category"] = "DROP"
        b["severity"] = round(55 + print_ratio * 30, 1)
        b["reason"] = f"Print-only block ({print_count}/{nonblank} lines are print()) — replace with prose"
        return b

    # ----- DROP: pure config / dict literal -----
    # Only fire when there is no real library imported AT ALL, no method calls,
    # and the block is essentially declarations.
    if (kv_ratio >= 0.75 and n_defs == 0 and n_classes == 0 and not has_lib
            and not has_method and not has_alg and cf == 0):
        # Make sure it's not a shell-snippet inside a Python block
        if not SHELL_LINE.search(code):
            b["category"] = "DROP"
            b["severity"] = round(60 + kv_ratio * 30 - n_lines * 0.3, 1)
            b["reason"] = f"Pure config/dict literal (kv_ratio={kv_ratio:.2f}, no library) — render as <table>"
            return b

    # ----- SIMPLIFY-TO-TABLE: short block ending in trailing prints -----
    last_lines = [l for l in code.rstrip().splitlines() if l.strip()]
    trailing = 0
    for ln in reversed(last_lines):
        if "print(" in ln:
            trailing += 1
        else:
            break
    if (1 <= trailing <= 3 and nonblank <= 10 and not has_lib and n_defs == 0
            and cf == 0 and not has_method and not has_alg):
        b["category"] = "SIMPLIFY-TO-TABLE"
        b["severity"] = round(40 + (10 - nonblank) * 3 + trailing * 5, 1)
        b["reason"] = f"Tiny block ending in {trailing} print() with no library — show as 2-row table"
        return b

    # ----- Default: KEEP -----
    keep_reason_parts = []
    if has_lib:
        keep_reason_parts.append(f"uses real lib")
    if has_method:
        keep_reason_parts.append("lib method call")
    if has_alg:
        keep_reason_parts.append("algorithm hints")
    if cf >= 1:
        keep_reason_parts.append(f"cf={cf}")
    if n_defs >= 1:
        keep_reason_parts.append(f"{n_defs} fns")
    if not keep_reason_parts:
        keep_reason_parts.append("default keep")
    b["category"] = "KEEP"
    b["severity"] = 0
    b["reason"] = "; ".join(keep_reason_parts)
    return b


def main():
    counts = {"DROP": 0, "SIMPLIFY-TO-TABLE": 0, "CONVERT-TO-DIAGRAM": 0, "KEEP": 0, "NON_PYTHON": 0}
    total = 0
    with JSONL_IN.open(encoding="utf-8") as fin, JSONL_OUT.open("w", encoding="utf-8") as fout:
        for line in fin:
            b = json.loads(line)
            b = classify(b)
            counts[b["category"]] += 1
            fout.write(json.dumps(b, ensure_ascii=False) + "\n")
            total += 1
    print(f"Total: {total}")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
