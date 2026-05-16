"""Audit every <pre><code> block in the LLMBook for technical correctness.

Read-only — produces a structured Markdown report at
E:/Projects/BookBlogsHome/LLMBook/code-correctness-audit.md
"""
from __future__ import annotations

import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

try:
    import yaml
except ImportError:
    yaml = None


ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_PARTS = {
    "node_modules",
    ".git",
    "KDP",
    "build",
    "temp_ebook",
    "temp_epub",
    "source_fix_backups",
    "pagefind",
    "templates",
    ".claude",
    ".book-update",
}


# ----------------------------------------------------------------------
# Findings storage
# ----------------------------------------------------------------------
class F:
    files_scanned = 0
    scanned = 0
    missing_lang_class: list = []  # (file, line_no, snippet_preview)
    py_indent_loss: list = []      # (file, line_no, snippet)
    py_other_syntax: list = []     # (file, line_no, err, snippet)
    mislabeled_shell: list = []    # (file, line_no, snippet) -- lang-python but bash
    mislabeled_yaml: list = []     # (file, line_no, snippet)
    mislabeled_other: list = []    # (file, line_no, what, snippet)
    pseudocode_as_python: list = []
    yaml_errors: list = []         # (file, line_no, err, snippet)
    json_errors: list = []
    p0_stale: list = []
    p1_stale: list = []
    unresolvable_pkgs: list = []
    mismatches: list = []
    lang_counts = defaultdict(int)
    pattern_counts = defaultdict(int)


# ----------------------------------------------------------------------
# Stale-API patterns
# ----------------------------------------------------------------------
P0_PATTERNS = [
    (r"\bopenai\.ChatCompletion\.create\b",
     "openai.ChatCompletion.create (removed in openai>=1.0; use client.chat.completions.create)"),
    (r"\bopenai\.Completion\.create\b",
     "openai.Completion.create (removed in openai>=1.0; use legacy client.completions.create only for completion-model APIs)"),
    (r"\bopenai\.Embedding\.create\b",
     "openai.Embedding.create (removed in openai>=1.0; use client.embeddings.create)"),
    (r"^\s*openai\.api_key\s*=", "openai.api_key = ... (legacy v0; use OpenAI(api_key=...) client)"),
    (r"\bclaude-2(?:\.\d+)?\b",
     "claude-2 / claude-2.x model id (deprecated; use claude-3.5-sonnet / claude-3-7-sonnet / claude-4 family)"),
    (r"\bclaude-instant(?:-v1)?\b", "claude-instant (deprecated/retired)"),
    (r"^\s*from\s+langchain\s+import\s+(?:LLMChain|ConversationChain|SequentialChain|SimpleSequentialChain|OpenAI|ChatOpenAI|PromptTemplate|HumanMessage|AIMessage|SystemMessage)\b",
     "from langchain import <legacy> (use langchain_core / langchain_community / langchain_openai paths)"),
    (r"^\s*from\s+langchain\.llms\s+import",
     "langchain.llms (legacy; use langchain_community.llms or provider-specific package)"),
    (r"^\s*from\s+langchain\.chat_models\s+import",
     "langchain.chat_models (legacy; use langchain_openai/langchain_anthropic etc.)"),
    (r"^\s*from\s+langchain\.embeddings\s+import",
     "langchain.embeddings (legacy; use langchain_community.embeddings or provider-specific)"),
    (r"\buse_auth_token\s*=",
     "use_auth_token= (deprecated in transformers>=4.40; use token=)"),
    (r"\bprepare_model_for_int8_training\b",
     "prepare_model_for_int8_training (deprecated; use prepare_model_for_kbit_training)"),
    (r"\btext-davinci-(?:002|003)\b",
     "text-davinci-002/003 (deprecated/retired models)"),
    (r"\bcode-davinci-002\b", "code-davinci-002 (deprecated/retired)"),
]

P1_PATTERNS = [
    (r"\bLLMChain\s*\(",
     "LLMChain( (deprecated in langchain>=0.1, removed in 0.3; use LCEL: prompt | llm | parser)"),
    (r"\bConversationChain\s*\(",
     "ConversationChain( (deprecated; use RunnableWithMessageHistory)"),
    (r"\bgpt-3\.5-turbo(?:-\w+)?\b",
     "gpt-3.5-turbo (works but discouraged in 2025+; prefer gpt-4o-mini / gpt-4.1-nano)"),
    (r"\bevaluation_strategy\s*=",
     "evaluation_strategy= (renamed eval_strategy in transformers>=4.41)"),
    (r"\btorch\.cuda\.amp\.autocast\b",
     "torch.cuda.amp.autocast (deprecated in torch>=2.4; use torch.amp.autocast('cuda'))"),
    (r"\btorch\.cuda\.amp\.GradScaler\b",
     "torch.cuda.amp.GradScaler (deprecated in torch>=2.4; use torch.amp.GradScaler('cuda'))"),
    (r"OpenAI-Beta\s*:\s*assistants=v1",
     "OpenAI Assistants v1 header (v2 is current as of late-2024)"),
    (r"\bclient\.beta\.threads\.runs\.create\b.*assistant_id",
     "Assistants API (deprecated in 2026 H1 in favor of Responses API; still supported)"),
]

SUSPICIOUS_PACKAGES = {
    # Clearly wrong / typos
    "tools-of-trade", "tools_of_trade",
    "openai-agents-sdk", "openai_agents_sdk",  # canonical name is "openai-agents"
    "anthropic-sdk", "anthropic_sdk",          # canonical name is "anthropic"
    "claude-sdk", "claude_sdk",
    "vercel-ai",  # not a python pkg
    "your-package-here", "your-package", "fake-package",
}


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def is_in_skip(path: Path) -> bool:
    return bool(set(path.parts) & SKIP_PARTS)


def get_line_no(source: str, char_offset: int) -> int:
    return source.count("\n", 0, char_offset) + 1


def normalize_lang(class_attr) -> str | None:
    if not class_attr:
        return None
    classes = class_attr if isinstance(class_attr, list) else class_attr.split()
    for c in classes:
        if c.startswith("lang-"):
            return c[5:].lower()
        if c.startswith("language-"):
            return c[9:].lower()
    return None


SHELL_PROMPT = re.compile(r"^\s*\$\s+|^\s*#!\s*/")
SHELL_CMD = re.compile(
    r"^\s*(?:pip|uv|poetry|npm|pnpm|yarn|docker|kubectl|helm|git|curl|wget|chmod|chown|"
    r"export|cd|mkdir|rm|ls|cat|grep|sed|awk|find|conda|mamba|brew|apt|apt-get|"
    r"systemctl|service|sudo|trivy|cosign|syft|wandb|huggingface-cli|mlx_lm|"
    r"gcloud|aws|az|terraform|ansible|make|cmake|node|deno|bun|tar|gzip|unzip|"
    r"python(?:3)?\s+-m|hf|llama-server|ollama|modal)\b"
)
PSEUDOCODE_HDR = re.compile(r"^\s*(?:Input|Output|Algorithm|Procedure|Pseudocode|Function)\s*:", re.IGNORECASE)
NON_PY_NUM_OPS = re.compile(r"[·×→←≤≥≠∈∉∀∃∑∏∫∂∇αβγδλμπσφψω]")


def classify_python_failure(code: str) -> tuple[str, str | None]:
    """Classify why this 'python' block failed to parse.

    Returns (category, sample_first_line) where category is one of:
      - "indent-loss"     : Python lost leading indentation (real authoring bug)
      - "shell"           : it's actually shell/bash mistagged
      - "yaml"            : looks like Kubernetes/Compose YAML mistagged
      - "markdown"        : looks like Markdown / prose mistagged
      - "typescript"      : JS/TS mistagged
      - "pseudocode"      : starts with Input:/Output:/etc. or math glyphs
      - "f-string-broken" : looks like a multi-line broken f-string
      - "other"           : real syntax error (e.g. truncated example)
    """
    lines_all = code.splitlines()
    lines = [l for l in lines_all if l.strip()]
    if not lines:
        return "empty", None
    first = lines[0].strip()
    if PSEUDOCODE_HDR.match(first):
        return "pseudocode", first[:80]
    if NON_PY_NUM_OPS.search(code):
        return "pseudocode", first[:80]
    shell_hits = sum(1 for l in lines if SHELL_PROMPT.match(l) or SHELL_CMD.match(l))
    if shell_hits / len(lines) > 0.3:
        return "shell", first[:80]
    if "apiVersion:" in code or "kind:" in code:
        return "yaml", first[:80]
    # TS / JS detect: `import { foo } from '...'` or `const x = ...; //`
    if re.search(r"import\s+\{[^}]+\}\s+from\s+['\"]", code) or "=>" in code or "// " in code.split("\n", 1)[0]:
        if "//" in code or "=>" in code:
            return "typescript", first[:80]
    # Markdown / prose mistagged: ## headings, bullet-style outside code, or "I" pronoun
    md_hits = sum(1 for l in lines if l.lstrip().startswith("## ") or l.lstrip().startswith("- "))
    if md_hits / len(lines) > 0.3:
        return "markdown", first[:80]
    # Broken f-string heuristic: a line that ends with print(f" or  f' and the next line doesn't close it
    for i, line in enumerate(lines_all[:-1]):
        if re.search(r'f["\']\s*$', line.rstrip()):
            return "f-string-broken", line.strip()[:80]
    # Indent-loss heuristic: open-block followed by line with same-or-less indent
    for i, line in enumerate(lines[:-1]):
        stripped = line.strip()
        if stripped.endswith(":") and re.match(
            r"^\s*(?:class|def|if|elif|else|for|while|with|try|except|finally|async)\b", stripped
        ):
            cur_indent = len(line) - len(line.lstrip())
            nxt = lines[i + 1]
            nxt_indent = len(nxt) - len(nxt.lstrip())
            if nxt_indent <= cur_indent:
                return "indent-loss", stripped[:80]
    return "other", first[:80]


def check_python(code: str):
    """Try to parse. Returns (ok, error-message, error-line)."""
    cleaned = re.sub(r"^\s*>>>\s?", "", code, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*\.\.\.\s?", "", cleaned, flags=re.MULTILINE)
    try:
        ast.parse(cleaned)
        return True, None, None
    except SyntaxError as e:
        return False, f"{type(e).__name__}: {e.msg}", e.lineno
    except ValueError as e:
        return False, f"ValueError: {e}", None


def check_json(code: str):
    code = code.strip()
    if not code or not (code.startswith("{") or code.startswith("[")):
        return True, None
    try:
        json.loads(code)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"JSONDecodeError: {e.msg} (line {e.lineno}, col {e.colno})"


def check_yaml(code: str):
    if yaml is None:
        return True, None
    try:
        list(yaml.safe_load_all(code))
        return True, None
    except yaml.YAMLError as e:
        return False, f"YAMLError: {str(e).splitlines()[0]}"


PROSE_PROMISE = re.compile(
    r"\b(Adam|AdamW|SGD|Adagrad|Adafactor|RMSprop|Lion)\s+optimizer\b",
    re.IGNORECASE,
)


def detect_python_optimizer(code: str) -> set[str]:
    found = set()
    for name in ["AdamW", "Adam", "SGD", "Adagrad", "Adafactor", "RMSprop", "Lion"]:
        if re.search(rf"\b{name}\s*\(", code):
            found.add(name)
    return found


def get_surrounding_prose(pre_tag, radius_chars=400) -> str:
    parts = []
    sib = pre_tag.previous_sibling
    collected = 0
    while sib is not None and collected < radius_chars:
        text = sib.get_text(" ", strip=True) if hasattr(sib, "get_text") else str(sib).strip()
        if text:
            parts.insert(0, text)
            collected += len(text)
        sib = sib.previous_sibling
    if pre_tag.parent and pre_tag.parent.previous_sibling and collected < radius_chars:
        p = pre_tag.parent.previous_sibling
        if hasattr(p, "get_text"):
            parts.insert(0, p.get_text(" ", strip=True))
    return " ".join(parts)[-radius_chars:]


def audit_file(path: Path):
    F.files_scanned += 1
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"READ-ERR {path}: {e}", file=sys.stderr)
        return

    soup = BeautifulSoup(source, "html.parser")
    pres = soup.find_all("pre")
    pre_positions = [m.start() for m in re.finditer(r"<pre\b", source, re.IGNORECASE)]
    pre_idx = 0

    for pre in pres:
        F.scanned += 1
        line_no = None
        if pre_idx < len(pre_positions):
            line_no = get_line_no(source, pre_positions[pre_idx])
            pre_idx += 1

        code = pre.find("code")
        if code is None:
            text = pre.get_text()
            lang = normalize_lang(pre.get("class"))
        else:
            text = code.get_text()
            lang = normalize_lang(code.get("class")) or normalize_lang(pre.get("class"))

        F.lang_counts[lang or "NONE"] += 1
        rel = path.relative_to(ROOT).as_posix()
        preview = (text[:120] or "").replace("\n", " ⏎ ").strip()

        # ---- Missing lang-XXX class ----
        if lang is None:
            F.missing_lang_class.append((rel, line_no, preview[:100]))

        # ---- Syntax + classification ----
        if lang in ("python", "py"):
            ok, err, eline = check_python(text)
            if not ok:
                cat, snip = classify_python_failure(text)
                location = (rel, line_no, snip or preview[:100])
                if cat == "indent-loss":
                    F.py_indent_loss.append(location)
                elif cat == "shell":
                    F.mislabeled_shell.append(location)
                elif cat == "yaml":
                    F.mislabeled_yaml.append(location)
                elif cat in ("markdown", "typescript"):
                    F.mislabeled_other.append((rel, line_no, cat, snip or preview[:100]))
                elif cat == "pseudocode":
                    F.pseudocode_as_python.append(location)
                elif cat == "f-string-broken":
                    F.py_other_syntax.append((rel, line_no, f"broken multiline f-string: {err}", snip or preview[:100]))
                else:
                    F.py_other_syntax.append((rel, line_no, err, snip or preview[:100]))

        elif lang == "json":
            ok, err = check_json(text)
            if not ok:
                F.json_errors.append((rel, line_no, err, preview[:100]))
        elif lang in ("yaml", "yml"):
            ok, err = check_yaml(text)
            if not ok:
                F.yaml_errors.append((rel, line_no, err, preview[:100]))

        # ---- P0/P1 stale API patterns (apply to all langs) ----
        for pat, label in P0_PATTERNS:
            m = re.search(pat, text, re.MULTILINE)
            if m:
                start = text.rfind("\n", 0, m.start()) + 1
                end = text.find("\n", m.end())
                if end == -1:
                    end = len(text)
                ctx = text[start:end].strip()
                F.p0_stale.append((rel, line_no, label, ctx[:160]))
                F.pattern_counts[label] += 1

        for pat, label in P1_PATTERNS:
            m = re.search(pat, text, re.MULTILINE)
            if m:
                start = text.rfind("\n", 0, m.start()) + 1
                end = text.find("\n", m.end())
                if end == -1:
                    end = len(text)
                ctx = text[start:end].strip()
                F.p1_stale.append((rel, line_no, label, ctx[:160]))
                F.pattern_counts[label] += 1

        # ---- Suspicious packages ----
        for line in text.splitlines():
            ls = line.strip()
            m = re.search(r"(?:pip(?:3)?|uv|poetry)\s+(?:install|add)\s+(.+)", ls)
            if m:
                args = m.group(1).split()
                for a in args:
                    a = a.strip(",")
                    if a.startswith("-") or "/" in a:
                        continue
                    base = re.split(r"[\[<>=!~]", a, maxsplit=1)[0].strip().lower()
                    if base in SUSPICIOUS_PACKAGES:
                        F.unresolvable_pkgs.append((rel, line_no, base, ls[:140]))
            m2 = re.match(r"(?:from|import)\s+([\w\-]+)", ls)
            if m2:
                base = m2.group(1).replace("_", "-").lower()
                if base in SUSPICIOUS_PACKAGES:
                    F.unresolvable_pkgs.append((rel, line_no, base, ls[:140]))

        # ---- Code/prose mismatch (optimizer heuristic) ----
        if lang in ("python", "py"):
            prose = get_surrounding_prose(pre)
            promised = PROSE_PROMISE.search(prose)
            if promised:
                pname = promised.group(1).lower()
                actual = detect_python_optimizer(text)
                if actual:
                    matched = False
                    if pname == "adam" and any(a.lower() in ("adam", "adamw") for a in actual):
                        matched = True
                    elif pname == "adamw" and "AdamW" in actual:
                        matched = True
                    elif pname == "sgd" and "SGD" in actual:
                        matched = True
                    elif pname.lower() in {a.lower() for a in actual}:
                        matched = True
                    if not matched:
                        F.mismatches.append(
                            (rel, line_no, f"prose says '{promised.group(0)}'", f"code uses {sorted(actual)}")
                        )


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------
def by_part(items):
    """Group rel-path findings by top-level book part."""
    g = defaultdict(int)
    for tup in items:
        rel = tup[0]
        part = rel.split("/", 1)[0]
        g[part] += 1
    return g


def section(out, title, items, fmt, limit=60):
    out.append(f"\n## {title}")
    out.append(f"_{len(items)} total._\n")
    if not items:
        out.append("_None found._")
        return
    for tup in items[:limit]:
        out.append(fmt(tup))
    if len(items) > limit:
        out.append(f"- ...and {len(items)-limit} more")


def main():
    files = [p for p in ROOT.rglob("*.html") if not is_in_skip(p)]
    for f in files:
        audit_file(f)

    total_python_syntax_failures = (
        len(F.py_indent_loss)
        + len(F.py_other_syntax)
        + len(F.mislabeled_shell)
        + len(F.mislabeled_yaml)
        + len(F.mislabeled_other)
        + len(F.pseudocode_as_python)
    )

    out = ["# Code Correctness Audit", ""]
    out.append("_Read-only audit of every `<pre><code>` block under "
               "`E:/Projects/BookBlogsHome/LLMBook`. "
               "Generated by `scripts/audit_code_blocks.py`. "
               "No source files were modified._\n")

    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------
    out.append("## Summary")
    out.append(f"- HTML files scanned: **{F.files_scanned}**")
    out.append(f"- Code blocks scanned: **{F.scanned}**")
    out.append("")
    out.append("**Real defects (recommend fixing):**")
    out.append(f"- Python blocks with **lost indentation** (visible bug): **{len(F.py_indent_loss)}**")
    out.append(f"- Python blocks with other real syntax errors: **{len(F.py_other_syntax)}**")
    out.append(f"- Blocks **mislabeled** `lang-python` but actually shell/bash: **{len(F.mislabeled_shell)}**")
    out.append(f"- Blocks **mislabeled** `lang-python` but actually YAML: **{len(F.mislabeled_yaml)}**")
    out.append(f"- Blocks **mislabeled** `lang-python` but actually Markdown/TypeScript: **{len(F.mislabeled_other)}**")
    out.append(f"- YAML blocks with parse errors (mostly template-laden GH Actions): **{len(F.yaml_errors)}**")
    out.append(f"- JSON blocks with parse errors: **{len(F.json_errors)}**")
    out.append(f"- Stale APIs (P0, removed in current major versions): **{len(F.p0_stale)}**")
    out.append(f"- Stale APIs (P1, deprecated but still functional): **{len(F.p1_stale)}**")
    out.append(f"- Unresolvable / typo packages: **{len(F.unresolvable_pkgs)}**")
    out.append(f"- Code/prose mismatches (optimizer heuristic): **{len(F.mismatches)}**")
    out.append(f"- Missing `lang-XXX` class: **{len(F.missing_lang_class)}**")
    out.append("")
    out.append("**Likely-false-positives (excluded from defect count):**")
    out.append(f"- Pseudocode/prose tagged `lang-python` (no real fix needed beyond reclassifying): **{len(F.pseudocode_as_python)}**")
    out.append("")
    out.append(f"_Total Python syntax-check failures (all categories): {total_python_syntax_failures}_")
    out.append("")

    # Language distribution
    out.append("### Language tag distribution")
    out.append("| lang | count |")
    out.append("|------|------:|")
    for lang, n in sorted(F.lang_counts.items(), key=lambda kv: -kv[1]):
        out.append(f"| `{lang}` | {n} |")
    out.append("")

    # -----------------------------------------------------------------
    # P0
    # -----------------------------------------------------------------
    out.append("## P0 stale API (deprecated/removed)")
    if F.p0_stale:
        by_label = defaultdict(list)
        for rel, ln, label, ctx in F.p0_stale:
            by_label[label].append((rel, ln, ctx))
        for label, items in sorted(by_label.items(), key=lambda kv: -len(kv[1])):
            out.append(f"\n### {label}  _({len(items)} occurrences)_")
            for rel, ln, ctx in items[:40]:
                out.append(f"- `{rel}:{ln}` — `{ctx}`")
            if len(items) > 40:
                out.append(f"- ...and {len(items)-40} more")
    else:
        out.append("_None found._")
    out.append("")

    # -----------------------------------------------------------------
    # P1
    # -----------------------------------------------------------------
    out.append("## P1 stale API (works but discouraged)")
    if F.p1_stale:
        by_label = defaultdict(list)
        for rel, ln, label, ctx in F.p1_stale:
            by_label[label].append((rel, ln, ctx))
        for label, items in sorted(by_label.items(), key=lambda kv: -len(kv[1])):
            out.append(f"\n### {label}  _({len(items)} occurrences)_")
            for rel, ln, ctx in items[:30]:
                out.append(f"- `{rel}:{ln}` — `{ctx}`")
            if len(items) > 30:
                out.append(f"- ...and {len(items)-30} more")
    else:
        out.append("_None found._")
    out.append("")

    # -----------------------------------------------------------------
    # Python indent-loss
    # -----------------------------------------------------------------
    out.append("## Python blocks with lost indentation (real bug)")
    out.append("")
    out.append(
        "Pygments-highlighted output dropped leading whitespace, so the code as "
        "displayed in the HTML cannot run. Pattern: `class Foo:` is followed by "
        "an unindented method/attribute. Fix once by regenerating pygments output "
        "with `prestyles=` or by re-running the source preprocessor."
    )
    if F.py_indent_loss:
        bypart = by_part(F.py_indent_loss)
        out.append("\n**Distribution by part:**")
        for part, n in sorted(bypart.items(), key=lambda kv: -kv[1]):
            out.append(f"- `{part}` — {n}")
        out.append("\n**Top affected files (first 40 occurrences):**")
        for rel, ln, snip in F.py_indent_loss[:40]:
            out.append(f"- `{rel}:{ln}` — `{snip}`")
        if len(F.py_indent_loss) > 40:
            out.append(f"- ...and {len(F.py_indent_loss)-40} more")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # Python other syntax errors
    # -----------------------------------------------------------------
    out.append("## Python blocks with other syntax errors")
    out.append("Real defects beyond indent loss: truncated examples, broken "
               "multi-line f-strings, decorators with no body, etc.")
    out.append("")
    if F.py_other_syntax:
        for rel, ln, err, snip in F.py_other_syntax[:50]:
            out.append(f"- `{rel}:{ln}` — {err} — `{snip}`")
        if len(F.py_other_syntax) > 50:
            out.append(f"- ...and {len(F.py_other_syntax)-50} more")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # Mislabeled shell
    # -----------------------------------------------------------------
    out.append("## Mislabeled `lang-python` blocks (actually shell/bash)")
    out.append("These are real shell commands tagged as Python. Highlighting is wrong; "
               "reading by screen readers / colorizers is incorrect.")
    out.append("")
    if F.mislabeled_shell:
        for rel, ln, snip in F.mislabeled_shell[:30]:
            out.append(f"- `{rel}:{ln}` — `{snip}`")
        if len(F.mislabeled_shell) > 30:
            out.append(f"- ...and {len(F.mislabeled_shell)-30} more")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # Mislabeled YAML
    # -----------------------------------------------------------------
    out.append("## Mislabeled `lang-python` blocks (actually YAML)")
    if F.mislabeled_yaml:
        for rel, ln, snip in F.mislabeled_yaml:
            out.append(f"- `{rel}:{ln}` — `{snip}`")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # Mislabeled Markdown / TS
    # -----------------------------------------------------------------
    out.append("## Mislabeled `lang-python` blocks (Markdown / TypeScript / JS)")
    if F.mislabeled_other:
        for rel, ln, what, snip in F.mislabeled_other:
            out.append(f"- `{rel}:{ln}` — actually **{what}** — `{snip}`")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # Pseudocode as python
    # -----------------------------------------------------------------
    out.append("## Pseudocode tagged `lang-python` (cosmetic — consider `lang-text`)")
    if F.pseudocode_as_python:
        for rel, ln, snip in F.pseudocode_as_python[:30]:
            out.append(f"- `{rel}:{ln}` — `{snip}`")
        if len(F.pseudocode_as_python) > 30:
            out.append(f"- ...and {len(F.pseudocode_as_python)-30} more")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # YAML errors
    # -----------------------------------------------------------------
    out.append("## YAML blocks with parse errors")
    out.append("Some failures here are legitimate: GitHub Actions templating, "
               "indentation issues, or comment-stripping artifacts. Spot-check before fixing.")
    out.append("")
    if F.yaml_errors:
        for rel, ln, err, snip in F.yaml_errors:
            out.append(f"- `{rel}:{ln}` — {err}")
            out.append(f"  `{snip}`")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # JSON
    # -----------------------------------------------------------------
    out.append("## JSON blocks with parse errors")
    if F.json_errors:
        for rel, ln, err, snip in F.json_errors:
            out.append(f"- `{rel}:{ln}` — {err} — `{snip}`")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # Unresolvable packages
    # -----------------------------------------------------------------
    out.append("## Unresolvable / typo packages")
    if F.unresolvable_pkgs:
        for rel, ln, pkg, line in F.unresolvable_pkgs[:100]:
            out.append(f"- `{rel}:{ln}` — `{pkg}` — `{line}`")
    else:
        out.append("_None._")
    out.append("")

    # -----------------------------------------------------------------
    # Mismatches
    # -----------------------------------------------------------------
    out.append("## Code / prose mismatches (optimizer heuristic)")
    if F.mismatches:
        for rel, ln, prose, code_obs in F.mismatches[:50]:
            out.append(f"- `{rel}:{ln}` — {prose}; {code_obs}")
    else:
        out.append("_None found by optimizer heuristic._")
    out.append("")

    # -----------------------------------------------------------------
    # Missing lang-XXX class
    # -----------------------------------------------------------------
    out.append("## Missing `lang-XXX` class")
    out.append(f"**{len(F.missing_lang_class)} blocks** lack a `lang-*` / `language-*` class. "
               "These are mostly output/trace blocks that should be tagged `lang-text` "
               "for screen-reader behavior and to disable syntax highlighting.")
    out.append("")
    by_file_missing = defaultdict(int)
    for rel, _, _ in F.missing_lang_class:
        by_file_missing[rel] += 1
    out.append("**Top files by missing-class count:**")
    for rel, n in sorted(by_file_missing.items(), key=lambda kv: -kv[1])[:30]:
        out.append(f"- `{rel}` — {n} block(s)")
    if F.missing_lang_class:
        out.append("\n**Examples (first 30):**")
        for rel, ln, snip in F.missing_lang_class[:30]:
            out.append(f"- `{rel}:{ln}` — `{snip}`")
    out.append("")

    # -----------------------------------------------------------------
    # Top patterns
    # -----------------------------------------------------------------
    out.append("## Top patterns to fix book-wide")
    if F.pattern_counts:
        for label, n in sorted(F.pattern_counts.items(), key=lambda kv: -kv[1])[:20]:
            out.append(f"- **{n}×** {label}")
    out.append("")
    if F.py_indent_loss:
        out.append(f"- **{len(F.py_indent_loss)}×** Python indent loss in pygments-highlighted output "
                   "(see dedicated section; fix at the pipeline level, not file-by-file)")
    if F.mislabeled_shell:
        out.append(f"- **{len(F.mislabeled_shell)}×** shell/bash blocks tagged `lang-python` "
                   "(retag to `lang-bash`)")
    if F.mislabeled_yaml:
        out.append(f"- **{len(F.mislabeled_yaml)}×** YAML blocks tagged `lang-python` "
                   "(retag to `lang-yaml`)")

    out.append("")
    out.append("---")
    out.append(f"_Script: `scripts/audit_code_blocks.py`._")

    report = "\n".join(out)
    # Cap
    lines = report.splitlines()
    if len(lines) > 500:
        lines = lines[:498]
        lines.append("")
        lines.append(f"_…report truncated at 500 lines (was {len(report.splitlines())})._")
    final = "\n".join(lines) + "\n"
    out_path = ROOT / "code-correctness-audit.md"
    out_path.write_text(final, encoding="utf-8")
    print(f"Wrote {out_path} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
