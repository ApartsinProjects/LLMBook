"""Check that html2pub.toml and KDP/metadata/metadata.yaml agree on
publication metadata.

html2pub.toml drives the EPUB OPF (what Amazon ingests).
KDP/metadata/metadata.yaml is the documented source of truth for KDP
submission. The publish.py pre-flight checks both files agree, but
that check fires LATE (after build). This audit catches drift earlier.

Fields compared:
  - publication_date  (toml: book.publication_date,  yaml: book.publication_date)
  - edition          (toml: book.edition,            yaml: book.edition)
  - identifier / UUID (toml: book.identifier,        yaml: identifiers.uuid)
  - rights           (toml: book.rights,             yaml: book.rights)
  - language         (toml: book.language,           yaml: book.language)
  - title            (toml: book.title,              yaml: book.title)

Plugin trigger: runs once when the framework visits
KDP/metadata/description.html (any KDP metadata file would do; this one
is guaranteed to exist).
"""
import re
import tomllib
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "METADATA_PARITY"
DESCRIPTION = "html2pub.toml and KDP/metadata/metadata.yaml disagree on a publication field"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])


def _load_yaml_simple(path: Path) -> dict:
    """Hand-rolled minimal YAML reader (avoid the PyYAML dep)."""
    out = {}
    cur_dict = out
    stack = [(0, out)]  # (indent, dict)
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        # Walk back the stack to the right parent
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
        else:
            parent[key] = val
    return out


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]

    rel = str(filepath.relative_to(book_root)).replace("\\", "/").lower()
    if rel != "kdp/metadata/description.html":
        return issues  # only run once, on this trigger file

    toml_path = book_root / "html2pub.toml"
    yaml_path = book_root / "KDP" / "metadata" / "metadata.yaml"
    if not toml_path.exists() or not yaml_path.exists():
        return issues

    try:
        toml_data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except Exception as e:
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                            f"Failed to parse html2pub.toml: {e}"))
        return issues
    try:
        yaml_data = _load_yaml_simple(yaml_path)
    except Exception as e:
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                            f"Failed to parse metadata.yaml: {e}"))
        return issues

    pairs = [
        ("publication_date", toml_data.get("book", {}).get("publication_date"),
         yaml_data.get("book", {}).get("publication_date")),
        ("edition", toml_data.get("book", {}).get("edition"),
         yaml_data.get("book", {}).get("edition")),
        ("identifier", toml_data.get("book", {}).get("identifier"),
         yaml_data.get("identifiers", {}).get("uuid")),
        ("rights", toml_data.get("book", {}).get("rights"),
         yaml_data.get("book", {}).get("rights")),
        ("language", toml_data.get("book", {}).get("language"),
         yaml_data.get("book", {}).get("language")),
        ("title", toml_data.get("book", {}).get("title"),
         yaml_data.get("book", {}).get("title")),
    ]
    for field, t, y in pairs:
        if t is None or y is None:
            continue
        if str(t).strip() != str(y).strip():
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                                f"{field}: html2pub.toml={t!r} but metadata.yaml={y!r}"))
    return issues
