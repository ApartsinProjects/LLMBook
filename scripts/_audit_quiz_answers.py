"""Audit C: Self-check quiz / answer pairing.

For every <div class="quiz-question">...</div> in the book, there should be a
paired <details>...<div class="answer">...</div></details> immediately after
(or within the same self-check callout). Flag mismatches.

Two kinds of orphans:
    quiz-question orphan : a <div class="quiz-question"> with no answer following
                           before the next quiz-question, the end of its enclosing
                           callout, or the end of the file.
    quiz-answer orphan   : a <details> containing <div class="answer"> that has
                           no <div class="quiz-question"> before it within the
                           enclosing self-check / quiz callout.

The audit is read-only and prints a flat list of (file, label) pairs so a human
can fill in missing content. The "label" for a quiz-question orphan is whatever
text is between the opening tag and the closing </div> (trimmed). For an answer
orphan, we report the position and a short snippet.

Alternate Q&A patterns (e.g., the question is encoded in the <summary> rather
than a <div class="quiz-question">) are NOT flagged as orphans because they are
intentional house style in some sections. Specifically, an answer is only flagged
as orphan if it is inside a callout that contains at least one <div class="quiz-question">.

Usage:
    python scripts/_audit_quiz_answers.py            # always read-only
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

EXCLUDE_DIR_NAMES = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", ".book-update",
    "vendor", "scripts", "docs", "styles", ".html2pub_cache", "agents",
    "images", "_concept-figs", "downloads", ".github",
}


def is_excluded(name: str) -> bool:
    if name in EXCLUDE_DIR_NAMES:
        return True
    if name.startswith("temp_"):
        return True
    if "backups" in name:
        return True
    return False


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if not is_excluded(d)]
        for fn in fns:
            if fn.endswith(".html"):
                out.append(Path(dp) / fn)
    return sorted(out)


_TAG_RE = re.compile(r"<[^>]+>")


def strip_tags(s: str) -> str:
    return _TAG_RE.sub("", s).strip()


def find_callouts(text: str) -> list[tuple[int, int, str]]:
    """Find ranges of self-check / quiz callouts.

    Returns list of (start_index, end_index, label).
    end_index is the index immediately after the closing </div> of the callout.
    We look for <div class="callout self-check"> and balance <div>...</div>.
    """
    out: list[tuple[int, int, str]] = []
    # Pattern: a callout div whose class list contains "self-check".
    # (We don't match "quiz" because "quiz-question" would false-match — and the
    # canonical callout class is "callout self-check" anyway.)
    open_re = re.compile(r'<div\s+class="[^"]*\bself-check\b[^"]*"[^>]*>', re.IGNORECASE)
    div_open_re = re.compile(r"<div\b[^>]*>", re.IGNORECASE)
    div_close_re = re.compile(r"</div\s*>", re.IGNORECASE)
    for m in open_re.finditer(text):
        start = m.start()
        # Walk forward to find the matching </div> by counting opens/closes.
        depth = 1
        pos = m.end()
        end = None
        while pos < len(text):
            no = div_open_re.search(text, pos)
            nc = div_close_re.search(text, pos)
            if nc is None:
                break
            if no is not None and no.start() < nc.start():
                depth += 1
                pos = no.end()
            else:
                depth -= 1
                pos = nc.end()
                if depth == 0:
                    end = pos
                    break
        if end is None:
            end = len(text)
        out.append((start, end, "self-check"))
    return out


_QUIZ_Q_RE = re.compile(
    r'<div\s+class="quiz-question"[^>]*>(?P<inner>.*?)</div>',
    re.DOTALL | re.IGNORECASE,
)
_DETAILS_RE = re.compile(r"<details\b[^>]*>(?P<inner>.*?)</details\s*>", re.DOTALL | re.IGNORECASE)
_ANSWER_DIV_RE = re.compile(r'<div\s+class="answer"[^>]*>', re.IGNORECASE)


def audit_file(text: str) -> tuple[list[str], list[str]]:
    """Return (question_orphans, answer_orphans) labels for one file."""
    q_orphans: list[str] = []
    a_orphans: list[str] = []

    callouts = find_callouts(text)
    # A question/answer pairing is only considered inside a callout. We require
    # questions to live in a self-check / quiz callout because that's the
    # canonical structure.
    for c_start, c_end, _label in callouts:
        block = text[c_start:c_end]
        # Find all positions of quiz-questions and details (containing div.answer) inside the block.
        q_positions: list[tuple[int, str]] = []
        for m in _QUIZ_Q_RE.finditer(block):
            label = strip_tags(m.group("inner"))[:200]
            q_positions.append((m.start(), label))
        a_positions: list[int] = []
        for m in _DETAILS_RE.finditer(block):
            if _ANSWER_DIV_RE.search(m.group("inner")):
                a_positions.append(m.start())

        if not q_positions and not a_positions:
            continue

        # Pair greedily: for each quiz-question, the next answer at or after its
        # position counts as its answer (as long as that answer is before the
        # next quiz-question).
        used_answers: set[int] = set()
        q_index = 0
        for q_idx, (q_pos, q_label) in enumerate(q_positions):
            next_q_pos = q_positions[q_idx + 1][0] if q_idx + 1 < len(q_positions) else c_end
            # Find first unused answer in [q_pos, next_q_pos).
            paired = False
            for a_pos in a_positions:
                if a_pos in used_answers:
                    continue
                if q_pos <= a_pos < next_q_pos:
                    used_answers.add(a_pos)
                    paired = True
                    break
            if not paired:
                q_orphans.append(q_label or "(empty)")

        # Any unused answers in this block are orphan answers BUT only if the
        # block also has at least one quiz-question (canonical pattern). If the
        # callout has no quiz-questions, it's the alternate <summary>-only
        # pattern and we don't flag it as broken. We do still surface a count
        # at the file level via the second return value of this function:
        # answer_orphans is the canonical-pattern orphan, and we report the
        # alternate-pattern count separately.
        if q_positions:
            for a_pos in a_positions:
                if a_pos not in used_answers:
                    snippet = block[a_pos:a_pos + 120].replace("\n", " ")
                    a_orphans.append(strip_tags(snippet)[:120])
    return q_orphans, a_orphans


def count_alternate_pattern(text: str) -> int:
    """Count answers in self-check callouts that use the <summary>-only pattern.

    Surfaced separately in the report so the user can see how many answers do
    not have a paired <div class="quiz-question"> tag (but ARE part of a valid
    alternate pattern where the question lives in the <summary>).
    """
    count = 0
    open_re = re.compile(r'<div\s+class="[^"]*\bself-check\b[^"]*"[^>]*>', re.IGNORECASE)
    div_open_re = re.compile(r"<div\b[^>]*>", re.IGNORECASE)
    div_close_re = re.compile(r"</div\s*>", re.IGNORECASE)
    for m in open_re.finditer(text):
        start = m.start()
        depth = 1
        pos = m.end()
        end = None
        while pos < len(text):
            no = div_open_re.search(text, pos)
            nc = div_close_re.search(text, pos)
            if nc is None:
                break
            if no is not None and no.start() < nc.start():
                depth += 1
                pos = no.end()
            else:
                depth -= 1
                pos = nc.end()
                if depth == 0:
                    end = pos
                    break
        if end is None:
            end = len(text)
        block = text[start:end]
        if 'class="quiz-question"' in block:
            continue
        # No quiz-question in this self-check: count its answers.
        for _ in _DETAILS_RE.finditer(block):
            pass
        count += len(_ANSWER_DIV_RE.findall(block))
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="(no-op; audit is read-only)")
    args = parser.parse_args()
    _ = args  # silence unused

    files = iter_html_files()
    total_q_orphans = 0
    total_a_orphans = 0
    total_alt_pattern_answers = 0
    q_orphan_rows: list[tuple[str, str]] = []
    a_orphan_rows: list[tuple[str, str]] = []
    files_scanned = 0
    files_with_quiz = 0

    for f in files:
        text = f.read_text(encoding="utf-8")
        files_scanned += 1
        if 'quiz-question' not in text and 'class="answer"' not in text:
            continue
        if 'quiz-question' in text:
            files_with_quiz += 1
        q_orphans, a_orphans = audit_file(text)
        total_alt_pattern_answers += count_alternate_pattern(text)
        rel = f.relative_to(ROOT).as_posix()
        for ql in q_orphans:
            q_orphan_rows.append((rel, ql))
        for al in a_orphans:
            a_orphan_rows.append((rel, al))
        total_q_orphans += len(q_orphans)
        total_a_orphans += len(a_orphans)

    print("[READ-ONLY] Audit C: quiz-question / answer pairing")
    print(f"  Files scanned:                  {files_scanned}")
    print(f"  Files with quiz:                {files_with_quiz}")
    print(f"  Quiz-question orphans:          {total_q_orphans}")
    print(f"  Quiz-answer orphans:            {total_a_orphans}")
    print(f"  Alternate-pattern <summary> Qs: {total_alt_pattern_answers}  (informational; not flagged)")
    if q_orphan_rows:
        print("\nQuiz-question orphans (no paired answer):")
        for rel, q in q_orphan_rows:
            print(f"  {rel}")
            print(f"    Q: {q}")
    if a_orphan_rows:
        print("\nQuiz-answer orphans (answer with no question in same callout):")
        for rel, a in a_orphan_rows:
            print(f"  {rel}")
            print(f"    A: {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
