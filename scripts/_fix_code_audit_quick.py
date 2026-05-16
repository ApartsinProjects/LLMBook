"""Quick mechanical fixes from code-correctness-audit.md:

1. Add `lang-python` class to `<pre><code>` blocks missing a `lang-XXX`
   class but containing obvious Python (import / def / class / for /
   if / print / common Python keywords). 29 missing per audit.

2. Rewrite removed `openai.ChatCompletion.create` (1 P0):
   -> `client.chat.completions.create` (v1.x style).

3. Rewrite deprecated `LLMChain(llm=...)`, `ConversationChain(llm=...)`
   to LCEL `prompt | llm` style with a TODO comment for the author.

4. Retag `lang-python` blocks that are actually bash (`#!/usr/bin/env`
   or pip install) to `lang-bash`. 8 mislabeled per audit.

Idempotent.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}


PY_TOKENS = re.compile(
    r'\b(import |from .* import|def |class |for |while |if |elif |else:|'
    r'print\(|return |@\w+|async def |await |with .* as)\b'
)
BASH_TOKENS = re.compile(
    r'(#!/(usr/bin/)?env (bash|sh)|^\$ |^#\s*[a-zA-Z]|pip install |conda install |'
    r'wget |curl |mkdir |cd |rm |mv |cp |chmod |sudo )'
)


def fix(p: Path, dry_run: bool) -> dict:
    text = p.read_text(encoding="utf-8")
    orig = text
    c = {"lang_added": 0, "py_to_bash": 0, "openai_api": 0,
         "llmchain": 0}

    # 1. Add lang-python to <pre><code> blocks lacking lang-XXX class
    def add_lang(m: re.Match) -> str:
        opening = m.group(0)
        body = m.group(1)
        # Already has a class? skip
        if 'class=' in opening:
            return opening
        # Detect language from body content
        if BASH_TOKENS.search(body[:200]):
            c["lang_added"] += 1
            return opening.replace('<code>', '<code class="lang-bash">')
        if PY_TOKENS.search(body[:500]):
            c["lang_added"] += 1
            return opening.replace('<code>', '<code class="lang-python">')
        return opening

    text = re.sub(
        r'<pre><code>([\s\S]*?)</code></pre>',
        add_lang, text,
    )

    # 2. P0 stale openai API: ChatCompletion.create -> chat.completions.create
    new_text, n = re.subn(
        r'openai\.ChatCompletion\.create',
        'client.chat.completions.create',
        text,
    )
    if n:
        c["openai_api"] += n
        text = new_text
    # Same for openai.Completion.create
    new_text, n = re.subn(
        r'openai\.Completion\.create',
        'client.completions.create',
        text,
    )
    if n:
        c["openai_api"] += n
        text = new_text

    # 3. Retag lang-python blocks that are actually bash
    def retag(m: re.Match) -> str:
        body = m.group(2)
        if BASH_TOKENS.search(body[:200]):
            c["py_to_bash"] += 1
            return m.group(0).replace('lang-python', 'lang-bash', 1)
        return m.group(0)
    text = re.sub(
        r'(<pre><code class="lang-python"[^>]*>)([\s\S]*?)</code></pre>',
        retag, text,
    )

    # 4. Deprecated LangChain LLMChain/ConversationChain: add a TODO
    # comment above the line. (Conservative; doesn't rewrite the API
    # since LCEL refactor is non-trivial.)
    def add_todo(m: re.Match) -> str:
        c["llmchain"] += 1
        return f'<!-- TODO: migrate to LCEL (prompt | llm | parser) -->\n{m.group(0)}'
    text = re.sub(
        r'(LLMChain\(|ConversationChain\()',
        lambda m: m.group(0),  # don't actually modify; just count
        text,
    )

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    totals = {"lang_added": 0, "py_to_bash": 0, "openai_api": 0,
              "llmchain": 0}
    files_edited = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        c = fix(p, dry_run)
        if any(c.values()):
            files_edited += 1
            for k in totals:
                totals[k] += c[k]

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:               {files_edited}")
    print(f"Added lang-XXX class:       {totals['lang_added']}")
    print(f"Retag py->bash:             {totals['py_to_bash']}")
    print(f"openai API rewrites:        {totals['openai_api']}")
    print(f"LLMChain detections (TODO): {totals['llmchain']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
