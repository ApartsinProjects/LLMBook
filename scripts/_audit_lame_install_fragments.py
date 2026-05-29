"""
Audit lame install/setup Code Fragments across the LLMBook.

A "lame install fragment" is a numbered Code Fragment whose ENTIRE body is a
trivial one-line shell command such as `pip install X`, `npm install X`,
`apt install X`, `conda install X`, `brew install X`, `curl ...`, `wget ...`,
`export ...`, `cd ...`, or `git ...`. These are pedagogically useless: they
take up a Code Fragment number without teaching anything, and are nearly always
followed by a callout/practical-example with the real worked code that
already includes the install line as a comment.

Pattern (from known offenders):

    <div class="code-block-wrapper">
    <pre><code class="lang-bash pygments-highlighted">pip install X</code></pre>
    </div>
    <div class="code-caption"><strong>Code Fragment N.N.N:</strong> Install X</div>

Followed immediately by:

    <div class="callout practical-example">
        <pre><code class="pygments-highlighted lang-python"># pip install X
        ...real code...

This script is READ-ONLY. It produces a report. Run with Python 3.14.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

# Resolve project root relative to this script (scripts/_audit_lame_install_fragments.py).
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

EXCLUDE_DIRS = {
    "KDP",
    ".claude",
    "scripts",
    "node_modules",
    "pagefind",
    "templates",
    ".git",
    ".html2epub_cache",
    ".github",
    "build",
    "vendor",
}
EXCLUDE_PREFIXES = ("temp_",)


def is_excluded(path: Path) -> bool:
    """Skip files under excluded directories or whose ancestors match prefixes."""
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return True
        if any(part.startswith(p) for p in EXCLUDE_PREFIXES):
            return True
    return False


# Regex for the one-line shell command pattern.
# Matches: pip install X, npm install X, apt install X, conda install X,
# brew install X, curl <url>, wget <url>, export VAR=..., cd path,
# git clone ..., pip3 install X, python -m pip install X, sudo apt ...
LAME_INSTALL_RE = re.compile(
    r"^\s*"
    r"(?:sudo\s+)?"
    r"(?:python\s+-m\s+)?"
    r"(?:pip|pip3|npm|yarn|pnpm|apt|apt-get|conda|mamba|brew|curl|wget|"
    r"export|cd|git|uv|poetry|docker|gh|aws|gcloud|az|kubectl)"
    r"\b.*$",
    re.MULTILINE,
)


@dataclass
class LameFragment:
    file: Path
    line: int
    fragment_id: Optional[str]
    caption: str
    body: str
    lang_class: str


def _line_of(tag, text: str) -> int:
    """Approximate 1-based line number where `tag` appears in `text`."""
    s = str(tag)[:120]
    idx = text.find(s)
    if idx < 0:
        s = str(tag)[:60]
        idx = text.find(s)
    if idx < 0:
        return 0
    return text.count("\n", 0, idx) + 1


def find_fragment_id_from_caption(caption_text: str) -> Optional[str]:
    m = re.search(r"Code Fragment\s*([\d.]+)", caption_text)
    return m.group(1).rstrip(".") if m else None


def normalise_caption(text: str) -> str:
    """Strip the 'Code Fragment N.N.N:' prefix."""
    return re.sub(r"^\s*Code Fragment\s*[\d.]+\s*:\s*", "", text).strip()


def _find_preceding_pre(caption_div):
    """Find the <pre> directly preceding this caption (layout A: code then caption)."""
    # Walk backward through siblings, skipping whitespace text nodes.
    for sib in caption_div.previous_siblings:
        if not hasattr(sib, "name") or sib.name is None:
            # NavigableString: skip if whitespace
            if str(sib).strip() == "":
                continue
            return None
        # Direct <pre>
        if sib.name == "pre":
            return sib
        # Wrapped: <div class="code-block-wrapper"><pre>...</pre></div>
        if sib.name == "div":
            cls = sib.get("class") or []
            if "code-block-wrapper" in cls or "code-output" in cls:
                pre = sib.find("pre")
                if pre is not None:
                    return pre
                return None
            # Hit another caption: stop
            if "code-caption" in cls:
                return None
            # Hit a callout: this caption probably belongs to a following structure (layout B)
            return None
        # Headings or hr: stop
        if sib.name in {"h1", "h2", "h3", "h4", "hr"}:
            return None
    return None


def _get_lang_class(pre_tag) -> str:
    """Get the language class from a <pre><code class=...> element."""
    code = pre_tag.find("code")
    classes = []
    if code is not None:
        cls = code.get("class") or []
        classes = cls if isinstance(cls, list) else [cls]
    else:
        cls = pre_tag.get("class") or []
        classes = cls if isinstance(cls, list) else [cls]
    return " ".join(classes)


def _is_one_line_install(body: str) -> bool:
    """True if the body is a single non-empty line matching the install/setup pattern."""
    stripped = body.strip()
    if not stripped:
        return False
    # Single line only (no newlines in the non-empty content).
    lines = [ln for ln in stripped.splitlines() if ln.strip()]
    if len(lines) != 1:
        return False
    line = lines[0].strip()
    return bool(LAME_INSTALL_RE.match(line))


def audit_file(html_path: Path) -> list[LameFragment]:
    """Return all lame install/setup Code Fragments in one HTML file."""
    findings: list[LameFragment] = []
    try:
        text = html_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return findings
    soup = BeautifulSoup(text, "html.parser")

    captions = soup.find_all("div", class_="code-caption")
    for cap in captions:
        cap_text = cap.get_text(" ", strip=True)
        fragment_id = find_fragment_id_from_caption(cap_text)
        if fragment_id is None:
            # Not a numbered Code Fragment; skip
            continue
        pre = _find_preceding_pre(cap)
        if pre is None:
            continue
        # Get the raw text (without highlight spans).
        body = pre.get_text("", strip=False)
        if not _is_one_line_install(body):
            continue
        lang_class = _get_lang_class(pre)
        line = _line_of(cap, text)
        findings.append(
            LameFragment(
                file=html_path.relative_to(PROJECT_ROOT),
                line=line,
                fragment_id=fragment_id,
                caption=normalise_caption(cap_text),
                body=body.strip(),
                lang_class=lang_class,
            )
        )
    return findings


def main() -> int:
    html_files: list[Path] = []
    for path in PROJECT_ROOT.rglob("*.html"):
        rel = path.relative_to(PROJECT_ROOT)
        if is_excluded(rel):
            continue
        html_files.append(path)
    print(f"Scanning {len(html_files)} HTML files...", file=sys.stderr)

    all_findings: list[LameFragment] = []
    for html_path in html_files:
        all_findings.extend(audit_file(html_path))

    # Sort by file, then by line.
    all_findings.sort(key=lambda f: (f.file.as_posix(), f.line))

    print_report(all_findings)
    return 0


def _section_key(path: Path) -> str:
    """Group findings by top-level part directory."""
    parts = path.parts
    if not parts:
        return "(root)"
    return parts[0]


def print_report(findings: list[LameFragment]) -> None:
    """Print the report to stdout."""
    print()
    print("=" * 78)
    print("LAME INSTALL/SETUP CODE FRAGMENT AUDIT")
    print("=" * 78)
    print()
    print(f"Total lame install/setup Code Fragments found: {len(findings)}")
    print()

    if not findings:
        print("(none)")
        return

    # Breakdown by section (top-level part directory).
    by_section: dict[str, list[LameFragment]] = defaultdict(list)
    for f in findings:
        by_section[_section_key(f.file)].append(f)

    print("Breakdown by section (top-level part):")
    print("-" * 78)
    for section in sorted(by_section.keys()):
        print(f"  {section}: {len(by_section[section])}")
    print()

    # Breakdown by command verb.
    verb_counts: Counter = Counter()
    for f in findings:
        first_token = f.body.strip().split()[0] if f.body.strip() else "?"
        # Strip sudo / python -m prefixes.
        if first_token in ("sudo",):
            tokens = f.body.strip().split()
            first_token = tokens[1] if len(tokens) > 1 else first_token
        verb_counts[first_token] += 1
    print("Breakdown by command verb:")
    print("-" * 78)
    for verb, count in verb_counts.most_common():
        print(f"  {verb:<12} {count}")
    print()

    # Full per-finding listing.
    print("All findings (sorted by file, line):")
    print("-" * 78)
    for f in findings:
        print(f"  File:     {f.file.as_posix()}:{f.line}")
        print(f"  Fragment: Code Fragment {f.fragment_id}")
        print(f"  Caption:  {f.caption}")
        print(f"  Lang:     {f.lang_class}")
        print(f"  Body:     {f.body}")
        print()


if __name__ == "__main__":
    sys.exit(main())
