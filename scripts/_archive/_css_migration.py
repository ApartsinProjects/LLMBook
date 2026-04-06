"""
CSS Migration Script
====================
Migrates all HTML files from inline <style> blocks to linking the shared
stylesheet styles/book.css.

Covers: part-*/, appendices/, capstone/, and root index.html.
"""

import os
import re
import glob

ROOT = r"E:/Projects/LLMCourse"
CSS_FILE = os.path.join(ROOT, "styles", "book.css")

# ------------------------------------------------------------------ #
#  Step 0: Ensure .nav-footer exists in book.css
# ------------------------------------------------------------------ #
def ensure_nav_footer():
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    if ".nav-footer" in css:
        print("[nav-footer] Already defined in book.css, skipping.")
        return

    nav_footer_block = """
/* ----- Nav footer (legacy class) ----- */
.nav-footer {
    display: flex;
    justify-content: space-between;
    padding: 2rem 0;
    margin-top: 3rem;
    border-top: 1px solid #e0e0e0;
    font-size: 0.95rem;
}

.nav-footer a {
    color: var(--primary, #0f3460);
    text-decoration: none;
}

.nav-footer a:hover {
    text-decoration: underline;
}
"""
    with open(CSS_FILE, "a", encoding="utf-8") as f:
        f.write(nav_footer_block)
    print("[nav-footer] Added definition to book.css.")


# ------------------------------------------------------------------ #
#  Helpers
# ------------------------------------------------------------------ #
def relative_css_path(filepath):
    """Return the correct relative path from *filepath* to styles/book.css."""
    rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
    parts = rel.split("/")

    # root index.html
    if len(parts) == 1:
        return "styles/book.css"

    # part-*/index.html  OR  capstone/*.html
    if len(parts) == 2:
        return "../styles/book.css"

    # part-*/module-*/section-*.html  OR  part-*/module-*/index.html
    # appendices/appendix-*/index.html
    if len(parts) == 3:
        return "../../styles/book.css"

    # Deeper nesting (unlikely but safe)
    depth = len(parts) - 1
    return "/".join([".."] * depth) + "/styles/book.css"


def count_css_rules(style_text):
    """Rough count of CSS selectors (rules) inside a <style> block."""
    # Strip comments
    stripped = re.sub(r"/\*.*?\*/", "", style_text, flags=re.DOTALL)
    # Count opening braces as a proxy for rule count
    return stripped.count("{")


def process_file(filepath):
    """Process a single HTML file. Returns a status string."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Already has a link to book.css?  Skip.
    if re.search(r'<link[^>]+book\.css[^>]*>', html):
        return "already-linked"

    rel_path = relative_css_path(filepath)
    link_tag = f'<link rel="stylesheet" href="{rel_path}">'

    # Locate the <style>...</style> block inside <head>
    head_match = re.search(r"(<head[^>]*>)(.*?)(</head>)", html, re.DOTALL)
    if not head_match:
        return "no-head"

    head_content = head_match.group(2)
    style_match = re.search(r"<style[^>]*>(.*?)</style>", head_content, re.DOTALL)

    if style_match:
        style_text = style_match.group(1)
        rule_count = count_css_rules(style_text)
        full_style_tag = style_match.group(0)

        if rule_count < 20:
            # Keep small override block AFTER the link tag
            replacement = link_tag + "\n    " + full_style_tag
        else:
            # Remove the entire style block, replace with just the link
            replacement = link_tag

        new_head_content = head_content.replace(full_style_tag, replacement, 1)
    else:
        # No <style> block at all; inject link tag after last <meta> or <title>
        insertion_point = None
        for tag in ["</title>", "</meta>", "<meta"]:
            idx = head_content.rfind(tag)
            if idx != -1:
                # Find end of that line
                nl = head_content.find("\n", idx)
                if nl == -1:
                    nl = len(head_content)
                insertion_point = nl
                break
        if insertion_point is None:
            insertion_point = 0

        new_head_content = (
            head_content[:insertion_point]
            + "\n    " + link_tag
            + head_content[insertion_point:]
        )

    new_html = html[:head_match.start(2)] + new_head_content + html[head_match.end(2):]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_html)

    if style_match:
        if rule_count < 20:
            return f"migrated-kept-override({rule_count} rules)"
        else:
            return f"migrated-removed-style({rule_count} rules)"
    else:
        return "migrated-no-style-found"


# ------------------------------------------------------------------ #
#  Collect all HTML files
# ------------------------------------------------------------------ #
def collect_html_files():
    files = []

    # Root index.html
    root_index = os.path.join(ROOT, "index.html")
    if os.path.isfile(root_index):
        files.append(root_index)

    # part-*/**/*.html
    for f in glob.glob(os.path.join(ROOT, "part-*", "**", "*.html"), recursive=True):
        files.append(f)

    # appendices/**/*.html
    for f in glob.glob(os.path.join(ROOT, "appendices", "**", "*.html"), recursive=True):
        files.append(f)

    # capstone/*.html
    for f in glob.glob(os.path.join(ROOT, "capstone", "*.html")):
        files.append(f)

    return sorted(set(files))


# ------------------------------------------------------------------ #
#  Main
# ------------------------------------------------------------------ #
def main():
    print("=" * 60)
    print("CSS Migration: inline <style> -> styles/book.css")
    print("=" * 60)

    ensure_nav_footer()

    files = collect_html_files()
    print(f"\nFound {len(files)} HTML files to process.\n")

    stats = {}
    for fp in files:
        status = process_file(fp)
        stats.setdefault(status, []).append(fp)
        short = os.path.relpath(fp, ROOT).replace("\\", "/")
        print(f"  [{status}] {short}")

    # ---- Summary ---- #
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for status, flist in sorted(stats.items()):
        print(f"  {status}: {len(flist)} files")
    print(f"  TOTAL: {len(files)} files")

    # ---- Verification ---- #
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    link_count = 0
    style_count = 0
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        if re.search(r'<link[^>]+book\.css[^>]*>', content):
            link_count += 1
        if re.search(r"<style[^>]*>", content):
            style_count += 1

    print(f"  Files with <link> to book.css: {link_count}")
    print(f"  Files still containing <style>: {style_count}")

    # Verify book.css has required definitions
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    required = [
        ".epigraph", ".prerequisites", ".whats-next", ".bibliography",
        ".code-caption", ".callout.big-picture", ".callout.key-insight",
        ".callout.note", ".callout.warning", ".callout.practical-example",
        ".callout.fun-note", ".callout.research-frontier",
        ".chapter-header", ".part-label", ".chapter-label",
        ".nav-footer", ".illustration", ".lab",
        "@media"
    ]
    print("\n  Required definitions in book.css:")
    all_ok = True
    for sel in required:
        found = sel in css
        mark = "OK" if found else "MISSING"
        if not found:
            all_ok = False
        print(f"    {sel}: {mark}")

    if all_ok:
        print("\n  All required CSS definitions are present.")
    else:
        print("\n  WARNING: Some definitions are missing!")


if __name__ == "__main__":
    main()
