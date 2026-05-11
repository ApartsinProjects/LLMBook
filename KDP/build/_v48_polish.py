"""v4.8: Polish pass on remaining manual items.

  1. Cross-refs for content overlap pairs (20.3.4 ↔ 20.7, 27.5 ↔ 27.6,
     28 ↔ 27.6).
  2. 'Optional - for depth' callouts on Module 4.3, 4.4, 4.5.
  3. Smooth section 4.1 info-theory teaser sentence.
  4. Real Python syntax errors: U+2208 (∈) inside code blocks should be
     'in' or other keyword; unterminated string literals.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def safe_read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


# =====================================================================
# 1. Cross-refs for content overlap pairs
# =====================================================================
def add_overlap_crossrefs() -> None:
    pairs = [
        # (file, target_section_basename, target_title, position_marker)
        ("part-5-retrieval-conversation/module-20-rag/section-20.3.html",
         "section-20.7", "Section 20.7: GraphRAG (full treatment)",
         "GraphRAG"),
        ("part-5-retrieval-conversation/module-20-rag/section-20.7.html",
         "section-20.3", "Section 20.3 (where GraphRAG was first introduced)",
         None),  # always insert at top
        ("part-7-multimodal-applications/module-27-multimodal/section-27.5.html",
         "section-27.6", "Section 27.6 (Robotics deployment patterns)",
         None),
        ("part-7-multimodal-applications/module-27-multimodal/section-27.6.html",
         "section-27.5", "Section 27.5 (VLA model architectures)",
         None),
        ("part-7-multimodal-applications/module-28-llm-applications/section-28.1.html",
         "../../module-27-multimodal/section-27.6", "Section 27.6 (Robotics applications including SayCan)",
         None),
    ]
    n = 0
    for rel, target_base, target_title, marker in pairs:
        p = ROOT / rel
        if not p.exists(): continue
        text = safe_read(p)
        # Skip if cross-ref already added
        if f"href=\"{target_base}.html\"" in text and target_title in text:
            continue
        # Build the cross-ref aside
        aside = (
            f'\n<aside class="callout note">\n'
            f'<div class="callout-title">Related coverage</div>\n'
            f'<p>This topic is also discussed in '
            f'<a class="cross-ref" href="{target_base}.html">{target_title}</a>. '
            f'Cross-reference for related context and depth.</p>\n'
            f'</aside>\n'
        )
        # Insert after first <p> in <main>
        new_text = re.sub(
            r'(<main[^>]*>(?:[^<]|<(?!p\s))*?<p[^>]*>[^<]*</p>\s*)',
            r'\1' + aside,
            text, count=1, flags=re.DOTALL,
        )
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n += 1
            print(f"  cross-ref added in {rel.split('/')[-1]} -> {target_base}")
    print(f"  Total: {n} cross-ref asides added\n")


# =====================================================================
# 2. 'Optional - for depth' callouts on Module 4 sections
# =====================================================================
def mark_module_4_optional() -> None:
    targets = [
        ("part-1-foundations/module-04-transformer-architecture/section-4.3.html",
         "Transformer Variants & Efficiency"),
        ("part-1-foundations/module-04-transformer-architecture/section-4.4.html",
         "GPU Fundamentals & Systems"),
        ("part-1-foundations/module-04-transformer-architecture/section-4.5.html",
         "Transformer Expressiveness Theory"),
    ]
    for rel, _topic in targets:
        p = ROOT / rel
        if not p.exists(): continue
        text = safe_read(p)
        if 'class="optional-marker"' in text:
            continue
        marker = (
            '\n<aside class="callout note optional-marker">\n'
            '<div class="callout-title">Optional - for depth</div>\n'
            '<p>This section dives deeper into a topic that is not strictly '
            'required for the rest of the book. Readers who are time-constrained '
            'can skim or skip on first pass and return when they need the '
            'specific details. The next section assumes only what was covered '
            'in the earlier sections of this chapter.</p>\n'
            '</aside>\n'
        )
        # Insert right after <h1>
        new_text = re.sub(
            r'(</h1>\s*)',
            r'\1' + marker,
            text, count=1,
        )
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            print(f"  optional marker added: {rel.split('/')[-1]}")


# =====================================================================
# 3. Smooth section 4.1 info-theory teaser
# =====================================================================
def smooth_4_1_teaser() -> None:
    p = ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.1.html"
    text = safe_read(p)
    original = text
    # The current teaser starts abruptly: "Modern language modeling rests on
    # four information-theoretic quantities: ..."
    # Smooth by adding a sentence connecting transformer mechanics back to it
    old = ("Modern language modeling rests on four information-theoretic quantities")
    new = ("Before we trace a token through the architecture, a quick reminder "
           "of the four information-theoretic quantities that recur throughout "
           "the rest of this book. Modern language modeling rests on those four")
    if old in text and new not in text:
        text = text.replace(old, new, 1)
        p.write_text(text, encoding="utf-8")
        print("  4.1 info-theory teaser smoothed (added connecting sentence)")


# =====================================================================
# 4. Real Python syntax errors
# =====================================================================
def fix_python_syntax_errors() -> None:
    # Replace U+2208 (∈) with 'in' inside code blocks
    n = 0
    targets = [
        ROOT / "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html",
        ROOT / "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.3.html",
    ]
    for p in targets:
        if not p.exists(): continue
        text = safe_read(p)
        original = text
        # Inside <code class="lang-python">...</code> blocks, replace ∈ with 'in'
        # and clean other math symbols
        def fix_block(m):
            body = m.group(1)
            # Only act if it has ∈
            if '∈' not in body and '∉' not in body and '∀' not in body:
                return m.group(0)
            body2 = body.replace('∈', ' in ').replace('∉', ' not in ').replace('∀', '# for all ')
            return f'{m.group(0)[:m.group(0).index(body)]}{body2}{m.group(0)[m.group(0).index(body)+len(body):]}'
        text = re.sub(r'<code\s+[^>]*class="[^"]*lang-python[^"]*"[^>]*>(.*?)</code>',
                       fix_block, text, flags=re.DOTALL)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n += 1
            print(f"  fixed Python math symbols in {p.name}")
    print(f"  Total: {n} Python files fixed")


def main() -> int:
    print("1. Cross-refs for content overlap pairs:"); add_overlap_crossrefs()
    print("2. Optional markers on Module 4.3-4.5:"); mark_module_4_optional()
    print("3. Smooth 4.1 teaser:"); smooth_4_1_teaser()
    print("4. Python syntax fixes:"); fix_python_syntax_errors()
    return 0


if __name__ == "__main__":
    sys.exit(main())
