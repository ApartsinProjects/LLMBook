"""v3.5 R4#2: Add code-captions to lab-appendix code blocks.

Strategy per uncaptioned <pre><code> block:
  1. Extract the FIRST comment line (Python: starting with '# ', JS/JSON/Bash:
     '# ' or '// ' or '<!-- '). That's the author's intent in their own words.
  2. If no comment, derive a caption from the FIRST executable line
     (e.g., 'pip install langchain' -> 'Install LangChain').
  3. If still nothing useful, use 'Language: <lang>' as last resort.

Caption format: '<div class="code-caption"><strong>Code Fragment X.Y.Z:</strong> <text></div>'
where X.Y.Z is the appendix-letter and a sequential index per file.

Affected appendices (from Round 4 audit):
  L LangChain, R Experiment Tracking, S Inference Serving,
  T Distributed ML, U Docker Containers
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parent.parent.parent

TARGET_APPENDICES = ["l-langchain", "r-experiment-tracking", "s-inference-serving",
                     "t-distributed-ml", "u-docker-containers"]


def extract_caption_text(code_text: str, lang: str) -> str:
    """Heuristic to derive a one-line caption."""
    lines = [ln.strip() for ln in code_text.split("\n") if ln.strip()]
    # 1. First comment line
    for ln in lines[:5]:
        if lang in ("python", "py"):
            if ln.startswith("# "):
                return ln[2:].rstrip(".").strip()
        elif lang in ("javascript", "js", "ts", "typescript"):
            if ln.startswith("// "):
                return ln[3:].rstrip(".").strip()
        elif lang in ("bash", "sh", "shell"):
            if ln.startswith("# "):
                return ln[2:].rstrip(".").strip()
        elif lang in ("yaml", "yml", "toml"):
            if ln.startswith("# "):
                return ln[2:].rstrip(".").strip()
    # 2. Recognized first-executable patterns
    if lines:
        first = lines[0]
        if first.startswith("pip install "):
            pkgs = first[12:].split()[:3]
            return f"Install {', '.join(pkgs)}"
        if first.startswith("docker "):
            return f"Docker command: {first[:60]}"
        if first.startswith("from "):
            mod = first.split()[1]
            return f"Import from {mod}"
        if first.startswith("import "):
            mod = first.split()[1].rstrip(",")
            return f"Import {mod}"
        if first.startswith(("FROM ", "WORKDIR ", "RUN ")):
            return f"Dockerfile: {first[:50]}..."
    # 3. Language fallback
    return f"{lang.capitalize()} example"


def lang_from_code_class(classes: list) -> str:
    for c in classes or []:
        if c.startswith("lang-"):
            return c[5:]
        if c.startswith("language-"):
            return c[9:]
    return "code"


def main() -> int:
    n_files = 0
    n_captions = 0
    for app in TARGET_APPENDICES:
        app_dir = ROOT / "appendices" / f"appendix-{app}"
        if not app_dir.exists():
            print(f"  [skip] {app} dir not found")
            continue
        # Get appendix letter (first char of name)
        letter = app[0]
        for p in sorted(app_dir.glob("*.html")):
            if p.name == "index.html":
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            if "<pre>" not in text and "<pre " not in text:
                continue
            soup = BeautifulSoup(text, "lxml")
            # Section number from filename: section-l.3 -> letter=l, index=3
            m = re.match(r"section-([a-z])\.(\d+)\.html", p.name)
            if not m:
                continue
            sec_letter, sec_idx = m.group(1), m.group(2)

            cap_idx = 1
            file_changes = 0
            for pre in soup.find_all("pre"):
                # Skip if a code-caption already exists immediately before or after
                prev = pre.find_previous_sibling()
                next_sib = pre.find_next_sibling()
                if (prev and "code-caption" in (prev.get("class") or [])) or \
                   (next_sib and "code-caption" in (next_sib.get("class") or [])):
                    continue
                # Skip pre that is wrapped in code-block-wrapper with sibling caption
                parent = pre.parent
                if parent and parent.name == "div" and "code-block-wrapper" in (parent.get("class") or []):
                    has_cap = any("code-caption" in (c.get("class") or [])
                                  for c in parent.find_all("div"))
                    if has_cap:
                        continue

                code = pre.find("code")
                if not code:
                    continue
                lang = lang_from_code_class(code.get("class") or [])
                caption_text = extract_caption_text(code.get_text(), lang)
                # Build caption tag
                cap = soup.new_tag("div", attrs={"class": "code-caption"})
                strong = soup.new_tag("strong")
                strong.string = f"Code Fragment {sec_letter.upper()}.{sec_idx}.{cap_idx}:"
                cap.append(strong)
                cap.append(NavigableString(f" {caption_text}"))
                pre.insert_after(cap)
                cap_idx += 1
                file_changes += 1

            if file_changes > 0:
                # Re-serialize body
                body = soup.find("body")
                if body is None:
                    continue
                body_inner = "".join(str(c) for c in body.children)
                head_close = text.find(">", text.find("<body")) + 1
                body_close = text.rfind("</body>")
                new_text = text[:head_close] + "\n" + body_inner + "\n" + text[body_close:]
                p.write_text(new_text, encoding="utf-8")
                n_files += 1
                n_captions += file_changes
                print(f"  {file_changes:>3}x  {p.relative_to(ROOT).as_posix()}")
    print(f"\nAdded {n_captions} code captions across {n_files} appendix files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
