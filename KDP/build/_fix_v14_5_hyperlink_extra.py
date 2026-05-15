"""Hyperlink top-tier concepts to their canonical DEFINING SECTION (non-glossary).

This is a companion to _fix_v14_5_hyperlink_concepts.py. The earlier script
mapped ~140 aliases to ~100 glossary gl-ids. Many high-value concepts have NO
glossary entry but do have an authoritative defining section elsewhere in the
book (e.g., GPTQ -> appendix-s/section-s.4, ReAct -> module-21/section-21.1).

For every chapter HTML page, scan prose text and convert mentions of these
concepts into <a class="concept-link"> links pointing to the defining section.

Strict rules:
- Only modify EXISTING text (never insert text).
- Never modify code/pre, math, navigation, or already-hyperlinked spans.
- Never link a concept on its own definition page (the target section/file).
- One link per concept per page (first uncovered mention).
- Skip files that would receive >20 new links (avoid over-linking).
- Skip files with link-density below 0.5 per 1000 chars of prose.
- Do NOT re-link if the page already has a glossary-link for the same concept.

Usage:
    python _fix_v14_5_hyperlink_extra.py            # dry run, prints report
    python _fix_v14_5_hyperlink_extra.py --apply    # actually rewrite files
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    sys.exit("Requires beautifulsoup4. Install: pip install beautifulsoup4")

REPO = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {
    "node_modules", ".git", "KDP", "pagefind", "temp_epub", "backup",
    "source_fix_backups", "_exercise_payloads", "agents", "templates",
    "vendor", "scripts", "styles", ".html2pub_cache", "downloads",
}

# Concept aliases mapped to (target_id, target_path, title).
# target_path is REPO-relative.
# target_id is a logical id used for deduplication (per-page) and report grouping.
CONCEPT_TARGETS: dict[str, tuple[str, str, str]] = {
    # ---- Quantization formats (appendix-s/section-s.4) ----
    "gptq": (
        "cx-gptq",
        "appendices/appendix-s-inference-serving/section-s.4.html",
        "Section S.4: Quantization for Serving (GPTQ, AWQ, GGUF)",
    ),
    "awq": (
        "cx-awq",
        "appendices/appendix-s-inference-serving/section-s.4.html",
        "Section S.4: Quantization for Serving (GPTQ, AWQ, GGUF)",
    ),
    "gguf": (
        "cx-gguf",
        "appendices/appendix-s-inference-serving/section-s.4.html",
        "Section S.4: Quantization for Serving (GPTQ, AWQ, GGUF)",
    ),
    # ---- Serving stacks ----
    "tgi": (
        "cx-tgi",
        "appendices/appendix-s-inference-serving/section-s.2.html",
        "Section S.2: Text Generation Inference (TGI)",
    ),
    "text generation inference": (
        "cx-tgi",
        "appendices/appendix-s-inference-serving/section-s.2.html",
        "Section S.2: Text Generation Inference (TGI)",
    ),
    "sglang": (
        "cx-sglang",
        "appendices/appendix-s-inference-serving/section-s.3.html",
        "Section S.3: SGLang: Structured Generation and RadixAttention",
    ),
    "huggingface": (
        "cx-huggingface",
        "appendices/appendix-k-huggingface-ecosystem/index.html",
        "Appendix K: HuggingFace: Transformers, Datasets, and Hub",
    ),
    "hugging face": (
        "cx-huggingface",
        "appendices/appendix-k-huggingface-ecosystem/index.html",
        "Appendix K: HuggingFace: Transformers, Datasets, and Hub",
    ),
    # ---- Tokenization ----
    "byte-pair encoding": (
        "cx-bpe",
        "part-1-foundations/module-02-tokenization-subword-models/section-2.2.html",
        "Section 2.2: Subword Tokenization Algorithms",
    ),
    "byte pair encoding": (
        "cx-bpe",
        "part-1-foundations/module-02-tokenization-subword-models/section-2.2.html",
        "Section 2.2: Subword Tokenization Algorithms",
    ),
    "bpe": (
        "cx-bpe",
        "part-1-foundations/module-02-tokenization-subword-models/section-2.2.html",
        "Section 2.2: Subword Tokenization Algorithms",
    ),
    # ---- Inference batching/serving optimizations ----
    "continuous batching": (
        "cx-continuous-batching",
        "part-2-understanding-llms/module-09-inference-optimization/section-9.4.html",
        "Section 9.4: Serving Infrastructure",
    ),
    "paged attention": (
        "cx-paged-attention",
        "part-2-understanding-llms/module-09-inference-optimization/section-9.4.html",
        "Section 9.4: Serving Infrastructure",
    ),
    "pagedattention": (
        "cx-paged-attention",
        "part-2-understanding-llms/module-09-inference-optimization/section-9.4.html",
        "Section 9.4: Serving Infrastructure",
    ),
    # ---- Pruning ----
    "pruning": (
        "cx-pruning",
        "part-2-understanding-llms/module-09-inference-optimization/section-9.5.html",
        "Section 9.5: Model Pruning & Sparsity",
    ),
    # ---- Retrieval (BM25, hybrid, dense, sparse, rerank) ----
    "bm25": (
        "cx-bm25",
        "part-5-retrieval-conversation/module-19-rag/section-19.2.html",
        "Section 19.2: Advanced RAG Techniques",
    ),
    "hybrid search": (
        "cx-hybrid-search",
        "part-5-retrieval-conversation/module-19-rag/section-19.2.html",
        "Section 19.2: Advanced RAG Techniques",
    ),
    "hybrid retrieval": (
        "cx-hybrid-search",
        "part-5-retrieval-conversation/module-19-rag/section-19.2.html",
        "Section 19.2: Advanced RAG Techniques",
    ),
    "dense retrieval": (
        "cx-dense-retrieval",
        "part-5-retrieval-conversation/module-19-rag/section-19.2.html",
        "Section 19.2: Advanced RAG Techniques",
    ),
    "sparse retrieval": (
        "cx-sparse-retrieval",
        "part-5-retrieval-conversation/module-19-rag/section-19.2.html",
        "Section 19.2: Advanced RAG Techniques",
    ),
    "reranking": (
        "cx-rerank",
        "part-5-retrieval-conversation/module-19-rag/section-19.2.html",
        "Section 19.2: Advanced RAG Techniques",
    ),
    "reranker": (
        "cx-rerank",
        "part-5-retrieval-conversation/module-19-rag/section-19.2.html",
        "Section 19.2: Advanced RAG Techniques",
    ),
    # ---- Agents ----
    "react framework": (
        "cx-react",
        "part-6-agentic-ai/module-21-ai-agents/section-21.1.html",
        "Section 21.1: What Makes an LLM an Agent (and What Doesn't)",
    ),
    "react agent": (
        "cx-react",
        "part-6-agentic-ai/module-21-ai-agents/section-21.1.html",
        "Section 21.1: What Makes an LLM an Agent (and What Doesn't)",
    ),
    "react loop": (
        "cx-react",
        "part-6-agentic-ai/module-21-ai-agents/section-21.1.html",
        "Section 21.1: What Makes an LLM an Agent (and What Doesn't)",
    ),
    "multi-agent": (
        "cx-multi-agent",
        "part-6-agentic-ai/module-23-multi-agent-systems/index.html",
        "Chapter 23: Multi-Agent Systems",
    ),
    "multi-agent system": (
        "cx-multi-agent",
        "part-6-agentic-ai/module-23-multi-agent-systems/index.html",
        "Chapter 23: Multi-Agent Systems",
    ),
    "multi-agent systems": (
        "cx-multi-agent",
        "part-6-agentic-ai/module-23-multi-agent-systems/index.html",
        "Chapter 23: Multi-Agent Systems",
    ),
    "agentic": (
        "cx-agentic",
        "part-6-agentic-ai/module-21-ai-agents/index.html",
        "Chapter 21: AI Agent Foundations",
    ),
    "ai agent": (
        "cx-agent",
        "part-6-agentic-ai/module-21-ai-agents/index.html",
        "Chapter 21: AI Agent Foundations",
    ),
    "ai agents": (
        "cx-agent",
        "part-6-agentic-ai/module-21-ai-agents/index.html",
        "Chapter 21: AI Agent Foundations",
    ),
    # ---- Evaluation ----
    "mt-bench": (
        "cx-mt-bench",
        "part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html",
        "Section 28.8: LLM-as-Judge",
    ),
    "llm-as-judge": (
        "cx-llm-judge",
        "part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html",
        "Section 28.8: LLM-as-Judge",
    ),
    "llm-as-a-judge": (
        "cx-llm-judge",
        "part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html",
        "Section 28.8: LLM-as-Judge",
    ),
    "llm as judge": (
        "cx-llm-judge",
        "part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html",
        "Section 28.8: LLM-as-Judge",
    ),
    # ---- Safety ----
    "jailbreak": (
        "cx-jailbreak",
        "part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html",
        "Section 30.1: LLM Security Threats",
    ),
    "jailbreaking": (
        "cx-jailbreak",
        "part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.1.html",
        "Section 30.1: LLM Security Threats",
    ),
    "red teaming": (
        "cx-red-teaming",
        "part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.8.html",
        "Section 30.8: Red Teaming Frameworks & LLM Security Testing",
    ),
    "red-teaming": (
        "cx-red-teaming",
        "part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.8.html",
        "Section 30.8: Red Teaming Frameworks & LLM Security Testing",
    ),
    "alignment tax": (
        "cx-alignment-tax",
        "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html",
        "Section 17.5: Alignment Research Frontiers",
    ),
}

# Block tags / classes inside which we must NOT recurse.
SKIP_TAG_NAMES = {
    "pre", "code", "script", "style", "math", "svg", "head", "header",
    "nav", "noscript",
}
SKIP_CLASS_TOKENS = {
    "math-block", "math", "katex", "katex-display", "header-nav",
    "part-label", "chapter-label", "page-nav", "footer-nav",
}

# Allowed parent tag names for prose linking.
PROSE_PARENT_TAGS = {"p", "li", "td", "th", "dd", "blockquote", "figcaption", "em", "strong", "span", "i", "b"}

# Sort aliases longest-first so "byte-pair encoding" beats "bpe".
SORTED_ALIASES = sorted(CONCEPT_TARGETS.keys(), key=len, reverse=True)


def compute_href(target_path: str, source_file: Path) -> str:
    """Compute relative href from source_file to target_path (REPO-relative)."""
    target_file = REPO / target_path
    rel = os.path.relpath(target_file, source_file.parent)
    rel = rel.replace("\\", "/")
    return rel


def is_skipped_element(el: Tag) -> bool:
    if el.name in SKIP_TAG_NAMES:
        return True
    cls = el.get("class") or []
    if isinstance(cls, str):
        cls = [cls]
    for c in cls:
        if c in SKIP_CLASS_TOKENS:
            return True
    return False


def ancestor_is_link(node) -> bool:
    cur = node.parent
    while cur is not None and isinstance(cur, Tag):
        if cur.name == "a":
            return True
        cur = cur.parent
    return False


def ancestor_is_skipped(node) -> bool:
    cur = node.parent
    while cur is not None and isinstance(cur, Tag):
        if is_skipped_element(cur):
            return True
        cur = cur.parent
    return False


def is_prose_text_node(node: NavigableString) -> bool:
    if ancestor_is_link(node):
        return False
    if ancestor_is_skipped(node):
        return False
    parent = node.parent
    if parent is None or not isinstance(parent, Tag):
        return False
    if parent.name not in PROSE_PARENT_TAGS:
        return False
    text = str(node)
    if not text.strip():
        return False
    return True


def build_alias_pattern() -> re.Pattern:
    parts = [re.escape(a) for a in SORTED_ALIASES]
    pattern = r"(?<![A-Za-z])(" + "|".join(parts) + r")(?![A-Za-z])"
    return re.compile(pattern, re.IGNORECASE)


ALIAS_RE = build_alias_pattern()


def link_html_for(matched_text: str, target_href: str, title: str) -> str:
    return (
        f'<a class="concept-link" href="{target_href}" title="{title}">'
        f'{matched_text}</a>'
    )


def collect_text_nodes(soup: BeautifulSoup) -> list:
    out = []
    for ns in soup.find_all(string=True):
        if isinstance(ns, NavigableString) and is_prose_text_node(ns):
            out.append(ns)
    return out


def get_already_used_concept_ids(soup: BeautifulSoup) -> set[str]:
    """Find concept-link target_ids already on the page (re-runs should skip)."""
    used = set()
    for a in soup.find_all("a"):
        cls = a.get("class") or []
        if "concept-link" not in cls:
            continue
        href = a.get("href", "")
        # Match a target_path; we can't recover target_id from href alone, so
        # we just collect the href tail (filename) as a soft proxy.
        tail = href.split("/")[-1].split("#")[0]
        used.add(tail)
    return used


def is_self_target(file_path: Path, target_path: str) -> bool:
    """True if this file IS the target (don't link to self)."""
    target_file = REPO / target_path
    try:
        return file_path.resolve() == target_file.resolve()
    except Exception:
        return False


def process_file(
    file_path: Path,
    samples: list,
    max_links_per_file: int = 20,
    min_density_per_1k: float = 0.5,
) -> tuple[int, dict, list]:
    try:
        raw = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return 0, {}, [f"read-error:{e}"]

    soup = BeautifulSoup(raw, "html.parser")
    used_target_tails = get_already_used_concept_ids(soup)
    used_concept_ids: set[str] = set()

    # Pre-compute prose chars for density.
    prose_chars = 0
    for ns in collect_text_nodes(soup):
        prose_chars += len(str(ns))

    text_nodes = collect_text_nodes(soup)

    new_links = 0
    by_cx: Counter = Counter()
    pending_replacements = []

    for ns in text_nodes:
        text = str(ns)
        if not text.strip():
            continue
        replacements = []
        last_end = 0
        modified = False

        for m in ALIAS_RE.finditer(text):
            alias = m.group(0).lower()
            target = CONCEPT_TARGETS.get(alias)
            if not target:
                continue
            target_id, target_path, target_title = target

            # Skip self-link.
            if is_self_target(file_path, target_path):
                continue
            # Skip if we already used this concept on this page.
            if target_id in used_concept_ids:
                continue
            # Skip if a concept-link to that file already exists.
            target_tail = target_path.split("/")[-1]
            if target_tail in used_target_tails:
                # We allow one concept_link per concept (target_id), but if
                # there's already a concept-link to the same target file, the
                # page is already cross-referenced; skip a duplicate.
                continue
            if new_links >= max_links_per_file:
                break

            used_concept_ids.add(target_id)
            used_target_tails.add(target_tail)
            by_cx[target_id] += 1
            new_links += 1

            pre = text[last_end : m.start()]
            if pre:
                replacements.append(NavigableString(pre))
            href = compute_href(target_path, file_path)
            link_soup = BeautifulSoup(
                link_html_for(m.group(0), href, target_title), "html.parser"
            )
            link_tag = link_soup.a
            replacements.append(link_tag)
            last_end = m.end()
            modified = True

            samples.append({
                "file": str(file_path.relative_to(REPO)).replace("\\", "/"),
                "target_id": target_id,
                "matched": m.group(0),
                "href": href,
                "context_before": pre[-40:] if pre else "",
                "context_after": text[m.end():m.end() + 40],
            })

        if modified:
            tail = text[last_end:]
            if tail:
                replacements.append(NavigableString(tail))
            pending_replacements.append((ns, replacements))

    if not pending_replacements:
        return 0, {}, []

    density = (new_links / prose_chars) * 1000 if prose_chars else 0
    if density < min_density_per_1k and new_links > 0:
        return 0, {}, [f"low-density:{density:.2f}"]

    if new_links > max_links_per_file:
        return 0, {}, [f"over-cap:{new_links}"]

    for ns, repl in pending_replacements:
        for piece in repl:
            ns.insert_before(piece)
        ns.extract()

    process_file._last_html = str(soup)
    return new_links, dict(by_cx), []


process_file._last_html = ""


def iter_target_files() -> Iterable[Path]:
    glossary_dir = REPO / "appendices" / "appendix-f-glossary"
    for p in REPO.rglob("*.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        # Skip glossary pages (they have a separate purpose).
        try:
            p.relative_to(glossary_dir)
            continue
        except ValueError:
            pass
        yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Actually rewrite files")
    ap.add_argument("--report", default=str(REPO / "KDP" / "build" / "AUDIT_hyperlinks_extra.md"))
    ap.add_argument("--max-links", type=int, default=20)
    ap.add_argument("--min-density", type=float, default=0.5)
    args = ap.parse_args()

    samples: list = []
    file_results: dict = {}
    skipped: list = []

    total_files = 0
    for path in iter_target_files():
        total_files += 1
        new_links, by_cx, skip_reasons = process_file(
            path, samples,
            max_links_per_file=args.max_links,
            min_density_per_1k=args.min_density,
        )
        if skip_reasons:
            skipped.append((path, skip_reasons))
            continue
        if new_links == 0:
            continue
        if args.apply:
            path.write_text(process_file._last_html, encoding="utf-8")
        file_results[path] = (new_links, by_cx)

    total_new = sum(n for n, _ in file_results.values())
    files_touched = len(file_results)

    per_cx_total: Counter = Counter()
    for _, by_cx in file_results.values():
        for g, c in by_cx.items():
            per_cx_total[g] += c

    report_lines = []
    mode = "APPLIED" if args.apply else "DRY RUN"
    report_lines.append(f"# Extra-Concept Hyperlinking Audit ({mode})\n")
    report_lines.append(f"- Files scanned: {total_files}")
    report_lines.append(f"- Aliases: {len(CONCEPT_TARGETS)}")
    report_lines.append(f"- Distinct concept-ids: {len(set(t[0] for t in CONCEPT_TARGETS.values()))}")
    report_lines.append(f"- Files modified: {files_touched}")
    report_lines.append(f"- Total new links: {total_new}")
    report_lines.append(f"- Files skipped (cap/density): {len(skipped)}\n")

    report_lines.append("## Top 25 files by new-link count\n")
    sorted_files = sorted(file_results.items(), key=lambda kv: -kv[1][0])
    for path, (n, _) in sorted_files[:25]:
        rel = str(path.relative_to(REPO)).replace("\\", "/")
        report_lines.append(f"- {n:3d}  {rel}")
    report_lines.append("")

    report_lines.append("## Most-linked extra concepts\n")
    for cx, c in per_cx_total.most_common(30):
        # Find a title to display.
        title = ""
        for alias, (cid, _, t) in CONCEPT_TARGETS.items():
            if cid == cx:
                title = t
                break
        report_lines.append(f"- {c:4d}  {cx}  ({title})")
    report_lines.append("")

    report_lines.append("## 10 sample link additions\n")
    for s in samples[:10]:
        snippet = f"...{s['context_before']}<a>{s['matched']}</a>{s['context_after']}..."
        report_lines.append(f"- `{s['file']}` -> `{s['target_id']}`")
        report_lines.append(f"  - {snippet}")
        report_lines.append(f"  - href: `{s['href']}`")
    report_lines.append("")

    # Aliases that produced zero links.
    matched_aliases = set(s["matched"].lower() for s in samples)
    unmatched = sorted(a for a in CONCEPT_TARGETS if a not in matched_aliases)
    report_lines.append("## Aliases that produced ZERO new links\n")
    report_lines.append("(could mean term is rare in prose, already linked elsewhere, or used only in code/headings)\n")
    for a in unmatched:
        cid = CONCEPT_TARGETS[a][0]
        report_lines.append(f"- `{a}` -> {cid}")
    report_lines.append("")

    if skipped:
        report_lines.append("## Files skipped (with reasons, first 30)\n")
        for path, reasons in skipped[:30]:
            rel = str(path.relative_to(REPO)).replace("\\", "/")
            report_lines.append(f"- {rel} : {','.join(reasons)}")

    report_text = "\n".join(report_lines)
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(report_text, encoding="utf-8")

    print(f"[{mode}] files_modified={files_touched} total_new_links={total_new}")
    print(f"report: {args.report}")
    if not args.apply:
        print("(dry run; pass --apply to commit changes)")


if __name__ == "__main__":
    main()
