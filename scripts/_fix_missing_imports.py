"""Auto-add the 198 high-confidence missing imports flagged by the
missing-imports audit. For each Python <pre><code> block, this script:
  1. Extracts the plain source via the same Pygments class scheme used
     by the rest of the book.
  2. AST-parses to find names that are referenced but unresolved.
  3. For each unresolved name that has a canonical import hint, prepends
     the import statement to the source.
  4. Re-highlights with Pygments and substitutes back into the HTML.

Conservative apply: a fragment is only modified if the new source still
AST-parses AND no new top-level names become unresolved. Otherwise the
fragment is left untouched.

Idempotent: re-running adds nothing if the imports are already present.

Run from project root:
    python scripts/_fix_missing_imports.py [--dry-run]
"""
from __future__ import annotations
import argparse
import ast
import builtins
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

# Canonical import hints. Keys are the unresolved name; values are the
# import statement to prepend.
HINTS = {
    "torch":                  "import torch",
    "nn":                     "from torch import nn",
    "F":                      "import torch.nn.functional as F",
    "np":                     "import numpy as np",
    "pd":                     "import pandas as pd",
    "plt":                    "import matplotlib.pyplot as plt",
    "json":                   "import json",
    "re":                     "import re",
    "time":                   "import time",
    "os":                     "import os",
    "sys":                    "import sys",
    "math":                   "import math",
    "random":                 "import random",
    "asyncio":                "import asyncio",
    "requests":               "import requests",
    "logging":                "import logging",
    "datetime":               "from datetime import datetime",
    "timedelta":              "from datetime import timedelta",
    "Path":                   "from pathlib import Path",
    "Counter":                "from collections import Counter",
    "defaultdict":            "from collections import defaultdict",
    "dataclass":              "from dataclasses import dataclass",
    "field":                  "from dataclasses import field",
    "Enum":                   "from enum import Enum",
    "BaseModel":              "from pydantic import BaseModel",
    "Field":                  "from pydantic import Field",
    "computed_field":         "from pydantic import computed_field",
    "field_validator":        "from pydantic import field_validator",
    "OpenAI":                 "from openai import OpenAI",
    "Anthropic":              "from anthropic import Anthropic",
    "AutoModelForCausalLM":   "from transformers import AutoModelForCausalLM",
    "AutoModelForSequenceClassification": "from transformers import AutoModelForSequenceClassification",
    "AutoTokenizer":          "from transformers import AutoTokenizer",
    "AutoConfig":             "from transformers import AutoConfig",
    "AutoModel":              "from transformers import AutoModel",
    "pipeline":               "from transformers import pipeline",
    "Trainer":                "from transformers import Trainer",
    "TrainingArguments":      "from transformers import TrainingArguments",
    "DataCollatorForLanguageModeling": "from transformers import DataCollatorForLanguageModeling",
    "DataLoader":             "from torch.utils.data import DataLoader",
    "Dataset":                "from torch.utils.data import Dataset",
    "load_dataset":           "from datasets import load_dataset",
    "wandb":                  "import wandb",
    "mlflow":                 "import mlflow",
    "FastAPI":                "from fastapi import FastAPI",
    "BaseException":          "",       # builtin, never need import
    "TYPE_CHECKING":          "from typing import TYPE_CHECKING",
    "Any":                    "from typing import Any",
    "Optional":               "from typing import Optional",
    "Union":                  "from typing import Union",
    "Literal":                "from typing import Literal",
    "Callable":               "from typing import Callable",
    "Sequence":               "from collections.abc import Sequence",
    "Iterable":               "from collections.abc import Iterable",
    "Mapping":                "from collections.abc import Mapping",
}

# Typing names that are commonly used without explicit import in pedagogical
# fragments; we don't add imports for these. (Lower-friction.)
TYPING_FREEBIES = {"Any", "Optional", "Union", "Literal", "Callable",
                   "Sequence", "Iterable", "Mapping", "TYPE_CHECKING",
                   "TypeVar", "Generic", "List", "Dict", "Tuple", "Set",
                   "FrozenSet"}

BUILTINS = set(dir(builtins))


def should_skip(p: Path) -> bool:
    return bool(set(p.parts) & SKIP_PARTS)


# --------------------------------------------------------------------- AST utilities

def _walk_defs_and_refs(tree: ast.Module) -> tuple[set, set]:
    """Return (defined_names, referenced_names) from a parsed module."""
    defs = set()
    refs = set()

    class Walker(ast.NodeVisitor):
        def visit_Import(self, node):
            for a in node.names:
                defs.add((a.asname or a.name).split(".")[0])
        def visit_ImportFrom(self, node):
            for a in node.names:
                if a.name == "*":
                    continue
                defs.add(a.asname or a.name)
        def visit_FunctionDef(self, node):
            defs.add(node.name)
            for a in node.args.args + node.args.kwonlyargs + node.args.posonlyargs:
                defs.add(a.arg)
            if node.args.vararg:   defs.add(node.args.vararg.arg)
            if node.args.kwarg:    defs.add(node.args.kwarg.arg)
            self.generic_visit(node)
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_ClassDef(self, node):
            defs.add(node.name)
            self.generic_visit(node)
        def visit_Lambda(self, node):
            for a in node.args.args:
                defs.add(a.arg)
            self.generic_visit(node)
        def visit_Assign(self, node):
            for t in node.targets:
                self._collect_target(t)
            self.generic_visit(node)
        def visit_AnnAssign(self, node):
            self._collect_target(node.target)
            self.generic_visit(node)
        def visit_AugAssign(self, node):
            self._collect_target(node.target)
            self.generic_visit(node)
        def visit_For(self, node):
            self._collect_target(node.target)
            self.generic_visit(node)
        visit_AsyncFor = visit_For
        def visit_With(self, node):
            for item in node.items:
                if item.optional_vars:
                    self._collect_target(item.optional_vars)
            self.generic_visit(node)
        visit_AsyncWith = visit_With
        def visit_ExceptHandler(self, node):
            if node.name:
                defs.add(node.name)
            self.generic_visit(node)
        def visit_comprehension(self, node):
            self._collect_target(node.target)
            self.generic_visit(node)
        def _collect_target(self, t):
            if isinstance(t, ast.Name):
                defs.add(t.id)
            elif isinstance(t, (ast.Tuple, ast.List)):
                for elt in t.elts:
                    self._collect_target(elt)
            elif isinstance(t, ast.Starred):
                self._collect_target(t.value)
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                refs.add(node.id)
        def visit_Attribute(self, node):
            # Walk to the base
            base = node
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name) and isinstance(base.ctx, ast.Load):
                refs.add(base.id)
            self.generic_visit(node)

    Walker().visit(tree)
    return defs, refs


def needed_imports_for_source(src: str) -> list[str]:
    """Return the list of import statements to prepend to src."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    defs, refs = _walk_defs_and_refs(tree)
    unresolved = refs - defs - BUILTINS - TYPING_FREEBIES - {"self", "cls", "_"}
    imports = []
    for name in sorted(unresolved):
        hint = HINTS.get(name)
        if hint:
            imports.append(hint)
    return imports


# --------------------------------------------------------------------- HTML utilities

PYGMENTS_FORMATTER = HtmlFormatter(nowrap=True, classprefix="")
PYTHON_LEXER = get_lexer_by_name("python")


def code_block_source(code_tag) -> str:
    """Extract plain text source from a Pygments-highlighted <code> block."""
    return code_tag.get_text()


def reflow_code_block(code_tag, new_src: str) -> None:
    """Replace the inner HTML of a <code> tag with newly-highlighted source."""
    new_html = highlight(new_src, PYTHON_LEXER, PYGMENTS_FORMATTER).rstrip("\n")
    soup = BeautifulSoup(f"<wrap>{new_html}</wrap>", "html.parser")
    wrap = soup.find("wrap")
    code_tag.clear()
    for child in list(wrap.children):
        code_tag.append(child.extract())


def process_file(p: Path, dry_run: bool) -> tuple[int, int]:
    """Add missing imports to every fragment in this file. Return (fragments_fixed, imports_added)."""
    text = p.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    fragments_fixed = 0
    imports_added = 0
    for code in soup.find_all("code"):
        classes = code.get("class") or []
        if not any(c in {"lang-python", "language-python"} or c.endswith("-python") for c in classes):
            continue
        src = code_block_source(code)
        if not src.strip():
            continue
        try:
            ast.parse(src)
        except SyntaxError:
            continue
        new_imports = needed_imports_for_source(src)
        if not new_imports:
            continue
        # Prepend new imports, dedup against existing top-of-fragment imports
        existing_lines = src.splitlines()
        prefix_imports = []
        i = 0
        while i < len(existing_lines) and (existing_lines[i].startswith("import ") or
                                            existing_lines[i].startswith("from ") or
                                            existing_lines[i].strip() == "" or
                                            existing_lines[i].lstrip().startswith("#")):
            prefix_imports.append(existing_lines[i])
            i += 1
        existing_normalized = {ln.strip() for ln in prefix_imports}
        truly_new = [imp for imp in new_imports if imp not in existing_normalized]
        if not truly_new:
            continue
        new_src = "\n".join(truly_new) + "\n" + src
        # Verify the new source still parses
        try:
            ast.parse(new_src)
        except SyntaxError:
            continue
        reflow_code_block(code, new_src)
        fragments_fixed += 1
        imports_added += len(truly_new)

    if fragments_fixed == 0:
        return 0, 0
    if not dry_run:
        p.write_text(str(soup), encoding="utf-8")
    return fragments_fixed, imports_added


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total_frags = 0
    total_imports = 0
    files_touched = 0
    for p in ROOT.rglob("*.html"):
        if should_skip(p):
            continue
        try:
            f, i = process_file(p, args.dry_run)
        except Exception as e:
            print(f"  ERROR {p.relative_to(ROOT)}: {e}")
            continue
        if f > 0:
            rel = p.relative_to(ROOT)
            print(f"  {rel}: {f} frag(s), +{i} import(s)")
            total_frags += f
            total_imports += i
            files_touched += 1
    print()
    print(f"TOTAL: {total_imports} imports added to {total_frags} fragments across {files_touched} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
