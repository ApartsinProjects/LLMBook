"""Enforce KDP submission hard limits that, if violated, REJECT the upload.

KDP rejects submissions where:
  - The book description exceeds 4000 characters (HTML or plain text).
  - Any keyword exceeds 50 characters.
  - More than 7 keywords are supplied.
  - More than 3 BISAC categories are supplied.

These are HARD checks at upload time, not soft suggestions. Catching them
in the local audit pipeline (P0) prevents an upload that comes back
hours later with a vague "submission failed" message.

Motivation: in Edition 16, description.html silently grew to 4450 chars
(450 over the limit) and two keywords grew to 51 and 52 chars (over the
50-char limit) as part of cumulative edits. All 130 other audit plugins
passed. The submission would have been rejected on upload.

Triggered: once, when the framework visits KDP/metadata/description.html
(any KDP metadata file would do; this one is guaranteed to exist).
"""
import re
import tomllib
from collections import namedtuple
from pathlib import Path

PRIORITY = "P0"
CHECK_ID = "KDP_SUBMISSION_LIMITS"
DESCRIPTION = "KDP hard limit violated (description > 4000 chars, keyword > 50 chars, > 7 keywords, > 3 BISAC categories)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

DESC_LIMIT = 4000
KEYWORD_LIMIT = 50
KEYWORDS_MAX = 7
CATEGORIES_MAX = 3


def _load_yaml_simple(path: Path) -> dict:
    """Hand-rolled minimal YAML reader (avoid the PyYAML dep)."""
    out = {}
    stack = [(0, out)]
    cur_list_key = None
    cur_list_indent = -1
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        # List item
        if stripped.startswith("- "):
            if cur_list_key is not None and indent > cur_list_indent:
                parent = stack[-1][1] if stack else out
                if cur_list_key not in parent or not isinstance(parent[cur_list_key], list):
                    parent[cur_list_key] = []
                val = stripped[2:].strip().strip('"').strip("'")
                parent[cur_list_key].append(val)
            continue
        cur_list_key = None
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1] if stack else out
        if ":" not in stripped:
            continue
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if not val:
            parent[key] = {}
            stack.append((indent, parent[key]))
            cur_list_key = key
            cur_list_indent = indent
        else:
            parent[key] = val
    return out


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]

    rel = str(filepath.relative_to(book_root)).replace("\\", "/").lower()
    if rel != "kdp/metadata/description.html":
        return issues  # only run once, on this trigger file

    # --- Check 1: description.html length ---
    desc_html = book_root / "KDP" / "metadata" / "description.html"
    if desc_html.exists():
        n = len(desc_html.read_text(encoding="utf-8"))
        if n > DESC_LIMIT:
            issues.append(Issue(PRIORITY, CHECK_ID, desc_html, 1,
                                f"description.html is {n} chars (KDP limit: {DESC_LIMIT}). "
                                f"Over by {n - DESC_LIMIT} chars. Trim before submitting."))

    # --- Check 2: keywords ---
    yaml_path = book_root / "KDP" / "metadata" / "metadata.yaml"
    if not yaml_path.exists():
        return issues
    try:
        y = _load_yaml_simple(yaml_path)
    except Exception as e:
        issues.append(Issue(PRIORITY, CHECK_ID, yaml_path, 1,
                            f"Failed to parse metadata.yaml: {e}"))
        return issues

    kdp = y.get("kdp", {}) if isinstance(y.get("kdp"), dict) else {}
    keywords = kdp.get("keywords", []) if isinstance(kdp.get("keywords"), list) else []
    if len(keywords) > KEYWORDS_MAX:
        issues.append(Issue(PRIORITY, CHECK_ID, yaml_path, 1,
                            f"{len(keywords)} keywords in metadata.yaml (KDP limit: {KEYWORDS_MAX}). "
                            f"Drop {len(keywords) - KEYWORDS_MAX} before submitting."))
    for i, kw in enumerate(keywords, 1):
        if len(kw) > KEYWORD_LIMIT:
            issues.append(Issue(PRIORITY, CHECK_ID, yaml_path, 1,
                                f"Keyword #{i} is {len(kw)} chars (KDP limit: {KEYWORD_LIMIT}): {kw!r}. "
                                f"Trim by {len(kw) - KEYWORD_LIMIT} chars."))

    # --- Check 3: categories ---
    categories = kdp.get("categories", []) if isinstance(kdp.get("categories"), list) else []
    if len(categories) > CATEGORIES_MAX:
        issues.append(Issue(PRIORITY, CHECK_ID, yaml_path, 1,
                            f"{len(categories)} BISAC categories in metadata.yaml "
                            f"(KDP limit: {CATEGORIES_MAX}). Drop {len(categories) - CATEGORIES_MAX}."))

    return issues
