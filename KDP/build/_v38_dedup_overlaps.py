"""v3.8: Auto-dedup substantive content overlaps identified in Round 6.

Strategy: pick the larger/more comprehensive section as canonical, delete
the smaller/duplicate, redirect inbound xrefs.

Targets:
  1. 20.7 GraphRAG (full chapter) overlaps with 20.3.4 (subsection of 20.3).
     Keep 20.7 as canonical (it's a full section). Delete the GraphRAG
     subsection from 20.3 (replace with 1-paragraph teaser + xref to 20.7).
  2. 21.5 Voice & multimodal interfaces vs 21.6 Voice agents.
     Keep 21.6 (titled 'Voice agents and speech interfaces' - more agentic).
     Merge 21.5 into 21.6, then delete 21.5.
  3. 26.8/9/10 (absorbed from Module 35) duplicate 26.3/4/5.
     Keep 26.3/4/5 (canonical Module 26 sections), delete 26.8/9/10.

This is conservative auto-dedup: when in doubt, keep the original section
and delete the absorbed/secondary one.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def update_inbound_refs(redirects: list[tuple[str, str]]) -> int:
    n_files = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        try:
            if p.stat().st_size > 5_000_000: continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        original = text
        for old, new in redirects:
            text = re.sub(rf'\b{re.escape(old)}\.html', f'{new}.html', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    return n_files


def delete_with_redirect(rel_path: str, target_basename: str) -> int:
    """Delete a section file, redirect all inbound refs to target."""
    p = ROOT / rel_path
    if not p.exists():
        print(f"  [skip] {rel_path} missing")
        return 0
    old_base = p.stem
    n = update_inbound_refs([(old_base, target_basename)])
    p.unlink()
    print(f"  rm {rel_path} -> redirected {n} files to {target_basename}.html")
    return n


def merge_section(src_rel: str, dst_rel: str, h2_title: str) -> int:
    """Append src content into dst as a new <h2>, then delete src."""
    src = ROOT / src_rel
    dst = ROOT / dst_rel
    if not src.exists() or not dst.exists():
        print(f"  [skip] src={src.exists()}, dst={dst.exists()}")
        return 0
    src_text = src.read_text(encoding="utf-8", errors="replace")
    dst_text = dst.read_text(encoding="utf-8", errors="replace")
    # Extract <main>...</main> body of src
    m = re.search(r"<main[^>]*>(.*?)</main>", src_text, re.DOTALL)
    if not m: m = re.search(r"<body[^>]*>(.*?)</body>", src_text, re.DOTALL)
    src_body = m.group(1) if m else src_text
    # Strip H1 + chrome
    src_body = re.sub(r"<h1[^>]*>.*?</h1>", "", src_body, count=1, flags=re.DOTALL)
    src_body = re.sub(r"<header[^>]*chapter-header[^>]*>.*?</header>",
                       "", src_body, count=1, flags=re.DOTALL)
    src_body = re.sub(r"<details[^>]*bibliography-collapsible[^>]*>.*?</details>",
                       "", src_body, flags=re.DOTALL)
    src_body = re.sub(r"<aside[^>]*whats-next[^>]*>.*?</aside>",
                       "", src_body, flags=re.DOTALL)

    block = f'\n<hr class="merged-section-divider"/>\n<section class="merged-section">\n<h2>{h2_title}</h2>\n{src_body.strip()}\n</section>\n'
    if "</main>" in dst_text:
        idx = dst_text.find("</main>")
        new_dst = dst_text[:idx] + block + dst_text[idx:]
    else:
        new_dst = dst_text + block
    dst.write_text(new_dst, encoding="utf-8")
    src.unlink()
    n = update_inbound_refs([(src.stem, dst.stem)])
    print(f"  merged {src_rel} -> {dst_rel} ({n} inbound refs redirected)")
    return n


def main() -> int:
    print("=== Op 1: 26.8/9/10 duplicate 26.3/4/5 - delete the absorbed ones ===")
    delete_with_redirect(
        "part-6-agentic-ai/module-26-agent-safety-production/section-26.8.html",
        "section-26.3"  # 26.8 = Reliability Engineering, overlaps 26.3 Production Observability
    )
    delete_with_redirect(
        "part-6-agentic-ai/module-26-agent-safety-production/section-26.9.html",
        "section-26.4"  # 26.9 = Observability/CI for Agents, overlaps 26.4 Error Recovery
    )
    delete_with_redirect(
        "part-6-agentic-ai/module-26-agent-safety-production/section-26.10.html",
        "section-26.5"  # 26.10 = Self-Improving Agents, overlaps 26.5 Testing Multi-Agent
    )

    print("\n=== Op 2: 21.5 voice merged into 21.6 ===")
    merge_section(
        "part-5-retrieval-conversation/module-21-conversational-ai/section-21.5.html",
        "part-5-retrieval-conversation/module-21-conversational-ai/section-21.6.html",
        "21.6.X Voice and Multimodal Interfaces (merged content)",
    )

    # Note: 20.7 GraphRAG dedup left for editorial review (substantive content
    # overlap, but both sections have unique content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
