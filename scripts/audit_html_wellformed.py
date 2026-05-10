#!/usr/bin/env python3
"""
HTML Well-Formedness Auditor
Checks all book HTML files for structural problems: unclosed tags,
mismatched nesting, orphan closing tags, and div balance issues.

Uses a stack-based HTMLParser approach to detect errors with line numbers.
"""

import os
import sys
from html.parser import HTMLParser
from pathlib import Path
from collections import defaultdict

# Void elements that do not need closing tags
VOID_ELEMENTS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
    "command", "keygen", "menuitem",
})

# Tags we track for nesting validation
TRACKED_TAGS = frozenset({
    "div", "p", "span", "ul", "ol", "li", "details", "summary",
    "section", "pre", "code", "table", "thead", "tbody", "tfoot",
    "tr", "td", "th", "dl", "dt", "dd", "blockquote", "figure",
    "figcaption", "nav", "header", "footer", "main", "article",
    "aside", "form", "fieldset", "legend", "select", "option",
    "textarea", "button", "label", "a", "em", "strong", "small",
    "sub", "sup", "mark", "del", "ins", "abbr", "cite", "dfn",
    "time", "var", "samp", "kbd", "s", "u", "b", "i", "ruby",
    "rt", "rp", "bdi", "bdo", "map", "object", "video", "audio",
    "canvas", "caption", "colgroup", "datalist", "dialog",
    "h1", "h2", "h3", "h4", "h5", "h6", "head", "html", "body",
    "title", "script", "style", "noscript", "template", "slot",
})

# Tags that can be implicitly closed in HTML5 (we still report them but
# categorize separately). For now we treat all tags strictly.


class WellFormednessChecker(HTMLParser):
    """Stack-based HTML parser that detects structural problems."""

    def __init__(self, filename):
        super().__init__(convert_charrefs=False)
        self.filename = filename
        self.stack = []  # list of (tag, attrs_str, line_no)
        self.errors = []  # list of (line_no, message, error_type)
        self.tag_open_counts = defaultdict(int)
        self.tag_close_counts = defaultdict(int)
        self._current_line = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        line = self.getpos()[0]
        self.tag_open_counts[tag] += 1

        if tag in VOID_ELEMENTS:
            return  # void elements, no closing needed

        # Build a short attribute string for error messages
        attr_str = ""
        if attrs:
            parts = []
            for k, v in attrs[:3]:  # first 3 attrs max
                if v is not None:
                    parts.append(f'{k}="{v[:30]}"')
                else:
                    parts.append(k)
            attr_str = " " + " ".join(parts)
            if len(attrs) > 3:
                attr_str += " ..."

        self.stack.append((tag, attr_str, line))

    def handle_endtag(self, tag):
        tag = tag.lower()
        line = self.getpos()[0]
        self.tag_close_counts[tag] += 1

        if tag in VOID_ELEMENTS:
            return

        # Search the stack for a matching open tag
        if not self.stack:
            self.errors.append((
                line,
                f"Orphan closing </{tag}> with no matching open tag",
                "orphan_close"
            ))
            return

        # Check if top of stack matches
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return

        # Look deeper in the stack for a match (mismatched nesting)
        # First, check if this close tag exists anywhere in the stack
        found_idx = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                found_idx = i
                break

        if found_idx is not None:
            # Everything between found_idx+1 and top is unclosed
            unclosed = self.stack[found_idx + 1:]
            for utag, uattr, uline in unclosed:
                self.errors.append((
                    uline,
                    f"Unclosed <{utag}{uattr}> (opened line {uline}, "
                    f"force-closed by </{tag}> at line {line})",
                    "unclosed"
                ))
            # Pop everything from found_idx onwards
            self.stack = self.stack[:found_idx]
        else:
            # No matching open tag at all
            top_tag, top_attr, top_line = self.stack[-1]
            self.errors.append((
                line,
                f"Mismatched close </{tag}>, expected </{top_tag}> "
                f"(opened at line {top_line})",
                "mismatch"
            ))

    def handle_startendtag(self, tag, attrs):
        """Self-closing tags like <br/> or <img/>."""
        tag = tag.lower()
        self.tag_open_counts[tag] += 1
        # These are properly self-closed, no action needed

    def finish(self):
        """Call after feeding all data. Reports any tags still on the stack."""
        for tag, attr_str, line in self.stack:
            self.errors.append((
                line,
                f"Unclosed <{tag}{attr_str}> (opened line {line}, "
                f"never closed by end of file)",
                "unclosed"
            ))

    def get_div_balance(self):
        opens = self.tag_open_counts.get("div", 0)
        closes = self.tag_close_counts.get("div", 0)
        return opens, closes


def check_file(filepath):
    """Check a single HTML file for well-formedness issues."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        return [], (0, 0), str(e)

    checker = WellFormednessChecker(filepath)
    try:
        checker.feed(content)
        checker.finish()
    except Exception as e:
        checker.errors.append((0, f"Parser error: {e}", "parser_error"))

    div_opens, div_closes = checker.get_div_balance()
    return checker.errors, (div_opens, div_closes), None


def collect_html_files(root_dir):
    """Collect all HTML files in the book directories."""
    html_files = []
    # Book content directories
    content_dirs = [
        "front-matter",
        "part-1-foundations",
        "part-2-understanding-llms",
        "part-3-working-with-llms",
        "part-4-training-adapting",
        "part-5-retrieval-conversation",
        "part-6-agentic-ai",
        "part-7-multimodal-applications",
        "part-8-evaluation-production",
        "part-9-safety-strategy",
        "part-10-frontiers",
        "part-11-idea-to-product",
        "appendices",
    ]

    for cdir in content_dirs:
        full_dir = os.path.join(root_dir, cdir)
        if not os.path.isdir(full_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(full_dir):
            for fname in sorted(filenames):
                if fname.endswith(".html"):
                    html_files.append(os.path.join(dirpath, fname))

    # Also check toc.html at root
    toc_path = os.path.join(root_dir, "toc.html")
    if os.path.isfile(toc_path):
        html_files.append(toc_path)

    return sorted(html_files)


def format_report(filepath, root_dir, errors, div_balance):
    """Format the report for a single file."""
    rel_path = os.path.relpath(filepath, root_dir)
    lines = [f"=== {rel_path} ==="]

    # Sort errors by line number
    for line_no, msg, etype in sorted(errors, key=lambda x: x[0]):
        lines.append(f"  Line {line_no}: {msg}")

    div_opens, div_closes = div_balance
    if div_opens != div_closes:
        diff = abs(div_opens - div_closes)
        lines.append(
            f"  DIV balance: {div_opens} opens, {div_closes} closes "
            f"(IMBALANCED by {diff})"
        )
    else:
        lines.append(
            f"  DIV balance: {div_opens} opens, {div_closes} closes (OK)"
        )

    return "\n".join(lines)


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Phase 1: Smoke test on 5 specific files
    smoke_files = [
        "part-4-training-adapting/module-16-distillation-merging/section-16.3.html",
        "part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html",
        "part-1-foundations/module-03-sequence-models-attention/section-3.3.html",
        "part-4-training-adapting/module-16-distillation-merging/section-16.1.html",
        "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html",
    ]

    print("=" * 70)
    print("PHASE 1: SMOKE TEST (5 files)")
    print("=" * 70)
    print()

    phase1_errors = 0
    phase1_files_with_errors = 0

    for rel_file in smoke_files:
        filepath = os.path.join(root_dir, rel_file)
        if not os.path.isfile(filepath):
            print(f"  WARNING: File not found: {rel_file}")
            continue

        errors, div_balance, read_error = check_file(filepath)
        if read_error:
            print(f"  ERROR reading {rel_file}: {read_error}")
            continue

        report = format_report(filepath, root_dir, errors, div_balance)
        print(report)
        print()

        if errors:
            phase1_files_with_errors += 1
            phase1_errors += len(errors)

    print(f"Phase 1 summary: {len(smoke_files)} files checked, "
          f"{phase1_files_with_errors} with errors, "
          f"{phase1_errors} total errors")
    print()

    # Phase 2: Full audit
    print("=" * 70)
    print("PHASE 2: FULL AUDIT")
    print("=" * 70)
    print()

    all_html = collect_html_files(root_dir)
    print(f"Found {len(all_html)} HTML files to check.")
    print()

    total_errors = 0
    files_with_errors = 0
    error_type_counts = defaultdict(int)
    all_reports = []
    files_with_div_imbalance = 0
    error_files_list = []

    for filepath in all_html:
        errors, div_balance, read_error = check_file(filepath)
        if read_error:
            rel = os.path.relpath(filepath, root_dir)
            all_reports.append(f"=== {rel} ===\n  ERROR reading file: {read_error}\n")
            continue

        div_opens, div_closes = div_balance
        has_errors = bool(errors)
        has_div_imbalance = (div_opens != div_closes)

        if has_errors or has_div_imbalance:
            report = format_report(filepath, root_dir, errors, div_balance)
            all_reports.append(report)

            if has_errors:
                files_with_errors += 1
                total_errors += len(errors)
                error_files_list.append(
                    (os.path.relpath(filepath, root_dir), len(errors))
                )
                for _, _, etype in errors:
                    error_type_counts[etype] += 1

            if has_div_imbalance:
                files_with_div_imbalance += 1

    # Print files with errors (summary)
    if error_files_list:
        print("Files with errors:")
        for rel, count in sorted(error_files_list):
            print(f"  {rel}: {count} error(s)")
        print()

    # Print error type breakdown
    if error_type_counts:
        print("Errors by type:")
        type_labels = {
            "unclosed": "Unclosed tags",
            "mismatch": "Mismatched nesting",
            "orphan_close": "Orphan closing tags",
            "parser_error": "Parser errors",
        }
        for etype, count in sorted(error_type_counts.items(),
                                   key=lambda x: -x[1]):
            label = type_labels.get(etype, etype)
            print(f"  {label}: {count}")
        print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total HTML files checked: {len(all_html)}")
    print(f"  Files with tag errors:    {files_with_errors}")
    print(f"  Files with DIV imbalance: {files_with_div_imbalance}")
    print(f"  Total tag errors:         {total_errors}")
    print()

    # Save full report
    report_path = os.path.join(root_dir, "scripts", "html_wellformed_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("HTML Well-Formedness Audit Report\n")
        f.write(f"Generated by: audit_html_wellformed.py\n")
        f.write(f"Total files checked: {len(all_html)}\n")
        f.write(f"Files with tag errors: {files_with_errors}\n")
        f.write(f"Files with DIV imbalance: {files_with_div_imbalance}\n")
        f.write(f"Total tag errors: {total_errors}\n")
        f.write("\n")

        if error_type_counts:
            f.write("Errors by type:\n")
            type_labels = {
                "unclosed": "Unclosed tags",
                "mismatch": "Mismatched nesting",
                "orphan_close": "Orphan closing tags",
                "parser_error": "Parser errors",
            }
            for etype, count in sorted(error_type_counts.items(),
                                       key=lambda x: -x[1]):
                label = type_labels.get(etype, etype)
                f.write(f"  {label}: {count}\n")
            f.write("\n")

        f.write("=" * 70 + "\n")
        f.write("DETAILED FINDINGS\n")
        f.write("=" * 70 + "\n\n")

        if all_reports:
            for report in all_reports:
                f.write(report + "\n\n")
        else:
            f.write("No errors found. All files are well-formed.\n")

    print(f"Full report saved to: {report_path}")


if __name__ == "__main__":
    main()
