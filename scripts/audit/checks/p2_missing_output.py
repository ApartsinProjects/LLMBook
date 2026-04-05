"""Detect code blocks that produce output but lack a following .code-output div."""
import json
import os
import re
import sys
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "MISSING_OUTPUT"
DESCRIPTION = "Code block with output-producing calls but no .code-output div follows"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Patterns that indicate the code produces visible output
OUTPUT_PATTERNS = [
    (re.compile(r'\bprint\s*\('), "print()"),
    (re.compile(r'\bdisplay\s*\('), "display()"),
    (re.compile(r'\.head\s*\('), ".head()"),
    (re.compile(r'\.describe\s*\('), ".describe()"),
    (re.compile(r'\.shape\b'), ".shape"),
    (re.compile(r'\.info\s*\('), ".info()"),
    (re.compile(r'>>>\s'), ">>> (REPL)"),
    (re.compile(r'\bpprint\s*\('), "pprint()"),
    (re.compile(r'\blogging\.'), "logging.*"),
    (re.compile(r'\blogger\.'), "logger.*"),
]

# Tags/patterns for opening and closing code blocks
PRE_OPEN_RE = re.compile(r'<pre\b[^>]*>', re.IGNORECASE)
PRE_CLOSE_RE = re.compile(r'</pre>', re.IGNORECASE)

# The output div we expect to find after an output-producing block
CODE_OUTPUT_RE = re.compile(r'<div\s+class="code-output"', re.IGNORECASE)

# Next structural boundary: another <pre> or a code-caption div
NEXT_BOUNDARY_RE = re.compile(
    r'<pre\b[^>]*>|<div\s+class="code-caption"',
    re.IGNORECASE,
)

# Detect if a <pre> is inside a callout div (check preceding lines)
CALLOUT_OPEN_RE = re.compile(r'<div\s+class="[^"]*\bcallout\b[^"]*"', re.IGNORECASE)
CALLOUT_CLOSE_RE = re.compile(r'</div>', re.IGNORECASE)

# Import/definition-only blocks: lines that only import or define
IMPORT_OR_DEF_RE = re.compile(
    r'^\s*(import\s|from\s\S+\s+import|class\s|def\s|#|@|\s*$|""".*"""|\'\'\'.*\'\'\')',
)


def _strip_html_tags(text):
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', '', text)


def _is_inside_callout(lines, pre_line_idx):
    """Check if this <pre> is nested inside a .callout div."""
    depth = 0
    for i in range(pre_line_idx - 1, max(-1, pre_line_idx - 40), -1):
        line = lines[i]
        # Count closing divs (they increase nesting depth going backwards)
        depth += len(re.findall(r'</div>', line, re.IGNORECASE))
        # Check for callout opening div
        for m in CALLOUT_OPEN_RE.finditer(line):
            if depth > 0:
                depth -= 1
            else:
                return True
        # Count non-callout opening divs
        non_callout_opens = len(re.findall(r'<div\b', line, re.IGNORECASE)) - len(CALLOUT_OPEN_RE.findall(line))
        depth -= non_callout_opens
    return False


def _is_definition_only(code_text):
    """Return True if the code block only imports or defines things (no output)."""
    lines = code_text.strip().split('\n')
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if not IMPORT_OR_DEF_RE.match(stripped):
            return False
    return True


def _find_output_triggers(code_text):
    """Return list of output-producing pattern descriptions found in code."""
    triggers = []
    for pattern, label in OUTPUT_PATTERNS:
        if pattern.search(code_text):
            triggers.append(label)
    return triggers


def run(filepath, html, context):
    """Run check on a single file. Called by the audit framework."""
    issues = []
    lines = html.split('\n')
    total = len(lines)

    i = 0
    while i < total:
        m_open = PRE_OPEN_RE.search(lines[i])
        if not m_open:
            i += 1
            continue

        pre_start = i

        # Collect code content until </pre>
        code_lines = []
        j = i
        found_close = False
        while j < total:
            text = lines[j] if j != i else lines[j][m_open.end():]
            m_close = PRE_CLOSE_RE.search(text if j != i else lines[j])
            if m_close and j != i:
                code_lines.append(text[:text.find('</pre>')])
                found_close = True
                break
            elif m_close and j == i:
                code_lines.append(text[:text.find('</pre>')])
                found_close = True
                break
            code_lines.append(text)
            j += 1

        pre_end = j
        if not found_close:
            i += 1
            continue

        code_text = _strip_html_tags('\n'.join(code_lines))

        # Skip short blocks (1-3 lines of actual code)
        non_empty = [ln for ln in code_text.strip().split('\n') if ln.strip()]
        if len(non_empty) <= 3:
            i = pre_end + 1
            continue

        # Skip blocks inside callout divs
        if _is_inside_callout(lines, pre_start):
            i = pre_end + 1
            continue

        # Skip definition-only blocks
        if _is_definition_only(code_text):
            i = pre_end + 1
            continue

        # Check for output-producing patterns
        triggers = _find_output_triggers(code_text)
        if not triggers:
            i = pre_end + 1
            continue

        # Look between </pre> and the next structural boundary for code-output
        has_output_div = False
        k = pre_end + 1
        while k < total:
            line = lines[k]
            if CODE_OUTPUT_RE.search(line):
                has_output_div = True
                break
            if NEXT_BOUNDARY_RE.search(line):
                break
            k += 1

        if not has_output_div:
            trigger_list = ", ".join(triggers[:3])
            if len(triggers) > 3:
                trigger_list += ", ..."
            issues.append(Issue(
                priority=PRIORITY,
                check_id=CHECK_ID,
                filepath=filepath,
                line=pre_start + 1,
                message=f"{trigger_list} found but no .code-output follows",
            ))

        i = pre_end + 1

    return issues


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------

def main():
    root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    skip_dirs = {"_archive", "node_modules", ".git", "vendor", "__pycache__"}
    json_mode = "--json" in sys.argv

    all_issues = []
    file_count = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for fname in sorted(filenames):
            if not fname.startswith("section-") or not fname.endswith(".html"):
                continue

            filepath = os.path.join(dirpath, fname)
            file_count += 1

            with open(filepath, encoding="utf-8", errors="replace") as f:
                html = f.read()

            relpath = os.path.relpath(filepath, root)
            file_issues = run(relpath, html, {})
            all_issues.extend(file_issues)

    if json_mode:
        data = {
            "check_id": CHECK_ID,
            "priority": PRIORITY,
            "description": DESCRIPTION,
            "files_scanned": file_count,
            "total_issues": len(all_issues),
            "issues": [
                {
                    "priority": iss.priority,
                    "check_id": iss.check_id,
                    "filepath": iss.filepath,
                    "line": iss.line,
                    "message": iss.message,
                }
                for iss in all_issues
            ],
        }
        print(json.dumps(data, indent=2))
    else:
        print(f"=== {DESCRIPTION} ===")
        print(f"Files scanned: {file_count}")
        print(f"Issues found:  {len(all_issues)}")
        print()

        for iss in all_issues:
            print(f"[{iss.priority}] {iss.check_id} | {iss.filepath}:{iss.line} | {iss.message}")

    return len(all_issues)


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
