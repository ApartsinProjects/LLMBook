"""Detect the same Figure X.Y.Z label used in MORE than one section file.

Pattern (BAD):
  Section 31.2a has Figure 31.2.1 (HNSW)
  Section 31.2b also has Figure 31.2.1 (HNSW, duplicate)

Two copies of the same figure number across sections create a broken
cross-reference: "see Figure 31.2.1" is ambiguous.

This is a P1 because it breaks the figure-numbering invariant.

Detection: scan every section file for "Figure X.Y.Z:" captions; record
{label -> [files]}. Flag labels with >1 file.
"""
import re
from collections import defaultdict, namedtuple

PRIORITY = "P1"
CHECK_ID = "DUPLICATE_FIGURE_ACROSS_SECTIONS"
DESCRIPTION = "Same Figure label used in multiple section files"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

FIG_RE = re.compile(
    # Negative lookahead `(?!\.\d)` prevents matching "Figure 20.0.1" as a
    # prefix of "Figure 20.0.1.1". Optional letter suffix allowed.
    r'<figcaption[^>]*>(?:<[^>]+>)?\s*<strong>\s*Figure\s+(\d+\.\d+\.\d+[a-z]?)(?!\.\d)(?!\d)',
    re.IGNORECASE,
)


def run(filepath, html, context):
    """This is a per-file check but cross-file. We accumulate state in
    context['_dup_fig_state']; the harness runs run() for every file in
    order, so we can spot duplicates only at the end. Workaround: emit
    issues from the SECOND occurrence onward.
    """
    issues = []
    if not filepath.name.startswith('section-'):
        return issues

    state = context.setdefault('_dup_fig_state', defaultdict(list))
    for m in FIG_RE.finditer(html):
        label = m.group(1)
        rel = str(filepath).replace('\\', '/')
        line = html[:m.start()].count('\n') + 1
        prior_files = [p for p in state[label] if p[0] != rel]
        if prior_files:
            other_file = prior_files[-1][0]
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'Figure {label} also appears in {other_file} (duplicate across sections)'
            ))
        state[label].append((rel, line))
    return issues
