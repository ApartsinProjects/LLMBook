"""v6.1: First batch of orphan-caption fixes.

Strategy from the v6.1 classification audit (52 orphans):
  Tier A (42): substantial code blocks needed         -> deferred to v6.2
  Tier B (6):  short install / single-line snippets   -> insert here
  Tier C (4):  output, pseudocode, prose-only         -> convert or delete here

This batch handles Tiers B and C. Tier A is too much for one commit.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# -- Tier B: install/short snippets to inject before each caption ----

INSTALL_SNIPPETS = {
    'part-1-foundations/module-02-tokenization-subword-models/section-2.3.html': {
        '2.3.22': 'pip install transformers',
    },
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html': {
        '6.4.8': 'pip install datasets',
    },
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html': {
        '6.6.7': 'pip install accelerate',
    },
    'part-10-frontiers/module-18-interpretability/section-18.3.html': {
        '18.3.13': 'pip install nnsight',
    },
}

# Section 5.3 CF 5.3.3 — 8-line outlines example
OUTLINES_EXAMPLE = '''# Outlines: enforce a regex constraint on generated text.
# Useful when you need a strictly formatted answer (e.g. a date, a
# version number, a phone number) without any post-processing.
from outlines import models, generate

model = models.transformers("gpt2")
# Match a US ZIP code: 5 digits, optional -4 suffix
generator = generate.regex(model, r"\\d{5}(-\\d{4})?")
print(generator("Customer's billing ZIP: "))
# Output is GUARANTEED to match the regex'''

# Section 26.4 CF 26.4.1 - ResilientAgent definition stub
RESILIENT_AGENT = '''import asyncio
from dataclasses import dataclass
from typing import Callable

@dataclass
class ResilientAgent:
    """An agent wrapper that adds retry, timeout, and circuit-breaker logic
    around any LLM call. The pattern: try once; on failure, back off and
    retry; if failure rate over the last N calls exceeds a threshold,
    open the circuit and short-circuit further calls for a cool-down period.
    """
    inner: Callable[[str], str]      # the underlying LLM call
    max_retries: int = 3
    timeout_s: float = 30.0
    failure_threshold: float = 0.3
    cool_down_s: float = 60.0

    def __post_init__(self):
        self._recent: list[bool] = []
        self._circuit_open_until: float = 0.0

    async def __call__(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        if loop.time() < self._circuit_open_until:
            raise RuntimeError("circuit breaker open; cool-down in effect")
        for attempt in range(self.max_retries):
            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, self.inner, prompt),
                    timeout=self.timeout_s,
                )
                self._record(True)
                return result
            except (asyncio.TimeoutError, Exception):
                self._record(False)
                await asyncio.sleep(2 ** attempt)         # exponential backoff
        self._maybe_open_circuit(loop.time())
        raise RuntimeError(f"all {self.max_retries} retries failed")

    def _record(self, success: bool) -> None:
        self._recent = (self._recent + [success])[-20:]   # keep last 20

    def _maybe_open_circuit(self, now: float) -> None:
        if len(self._recent) < 10:
            return
        failure_rate = 1 - (sum(self._recent) / len(self._recent))
        if failure_rate >= self.failure_threshold:
            self._circuit_open_until = now + self.cool_down_s'''

CODE_BLOCKS = [
    # (file_rel, caption_num, body_text)
    *[(f, k, v) for f, d in INSTALL_SNIPPETS.items() for k, v in d.items()],
    ('part-1-foundations/module-05-decoding-text-generation/section-5.3.html', '5.3.3', OUTLINES_EXAMPLE),
    ('part-6-agentic-ai/module-26-agent-safety-production/section-26.4.html', '26.4.1', RESILIENT_AGENT),
]


def insert_code_before_caption(file_rel: str, cap_num: str, body: str) -> bool:
    p = ROOT / file_rel
    text = p.read_text(encoding='utf-8')
    pat = re.compile(
        r'(<div class="code-caption"><strong>Code Fragment '
        + re.escape(cap_num) + r':</strong>)'
    )
    m = pat.search(text)
    if not m:
        print(f'  NO MATCH for CF {cap_num} in {file_rel}')
        return False
    # Idempotent: check if there's already a <pre> in the 1500 chars before
    if '<pre' in text[max(0, m.start() - 1500):m.start()]:
        # Check more precisely if the immediately-preceding pre has matching content
        # Simplest: skip if already inserted (look for first 30 chars of body)
        signature = body.split('\n')[0][:40]
        if signature and signature in text[max(0, m.start() - 1800):m.start()]:
            print(f'  already inserted: CF {cap_num}')
            return False

    # Insert a new code block before the caption
    is_install = body.startswith('pip install') or body.startswith('!pip')
    lang = 'lang-bash' if is_install else 'lang-python'
    new_block = (
        f'<div class="code-block-wrapper">\n'
        f'<pre><code class="{lang}">{body}</code></pre>\n'
        f'</div>\n'
    )
    new_text = text[:m.start()] + new_block + text[m.start():]
    p.write_text(new_text, encoding='utf-8')
    print(f'  inserted CF {cap_num} ({len(body)} chars) in {file_rel}')
    return True


# -- Tier C: convert/delete --------------------------------------------

# CF D.6.2 - "Expected output" -> retag the existing caption to use code-output styling.
# CF 3.1.3 - "Compare parameter counts" - DELETE the orphan caption (the prose explains it)
# CF 4.4.3 - "Each program handles one row" - DELETE the orphan caption
# CF 5.1.11 - "Pseudocode for beam search" - retag as lang-text and add the pseudocode

DELETE_CAPTIONS = [
    ('part-1-foundations/module-03-sequence-models-attention/section-3.1.html', '3.1.3'),
    ('part-1-foundations/module-04-transformer-architecture/section-4.4.html', '4.4.3'),
]

# Beam search pseudocode (CF 5.1.11)
BEAM_SEARCH_PSEUDO = '''Algorithm: Beam Search Decoding
Input:  model M, prompt tokens x, beam width k, max length T
Output: the most probable continuation y

  beams := [(score=0.0, tokens=x)]               # one initial beam: the prompt
  for t in 1..T:
      cands := []
      for (score, tokens) in beams:
          if tokens[-1] == EOS: cands.append((score, tokens)); continue
          probs := M.next_token_logits(tokens)
          probs := softmax(probs)
          for token, p in topk(probs, k):
              cands.append((score + log p, tokens + [token]))
      beams := topk(cands, k, key=score)         # keep best k expansions
      if all beams end in EOS: break

  return argmax_score(beams).tokens'''

# CF D.6.2: expected output text
EXPECTED_OUTPUT_D62 = '''Python: 3.11.7
PyTorch: 2.4.0+cu124
CUDA available: True
CUDA device: NVIDIA RTX 4090 (24.0 GB)
Transformers: 4.45.2
Datasets: 3.0.1
Accelerate: 1.0.1
PEFT: 0.13.0'''


def delete_caption(file_rel: str, cap_num: str) -> bool:
    p = ROOT / file_rel
    text = p.read_text(encoding='utf-8')
    pat = re.compile(
        r'<div class="code-caption"><strong>Code Fragment '
        + re.escape(cap_num) + r':</strong>[^<]*</div>\s*\n?'
    )
    new, n = pat.subn('', text, count=1)
    if n:
        p.write_text(new, encoding='utf-8')
        print(f'  deleted orphan CF {cap_num} caption in {file_rel}')
    return bool(n)


def main() -> int:
    inserted = 0
    for fr, cap, body in CODE_BLOCKS:
        if insert_code_before_caption(fr, cap, body):
            inserted += 1
    # Beam search pseudocode (5.1.11)
    if insert_code_before_caption(
        'part-1-foundations/module-05-decoding-text-generation/section-5.1.html',
        '5.1.11', BEAM_SEARCH_PSEUDO,
    ):
        inserted += 1
    # Expected output (D.6.2)
    if insert_code_before_caption(
        'appendices/appendix-d-environment-setup/section-d.6.html',
        'D.6.2', EXPECTED_OUTPUT_D62,
    ):
        inserted += 1
    # Delete the 2 trivial orphan captions
    deleted = 0
    for fr, cap in DELETE_CAPTIONS:
        if delete_caption(fr, cap):
            deleted += 1
    print(f'\nInserted {inserted} code blocks, deleted {deleted} captions.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
