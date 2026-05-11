"""v3.5 R4#3: Re-tag <code class="lang-text"> blocks as lang-python when
they're clearly Python (more lenient heuristic than fix_mislabeled_code.py).

The original heuristic required np./torch./pandas/etc. library mentions.
This catches PEFT-config blocks, dataclass examples, and LoRA snippets that
use PEFT/peft/HF libraries which weren't in the original whitelist.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# Keywords/idioms that are strong Python signals
PY_KEYWORDS = re.compile(
    r"\b(import|from|def|class|return|lambda|with|for|while|if|elif|else|"
    r"try|except|yield|async|await|self|None|True|False)\b"
)
PY_LIBS_OR_TYPES = (
    "peft", "PEFT", "transformers", "huggingface", "from torch", "from peft",
    "LoraConfig", "PromptTuningConfig", "PrefixTuningConfig", "AdapterConfig",
    "Trainer", "TrainingArguments", "AutoModel", "AutoTokenizer",
    "DataLoader", "Dataset", "Tensor", "nn.Module", "@dataclass",
    "openai", "anthropic", "langchain", "llama_index", "chromadb",
    "pydantic", "BaseModel", "ConfigDict", "torch.nn",
    "Optional[", "List[", "Dict[", "Tuple[",
)


def looks_like_python(text: str) -> bool:
    if not PY_KEYWORDS.search(text):
        # Allow comment-only blocks if they have Python-style # comments AND PY libs
        if not text.strip().startswith("#"):
            return False
    return any(lib in text for lib in PY_LIBS_OR_TYPES)


def main() -> int:
    from bs4 import BeautifulSoup
    n_files = 0
    n_blocks = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "lang-text" not in text:
            continue
        soup = BeautifulSoup(text, "lxml")
        changed = 0
        for code in soup.find_all("code", class_=lambda c: c and "lang-text" in c):
            body = code.get_text()
            if looks_like_python(body):
                cls = [c for c in code.get("class") or [] if c != "lang-text"]
                cls.append("lang-python")
                code["class"] = cls
                changed += 1
        if changed:
            # Re-serialize body inner HTML and patch
            body_tag = soup.find("body")
            if body_tag is None:
                continue
            body_inner = "".join(str(c) for c in body_tag.children)
            head_close = text.find(">", text.find("<body")) + 1
            body_close = text.rfind("</body>")
            new_text = text[:head_close] + "\n" + body_inner + "\n" + text[body_close:]
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_blocks += changed
            print(f"  {changed:>2}x  {p.relative_to(ROOT).as_posix()}")
    print(f"\nRe-tagged {n_blocks} lang-text -> lang-python across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
