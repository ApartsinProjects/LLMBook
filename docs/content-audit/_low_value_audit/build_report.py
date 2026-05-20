"""Build the final markdown report from the classified code blocks."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from collections import Counter

OUT = Path("E:/Projects/BookBlogsHome/LLMBook/docs/content-audit/LOW_VALUE_CODE_FRAGMENTS.md")
JSONL = Path(__file__).parent / "code_blocks_classified.jsonl"


def short_path(p: str) -> str:
    """Return the path relative to LLMBook root."""
    root = "E:/Projects/BookBlogsHome/LLMBook/"
    return p[len(root):] if p.startswith(root) else p


def short_code(code: str, max_lines: int = 6, max_chars: int = 80) -> str:
    lines = []
    for ln in code.splitlines()[:max_lines]:
        if len(ln) > max_chars:
            ln = ln[:max_chars - 3] + "..."
        lines.append(ln)
    if len(code.splitlines()) > max_lines:
        lines.append(f"... ({len(code.splitlines()) - max_lines} more lines)")
    return "\n".join(lines)


def main():
    blocks = [json.loads(l) for l in JSONL.open(encoding="utf-8")]
    total = len(blocks)
    python_blocks = [b for b in blocks if b["category"] != "NON_PYTHON"]
    counts = Counter(b["category"] for b in blocks)

    candidates = [b for b in blocks if b["category"] in ("DROP", "SIMPLIFY-TO-TABLE", "CONVERT-TO-DIAGRAM")]
    candidates.sort(key=lambda b: -b["severity"])

    # Breakdown by part
    part_counts = Counter()
    for b in candidates:
        path = short_path(b["file"])
        m = re.match(r"(part-\d+|appendices)", path)
        part = m.group(1) if m else "other"
        part_counts[part] += 1

    # Categorize candidates by recommendation
    drop_count = sum(1 for b in candidates if b["category"] == "DROP")
    simp_count = sum(1 for b in candidates if b["category"] == "SIMPLIFY-TO-TABLE")
    conv_count = sum(1 for b in candidates if b["category"] == "CONVERT-TO-DIAGRAM")

    out = []
    out.append("# Low-Value Code Fragments Audit (v2.0)")
    out.append("")
    out.append("Read-only scouting pass over every `<pre><code>` block in every "
               "`section-*.html` file. Goal: surface code blocks that re-state prose, "
               "encode taxonomies, or define data shells without doing the interesting "
               "work, and recommend a smaller HTML alternative (table, blockquote, "
               "diagram, prose).")
    out.append("")
    out.append("**No HTML files were edited.** This document is a remediation backlog.")
    out.append("")
    out.append("## Executive Summary")
    out.append("")
    out.append(f"- **Total `<pre><code>` blocks scanned:** {total}")
    out.append(f"- **Python-tagged blocks:** {len(python_blocks)}")
    out.append(f"- **Non-Python blocks (bash, yaml, json, etc., excluded from scope):** {counts.get('NON_PYTHON', 0)}")
    out.append("")
    out.append("| Category | Count | % of python blocks |")
    out.append("| --- | ---:| ---:|")
    out.append(f"| **DROP** | {counts.get('DROP', 0)} | {counts.get('DROP', 0) / len(python_blocks) * 100:.1f}% |")
    out.append(f"| **SIMPLIFY-TO-TABLE** | {counts.get('SIMPLIFY-TO-TABLE', 0)} | {counts.get('SIMPLIFY-TO-TABLE', 0) / len(python_blocks) * 100:.1f}% |")
    out.append(f"| **CONVERT-TO-DIAGRAM** | {counts.get('CONVERT-TO-DIAGRAM', 0)} | {counts.get('CONVERT-TO-DIAGRAM', 0) / len(python_blocks) * 100:.1f}% |")
    out.append(f"| **KEEP** | {counts.get('KEEP', 0)} | {counts.get('KEEP', 0) / len(python_blocks) * 100:.1f}% |")
    out.append("")
    out.append("**Distribution by part (DROP/SIMPLIFY/CONVERT candidates only):**")
    out.append("")
    out.append("| Part | Candidates |")
    out.append("| --- | ---:|")
    for part, n in sorted(part_counts.items(), key=lambda kv: -kv[1]):
        out.append(f"| `{part}` | {n} |")
    out.append("")
    out.append("**Methodology.** A Python classifier parses every block, strips Pygments "
               "spans, and runs a battery of conservative heuristics. KEEP is the default; "
               "the classifier only flags blocks that satisfy at least one explicit "
               "anti-pattern (data-class-only with the class never re-used, comment-only "
               "pseudocode, triple-quoted string masquerading as code, YAML mis-tagged as "
               "Python, etc.). The scripts that produced this audit live in "
               "`docs/content-audit/_low_value_audit/`.")
    out.append("")
    out.append("## Top 30 DROP / SIMPLIFY / CONVERT Candidates")
    out.append("")
    out.append("Ranked by severity (audit score combining size, kv-ratio, comment ratio, "
               "and lack of library/method/algorithm signal). Code excerpts are truncated; "
               "the file + line column points to the exact `<pre>` start for review.")
    out.append("")
    for i, b in enumerate(candidates[:30], 1):
        rel = short_path(b["file"])
        out.append(f"### {i}. `{rel}` line {b['line_no']}")
        out.append("")
        out.append(f"- **Recommendation:** **{b['category']}**  (severity {b['severity']:.0f})")
        out.append(f"- **Why:** {b['reason']}")
        recommendation_text = recommendation_for(b)
        out.append(f"- **Replacement:** {recommendation_text}")
        out.append("")
        out.append("```python")
        out.append(short_code(b["code"], max_lines=8))
        out.append("```")
        out.append("")

    out.append("## Patterns Observed")
    out.append("")
    out.append(write_patterns(candidates))
    out.append("")
    out.append("## Risk Notes")
    out.append("")
    out.append(write_risks(candidates))
    out.append("")
    out.append("## Methodology Notes and Reproduction")
    out.append("")
    out.append("The classifier and extractor live in `docs/content-audit/_low_value_audit/`:")
    out.append("")
    out.append("- `extract_blocks.py` — walks every `section-*.html`, strips Pygments tags, "
               "extracts code + 500 char surrounding context, dumps JSONL.")
    out.append("- `classify.py` — applies the hard-KEEP rules first, then DROP / SIMPLIFY / "
               "CONVERT rules. Conservative by design: when in doubt, the block is KEEP.")
    out.append("- `code_blocks_classified.jsonl` — full per-block output with reason and "
               "severity.")
    out.append("")
    out.append("To reproduce: re-run `extract_blocks.py` then `classify.py`. The first "
               "step depends on `section_files.txt` (the list of section files to scan).")
    out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote report to {OUT}")
    print(f"  {drop_count} DROP, {simp_count} SIMPLIFY, {conv_count} CONVERT, "
          f"{counts.get('KEEP', 0)} KEEP")


def recommendation_for(b: dict) -> str:
    code = b["code"]
    cat = b["category"]
    if "Pure data-class" in b["reason"]:
        return ("Replace with an HTML `<table>` of `field | type | description`. Keep the "
                "field names visible but drop the Python ceremony.")
    if "config/dict literal" in b["reason"].lower():
        return ("Replace with an HTML `<table>` of `key | value | meaning`. The Python "
                "syntax adds no information here.")
    if "YAML/K8s config" in b["reason"]:
        return ("Re-tag the `<pre><code>` class as `lang-yaml` (so Pygments highlights "
                "correctly) and consider replacing each block with a `<table>` of "
                "`field | value` for the most critical keys, leaving the full manifest "
                "in a collapsible details disclosure.")
    if "Comment-only" in b["reason"]:
        return ("Drop the code block; convert the bullet points into a numbered list or "
                "a shell snippet (`<pre><code class=\"lang-bash\">`). Comments are not "
                "code.")
    if "string-literal" in b["reason"].lower():
        return ("Replace with `<pre class=\"prompt-template\">...</pre>` or a "
                "`<blockquote>` so the reader sees the template as text, not as Python.")
    if "Math formula" in b["reason"]:
        return ("Render with KaTeX/MathJax inline math. The current rendering shows raw "
                "ASCII operators which is jarring in a technical book.")
    if "TODO stub" in b["reason"]:
        return ("Inline the TODO into the exercise prose. A one-line code block adds "
                "scrollbar weight without conveying structure.")
    if "Tiny block ending" in b["reason"]:
        return ("Replace the `print()` lines with a two-row HTML table: row 1 lists the "
                "expression, row 2 lists the resulting value. The Python ceremony is not "
                "the lesson here.")
    return "See **reason** above; consider a smaller HTML primitive."


def write_patterns(candidates: list[dict]) -> str:
    pat_lines = []
    pat_lines.append("Five recurring anti-patterns surfaced. Each is illustrated with one "
                     "real example from the candidate list.")
    pat_lines.append("")
    pat_lines.append("### Pattern 1: Pure prompt template assigned to a variable")
    pat_lines.append("")
    pat_lines.append("A multi-line triple-quoted string assigned to `SYSTEM_PROMPT` (or "
                     "`template`, `SAYCAN_PROMPT`, etc.) and then never used in the same "
                     "block. The reader has to parse Python triple-string syntax around "
                     "what is actually just prose. Common in chapters 1, 12, and 24.")
    pat_lines.append("")
    pat_lines.append("**Example:** ChatML / Llama-3 chat templates in `section-1.7a.html` "
                     "(lines 148, 178) — the *content* is the special-token sequence, not "
                     "the `template = \"\"\"...\"\"\"; print(template)` plumbing.")
    pat_lines.append("")
    pat_lines.append("**Remediation:** Replace with `<pre class=\"prompt-template\">` "
                     "containing only the template text. Reader sees the structure without "
                     "the assignment ceremony.")
    pat_lines.append("")
    pat_lines.append("### Pattern 2: Comment-only \"pseudocode\" inside a Python code block")
    pat_lines.append("")
    pat_lines.append("A `<pre><code class=\"lang-python\">` block whose lines are all `#` "
                     "comments. Frequently shell commands the author wanted in a code "
                     "box for visual styling, or a numbered list of exercise steps. The "
                     "Python class is wrong because the Python parser would skip every "
                     "line.")
    pat_lines.append("")
    pat_lines.append("**Example:** `section-47.2.html` line 196 — six lines of `# pip "
                     "install garak\\n# garak --model_type openai ...`. Should be tagged "
                     "`lang-bash` (or a shell snippet) and the # marks dropped.")
    pat_lines.append("")
    pat_lines.append("**Remediation:** Re-tag as `lang-bash` (or as `lang-text` for "
                     "outlines) and remove the comment hashes that exist only to make "
                     "the lines look like Python.")
    pat_lines.append("")
    pat_lines.append("### Pattern 3: YAML / Kubernetes manifest mis-tagged as Python")
    pat_lines.append("")
    pat_lines.append("Container / orchestration YAML rendered inside `<pre><code "
                     "class=\"lang-python\">`. The Pygments lexer attempts Python "
                     "highlighting on `apiVersion: kueue.x-k8s.io/v1beta1` and produces "
                     "visually noisy output. The block is also leaking indentation in the "
                     "extracted text (YAML structure looks flat after our strip).")
    pat_lines.append("")
    pat_lines.append("**Example:** All three K8s blocks in "
                     "`part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.3.html` "
                     "and `section-65.5.html`.")
    pat_lines.append("")
    pat_lines.append("**Remediation:** Re-tag as `lang-yaml`. Pygments will then "
                     "highlight keys and values appropriately and indentation will be "
                     "preserved.")
    pat_lines.append("")
    pat_lines.append("### Pattern 4: TODO / placeholder stub as its own code block")
    pat_lines.append("")
    pat_lines.append("A `<pre>` containing just `# TODO: implement X` or two lines of "
                     "exercise instructions. The visual weight of the code box is "
                     "disproportionate to the content. Common in exercises in modules "
                     "27 and 29.")
    pat_lines.append("")
    pat_lines.append("**Example:** `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` "
                     "line 210 — `# TODO: Define tool schemas ...` on one line.")
    pat_lines.append("")
    pat_lines.append("**Remediation:** Fold the TODO into the exercise prose as a `<li>` "
                     "or `<ol>` item. Reserve code blocks for content the reader will "
                     "actually run or read line by line.")
    pat_lines.append("")
    pat_lines.append("### Pattern 5: Math formula written with ASCII operators in a code block")
    pat_lines.append("")
    pat_lines.append("A one-line block containing `p_theta(a_{1:H} | I, l) = "
                     "prod_{t=1..H} p_theta(...)` rendered as Python source. The reader "
                     "sees raw `_`, `{`, and `|` instead of formatted math.")
    pat_lines.append("")
    pat_lines.append("**Example:** `section-24.1.html` line 59, `section-24.4.html` line "
                     "113, `section-24.7.html` line 60 (all in `part-5-multimodal-llms/"
                     "module-24-vla-models`).")
    pat_lines.append("")
    pat_lines.append("**Remediation:** Render with KaTeX (the rest of the book uses it). "
                     "Inline math goes in `\\(...\\)`, display math in `\\[...\\]`.")
    pat_lines.append("")
    return "\n".join(pat_lines)


def write_risks(candidates: list[dict]) -> str:
    lines = []
    lines.append("Most candidates are clear-cut. A small number are contestable; flagged "
                 "below so a human reviewer can override the recommendation.")
    lines.append("")
    lines.append("1. **DNA tokenization (section-75.4.html:217, SIMPLIFY-TO-TABLE).** The "
                 "block prints three token counts (1200 vs 1195 vs 199) computed from a "
                 "list comprehension. A pure table would lose the *derivation* (the step "
                 "size of 6 vs the overlap of 1) that the list comprehension makes "
                 "visible. **Risk:** demoting to a table erases the pedagogical content. "
                 "**Suggested action:** leave as code, but add a one-row caption table "
                 "comparing the three strategies.")
    lines.append("")
    lines.append("2. **Databricks widgets (section-19.1.html:233, SIMPLIFY-TO-TABLE).** "
                 "Uses `dbutils.widgets`, which IS a real (Databricks) library, but "
                 "the classifier missed it because `dbutils` is not in the LIB_HANDLE "
                 "set. The block is genuinely showing how to wire UI widgets to "
                 "parameter values — KEEP is probably the right call.")
    lines.append("")
    lines.append("3. **Few-shot classification example (section-6.7.html:75, DROP).** "
                 "The triple-quoted prompt IS the pedagogical artifact (few-shot prompt "
                 "structure). DROP-to-blockquote is correct, but the *caption* of "
                 "the existing code block (\"Code Fragment 6.7.1\") will need to be "
                 "preserved in any replacement.")
    lines.append("")
    lines.append("4. **TODO stubs (10 candidates across modules 27 and 29).** These "
                 "are *intentional* hole-fillers for exercises that the reader is meant "
                 "to fill in. Flagging them as DROP is debatable: the code-block framing "
                 "signals \"this is where your code goes.\" **Alternative:** keep the "
                 "code blocks but change the wrapper to `<pre class=\"exercise-stub\">` "
                 "or similar, so the visual signal is preserved but they are not parsed "
                 "as production code samples.")
    lines.append("")
    lines.append("5. **`.env` file (section-14.1.html:179, DROP).** Showing the *shape* "
                 "of a `.env` file is genuinely useful for a reader who has never seen "
                 "one. Replacing with a table loses the visual cue that this is a "
                 "plain-text dotenv file. **Alternative:** keep the block but re-tag as "
                 "`lang-bash` or `lang-dotenv` so it does not get parsed as Python.")
    lines.append("")
    lines.append("6. **All four \"comment-only\" blocks that show CLI invocations** "
                 "(garak, accelerate config, evals, pagefind, vLLM) could legitimately "
                 "be re-tagged as `lang-bash` without dropping anything. The DROP "
                 "recommendation here is really \"drop the wrong lang class\" rather "
                 "than \"drop the content.\"")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
