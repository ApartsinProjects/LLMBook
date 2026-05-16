"""Convert <div class="callout bibliography"><ul class="bibliography-list">
blocks to the canonical collapsible card pattern used in templates:

  <details class="bibliography-collapsible" open>
  <summary><strong>{title}</strong></summary>
  <section class="bibliography">
    <h3>{optional sub-heading if h4 was inside}</h3>
    <div class="bib-entry-card">
      <div class="bib-ref">{li-content}</div>
    </div>
    ...
  </section>
  </details>

Preserves:
- The title (Further Reading / Bibliography / References) as the summary
- Any h4 sub-headings as h3 inside the section
- All link entries with their notes / annotations
- The <a> tags, <strong>, <em>, etc. inside each li
- rel='noopener' target='_blank' attrs

Skips bibliography blocks already in the collapsible-card form.

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}


def convert_one_block(text: str) -> tuple[str, int]:
    """Find a <div class="callout bibliography"> block and convert it.
    Returns (text, count_converted)."""
    n = 0

    # Match the canonical block. We need a non-greedy / balanced approach
    # because <ul class="bibliography-list"> is the inner element.
    pattern = re.compile(
        r'<div class="callout bibliography">\s*'
        r'(?:<div class="callout-title">([^<]+)</div>\s*)?'  # title (optional)
        r'([\s\S]*?)'                                        # body
        r'</div>',
    )

    def repl(m: re.Match) -> str:
        nonlocal n
        title = (m.group(1) or "Further Reading").strip()
        body = m.group(2)

        # Extract h4 sub-headings and ul/li structure from body
        # Each `<h4>...</h4>` becomes `<h3>...</h3>` inside section.
        # Each `<ul class="bibliography-list">...</ul>` is unpacked into
        # bib-entry-card divs.

        out_parts: list[str] = []
        cursor = 0
        for sub in re.finditer(
            r'<h4[^>]*>([^<]+)</h4>|'
            r'<ul[^>]*class="bibliography-list"[^>]*>([\s\S]*?)</ul>',
            body,
        ):
            if cursor < sub.start():
                # Trailing content between blocks (rarely useful) is
                # passed through.
                stray = body[cursor:sub.start()].strip()
                if stray and not re.match(r'^\s*<!--', stray):
                    out_parts.append(stray)
            if sub.group(1):  # h4 heading
                out_parts.append(f'<h3>{sub.group(1).strip()}</h3>')
            else:  # ul with li entries
                ul_body = sub.group(2)
                for li in re.finditer(r'<li[^>]*>([\s\S]*?)</li>', ul_body):
                    li_content = li.group(1).strip()
                    out_parts.append(
                        f'<div class="bib-entry-card">\n'
                        f'<div class="bib-ref">{li_content}</div>\n'
                        f'</div>'
                    )
            cursor = sub.end()
        if cursor < len(body):
            tail = body[cursor:].strip()
            if tail and not re.match(r'^\s*<!--', tail):
                out_parts.append(tail)

        if not out_parts:
            # Empty body — keep the block as a stub
            return m.group(0)

        n += 1
        body_html = "\n".join(out_parts)
        return (
            f'<details class="bibliography-collapsible" open>\n'
            f'<summary><strong>{title}</strong></summary>\n'
            f'<section class="bibliography">\n'
            f'{body_html}\n'
            f'</section>\n'
            f'</details>'
        )

    new_text = pattern.sub(repl, text)
    return new_text, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    total = 0
    files_edited = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        if '<div class="callout bibliography">' not in text:
            continue
        new_text, n = convert_one_block(text)
        if n > 0 and new_text != text:
            files_edited += 1
            total += n
            if not dry_run:
                p.write_text(new_text, encoding="utf-8")

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:            {files_edited}")
    print(f"Bibliography blocks:     {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
