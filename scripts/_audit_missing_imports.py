"""
Audit missing imports / undefined names in Python code fragments across the LLMBook.

For every <pre><code class="...lang-python..."> block:

1. Parse with `ast.parse`. Skip blocks that don't parse cleanly (already covered
   by the deep-fragment audit).

2. Walk the AST and collect:
     - All Name references (load context)
     - All Attribute references (base name)
     - All imports (`import X`, `from X import Y`, `from X import Y as Z`)
     - All function / class / variable definitions
     - All function parameter names
     - All comprehension targets

3. For each Name reference, check it's resolvable:
     - Imported (any form), OR
     - Local definition (function / class / variable), OR
     - Python builtin (open, print, range, len, dict, list, set, tuple, str,
       int, float, bool, bytes, None, True, False, Exception, etc.), OR
     - Function parameter / comprehension variable in scope, OR
     - Typing construct (Any, Optional, Union, Literal, etc.) -- these
       technically need importing but in pedagogical fragments are often used
       without.

4. If a Name is referenced but not resolvable, flag it.

Output: missing-imports-audit.md.

READ-ONLY. BeautifulSoup + ast. Same exclusions as the lame-code audit.
"""

from __future__ import annotations

import ast
import builtins
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORT_PATH = PROJECT_ROOT / "missing-imports-audit.md"

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
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
        if any(part.startswith(p) for p in EXCLUDE_PREFIXES):
            return True
        if any(c in part.lower() for c in EXCLUDE_CONTAINS):
            return True
    return False


# ---------------- Whitelist of names that should be considered "resolved"
# ---------------- even if not explicitly imported in the fragment.

PYTHON_BUILTINS = set(dir(builtins))

# Typing constructs and common stdlib names that pedagogical fragments often
# use without explicit imports. Surfacing these as "missing" produces too much
# noise to be actionable.
TYPING_NAMES = {
    "Any", "Optional", "Union", "Literal", "Tuple", "List", "Dict", "Set",
    "FrozenSet", "Iterable", "Iterator", "Generator", "Callable", "Awaitable",
    "Coroutine", "AsyncIterable", "AsyncIterator", "AsyncGenerator",
    "Mapping", "MutableMapping", "Sequence", "MutableSequence",
    "Type", "TypeVar", "Generic", "ClassVar", "Final", "Protocol",
    "TypedDict", "NamedTuple", "Annotated", "NewType", "cast", "overload",
    "TYPE_CHECKING", "Self", "Never", "Concatenate", "ParamSpec",
    "Unpack", "Required", "NotRequired", "LiteralString",
    # collections.abc convenience
    "Hashable", "Container", "Sized", "Collection", "Reversible",
}

# Conventional sentinel / pedagogical placeholder names; not real undefined names.
PEDAGOGICAL_PLACEHOLDERS = {
    "...",  # ellipsis isn't a Name, but useful conceptually
    "_",    # ignored variable
    "self",  # method receiver
    "cls",   # classmethod receiver
}

# Names that almost always come from a fixture defined earlier in the same
# chapter (printed in prior fragments). Flagging them adds noise.
COMMON_FIXTURE_NAMES = {
    "documents", "queries", "responses", "examples", "samples", "results",
    "dataset", "data", "df", "tokens", "messages", "prompts",
    "chunks", "embeddings", "model", "tokenizer", "logger", "config",
}

# Pre-defined Jupyter / IPython names that often appear without import.
JUPYTER_NAMES = {"display", "HTML", "Markdown", "Image", "Audio", "Video",
                 "get_ipython", "IPython"}


# Library-import map -- canonical "you forgot to import X" patterns where the
# code uses a well-known alias / class name but never imports it.
# Used for the "high-confidence missing imports" section and for the global
# stats roll-up. Each entry: name -> suggested import statement.
COMMON_IMPORT_HINTS: dict[str, str] = {
    "pd": "import pandas as pd",
    "np": "import numpy as np",
    "torch": "import torch",
    "nn": "from torch import nn",
    "F": "import torch.nn.functional as F",
    "tf": "import tensorflow as tf",
    "plt": "import matplotlib.pyplot as plt",
    "sns": "import seaborn as sns",
    "px": "import plotly.express as px",
    "go": "import plotly.graph_objects as go",
    "sk": "import sklearn",
    "json": "import json",
    "re": "import re",
    "os": "import os",
    "sys": "import sys",
    "math": "import math",
    "random": "import random",
    "time": "import time",
    "datetime": "from datetime import datetime",
    "timedelta": "from datetime import timedelta",
    "date": "from datetime import date",
    "Path": "from pathlib import Path",
    "BaseModel": "from pydantic import BaseModel",
    "Field": "from pydantic import Field",
    "validator": "from pydantic import validator",
    "field_validator": "from pydantic import field_validator",
    "ConfigDict": "from pydantic import ConfigDict",
    "dataclass": "from dataclasses import dataclass",
    "field": "from dataclasses import field",
    "asdict": "from dataclasses import asdict",
    "OpenAI": "from openai import OpenAI",
    "AsyncOpenAI": "from openai import AsyncOpenAI",
    "Anthropic": "from anthropic import Anthropic",
    "AsyncAnthropic": "from anthropic import AsyncAnthropic",
    "HuggingFaceEmbeddings": "from langchain_community.embeddings import HuggingFaceEmbeddings",
    "ChatOpenAI": "from langchain_openai import ChatOpenAI",
    "ChatAnthropic": "from langchain_anthropic import ChatAnthropic",
    "PromptTemplate": "from langchain.prompts import PromptTemplate",
    "AutoTokenizer": "from transformers import AutoTokenizer",
    "AutoModel": "from transformers import AutoModel",
    "AutoModelForCausalLM": "from transformers import AutoModelForCausalLM",
    "AutoModelForSeq2SeqLM": "from transformers import AutoModelForSeq2SeqLM",
    "AutoModelForSequenceClassification": "from transformers import AutoModelForSequenceClassification",
    "pipeline": "from transformers import pipeline",
    "Trainer": "from transformers import Trainer",
    "TrainingArguments": "from transformers import TrainingArguments",
    "load_dataset": "from datasets import load_dataset",
    # `Dataset` is ambiguous (torch.utils.data.Dataset vs datasets.Dataset);
    # in the LLMBook corpus the PyTorch variant dominates, so suggest that.
    "Dataset": "from torch.utils.data import Dataset",
    "DataLoader": "from torch.utils.data import DataLoader",
    "TensorDataset": "from torch.utils.data import TensorDataset",
    "FastAPI": "from fastapi import FastAPI",
    "HTTPException": "from fastapi import HTTPException",
    "asyncio": "import asyncio",
    "aiohttp": "import aiohttp",
    "requests": "import requests",
    "httpx": "import httpx",
    "boto3": "import boto3",
    "redis": "import redis",
    "Counter": "from collections import Counter",
    "defaultdict": "from collections import defaultdict",
    "OrderedDict": "from collections import OrderedDict",
    "deque": "from collections import deque",
    "namedtuple": "from collections import namedtuple",
    "lru_cache": "from functools import lru_cache",
    "partial": "from functools import partial",
    "reduce": "from functools import reduce",
    "wraps": "from functools import wraps",
    "chain": "from itertools import chain",
    "combinations": "from itertools import combinations",
    "product": "from itertools import product",
    "groupby": "from itertools import groupby",
    "ABC": "from abc import ABC",
    "abstractmethod": "from abc import abstractmethod",
    "Enum": "from enum import Enum",
    "IntEnum": "from enum import IntEnum",
    "auto": "from enum import auto",
    "ChromaDB": "import chromadb",
    "chromadb": "import chromadb",
    "faiss": "import faiss",
    "pinecone": "import pinecone",
    "weaviate": "import weaviate",
    "qdrant_client": "import qdrant_client",
    "wandb": "import wandb",
    "mlflow": "import mlflow",
    "Image": "from PIL import Image",
    "uuid": "import uuid",
    "hashlib": "import hashlib",
    "pickle": "import pickle",
    "logging": "import logging",
    "argparse": "import argparse",
    "Decimal": "from decimal import Decimal",
}


# ---------------- AST scope analysis ----------------


@dataclass
class ScopeReport:
    imports: set[str] = field(default_factory=set)
    defs: set[str] = field(default_factory=set)
    refs: list[tuple[str, int]] = field(default_factory=list)  # (name, line)
    params: set[str] = field(default_factory=set)


def _add_target_names(target: ast.AST, into: set[str]) -> None:
    """Add bound names from an assignment target (handles tuples / starred)."""
    if isinstance(target, ast.Name):
        into.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            _add_target_names(elt, into)
    elif isinstance(target, ast.Starred):
        _add_target_names(target.value, into)


def _collect_arg_names(args: ast.arguments, into: set[str]) -> None:
    for a in args.args:
        into.add(a.arg)
    for a in args.kwonlyargs:
        into.add(a.arg)
    for a in args.posonlyargs:
        into.add(a.arg)
    if args.vararg is not None:
        into.add(args.vararg.arg)
    if args.kwarg is not None:
        into.add(args.kwarg.arg)


def analyze_tree(tree: ast.AST) -> ScopeReport:
    """Single-pass collection of imports, defs, params, and Name references.

    We treat the whole fragment as one flat scope: this is correct enough for
    pedagogical snippets, which are small and rarely shadow names. The goal is
    to flag obvious missing imports, not to be a strict static checker.
    """
    rep = ScopeReport()

    # First pass: gather all binding sites (imports, defs, params,
    # comprehension targets, assignments). We deliberately collect targets
    # from every assignment statement we see -- short fragments rarely shadow.
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound = alias.asname or alias.name.split(".")[0]
                rep.imports.add(bound)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                bound = alias.asname or alias.name
                if bound == "*":
                    # star imports: we can't know what names came in; record a
                    # marker so we can downweight any unresolved name from this
                    # fragment.
                    rep.imports.add("__star__")
                else:
                    rep.imports.add(bound)
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            rep.defs.add(node.name)
            _collect_arg_names(node.args, rep.params)
        elif isinstance(node, ast.ClassDef):
            rep.defs.add(node.name)
        elif isinstance(node, ast.Lambda):
            _collect_arg_names(node.args, rep.params)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                _add_target_names(t, rep.defs)
        elif isinstance(node, ast.AnnAssign) and node.target is not None:
            _add_target_names(node.target, rep.defs)
        elif isinstance(node, ast.AugAssign):
            _add_target_names(node.target, rep.defs)
        elif isinstance(node, ast.NamedExpr):  # walrus
            _add_target_names(node.target, rep.defs)
        elif isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
            _add_target_names(node.target, rep.defs)
        elif isinstance(node, ast.With) or isinstance(node, ast.AsyncWith):
            for item in node.items:
                if item.optional_vars is not None:
                    _add_target_names(item.optional_vars, rep.defs)
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            for gen in node.generators:
                _add_target_names(gen.target, rep.defs)
        elif isinstance(node, ast.ExceptHandler):
            if node.name:
                rep.defs.add(node.name)
        elif isinstance(node, ast.Global):
            # `global x` should make x resolvable (binding-in-enclosing-scope).
            for n in node.names:
                rep.defs.add(n)
        elif isinstance(node, ast.Nonlocal):
            for n in node.names:
                rep.defs.add(n)

    # Second pass: collect Name references in load context, including the base
    # name of Attribute chains (a.b.c -> we want `a`).
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            rep.refs.append((node.id, getattr(node, "lineno", 0)))
        elif isinstance(node, ast.Attribute):
            # Walk to the base Name of the attribute chain.
            base = node
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name) and isinstance(base.ctx, ast.Load):
                rep.refs.append((base.id, getattr(node, "lineno", 0)))

    return rep


def is_resolvable(name: str, rep: ScopeReport) -> bool:
    if name in rep.imports:
        return True
    if name in rep.defs:
        return True
    if name in rep.params:
        return True
    if name in PYTHON_BUILTINS:
        return True
    if name in TYPING_NAMES:
        return True
    if name in PEDAGOGICAL_PLACEHOLDERS:
        return True
    if name in JUPYTER_NAMES:
        return True
    if "__star__" in rep.imports:
        # An unspecified star-import could plausibly bind this name.
        return True
    return False


# ---------------- HTML extraction ----------------


def iter_python_blocks_in_html(html_path: Path):
    """Yield (line_number, code_text) for each python <pre><code> in the file."""
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
    s = str(tag)[:120]
    idx = text.find(s)
    if idx < 0:
        s = str(tag)[:60]
        idx = text.find(s)
    if idx < 0:
        return 0
    return text.count("\n", 0, idx) + 1


# ---------------- Findings ----------------


@dataclass
class FragmentFinding:
    file: Path
    line: int
    missing: list[tuple[str, int]] = field(default_factory=list)  # (name, line)

    @property
    def names(self) -> list[str]:
        return [n for n, _ in self.missing]


def _seen_filter(refs: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Dedupe by name, keep first occurrence with its line number."""
    seen = {}
    for name, line in refs:
        if name not in seen:
            seen[name] = line
    return [(n, seen[n]) for n in seen]


def audit_file(html_path: Path) -> tuple[int, int, list[FragmentFinding]]:
    """Returns (total_blocks, parsed_blocks, findings_for_this_file)."""
    total = 0
    parsed = 0
    findings: list[FragmentFinding] = []
    for block_line, code in iter_python_blocks_in_html(html_path):
        total += 1
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        parsed += 1
        rep = analyze_tree(tree)
        missing = []
        for name, name_line in _seen_filter(rep.refs):
            if not is_resolvable(name, rep):
                missing.append((name, block_line + max(0, name_line - 1)))
        if missing:
            findings.append(FragmentFinding(
                file=html_path.relative_to(PROJECT_ROOT),
                line=block_line,
                missing=missing,
            ))
    return total, parsed, findings


# ---------------- Report ----------------


def suggest_import(name: str) -> Optional[str]:
    return COMMON_IMPORT_HINTS.get(name)


def write_report(
    findings: list[FragmentFinding],
    total_fragments: int,
    parsed_fragments: int,
) -> None:
    # Aggregate stats.
    name_counter: Counter[str] = Counter()
    name_files: dict[str, set[str]] = defaultdict(set)
    for f in findings:
        for name, _line in f.missing:
            name_counter[name] += 1
            name_files[name].add(f.file.as_posix())

    high_confidence: list[tuple[FragmentFinding, str, int, str]] = []
    # tuple: (finding, name, line, suggested-import)
    for f in findings:
        for name, line in f.missing:
            sug = suggest_import(name)
            if sug:
                high_confidence.append((f, name, line, sug))

    common_fixture_hits: Counter[str] = Counter()
    for f in findings:
        for name, _line in f.missing:
            if name in COMMON_FIXTURE_NAMES:
                common_fixture_hits[name] += 1

    total_flags = sum(len(f.missing) for f in findings)

    lines: list[str] = []
    lines.append("# Missing Imports Audit")
    lines.append("")
    lines.append("Generated by `scripts/_audit_missing_imports.py`.")
    lines.append("")
    lines.append("This audit walks every `<pre><code class=\"...lang-python...\">` block in the book, parses it with `ast.parse`, collects all `Name` and `Attribute` references in load context, and flags any name that is not resolvable via:")
    lines.append("")
    lines.append("- an import in the same fragment, or")
    lines.append("- a local definition (function / class / variable / parameter / comprehension target) in the same fragment, or")
    lines.append("- a Python builtin, or")
    lines.append("- a common `typing` construct (`Any`, `Optional`, `Union`, `Literal`, ...) that pedagogical fragments often use without explicit import.")
    lines.append("")
    lines.append("Fragments that fail to parse are skipped (already covered by the deep-fragment audit).")
    lines.append("")

    # ----- 1. Summary -----
    lines.append("## 1. Summary")
    lines.append("")
    lines.append(f"- Python fragments scanned: **{total_fragments}**")
    lines.append(f"- Python fragments that parsed cleanly: **{parsed_fragments}**")
    lines.append(f"- Fragments with at least one unresolved name: **{len(findings)}**")
    lines.append(f"- Total missing-name flags raised: **{total_flags}**")
    lines.append(f"- Distinct unresolved names: **{len(name_counter)}**")
    lines.append(f"- High-confidence missing-import flags (name matches a known import hint): **{len(high_confidence)}**")
    lines.append("")
    lines.append("### Breakdown by Missing Name (Top 30)")
    lines.append("")
    lines.append("| Name | Occurrences | Distinct files | Suggested import |")
    lines.append("|---|---|---|---|")
    for name, count in name_counter.most_common(30):
        files = len(name_files[name])
        sug = suggest_import(name) or "_(no canonical hint)_"
        lines.append(f"| `{name}` | {count} | {files} | `{sug}` |" if sug != "_(no canonical hint)_"
                     else f"| `{name}` | {count} | {files} | {sug} |")
    lines.append("")

    # ----- 2. High-confidence missing imports -----
    lines.append("## 2. High-Confidence Missing Imports")
    lines.append("")
    lines.append("These flags match a canonical alias / class name in the import-hint table (`pd`, `np`, `torch`, `BaseModel`, `OpenAI`, `Path`, ...). Each row is a high-signal candidate for an auto-fix sweep.")
    lines.append("")
    if not high_confidence:
        lines.append("_None detected._")
    else:
        # Group by file for readability, sorted by file then line.
        high_confidence.sort(key=lambda t: (t[0].file.as_posix(), t[2], t[1]))
        # Limit to 200 rows so the report stays manageable.
        cap = 200
        lines.append(f"_Showing {min(cap, len(high_confidence))} of {len(high_confidence)} high-confidence flags._")
        lines.append("")
        lines.append("| File | Line | Missing name | Suggested import |")
        lines.append("|---|---|---|---|")
        for f, name, line, sug in high_confidence[:cap]:
            lines.append(f"| `{f.file.as_posix()}` | {line} | `{name}` | `{sug}` |")
    lines.append("")

    # ----- 3. Aggregate stats by canonical name -----
    lines.append("## 3. Aggregate Stats by Canonical Name")
    lines.append("")
    lines.append("How widely each known missing-import alias is referenced across files. Targets for a single sweep that adds the canonical import per file.")
    lines.append("")
    lines.append("| Canonical name | Suggested import | Distinct files affected | Total occurrences |")
    lines.append("|---|---|---|---|")
    hint_rows: list[tuple[str, str, int, int]] = []
    for name, sug in COMMON_IMPORT_HINTS.items():
        n_files = len(name_files.get(name, set()))
        n_occ = name_counter.get(name, 0)
        if n_occ:
            hint_rows.append((name, sug, n_files, n_occ))
    hint_rows.sort(key=lambda r: (-r[2], -r[3], r[0]))
    for name, sug, n_files, n_occ in hint_rows[:50]:
        lines.append(f"| `{name}` | `{sug}` | {n_files} | {n_occ} |")
    lines.append("")

    # ----- 4. Other commonly-unresolved names (likely fixtures / context) -----
    lines.append("## 4. Other Frequently-Unresolved Names")
    lines.append("")
    lines.append("Names that are flagged often but do **not** match the import-hint table. These are usually fixtures defined earlier in the same chapter (e.g. `documents`, `queries`, `model`), or examples of bespoke types whose definitions live in a prior fragment. Cross-fragment continuity is by design in this book, so these are mostly noise -- but the very top of this list is worth glancing at for genuine typos.")
    lines.append("")
    other_rows: list[tuple[str, int, int]] = []
    for name, count in name_counter.most_common():
        if name in COMMON_IMPORT_HINTS:
            continue
        n_files = len(name_files[name])
        other_rows.append((name, count, n_files))
    other_rows = other_rows[:40]
    lines.append("| Name | Occurrences | Distinct files | Likely category |")
    lines.append("|---|---|---|---|")
    for name, count, n_files in other_rows:
        if name in COMMON_FIXTURE_NAMES:
            cat = "Cross-fragment fixture"
        elif name[:1].isupper():
            cat = "Type defined earlier"
        else:
            cat = "Variable defined earlier"
        lines.append(f"| `{name}` | {count} | {n_files} | {cat} |")
    lines.append("")

    # ----- 5. Recommended next steps -----
    lines.append("## 5. Recommended Next Steps")
    lines.append("")
    top_hints = hint_rows[:10]
    if top_hints:
        lines.append("Auto-fix sweep candidates, ranked by how many files would gain a correct import (lower-risk first):")
        lines.append("")
        for name, sug, n_files, n_occ in top_hints:
            lines.append(f"1. **`{name}`** -- referenced in {n_files} file(s), {n_occ} occurrence(s). Add `{sug}` at the top of each affected fragment when the fragment is the *first* introduction in its chapter.")
        lines.append("")
    lines.append("Implementation sketch for a sweep:")
    lines.append("")
    lines.append("- Iterate the rows from Section 2 of this report.")
    lines.append("- For each `(file, line, name, suggested import)`, locate the `<pre><code class=\"...lang-python...\">` whose start line is closest to the reported line.")
    lines.append("- If the fragment does not already contain the suggested import statement, prepend it inside the `<pre>` text (preserving syntax-highlight spans is unnecessary -- subsequent rebuilds re-highlight).")
    lines.append("- Re-run this audit; the suggested-import column should drop to zero for these names.")
    lines.append("")
    lines.append("Cross-fragment fixtures (Section 4) should *not* be auto-fixed: they reference data introduced in a prior code fragment in the same chapter, which is by design. A separate audit could verify those fixtures are actually defined upstream in the same chapter file.")
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report to {REPORT_PATH}", file=sys.stderr)


def main() -> int:
    html_files: list[Path] = []
    for path in PROJECT_ROOT.rglob("*.html"):
        if is_excluded(path.relative_to(PROJECT_ROOT)):
            continue
        html_files.append(path)
    print(f"Scanning {len(html_files)} HTML files...", file=sys.stderr)

    all_findings: list[FragmentFinding] = []
    total_fragments = 0
    parsed_fragments = 0
    for html_path in html_files:
        total, parsed, findings = audit_file(html_path)
        total_fragments += total
        parsed_fragments += parsed
        all_findings.extend(findings)

    print(
        f"Scanned {total_fragments} python fragments; {parsed_fragments} parsed; "
        f"{len(all_findings)} fragments with at least one unresolved name",
        file=sys.stderr,
    )
    write_report(all_findings, total_fragments, parsed_fragments)
    return 0


if __name__ == "__main__":
    sys.exit(main())
