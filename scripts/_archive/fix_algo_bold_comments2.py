"""Fix <b> tags to algo-line-keyword and add algo-line-comment in algorithm callout pre blocks."""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates", "styles"}

def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)

def fix_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    orig = text

    # Find algorithm callout blocks using multiline regex
    # Match from callout algorithm opening to its closing </div> (greedy enough to include <pre>)
    def fix_algo_block(match):
        block = match.group(0)

        # Only fix inside <pre>...</pre>
        def fix_pre_content(pre_match):
            content = pre_match.group(0)

            # Replace <b>text</b> with algo-line-keyword
            content = re.sub(
                r"<b>([^<]+)</b>",
                r'<span class="algo-line-keyword">\1</span>',
                content,
            )

            # Add algo-line-comment to // and # comment patterns
            lines = content.split("\n")
            new_lines = []
            for line in lines:
                if "algo-line-comment" not in line:
                    # Inline comments: // at end of line
                    if "//" in line:
                        line = re.sub(
                            r"(//[^<\n]*)",
                            r'<span class="algo-line-comment">\1</span>',
                            line,
                        )
                new_lines.append(line)
            return "\n".join(new_lines)

        block = re.sub(r"<pre[^>]*>.*?</pre>", fix_pre_content, block, flags=re.DOTALL)
        return block

    # Match callout algorithm divs (they contain <pre> blocks)
    text = re.sub(
        r'<div class="callout algorithm"[^>]*>.*?</pre>\s*</div>',
        fix_algo_block,
        text,
        flags=re.DOTALL,
    )

    if text != orig:
        filepath.write_text(text, encoding="utf-8")
        bold_diff = orig.count("<b>") - text.count("<b>")
        comment_diff = text.count("algo-line-comment") - orig.count("algo-line-comment")
        return bold_diff, comment_diff
    return 0, 0

def main():
    files = find_html_files()
    print(f"Scanning {len(files)} HTML files for algorithm callouts...\n")

    total_bold = 0
    total_comment = 0
    fixed_files = 0

    for f in files:
        b, c = fix_file(f)
        if b or c:
            fixed_files += 1
            total_bold += b
            total_comment += c
            print(f"  {f.relative_to(BASE)}: {b} bold->keyword, {c} comments")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {fixed_files} files, {total_bold} bold->keyword, {total_comment} comments added")

if __name__ == "__main__":
    main()
