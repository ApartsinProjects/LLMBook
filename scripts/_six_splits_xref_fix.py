"""
Update all cross-references (prev/next nav, prose links) to point to the right
half of the six newly-split sections.

For each old section-X.Y.html href, we need to decide between section-X.Ya.html
and section-X.Yb.html. The rule:
  - href with #anchor-id: look up where that id lives (a or b)
  - href without #anchor: default to a (the conceptual entry point)
  - prev/next nav links from neighbor sections:
      * the section BEFORE the original points to Xa (next-link)
      * the section AFTER the original points to Xb (prev-link)
      * everything else uses anchor lookup or defaults to a

Approach:
  1) Build a map: section_path_str -> dict(id -> file_a_or_b)
  2) For every HTML file in the book, rewrite href="...section-X.Y.html[#id]" links per the rule
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent

# (old basename, a_basename, b_basename, full a path, full b path)
SPLITS = [
    ("part-1-llm-building-blocks/module-00-ml-pytorch-foundations", "section-0.3.html", "section-0.3a.html", "section-0.3b.html"),
    ("part-1-llm-building-blocks/module-03-transformer-architecture", "section-3.1.html", "section-3.1a.html", "section-3.1b.html"),
    ("part-4-training-adaptation/module-17-peft", "section-17.5.html", "section-17.5a.html", "section-17.5b.html"),
    ("part-7-retrieval-information-extraction-with-llms/module-32-rag", "section-32.1.html", "section-32.1a.html", "section-32.1b.html"),
    ("part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag", "section-35.5.html", "section-35.5a.html", "section-35.5b.html"),
]

# Special prev/next neighbor rewrites
# (file relative to BOOK, current href substring, replacement href)
PREV_NEXT_REWRITES = [
    # 0.2 next -> 0.3a; 0.4 prev -> 0.3b
    ("part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.2.html",
     '<a class="next" href="section-0.3.html"><span class="nav-label">Next</span><span class="nav-num">Section 0.3</span><span class="nav-title">PyTorch in 90 Minutes: Tensors to Training Loop</span></a>',
     '<a class="next" href="section-0.3a.html"><span class="nav-label">Next</span><span class="nav-num">Section 0.3a</span><span class="nav-title">PyTorch Tensors, Autograd &amp; Training Loop</span></a>'),
    ("part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html",
     '<a class="prev" href="section-0.3.html"><span class="nav-label">Previous</span><span class="nav-num">Section 0.3</span><span class="nav-title">PyTorch in 90 Minutes: Tensors to Training Loop</span></a>',
     '<a class="prev" href="section-0.3b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 0.3b</span><span class="nav-title">PyTorch Debugging, Lab &amp; Modern Performance</span></a>'),
    # 3.2 prev -> 3.1b
    ("part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html",
     '<a class="prev" href="section-3.1.html"><span class="nav-label">Previous</span><span class="nav-num">Section 3.1</span><span class="nav-title">How a Transformer Computes One Token</span></a>',
     '<a class="prev" href="section-3.1b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 3.1b</span><span class="nav-title">Transformer Init, Causal Mask &amp; Forward Pass</span></a>'),
    # 17.4 next -> 17.5a; 17.6 prev -> 17.5b
    ("part-4-training-adaptation/module-17-peft/section-17.4.html",
     '<a class="next" href="section-17.5.html"><span class="nav-label">Next</span><span class="nav-num">Section 17.5</span><span class="nav-title">Knowledge Distillation for LLMs</span></a>',
     '<a class="next" href="section-17.5a.html"><span class="nav-label">Next</span><span class="nav-num">Section 17.5a</span><span class="nav-title">Knowledge Distillation: Foundations &amp; Pipelines</span></a>'),
    ("part-4-training-adaptation/module-17-peft/section-17.6.html",
     '<a class="prev" href="section-17.5.html"><span class="nav-label">Previous</span><span class="nav-num">Section 17.5</span><span class="nav-title">Knowledge Distillation for LLMs</span></a>',
     '<a class="prev" href="section-17.5b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 17.5b</span><span class="nav-title">Distillation: Licensing, Speculative &amp; Reasoning</span></a>'),
    # 31.5 next -> 32.1a (cross-chapter); 32.2 prev -> 32.1b
    ("part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html",
     '<a class="next" href="../module-32-rag/section-32.1.html"><span class="nav-label">Next</span><span class="nav-num">Section 32.1</span><span class="nav-title">RAG Architecture &amp; Fundamentals</span></a>',
     '<a class="next" href="../module-32-rag/section-32.1a.html"><span class="nav-label">Next</span><span class="nav-num">Section 32.1a</span><span class="nav-title">RAG Foundations: Pipeline &amp; Why It Beats Fine-Tuning</span></a>'),
    ("part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html",
     '<a class="prev" href="section-32.1.html"><span class="nav-label">Previous</span><span class="nav-num">Section 32.1</span><span class="nav-title">RAG Architecture &amp; Fundamentals</span></a>',
     '<a class="prev" href="section-32.1b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 32.1b</span><span class="nav-title">RAG Indexing, Evaluation &amp; Long-Context Tradeoff</span></a>'),
    # 35.4 next -> 35.5a; 36.1 prev -> 35.5b (cross-chapter)
    ("part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html",
     '<a class="next" href="section-35.5.html"><span class="nav-label">Next</span><span class="nav-num">Section 35.5</span><span class="nav-title">RAG Frameworks &amp; Orchestration</span></a>',
     '<a class="next" href="section-35.5a.html"><span class="nav-label">Next</span><span class="nav-num">Section 35.5a</span><span class="nav-title">RAG Frameworks: LangChain, LlamaIndex &amp; Haystack</span></a>'),
    ("part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.1.html",
     '<a class="prev" href="../module-35-advanced-rag/section-35.5.html"><span class="nav-label">Previous</span><span class="nav-num">Section 35.5</span><span class="nav-title">RAG Frameworks &amp; Orchestration</span></a>',
     '<a class="prev" href="../module-35-advanced-rag/section-35.5b.html"><span class="nav-label">Previous</span><span class="nav-num">Section 35.5b</span><span class="nav-title">RAG Production: DSPy, Hardening &amp; Security</span></a>'),
]


def collect_ids(html_path: Path):
    """Return set of all id="..." attribute values in the html."""
    text = html_path.read_text(encoding="utf-8")
    return set(m.group(1) for m in re.finditer(r' id="([^"]+)"', text))


def build_id_maps():
    """For each split, build dict mapping {anchor_id: 'a' or 'b'}."""
    maps = {}
    for module_rel, old, a, b in SPLITS:
        old_full = (BOOK / module_rel / old).as_posix()
        a_path = BOOK / module_rel / a
        b_path = BOOK / module_rel / b
        ids_a = collect_ids(a_path)
        ids_b = collect_ids(b_path)
        # In case of collision: prefer b for newer position; but realistically, the front-matter (shared)
        # has ids that exist in BOTH. For those collisions, route to a.
        m = {}
        for i in ids_a:
            m[i] = a
        for i in ids_b:
            if i not in m:
                m[i] = b
            # else keep 'a'
        maps[(module_rel, old)] = m
    return maps


def apply_xref_fixes(maps):
    """Walk the book and rewrite href="...section-X.Y.html" references."""
    book_files = list(BOOK.rglob("*.html"))
    # Exclude KDP/output and node_modules and similar build dirs
    exclude_substrings = ["KDP", "node_modules", "pagefind", "vendor", "_archive"]
    book_files = [f for f in book_files if not any(s in str(f) for s in exclude_substrings)]

    # Build mapping of OLD basename -> per-split details
    # Old href patterns:
    #   section-X.Y.html
    #   section-X.Y.html#anchor
    #   ../module-XX-foo/section-X.Y.html
    #   ../../part-N/module-XX-foo/section-X.Y.html
    # We must match by the relative-path tail ending in old_basename
    changes = 0
    for f in book_files:
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        orig = text

        for module_rel, old, a, b in SPLITS:
            id_map = maps[(module_rel, old)]
            # Build regex: match either "section-X.Y.html" or "section-X.Y.html#anchor"
            # We anchor on the basename within href="..." to avoid corrupting prose.
            # Match: href="(possible-prefix)/section-X.Y.html(#anchor)?"
            # We need both the basename match and to recompute the replacement.
            pattern = re.compile(r'href="([^"]*?)(' + re.escape(old) + r')(#([^"]+))?"')

            def repl(m):
                prefix = m.group(1)
                base = m.group(2)
                hash_part = m.group(3) or ""
                anchor = m.group(4)
                if anchor:
                    # Pick a or b by id_map
                    new_base = id_map.get(anchor, a)
                else:
                    new_base = a
                return f'href="{prefix}{new_base}{hash_part}"'

            new_text = pattern.sub(repl, text)
            if new_text != text:
                text = new_text

        if text != orig:
            f.write_text(text, encoding="utf-8")
            changes += 1
    return changes


def apply_prev_next_rewrites():
    n = 0
    for rel, old, new in PREV_NEXT_REWRITES:
        p = BOOK / rel
        if not p.exists():
            print(f"  MISS: file not found: {p}")
            continue
        t = p.read_text(encoding="utf-8")
        if old in t:
            t = t.replace(old, new)
            p.write_text(t, encoding="utf-8")
            n += 1
            print(f"  OK: {rel}")
        else:
            # Try a soft match - the title text may have already shifted
            # If we already see new, skip silently
            if new in t:
                print(f"  ALREADY: {rel}")
            else:
                print(f"  MISS: {rel} (couldn't find exact old block)")
    return n


if __name__ == "__main__":
    maps = build_id_maps()
    print("ID maps:")
    for k, v in maps.items():
        print(f"  {k[0]}/{k[1]}: {len(v)} ids")

    print()
    print("Applying targeted prev/next block rewrites...")
    n2 = apply_prev_next_rewrites()
    print(f"  Rewrote {n2} prev/next blocks.")

    print()
    print("Applying generic xref rewrites...")
    n = apply_xref_fixes(maps)
    print(f"  Rewrote {n} files.")
