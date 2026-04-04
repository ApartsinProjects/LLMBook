"""Inject Prism.js syntax highlighting tags into all HTML files.

Inserts a CSS link and a single bundled JS script tag after the KaTeX
block in <head>. Computes the correct relative path based on file depth.
Idempotent: skips files that already have prism tags.
"""

import os
import re
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")

def get_relative_prefix(html_path: Path) -> str:
    """Return the relative path prefix from html_path to the project root."""
    rel = html_path.parent.relative_to(ROOT)
    depth = len(rel.parts)
    if depth == 0:
        return "."
    return "/".join([".."] * depth)

def build_prism_tags(prefix: str) -> str:
    """Build the two HTML tags for Prism CSS and JS."""
    return (
        f'    <link rel="stylesheet" href="{prefix}/vendor/prism/prism-theme.css">\n'
        f'    <script defer src="{prefix}/vendor/prism/prism-bundle.min.js"></script>'
    )

def process_file(html_path: Path) -> bool:
    """Inject Prism tags into a single HTML file. Returns True if modified."""
    text = html_path.read_text(encoding="utf-8")

    # Idempotency: skip if already has prism
    if "prism-theme.css" in text or "prism-bundle" in text:
        return False

    # Only add Prism to files that contain code blocks
    if '<code class="language-' not in text and "<code class='language-" not in text:
        return False

    prefix = get_relative_prefix(html_path)
    tags = build_prism_tags(prefix)

    # Strategy: insert after the last </script> before </head>
    # The KaTeX auto-render block ends with </script>\n</head>
    pattern = r'(</script>\s*)(</head>)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        insertion = match.group(1) + tags + "\n"
        text = text[:match.start()] + insertion + match.group(2) + text[match.end():]
        html_path.write_text(text, encoding="utf-8")
        return True

    # Fallback: insert before </head>
    pattern2 = r'(</head>)'
    match2 = re.search(pattern2, text, re.IGNORECASE)
    if match2:
        text = text[:match2.start()] + tags + "\n" + match2.group(1) + text[match2.end():]
        html_path.write_text(text, encoding="utf-8")
        return True

    return False

def main():
    html_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ("vendor", "node_modules", ".git", "__pycache__")]
        for f in filenames:
            if f.endswith(".html"):
                html_files.append(Path(dirpath) / f)

    modified = 0
    skipped = 0
    errors = 0
    for html_path in sorted(html_files):
        try:
            if process_file(html_path):
                modified += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {html_path}: {e}")
            errors += 1

    print(f"Done: {modified} modified, {skipped} skipped, {errors} errors")
    print(f"Total: {modified + skipped + errors}")

if __name__ == "__main__":
    main()
