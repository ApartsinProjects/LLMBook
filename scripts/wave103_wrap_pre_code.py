"""Wave 103: Wrap orphan <pre><code> blocks in <div class="code-block-wrapper">.

The audit flags <pre><code class="pygments-highlighted lang-text"> elements
that are NOT inside the canonical <div class="code-block-wrapper">.
Wrapping them ensures correct margins, copy-button placement, and
caption alignment per the book's CSS.

Skips files currently being modified by background agents (dedup,
split-pair polish) to avoid edit conflicts.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

# Files currently being edited by background agents
AGENT_FILES = {
    # 24 split-pair files (polish agent aeab98f)
    "section-0.3a.html", "section-0.3b.html",
    "section-3.1a.html", "section-3.1b.html",
    "section-19.3a.html", "section-19.3b.html",
    "section-31.1a.html", "section-31.1b.html",
    "section-47.1a.html", "section-47.1b.html",
    "section-35.1a.html", "section-35.1b.html",
    "section-5.2a.html", "section-5.2b.html",
    "section-10.6a.html", "section-10.6b.html",
    "section-66.2.html",
    "section-17.5a.html", "section-17.5b.html",
    "section-32.1a.html", "section-32.1b.html",
    "section-35.5a.html", "section-35.5b.html",
    # Dedup agent (a048b64) targets
    "section-42.6.html", "section-42.9.html",
    "section-42.4.html", "section-44.3.html", "section-44.5.html",
    "section-1.5.html", "section-1.6.html", "section-1.7.html",
}

# Match <pre><code class="pygments-highlighted lang-..."> ... </code></pre>
# that is NOT immediately preceded by <div class="code-block-wrapper">.
PRE_RE = re.compile(
    r'<pre><code\s+class="pygments-highlighted[^"]*">.*?</code></pre>',
    re.DOTALL,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    n_fixes = 0
    out_chunks: list[str] = []
    pos = 0
    for m in PRE_RE.finditer(text):
        before = text[pos:m.start()]
        # Walk back a small window to check for the wrapper opening
        # tag immediately before this <pre>.
        tail = text[max(0, m.start() - 200):m.start()]
        if re.search(r'<div\s+class="code-block-wrapper"[^>]*>\s*$', tail):
            # Already wrapped; emit as-is
            out_chunks.append(before)
            out_chunks.append(m.group(0))
            pos = m.end()
            continue
        # Wrap it
        out_chunks.append(before)
        out_chunks.append('<div class="code-block-wrapper">')
        out_chunks.append(m.group(0))
        out_chunks.append('</div>')
        pos = m.end()
        n_fixes += 1
    out_chunks.append(text[pos:])
    if n_fixes == 0:
        return 0
    p.write_text(''.join(out_chunks), encoding="utf-8")
    return n_fixes


def main():
    n_files = n_total = 0
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & SKIP:
            continue
        if p.name in AGENT_FILES:
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_total += n
            print(f"  + {p.relative_to(ROOT)}: wrapped {n} pre/code block(s)")
    print(f"\nFiles touched: {n_files}, wrappings: {n_total}")


if __name__ == "__main__":
    main()
