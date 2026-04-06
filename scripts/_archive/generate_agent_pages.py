#!/usr/bin/env python3
"""
Generate HTML pages for each agent skill markdown file and a workflow page.
Uses regex-based markdown-to-HTML conversion with book-matching styles.
"""

import os
import re
import glob

SOURCE_DIR = r"C:\Users\apart\.claude\skills\textbook-chapter\agents"
SKILL_FILE = r"C:\Users\apart\.claude\skills\textbook-chapter\SKILL.md"
OUTPUT_DIR = r"E:\Projects\LLMCourse\agents"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---- Markdown to HTML converter (regex-based, no external packages) ----

def md_to_html(md_text):
    """Convert markdown text to HTML using regex replacements."""
    lines = md_text.split('\n')
    html_lines = []
    in_code_block = False
    code_lang = ''
    code_lines = []
    in_list = False
    in_ordered_list = False
    list_indent_stack = []  # track nested lists

    def close_lists():
        nonlocal in_list, in_ordered_list
        result = []
        if in_list:
            result.append('</ul>')
            in_list = False
        if in_ordered_list:
            result.append('</ol>')
            in_ordered_list = False
        return result

    def process_inline(text):
        """Process inline markdown: bold, italic, code, links."""
        # Inline code (must come before bold/italic to avoid conflicts)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Bold + italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        return text

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                html_lines.extend(close_lists())
                in_code_block = True
                code_lang = line.strip()[3:].strip()
                code_lines = []
                i += 1
                continue
            else:
                lang_attr = f' class="language-{code_lang}"' if code_lang else ''
                code_content = '\n'.join(code_lines)
                code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_lines.append(f'<pre><code{lang_attr}>{code_content}</code></pre>')
                in_code_block = False
                code_lang = ''
                code_lines = []
                i += 1
                continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        stripped = line.strip()

        # Empty line
        if not stripped:
            html_lines.extend(close_lists())
            i += 1
            continue

        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)', stripped)
        if heading_match:
            html_lines.extend(close_lists())
            level = len(heading_match.group(1))
            text = process_inline(heading_match.group(2))
            # Add id for anchoring
            anchor = re.sub(r'[^a-z0-9]+', '-', heading_match.group(2).lower()).strip('-')
            html_lines.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', stripped):
            html_lines.extend(close_lists())
            html_lines.append('<hr>')
            i += 1
            continue

        # Ordered list item
        ol_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if ol_match:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if not in_ordered_list:
                html_lines.append('<ol>')
                in_ordered_list = True
            html_lines.append(f'<li>{process_inline(ol_match.group(2))}</li>')
            i += 1
            continue

        # Unordered list item
        ul_match = re.match(r'^[-*+]\s+(.+)', stripped)
        if ul_match:
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{process_inline(ul_match.group(1))}</li>')
            i += 1
            continue

        # Indented sub-list items (starts with spaces then - or *)
        sub_match = re.match(r'^\s+[-*+]\s+(.+)', line)
        if sub_match and (in_list or in_ordered_list):
            html_lines.append(f'<li class="sub-item">{process_inline(sub_match.group(1))}</li>')
            i += 1
            continue

        # Indented continuation of ordered list (e.g. "   - Why it matters:")
        sub_ol_match = re.match(r'^\s+[-*+]\s+(.+)', line)
        if sub_ol_match:
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{process_inline(sub_ol_match.group(1))}</li>')
            i += 1
            continue

        # Blockquote
        if stripped.startswith('>'):
            html_lines.extend(close_lists())
            quote_text = process_inline(stripped[1:].strip())
            html_lines.append(f'<blockquote>{quote_text}</blockquote>')
            i += 1
            continue

        # Regular paragraph
        html_lines.extend(close_lists())
        html_lines.append(f'<p>{process_inline(stripped)}</p>')
        i += 1

    # Close any remaining open lists
    html_lines.extend(close_lists())

    return '\n'.join(html_lines)


def get_html_template(title, body_html, back_link="../team.html"):
    """Wrap converted HTML in a styled page template."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AI Textbook Agent Team</title>
    <style>
        :root {{
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #0f3460;
            --highlight: #e94560;
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text: #2d3436;
            --text-light: #636e72;
            --border: #dfe6e9;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
        }}

        header {{
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: white;
            padding: 2.5rem 2rem;
            text-align: center;
        }}
        header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}
        header .subtitle {{
            font-size: 1.05rem;
            opacity: 0.85;
            max-width: 700px;
            margin: 0 auto;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 1rem;
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            font-size: 0.95rem;
            transition: color 0.2s;
        }}
        .back-link:hover {{
            color: white;
            text-decoration: underline;
        }}

        .container {{
            max-width: 860px;
            margin: 0 auto;
            padding: 2.5rem 2rem 4rem;
        }}

        .content h1 {{
            font-size: 1.8rem;
            color: var(--primary);
            margin: 2rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--highlight);
        }}
        .content h2 {{
            font-size: 1.45rem;
            color: var(--secondary);
            margin: 2rem 0 0.8rem;
            padding-bottom: 0.3rem;
            border-bottom: 2px solid var(--border);
        }}
        .content h3 {{
            font-size: 1.2rem;
            color: var(--accent);
            margin: 1.5rem 0 0.6rem;
        }}
        .content h4 {{
            font-size: 1.05rem;
            color: var(--primary);
            margin: 1.2rem 0 0.5rem;
        }}
        .content h5, .content h6 {{
            font-size: 0.95rem;
            color: var(--text-light);
            margin: 1rem 0 0.4rem;
        }}

        .content p {{
            margin-bottom: 1rem;
            text-align: justify;
            hyphens: auto;
        }}

        .content ul, .content ol {{
            margin: 0.8rem 0 1.2rem 1.5rem;
        }}
        .content li {{
            margin-bottom: 0.4rem;
        }}
        .content li.sub-item {{
            margin-left: 1.5rem;
            list-style-type: circle;
        }}

        .content blockquote {{
            border-left: 4px solid var(--highlight);
            background: linear-gradient(135deg, rgba(233,69,96,0.05), rgba(15,52,96,0.05));
            padding: 1rem 1.5rem;
            margin: 1.2rem 0;
            border-radius: 0 8px 8px 0;
            font-style: italic;
            color: var(--primary);
        }}

        .content pre {{
            background: var(--primary);
            color: #e0e0e0;
            padding: 1.2rem 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.2rem 0;
            font-size: 0.9rem;
            line-height: 1.5;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .content code {{
            font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
            font-size: 0.9em;
        }}
        .content p code, .content li code, .content h2 code, .content h3 code {{
            background: rgba(15,52,96,0.08);
            color: var(--accent);
            padding: 2px 6px;
            border-radius: 4px;
        }}

        .content hr {{
            border: none;
            border-top: 2px solid var(--border);
            margin: 2rem 0;
        }}

        .content a {{
            color: var(--highlight);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-color 0.2s;
        }}
        .content a:hover {{
            border-bottom-color: var(--highlight);
        }}

        .content strong {{
            color: var(--primary);
            font-weight: 700;
        }}

        /* Table styling */
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.2rem 0;
        }}
        .content th {{
            background: var(--secondary);
            color: white;
            padding: 0.6rem 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .content td {{
            padding: 0.5rem 1rem;
            border-bottom: 1px solid var(--border);
            font-size: 0.9rem;
        }}
        .content tr:hover td {{
            background: rgba(15,52,96,0.03);
        }}

        footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-light);
            font-size: 0.85rem;
            border-top: 1px solid var(--border);
        }}

        @media (max-width: 768px) {{
            header {{ padding: 1.5rem 1rem; }}
            header h1 {{ font-size: 1.5rem; }}
            .container {{ padding: 1.5rem 1rem 3rem; }}
            .content h1 {{ font-size: 1.4rem; }}
            .content h2 {{ font-size: 1.2rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <p class="subtitle">AI Textbook Production Agent Team</p>
        <a href="{back_link}" class="back-link">&#8592; Back to Team Overview</a>
    </header>
    <div class="container">
        <div class="content">
{body_html}
        </div>
    </div>
    <footer>
        Part of the 36-Agent Textbook Production Pipeline
    </footer>
</body>
</html>'''


def extract_title_from_md(md_text):
    """Extract the first H1 heading as the page title."""
    match = re.match(r'^#\s+(.+)', md_text.strip(), re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Agent"


def process_agent_file(filepath, output_dir):
    """Read a markdown agent file and produce an HTML page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        md_text = f.read()

    title = extract_title_from_md(md_text)
    body_html = md_to_html(md_text)
    html = get_html_template(title, body_html)

    basename = os.path.splitext(os.path.basename(filepath))[0] + '.html'
    outpath = os.path.join(output_dir, basename)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Generated: {basename}")
    return basename


def process_workflow(skill_file, output_dir):
    """Extract the workflow/pipeline section from SKILL.md and create workflow.html."""
    with open(skill_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Remove the YAML front matter
    md_text = re.sub(r'^---\n.*?\n---\n', '', md_text, flags=re.DOTALL)

    title = "Textbook Chapter Production Pipeline"
    body_html = md_to_html(md_text.strip())
    html = get_html_template(title, body_html)

    outpath = os.path.join(output_dir, 'workflow.html')
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Generated: workflow.html")


def main():
    print("Generating agent HTML pages...")
    print(f"  Source: {SOURCE_DIR}")
    print(f"  Output: {OUTPUT_DIR}")
    print()

    # Process all agent markdown files
    agent_files = sorted(glob.glob(os.path.join(SOURCE_DIR, '*.md')))
    print(f"Found {len(agent_files)} agent files.")
    for filepath in agent_files:
        process_agent_file(filepath, OUTPUT_DIR)

    print()

    # Process workflow page
    print("Generating workflow page from SKILL.md...")
    process_workflow(SKILL_FILE, OUTPUT_DIR)

    print()
    print(f"Done! Generated {len(agent_files) + 1} HTML files in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
