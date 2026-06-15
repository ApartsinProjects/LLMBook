# Graduate-Depth Audit: Part 15 (Research Frontiers)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 75.1 | Emergent Abilities: Real or Mirage? | COURSE-READY | - |
| 75.2 | Scaling Frontiers: What Comes Next | COURSE-READY | - |
| 75.3 | Alternative Architectures Beyond Transformers | COURSE-READY | - |
| 75.3a | Linear Attention, Hybrids, Benchmarks, Neuromorphic | COURSE-READY | - |
| 75.4 | Beyond Text: LLMs as Universal Sequence Machines | CATALOG-OK | Marked GIANT_SECTION catalog-by-design; surveys per-domain tokenizers (DNA, protein, chem, time-series, EHR). |
| 76.1 | A Theory of Reasoning in LLMs | COURSE-READY | - |
| 76.2 | Memory as a Computational Primitive | COURSE-READY | - |
| 76.3 | Mechanistic Interpretability at Scale | COURSE-READY | - |
| 76.4 | The Nature of Agency | COURSE-READY | - |
| 77.1 | Frontier Benchmarks: HLE, ARC-AGI-2, FrontierMath | COURSE-READY | - |
| 77.2 | Alignment at Frontier Scale | COURSE-READY | - |
| 77.3 | AGI Timelines: The 2027-2033 Spectrum | COURSE-READY | - |
| 77.4 | Economic Implications and Labor-Market Data | COURSE-READY | - |
| 77.5 | What 2026 Settled (and What Remains Open) | DEPTH-GAP | Reflective closing essay (first-person retrospective, three theses, junior-engineer advice). No analytical mechanism or framed technical open problems in the body; it is an attitude/epilogue piece, not a lecturable seminar. |
| 78.1 | Platforms | CATALOG-OK | Paper-discovery venue catalog (arXiv, OpenReview, lab blogs); intentional tools-of-the-trade index. |
| 78.2 | (Libraries / research stack) | CATALOG-OK | Tools-of-the-trade catalog by chapter design. |
| 78.3 | (Libraries / research stack) | CATALOG-OK | Tools-of-the-trade catalog by chapter design. |
| 78.4 | (Libraries / research stack) | CATALOG-OK | Tools-of-the-trade catalog by chapter design. |
| 78.5 | External Reading and Communities | CATALOG-OK | Durable-venue and community reading list; intentional closing index. |

## Summary
- COURSE-READY: 12 | DEPTH-GAP: 1 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 6
- Top sections most worth enriching:
  1. **77.5 (What 2026 Settled)**: the one DEPTH-GAP. Add a short framed-open-problems block (3 to 4 named, measurable technical questions: e.g., does test-time-compute scaling plateau, does weak-to-strong certification become possible, does SAE feature steering survive the carve-the-joints critique) so the closing section is lecturable analytically and not only as a personal epilogue.
  2. **77.1 (Frontier Benchmarks)**: strongest of the module-77 briefings but lightest on derivation; would benefit from one worked construct-validity argument (why a continuous re-scoring of one named benchmark dissolves an apparent emergence) to lift it from sharp survey to mechanism.
  3. **75.4 (Universal Sequence Machines)**: correctly CATALOG-OK, but it carries unusually strong exercises and a "tokenizer is the theory" thesis; a single deeper case study (one domain worked end to end with the information-vs-context-length tradeoff quantified) would let part of it double as analytical content without breaking the catalog framing.
