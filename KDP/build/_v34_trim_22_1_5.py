"""v3.4 Wave A: Trim 22.1.5 'Agent Memory Systems' (9600 words) to a brief
teaser + cross-reference, since the canonical treatment now lives in 22.6
'Memory Architecture for Agents' (formerly 22.7).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "part-6-agentic-ai/module-22-ai-agents/section-22.1.html"


REPLACEMENT = '''<h2>22.1.5 Agent Memory Systems</h2>
<p>
 Agents need memory beyond the single context window. We sketch the
 categories briefly here; <a class="cross-ref" href="section-22.6.html">Section 22.6</a>
 covers the full taxonomy, storage strategies, retrieval policies, and
 production patterns.
</p>
<ul>
<li><strong>Working memory</strong>: the live context window during a turn (system
prompt, user message, tool results, reasoning traces). Bounded by the model's
context limit; the engineering question is what to keep and what to evict.</li>
<li><strong>Episodic memory</strong>: records of past interactions stored outside
the context window so the agent can recall what happened in earlier sessions.
Typically a vector database keyed by user/session/topic.</li>
<li><strong>Semantic memory</strong>: extracted facts, preferences, and learned
heuristics that persist across sessions. Distilled from episodic memory or
populated by the agent's own reflection step.</li>
<li><strong>Procedural memory</strong>: skill libraries, tool descriptions, and
learned routines the agent invokes by name. Often stored as structured
templates or callable code rather than embeddings.</li>
</ul>
<p>
 The hard problems (when to write, when to retrieve, how to compress, how to
 forget, how to prevent contamination across users) are the topic of
 <a class="cross-ref" href="section-22.6.html">Section 22.6</a>.
</p>
'''


def main() -> int:
    text = SRC.read_text(encoding="utf-8", errors="replace")
    # Find the 22.1.5 block: from <h2>22.1.5 ... up to next <h2>22.1.6
    pattern = re.compile(
        r'<h2[^>]*>\s*22\.1\.5\s+Agent Memory Systems\s*</h2>.*?(?=<h2[^>]*>\s*22\.1\.6)',
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        print("[skip] 22.1.5 block not found - already trimmed?")
        return 0
    old_words = len(re.sub(r'<[^>]+>', ' ', match.group(0)).split())
    new_words = len(re.sub(r'<[^>]+>', ' ', REPLACEMENT).split())
    new_text = text[:match.start()] + REPLACEMENT + text[match.end():]
    SRC.write_text(new_text, encoding="utf-8")
    print(f"  Trimmed 22.1.5: {old_words} -> {new_words} words ({old_words - new_words} removed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
