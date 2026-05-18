"""Wave 85: Wrap "Part Overview" h2 + paragraph in <div class="part-overview">.

8 part-index pages have <h2>Part Overview</h2><p>...</p> but lack the
required <div class="part-overview">...</div> wrapper. Audit plugin
PART_INDEX wants the wrapper as the canonical marker. This wave adds it
mechanically by finding the h2 + immediately-following p and wrapping
them in the canonical div.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

PARTS_NEEDING_FIX = [
    "part-5-multimodal-llms",
    "part-7-retrieval-information-extraction-with-llms",
    "part-8-conversational-ai-with-llms",
    "part-10-llm-security-runtime-safety",
    "part-11-llm-ethics-trust-governance",
    "part-12-llm-systems-at-scale",
    "part-13-llmops-lifecycle",
    "part-14-designing-llm-agent-products",
]

# Match: <h2>Part Overview</h2> (possibly with attrs/id) followed by
# whitespace and an immediately-following <p>...</p> (single or multi-line,
# but not crossing into another tag).
OVERVIEW_RE = re.compile(
    r'(<h2[^>]*>Part Overview</h2>)\s*'
    r'(<p[^>]*>.*?</p>)',
    re.IGNORECASE | re.DOTALL,
)


def fix_file(p: Path) -> bool:
    html = p.read_text(encoding="utf-8")
    # Skip if already wrapped
    if 'class="part-overview"' in html:
        return False
    m = OVERVIEW_RE.search(html)
    if not m:
        return False
    h2 = m.group(1)
    p_tag = m.group(2)
    new = (
        '<div class="part-overview">\n'
        f'{h2}\n'
        f'{p_tag}\n'
        '</div>'
    )
    new_html = html[:m.start()] + new + html[m.end():]
    if new_html == html:
        return False
    p.write_text(new_html, encoding="utf-8")
    return True


def main():
    n_fixed = 0
    for part in PARTS_NEEDING_FIX:
        p = ROOT / part / "index.html"
        if not p.exists():
            print(f"  ! missing: {p}")
            continue
        if fix_file(p):
            n_fixed += 1
            print(f"  + {part}: wrapped Part Overview")
        else:
            print(f"  . {part}: no change (already wrapped or pattern not found)")
    print(f"\nTotal part-index files updated: {n_fixed}")


if __name__ == "__main__":
    main()
