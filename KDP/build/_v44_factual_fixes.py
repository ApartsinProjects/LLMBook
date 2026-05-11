"""v4.4: Verifiable factual corrections from chapter-review audit.

These are SPECIFIC errors with known-correct values from authoritative
sources (papers, official docs).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def safe_read(p: Path) -> str | None:
    try:
        if p.stat().st_size > 5_000_000: return None
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


# (file_path, [(old_text, new_text, label)])
FIXES = [
    ("part-7-multimodal-applications/module-27-multimodal/section-27.5.html", [
        ("PaLM-E (12B VLM)", "PaLM-E (562B VLM)", "PaLM-E parameter count"),
        ("PaLM-E (12B)", "PaLM-E (562B)", "PaLM-E param count alt"),
    ]),
    ("part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html", [
        ("LSTM, covered in Chapter 00", "LSTM, covered in Chapter 3", "LSTM xref"),
        ("LSTMs covered in Chapter 00", "LSTMs covered in Chapter 3", "LSTM xref alt"),
        ("see Chapter 00 for details on LSTM", "see Chapter 3 for details on LSTM", "LSTM xref alt2"),
    ]),
    ("part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html", [
        ("GRPO halves GPU memory compared to PPO",
         "GRPO saves roughly 1/3 of GPU memory vs PPO (the value model is dropped, but the policy and reward models still consume the bulk of memory)",
         "GRPO memory claim"),
        ("PRMs solve roughly 15% more problems than ORMs",
         "PRMs solve roughly 9 percentage points more problems than ORMs (Lightman et al., 2023)",
         "PRM uplift"),
    ]),
    ("part-2-understanding-llms/module-09-inference-optimization/section-9.6.html", [
        ("doubling model size requires roughly doubling the training compute",
         "doubling model size requires roughly 4x the training compute (Chinchilla scaling: D should scale with N)",
         "Chinchilla scaling"),
    ]),
    ("part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html", [
        ("Best-of-N improvement is logarithmic with N",
         "Best-of-N expected pass rate is 1 - (1-p)^N, which is exponential approach to 1 (each doubling of N gives diminishing returns, but the curve is not logarithmic)",
         "Best-of-N scaling"),
    ]),
    ("part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html", [
        ("Best-of-N improvement is logarithmic with N",
         "Best-of-N expected pass rate is 1 - (1-p)^N, exponential approach to 1",
         "Best-of-N scaling alt"),
    ]),
    ("part-7-multimodal-applications/module-28-llm-applications/section-28.1.html", [
        ("the best AI coding agents solve about 50% of real GitHub issues",
         "the best AI coding agents solve 70%+ of SWE-Bench Verified issues (as of late 2025)",
         "AI coding agent benchmark"),
        ("solve about 50% of real GitHub issues",
         "solve 70%+ of SWE-Bench Verified issues (as of late 2025)",
         "AI coding agent alt"),
    ]),
    ("part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html", [
        # Fix temperature listed as regression example (it's actually OK if it
        # means 'predict the temperature reading') -- but cross-ref to 5.2
        # (sampling temperature) is clearly wrong. Drop the link.
        ('href="../module-05-decoding-text-generation/section-5.2.html">temperature</a>',
         "temperature",
         "Strip 0.1 temperature wrong xref"),
    ]),
]


def main() -> int:
    n_files = 0
    n_fixes = 0
    for rel, replacements in FIXES:
        p = ROOT / rel
        text = safe_read(p)
        if text is None:
            print(f"  [skip] {rel} not found")
            continue
        original = text
        local = 0
        for old, new, label in replacements:
            if old in text:
                text = text.replace(old, new)
                local += 1
                print(f"  {rel.split('/')[-1]}: {label}")
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += local

    print(f"\nTotal: {n_fixes} factual fixes in {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
