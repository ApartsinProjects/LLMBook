"""Detect Big Picture callouts where the first paragraph is mostly `<strong>`.

User feedback (section-23.1): the entire lead sentence was wrapped in
`<strong>`, producing visually heavy paragraphs that hurt readability.

Canonical Big Picture uses bold sparingly for key terms only. Flag any
big-picture paragraph where >40% of the words are inside `<strong>`.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "BIG_PICTURE_EXCESS_BOLD"
DESCRIPTION = "Big Picture callout paragraph is mostly <strong>; reserve bold for key terms"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

BIG_PICTURE_RE = re.compile(
    r'<div\s+class="callout\s+big-picture"[^>]*>([\s\S]*?)</div>\s*(?=<div|<h[1-6]|<nav|<details|<section)',
    re.IGNORECASE,
)
P_RE = re.compile(r'<p[^>]*>([\s\S]*?)</p>', re.IGNORECASE)
STRONG_RE = re.compile(r'<strong[^>]*>([\s\S]*?)</strong>', re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def _word_count(text):
    return len(re.findall(r'\w+', text))


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    for m in BIG_PICTURE_RE.finditer(html):
        body = m.group(1)
        for pm in P_RE.finditer(body):
            para = pm.group(1)
            plain = TAG_RE.sub('', para)
            total_words = _word_count(plain)
            if total_words < 20:
                continue
            bold_words = sum(
                _word_count(TAG_RE.sub('', sm.group(1)))
                for sm in STRONG_RE.finditer(para)
            )
            if bold_words / total_words > 0.4:
                pct = int(bold_words / total_words * 100)
                line = _line(html, m.start())
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'Big Picture paragraph is {pct}% bold ({bold_words}/{total_words} words); reserve <strong> for key terms only',
                ))
                break  # one issue per big-picture is enough
    return issues
