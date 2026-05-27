"""
Pedagogy-completeness audit for the LLMBook.

For each named technique/model/algorithm in the book, score 0-4 on:
  1. Architecture diagram presence
  2. Inner workings (math or pseudocode)
  3. Code example
  4. Worked / numerical example

A "technique" is detected as the title of an <h3> (sub-section). Each h3
defines a "section block" that runs from that h3 to the next h2 or h3.
The block is scored on the four dimensions, then the technique-name
is paired with the score.

Output:
  - Per-chapter summary (median score, top-5 most-deficient)
  - Global ranked list of (technique, section, score) ascending by score
  - Concrete "needs work" list (techniques with score <= 1)
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser


# ------------- Section extraction -------------

class SectionExtractor(HTMLParser):
    """Find <h2> and <h3> blocks. Each block is identified by its title
    (text inside the heading) and the raw HTML inside it (until the next
    heading at the same or higher level)."""

    def __init__(self):
        super().__init__()
        self.headings = []  # list of {tag, title, start_offset}
        self.current_title_parts = []
        self.capturing_heading = None
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        if tag in ("h2", "h3"):
            self.capturing_heading = tag
            self.current_title_parts = []

    def handle_endtag(self, tag):
        if tag == self.capturing_heading:
            title = " ".join(self.current_title_parts).strip()
            self.headings.append({"tag": tag, "title": title,
                                  "offset": self.getpos()})
            self.capturing_heading = None
            self.current_title_parts = []

    def handle_data(self, data):
        if self.capturing_heading is not None:
            self.current_title_parts.append(data)


def split_into_section_blocks(html: str) -> list[dict]:
    """Return a list of {title, html, level} where each block is the HTML
    between one heading (h2 or h3) and the next."""
    # Find all headings via regex (simpler than HTMLParser for this)
    heading_pattern = re.compile(r'<(h[23])\b[^>]*>(.*?)</\1>',
                                  re.DOTALL | re.IGNORECASE)
    matches = list(heading_pattern.finditer(html))
    blocks = []
    for i, m in enumerate(matches):
        tag = m.group(1).lower()
        # Strip inner HTML from heading title
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        title = re.sub(r'\s+', ' ', title)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        body = html[start:end]
        blocks.append({"title": title, "html": body, "level": tag})
    return blocks


# ------------- Per-dimension detectors -------------

FIG_PATTERNS = [
    re.compile(r'<figure\b', re.IGNORECASE),
    re.compile(r'<svg\b', re.IGNORECASE),
    re.compile(r'<div\s+class="[^"]*diagram-container[^"]*"', re.IGNORECASE),
    re.compile(r'<div\s+class="[^"]*illustration[^"]*"', re.IGNORECASE),
]

MATH_PATTERNS = [
    re.compile(r'\$\$[^$]+\$\$', re.DOTALL),  # display math
    re.compile(r'\$[^$\n]{2,}\$'),  # inline math (at least 2 chars)
]

CODE_PATTERNS = [
    re.compile(r'<pre[^>]*><code[^>]*class="[^"]*language-python', re.IGNORECASE),
    re.compile(r'<pre[^>]*><code[^>]*class="[^"]*language-(?:bash|json|yaml|cuda|cpp|rust)', re.IGNORECASE),
]

EXAMPLE_CALLOUT_PATTERN = re.compile(
    r'<div\s+class="[^"]*callout\s+(practical-example|numeric-example|key-insight|algorithm)[^"]*"',
    re.IGNORECASE
)


def score_block(body: str) -> dict:
    """Return {has_figure, has_math, has_code, has_example}."""
    has_figure = any(p.search(body) for p in FIG_PATTERNS)
    has_math = any(p.search(body) for p in MATH_PATTERNS)
    has_code = any(p.search(body) for p in CODE_PATTERNS)
    has_example = bool(EXAMPLE_CALLOUT_PATTERN.search(body))
    return {
        "has_figure": has_figure,
        "has_math": has_math,
        "has_code": has_code,
        "has_example": has_example,
        "score": sum([has_figure, has_math, has_code, has_example]),
    }


# ------------- Heuristic: is this h3 introducing a "technique"? -------------

# Triggers that suggest the h3 is naming a technique/model/algorithm
TECHNIQUE_TITLE_REGEX = re.compile(
    r'(?:'
    # 1. Begins with a capitalized name + optional colon
    r'^[A-Z][A-Za-z0-9\-]+(?:\s+[A-Z][A-Za-z0-9\-]+)*\b'
    # 2. or contains a known technique keyword
    r'|GPT|BERT|CLIP|BLIP|T5|MoE|LoRA|QLoRA|RAG|DPO|PPO|GRPO|RLHF|RLAIF|'
    r'BPE|RoPE|YaRN|FSDP|DDP|MCP|wav2vec|HuBERT|WavLM|EnCodec|SoundStream|'
    r'Whisper|CTC|AST|Conformer|CLAP|AudioCLIP|RAPTOR|RAFT|HyDE|CAG|MMR|'
    r'BERTopic|TIGER|LLaRA|P5|Toolformer|ToolkenGPT|Gorilla|ReAct|MemGPT|'
    r'LangGraph|LangChain|DPR|VITS|Bark|MusicGen|MusicLM|DETR|ViT|Swin|'
    r'DeiT|DINO|SAM|VAE|RVQ'
    r')'
)

# Anti-triggers — h3s that are NOT techniques even if capitalized
NON_TECHNIQUE_KEYWORDS = {
    "exercise", "exercises", "what's next", "summary", "key takeaway",
    "key takeaways", "prerequisites", "official documentation",
    "practical guides", "further reading", "external reading",
    "bibliography", "references", "lab", "background", "context",
    "introduction", "overview", "the rest", "putting it all together",
    "key insight",
}


def looks_like_technique(title: str) -> bool:
    """Heuristic: is this h3 titled with a technique name?"""
    if not title:
        return False
    if title.lower() in NON_TECHNIQUE_KEYWORDS:
        return False
    # Strip section numbering prefix like "27.1.3.2 "
    stripped = re.sub(r'^\d+(\.\d+)*\.?\s+', '', title)
    if stripped.lower() in NON_TECHNIQUE_KEYWORDS:
        return False
    return bool(TECHNIQUE_TITLE_REGEX.match(stripped))


# ------------- Main audit -------------

def audit_file(path: Path) -> list[dict]:
    """Audit one HTML file. Return list of per-technique records."""
    try:
        html = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    # Strip head + nav + footer to focus on main content
    main_match = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
    if main_match:
        html = main_match.group(1)

    blocks = split_into_section_blocks(html)
    records = []
    for blk in blocks:
        if blk["level"] != "h3":
            continue
        if not looks_like_technique(blk["title"]):
            continue
        score = score_block(blk["html"])
        records.append({
            "file": str(path),
            "title": blk["title"],
            "score": score["score"],
            "has_figure": score["has_figure"],
            "has_math": score["has_math"],
            "has_code": score["has_code"],
            "has_example": score["has_example"],
            "body_chars": len(blk["html"]),
        })
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Book root directory")
    parser.add_argument("--scope", default="**/section-*.html",
                        help="Glob (relative to root) for files to audit")
    parser.add_argument("--out", default="slide-summaries/_pedagogy_audit.json")
    args = parser.parse_args()

    root = Path(args.root)
    all_records = []
    for path in sorted(root.glob(args.scope)):
        if "_downloads" in path.parts or "node_modules" in path.parts:
            continue
        all_records.extend(audit_file(path))

    # Tally
    by_score = defaultdict(int)
    for r in all_records:
        by_score[r["score"]] += 1
    total = len(all_records)

    # Most deficient (score 0 or 1), sorted by chapter
    deficient = sorted([r for r in all_records if r["score"] <= 1],
                       key=lambda r: r["file"])

    # Per-chapter median
    by_chapter = defaultdict(list)
    for r in all_records:
        # extract "part-X-name/module-YY-name/" prefix
        p = Path(r["file"])
        parts = p.parts
        # find part-X and module-Y
        chapter_key = "/".join(parts[-3:-1]) if len(parts) >= 3 else str(p.parent)
        by_chapter[chapter_key].append(r["score"])

    chapter_summary = {}
    for ch, scores in by_chapter.items():
        scores_sorted = sorted(scores)
        median = scores_sorted[len(scores_sorted) // 2]
        chapter_summary[ch] = {
            "count": len(scores),
            "median": median,
            "mean": round(sum(scores) / len(scores), 2),
            "score_0_or_1": sum(1 for s in scores if s <= 1),
        }

    output = {
        "total_techniques_detected": total,
        "score_distribution": dict(by_score),
        "score_0_count": by_score[0],
        "score_1_count": by_score[1],
        "score_2_count": by_score[2],
        "score_3_count": by_score[3],
        "score_4_count": by_score[4],
        "deficient": deficient,
        "chapter_summary": chapter_summary,
    }
    out_path = Path(args.out)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"Audited {total} technique sub-sections across {len(by_chapter)} chapters.")
    print(f"Score distribution:")
    for s in sorted(by_score):
        bar = "#" * (40 * by_score[s] // max(total, 1))
        print(f"  {s}/4: {by_score[s]:4d}  {bar}")
    print(f"")
    print(f"  Need work (score <=1): {by_score[0] + by_score[1]} techniques")
    print(f"")
    print(f"Wrote detailed report to: {out_path}")


if __name__ == "__main__":
    main()
