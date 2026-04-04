"""
Synchronize the book tagline across all HTML pages.

Canonical tagline:
  "From the mathematics of attention to production agent systems.
   A practitioner's guide for engineers, researchers, and students."

Also removes any "Benchmarked against Stanford CS336..." text.
"""

import os
import re
import glob

ROOT = r"E:\Projects\LLMCourse"
CANONICAL = (
    "From the mathematics of attention to production agent systems. "
    "A practitioner\u2019s guide for engineers, researchers, and students."
)

changes = []

# ── Specific replacements keyed by relative path ──────────────────────────
# Each entry: (old_text, new_text)
TARGETED = {
    "cover.html": [
        # subtitle block
        (
            '<p class="subtitle">\n'
            "        From the mathematics of attention to production agent systems.\n"
            "        A complete guide for engineers, researchers, and leaders\n"
            "        at every stage of the journey.\n"
            "    </p>",
            '<p class="subtitle">\n'
            f"        {CANONICAL}\n"
            "    </p>",
        ),
    ],
    "toc.html": [
        (
            '<p class="chapter-subtitle">A comprehensive guide to the full stack of modern Large Language Model technology, from foundational NLP through production-grade AI agent systems.</p>',
            f'<p class="chapter-subtitle">{CANONICAL}</p>',
        ),
    ],
    "introduction.html": [
        (
            '<p class="subtitle">Your roadmap to mastering the full stack of Large Language Model technology</p>',
            f'<p class="subtitle">{CANONICAL}</p>',
        ),
    ],
}

def apply_targeted(rel, html):
    """Apply targeted text replacements for a specific file."""
    if rel not in TARGETED:
        return html, False
    modified = False
    for old, new in TARGETED[rel]:
        if old in html:
            html = html.replace(old, new)
            modified = True
    return html, modified


def remove_benchmarked(html):
    """Remove any 'Benchmarked against Stanford CS336...' sentences."""
    pattern = r'Benchmarked against Stanford CS336[^<.]*\.'
    new_html, count = re.subn(pattern, '', html)
    if count:
        return new_html, True
    return html, False


def main():
    # Collect all HTML files
    html_files = glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
    html_files.append(os.path.join(ROOT, "index.html"))
    html_files.append(os.path.join(ROOT, "cover.html"))
    html_files.append(os.path.join(ROOT, "toc.html"))
    html_files.append(os.path.join(ROOT, "introduction.html"))
    html_files = sorted(set(os.path.normpath(f) for f in html_files if os.path.isfile(f)))

    total_changed = 0

    for fpath in html_files:
        rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
        with open(fpath, "r", encoding="utf-8") as f:
            original = f.read()

        html = original

        # 1. Apply targeted replacements
        html, t1 = apply_targeted(rel, html)

        # 2. Remove benchmarked text
        html, t2 = remove_benchmarked(html)

        if html != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(html)
            total_changed += 1
            if t1:
                changes.append(f"  [tagline]     {rel}")
            if t2:
                changes.append(f"  [benchmarked] {rel}")

    print(f"Scanned {len(html_files)} HTML files.")
    print(f"Modified {total_changed} file(s):\n")
    for c in changes:
        print(c)

    if total_changed == 0:
        print("  (no changes needed)")

    # Verification: check that canonical tagline now appears where expected
    print("\n--- Verification ---")
    for key_file in ["cover.html", "toc.html", "introduction.html"]:
        fpath = os.path.join(ROOT, key_file)
        if not os.path.isfile(fpath):
            print(f"  SKIP (not found): {key_file}")
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if CANONICAL in content:
            print(f"  OK: {key_file}")
        else:
            print(f"  MISSING: {key_file} does not contain canonical tagline")

    # Also verify index.html (it uses span tags inside the subtitle)
    idx = os.path.join(ROOT, "index.html")
    with open(idx, "r", encoding="utf-8") as f:
        idx_content = f.read()
    if "From the mathematics of attention to production agent systems." in idx_content:
        print("  OK: index.html (contains canonical first sentence; uses span tags for easter eggs)")
    else:
        print("  MISSING: index.html does not contain canonical tagline")


if __name__ == "__main__":
    main()
