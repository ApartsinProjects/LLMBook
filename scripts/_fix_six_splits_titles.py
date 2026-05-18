"""
Post-fix the split section files:
1. Escape & to &amp; in <title> tags.
2. Fix 35.5b "next" link to point to section-36.1.html instead of module index.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent

files_to_fix = [
    BOOK / "part-1-llm-building-blocks" / "module-00-ml-pytorch-foundations" / "section-0.3a.html",
    BOOK / "part-1-llm-building-blocks" / "module-00-ml-pytorch-foundations" / "section-0.3b.html",
    BOOK / "part-1-llm-building-blocks" / "module-03-transformer-architecture" / "section-3.1a.html",
    BOOK / "part-1-llm-building-blocks" / "module-03-transformer-architecture" / "section-3.1b.html",
    BOOK / "part-4-training-adaptation" / "module-17-peft" / "section-17.5a.html",
    BOOK / "part-4-training-adaptation" / "module-17-peft" / "section-17.5b.html",
    BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1a.html",
    BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-32-rag" / "section-32.1b.html",
    BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-35-advanced-rag" / "section-35.5a.html",
    BOOK / "part-7-retrieval-information-extraction-with-llms" / "module-35-advanced-rag" / "section-35.5b.html",
]


def fix_title_amp(text: str) -> str:
    # Find the line(s) containing <title>...</title> and replace bare & with &amp;
    def repl(m):
        inner = m.group(1)
        # Replace & that is NOT already part of an entity
        # Simple approach: replace standalone & (not followed by 'amp;', 'lt;', 'gt;', 'quot;', '#')
        new_inner = re.sub(r'&(?!(amp;|lt;|gt;|quot;|#))', '&amp;', inner)
        return f'<title>{new_inner}</title>'
    return re.sub(r'<title>(.*?)</title>', repl, text)


def fix_nav_linear_chain_35_5b(text: str) -> str:
    """For section-35.5b.html, change the chapter-nav next link to point to section-36.1.html."""
    old = '<a class="next" href="../module-36-retrieval-tools/index.html"><span class="nav-label">Next</span><span class="nav-num">Chapter 36</span><span class="nav-title">Retrieval Tools of the Trade</span></a>'
    new = '<a class="next" href="../module-36-retrieval-tools/section-36.1.html"><span class="nav-label">Next</span><span class="nav-num">Section 36.1</span><span class="nav-title">Platforms</span></a>'
    return text.replace(old, new)


if __name__ == "__main__":
    for p in files_to_fix:
        text = p.read_text(encoding="utf-8")
        orig = text
        text = fix_title_amp(text)
        if p.name == "section-35.5b.html":
            text = fix_nav_linear_chain_35_5b(text)
        if text != orig:
            p.write_text(text, encoding="utf-8")
            print(f"  OK: {p.name}")
        else:
            print(f"  NO CHANGE: {p.name}")
