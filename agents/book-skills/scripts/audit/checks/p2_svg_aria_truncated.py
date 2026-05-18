"""Check for SVG aria-label attributes that appear truncated (end mid-sentence)."""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "SVG_ARIA_TRUNCATED"
DESCRIPTION = "SVG aria-label appears truncated (cut off mid-sentence)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

SVG_ARIA_RE = re.compile(
    r'<svg\b[^>]*\baria-label=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def _looks_truncated(label):
    """Heuristic: label is truncated if it ends mid-word or with hanging connectives.

    Tuned to be conservative — only flag clear truncations:
      - Ends with comma + nothing
      - Ends with a stop-word (the, a, of, in, to, for, with, from, by, on, etc.)
      - Last "word" is <= 2 chars and not a known acceptable abbreviation
        (a real word-stem cut like "fol" or single-letter "o" at the end)
    Removed the over-aggressive "long-label ends-lowercase" heuristic that
    falsely flagged correct sentence endings like "parameters" or "storage".
    """
    label = label.strip()
    if not label:
        return False

    # Too short to judge
    if len(label) < 20:
        return False

    # Ends with a common truncation indicator
    last_char = label[-1]
    # Normal endings: period, question mark, closing paren, etc.
    if last_char in '.?!:)]:':
        return False

    # Ends with comma + nothing
    if last_char == ',':
        return True

    # Last "word" check
    words = label.split()
    if not words:
        return False
    trailing = words[-1].lower().strip(",.;:!?)\"'")

    # Stop-word ending
    TRUNCATION_WORDS = {
        "the", "a", "an", "and", "or", "of", "in", "to", "for",
        "with", "from", "by", "on", "at", "as", "is", "are",
        "but", "nor", "so", "yet", "into", "onto", "upon",
    }
    if trailing in TRUNCATION_WORDS:
        return True

    # Mid-word truncation: 1-2 char tail that isn't a known acceptable token
    ACCEPTABLE_SHORT_WORDS = {
        "ai", "ml", "ui", "io", "is", "be", "do", "go", "no", "ok",
        "us", "we", "or", "of", "at", "in", "to", "on", "up", "vm",
        "cli", "css", "csv", "css", "dns", "fp4", "fp8", "fp16", "fp32",
        "gpu", "cpu", "tpu", "nlp", "llm", "api", "ada", "git", "ide",
        "tcp", "udp", "url", "uri", "uuid", "xml", "yml", "rag",
        "qr", "qc", "qa", "qe",  # numeric/marketing
        # Roman numerals (sections, annexes, book parts ending in roman num)
        "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
        "xi", "xii", "xiii", "xiv", "xv",
    }
    if len(trailing) <= 2 and trailing not in ACCEPTABLE_SHORT_WORDS:
        return True

    return False


def run(filepath, html, context):
    issues = []
    for i, line in enumerate(html.split("\n"), 1):
        for m in SVG_ARIA_RE.finditer(line):
            label = m.group(1).strip()
            if _looks_truncated(label):
                display = label[-60:] if len(label) > 60 else label
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, i,
                    f'SVG aria-label appears truncated: "...{display}"',
                ))
    return issues
