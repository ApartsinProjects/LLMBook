"""
Inject <script defer src="...scripts/book.js"></script> into all section HTML files.
Adds the tag right before </head>.
Skips files that already have it.
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

stats = {"scanned": 0, "injected": 0, "already_has": 0}


def get_root_path(filepath):
    rel = filepath.relative_to(BOOK_ROOT)
    depth = len(rel.parts) - 1
    if depth == 0:
        return "."
    return "/".join([".."] * depth)


def inject(filepath):
    content = filepath.read_text(encoding="utf-8")
    stats["scanned"] += 1

    if "book.js" in content:
        stats["already_has"] += 1
        return False

    root = get_root_path(filepath)
    script_tag = f'<script defer src="{root}/scripts/book.js"></script>'

    # Insert before </head>
    if "</head>" in content:
        content = content.replace("</head>", f"{script_tag}\n</head>", 1)
        filepath.write_text(content, encoding="utf-8")
        stats["injected"] += 1
        return True

    return False


def main():
    patterns = [
        "part-*/module-*/section-*.html",
        "part-*/module-*/index.html",
        "appendices/appendix-*/section-*.html",
        "appendices/appendix-*/index.html",
        "front-matter/*.html",
        "part-*/index.html",
    ]

    all_files = []
    for pattern in patterns:
        all_files.extend(BOOK_ROOT.glob(pattern))
    all_files = sorted(set(all_files))

    print(f"Scanning {len(all_files)} files...")

    for f in all_files:
        changed = inject(f)
        if changed:
            print(f"  INJECTED: {f.relative_to(BOOK_ROOT)}")

    print(f"\n=== Summary ===")
    print(f"Total scanned: {stats['scanned']}")
    print(f"Script tag injected: {stats['injected']}")
    print(f"Already had book.js: {stats['already_has']}")


if __name__ == "__main__":
    main()
