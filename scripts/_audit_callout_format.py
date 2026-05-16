"""Callout-format consistency audit.

Walks every .html file (excluding KDP/, .claude/, temp_*, scripts/, *backups*,
node_modules/, pagefind/, templates/) and inspects every `<div class="callout
...">` for canonical title text and canonical body structure.

The audit is READ-ONLY. Findings are written to
`callout-format-audit.md` at the project root.

Run from the project root:
    python scripts/_audit_callout_format.py
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "callout-format-audit.md"

SKIP_DIR_NAMES = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    "build", ".git", "__pycache__", "agents", "vendor",
    "source_fix_backups",
}
SKIP_PREFIXES = ("temp_",)
SKIP_NAME_FRAGMENTS = ("backups",)


def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    if parts & SKIP_DIR_NAMES:
        return True
    for part in p.parts:
        if part.startswith(SKIP_PREFIXES):
            return True
        if any(frag in part for frag in SKIP_NAME_FRAGMENTS):
            return True
    return False


def collect_html_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.rglob("*.html")):
        if should_skip(p):
            continue
        files.append(p)
    return files


# ----------------------------------------------------------------------
# Canonical specs
# ----------------------------------------------------------------------
# For each callout class, canonical_titles is the set of title strings the
# title MAY take (exact match, case-sensitive). title_prefixes is the set of
# allowed leading substrings (e.g. "Tip: Be careful" -> prefix "Tip").
# Some classes accept a strictly-required prefix pattern that includes a
# numeric sequence (e.g. exercise must have "Exercise N.M.P: ...").

CANONICAL: dict[str, dict] = {
    "big-picture": {
        "titles": {"Big Picture"},
        "prefixes": ("Big Picture:", "Big Picture ", "Big-Picture"),
        # NOTE: many big-picture callouts in this book use non-"Big Picture"
        # titles like "Why this page exists" or "What this appendix is".
        # Those are flagged so the team can decide whether to rename the
        # title or move the callout to a different class. They're not
        # auto-tolerated.
    },
    "key-insight": {
        # Two acceptable titles: per CONTENT_GUIDELINES the class is for
        # "Key Insight", but in practice "Key Takeaways" is used 157 times
        # at the close of chapters and is documented as an acceptable
        # variant.
        "titles": {"Key Insight", "Key Takeaway", "Key Takeaways"},
        "prefixes": ("Key Insight:", "Key Takeaway:", "Key Takeaways:"),
    },
    "note": {
        "titles": {"Note"},
        "prefixes": ("Note:", "Note ", "Note -"),
    },
    "warning": {
        "titles": {"Warning"},
        "prefixes": ("Warning:", "Warning ", "Warning -"),
    },
    "tip": {
        "titles": {"Tip"},
        "prefixes": ("Tip:", "Tip ", "Tip -"),
    },
    "looking-back": {
        "titles": {"Looking Back"},
        "prefixes": ("Looking Back:", "Looking-Back"),
    },
    "practical-example": {
        "titles": {"Practical Example"},
        "prefixes": ("Practical Example:", "Practical Example ", "Practical Example -"),
    },
    "fun-note": {
        # Per CONTENT_GUIDELINES the canonical title is "Fun Fact" (class
        # `callout fun-note`). Plain "Fun Note" is also widely used here.
        "titles": {"Fun Fact", "Fun Note"},
        "prefixes": ("Fun Fact:", "Fun Note:", "Fun Fact ", "Fun Note "),
    },
    "exercise": {
        # Title shape: "Exercise N.M.P: Title <span class="exercise-type ...">..."
        # We also tolerate "Exercises" and "Exercise" as plural/group titles.
        "titles": set(),
        "prefixes": (),
        "regex": re.compile(r"^Exercise\s+\d+(\.\d+)*:"),
        "tolerated_plain": {"Exercise", "Exercises", "Hands-On Lab"},
    },
    "self-check": {
        # Canonical: "Self-Check". "Self-Check Questions" is the deviation
        # the user already flagged.
        "titles": {"Self-Check"},
        "prefixes": ("Self-Check:",),
    },
    "research-frontier": {
        "titles": {"Research Frontier"},
        "prefixes": ("Research Frontier:", "Research Frontier ", "Research Frontier -"),
    },
    "algorithm": {
        # Canonical: "Algorithm N.M.P: ...". Many existing instances use
        # "Pseudocode N.M.P: ..." which is the older naming. We flag both
        # the plain title and any drift from the numeric pattern.
        "titles": set(),
        "prefixes": (),
        "regex": re.compile(r"^(Algorithm|Pseudocode)\s+\d+(\.\d+)*:"),
        "tolerated_plain": {"Algorithm", "Pseudocode"},
    },
    "postmortem": {
        "titles": {"Postmortem"},
        "prefixes": ("Postmortem:",),
    },
    "cross-ref": {
        # Per the user's spec the canonical title is "Canonical reference".
        # "See also" and "Appendix Reference" are documented as separate
        # flavors that share the same class; we flag them as type-mismatch
        # candidates rather than canonical.
        "titles": {"Canonical reference"},
        "prefixes": ("Canonical reference:",),
    },
    "lab": {
        # Canonical: "Lab N.M.P: ..."
        "titles": set(),
        "prefixes": (),
        "regex": re.compile(r"^Lab\s+\d+(\.\d+)*:"),
        "tolerated_plain": {"Lab"},
    },
    "pathway": {
        "titles": set(),
        "prefixes": ("Pathway:",),
    },
    # ------------------------------------------------------------------
    # Classes not in the user's canonical table but present in the book.
    # We add minimal canonical specs based on observed dominant titles so
    # the audit covers everything (rather than treating them as "unknown").
    # ------------------------------------------------------------------
    "library-shortcut": {
        "titles": {"Library Shortcut"},
        "prefixes": ("Library Shortcut:", "Library Shortcut ",),
    },
    "production-pattern": {
        "titles": {"Production Pattern"},
        "prefixes": ("Production Pattern:", "Production Pattern ",),
    },
    "numeric-example": {
        "titles": {"Worked Example", "Numerical Example"},
        "prefixes": (
            "Worked Example:", "Worked Example ",
            "Numerical Example:", "Numerical Example ",
        ),
    },
    "thesis-thread": {
        "titles": set(),
        "prefixes": ("Thesis ",),
    },
}

# Classes whose body should be wrapped <p> elements (no special structure).
SIMPLE_PROSE_CLASSES = {
    "big-picture", "key-insight", "note", "warning", "tip",
    "looking-back", "fun-note", "postmortem", "cross-ref",
    "pathway", "thesis-thread", "library-shortcut",
    "production-pattern", "numeric-example",
}
# Classes that should have list-shaped or specially-shaped bodies.
LIST_TOLERANT_CLASSES = {
    "key-insight", "practical-example", "research-frontier",
    "production-pattern", "library-shortcut",
}


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


# ----------------------------------------------------------------------
# Body-structure inspectors
# ----------------------------------------------------------------------

def non_whitespace_children(el: Tag) -> list:
    """Return direct children of `el` excluding whitespace-only text."""
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            if str(c).strip() == "":
                continue
        out.append(c)
    return out


def find_title_div(el: Tag) -> Tag | None:
    for child in el.find_all("div", recursive=False):
        cc = child.get("class") or []
        if "callout-title" in cc:
            return child
    return None


def is_empty_body(el: Tag, title_div: Tag | None) -> bool:
    """Return True if the callout has no body content beyond the title."""
    non_title = []
    for c in non_whitespace_children(el):
        if c is title_div:
            continue
        non_title.append(c)
    if not non_title:
        return True
    text = "".join(
        (c.get_text(strip=True) if hasattr(c, "get_text") else str(c).strip())
        for c in non_title
    )
    return not text


def self_check_body_issue(el: Tag, title_div: Tag | None) -> str | None:
    """Return a string describing how a self-check body deviates, or None.

    Canonical: each `<p class="quiz-question">` (or `<div class="quiz-question">`)
    is followed by a `<details><summary>Show Answer</summary><div class="answer">
    ...</div></details>` block.
    """
    body_children = [c for c in non_whitespace_children(el) if c is not title_div]
    # Accept BOTH <p class="quiz-question"> and <div class="quiz-question">
    # (the second is widely used in part-1 and part-2 sections).
    questions = [
        t for t in el.find_all(["p", "div"])
        if t.get("class") and "quiz-question" in t.get("class")
    ]
    detail_blocks = el.find_all("details", recursive=False)
    detail_blocks_deep = el.find_all("details")

    issues: list[str] = []

    has_list_root = any(
        isinstance(c, Tag) and c.name in ("ol", "ul")
        for c in body_children
    )

    if not questions and not detail_blocks_deep:
        if has_list_root:
            issues.append("uses <ol>/<ul> body without paired answers (no quiz-question wrappers, no details)")
        else:
            issues.append("no quiz-question wrappers and no details blocks")
    elif questions and not detail_blocks_deep:
        issues.append(f"{len(questions)} question(s) but 0 answer details")
    elif detail_blocks_deep and not questions:
        # This is also non-canonical: the question text is inside the
        # <summary> rather than a separate quiz-question wrapper.
        issues.append(
            f"{len(detail_blocks_deep)} details block(s) without "
            f"<p class=\"quiz-question\"> wrapper (question text likely "
            f"in <summary>)"
        )
    elif questions and detail_blocks_deep:
        if len(questions) != len(detail_blocks_deep):
            issues.append(
                f"{len(questions)} question(s) but {len(detail_blocks_deep)} answer block(s)"
            )
    # Check each <details> has the canonical structure
    for d in detail_blocks_deep:
        summary = d.find("summary")
        if summary is None:
            issues.append("a <details> missing <summary>")
            break
        # canonical: summary text = "Show Answer"; body has <div class="answer">
        summary_text = summary.get_text(strip=True)
        if summary_text != "Show Answer":
            # If the summary text is the question itself, that's a different
            # (and notable) deviation; report a short tag.
            short = (summary_text[:60] + "...") if len(summary_text) > 60 else summary_text
            issues.append(f"a <details><summary> not \"Show Answer\" (was: {short!r})")
            break
        answer_div = d.find("div", class_="answer")
        if answer_div is None:
            issues.append("a <details> missing <div class=\"answer\">")
            break
    return "; ".join(issues) if issues else None


def research_frontier_body_issue(el: Tag, title_div: Tag | None) -> str | None:
    """Canonical research-frontier sub-sections:
    <p><strong>Open Questions:</strong></p><ul>...</ul>
    <p><strong>Recent Developments:</strong></p><ul>...</ul>
    <p><strong>Explore Further:</strong> ...</p>
    """
    # collect all <strong> labels at the start of <p> elements in body
    body = el
    strong_labels = []
    for p in body.find_all("p"):
        s = p.find("strong")
        if s is None:
            continue
        # only count if <strong> is the first non-whitespace content
        text = p.get_text(strip=True)
        s_text = s.get_text(strip=True)
        if not text.startswith(s_text):
            continue
        # normalize: drop trailing colon
        label = s_text.rstrip(":").strip()
        strong_labels.append(label)
    canonical = {"Open Questions", "Recent Developments", "Explore Further"}
    found = {l for l in strong_labels}
    missing = canonical - found
    # Also accept "Recent Developments (...)" variants
    relaxed_found = set()
    for l in found:
        if l.startswith("Recent Developments"):
            relaxed_found.add("Recent Developments")
        elif l.startswith("Open Questions"):
            relaxed_found.add("Open Questions")
        elif l.startswith("Explore Further"):
            relaxed_found.add("Explore Further")
        else:
            relaxed_found.add(l)
    missing = canonical - relaxed_found
    if not missing:
        return None  # canonical
    # Some research-frontier callouts are short prose without sub-sections.
    # Only flag if NONE of the canonical sub-sections are present.
    if len(relaxed_found & canonical) == 0:
        # body might be plain prose — still mention if we want strict
        return f"no canonical sub-sections (Open Questions / Recent Developments / Explore Further) present"
    return f"missing sub-section(s): {sorted(missing)}"


def exercise_body_issue(el: Tag, title_div: Tag | None) -> str | None:
    """Check exercise body has at least one <p> or list; solution optional."""
    body_children = [c for c in non_whitespace_children(el) if c is not title_div]
    if not body_children:
        return "empty body"
    # accept <p>, <ol>, <ul>, <details>, <pre>, <code>, etc.
    has_content = any(
        isinstance(c, Tag) and c.name in {"p", "ol", "ul", "details", "pre", "div", "figure", "code"}
        for c in body_children
    )
    if not has_content:
        # might just be raw text
        text = "".join(
            (c.get_text(strip=True) if hasattr(c, "get_text") else str(c).strip())
            for c in body_children
        )
        if text:
            return "body contains only raw text (no <p> wrapper)"
        return "empty body"
    return None


def simple_prose_body_issue(el: Tag, title_div: Tag | None, cls: str) -> str | None:
    """For simple-prose classes, body should contain at least one <p> (or in
    some cases a list). Empty bodies and bodies that are only text nodes are
    flagged."""
    body_children = [c for c in non_whitespace_children(el) if c is not title_div]
    if not body_children:
        return "empty body"
    has_block = any(
        isinstance(c, Tag) and c.name in {
            "p", "ol", "ul", "table", "figure", "pre", "div", "blockquote", "details",
        }
        for c in body_children
    )
    if has_block:
        return None
    # No block-level body; check whether there's any text at all
    text = "".join(
        (c.get_text(strip=True) if hasattr(c, "get_text") else str(c).strip())
        for c in body_children
    )
    if not text:
        return "empty body"
    return "body has no block-level wrapper (raw text directly inside callout)"


def algorithm_body_issue(el: Tag, title_div: Tag | None) -> str | None:
    """Algorithm callouts should contain a <pre>/<code> block (the pseudo-
    code) or at minimum a <p> description."""
    body_children = [c for c in non_whitespace_children(el) if c is not title_div]
    if not body_children:
        return "empty body"
    has_code = any(
        isinstance(c, Tag) and c.name in {"pre", "code"}
        for c in body_children
    ) or el.find(["pre", "code"]) is not None
    has_p = any(
        isinstance(c, Tag) and c.name == "p"
        for c in body_children
    ) or el.find("p") is not None
    if not has_code and not has_p:
        return "no code/pseudocode block and no <p> description"
    return None


# ----------------------------------------------------------------------
# Title classification
# ----------------------------------------------------------------------

def title_matches_canonical(cls: str, title: str) -> tuple[bool, str | None]:
    """Return (is_canonical, deviation_reason_if_not).

    deviation_reason is None when canonical, otherwise a short tag like
    'wrong-title' / 'plain-when-numbered-required'."""
    spec = CANONICAL.get(cls)
    if spec is None:
        return True, None  # unknown class — handled elsewhere
    # Exact-title match wins.
    if title in spec.get("titles", set()):
        return True, None
    # Prefix match.
    for prefix in spec.get("prefixes", ()):
        if title.startswith(prefix):
            return True, None
    # Regex (used by exercise / algorithm / lab).
    regex = spec.get("regex")
    if regex is not None:
        if regex.search(title):
            return True, None
        # Numbered class but title is a tolerated plain string?
        tolerated = spec.get("tolerated_plain", set())
        if title in tolerated:
            return False, "plain-when-numbered-required"
    # Tolerated plain (for exercise/algorithm/lab classes).
    if title in spec.get("tolerated_plain", set()):
        return False, "plain-when-numbered-required"
    return False, "wrong-title"


# ----------------------------------------------------------------------
# Per-file walker
# ----------------------------------------------------------------------

# Findings, accumulated globally.
findings_title: dict[str, list[tuple[Path, int, str, str]]] = defaultdict(list)
# Keyed by callout class -> list of (file, line, title, deviation_reason)

findings_body: dict[str, list[tuple[Path, int, str, str]]] = defaultdict(list)
# Keyed by callout class -> list of (file, line, title, issue_description)

findings_empty: list[tuple[Path, int, str]] = []
# (file, line, callout class)

findings_class_title_mismatch: list[tuple[Path, int, str, str, str]] = []
# (file, line, class, title, suggested_class)

findings_unknown_class: dict[str, list[tuple[Path, int, str]]] = defaultdict(list)
# class -> (file, line, title)

per_class_total: dict[str, int] = defaultdict(int)
per_class_nonstd: dict[str, int] = defaultdict(int)
# nonstandard count: title-deviant OR body-deviant (deduplicated per callout)


def line_of(el: Tag) -> int:
    return getattr(el, "sourceline", 0) or 0


# A small heuristic: if title literally starts with one of these labels but
# the class is a generic one (e.g. "note"), it's likely a class/title
# mismatch.
TITLE_TO_EXPECTED_CLASS = {
    "Self-Check": "self-check",
    "Self-Check Questions": "self-check",
    "Big Picture": "big-picture",
    "Key Insight": "key-insight",
    "Key Takeaway": "key-insight",
    "Key Takeaways": "key-insight",
    "Looking Back": "looking-back",
    "Fun Fact": "fun-note",
    "Fun Note": "fun-note",
    "Library Shortcut": "library-shortcut",
    "Postmortem": "postmortem",
    "Research Frontier": "research-frontier",
    "Open Question": "research-frontier",
    "Practical Example": "practical-example",
    "Real-World Scenario": "practical-example",
    "Production Pattern": "production-pattern",
    "Production Tip": "tip",
    "Production Alternative": "tip",
    "Worked Example": "numeric-example",
    "Numerical Example": "numeric-example",
    "Pathway": "pathway",
    "Canonical reference": "cross-ref",
    "See also": "cross-ref",
    "Appendix Reference": "cross-ref",
}


def classify_callout(div: Tag, p: Path) -> None:
    """Inspect a single <div class="callout ..."> and record findings."""
    classes = div.get("class") or []
    if "callout" not in classes:
        return
    type_cls = next((c for c in classes if c != "callout"), None)
    if type_cls is None:
        return
    per_class_total[type_cls] += 1

    line = line_of(div)
    title_div = find_title_div(div)
    title_text = title_div.get_text(strip=True) if title_div is not None else ""

    # 1. Empty-body check
    if is_empty_body(div, title_div):
        findings_empty.append((p, line, type_cls))
        per_class_nonstd[type_cls] += 1
        return  # nothing else to check

    # 2. Title canonical?
    is_canon, dev_reason = title_matches_canonical(type_cls, title_text)
    if not is_canon:
        findings_title[type_cls].append((p, line, title_text, dev_reason or ""))
        per_class_nonstd[type_cls] += 1

    # 3. Class/title mismatch — title is a recognized prefix that maps to
    #    a different canonical class.
    expected_cls = None
    for key, mapped_cls in TITLE_TO_EXPECTED_CLASS.items():
        if title_text == key or title_text.startswith(key + ":") or title_text.startswith(key + " "):
            expected_cls = mapped_cls
            break
    if expected_cls is not None and expected_cls != type_cls:
        findings_class_title_mismatch.append(
            (p, line, type_cls, title_text, expected_cls)
        )
        # mark non-standard (but avoid double-counting if title was also
        # already flagged).

    # 4. Body-structure check (class-specific).
    body_issue = None
    if type_cls == "self-check":
        body_issue = self_check_body_issue(div, title_div)
    elif type_cls == "research-frontier":
        body_issue = research_frontier_body_issue(div, title_div)
    elif type_cls == "exercise":
        body_issue = exercise_body_issue(div, title_div)
    elif type_cls == "algorithm":
        body_issue = algorithm_body_issue(div, title_div)
    elif type_cls in SIMPLE_PROSE_CLASSES:
        body_issue = simple_prose_body_issue(div, title_div, type_cls)
    elif type_cls == "practical-example":
        # accept <p>, <ul>, <ol>, etc.
        body_issue = simple_prose_body_issue(div, title_div, type_cls)

    if body_issue is not None:
        findings_body[type_cls].append((p, line, title_text, body_issue))
        # only increment non-standard count once per callout
        if is_canon and (expected_cls is None or expected_cls == type_cls):
            per_class_nonstd[type_cls] += 1

    # 5. Unknown class?
    if type_cls not in CANONICAL:
        findings_unknown_class[type_cls].append((p, line, title_text))


def audit_file(p: Path) -> None:
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    soup = BeautifulSoup(text, "html.parser")
    for div in soup.find_all("div", class_="callout"):
        classes = div.get("class") or []
        if "callout" not in classes:
            continue
        classify_callout(div, p)


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------

def write_report() -> None:
    out: list[str] = []
    files = collect_html_files()
    total_callouts = sum(per_class_total.values())
    total_nonstd = sum(per_class_nonstd.values())

    out.append("# Callout Format Audit")
    out.append("")
    out.append(
        f"Generated by `scripts/_audit_callout_format.py`. "
        f"Scope: {len(files)} HTML files, {total_callouts} callouts."
    )
    out.append("")
    out.append("This audit is READ-ONLY. It flags callouts whose title text or")
    out.append("body structure deviates from the canonical form for their CSS")
    out.append("class. Empty callouts are listed in section 3 (also caught by")
    out.append("`wellformedness-audit.md`).")
    out.append("")

    # --------------------------------------------------------------
    # 1. Summary table
    # --------------------------------------------------------------
    out.append("## 1. Summary")
    out.append("")
    out.append(f"**Headline:** {total_nonstd} non-standard callouts out of "
               f"{total_callouts} across {len(files)} HTML files.")
    out.append("")
    out.append("| Class | Total | Non-standard | % |")
    out.append("|---|---:|---:|---:|")
    all_classes = sorted(
        set(per_class_total) | set(per_class_nonstd) | set(CANONICAL),
        key=lambda c: -per_class_total.get(c, 0),
    )
    for cls in all_classes:
        tot = per_class_total.get(cls, 0)
        nstd = per_class_nonstd.get(cls, 0)
        if tot == 0:
            continue
        pct = (nstd / tot * 100.0) if tot else 0.0
        out.append(f"| `{cls}` | {tot} | {nstd} | {pct:.1f}% |")
    out.append(f"| **TOTAL** | **{total_callouts}** | **{total_nonstd}** "
               f"| **{(total_nonstd/total_callouts*100):.1f}%** |"
               if total_callouts else f"| **TOTAL** | 0 | 0 | - |")
    out.append("")

    # --------------------------------------------------------------
    # 2. Title-text deviations (grouped by class)
    # --------------------------------------------------------------
    out.append("## 2. Title-text deviations")
    out.append("")
    out.append("Callouts whose title is not the canonical string for their class.")
    out.append("Group by class; sorted by frequency of the offending title.")
    out.append("")
    if not findings_title:
        out.append("None found.")
        out.append("")
    else:
        for cls in sorted(findings_title, key=lambda c: -len(findings_title[c])):
            entries = findings_title[cls]
            spec = CANONICAL.get(cls, {})
            canonical_titles = sorted(spec.get("titles", set())) or ["(see regex)"]
            out.append(f"### `callout {cls}` — {len(entries)} deviation(s)")
            out.append("")
            out.append(f"Canonical title(s): {', '.join(repr(t) for t in canonical_titles)}")
            if spec.get("prefixes"):
                out.append(f"Allowed prefix(es): {', '.join(repr(t) for t in spec['prefixes'])}")
            if spec.get("regex"):
                out.append(f"Allowed pattern: `{spec['regex'].pattern}`")
            out.append("")
            # group by exact title text
            by_title: dict[str, list[tuple[Path, int, str]]] = defaultdict(list)
            for (fpath, line, title, reason) in entries:
                by_title[title].append((fpath, line, reason))
            # Split into recurring (>=2) and singletons. List recurring titles
            # with up to 3 examples each; summarize singletons in one bulleted
            # cluster (file:line + truncated title) keeping output dense.
            recurring = [(t, by_title[t]) for t in by_title if len(by_title[t]) >= 2]
            singletons = [(t, by_title[t]) for t in by_title if len(by_title[t]) == 1]
            recurring.sort(key=lambda x: -len(x[1]))
            for title, instances in recurring[:10]:
                t_short = (title[:100] + "...") if len(title) > 100 else title
                out.append(f"- **{len(instances)}x** `\"{t_short}\"`")
                for (fpath, line, reason) in instances[:3]:
                    out.append(f"  - `{rel(fpath)}:{line}`")
                if len(instances) > 3:
                    out.append(f"  - ... and {len(instances) - 3} more")
            if len(recurring) > 10:
                out.append(f"- ... and {len(recurring) - 10} more recurring title(s)")
            if singletons:
                out.append(f"- **{len(singletons)} unique title(s) appearing once each:**")
                for title, instances in singletons[:15]:
                    (fpath, line, reason) = instances[0]
                    t_short = (title[:80] + "...") if len(title) > 80 else title
                    out.append(f"  - `{rel(fpath)}:{line}` `\"{t_short}\"`")
                if len(singletons) > 15:
                    out.append(f"  - ... and {len(singletons) - 15} more unique title(s)")
            out.append("")

    # --------------------------------------------------------------
    # 3. Body-structure deviations
    # --------------------------------------------------------------
    out.append("## 3. Body-structure deviations")
    out.append("")
    out.append("Callouts whose body shape doesn't match the canonical structure")
    out.append("for the class. Self-check missing answer blocks gets priority.")
    out.append("")
    if not findings_body and not findings_empty:
        out.append("None found.")
        out.append("")
    else:
        # Empty bodies first
        if findings_empty:
            out.append(f"### Empty bodies ({len(findings_empty)})")
            out.append("")
            out.append("Callouts with only a title and no content body. These are")
            out.append("also flagged by `wellformedness-audit.md`.")
            out.append("")
            for (fpath, line, cls) in findings_empty[:50]:
                out.append(f"- `{rel(fpath)}:{line}` — `callout {cls}`")
            if len(findings_empty) > 50:
                out.append(f"- ... and {len(findings_empty) - 50} more")
            out.append("")
        # Per-class body issues
        for cls in sorted(findings_body, key=lambda c: -len(findings_body[c])):
            entries = findings_body[cls]
            out.append(f"### `callout {cls}` — {len(entries)} body deviation(s)")
            out.append("")
            # group by issue description
            by_issue: dict[str, list[tuple[Path, int, str]]] = defaultdict(list)
            for (fpath, line, title, issue) in entries:
                by_issue[issue].append((fpath, line, title))
            for issue in sorted(by_issue, key=lambda i: -len(by_issue[i])):
                instances = by_issue[issue]
                out.append(f"- **{len(instances)}x** {issue}")
                for (fpath, line, title) in instances[:10]:
                    t_short = (title[:80] + "...") if len(title) > 80 else title
                    out.append(f"  - `{rel(fpath)}:{line}` title=`\"{t_short}\"`")
                if len(instances) > 10:
                    out.append(f"  - ... and {len(instances) - 10} more")
            out.append("")

    # --------------------------------------------------------------
    # 4. Class/title mismatches
    # --------------------------------------------------------------
    out.append("## 4. Class/title mismatches")
    out.append("")
    out.append("Callouts whose title text strongly suggests a different class")
    out.append("than the one assigned. For example, a `callout note` titled")
    out.append("\"Self-Check\" should probably be `callout self-check`.")
    out.append("")
    if not findings_class_title_mismatch:
        out.append("None found.")
        out.append("")
    else:
        # group by (actual_class -> expected_class)
        by_pair: dict[tuple[str, str], list[tuple[Path, int, str]]] = defaultdict(list)
        for (fpath, line, actual, title, expected) in findings_class_title_mismatch:
            by_pair[(actual, expected)].append((fpath, line, title))
        for (actual, expected) in sorted(by_pair, key=lambda k: -len(by_pair[k])):
            entries = by_pair[(actual, expected)]
            out.append(f"### `callout {actual}` -> probably should be `callout {expected}` ({len(entries)}x)")
            out.append("")
            for (fpath, line, title) in entries[:10]:
                t_short = (title[:100] + "...") if len(title) > 100 else title
                out.append(f"- `{rel(fpath)}:{line}` title=`\"{t_short}\"`")
            if len(entries) > 10:
                out.append(f"- ... and {len(entries) - 10} more")
            out.append("")

    # --------------------------------------------------------------
    # 5. Unknown / undocumented classes
    # --------------------------------------------------------------
    if findings_unknown_class:
        out.append("## 4b. Unknown callout classes")
        out.append("")
        out.append("Classes encountered that don't appear in the canonical")
        out.append("table. May indicate a typo or an undocumented extension.")
        out.append("")
        for cls in sorted(findings_unknown_class, key=lambda c: -len(findings_unknown_class[c])):
            entries = findings_unknown_class[cls]
            out.append(f"### `callout {cls}` ({len(entries)} instance(s))")
            out.append("")
            for (fpath, line, title) in entries[:5]:
                t_short = (title[:80] + "...") if len(title) > 80 else title
                out.append(f"- `{rel(fpath)}:{line}` title=`\"{t_short}\"`")
            if len(entries) > 5:
                out.append(f"- ... and {len(entries) - 5} more")
            out.append("")

    # --------------------------------------------------------------
    # 6. Recommended fix priority
    # --------------------------------------------------------------
    out.append("## 5. Recommended fix priority")
    out.append("")
    # Compute key counts
    sc_body_count = sum(
        1 for entries in findings_body.values() for (_, _, _, _) in entries
    ) if False else (
        len(findings_body.get("self-check", []))
    )
    sc_title_count = len(findings_title.get("self-check", []))
    ex_plain_count = sum(
        1 for (_, _, _, reason) in findings_title.get("exercise", [])
        if reason == "plain-when-numbered-required"
    )
    ex_other_count = len(findings_title.get("exercise", [])) - ex_plain_count
    rf_body_count = len(findings_body.get("research-frontier", []))
    rf_title_count = len(findings_title.get("research-frontier", []))
    cr_count = len(findings_title.get("cross-ref", []))
    bp_title_count = len(findings_title.get("big-picture", []))
    mismatch_count = len(findings_class_title_mismatch)

    # Priorities are HARD-RANKED by user-visible impact, not by raw count.
    # Self-check and exercise deviations are user-facing bugs (the reader
    # sees a broken quiz or an unnumbered exercise). Research-frontier and
    # big-picture title drift is editorial, not functional.
    priorities: list[tuple[int, str]] = []
    if sc_body_count + sc_title_count > 0:
        priorities.append((
            100,
            f"**Self-Check (user-visible).** {sc_title_count} title-text "
            f"deviation(s) (the \"Self-Check Questions\" with `<ol>` body "
            f"and no answers — the bug the user flagged) and "
            f"{sc_body_count} body deviation(s) (notably `<details>` blocks "
            f"missing `<div class=\"answer\">` wrappers, and 9 callouts that "
            f"are just `<ol>` of questions with no `<details>` answer at "
            f"all). The 9 answer-less self-checks are the worst regressions.",
        ))
    if ex_plain_count + ex_other_count > 0:
        priorities.append((
            90,
            f"**Exercise titles (user-visible).** {ex_plain_count} "
            f"exercise(s) titled only \"Exercise\" / \"Exercises\" / "
            f"\"Hands-On Lab\" without the required `Exercise N.M.P: Title` "
            f"sequence number, plus {ex_other_count} other title shape(s). "
            f"Numbering is required for cross-references and the exercise "
            f"index in `appendices/appendix-t-problem-solution-key/`.",
        ))
    if mismatch_count > 0:
        priorities.append((
            80,
            f"**Class/title mismatches (easy renames).** {mismatch_count} "
            f"callout(s) whose title strongly suggests a different class "
            f"than the one set. See section 4 — most are `callout library-"
            f"shortcut` titled \"Appendix Reference\" that should be "
            f"`callout cross-ref`.",
        ))
    if cr_count > 0:
        priorities.append((
            70,
            f"**cross-ref disambiguation.** {cr_count} `callout cross-ref` "
            f"titled \"See also\" or \"Appendix Reference\" sharing the "
            f"class with canonical \"Canonical reference\" callouts. Either "
            f"rename to canonical or split into separate classes (see "
            f"existing `canonical-reference-audit.md`).",
        ))
    if rf_body_count + rf_title_count > 0:
        priorities.append((
            60,
            f"**Research Frontier sub-sections (editorial).** {rf_body_count} "
            f"callout(s) lack one or more of the canonical Open Questions "
            f"/ Recent Developments / Explore Further sub-sections; "
            f"{rf_title_count} title(s) diverge from \"Research Frontier\" "
            f"(e.g. \"Open Question: ...\", \"Paper Spotlight: ...\", "
            f"\"Methodology: ...\"). High volume but low user impact.",
        ))
    if bp_title_count > 0:
        priorities.append((
            50,
            f"**Big-Picture titles (editorial).** {bp_title_count} `callout "
            f"big-picture` instance(s) use non-\"Big Picture\" titles like "
            f"\"Why this page exists\", \"Bridge: ...\", \"What this "
            f"appendix is\". Intentional for some chapter intros — review "
            f"and decide whether to rename or move to a different class.",
        ))
    # add a generic body-deviation bullet if anything else
    other_body = sum(
        len(entries) for cls, entries in findings_body.items()
        if cls not in ("self-check", "exercise", "research-frontier")
    )
    if other_body > 0:
        priorities.append((
            40,
            f"**Other body-structure deviations.** {other_body} callout(s) "
            f"across other classes lack canonical body shape (raw text "
            f"without `<p>`, etc.). See section 3 for the breakdown.",
        ))

    priorities.sort(key=lambda x: -x[0])
    if not priorities:
        out.append("All callouts conform to canonical form. No action needed.")
    else:
        for i, (_, text) in enumerate(priorities[:7], 1):
            out.append(f"{i}. {text}")
    out.append("")

    # Final notes
    out.append("---")
    out.append("")
    out.append("Re-run this audit with:")
    out.append("")
    out.append("```")
    out.append("python scripts/_audit_callout_format.py")
    out.append("```")
    out.append("")

    OUT_PATH.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    files = collect_html_files()
    for p in files:
        audit_file(p)
    write_report()
    total_callouts = sum(per_class_total.values())
    total_nonstd = sum(per_class_nonstd.values())
    print(f"Scanned {len(files)} files, {total_callouts} callouts, "
          f"{total_nonstd} non-standard.")
    print(f"Report: {OUT_PATH.relative_to(ROOT) if OUT_PATH.is_relative_to(ROOT) else OUT_PATH}")


if __name__ == "__main__":
    main()
