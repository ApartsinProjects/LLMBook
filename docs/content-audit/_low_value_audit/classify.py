"""Classify each code block into DROP, SIMPLIFY-TO-TABLE, CONVERT-TO-DIAGRAM, or KEEP.

Heuristics implemented (intentionally conservative for KEEP):

1. KEEP if:
   - imports a real library that's clearly demonstrating a method
     (transformers, langchain, openai, vllm, anthropic, peft, trl, accelerate,
      torch, numpy, pandas, sklearn, datasets, sentence_transformers, etc.)
     AND has more than dataclass-only code
   - has a non-trivial def with control flow (for/while/if-elif/recursion/yield)
   - shows two implementations side-by-side (multiple ``` blocks ... we cannot
     detect side-by-side from single block, so we look at "before" vs "after"
     comment hints)
   - contains a real algorithm (matmul, attention, sampling, beam search, etc.)

2. DROP if:
   - dataclass_only=True with no methods, and code does not appear referenced
     in the surrounding text (we approximate by checking that none of the
     class field names appear in the 500-char window after the block)
   - pure dict / list literal with kv_ratio > 0.7 and no def
   - pseudocode that looks like prose disguised as code (lots of comments,
     few real statements) — too noisy to flag automatically; skip
   - print-only block: code is purely sequence of print(...) statements
     re-stating prose (>= 60% of non-blank lines are print calls)

3. SIMPLIFY-TO-TABLE if:
   - Block has 1-3 print statements at the end whose only purpose is to
     show 1-2 variables
   - Or: block is essentially `x = ...; y = ...; print(x); print(y)`

4. CONVERT-TO-DIAGRAM if:
   - class hierarchy: 3+ class definitions, mostly field declarations, that
     describe a taxonomy or state machine
   - decision tree / state machine literal: dict of states with transitions

Severity scoring (higher = worse, more in need of action):
   DROP and language is python: severity = 100 - n_lines + dataclass_only*30 + kv_ratio*50
   SIMPLIFY: severity = print_ratio*70 + (1/n_lines)*10
   CONVERT: severity = kv_ratio*60 + (n_classes * 10)
"""
from __future__ import annotations
import json, re
from pathlib import Path

JSONL_IN = Path(__file__).parent / "code_blocks.jsonl"
JSONL_OUT = Path(__file__).parent / "code_blocks_classified.jsonl"

REAL_LIBS = {
    "transformers", "langchain", "langgraph", "langchain_core", "langchain_community",
    "langchain_openai", "langchain_anthropic", "openai", "anthropic", "vllm",
    "peft", "trl", "accelerate", "torch", "torch.nn", "torch.nn.functional",
    "torch.utils.data", "torch.optim", "numpy", "np", "pandas", "pd",
    "sklearn", "datasets", "sentence_transformers", "tokenizers", "tiktoken",
    "evaluate", "wandb", "mlflow", "ray", "deepspeed", "bitsandbytes",
    "faiss", "chromadb", "weaviate", "pinecone", "qdrant_client",
    "fastapi", "pydantic", "redis", "kafka", "celery",
    "matplotlib", "matplotlib.pyplot", "plt", "seaborn", "sns", "plotly",
    "scipy", "scipy.stats", "scipy.special", "scipy.optimize",
    "tensorflow", "tf", "keras", "jax", "jax.numpy", "jnp",
    "diffusers", "controlnet_aux", "opencv", "cv2", "PIL", "imageio",
    "whisper", "librosa", "soundfile",
    "polars", "ibis", "duckdb", "sqlite3", "sqlalchemy",
    "torch.distributed", "fairscale", "flash_attn",
    "gradio", "streamlit",
    "guardrails", "promptlayer", "weave", "presidio_analyzer",
    "boto3", "google.cloud", "azure",
    "regex", "spacy", "nltk", "gensim", "fasttext",
}
# Allow prefix matching (numpy as np, etc.)
LIB_PREFIXES = tuple(sorted({l.split(".")[0] for l in REAL_LIBS}))


def is_real_lib(name: str) -> bool:
    if not name:
        return False
    head = name.split(".")[0]
    return head in {p for p in LIB_PREFIXES}


CONTROL_FLOW_RE = re.compile(r"\b(for|while|if|elif|else|yield|return|with|try|except|raise|async|await)\b")
ALG_HINTS_RE = re.compile(
    r"\b(softmax|attention|matmul|einsum|sigmoid|relu|gelu|layernorm|"
    r"beam_search|top_k|top_p|sampling|tokenize|encode|decode|embed|"
    r"loss|backward|optim|gradient|sample|generate|forward|predict|"
    r"masked_fill|cross_entropy|gather|scatter|cat|stack|reshape|transpose|"
    r"argmax|argmin)\b", re.IGNORECASE,
)

CLASS_RE = re.compile(r"^\s*class\s+(\w+)", re.MULTILINE)
DEF_RE = re.compile(r"^\s*def\s+(\w+)", re.MULTILINE)


def field_names_from_class(code: str) -> list[str]:
    """Return rough list of attribute/field names declared inside class bodies."""
    out = []
    # Pydantic / dataclass style:  name: type = value  OR name: type
    for m in re.finditer(r"^\s{4,}(\w+)\s*:", code, re.MULTILINE):
        out.append(m.group(1))
    return out


def references_in_surrounding(field_names: list[str], ctx_after: str) -> int:
    """Count how many field names are referenced in the following context."""
    if not field_names:
        return 0
    return sum(1 for f in field_names if re.search(rf"\b{re.escape(f)}\b", ctx_after))


def classify(b: dict) -> dict:
    code = b["code"]
    lang = (b.get("lang_class") or "").lower()
    is_python = "python" in lang or "lang-python" in lang
    is_text = "language-text" in lang or "lang-text" in lang or "language-output" in lang or "no-highlight" in lang

    # Only audit Python blocks per user's scope: "<pre><code class="...lang-python">"
    if not is_python:
        b["category"] = "NON_PYTHON"
        b["severity"] = 0
        b["reason"] = "Not a python code block (skipped per scope)"
        return b

    # Strip docstring lines for analysis
    n_lines = b["n_lines"]
    nonblank_count = b["nonblank_line_count"]

    n_classes = len(CLASS_RE.findall(code))
    n_defs = len(DEF_RE.findall(code))
    cf_hits = len(CONTROL_FLOW_RE.findall(code))
    alg_hits = len(ALG_HINTS_RE.findall(code))

    real_libs = [im for im in (b.get("imports") or []) if is_real_lib(im)]
    has_real_lib = bool(real_libs)
    # method calls on imported libs ("model.generate", "client.chat.completions")
    has_lib_method = bool(re.search(r"\b(client|model|tokenizer|pipeline|llm|chain|graph|trainer|trl|peft|optimizer)\.\w+\(", code))

    # ----- CONVERT-TO-DIAGRAM -----
    # multiple classes / enum-like literals describing a hierarchy or state machine
    converted = False
    state_dict_match = re.search(r"=\s*\{[^{}]*(?:\"[^\"]+\"|'[^']+')\s*:\s*\{", code)
    if n_classes >= 3 and not has_lib_method and cf_hits < 4:
        b["category"] = "CONVERT-TO-DIAGRAM"
        b["severity"] = round(60 + n_classes * 5 + (1 if state_dict_match else 0) * 10, 1)
        b["reason"] = f"Defines {n_classes} classes with little logic — diagram preferable"
        return b
    # State machines / decision trees represented as dict-of-dicts
    if state_dict_match and "for " not in code and "return" not in code and n_lines < 50:
        # Make sure it really is a transition table
        if re.search(r"(transitions|states|next_state|action|policy|graph)\b", code, re.IGNORECASE):
            b["category"] = "CONVERT-TO-DIAGRAM"
            b["severity"] = round(70 + (b["kv_ratio"] * 30), 1)
            b["reason"] = "State machine / transition table — diagram preferable"
            return b

    # ----- DROP candidates -----
    # 1) pure dataclass / pydantic model with no methods
    is_dataclass = bool(re.search(r"@dataclass\b", code))
    is_pydantic = bool(re.search(r"class\s+\w+\(\s*BaseModel\s*\)", code))
    is_namedtuple = bool(re.search(r"=\s*NamedTuple\(", code))
    is_enum_only = bool(re.search(r"class\s+\w+\(.*?Enum.*?\)", code)) and n_defs == 0

    if (is_dataclass or is_pydantic or is_enum_only) and n_defs == 0 and not has_lib_method:
        fields = field_names_from_class(code)
        # Check follow-up usage
        ctx_after = b.get("ctx_after_head", "")
        refs = references_in_surrounding(fields, ctx_after)
        if refs <= 1 or len(fields) <= 4:
            b["category"] = "DROP"
            b["severity"] = round(80 - n_lines + (30 if is_dataclass else 20) + min(len(fields), 10) * 2, 1)
            b["reason"] = (
                f"@dataclass/BaseModel/Enum-only ({len(fields)} fields, no methods); "
                f"{refs} field references in following 500 chars — table is clearer"
            )
            return b

    # 2) pure dict/list literal (config table)
    if b["kv_ratio"] >= 0.65 and n_defs == 0 and n_classes == 0 and not has_real_lib and not has_lib_method:
        # Make sure it isn't algorithm-heavy
        if cf_hits <= 1 and alg_hits <= 1:
            b["category"] = "DROP"
            b["severity"] = round(70 + b["kv_ratio"] * 30 - n_lines * 0.5, 1)
            b["reason"] = f"Config/dict literal (kv_ratio={b['kv_ratio']:.2f}, no fns/classes) — render as <table>"
            return b

    # 3) print-only block
    if b["print_ratio"] >= 0.6 and nonblank_count >= 3 and not has_real_lib and cf_hits <= 1:
        b["category"] = "DROP"
        b["severity"] = round(50 + b["print_ratio"] * 40, 1)
        b["reason"] = f"Print-only block ({b['print_count']}/{nonblank_count} lines are print()) — replace with prose"
        return b

    # ----- SIMPLIFY-TO-TABLE -----
    # 1-3 print statements at end whose only purpose is to show 1-2 variables
    last_lines = code.rstrip().splitlines()
    # count trailing print lines
    trailing_prints = 0
    for ln in reversed(last_lines):
        if "print(" in ln:
            trailing_prints += 1
        elif ln.strip() == "":
            continue
        else:
            break
    if 1 <= trailing_prints <= 3 and not has_real_lib and cf_hits <= 1 and n_defs == 0 and n_lines <= 12:
        # And the prints are showing simple variables
        if all(re.search(r"print\(\s*['\"]?\w[\w\.,\s'\":\-+%]*['\"]?\s*[,)]", l) for l in last_lines[-trailing_prints:]):
            b["category"] = "SIMPLIFY-TO-TABLE"
            b["severity"] = round(40 + (10 - n_lines) * 2 + trailing_prints * 5, 1)
            b["reason"] = f"Small block ending in {trailing_prints} print() — show as 2-row table"
            return b

    # Toy demo (a+b style) — no imports, no defs, short, just arithmetic + print
    arith_match = re.search(r"^\s*\w+\s*=\s*[\w\d\+\-\*/\.\(\)\s]+$", code, re.MULTILINE)
    if (not has_real_lib and n_defs == 0 and n_classes == 0 and n_lines <= 8 and
            b["print_count"] >= 1 and cf_hits <= 1 and alg_hits == 0):
        # genuinely trivial: no library, very short, no algorithm
        b["category"] = "DROP"
        b["severity"] = round(45 + (8 - n_lines) * 3 + b["print_count"] * 3, 1)
        b["reason"] = f"Toy demo (no library, {n_lines} lines, {b['print_count']} prints, no algorithm) — prose suffices"
        return b

    # ----- Default: KEEP -----
    keep_reason = []
    if has_real_lib:
        keep_reason.append(f"uses {','.join(real_libs[:3])}")
    if cf_hits >= 3:
        keep_reason.append(f"control-flow x{cf_hits}")
    if alg_hits >= 2:
        keep_reason.append(f"algorithm hints x{alg_hits}")
    if n_defs >= 1:
        keep_reason.append(f"{n_defs} fns")
    if has_lib_method:
        keep_reason.append("lib method calls")
    b["category"] = "KEEP"
    b["severity"] = 0
    b["reason"] = "; ".join(keep_reason) if keep_reason else "default keep"
    return b


def main():
    total = 0
    counts = {"DROP": 0, "SIMPLIFY-TO-TABLE": 0, "CONVERT-TO-DIAGRAM": 0, "KEEP": 0, "NON_PYTHON": 0}
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
