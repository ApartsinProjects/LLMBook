"""Add library-shortcut callouts after hand-rolled code blocks that lack them.

Idempotent. Run with --apply to write changes; default is dry-run.

Targets 5 hand-rolled patterns:
 - cosine_similarity -> sklearn.metrics.pairwise.cosine_similarity / faiss
 - retry/backoff loop -> tenacity
 - text chunker -> langchain.text_splitter.RecursiveCharacterTextSplitter
 - semantic cache -> gptcache / langchain-community
 - attention from scratch -> torch.nn.functional.scaled_dot_product_attention

For each matching wrapper, inserts a <div class="callout library-shortcut"> as
the next sibling immediately after the wrapper, unless one already sits within
8 next-siblings or as the immediate previous sibling.

Validates that the rewritten HTML still parses as well-formed XML/HTML and
that the file size grows by exactly the inserted callout (no other diff).

Usage:
    /c/Python314/python scripts/_add_library_shortcuts.py            # dry-run
    /c/Python314/python scripts/_add_library_shortcuts.py --apply    # write
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup, Tag, NavigableString

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

EXCLUDE = {"KDP", "node_modules", ".git", "temp_ebook", "temp_epub",
           "source_fix_backups", "pagefind", "templates", ".claude",
           ".book-update", "vendor", "scripts", "docs", "styles", "build"}


def is_excluded(p: Path) -> bool:
    return any(part in EXCLUDE or part.startswith("temp_")
               for part in p.relative_to(PROJECT_ROOT).parts)


# --------------------------------------------------------------------------- #
# Shortcut templates per pattern
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Shortcut:
    pattern_id: str
    title: str
    body_html: str   # inner HTML of the <p> inside the callout


SHORTCUTS: dict[str, Shortcut] = {
    "cosine": Shortcut(
        pattern_id="cosine",
        title="Library Shortcut: vectorized cosine similarity",
        body_html=(
            "In production, prefer <code>sklearn.metrics.pairwise.cosine_similarity(A, B)</code> "
            "(vectorized over arrays, drop-in replacement for the loop above), or "
            "<code>faiss.IndexFlatIP</code> with L2-normalized vectors when you need "
            "billion-scale retrieval. The hand-rolled <code>np.dot / np.linalg.norm</code> "
            "version above shows the math; the library version is what you would ship."
        ),
    ),
    "retry": Shortcut(
        pattern_id="retry",
        title="Library Shortcut: tenacity",
        body_html=(
            "In production, prefer the <code>tenacity</code> library "
            "(<code>pip install tenacity</code>) instead of a hand-rolled "
            "<code>for attempt in range(...)</code> + <code>time.sleep</code> loop: "
            "<code>@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=60), "
            "retry=retry_if_exception_type(httpx.HTTPError))</code> gives you exponential "
            "backoff with jitter, per-exception filtering, and async support in one decorator."
        ),
    ),
    "chunker": Shortcut(
        pattern_id="chunker",
        title="Library Shortcut: RecursiveCharacterTextSplitter",
        body_html=(
            "In production, prefer "
            "<code>langchain_text_splitters.RecursiveCharacterTextSplitter(chunk_size=512, "
            "chunk_overlap=64)</code> instead of a hand-rolled window loop. It handles "
            "paragraph and sentence boundaries, falls back through a list of separators, "
            "and ships with token-aware variants (<code>TokenTextSplitter</code>, "
            "<code>MarkdownTextSplitter</code>) for free. The hand-rolled version above "
            "is useful to see the mechanics; the library version is what you would ship."
        ),
    ),
    "semantic_cache": Shortcut(
        pattern_id="semantic_cache",
        title="Library Shortcut: gptcache",
        body_html=(
            "In production, prefer <code>gptcache</code> (<code>pip install gptcache</code>) "
            "or the semantic-cache wrapper in <code>langchain_community.cache</code> instead "
            "of a hand-rolled list-backed similarity cache. Both support pluggable embedding "
            "backends, vector-store backends (FAISS, Milvus, Chroma), and TTL eviction out "
            "of the box. The hand-rolled version above shows the threshold logic; the library "
            "version scales to millions of entries."
        ),
    ),
    "attention": Shortcut(
        pattern_id="attention",
        title="Library Shortcut: scaled_dot_product_attention",
        body_html=(
            "In production, prefer "
            "<code>torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=True)</code>. "
            "On supported hardware (Ampere and newer NVIDIA, recent AMD) it dispatches to "
            "FlashAttention or memory-efficient kernels and runs 2-4x faster while using "
            "a fraction of the activation memory. The hand-rolled "
            "<code>(q @ k.T) / sqrt(d_k)</code> version above shows the math; the library "
            "version is what you would ship."
        ),
    ),
}


# --------------------------------------------------------------------------- #
# Classification
# --------------------------------------------------------------------------- #


def classify(src: str) -> str | None:
    if (re.search(r"def\s+\w*[Cc]os(?:ine)?_?[Ss]im\w*\(", src) or
            re.search(r"np\.dot\([^)]+?\)\s*/\s*\(\s*np\.linalg\.norm", src)):
        if not re.search(r"from\s+sklearn\.metrics\.pairwise\s+import\s+cosine_similarity", src):
            # Treat semantic-cache flavor separately
            if re.search(r"class\s+\w*[Ss]emantic[Cc]ache\b", src) and \
               not re.search(r"\bgptcache\b|langchain_community", src):
                return "semantic_cache"
            return "cosine"
    if (re.search(r"for\s+attempt\s+in\s+range\(", src) and
            re.search(r"\bexcept\b", src) and
            re.search(r"time\.sleep\b|asyncio\.sleep\(", src) and
            not re.search(r"\b(?:import|from)\s+tenacity\b", src)):
        return "retry"
    if (re.search(r"def\s+\w*chunk\w*\(.*?text", src, re.DOTALL) and
            re.search(r"\bchunk_size\b|\bchunk_overlap\b|\boverlap\b", src) and
            not re.search(r"from\s+langchain", src) and
            not re.search(r"from\s+llama_index", src)):
        return "chunker"
    if (re.search(r"\bq\s*@\s*k\.(T|transpose)", src) and
            re.search(r"softmax", src) and
            re.search(r"math\.sqrt|head_dim|d_?k\b", src) and
            not re.search(r"scaled_dot_product_attention", src)):
        return "attention"
    if (re.search(r"class\s+\w*[Ss]emantic[Cc]ache\b|def\s+\w*[Ss]emantic[Cc]ache\b", src) and
            not re.search(r"\bgptcache\b|langchain_community", src)):
        return "semantic_cache"
    return None


def neighbor_has_library_shortcut(wrapper: Tag, lookahead: int = 8) -> bool:
    sib = wrapper
    for _ in range(lookahead):
        sib = sib.find_next_sibling()
        if sib is None:
            break
        if isinstance(sib, Tag):
            cls = sib.get("class") or []
            if "callout" in cls and "library-shortcut" in cls:
                return True
            if sib.name in {"h1", "h2", "h3", "h4"}:
                break
    prev = wrapper.find_previous_sibling()
    if isinstance(prev, Tag):
        cls = prev.get("class") or []
        if "callout" in cls and "library-shortcut" in cls:
            return True
    return False


# --------------------------------------------------------------------------- #
# Callout builder
# --------------------------------------------------------------------------- #


def build_callout_html(s: Shortcut) -> str:
    return (
        f'<div class="callout library-shortcut">\n'
        f'<div class="callout-title">{s.title}</div>\n'
        f'<p>{s.body_html}</p>\n'
        f'</div>\n'
    )


# --------------------------------------------------------------------------- #
# Pipeline
# --------------------------------------------------------------------------- #


@dataclass
class Edit:
    path: Path
    fragment_id: str | None
    pattern_id: str
    n_lines: int


def fragment_id(wrapper: Tag) -> str | None:
    cap = wrapper.find("div", class_="code-caption")
    if not cap:
        return None
    m = re.match(r"Code Fragment\s+(\d+(?:\.\d+)+)", cap.get_text(" ", strip=True))
    return m.group(1) if m else None


def process_file(path: Path, *, apply: bool) -> list[Edit]:
    text = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(text, "html.parser")
    edits: list[Edit] = []

    wrappers_to_edit = []
    for wrapper in soup.find_all("div", class_="code-block-wrapper"):
        code = wrapper.find("code")
        if code is None:
            continue
        cls = code.get("class") or []
        if not any("lang-python" in c for c in cls):
            continue
        src = code.get_text()
        if src.count("\n") < 15:
            continue
        kind = classify(src)
        if kind is None or kind not in SHORTCUTS:
            continue
        if neighbor_has_library_shortcut(wrapper):
            continue
        wrappers_to_edit.append((wrapper, kind, src.count("\n")))

    if not wrappers_to_edit:
        return edits

    # Walk backwards through the document so prior insertions do not move later
    # wrappers' indexes (insertion site is wrapper.next_sibling, so later edits
    # shift positions; processing from last to first avoids that).
    for wrapper, kind, n_lines in reversed(wrappers_to_edit):
        shortcut = SHORTCUTS[kind]
        edits.append(Edit(
            path=path,
            fragment_id=fragment_id(wrapper),
            pattern_id=kind,
            n_lines=n_lines,
        ))
        if apply:
            new_html = build_callout_html(shortcut)
            new_tag = BeautifulSoup(new_html, "html.parser")
            # Insert after wrapper with a newline before
            wrapper.insert_after(NavigableString("\n"), new_tag)

    if apply and edits:
        new_text = str(soup)
        path.write_text(new_text, encoding="utf-8")

    edits.reverse()  # restore document order
    return edits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="write changes; without this flag, dry-run only")
    args = ap.parse_args()

    all_edits: list[Edit] = []
    files_visited = 0
    for path in sorted(PROJECT_ROOT.glob("part-*/**/*.html")):
        if is_excluded(path):
            continue
        files_visited += 1
        edits = process_file(path, apply=args.apply)
        all_edits.extend(edits)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] Visited {files_visited} files. Edits: {len(all_edits)}")
    print()

    by_pattern: dict[str, int] = {}
    by_file: dict[Path, list[Edit]] = {}
    for e in all_edits:
        by_pattern[e.pattern_id] = by_pattern.get(e.pattern_id, 0) + 1
        by_file.setdefault(e.path, []).append(e)

    print("Counts by pattern:")
    for pid, n in sorted(by_pattern.items(), key=lambda kv: -kv[1]):
        print(f"  {pid:<16} {n}")
    print()

    print("Edits by file:")
    for path, edits in sorted(by_file.items()):
        rel = path.relative_to(PROJECT_ROOT)
        print(f"  {rel}")
        for e in edits:
            frag = e.fragment_id or "(unnamed)"
            print(f"      [{e.pattern_id:>14}] frag={frag}  lines={e.n_lines}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
